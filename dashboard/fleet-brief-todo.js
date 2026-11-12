// The team brief's lines as Work to-dos (fleet_brief_todos.py, docs/fleet.md). A line that joined an owner's to-do is a note on it.
const briefAsking=new Map();
const briefPerson=p=>p.node?html`<a href="${graphHash(p.node)}">${p.name}</a>`:html`<span>${p.name}</span>`;
function briefWhy(why,team){why=String(why||'');why=why.charAt(0).toUpperCase()+why.slice(1);const linked=(team||[]).filter(p=>p.node&&p.name);if(!linked.length)return html`${why}`;
 const re=new RegExp('('+linked.map(p=>p.name.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')'),by=Object.fromEntries(linked.map(p=>[p.name,p]));
 return html`${String(why).split(re).map(x=>by[x]?briefPerson(by[x]):html`${x}`)}`}
const briefOrg=(s,i)=>i.org?.id&&i.org.name&&cardOrg(s)?.name!==i.org.name?html`<a class="fleet-brief-org" href="${graphHash(i.org.id)}">${i.org.name}</a> · `:'';
function briefAnswers(a){if(!a)return'';
 return html`<div class="fleet-brief-asked"><p class="muted">${t('Asked the team: {}',a.question)}</p>${a.answers.length?html`<ul>${a.answers.map(x=>html`<li><strong>${x.name}</strong> ${x.state==='answered'?html`<span>${x.text}</span>`:html`<span class="muted">${x.state==='waiting'?'Waiting for an answer':'No answer'}</span>`}</li>`)}</ul>`:''}</div>`}
function briefEditor(s){if(!briefAsking.has(String(s.id)))return'';
 return html`<div class="change-editor fleet-brief-ask"><label for="brief-ask-${s.id}">Ask the team</label><textarea id="brief-ask-${s.id}" rows="2" spellcheck="true" autocapitalize="sentences" data-brief-text="${s.id}">${briefAsking.get(String(s.id))}</textarea><div class="actions"><button class="primary" data-brief-todo="send" data-card="${s.id}">Send</button><button class="ghost" data-brief-todo="cancel" data-card="${s.id}">Cancel</button></div></div>`}
function fleetBriefNote(s){const b=s.fleet_brief;if(!b||closed(s))return'';
 const lines=b.items.map(i=>html`<p class="note fleet fleet-brief-why">${briefOrg(s,i)}${b.own?'':html`${t('From the team brief: {}',i.title)} · `}${briefWhy(i.why,i.team)}</p>`);
 const ask=!b.own&&!b.asked&&!briefAsking.has(String(s.id))&&b.items.some(i=>i.ask)?html`<p class="note fleet"><button type="button" class="link" data-brief-todo="ask" data-card="${s.id}">Ask the team</button></p>`:'';
 return html`${lines}${briefAnswers(b.asked)}${ask}${briefEditor(s)}`}
// On a phone the lead has its own row (two-rows)
function fleetBriefActions(s){const b=s.fleet_brief,open=b.items.find(i=>i.open)?.open,asked=!!b.asked,ask=b.items.some(i=>i.ask);if(briefAsking.has(String(s.id)))return'';
 return html`<div class="actions${asked||ask?html` two-rows`:''}">${asked?html`<button class="primary" data-id="${s.id}" data-choice="complete">Done</button>`:ask?html`<button class="primary" data-brief-todo="ask" data-card="${s.id}">Ask the team</button>`:''}${open?html`<a class="open" href="${safeURL(open)}" target="_blank" rel="noopener">${t('Open')} ↗</a>`:''}<button class="ghost" data-id="${s.id}" data-choice="snooze">Snooze</button><button class="quiet" data-brief-todo="skip" data-card="${s.id}">Not needed</button></div>`}
const briefDay=at=>localeDate(/^\d{4}-\d\d-\d\d$/.test(at)?new Date(at+'T12:00:00'):new Date(at),DL,{day:'numeric',month:'short'});
// Details: only what the Team Graph shares
function fleetBriefDetails(s){const b=s.fleet_brief;if(!b||closed(s))return'';
 const row=(k,v)=>v?html`<div><dt>${t(k)}</dt><dd>${v}</dd></div>`:'';
 const mail=m=>html`<li><span translate="no">${m.subject||t('(no subject)')}</span> <small class="muted">${[m.from,m.at?briefDay(m.at):'',m.via?t('via {}',m.via):''].filter(Boolean).join(' · ')}</small></li>`;
 return html`${b.items.map(i=>{const people=[...(i.team||[]).map(briefPerson),...(i.also||[]).map(n=>html`<span>${n}</span>`)];
  return html`<div class="fleet-brief-details">${b.own&&b.items.length===1?'':html`<p class="tech-head">${t('From the team brief: {}',i.title)}</p>`}<dl class="card-fields">${i.kind==='waiting'?row('Waiting since',i.at?briefDay(i.at):''):''}${row('On the team',people.length?html`${people.map((p,k)=>html`${k?', ':''}${p}`)}`:'')}${row('Your latest email',i.own?html`<ul class="fleet-brief-mail">${mail(i.own)}</ul>`:'')}${row('Shared by the team',i.threads?.length?html`<ul class="fleet-brief-mail">${i.threads.map(mail)}</ul>`:'')}</dl></div>`})}`}
$('#suggestions').addEventListener('click',async e=>{const b=e.target.closest('[data-brief-todo]');if(!b)return;const id=b.dataset.card,s=(state.suggestions||[]).find(x=>String(x.id)===id),act=b.dataset.briefTodo;
 if(act==='ask'){briefAsking.set(id,(s?.fleet_brief?.items||[]).find(i=>i.ask)?.ask||'');render();requestAnimationFrame(()=>{const el=document.getElementById('brief-ask-'+id);if(el){el.focus();el.setSelectionRange(el.value.length,el.value.length)}});return}
 if(act==='cancel'){briefAsking.delete(id);render();return}
 b.disabled=true;
 try{if(act==='send'){const text=document.getElementById('brief-ask-'+id)?.value.trim()||'';await fleetPost('fleet_brief_todo',{suggestion_id:id,do:'ask',text});briefAsking.delete(id);toast('Asked the team.')}
  else{await fleetPost('fleet_brief_todo',{suggestion_id:id,do:'skip'});toast('Closed. The brief learns from it.')}
  await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#suggestions').addEventListener('input',e=>{const el=e.target.closest('[data-brief-text]');if(el)briefAsking.set(el.dataset.briefText,el.value)});
