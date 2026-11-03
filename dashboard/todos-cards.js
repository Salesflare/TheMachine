// The files the owner made the to-do with (New to-do): a chip each, opened from the Machine
const cardFiles=s=>(s.files||[]).length?`<div class="chat-files card-files">${s.files.map(f=>`<a class="agent-file via-file" href="api/chat-file?id=${encodeURIComponent(f.id)}" target="_blank" rel="noopener"${/^image\//.test(f.type)?'':` download="${esc(f.name)}"`}>${esc(f.name)}</a>`).join('')}</div>`:'';
function cardBody(s,section){const asked=section==='Chat'?'':askedBody(s);if(asked)return asked;const named=resultLinks(s);let text=s.step_stopped||named.text,lead='';
if(s.skill_proposal?.related)text=text.split(/\n\s*\n/).filter(p=>!p.trim().startsWith('Related to ')).join('\n\n');const m=text.match(/^\*\*([^*\n]+)\*\*\s*\n([\s\S]+)$/);if(m){lead=m[1];text=m[2].trim()}
const html=named.html((lead?`<p class="lead-line" translate="no">${esc(lead)}</p>`:'')+cardLinks(text.split(/\n\s*\n/).map(p=>p.trim()).filter(Boolean).map(p=>`<p>${format(p,true)}</p>`).join(''),s));
const proposal=skillProposal(s)+proposedSkillBox(s);
// Short by default: the status line says where it stands; the rest folds behind Show more.
const lines=2,per=innerWidth<600?38:72,rows=named.plain(text).split('\n').reduce((n,l)=>n+(l.trim()?Math.ceil(l.length/per):.6),0);
if(closed(s)||rows<=lines+.5)return `<div class="body" translate="no">${html}</div>${proposal}`;const open=expandedBodies.has(s.id);
return `<div class="body${open?'':' clamp'}" style="--lines:${lines}" translate="no">${html}</div><button type="button" class="more" data-more="${s.id}" aria-expanded="${open}">${open?'Show less':'Show more'}</button>${proposal}`}
const snoozedUntil=v=>new Date(v).toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'})+' at '+fmtHM(v);
// With a teammate who hasn't answered a handoff: Later is when it comes back to check in with them, not a snooze.
const checkinLabel=s=>'Check in with '+s.handoff_wait.name+' '+chatUntil(s.snoozed_until)+' if no answer';
const backLabel=v=>t('Back {}',fmtDHM(v,{weekday:'short',day:'numeric',month:'short'}))+' · '+ago(v);
// The stored line ("Source: email from Sam · Tue, Oct 27 (+2 more)") in the UI language. Its date is written again in
// the UI language in the region's order, whichever language it was stored in (English since the server writes the
// words in English, the owner's language before: "di 27 okt" reads "Tue 27 Oct" in English).
const SRC_MON=(()=>{const m={};for(const row of ['jan feb mar apr may jun jul aug sep oct nov dec','jan feb mrt apr mei jun jul aug sep okt nov dec',
 'janv févr mars avr mai juin juil août sept oct nov déc','jan feb märz apr mai juni juli aug sep okt nov dez','ene feb mar abr may jun jul ago sept oct nov dic',
 'gen feb mar apr mag giu lug ago set ott nov dic','jan fev mar abr mai jun jul ago set out nov dez'])row.split(' ').forEach((w,i)=>{m[w]=i});return m})();
const sourceDay=d=>{const m=/^[\p{L}.]+,?\s+(?:([\p{L}]+)\.?\s+(\d{1,2})|(\d{1,2})\.?\s+(?:de\s+)?([\p{L}]+)\.?)$/u.exec(d);if(!m)return d;const mon=SRC_MON[(m[1]||m[4]).toLowerCase()];if(mon==null)return d;
 const now=new Date(),at=new Date(now.getFullYear(),mon,+(m[2]||m[3]),12);if(at-now>864e5*31)at.setFullYear(at.getFullYear()-1);return at.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'})};
const sourceText=v=>{let s=String(v||'').replace(/^Source:\s*/i,''),more='';
 s=s.replace(/ \(\+(\d+) more\)$/,(_,n)=>{more=' '+t('(+{} more) (a source)',n);return ''});
 const i=s.lastIndexOf(' · '),head=i<0?s:s.slice(0,i),day=i<0?'':' · '+sourceDay(s.slice(i+3)),m=/^(.+?) from (.+)$/.exec(head),dm=/^Slack DM with (.+)$/.exec(head);
 const up=x=>x?x[0].toUpperCase()+x.slice(1):x,what=dm?t('Slack DM with {} (a source)',dm[1]):m?t('{} from {} (a source)',t(up(m[1])),m[2]):t(up(head));return up(what)+day+more};
const sourceHtml=v=>{const t=sourceText(v),i=t.lastIndexOf(' · ');return html`<span class="src">${i<0?t:html`${t.slice(0,i+3)}<span class="src-date">${t.slice(i+3)}</span>`}</span>`};  // the date never splits over two lines
const syncError=v=>v==='android_feed_unavailable'?'Notification bridge unavailable':v==='android_offline'?'Phone disconnected':v==='android_notifications_unavailable'?'Phone notifications unavailable':v==='android_gateway_unavailable'?'OpenClaw connection unavailable':v?.startsWith('network')?'Connection problem':v==='timeout'?'Connection timed out':['slack:HTTP_429','slack_ratelimited'].includes(v)?'Slack rate limit':readableError(v);
// Error codes like linkedin_read_failed, in words: the source's name and what went wrong.
// Telegram chats stopped for a reason only the owner can fix: said on its card, never a silent gap (telegram_store.ERRORS)
const TELEGRAM_STOP={telegram_logged_out:'Logged out of Telegram',telegram_app_blocked:'Telegram stopped accepting the app ID'};
function readableError(v){if(!v)return 'Sync error';const m=/^([a-z]+)[_:](.+)$/.exec(v),name=m?service(m[1]):'',what=m?m[2]:v;
// The service busy (google_meet_http:HTTP_503, docs_drive:HTTP_429): the service by its full name, which can have a _ in it
const busy=/:HTTP_(5\d\d|429)$/.exec(v);if(busy){const k=Object.keys(SERVICE_NAMES).filter(s=>v.startsWith(s)).sort((a,b)=>b.length-a.length)[0],who=k?SERVICE_NAMES[k]:t('The source');
 return busy[1]==='429'?t('{} asked to slow down',who):t('{} had a problem on its side',who)}
if(/signed_out$/.test(what))return 'Signed out of '+name;
if(TELEGRAM_STOP[v])return TELEGRAM_STOP[v];
if(v==='docs_not_connected')return 'Reading docs needs its own OK';
if(v==='docs_no_signin')return 'Sign in with Microsoft for this address';
if(v==='google_meet_not_connected'||v==='google_meet_signin_expired')return 'Connect Google Meet again';
if(/google_signin_expired/.test(what))return name?t('Google sign-in for {} expired',name):t('Google sign-in for this account expired');
if(/microsoft_signin_pending|microsoft_broker_busy/.test(v))return 'Microsoft is still setting up access; it retries by itself';
if(/microsoft_signin_expired/.test(what))return name?t('Microsoft sign-in for {} expired',name):t('Microsoft sign-in for this account expired');
if(/browser_busy$/.test(what))return 'The browser was busy with another read';
if(/browser_unreachable$/.test(what))return 'The browser stopped answering; it restarts by itself';
if(/timeout$/.test(what))return t('{} was slow to answer',name||t('The source'));
if(/rate_?limit/.test(what))return t('{} asked to slow down',name||t('The source'));
if(/read_failed$/.test(what))return name?t('Couldn’t read {}',name):t('Couldn’t read the source');
if(/^HTTP_5/.test(what))return t('{} had a problem on its side',name||t('The source'));
const words=v.replace(/[_:]+/g,' ').trim();return words[0].toUpperCase()+words.slice(1)}
const SERVICE_NAMES={gmail:'Email',calendar:'Calendar',outlook:'Outlook',outlook_calendar:'Outlook Calendar',slack:'Slack',salesflare:'Salesflare CRM',whatsapp:'WhatsApp',telegram:'Telegram chats',linkedin:'LinkedIn',android:'Android notifications',gateway:'OpenClaw Gateway',github:'GitHub',intercom:'Intercom',zoom:'Zoom',google_meet:'Google Meet',trello:'Trello',stripe:'Stripe',rss:'Feed',docs:'Microsoft Word',shortcut:'Shortcut',x:'X'};
const service=v=>SERVICE_NAMES[v]||v;
const label=v=>({pending:'Needs your decision',accepted:'Accepted',prepared:'Ready for you',rejected:'Not needed',snoozed:'Later',instructions:'Changes requested',completed:'Done'}[v]||v);
const tone=v=>({pending:'amber',accepted:'lavender',instructions:'lavender',prepared:'mint',snoozed:'lavender',completed:'mint',rejected:'muted'}[v]||'muted');
// A blocker waiting on the owner (a sign-in in the kept tab) resumes with Continue; same rule as the service.
const retryLabel=r=>/\b(?:sign(?:ed)?[ -]?in|log(?:ged)?[ -]?in|signed out|2fa|two-factor|authenticator|passkey|tap continue)\b/i.test(r||'')&&!/try again/i.test(r||'')?'Continue':'Try again';
// One calm line at the top of a page, in a quiet card; with a button when there is somewhere to go (data: its data-* attributes).
const pageNotice=(text,button,data={},cls='')=>`<div class="notice-card${cls?' '+cls:''}" role="status"><span>${esc(text)}</span>${button?`<button type="button" class="head-link"${Object.entries(data).map(([k,v])=>` data-${k}="${esc(v)}"`).join('')}>${esc(button)}</button>`:''}</div>`;
const chip=(text,t)=>html`<span class="chip t-${t}"><span class="ct">${text}</span></span>`;
const chipNode=(text,tone)=>make('span',{class:`chip t-${tone}`},make('span',{class:'ct'},text));
// Deadlines in local days: overdue and today stand out; the rest read as a weekday or date.
function dueChip(s){if(!s.due||closed(s)||looksDone(s))return '';const today=new Date(localDay(new Date())+'T12:00'),due=new Date(s.due+'T12:00'),days=Math.round((due-today)/864e5);
 // With a time (New to-do's "15:00", "in 2 hours"): the time shows, and it is overdue from that moment
 const at=s.due_at?new Date(s.due_at):null,timed=at&&!isNaN(at),late=timed?at<new Date():days<0;
 const text=late?'Overdue':timed?'Due '+(days===0?'':at.toLocaleDateString(DL,days<7?{weekday:'short'}:{day:'numeric',month:'short'})+' ')+fmtHM(at)
  :days===0?'Due today':days===1?'Due tomorrow':'Due '+due.toLocaleDateString(DL,days<7?{weekday:'long'}:{day:'numeric',month:'short'});
 return html`<span class="chip t-${late||days<=0?'orange':days===1?'amber':'muted'}" title="Due ${due.toLocaleDateString(DL,{weekday:'long',day:'numeric',month:'long'})+(timed?' '+fmtHM(at):'')}">${text}</span>`}
const closed=s=>['completed','rejected'].includes(s.status);
// A done to-do keeps its title (what needed doing); how it ended goes under it: what went out has its own line
// (outboxLine), the sign that it was handled is this one.
const doneLine=s=>{if(s.status!=='completed')return '';let why='';try{why=JSON.parse(s.handled_hint||'{}').reason||''}catch{}
 return why?html`<p class="note status-line done-line">${t('Done: {}',why)}</p>`:''};
// A to-do that outlived its moment closed by itself (Store.expire_passed): when that was reads from the stored time, so
// "yesterday" is right on the day it is read, never a word saved the day before.
const expiredLine=s=>{const at=new Date(s.expires_at||'');if(!s.expired_at||isNaN(at))return '';const what=s.expires_what||'',hm=fmtHM(at),
 days=Math.round((new Date(localDay(new Date())+'T12:00')-new Date(localDay(at)+'T12:00'))/864e5);
 return days===0?t('No longer needed: {} was today at {}.',what,hm):days===1?t('No longer needed: {} was yesterday at {}.',what,hm)
  :t('No longer needed: {} was on {} at {}.',what,at.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'}),hm)};
// A to-do that looks done already: its run found it done, or a later message suggests it's handled (LOOKS_DONE_SQL in
// assistant.py). It waits in one quiet group above Done (lookDoneList), is never late and never counts as waiting for
// you. Only you close it.
const looksDone=s=>!closed(s)&&s.status!=='snoozed'&&(!!s.handled_hint||s.status==='prepared'&&(()=>{try{return JSON.parse(s.outcome||'{}')?.state==='already_done'}catch{return false}})());
// Waiting on others: its run found a step still open on someone else's side (outcome waiting: a review, merge, deploy, a
// reply). Nothing is ready for you there, so it sits in its own folded group above Coming back later and never counts.
// A new message on it (assistant.py update_card) makes it an open to-do again. Same rule as waits_on_others().
const waitsOnOthers=s=>!closed(s)&&s.status==='prepared'&&!looksDone(s)&&(()=>{try{return JSON.parse(s.outcome||'{}')?.state==='waiting'}catch{return false}})();
// Its one line of evidence: the hint's reason, else the result's first sentence (what shows it)
function doneWhy(s){try{const h=JSON.parse(s.handled_hint||'null');if(h?.reason)return h.reason}catch{}
 const plain=String(s.body||'').replace(/\[([^\]]*)\]\([^)]*\)/g,'$1').replace(/[*_`]/g,'').replace(/\s+/g,' ').trim();
 return (plain.match(/^.*?[.!?](?=\s|$)/)?.[0]||plain).replace(/\.$/,'').slice(0,200)}
const ICONS={x:'<path d="M4 4l16 16M20 4L4 20"/>',plugin:'<circle cx="12" cy="12" r="8"/><path d="M12 8v8M8 12h8"/>',gateway:'<rect x="4" y="4" width="16" height="6" rx="1.5"/><rect x="4" y="14" width="16" height="6" rx="1.5"/><path d="M8 7h.01M8 17h.01"/>',gmail:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/>',calendar:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',slack:'<path d="M10 3 8 21M16 3l-2 18M4 9h16M3.5 15h16"/>',salesflare:'<path d="M4 20V8l8-4 8 4v12"/><path d="M9 20v-5h6v5M9 11h.01M15 11h.01"/>',android:'<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18h2"/>',whatsapp:'<path d="M20 12a8 8 0 0 1-11.6 7.1L4 20l1.2-4.2A8 8 0 1 1 20 12z"/>',telegram:'<path d="M21 4L3 11l6 2.5L11 20l3.5-4.5L19 19z"/><path d="M9 13.5L21 4"/>',linkedin:'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 10v7M8 7h.01M12 17v-7M12 13a3 3 0 0 1 6 0v4"/>',github:'<circle cx="6" cy="6" r="2.2"/><circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="8" r="2.2"/><path d="M6 8.2v7.6M18 10.2c0 4-6 3-10.5 6.3"/>',stripe:'<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="M3 10h18M7 15h4"/>'};
ICONS.docs='<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h4"/>';ICONS.outlook=ICONS.gmail;ICONS.outlook_calendar=ICONS.calendar;ICONS.zoom='<rect x="3" y="6.5" width="12.5" height="11" rx="2"/><path d="m15.5 10.5 5-3v9l-5-3"/>';ICONS.google_meet=ICONS.zoom;
const icon=s=>html`<span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24">${raw(ICONS[s]||ICONS.plugin)}</svg></span>`;
const kindService=k=>({'calendar.event':'calendar','meeting.notes':'calendar','slack.message':'slack','android.notification':'android','whatsapp.message':'whatsapp','telegram.message':'telegram','salesflare.email':'salesflare','salesflare.meeting':'salesflare','gateway.alert':'gateway'}[k]||(/^[a-z][a-z0-9_]*\./.test(k)&&k!=='gmail.message'?k.split('.')[0]:'gmail'));
const changing=new Set(),dismissing=new Set();
const taskActions=s=>{const choices=s?.next_actions||(s?.next_action?.kind==='menu'?s.next_action.actions:s?.next_action?[s.next_action]:[]);const ready=choices.some(a=>['email','email_demo','linkedin','slack','x','whatsapp','telegram','intercom','doc_reply','merge','finish','handoff','calendar','doc_write'].includes(a.kind));return choices.filter(a=>a.kind!=='prepare'||(!ready&&!/^Draft (shorter|longer|another|alternative|follow-up)\b/i.test(a.label||'')))};
// Handed to someone: the card waits for their reply and closes when they answer.
// What we don't know (gap_note.py): one quiet line when the last word with the person is old or unanswered, from synced
// signals only, and the channels they may have answered on that aren't synced here. A fresh conversation gets none.
const gapOr=list=>{try{return new Intl.ListFormat(I18N.lang||'en',{type:'disjunction'}).format(list)}catch{return list.join(', ')}};
const gapLine=(s,hint)=>{const g=s.gap;let w={};try{w=JSON.parse(s.awaiting||'{}')||{}}catch{}
 if(!g||closed(s)||s.status==='snoozed'||hint||w.delegated||s.follow_up||withTeammate(s))return '';
 const via=g.channel==='email'?t('email'):g.channel,more=g.unsynced?.length?' '+t('They may have replied on {} (not synced).',gapOr(g.unsynced)):'';
 return `<p class="note gap-line">${esc((g.wrote_last?t('Your last message: {} days ago by {}; no reply since.',g.days,via):t('Last contact {} days ago by {}; nothing since.',g.days,via))+more)}</p>`};
const handedNote=s=>{let w={};try{w=JSON.parse(s.awaiting||'{}')}catch{}if(!w.delegated)return '';const text=s.status==='snoozed'?t('Sent to {}. Waiting for their reply; it closes when they answer.',w.name):s.status==='completed'&&w.answered?t('{} replied, so I closed this.',w.name):s.status==='prepared'?t('No reply from {} yet.',w.name):'';return text?html`<p class="note">${text}</p>`:''};
// Under way or done, so no Send. An unconfirmed send checked long enough (retry_ok) may be sent again by the owner.
const sendBusy=a=>['queued','sending','sent','uncertain','local_preparation','paused','undoing','undone'].includes(a?.status)&&!a?.retry_ok;
const sentAt=a=>a?.sent_at?' at '+fmtHM(a.sent_at,{timeZone:state?.hours?.timezone||undefined}):'';
// a sent note in the owner's language: the plain sentence, or the one with the time it went out
const sentNote=(a,plain,timed,...x)=>a?.sent_at?t(timed,...x,fmtHM(a.sent_at,{timeZone:state?.hours?.timezone||undefined})):t(plain,...x);
const actionNote=(a,kind,action)=>kind==='doc_write'?({queued:'Writing the doc…',sending:'Writing the doc…',sent:docDoneText(action||{},a),blocked:a?.error,uncertain:a?.error,failed:a?.error})[a?.status]||'':kind==='calendar'?({queued:'Changing the calendar…',sending:'Changing the calendar…',sent:action?calDoneText(action,a):'Done.',blocked:a?.error,uncertain:a?.error,failed:a?.error})[a?.status]||'':kind==='merge'?({queued:a?.auto?'Testing the fix. It merges by itself if every check passes.':'Testing and merging the fix…',sending:'Testing and merging the fix…',sent:(a?.auto?'Merged by itself and restarted. You can undo it for 24 hours; it undoes itself if the error comes back.':'Merged. The Machine restarts with the fix.')+(a?.error?' '+a.error:''),blocked:(a?.error||'')+(a?.auto?' Tap Merge fix to merge it anyway.':''),uncertain:a?.error,failed:a?.error,undoing:'Undoing the merge…',undone:a?.error||'Merge undone.'})[a?.status]||'':({queued:'Sending your approved draft…',sending:'Sending your approved draft…',sent:/^(urn:li:|linkedin:)/.test(a?.message_id||'')?sentNote(a,'LinkedIn message sent.','LinkedIn message sent at {}.'):/^slack:/.test(a?.message_id||'')?sentNote(a,'Slack message sent.','Slack message sent at {}.'):/^x:/.test(a?.message_id||'')?sentNote(a,'Reply posted on X.','Reply posted on X at {}.'):/^xdm:/.test(a?.message_id||'')?sentNote(a,'X message sent.','X message sent at {}.'):/^whatsapp:/.test(a?.message_id||'')?sentNote(a,'WhatsApp message sent.','WhatsApp message sent at {}.'):/^intercom:/.test(a?.message_id||'')?sentNote(a,'Sent as {} in Intercom.','Sent as {} in Intercom at {}.',a?.as_name||t('your Intercom admin')):/^doc:/.test(a?.message_id||'')?sentNote(a,'Reply posted in the doc.','Reply posted in the doc at {}.'):sentNote(a,'Email sent.','Email sent at {}.')+(['queued','snoozed'].includes(a?.snooze_status)&&a?.snooze_until?' '+t('Thread out of your inbox until {}.',fmtDHM(a.snooze_until,{weekday:'short',day:'numeric',month:'short'},{timeZone:state?.hours?.timezone||undefined})):a?.snooze_status==='failed'?' '+(a.snooze_error||'I couldn’t snooze the thread in Gmail.'):''),blocked:a?.error,uncertain:a?.error,failed:a?.error})[a?.status]||'';
const safeURL=u=>{try{return ['https:','http:'].includes(new URL(u).protocol)?u:''}catch{return ''}};
const resultLink=/\[[^\]]*\]\((?:\/[^\s<>"\)]*\/workspace\/)?memory\/assistant\/[^\s\)]+\)|(?:\/[^\s<>"\)]*\/workspace\/)?memory\/assistant\/[^\s<>"\)]+/g;
// Result links become the Read result button; drop the lines they leave empty and the gaps after them (same rule as Telegram).
// A sentence the link ended ("The draft is at <path>.") points at nothing without it, so it goes too (strip_result_links).
const danglingPointer=/(^|[.!?]\s+)[^.!?]*\b(?:at|in|to|under|into|on|see|here)\s*[.:]?\s*$/i;
// A named link to a result ("Your [plan](memory/assistant/x.md) is ready") keeps its words: link(words,path) says how
// they show (the card: a link that opens that file), plain words otherwise. A bare path has no words, so it goes.
const resultNamed=/\[([^\]\n]*\S[^\]\n]*)\]\((?:\/[^\s<>"\)]*\/workspace\/)?(memory\/assistant\/[^\s\)]+)\)/g;
const resultBody=(s,link)=>s.body.split('\n').flatMap(line=>{const named=line.replace(resultNamed,(m,words,path)=>link?link(words.trim(),path.replace(/[.,;\]]+$/,'')):words.trim());
 let kept=named.replace(resultLink,'').replace(/  /g,' ').trimEnd();if(kept!==named.trimEnd())kept=kept.replace(danglingPointer,'$1').replace(/([.!?])\s+[.!?](?=\s|$)/g,'$1').trimEnd();return kept!==named.trimEnd()&&(/^[\s·•|,;:()\-–—]*$/.test(kept)||/^\s*[-*•]?\s*[^\s:]+(?: [^\s:]+){0,3}:$/.test(kept))?[]:[kept]}).join('\n').replace(/\n{3,}/g,'\n\n').trim();
// On the card a named result link opens that file like Read result does; one the task doesn't serve stays plain words.
const resultLinks=s=>{const found=[];return {text:resultBody(s,(words,path)=>{found.push({words,path});return ''+(found.length-1)+''}),
 html:h=>h.replace(/(\d+)/g,(m,i)=>{const f=found[i];return (s.result_files||[]).some(r=>r.path===f.path)?`<button type="button" class="link result-link" data-id="${esc(s.id)}" data-result="read" data-file="${esc(f.path)}" data-file-name="${esc(f.words)}">${esc(f.words)}</button>`:esc(f.words)}),
 plain:t=>t.replace(/(\d+)/g,(m,i)=>found[i].words)}};
const needsDecision=s=>s.status==='pending'||(!closed(s)&&s.status!=='snoozed'&&s.preparation_status==='blocked');
// Where an open to-do sits: Ready, Needs your decision or Preparing. One that starts preparing (Do it, Ask for changes)
// stays where it was until the run is done, so it doesn't jump to another section and back while it works.
const placeHeld=new Map();
const placeOf=s=>{const now=needsDecision(s)?'needs':s.status==='prepared'?'ready':'preparing',was=placeHeld.get(s.id);
 if(now==='preparing'&&was&&was!=='preparing')return was;placeHeld.set(s.id,now);return now};
// A to-do held for later (deliver_after): when it reaches the owner, and where, as deliver_one sends it
// (state.todo_channels, from Settings, Notifications: New to-dos). Nowhere but here: no chip.
function deliveryLabel(value,ch=state?.todo_channels){
const tg=!!ch?.telegram,push=(ch?.push||0)>0;if(!tg&&!push)return '';
const target=new Date(value),today=localDay(new Date()),tomorrow=new Date();tomorrow.setDate(tomorrow.getDate()+1);
const day=localDay(target)===today?t('Today'):localDay(target)===localDay(tomorrow)?t('Tomorrow'):target.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'});
const when=day+' · '+fmtHM(target);
return tg&&push?t('Telegram and notification {}',when):tg?t('Telegram {}',when):t('Notification {}',when);
}
const DRAFT_KINDS=['email','email_demo','linkedin','slack','x','whatsapp','telegram','intercom','doc_reply','handoff','finish','calendar','doc_write'];
// A calendar change on a card (kind calendar): what it adds, changes or deletes, on which calendar. Nobody is invited.
const CAL_DO={create:'Add to {}',update:'Change on {}',delete:'Delete from {}'},CAL_DID={create:'Added to {}',update:'Changed on {}',delete:'Deleted from {}'};
const CAL_DID_DOT={create:'Added to {}.',update:'Changed on {}.',delete:'Deleted from {}.'},CAL_DID_AT={create:'Added to {} at {}.',update:'Changed on {} at {}.',delete:'Deleted from {} at {}.'},CAL_DID_INV={create:'Added to {}, invited {}.',update:'Changed on {}, invited {}.',delete:'Deleted from {}, invited {}.'};
const CAL_LABEL={create:'Add to calendar',update:'Save event',delete:'Delete event'};
const calDoneText=(a,sent)=>CAL_DID[a.op]?sentNote(sent,CAL_DID_DOT[a.op],CAL_DID_AT[a.op],a.calendar_name):a.calendar_name;
// What a calendar change does, as label and value rows: on the card and in its review.
const calRows=a=>[['What',a.title],['When',a.when],...(a.op==='update'&&a.was&&(a.was.title!==a.title||a.was.when!==a.when)?[['Was',a.was.title+', '+a.was.when]]:[]),...(a.location?[['Where',a.location]]:[]),...(a.notes?[['Notes',a.notes]]:[])];
const calChangeText=a=>[a.title,a.when,a.op==='update'&&a.was&&(a.was.title!==a.title||a.was.when!==a.when)?t('Was: {}',a.was.title+', '+a.was.when):'',a.location?t('Where: {}',a.location):'',a.notes?t('Notes: {}',a.notes):''].filter(Boolean).join('\n');
// The text a draft sends, or a final step posts (its message; else what goes out). Edit changes exactly this.
const draftText=a=>a.kind==='finish'?(a.message||a.preview):a.kind==='calendar'?calChangeText(a):a.kind==='doc_write'?docWriteText(a):a.body;
// Email and Slack turn [words](https://...) into a real link when sent, so the draft shows it as one; a handoff
// reaches the teammate as plain text, words (URL), so the draft shows that.
const MD_LINK=/\[([^\[\]\n]{1,200})\]\((https:\/\/[^\s()<>]{1,2000})\)/g;
// An email's text marks, drawn exactly as the send writes them (next_actions.mail_html; tests/mail_format_cases.json
// keeps the two in step): **bold**, _italic_ or *italic*, [words](https://link), "- " and "1. " lines as lists, \* for
// a mark meant as itself. Everything else is text. The preview, the editor and the sent mail are one and the same.
const MAIL_ESCAPE=/\\([\\*_\[\]()\-.#])/g,MAIL_LINK=/\[([^\[\]\n]{1,200})\]\((https:\/\/[^\s()<>]{1,2000})\)|(https:\/\/[^\s<>]*[^\s<>.,;:!?)\]])/g,MAIL_KEPT=/[\uE000-\uF8FF]/g;
const MAIL_BOLD=/\*\*([^\s*](?:(?:[^*]|\*(?!\*))*[^\s])?)\*\*(?!\*)/g,mailSpan=c=>`(?:[^\\s${c}<]|<b>[^<]*</b>)(?:(?:[^${c}<]|<b>[^<]*</b>)*(?:[^\\s${c}<]|<b>[^<]*</b>))?`;
const MAIL_ITALIC=[new RegExp(`(^|[^\\p{L}\\p{N}_*])\\*(${mailSpan('*')})\\*(?![\\p{L}\\p{N}_*])`,'gu'),new RegExp(`(^|[^\\p{L}\\p{N}_])_(${mailSpan('_')})_(?![\\p{L}\\p{N}_])`,'gu')];
const mailEsc=(v,q=true)=>String(v).replace(q?/[&<>"']/g:/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#x27;'}[c]));
// Escapes, links and & < > wait as kept characters (one each, as their entities did for the marks), the marks become
// <b> and <i> in the text, and then it is built with html``: the marks and links as markup, everything else as text.
const MAIL_TAG={'<b>':html`<b>`,'</b>':html`</b>`,'<i>':html`<i>`,'</i>':html`</i>`};
function mailInline(text,nested=false,attrs=''){const kept=[],keep=v=>String.fromCharCode(0xE000+kept.push(v)-1),back=x=>x.replace(MAIL_KEPT,c=>kept[c.charCodeAt(0)-0xE000]);
 let s=String(text??'').replace(MAIL_KEPT,'').replace(MAIL_ESCAPE,(m,c)=>keep(c));
 if(!nested)s=s.replace(MAIL_LINK,(m,w,u,bare)=>keep(w?html`<a href="${safeHref(back(u))}"${attrs}>${mailInline(w,true)}</a>`:html`<a href="${safeHref(back(bare))}"${attrs}>${back(bare)}</a>`));
 s=s.replace(/[&<>]/g,keep).replace(MAIL_BOLD,'<b>$1</b>');for(const r of MAIL_ITALIC)s=s.replace(r,'$1<i>$2</i>');
 return html`${s.split(/(<\/?[bi]>|[\uE000-\uF8FF])/).map((x,i)=>i%2?MAIL_TAG[x]||kept[x.charCodeAt(0)-0xE000]:x)}`}
// Line ends as next_actions.paragraphs reads them: \r\n is one break, a line of only spaces an empty line (a blank line between paragraphs).
function mailBlocks(body){const out=[];for(const line of String(body??'').split(/\r\n?|\n/).map(l=>l.trim()?l:'')){const b=/^- ([\s\S]*)$/.exec(line),n=/^([0-9]{1,3})\. ([\s\S]*)$/.exec(line),last=out[out.length-1];
  if(b){if(last?.type==='ul')last.items.push(b[1]);else out.push({type:'ul',items:[b[1]]})}
  else if(n){if(last?.type==='ol')last.items.push(n[2]);else out.push({type:'ol',start:+n[1],items:[n[2]]})}
  else if(last?.type==='text')last.items.push(line);else out.push({type:'text',items:[line]})}return out}
// The HTML part as sent; links=true opens them in a new tab here (the mail itself has plain links)
const mailHtml=(body,here=true)=>{const at=here?html` target="_blank" rel="noreferrer"`:'';return html`${mailBlocks(body).map(b=>b.type==='text'?b.items.map(l=>{const v=mailInline(l,false,at);return html`<div>${String(v)?v:html`<br>`}</div>`})
 :html`${b.type==='ol'?html`<ol${b.start!==1?html` start="${b.start}"`:''} style="margin:0 0 0 1.6em;padding:0">`:html`<ul style="margin:0 0 0 1.6em;padding:0">`}${b.items.map(i=>html`<li>${mailInline(i,false,at)}</li>`)}${b.type==='ol'?html`</ol>`:html`</ul>`}`)}`};
// Slack's links are found in the escaped text, as before; each piece goes back to text for html`` to escape once.
const unesc=s=>s.replace(/&(amp|lt|gt|quot|#39);/g,(m,k)=>({amp:'&',lt:'<',gt:'>',quot:'"','#39':"'"}[k]));
const slackBody=text=>{const p=esc(text).split(MD_LINK),out=[];for(let i=0;i<p.length;i+=3){out.push(unesc(p[i]));if(i+2<p.length)out.push(html`<a href="${safeHref(unesc(p[i+2]))}" target="_blank" rel="noreferrer">${unesc(p[i+1])}</a>`)}return html`${out}`};
const draftBody=(a,text)=>['email','email_demo'].includes(a.kind)?mailHtml(text):a.kind==='slack'?slackBody(text):html`${String(text).replace(MD_LINK,'$1 ($2)')}`;
// An email that goes instead of a reply in the to-do's Intercom conversation: why (next_actions.INTERCOM_FALLBACK, the same words).
const INTERCOM_WHY={shared:'Intercom is shared with you to read only, so this goes by email.',off:'Intercom replies are off here, so this goes by email. Sign in with Intercom to reply there.',missing:'Intercom isn’t connected on this Machine, so this goes by email.'};
// A reply from another mailbox than the one the email came in on (next_actions.REPLY_ELSEWHERE, the same words).
const replyElsewhere=a=>a.kind==='email'&&a.reply_elsewhere?t('Goes from {}, not {} where the email came in. It still lands in their thread.',a.from,a.reply_elsewhere):'';
// The draft as written: To · Subject in small type, the text with its line breaks; long drafts fold behind Show more.
function draftBox(s,a,label){if(a.kind==='doc_write')return docWriteBox(s,a);if(a.kind==='calendar'){const done=(a.state||s.action_status)?.status==='sent';
 return `<div class="draft cal-change${done?' sent':''}" role="group" aria-label="Calendar change"><div class="dm">${esc((done?CAL_DID:CAL_DO)[a.op]?t((done?CAL_DID:CAL_DO)[a.op],a.calendar_name):a.calendar_name)}</div><dl class="cal-rows">${calRows(a).map(([k,v])=>`<div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl></div>`}
const fin=a.kind==='finish',sent=(a.state||s.action_status)?.status===(fin?'done':'sent'),mail=['email','email_demo'].includes(a.kind),text=draftText(a);
const to=a.kind==='x'&&!a.to_name&&a.to_screen_name?'@'+a.to_screen_name:a.to_name||(a.to||[]).join(', ');
// A final step (Submit, Pay…): its label, and who gets the message when it posts one.
const head=fin?(sent?'Done: ':'')+a.label+(to?' · '+t('To: {}',to):''):(label?label+' · ':'')+(sent?'Sent to':'To')+': '+(to||'…')+(mail&&a.subject?' · '+a.subject:'');
const key='draft-'+s.id+'-'+a.revision,rows=String(text).split('\n').reduce((n,l)=>n+(l.trim()?Math.ceil(l.length/56):1),0),fold=rows>16,open=expandedBodies.has(key);
return `<div class="draft${sent?' sent':''}${fold&&!open?' clamp':''}"${sent||fin?'':` data-rev="${esc(a.revision||'')}"`} role="group" aria-label="${fin?(a.message?'Message to post':'What goes out'):(sent?'Sent':'Draft')+' '+(mail?'email':'message')}"><div class="dm">${esc(head)}</div>${mail&&!sent&&INTERCOM_WHY[a.intercom_fallback]?`<p class="draft-why">${esc(INTERCOM_WHY[a.intercom_fallback])}${a.intercom_fallback==='off'?'':' <a href="#health" class="draft-connect" data-connect-open="intercom">Connect your own Intercom</a>'}</p>`:''}${!sent&&replyElsewhere(a)?`<p class="draft-why">${esc(replyElsewhere(a))}</p>`:''}<div class="db${mail?' mail':''}">${draftBody(a,text)}</div>${(a.attachments||[]).length?`<div class="attachments">${draftFileLinks(s.id,a.attachments)}</div>`:''}</div>${fold?`<button type="button" class="more" data-more="${esc(key)}" aria-expanded="${open}">${open?'Show less':'Show more'}</button>`:''}`}
// The order of the choices in a to-do's … menu (cardActions): a decision's Snooze first, a ready one's Ask for changes.
const SECONDARY={pending:['snooze','reject','complete','accept','change','handoff'],snoozed:['accept','snooze','reject'],prepared:['change','complete','snooze','reject','handoff']};
// Already handled (a later message, or the teammate's own Machine): nothing to hand on.
// Who an open to-do is about (the one waited on first): a chip that opens their page in the Graph.
// The to-do's pills (status, Work or Personal, who, their organization, the project) are one size; who, organization
// and project each start with the Graph's own icon for it, drawn the same way
const CHIP_ICON={person:'<svg class="ci" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8.5" r="3.2"/><path d="M5.5 19.5c.8-3.4 3.4-5.2 6.5-5.2s5.7 1.8 6.5 5.2"/></svg>',
 org:'<svg class="ci" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 20V5.5h8V20M14 9.5h4V20M4 20h16M9 9h2M9 12.5h2M9 16h2"/></svg>',
 project:'<svg class="ci" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7.5V18a1.5 1.5 0 0 0 1.5 1.5h13A1.5 1.5 0 0 0 20 18V9.5A1.5 1.5 0 0 0 18.5 8H12l-2-2.5H5.5A1.5 1.5 0 0 0 4 7z"/></svg>'};
const whoChip=s=>{const p=(s.people||[])[0];if(!p?.id||!p.name)return '';let w={};try{w=JSON.parse(s.awaiting||'{}')||{}}catch{}
 const waited=s.handoff_wait?.name||w.name,first=waited&&(s.people||[]).find(x=>x.name===waited)||p;
 const short=String(first.name).split(' ')[0];return html`<a class="chip scope who" href="${graphHash(first.id)}" title="Open ${first.name}" aria-label="Open ${first.name}">${raw(CHIP_ICON.person)}<span class="who-full">${first.name}</span>${short!==first.name?html`<span class="who-short">${short}</span>`:''}</a>${first.org?.id&&first.org.name&&first.org.name!==first.name?html`<a class="chip scope who org" href="${graphHash(first.org.id)}" title="Open ${first.org.name}" aria-label="Open ${first.org.name}">${raw(CHIP_ICON.org)}<span>${first.org.name}</span></a>`:''}`};
// A to-do a teammate has now: Take it back makes it yours again; Hand off to someone else gives it to another one
// (and takes it back from them, see handoffEditor). Both sit in sight, beside the to-do's own buttons.
const canReassign=s=>!closed(s)&&!s.handled_hint&&!!state?.fleet?.on&&['asked','waiting for them'].includes(s.fleet_handoff?.stage)&&!handingOff.has(s.id)&&!redirect(s);
const canHandoff=s=>!closed(s)&&!s.handled_hint&&!!state?.fleet?.on&&s.scope==='work'&&(!s.fleet_handoff||['declined','expired'].includes(s.fleet_handoff.stage))&&!handingOff.has(s.id);
// The way into a card's chat: optional, a small quiet link on the card's top row ("Chat ›"); a dot on its icon when there is
// a conversation behind it already (a run, a note of yours, a coding agent's answer). Typing in Change still changes the card in place.
const CHAT_ICON='<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M5 5.5h14a1.5 1.5 0 0 1 1.5 1.5v8.5a1.5 1.5 0 0 1-1.5 1.5h-7.5L7 20.5V17H5a1.5 1.5 0 0 1-1.5-1.5V7A1.5 1.5 0 0 1 5 5.5z"/></svg>';
const chatHad=s=>!!(s.agent_job||s.latest_feedback||s.change_prompt||s.preparation_status&&s.preparation_status!=='queued');
const chatLink=s=>html`<a class="card-chat-link${chatHad(s)?' had':''}" href="#chat=${s.id}" title="${chatHad(s)?'Open the conversation':'Open as a chat'}">${raw(CHAT_ICON)}<span>Chat</span><span aria-hidden="true">›</span></a>`;
// A ready draft the Machine can't send itself (no send path, such as an internal note): Copy draft leads, with why.
// A skill the to-do's run proposed (proposed_skill): what is in it on the card, and Create skill (or Update skill, its before
// and after first) leads. It goes through the owner's own Approve (skill_decide); nothing is installed before that tap.
const skillDecided=s=>!!(s.proposed_skill?.dismissed||s.proposed_skill?.created);
const skillLead=s=>s.status==='prepared'&&!!s.proposed_skill&&!skillDecided(s);
// Created or dismissed (here or in Settings, Skills): the to-do says so and Mark done leads; closing it stays the owner's call.
// The run's saved "Needs you: approve …" no longer holds then, so the status line leaves it out (the stored text stays).
const proposedSkillBox=s=>{const p=s.proposed_skill;if(!p||closed(s))return '';if(p.dismissed)return `<p class="note skill-dismissed">${esc(t('Skill dismissed'))}</p>`;if(p.created)return `<p class="note skill-created">${esc(t('Skill created. Your Machine uses it from now on.'))}</p>`;
 if(p.update)return `<details class="skill-notes"><summary>${esc(t('Read the change'))}</summary><div class="skill-ba">${skillBeforeAfter(p.update)}</div></details>`;
 return `<details class="skill-notes"><summary>${esc(t('Read the skill'))}</summary><p><strong translate="no">${esc(p.name)}</strong></p><p class="note" translate="no">${esc(t('When: {}',p.description))}</p><div translate="no">${p.body.replace(/^#{1,6}\s+(.+)$/gm,'**$1**').split(/\n\s*\n/).map(x=>x.trim()).filter(Boolean).map(x=>`<p>${format(x,true)}</p>`).join('')}</div></details>`};
const skillButton=s=>{const p=s.proposed_skill;return 'update' in p?html`<button class="primary" data-skill-update="${p.id}" data-settings>${t('Update skill')}</button>`
 :html`<button class="primary" data-skill-create="${p.id}" data-card="${s.id}">${t('Create skill')}</button>`};
document.addEventListener('click',async e=>{const b=e.target.closest('[data-skill-create]');if(!b)return;e.preventDefault();b.disabled=true;
 try{await skillAct('skill_decide',{id:b.dataset.skillCreate,choice:'approve'});toast(t('Skill created. Your Machine uses it from now on.'));await refresh()}
 catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
const copyLead=(s,smart)=>!s.proposed_skill&&s.status==='prepared'&&!smart.some(a=>a.kind!=='open')&&/\bdraft/i.test(s.body||'')&&(s.result_files||[]).some(f=>!/\.pdf$/i.test(f.name));
const COPY_WHY='This can’t be sent from here. Copy it to send it yourself.';
// The button row: the action that fits this to-do (its prepared send, Do it, Answer, Mark done, Check in now), Ask for
// changes when there is a draft or result to review, Snooze, and Mark done on a ready one without a draft (with one,
// it tops the …); then a quiet … with Hand off… (a teammate, a connected coding agent and Ask to review on one small sheet), Repeat… and Not
// needed last. Telling The Machine to do it another way is the Chat's job. The title, project and area change in place
// (a tap on the title; the project and area under Details). On a phone the … opens as a bottom sheet. A choice not in
// sight (Mark done on a decision) stays on the card, hidden, so the keyboard shortcuts and the chat's menu still find it.
const mmPlain=h=>h.replace(/^<(\w+)([^>]*?) class="([^"]*)"/,(m,tag,pre,c)=>`<${tag}${pre} class="${[...c.split(' ').filter(x=>x&&x!=='primary'),...(tag==='button'&&!/\bghost\b/.test(c)?['ghost']:[])].join(' ')}"`);
function cardActions(s,choices,smartButtons,unmerge,hint,smart){const skill=skillLead(s),copy=copyLead(s,smart)||skill,asked=moveAsk(s);
 if(asked)smartButtons=`<button class="primary" data-card-move="${esc(s.id)}" data-area="${esc(s.preparation_move_to)}">${esc(moveText(s.preparation_move_to))}</button>`+smartButtons;
 if(skill)smartButtons=skillButton(s)+smartButtons;
 else if(copy)smartButtons=`<button class="primary" data-id="${s.id}" data-result="copy">Copy draft</button>`+smartButtons;
 const answered=s.status==='prepared'&&(()=>{try{return JSON.parse(s.outcome||'{}').state==='answered'}catch{return false}})();
 const ask=askQuestion(s,smart,hint);
 const mine=ownerStep(s)&&!ask;
 const isPrimary=c=>c==='send'||(c==='checkin'&&withTeammate(s))||(c==='retry'&&!ask&&!asked)||c==='answer'||(c==='complete'&&mine)||(c==='complete'&&!copy&&!withTeammate(s)&&(hint||(s.status==='prepared'&&!answered&&!ask&&!finalStep(s)&&!smart.some(a=>a.kind!=='open'))))||(c==='accept'&&(s.status==='pending'||answered)&&!hint&&!mine);
 const btn=([c,t])=>c==='accept'&&s.status==='pending'&&s.skill_proposal?.update?`<button class="${isPrimary(c)?'primary':'ghost'}" data-skill-update="${esc(s.id)}">${esc(t)}</button>`:c==='change'&&agentAsk(s)?`<button class="ghost" data-agent-ask="${esc(s.id)}">Ask for changes</button>`:c==='handoff'?`<button class="ghost" data-fleet-handoff="${esc(s.id)}">${esc(t)}</button>`:c==='takeback'?`<button class="ghost" data-handoff-take-back="${esc(s.id)}">${esc(t)}</button>`:c==='checkin'?`<button class="primary" data-handoff-checkin="${esc(s.id)}" title="Open the chat to check in">${esc(t)}</button>`:c.startsWith('agent:')?`<button class="ghost" data-agent-hand="${esc(c.slice(6))}" data-card="${esc(s.id)}">${esc(t)}</button>`:`<button class="${isPrimary(c)?'primary':c==='reject'?'quiet':'ghost'}" data-id="${esc(s.id)}" data-choice="${esc(c)}"${c==='change'?` title="${s.status==='pending'?'Tell me how to do it instead':s.status==='prepared'&&smart.some(a=>DRAFT_KINDS.includes(a.kind))?'Tell me what to change in the draft, and I redo it':'Tell me what to change, and I redo it'}"`:''}>${esc(t)}</button>`;
 const all=[...choices,...(canHandoff(s)&&s.status!=='snoozed'&&!smart.some(a=>a.kind==='handoff')?[['handoff',s.fleet_handoff?.back?'Hand off to someone else':'Hand off']]:canReassign(s)?[['takeback','Take it back'],['handoff','Hand off to someone else']]:[]),...(canAgent(s)?agentTools().map(t=>['agent:'+t.id,window.t('Hand to {}',t.name)]):[]),...(agentAsk(s)&&!choices.some(([c])=>c==='change')?[['change','']]:[])];
 const head=all.filter(([c])=>isPrimary(c)),order=(mine&&s.status==='pending'?['accept','snooze','reject','change','handoff']:ask?['handoff','complete','retry','snooze','reject']:answered?['snooze','change','complete','reject','handoff']:SECONDARY[s.status])||['complete','snooze','change','reject','handoff'];
 const rank=c=>c.startsWith('agent:')?99:c==='change'&&agentAsk(s)?-1:order.indexOf(c),rest=all.filter(([c])=>!isPrimary(c)).sort((a,b)=>rank(a[0])-rank(b[0]));
 const handing=([c])=>c==='handoff'||c.startsWith('agent:');
 // The lead: the prepared action, else the to-do's primary choice, else its first plain one in order (Check in now while a teammate has it, Unsnooze on a snoozed one)
 const tpl=document.createElement('template');tpl.innerHTML=smartButtons;const leads=[...[...tpl.content.children].map(n=>n.outerHTML),...head.map(btn)];
 const first=leads.findIndex(h=>/^<\w+[^>]* class="[^"]*\bprimary\b/.test(h));if(first>0)leads.unshift(...leads.splice(first,1));  // a primary leads over a plain link (Open in Maps)
 let others=rest;if(!leads.length){const plain=x=>!handing(x)&&x[0]!=='reject',i=[rest.findIndex(x=>plain(x)&&order.includes(x[0])),rest.findIndex(plain)].find(j=>j>=0)??-1;if(i>=0){leads.push(btn(rest[i]));others=rest.filter((_,j)=>j!==i)}}
 // Hand off…: who or what can take it, on one small sheet; a single one is a plain item with its whole name
 const agentName=c=>agentTools().find(t=>'agent:'+t.id===c)?.name;
 const hand=[...others.filter(x=>x[0]==='takeback').map(btn),...others.filter(handing).map(x=>btn([x[0],x[0]==='handoff'?t('A teammate'):agentName(x[0])||x[1]]).replace('<button ',`<button data-full="${esc(x[0]==='handoff'?t(x[1]):x[1])}" `)),...(reviewMore(s)?[reviewMore(s)]:[])];
 const handFull=h=>String(h).replace(/ data-full="([^"]*)"([^>]*)>[^<]*</,(m,full,rest)=>`${rest}>${full}<`);
 const sheet=hand.length>1?`<button type="button" class="ghost" data-mm-open="handoff" aria-haspopup="true">${esc(t('Hand off…'))}</button>`:hand.map(handFull).join('');
 const sub=hand.length>1?`<div class="mm-sub" role="group" aria-label="${esc(t('Hand off'))}" hidden><p class="mm-head"><button type="button" class="mm-back" data-mm-back aria-label="${esc(t('Back'))}">‹</button><span>${esc(t('Hand off'))}</span></p>${hand.join('')}</div>`:'';
 const repeat=closed(s)||s.repeats?'':`<button type="button" class="ghost" data-repeat="${esc(s.id)}">${esc(t('Repeat…'))}</button>`;
 // In sight: Ask for changes on a draft or result, Snooze, and Mark done on a ready one without a draft
 const draft=smart.some(a=>DRAFT_KINDS.includes(a.kind)),ready=s.status==='prepared'&&!answered&&!ask&&!mine&&!withTeammate(s);
 const doneShown=ready&&!draft,doneTop=ready&&draft;  // with a draft, Mark done tops the … so the row stays one line
 const review=s.status==='prepared'||!!agentAsk(s);
 const shown=x=>x[0]==='snooze'||(x[0]==='change'&&review)||(x[0]==='complete'&&doneShown);
 const quiet=x=>(x[0]==='complete'&&!doneTop)||x[0]==='change';  // on the card, out of sight: the D key, the palette and the chat use them
 const plain=others.filter(x=>!handing(x)&&x[0]!=='reject'&&x[0]!=='takeback');
 const row=plain.filter(shown).map(btn).join(''),hiddenBtns=plain.filter(x=>!shown(x)&&quiet(x)).map(b=>btn(b).replace('<button ','<button hidden ')).join('');
 const items=[...plain.filter(x=>doneTop&&x[0]==='complete').map(btn),...leads.slice(1).map(mmPlain),...plain.filter(x=>!shown(x)&&!quiet(x)&&!(doneTop&&x[0]==='complete')).map(btn),sheet,repeat,unmerge,...others.filter(x=>x[0]==='reject').map(b=>'<hr class="mm-sep">'+btn(b))].filter(Boolean).join('');
 const menu=items?`<details class="more-actions"><summary aria-label="${esc(t('More actions'))}" title="${esc(t('More actions'))}">${DOTS}</summary><div class="more-menu" role="group" aria-label="${esc(t('More actions'))}">${items}${sub}</div></details>`:'';
 const two=(leads[0]?1:0)+plain.filter(shown).length>2;  // on a phone: the lead on its own row, the rest on one
 return `<div class="actions${two?' two-rows':''}">${leads[0]||''}${row}${menu}${hiddenBtns}</div>${copy&&!skill?`<p class="copy-why">${COPY_WHY}</p>`:''}`}
// The … menu's Hand off… opens its sheet in place (Back returns); a click outside, Escape or a choice closes the menu.
document.addEventListener('click',e=>{const o=e.target.closest('.more-menu [data-mm-open],.more-menu [data-mm-back]');if(!o)return;e.preventDefault();const m=o.closest('.more-menu'),sub=m.querySelector('.mm-sub'),go=o.dataset.mmOpen!=null;
 m.classList.toggle('mm-in',go);if(sub)sub.hidden=!go;(go?sub?.querySelector('button:not([data-mm-back])'):m.querySelector('[data-mm-open]'))?.focus()});
document.addEventListener('toggle',e=>{const d=e.target;if(!d.matches?.('details.more-actions')||d.open)return;const m=d.querySelector('.more-menu');m?.classList.remove('mm-in');const sub=m?.querySelector('.mm-sub');if(sub)sub.hidden=true},true);
document.addEventListener('keydown',e=>{if(e.key!=='Escape')return;const d=document.activeElement?.closest?.('details.more-actions[open]');if(!d)return;e.preventDefault();d.open=false;d.querySelector('summary')?.focus()});
// A Needs you line ends with one mark: a question keeps its "?" instead of getting ".".
const sentence=t=>{t=String(t).trim();return /[.?!…]$/.test(t)?t:t+'.'};
// A card waiting on the owner's answer: Answer leads and opens the Change editor under the question; Mark done and
// Hand off step back. Either a result whose needs_you is a question, with nothing to send, or a run that stopped to
// ask the owner: a blocker it wrote itself (no error of the service's own), not a sign-in and not waiting in the browser.
// A result that left the final click (submit, pay, book) to the owner: what that click is, or ''. Same rule as card() in assistant.py.
const finalStep=s=>{if(s.status!=='prepared'||s.handled_hint)return '';try{const o=JSON.parse(s.outcome||'{}');return o.state==='your_step'&&o.step||''}catch{return ''}};
// One that names its questions counts even after a browser step. Same rules as ask_blocked(), ask_text() and
// retry_pointless() in assistant.py.
// A run that named no questions asks nothing (it says what stopped it): Stuck and Try again, never Answer.
const askBlocked=s=>s.preparation_status==='blocked'&&!s.preparation_error&&!!String(s.preparation_reason||'').trim()&&retryLabel(s.preparation_reason)!=='Continue'&&(!!s.preparation_questions?.length||!s.preparation_no_questions&&!s.preparation_browser);
// The card's state in a word: its chip, and the chat's status line while it is stuck or preparing (chatStatus), so the two never
// disagree. A stopped run comes first: a card whose run stopped is not Preparing any more, whatever its status says.
// Closed by itself once its moment passed (expired_at): Not needed, like a dismissed one, so it never reads as done by them
const lapsed=s=>s.status==='completed'&&!!s.expired_at;
const cardState=s=>lapsed(s)?'Not needed':s.preparation_status==='blocked'&&!closed(s)&&s.status!=='snoozed'?(s.preparation_error==='stopped'?'Stopped':askBlocked(s)||moveAsk(s)||s.preparation_browser&&!s.preparation_error?'Needs your help':'Stuck'):['accepted','instructions'].includes(s.status)?'Preparing':label(s.status);
const askQuestion=(s,smart,hint)=>{if(closed(s)||s.status==='snoozed'||hint)return '';if(askBlocked(s))return s.preparation_questions?.length?s.preparation_questions.map(q=>q.question).join(' '):String(s.preparation_reason).trim();
 if(s.status!=='prepared'||s.preparation_status==='blocked'||smart.some(a=>a.kind!=='open'))return '';
 try{const o=JSON.parse(s.outcome||'{}'),q=String(o.needs||'').trim();return o.state==='needs_you'&&/\?$/.test(q)?q:''}catch{return ''}};
// A draft's Send opens the preview first: the button says so.
const sendLabel=a=>a.kind==='calendar'?CAL_LABEL[a.op]:a.kind==='doc_write'?DOC_LABEL[a.op]:a.kind==='doc_reply'?'Review and post':['email','email_demo','linkedin','slack','x','whatsapp','telegram','intercom'].includes(a.kind)&&/^Send\b/.test(a.label||'')?reviewSend(a.label):a.label;
// "Send reply" reads "Review and send reply": a known label whole, "to Sam" by its pattern, else the start translated
function reviewSend(label){const whole=label.replace(/^Send\b/,'Review and send'),rest=label.replace(/^Send\b\s*/,''),to=/^to (.+)$/.exec(rest);
 return !rest?t('Review and send'):I18N.cat?.[whole]!=null||I18N.en[whole]!=null?t(whole):to?t('Review and send to {}',to[1]):t('Review and send')+' '+rest}
// A step only the owner can do (a visit, a pickup; the review's owner_step): Done leads, and Plan it is what The Machine
// can do around it (a calendar slot, directions, a message if plans change). Never Do it. Same rule as controls() in assistant.py.
const ownerStep=s=>!!s.owner_step&&!closed(s)&&s.status!=='snoozed';
const ownerStepChoices=choices=>[['complete','Done'],...choices.filter(([c])=>c!=='complete').map(([c,t])=>c==='accept'?[c,'Plan it']:[c,t])];
// A to-do's project (graph.set_card_project): a chip to its page, and a small picker to change it or take it off.
// Set by hand it stays; otherwise the review or the project its thread or people are on chose it.
// The chip opens the project's page; Project under Details opens the picker.
const projectChip=s=>s.project_node?html`<a class="chip project-link" href="${graphHash(s.project_node.node_id)}" title="Project">${raw(CHIP_ICON.project)}<span>${s.project_node.name}</span></a>`:'';
async function cardProjectPick(id,anchor){let names=[];try{const r=await request('api/graph?view=projects');names=r.projects||[]}catch{}
 const s=(state.suggestions||[]).find(x=>x.id===id)||{},cur=s.project_node?.node_id||'';document.querySelector('.project-picker')?.remove();
 const box=document.createElement('div');box.className='project-picker';box.setAttribute('role','dialog');box.setAttribute('aria-label','Project for this to-do');
 box.innerHTML=`<label>Project <select>${cur?'':'<option value="" selected>Choose a project</option>'}${names.map(p=>`<option value="${esc(p.id)}"${p.id===cur?' selected':''}>${esc(p.name)}</option>`).join('')}</select></label>${cur?`<a class="pp-open" href="${esc(graphHash(cur))}">${esc(t('Open project'))} ›</a>`:''}<div class="actions"><button type="button" class="primary" data-pp="save">Save</button>${cur?'<button type="button" class="ghost" data-pp="none">No project</button>':''}<button type="button" class="quiet" data-pp="cancel">Cancel</button></div>`;
 anchor.closest('details.more-actions,details.chat-menu')?.removeAttribute('open');(anchor.closest('.card')||anchor.closest('.chat-main')||document.body).appendChild(box);box.querySelector('select').focus();
 box.onclick=async e=>{const b=e.target.closest('[data-pp]');if(!b)return;const k=b.dataset.pp;if(k==='cancel'){box.remove();return}
  const v=k==='none'?'':box.querySelector('select').value;if(k==='save'&&!v){box.remove();return}b.disabled=true;
  try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'card_project',args:{suggestion_id:id,project:v}})});
   const t=(state.suggestions||[]).find(x=>x.id===id);if(t){t.project_node=r.project;t.project=r.project?.name||null}box.remove();toast(r.project?'On '+r.project.name+'.':'Off its project.');if(typeof render==='function')render()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}}}
document.addEventListener('click',e=>{const b=e.target.closest('[data-card-project]');if(!b)return;e.preventDefault();cardProjectPick(b.dataset.cardProject,b)});
// A to-do's area (todo_areas.py): a tap on its area chip opens a small picker; Move moves it, with Undo on the toast.
// Its accounts become that area's, so what it may read and send from follows. A run that stopped to ask for a move (preparation_move_to) gets it as the to-do's lead button.
// A company by the name Connections shows (Work · Acme), from api/status areas: only real companies, never a profile's
// own source (todo_areas.companies). The picker starts on the area the run asked for, else where the to-do's people
// point (area_hint), else on Choose… with Move off until one is picked: never just the first.
const areaOrg=id=>(state.areas||[]).find(a=>a.id===id)?.name||String(id).slice(5),manyWork=()=>(state.areas||[]).filter(a=>a.id!=='personal').length>1;
const areaName=id=>id==='personal'?t('Personal'):manyWork()?t('Work at {}',areaOrg(id)):t('Work');
const moveText=id=>id==='personal'?t('Move to Personal'):manyWork()?t('Move to Work at {}',areaOrg(id)):t('Move to Work');
const movedText=id=>id==='personal'?t('Moved to Personal'):manyWork()?t('Moved to Work at {}',areaOrg(id)):t('Moved to Work');
const moveTargets=s=>!s.area||closed(s)?[]:(state.areas||[]).filter(a=>a.id!==s.area);
// Its area as a chip on its line, under All; Area under Details changes it (the picker).
const areaChip=s=>s.scope&&scopeFilter==='all'?html`<span class="chip scope">${s.scope==='work'?'Work':'Personal'}</span>`:'';
const moveAsk=s=>!closed(s)&&s.preparation_status==='blocked'&&!s.preparation_error&&!!s.preparation_move_to&&moveTargets(s).some(a=>a.id===s.preparation_move_to);
async function cardMove(id,area,b,undo){if(b)b.disabled=true;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'card_move',args:{suggestion_id:id,decision_id:crypto.randomUUID(),...(undo?{undo}:{area})}})});
  document.querySelector('.area-picker')?.remove();await refresh();if(typeof chatId!=='undefined'&&chatId===id&&typeof chatPoll==='function')chatPoll();
  if(undo){toast(t('Undone.'));return}
  toast(movedText(r.area));  // one that asked for it carries on by itself: Preparing shows on it
  const tt=$('#toast'),u=document.createElement('button');u.type='button';u.dataset.moveUndo=r.decision_id;u.dataset.id=id;u.textContent=t('Undo');tt.append(' ',u);clearTimeout(toastTimer);toastTimer=setTimeout(()=>tt.classList.remove('show'),15000)}
 catch(err){errCaught(err);toast(err.message,true)}finally{if(b)b.disabled=false}}
function cardAreaPick(id,anchor){const s=(state.suggestions||[]).find(x=>x.id===id)||{},to=moveTargets(s);document.querySelector('.area-picker')?.remove();if(!to.length)return;
 const pick=[s.preparation_move_to,s.area_hint,to.length===1&&to[0].id].find(x=>x&&to.some(a=>a.id===x))||'';
 const box=document.createElement('div');box.className='project-picker area-picker';box.setAttribute('role','dialog');box.setAttribute('aria-label',t('Area for this to-do'));
 box.innerHTML=`<label>${esc(t('Move to'))} <select>${pick?'':`<option value="" disabled selected>${esc(t('Choose…'))}</option>`}${to.map(a=>`<option value="${esc(a.id)}"${a.id===pick?' selected':''}>${esc(areaName(a.id))}</option>`).join('')}</select></label><div class="actions"><button type="button" class="primary" data-ap="move"${pick?'':' disabled'}>${esc(t('Move'))}</button><button type="button" class="quiet" data-ap="cancel">${esc(t('Cancel'))}</button></div>`;
 anchor.closest('details.more-actions,details.chat-menu')?.removeAttribute('open');(anchor.closest('.card')||anchor.closest('.chat-main')||document.body).appendChild(box);
 const sel=box.querySelector('select');sel.focus();sel.onchange=()=>{box.querySelector('[data-ap="move"]').disabled=!sel.value};
 box.onclick=e=>{const b=e.target.closest('[data-ap]');if(!b)return;if(b.dataset.ap==='cancel'){box.remove();return}if(sel.value)cardMove(id,sel.value,b)}}
document.addEventListener('click',e=>{const m=e.target.closest('[data-card-move]');if(m){e.preventDefault();m.closest('details.more-actions,details.chat-menu')?.removeAttribute('open');cardMove(m.dataset.cardMove,m.dataset.area,m);return}
 const p=e.target.closest('[data-card-area]');if(p){e.preventDefault();cardAreaPick(p.dataset.cardArea,p);return}
 const u=e.target.closest('[data-move-undo]');if(u){e.preventDefault();$('#toast').classList.remove('show');cardMove(u.dataset.id,null,null,u.dataset.moveUndo)}});
// A project's to-dos on its page: open ones, then the latest done (graph.project_todos).
const projectTodos=n=>n.kind==='project'&&n.todos?.length?`<div class="section-head"><h2>To-dos</h2><span class="count">${n.todos.filter(c=>!c.done).length||''}</span></div><article class="graph-open project-todos">${n.todos.map(c=>`<div class="promise${c.done?' done':''}"><span class="grow"><a href="#card=${esc(c.id)}" translate="no">${esc(c.title)}</a>${c.done?'<small>done</small>':c.due?`<small>due ${esc(day(c.due))}</small>`:''}</span></div>`).join('')}</article>`:'';
// First-use tips (Store.first_tips): on a new person's first to-dos, one short line under the buttons of the to-do it is
// about, one at a time. 'send' on the first ready draft (nothing goes out until Send), else 'change' on the first open
// to-do (Change how or Ask for changes, and Not needed, named as their buttons and working like them). A tip goes
// for good, on every device, once its button is used or × closes it. render() picks the to-do (tipSend, tipChange).
let tipSend='',tipChange='';const tipsGone=new Set();
const firstTips=()=>(state.first_tips||[]).filter(x=>!tipsGone.has(x));
const TIP_SEND_KINDS=['email','email_demo','linkedin','slack','x','whatsapp','telegram','intercom','doc_reply'];
const sendTipFits=s=>s.status==='prepared'&&!closed(s)&&!s.handled_hint&&!withTeammate(s)&&taskActions(s).some(a=>TIP_SEND_KINDS.includes(a.kind)&&draftText(a)&&!sendBusy(a.state||s.action_status));
function tipDone(tip){if(!firstTips().includes(tip))return;tipsGone.add(tip);
 request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'tip_done',args:{tip}})})
  .then(r=>{if(Array.isArray(r?.first_tips))state.first_tips=r.first_tips}).catch(()=>{})}
const tipLine=(tip,text)=>html`<p class="first-tip" data-tip="${tip}"><span class="tip-text">${text}</span><button type="button" class="tip-x" data-tip-done="${tip}" aria-label="Hide this tip" title="Hide this tip">×</button></p>`;
function firstTip(s,section,choices){if(closed(s)||!['Ready for you','Needs your decision'].includes(section))return '';
 if(tipSend)return tipSend===s.id?tipLine('send',t('You can edit it before it goes. It only goes out when you press Send.')):'';
 const change=choices.find(([c])=>c==='change'),reject=choices.find(([c])=>c==='reject');
 if(tipChange==='next'&&change&&reject&&!agentAsk(s)&&!withTeammate(s))tipChange=s.id;
 if(tipChange!==s.id)return '';
 const act=([c,label])=>html`<button type="button" class="tip-act" data-id="${s.id}" data-choice="${c}">${t(label)}</button>`;
 return tipLine('change',htmlT('Not quite right? {} tells me what to change. {} clears it.',act(change),act(reject)))}
function suggestionCard(s,section){
// A result that only answered, explained or planned leaves the task itself to do: Do it leads again.
const answered=s.status==='prepared'&&(()=>{try{return JSON.parse(s.outcome||'{}').state==='answered'}catch{return false}})();
const smart=taskActions(s),tpSent=taskPageSent(s,smart);
const handled=!closed(s)&&s.handled_hint?(()=>{try{return JSON.parse(s.handled_hint)}catch{return {}}})():{},hint=handled.reason||'';
const ask=askQuestion(s,smart,hint);
// Try again already ran without anything new and stopped asking again: retrying alone won't help, so it isn't offered.
const retryPointless=s.preparation_cause==='retry'&&askBlocked(s);
const asked=ask?[['answer','Answer'],...(s.preparation_status==='blocked'&&!retryPointless?[['retry',retryLabel(s.preparation_reason)]]:[]),['complete','Mark done'],['snooze','Snooze'],['reject','Not needed']]:withTeammate(s)?[['checkin','Check in now'],['complete','Mark done'],['snooze','Snooze'],['reject','Not needed']]:s.status==='pending'?[['accept',s.labels?.accept||'Do it'],['complete','Mark done'],['snooze','Snooze'],['change','Change how'],['reject',s.labels?.reject||'Not needed']]:s.status==='snoozed'?[['accept',s.handoff_wait?'Check in now':'Unsnooze'],['snooze','Change time'],['reject','Not needed']]:[...(s.preparation_status==='blocked'?[['retry',retryLabel(s.preparation_reason)]]:answered?[['accept','Do it']]:[]),['complete','Mark done'],['snooze','Snooze'],['change','Ask for changes'],['reject','Not needed']];
const choices=ownerStep(s)&&!ask?ownerStepChoices(asked):asked;
const notes=smart.map(a=>({action:a,state:a.state||s.action_status})).filter(x=>x.action!==tpSent&&actionNote(x.action.kind==='intercom'?{...x.state,as_name:x.action.as_name}:x.state,x.action.kind));
const undo=closed(s)&&s.undo_until&&Date.parse(s.undo_until)>Date.now();
const status=cardState(s);
// One status line, under the title: where it stands and what's left for you. A later sign that it's
// handled wins over the result's own line; nothing else repeats it.
const statusLine=(()=>{const line=(text,cls='')=>`<p class="note status-line${cls}">${format(text)}</p>`;
 // Snoozed from a Change ("remind me about this on Tuesday"): the card says until when, like the Snooze button's.
 if(s.status==='snoozed'&&s.snoozed_until&&(()=>{try{return JSON.parse(s.outcome||'{}').state==='snoozed'}catch{return false}})())return line('Snoozed until '+snoozedUntil(s.snoozed_until));
 if(closed(s)&&expiredLine(s))return line(expiredLine(s),' outcome done');
 if(closed(s))return doneLine(s);if(s.status==='snoozed')return '';let o=null;if(s.status==='prepared'&&s.outcome)try{o=JSON.parse(s.outcome)}catch{}
 if(o?.state==='already_done')return line('Looks done already. Mark it done if that’s right.',' outcome done');
 if(hint)return line((handled.fleet?'Done: ':'Looks handled: ')+hint,' handled');
 if(ask&&s.preparation_status==='blocked')return askLine(s,ask);
 if(s.early&&s.status==='accepted')return line('Preparing this ahead, so it arrives ready.');
 // A send on its way or done has its own line below; the result's needs line no longer holds.
 if(smart.some(a=>sendBusy(a.state||s.action_status)&&!['local_preparation','paused'].includes((a.state||s.action_status)?.status)))return '';
 // With a teammate (and nothing new to send them): their line says where it is, not an older "Needs you".
 if(withTeammate(s)||['asked','waiting for them'].includes(s.fleet_handoff?.stage)&&!redirect(s)&&['needs_you','your_step'].includes(o?.state))return '';
 if(o?.state==='needs_you'&&!skillDecided(s))return line('Needs you: '+sentence(o.needs),' outcome');
 // Waiting on a step still open elsewhere (a review, a merge, their reply): an open to-do, never "Looks done"
 if(o?.state==='waiting')return line(t('Waiting on: {}',sentence(o.waiting_on||'')),' outcome');
 if(s.early&&s.status==='prepared'&&smart.some(a=>a.kind!=='open'))return line('Ready to approve. Nothing goes out until you do.');
 // Prepared is not done: while a draft, change or final click still waits for them, never "Finished" (next_actions.WAITING_KINDS).
 if(s.status==='prepared'&&(!o||o.state==='done')&&smart.some(a=>[...DRAFT_KINDS,'merge'].includes(a.kind)))return line('Ready to approve. Nothing goes out until you do.',' outcome');
 if(o?.state==='answered')return line('Answered. Nothing done yet.');
 if(o?.state==='snoozed')return line('Back, as you asked.');
 if(o?.state==='your_step')return line('Ready for you to check and '+o.step+'.',' outcome');
 if(o?.state==='done')return line('Finished. Mark it done if it looks right.',' outcome done');
 return ''})();
// Like the site's demo card: a ready draft shows in an inset box, the source line sits under the content, and the prepared action leads the button grid.
const drafts=s.status==='prepared'&&!tpSent?smart.filter(a=>DRAFT_KINDS.includes(a.kind)&&draftText(a)):[];
// One faint line, like the site: the source itself opens the original; Read result and Copy draft (when there is a draft or file) sit at its end.
    const calOnly=smart.length&&smart.every(a=>a.kind==='calendar')&&!s.result_files?.length;
    const results=(s.status==='prepared'&&!calOnly)||s.result_files?.length?`<span class="foot-links"><button type="button" class="link" data-id="${s.id}" data-result="read">Read result</button>${(messageDrafts(s).length||s.result_files?.length)&&!copyLead(s,smart)&&!s.proposed_skill?`<button type="button" class="link" data-id="${s.id}" data-result="copy">Copy draft</button>`:''}</span>`:'';
    const readLabel=isEmail(s)?'Read email':'Read message',src=s.source_line?sourceHtml(s.source_line):'';
    const original=hasOriginal(s)?`<button type="button" class="link read-original via-${cardViaIcon(s)}" data-id="${s.id}" data-original="read" aria-label="${readLabel}" title="${readLabel}">${src||readLabel}<span aria-hidden="true"> ↗</span></button>`:src?`<p class="source">${src}</p>`:'';
// What only matters on a second look folds behind one Details: a closed to-do's coding agent result and the files it was
// made with, your note and the source line. The row under it keeps
// Details, when it comes back and the result links; a closed to-do's Reopen sits on the same row.
    const panel=(section==='Chat'?'':cardFields(s))+(closed(s)?agentBlock(s)+cardFiles(s):'')+teamLearningsUsed(s)+(s.latest_feedback?`<div class="saved-feedback" data-chat-open="${s.id}" title="Open the chat"><div class="row"><strong>Your note</strong>${time(s.latest_feedback.created_at,true)}<a class="see-chat" href="#chat=${s.id}">See in chat ›</a></div><blockquote>${format(s.latest_feedback.feedback)}</blockquote></div>`:'')+(original?`<div class="card-source">${original}</div>`:'');
    const detailsOpen=expandedDetails.has(s.id),toggle=panel||closed(s)&&section!=='Chat'&&String(s.body||'').length>40;  // a closed one's body is one line until Details opens
    const foot=toggle||s.snoozed_until&&!s.handoff_wait||results||section!=='Chat'?`<div class="card-foot">${toggle?`<button type="button" class="link details-toggle" data-details="${s.id}" aria-expanded="${detailsOpen}" aria-controls="details-${s.id}">Details</button>`:''}${s.snoozed_until&&!s.handoff_wait?`<span class="back-on" title="${esc(date(s.snoozed_until))}">${esc(backLabel(s.snoozed_until))}</span>`:''}${results}${section==='Chat'?'':chatLink(s)}</div>${toggle?`<div class="card-details" id="details-${s.id}"${detailsOpen?'':' hidden'}>${panel}</div>`:''}`:'';
// A page the task's own run worked on opens in the Machine's browser (its viewer, with that tab in front), never in yours.
const viewIn=s.browser_view&&!smart.some(a=>a.browser)?[{kind:'open',browser:true,label:s.browser_view.label,site:s.browser_view.site}]:[];
const smartButtons=s.status==='prepared'?[...smart,...viewIn].map(a=>a.kind==='handoff'?(canHandoff(s)||redirect(s)?`<button class="primary" data-fleet-handoff="${esc(s.id)}">${esc(a.to_name?'Review handoff to '+String(a.to_name).split(' ')[0]:a.label||'Hand off')}</button>`:''):a.kind==='open'&&a.browser?`<a class="open${finalStep(s)?' primary':''}" href="${esc(state.browser_link||'#')}" target="_blank" rel="noopener" data-browser-show="${esc(s.id)}"${a.site?` title="${esc(a.site)}, in your Machine’s browser"`:''}>${esc(a.label)} ↗</a>`:a.kind==='open'?`<a class="open" href="${esc(safeURL(a.url))}" target="_blank" rel="noreferrer">${esc(a.label)} ↗</a>`:!(a.kind==='finish'&&(a.state||s.action_status)?.status==='done')&&!sendBusy(a.state||s.action_status)?`<button class="primary" data-id="${s.id}" data-smart="${a.revision}">${esc(sendLabel(a)||(a.kind==='prepare'?'Prepare next step':'Review and send'))}</button>`:'').join(''):'';
// Under Details, a to-do's name, project and area (an open one's), each a tap to change (Rename, the project picker, the area
// picker). The title also renames with a tap on it, or E.
function cardFields(s){const f=(k,v,attr)=>html`<div><dt>${t(k)}</dt><dd><button type="button" class="field" ${attr}="${s.id}"><span translate="no">${v}</span></button></dd></div>`;
 return html`<dl class="card-fields">${f('Name',s.title,'data-rename')}${s.project_node?f('Project',s.project_node.name,'data-card-project'):''}${moveTargets(s).length?f('Area',areaName(s.area),'data-card-area'):''}</dl>`}
// A merged fix stays reversible for a day.
const unmerge=['prepared','completed'].includes(s.status)&&smart.some(a=>a.kind==='merge'&&Date.parse((a.state||s.action_status)?.undo_until||'')>Date.now())?`<button data-id="${s.id}" data-unmerge="1">Undo merge</button>`:'';
// Title first, then one quiet line: its state (when the section doesn't say it already), due, who, their organization,
// the project, Work or Personal (only under All) and when. Chat sits at the end of the Details row. Closed ones are compact (is-closed).
return `<article id="task-${s.id}" class="card todo t-${(lapsed(s)?'muted':tone(s.status))}${closed(s)?' is-closed':''}" data-status="${esc(s.status)}"><h3>${section==='Chat'?`<span translate="no">${esc(s.title)}</span>`:`<a class="title-link" href="#chat=${s.id}" title="Open the chat"><span translate="no">${esc(s.title)}</span></a>`}</h3><div class="meta"><div class="card-badges">${status!==section&&!['Look done','Waiting on others'].includes(section)?chip(status,(lapsed(s)?'muted':tone(s.status))):''}${dueChip(s)}${repeatChip(s)}${whoChip(s)}${projectChip(s)}${areaChip(s)}${s.status==='pending'&&s.deliver_after&&new Date(s.deliver_after)>new Date()&&deliveryLabel(s.deliver_after)?chip(deliveryLabel(s.deliver_after),'muted'):''}<span class="meta-side">${s.origin==='owner'?'<span class="added-by">Added by you</span>':''}${time(s.created_at,true)}</span></div></div>${mergeOffer(s)}${statusLine}${outboxLine(s)}${tpSent&&s.task_page.lead?`<p class="tp-lead" translate="no">${esc(s.task_page.lead)}</p>`:cardBody(s,section)}${gapLine(s,hint)}${closed(s)?'':cardFiles(s)}${handedNote(s)}${s.follow_up?.advice&&s.status==='prepared'?`<p class="note">${esc(t('The Machine would stop here: {}',s.follow_up.advice))}</p>`:''}${skillHintNote(s)}${familyInviteNote(s)}${fleetNote(s)}${meetBlock(s)}${reviewBlock(s)}${closed(s)?'':agentBlock(s)}${s.status==='prepared'?drafts.map(a=>draftBox(s,a,drafts.length>1?a.label:'')).join(''):''}${tpSent?taskPageSentLine(s,tpSent):''}${taskPageBlock(s)}${['queued','starting','running','blocked'].includes(s.preparation_status)&&!closed(s)&&s.status!=='snoozed'?preparationNote(s,ask):''}${s.change_prompt?.status==='uncertain'&&!closed(s)&&s.status!=='snoozed'?'<p class="note">I couldn’t confirm the message asking what to change. If it arrived, reply to it; otherwise use Ask for changes here.</p>':''}${s.status==='prepared'||s.status==='completed'?notes.filter(x=>s.status==='prepared'||x.state?.status==='sent').map(x=>{const st=x.state?.status;return `<p class="note${st==='sent'?' sent-ok':''}">${smart.length>1?esc(x.action.label)+': ':''}${esc(actionNote(x.action.kind==='intercom'?{...x.state,as_name:x.action.as_name}:x.state,x.action.kind,x.action))}</p>${['queued','sending'].includes(st)?'<div class="send-progress" aria-hidden="true"><i></i></div>':''}`}).join(''):''}${foot}${closed(s)?`<div class="actions">${s.follow_up?.back?`<button class="ghost" data-fu-back="${esc(s.id)}">${esc(t('Bring back'))}</button>`:undo&&s.status!=='completed'?`<button class="ghost" data-id="${s.id}" data-choice="undo">Undo Not needed</button>`:''}${s.status==='completed'&&undo&&s.expired_at?`<button class="ghost" data-id="${s.id}" data-choice="undo">Undo</button>`:s.status==='completed'?`<button class="ghost" data-id="${s.id}" data-choice="reopen">Reopen</button>`:''}</div>`:`${changing.has(s.id)?`<div class="change-editor${ask?' answer-editor':''}"><label for="feedback-${s.id}">${ask?'Your answer':s.status==='pending'?'How should I do it instead?':'What should I change?'}</label><div class="mic-wrap"><textarea id="feedback-${s.id}" placeholder="${ask?'Type it here (Ctrl+Enter sends)':'Tell me what to change (Ctrl+Enter saves)'}"></textarea>${micBtn()}</div><div class="actions"><button class="primary" data-id="${s.id}" data-choice="other"${ask?' data-answer="1"':''}>${ask?'Send answer':'Save changes'}</button>${ask?'':(smartButtons.match(/<button class="primary" data-id="[^"]+" data-smart="[^"]+">[^<]*<\/button>/g)||[]).map(b=>b.replace('class="primary"','class="ghost"')).join('')}<button class="ghost" data-id="${s.id}" data-choice="cancel-change">Cancel</button></div></div>`:''}${handoffEditor(s)}${reviewEditor(s)}${agentEditor(s)}${agentAskEditor(s)}${dismissing.has(s.id)?`<div class="change-editor dismiss-editor"><p class="dismiss-q" id="dismiss-q-${s.id}">Why isn’t this needed? <small>Optional</small></p><div class="reason-chips" role="group" aria-labelledby="dismiss-q-${s.id}">${['Not relevant','Wrong facts','Already handled'].map(r=>`<button type="button" class="reason" aria-pressed="false" data-id="${s.id}" data-choice="dismiss-pick" data-reason="${r}">${r}</button>`).join('')}</div><textarea id="dismiss-${s.id}" rows="1" aria-label="Note (optional)" placeholder="Add a note (optional)"></textarea><div class="actions"><button class="primary" data-id="${s.id}" data-choice="dismiss-typed">Confirm not needed</button><button class="ghost" data-id="${s.id}" data-choice="cancel-dismiss">Cancel</button></div></div>`:''}${changing.has(s.id)||dismissing.has(s.id)||handingOff.has(s.id)||reviewing.has(s.id)||reviewHolds(s)||agentEditing.has(s.id)||agentAsking.has(s.id)||pageApprove.has(s.id)?'':(meetOpen(s)?meetActions(s):s.fleet_handoff?.back&&s.status!=='snoozed'&&!ask?handoffBackActions(s):cardActions(s,choices,smartButtons,unmerge,hint,smart))+firstTip(s,section,choices)}`}</article>`;
}
// Success notices clear themselves after a few seconds; errors stay until the next notice.
let noticeTimer;const notice=(text,error=false)=>{const n=$('#notice');n.textContent=text;n.className=error?'error':'';clearTimeout(noticeTimer);if(text&&!error)noticeTimer=setTimeout(()=>{if(n.textContent===text)n.textContent=''},4500)};
// Preparing shows a live clock and the latest steps the AI run took; Needs your help keeps the technical details folded away.
const steps=new Map(),openTech=new Set();
const elapsed=v=>{const t=Math.max(0,Math.floor((Date.now()-new Date(v))/1000));return Math.floor(t/60)+':'+String(t%60).padStart(2,'0')};
// A preparation that waits on the browser (a sign-in, a captcha, a code) offers it: the viewer when this install has one
// (with the task's tab brought to the front there too), otherwise its tab brought to the front on this computer.
// Sign in only while the run waits on a sign-in right now (b.sign_in); past that step, even while still on the
// browser, it's only Open the browser.
// Open the browser: a link to the viewer when there is one (the Browser pane on a computer), else a button that brings
// the browser on this computer to the front. In the chat the run's live picture is that link (peekHTML).
const browserOpen=(id,b,img='')=>{const at=`data-browser-focus="${esc(id)}" data-task="${esc(id)}" data-page="${esc(b.page||'')}"`,cls=img?'peek-thumb':'browser-link',lab=img?' aria-label="Open the browser" title="What the browser shows now"':'';
 return safeURL(b.link)?`<a class="${cls}" href="${esc(b.link)}" target="_blank" rel="noopener" ${at}${lab} data-quiet>${img||'Open the browser'}</a>`:`<button type="button" class="${cls}" ${at}${lab}>${img||'Open the browser'}</button>`};
const browserLink=(id,b)=>!b?'':(b.sign_in?`<button type="button" class="browser-link" data-signin data-task="${esc(id)}" data-page="${esc(b.page||'')}">Sign in</button> `:'')+browserOpen(id,b);
const browserNodes=(id,b)=>{if(!b)return [];const at={'data-browser-focus':id,'data-task':id,'data-page':b.page||''};
 return [...b.sign_in?[make('button',{type:'button',class:'browser-link','data-signin':'','data-task':id,'data-page':b.page||''},'Sign in'),' ']:[],
  safeURL(b.link)?make('a',{class:'browser-link',href:b.link,target:'_blank',rel:'noopener',...at,'data-quiet':''},'Open the browser'):make('button',{type:'button',class:'browser-link',...at},'Open the browser')]};
// A run that stopped to ask: its questions as the Needs you line, each clear choice as quick picks that fill the answer box.
function askLine(s,ask){const qs=s.preparation_questions||[];
 if(!qs.length)return `<p class="note status-line outcome">${esc('Needs you: '+sentence(ask))}</p>`;
 return `<div class="note status-line outcome ask-line"><span>Needs you:</span>${qs.map((q,i)=>`<div class="ask-q"><p>${esc(sentence(q.question))}</p>${q.options?.length?`<div class="reason-chips" role="group" aria-label="${esc(q.question)}">${q.options.map(o=>`<button type="button" class="reason pick" aria-pressed="false" data-id="${s.id}" data-choice="pick" data-q="${i}" data-pick="${esc(o)}">${esc(o)}</button>`).join('')}</div>`:''}</div>`).join('')}</div>`}
// Technical details on a card that asks: without local paths or long internal IDs.
const plainDetails=t=>String(t||'').replace(/(?:~|\/home|\/tmp|\/var|\/Users|memory|data)\/[^\s,;:)"'”]+/g,'…').replace(/\b(?=[A-Za-z0-9_-]*\d)[A-Za-z0-9_-]{20,}\b|\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/g,'…');
// A run's latest three steps, one line each, in a box that keeps its height from the start: the to-do doesn't grow
// line by line while it works.
const stepItems=list=>(list||[]).slice(-1).map(x=>`<li title="${esc(x.title)}">${esc(x.title)}</li>`).join('');
const stepNodes=list=>(list||[]).slice(-1).map(x=>make('li',{title:String(x.title??'')},String(x.title??'')));
// Why a queued run waits (s.preparation_hold from the dispatcher: why, until): said on its to-do instead of "I'll start
// shortly." for minutes. No hold: it starts within seconds. ai: its start waits for the Gateway to come back (a reboot,
// a restart), shown instead of a live "Preparing…" timer; it carries on by itself (assistant.py PREPARATION_WAITING).
function holdNote(h){if(!h)return '';const when=pauseWhen(h.until);
 if(h.why==='ai')return t('Waiting for the AI to come back. Then I’ll carry on.');
 if(h.why==='limit')return when?t('Waiting for the usage limit to reset. Starts around {}.',when):t('Waiting for the usage limit to reset.');
 if(h.why==='budget')return when?t('Saving usage for now. Starts around {}.',when):t('Saving usage for now. Starts when there’s room.');
 if(h.why==='retry')return when?t('Trying again around {}.',when):'';
 return {after:t('Starts after the current one.'),busy:t('Starts when one of the running to-dos finishes.'),others:t('Starts after the other to-dos.'),paused:t('Follow-ups are paused.')}[h.why]||''}
function preparationNote(s,ask=''){
if(s.preparation_status==='starting'&&s.preparation_error==='openclaw_unavailable')return `<p class="note">${esc(holdNote({why:'ai'}))}</p>`;
if(s.preparation_status==='queued')return `<p class="note">${esc(holdNote(s.preparation_hold)||(s.preparation_retried?'That attempt didn’t finish, so I’m trying once more…':s.preparation_signed_in?'Signed in. I’ll start shortly.':'I’ll start shortly.'))}</p>`;
// A blocker that asks the owner already leads as the Needs you line: not said twice.
if(s.preparation_status==='blocked')return `${ask?(s.preparation_browser?`<p class="note">${browserLink(s.id,s.preparation_browser)}</p>`:''):`<p class="note">${format(s.preparation_reason||'I couldn’t finish this. You can try again or change the request.')} ${browserLink(s.id,s.preparation_browser)}</p>`}${s.preparation_details?`<details class="tech" data-tech="${s.id}" ${openTech.has(s.id)?'open':''}><summary>${ask?'Technical details':'Details'}</summary><pre>${linkText(ask?plainDetails(s.preparation_details):s.preparation_details)}</pre></details>`:''}`;
return `<div class="prep"><div class="prep-main"><p class="note">Preparing… ${s.preparation_started_at?`<span class="elapsed" data-since="${esc(s.preparation_started_at)}">${elapsed(s.preparation_started_at)}</span>`:''}${s.preparation_retried?' · second try':''} <span data-browser="${s.id}">${browserLink(s.id,s.preparation_browser)}</span></p><ul class="steps" data-steps="${s.id}" aria-live="polite">${stepItems(steps.get(s.id))}</ul></div><div class="peek" data-peek="${s.id}">${peekHTML(s.id)}</div></div>`}
// While a preparation is on the browser, its card shows that tab live: a small picture every few seconds (right of
// the steps; below them on a phone), larger on a click. Only the tab the run opened itself; gone when it stops.
const peeks=new Map();
// The chat shows the same picture where its Open the browser link is (a slot with data-peek-via): a click there opens
// the Browser pane, as the link does; without a picture the slot holds the link itself.
const peekHTML=(id,b)=>{const p=peeks.get(id);if(!(p?.on&&p.image))return b?browserLink(id,b):'';const img=`<img alt="The Machine’s browser, now" src="${esc(p.image)}">`;
 return b?browserOpen(id,b,img):`<button type="button" class="peek-thumb" data-peek-open="${esc(id)}" aria-label="See the browser larger" title="What the browser shows now">${img}</button>`};
function paintPeek(id){const p=peeks.get(id);for(const slot of document.querySelectorAll(`[data-peek="${CSS.escape(id)}"]`)){const img=slot.querySelector('img');
 if(img&&p?.on&&p.image){if(img.getAttribute('src')!==p.image)img.src=p.image;continue}
 // In the chat the picture coming or going keeps the thread where it is (at the end it stays at the end)
 const html=peekHTML(id,'peekVia' in slot.dataset?JSON.parse(slot.dataset.peekVia||'{}'):null);if(slot.innerHTML===html)continue;
 if(slot.closest('.chat-main'))chatKeepPlace(()=>{slot.innerHTML=html});else slot.innerHTML=html}
 const d=$('#peek-dialog');if(d.open&&d.dataset.task===id){if(p?.on&&p.image)$('#peek-image').src=p.image;else d.close()}}
setInterval(async()=>{if(document.hidden)return;for(const [id,p] of peeks){if(!p.on)continue;if(!document.getElementById('task-'+id)){peeks.delete(id);continue}
 try{const r=await request('api/peek?id='+encodeURIComponent(id));p.on=r.on;if(r.image)p.image=r.image;paintPeek(id)}catch{}}},2500);
document.addEventListener('click',e=>{const b=e.target.closest('[data-peek-open]');if(!b)return;const id=b.dataset.peekOpen,p=peeks.get(id);if(!p?.image)return;const d=$('#peek-dialog');d.dataset.task=id;$('#peek-image').src=p.image;d.showModal()});
