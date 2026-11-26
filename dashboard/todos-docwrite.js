// A doc write (doc_writes.py) on its to-do and in the review dialog: a new doc in full, or an edit as each paragraph
// before and after, with what goes struck through and what comes in marked. A new private doc is made while the to-do
// is prepared, and Open the doc leads its buttons (Store.make_new_docs, cardActions); an edit is written only after the owner confirms it in the
// dialog, and only into the doc as it was when this was drafted (the server pins its version).
// Notion (connectors/notion.py): a page is a doc here; done marks a task assigned to the owner done, after their OK.
const DOC_DO={create:'New doc in {}',edit:'Edit “{}” in {}',done:'Mark “{}” done in {}'},DOC_DID={create:'Created in {}',edit:'Saved in {}',done:'Marked done in {}'};
const DOC_LABEL={create:'Review and create',edit:'Review changes',done:'Mark done'};
const docWhere=a=>a.provider==='microsoft'?'Word':a.provider==='notion'?'Notion':a.file_kind==='sheets'?'Google Sheets':a.file_kind?'Google Slides':'Google Docs';
// A Sheet or Slides file's edit draws in its lazy part (todos-filewrite.js), once that's in
const docBusy=a=>a?.file_kind?'Writing the file…':'Writing the doc…';
// (one function per shape: the html and the plain text never share a return, so text never carries markup)
const fileWait=()=>(lazyRun('filewrite',render),'');
const fileWHtml=a=>lazyIn('filewrite')?fileWriteHtml(a):fileWait();
const fileWText=a=>lazyIn('filewrite')?fileWriteText(a):fileWait();
const docHead=(a,done)=>done?t(DOC_DID[a.op]||DOC_DID.edit,docWhere(a)):a.op==='create'?t(a.provider==='notion'?'New page in {}':DOC_DO.create,docWhere(a)):t(DOC_DO[a.op]||DOC_DO.edit,a.doc_title||'',docWhere(a));
const docDoneText=(a,sent)=>a.file_kind?sentNote(sent,'Changes saved in the file.','Changes saved in the file at {}.'):a.op==='create'?(a.provider==='notion'?sentNote(sent,'Page created.','Page created at {}.'):sentNote(sent,'Doc created.','Doc created at {}.'))
 :a.op==='done'?sentNote(sent,'Marked done in Notion.','Marked done in Notion at {}.'):sentNote(sent,'Changes saved in the doc.','Changes saved in the doc at {}.');
// New text as the doc gets it: "# " to "### " lines are headings, the rest paragraphs (doc_writes.lines). Google Docs
// (g) also gets "- " lines as bullets and **bold**, *italic*, [text](link) as marks (doc_writes.google_lines, MARKS).
const docR=/\*\*(?=\S)(.+?)(?<=\S)\*\*|(?<![\w*])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![\w*])|\[([^\]\n]+)\]\((https?:\/\/[^\s<>"\\)]+)\)/g;
const docM=x=>{const o=[];let i=0;for(const m of x.matchAll(docR)){o.push(x.slice(i,m.index),m[1]?html`<b>${m[1]}</b>`:m[2]?html`<i>${m[2]}</i>`:html`<u>${m[3]}</u> (${m[4]})`);i=m.index+m[0].length}return[...o,x.slice(i)]};
const docH=/^(#{1,3}) +(.*)$/,docLines=(text,tag,g)=>String(text||'').split('\n').filter(l=>l.trim()).map(l=>{const m=docH.exec(l),b=g&&!m&&/^[-*•] +(.*\S)/.exec(l);
 const x=m?m[2]:b?'• '+b[1]:l,y=g?docM(x):x;return html`<p class="dw-p${m?' dw-h'+m[1].length:''}">${tag==='ins'?html`<ins>${y}</ins>`:y}</p>`});
// One paragraph with its changed piece marked: struck through before, marked after.
const docMark=(text,piece,tag)=>{const s=String(text||''),i=piece?s.indexOf(piece):-1;
 return i<0?s:html`${s.slice(0,i)}${tag==='del'?html`<del>${piece}</del>`:html`<ins>${piece}</ins>`}${s.slice(i+piece.length)}`};
// Formatting (Google Docs): what it does, and its paragraph with the formatted text marked.
const docK=(k,x)=>html`<div class="dw-k">${k}</div>${x}`,docP=(c,x,tag)=>html`<p class="dw-p">${docMark(c,x,tag)}</p>`;
const docChange=(c,n,total,g)=>html`${total>1?html`<div class="dw-n">${t('Change {} of {}',n,total)}</div>`:''}${'format' in c?docK(t(c.how,c.link),docP(c.before,c.format,'ins'))
 :'find' in c?html`${docK(t('Before'),docP(c.before,c.find,'del'))}${docK(t('After'),docP(c.after,c.replace,'ins'))}`
 :'after' in c?docK(t('Add after “{}”',c.before),docLines(c.insert,'ins',g)):docK(t('Add at the end'),docLines(c.append,'ins',g))}`;
// A new doc's text under its title: a first heading that only repeats the title shows once (doc_writes.untitled).
const docSame=x=>String(x||'').trim().replace(/\s+/g,' ').toLowerCase();
const docBody=a=>{const ls=String(a.body||'').split('\n').filter(l=>l.trim()),m=ls.length?docH.exec(ls[0].trim()):null;
 return m&&docSame(m[2])===docSame(a.title)?ls.slice(1).join('\n'):String(a.body||'')};
const docWriteHtml=a=>a.file_kind?fileWHtml(a):a.op==='done'?html`<p class="dw-p">${t('Mark “{}” done in {}',a.doc_title||'',docWhere(a))}</p>`:a.op==='create'?html`<p class="dw-p dw-h1">${a.title}</p>${docLines(docBody(a),0,a.provider==='google')}`:html`${(a.changes||[]).map((c,i,all)=>html`<div class="dw-ch">${docChange(c,i+1,all.length,a.provider==='google')}</div>`)}`;
// Plain text of the same, for chat and copy (doc_writes.preview).
const docWriteText=a=>a.file_kind?fileWText(a):a.op==='done'?t('Mark “{}” done in {}',a.doc_title||'',docWhere(a)):a.op==='create'?a.title+'\n\n'+docBody(a):(a.changes||[]).map(c=>'format' in c?t(c.how,c.link)+': '+c.format:'find' in c?t('Before')+': '+c.before+'\n'+t('After')+': '+c.after:'after' in c?t('Add after “{}”',c.before)+'\n'+c.insert:t('Add at the end')+'\n'+c.append).join('\n\n');
function docWriteBox(s,a){const st=a.state||s.action_status,done=st?.status==='sent',url=a.url||(done?st?.url:''),key='draft-'+s.id+'-'+a.revision,open=expandedBodies.has(key);
 const size=a.op==='create'?String(a.body||'').split('\n').length:(a.changes||[]).length*4,fold=size>16,open_=t(a.provider==='notion'?'Open the page':a.file_kind?'Open the file':'Open the doc');
 return html`<div class="draft doc-write${done?' sent':''}${fold&&!open?' clamp':''}" data-clamp="${key}" role="group" aria-label="${t(a.op==='create'?'New doc':'Doc changes')}"><div class="dm">${viaIco(actionVia(a))}<span>${docHead(a,done)}${!done&&safeURL(url)?html` · <a href="${safeHref(safeURL(url))}" target="_blank" rel="noreferrer">${open_}</a>`:''}</span></div><div class="db dw">${docWriteHtml(a)}</div></div>${fold?html`<button type="button" class="more" data-more="${key}" aria-expanded="${open}">${open?'Show less':'Show more'}</button>`:''}`}
