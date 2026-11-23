import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,mkdtemp,rm} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {dirname,join} from 'node:path';import {tmpdir} from 'node:os';
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
 // Where OpenClaw builds keep the three client helpers, as small stand-ins for the real package: pull requests run the
 // pinned release only, so the newer layout is checked here too. A module outside OpenClaw's dist is never read.
 const layouts={
  // up to 2026.11.4: the fetch helpers in the send module, the throttler imported by it
  'send module':{'send-1.mjs':'import { t as getOrCreateAccountThrottler } from "./chunk-1.mjs";\nfunction sendMessageTelegram() {}\nfunction createTelegramClientFetch() { return 1; }\nfunction asTelegramClientFetch() { return 2; }\nexport { sendMessageTelegram as n, createTelegramClientFetch as a, asTelegramClientFetch as b };\n',
   'chunk-1.mjs':'function getOrCreateAccountThrottler() { return 3; }\nexport { getOrCreateAccountThrottler as t };\n'},
  // from 2026.11.5: the fetch helpers in the outbound module, the throttler in another; the send module imports neither helper
  'outbound module':{'send-1.mjs':'import { n as other } from "./outbound-1.mjs";\nfunction sendMessageTelegram() {}\nexport { sendMessageTelegram as n };\n',
   'outbound-1.mjs':'import { t as getOrCreateAccountThrottler } from "./gate-1.mjs";\nfunction other() {}\nfunction createTelegramClientFetch() { return 1; }\nfunction asTelegramClientFetch() { return 2; }\nexport { other as n, createTelegramClientFetch as a, asTelegramClientFetch as b };\n',
   'gate-1.mjs':'import "./outbound-1.mjs";\nfunction getOrCreateAccountThrottler() { return 3; }\nexport { getOrCreateAccountThrottler as t };\n'},
  // removed: nothing guessed, the plain prompt goes out instead
  removed:{'send-1.mjs':'import { n as other } from "./outbound-1.mjs";\nfunction sendMessageTelegram() {}\nexport { sendMessageTelegram as n };\n',
   'outbound-1.mjs':'function other() {}\nfunction createTelegramClientFetch() { return 1; }\nfunction asTelegramClientFetch() { return 2; }\nexport { other as n, createTelegramClientFetch as a, asTelegramClientFetch as b };\n'},
  // outside dist: not read
  outside:{'send-1.mjs':'import { t as getOrCreateAccountThrottler } from "../outside.mjs";\nfunction sendMessageTelegram() {}\nfunction createTelegramClientFetch() { return 1; }\nfunction asTelegramClientFetch() { return 2; }\nexport { sendMessageTelegram as n, createTelegramClientFetch as a, asTelegramClientFetch as b };\n',
   '../outside.mjs':'function getOrCreateAccountThrottler() { return 3; }\nexport { getOrCreateAccountThrottler as t };\n'}};
 const probe=join(dir,'probe.mjs');
 await writeFile(probe,`import {telegramInternals} from ${JSON.stringify(new URL('../openclaw-plugin/change-prompt.ts',import.meta.url).href)};
try{const r=await telegramInternals();console.log([r.createTelegramClientFetch(),r.asTelegramClientFetch(),r.getOrCreateAccountThrottler()].join())}catch(e){console.log(e.message)}`);
 for(const [name,files] of Object.entries(layouts)) {
  const pkg=join(dir,name.replace(' ','-')),put=async(path,text)=>{const to=join(pkg,path);await mkdir(dirname(to),{recursive:true});await writeFile(to,text)};
  await put('package.json','{"name":"openclaw","type":"module"}');
  await put('node_modules/grammy/out/mod.js','export class Bot {}\n');
  await put('dist/extensions/telegram/api.js','export function resolveTelegramAccount() {}\n');
  await put('dist/extensions/telegram/runtime-api.js','import { n as sendMessageTelegram } from "../../send-1.mjs";\nfunction resolveTelegramTransport() {}\nfunction makeProxyFetch() {}\nexport { sendMessageTelegram, resolveTelegramTransport, makeProxyFetch };\n');
  for(const [path,text] of Object.entries(files))await put('dist/'+path,text);
  const found=execFileSync(process.execPath,[probe],{env:{...process.env,OPENCLAW_PACKAGE_DIR:pkg},timeout:30000}).toString().trim();
  assert.equal(found,['removed','outside'].includes(name)?'Telegram client helper unavailable: getOrCreateAccountThrottler':'1,2,3',name);
 }
 console.log('Change prompt: helpers found in both layouts, pre-send classification, accepted receipt before bookkeeping and cleanup fencing passed.');
}finally{await rm(dir,{recursive:true,force:true})}
