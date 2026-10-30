// A doc write (doc_writes.py) on its to-do and in the review dialog: a new doc in full, or an edit as each paragraph
// before and after, with what goes struck through and what comes in marked. Nothing is written until the owner
// confirms it in the dialog, and only into the doc as it was when this was drafted (the server pins its version).
const DOC_DO={create:'New doc in {}',edit:'Edit “{}” in {}'},DOC_DID={create:'Created in {}',edit:'Saved in {}'};
const DOC_LABEL={create:'Review and create',edit:'Review changes'};
const docWhere=a=>a.provider==='microsoft'?'Word':'Google Docs';
const docHead=(a,done)=>done?t(DOC_DID[a.op]||DOC_DID.edit,docWhere(a)):a.op==='create'?t(DOC_DO.create,docWhere(a)):t(DOC_DO.edit,a.doc_title||'',docWhere(a));
const docDoneText=(a,sent)=>a.op==='create'?sentNote(sent,'Doc created.','Doc created at {}.'):sentNote(sent,'Changes saved in the doc.','Changes saved in the doc at {}.');
// New text as the doc gets it: "# " to "### " lines are headings, the rest paragraphs (doc_writes.lines).
const docLines=(text,tag)=>String(text||'').split('\n').filter(l=>l.trim()).map(l=>{const m=/^(#{1,3}) +(.*)$/.exec(l);
 return `<p class="dw-p${m?' dw-h'+m[1].length:''}">${tag?`<${tag}>`:''}${esc(m?m[2]:l)}${tag?`</${tag}>`:''}</p>`}).join('');
// One paragraph with its changed piece marked: struck through before, marked after.
const docMark=(text,piece,tag)=>{const s=String(text||''),i=piece?s.indexOf(piece):-1;
 return i<0?esc(s):esc(s.slice(0,i))+`<${tag}>${esc(piece)}</${tag}>`+esc(s.slice(i+piece.length))};
const docChange=(c,n,total)=>{const head=total>1?`<div class="dw-n">${esc(t('Change {} of {}',n,total))}</div>`:'';
 if('find' in c)return head+`<div class="dw-k">${esc(t('Before'))}</div><p class="dw-p">${docMark(c.before,c.find,'del')}</p><div class="dw-k">${esc(t('After'))}</div><p class="dw-p">${docMark(c.after,c.replace,'ins')}</p>`;
 if('after' in c)return head+`<div class="dw-k">${esc(t('Add after “{}”',c.before.length>80?c.before.slice(0,79)+'…':c.before))}</div>${docLines(c.insert,'ins')}`;
 return head+`<div class="dw-k">${esc(t('Add at the end'))}</div>${docLines(c.append,'ins')}`};
// A new doc's text under its title: a first heading that only repeats the title shows once (doc_writes.untitled).
const docSame=x=>String(x||'').trim().replace(/\s+/g,' ').toLowerCase();
const docBody=a=>{const ls=String(a.body||'').split('\n').filter(l=>l.trim()),m=ls.length?/^#{1,3} +(.*)$/.exec(ls[0].trim()):null;
 return m&&docSame(m[1])===docSame(a.title)?ls.slice(1).join('\n'):String(a.body||'')};
const docWriteHtml=a=>a.op==='create'?`<p class="dw-p dw-h1">${esc(a.title)}</p>${docLines(docBody(a))}`:(a.changes||[]).map((c,i,all)=>`<div class="dw-ch">${docChange(c,i+1,all.length)}</div>`).join('');
// Plain text of the same, for chat and copy (doc_writes.preview).
const docWriteText=a=>a.op==='create'?a.title+'\n\n'+docBody(a):(a.changes||[]).map(c=>'find' in c?t('Before')+': '+c.before+'\n'+t('After')+': '+c.after:'after' in c?t('Add after “{}”',c.before)+'\n'+c.insert:t('Add at the end')+'\n'+c.append).join('\n\n');
function docWriteBox(s,a){const done=(a.state||s.action_status)?.status==='sent',key='draft-'+s.id+'-'+a.revision,open=expandedBodies.has(key);
 const size=a.op==='create'?String(a.body||'').split('\n').length:(a.changes||[]).length*4,fold=size>16;
 return `<div class="draft doc-write${done?' sent':''}${fold&&!open?' clamp':''}" role="group" aria-label="${esc(a.op==='create'?t('New doc'):t('Doc changes'))}"><div class="dm">${esc(docHead(a,done))}${safeURL(a.url)?` · <a href="${esc(safeURL(a.url))}" target="_blank" rel="noreferrer">${esc(t('Open the doc'))}</a>`:''}</div><div class="db dw">${docWriteHtml(a)}</div></div>${fold?`<button type="button" class="more" data-more="${esc(key)}" aria-expanded="${open}">${open?'Show less':'Show more'}</button>`:''}`}
// The review dialog for it: everything that goes in, then Create or Save. The tap here writes it, once.
function openDocWrite(id,draft){sendTask=id;sendRevision=draft.revision;sendDraft=draft;$('#send-editor').hidden=true;$('#send-edit').hidden=true;
 $('#send-title').textContent=draft.op==='create'?t('Create this doc?'):t('Save these changes?');$('#send-confirm').textContent=draft.op==='create'?t('Create'):t('Save');
 $('#send-preview').classList.remove('code','mail');$('#send-confirm').hidden=false;$('#send-confirm').disabled=false;$('#send-cancel').textContent='Cancel';$('#send-recipients').hidden=true;$('#send-files').hidden=true;$('#send-error').textContent='';
 sendHeader=()=>sendRows(draft.op==='create'?[['Doc',draft.title],['Where',docWhere(draft)+(draft.account_name?' · '+draft.account_name:'')]]:[['Doc',draft.doc_title],['Where',docWhere(draft)],['Changes',String((draft.changes||[]).length)]]);sendHeader();
 $('#send-preview').hidden=false;$('#send-preview').innerHTML=`<div class="dw">${docWriteHtml(draft)}</div>`;
 sendFine(draft.op==='create'?t('Only you can see the new doc until you share it.'):t('Only these changes are made, and only if the doc hasn’t changed since.'));$('#send-dialog').showModal()}
