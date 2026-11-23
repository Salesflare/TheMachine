// Load the real installed SDK, without a Gateway or a live Telegram send. Stub-only tests
// cannot detect packaging changes, missing modules, or renamed minified exports.
import {FIXTURE,ROOT} from './test-env.mjs';
import assert from 'node:assert/strict';
import {gatewayRuntime,OPENCLAW} from '../openclaw-root.mjs';
import {telegramInternals} from '../openclaw-plugin/change-prompt.ts';
import {execFileSync} from 'node:child_process';
const telegram=await telegramInternals();
for(const name of ['resolveTelegramAccount','sendMessageTelegram','getOrCreateAccountThrottler',
                  'createTelegramClientFetch','asTelegramClientFetch','resolveTelegramTransport','makeProxyFetch','Bot'])
  assert.equal(typeof telegram[name],'function',name);
// The Change prompt's helper end to end on this OpenClaw, against a local stand-in for Telegram's Bot API (a made-up token,
// nothing leaves this computer): one reply prompt with the force-reply box, its receipt saved, and only the answer on
// stdout. The service reads that as JSON; OpenClaw's log line in front of it left the prompt unconfirmed for a minute.
{
  const {createServer}=await import('node:http'),{spawn}=await import('node:child_process');
  const {mkdirSync,writeFileSync,readFileSync:read}=await import('node:fs');
  const calls=[];
  const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;
    const sent=JSON.parse(body||'{}');calls.push([req.url.split('/').pop(),sent]);res.setHeader('Content-Type','application/json');
    res.end(JSON.stringify({ok:true,result:{message_id:777,date:1,chat:{id:1000001,type:'private'},from:{id:1,is_bot:true,first_name:'Bot'},text:sent.text}}))});
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  const home=FIXTURE+'/telegram',receipts=home+'/receipts';mkdirSync(home);
  writeFileSync(home+'/openclaw.json',JSON.stringify({channels:{telegram:{enabled:true,botToken:'1:'+'A'.repeat(35),
    apiRoot:'http://127.0.0.1:'+server.address().port,dmPolicy:'allowlist',allowFrom:['1000001']}}}));
  const clean=Object.fromEntries(Object.entries(process.env).filter(([k])=>!/^(OPENCLAW_|XDG_|(https?|all|no)_proxy$)/i.test(k)));
  const child=spawn(process.execPath,[ROOT+'/change-prompt-run.mjs'],{env:{...clean,HOME:home,OPENCLAW_STATE_DIR:home+'/state',
    OPENCLAW_CONFIG_PATH:home+'/openclaw.json',OPENCLAW_PACKAGE_DIR:OPENCLAW,ASSISTANT_PROMPT_RECEIPTS:receipts}});
  let out='',err='';child.stdout.on('data',d=>out+=d);child.stderr.on('data',d=>err+=d);
  child.stdin.end(JSON.stringify({receipt_key:'a'.repeat(64),card_id:'40',text:'Synthetic <to-do>',target:'1000001'}));
  const stop=setTimeout(()=>child.kill('SIGKILL'),60000);
  const code=await new Promise(r=>child.on('close',r));clearTimeout(stop);server.closeAllConnections();server.close();
  const said=`exit ${code}, stdout ${out}, stderr ${err.slice(-600)}`;
  const sends=calls.filter(([method])=>method==='sendMessage').map(([,payload])=>payload);
  assert.equal(sends.length,1,'one prompt sent: '+said);
  assert.deepEqual([String(sends[0].chat_id),sends[0].reply_parameters?.message_id,sends[0].reply_markup?.force_reply,sends[0].text],
    ['1000001',40,true,'Synthetic &lt;to-do&gt;']);
  assert.equal(out,'{"messageId":"777"}','only the answer on stdout: '+said);assert.equal(code,0,said);
  assert.deepEqual(JSON.parse(read(receipts+'/'+'a'.repeat(64)+'.json','utf8')),{messageId:'777'});
}
assert.equal(typeof (await gatewayRuntime()).callGatewayFromCli,'function');
assert.equal(typeof (await import(OPENCLAW+'/dist/plugin-sdk/runtime-config-snapshot.js')).getRuntimeConfig,'function');
for(const file of ['runtime-config-snapshot','system-event-runtime','plugin-entry'])
  assert.ok(Object.keys(await import(OPENCLAW+'/dist/plugin-sdk/'+file+'.js')).length);
// The phone feed (android-feed.ts) removes the notifications it saved from the main session's queue by id, and only those.
{
  const events=await import(OPENCLAW+'/dist/plugin-sdk/system-event-runtime.js'), key='agent:main:feed-compat-test';
  for(const [text,contextKey] of [['Notification posted one','notification:one'],['Another plugin','other:two']])
    assert.ok(events.enqueueSystemEvent(text,{sessionKey:key,contextKey}));
  const [first]=events.peekSystemEventEntries(key,'main');
  assert.equal(events.consumeSelectedSystemEventEntries(key,[{id:first.id}]).length,1);
  assert.deepEqual(events.peekSystemEventEntries(key,'main').map(e=>e.contextKey),['other:two']);
  events.drainSystemEventEntries(key);
}
// Exercise real capability admission too, always in a separate disposable OpenClaw home.
const env=Object.fromEntries(Object.entries(process.env).filter(([k])=>!k.startsWith('OPENCLAW_')));
Object.assign(env,{HOME:FIXTURE,OPENCLAW_STATE_DIR:FIXTURE+'/state',OPENCLAW_CONFIG_PATH:FIXTURE+'/openclaw.json'});
delete env.XDG_CONFIG_HOME; delete env.XDG_DATA_HOME;
execFileSync(process.execPath,[OPENCLAW+'/openclaw.mjs','plugins','install','--link','--force',
  '--accept-capabilities',ROOT+'/openclaw-plugin'],{env,timeout:120000,stdio:'pipe'});
// Card chat reads a card's session with the pinned official Gateway client (package-lock.json), never private files:
// the wire version and the chat.history contract it relies on, against the installed OpenClaw's own docs.
import {readFileSync} from 'node:fs';
const lock=JSON.parse(readFileSync(ROOT+'/package-lock.json','utf8')).packages;
for(const name of ['@openclaw/gateway-client','@openclaw/gateway-protocol'])
  assert.equal(JSON.parse(readFileSync(ROOT+'/node_modules/'+name+'/package.json','utf8')).version,lock['node_modules/'+name].version,name);
const {GatewayClient}=await import('@openclaw/gateway-client');
const {PROTOCOL_VERSION}=await import('@openclaw/gateway-protocol/version');
assert.equal(typeof GatewayClient,'function');
assert.match(readFileSync(OPENCLAW+'/docs/gateway/clients.md','utf8'),new RegExp('current wire version is `'+PROTOCOL_VERSION+'`'));
const schema=JSON.parse(readFileSync(ROOT+'/node_modules/@openclaw/gateway-protocol/protocol.schema.json','utf8'));
assert.equal(schema.methods['chat.history'].scope,'operator.read');
for(const key of ['sessionKey','cursor','limit','maxChars'])assert.ok(schema.definitions.ChatHistoryParams.properties[key],key);
for(const key of ['kind','messages','deltaCursor','inFlightRun'])assert.ok(schema.definitions.ChatHistoryDeltaResult.properties[key],key);
// The helper refuses anything but a card's session, and says only "unavailable" without a Gateway.
const helper=(request,extra={})=>JSON.parse(execFileSync(process.execPath,[ROOT+'/chat-history-run.mjs'],{input:JSON.stringify(request),env:{...env,...extra},timeout:30000,stdio:['pipe','pipe','ignore']}).toString()||'{}');
// The helper asks for read access only (and defines it: a missing name would only show as unavailable).
assert.match(readFileSync(ROOT+'/chat-history-run.mjs','utf8'),/^const SCOPES = \['operator\.read'\];$/m);
assert.throws(()=>helper({session_key:'agent:main:main',limit:10},{ASSISTANT_STATE_DIR:FIXTURE+'/chat'}));
assert.throws(()=>helper({session_key:'agent:main:assistant-review-preparation-'+'a'.repeat(32),limit:10},{ASSISTANT_STATE_DIR:'chat'}));
{const r=helper({session_key:'agent:main:assistant-review-preparation-'+'a'.repeat(32),limit:10},{ASSISTANT_STATE_DIR:FIXTURE+'/chat',OPENCLAW_CONFIG_PATH:FIXTURE+'/none.json',OPENCLAW_GATEWAY_PORT:'9'});
 assert.equal(r.error,'unavailable');assert.ok(['timeout','auth','offline','other'].includes(r.reason),'only a fixed word for why: '+JSON.stringify(r));assert.deepEqual(Object.keys(r).sort(),['error','reason'])}
console.log('Pinned SDK and Telegram transport loaded; real plugin installation passed in a disposable home; the Change prompt reached a local stand-in for Telegram. No Gateway or live send.');
