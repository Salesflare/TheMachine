// The messages behind each card, read in a dialog. HTML renders in a sandboxed frame:
// no scripts, forms or navigation of the dashboard; links open outside (events-email-frame.js).
const originals=new Map(),emailViews=new Map(),around=new Map();  // around: what was said around a to-do's source message
const fileSize=b=>!b?'':b<1024?b+' B':b<1048576?Math.round(b/1024)+' KB':(b/1048576).toFixed(1)+' MB';
// A mailing list's rewrite as people say it: Google Groups' "'Sam Lee' via Sales" is "Sam Lee via Sales", and a group named
// after its address ("info@acme.com readers") is that address (assistant.group_sender).
const groupSender=v=>{const m=/^'(.+)' via (.+)$/.exec(v);if(!m)return v;const at=/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+/.exec(m[2].trim());return `${m[1].trim()} via ${at?at[0]:m[2].trim()}`};
const sender=v=>groupSender(String(v||'').replace(/\s*<[^>]+>/,'').replace(/^"|"$/g,'').trim())||String(v||'');
const linkify=t=>html`${String(t??'').split(/(https?:\/\/[^\s<>"']+[^\s<>"'.,;:!?)\]])/g).map((x,i)=>i%2?html`<a href="${x}" target="_blank" rel="noreferrer">${x}</a>`:x)}`;
const apiURL=path=>new URL(path,document.baseURI).href;
// Any card built from collected messages can show them, including older cards without a source line.
const eventIds=s=>{try{return Array.isArray(s.event_ids)?s.event_ids:JSON.parse(s.event_ids||'[]')}catch{return []}};
// Each service by its own logo (dashboard.html --i-*): where a to-do came from and what its prepared step goes out on.
// An email or a calendar change by the account's service: Google's own logo; Outlook and the rest the plain envelope.
const svcOf=id=>(state?.connectors||[]).find(c=>c.id===id)?.service||'';
const VIA_NAME={gmail:'Gmail',mail:'Email',slack:'Slack',whatsapp:'WhatsApp',telegram:'Telegram',signal:'Signal',linkedin:'LinkedIn',x:'X',intercom:'Intercom',gdocs:'Google Docs',file:'Doc',gcal:'Google Calendar',cal:'Calendar',handoff:'Hand off',browser:'Browser',github:'GitHub'};
// On a button that already says what it does, the logo is only a picture (hidden from screen readers).
const viaIco=(k,quiet)=>k?quiet?html`<i class="via-ico via-${k}" aria-hidden="true"></i>`:html`<i class="via-ico via-${k}" role="img" aria-label="${t(VIA_NAME[k]||service(k)||'The source')}" title="${t(VIA_NAME[k]||service(k)||'The source')}"></i>`:'';
const STEP_VIA={slack:'slack',whatsapp:'whatsapp',telegram:'telegram',signal:'signal',linkedin:'linkedin',x:'x',intercom:'intercom',handoff:'handoff',finish:'browser'};
// A final step on GitHub that runs with gh or a GitHub MCP server (github_route.py) shows GitHub's logo, else the browser.
// Mail and calendar steps by their account: Gmail or Outlook, Google or Outlook Calendar, else the plain line icon
const mailVia=svc=>['gmail','outlook'].includes(svc)?svc:'mail',calVia=svc=>svc==='calendar'?'gcal':svc==='outlook_calendar'?svc:'cal';
const actionVia=a=>a?.kind==='finish'&&['gh','mcp'].includes(a.via)?'github':['email','email_demo'].includes(a?.kind)?mailVia(svcOf(a.account_id)):a?.kind==='calendar'?calVia(svcOf(a.account_id)):['doc_write','doc_reply'].includes(a?.kind)?(a.provider==='microsoft'?'docs':'gdocs'):STEP_VIA[a?.kind]||'';
// A to-do's source by its words ("Source: Slack …"), else the service of the account it came from (todos-logos.js MONO)
const cardViaIcon=s=>{const v=(/^Source:\s*([^·\n]+)/i.exec(s.source_line||'')?.[1]||'').trim(),svc=(Array.isArray(s.account_ids)?s.account_ids:(()=>{try{return JSON.parse(s.account_ids||'[]')}catch{return []}})()).map(svcOf);
 if(isEmail(s)||/^(email|gmail|outlook|mail)\b/i.test(v))return (s.original_urls||[]).some(u=>/^https:\/\/mail\.google\.com\//.test(u))||svc.includes('gmail')&&!svc.includes('outlook')?'gmail':svc.includes('outlook')||(s.original_urls||[]).some(u=>/^https:\/\/outlook\./.test(u))?'outlook':'mail';
 const named=[['slack',/^slack\b/i],['whatsapp',/^whatsapp\b/i],['telegram',/^telegram\b/i],['signal',/^signal\b/i],['linkedin',/^linkedin\b/i],['x',/^x( message)?\b/i],['intercom',/^intercom\b/i],['gdocs',/^(doc |suggested edit)/i],
  ['teams',/^(microsoft )?teams\b/i],['zoom',/^zoom\b/i],['google_meet',/^(google )?meet\b/i],['github',/^github\b/i],['stripe',/^stripe\b/i],['salesflare',/^salesflare\b/i],['salesforce',/^salesforce\b/i],['trello',/^trello\b/i],['shortcut',/^shortcut\b/i]].find(([,r])=>r.test(v));
 return named?named[0]:/^your fleet$/i.test(v)?'handoff':/note/i.test(v)?'note':/calendar/i.test(v)?calVia(svc.find(x=>/calendar/.test(x))):svc.map(x=>x==='calendar'?'':monoKey(x)).find(Boolean)||'chat'};
// A card the owner added has their own words as its only signal until the review links an email: nothing to open yet.
const hasOriginal=s=>Boolean(s.source_line||(!['owner','machine'].includes(s.origin)&&eventIds(s).length)||(s.original_urls||[]).length);  // machine: an update's note, no thread
// A meeting's notes lead ("Source: notes from Board meeting", meeting_mail.py): not an email, even with its notes mail among the originals
const isEmail=s=>/^Source: email/.test(s.source_line||'')||!/^Source: notes from /.test(s.source_line||'')&&(s.original_urls||[]).some(u=>/^https:\/\/(mail\.google\.com|outlook\.(office|office365|live)\.com)\//.test(u));
const originalsFor=id=>{if(!originals.has(id))originals.set(id,request('api/originals?id='+id).then(r=>{around.set(id,r.around||null);return r.originals}).catch(e=>{originals.delete(id);throw e}));return originals.get(id)};
// How each kind of message reads (its header, text, a chat as one thread) is the lazy part 'msgview' (events-message.js):
// the viewer loads it with the message, so the first load doesn't carry it.
// Files attached to this card's email draft, as links that open over the Tailscale dashboard.
const draftFileLinks=(id,files)=>html`${(files||[]).map(a=>html`<a class="attachment" href="${'api/draft-attachment?id='+encodeURIComponent(id)+'&sha='+encodeURIComponent(a.sha256)}" target="_blank" rel="noreferrer">📎 ${a.name}<small>${fileSize(a.size)}</small></a>`)}`;
const draftFiles=s=>{const seen=new Set();return taskActions(s).filter(a=>['email','email_demo'].includes(a.kind)).flatMap(a=>a.attachments||[]).filter(a=>!seen.has(a.sha256)&&seen.add(a.sha256))};
const draftFilesBlock=s=>{const files=draftFiles(s);return files.length?html`<div class="draft-files"><h3>Attached to your draft</h3><div class="attachments">${draftFileLinks(s.id,files)}</div></div>`:''};
const emailViewFor=(id,ev)=>{const key=id+':'+ev;if(!emailViews.has(key))emailViews.set(key,request(`api/email?id=${id}&event=${encodeURIComponent(ev)}`).catch(e=>{emailViews.delete(key);return {html:'',failed:e?.status!==404||!!e.retry}}));return emailViews.get(key)};
// Cards on screen read their email ahead, quietly: two at a time when the browser is idle, each card once, the last
// PREFETCH_KEEP kept. Opening one is then instant.
const PREFETCH_KEEP=30,prefetchQueue=[],prefetched=new Set();let prefetching=0;
const idle=f=>(window.requestIdleCallback||(g=>setTimeout(g,200)))(f);
function trim(map){while(map.size>PREFETCH_KEEP)map.delete(map.keys().next().value)}
function prefetchNext(){while(prefetching<2&&prefetchQueue.length){const id=prefetchQueue.shift();prefetching++;
 idle(async()=>{try{const list=await originalsFor(id),first=list[0];if(first?.kind==='email')await emailViewFor(id,first.event_id);trim(originals);trim(emailViews);trim(around)}catch{prefetched.delete(id)}finally{prefetching--;prefetchNext()}})}}
// A to-do's source sits behind Details: the to-do itself coming into sight reads its original ahead.
const prefetchSeen=window.IntersectionObserver?new IntersectionObserver(entries=>{for(const e of entries){if(!e.isIntersecting)continue;prefetchSeen.unobserve(e.target);const id=e.target.dataset.id||e.target.querySelector('[data-original="read"][data-id]')?.dataset.id;
 if(id&&!prefetched.has(id)&&!originals.has(id)){prefetched.add(id);prefetchQueue.push(id)}}prefetchNext()},{rootMargin:'100px'}):null;
let prefetchScan=0;if(prefetchSeen)new MutationObserver(()=>{cancelAnimationFrame(prefetchScan);prefetchScan=requestAnimationFrame(()=>{for(const b of document.querySelectorAll('[data-original="read"][data-id]'))if(!prefetched.has(b.dataset.id))prefetchSeen.observe(b.closest('.card-details')?b.closest('article'):b)})}).observe(document.body,{childList:true,subtree:true});
async function openEmail(id,{keep}={}){const s=state.suggestions.find(s=>s.id===id);const dialog=$('#email-dialog');
if(!keep){$('#email-title').textContent=s?.title||'Original';setHTML($('#email-content'),html`<p class="muted">Loading…</p>`);dialog.showModal()}
let list;try{[list]=await Promise.all([originalsFor(id),lazyPart('msgview')])}catch(e){errCaught(e);setHTML($('#email-content'),html`<p class="muted">${e.message}</p>`);return}
if(!list.length){setHTML($('#email-content'),html`${draftFilesBlock(s)}<p class="muted">The original is no longer available.</p>`);return}
const [first,...rest]=list,near=nearOf(id,list),all=[...list,...near.before,...near.after],at=o=>all.indexOf(o);
if(first.kind==='calendar'&&!rest.length&&!draftFiles(s||{}).length){openMeeting(first.event_id,s?.title);return}  // a to-do from a meeting: the meeting itself
const box=$('#email-content'),wire=()=>{box.querySelectorAll('details.email').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)fillMessage(d,all[+d.dataset.msg],id)}));
 box.querySelector('[data-convo-earlier]')?.addEventListener('click',e=>showEarlier(id,e.currentTarget))};
const inView=()=>{if(!keep)box.querySelector('.convo-main,.email-main')?.scrollIntoView({block:box.querySelector('.convo-main')?'center':'start'})};
// A chat to-do: its conversation as one thread, with what was said around it (its other conversations after it); anything else still as related messages
if(isChat(first)){const others=list.filter(o=>!isChat(o)),main=near.main??first.event_id;
 setHTML(box,html`${draftFilesBlock(s)}${chatThreads([...list,...near.before,...near.after]).map(c=>chatThreadHTML(c,{main,earlier:near.earlier&&c.some(o=>o.event_id===main)}))}${others.length?html`<h3 class="email-earlier">${t(['{} related message','{} related messages'],others.length)}</h3>${others.map(o=>html`<details class="email" data-msg="${at(o)}"><summary>${sender(o.from)||kindLabel(o.kind)} · ${localeDate(new Date(o.occurred_at),DL,{day:'numeric',month:'short'})}</summary>${messageHTML(o,id,at(o))}</details>`)}`:''}`);
 wire();inView();return}
// An email: the thread's earlier mail folded above it and the replies below, the to-do's own one open and marked
const chats=rest.filter(isChat),mails=rest.filter(o=>!isChat(o)),threaded=near.before.length||near.after.length||near.earlier;
setHTML(box,html`${draftFilesBlock(s)}${near.earlier?earlierButton():''}${near.before.map(o=>emailRow(o,at(o)))}<div class="email${threaded?' email-main':''}" data-msg="0"${threaded?html` aria-label="${t('The message this to-do is about')}"`:''}>${messageHTML(first,id,0,s?.title)}</div>${near.after.map(o=>emailRow(o,at(o)))}${mails.length?html`<h3 class="email-earlier">${t(['{} related message','{} related messages'],mails.length)}</h3>${mails.map(o=>html`<details class="email" data-msg="${at(o)}"><summary>${sender(o.from)||kindLabel(o.kind)} · ${localeDate(new Date(o.occurred_at),DL,{day:'numeric',month:'short'})}</summary>${messageHTML(o,id,at(o))}</details>`)}`:''}${chatThreads(chats).map(c=>chatThreadHTML(c))}`);
fillMessage(box.querySelector('[data-msg="0"]'),first,id);wire();inView()}
// The link to an event in its own calendar: Google Calendar, Outlook, or another one
const calOpenLabel=url=>{let h='';try{h=new URL(url).hostname}catch{}return /(^|\.)google\.com$/.test(h)?'Open in Google Calendar ↗':/(^|\.)(outlook\.(com|office\.com|office365\.com|live\.com)|office\.com|live\.com)$/.test(h)?'Open in Outlook ↗':'Open in its calendar ↗'};
