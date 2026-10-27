import {dirname, resolve} from 'node:path';
import {readFile} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import { t } from './i18n.ts';
// ForceReply uses the existing OpenClaw Telegram send/cache/receipt route, with no poller.
// The public extension API provides account and transport helpers. Three client helpers
// still need a compatibility bridge: resolve their named exports from the installed build's
// own export table instead of hardcoding content hashes or minified export aliases.
// No version pin: any OpenClaw release whose modules still provide every helper below works;
// one that doesn't throws here, and the service falls back to the plain prompt.
const DIST=process.env.OPENCLAW_PACKAGE_DIR||resolve(dirname(process.execPath),'..','lib','node_modules','openclaw');
export async function telegramInternals() {
  const manifest=JSON.parse(await readFile(resolve(DIST,'package.json'),'utf8'));
  if(manifest.name!=='openclaw') throw Error('OpenClaw not found next to this Node');
  const entry=resolve(DIST,'dist/extensions/telegram/runtime-api.js');
  const source=await readFile(entry,'utf8');
  const sendPath=source.match(/import \{[^}]*\bas sendMessageTelegram\b[^}]*\} from "([^"\n]+)"/);
  if(!sendPath) throw Error('Telegram send module unavailable');
  const sendFile=resolve(dirname(entry),sendPath[1]);
  if(!sendFile.startsWith(resolve(DIST,'dist')+'/')) throw Error('Unexpected Telegram send module');
  const sendSource=await readFile(sendFile,'utf8');
  const table=sendSource.match(/export \{ ([^}]+) \};\s*$/)?.[1];
  const [account,runtime,send,{Bot}]=await Promise.all([
    import(pathToFileURL(resolve(DIST,'dist/extensions/telegram/api.js')).href),
    import(pathToFileURL(entry).href),import(pathToFileURL(sendFile).href),
    import(pathToFileURL(resolve(DIST,'node_modules/grammy/out/mod.js')).href)]);
  const helpers:any={};
  for(const name of ['getOrCreateAccountThrottler','createTelegramClientFetch','asTelegramClientFetch']) {
    const alias=table?.split(',').map(x=>x.trim().split(/\s+as\s+/)).find(x=>x[0]===name)?.[1];
    if(!alias||typeof send[alias]!=='function') throw Error('Telegram client helper unavailable: '+name);
    helpers[name]=send[alias];
  }
  const result={resolveTelegramAccount:account.resolveTelegramAccount,sendMessageTelegram:runtime.sendMessageTelegram,
    resolveTelegramTransport:runtime.resolveTelegramTransport,makeProxyFetch:runtime.makeProxyFetch,Bot,...helpers};
  if(Object.values(result).some(x=>typeof x!=='function')) throw Error('Incomplete Telegram API');
  return result;
}

export function forceReplyPayload(method: string, payload: any, cardId: string, owner: string) {
  if (method !== 'sendMessage') return payload;
  if (!owner || String(payload.chat_id) !== String(owner)) throw new Error('Wrong Change recipient');
  return {...payload, reply_parameters:{message_id:Number(cardId)},
    reply_markup:{force_reply:true,input_field_placeholder:t('Your reply')}};
}
// `text` is the service's prompt_text(), so a cached copy can be matched exactly on recovery.
export async function sendChangePrompt(cfg: any, cardId: string, text: string, confirmed?: (id:string)=>Promise<void>, owner = '', accountId = 'default') {
  let admitted=false,transport:any;
  try {
  if (!/^\d+$/.test(cardId) || !/^-?\d+$/.test(String(owner))) throw new Error('Missing suggestion card');
  const {resolveTelegramAccount, sendMessageTelegram, getOrCreateAccountThrottler, createTelegramClientFetch,
    asTelegramClientFetch, resolveTelegramTransport, makeProxyFetch, Bot} = await telegramInternals();
  const account=resolveTelegramAccount({cfg,accountId});
  transport=resolveTelegramTransport(account.config.proxy ? makeProxyFetch(account.config.proxy) : undefined,{network:account.config.network});
    const clientFetch=createTelegramClientFetch({fetchImpl:asTelegramClientFetch(transport.fetch),transport});
    const bot=new Bot(account.token,{client:{...(clientFetch?{fetch:asTelegramClientFetch(clientFetch)}:{}),...(account.config.apiRoot?{apiRoot:account.config.apiRoot}:{})}});
    bot.api.config.use(getOrCreateAccountThrottler(account.token).transformer);
    bot.api.config.use(async(previous,method,payload,signal)=>{
      const result=await previous(method,forceReplyPayload(method,payload,cardId,owner),signal);
      // Save Telegram's accepted identity before OpenClaw's later cache/bookkeeping.
      if(method==='sendMessage'&&result?.ok&&result.result?.message_id){
        try{await confirmed?.(String(result.result.message_id));}catch{/* Never turn an accepted send into a transport retry. Final receipt saving can retry. */}
      }
      return result;
    });
    admitted=true;
    const result=await sendMessageTelegram(String(owner),text.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])),{cfg,accountId,api:bot.api,textMode:'html',replyToMessageId:Number(cardId)});
    if (!result?.messageId) throw new Error('Unconfirmed Change prompt');
    await confirmed?.(String(result.messageId));
    return String(result.messageId);
  } catch {
    throw Object.assign(new Error('Change prompt '+(admitted?'outcome unknown':'setup unavailable')),{definitelyNotSent:!admitted});
  } finally {try{await transport?.close?.();}catch{/* A cleanup failure never invalidates a saved receipt. */}}
}
