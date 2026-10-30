// New card: the owner adds a card in their own words. It goes through the same path as the cards the review makes
// (card_new), so it has the same states, buttons, chat, snooze and handoffs; the next review fills it in. Creating
// it sends nothing. One field is enough; Work or Personal, a due date, a person and an email are optional chips.
const nc={scope:null,due:null,about:[],attach:[],files:[],draft:'',pick:null,hits:[],timer:null,busy:false};
// "Friday", "in 2 weeks", "tomorrow", "24 Oct", "Oct 24", "24/10" or 2026-10-24, read as a date from today on; with a time
// too: "15:00", "2pm", "in 2 hours", "now", "tomorrow 9", "fri at 3pm". The same in the app's other languages ("over 2 uur",
// "morgen 9u", "demain 14h", "morgen um 9 Uhr", "mañana a las 9", "domani alle 15", "amanhã às 9"). A Date; .timed when a time was given.
const NC_WORDS=[[/\b(?:eind van de week|fin de semaine|fin de la semaine|ende der woche|fine settimana|fim da semana|fin de semana)\b/g,'end of week'],
 [/\b(?:eind van de maand|fin du mois|ende des monats|fine mese|fim do mes|fin de mes)\b/g,'end of month'],
 [/\b(?:volgende week|la semaine prochaine|semaine prochaine|nachste woche|la semana que viene|la proxima semana|proxima semana|semana que viene|la prossima settimana|prossima settimana|settimana prossima|semana que vem)\b/g,'next week'],
 [/\b(?:overmorgen|apres-demain|apres demain|ubermorgen|pasado manana|dopodomani|depois de amanha)\b/g,'in 2 days'],
 [/\b(?:vanavond|ce soir|heute abend|esta noche|stasera|hoje a noite)\b/g,'tonight'],
 [/\b(?:aujourd'hui|aujourd hui)\b/g,'today'],[/\b(?:a las|a la|alle|om|um|a|as)\b(?= \d)/g,'at'],[/\bun'/g,'a '],[/\b(\d{1,2}) uhr (\d{2})\b/g,'$1:$2'],[/\b(\d{1,2}) uhr\b/g,'$1:00']];
const NC_WORD={vandaag:'today',heute:'today',hoy:'today',oggi:'today',hoje:'today',morgen:'tomorrow',demain:'tomorrow',manana:'tomorrow',domani:'tomorrow',amanha:'tomorrow',
 nu:'now',maintenant:'now',jetzt:'now',ahora:'now',adesso:'now',agora:'now',over:'in',dans:'in',en:'in',tra:'in',fra:'in',em:'in',
 uur:'hours',uren:'hours',heure:'hours',heures:'hours',stunde:'hours',stunden:'hours',hora:'hours',horas:'hours',ora:'hours',ore:'hours',
 minuut:'minutes',minuten:'minutes',minuto:'minutes',minutos:'minutes',minuti:'minutes',dag:'days',dagen:'days',jour:'days',jours:'days',tag:'days',tage:'days',tagen:'days',dia:'days',dias:'days',giorno:'days',giorni:'days',
 weken:'weeks',semaine:'weeks',semaines:'weeks',woche:'weeks',wochen:'weeks',semana:'weeks',semanas:'weeks',settimana:'weeks',settimane:'weeks',
 maand:'months',maanden:'months',mois:'months',monat:'months',monate:'months',monaten:'months',mes:'months',meses:'months',mese:'months',mesi:'months',
 een:'a',ein:'a',eine:'a',einer:'a',einem:'a',un:'a',une:'a',una:'a',uno:'a',um:'a',uma:'a',twee:'two',deux:'two',zwei:'two',dos:'two',due:'two',dois:'two',duas:'two',drie:'three',trois:'three',drei:'three',tres:'three',tre:'three',
 maandag:'mon',lundi:'mon',montag:'mon',lunes:'mon',lunedi:'mon',segunda:'mon',dinsdag:'tue',mardi:'tue',dienstag:'tue',martes:'tue',martedi:'tue',terca:'tue',
 woensdag:'wed',mercredi:'wed',mittwoch:'wed',miercoles:'wed',mercoledi:'wed',quarta:'wed',donderdag:'thu',jeudi:'thu',donnerstag:'thu',jueves:'thu',giovedi:'thu',quinta:'thu',
 vrijdag:'fri',vendredi:'fri',freitag:'fri',viernes:'fri',venerdi:'fri',sexta:'fri',zaterdag:'sat',samedi:'sat',samstag:'sat',sabado:'sat',sabato:'sat',zondag:'sun',dimanche:'sun',sonntag:'sun',domingo:'sun',domenica:'sun',
 volgende:'next',prochain:'',prochaine:'',nachste:'next',nachsten:'next',proximo:'next',proxima:'next',prossimo:'next',prossima:'next',feira:'',
 januari:'jan',janvier:'jan',januar:'jan',enero:'jan',gennaio:'jan',janeiro:'jan',februari:'feb',fevrier:'feb',februar:'feb',febrero:'feb',febbraio:'feb',fevereiro:'feb',
 maart:'mar',mars:'mar',marz:'mar',marzo:'mar',marco:'mar',avril:'apr',abril:'apr',aprile:'apr',mei:'may',mai:'may',mayo:'may',maggio:'may',maio:'may',
 juni:'jun',juin:'jun',junio:'jun',giugno:'jun',junho:'jun',juli:'jul',juillet:'jul',julio:'jul',luglio:'jul',julho:'jul',augustus:'aug',aout:'aug',agosto:'aug',
 septembre:'sep',septiembre:'sep',settembre:'sep',setembro:'sep',oktober:'oct',octobre:'oct',octubre:'oct',ottobre:'oct',outubro:'oct',novembre:'nov',noviembre:'nov',novembro:'nov',
 decembre:'dec',dezember:'dec',diciembre:'dec',dicembre:'dec',dezembro:'dec'};
function ncDue(text,today=new Date()){let t=String(text||'').trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[’`]/g,"'").replace(/\s+/g,' ').replace(/^(by|on|due|before) /,'');
 for(const[re,to]of NC_WORDS)t=t.replace(re,to);
 t=t.split(' ').map(w=>w in NC_WORD?NC_WORD[w]:w).filter(Boolean).join(' ').replace(/^at /,'');if(!t)return null;
 const timed=x=>{if(x)x.timed=true;return x};
 if(t==='now')return timed(new Date(today));
 const NUM={a:1,an:1,one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9,ten:10};
 let m=/^in (\d{1,3}(?:[.,]5)?|a|an|one|two|three|four|five|six|seven|eight|nine|ten|half an?) ?(h|hrs?|hours?|m|mins?|minutes?)$/.exec(t);
 if(m){const n=/^half/.test(m[1])?.5:NUM[m[1]]||+m[1].replace(',','.');return timed(new Date(+today+n*(/^h/.test(m[2])?36e5:6e4)))}
 // A time of day: 15:00, 15.30, 15h, 15h30, 9u, 2pm, 2:30 pm; a bare hour ("9") only after a day ("tomorrow 9")
 const clock=(s,bare)=>{const c=/^(\d{1,2})(?:[:.](\d{2})|[hu](\d{2})?)?(?: ?([ap])\.?m?\.?)?$/.exec(s);if(!c)return null;
  if(!bare&&c[2]==null&&c[3]==null&&!c[4]&&!/[hu]$/.test(s))return null;let h=+c[1];const min=+(c[2]??c[3]??0);
  if(c[4]){if(h<1||h>12)return null;h=h%12+(c[4]==='p'?12:0)}if(h>23||min>59)return null;return[h,min]};
 let day=null,hm=null;
 m=/^(.*?) ?(?:at )?(\d{1,2}(?:[:.]\d{2}|[hu](?:\d{2})?)?(?: ?[ap]\.?m?\.?)?)$/.exec(t);
 if(m&&m[1]&&!/^(in \d+|\d{1,2})$/.test(m[1])&&(hm=clock(m[2],true))){day=ncDay(m[1].replace(/ at$/,''),today);if(!day)hm=null}
 if(!day&&(hm=clock(t,false))){const x=new Date(today);x.setHours(hm[0],hm[1],0,0);if(x<today)x.setDate(x.getDate()+1);return timed(x)}
 if(day&&hm){day.setHours(hm[0],hm[1],0,0);return timed(day)}
 if(t==='tonight'){const x=new Date(today);x.setHours(18,0,0,0);return x>today?timed(x):ncDay('today',today)}
 return ncDay(t,today)}
function ncDay(t,today){const d=new Date(today.getFullYear(),today.getMonth(),today.getDate()),add=n=>{d.setDate(d.getDate()+n);return d};
 const MONTHS=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'],DAYS=['sun','mon','tue','wed','thu','fri','sat'];
 const NUM={a:1,an:1,one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9,ten:10};
 if(t==='today'||t==='tonight')return d;if(t==='tomorrow'||t==='tmr')return add(1);
 let m=/^in (\d{1,3}|a|an|one|two|three|four|five|six|seven|eight|nine|ten) (day|week|month)s?$/.exec(t);
 if(m){const n=NUM[m[1]]||+m[1];if(m[2]==='month'){d.setMonth(d.getMonth()+n);return d}return add(m[2]==='week'?7*n:n)}
 if(t==='next week')return add(((8-d.getDay())%7)||7);
 if(t==='end of week'||t==='eow'||t==='this week')return add((5-d.getDay()+7)%7);
 if(t==='end of month'||t==='eom')return new Date(d.getFullYear(),d.getMonth()+1,0);
 m=/^(this |next )?(sun|mon|tue|wed|thu|fri|sat)[a-z]*$/.exec(t);
 if(m)return add((DAYS.indexOf(m[2])-d.getDay()+7)%7||7);
 m=/^(?:(sun|mon|tue|wed|thu|fri|sat)[a-z]* next week|next week (?:on )?(sun|mon|tue|wed|thu|fri|sat)[a-z]*)$/.exec(t);
 if(m){add(((8-d.getDay())%7)||7);return add((DAYS.indexOf(m[1]||m[2])+6)%7)}
 m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(t);if(m){const x=new Date(+m[1],+m[2]-1,+m[3]);return x.getMonth()===+m[2]-1?x:null}
 const dm=(day,mon)=>{if(mon<0||day<1||day>31)return null;let x=new Date(d.getFullYear(),mon,day);if(x.getMonth()!==mon)return null;if(x<d)x=new Date(d.getFullYear()+1,mon,day);return x};
 m=/^(\d{1,2})(?:st|nd|rd|th|e|er|\.)? (?:of |de )?([a-z]{3})[a-z]*$/.exec(t);if(m)return dm(+m[1],MONTHS.indexOf(m[2]));
 m=/^([a-z]{3})[a-z]* (\d{1,2})(?:st|nd|rd|th)?$/.exec(t);if(m)return dm(+m[2],MONTHS.indexOf(m[1]));
 m=/^(\d{1,2})[/.](\d{1,2})$/.exec(t);if(m)return dm(+m[1],+m[2]-1);
 return null}
const ncISO=d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
// The moment with its offset, for due_at: 2026-10-27T15:00:00+01:00
const ncAt=d=>{const o=-d.getTimezoneOffset(),p=n=>String(Math.floor(Math.abs(n))).padStart(2,'0');return ncISO(d)+'T'+p(d.getHours())+':'+p(d.getMinutes())+':00'+(o<0?'-':'+')+p(o/60)+':'+p(o%60)};
const ncRead=d=>d.toLocaleDateString(DL,{weekday:'short',day:'numeric',month:'short'})+(d.timed?' '+fmtHM(d):'');
function ncDialog(){let d=$('#new-card');if(d)return d;d=document.createElement('dialog');d.id='new-card';d.setAttribute('aria-labelledby','new-card-title');
 d.innerHTML=`<form method="dialog"><div class="snooze-heading"><h2 id="new-card-title">New to-do</h2><button aria-label="Close">×</button></div></form><p class="nc-drop-hint">Drop to add to the to-do</p><div class="chat-tray nc-tray" id="nc-tray" hidden></div><div class="chat-box"><button type="button" class="chat-attach" id="nc-attach" aria-label="Add files" title="Add files">${CLIP}</button><input type="file" id="nc-file" multiple hidden accept="${CHAT_ACCEPT}"><textarea id="nc-text" rows="2" aria-label="${esc(t('What needs doing?'))}" placeholder="${esc(t('What needs doing?'))}" maxlength="2000" enterkeyhint="done"></textarea><div class="chat-tools">${micBtn()}<button type="button" class="chat-send" id="nc-add" aria-label="Add the to-do" title="Add the to-do" disabled>${SEND}</button></div></div><div class="nc-chips" id="nc-chips" role="group" aria-label="Optional"></div><div class="nc-pick" id="nc-pick" hidden></div><p class="nc-error" id="nc-error" role="alert"></p><p class="nc-foot"><span>Nothing is sent. I’ll fill in the rest.</span><span class="nc-keys">Enter adds it</span></p>`;
 document.body.append(d);
 const text=$('#nc-text');text.addEventListener('input',()=>{ncReady();text.style.height='auto';text.style.height=Math.min(200,Math.max(44,text.scrollHeight))+'px'});
 text.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();ncCreate()}});
 $('#nc-add').onclick=ncCreate;
 // Files: the paperclip (on a phone also the camera), a pasted screenshot, or a drop on the form
 $('#nc-attach').onclick=()=>$('#nc-file').click();
 $('#nc-file').addEventListener('change',e=>{ncAddFiles([...e.target.files]);e.target.value=''});
 text.addEventListener('paste',e=>{const files=[...(e.clipboardData?.files||[])];if(!files.length||e.clipboardData.getData('text/plain'))return;e.preventDefault();ncAddFiles(files)});
 $('#nc-tray').addEventListener('click',e=>{const x=e.target.closest('[data-nc-remove]');if(!x)return;const f=nc.files.find(v=>v.key===x.dataset.ncRemove);nc.files=nc.files.filter(v=>v!==f);ncForget([f]);ncTray();text.focus()});
 {let depth=0;const files=e=>[...(e.dataTransfer?.types||[])].includes('Files');
  d.addEventListener('dragenter',e=>{if(!files(e))return;e.preventDefault();depth++;d.classList.add('nc-drop')});
  d.addEventListener('dragover',e=>{if(!files(e))return;e.preventDefault();e.dataTransfer.dropEffect='copy'});
  d.addEventListener('dragleave',e=>{if(!files(e))return;if(--depth<=0){depth=0;d.classList.remove('nc-drop')}});
  d.addEventListener('drop',e=>{if(!files(e))return;e.preventDefault();depth=0;d.classList.remove('nc-drop');ncAddFiles([...e.dataTransfer.files])})}
 $('#nc-chips').addEventListener('click',e=>{const x=e.target.closest('[data-nc-drop]');if(x){const[k,i]=x.dataset.ncDrop.split(':');if(k==='due')nc.due=null;else nc[k].splice(+i,1);ncChips();return}
  const b=e.target.closest('[data-nc]');if(!b)return;const k=b.dataset.nc;
  if(k==='work'||k==='personal'){nc.scope=nc.scope===k?null:k;ncChips();return}ncPick(nc.pick===k?null:k)});
 $('#nc-pick').addEventListener('click',e=>{const h=e.target.closest('[data-nc-hit]');if(h)ncChoose(+h.dataset.ncHit)});
 d.addEventListener('close',()=>{ncPick(null);ncForget(nc.files);nc.files=[];ncTray();if(nc.byPointer)setTimeout(()=>document.activeElement?.closest?.('[data-new-card]')&&document.activeElement.blur())});
 return d}
function ncChips(){const due=nc.due?`<button type="button" class="set" data-nc="due">Due ${esc(ncRead(nc.due))}<span class="x" data-nc-drop="due:0" aria-label="Remove the due date">×</span></button>`:`<button type="button" data-nc="due" aria-expanded="${nc.pick==='due'}">Due</button>`;
 const set=(k,list,label)=>list.map((x,i)=>`<button type="button" class="set" data-nc="${k}">${esc(label(x))}<span class="x" data-nc-drop="${k}:${i}" aria-label="Remove">×</span></button>`).join('');
 $('#nc-chips').innerHTML=[['work','Work'],['personal','Personal']].map(([k,t])=>`<button type="button" data-nc="${k}" aria-pressed="${nc.scope===k}">${t}</button>`).join('')+due
  +set('about',nc.about,x=>x.name)+(nc.about.length<5?`<button type="button" data-nc="about" aria-expanded="${nc.pick==='about'}">Person</button>`:'')
  +set('attach',nc.attach,x=>x.title||'Email')+(nc.attach.length<5?`<button type="button" data-nc="attach" aria-expanded="${nc.pick==='attach'}" title="Attach an email this to-do is about" aria-label="Attach an email"><svg class="nc-ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5.5" width="18" height="13" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="m3.5 7.5 8.5 6 8.5-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>Email</button>`:'')}
const NC_PICK={due:['When is it due?','Friday, 15:00, in 2 hours, tomorrow 9'],about:['Link a person','A name or a company'],attach:['Attach an email','Search by subject or sender']};
// The calendar icon's quick picks, like Snooze's: a time today or a morning, or a day from the date picker.
const NC_QUICK=[['2h','2 hours'],['tomorrow','Tomorrow · 9:00'],['3d','3 days · 9:00'],['1w','1 week · 9:00']];
const ncQuick=(q,now=new Date())=>{if(q==='2h'){const x=new Date(+now+2*36e5);x.timed=true;return x}const x=new Date(now.getFullYear(),now.getMonth(),now.getDate()+({tomorrow:1,'3d':3,'1w':7})[q],9,0);x.timed=true;return x};
function ncPick(k){nc.pick=k;nc.hits=[];const box=$('#nc-pick');if(!box)return;ncChips();if(!k){box.hidden=true;box.innerHTML='';return}
 box.hidden=false;box.innerHTML=`${k==='due'?'<div class="nc-due-row">':''}<input id="nc-find" type="search" autocomplete="off" aria-label="${NC_PICK[k][0]}" placeholder="${NC_PICK[k][1]}">${k==='due'?`<button type="button" class="nc-cal" id="nc-cal" title="Quick picks" aria-label="Quick picks" aria-expanded="false" aria-controls="nc-quick"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M4 6.5h16v13H4zM4 10.5h16M8.5 3.5v5M15.5 3.5v5"/></svg></button></div><div class="nc-quick" id="nc-quick" role="group" aria-label="Quick picks" hidden>${NC_QUICK.map(([q,t])=>`<button type="button" data-nc-quick="${q}">${t}</button>`).join('')}<label class="nc-date-pick">Choose date<input id="nc-date" type="date" min="${ncISO(new Date())}" aria-label="Choose date"></label></div>`:''}<p class="nc-read" id="nc-read" aria-live="polite"></p><ul class="nc-hits" id="nc-hits"></ul>`;
 const f=$('#nc-find');f.focus();
 if(k==='due'){const cal=$('#nc-date'),quick=$('#nc-quick'),icon=$('#nc-cal');icon.addEventListener('click',()=>{quick.hidden=!quick.hidden;icon.setAttribute('aria-expanded',String(!quick.hidden));if(!quick.hidden)quick.querySelector('button')?.focus()});
  quick.addEventListener('click',e=>{const q=e.target.closest('[data-nc-quick]');if(q){nc.due=ncQuick(q.dataset.ncQuick);ncPick(null);$('#nc-text').focus()}});
  cal.addEventListener('click',()=>{try{cal.showPicker?.()}catch{}});cal.addEventListener('change',()=>{const m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(cal.value);if(m){nc.due=new Date(+m[1],+m[2]-1,+m[3]);ncPick(null);$('#nc-text').focus()}});
  $('#nc-read').addEventListener('click',e=>{const d=e.target.closest('[data-nc-set]')&&ncDue(f.value);if(d){nc.due=d;ncPick(null);$('#nc-text').focus()}})}
 f.addEventListener('input',()=>{if(k==='due'){const d=ncDue(f.value);$('#nc-read').innerHTML=f.value.trim()?d?`<button type="button" class="link" data-nc-set>Due ${esc(ncRead(d))}</button> <small>Enter sets it</small>`:'I can’t read that yet. Try 15:00, in 2 hours or Friday.':'';return}clearTimeout(nc.timer);nc.timer=setTimeout(()=>ncSearch(k,f.value),200)});
 f.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();e.stopPropagation();ncPick(null);$('#nc-text').focus();return}
  if(e.key!=='Enter'||e.isComposing)return;e.preventDefault();if(k==='due'){const d=ncDue(f.value);if(d){nc.due=d;ncPick(null);$('#nc-text').focus()}}else if(nc.hits.length)ncChoose(0)})}
async function ncSearch(k,q){q=q.trim();const list=$('#nc-hits');if(!list)return;if(q.length<2){nc.hits=[];list.innerHTML='';return}
 try{if(k==='about'){const r=await request('api/graph?q='+encodeURIComponent(q));nc.hits=(r.found||[]).filter(n=>['person','org','project'].includes(n.kind)&&!nc.about.some(a=>a.id===n.id)).slice(0,6).map(n=>({id:n.id,name:n.name,note:n.kind==='person'?(n.ids||[])[0]||'':n.kind==='org'?n.domain||'Organization':'Project'}))}
  else{const r=await request('api/events?account=all&kind=email&q='+encodeURIComponent(q));nc.hits=(Array.isArray(r)?r:[]).filter(e=>!nc.attach.some(a=>a.id===e.id)).slice(0,6).map(e=>({id:e.id,title:e.title||'(no subject)',note:e.metadata?.from||''}))}}
 catch(e){nc.hits=[]}
 if(nc.pick!==k||$('#nc-find')?.value.trim()!==q)return;
 list.innerHTML=nc.hits.length?nc.hits.map((h,i)=>`<li><button type="button" data-nc-hit="${i}">${esc(h.name||h.title)}${h.note?`<small>${esc(String(h.note).replace(/<[^>]*>/g,'').trim())}</small>`:''}</button></li>`).join(''):`<li class="nc-read">${k==='about'?'Nobody by that name.':'No emails match.'}</li>`}
function ncChoose(i){const h=nc.hits[i];if(!h)return;if(nc.pick==='about')nc.about.push({id:h.id,name:h.name});else nc.attach.push({id:h.id,title:h.title});ncPick(null);$('#nc-text').focus()}
// The sheet sits on the phone's keyboard: the keyboard's height, from the visual viewport.
function ncKeyboard(){const v=window.visualViewport;if(!v)return;for(const d of document.querySelectorAll('#new-card,#help-panel'))d.style.setProperty('--nc-kb',(d.open?Math.max(0,Math.round(innerHeight-v.height-v.offsetTop)):0)+'px')}  // and Help's
window.visualViewport?.addEventListener('resize',ncKeyboard);window.visualViewport?.addEventListener('scroll',ncKeyboard);
function ncOpen(o={}){const d=ncDialog();if(d.open)return;Object.assign(nc,{scope:scopeFilter==='work'||scopeFilter==='personal'?scopeFilter:null,due:null,about:o.about||[],attach:[],files:[],
  draft:[...crypto.getRandomValues(new Uint8Array(8))].map(b=>b.toString(16).padStart(2,'0')).join(''),pick:null,busy:false,byPointer:false});
 const t=$('#nc-text');t.value='';t.style.height='';$('#nc-add').disabled=true;$('#nc-error').textContent='';ncTray();ncPick(null);d.showModal();t.focus();ncKeyboard()}
async function ncCreate(){const text=$('#nc-text').value.trim();if(!text||nc.busy||nc.files.some(f=>f.state==='up'))return;if(nc.pick==='due'){const d=ncDue($('#nc-find')?.value);if(d)nc.due=d}nc.busy=true;$('#nc-add').disabled=true;$('#nc-error').textContent='';
 try{const made=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'card_new',args:{text,scope:nc.scope,due:nc.due?ncISO(nc.due):null,due_at:nc.due?.timed?ncAt(nc.due):null,about:nc.about.map(a=>a.id),attach:nc.attach.map(a=>a.id),...(nc.files.length?{draft:nc.draft,files:nc.files.map(f=>f.id)}:{})}})});
  nc.files=[];$('#new-card').close();toast('Added');if(chatId)chatGo(made.id);else{showTab('inbox');history.replaceState(null,'',location.pathname+location.search+'#card='+made.id)}await refresh()}
 catch(e){errCaught(e);$('#nc-error').textContent=e.message||'Couldn’t add the to-do'}finally{nc.busy=false;ncReady()}}
// New to-do's files (chat_files.py, as in the chat): each uploads at once under the form's draft key, and the to-do
// takes them when it is added. Closed without adding, they are taken back (and would go after a day anyway).
function ncReady(){const b=$('#nc-add');if(b)b.disabled=nc.busy||!$('#nc-text')?.value.trim()||nc.files.some(f=>f.state==='up')}
function ncTray(){const t=$('#nc-tray');if(t){t.innerHTML=chatTrayHTML(nc.files,'nc-remove');t.hidden=!nc.files.length}ncReady()}
function ncForget(list){for(const f of list)if(f?.id)request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'chat_file_remove',args:{draft:f.draft,id:f.id}})}).catch(()=>{})}
function ncAddFiles(list){const problems=[],draft=nc.draft;$('#nc-error').textContent='';
 for(const f of list){const name=chatFileName(f),img=CHAT_IMAGE.test(name);
  if(nc.files.length>=CHAT_LIMIT.count){problems.push(t('A to-do can carry up to {} files.',CHAT_LIMIT.count));break}
  const why=chatFileProblem(f,name);if(why){problems.push(why);continue}
  const item={key:crypto.randomUUID(),name,size:f.size,type:img?(f.type||'image/png'):(f.type||'file'),url:'',state:'up',draft};nc.files.push(item);
  (async()=>{try{const url=await chatDataUrl(f);if(img){item.url=url;ncTray()}
    const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf,'X-Upload':'chat-file'},body:JSON.stringify({action:'chat_upload',args:{draft,name,data:url.split(',')[1]||''}})});
    item.id=r.id;if(!nc.files.includes(item)){ncForget([item]);return}Object.assign(item,{name:r.name,type:r.type,state:'ok'})}
   catch(err){errCaught(err);nc.files=nc.files.filter(x=>x!==item);$('#nc-error').textContent=`${name}: ${(I18N.cat&&i18nLookup(err.message))||err.message}`}ncTray()})()}
 if(problems.length)$('#nc-error').textContent=problems.join(' ');ncTray();$('#nc-text')?.focus()}
// Entry points: a row under Find a to-do on a computer, "+" in the top bar on a phone, C, and the palette (Ctrl/⌘K) then "new".
{const row=document.createElement('button');row.type='button';row.className='side-new';row.id='side-new';row.dataset.newCard='';row.title='New to-do (N)';row.setAttribute('aria-label','New to-do');
 row.innerHTML=`${NC_PLUS}<span>New to-do</span><kbd>N</kbd>`;$('#side-search').after(row);
 // Talk: the main live conversation, through what needs the owner (shows once this Machine can talk live)
 const talkRow=document.createElement('button');talkRow.type='button';talkRow.className='side-new side-talk';talkRow.id='side-talk';talkRow.dataset.talkMain='';talkRow.hidden=true;
 talkRow.title='Talk (T)';talkRow.setAttribute('aria-label','Talk');talkRow.setAttribute('aria-pressed','false');talkRow.innerHTML=`${WAVE}<span>Talk</span><kbd>T</kbd>`;row.after(talkRow);
 const plus=document.createElement('button');plus.type='button';plus.className='head-link settings-link new-card-link';plus.id='new-card-top';plus.dataset.newMenu='';plus.title='New';plus.setAttribute('aria-label','New');plus.setAttribute('aria-haspopup','menu');plus.setAttribute('aria-expanded','false');
 // With the phone drawer (#topbar), the sidebar row shows in the drawer and the "+" sits on the right of the top bar.
 const top=$('#topbar');if(top){plus.className='topbar-menu new-card-top';plus.innerHTML=NC_PLUS;top.append(plus);document.documentElement.classList.add('nc-drawer')}
 else{plus.innerHTML=`${NC_PLUS}<span class="lbl">New</span>`;$('#open-settings').before(plus)}}
document.addEventListener('click',e=>{if(e.target.closest('[data-new-card]')){e.preventDefault();if(typeof drawerClose==='function')drawerClose();ncOpen();nc.byPointer=e.detail>0}});
// "+" in the top bar: what to make. A card, a person, an organization, a project or an event (first on the Calendar).
const NEW_WHAT=[['card','New to-do'],['person','New person'],['org','New organization'],['project','New project']];
const newWhatList=()=>$('#calendar')?.hidden===false?[['event','New event'],...NEW_WHAT]:[...NEW_WHAT,['event','New event']];
function newMenu(open){const b=$('#new-card-top');let m=$('#new-menu');if(!open){if(m&&!m.hidden){m.hidden=true;b?.setAttribute('aria-expanded','false')}return}
 if(!m){m=document.createElement('div');m.id='new-menu';m.className='fact-menu-list new-menu';m.setAttribute('role','menu');m.setAttribute('aria-label','New');document.body.append(m)}
 m.innerHTML=newWhatList().map(([k,t])=>`<button type="button" role="menuitem" data-new-what="${k}">${t}</button>`).join('');
 const r=b.getBoundingClientRect();m.style.top=Math.round(r.bottom+6)+'px';m.style.right=Math.max(8,Math.round(innerWidth-r.right))+'px';m.hidden=false;b.setAttribute('aria-expanded','true');m.querySelector('button').focus({preventScroll:true})}
const newWhat=(k,byPointer)=>{if(k==='card'){ncOpen();nc.byPointer=byPointer}else if(k==='event')calNew();else if(k==='project')pjOpen({});else recOpen(k)};
document.addEventListener('click',e=>{const plus=e.target.closest('[data-new-menu]');if(plus){e.preventDefault();newMenu($('#new-menu')?.hidden!==false);return}
 const w=e.target.closest('[data-new-what]');if(w){newMenu(false);if(typeof drawerClose==='function')drawerClose();newWhat(w.dataset.newWhat,e.detail>0);return}
 if(!e.target.closest('#new-menu'))newMenu(false)});
document.addEventListener('keydown',e=>{const m=$('#new-menu');if(!m||m.hidden)return;if(e.key==='Escape'){e.preventDefault();newMenu(false);$('#new-card-top')?.focus();return}
 if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const all=[...m.querySelectorAll('button')],i=all.indexOf(document.activeElement);all[(i+(e.key==='ArrowDown'?1:all.length-1))%all.length].focus()}});
addEventListener('resize',()=>newMenu(false));
const ncTyping=t=>t?.closest?.('input,textarea,select,[contenteditable=""],[contenteditable="true"],dialog[open]');
// C, Ctrl/⌘K and the other keys: the action registry and the palette at the end of this script.
const ncAsked=()=>{const q=$('#side-find').value.trim().toLowerCase();return q.length>=2&&(q==='+'||('new to-do'.startsWith(q)||'new card'.startsWith(q)))};
