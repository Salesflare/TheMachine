import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
// Run the actual helper with only the SDK import replaced. No live Gateway calls.
const source=(await readFile(new URL('../preparation-run.mjs',import.meta.url),'utf8')).replace(/^import \{gatewayRuntime\}.*;\nconst \{callGatewayFromCli\}=await gatewayRuntime\(\);$/m,'');
const execute=new (Object.getPrototypeOf(async function(){}).constructor)('callGatewayFromCli','process',source);
const id='a'.repeat(32);
async function run(request,replies){
  const calls=[];let output='';
  await execute(async(method,options,args,scope)=>{
    calls.push({method,options,args,scope});
    const value=replies.shift();if(value instanceof Error)throw value;return value;
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
  ['unexpected private email text','unclassified'],
]){
  r=await run({kind:'review',job_id:id,action:'status'},[{status:'error',error:text}]);
  assert.equal(r.result.error,'runtime_error');assert.equal(r.result.reason,reason);assert.ok(!JSON.stringify(r.result).includes('private'));
}
r=await run({kind:'review',job_id:id,action:'status'},[{status:'error',error:'HTTP 429 rate limit'}]);assert.equal(r.result.reason,undefined);
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
    ['Claude AI usage limit reached|'+(t0+3600),v=>v===t0+3600],
    ['You have hit your limit, try again in 2h 30m',v=>Math.abs(v-(t0+9000))<5],
    ['Provider openai is in cooldown',v=>v===undefined],
  ]){
    r=await run({kind:'review',job_id:id,action:'status'},[{status:'error',error:text}]);
    assert.equal(r.result.error,'usage_limited');assert.equal(r.result.error_phase,'model');
    assert.ok(check(r.result.retry_at),text);assert.ok(!JSON.stringify(r.result).includes('private'));
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
// Try again on a stuck preparation stops only its exact isolated session and run.
r=await run({kind:'preparation',job_id:id,action:'stop'},[{ok:true,status:'no-active-run',abortedRunId:null}]);
assert.equal(r.result.status,'lost');assert.equal(r.calls[0].args.key,'agent:main:assistant-review-preparation-'+id);assert.equal(r.calls[0].args.runId,id);
await assert.rejects(()=>run({kind:'other',job_id:id,action:'stop'},[]));
console.log('Exact-run recovery, wait-only timeout, cancellation proof and admission idempotency passed.');
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
