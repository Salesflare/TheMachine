// Back for a check-in while a teammate still has it: no Do it (that would prepare it all over again); Check in now leads
// (a nudge to them, drafted on the to-do). Once that nudge is being drafted or ready (handoff_checkin), it reads and acts
// like any prepared to-do: Send leads.
const withTeammate=s=>!closed(s)&&s.status!=='snoozed'&&!s.handled_hint&&!s.handoff_checkin&&['asked','waiting for them'].includes(s.fleet_handoff?.stage)&&!redirect(s);
// A new handoff text on a card a teammate still has (the owner asked to hand it to someone else): it waits for their review.
const redirect=s=>!closed(s)&&s.status!=='snoozed'&&['asked','waiting for them'].includes(s.fleet_handoff?.stage)&&taskActions(s).some(a=>a.kind==='handoff');
const firstName=n=>String(n||'').split(' ')[0];
// A handoff that didn't go out to "Pat’s Machine" (Pat Lee): said with a first name, like the chat's lines
const handoffMachine=n=>n&&n!=='A teammate'?t('{}’s Machine',String(n).split(' ')[0]):t('a teammate’s Machine');
const handoffFailed=s=>s.fleet_handoff_failed&&!s.fleet_handoff&&!closed(s)?html`<p class="note fleet handoff-failed" role="alert">${t('Handoff didn’t go out to {}',handoffMachine(s.fleet_handoff_failed.name))} · <button type="button" class="link" data-fleet-handoff="${s.id}">Try again</button></p>`:'';
// Their Machine can't notify them (no phone, Telegram or email on): said under the handoff while it waits on them
// What a check-in or handoff tap on this to-do has to say (it couldn't go): on this to-do, not in a toast over another
const handoffNotes=new Map(),handoffNote=s=>handoffNotes.has(s.id)&&!closed(s)?html`<p class="note fleet handoff-note" role="status">${handoffNotes.get(s.id)}</p>`:'';
const noPing=s=>s.fleet_handoff?.no_ping&&!closed(s)?html`<p class="note fleet no-ping" role="status">${t('{} won’t get a ping. Let them know.',firstName(s.fleet_handoff.name))}</p>`:'';
function fleetHandoff(s){const contact=s.handoff_contact?html`<p class="note handoff-contact">${t('Contact: {}',s.handoff_contact)}</p>`:'';
 if(handoffFailed(s))return html`${contact}${handoffFailed(s)}`;
 if(s.handoff_silent&&!s.fleet_handoff&&!closed(s))return html`${contact}<p class="note fleet silent-note">${s.handoff_silent.line} · <button type="button" class="link" data-handoff-not-mine="${s.id}">Not mine</button></p>`;  // theirs by what they did; one tap undoes it
 if(s.handoff_mail&&!s.fleet_handoff)return html`${contact}${mailHandoff(s)}`;
 if(contact&&!s.fleet_handoff)return contact;
 if(s.fleet_handoff)return html`<p class="note${s.fleet_handoff.back?'':html` handled`} fleet">${handoffLine(s.fleet_handoff,s)}</p>${noPing(s)}${s.handoff_wait&&s.snoozed_until?html`<p class="checkin-line" title="${date(s.snoozed_until)}">${checkinLabel(s)}</p>`:''}${handoffNote(s)}`;  // also once it is done
 if(closed(s)||!state?.fleet?.on||s.scope!=='work')return'';
 if(s.fleet_handoff)return html`<p class="note handled fleet">${t('Handed off to {}: {}',s.fleet_handoff.name,t(s.fleet_handoff.stage))}</p>`;
 return''}  // the Hand off button sits with the card's other buttons (cardActions); its form with the other editors
const handoffHolds=d=>d.to!=='email'&&(d.holding||[]).some(h=>h.fleet+'|'+h.member_id===d.to);
// Hand off to a teammate: the same calm sheet as Hand to Codex / Claude Code (.agent-sheet). Who, then what they are
// asked to do as editable lead text, what goes along as chips with a quiet ×, an optional note.
function handoffEditor(s){const d=handingOff.get(s.id);if(!d||closed(s))return'';const id=s.id,mail=d.to==='email';
 const opts=[...d.who.map(([f,m,n])=>[f+'|'+m,n]),['email','By email']];
 const pick=opts.length<=4?html`<span class="agent-switch" role="radiogroup" aria-label="Hand off to">${opts.map(([v,n])=>html`<label><input type="radio" name="to" value="${v}"${d.to===v?html` checked`:''}><span>${n}</span></label>`)}</span>`
  :html`<select name="to" class="handoff-pick" aria-label="Hand off to">${opts.map(([v,n])=>html`<option value="${v}"${d.to===v?html` selected`:''}>${n}</option>`)}</select>`;
 const name=mail?t('them'):((d.who.find(([f,m])=>f+'|'+m===d.to)||[])[2]||t('them'));
 const x=(what,attr)=>html`<button type="button" class="chip-x" ${attr} aria-label="Leave out ${what}" title="Leave out">×</button>`;
 const chips=mail?'':orEmpty(html`${[...(d.contact&&d.with_contact!==false?[html`<span class="agent-get"><i class="via-ico via-link" aria-hidden="true"></i><span class="agent-get-label">${t('Contact: {}',d.contact)}</span>${x(d.contact,html`data-handoff-drop="contact"`)}</span>`]:[]),
  ...(d.sources||[]).map((v,n)=>d.dropped?.includes(n)?'':html`<span class="agent-get"><i class="via-ico via-${v.kind==='email'?'mail':'chat'}" aria-hidden="true"></i><span class="agent-get-label">${v.label}</span>${x(v.label,html`data-handoff-drop="${n}"`)}</span>`)]}`);
 const had=!mail&&['asked','waiting for them'].includes(s.fleet_handoff?.stage)&&(d.who.find(([f,m])=>f+'|'+m===d.to)||[])[2]!==s.fleet_handoff.name?[firstName(s.fleet_handoff.name),...(s.fleet_handoff.also||[])].join(' and '):'';
 const back=had?html`<label class="handoff-back"><input type="checkbox" name="replace"${d.replace===false?'':html` checked`}> Take it back from ${had}</label>`:'';
 const err=d.error?html`<p class="handoff-error" role="alert">${d.error}</p>`:'';
 // Someone who still has it: handing it to them again is a check-in on that handoff (Check in now), with an optional line
 if(handoffHolds(d))return html`<form class="fleet-handoff-form agent-sheet handoff-checkin-form" data-card="${id}"><div class="agent-sheet-head"><span class="agent-sheet-title">Hand off to</span>${pick}</div>
 <p class="agent-what">${t('{} still has this. Check in drafts a short nudge for you to send.',firstName(name))}</p>
 <textarea name="note" class="agent-note" spellcheck="true" autocapitalize="sentences" rows="1" maxlength="600" placeholder="${t('Anything to add? Optional')}" aria-label="${t('Anything to add? Optional')}">${d.checkin_note||''}</textarea>${err}
 <div class="agent-sheet-foot"><button type="button" class="ghost" data-handoff-cancel="${id}">Cancel</button><button class="primary">${t('Check in')}</button></div></form>`;
 return html`<form class="fleet-handoff-form agent-sheet" data-card="${id}"><div class="agent-sheet-head"><span class="agent-sheet-title">Hand off to</span>${pick}</div><input type="hidden" name="title" value="${d.title}">
 ${mail?html`<input name="email" type="email" class="handoff-email" maxlength="254" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="handoff-team-${id}" value="${d.email||''}" placeholder="Their email" aria-label="Their email" required><ul class="cal-sug handoff-sug" id="handoff-team-${id}" role="listbox" aria-label="Teammates" hidden></ul>`:''}
 <textarea name="task" class="agent-note handoff-task" spellcheck="true" autocapitalize="sentences" rows="1" maxlength="1000" aria-label="What they are asked to do">${d.task??d.summary}</textarea>${!mail&&chips?html`<div class="agent-gets" aria-label="Goes along">${chips}</div>`:''}
 <textarea name="note" class="agent-note" spellcheck="true" autocapitalize="sentences" rows="1" maxlength="600" placeholder="${t('Add a note for {}',name)}" aria-label="${t('Add a note for {}',name)}">${d.note||''}</textarea>${mail?mailParts(d):''}${back}${err}
 <div class="agent-sheet-foot"><button type="button" class="ghost" data-handoff-cancel="${id}">Cancel</button><button class="primary"${mail&&d.parts?.mailbox===false?html` disabled`:''}>${mail?'Prepare email':'Hand off'}</button></div></form>`}
// By email: what goes in the email (handoff_mail.parts), each ticked until the owner unticks it. Only what the Team Graph
// shares with the team is offered; the email then waits on the to-do for the owner to read and send.
function mailParts(d){const p=d.parts,off=d.off||new Set();if(!p)return html`<p class="agent-what">${t('You read it on the to-do before it goes.')}</p>`;
 if(p.mailbox===false)return html`<p class="agent-what handoff-no-mailbox" role="status">${t('No Gmail or Outlook account to send it from. Connect one in Connections.')}</p>`;  // nothing to send it from: said here, not as an error
 const row=(k,body)=>html`<label class="handoff-part"><input type="checkbox" data-handoff-part="${k}"${off.has(k)?'':html` checked`}><span>${body}</span></label>`;
 const ico=k=>html`<i class="via-ico via-${k}" aria-hidden="true"></i>`;
 const rows=[...p.lines.map(x=>row(x.key,(x.key==='due'?t('Due {}',tpDay(x.due)):x.text))),...(p.draft?[row('draft',html`${ico('mail')}${t('Draft ready to send: {}',p.draft.subject)}`)]:[]),
  ...p.links.map(x=>row(x.key,html`${ico('link')}${(x.title||x.url)}`)),...p.files.map(x=>row(x.key,html`${ico('file')}${x.name}`)),row('take',t('Take this on in your own Machine'))];
 return html`<fieldset class="handoff-parts"><legend>${t('Goes in the email')}</legend>${rows}</fieldset>${p.shared?'':html`<p class="agent-what">${t('Personal and Only you content stays out.')}</p>`}<p class="agent-what">${t('You read it on the to-do before it goes.')}</p>`}
// On the to-do once it went out: who has it, and the promise to track until it's done.
function mailHandoff(s){const m=s.handoff_mail;if(!m)return'';const first=firstName(m.name),led=s.task_page?.lead&&s.task_page.state!=='offered';
 return html`${led?'':html`<p class="note handled fleet">${t('Handed to {} by email',m.name)}</p>`}${m.promise?html`<p class="checkin-line handoff-promise">${m.promise==='kept'?t('{} took this on',first):t('{} takes this on',first)}</p>`:''}`}
// Hand off by email: teammates at the owner's company first (api/invitees team: the Graph's people on its domains,
// then what is typed completed with each domain).
{let timer=0,seq=0;const sugOf=t=>t.parentElement?.querySelector('.handoff-sug'),hide=t=>{const l=sugOf(t);if(l){l.hidden=true;l.replaceChildren()}t.setAttribute('aria-expanded','false')};
 document.addEventListener('input',e=>{const t=e.target;if(!t.matches?.('.handoff-email'))return;const list=sugOf(t),q=t.value.trim();clearTimeout(timer);const n=++seq;if(!list)return;if(q.length<2){hide(t);return}
  timer=setTimeout(async()=>{let found=[];try{found=(await request('api/invitees?team=1&q='+encodeURIComponent(q))).people||[]}catch{}if(n!==seq)return;found=found.filter(p=>p.email!==q.toLowerCase());
   setHTML(list,html`${found.map(p=>html`<li><button type="button" role="option" tabindex="-1" data-team-email="${p.email}" data-team-name="${p.name||''}">${p.name?html`<span>${p.name}</span><small>${p.email}</small>`:html`<span>${p.email}</span>`}</button></li>`)}`);
   list.hidden=!found.length;t.setAttribute('aria-expanded',String(!!found.length))},250)});
 document.addEventListener('pointerdown',e=>{if(e.target.closest?.('.handoff-sug'))e.preventDefault()});
 document.addEventListener('click',e=>{const b=e.target.closest?.('[data-team-email]');if(!b)return;const t=b.closest('form')?.querySelector('.handoff-email');if(!t)return;seq++;t.value=b.dataset.teamEmail;hide(t);t.focus();
  const d=handingOff.get(t.form?.dataset.card);if(d)Object.assign(d,{email:t.value,picked:{email:t.value,name:b.dataset.teamName||''}})});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&e.target.matches?.('.handoff-email')&&!sugOf(e.target)?.hidden){e.preventDefault();e.stopPropagation();seq++;hide(e.target)}},true);
 document.addEventListener('focusout',e=>{const t=e.target;if(t.matches?.('.handoff-email'))setTimeout(()=>{if(document.activeElement!==t){seq++;hide(t)}},200)})}
// Hand to Claude Code / Hand to Codex (agent_jobs.py): the owner reads and edits the brief; the card then follows the job:
// Sent, Running (or Waiting for their computer), a Result to mark done, ask changes on or hand off again, or Failed.
const agentEditing=new Map(),agentAsking=new Set(),AGENT_ACTIVE=['sent','running','waiting'];
const agentTools=()=>state?.agent_tools||[];
const agentWhere=x=>x.place==='device'?t('Runs on {}, with the Codex signed in there.',x.device):agentWhereElse(x);
const agentWhereElse=x=>x.place==='cloud'?t('Runs in Codex cloud, not on your computer.'):x.place==='remote'?t('Runs in your Claude session on {}.',x.device):t('Runs on this computer with your own {} setup.',x.name);
const canAgent=s=>!closed(s)&&s.status!=='snoozed'&&agentTools().length>0&&!AGENT_ACTIVE.includes(s.agent_job?.status);
const agentOpen=s=>{const j=s.agent_job;return!!j&&!closed(s)&&!j.outcome&&['result','failed'].includes(j.status)};
const agentCancel=j=>html`<div class="actions"><button class="ghost" data-agent-cancel="${j.id}">Cancel</button></div>`;
// A Codex thread opens on this computer: from the owner's other devices through the Codex app's remote connection (hostId).
const onMachine=()=>['localhost','127.0.0.1','[::1]','::1'].includes(location.hostname);
const agentHref=j=>j.url_elsewhere&&/^codex:\/\/threads\/[0-9a-f-]{36}\?hostId=/.test(j.url_elsewhere)&&!onMachine()?j.url_elsewhere:j.url;
// Its label is built in the owner's language here (translate="no": the page doesn't read it again). While The Machine's
// own Codex runs the turn the Codex app can't open the thread yet (it says it can't find it): the link says so instead.
const agentApp=j=>j.app_name?t('Open in {}',j.app_name):t('Open');
const AGENT_LATER='Codex is still on it here. It opens in the Codex app when it’s done.';
const agentLink=j=>j.url&&/^(https:\/\/|codex:\/\/threads\/)/.test(j.url)?html`<a class="agent-app" href="${agentHref(j)}" target="_blank" rel="noreferrer" translate="no" aria-label="${agentApp(j)}"${j.opens_later?html` data-later title="${t(AGENT_LATER)}"`:''}><span class="agent-app-long">${agentApp(j)}</span><span class="agent-app-short">${t('Open')}</span> ↗</a>`:'';
document.addEventListener('click',e=>{if(e.target.closest?.('a.agent-app[data-later]')){e.preventDefault();toast(t(AGENT_LATER))}});
// A result's header keeps one row: when "Open in Codex" no longer fits next to the tool's name it reads "Open" (the
// name is already on the left). Measured per header as its width changes, not at a fixed screen width.
// A wider header tries the long label again; any other change (a late font, new text) only ever shortens it, so it can't flip back and forth.
const agentHeadWraps=h=>{const a=h.querySelector('a.agent-app'),n=h.firstElementChild;return !!a&&a!==n&&a.getBoundingClientRect().top>=n.getBoundingClientRect().bottom-1};
function agentHeadSize(h,width){if(width!==undefined&&h._fitW!==width){h._fitW=width;h.classList.remove('tight')}if(!h.classList.contains('tight')&&agentHeadWraps(h))h.classList.add('tight')}
const agentHeadFit=new ResizeObserver(rows=>{for(const {target:h,contentRect:r} of rows)if(r.width&&h._fitW!==r.width)agentHeadSize(h,r.width)});  // the width it has (or none): nothing to measure
// A header drawn anew is fitted before it is painted, so a refresh never shows it wrapped first and then pulls the card up
new MutationObserver(()=>{for(const h of document.querySelectorAll('.agent-result .agent-head:not([data-fit])')){h.dataset.fit='';agentHeadSize(h);agentHeadFit.observe(h)}}).observe(document.body,{childList:true,subtree:true});
const agentHeadsFit=()=>{for(const h of document.querySelectorAll('.agent-result .agent-head[data-fit]'))agentHeadSize(h)};
document.fonts?.ready.then(agentHeadsFit);document.fonts?.addEventListener?.('loadingdone',agentHeadsFit);
// A job's follow-up goes to the same session: the card's Change asks the agent while its result is open.
const agentAsk=s=>agentOpen(s)&&s.agent_job.can_follow_up;
const agentFile=(j,f)=>html`<a class="agent-file" href="api/agent-file?job=${encodeURIComponent(j.id)}&path=${encodeURIComponent(f.path)}" target="_blank" rel="noreferrer">${f.path.split('/').pop()}</a>`;
// The agent's own words, as text: a link to one of its files is that file's chip, other local paths are just their name,
// markdown marks go. Never a path on this computer.
function agentText(j,text,used=[]){const chips=[],files=j.files||[];
 const fileFor=t=>{const name=String(t).split(/[\\/]/).pop();return files.find(f=>f.path===t||f.path.split('/').pop()===name)};
 let t=String(text||'').replace(/\r/g,'').replace(/\[([^\]\n]+)\]\(([^)\s]+)\)/g,(m,label,target)=>{if(/^https?:/.test(target))return m;const f=fileFor(target);if(f){used.push(f);chips.push(agentFile(j,f));return '\u0002'+(chips.length-1)+'\u0003'}return label})
  .replace(/`([^`\n]+)`/g,'$1').replace(/^#{1,6}\s+/gm,'').replace(/^\s*[*-]\s+/gm,'• ')
  .replace(/(^|[\s(])(?:~|\/(?:home|Users|tmp|var|root|data|mnt|opt|srv))(?:\/[^\s/)]+)*\/([^\s/)]+)/g,'$1$2');
 // the file chips go in where their marks are, through the DOM
 return htmlEdit(html`${t.trim().split(/\n\s*\n/).filter(Boolean).map(p=>html`<p>${format(p,true)}</p>`)}`,c=>{const w=document.createTreeWalker(c,NodeFilter.SHOW_TEXT),hits=[];
  while(w.nextNode())if(/\u0002\d+\u0003/.test(w.currentNode.data))hits.push(w.currentNode);
  for(const n of hits)n.replaceWith(...n.data.split(/\u0002(\d+)\u0003/).map((x,i)=>i%2?htmlNodes(chips[x]):x))})}
// Which of a job's files to show as chips: the ones its answer names, else what it made for the owner. Housekeeping
// (.pid, .log, lock and scratch files, dot folders) only shows under Details. At most AGENT_CHIPS, then "+N more".
const AGENT_CHIPS=3,AGENT_NOISE=/(^|\/)(\.[^/]*|node_modules|__pycache__|tmp|temp|scratch|cache|logs?)(\/|$)|\.(pid|log|lock|tmp|temp|swp|swo|bak|orig|out|err)$|~$/i;
function agentPick(paths,text){const said=String(text||''),named=paths.filter(f=>said.includes(f)||said.includes(f.split('/').pop()));
 const shown=(named.length?named:paths.filter(f=>!AGENT_NOISE.test(f))).slice(0,AGENT_CHIPS);return {shown,hidden:paths.length-shown.length}}
const agentMoreFiles=n=>n?html`<button type="button" class="agent-file agent-morefiles" data-agent-files>+${n} more</button>`:'';
const agentAllFiles=(j,paths,label=true)=>html`<div class="agent-allfiles">${label?html`<p class="muted">All files</p>`:''}<div class="agent-files">${paths.map(f=>agentFile(j,{path:f}))}</div></div>`;
// The result in one line: its first paragraph, cut at a sentence when long. The rest folds behind What it did.
function agentLine(text){const first=String(text||'').trim().split(/\n\s*\n/)[0]||'';if(first.length<=240)return first;const cut=first.slice(0,240),end=Math.max(cut.lastIndexOf('. '),cut.lastIndexOf('! '),cut.lastIndexOf('? '));return end>80?cut.slice(0,end+1):cut.replace(/\s+\S*$/,'')+'…'}
// A result hides with Hide; handing it off again is the … menu's Hand off. A failed job keeps Try again and Hand off again beside it.
const agentTools2=(s,j,retry)=>html`<div class="agent-tools">${retry?html`<button data-agent-retry="${j.id}">Try again</button><button data-agent-again="${s.id}">Hand off again</button>`:''}<button data-agent-aside="${j.id}">Hide</button></div>`;
function agentBlock(s){const j=s.agent_job;if(!j||['set_aside','again'].includes(j.outcome)||(closed(s)&&j.status!=='result'))return'';
 const who=j.name,cloud=j.place==='cloud',since=j.started_at||j.updated_at;
 if(j.status==='sent')return html`<div class="agent-job"><p class="note">${t(cloud?'Sent to {} in Codex cloud. Starting soon.':'Sent to {}. Starting soon.',who)}</p>${agentCancel(j)}</div>`;
 if(j.status==='waiting')return html`<div class="agent-job"><p class="note">${t('Sent. Waiting for {}.',j.device||t('your computer'))} ${agentLink(j)}</p>${agentCancel(j)}</div>`;
 if(j.status==='running')return html`<div class="agent-job"><p class="note">${t(cloud?'{} is working on it in Codex cloud':'{} is working on it',who)} · <span class="elapsed" data-since="${since}">${elapsed(since)}</span> ${agentLink(j)}</p>${j.progress?html`<p class="muted agent-progress">${j.progress}</p>`:''}${agentCancel(j)}</div>`;
 if(j.status==='failed'&&j.error_kind==='busy')return html`<div class="agent-job"><p class="note">${j.error} ${agentLink(j)}</p>${closed(s)?'':agentTools2(s,j,true)}</div>`;
 if(j.status==='failed')return html`<div class="agent-job"><p class="note failed">${htmlT('{} stopped: {}',who,html`<span class="agent-error">${j.error||t('it did not finish')}</span>`)} ${agentLink(j)}</p>${closed(s)?'':agentTools2(s,j,true)}</div>`;
 if(j.status==='cancelled')return closed(s)?'':html`<div class="agent-job"><p class="note">${t('{}: canceled.',who)}</p></div>`;
 // What it did: the answer after its line (its first paragraph shows once, above), without the headings that only title it
 const line=agentLine(j.summary),first=String(j.summary||'').trim().split(/\n\s*\n/)[0]||'',all=String(j.summary||'').trim();
 const restText=(line===first?all.slice(first.length):all).replace(/^\s*(#{1,6}[^\n]*(\n|$)\s*)+/,'').trim(),rest=!!restText;
 const files=(j.files||[]).filter(f=>!(j.draft_updated&&f.path==='draft.md'));
 const inLine=[],lineHtml=agentText(j,line,inLine),own=files.filter(f=>!inLine.includes(f)).map(f=>f.path);  // a file already in the line is not repeated
 const pick=agentPick(own,j.summary);
 const chips=pick.shown.length||pick.hidden?html`<div class="agent-files">${pick.shown.map(f=>agentFile(j,{path:f}))}${agentMoreFiles(pick.hidden)}</div>`:'';
 const diff=j.has_diff?html`<details class="agent-diff" data-agent-diff="${j.id}"><summary>Show changes</summary><pre></pre></details>`:'';
 const more=rest||diff||pick.hidden?html`<details class="agent-more"><summary>What it did</summary>${rest?html`<div class="agent-text">${agentText(j,restText)}</div>`:''}${pick.hidden?agentAllFiles(j,own):''}${diff}</details>`:'';
 return html`<div class="agent-job draft agent-result" role="group" aria-label="${t('{} result',j.name)}"><div class="agent-head"><span class="dm">${who}${j.place==='cloud'?' (Codex cloud)':''}${j.turns>1?' · '+t('after your changes'):''}</span>${agentLink(j)}</div><div class="agent-line agent-text">${lineHtml}</div>${j.draft_updated?html`<p class="muted agent-progress">Updated the draft below. Send it when it reads right.</p>`:''}${chips}${more}${closed(s)?'':agentTools2(s,j,false)}</div>`}
// Hand to Codex / Claude Code: a compact sheet (in the chat it takes the message box's place). One plain line of what it
// will do, small chips for what it gets (never links), an optional note; the whole job only behind "See the full job".
const agentToolName=t=>t.place==='cloud'?t.name+' cloud':t.name;
const AGENT_GETS={mail:'mail',chat:'chat',draft:'note',file:'file',link:'link'};
function agentEditor(s){const d=agentEditing.get(s.id);if(!d||closed(s))return'';const t=agentTools().find(x=>x.id===d.tool)||agentTools()[0];if(!t)return'';
 const n=agentToolName(t),id=s.id;
 const pick=agentTools().length>1?html`<span class="agent-switch" role="radiogroup" aria-label="Hand to">${agentTools().map(x=>html`<label title="${agentWhere(x)}"><input type="radio" name="tool" value="${x.id}"${x.id===t.id?html` checked`:''}><span>${agentToolName(x)}</span></label>`)}</span>`
  :html`<input type="hidden" name="tool" value="${t.id}"><span class="agent-one" title="${agentWhere(t)}">${n}</span>`;
 const gets=orEmpty(html`${(d.gets||[]).map(g=>html`<span class="agent-get"><i class="via-ico via-${AGENT_GETS[g.kind]||'file'}" aria-hidden="true"></i><span class="agent-get-label">${g.label}</span></span>`)}`);
 return html`<form class="agent-form agent-sheet" data-card="${id}"><div class="agent-sheet-head"><span class="agent-sheet-title">Hand to</span>${pick}</div>
 ${d.line?html`<p class="agent-what">${d.line}</p>`:''}${gets?html`<div class="agent-gets" aria-label="What it gets">${gets}</div>`:''}
 <textarea id="agent-note-${id}" spellcheck="true" autocapitalize="sentences" name="note" class="agent-note" rows="1" maxlength="4000" placeholder="${window.t('Add a note for {}',n)}" aria-label="${window.t('Add a note for {}',n)}">${d.note||''}</textarea>
 <details class="agent-full" data-agent-full="${id}"${d.full?html` open`:''}><summary>See the full job</summary><textarea id="agent-brief-${id}" name="brief" maxlength="12000" spellcheck="false" aria-label="The full job">${d.brief}</textarea></details>
 <div class="agent-sheet-foot"><button type="button" class="ghost" data-agent-edit-cancel="${id}">Cancel</button><button class="primary">Hand off</button></div></form>`}
function agentAskEditor(s){if(!agentAsking.has(s.id)||!s.agent_job)return'';
 return html`<div class="change-editor"><label for="agent-ask-${s.id}">What should ${s.agent_job.name} change? <small>Goes to the ${s.agent_job.name} job</small></label><textarea id="agent-ask-${s.id}" spellcheck="true" autocapitalize="sentences" maxlength="4000" placeholder="Ctrl+Enter sends"></textarea><div class="actions"><button class="primary" data-agent-ask-send="${s.id}">Send</button><button class="ghost" data-agent-ask-cancel="${s.id}">Cancel</button></div></div>`}
const agentPost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
async function agentHand(id,tool,b){if(b)b.disabled=true;try{const d=await agentPost('agent_draft',{suggestion_id:id});agentEditing.set(id,{tool,brief:d.brief,line:d.line,gets:d.gets,note:''});render();if(chatId)paintChat();document.getElementById('agent-note-'+id)?.focus()}catch(err){errCaught(err);toast(err.message,true)}finally{if(b)b.disabled=false}}
$('#suggestions').addEventListener('click',async e=>{const t=e.target;let b;
 if(b=t.closest('[data-agent-hand]'))return agentHand(b.dataset.card,b.dataset.agentHand,b);
 if(b=t.closest('[data-agent-files]')){const d=b.closest('.agent-job,.chat-msg')?.querySelector('details.agent-more');if(d){d.open=true;d.querySelector('.agent-allfiles')?.scrollIntoView({block:'nearest'})}return}
 if(b=t.closest('[data-agent-again]')){const s=state.suggestions.find(x=>x.id===b.dataset.agentAgain);return agentHand(b.dataset.agentAgain,s?.agent_job?.tool,b)}
 if(b=t.closest('[data-agent-edit-cancel]')){agentEditing.delete(b.dataset.agentEditCancel);render();if(chatId)$('#chat-input')?.focus();return}
 if(b=t.closest('[data-agent-ask]')){agentAsking.add(b.dataset.agentAsk);render();document.getElementById('agent-ask-'+b.dataset.agentAsk)?.focus();return}
 if(b=t.closest('[data-agent-ask-cancel]')){agentAsking.delete(b.dataset.agentAskCancel);render();return}
 if(b=t.closest('[data-agent-ask-send]'))return agentAskSend(b.dataset.agentAskSend,b);
 const act=[['agentCancel','agent_cancel','Canceled.'],['agentRetry','agent_retry','Sent again.'],['agentAside','agent_outcome','']].find(([k])=>t.closest(`[data-${k.replace(/[A-Z]/g,c=>'-'+c.toLowerCase())}]`));
 if(act){b=t.closest(`[data-${act[0].replace(/[A-Z]/g,c=>'-'+c.toLowerCase())}]`);b.disabled=true;try{await agentPost(act[1],{job_id:b.dataset[act[0]],...(act[1]==='agent_outcome'?{outcome:'set_aside'}:{})});if(act[2])toast(act[2]);await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}}});
async function agentAskSend(id,b){const s=state.suggestions.find(x=>x.id===id),box=document.getElementById('agent-ask-'+id);if(!s?.agent_job||!box?.value.trim())return;if(b)b.disabled=true;
 try{await agentPost('agent_follow_up',{job_id:s.agent_job.id,text:box.value.trim()});agentAsking.delete(id);box.value='';toast('Sent to '+s.agent_job.name+'.');await refresh()}catch(err){errCaught(err);if(b)b.disabled=false;toast(err.message,true)}}
$('#suggestions').addEventListener('keydown',e=>{const box=e.target.closest('textarea[id^="agent-ask-"]');if(box&&e.key==='Enter'&&(e.ctrlKey||e.metaKey)){e.preventDefault();agentAskSend(box.id.slice(10))}});
$('#suggestions').addEventListener('input',e=>{const f=e.target.closest('.agent-form');const d=f&&agentEditing.get(f.dataset.card);if(!d)return;
 if(e.target.name==='tool'){d.tool=e.target.value;const t=agentTools().find(x=>x.id===d.tool),n=t?agentToolName(t):'';const note=f.elements.note;note.placeholder=note.ariaLabel=window.t('Add a note for {}',n)}
 else if(e.target.name==='note')d.note=e.target.value;else d.brief=f.elements.brief.value});
$('#suggestions').addEventListener('toggle',e=>{const x=e.target;if(!x.matches?.('[data-agent-full]'))return;const d=agentEditing.get(x.dataset.agentFull);if(d)d.full=x.open},true);
$('#suggestions').addEventListener('submit',async e=>{const f=e.target;if(!f.classList.contains('agent-form'))return;e.preventDefault();const id=f.dataset.card,d=agentEditing.get(id),b=f.querySelector('button.primary');if(!d)return;b.disabled=true;
 try{const j=await agentPost('agent_send',{suggestion_id:id,tool:f.elements.tool?.value||d.tool,brief:f.elements.brief.value,note:f.elements.note?.value.trim()||''});agentEditing.delete(id);f.elements.brief.value='';toast('Sent to '+j.name+'.');await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#suggestions').addEventListener('toggle',async e=>{const d=e.target;if(!d.matches?.('[data-agent-diff]')||!d.open)return;const pre=d.querySelector('pre');if(pre.textContent)return;
 try{const r=await fetch('api/agent-diff?job='+encodeURIComponent(d.dataset.agentDiff),{credentials:'same-origin'});pre.textContent=r.ok?await r.text():'The changes are not available.'}catch{pre.textContent='The changes are not available.'}},true);
// While a job runs, follow it every few seconds with the small /api/agent-jobs, not the whole status.
setInterval(async()=>{if(document.hidden||!(state?.suggestions||[]).some(s=>AGENT_ACTIVE.includes(s.agent_job?.status)))return;
 try{const r=await request('api/agent-jobs');let changed=false,ended=false;for(const s of state.suggestions){const j=r.jobs?.[s.id];if(!j||JSON.stringify(j)===JSON.stringify(s.agent_job))continue;if(AGENT_ACTIVE.includes(s.agent_job?.status)&&!AGENT_ACTIVE.includes(j.status))ended=true;s.agent_job=j;changed=true}
 if(ended)await refresh();else if(changed&&!document.querySelector('#suggestions textarea:focus,#suggestions select:focus,#suggestions input:focus'))render()}catch{}},4000);
// In a to-do's Details: the team learnings its draft followed, each with Remove (gone for the whole Fleet).
const teamLearningsUsed=s=>{const l=(s.team_learnings_used||[]).map(l=>html`<p class="note fleet fleet-learn-used">${t('Used a team learning: {}',String(l.text||'').replace(/<[^>]*>/g,''))} <button type="button" class="link" data-fleet-learn-remove="${l.fp}" data-fleet="${l.fleet}">${t('Remove')}</button></p>`);return l.length?html`${l}`:''};
function fleetNote(s){if(closed(s))return fleetHandoff(s);const h=s.fleet_holder;let out='';
 if(h?.offer)out=html`${out}${html`<p class="note fleet">${h.offer.join(', ')} also got this email. <button type="button" class="link" data-fleet-take="${s.id}">Tell them you’re on it</button></p>`}`;
 else if(h?.name&&!h.mine)out=html`${out}${html`<p class="note handled fleet">${h.name} is on it. <button type="button" class="link" data-fleet-take="${s.id}">I’ll handle it</button></p>`}`;
 if(s.fleet_context?.length)out=html`${out}${html`<p class="note fleet">From your Fleet: ${s.fleet_context.join(' · ')}</p>`}`;
 if(s.fleet_split)out=html`${out}${html`<p class="note fleet">Follow-ups split in your Fleet: ${s.fleet_split}</p>`}`;return html`${out}${fleetHandoff(s)}`}
