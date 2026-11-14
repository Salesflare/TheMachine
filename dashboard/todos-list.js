let resultId=null,resultText='';
// The draft's files already show as links above the result, so drop a written list of only those files.
function withoutListedFiles(text,files){
const names=files.map(a=>a.name.toLowerCase()),lines=(text||'').split('\n'),out=[];
for(let i=0;i<lines.length;i++){
if(names.length&&/^\s*(?:#{1,6}\s*|\*\*)?(?:attachments?|bijlagen?)(?:\*\*)?\s*:?\s*$/i.test(lines[i])){
let j=i+1;while(j<lines.length&&!lines[j].trim())j++;const start=j;
while(j<lines.length&&/^\s*[-*•]\s+/.test(lines[j])&&names.some(n=>lines[j].toLowerCase().includes(n)))j++;
if(j>start&&(j>=lines.length||!/^\s*[-*•]\s+/.test(lines[j]))){i=j-1;while(out.length&&!out.at(-1).trim()&&j<lines.length&&!lines[j].trim())out.pop();continue}}
out.push(lines[i])}
return out.join('\n')}
async function resultTextFor(s,file){if(!file)return resultBody(s);const doc=await request('api/result?id='+s.id+'&file='+encodeURIComponent(file.path));return doc.pdf?null:doc.text}
async function copyResult(id){const s=state.suggestions.find(s=>s.id===id);if(!s)throw Error('Result not found');const doc=(s.result_files||[]).find(f=>!/\.pdf$/i.test(f.name)),draft=messageDrafts(s)[0];const text=!doc&&draft?draft.body:resultId===id&&$('#result-dialog').open?resultText:await resultTextFor(s,doc);if(!text)throw Error('Open the PDF to read this result.');try{await navigator.clipboard.writeText(text);toast('Copied.')}catch{await openResult(id);toast('Couldn’t copy automatically. Select the text to copy it.',true)}}
// The message drafts on a ready card, so Read result (also from Telegram) shows what Send would send (2026-10-20).
const messageDrafts=s=>s?.status!=='prepared'?[]:taskActions(s).filter(a=>SENDS.includes(a.kind)&&a.body&&!(sendBusy(a.state||s.action_status)&&!['local_preparation','paused'].includes((a.state||s.action_status)?.status)));
const draftHead=a=>a.kind==='email'?[['To',a.to_options?.length?t('You choose: {}',a.to_options.join(', ')):movedLine(a)||(a.to||[]).join(', ')],...['cc','bcc'].filter(k=>a[k]?.length).map(k=>[k==='cc'?'Cc':'Bcc',a[k].join(', ')]),['Subject',a.subject||'']]:[['To',a.kind==='x'&&a.reply_to?'@'+a.to_screen_name:a.to_name||''],...(replyWhere(a)?[['Where',replyWhere(a)]]:[])];
const messageDraftBlock=s=>messageDrafts(s).map(a=>html`<div class="result-draft"><h3>${a.kind==='email'?'Email':a.kind==='x'?(a.reply_to?'X reply':'X message'):a.kind==='linkedin'?'LinkedIn message':a.kind==='slack'?'Slack message':'WhatsApp message'} draft</h3>${draftHead(a).map(([k,v])=>html`<p class="muted"><b>${k}:</b> ${v}</p>`)}<div class="draft-text">${a.body}</div>${a.signature?html`<p class="muted">+ your signature</p>`:''}<div class="actions result-actions"><button class="primary" data-send-draft="${a.revision}">Review and send</button></div></div>`);
async function openResult(id,file){const s=state.suggestions.find(s=>s.id===id);if(!s)return;file=file||(s.result_files||[]).find(f=>!/\.pdf$/i.test(f.name));resultId=id;$('#result-title').textContent=s.title;resultText=await resultTextFor(s,file);setHTML($('#result-content'),html`${format(withoutListedFiles(resultText,draftFiles(s))||'Open the PDF below to read it.')}${messageDraftBlock(s)}`);setHTML($('#result-files'),html`${(s.result_files||[]).map(f=>{const href='result-file?id='+encodeURIComponent(id)+'&file='+encodeURIComponent(f.path);return /\.pdf$/i.test(f.name)?html`<a href="${href}" target="_blank" rel="noreferrer">Open ${f.name} ↗</a>`:html`<button class="ghost" data-file="${f.path}">${f.name}</button><a href="${href}" download="${f.name}">Download</a>`})}${draftFilesBlock(s)}`);if(!$('#result-dialog').open)$('#result-dialog').showModal()}
$('#result-files').onclick=async e=>{const file=e.target.closest('[data-file]')?.dataset.file;if(file){try{await openResult(resultId,state.suggestions.find(s=>s.id===resultId).result_files.find(f=>f.path===file))}catch(e){errCaught(e);toast(e.message,true)}}};
$('#result-content').onclick=e=>{const revision=e.target.closest('[data-send-draft]')?.dataset.sendDraft;if(revision){$('#result-dialog').close();openSend(resultId,revision)}};
$('#result-copy').onclick=()=>copyResult(resultId).catch(e=>toast(e.message,true));
// #result=<id> from Telegram and notifications sent before: the card's own page (its chat), as a tap in the list opens.
function openResultLink(){const match=/^#result=([a-f0-9]{16})$/.exec(location.hash);if(match&&state.suggestions){history.replaceState(null,'',location.pathname+location.search+'#chat='+match[1]);openChatLink()}}
// A link the installed app caught while it was open (launch_handler focus-existing): go where it points, any # link (a
// to-do, a chat, a promise), also the same link again. The launch that opened this page with its link comes first and
// is the page's own address: that one the page opens by itself. A link handed in is use: an update waiting for a quiet
// moment doesn't reload the page under it.
{const first=location.href;let seen=false;if('launchQueue' in window)launchQueue.setConsumer(p=>{const u=p.targetURL&&new URL(p.targetURL),opening=!seen;seen=true;
 if(!u||!u.hash||opening&&u.href===first)return;
 try{lastInput=lastTouch=Date.now()}catch{}  // (shell-tabs.js, further down the page: not there yet while the page itself still loads)
 if(u.hash!==location.hash)location.hash=u.hash;else dispatchEvent(new HashChangeEvent('hashchange'))})}
// A draft moved off an address that bounced to the person's working one (bounces.moved): "Bounced, now to <address>".
const movedLine=(a,to)=>{const x=(to||a?.to||[]).map(v=>String(v).toLowerCase()).find(v=>a?.moved?.[v]);return x?t('Bounced, now to {}',x):''};
// A follow-up held because its address bounced (follow_ups.BOUNCED_HELD) reads in the owner's language like the other holds
const heldLine=e=>{const m=/^Not sent: (\S+@\S+) bounced\.$/.exec(e||'');return m?t('Not sent: {} bounced.',m[1]):t(e)};
// The send dialog is the lazy 'compose' part (todos-send.js): these open it once it's in, at once when it already is.
function openSend(id,revision,step){lazyRun('compose',()=>sendOpen(id,revision,step))}
function openSendAll(id){lazyRun('compose',()=>sendOpenAll(id))}
function openSendLink(){const match=/^#send=([a-f0-9]{16})&revision=([a-f0-9]{12})(&edit=1)?$/.exec(location.hash);if(match&&state.suggestions){lazyRun('compose',()=>{openSend(match[1],match[2]);if(match[3]&&$('#send-dialog').open)editSend()});history.replaceState(null,'',location.pathname)}}
// Edit the draft yourself: Send then sends exactly the edited text.
// The editor shows plain text: a link reads "words (address)" and Markdown marks are gone. Saving turns those links back
// into links; an untouched text sends exactly as drafted.
const plainDraft=t=>String(t||'').replace(MD_LINK,'$1 ($2)').replace(/\*\*([^*\n]+)\*\*/g,'$1').replace(/__([^_\n]+)__/g,'$1');
const unplainDraft=(edited,original)=>{let out=edited;for(const m of String(original||'').matchAll(MD_LINK))out=out.split(m[1]+' ('+m[2]+')').join(m[0]);return out};
const showTheme=window.showTheme=()=>$('#theme-toggle').setAttribute('aria-checked',String(document.documentElement.dataset.theme==='light'));
{const lines=['Reads everything. Sends nothing you didn’t approve.','All rights reserved. All decisions yours.','Powered by coffee (yours) and electricity (mine).','No inboxes were harmed.'];
const day=Math.floor(Date.now()/864e5);$('#copyright').textContent=`© ${new Date().getFullYear()} The Machine. ${lines[day%lines.length]}`}
$('#theme-toggle').onclick=()=>{chooseTheme(document.documentElement.dataset.theme==='light'?'dark':'light');showTheme()};showTheme();
matchMedia('(prefers-color-scheme: light)').addEventListener('change',showTheme);
// An email address the dashboard shows as a link (a person's page, a link in a to-do or a chat) opens the composer
// (todos-compose.js), not the mail app. A right-click, a middle-click or a modifier key keeps the link's own mailto, as
// does Open in email in the composer. Only a plain address (a subject may come along); anything more stays a mailto.
const composeLink=href=>{const m=/^mailto:([^?#]+)(?:\?([^#]*))?$/i.exec(href);if(!m)return null;let to,q;
 try{to=decodeURIComponent(m[1]).trim();q=new URLSearchParams(m[2]||'')}catch{return null}
 if(!/^[^\s<>@,;"]+@[^\s<>@,;"]+\.[^\s<>@,;"]+$/.test(to)||[...q.keys()].some(k=>k.toLowerCase()!=='subject'))return null;return{to,subject:q.get('subject')||''}};
document.addEventListener('click',e=>{const a=e.target.closest?.('a[href^="mailto:" i]');
 if(!a||e.defaultPrevented||e.button||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey||a.closest('#send-dialog'))return;
 const m=composeLink(a.getAttribute('href'));if(!m)return;e.preventDefault();lazyRun('compose',()=>openCompose(m.to,m.subject,a.href))});
// The one way a draft goes out from the dashboard: the send dialog's Send and Go through's (todos-clear.js), for exactly
// the revision the owner saw. The server sends that revision or refuses (Store.confirm_action).
async function sendConfirmed(id,revision,kind,extra={}){await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'confirm_action',args:{suggestion_id:id,revision,approval_id:crypto.randomUUID(),...extra}})});
 if(SENT_WATCH.includes(kind))sentWatch.set(id,{revision,kind,at:Date.now()})}
// Once a send went out, one short toast says where the to-do is now, with Open to go to it there: "Sent. Moved to
// Done.", "Sent. Moved to Later until Mon." (handed to someone: back then unless they reply). Nothing when it failed.
const SENT_WATCH=[...SENDS,'finish'],sentWatch=new Map();
const sentDay=v=>{const d=new Date(v),days=(d-Date.now())/864e5;return days<6?localeDate(d,DL,{weekday:'short'}):localeDate(d,DL,{weekday:'short',day:'numeric',month:'short'})};
function sentWhere(){for(const [id,w] of sentWatch){const s=(state?.suggestions||[]).find(x=>x.id===id),st=s&&(taskActions(s).find(a=>a.revision===w.revision)?.state||s.action_status)?.status;
 if(!s||Date.now()-w.at>6e5){sentWatch.delete(id);continue}
 if(s.status==='prepared'&&!['sent','done'].includes(st)){if(['failed','blocked','uncertain','undone'].includes(st))sentWatch.delete(id);continue}  // still going, or it didn't go (the to-do says why)
 if(chatId&&chatId!==id)continue;  // another to-do is open: said once that one closes, never over it
 sentWatch.delete(id);const sent=w.kind!=='finish';
 const text=closed(s)||looksDone(s)?t(sent?'Sent. Moved to Done.':'Finished. Moved to Done.'):s.status==='snoozed'&&s.snoozed_until?t('Sent. Moved to Later until {}.',sentDay(s.snoozed_until)):waitsOnOthers(s)?t('Sent. Moved to Waiting on others.'):sent?t('Sent.'):'';
 if(text){toastOpen(text,s.status==='prepared'&&!waitsOnOthers(s)?'':id);$('#toast').dataset.about=id}}}
function toastOpen(text,id){toast(text);if(!id)return;const b=make('button',{type:'button','data-toast-open':id},t('Open'));$('#toast').append(' ',b);clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),8000)}
$('#toast').addEventListener('click',e=>{const b=e.target.closest('[data-toast-open]');if(!b)return;$('#toast').classList.remove('show');location.hash='#card='+b.dataset.toastOpen});
// A notification's quick button (sw.js quickKeep, #quick=): Snooze (2 hours, or tomorrow on a reminder) or Mark done on its to-do. A browser's
// notification can't ask for an unlock first, so it opens here and this does it, with Undo. The button comes from the
// worker only, once: a #quick= link from anywhere else does nothing. A to-do handled meanwhile opens as it is now.
const QUICK_RUN={snooze2h:['snooze','2h'],snooze:['snooze','tomorrow'],done:['complete']};let quickBusy=false;
function openQuickLink(){const m=/^#quick=(k_[a-f0-9]{16})$/.exec(location.hash);if(!m||!state?.suggestions||quickBusy)return;history.replaceState(null,'',location.pathname+location.search);if(!navigator.serviceWorker)return;quickBusy=true;
 navigator.serviceWorker.ready.then(r=>new Promise((ok,no)=>{const ch=new MessageChannel();ch.port1.onmessage=e=>ok(e.data);setTimeout(()=>no(Error('timeout')),15000);
  (navigator.serviceWorker.controller||r.active).postMessage({quick:m[1]},[ch.port2])})).then(d=>d&&quickRun(String(d.tag||''),String(d.action||''))).catch(e=>{errCaught(e);toast(e.message,true)}).finally(()=>{quickBusy=false})}
async function quickRun(id,action){const run=QUICK_RUN[action],s=state.suggestions.find(x=>x.id===id);if(!run||!/^[a-f0-9]{16}$/.test(id))return;
 if(!s||closed(s)||s.status==='snoozed'){chatGo(id);return}
 const done=await decideOrWait(id,[{choice:run[0],feedback:'',...(run[1]?{snooze_option:run[1]}:{})}],run[0]);await refresh();if(done?.waiting)return;
 if(run[0]==='complete'){toast(t('Marked done'),false,id);return}
 toast(t('Snoozed.')+' '+remindBack(done?.snoozed_until).line);const b=make('button',{type:'button','data-quick-undo':id},t('Undo'));$('#toast').append(' ',b);clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),15000)}
// Undo of that snooze: back where it was (Unsnooze). Its own attribute: the Snooze dialog's toast has its own Undo
$('#toast').addEventListener('click',async e=>{const b=e.target.closest('[data-quick-undo]');if(!b)return;b.disabled=true;
 try{await decidePost(b.dataset.quickUndo,{choice:'accept',feedback:'',decision_id:crypto.randomUUID()});await refresh();toast(t('Unsnoozed it'))}catch(err){errCaught(err);toast(err.message,true)}});
function openSnoozeLink(){const link=/^#snooze(-custom)?=([a-f0-9]{16})$/.exec(location.hash);if(link&&state.suggestions){if(state.suggestions.some(s=>s.id===link[2]&&!closed(s))){if($('#snooze-dialog').open)$('#snooze-dialog').close();openSnooze(link[2],!!link[1])}history.replaceState(null,'',location.pathname)}}
