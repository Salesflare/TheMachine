import assert from 'node:assert/strict';
import {isDeepStrictEqual} from 'node:util';

// The dashboard's calls to its Machine (POST api/action, {action, args}), for the browser tests. The page also calls on
// its own timers (status polls, voice_status, client_error, card_chat), so "the last call" after a click can be one of
// those under load. A test names the call it expects and waits for it to be answered, never for a fixed time or by order.
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

// What the page shows once it has caught up: get() again until it deep-equals want (or the time is up, then the usual
// assertion with the last value). For a check right after a call is answered, while the page may still redraw.
export async function settled(get,want,message,{timeout=30000}={}){const end=Date.now()+timeout;let got;
 for(;;){got=await get();if(isDeepStrictEqual(got,want)||Date.now()>end)break;await new Promise(r=>setTimeout(r,50))}
 assert.deepEqual(got,want,message)}
