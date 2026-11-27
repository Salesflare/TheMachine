// Settings, Apps, top: The Machine's own apps, iPhone and iPad (App Store) and Android (Google Play), from the
// Machine's store links (state.phone_app_store, setup_card.phone_app_nudge). A phone's browser shows its own store
// only; the phone app shows none (it is the app, and an iPhone app never points at Google Play). A computer's browser
// also gets the desktop app (state.desktop_app, desk.app in machine/delivery/desk.py): Windows, Mac and Linux, so every
// system shows, with this computer's filled and "This computer". Not on a phone, in the phone app or in the desktop app. The
// dashboard installed from the browser stays in Settings, General, This device (settings-device.js).
// Under them, how the app signs in (appsSignIn): the one place for the phone app. Loads when first needed, with
// Settings' other panels (dashboard_parts.LAZY); deviceRender draws it once it's in.
const DL_ICON='<svg class="dl" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11m-4.5-4.5L12 15l4.5-4.5M5 19.5h14"/></svg>';
function appsRender(){const box=$('#settings-apps');if(!box)return;const p=state?.phone_app_store||{},ok=u=>/^https:\/\//.test(u||'');
 const rows=DEV.phoneApp?[]:[['ios','iPhone and iPad',STORE_APPLE,'App Store'],['android','Android',STORE_PLAY,'Google Play']]
  .filter(([k])=>ok(p[k])&&(DEV.ios?k==='ios':DEV.android?k==='android':true));
 const h=rows.map(([k,name,mark,store])=>html`<div data-app-store="${k}"><span class="grow"><strong${k==='android'?html` translate="no"`:''}>${name}</strong></span><a class="store-badge" href="${safeHref(p[k])}" target="_blank" rel="noopener">${raw(mark)}<span translate="no">${store}</span></a></div>`);
 // Mac from the Mac App Store once it has the app (mac_store): its badge, as the phones' stores
 const d=state?.desktop_app;
 if(d&&!onPhone()&&!DEV.phoneApp&&!desktopApp)for(const [k,name] of [['windows','Windows'],['mac','Mac'],['linux','Linux']]){const me=d.on===k,mas=k==='mac'&&ok(d.mac_store);
  h.push(html`<div data-app-desk="${k}"><span class="grow"><strong translate="no">${name}</strong>${me?html`<small>${t('This computer')}</small>`:''}${k==='linux'?html`<small>${t('Also a .deb and a PKGBUILD.')} <a class="learn" href="${safeHref(d.help+'#linux')}" target="_blank" rel="noopener">${t('Learn more')}</a></small>`:''}</span><a class="store-badge${me?'':' alt'}" href="${safeHref(d[k])}" target="_blank" rel="noopener">${raw(mas?STORE_APPLE:DL_ICON)}<span>${mas?html`<span translate="no">Mac App Store</span>`:t('Download')}</span></a></div>`)}
 putHTML($('#apps-list'),html`${h}`);appsSignIn(rows.length);const none=!h.length;if(box.hidden!==none)box.hidden=none}
// Under the stores: how the phone app finds this Machine (phone_app in machine/delivery/push.py). Hosted or on The
// Machine Network: it signs in with the account. Self-hosted and not on the Network: the same line, and folded under
// "Not on the Network?" a QR code of the app's connect link (not on a phone: it can't scan itself) and the address to
// type in. Nothing without a store row (inside the app itself).
function appsSignIn(stores){const el=$('#apps-signin'),p=state?.notify?.phone_app;if(!el)return;
 const h=!stores?'':p?.hosted?html`${t('The app signs in with your account.')}`:
  p?.url?html`${t('The app signs in with your account on The Machine Network.')}<details class="connect-alt phone-own"><summary>${t('Not on the Network?')}</summary>${onPhone()?'':html`<small>${t('Install the app, then scan this with the phone’s camera.')}</small>${p.qr?.length?qrSvg(p.qr):''}`}<small>${htmlT('Or enter this address in the app: {}',html`<code class="phone-url">${p.url}</code>`)}</small></details>`:'';
 putHTML(el,h||html``);el.hidden=!h}
