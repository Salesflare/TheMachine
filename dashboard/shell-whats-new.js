// What's new (state.whats_new, machine/store/whats_new.py): one small dialog when a bigger feature or improvement
// shipped since this person got started. One entry: its title, its text, Close and a button that opens it. Several:
// one short list, newest first, each with a quiet link that opens it. Close, Esc, a tap beside it and the buttons
// all close it, and closing marks everything in it as seen on the Machine (whats_new_seen), so it is gone on every
// device. A lazy part (dashboard_parts.LAZY): shell-tabs.js whatsNewMaybe loads it only when there is something to tell.
function whatsNewSeen(){if(!state?.whats_new)return;state.whats_new=null;
 request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'whats_new_seen',args:{}})}).catch(()=>{})}
// An entry's button: a command of the palette by its id (shell-keys.js ACTIONS), or Search itself
function whatsNewRun(run){if(run==='search')return palOpen();const ctx=kbCtx(),a=actsFor(ctx).find(x=>x.id===run);if(a)actRun(a,ctx)}
function whatsNewOpen(n){const list=n?.entries||[];if(!list.length||document.querySelector('dialog[open]'))return;
 let d=$('#whats-new');
 if(!d){d=document.createElement('dialog');d.id='whats-new';d.tabIndex=-1;d.setAttribute('aria-labelledby','wn-title');document.body.append(d);
  d.addEventListener('close',whatsNewSeen);
  d.addEventListener('click',e=>{const b=e.target.closest('[data-wn-run]');if(b){d.close();whatsNewRun(b.dataset.wnRun)}else if(e.target===d||e.target.closest('[data-wn-close]'))d.close()})}
 const one=list.length===1?list[0]:null;
 setHTML(d,one?html`<h2 id="wn-title" translate="no">${one.title}</h2><p translate="no">${one.text}</p><div class="wn-acts"><button type="button" class="ghost" data-wn-close>Close</button>${one.action?html`<button type="button" class="primary" data-wn-run="${one.action.run}" translate="no">${one.action.label}</button>`:''}</div>`
  :html`<h2 id="wn-title">What’s new</h2><ul class="wn-list">${list.map(e=>html`<li><b translate="no">${e.title}</b><p translate="no">${e.text}</p>${e.action?html`<button type="button" class="wn-open" data-wn-run="${e.action.run}" translate="no">${e.action.label}</button>`:''}</li>`)}</ul><div class="wn-acts"><button type="button" class="primary" data-wn-close>Close</button></div>`);
 d.showModal();d.focus()}  // no button lit up: Tab reaches them, Esc closes
