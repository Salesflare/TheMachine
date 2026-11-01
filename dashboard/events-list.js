async function search(){let account=$('#account').value||'all';const name=id=>{const c=(state.connectors||[]).find(c=>c.id===id);return c?(c.display_name||c.email||id):id};try{let rows=await request('api/events?account='+encodeURIComponent(account)+'&q='+encodeURIComponent($('#query').value));const row=(e,later='')=>`<article class="event tap" data-event="${e.id}"${e.kind==='calendar.event'?' data-meeting':''} tabindex="0"${later}><div class="event-head">${icon(kindService(e.kind))}<div><h3 translate="no">${esc(e.title)}</h3><small>${account==='all'?esc(name(e.account_id))+' · ':''}<span>${esc(when(e))}</span>${(w=>w?' · '+esc(w):'')(e.kind==='calendar.event'?'':e.kind==='android.notification'?(e.metadata.app_name||e.metadata.package_name||'Unknown app'):['whatsapp.message','linkedin.message'].includes(e.kind)?('From '+(e.metadata.from_me?'You':e.metadata.sender_display||e.metadata.from||'Unknown sender')):(e.metadata.from||e.metadata.channel_name||e.metadata.chat_name||''))}</small></div></div><p class="body clamp" style="--lines:3" translate="no">${esc(e.body)}</p>${e.metadata.source_url?`<a class="open" href="${esc(e.metadata.source_url)}" target="_blank" rel="noreferrer">Open in ${e.kind==='calendar.event'?'Calendar':e.kind==='slack.message'?'Slack':e.kind==='linkedin.message'?'LinkedIn':e.kind.startsWith('salesflare.')?'Salesflare':e.kind.startsWith('github.')?'GitHub':e.kind==='stripe.event'?'Stripe':e.kind.startsWith('x.')?'X':e.kind==='gmail.message'?'Gmail':'the original'} ↗</a>`:''}${e.kind==='android.notification'?'<p class="note">Phone preview only. Check the app for the full message.</p>':e.metadata.truncated?'<p class="note">Some conversation history or text is omitted; check the original.</p>':''}</article>`;
 /* As on a person's timeline: meetings still to come apart under Coming up, soonest first; the list itself newest first */
 const at=Date.now(),up=rows.filter(e=>Date.parse(e.occurred_at)>at).sort((a,b)=>Date.parse(a.occurred_at)-Date.parse(b.occurred_at)),past=rows.filter(e=>!(Date.parse(e.occurred_at)>at)).sort((a,b)=>Date.parse(b.occurred_at)-Date.parse(a.occurred_at));
 $('#results').innerHTML=(up.length?`<div class="ev-soon"><h3 class="ge-day">Coming up</h3>${up.map((e,i)=>row(e,i>=GE_SOON?' hidden':'')).join('')}${up.length>GE_SOON?'<button type="button" class="ghost ge-more" data-ev-soon>Show all upcoming</button>':''}</div>${past.length?'<h3 class="ge-day">Latest</h3>':''}`:'')+past.map(e=>row(e)).join('')||'<div class="empty all-clear"><img class="sticker" src="brand/thinking.webp" alt=""><div><strong>No matching messages.</strong>Try another account or a broader search.</div></div>';notice('')}catch(e){errCaught(e);notice(e.message,true);if($('#results').textContent==='Loading…')$('#results').innerHTML=''}}
$('#search').onclick=search;$('#account').onchange=search;
$('#results').onclick=e=>{const m=e.target.closest('[data-ev-soon]');if(m){for(const a of m.parentElement.querySelectorAll('article[hidden]'))a.hidden=false;m.remove();return}openEventFrom(e)};
// Any collected message opens in the same reader as a card's originals: the full email, the WhatsApp text, the Slack thread.
function openEventFrom(e){const a=e.target.closest('article[data-event]');if(!a||e.target.closest('a,button,input'))return false;const title=a.querySelector('h3,h4')?.textContent;
 if(a.dataset.events)openConversation(a);else if('meeting' in a.dataset)openMeeting(a.dataset.meeting||a.dataset.event,title);else openEvent(a.dataset.event,title);return true}
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.matches?.('article[data-event]'))openEventFrom(e)});
const openEvent=(ev,title)=>openOriginal(ev,title,false);
// One collected signal as it came in. A meeting opens as it does in the Calendar instead (openMeeting), unless its raw
// invite is asked for (raw: Original invite in the meeting's details).
async function openOriginal(ev,title,raw){const dialog=$('#email-dialog');$('#email-title').textContent=title||t('Original');$('#email-content').innerHTML='<p class="muted">Loading…</p>';if(!dialog.open)dialog.showModal();
let o;try{o=(await request('api/originals?event='+encodeURIComponent(ev))).originals[0]}catch(e){errCaught(e);$('#email-content').innerHTML=`<p class="muted">${esc(e.message)}</p>`;return}
if(!o){$('#email-content').innerHTML='<p class="muted">The original is no longer available.</p>';return}
if(o.kind==='calendar'&&!raw){openMeeting(ev,title);return}
o.raw=!!raw;$('#email-content').innerHTML=`<div class="email" data-msg="0">${messageHTML(o,'',0)}</div>`;fillMessage($('#email-content [data-msg="0"]'),o,'')}
// A meeting, wherever it is opened (a timeline, Events, a to-do's source, a search): the Calendar's own details, with its
// Notes, Transcript and Generate notes, and its invite one tap away. When the meeting can't be read that way, its invite.
async function openMeeting(ev,title){let m=null;try{m=(await request('api/meeting?event='+encodeURIComponent(ev))).meeting}catch(e){errCaught(e)}
 if(!m){openOriginal(ev,title,true);return}if($('#email-dialog').open)$('#email-dialog').close();calView(m)}
$('#email-content').addEventListener('click',e=>{const b=e.target.closest('[data-open-meeting]');if(b)openMeeting(b.dataset.openMeeting,'')});
// A conversation from the Graph: its messages in order, each who said it, when and the whole text.
async function openConversation(row){const dialog=$('#email-dialog'),group='group' in row.dataset;$('#email-title').textContent=row.dataset.title||'Conversation';$('#email-content').innerHTML='<p class="muted">Loading…</p>';dialog.showModal();
let list;try{list=(await request('api/originals?events='+encodeURIComponent(row.dataset.events))).originals}catch(e){errCaught(e);$('#email-content').innerHTML=`<p class="muted">${esc(e.message)}</p>`;return}
if(!list.length){$('#email-content').innerHTML='<p class="muted">The messages are no longer available.</p>';return}
/* A transcript: the date once, then turns; a turn is one sender's messages minutes apart, its time said once */
let h=`<p class="convo-day">${esc(new Date(list[0].occurred_at).toLocaleDateString(DL,{weekday:'long',day:'numeric',month:'long'}))}</p>`,prev=null;
for(const o of list){const me=o.from==='You',at=Date.parse(o.occurred_at),same=prev&&prev.from===o.from&&at-Date.parse(prev.occurred_at)<5*6e4;
 if(!same)h+=(prev?'</div>':'')+`<div class="convo-turn${me?' me':''}"><p class="convo-meta">${!me&&group?`<b>${esc(sender(o.from)||'')}</b> · `:''}${esc(graphTime(new Date(at)))}</p>`;
 h+=`<div class="convo-say">${linkify(String(o.body||'').replace(/\r\n/g,'\n').trim())}</div>`;prev=o}
const url=[...list].reverse().find(o=>o.url)?.url;
$('#email-content').innerHTML=`<div class="convo">${h}</div>${url?`<a class="convo-source" href="${esc(url)}" target="_blank" rel="noreferrer">Open in ${esc(row.dataset.src||'the source')}</a>`:''}</div>`}
$('#query').onkeydown=e=>{if(e.key==='Enter')search()};
// Messages, the results page: everything the Machine read, by meaning and by words, every account or one. It isn't in
// the sidebar: the palette's See all results (and a message there), G then E and #messages (#events) open it; an empty
// search shows the newest.
function msgSearch(q){$('#query').value=q||'';$('#results').innerHTML='<p class="muted">Loading…</p>';showTab('events');search();scrollTo(0,0)}
function msgOpen(m){if(m.kind==='calendar.event')openMeeting(m.id,m.title);else openEvent(m.id,m.title)}
// who it's from by name only ("Ana Ruiz <ana@x.example>" reads Ana Ruiz; a bare address stays), then when
const msgSub=m=>[String(m.metadata?.from||m.metadata?.sender_display||m.metadata?.channel_name||m.metadata?.chat_name||'').replace(/^\s*"?([^"<]*?)"?\s*<[^>]*>\s*$/,(all,n)=>n.trim()||all),when(m)].filter(Boolean).join(' · ');
