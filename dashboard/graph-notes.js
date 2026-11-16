// A trip's or an event's page (#graph/note:<id>), opened from its band in Calendar (note_pages_app.py note_page): its
// dates and its lines, each with the message it came from and the to-do it points to. The Machine keeps it up to date
// from booking and ticket mail; there is nothing to edit here.
const NOTE_KIND={trip:'Trip',event:'Event'};
const noteDay=v=>v?shortDay(String(v).slice(0,10)):'';
const noteDates=x=>x.starts?(x.ends&&x.ends!==x.starts?t('{} to {}',noteDay(x.starts),noteDay(x.ends)):noteDay(x.starts)):'';
// A line's words with its links: each name a link to its page, the rest plain words
function noteText(x){const text=x.text,low=text.toLowerCase(),spots=[];
 for(const l of x.links||[]){const i=low.indexOf(l.name.toLowerCase());if(i>=0&&!spots.some(s=>i<s.end&&i+l.name.length>s.i))spots.push({i,end:i+l.name.length,id:l.id})}
 spots.sort((a,b)=>a.i-b.i);const out=[];let at=0;for(const s of spots){out.push(text.slice(at,s.i),html`<a href="${graphHash(s.id)}" class="note-link">${text.slice(s.i,s.end)}</a>`);at=s.end}out.push(text.slice(at));return out}
// until: a line that runs into another day (an event) reads from its start to its end
const noteStamp=v=>noteDay(v)+(String(v).length>10?' '+fmtHM(new Date(v)):'');
const noteWhen=(v,until)=>v?html`<time datetime="${v}">${until?t('{} to {}',noteStamp(v),noteStamp(until)):noteStamp(v)}</time>`:'';
// Where a line came from, and the to-do it points to (a ticket: the details stay there)
function noteSource(x){const from=x.source?.gone?t('From a message that is gone')
 :x.source?html`<button type="button" class="link" data-note-src="${x.source.id}" data-kind="${x.source.kind}" data-title="${x.source.title}">${x.source.kind==='calendar.event'?t('From your calendar'):t('From {}',x.source.from||x.source.title||t('a message'))}</button>`:'';
 // the to-do itself: an open one in the list, picked out; a done one in its chat, as from Done
 const todoOpen=(state?.suggestions||[]).some(s=>s.id===x.todo&&!closed(s)&&!looksDone(s)&&s.status!=='snoozed');
 const todo=x.todo?html`<a href="${todoOpen?'#card=':'#chat='}${encodeURIComponent(x.todo)}">${t('Open the to-do')}</a>`:'';
 return from||todo?html`<small class="note-src">${from}${from&&todo?' · ':''}${todo}</small>`:''}
const noteLine=x=>html`<li id="note-line-${x.id}">${noteWhen(x.at,x.data?.until)}<span class="note-text">${noteText(x)}${noteSource(x)}</span></li>`;
// Calendar › its name, and its name as the heading right under it (the crumb is for screen readers and the tab's title)
function notePage(n){const areas=n.areas||[],label=areas.find(x=>x.id===n.area)?.label||'',lines=n.lines||[],sep=html`<span aria-hidden="true">›</span>`;
 const crumbs=html`<div class="graph-crumbs note-crumbs" role="navigation" aria-label="${t('Breadcrumb')}"><a href="#calendar">${t('Calendar')}</a><span class="crumb-here" aria-current="page">${sep}${n.name}</span></div>`;
 const sub=[NOTE_KIND[n.kind]?t(NOTE_KIND[n.kind]):'',noteDates(n),areas.length>1?label:'',t('Kept up to date by The Machine')].filter(Boolean).join(' · ');
 return html`${crumbs}<article class="graph-detail note-page"><div class="name-row"><h3 title="${n.name}">${n.name}</h3></div><p class="graph-sub detail-sub">${sub}</p>
  ${lines.length?html`<ul class="note-lines">${lines.map(noteLine)}</ul>`:html`<p class="graph-sub note-empty">${t('Nothing in this note yet.')}</p>`}</article>`}
// A line's message opens where it is; this comes before the Graph's click handler, which would open the row it sits in
$('#people-view').addEventListener('click',e=>{const el=e.target.closest('[data-note-src]');if(!el)return;e.preventDefault();e.stopPropagation();
 const d=el.dataset;msgOpen({id:Number(d.noteSrc),kind:d.kind,title:d.title})},true);
