// A usage limit reset offered on To-dos before work stops (state.reset_nudge, ModelPacingApp.reset_nudge): a limit
// window holds background work back (model_budget.held_back) or a limit is reached, and resets are left. One quiet
// line above the to-dos: "ChatGPT weekly limit 92% used. Preparing is slowed. 2 resets left." with Use a reset, which is
// Settings' own button (settings-models.js: its confirm, then model_reset), and × to hide it until that window resets.
// Hidden in this browser only. Part of the mailcheck group (dashboard_parts.LAZY): shell-render.js mailCheckSlot.
const nudgeKey=n=>`${n.window||'limit'}:${n.until||''}`;
function resetNudgeLine(){const n=state?.reset_nudge;if(!n?.resets||chatOpen())return '';let gone='';try{gone=localStorage.getItem('reset-nudge-gone')}catch{}
 if(gone===nudgeKey(n))return '';
 const held=n.reached||!n.window?'':t(n.window==='week'?'{} weekly limit {}% used. Preparing is slowed.':'{} 5-hour limit {}% used. Preparing is slowed.',n.name||'AI',+n.used|0);
 return html`<div class="reset-nudge"><span>${held} ${t(['{} reset left.','{} resets left.'],n.resets)}</span><button type="button" class="ghost" data-model-reset>${t('Use a reset')}</button><button type="button" class="fixed-close" data-reset-nudge-x aria-label="${t('Close')}" title="${t('Close')}">×</button></div>`}
const mailCheckTop=()=>html`${resetNudgeLine()}${mailCheckBlock()}`;
document.addEventListener('click',e=>{if(!e.target.closest('[data-reset-nudge-x]')||!state?.reset_nudge)return;try{localStorage.setItem('reset-nudge-gone',nudgeKey(state.reset_nudge))}catch{}render()});
