// Work/Personal filter, remembered on this device.
// Tapping a count tile (or a section heading) folds or unfolds that section; remembered on this device.
const folded=new Set(JSON.parse(localStorage.getItem('folded-sections')||'[]'));
function toggleSection(key){
if(key==='later'){const l=$('#later-list');if(!l)return;l.open=!l.open;if(l.open)l.scrollIntoView({behavior:'smooth',block:'start'});return}
folded.has(key)?folded.delete(key):folded.add(key);localStorage.setItem('folded-sections',JSON.stringify([...folded]));render();
if(!folded.has(key))document.getElementById('section-'+key)?.scrollIntoView({behavior:'smooth',block:'start'})}
$('#suggestions').addEventListener('click',e=>{const h=e.target.closest('.section-head[data-fold]');if(h)toggleSection(h.dataset.fold);const m=e.target.closest('[data-more]');if(!m)return;const id=m.dataset.more,open=!expandedBodies.has(id);open?expandedBodies.add(id):expandedBodies.delete(id);m.previousElementSibling.classList.toggle('clamp',!open);m.setAttribute('aria-expanded',open);m.textContent=open?'Show less':'Show more'})
// Long history lists show the latest few; Show more adds ten at a time and survives the refresh.
const notesN=n=>`${n} note${n===1?'':'s'}`;
// What I've learned: one block per kind (how they write per channel, facts, how to do things, moved into skills); newest first.
// Each block has a count and folds after 5 with Show all; a channel shows 2 lines with More. A condensed one says what it stands for, with Undo.
const learnAll=new Set(),voiceOpen=new Set();let learnEdit=null,learnEditText=null;  // the fact being edited, and what was typed so far
// Open one learning on What I've learned (from a card's chat): its block unfolded, the row in view and lit; with edit, its editor open.
function learnedShow(id,what,edit){if(chatId){history.pushState(null,'',location.pathname+location.search);openChatLink()}showTab('feedback');  // Back returns to the chat
const f=(state.facts||[]).find(x=>x.id===id);
 if(edit&&f){learnEdit=id;learnEditText=null}const group=f?(f.kind==='draft'?'rules':'facts'):null;if(group)learnAll.add(group);
 $('#facts').innerHTML=learnedList();const row=f?document.getElementById('learned-'+id):null;
 requestAnimationFrame(()=>{(row||$('#facts')).scrollIntoView({block:row?'center':'start'});if(row){row.classList.remove('flash');void row.offsetWidth;row.classList.add('flash')}const t=row?.querySelector('textarea');if(t){t.focus();t.setSelectionRange(t.value.length,t.value.length)}})}
const learnDay=d=>d.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short',...(d.getFullYear()!==new Date().getFullYear()?{year:'numeric'}:{})});  // Tue, Oct 20, as elsewhere
const VOICE_ICON={linkedin:'linkedin',whatsapp:'whatsapp',telegram:'telegram',slack:'slack',email:'gmail',gmail:'gmail',outlook:'gmail',x:'x','x dm':'x',twitter:'x',github:'github'};
// The learning loop's changes (learning_loop.py): what changed, why, and Undo; an undone one stays, marked.
const LEARN_WHAT={voice:c=>`${c.channel==='All'?'Everywhere':c.channel}: how you write`,draft:c=>c.before?'Rule changed':'Rule added',fact:c=>c.before?'Fact changed':'Fact added'};
function learnChange(c){const what=(LEARN_WHAT[c.kind]||(()=>'Changed'))(c),text=String(c.text||'').split('\n').map(l=>l.trim()).filter(Boolean).join(' · ');
 return `<div class="change-row${c.undone?' undone':''}"><span class="grow"><strong>${esc(what)}</strong><span class="change-text">${esc(text)}</span>${c.why?`<small>${esc(c.why)}</small>`:''}<small class="change-when">${esc(learnDay(new Date(c.at)))}${c.undone?' · Undone':''}</small></span>${c.undone?'':`<span class="learn-acts"><button type="button" class="quiet" data-learn-undo="${c.id}" aria-label="Undo: ${esc(what)}">Undo</button></span>`}</div>`}
// A fact's sort and end day, quietly under it: "Temporary · Until Nov 14". A plain fact without an end shows nothing.
const FACT_SORT={event:'Temporary',commitment:'Commitment',preference:'Preference'};
const factUntil=d=>new Date(d+'T12:00:00').toLocaleDateString(DL,{day:'numeric',month:'short',...(d.slice(0,4)!==String(new Date().getFullYear())?{year:'numeric'}:{})});
function factMeta(f){const bits=[FACT_SORT[f.fact_kind]?t(FACT_SORT[f.fact_kind]):'',f.valid_until?t('Until {}',factUntil(f.valid_until)):''].filter(Boolean);return bits.length?`<small class="fact-meta">${esc(bits.join(' · '))}</small>`:''}
function learnedList(){
 const facts=state.facts||[],at=x=>x.updated_at||x.created_at||'',newest=(a,b)=>at(b).localeCompare(at(a));
 const mergedUndo=(n,attr,label)=>n?`<small>Merged from ${notesN(n)} · <button type="button" class="learn-link" ${attr} aria-label="Undo merge: ${esc(label)}">Undo merge</button></small>`:'';
 const fact=f=>learnEdit===f.id?`<div class="fact-row" id="learned-${f.id}"><form class="fact-edit" data-fact-edit="${f.id}"><textarea name="text" maxlength="240" aria-label="Edit what I learned">${esc(learnEditText??f.text)}</textarea><span class="learn-acts"><button type="button" class="quiet learn-remove" data-forget="${f.id}" aria-label="Remove: ${esc(f.text)}">Remove</button><button type="button" class="quiet" data-edit-cancel>Cancel</button><button type="submit" class="primary">Save</button></span></form></div>`:
  `<div class="fact-row" id="learned-${f.id}"><span class="grow">${esc(f.text)}${factMeta(f)}${mergedUndo(f.merged,`data-unmerge-fact="${f.id}"`,f.text)}</span><span class="learn-acts"><button type="button" class="quiet" data-edit-fact="${f.id}" aria-label="Edit: ${esc(f.text)}">Edit</button><button type="button" class="quiet" data-forget="${f.id}" aria-label="Remove: ${esc(f.text)}">Remove</button></span></div>`;
 const voice=v=>{const name=v.channel==='All'?'Everywhere':v.channel,lines=String(v.text||'').split('\n').map(l=>l.trim()).filter(Boolean),open=voiceOpen.has(v.channel),extra=lines.length-2;
  return `<div class="voice-row" data-channel="${esc(v.channel)}">${icon(VOICE_ICON[String(v.channel).toLowerCase()]||'plugin')}<span class="grow"><strong>${esc(name)}</strong><ul class="voice-lines">${lines.map((l,i)=>`<li${i>1&&!open?' hidden':''}>${esc(l)}</li>`).join('')}</ul>${extra>0?`<button type="button" class="voice-more" data-voice-more="${esc(v.channel)}" aria-expanded="${open}">${open?'Less':extra+' more'}</button>`:''}${mergedUndo(v.merged,`data-unmerge-voice="${esc(v.channel)}"`,v.channel)}</span><span class="learn-acts"><button type="button" class="quiet" data-voice-edit="${esc(v.channel)}" aria-label="Edit how you write: ${esc(name)}">Edit</button></span></div>`};
 const groups=[['voices','How you write','Per channel, from your messages and notes.',[...(state.voices||[])].sort(newest).map(voice)],
  ['facts','Facts','Things I keep in mind about your work.',facts.filter(f=>f.kind!=='draft').sort(newest).map(fact)],
  ['rules','How to do things','Rules for a kind of task.',facts.filter(f=>f.kind==='draft').sort(newest).map(fact)],
  ['ended','Ended','Past their end date. Bring one back if it still holds.',(state.facts_ended||[]).map(f=>`<div class="fact-row"><span class="grow">${esc(f.text)}${factMeta(f)}</span><span class="learn-acts"><button type="button" class="quiet" data-fact-back="${f.id}" aria-label="${esc(t('Bring back: {}',f.text))}">${esc(t('Bring back'))}</button></span></div>`)],
  ['skills','Moved into skills','Notes that now live in a skill.',(state.moved||[]).map(m=>`<div><span class="grow"><strong>${esc(m.name)}</strong> ${notesN(m.notes)}</span><span class="learn-acts"><button type="button" class="quiet" data-unmerge-skill="${esc(m.skill_id)}" aria-label="Put back the notes in ${esc(m.name)}">Put back</button></span></div>`)]].filter(g=>g[3].length);
 const changes=state.learning_changes||[];
 if(changes.length)groups.unshift(['changes','Recent changes','What I picked up from your edits, dismissals and chats.',changes.map(learnChange)]);
 if(!groups.length)return'<div class="muted">Nothing yet. When a note on a to-do holds beyond it, I keep it here.</div>';
 const c=state.condensed;
 return (c&&c.notes?`<div class="muted learn-note">Condensed ${notesN(c.notes)} on ${esc(learnDay(new Date(c.at)))}.</div>`:'')+
  groups.map(([k,title,blurb,rows])=>{const all=learnAll.has(k)||rows.length<=6;
   return `<section class="learn-group" data-group="${k}" aria-labelledby="learn-${k}"><div class="learn-head"><h3 id="learn-${k}">${title} <span class="count">${rows.length}</span></h3><p>${blurb}</p></div><div class="list">${(all?rows:rows.slice(0,5)).join('')}${rows.length>6?`<button type="button" class="quiet learn-all" data-learn-all="${k}" aria-expanded="${all}">${all?'Show fewer':'Show all '+rows.length}</button>`:''}</div></section>`}).join('');
}
// Long lists load a page at a time (Done, the Graph's tabs, its search): 30 rows, the next page by itself as the end
// scrolls near, and a quiet Show more for keyboards, screen readers and when the scroll doesn't tell. A pager keeps what
// it loaded, so a refresh, a tab switch or going back from a card or a person shows the same rows at the same place.
const pagers=new Map();
function pager(key,load,row,rows){let p=pagers.get(key);if(!p){p={key,load,row,rows,items:[],next:'0',total:null,busy:false,failed:false,html:''};pagers.set(key,p)}else{p.load=load;p.row=row;p.rows=rows}return p}
function pagerDrop(prefix){for(const k of [...pagers.keys()])if(k===prefix||k.startsWith(prefix+':'))pagers.delete(k)}
const pagerSlot=(key,empty='',rows='')=>`<div class="pager" data-pager="${esc(key)}" data-empty="${esc(empty)}" data-rows="${esc(rows)}"></div>`;
const pagerFoot=p=>p.busy?'<p class="pager-loading" role="status">Loading…</p>':p.failed?'<button type="button" class="quiet more-rows" data-pager-more>Couldn’t load. Try again</button>':p.next!=null?'<button type="button" class="quiet more-rows" data-pager-more>Show more</button>':'';
function pagerFootPaint(el,p){const empty=!p.items.length&&p.next==null&&!p.busy&&!p.failed;el.querySelector('.pager-foot').innerHTML=empty&&el.dataset.empty?`<p class="muted pager-empty">${esc(el.dataset.empty)}</p>`:pagerFoot(p)}
function pagerMount(root=document){for(const el of root.querySelectorAll('[data-pager]')){const p=pagers.get(el.dataset.pager);if(!p)continue;
 if(!el.firstChild){if(p.rows)p.html=p.rows(p.items);el.innerHTML=`<div class="pager-rows ${esc(el.dataset.rows||'')}">${p.html}</div><div class="pager-foot"></div>`;pagerSeen.observe(el.querySelector('.pager-foot'));detailsSync(el)}pagerFootPaint(el,p)}}
const pagerNear=el=>{const f=el.querySelector('.pager-foot');if(!f||!el.offsetParent)return false;const r=f.getBoundingClientRect(),box=el.closest('.side-cards,.chat-side');return r.top<innerHeight+600&&r.bottom>-600&&!box};
function pagerMore(key){const p=pagers.get(key);if(!p||p.next==null&&!p.busy)return Promise.resolve();if(p.busy)return p.pending;return p.pending=pagerLoad(key,p)}
async function pagerLoad(key,p,paint=true){p.busy=true;p.failed=false;const els=()=>paint?[...document.querySelectorAll('[data-pager]')].filter(e=>e.dataset.pager===key):[];
 for(const el of els())pagerFootPaint(el,p);let fresh='';
 try{const r=await p.load(p.next);if(pagers.get(key)!==p)return;const have=new Set(p.items.map(x=>x?.id).filter(Boolean));r.items=r.items.filter(x=>!x?.id||!have.has(x.id));p.items.push(...r.items);if(p.rows){p.html=p.rows(p.items);fresh=r.items.length?null:''}else{fresh=r.items.map(x=>p.row(x)).join('');p.html+=fresh}p.next=r.next??null;p.total=r.total??p.total;p.onload?.(r.items)}catch{p.failed=true}finally{p.busy=false}
 for(const el of els()){const rows=el.querySelector('.pager-rows');if(fresh===null){if(rows)rows.innerHTML=p.html}else rows?.insertAdjacentHTML('beforeend',fresh);pagerFootPaint(el,p)}
 if(fresh)requestAnimationFrame(()=>{for(const el of els())if(pagerNear(el)){pagerMore(key);break}})}
const pagerSeen=new IntersectionObserver(es=>{for(const e of es)if(e.isIntersecting){const el=e.target.closest('[data-pager]');if(el&&pagerNear(el))pagerMore(el.dataset.pager)}},{rootMargin:'0px 0px 600px 0px'});
document.addEventListener('click',e=>{const b=e.target.closest('[data-pager-more]');if(!b)return;e.preventDefault();e.stopPropagation();const el=b.closest('[data-pager]'),p=pagers.get(el?.dataset.pager);if(p?.failed)p.failed=false;if(el)pagerMore(el.dataset.pager)},true);
// Done cards beyond the status payload: those loaded join the cards the page knows, so a chat or an action finds them
const doneExtra=new Map();
const closedAt=s=>s.closed_at||(state?.decisions||[]).filter(d=>d.suggestion_id===s.id&&['complete','reject'].includes(d.choice)).map(d=>d.created_at).sort().at(-1)||s.created_at;
const doneKey=()=>'done:'+scopeFilter;
// A Machine from before the Done pages has no api/cards/done: then the done cards in the status payload are the list
const doneLocal=()=>{const items=(state?.suggestions||[]).filter(s=>closed(s)&&(scopeFilter==='all'||s.scope===scopeFilter)).sort((a,b)=>closedAt(b).localeCompare(closedAt(a)));return {items,next:null,total:items.length}};
// The first page is the done cards the status payload already has, so the list is there at once; the Machine sends the rest
function donePager(){const fresh=!pagers.has(doneKey()),p=pager(doneKey(),cursor=>request(`api/cards/done?cursor=${encodeURIComponent(cursor)}${scopeFilter==='all'?'':'&scope='+scopeFilter}`).catch(()=>null).then(r=>{
  if(!Array.isArray(r?.cards)){const l=doneLocal(),n=Number(cursor)||0;return {items:l.items.slice(n,n+30),next:n+30<l.items.length?String(n+30):null,total:l.total}}
  for(const c of r.cards)doneExtra.set(c.id,c);cardsMerge();return {items:r.cards,next:r.next,total:r.total}}),s=>suggestionCard(s),doneRows);
 if(fresh){const l=doneLocal(),n=Math.min(30,l.items.length),total=Math.max(l.total,state?.done_counts?.[scopeFilter]??0);p.items=l.items.slice(0,n);p.html=doneRows(p.items);p.total=total;p.next=total>n?String(n):null}
 return p}
// Done: sent and skipped follow-ups fold into one row per board (or the projects' own rules) and day: "13 follow-ups
// sent for Partner listings". Opening it lists them (project, to, when), each a link to its to-do. A search (the
// sidebar's Find, the palette) still finds each one.
const doneOpen=new Set(),donePageOpen=new Set();  // the sidebar's open rows, the Done list's
const fuDoneState=s=>['sent','skipped','stopped'].includes(s?.follow_up?.state)?(s.follow_up.state==='sent'?'sent':'skipped'):'';
function doneFold(items){const groups=new Map(),out=[];
 for(const x of items){const st=x&&!x.fuGroup&&!x.fuFold&&fuDoneState(x);if(!st){out.push(x);continue}
  const k=(x.follow_up.group||'own')+'@'+localDay(new Date(closedAt(x)));let g=groups.get(k);
  if(!g){g={fuFold:k,id:'fold-'+k,items:[],board:x.follow_up.group?x.follow_up.board||'':'',closed_at:closedAt(x),scope:x.scope};groups.set(k,g);out.push(g)}g.items.push(x)}
 return out.map(x=>!x.fuFold?x:x.items.length>1?Object.assign(x,{title:doneFoldTitle(x)}):x.items[0])}
// "13 follow-ups sent for Partner listings", and the skipped ones as a quiet count beside it so the title stays short
function doneFoldTitle(g){const sent=g.items.filter(s=>fuDoneState(s)==='sent').length;g.skipped=g.items.length-sent;
 if(!sent)return g.board?t(['{} follow-up skipped for {}','{} follow-ups skipped for {}'],g.skipped,g.board):t(['{} follow-up skipped','{} follow-ups skipped'],g.skipped);
 return g.board?t(['{} follow-up sent for {}','{} follow-ups sent for {}'],sent,g.board):t(['{} follow-up sent','{} follow-ups sent'],sent)}
const doneFoldSkipped=g=>g.skipped&&g.skipped<g.items.length?t('{} skipped',g.skipped):'';
// One folded follow-up: the project, who it went to, and when (or that it was skipped)
function doneFoldWho(s){const a=frDraft(s),to=a?(a.to_name||(a.to||[]).join(', ')):'';return to?t('To {}',to):''}
const doneFoldWhen=s=>fuDoneState(s)==='sent'?new Date(closedAt(s)).toLocaleTimeString(DL,{hour:'numeric',minute:'2-digit'}):t('Skipped');
function sideRow(x,cur){
 if(x.fuGroup)return `<a href="#" ${x.writing?'data-fu-card':'data-fu-review'}="${esc(x.fuGroup)}" title="${esc(x.title)}" translate="no">${esc(x.title)}</a>`;
 if(x.fuFold){const open=doneOpen.has(x.fuFold);
  const n=doneFoldSkipped(x);
  return `<button type="button" class="done-fold" data-done-fold="${esc(x.fuFold)}" aria-expanded="${open}" title="${esc([x.title,n].filter(Boolean).join(' · '))}"><span translate="no">${esc(x.title)}</span>${n?`<small>${esc(n)}</small>`:''}${CHEVRON}</button>`
   +(open?`<div class="done-fold-list">${x.items.map(s=>`<a href="#chat=${esc(s.id)}" title="${esc(s.title)}"${s.id===cur?' aria-current="page"':''}><span translate="no">${esc(frName(s.follow_up))}</span><small>${esc([doneFoldWho(s),doneFoldWhen(s)].filter(Boolean).join(' · '))}</small></a>`).join('')}</div>`:'')}
 return `<a href="#chat=${esc(x.id)}" title="${esc(x.title)}" translate="no"${x.id===cur?' aria-current="page"':''}>${esc(x.title)}</a>`}
// The Done list on the Suggestions page: the same fold, a quiet to-do that opens to the list
function doneRows(items){return doneFold(items).map(x=>x.fuFold?doneFoldCard(x):suggestionCard(x)).join('')}
function doneFoldCard(g){const open=donePageOpen.has(g.fuFold);
 return `<article class="card todo t-faint fu-done" id="${esc(g.id.replace(/[^\w-]/g,'-'))}" data-status="completed"><details data-done-fold-card="${esc(g.fuFold)}"${open?' open':''}><summary><h3 translate="no">${esc(g.title)}</h3>${doneFoldSkipped(g)?`<span class="done-fold-n">${esc(doneFoldSkipped(g))}</span>`:''}<span class="meta-side">${time(g.closed_at,true)}</span></summary>`
  +`<ul class="fu-done-list">${g.items.map(s=>`<li><a href="#chat=${esc(s.id)}" translate="no">${esc(frName(s.follow_up))}</a><span>${esc(doneFoldWho(s))}</span><span class="muted">${esc(doneFoldWhen(s))}</span></li>`).join('')}</ul></details></article>`}
document.addEventListener('click',e=>{const b=e.target.closest('[data-done-fold]');if(!b)return;e.preventDefault();const k=b.dataset.doneFold;doneOpen.has(k)?doneOpen.delete(k):doneOpen.add(k);const inSide=!!b.closest('#side-cards');sideCards();if(chatOpen())render();
 (inSide?$('#side-cards'):document).querySelector(`[data-done-fold="${CSS.escape(k)}"]`)?.focus()});
document.addEventListener('toggle',e=>{const d=e.target;if(!d.matches?.('[data-done-fold-card]'))return;d.open?donePageOpen.add(d.dataset.doneFoldCard):donePageOpen.delete(d.dataset.doneFoldCard)},true);
function cardsMerge(){if(!state?.suggestions)return;const ids=new Set(state.suggestions.map(s=>s.id));for(const c of doneExtra.values())if(!ids.has(c.id))state.suggestions.push(c)}
let doneSeen='';  // done counts and ids as last shown: when they change, the Done lists start over from the top
const listShown={};const clipList=(id,rows,empty,n=3)=>{const k=listShown[id]||n;return rows.length?rows.slice(0,k).join('')+(rows.length>k?`<button type="button" class="quiet more-rows" data-more="${id}" data-shown="${k}">Show ${Math.min(10,rows.length-k)} more</button>`:''):empty};
document.addEventListener('click',e=>{const b=e.target.closest('[data-more]');if(!b)return;listShown[b.dataset.more]=(Number(b.dataset.shown)||listShown[b.dataset.more]||3)+10;render()});
document.addEventListener('click',async e=>{const b=e.target.closest('[data-promise]');if(!b)return;b.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'promise_close',args:{id:Number(b.dataset.promise),status:b.dataset.close}})});toast(b.dataset.close==='kept'?'Marked done.':'Dropped.');refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#facts').addEventListener('click',async e=>{const vm=e.target.closest('[data-voice-more]');if(vm){const ch=vm.dataset.voiceMore,open=!voiceOpen.has(ch);open?voiceOpen.add(ch):voiceOpen.delete(ch);$('#facts').innerHTML=learnedList();$(`#facts [data-voice-more="${CSS.escape(ch)}"]`)?.focus();return}
 const la=e.target.closest('[data-learn-all]');if(la){const k=la.dataset.learnAll;learnAll.has(k)?learnAll.delete(k):learnAll.add(k);$('#facts').innerHTML=learnedList();$(`#facts [data-learn-all="${k}"]`)?.focus();return}
 const lu=e.target.closest('[data-learn-undo]');if(lu){lu.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'learning_undo',args:{id:Number(lu.dataset.learnUndo)}})});toast('Undone.');refresh()}catch(err){errCaught(err);lu.disabled=false;toast(err.message,true)}return}
 const fb=e.target.closest('[data-fact-back]');if(fb){fb.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'unmerge_fact',args:{expired:Number(fb.dataset.factBack)}})});toast(t('Brought back.'));refresh()}catch(err){errCaught(err);fb.disabled=false;toast(err.message,true)}return}
 const u=e.target.closest('[data-unmerge-fact],[data-unmerge-voice],[data-unmerge-skill]');if(u){u.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'unmerge_fact',args:u.dataset.unmergeSkill?{skill:u.dataset.unmergeSkill}:u.dataset.unmergeVoice?{channel:u.dataset.unmergeVoice}:{id:Number(u.dataset.unmergeFact)}})});toast('Notes restored.');refresh()}catch(err){errCaught(err);u.disabled=false;toast(err.message,true)}return}
 const ed=e.target.closest('[data-edit-fact]');if(ed){learnEdit=Number(ed.dataset.editFact);learnEditText=null;$('#facts').innerHTML=learnedList();const t=$(`#learned-${learnEdit} textarea`);t?.focus();t?.setSelectionRange(t.value.length,t.value.length);return}
 if(e.target.closest('[data-edit-cancel]')){const id=learnEdit;learnEdit=learnEditText=null;$('#facts').innerHTML=learnedList();$(`#facts [data-edit-fact="${id}"]`)?.focus();return}
 const b=e.target.closest('[data-forget]');if(!b)return;b.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'forget_fact',args:{id:Number(b.dataset.forget)}})});if(learnEdit===Number(b.dataset.forget))learnEdit=learnEditText=null;toast('Removed.');refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#facts').addEventListener('input',e=>{if(e.target.closest('[data-fact-edit]'))learnEditText=e.target.value});
$('#facts').addEventListener('keydown',e=>{if(e.key==='Escape'&&e.target.closest('[data-fact-edit]'))e.target.closest('form').querySelector('[data-edit-cancel]').click()});
$('#facts').addEventListener('submit',async e=>{const form=e.target.closest('[data-fact-edit]');if(!form)return;e.preventDefault();const id=Number(form.dataset.factEdit),text=form.text.value.trim(),save=form.querySelector('[type=submit]');save.disabled=true;
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'edit_fact',args:{id,text}})});const f=(state.facts||[]).find(x=>x.id===id);if(f)f.text=text;learnEdit=learnEditText=null;$('#facts').innerHTML=learnedList();toast('Saved.');refresh()}catch(err){errCaught(err);save.disabled=false;toast(err.message,true)}});
// Ctrl+Enter (Cmd+Enter on a Mac) in a filled text field clicks the nearest primary button of its form, editor or card, if enabled. Plain Enter is left alone.
// A chat composer is its own boundary: it sends its message itself and never presses the card's Do it behind it.
document.addEventListener('keydown',e=>{const f=e.target;if(e.key!=='Enter'||!(e.ctrlKey||e.metaKey)||e.isComposing||e.defaultPrevented||!f.matches?.('textarea,input:not([type]),input[type=text],input[type=email],input[type=search],input[type=url],input[type=tel],input[type=number]')||!f.value.trim())return;const shown=b=>b.getClientRects().length>0;for(let box=f.parentElement;box&&box!==document.body;box=box.parentElement){const b=[...box.querySelectorAll('button.primary')].find(shown);if(b){e.preventDefault();if(!b.disabled)b.click();return}if(box.matches('form,dialog,article,.chat-compose'))return}});
$('#suggestions').addEventListener('keydown',e=>{const h=e.target.closest('.section-head[data-fold]');if(h&&(e.key==='Enter'||e.key===' ')){e.preventDefault();toggleSection(h.dataset.fold)}});
$('#suggestions').addEventListener('toggle',e=>{if(e.target.id==='later-list')$('[data-fold-tile="later"]')?.setAttribute('aria-expanded',e.target.open)},true);
// The To-dos filter (All, Work, Personal) is kept on the Machine with the language (locale_prefs.todo_scope), so every
// device shows the same list. A filter this browser kept from before goes to the Machine once, then this browser forgets
// it; a Machine that can't save it (no config.json) keeps it on this device. A card link may show All for a while
// (openCardLink); a change from another device comes in with the next refresh.
const scopeLegacy=(()=>{try{const v=localStorage.getItem('scope-filter');return ['work','personal'].includes(v)?v:null}catch{return null}})();
let scopeFilter=scopeLegacy||'all',scopeSynced,scopeSaving=0,scopeMigrated=false;
function scopeSave(v){scopeSaving++;
 return request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'set_locale',args:{todo_scope:v}})})
  .then(l=>{if(l&&'todo_scope' in l){state.locale=l;scopeSynced=l.todo_scope}try{localStorage.removeItem('scope-filter')}catch{}})
  .catch(()=>{try{localStorage.setItem('scope-filter',v)}catch{}}).finally(()=>{scopeSaving--})}
function scopeSync(l){if(!l||!('todo_scope' in l)||scopeSaving)return;const v=l.todo_scope;
 if(v==null){if(scopeLegacy&&l.saveable&&!scopeMigrated){scopeMigrated=true;scopeSave(scopeLegacy)}return}
 if(v!==scopeSynced){scopeSynced=v;scopeFilter=v}}
function scopeSet(v){if(!['all','work','personal'].includes(v))return;linkedCardId=null;scopeFilter=v;scopeSynced=v;scopeSave(v);render()}
// When a filter is on, the list says so at its top, with the way back to All.
const scopeNote=empty=>scopeFilter==='all'?'':`<p class="scope-note" role="status"><span>${scopeFilter==='work'?(empty?'No work to-dos':'Work only'):(empty?'No personal to-dos':'Personal only')}</span> · <button type="button" class="link" data-scope="all">Show all</button></p>`;
$('#suggestions').addEventListener('click',e=>{const b=e.target.closest('.scope-note [data-scope]');if(b){e.stopPropagation();scopeSet(b.dataset.scope)}});
let linkedCardId=null;
$('#suggestion-stats').addEventListener('click',e=>{const t=e.target.closest('[data-fold-tile]');if(t)toggleSection(t.dataset.foldTile)});
$('#suggestion-summary').addEventListener('click',e=>{const b=e.target.closest('[data-scope]');if(b)scopeSet(b.dataset.scope)});
// Promises from your messages, both ways. A still-open one becomes a card when it's due.
// To-dos that look done: one folded group above Done, a short line each (title and what shows it) with Not done and
// Done, and Mark all done. A row opens to the full to-do. Nothing closes without you.
const lookExpanded=new Set();
function lookDoneList(items,open){if(!items.length)return '';
 const row=s=>{const x=lookExpanded.has(s.id),why=doneWhy(s);
  return `<div class="ld-row${x?' open':''}" data-ld="${esc(s.id)}"><button type="button" class="ld-main" data-ld-expand="${esc(s.id)}" aria-expanded="${x}">${CHEVRON}<span class="ld-text"><span class="ld-title" translate="no">${esc(s.title)}</span>${why?`<small class="ld-why">${esc(why)}</small>`:''}</span></button><span class="ld-acts"><button type="button" class="ghost" data-ld-not="${esc(s.id)}">${esc(t('Not done'))}</button><button type="button" data-id="${esc(s.id)}" data-choice="complete">${esc(t('Done'))}</button></span>${x?suggestionCard(s,'Look done'):''}</div>`};
 return `<details id="lookdone-list" ${open?'open':''}><summary id="lookdone-head"><span>${esc(t('Look done'))}</span><span class="count">${items.length}</span></summary><div class="ld-bar"><small>${esc(t('Check these and close them. Nothing closes without you.'))}</small><button type="button" class="ghost" data-ld-all>${esc(t('Mark all done'))}</button></div>${items.map(row).join('')}</details>`}
async function lookAllDone(b){const ids=[...document.querySelectorAll('#lookdone-list [data-ld]')].map(x=>x.dataset.ld);if(!ids.length)return;b.disabled=true;const done=[];
 try{for(const id of ids){await decidePost(id,{choice:'complete',feedback:'',decision_id:crypto.randomUUID()});done.push(id)}}
 catch(err){errCaught(err);toast(err.message,true)}
 finally{await refresh().catch(()=>{});b.disabled=false}
 if(done.length)toast(t(['Marked {} done','Marked {} done'],done.length),false,done.join(','))}
async function lookNotDone(b){const id=b.dataset.ldNot;b.disabled=true;
 try{await decidePost(id,{choice:'not_done',feedback:'',decision_id:crypto.randomUUID()});lookExpanded.delete(id);await refresh();toast(t('Back on your list. I’ll learn from it.'))}
 catch(err){errCaught(err);toast(err.message,true);await refresh().catch(()=>{})}finally{b.disabled=false}}
function promisesList(open){const items=(state.promises||[]).filter(p=>['open','card'].includes(p.state));if(!items.length)return '';
const pday=v=>new Date(v).toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'});
const row=p=>`<div class="promise"><span class="grow">${t(p.together?'With {}:':p.direction==='mine'?'To {}:':'From {}:',`<b>${esc(p.who)}</b>`)} <a class="promise-link" href="${promiseHref(p)}">${esc(p.what)}</a><small>${esc(t(p.direction==='mine'?'You said it {}':'Said {}',pday(p.made_at)))}${p.state==='card'?' · '+esc(t('a to-do now')):p.due?'':' · '+esc(new Date(p.check_at)>Date.now()?t('no date, follow-up {}',pday(p.check_at)):t('no date, checked {}',pday(p.check_at)))}</small></span>${dueChip(p)}${p.state==='open'?`<button type="button" class="quiet" data-promise="${p.id}" data-close="kept" aria-label="${esc(t('Done: {}',p.what))}">Done</button><button type="button" class="quiet" data-promise="${p.id}" data-close="dropped" aria-label="${esc(t('Not needed: {}',p.what))}">Drop</button>`:''}</div>`;
const group=(direction,title)=>{const rows=items.filter(p=>p.direction===direction);return rows.length?`<h3 class="promise-head">${title}<span class="count">${rows.length}</span></h3>`+rows.map(row).join(''):''};
return `<details id="promises-list" ${open?'open':''}><summary id="promises-head"><span>Promises</span><span class="count">${items.length}</span></summary>${group('mine','You promised')}${group('theirs','Promised to you')}</details>`}
