// The command palette (Ctrl/⌘K, /) and the shortcut sheet (?). A lazy part (dashboard_parts.LAZY 'palette'):
// shell-keys.js opens them through palOpen() and keysOpen(), and keeps the registry, the keys and Search's placeholder.
// Fuzzy match: the whole query in the label (at the start best, then at a word), else every word in order as letters.
function palScore(q,text){q=q.trim().toLowerCase();const t=String(text||'').toLowerCase();if(!q)return 1;if(!t)return -1;
 const at=t.indexOf(q);if(at===0)return 100-t.length/1000;if(at>0)return(/[\s\-:·/(]/.test(t[at-1])?85:70)-at/1000;
 let total=0;for(const w of q.split(/\s+/)){const i=t.indexOf(w);if(i>=0){total+=i===0||/[\s\-:·/(]/.test(t[i-1])?50:40;continue}
  let j=0,prev=-2,s=0;for(const ch of w){const k=t.indexOf(ch,j);if(k<0)return -1;s+=k===prev+1?3:k===0||/[\s\-:·/(]/.test(t[k-1])?2:.5;prev=k;j=k+1}total+=Math.min(35,s/(w.length*3)*35)}
 return total/q.split(/\s+/).length}
// A to-do by its title or who its messages went to (Northfield, Dana, dana@…), open, later and done alike; its line says where
// it is when that's not the main list (Later, Waiting on others, Done 5 minutes ago)
const palCardScore=(q,s)=>Math.max(palScore(q,s.title),cardWho(s)?palScore(q,cardWho(s))-5:-1);
const palCardSub=s=>[closed(s)?t(s.status==='completed'&&!lapsed(s)?'Done {}':'Marked not needed {}',ago(closedAt(s))):s.status==='snoozed'?t('Later'):waitsOnOthers(s)?t('Waiting on others'):looksDone(s)?t('Looks done'):'',s.scope==='work'?t('Work'):s.scope==='personal'?t('Personal'):''].filter(Boolean).join(' · ');
// Keywords count for whole words only ("mode" finds the theme); letters in order only on the label itself.
const palMatch=(q,a,label)=>{const l=palScore(q,label),w=q.trim().toLowerCase(),k=a.keywords&&w.split(/\s+/).every(x=>a.keywords.toLowerCase().includes(x))?palScore(q,a.keywords)*.6:-1;return Math.max(l,k)};
// Recent commands, newest first (this browser only).
const PAL_RECENT='palette-recent';
const palRecent=()=>{try{const v=JSON.parse(localStorage.getItem(PAL_RECENT)||'[]');return Array.isArray(v)?v.filter(x=>typeof x==='string').slice(0,5):[]}catch{return []}};
function palRemember(id){try{localStorage.setItem(PAL_RECENT,JSON.stringify([id,...palRecent().filter(x=>x!==id)].slice(0,5)))}catch{}}
function palDialog(){let d=$('#palette');if(d)return d;d=document.createElement('dialog');d.id='palette';d.setAttribute('aria-label','Search and commands');
 d.innerHTML=`<div class="pal-field"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4 4"/></svg><input id="pal-q" type="text" role="combobox" aria-expanded="true" aria-controls="pal-list" aria-autocomplete="list" placeholder="Search or ask" autocomplete="off" spellcheck="false" enterkeyhint="go"></div><button type="button" class="pal-hint" id="pal-hint" hidden></button><div class="pal-list" id="pal-list" role="listbox" aria-label="Results"></div><div class="pal-foot"><span><kbd>↑</kbd><kbd>↓</kbd> move</span><span><kbd>Enter</kbd> run</span><span><kbd>Esc</kbd> close</span><span><kbd>?</kbd> shortcuts</span></div>`;
 document.body.append(d);const q=d.querySelector('#pal-q');
 q.addEventListener('input',()=>{pal.q=q.value;pal.sel=0;palRender();palFind()});
 q.addEventListener('keydown',e=>{if(e.isComposing||e.keyCode===229)return;
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const n=pal.items.length;if(n){pal.sel=(pal.sel+(e.key==='ArrowDown'?1:-1)+n)%n;palPaint()}return}
  if(e.key==='Enter'){e.preventDefault();palPick(pal.sel);return}
  if(e.key==='Tab'){e.preventDefault();return}  // focus stays in the field while it is open
  if(e.key==='Escape'){e.preventDefault();palClose()}});
 d.addEventListener('cancel',e=>{e.preventDefault();palClose()});
 d.addEventListener('click',e=>{if(e.target===d){palClose();return}if(e.target.closest('#pal-hint')){palTry();return}const o=e.target.closest('[data-pal]');if(o)palPick(+o.dataset.pal)});
 d.addEventListener('mousemove',e=>{const o=e.target.closest('[data-pal]');if(o&&+o.dataset.pal!==pal.sel){pal.sel=+o.dataset.pal;palPaint(false)}});
 return d}
function palShow(o){const d=palDialog();if(d.open)return;for(const x of document.querySelectorAll('dialog[open]'))if(x!==d)return;
 pal.todos=!!o?.todos;pal.from=document.activeElement;pal.ctx=kbCtx();pal.q='';pal.sel=0;pal.found=null;pal.msgs=null;pal.done=[];pal.ask=null;pal.tried=null;pal.seq++;pal.opens++;pal.hint=palExample();palExamplesLoad();if(typeof drawerClose==='function')drawerClose();
 const q=d.querySelector('#pal-q');q.value='';d.showModal();q.focus();palRender()}
const palArea=()=>scopeFilter==='work'||scopeFilter==='personal'?scopeFilter:null;
function palExamplesLoad(){if(!palAskable())return;const area=palArea();
  const people=[...new Set((state.suggestions||[]).filter(s=>!closed(s)&&(scopeFilter==='all'||!scopeFilter||s.scope===scopeFilter)).map(s=>(s.people||[])[0]?.id).filter(Boolean))].slice(0,6);
  const key=JSON.stringify([area,people]);if(pal.examplesKey===key&&Date.now()-pal.examplesAt<5*60e3)return;pal.examplesKey=key;pal.examplesAt=Date.now();
  request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'search_ask_examples',args:{people,area}})})
   .then(r=>{if(pal.examplesKey!==key)return;pal.examples=r&&typeof r==='object'?r:null;if(!pal.hint&&$('#palette')?.open){pal.hint=palExample();palAskShow()}}).catch(()=>{pal.examplesAt=0})}
function palExample(){const ex=pal.examples;if(!ex)return null;
  const people=(Array.isArray(ex.people)?ex.people:[]).map(p=>({p,n:String(p.name||'').trim().split(/\s+/)[0]})).filter(x=>/^\p{L}[\p{L}'’-]{1,19}$/u.test(x.n));
  const all=people.map(({p,n})=>({q:t('what did {} say last week?',n),plan:{person:p.id,from:p.from,to:p.to,said_by:'person'}}));
  return all.length?all[pal.opens%all.length]:null}
function palTry(){const q=$('#pal-q');if(!q||!pal.hint)return;pal.tried=pal.hint;q.value=pal.hint.q;q.focus();q.dispatchEvent(new Event('input'))}
function palClose(){const d=$('#palette');clearTimeout(pal.timer);clearTimeout(pal.askTimer);pal.ask=null;pal.seq++;if(d?.open)d.close();if(d?.contains(document.activeElement))document.activeElement.blur();  /* never left in the closed field, or keys would think you type */
 const f=pal.from;pal.from=null;if(f?.isConnected&&f!==document.body)f.focus({preventScroll:true})}
const palToggle=()=>$('#palette')?.open?palClose():palOpen();
function palRows(){const q=pal.q.trim(),ctx=pal.ctx,recent=palRecent(),groups=[],seen=new Set();
 const acts=actsFor(ctx).map(a=>({a,label:actLabel(a,ctx)}));
 if(!q){const rec=recent.map(id=>acts.find(x=>x.a.id===id)).filter(Boolean);rec.forEach(x=>seen.add(x.a.id));if(rec.length)groups.push(['Recent',rec]);
  for(const g of ['This to-do','Actions','Go to']){const xs=acts.filter(x=>x.a.group===g&&!seen.has(x.a.id));if(xs.length)groups.push([g,xs])}}
 else{const scored=acts.map(x=>({...x,s:palMatch(q,x.a,x.label)+(recent.includes(x.a.id)?8-recent.indexOf(x.a.id):0)})).filter(x=>x.s>8).sort((x,y)=>y.s-x.s||!!y.a.keys-!!x.a.keys);  /* a tie goes to the one with its own key: the everyday action (New to-do before New event) */
  for(const g of ['This to-do','Actions','Go to']){const xs=scored.filter(x=>x.a.group===g).slice(0,8);if(xs.length)groups.push([g,xs])}
  if(groups.length>1){const best=g=>g[1][0].s;groups.sort((x,y)=>best(y)-best(x))}
  const cards=(state.suggestions||[]).filter(s=>!closed(s)).map(s=>({s,score:palCardScore(q,s)})).filter(x=>x.score>=40)  /* words, not scattered letters */.sort((x,y)=>y.score-x.score).slice(0,5);
  if(cards.length)groups.push(['To-dos',cards.map(({s})=>({a:{id:'card:'+s.id,run:()=>chatGo(s.id),entity:true},label:s.title,sub:palCardSub(s)}))]);
  // Done cards in their own group under the open ones: the loaded ones and what the Machine found among all of them
  {const seen=new Set(),done=[...(state.suggestions||[]).filter(closed),...pal.done||[]].filter(s=>!seen.has(s.id)&&seen.add(s.id)).map(s=>({s,score:palCardScore(q,s)})).filter(x=>x.score>=40).sort((x,y)=>y.score-x.score).slice(0,5);
   if(done.length)groups.push(['Done',done.map(({s})=>({a:{id:'card:'+s.id,run:()=>{doneExtra.set(s.id,s);cardsMerge();chatGo(s.id)},entity:true},label:s.title,sub:palCardSub(s)}))])}
  for(const [kind,name] of [['person','People'],['org','Organizations'],['project','Projects']]){const xs=(pal.found||[]).filter(n=>n.kind===kind).slice(0,5);
   if(xs.length)groups.push([name,xs.map(n=>({a:{id:'graph:'+n.id,run:()=>{location.hash=graphHash(n.id)},entity:true},label:n.name||n.id,sub:kind==='person'?(n.ids||[])[0]||'':kind==='org'&&n.domain!==n.name?n.domain||'':''}))])}
  // Messages: the top few of everything the Machine read (the results page's own search), then See all results
  // (a message the answer links to shows once, under the answer). A question about someone or some days lists the
  // other messages the answer read (theirs, those days, newest first), never keyword hits from another time; while
  // such a question is still being answered, only See all results.
  const ak=pal.ask?.q===q?pal.ask:null,asked=new Set(ak?.state==='done'?ak.sources.map(m=>m.id):[]);
  const read=ak?.state==='done'&&Array.isArray(ak.messages),holding=ak&&ak.state==='wait'&&(ak.mark||ak.plan);
  const msgs=read?ak.messages.map(m=>({a:{id:'msg:'+m.id,run:()=>msgOpen(m),entity:true},label:m.title||m.from||t('Message'),sub:[m.title?m.from:'',m.at?humanTime(m.at):''].filter(Boolean).join(' · ')}))
   :holding?[]:(pal.msgs||[]).filter(m=>!asked.has(m.id)).map(m=>({a:{id:'msg:'+m.id,run:()=>msgOpen(m),entity:true},label:m.title||t('Message'),sub:msgSub(m)}));
  if(q.length>=2)groups.push([msgs.length?'Messages':'',[...msgs,  /* no heading over See all results alone */
   {a:{id:'msg-all',run:()=>msgSearch(q),entity:true},label:t('See all results for “{}”',q),sub:pal.msgs===null&&!holding&&!read?t('Looking…'):''}]])}
 // From the sidebar's Search box: the to-dos first (before typing, the first open ones)
 if(pal.todos){if(!q){const open=(state.suggestions||[]).filter(s=>!closed(s)).slice(0,5);if(open.length)groups.unshift(['To-dos',open.map(s=>({a:{id:'card:'+s.id,run:()=>chatGo(s.id),entity:true},label:s.title,sub:palCardSub(s)}))])}
  else groups.sort((x,y)=>['To-dos','Done'].includes(y[0])-['To-dos','Done'].includes(x[0]))}
 // A question's answer on top, its messages under it (palAsk)
 const a=pal.ask;if(q&&a&&a.q===q&&(a.state==='done'||(a.mark||a.plan)&&a.state!=='none'))groups.unshift(['Answer',[...a.sources.map(m=>({a:{id:'ask:'+m.id,run:()=>msgOpen(m),entity:true},label:m.title||m.from||t('Message'),sub:[m.title?m.from:'',m.at?humanTime(m.at):''].filter(Boolean).join(' · ')})),...(a.memory||[]).map(palMemoryRow)],a]);
 return groups}
// What the answer used besides messages (ask_memory.py), each named as what it is and opening where it lives: a
// promise its page, a fact Learning, a person, project or organization its record, meeting notes the notes
const PAL_MEMORY={promise:['Promise',m=>{location.hash=promiseHref(m)}],fact:['Learned',()=>{location.hash='#learning=learned'}],person:['Summary',m=>{location.hash=graphHash(m.id)}],
 project:['Project',m=>{location.hash=graphHash(m.id)}],org:['Organization',m=>{location.hash=graphHash(m.id)}],meeting:['Meeting notes',m=>msgOpen(m)]};
const palMemoryRow=m=>{const [name,go]=PAL_MEMORY[m.type]||PAL_MEMORY.meeting;
 return {a:{id:'ask:'+m.type+':'+m.id,run:()=>go(m),entity:true},label:m.title||t(name),sub:[t(name),m.from,m.at?humanTime(m.at):''].filter(Boolean).join(' · ')}};
// While it works: three gentle dots (still with reduced motion), and Looking… for a screen reader
const palAnswer=a=>a.state==='done'?`<p class="pal-answer" id="pal-answer" translate="no" dir="auto">${esc(a.text.slice(0,a.shown))}</p>`
 :a.state==='error'?`<p class="pal-answer muted" id="pal-answer">${esc(t('Couldn’t answer that right now.'))}</p>`
 :`<p class="pal-answer muted" id="pal-answer" role="status"><span class="pal-dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="pal-sr">${esc(t('Looking…'))}</span></p>`;
function palRender(){const d=$('#palette');if(!d?.open)return;palAskShow();const groups=palRows(),list=d.querySelector('#pal-list'),was=pal.items[pal.sel]?.a.id;pal.items=[];let html='';
 for(const [g,xs,ask] of groups){html+=`${g?`<div class="pal-group" role="presentation">${esc(g)}</div>`:''}${ask?palAnswer(ask):''}`;
  for(const x of xs){const i=pal.items.push(x)-1;const keys=x.a.review?'':x.a.keys;
   html+=`<div class="pal-item" role="option" id="pal-o-${i}" data-pal="${i}" aria-selected="false"><span class="pal-label">${esc(x.label)}</span>${x.sub?`<small>${esc(x.sub)}</small>`:''}${keys?`<span class="pal-keys" aria-label="${esc(kbText(keys))}">${kbKeys(keys)}</span>`:''}</div>`}}
 if(!pal.items.length&&!groups.some(g=>g[2]))html=`<p class="pal-empty">${pal.q.trim().length>=2&&pal.found===null?'Looking…':'Nothing matches.'}</p>`;
 // an answer that comes in keeps the row the keyboard was on (it never jumps to the answer's messages)
 const kept=pal.keep&&was?pal.items.findIndex(x=>x.a.id===was):-1;pal.keep=false;if(kept>=0)pal.sel=kept;
 list.innerHTML=html;pal.sel=Math.min(pal.sel,Math.max(0,pal.items.length-1));palPaint(kept<0)}
function palPaint(scroll=true){const d=$('#palette');if(!d)return;const q=d.querySelector('#pal-q');
 for(const o of d.querySelectorAll('[data-pal]'))o.setAttribute('aria-selected',String(+o.dataset.pal===pal.sel));
 const on=d.querySelector(`#pal-o-${pal.sel}`);if(on){q.setAttribute('aria-activedescendant',on.id);if(scroll)on.scrollIntoView({block:'nearest'})}else q.removeAttribute('aria-activedescendant')}
// People, organizations and projects come from the Graph's own search (api/graph?q=), a moment after typing stops;
// an answer to an older query is dropped.
// Messages come from the results page's search (api/events: by meaning and words, every account) on their own, as
// it can take longer: the rest shows first.
function palFind(){clearTimeout(pal.timer);const q=pal.q.trim(),seq=++pal.seq;palAsk(q,seq);if(q.length<2){pal.found=[];pal.msgs=[];return}pal.found=null;pal.msgs=null;
 pal.timer=setTimeout(async()=>{let found=[],done=[];const e=encodeURIComponent(q);
  request('api/events?account=all&q='+e).then(r=>Array.isArray(r)?r:[]).catch(()=>[]).then(rows=>{if(seq!==pal.seq||!$('#palette')?.open)return;pal.msgs=rows.slice(0,4);palRender()});
  await Promise.all([request('api/graph?q='+e).then(r=>{found=Array.isArray(r?.found)?r.found:[]}).catch(()=>{}),
   request('api/cards/done?limit=8&q='+e).then(r=>{done=Array.isArray(r?.cards)?r.cards:[]}).catch(()=>{})]);  /* done cards beyond the loaded ones */
  if(seq!==pal.seq||!$('#palette')?.open)return;pal.found=found;pal.done=done;palRender()},180)}
// Ask from search (search_ask.py): words that ask something get a short answer from the person's own messages, above
// the results, with each message it used as a row that opens it. Only from the area in view (All, Work or Personal).
// Whether they ask something is the model's call from what they mean: a name or a few keywords get nothing back and
// the results stay as they are. It never holds the results up: it asks once typing rests, and an older answer is
// dropped. Nothing shows when no model is connected. A question mark shows Looking… while it works.
const ASK_REST=800;
function palAsk(q,seq){clearTimeout(pal.askTimer);if(pal.ask&&pal.ask.q!==q)pal.ask=null;
 const plan=pal.tried?.q===q?pal.tried.plan:null;  // the suggested question, as offered: at once, with its person and days
 if(pal.askOff||pal.ask||!plan&&q.split(/\s+/).length<3)return;
 pal.askTimer=setTimeout(async()=>{if(seq!==pal.seq||!$('#palette')?.open)return;
  const area=palArea(),a=pal.ask={q,state:'wait',text:'',sources:[],shown:0,mark:/[?？¿؟]\s*$/.test(q),plan:!!plan};
  if(a.mark||a.plan){pal.keep=true;palRender()}
  let r;try{r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'search_ask',args:{query:q,area,...(plan?{plan}:{})}})})}catch{r={error:true}}
  if(pal.ask!==a)return;
  if(r?.off){pal.askOff=true;pal.ask=null}
  else if(typeof r?.answer==='string'&&r.answer.trim())Object.assign(a,{state:'done',text:r.answer.trim(),sources:Array.isArray(r.sources)?r.sources:[],memory:Array.isArray(r.memory)?r.memory:[],...(Array.isArray(r.messages)?{messages:r.messages}:{})});
  else if(r?.error)a.state='error';
  else a.state='none';  // not a question, or nothing found: the results stay as they are
  if(!$('#palette')?.open)return;pal.keep=true;palRender();if(a.state==='done')palReveal(a)},plan?0:ASK_REST)}
// The answer comes in a few words at a time, as it is read
function palReveal(a){const step=()=>{if(pal.ask!==a)return;a.shown=Math.min(a.text.length,(a.text.indexOf(' ',a.shown+4)+1||a.text.length));
 const p=$('#pal-answer');if(p)p.textContent=a.text.slice(0,a.shown);if(a.shown<a.text.length)setTimeout(step,28)};step()}
function palPick(i){const x=pal.items[i];if(!x)return;const ctx=pal.ctx;palClose();if(!x.a.entity)palRemember(x.a.id);actRun(x.a,ctx)}

// The shortcut sheet (?), from the same registry.
function keysShow(){let d=$('#keys-sheet');for(const x of document.querySelectorAll('dialog[open]'))if(x!==d)return;
 if(!d){d=document.createElement('dialog');d.id='keys-sheet';d.setAttribute('aria-labelledby','keys-title');document.body.append(d);d.addEventListener('click',e=>{if(e.target===d)d.close()})}
 const row=(keys,label,more='')=>`<p><span>${esc(label)}</span><span class="keys">${kbKeys(keys)}${more}</span></p>`,ctx={card:null,id:'',chat:false};
 const of=g=>ACTIONS.filter(a=>a.group===g&&a.keys&&!a.review&&!a.each&&!a.alias&&(!a.when||(()=>{try{return a.when(ctx)}catch{return false}})()||g==='This to-do'||g==='Calendar')).map(a=>row(a.keys,a.id==='talk'?'Talk (not on the Calendar)':actLabel(a,ctx))).join('');  // on the Calendar, T is Today
 d.innerHTML=`<form method="dialog"><div class="snooze-heading"><h2 id="keys-title">Keyboard shortcuts</h2><button aria-label="Close">×</button></div></form><div class="keys-sheet">
 <div><h3>General</h3>${row('mod+k','Search and commands','<span class="then">or</span><kbd>/</kbd>')}${of('Actions')}${row('esc','Close a chat or dialog')}</div>
 <div><h3>Go to</h3>${of('Go to')}</div>
 <div><h3>Calendar</h3>${of('Calendar')}${row('←','Previous')}${row('→','Next')}</div>
 <div><h3>Lists and to-dos</h3>${row('j','Next','<span class="then">or</span><kbd>↓</kbd>')}${row('k','Previous','<span class="then">or</span><kbd>↑</kbd>')}${row('enter','Open')}${row('→','Open a folded list')}${row('←','Fold it again')}${of('This to-do')}</div></div>`;
 d.showModal()}
