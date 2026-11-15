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

// The page's requests in flight, for quiet(): call it when the page is made, before it loads anything. quiet(page)
// then counts them by itself.
const TRACKED=new WeakMap();
export function trackRequests(page){let open=0;const done=()=>{open=Math.max(0,open-1)};
 page.on('request',()=>{open++});page.on('requestfinished',done);page.on('requestfailed',done);const count=()=>open;TRACKED.set(page,count);return count}

// The page has settled: no request in flight (from trackRequests), and for `frames` animation frames in a
// row no change to the page, no scroll and no animation running (an endless one, a spinner, doesn't count). For a check that
// measures where things are after something happened (nothing jumped, nothing shifted).
export async function quiet(page,requests=TRACKED.get(page)||(()=>0),{frames=8,timeout=15000}={}){const end=Date.now()+timeout;
 const still=n=>new Promise(done=>{let changed=false,left=n;const mark=()=>{changed=true},watch=new MutationObserver(mark);
  watch.observe(document,{subtree:true,childList:true,attributes:true,characterData:true});document.addEventListener('scroll',mark,{capture:true});
  const stop=()=>{watch.disconnect();document.removeEventListener('scroll',mark,{capture:true})};
  const moving=()=>document.getAnimations().some(a=>a.playState==='running'&&a.effect?.getComputedTiming().iterations!==Infinity);
  const frame=()=>{if(changed||moving()){stop();return done(false)}if(--left<=0){stop();return done(true)}requestAnimationFrame(frame)};
  requestAnimationFrame(frame)});
 for(;;){if(!requests()&&await page.evaluate(still,frames)&&!requests())return;
  if(Date.now()>end)assert.fail(`the page kept changing for ${timeout} ms`);
  await new Promise(r=>setTimeout(r,20))}}

// What the page shows once it has caught up: get() again until it deep-equals want (or the time is up, then the usual
// assertion with the last value). For a check right after a call is answered, while the page may still redraw.
export async function settled(get,want,message,{timeout=30000}={}){const end=Date.now()+timeout;let got;
 for(;;){got=await get();if(isDeepStrictEqual(got,want)||Date.now()>end)break;await new Promise(r=>setTimeout(r,50))}
 assert.deepEqual(got,want,message)}
