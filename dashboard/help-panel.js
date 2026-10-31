// Help (help_chat.py, docs/help/help-chat.md): ask how The Machine works. It answers from the help pages first and the
// app's own code second, on this Machine's own model, and changes nothing. Report a bug shows the description, the
// screenshot and the scrubbed support report exactly as they go, and sends them only on Send: a hosted Machine to its
// account (/_machine/bug, with the owner's sign-in there), a self-hosted one paired with the Network through its app
// (bug_send). Settings, Security, Support access: the owner lets The Machine team read logs and settings, read-only,
// for 24 hours, and sees every time they did. Hosted through /_machine/support-access with the owner's sign-in there; a
// self-hosted one paired with the Network through its app (support_access, fleet.Fleet.support_access), hidden when it isn't.
// The markup in its own function, so the string check (scripts/i18n_extract.py, area help) reads it
function helpMarkup(){return `<div class="snooze-heading"><h2 id="help-title">Help</h2><button type="button" data-help-close aria-label="Close">×</button></div>
<div class="sub-tabs" role="tablist" aria-label="Help"><button type="button" role="tab" data-help-tab="ask" aria-selected="true">Ask</button><button type="button" role="tab" data-help-tab="bug" aria-selected="false">Report a bug</button></div>
<div id="help-ask-pane"><div class="help-log" id="help-log" aria-live="polite"></div>
<form class="help-ask" id="help-form" novalidate><div class="chat-box"><textarea id="help-q" rows="1" maxlength="600" enterkeyhint="send"></textarea><div class="chat-tools">${micBtn()}<button class="chat-send" id="help-go" aria-label="Ask" title="Ask" disabled>${SEND}</button></div></div><div class="chat-model" id="help-model"></div></form>
<p class="help-foot"><span>It can’t see or change your data.</span><a href="https://themachine.computer/help" target="_blank" rel="noopener">All help pages</a></p></div>
<div id="help-read-pane" hidden><div class="help-read-head"><button type="button" class="link" data-help-back><span aria-hidden="true">← </span>Back</button><a id="help-read-site" href="https://themachine.computer/help" target="_blank" rel="noopener">Open on the site</a></div><article id="help-read" class="help-read" translate="no" tabindex="-1"></article></div>
<div id="help-bug-pane" hidden><form id="bug-form" novalidate><label>What went wrong?<textarea id="bug-what" rows="4" maxlength="4000"></textarea></label>
<div class="bug-shot"><button type="button" class="chat-say" id="bug-shot-take" hidden>Take a screenshot</button><button type="button" class="chat-say" id="bug-shot-pick">Attach an image</button><input type="file" id="bug-shot-file" accept="image/png,image/jpeg,image/webp" hidden><img id="bug-shot-img" alt="Screenshot to send" hidden><button type="button" class="chat-say" id="bug-shot-remove" hidden>Remove</button></div>
<label class="bug-check"><input type="checkbox" id="bug-diag" checked> Include a support report</label><p class="fine" id="bug-diag-fine">Versions, checks, recent errors and read-only logs for 24 hours. No messages, keys or addresses.</p>
<p id="bug-error" role="status"></p><div class="actions"><button class="primary" id="bug-send">Send</button></div><div id="bug-queued" class="bug-sent" hidden></div></form></div>`}
const helpBox=document.createElement('dialog');helpBox.id='help-panel';helpBox.setAttribute('aria-labelledby','help-title');
helpBox.innerHTML=helpMarkup();
document.body.append(helpBox);
const helpChat=[];let helpBusy=false,bugShot=null,helpModel=null;  // helpModel: a model or thinking level picked for this Help chat
const HELP_SRC=/^https:\/\/(themachine\.computer\/help\/|github\.com\/Salesflare\/TheMachine\/blob\/)/;
// Why two people look like one (graph.py likely_same): its parts, each in the language
const sameWhy=w=>String(w||'').split(', ').map(x=>{const m=/^both at (.+)$/.exec(x);return m?t('both at {}',m[1]):t(x)}).join(', ');
function helpTab(t){for(const b of helpBox.querySelectorAll('[data-help-tab]'))b.setAttribute('aria-selected',String(b.dataset.helpTab===t||t==='read'&&b.dataset.helpTab==='ask'));$('#help-ask-pane').hidden=t!=='ask';$('#help-bug-pane').hidden=t!=='bug';$('#help-read-pane').hidden=t!=='read'}
// A help article in the app's language (docs/help/<language>/, the English one until it is translated): its own light
// markdown (## and ### headings with the site's anchors, paragraphs, - and 1. lists, **bold**, `code`, links). A link to
// another article opens here too; any other link opens in a new tab.
const HELP_PAGE=/^https:\/\/themachine\.computer\/help\/([a-z0-9-]+)\/?(?:#([a-z0-9-]+))?$/;
function helpDoc(a){const ids=[...(a.anchors||[])];
 const inline=s=>esc(s).replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\*\*(.+?)\*\*/g,'<b>$1</b>')
  .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g,(m,label,href)=>{const md=/^([a-z0-9-]+)\.md(?:#([a-z0-9-]+))?$/.exec(href);
   return md?`<a href="${HELP}${md[1]}${md[2]?'#'+md[2]:''}" data-help-slug="${md[1]}" data-help-anchor="${md[2]||''}">${label}</a>`
    :/^(https:|mailto:)/.test(href.replace(/&amp;/g,'&'))?`<a href="${href}" target="_blank" rel="noopener">${label}</a>`:label});
 const out=[`<h3>${esc(a.title)}</h3>`,a.summary?`<p class="help-sum">${inline(a.summary)}</p>`:''];let list=null,para=[],code=null;
 const flush=()=>{if(para.length)out.push(`<p>${para.map(inline).join(' ')}</p>`);para=[];if(list)out.push(`<${list.tag}>${list.items.map(i=>`<li>${inline(i)}</li>`).join('')}</${list.tag}>`);list=null};
 for(const line of String(a.body||'').split('\n')){
  if(code){if(/^```/.test(line)){out.push(`<pre>${esc(code.join('\n'))}</pre>`);code=null}else code.push(line);continue}
  if(/^```/.test(line)){flush();code=[];continue}
  const h=/^(#{2,3}) (.+)$/.exec(line),b=/^\s*[-*] (.*)$/.exec(line),n=/^\s*\d+\. (.*)$/.exec(line);
  if(h){flush();out.push(`<h${h[1].length+2} id="help-a-${esc(ids.shift()||'')}">${inline(h[2])}</h${h[1].length+2}>`);continue}
  if(!line.trim()){flush();continue}
  if(b||n){const tag=b?'ul':'ol';if(para.length||list&&list.tag!==tag)flush();list??={tag,items:[]};list.items.push((b||n)[1]);continue}
  if(list&&/^\s+\S/.test(line)){list.items[list.items.length-1]+=' '+line.trim();continue}
  if(list)flush();para.push(line.trim())}
 if(code)out.push(`<pre>${esc(code.join('\n'))}</pre>`);flush();return out.join('')}
async function helpArticle(slug,anchor=''){helpTab('read');if(!helpBox.open)helpBox.showModal();const box=$('#help-read');box.innerHTML=`<p class="help-intro">${esc(t('Opening…'))}</p>`;$('#help-read-site').href=HELP+slug+(anchor?'#'+anchor:'');
 try{const a=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'help_article',args:{slug}})});
  box.innerHTML=helpDoc(a);const to=anchor&&box.querySelector('#help-a-'+CSS.escape(anchor));box.scrollTop=to?to.offsetTop-box.offsetTop:0;box.focus({preventScroll:true})}
 catch(err){errCaught(err);box.innerHTML=`<p class="help-intro">${esc(err.message||t('That help page doesn’t exist.'))}</p>`}}
// In another language than English, a link to a help page anywhere in the app opens it here, in that language; the
// site's pages are in English. A click with a modifier key still opens the site.
document.addEventListener('click',e=>{const a=e.target.closest('a[href]');if(!a||e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
 const m=HELP_PAGE.exec(a.href);if(!m||(I18N.lang||'en')==='en'&&!a.dataset.helpSlug)return;e.preventDefault();helpArticle(m[1],m[2]||'')});
function helpOpen(t='ask',about=''){helpTab(t);{const q=$('#help-q'),w=$('#bug-what');q.placeholder=window.t('How do I snooze a to-do?');q.ariaLabel=window.t('Your question');w.placeholder=window.t('What you did, what you expected, what happened')}  /* text areas: the page's translation leaves them alone */if(t==='bug')bugReset(about);else{helpRender();cmPaint('help')}if(!helpBox.open)helpBox.showModal();(t==='ask'?$('#help-q'):$('#bug-what')).focus();ncKeyboard()}
$('#open-help').onclick=()=>helpOpen();
helpBox.addEventListener('click',e=>{if(e.target.closest('[data-help-back]')){helpOpen('ask');return}const t=e.target.closest('[data-help-tab]');if(t){helpOpen(t.dataset.helpTab);return}const r=e.target.closest('[data-help-bug]');if(r){helpReport(helpChat[+r.dataset.helpBug]?.bug);return}if(e.target.closest('[data-help-close]'))helpBox.close()});
document.addEventListener('click',e=>{if(!e.target.closest('#toast [data-bug-report]'))return;const t=$('#toast'),said=(t.firstChild?.nodeType===3?t.firstChild.textContent:'').trim();t.classList.remove('show');helpOpen('bug',said)});
// The answer as the card chat shows it: markdown, with links only to the help pages and the app's code (any other link
// keeps its words). The thread is what people wrote, so the page's translation leaves it alone (translate="no").
const helpMarkdown=v=>chatMarkdown(String(v||'').replace(TEXT_LINK,(m,label,url)=>url&&!HELP_SRC.test(url)?label:m));
function helpRender(){const log=$('#help-log'),src=m=>(m.sources||[]).filter(s=>HELP_SRC.test(s.url));
 const shares=state.team_learnings?.network&&state.team_learnings?.help_topics!==false;  // Settings, Share what Help is asked
 log.innerHTML=(helpChat.length?'':'<p class="help-intro">Ask how anything in The Machine works. Answers come from the help pages, with links.</p>'+(shares?'<p class="help-intro help-topics">Only the topic of each question goes to The Machine team, never your words.</p>':''))+helpChat.map((m,i)=>m.role==='user'
  ?`<div class="chat-msg you"><div class="bubble" translate="no">${esc(m.text)}</div></div>`
  :m.busy?`<div class="chat-msg machine"><div class="bubble typing" role="status" aria-label="Looking it up…"><i></i><i></i><i></i></div></div>`
  :`<div class="chat-msg machine${m.error?' err':''}"><div class="bubble" translate="no">${m.error?esc(m.text):helpMarkdown(m.text)}</div>${src(m).length?`<div class="chat-files">${src(m).map(s=>`<a class="agent-file" href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.kind==='code'?t('Code: {}',s.title):s.title)}</a>`).join('')}</div>`:''}${m.bug?`<div class="chat-options"><button type="button" class="ghost" data-help-bug="${i}">Report this bug</button></div>`:''}</div>`).join('');
 log.scrollTop=log.scrollHeight}
// When Help judged the question describes a bug (help_chat.split_bug): Report a bug, prefilled with its write-up and the
// support report ticked, to edit there. It goes only through Review and Send, as any report. A text the owner already
// wrote there stays, with the write-up under it.
let helpDraft='';
function helpReport(draft){if(!draft)return;const w=$('#bug-what'),cur=w.value.trim();
 helpOpen('bug');w.value=!cur||cur===helpDraft?draft:cur+'\n\n'+draft;helpDraft=draft;$('#bug-diag').checked=true;w.style.height='';w.style.height=Math.min(200,Math.max(104,w.scrollHeight+4))+'px';w.setSelectionRange(0,0);w.scrollTop=0}  // the whole write-up in view
const helpGrow=()=>{const q=$('#help-q');q.style.height='34px';q.style.height=Math.min(140,Math.max(34,q.scrollHeight))+'px';$('#help-go').disabled=!q.value.trim()};
// A question asked while Help still answers shows as sent and waits its turn: one answer at a time, in order, each
// with the answers before it as its history.
const helpQueue=[];
$('#help-form').onsubmit=e=>{e.preventDefault();const q=$('#help-q').value.trim();if(!q)return;
 const asked={role:'user',text:q};helpChat.push(asked);helpQueue.push(asked);$('#help-q').value='';helpGrow();helpRender();if(!helpBusy)helpNext()};
async function helpNext(){const asked=helpQueue.shift();if(!asked)return;helpBusy=true;
 const at=helpChat.indexOf(asked),history=helpChat.slice(0,at).filter(m=>!m.busy&&!m.error).slice(-4).map(m=>({role:m.role,text:m.text})),wait={role:'assistant',text:'Looking it up…',busy:true};
 helpChat.splice(at+1,0,wait);helpRender();
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'help_ask',args:{question:asked.text,history,...(helpModel||{})}})});Object.assign(wait,{text:r.answer,sources:r.sources||[],bug:typeof r.bug==='string'&&r.bug.trim()?r.bug.trim():null,busy:false})}
 catch(err){errCaught(err);Object.assign(wait,{text:err.message||t('Help can’t answer right now.'),busy:false,error:true})}
 finally{helpBusy=false;helpGrow();helpRender();if(helpQueue.length)helpNext();else if(helpBox.open)$('#help-q').focus()}}
$('#help-q').addEventListener('input',helpGrow);
$('#help-q').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();$('#help-form').requestSubmit()}});
function bugReset(about){$('#bug-error').textContent='';if(!$('#bug-what').value.trim())$('#bug-diag').checked=true;  // a new report: the support report is in by default

 if(about&&!$('#bug-what').value.trim())$('#bug-what').value=`The dashboard said: “${about}”\n\n`;
 $('#bug-shot-take').hidden=!navigator.mediaDevices?.getDisplayMedia||matchMedia('(pointer:coarse)').matches;bugShotShow();bugQueuedLoad();bugDiagFine();supportAccessLoad(true).then(bugDiagFine)}
function bugShotShow(){const img=$('#bug-shot-img');img.hidden=!bugShot;if(bugShot)img.src=bugShot;else img.removeAttribute('src');$('#bug-shot-remove').hidden=!bugShot}
async function bugShrink(src){const img=new Image();img.src=src;await img.decode();const k=Math.min(1,1600/img.naturalWidth),c=document.createElement('canvas');  // a JPEG at most 1600 px wide
 c.width=Math.round(img.naturalWidth*k);c.height=Math.round(img.naturalHeight*k);c.getContext('2d').drawImage(img,0,0,c.width,c.height);return c.toDataURL('image/jpeg',.82)}
$('#bug-shot-pick').onclick=()=>$('#bug-shot-file').click();
$('#bug-shot-file').onchange=async e=>{const f=e.target.files[0];e.target.value='';if(!f)return;$('#bug-error').textContent='';if(f.size>20e6){$('#bug-error').textContent='That image is too big.';return}
 try{const url=await new Promise((ok,no)=>{const r=new FileReader();r.onload=()=>ok(r.result);r.onerror=no;r.readAsDataURL(f)});bugShot=await bugShrink(url)}catch{$('#bug-error').textContent='That image can’t be read.'}bugShotShow()};  // a data: URL: the page's CSP allows no blob: images
// The dashboard as it is behind Help: the browser asks which tab to share, one frame is kept, and sharing stops at once.
$('#bug-shot-take').onclick=async()=>{let stream;helpBox.close();
 try{stream=await navigator.mediaDevices.getDisplayMedia({video:{displaySurface:'browser'},preferCurrentTab:true,selfBrowserSurface:'include',audio:false});
  const v=document.createElement('video');v.muted=true;v.srcObject=stream;await v.play();await new Promise(r=>setTimeout(r,400));
  const c=document.createElement('canvas');c.width=v.videoWidth;c.height=v.videoHeight;c.getContext('2d').drawImage(v,0,0);bugShot=await bugShrink(c.toDataURL('image/png'))}
 catch{}finally{stream?.getTracks().forEach(t=>t.stop());helpBox.showModal();bugShotShow()}};
$('#bug-shot-remove').onclick=()=>{bugShot=null;bugShotShow()};
const bugHosted=()=>!!state.manage_url;
// Send: what the owner wrote goes at once and the form closes. With Include a support report ticked (one box, the
// owner's consent to both) the Machine adds the scrubbed support report (support.report, built side by side within a
// time budget) and Support access turns on for 24 hours; unticked, neither. The report is kept before anything goes,
// so a slow or failed support report never loses it: a self-hosted Machine keeps it (bug_queue.py) and its worker
// builds the support report and sends; a hosted dashboard keeps it on this device (bug-later) until it is out.
$('#bug-form').onsubmit=async e=>{e.preventDefault();const out=$('#bug-error'),w=$('#bug-what'),text=w.value.trim();out.textContent='';if(!text){out.textContent='Say what went wrong first.';w.focus();return}
 if(!bugHosted()&&!state.fleet){out.innerHTML='This Machine isn’t linked to an account. Email <a href="mailto:support@themachine.computer">support@themachine.computer</a>, with a file from <code>assistant support-bundle</code> if you like.';return}
 const body={description:text,screenshot:bugShot},diag=$('#bug-diag').checked,access=diag&&saCan()&&!saOn(),shot=bugShot;
 helpBox.close();w.value='';w.style.height='';bugShot=null;bugShotShow();
 try{const r=bugHosted()?await bugHostedKeep(body,diag):await bugAction('bug_send',{...body,diagnostics:diag});  // access only once the report is in hand
  const on=access?await supportAccessSet(true).then(()=>saOn(),()=>{toast('Support access didn’t turn on. Report it again with the box ticked.',true);return null}):false;if(on===null)return;
  toast(r?.queued?t('Saved. It goes out by itself at {}.',fmtHM(r.at*1000)):r?.sending?t('Saved. Sending…'):t('Sent, thanks. You’ll see it here when it’s fixed.'));
  if(r?.completed)r.completed.then(({sent,error})=>{if(error)bugUndo(text,shot,diag,error.message);else toast(sent?.queued?t('Saved. It goes out by itself at {}.',fmtHM(sent.at*1000)):t('Sent, thanks. You’ll see it here when it’s fixed.'))});
  if(on)$('#toast').insertAdjacentHTML('beforeend',`<small class="toast-fine">${esc(t('Support can look until {}.',fmtDHM(saData.until,{weekday:'short',month:'short',day:'numeric'})))}</small>`);clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),6000)}
 catch(err){errCaught(err);bugUndo(text,shot,diag,err.message)}};
// A report that didn't go: back in the form, as it was, with why
function bugUndo(text,shot,diag,why){helpOpen('bug');const w=$('#bug-what');if(!w.value.trim())w.value=text;if(!bugShot){bugShot=shot;bugShotShow()}$('#bug-diag').checked=diag;$('#bug-error').textContent=why||'The report didn’t go out. Email support@themachine.computer.'}
// The fine print says what the box gives: the 24 hours only where Support access can turn on and isn't on already
const bugDiagFine=()=>{$('#bug-diag-fine').textContent=t(saCan()&&!saOn()?'Versions, checks, recent errors and read-only logs for 24 hours. No messages, keys or addresses.':'Versions, checks and recent errors. No messages, keys or addresses.')};
// A report the control plane can't take now (its limit, 5xx, offline) is never lost: the Machine keeps it and sends it
// by itself when it is due (bug_queue.py). A hosted dashboard hands it over (bug_later) with the control plane's
// Retry-After; a hosted Machine outside the Network can't send it itself, so this page keeps it and sends it while open.
const bugAction=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf,'X-Upload':'bug-report'},body:JSON.stringify({action,args})});
// The support report from the Machine, at most REPORT_WAIT ms: without it, what the owner wrote still goes, with why
const REPORT_WAIT=30000;
async function bugReportBuilt(){try{const found=await Promise.race([request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'bug_preview',args:{}})}),new Promise((_,no)=>setTimeout(()=>no(Error('timeout')),REPORT_WAIT))]);return {parts:found.parts,settings:found.settings}}
 catch(err){errCaught(err);return {parts:{report:[err.message==='timeout'?'not ready in time':'not built']}}}}
async function bugPost(body){let r=null,d={};
 try{r=await fetch('/_machine/bug',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),credentials:'same-origin',redirect:'manual'});try{d=await r.json()}catch{}}catch{}
 if(r?.ok)return {sent:true};
 if(r&&r.status&&r.status!==429&&r.status<500)throw Error(d.error||'The report didn’t go out. Email support@themachine.computer.');
 return {wait:Math.max(60,+(r?.headers.get('retry-after')||d.retry_after||0))}}
let bugPage=[];try{bugPage=JSON.parse(localStorage.getItem('bug-later')||'[]')}catch{}
const bugPageKeep=()=>{try{localStorage.setItem('bug-later',JSON.stringify(bugPage,(k,v)=>k==='busy'?undefined:v))}catch{}};  // a full storage keeps it for this visit only
async function bugPageFlush(){for(const q of bugPage.filter(q=>!q.busy&&q.next_at*1000<=Date.now())){let r;q.busy=true;try{await bugPageReport(q);r=await bugPost(q.body)}catch{r={sent:true}}finally{q.busy=false}  // refused for good: dropped
  if(r.sent)bugPage=bugPage.filter(x=>x!==q);else{q.tries=(q.tries||0)+1;q.next_at=Math.floor(Date.now()/1000)+Math.max(r.wait,Math.min(3600,60*2**q.tries));break}}
 bugPageKeep()}
if(bugPage.length&&bugHosted())bugPageFlush();setInterval(()=>{if(bugPage.length&&bugHosted())bugPageFlush()},30000);
const bugPageReport=async q=>{if(!q.diag)return;q.body={...q.body,report:await bugReportBuilt()};delete q.diag;bugPageKeep()};
const bugPageDrop=q=>{bugPage=bugPage.filter(x=>x!==q);bugPageKeep()};
// Kept on this device first, then (not awaited by the form) the support report and the control plane; a report that
// can't go now goes to the Machine (bug_later) or stays here, and one refused for good comes back to the form
async function bugHostedKeep(body,diag){const q={id:'p'+Date.now(),body,...(diag?{diag:true}:{}),next_at:Math.floor(Date.now()/1000)};bugPage.push(q);bugPageKeep();
 const completed=bugHostedGo(q).then(sent=>({sent}),error=>({error}));return {sending:true,completed}}
async function bugHostedGo(q){q.busy=true;let r;
 try{await bugPageReport(q);r=await bugPost(q.body)}catch(err){bugPageDrop(q);throw err}finally{q.busy=false}
 if(r.sent){bugPageDrop(q);return r}
 try{const later=await bugAction('bug_later',{...q.body,retry_after:r.wait});bugPageDrop(q);bugQueuedLoad();return later}
 catch{q.next_at=Math.floor(Date.now()/1000)+r.wait;bugPageKeep();return {queued:true,at:q.next_at}}}
function bugQueuedShow(list){list=[...(list||[]),...bugPage.map(q=>({what:q.body.description.slice(0,80),next_at:q.next_at}))];const el=$('#bug-queued');el.hidden=!list.length;
 el.innerHTML=list?.length?`<h3>Waiting to go out</h3><ul class="bug-parts">${list.map(q=>`<li><span translate="no">${esc(q.what)}</span> · ${esc(t('Goes out at {}',fmtHM(q.next_at*1000)))}</li>`).join('')}</ul>`:''}
async function bugQueuedLoad(){try{bugQueuedShow((await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'bug_queued',args:{}})})).queued)}catch{bugQueuedShow([])}}
SETTINGS_OF['settings-support']='security';
{const d=document.createElement('div');d.id='settings-support';d.hidden=true;
 d.innerHTML=`<div class="section-head"><h2>Support access</h2><p>Let The Machine team read this Machine’s logs and settings to fix a problem. Read-only, never your messages or keys. <a class="learn" href="https://themachine.computer/help/get-support#support-access" target="_blank" rel="noopener">Learn more</a></p></div><div class="list settings-list"><div><span class="grow"><strong id="sa-state">Off</strong><small id="sa-note">Ends by itself after 24 hours.</small></span><button type="button" class="ghost" id="sa-toggle">Allow for 24 hours</button></div></div><p class="sa-log"><button type="button" class="link" id="sa-activity">See each look in Activity</button></p>`;
 $('#settings-share').after(d)}
let saAt=0,saData=null,saShown=false;
// A self-hosted Machine paired with the Network (status fleet) asks its app; if it isn't paired after all, it answers with an error (4xx) and the section stays hidden
const saLocal=allow=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'support_access',args:allow===undefined?{}:{allow}})});
async function supportAccessLoad(force){if(!bugHosted()&&!state.fleet){saShown=false;$('#settings-support').hidden=true;return}if(!force&&Date.now()-saAt<30000)return;saAt=Date.now();
 try{if(bugHosted()){const r=await fetch('/_machine/support-access',{credentials:'same-origin',redirect:'manual'});if(!r.ok)throw Error();saData=await r.json()}else saData=await saLocal();saShown=true}
 catch(e){errCaught(e);saData={error:true};if(!bugHosted()&&e.status>=400&&e.status<500)saShown=false}supportAccessRender()}
// Support access is given where it's needed, with the support report in Report a bug; Settings shows it only while it's on, to end it.
// Each look (and each one refused) is a line in Settings, Activity (settings-activity.js), under Support access.
const saOn=()=>!!saData?.until&&new Date(saData.until)>new Date(),saCan=()=>(bugHosted()||saShown)&&!saData?.error;
async function supportAccessSet(allow){if(bugHosted()){const r=await fetch('/_machine/support-access',{method:'POST',headers:{'Content-Type':'application/json'},credentials:'same-origin',redirect:'manual',body:JSON.stringify({allow})});if(!r.ok)throw Error();saData=await r.json()}else saData=await saLocal(allow);saAt=Date.now();supportAccessRender()}
function supportAccessRender(){const d=saData||{},on=saOn(),b=$('#sa-toggle');$('#settings-support').hidden=!(bugHosted()||saShown)||!on;
 $('#sa-state').textContent=d.error?'Can’t check right now':on?t('On until {}',fmtDHM(d.until,{weekday:'short',month:'short',day:'numeric'})):'Off';
 $('#sa-note').textContent=on?'Read-only. Turn it off any time.':'Ends by itself after 24 hours.';b.textContent=on?'Turn off':'Allow for 24 hours';b.dataset.on=on?'1':'';b.disabled=!!d.error;
 if(typeof actDraw==='function'&&settingsNow==='activity')actDraw()}
$('#sa-activity').onclick=()=>{act.filter='access';act.items=[];act.next=null;showSettings('activity');actLoad()};
$('#sa-toggle').onclick=async()=>{const b=$('#sa-toggle'),was=!!b.dataset.on;b.disabled=true;
 try{await supportAccessSet(!was);toast(was?'Support access is off.':'Support access is on for 24 hours.')}
 catch{toast('That didn’t work. Try again.',true)}finally{saAt=Date.now();supportAccessRender()}};
new MutationObserver(()=>{if(!$('#settings').hidden)supportAccessLoad()}).observe($('#settings'),{attributes:true,attributeFilter:['hidden']});
