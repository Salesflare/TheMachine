import assert from 'node:assert/strict';
import { readFile, writeFile, mkdtemp, rm, readdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
const fixtureDir=await mkdtemp(join(tmpdir(),'assistant-handler-'));
// Exercise the bridge against the installed Telegram decoder, independently
// of our encoder. Generated chunk names are discovered only in this test.
import {OPENCLAW} from '../openclaw-root.mjs';
const coreDist=join(OPENCLAW,'dist');
const callbackChunk=(await readdir(coreDist)).find(name=>/^native-command-callback-data-.*\.mjs$/.test(name));
assert.ok(callbackChunk,'installed Telegram callback codec is available');
const {a:decodeCallback}=await import(join(coreDist,callbackChunk));
let source=await readFile(new URL('../openclaw-plugin/index.ts',import.meta.url),'utf8');
source=source.replace("import { buildCallback } from './telegram-callback.ts';",`import { buildCallback } from ${JSON.stringify(new URL('../openclaw-plugin/telegram-callback.ts',import.meta.url).pathname)};`);
source=source.replace("import { t, useLanguage } from './i18n.ts';",`import { t, useLanguage } from ${JSON.stringify(new URL('../openclaw-plugin/i18n.ts',import.meta.url).pathname)};`);
const start=source.indexOf('async function settings()'),end=source.indexOf('export default definePluginEntry');
source=source.slice(0,start)+'async function settings(){return globalThis.fixtureConfig;}\nfunction ownerChat(){return String(globalThis.fixtureConfig.telegram_owner);}\nasync function call(action,args={}){return globalThis.fixtureCall(action,args); }\n'+source.slice(end);
for(const line of ["import { readFile } from 'node:fs/promises';","import { homedir } from 'node:os';","import { join } from 'node:path';"])source=source.replace(line,'');
source=source.replace("import { sendChangePrompt } from './change-prompt.ts';",'const sendChangePrompt=async()=>"456";');
source=source.replace("import { registerAndroidFeed } from './android-feed.ts';",'const registerAndroidFeed=()=>{};');
source=source.replace("import { registerHeartbeatFailureGate } from './heartbeat-failure-gate.ts';",'const registerHeartbeatFailureGate=()=>{};');
source=source.replace("import { registerSecretRedaction } from './secret-redaction.ts';",'const registerSecretRedaction=()=>{};');
source=source.replace("import { registerReviewRecovery, currentReviewRun } from './review-recovery.ts';",'const registerReviewRecovery=()=>{};const currentReviewRun=key=>globalThis.fixtureRuns?.[key];');
source=source.replace("import { definePluginEntry } from 'openclaw/plugin-sdk/plugin-entry';",'const definePluginEntry=v=>v;').replace('export default definePluginEntry','globalThis.fixturePlugin=definePluginEntry');
const fixturePath=join(fixtureDir,'handler.ts');await writeFile(fixturePath,source);
const id='aaaaaaaaaaaaaaaa';let handler, beforeDispatch, promptBuild, toolFactory, toolFactories={}, choices=[], edits=[], replies=[];
globalThis.fixtureConfig={telegram_owner:'1000001',dashboard_host:'machine.example.ts.net',dashboard_path:'/assistant/'};
let item={id,status:'snoozed'};
globalThis.fixtureCall=async(action,args)=>{if(action==='refresh_card')return {queued:true};if(action==='status')return {suggestions:[item],deliveries:[{suggestion_id:id,message_id:'123',previous_message_ids:'["old"]'}]};choices.push(args);if(action==='decide')item.status=args.choice==='complete'?'completed':args.choice==='reject'?'rejected':args.choice==='snooze'?'snoozed':'accepted';return {status:item.status,snoozed_until:'2026-10-10T07:00:00Z'};};
await import(fixturePath);
globalThis.fixturePlugin.register({runtime:{config:{current:()=>({})}},registerTool(factory,opts){toolFactories[opts.name]=factory;if(opts.name==='assistant_signals')toolFactory=factory;},registerInteractiveHandler(h){handler=h.handler},on(name,h){if(name==='before_dispatch')beforeDispatch=h;if(name==='before_prompt_build')promptBuild=h},registerCommand(){}});
const ctx=(choice,message='123')=>({auth:{isAuthorizedSender:true},isGroup:false,accountId:'default',senderId:'1000001',callback:{data:`assistant:${id}:${choice}`,chatId:'1000001',messageId:message},callbackId:'unique',respond:{editButtons:async x=>edits.push(x),reply:async x=>replies.push(x),editMessage:async x=>edits.push(x),clearButtons:async()=>{}}});
await handler(ctx('snooze'));assert.equal(choices.length,0);let buttons=edits.pop().buttons.flat();assert.equal(buttons.length,6);assert.ok(buttons.some(b=>b.url?.startsWith('https://machine.example.ts.net/assistant/#snooze-custom=')));assert.ok(buttons.filter(b=>b.callback_data).every(b=>Buffer.byteLength(b.callback_data)<=64&&decodeCallback(b.callback_data)));
await handler(ctx('back'));assert.deepEqual(edits.pop().buttons.flat().map(b=>b.text),['Unsnooze','Change time','Not needed']);
await handler(ctx('snooze_tomorrow','old'));assert.equal(choices.pop().snooze_option,'tomorrow');
item.status='prepared';const repliesBeforeDone=replies.length;await handler(ctx('complete'));assert.equal(choices.pop().choice,'complete');assert.deepEqual(edits.pop().buttons,[]);assert.equal(replies.length,repliesBeforeDone);
item.status='completed';await handler(ctx('accept'));assert.equal(choices.length,0);assert.equal(replies.length,repliesBeforeDone);
item.status='pending';await handler(ctx('back'));assert.equal(edits.pop().buttons.flat()[0].text,'Do it');
item.status='completed';item.undo_until=new Date(Date.now()+300000).toISOString();await handler(ctx('undo'));assert.equal(choices.pop().choice,'undo');
item.status='accepted';item.preparation_status='blocked';await handler(ctx('back'));assert.equal(edits.pop().buttons.flat()[0].text,'Try again');item.preparation_reason='Sign in to Stripe in the open tab, then tap Continue.';await handler(ctx('back'));assert.equal(edits.pop().buttons.flat()[0].text,'Continue');delete item.preparation_reason;delete item.preparation_status;delete item.undo_until;
item.status='accepted';item.preparation_browser={link:'https://app.example.com/open?to=browser'};await handler(ctx('back'));{const b=edits.pop().buttons.flat();assert.equal(b[0].text,'Open the browser');assert.equal(b[0].url,'https://app.example.com/open?to=browser');}
item.preparation_browser={link:'http://127.0.0.1:6080/vnc.html'};await handler(ctx('back'));assert.ok(!edits.pop().buttons.flat().some(b=>b.text==='Open the browser'));
item.status='pending';item.preparation_browser={link:'https://app.example.com/open?to=browser'};await handler(ctx('back'));assert.ok(!edits.pop().buttons.flat().some(b=>b.text==='Open the browser'));delete item.preparation_browser;
const unauthorized=ctx('accept');unauthorized.senderId='someone-else';await handler(unauthorized);assert.equal(choices.length,0);
item.status='pending';const baseline=replies.length;await handler(ctx('accept'));choices.pop();await handler(ctx('reject'));choices.pop();item.status='pending';await handler(ctx('snooze_2h'));choices.pop();assert.equal(replies.length,baseline);
item.status='pending';await handler(ctx('other'));const prompt=choices.pop();assert.equal(prompt.card_message_id,'123');assert.equal(prompt.managed_prompt,true);assert.equal(choices.length,0);assert.equal(replies.length,baseline);
{const saved=globalThis.fixtureCall;globalThis.fixtureCall=async(action,args)=>action==='request_feedback'?{awaiting_feedback:true,duplicate:true,earlier_prompt:'uncertain'}:saved(action,args);
item.status='pending';const before=replies.length;await handler(ctx('other'));await handler(ctx('other'));assert.equal(replies.length,before);globalThis.fixtureCall=saved;}
// The result notice's quick buttons (telegram.py TELEGRAM_QUICK): Snooze (2 hours) and Mark done run from it, then it says what
// happened with one Open; anything else from it does nothing; a to-do handled meanwhile keeps only Open.
{const saved=globalThis.fixtureCall;globalThis.fixtureCall=async(action,args)=>{const r=await saved(action,args);if(action==='status')r.deliveries[0].notification_message_id='777';return r};
 delete item.next_action;delete item.next_actions;item.status='prepared';
 await handler(ctx('snooze_2h','777'));{const c=choices.pop();assert.equal(c.choice,'snooze');assert.equal(c.snooze_option,'2h');}
 {const b=edits.pop().buttons.flat();assert.deepEqual(b.map(x=>x.text),['Snoozed it']);assert.match(b[0].url,/#chat=a{16}$/);}
 item.status='prepared';await handler(ctx('complete','777'));assert.equal(choices.pop().choice,'complete');assert.deepEqual(edits.pop().buttons.flat().map(x=>x.text),['Marked it done']);
 item.status='prepared';{const before=[choices.length,replies.length];await handler(ctx('reject','777'));await handler(ctx('confirm_abcdef123456','777'));
  assert.equal(choices.length,before[0]);assert.equal(replies.length,before[1]+2);}
 item.status='snoozed';{const before=choices.length;await handler(ctx('complete','777'));assert.equal(choices.length,before);assert.deepEqual(edits.pop().buttons.flat().map(x=>x.text),['Open']);}
 globalThis.fixtureCall=saved;}
item.status='prepared';item.next_action={kind:'email',revision:'abcdef123456',from:'owner@example.com',to:['recipient@example.com'],cc:[],bcc:[],subject:'Verified subject',body:'Exact draft'};
await handler(ctx('back'));buttons=edits.pop().buttons.flat();assert.equal(buttons[0].text,'Send');assert.ok(buttons.every(b=>!b.callback_data||Buffer.byteLength(b.callback_data)<=64));
const beforeSend=choices.length;await handler(ctx('send_abcdef123456'));const review=edits.pop();assert.match(review.text,/From: owner@example.com/);assert.match(review.text,/Exact draft/);assert.equal(choices.length,beforeSend);
assert.deepEqual(review.buttons.flat().map(b=>b.text),['Send now','Edit','Cancel']);assert.match(review.buttons.flat()[1].url,/#send=[a-f0-9]{16}&revision=abcdef123456&edit=1$/);
await handler(ctx('confirm_abcdef123456'));assert.equal(choices.pop().revision,'abcdef123456');edits.pop();
{const before=replies.length;await handler(ctx('confirm_000000000000'));assert.equal(choices.length,beforeSend);edits.pop();
 assert.equal(replies.length,before+1);assert.match(replies.pop().text,/nothing was sent/);}  // a Send on an older card says so
// The card shows this draft in full (card_send): its redraw offers Send that confirms, and Edit.
item.card_send='abcdef123456';await handler(ctx('back'));{const b=edits.pop().buttons.flat();assert.deepEqual(b.slice(0,2).map(x=>x.text),['Send','Edit']);
 assert.match(JSON.stringify(decodeCallback(b[0].callback_data)),/confirm_abcdef123456/);
 assert.match(b[1].url,/^https:\/\/machine\.example\.ts\.net\/assistant\/#send=a{16}&revision=abcdef123456&edit=1$/);}
{const before=choices.length;await handler(ctx('confirm_abcdef123456'));assert.equal(choices.length,before+1);assert.equal(choices.pop().revision,'abcdef123456');edits.pop();}
delete item.card_send;delete item.next_action;
item.next_action={kind:'email',revision:'abcdef123456',from:'owner@example.com',to:[],to_options:['will@vendor.example','ann@example.com'],cc:[],bcc:[],subject:'Pick',body:'Draft'};
{await handler(ctx('send_abcdef123456'));const pick=edits.pop();assert.match(pick.text,/Who should get this email/);const b=pick.buttons.flat();
 assert.deepEqual(b.map(x=>x.text),['Send to will@vendor.example','Send to ann@example.com','Choose several','Edit','Cancel']);assert.equal(b.find(x=>x.text==='Edit').url.endsWith('&edit=1'),true);assert.ok(b.every(x=>!x.callback_data||Buffer.byteLength(x.callback_data)<=64));
 const before=choices.length;await handler(ctx('confirm_abcdef123456'));assert.equal(choices.length,before);edits.pop();  // An old plain Send now shows the choice again.
 await handler(ctx('confirm_abcdef123456_5'));assert.equal(choices.length,before);edits.pop();
 await handler(ctx('confirm_abcdef123456_1'));assert.deepEqual(choices.pop().recipients,['ann@example.com']);edits.pop();}
delete item.next_action;
item.next_actions=[{kind:'email',label:'Send reply',revision:'abcdef123456',from:'owner@example.com',to:['recipient@example.com'],subject:'Exact reply',body:'Approved text'},
 {kind:'prepare',label:'Investigate further',revision:'fedcba654321',instructions:'Check the exact affected mapping locally'},
 {kind:'open',label:'Open the Zap',revision:'111111111111',url:'https://example.com/zap'}];
await handler(ctx('back'));const menu=edits.pop().buttons;assert.ok(menu.every(row=>row.length<=3));assert.deepEqual(menu.flat().slice(0,2).map(b=>b.text),['Send reply','Open the Zap']);
const beforeWrongKind=choices.length;await handler(ctx('send_fedcba654321'));await handler(ctx('next_abcdef123456'));assert.equal(choices.length,beforeWrongKind);
item.next_actions=item.next_actions.slice(1);
await handler(ctx('next_fedcba654321'));assert.equal(choices.pop().revision,'fedcba654321');assert.ok(!edits.pop().buttons.flat().some(b=>b.text==='Investigate further'));
{const saved=globalThis.fixtureCall;globalThis.fixtureCall=async(action,args)=>{if(action==='confirm_action')throw Object.assign(new Error('Newer result'),{status:400});return saved(action,args)};
 await handler(ctx('confirm_abcdef123456'));globalThis.fixtureCall=saved;}
delete item.next_actions;
item.next_action={kind:'email_demo',label:'Send',revision:'abcdef123456',from:'the-machine@example.invalid',to:['alex@example.invalid'],subject:'Demo reply',body:'Thanks for the proposal.'};
await handler(ctx('send_abcdef123456'));const demoPreview=edits.pop();assert.match(demoPreview.text,/nothing will be sent/);assert.deepEqual(demoPreview.buttons.flat().map(b=>b.text),['Back']);
const demoChoices=choices.length;await handler(ctx('confirm_abcdef123456'));assert.equal(choices.length,demoChoices);delete item.next_action;
item.status='prepared';item.next_action={kind:'linkedin',label:'Send reply',revision:'abcdef123456',account_id:'li',conversation_id:'urn:li:msg_conversation:(x,2-A)',to_name:'Ada Lovelace',body:'Friday works.'};
await handler(ctx('back'));assert.equal(edits.pop().buttons.flat()[0].text,'Send reply');
{const before=choices.length;await handler(ctx('send_abcdef123456'));const r=edits.pop();assert.match(r.text,/Send this LinkedIn message\?\nTo: Ada Lovelace\n\nFriday works\./);
 assert.deepEqual(r.buttons.flat().map(b=>b.text),['Send now','Edit','Cancel']);assert.equal(choices.length,before);
 await handler(ctx('confirm_abcdef123456'));assert.equal(choices.pop().revision,'abcdef123456');edits.pop();}
// Handing it to a colleague on Slack: the Send shares a row with Mark done, and the preview says the card waits.
item.status='prepared';item.next_action={kind:'slack',label:'Send to Sam',revision:'abcdef123456',account_id:'slack',to_email:'sam@example.com',to_name:'Sam',body:'Could you check the invoice?',delegate:true,wait_days:3};
await handler(ctx('back'));assert.deepEqual(edits.pop().buttons.map(row=>row.map(b=>b.text)),[['Send to Sam','Mark done','Snooze'],['Ask for changes','Not needed']]);
{const before=choices.length;await handler(ctx('send_abcdef123456'));const r=edits.pop();
 assert.equal(r.text,'Send this Slack message?\nTo: Sam (sam@example.com)\n\nCould you check the invoice?\n\nAfter sending, this to-do waits 3 days for Sam’s reply; it closes when they answer.');
 assert.deepEqual(r.buttons.flat().map(b=>b.text).filter(t=>t!=='Edit'),['Send now','Cancel']);assert.equal(choices.length,before);
 await handler(ctx('confirm_abcdef123456'));assert.equal(choices.pop().revision,'abcdef123456');edits.pop();}
// X: a reply shows the account and the post it answers; a DM the conversation.
item.status='prepared';item.next_action={kind:'x',label:'Reply on X',revision:'abcdef123456',account_id:'x-acme',handle:'acme',reply_to:'1978',to_screen_name:'ada',to_name:'Ada',to_text:'Does it sync?',body:'Yes, it does.'};
await handler(ctx('back'));assert.equal(edits.pop().buttons.flat()[0].text,'Reply on X');
{const before=choices.length;await handler(ctx('send_abcdef123456'));const r=edits.pop();
 assert.equal(r.text,'Reply on X as @acme?\nTo: @ada (Ada)\n“Does it sync?”\n\nYes, it does.');
 assert.deepEqual(r.buttons.flat().map(b=>b.text).filter(t=>t!=='Edit'),['Send now','Cancel']);assert.equal(choices.length,before);
 await handler(ctx('confirm_abcdef123456'));assert.equal(choices.pop().revision,'abcdef123456');edits.pop();}
item.status='prepared';item.next_action={kind:'x',label:'Send',revision:'abcdef123456',account_id:'x-acme',handle:'acme',conversation_id:'42-7',to_name:'Ada',body:'Hi Ada'};
{await handler(ctx('send_abcdef123456'));assert.equal(edits.pop().text,'Send this X message?\nAs @acme to Ada\n\nHi Ada');}
// A merged fix to The Machine: Undo merge for a day, through the owner's tap only.
item.status='prepared';item.next_action={kind:'merge',label:'Merge fix',revision:'abcdef123456',summary:'Fix',stat:'1 file',state:{status:'sent',message_id:'merge:abc',undo_until:new Date(Date.now()+864e5).toISOString()}};
await handler(ctx('back'));{const labels=edits.pop().buttons.flat().map(b=>b.text);assert.ok(labels.includes('Undo merge'));assert.ok(!labels.includes('Merge fix'));}
await handler(ctx('unmerge'));{const c=choices.pop();assert.equal(c.suggestion_id,id);assert.match(c.approval_id,/^telegram:/);}
item.next_action.state.undo_until=new Date(Date.now()-1000).toISOString();await handler(ctx('back'));assert.ok(!edits.pop().buttons.flat().some(b=>b.text==='Undo merge'));
// The last step of a prepared task: the review shows what goes out; Confirm runs only that step.
item.status='prepared';item.next_action={kind:'finish',label:'Submit claim',revision:'abcdef123456',instructions:'Press Submit on the filled-in claim.',preview:'42.50 EUR, Travel, 16 Oct',url:'https://expenses.example.com/claims/7'};
await handler(ctx('back'));assert.equal(edits.pop().buttons.flat()[0].text,'Submit claim');
{const before=choices.length;await handler(ctx('next_abcdef123456'));assert.equal(choices.length,before);
 await handler(ctx('send_abcdef123456'));const r=edits.pop();
 assert.equal(r.text,'Submit claim?\n\n42.50 EUR, Travel, 16 Oct\n\nhttps://expenses.example.com/claims/7\n\nConfirm does only this last step, checks that it went through and reports back.');
 assert.deepEqual(r.buttons.map(row=>row.map(b=>b.text)),[['Confirm','Edit','Cancel'],['Open page']]);assert.equal(choices.length,before);
 assert.match(r.buttons[0][1].url,/#send=[a-f0-9]{16}&revision=abcdef123456&edit=1$/);
 await handler(ctx('confirm_abcdef123456'));assert.equal(choices.pop().revision,'abcdef123456');
 assert.ok(!edits.pop().buttons.flat().some(b=>b.text==='Submit claim'));}
// A step that posts a message shows its exact text and who gets it; Edit opens it in the dashboard editor.
{const step=item.next_action;item.next_action={...step,state:undefined,label:'Submit inbox reply',preview:'Reply in conversation 7.',to_name:'Sam Example',message:'Hi Sam,\n\nFixed now.'};
 await handler(ctx('back'));edits.pop();await handler(ctx('send_abcdef123456'));const r=edits.pop();
 assert.equal(r.text,'Submit inbox reply?\nTo: Sam Example\nReply in conversation 7.\n\nHi Sam,\n\nFixed now.\n\nFiles: none\n\nhttps://expenses.example.com/claims/7\n\nConfirm types exactly this text on the page, attaches no file, submits it, checks that it went through and reports back.');
 assert.deepEqual(r.buttons[0].map(b=>b.text),['Confirm','Edit','Cancel']);
 // With a file it uploads, the review names it and its size, and Confirm says it attaches it.
 item.next_action={...item.next_action,attachments:[{name:'receipt.pdf',size:21213,sha256:'a'.repeat(64),type:'application/pdf'}]};
 await handler(ctx('back'));edits.pop();await handler(ctx('send_abcdef123456'));const f=edits.pop();
 assert.match(f.text,/\n\nAttachments: receipt\.pdf \(21 KB\)\n/);assert.match(f.text,/attaches the files above, submits it/);item.next_action=step;}
item.next_action.state={status:'done'};
{const before=choices.length;await handler(ctx('back'));assert.ok(!edits.pop().buttons.flat().some(b=>b.text==='Submit claim'));
 await handler(ctx('confirm_abcdef123456'));assert.equal(choices.length,before);edits.pop();}
item.next_action.state={status:'needs_input'};
await handler(ctx('back'));assert.ok(edits.pop().buttons.flat().some(b=>b.text==='Submit claim'));
item.status='pending';await handler(ctx('back'));assert.deepEqual(edits.pop().buttons.map(row=>row.map(b=>b.text)),[['Do it','Mark done','Snooze'],['Ask for changes','Not needed']]);
delete item.next_action;
item.status='pending';await handler(ctx('reject'));assert.equal(choices.length,0);assert.deepEqual(edits.pop().buttons.flat().map(b=>b.text),['Not relevant','Wrong facts','Other reason…','No reason','Cancel']);
await handler(ctx('dismiss_handled'));{const d=choices.pop();assert.equal(d.choice,'reject');assert.equal(d.feedback,'Already handled');}
item.status='pending';await handler(ctx('dismiss_none'));{const d=choices.pop();assert.equal(d.choice,'reject');assert.equal(d.feedback,'');}
item.status='pending';await handler(ctx('dismiss_other'));{const d=choices.pop();assert.equal(d.kind,'dismiss');assert.equal(d.managed_prompt,true);}
item.status='pending';item.snooze_choices=[['2h','2 hours'],['tomorrow','Monday · 9:00'],['1w','1 week · 9:00']];await handler(ctx('snooze'));assert.deepEqual(edits.pop().buttons.flat().map(b=>b.text),['2 hours','Monday · 9:00','1 week · 9:00','Choose date','Cancel']);delete item.snooze_choices;
const countBeforeStale=choices.length;
item.status='instructions';await handler(ctx('undo'));assert.equal(choices.length,countBeforeStale);assert.equal(edits.pop().buttons.flat().at(-1).text,'Not needed');
item.status='completed';item.undo_until=new Date(Date.now()-1000).toISOString();await handler(ctx('undo'));assert.equal(choices.length,countBeforeStale);assert.deepEqual(edits.pop().buttons,[]);
item.status='pending';await handler(ctx('retry'));assert.equal(choices.length,countBeforeStale);
// Mark done works on a new card too: it was already handled without Do it.
await handler(ctx('complete'));assert.equal(choices.pop().choice,'complete');assert.equal(choices.length,countBeforeStale);
const savedCall=globalThis.fixtureCall;globalThis.fixtureCall=async(action,args)=>{if(action==='decide')throw Object.assign(new Error('A newer decision replaced this action'),{status:400});return savedCall(action,args)};
item.status='completed';item.undo_until=new Date(Date.now()+300000).toISOString();await handler(ctx('undo'));assert.equal(choices.length,countBeforeStale);assert.equal(edits.pop().buttons.flat()[0].text,'Undo');
globalThis.fixtureCall=async(action,args)=>{if(action==='decide')throw Object.assign(new Error('Server unavailable'),{status:503});return savedCall(action,args)};
await assert.rejects(handler(ctx('undo')),/Server unavailable/);
globalThis.fixtureCall=async(action,args)=>{assert.equal(action,'feedback_reply');assert.equal(args.timestamp,1791614021000);assert.equal(args.reply_to_id,'2982');return {handled:true};};
const handled=await beforeDispatch({content:'I fixed it already',timestamp:1791614021000},{channelId:'telegram',accountId:'default',senderId:'1000001',conversationId:'1000001',sessionKey:'agent:main:main',messageId:'2984',replyToId:'2982'});assert.deepEqual(handled,{handled:true});
// Both profile reads and saves use the host's run, never a model-provided one.
{
 const key='agent:main:assistant-review-profile-aaaaaaaaaaaaaaaa';
 const tool=toolFactory({agentId:'main',sessionKey:key});
 globalThis.fixtureCall=async(action,args)=>{assert.equal(args._profile_session,key);return {ok:true};};
 for(const action of ['profile_evidence','save_profile'])await tool.execute('test',{action,args:{_profile_session:'forged',page:2}});
 const mainTool=toolFactory({agentId:'main',sessionKey:'agent:main:main'});
 globalThis.fixtureCall=async(action,args)=>{assert.equal(args._profile_session,undefined);return {ok:true};};
 await mainTool.execute('test',{action:'profile_evidence',args:{_profile_session:key}});
}
// A to-do's run reads its emails' attachments through the mail connection (mail_attachment), bound to its own run:
// the job and folder come from the host, never the model, and other chats can't reach it.
{
 const saved=globalThis.fixtureCall,calls=[];const run='b'.repeat(32),key='agent:main:assistant-review-preparation-'+run;
 globalThis.fixtureRuns={[key]:run};globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);return {saved:'/run/a.pdf'};};
 const tool=toolFactory({agentId:'main',sessionKey:key});
 await tool.execute('t',{action:'mail_attachment',args:{event_id:54,save:'a.pdf',job_id:'spoof',_folder:'/etc'}});
 assert.deepEqual(calls,[['mail_attachment',{event_id:54,save:'a.pdf',job_id:run}]]);
 for(const c of [{agentId:'main',sessionKey:'agent:main:main',messageChannel:'telegram',nativeChannelId:'1000001'},{agentId:'main',sessionKey:'agent:main:assistant-review-preparation-'+'c'.repeat(32)}])
  await assert.rejects(toolFactory(c).execute('t',{action:'mail_attachment',args:{event_id:54}}),/to-do’s own run/);
 assert.equal(calls.length,1);globalThis.fixtureCall=saved;delete globalThis.fixtureRuns;
}
// A to-do's run reads a Slack conversation through the Slack connection (slack_read), never the browser; only its own run.
{
 const saved=globalThis.fixtureCall,calls=[];const run='d'.repeat(32),key='agent:main:assistant-review-preparation-'+run;
 globalThis.fixtureRuns={[key]:run};globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);return {status:'reading'};};
 await toolFactory({agentId:'main',sessionKey:key}).execute('t',{action:'slack_read',args:{channel:'#proj-halvorsen'}});
 assert.deepEqual(calls,[['slack_read',{channel:'#proj-halvorsen'}]]);
 for(const c of [{agentId:'main',sessionKey:'agent:main:main',messageChannel:'telegram',nativeChannelId:'1000001'},{agentId:'main',sessionKey:'agent:main:assistant-review-preparation-'+'c'.repeat(32)}])
  await assert.rejects(toolFactory(c).execute('t',{action:'slack_read',args:{channel:'general'}}),/to-do’s own run/);
 assert.equal(calls.length,1);globalThis.fixtureCall=saved;delete globalThis.fixtureRuns;
}
// What the owner states in their own private chat is saved as a fact: only that chat is told so and only its
// remember_fact carries the bridge's mark (never a model-supplied one), which the service ties to their last message.
{
 const saved=globalThis.fixtureCall,calls=[];globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);return {id:1};};
 const own={agentId:'main',sessionKey:'agent:main:main',messageChannel:'telegram',nativeChannelId:'1000001'};
 const review={agentId:'main',sessionKey:'agent:main:assistant-review-signals-'+'e'.repeat(32)},todo={agentId:'main',sessionKey:'agent:main:assistant-review-preparation-'+'e'.repeat(32)};
 assert.match(toolFactory(own).description,/tells you here something that stays true.*remember_fact.*no decision_id.*Learning/);
 for(const c of [review,todo])assert.doesNotMatch(toolFactory(c).description,/tells you here something that stays true/);
 await toolFactory(own).execute('t',{action:'remember_fact',args:{text:'The office moved to Ghent.'}});
 assert.deepEqual(calls.pop(),['remember_fact',{text:'The office moved to Ghent.',_owner_chat:true}]);
 for(const c of [review,todo]){
  await toolFactory(c).execute('t',{action:'remember_fact',args:{text:'The office moved to Ghent.',_owner_chat:true,decision_id:'n1'}});
  assert.deepEqual(calls.pop(),['remember_fact',{text:'The office moved to Ghent.',decision_id:'n1'}]);  // a spoofed mark is dropped
 }
 await toolFactory(own).execute('t',{action:'status',args:{_owner_chat:true}});assert.deepEqual(calls.pop(),['status',{}]);
 assert.equal(toolFactory({...own,nativeChannelId:'1000002'}),null);  // someone else's Telegram chat has no such tool
 globalThis.fixtureCall=saved;
}
// Every main chat can offer a bug report: the owner's Telegram chat through assistant_signals, the others (WhatsApp,
// Slack, Teams, the web chat, any channel on agent:main:main) through assistant_bug_report, which only writes one up.
{
 const bug=toolFactories.assistant_bug_report;assert.ok(bug,'the bug report tool is registered');
 for(const messageChannel of ['whatsapp','slack','msteams','webchat','discord']){
  const c={agentId:'main',sessionKey:'agent:main:main',messageChannel};
  assert.equal(toolFactory(c),null,messageChannel+' main chat has no assistant_signals');
  assert.equal(bug(c).name,'assistant_bug_report');assert.match(bug(c).description,/problem with The Machine itself/);
 }
 assert.equal(bug({agentId:'main',sessionKey:'agent:main:main',messageChannel:'telegram',nativeChannelId:'1000002'}).name,'assistant_bug_report');  // Telegram, not the owner's chat
 // The owner's Telegram chat, the heartbeat and the to-do chats have assistant_signals bug_offer: no second tool there
 for(const c of [{agentId:'main',sessionKey:'agent:main:main',messageChannel:'telegram',nativeChannelId:'1000001'},{agentId:'main',sessionKey:'agent:main:main'},
   {agentId:'main',sessionKey:'agent:main:assistant-review-preparation-'+'a'.repeat(32)}]){assert.ok(toolFactory(c));assert.equal(bug(c),null);}
 // Not in groups, other agents or sandboxed runs
 for(const c of [{agentId:'main',sessionKey:'agent:main:whatsapp:group:120363000000000001@g.us',messageChannel:'whatsapp'},{agentId:'work',sessionKey:'agent:main:main',messageChannel:'slack'},
   {agentId:'main',sessionKey:'agent:main:main',messageChannel:'slack',sandboxed:true}])assert.equal(bug(c),null);
 const saved=globalThis.fixtureCall,calls=[];
 globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);return {linked:true,id:'bo_'+'0'.repeat(16),url:'https://machine.example.ts.net/assistant/#bug-offer=bo_'+'0'.repeat(16),say:'Offer it.'};};
 const out=await bug({agentId:'main',sessionKey:'agent:main:main',messageChannel:'whatsapp'}).execute('t',{words:'the to-do list shows twice',summary:'To-dos show twice.',extra:'x'});
 assert.deepEqual(calls,[['bug_offer',{words:'the to-do list shows twice',summary:'To-dos show twice.'}]]);  // only the bug offer, nothing else
 assert.match(JSON.parse(out.content[0].text).url,/^https:\/\/machine\.example\.ts\.net\/assistant\/#bug-offer=bo_0{16}$/);
 globalThis.fixtureCall=saved;
}
// The owner's own main chat (their Telegram chat, the web chat) reads back what was learned with assistant_memory: the
// chat mark is the bridge's, and no other chat, group, agent or run gets the tool.
{
 const memory=toolFactories.assistant_memory;assert.ok(memory,'the memory tool is registered');
 for(const c of [{agentId:'main',sessionKey:'agent:main:main',messageChannel:'telegram',nativeChannelId:'1000001'},{agentId:'main',sessionKey:'agent:main:main',messageChannel:'webchat'}])
  assert.equal(memory(c).name,'assistant_memory');
 for(const c of [{agentId:'main',sessionKey:'agent:main:main',messageChannel:'telegram',nativeChannelId:'1000002'},{agentId:'main',sessionKey:'agent:main:main',messageChannel:'whatsapp'},
   {agentId:'main',sessionKey:'agent:main:assistant-review-preparation-'+'a'.repeat(32)},{agentId:'work',sessionKey:'agent:main:main',messageChannel:'webchat'},
   {agentId:'main',sessionKey:'agent:main:main',messageChannel:'webchat',sandboxed:true},{agentId:'main',sessionKey:'agent:main:webchat:other',messageChannel:'webchat'}])assert.equal(memory(c),null);
 const saved=globalThis.fixtureCall,calls=[];
 globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);return {found:'- You only book aisle seats on flights.'};};
 const out=await memory({agentId:'main',sessionKey:'agent:main:main',messageChannel:'webchat'}).execute('t',{words:'aisle seats',_owner_chat:false,extra:'x'});
 assert.deepEqual(calls,[['recall_learned',{words:'aisle seats',_owner_chat:true}]]);
 assert.match(JSON.parse(out.content[0].text).found,/aisle seats/);
 globalThis.fixtureCall=saved;
}
// The web chat's main session saves what the owner states there with assistant_remember: its message is noted by the
// bridge (owner key, no words), the chat mark is the bridge's, and no other chat, group, agent or run gets the tool.
{
 const remember=toolFactories.assistant_remember;assert.ok(remember,'the remember tool is registered');
 const web={agentId:'main',sessionKey:'agent:main:main',messageChannel:'webchat'};
 assert.equal(remember(web).name,'assistant_remember');assert.match(remember(web).description,/stays true.*Learning/);
 for(const c of [{agentId:'main',sessionKey:'agent:main:main',messageChannel:'telegram',nativeChannelId:'1000001'},{agentId:'main',sessionKey:'agent:main:main',messageChannel:'whatsapp'},
   {agentId:'main',sessionKey:'agent:main:assistant-review-preparation-'+'a'.repeat(32),messageChannel:'webchat'},{agentId:'work',sessionKey:'agent:main:main',messageChannel:'webchat'},
   {...web,sandboxed:true},{agentId:'main',sessionKey:'agent:main:webchat:other',messageChannel:'webchat'}])assert.equal(remember(c),null);
 const saved=globalThis.fixtureCall,calls=[];
 globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);return {id:7,text:args.text};};
 assert.equal(await beforeDispatch({content:'remember that I take the train',channel:'webchat'},{channelId:'webchat',sessionKey:'agent:main:main',messageId:'run-1'}),undefined);
 assert.deepEqual(calls.pop(),['web_chat_said',{message_id:'run-1'}]);  // its id only, and the chat answers as always
 for(const [event,ctx] of [[{content:'/status'},{channelId:'webchat',sessionKey:'agent:main:main',messageId:'run-2'}],[{content:'hi'},{channelId:'webchat',sessionKey:'agent:main:other',messageId:'run-3'}],
   [{content:'hi'},{channelId:'whatsapp',sessionKey:'agent:main:main',messageId:'run-4'}]])await beforeDispatch(event,ctx);
 assert.deepEqual(calls,[]);  // a command, another session or another channel: nothing noted
 await remember(web).execute('t',{text:'You take the train.',kind:'preference',_owner_chat:false,decision_id:'n1'});
 assert.deepEqual(calls.pop(),['remember_fact',{text:'You take the train.',_owner_chat:true,kind:'preference'}]);
 globalThis.fixtureCall=saved;
}
// In Code Mode the model never sees tool descriptions, so the owner's main chat carries the memory habit in its system
// prompt: save what they say in passing that stays true, look up before answering, naming the save tool this chat has.
{
 assert.ok(promptBuild,'the memory habit hook is registered');
 const web=await promptBuild({},{agentId:'main',sessionKey:'agent:main:main',messageProvider:'webchat'});
 assert.match(web.appendSystemContext,/assistant_remember.*don't say "remember".*assistant_memory.*forget or stop using something learned, call assistant_forget\..*Small talk/s);
 assert.doesNotMatch(web.appendSystemContext,/remember_fact/);
 for(const c of [{agentId:'main',sessionKey:'agent:main:main',channel:'telegram',senderId:'1000001',chatId:'1000001'},{agentId:'main',sessionKey:'agent:main:main'}])
  assert.match((await promptBuild({},c)).appendSystemContext,/assistant_signals remember_fact.*assistant_memory.*call assistant_forget\./s);
 for(const c of [{agentId:'main',sessionKey:'agent:main:main',channel:'telegram',senderId:'1000002'},{agentId:'main',sessionKey:'agent:main:main',messageProvider:'whatsapp'},
   {agentId:'main',sessionKey:'agent:main:assistant-review-preparation-'+'a'.repeat(32)},{agentId:'work',sessionKey:'agent:main:main',messageProvider:'webchat'},
   {agentId:'main',sessionKey:'agent:main:main',messageProvider:'webchat',sandboxed:true}])assert.equal(await promptBuild({},c),undefined);
 // The tool descriptions say the same where they are shown: in passing, and looked up before answering
 assert.match(toolFactories.assistant_remember({agentId:'main',sessionKey:'agent:main:main',messageChannel:'webchat'}).description,/without saying "remember"/);
 assert.match(toolFactories.assistant_memory({agentId:'main',sessionKey:'agent:main:main',messageChannel:'webchat'}).description,/Look here first when an answer may depend/);
}
// The owner's own main chat (their private Telegram chat, the web chat) forgets with assistant_forget: declared in the
// manifest as side-effecting, the chat mark and the owner key are the bridge's, and no other chat, agent or run gets it.
{
 const manifest=JSON.parse(await readFile(new URL('../openclaw-plugin/openclaw.plugin.json',import.meta.url),'utf8'));
 assert.ok(manifest.contracts.tools.includes('assistant_forget'));assert.equal(manifest.toolMetadata.assistant_forget.sideEffecting,true);
 assert.match(source,/const OWNER_ACTIONS = new Set\(\[[^\]]*'forget_learned'/);  // sent with the owner key: the local CLI can't forget
 const forget=toolFactories.assistant_forget;assert.ok(forget,'the forget tool is registered');
 for(const c of [{agentId:'main',sessionKey:'agent:main:main',messageChannel:'webchat'},{agentId:'main',sessionKey:'agent:main:main',messageChannel:'telegram',nativeChannelId:'1000001'}])
  assert.equal(forget(c).name,'assistant_forget');
 assert.match(forget({agentId:'main',sessionKey:'agent:main:main',messageChannel:'webchat'}).description,/asks to forget, drop or stop using/);
 for(const c of [{agentId:'main',sessionKey:'agent:main:main',messageChannel:'telegram',nativeChannelId:'1000002'},{agentId:'main',sessionKey:'agent:main:main',messageChannel:'whatsapp'},
   {agentId:'main',sessionKey:'agent:main:assistant-review-preparation-'+'a'.repeat(32)},{agentId:'work',sessionKey:'agent:main:main',messageChannel:'webchat'},
   {agentId:'main',sessionKey:'agent:main:main',messageChannel:'webchat',sandboxed:true},{agentId:'main',sessionKey:'agent:main:webchat:other',messageChannel:'webchat'}])assert.equal(forget(c),null);
 const saved=globalThis.fixtureCall,calls=[];
 globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);return {forgot:'You moved to Ghent.',undo:3};};
 const out=await forget({agentId:'main',sessionKey:'agent:main:main',messageChannel:'webchat'}).execute('t',{words:'moved to Ghent',_owner_chat:false,id:'x'});
 assert.deepEqual(calls.pop(),['forget_learned',{words:'moved to Ghent',_owner_chat:true}]);  // a model's mark or a non-number id never goes
 assert.equal(JSON.parse(out.content[0].text).undo,3);
 await forget({agentId:'main',sessionKey:'agent:main:main',messageChannel:'webchat'}).execute('t',{id:12});
 assert.deepEqual(calls.pop(),['forget_learned',{words:'',_owner_chat:true,id:12}]);
 globalThis.fixtureCall=saved;
}
// The Find my skills report: bound to its own skills session (sent as an upload); refused from any other session.
{
 const key='agent:main:assistant-review-skills-'+'d'.repeat(32);
 globalThis.fixtureCall=async(action,args)=>{assert.equal(action,'skills_found');assert.equal(args._skills_session,key);return {added:1};};
 await toolFactory({agentId:'main',sessionKey:key}).execute('test',{action:'skills_found',args:{_skills_session:'forged',found:[]}});
 await assert.rejects(toolFactory({agentId:'main',sessionKey:'agent:main:assistant-review-profile-'+'d'.repeat(32)}).execute('test',{action:'skills_found',args:{found:[]}}),/Only the Find my skills turn/);
}
// A routine's result: bound to its own routine session; a forged one is replaced, any other session is refused.
{
 const key='agent:main:assistant-review-routine-'+'e'.repeat(32);
 globalThis.fixtureCall=async(action,args)=>{assert.equal(action,'routine_result');assert.equal(args._routine_session,key);return {saved:true};};
 await toolFactory({agentId:'main',sessionKey:key}).execute('test',{action:'routine_result',args:{_routine_session:'forged',text:'Two deals went quiet.'}});
 await assert.rejects(toolFactory({agentId:'main',sessionKey:'agent:main:assistant-review-signals-'+'e'.repeat(32)}).execute('test',{action:'routine_result',args:{text:'x'}}),/Only a routine’s own run/);
}
// A Fleet question: the tap goes to the service with the tapped message id; the service's message replaces the old one.
{const saved=globalThis.fixtureCall,calls=[];const q='q_'+'c'.repeat(16);
 globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);if(args.message_id!=='321'){throw Object.assign(new Error('That Telegram message is not the one sent for this question'),{status:400});}
  return {status:'answered',message:{text:"Pat's Machine asks: Who knows someone at acme.example?\n   → Answered once",buttons:[[{text:'Open in To-dos',url:'https://machine.example.ts.net/assistant/#fleet='+q}]]}};};
 const fleetCtx=(data,message='321')=>({...ctx('accept',message),callback:{data,chatId:'1000001',messageId:message}});
 const before=edits.length;await handler(fleetCtx(`assistant:fleet:${q}:once`));
 assert.deepEqual(calls.pop(),['fleet_decide',{id:q,choice:'once',source:'telegram',message_id:'321',decision_id:'telegram:unique'}]);
 const edited=edits.pop();assert.equal(edits.length,before);assert.match(edited.text,/Answered once/);assert.equal(edited.buttons[0][0].url.endsWith('#fleet='+q),true);
 await handler(fleetCtx(`assistant:fleet:${q}:never`));await handler(fleetCtx(`assistant:fleet:q_x:once`));assert.equal(calls.length,0);  // never is for the dashboard
 await handler(fleetCtx(`assistant:fleet:${q}:always`,'999'));assert.equal(calls.pop()[1].message_id,'999');assert.equal(edits.length,before);  // refused: buttons cleared, nothing decided
 const stranger=fleetCtx(`assistant:fleet:${q}:once`);stranger.senderId='someone-else';await handler(stranger);assert.equal(calls.length,0);
 globalThis.fixtureCall=saved;}
// A member asks the Fleet for a server: Confirm relays the tap with its message id; a stale tap says why; only the owner's chat.
{const saved=globalThis.fixtureCall,calls=[];const n='fn_'+'d'.repeat(16);let status='confirmed';
 globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);if(args.message_id!=='654'){throw Object.assign(new Error('That Telegram message is not the one sent for this request'),{status:400});}
  return {status,reason:status==='stale'?'Already settled: Confirmed in Telegram: their server is starting. Nothing more was done.':'',
   message:{text:'Ann wants a Standard server in Acme: €30/month, new total €60/month.\n\n→ Confirmed in Telegram: their server is starting.',buttons:[[{text:'Open',url:'https://machine.example.ts.net/assistant/#fleet='+n}]]}};};
 const tap=(data,message='654')=>({...ctx('accept',message),callback:{data,chatId:'1000001',messageId:message}});
 const before=edits.length,said=replies.length;await handler(tap(`assistant:fleetn:${n}:confirm`));
 assert.deepEqual(calls.pop(),['fleet_notice_decide',{id:n,choice:'confirm',source:'telegram',message_id:'654',decision_id:'telegram:unique'}]);
 assert.match(edits.pop().text,/Confirmed in Telegram/);assert.equal(edits.length,before);assert.equal(replies.length,said);
 status='stale';await handler(tap(`assistant:fleetn:${n}:confirm`));calls.pop();assert.match(edits.pop().text,/Confirmed in Telegram/);assert.equal(replies.length,said);  // the message itself shows it
 {const respond=tap('x').respond;const t=tap(`assistant:fleetn:${n}:confirm`);t.respond={...respond,editMessage:async()=>{throw new Error('Bad Request: message is not modified');}};
  await handler(t);calls.pop();assert.match(replies.pop().text,/^Already settled/);}  // unchanged message: the reason comes as a reply
 {const t=tap(`assistant:fleetn:${n}:confirm`);let cleared=0;t.respond={...t.respond,clearButtons:async()=>{cleared++;}};
  globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);throw Object.assign(new Error('The operation was aborted'),{name:'AbortError'});};
  await handler(t);calls.pop();assert.match(replies.pop().text,/did not answer just now, so nothing was done/);assert.equal(cleared,0);  // service away: buttons stay
  globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);throw Object.assign(new Error('That request is no longer here, so nothing was done.'),{status:400});};
  await handler(tap(`assistant:fleetn:${n}:confirm`));calls.pop();assert.match(replies.pop().text,/no longer here/);
  globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);if(args.message_id!=='654'){throw Object.assign(new Error('That Telegram message is not the one sent for this request'),{status:400});}
   return {status,reason:'',message:{text:'x',buttons:[]}};};}
 await handler(tap(`assistant:fleetn:${n}:decline`,'999'));assert.equal(calls.pop()[1].message_id,'999');assert.equal(edits.length,before);
 assert.match(replies.pop().text,/nothing was done/);  // not the message sent for it: buttons cleared, nothing decided
 const heard=replies.length;await handler(tap(`assistant:fleetn:${n}:approve`));await handler(tap(`assistant:fleetn:fn_x:confirm`));assert.equal(calls.length,0);
 assert.equal(replies.length,heard+2);assert.match(replies.pop().text,/That button did nothing/);replies.pop();  // an unknown button says so
 const quiet=replies.length;
 const stranger=tap(`assistant:fleetn:${n}:confirm`);stranger.senderId='someone-else';await handler(stranger);
 const group=tap(`assistant:fleetn:${n}:confirm`);group.callback.chatId='-100200';await handler(group);assert.equal(calls.length,0);assert.equal(replies.length,quiet);  // not the owner's chat: silence
 globalThis.fixtureCall=saved;}
// The weekly recap: a tap goes to the service with the tapped message id; the service edits the recap itself. A refusal says why.
{const saved=globalThis.fixtureCall,calls=[];const r='r_'+'e'.repeat(12);
 globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);if(args.message_id!=='777')throw Object.assign(new Error('That Telegram message is not the recap this line was sent in'),{status:400});
  return args.choice==='keep'?{status:'filtered',reason:'Already done: filtered.'}:{status:'filtered'};};
 const tap=(data,message='777')=>({...ctx('accept',message),callback:{data,chatId:'1000001',messageId:message}});
 const before=edits.length,said=replies.length;await handler(tap(`assistant:recap:${r}:filter`));
 assert.deepEqual(calls.pop(),['recap_decide',{id:r,choice:'filter',source:'telegram',message_id:'777',decision_id:'telegram:unique'}]);
 assert.equal(edits.length,before);assert.equal(replies.length,said);  // the service edits the message; nothing to say
 await handler(tap(`assistant:recap:${r}:keep`));calls.pop();assert.match(replies.pop().text,/Already done/);
 await handler(tap(`assistant:recap:${r}:undo`,'999'));calls.pop();assert.match(replies.pop().text,/not the recap/);
 globalThis.fixtureCall=async(action,args)=>{calls.push([action,args]);throw Object.assign(new Error('The operation was aborted'),{name:'AbortError'});};
 await handler(tap(`assistant:recap:${r}:drop`));calls.pop();assert.match(replies.pop().text,/did not answer just now, so nothing was done/);
 const heard=replies.length;await handler(tap(`assistant:recap:${r}:send`));await handler(tap(`assistant:recap:r_x:filter`));assert.equal(calls.length,0);
 assert.equal(replies.length,heard+2);replies.pop();replies.pop();  // only its own choices: anything else is an unknown button
 const stranger=tap(`assistant:recap:${r}:filter`);stranger.senderId='someone-else';await handler(stranger);assert.equal(calls.length,0);
 globalThis.fixtureCall=saved;}
console.log('Telegram handler: snooze menu, typed callback sizes, old recorded cards, completion and ownership passed.');

await rm(fixtureDir,{recursive:true,force:true});
