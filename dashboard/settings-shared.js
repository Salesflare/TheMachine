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
 settingsNow=shown.has(settingsTab)?settingsTab:SETTINGS_TABS.map(t=>t[0]).find(t=>shown.has(t))||'general';const live=!s.hidden&&lazyIn('settings');if(settingsNow==='account'&&live)loadAccount();if(settingsNow==='general'&&live){loadDictation();loadExport()}if((settingsNow==='general'||settingsNow==='model')&&live)upkeepShown();if(settingsNow==='activity'&&!s.hidden&&typeof actShown==='function')actShown();if(settingsNow==='apps'&&live&&!aiView)aiLoad();if(!s.hidden)helpLink('settings');
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
  return `<li class="share-item" data-n="${i.n}"><label><span class="share-lbl">Learning to share</span><textarea data-share-field="text" rows="2" maxlength="280">${esc(d.text??i.text)}</textarea></label>`
   +(i.example?`<label><span class="share-lbl">Example, made up</span><textarea data-share-field="example" rows="2" maxlength="200">${esc(d.example??i.example)}</textarea></label>`:'')
   +shareCaseHtml(i,d)
   +(i.log?`<label class="share-log"><input type="checkbox" data-share-log${d.log?' checked':''}> Add the error log</label><details class="share-log-text"><summary>See the log</summary><pre>${esc(i.log)}</pre></details>`:'')
   +`<div class="share-foot">${i.taken?`<small>${esc(i.taken)}</small>`:''}<button type="button" class="quiet" data-share-remove>Remove</button></div></li>`};
 box.innerHTML=head+`<div class="share-panel" role="region" aria-label="What would be sent"><p class="fine">This is exactly what would be sent. Edit or remove anything.</p><ol class="share-items">${a.items.map(item).join('')}</ol>`
  +(a.personal&&state.team_learnings?.auto&&!state.team_learnings?.auto_personal&&!state.team_learnings?.auto_careful?`<p class="fine">${esc(t('These come from Personal to-dos, so I ask first.'))}</p>`:'')
  +(state.team_learnings?.auto_careful||state.team_learnings?.auto?'':`<label class="share-named share-auto"><input type="checkbox" id="share-auto-tick"${shareDraft.auto?' checked':''}> ${esc(t('Send automatically from now on'))}</label><p class="fine share-auto-fine">${esc(t('New learnings go without asking. See or withdraw them in Settings, Activity. Your email never goes by itself.'))}</p>`)
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
 {const n=$('#share-auto-note');n._html??=n.innerHTML;if(t?.auto_careful)n.textContent=window.t('A Careful Work Fleet keeps asking each time.');else{const h=t?.auto_personal?esc(window.t('New learnings go without asking. See or withdraw them in Settings, Activity.'))+' '+n._html.slice(n._html.indexOf('<a')):n._html;if(n.innerHTML!==h)n.innerHTML=h}}const vm=t?.vote_mode||(t?.vote===false?'off':'on');for(const r of document.querySelectorAll('#share-vote input'))r.checked=r.value===vm;$('#share-vote-note').textContent=vm==='ask'?'Each vote waits for you under Learning, Shared.':'';$('#share-help').setAttribute('aria-checked',String(t?.help_topics!==false));$('#share-errors').setAttribute('aria-checked',String(t?.errors!==false))}
$('#share-help').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await sharePost('set_help_topics',{on});state.team_learnings=r.team_learnings;renderShareOffer();if(lazyIn('settings'))secLocal('help_topics',on?'on':'off');notice(on?'Help topics go to the team, never your words.':'Help topics won’t go to the team.')}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}};
// Vote on learnings from other Machines: On (votes by itself), Ask first (each vote waits under Learning, Shared) or Off.
$('#share-vote').addEventListener('change',async e=>{const mode=e.target.value,all=document.querySelectorAll('#share-vote input');for(const r of all)r.disabled=true;
 try{const r=await sharePost('set_learnings_vote',{mode});state.team_learnings=r.team_learnings;renderShareOffer();renderVotes(true);
  notice(mode==='on'?'I’ll vote on learnings from other Machines.':mode==='ask'?'I’ll ask you before each vote goes.':'I won’t vote on learnings from other Machines.')}
 catch(err){errCaught(err);notice(err.message);renderShareOffer()}finally{for(const r of all)r.disabled=false}});
// Learning, Shared, under Ask first: the votes waiting for the owner, in one quiet box (never a to-do each, never a notification).
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
 try{const r=await sharePost('set_learnings_auto',{on});state.team_learnings=r.team_learnings;renderShareOffer();renderShare(true);notice(on?t('New learnings go automatically. They’re listed in Settings, Activity.'):t('I’ll ask before sending learnings.'))}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=!!state.team_learnings?.auto_careful}};
$('#share-offer').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await sharePost('set_learnings_offer',{on});state.team_learnings=r.team_learnings;renderShareOffer();renderShare(true);if(lazyIn('settings'))secLocal('learnings',on?'on':'off');notice(on?'I’ll offer learnings to share now and then.':'I won’t offer learnings to share.')}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}};
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
