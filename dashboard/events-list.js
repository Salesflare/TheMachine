// Keyword matches at once (words=1), then the full search: rows shown stay, its others come in under
let evSearched=0;
async function search(){let account=$('#account').value||'all';const q=$('#query').value.trim();evAnswer(q);const n=++evSearched,url='api/events?account='+encodeURIComponent(account)+'&q='+encodeURIComponent($('#query').value);let early=null,last=false;
 if(q)Promise.all([request(url+'&words=1'),localeIn]).then(([rows])=>{if(n===evSearched&&!last&&rows?.length){early=rows;draw(rows)}}).catch(()=>{});
 // Each row reads by its kind (message_view.list_row): who by name, its words without stamps, ids or markup, and
 // "Open in …" in the same place on every row that has a link. A message with none (a WhatsApp, Signal or Telegram
 // chat, a phone notification, a note of the Machine's own) has no web address to open.
 const row=(e,later='')=>{const r=e.row||{title:e.title,who:'',text:e.body,url:e.metadata?.source_url||''},link=r.url&&safeURL(r.url),from=r.who&&['whatsapp.message','linkedin.message'].includes(e.kind)?'From '+r.who:r.who;
  const meta=[account==='all'?evAccountName(e.account_id):'',html`<span>${when(e)}</span>`,from].filter(Boolean).map((x,i)=>i?[' · ',x]:x);
  const said=r.turns?.length?html`<p class="body clamp ev-turns" style="--lines:3" translate="no">${r.turns.map((x,i)=>html`${i?html`<br>`:''}<b>${x.from}</b> ${x.body}`)}</p>`:r.text?html`<p class="body clamp" style="--lines:3" translate="no">${r.text}</p>`:'';
  return html`<article class="event tap" data-event="${e.id}"${e.kind==='calendar.event'?html` data-meeting`:''} tabindex="0"${later?html` hidden`:''}><div class="event-head"><span class="icon">${markIco(sourceMark(e.kind,e.account_id,e.metadata.package_name))}</span><div><h3 translate="no">${r.title||e.title}</h3><small>${meta}</small></div></div>${said}${link?html`<a class="open" href="${onPhone()&&safeURL(r.phone_url||'')||link}" target="_blank" rel="noreferrer">${r.app?t('Open in {} ↗',r.app):t('Open original')}</a>`:''}${e.kind==='android.notification'?html`<p class="note">Phone preview only. Check the app for the full message.</p>`:e.metadata.truncated?html`<p class="note">Some conversation history or text is omitted; check the original.</p>`:''}</article>`};
 /* As on a person's timeline: meetings still to come apart under Coming up, soonest first; the list itself newest first.
    With words searched, the best match first, as the search ranked them */
 function draw(rows){const at=Date.now(),up=q?[]:rows.filter(e=>Date.parse(e.occurred_at)>at).sort((a,b)=>Date.parse(a.occurred_at)-Date.parse(b.occurred_at)),past=q?rows:rows.filter(e=>!(Date.parse(e.occurred_at)>at)).sort((a,b)=>Date.parse(b.occurred_at)-Date.parse(a.occurred_at));
 setHTML($('#results'),up.length||past.length?html`${up.length?html`<div class="ev-soon"><h3 class="ge-day">Coming up</h3>${up.map((e,i)=>row(e,i>=GE_SOON))}${up.length>GE_SOON?html`<button type="button" class="ghost ge-more" data-ev-soon>Show all upcoming</button>`:''}</div>${past.length?html`<h3 class="ge-day">Latest</h3>`:''}`:''}${past.map(e=>row(e))}`:html`<div class="empty all-clear"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>No matching messages.</strong>Try another account or a broader search.</div></div>`)}
 try{const rows=await request(url);last=true;if(n!==evSearched)return;
  const box=$('#results'),want=rows.map(e=>''+e.id),kept=early?[...box.querySelectorAll('article')].filter(a=>want.includes(a.dataset.event)||a.remove()).map(a=>a.dataset.event):[];
  if(kept.length){const more=document.createElement('template');setHTML(more,html`${rows.filter(e=>!kept.includes(''+e.id)).map(e=>row(e))}`);box.append(more.content)}else draw(rows);
  notice('')}catch(e){last=true;errCaught(e);notice(e.message,true);if($('#results').textContent==='Loading…')$('#results').innerHTML=''}}
$('#search').onclick=search;$('#account').onchange=search;
// A question searched with every account in view gets a short answer above the results, from Ask (search_ask.py, the
// palette's own turns), with the messages it read to open. Three words or more, once per search; nothing when it isn't
// a question or the messages don't answer it.
let evAsked=0;
async function evAnswer(q){const n=++evAsked,box=$('#ev-answer');box.hidden=true;box.textContent='';
 if($('#account').value!=='all'||q.split(/\s+/).length<3)return;
 if(/[?？¿؟]$/.test(q)){setHTML(box,html`<p class="pal-answer muted" role="status"><span class="pal-dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="pal-sr">${t('Looking…')}</span></p>`);box.hidden=false}
 let r;try{r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'search_ask',args:{query:q,area:'all'}})})}catch{r=null}
 if(n!==evAsked)return;const src=Array.isArray(r?.sources)?r.sources:[],text=typeof r?.answer==='string'?r.answer.trim():'';
 box.hidden=!text||!src.length&&!r.memory?.length;if(box.hidden){box.textContent='';return}
 setHTML(box,html`<h3 class="ge-day">${t('Answer')}</h3><p dir="auto" translate="no">${text}</p>${src.map((m,i)=>html`<button type="button" class="ev-src" data-src="${i}" translate="no">${[m.title||m.from,m.at?humanTime(m.at):''].filter(Boolean).join(' · ')}</button>`)}`);
 box.onclick=e=>{const b=e.target.closest('[data-src]');if(b)msgOpen(src[+b.dataset.src])}}
$('#results').onclick=e=>{const m=e.target.closest('[data-ev-soon]');if(m){for(const a of m.parentElement.querySelectorAll('article[hidden]'))a.hidden=false;m.remove();return}openEventFrom(e)};
// Any collected message opens in the same reader as a card's originals: the full email, the WhatsApp text, the Slack thread.
function openEventFrom(e){const a=e.target.closest('article[data-event]');if(!a||e.target.closest('a,button,input'))return false;const title=a.querySelector('h3,h4')?.textContent;
 if(a.dataset.events)openConversation(a);else if('meeting' in a.dataset)openMeeting(a.dataset.meeting||a.dataset.event,title);else openEvent(a.dataset.event,title);return true}
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.matches?.('article[data-event]'))openEventFrom(e)});
const openEvent=(ev,title,local)=>openOriginal(ev,title,false,local);  // local: nothing from outside loads (events-email-frame.js)
// One collected signal as it came in. A meeting opens as it does in the Calendar instead (openMeeting), unless its raw
// invite is asked for (raw: Original invite in the meeting's details).
async function openOriginal(ev,title,raw,local){const dialog=$('#email-dialog');$('#email-title').textContent=title||t('Original');setHTML($('#email-content'),html`<p class="muted">Loading…</p>`);if(!dialog.open)dialog.showModal();
let o;try{[{originals:[o]}]=await Promise.all([request('api/originals?event='+encodeURIComponent(ev)),lazyPart('msgview')])}catch(e){errCaught(e);setHTML($('#email-content'),html`<p class="muted">${e.message}</p>`);return}
if(!o){setHTML($('#email-content'),html`<p class="muted">The original is no longer available.</p>`);return}
if(o.kind==='calendar'&&!raw){openMeeting(ev,title);return}
// Titled by the message itself (an email's subject, a chat's conversation), not by the row it was opened from
const shown=viewTitle(o)||title||t('Original');$('#email-title').textContent=shown;
if(isChat(o)){setHTML($('#email-content'),chatThreadHTML([o],{titled:true}));return}  // a chat message as in its thread, its text once
o.raw=!!raw;o.local=!!local;setHTML($('#email-content'),html`<div class="email" data-msg="0">${messageHTML(o,'',0,shown)}</div>`);fillMessage($('#email-content [data-msg="0"]'),o,'')}
// A meeting, wherever it is opened (a timeline, Events, a to-do's source, a search): the Calendar's own details, with its
// Notes, Transcript and Generate notes, and its invite one tap away. When the meeting can't be read that way, its invite.
async function openMeeting(ev,title){let m=null;try{m=(await request('api/meeting?event='+encodeURIComponent(ev))).meeting}catch(e){errCaught(e)}
 if(!m){openOriginal(ev,title,true);return}if($('#email-dialog').open)$('#email-dialog').close();lazyRun('calendar',()=>calView(m))}
$('#email-content').addEventListener('click',e=>{const b=e.target.closest('[data-open-meeting]');if(b)openMeeting(b.dataset.openMeeting,'')});
// A conversation from the Graph: its messages in order, each who said it, when and the whole text.
async function openConversation(row){const dialog=$('#email-dialog'),group='group' in row.dataset;$('#email-title').textContent=row.dataset.title||'Conversation';setHTML($('#email-content'),html`<p class="muted">Loading…</p>`);dialog.showModal();
let list;try{[{originals:list}]=await Promise.all([request('api/originals?events='+encodeURIComponent(row.dataset.events)),lazyPart('msgview')])}catch(e){errCaught(e);setHTML($('#email-content'),html`<p class="muted">${e.message}</p>`);return}
if(!list.length){setHTML($('#email-content'),html`<p class="muted">The messages are no longer available.</p>`);return}
setHTML($('#email-content'),chatThreadHTML(list,{names:group,head:false,src:row.dataset.src}))}
$('#query').onkeydown=e=>{if(e.key==='Enter')search()};
// Messages, the results page: everything the Machine read, by meaning and by words, every account or one. It isn't in
// the sidebar: the palette's See all results (and a message there), G then E and #messages (#events) open it; an empty
// search shows the newest.
function msgSearch(q){$('#query').value=q||'';$('#results').innerHTML='<p class="muted">Loading…</p>';showTab('events');search();scrollTo(0,0)}
function msgOpen(m){if(m.kind==='calendar.event')openMeeting(m.id,m.title);else openEvent(m.id,m.title)}
// The account a row came from, as its Connections card names it (names.account_card): its own name ("Lumen Labs
// Slack"), else Work or Personal when the card's title is only its address or its app's name (the row's icon says the
// app). The address only when another account of that app would read the same. Never an id.
const evAccountLabel=c=>{const title=String(c.card_title||c.display_name||''),scope=String(c.card_subtitle||'').split(' · ')[0],plain=s=>String(s||'').toLowerCase().replace(/[^\p{L}\p{N}]/gu,'');
 return title&&!title.includes('@')&&!(c.service&&plain(title).startsWith(plain(c.service)))?title:scope||title};
const evAccountName=id=>{const all=state.connectors||[],c=all.find(c=>c.id===id);if(!c)return '';const label=evAccountLabel(c);
 return all.some(o=>o.id!==id&&o.service===c.service&&evAccountLabel(o)===label)&&c.card_title?c.card_title:label};
// who it's from by name only ("Ana Ruiz <ana@x.example>" reads Ana Ruiz; a bare address stays), then when
const msgSub=m=>[String(m.metadata?.from||m.metadata?.sender_display||m.metadata?.channel_name||m.metadata?.chat_name||'').replace(/^\s*"?([^"<]*?)"?\s*<[^>]*>\s*$/,(all,n)=>n.trim()||all),when(m)].filter(Boolean).join(' · ');
