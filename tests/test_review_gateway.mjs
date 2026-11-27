import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
// Run the actual helper with only the SDK import replaced. No live Gateway calls.
const source=(await readFile(new URL('../preparation-run.mjs',import.meta.url),'utf8')).replace(/^import \{gatewayRuntime\}.*;\nconst \{callGatewayFromCli\}=await gatewayRuntime\(\);$/m,'');
const execute=new (Object.getPrototypeOf(async function(){}).constructor)('callGatewayFromCli','process',source);
const id='a'.repeat(32);
async function run(request,replies){
  const calls=[];let output='',described;
  await execute(async(method,options,args,scope)=>{
    calls.push({method,options,args,scope});
    // Like the real Gateway (OpenClaw 2026.11.2 sessions-patch-admission): a lifecycle patch (archived) needs the
    // session's current sessionId as expectedSessionId, the one its row (sessions.describe) shows.
    if(method==='sessions.patch'&&typeof args.archived==='boolean'&&
        (args.expectedSessionId===undefined||args.expectedSessionId!==described)){
      throw Object.assign(new Error(args.expectedSessionId===undefined?`expectedSessionId required for session lifecycle patch: ${args.key}`:
        `session changed: ${args.key}`),{name:'GatewayClientRequestError',gatewayCode:'INVALID_REQUEST'});
    }
    const value=replies.shift();
    if(method==='sessions.describe'&&!(value instanceof Error))described=(value?.session??value)?.sessionId;
    if(value instanceof Error)throw value;return value;
  },{stdin:{async *[Symbol.asyncIterator](){yield JSON.stringify(request)}},stdout:{write(value){output+=value}}});
  return {calls,result:JSON.parse(output)};
}
let r=await run({kind:'review',job_id:id,action:'stop'},[{ok:true,status:'no-active-run',abortedRunId:null}]);
assert.equal(r.result.status,'lost');
assert.deepEqual(r.calls[0].args,{key:'agent:main:assistant-review-signals-'+id,agentId:'main',runId:id,clearQueued:true});
r=await run({kind:'review',job_id:id,action:'stop'},[{ok:true,status:'aborted',abortedRunId:id},{status:'timeout'}]);
assert.equal(r.result.status,'pending');  // abort admission is not terminal proof
r=await run({kind:'review',job_id:id,action:'stop'},[{ok:true,status:'aborted',abortedRunId:id},{status:'timeout',endedAt:123}]);
assert.equal(r.result.status,'timed_out');
r=await run({kind:'preparation',job_id:id,action:'stop'},[{ok:true,status:'aborted',abortedRunId:id},{status:'aborted',endedAt:123}]);
assert.equal(r.result.status,'aborted');  // a preparation we stopped did not time out
// Past the queue, a session whose complete active set lacks the run proves a restart lost it; unknown sets prove nothing.
r=await run({kind:'preparation',job_id:id,action:'status',probe:true},[{status:'timeout'},{session:{hasActiveRun:true,activeRunIds:['b'.repeat(32)]}}]);
assert.equal(r.result.status,'lost');assert.equal(r.calls[1].method,'sessions.describe');
for(const row of [{session:{hasActiveRun:true}},{session:{activeRunIds:null}},{session:{activeRunIds:[id]}},new Error('offline')]){
  r=await run({kind:'preparation',job_id:id,action:'status',probe:true},[{status:'timeout'},row]);assert.equal(r.result.status,'pending');
}
r=await run({kind:'preparation',job_id:id,action:'status'},[{status:'timeout'}]);assert.equal(r.calls.length,1);  // no probe while young
// A review gone from its own session after a Gateway restart: restart recovery's turn running there carries it on
// (pending), and with nothing running it is absent, not lost: the service waits for recovery. Nothing is released.
r=await run({kind:'review',job_id:id,action:'status',probe:true},[{status:'timeout'},{session:{hasActiveRun:true,activeRunIds:['b'.repeat(32)]}}]);
assert.equal(r.result.status,'pending');assert.equal(r.calls.length,2);
r=await run({kind:'review',job_id:id,action:'status',probe:true},[{status:'timeout'},{session:{hasActiveRun:false,activeRunIds:[]}}]);
assert.deepEqual(r.result,{run_id:id,status:'absent'});assert.equal(r.calls.length,2);  // no sessions.abort
r=await run({kind:'review',job_id:id,action:'status',probe:true},[{status:'timeout'},{session:{activeRunIds:[id]}}]);
assert.equal(r.result.status,'pending');
for(const response of [{ok:true,status:'aborted',abortedRunId:'b'.repeat(32)},{ok:true,status:'no-active-run',warning:'cleanup pending'},new Error('offline')]){
  r=await run({kind:'review',job_id:id,action:'stop'},[response]);assert.equal(r.result.status,'unavailable');
}
r=await run({kind:'review',job_id:id,action:'status'},[{status:'timeout'}]);assert.equal(r.result.status,'pending');
r=await run({kind:'review',job_id:id,action:'status'},[{status:'timeout',endedAt:123}]);assert.equal(r.result.status,'timed_out');
// Actual installed wait fields survive as small categories, never raw private text.
for(const [response,error,phase] of [
  [{status:'error',error:'LLM idle timeout (120s): no response from model; private token=abc'},'model_idle_timeout','model'],
  [{status:'error',error:'before_tool_call hook failed: PluginInstanceUnavailableError secret=abc'},'bridge_error','bridge'],
  [{status:'error',error:'ENOTFOUND private.example.com'},'connection_error','connection'],
  [{status:'error',error:'HTTP 429 rate limit; private token=abc'},'rate_limited','model'],
  [{status:'timeout',endedAt:123,error:'timed out',timeoutPhase:'queue'},'runtime_timeout','queue'],
  [{status:'error',error:'unexpected private email text'},'runtime_error','runtime'],
  [{status:'aborted'},'runtime_aborted','runtime'],
]){
  r=await run({kind:'review',job_id:id,action:'status'},[response]);
  assert.equal(r.result.error,error);assert.equal(r.result.error_phase,phase);
  assert.ok(!JSON.stringify(r.result).includes('private'));assert.ok(!JSON.stringify(r.result).includes('abc'));
}
// A generic runtime error keeps a reason from a fixed list (2026-10-30: the Gateway's MCP runtime limit stalled reviews).
for(const [text,reason] of [
  ['bundle-mcp: live runtime limit (256) reached; stop or reset unused sessions private','mcp_runtime_limit'],
  ['The AI service is temporarily overloaded. Please try again in a moment. | server_is_overloaded private','provider_overloaded'],
  ['request failed status=503 private','provider_error'],
  ['OpenClaw stopped this turn after 3 consecutive identical tool failures. private','repeated_tool_error'],
  ['worker task capacity reached: code=overloaded private','unclassified'],
  ['unexpected private email text','unclassified'],
]){
  r=await run({kind:'review',job_id:id,action:'status'},[{status:'error',error:text}]);
  assert.equal(r.result.error,'runtime_error');assert.equal(r.result.reason,reason);assert.ok(!JSON.stringify(r.result).includes('private'));
}
r=await run({kind:'review',job_id:id,action:'status'},[{status:'error',error:'HTTP 429 rate limit'}]);assert.equal(r.result.reason,undefined);
// A Claude sign-in that lapsed (2026-11-27: two Machines' reviews failed for hours as "unclassified"): Claude Code's and
// OpenClaw's own words, and OpenClaw's failover class when the words say nothing
for(const [response,reason] of [
  [{status:'error',error:'Not logged in · Please run /login private'},'auth_failed'],
  [{status:'error',error:'OAuth token has expired. Please obtain a new token private'},'auth_failed'],
  // a refresh that failed before the sign-in's end (2026-11-27: reported as "unclassified")
  [{status:'error',error:'Failed to authenticate: OAuth session expired and could not be refreshed private'},'auth_failed'],
  [{status:'error',error:'CLI backend "claude-cli" could not materialize selected auth profile "x". Re-authenticate with: openclaw models auth login. private'},'auth_failed'],
  [{status:'error',error:'no auth profile for anthropic private'},'auth_missing'],
  [{status:'error',error:'Your credit balance is too low to access the Anthropic API. private'},'billing'],
  [{status:'error',error:'LLM request failed.',errorObservation:{failoverReason:'auth'}},'auth_failed'],
  [{status:'error',error:'LLM request failed.',errorObservation:{failoverReason:'overloaded'}},'provider_overloaded'],
  [{status:'error',error:'LLM request failed.',errorObservation:{failoverReason:'server_error'}},'provider_error'],
  [{status:'error',error:'LLM request failed.',failoverReason:'billing'},'billing'],
  [{status:'error',error:'LLM request failed.',errorObservation:{failoverReason:'format'}},'unclassified'],
  [{status:'error',error:'LLM request failed.',errorObservation:{failoverReason:'toString'}},'unclassified'],
  [{status:'error',error:'LLM request failed.'},'unclassified'],
]){
  r=await run({kind:'review',job_id:id,action:'status'},[response]);
  assert.equal(r.result.error,'runtime_error');assert.equal(r.result.reason,reason,JSON.stringify(response));assert.ok(!JSON.stringify(r.result).includes('private'));
}
// A finished review, profile or skills run releases its one-off session's MCP connections; a pending one and a
// preparation (a to-do's chat, used again) keep theirs, and a failed release changes nothing.
for(const [kind,prefix] of [['review','signals'],['profile','profile'],['skills','skills']]){
  r=await run({kind,job_id:id,action:'status'},[{status:'ok'},{ok:true,status:'no-active-run'}]);
  assert.equal(r.result.status,'ok');assert.equal(r.calls[1].method,'sessions.abort');
  assert.deepEqual(r.calls[1].args,{key:`agent:main:assistant-review-${prefix}-`+id,agentId:'main',clearQueued:true});
}
r=await run({kind:'review',job_id:id,action:'status'},[{status:'error',error:'x'},new Error('offline')]);
assert.equal(r.result.status,'error');assert.equal(r.calls.length,2);
r=await run({kind:'review',job_id:id,action:'stop'},[{ok:true,status:'no-active-run',abortedRunId:null},{ok:true,status:'no-active-run'}]);
assert.equal(r.result.status,'lost');assert.equal(r.calls[1].args.runId,undefined);
r=await run({kind:'review',job_id:id,action:'status'},[{status:'timeout'}]);assert.equal(r.calls.length,1);
r=await run({kind:'preparation',job_id:id,action:'status'},[{status:'ok'}]);assert.equal(r.calls.length,1);
// Claude Code's runtime fails a NO_REPLY-only final as an empty response: marked, so the service can judge by what was saved
r=await run({kind:'review',job_id:id,action:'status'},[{status:'error',error:'CLI backend returned an empty response.'}]);
assert.deepEqual(r.result,{run_id:id,status:'error',error:'runtime_error',error_phase:'runtime',silent_end:true});
r=await run({kind:'review',job_id:id,action:'status'},[{status:'error',error:'CLI backend returned an empty response. private'}]);
assert.equal(r.result.silent_end,undefined);
// A sign-in's usage limit is its own category, with only the reset time kept (2026-10-25: retried every few minutes).
{
  const t0=Math.round(Date.now()/1000);
  for(const [text,check] of [
    ["You've reached your Codex subscription usage limit. Next reset Oct 25, 11:12 PM UTC. private",v=>v>t0&&new Date(v*1000).getUTCHours()===23&&new Date(v*1000).getUTCMinutes()===12],
    // A clock time wins over the rounded span next to it (2026-11-22: "in 3 days" held the work 7 hours past the reset)
    ["You've reached your Codex subscription usage limit. Next reset in 3 days, Nov 25 at 8:33 AM UTC. Wait until the reset time. private",
      v=>v>t0&&new Date(v*1000).getUTCHours()===8&&new Date(v*1000).getUTCMinutes()===33],
    ["You've reached your Codex subscription usage limit. Next reset in 17 hours, Nov 23 at 8:16 PM UTC. private",
      v=>v>t0&&new Date(v*1000).getUTCHours()===20&&new Date(v*1000).getUTCMinutes()===16],
    ['Claude AI usage limit reached|'+(t0+3600),v=>v===t0+3600],
    ['You have hit your limit, try again in 2h 30m',v=>Math.abs(v-(t0+9000))<5],
    ['Provider openai is in cooldown',v=>v===undefined],
    // ChatGPT's own words over HTTP, as OpenClaw 2026.11.2 passes them on
    ['\u26a0\ufe0f You have hit your ChatGPT usage limit (plus plan). Try again in ~2580 min.',v=>Math.abs(v-(t0+2580*60))<5],
    ['\u26a0\ufe0f You have hit your ChatGPT usage limit (plus plan). Try again in ~2580 min.; Retry-After: 154800 seconds',v=>Math.abs(v-(t0+2580*60))<5],
  ]){
    r=await run({kind:'review',job_id:id,action:'status'},[{status:'error',error:text}]);
    assert.equal(r.result.error,'usage_limited');assert.equal(r.result.error_phase,'model');
    assert.ok(check(r.result.retry_at),text);assert.ok(!JSON.stringify(r.result).includes('private'));
  }
}
// What OpenClaw 2026.11.2 says instead of the limit itself (2026-11-25: unclassified, and a to-do stopped): its rewritten
// rate limit (ChatGPT's "Codex error: The usage limit has been reached" over its WebSocket, or a 429 without plan or
// reset), all sign-ins resting, a limit the Codex account doesn't report. Which limit it was is the service's to read.
for(const text of ['\u26a0\ufe0f The AI service needs a short break. Please try again in a few minutes.',
    '\u26a0\ufe0f The AI service needs a short break. Please try again in ~60 min.',
    'openai is asking us to slow down. Please wait a moment before trying again.',
    'Codex rejected the request with a usage-limit error, but its current account usage does not report an exhausted limit. Retry the request.']){
  for(const kind of ['review','preparation','profile','skills','routine']){
    r=await run({kind,job_id:id,action:'status'},[{status:'error',error:text},{ok:true}]);
    assert.deepEqual(r.result,{run_id:id,status:'error',error:'rate_limited',error_phase:'model'});
  }
}
// Background work can name a cheaper model; anything malformed is dropped.
r=await run({kind:'review',job_id:id,action:'start',message:'Review',provider:'openai',model:'gpt-6.1-sol'},[{runId:id}]);
assert.equal(r.calls[0].args.provider,'openai');assert.equal(r.calls[0].args.model,'gpt-6.1-sol');
r=await run({kind:'review',job_id:id,action:'start',message:'Review',provider:'openai',model:'x y; rm'},[{runId:id}]);
assert.equal(r.calls[0].args.model,undefined);assert.equal(r.calls[0].args.provider,undefined);
r=await run({kind:'review',job_id:id,action:'status'},[{status:'pending',timeoutPhase:'queue'}]);
assert.equal(r.result.status,'pending');assert.equal(r.result.error,undefined);
r=await run({kind:'review',job_id:id,action:'start',message:'Review'},[{runId:id}]);
assert.equal(r.result.status,'admitted');assert.equal(r.calls[0].args.idempotencyKey,id);
assert.equal(r.calls[0].args.deliver,false);assert.equal(r.calls[0].args.disableMessageTool,true);
// Every Machine run gets OpenClaw's smaller prompt and none of the workspace's own files (the plugin adds USER.md and
// what else it needs), a preparation and the to-do chat in its session too, as on a hosted Machine.
for(const kind of ['review','profile','skills','routine','preparation']){
  r=await run({kind,job_id:id,action:'start',message:'Read'},[{runId:id}]);
  assert.equal(r.calls[0].args.promptMode,'minimal',kind);assert.equal(r.calls[0].args.bootstrapContextMode,'lightweight',kind);
}
r=await run({kind:'preparation',job_id:id,session_job_id:'b'.repeat(32),action:'start',message:'A to-do chat turn',fast:false},[{ok:true},{runId:id}]);
assert.equal(r.calls.at(-1).args.promptMode,'minimal');assert.equal(r.calls.at(-1).args.bootstrapContextMode,'lightweight');
// A refused start keeps its key (it may have been admitted) unless the Gateway says the run id's turn is over.
const refusal=Object.assign(new Error('Pending input ownership ended; submit a new turn to continue'),{name:'GatewayClientRequestError',gatewayCode:'UNAVAILABLE'});
r=await run({kind:'review',job_id:id,action:'start',message:'Review'},[refusal,{status:'error',endedAt:123}]);
assert.deepEqual(r.result,{run_id:id,status:'lost',error:'runtime_lost',error_phase:'runtime'});
for(const other of [Object.assign(new Error('codex app-server request timed out'),{name:'GatewayClientRequestError'}),new Error('submit a new turn')]){
  r=await run({kind:'review',job_id:id,action:'start',message:'Review'},[other]);assert.equal(r.result.status,'unavailable');
}
// Refusal text alone never authorizes replay while the old execution could still exist.
r=await run({kind:'preparation',job_id:id,action:'start',message:'Work'},[refusal,{status:'pending'},new Error('offline')]);
assert.equal(r.result.status,'unavailable');
assert.deepEqual(r.calls[2].args,{key:'agent:main:assistant-review-preparation-'+id,agentId:'main',runId:id,clearQueued:true});
r=await run({kind:'preparation',job_id:id,action:'start',message:'Work'},[refusal,{status:'pending'},{ok:true,status:'no-active-run',abortedRunId:null}]);
assert.equal(r.result.status,'lost');
r=await run({kind:'review',job_id:id,action:'start',message:'Review'},[refusal,{status:'pending'},{ok:true,status:'aborted',abortedRunId:id},{status:'timeout'}]);
assert.equal(r.result.status,'unavailable');
// The Gateway accepted this key with other content (OpenClaw 2026.11.2, after a restart): refused for good, so once the
// exact run is proven gone it is lost and starts again under a fresh key, instead of retrying until the deadline.
for(const text of ['Pending input idempotency key conflicts with the accepted input','Input completion idempotency key conflicts with the accepted input']){
  const conflict=Object.assign(new Error(text),{name:'GatewayClientRequestError',gatewayCode:'UNAVAILABLE'});
  r=await run({kind:'preparation',job_id:id,action:'start',message:'Work'},[conflict,{status:'pending'},{ok:true,status:'no-active-run',abortedRunId:null}]);
  assert.deepEqual(r.result,{run_id:id,status:'lost',error:'runtime_lost',error_phase:'runtime'});
  assert.deepEqual(r.calls[2].args,{key:'agent:main:assistant-review-preparation-'+id,agentId:'main',runId:id,clearQueued:true});
  r=await run({kind:'preparation',job_id:id,action:'start',message:'Work'},[conflict,{status:'pending'},new Error('offline')]);
  assert.equal(r.result.status,'unavailable');  // not proven gone: keeps the key, never a second run beside it
}
// Try again on a stuck preparation stops only its exact isolated session and run.
r=await run({kind:'preparation',job_id:id,action:'stop'},[{ok:true,status:'no-active-run',abortedRunId:null}]);
assert.equal(r.result.status,'lost');assert.equal(r.calls[0].args.key,'agent:main:assistant-review-preparation-'+id);assert.equal(r.calls[0].args.runId,id);
await assert.rejects(()=>run({kind:'other',job_id:id,action:'stop'},[]));
console.log('Exact-run recovery, wait-only timeout, cancellation proof and admission idempotency passed.');
// A start that can never succeed is over as what it is, before any Gateway call (2026-11-24: one too long was retried as
// "unavailable" until the deadline). Characters, as the service counts them: an emoji is one.
for(const kind of ['preparation','review','profile','skills','routine']){
  r=await run({kind,job_id:id,action:'start',message:'x'.repeat(60001)},[]);
  assert.deepEqual([r.result,r.calls],[{run_id:id,status:'error',error:'prompt_too_long',error_phase:'runtime'},[]]);
  for(const message of ['\u{1F600}'.repeat(60000),'x'.repeat(60000)]){
    r=await run({kind,job_id:id,action:'start',message},[{runId:id}]);assert.equal(r.result.status,'admitted');
  }
  for(const message of [undefined,' ']){
    r=await run({kind,job_id:id,action:'start',message},[]);
    assert.deepEqual([r.result,r.calls],[{run_id:id,status:'error',error:'invalid_request',error_phase:'runtime'},[]]);
  }
}
r=await run({kind:'preparation',job_id:id,action:'start',message:'Work',attachments:[{type:'image',mimeType:'text/html',fileName:'a',content:''}]},[]);
assert.deepEqual([r.result,r.calls],[{run_id:id,status:'error',error:'invalid_attachments',error_phase:'runtime'},[]]);
// Fast (chat_model.py): the session's speed is set right before a to-do chat's turn; OpenClaw sends each provider's own
// fast option. Back to standard for the next turn of a session that ran fast: when that fails, nothing starts, so
// background work never runs fast. A failed "fast" leaves the turn at standard speed.
{
  const msg={kind:'preparation',job_id:id,action:'start',message:'hi'},key='agent:main:assistant-review-preparation-'+id,admitted={runId:id};
  r=await run({...msg,fast:true},[{ok:true},admitted]);
  assert.deepEqual(r.calls.map(c=>c.method),['sessions.patch','agent']);assert.deepEqual(r.calls[0].args,{key,fastMode:true});
  assert.equal(r.calls[1].args.fastMode,undefined);assert.deepEqual(r.result,{run_id:id,status:'admitted',fast:'fast'});
  r=await run({...msg,fast:false},[{ok:true},admitted]);
  assert.deepEqual(r.calls[0].args,{key,fastMode:false});assert.equal(r.result.fast,'standard');
  r=await run({...msg,fast:false},[new Error('offline')]);
  assert.deepEqual(r.calls.map(c=>c.method),['sessions.patch']);assert.equal(r.result.status,'unavailable');
  r=await run({...msg,fast:true},[new Error('offline'),admitted]);
  assert.deepEqual(r.calls.map(c=>c.method),['sessions.patch','agent']);assert.equal(r.result.fast,'unavailable');
  r=await run(msg,[admitted]);  // no choice sent: the turn goes as before, no session change
  assert.deepEqual(r.calls.map(c=>c.method),['agent']);assert.equal(r.result.fast,undefined);
  r=await run({kind:'review',job_id:id,action:'start',message:'hi',fast:true},[admitted]);  // never for a review
  assert.deepEqual(r.calls.map(c=>c.method),['agent']);
}
// A start that can't reach the Gateway at all (down after a reboot) says so: the service waits for it without a
// deadline (2026-11-02). A timeout or refusal is not proof it is down: it says only its fixed code, for the log.
for(const down of [new Error('connect ECONNREFUSED 127.0.0.1:18789'),new Error('gateway closed (1006): ')]){
  r=await run({kind:'preparation',job_id:id,action:'start',message:'Work'},[down]);
  assert.deepEqual(r.result,{run_id:id,status:'unavailable',reason:'offline'});
}
for(const [other,why] of [[new Error('gateway timeout after 15000ms'),'timeout'],[refusal,'refused'],[new Error('private words'),'other']]){
  r=await run({kind:'preparation',job_id:id,action:'start',message:'Work'},[other,{status:'pending'},new Error('later')]);
  assert.equal(r.result.status,'unavailable');assert.equal(r.result.reason,why);assert.ok(!JSON.stringify(r.result).includes('private'));
}
// A to-do's chat left alone past OpenClaw's retention is archived, and the Gateway refuses new work in it. A new signal
// reopening the to-do weeks later restores the chat and starts the turn, instead of being refused every minute while the
// to-do says it waits for the AI (2026-11-20). One that can't be restored fails the start; offline still waits.
{
  const key='agent:main:assistant-review-preparation-'+id,msg={kind:'preparation',job_id:id,action:'start',message:'Work'};
  const archived=()=>Object.assign(new Error(`Session "${key}" is archived. Restore it before starting new work.`),{name:'GatewayClientRequestError',gatewayCode:'INVALID_REQUEST'});
  // The restore names the session's current sessionId (the Gateway refuses a lifecycle patch without it).
  const row={session:{key,sessionId:'s-1',archived:true}};
  r=await run(msg,[archived(),row,{ok:true},{runId:id}]);
  assert.deepEqual(r.calls.map(c=>c.method),['agent','sessions.describe','sessions.patch','agent']);
  assert.deepEqual(r.calls[1].args,{key,agentId:'main'});
  assert.deepEqual(r.calls[2].args,{key,archived:false,expectedSessionId:'s-1'});assert.equal(r.calls[3].args.idempotencyKey,id);
  assert.deepEqual(r.result,{run_id:id,status:'admitted'});
  r=await run({...msg,fast:false},[archived(),row,{ok:true},{ok:true},{runId:id}]);  // the speed reset hits it first
  assert.deepEqual(r.calls.map(c=>c.method),['sessions.patch','sessions.describe','sessions.patch','sessions.patch','agent']);assert.equal(r.result.status,'admitted');
  // Not restorable: the patch refused, no row (or no sessionId), or still archived after the restore.
  for(const replies of [[archived(),row,new Error('not allowed')],[archived(),{session:null}],[archived(),{session:{key}}],
      [archived(),new Error('not allowed')],[archived(),row,{ok:true},archived()]]){
    r=await run(msg,replies);
    assert.deepEqual(r.result,{run_id:id,status:'error',error:'session_archived',error_phase:'session'});
    assert.ok(!r.calls.some(c=>c.method==='sessions.patch'&&c.args.archived===false&&c.args.expectedSessionId===undefined));
  }
  for(const replies of [[archived(),new Error('connect ECONNREFUSED 127.0.0.1:18789')],[archived(),row,new Error('connect ECONNREFUSED 127.0.0.1:18789')]]){
    r=await run(msg,replies);
    assert.deepEqual(r.result,{run_id:id,status:'unavailable',reason:'offline'});
  }
  r=await run(msg,[archived(),row,{ok:true},new Error('gateway timeout after 20000ms')]);  // may have been admitted: keeps its key
  assert.deepEqual(r.result,{run_id:id,status:'unavailable',reason:'timeout'});
  r=await run(msg,[Object.assign(new Error('archived'),{name:'GatewayClientRequestError'})]);  // other text: no restore
  assert.deepEqual(r.calls.map(c=>c.method),['agent']);assert.equal(r.result.status,'unavailable');
}
