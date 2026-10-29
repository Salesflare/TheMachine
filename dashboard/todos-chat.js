// Like Slack: in use means visible, in focus and touched in the last 10 minutes. Open in the background, minimized or
// idle, it isn't, and the Machine notifies (a push a minute after, an email if still unseen later). The page says so
// at once when that changes, and every minute while in use; the Machine forgets a page after two.
const notifyPresence=(()=>{const id=Math.random().toString(36).slice(2,12)||'page',IDLE=6e5;let input=Date.now(),last=0,was=null;
 const inUse=()=>document.visibilityState==='visible'&&document.hasFocus()&&Date.now()-input<IDLE;
 const beat=()=>{if(!state?.notify)return;const on=inUse();if(on===was&&(!on||Date.now()-last<55e3))return;was=on;last=Date.now();
  notifyPost('notify_active',{client:id,active:on,idle:Math.round((Date.now()-input)/1e3)}).catch(()=>{was=null})};
 const touched=()=>{input=Date.now();if(!was)beat()};
 for(const ev of ['pointerdown','pointermove','keydown','wheel','touchstart','scroll'])addEventListener(ev,touched,{passive:true,capture:true});
 setInterval(beat,3e4);addEventListener('focus',beat);addEventListener('blur',beat);document.addEventListener('visibilitychange',beat);addEventListener('pagehide',beat);
 return {beat,inUse,id}})();
function openCardLink(){
const m=/^#card=([a-f0-9]{16})$/.exec(location.hash);if(!m||!state.suggestions)return;
const target=state.suggestions.find(s=>s.id===m[1]);if(!target)return; // Keep the link for a later successful refresh.
linkedCardId=target.id;const fuEl=()=>target.follow_up?.group&&document.getElementById('fu-'+target.follow_up.group.replace(':','-'));
// Reveal this destination without overwriting the device's saved filter/fold preferences.
if(scopeFilter!=='all'&&target.scope!==scopeFilter)scopeFilter='all';
folded.delete(placeOf(target));if(looksDone(target))lookExpanded.add(target.id);
render();document.querySelector('nav [data-tab="inbox"]').click();
const c=document.getElementById('task-'+target.id)||fuEl();if(!c)return;
for(let parent=c.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;
history.replaceState(null,'',location.pathname+location.search);
c.scrollIntoView({block:'center',behavior:'smooth'});c.classList.remove('flash');void c.offsetWidth;c.classList.add('flash');kbFocus(c,false)}
// Card chat (#chat=<id>): a card's whole story as a conversation, strictly by time: the messages it is about, what the
// Machine did (its steps folded into one quiet line before each reply) and the drafts it wrote, what you said and
// what went out. The card's buttons sit in a slim bar above the message box. A message is a Change (the same decide
// path, so the card, Telegram and learning stay in step). Read through the service only (card_chat), about once a
// second while the card's run is going.
let chatId=null,chat=null,chatTimer=null,chatDrawer=false;
const chatOpen=()=>chatId&&state.suggestions?.find(s=>s.id===chatId)||null;
// The browser's own locale for times, except an English browser outside the US reads them the 24-hour way.
const chatHM=at=>fmtHM(at);
const chatDayOf=at=>{const d=new Date(at),t=new Date();t.setHours(0,0,0,0);const n=Math.round((t-new Date(d).setHours(0,0,0,0))/864e5);
 return n===0?'Today':n===1?'Yesterday':d.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short',...(d.getFullYear()!==t.getFullYear()?{year:'numeric'}:{})})};
// Light markdown for a reply: paragraphs, lists, headings as bold lines, **bold**, *italic* and links.
// Slack-style emoji shortcodes (":tada:") as emoji; an unknown code, or one with a skin tone suffix, stays as typed
const EMOJI={"smile":"😄","smiley":"😃","grinning":"😀","grin":"😁","joy":"😂","rofl":"🤣","sweat_smile":"😅","laughing":"😆","wink":"😉","blush":"😊","slightly_smiling_face":"🙂","upside_down_face":"🙃","heart_eyes":"😍","kissing_heart":"😘","thinking_face":"🤔","thinking":"🤔","face_with_hand_over_mouth":"🤭","shushing_face":"🤫","neutral_face":"😐","expressionless":"😑","no_mouth":"😶","smirk":"😏","unamused":"😒","roll_eyes":"🙄","face_with_rolling_eyes":"🙄","grimacing":"😬","relieved":"😌","pensive":"😔","sleepy":"😪","sleeping":"😴","mask":"😷","nerd_face":"🤓","sunglasses":"😎","confused":"😕","worried":"😟","open_mouth":"😮","astonished":"😲","flushed":"😳","pleading_face":"🥺","cry":"😢","sob":"😭","scream":"😱","sweat":"😓","weary":"😩","tired_face":"😫","yawning_face":"🥱","triumph":"😤","rage":"😡","angry":"😠","exploding_head":"🤯","partying_face":"🥳","star_struck":"🤩","zany_face":"🤪","money_mouth_face":"🤑","hugging_face":"🤗","hugs":"🤗","saluting_face":"🫡","melting_face":"🫠","skull":"💀","ghost":"👻","robot_face":"🤖","see_no_evil":"🙈","hear_no_evil":"🙉","speak_no_evil":"🙊","heart":"❤️","orange_heart":"🧡","yellow_heart":"💛","green_heart":"💚","blue_heart":"💙","purple_heart":"💜","black_heart":"🖤","white_heart":"🤍","broken_heart":"💔","sparkling_heart":"💖","100":"💯","fire":"🔥","sparkles":"✨","star":"⭐","tada":"🎉","confetti_ball":"🎊","balloon":"🎈","gift":"🎁","trophy":"🏆","rocket":"🚀","zap":"⚡","boom":"💥","bulb":"💡","eyes":"👀","wave":"👋","raised_hands":"🙌","clap":"👏","pray":"🙏","muscle":"💪","ok_hand":"👌","+1":"👍","thumbsup":"👍","-1":"👎","thumbsdown":"👎","point_up":"☝️","point_right":"👉","point_left":"👈","point_down":"👇","v":"✌️","crossed_fingers":"🤞","handshake":"🤝","facepalm":"🤦","face_palm":"🤦","shrug":"🤷","man_shrugging":"🤷‍♂️","woman_shrugging":"🤷‍♀️","white_check_mark":"✅","heavy_check_mark":"✔️","x":"❌","warning":"⚠️","no_entry":"⛔","question":"❓","exclamation":"❗","bangbang":"‼️","heavy_plus_sign":"➕","arrow_right":"➡️","arrow_left":"⬅️","arrow_up":"⬆️","arrow_down":"⬇️","repeat":"🔁","hourglass":"⌛","hourglass_flowing_sand":"⏳","alarm_clock":"⏰","calendar":"📆","date":"📅","memo":"📝","pencil":"📝","pencil2":"✏️","email":"📧","envelope":"✉️","phone":"☎️","iphone":"📱","computer":"💻","link":"🔗","lock":"🔒","unlock":"🔓","key":"🔑","mag":"🔍","chart_with_upwards_trend":"📈","chart_with_downwards_trend":"📉","moneybag":"💰","dollar":"💵","euro":"💶","coffee":"☕","beer":"🍺","beers":"🍻","champagne":"🍾","pizza":"🍕","cake":"🍰","sunny":"☀️","cloud":"☁️","rain_cloud":"🌧️","snowflake":"❄️","rainbow":"🌈","earth_africa":"🌍","car":"🚗","airplane":"✈️","house":"🏠","office":"🏢","dog":"🐶","cat":"🐱","unicorn_face":"🦄","raised_hand":"✋","writing_hand":"✍️","brain":"🧠","money_with_wings":"💸","pushpin":"📌","paperclip":"📎","package":"📦","construction":"🚧","sos":"🆘","ok":"🆗","new":"🆕","cool":"🆒","free":"🆓","heavy_minus_sign":"➖","slightly_frowning_face":"🙁","frowning":"😦","disappointed":"😞","hushed":"😯","innocent":"😇","yum":"😋","stuck_out_tongue":"😛","stuck_out_tongue_winking_eye":"😜","kissing":"😗","relaxed":"☺️","star2":"🌟","dizzy":"💫","sweat_drops":"💦","dash":"💨","zzz":"💤"};
const chatEmoji=t=>String(t).replace(/:([a-z0-9_+-]{1,40}):(?!:)/g,(m,k)=>EMOJI[k]||m);
function chatMarkdown(text){text=chatEmoji(text);const out=[];let list=null,para=[],quote=null;
 // Quoted lines ("> …") are a quote, never a raw ">"
 const src=String(text||'').split('\n'),lines=[];for(const l of src){const q=/^\s*>\s?(.*)$/.exec(l);if(q){(quote??=[]).push(q[1]);continue}if(quote){lines.push({quote});quote=null}lines.push(l)}if(quote)lines.push({quote});
 const inline=t=>format(t).replace(/(^|[^*\w])\*([^*\n]+)\*(?!\*)/g,'$1<em>$2</em>');
 const flush=()=>{if(para.length)out.push(`<p>${para.map(inline).join('<br>')}</p>`);para=[];if(list)out.push(`<${list.tag}>${list.items.map(i=>`<li>${inline(i)}</li>`).join('')}</${list.tag}>`);list=null};
 for(const line of lines){if(line.quote){flush();out.push(`<blockquote class="chat-quote">${chatMarkdown(line.quote.join('\n'))}</blockquote>`);continue}const b=/^\s*[-*•]\s+(.*)$/.exec(line),n=/^\s*\d+[.)]\s+(.*)$/.exec(line),h=/^\s*#{1,6}\s+(.*)$/.exec(line);
  if(!line.trim()){flush();continue}
  if(b||n){const tag=b?'ul':'ol';if(para.length||list&&list.tag!==tag)flush();list??={tag,items:[]};list.items.push((b||n)[1]);continue}
  if(list)flush();para.push(h?`**${h[1].replace(/\*\*/g,'')}**`:line)}
 flush();return out.join('')}
// What changed between two versions of a draft, word by word.
function chatDiff(a,b){const x=String(a).split(/(\s+)/),y=String(b).split(/(\s+)/);if(x.length*y.length>400000)return null;
 const m=x.length,n=y.length,L=Array.from({length:m+1},()=>new Uint16Array(n+1));
 for(let i=m-1;i>=0;i--)for(let j=n-1;j>=0;j--)L[i][j]=x[i]===y[j]?L[i+1][j+1]+1:Math.max(L[i+1][j],L[i][j+1]);
 const out=[];let i=0,j=0;const push=(k,t)=>{const l=out.at(-1);l&&l[0]===k?l[1]+=t:out.push([k,t])};
 while(i<m&&j<n){if(x[i]===y[j]){push('=',x[i]);i++;j++}else if(L[i+1][j]>=L[i][j+1])push('-',x[i++]);else push('+',y[j++])}
 while(i<m)push('-',x[i++]);while(j<n)push('+',y[j++]);
 return out.map(([k,t])=>k==='='?esc(t):k==='-'?(t.trim()?`<del>${esc(t)}</del>`:''):`<ins>${esc(t)}</ins>`).join('')}
// The card's own pieces for the chat, taken from the card as the dashboard draws it, so they stay the same.
// The card's own sends (their state refreshes every 2 s while one goes out): what the chat's draft says under it
const CHAT_SENDS=['email','linkedin','slack','x','whatsapp','telegram','intercom','doc_reply'];
const chatSends=s=>taskActions(s).filter(a=>CHAT_SENDS.includes(a.kind)).map(a=>({a,st:a.state||s.action_status})).filter(x=>x.st?.status);
const chatGoing=st=>['queued','sending'].includes(st?.status)||st?.status==='uncertain'&&!st.retry_ok;
const chatFailed=st=>['failed','blocked'].includes(st?.status)||!!st?.retry_ok;
const CHAT_BY={email:'Sent to {} by email',email_demo:'Sent to {} by email',slack:'Sent to {} on Slack',linkedin:'Sent to {} on LinkedIn',whatsapp:'Sent to {} on WhatsApp',telegram:'Sent to {} on Telegram',x:'Sent to {} on X',intercom:'Sent to {} in Intercom',doc_reply:'Sent to {} in the doc'};
function chatSendLine(d,x){const st=x.st,who=d.to.length&&!d.to.some(v=>v.includes('@'))?d.to.join(', '):x.a.to_name?.split(/\s+/)[0]||d.to.join(', ')||t('them');
 if(chatGoing(st))return `<p class="chat-sendstate" role="status">${esc(t(st.status==='uncertain'?'Checking it went out…':'Sending…'))}</p><div class="send-progress" aria-hidden="true"><i></i></div>`;
 if(st.status==='sent')return `<p class="chat-sendstate ok" role="status">${esc(d.kind==='intercom'?t('Sent as {}',x.a.as_name||t('your Intercom admin')):t(CHAT_BY[d.kind]||'Sent to {}',who))}${st.sent_at?' · '+chatHM(Date.parse(st.sent_at)):''}</p>`;
 if(chatFailed(st))return `<p class="chat-sendstate failed" role="alert">${st.retry_ok?esc(st.error):esc(t('Didn’t go out.'))+(st.error?' '+esc(st.error):'')}</p>`;
 return ''}
function chatParts(s){const t=document.createElement('template');t.innerHTML=suggestionCard(s,'Chat');const card=t.content.querySelector('article');
 const acts=[...(card?.querySelector(':scope>.actions')?.children||[])].flatMap(n=>n.matches('details.more-actions')?[...n.querySelector('.more-menu').children]:[n])
  .filter(n=>!['change','answer','cancel-change'].includes(n.dataset.choice)&&n.dataset.handoffCheckin==null);  // in the chat already: no Check in now
 // A snoozed card's way back is Unsnooze; a closed one's is Reopen or Undo: a text button on the status line
 const back=s.status==='snoozed'?acts.find(n=>n.dataset.choice==='accept'):closed(s)?acts.find(n=>n.dataset.fuBack)||acts.find(n=>n.dataset.choice==='reopen')||acts.find(n=>n.dataset.choice==='undo'):null;
 if(back){back.className='link chat-inline';if(!back.dataset.fuBack)back.textContent=s.status==='snoozed'?(s.handoff_wait?'Check in now':'Unsnooze'):'Reopen'}
 const sends=chatSends(s),going=sends.some(x=>chatGoing(x.st)),went=sends.some(x=>x.st.status==='sent');
 // While a message goes out nothing is the next step yet; once it went out, Mark done is; after a failure, Try again
 let lead=back||going?null:acts.find(n=>n.classList.contains('primary'))||(withTeammate(s)?acts.find(n=>n.dataset.choice==='complete'):null)||null;
 if(went&&!going&&!back&&!lead?.dataset.smart)lead=acts.find(n=>n.dataset.choice==='complete')||lead;
 if(lead?.dataset.smart&&chatFailed(sends.find(x=>String(x.a.revision)===lead.dataset.smart)?.st))lead.textContent='Try again';
 const rest=acts.filter(n=>n!==lead&&n!==back);
 const decide=rest.filter(n=>['complete','snooze','reject','accept','retry'].includes(n.dataset.choice)||n.dataset.smart!=null);
 const status=card?.querySelector('.status-line:not(.ask-line):not(.done-line)')?.textContent.trim()||card?.querySelector('.card-badges .chip')?.textContent.trim()||'';
 const body=card?.querySelector('.body');body?.classList.remove('clamp');
 const panel=[...(card?.querySelectorAll('.merge-offer,.change-editor:not([class*="answer"]),.fleet-handoff-form')||[])].filter(n=>!n.querySelector('[id^="feedback-"]')).map(n=>n.outerHTML).join('')
  +(['blocked','running','starting'].includes(s.preparation_status)&&s.preparation_browser?`<p class="note">${browserLink(s.id,s.preparation_browser)}</p>`:'');
 const html=n=>n?.outerHTML||'';
 return {sends,going,sheet:html(card?.querySelector('.agent-form')),lead:html(lead),send:!!lead?.dataset.smart,copy:lead?.dataset.result==='copy',back:html(back),rest:rest.map(html).join(''),options:[lead,...decide].filter(Boolean).slice(0,3).map(n=>{n.classList.remove('ghost','primary');n.classList.add(n===lead?'primary':'ghost');return n.outerHTML}).join(''),
  status,intro:body?.innerHTML||'',ask:html(card?.querySelector('.ask-line')),agent:html(card?.querySelector('.agent-job')),
  links:card?.querySelector('.foot-links')?.innerHTML||'',panel}}
// What the card asks of the owner, in one plain line, when its text doesn't already ask: the question its run wrote,
// else from the title's "X needs your call on Y". An offer the card ends with ("I can check … and draft …") becomes a suggestion instead.
const CHAT_OFFER=/(?:^|\s)((?:I can|I could|I'll|I will|Happy to)\s[^.!?]*[.!?]?)\s*$/;
function chatQuestion(s){const body=String(s.body||'').trim(),offer=CHAT_OFFER.exec(body),rest=offer?body.slice(0,offer.index).trim().replace(/[;,:]$/,'.'):body;
 const m=/^.+?\s(?:needs|wants|is waiting (?:on|for)|awaits)\s+your\s+(call|decision|go-ahead|approval|ok|answer|input|help)\s+(?:on|about|for|with)\s+(.+?)[.?!]?$/i.exec(s.title||'');
 const own=s.preparation_questions?.[0]?.question,ask=/\?\s*$/.test(rest)?'':own?String(own).trim().replace(/[.?!]?$/,'?'):m?`Your ${/answer/i.test(m[1])?'answer':/input|help/i.test(m[1])?'input':'call'}: ${m[2]}?`:/^(?:Decide|Choose|Pick|Approve|Confirm)\b/.test(s.title||'')?String(s.title).replace(/[.?!]?$/,'?'):'';
 return {ask,offer:ask&&offer?offer[1]:'',body:ask&&offer?rest:body}}
const chatOpenSet=new Set();  // what is unfolded (steps, long messages, drafts, diffs, repeated taps), kept through a poll
const chatFold=(key,cls,summary,body)=>`<details class="${cls}" data-fold-key="${esc(key)}"${chatOpenSet.has(key)?' open':''}><summary>${summary}</summary>${body}</details>`;
const chatLong=(t,lines=4)=>String(t||'').split('\n').length>lines||String(t||'').length>lines*70;
const chatViaIcon=(v,note)=>note?'note':/^(email|gmail|outlook|mail)/i.test(v||'')?'mail':/calendar/i.test(v||'')?'cal':'chat';
const CHAT_VIA={email:'Email',gmail:'Email',slack:'Slack',linkedin:'LinkedIn',whatsapp:'WhatsApp',telegram:'Telegram',x:'X',calendar:'Calendar',intercom:'Intercom',github:'GitHub',android:'Phone'};
// The owner's own taps read as what they did, not a bare button name
// (said without "You": the side already says who)
const CHAT_TAPS={'Do it':'Chose Do it','Plan it':'Chose Plan it','Reopened':'Reopened it','Snoozed':'Snoozed it','Unsnoozed':'Unsnoozed it','Back for a check-in':'Brought it back for a check-in','Check-in moved':'Moved the check-in','Marked done':'Marked it done','Not done yet':'Marked it not done'};
// A send approved by voice waits a few seconds with Undo; the chat paints again when that ends
let chatUndoTimer=null;
const chatUndoVoice=(s,i)=>{clearTimeout(chatUndoTimer);chatUndoTimer=setTimeout(()=>paintChat(),i.undo_until-Date.now()+50);return ` · <button type="button" class="link" data-voice-undo="${esc(i.undo_voice)}" data-sid="${esc(s.id)}">Undo</button>`};
const chatEventText=i=>String(i.mine&&CHAT_TAPS[i.text]||i.text||'').replace(/^You\s+(\S)/,(m,c)=>c.toUpperCase());
const chatVia=v=>CHAT_VIA[v]||(v&&v!=='signal'?v[0].toUpperCase()+v.slice(1):'');
// Whose side an item is on: the owner's messages and taps on the right, the Machine and the people it is about on the left.
const chatSide=i=>i.kind==='you'||i.kind==='event'&&i.mine||i.kind==='source'&&i.mine?'you':i.kind==='event'||i.kind==='learned'?'mid':'them';
// What a note on this card taught (from what was stored, never from what a reply says): a quiet line that opens it on
// What I've learned, with Edit and Undo while it is there (a channel's voice has its own 'Saved to How you write' line).
function chatLearned(i){const sep='<span class="learned-sep" aria-hidden="true">·</span>',q=i.text?`<q>${esc(i.text)}</q>`:'';
 if(i.state==='removed')return `<div class="chat-event chat-learned gone"><span class="learned-acts">Removed from what I’ve learned</span>${q}</div>`;
 const id=i.state==='merged'?i.into:i.id,go=`<button type="button" class="link" data-learned-go="${id||''}" data-what="${i.what}">Saved to what I’ve learned</button>`;
 return `<div class="chat-event chat-learned"><span class="learned-acts">${go}${i.state==='saved'?`${sep}<button type="button" class="link" data-learned-edit="${i.id}" aria-label="Edit what was learned">Edit</button>${sep}<button type="button" class="link" data-learned-undo="${i.id}" aria-label="Undo: remove from what I’ve learned">Undo</button>`:''}</span>${q}</div>`}
// A reply that says it left a page open in the browser (a sign-in tab, a form)
const CHAT_TAB=/\b(?:tab|browser)\b[^.]*\b(?:open|opened|reopened|ready)\b|\b(?:open|opened|reopened)\b[^.]*\b(?:tab|browser)\b|\bis open for\b/i;
function chatLog(s=chatOpen()){if(!chat)return '<p class="chat-note">Loading…</p>';const p=s?chatParts(s):{},out=[];let day='',side='';
 const items=[...(chat.items||[])];
 // The card itself opens the conversation when no run has said anything yet: what it is about and what it needs
 if(s&&!items.some(i=>i.kind==='reply'))items.push({kind:'card',at:Date.parse(s.created_at)||0});
 // A coding agent's job that is still going or waits on you: its live block from the card, with its buttons
 const live=s?.agent_job&&p.agent?s.agent_job:null;if(live)items.push({kind:'agentlive',at:Date.parse(live.updated_at||live.started_at)||Date.now()});
 if(live)for(let n=items.length-1;n>=0;n--)if(items[n].kind==='agent'&&items[n].id===live.id){items.splice(n,1);break}  // its latest answer
 items.sort((a,b)=>(a.at||0)-(b.at||0));
 // The same tap again and again (five snoozes in a row) is one line with a count, unfolded for the times
 const rows=[];for(const i of items){const l=rows.at(-1);if(i.kind==='event'&&l?.kind==='event'&&l.text===i.text&&!!l.mine===!!i.mine)l.times.push(i.at),l.at=i.at;else rows.push(i.kind==='event'?{...i,times:[i.at]}:i)}
 const stamp=at=>{if(!at)return;const d=chatDayOf(at);if(d!==day){day=d;side='';out.push(`<div class="chat-day">${esc(d)}</div>`)}};
 const tm=at=>at?`<time class="chat-time" datetime="${new Date(at).toISOString()}" title="${esc(new Date(at).toLocaleDateString(DL,{weekday:'short',month:'short',day:'numeric',year:'numeric'})+' '+chatHM(at))}">${chatHM(at)}</time>`:'';
 const push=(i,html)=>{const sd=chatSide(i);out.push(html.replace('class="chat-','class="'+(sd===side?'cont ':'')+'chat-'));side=sd};
 const sent=new Set(items.filter(i=>i.kind==='event'&&i.sent).map(i=>i.sent.trim()));
 // Each send or cancel belongs to the latest draft before it (by its text for a send): only that one says Sent or Not sent
 const outcome=new Map();{const open=[];for(const i of items){if(i.kind==='reply')open.push(...(i.drafts||[]));if(i.kind!=='event')continue;
  const sent=i.sent?.trim(),d=sent?open.findLast(x=>!outcome.has(x)&&x.body.trim()===sent):/^(Send canceled|Didn’t go out)/.test(i.text||'')?open.findLast(x=>!outcome.has(x)):null;if(d)outcome.set(d,sent?'sent':'not')}}
 const drafts=items.flatMap(i=>i.kind==='reply'?(i.drafts||[]):[]),newest=drafts.at(-1);let prev=null;
 // The card's live send of a draft: the one with its text, else the newest when the card has one send
 const liveOf=d=>p.sends?.find(x=>typeof x.a.body==='string'&&x.a.body.trim()===d.body.trim())||(d===newest&&p.sends?.length===1?p.sends[0]:null);
 for(const d of drafts)if(liveOf(d)?.st.status==='sent')sent.add(d.body.trim());
 // The decision buttons go on the Machine's latest message when the card is waiting on one (a Send goes on its draft)
 const open=s&&!closed(s)&&s.status!=='snoozed'&&!chat.active&&!['queued','starting','running'].includes(s.preparation_status);
 const lastMachine=rows.findLastIndex(i=>i.kind==='reply'||i.kind==='card'||i.kind==='event'&&i.handoff);
 const tabAt=s&&!closed(s)&&s.browser_open?rows.findLastIndex(i=>i.kind==='reply'&&CHAT_TAB.test(i.text||'')):-1;
 // While a message goes out no other choice shows; they come back once it went or failed
 const options=(n,onDraft)=>open&&!p.going&&n===lastMachine&&p.options&&!(p.send&&onDraft)?`<div class="chat-options">${p.options}</div>`:'';
 const clamp=(k,html,long,more='More')=>long?`<div class="chat-clamp${chatOpenSet.has(k)?' open':''}">${html}</div><button type="button" class="link chat-more" data-unclamp="${k}">${chatOpenSet.has(k)?'Less':more}</button>`:html;
 // What the Machine or an agent made for the owner is a result: a reply with a draft or an outcome headline ("**Verf · prijsbenchmark klaar**"),
 // an agent's answer with files, or the card's own question while it waits on a call. The latest one is the raised card; earlier ones step back.
 const q=s&&!items.some(i=>i.kind==='reply')&&!p.ask?chatQuestion(s):{};
 const headline=t=>{const m=/^\s*\*\*([^*\n]+)\*\*[ \t]*(?:\n+|$)/.exec(String(t||''));return m?{title:m[1].trim(),rest:String(t).slice(m[0].length).trim()}:null};
 const copyAt=s&&s.status==='prepared'&&!p.send&&p.copy?rows.findLastIndex(i=>i.kind==='reply'):-1;
 const isResult=(i,n)=>i.kind==='reply'?!!((i.drafts||[]).length||headline(i.text)||n===copyAt):i.kind==='card'?!!(s&&!closed(s)&&!['asked','waiting for them'].includes(s.fleet_handoff?.stage)&&(p.ask||q.ask||s.status==='prepared'&&p.send)):false;
 // Raised only while it is open: a draft not sent yet, an outcome on a card still going, or the call the card waits on
 // A draft is open only while the card offers it to send: once a change is asked for, it is an earlier draft.
const isOpen=i=>!closed(s)&&(i.kind==='card'||!(i.drafts||[]).length||s.status==='prepared'&&i.drafts.some(d=>!sent.has(d.body.trim())));
 const last=rows.findLastIndex(isResult),current=last>=0&&isOpen(rows[last])?last:-1;
 const result=(n,i,inner,only)=>`<div class="chat-result ${n===current?'current':'earlier'}${only?' only-draft':''}">${inner}${tm(i.at)}</div>`;
 let lastTo='';
 rows.forEach((i,n)=>{stamp(i.at);const k=n+':'+i.kind,res=isResult(i,n),quiet=res&&n!==current;
  if(i.kind==='source'){const via=chatVia(i.via)+(i.note&&i.via?' note':''),who=[i.mine?'You':i.from,via].filter(Boolean).map(esc).join(' · ')||'Message';
   // Several messages in a row from the same person: their name (and the time) on the first; the link to the thread once, under the last
   const same=j=>j?.kind==='source'&&j.from===i.from&&j.mine===i.mine&&!!j.note===!!i.note&&chatDayOf(j.at)===chatDayOf(i.at),first=!same(rows[n-1]);
   const last=!(rows[n+1]?.kind==='source'&&!rows[n+1].mine&&chatDayOf(rows[n+1].at)===chatDayOf(i.at));
   const body=clamp(k,i.text?chatMarkdown(i.text):`<p>${esc(i.title)}</p>`,chatLong(i.text,i.note?2:3));
   push(i,`<div class="chat-msg ${i.mine?'you':'them'} chat-source${i.note?' note':''}">${first?`<div class="chat-from"><span><i class="via-ico via-${chatViaIcon(i.via,i.note)}" aria-hidden="true"></i>${who}</span>${tm(i.at)}</div>`:''}${i.files?chatAttHTML(i.files):''}<div class="bubble"><div class="say" translate="no">${body}</div>${last&&hasOriginal(s)&&!i.mine?`<button type="button" class="link read-original" data-id="${s.id}" data-original="read">Read the thread</button>`:''}</div>${first?'':tm(i.at)}</div>`)}
  else if(i.kind==='card'){const hasDraft=s.status==='prepared'&&p.send,intro=q.offer?chatMarkdown(q.body):p.intro;
   push(i,`<div class="chat-msg machine chat-card"><div class="bubble">${intro||`<p translate="no">${esc(s.title)}</p>`}</div>${res?'':options(n,hasDraft)+(hasDraft?`<div class="chat-card-send">${p.lead}</div>`:'')+tm(i.at)}</div>`);
   if(res)push(i,result(n,i,`${p.ask?`<div class="chat-ask">${p.ask}</div>`:q.ask?`<p class="chat-q chat-result-title" translate="no">${esc(q.ask)}</p>`:`<p class="chat-result-title" translate="no">${esc(s.title)}</p>`}${options(n,hasDraft)}${hasDraft?`<div class="chat-card-send">${p.lead}</div>`:''}`))}
  else if(i.kind==='agentlive')push(i,`<div class="chat-msg machine chat-agent">${p.agent}</div>`);
  else if(i.kind==='agent'){const all=i.files||[],pick=agentPick(all,i.full||i.text),files=pick.shown.map(f=>agentFile({id:i.id},{path:f})).join('')+agentMoreFiles(pick.hidden),
    allFiles=pick.hidden?`<details class="agent-more chat-allfiles"><summary>All files</summary>${agentAllFiles({id:i.id},all,false)}</details>`:'';
   // A shortened answer (its housekeeping left out) has More too, which shows the whole answer
   const whole=i.full&&chatOpenSet.has(k)?i.full:i.text,text=clamp(k,chatMarkdown(whole),chatLong(i.text)||!!i.full);
   // Plain text like any reply: whose answer it is, small above; its files and "<agent> sent nothing" on one line under it
   // (left out once the owner sent the card's message after it)
   const nothing=i.nothing_sent&&!rows.slice(n+1).some(j=>j.kind==='event'&&j.sent)?`<small class="chat-noted">${esc(i.name)} sent nothing</small>`:'';
   push(i,`<div class="chat-msg machine chat-agent-msg"><div class="chat-agent-name">${esc(i.name)}</div><div class="bubble" translate="no">${text}</div>${files||nothing?`<div class="chat-files">${files}${nothing}</div>`:''}${allFiles}${tm(i.at)}</div>`)}
  else if(i.kind==='steps')push(i,`<div class="chat-work">${chatFold(k,'chat-steps',`Checked ${i.steps.length} thing${i.steps.length===1?'':'s'}`,`<ol>${i.steps.map(t=>`<li>${esc(t)}</li>`).join('')}</ol>`)}</div>`);
  else if(i.kind==='event'){const c=i.times.length,t=chatEventText(i),line=(c>1?`${esc(t)} ${c} times<span class="chev" aria-hidden="true">›</span>`:esc(t))+(i.voice&&c===1?` · <a class="learn-link" href="#settings/writing" data-voice-edit="${esc(i.voice)}">Edit</a>`:'')+(i.undo_voice&&s&&i.undo_until>Date.now()?chatUndoVoice(s,i):'');
   // A handoff that didn't go out: Try again opens the handoff form again, as it was sent
   const retry=i.retry_handoff&&s&&!closed(s)&&!s.fleet_handoff?` · <button type="button" class="link" data-fleet-handoff="${esc(s.id)}">Try again</button>`:'';
   push(i,`<div class="chat-event${i.mine?' mine':''}${i.retry_handoff?' failed':''}">${c>1?chatFold(k+':'+i.times[0],'',line+tm(i.at),`<ol>${i.times.map(t=>`<li>${esc(chatDayOf(t))} ${chatHM(t)}</li>`).join('')}</ol>`):line+(i.handoff?`<span class="chat-when"> · ${chatHM(i.at)}</span>`:tm(i.at))+retry}</div>`);
   if(i.handoff&&n===lastMachine&&s&&withTeammate(s))push({kind:'event',mine:i.mine},`<div class="chat-event chat-handoff-wait">${esc(window.t('No answer from {} yet',String(s.fleet_handoff.name||window.t('your teammate')).split(' ')[0]))}</div>`);
   if(i.handoff&&n===lastMachine&&options(n,false))push({kind:'event',mine:false},`<div class="chat-msg machine chat-handoff-options">${options(n,false)}</div>`)}
  else if(i.kind==='learned')push(i,chatLearned(i));  // no time of its own: it sits under its reply, and beside a wide centered line it would stick out sideways
  else if(i.kind==='you'){const to=i.to||'',show=to&&to!==lastTo;lastTo=to;
   const att=chatAttHTML(i.files);
   push(i,`<div class="chat-msg you">${show?`<div class="chat-to">to ${esc(to)}</div>`:''}${att}${i.text?`<div class="bubble" translate="no">${chatMarkdown(i.text)}</div>`:''}${tm(i.at)}</div>`)}
  else if(i.kind==='reply'){const ds=i.drafts||[],h=headline(i.text);
   const tab=n===tabAt?`<a class="agent-file via-browser" href="${esc(state.browser_link||'#')}" target="_blank" rel="noopener" data-browser-show="${esc(s.id)}">View in Machine browser</a>`:'';
   // A reply cut off by Stop: a small Stopped right under what it said so far, before the card's choices
   const noted=(i.stopped?'<small class="chat-noted chat-stopped">Stopped</small>':'')+(i.noted?'<small class="chat-noted">Noted for next time</small>':'');
   // Without a headline the reply is plain text and its drafts are the result; with one, the headline and summary lead the result
   const fileOf=f=>`<button type="button" class="agent-file via-file" data-id="${esc(s.id)}" data-result="read" data-file="${esc(f.path)}" data-file-name="${esc(f.label)}">${esc(f.label)}<span aria-hidden="true"> ›</span></button>`;
   const copy=n===copyAt,files=(i.files||[]).filter(f=>!copy||f!==i.files[0]).map(fileOf).join('');
   const chips=tab||files?`<div class="chat-files">${tab}${files}</div>`:'';
   if(!res||!h)push(i,`<div class="chat-msg machine">${i.text||!i.stopped?`<div class="bubble" translate="no">${chatMarkdown(i.text)}</div>`:''}${chips}${noted}${ds.length||copy?'':options(n,false)}${res?'':tm(i.at)}</div>`);
   if(!res)return;
   if(copy){const f=(i.files||[])[0]||{label:'Draft',path:(s.result_files||[]).find(f=>!/\.pdf$/i.test(f.name))?.path},key=s.id+'|'+f.path,text=chatFiles.get(key),fk=k+':file';
    const df=draftFile(text),src=rows.findLast(x=>x.kind==='source'&&!x.mine&&x.via),where=src?chatVia(src.via)+(src.note?' note':''):'';
    const title=[df.name||f.label,where].filter(Boolean).join(' · ');
    const body=text==null?`<div data-preview="${esc(key)}"><p class="chat-note">Loading the draft…</p></div>`:df.body?`<div class="chat-draft-text chat-clamp${chatOpenSet.has(fk)?' open':''}">${chatMarkdown(df.body)}</div>${chatLong(df.body,4)?`<button type="button" class="link chat-more" data-unclamp="${fk}">${chatOpenSet.has(fk)?'Less':'Show all'}</button>`:''}`:'';
    push(i,result(n,i,`<div class="chat-result-head"><span class="chat-result-title">${esc(title)}</span><button type="button" class="link" data-id="${esc(s.id)}" data-result="read" data-file="${esc(f.path)}" data-file-name="${esc(f.label)}">Open</button></div>${body}<p class="chat-why">${COPY_WHY}</p>${options(n,false)}`));return}
   const parts=ds.map((d,m)=>{const dk=k+':d'+m,ls=liveOf(d),liveSent=ls?.st.status==='sent',went=outcome.get(d)==='sent'||liveSent,last=d===newest&&!went&&s?.status==='prepared',not=!last&&outcome.get(d)==='not';
    const before=prev&&prev.kind===d.kind&&!sent.has(prev.body.trim())&&prev.body!==d.body?chatDiff(prev.body,d.body):null;prev=d;
    const to=d.to.length?' to '+d.to.join(', '):'',what=d.reply?'Reply':d.kind==='email'||d.kind==='email_demo'?'Email':d.kind==='whatsapp'?'WhatsApp':d.kind==='telegram'?'Telegram':'Message';
    const links=[chatLong(d.body,quiet?2:4)?`<button type="button" class="link" data-unclamp="${dk}">${chatOpenSet.has(dk)?'Less':'Show all'}</button>`:'',before?`<button type="button" class="link" data-unclamp="${dk}:diff">${chatOpenSet.has(dk+':diff')?'Hide changes':'Show what changed'}</button>`:''].filter(Boolean).join('');
    return `<div class="chat-draft${went||not?' went':''}${last?' current':''}"><div class="chat-draft-head"><span>${what}${esc(to)}</span>${went?(liveSent?'':'<span class="went-tag">Sent</span>'):not?'<span class="went-tag not">Not sent</span>':last||!quiet?'':'<span>Earlier draft</span>'}</div>${d.subject&&!d.reply?`<div class="chat-draft-subject">${esc(d.subject)}</div>`:''}<div class="chat-clamp${chatOpenSet.has(dk)?' open':''}${d.kind==='email'||d.kind==='email_demo'?' mail-text':''}">${d.kind==='email'||d.kind==='email_demo'?mailHtml(d.body):chatMarkdown(d.body)}</div>
     ${before&&chatOpenSet.has(dk+':diff')?`<div class="chat-diff">${before}</div>`:''}${ls&&(last||liveSent)?chatSendLine(d,ls):''}${links||last&&p.send?`<div class="chat-draft-foot"><span>${links}</span>${last&&p.send?p.lead:''}</div>`:''}</div>`}).join('');
   const head=h?`<div class="chat-result-head"><span class="chat-result-title" translate="no">${format(h.title)}</span></div>${h.rest?`<div class="bubble" translate="no">${clamp(k,chatMarkdown(h.rest),quiet&&chatLong(h.rest,2))}</div>`:''}${chips}${noted}`:'';
   push(i,result(n,i,head+parts+(ds.length?options(n,true):h?options(n,false):''),!h&&ds.length===1))}});
 // A result with files: its links under the last reply
 if(p.links&&!drafts.length&&s?.status==='prepared'&&!p.copy)out.push(`<div class="chat-links">${p.links}</div>`);
 if(s)out.push(outboxChat(s));
 if(chat.active)out.push(chat.live?.text?`<div class="chat-msg machine chat-live"><div class="bubble" translate="no">${chatMarkdown(chat.live.text)}</div></div>`:'<div class="chat-msg machine chat-live"><div class="bubble typing" role="status" aria-label="Working"><i></i><i></i><i></i></div></div>');
 // The run's side of the chat couldn't be read (the Gateway was slow or away) and nothing of it was loaded before:
 // said once the run is over, never as an aside under the typing dots; the next ask (a few seconds) tries again.
 if(chat.unavailable&&!chat.active)out.push('<p class="chat-note">I couldn’t load my replies just now. Trying again…</p>');
 return out.join('')}
// At most two things to say, from what the card holds; tapping one fills the message box.
// Quick picks only from next steps the card itself proposes; cards don't carry any yet, so there are none (no templated lines).
function chatSuggestions(s){return []}
const chatPicks=s=>chatSuggestions(s).map(t=>`<button type="button" class="chat-say" data-chat-say="${esc(t)}">${esc(t)}</button>`).join('');
// Suggestions show while nothing has been said yet, or while you are writing
const chatPicksShown=()=>!(chat?.items||[]).some(i=>i.kind==='you')||document.activeElement?.id==='chat-input';
const BACK='<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M15 5l-7 7 7 7"/></svg>';
const NC_PLUS='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>';
const SEND='<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 4.5l7 7-1.4 1.4-4.6-4.6V20h-2V8.3l-4.6 4.6L5 11.5z"/></svg>';
const DOTS='<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="5" cy="12" r="1.8" fill="currentColor"/><circle cx="12" cy="12" r="1.8" fill="currentColor"/><circle cx="19" cy="12" r="1.8" fill="currentColor"/></svg>';
const chatUntil=v=>{const d=new Date(v),days=(d-Date.now())/864e5;return (chatDayOf(v)==='Today'?'today':days<6&&days>-1?d.toLocaleDateString(DL,{weekday:'short'}):d.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'}))+' '+chatHM(v)};
// One small line over the message box: where the card stands, with its one way back (Unsnooze, Reopen) as a text button
function chatStatus(s,p=chatParts(s)){const text=chat?.active?'Working on it…':s.status==='snoozed'?(s.snoozed_until?(s.handoff_wait?checkinLabel(s):'Snoozed until '+chatUntil(s.snoozed_until)):'Snoozed')
  :closed(s)?(s.status==='completed'?'Done':'Not needed'):s.preparation_status==='blocked'&&s.preparation_error==='stopped'?'':s.preparation_status==='blocked'?p.status||cardState(s):['queued','starting','running'].includes(s.preparation_status)||['accepted','instructions'].includes(s.status)?'Preparing':'';
 return text?`<span>${esc(text)}</span>${p.back&&!chat?.active?`<span aria-hidden="true">·</span>${p.back}`:''}`:''}
function chatView(s,groups){const p=chatParts(s);
 const side=`<aside class="chat-side" aria-label="Tasks"><div class="scope-filter" role="group" aria-label="Show">${[['all','All'],['work','Work'],['personal','Personal']].map(([v,t])=>`<button type="button" data-scope="${v}" aria-pressed="${scopeFilter===v}">${t}</button>`).join('')}</div>${groups.map(([items,title,key])=>{const cut=sideList(items,key);return cut.count?`<h3>${title}<span>${cut.count}</span></h3>${cut.list.map(x=>sideRow(x,s.id)).join('')}${cut.more?sideMoreRow(key):''}`:''}).join('')}</aside>`;
 return `<div class="chat-layout${chatDrawer?' drawer':''}" data-chat="${s.id}">${side}<div class="chat-main"><header class="chat-head"><a class="chat-back" href="#card=${s.id}" data-chat-back aria-label="Back to the to-do" title="Back to the to-do">${BACK}</a><h2 class="chat-title" title="${esc(s.title)}" translate="no">${esc(s.title)}</h2>
  <details class="chat-menu" id="chat-menu"><summary aria-label="More actions" title="More actions">${DOTS}</summary><div class="chat-menu-list" role="group" aria-label="More actions">${p.rest}<button type="button" class="ghost" data-chat-drawer aria-expanded="${chatDrawer}">All tasks</button></div></details></header>
 <article id="task-${s.id}" class="chat-panel">${p.panel}</article><div class="chat-log" id="chat-log" aria-live="polite">${chatLog(s)}</div>
 <div class="chat-compose"><div class="offline-bar chat-offline" id="chat-offline" role="status"${netShown()?'':' hidden'}>${netShown()?netHtml():''}</div><div class="chat-sheet" id="chat-sheet">${p.sheet}</div><div class="chat-status" id="chat-status">${chatStatus(s,p)}</div><div class="chat-picks" id="chat-picks"${chatPicksShown()?'':' hidden'}>${chatPicks(s)}</div><p class="chat-drop-hint">Drop to add to your message</p><p class="chat-file-error" id="chat-file-error" role="alert" hidden></p><div class="chat-tray" id="chat-tray"${chatPending.length?'':' hidden'}>${chatTrayHTML()}</div><div class="chat-box"><button type="button" class="chat-attach" data-chat-attach aria-label="Add files" title="Add files">${CLIP}</button><input type="file" id="chat-file" multiple hidden accept="${CHAT_ACCEPT}"><textarea id="chat-input" rows="1" aria-label="Message" placeholder="${esc(window.t('Ask or change something'))}" enterkeyhint="send"></textarea><div class="chat-tools"><span class="grow"></span>${micBtn()}${talkBtn()}<button type="button" class="chat-send chat-stop" data-chat-stop aria-label="Stop" title="Stop"${chat?.active?'':' hidden'}>${STOP}</button><button type="button" class="chat-send" data-chat-send aria-label="Send" title="Send"${chat?.active?' hidden':''} disabled>${SEND}</button></div></div><div class="chat-model" id="chat-model">${cmPill('chat')}</div></div></div></div>`}
function chatGrow(t){if(!t)return;t.style.height='34px';t.style.height=Math.min(160,Math.max(34,t.scrollHeight))+'px';chatSendState()}
// While a reply runs, Stop takes the place of Send until something is typed or added (sending then replaces the run).
function chatSendState(){const t=$('#chat-input'),b=$('[data-chat-send]'),x=$('[data-chat-stop]');if(!t||!b)return;
 const has=!!t.value.trim()||chatPending.length>0,ready=chatPending.every(f=>f.state==='ok'),stop=!!chat?.active&&!has;
 // With Talk live here, an empty box shows the wave where Send goes (as Send has nothing to send then)
 const w=$('.chat-compose [data-talk]'),talkHere=!!w&&talkOk();if(w)w.hidden=!talkHere||has||stop;
 b.disabled=!has||!ready;b.hidden=stop||talkHere&&!has;if(x){x.hidden=!stop;if(!stop)x.disabled=false}}
// Files the owner added (chat_files.py), on their message or on the to-do they made: images as pictures, the rest as chips
function chatAttHTML(fs){fs=fs||[];if(!fs.length)return '';const imgs=fs.filter(f=>/^image\//.test(f.type)),docs=fs.filter(f=>!/^image\//.test(f.type)),url=f=>'api/chat-file?id='+encodeURIComponent(f.id);
 return `<div class="chat-you-files">${imgs.map(f=>`<a class="chat-you-img" href="${url(f)}" target="_blank" rel="noopener" title="${esc(f.name)}"><img src="${url(f)}" alt="${esc(f.name)}" loading="lazy"></a>`).join('')}${docs.length?`<div class="chat-files">${docs.map(f=>`<a class="agent-file via-file" href="${url(f)}" target="_blank" rel="noopener" download="${esc(f.name)}">${esc(f.name)}</a>`).join('')}</div>`:''}</div>`}
// Files added to the next message (chat_files.py): from Add files, a paste or a drop, each uploaded at once and sent
// with the message. The same limits as the service's: they say so before anything uploads.
const CHAT_IMAGE=/\.(png|jpe?g|gif|webp)$/i,CHAT_EXT=/\.(png|jpe?g|gif|webp|pdf|txt|md|csv|tsv|json|log|rtf|eml|ics|docx|xlsx|pptx|odt|ods)$/i;
const CHAT_ACCEPT='image/png,image/jpeg,image/gif,image/webp,.pdf,.txt,.md,.csv,.tsv,.json,.log,.rtf,.eml,.ics,.docx,.xlsx,.pptx,.odt,.ods';
const CHAT_LIMIT={image:5*1048576,file:10*1048576,count:5};
const CLIP='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.5l-8.1 8.1a5 5 0 0 1-7.1-7.1l8.4-8.4a3.3 3.3 0 0 1 4.7 4.7l-8.4 8.4a1.7 1.7 0 0 1-2.4-2.4l7.8-7.8"/></svg>';
const STOP='<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="5" width="14" height="14" rx="2.5" fill="currentColor"/></svg>';
const FILE_ICO='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 2.8h8l4.2 4.2V21.2H6z M14 2.8V7h4.2"/></svg>';
let chatPending=[];
const chatSize=n=>n>=1048576?(n/1048576).toFixed(1)+' MB':Math.max(1,Math.round(n/1024))+' KB';
const chatTrayHTML=(list=chatPending,attr='att-remove')=>list.map(f=>{const img=f.type.startsWith('image/')&&f.url;return `<div class="chat-att${img?' img':''}${f.state==='up'?' up':''}" title="${esc(f.name)}">${img?`<img src="${f.url}" alt="${esc(f.name)}">`:`<span class="chat-att-ico">${FILE_ICO}</span>`}<span class="chat-att-name">${esc(f.name)}<small>${f.state==='up'?'Uploading…':chatSize(f.size)}</small></span><button type="button" class="chat-att-x" data-${attr}="${f.key}" aria-label="Remove ${esc(f.name)}" title="Remove">×</button></div>`}).join('');
function chatTray(){const t=$('#chat-tray');if(t){t.innerHTML=chatTrayHTML();t.hidden=!chatPending.length}chatSendState()}
function chatFileError(msg){const e=$('#chat-file-error');if(!e){if(msg)toast(msg,true);return}e.textContent=msg||'';e.hidden=!msg}
const chatDataUrl=f=>new Promise((ok,fail)=>{const r=new FileReader();r.onload=()=>ok(String(r.result));r.onerror=()=>fail(Error('That file couldn’t be read'));r.readAsDataURL(f)});
// A file's name (a pasted screenshot gets one) and why it can't go, before anything uploads (also New to-do's, ncAddFiles)
const chatFileName=f=>(f.name&&f.name!=='image.png'?f.name:'Pasted image.'+((f.type||'image/png').split('/')[1]||'png').replace('jpeg','jpg')).slice(0,120);
function chatFileProblem(f,name){const img=CHAT_IMAGE.test(name),limit=img?CHAT_LIMIT.image:CHAT_LIMIT.file;
 if(!CHAT_EXT.test(name))return t('I can’t read {}. Add an image, a PDF, a text or an Office file.',name);
 if(f.size>limit)return t(img?'{} is too big ({}). Images can be up to {}.':'{} is too big ({}). Files can be up to {}.',name,chatSize(f.size),chatSize(limit));
 if(!f.size)return t('{} is empty.',name);return ''}
function chatAddFiles(list){const s=chatOpen();if(!s)return;chatFileError('');const problems=[];
 for(const f of list){const name=chatFileName(f),img=CHAT_IMAGE.test(name);
  if(chatPending.length>=CHAT_LIMIT.count){problems.push(t('A message can carry up to {} files.',CHAT_LIMIT.count));break}
  const why=chatFileProblem(f,name);if(why){problems.push(why);continue}
  const item={key:crypto.randomUUID(),name,size:f.size,type:img?(f.type||'image/png'):(f.type||'file'),url:'',state:'up',sid:s.id};chatPending.push(item);
  (async()=>{try{const url=await chatDataUrl(f),data=url.split(',')[1]||'';if(img){item.url=url;chatTray()}const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf,'X-Upload':'chat-file'},body:JSON.stringify({action:'chat_upload',args:{suggestion_id:s.id,name,data}})});
    if(!chatPending.includes(item)){request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'chat_file_remove',args:{suggestion_id:s.id,id:r.id}})}).catch(()=>{});return}
    Object.assign(item,{id:r.id,name:r.name,type:r.type,state:'ok'})}
   catch(err){errCaught(err);chatPending=chatPending.filter(x=>x!==item);chatFileError(`${name}: ${err.message}`)}chatTray()})()}
 if(problems.length)chatFileError(problems.join(' '));chatTray();$('#chat-input')?.focus()}
function chatDropFiles(){chatPending=[]}
// Voice input (voice_input.py): the mic in a message box. Tap to talk and tap again to stop, or hold it while talking.
// The clip becomes 16 kHz mono WAV here and goes to the Machine, which writes it out (on the Machine itself, or with the
// owner's OpenAI key when they picked that in Settings). The text lands in the box to read and edit: nothing is sent. The
// clip stays only in this page's memory until its text is back. Never the browser's own speech recognition: in Chrome
// that sends the audio to Google, and Firefox has none.
const MIC='<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="3" width="6" height="11.5" rx="3"/><path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3"/></svg>';
const CHECK='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
const MIC_MAX=120,MIC_HOLD=600;
const micBtn=()=>`<button type="button" class="chat-mic" data-mic aria-label="Talk" title="Talk">${MIC}</button>`;
let mic=null,micPrepped=false,micDemo=false,micUse='';  // the one recording at a time; whether this page asked the Machine; the site's demo (it answers {demo:true}); what a tap does now (voice_view's use)
const MIC_DEMO='Voice input works on your own Machine. This demo can’t listen.';
const micOk=()=>!!(window.isSecureContext&&navigator.mediaDevices?.getUserMedia&&window.MediaRecorder&&window.OfflineAudioContext);
const micClock=s=>`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
const micPost=(action,args={},upload=false)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf,...(upload?{'X-Upload':'voice'}:{})},body:JSON.stringify({action,args})});
// The first tap gets the Machine's own engine ready while the owner talks (a download the first time only).
// What a tap does is asked once: OpenAI or this Machine; on Automatic while this Machine's own isn't ready yet, the
// browser's own speech recognition (it never waits on a download); with On this Machine picked, the recording waits.
// Each tap also has the Machine load the engine in use (warm) while the owner talks, so Done doesn't wait for it.
async function micPrep(){if(micPrepped){micPost('voice_status',{warm:true}).then(s=>{if(s.use)micUse=s.use}).catch(()=>{});return}
 micPrepped=true;try{const s=await micPost('voice_status',{warm:true});if(s.demo)micDemo=true;micUse=s.use||''}catch{micPrepped=false}}
const micSR=()=>window.SpeechRecognition||window.webkitSpeechRecognition;
const MIC_BCP={de:'de-DE',en:'en-US',es:'es-ES',fr:'fr-FR',it:'it-IT',nl:'nl-NL',pt:'pt-BR'};
// The browser's own speech recognition, while this Machine's own engine isn't ready: what it hears is kept as it goes
function micBrowser(v){const SR=micSR(),sr=new SR(),code=(state.dictation?.language||document.documentElement.lang||'en').slice(0,2);
 Object.assign(sr,{lang:MIC_BCP[code]||'en-US',continuous:true,interimResults:true});v.sr=sr;v.heard=[];v.interim='';v.browser=true;
 sr.onresult=e=>{let now='';for(let i=e.resultIndex;i<e.results.length;i++){const r=e.results[i];if(r.isFinal)v.heard.push(r[0].transcript.trim());else now+=r[0].transcript}v.interim=now.trim()};
 sr.onerror=e=>{if(mic!==v||e.error==='no-speech'||e.error==='aborted')return;v.srFailed=e.error==='not-allowed'||e.error==='service-not-allowed'?'blocked':'other'};
 // Chrome stops after a pause: it goes on until Done, the cross or 2 minutes
 sr.onend=()=>{if(mic!==v)return;if(v.state==='rec'&&!v.srFailed){try{sr.start()}catch{}return}
  if(v.state==='work'){const text=[...v.heard,v.interim].filter(Boolean).join(' ');v.sr=null;
   if(!text&&v.srFailed){micFail(v,v.srFailed==='blocked'?t('The microphone is blocked. Allow it for this site in your browser’s settings.'):t('Your browser’s speech recognition didn’t answer. Try again.'));return}micDone(v,text)}}
 sr.start()}
function micPaint(v){if(!v.box.isConnected){const box=document.getElementById(v.input)?.closest('.chat-box,.mic-wrap');if(!box){micCancel();return}v.box=box}
 let bar=v.box.querySelector(':scope>.mic-bar');if(!bar){bar=document.createElement('div');bar.className='mic-bar';bar.setAttribute('role','status');v.box.append(bar)}v.box.classList.add('mic-on');
 const x=`<button type="button" class="mic-x" data-mic-cancel aria-label="Cancel" title="Cancel">×</button>`,rec=v.state==='rec'||v.state==='start';
 // Drawn once per state, so a button never changes under a finger; the clock, the level and the progress update in place
 const key=v.state+'|'+(v.error||'')+'|'+!!v.wav+'|'+!!v.capped;
 if(bar.dataset.k!==key){bar.dataset.k=key;bar.innerHTML=rec?`${x}<span class="mic-live"><i class="mic-dot" aria-hidden="true"></i><span class="mic-time">0:00</span><span class="mic-wave" aria-hidden="true">${'<i></i>'.repeat(v.levels.length)}</span><span class="mic-hint">${esc(t(v.state==='start'?'Starting the microphone…':v.browser?'Your browser writes this one down.':'Listening…'))}</span></span><button type="button" class="chat-send mic-done" data-mic-stop aria-label="Done" title="Done"${v.state==='start'?' disabled':''}>${CHECK}</button>`
  :v.state==='error'?`${x}<span class="mic-live mic-err">${esc(v.error)}</span>${v.wav?`<button type="button" class="mic-retry" data-mic-retry>${esc(t('Try again'))}</button>`:''}`
  :`${x}<span class="mic-live"><i class="mic-spin" aria-hidden="true"></i><span class="mic-hint"></span></span><span class="mic-prog" aria-hidden="true"${v.state==='prep'?'':' hidden'}><i></i></span>`}
 if(rec){const left=MIC_MAX-v.secs,near=v.state==='rec'&&left<=15,live=bar.querySelector('.mic-live');live.classList.toggle('near',near);
  bar.querySelector('.mic-time').textContent=near?t('{} left',micClock(Math.ceil(left))):micClock(v.secs);
  bar.querySelectorAll('.mic-wave i').forEach((el,i)=>{el.style.height=Math.round(3+v.levels[i]*19)+'px'});
  const heard=micHeard(v);if(heard&&v.state==='rec'){const h=bar.querySelector('.mic-hint');h.classList.add('mic-heard');h.textContent=micTail(heard,matchMedia('(max-width:420px)').matches?26:48)}}
 else if(v.state!=='error'){bar.querySelector('.mic-hint').textContent=v.state==='wait'?t('Kept until you’re back online.'):v.state==='prep'?(v.left!=null?(v.left<=1?t('Getting voice ready… about a minute left'):t('Getting voice ready… about {} minutes left',v.left)):v.pct!=null?t('Getting voice ready… {}%',v.pct):t('Getting voice ready… This takes a few minutes.')):v.capped?t('Stopped at 2 minutes. Writing it down…'):t('Writing it down…');
  const p=bar.querySelector('.mic-prog');p.hidden=v.state!=='prep';p.firstChild.style.width=(v.pct||0)+'%';p.classList.toggle('busy',v.pct==null)}}
function micClose(v){if(v.box){v.box.classList.remove('mic-on');v.box.querySelector(':scope>.mic-bar')?.remove()}if(mic===v)mic=null}
function micRelease(v){clearInterval(v.tick);v.tick=null;try{v.stream?.getTracks().forEach(x=>x.stop())}catch{}try{v.meter?.close()}catch{}v.meter=null}
function micCancel(){const v=mic;if(!v)return;mic=null;if(v.sr){try{v.sr.abort()}catch{}v.sr=null}if(v.rec){v.rec.onstop=null;try{if(v.rec.state!=='inactive')v.rec.stop()}catch{}}micRelease(v);micClose(v);document.getElementById(v.input)?.focus({preventScroll:true})}
function micFail(v,msg){v.state='error';v.error=msg;micRelease(v);micPaint(v)}
async function micStart(btn,down){if(mic)return;const box=btn.closest('.chat-box,.mic-wrap'),input=box?.querySelector('textarea');if(!input)return;
 const v=mic={box,input:input.id,state:'start',chunks:[],levels:Array(18).fill(0),secs:0,down};
 if(!micOk()){micFail(v,t('Voice input doesn’t work in this browser.'));return}
 if(micDemo){micFail(v,t(MIC_DEMO));return}
 micPaint(v);const prep=micPrep();
 let stream;try{stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,channelCount:1}})}
 catch(e){await prep;if(mic!==v)return;micFail(v,micDemo?t(MIC_DEMO):e?.name==='NotAllowedError'||e?.name==='SecurityError'?t('The microphone is blocked. Allow it for this site in your browser’s settings.')
  :e?.name==='NotFoundError'||e?.name==='OverconstrainedError'?t('No microphone found. Connect one and try again.'):t('The microphone couldn’t start. Try again.'));return}
 if(mic!==v){stream.getTracks().forEach(x=>x.stop());return}  // canceled while the browser asked
 await prep;if(mic!==v){stream.getTracks().forEach(x=>x.stop());return}
 if(micUse==='browser'&&micSR()){try{micBrowser(v)}catch{v.browser=false}
  if(v.browser){Object.assign(v,{stream,state:'rec',t0:Date.now()});micMeter(v,stream);v.tick=setInterval(()=>micTick(v),100);micPaint(v);return}}
 const type=['audio/webm;codecs=opus','audio/mp4','audio/webm','audio/ogg;codecs=opus'].find(x=>MediaRecorder.isTypeSupported?.(x))||'';
 let rec;try{rec=new MediaRecorder(stream,type?{mimeType:type,audioBitsPerSecond:32000}:{})}catch{micFail(v,t('The microphone couldn’t start. Try again.'));stream.getTracks().forEach(x=>x.stop());return}
 Object.assign(v,{stream,rec,state:'rec',t0:Date.now()});
 rec.ondataavailable=e=>{if(e.data?.size)v.chunks.push(e.data)};rec.onstop=()=>micStopped(v);rec.start(1000);
 micMeter(v,stream);if(micUse==='openai'||micUse==='local')micTap(v);v.tick=setInterval(()=>micTick(v),100);micPaint(v)}
// While the owner talks, what they said so far goes to the Machine at each pause (a part, at least MIC_PART.min seconds;
// at most MIC_PART.max without a pause), so after Done only the last few seconds are left to write down. What comes
// back shows in the bar as they talk. If a part fails, the whole clip goes as one, as it does without parts.
const MIC_PART={min:6,max:25,pause:0.7,quiet:0.012};
function micTap(v){const ac=v.meter;if(!ac?.createScriptProcessor)return;
 try{const src=ac.createMediaStreamSource(v.stream),node=ac.createScriptProcessor(4096,1,1);Object.assign(v,{tap:node,pcm:[],pcmLen:0,rate:ac.sampleRate,quiet:0,parts:[],sentTo:0});
  node.onaudioprocess=e=>{if(mic!==v||v.state!=='rec')return;const d=e.inputBuffer.getChannelData(0);v.pcm.push(new Float32Array(d));v.pcmLen+=d.length;
   let sum=0;for(let i=0;i<d.length;i++)sum+=d[i]*d[i];v.quiet=Math.sqrt(sum/d.length)>MIC_PART.quiet?0:v.quiet+d.length;
   const unsent=(v.pcmLen-v.sentTo)/v.rate;if(unsent>=MIC_PART.max||unsent>=MIC_PART.min&&v.quiet/v.rate>=MIC_PART.pause)micPart(v,v.pcmLen)};
  src.connect(node);node.connect(ac.destination)}catch{v.tap=null;v.parts=null}}
function micSlice(v,from,to){const out=new Float32Array(to-from);let at=0;for(const c of v.pcm){const a=Math.max(from-at,0),b=Math.min(to-at,c.length);if(b>a)out.set(c.subarray(a,b),at+a-from);at+=c.length;if(at>=to)break}return out}
function micPart(v,to){const from=v.sentTo,part={text:null};v.sentTo=to;v.parts.push(part);const n=v.parts.length;
 part.done=(async()=>{const wav=await micWavOf(micSlice(v,from,Math.max(to,from+Math.ceil(v.rate*0.35))),v.rate);  // a short last bit gets a little silence
  const r=await micPost('voice_transcribe',{data:micB64(wav),part:n,...(v.lang?{language:v.lang}:{})},true);
  if(r.pending||r.demo||typeof r.text!=='string')throw Error('whole');part.text=r.text;if(!v.lang&&r.language)v.lang=r.language})().catch(()=>{part.failed=true})}
// The end of what it heard, from a word's start, so the newest words show
const micTail=(text,n)=>text.length<=n?text:'…'+(text.slice(-n).match(/\s(\S.*)$/)?.[1]||text.slice(-n));
const micHeard=v=>(v.parts||[]).map(p=>p.text).filter(Boolean).join(' ');
function micMeter(v,stream){try{const ac=new (window.AudioContext||window.webkitAudioContext)(),an=ac.createAnalyser();an.fftSize=512;ac.createMediaStreamSource(stream).connect(an);v.meter=ac;v.analyser=an;v.wave=new Uint8Array(an.fftSize)}catch{}}
function micTick(v){if(mic!==v||v.state!=='rec')return;v.secs=(Date.now()-v.t0)/1000;
 if(v.analyser){v.analyser.getByteTimeDomainData(v.wave);let sum=0;for(const x of v.wave)sum+=((x-128)/128)**2;v.levels=[...v.levels.slice(1),Math.min(1,Math.sqrt(sum/v.wave.length)*4)]}
 if(v.secs>=MIC_MAX){v.capped=true;micStop();return}micPaint(v)}
function micStop(){const v=mic;if(!v||v.state!=='rec')return;v.state='work';micRelease(v);const tail=v.pcmLen-v.sentTo;if(v.parts?.length&&tail>0&&(tail/v.rate>=0.3||v.quiet<tail))micPart(v,v.pcmLen);if(v.sr){try{v.sr.stop()}catch{v.sr.onend?.()}micPaint(v);return}try{v.rec.stop()}catch{micStopped(v)}micPaint(v)}
async function micStopped(v){if(mic!==v)return;const blob=new Blob(v.chunks,{type:v.rec?.mimeType||'audio/webm'});v.chunks=[];
 if((Date.now()-v.t0)<500||!blob.size){micFail(v,t('That was too short. Talk a little longer.'));return}
 if(v.parts?.length){const parts=v.parts;v.parts=null;await Promise.all(parts.map(p=>p.done));if(mic!==v)return;
  if(parts.every(p=>!p.failed)){v.pcm=[];micDone(v,parts.map(p=>p.text).filter(Boolean).join(' '));return}}
 try{v.wav=await micWav(blob)}catch{if(mic===v)micFail(v,t('That recording couldn’t be read. Try again.'));return}micSend(v)}
// MediaRecorder's clip (WebM/Opus, or MP4/AAC on Safari) as 16 kHz mono 16-bit WAV, the one format the Machine takes
async function micWav(blob){const ac=new (window.AudioContext||window.webkitAudioContext)();
 try{return await micWav16(await ac.decodeAudioData(await blob.arrayBuffer()))}finally{try{ac.close()}catch{}}}
// A part: the samples the page heard, at the microphone's own rate
async function micWavOf(samples,rate){const buf=new AudioBuffer({length:Math.max(1,samples.length),numberOfChannels:1,sampleRate:rate});buf.copyToChannel(samples,0);return micWav16(buf)}
async function micWav16(buf){const off=new OfflineAudioContext(1,Math.max(1,Math.ceil(buf.duration*16000)),16000),src=off.createBufferSource();src.buffer=buf;src.connect(off.destination);src.start();
  const pcm=(await off.startRendering()).getChannelData(0),out=new DataView(new ArrayBuffer(44+pcm.length*2)),w=(o,s)=>[...s].forEach((c,i)=>out.setUint8(o+i,c.charCodeAt(0)));
  w(0,'RIFF');out.setUint32(4,36+pcm.length*2,true);w(8,'WAVE');w(12,'fmt ');out.setUint32(16,16,true);out.setUint16(20,1,true);out.setUint16(22,1,true);out.setUint32(24,16000,true);out.setUint32(28,32000,true);out.setUint16(32,2,true);out.setUint16(34,16,true);w(36,'data');out.setUint32(40,pcm.length*2,true);
  for(let i=0;i<pcm.length;i++){const s=Math.max(-1,Math.min(1,pcm[i]));out.setInt16(44+i*2,s<0?s*0x8000:s*0x7fff,true)}return out.buffer}
const micB64=buf=>{const u=new Uint8Array(buf);let s='';for(let i=0;i<u.length;i+=0x8000)s+=String.fromCharCode.apply(null,u.subarray(i,i+0x8000));return btoa(s)};
async function micSend(v){if(mic!==v)return;v.state='work';v.error='';micPaint(v);
 try{const r=await micPost('voice_transcribe',{data:micB64(v.wav)},true);if(mic!==v)return;
  if(r.demo){micDemo=true;micFail(v,t(MIC_DEMO));return}
  if(r.pending){await micReady(v,r.voice);if(mic===v)micSend(v);return}
  micDone(v,r.text||'')}
 catch(err){errCaught(err);if(mic!==v)return;
  // Offline: the clip waits here with the offline bar, and goes when the Machine answers again (or on its Try now)
  if(err.offline){netSet(true,err.restarting);v.state='wait';micPaint(v);return}
  v.state='error';v.error=err.message;micPaint(v)}}
// The Machine is back (or Try now was tapped): a clip that waited goes now. Safe to call before this part of the page has run.
function micResume(){try{if(mic?.state==='wait')micSend(mic)}catch{}}
// The Machine's own engine is getting ready (the first time only): its progress, then the clip goes again
async function micReady(v,s){for(;;){if(mic!==v)return;const l=s?.local||{};
  if(l.state==='ready')return;if(l.state==='failed')throw Error(l.error||t('Getting voice ready failed. Try again later.'));
  if(l.state==='missing')await micPost('voice_prepare');
  v.state='prep';v.pct=l.step==='model'&&l.total?Math.min(99,Math.round(100*l.done/l.total)):null;
  // Minutes left from the download's own pace (once it has gone a few seconds), plus about a minute to start it
  if(l.step==='model'&&l.total){const now=Date.now();v.seen=v.seen||{at:now,done:l.done};const secs=(now-v.seen.at)/1000,rate=secs>=4?(l.done-v.seen.done)/secs:0;
   v.left=rate>0?Math.max(1,Math.ceil(((l.total-l.done)/rate+60)/60)):null}else v.left=null;micPaint(v);
  await new Promise(r=>setTimeout(r,1500));s=await micPost('voice_status')}}
function micDone(v,text){const input=document.getElementById(v.input);micClose(v);if(!input)return;text=text.trim();
 if(!text){toast(t('I didn’t catch anything. Try again.'),true);return}
 const a=input.selectionStart??input.value.length,b=input.selectionEnd??a,before=input.value.slice(0,a),after=input.value.slice(b),gap=before&&!/\s$/.test(before)?' ':'',room=input.maxLength>0?input.maxLength-before.length-after.length-gap.length:text.length;
 const put=text.slice(0,Math.max(0,room));input.value=before+gap+put+(after&&!/^\s/.test(after)?' ':'')+after;const at=(before+gap+put).length;
 try{input.setSelectionRange(at,at)}catch{}input.dispatchEvent(new Event('input',{bubbles:true}));if(matchMedia('(pointer:fine)').matches)input.focus({preventScroll:true})}
document.addEventListener('pointerdown',e=>{const b=e.target.closest('[data-mic]');if(!b||e.button>0||b.disabled)return;e.preventDefault();const at=Date.now();micStart(b,at);
 addEventListener('pointerup',()=>{const v=mic;if(v&&v.down===at&&v.state==='rec'&&Date.now()-at>=MIC_HOLD)micStop()},{once:true})});  // held: let go to stop
document.addEventListener('click',e=>{const b=e.target.closest('[data-mic],[data-mic-stop],[data-mic-cancel],[data-mic-retry]');if(!b)return;e.preventDefault();e.stopPropagation();
 if(b.hasAttribute('data-mic')){if(e.detail===0)micStart(b,0);return}  // pointerdown started it; a key press (Enter, Space) has no pointer
 if(b.hasAttribute('data-mic-stop'))micStop();else if(b.hasAttribute('data-mic-cancel'))micCancel();else if(mic?.wav)micSend(mic)},true);
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&mic){e.preventDefault();e.stopPropagation();micCancel()}},true);  // before a dialog closes on it
document.addEventListener('close',e=>{if(mic&&e.target.contains?.(mic.box))micCancel()},true);
// Talk live (talk_live.py): a spoken conversation with The Machine about the open to-do, with OpenAI's Realtime voice.
// The Machine starts the session (the OpenAI sign-in and the session's secret never come here) and hands on this page's
// WebRTC offer; the audio then goes directly between this page and OpenAI. The owner can talk over it (OpenAI stops
// and listens). The voice gets this page's tools: two that read, through the Machine, and `ask_chat`, which hands a
// request to the to-do's chat the way a typed message goes (decideOrWait), so the chat's own rules hold: it can change
// the draft or snooze, never send. Sending by voice: `ask_to_send` only works for the draft shown in this chat (on a
// phone or with the screen off the voice reads it out first) and gets the confirm question; `send_answer` lets the
// Machine judge the owner's next words itself. A clear yes approves that one draft, held a few seconds with Undo in the
// chat ("Approved by voice"). What both sides say goes into the chat. At most 10 minutes, with a warning a minute before.
const WAVE='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 10v4M8 7v10M12 4v16M16 7v10M20 10v4"/></svg>';
let talk=null,talkInfo={at:0,ready:null,busy:false},talkTodos=[];  // the one open conversation; whether this Machine can talk live (asked every 10 minutes); what Talk goes through
const talkOk=()=>talkInfo.ready===true&&!!(window.RTCPeerConnection&&navigator.mediaDevices?.getUserMedia);
const talkBtn=()=>`<button type="button" class="chat-mic chat-talk" data-talk aria-label="Talk live" title="Talk live"${talkOk()?'':' hidden'}>${WAVE}</button>`;
async function talkLoad(){if(talkInfo.busy||Date.now()-talkInfo.at<600000)return;talkInfo.busy=true;
 let later=false;try{const r=await micPost('talk_status');talkInfo.ready=r.demo?false:r.ready===true;later=!r.demo&&r.ready==null}catch{}finally{talkInfo.busy=false;talkInfo.at=later?0:Date.now()}
 if(later&&!talkInfo.retry)talkInfo.retry=setTimeout(()=>{talkInfo.retry=null;if(chatOpen())talkLoad()},3000);  // the Machine is still asking OpenClaw
 chatSendState();talkSide()}
// Talk in the sidebar (and the phone drawer): the main conversation, about whatever needs the owner
// Whether this Machine can talk live also comes with the page's status (talk_ready), so Talk shows without asking
function talkFromStatus(){if(typeof state.talk_ready==='boolean'&&talkInfo.ready!==state.talk_ready&&!talkInfo.busy){talkInfo.ready=state.talk_ready;talkSide()}}
// Talk in the sidebar, or T: starts the main conversation, or ends it while it's live (the same as End)
function talkMain(){const was=talk?.main,first=chatOpen()?.id||null;if(talk)talkEnd();if(was||!talkOk())return;talkLog=[];
 talkAfterDrawer(()=>{talkGoView();talkStart(true,first)})}
// The phone drawer closes with a step back in history: Talk's view goes on after that, or that step would undo it
function talkAfterDrawer(go){if(typeof drawerPopping!=='undefined'&&drawerPopping)addEventListener('popstate',()=>setTimeout(go),{once:true});else go()}
function talkSide(){const b=$('#side-talk');if(b){b.hidden=!talkOk()&&!talk?.main;b.setAttribute('aria-pressed',String(!!talk?.main));b.setAttribute('aria-current',talkViewOn()?'page':'false')}}
// Talk's own view (#talk): one transcript for the whole conversation, the to-do it is about now (with its draft: the one
// a spoken yes can send) and the bar. The voice opening a to-do changes that card, never the page the owner is on.
// Each to-do's chat still gets what was said about it, what was decided and what was sent.
let talkLog=[];  // this page's transcript of the main conversation: {role,text}, and {about,title} where the to-do changes
const talkViewOn=()=>!!$('#talk-view')&&!$('#talk-view').hidden;
let talkBack='inbox';
function talkGoView(){if(location.hash==='#talk')talkViewShow();else location.hash='#talk'}
function talkViewShow(){const sec=$('#talk-view');if(sec.hidden)talkBack=!$('#settings').hidden?'settings':document.querySelector('nav button.active')?.dataset.tab||'inbox';
 for(const x of document.querySelectorAll('main>section'))x.hidden=x!==sec;
 for(const b of document.querySelectorAll('nav button')){b.classList.remove('active');b.setAttribute('aria-current','false')}
 $('#open-settings')?.setAttribute('aria-current','false');talkViewPaint();talkPaint();talkSide();requestAnimationFrame(()=>scrollTo(0,document.documentElement.scrollHeight))}
function talkLeave(){if(!talkViewOn())return;if(talkBack==='settings')showSettings();else document.querySelector(`nav [data-tab="${talkBack}"]`)?.click()}
function talkDraftHtml(s){const a=s.status==='prepared'?(s.next_actions||[]).find(a=>a.revision&&['email','linkedin','slack','x','whatsapp','telegram','intercom','doc_reply'].includes(a.kind)&&a.body):null;if(!a)return '';
 const to=a.to_name||(Array.isArray(a.to)?a.to.join(', '):a.to||''),mail=a.kind==='email';
 return `<div class="chat-draft current"><span hidden data-smart="${esc(a.revision)}"></span>${to?`<div class="chat-draft-head"><span>${esc(t('To: {}',to))}</span></div>`:''}${a.subject&&!a.reply&&!/^re:/i.test(a.subject)?`<div class="chat-draft-subject">${esc(a.subject)}</div>`:''}<div class="chat-clamp${mail?' mail-text':''}">${mail?mailHtml(a.body):chatMarkdown(a.body)}</div></div>`}
function talkViewPaint(){const sec=$('#talk-view');if(!sec||sec.hidden)return;const v=talk,live=!!v?.main;
 if(!sec.firstElementChild)sec.innerHTML='<div class="talk-head"><h2></h2><span class="talk-again"></span></div><div class="talk-about-slot"></div><div class="chat-log talk-log" aria-live="polite"></div><div class="talk-foot"></div>';
 sec.querySelector('h2').textContent=t('Talk');
 const again=live||!talkOk()?'':`<button type="button" class="talk-again-btn" data-talk-main>${esc(t('Start again'))}</button>`,ag=sec.querySelector('.talk-again');if(ag.innerHTML!==again)ag.innerHTML=again;
 const s=live&&v.sid?state.suggestions?.find(x=>x.id===v.sid):null;
 const about=s?`<div class="talk-about" data-about="${esc(s.id)}"><div class="talk-about-top"><span>${esc(t('Talking about'))}</span><a href="#chat=${esc(s.id)}">${esc(t('Open the chat'))}</a></div><h3 translate="no">${esc(s.title)}</h3>${talkDraftHtml(s)}</div>`:'';
 const slot=sec.querySelector('.talk-about-slot');if(slot.dataset.k!==about){slot.dataset.k=about;slot.innerHTML=about}
 const log=sec.querySelector('.talk-log'),key=talkLog.length+'|'+live;if(log.dataset.k===key)return;log.dataset.k=key;
 log.innerHTML=talkLog.map(x=>x.record?talkRecordHtml(x.record):x.made?`<p class="talk-mark talk-made">${esc(t('Added a to-do: {}',x.title))}</p>`:x.about?`<p class="talk-mark" translate="no">${esc(x.title)}</p>`:`<div class="chat-msg ${x.role==='user'?'you':'machine'}"><div class="bubble" translate="no">${esc(x.text)}</div></div>`).join('')
  +(!talkLog.length||!live?`<p class="talk-mark">${esc(live?t('Say something to start.'):t('Talk ended.'))}</p>`:'');
 requestAnimationFrame(()=>scrollTo(0,document.documentElement.scrollHeight))}
addEventListener('hashchange',e=>{if(location.hash==='#talk'){if(talk?.main||talkLog.length)talkViewShow();else history.replaceState(null,'',location.pathname+location.search)}
 else if(/#talk$/.test(e.oldURL)&&!/^#chat=/.test(location.hash))talkLeave()});
// "Open the chat" stays in the page, also when the page's base is another path
$('#talk-view')?.addEventListener('click',e=>{const b=e.target.closest('[data-talk-event]');if(b){const title=b.textContent;if('meeting' in b.dataset)openMeeting(b.dataset.talkEvent,title);else openEvent(b.dataset.talkEvent,title);return}
 const a=e.target.closest('a[href^="#chat="]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey)return;e.preventDefault();chatGo(a.getAttribute('href').slice(6))});
if(location.hash==='#talk')history.replaceState(null,'',location.pathname+location.search);  // a reload: the conversation ended with the page
{const sec=document.getElementById('talk-view');if(sec)new MutationObserver(()=>{talkSide();if(!sec.hidden)return;if(location.hash==='#talk')history.replaceState(null,'',location.pathname+location.search);if(talk)talkPaint()}).observe(sec,{attributes:true,attributeFilter:['hidden']})}
// The bar sits above the chat's message box; Talk's own floats at the bottom of the page when no chat is open
function talkPaint(){const v=talk;if(!v)return;const box=v.main&&talkViewOn()?$('#talk-view .talk-foot'):document.querySelector('.chat-compose');
 if(!box&&!v.main){talkEnd();return}
 let host=box,bar=box?.querySelector(':scope>.talk');
 if(!box){host=$('#talk-dock');if(!host){host=document.createElement('div');host.id='talk-dock';document.body.append(host)}bar=host.querySelector('.talk')}
 document.querySelectorAll('.talk').forEach(x=>{if(x!==bar&&!x.closest('#settings'))x.remove()});if(box)$('#talk-dock')?.remove();
 if(!bar){bar=document.createElement('div');bar.className='talk';if(box)box.insertBefore(bar,box.querySelector('.chat-box'));else host.append(bar)}
 if(!box&&!host.dataset.ro){host.dataset.ro=1;new ResizeObserver(()=>document.body.style.setProperty('--talk-dock-h',host.offsetHeight+'px')).observe(host)}
 const key=v.state+'|'+v.muted+'|'+(v.error||'');
 if(bar.dataset.k!==key){bar.dataset.k=key;
  bar.innerHTML=v.state==='error'?`<div class="talk-bar talk-err" role="alert"><span class="grow">${esc(v.error)}</span><button type="button" class="talk-end" data-talk-close>${esc(t('Close'))}</button></div>`
   :`<div class="talk-bar" role="status"><span class="talk-live"><i class="talk-dot${v.state==='live'?'':' wait'}" aria-hidden="true"></i><strong>${esc(t(v.state==='live'?'Live':'Connecting…'))}</strong><span class="talk-time"></span></span><span class="talk-hint"></span>`
   +`<button type="button" class="talk-mute" data-talk-mute aria-pressed="${v.muted}"${v.state==='live'?'':' disabled'}>${esc(t(v.muted?'Unmute':'Mute'))}</button><button type="button" class="talk-end" data-talk-end>${esc(t('End'))}</button></div>`
   +(v.per_use?`<small class="talk-cost">${esc(t('OpenAI charges your API key per minute of talk.'))}</small>`:'')}
 if(v.state==='error')return;
 const left=v.limit-v.secs,near=v.state==='live'&&left<=v.limit-v.warn;
 bar.querySelector('.talk-time').textContent=near?t('{} left',micClock(Math.max(0,Math.ceil(left)))):v.state==='live'?micClock(v.secs):'';
 bar.querySelector('.talk-hint').textContent=v.muted?t('Muted'):v.state==='live'&&talkAsking(v)?t('Say yes to send it.'):'';
 bar.querySelector('.talk-live').classList.toggle('near',near)}
function talkFail(v,msg){if(talk!==v)return;talkClose(v);v.state='error';v.error=msg;talk=v;talkPaint()}
function talkClose(v){clearInterval(v.tick);v.closed=true;talkWake(v);talkMedia(v);try{v.dc?.close()}catch{}try{v.pc?.close()}catch{}try{v.stream?.getTracks().forEach(x=>x.stop())}catch{}
 if(v.audio){v.audio.srcObject=null;v.audio.remove()}if(v.id&&!v.ended){v.ended=true;micPost('talk_end',{id:v.id}).catch(()=>{})}}
let talkLimitToast='';  // the limit's toast is about that session only: cleared when another starts or ends
function talkToastClear(){const t=$('#toast');if(talkLimitToast&&t?.textContent===talkLimitToast)t.classList.remove('show');talkLimitToast=''}
function talkEnd(){const v=talk;if(!v)return;talk=null;talkToastClear();talkClose(v);document.querySelectorAll('.chat-compose>.talk,.talk-foot>.talk').forEach(x=>x.remove());$('#talk-dock')?.remove();document.body.style.removeProperty('--talk-dock-h');talkSide();talkViewPaint()}
async function talkStart(main,first=null){const s=main?null:chatOpen();if(talk||!main&&!s||main&&!talkOk())return;talkToastClear();micCancel();
 const v=talk={main:!!main,sid:s?.id||null,state:'start',muted:false,secs:0,limit:600,warn:540,per_use:false,said:new Set(),posting:Promise.resolve(),queue:[],relay:null,heard:{},responding:false,tell:[],known:new Set(talkNeeds().map(x=>x.id)),prep:new Set()};talkPaint();talkSide();talkViewPaint();
 try{v.stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,channelCount:1}})}
 catch(e){talkFail(v,e?.name==='NotAllowedError'||e?.name==='SecurityError'?t('The microphone is blocked. Allow it for this site in your browser’s settings.')
  :e?.name==='NotFoundError'||e?.name==='OverconstrainedError'?t('No microphone found. Connect one and try again.'):t('The microphone couldn’t start. Try again.'));return}
 if(talk!==v){v.stream.getTracks().forEach(x=>x.stop());return}
 try{const r=await micPost('talk_start',main?{main:true}:{suggestion_id:s.id});if(talk!==v){micPost('talk_end',{id:r.id}).catch(()=>{});return}
  Object.assign(v,{id:r.id,limit:r.limit||600,warn:r.warn||540,per_use:!!r.per_use,tools:r.tools||[],instructions:r.instructions||'',note:r.ask_note||'',notes:r.notes||{},voice:r.voice||'',speed:r.speed||0,turn:r.turn||null});talkPaint();
  if(v.main&&(first||chatOpen()))talkFocus(v,first||chatOpen().id);  // started from a to-do's chat: that one first
  const pc=v.pc=new RTCPeerConnection();v.audio=document.createElement('audio');v.audio.autoplay=true;v.audio.hidden=true;document.body.append(v.audio);
  pc.ontrack=e=>{v.audio.srcObject=e.streams[0];v.audio.play?.().catch(()=>{})};pc.addTrack(v.stream.getAudioTracks()[0],v.stream);
  pc.onconnectionstatechange=()=>{if(talk===v&&['failed','disconnected'].includes(pc.connectionState))talkLost(v)};
  v.stream.getAudioTracks()[0]?.addEventListener('ended',()=>talkLost(v));  // iPhone stops the mic when the app leaves the screen
  const dc=v.dc=pc.createDataChannel('oai-events');dc.onopen=()=>talkReady(v);dc.onmessage=e=>talkEvent(v,e.data);
  const offer=await pc.createOffer();await pc.setLocalDescription(offer);
  const a=await micPost('talk_offer',{id:v.id,sdp:offer.sdp});if(talk!==v)return;await pc.setRemoteDescription({type:'answer',sdp:a.sdp})}
 catch(err){if(err.offline)netSet(true,err.restarting);talkFail(v,err.offline?t('Offline. Start it again when you’re back online.'):err.message||t('Talk live couldn’t start. Try again.'))}}
// The voice's own setup: this page's instructions and tools (never the Gateway's agent), and what the owner says written down
function talkReady(v){if(talk!==v)return;v.state='live';v.t0=Date.now();talkWake(v);talkMedia(v);
 v.dc.send(JSON.stringify({type:'session.update',session:{type:'realtime',instructions:v.instructions,tools:v.tools,tool_choice:'auto',audio:{input:{transcription:{model:'gpt-4o-mini-transcribe'},...(v.turn?{turn_detection:v.turn}:{})},output:{...(v.voice?{voice:v.voice}:{}),...(v.speed?{speed:v.speed}:{})}}}}));
 v.tick=setInterval(()=>talkTick(v),250);talkPaint()}
function talkTick(v){if(talk!==v)return;if(!v.main&&chatOpen()?.id!==v.sid){talkEnd();return}
 if(talkDue(v))return;
 if(v.relay&&!chat?.active&&Date.now()-v.relay.at>20000)talkTurnDone();  // a turn that ended between two looks
 if(v.main)talkNew(v);
 talkPaint()}
// What has to happen at a moment, from the clock (wall time since it went live), not from counting ticks: timers
// slow down in the background, so this also runs on the voice's events and when the page shows again (talkTick is
// the backstop). end_talk ends once its goodbye has been heard; the limit ends it; a waiting note goes when it can.
function talkDue(v,flush=true){if(talk!==v||v.state!=='live')return false;v.secs=(Date.now()-v.t0)/1000;
 if(v.ending&&(Date.now()-v.ending>10000||!v.playing&&!v.responding&&(v.byeHeard||Date.now()-v.ending>1500))){talkEnd();return true}
 if(v.secs>=v.limit){talkEnd();talkLimitToast=v.main?t('Talk ends after 30 minutes. Start it again to go on.'):t('Talk live ends after 10 minutes. Start it again to go on.');toast(talkLimitToast);return true}
 if(flush)talkTellNext(v);return false}
// The connection or the microphone went away. In the background (a phone's lock screen, an iPhone leaving the app)
// it ends cleanly and says so, with Start again; on screen it shows the error.
function talkLost(v){if(talk!==v||v.closed)return;if(document.hidden||v.hiddenAt){talkEnd();toast(t('Talk stopped while in the background.'))}
 else talkFail(v,t('Talk live lost its connection. Start it again to go on.'))}
// Keeps going in the background: the screen stays on while it is live (Wake Lock, taken again when the page shows),
// and the lock screen or notification shows it with Mute and End (Media Session). Where a browser has neither,
// nothing happens.
async function talkWake(v){const on=talk===v&&v.state==='live'&&!v.closed&&!document.hidden;
 if(!on){const w=v.wake;v.wake=null;try{await w?.release()}catch{}return}
 if(v.wake&&!v.wake.released||!navigator.wakeLock?.request)return;
 try{v.wake=await navigator.wakeLock.request('screen');if(talk!==v||v.closed){v.wake.release().catch(()=>{});v.wake=null}}catch{}}
function talkMedia(v){const m=navigator.mediaSession;if(!m)return;const on=talk===v&&v.state==='live'&&!v.closed;
 const handle=(name,fn)=>{try{m.setActionHandler(name,on?fn:null)}catch{}};
 try{m.metadata=on&&typeof MediaMetadata==='function'?new MediaMetadata({title:t('Talk'),artist:'The Machine',artwork:[{src:new URL('brand/app-icon-192.png',document.baseURI).href,sizes:'192x192',type:'image/png'}]}):null}catch{}
 handle('pause',()=>talkMute(v,true));handle('play',()=>talkMute(v,false));handle('stop',()=>talkEnd());handle('hangup',()=>talkEnd());
 handle('togglemicrophone',()=>talkMute(v,!v.muted));
 try{m.playbackState=on?v.muted?'paused':'playing':'none'}catch{}
 try{if(on)m.setMicrophoneActive?.(!v.muted)}catch{}}
document.addEventListener('visibilitychange',()=>{const v=talk;if(!v)return;
 if(document.hidden){v.hiddenAt=Date.now();return}
 v.hiddenAt=0;if(v.state!=='live')return;
 // Back on screen: is it still there? A connection or microphone that went away while hidden ends cleanly.
 const mic=v.stream?.getAudioTracks()[0];
 if(['failed','closed','disconnected'].includes(v.pc?.connectionState)||v.dc&&v.dc.readyState!=='open'||mic?.readyState==='ended'){v.hiddenAt=1;talkLost(v);return}
 if(!talkDue(v)){talkWake(v);talkPaint()}});
// Talk works on the to-do on screen: the one the voice opens, or the one the owner opens. A send question about another is dropped.
function talkFocus(v,id){if(talk!==v||v.sid===id)return v.focusing;v.sid=id;v.asked=null;v.askedAt=0;v.queue=[];v.relay=null;
 if(v.main){talkLog.push({about:id,title:String(state.suggestions?.find(x=>x.id===id)?.title||'').slice(0,200)});talkViewPaint()}
 return v.focusing=micPost('talk_focus',{id:v.id,suggestion_id:id}).catch(()=>{})}
// Every open to-do, in the order the dashboard shows them, each with its state in plain words (talk_live.STATES):
// what needs the owner (Ready, To decide) first. At most 30; counts has them all.
const talkWho=s=>String((s.people||[])[0]?.name||'').slice(0,80);
const TALK_STATE={ready:'ready',needs:'to decide',preparing:'preparing',waiting:'waiting on others',later:'snoozed',lookdone:'looks done'};
const talkNeeds=()=>talkTodos.filter(([,l])=>l==='ready'||l==='needs').map(([s])=>s);
function talkList(){const counts={};for(const [,l] of talkTodos)counts[TALK_STATE[l]]=(counts[TALK_STATE[l]]||0)+1;
 return {todos:talkTodos.slice(0,30).map(([s,l])=>({id:s.id,state:TALK_STATE[l],title:String(s.title||'').slice(0,200),...(talkWho(s)?{from:talkWho(s)}:{})})),count:talkTodos.length,counts}}
async function talkOpen(v,id){if(!/^[a-f0-9]{16}$/.test(id))return {error:'No to-do with that id. Use list_todos or find_todos.'};  // a closed one too (Done / dismissed)
 const known=state.suggestions?.some(s=>s.id===id);
 if(!known)try{await micPost('talk_focus',{id:v.id,suggestion_id:id})}catch{return {error:'No to-do with that id. Use list_todos or find_todos.'}}
 if(chatOpen()&&chatOpen().id!==id)talkGoView();await talkFocus(v,id);
 try{const out=(await micPost('talk_tool',{id:v.id,name:'todo_details',args:{}})).output;
  const mark=talkLog.findLast(x=>x.about===id);if(mark&&!mark.title&&out?.title){mark.title=String(out.title).slice(0,200);const l=$('#talk-view .talk-log');if(l)l.dataset.k='';talkViewPaint()}  // one the page hasn't loaded
  return out}catch(err){return {error:err.message}}}
// A new to-do, by voice: the same as New to-do (card_new, Work or Personal as the list shows), never sent anywhere.
// The voice stays on the to-do in focus; the transcript gets a mark, and it isn't announced as new.
async function talkCreate(v,args){const title=String(args.title||'').replace(/\s+/g,' ').trim().slice(0,200),note=String(args.note||'').trim().slice(0,1500);
 if(!title)return {error:'Say what the to-do is.'};
 try{const made=await micPost('card_new',{text:title+(note?'\n'+note:''),scope:scopeFilter==='work'||scopeFilter==='personal'?scopeFilter:null,due:null,due_at:null,about:[],attach:[]});
  v.known.add(made.id);if(talk===v&&v.main){talkLog.push({made:made.id,title});talkViewPaint()}refresh().catch(()=>{});
  return {ok:true,id:made.id,title,note:'Added to their list. Say so in a few words. The to-do in focus is still the same.'}}
 catch(err){return {error:err.message||'Couldn’t add the to-do.'}}}
// A to-do's own buttons, by voice (todo_action): the same decide and card_rename actions the card and the Done /
// dismissed list use, offered only where the page offers them. Never a send.
async function talkDo(v,args){const id=String(args.id||v.sid||''),act=String(args.action||''),s=state.suggestions?.find(x=>x.id===id);
 if(!/^[a-f0-9]{16}$/.test(id))return {error:'Say which to-do: open it first, or give its id.'};
 const say=(text,extra={})=>{refresh().catch(()=>{});return {ok:true,...extra,note:text}};
 const go=async(choice,extra={},feedback='')=>{const step={choice,feedback,decision_id:crypto.randomUUID(),...extra};
  return OUTBOX_CHOICES.includes(choice)?decideOrWait(id,[step],choice):decidePost(id,step)};
 const open=s&&!closed(s);
 try{
  if(act==='rename'){const title=String(args.title||'').replace(/\s+/g,' ').trim().slice(0,200);if(!title)return {error:'Say the new title.'};
   await micPost('card_rename',{suggestion_id:id,title,reset:false,decision_id:crypto.randomUUID()});return say('Renamed. Say so in a few words.',{title})}
  if(act==='reopen'){const undo=s?.undo_until&&Date.parse(s.undo_until)>Date.now();
   if(s&&!closed(s))return {error:'It is open already.'};
   if(s?.status==='rejected'&&!undo||!s&&args.dismissed)return {error:'It was dismissed too long ago to bring back. Offer to add it again with create_todo.'};
   if(s){await go(s.status==='completed'&&!(undo&&s.expired_at)?'reopen':'undo');return say('Reopened. Say so in a few words.')}
   try{await go('reopen')}catch{try{await go('undo')}catch{return {error:'It was dismissed too long ago to bring back. Offer to add it again with create_todo.'}}}
   return say('Reopened. Say so in a few words.')}
  if(!open)return {error:s?'It is closed. Reopen it first.':'No open to-do with that id. Use list_todos or find_todos.'};
  if(act==='mark_done'){await go('complete');return say('Marked done. Say so in a few words.')}
  if(act==='dismiss'){await go('reject',{},String(args.why||'').trim().slice(0,1000));return say('Dismissed. Say so in a few words.')}
  if(act==='snooze'){const until=String(args.snooze_until||''),when=until&&!isNaN(Date.parse(until))?{snoozed_until:new Date(until).toISOString()}:{snooze_option:['2h','tomorrow','3d','1w'].includes(args.snooze)?args.snooze:'tomorrow'};
   const r=await go('snooze',when);return say('Snoozed. Say so in a few words.',r?.snoozed_until?{until:r.snoozed_until}:{})}
  if(act==='unsnooze'){if(s.status!=='snoozed')return {error:'It isn’t snoozed.'};await go('accept');return say('Back on the list. Say so in a few words.')}
  if(act==='do_it'){if(s.status!=='pending')return {error:'It doesn’t wait for a decision.'};await go('accept');return say('The Machine will prepare it. Say so in a few words.')}
  if(act==='try_again'){if(s.preparation_status!=='blocked')return {error:'Nothing is stuck there.'};await go('retry');return say('Trying again. Say so in a few words.')}
  if(act==='not_done'){if(!looksDone(s))return {error:'It doesn’t look done.'};await go('not_done');return say('Back on the list. Say so in a few words.')}
  return {error:'Unknown action.'}}
 catch(err){refresh().catch(()=>{});return {error:err.message||'That didn’t work.'}}}
// How the Machine is doing, as Connections and Needs you show it (machine_status)
function talkStatus(){const rh=state.review_health||{};
 return {connections:(state.connectors||[]).slice(0,30).map(c=>{const h=connectorHealth(c);return {name:String(c.display_name||c.email||c.id).slice(0,80),source:service(c.service),state:String(h.text||'Connected').slice(0,120),...(h.tone==='orange'?{needs_owner:true}:{})}}),
  reviews:{on:state.reviews_on!==false,waiting:rh.pending||0,...(rh.last_completed?{last:rh.last_completed}:{})},
  needs_owner:[...document.querySelectorAll('#needs-you li>span')].map(x=>x.textContent.trim()).filter(Boolean).slice(0,8)}}
// Anything else, by voice (ask_machine): a new to-do the way New to-do makes one, with the request handed to its chat
// (talk_live.ASK_PREFIX: the chat's own rules, it never sends). Its turn is followed here; the answer goes to the voice.
async function talkMachine(v,req){
 try{const made=await micPost('card_new',{text:req,scope:scopeFilter==='work'||scopeFilter==='personal'?scopeFilter:null,due:null,due_at:null,about:[],attach:[]});v.known.add(made.id);
  if(talk===v){talkLog.push({made:made.id,title:req.split('\n')[0].slice(0,200)});talkViewPaint()}
  const r=await decideOrWait(made.id,[{choice:'other',feedback:req,decision_id:'chat-voice-'+crypto.randomUUID()}],'other');
  refresh().catch(()=>{});talkWatch(v,made.id);
  return {ok:true,waiting:!!r?.waiting,note:v.note}}
 catch(err){return {error:err.message||'Couldn’t add the to-do.'}}}
// Its answer is the chat's reply; a turn that ended without one, or never started in two minutes, says it stopped.
async function talkWatch(v,id){const at=Date.now();let busy=false;
 for(let n=0;n<400&&talk===v;n++){await new Promise(ok=>setTimeout(ok,1500));if(talk!==v)return;
  const r=await talkChatRead(id);if(!r||r.unavailable)continue;if(r.active){busy=true;continue}
  const said=talkReplies(r.items||[]).map(i=>String(i.text||'').trim()).filter(Boolean);
  if(said.length||busy||Date.now()-at>120000){talkTell(v,said.length?(v.notes.done||'{answer}').replace('{answer}',said.join(' ').slice(0,3000)):v.notes.stopped||'');refresh().catch(()=>{});return}}}
// A record the voice opened (open_record): a small card in the transcript, opening its own page or the meeting
const TALK_KIND={person:'Person',organization:'Organization',project:'Project',meeting:'Meeting',message:'Message',promise:'Promise'};
function talkRecordHtml(c){const title=esc(c.title||''),go=c.node?`<a href="${esc(graphHash(c.node))}">${title}</a>`:c.promise?`<a href="${esc(promiseHref({id:c.promise}))}">${title}</a>`
  :c.event?`<button type="button" class="talk-record-open" data-talk-event="${esc(String(c.event))}"${c.kind==='meeting'?' data-meeting':''}>${title}</button>`:title;
 return `<div class="talk-record"><span class="talk-record-kind">${esc(t(TALK_KIND[c.kind]||'Message'))}</span><strong translate="no">${go}</strong>${c.line?`<small translate="no">${esc(c.line)}</small>`:''}</div>`}
// A to-do that comes to need the owner while Talk is open (Ready or To decide): a short heads-up at the next pause
// (talkTellNext waits while either side talks), once. One that was preparing says it's ready now (notes.ready).
function talkNew(v){if(!v.dc||v.state!=='live')return;for(const [s,l] of talkTodos)if(l==='preparing')v.prep.add(s.id);
 for(const s of talkNeeds())if(!v.known.has(s.id)){v.known.add(s.id);const note=v.prep.has(s.id)&&v.notes.ready||v.notes.new||'{title}';
  talkTell(v,note.replace('{title}',String(s.title||'').slice(0,200)).replace('{from}',talkWho(s)||'unknown'))}}
// What the voice says is kept once its response is done, unless the owner talked over it (OpenAI stops it): a cut-off start
// ("The chat is on…") never lands in the chat.
async function talkEvent(v,data){if(talk!==v)return;let e;try{e=JSON.parse(data)}catch{return}
 if(e.type==='input_audio_buffer.speech_started')v.speaking=true;
 else if(e.type==='input_audio_buffer.speech_stopped'){v.speaking=false;setTimeout(()=>talkTellNext(v),1200)}
 else if(e.type==='conversation.item.input_audio_transcription.completed')talkLine(v,'user',e.transcript,e.item_id);
 else if(e.type==='response.created')v.responding=true;
 else if(e.type==='response.output_audio_transcript.done')(v.heard[e.response_id]||=[]).push([e.transcript,e.item_id]);
 else if(e.type==='response.done'){v.responding=false;const id=e.response?.id,said=v.heard[id]||[];delete v.heard[id];
  if(e.response?.status!=='cancelled')said.forEach(([text,item])=>talkLine(v,'assistant',text,item));talkTellNext(v)}
 else if(e.type==='output_audio_buffer.started')v.playing=true;
 else if(e.type==='output_audio_buffer.stopped'||e.type==='output_audio_buffer.cleared')v.playing=false;
 else if(e.type==='response.function_call_arguments.done')talkTool(v,e);
 if(v.ending&&e.type==='output_audio_buffer.stopped')v.byeHeard=true;
 talkDue(v,false)}  // every event of the voice's: the goodbye heard, the limit (a waiting note goes on response.done)
// What one side said goes into the chat as an ordinary message (and is kept by the Machine, talk_line)
function talkLine(v,role,text,item){text=String(text||'').trim();const key=role+':'+(item||text);if(!text||v.said.has(key))return;v.said.add(key);
 v.posting=Promise.all([v.posting,micPost('talk_line',{id:v.id,role,text}).catch(()=>{})]);  // kept before the Machine judges an answer
 if(v.main){talkLog.push({role,text});talkViewPaint()}
 if(chat&&chatOpen()?.id===v.sid){chat={...chat,items:[...(chat.items||[]),{kind:role==='user'?'you':'reply',text,via:'live',at:Date.now()}]};paintChat();chatToEnd()}}
async function talkTool(v,e){let args={},output;try{args=JSON.parse(e.arguments||'{}')}catch{}
 // The owner said they're done: it ends the way End does, once its goodbye has been heard (talkTick)
 if(e.name==='end_talk'){v.ending=Date.now();if(v.dc?.readyState==='open')v.dc.send(JSON.stringify({type:'conversation.item.create',item:{type:'function_call_output',call_id:e.call_id,output:JSON.stringify({ok:true})}}));return}
 if(e.name==='ask_chat'){const req=String(args.request||'').trim().slice(0,2000);output=req?await talkAsk(v,req):{error:'Say what to ask.'};if(output.ok)output.note=output.queued?v.notes.queued||v.note:v.note}
 else if(e.name==='list_todos'&&v.main)output=talkList();
 else if(e.name==='create_todo')output=await talkCreate(v,args);
 else if(e.name==='machine_status'&&v.main)output=talkStatus();
 else if(e.name==='todo_action'&&v.main)output=await talkDo(v,args);
 else if(e.name==='ask_machine'&&v.main){const req=String(args.request||'').trim().slice(0,2000);output=req?await talkMachine(v,req):{error:'Say what to ask.'}}
 else if(e.name==='open_todo'&&v.main)output=await talkOpen(v,String(args.id||''));
 else if(v.main&&!v.sid&&['ask_chat','ask_to_send','send_answer'].includes(e.name))output={error:'No to-do is open. Call open_todo first.'};
 else if(e.name==='ask_to_send')output=await talkAskSend(v,args);
 else if(e.name==='send_answer')output=await talkAnswer(v);
 else try{output=(await micPost('talk_tool',{id:v.id,name:e.name,args})).output}catch(err){output={error:err.message}}
 if(output?.card){const card=output.card;delete output.card;if(talk===v&&v.main){talkLog.push({record:card});talkViewPaint()}}  // open_record: shown in the transcript
 if(talk!==v||v.dc?.readyState!=='open')return;
 v.dc.send(JSON.stringify({type:'conversation.item.create',item:{type:'function_call_output',call_id:e.call_id,output:JSON.stringify(output)}}));
 v.dc.send(JSON.stringify({type:'response.create'}))}
// The draft the voice may ask to send: the current one in this chat, on screen (scrolled into view). On a phone or with
// the screen off, the owner may not see it, so the voice reads it out in full before the question.
const talkShown=v=>$('#send-dialog')?.open?null:chatOpen()?.id===v.sid?document.querySelector('#chat-log .chat-draft.current [data-smart]')
 :v.main&&v.sid&&talkViewOn()?document.querySelector(`#talk-view .talk-about[data-about="${CSS.escape(v.sid)}"] .chat-draft.current [data-smart]`):null;
// A send question is open: asked, not yet answered, and not too old
const talkAsking=v=>!!v.asked&&Date.now()-(v.askedAt||0)<180000;  // the Machine's question is open (talk_live.ASK_SECONDS)
// The voice reads the whole draft out, so the screen isn't needed (a phone in a pocket, another page). When this
// to-do's draft shows (Talk's card, its chat), that one is asked about; else the Machine picks it (its only one, or the
// number the voice gives). The Machine pins the revision; a changed draft is asked about again.
async function talkAskSend(v,args={}){const b=talkShown(v);b?.closest('.chat-draft')?.scrollIntoView({block:'nearest'});
 try{const r=await micPost('talk_ask_send',{id:v.id,...(b?{revision:b.dataset.smart}:{}),...(Number.isInteger(args.draft)?{draft:args.draft}:{})});if(r.question){v.asked=r.revision;v.askedAt=Date.now()}return r}
 catch(err){return {error:err.message}}}
// The owner answered: what was said is kept first, then the Machine judges it (its own record, not the voice's word).
// The answer can still be on its way from OpenAI, so it asks again for a few seconds.
async function talkAnswer(v){let r={status:'not_asked'};
 for(let i=0,tries=v.asked?8:1;i<tries&&talk===v;i++){
  await v.posting;try{r=await micPost('talk_send',{id:v.id})}catch(err){return {error:err.message}}
  if(!['no_answer','not_asked'].includes(r.status))break;await new Promise(ok=>setTimeout(ok,700))}
 if(r.status==='queued'){v.asked=null;await refresh();if(chatOpen()?.id===v.sid)chatPoll()}else if(r.status!=='no_answer'&&r.status!=='not_asked')v.asked=null;
 return r}
// What the voice asks the chat goes the way a typed message does (chatSubmit's decideOrWait, so it can wait offline
// too), as a hand-off (talk_live.RELAY_PREFIX): the chat doesn't show it as the owner's message (what they said is
// there already), and its drafts wait for their Approve. A request while the chat is still on one never stops it:
// it waits and goes when that turn ends. Then the chat's answer goes straight to the voice, which tells the owner.
async function talkAsk(v,req){const s=state.suggestions?.find(x=>x.id===v.sid);if(!s)return {error:'This to-do is gone.'};
 if(v.relay||chat?.active&&chatOpen()?.id===s.id){v.queue.push(req);return {ok:true,queued:true}}
 return talkRelay(v,s,[req])}
const talkReplies=(items=chat?.items||[])=>items.filter(i=>i.kind==='reply'&&i.via!=='live');
const talkChatRead=id=>micPost('card_chat',{suggestion_id:id}).catch(()=>null);
async function talkRelay(v,s,reqs){const here=chatOpen()?.id===s.id,seen=here?null:await talkChatRead(s.id);if(talk!==v||v.sid!==s.id)return {error:'This to-do is no longer open.'};
 const relay=v.relay={at:Date.now(),replies:talkReplies(here?undefined:seen?.items||[]).length,sid:s.id};
 const steps=[...(s.status==='completed'?[{choice:'reopen',feedback:'',decision_id:crypto.randomUUID()}]:[]),{choice:'other',feedback:reqs.join('\n'),decision_id:'chat-talk-'+crypto.randomUUID()}];
 try{const r=await decideOrWait(s.id,steps,'other');
  if(chatOpen()?.id===s.id){chat={...(chat||{}),active:!r?.waiting,cursor:null};changing.delete(s.id)}
  if(!r?.waiting){await refresh();if(chatOpen()?.id===s.id){paintChat();chatToEnd();chatPoll()}else talkFollow(v,relay)}
  return {ok:true,waiting:!!r?.waiting}}
 catch(err){v.relay=null;return {error:err.message}}}
// The chat's turn ended: its answer goes to the voice at once (no checking back), then what waited goes
// The chat isn't on screen (Talk's own view, another page): its turn is followed here, the way an open chat polls it
async function talkFollow(v,relay){let busy=false;
 for(let n=0;n<400&&talk===v&&v.relay===relay;n++){await new Promise(ok=>setTimeout(ok,1500));if(talk!==v||v.relay!==relay||chatOpen()?.id===relay.sid)return;  // an open chat takes over
  const r=await talkChatRead(relay.sid);if(!r||r.unavailable||talk!==v||v.relay!==relay)continue;if(r.active){busy=true;continue}
  if(busy||talkReplies(r.items||[]).length>relay.replies||Date.now()-relay.at>20000){refresh();talkTurnDone(r.items||[]);return}}}
function talkTurnDone(items){const v=talk;if(!v||talk.state!=='live')return;if(!items){if(chatOpen()?.id!==v.sid)return;items=chat?.items||[]}
 if(v.relay){const said=talkReplies(items).slice(v.relay.replies).map(i=>String(i.text||'').trim()).filter(Boolean).join(' ').slice(0,3000);v.relay=null;
  talkTell(v,said?(v.notes.done||'{answer}').replace('{answer}',said):v.notes.stopped||'')}
 if(v.queue.length){const s=state.suggestions?.find(x=>x.id===v.sid),reqs=v.queue;v.queue=[];if(s)talkRelay(v,s,reqs)}}
// A note for the voice, as a message it answers aloud; while it is talking, after that
function talkTell(v,text){if(!text)return;v.tell.push(text);talkTellNext(v)}
function talkTellNext(v){if(talk!==v||v.responding||v.speaking||!v.tell.length||v.dc?.readyState!=='open')return;const text=v.tell.shift();v.responding=true;
 v.dc.send(JSON.stringify({type:'conversation.item.create',item:{type:'message',role:'system',content:[{type:'input_text',text}]}}));
 v.dc.send(JSON.stringify({type:'response.create'}))}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-voice-undo]');if(!b)return;e.preventDefault();b.disabled=true;
 try{await micPost('talk_undo',{suggestion_id:b.dataset.sid,approval_id:b.dataset.voiceUndo});toast(t('Canceled. It won’t be sent.'))}catch(err){errCaught(err);toast(err.message,true)}
 await refresh();if(chatOpen())chatPoll()});
document.addEventListener('click',e=>{const b=e.target.closest('[data-talk],[data-talk-main],[data-talk-end],[data-talk-close],[data-talk-mute]');if(!b)return;e.preventDefault();
 if(b.hasAttribute('data-talk-main')){if(typeof drawerClose==='function')drawerClose();if(talk?.main&&!talkViewOn()&&b.id==='side-talk'){talkAfterDrawer(talkGoView);return}talkMain();return}  // live, from another page: back to Talk
 if(b.hasAttribute('data-talk')){if(talk)talkEnd();else talkStart();return}
 if(b.hasAttribute('data-talk-end')||b.hasAttribute('data-talk-close')){talkEnd();return}
 const v=talk;if(!v)return;
 if(b.hasAttribute('data-talk-mute'))talkMute(v,!v.muted)});
function talkMute(v,on){if(talk!==v||v.state!=='live')return;v.muted=on;v.stream?.getAudioTracks().forEach(x=>{x.enabled=!on});talkMedia(v);talkPaint()}
// On open: the latest at the bottom, nothing cut off under the header; a short chat just sits under the header.
// The thread scrolls in its own box (on a phone too, so the message box never moves); a page without that layout scrolls itself.
const chatScroller=()=>{const l=$('#chat-log');return l&&getComputedStyle(l).overflowY!=='visible'?l:null};
const chatToEnd=()=>{const l=chatScroller();if(l)l.scrollTop=l.scrollHeight;else scrollTo(0,document.documentElement.scrollHeight)};
function chatScrollStart(){const log=$('#chat-log');if(!log)return;if(chatScroller())return chatToEnd();scrollTo(0,document.documentElement.scrollHeight);
 // The first item under the header starts whole when only a little of it is hidden; otherwise it fades under the header.
 const head=$('.chat-head')?.getBoundingClientRect().bottom||0,cut=[...log.children].find(n=>{const b=n.getBoundingClientRect();return b.top<head-1&&b.bottom>head+1});
 if(cut&&head-cut.getBoundingClientRect().top<=12)scrollBy(0,-(head-cut.getBoundingClientRect().top))}
// Make el's children match html, replacing only the ones that changed (same position, same item), so expanded parts,
// hovers and the scroll position stay as they are.
function chatPatch(el,html){const t=document.createElement('template');t.innerHTML=html;const fresh=[...t.content.childNodes].filter(n=>n.nodeType===1||n.textContent.trim()),old=[...el.childNodes].filter(n=>n.nodeType===1||n.textContent.trim());
 fresh.forEach((n,i)=>{const o=old[i];if(!o)el.append(n);else if(!o.isEqualNode(n))o.replaceWith(n)});old.slice(fresh.length).forEach(n=>n.remove())}
// Around an update of the thread: at the end (within 40px) it stays at the end; otherwise the item in view stays where it is.
function chatKeepPlace(fn){const log=$('#chat-log');if(!log)return fn();const l=chatScroller(),end=chatEndNow(40);
 const top=l?l.getBoundingClientRect().top:($('.chat-head')?.getBoundingClientRect().bottom||0),kids=[...log.children];
 const at=kids.findIndex(n=>n.getBoundingClientRect().bottom>top+1),y=at>=0?kids[at].getBoundingClientRect().top:0,keep=l?.scrollTop;fn();
 if(end&&chat?.items?.length){chatToEnd();return}if(l)l.scrollTop=keep;const n=at>=0?$('#chat-log').children[at]:null;if(!n)return;
 const d=n.getBoundingClientRect().top-y;if(Math.abs(d)>.5){if(l)l.scrollTop+=d;else scrollBy(0,d)}}
// Long names fade out at the edge instead of wrapping; the full name is in their tooltip.
function chatFades(){document.querySelectorAll('.chat-side a,.chat-title,.side-cards a').forEach(n=>{const cut=n.scrollHeight>n.clientHeight+1;n.classList.toggle('fade',n.scrollWidth>n.clientWidth+1||cut);
 // A title cut after its second line ends where its last whole word does, often well before the edge: fade out there
 if(!cut||!n.firstChild||n.firstChild.nodeType!==3){n.style.removeProperty('--fade-x');return}
 const box=n.getBoundingClientRect(),r=document.createRange(),txt=n.firstChild;let lo=0,hi=txt.length;
 while(lo<hi){const m=(lo+hi+1)>>1;r.setStart(txt,m-1);r.setEnd(txt,m);const q=r.getBoundingClientRect();if(q.bottom<=box.bottom+1)lo=m;else hi=m-1}
 while(lo>1&&/\s/.test(txt.data[lo-1]))lo--;r.setStart(txt,Math.max(0,lo-1));r.setEnd(txt,lo);n.style.setProperty('--fade-x',Math.round(r.getBoundingClientRect().right-box.left)+'px')})}
addEventListener('resize',()=>chatFades());
// A scrolled box shows its thin thumb while it moves
// Fonts that arrive late change the widths: measure the fades again then
document.fonts?.ready.then(()=>requestAnimationFrame(chatFades));document.fonts?.addEventListener?.('loadingdone',()=>requestAnimationFrame(chatFades));
document.addEventListener('scroll',e=>{const b=e.target;if(!b.matches?.('.chat-log,.chat-side,.side-cards'))return;b.classList.add('scrolling');clearTimeout(b._scrolling);b._scrolling=setTimeout(()=>b.classList.remove('scrolling'),900)},{capture:true,passive:true});
// A result file shown in the thread (a copy-only draft): read once, then kept while the page is open
const chatFiles=new Map();
// A saved draft file as the card shows it: only the draft (the quoted text under its heading, unquoted), never the
// sources section after it; its name from its heading ("X: draft internal answer for Andrea" is "Internal answer for Andrea")
function draftFile(text){const lines=String(text||'').replace(/\r/g,'').split('\n');let head='';if(/^#\s/.test(lines[0]||''))head=lines.shift().replace(/^#\s+/,'').trim();
 const end=lines.findIndex(l=>/^#{1,6}\s/.test(l)),part=(end<0?lines:lines.slice(0,end));const quoted=part.filter(l=>/^\s*>/.test(l));
 const body=(quoted.length?quoted.map(l=>l.replace(/^\s*>\s?/,'')):part).join('\n').replace(/\n{3,}/g,'\n\n').trim();
 let name=head.includes(':')?head.slice(head.lastIndexOf(':')+1).trim():head;name=name.replace(/^(?:a\s+)?draft(?:ed)?\s+(?:of\s+)?/i,'');
 return {name:name?name[0].toUpperCase()+name.slice(1):'',body,sources:end>=0}}
async function chatPreviews(){for(const n of document.querySelectorAll('#chat-log [data-preview]')){const key=n.dataset.preview;if(chatFiles.has(key))continue;chatFiles.set(key,null);
 const [id,path]=key.split('|');try{const d=await request('api/result?id='+id+'&file='+encodeURIComponent(path));chatFiles.set(key,d.pdf?'':String(d.text||''))}catch{chatFiles.set(key,'')}paintChat()}}
// A refresh while the chat is open updates the thread, list and header in place and keeps the message box itself,
// so a field you are typing in never loses its focus, text or caret.
function chatMount(id,html){const box=$('#suggestions'),cur=box.querySelector(':scope>.chat-layout');
 if(!cur||cur.dataset.chat!==id||!cur.querySelector('#chat-input')){box.innerHTML=html;requestAnimationFrame(chatFades);return}
 const t=document.createElement('template');t.innerHTML=html;const nu=t.content.querySelector('.chat-layout');cur.className=nu.className;
 const swap=sel=>{const a=cur.querySelector(sel),b=nu.querySelector(sel);if(!a||!b||a.isEqualNode(b))return;a.replaceWith(b)};
 const side=cur.querySelector('.chat-side'),top=side?.scrollTop;if(side)chatPatch(side,nu.querySelector('.chat-side').innerHTML);if(side)side.scrollTop=top;
 swap('.chat-panel');chatKeepPlace(()=>chatPatch(cur.querySelector('#chat-log'),nu.querySelector('#chat-log').innerHTML));
 if(!cur.querySelector('#chat-menu')?.open)swap('.chat-head');swap('#chat-status');swap('#chat-picks');{const typing=document.activeElement?.matches('textarea,input[type=text]')&&cur.querySelector('#chat-sheet')?.contains(document.activeElement);if(!typing||!nu.querySelector('#chat-sheet')?.children.length)swap('#chat-sheet')}chatFades()}
// On a phone the chat column is exactly the visible part of the window (--vv-h, --vv-top): where the browser doesn't
// shrink the page for the on-screen keyboard (iOS Safari) that part shrinks and slides instead, and the message box
// rides on the keyboard; Android Chrome resizes the page itself (interactive-widget=resizes-content). Zoomed in with
// two fingers, the column keeps the window's size. Keep the latest message in view when you were at the end.
let chatAtEnd=false;
const chatEndNow=(gap=80)=>{const l=chatScroller();return l?l.scrollTop+l.clientHeight>=l.scrollHeight-gap:innerHeight+scrollY>=document.documentElement.scrollHeight-gap};
function chatKeyboard(){const v=window.visualViewport;if(!v)return;const kb=Math.max(0,Math.round(innerHeight-v.height-v.offsetTop)),typing=document.activeElement?.id==='chat-input',zoomed=Math.abs((v.scale||1)-1)>.01,r=document.documentElement.style;
 r.setProperty('--vv-h',(zoomed?innerHeight:v.height)+'px');r.setProperty('--vv-top',(zoomed?0:Math.max(0,v.offsetTop))+'px');document.body.classList.toggle('kb-open',typing&&(kb>0||innerHeight<screen.height*.6));
 if(typing&&chatAtEnd)requestAnimationFrame(chatToEnd)}
window.visualViewport?.addEventListener('resize',chatKeyboard);window.visualViewport?.addEventListener('scroll',chatKeyboard);addEventListener('resize',chatKeyboard);chatKeyboard();
function paintChat(){const log=$('#chat-log'),s=chatOpen();if(!log||!s)return;chatKeepPlace(()=>chatPatch(log,chatLog(s)));
 const st=$('#chat-status'),sh=chatStatus(s);if(st&&st.innerHTML!==sh)st.innerHTML=sh;const menu=$('#chat-menu');if(menu&&!menu.open)menu.querySelector('.chat-menu-list').innerHTML=chatParts(s).rest+`<button type="button" class="ghost" data-chat-drawer aria-expanded="${chatDrawer}">All tasks</button>`;
 const picks=$('#chat-picks');if(picks){const ph=chatPicks(s);if(picks.innerHTML!==ph)picks.innerHTML=ph;picks.hidden=!chatPicksShown()}
 chatSendState();chatFades();chatPreviews();cmPaint('chat')}
// The chat this device kept for the card: shown at once while the live one loads (that one replaces it in place)
async function chatKept(id){const hit=await localCache.read('chat:'+id);if(!hit||id!==chatId||chat&&!(chat.unavailable&&!chat.items?.length))return;chat={...hit.value,cursor:null,active:false};paintChat();requestAnimationFrame(chatScrollStart)}
async function chatPoll(){clearTimeout(chatTimer);const id=chatId;if(!id)return;
 if(!document.hidden&&!$('#inbox').hidden)try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'card_chat',args:{suggestion_id:id,...(chat?.cursor&&chat.items?{cursor:chat.cursor}:{})}})});
  if(id!==chatId)return;const was=chat?.active,first=!chat;
  // A read that failed while the chat was already on screen changes nothing but whether the run still goes: what was
  // shown stays (with the live answer), quietly, and the next ask catches up
  if(r.unavailable&&chat?.items?.length&&!chat.unavailable)chat={...chat,active:r.active,status:r.status,live:r.active?chat.live:null,stale:true};
  else{const keep=r.unchanged;chat={...r,items:keep?chat.items:r.items,cursor:(keep?chat.cursor:r.cursor)||null}}paintChat();if(!r.unchanged&&!r.unavailable)localCache.put('chat:'+id,{...chat,cursor:null});if(first){requestAnimationFrame(chatScrollStart);setTimeout(chatScrollStart,150)}if(was&&!r.active){refresh();talkTurnDone()}}catch(e){errCaught(e);if(id===chatId&&!chat){chat={items:[],unavailable:true};paintChat()}}
 if(id===chatId)chatTimer=setTimeout(chatPoll,chat?.active?1000:chat?.unavailable||chat?.stale?4000:10000)}
// Whether this page put the open chat on the history (so back can take it off again instead of adding an entry)
let chatPushed=false;
function openChatLink(){if(!state.suggestions||location.hash==='#browser')return;  // the browser pane over a chat keeps that chat for Back
const m=/^#chat=([a-f0-9]{16})$/.exec(location.hash),id=m&&state.suggestions.some(s=>s.id===m[1])?m[1]:null;
 if(id===chatId)return;const was=chatId;chatId=id;chat=null;if(talk?.main){if(id&&talk.sid!==id)talkFocus(talk,id)}else if(talk&&talk.sid!==id)talkEnd();if(id)talkLoad();chatDrawer=false;chatDropFiles();chatOpenSet.clear();clearTimeout(chatTimer);if(!id)chatPushed=false;
 if(id){document.querySelector('nav [data-tab="inbox"]').click();render();scrollTo(0,0);chatKept(id);chatDraftBack(id);chatPoll();if(kbKeyed()&&matchMedia('(pointer:fine)').matches)$('#chat-input')?.focus({preventScroll:true})}else{render();const c=was&&document.getElementById('task-'+was);if(c){for(let d=c.parentElement;d;d=d.parentElement)if(d.tagName==='DETAILS')d.open=true;c.scrollIntoView({block:'center'});const a=document.activeElement;if(!a||a===document.body||!a.isConnected)kbFocus(c)}}}
// A chat opens only on a real tap: not on the tap that stops a fling, nor on one that ends a scroll or a drag.
let chatScrolledAt=0,chatDown=null;
addEventListener('scroll',()=>{chatScrolledAt=Date.now()},{passive:true});
document.addEventListener('pointerdown',e=>{chatDown={x:e.clientX,y:e.clientY,at:Date.now(),scrolled:Date.now()-chatScrolledAt<250}},{passive:true,capture:true});
const chatRealTap=e=>!(chatDown&&(chatDown.scrolled||Math.hypot(e.clientX-chatDown.x,e.clientY-chatDown.y)>8));
function chatGo(id){if(history.state?.drawer){history.replaceState(null,'',location.pathname+location.search+'#chat='+id);chatPushed=true}else if(!chatId){history.pushState(null,'',location.pathname+location.search+'#chat='+id);chatPushed=true}else history.replaceState(null,'',location.pathname+location.search+'#chat='+id);openChatLink()}
// In-page links, also when the page's base is another path; the "You asked" note opens the chat too.
$('#suggestions').addEventListener('click',e=>{const a=e.target.closest('a[href^="#chat="],a[href^="#card="]'),note=!a&&e.target.closest('[data-chat-open]');
 if(note&&!e.target.closest('a,button')){if(chatRealTap(e))chatGo(note.dataset.chatOpen);return}
 if(!a||e.ctrlKey||e.metaKey||e.shiftKey)return;e.preventDefault();const href=a.getAttribute('href');
 if(a.hasAttribute('data-chat-back')){if(chatPushed){history.back();return}history.replaceState(null,'',location.pathname+location.search+href);openChatLink();openCardLink();return}
 if(href.startsWith('#chat=')){if(chatRealTap(e)||chatId)chatGo(href.slice(6));return}
 location.hash=href});
$('#suggestions').addEventListener('toggle',e=>{const k=e.target.dataset?.foldKey;if(k==null||!e.target.closest('#chat-log'))return;e.target.open?chatOpenSet.add(k):chatOpenSet.delete(k)},true);
$('#suggestions').addEventListener('input',e=>{if(e.target.id==='chat-input'){chatGrow(e.target);chatDraftKeep(chatId,e.target.value)}});
$('#suggestions').addEventListener('focusin',e=>{if(e.target.id!=='chat-input')return;chatAtEnd=chatEndNow();if($('#chat-picks'))$('#chat-picks').hidden=false;chatKeyboard();setTimeout(chatKeyboard,350)});
$('#suggestions').addEventListener('focusout',e=>{if(e.target.id!=='chat-input')return;setTimeout(chatKeyboard,0);setTimeout(()=>{const p=$('#chat-picks');if(p&&!p.contains(document.activeElement))p.hidden=!chatPicksShown()},150)});
// Enter sends with a keyboard; on a touch screen Enter is a new line and the button sends.
$('#suggestions').addEventListener('change',e=>{if(e.target.id!=='chat-file')return;chatAddFiles([...e.target.files]);e.target.value=''});
// A pasted screenshot or file joins the message; pasted text stays text (an Office copy carries both: the text wins)
$('#suggestions').addEventListener('paste',e=>{if(e.target.id!=='chat-input')return;const files=[...(e.clipboardData?.files||[])];if(!files.length||e.clipboardData.getData('text/plain'))return;e.preventDefault();chatAddFiles(files)});
{let depth=0;const dragged=e=>chatId&&[...(e.dataTransfer?.types||[])].includes('Files')&&e.target.closest?.('.chat-layout');
 const mark=on=>$('#suggestions .chat-layout')?.classList.toggle('chat-drop',on);
 $('#suggestions').addEventListener('dragenter',e=>{if(!dragged(e))return;e.preventDefault();depth++;mark(true)});
 $('#suggestions').addEventListener('dragover',e=>{if(!dragged(e))return;e.preventDefault();e.dataTransfer.dropEffect='copy'});
 $('#suggestions').addEventListener('dragleave',e=>{if(!dragged(e))return;if(--depth<=0){depth=0;mark(false)}});
 $('#suggestions').addEventListener('drop',e=>{if(!dragged(e))return;e.preventDefault();depth=0;mark(false);chatAddFiles([...e.dataTransfer.files])})}
// Enter sends (on a phone it's a new line, the keyboard's Send key sends), Shift+Enter is a new line, Ctrl/Cmd+Enter
// always sends. Every way goes through chatSubmit, the Send button's own path, and is handled here so the page-wide
// Ctrl+Enter (it clicks the nearest primary button) never reaches the card's Do it under the box.
$('#suggestions').addEventListener('keydown',e=>{if(e.target.id!=='chat-input'||e.key!=='Enter'||e.isComposing||e.keyCode===229||e.altKey)return;const mod=e.ctrlKey||e.metaKey;
 if(!mod&&(e.shiftKey||matchMedia('(pointer: coarse)').matches))return;e.preventDefault();chatSubmit()});
// Sends what's in the message box (and its files): the bubble shows and the box empties once the Machine has it
async function chatSubmit(){const b=$('[data-chat-send]'),input=$('#chat-input');if(!b||b.disabled)return;const s=chatOpen(),text=input?.value.trim(),sending=chatPending.filter(f=>f.state==='ok'&&f.sid===s?.id);
 if(!s||!text&&!sending.length||chatPending.some(f=>f.state==='up')){input?.focus();return}b.disabled=true;
 const decide=args=>decidePost(s.id,args);
 // Without files a message can wait on the device while offline (decideOrWait); with files it needs the Machine now
 const steps=[...(s.status==='completed'?[{choice:'reopen',feedback:'',decision_id:crypto.randomUUID()}]:[]),{choice:'other',feedback:text,decision_id:'chat-'+crypto.randomUUID()}];
 try{if(!sending.length){const r=await decideOrWait(s.id,steps,'other');if(r?.waiting){input.value='';chatGrow(input);chatDraftKeep(s.id,'');b.disabled=false;chatSendState();paintChat();chatToEnd();return}}
  else{for(const a of steps.slice(0,-1))await decide(a);await decide({...steps.at(-1),files:sending.map(f=>f.id)})}
  const files=sending.map(f=>({id:f.id,name:f.name,type:f.type,size:f.size}));chatDropFiles();chatTray();chatFileError('');
  input.value='';chatGrow(input);chatDraftKeep(s.id,'');chat={...(chat||{}),items:[...(chat?.items||[]),{kind:'you',text,at:Date.now(),...(files.length?{files}:{})}],active:true,cursor:null};changing.delete(s.id);await refresh();paintChat();chatToEnd();chatPoll()}
 catch(err){errCaught(err);toast(err.message,true);b.disabled=false}}
$('#suggestions').addEventListener('click',async e=>{if(!chatId)return;
 const layout=e.target.closest('.chat-layout');if(e.target===layout&&chatDrawer){chatDrawer=false;layout.classList.remove('drawer');return}
 if(e.target.closest('[data-chat-drawer]')){e.target.closest('details')?.removeAttribute('open');drawerOpen();return}
 if(e.target.closest('.chat-menu-list button'))setTimeout(()=>$('#chat-menu')?.removeAttribute('open'));
 const scope=e.target.closest('.chat-side [data-scope]');if(scope){e.stopPropagation();scopeSet(scope.dataset.scope);return}
 const lg=e.target.closest('[data-learned-go],[data-learned-edit]');if(lg){e.stopPropagation();const v=lg.dataset.learnedGo;lg.dataset.learnedEdit?learnedShow(Number(lg.dataset.learnedEdit),'fact',true):learnedShow(Number(v)||null,lg.dataset.what);return}
 const lu=e.target.closest('[data-learned-undo]');if(lu){e.stopPropagation();lu.disabled=true;try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'forget_fact',args:{id:Number(lu.dataset.learnedUndo)}})});toast('Removed from what I’ve learned.');if(chat)chat.cursor=null;await chatPoll();refresh()}catch(err){errCaught(err);lu.disabled=false;toast(err.message,true)}return}
 const un=e.target.closest('[data-unclamp]');if(un){e.stopPropagation();const k=un.dataset.unclamp;chatOpenSet.has(k)?chatOpenSet.delete(k):chatOpenSet.add(k);paintChat();return}
 const b=e.target.closest('button');const input=$('#chat-input');
 // A quick pick or a suggestion fills the message box.
 if(b&&(b.dataset.choice==='pick'||b.dataset.chatSay!=null)&&input){e.stopPropagation();input.value=b.dataset.pick??b.dataset.chatSay;chatGrow(input);input.focus();return}
 if(e.target.closest('[data-chat-attach]')){e.stopPropagation();$('#chat-file')?.click();return}
 const rm=e.target.closest('[data-att-remove]');if(rm){e.stopPropagation();const f=chatPending.find(x=>x.key===rm.dataset.attRemove);chatPending=chatPending.filter(x=>x!==f);
  if(f?.id)request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'chat_file_remove',args:{suggestion_id:f.sid,id:f.id}})}).catch(()=>{});chatFileError('');chatTray();input?.focus();return}
 if(b?.hasAttribute('data-chat-stop')){e.stopPropagation();const s=chatOpen();if(!s)return;b.disabled=true;
  try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'chat_stop',args:{suggestion_id:s.id}})});
   if(chat)chat={...chat,active:false,live:null,cursor:null};await refresh();paintChat();chatPoll()}catch(err){errCaught(err);toast(err.message,true);b.disabled=false}return}
 if(!b?.hasAttribute('data-chat-send'))return;e.stopPropagation();chatSubmit()},true);
