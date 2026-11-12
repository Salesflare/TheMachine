// Settings' tabs, links and what the rest of the page uses from Settings (Learning's Share and Votes boxes, the voice
// editor's links). Settings' own panels (settings-general, -skills, -ai, -export and -upkeep) load when first needed
// (dashboard_parts.LAZY); showSettings() opens Settings once they're in.
// Settings in tabs, a pill row like Graph and Connections. A Machine linked to a control plane account (hosted, or
// paired with the Network: status account_url) gets Account first, the account in short with buttons to its pages.
// Each part of Settings goes to a tab by its id; a part without one goes with the part before it (a heading with what
// follows it). A tab with nothing to show is left out. Links: #settings, #settings/skills (or #settings=skills); the last tab is kept.
const SETTINGS_TABS=[['account','Account'],['general','General'],['security','Security'],['activity','Activity'],['notify','Notifications'],['writing','Writing'],['skills','Skills'],['apps','Apps'],['model','Model']];
const SETTINGS_OF={'settings-notify':'notify','settings-acct':'account','settings-addresses':'account','settings-domains':'account','settings-acct-end':'account',hours:'notify','settings-signatures':'writing','settings-voices':'writing','settings-skills':'skills','settings-model':'model','agents-settings':'model','settings-browser':'general','settings-fleet':'general','settings-account-block':'general','settings-locale':'general','settings-dictation':'general','settings-security':'security','settings-lookups':'security','settings-share':'security','settings-apps':'apps','settings-ai':'apps','settings-export':'general'};
// Apps was AIs (#settings/ai) until 2026-11: an old link or a kept tab opens Apps
const SETTINGS_OLD={hours:'notify',ai:'apps',ais:'apps'};
let settingsTab=SETTINGS_OLD[localStorage.getItem('settings-tab')]||localStorage.getItem('settings-tab')||'account',settingsNow='';
{const bar=document.createElement('div');bar.className='sub-tabs';bar.id='settings-tabs';bar.setAttribute('role','tablist');bar.setAttribute('aria-label','Settings');
 bar.innerHTML=SETTINGS_TABS.map(([id,label])=>`<button type="button" role="tab" data-settings-tab="${id}" aria-selected="false">${label}</button>`).join('');
 $('#settings').prepend(bar)}
function settingsSync(){const s=$('#settings'),bar=$('#settings-tabs'),shown=new Set(),set=(el,k,v)=>{if(el[k]!==v)el[k]=v};if(s.firstElementChild!==bar)s.prepend(bar);
 let tab='general';for(const el of s.children){if(el===bar)continue;tab=SETTINGS_OF[el.id]||(el.classList.contains('section-head')?SETTINGS_OF[el.nextElementSibling?.id]||'general':tab);el.dataset.stab=tab;if(!el.hidden&&!el.classList.contains('section-head'))shown.add(tab)}
 settingsNow=shown.has(settingsTab)?settingsTab:SETTINGS_TABS.map(t=>t[0]).find(t=>shown.has(t))||'general';const live=!s.hidden&&lazyIn('settings');if(live)loadSettingsViews();if(settingsNow==='account'&&live)loadAccount();if(settingsNow==='general'&&live){loadDictation();loadExport()}if((settingsNow==='general'||settingsNow==='model')&&live)upkeepShown();if(settingsNow==='activity'&&!s.hidden&&typeof actShown==='function')actShown();if(settingsNow==='apps'&&live&&!aiView)aiLoad();if(!s.hidden)helpLink('settings');
 for(const el of s.children)if(el!==bar)el.classList.toggle('stab-off',el.dataset.stab!==settingsNow);
 for(const b of bar.querySelectorAll('[data-settings-tab]')){set(b,'hidden',!shown.has(b.dataset.settingsTab));const on=String(b.dataset.settingsTab===settingsNow);if(b.getAttribute('aria-selected')!==on)b.setAttribute('aria-selected',on)}needsYouPlace()}
new MutationObserver(settingsSync).observe($('#settings'),{childList:true,subtree:true,attributes:true,attributeFilter:['hidden']});
const settingsHash=()=>{if(!$('#settings').hidden)history.replaceState(null,'',location.pathname+location.search+'#settings/'+settingsNow)};
function settingsOpen(tab){tab=SETTINGS_OLD[tab]||tab;if(SETTINGS_TABS.some(t=>t[0]===tab)){settingsTab=tab;localStorage.setItem('settings-tab',tab)}const was=!$('#settings').hidden;
 for(const b of document.querySelectorAll('nav button[data-tab]')){b.classList.remove('active');b.setAttribute('aria-current','false')}for(const x of document.querySelectorAll('main>section'))x.hidden=x.id!=='settings';$('#open-settings').setAttribute('aria-current','page');
 settingsSync();settingsHash();if(!was)scrollTo(0,0);requestAnimationFrame(()=>{tabsShow($('#settings-tabs'));if(!was)kbLand()})}
// Settings' panels load when first needed: Settings opens once they're in (and a Writing link's voice gets the focus)
function showSettings(tab){if(lazyIn('settings'))return settingsOpen(tab);lazyRun('settings',()=>{settingsOpen(tab);voiceEditShow()})}
$('#open-settings').onclick=()=>showSettings();
$('#settings-tabs').onclick=e=>{const b=e.target.closest('[data-settings-tab]');if(!b)return;showSettings(b.dataset.settingsTab)};
$('nav').addEventListener('click',e=>{if(!e.target.closest('button')?.dataset.tab)return;$('#open-settings').setAttribute('aria-current','false');if(location.hash.startsWith('#settings'))history.replaceState(null,'',location.pathname+location.search)});
// Feedback, Share learnings with The Machine team (team_learnings.py): a quiet card, then exactly what would be sent, item
// by item, to edit or remove. An item's error log goes only when ticked (off by default), the owner's email only when
// ticked. Send, Not now and Never ask; the Settings switch turns the asking on or off. A refresh keeps what is typed.
let shareOpen=false,shareKey='';const shareDraft={id:'',items:{},named:false,auto:false};
const sharePost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
const shareKept=a=>a.items.filter(i=>!shareDraft.items[i.n]?.removed);
const shareCount=n=>n===1?'1 learning':n+' learnings';
function renderShareOffer(){const t=state.team_learnings;$('#settings-share').hidden=!t?.network;$('#share-offer').setAttribute('aria-checked',String(!!t?.offer));
 $('#share-auto-row').hidden=!t?.offer;$('#share-auto').setAttribute('aria-checked',String(!!t?.auto&&!t?.auto_careful));$('#share-auto').disabled=!!t?.auto_careful;
 {const n=$('#share-auto-note');n._html??=n.innerHTML;if(t?.auto_careful)n.textContent=window.t('A Careful Work Fleet keeps asking each time.');else{const h=t?.auto_personal?esc(window.t('New learnings go without asking. See or withdraw them in Settings, Activity.'))+' '+n._html.slice(n._html.indexOf('<a')):n._html;if(n.innerHTML!==h)n.innerHTML=h}}const vm=t?.vote_mode||(t?.vote===false?'off':'on');for(const r of document.querySelectorAll('#share-vote input'))r.checked=r.value===vm;$('#share-vote-note').textContent=vm==='ask'?'Each vote waits for you under Learning, Shared.':'';$('#share-help').setAttribute('aria-checked',String(t?.help_topics!==false));$('#share-errors').setAttribute('aria-checked',String(t?.errors!==false))}
$('#share-help').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await sharePost('set_help_topics',{on});state.team_learnings=r.team_learnings;renderShareOffer();if(lazyIn('settings'))secLocal('help_topics',on?'on':'off');notice(on?'Help topics go to the team, never your words.':'Help topics won’t go to the team.')}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}};
// Vote on learnings from other Machines: On (votes by itself), Ask first (each vote waits under Learning, Shared) or Off.
$('#share-vote').addEventListener('change',async e=>{const mode=e.target.value,all=document.querySelectorAll('#share-vote input');for(const r of all)r.disabled=true;
 try{const r=await sharePost('set_learnings_vote',{mode});state.team_learnings=r.team_learnings;renderShareOffer();if(lazyIn('learning'))renderVotes(true);  // Learning's part (learning-share.js) draws it once it's in
  notice(mode==='on'?'I’ll vote on learnings from other Machines.':mode==='ask'?'I’ll ask you before each vote goes.':'I won’t vote on learnings from other Machines.')}
 catch(err){errCaught(err);notice(err.message);renderShareOffer()}finally{for(const r of all)r.disabled=false}});
$('#share-errors').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await sharePost('set_error_reports',{on});state.team_learnings=r.team_learnings;renderShareOffer();notice(on?'I’ll send error reports.':'I won’t send error reports.')}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}};
$('#share-auto').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await sharePost('set_learnings_auto',{on});state.team_learnings=r.team_learnings;renderShareOffer();if(lazyIn('learning'))renderShare(true);notice(on?t('New learnings go automatically. They’re listed in Settings, Activity.'):t('I’ll ask before sending learnings.'))}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=!!state.team_learnings?.auto_careful}};
$('#share-offer').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await sharePost('set_learnings_offer',{on});state.team_learnings=r.team_learnings;renderShareOffer();if(lazyIn('learning'))renderShare(true);if(lazyIn('settings'))secLocal('learnings',on?'on':'off');notice(on?'I’ll offer learnings to share now and then.':'I won’t offer learnings to share.')}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}};
// Edit on a saved line (a card's chat, What I've learned): Settings, Writing, with that channel's line in view and ready to type in
let voiceEditing=null;
function voiceEditShow(){const ch=voiceEditing;if(ch==null||$('#settings').hidden)return;voiceEditing=null;
 const f=[...$('#voices').querySelectorAll('.voice-form:not([data-new])')].find(x=>x.dataset.channel===ch)||$('#voices .voice-form[data-new]'),t=f?.querySelector('textarea');if(!t)return;
 if(f.dataset.new!==undefined&&!f.querySelector('input').value)f.querySelector('input').value=ch;
 f.classList.remove('voice-flash');void f.offsetWidth;f.classList.add('voice-flash');t.scrollIntoView({block:'center'});t.focus({preventScroll:true});t.setSelectionRange(t.value.length,t.value.length)}
document.addEventListener('click',e=>{const a=e.target.closest('[data-voice-edit]');if(!a)return;e.preventDefault();voiceEditing=a.dataset.voiceEdit;
 if(location.hash==='#settings/writing'&&!$('#settings').hidden){voiceEditShow();return}if(location.hash==='#settings/writing'){showSettings('writing');voiceEditShow();return}location.hash='#settings/writing'});
addEventListener('hashchange',()=>requestAnimationFrame(voiceEditShow));
// Skills' own panel loads when first needed (settings-skills.js); a to-do card's skill hint and Create skill use these.
let skillsKey='',skillEditing=null,skillSharing=null;
const skillAct=async(action,args)=>{const v=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});if(v&&v.skills)state.skills=v;skillsKey='';if(lazyIn('settings'))renderSkills();renderNeedsYou();return v};
// "There's a skill for this": the agent judged that a skill would clearly help with a card. Quiet, dismissable.
const hintFor=id=>(state.skills?.hints||[]).find(h=>String(h.suggestion_id)===String(id));
const skillHintNote=s=>{const h=!closed(s)&&hintFor(s.id);return h?html`<p class="note skill-hint">There’s a skill for this: <button type="button" class="link" data-hint-look="${h.id}">${h.name}</button>${h.kind==='clawhub'?' on ClawHub':''}. <button type="button" class="link" data-hint-dismiss="${h.id}">Not now</button></p>`:''};
// A skill hint's buttons on a card work before Skills is in: the click waits for it, then goes on.
document.addEventListener('click',e=>{if(lazyIn('settings'))return;const b=e.target.closest('[data-hint-look],[data-hint-dismiss]');if(!b)return;
 e.preventDefault();e.stopImmediatePropagation();lazyRun('settings',()=>b.click())},true);
// Connected AIs' panel loads when first needed (settings-ai.js); its view, its requests and the pairing that
// Connections and General start too are here. aiView is set only once that panel is in.
var aiView=null;let aiPairTimer=0,aiPairUntil=0;
const aiPost=(action,args={})=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
// Get your address (and Pair this Machine in Connections): the tab opens within the click, then goes to the account's
// page once it is known; a browser that blocks it goes there in this tab. Then ai_pair_state every 2.5 s, up to 10 minutes.
async function aiPairGo(done){const tab=window.open('','_blank');
 try{const r=await aiPost('ai_pair_start',{});if(tab&&!tab.closed){tab.opener=null;tab.location.href=r.url}else location.href=r.url;
  if(aiView){aiView.reach={...(aiView.reach||{}),pairing:r.code?{url:r.url,code:r.code,state:'waiting'}:null};renderAi()}
  aiPairUntil=Date.now()+600000;aiPairPoll(done)}
 catch(e){if(tab)tab.close();errCaught(e);notice(e.message,true)}}
function aiPairPoll(done){clearTimeout(aiPairTimer);if(Date.now()>aiPairUntil)return;
 aiPairTimer=setTimeout(async()=>{let r;try{r=await aiPost('ai_pair_state',{fresh:true})}catch{return aiPairPoll(done)}
  if(aiView){aiView.reach=r.reach;renderAi()}
  if(done&&(r.state==='paired'||r.reach?.paired)){done(r);done=null}
  if(r.reach?.address)return notice(t('Your address is ready'));
  if(r.state!=='gone')aiPairPoll(done)},2500)}
