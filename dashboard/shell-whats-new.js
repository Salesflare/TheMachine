// What's new (state.whats_new, machine/store/whats_new.py): a small dialog about features shipped since this person
// got started, at most three, one per view: picture, title, text and the entry's button. Back and Next stay in one
// place, Done on the last; dots, arrow keys and a swipe step too. Closing it any way marks all seen (whats_new_seen).
// Lazy (dashboard_parts.LAZY), loaded by shell-tabs.js whatsNewMaybe.
// Pictures ('art'), 440 by 180, no words: c card, f accent tint with accent edge, b text line, s title, m/t accent and
// its tint, e edge in a card, l accent line, k line on the accent, q quiet line. `new` stands in for a missing one.
const wnBar=(x,y,w,c='b',h=6)=>`<rect class="${c}" x="${x}" y="${y}" width="${w}" height="${h}" rx="${h/2}"/>`;
const wnTick=(x,y,r=10)=>`<circle class="m" cx="${x}" cy="${y}" r="${r}"/><path class="k" d="M${x-4.5} ${y+.5}l3.2 3.2 6-6.6"/>`;
const wnFile=(x,y,w,turn=0)=>`<g transform="rotate(${turn} ${x+24} ${y+28})"><path class="c" d="M${x+4} ${y}h28l12 12v40a4 4 0 0 1-4 4h-36a4 4 0 0 1-4-4v-48a4 4 0 0 1 4-4z"/><path class="q" d="M${x+32} ${y}v12h12"/>`+w.map((n,i)=>wnBar(x+8,y+23+i*9,n,'b',4)).join('')+'</g>';
const WN_ART={
 // Routines: three of them, each with its repeat mark, a name and how often; two ran, the third waits for its time
 routines:()=>`<rect class="c" x="70" y="18" width="300" height="144" rx="12"/><path class="e" d="M70 66h300M70 114h300"/>`+[[112,62],[84,92],[128,54]].map(([a,b],i)=>{const y=18+i*48;
  return `<g class="l" transform="translate(88 ${y+14}) scale(.83)"><path d="m17 2 4 4-4 4M3 11v-1a4 4 0 0 1 4-4h14M7 22l-4-4 4-4M21 13v1a4 4 0 0 1-4 4H3"/></g>`+wnBar(124,y+15,a,'s')+wnBar(124,y+29,b)+(i<2?wnTick(346,y+24):`<circle class="q" cx="346" cy="${y+24}" r="9.5"/><path class="q" d="M346 ${y+18}v6.5l4 2.5"/>`)}).join(''),
 // Search: the box with a question in it (its question mark drawn, not written), the answer under it, and the messages it used
 search:()=>`<rect class="c" x="60" y="16" width="320" height="40" rx="20"/><circle class="q" cx="84" cy="35" r="6"/><path class="q" d="M88.5 39.5l5 5"/>`+wnBar(106,33,128,'s')+`<path class="l" stroke-width="2.4" d="M243 30.5a4.5 4.5 0 1 1 6 4.2c-1.1.5-1.5 1.3-1.5 2.5v1"/><circle class="m" cx="247.5" cy="42.5" r="1.6"/><rect class="m" x="260" y="27" width="2" height="18" rx="1"/><rect class="c" x="60" y="66" width="320" height="98" rx="12"/><path class="m" d="M84 77l2.2 5.3 5.3 2.2-5.3 2.2-2.2 5.3-2.2-5.3-5.3-2.2 5.3-2.2z"/>`+wnBar(100,82,236)+wnBar(78,97,284)+wnBar(78,112,176)
  +[[78,82],[168,96],[272,74]].map(([x,w])=>`<rect class="t" x="${x}" y="130" width="${w}" height="22" rx="11"/><path class="l" d="M${x+9} 136.5h12v9h-12zl6 4.5 6-4.5"/>`+wnBar(x+28,138,w-40,'s')).join(''),
 // Export: the Machine's folder with files in it, and its files on their way out of it to a download
 export:()=>`<path class="c" d="M44 46a8 8 0 0 1 8-8h30l10 10h68a8 8 0 0 1 8 8v90a8 8 0 0 1-8 8H52a8 8 0 0 1-8-8z"/>`+wnFile(62,34,[26,20,24],-8)+wnFile(108,30,[22,28,16],6)
  +`<path class="f" d="M44 84h124v62a8 8 0 0 1-8 8H52a8 8 0 0 1-8-8z"/><rect class="m" x="96" y="110" width="20" height="6" rx="3"/>`
  +`<path class="l" stroke-dasharray="2 7" d="M184 97h30"/><path class="l" d="M218 90l7 7-7 7"/>`+wnFile(244,52,[28,22,26],-10)+wnFile(298,40,[22,28,18],4)+wnFile(346,70,[26,20,28],12)
  +`<circle class="m" cx="396" cy="138" r="16"/><path class="k" d="M396 129.5v12m-5-5 5 5 5-5M389.5 146.5h13"/>`,
 new:()=>`<rect class="c" x="120" y="42" width="200" height="96" rx="12"/><path class="m" d="M152 62l4 9.5 9.5 4-9.5 4-4 9.5-4-9.5-9.5-4 9.5-4z"/>`+wnBar(180,68,110,'s')+wnBar(180,84,76)+wnBar(142,108,156)+wnBar(142,122,112)};
let wn={list:[],i:0};
// A tap on the backdrop (the dialog itself is the target there, and on its own padding too)
const wnBeside=(d,e)=>{const r=d.getBoundingClientRect();return e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom};
function whatsNewSeen(){if(!state?.whats_new)return;state.whats_new=null;
 request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'whats_new_seen',args:{}})}).catch(()=>{})}
// An entry's button: a command of the palette by its id (shell-keys.js ACTIONS), or Search itself
function whatsNewRun(run){if(run==='search')return palOpen();const ctx=kbCtx(),a=actsFor(ctx).find(x=>x.id===run);if(a)actRun(a,ctx)}
// One view: its picture, dot and text; Back (not on the first) left, Next right, Done in Next's place on the last
function whatsNewGo(i){const d=$('#whats-new'),n=wn.list.length;if(!(i>=0&&i<n))return;const was=wn.i;wn.i=i;const last=i===n-1,acts=d.querySelector('.wn-acts'),a=document.activeElement,held=acts.contains(a)&&(a.classList.contains('primary')?'.primary':'.ghost');
 d.classList.toggle('wn-back',i<was);void d.offsetWidth;  // the way in is set before the view comes up
 for(const sel of ['.wn-art','.wn-view','.wn-dots button'])d.querySelectorAll(sel).forEach((x,j)=>x.classList.toggle('on',j===i));
 d.querySelectorAll('.wn-dots button').forEach((b,j)=>b.toggleAttribute('aria-current',j===i));
 d.querySelectorAll('.wn-view h2').forEach((h,j)=>{if(j===i)h.id='wn-title';else h.removeAttribute('id')});
 setHTML(acts,html`${i?html`<button type="button" class="ghost" data-wn-go="${i-1}">Back</button>`:''}${last?html`<button type="button" class="primary" data-wn-close>Done</button>`:html`<button type="button" class="primary" data-wn-go="${i+1}">Next</button>`}`);
 if(held)(acts.querySelector(held)||acts.querySelector('.primary')).focus()}  // Enter keeps going
function whatsNewOpen(n){const list=(n?.entries||[]).slice(0,3);if(!list.length||document.querySelector('dialog[open]'))return;
 let d=$('#whats-new');
 if(!d){d=document.createElement('dialog');d.id='whats-new';d.tabIndex=-1;d.setAttribute('aria-labelledby','wn-title');document.body.append(d);
  d.addEventListener('close',whatsNewSeen);
  d.addEventListener('keydown',e=>{const by={ArrowRight:1,ArrowLeft:-1}[e.key];if(by&&!e.altKey&&!e.ctrlKey&&!e.metaKey&&!e.shiftKey){e.preventDefault();whatsNewGo(wn.i+by)}});
  let sw=null;
  d.addEventListener('touchstart',e=>{const t=e.touches[0];sw=e.touches.length===1?{x:t.clientX,y:t.clientY}:null},{passive:true});
  d.addEventListener('touchend',e=>{const t=e.changedTouches[0],dx=t.clientX-sw?.x;if(sw&&Math.abs(dx)>48&&Math.abs(dx)>1.5*Math.abs(t.clientY-sw.y))whatsNewGo(wn.i+(dx<0?1:-1));sw=null},{passive:true});
  d.addEventListener('click',e=>{const b=e.target.closest('[data-wn-run]'),go=e.target.closest('[data-wn-go]');
   if(b){d.close();whatsNewRun(b.dataset.wnRun)}else if(go)whatsNewGo(+go.dataset.wnGo);else if(e.target.closest('[data-wn-close]')||e.target===d&&wnBeside(d,e))d.close()})}
 const many=list.length>1,drawn=list.some(e=>WN_ART[e.art]),art=e=>(WN_ART[e.art]||WN_ART.new)();wn={list,i:0};
 setHTML(d,html`<button type="button" class="wn-x${drawn?' on-art':''}" data-wn-close aria-label="Close" title="Close">×</button>${drawn?html`<div class="wn-arts" aria-hidden="true">${list.map(e=>html`<div class="wn-art"><svg viewBox="0 0 440 180">${raw(art(e))}</svg></div>`)}</div>`:''}${many?html`<div class="wn-dots">${list.map((e,i)=>html`<button type="button" data-wn-go="${i}" aria-label="${e.title}" translate="no"></button>`)}</div>`:''}<div class="wn-views">${list.map(e=>html`<div class="wn-view"><h2 translate="no">${e.title}</h2><p translate="no">${e.text}</p>${e.action?html`<button type="button" class="wn-run" data-wn-run="${e.action.run}" translate="no">${e.action.label}</button>`:''}</div>`)}</div><div class="wn-acts"></div>`);
 whatsNewGo(0);d.showModal();d.focus()}  // no button lit up: Tab reaches them, Esc closes
