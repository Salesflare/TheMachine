// A lazy part (dashboard_parts.LAZY 'fleetask'): the to-dos whose answer the owner reads, edits and sends, a teammate's
// free question (fleet.py) and a family member's question to this Machine (family_questions.py), and the Family tab's
// own box to ask one member's Machine. Their words are shown quoted, as data.
// What a question found, beside its answer: a short list, each with a day as people say it (Mon within the week, else
// Nov 9). A chat line's "#channel: Name" reads "Name in #channel".
const fleetMatchDay=v=>{const d=new Date(String(v||'').length===10?v+'T12:00':v);if(!v||isNaN(d))return '';const n=Math.round((new Date().setHours(12,0,0,0)-new Date(d).setHours(12,0,0,0))/864e5);
 return n>=0&&n<7?(n===0?t('Today'):n===1?t('Yesterday'):localeDate(d,DL,{weekday:'short'})):localeDate(d,DL,{day:'numeric',month:'short',...(d.getFullYear()!==new Date().getFullYear()?{year:'numeric'}:{})})};
const fleetMatchTitle=s=>{const m=/^#([^\s:]+):\s+(.+)$/.exec(s||'');return m?t('{} in #{}',m[2],m[1]):s};
// A family question's messages open in the reader (open), so the owner can read them before anything goes.
const fleetMatches=(from,ms,open)=>html`<p class="fleet-from">${from}</p><ul class="fleet-matches">${ms.slice(0,5).map(m=>{const when=fleetMatchDay(m.at),said=[open?m.from:'',when].filter(Boolean).join(' · '),title=fleetMatchTitle(m.title)||m.from;return html`<li>${open?html`<button type="button" class="fleet-source" data-fleet-source="${m.id}" translate="no">${title}</button>`:html`<span>${title}</span>`}${said?html` <span class="muted">· <span translate="no">${said}</span></span>`:''}</li>`})}</ul>`;
function fleetAskCard(f,w,card,theirs,decide,title){const d=w.draft||{},ours=w.kind==='question',found=(ours?d.sources:d.matches)||[];
 // One that was set aside (family_question_check.py) shows only its words: nothing on what was found, or that nothing was.
 const from=found.length?fleetMatches(ours?'From your messages':'In your work accounts',found,ours):d.state==='aside'?'':html`<p class="muted">${ours?d.state==='empty'?'Nothing found. You can still answer.':'No draft this time. You can still answer.':'Nothing found in your work accounts. You can still answer.'}</p>`;
 return card(w.id,w,title,html`${ours?html`<blockquote>${w.question}</blockquote>`:theirs(w)}${from}<label class="fleet-field muted" for="fleet-free-${w.id}">Your answer (only this goes to them)<textarea id="fleet-free-${w.id}" maxlength="600">${d.text||''}</textarea></label>`,
  html`<div class="actions"><button class="primary" data-fleet-send="${w.id}">Send answer</button>${decide(w,'decline','Decline')}${fleetMore([decide(w,'never','Never from '+w.name)])}</div>`)}
fleetOn('click',e=>{const b=e.target.closest('[data-fleet-source]');if(b)openEvent(b.dataset.fleetSource,b.textContent)});
// The Family tab: ask one member's Machine, and how the questions asked so far stand.
function familyAsk(fam,people){const one=people.length===1&&fleetFirst(people[0].name);
 const state=q=>q.state==='answered'?html`<p class="family-answer"><span translate="no">${q.answer}</span></p>`
  :html`<p class="family-answer"><small class="muted">${q.state==='old'?t('{}’s Machine needs an update first.',fleetFirst(q.name)):q.state==='none'?'No answer':'No answer yet'}</small></p>`;
 return html`<div class="fleet-box family-ask"><h3>${one?t('Ask {}’s Machine',one):'Ask someone’s Machine'}</h3><form class="fleet-ask family-question-form">${one?html`<input type="hidden" name="member" value="${people[0].member_id}">`:html`<select name="member" aria-label="Who">${people.map(p=>html`<option value="${p.member_id}">${p.name}</option>`)}</select>`}<input name="text" maxlength="300" required placeholder="${t('Any news about the carpet?')}" aria-label="Question"><button class="primary">Ask</button></form>${(fam.questions||[]).length?html`<ul class="family-list">${fam.questions.map(q=>html`<li><span translate="no">“${q.question}”</span> <small class="muted">· <span translate="no">${fleetFirst(q.name)}</span> · ${fleetMatchDay(q.at)}</small>${state(q)}</li>`)}</ul>`:html`<p class="muted">Their Machine drafts an answer from their personal messages. They read it and send it.</p>`}</div>`}
fleetOn('submit',async e=>{const f=e.target;if(!f.classList.contains('family-question-form'))return;e.preventDefault();
 const b=f.querySelector('button');b.disabled=true;
 try{await fleetPost('family_question',{member_id:f.elements.member.value,text:f.elements.text.value.trim()});f.reset();toast('Asked. The answer shows here.');await fleetView()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
