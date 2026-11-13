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
const m=/^#card=([a-f0-9]{16})(&or=chat)?$/.exec(location.hash);if(!m||!state.suggestions)return;
const target=state.suggestions.find(s=>s.id===m[1]);
// &or=chat (the morning digest's Open): a to-do no longer on the list as shown (done, snoozed, another scope, or not
// here) opens its chat instead, as these links did before; openChatLink asks for an older done one itself
const toChat=()=>{history.replaceState(null,'',location.pathname+location.search+'#chat='+m[1]);openChatLink()};
if(m[2]&&(!target||closed(target)||target.status==='snoozed'||scopeFilter!=='all'&&target.scope!==scopeFilter)){toChat();return}
if(!target){doneFetch(m[1],()=>{if(location.hash==='#card='+m[1])openCardLink()});return} // an older done one: asked for; else kept for a later refresh
// One that looks done sits in Done, paged and folded, often past its first page: its chat is where it shows, so a
// link to it opens that; so does one with no row in the list for another reason, never a view with nothing picked out.
if(looksDone(target)){toChat();return}
linkedCardId=target.id;const fuEl=()=>target.follow_up?.group&&document.getElementById('fu-'+target.follow_up.group.replace(':','-'));
// Reveal this destination without overwriting the device's saved filter/fold preferences.
if(scopeFilter!=='all'&&target.scope!==scopeFilter)scopeFilter='all';
folded.delete('foryou');
// a link to this to-do (Open draft from a notification) shows it whole: its summary and its draft, never behind Show more
expandedBodies.add(target.id);for(const a of target.next_actions||(target.next_action?.kind==='menu'?target.next_action.actions:target.next_action?[target.next_action]:[]))expandedBodies.add('draft-'+target.id+'-'+a.revision);
render();document.querySelector('nav [data-tab="inbox"]').click();
const c=document.getElementById('task-'+target.id)||fuEl();if(!c){toChat();return}
for(let parent=c.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;
history.replaceState(null,'',location.pathname+location.search);
// a tall card (a draft in full) from its top, under the header, so its title shows too
const tall=c.offsetHeight>innerHeight*.7;c.style.scrollMarginTop=tall?'72px':'';c.scrollIntoView({block:tall?'start':'center',behavior:'smooth'});c.classList.remove('flash');void c.offsetWidth;c.classList.add('flash');kbFocus(c,false)}
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
 return n===0?'Today':n===1?'Yesterday':localeDate(d,DL,{weekday:'short',day:'numeric',month:'short',...(d.getFullYear()!==t.getFullYear()?{year:'numeric'}:{})})};
// Light markdown for a reply: paragraphs, lists, headings as bold lines, **bold**, *italic* and links.
// Slack-style emoji shortcodes (":tada:", ":+1::skin-tone-3:") as emoji; an unknown code stays as typed
const EMOJI={"smile":"😄","smiley":"😃","grinning":"😀","grin":"😁","joy":"😂","rofl":"🤣","sweat_smile":"😅","laughing":"😆","wink":"😉","blush":"😊","slightly_smiling_face":"🙂","upside_down_face":"🙃","heart_eyes":"😍","kissing_heart":"😘","thinking_face":"🤔","thinking":"🤔","face_with_hand_over_mouth":"🤭","shushing_face":"🤫","neutral_face":"😐","expressionless":"😑","no_mouth":"😶","smirk":"😏","unamused":"😒","roll_eyes":"🙄","face_with_rolling_eyes":"🙄","grimacing":"😬","relieved":"😌","pensive":"😔","sleepy":"😪","sleeping":"😴","mask":"😷","nerd_face":"🤓","sunglasses":"😎","confused":"😕","worried":"😟","open_mouth":"😮","astonished":"😲","flushed":"😳","pleading_face":"🥺","cry":"😢","sob":"😭","scream":"😱","sweat":"😓","weary":"😩","tired_face":"😫","yawning_face":"🥱","triumph":"😤","rage":"😡","angry":"😠","exploding_head":"🤯","partying_face":"🥳","star_struck":"🤩","zany_face":"🤪","money_mouth_face":"🤑","hugging_face":"🤗","hugs":"🤗","saluting_face":"🫡","melting_face":"🫠","skull":"💀","ghost":"👻","robot_face":"🤖","see_no_evil":"🙈","hear_no_evil":"🙉","speak_no_evil":"🙊","heart":"❤️","orange_heart":"🧡","yellow_heart":"💛","green_heart":"💚","blue_heart":"💙","purple_heart":"💜","black_heart":"🖤","white_heart":"🤍","broken_heart":"💔","sparkling_heart":"💖","100":"💯","fire":"🔥","sparkles":"✨","star":"⭐","tada":"🎉","confetti_ball":"🎊","balloon":"🎈","gift":"🎁","trophy":"🏆","rocket":"🚀","zap":"⚡","boom":"💥","bulb":"💡","eyes":"👀","wave":"👋","raised_hands":"🙌","clap":"👏","pray":"🙏","muscle":"💪","ok_hand":"👌","+1":"👍","thumbsup":"👍","-1":"👎","thumbsdown":"👎","point_up":"☝️","point_right":"👉","point_left":"👈","point_down":"👇","v":"✌️","crossed_fingers":"🤞","handshake":"🤝","facepalm":"🤦","face_palm":"🤦","shrug":"🤷","man_shrugging":"🤷‍♂️","woman_shrugging":"🤷‍♀️","white_check_mark":"✅","heavy_check_mark":"✔️","x":"❌","warning":"⚠️","no_entry":"⛔","question":"❓","exclamation":"❗","bangbang":"‼️","heavy_plus_sign":"➕","arrow_right":"➡️","arrow_left":"⬅️","arrow_up":"⬆️","arrow_down":"⬇️","repeat":"🔁","hourglass":"⌛","hourglass_flowing_sand":"⏳","alarm_clock":"⏰","calendar":"📆","date":"📅","memo":"📝","pencil":"📝","pencil2":"✏️","email":"📧","envelope":"✉️","phone":"☎️","iphone":"📱","computer":"💻","link":"🔗","lock":"🔒","unlock":"🔓","key":"🔑","mag":"🔍","chart_with_upwards_trend":"📈","chart_with_downwards_trend":"📉","moneybag":"💰","dollar":"💵","euro":"💶","coffee":"☕","beer":"🍺","beers":"🍻","champagne":"🍾","pizza":"🍕","cake":"🍰","sunny":"☀️","cloud":"☁️","rain_cloud":"🌧️","snowflake":"❄️","rainbow":"🌈","earth_africa":"🌍","car":"🚗","airplane":"✈️","house":"🏠","office":"🏢","dog":"🐶","cat":"🐱","unicorn_face":"🦄","raised_hand":"✋","writing_hand":"✍️","brain":"🧠","money_with_wings":"💸","pushpin":"📌","paperclip":"📎","package":"📦","construction":"🚧","sos":"🆘","ok":"🆗","new":"🆕","cool":"🆒","free":"🆓","heavy_minus_sign":"➖","slightly_frowning_face":"🙁","frowning":"😦","disappointed":"😞","hushed":"😯","innocent":"😇","yum":"😋","stuck_out_tongue":"😛","stuck_out_tongue_winking_eye":"😜","kissing":"😗","relaxed":"☺️","star2":"🌟","dizzy":"💫","sweat_drops":"💦","dash":"💨","zzz":"💤","spiral_calendar_pad":"🗓️","spiral_calendar":"🗓️","spiral_note_pad":"🗒️","card_index":"📇","clipboard":"📋","bookmark_tabs":"📑","page_facing_up":"📄","page_with_curl":"📃","scroll":"📜","calling":"📲","desktop_computer":"🖥️","keyboard":"⌨️","mag_right":"🔎","hammer_and_wrench":"🛠️","wrench":"🔧","hammer":"🔨","gear":"⚙️","inbox_tray":"📥","outbox_tray":"📤","incoming_envelope":"📨","mailbox":"📫","telephone_receiver":"📞","loudspeaker":"📢","mega":"📣","bell":"🔔","no_bell":"🔕","bar_chart":"📊","credit_card":"💳","receipt":"🧾","briefcase":"💼","globe_with_meridians":"🌐","rotating_light":"🚨","stopwatch":"⏱️","clock1":"🕐","watch":"⌚","umbrella":"☔","wine_glass":"🍷","birthday":"🎂","medal":"🏅","first_place_medal":"🥇","dart":"🎯","game_die":"🎲","musical_note":"🎵","headphones":"🎧","movie_camera":"🎥","camera":"📷","tv":"📺","books":"📚","book":"📖","notebook":"📓","ledger":"📒","label":"🏷️","triangular_flag_on_post":"🚩","checkered_flag":"🏁","flag-be":"🇧🇪","flag-us":"🇺🇸","flag-gb":"🇬🇧","flag-nl":"🇳🇱","flag-fr":"🇫🇷","flag-de":"🇩🇪","flag-es":"🇪🇸","ballot_box_with_check":"☑️","heavy_multiplication_x":"✖️","negative_squared_cross_mark":"❎","grey_question":"❔","no_entry_sign":"🚫","red_circle":"🔴","large_green_circle":"🟢","large_yellow_circle":"🟡","large_blue_circle":"🔵","white_circle":"⚪","black_circle":"⚫","arrows_counterclockwise":"🔄","top":"🔝","soon":"🔜","heavy_dollar_sign":"💲","speech_balloon":"💬","thought_balloon":"💭","sparkle":"❇️","gem":"💎","crown":"👑","alien":"👽","poop":"💩","hankey":"💩","writing":"✍️","eye":"👁️","busts_in_silhouette":"👥","bust_in_silhouette":"👤","man-shrugging":"🤷‍♂️","woman-shrugging":"🤷‍♀️","man-facepalming":"🤦‍♂️","woman-facepalming":"🤦‍♀️","mindblown":"🤯","star-struck":"🤩","cold_sweat":"😰","smiling_imp":"😈","heart_on_fire":"❤️‍🔥","two_hearts":"💕","seedling":"🌱","evergreen_tree":"🌲","deciduous_tree":"🌳","cactus":"🌵","herb":"🌿","four_leaf_clover":"🍀","sunflower":"🌻","rose":"🌹","tulip":"🌷","bug":"🐛","bee":"🐝","turtle":"🐢","snail":"🐌","whale":"🐳","octopus":"🐙","chart":"💹","sleuth_or_spy":"🕵️","female-detective":"🕵️‍♀️","ship":"🚢","satellite":"📡","electric_plug":"🔌","battery":"🔋","floppy_disk":"💾","cd":"💿","printer":"🖨️","file_folder":"📁","open_file_folder":"📂","card_file_box":"🗃️","wastebasket":"🗑️","world_map":"🗺️","round_pushpin":"📍","compass":"🧭","test_tube":"🧪","microscope":"🔬","pill":"💊","syringe":"💉","hospital":"🏥","school":"🏫","mortar_board":"🎓"};
const chatEmoji=t=>String(t).replace(/:([a-z0-9_+-]{1,40}):(?::skin-tone-([2-6]):)?(?!:)/g,(m,k,tone)=>EMOJI[k]?EMOJI[k]+(tone?String.fromCodePoint(0x1F3F9+ +tone):''):m);
// The one markdown renderer for what people and sources wrote (a reply here, a message in the viewer: events-email.js):
// `code` and ``` blocks as written, ~~strike~~, and a custom :emoji: code nobody can show as quiet text.
const mdPieces=(s,mark)=>s.replace(/~~([^~\n]+)~~/g,(m,x)=>mark(html`<del>`)+x+mark(html`</del>`))
 .replace(/(^|[\s(])(:(?=[a-z0-9_+-]*[a-z])[a-z0-9_+-]{2,40}:)(?=$|[\s).,!?])/g,(m,a,c)=>a+mark(html`<span class="emo-raw">`)+c+mark(html`</span>`));
function chatMarkdown(text){const out=[];let list=null,para=[],quote=null,fence=null;
 // Quoted lines ("> …") are a quote, never a raw ">"; a ``` block is code
 const src=String(text||'').split('\n'),lines=[];
 for(const l of src){if(fence){if(/^\s*```\s*$/.test(l)){lines.push({code:fence.join('\n')});fence=null}else fence.push(l);continue}
  const f=/^\s*```(.*)$/.exec(l);if(f){if(quote){lines.push({quote});quote=null}const one=/^(.*?)```\s*$/.exec(f[1]);if(one)lines.push({code:one[1]});else fence=/^[\w+-]*$/.test(f[1].trim())?[]:[f[1]];continue}
  const q=/^\s*>\s?(.*)$/.exec(l);if(q){(quote??=[]).push(q[1]);continue}if(quote){lines.push({quote});quote=null}lines.push(l)}
 if(fence)lines.push({code:fence.join('\n')});if(quote)lines.push({quote});
 const inline=t=>html`${String(t).split(/`([^`\n]+)`/).map((x,i)=>i%2?html`<code>${x}</code>`:richText(chatEmoji(x),true,{em:true,pieces:mdPieces}))}`;
 const flush=()=>{if(para.length)out.push(html`<p>${para.map((x,i)=>html`${i?html`<br>`:''}${inline(x)}`)}</p>`);para=[];if(list){const items=list.items.map(i=>html`<li>${inline(i)}</li>`);out.push(list.tag==='ol'?html`<ol>${items}</ol>`:html`<ul>${items}</ul>`)}list=null};
 for(const line of lines){if(line.code!=null){flush();out.push(html`<pre class="md-code"><code>${line.code}</code></pre>`);continue}
  if(line.quote){flush();out.push(html`<blockquote class="chat-quote">${chatMarkdown(line.quote.join('\n'))}</blockquote>`);continue}const b=/^\s*[-*•]\s+(.*)$/.exec(line),n=/^\s*\d+[.)]\s+(.*)$/.exec(line),h=/^\s*#{1,6}\s+(.*)$/.exec(line);
  if(!line.trim()){flush();continue}
  if(b||n){const tag=b?'ul':'ol';if(para.length||list&&list.tag!==tag)flush();list??={tag,items:[]};list.items.push((b||n)[1]);continue}
  if(list)flush();para.push(h?`**${h[1].replace(/\*\*/g,'')}**`:line)}
 flush();return html`${out}`}
// What changed between two versions of a draft, word by word.
function chatDiff(a,b){const x=String(a).split(/(\s+)/),y=String(b).split(/(\s+)/);if(x.length*y.length>400000)return null;
 const m=x.length,n=y.length,L=Array.from({length:m+1},()=>new Uint16Array(n+1));
 for(let i=m-1;i>=0;i--)for(let j=n-1;j>=0;j--)L[i][j]=x[i]===y[j]?L[i+1][j+1]+1:Math.max(L[i+1][j],L[i][j+1]);
 const out=[];let i=0,j=0;const push=(k,t)=>{const l=out.at(-1);l&&l[0]===k?l[1]+=t:out.push([k,t])};
 while(i<m&&j<n){if(x[i]===y[j]){push('=',x[i]);i++;j++}else if(L[i+1][j]>=L[i][j+1])push('-',x[i++]);else push('+',y[j++])}
 while(i<m)push('-',x[i++]);while(j<n)push('+',y[j++]);
 return html`${out.map(([k,t])=>k==='='?t:k==='-'?(t.trim()?html`<del>${t}</del>`:''):html`<ins>${t}</ins>`)}`}
// The card's own pieces for the chat, taken from the card as the dashboard draws it, so they stay the same.
// The card's own sends (their state refreshes every 2 s while one goes out): what the chat's draft says under it
const CHAT_SENDS=['email','linkedin','slack','x','whatsapp','telegram','signal','intercom','doc_reply'];
const chatSends=s=>taskActions(s).filter(a=>CHAT_SENDS.includes(a.kind)).map(a=>({a,st:a.state||s.action_status})).filter(x=>x.st?.status);
const chatGoing=st=>['queued','sending'].includes(st?.status)||st?.status==='uncertain'&&!st.retry_ok;
const chatFailed=st=>['failed','blocked'].includes(st?.status)||!!st?.retry_ok;
const CHAT_BY={email:'Sent to {} by email',email_demo:'Sent to {} by email',slack:'Sent to {} on Slack',linkedin:'Sent to {} on LinkedIn',whatsapp:'Sent to {} on WhatsApp',telegram:'Sent to {} on Telegram',signal:'Sent to {} on Signal',x:'Sent to {} on X',intercom:'Sent to {} in Intercom',doc_reply:'Sent to {} in the doc'};
function chatSendLine(d,x){const st=x.st,who=d.to.length&&!d.to.some(v=>v.includes('@'))?d.to.join(', '):x.a.to_name?.split(/\s+/)[0]||d.to.join(', ')||t('them');
 if(chatGoing(st))return html`<p class="chat-sendstate" role="status">${t(st.status==='uncertain'?'Checking it went out…':'Sending…')}</p><div class="send-progress" aria-hidden="true"><i></i></div>`;
 if(st.status==='sent')return html`<p class="chat-sendstate ok" role="status">${d.kind==='intercom'?t('Sent as {}',x.a.as_name||t('your Intercom admin')):t(CHAT_BY[d.kind]||'Sent to {}',who)}${st.sent_at?' · '+chatHM(Date.parse(st.sent_at)):''}</p>`;
 if(chatFailed(st))return html`<p class="chat-sendstate failed" role="alert">${st.retry_ok?st.error:t('Didn’t go out.')+(st.error?' '+st.error:'')}</p>`;
 return ''}
// A running to-do's live browser in the chat, as on its card: a slot while it runs (empty, so not shown, without a
// picture), so the picture stays between browser steps and goes only when the run is done with the browser. A click
// opens the Browser pane; while the run waits on the browser the slot holds Open the browser even before a picture.
const chatPeek=s=>{const via=s.preparation_browser||{link:state.browser_link||'',page:'',quiet:true};
 return html`<div class="note peek chat-peek" data-peek="${s.id}" data-peek-via="${JSON.stringify(via)}">${peekHTML(s.id,via)}</div>`};
function chatParts(s){const t=document.createElement('template');setHTML(t,suggestionCard(s,'Chat'));const card=t.content.querySelector('article');
 // The card's … menu, flat: Hand off…'s sheet gives its choices by their whole names (Hand to Codex, not Codex)
 const acts=[...(card?.querySelector(':scope>.actions')?.children||[])].flatMap(n=>n.matches('details.more-actions')?[...n.querySelectorAll('.more-menu>button,.more-menu>a,.mm-sub>button:not([data-mm-back]),.mm-sub>a:not([data-mm-back])')].filter(x=>x.dataset.mmOpen==null).map(x=>{if(x.dataset.full){x.textContent=x.dataset.full;delete x.dataset.full}return x}):[n]).map(n=>{n.removeAttribute('hidden');return n})  // a choice kept out of sight on the card is in the chat's menu
  .filter(n=>!['change','answer','cancel-change'].includes(n.dataset.choice)&&(n.dataset.handoffCheckin==null||s.status==='snoozed')&&n.dataset.rowFoldMenu==null);  // in the chat already: a nudge is asked for in words (a snoozed one's way back stays); Snooze once (the …'s copy is for a full row)
 // A snoozed card's way back is Unsnooze; a closed one's is Reopen or Undo: a text button on the status line
 // A to-do that looks done is one in Done, like the list draws it (lookDoneCard): Reopen puts it back on the list (not_done)
 const ld=looksDone(s),ldBack=ld?(()=>{const b=document.createElement('button');b.type='button';b.className='ghost';b.dataset.ldNot=s.id;return b})():null;
 const back=ld?ldBack:s.status==='snoozed'?acts.find(n=>n.dataset.choice==='accept'||n.dataset.handoffCheckin!=null):closed(s)?acts.find(n=>n.dataset.fuBack)||acts.find(n=>n.dataset.choice==='reopen')||acts.find(n=>n.dataset.choice==='undo'):null;
 if(back&&!back.dataset.fuBack)back.textContent=s.status==='snoozed'?(s.handoff_wait?'Check in now':'Unsnooze'):'Reopen';
 // The way back is in the ⋯ too, so the menu is never empty on a done to-do
 const backItem=back?.cloneNode(true);if(back)back.className='link chat-inline';
 const sends=chatSends(s),going=sends.some(x=>chatGoing(x.st)),went=sends.some(x=>x.st.status==='sent');
 // While a message goes out nothing is the next step yet; once it went out, Mark done is; after a failure, Try again
 let lead=back&&!ld||going?null:acts.find(n=>n.classList.contains('primary'))||(withTeammate(s)?acts.find(n=>n.dataset.choice==='complete'):null)||null;
 if(went&&!going&&!back&&!lead?.dataset.smart)lead=acts.find(n=>n.dataset.choice==='complete')||lead;
 if(lead?.dataset.smart&&chatFailed(sends.find(x=>String(x.a.revision)===lead.dataset.smart)?.st))lead.textContent='Try again';
 const ready=sendReady(s);
 if(lead?.dataset.smart&&ready.length>1&&ready.some(a=>a.revision==lead.dataset.smart)){lead.dataset.smart=ready[0].revision;lead.dataset.sendAll=1;lead.textContent=window.t(ready.every(a=>a.kind==='email')?'Review and send {} emails':'Review and send all {}',ready.length)}
 // On the card the title, project and area change with a tap on each; here they are in the menu too.
 const edits=document.createElement('template');setHTML(edits,closed(s)||ld?'':html`<button type="button" class="ghost" data-rename="${s.id}">${window.t('Rename')}</button>${s.project_node?html`<button type="button" class="ghost" data-card-project="${s.id}">${window.t('Change project')}</button>`:''}${moveTargets(s).length?html`<button type="button" class="ghost" data-card-area="${s.id}">${window.t('Change area')}</button>`:''}`);
 // Looks done: Done's menu (Reopen), and Mark done to say it is
 const rest=ld?[]:[...acts.filter(n=>n!==lead&&n!==back),...edits.content.children];
 const decide=rest.filter(n=>['complete','snooze','reject','accept','retry'].includes(n.dataset.choice)||n.dataset.smart!=null);
 if(backItem)rest.unshift(backItem);
 const status=card?.querySelector('.status-line:not(.ask-line):not(.done-line)')?.textContent.trim()||card?.querySelector('.card-badges .chip')?.textContent.trim()||'';
 const body=card?.querySelector('.body');body?.classList.remove('clamp');
 const panel=html`${[...(card?.querySelectorAll('.merge-offer,.change-editor:not([class*="answer"]),.fleet-handoff-form')||[])].filter(n=>!n.querySelector('[id^="feedback-"],[data-rt-change]')).map(n=>nodeHTML(n))}${s.preparation_status==='blocked'?(s.preparation_browser?html`<p class="note">${browserLink(s.id,s.preparation_browser)}</p>`:''):['running','starting'].includes(s.preparation_status)?chatPeek(s):''}`;
 const outer=n=>n?nodeHTML(n):'';
 return {sends,single:taskActions(s).filter(a=>CHAT_SENDS.includes(a.kind)).length<2,going,sheet:outer(card?.querySelector('.agent-form')),lead:outer(lead),send:!!lead?.dataset.smart,copy:lead?.dataset.result==='copy',back:outer(back),rest:orEmpty(html`${rest.map(outer)}`),options:orEmpty(html`${[lead,...decide].filter(Boolean).slice(0,3).map(n=>{n.classList.remove('ghost','primary');n.classList.add(n===lead?'primary':'ghost');return nodeHTML(n)})}`),
  status,intro:orEmpty(nodeHTML(...body?.childNodes||[])),ask:outer(card?.querySelector('.ask-line')),agent:outer(card?.querySelector('.agent-job')),
  links:orEmpty(nodeHTML(...card?.querySelector('.foot-links')?.childNodes||[])),panel:orEmpty(panel)}}
// What the card asks of the owner, in one plain line, when its text doesn't already ask: the question its run wrote,
// else from the title's "X needs your call on Y". An offer the card ends with ("I can check … and draft …") becomes a suggestion instead.
const CHAT_OFFER=/(?:^|\s)((?:I can|I could|I'll|I will|Happy to)\s[^.!?]*[.!?]?)\s*$/;
function chatQuestion(s){const body=String(s.body||'').trim(),offer=CHAT_OFFER.exec(body),rest=offer?body.slice(0,offer.index).trim().replace(/[;,:]$/,'.'):body;
 const m=/^.+?\s(?:needs|wants|is waiting (?:on|for)|awaits)\s+your\s+(call|decision|go-ahead|approval|ok|answer|input|help)\s+(?:on|about|for|with)\s+(.+?)[.?!]?$/i.exec(s.title||'');
 const own=s.preparation_questions?.[0]?.question,ask=/\?\s*$/.test(rest)?'':own?String(own).trim().replace(/[.?!]?$/,'?'):m?`Your ${/answer/i.test(m[1])?'answer':/input|help/i.test(m[1])?'input':'call'}: ${m[2]}?`:/^(?:Decide|Choose|Pick|Approve|Confirm)\b/.test(s.title||'')?String(s.title).replace(/[.?!]?$/,'?'):'';
 return {ask,offer:ask&&offer?offer[1]:'',body:ask&&offer?rest:body}}
const chatOpenSet=new Set();  // what is unfolded (steps, long messages, drafts, diffs, repeated taps), kept through a poll
// What is unfolded on screen right now, read before the thread is built again: the toggle event that records a fold
// comes a moment after it opens or closes, so a repaint in between (a poll, a draft preview loading) would undo it.
// Only from this chat's own thread, since the keys are positions in it.
function chatFoldsNow(id){const log=$('#chat-log');if(!log||log.closest('.chat-layout')?.dataset.chat!==id)return;
 for(const d of log.querySelectorAll('details[data-fold-key]'))d.open?chatOpenSet.add(d.dataset.foldKey):chatOpenSet.delete(d.dataset.foldKey)}
const chatFold=(key,cls,summary,body)=>html`<details class="${cls}" data-fold-key="${key}"${chatOpenSet.has(key)?html` open`:''}><summary>${summary}</summary>${body}</details>`;
// A run's steps, one row per kind with how many times, in the order each first came (the service already folds them;
// a step list from an older Machine is plain titles, one per step, said here as the service says them now, and
// its vague "Working" has no row)
const CHAT_STEP_OLD={'Using the browser':'Used the browser','Running a command':'Ran a command','Reading a file':'Read a file','Writing notes':'Wrote notes',
 'Searching the web':'Searched the web','Reading a web page':'Read a web page','Checking the assistant':'Looked things up in The Machine','Searching memory':'Searched memory',Working:''};
function chatSteps(steps){const rows=new Map();
 for(const s of steps||[]){const old=typeof s==='string'&&Object.prototype.hasOwnProperty.call(CHAT_STEP_OLD,s)?CHAT_STEP_OLD[s]:undefined,
  label=typeof s==='string'?(old!==undefined?old&&t(old):s):Array.isArray(s?.line)?t(...s.line):String(s?.text||'');if(!label)continue;
  const n=typeof s==='object'&&s.n>0?s.n:1,row=rows.get(label);row?row.n+=n:rows.set(label,{label,n})}
 return [...rows.values()]}
const chatLong=(t,lines=4)=>String(t||'').split('\n').length>lines||String(t||'').length>lines*70;
// A source in the chat by its one-color mark (todos-logos.js): Gmail, Outlook, Slack and the rest by name, else mail or chat
const chatViaIcon=(v,note)=>{const k=String(v||'').toLowerCase().trim();return note?'note':/^(gmail|outlook)\b/.test(k)?k.split(/\W/)[0]:/^(email|mail)/.test(k)?'mail':/calendar/.test(k)?'cal':monoKey(k)&&!['source','gateway'].includes(k)?k:'chat'};
const CHAT_VIA={email:'Email',gmail:'Email',slack:'Slack',linkedin:'LinkedIn',whatsapp:'WhatsApp',telegram:'Telegram',signal:'Signal chats',x:'X',calendar:'Calendar',intercom:'Intercom',github:'GitHub',android:'Phone'};
// The owner's own taps read as what they did, not a bare button name
// (said without "You": the side already says who)
const CHAT_TAPS={'Do it':'Chose Do it','Plan it':'Chose Plan it','Reopened':'Reopened it','Snoozed':'Snoozed it','Unsnoozed':'Unsnoozed it','Back for a check-in':'Brought it back for a check-in','Check-in moved':'Moved the check-in','Marked done':'Marked it done','Not done yet':'Marked it not done'};
// A send approved by voice waits a few seconds with Undo; the chat paints again when that ends
let chatUndoTimer=null;
const chatUndoVoice=(s,i)=>{clearTimeout(chatUndoTimer);chatUndoTimer=setTimeout(()=>paintChat(),i.undo_until-Date.now()+50);return html` · <button type="button" class="link" data-voice-undo="${i.undo_voice}" data-sid="${s.id}">Undo</button>`};
const chatEventText=i=>String(i.mine&&CHAT_TAPS[i.text]||i.text||'').replace(/^You\s+(\S)/,(m,c)=>c.toUpperCase());
const chatVia=v=>CHAT_VIA[v]||(v&&v!=='signal'?v[0].toUpperCase()+v.slice(1):'');
// Whose side an item is on: the owner's messages and taps on the right, the Machine and the people it is about on the left.
const chatSide=i=>i.kind==='you'||i.kind==='event'&&i.mine||i.kind==='source'&&i.mine?'you':i.kind==='event'||i.kind==='learned'||i.kind==='fixed'||i.kind==='recipe'||i.kind==='rc'?'mid':'them';
// A wrong thing fixed where it came from (corrections.py): what is right now and where the wrong one came from, in the
// owner's words, with Undo while it holds; an undone one stays, marked.
function chatFixed(i){const sep=html`<span class="learned-sep" aria-hidden="true">·</span>`,what=Array.isArray(i.line)?window.t(...i.line):String(i.text||''),
 line=i.from?window.t('Fixed: {}, from {}',what,i.from):window.t('Fixed: {}',what);
 return html`<div class="chat-event chat-learned chat-fixed${i.undone?html` gone`:''}"><span class="learned-acts"><span>${line}</span><span class="fixed-act">${sep}${i.undone?html`<span>${window.t('Undone')}</span>`:html`<button type="button" class="link" data-fixed-undo="${i.id}" aria-label="${window.t('Undo: {}',line)}">${window.t('Undo')}</button>`}</span></span></div>`}
// What a note on this card taught (from what was stored, never from what a reply says): a quiet line that opens it on
// What I've learned, with Edit and Undo while it is there (a channel's voice has its own 'Saved to How you write' line).
// A fact about a person, organization or project says so and opens that page, where it lives.
// A contact detail went on someone's record instead (contact_facts.py): the line opens their page, and Undo puts it back.
function chatLearned(i){const sep=html`<span class="learned-sep" aria-hidden="true">·</span>`,q=i.text?html`<q>${i.text}</q>`:'',node=i.about?html` data-learned-node="${i.about.id}"`:'';
 if(i.state==='record'){const line=window.t('Added to {}',i.name);return html`<div class="chat-event chat-learned"><span class="learned-acts"><a class="link" href="#graph/${encodeURIComponent(i.record)}">${line}</a>${sep}<button type="button" class="link" data-fixed-undo="${i.change}" aria-label="${window.t('Undo: {}',line)}">${window.t('Undo')}</button></span>${q}</div>`}
 if(i.state==='removed')return html`<div class="chat-event chat-learned gone"><span class="learned-acts">Removed from what I’ve learned</span>${q}</div>`;
 const id=i.state==='merged'?i.into:i.id,go=html`<button type="button" class="link" data-learned-go="${id||''}" data-what="${i.what}"${node}>${i.about?window.t('Saved to {} in the Graph',i.about.name):'Saved to what I’ve learned'}</button>`;
 return html`<div class="chat-event chat-learned"><span class="learned-acts">${go}${i.state==='saved'?html`${sep}<button type="button" class="link" data-learned-edit="${i.id}"${node} aria-label="Edit what was learned">Edit</button>${sep}<button type="button" class="link" data-learned-undo="${i.id}" aria-label="Undo: remove from what I’ve learned">Undo</button>`:''}</span>${q}</div>`}
let recipeEdit=null;  // todos-recipe.js
// A reply that says it left a page open in the browser (a sign-in tab, a form)
const CHAT_TAB=/\b(?:tab|browser)\b[^.]*\b(?:open|opened|reopened|ready)\b|\b(?:open|opened|reopened)\b[^.]*\b(?:tab|browser)\b|\bis open for\b/i;
function chatLog(s=chatOpen()){if(!chat)return html`<p class="chat-note">Loading…</p>`;if(s)chatFoldsNow(s.id);const p=s?chatParts(s):{},out=[];let day='',side='';
 const items=[...(chat.items||[])];
 // The card itself opens the conversation when no run has said anything yet: what it is about and what it needs
 if(s&&!items.some(i=>i.kind==='reply'))items.push({kind:'card',at:Date.parse(s.created_at)||0});
 // A coding agent's job that is still going or waits on you: its live block from the card, with its buttons
 const live=s?.agent_job&&p.agent?s.agent_job:null;if(live)items.push({kind:'agentlive',at:Date.parse(live.updated_at||live.started_at)||Date.now()});
 if(live)for(let n=items.length-1;n>=0;n--)if(items[n].kind==='agent'&&items[n].id===live.id){items.splice(n,1);break}  // its latest answer
 items.sort((a,b)=>(a.at||0)-(b.at||0));
 // The same tap again and again (five snoozes in a row) is one line with a count, unfolded for the times
 const rows=[];for(const i of items){const l=rows.at(-1);if(i.kind==='event'&&l?.kind==='event'&&l.text===i.text&&!!l.mine===!!i.mine)l.times.push(i.at),l.at=i.at;else rows.push(i.kind==='event'?{...i,times:[i.at]}:i)}
 if(s?.routine_change)lazyIn('routinetodos')?routineChangeRow(s,rows):lazyRun('routinetodos',paintChat);  // todos-routine-change.js
 const stamp=at=>{if(!at)return;const d=chatDayOf(at);if(d!==day){day=d;side='';out.push(html`<div class="chat-day">${d}</div>`)}};
 const tm=at=>at?html`<time class="chat-time" datetime="${new Date(at).toISOString()}" title="${localeDate(new Date(at),DL,{weekday:'short',month:'short',day:'numeric',year:'numeric'})+' '+chatHM(at)}">${chatHM(at)}</time>`:'';
 const push=(i,body)=>{const sd=chatSide(i);out.push(sd!==side?body:htmlEdit(body,c=>{const e=[...c.querySelectorAll('[class]')].find(n=>n.getAttribute('class').startsWith('chat-'));e?.setAttribute('class','cont '+e.getAttribute('class'))}));side=sd};
 const sent=new Set(items.filter(i=>i.kind==='event'&&i.sent).map(i=>i.sent.trim()));
 // Each send or cancel belongs to the latest draft before it (by its text for a send): only that one says Sent or Not sent
 const outcome=new Map();{const open=[];for(const i of items){if(i.kind==='reply')open.push(...(i.drafts||[]));if(i.kind!=='event')continue;
  const sent=i.sent?.trim(),d=sent?open.findLast(x=>!outcome.has(x)&&x.body.trim()===sent):/^(Send canceled|Didn’t go out)/.test(i.text||'')?open.findLast(x=>!outcome.has(x)):null;if(d)outcome.set(d,sent?'sent':'not')}}
 const drafts=items.flatMap(i=>i.kind==='reply'?(i.drafts||[]):[]),newest=drafts.at(-1);let prev=null;
 // The card's live send of a draft: the one with its text, else the newest when it is the only one
 const liveOf=d=>p.sends?.find(x=>typeof x.a.body==='string'&&x.a.body.trim()===d.body.trim())||(d===newest&&p.single&&p.sends?.length===1?p.sends[0]:null);
 for(const d of drafts)if(liveOf(d)?.st.status==='sent')sent.add(d.body.trim());
 // The decision buttons go on the Machine's latest message when the card is waiting on one (a Send goes on its draft)
 const open=s&&!closed(s)&&s.status!=='snoozed'&&!chat.active&&!['queued','starting','running'].includes(s.preparation_status);
 const lastMachine=rows.findLastIndex(i=>i.kind==='reply'||i.kind==='card'||i.kind==='event'&&i.handoff);
 const tabAt=s&&!closed(s)&&s.browser_open?rows.findLastIndex(i=>i.kind==='reply'&&CHAT_TAB.test(i.text||'')):-1;
 // While a message goes out no other choice shows; they come back once it went or failed
 const options=(n,onDraft)=>open&&!p.going&&n===lastMachine&&p.options&&!(p.send&&onDraft)?html`<div class="chat-options">${p.options}</div>`:'';
 const clamp=(k,body,long,more='More')=>long?html`<div class="chat-clamp${chatOpenSet.has(k)?html` open`:''}" data-unclamp-by="${k}">${body}</div><button type="button" class="link chat-more" data-unclamp="${k}">${chatOpenSet.has(k)?'Less':more}</button>`:body;
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
 const result=(n,i,inner,only)=>html`<div class="chat-result ${n===current?'current':'earlier'}${only?html` only-draft`:''}">${inner}${tm(i.at)}</div>`;
 let lastTo='';
 rows.forEach((i,n)=>{stamp(i.at);const k=n+':'+i.kind,res=isResult(i,n),quiet=res&&n!==current;
  if(i.kind==='source'){const via=chatVia(i.via)+(i.note&&i.via?' note':''),who=[i.mine?'You':i.from,via].filter(Boolean).join(' · ')||'Message';
   // Several messages in a row from the same person: their name and time on the first, each later one its own small time line; the link to the thread once, under the last
   const same=j=>j?.kind==='source'&&j.from===i.from&&j.mine===i.mine&&!!j.note===!!i.note&&chatDayOf(j.at)===chatDayOf(i.at),first=!same(rows[n-1]);
   const last=!(rows[n+1]?.kind==='source'&&!rows[n+1].mine&&chatDayOf(rows[n+1].at)===chatDayOf(i.at));
   const body=clamp(k,i.text?chatMarkdown(i.text):html`<p>${i.title}</p>`,chatLong(i.text,i.note?2:3));
   // A reply's quoted history is history, not a second message: folded under the new text
   const quoted=i.quoted?chatFold(k+':quoted','chat-quoted',t('Earlier messages'),html`<div class="chat-quoted-text" translate="no">${chatMarkdown(i.quoted)}</div>`):'';
   push(i,html`<div class="chat-msg ${i.mine?'you':'them'} chat-source${i.note?html` note`:''}">${first?html`<div class="chat-from"><span><i class="via-ico via-${chatViaIcon(i.via,i.note)}" aria-hidden="true"></i>${who}</span>${tm(i.at)}</div>`:html`<div class="chat-from chat-from-next">${tm(i.at)}</div>`}${i.files?chatAttHTML(i.files):''}<div class="bubble"><div class="say" translate="no">${body}</div>${quoted}${last&&hasOriginal(s)&&!i.mine?html`<button type="button" class="link read-original" data-id="${s.id}" data-original="read">Read the thread</button>`:''}</div></div>`)}
  else if(i.kind==='card'){const hasDraft=s.status==='prepared'&&p.send,intro=q.offer?chatMarkdown(q.body):p.intro;
   push(i,html`<div class="chat-msg machine chat-card"><div class="bubble">${intro||html`<p translate="no">${s.title}</p>`}</div>${res?'':html`${options(n,hasDraft)}${hasDraft?html`<div class="chat-card-send">${p.lead}</div>`:''}${tm(i.at)}`}</div>`);
   if(res)push(i,result(n,i,html`${p.ask?html`<div class="chat-ask">${p.ask}</div>`:q.ask?html`<p class="chat-q chat-result-title" translate="no">${q.ask}</p>`:html`<p class="chat-result-title" translate="no">${s.title}</p>`}${options(n,hasDraft)}${hasDraft?html`<div class="chat-card-send">${p.lead}</div>`:''}`))}
  else if(i.kind==='agentlive')push(i,html`<div class="chat-msg machine chat-agent">${p.agent}</div>`);
  else if(i.kind==='agent'){const all=i.files||[],pick=agentPick(all,i.full||i.text),files=orEmpty(html`${pick.shown.map(f=>agentFile({id:i.id},{path:f}))}${agentMoreFiles(pick.hidden)}`),
    allFiles=pick.hidden?html`<details class="agent-more chat-allfiles"><summary>All files</summary>${agentAllFiles({id:i.id},all,false)}</details>`:'';
   // A shortened answer (its housekeeping left out) has More too, which shows the whole answer
   const whole=i.full&&chatOpenSet.has(k)?i.full:i.text,text=clamp(k,chatMarkdown(whole),chatLong(i.text)||!!i.full);
   // Plain text like any reply: whose answer it is, small above; its files and "<agent> sent nothing" on one line under it
   // (left out once the owner sent the card's message after it)
   const nothing=i.nothing_sent&&!rows.slice(n+1).some(j=>j.kind==='event'&&j.sent)?html`<small class="chat-noted">${i.name} sent nothing</small>`:'';
   push(i,html`<div class="chat-msg machine chat-agent-msg"><div class="chat-agent-name">${i.name}</div><div class="bubble" translate="no">${text}</div>${files||nothing?html`<div class="chat-files">${files}${nothing}</div>`:''}${allFiles}${tm(i.at)}</div>`)}
  else if(i.kind==='steps'){const steps=chatSteps(i.steps),n=i.count||(i.steps||[]).reduce((a,s)=>a+(s?.n>0?s.n:1),0);
   push(i,html`<div class="chat-work">${chatFold(k,'chat-steps',t(['Checked {} thing','Checked {} things'],n),html`<ul>${steps.map(s=>html`<li><span>${s.label}</span>${s.n>1?html`<span class="chat-step-n"> · ${s.n}</span>`:''}</li>`)}</ul>`)}</div>`)}
  else if(i.kind==='event'){const c=i.times.length,t=chatEventText(i),line=html`${c>1?html`${t} ${c} times<span class="chev" aria-hidden="true">›</span>`:t}${i.voice&&c===1?html` · <a class="learn-link" href="#settings/writing" data-voice-edit="${i.voice}">Edit</a>`:''}${i.undo_voice&&s&&i.undo_until>Date.now()?chatUndoVoice(s,i):''}`;
   // A handoff that didn't go out: Try again opens the handoff form again, as it was sent
   const retry=i.retry_handoff&&s&&!closed(s)&&!s.fleet_handoff?html` · <button type="button" class="link" data-fleet-handoff="${s.id}">Try again</button>`:'';
   push(i,html`<div class="chat-event${i.mine?html` mine`:''}${i.retry_handoff?html` failed`:''}">${c>1?chatFold(k+':'+i.times[0],'',html`${line}${tm(i.at)}`,html`<ol>${i.times.map(t=>html`<li>${chatDayOf(t)} ${chatHM(t)}</li>`)}</ol>`):html`${line}${i.handoff?html`<span class="chat-when"> · ${chatHM(i.at)}</span>`:tm(i.at)}${retry}`}</div>`);
   if(i.handoff&&n===lastMachine&&s&&withTeammate(s))push({kind:'event',mine:i.mine},html`<div class="chat-event chat-handoff-wait">${window.t('No answer from {} yet',String(s.fleet_handoff.name||window.t('your teammate')).split(' ')[0])}</div>`);
   if(i.handoff&&n===lastMachine&&options(n,false))push({kind:'event',mine:false},html`<div class="chat-msg machine chat-handoff-options">${options(n,false)}</div>`)}
  else if(i.kind==='learned')push(i,chatLearned(i));
  else if(i.kind==='fixed')push(i,chatFixed(i));  // no time of its own: it sits under its reply, and beside a wide centered line it would stick out sideways
  else if(i.kind==='recipe')push(i,lazyIn('recipe')?chatRecipe(i):(lazyRun('recipe',paintChat),''));
  else if(i.kind==='rc')push(i,i.html);
  else if(i.kind==='you'){const to=i.to||'',show=to&&to!==lastTo;lastTo=to;
   const att=chatAttHTML(i.files);
   push(i,html`<div class="chat-msg you">${show?html`<div class="chat-to">to ${to}</div>`:''}${att}${i.text?html`<div class="bubble" translate="no">${chatMarkdown(i.text)}</div>`:''}${tm(i.at)}</div>`)}
  else if(i.kind==='reply'){const ds=i.drafts||[],h=headline(i.text);
   const tab=n===tabAt?html`<a class="agent-file via-browser" href="${safeHref(state.browser_link||'#')}" target="_blank" rel="noopener" data-browser-show="${s.id}">View in Machine browser</a>`:'';
   // Stopped, and what the run learned, right under the reply's text: at its foot a bare note read as a label on
   // the owner's next message
   const noted=html`${i.stopped?html`<small class="chat-noted chat-stopped">Stopped</small>`:''}${i.noted?html`<small class="chat-noted chat-noted-learned"><a class="link" href="#learning=learned">Saved to what I’ve learned</a></small>`:''}`;
   // Without a headline the reply is plain text and its drafts are the result; with one, the headline and summary lead the result
   const fileOf=f=>html`<button type="button" class="agent-file via-file" data-id="${s.id}" data-result="read" data-file="${f.path}" data-file-name="${f.label}">${f.label}<span aria-hidden="true"> ›</span></button>`;
   const copy=n===copyAt,files=orEmpty(html`${(i.files||[]).filter(f=>!copy||f!==i.files[0]).map(fileOf)}`);
   const chips=tab||files?html`<div class="chat-files">${tab}${files}</div>`:'';
   if(!res||!h)push(i,html`<div class="chat-msg machine">${i.text||!i.stopped?html`<div class="bubble" translate="no">${chatMarkdown(i.text)}</div>`:''}${noted}${chips}${ds.length||copy?'':options(n,false)}${res?'':tm(i.at)}</div>`);
   if(!res)return;
   if(copy){const f=(i.files||[])[0]||{label:'Draft',path:(s.result_files||[]).find(f=>!/\.pdf$/i.test(f.name))?.path},key=s.id+'|'+f.path,text=chatFiles.get(key),fk=k+':file';
    const df=draftFile(text),src=rows.findLast(x=>x.kind==='source'&&!x.mine&&x.via),where=src?chatVia(src.via)+(src.note?' note':''):'';
    const title=[df.name||f.label,where].filter(Boolean).join(' · ');
    const body=text==null?html`<div data-preview="${key}"><p class="chat-note">Loading the draft…</p></div>`:df.body?html`<div class="chat-draft-text chat-clamp${chatOpenSet.has(fk)?html` open`:''}"${chatLong(df.body,4)?html` data-unclamp-by="${fk}"`:''}>${chatMarkdown(df.body)}</div>${chatLong(df.body,4)?html`<button type="button" class="link chat-more" data-unclamp="${fk}">${chatOpenSet.has(fk)?'Less':'Show all'}</button>`:''}`:'';
    push(i,result(n,i,html`<div class="chat-result-head"><span class="chat-result-title">${title}</span><button type="button" class="link" data-id="${s.id}" data-result="read" data-file="${f.path}" data-file-name="${f.label}">Open</button></div>${body}<p class="chat-why">${COPY_WHY}</p>${options(n,false)}`));return}
   const parts=html`${ds.map((d,m)=>{const dk=k+':d'+m,ls=liveOf(d),liveSent=ls?.st.status==='sent',went=outcome.get(d)==='sent'||liveSent,last=d===newest&&!went&&s?.status==='prepared',not=!last&&outcome.get(d)==='not';
    const before=prev&&!ds.includes(prev)&&prev.kind===d.kind&&!sent.has(prev.body.trim())&&prev.body!==d.body?chatDiff(prev.body,d.body):null;prev=d;
    const to=d.to.length?' to '+d.to.join(', '):'',what=d.reply?'Reply':d.kind==='email'||d.kind==='email_demo'?'Email':d.kind==='whatsapp'?'WhatsApp':d.kind==='telegram'?'Telegram':d.kind==='signal'?'Signal':'Message';
    const links=orEmpty(html`${[chatLong(d.body,quiet?2:4)?html`<button type="button" class="link" data-unclamp="${dk}">${chatOpenSet.has(dk)?'Less':'Show all'}</button>`:'',before?html`<button type="button" class="link" data-unclamp="${dk}:diff">${chatOpenSet.has(dk+':diff')?'Hide changes':'Show what changed'}</button>`:''].filter(Boolean)}`);
    return html`<div class="chat-draft${went||not?html` went`:''}${last?html` current`:''}"><div class="chat-draft-head"><span>${what}${to}</span>${went?(liveSent?'':html`<span class="went-tag">Sent</span>`):not?html`<span class="went-tag not">Not sent</span>`:last||!quiet?'':html`<span>Earlier draft</span>`}</div>${d.subject&&!d.reply?html`<div class="chat-draft-subject">${d.subject}</div>`:''}<div class="chat-clamp${chatOpenSet.has(dk)?html` open`:''}${d.kind==='email'||d.kind==='email_demo'?html` mail-text`:''}"${chatLong(d.body,quiet?2:4)?html` data-unclamp-by="${dk}"`:''}>${d.kind==='email'||d.kind==='email_demo'?mailHtml(d.body):chatMarkdown(d.body)}</div>
     ${before&&chatOpenSet.has(dk+':diff')?html`<div class="chat-diff">${before}</div>`:''}${ls&&(last||liveSent)?chatSendLine(d,ls):''}${links||last&&p.send?html`<div class="chat-draft-foot"><span>${links}</span>${last&&p.send?p.lead:''}</div>`:''}</div>`})}`;
   const head=h?html`<div class="chat-result-head"><span class="chat-result-title" translate="no">${format(h.title)}</span></div>${h.rest?html`<div class="bubble" translate="no">${clamp(k,chatMarkdown(h.rest),quiet&&chatLong(h.rest,2))}</div>`:''}${noted}${chips}`:'';
   push(i,result(n,i,html`${head}${parts}${ds.length?options(n,true):h?options(n,false):''}`,!h&&ds.length===1))}});
 // A result with files: its links under the last reply
 if(p.links&&!drafts.length&&s?.status==='prepared'&&!p.copy)out.push(html`<div class="chat-links">${p.links}</div>`);
 if(s)out.push(outboxChat(s));
 if(chat.active)out.push(chat.live?.text?html`<div class="chat-msg machine chat-live"><div class="bubble" translate="no">${chatMarkdown(chat.live.text)}</div></div>`:raw('<div class="chat-msg machine chat-live"><div class="bubble typing" role="status" aria-label="Working"><i></i><i></i><i></i></div></div>'));
 // The run's side of the chat couldn't be read (the Gateway was slow or away) and nothing of it was loaded before:
 // said once the run is over, never as an aside under the typing dots; the next ask (a few seconds) tries again.
 if(chat.unavailable&&!chat.active)out.push(html`<p class="chat-note">I couldn’t load my replies just now. Trying again…</p>`);
 return html`${out}`}
// Up to three things to say, each specific to this to-do; tapping one fills the message box. Never canned lines (the
// old "What would you say?" chips went for that): the offer its text ends with ("I can check both dates" → "Check
// both dates"), and the review's asks for it (chat_asks, written with the to-do: no model call of their own). None
// when there is nothing that specific. In the to-do's own words, so never translated again.
const CHAT_OFFER_LEAD=/^(?:I can|I could|I'll|I will|Happy to)\s+/i;
function chatSuggestions(s){if(!chat||chat.active||closed(s))return [];let asks=[];try{asks=JSON.parse(s.chat_asks||'[]')}catch{}
 const q=(chat.items||[]).some(i=>i.kind==='reply')?{}:chatQuestion(s),offer=String(q.offer||'').replace(CHAT_OFFER_LEAD,'').replace(/[.!?]+$/,'').trim();
 const out=[offer&&offer[0].toUpperCase()+offer.slice(1),...(Array.isArray(asks)?asks:[])].map(x=>String(x||'').trim()).filter(x=>x&&x.length<=60);
 return [...new Set(out)].slice(0,3)}
const chatPicks=s=>html`${chatSuggestions(s).map(t=>html`<button type="button" class="chat-say" translate="no" data-chat-say="${t}">${t}</button>`)}`;
// Suggestions show while nothing has been said yet, or while you are writing
const chatPicksShown=()=>!(chat?.items||[]).some(i=>i.kind==='you')||document.activeElement?.id==='chat-input';
const BACK=html`<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M15 5l-7 7 7 7"/></svg>`;
const NC_PLUS=html`<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>`;
const SEND=html`<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 4.5l7 7-1.4 1.4-4.6-4.6V20h-2V8.3l-4.6 4.6L5 11.5z"/></svg>`;
const DOTS=html`<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="5" cy="12" r="1.8" fill="currentColor"/><circle cx="12" cy="12" r="1.8" fill="currentColor"/><circle cx="19" cy="12" r="1.8" fill="currentColor"/></svg>`;
const chatUntil=v=>{const d=new Date(v),days=(d-Date.now())/864e5;return (chatDayOf(v)==='Today'?'today':days<6&&days>-1?localeDate(d,DL,{weekday:'short'}):localeDate(d,DL,{weekday:'short',day:'numeric',month:'short'}))+' '+chatHM(v)};
// One small line over the message box: where the card stands, with its one way back (Unsnooze, Reopen) as a text button
function chatStatus(s,p=chatParts(s)){const text=chat?.active?'Working on it…':s.status==='snoozed'?(s.snoozed_until?(s.handoff_wait?checkinLabel(s):'Snoozed until '+chatUntil(s.snoozed_until)):'Snoozed')
  :closed(s)?(s.status==='completed'&&!lapsed(s)?'Done':'Not needed'):looksDone(s)?'Looks done':waitsAfterOwner(s)?p.status:stillWaiting(s)?stillWaiting(s):s.preparation_status==='working'?cardState(s):s.preparation_status==='blocked'&&s.preparation_error==='stopped'?'':s.preparation_status==='blocked'?p.status||cardState(s):['queued','starting','running'].includes(s.preparation_status)||['accepted','instructions'].includes(s.status)&&s.preparation_status!=='handed'?'Preparing':'';
 return text?html`<span>${text}</span>${p.back&&!chat?.active?html`<span aria-hidden="true">·</span>${p.back}`:''}`:''}
function chatView(s,groups){const p=chatParts(s);
 const side=html`<aside class="chat-side" aria-label="Tasks"><div class="scope-filter" role="group" aria-label="Show">${[['all','All'],['work','Work'],['personal','Personal']].map(([v,t])=>html`<button type="button" data-scope="${v}" aria-pressed="${scopeFilter===v}">${t}</button>`)}</div>${groups.map(([items,title,key])=>{const cut=sideList(items,key);return cut.count?html`<h3>${title}<span>${cut.count}</span></h3>${cut.list.map(x=>sideRow(x,s.id))}${cut.more?sideMoreRow(key):''}`:''})}</aside>`;
 return html`<div class="chat-layout${chatDrawer?html` drawer`:''}" data-chat="${s.id}">${side}<div class="chat-main"><header class="chat-head"><a class="chat-back" href="#card=${s.id}" data-chat-back aria-label="Back to the to-do" title="Back to the to-do">${BACK}</a><h2 class="chat-title" title="${s.title}" translate="no">${s.title}</h2>
  <details class="chat-menu" id="chat-menu"${p.rest?'':html` data-empty`}><summary aria-label="More actions" title="More actions">${DOTS}</summary><div class="chat-menu-list" role="group" aria-label="More actions">${p.rest}<button type="button" class="ghost" data-chat-drawer aria-expanded="${chatDrawer}">All tasks</button></div></details></header>
 <article id="task-${s.id}" class="chat-panel">${p.panel}</article><div class="chat-log" id="chat-log" aria-live="polite">${chatLog(s)}</div>
 <div class="chat-compose"><div class="offline-bar chat-offline" id="chat-offline" role="status"${netShown()?'':html` hidden`}>${netShown()?netHtml():''}</div><div class="chat-sheet" id="chat-sheet">${p.sheet}</div><div class="chat-status" id="chat-status">${chatStatus(s,p)}</div><div class="chat-picks" id="chat-picks"${chatPicksShown()?'':html` hidden`}>${chatPicks(s)}</div><p class="chat-drop-hint">Drop to add to your message</p><p class="chat-file-error" id="chat-file-error" role="alert" hidden></p><div class="chat-tray" id="chat-tray"${chatPending.length?'':html` hidden`}>${chatTrayHTML()}</div><div class="chat-box"><button type="button" class="chat-attach" data-chat-attach aria-label="Add files" title="Add files">${CLIP}</button><input type="file" id="chat-file" multiple hidden accept="${CHAT_ACCEPT}"><textarea id="chat-input" spellcheck="true" autocapitalize="sentences" rows="1" aria-label="Message" placeholder="${window.t('Ask or change something')}" enterkeyhint="send"></textarea><div class="chat-tools"><span class="grow"></span>${micBtn()}${talkBtn()}<button type="button" class="chat-send chat-stop" data-chat-stop aria-label="Stop" title="Stop"${chat?.active?'':html` hidden`}>${STOP}</button><button type="button" class="chat-send" data-chat-send aria-label="Send" title="Send"${chat?.active?html` hidden`:''} disabled>${SEND}</button></div></div><div class="chat-model" id="chat-model">${cmPill('chat')}</div></div></div></div>`}
function chatGrow(t){if(!t)return;t.style.height='34px';t.style.height=Math.min(160,Math.max(34,t.scrollHeight))+'px';chatSendState()}
// While a reply runs, Stop takes the place of Send until something is typed or added (sending then replaces the run).
function chatSendState(){const t=$('#chat-input'),b=$('[data-chat-send]'),x=$('[data-chat-stop]');if(!t||!b)return;
 const has=!!t.value.trim()||chatPending.length>0,ready=chatPending.every(f=>f.state==='ok'),stop=!!chat?.active&&!has;
 // With Talk live here, an empty box shows the wave where Send goes (as Send has nothing to send then)
 const w=$('.chat-compose [data-talk]'),talkHere=!!w&&talkOk();if(w)w.hidden=!talkHere||has||stop;
 b.disabled=!has||!ready;b.hidden=stop||talkHere&&!has;if(x){x.hidden=!stop;if(!stop)x.disabled=false}}
// Files the owner added (chat_files.py), on their message or on the to-do they made: images as pictures that open full
// size (events-photos.js), the rest as chips; each by fileLabel, as on the to-do
function chatAttHTML(fs){fs=fs||[];if(!fs.length)return '';const docs=fs.filter(f=>!/^image\//.test(f.type)),url=f=>'api/chat-file?id='+encodeURIComponent(f.id);
 return html`<div class="chat-you-files">${filePhotos(fs).map(p=>html`<span class="chat-you-img">${photoThumb(p)}</span>`)}${docs.length?html`<div class="chat-files">${docs.map(f=>html`<a class="agent-file via-file" href="${safeHref(url(f))}" target="_blank" rel="noopener" download="${f.name}">${fileLabel(f)}</a>`)}</div>`:''}</div>`}
// Files added to the next message (chat_files.py): from Add files, a paste or a drop, each uploaded at once and sent
// with the message. The same limits as the service's: they say so before anything uploads.
const CHAT_IMAGE=/\.(png|jpe?g|gif|webp)$/i,CHAT_EXT=/\.(png|jpe?g|gif|webp|pdf|txt|md|csv|tsv|json|log|rtf|eml|ics|docx|xlsx|pptx|odt|ods)$/i;
const CHAT_ACCEPT='image/png,image/jpeg,image/gif,image/webp,.pdf,.txt,.md,.csv,.tsv,.json,.log,.rtf,.eml,.ics,.docx,.xlsx,.pptx,.odt,.ods';
const CHAT_LIMIT={image:5*1048576,file:10*1048576,count:5};
const CLIP=html`<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.5l-8.1 8.1a5 5 0 0 1-7.1-7.1l8.4-8.4a3.3 3.3 0 0 1 4.7 4.7l-8.4 8.4a1.7 1.7 0 0 1-2.4-2.4l7.8-7.8"/></svg>`;
const STOP=html`<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="5" width="14" height="14" rx="2.5" fill="currentColor"/></svg>`;
const FILE_ICO=html`<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 2.8h8l4.2 4.2V21.2H6z M14 2.8V7h4.2"/></svg>`;
let chatPending=[];
const chatSize=n=>n>=1048576?(n/1048576).toFixed(1)+' MB':Math.max(1,Math.round(n/1024))+' KB';
const chatTrayHTML=(list=chatPending,attr='att-remove')=>html`${list.map(f=>{const img=f.type.startsWith('image/')&&f.url,label=fileLabel(f);return html`<div class="chat-att${img?html` img`:''}${f.state==='up'?html` up`:''}" title="${label}">${img?html`<img src="${safeHref(f.url)}" alt="${label}">`:html`<span class="chat-att-ico">${FILE_ICO}</span>`}<span class="chat-att-name">${label}<small>${f.state==='up'?'Uploading…':chatSize(f.size)}</small></span><button type="button" class="chat-att-x" data-${attr}="${f.key}" aria-label="Remove ${label}" title="Remove">×</button></div>`})}`;
function chatTray(){const t=$('#chat-tray');if(t){setHTML(t,chatTrayHTML());t.hidden=!chatPending.length}chatSendState()}
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
