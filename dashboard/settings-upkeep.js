// Settings, General, Version and Settings, Model, Search by meaning. Hosted: the control plane's summary (version,
// meaning in /_machine/account) with Update now and the switch, through the owner's sign-in on this very host
// (/_machine/update, /_machine/meaning; a change only from this page). Until the control plane sends them, nothing
// shows here: its Overview still has both. Self-hosted: the release this code is (state.source_url) and whether
// config.json has an embeddings block, read-only, since updates and that block are this computer's.
SETTINGS_OF['settings-version']='general';SETTINGS_OF['settings-meaning']='model';
var upkeep={busy:'',timer:null};  // var: settingsSync may run before this line
const UPKEEP_NOTE={waiting:'Waiting for the current work to finish…',model:'Getting the model ready…',first:'Reading your notes and conversations for the first time…'};
// Only what changed is written: Settings' tabs follow every change under #settings (settingsSync), which calls back here
// h: an html`` result, so every value from the control plane is escaped (setHTML takes nothing else)
const upkeepSet=(el,h)=>{if(el.dataset.shown!==h.s){el.dataset.shown=h.s;setHTML(el,h)}},upkeepHide=(el,off)=>{if(el.hidden!==off)el.hidden=off};
function upkeepShown(){if(state.account_url)loadAccount();upkeepRender()}
const upkeepCloud=()=>{const d=typeof acct!=='undefined'&&acct.data;return d&&!d.error?d:null};
// What to show: the control plane's when it sends it (hop: with its buttons), else this Machine's own when it isn't hosted
function upkeepVersion(){const d=upkeepCloud();if(d?.version)return{...d.version,hop:!!d.hop};if(state.manage_url)return null;
 const tag=/\/tree\/(release-\d{8}-\d{4})$/.exec(state.source_url||'')?.[1];return tag?{release:tag,state:'',local:true}:null}
function upkeepMeaning(){const d=upkeepCloud();if(d&&'meaning' in d)return d.meaning?{...d.meaning,on:!!d.meaning.on,want:!!d.meaning.want,hop:!!d.hop}:null;if(state.manage_url||!state.meaning)return null;
 return{on:!!state.meaning.on,want:!!state.meaning.on,local:true}}
function upkeepRender(){const v=upkeepVersion(),m=upkeepMeaning(),vb=$('#settings-version'),mb=$('#settings-meaning');if(!vb||!mb)return;
 upkeepHide(vb,!v);if(v){const what=v.release?t('Release {}',v.release.replace(/^release-/,'').slice(0,8)):v.commit||'';
  const now=v.state==='updating'?t('Updating, a few minutes. Your data stays.'):v.state==='behind'?t('A newer version is ready.'):v.state==='current'?t('Up to date'):'';
  const go=v.hop&&v.state==='updating'?html`<button type="button" class="head-link" disabled>${t('Updating…')}</button>`:v.hop&&v.state==='behind'?html`<button type="button" class="head-link" id="version-update"${upkeep.busy==='update'?raw(' disabled'):''}>${t('Update now')}</button>`:'';
  upkeepSet($('#version-list'),html`<div><span class="grow"><strong>The Machine</strong><small>${[what,now].filter(Boolean).join(' · ')}</small>${
   v.failed&&v.state!=='updating'?html`<small class="upkeep-error">${t('The last update didn’t finish. Your Machine kept the version before it.')}</small>`:''}</span>${go}</div>`);
  clearTimeout(upkeep.timer);if(v.hop&&v.state==='updating')upkeep.timer=setTimeout(()=>upkeepGet('update'),30000)}
 upkeepHide(mb,!m);if(m){const turning=m.want!==m.on&&!m.error;
  const head=m.error?t('Not on yet'):turning?(m.want?t('Turning on…'):t('Turning off…')):m.on?t('On'):t('Off');
  const more=m.error?t('It couldn’t be turned on. Your Machine tries again by itself.'):m.on&&!turning&&UPKEEP_NOTE[m.note]?t(UPKEEP_NOTE[m.note]):'';
  const cost=m.local?t('Set up by hand on this computer. Learn more shows how.'):m.big?t('It uses about half a gigabyte of memory.'):m.memory_gb?t('It uses about half a gigabyte of your {} GB, so a busy Machine can slow down.',m.memory_gb):'';
  const sw=m.hop?html`<button type="button" id="meaning-switch" class="lookup-switch" role="switch" aria-checked="${m.want?'true':'false'}" aria-label="${t('Search by meaning')}"${upkeep.busy==='meaning'?raw(' disabled'):''}></button>`:'';
  upkeepSet($('#meaning-list'),html`<div><span class="grow"><strong>${head}</strong>${[more,cost].filter(Boolean).map(x=>html`<small>${x}</small>`)}${m.local?cantSaveMore('embeddings'):''}</span>${sw}</div>`);
  upkeepHide($('#meaning-private'),!!m.local)}}
async function upkeepCall(part,body){const r=await fetch('/_machine/'+part,{credentials:'same-origin',redirect:'manual',...(body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{})});
 if(!r.ok)throw Error(r.status===401?'Can’t reach your account right now. Try again.':'Can’t reach your Machine right now. Try again in a moment.');
 const view=await r.json();if(acct.data&&!acct.data.error)acct.data[part==='update'?'version':'meaning']=view;return view}
async function upkeepGet(part){try{await upkeepCall(part)}catch(e){errCaught(e)}upkeepRender()}
async function upkeepPress(part,body){if(upkeep.busy)return;upkeep.busy=part;upkeepRender();
 try{await upkeepCall(part,body)}catch(e){errCaught(e);notice(t(e.message))}finally{upkeep.busy='';upkeepRender()}}
$('#settings-version').addEventListener('click',e=>{if(e.target.closest('#version-update'))upkeepPress('update',{})});
$('#settings-meaning').addEventListener('click',e=>{const b=e.target.closest('#meaning-switch');if(b)upkeepPress('meaning',{on:b.getAttribute('aria-checked')!=='true'})});
// Served as a part that loads when first needed (dashboard_parts.LAZY), with Settings' other panels: a page
// drawn before they came draws Settings' panels now (render skipped them). Inline (the tests, the demo) these parts run
// before shell-render.js, which draws them itself.
if(self.LAZY_FILES?.settings&&drawnWhole)try{renderHours();renderLocale();renderAgents();renderSignatures();renderLookups();renderAddresses();renderSecurity();renderVoices();renderSkills();appsRender()}catch(e){errCaught(e);console.error(e)}
