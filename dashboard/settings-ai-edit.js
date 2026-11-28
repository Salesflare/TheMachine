// A lazy part (dashboard_parts.LAZY 'aiedit'): a connected AI's Change panel, which settings-ai.js aiConnection asks for
// when Change opens: access, area and Extend, Activity, Turn off now and Remove (their changes and clicks are
// settings-ai.js's), what Messages does, and the Events switches, one per MCP event (ai_events.py,
// docs/ai-connections.md, Events). Each event is off until the owner turns it on; turning one off ends the AI's watch on
// it at once (ai_access.change).
const AI_EXPIRY=[['1d','1 day'],['7d','7 days'],['30d','30 days'],['1y','1 year']];
const AI_EVENTS=[['todo.created','New to-dos'],['meeting.briefing_ready','Meeting briefings'],['promise.due','Promises due']];
const aiOptions=(list,now)=>list.map(([v,l])=>`<option value="${v}"${v===now?' selected':''}>${esc(t(l))}</option>`).join('');
const aiEditPanel=(c,both,open)=>`<span class="ai-controls"><select data-ai-level aria-label="Access">${aiOptions(AI_LEVELS,c.level)}</select>${both?`<select data-ai-area aria-label="What it can see">${aiOptions(AI_AREAS,c.area)}</select>`:''}<select data-ai-expiry aria-label="For how long"><option value="" selected>${esc(t(c.expired?'Renew for…':'Extend…'))}</option>${aiOptions(AI_EXPIRY,'')}</select></span>
<span class="ai-controls"><button type="button" class="ghost" data-ai-activity aria-expanded="${open}">Activity</button>${c.level!=='off'?'<button type="button" class="ghost" data-ai-off>Turn off now</button>':''}<button type="button" class="ghost" data-ai-remove>Remove</button></span>
<small class="ai-msg-note"><strong>Messages</strong> Reads your email and chats. Its changes then wait for your OK.</small>
<span class="ai-evs"><span class="ai-ev-label">Events</span>${AI_EVENTS.map(([k,l])=>`<label class="ai-ev">${esc(t(l))}<button type="button" class="lookup-switch" role="switch" aria-checked="${(c.events||[]).includes(k)}" data-ai-event="${k}"></button></label>`).join('')}</span>
<small class="ai-msg-note"><strong>Events</strong> Wakes it when one happens, so it can start. It gets the title and a short why.</small>`;
$('#ai-list').addEventListener('click',e=>{const sw=e.target.closest('[data-ai-event]'),row=sw?.closest('[data-ai]');if(!row)return;
 sw.setAttribute('aria-checked',sw.getAttribute('aria-checked')!=='true');
 aiDo('ai_change',{id:row.dataset.ai,events:[...row.querySelectorAll('[data-ai-event][aria-checked=true]')].map(x=>x.dataset.aiEvent)},'Saved')});
