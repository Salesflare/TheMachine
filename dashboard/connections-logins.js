// A lazy part (dashboard_parts.LAZY 'logins'): Connections, Sign-ins. The saved sign-ins, one row per account
// (Import is the 'loginimport' part). connections-signin.js calls in through lazyRun.
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
// Work and Personal: the sides a sign-in is saved under (the list, the sign-in dialog's Save as)
const LI_ACCOUNTS=['Work','Personal'];
