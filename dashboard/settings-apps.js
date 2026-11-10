// Settings, Apps, top: The Machine's own apps, iPhone and iPad (App Store) and Android (Google Play), from the
// Machine's store links (state.phone_app_store, setup_card.phone_app_nudge). A phone's browser shows its own store
// only; the phone app shows none (it is the app, and an iPhone app never points at Google Play). A computer's browser
// also gets Computer: the dashboard installed from the browser, with This device's own prompt and steps
// (settings-device.js: installEvt, appInstall, installSteps). Not on a phone, nor once it runs as the installed app.
// Under them, how the app signs in (appsSignIn): the one place for the phone app. Loads when first needed, with
// Settings' other panels (dashboard_parts.LAZY); deviceRender draws it once it's in.
function appsRender(){const box=$('#settings-apps');if(!box)return;const p=state?.phone_app_store||{},ok=u=>/^https:\/\//.test(u||'');
 const rows=DEV.phoneApp?[]:[['ios','iPhone and iPad',STORE_APPLE,'App Store'],['android','Android',STORE_PLAY,'Google Play']]
  .filter(([k])=>ok(p[k])&&(DEV.ios?k==='ios':DEV.android?k==='android':true));
 const h=rows.map(([k,name,mark,store])=>html`<div data-app-store="${k}"><span class="grow"><strong${k==='android'?html` translate="no"`:''}>${name}</strong></span><a class="store-badge" href="${safeHref(p[k])}" target="_blank" rel="noopener">${raw(mark)}<span translate="no">${store}</span></a></div>`);
 const pc=nudgeable&&!DEV.phoneApp&&!DEV.mobile&&!appInstalled();
 if(pc)h.push(installEvt?html`<div data-app-computer="install"><span class="grow"><strong>Computer</strong><small>Pin it to your taskbar or dock.</small></span><button type="button" data-device="install-app">Install</button></div>`
  :html`<div data-app-computer="steps"><span class="grow"><strong>Computer</strong><small>${installSteps()}</small></span></div>`);
 putHTML($('#apps-list'),html`${h}`);appsSignIn(rows.length);const none=!h.length;if(box.hidden!==none)box.hidden=none}
// Under the stores: how the phone app finds this Machine (phone_app in machine/delivery/push.py). Hosted or on The
// Machine Network: it signs in with the account. Self-hosted and not on the Network: the same line, and folded under
// "Not on the Network?" a QR code of the app's connect link (not on a phone: it can't scan itself) and the address to
// type in. Nothing without a store row (inside the app itself).
function appsSignIn(stores){const el=$('#apps-signin'),p=state?.notify?.phone_app;if(!el)return;
 const h=!stores?'':p?.hosted?html`${t('The app signs in with your account.')}`:
  p?.url?html`${t('The app signs in with your account on The Machine Network.')}<details class="connect-alt phone-own"><summary>${t('Not on the Network?')}</summary>${onPhone()?'':html`<small>${t('Install the app, then scan this with the phone’s camera.')}</small>${p.qr?.length?qrSvg(p.qr):''}`}<small>${htmlT('Or enter this address in the app: {}',html`<code class="phone-url">${p.url}</code>`)}</small></details>`:'';
 putHTML(el,h||html``);el.hidden=!h}
// Install: the browser's own prompt, from this tap (appInstall redraws when it's done)
$('#apps-list')?.addEventListener('click',async e=>{const b=e.target.closest('[data-device]');if(!b)return;b.disabled=true;try{await deviceRun(b.dataset.device)}finally{b.disabled=false}});
