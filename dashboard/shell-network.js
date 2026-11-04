// A lost connection, a cut-off or garbled answer or a server hiccup (5xx) is "offline": quiet, retried. Only a clear refusal
// (a 4xx with its reason) is said out loud.
const offline=e=>Object.assign(Error('Can’t reach your Machine right now. Try again in a moment.'),{offline:true,cause:e});
// A page opened from the app's on-device copy (sw.js) has no CSRF token of its own: a change waits for api/session,
// which brings it (sessionCheck).
let csrfLive=csrf,csrfSet=null;const csrfReady=csrf?Promise.resolve():new Promise(r=>csrfSet=r);
const sessionGone=()=>Object.assign(Error('Signed out. Sign in again to see your Machine.'),{sessionGone:true});
async function request(path,options){let r;
 if(options?.headers&&'X-CSRF-Token' in options.headers&&!options.headers['X-CSRF-Token']){if(!csrfLive&&navigator.onLine===false)throw offline();
  // The Machine away: wait a little for api/session, then say offline (a change that may wait then waits, decideOrWait)
  await(netDown?Promise.race([csrfReady,new Promise((ok,no)=>setTimeout(()=>no(offline()),8000))]):csrfReady);options={...options,headers:{...options.headers,'X-CSRF-Token':csrfLive}}}
 // A timeout (a signal's, or a fetch that hung 30 s and more while the device is online) goes to the error reports (errApi)
 const t0=Date.now();try{r=await fetch(path,options)}catch(e){if(e?.name==='TimeoutError'||e?.name!=='AbortError'&&navigator.onLine!==false&&Date.now()-t0>=30000)errApi(path,options,'timeout');throw offline(e)}
 // The sign-in gate in front of a hosted Machine answers with a redirect to its sign-in page (seen with redirect:'manual')
 if(r.type==='opaqueredirect')throw sessionGone();
 // Only a JSON answer is read; an empty or HTML 502 while the service restarts, a cut-off body or any 5xx is "offline"
 const json=/json/i.test(r.headers.get('content-type')||'');let d=null;if(json)try{d=await r.json()}catch(e){if(r.ok||r.status>=500)throw offline(e)}
 // A 5xx the Machine answered itself (JSON) is a failed call for the error reports, and a gateway timeout (504) a timeout;
 // an HTML 502 or 503 is the Machine away or restarting, as is an answer that says so
 if(r.status>=500&&!d?.restarting&&(json||r.status===504))errApi(path,options,json?r.status:'timeout')
 if(r.status>=500||r.ok&&!json){const wait=+r.headers.get('retry-after');if(d?.restarting)netSetup=!!d.setting_up||setupUnderway();throw Object.assign(offline(d?.error),{restarting:!!d?.restarting,retryAfter:wait>0?Math.min(wait,60)*1000:0})}
 if(!r.ok)throw Object.assign(Error(d?.error||'Request failed'),{status:r.status});return d}
let retryIn=0,retryTimer=null;
// On the device: the last cards, the open card's chat and the Graph's lists, so the app opens with them at once and
// then refreshes. Sensitive, so: encrypted at rest (AES-GCM, a non-extractable key that stays in this browser's
// IndexedDB), only for the owner the page was served for (CACHE_SCOPE, from the server), at most 7 days old and a few MB,
// never a token (scrubbed), and wiped on Sign out, on another owner and when the server says the session is gone.
// Not in a frame (the site's demo). docs/architecture.md, "On the device".
const CACHE_SCOPE='__CACHE_SCOPE__';
const localCache=(()=>{const DB='tm-cache',MAX_AGE=7*864e5,MAX_BYTES=8e6,MAX_ITEM=3e6;let framed=true;try{framed=window.top!==window}catch{}
 const on=/^[a-f0-9]{32}$/.test(CACHE_SCOPE)&&!framed&&isSecureContext&&!!window.indexedDB&&!!window.crypto?.subtle;
 const req=r=>new Promise((ok,no)=>{r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)});
 const store=(db,name,mode='readonly')=>db.transaction(name,mode).objectStore(name);
 const aad=name=>new TextEncoder().encode(CACHE_SCOPE+'\n'+name);  // a copy only opens under its own name and owner
 const SECRET=/^(csrf|token|secret|password|passcode|api_?key|private_?key|cookie|authorization)$|_(token|secret|password|key)$/i;
 const scrub=v=>Array.isArray(v)?v.map(scrub):v&&typeof v==='object'?Object.fromEntries(Object.entries(v).filter(([k])=>!SECRET.test(k)).map(([k,x])=>[k,scrub(x)])):v;
 let opened=null,db=null,last=0,blocked=false;const writes=new Map(),durable=name=>['outbox','chat-drafts'].includes(name);
 const open=()=>opened||(opened=(async()=>{db=await new Promise((ok,no)=>{const r=indexedDB.open(DB,1);r.onupgradeneeded=()=>{r.result.createObjectStore('meta');r.result.createObjectStore('data')};r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error);r.onblocked=()=>no(Error('blocked'))});
  db.onversionchange=()=>{db.close();db=null;opened=null};
  let meta=await req(store(db,'meta').get('key'));
  if(!meta||meta.scope!==CACHE_SCOPE||!(meta.key instanceof CryptoKey)){  // another owner, or nothing yet: start over
   await req(store(db,'data','readwrite').clear());meta={scope:CACHE_SCOPE,key:await crypto.subtle.generateKey({name:'AES-GCM',length:256},false,['encrypt','decrypt'])};await req(store(db,'meta','readwrite').put(meta,'key'))}
  return meta.key})().catch(e=>{opened=null;throw e}));
 async function trim(){const rows=[];await new Promise(ok=>{const c=store(db,'data').openCursor();c.onsuccess=()=>{const x=c.result;if(!x)return ok();rows.push([x.key,x.value.at,x.value.ct.byteLength]);x.continue()};c.onerror=ok});
  rows.sort((a,b)=>b[1]-a[1]);let total=0;const out=store(db,'data','readwrite');for(const [k,at,size] of rows){total+=size;if(!durable(k)&&(total>MAX_BYTES||Date.now()-at>MAX_AGE))out.delete(k)}}
 // Snapshot at the call, serialize writes per name, and acknowledge the transaction's commit, not just its request.
 function put(name,value){if(!on||blocked)return Promise.resolve(false);let text;
  try{text=JSON.stringify(scrub(value));if(text.length>MAX_ITEM)return Promise.resolve(false)}catch{return Promise.resolve(false)}
  const writing=(writes.get(name)||Promise.resolve()).then(async()=>{if(blocked)return false;const key=await open();if(blocked)return false;
   const iv=crypto.getRandomValues(new Uint8Array(12)),ct=await crypto.subtle.encrypt({name:'AES-GCM',iv,additionalData:aad(name)},key,new TextEncoder().encode(text));
   if(blocked)return false;await new Promise((ok,no)=>{const tx=db.transaction('data','readwrite');tx.oncomplete=ok;tx.onerror=tx.onabort=()=>no(tx.error);tx.objectStore('data').put({iv,ct,at:Date.now()},name)});
   if(Date.now()-last>6e4){last=Date.now();await trim()}return true}).catch(()=>false);
  writes.set(name,writing);writing.finally(()=>{if(writes.get(name)===writing)writes.delete(name)});return writing}
 async function read(name){if(!on||blocked)return null;try{await writes.get(name);if(blocked)return null;const key=await open(),row=await req(store(db,'data').get(name));if(!row)return null;
  if(!durable(name)&&(Date.now()-row.at>MAX_AGE||row.at>Date.now()+6e5)){store(db,'data','readwrite').delete(name);return null}
  return {value:JSON.parse(new TextDecoder().decode(await crypto.subtle.decrypt({name:'AES-GCM',iv:row.iv,additionalData:aad(name)},key,row.ct))),at:row.at}}catch{return null}}
 // Everything this device kept: the data, its key, the skeleton's count and the service worker's copy of the page.
 async function wipe(){blocked=true;await Promise.allSettled([...writes.values()]);try{await opened}catch{}opened=null;try{db?.close()}catch{}db=null;
  try{localStorage.removeItem('skeleton-cards')}catch{}
  await Promise.all([new Promise(ok=>{try{const r=indexedDB.deleteDatabase(DB);r.onsuccess=r.onerror=r.onblocked=()=>ok()}catch{ok()}}),
   (async()=>{try{for(const k of await caches.keys())if(k.startsWith('tm-'))await caches.delete(k)}catch{}})()])}
 return {on,put,read,wipe}})();
// A screen's last data: on the first look this page, what the device kept (at once) while the live answer loads, then
// `fresh` once it is in; later, live first and the kept copy only while the Machine can't be reached.
const liveSeen=new Set(),liveNext=new Map();
async function cachedGet(path,fresh){if(!localCache.on)return request(path);
 if(liveNext.has(path)){const v=liveNext.get(path);liveNext.delete(path);return v}
 if(!liveSeen.has(path)){liveSeen.add(path);const hit=await localCache.read('get:'+path);
  if(hit){request(path).then(v=>{localCache.put('get:'+path,v);if(JSON.stringify(v)===JSON.stringify(hit.value))return;liveNext.set(path,v);fresh?.()},e=>{if(e.offline)staleMark(hit.at)});return hit.value}}
 try{const v=await request(path);localCache.put('get:'+path,v);return v}
 catch(e){if(e.offline){const hit=await localCache.read('get:'+path);if(hit){staleMark(hit.at);return hit.value}}throw e}}
const hhmm=t=>fmtHM(t);
// What the screen shows is older than now: "Offline · updated 10:42", quietly at the foot of the sidebar
let staleAt=0;function staleMark(at){staleAt=at;staleLine(t('Offline · updated {}',hhmm(at)))}
// On a phone the sidebar's line is in the drawer, so the same words show quietly over the cards there too
function staleLine(text){$('#live').classList.add('stale');$('#updated').textContent=text;const n=$('#stale-note');n.textContent=text;n.hidden=false;if(typeof netPaint==='function')netPaint()}
let shownAt=0,shownCached=false;  // when the cards on screen were read, and whether they came from the device
// Offline or on a spotty link (a train, a plane): the owner keeps working. The banner says what is going on, the owner's
// own decisions on a to-do wait on the device and go by themselves, in order, once the Machine answers again, and a
// typed chat message is never lost. docs/architecture.md, "On the device".
// What may wait: Snooze, Not needed, Mark done, Reopen and a note or chat message to The Machine. Each carries its
// decision_id, so a change sent twice (the answer lost on the way back) is saved once. Never a send to other people:
// Send needs the Machine to answer while the owner looks, and says it is offline instead. Waiting changes are kept with
// the rest of the device's copy (encrypted, wiped with it), each shown on its to-do with Cancel until it goes.
const OUTBOX_CHOICES=['snooze','reject','complete','reopen','undo','other'];
const outbox={items:[],busy:null,timer:null,wait:0};
let netDown=false,netRestarting=false,netSetup=false;
// A restart during a new owner's setup (the Machine says so, setting_up, or the page sees it: an AI connecting, the
// first look waiting or running) says "Setting up…", not that the Machine is restarting or offline
const setupUnderway=()=>{const live=state?.review_live||{};return !!(live.ai_connecting||live.first_look||(live.runs||[]).some(r=>r.auto&&r.preview))};
const decidePost=(sid,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'decide',args:{suggestion_id:sid,...args}})});
const outboxLoaded=localCache.read('outbox').then(hit=>{const kept=Array.isArray(hit?.value)?hit.value.filter(x=>x&&x.id&&x.sid&&Array.isArray(x.steps)&&x.steps.length):[];
 for(const x of kept)if(!outbox.items.some(y=>y.id===x.id))outbox.items.push({...x,sending:false});if(kept.length){netPaint();outboxFlush()}}).catch(()=>{});
async function outboxSave(){const saved=await localCache.put('outbox',outbox.items.map(({sending,...x})=>x));netPaint();if(state?.suggestions)focusKept(render);return saved}
// A decision on a to-do: sent now, or, when the Machine can't be reached, kept to go later (true). Anything else
// (a clear refusal) is thrown as before. Behind changes already waiting it waits too, so the order stays the owner's.
async function decideOrWait(sid,steps,kind){await outboxLoaded;steps=steps.map(a=>({...a,decision_id:a.decision_id||crypto.randomUUID()}));
 const queue=async rest=>{outbox.items.push({id:crypto.randomUUID(),sid,kind,steps:rest,text:kind==='other'?rest.at(-1).feedback:'',at:Date.now()});const persistent=await outboxSave();if(!persistent)toast(t('Keep this page open. This device couldn’t save your waiting changes.'),true);outboxRetry();return {waiting:true,persistent}};
 if(outbox.items.length||navigator.onLine===false||netDown&&!csrfLive)return queue(steps);
 let r;for(let n=0;n<steps.length;n++){try{r=await decidePost(sid,steps[n])}catch(e){if(e.offline){netSet(true,e.restarting);return queue(steps.slice(n))}throw e}}return r}
const outboxWaits=sid=>outbox.items.filter(x=>x.sid===sid);
// Send the waiting changes, oldest first. Offline again: try later, a little later each time (2 s up to a minute, with
// some jitter so many devices don't come back at once). A change the Machine refuses (the to-do is gone) is dropped and said.
function outboxRetry(){clearTimeout(outbox.timer);if(!outbox.items.length)return;outbox.wait=Math.min(6e4,(outbox.wait||1e3)*2);outbox.timer=setTimeout(outboxFlush,outbox.wait*(.8+Math.random()*.4))}
function outboxFlush(){return outbox.busy||(outbox.busy=(async()=>{await outboxLoaded;let saved=0;clearTimeout(outbox.timer);
 try{while(outbox.items.length){const it=outbox.items[0];let accepted=true;it.sending=true;netPaint();
   try{while(it.steps.length){await decidePost(it.sid,it.steps[0]);it.steps.shift();if(it.steps.length)await outboxSave()}}
   catch(e){errCaught(e);it.sending=false;if(e.offline){netSet(true,e.restarting);outboxRetry();return}
    if(e.sessionGone||e.status===401||e.status===403){netPaint();return}
    accepted=false;if(it.kind==='other'&&it.text)chatDraftReturn(it.sid,it.text);toast(t('A waiting change couldn’t be saved: {}',e.message),true)}
   if(outbox.items[0]===it)outbox.items.shift();if(accepted)saved++;await outboxSave()}
  outbox.wait=0}
 finally{outbox.busy=null;netPaint();if(saved){toast(t('Back online. Your waiting changes are saved.'));refresh().catch(()=>{});if(chatId)chatPoll()}}})())}
function outboxCancel(id){const i=outbox.items.findIndex(x=>x.id===id);if(i<0||outbox.items[i].sending)return false;const [it]=outbox.items.splice(i,1);outboxSave();
 // A chat message that didn't go comes back into the box, so nothing typed is lost
 if(it.kind==='other'&&it.text)chatDraftReturn(it.sid,it.text);
 return true}
const OUTBOX_LINE={snooze:'Snooze saves when you’re back online.',reject:'Not needed saves when you’re back online.',complete:'Done saves when you’re back online.',
 reopen:'Reopen saves when you’re back online.',undo:'Reopen saves when you’re back online.',other:'Your note sends when you’re back online.'};
const outboxNote=x=>t(OUTBOX_LINE[x.kind]||OUTBOX_LINE.other);
// On the to-do: what waits, and Cancel while it hasn't gone yet
// (its last word and Cancel never part, so Cancel never sits alone on a phone's line)
const outboxLine=s=>outboxWaits(s.id).filter(x=>x.kind!=='other'||chatId!==s.id).map(x=>{const text=x.sending?t('Saving…'):outboxNote(x),cut=text.lastIndexOf(' ')+1;
 return html`<p class="note outbox-wait" data-outbox="${x.id}"><span>${text.slice(0,cut)}<span class="nowrap">${text.slice(cut)}${x.sending?'':html`<button type="button" class="link" data-outbox-cancel="${x.id}">${t('Cancel')}</button>`}</span></span></p>`});
// In the chat: a message that waits shows as sent by the owner, marked, with Cancel (which puts it back in the box)
const outboxChat=s=>outboxWaits(s.id).filter(x=>x.kind==='other').map(x=>html`<div class="chat-msg you outbox-msg" data-outbox="${x.id}"><div class="bubble" translate="no">${chatMarkdown(x.text)}</div><small class="chat-noted outbox-note">${x.sending?t('Sending…'):t('Sends when you’re back online')}${x.sending?'':html` · <button type="button" class="link" data-outbox-cancel="${x.id}">${t('Cancel')}</button>`}</small></div>`);
document.addEventListener('click',e=>{const b=e.target.closest?.('[data-outbox-cancel]');if(!b)return;e.preventDefault();e.stopPropagation();
 if(outboxCancel(b.dataset.outboxCancel))toast(t('Canceled.'));if(chatId)paintChat()},true);
// The banner over every view: offline (or the Machine restarting), since when the screen is from, and what waits.
function netSet(down,restarting=false){const was=netDown;netDown=!!down;netRestarting=!!down&&!!restarting;if(down)liveLine();if(!down&&was&&outbox.items.length){outbox.wait=0;outboxFlush()}if(!down&&was)micResume();netPaint()}
// The sidebar's line (and the phone's) says the same while offline: "Offline · updated 10:42", with the bar's dot
function liveLine(){if(netRestarting){staleLine(netSetup?t('Setting up…'):t('Restarting · retrying'));return}const at=shownAt||staleAt;staleLine(at?t('Offline · updated {}',hhmm(at)):t('Offline.'))}
const netShown=()=>netDown||outbox.items.length>0;
function netText(){const n=outbox.items.length;
 const head=!netDown?'':netRestarting?(netSetup?t('Setting up…'):t('Your Machine is restarting.')):shownAt||staleAt?t('Offline. Showing what was here at {}.',hhmm(shownAt||staleAt)):t('Offline.');
 const waits=n?t(['{} change waits to send.','{} changes wait to send.'],n):'';
 return [head,waits].filter(Boolean).join(' ')}
const netHtml=()=>html`<span class="offline-text">${netText()}</span><button type="button" class="link" data-net-retry>${t('Try now')}</button>`;  // the chat's first draw
const netNodes=()=>[make('span',{class:'offline-text'},netText()),make('button',{type:'button',class:'link','data-net-retry':''},t('Try now'))];
// The same bar sits in an open chat too (#chat-offline, above the message box): the chat covers the page's own
function netPaint(){const show=netShown(),html=show?netText()+'|'+t('Try now'):'';$('#stale-note')?.classList.toggle('covered',show);
 for(const bar of [$('#offline-bar'),$('#chat-offline')]){if(!bar)continue;bar.hidden=!show;if(show)putOnce(bar,html,netNodes)}}
document.addEventListener('click',e=>{if(!e.target.closest?.('#offline-bar [data-net-retry],#chat-offline [data-net-retry]'))return;outbox.wait=0;if(outbox.items.length)outboxFlush();micResume();retryIn=0;refreshWhenReady()});
addEventListener('offline',()=>netSet(true));
addEventListener('online',()=>{outbox.wait=0;outboxFlush()});
