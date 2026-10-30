const DAYS=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];let hoursDirty=false;
function zones(){try{return Intl.supportedValuesOf('timeZone')}catch(e){return[]}}
// Settings in tabs, a pill row like Graph and Connections. A Machine linked to a control plane account (hosted, or
// paired with the Network: status account_url) gets Account first, the account in short with buttons to its pages.
// Each part of Settings goes to a tab by its id; a part without one goes with the part before it (a heading with what
// follows it). A tab with nothing to show is left out. Links: #settings, #settings/skills (or #settings=skills); the last tab is kept.
const SETTINGS_TABS=[['account','Account'],['general','General'],['security','Security'],['notify','Notifications'],['writing','Writing'],['skills','Skills'],['model','Model']];
const SETTINGS_OF={'settings-notify':'notify','settings-acct':'account','settings-addresses':'account','settings-domains':'account',hours:'notify','settings-signatures':'writing','settings-voices':'writing','settings-skills':'skills','settings-model':'model','agents-settings':'model','settings-browser':'general','settings-fleet':'general','settings-account-block':'general','settings-locale':'general','settings-dictation':'general','settings-security':'security','settings-lookups':'security','settings-share':'security'};
let settingsTab=localStorage.getItem('settings-tab')||'account',settingsNow='';
{const bar=document.createElement('div');bar.className='sub-tabs';bar.id='settings-tabs';bar.setAttribute('role','tablist');bar.setAttribute('aria-label','Settings');
 bar.innerHTML=SETTINGS_TABS.map(([id,label])=>`<button type="button" role="tab" data-settings-tab="${id}" aria-selected="false">${label}</button>`).join('');
 $('#settings').prepend(bar)}
function settingsSync(){const s=$('#settings'),bar=$('#settings-tabs'),shown=new Set(),set=(el,k,v)=>{if(el[k]!==v)el[k]=v};if(s.firstElementChild!==bar)s.prepend(bar);
 let tab='general';for(const el of s.children){if(el===bar)continue;tab=SETTINGS_OF[el.id]||(el.classList.contains('section-head')?SETTINGS_OF[el.nextElementSibling?.id]||'general':tab);el.dataset.stab=tab;if(!el.hidden&&!el.classList.contains('section-head'))shown.add(tab)}
 settingsNow=shown.has(settingsTab)?settingsTab:SETTINGS_TABS.map(t=>t[0]).find(t=>shown.has(t))||'general';if(settingsNow==='account'&&!s.hidden)loadAccount();if(settingsNow==='general'&&!s.hidden)loadDictation();if(!s.hidden)helpLink('settings');
 for(const el of s.children)if(el!==bar)el.classList.toggle('stab-off',el.dataset.stab!==settingsNow);
 for(const b of bar.querySelectorAll('[data-settings-tab]')){set(b,'hidden',!shown.has(b.dataset.settingsTab));const on=String(b.dataset.settingsTab===settingsNow);if(b.getAttribute('aria-selected')!==on)b.setAttribute('aria-selected',on)}needsYouPlace()}
new MutationObserver(settingsSync).observe($('#settings'),{childList:true,subtree:true,attributes:true,attributeFilter:['hidden']});
const settingsHash=()=>{if(!$('#settings').hidden)history.replaceState(null,'',location.pathname+location.search+'#settings/'+settingsNow)};
function showSettings(tab){if(tab==='hours')tab='notify';if(SETTINGS_TABS.some(t=>t[0]===tab)){settingsTab=tab;localStorage.setItem('settings-tab',tab)}const was=!$('#settings').hidden;
 for(const b of document.querySelectorAll('nav button[data-tab]')){b.classList.remove('active');b.setAttribute('aria-current','false')}for(const x of document.querySelectorAll('main>section'))x.hidden=x.id!=='settings';$('#open-settings').setAttribute('aria-current','page');
 settingsSync();settingsHash();if(!was)scrollTo(0,0);requestAnimationFrame(()=>{tabsShow($('#settings-tabs'));if(!was)kbLand()})}
$('#open-settings').onclick=()=>showSettings();
$('#settings-tabs').onclick=e=>{const b=e.target.closest('[data-settings-tab]');if(!b)return;showSettings(b.dataset.settingsTab)};
$('nav').addEventListener('click',e=>{if(!e.target.closest('button')?.dataset.tab)return;$('#open-settings').setAttribute('aria-current','false');if(location.hash.startsWith('#settings'))history.replaceState(null,'',location.pathname+location.search)});
$('#settings-shared').onclick=()=>sharedOpen((graphSharing.find(x=>x.confirmed)||graphSharing[0])?.fleet);
$('#settings-fleet-rules').onclick=()=>{document.querySelector('nav [data-tab="fleet"]').click();fleetShown.then(()=>{showFleetPane('sharing');$('#fleet-view').scrollIntoView({block:'start',behavior:'smooth'})})};
const CLOUD='https://app.themachine.computer';
  // the hosted service (beta): a self-hosted Machine's Fleet account lives there
// Settings, Account: the owner's account in short from the control plane, and a button per page of it, each in a new tab.
// Hosted: the control plane answers on this very host, with the owner's sign-in here (/_machine/account), and a button is
// a POST to /_machine/account-hop: a one-time hop (a minute, this browser only) that opens that page signed in (Stripe's
// billing portal included, which can't be framed). Self-hosted and paired: this Machine asks (api/account) and the
// buttons link to the account, which asks to sign in. Read when the tab opens, at most once a minute.
var acct={at:0,data:null,busy:false};  // var: settingsSync may run before this line
const ACCT_GO={account:'Open account',plan:'Change plan',portal:'Billing',cancel:'Cancel plan',connections:'Manage',fleet:'Fleet'};
const acctDay=d=>{const x=new Date(d+'T12:00:00');return isNaN(x)?d:humanDay(x)};  // the app's style: Fri 20 Nov, the year only when not this one
function acctGo(d,key,cls='head-link'){if(!(d.actions||[]).includes(key))return'';const label=esc(ACCT_GO[key])+' ↗';
 if(d.hop)return`<form method="post" action="/_machine/account-hop" target="_blank"><input type="hidden" name="to" value="${key}"><button class="${cls}" data-acct-go="${key}">${label}</button></form>`;
 const url=d.links?.[key];return /^https:\/\//.test(url||'')?`<a class="${cls}" href="${esc(url)}" target="_blank" rel="noopener" data-acct-go="${key}">${label}</a>`:''}
async function loadAccount(force){if(!acct||acct.busy||!state.account_url||(!force&&acct.data&&Date.now()-acct.at<60000))return;acct.busy=true;if(!acct.data)renderAccount();
 try{const d=await request(state.manage_url?'/_machine/account':'api/account');acct.data=d.error?{error:d.error}:{...d,hop:!!(state.manage_url&&d.hop)}}catch(e){errCaught(e);acct.data={error:'Can’t reach your account right now.'}}finally{acct.busy=false;acct.at=Date.now()}renderAccount()}
function renderAccount(){const d=acct.data,list=$('#acct-list'),foot=$('#acct-foot'),out=state.manage_url?'<form method="post" action="/_machine/logout" class="acct-end"><button class="head-link">Sign out</button></form>':'';
 if(!d||d.error){$('#acct-email').textContent='';list.innerHTML=`<div><span class="grow">${d?esc(d.error):'Loading…'}</span></div>`;foot.innerHTML=(d&&state.account_url?`<a class="head-link" href="${esc(state.account_url)}" target="_blank" rel="noopener">Open account ↗</a>`:'')+out;return}
 $('#acct-email').textContent=d.email||'';const rows=[],p=d.plan,n=d.next_invoice,srv=d.server;
 if(p)rows.push(`<div><span class="grow"><strong>${esc(p.name)}</strong><span class="acct-status s-${esc(p.status)}">${esc(p.status_text)}</span>${p.price?`<small>${esc(p.price)}</small>`:''}</span>${acctGo(d,'plan')}${n?'':acctGo(d,'portal')}</div>`);
 if(n)rows.push(`<div><span class="grow">Next invoice<small>${esc(acctDay(n.date))}${n.amount?' · '+esc(n.amount):''}</small></span>${acctGo(d,'portal')}</div>`);
 if(p?.cancel_at)rows.push(`<div><span class="grow">Ends<small>${esc(acctDay(p.cancel_at))}</small></span></div>`);
 if(srv)rows.push(`<div><span class="grow">Machine<small>${esc(srv.size)} · ${esc(srv.region)}</small></span></div>`);
 if(srv){const c=d.connections||[];rows.push(`<div><span class="grow">Connected accounts<small>${c.length?c.map(x=>esc(x.service)+': '+esc(x.email)).join('<br>'):'None yet'}</small></span>${acctGo(d,'connections')}</div>`)}
 const fl=d.fleets||[],role={owner:'Owner',admin:'Admin',member:'Member'};
 rows.push(fl.length?fl.map((f,i)=>`<div><span class="grow">${esc(f.name)}<small>${[role[f.role]||esc(f.role),f.people===1?'1 person':f.people+' people',f.seats!=null?(f.seats===1?'1 seat':f.seats+' seats'):''].filter(Boolean).join(' · ')}</small></span>${i?'':acctGo(d,'fleet')}</div>`).join(''):`<div><span class="grow">Fleet<small>None yet</small></span>${acctGo(d,'fleet')}</div>`);
 list.innerHTML=rows.join('');foot.innerHTML=acctGo(d,'account')+out+(d.actions?.includes('cancel')?`<div class="acct-cancel">${acctGo(d,'cancel','acct-quiet')}</div>`:'')}
function renderHours(){const account=$('#settings-account-block'),linked=!!state.account_url;$('#settings-acct').hidden=!linked;account.hidden=linked;$('#manage').hidden=$('#sign-out').hidden=true;$('#settings-fleet').hidden=!state.fleet?.on;$('#settings-shared-row').hidden=!state.fleet?.on;if(linked){if(!acct.data)renderAccount()}else{const cli=`More settings live on this Machine. <a href="${HELP}settings#on-this-machine" target="_blank" rel="noopener">Learn more</a>`,paired=!!state.fleet;$('#settings-more').innerHTML=paired?`<strong>Your Fleet account</strong><small>Paired with your Fleet. Seats, invites and billing are in your account.</small><small>${cli}</small>`:`<strong>The Machine Network</strong><span class="alpha">Beta</span><small>Connect with friends for free, or with teammates in a Fleet. Sign in, then pair with the code from your account.</small><small>${cli}</small>`;const b=$('#settings-cloud');b.href=CLOUD+(paired?'/account':'/start');b.textContent=paired?'Open your account':'Join the Network';b.hidden=false}const h=state.hours,form=$('#hours');if(!h){form.hidden=true;return}form.hidden=false;if(hoursDirty)return;
 $('#hours-days').innerHTML=DAYS.map((d,i)=>`<button type="button" data-day="${i+1}" aria-pressed="${h.days.includes(i+1)}" aria-label="${['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][i]}">${d}</button>`).join('');
 $('#hours-start').value=h.start;$('#hours-end').value=h.end;$('#hours-morning').value=h.morning;$('#hours-digest').value=h.digest_at;
 const list=[...new Set([h.timezone,...zones()])].sort();$('#hours-zone').innerHTML=list.map(z=>`<option${z===h.timezone?' selected':''}>${esc(z)}</option>`).join('');
 const here=Intl.DateTimeFormat().resolvedOptions().timeZone,detect=$('#hours-detect');detect.hidden=!here||here===h.timezone;detect.textContent=t('Use this device’s: {}',here);detect.dataset.zone=here||'';
 for(const el of form.querySelectorAll('input,select,button'))el.disabled=!h.saveable;$('#hours-error').textContent=h.saveable?'':'Change these in config.json (work_hours) on this computer.'}
$('#hours').addEventListener('input',()=>{hoursDirty=true});
$('#hours').addEventListener('click',e=>{const day=e.target.closest('[data-day]');if(day){day.setAttribute('aria-pressed',day.getAttribute('aria-pressed')!=='true');hoursDirty=true}
 if(e.target.id==='hours-detect'){const z=e.target.dataset.zone,sel=$('#hours-zone');if(![...sel.options].some(o=>o.value===z))sel.add(new Option(z,z));sel.value=z;e.target.hidden=true;hoursDirty=true}});
$('#hours').addEventListener('submit',async e=>{e.preventDefault();const days=[...document.querySelectorAll('#hours-days [aria-pressed="true"]')].map(b=>Number(b.dataset.day));
 const args={days,start:$('#hours-start').value,end:$('#hours-end').value,morning:$('#hours-morning').value,digest_at:$('#hours-digest').value,timezone:$('#hours-zone').value};
 try{if(!days.length)throw Error('Pick at least one work day.');for(const k of['start','end','morning','digest_at'])if(!args[k])throw Error('Fill in every time.');
  $('#hours-save').disabled=true;state.hours=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'set_work_hours',args})});
  hoursDirty=false;$('#hours-error').textContent='';renderHours();notice('Work hours saved.')}catch(err){errCaught(err);$('#hours-error').textContent=err.message}finally{$('#hours-save').disabled=!state.hours?.saveable}});
// Language and region (locale_prefs.py): the region sets the date order and the usual clock; Time format overrides the
// clock, Language the words (i18n/). Saved at once.
const LOCALE_REGIONS='AD AE AF AG AI AL AM AO AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BM BN BO BR BS BT BW BY BZ CA CD CF CG CH CI CL CM CN CO CR CU CV CW CY CZ DE DJ DK DM DO DZ EC EE EG ER ES ET FI FJ FM FO FR GA GB GD GE GG GH GI GL GM GN GQ GR GT GU GW GY HK HN HR HT HU ID IE IL IM IN IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MG MH MK ML MM MN MO MP MR MT MU MV MW MX MY MZ NA NC NE NG NI NL NO NP NR NZ OM PA PE PF PG PH PK PL PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SI SK SL SM SN SO SR SS ST SV SY SZ TC TD TG TH TJ TL TM TN TO TR TT TV TW TZ UA UG US UY UZ VA VC VE VG VI VN VU WS XK YE ZA ZM ZW'.split(' ');
const regionName=(()=>{let n=null,lang='';return c=>{if(lang!==I18N.lang){lang=I18N.lang;try{n=new Intl.DisplayNames([lang||'en'],{type:'region'})}catch{n=null}}try{return n?.of(c)||c}catch{return c}}})();
let localeGuessed=false;  // no region yet (self-hosted): the browser's, saved once on first load, as signup does
function guessLocale(){localeGuessed=true;let zone='',language='';try{zone=Intl.DateTimeFormat().resolvedOptions().timeZone||'';language=navigator.language||''}catch{}
 request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'set_locale',args:{browser:{zone,language}}})})
  .then(l=>{if(l?.region){state.locale=l;render()}}).catch(()=>{})}
function renderLocale(){const l=state.locale,box=$('#settings-locale');box.hidden=!l;if(!l)return;
 if(!l.region&&l.saveable&&!localeGuessed)guessLocale();
 const reg=$('#locale-region'),clk=$('#locale-clock'),sample=new Date();sample.setHours(14,5,0,0);
 i18nLanguages(l);if(!reg.options.length||reg.dataset.for!==(l.region||'')+I18N.lang){const list=LOCALE_REGIONS.map(c=>[c,regionName(c)]).sort((a,b)=>a[1].localeCompare(b[1]));
  reg.innerHTML=(l.region?'':'<option value="" selected>Not set</option>')+list.map(([c,n])=>`<option value="${c}"${c===l.region?' selected':''}>${esc(n)}</option>`).join('');reg.dataset.for=(l.region||'')+I18N.lang}
 const auto=l.auto_hour12?'2:05 PM':'14:05';
 $('#locale-auto').textContent='Automatic: '+auto;
 clk.innerHTML=[['auto','Automatic'],['12h','12-hour'],['24h','24-hour']].map(([v,t])=>`<option value="${v}"${v===l.clock?' selected':''}>${t}</option>`).join('');
 $('#locale-sample').textContent=fmtDHM(sample,{weekday:'short',day:'numeric',month:'short'});
 for(const el of [reg,clk,$('#locale-language')])el.disabled=!l.saveable}
$('#settings-locale').addEventListener('change',async e=>{const el=e.target;if(!el.matches('select')||!el.value)return;const l=state.locale||{};
 const args=el.id==='locale-language'?{language:el.value}:el.id==='locale-region'?{locale:(l.language||'en').split('-')[0]+'-'+el.value}:{clock:el.value};el.disabled=true;
 try{state.locale=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'set_locale',args})});await i18nLoad(state.locale.language);DL=state.locale.date_locale||DL;H12=!!state.locale.hour12;i18nRerender();notice(t('Saved.'))}
 catch(err){errCaught(err);notice(err.message);renderLocale()}finally{el.disabled=!state.locale?.saveable}});
// Settings, General, Voice input (voice_input.py): where speech becomes text (this Machine, or OpenAI with the owner's
// key when OpenClaw has one), how accurate the Machine's own model is, and the language (Detect picks among the app's).
const MIC_LANGS=[['de','Deutsch'],['en','English'],['es','Español'],['fr','Français'],['it','Italiano'],['nl','Nederlands'],['pt','Português']];
let dictation={at:0,busy:false,timer:null};
async function loadDictation(force){if(dictation.busy||(!force&&Date.now()-dictation.at<30000))return;dictation.busy=true;if(!state.dictation)renderDictation();
 try{state.dictation=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'voice_status',args:{settings:true}})});dictation.at=Date.now()}catch{}
 finally{dictation.busy=false}renderDictation()}
// One short line: which engine is in use, and how this Machine's own is getting on
function dictationNote(d){const l=d.local||{},auto=d.engine==='auto';
 if(d.in_use==='openai')return t('In use: OpenAI. Your recordings go to OpenAI.');
 if(l.state==='ready')return t('In use: this Machine. Your recordings never leave it.');
 if(l.state==='failed')return l.error||t('Getting voice ready failed. Try again later.');
 if(l.state==='preparing')return t(auto?'Getting ready (in the background). Until then, your browser writes it down.':'Getting ready (in the background).');
 return t(auto?'This Machine gets ready in the background when it’s quiet. Until then, your browser writes it down.':'This Machine gets ready in the background when it’s quiet.')}
function renderDictation(){const d=state.dictation,box=$('#settings-dictation'),list=$('#dictation-list');box.hidden=false;
 if(!d||d.demo){list.innerHTML=`<div><span class="grow"><small>${esc(t(d?MIC_DEMO:'Loading…'))}</small></span></div>`;return}
 const opt=(v,label,on,off)=>`<option value="${v}"${on?' selected':''}${off?' disabled':''}>${esc(t(label))}</option>`,l=d.local||{};
 list.innerHTML=`<div><span class="grow"><strong>${esc(t('Turned into text'))}</strong><small id="dictation-note">${esc(dictationNote(d))}${l.state==='failed'&&d.in_use==='local'?` <button type="button" class="quiet" data-dictation-retry>${esc(t('Try again'))}</button>`:''}</small></span><select id="dictation-engine" aria-label="${esc(t('Turned into text'))}">${opt('auto','Automatic',d.engine==='auto')}${opt('local','On this Machine',d.engine==='local')}${opt('openai',d.openai===null?'With OpenAI (checking…)':'With OpenAI',d.engine==='openai',!d.openai&&d.engine!=='openai')}</select></div>`
  +(d.openai===false&&d.engine!=='local'?`<div class="dictation-fine"><small>${esc(t('OpenAI needs OpenAI set up in OpenClaw: an API key, or a ChatGPT sign-in that allows audio.'))}</small></div>`:'')
  +(d.in_use==='local'?`<div><span class="grow"><strong>${esc(t('Accuracy'))}</strong><small>${esc(t(d.model==='base'?'Quicker, but it gets more words wrong.':'Best for most languages. Slower on a small Machine.'))}</small></span><select id="dictation-model" aria-label="${esc(t('Accuracy'))}">${opt('small','More accurate',d.model==='small')}${opt('base','Faster',d.model==='base')}</select></div>`:'')
  +`<div><span class="grow"><strong>${esc(t('Language'))}</strong><small>${esc(t('Detect works for every app language. Picking yours is a little faster.'))}</small></span><select id="dictation-language" aria-label="${esc(t('Voice input language'))}"><option value=""${d.language?'':' selected'}>${esc(t('Detect'))}</option>${MIC_LANGS.map(([c,n])=>`<option value="${c}" translate="no"${d.language===c?' selected':''}>${n}</option>`).join('')}</select></div>`
  +(d.talk?`<div><span class="grow"><strong>${esc(t('Talk live'))}</strong><small id="talk-note">${esc(t(d.talk.ready==null?'Checking…':d.talk.ready?'Ready. Tap Talk in the menu, or the wave in a to-do’s chat.':'Needs OpenAI set up in OpenClaw: a ChatGPT sign-in, or an API key.'))}</small></span></div>`
   +(d.talk.ready&&d.talk_voice?`<div><span class="grow"><strong>${esc(t('Voice'))}</strong><small>${esc(t('How The Machine sounds when you talk live.'))}</small></span><button type="button" class="quiet talk-sample" data-talk-sample aria-label="${esc(t('Play a sample'))}" title="${esc(t('Play a sample'))}">${PLAY}</button><select id="talk-voice" aria-label="${esc(t('Voice'))}">${TALK_VOICES.map(n=>`<option value="${n}" translate="no"${d.talk_voice===n?' selected':''}>${n[0].toUpperCase()+n.slice(1)}</option>`).join('')}</select></div>`:''):'');
 // Still preparing, or the Machine still asking OpenClaw what OpenAI can do here (it answers at once, and fills that in later)
 clearTimeout(dictation.timer);if((l.state==='preparing'||d.openai==null||d.talk&&d.talk.ready==null)&&!$('#settings').hidden)dictation.timer=setTimeout(()=>loadDictation(true),2000)}
$('#settings-dictation').addEventListener('change',async e=>{const el=e.target;if(!el.matches('select'))return;const key={'dictation-engine':'engine','dictation-model':'model','dictation-language':'language','talk-voice':'talk_voice'}[el.id];if(!key)return;el.disabled=true;
 try{state.dictation=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'voice_prefs',args:{[key]:el.value}})}).then(r=>({talk:state.dictation?.talk,...r}));micPrepped=false;notice(t('Saved.'))}catch(err){errCaught(err);notice(err.message)}renderDictation()});
// Talk live's voices (voice_input.TALK_VOICES): a few seconds of each, from the Machine itself (brand/voices)
const TALK_VOICES=['cedar','marin','ash','ballad','coral','echo','sage','shimmer','verse','alloy'];
const PLAY='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z"/></svg>';
let talkSample=null;
$('#settings-dictation').addEventListener('click',e=>{const b=e.target.closest('[data-talk-sample]');if(!b)return;const name=$('#talk-voice')?.value;if(!TALK_VOICES.includes(name))return;
 try{talkSample?.pause()}catch{}talkSample=new Audio('brand/voices/'+name+'.mp3');talkSample.play().catch(()=>toast(t('That sample couldn’t play.'),true))});
$('#settings-dictation').addEventListener('change',e=>{if(e.target.id==='talk-voice')$('[data-talk-sample]')?.click()});  // hear the one just picked
$('#settings-dictation').addEventListener('click',async e=>{if(!e.target.closest('[data-dictation-retry]'))return;try{state.dictation=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'voice_prepare',args:{}})})}catch(err){errCaught(err);notice(err.message)}renderDictation()});
// Codex and Claude Code (Settings, Model; agent_remote.py): where Hand to Codex and Hand to Claude Code send a to-do.
// Only what this Machine needs is asked: Codex on the owner's computer is one line (chosen on the setup page); Codex
// cloud asks its environment ID, and its branch once that is in; Claude Code asks a session link, and once one is in,
// the connector that brings Claude's result back. Runs on (agents.claude.device) is kept as it was.
function renderAgents(){const f=$('#agents-settings'),a=state.agents_settings;f.hidden=!a;if(!a||agentsDirty)return;
 const onDevice=a.codex_where==='device',onMachine=a.codex_where==='machine',set=onDevice||onMachine,ch=$('#agents-codex-change');
 $('#agents-codex-row').hidden=!set;$('#agents-env-row').hidden=set;$('#agents-branch-row').hidden=set||!a.codex_env;
 $('#agents-codex-where').textContent=onDevice?t('Runs on {}, with the Codex signed in there.',a.codex_device):onMachine?t('Runs on your Machine, signed in with your ChatGPT plan.'):'';
 ch.hidden=!(set&&a.codex_setup);if(a.codex_setup)ch.href=a.codex_setup;
 // drawn by the page (the default), so a saved link or ID is never taken for text typed and not saved yet
 for(const [id,v] of [['agents-session',a.claude_session?'https://claude.ai/code/'+a.claude_session:''],['agents-env',a.codex_env||''],['agents-branch',a.codex_branch||'']]){const el=$('#'+id);el.value=el.defaultValue=v}
 $('#agents-connector').textContent=a.connector;$('#agents-connector-note').hidden=!a.claude_session;$('#agents-actions').hidden=true;
 for(const el of f.querySelectorAll('input,button'))el.disabled=!a.saveable;
 $('#agents-error').textContent=a.saveable?(a.claude_session&&!a.on_network?'Claude results need The Machine Network.':''):'Change these in config.json (agents) on this computer.'}
let agentsDirty=false;$('#agents-settings').addEventListener('input',()=>{agentsDirty=true;$('#agents-actions').hidden=false;$('#agents-error').textContent=''});
$('#agents-settings').addEventListener('submit',async e=>{e.preventDefault();const a=state.agents_settings||{},args={claude_session:$('#agents-session').value.trim(),device:a.device||'',codex_env:$('#agents-env').value.trim(),codex_branch:$('#agents-branch').value.trim()};
 try{$('#agents-save').disabled=true;state.agents_settings=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'set_agents',args})});
  agentsDirty=false;renderAgents();notice('Saved.')}catch(err){errCaught(err);$('#agents-error').textContent=err.message}finally{$('#agents-save').disabled=!state.agents_settings?.saveable}});
// How you write: a few short lines per channel (All: everywhere), learned from your own messages, notes and edits.
// Drafts on a channel follow its line. Edit, remove or add one here; an empty line removes it.
const VOICE_KNOWN=['All','Email','Slack','WhatsApp','Telegram','LinkedIn','X DM'];
const voiceFrom=v=>v.source==='owner'?'Yours':v.source==='profile'||v.source==='study'?'From your messages':'Learned';
let voiceDirty=false;
const voiceForm=v=>`<form class="sig-form voice-form" data-channel="${esc(v.channel)}" novalidate><div class="sig-head"><strong>${esc(v.channel==='All'?'Everywhere':v.channel)}</strong><small class="muted">${voiceFrom(v)} · ${time(v.updated_at,true)}</small></div><textarea rows="${Math.min(6,Math.max(3,(v.text.match(/\n/g)||[]).length+2))}" maxlength="450" aria-label="How you write: ${esc(v.channel)}">${esc(v.text)}</textarea><p role="status"></p><div class="actions"><button class="primary" hidden>Save</button><button type="button" class="quiet" data-voice-remove>Remove</button></div></form>`;
function renderVoices(){if(voiceDirty)return;const list=state.voices||[],free=VOICE_KNOWN.filter(c=>!list.some(v=>v.channel===c));
 $('#voices').innerHTML=(list.length?list.map(voiceForm).join(''):'<p class="muted">Nothing yet. I learn it from your notes, edits and messages.</p>')+
 `<form class="sig-form voice-form" data-new novalidate><div class="sig-head"><input list="voice-channels" maxlength="30" placeholder="Channel" aria-label="Channel"><datalist id="voice-channels">${free.map(c=>`<option value="${esc(c)}">`).join('')}</datalist></div><textarea rows="3" maxlength="450" placeholder="How you write there, a few short lines" aria-label="How you write there"></textarea><p role="status"></p><div class="actions"><button class="ghost">Add</button></div></form>`}
async function voiceSave(f,text){const out=f.querySelector('[role=status]'),channel=f.dataset.new!==undefined?f.querySelector('input').value.trim():f.dataset.channel;
 try{if(!channel)throw Error('Name the channel.');if(f.dataset.new!==undefined&&!text)throw Error('Say how you write there.');
  for(const b of f.querySelectorAll('button'))b.disabled=true;
  const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'set_voice',args:{channel,text}})});
  const pending=[...$('#voices').querySelectorAll('.voice-form')].filter(form=>form!==f&&form.dataset.dirty==='1')
   .map(form=>({channel:form.dataset.channel,new:form.dataset.new!==undefined,text:form.querySelector('textarea').value,name:form.querySelector('input')?.value}));
  state.voices=r.voices;voiceDirty=false;renderVoices();if(learnEdit==null)$('#facts').innerHTML=learnedList();  // What I've learned shows the new line too
  for(const edit of pending){const form=[...$('#voices').querySelectorAll('.voice-form')].find(form=>edit.new?form.dataset.new!==undefined:form.dataset.channel===edit.channel);
   if(!form)continue;form.querySelector('textarea').value=edit.text;if(edit.new)form.querySelector('input').value=edit.name;
   form.dataset.dirty='1';const button=form.querySelector('.primary');if(button)button.hidden=false;voiceDirty=true}
  notice(text?'Saved.':'Removed.')}
 catch(err){errCaught(err);out.textContent=err.message;for(const b of f.querySelectorAll('button'))b.disabled=false}}
$('#voices').addEventListener('input',e=>{const f=e.target.closest('.voice-form');if(!f)return;f.dataset.dirty='1';voiceDirty=true;f.querySelector('[role=status]').textContent='';const b=f.querySelector('.primary');if(b)b.hidden=false});
$('#voices').addEventListener('submit',e=>{e.preventDefault();voiceSave(e.target,e.target.querySelector('textarea').value.trim())});
$('#voices').addEventListener('click',e=>{const b=e.target.closest('[data-voice-remove]');if(b)voiceSave(b.closest('.voice-form'),'')});
// Edit on a saved line (a card's chat, What I've learned): Settings, Writing, with that channel's line in view and ready to type in
let voiceEditing=null;
function voiceEditShow(){const ch=voiceEditing;if(ch==null||$('#settings').hidden)return;voiceEditing=null;
 const f=[...$('#voices').querySelectorAll('.voice-form:not([data-new])')].find(x=>x.dataset.channel===ch)||$('#voices .voice-form[data-new]'),t=f?.querySelector('textarea');if(!t)return;
 if(f.dataset.new!==undefined&&!f.querySelector('input').value)f.querySelector('input').value=ch;
 f.classList.remove('voice-flash');void f.offsetWidth;f.classList.add('voice-flash');t.scrollIntoView({block:'center'});t.focus({preventScroll:true});t.setSelectionRange(t.value.length,t.value.length)}
document.addEventListener('click',e=>{const a=e.target.closest('[data-voice-edit]');if(!a)return;e.preventDefault();voiceEditing=a.dataset.voiceEdit;
 if(location.hash==='#settings/writing'&&!$('#settings').hidden){voiceEditShow();return}if(location.hash==='#settings/writing'){showSettings('writing');voiceEditShow();return}location.hash='#settings/writing'});
addEventListener('hashchange',()=>requestAnimationFrame(voiceEditShow));
// Signatures: one card per mailbox with a small rich editor. The signature is edited inside a sandboxed frame (no
// scripts run there; it loads images only), on white paper like an email; the server cleans what it stores and sends.
// With nothing kept yet, the mailbox's own is imported once: Gmail's signature, or the one Outlook's sent mail ends with.
const sigDoc=(h,dark)=>`<!doctype html><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src https: data:; style-src 'unsafe-inline'"><style>html{background:${dark?'#ECE9E1':'#fff'}}body{font:14px/1.45 Arial,Helvetica,sans-serif;color:#222;margin:12px 14px;min-height:48px;outline:none;overflow-wrap:anywhere}body:empty::before{content:"No signature";color:#999}img{max-width:100%;height:auto}a{color:#1a5fb4}</style><body contenteditable="true" spellcheck="false">${h||''}</body>`;
const sigDirty=new Set(),sigImported=new Set();
const sigSized=new ResizeObserver(rows=>{for(const r of rows)r.target._fit?.()});  // drawn while Settings was hidden: sized once shown
const SIG_TOOLS=[['bold','<b>B</b>','Bold'],['italic','<i>I</i>','Italic'],['underline','<u>U</u>','Underline'],['link','Link','Link'],['image','Image','Image by address'],['color','','Text color'],['clear','Clear','Clear formatting'],['html','&lt;/&gt; HTML','Edit the HTML']];
const sigState=s=>s.source==='owner'?'Custom':s.source&&s.html?'Imported':'None';
const sigFrom=s=>s.service==='outlook'?'Found in your Outlook sent mail':'Imported from Gmail';
function sigCard(s){const off=s.saveable?'':' disabled';
 return `<form class="sig-form" data-account="${esc(s.account_id)}" data-service="${esc(s.service)}" novalidate><div class="sig-head"><strong class="ell">${esc(s.email||s.account_id)}</strong><small class="muted">${s.service==='outlook'?'Outlook':'Gmail'} · <span class="sig-state">${sigState(s)}</span></small></div>
 <div class="sig-tools" role="toolbar" aria-label="Formatting">${SIG_TOOLS.map(([k,t,l])=>k==='color'?`<label class="sig-color" title="${l}"><span aria-hidden="true">A</span><input type="color" value="#222222" data-sig-tool="color" aria-label="${l}"${off}></label>`:`<button type="button" data-sig-tool="${k}" title="${l}" aria-label="${l}"${k==='html'?' aria-pressed="false"':''}${off}>${k==='html'?'<span class="sig-code">&lt;/&gt; </span>HTML':t}</button>`).join('')}</div>
 <iframe class="sig-paper" sandbox="allow-same-origin" title="Signature for ${esc(s.email||s.account_id)}"></iframe><textarea class="sig-source" rows="6" maxlength="20000" aria-label="Signature HTML" spellcheck="false" hidden></textarea>
 <p class="sig-note muted">${s.source&&s.source!=='owner'&&s.html?esc(sigFrom(s))+' · ':''}<button type="button" class="link" data-sig-import${off}>${s.source&&s.source!=='owner'?'Re-import':s.service==='outlook'?'Find in sent mail':'Import from Gmail'}</button>${s.source==='owner'?` · <button type="button" class="link" data-sig-mailbox${off}>Use mailbox signature</button>`:''}</p>
 <p role="status"></p><div class="actions sig-save" hidden><button class="primary"${off}>Save</button><button type="button" class="ghost" data-sig-cancel>Cancel</button></div></form>`}
const sigDark=()=>(document.documentElement.dataset.theme||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'))==='dark';
function sigLoad(f,html){const fr=f.querySelector('.sig-paper');fr.onload=()=>{const d=fr.contentDocument;if(!d?.body)return;try{d.execCommand('styleWithCSS',false,true)}catch{}
  const fit=()=>{if(!fr.offsetWidth)return;fr.style.height=Math.max(72,Math.min(420,d.body.scrollHeight+26))+'px'};fr._fit=fit;fit();sigSized.observe(fr);for(const i of d.images)i.addEventListener('load',fit);
  d.addEventListener('input',()=>{sigChanged(f);fit()});if(!f.querySelector('[data-sig-tool]').disabled)return;d.body.contentEditable='false'};
 fr.srcdoc=sigDoc(html,sigDark())}
const sigHtml=f=>{const src=f.querySelector('.sig-source');return src.hidden?f.querySelector('.sig-paper').contentDocument?.body?.innerHTML.trim()||'':src.value.trim()};
function sigChanged(f){sigDirty.add(f.dataset.account);f.querySelector('.sig-save').hidden=false;f.querySelector('[role=status]').textContent=''}
// Settings, Account, Your addresses (own_addresses.py): the owner's own addresses, where each came from, with Remove; and
// the ones that may be shared (a team address, sent from only), each with three choices and what each one changes:
// Mine, The team's (no to-dos from it) and Not mine. Nothing is picked for them. A chosen one keeps Change on its row.
const ADDR_PICKS=[['confirm','Mine: only I answer it','Its mail can become your to-dos.'],['team','The team’s: others answer it too','A shared inbox, like support@. No to-dos from it. Its mail still fills in the Graph.'],['remove','Not mine','It won’t count as yours.']];
const ADDR_LINE={confirm:'Mine',team:'The team’s · No to-dos from it',remove:'Not mine'};
const addrOpen=new Set();
function addrPick(a){return `<div class="addr-pick" role="radiogroup" aria-label="Whose is ${esc(a.address)}?">${ADDR_PICKS.map(([c,l,d])=>`<button type="button" role="radio" aria-checked="${a.choice===c}" data-addr="${esc(a.address)}" data-addr-choice="${c}"><strong>${l}</strong><small>${d}</small></button>`).join('')}</div>`}
function renderAddresses(){const v=state.own_addresses,box=$('#settings-addresses');$('#settings-domains').hidden=!v;box.hidden=!v||!(v.yours?.length||v.maybe?.length||v.team?.length||v.not_mine?.length);if(box.hidden)return;
 const row=(a,acts,pick)=>`<div${pick?' class="addr-choosing"':''}><span class="grow"><strong>${esc(a.address)}</strong><small>${esc([a.choice&&ADDR_LINE[a.choice],a.why,...(a.sources||[]).filter(s=>s!=='You confirmed it')].filter(Boolean).join(' · '))}</small></span>${acts?`<span class="addr-acts">${acts}</span>`:''}${pick?addrPick(a):''}</div>`;
 const change=a=>addrOpen.has(a.address)?`<button type="button" class="quiet" data-addr="${esc(a.address)}" data-addr-close>Cancel</button>`:`<button type="button" class="ghost" data-addr="${esc(a.address)}" data-addr-open>Change</button>`;
 const chosen=a=>row(a,change(a),addrOpen.has(a.address));
 const html=(v.yours||[]).map(a=>a.choice?chosen(a):row(a,a.removable?`<button type="button" class="ghost" data-addr="${esc(a.address)}" data-addr-choice="remove" data-addr-ask>Remove</button>`:'')).join('');
 const lists={'#addr-list':html,'#addr-maybe-list':(v.maybe||[]).map(a=>row(a,'',true)).join(''),'#addr-team-list':(v.team||[]).map(chosen).join(''),'#addr-not-list':(v.not_mine||[]).map(chosen).join('')};
 for(const [id,h] of Object.entries(lists)){if($(id).innerHTML!==h)$(id).innerHTML=h;if(id!=='#addr-list')$(id).parentElement.hidden=!h}
 // the company's domains: found ones (from the owner's own addresses) stay; added ones have Remove
 $('#settings-domains').hidden=false;
 const dom=(v.domains||[]).map(d=>`<div><span class="grow"><strong>${esc(d.domain)}</strong><small>${esc(d.added?t('Added by you'):t('From your addresses'))}</small></span>${d.added?`<span class="addr-acts"><button type="button" class="ghost" data-domain-remove="${esc(d.domain)}">Remove</button></span>`:''}</div>`).join('');
 const list=$('#addr-domain-list'),rows=[...list.children].filter(x=>x.tagName==='DIV');  // the add row stays, with what's typed in it
 if(rows.map(x=>x.outerHTML).join('')!==dom){rows.forEach(x=>x.remove());$('#addr-domain-form').insertAdjacentHTML('beforebegin',dom)}}
async function ownDomain(domain,on){const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'own_domain',args:{domain,on}})});
 state.own_addresses=r.own_addresses;renderAddresses();return r}
$('#addr-domain-form').addEventListener('submit',async e=>{e.preventDefault();const f=e.currentTarget,b=f.querySelector('button');b.disabled=true;
 try{await ownDomain(f.elements.domain.value.trim(),true);f.reset();notice('Added. People there are your colleagues now.')}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}});
$('#addr-domain-list').addEventListener('click',async e=>{const b=e.target.closest('[data-domain-remove]');if(!b)return;
 if(!confirm(t('Remove {}? People there count as a client again.',b.dataset.domainRemove)))return;b.disabled=true;
 try{await ownDomain(b.dataset.domainRemove,false);notice('Removed.')}catch(err){errCaught(err);b.disabled=false;notice(err.message)}});
$('#settings-addresses').addEventListener('click',async e=>{const o=e.target.closest('[data-addr-open],[data-addr-close]');
 if(o){o.hasAttribute('data-addr-open')?addrOpen.add(o.dataset.addr):addrOpen.delete(o.dataset.addr);renderAddresses();
  if(o.hasAttribute('data-addr-open'))$('#settings-addresses').querySelector(`.addr-pick [data-addr="${CSS.escape(o.dataset.addr)}"]`)?.focus();return}
 const b=e.target.closest('[data-addr-choice]');if(!b)return;const address=b.dataset.addr,choice=b.dataset.addrChoice;
 if(b.getAttribute('aria-checked')==='true'){addrOpen.delete(address);renderAddresses();return}
 if(b.hasAttribute('data-addr-ask')&&!confirm(t('Remove {}? Mail from it won’t count as yours.',address)))return;
 for(const x of $('#settings-addresses').querySelectorAll(`[data-addr="${CSS.escape(address)}"]`))x.disabled=true;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'own_address',args:{address,choice}})});
  addrOpen.delete(address);state.own_addresses=r.own_addresses;renderAddresses();notice({confirm:'Added to your addresses.',team:'Marked as the team’s. No to-dos from it.'}[choice]||'Removed. It won’t count as yours.')}catch(err){errCaught(err);notice(err.message);renderAddresses()}});
// Settings, Look up work contacts: there when this Machine can look people up (hosted, or a service with people_url).
function renderLookups(){const l=state.lookups||{},box=$('#settings-lookups'),b=$('#lookup-people');box.hidden=!l.people_available;b.setAttribute('aria-checked',String(l.people!==false));b.disabled=!!l.required_off;
 b.title=l.required_off?'Off in a Careful Work Fleet':''}
// Settings, Security (security_levels.py): Standard is today's defaults; Careful sets the stricter ones. Changing one after shows Custom.
const SEC_ROWS=[['notify_text','Text in notifications','Show what a to-do says on your lock screen.'],['save_logins','Offer to save sign-ins','“Save for next time” when your Machine signs in to a site.'],['keep_days','Keep Do it details 90 days','Off: 30 days.']];
const SEC_NOTE={standard:'Standard: today’s defaults.',careful:'Careful: no text in notifications, no saved sign-ins, no lookups, less history. Family free/busy asks first; Friends get no meeting context.',custom:'Custom: you changed a setting. Pick a level to reset them.'};
function renderSecurity(){const v=state.security,box=$('#settings-security');box.hidden=!v;if(!v)return;
 for(const r of box.querySelectorAll('[name="sec-level"]'))r.checked=r.value===v.level;$('#sec-note').textContent=SEC_NOTE[v.level]||'';
 const on=k=>k==='keep_days'?v.settings[k]==='90':v.settings[k]==='on';
 $('#sec-list').innerHTML=SEC_ROWS.map(([k,t,d])=>`<div><span class="grow"><strong>${t}</strong><small>${d}${k==='save_logins'?' <button type="button" class="quiet sec-forget" id="sec-forget">Forget all saved sign-ins</button>':''}</small></span><button type="button" class="lookup-switch" role="switch" data-sec="${k}" aria-checked="${on(k)}" aria-label="${t}"></button></div>`).join('');
 $('#sec-fleets').innerHTML=(v.fleets||[]).map(f=>`<p><strong>${esc(f.name)}</strong>: <span>${f.level==='careful'?'Careful, set by its admin. Answers wait for you, without names. No attachments in the team Graph, no text in work notifications, no lookups.':'Standard, set by its admin.'}</span></p>`).join('')}
function secLocal(k,val){const v=state.security;if(!v||!(k in v.settings))return;v.settings[k]=val;
 v.level=['standard','careful'].find(l=>Object.keys(v.settings).every(x=>v.settings[x]===v[l][x]))||'custom';renderSecurity()}
const secPost=async(action,args)=>{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
 if(r.security)state.security=r.security;if(r.lookups)state.lookups=r.lookups;if(r.team_learnings)state.team_learnings=r.team_learnings;renderSecurity();renderLookups();renderShareOffer();return r};
$('#settings-security').addEventListener('change',async e=>{const r=e.target.closest('[name="sec-level"]'),v=state.security;if(!r||!v)return;
 const target=v[r.value]||{},n=Object.keys(target).filter(k=>v.settings[k]!==target[k]).length;
 if(n&&!confirm(`Switch to ${r.value==='careful'?'Careful':'Standard'}? This changes ${n} setting${n===1?'':'s'}.`)){renderSecurity();return}
 try{await secPost('security_level',{level:r.value})}catch(err){errCaught(err);notice(err.message);renderSecurity()}});
$('#settings-security').addEventListener('click',async e=>{const b=e.target.closest('[data-sec]');
 if(e.target.closest('#sec-forget')){if(!confirm('Forget every saved sign-in? Your Machine asks again next time.'))return;
  try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'browser_login_forget',args:{all:true}})});notice(r.forgotten?`Forgot ${r.forgotten} saved sign-in${r.forgotten===1?'':'s'}.`:'No saved sign-ins.')}catch(err){errCaught(err);notice(err.message)}return}
 if(!b)return;const k=b.dataset.sec,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{await secPost('security_setting',{key:k,value:k==='keep_days'?(on?'90':'30'):(on?'on':'off')})}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}});
$('#lookup-people').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{state.lookups=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'set_people_lookup',args:{on}})});renderLookups();secLocal('people_lookup',on?'on':'off');notice(on?'Work contacts are looked up.':'Work contacts are no longer looked up.')}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}};
// Feedback, Share learnings with The Machine team (team_learnings.py): a quiet card, then exactly what would be sent, item
// by item, to edit or remove. An item's error log goes only when ticked (off by default), the owner's email only when
// ticked. Send, Not now and Never ask; the Settings switch turns the asking on or off. A refresh keeps what is typed.
let shareOpen=false,shareKey='';const shareDraft={id:'',items:{},named:false,auto:false};
const sharePost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
const shareKept=a=>a.items.filter(i=>!shareDraft.items[i.n]?.removed);
const shareCount=n=>n===1?'1 learning':n+' learnings';
// A learning's use cases (1 to 3: situation, action, result), each to edit or remove; at least one stays.
const shareCases=(i,d)=>(i.use_cases||[]).map((c,k)=>({...c,...(d.cases?.[k]||{}),k}));
function shareCaseHtml(i,d){const cases=shareCases(i,d);if(!cases.length)return '';const kept=cases.filter(c=>!c.removed).length;
 return `<div class="share-cases"><span class="share-lbl">${esc(t('Use cases'))}</span>`+cases.map(c=>c.removed
  ?`<div class="share-case removed" data-k="${c.k}"><span>${esc(t('Use case removed.'))}</span><button type="button" class="quiet" data-case-undo>${esc(t('Undo'))}</button></div>`
  :`<div class="share-case" data-k="${c.k}">`+[['given','Situation'],['when','Action'],['then','Result']].map(([f,l])=>`<label><span class="share-lbl">${esc(t(l))}</span><textarea data-share-case="${f}" rows="1" maxlength="160">${esc(c[f]||'')}</textarea></label>`).join('')
   +(kept>1?`<button type="button" class="quiet" data-case-remove>${esc(t('Remove use case'))}</button>`:'')+'</div>').join('')+'</div>'}
function renderShare(force){const a=state.team_learnings?.ask,box=$('#share-learnings');if(!box)return;
 if(!a){box.innerHTML='';shareKey='';shareOpen=false;return}
 if(shareDraft.id!==a.id){shareDraft.id=a.id;shareDraft.items={};shareDraft.named=!!a.pending?.named;shareDraft.auto=false;shareOpen=false;
  if(a.pending){const keep=new Map(a.pending.items.map(i=>[i.n,i]));for(const i of a.items)shareDraft.items[i.n]=keep.get(i.n)||{removed:true}}}
 const key=[a.id,shareOpen,Object.keys(shareDraft.items).filter(k=>shareDraft.items[k].removed).join(','),Object.entries(shareDraft.items).map(([n,d])=>n+':'+Object.keys(d.cases||{}).filter(k=>d.cases[k].removed).join('.')).join(','),a.error||''].join('|');
 if(key===shareKey&&!force)return;shareKey=key;
 const n=a.items.length,kept=shareKept(a).length;
 const head=`<div class="notice-card share-ask" role="region" aria-label="Share learnings"><span><strong>Share ${n===1?'a learning':n+' learnings'} with The Machine team?</strong> General learnings from how you use it. You choose what to share.</span>${shareOpen?'':'<div class="share-ask-acts"><button type="button" class="head-link" data-share="open">Review</button><button type="button" class="quiet" data-share="later">Not now</button></div>'}</div>`;
 if(!shareOpen){box.innerHTML=head;return}
 const item=i=>{const d=shareDraft.items[i.n]||{};
  if(d.removed)return `<li class="share-item removed" data-n="${i.n}"><span>Removed. It won’t be sent.</span><button type="button" class="quiet" data-share-undo>Undo</button></li>`;
  return `<li class="share-item" data-n="${i.n}"><label><span class="share-lbl">Learning</span><textarea data-share-field="text" rows="2" maxlength="280">${esc(d.text??i.text)}</textarea></label>`
   +(i.example?`<label><span class="share-lbl">Example, made up</span><textarea data-share-field="example" rows="2" maxlength="200">${esc(d.example??i.example)}</textarea></label>`:'')
   +shareCaseHtml(i,d)
   +(i.log?`<label class="share-log"><input type="checkbox" data-share-log${d.log?' checked':''}> Add the error log</label><details class="share-log-text"><summary>See the log</summary><pre>${esc(i.log)}</pre></details>`:'')
   +`<div class="share-foot">${i.taken?`<small>${esc(i.taken)}</small>`:''}<button type="button" class="quiet" data-share-remove>Remove</button></div></li>`};
 box.innerHTML=head+`<div class="share-panel" role="region" aria-label="What would be sent"><p class="fine">This is exactly what would be sent. Edit or remove anything.</p><ol class="share-items">${a.items.map(item).join('')}</ol>`
  +(state.team_learnings?.auto_careful?'':`<label class="share-named share-auto"><input type="checkbox" id="share-auto-tick"${shareDraft.auto?' checked':''}> ${esc(t('Send automatically from now on'))}</label><p class="fine share-auto-fine">${esc(t('New learnings go without asking. See or withdraw them in Fleet, Activity. Your email never goes by itself.'))}</p>`)
  +`<label class="share-named"><input type="checkbox" id="share-named"${shareDraft.named?' checked':''}> Add my email so the team can reply</label>`
  +'<p class="fine">Encrypted for the team. Without your email it comes from a made-up name. Other Machines may vote on a learning, without knowing who sent it. <a class="learn" href="https://themachine.computer/help/share-learnings" target="_blank" rel="noopener">Learn more</a></p>'
  +(a.error?'<p class="share-error" role="status">Delivery isn’t confirmed yet. Try again to confirm the same items, without duplicates.</p>':'')
  +`<div class="actions"><button type="button" class="primary" data-share="send"${kept?'':' disabled'}>Send ${shareCount(kept)}</button><button type="button" class="ghost" data-share="later">Not now</button><button type="button" class="quiet" data-share="never">Never ask</button></div></div>`}
$('#share-learnings').addEventListener('input',e=>{const li=e.target.closest('.share-item'),a=state.team_learnings?.ask;if(!li||!a)return;const d=shareDraft.items[li.dataset.n]??={};
 if(e.target.dataset.shareField)d[e.target.dataset.shareField]=e.target.value;if(e.target.matches('[data-share-log]'))d.log=e.target.checked;
 if(e.target.dataset.shareCase){const k=e.target.closest('.share-case').dataset.k;((d.cases??={})[k]??={})[e.target.dataset.shareCase]=e.target.value}});
$('#share-learnings').addEventListener('change',e=>{if(e.target.id==='share-named')shareDraft.named=e.target.checked;else if(e.target.id==='share-auto-tick')shareDraft.auto=e.target.checked;else if(e.target.matches('[data-share-log]')){const li=e.target.closest('.share-item');(shareDraft.items[li.dataset.n]??={}).log=e.target.checked}});
$('#share-learnings').addEventListener('click',async e=>{const a=state.team_learnings?.ask;if(!a)return;const li=e.target.closest('.share-item');
 if(e.target.closest('[data-share-remove]')){(shareDraft.items[li.dataset.n]??={}).removed=true;renderShare();$('#share-learnings [data-share="send"]')?.focus();return}
 const cs=e.target.closest('[data-case-remove],[data-case-undo]');if(cs){const d=shareDraft.items[li.dataset.n]??={},k=cs.closest('.share-case').dataset.k;((d.cases??={})[k]??={}).removed=cs.hasAttribute('data-case-remove');renderShare(true);return}
 if(e.target.closest('[data-share-undo]')){(shareDraft.items[li.dataset.n]??={}).removed=false;renderShare();$(`#share-learnings .share-item[data-n="${li.dataset.n}"] textarea`)?.focus();return}
 const b=e.target.closest('[data-share]');if(!b)return;const what=b.dataset.share;
 if(what==='open'){shareOpen=true;renderShare();$('#share-learnings textarea')?.focus();return}
 b.disabled=true;
 try{let r;
  if(what==='send'){const items=shareKept(a).map(i=>{const d=shareDraft.items[i.n]||{};return {n:i.n,text:d.text??i.text,example:d.example??i.example??'',log:!!d.log,...(i.use_cases?.length?{use_cases:shareCases(i,d).filter(c=>!c.removed).map(c=>({given:c.given,when:c.when,then:c.then}))}:{})}});
   const auto=!!shareDraft.auto&&!state.team_learnings?.auto_careful;r=await sharePost('learnings_share',{id:a.id,items,named:shareDraft.named,auto});toast(auto?t(['Sent {} learning. New ones go automatically now.','Sent {} learnings. New ones go automatically now.'],r.count||items.length):`Sent ${shareCount(r.count||items.length)}. Thank you.`)}
  else if(what==='later'){r=await sharePost('learnings_later',{id:a.id});toast('Not now. I’ll ask again another week.')}
  else if(what==='never'){r=await sharePost('learnings_never',{id:a.id});toast('I won’t ask again. Turn it back on in Settings.')}
  if(r?.team_learnings)state.team_learnings=r.team_learnings;renderShare(true);renderShareOffer()}
 catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
function renderShareOffer(){const t=state.team_learnings;$('#settings-share').hidden=!t?.network;$('#share-offer').setAttribute('aria-checked',String(!!t?.offer));
 $('#share-auto-row').hidden=!t?.offer;$('#share-auto').setAttribute('aria-checked',String(!!t?.auto&&!t?.auto_careful));$('#share-auto').disabled=!!t?.auto_careful;
 {const n=$('#share-auto-note');n._html??=n.innerHTML;if(t?.auto_careful)n.textContent=window.t('A Careful Work Fleet keeps asking each time.');else if(n.innerHTML!==n._html)n.innerHTML=n._html}const vm=t?.vote_mode||(t?.vote===false?'off':'on');for(const r of document.querySelectorAll('#share-vote input'))r.checked=r.value===vm;$('#share-vote-note').textContent=vm==='ask'?'Each vote waits for you on the Feedback page.':'';$('#share-help').setAttribute('aria-checked',String(t?.help_topics!==false));$('#share-errors').setAttribute('aria-checked',String(t?.errors!==false))}
$('#share-help').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await sharePost('set_help_topics',{on});state.team_learnings=r.team_learnings;renderShareOffer();secLocal('help_topics',on?'on':'off');notice(on?'Help topics go to the team, never your words.':'Help topics won’t go to the team.')}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}};
// Vote on learnings from other Machines: On (votes by itself), Ask first (each vote waits on the Feedback page) or Off.
$('#share-vote').addEventListener('change',async e=>{const mode=e.target.value,all=document.querySelectorAll('#share-vote input');for(const r of all)r.disabled=true;
 try{const r=await sharePost('set_learnings_vote',{mode});state.team_learnings=r.team_learnings;renderShareOffer();renderVotes(true);
  notice(mode==='on'?'I’ll vote on learnings from other Machines.':mode==='ask'?'I’ll ask you before each vote goes.':'I won’t vote on learnings from other Machines.')}
 catch(err){errCaught(err);notice(err.message);renderShareOffer()}finally{for(const r of all)r.disabled=false}});
// Feedback, under Ask first: the votes waiting for the owner, in one quiet box (never a to-do each, never a notification).
// Review shows each tip and the vote as it would go; Send or Skip one, or all at once.
let votesOpen=false,votesKey='';const VOTE_LABEL={useful:'Useful',not_useful:'Not useful',not_relevant:'Not relevant here'};
function renderVotes(force){const tl=state.team_learnings,box=$('#share-votes');if(!box)return;const list=tl?.vote_mode==='ask'?tl.votes_waiting||[]:[];
 if(!list.length){box.innerHTML='';votesKey='';votesOpen=false;return}
 const key=votesOpen+'|'+list.map(v=>v.id).join(',');if(key===votesKey&&!force)return;votesKey=key;
 const n=list.length,head=`<div class="notice-card share-ask" role="region" aria-label="Votes on learnings from other Machines"><span><strong>${esc(t(['{} vote waits for you','{} votes wait for you'],n))}</strong> ${esc(t('Learnings from other Machines, and how I’d vote for you.'))}</span>${votesOpen?'':`<div class="share-ask-acts"><button type="button" class="head-link" data-votes="open">${esc(t('Review'))}</button></div>`}</div>`;
 if(!votesOpen){box.innerHTML=head;return}
 const item=v=>`<li class="share-item vote-item" data-id="${esc(v.id)}"><p class="vote-tip">${esc(v.text)}</p>${v.example?`<p class="fine vote-ex">${esc(v.example)}</p>`:''}`
  +`<p class="vote-is"><span class="share-lbl">${esc(t('My vote'))}</span> <strong>${esc(t(VOTE_LABEL[v.vote]||v.vote))}</strong>${v.reason?` · ${esc(v.reason)}`:''}</p>`
  +(v.use_case?`<p class="fine vote-case">${esc([v.use_case.given,v.use_case.when,v.use_case.then].filter(Boolean).join(' · '))}</p>`:'')
  +`<div class="share-foot"><button type="button" class="ghost" data-vote-send>${esc(t('Send'))}</button><button type="button" class="quiet" data-vote-skip>${esc(t('Skip'))}</button></div></li>`;
 box.innerHTML=head+`<div class="share-panel" role="region" aria-label="${esc(t('Votes that would be sent'))}"><p class="fine">${esc(t('Only the vote goes, with its short reason. Nothing about you.'))}</p><ol class="share-items">${list.map(item).join('')}</ol>`
  +`<div class="actions"><button type="button" class="primary" data-votes="send">${esc(t(['Send {} vote','Send {} votes'],n))}</button><button type="button" class="ghost" data-votes="skip">${esc(t('Skip all'))}</button></div></div>`}
$('#share-votes').addEventListener('click',async e=>{const list=state.team_learnings?.votes_waiting||[];
 if(e.target.closest('[data-votes="open"]')){votesOpen=true;renderVotes(true);return}
 const one=e.target.closest('[data-vote-send],[data-vote-skip]'),all=e.target.closest('[data-votes="send"],[data-votes="skip"]');if(!one&&!all)return;
 const send=one?one.hasAttribute('data-vote-send'):all.dataset.votes==='send',ids=one?[one.closest('.vote-item').dataset.id]:list.map(v=>v.id),b=one||all;b.disabled=true;
 try{const r=await sharePost('learnings_votes_decide',{ids,send});if(r?.team_learnings)state.team_learnings=r.team_learnings;
  toast(send?t(['Sending {} vote.','Sending {} votes.'],ids.length):ids.length===1?t('Skipped. It won’t be sent.'):t('Skipped {} votes. They won’t be sent.',ids.length));renderVotes(true)}
 catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#share-errors').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await sharePost('set_error_reports',{on});state.team_learnings=r.team_learnings;renderShareOffer();notice(on?'I’ll send error reports.':'I won’t send error reports.')}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}};
$('#share-auto').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await sharePost('set_learnings_auto',{on});state.team_learnings=r.team_learnings;renderShareOffer();renderShare(true);notice(on?t('New learnings go automatically. They’re listed in Fleet, Activity.'):t('I’ll ask before sending learnings.'))}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=!!state.team_learnings?.auto_careful}};
$('#share-offer').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await sharePost('set_learnings_offer',{on});state.team_learnings=r.team_learnings;renderShareOffer();renderShare(true);secLocal('learnings',on?'on':'off');notice(on?'I’ll offer learnings to share now and then.':'I won’t offer learnings to share.')}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}};
function renderSignatures(){const list=state.signatures||[],box=$('#settings-signatures');box.hidden=!list.length;if(!list.length||sigDirty.size)return;
 $('#signatures').innerHTML=list.map(sigCard).join('');
 for(const f of $('#signatures').querySelectorAll('.sig-form'))sigLoad(f,list.find(s=>s.account_id===f.dataset.account)?.html);
 // Nothing kept yet: import the mailbox's own once, so the editor starts from the real signature.
 for(const s of list)if(!s.source&&s.saveable&&!sigImported.has(s.account_id)){sigImported.add(s.account_id);sigImport(s.account_id,true)}}
const sigPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
async function sigImport(id,auto){const form=()=>$(`#signatures .sig-form[data-account="${CSS.escape(id)}"]`),say=t=>{const o=form()?.querySelector('[role=status]');if(o)o.textContent=t};
 const button=form()?.querySelector('[data-sig-import]');if(button)button.disabled=true;
 try{const r=await sigPost('detect_signature',{account_id:id}),none=form()?.dataset.service==='outlook'?'No signature repeats in your recent sent mail.':'Gmail has no signature for this address.';
  if((state.signatures||[]).find(s=>s.account_id===id)?.source==='owner'){  // the owner's own stays until they save the imported one
   const f=form();if(!f)return;if(!r.found){say(none);return}const src=f.querySelector('.sig-source');if(src.hidden)sigLoad(f,r.html);else src.value=r.html;sigChanged(f);say('Imported. Save to use it.');return}
  const s=(r.signatures||[]).find(x=>x.account_id===id),f=form();if(s)state.signatures=(state.signatures||[]).map(x=>x.account_id===id?s:x);  /* only this one: imports run side by side */
  if(f&&s&&!sigDirty.has(id)){f.outerHTML=sigCard(s);sigLoad(form(),s.html)}
  if(!r.found&&!auto)say(none)}
 catch(err){errCaught(err);say(err.message)}finally{const b=form()?.querySelector('[data-sig-import]');if(b)b.disabled=!(state.signatures||[]).find(x=>x.account_id===id)?.saveable}}
function sigTool(f,tool,value){const fr=f.querySelector('.sig-paper'),d=fr.contentDocument,src=f.querySelector('.sig-source');
 if(tool==='html'){const on=src.hidden;if(on){src.value=d.body.innerHTML.trim();fr.hidden=true;src.hidden=false;src.focus()}else{fr.hidden=false;src.hidden=true;sigLoad(f,src.value)}
  f.querySelector('[data-sig-tool="html"]').setAttribute('aria-pressed',on);for(const b of f.querySelectorAll('[data-sig-tool]:not([data-sig-tool="html"])'))b.disabled=on;return}
 if(!src.hidden)return;fr.contentWindow.focus();
 if(tool==='link'){const u=prompt('Link address (https://, mailto: or tel:)','https://');if(!u||!/^(https?:\/\/|mailto:|tel:)\S+$/i.test(u.trim()))return;d.execCommand('createLink',false,u.trim())}
 else if(tool==='image'){const u=prompt('Image address (https://)','https://');if(!u||!/^https:\/\/\S+$/i.test(u.trim()))return;d.execCommand('insertImage',false,u.trim())}
 else if(tool==='color')d.execCommand('foreColor',false,value);
 else if(tool==='clear'){d.execCommand('removeFormat');d.execCommand('unlink')}
 else d.execCommand(tool);
 sigChanged(f)}
$('#signatures').addEventListener('mousedown',e=>{if(e.target.closest('button[data-sig-tool]'))e.preventDefault()});  // keeps the selection in the editor
$('#signatures').addEventListener('click',async e=>{const f=e.target.closest('.sig-form');if(!f)return;const t=e.target.closest('button[data-sig-tool]');if(t){sigTool(f,t.dataset.sigTool);return}
 if(e.target.closest('[data-sig-import]'))return sigImport(f.dataset.account);
 if(e.target.closest('[data-sig-cancel]')){sigDirty.delete(f.dataset.account);const s=(state.signatures||[]).find(x=>x.account_id===f.dataset.account);f.outerHTML=sigCard(s);sigLoad($(`#signatures .sig-form[data-account="${CSS.escape(s.account_id)}"]`),s.html);return}
 const m=e.target.closest('[data-sig-mailbox]');if(m){m.disabled=true;try{state.signatures=await sigPost('set_signature',{account_id:f.dataset.account,use_mailbox:true});sigDirty.delete(f.dataset.account);if(!sigDirty.size)renderSignatures();notice('Using the mailbox signature.')}catch(err){errCaught(err);f.querySelector('[role=status]').textContent=err.message;m.disabled=false}}});
$('#signatures').addEventListener('input',e=>{const f=e.target.closest('.sig-form');if(!f)return;if(e.target.matches('[data-sig-tool="color"]'))sigTool(f,'color',e.target.value);else if(e.target.matches('.sig-source'))sigChanged(f)});
$('#signatures').addEventListener('submit',async e=>{e.preventDefault();const f=e.target,out=f.querySelector('[role=status]'),b=f.querySelector('.primary');b.disabled=true;
 try{state.signatures=await sigPost('set_signature',{account_id:f.dataset.account,html:sigHtml(f)});
  sigDirty.delete(f.dataset.account);if(!sigDirty.size)renderSignatures();notice('Signature saved.')}catch(err){errCaught(err);out.textContent=err.message}finally{b.disabled=false}});
