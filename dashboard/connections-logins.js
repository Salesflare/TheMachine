// A lazy part (dashboard_parts.LAZY 'logins'): Connections, Sign-ins. The saved sign-ins, one row per account, and
// Import (loginImportOpen). connections-signin.js calls in through lazyRun.
const savedOn=v=>{const d=v&&new Date(v);if(!d||isNaN(d))return '';return localeDate(d,DL,d.getFullYear()===new Date().getFullYear()?{day:'numeric',month:'short'}:{month:'short',year:'numeric'})};
// One row per site, its name never cut short by a label. Each account: its username (or a muted "No username saved"),
// then its side as a menu that stays changeable (Work, Personal, a name of the owner's own, or not set yet: Default,
// shown as "Work or personal?"; browser_login_rename), whether a password is kept, and its own Forget. A name another
// account on the site has is greyed out.
const loginWho=(l,list)=>{const user=String(l.username||''),a=String(l.account||'Default'),taken=list.filter(x=>x!==l).map(x=>String(x.account||'Default'));
 return html`<span class="login-user${user?'':' login-none'}" title="${user}">${user||t('No username saved')}</span><span class="login-meta"><select data-login-side="${l.id}" aria-label="${t('Work or personal for {}',user||l.site)}">${[...new Set(['Default',...LI_ACCOUNTS,a])].map(o=>html`<option value="${o}"${o===a?html` selected`:taken.includes(o)?html` disabled`:''}>${o==='Default'?t('Work or personal?'):t(o)}</option>`)}</select>${loginPass(l)}</span>`};
const loginPass=l=>{const on=savedOn(l.saved_at);return html`<small class="login-pass">${l.password_saved?LOCK:''}<span>${l.password_saved?'Password saved':'No password saved'}${on?` · ${on}`:''}</span></small>`};
const loginForget=(l,label)=>html`<button type="button" class="quiet" data-forget-login="${l.id||l.site}" aria-label="${t('Forget {}',label)}">Forget</button>`;
function savedLoginRow([site,list]){const mark=html`<span class="login-mark" aria-hidden="true">${(site.replace(/^www\./,'')[0]||'?').toUpperCase()}</span>`;
 if(list.length===1){const l=list[0];return html`<div class="saved-login">${mark}<span class="grow"><strong title="${site}">${site}</strong>${loginWho(l,list)}</span>${loginForget(l,site)}</div>`}
 return html`<div class="saved-login many">${mark}<span class="grow"><strong title="${site}">${site}</strong><span class="login-accts">${list.map(l=>html`<span class="login-acct"><span class="grow">${loginWho(l,list)}</span>${loginForget(l,l.username||site)}</span>`)}</span></span></div>`}
const loginSites=logins=>{const by=new Map();for(const l of logins){const s=String(l.site||'');if(!by.has(s))by.set(s,[]);by.get(s).push(l)}return [...by]};
async function savedLoginsDraw(){try{const r=await signinPost('browser_logins',{}),logins=Array.isArray(r.logins)?r.logins:[];if(savedLoginCount!==logins.length){savedLoginCount=logins.length;if(lazyIn('connections'))renderHealthTabs()}
 $('#saved-logins').classList.toggle('empty',!logins.length);
 setHTML($('#saved-logins'),logins.length?html`${loginSites(logins).map(savedLoginRow)}`:html`<div><strong>No saved sign-ins</strong><span>Tick Save for next time when you sign in to a site, or import them.</span></div>`)}catch{}}
$('#saved-logins').onchange=async e=>{const s=e.target.closest('[data-login-side]');if(!s)return;s.disabled=true;
 try{await signinPost('browser_login_rename',{id:s.dataset.loginSide,account:s.value});toast(t('Saved.'))}catch(err){errCaught(err);toast(err.message,true)}savedLoginsDraw()};
$('#saved-logins').onclick=async e=>{const b=e.target.closest('[data-forget-login]');if(!b)return;b.disabled=true;const v=b.dataset.forgetLogin;try{await signinPost('browser_login_forget',/^[0-9a-f]{16}$/.test(v)?{id:v}:{site:v});toast('Forgotten.');savedLoginsDraw()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}};
// The sign-in dialog's saved sign-ins (connections-signin-dialog.js signinShow): those for the page's exact address,
// one per account. The to-do's own (`pick`: chosen before, the only one, or the one named for its Work or Personal
// side) is the one button; with several and none picked, the dialog asks once which one, and the service remembers it
// for that to-do. `all`: Other account. Save for next time gets Save as: Work or Personal (starting at the to-do's own
// side, `page.side`), a name this site already has, or a name of the owner's own.
let signinNow=null;
function signinSaveAs(page){const list=page.accounts||[],own=[...new Set(list.map(a=>String(a.account||'')).filter(a=>a&&a!=='Default'&&!LI_ACCOUNTS.includes(a)))];
 let sel=$('#signin-account');if(!sel){sel=make('select',{id:'signin-account',class:'signin-as','aria-label':t('Save as')});
  const name=make('input',{id:'signin-account-name',class:'signin-as-name',maxlength:'40',placeholder:t('Account name'),'aria-label':t('Account name'),hidden:''});
  sel.onchange=()=>{name.hidden=sel.value!=='';if(!name.hidden)name.focus()};$('#signin-save-row').after(name);$('#signin-save-row').append(sel)}
 setHTML(sel,html`${[...LI_ACCOUNTS,...own].map(a=>html`<option value="${a}">${t(a)}</option>`)}<option value="">${t('Other name…')}</option>`);
 sel.value=page.side&&LI_ACCOUNTS.includes(page.side)?page.side:'Personal';$('#signin-account-name').hidden=true;$('#signin-account-name').value=''}
function signinAccounts(page,all){signinNow=page;signinSaveAs(page);const box=$('#signin-saved'),list=page.accounts||(page.saved?[{id:'',account:'Default',username:page.saved.username}]:[]);
 const show=list.length&&(page.username||page.password);box.hidden=!show;if(!show)return setHTML(box,'');
 const many=list.length>1,pick=list.find(a=>a.id&&a.id===page.pick)||(!many?list[0]:null),ask=many&&!pick&&!!signinTask;
 const label=a=>{const side=a.account&&a.account!=='Default'?t(a.account):'';return a.username?(side?`${a.username} · ${side}`:a.username):side};
 const btn=(a,cls)=>html`<button type="button" class="${cls}" data-login="${a.id}">${label(a)?t('Sign in as {}',label(a)):t('Sign in as the saved user')}</button>`;
 setHTML(box,html`${ask?html`<p class="signin-which">${t('Which account for this to-do?')}</p>`:''}<div class="signin-acct">${pick&&!all?html`${btn(pick,'primary')}${many?html`<button type="button" class="quiet" data-login-other>${t('Other account')}</button>`:''}`:html`${list.map(a=>btn(a,a===pick?'primary':''))}`}</div>`)}
$('#signin-saved').onclick=e=>{const b=e.target.closest('button');if(!b)return;
 if('loginOther' in b.dataset){signinAccounts(signinNow||{},true);return}
 signinSend({use_saved:b.dataset.login||true,...(!$('#signin-code-row').hidden&&$('#signin-code').value.trim()?{code:$('#signin-code').value.trim()}:{})})};
// Import: sign-ins from a password manager's CSV export (1Password, LastPass, Bitwarden, Chrome), or from 1Password's op or
// LastPass's lpass when the owner has signed in to it on this computer; then a review where they tick which to keep and
// the account they go under (Work or Personal). No password ever reaches the page: the service holds what it
// read until Keep, then drops it (login_import.py). Nothing here signs in to a password manager.
const LI_ICON={file:html`<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 1.75h5l3 3v9.5H4z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/><path d="M8.75 1.75v3.25H12" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>`,
 '1password':html`<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.25" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M8 4.75v6.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>`,
 lastpass:html`<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="2.9" cy="8" r="1.25" fill="currentColor"/><circle cx="6.4" cy="8" r="1.25" fill="currentColor"/><circle cx="9.9" cy="8" r="1.25" fill="currentColor"/><path d="M13.4 4.5v7" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>`};
const LI_TOOLS={'1password':'1Password',lastpass:'LastPass'};
const LI_ACCOUNTS=['Work','Personal'];
let liReview=null,liTools={};
const liPost=args=>signinPost('browser_login_import',args);
function liDialog(){let d=$('#login-import');if(d)return d;
 d=make('dialog',{id:'login-import','aria-labelledby':'li-title'});document.body.append(d);
 d.addEventListener('close',()=>{const r=liReview;liReview=null;if(r)liPost({do:'drop',token:r.token}).catch(()=>{})});
 d.addEventListener('click',liClick);d.addEventListener('change',liChange);return d}
function liHead(title){return html`<div class="snooze-heading"><h2 id="li-title">${title}</h2><button type="button" data-li-close aria-label="${t('Close')}">×</button></div>`}
const liToolSays=s=>s==='ready'?t('Signed in on this computer'):s==='signed_out'?t('Sign in to it on this computer first'):t('Not installed on this computer');
function liPick(error){const d=liDialog();
 setHTML(d,html`${liHead(t('Import sign-ins'))}<p class="li-lead">${t('Bring in sign-ins from your password manager. You choose which to keep.')}</p>
 <div class="li-sources"><label class="li-source"><span class="li-icon">${LI_ICON.file}</span><span class="grow"><strong>${t('From an export file')}</strong><small>${t('A CSV from 1Password, LastPass, Bitwarden or Chrome')}</small></span><input type="file" accept=".csv,text/csv" data-li-file class="li-file"></label>
 ${Object.entries(LI_TOOLS).map(([k,name])=>html`<button type="button" class="li-source" data-li-tool="${k}"${liTools[k]&&liTools[k]!=='ready'?html` disabled`:''}><span class="li-icon">${LI_ICON[k]}</span><span class="grow"><strong>${name}</strong><small>${liTools[k]?liToolSays(liTools[k]):t('Checking…')}</small></span></button>`)}</div>
 <p class="li-error" role="alert">${error||''}</p><p class="fine">${t('Passwords stay encrypted on this Machine and never reach the assistant.')}</p>`);
 if(!d.open)d.showModal()}
async function loginImportOpen(){liReview=null;liPick();
 try{const r=await liPost({do:'tools'});liTools=r.tools||{};if(!liReview&&$('#login-import')?.open)liPick()}catch(err){errCaught(err)}}
function liRow(r,account){const replaces=(r.saved||[]).some(a=>a.toLowerCase()===account.toLowerCase());
 return html`<label class="li-row"><input type="checkbox" data-li-key="${r.key}" checked><span class="login-mark" aria-hidden="true">${(r.site.replace(/^www\./,'')[0]||'?').toUpperCase()}</span><span class="grow"><strong title="${r.site}">${r.site}</strong><span class="login-user" title="${r.username}">${r.username||t('No username')}</span>${replaces?html`<small class="li-note">${t('Replaces the saved {} sign-in',t(account))}</small>`:''}</span></label>`}
function liShow(){const d=liDialog(),r=liReview,account=d.querySelector('[data-li-account]')?.value||r.account||'Work';r.account=account;
 const keep=[...d.querySelectorAll('[data-li-key]')].filter(x=>x.checked).map(x=>x.dataset.liKey),picked=d.querySelector('[data-li-key]')?new Set(keep):null;
 setHTML(d,html`${liHead(t('Choose sign-ins to keep'))}<p class="li-lead">${t(['{} sign-in found in {}.','{} sign-ins found in {}.'],r.rows.length,r.manager)}${r.skipped?' '+t(['{} without a secure web address left out.','{} without a secure web address left out.'],r.skipped):''}</p>
 ${r.rows.length?html`<div class="li-bar"><label class="li-all"><input type="checkbox" data-li-all checked> ${t('All')}</label><label class="li-as">${t('Save as')}<select data-li-account>${LI_ACCOUNTS.map(a=>html`<option value="${a}"${a===account?html` selected`:''}>${t(a)}</option>`)}</select></label></div>
 <div class="li-rows list">${r.rows.map(x=>liRow(x,account))}</div>`:html`<p class="muted">${t('Nothing to import from this one.')}</p>`}
 <p class="li-error" role="alert"></p><div class="actions"><button type="button" class="primary" data-li-keep>${t('Keep')}</button><button type="button" class="ghost" data-li-back>${t('Back')}</button></div>`);
 if(picked)for(const x of d.querySelectorAll('[data-li-key]'))x.checked=picked.has(x.dataset.liKey);liCount()}
function liCount(){const d=$('#login-import'),boxes=[...d.querySelectorAll('[data-li-key]')],n=boxes.filter(x=>x.checked).length,b=d.querySelector('[data-li-keep]'),all=d.querySelector('[data-li-all]');
 if(b){b.textContent=t(['Keep {} sign-in','Keep {} sign-ins'],n);b.disabled=!n}if(all){all.checked=n===boxes.length;all.indeterminate=n>0&&n<boxes.length}}
function liFail(err){errCaught(err);const e=$('#login-import .li-error');if(e)e.textContent=err.message}
async function liStart(args,busy){const d=liDialog();for(const b of d.querySelectorAll('button,input'))b.disabled=true;const e=d.querySelector('.li-error');if(e)e.textContent=busy;
 try{const r=await liPost(args);if(!d.open){liPost({do:'drop',token:r.token}).catch(()=>{});return}liReview={...r,account:'Work'};liShow()}catch(err){liPick();liFail(err)}}
async function liChange(e){const d=$('#login-import');
 if(e.target.matches('[data-li-file]')){const f=e.target.files?.[0];e.target.value='';if(!f)return;
  if(f.size>5*1024*1024){liFail(Error(t('That file is too big (5 MB at most)')));return}
  let text='';try{text=await f.text()}catch(err){liFail(Error(t('That file couldn’t be read as a CSV')));return}
  await liStart({do:'file',text},t('Reading the file…'));text='';return}
 if(e.target.matches('[data-li-all]')){for(const x of d.querySelectorAll('[data-li-key]'))x.checked=e.target.checked;liCount();return}
 if(e.target.matches('[data-li-account]')){liShow();return}
 if(e.target.matches('[data-li-key]'))liCount()}
async function liClick(e){const d=$('#login-import'),b=e.target.closest('button');if(!b)return;
 if('liClose' in b.dataset){d.close();return}
 if(b.dataset.liTool){await liStart({do:'tool',manager:b.dataset.liTool},t('Asking {}…',LI_TOOLS[b.dataset.liTool]));return}
 if('liBack' in b.dataset){const r=liReview;liReview=null;if(r)liPost({do:'drop',token:r.token}).catch(()=>{});liPick();return}
 if('liKeep' in b.dataset&&liReview){const keys=[...d.querySelectorAll('[data-li-key]')].filter(x=>x.checked).map(x=>x.dataset.liKey);if(!keys.length)return;
  b.disabled=true;const r=liReview;
  try{const done=await liPost({do:'keep',token:r.token,keys,account:d.querySelector('[data-li-account]')?.value||'Work'});liReview=null;d.close();toast(t(['Kept {} sign-in.','Kept {} sign-ins.'],done.kept||0));savedLoginsDraw()}
  catch(err){b.disabled=false;liFail(err);if(/expired/i.test(err.message)){liReview=null}}}}
