// What's new (state.whats_new, machine/store/whats_new.py): a small dialog with this morning's pick of features shipped
// since this person got started, at most five, one per view: picture, title, text and the entry's button. Back and Next
// stay in one place, Done on the last; dots, arrow keys and a swipe step too. Closing it any way marks them seen
// (whats_new_seen).
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
 // A project's page: its name, then the description in the accent tint with its sparkle and the mark that it renews
 // itself, and the Timeline's lines under it
 project:()=>`<rect class="c" x="70" y="14" width="300" height="152" rx="12"/><rect class="m" x="92" y="32" width="28" height="28" rx="7"/>`+wnBar(132,36,140,'s',8)+wnBar(132,51,80)
  +`<rect class="f" x="92" y="74" width="256" height="48" rx="9"/><path class="m" d="M110 87l2 4.8 4.8 2-4.8 2-2 4.8-2-4.8-4.8-2 4.8-2z"/>`+wnBar(126,86,170)+wnBar(126,100,120)
  +`<g class="l" transform="translate(320 86) scale(.8)"><path d="M3 12a9 9 0 0 1 15.4-6.4L21 8M21 3v5h-5M21 12a9 9 0 0 1-15.4 6.4L3 16M3 21v-5h5"/></g>`
  +[136,152].map((y,i)=>`<circle class="q" cx="98" cy="${y+3}" r="3.5"/>`+wnBar(110,y,i?120:170)).join(''),
 // The team's board: three stages of project cards, every one there, the teammates' faces above it
 team:()=>[60,170,280].map((x,i)=>`<rect class="c" x="${x}" y="46" width="100" height="122" rx="10"/>`+wnBar(x+12,58,[44,56,38][i],'s')
  +[0,1,2].slice(0,3-i%2).map(j=>`<rect class="${j===1-i%2?'f':'t'}" x="${x+10}" y="${74+j*31}" width="80" height="23" rx="6"/>`+wnBar(x+18,82+j*31,[52,40,60][(i+j)%3])).join('')).join('')
  +[0,1,2].map(i=>`<circle class="${i===1?'f':'m'}" cx="${192+i*28}" cy="26" r="11"/>`).join(''),
 // The day's digest under its moon: what got done (ticked) over what is still open (empty rings), a copy button per part
 digest:()=>`<rect class="c" x="44" y="14" width="250" height="152" rx="12"/><g class="l" transform="translate(262 22) scale(.9)"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></g>`
  +wnBar(62,30,64,'s')+wnTick(72,54,7)+wnBar(88,51,130)+wnTick(72,76,7)+wnBar(88,73,96)+`<path class="e" d="M44 94h250"/>`
  +wnBar(62,108,78,'s')+[130,150].map((y,i)=>`<circle class="q" cx="72" cy="${y}" r="6.5"/>`+wnBar(88,y-3,i?92:140)).join('')
  +[46,108].map(y=>`<rect class="t" x="306" y="${y}" width="86" height="30" rx="15"/><g class="l" transform="translate(317 ${y+7}) scale(.67)"><rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2"/></g>`+wnBar(341,y+12,38,'s')).join(''),
 // The team brief's lines as to-dos: who waits, a line on what they asked, what's at stake, the teammates in touch
 brief:()=>[0,1,2].map(i=>{const y=14+i*52;
  return `<rect class="c" x="50" y="${y}" width="340" height="44" rx="10"/><circle class="${i===1?'f':'m'}" cx="74" cy="${y+22}" r="11"/>`+wnBar(96,y+12,[150,120,138][i],'s')+wnBar(96,y+26,[110,140,96][i])
   +(([x,w])=>`<rect class="t" x="${x}" y="${y+10}" width="${w}" height="24" rx="12"/>`+wnBar(x+12,y+19,w-24,'m'))([[270,60],[282,48],[262,68]][i])
   +[0,1].map(j=>`<circle class="${j?'t':'f'}" cx="${356+j*14}" cy="${y+22}" r="8"/>`).join('')}).join(''),
 // A chat as its messenger shows it: the app's mark and the chat's name, a day line, their bubble left, the owner's right
 chats:()=>`<rect class="c" x="90" y="10" width="260" height="160" rx="12"/><circle class="m" cx="112" cy="30" r="9"/>`+wnBar(128,27,90,'s')+`<path class="e" d="M90 50h260"/>`
  +`<rect class="t" x="190" y="60" width="60" height="16" rx="8"/>`+wnBar(204,65,32,'b')
  +`<circle class="f" cx="112" cy="100" r="9"/><rect class="c" x="128" y="84" width="140" height="32" rx="14"/>`+wnBar(142,97,104)
  +`<rect class="m" x="186" y="126" width="148" height="32" rx="14"/>`+wnBar(200,139,96,'t'),
 // A person's page with their address lit up, and the small composer it opens: To, subject, the message and Send
 compose:()=>`<rect class="c" x="30" y="38" width="160" height="104" rx="12"/><circle class="m" cx="58" cy="66" r="14"/>`+wnBar(80,58,84,'s')+wnBar(80,72,56)
  +`<rect class="t" x="44" y="96" width="132" height="28" rx="8"/><g class="l" transform="translate(52 101) scale(.75)"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></g>`+wnBar(76,107,88,'m')
  +`<path class="l" stroke-dasharray="2 7" d="M196 90h14"/><path class="l" d="M212 83l7 7-7 7"/>`
  +`<rect class="c" x="230" y="14" width="158" height="152" rx="12"/>`+wnBar(246,30,20,'b')+wnBar(274,30,84,'s')+`<path class="e" d="M230 46h158M230 74h158"/>`+wnBar(246,57,110,'s')
  +wnBar(246,88,126)+wnBar(246,102,112)+wnBar(246,116,84)+`<rect class="m" x="312" y="134" width="62" height="22" rx="11"/><g class="k" transform="translate(330 137) scale(.66)"><path d="m22 2-7 20-4-9-9-4zM22 2 11 13"/></g>`+wnBar(350,142,14,'t'),
 // The Machine in the middle, with chats, a mailbox and a calendar connected to it, and room for more
 connect:()=>`<path class="l" stroke-dasharray="2 7" d="M118 90h76M246 78l76-36M246 102l76 36"/><rect class="f" x="190" y="60" width="60" height="60" rx="14"/><path class="m" d="M220 74l4 9.5 9.5 4-9.5 4-4 9.5-4-9.5-9.5-4 9.5-4z"/>`
  +[[62,62,'<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>'],[326,14,'<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>'],[326,110,'<path d="M8 2v4M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>']]
   .map(([x,y,p])=>`<rect class="c" x="${x}" y="${y}" width="56" height="56" rx="12"/><g class="l" transform="translate(${x+14} ${y+14}) scale(1.17)">${p}</g>`).join('')
  +`<circle class="t" cx="90" cy="148" r="12"/><path class="l" d="M90 142v12M84 148h12"/>`,
 // The chat: the owner says something that stays true, the reply keeps it, and it lands as a kept fact with its bookmark
 memory:()=>`<rect class="f" x="174" y="14" width="200" height="44" rx="14"/>`+wnBar(190,26,150)+wnBar(190,40,110)
  +`<rect class="c" x="54" y="70" width="190" height="34" rx="14"/>`+wnBar(70,84,110)+wnTick(222,87,8)
  +`<rect class="c" x="54" y="118" width="300" height="46" rx="10"/><rect class="t" x="66" y="128" width="26" height="26" rx="7"/><g class="l" transform="translate(70 132) scale(.75)"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></g>`
  +wnBar(104,130,150,'s')+wnBar(104,144,104),
 // A watched page under its eye: one line of it changed (the old one crossed out, the new one in the accent), and that
 // change becomes a to-do
 watch:()=>`<rect class="c" x="34" y="18" width="216" height="148" rx="12"/>`+[0,1,2].map(i=>`<circle class="q" cx="${52+i*12}" cy="33" r="3.5"/>`).join('')
  +`<path class="e" d="M34 47h216"/><circle class="m" cx="232" cy="22" r="17"/><g class="k" transform="translate(220 10)"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></g>`
  +wnBar(52,60,118,'s',8)+wnBar(52,76,158)+`<rect class="f" x="46" y="90" width="192" height="44" rx="8"/>`+wnBar(58,100,96)+`<path class="q" d="M54 103h104"/>`+wnBar(58,116,124,'m')
  +wnBar(52,146,136)+`<path class="l" stroke-dasharray="2 7" d="M258 112h22"/><path class="l" d="M284 105l7 7-7 7"/>`
  +`<rect class="c" x="304" y="74" width="118" height="76" rx="12"/><circle class="m" cx="326" cy="96" r="9"/>`+wnBar(342,92,64,'s',8)+wnBar(318,116,90)+wnBar(318,130,66),
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
function whatsNewOpen(n){const list=(n?.entries||[]).slice(0,5);if(!list.length||document.querySelector('dialog[open]'))return;
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
