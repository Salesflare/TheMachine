import {H, W} from './test-env.mjs';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {registerReviewRecovery} from '../openclaw-plugin/review-recovery.ts';

const ctx={agentId:'main',sessionKey:'agent:main:assistant-review-preparation-'+'a'.repeat(32),runId:'run',toolCallId:'call'};
const hooks={};registerReviewRecovery({on(name,fn){hooks[name]=fn}},async()=>({active:true}));
const run=async(params,toolName='exec')=>hooks.before_tool_call({toolName,params},ctx);
for(const command of [
  "python3 integrations/browser-lease.py claim --owner x --minutes 30; find "+H+" -iname '*invoice*' -o -iname '*contract*' 2>/dev/null | head -70",
  'gh api user','gh api -X GET user','gh run list -R example/app','gog gmail messages list --readonly',
  'python3 -c "print(1)"','gh issue create -R Example/Server --title x --body-file memory/assistant/x.md --label deadline','gh issue comment 12 -R Example/Server --body x','gh issue edit 12 --add-label BUG','curl https://example.com','rg -n invoice ~/Documents','ls ~ && du -sh ~/Downloads',
]) assert.equal(await run({command}),undefined,command);
for(const command of [
  // Loose on purpose: what the owner asks or confirms runs.
  'linkedin-inbox send --profile example --text draft --yes','gog gmail send --to a@example.com','gog gmail labels list','openclaw message send --message hi',
  'sudo ls','rm -rf memory/tmp','git push','systemctl --user restart x','openclaw gateway restart','gh pr merge 5','gh api -X DELETE repos/a/b/caches/1',
  'gh api repos/a/b/issues -f title=x','gh issue close 12','gh pr create --fill','gog calendar create primary --summary x',
]) assert.equal(await run({command}),undefined,command);
for(const command of [
  'printf fix > tools/personal-assistant/assistant.py','sort -o tools/personal-assistant/assistant.py memory/assistant/x',
  'gog auth list','rg token '+H+'','cat '+H+'/.ssh/id_rsa',
]) assert.equal((await run({command}))?.block,true,command);
assert.equal(await run({action:'act',request:{kind:'click',ref:'e1'}},'browser'),undefined);
// No keyword prohibition: a native scan setting and its browser toggle use normal tools.
assert.equal(await run({action:'disable',scan_id:'owner-selected'},'codex_security'),undefined);
assert.equal(await run({action:'act',request:{kind:'click',ref:'stop-owner-selected-scan'}},'browser'),undefined);
assert.equal(await run({path:'memory/assistant/261012-x.md',content:'x'},'write'),undefined);
assert.equal(await run({path:''+H+'/Documents/x.md',content:'x'},'write'),undefined);
assert.equal((await run({path:'tools/personal-assistant/assistant.py',content:'x'},'write')).block,true);
assert.equal((await run({path:''+H+'/.ssh/id_rsa'},'read')).block,true);
assert.equal(await run({text:'hi'},'message'),undefined);
assert.equal(await hooks.before_tool_call({toolName:'exec',params:{command:'sudo ls'}},{...ctx,sessionKey:'agent:main:main'}),undefined);
console.log('Preparation policy: everything runs except reading credentials and editing the assistant itself.');
const calls=[];const journalHooks={};
registerReviewRecovery({on(n,f){journalHooks[n]=f}},async(a,args)=>{calls.push({a,args});return {active:true};});
await journalHooks.before_tool_call({toolName:'browser',toolCallId:'big',params:{html:'x'.repeat(100000)}},ctx);
await journalHooks.after_tool_call({toolName:'browser',toolCallId:'big',params:{html:'x'.repeat(100000)},result:{body:'x'.repeat(100000)}},ctx);
assert.ok(JSON.stringify(calls[0].args).length<65536);assert.ok(JSON.stringify(calls[1].args).length<65536);
assert.equal(calls[0].args.params.clipped,true);assert.equal(calls[1].args.result.clipped,true);
// Exercise the actual hook envelope through the real continuation gate, not a mocked predicate.
const largeSave={action:'prepare',args:{body:'Ready',next_actions:[
  {kind:'email',body:'a'.repeat(11500)},{kind:'email',body:'b'.repeat(11500)}]}};
await journalHooks.before_tool_call({toolName:'assistant_signals',toolCallId:'save',params:largeSave},ctx);
const saveIntent=calls.at(-1).args;
assert.equal(saveIntent.params.clipped,true);assert.equal(saveIntent.tool_action,'prepare');
assert.ok(JSON.stringify(saveIntent).length<65536);
const python=spawnSync('python3',['-c',`
import json,sys
from test_preparation import Preparation
t=Preparation();t.setUp()
try:
 t.accept();old=t.job()['job_id'];t.app.preparation_step(lambda _: {'status':'admitted'})
 t.app.action('preparation_tool_intent',{'job_id':old,'call_id':'write','tool':'browser','params':{'action':'click'}})
 t.app.preparation_step(lambda _: {'status':'error'})
 with t.store.connect() as db:db.execute('UPDATE preparations SET retry_at=NULL')
 t.app.preparation_step(lambda _: {'status':'admitted'})
 args=json.load(sys.stdin);args['job_id']=t.job()['job_id']
 assert t.app.action('preparation_tool_intent',args)['active']
 args['call_id']='ordinary-write';args['tool']='browser';args['tool_action']='act';args['params']={'action':'act'}
 assert not t.app.action('preparation_tool_intent',args)['active']
 print('Clipped finishing hook admitted through continuation gate; ordinary writes still require history.')
finally:t.doCleanups()
`],{cwd:new URL('..',import.meta.url),input:JSON.stringify(saveIntent),encoding:'utf8'});
assert.equal(python.status,0,python.stderr||python.stdout);console.log(python.stdout.trim());
