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
function learnedShow(id,what,edit){if(chatId){history.pushState(null,'',location.pathname+location.search);openChatLink()}showTab('feedback','learned');  // Back returns to the chat
const f=(state.facts||[]).find(x=>x.id===id);
 if(edit&&f){learnEdit=id;learnEditText=null}const group=f?(f.kind==='draft'?'rules':'facts'):null;if(group)learnAll.add(group);
 setHTML($('#facts'),learnedList());const row=f?document.getElementById('learned-'+id):null;
 requestAnimationFrame(()=>{(row||$('#facts')).scrollIntoView({block:row?'center':'start'});if(row){row.classList.remove('flash');void row.offsetWidth;row.classList.add('flash')}const t=row?.querySelector('textarea');if(t){t.focus();t.setSelectionRange(t.value.length,t.value.length)}})}
const learnDay=d=>d.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short',...(d.getFullYear()!==new Date().getFullYear()?{year:'numeric'}:{})});  // Tue, Oct 20, as elsewhere
const VOICE_ICON={linkedin:'linkedin',whatsapp:'whatsapp',telegram:'telegram',slack:'slack',email:'gmail',gmail:'gmail',outlook:'gmail',x:'x','x dm':'x',twitter:'x',github:'github'};
// The learning loop's changes (learning_loop.py): what changed, why, and Undo; an undone one stays, marked.
const LEARN_WHAT={voice:c=>`${c.channel==='All'?'Everywhere':c.channel}: how you write`,source:()=>'Fixed at the source',draft:c=>c.before?'Rule changed':'Rule added',fact:c=>c.before?'Fact changed':'Fact added'};
function learnChange(c){const what=(LEARN_WHAT[c.kind]||(()=>'Changed'))(c),text=String((Array.isArray(c.line)?t(...c.line):c.text)||'').split('\n').map(l=>l.trim()).filter(Boolean).join(' · ');
 return html`<div class="change-row${c.undone?html` undone`:''}"><span class="grow"><strong>${what}</strong><span class="change-text">${text}</span>${c.why?html`<small>${c.why}</small>`:''}<small class="change-when">${learnDay(new Date(c.at))}${c.undone?' · Undone':''}</small></span>${c.undone?'':html`<span class="learn-acts"><button type="button" class="quiet" data-learn-undo="${c.id}" aria-label="Undo: ${what}">Undo</button></span>`}</div>`}
// A fact's sort and end day, quietly under it: "Temporary · Until Nov 14". A plain fact without an end shows nothing.
const FACT_SORT={event:'Temporary',commitment:'Commitment',preference:'Preference'};
const factUntil=d=>new Date(d+'T12:00:00').toLocaleDateString(DL,{day:'numeric',month:'short',...(d.slice(0,4)!==String(new Date().getFullYear())?{year:'numeric'}:{})});
function factMeta(f){const bits=[FACT_SORT[f.fact_kind]?t(FACT_SORT[f.fact_kind]):'',f.valid_until?t('Until {}',factUntil(f.valid_until)):'',String(f.source||'').startsWith('ai:')?t('AI: {}',f.source.slice(3)):''].filter(Boolean);return bits.length?html`<small class="fact-meta">${bits.join(' · ')}</small>`:''}
// Learning's sub-tabs, like the Graph's and the Fleet's: How it's going first, then what I learned, the learning loop's
// changes, the decisions, and Team (sharing with The Machine team, votes waiting) only while something waits there. A
// tab with nothing to show is left out; the last one opened is kept on this device. Links: #learning=<tab>, #feedback.
const LEARN_PANES=[['learned','What I’ve learned'],['changes','Changes'],['decisions','Decisions'],['shared','Shared'],['going','How it’s going']];  // Shared: with The Machine team (share asks, votes); #learning=team is its old link
let learnPane=(()=>{try{const v=localStorage.getItem('learn-pane');return v==='team'?'shared':v||'learned'}catch{return 'learned'}})();
const learnTeamWaiting=()=>{const tl=state?.team_learnings;return (tl?.ask?1:0)+(tl?.vote_mode==='ask'?(tl.votes_waiting||[]).length:0)};
function learnHas(id){const s=state||{};
 return id==='going'||id==='learned'&&!!((s.voices||[]).length||(s.facts||[]).length||(s.facts_ended||[]).length||(s.moved||[]).length)||id==='changes'&&!!(s.learning_changes||[]).length
  ||id==='decisions'&&!!(s.decisions||[]).length||id==='shared'&&learnTeamWaiting()>0}
const learnShown=()=>{const ids=LEARN_PANES.map(([id])=>id).filter(learnHas);return ids.includes(learnPane)?learnPane:ids[0]};
// one pane only (a new Machine: How it's going) shows no pill row
function learnTabs(){const box=$('#learn-tabs');if(!box)return;const cur=learnShown(),n=learnTeamWaiting();
 const tabs=html`${LEARN_PANES.filter(([id])=>learnHas(id)).map(([id,label])=>html`<button type="button" role="tab" id="learn-tab-${id}" aria-controls="learn-pane-${id}" data-learn-tab="${id}" aria-selected="${id===cur}"><span class="ell">${t(label)}</span>${id==='shared'&&n?html` <span class="badge">${n}</span>`:''}</button>`)}`;
 if(box.innerHTML!==String(tabs))setHTML(box,tabs);box.hidden=box.childElementCount<2;for(const p of document.querySelectorAll('#feedback [data-learn-pane]'))p.hidden=p.dataset.learnPane!==cur}
function showLearnPane(id){learnPane=id;try{localStorage.setItem('learn-pane',id)}catch{}learnTabs();tabsShow($('#learn-tabs'))}
$('#learn-tabs').addEventListener('click',e=>{const b=e.target.closest('[data-learn-tab]');if(b)showLearnPane(b.dataset.learnTab)});
// Changes: the learning loop's recent changes, newest first, each with Undo; the first few, then Show more
const learnChanges=()=>clipHTML('learn-changes',(state.learning_changes||[]).map(learnChange),'',8);
function learnedList(){
 const facts=state.facts||[],at=x=>x.updated_at||x.created_at||'',newest=(a,b)=>at(b).localeCompare(at(a));
 const mergedUndo=(n,attr,label)=>n?html`<small>Merged from ${notesN(n)} · <button type="button" class="learn-link" ${attr} aria-label="Undo merge: ${label}">Undo merge</button></small>`:'';
 const fact=f=>learnEdit===f.id?html`<div class="fact-row" id="learned-${f.id}"><form class="fact-edit" data-fact-edit="${f.id}"><textarea name="text" maxlength="240" aria-label="Edit what I learned">${learnEditText??f.text}</textarea><span class="learn-acts"><button type="button" class="quiet learn-remove" data-forget="${f.id}" aria-label="Remove: ${f.text}">Remove</button><button type="button" class="quiet" data-edit-cancel>Cancel</button><button type="submit" class="primary">Save</button></span></form></div>`:
  html`<div class="fact-row" id="learned-${f.id}"><span class="grow">${f.text}${factMeta(f)}${mergedUndo(f.merged,html`data-unmerge-fact="${f.id}"`,f.text)}</span><span class="learn-acts"><button type="button" class="quiet" data-edit-fact="${f.id}" aria-label="Edit: ${f.text}">Edit</button><button type="button" class="quiet" data-forget="${f.id}" aria-label="Remove: ${f.text}">Remove</button></span></div>`;
 const voice=v=>{const name=v.channel==='All'?'Everywhere':v.channel,lines=String(v.text||'').split('\n').map(l=>l.trim()).filter(Boolean),open=voiceOpen.has(v.channel),extra=lines.length-2;
  return html`<div class="voice-row" data-channel="${v.channel}">${icon(VOICE_ICON[String(v.channel).toLowerCase()]||'plugin')}<span class="grow"><strong>${name}</strong><ul class="voice-lines">${lines.map((l,i)=>html`<li${i>1&&!open?html` hidden`:''}>${l}</li>`)}</ul>${extra>0?html`<button type="button" class="voice-more" data-voice-more="${v.channel}" aria-expanded="${open}">${open?'Less':extra+' more'}</button>`:''}${mergedUndo(v.merged,html`data-unmerge-voice="${v.channel}"`,v.channel)}</span><span class="learn-acts"><button type="button" class="quiet" data-voice-edit="${v.channel}" aria-label="Edit how you write: ${name}">Edit</button></span></div>`};
 const groups=[['voices','How you write','Per channel, from your messages and notes.',[...(state.voices||[])].sort(newest).map(voice)],
  ['facts','Facts','Things I keep in mind about your work.',facts.filter(f=>f.kind!=='draft').sort(newest).map(fact)],
  ['rules','How to do things','Rules for a kind of task.',facts.filter(f=>f.kind==='draft').sort(newest).map(fact)],
  ['ended','Ended','Past their end date. Bring one back if it still holds.',(state.facts_ended||[]).map(f=>html`<div class="fact-row"><span class="grow">${f.text}${factMeta(f)}</span><span class="learn-acts"><button type="button" class="quiet" data-fact-back="${f.id}" aria-label="${t('Bring back: {}',f.text)}">${t('Bring back')}</button></span></div>`)],
  ['skills','Moved into skills','Notes that now live in a skill.',(state.moved||[]).map(m=>html`<div><span class="grow"><strong>${m.name}</strong> ${notesN(m.notes)}</span><span class="learn-acts"><button type="button" class="quiet" data-unmerge-skill="${m.skill_id}" aria-label="Put back the notes in ${m.name}">Put back</button></span></div>`)]].filter(g=>g[3].length);
 if(!groups.length)return html`<div class="muted">Nothing yet. When a note on a to-do holds beyond it, I keep it here.</div>`;
 const c=state.condensed;
 return html`${c&&c.notes?html`<div class="muted learn-note">Condensed ${notesN(c.notes)} on ${learnDay(new Date(c.at))}.</div>`:''}${
  groups.map(([k,title,blurb,rows])=>{const all=learnAll.has(k)||rows.length<=6;
   return html`<section class="learn-group" data-group="${k}" aria-labelledby="learn-${k}"><div class="learn-head"><h3 id="learn-${k}">${title} <span class="count">${rows.length}</span></h3><p>${blurb}</p></div><div class="list">${all?rows:rows.slice(0,5)}${rows.length>6?html`<button type="button" class="quiet learn-all" data-learn-all="${k}" aria-expanded="${all}">${all?'Show fewer':'Show all '+rows.length}</button>`:''}</div></section>`})}`;
}
// Long lists load a page at a time (Done, the Graph's tabs, its search): 30 rows, the next page by itself as the end
// scrolls near, and a quiet Show more for keyboards, screen readers and when the scroll doesn't tell. A pager keeps what
// it loaded, so a refresh, a tab switch or going back from a card or a person shows the same rows at the same place.
const pagers=new Map();
function pager(key,load,row,rows){let p=pagers.get(key);if(!p){p={key,load,row,rows,items:[],next:'0',total:null,busy:false,failed:false,html:html``};pagers.set(key,p)}else{p.load=load;p.row=row;p.rows=rows}return p}
function pagerDrop(prefix){for(const k of [...pagers.keys()])if(k===prefix||k.startsWith(prefix+':'))pagers.delete(k)}
const pagerSlot=(key,empty='',rows='')=>html`<div class="pager" data-pager="${key}" data-empty="${empty}" data-rows="${rows}"></div>`;
const pagerFoot=p=>p.busy?html`<p class="pager-loading" role="status">Loading…</p>`:p.failed?html`<button type="button" class="quiet more-rows" data-pager-more>Couldn’t load. Try again</button>`:p.next!=null?html`<button type="button" class="quiet more-rows" data-pager-more>Show more</button>`:html``;
function pagerFootPaint(el,p){const empty=!p.items.length&&p.next==null&&!p.busy&&!p.failed;setHTML(el.querySelector('.pager-foot'),empty&&el.dataset.empty?html`<p class="muted pager-empty">${el.dataset.empty}</p>`:pagerFoot(p))}
function pagerMount(root=document){for(const el of root.querySelectorAll('[data-pager]')){const p=pagers.get(el.dataset.pager);if(!p)continue;
 if(!el.firstChild){if(p.rows)p.html=p.rows(p.items);setHTML(el,html`<div class="pager-rows ${el.dataset.rows||''}">${p.html}</div><div class="pager-foot"></div>`);pagerSeen.observe(el.querySelector('.pager-foot'));detailsSync(el)}pagerFootPaint(el,p)}}
const pagerNear=el=>{const f=el.querySelector('.pager-foot');if(!f||!el.offsetParent)return false;const r=f.getBoundingClientRect(),box=el.closest('.side-cards,.chat-side');return r.top<innerHeight+600&&r.bottom>-600&&!box};
function pagerMore(key){const p=pagers.get(key);if(!p||p.next==null&&!p.busy)return Promise.resolve();if(p.busy)return p.pending;return p.pending=pagerLoad(key,p)}
async function pagerLoad(key,p,paint=true){p.busy=true;p.failed=false;const els=()=>paint?[...document.querySelectorAll('[data-pager]')].filter(e=>e.dataset.pager===key):[];
 for(const el of els())pagerFootPaint(el,p);let fresh='';
 try{const r=await p.load(p.next);if(pagers.get(key)!==p)return;const have=new Set(p.items.map(x=>x?.id).filter(Boolean));r.items=r.items.filter(x=>!x?.id||!have.has(x.id));p.items.push(...r.items);if(p.rows){p.html=p.rows(p.items);fresh=r.items.length?null:''}else{fresh=orEmpty(html`${r.items.map(x=>p.row(x))}`);p.html=html`${p.html}${fresh}`}p.next=r.next??null;p.total=r.total??p.total;p.onload?.(r.items)}catch{p.failed=true}finally{p.busy=false}
 for(const el of els()){const rows=el.querySelector('.pager-rows');if(fresh===null){if(rows)setHTML(rows,p.html)}else rows?.append(htmlNodes(fresh));pagerFootPaint(el,p)}
 if(fresh)requestAnimationFrame(()=>{for(const el of els())if(pagerNear(el)){pagerMore(key);break}})}
const pagerSeen=new IntersectionObserver(es=>{for(const e of es)if(e.isIntersecting){const el=e.target.closest('[data-pager]');if(el&&pagerNear(el))pagerMore(el.dataset.pager)}},{rootMargin:'0px 0px 600px 0px'});
document.addEventListener('click',e=>{const b=e.target.closest('[data-pager-more]');if(!b)return;e.preventDefault();e.stopPropagation();const el=b.closest('[data-pager]'),p=pagers.get(el?.dataset.pager);if(p?.failed)p.failed=false;if(el)pagerMore(el.dataset.pager)},true);
// Done cards beyond the status payload: those loaded join the cards the page knows, so a chat or an action finds them
const doneExtra=new Map();
const closedAt=s=>s.closed_at||(state?.decisions||[]).filter(d=>d.suggestion_id===s.id&&['complete','reject'].includes(d.choice)).map(d=>d.created_at).sort().at(-1)||s.created_at;
// A to-do that looks done sits in Done by when it started to (the Machine's looks_done_at, else the sign's own time)
const lookAt=s=>{try{const h=JSON.parse(s.handled_hint||'null');if(h?.at)return h.at}catch{}return s.looks_done_at||s.created_at};
const doneAt=s=>looksDone(s)?lookAt(s):closedAt(s);
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
function sideRow(x,cur){const here=id=>id===cur?html` aria-current="page"`:'';
 if(x.fleet)return html`<a href="#${x.fleet}" data-side-fleet="${x.fleet}" title="${x.title}" translate="no">${x.title}</a>`;  // a Fleet item (fleetSide)
 if(x.fuGroup)return x.writing?html`<a href="#" data-fu-card="${x.fuGroup}" title="${x.title}" translate="no">${x.title}</a>`:html`<a href="#" data-fu-review="${x.fuGroup}" title="${x.title}" translate="no">${x.title}</a>`;
 if(x.fuFold){const open=doneOpen.has(x.fuFold);
  const n=doneFoldSkipped(x);
  return html`<button type="button" class="done-fold" data-done-fold="${x.fuFold}" aria-expanded="${open}" title="${[x.title,n].filter(Boolean).join(' · ')}"><span translate="no">${x.title}</span>${n?html`<small>${n}</small>`:''}${raw(CHEVRON)}</button>${
   open?html`<div class="done-fold-list">${x.items.map(s=>html`<a href="#chat=${s.id}" title="${s.title}"${here(s.id)}><span translate="no">${frName(s.follow_up)}</span><small>${[doneFoldWho(s),doneFoldWhen(s)].filter(Boolean).join(' · ')}</small></a>`)}</div>`:''}`}
 if(looksDone(x))return html`<a href="#chat=${x.id}" class="side-ld" title="${x.title}"${here(x.id)}><span translate="no">${x.title}</span><small>${t('Looks done')}</small></a>`;  // at the top of Done, still open
 return html`<a href="#chat=${x.id}" title="${x.title}" translate="no"${here(x.id)}>${x.title}</a>`}
// The Done list on the Suggestions page: the same fold, a quiet to-do that opens to the list
// Done reads newest first by when each one closed, the ones that look done among them by when they started to (doneAt):
// one just sent is at the top. A looks-done one older than the loaded part waits until that part is loaded.
const lookDoneNow=()=>(state?.suggestions||[]).filter(s=>looksDone(s)&&(scopeFilter==='all'||s.scope===scopeFilter));
function doneRows(items){const p=pagers.get(doneKey()),last=p?.next!=null&&items.length?doneAt(items.at(-1)):'',looks=lookDoneNow().filter(s=>doneAt(s)>=last);
 const rows=[...looks,...doneFold(items)].sort((a,b)=>doneAt(b).localeCompare(doneAt(a)));
 return html`${rows.map(x=>x.fuFold?doneFoldCard(x):looksDone(x)?lookDoneCard(x):suggestionCard(x))}`}
function doneFoldCard(g){const open=donePageOpen.has(g.fuFold);
 return html`<article class="card todo t-faint fu-done" id="${g.id.replace(/[^\w-]/g,'-')}" data-status="completed"><details data-done-fold-card="${g.fuFold}"${open?html` open`:''}><summary><h3 translate="no">${g.title}</h3>${doneFoldSkipped(g)?html`<span class="done-fold-n">${doneFoldSkipped(g)}</span>`:''}<span class="meta-side">${time(g.closed_at,true)}</span></summary><ul class="fu-done-list">${g.items.map(s=>html`<li><a href="#chat=${s.id}" translate="no">${frName(s.follow_up)}</a><span>${doneFoldWho(s)}</span><span class="muted">${doneFoldWhen(s)}</span></li>`)}</ul></details></article>`}
document.addEventListener('click',e=>{const b=e.target.closest('[data-done-fold]');if(!b)return;e.preventDefault();const k=b.dataset.doneFold;doneOpen.has(k)?doneOpen.delete(k):doneOpen.add(k);const inSide=!!b.closest('#side-cards');sideCards();if(chatOpen())render();
 (inSide?$('#side-cards'):document).querySelector(`[data-done-fold="${CSS.escape(k)}"]`)?.focus()});
document.addEventListener('toggle',e=>{const d=e.target;if(!d.matches?.('[data-done-fold-card]'))return;d.open?donePageOpen.add(d.dataset.doneFoldCard):donePageOpen.delete(d.dataset.doneFoldCard)},true);
function cardsMerge(){if(!state?.suggestions)return;const ids=new Set(state.suggestions.map(s=>s.id));for(const c of doneExtra.values())if(!ids.has(c.id))state.suggestions.push(c)}
let doneSeen='';  // done counts and ids as last shown: when they change, the Done lists start over from the top
const listShown={};const clipList=(id,rows,empty,n=3)=>{const k=listShown[id]||n;return rows.length?html`${rows.slice(0,k)}${rows.length>k?html`<button type="button" class="quiet more-rows" data-more="${id}" data-shown="${k}">Show ${Math.min(10,rows.length-k)} more</button>`:''}`:empty};
// clipList for html`` rows
const clipHTML=(id,rows,empty,n=3)=>{const k=listShown[id]||n;return rows.length?html`${rows.slice(0,k)}${rows.length>k?html`<button type="button" class="quiet more-rows" data-more="${id}" data-shown="${k}">Show ${Math.min(10,rows.length-k)} more</button>`:''}`:html`${empty}`};
// clipList as nodes: the first rows, then Show more; `empty` gives the nodes for no rows
const clipNodes=(id,rows,empty,n=3)=>{const k=listShown[id]||n;return rows.length?[...rows.slice(0,k),...rows.length>k?[make('button',{type:'button',class:'quiet more-rows','data-more':id,'data-shown':k},`Show ${Math.min(10,rows.length-k)} more`)]:[]]:empty()};
document.addEventListener('click',e=>{const b=e.target.closest('[data-more]');if(!b)return;listShown[b.dataset.more]=(Number(b.dataset.shown)||listShown[b.dataset.more]||3)+10;render()});
document.addEventListener('click',async e=>{const b=e.target.closest('[data-promise]');if(!b)return;b.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'promise_close',args:{id:Number(b.dataset.promise),status:b.dataset.close}})});toast(b.dataset.close==='kept'?'Marked done.':'Dropped.');refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#facts').addEventListener('click',async e=>{const vm=e.target.closest('[data-voice-more]');if(vm){const ch=vm.dataset.voiceMore,open=!voiceOpen.has(ch);open?voiceOpen.add(ch):voiceOpen.delete(ch);setHTML($('#facts'),learnedList());$(`#facts [data-voice-more="${CSS.escape(ch)}"]`)?.focus();return}
 const la=e.target.closest('[data-learn-all]');if(la){const k=la.dataset.learnAll;learnAll.has(k)?learnAll.delete(k):learnAll.add(k);setHTML($('#facts'),learnedList());$(`#facts [data-learn-all="${k}"]`)?.focus();return}
 const fb=e.target.closest('[data-fact-back]');if(fb){fb.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'unmerge_fact',args:{expired:Number(fb.dataset.factBack)}})});toast(t('Brought back.'));refresh()}catch(err){errCaught(err);fb.disabled=false;toast(err.message,true)}return}
 const u=e.target.closest('[data-unmerge-fact],[data-unmerge-voice],[data-unmerge-skill]');if(u){u.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'unmerge_fact',args:u.dataset.unmergeSkill?{skill:u.dataset.unmergeSkill}:u.dataset.unmergeVoice?{channel:u.dataset.unmergeVoice}:{id:Number(u.dataset.unmergeFact)}})});toast('Notes restored.');refresh()}catch(err){errCaught(err);u.disabled=false;toast(err.message,true)}return}
 const ed=e.target.closest('[data-edit-fact]');if(ed){learnEdit=Number(ed.dataset.editFact);learnEditText=null;setHTML($('#facts'),learnedList());const t=$(`#learned-${learnEdit} textarea`);t?.focus();t?.setSelectionRange(t.value.length,t.value.length);return}
 if(e.target.closest('[data-edit-cancel]')){const id=learnEdit;learnEdit=learnEditText=null;setHTML($('#facts'),learnedList());$(`#facts [data-edit-fact="${id}"]`)?.focus();return}
 const b=e.target.closest('[data-forget]');if(!b)return;b.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'forget_fact',args:{id:Number(b.dataset.forget)}})});if(learnEdit===Number(b.dataset.forget))learnEdit=learnEditText=null;toast('Removed.');refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#learn-changes').addEventListener('click',async e=>{const lu=e.target.closest('[data-learn-undo]');if(!lu)return;lu.disabled=true;
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'learning_undo',args:{id:Number(lu.dataset.learnUndo)}})});toast('Undone.');refresh()}catch(err){errCaught(err);lu.disabled=false;toast(err.message,true)}});
$('#facts').addEventListener('input',e=>{if(e.target.closest('[data-fact-edit]'))learnEditText=e.target.value});
$('#facts').addEventListener('keydown',e=>{if(e.key==='Escape'&&e.target.closest('[data-fact-edit]'))e.target.closest('form').querySelector('[data-edit-cancel]').click()});
$('#facts').addEventListener('submit',async e=>{const form=e.target.closest('[data-fact-edit]');if(!form)return;e.preventDefault();const id=Number(form.dataset.factEdit),text=form.text.value.trim(),save=form.querySelector('[type=submit]');save.disabled=true;
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'edit_fact',args:{id,text}})});const f=(state.facts||[]).find(x=>x.id===id);if(f)f.text=text;learnEdit=learnEditText=null;setHTML($('#facts'),learnedList());toast('Saved.');refresh()}catch(err){errCaught(err);save.disabled=false;toast(err.message,true)}});
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
const scopeNote=empty=>scopeFilter==='all'?'':html`<p class="scope-note" role="status"><span>${scopeFilter==='work'?(empty?'No work to-dos':'Work only'):(empty?'No personal to-dos':'Personal only')}</span> · <button type="button" class="link" data-scope="all">Show all</button></p>`;
$('#suggestions').addEventListener('click',e=>{const b=e.target.closest('.scope-note [data-scope]');if(b){e.stopPropagation();scopeSet(b.dataset.scope)}});
let linkedCardId=null;
$('#suggestion-stats').addEventListener('click',e=>{const t=e.target.closest('[data-fold-tile]');if(t)toggleSection(t.dataset.foldTile)});
$('#suggestion-summary').addEventListener('click',e=>{const b=e.target.closest('[data-scope]');if(b)scopeSet(b.dataset.scope)});
// Promises from your messages, both ways. A still-open one becomes a card when it's due.
// To-dos that look done: at the top of Done / dismissed, each like a done one there: "Looks done" where that says Done,
// what shows it as its line, Details, Chat and Reopen (not_done: back on the list). They stay open until the owner closes them.
const lookExpanded=new Set();  // a link to one opens Done (openCardLink)
const LD_CLASS='looks-done';
function lookDoneCard(s){
 return htmlEdit(suggestionCard({...s,status:'completed',body:doneWhy(s)||s.body,handled_hint:null,outcome:null,undo_until:null,expired_at:null}),c=>{
  [...c.querySelectorAll('[class]')].find(n=>/(^| )is-closed$/.test(n.getAttribute('class')))?.classList.add(LD_CLASS);c.querySelector('[data-status="completed"]')?.setAttribute('data-status',s.status);
  const ct=c.querySelector('span[class="ct"]');if(ct&&!ct.children.length){ct.textContent=t('Looks done {}',ago(lookAt(s)));ct.parentElement.title=date(lookAt(s))}
  for(const b of c.querySelectorAll('[data-choice="reopen"],[data-choice="undo"]')){b.removeAttribute('data-choice');b.setAttribute('data-ld-not',s.id)}})}
async function lookNotDone(b){const id=b.dataset.ldNot;b.disabled=true;
 try{await decidePost(id,{choice:'not_done',feedback:'',decision_id:crypto.randomUUID()});lookExpanded.delete(id);await refresh();toast(t('Back on your list. I’ll learn from it.'))}
 catch(err){errCaught(err);toast(err.message,true);await refresh().catch(()=>{})}finally{b.disabled=false}}
function promisesList(open){const items=(state.promises||[]).filter(p=>['open','card'].includes(p.state));if(!items.length)return '';
const pday=v=>new Date(v).toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'});
const row=p=>html`<div class="promise"><span class="grow">${htmlT(p.together?'With {}:':p.direction==='mine'?'To {}:':'From {}:',html`<b>${p.who}</b>`)} <a class="promise-link" href="${promiseHref(p)}">${p.what}</a><small>${t(p.direction==='mine'?'You said it {}':'Said {}',pday(p.made_at))}${p.state==='card'&&p.suggestion_id?html` · <a class="promise-todo" href="#chat=${p.suggestion_id}">${t('a to-do now')}</a>`:p.due?'':' · '+(new Date(p.check_at)>Date.now()?t('no date, follow-up {}',pday(p.check_at)):t('no date, checked {}',pday(p.check_at)))}</small></span>${dueChip(p)}${['open','card'].includes(p.state)?html`<button type="button" class="quiet" data-promise="${p.id}" data-close="kept" aria-label="${t('Done: {}',p.what)}">Done</button><button type="button" class="quiet" data-promise="${p.id}" data-close="dropped" aria-label="${t('Not needed: {}',p.what)}">Drop</button>`:''}</div>`;
const group=(direction,title)=>{const rows=items.filter(p=>p.direction===direction);return rows.length?html`<h3 class="promise-head">${title}<span class="count">${rows.length}</span></h3>${rows.map(row)}`:''};
return html`<details id="promises-list" ${open?'open':''}><summary id="promises-head"><span>Promises</span><span class="count">${items.length}</span></summary>${group('mine','You promised')}${group('theirs','Promised to you')}</details>`}
