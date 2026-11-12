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
const CONNECT_SITES=['linkedin','x','facebook'];
// From a hosted setup page (#signin-site=linkedin): that site's sign-in only, and once in, setup connects it by itself.
// Also ChatGPT and Claude, for Find my skills (Settings > Skills > Import): once in, the list looks there by itself (`signinAfter`).
// And Facebook, for the Import birthdays from Facebook to-do: once in, it reads again by itself.
const SIGNIN_SITES={linkedin:{name:'LinkedIn',hosts:['linkedin.com']},x:{name:'X',hosts:['x.com']},chatgpt:{name:'ChatGPT',hosts:['chatgpt.com','openai.com']},claude:{name:'Claude',hosts:['claude.ai']},facebook:{name:'Facebook',hosts:['facebook.com']}};
// The sign-in dialog is the lazy 'signin' part (connections-signin-dialog.js): this opens it once it's in.
function openSignin(...args){lazyRun('signin',()=>signinOpen(...args))}
const onSite=(page,s)=>s.hosts.some(h=>page?.site===h||page?.site?.endsWith('.'+h));
document.addEventListener('click',async e=>{const b=e.target.closest('[data-copy-link]');if(!b)return;try{await navigator.clipboard.writeText(b.dataset.copyLink);toast('Copied.')}catch{toast('Couldn’t copy automatically. Select the text to copy it.',true)}});
document.addEventListener('click',async e=>{const b=e.target.closest('[data-copy-command]');if(!b)return;try{await navigator.clipboard.writeText(b.dataset.copyCommand);toast('Copied.')}catch{toast('Couldn’t copy automatically. Select the command to copy it.',true)}});
document.addEventListener('click',e=>{const b=e.target.closest('[data-signin]');if(b)openSignin(b.dataset.signin||null,!!b.dataset.task,b.dataset.task||null,b.dataset.page||null)});
// Saved sign-ins: one row per site with its username and whether a password is kept. The password itself never
// reaches the page (the list has none), so a row only ever says "Password saved".
const LOCK=html`<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3.25" y="7" width="9.5" height="6.5" rx="1.6" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M5.5 7V5.2a2.5 2.5 0 0 1 5 0V7" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>`;
const savedOn=v=>{const d=v&&new Date(v);if(!d||isNaN(d))return '';return localeDate(d,DL,d.getFullYear()===new Date().getFullYear()?{day:'numeric',month:'short'}:{month:'short',year:'numeric'})};
function savedLoginRow(l){const site=String(l.site||''),user=String(l.username||''),on=savedOn(l.saved_at);
 return html`<div class="saved-login"><span class="login-mark" aria-hidden="true">${(site.replace(/^www\./,'')[0]||'?').toUpperCase()}</span><span class="grow"><strong title="${site}">${site}</strong>${user?html`<span class="login-user" title="${user}">${user}</span>`:''}<small class="login-pass">${l.password_saved?LOCK:''}<span>${l.password_saved?'Password saved':'No password saved'}${on?` · ${on}`:''}</span></small></span><button type="button" class="quiet" data-forget-login="${site}" aria-label="Forget ${site}">Forget</button></div>`}
async function savedLogins(){try{const r=await signinPost('browser_logins',{}),logins=Array.isArray(r.logins)?r.logins:[];if(savedLoginCount!==logins.length){savedLoginCount=logins.length;if(lazyIn('connections'))renderHealthTabs()}
 $('#saved-logins').classList.toggle('empty',!logins.length);
 setHTML($('#saved-logins'),logins.length?html`${logins.map(savedLoginRow)}`:html`<div><strong>No saved sign-ins</strong><span>Tick Save for next time when you sign in to a site.</span></div>`)}catch{}}
$('#saved-logins').onclick=async e=>{const b=e.target.closest('[data-forget-login]');if(!b)return;b.disabled=true;try{await signinPost('browser_login_forget',{site:b.dataset.forgetLogin});toast('Forgotten.');savedLogins()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}};
// A task link from someone's email (task_invites.py), opened into this Machine: its card, then who sent it to connect with.
{const m=/^#task=([A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43})$/.exec(location.hash);if(m){history.replaceState(null,'',location.pathname);
 fleetPost('task_import',{link:m[1]}).then(async r=>{await refresh();const who=r.from||{};
  if(r.can_connect)toast(`Added ${who.name}’s task. Connect with them on the Network?`,false);else toast(`Added ${who.name}’s task to your to-dos.`);
  if(r.can_connect)$('#toast').append(' ',make('button',{'data-task-connect':who.username},'Connect'))}).catch(err=>toast(err.message,true))}}
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
