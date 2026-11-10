// Missed to-dos (Learning, How it's going): the weekly check of messages that got no to-do (missed_work.py). One
// number (the share that likely needed one, with its range), the misses it found to check (each opens the message and
// takes the owner's Real miss or Not a miss, kept on this Machine).
const MW_CHANNEL={email:'Email',message:'Message',meeting:'Meeting'};
const mwPct=v=>v==null?null:Math.round(100*v);
const mwUrl=u=>typeof u==='string'&&/^https:\/\//.test(u)?u:null;  // only https links open, like the server keeps them
function missedNodes(m){if(!m)return [];const est=m.adjusted||m.raw;if(!est||est.rate==null)return [];
 const day=localeDate(new Date(m.at),DL,{day:'numeric',month:'short'});
 const row=x=>{const url=mwUrl(x.url),id=Number(x.event_id);return make('div',{class:'mw-row'},make('span',{class:'grow'},make('small',{},t(MW_CHANNEL[x.channel]||'Message')+' · '+(x.area==='Personal'?t('Personal'):x.area??'')),x.reason||''),
  make('span',{class:'mw-acts'},url?make('a',{href:url,target:'_blank',rel:'noopener noreferrer'},t('Open')):'',
   make('button',{type:'button','data-mw-label':'real','data-mw-id':id,'aria-pressed':x.label==='real'},t('Real miss')),
   make('button',{type:'button','data-mw-label':'not','data-mw-id':id,'aria-pressed':x.label==='not'},t('Not a miss'))))};

 return [make('h3',{class:'q-h'},t('Missed to-dos')),make('p',{class:'learn-intro'},t('Each week I check a sample of messages that got no to-do. Last check {}.',day)),
  make('div',{class:'q-tiles mw-tiles'},qTile(mwPct(est.rate),'Likely missed',t(['Of {} message with no to-do','Of {} messages with no to-do'],Number(m.population||0).toLocaleString(DL)),make('small',{class:'q-was'},t('Between {}% and {}%',mwPct(est.low),mwPct(est.high))))),
  ...m.misses?.length?[make('div',{class:'list mw-list'},m.misses.map(row))]:[]]}
// How it's going and Missed to-dos, drawn again from state
const renderQuality=()=>$('#quality').replaceChildren(...qualityNodes(state.quality),...missedNodes(state.missed_work));
$('#quality').addEventListener('click',async e=>{const b=e.target.closest('[data-mw-label]');if(!b)return;const on=b.getAttribute('aria-pressed')==='true';b.disabled=true;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'missed_work_label',args:{event_id:Number(b.dataset.mwId),label:on?'':b.dataset.mwLabel}})});
  state.missed_work=r.missed_work;renderQuality()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
// Long history lists show the latest few; Show more adds ten at a time and survives the refresh.
const notesN=n=>`${n} note${n===1?'':'s'}`;
// Open one learning on What I've learned (from a card's chat): its block unfolded, the row in view and lit; with edit, its editor open.
function learnedShow(id,what,edit){const f=(state.facts||[]).find(x=>x.id===id);if(f?.about?.length)return recordFactShow(f.about[0].id,edit?id:null);  // it lives on that record's page
 if(chatId){history.pushState(null,'',location.pathname+location.search);openChatLink()}showTab('feedback','learned');  // Back returns to the chat
 if(edit&&f){learnEdit=id;learnEditText=null}const group=f?(f.kind==='draft'?'rules':'facts'):null;if(group)learnAll.add(group);
 setHTML($('#facts'),learnedList());const row=f?document.getElementById('learned-'+id):null;
 requestAnimationFrame(()=>{(row||$('#facts')).scrollIntoView({block:row?'center':'start'});if(row){row.classList.remove('flash');void row.offsetWidth;row.classList.add('flash')}const t=row?.querySelector('textarea');if(t){t.focus();t.setSelectionRange(t.value.length,t.value.length)}})}
const learnDay=d=>localeDate(d,DL,{weekday:'short',day:'numeric',month:'short',...(d.getFullYear()!==new Date().getFullYear()?{year:'numeric'}:{})});  // Tue, Oct 20, as elsewhere
const VOICE_ICON={linkedin:'linkedin',whatsapp:'whatsapp',telegram:'telegram',slack:'slack',email:'gmail',gmail:'gmail',outlook:'gmail',x:'x','x dm':'x',twitter:'x',github:'github'};
// The learning loop's changes (learning_loop.py): what changed, why, and Undo; an undone one stays, marked.
const LEARN_WHAT={voice:c=>`${c.channel==='All'?'Everywhere':c.channel}: how you write`,source:()=>'Fixed at the source',draft:c=>c.before?'Rule changed':'Rule added',fact:c=>c.before?'Fact changed':'Fact added',learned:()=>'Marked not right',about:()=>'Facts linked'};
function learnChange(c){const what=(LEARN_WHAT[c.kind]||(()=>'Changed'))(c),text=String((Array.isArray(c.line)?t(...c.line):c.text)||'').split('\n').map(l=>l.trim()).filter(Boolean).join(' · ');
 return html`<div class="change-row${c.undone?html` undone`:''}"><span class="grow"><strong>${what}</strong><span class="change-text">${text}</span>${c.why?html`<small>${c.why}</small>`:''}<small class="change-when">${learnDay(new Date(c.at))}${c.undone?' · Undone':''}</small></span>${c.undone?'':html`<span class="learn-acts"><button type="button" class="quiet" data-learn-undo="${c.id}" aria-label="Undo: ${what}">Undo</button></span>`}</div>`}
const learnTeamWaiting=()=>{const tl=state?.team_learnings;return (tl?.ask?1:0)+(tl?.vote_mode==='ask'?(tl.votes_waiting||[]).length:0)};
function learnHas(id){const s=state||{};
 return id==='going'||id==='learned'&&!!((s.voices||[]).length||(s.facts||[]).length||(s.facts_ended||[]).length||(s.facts_aside||[]).length||(s.moved||[]).length||(s.bring_in||[]).length)||id==='changes'&&!!(s.learning_changes||[]).length
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
 // Facts about a person, organization or project live on its Graph page: one quiet line under Facts says how many,
 // and opens to the records, each a link with its count
 const onPages=new Map();for(const f of facts)if(f.kind!=='draft')for(const a of f.about||[]){const r=onPages.get(a.id)||{...a,n:0};r.n++;onPages.set(a.id,r)}
 const paged=facts.filter(f=>f.kind!=='draft'&&f.about?.length).length,pages=[...onPages.values()].sort((a,b)=>b.n-a.n||String(a.name).localeCompare(String(b.name)));
 const pagesLine=paged?html`<details class="learn-pages"><summary>${t(['{} fact lives on a Graph page','{} facts live on Graph pages'],paged)}</summary><p>${pages.map(r=>html`<a href="${graphHash(r.id)}">${r.name}<span class="count">${r.n}</span></a>`)}</p></details>`:'';
 const fact=f=>learnEdit===f.id?html`<div class="fact-row" id="learned-${f.id}"><form class="fact-edit" data-fact-edit="${f.id}"><textarea name="text" maxlength="240" aria-label="Edit what I learned">${learnEditText??f.text}</textarea><span class="learn-acts"><button type="button" class="quiet learn-remove" data-forget="${f.id}" aria-label="Remove: ${f.text}">Remove</button><button type="button" class="quiet" data-edit-cancel>Cancel</button><button type="submit" class="primary">Save</button></span></form></div>`:
  html`<div class="fact-row" id="learned-${f.id}"><span class="grow">${f.text}${factMeta(f)}${mergedUndo(f.merged,html`data-unmerge-fact="${f.id}"`,f.text)}</span><span class="learn-acts"><button type="button" class="quiet" data-edit-fact="${f.id}" aria-label="Edit: ${f.text}">Edit</button><button type="button" class="quiet" data-forget="${f.id}" aria-label="Remove: ${f.text}">Remove</button></span></div>`;
 const voice=v=>{const name=v.channel==='All'?'Everywhere':v.channel,lines=String(v.text||'').split('\n').map(l=>l.trim()).filter(Boolean),open=voiceOpen.has(v.channel),extra=lines.length-2;
  return html`<div class="voice-row" data-channel="${v.channel}">${icon(VOICE_ICON[String(v.channel).toLowerCase()]||'plugin')}<span class="grow"><strong>${name}</strong><ul class="voice-lines">${lines.map((l,i)=>html`<li${i>1&&!open?html` hidden`:''}>${l}</li>`)}</ul>${extra>0?html`<button type="button" class="voice-more" data-voice-more="${v.channel}" aria-expanded="${open}">${open?'Less':extra+' more'}</button>`:''}${mergedUndo(v.merged,html`data-unmerge-voice="${v.channel}"`,v.channel)}</span><span class="learn-acts"><button type="button" class="quiet" data-voice-edit="${v.channel}" aria-label="Edit how you write: ${name}">Edit</button></span></div>`};
 const groups=[['voices','How you write','Per channel, from your messages and notes.',[...(state.voices||[])].sort(newest).map(voice)],
  ['facts','Facts','About you and how you work.',facts.filter(f=>f.kind!=='draft'&&!f.about?.length).sort(newest).map(fact),pagesLine],
  ['rules','How to do things','Rules for a kind of task.',facts.filter(f=>f.kind==='draft').sort(newest).map(fact)],
  ['ended','Ended','Past their end date. Bring one back if it still holds.',(state.facts_ended||[]).map(f=>html`<div class="fact-row"><span class="grow">${f.text}${factMeta(f)}</span><span class="learn-acts"><button type="button" class="quiet" data-fact-back="${f.id}" aria-label="${t('Bring back: {}',f.text)}">${t('Bring back')}</button></span></div>`)],
  ['aside','Set aside','Not used lately, to make room. Bring one back if it still holds.',(state.facts_aside||[]).map(f=>html`<div class="fact-row"><span class="grow">${f.text}${factMeta(f)}</span><span class="learn-acts"><button type="button" class="quiet" data-fact-back="${f.id}" aria-label="${t('Bring back: {}',f.text)}">${t('Bring back')}</button></span></div>`)],
  ['skills','Moved into skills','Notes that now live in a skill.',(state.moved||[]).map(m=>html`<div><span class="grow"><strong>${m.name}</strong> ${notesN(m.notes)}</span><span class="learn-acts"><button type="button" class="quiet" data-unmerge-skill="${m.skill_id}" aria-label="Put back the notes in ${m.name}">Put back</button></span></div>`)]].filter(g=>g[3].length||g[4]);
 const bring=bringSection();  // lines of their OpenClaw notes to tick (learning-bring.js); nothing when there are none
 if(!groups.length&&!bring)return html`<div class="muted">Nothing yet. When a note on a to-do holds beyond it, I keep it here.</div>`;
 const c=state.condensed;
 return html`${bring}${c&&c.notes?html`<div class="muted learn-note">Condensed ${notesN(c.notes)} on ${learnDay(new Date(c.at))}.</div>`:''}${
  groups.map(([k,title,blurb,rows,foot])=>{const all=learnAll.has(k)||rows.length<=6;
   return html`<section class="learn-group" data-group="${k}" aria-labelledby="learn-${k}"><div class="learn-head"><h3 id="learn-${k}">${title} <span class="count">${rows.length}</span></h3><p>${blurb}</p></div>${rows.length?html`<div class="list">${all?rows:rows.slice(0,5)}${rows.length>6?html`<button type="button" class="quiet learn-all" data-learn-all="${k}" aria-expanded="${all}">${all?'Show fewer':'Show all '+rows.length}</button>`:''}</div>`:''}${foot||''}</section>`})}`;
}
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
// Served as a part that loads when first needed (dashboard_parts.LAZY): a page drawn before it came draws Learning's
// own parts now (render skipped them)
if(drawnWhole)try{renderQuality();if(learnEdit==null)setHTML($('#facts'),learnedList());setHTML($('#learn-changes'),learnChanges());learnTabs()}catch(e){errCaught(e);console.error(e)}
