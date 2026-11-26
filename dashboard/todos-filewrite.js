// A lazy part (dashboard_parts.LAZY 'filewrite'): an edit to a linked Google Sheet or Slides file (file_writes.py), on
// its to-do, in the chat and in the review dialog. A sheet's cells as a table, each before and after (new rows and a new
// tab's cells as they come in); a slide's text before and after, with what goes struck through and what comes in marked;
// a new slide as its title and body. fileWrite(a) is the html, fileWrite(a,1) its plain text, fileWrite(a,2,sent) the
// line once it's saved (docWriteHtml, docWriteText and docDoneText ask for it through fileW).
const fwKey=c=>'find' in c?t('Slide {}',c.slide):c.add_slide?t('New slide {}: {}',c.at,c.add_slide):c.add_tab?t('New tab “{}”',c.add_tab)
 :c.append?t('New rows in “{}” after row {}',c.tab,c.row-1):t('Cells {} in “{}”',c.cells,c.tab);
const fwHow=c=>c.formulas?t('Entered as formulas, so they calculate.'):'';
const fwCells=c=>html`<table class="fw-t"><thead><tr><th scope="col">${t('Cell')}</th>${c.cells?html`<th scope="col">${t('Before')}</th>`:''}<th scope="col">${c.cells?t('After'):t('New')}</th></tr></thead><tbody>${(c.shown||[]).map(x=>html`<tr><th scope="row">${x.cell}</th>${c.cells?html`<td>${x.before?html`<del>${x.before}</del>`:''}</td>`:''}<td>${x.after===x.before?x.after:html`<ins>${x.after}</ins>`}</td></tr>`)}</tbody></table>`;
const fwChange=c=>html`<div class="dw-k">${fwKey(c)}</div>${'find' in c?(c.shown||[]).map(x=>html`<div class="dw-k">${t('Before')}</div><p class="dw-p">${docMark(x.before,c.find,'del')}</p><div class="dw-k">${t('After')}</div><p class="dw-p">${docMark(x.after,c.replace,'ins')}</p>`)
 :c.add_slide?docLines(c.body,'ins'):c.shown?.length?fwCells(c):''}${fwHow(c)?html`<div class="dw-k">${fwHow(c)}</div>`:''}`;
const fwText=c=>[fwKey(c),...'find' in c?(c.shown||[]).flatMap(x=>[t('Before')+': '+x.before,t('After')+': '+x.after]):c.add_slide?[c.body]
 :(c.shown||[]).map(x=>x.cell+': '+(x.before?x.before+' → ':'')+x.after),fwHow(c)].filter(Boolean).join('\n');
function fileWrite(a,x,sent){const cs=a.changes||[];
 if(x===2)return sentNote(sent,'Changes saved in the file.','Changes saved in the file at {}.');
 if(x)return cs.map(fwText).join('\n\n');
 return html`${cs.map((c,i)=>html`<div class="dw-ch">${cs.length>1?html`<div class="dw-n">${t('Change {} of {}',i+1,cs.length)}</div>`:''}${fwChange(c)}</div>`)}`}
