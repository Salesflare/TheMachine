// New email (docs/help/email-composer.md): a click on an email address (todos-list.js composeLink) opens the send dialog
// every draft uses, empty, to that address, ready to write: From, To, Subject and the message with its formatting tools.
// From offers the owner's mailboxes that can send (and Gmail's confirmed aliases), the one for the person's area first
// (compose_from: Work for a work contact). Nothing goes out until Send: that makes the email a draft on a to-do of its own
// (compose_email) and sends exactly that revision (sendConfirmed, Store.confirm_action), so it goes out, shows and settles
// like any sent draft. Without a mailbox that can send, the address opens the mail app as before; Open in email in the
// composer does too, with what was typed. body: a draft to start from (a subscription's Cancel, todos-subs.js), sent only
// on the owner's Send like any other.
let composeBusy=false;
async function openCompose(to,subject,href,body){if(composeBusy)return;composeBusy=true;let r=null;
 try{r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'compose_from',args:{to}})})}
 catch(e){errCaught(e)}finally{composeBusy=false}
 if(!r?.from?.length){location.href=href;return}
 if($('#send-dialog').open)$('#send-dialog').close();
 sendBatch=null;sendTask=null;sendRevision=null;sendDraft={kind:'email',compose:true,to:[to],to_name:r.to_name||'',subject:subject||'',body:body||'',from:r.from};
 sendFrom=r.from.some(c=>c.from===r.default)?r.default:r.from[0].from;
 for(const id of ['send-step','send-recipients','send-bounce','send-files','send-ask','send-ask-open','send-edit','send-subject-label'])$('#'+id).hidden=id!=='send-subject-label';
 $('#send-title').textContent=t('New email');$('#send-act').hidden=false;$('#send-confirm').hidden=false;$('#send-confirm').disabled=false;$('#send-confirm').textContent=t('Send now');
 $('#send-cancel').textContent=t('Cancel');$('#send-error').textContent='';$('#send-preview').classList.remove('code');sendFine('');
 $('#send-mailapp').hidden=false;sendHeader=composeHead;$('#send-dialog').showModal();editSend(false);
 (subject?mailRich():$('#send-subject')).focus()}
// From (a picker with more than one address, grouped by area when there are several) and To, as on a to-do's email
function composeHead(){const d=sendDraft;if(!d?.compose)return;const froms=d.from,areas=new Set(froms.map(c=>c.area)).size>1;
 sendRows([['From',sendFrom],['To',d.to_name?d.to_name+' <'+d.to[0]+'>':d.to[0]]]);
 if(froms.length<2)return;
 cmLists.from={label:t('Send from'),choices:()=>froms.map(c=>({value:c.from,label:c.from,name:true,...(areas&&c.area?{group:c.area}:{})})),value:()=>sendFrom,
  pick:v=>{sendFrom=v;const s=$('#send-from>span');if(s)s.textContent=v}};
 setHTML($('#send-head dd'),cmTrigger('from','from',sendFrom,'from-pick',html` id="send-from" translate="no"`))}
// Send: the subject and the message first; then the draft on its to-do, and that exact revision confirmed. When the
// confirm doesn't go through, the email waits on its to-do, ready to send from there.
async function composeSend(b){const d=sendDraft,subject=$('#send-subject').value.trim(),body=mailOut(d.body);
 if(body==null){b.disabled=false;return}
 const miss=!subject?t('Add a subject first.'):!body.trim()?t('Write the message first.'):'';
 if(miss){$('#send-error').textContent=miss;(subject?mailRich():$('#send-subject')).focus();b.disabled=false;return}
 const pick=d.from.find(c=>c.from===sendFrom)||d.from[0];
 const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'compose_email',args:{to:d.to[0],account_id:pick.account_id,subject,body}})});
 try{await sendConfirmed(r.suggestion_id,r.revision,'email',(r.from_options||[]).length>1?{sender:pick.from}:{})}
 catch(e){errCaught(e);$('#send-dialog').close();toastOpen(t('Not sent. The email waits in a to-do.'),r.suggestion_id);await refresh();return}
 $('#send-dialog').close();toast(t('Sending your email…'));await refresh()}
// Open in email: the address's own mailto, with the subject and the text typed so far
$('#send-mailapp a').addEventListener('click',e=>{const d=sendDraft;if(!d?.compose)return;e.preventDefault();
 const q=[['subject',$('#send-subject').value.trim()],['body',mailRich().innerText.trim()]].filter(x=>x[1]).map(([k,v])=>k+'='+encodeURIComponent(v)).join('&');
 const href='mailto:'+encodeURIComponent(d.to[0]).replace(/%40/g,'@')+(q?'?'+q:'');$('#send-dialog').close();location.href=href});
