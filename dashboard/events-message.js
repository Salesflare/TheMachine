// A lazy part (dashboard_parts.LAZY 'msgview'): how a message reads in the viewer, by its kind. events-email.js
// openEmail, events-list.js openOriginal and openSources, and graph-record.js openTeamThread load it with
// lazyPart('msgview') before they draw a message.
// What a source is, when nobody sent it: never the raw kind ("calendar"), and never "Signal" for a kind nothing names
// (source_kind's 'signal'), which reads as the Signal app
const KIND_LABEL={calendar:'Meeting invite',email:'Email',phone:'Phone',signal:'Original',note:'Note',message:'Message'};
const kindLabel=k=>t(KIND_LABEL[k]||k||'Original');
// A message reads by its view (machine/store/message_view.py: email, chat, notification or card), and says each thing
// once: the dialog's title, the header, Details and the body never repeat each other (sameText). `shown`: the dialog's
// title, so a subject or a title that is already up there isn't said again.
const sameText=(a,b)=>{const n=s=>String(s??'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim();return !!n(a)&&n(a)===n(b)};
// "Sam Lee <sam@x.example>, lee@y.example" as [{name,addr}]
const mailPeople=v=>{const out=[];String(v||'').replace(/(?:"([^"]*)"|([^,<"]*?))\s*<([^<>\s]+@[^<>\s]+)>|([^\s,<>"]+@[^\s,<>"]+)/g,(m,q,n,addr,bare)=>{out.push({name:groupSender((q??n??'').trim()),addr:(addr||bare).trim()});return ''});return out};
// '"a@x" <a@x>' has no name; Details writes "Sam Lee <sam@x>", else the address
const mailName=p=>p.name&&!sameText(p.name,p.addr)&&!/^\S+@\S+$/.test(p.name)?p.name:'';
const mailFirst=p=>{const n=mailName(p);return n&&!n.includes('@')?n.split(/\s+/)[0]:p.addr};
const mailFull=p=>{const n=mailName(p);return n?`${n} <${p.addr}>`:p.addr};
const msgWhen=o=>html`<time datetime="${o.occurred_at}">${fmtDHM(o.occurred_at,{weekday:'short',day:'numeric',month:'short'})}</time>`;
// The title a message opens under: an email's subject, a chat's conversation, a notification's own title or its app
const viewTitle=o=>isChat(o)||o.view==='chat'?o.subject||chatTitle(o)||o.app||'':o.view==='notification'?o.title||o.app_name||'':o.title||'';
// Where it opens outside, named as the to-do cards name it: "Open in Salesflare ↗"
// (a Gmail message on a phone: its phone_url, the conversation on Gmail's mobile site; the desktop link lands in the inbox there)
// with the source's own mono icon, as on the to-do cards (via-* in todos-chat.css)
const OPEN_VIA={gmail:'gmail',slack:'slack',whatsapp:'whatsapp',telegram:'telegram',linkedin:'linkedin',x:'x',intercom:'intercom',github:'github',docs:'gdocs',calendar:'gcal'};
const outlookURL=u=>/^https:\/\/outlook\./.test(u);  // Outlook mail reads as gmail.message too: its link says which
const openVia=o=>'via-'+(o.source==='gmail.message'&&outlookURL(o.url)?'outlook':OPEN_VIA[o.source?kindService(o.source):'']||(o.view==='email'||o.kind==='email'?'mail':'link'));
const openLink=o=>!o.url||!safeURL(o.url)?'':html`<p class="email-open"><a class="read-original ${openVia(o)}" href="${onPhone()&&safeURL(o.phone_url||'')||o.url}" target="_blank" rel="noreferrer">${o.kind==='calendar'?t(calOpenLabel(o.url)):o.app?t('Open in {} ↗',o.app):o.kind==='email'?t('Open in {} ↗',outlookURL(o.url)?'Outlook':'Gmail'):t('Open original')}</a></p>`;
const attachmentsHTML=(o,id)=>(o.attachments||[]).length?html`<div class="attachments">${o.attachments.map(a=>html`<a class="attachment" href="api/attachment?id=${id}&event=${encodeURIComponent(o.event_id)}&part=${encodeURIComponent(a.part)}" target="_blank" rel="noreferrer">📎 ${a.name}<small>${fileSize(a.size)}</small></a>`)}</div>`:'';
const srcIcon=o=>o.source?html`<span class="icon">${markIco(sourceMark(o.source,o.account_id,o.app))}</span>`:'';
// An email: the sender by name with the address quiet, "to Dana, Mira", the date, and the subject only when the
// dialog's title isn't it already. A name that already says the address ("Sam via sales@…") has none after it.
// Details only with rows the header lacks: To/Cc when a name hides an address, Bcc, Reply-To, Sent via (details_only).
function mailHead(o,shown){const [f]=mailPeople(o.from),name=f?.name||sender(o.from),addr=f&&f.name&&!sameText(f.name,f.addr)&&!f.name.toLowerCase().includes(f.addr.toLowerCase())?f.addr:'';
 const to=mailPeople(o.to),cc=mailPeople(o.cc),list=ps=>ps.map(mailFirst).join(', ');
 const line=[to.length?t('to {}',list(to)):'',cc.length?t('cc {}',list(cc)):''].filter(Boolean).join(' · ');
 const adds=ps=>ps.some(p=>mailFull(p)!==mailFirst(p)),full=ps=>ps.map(mailFull).join(', ');
 const rows=[[t('To'),adds(to)&&full(to)],[t('Cc'),adds(cc)&&full(cc)],[t('Bcc'),full(mailPeople(o.bcc))],[t('Reply to'),full(mailPeople(o.reply_to))],[t('Sent via'),o.sent_via||'']]
  .filter(([,v])=>v).map(([k,v])=>html`<div><span>${k}</span> ${v}</div>`);
 const meta=[...rows,o.details?html`<pre class="email-tech">${o.details}</pre>`:''].filter(Boolean);
 return html`<div class="email-meta"><div class="email-from"><span class="email-who"><strong translate="no">${name||kindLabel(o.kind)}</strong>${addr?html` <span class="email-addr" translate="no">${addr}</span>`:''}</span>${msgWhen(o)}</div>${line?html`<div class="email-to" translate="no">${line}</div>`:''}${o.title&&!sameText(o.title,shown)?html`<div class="email-subject" translate="no">${o.title}</div>`:''}${meta.length?html`<details class="email-headers"><summary>${t('Details')}</summary>${meta}</details>`:''}</div>`}
// A notification: its app with its icon and the time, then its title (when the dialog's title isn't it) and text, once each
function noteHead(o,shown){const app=o.app_name||o.app||kindLabel(o.kind);
 return html`<div class="email-meta"><div class="email-from"><span class="msg-app">${srcIcon(o)}${sameText(app,shown)?'':html`<strong translate="no">${app}</strong>`}</span>${msgWhen(o)}</div>${o.title&&!sameText(o.title,shown)?html`<div class="msg-note-title" translate="no">${o.title}</div>`:''}</div>`}
// GitHub's reasons a notification came (message_view.GITHUB_REASONS)
const GH_REASON={author:'You opened it',mention:'Mentioned',team_mention:'Your team was mentioned',review_requested:'Review requested',assign:'Assigned to you',comment:'You commented',state_change:'You changed its state',subscribed:'You follow it',security_alert:'Security alert',invitation:'Invitation',ci_activity:'CI activity'};
const GH_STATE={open:'Open',closed:'Closed',merged:'Merged',draft:'Draft'};
const botTag=bot=>bot?html` <span class="msg-bot">${t('Bot')}</span>`:'';
// An item with a state (an issue, a deal, a payment, a doc comment): where it is, its state, who, why, the time
function cardHead(o,shown){const c=o.card||{},state=GH_STATE[c.state];
 const bare=(n,bot)=>bot?String(n).replace(/\[bot\]$/i,''):n;  // the Bot tag says it: "sweeper Bot", not "sweeper[bot] Bot"
 const who=c.comment_by?html`${t('Comment by {}',bare(c.comment_by,c.comment_bot))}${botTag(c.comment_bot)}`:c.author?html`${t('By {}',bare(c.author,c.bot))}${botTag(c.bot)}`:o.from&&!sameText(o.from,shown)?html`${sender(o.from)}`:'';
 return html`<div class="email-meta"><div class="email-from"><span class="msg-app">${srcIcon(o)}<strong translate="no">${c.ref||o.app||kindLabel(o.kind)}</strong>${state?html`<span class="msg-state msg-${c.state}">${t(state)}</span>`:''}</span>${msgWhen(o)}</div>${who?html`<div class="email-to" translate="no">${who}</div>`:''}${c.reason&&GH_REASON[c.reason]?html`<div class="msg-why">${t(GH_REASON[c.reason])}</div>`:''}${o.title&&!sameText(o.title,shown)?html`<div class="email-subject" translate="no">${o.title}</div>`:''}${o.details?html`<details class="email-headers"><summary>${t('Details')}</summary><pre class="email-tech">${o.details}</pre></details>`:''}</div>`}
function messageHTML(o,id,i,shown){
const head=o.view==='notification'?noteHead(o,shown):o.view==='card'?cardHead(o,shown):mailHead(o,shown);
return html`${head}${attachmentsHTML(o,id)}<div class="email-body" data-email-body="${i}"><p class="muted">Loading…</p></div>${o.context?html`<details class="msg-context"><summary>${t('Description')}</summary><div class="msg-md">${chatMarkdown(o.context)}</div></details>`:''}${o.kind==='calendar'&&!o.raw?html`<p class="email-open"><button type="button" class="link" data-open-meeting="${o.event_id}">${t('Notes and transcript')}</button></p>`:''}${openLink(o)}`}
// Plain text in paragraphs: a blank line starts one, quoted lines ("> …") and a signature after "-- " read quieter
function mailText(said){const blocks=[];let sig=false;
 for(const para of said.split(/\n\s*\n/)){const lines=para.split('\n');if(/^--\s?$/.test(lines[0]))sig=true;
  const quoted=lines.every(l=>/^\s*>/.test(l)),text=quoted?lines.map(l=>l.replace(/^\s*>\s?/,'')).join('\n'):para;
  blocks.push(html`<p class="${quoted||sig?'email-quiet':''}">${linkify(text)}</p>`)}
 return html`<div class="email-text">${blocks}</div>`}
// Long bodies fold behind Show more, so a long issue or thread isn't a wall
function foldLong(box){if(box.classList.contains('msg-fold-open')||box.nextElementSibling?.classList.contains('msg-more'))return;box.classList.add('msg-folded');
 if(box.scrollHeight<=box.clientHeight+40){box.classList.remove('msg-folded');return}
 const b=document.createElement('button');b.type='button';b.classList.add('link','msg-more');b.textContent=t('Show more');b.onclick=()=>{box.classList.remove('msg-folded');box.classList.add('msg-fold-open');b.remove()};box.after(b)}
async function fillMessage(container,o,id){
const box=container.querySelector('.email-body');if(!box||box.dataset.filled)return;box.dataset.filled='1';
const said=String(o.body||'').replace(/\r\n/g,'\n').split('\n').filter(l=>!(o.kind==='calendar'&&/^Participants: /.test(l))).join('\n').trim();  // an invite's raw guest addresses: the meeting's With has them by name
const text=()=>{setHTML(box,said?o.format==='markdown'?html`<div class="msg-md">${chatMarkdown(said)}</div>`:mailText(said):o.view==='notification'||o.view==='card'&&o.card?'':html`<p class="muted">${t('No description.')}</p>`);requestAnimationFrame(()=>foldLong(box))};
if(o.kind!=='email'||o.near){text();return}  // a message around the source reads as its stored text
const view=await emailViewFor(id,o.event_id);if(!view.html){text();if(view.failed)emailRetry(container,box,o,id);return}
lazyPart('emailframe').then(()=>emailFrame(box,view,o,id),text)}  // its frame (events-email-frame.js)
// The full email didn't come (Gmail or the Machine didn't answer): the saved text stays, with one line to try again.
// Not when there is no full email to read (an email from another provider): that is the saved text alone.
function emailRetry(container,box,o,id){const p=document.createElement('p');p.className='email-retry muted';
setHTML(p,html`${t('Couldn’t load the full email.')} <button type="button" class="link" data-email-retry>${t('Try again')}</button>`);box.append(p);
p.querySelector('button').onclick=()=>{delete box.dataset.filled;setHTML(box,html`<p class="muted">Loading…</p>`);fillMessage(container,o,id)}}
// Chats (Slack, WhatsApp, Telegram, Intercom and the rest: event_views' chat) read as one thread, oldest first: the
// conversation named once on top (it stays in view while the thread scrolls), a day line when the day changes, each
// sender's run of messages under their name and time once, a light time inside a run only after a pause. The to-do's
// own message is outlined under a "This to-do" line when the thread holds more, and the viewer opens on it.
// A Slack thread shown after the channel's messages before it (thread: true, machine/store/conversation.py) starts
// under an In thread line. Each sender has the avatar circle with their initials, as people have elsewhere.
// One link opens the whole thread where it lives. Slack's :emoji: codes read as emoji (chatEmoji).
const THREAD_APP={Slack:'Slack',WhatsApp:'WhatsApp',Telegram:'Telegram',Signal:'Signal',Intercom:'Intercom',LinkedIn:'LinkedIn','X message':'X',Teams:'Teams'};
const THREAD_VIA={Slack:'slack',WhatsApp:'whatsapp',Telegram:'telegram',Signal:'signal',Intercom:'intercom',LinkedIn:'linkedin','X message':'x',Teams:'teams'};
// Messenger chats (convo-im, events-message.css) read like their app: the other side's bubbles on the left under their
// name and avatar, the owner's on the right in the accent, each bubble with its own time. Slack and Intercom keep a
// run's time on its name line.
const THREAD_IM=new Set(['WhatsApp','Telegram','Signal','LinkedIn','X message','Teams']);
const isChat=o=>typeof o?.chat==='string';
const chatTitle=o=>o.dm&&o.chat?t('DM with {}',o.chat):o.chat||'';
const THREAD_PAUSE=10*6e4;
const senderInitials=name=>{const w=String(name||'').trim().split(/\s+/).filter(x=>/^\p{L}/u.test(x));return((w[0]?.[0]||[...String(name||'?')][0])+(w.length>1?w.at(-1)[0]:'')).toUpperCase()};
// A photo, video or file a chat message sent without a caption (message_view.media_shown: its text only said "Sent
// image"): a chip with what it is, never those words as a message. A photo the Machine kept shows itself instead.
// each kind's icon class written out whole, so the lazy CSS check (tests/test_dashboard_parts.py) finds it here
const MEDIA_LABEL={photo:['convo-m-photo',()=>t('Photo')],video:['convo-m-video',()=>t('Video')],audio:['convo-m-audio',()=>t('Audio')],
 voice:['convo-m-voice',()=>t('Voice message')],sticker:['convo-m-sticker',()=>t('Sticker')],file:['convo-m-file',()=>t('File')]};
const mediaChip=m=>{const [ico,label]=MEDIA_LABEL[m]||MEDIA_LABEL.file;return html`<span class="convo-media"><i class="convo-media-ico ${ico}" aria-hidden="true"></i>${label()}</span>`};
// A link on a line of its own, or ending one, reads as a card under the text: the page's name from its address when the
// address carries one (".../p/oak-desk-lamp-with-dimmer/930..." is "Oak desk lamp with dimmer") over the site, else
// the site and path, shortened. Three links to one shop read as three things, never three bare "shop.example"s.
const LINK_END=/^(.*?)\s*\b(https?:\/\/[^\s<>"'`]+?)[.,;:!?)]*\s*$/;
function chatLinks(text){const keep=[],links=[];
 for(const line of String(text).split('\n')){const m=LINK_END.exec(line);
  if(m&&safeURL(m[2])&&!/\]\($/.test(m[1])){if(m[1].trim())keep.push(m[1]);links.push(m[2])}else keep.push(line)}
 return {text:keep.join('\n').trim(),links}}
const linkName=u=>{let x;try{x=new URL(u)}catch{return ''}
 const seg=x.pathname.split('/').map(s=>{try{return decodeURIComponent(s)}catch{return s}}).reverse()
  .find(s=>/^[\p{L}\p{N}]+(?:[-_+][\p{L}\p{N}]+){2,}(?:\.html?)?$/u.test(s)&&!/^[\da-f-]+$/i.test(s)&&(s.match(/\p{L}{2,}/gu)||[]).length>=3);
 if(!seg)return '';const w=seg.replace(/\.html?$/,'').split(/[-_+]+/).filter(w=>!/^\d{4,}$/.test(w)).join(' ');return w.charAt(0).toUpperCase()+w.slice(1)};
const linkSite=u=>{try{return new URL(u).hostname.replace(/^www\./,'')}catch{return ''}};
const linkWhere=u=>{try{const x=new URL(u),s=linkSite(u)+x.pathname.replace(/\/+$/,'');return s.length>44?s.slice(0,43)+'…':s}catch{return u}};
const linkCard=u=>{const name=linkName(u);return html`<a class="convo-link" href="${u}" target="_blank" rel="noreferrer" title="${u}">${name?html`<span class="convo-link-name">${name}</span>`:''}<span class="convo-link-site"><i class="via-ico via-link" aria-hidden="true"></i><span>${name?linkSite(u):linkWhere(u)}</span></span></a>`};
// A day line as people say it: Today, Yesterday, else the date
const convoDay=at=>{const d=new Date(at),n=Math.round((new Date().setHours(0,0,0,0)-new Date(at).setHours(0,0,0,0))/864e5);
 return n===0?t('Today'):n===1?t('Yesterday'):localeDate(d,DL,{weekday:'long',day:'numeric',month:'long',...(d.getFullYear()!==new Date().getFullYear()?{year:'numeric'}:{})})};
function chatThreadHTML(items,{main,names=true,head=true,src,earlier,titled}={}){
const msgs=items.flatMap(o=>o.turns?.length?o.turns.map(x=>({...x,kind:o.kind})):[o]).filter(o=>String(o.body||'').trim()||o.photo||o.media).sort((a,b)=>Date.parse(a.occurred_at)-Date.parse(b.occurred_at));
const first=items.find(o=>o.event_id===main)||items[0]||{},im=THREAD_IM.has(first.kind);
// a messenger's 1:1 (one other person, who the chat is named after) names nobody over the bubbles: the line on top does
const others=new Set(msgs.filter(o=>o.from!=='You'&&!o.role).map(o=>sender(o.from)).filter(Boolean)),firstWord=s=>String(s||'').trim().split(/\s+/)[0].toLowerCase();
const duo=im&&others.size<=1&&(first.dm||!first.chat||[...others].every(w=>sameText(w,first.chat)||firstWord(w)===firstWord(first.chat)));
const days=[];let prev=null,plain=false,inThread=false;
// The owner's side on the right: their own messages, and in a support chat (Intercom) the team's and its bot's, each named
for(const o of msgs){const at=Date.parse(o.occurred_at),day=convoDay(at),you=o.from==='You',me=you||o.role==='team'||o.role==='bot',mark=main!=null&&o.event_id===main&&msgs.length>1;
 if(days.at(-1)?.day!==day){days.push({day,turns:[]});prev=null}
 if(o.thread&&plain&&!inThread){days.at(-1).turns.push({thread:true});prev=null}
 inThread||=Boolean(o.thread);plain||=!inThread;
 const said=chatLinks(o.media_only?'':String(o.body||'').replace(/\r\n/g,'\n').trim()),only=!said.text&&!o.photo;
 const who=!you&&names?sender(o.from):'',turns=days.at(-1).turns,time=html`<time datetime="${o.occurred_at}">${fmtHM(at)}</time>`;
 const say=html`${o.note?html`<span class="convo-tag">${t('Note')}</span>`:''}${o.media?mediaChip(o.media):''}${said.text?chatMarkdown(said.text):''}${said.links.map(linkCard)}${o.photo?photoThumbs([o.photo]):''}`;
 if(!prev||prev.from!==o.from)turns.push({me,says:[],meta:im&&(me||!who||duo)?'':html`<p class="convo-meta">${who&&!me?html`<span class="convo-av" data-av="${senderInitials(who)}" aria-hidden="true"></span>`:''}${who?html`<b translate="no">${who}</b>${o.role==='bot'?html` <span class="msg-bot">${t('Bot')}</span>`:''}${im?'':' · '}`:''}${im?'':time}</p>`});
 else if(!im&&at-Date.parse(prev.occurred_at)>=THREAD_PAUSE)turns.at(-1).says.push(html`<p class="convo-at">${time}</p>`);
 if(mark)turns.at(-1).says.push(html`<p class="convo-this" aria-hidden="true">${t('This to-do')}</p>`);
 const kind=only&&o.media&&!said.links.length?' convo-say-media':only&&said.links.length?' convo-say-link':'';
 turns.at(-1).says.push(html`<div class="convo-say${kind}${mark?' convo-main':''}${o.note?' convo-note':''}"${mark?html` aria-label="${t('The message this to-do is about')}"`:''}>${im?html`<div class="convo-said">${say}</div><span class="convo-t">${time}</span>`:say}</div>`);prev=o}
// titled: the dialog's title names the conversation already, so the line above it names only the app (and its channel)
const app=THREAD_APP[first.kind]||first.app||src,title=titled?app:head?chatTitle(first):'';
const url=[first,...[...items].reverse()].find(o=>o?.url&&safeURL(o.url))?.url;
return html`<div class="convo${im?' convo-im':''}">${title?html`<p class="convo-chat">${viaIco(THREAD_VIA[first.kind],true)}<span translate="no">${title}</span>${im&&app&&!sameText(app,title)?html`<span class="convo-app">${app}</span>`:''}${first.via?html`<span class="msg-via">${t('via {}',first.via)}</span>`:''}</p>`:''}${earlier?earlierButton():''}${days.map(d=>html`<p class="convo-day"><span>${d.day}</span></p>${d.turns.map(x=>x.thread?html`<p class="convo-day convo-thread"><span>${t('In thread')}</span></p>`:html`<div class="convo-turn${x.me?' me':''}">${x.meta}${x.says}</div>`)}`)}${url?html`<a class="convo-source read-original ${openVia(first)}" href="${url}" target="_blank" rel="noreferrer">${app?t('Open in {} ↗',app):t('Open original')}</a>`:''}</div>`}
// A to-do's chat sources by conversation: the to-do's own conversation first, each one thread.
function chatThreads(list){const by=new Map();for(const o of list.filter(isChat)){const k=o.kind+'\u0000'+o.chat;if(!by.has(k))by.set(k,[]);by.get(k).push(o)}return [...by.values()]}
// A to-do's source opens with what was said around it (api/originals' around, machine/store/conversation.py): the
// messages before it and the replies after it, the source tinted and in view, and a quiet Show earlier for older ones.
const earlierButton=()=>html`<button type="button" class="link convo-earlier" data-convo-earlier>${t('Show earlier')}</button>`;
const nearOf=(id,list)=>{const c=around.get(id);if(!c)return {before:[],after:[]};const have=new Set(list.map(o=>o.event_id)),mark=o=>({...o,near:true}),keep=o=>o.event_id==null||!have.has(o.event_id);
 return {before:c.before.filter(keep).map(mark),after:c.after.filter(keep).map(mark),main:c.event_id,earlier:c.earlier}};
async function showEarlier(id,button){const c=around.get(id),from=c?.before.find(o=>o.event_id!=null)?.event_id??c?.event_id;if(!c||from==null)return;
 button.disabled=true;let r;try{r=(await request(`api/originals?id=${encodeURIComponent(id)}&before=${encodeURIComponent(from)}`)).around}catch(e){button.disabled=false;errCaught(e);toast(e.message,true);return}
 const dialog=$('#email-dialog'),fromEnd=dialog.scrollHeight-dialog.scrollTop;  // what was in view stays in view
 const seen=new Set(c.before.map(o=>o.event_id).filter(v=>v!=null)),live=new Set(c.before.filter(o=>o.event_id==null).map(o=>o.occurred_at+o.from));
 c.before=[...(r?.before||[]).filter(o=>o.event_id==null?!live.has(o.occurred_at+o.from):!seen.has(o.event_id)),...c.before];c.earlier=Boolean(r?.earlier);
 await openEmail(id,{keep:true});dialog.scrollTop=dialog.scrollHeight-fromEnd}
const peek=o=>String(o.body||'').replace(/\s+/g,' ').trim().slice(0,160);  // a folded email's first words, on one line
const emailRow=(o,i)=>html`<details class="email email-near" data-msg="${i}"><summary>${sender(o.from)||kindLabel(o.kind)} · ${localeDate(new Date(o.occurred_at),DL,{day:'numeric',month:'short'})}${peek(o)?html`<span class="email-peek">${peek(o)}</span>`:''}</summary>${messageHTML(o,'',i)}</details>`;
