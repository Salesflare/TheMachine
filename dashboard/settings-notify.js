// A lazy part (dashboard_parts.LAZY 'settings'): Settings, Notifications and Model's panel, drawn once Settings is in.
// Settings, Notifications (notify.py): each kind by channel, this device, the digest time and quiet hours. The app
// icon's badge is the To-dos count (appBadge in shell-render.js). While this page is in front of them, it tells the Machine so no
// push goes out (a heartbeat a minute; the Machine forgets it after two).
const NOTIFY_KINDS=[['todo','New to-dos','Only what can’t wait: due today, a reply, urgent'],['result','Results and questions','A reply ready to send, a sign-in, a Fleet question'],
 ['reminder','Reminders','Snoozes and waits coming back'],['digest','Morning digest','Meetings, what’s due, what came in overnight'],['evening','Evening digest','']];
const NOTIFY_COLS={push:'Push',telegram:'Telegram',email:'Email'};
const notifyHM=t=>{try{return fmtHM('2000-01-01T'+t)}catch{return t}};
// When the morning digest goes (notify.digest_time): its own time, but never before 5 minutes after the morning's
// snoozes come back (Snoozes land at), unless that falls past midnight or outside the hours
const digestTime=(own,h)=>{const m=/^(\d{2}):(\d{2})$/.exec(h?.morning||'');if(!m)return own;const x=+m[1]*60+ +m[2]+5;if(x>=1440)return own;
 const later=String(Math.floor(x/60)).padStart(2,'0')+':'+String(x%60).padStart(2,'0'),s=h.start,e=h.end;if(later<=own)return own;
 if(s&&e&&s!==e&&!(s<e?s<=later&&later<e:later>=s||later<e))return own;return later};
// Weekly recap (machine/app/recap_settings.py): weekly_recap in config.json, one switch for the recap wherever it comes
const RECAP_DAYS=['Mondays after {}','Tuesdays after {}','Wednesdays after {}','Thursdays after {}','Fridays after {}','Saturdays after {}','Sundays after {}'];
const recapRow=(r,cols)=>!r?'':html`<div class="notify-row" role="row"><span role="rowheader"><strong>Weekly recap</strong><small><span>${t(RECAP_DAYS[(r.weekday||5)-1]||RECAP_DAYS[4],notifyHM(r.at||'16:00'))}</span><span aria-hidden="true"> · </span><a class="learn" href="${HELP}weekly-recap" target="_blank" rel="noopener">Learn more</a></small></span>${cols.map((c,i)=>i<cols.length-1?html`<span class="notify-cell" role="cell"></span>`:html`<span class="notify-cell" role="cell">${r.saveable?html`<button type="button" class="lookup-switch" role="switch" aria-checked="${!!r.on}" aria-label="Weekly recap" data-recap-switch></button>`:html`<span class="notify-na">${r.on?'On':'Off'}</span>`}</span>`)}</div>`;
function renderNotify(){const n=state?.notify,box=$('#settings-notify');
 if(!box||!n){if(box)box.hidden=true;return}box.hidden=false;
 const cols=['push',...(n.telegram?['telegram']:[]),...(n.email?['email']:[])],grid=$('#notify-grid');
 grid.style.setProperty('--notify-cols',cols.length);
 // the digest row's line: its time (set in Work hours below) and Preview, shown on the page, nothing sent
 const h=state.hours||{},own=h.digest_at||n.digest_at||'08:30',at=digestTime(own,h),digest=html`<span>${at===own?t('Work days at {}',notifyHM(at)):t('Work days at {}, after snoozes land',notifyHM(at))}</span><span aria-hidden="true"> · </span><button type="button" class="notify-link" data-notify-preview>${$('#notify-preview').hidden?'Preview':'Hide preview'}</button>`;
 const cell=(kind,label,ch)=>{const p=n.prefs[kind]||{};if(!(ch in p))return html`<span class="notify-cell" role="cell"><span class="notify-na">–</span></span>`;
  return html`<span class="notify-cell" role="cell"><button type="button" class="lookup-switch" role="switch" aria-checked="${!!p[ch]}" aria-label="${label+': '+NOTIFY_COLS[ch]}" data-notify-kind="${kind}" data-notify-channel="${ch}"></button></span>`};
 putHTML(grid,html`<div class="notify-row" role="row"><span role="columnheader"></span>${cols.map(c=>html`<span class="notify-col" role="columnheader">${NOTIFY_COLS[c]}</span>`)}</div>${
  NOTIFY_KINDS.map(([k,label,hint])=>html`<div class="notify-row" role="row"><span role="rowheader"><strong>${label}</strong><small>${k==='digest'?digest:k==='evening'?t('Work days at {}',notifyHM(h.evening_time||'')):hint}</small></span>${cols.map(c=>cell(k,label,c))}</div>`)}${recapRow(n.weekly_recap,cols)}`);
 // In the mobile app this device is the phone: its own push (www/inject.js keeps the id app_push_register gave it),
 // not the web's, which a WebView doesn't have. It turns on with the phone's notifications for the app.
 const phone=phoneAppPush(),mine=phone&&(n.app_devices||[]).find(p=>p.id===phone.id);
 const on=phone?!!mine:pushOn(),can=!phone&&pushOK&&devicePush.perm!=='denied';
 // The app: Turn on asks the phone; once it won't ask again, Open settings (the app's page there). An app from before: a line
 const app=phone&&n.app_push_ready?(!window.machinePhone?(mine?'':'old'):phonePush==='blocked'?'blocked':mine&&phonePush!=='prompt'?'':'off'):'';
 if(phone&&window.machinePhone&&!phonePush)phonePushCheck();
 const device=phone?(app==='blocked'?'Notifications are off for The Machine.':app==='off'?'Push is off here.':mine?'Push is on here.':!n.app_push_ready?'Notifications in the app need The Machine Network. The app works without them.':app==='off'?'Push is off here.':'To get notifications, allow them for The Machine in the phone’s settings.')
  :on?'Push is on here.':!can?'This browser can’t show push here.':n.push_devices?t(['Push is off here, on for {} other device.','Push is off here, on for {} other devices.'],n.push_devices):'Push is off here.';
 // Phones with the mobile app (notify.py, app_push): each with Remove, which stops its notifications
 const phones=(n.app_devices||[]).filter(p=>p!==mine).map(p=>html`<div><span class="grow"><strong>${p.label}</strong><small>Phone with the app</small></span><button type="button" data-app-remove="${p.id}">Remove</button></div>`);
 putHTML($('#notify-more'),html`<div><span class="grow"><strong>This device</strong><small>${device}</small></span>${mine&&!app?html`<button type="button" class="ghost" data-app-test="${mine.id}">Send a test</button>`:''}${!on&&can?html`<button type="button" data-device="push-on">Turn on</button>`:''}${app==='blocked'?html`<button type="button" data-app-settings>Open settings</button>`:app==='off'?html`<button type="button" data-app-on>Turn on</button>`:''}</div>${phones}`)}
$('#settings-notify').addEventListener('click',async e=>{const rs=e.target.closest('[data-recap-switch]');
 if(rs){const on=rs.getAttribute('aria-checked')!=='true';rs.disabled=true;
  try{state.notify.weekly_recap=await notifyPost('recap_set',{on});renderNotify()}catch(err){errCaught(err);toast(err.message,true)}finally{rs.disabled=false}return}
 const sw=e.target.closest('[data-notify-kind]');
 if(sw){const on=sw.getAttribute('aria-checked')!=='true';sw.disabled=true;
  try{state.notify=await notifyPost('notify_set',{kind:sw.dataset.notifyKind,channel:sw.dataset.notifyChannel,on});renderNotify()}catch(err){errCaught(err);toast(err.message,true)}finally{sw.disabled=false}return}
 const test=e.target.closest('[data-app-test]');if(test){test.disabled=true;
  try{await notifyPost('push_test',{app_device:test.dataset.appTest});toast('Test sent. It shows up in a moment.')}catch(err){errCaught(err);toast(err.message,true)}finally{test.disabled=false}return}
 if(e.target.closest('[data-app-settings]')){window.machinePhone?.settings().catch(()=>{});return}
 const ask=e.target.closest('[data-app-on]');if(ask){ask.disabled=true;
  try{const r=await window.machinePhone.pushOn();if(r==='on'){phonePush='granted';toast('Push is on here.');await refresh();deviceRender()}else if(r==='blocked'){phonePush='blocked';deviceRender()}}catch(err){errCaught(err);toast(err.message,true)}finally{ask.disabled=false}return}
 const rm=e.target.closest('[data-app-remove]');if(rm){rm.disabled=true;
  try{await notifyPost('app_push_unregister',{id:rm.dataset.appRemove});state.notify.app_devices=(state.notify.app_devices||[]).filter(p=>p.id!==rm.dataset.appRemove);state.notify.push_devices=Math.max(0,(state.notify.push_devices||1)-1);toast('Removed');renderNotify()}catch(err){errCaught(err);toast(err.message,true)}finally{rm.disabled=false}return}
 const d=e.target.closest('[data-device]');if(d){d.disabled=true;try{await deviceRun(d.dataset.device)}finally{d.disabled=false;renderNotify()}return}
 const pv=e.target.closest('[data-notify-preview]');if(pv){const out=$('#notify-preview');if(!out.hidden){out.hidden=true;renderNotify();return}pv.disabled=true;
  // Right under the digest's row, and scrolled to: the click shows what it opened, also at a short window
  try{const r=await notifyPost('notify_preview');out.textContent=r.empty?'Nothing for a digest right now.':r.text;out.hidden=false;renderNotify();out.scrollIntoView({block:'nearest'})}catch(err){errCaught(err);toast(err.message,true)}finally{pv.disabled=false}}});
// Settings, Model: the model, its plan's usage and resets (renderModelUsage in settings-models.js draws it once Settings is in)
function renderModelPanel(){const m=state.model_status,box=$('#settings-model');if(!box)return;box.hidden=!m&&!state.chat_model?.models?.length;if(!m)return;const now=Date.now()/1000,bg=state.chat_model?.background||m.model;
 const own=m.provider==='mistral',head=html`<div class="list settings-list"><div><span class="grow"><strong title="${bg||''}">${modelName(bg)||'Model unknown'}</strong><small>${[t('Background work'),m.chatgpt?t('Signed in with ChatGPT'):m.claude_plan?t('Uses your Claude plan'):own?t('Uses your Mistral API key'):m.provider,m.plan?t('plan: {}',m.plan):''].filter(Boolean).join(' · ')}</small></span><small class="model-checked" title="${m.checked_at?fmtDHM(m.checked_at,{day:'numeric',month:'short'}):''}">${t('Updated {}',ago(m.checked_at))}</small></div></div>`;
 const bars=orEmpty(html`${(m.windows||[]).filter(w=>!(w.reset&&w.reset<now)).map(w=>html`<div class="usage${w.used>=100?html` full`:''}"><span>${t('{}: {}% used',windowLabel(w.label),+w.used|0)}${w.reset?' · '+t('resets in {}',untilText(w.reset)):''}</span><progress max="100" value="${+w.used|0}">${+w.used|0}%</progress></div>`)}`)||html`<p class="muted">No usage windows reported yet.</p>`;
 const r=m.resets,expiry=r?.credits?.find(c=>c.expires)?.expires;
 // Resets this computer can't count (no Codex CLI signed in to the same account, as on a hosted Machine): no
 // "unknown" count, only the way to ChatGPT's usage page; a team plan's resets are under its workspace there.
 const team=/team|business|enterprise|edu/i.test(m.plan||''),resets=r?html`<div class="list settings-list"><div><span class="grow"><strong>${t('Resets available: {}',r.available)}</strong><small>${r.available?t('A reset starts your ChatGPT usage limits over.')+(expiry?' '+t('The first one expires {}.',localeDate(new Date(expiry*1000),DL,{month:'short',day:'numeric',year:'numeric'})):''):t('Your plan has no usage limit resets right now.')}</small></span>${resetAction(m)}</div></div>`
  :m.usage_page?html`<div class="list settings-list"><div><span class="grow"><strong>Usage limit resets</strong><small>${t(team?'ChatGPT shows them under your team workspace.':'ChatGPT shows them.')}</small></span>${resetAction(m)}</div></div>`:'';
 setHTML($('#model-panel'),html`${head}${limitNote(m)}${m.claude_plan||own?(m.windows||[]).length?bars:'':html`${bars}${resets}`}`)}
