// Here's what I've learned (state.first_look_learned, first_learned.py): at the end of the first look, under the to-dos
// (in the ending when there are none), how the owner writes, the people they work with most right now with what they
// work on together, and their usual hours. Work facts only, no filler: a part without enough signal isn't there. Each
// row has Not right, which opens a one-line fix in its place (Save; Remove takes it off); every fix is kept with Undo
// under Learning, Changes. The × closes it for good, on every device.
let lfOpen=null,lfText=null;  // the row being fixed: its key ('v<line>', 'p:<node id>', 'h'), and what is typed in it so far
const LF_X='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7L7 17"/></svg>';
const lfDay=(d,o)=>localeDate(new Date(2024,0,d),DL,{weekday:o});  // 1 Jan 2024 was a Monday: ISO weekday d
function lfDays(days){const d=(days||[]).map(Number).filter(n=>n>=1&&n<=7);if(d.join()==='1,2,3,4,5')return t('Weekdays');
 const run=d.length>2&&d.every((n,i)=>!i||n===d[i-1]+1);if(run)return t('{} to {}',lfDay(d[0],'long'),lfDay(d[d.length-1],'long'));
 try{return new Intl.ListFormat(I18N.lang||'en',{type:'conjunction',style:'short'}).format(d.map(n=>lfDay(n,'short')))}catch{return d.map(n=>lfDay(n,'short')).join(', ')}}
const lfClock=s=>{const [h,m]=String(s||'').split(':').map(Number);return fmtHM(new Date(2024,0,1,h|0,m|0))};
const lfHours=h=>h.text?h.text:t('{}, {} to {}',lfDays(h.days),lfClock(h.start),lfClock(h.end));
function lfRow(key,main,sub,value,label){
 if(lfOpen===key)return html`<li class="lf-row lf-editing"><form class="lf-edit" data-lf-form="${key}"><label><span>${label}</span><input name="text" value="${lfText??value}" maxlength="160" autocomplete="off"></label><span class="lf-acts"><button type="submit" class="primary">${t('Save')}</button><button type="button" class="quiet" data-lf-remove>${t('Remove')}</button><button type="button" class="quiet" data-lf-cancel>${t('Cancel')}</button></span></form></li>`;
 return html`<li class="lf-row"><span class="lf-text">${main?html`<strong translate="no">${main}</strong>`:''}<span${main?html` translate="no"`:''}>${sub}</span></span><button type="button" class="quiet lf-wrong" data-lf-wrong="${key}">${t('Not right')}</button></li>`}
function learnedCard(){const d=state?.first_look_learned;if(!d||scopeFilter==='personal')return '';
 const w=d.writing,people=d.people||[],h=d.hours;if(!w&&!people.length&&!h)return '';
 const part=(title,rows)=>html`<div class="lf-part"><h3>${title}</h3><ul>${rows}</ul></div>`;
 return html`<section class="learned-card" aria-labelledby="lf-title"><div class="lf-head"><h2 id="lf-title">${t('Here’s what I’ve learned')}</h2><button type="button" class="lf-x" data-lf-close aria-label="${t('Close')}" title="${t('Close')}">${raw(LF_X)}</button></div><p class="lf-sub">${t('From your first look. Fix anything that’s off.')}</p><div class="lf-grid">${
  w?part(t('How you write'),w.lines.map((l,i)=>lfRow('v'+i,'',l,l,t('How you write')))):''}${
  people.length?part(t('People you work with most'),people.map(p=>lfRow('p:'+p.id,p.name,p.topic,p.topic,t('What you work on with {}',p.name)))):''}${
  h?part(t('Your usual hours'),[lfRow('h','',lfHours(h),h.text||t('Usual hours: {}',lfHours(h)),t('When you usually work'))]):''}</div></section>`}
// Drawn in place (the list's own render keeps it while a fix is open: a refresh redraws the same row in the same state)
function learnedDraw(focus){const box=$('#suggestions .learned-card');if(!box)return;const card=learnedCard();if(!String(card)){box.remove();return}
 box.replaceWith(htmlNodes(card));if(focus){const el=$('#suggestions .learned-card '+focus);el?.focus();if(el?.select)el.select()}}
async function learnedSend(args){const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify(args)});
 state.first_look_learned=r.first_look_learned;return r}
function learnedArgs(key,text){const d=state.first_look_learned||{};
 if(key==='h')return{action:'learned_fix',args:{item:'hours',text,shown:lfHours(d.hours||{})}};
 if(key.startsWith('p:')){const p=(d.people||[]).find(x=>'p:'+x.id===key);return{action:'learned_fix',args:{item:'person',id:key.slice(2),text,shown:p?.name||''}}}
 const line=d.writing?.lines?.[+key.slice(1)];return{action:'learned_fix',args:{item:'voice',channel:d.writing?.channel,line,text}}}
$('#suggestions').addEventListener('click',async e=>{
 const x=e.target.closest('[data-lf-close]');if(x){x.disabled=true;try{await learnedSend({action:'learned_close',args:{}});lfOpen=lfText=null;learnedDraw()}catch(err){errCaught(err);x.disabled=false;toast(err.message,true)}return}
 const w=e.target.closest('[data-lf-wrong]');if(w){lfOpen=w.dataset.lfWrong;lfText=null;learnedDraw('input');return}
 if(e.target.closest('[data-lf-cancel]')){const k=lfOpen;lfOpen=lfText=null;learnedDraw(`[data-lf-wrong="${CSS.escape(k||'')}"]`);return}
 const rm=e.target.closest('[data-lf-remove]');if(rm&&lfOpen){rm.disabled=true;try{await learnedSend(learnedArgs(lfOpen,''));lfOpen=lfText=null;learnedDraw();toast(t('Taken off. Undo it under Learning, Changes.'))}catch(err){errCaught(err);rm.disabled=false;toast(err.message,true)}}});
$('#suggestions').addEventListener('submit',async e=>{const f=e.target.closest('[data-lf-form]');if(!f)return;e.preventDefault();const text=f.text.value.trim(),save=f.querySelector('[type=submit]');
 if(!text){f.querySelector('[data-lf-remove]').click();return}save.disabled=true;
 try{await learnedSend(learnedArgs(f.dataset.lfForm,text));lfOpen=lfText=null;learnedDraw();toast(t('Fixed. Undo it under Learning, Changes.'))}catch(err){errCaught(err);save.disabled=false;toast(err.message,true)}});
$('#suggestions').addEventListener('keydown',e=>{if(e.key==='Escape'&&e.target.closest('[data-lf-form]'))e.target.closest('form').querySelector('[data-lf-cancel]').click()});
$('#suggestions').addEventListener('input',e=>{if(e.target.closest('[data-lf-form]'))lfText=e.target.value});
