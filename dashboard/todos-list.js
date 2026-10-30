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
const messageDrafts=s=>s?.status!=='prepared'?[]:taskActions(s).filter(a=>['email','linkedin','slack','x','whatsapp','telegram','intercom','doc_reply'].includes(a.kind)&&a.body&&!(sendBusy(a.state||s.action_status)&&!['local_preparation','paused'].includes((a.state||s.action_status)?.status)));
const draftHead=a=>a.kind==='email'?[['To',a.to_options?.length?t('You choose: {}',a.to_options.join(', ')):movedLine(a)||(a.to||[]).join(', ')],...['cc','bcc'].filter(k=>a[k]?.length).map(k=>[k==='cc'?'Cc':'Bcc',a[k].join(', ')]),['Subject',a.subject||'']]:[['To',a.kind==='x'&&a.reply_to?'@'+a.to_screen_name:a.to_name||'']];
const messageDraftBlock=s=>messageDrafts(s).map(a=>`<div class="result-draft"><h3>${a.kind==='email'?'Email':a.kind==='x'?(a.reply_to?'X reply':'X message'):a.kind==='linkedin'?'LinkedIn message':a.kind==='slack'?'Slack message':'WhatsApp message'} draft</h3>${draftHead(a).map(([k,v])=>`<p class="muted"><b>${k}:</b> ${esc(v)}</p>`).join('')}<div class="draft-text">${esc(a.body)}</div>${a.signature?'<p class="muted">+ your signature</p>':''}<div class="actions result-actions"><button class="primary" data-send-draft="${esc(a.revision)}">Review and send</button></div></div>`).join('');
async function openResult(id,file){const s=state.suggestions.find(s=>s.id===id);if(!s)return;file=file||(s.result_files||[]).find(f=>!/\.pdf$/i.test(f.name));resultId=id;$('#result-title').textContent=s.title;resultText=await resultTextFor(s,file);$('#result-content').innerHTML=format(withoutListedFiles(resultText,draftFiles(s))||'Open the PDF below to read it.')+messageDraftBlock(s);$('#result-files').innerHTML=(s.result_files||[]).map(f=>/\.pdf$/i.test(f.name)?`<a href="result-file?id=${id}&file=${encodeURIComponent(f.path)}" target="_blank" rel="noreferrer">Open ${esc(f.name)} ↗</a>`:`<button class="ghost" data-file="${esc(f.path)}">${esc(f.name)}</button><a href="result-file?id=${id}&file=${encodeURIComponent(f.path)}" download="${esc(f.name)}">Download</a>`).join('')+draftFilesBlock(s);if(!$('#result-dialog').open)$('#result-dialog').showModal()}
$('#result-files').onclick=async e=>{const file=e.target.closest('[data-file]')?.dataset.file;if(file){try{await openResult(resultId,state.suggestions.find(s=>s.id===resultId).result_files.find(f=>f.path===file))}catch(e){errCaught(e);toast(e.message,true)}}};
$('#result-content').onclick=e=>{const revision=e.target.closest('[data-send-draft]')?.dataset.sendDraft;if(revision){$('#result-dialog').close();openSend(resultId,revision)}};
$('#result-copy').onclick=()=>copyResult(resultId).catch(e=>toast(e.message,true));
// #result=<id> from Telegram and notifications sent before: the card's own page (its chat), as a tap in the list opens.
function openResultLink(){const match=/^#result=([a-f0-9]{16})$/.exec(location.hash);if(match&&state.suggestions){history.replaceState(null,'',location.pathname+location.search+'#chat='+match[1]);openChatLink()}}
// A link the installed app caught while it was open (launch_handler focus-existing): go where it points.
{const first=location.href;if('launchQueue' in window)launchQueue.setConsumer(p=>{const u=p.targetURL&&new URL(p.targetURL);if(u&&u.href!==first&&u.hash&&u.hash!==location.hash)location.hash=u.hash})}
let sendTask=null,sendRevision=null,sendDraft=null,sendHeader=null;
// Review and send opens on the draft itself, ready to edit, with Ask for changes (an instruction I redo the draft from) beside Send.
const SEND_EDITABLE=['email','linkedin','slack','x','whatsapp','telegram','intercom','doc_reply'];
function sendShow(){const edit=SEND_EDITABLE.includes(sendDraft?.kind);$('#send-ask').hidden=true;$('#send-act').hidden=false;$('#send-ask-text').value='';$('#send-ask-open').hidden=!edit;
 $('#send-dialog').showModal();if(edit)editSend(matchMedia('(pointer:fine)').matches)}
function openSend(id,revision){$('#send-ask').hidden=true;$('#send-bounce').hidden=true;$('#send-act').hidden=false;$('#send-ask-open').hidden=true;
const task=state.suggestions.find(s=>s.id===id),smart=taskActions(task),draft=revision?smart.find(a=>a.revision===revision):smart.find(a=>a.kind==='email');
if(!task||task.status!=='prepared'||!['email','email_demo','linkedin','slack','x','whatsapp','telegram','intercom','doc_reply','merge','finish','calendar','doc_write'].includes(draft?.kind)||(revision&&draft.revision!==revision)){toast('That draft changed. Review the current result.',true);return}
// A new doc or a doc edit: all of it, before and after (todos-docwrite.js)
if(draft.kind==='doc_write'){openDocWrite(id,draft);return}
// A calendar change: exactly what it adds, changes or deletes; the tap here makes it, and nobody hears about it.
if(draft.kind==='calendar'){sendTask=id;sendRevision=draft.revision;sendDraft=draft;$('#send-editor').hidden=true;$('#send-edit').hidden=true;$('#send-title').textContent={create:t('Add to {}?',draft.calendar_name),update:'Change this event?',delete:'Delete this event?'}[draft.op];$('#send-confirm').textContent={create:'Add',update:'Save',delete:'Delete'}[draft.op];$('#send-preview').classList.remove('code');$('#send-confirm').hidden=false;$('#send-confirm').disabled=false;$('#send-cancel').textContent='Cancel';$('#send-recipients').hidden=true;$('#send-files').hidden=true;$('#send-error').textContent='';
sendHeader=()=>sendRows([['Calendar',draft.calendar_name],['What',draft.title],['When',draft.when],...(draft.op==='update'&&draft.was&&(draft.was.title!==draft.title||draft.was.when!==draft.when)?[['Was',draft.was.title+', '+draft.was.when]]:[]),...(draft.location?[['Where',draft.location]]:[])]);sendHeader();
$('#send-preview').hidden=!draft.notes;sendBody(draft.notes||'');sendFine(draft.op==='delete'?'Only this event goes. Nobody gets an update.':'Nobody is invited or gets an update.');$('#send-dialog').showModal();return}
$('#send-confirm').textContent=draft.kind==='merge'?'Merge now':draft.kind==='finish'?'Confirm':draft.kind==='doc_reply'?'Post now':'Send now';$('#send-preview').classList.toggle('code',draft.kind==='merge');
// A fix to The Machine itself: what it changes, the files, and the full diff to read before merging.
if(draft.kind==='merge'){sendTask=id;sendRevision=draft.revision;sendDraft=draft;$('#send-editor').hidden=true;$('#send-preview').hidden=false;$('#send-edit').hidden=true;$('#send-title').textContent='Merge this fix into The Machine?';$('#send-confirm').hidden=false;$('#send-confirm').disabled=false;$('#send-cancel').textContent='Cancel';$('#send-recipients').hidden=true;$('#send-files').hidden=true;$('#send-error').textContent='';
sendHeader=()=>sendRows([['Fix',draft.summary],['Files',draft.files.length+' file'+(draft.files.length>1?'s':'')+', '+draft.commits+' commit'+(draft.commits>1?'s':'')]]);sendHeader();sendBody(draft.diff);$('#send-preview').insertAdjacentHTML('beforeend',`<p><a class="full-diff" href="api/merge-diff?id=${encodeURIComponent(id)}&revision=${encodeURIComponent(draft.revision)}" target="_blank" rel="noreferrer" download="the-machine-fix.diff">Download complete diff</a></p>`);
sendFine((draft.plugin?'The OpenClaw plugin changes too: it takes effect after openclaw plugins reload personal-assistant-bridge. ':'')+'Merge now runs the tests again, then updates the running code and restarts The Machine.');$('#send-dialog').showModal();return}
// The last step of a prepared task: what goes out; Confirm runs only that step.
if(draft.kind==='finish'){sendTask=id;sendRevision=draft.revision;sendDraft=draft;$('#send-editor').hidden=true;$('#send-preview').hidden=false;$('#send-edit').hidden=false;$('#send-subject-label').hidden=true;$('#send-title').textContent=draft.label+'?';$('#send-confirm').hidden=false;$('#send-confirm').disabled=false;$('#send-cancel').textContent='Cancel';$('#send-recipients').hidden=true;$('#send-files').hidden=true;$('#send-error').textContent='';
// It posts a message: the exact text, which Edit changes; Confirm types exactly that (replacing any earlier draft on the page).
// Files it uploads are listed and open from the card; without any, the dialog says nothing gets attached.
const files=draft.attachments||[];$('#send-files').hidden=!files.length;$('#send-files').innerHTML=draftFileLinks(id,files);
sendHeader=()=>sendRows([...(draft.url?[['Page',draft.url]]:[]),...(draft.message&&draft.to_name?[['To',draft.to_name]]:[]),...(draft.message?[['What',draft.preview]]:[]),...(draft.message&&!files.length?[['Files','None']]:[])]);sendHeader();sendBody(draftText(draft));
sendFine(draft.message?`Confirm types exactly this text on the page (replacing an earlier draft there), ${files.length?`attaches ${files.length>1?'these '+files.length+' files':'this file'}`:'attaches no file'}, submits it, checks that it went through and reports back.`:files.length?`Confirm does only this last step with ${files.length>1?'these files':'this file'}, checks that it went through and reports back.`:'Confirm does only this last step, checks that it went through and reports back.');$('#send-dialog').showModal();return}
sendTask=id;sendRevision=draft.revision;sendDraft=draft;$('#send-editor').hidden=true;$('#send-preview').hidden=false;$('#send-edit').hidden=draft.kind==='email_demo';$('#send-subject-label').hidden=['linkedin','slack','x','whatsapp','telegram','intercom','doc_reply'].includes(draft.kind);
// Handing it to someone: the card then waits for their reply.
const waits=draft.delegate?`After sending, this to-do waits ${draft.wait_days} day${draft.wait_days>1?'s':''} for ${draft.to_name?draft.to_name+'’s':'a'} reply; it closes when they answer.`:'';
if(['linkedin','slack','x','whatsapp','telegram','intercom','doc_reply'].includes(draft.kind)){$('#send-title').textContent=draft.kind==='doc_reply'?'Post this reply in the doc?':draft.kind==='x'?(draft.reply_to?'Reply on X?':'Send this X message?'):draft.kind==='slack'?'Send this Slack message?':draft.kind==='whatsapp'?'Send this WhatsApp message?':draft.kind==='telegram'?'Send this Telegram message?':draft.kind==='intercom'?'Send this reply in Intercom?':'Send this LinkedIn message?';$('#send-confirm').hidden=false;$('#send-confirm').disabled=false;$('#send-cancel').textContent='Cancel';$('#send-recipients').hidden=true;$('#send-files').hidden=true;$('#send-error').textContent='';
sendHeader=()=>sendRows(draft.kind==='doc_reply'?[['To',draft.to_name],['On',draft.doc_title]]:draft.kind==='intercom'?[['To',draft.to_name],['As',draft.as_name+' in Intercom']]:draft.kind==='x'?[['As','@'+draft.handle],draft.reply_to?['Replying to','@'+draft.to_screen_name+(draft.to_text?': “'+draft.to_text+'”':'')]:['To',draft.to_name]]:[['To',draft.to_name+(draft.profile?' (linkedin.com/in/'+draft.profile+')':draft.to_email?' ('+draft.to_email+')':'')]]);
sendHeader();sendBody(draft.body);sendFine(waits);sendShow();return}
const demo=draft.kind==='email_demo';$('#send-title').textContent=demo?'Demo email preview':INTERCOM_WHY[draft.intercom_fallback]?'Send by email instead?':'Send this email?';$('#send-confirm').hidden=demo;$('#send-cancel').textContent=demo?'Back':'Cancel';
// No verified recipient: pick from the thread's addresses (the first is preselected); To updates as you tick.
const options=draft.to_options||[];$('#send-recipients').hidden=!options.length;
const pre=Math.max(0,options.findIndex(x=>!draft.bounced?.[x.toLowerCase()]));  /* a working address is preselected */
$('#send-recipients div').innerHTML=options.map((x,i)=>`<label><input type="checkbox" value="${esc(x)}" ${i===pre?'checked':''}>${esc(x)}${bounceNote(draft.bounced?.[x.toLowerCase()])}</label>`).join('');
// Like the site's send preview: From/To/Subject rows, then the message in its own box.
// From: a small picker when this mailbox may also send as an alias of theirs (only ones Gmail confirms; own_addresses.senders).
const froms=draft.from_options||[];sendFrom=draft.from;
const header=(subject=true)=>{const to=options.length?sendRecipients():draft.to;sendBounced(to,draft);const rows=[['From',sendFrom],['To',to.length===1&&draft.to_name&&!options.length?draft.to_name+' <'+to[0]+'>':to.join(', ')||'(choose above)']];for(const key of ['cc','bcc'])if(draft[key]?.length)rows.push([key[0].toUpperCase()+key.slice(1),draft[key].join(', ')]);if(subject)rows.push(['Subject',draft.subject]);$('#send-confirm').disabled=!to.length;sendRows(rows);
 if(froms.length>1){$('#send-head dd').innerHTML=`<select id="send-from" aria-label="Send from">${froms.map(a=>`<option value="${esc(a)}"${a===sendFrom?' selected':''}>${esc(a)}</option>`).join('')}</select>`;$('#send-from').onchange=e=>{sendFrom=e.target.value}}};
sendHeader=header;$('#send-recipients').onchange=()=>header($('#send-editor').hidden);
header();sendBody(draft.body,draft.signature);sendFine([INTERCOM_WHY[draft.intercom_fallback]||'',draft.snooze_days?`After sending, the thread leaves your inbox for ${draft.snooze_days} day${draft.snooze_days>1?'s':''} (a weekday morning; a reply brings it back sooner).`:'',waits].filter(Boolean).join(' '));
const files=draft.attachments||[];$('#send-files').hidden=!files.length;
$('#send-files').innerHTML=draftFileLinks(id,files);
$('#send-error').textContent=demo?'Demo only. Nothing will be sent.':'';$('#send-confirm').disabled=options.length&&!sendRecipients().length;sendShow();
}
// A recipient whose address bounced: the sheet says so above the email; Send stays, the owner decides.
const sendBounced=(to,draft)=>{const el=$('#send-bounce'),hit=(to||[]).map(a=>draft?.bounced?.[String(a).toLowerCase()]).find(Boolean),moved=!hit&&movedLine(draft,to);el.hidden=!hit&&!moved;el.textContent=hit?t(to.length>1?'An address here bounced on {}':'This address bounced on {}',bounceDay(hit)):moved||''};
// A draft moved off an address that bounced to the person's working one (bounces.moved): "Bounced, now to <address>".
const movedLine=(a,to)=>{const x=(to||a?.to||[]).map(v=>String(v).toLowerCase()).find(v=>a?.moved?.[v]);return x?t('Bounced, now to {}',x):''};
// A follow-up held because its address bounced (follow_ups.BOUNCED_HELD) reads in the owner's language like the other holds
const heldLine=e=>{const m=/^Not sent: (\S+@\S+) bounced\.$/.exec(e||'');return m?t('Not sent: {} bounced.',m[1]):t(e)};
const sendRows=rows=>{$('#send-head').innerHTML=rows.map(([k,v])=>`<div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('')};
const sendBody=(body,signature)=>{const mail=['email','email_demo'].includes(sendDraft?.kind);$('#send-preview').classList.toggle('mail',mail);$('#send-preview').innerHTML=draftBody(sendDraft||{},body)+(signature?mail?'<span class="sig">+ your signature</span>':'<span class="sig">\n\n+ your signature</span>':'')};
const sendFine=text=>{$('#send-fine').textContent=text;$('#send-fine').hidden=!text};
let sendFrom=null;
const sendRecipients=()=>[...document.querySelectorAll('#send-recipients input:checked')].map(x=>x.value);
function openSendLink(){const match=/^#send=([a-f0-9]{16})&revision=([a-f0-9]{12})(&edit=1)?$/.exec(location.hash);if(match&&state.suggestions){openSend(match[1],match[2]);if(match[3]&&$('#send-dialog').open)editSend();history.replaceState(null,'',location.pathname)}}
// Edit the draft yourself: Send then sends exactly the edited text.
// The editor shows plain text: a link reads "words (address)" and Markdown marks are gone. Saving turns those links back
// into links; an untouched text sends exactly as drafted.
const plainDraft=t=>String(t||'').replace(MD_LINK,'$1 ($2)').replace(/\*\*([^*\n]+)\*\*/g,'$1').replace(/__([^_\n]+)__/g,'$1');
const unplainDraft=(edited,original)=>{let out=edited;for(const m of String(original||'').matchAll(MD_LINK))out=out.split(m[1]+' ('+m[2]+')').join(m[0]);return out};
function editSend(focus=true){const mail=sendDraft.kind==='email';$('#send-subject').value=sendDraft.subject||'';$('#send-body-label').hidden=mail;$('#send-rich').hidden=!mail;$('#send-rich-link').hidden=true;
 if(mail){mailLoad(draftText(sendDraft));if(KB_MAC)for(const[k,v]of[['b','Bold (Ctrl B)'],['i','Italic (Ctrl I)'],['link','Link (Ctrl K)']]){const x=document.querySelector(`[data-mail-tool="${k}"]`);if(x)x.title=t(v).replace('Ctrl ','⌘')}}  /* on a Mac the keys are ⌘ */
 else $('#send-body').value=plainDraft(draftText(sendDraft));
 $('#send-editor').hidden=false;sendHeader(false);subjectFit();$('#send-preview').hidden=true;$('#send-edit').hidden=true;if(focus!==false)(mail?mailRich():$('#send-body')).focus()}
// An email is edited as it will look (bold, italic, lists, links), never as marks or HTML. The editor holds only what
// an email can carry: a paste or a drop comes in as plain text, and Send reads the page back into the email's marks
// (mailBody), draws those once more the way the mail will be written (mailHtml) and sends only when both read the same.
// When they don't, the editor shows what would go out and Send waits for another tap. An untouched draft sends as drafted.
const mailRich=()=>$('#send-rich-body');
const mailStyled=(el,k)=>k==='b'?/^(B|STRONG)$/.test(el.tagName)||/^(bold|bolder|[6-9]00)$/.test(el.style.fontWeight):/^(I|EM)$/.test(el.tagName)||el.style.fontStyle==='italic';
// The page as lines: {type:'line'|'ul'|'ol', start, runs:[{t,b,i,h}]}; a bare address that is its own link counts as text
// Anything the email can't carry: other blocks (a heading, a quote), media, or text that looks different from its line
// (a color, a size, underline). Bold, italic and links are carried; their own look is theirs.
const MAIL_KEEP=/^(DIV|BR|B|STRONG|I|EM|UL|OL|LI|SPAN|FONT|A)$/;
function mailForeign(el){if(!MAIL_KEEP.test(el.tagName))return true;if(el.tagName==='A')return !/^https:\/\//.test(el.getAttribute('href')||'');if(/^(DIV|BR|UL|OL|LI)$/.test(el.tagName)||!el.isConnected)return false;
 const c=getComputedStyle(el),p=getComputedStyle(el.parentElement);return ['color','fontSize','fontFamily','textDecorationLine','verticalAlign','letterSpacing'].some(k=>c[k]!==p[k])||!/^(rgba\(0, 0, 0, 0\)|transparent)$/.test(c.backgroundColor)}
function mailModel(root){const blocks=[];let cur=null,foreign=false;
 const line=type=>cur||(cur={type,runs:[]});const end=()=>{if(cur)blocks.push(cur);cur=null};
 const after=n=>{for(let x=n;x&&x!==root&&!/^(DIV|P|LI|UL|OL)$/.test(x.tagName||'');x=x.parentNode)for(let s=x.nextSibling;s;s=s.nextSibling)if(s.nodeType===1||s.data?.trim())return true;return false};
 const walk=(n,m,type)=>{for(const c of n.childNodes){
  if(c.nodeType===3){c.data.split('\n').forEach((p,k)=>{if(k){line(type);end()}if(p)line(type).runs.push({t:p.replace(/ /g,' '),...m})});continue}
  if(c.nodeType!==1)continue;const tag=c.tagName;if(!foreign&&mailForeign(c))foreign=true;
  if(tag==='BR'){line(type);if(after(c))end();continue}
  if(tag==='UL'||tag==='OL'){end();let first=true;for(const li of c.children){cur={type:tag.toLowerCase(),runs:[]};if(first&&tag==='OL')cur.start=c.start||1;first=false;walk(li,m,cur.type);line(tag.toLowerCase());end()}continue}
  if(/^(DIV|P|H[1-6]|BLOCKQUOTE|PRE|LI|TABLE|TR|TD|TH|SECTION|ARTICLE)$/.test(tag)){end();walk(c,m,type);end();continue}
  const h=tag==='A'&&/^https:\/\//.test(c.getAttribute('href')||'')?c.getAttribute('href'):m.h;
  walk(c,{b:m.b||mailStyled(c,'b'),i:m.i||mailStyled(c,'i'),h},type)}};
 walk(root,{b:false,i:false,h:''},'line');end();
 // Spaces carry no bold or italic (they look the same either way), so a mark never has to open or close on one
 for(const bl of blocks){const runs=[],add=x=>{if(!x.t)return;const l=runs[runs.length-1];if(l&&l.b===x.b&&l.i===x.i&&l.h===x.h)l.t+=x.t;else runs.push(x)};
  for(const r of bl.runs){const h=r.h&&r.h!==r.t?r.h:'',m=/^(\s*)([\s\S]*?)(\s*)$/.exec(r.t);add({t:m[1],b:false,i:false,h});add({t:m[2],b:!!r.b,i:!!r.i,h});add({t:m[3],b:false,i:false,h})}
  bl.runs=runs;if(bl.type==='ol'&&bl.start==null)delete bl.start}
 blocks.foreign=foreign;return blocks}
const MAIL_BARE=/https:\/\/[^\s<>]*[^\s<>.,;:!?)\]]/g;
const mailMarkText=s=>{let out='',at=0;for(const m of s.matchAll(MAIL_BARE)){out+=s.slice(at,m.index).replace(/[\\*_\[\]]/g,'\\$&')+m[0];at=m.index+m[0].length}return out+s.slice(at).replace(/[\\*_\[\]]/g,'\\$&')};
const mailWrap=(s,mark)=>{const m=/^(\s*)([\s\S]*?)(\s*)$/.exec(s);return m[2]?m[1]+mark+m[2]+mark+m[3]:s};
// Back into the email's marks: links around bold around italic, so the marks always close in order
function mailBody(blocks){const italic=rs=>rs.map(r=>r.i?mailWrap(mailMarkText(r.t),'_'):mailMarkText(r.t)).join('');
 const bold=rs=>{let out='',k=0;while(k<rs.length){const b=rs[k].b,g=[];while(k<rs.length&&rs[k].b===b)g.push(rs[k++]);out+=b?mailWrap(italic(g),'**'):italic(g)}return out};
 const runs=rs=>{let out='',k=0;while(k<rs.length){const h=rs[k].h,g=[];while(k<rs.length&&rs[k].h===h)g.push(rs[k++]);out+=h?`[${bold(g).replace(/\n/g,' ')}](${h})`:bold(g)}return out};
 let n=1;return blocks.map((bl,k)=>{const text=runs(bl.runs);
  if(bl.type==='ul')return '- '+text;if(bl.type==='ol'){n=bl.start!=null?bl.start:n+1;return n+'. '+text}
  return text.replace(/^- /,'\\- ').replace(/^([0-9]{1,3})\. /,'$1\\. ')}).join('\n')}
const mailSame=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const mailModelOf=body=>{const d=document.createElement('div');d.innerHTML=mailHtml(body,false);return mailModel(d)};
let mailStart=null;
// fresh: the draft as it stands (an untouched editor sends exactly it); else only the page changes, to show what goes out
function mailLoad(body,fresh=true){const r=mailRich();r.innerHTML=mailHtml(body,false);if(fresh)mailStart=mailModel(r);mailTools()}
// What goes out from the editor: the draft as it was when nothing changed, else the page read back. null: not the same yet.
function mailOut(original){const now=mailModel(mailRich());if(!now.foreign&&mailStart&&mailSame(now,mailStart))return original;const body=mailBody(now);
 if(!now.foreign&&mailSame(mailModelOf(body),now))return body;
 mailLoad(body,false);$('#send-error').textContent=t('Some formatting can’t go in an email, so it was taken out. Check the message, then send.');return null}
function mailTools(){const on=document.activeElement===mailRich()||mailRich().contains(document.getSelection()?.anchorNode);
 for(const b of document.querySelectorAll('[data-mail-tool]')){const k=b.dataset.mailTool;let v=false;
  if(on)try{v=k==='link'?!!document.getSelection().anchorNode?.parentElement?.closest('#send-rich-body a'):document.queryCommandState({b:'bold',i:'italic',ul:'insertUnorderedList',ol:'insertOrderedList'}[k])}catch{}
  b.setAttribute('aria-pressed',String(v))}}
let mailRange=null;
function mailTool(k){const r=mailRich();r.focus();if(mailRange){const s=getSelection();s.removeAllRanges();s.addRange(mailRange);mailRange=null}
 if(k==='link'){const a=getSelection().anchorNode?.parentElement?.closest('#send-rich-body a');
  if(a){const range=document.createRange();range.selectNodeContents(a);const s=getSelection();s.removeAllRanges();s.addRange(range);document.execCommand('unlink');mailTools();return}
  mailRange=getSelection().rangeCount?getSelection().getRangeAt(0).cloneRange():null;$('#send-rich-link').hidden=false;$('#send-rich-url').value='';$('#send-rich-url').focus();return}
 document.execCommand({b:'bold',i:'italic',ul:'insertUnorderedList',ol:'insertOrderedList'}[k]);mailTools()}
// A link is an https address; a bare name.example gets https:// in front. Anything else (javascript:, mailto:…) is refused.
function mailLinkAdd(){let u=$('#send-rich-url').value.trim();if(u&&!/^[a-z][a-z0-9+.-]*:/i.test(u))u='https://'+u.replace(/^\/+/,'');
 let ok=false;try{const x=new URL(u);ok=x.protocol==='https:'&&!!x.hostname}catch{}
 if(!ok){$('#send-rich-url').setCustomValidity(t('Use a web address that starts with https://'));$('#send-rich-url').reportValidity();return}
 u=u.replace(/[\s()<>]/g,c=>'%'+c.charCodeAt(0).toString(16).toUpperCase().padStart(2,'0'));
 $('#send-rich-link').hidden=true;const r=mailRich();r.focus();const s=getSelection();if(mailRange){s.removeAllRanges();s.addRange(mailRange)}mailRange=null;
 if(s.isCollapsed)document.execCommand('insertHTML',false,`<a href="${esc(u)}">${esc(u)}</a>`);else document.execCommand('createLink',false,u);mailTools()}
$('#send-rich-url').addEventListener('input',e=>e.target.setCustomValidity(''));
$('#send-rich-url').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();mailLinkAdd()}else if(e.key==='Escape'){e.preventDefault();e.stopPropagation();$('#send-rich-link').hidden=true;mailRich().focus()}});
$('#send-rich-add').onclick=mailLinkAdd;$('#send-rich-cancel').onclick=()=>{$('#send-rich-link').hidden=true;mailRange=null;mailRich().focus()};
$('#send-rich').addEventListener('mousedown',e=>{if(e.target.closest('[data-mail-tool]'))e.preventDefault()});  // keeps the selection in the text
$('#send-rich').addEventListener('click',e=>{const b=e.target.closest('[data-mail-tool]');if(b)mailTool(b.dataset.mailTool)});
document.addEventListener('selectionchange',()=>{if(!$('#send-rich').hidden)mailTools()});
{const r=mailRich();
 r.addEventListener('keydown',e=>{const mod=KB_MAC?e.metaKey&&!e.ctrlKey:e.ctrlKey&&!e.metaKey,k=e.key.toLowerCase();
  if(e.key==='Enter'&&e.shiftKey){e.preventDefault();document.execCommand('insertParagraph');return}  // one line per line, as the mail writes it
  if(!mod||e.altKey)return;
  if(k==='b'||k==='i'){e.preventDefault();mailTool(k);return}
  if(k==='k'){e.preventDefault();mailTool('link');return}
  if(k==='u'||(e.shiftKey&&(k==='7'||k==='8'))){e.preventDefault();if(k!=='u')mailTool(k==='7'?'ol':'ul')}});
 const plain=(e,data)=>{const text=data?.getData('text/plain');e.preventDefault();if(text)document.execCommand('insertText',false,text.replace(/\r\n?/g,'\n'))};
 r.addEventListener('paste',e=>plain(e,e.clipboardData));r.addEventListener('drop',e=>plain(e,e.dataTransfer));
 r.addEventListener('input',()=>{$('#send-error').textContent='';mailTools()})}
$('#send-edit').onclick=()=>editSend();
// Ask for changes inside the dialog: the same instruction as the card's, and the draft is redone from it.
$('#send-ask-open').onclick=()=>{$('#send-act').hidden=true;$('#send-ask').hidden=false;$('#send-ask-text').focus()};
$('#send-ask-back').onclick=()=>{$('#send-ask').hidden=true;$('#send-act').hidden=false};
$('#send-ask-save').onclick=async()=>{const text=$('#send-ask-text').value.trim(),b=$('#send-ask-save');if(!text){$('#send-ask-text').focus();toast('Tell me what to change first.',true);return}
 b.disabled=true;try{await saveDecision(sendTask,'other',text);$('#send-dialog').close()}catch(e){errCaught(e);$('#send-error').textContent=e.message}finally{b.disabled=false}};
$('#send-ask-text').addEventListener('keydown',e=>{if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)&&!e.isComposing){e.preventDefault();$('#send-ask-save').click()}});
const showTheme=window.showTheme=()=>$('#theme-toggle').setAttribute('aria-checked',String(document.documentElement.dataset.theme==='light'));
{const lines=['Reads everything. Sends nothing you didn’t approve.','All rights reserved. All decisions yours.','Powered by coffee (yours) and electricity (mine).','No inboxes were harmed in the making of this list.','Handcrafted by one human and one very patient robot.'];
const day=Math.floor(Date.now()/864e5);$('#copyright').textContent=`© ${new Date().getFullYear()} The Machine. ${lines[day%lines.length]}`}
$('#theme-toggle').onclick=()=>{chooseTheme(document.documentElement.dataset.theme==='light'?'dark':'light');showTheme()};showTheme();
matchMedia('(prefers-color-scheme: light)').addEventListener('change',showTheme);
$('#send-cancel').onclick=()=>$('#send-dialog').close();
// A closed send panel keeps nothing: the next one fills it again, and a sent or canceled draft never reads as typing
$('#send-dialog').addEventListener('close',()=>{if($('#send-dialog').open)return;for(const id of ['send-subject','send-body','send-ask-text'])$('#'+id).value='';$('#send-rich-body').innerHTML='';$('#send-error').textContent=''});
// The subject wraps as it grows (field-sizing, or its height here where that's missing) but stays one line of text:
// Enter adds no line break and a pasted one becomes a space.
const subjectFit=()=>{const x=$('#send-subject');if(CSS.supports?.('field-sizing','content')||!x.offsetParent)return;x.style.height='auto';x.style.height=x.scrollHeight+'px'};
$('#send-subject').onkeydown=e=>{if(e.key==='Enter'&&!e.isComposing)e.preventDefault()};
$('#send-subject').oninput=e=>{const x=e.target,v=x.value.replace(/[ \t]*[\r\n]+[ \t]*/g,' ');if(v!==x.value){const at=x.selectionStart-(x.value.length-v.length);x.value=v;x.setSelectionRange(at,at)}subjectFit()};
addEventListener('resize',()=>{if($('#send-dialog').open)subjectFit()});
$('#send-confirm').onclick=async()=>{const b=$('#send-confirm');b.disabled=true;try{
if(!$('#send-editor').hidden){const mail=sendDraft.kind==='email',typed=$('#send-body').value,body=mail?mailOut(draftText(sendDraft)):typed===plainDraft(draftText(sendDraft))?draftText(sendDraft):unplainDraft(typed,draftText(sendDraft)),subject=['linkedin','slack','x','whatsapp','telegram','intercom','doc_reply','finish'].includes(sendDraft.kind)?undefined:$('#send-subject').value;
if(body==null){b.disabled=false;return}
if(body!==draftText(sendDraft)||subject!==sendDraft.subject){const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'revise_draft',args:{suggestion_id:sendTask,revision:sendRevision,body,subject}})});sendRevision=r.revision;
 // The saved text is what goes out. When saving changed it (a blank line before the name), it shows first and Send waits.
 if(r.body!=null){sendDraft={...sendDraft,revision:r.revision,...(subject===undefined?{}:{subject}),...(sendDraft.kind==='finish'?{[sendDraft.message?'message':'preview']:r.body}:{body:r.body})};
  if(r.body.trim()!==body.trim()){if(mail)mailLoad(r.body);else $('#send-body').value=plainDraft(r.body);$('#send-error').textContent=t('Saved with a small change. Check the message, then send.');b.disabled=false;return}}}}
await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'confirm_action',args:{suggestion_id:sendTask,revision:sendRevision,approval_id:crypto.randomUUID(),...($('#send-recipients').hidden?{}:{recipients:sendRecipients()}),...(sendDraft.kind==='email'&&sendDraft.from_options?.length>1&&sendFrom?{sender:sendFrom}:{})}})});
$('#send-dialog').close();toast(sendDraft.kind==='merge'?'Testing and merging the fix…':sendDraft.kind==='finish'?'On it. I’ll report back.':sendDraft.kind==='calendar'?'Changing the calendar…':sendDraft.kind==='doc_write'?'Writing the doc…':'Sending your approved draft…');await refresh();
}catch(e){errCaught(e);$('#send-error').textContent=e.offline?t('Offline. Send again when you’re back online.'):e.message;b.disabled=false}};
function openSnoozeLink(){const link=/^#snooze(-custom)?=([a-f0-9]{16})$/.exec(location.hash);if(link&&state.suggestions){if(state.suggestions.some(s=>s.id===link[2]&&!closed(s))){if($('#snooze-dialog').open)$('#snooze-dialog').close();openSnooze(link[2],!!link[1])}history.replaceState(null,'',location.pathname)}}
