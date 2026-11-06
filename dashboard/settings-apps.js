// Settings, Apps, top: The Machine's own apps, iPhone and iPad (App Store) and Android (Google Play), from the
// Machine's store links (state.phone_app_store, setup_card.phone_app_nudge). A phone's browser shows its own store
// only; the phone app shows none (it is the app, and an iPhone app never points at Google Play). There is no desktop
// app to download: a computer installs the dashboard from the browser (Settings, General, This device).
function appsRender(){const box=$('#settings-apps');if(!box)return;const p=state?.phone_app_store||{},ok=u=>/^https:\/\//.test(u||'');
 const rows=DEV.phoneApp?[]:[['ios','iPhone and iPad',STORE_APPLE,'App Store'],['android','Android',STORE_PLAY,'Google Play']]
  .filter(([k])=>ok(p[k])&&(DEV.ios?k==='ios':DEV.android?k==='android':true));
 const h=rows.map(([k,name,mark,store])=>html`<div data-app-store="${k}"><span class="grow"><strong${k==='android'?html` translate="no"`:''}>${name}</strong></span><a class="store-badge" href="${safeHref(p[k])}" target="_blank" rel="noopener">${raw(mark)}<span translate="no">${store}</span></a></div>`);
 putHTML($('#apps-list'),html`${h}`);if(box.hidden!==!rows.length)box.hidden=!rows.length}
