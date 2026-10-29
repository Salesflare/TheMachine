// A card waiting on the owner's sign-in carries on by itself once they're in, whichever way they signed in (the dialog,
// the Browser pane, the browser on the computer): the service sees it (watch_sign_ins). Look at such cards every few
// seconds so the card shows that at once, and look in the browser right away when the owner closes it there.
const signinWaiting=s=>s.preparation_status==='blocked'&&!!s.preparation_browser?.sign_in&&['accepted','instructions'].includes(s.status);
let taskSigninBusy=false;
async function taskSigninPoll(){if(taskSigninBusy||document.hidden)return;const waits=(state?.suggestions||[]).filter(signinWaiting).slice(0,3);if(!waits.length)return;taskSigninBusy=true;
 try{for(const s of waits){let p;try{p=await request('api/progress?id='+encodeURIComponent(s.id))}catch{continue}
  if(p.status!=='blocked'){if(['queued','starting','running'].includes(p.status)&&!$('#signin-dialog').open&&!($('#toast').classList.contains('show')&&['Signed in. Carrying on with it.','Signed in. I’ll carry on.'].map(x=>t(x)).includes($('#toast').textContent.trim())))toast('Signed in. Carrying on with it.');await refresh();return}}}
 finally{taskSigninBusy=false}}
setInterval(taskSigninPoll,5000);
async function signinClosed(){if(!(state?.suggestions||[]).some(signinWaiting))return;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'browser_login_check',args:{}})});
  if(r.resumed?.length){toast('Signed in. Carrying on with it.');await refresh();return}}catch{}
 taskSigninPoll()}
const signinPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
let signinPages=[];
const SIGNIN_FIELDS=['#signin-user-row','#signin-pass-row','#signin-code-row','#signin-save-row','#signin-go','#signin-saved'];
// One state of the dialog at a time: waiting (neutral, spinner), the fields, the browser itself, or a real error (red).
function signinMode(mode,view){for(const id of SIGNIN_FIELDS)if(mode!=='form')$(id).hidden=true;$('#signin-fine').hidden=mode!=='form';
$('#signin-view').hidden=!(mode==='browser'&&view);if($('#signin-view').hidden)$('#signin-frame').removeAttribute('src');
$('#signin-retry').hidden=!['browser','error'].includes(mode);$('#signin-continue').hidden=!(mode==='browser'&&(signinTask||signinAfter));
$('#signin-browser').className=mode==='browser'&&!view?'primary':'ghost';if(mode!=='error')$('#signin-error').textContent='';if(mode==='form'||mode==='error')signinStatus('')}
function signinStatus(text,spin){$('#signin-status').hidden=!text;$('#signin-status-text').textContent=text||'';$('#signin-status .spin').hidden=!spin}
// Which code the page wants, in its own words: the kind (text message, authenticator app, email, security key) the
// service read from what the page says, the site's sentence quoted, and its own "another way" links as buttons.
const CODE_SAYS={sms:(b,p)=>[`${b} sent a code by text message`,p.sent_to?`To your phone ${p.sent_to} (as ${b} shows it).`:'Check the text messages on your phone.'],
app:b=>['Code from your authenticator app',`Not a text message: open the app where you added ${b}.`],
email:(b,p)=>['Code from your email',p.sent_to?`Sent to ${p.sent_to} (as ${b} shows it).`:`Look for an email from ${b}.`],
key:b=>[`${b} wants your security key`,'Open the browser to use it there.']};
function signinCode(page,message){const b=page.brand||page.site,says=CODE_SAYS[page.code_kind],[title,help]=says?says(b,page):[`Enter the code ${page.site} asks for`,''];
const only=!page.username&&!page.password;if(only)$('#signin-title').textContent=title;
const h=$('#signin-code-help');h.textContent=only?help:title+(help?'. '+help:'');h.hidden=!h.textContent;
const a=$('#signin-code-ask');a.textContent=page.ask?`${b} says: “${page.ask}”`:'';a.hidden=!page.ask;
$('#signin-code-label').textContent=says&&page.code_kind!=='key'?'Code':'One-time code';
const o=$('#signin-others');o.innerHTML=(page.others||[]).map(l=>`<button type="button" class="ghost" data-signin-other="${esc(l)}">${esc(l)}</button>`).join('');o.hidden=!page.others?.length;
if(!message&&page.error)$('#signin-error').textContent=`${b} says: “${page.error}”`}
$('#signin-others').onclick=async e=>{const btn=e.target.closest('[data-signin-other]');if(!btn)return;const f=$('#signin-form'),label=btn.dataset.signinOther,run=signinRun;
for(const x of document.querySelectorAll('#signin-others button,#signin-go'))x.disabled=true;$('#signin-error').textContent='';signinStatus(`Clicking “${label}” on the page…`,true);
try{const r=await signinPost('browser_login_choose',{page:f.dataset.page,host:f.dataset.host,option:label});if(run!==signinRun)return;
if(r.page)signinShow(r.page,'');else signinBrowser({site:f.dataset.host},run)}
catch(err){errCaught(err);signinStatus('');$('#signin-error').textContent=err.message}finally{for(const x of document.querySelectorAll('#signin-others button,#signin-go'))x.disabled=false}};
function signinFail(message){signinMode('error');$('#signin-error').textContent=message}
function signinShow(page,message){const d=$('#signin-dialog');$('#signin-pass').value='';$('#signin-code').value='';
if(!page){signinFail(message||'No sign-in page is open right now. Open the browser to see what it shows.');return}
signinMode('form');$('#signin-error').textContent=message||'';
$('#signin-title').textContent=signinSite?`Sign in to ${signinSite.name} on your Machine`:'Sign in to '+page.site;$('#signin-form').dataset.page=page.id;$('#signin-form').dataset.host=page.host;
$('#signin-user-row').hidden=!page.username;$('#signin-pass-row').hidden=!page.password;$('#signin-code-row').hidden=!page.code;if(page.code)signinCode(page,message);$('#signin-save-row').hidden=!(page.username||page.password)||state.security?.settings?.save_logins==='off';$('#signin-go').hidden=false;
const saved=page.saved&&(page.username||page.password);$('#signin-saved').hidden=!saved;if(saved)$('#signin-use-saved').textContent=page.saved.username?t('Sign in as {}',page.saved.username):t('Sign in as the saved user');
if(!d.open)d.showModal();(page.username&&!$('#signin-user').value?$('#signin-user'):page.password?$('#signin-pass'):page.code?$('#signin-code'):$('#signin-go')).focus()}
// `task`: the card waiting on this sign-in; once the page is past it, that task carries on by itself. `page`: its tab.
let signinTask=null,signinTab=null,signinRun=0,signinArgs=[],signinSite=null,signinApproving=null,signinAfter=null,signinFresh=false;
const CONNECT_SITES=['linkedin','x'];
// From a hosted setup page (#signin-site=linkedin): that site's sign-in only, and once in, setup connects it by itself.
// Also ChatGPT and Claude, for Find my skills (Settings > Skills > Import): once in, the list looks there by itself (`signinAfter`).
const SIGNIN_SITES={linkedin:{name:'LinkedIn',hosts:['linkedin.com']},x:{name:'X',hosts:['x.com']},chatgpt:{name:'ChatGPT',hosts:['chatgpt.com','openai.com']},claude:{name:'Claude',hosts:['claude.ai']}};
const onSite=(page,s)=>s.hosts.some(h=>page?.site===h||page?.site?.endsWith('.'+h));
const siteName=page=>signinSite?.name||Object.values(SIGNIN_SITES).find(s=>onSite(page,s))?.name||page?.site||'the site';
function signinDone(resumed){signinApproving=null;
if(signinAfter){const go=signinAfter,name=signinSite?.name||'the site';signinAfter=null;$('#signin-dialog').close();toast(go.says||`Signed in to ${name}. Looking there now.`);go();return}
if(signinSite){signinMode('wait');$('#signin-browser').hidden=true;$('#signin-title').textContent=`Signed in to ${signinSite.name}`;signinStatus(`You’re in. Your setup page connects ${signinSite.name} by itself; you can close this tab.`,false);return}
$('#signin-dialog').close();toast(resumed?.length?'Signed in. Carrying on with it.':'Signed in. I’ll carry on.');refresh()}
// No field left but not in yet: the site waits on its app (LinkedIn's "approve this sign-in"), a two-step page or a check.
function signinApprove(page,run){signinApproving=page;const name=siteName(page);signinMode('wait');$('#signin-continue').hidden=false;$('#signin-continue').className='primary';
signinStatus(`Approve the sign-in in your ${name} app, then press Continue.`,true);signinCheck(run,false)}
// Approving can take a while; after two minutes with nothing new, the site may have stopped it: say so, with Try again.
const SIGNIN_STALL=120000;
async function signinCheck(run,now){const page=signinApproving;if(!page)return;const since=Date.now();
for(let first=true;run===signinRun&&$('#signin-dialog').open&&signinApproving===page;first=false){
 if(!(now&&first))await new Promise(r=>setTimeout(r,3000));if(run!==signinRun||signinApproving!==page)return;
 let r;try{r=await signinPost('browser_login_pages',{watch:page.id,host:page.host,...(signinTask?{suggestion_id:signinTask}:{})})}catch(err){errCaught(err);if(run===signinRun){signinApproving=null;signinFail(err.message)}return}
 if(run!==signinRun||signinApproving!==page)return;
 if(r.state==='done'){signinDone(r.resumed);return}
 if(r.state==='form'){signinApproving=null;signinShow(r.page,'');return}
 if(r.state==='captcha'){signinApproving=null;signinBrowser({site:siteName(page),kind:'captcha'},run);return}
 if(now&&first)signinStatus(`Not approved yet. Approve the sign-in in your ${siteName(page)} app first; I keep checking.`,true);
 else if(Date.now()-since>SIGNIN_STALL&&$('#signin-retry').hidden){signinStatus(t('{} hasn’t moved on. If it stopped the sign-in, press Try again.',siteName(page)),false);signinFresh=true;$('#signin-retry').hidden=false;$('#signin-retry').className='primary';$('#signin-continue').className='ghost'}}}
const signinWithin=(promise,ms)=>Promise.race([promise,new Promise((_,no)=>setTimeout(()=>no(Error('The browser took too long to answer.')),ms))]);
const SIGNIN_SAYS={eid:n=>t('{} signs in with itsme or eID.',n),passkey:n=>t('{} wants a passkey.',n),captcha:n=>t('{} wants a quick check that you’re not a robot.',n),account:n=>t('{} wants you to pick the right account.',n),code:n=>t('{} wants a one-time code.',n)};
async function openSignin(account,wait,task,page,site,after){const run=++signinRun;signinFresh=false;signinArgs=[account,wait,task,page,site,after];signinAfter=after||null;signinTask=task||null;signinTab=page||null;signinSite=SIGNIN_SITES[site]||null;signinApproving=null;$('#signin-continue').className='ghost';$('#signin-retry').className='ghost';$('#signin-browser').hidden=false;const d=$('#signin-dialog');$('#signin-user').value='';$('#signin-save').checked=false;$('#signin-pick').hidden=true;
$('#signin-title').textContent=signinSite?`Sign in to ${signinSite.name} on your Machine`:'Sign in';signinMode('wait');if(!d.open)d.showModal();let info=null;
if(task){signinStatus('Opening the sign-in page…',true);
try{info=await signinWithin(signinPost('browser_login_open',{suggestion_id:task}),20000)}catch(err){errCaught(err);if(run===signinRun)signinFail(err.message);return}
if(run!==signinRun||!d.open)return;if(info.site){$('#signin-title').textContent='Sign in to '+info.site;signinStatus(`Opening ${info.site} sign-in…`,true)}}
else signinStatus('Looking for the sign-in page…',true);
// Nothing to type for itsme or eID, a passkey, a captcha or choosing an account: straight to the browser.
const until=Date.now()+(info&&['eid','passkey','captcha','account'].includes(info.kind)||info?.state==='unknown'?0:task||wait?15000:0);
for(;;){try{signinPages=(await signinWithin(signinPost('browser_login_pages',task?{suggestion_id:task}:account?{account}:{}),20000)).pages}catch(err){errCaught(err);if(run===signinRun)signinFail(err.message);return}
if(signinSite)signinPages=signinPages.filter(p=>onSite(p,signinSite));
if(run!==signinRun||!d.open)return;if(signinPages.length||Date.now()>=until)break;await new Promise(r=>setTimeout(r,2500));if(run!==signinRun||!d.open)return}
$('#signin-page').innerHTML=signinPages.map((p,i)=>`<option value="${i}">${esc(p.site)}${p.title?' · '+esc(p.title):''}</option>`).join('');$('#signin-pick').hidden=signinPages.length<2;
if(signinPages.length){signinShow(signinPages[0]);if(signinSite)$('#signin-title').textContent=`Sign in to ${signinSite.name} on your Machine`;return}
if(signinAfter){signinBrowser({site:signinSite?.name},run);return}
if(signinSite){signinFail(`No ${signinSite.name} sign-in page is open on your Machine. Signed in already? Then go back to setup; it connects by itself. Otherwise press Try again.`);return}
if(!task){signinFail('No sign-in page is open right now. Open the browser to see what it shows.');return}
signinBrowser(info,run)}
// The task's sign-in in the browser itself, in the dialog when this dashboard has the live view; it carries on once you're in.
function signinBrowser(info,run){const link=state.browser_link||info?.view||'';let view=false;try{view=!!link&&new URL(link,location.href).origin===location.origin}catch{}
signinMode('browser',view);const name=info?.site||t('This site'),says=SIGNIN_SAYS[info?.kind];
signinStatus((info?.state==='unknown'?t(view?'Finish signing in for this task below.':'Finish signing in for this task in the browser.'):says?says(name)+' '+t(view?'Finish it below.':'Finish it in the browser.'):t(view?'Finish signing in to {} below.':'Finish signing in to {} in the browser.',name))+' '+t(signinAfter?'Then press Continue.':'I carry on by myself once you’re in.'),false);
if(view)$('#signin-frame').src=link;signinWatch(run)}
async function signinWatch(run){while(run===signinRun&&$('#signin-dialog').open&&signinTask){await new Promise(r=>setTimeout(r,4000));if(run!==signinRun||!$('#signin-dialog').open)return;
try{const p=await request('api/progress?id='+encodeURIComponent(signinTask));if(p.status!=='blocked'){$('#signin-dialog').close();toast('Signed in. Carrying on with it.');refresh();return}}catch{}}}
// After a sign-in that stalled at the site, Try again starts LinkedIn's or X's sign-in page afresh in that tab.
$('#signin-retry').onclick=async()=>{const site=signinArgs[4];if(signinFresh&&SIGNIN_SITES[site]&&CONNECT_SITES.includes(site)){try{await connectPost('connect_site_signin',{site,fresh:true})}catch(err){errCaught(err)}}openSignin(...signinArgs)};
$('#signin-continue').onclick=async()=>{if(signinApproving){signinCheck(signinRun,true);return}if(signinAfter){signinDone();return}const id=signinTask;$('#signin-dialog').close();try{await saveDecision(id,'retry')}catch(err){errCaught(err);toast(err.message,true)}};
$('#signin-page').onchange=e=>signinShow(signinPages[Number(e.target.value)]);
async function signinSend(args){const f=$('#signin-form'),go=$('#signin-go'),saved=$('#signin-use-saved');go.disabled=saved.disabled=true;$('#signin-error').textContent='Signing in…';
try{const r=await signinPost('browser_login_fill',{page:f.dataset.page,host:f.dataset.host,...(signinTask?{suggestion_id:signinTask}:{}),...args});
if(r.result==='done'){signinDone(r.resumed);return}if(r.result==='approve'){signinApprove(r.page,signinRun);return}
if(r.result==='captcha'){signinBrowser({site:siteName(r.page),kind:'captcha'},signinRun);return}
if(r.result==='blocked'){signinShow(r.page,t('{} went back to the start, so it stopped this sign-in. Wait a minute, then try again.',r.page.brand||siteName(r.page)));return}
if(r.result==='next')signinShow(r.page,'');else signinShow(r.page||null,r.page?.error?`${r.page.brand||r.page.site} says: “${r.page.error}”`:'The site didn’t accept that. Check and try again, or open the browser.')}
catch(err){errCaught(err);$('#signin-error').textContent=err.message}finally{go.disabled=saved.disabled=false;$('#signin-pass').value='';$('#signin-code').value=''}}
$('#signin-form').onsubmit=e=>{e.preventDefault();const args={save:$('#signin-save').checked};
if(!$('#signin-user-row').hidden&&$('#signin-user').value)args.username=$('#signin-user').value;if(!$('#signin-pass-row').hidden&&$('#signin-pass').value)args.password=$('#signin-pass').value;if(!$('#signin-code-row').hidden&&$('#signin-code').value.trim())args.code=$('#signin-code').value.trim();
if(!args.username&&!args.password&&!args.code){$('#signin-error').textContent='Fill in what the site asks for.';return}signinSend(args)};
$('#signin-use-saved').onclick=()=>signinSend({use_saved:true,...(!$('#signin-code-row').hidden&&$('#signin-code').value.trim()?{code:$('#signin-code').value.trim()}:{})});
$('#signin-browser').onclick=async()=>{const link=state.browser_link;if(browserPane())$('#signin-dialog').close();else if(link)window.open(link,'_blank','noopener');try{const r=await signinPost('browser_focus',signinTask?{suggestion_id:signinTask}:{page:signinTab});if(!link||!r.shown)toast(r.shown?'The browser is in front now.':r.unknown?'I don’t know which tab this task uses; find it in the browser.':'I couldn’t reach the browser on this computer.',!r.shown)}catch(err){errCaught(err);if(!link)toast(err.message,true)}};
// Full size: the sign-in's browser over the whole window, for a small screen in the view; the same button goes back.
const signinFull=on=>{$('#signin-dialog').classList.toggle('signin-full',on);$('#signin-full').setAttribute('aria-pressed',String(on));$('#signin-full').textContent=on?'Exit full size':'Full size'};
$('#signin-full').onclick=()=>signinFull(!$('#signin-dialog').classList.contains('signin-full'));
$('#signin-dialog').addEventListener('close',()=>{signinFull(false);if(signinTask)signinClosed();signinRun++;signinAfter=null;$('#signin-frame').removeAttribute('src');$('#signin-pass').value='';$('#signin-code').value='';$('#signin-user').value=''});
document.addEventListener('click',async e=>{const b=e.target.closest('[data-copy-link]');if(!b)return;try{await navigator.clipboard.writeText(b.dataset.copyLink);toast('Copied.')}catch{toast('Couldn’t copy automatically. Select the text to copy it.',true)}});
document.addEventListener('click',async e=>{const b=e.target.closest('[data-copy-command]');if(!b)return;try{await navigator.clipboard.writeText(b.dataset.copyCommand);toast('Copied.')}catch{toast('Couldn’t copy automatically. Select the command to copy it.',true)}});
document.addEventListener('click',e=>{const b=e.target.closest('[data-signin]');if(b)openSignin(b.dataset.signin||null,!!b.dataset.task,b.dataset.task||null,b.dataset.page||null)});
// Saved sign-ins: one row per site with its username and whether a password is kept. The password itself never
// reaches the page (the list has none), so a row only ever says "Password saved".
const LOCK='<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3.25" y="7" width="9.5" height="6.5" rx="1.6" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M5.5 7V5.2a2.5 2.5 0 0 1 5 0V7" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>';
const savedOn=v=>{const d=v&&new Date(v);if(!d||isNaN(d))return '';return d.toLocaleDateString(DL,d.getFullYear()===new Date().getFullYear()?{day:'numeric',month:'short'}:{month:'short',year:'numeric'})};
function savedLoginRow(l){const site=String(l.site||''),user=String(l.username||''),on=savedOn(l.saved_at);
 return `<div class="saved-login"><span class="login-mark" aria-hidden="true">${esc((site.replace(/^www\./,'')[0]||'?').toUpperCase())}</span><span class="grow"><strong title="${esc(site)}">${esc(site)}</strong>${user?`<span class="login-user" title="${esc(user)}">${esc(user)}</span>`:''}<small class="login-pass">${l.password_saved?LOCK:''}<span>${l.password_saved?'Password saved':'No password saved'}${on?` · ${esc(on)}`:''}</span></small></span><button type="button" class="quiet" data-forget-login="${esc(site)}" aria-label="Forget ${esc(site)}">Forget</button></div>`}
async function savedLogins(){try{const r=await signinPost('browser_logins',{}),logins=Array.isArray(r.logins)?r.logins:[];if(savedLoginCount!==logins.length){savedLoginCount=logins.length;renderHealthTabs()}
 $('#saved-logins').classList.toggle('empty',!logins.length);
 $('#saved-logins').innerHTML=logins.length?logins.map(savedLoginRow).join(''):'<div><strong>No saved sign-ins</strong><span>Tick Save for next time when you sign in to a site.</span></div>'}catch{}}
$('#saved-logins').onclick=async e=>{const b=e.target.closest('[data-forget-login]');if(!b)return;b.disabled=true;try{await signinPost('browser_login_forget',{site:b.dataset.forgetLogin});toast('Forgotten.');savedLogins()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}};
// A task link from someone's email (task_invites.py), opened into this Machine: its card, then who sent it to connect with.
{const m=/^#task=([A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43})$/.exec(location.hash);if(m){history.replaceState(null,'',location.pathname);
 fleetPost('task_import',{link:m[1]}).then(async r=>{await refresh();const who=r.from||{};
  if(r.can_connect)toast(`Added ${who.name}’s task. Connect with them on the Network?`,false);else toast(`Added ${who.name}’s task to your to-dos.`);
  if(r.can_connect){const t=$('#toast');t.insertAdjacentHTML('beforeend',` <button data-task-connect="${esc(who.username)}">Connect</button>`)}}).catch(err=>toast(err.message,true))}}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-task-connect]');if(!b)return;b.disabled=true;
 try{await fleetPost('fleet_friend',{do:'add',username:b.dataset.taskConnect});toast('Friend request sent. You’re connected once they accept.')}catch(err){errCaught(err);toast(err.message,true)}});
{const m=/^#signin-site=(linkedin|x)$/.exec(location.hash);if(m){history.replaceState(null,'',location.pathname);openSignin(null,true,null,null,m[1])}}
{const m=/^#signin(?:=([\w.@:-]{1,100}))?$/.exec(location.hash);if(m){history.replaceState(null,'',location.pathname);openSignin(m[1]?decodeURIComponent(m[1]):null,true)}}
// Telegram's Sign in button on a card waiting on a sign-in: the same dialog, for that task.
{const m=/^#signin-for=([a-f0-9]{16})$/.exec(location.hash);if(m){history.replaceState(null,'',location.pathname);openSignin(null,true,m[1])}}
// View in browser: shown only while the task's page is open in the Machine's browser (browser_open); the click brings it
// to the front there (reopened when it closed since the card was drawn, never a dead tab), and its viewer
// opens in a new tab (the link itself). From Telegram the dashboard opens with #browser-for=<task> and goes on to the viewer.
async function browserShow(id){return request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'browser_show',args:{suggestion_id:id}})})}
