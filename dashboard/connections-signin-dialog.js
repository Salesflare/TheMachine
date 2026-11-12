// A lazy part (dashboard_parts.LAZY 'signin'): the sign-in dialog. connections-signin.js opens it through openSignin(), nothing here until it's in.
let signinPages=[];
const SIGNIN_FIELDS=['#signin-user-row','#signin-pass-row','#signin-code-row','#signin-save-row','#signin-go','#signin-saved'];
// One state of the dialog at a time: waiting (neutral, spinner), the fields, the browser itself, or a real error (red).
function signinMode(mode,view){for(const id of SIGNIN_FIELDS)if(mode!=='form')$(id).hidden=true;$('#signin-fine').hidden=mode!=='form';
$('#signin-view').hidden=!(mode==='browser'&&view);if($('#signin-view').hidden)$('#signin-frame').removeAttribute('src');
$('#signin-retry').hidden=!['browser','error'].includes(mode);$('#signin-continue').hidden=!(mode==='browser'&&(signinTask||signinAfter));
$('#signin-browser').className=mode==='browser'&&!view?'primary':'ghost';if(mode!=='error')$('#signin-error').textContent='';if(mode==='form'||mode==='error')signinStatus('');$('#signin-home').hidden=true}
// A site that refused the sign-in or put a robot check up, on a hosted Machine: sites often do that to a browser in the
// cloud, so one line links the setup page's step that sends this browser out through the owner's home connection.
// Not on the owner's own computer: its browser is already at home.
function signinHome(){let link='';try{link=state.manage_url?new URL('#browser-route',state.manage_url).href:''}catch{}
if(!/^https:\/\//.test(link))return;$('#signin-home-link').href=link;$('#signin-home').hidden=false}
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
const o=$('#signin-others');setHTML(o,html`${(page.others||[]).map(l=>html`<button type="button" class="ghost" data-signin-other="${l}">${l}</button>`)}`);o.hidden=!page.others?.length;
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
async function signinOpen(account,wait,task,page,site,after){const run=++signinRun;signinFresh=false;signinArgs=[account,wait,task,page,site,after];signinAfter=after||null;signinTask=task||null;signinTab=page||null;signinSite=SIGNIN_SITES[site]||null;signinApproving=null;$('#signin-continue').className='ghost';$('#signin-retry').className='ghost';$('#signin-browser').hidden=false;const d=$('#signin-dialog');$('#signin-user').value='';$('#signin-save').checked=false;$('#signin-pick').hidden=true;
$('#signin-title').textContent=signinSite?`Sign in to ${signinSite.name} on your Machine`:'Sign in';signinMode('wait');if(!d.open)d.showModal();let info=null;
if(task){signinStatus('Opening the sign-in page…',true);
try{info=await signinWithin(signinPost('browser_login_open',{suggestion_id:task}),20000)}catch(err){errCaught(err);if(run===signinRun)signinFail(err.message);return}
if(run!==signinRun||!d.open)return;if(info.site){$('#signin-title').textContent='Sign in to '+info.site;signinStatus(`Opening ${info.site} sign-in…`,true)}}
else signinStatus('Looking for the sign-in page…',true);
// Nothing to type for itsme or eID, a passkey, a captcha or choosing an account: straight to the browser.
const until=Date.now()+(info&&['eid','passkey','captcha','account'].includes(info.kind)||info?.state==='unknown'?0:task||wait?15000:0);
let walls=[];
for(;;){try{const r=await signinWithin(signinPost('browser_login_pages',task?{suggestion_id:task}:account?{account}:{}),20000);signinPages=r.pages;walls=Array.isArray(r.walls)?r.walls:[]}catch(err){errCaught(err);if(run===signinRun)signinFail(err.message);return}
if(signinSite){signinPages=signinPages.filter(p=>onSite(p,signinSite));walls=walls.filter(p=>onSite(p,signinSite))}
if(run!==signinRun||!d.open)return;if(signinPages.length||walls.length||Date.now()>=until)break;await new Promise(r=>setTimeout(r,2500));if(run!==signinRun||!d.open)return}
setHTML($('#signin-page'),html`${signinPages.map((p,i)=>html`<option value="${i}">${p.site}${p.title?' · '+p.title:''}</option>`)}`);$('#signin-pick').hidden=signinPages.length<2;
if(signinPages.length){signinShow(signinPages[0]);if(signinSite)$('#signin-title').textContent=`Sign in to ${signinSite.name} on your Machine`;return}
// no form, but a robot check or block page in front of the site: finish it in the browser
if(walls.length){signinBrowser({site:siteName(walls[0]),kind:'captcha'},run);return}
if(signinAfter){signinBrowser({site:signinSite?.name},run);return}
if(signinSite){signinFail(`No ${signinSite.name} sign-in page is open on your Machine. Signed in already? Then go back to setup; it connects by itself. Otherwise press Try again.`);return}
if(!task){signinFail('No sign-in page is open right now. Open the browser to see what it shows.');return}
signinBrowser(info,run)}
// The task's sign-in in the browser itself, in the dialog when this dashboard has the live view; it carries on once you're in.
function signinBrowser(info,run){const link=state.browser_link||info?.view||'';let view=false;try{view=!!link&&new URL(link,location.href).origin===location.origin}catch{}
signinMode('browser',view);const name=info?.site||t('This site'),says=SIGNIN_SAYS[info?.kind];
signinStatus((info?.state==='unknown'?t(view?'Finish signing in for this task below.':'Finish signing in for this task in the browser.'):says?says(name)+' '+t(view?'Finish it below.':'Finish it in the browser.'):t(view?'Finish signing in to {} below.':'Finish signing in to {} in the browser.',name))+' '+t(signinAfter?'Then press Continue.':'I carry on by myself once you’re in.'),false);
if(info?.kind==='captcha')signinHome();if(view)$('#signin-frame').src=link;signinWatch(run)}
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
if(r.result==='blocked'){signinShow(r.page,t('{} went back to the start, so it stopped this sign-in. Wait a minute, then try again.',r.page.brand||siteName(r.page)));signinHome();return}
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
