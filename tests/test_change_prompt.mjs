import assert from 'node:assert/strict';
import {readFile,writeFile,mkdtemp,rm} from 'node:fs/promises';
import {join} from 'node:path';import {tmpdir} from 'node:os';
let source=await readFile(new URL('../openclaw-plugin/change-prompt.ts',import.meta.url),'utf8');
const start=source.indexOf('export async function telegramInternals()'),end=source.indexOf('export function forceReplyPayload');
source=source.slice(0,start)+'async function telegramInternals(){return globalThis.internals();}\n'+source.slice(end);
source=source.replace("'./i18n.ts'",JSON.stringify(new URL('../openclaw-plugin/i18n.ts',import.meta.url).href));  // the copy runs from a temp folder
const dir=await mkdtemp(join(tmpdir(),'assistant-prompt-'));
try{
 const file=join(dir,'prompt.ts');await writeFile(file,source);const {sendChangePrompt}=await import(file);
 let transforms=[],accepted=[];
 class Bot {constructor(){this.api={config:{use:f=>transforms.push(f)}}}}
 const setup=(send,close=async()=>{})=>globalThis.internals=async()=>({resolveTelegramAccount:()=>({token:'synthetic',config:{}}),resolveTelegramTransport:()=>({fetch:()=>{},close}),createTelegramClientFetch:()=>null,asTelegramClientFetch:x=>x,getOrCreateAccountThrottler:()=>({transformer:async(prev,...args)=>prev(...args)}),makeProxyFetch:()=>null,Bot,sendMessageTelegram:send});
 globalThis.internals=async()=>{throw Error('Missing internal module')};
 await assert.rejects(sendChangePrompt({},'123','Synthetic',undefined,'1000001'),error=>error.definitelyNotSent===true);
 setup(async()=>{throw Error('Response lost')});
 await assert.rejects(sendChangePrompt({},'123','Synthetic',undefined,'1000001'),error=>error.definitelyNotSent===false);
 setup(async()=>{
  await transforms.at(-1)(async()=>({ok:true,result:{message_id:456}}),'sendMessage',{chat_id:'1000001'},undefined);
  throw Error('Bookkeeping failed after Telegram accepted');
 });
 await assert.rejects(sendChangePrompt({},'123','Synthetic',async id=>accepted.push(id),'1000001'),error=>error.definitelyNotSent===false);
 assert.deepEqual(accepted,['456']);
 setup(async()=>({messageId:'456'}),async()=>{throw Error('Cleanup failed')});
 assert.equal(await sendChangePrompt({},'123','Synthetic',undefined,'1000001'),'456');
 console.log('Change prompt: pre-send classification, accepted receipt before bookkeeping and cleanup fencing passed.');
}finally{await rm(dir,{recursive:true,force:true})}
