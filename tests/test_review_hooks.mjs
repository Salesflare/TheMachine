import {H, W} from './test-env.mjs';
import assert from 'node:assert/strict';
import {registerReviewRecovery, processingOnlyReviewSummary, currentReviewRun, contextFile} from '../openclaw-plugin/review-recovery.ts';
const hooks={},calls=[];
let review=null;
registerReviewRecovery({on(name,fn){hooks[name]=fn}},async(action,args)=>{
 calls.push({action,args});return action==='review_context'?{review}:{recorded:true,active:true};
});
const main={agentId:'main',sessionKey:'agent:main:main',runId:'heartbeat-run',trigger:'heartbeat',messageProvider:'telegram',senderId:'1000001',chatId:'1000001'};
// Reviews run in isolated sessions started by the service; heartbeats no longer review.
const ctx={...main,sessionKey:'agent:main:assistant-review-signals-'+'a'.repeat(32),runId:'trusted-run',trigger:undefined};
assert.equal(await hooks.before_prompt_build({},main),undefined);
assert.equal(await hooks.before_prompt_build({}, {...ctx,chatId:'shared-chat'}),undefined);
assert.equal(calls.length,0);
const built=await hooks.before_prompt_build({},ctx);
// What every review gets alike goes at the start of the system prompt, where the prompt cache reuses it from one review
// to the next; the turn's message holds only this run's own words (none here: no unfinished review to resume).
assert.equal(built.prependContext,undefined);
assert.ok(built.prependSystemContext.includes('analysis_page'));
const reviewContext=built.prependSystemContext;
assert.equal((await hooks.before_prompt_build({},{...ctx,sessionKey:'agent:main:assistant-review-signals-'+'d'.repeat(32),runId:'other-run'})).prependSystemContext,reviewContext);
assert.ok(reviewContext.includes('## About the owner (USER.md)'));assert.ok(reviewContext.includes('## Assistant instructions'));
// Only the parts of AGENTS.md a review uses: it is resent on every step of the turn.
assert.ok(reviewContext.includes('## Reviewing signals'));assert.ok(reviewContext.includes('## Lessons that generalize'));
for(const title of ['## Preparing accepted suggestions','## Operations','## Public repository hygiene','## Security maintenance'])assert.ok(!reviewContext.includes(title),title);
assert.ok(!reviewContext.includes('Read tools/personal-assistant/AGENTS.md'));
// Context files come from a fixed list by name; a path or any other name reads nothing.
assert.ok((await contextFile('USER','Owner')).includes('The owner prefers short answers.'));
{ // The whole USER.md up to its cap (owner rules can be long); past it the dashboard says so (needs_you)
 const {readFileSync,writeFileSync}=await import('node:fs');const {ownerContext,USER_MD_LIMIT}=await import('../openclaw-plugin/review-recovery.ts');
 const file=W+'/USER.md',before=readFileSync(file,'utf8');
 try{
  assert.equal(USER_MD_LIMIT,40000);
  writeFileSync(file,'x'.repeat(35000)+' LAST RULE');assert.ok((await ownerContext()).includes('LAST RULE'));
  writeFileSync(file,'x'.repeat(41000)+' LAST RULE');const cut=await ownerContext();
  assert.ok(!cut.includes('LAST RULE'));assert.ok(cut.includes('[…shortened]'));
 }finally{writeFileSync(file,before)}
}
for(const name of ['/etc/passwd','../USER.md',W+'/USER.md','USER.md','constructor','toString'])assert.equal(await contextFile(name,'x'),'',name);
// Review turns may only read.
assert.equal((await hooks.before_tool_call({toolName:'browser',params:{}},ctx)).block,true);
assert.equal((await hooks.before_tool_call({toolName:'gateway_exec',params:{}},ctx)).block,true);
assert.equal((await hooks.before_tool_call({toolName:'exec',params:{}},ctx)).block,true);  // embedded runtime shell
assert.equal((await hooks.before_tool_call({toolName:'write',params:{}},ctx)).block,true);
assert.notEqual((await hooks.before_tool_call({toolName:'read',params:{}},ctx))?.block,true);
// Code Mode: namespaced names and the script runner (seen live on October 11).
assert.notEqual((await hooks.before_tool_call({toolName:'openclawassistant_signals',params:{action:'status',args:{}}},ctx))?.block,true);
assert.notEqual((await hooks.before_tool_call({toolName:'openclaw__memory_search',params:{}},ctx))?.block,true);
assert.equal((await hooks.before_tool_call({toolName:'openclawbrowser',params:{}},ctx)).block,true);
assert.notEqual((await hooks.before_tool_call({toolName:'exec',toolKind:'code_mode_exec',params:{}},ctx))?.block,true);
// Code Mode's wait resumes that exec by its runId and passes; anything else named wait is checked like any tool.
assert.notEqual((await hooks.before_tool_call({toolName:'wait',params:{runId:'run-1'}},ctx))?.block,true);
assert.equal((await hooks.before_tool_call({toolName:'wait',params:{runId:'run-1',command:'ls'}},ctx)).block,true);
assert.equal((await hooks.before_tool_call({toolName:'wait',params:{}},ctx)).block,true);
assert.equal(await hooks.before_tool_call({toolName:'openclawassistant_signals',params:{action:'begin_analysis',args:{}}},ctx),undefined);  // no rewrite under Code Mode names
assert.notEqual((await hooks.before_tool_call({toolName:'memory_search',params:{}},ctx))?.block,true);
// Without Code Mode, tool search: looking tools up and tool_call pass; the tool it runs is checked by its own name
for(const toolName of ['tool_search','tool_describe','tool_call'])assert.notEqual((await hooks.before_tool_call({toolName,params:{name:'assistant_signals'}},ctx))?.block,true,toolName);
// OpenClaw 2026.11 calls the runner dispatch_action; blocked, a review on such a model stopped after three refusals
const dispatched={toolName:'dispatch_action',params:{id:'assistant_signals',args:{action:'status',args:{}}}};
assert.notEqual((await hooks.before_tool_call(dispatched,ctx))?.block,true);
assert.equal((await hooks.before_tool_call({toolName:'exec',params:{command:'ls'}},ctx)).block,true);  // what tool_call would run
assert.equal(await hooks.before_tool_call({toolName:'browser',params:{}},main),undefined);  // main session unaffected
// Profile drafts (assistant profile) read the same way and get only the owner's USER.md, not review instructions.
const profileCtx={...ctx,sessionKey:'agent:main:assistant-review-profile-'+'b'.repeat(32),runId:'profile-run'};
const profileContext=(await hooks.before_prompt_build({},profileCtx)).prependContext;
assert.ok(profileContext.includes('## About the owner (USER.md)'));assert.ok(!profileContext.includes('analysis_page'));
assert.equal((await hooks.before_tool_call({toolName:'write',params:{}},profileCtx)).block,true);
assert.equal((await hooks.before_tool_call({toolName:'message',params:{}},profileCtx)).block,true);
assert.notEqual((await hooks.before_tool_call({toolName:'assistant_signals',params:{action:'profile_evidence',args:{}}},profileCtx))?.block,true);
// Find my skills: the browser (to read the owner's accounts) and assistant_signals (its report); no shell or writes,
// and no review instructions.
const skillsCtx={...ctx,sessionKey:'agent:main:assistant-review-skills-'+'c'.repeat(32),runId:'skills-run'};
{const {NOT_FIRST_CHAT,READ_ONLY_RUN}=await import('../openclaw-plugin/review-recovery.ts');
 const built=await hooks.before_prompt_build({},skillsCtx);  // USER.md from the plugin: the run gets no workspace files
 assert.ok(built.prependContext.startsWith(NOT_FIRST_CHAT+' '+READ_ONLY_RUN));assert.ok(built.prependContext.includes('## About the owner (USER.md)'));
 assert.ok(!built.prependContext.includes('analysis_page'));assert.equal(built.toolsAllow,undefined);}
assert.notEqual((await hooks.before_tool_call({toolName:'browser',params:{action:'open'}},skillsCtx))?.block,true);
assert.notEqual((await hooks.before_tool_call({toolName:'assistant_signals',params:{action:'skills_found',args:{}}},skillsCtx))?.block,true);
for(const toolName of ['exec','write','message'])assert.equal((await hooks.before_tool_call({toolName,params:{command:'ls'}},skillsCtx)).block,true);
// A routine's run (routines_app.py) only reads, then reports with routine_result: no browser, shell, writes, or any
// assistant_signals action that suggests, prepares or saves.
{const routineCtx={...ctx,sessionKey:'agent:main:assistant-review-routine-'+'e'.repeat(32),runId:'routine-run'};
 for(const action of ['events','status','related','graph','routine_result'])assert.notEqual((await hooks.before_tool_call({toolName:'assistant_signals',params:{action}},routineCtx))?.block,true,action);
 assert.notEqual((await hooks.before_tool_call(dispatched,routineCtx))?.block,true);  // tool search's runner
 assert.notEqual((await hooks.before_tool_call({toolName:'memory_search',params:{query:'deals'}},routineCtx))?.block,true);
 for(const action of ['suggest','prepare','promise','remember_fact','begin_analysis','meeting_notes'])assert.equal((await hooks.before_tool_call({toolName:'assistant_signals',params:{action}},routineCtx)).block,true,action);
 for(const toolName of ['exec','write','message','browser'])assert.equal((await hooks.before_tool_call({toolName,params:{command:'ls'}},routineCtx)).block,true,toolName);
 // It reads like the owner would: web search and pages, the browser to look, gh and git that only read. A test
 // run said it could not check what merged or read the posts "in this read-only run".
 const routineCall=async(toolName,params)=>(await hooks.before_tool_call({toolName,params},routineCtx))?.block===true;
 for(const toolName of ['web_search','web_fetch'])assert.equal(await routineCall(toolName,{query:'x',url:'https://example.com'}),false,toolName);
 for(const params of [{action:'open',targetUrl:'https://x.com/example'},{action:'navigate',targetUrl:'https://github.com/example/repo/pulls'},
   {action:'snapshot'},{action:'text'},{action:'tabs'},{action:'screenshot'},{action:'act',request:{kind:'scrollIntoView',ref:'e4'}},
   {action:'act',request:{kind:'press',key:'PageDown'}},{action:'act',kind:'wait',timeMs:500}])
  assert.equal(await routineCall('browser',params),false,JSON.stringify(params));
 for(const params of [{action:'act',request:{kind:'click',ref:'e9'}},{action:'act',request:{kind:'type',ref:'e2',text:'hi'}},
   {action:'act',request:{kind:'fill',fields:[]}},{action:'act',request:{kind:'press',key:'Enter'}},{action:'act',request:{kind:'press',key:'Control+Enter'}},
   {action:'act',request:{kind:'evaluate',fn:'1'}},{action:'act',request:{kind:'wait',fn:'document.forms[0].submit()'}},
   {action:'act',request:{kind:'batch',actions:[{kind:'click'}]}},{action:'act',kind:'click',ref:'e9'},{action:'upload',paths:['/tmp/a']},
   {action:'dialog',accept:true},{action:'download'},{action:'open',targetUrl:'javascript:alert(1)'},{action:'navigate',targetUrl:'file:///etc/passwd'},
   {action:'screenshot',path:'/tmp/shot.png'},{action:'importprofile'}])
  assert.equal(await routineCall('browser',params),true,JSON.stringify(params));
 for(const command of ['gh pr list --repo example/repo --state merged --search "merged:>2026-11-07" --json number,title',
   'gh pr view 12 --repo example/repo','gh api repos/example/repo/pulls?state=closed','gh api -X GET repos/example/repo/commits',
   'gh search prs --repo example/repo --merged','gh release list','git log --since=2026-11-07 --oneline','git -C repo show HEAD'])
  assert.equal(await routineCall('exec',{command}),false,command);
 for(const command of ['gh pr merge 12','gh pr comment 12 --body hi','gh api -X POST repos/example/repo/issues','gh api repos/example/repo/issues -f title=x',
   'gh api --method=PATCH repos/example/repo','gh api graphql','gh pr list | sh','gh pr list > out.txt','gh pr list && rm -rf x','gh pr list $(id)',
   'git push','git log --output=/tmp/x','git -c core.pager=sh log','curl https://example.com','ls','rm -rf repo','GH_PAGER=sh gh pr list'])
  assert.equal(await routineCall('exec',{command}),true,command);
 // Git that only reads, never an option that runs a program: --upload-pack (or any start of it git accepts, like
 // --upl=), --exec, -u on ls-remote, ext:: and other remote helpers, a config or pager setting.
 for(const command of ['git ls-remote --heads origin','git ls-remote --tags https://github.com/example/repo','git log --no-ext-diff -1',
   'git show --stat HEAD','git diff --name-only HEAD~1'])
  assert.equal(await routineCall('exec',{command}),false,command);
 for(const command of ['git ls-remote --upload-pack="touch /tmp/x" .','git ls-remote --upload-pack "touch /tmp/x" .','git ls-remote --upl=sh .',
   'git ls-remote --u=sh .','git ls-remote --exec=sh .','git ls-remote -u sh .','git ls-remote -qu sh .','git ls-remote --receive-pack=sh .',
   'git ls-remote "ext::sh -c touch% /tmp/x"','git ls-remote fd::3','git -C repo -c core.sshCommand=sh ls-remote origin',
   'git log --config-env=core.pager=X','git log --git-dir=/tmp/x','git log --work-tree=/tmp','git diff --ext-diff','git diff --text"conv"',
   'git log --exec-path=/tmp','git log --outp=/tmp/x','git show --open-files-in-pager=sh','git -c core.pager=sh log'])
  assert.equal(await routineCall('exec',{command}),true,command);}
// An isolated review ends with one fixed line (its turn has delivery off): after NO_REPLY, OpenClaw asked twice more
{ const system=(await hooks.before_prompt_build({},ctx)).prependSystemContext;
  assert.ok(system.includes('End with exactly the line Done.'));assert.ok(!system.includes('end with exactly NO_REPLY'));
  assert.ok(system.includes('this reply is never sent to anyone'));assert.ok(!system.includes('alerts and authorized'));
  assert.ok(system.includes('Do not announce starting')); }
// Codex refuses a tool call whose parameters a hook rewrote, so the hook never returns params;
// the tool binds ownership from the run the prompt hook recorded for this session.
assert.equal(await hooks.before_tool_call({toolName:'assistant_signals',params:{action:'begin_analysis',args:{account_ids:['work'],_review_run:'spoof'}}},ctx),undefined);
assert.equal(currentReviewRun(ctx.sessionKey),'trusted-run');
review={id:'review-id',owner_run:'trusted-run',last_error:'ai_connection_reset'};
{ // An unfinished review to resume is this run's own: it stays in the message, the system context is unchanged
 const resumed=await hooks.before_prompt_build({},ctx);
 assert.ok(resumed.prependContext.includes('review-id'));assert.ok(!resumed.prependSystemContext.includes('review-id'));
 assert.equal(resumed.prependSystemContext,reviewContext);
}
await hooks.model_call_ended({outcome:'error',failureKind:'connection_reset'},ctx);
assert.equal(calls.at(-1).args.reason,'ai_connection_reset');
let guard=await hooks.before_agent_finalize({},ctx);
assert.equal(guard.action,'revise');assert.equal(guard.retry.maxAttempts,2);
assert.ok(guard.retry.instruction.includes('End with exactly the line Done.'));assert.ok(!guard.retry.instruction.includes('NO_REPLY'));
await hooks.agent_end({success:true},ctx);
assert.equal(calls.at(-1).args.terminal,true);assert.equal(calls.at(-1).args.reason,'review_not_finished');
review=null;assert.equal(await hooks.before_agent_finalize({},ctx),undefined);
const before=calls.length;await hooks.model_call_ended({outcome:'error'}, main);assert.equal(calls.length,before);
console.log('Review hooks: private scope, host-bound run, retry hint, redacted error and bounded finish guard passed.');

const prepCtx={...ctx,sessionKey:'agent:main:assistant-review-preparation-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'};
const previousCount=calls.length;const prep=await hooks.before_prompt_build({},prepCtx);
assert.ok(prep.prependSystemContext.includes('\n\n## About the owner (USER.md)'));assert.ok(prep.prependSystemContext.includes('## Preparation rules')&&prep.prependSystemContext.includes('then tap Continue'));assert.ok(!prep.prependSystemContext.includes('analysis_page'));
// The rules go in the system prompt, never the turn's message: a message is saved into the session, so every later turn
// (Do it after a prepare-ahead, a to-do chat) added one more copy. The same rules on each turn, so the cached prefix holds.
assert.equal(prep.prependContext,undefined);
assert.equal((await hooks.before_prompt_build({},prepCtx)).prependSystemContext,prep.prependSystemContext);
assert.equal(calls.length,previousCount);  // a preparation is not a review
{ // On OpenClaw's embedded runtime (its hook context has activeProjectKeys) a read-only run's turn sees only the tools it
  // may call, plus tool search's runners; Code Mode's exec and wait OpenClaw keeps by itself, so they're not named here
  // (a plain exec would be the shell). Codex app-server refuses a turn whose hook narrows tools: there nothing changes.
 const {turnTools,TOOL_SEARCH_TOOLS,REVIEW_TOOLS,embeddedRuntime}=await import('../openclaw-plugin/review-recovery.ts');
 const embedded=c=>({...c,activeProjectKeys:[]});
 assert.equal(embeddedRuntime(embedded(ctx)),true);assert.equal(embeddedRuntime(ctx),false);
 const reviewTurn=await hooks.before_prompt_build({},embedded(ctx));
 assert.deepEqual(new Set(reviewTurn.toolsAllow),new Set([...REVIEW_TOOLS,...TOOL_SEARCH_TOOLS]));
 for(const name of ['dispatch_action','tool_search','tool_describe','tool_call','assistant_signals'])assert.ok(reviewTurn.toolsAllow.includes(name),name);
 for(const name of ['skills_read','exec','write','browser','message','wait'])assert.ok(!reviewTurn.toolsAllow.includes(name),name);
 assert.equal(reviewTurn.prependSystemContext,reviewContext);  // the same instructions, cache prefix and all
 assert.ok(reviewContext.includes('do not call skills_read'));
 // Every tool a turn sees is one before_tool_call lets it call: nothing listed only to be refused.
 for(const name of turnTools(ctx.sessionKey))assert.notEqual((await hooks.before_tool_call({toolName:name,params:{id:'assistant_signals',args:{action:'status'}}},ctx))?.block,true,name);
 const profileTurn=await hooks.before_prompt_build({},embedded(profileCtx));
 assert.ok(profileTurn.prependContext.includes('## About the owner (USER.md)'));
 assert.deepEqual(new Set(profileTurn.toolsAllow),new Set([...REVIEW_TOOLS,...TOOL_SEARCH_TOOLS]));
 // Without the workspace files, OpenClaw tells a run on a new install to read BOOTSTRAP.md first; a sandbox review did.
 const {NOT_FIRST_CHAT,OWNER_RULES_HERE}=await import('../openclaw-plugin/review-recovery.ts');
 assert.ok(reviewContext.includes(NOT_FIRST_CHAT));assert.ok(profileTurn.prependContext.startsWith(NOT_FIRST_CHAT));
 // A preparation and its to-do chat have no workspace files either (preparation-run.mjs): USER.md comes with its rules.
 assert.ok(prep.prependSystemContext.startsWith(NOT_FIRST_CHAT+' '+OWNER_RULES_HERE+'\n\n## About the owner (USER.md)'));
 // ...and is told those rules are here, so it does not go read the chat's own AGENTS.md (a sandbox Do it did, 4 in 11).
 assert.ok(!profileTurn.prependContext.includes(OWNER_RULES_HERE));
 const skillsTurn=await hooks.before_prompt_build({},embedded(skillsCtx));
 assert.ok(skillsTurn.toolsAllow.includes('browser'));assert.ok(!skillsTurn.toolsAllow.includes('exec'));assert.ok(skillsTurn.prependContext.startsWith(NOT_FIRST_CHAT));
 const routineTurn=await hooks.before_prompt_build({},embedded({...ctx,sessionKey:'agent:main:assistant-review-routine-'+'e'.repeat(32),runId:'routine-run'}));
 for(const name of ['assistant_signals','web_search','web_fetch','browser','exec','dispatch_action'])assert.ok(routineTurn.toolsAllow.includes(name),name);
 for(const name of ['write','message','skills_read'])assert.ok(!routineTurn.toolsAllow.includes(name),name);
 // Codex (no activeProjectKeys): no toolsAllow, the rest as before.
 for(const c of [ctx,profileCtx,skillsCtx])assert.equal((await hooks.before_prompt_build({},c))?.toolsAllow,undefined,c.sessionKey);
 // A preparation keeps every tool and skill, on either runtime; so does the owner's own chat.
 assert.equal(turnTools(prepCtx.sessionKey),undefined);
 const prepTurn=await hooks.before_prompt_build({},embedded(prepCtx));
 assert.equal(prepTurn.toolsAllow,undefined);assert.equal(prepTurn.prependSystemContext,prep.prependSystemContext);
 assert.equal(await hooks.before_prompt_build({},embedded(main)),undefined);
}
// Preparations read untrusted email. Research, drafting and other changes run;
// only credentials and self-edits stay blocked (loosened at his request October 12 and 14).
const prepOutcome=async(toolName,params,extra={})=>{
 const r=await hooks.before_tool_call({toolName,params,...extra},prepCtx);
 return r?.block?'block':r?.requireApproval?'ask':'run';
};
const expect=async(outcome,cases)=>{for(const [tool,params] of cases)assert.equal(await prepOutcome(tool,params),outcome,tool+' '+JSON.stringify(params));};
{ // An OpenClaw-made workshop skill about assistant_signals repeats the Machine's rules: Machine runs skip it, by
  // name or by its file; other skills still load, and the owner's own chats keep them all. The files are never touched.
 const {mkdirSync,writeFileSync,readFileSync}=await import('node:fs');const {FIXTURE}=await import('./test-env.mjs');
 process.env.OPENCLAW_STATE_DIR=FIXTURE+'/state';const shop=FIXTURE+'/state/agents/main/agent/workshop-skills';
 for(const [name,text] of [['signal-prep','---\nname: signal-prep\n---\nUse assistant_signals status first.'],['gog','---\nname: gog\n---\nSearch mail with gog.']]){
  mkdirSync(`${shop}/${name}`,{recursive:true});writeFileSync(`${shop}/${name}/SKILL.md`,text);
 }
 await expect('block',[['skills_read',{name:'signal-prep'}],['openclaw__skills_read',{name:'signal-prep'}],['read',{path:`${shop}/signal-prep/SKILL.md`}]]);
 await expect('run',[['skills_read',{name:'gog'}],['skills_read',{name:'weather'}],['skills_read',{name:'../signal-prep'}]]);
 assert.equal((await hooks.before_tool_call({toolName:'skills_read',params:{name:'signal-prep'}},ctx)).block,true);  // reviews too
 assert.equal(await hooks.before_tool_call({toolName:'skills_read',params:{name:'signal-prep'}},main),undefined);  // the owner's chat
 assert.ok(readFileSync(`${shop}/signal-prep/SKILL.md`,'utf8').includes('assistant_signals'));
 // A preparation is told which ones, instead of trying each and being refused; the other skills are not named.
 const told=(await hooks.before_prompt_build({},prepCtx)).prependSystemContext;
 assert.ok(told.includes('older copies of those rules: do not read them (signal-prep).'));
 delete process.env.OPENCLAW_STATE_DIR;
}
await expect('run',[['assistant_signals',{action:'prepare'}],['openclawweb_fetch',{url:'https://example.com'}],['memory_search',{}],
  ['browser',{action:'snapshot'}],['exec',{command:"gog gmail messages search 'from:a {b c}' --account x --readonly --json"}],
  ['bash',{command:"/usr/bin/bash -c 'assistant show 42476e61036c4665 --json'"}],['exec',{command:['rg','-n','Acme','memory']}],
  ['exec',{command:"curl -q -fsSL --max-time 15 https://api.example.com/openapi.json | jq '.paths | keys'"}],
  ['exec',{command:'rg -n Zap memory 2>/dev/null | head -20'}],
  ['exec',{command:'python3 integrations/browser-lease.py claim --owner prep --minutes 30'}],
  ['write',{path:'memory/assistant/261011-brief.md',content:'x'}],
  ['apply_patch',{input:'*** Begin Patch\n*** Add File: '+W+'/memory/assistant/261011-x.md\n+x\n*** End Patch'}]]);
assert.equal(await prepOutcome('exec',{},{toolKind:'code_mode_exec'}),'run');  // the runner; its calls are checked one by one
{ // Tool search's runner is not journaled either: journaled, dispatch_action was not preparation_history, so a continued
  // to-do refused every step. The tool it runs passes the hook (and the journal) by its own name.
 const before=calls.length;
 for(const toolName of ['tool_search','tool_describe','dispatch_action'])assert.equal(await prepOutcome(toolName,{id:'assistant_signals',args:{action:'preparation_history'}}),'run',toolName);
 await hooks.after_tool_call({toolName:'dispatch_action',params:{id:'assistant_signals',args:{}},result:{}},prepCtx);
 assert.equal(calls.length,before);
 await prepOutcome('assistant_signals',{action:'preparation_history'});
 assert.equal(calls.at(-1).action,'preparation_tool_intent');assert.equal(calls.at(-1).args.tool,'assistant_signals');
}
// No ask tier any more (October 12): approvals can't reach a background run, so everything not blocked runs.
await expect('run',[['sessions_spawn',{}],['browser',{action:'act',request:{kind:'click'}}],['browser',{}],
  ['exec',{command:'python3 assistant.py call'}],['exec',{command:'npm test'}],['exec',{command:'cat $(ls)'}],
  ['exec',{command:'rg --pre=sh x memory'}],['exec',{command:'curl -X POST https://example.com'}],
  ['exec',{command:'curl http://127.0.0.1:8787/api/state'}],['edit',{path:''+H+'/.bashrc'}],
  ['write',{path:'memory/assistant/../../AGENTS.md',content:'x'}],
  ['apply_patch',{input:'*** Begin Patch\n*** Add File: memory/assistant/a.md\n*** Update File: AGENTS.md\n*** End Patch'}]]);
assert.equal((await hooks.before_tool_call({toolName:'exec',params:{command:'npm test'}},prepCtx))?.requireApproval,undefined);
// Loose on purpose: what the owner asks or confirms runs, including sending,
// deleting, restarts and Google/GitHub writes. Only credentials and self-edits stay blocked.
await expect('run',[['exec',{command:'ls; rm -rf memory/tmp'}],['exec',{command:'gog gmail labels modify x'}],
  ['exec',{command:'git push'}],['exec',{command:'systemctl --user restart x'}],['exec',{command:'openclaw gateway restart'}],
  ['exec',{command:'gh pr create'}],['exec',{command:'sudo ls'}],['message',{action:'send'}],['sessions_send',{}],
  ['exec',{command:'gog gmail send --to a@example.com --subject x --body y'}],['exec',{command:'gog gmail drafts send d1'}],
  ['exec',{command:'gog gmail get 1 --readonly=true'}],['exec',{command:'gog calendar events list --readonly | jq .'}]]);
await expect('block',[['exec',{command:'gog auth add x --readonly'}],['exec',{command:'rg token '+H+''}],
  ['write',{path:W+'/tools/personal-assistant/assistant.py',content:'x'}],
  ['exec',{command:'curl -H "X-Assistant-Owner: k" -d @x http://127.0.0.1:8787/api/action'}],
  ['bash',{command:"/usr/bin/bash -c 'cat "+H+"/.local/share/personal-assistant/api-token'"}],
  ['read',{path:''+H+'/.local/share/personal-assistant/owner-token'}],
  ['write',{path:''+H+'/.local/share/personal-assistant/config.json',content:'x'}]]);
assert.equal((await hooks.before_tool_call({toolName:'read',params:{path:''+H+'/.local/share/personal-assistant/api-token'}},ctx)).block,true);  // reviews too
assert.equal(await hooks.before_tool_call({toolName:'exec',params:{command:'gog gmail send'}},main),undefined);  // main chat keeps its own approvals

const processing='Resumed and finished the interrupted review, then completed one more batch: 78 of 80 signal slots assessed.\nSaved one vendor follow-up suggestion. The incomplete partner signal remains pending. The service’s review-budget gate stopped further claims; this was not a complete inbox review.';
const continuation='Resumed and finished the unfinished review, then committed two more batches. 114 of 120 signal slots assessed; no new suggestion was warranted.\nThe empty newsletter message and incomplete partner text remain pending. This was a bounded review, not a complete inbox or history check.';
const delivery={payload:{text:processing},kind:'final',sessionKey:ctx.sessionKey,runId:ctx.runId};
const destination={channelId:'telegram',accountId:'default',conversationId:'1000001'};
assert.equal(processingOnlyReviewSummary(processing),true);
assert.equal(processingOnlyReviewSummary(continuation),true);
assert.equal((await hooks.reply_payload_sending(delivery,destination)).cancel,true);
assert.equal(await hooks.reply_payload_sending({...delivery,payload:{text:processing+'\nYour meeting starts in 20 minutes.'}},destination),undefined);
assert.equal(processingOnlyReviewSummary('Resumed and finished the interrupted review: your meeting starts now.'),false);
assert.equal(await hooks.reply_payload_sending({...delivery,runId:'another-run'},destination),undefined);
assert.equal(await hooks.reply_payload_sending(delivery,{...destination,conversationId:'shared-chat'}),undefined);
assert.equal(await hooks.reply_payload_sending(delivery,{...destination,accountId:'other-account'}),undefined);
assert.equal(await hooks.reply_payload_sending({...delivery,kind:'tool'},destination),undefined);
assert.equal(await hooks.reply_payload_sending({...delivery,payload:{text:processing,mediaUrl:'/report.pdf'}},destination),undefined);
assert.equal(await hooks.reply_payload_sending({...delivery,payload:{text:'A new suggestion: confirm a time with Peter.'}},destination),undefined);
const internal={...main,runId:'internal-run',trigger:'user',inputProvenance:{kind:'internal_system',sourceTool:'notifications-event'}};
const n=calls.length;
assert.ok((await hooks.before_prompt_build({},internal)).prependContext.includes('exactly NO_REPLY'));
assert.equal(calls.length,n); // A notification is not an extra review trigger.
await hooks.before_tool_call({toolName:'assistant_signals',params:{action:'begin_analysis',args:{}}},internal);
assert.equal((await hooks.reply_payload_sending({...delivery,sessionKey:internal.sessionKey,runId:internal.runId,payload:{text:continuation}},destination)).cancel,true);
review={id:'internal-review',owner_run:internal.runId};
assert.equal((await hooks.before_agent_finalize({},internal)).action,'revise');
await hooks.agent_end({success:true},internal);
assert.equal(calls.at(-1).args.owner_run,internal.runId);assert.equal(calls.at(-1).args.terminal,true);
review=null;
const irrelevantNotification={...internal,runId:'notification-without-review'};
await hooks.before_prompt_build({},irrelevantNotification);
const countBeforeFinish=calls.length;
await hooks.agent_end({success:true},irrelevantNotification);
assert.equal(calls.length,countBeforeFinish);
const human={...main,runId:'human-run',trigger:'user',inputProvenance:{kind:'external_user'}};
assert.equal(await hooks.before_prompt_build({},human),undefined);
await hooks.before_tool_call({toolName:'assistant_signals',params:{action:'finish_analysis',args:{}}},human);
assert.equal(await hooks.reply_payload_sending({...delivery,runId:human.runId},destination),undefined);
assert.equal(await hooks.before_prompt_build({}, {...human,trigger:'heartbeat'}),undefined);
assert.equal(await hooks.reply_payload_sending({...delivery,runId:'unproven-internal'},destination),undefined);
console.log('Quiet reviews: both real leaked summaries canceled; internal continuations, user replies, mixed alerts, media, scope and service-owned suggestions protected.');
