// What someone typed to send and didn't send yet survives Esc, a closed sheet, another page, a reload and a killed phone
// app (docs/help/email-composer.md; docs/architecture.md, "On the device"). One mechanism for every message: a new email,
// any draft in the send dialog (all channels, its Ask for changes too) and a follow-up edited in its review.
// Every other box people type in to ask or answer keeps its text with it too (todos-kept-box.js).
// - Kept in this browser only, sealed (localCache 'kept'): never sent to the Machine, in a log or the address, gone on
//   sign-out and when someone else signs in. Where nothing can be sealed (a plain http address), only while the page is open.
// - Only what differs from the draft, for 30 days after the last typing. It goes when it's sent or discarded (Undo).
// - It never sends by itself and never replaces a draft that changed meanwhile, nor another tab's: both stay (o), and a
//   line in the dialog switches between them.
// An entry: k (its message), id (the to-do; '' for a new email), rev (the draft's revision it was typed on), at, by (the
// tab), open (its composer was open), v (the fields; null: the draft as it is), o (the other versions), q (only Ask for
// changes), and a new email's to, sub, name and bb (its first text).
const KT_AGE=30*864e5,KT_BACK=18e5,ktTab=Math.random().toString(36).slice(2);
let ktList=[],ktNow=null,ktQueue=[],ktRun=Promise.resolve(),ktIn=false;
const ktSame=(a,b)=>JSON.stringify(a)===JSON.stringify(b),ktGet=k=>ktList.find(e=>e.k===k);
const ktSet=(list,[k,fn])=>{const e=fn(list.find(x=>x.k===k)),rest=list.filter(x=>x.k!==k&&Date.now()-x.at<KT_AGE);return(e?[e,...rest]:rest).slice(0,40)};
const ktChan=localCache.on&&self.BroadcastChannel?new BroadcastChannel('kept'):null;
// Read again before each write, one tab at a time, so two tabs never drop each other's
async function ktSync(write){const hit=await localCache.read('kept'),n=ktQueue.length;
 ktList=(write?ktQueue.splice(0,n):ktQueue).reduce(ktSet,Array.isArray(hit?.value)?hit.value.filter(e=>e?.k&&Date.now()-e.at<KT_AGE):ktList);
 const held=write&&n?await localCache.put('kept',ktList):hit||!ktList.length;if(write&&n)ktChan?.postMessage(0);
 if(held)try{ktList.length?localStorage.kept=1:localStorage.removeItem('kept')}catch{}}
function ktWrite(k,fn){ktList=ktSet(ktList,[k,fn]);if(!localCache.on)return;ktQueue.push([k,fn]);
 ktRun=ktRun.then(()=>ktQueue.length&&(navigator.locks?navigator.locks.request('kept',()=>ktSync(true)):ktSync(true))).catch(()=>{})}
const ktReady=ktSync().then(()=>{ktIn=true;if(!ktList.length)return;ktDraw();ktLive(100);
 // A final step's message opened while this was read: its editor opens too
 if($('#send-dialog').open&&$('#send-editor').hidden&&sendDraft?.kind==='finish'){const s=state.suggestions.find(x=>x.id===sendTask);if(s&&ktFresh(s,sendDraft))editSend()}});
function keptRead(){return ktReady}
const ktLive=n=>{if(state?.suggestions&&!shownCached&&!netDown){ktPrune();ktBack()}else if(n)setTimeout(ktLive,300,n-1)};
if(ktChan)ktChan.onmessage=()=>ktSync().then(ktOther);
// The to-do lists, the chat, the follow-ups' review and Go through, drawn with what is kept now
function ktDraw(){if(!state?.suggestions||$('#send-dialog').open)return;self.ktAsks?.();focusKept(render);if(chatId)paintChat();
 if(fr&&!fr.editing&&$('#fu-review').open)frDraw();if(self.crDraw&&cr)crDraw()}

// The message: its to-do, kind and place among that kind (a draft's revision changes as it's edited), or a new email's address
const ktKey=(s,a)=>s.id+'|'+a.kind+'|'+taskActions(s).filter(x=>x.kind===a.kind).findIndex(x=>x.revision===a.revision);
const ktAct=e=>{const [id,kind,n]=e.k.split('|'),s=state.suggestions?.find(x=>x.id===id);return [s,s&&taskActions(s).filter(x=>x.kind===kind)[n]]};
// Sent from elsewhere (another device, the Machine, or here with the answer lost on the way)
function ktSent(e){if(!e.id)return state.suggestions.some(s=>Date.parse(s.created_at)>e.at&&taskActions(s).some(a=>a.kind==='email'&&a.to?.[0]===e.to&&a.subject===e.v?.s.trim()));
 const [s,a]=ktAct(e),st=a&&(a.state||s.action_status);return /^(sent|done)$/.test(st?.status)&&(a.revision===e.rev||Date.parse(st.sent_at)>e.at)}
const ktPrune=()=>{for(const e of ktList)if(ktSent(e))ktWrite(e.k,()=>null)};
const ktFresh=(s,a)=>{const e=ktList.length&&s.status==='prepared'&&!sendBusy(a.state||s.action_status)&&ktGet(ktKey(s,a));return e&&!e.q&&(e.v||e.o.length)?e:null};

// On a to-do's draft: what is kept on it. keptText: the text itself, when it was typed on the draft as it is now.
function keptMark(s,a){if(!a){a=taskActions(s).find(x=>ktFresh(s,x));if(!a)return ''}const e=ktFresh(s,a);
 return e?html`<p class="draft-why kept-mark"><span>${e.v&&e.rev===a.revision?t('Edited, not sent.'):t('This draft changed. What was typed is kept.')}</span>${ktBtns(e)}</p>`:''}
const ktBtns=e=>html`<button type="button" class="link" data-kept-go="${e.k}">${t('Continue')}</button><button type="button" class="link" data-kept-drop="${e.k}">${t('Discard')}</button>`;
function keptText(s,a){const e=ktFresh(s,a);return e?.v&&e.rev===a.revision?e.v.b:null}
// Above the to-dos: the new emails that weren't sent
function keptRows(){if(!state?.suggestions)return '';ktPrune();
 const rows=ktList.filter(e=>!e.id&&e.v);return rows.length?html`<div class="kept-rows">${rows.map(e=>html`<p class="kept-row"><span>${t('Unsent email to {}',e.name||e.to)}</span>${ktBtns(e)}</p>`)}</div>`:''}

// The send dialog's fields as they are, and put back
const ktVals=()=>({s:$('#send-subject').value,b:sendDraft.kind==='email'?mailBody(mailModel(mailRich())):$('#send-body').value,f:sendDraft.kind==='email'&&sendFrom||'',
 t:$('#send-recipients').hidden?[]:sendRecipients(),a:$('#send-ask-text').value});
function ktFill(v){const d=sendDraft,mail=d.kind==='email';$('#send-subject').value=v.s;mail?mailLoad(v.b,false):$('#send-body').value=v.b;
 if((d.compose?d.from.map(x=>x.from):d.from_options||[]).includes(v.f))sendFrom=v.f;
 const to=[...document.querySelectorAll('#send-recipients input')];if(to.some(x=>v.t.includes(x.value)))for(const x of to)x.checked=v.t.includes(x.value);
 $('#send-ask-text').value=v.a;$('#send-ask').hidden=!v.a;$('#send-act').hidden=!!v.a;sendHeader(false);subjectFit();sendCaptionFit();
 ktNow.v=ktVals();
 // Where they left it: the end of the text
 setTimeout(()=>{const el=mail?mailRich():$('#send-body'),at=document.activeElement;if(at!==el&&!(d.compose&&v.b&&at===$('#send-subject')))return;
  el.focus();mail?getSelection().selectAllChildren(el):el.setSelectionRange(el.value.length,el.value.length);if(mail)getSelection().collapseToEnd()})}
const ktTyped=n=>!ktSame(n.v,n.base);
// The dialog shows a message to edit (editSend): what was typed on it before comes back
function keptOpen(){const d=sendDraft,s=d.compose?null:state.suggestions.find(x=>x.id===sendTask);if(!d.compose&&!s)return;
 const k=d.compose?'new|'+d.to[0]+'|'+d.subject:ktNow?.id===s.id&&ktNow.d===d?ktNow.k:ktKey(s,d);ktLeave();
 const base=ktVals(),n=ktNow={k,d,id:s?.id||'',base,v:base,o:[]};
 navigator.locks?.request('kept:'+k,{mode:'shared'},()=>new Promise(r=>{ktNow===n?n.free=r:r()})).catch(()=>{});
 const show=()=>{if(ktNow!==n)return;const e=ktGet(k);if(e){n.at=e.at;n.o=[...e.o];
   if(e.v)d.compose||e.rev===d.revision?n.typed?n.o.unshift({by:e.by,v:e.v}):ktFill(e.v):n.o.unshift({by:'',v:e.v});
   ktWrite(k,x=>x&&{...x,open:true})}ktShow()};
 ktIn?show():ktReady.then(show)}
// Out of the composer: it stays kept, unless it was sent or discarded
function ktLeave(){const n=ktNow;if(!n)return false;ktNow=null;n.free?.();ktWrite(n.k,x=>x&&{...x,open:false});$('#send-dialog').classList.remove('kept-on');return !!ktGet(n.k)}
// Cancel is Discard while there is something typed, and the line about the other version
function ktShow(){const n=ktNow,on=ktTyped(n),x=n.o[0];$('#send-dialog').classList.toggle('kept-on',on);$('#send-cancel').textContent=on?t('Discard'):t('Cancel');
 let p=$('#kept-note');if(!x){p?.remove();return}if(!p){p=make('p',{id:'kept-note',class:'kept-note',role:'status'});$('.send-top').before(p)}
 const draft=!x.by,back=draft&&ktSame(x.v,n.base);
 setHTML(p,html`<span>${!draft?t('Also edited in another tab.'):back?t('This draft changed. Showing what was typed.'):t('This draft changed. What was typed is kept.')}</span><button type="button" class="link" data-kept-use>${back?t('Show the new draft'):t('Use it')}</button>${back?'':html`<button type="button" class="link" data-kept-lose>${t('Discard')}</button>`}`)}
function ktSave(){const n=ktNow,d=n.d,o=n.o.filter(x=>!ktSame(x.v,n.base)),v=ktTyped(n)?n.v:null,seen=n.at,at=n.at=Date.now();
 ktWrite(n.k,x=>{const more=x?.v&&x.by!==ktTab&&x.at!==seen&&!ktSame(x.v,v)&&!o.some(y=>ktSame(y.v,x.v))?[{by:x.by,v:x.v}]:[];
  return v||o.length||more.length?{k:n.k,id:n.id,rev:d.revision||'',at,by:ktTab,open:true,v,o:[...o,...more],q:!!v&&ktSame({...v,a:''},{...n.base,a:''}),
   ...(d.compose?{to:d.to[0],sub:d.subject,name:d.to_name,bb:d.body}:{})}:null})}
function ktType(){const n=ktNow;if(!n||sendDraft!==n.d||!$('#send-dialog').open||$('#send-editor').hidden)return;const v=ktVals();if(ktSame(v,n.v))return;n.v=v;n.typed=true;ktSave();ktShow()}
// Another tab kept or dropped something: an untouched composer follows it, one typed in keeps both
function ktOther(){const n=ktNow,e=n&&ktGet(n.k);if(e?.v&&e.by!==ktTab&&e.at!==n.at&&!ktSame(e.v,n.v)){
  if(n.typed)n.o=[...n.o.filter(x=>x.by!==e.by),{by:e.by,v:e.v}];else if(n.d.compose||e.rev===n.d.revision){ktFill(e.v);n.at=e.at}ktShow()}
 ktDraw()}
// Sent (its to-do and revision), or saved on the Machine as a new revision (nothing given): no longer kept here
function keptGone(id,rev){const n=ktNow;if(id){for(const e of ktList)if(e.id===id&&(e.rev===rev||ktAct(e)[1]?.revision===rev))ktWrite(e.k,()=>null);if(n?.d.revision===rev)ktLeave();return}
 if(!n)return;ktWrite(n.k,()=>null);if(sendDraft.compose){ktLeave();return}
 const {body,subject,message,preview}=sendDraft;const a=ktAct(n)[1];if(a)Object.assign(a,JSON.parse(JSON.stringify({revision:sendRevision,body,subject,message,preview})));
 setTimeout(()=>{if(ktNow!==n)return;n.d=sendDraft;n.base=n.v=ktVals();n.o=[];n.typed=false;ktShow()})}

// Discard, with Undo; then(e) runs on Undo
function ktTell(text,label,fn){toast(text);const b=make('button',{type:'button'},label);b.onclick=()=>{$('#toast').classList.remove('show');fn()};
 $('#toast').append(' ',b);clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),15000)}
function ktDrop(k,left,then){const e=ktGet(k);ktWrite(k,()=>left||null);e?ktTell(t('Discarded.'),t('Undo'),()=>{ktWrite(k,()=>({...e,open:false}));ktDraw();then?.(e)}):toast(t('Discarded.'))}
// Back in its composer. A new email without a mailbox that can send now opens in the mail app, as it does from its address.
function ktGo(e,quiet){if(e.id){const [s,a]=ktAct(e);if(a)openSend(s.id,a.revision);return}
 const q=[['subject',e.v.s.trim()],['body',e.v.b]].filter(x=>x[1]).map(x=>x[0]+'='+encodeURIComponent(x[1])).join('&');
 lazyRun('compose',()=>openCompose(e.to,e.sub,quiet?'':'mailto:'+encodeURIComponent(e.to).replace(/%40/g,'@')+(q&&'?'+q),e.bb))}
// The page went away with a composer open (a reload, the phone app killed): it opens again as it was, once the Machine
// answers, unless the owner is on to something else or another tab has it open
function ktBack(){if(self.COMPACT)return;const e=ktList.find(x=>x.open&&x.v&&Date.now()-x.at<KT_BACK);if(!e)return;
 (navigator.locks?.query?.()||Promise.resolve({held:[]})).then(q=>{if(q.held.some(l=>l.name==='kept:'+e.k)||location.hash&&!/^#(chat|card)=/.test(location.hash)||modalOpen()||document.activeElement?.matches('input,textarea'))return;ktGo(e,true)},()=>{})}

document.addEventListener('input',e=>{const x=e.target;if(x.closest?.('#send-dialog'))ktType();
 // A follow-up edited in its review: the same entry as its send dialog's
 else if(x.dataset?.frText){const s=state.suggestions.find(y=>y.id===x.dataset.frText),a=s&&frDraft(s);if(!a)return;const mail=a.kind==='email',same=x.value===plainDraft(draftText(a));
  ktWrite(ktKey(s,a),old=>{const o=old?old.rev!==a.revision&&old.v?[{by:'',v:old.v},...old.o]:old.o:[],v=same?null:{s:a.subject||'',f:'',t:[],a:'',...(old?.rev===a.revision?old.v:{}),b:mail?unplainDraft(x.value,draftText(a)):x.value};
   return v||o.length?{k:ktKey(s,a),id:s.id,rev:a.revision,at:Date.now(),by:ktTab,open:false,v,o}:null});
  const b=document.querySelector('[data-fr-cancel]');if(b)b.textContent=same?t('Cancel'):t('Discard')}});
// From, To and the formatting tools change without typing
for(const ev of ['click','keyup']){addEventListener(ev,ktType);document.addEventListener(ev,()=>{if(ktNow)setTimeout(ktType)},true)}
document.addEventListener('close',e=>{if(e.target.id!=='send-dialog'||e.target.open||!ktNow)return;if(ktLeave())toast(t('Kept, not sent.'));ktDraw()},true);
document.addEventListener('click',e=>{const b=e.target.closest?.('[data-kept-go],[data-kept-drop],[data-kept-use],[data-kept-lose],[data-fr-cancel],#send-cancel');if(!b)return;const n=ktNow;
 if(b.id==='send-cancel'){if(n&&ktTyped(n)){const o=n.o.filter(x=>!ktSame(x.v,n.base));n.free?.();ktNow=null;
   ktDrop(n.k,o.length?{...ktGet(n.k),open:false,v:o[0].v,o:o.slice(1),...(o[0].by?{}:{rev:''})}:null,ktGo)}return}
 if(b.dataset.frCancel!=null){const s=state.suggestions.find(x=>x.id===fr?.editing),a=s&&frDraft(s);if(a&&keptText(s,a)!=null)ktDrop(ktKey(s,a));return}
 e.preventDefault();e.stopPropagation();
 if(b.dataset.keptUse!=null){const x=n.o.shift(),v=ktVals();if(!x.by||!ktSame(v,n.base))n.o.push({by:x.by,v});n.typed=true;ktFill(x.v);ktSave();ktShow()}
 else if(b.dataset.keptLose!=null){n.o.shift();ktSave();ktShow()}
 else if(b.dataset.keptDrop){ktDrop(b.dataset.keptDrop);ktDraw()}
 else{const x=ktGet(b.dataset.keptGo),a=x&&ktAct(x)[1];if(!x)return;
  if(fr&&a&&x.rev===a.revision){fr.editing=fr.cur=x.id;frDraw(true);return}$('#fu-review').close();ktGo(x)}},true);
lazyPart('keptbox').catch(()=>{});
