// One service-started turn in the existing main agent, through the installed Gateway:
// a preparation for an accepted suggestion, a signal review, a profile draft (assistant profile) or Find my skills. Each runs in its own
// isolated session with message delivery off. No model/client credentials here.
import {gatewayRuntime} from './openclaw-root.mjs';
const {callGatewayFromCli}=await gatewayRuntime();
let input=''; for await (const chunk of process.stdin) input+=chunk;
const request=JSON.parse(input);
const kind=request.kind || 'preparation';
if (!/^[a-f0-9]{32}$/.test(request.job_id || '') || !['start','status','stop'].includes(request.action) || !['preparation','review','profile','skills'].includes(kind)) {
  throw new Error('Invalid request');
}
const session={preparation:'agent:main:assistant-review-preparation-', review:'agent:main:assistant-review-signals-', profile:'agent:main:assistant-review-profile-', skills:'agent:main:assistant-review-skills-'}[kind];
const sessionId=request.session_job_id || request.job_id;
if (!/^[a-f0-9]{32}$/.test(sessionId) || (kind!=='preparation' && sessionId!==request.job_id)) throw new Error('Invalid session');
// Do it turns make and test real changes (2026-10-13), so they get as long as a review.
const runSeconds={preparation:1200, review:1200, profile:900, skills:900}[kind];
const scope={scopes:['operator.admin','operator.read','operator.write']};
const USAGE_LIMIT=/usage limit|(?:reached|hit) (?:your|the) [a-z0-9 -]*limit|limit (?:reached|exceeded)|insufficient_quota|quota exceeded|in cooldown|out of (?:credits|usage)/i;
// When a usage limit lifts, from the provider's own words: an epoch (Claude: "limit reached|1761500000"), "in 2h 5m" or
// "try again in 30 minutes", or a clock time "11:12 PM UTC" (the next one). Only the time is kept, never the text.
function resetAt(text, now=Date.now()){
  const epoch=text.match(/\|(\d{10})\b/);
  if(epoch)return Number(epoch[1]);
  const span=text.match(/\b(?:in|after)\s+((?:\d+\s*(?:days?|d|hours?|hrs?|h|minutes?|mins?|m|seconds?|secs?|s)\b[\s,]*(?:and\s+)?)+)/i);
  if(span){
    let seconds=0;
    for(const [,n,unit] of span[1].matchAll(/(\d+)\s*([a-z]+)/gi)){
      const u=unit.toLowerCase();
      seconds+=Number(n)*(u.startsWith('d')?86400:u.startsWith('h')?3600:u.startsWith('m')?60:1);
    }
    if(seconds>0)return Math.round(now/1000)+seconds;
  }
  const clock=text.match(/reset[^0-9]{0,40}?(?:([A-Z][a-z]{2,8}\.? \d{1,2}),? )?(\d{1,2}):(\d{2})\s*(AM|PM)?\s*(UTC|GMT)?/i);
  if(clock){
    let hours=Number(clock[2])%12+(/pm/i.test(clock[4]||'')?12:0);
    if(!clock[4])hours=Number(clock[2]);
    const at=new Date(now);at.setUTCHours(hours,Number(clock[3]),0,0);
    if(clock[1]){const day=new Date(`${clock[1]} ${new Date(now).getUTCFullYear()} 00:00 UTC`);
      if(!Number.isNaN(day.getTime()))at.setUTCFullYear(day.getUTCFullYear(),day.getUTCMonth(),day.getUTCDate());}
    while(at.getTime()<=now)at.setUTCDate(at.getUTCDate()+1);
    return Math.round(at.getTime()/1000);
  }
  return null;
}
// Retain useful failure categories, never raw provider text, endpoints or parameters.
function failure(result,status){
  if(status==='ok'||status==='admitted'||status==='pending')return {};
  const text=[result?.error?.message,result?.error,result?.errorMessage,result?.summary].filter(v=>typeof v==='string').join(' ');
  let error=status==='timed_out'?'runtime_timeout':status==='aborted'?'runtime_aborted':status==='lost'?'runtime_lost':'runtime_error';
  let phase='runtime';
  if(USAGE_LIMIT.test(text)){
    // The sign-in's usage limit (ChatGPT, Claude), not a short rate limit: the service waits until the reset it names.
    const retryAt=resetAt(text);
    return {error:'usage_limited',error_phase:'model',...(retryAt?{retry_at:retryAt}:{})};
  }
  if(/LLM idle timeout/i.test(text)){error='model_idle_timeout';phase='model';}
  else if(/before_tool_call|PluginInstanceUnavailable|failurePhase[^a-z]*bridge/i.test(text)){error='bridge_error';phase='bridge';}
  else if(/rate.?limit|\b429\b/i.test(text)){error='rate_limited';phase='model';}
  else if(/ECONNRESET|ECONNREFUSED|ENOTFOUND|EAI_AGAIN|connection (?:reset|closed)|network/i.test(text)){error='connection_error';phase='connection';}
  else if(/timeout|timed out/i.test(text)){error='runtime_timeout';}
  else if(/abort|cancel/i.test(text)){error='runtime_aborted';}
  if(['queue','provider','model','tool','gateway_draining'].includes(result?.timeoutPhase))phase=result.timeoutPhase;
  return {error,error_phase:phase};
}
try {
  let result;
  if (request.action==='start') {
    if (typeof request.message!=='string' || request.message.length>60000) throw new Error('Invalid prompt');  // PROMPT_LIMIT in assistant.py
    // Images the owner added to their chat message (chat_files.py): sent to the model as images. Other files are in
    // the run's attachments folder, named in the message.
    const IMAGE=/^image\/(?:png|jpeg|gif|webp)$/;
    const attachments=Array.isArray(request.attachments)?request.attachments:[];
    if (attachments.length>5 || attachments.some(a=>a?.type!=='image' || !IMAGE.test(a.mimeType||'') || typeof a.fileName!=='string' ||
        a.fileName.length>200 || typeof a.content!=='string' || a.content.length>7*1024*1024 || !/^[A-Za-z0-9+/]*={0,2}$/.test(a.content)) ||
        attachments.reduce((n,a)=>n+a.content.length,0)>20*1024*1024) throw new Error('Invalid attachments');
    result=await callGatewayFromCli('agent',{timeout:'20000'}, {
      agentId:'main', sessionKey:session+sessionId,
      message:request.message, idempotencyKey:request.job_id, timeout:runSeconds,
      deliver:false, disableMessageTool:true,
      ...(attachments.length?{attachments:attachments.map(a=>({type:'image', mimeType:a.mimeType, fileName:a.fileName, content:a.content}))}:{}),
      // Background work never runs on the costliest model: the service names the one to use instead (assistant.py
      // background_model), only one the owner's model allowlist allows.
      ...(typeof request.provider==='string' && typeof request.model==='string' &&
          /^[a-z0-9-]{1,40}$/.test(request.provider) && /^[a-z0-9.:-]{1,80}$/i.test(request.model) ? {provider:request.provider, model:request.model}:{}),
    },scope);
    if (result?.runId!==request.job_id) throw new Error('Unconfirmed admission');
    process.stdout.write(JSON.stringify({run_id:request.job_id,status:'admitted'}));
  } else if (request.action==='stop') {
    // After the normal runtime plus an outage grace period, stop only our exact
    // isolated turn. A successful no-active-run receipt also reconciles a run
    // lost in a Gateway restart. Unknown/failed responses never release custody.
    result=await callGatewayFromCli('sessions.abort',{timeout:'15000'}, {
      key:session+sessionId, agentId:'main', runId:request.job_id, clearQueued:true,
    },scope);
    const stopped=result?.ok===true && !result?.warning && result?.status==='aborted' && result?.abortedRunId===request.job_id;
    const absent=result?.ok===true && !result?.warning && result?.status==='no-active-run' && !result?.abortedRunId;
    let status=absent?'lost':'unavailable', outcome;
    if (stopped) {
      outcome=await callGatewayFromCli('agent.wait',{timeout:'15000'}, {runId:request.job_id,timeoutMs:0},scope);
      // Cancellation was admitted, but don't claim the old runtime has finished
      // until its terminal outcome (or the next exact no-active-run receipt).
      // A preparation is stopped only when it is no longer wanted or ran past its time; recorded as aborted, not as the
      // model timing out. Reviews keep timed_out: their tries and back-off count it.
      status=outcome?.endedAt && ['ok','error','aborted','timeout'].includes(outcome?.status) ? (kind==='preparation'?'aborted':'timed_out'):'pending';
    }
    process.stdout.write(JSON.stringify({run_id:request.job_id,status,...failure(outcome,status)}));
  } else {
    result=await callGatewayFromCli('agent.wait',{timeout:'15000'}, {runId:request.job_id,timeoutMs:0},scope);
    let status=['ok','error','aborted'].includes(result?.status)?result.status:
        result?.status==='timeout' && result?.endedAt ? 'timed_out':'pending';
    // A Gateway crash or restart ends a run without a terminal state for its id (restart recovery resumes the
    // session under a new run id). Once the run is past the queue, an exact session row whose complete set of
    // active runs doesn't hold ours proves it is gone. Omitted or null ids prove nothing: keep waiting.
    if (status==='pending' && request.probe===true) {
      try {
        const row=await callGatewayFromCli('sessions.describe',{timeout:'15000'},{key:session+sessionId,agentId:'main'},scope);
        const ids=(row?.session ?? row)?.activeRunIds;
        if (Array.isArray(ids) && !ids.includes(request.job_id)) {
          status='lost'; result={error:'run not active in its session (Gateway restart?)'};
        }
      } catch {}  // unknown: stay pending
    }
    process.stdout.write(JSON.stringify({run_id:request.job_id,status,...failure(result,status)}));
  }
} catch (error) {
  // An admission timeout is ambiguous. A "submit a new turn" reply means this
  // key can't be admitted again, but it isn't proof the old execution ended.
  // Reconcile that exact run before allowing a fresh key or external work.
  let ended=false;
  if (request.action==='start' && error?.name==='GatewayClientRequestError' && /submit a new turn/i.test(error?.message || '')) {
    try {
      const prior=await callGatewayFromCli('agent.wait',{timeout:'15000'},{runId:request.job_id,timeoutMs:0},scope);
      ended=!!prior?.endedAt && ['ok','error','aborted','timeout'].includes(prior?.status);
      if (!ended) {
        const stopped=await callGatewayFromCli('sessions.abort',{timeout:'15000'},
          {key:session+sessionId,agentId:'main',runId:request.job_id,clearQueued:true},scope);
        ended=stopped?.ok===true && !stopped?.warning && stopped?.status==='no-active-run' && !stopped?.abortedRunId;
        if (!ended && stopped?.ok===true && !stopped?.warning && stopped?.status==='aborted' && stopped?.abortedRunId===request.job_id) {
          const outcome=await callGatewayFromCli('agent.wait',{timeout:'15000'},{runId:request.job_id,timeoutMs:0},scope);
          ended=!!outcome?.endedAt && ['ok','error','aborted','timeout'].includes(outcome?.status);
        }
      }
    } catch {}  // keep the same key/custody when the status check is unavailable
  }
  process.stdout.write(JSON.stringify(ended?{run_id:request.job_id,status:'lost',error:'runtime_lost',error_phase:'runtime'}:{run_id:request.job_id,status:'unavailable'}));
}
