// A lazy part (dashboard_parts.LAZY 'compose'): the send dialog. todos-list.js opens it through openSend(), nothing here until it's in.
let sendTask=null,sendRevision=null,sendDraft=null,sendHeader=null,sendBatch=null;
// Review and send opens on the draft itself, ready to edit, with Ask for changes (an instruction I redo the draft from) beside Send.
const SEND_CHATS=['linkedin','slack','x','whatsapp','telegram','signal','intercom','doc_reply'],SEND_EDITABLE=['email',...SEND_CHATS];
function sendShow(){const edit=SEND_EDITABLE.includes(sendDraft?.kind);$('#send-ask').hidden=true;$('#send-act').hidden=false;$('#send-ask-text').value='';$('#send-ask-open').hidden=!edit;
 sendStep();if(!$('#send-dialog').open)$('#send-dialog').showModal();$('#send-dialog').scrollTop=0;if(edit)editSend(matchMedia('(pointer:fine)').matches)}
// Several ready: each shows in turn, the last Send sends all
function sendOpenAll(id){const ready=sendReady(state.suggestions.find(s=>s.id===id));if(ready.length<2){openSend(id,ready[0]?.revision);return}
 sendBatch={id,list:ready.map(a=>a.revision),mail:ready.every(a=>a.kind==='email'),at:0,done:[]};openSend(id,ready[0].revision,1)}
function sendStep(){const b=sendBatch;$('#send-step').hidden=!b;if(!b)return;const n=b.list.length;
 $('#send-step').textContent=t('{} of {}',b.at+1,n);$('#send-confirm').textContent=b.at<n-1?t('Next'):t(b.mail?'Send {} emails':'Send all {}',n)}
function sendOpen(id,revision,step){if(!step)sendBatch=null;$('#send-mailapp').hidden=true;$('#send-ask').hidden=true;$('#send-bounce').hidden=true;$('#send-act').hidden=false;$('#send-ask-open').hidden=true;
const task=state.suggestions.find(s=>s.id===id),smart=taskActions(task),draft=revision?smart.find(a=>a.revision===revision):smart.find(a=>a.kind==='email');
if(!task||task.status!=='prepared'||!SEND_KINDS.includes(draft?.kind)||(revision&&draft.revision!==revision)){toast('That draft changed. Review the current result.',true);return}
// A new doc or a doc edit: all of it, before and after (todos-docwrite.js)
if(draft.kind==='doc_write'){openDocWrite(id,draft);return}
// A calendar change: exactly what it adds, changes or deletes; the tap here makes it, and nobody hears about it.
if(draft.kind==='calendar'){sendTask=id;sendRevision=draft.revision;sendDraft=draft;$('#send-editor').hidden=true;$('#send-edit').hidden=true;$('#send-title').textContent={create:t('Add to {}?',draft.calendar_name),update:'Change this event?',delete:'Delete this event?'}[draft.op];$('#send-confirm').textContent={create:'Add',update:'Save',delete:'Delete'}[draft.op];$('#send-preview').classList.remove('code');$('#send-confirm').hidden=false;$('#send-confirm').disabled=false;$('#send-cancel').textContent='Cancel';$('#send-recipients').hidden=true;$('#send-files').hidden=true;$('#send-error').textContent='';
sendHeader=()=>sendRows([['Calendar',draft.calendar_name],['What',draft.title],['When',draft.when],...(draft.op==='update'&&draft.was&&(draft.was.title!==draft.title||draft.was.when!==draft.when)?[['Was',draft.was.title+', '+draft.was.when]]:[]),...(draft.location?[['Where',draft.location]]:[])]);sendHeader();
$('#send-preview').hidden=!draft.notes;sendBody(draft.notes||'');sendFine(draft.op==='delete'?'Only this event goes. Nobody gets an update.':'Nobody is invited or gets an update.');$('#send-dialog').showModal();return}
$('#send-confirm').textContent=draft.kind==='merge'?'Merge now':draft.kind==='finish'?'Confirm':draft.kind==='doc_reply'?'Post now':'Send now';$('#send-preview').classList.toggle('code',draft.kind==='merge');
// A fix to The Machine itself: what it changes, the files, and the full diff to read before merging.
if(draft.kind==='merge'){sendTask=id;sendRevision=draft.revision;sendDraft=draft;$('#send-editor').hidden=true;$('#send-preview').hidden=false;$('#send-edit').hidden=true;$('#send-title').textContent='Merge this fix into The Machine?';$('#send-confirm').hidden=false;$('#send-confirm').disabled=false;$('#send-cancel').textContent='Cancel';$('#send-recipients').hidden=true;$('#send-files').hidden=true;$('#send-error').textContent='';
sendHeader=()=>sendRows([['Fix',draft.summary],['Files',draft.files.length+' file'+(draft.files.length>1?'s':'')+', '+draft.commits+' commit'+(draft.commits>1?'s':'')]]);sendHeader();sendBody(draft.diff);$('#send-preview').append(make('p',{},make('a',{class:'full-diff',href:'api/merge-diff?id='+encodeURIComponent(id)+'&revision='+encodeURIComponent(draft.revision),target:'_blank',rel:'noreferrer',download:'the-machine-fix.diff'},'Download complete diff')));
sendFine((draft.plugin?'The OpenClaw plugin changes too: it takes effect after openclaw plugins reload personal-assistant-bridge. ':'')+'Merge now runs the tests again, then updates the running code and restarts The Machine.');$('#send-dialog').showModal();return}
// The last step of a prepared task: what goes out; Confirm runs only that step.
if(draft.kind==='finish'){sendTask=id;sendRevision=draft.revision;sendDraft=draft;$('#send-editor').hidden=true;$('#send-preview').hidden=false;$('#send-edit').hidden=false;$('#send-subject-label').hidden=true;$('#send-title').textContent=draft.label+'?';$('#send-confirm').hidden=false;$('#send-confirm').disabled=false;$('#send-cancel').textContent='Cancel';$('#send-recipients').hidden=true;$('#send-files').hidden=true;$('#send-error').textContent='';
// It posts a message: the exact text, which Edit changes; Confirm types exactly that (replacing any earlier draft on the page).
// Files it uploads are listed and open from the card; without any, the dialog says nothing gets attached.
const files=draft.attachments||[];$('#send-files').hidden=!files.length;setHTML($('#send-files'),draftFileLinks(id,files));
sendHeader=()=>sendRows([...(draft.url?[['Page',draft.url]]:[]),...(githubWay(draft)?[[t('How'),githubWay(draft)]]:[]),...(draft.message&&draft.to_name?[['To',draft.to_name]]:[]),...(draft.message?[['What',draft.preview]]:[]),...(draft.message&&!files.length?[['Files','None']]:[])]);sendHeader();sendBody(draftText(draft));
sendFine(draft.message?`Confirm types exactly this text on the page (replacing an earlier draft there), ${files.length?`attaches ${files.length>1?'these '+files.length+' files':'this file'}`:'attaches no file'}, submits it, checks that it went through and reports back.`:files.length?`Confirm does only this last step with ${files.length>1?'these files':'this file'}, checks that it went through and reports back.`:'Confirm does only this last step, checks that it went through and reports back.');$('#send-dialog').showModal();return}
sendTask=id;sendRevision=draft.revision;sendDraft=draft;$('#send-editor').hidden=true;$('#send-preview').hidden=false;$('#send-edit').hidden=draft.kind==='email_demo';$('#send-subject-label').hidden=SEND_CHATS.includes(draft.kind);
// Handing it to someone: the card then waits for their reply.
const waits=draft.delegate?`After sending, this to-do waits ${draft.wait_days} day${draft.wait_days>1?'s':''} for ${draft.to_name?draft.to_name+'’s':'a'} reply; it closes when they answer.`:'';
if(SEND_CHATS.includes(draft.kind)){$('#send-title').textContent=draft.kind==='doc_reply'?'Post this reply in the doc?':draft.kind==='x'?(draft.reply_to?'Reply on X?':'Send this X message?'):draft.kind==='slack'?'Send this Slack message?':draft.kind==='whatsapp'?'Send this WhatsApp message?':draft.kind==='telegram'?'Send this Telegram message?':draft.kind==='signal'?'Send this Signal message?':draft.kind==='intercom'?'Send this reply in Intercom?':'Send this LinkedIn message?';$('#send-confirm').hidden=false;$('#send-confirm').disabled=false;$('#send-cancel').textContent='Cancel';$('#send-recipients').hidden=true;$('#send-files').hidden=true;$('#send-error').textContent='';
sendHeader=()=>sendRows(draft.kind==='doc_reply'?[['To',draft.to_name],['On',draft.doc_title]]:draft.kind==='intercom'?[['To',draft.to_name],['As',draft.as_name+' in Intercom']]:draft.kind==='x'?[['As','@'+draft.handle],draft.reply_to?['Replying to','@'+draft.to_screen_name+(draft.to_text?': “'+draft.to_text+'”':'')]:['To',draft.to_name]]:[['To',draft.to_name+(draft.profile?' (linkedin.com/in/'+draft.profile+')':draft.to_email?' ('+draft.to_email+')':'')],...(replyWhere(draft)?[['Where',replyWhere(draft)]]:[])]);
sendHeader();sendBody(draft.body);sendFine(waits);sendShow();return}
const demo=draft.kind==='email_demo';$('#send-title').textContent=demo?'Demo email preview':INTERCOM_WHY[draft.intercom_fallback]?'Send by email instead?':'Send this email?';$('#send-confirm').hidden=demo;$('#send-cancel').textContent=demo?'Back':'Cancel';
// No verified recipient: pick from the thread's addresses (the first is preselected); To updates as you tick.
const options=draft.to_options||[];$('#send-recipients').hidden=!options.length;
const pre=Math.max(0,options.findIndex(x=>!draft.bounced?.[x.toLowerCase()]));  /* a working address is preselected */
setHTML($('#send-recipients div'),html`${options.map((x,i)=>html`<label><input type="checkbox" value="${x}" ${i===pre?html`checked`:''}>${x}${bounceNote(draft.bounced?.[x.toLowerCase()])}</label>`)}`);
// Like the site's send preview: From/To/Subject rows, then the message in its own box.
// From: a small picker when this mailbox may also send as an alias of theirs (only ones Gmail confirms; own_addresses.senders);
// it opens the app's own menu (cmMenu), never the browser's list.
const froms=draft.from_options||[];sendFrom=draft.from;
const header=(subject=true)=>{const to=options.length?sendRecipients():draft.to;sendBounced(to,draft);const rows=[['From',sendFrom],['To',to.length===1&&draft.to_name&&!options.length?draft.to_name+' <'+to[0]+'>':to.join(', ')||'(choose above)']];for(const key of ['cc','bcc'])if(draft[key]?.length)rows.push([key[0].toUpperCase()+key.slice(1),draft[key].join(', ')]);if(subject)rows.push(['Subject',draft.subject]);$('#send-confirm').disabled=!to.length;sendRows(rows);
 if(froms.length>1){cmLists.from={label:'Send from',choices:()=>froms.map(a=>({value:a,label:a,name:true})),value:()=>sendFrom,pick:v=>{sendFrom=v;const s=$('#send-from>span');if(s)s.textContent=v}};
  setHTML($('#send-head dd'),cmTrigger('from','from',sendFrom,'from-pick',html` id="send-from" translate="no"`))}};
sendHeader=header;$('#send-recipients').onchange=()=>header($('#send-editor').hidden);
header();sendBody(draft.body,draft.signature);sendFine([INTERCOM_WHY[draft.intercom_fallback]||'',replyElsewhere(draft),draft.snooze_days?t(['Leaves your inbox for {} day after sending, or until a reply.','Leaves your inbox for {} days after sending, or until a reply.'],draft.snooze_days):'',waits].filter(Boolean).join(' '));
const files=draft.attachments||[];$('#send-files').hidden=!files.length;
setHTML($('#send-files'),draftFileLinks(id,files));
$('#send-error').textContent=demo?'Demo only. Nothing will be sent.':'';$('#send-confirm').disabled=options.length&&!sendRecipients().length;sendShow();
}
// A recipient whose address bounced: the sheet says so above the email; Send stays, the owner decides.
const sendBounced=(to,draft)=>{const el=$('#send-bounce'),hit=(to||[]).map(a=>draft?.bounced?.[String(a).toLowerCase()]).find(Boolean),moved=!hit&&movedLine(draft,to);el.hidden=!hit&&!moved;el.textContent=hit?t(to.length>1?'An address here bounced on {}':'This address bounced on {}',bounceDay(hit)):moved||''};
const sendRows=rows=>{setHTML($('#send-head'),html`${rows.map(([k,v])=>html`<div><dt>${k}</dt><dd>${v}</dd></div>`)}`)};
const sendBody=(body,signature)=>{const mail=['email','email_demo'].includes(sendDraft?.kind);$('#send-preview').classList.toggle('mail',mail);setHTML($('#send-preview'),html`${draftBody(sendDraft||{},body)}${signature?mail?html`<span class="sig">+ your signature</span>`:html`<span class="sig">\n\n+ your signature</span>`:''}`)};
const sendFine=text=>{$('#send-fine').textContent=text;$('#send-fine').hidden=!text};
let sendFrom=null;
const sendRecipients=()=>[...document.querySelectorAll('#send-recipients input:checked')].map(x=>x.value);
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
const mailModelOf=body=>{const d=document.createElement('div');setHTML(d,mailHtml(body,false));return mailModel(d)};
let mailStart=null;
// fresh: the draft as it stands (an untouched editor sends exactly it); else only the page changes, to show what goes out
function mailLoad(body,fresh=true){const r=mailRich();setHTML(r,mailHtml(body,false));if(fresh)mailStart=mailModel(r);mailTools()}
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
 if(s.isCollapsed)document.execCommand('insertHTML',false,String(html`<a href="${safeHref(u)}">${u}</a>`));else document.execCommand('createLink',false,u);mailTools()}
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
$('#send-cancel').onclick=()=>$('#send-dialog').close();
// A closed send panel keeps nothing: the next one fills it again, and a sent or canceled draft never reads as typing
$('#send-dialog').addEventListener('close',()=>{if($('#send-dialog').open)return;sendBatch=null;if(sendDraft?.compose)sendDraft=null;$('#send-mailapp').hidden=true;$('#send-step').hidden=true;for(const id of ['send-subject','send-body','send-ask-text'])$('#'+id).value='';$('#send-rich-body').replaceChildren();$('#send-error').textContent=''});
// The subject wraps as it grows (field-sizing, or its height here where that's missing) but stays one line of text:
// Enter adds no line break and a pasted one becomes a space.
const subjectFit=()=>{const x=$('#send-subject');if(CSS.supports?.('field-sizing','content')||!x.offsetParent)return;x.style.height='auto';x.style.height=x.scrollHeight+'px'};
$('#send-subject').onkeydown=e=>{if(e.key==='Enter'&&!e.isComposing)e.preventDefault()};
$('#send-subject').oninput=e=>{const x=e.target,v=x.value.replace(/[ \t]*[\r\n]+[ \t]*/g,' ');if(v!==x.value){const at=x.selectionStart-(x.value.length-v.length);x.value=v;x.setSelectionRange(at,at)}subjectFit()};
addEventListener('resize',()=>{if($('#send-dialog').open)subjectFit()});
$('#send-confirm').onclick=async()=>{const b=$('#send-confirm');b.disabled=true;try{
if(sendDraft?.compose){await composeSend(b);return}  // a new email (todos-compose.js, there while it's open)
if(!$('#send-editor').hidden){const mail=sendDraft.kind==='email',typed=$('#send-body').value,body=mail?mailOut(draftText(sendDraft)):typed===plainDraft(draftText(sendDraft))?draftText(sendDraft):unplainDraft(typed,draftText(sendDraft)),subject=['linkedin','slack','x','whatsapp','telegram','signal','intercom','doc_reply','finish'].includes(sendDraft.kind)?undefined:$('#send-subject').value;
if(body==null){b.disabled=false;return}
if(body!==draftText(sendDraft)||subject!==sendDraft.subject){const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'revise_draft',args:{suggestion_id:sendTask,revision:sendRevision,body,subject}})});sendRevision=r.revision;
 // The saved text is what goes out. When saving changed it (a blank line before the name), it shows first and Send waits.
 if(r.body!=null){sendDraft={...sendDraft,revision:r.revision,...(subject===undefined?{}:{subject}),...(sendDraft.kind==='finish'?{[sendDraft.message?'message':'preview']:r.body}:{body:r.body})};
  if(r.body.trim()!==body.trim()){if(mail)mailLoad(r.body);else $('#send-body').value=plainDraft(r.body);$('#send-error').textContent=t('Saved with a small change. Check the message, then send.');b.disabled=false;return}}}}
const extra={...($('#send-recipients').hidden?{}:{recipients:sendRecipients()}),...(sendDraft.kind==='email'&&sendDraft.from_options?.length>1&&sendFrom?{sender:sendFrom}:{})};
// Several: Next keeps this one, the last Send sends each in order
if(sendBatch){const sb=sendBatch,n=sb.list.length;sb.done[sb.at]={...sb.done[sb.at],revision:sendRevision,kind:sendDraft.kind,extra};
 if(sb.at<n-1){sb.at++;openSend(sb.id,sb.list[sb.at],1);if(sendRevision!==sb.list[sb.at]){sendBatch=null;$('#send-dialog').close()}return}
 let went=0;for(const x of sb.done){try{await sendConfirmed(sb.id,x.revision,x.kind,x.extra)}catch(e){if(went)e.message=t('Sent {} of {}. {}',went,n,e.message);throw e}went++}
 sendBatch=null;$('#send-dialog').close();toast(t('Sending your {} approved drafts…',n));await refresh();return}
await sendConfirmed(sendTask,sendRevision,sendDraft.kind,extra);
$('#send-dialog').close();toast(sendDraft.kind==='merge'?'Testing and merging the fix…':sendDraft.kind==='finish'?'On it. I’ll report back.':sendDraft.kind==='calendar'?'Changing the calendar…':sendDraft.kind==='doc_write'?'Writing the doc…':'Sending your approved draft…');await refresh();
}catch(e){errCaught(e);$('#send-error').textContent=e.offline&&!e.slow?t('Offline. Send again when you’re back online.'):e.message;b.disabled=false}};
// The review dialog for it: everything that goes in, then Create or Save. The tap here writes it, once.
function openDocWrite(id,draft){sendTask=id;sendRevision=draft.revision;sendDraft=draft;$('#send-editor').hidden=true;$('#send-edit').hidden=true;
 $('#send-title').textContent=draft.op==='create'?t('Create this doc?'):t('Save these changes?');$('#send-confirm').textContent=draft.op==='create'?t('Create'):t('Save');
 $('#send-preview').classList.remove('code','mail');$('#send-confirm').hidden=false;$('#send-confirm').disabled=false;$('#send-cancel').textContent='Cancel';$('#send-recipients').hidden=true;$('#send-files').hidden=true;$('#send-error').textContent='';
 sendHeader=()=>sendRows(draft.op==='create'?[['Doc',draft.title],['Where',docWhere(draft)+(draft.account_name?' · '+draft.account_name:'')]]:[['Doc',draft.doc_title],['Where',docWhere(draft)],['Changes',String((draft.changes||[]).length)]]);sendHeader();
 $('#send-preview').hidden=false;setHTML($('#send-preview'),html`<div class="dw">${docWriteHtml(draft)}</div>`);
 sendFine(draft.op==='create'?t('Only you can see the new doc until you share it.'):t('Only these changes are made, and only if the doc hasn’t changed since.'));$('#send-dialog').showModal()}
