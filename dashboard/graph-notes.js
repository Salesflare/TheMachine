// Notes in the Graph (note_pages.py): the readable overview of one subject. Graph › Notes lists them as a tree, folded
// (the ones the owner opened stay open on this device); a note's page (#graph/note:<id>) shows where it sits, its lines
// with where each came from, the notes under it and Linked from. The owner adds and edits lines, renames, moves, merges
// and deletes notes (each with Undo); a line can name a person, organization, project or another note: type @ and a
// name, pick one, and it shows as a plain link. Nothing here sends anything, and notes stay on this Machine.
let noteList=null,noteEditing=null,noteAdding=false,noteFind=0;
const notesOpen=new Set((()=>{try{return JSON.parse(sideStore.get('notes-open')||'[]')}catch{return[]}})());
const NOTE_KIND={trip:'Trip'};
const noteDay=v=>v?shortDay(String(v).slice(0,10)):'';
const noteDates=x=>x.starts?(x.ends&&x.ends!==x.starts?t('{} to {}',noteDay(x.starts),noteDay(x.ends)):noteDay(x.starts)):'';
const noteMeta=x=>[NOTE_KIND[x.kind]?t(NOTE_KIND[x.kind]):'',noteDates(x),x.lines?t(['{} line','{} lines'],x.lines):x.children?t(['{} note','{} notes'],x.children):''].filter(Boolean).join(' · ');
const noteRow=(x,fold='')=>html`<article class="tap note-item" data-node="${x.id}"${fold?html` data-depth="${Math.min(x.depth,6)}"`:''}>${fold}<div class="graph-row one">${nodeButton(x)}<small>${noteMeta(x)}</small></div></article>`;
const noteTitleForm=(cls,parent,shown)=>html`<form class="note-form ${cls}"${parent?html` data-note-parent="${parent}"`:''}${shown?'':html` hidden`}><input name="title" maxlength="120" required aria-label="${t('Title')}" placeholder="${t('Title')}" autocomplete="off"><span class="note-acts"><button type="button" class="quiet" data-note-cancel>${t('Cancel')}</button><button class="primary">${t('Start the note')}</button></span></form>`;
// The list: each note after the one it is under; a note's own notes show once it is unfolded
function notesPane(notes){if(notes)noteList=notes;else if(!noteList){request('api/graph').then(g=>{noteList=g.notes||[];people(graphNode,true)}).catch(errCaught);return html`<p class="pager-loading" role="status">Loading…</p>`}
 const shown=[];let hideBelow=Infinity;
 for(const x of noteList){if(x.depth>hideBelow)continue;hideBelow=x.children&&!notesOpen.has(x.id)?x.depth:Infinity;shown.push(x)}
 const add=noteTitleForm('note-new-form','',noteNewPending);noteNewPending=false;
 if(!noteList.length)return html`${add}<div class="empty all-clear graph-empty"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>${t('No notes yet.')}</strong><span class="poke-line">${t('The Machine starts notes like trips from your messages. Or start one with New note.')}</span></div></div>`;
 return html`${add}<div class="graph-list note-tree">${shown.map(x=>{const open=notesOpen.has(x.id);return noteRow(x,x.children?html`<button type="button" class="note-fold" data-note-fold="${x.id}" aria-expanded="${open}" aria-label="${open?t('Hide the notes under {}',x.name):t('Show the notes under {}',x.name)}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>`:html`<span class="note-fold" aria-hidden="true"></span>`)})}</div>`}
// New note (the head's button on Graph › Notes, the top bar's + on a phone, the palette): a title is all it takes,
// then its page opens. From elsewhere it opens Notes first.
let noteNewPending=false;
function noteNew(){const find=()=>$('#people-view [data-graph-panel="notes"]:not([hidden]) .note-new-form'),show=f=>{f.hidden=false;f.elements.title.focus()},f=find();if(f&&!$('#people').hidden&&!graphNode)return show(f);
 noteNewPending=true;$('.side-sub a[data-graph-sub="notes"]')?.click();let tries=0;const wait=()=>{const f=find();if(f&&!f.hidden)return f.elements.title.focus();if(f&&noteNewPending){noteNewPending=false;return show(f)}if(++tries<60)setTimeout(wait,50)};wait()}
// A line's words with its links: each name a link to its page, the rest plain words
function noteText(x){const text=x.text,low=text.toLowerCase(),spots=[];
 for(const l of x.links||[]){const i=low.indexOf(l.name.toLowerCase());if(i>=0&&!spots.some(s=>i<s.end&&i+l.name.length>s.i))spots.push({i,end:i+l.name.length,id:l.id})}
 spots.sort((a,b)=>a.i-b.i);const out=[];let at=0;for(const s of spots){out.push(text.slice(at,s.i),html`<a href="${graphHash(s.id)}" class="note-link">${text.slice(s.i,s.end)}</a>`);at=s.end}out.push(text.slice(at));return out}
const noteWhen=v=>v?html`<time datetime="${v}">${noteDay(v)}${String(v).length>10?' '+fmtHM(new Date(v)):''}</time>`:'';
const noteSource=x=>x.source?.gone?html`<small class="note-src">${t('From a message that is gone')}</small>`
 :x.source?html`<small class="note-src"><button type="button" class="link" data-note-src="${x.source.id}" data-kind="${x.source.kind}" data-title="${x.source.title}">${t('From {}',x.source.title||t('a message'))}</button></small>`
 :x.fact_id?html`<small class="note-src">${t('From what I learned')}</small>`:'';
const noteLineForm=x=>html`<form class="note-form note-line-form" data-note-line="${x.id}" data-links="${JSON.stringify(x.links||[])}"><textarea name="text" maxlength="${x.fact_id?240:1000}" rows="2" required aria-label="${t('Line')}">${x.text}</textarea><span class="note-acts"><button type="button" class="quiet" data-note-cancel>${t('Cancel')}</button><button class="primary">${t('Save')}</button></span></form>`;
function noteLine(x){if(noteEditing===x.id)return html`<li>${noteLineForm(x)}</li>`;
 const menu=html`<details class="fact-menu"><summary aria-label="${t('Options for this line')}" title="${t('Options')}">⋯</summary><div class="fact-menu-list" role="menu"><button type="button" role="menuitem" data-note-line-edit="${x.id}">${t('Edit')}${x.fact_id?html`<small>${t('Also changes it under What I’ve learned')}</small>`:''}</button>${x.edited?html`<button type="button" role="menuitem" data-note-line-reset="${x.id}">${t('Back to the original')}</button>`:''}<button type="button" role="menuitem" class="danger" data-note-line-remove="${x.id}">${t('Remove')}</button></div></details>`;
 return html`<li>${noteWhen(x.at)}<span class="note-text">${noteText(x)}${noteSource(x)}</span>${menu}</li>`}
// Is note b somewhere under note a (so a can't go under b, or into it)?
function noteBelow(a,b){const by=new Map((noteList||[]).map(x=>[x.id,x]));for(let x=by.get(b),i=0;x&&i<8;x=by.get(x.parent),i++)if(x.parent===a)return true;return false}
const noteOptions=(list,picked)=>list.map(x=>html`<option value="${x.id}"${x.id===picked?html` selected`:''}>${'  '.repeat(x.depth||0)}${x.name}</option>`);
let noteFor='';
function notePage(n){if(n.tree)noteList=n.tree;if(noteFor!==n.id){noteFor=n.id;noteAdding=false;noteEditing=null}const areas=n.areas||[],label=areas.find(x=>x.id===n.area)?.label||'',kids=n.children||[],lines=n.lines||[];
 const crumbs=html`<div class="graph-crumbs" role="navigation" aria-label="Breadcrumb"><a href="#graph" data-crumb="">Graph</a><span aria-hidden="true">›</span><a href="#graph=notes" data-crumb="notes">Notes</a>${(n.path||[]).map(p=>html`<span aria-hidden="true">›</span><a href="${graphHash(p.id)}">${p.name}</a>`)}<span aria-hidden="true">›</span><span aria-current="page">${n.name}</span></div>`;
 const sub=[NOTE_KIND[n.kind]?t(NOTE_KIND[n.kind]):'',noteDates(n),areas.length>1?label:'',n.by==='owner'?'':t('Kept up to date by The Machine')].filter(Boolean).join(' · ');
 const menu=html`<details class="fact-menu person-menu"><summary aria-label="${t('More for this note')}" title="${t('More')}">⋯</summary><div class="fact-menu-list" role="menu"><button type="button" role="menuitem" data-note-child>${t('New note under this one')}</button><button type="button" role="menuitem" data-note-merge-open>${t('Merge into…')}</button><button type="button" role="menuitem" class="danger" data-note-delete>${t('Delete')}</button></div></details>`;
 const others=(noteList||[]).filter(x=>x.id!==n.id&&!noteBelow(n.id,x.id));
 const edit=html`<form class="note-form note-edit-form" hidden><label>${t('Title')}<input name="title" maxlength="120" required value="${n.name}"></label>${areas.length>1?html`<label>${t('Area')}<select name="area">${areas.map(a=>html`<option value="${a.id}"${a.id===n.area?html` selected`:''}>${a.label}</option>`)}</select></label>`:''}<label>${t('Under')}<select name="parent"><option value="">${t('Top of Notes')}</option>${noteOptions(others,n.parent)}</select></label><span class="note-days"><label>${t('Starts')}<input type="date" name="starts" value="${n.starts||''}"${n.dated?html` required`:''}></label><label>${t('Ends')}<input type="date" name="ends" value="${n.ends||''}"></label></span><span class="note-acts"><button type="button" class="quiet" data-note-cancel>${t('Cancel')}</button><button class="primary">${t('Save')}</button></span></form>`;
 const merge=html`<form class="note-form note-merge-form" hidden><label>${t('Merge into')}<select name="into" required><option value="">${t('Pick a note')}</option>${noteOptions(others)}</select></label><p class="graph-sub">${t('Its lines and the notes under it move there. The Machine adds to that note from then on.')}</p><span class="note-acts"><button type="button" class="quiet" data-note-cancel>${t('Cancel')}</button><button class="primary">${t('Merge')}</button></span></form>`;
 const add=html`<form class="note-form note-add-form"${noteAdding?'':html` hidden`}><textarea name="text" maxlength="1000" rows="2" required aria-label="${t('New line')}" placeholder="${t('Type @ to link a person, project or note')}"></textarea><span class="note-acts"><button type="button" class="quiet" data-note-cancel>${t('Cancel')}</button><button class="primary">${t('Add')}</button></span></form>`;
 return html`${crumbs}<article class="graph-detail note-page"><div class="name-row"><h3 title="${n.name}">${n.name}</h3><div class="org-actions"><button class="ghost" data-note-edit>${t('Edit')}</button>${menu}</div></div>${sub?html`<p class="graph-sub detail-sub">${sub}</p>`:''}${edit}${merge}
  ${lines.length?html`<ul class="note-lines">${lines.map(noteLine)}</ul>`:noteAdding?'':html`<p class="graph-sub note-empty">${t('Nothing in this note yet.')}</p>`}${add}<button type="button" class="quiet note-add-line" data-note-add${noteAdding?html` hidden`:''}>+ ${t('Add a line')}</button></article>
  <section class="note-kids"${kids.length?'':html` hidden`}><div class="section-head"><h2>${t('Notes under this one')}</h2>${kids.length?html`<span class="count">${kids.length}</span>`:''}</div>${noteTitleForm('note-under-form',n.id,false)}<div class="graph-list">${kids.map(x=>noteRow(x))}</div></section>${linkedFrom(n)}`}
// Linked from: the notes that name this page (a note, person, organization or project), on that page
const linkedFrom=n=>n.linked_from?.length?html`<section class="note-backlinks"><div class="section-head"><h2>${t('Linked from')}</h2><span class="count">${n.linked_from.length}</span></div><div class="graph-list">${n.linked_from.map(x=>noteRow(x))}</div></section>`:'';
// A redraw after the owner's own change: forms they closed are closed first, so the redraw isn't held for them
function noteRedraw(node=graphNode){for(const f of $('#people-view').querySelectorAll('.note-form'))f.hidden=true;return people(node,true)}
function noteUndo(text,action,args){toast(text);$('#toast').append(htmlNodes(html` <button type="button" data-note-undo="${action}" data-args="${JSON.stringify(args)}">${t('Undo')}</button>`));clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),15000)}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-note-undo]');if(!b)return;b.disabled=true;
 try{const r=await graphPost(b.dataset.noteUndo,JSON.parse(b.dataset.args));$('#toast').classList.remove('show');noteList=null;if(b.dataset.noteUndo==='note_line_restore')noteRedraw();else graphOpen(r.id)}catch(err){errCaught(err);toast(err.message,true)}});
async function noteDo(action,args,done){try{const r=await graphPost(action,args);await done?.(r);return r||{}}catch(err){errCaught(err);toast(err.message,true);return null}}
// Type @ and a name: people, organizations, projects and notes that match, to pick one; it goes in as its name, linked
async function noteSuggest(ta){const f=ta.form,box=f.querySelector('.note-suggest')||ta.insertAdjacentElement('afterend',make('div',{class:'note-suggest',role:'listbox','aria-label':t('Link to')}));
 const m=/(?:^|\s)@([^@\n]{1,40})$/.exec(ta.value.slice(0,ta.selectionStart));if(!m||!m[1].trim()){box.hidden=true;return}
 const q=m[1].trim(),mine=++noteFind,words=q.toLowerCase().split(/\s+/),notes=(noteList||[]).filter(x=>x.id!==graphNode&&words.every(w=>x.name.toLowerCase().includes(w))).slice(0,4);
 let found=[];try{found=(await request('api/graph?q='+encodeURIComponent(q))).found||[]}catch{}if(mine!==noteFind)return;
 const all=[...notes,...found.filter(x=>(['person','org','project'].includes(x.kind)&&!x.team_only&&!/^team:/.test(x.id)||/^note:/.test(x.id))&&x.id!==graphNode&&!notes.some(n=>n.id===x.id))].slice(0,8);
 const kind=x=>/^note:/.test(x.id)?t(NOTE_KIND[x.kind]||'Note'):t({person:'Person',org:'Organization',project:'Project'}[x.kind]||'');
 setHTML(box,all.length?html`${all.map(x=>html`<button type="button" role="option" data-note-pick="${x.id}" data-name="${x.name}"><span class="ell">${x.name}</span><small>${kind(x)}</small></button>`)}`:html`<p class="graph-sub">${t('Nothing by that name.')}</p>`);box.hidden=false}
function notePick(b){const f=b.closest('form'),ta=f.elements.text,before=ta.value.slice(0,ta.selectionStart),start=before.lastIndexOf('@'),name=b.dataset.name;
 ta.value=before.slice(0,start)+name+' '+ta.value.slice(ta.selectionStart).replace(/^\s+/,'');
 f.dataset.links=JSON.stringify([...JSON.parse(f.dataset.links||'[]').filter(l=>l.id!==b.dataset.notePick),{id:b.dataset.notePick,name}]);
 f.querySelector('.note-suggest').hidden=true;const at=start+name.length+1;ta.focus();ta.setSelectionRange(at,at)}
$('#people-view').addEventListener('input',e=>{if(e.target.matches('.note-add-form textarea,.note-line-form textarea'))noteSuggest(e.target)});
$('#people-view').addEventListener('keydown',e=>{const box=e.target.form?.querySelector('.note-suggest:not([hidden])');if(!box)return;
 if(e.key==='Escape'){box.hidden=true;e.stopPropagation()}else if((e.key==='Enter'||e.key==='Tab')&&box.querySelector('[data-note-pick]')){e.preventDefault();notePick(box.querySelector('[data-note-pick]'))}},true);
// The page's own buttons; they come before the Graph's click handler, which would open the row they sit in
$('#people-view').addEventListener('click',async e=>{const el=e.target.closest('[data-note-fold],[data-note-src],[data-note-pick],[data-note-cancel],[data-note-add],[data-note-edit],[data-note-child],[data-note-merge-open],[data-note-delete],[data-note-line-edit],[data-note-line-reset],[data-note-line-remove]');if(!el)return;
 e.preventDefault();e.stopPropagation();el.closest('details')?.removeAttribute('open');const d=el.dataset,id=graphNode,view=$('#people-view');
 const open=sel=>{for(const f of view.querySelectorAll('.note-edit-form,.note-merge-form'))f.hidden=true;const f=view.querySelector(sel);if(!f)return;f.hidden=false;f.querySelector('input,select,textarea')?.focus()};
 if('noteFold' in d){if(notesOpen.has(d.noteFold))notesOpen.delete(d.noteFold);else notesOpen.add(d.noteFold);sideStore.set('notes-open',JSON.stringify([...notesOpen]));const p=el.closest('[data-graph-panel]');if(p)setHTML(p,notesPane());return}
 if('noteSrc' in d)return msgOpen({id:Number(d.noteSrc),kind:d.kind,title:d.title});
 if('notePick' in d)return notePick(el);
 if('noteCancel' in d){const f=el.closest('form');if(f.matches('.note-line-form')){noteEditing=null;return noteRedraw()}if(f.matches('.note-add-form')){noteAdding=false;return noteRedraw()}f.hidden=true;return}
 if('noteAdd' in d){noteAdding=true;el.hidden=true;view.querySelector('.note-empty')?.remove();return open('.note-add-form')}
 if('noteEdit' in d)return open('.note-edit-form');
 if('noteMergeOpen' in d)return open('.note-merge-form');
 if('noteChild' in d){view.querySelector('.note-kids').hidden=false;return open('.note-under-form')}
 if('noteDelete' in d)return noteDo('note_delete',{id},()=>{noteUndo(t('Deleted the note.'),'note_restore',{id});noteList=null;graphBack('notes')});
 if('noteLineEdit' in d){noteEditing=Number(d.noteLineEdit);await noteRedraw();const ta=view.querySelector('.note-line-form textarea');if(ta){ta.focus();ta.setSelectionRange(ta.value.length,ta.value.length)}return}
 if('noteLineReset' in d)return noteDo('note_line_reset',{line:Number(d.noteLineReset)},()=>noteRedraw());
 if('noteLineRemove' in d)return noteDo('note_line_remove',{line:Number(d.noteLineRemove)},()=>{noteUndo(t('Removed the line.'),'note_line_restore',{line:Number(d.noteLineRemove)});return noteRedraw()})},true);
$('#people-view').addEventListener('submit',async e=>{const f=e.target.closest('.note-form');if(!f)return;e.preventDefault();e.stopPropagation();
 const save=f.querySelector('.primary'),id=graphNode,v=n=>f.elements[n]?.value,links=JSON.parse(f.dataset.links||'[]');save.disabled=true;let r=null;
 if(f.matches('.note-new-form,.note-under-form'))r=await noteDo('note_new',{title:v('title'),parent:f.dataset.noteParent||''},r=>{noteList=null;graphOpen(r.id)});
 else if(f.matches('.note-add-form'))r=await noteDo('note_line_add',{id,text:v('text'),links},async()=>{await noteRedraw();const ta=$('#people-view .note-add-form textarea');if(ta){ta.closest('form').hidden=false;ta.focus()}});
 else if(f.matches('.note-line-form'))r=await noteDo('note_line_edit',{line:Number(f.dataset.noteLine),text:v('text'),links},()=>{noteEditing=null;toast(t('Saved.'));return noteRedraw()});
 else if(f.matches('.note-edit-form')){const args={id,title:v('title'),parent:v('parent'),starts:v('starts'),ends:v('ends'),...(f.elements.area?{area:v('area')}:{})};r=await noteDo('note_edit',args,()=>{noteList=null;toast(t('Saved.'));return noteRedraw()})}
 else if(f.matches('.note-merge-form'))r=await noteDo('note_merge',{id,into:v('into')},r=>{noteUndo(t('Merged the notes.'),'note_unmerge',{id});noteList=null;graphOpen(r.id)});
 if(!r&&save.isConnected)save.disabled=false},true);
