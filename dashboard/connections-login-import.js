// A lazy part (dashboard_parts.LAZY 'loginimport'): Connections, Sign-ins, Import (loginImportOpen), opened from
// connections-signin.js through lazyRun. Where from, then a review where the owner ticks which to keep and the account
// they go under (Work or Personal). No password ever reaches the page: the service holds what it read until Keep, then
// drops it (login_import.py). Nothing here signs in to a password manager.
// Where from: an export file; LastPass, Bitwarden and Google Password Manager open their own export page in the
// Machine's browser (shown below when this dashboard has the live view, else Open the browser), where the owner signs in
// and the Machine clicks on to the export; the service picks up the download, reads it and deletes it from disk. 1Password has no web export: its
// app's file, or op when that is signed in on the Machine (LastPass's lpass too).
const LI_ICON={file:html`<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 1.75h5l3 3v9.5H4z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/><path d="M8.75 1.75v3.25H12" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>`,
 lastpass:html`<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="2.9" cy="8" r="1.25" fill="currentColor"/><circle cx="6.4" cy="8" r="1.25" fill="currentColor"/><circle cx="9.9" cy="8" r="1.25" fill="currentColor"/><path d="M13.4 4.5v7" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>`,
 '1password':html`<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.25" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M8 4.75v6.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>`,
 bitwarden:html`<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.25 2h9.5v6.2c0 2.9-2.6 4.8-4.75 5.8-2.15-1-4.75-2.9-4.75-5.8z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/><path d="M8 3.5v8.6" stroke="currentColor" stroke-width="1.3"/></svg>`,
 chrome:html`<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M13.6 8.1H8.2v2.2h3.1A3.6 3.6 0 1 1 10.4 5l1.6-1.6A5.9 5.9 0 1 0 13.9 8c0-.3 0-.5-.1-.8z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>`};
const LI_NAMES={lastpass:'LastPass','1password':'1Password',bitwarden:'Bitwarden',chrome:'Google Password Manager'};
const liSteps=k=>({lastpass:[t('Sign in to LastPass.'),t('Open Advanced Options, then Export.'),t('If LastPass emails you, confirm there and export again.')],
 bitwarden:[t('Sign in to Bitwarden.'),t('Pick .csv or .json, then Export vault.')],
 chrome:[t('Sign in to Google.'),t('Choose Export passwords, then Export.')]})[k];
const LI_SIDES=['Work','Personal'];
let liReview=null,liTools={},liWatch=null,liAway=false;
const liPost=args=>signinPost('browser_login_import',args);
function liDialog(){let d=$('#login-import');if(d)return d;
 d=make('dialog',{id:'login-import','aria-labelledby':'li-title'});document.body.append(d);
 d.addEventListener('close',()=>{const r=liReview,w=liWatch;liReview=null;if(r)liPost({do:'drop',token:r.token}).catch(()=>{});
  if(w&&!liAway){liWatch=null;liPost({do:'export_stop',watch:w.token}).catch(()=>{})}});
 d.addEventListener('click',liClick);d.addEventListener('change',liChange);return d}
function liHead(title){return html`<div class="snooze-heading"><h2 id="li-title">${title}</h2><button type="button" data-li-close aria-label="${t('Close')}">×</button></div>`}
const liFileRow=()=>html`<label class="li-source"><span class="li-icon">${LI_ICON.file}</span><span class="grow"><strong>${t('From an export file')}</strong><small>${t('A CSV from 1Password, LastPass, Bitwarden or Chrome')}</small></span><input type="file" accept=".csv,text/csv,.json,application/json" data-li-file class="li-file"></label>`;
const liSays=k=>liTools[k]==='ready'?t('Signed in on this Machine'):k==='1password'?t('Export from the 1Password app'):t('Export in your Machine’s browser');
function liOpen(d){liAway=false;if(!d.open)d.showModal()}
function liPick(error){const d=liDialog();
 setHTML(d,html`${liHead(t('Import sign-ins'))}<p class="li-lead">${t('Bring in sign-ins from your password manager. You choose which to keep.')}</p>
 <div class="li-sources">${liFileRow()}${Object.entries(LI_NAMES).map(([k,name])=>html`<button type="button" class="li-source" data-li-go="${k}"><span class="li-icon">${LI_ICON[k]}</span><span class="grow"><strong>${name}</strong><small>${liSays(k)}</small></span></button>`)}</div>
 <p class="li-error" role="alert">${error||''}</p><p class="fine">${t('Passwords stay encrypted on this Machine and never reach the assistant.')}</p>`);liOpen(d)}
// 1Password: its app writes the file (its website can't), then it comes in like any export file
function liApp(){const d=liDialog();
 setHTML(d,html`${liHead(t('Export from {}','1Password'))}<ol class="li-steps"><li>${t('In the 1Password app on a computer, choose File, then Export.')}</li><li>${t('Pick CSV and save the file.')}</li><li>${t('Choose that file here.')}</li></ol>
 <div class="li-sources">${liFileRow()}</div><p class="li-error" role="alert"></p><div class="actions"><button type="button" class="ghost" data-li-back>${t('Back')}</button></div>
 <p class="fine">${t('Delete the file from that computer when you’re done.')}</p>`);liOpen(d)}
const liView=()=>{const link=state.browser_link||liWatch?.view||'';try{return link&&new URL(link,location.href).origin===location.origin?link:''}catch{return ''}};
// One line for what is left: the Machine clicks on to the export step (login_export_guide.py), the owner signs in and
// confirms it's them. When the page isn't as expected (step 'manual'), the steps to do by hand.
const liLine=({k,step:s})=>s==='working'?t('Going to the export…'):s==='password'?(k==='chrome'?t('Confirm it’s you to export.'):t('Type your master password to export.'))
 :s==='email'?t('Confirm the email {} sent you.',LI_NAMES[k]):s==='manual'?t('Waiting for the export file…'):s==='signin'?liSteps(k)[0]:t('Opening {}…',LI_NAMES[k]);
function liStep(){const d=$('#login-import'),w=liWatch,p=d?.querySelector('.li-wait');if(!p||!w)return;
 p.classList.toggle('li-you',['signin','password','email'].includes(w.step));p.lastChild.textContent=liLine(w);d.querySelector('.li-manual').hidden=w.step!=='manual'}
function liExportShow(){const d=liDialog(),w=liWatch,view=liView();
 setHTML(d,html`${liHead(t('Export from {}',LI_NAMES[w.k]))}<p class="li-wait" role="status"><span class="spin" aria-hidden="true"></span><span></span></p>
 <div class="li-manual" hidden><p class="li-miss">${t('I couldn’t find the next step. Follow these steps:')}</p><ol class="li-steps">${liSteps(w.k).map(s=>html`<li>${s}</li>`)}</ol></div><p class="li-error" role="alert"></p>
 <div class="actions"><button type="button" class="${view?'ghost':'primary'}" data-li-browser>${t('Open the browser')}</button><button type="button" class="ghost" data-li-back>${t('Back')}</button></div>
 <p class="fine">${t('The file is read once, then deleted from your Machine.')}</p>`);
 if(view)d.querySelector('.li-error').before(make('div',{class:'li-view'},make('iframe',{src:view,title:t('The browser')})));liStep();liOpen(d)}
async function liExport(k){const d=liDialog();liBusy(d,t('Opening {}…',LI_NAMES[k]));
 try{const r=await liPost({do:'export',manager:k});liWatch={token:r.watch,k,view:r.view,page:r.page,step:'opening'};liExportShow();liFollow(liWatch)}catch(err){liPick();liFail(err)}}
// Every two seconds until the file is in (also while the owner is away in the browser pane); then the review, the
// dialog opened again if it was closed for the browser
async function liFollow(w){while(liWatch===w){await new Promise(r=>setTimeout(r,2000));if(liWatch!==w)return;let r;
 try{r=await liPost({do:'export_check',watch:w.token})}catch(err){errCaught(err);continue}if(liWatch!==w)continue;
 if(r.state==='waiting'){if(r.step&&r.step!==w.step){w.step=r.step;liStep()}continue}
 liWatch=null;const d=liDialog();
 if(r.state==='review'){liReview={...r,account:'Work'};liOpen(d);liShow();return}
 liPick(r.state==='failed'?r.error:t('The export page waited too long. Try again.'));return}}
function liBusy(d,busy){for(const b of d.querySelectorAll('button,input'))b.disabled=true;const e=d.querySelector('.li-error');if(e)e.textContent=busy}
async function loginImportOpen(){liReview=null;if(liWatch){liExportShow();return}liPick();
 try{const r=await liPost({do:'tools'});liTools=r.tools||{};if(!liReview&&!liWatch&&$('#login-import')?.open&&$('#login-import [data-li-go]'))liPick()}catch(err){errCaught(err)}}
function liRow(r,account){const replaces=(r.saved||[]).some(a=>a.toLowerCase()===account.toLowerCase());
 return html`<label class="li-row"><input type="checkbox" data-li-key="${r.key}" checked><span class="login-mark" aria-hidden="true">${(r.site.replace(/^www\./,'')[0]||'?').toUpperCase()}</span><span class="grow"><strong title="${r.site}">${r.site}</strong><span class="login-user" title="${r.username}">${r.username||t('No username')}</span>${replaces?html`<small class="li-note">${t('Replaces the saved {} sign-in',t(account))}</small>`:''}</span></label>`}
function liShow(){const d=liDialog(),r=liReview,account=d.querySelector('[data-li-account]')?.value||r.account||'Work';r.account=account;
 const keep=[...d.querySelectorAll('[data-li-key]')].filter(x=>x.checked).map(x=>x.dataset.liKey),picked=d.querySelector('[data-li-key]')?new Set(keep):null;
 setHTML(d,html`${liHead(t('Choose sign-ins to keep'))}<p class="li-lead">${t(['{} sign-in found in {}.','{} sign-ins found in {}.'],r.rows.length,r.manager)}${r.skipped?' '+t(['{} without a secure web address left out.','{} without a secure web address left out.'],r.skipped):''}</p>
 ${r.rows.length?html`<div class="li-bar"><label class="li-all"><input type="checkbox" data-li-all checked> ${t('All')}</label><label class="li-as">${t('Save as')}<select data-li-account>${LI_SIDES.map(a=>html`<option value="${a}"${a===account?html` selected`:''}>${t(a)}</option>`)}</select></label></div>
 <div class="li-rows list">${r.rows.map(x=>liRow(x,account))}</div>`:html`<p class="muted">${t('Nothing to import from this one.')}</p>`}
 <p class="li-error" role="alert"></p><div class="actions"><button type="button" class="primary" data-li-keep>${t('Keep')}</button><button type="button" class="ghost" data-li-back>${t('Back')}</button></div>`);
 if(picked)for(const x of d.querySelectorAll('[data-li-key]'))x.checked=picked.has(x.dataset.liKey);liCount()}
function liCount(){const d=$('#login-import'),boxes=[...d.querySelectorAll('[data-li-key]')],n=boxes.filter(x=>x.checked).length,b=d.querySelector('[data-li-keep]'),all=d.querySelector('[data-li-all]');
 if(b){b.textContent=t(['Keep {} sign-in','Keep {} sign-ins'],n);b.disabled=!n}if(all){all.checked=n===boxes.length;all.indeterminate=n>0&&n<boxes.length}}
function liFail(err){errCaught(err);const e=$('#login-import .li-error');if(e)e.textContent=err.message}
async function liStart(args,busy){const d=liDialog();liBusy(d,busy);
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
 const k=b.dataset.liGo;if(k){if(liTools[k]==='ready')await liStart({do:'tool',manager:k},t('Asking {}…',LI_NAMES[k]));else if(k==='1password')liApp();else await liExport(k);return}
 // the browser pane covers the dashboard: the dialog steps aside and comes back with the review
 if('liBrowser' in b.dataset){const link=state.browser_link;if(browserPane()){liAway=true;d.close()}else if(link)window.open(link,'_blank','noopener');
  try{const r=await signinPost('browser_focus',{page:liWatch?.page});if(!link&&!r.shown)toast(t('I couldn’t reach your Machine’s browser.'),true)}catch(err){errCaught(err)}return}
 if('liBack' in b.dataset){const r=liReview,w=liWatch;liReview=liWatch=null;if(r)liPost({do:'drop',token:r.token}).catch(()=>{});if(w)liPost({do:'export_stop',watch:w.token}).catch(()=>{});liPick();return}
 if('liKeep' in b.dataset&&liReview){const keys=[...d.querySelectorAll('[data-li-key]')].filter(x=>x.checked).map(x=>x.dataset.liKey);if(!keys.length)return;
  b.disabled=true;const r=liReview;
  try{const done=await liPost({do:'keep',token:r.token,keys,account:d.querySelector('[data-li-account]')?.value||'Work'});liReview=null;d.close();toast(t(['Kept {} sign-in.','Kept {} sign-ins.'],done.kept||0));lazyRun('logins',savedLoginsDraw)}
  catch(err){b.disabled=false;liFail(err);if(/expired/i.test(err.message)){liReview=null}}}}
