// A lazy part (dashboard_parts.LAZY 'learning'): Learning's Share learnings card and votes, drawn once Learning is in.
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
  else if(what==='never'){r=await sharePost('learnings_never',{id:a.id});toastSettings('I won’t ask again. Turn it back on in {}.','settings-share')}
  if(r?.team_learnings)state.team_learnings=r.team_learnings;renderShare(true);renderShareOffer()}
 catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
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
