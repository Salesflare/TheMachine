// What's new (state.whats_new, machine/store/whats_new.py): a small dialog with this morning's pick of features shipped
// since this person got started, at most five, one per view: picture, title, text and the entry's button. Back and Next
// stay in one place, Done on the last; dots, arrow keys and a swipe step too. Closing it any way marks them seen
// (whats_new_seen).
// Lazy (dashboard_parts.LAZY), loaded by shell-tabs.js whatsNewMaybe.
// Pictures ('art'), 440 by 180, no words: c card, f accent tint with accent edge, b text line, s title, m/t accent and
// its tint, e edge in a card, l accent line, k line on the accent, q quiet line. `new` stands in for a missing one.
// Shared shapes: wnR a rounded box, wnC a dot or ring, wnBar a line of text, wnTick a done mark, wnStar a sparkle
// (center, size), wnGo the dashed way from one thing to the next with its arrowhead (g after the dashes)
const wnStar=(x,y,s,c='m')=>`<path class="${c}" d="M${x} ${y-s}l${.3*s} ${.7*s} ${.7*s} ${.3*s}-${.7*s} ${.3*s}-${.3*s} ${.7*s}-${.3*s}-${.7*s}-${.7*s}-${.3*s} ${.7*s}-${.3*s}z"/>`;
const wnGo=(x,y,w,g=4)=>`<path class="l" stroke-dasharray="2 7" d="M${x} ${y}h${w}"/><path class="l" d="M${x+w+g} ${y-7}l7 7-7 7"/>`;
const wnR=(c,x,y,w,h,r)=>`<rect class="${c}" x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}"/>`;
const wnC=(c,x,y,r)=>`<circle class="${c}" cx="${x}" cy="${y}" r="${r}"/>`;
const wnBar=(x,y,w,c='b',h=6)=>wnR(c,x,y,w,h,h/2);
const wnTick=(x,y,r=10)=>`${wnC('m',x,y,r)}<path class="k" d="M${x-4.5} ${y+.5}l3.2 3.2 6-6.6"/>`;
const WN_ART={
 // The desktop app: the dashboard in a window of its own, and the robot beside it with its small box open
 desktop:()=>wnR('c',24,20,254,140,12)
  +[0,1,2].map(i=>wnR(i?'c':'f',40,34+i*38,222,32,8)+wnBar(54,43+i*38,[150,120,170][i],'s')+wnBar(54,53+i*38,100)).join('')
  +wnR('c',292,14,100,74,12)+wnBar(304,30,52,'s')+wnBar(304,46,76)+wnBar(304,62,60)
  +`<path class="l" d="M342 100v12"/>${wnR('m',318,112,48,38,12)}${wnC('t',332,131,5)}${wnC('t',352,131,5)}`,
 // Send later: an approved message (its tick), its wait on the clock, then on its way
 later:()=>wnR('c',40,40,186,100,12)+wnBar(56,58,90,'s')+wnBar(56,80,150)+wnBar(56,94,110)+wnTick(204,118,9)
  +wnGo(236,90,16)+wnC('f',300,90,30)+`<path class="l" d="M300 72v18l12 8"/>`+wnGo(338,90,16)
  +`${wnC('m',392,90,20)}<g class="k" transform="translate(383 81) scale(.75)"><path d="m22 2-7 20-4-9-9-4zM22 2 11 13"/></g>`,
 // A meeting with its guests, and its briefing: what was agreed earlier (ticked) and what's still open (rings)
 meeting:()=>wnR('f',30,40,130,100,12)+wnBar(46,58,80,'s')+wnBar(46,74,56)+['m','c','t'].map((c,i)=>wnC(c,54+i*18,112,8)).join('')+wnGo(170,90,16)
  +wnR('c',210,14,180,152,12)+wnStar(232,35,8)+wnBar(248,32,96,'s',5)
  +[0,1,2].map(i=>{const y=72+i*34;return (i>1?wnC('q',232,y,7):wnTick(232,y,8))+wnBar(250,y-8,[108,86,120][i],'s',5)+wnBar(250,y+2,124)}).join(''),
 // Search with a question in it, its answer with the sparkle, from older mail (the lit one, under older ones)
 mail:()=>wnR('c',40,14,344,40,20)+wnC('q',64,34,6)+`<path class="q" d="M68.5 38.5l5 5"/>`+wnBar(86,31,160,'s')
  +wnR('c',40,72,214,60,12)+wnStar(62,92,7.5)+wnBar(78,88,150)+wnBar(56,108,180)
  +[0,1].map(i=>{const x=284+i*24,y=70+i*22,c=i;return wnR(c?'f':'c',x,y,84,60,8)+`<path class="${c?'l':'e'}" d="M${x+6} ${y+10}l36 22 36-22"/>`}).join(''),
 // A connected AI's chat with The Machine: it starts from the brief (its bookmark), and what the owner settles is kept
 learn:()=>wnR('f',30,56,68,68,16)+wnStar(64,90,16)+wnGo(108,90,16)
  +`${wnR('c',150,14,240,152,12)}${wnR('t',166,30,160,34,10)}<g class="l" transform="translate(174 36) scale(.9)"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></g>`
  +wnBar(200,39,110,'s')+wnBar(200,51,80)+wnR('m',236,82,140,26,12)+wnBar(250,92,100,'t')+wnTick(178,140,8)+wnBar(194,137,150),
 // Routines: three of them, each with its repeat mark, a name and how often; two ran, the third waits for its time
 routines:()=>`${wnR('c',70,18,300,144,12)}<path class="e" d="M70 66h300M70 114h300"/>`+[[112,62],[84,92],[128,54]].map(([a,b],i)=>{const y=18+i*48;
  return `<g class="l" transform="translate(88 ${y+14}) scale(.83)"><path d="m17 2 4 4-4 4M3 11v-1a4 4 0 0 1 4-4h14M7 22l-4-4 4-4M21 13v1a4 4 0 0 1-4 4H3"/></g>`+wnBar(124,y+15,a,'s')+wnBar(124,y+29,b)+(i<2?wnTick(346,y+24):`${wnC('q',346,y+24,9.5)}<path class="q" d="M346 ${y+18}v6.5l4 2.5"/>`)}).join(''),
 // A newer model: the old one faded on the left, the new one lit up with its sparkle, and what it does going out fast
 // (speed lines): a chat's answer, and background work ticked off
 sol:()=>wnR('t',44,60,72,60,14)+wnStar(80,90,13,'q')+wnGo(126,90,20)
  +wnR('f',172,44,92,92,20)+wnStar(218,90,24)+`<path class="l" d="M272 66h12M268 90h18M272 114h12"/>`
  +wnR('c',296,44,96,34,14)+wnBar(310,58,66)+wnR('c',296,102,96,34,12)+wnBar(310,116,44)+wnTick(372,119,8),
 // A project's page: its name, then the description in the accent tint with its sparkle and the mark that it renews
 // itself, and the Timeline's lines under it
 project:()=>`${wnR('c',70,14,300,152,12)}${wnR('m',92,32,28,28,7)}`+wnBar(132,36,140,'s',8)+wnBar(132,51,80)
  +wnR('f',92,74,256,48,9)+wnStar(110,93.8,6.8)+wnBar(126,86,170)+wnBar(126,100,120)
  +`<g class="l" transform="translate(320 86) scale(.8)"><path d="M3 12a9 9 0 0 1 15.4-6.4L21 8M21 3v5h-5M21 12a9 9 0 0 1-15.4 6.4L3 16M3 21v-5h5"/></g>`
  +[136,152].map((y,i)=>wnC('q',98,y+3,3.5)+wnBar(110,y,i?120:170)).join(''),
 // The team's board: three stages of project cards, every one there, the teammates' faces above it
 team:()=>[60,170,280].map((x,i)=>wnR('c',x,46,100,122,10)+wnBar(x+12,58,[44,56,38][i],'s')
  +[0,1,2].slice(0,3-i%2).map(j=>wnR(j===1-i%2?'f':'t',x+10,74+j*31,80,23,6)+wnBar(x+18,82+j*31,[52,40,60][(i+j)%3])).join('')).join('')
  +[0,1,2].map(i=>wnC(i===1?'f':'m',192+i*28,26,11)).join(''),
 // The day's digest under its moon: what got done (ticked) over what is still open (empty rings), a copy button per part
 digest:()=>`${wnR('c',44,14,250,152,12)}<g class="l" transform="translate(262 22) scale(.9)"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></g>`
  +wnBar(62,30,64,'s')+wnTick(72,54,7)+wnBar(88,51,130)+wnTick(72,76,7)+wnBar(88,73,96)+`<path class="e" d="M44 94h250"/>`
  +wnBar(62,108,78,'s')+[130,150].map((y,i)=>wnC('q',72,y,6.5)+wnBar(88,y-3,i?92:140)).join('')
  +[46,108].map(y=>`${wnR('t',306,y,86,30,15)}<g class="l" transform="translate(317 ${y+7}) scale(.67)"><rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2"/></g>`+wnBar(341,y+12,38,'s')).join(''),
 // The team brief's lines as to-dos: who waits, a line on what they asked, what's at stake, the teammates in touch
 brief:()=>[0,1,2].map(i=>{const y=14+i*52;
  return `${wnR('c',50,y,340,44,10)}${wnC(i===1?'f':'m',74,y+22,11)}`+wnBar(96,y+12,[150,120,138][i],'s')+wnBar(96,y+26,[110,140,96][i])
   +(([x,w])=>wnR('t',x,y+10,w,24,12)+wnBar(x+12,y+19,w-24,'m'))([[270,60],[282,48],[262,68]][i])
   +[0,1].map(j=>wnC(j?'t':'f',356+j*14,y+22,8)).join('')}).join(''),
 // A chat as its messenger shows it: the app's mark and the chat's name, a day line, their bubble left, the owner's right
 chats:()=>`${wnR('c',90,10,260,160,12)}${wnC('m',112,30,9)}`+wnBar(128,27,90,'s')+`<path class="e" d="M90 50h260"/>`
  +wnR('t',190,60,60,16,8)+wnBar(204,65,32,'b')
  +`${wnC('f',112,100,9)}${wnR('c',128,84,140,32,14)}`+wnBar(142,97,104)
  +wnR('m',186,126,148,32,14)+wnBar(200,139,96,'t'),
 // A person's page with their address lit up, and the small composer it opens: To, subject, the message and Send
 compose:()=>`${wnR('c',30,38,160,104,12)}${wnC('m',58,66,14)}`+wnBar(80,58,84,'s')+wnBar(80,72,56)
  +`${wnR('t',44,96,132,28,8)}<g class="l" transform="translate(52 101) scale(.75)"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></g>`+wnBar(76,107,88,'m')
  +wnGo(196,90,14,2)
  +wnR('c',230,14,158,152,12)+wnBar(246,30,20,'b')+wnBar(274,30,84,'s')+`<path class="e" d="M230 46h158M230 74h158"/>`+wnBar(246,57,110,'s')
  +wnBar(246,88,126)+wnBar(246,102,112)+wnBar(246,116,84)+`${wnR('m',312,134,62,22,11)}<g class="k" transform="translate(330 137) scale(.66)"><path d="m22 2-7 20-4-9-9-4zM22 2 11 13"/></g>`+wnBar(350,142,14,'t'),
 // The Machine in the middle, with chats, a mailbox and a calendar connected to it, and room for more
 connect:()=>`<path class="l" stroke-dasharray="2 7" d="M118 90h76M246 78l76-36M246 102l76 36"/>`+wnR('f',190,60,60,60,14)+wnStar(220,87.5,13.5)
  +[[62,62,'<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>'],[326,14,'<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>'],[326,110,'<path d="M8 2v4M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>']]
   .map(([x,y,p])=>`${wnR('c',x,y,56,56,12)}<g class="l" transform="translate(${x+14} ${y+14}) scale(1.17)">${p}</g>`).join('')
  +`${wnC('t',90,148,12)}<path class="l" d="M90 142v12M84 148h12"/>`,
 // The chat: the owner says something that stays true, the reply keeps it, and it lands as a kept fact with its bookmark
 memory:()=>wnR('f',174,14,200,44,14)+wnBar(190,26,150)+wnBar(190,40,110)
  +wnR('c',54,70,190,34,14)+wnBar(70,84,110)+wnTick(222,87,8)
  +`${wnR('c',54,118,300,46,10)}${wnR('t',66,128,26,26,7)}<g class="l" transform="translate(70 132) scale(.75)"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></g>`
  +wnBar(104,130,150,'s')+wnBar(104,144,104),
 // A watched page under its eye: one line of it changed (the old one crossed out, the new one in the accent), and that
 // change becomes a to-do
 watch:()=>wnR('c',34,18,216,148,12)+[0,1,2].map(i=>wnC('q',52+i*12,33,3.5)).join('')
  +`<path class="e" d="M34 47h216"/>${wnC('m',232,22,17)}<g class="k" transform="translate(220 10)"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></g>`
  +wnBar(52,60,118,'s',8)+wnBar(52,76,158)+wnR('f',46,90,192,44,8)+wnBar(58,100,96)+`<path class="q" d="M54 103h104"/>`+wnBar(58,116,124,'m')
  +wnBar(52,146,136)+wnGo(258,112,22)
  +`${wnR('c',304,74,118,76,12)}${wnC('m',326,96,9)}`+wnBar(342,92,64,'s',8)+wnBar(318,116,90)+wnBar(318,130,66),
 // Sign-ins coming in: a password manager's key and hidden password, on their way into the saved sign-ins, where the
 // one arriving (lit up) is for the same site as the one there: one marked Work (briefcase), one Personal (house)
 logins:()=>`${wnR('c',40,46,128,88,12)}${wnC('m',70,76,16)}<g class="k" transform="translate(59 65) scale(.9)"><path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4M21 2l-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/></g>`
  +wnBar(96,70,52,'s')+wnBar(96,82,36)+[0,1,2,3,4].map(i=>wnC('b',60+i*12,114,3.5)).join('')
  +wnGo(176,90,16)+wnR('c',214,18,160,148,12)+wnBar(230,32,64,'s')+`<path class="e" d="M214 48h160"/>${wnR('f',222,55,144,34,8)}`
  +[['m',56,'<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>'],['m',42,'<path d="M3 10l9-7 9 7v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1zM9 21v-7h6v7"/>'],['t',36]].map(([c,w,p],i)=>{const y=72+i*38;
   return wnR(c,232,y-10,20,20,6)+wnBar(262,y-8,i<2?66:54,'s')+wnBar(262,y+3,w)+(p?`${wnC('t',350,y,12)}<g class="l" transform="translate(342.2 ${y-7.8}) scale(.65)">${p}</g>`:'')}).join(''),
 new:()=>wnR('c',120,42,200,96,12)+wnStar(152,75.5,13.5)+wnBar(180,68,110,'s')+wnBar(180,84,76)+wnBar(142,108,156)+wnBar(142,122,112)};
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
