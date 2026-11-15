import assert from 'node:assert/strict';
import {isDeepStrictEqual} from 'node:util';

// The dashboard's calls to its Machine (POST api/action, {action, args}), for the browser tests. The page also calls on
// its own timers (status polls, voice_status, client_error, card_chat), so "the last call" after a click can be one of
// those under load. A test names the call it expects and waits for it to be answered, never for a fixed time or by order
// (page.waitForTimeout: tests/test_fixed_waits.py counts them per file, and the counts only come down).
//
//   const call=await callAfter(page,'security_setting',()=>page.locator('[data-sec="save_logins"]').click());
//   assert.deepEqual(call,{action:'security_setting',args:{key:'save_logins',value:'on'}});
//
// match: an action name, or a function of the call ({action, args}) that says whether it is the one.
const which=match=>typeof match==='function'?match:call=>call.action===match;
const body=request=>{try{return JSON.parse(request.postData()||'null')}catch{return null}};
const isCall=(request,want)=>{if(request.method()!=='POST'||!new URL(request.url()).pathname.endsWith('/api/action'))return false;const b=body(request);return !!b&&want(b)};

// Runs run() and returns the first matching call it led to, once the Machine (the fixture server) has answered it.
export async function callAfter(page,match,run,{timeout=30000}={}){const want=which(match);
 const [response]=await Promise.all([page.waitForResponse(r=>isCall(r.request(),want),{timeout}),run()]);
 return body(response.request())}

// The first call in calls (the list a fixture server keeps of the calls it got, {action, args, ...}) that matches,
// once it is there: waits for it instead of a fixed time, and fails, naming it, when it never comes.
//   const removed=await waitForAction(actions,'chat_file_remove');
export async function waitForAction(calls,match,{timeout=15000}={}){const want=which(match),end=Date.now()+timeout;
 for(;;){const found=calls.find(call=>call&&want(call));if(found)return found;
  if(Date.now()>end)assert.fail(`no ${typeof match==='string'?match+' ':''}call within ${timeout} ms`);
  await new Promise(r=>setTimeout(r,20))}}

// What the page shows once it has caught up: get() again until it deep-equals want (or the time is up, then the usual
// assertion with the last value). For a check right after a call is answered, while the page may still redraw.
export async function settled(get,want,message,{timeout=30000}={}){const end=Date.now()+timeout;let got;
 for(;;){got=await get();if(isDeepStrictEqual(got,want)||Date.now()>end)break;await new Promise(r=>setTimeout(r,50))}
 assert.deepEqual(got,want,message)}
