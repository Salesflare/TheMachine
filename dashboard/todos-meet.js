// Scheduling between Machines (meet.py, meet_app.py): a time two Machines agreed shows on the to-do with Book it,
// Other time and Not needed; the invite goes out only once both owners tapped Book it. The setting sits in the Network pane.
// No Machine there (meet_link.py): the email draft carries a booking link, and a time picked on it is a to-do with
// Book it and Not needed (role link, state picked).
const meetOpen=s=>!!s.meet&&(s.meet.state==='proposed'||s.meet.state==='picked')&&!closed(s)&&s.status!=='snoozed';
const LINK_LINES={open:'Booking link in the email draft. {} can pick a time.',picked:'{} picked a time on the booking link.',booked:'Booked through the booking link.',closed:'The booking link ended.',expired:'The booking link ended.'};
function meetBlock(s){const m=s.meet;if(!m||closed(s)&&m.state!=='booked')return'';const who=(m.name||'');
 let line='';
 if(m.state==='asked')line=t('Asking {}’s Machine for a time that suits you both.',m.name);
 else if(m.state==='waiting')line=t('Asked {}’s Machine for another time.',m.name);
 else if(m.state==='link')line=t(LINK_LINES[m.link_state]||LINK_LINES.closed,m.name);
 else if(m.state==='picked')line=m.note==='failed'?t('The booking didn’t go through. Tap Book it to try again.'):t('Nothing is booked until you tap Book it.');
 else if(m.state==='booked')line=m.role!=='answerer'?t('Booked {}. The invite went to {}.',m.when,m.name):t('Booked {} by {}.',m.when,m.name);
 else if(m.state==='proposed'){
  line=m.note==='failed'?t('The booking didn’t go through. Tap Book it to try again.'):m.mine_ok?t('Waiting for {} to tap Book it.',m.name):m.their_ok?t('{} tapped Book it. The invite goes out when you do too.',m.name):t('Free for you both. The invite goes out once you both tap Book it.')}
 if(!line)return'';
 return html`<p class="note meet-line" data-meet-state="${m.state}">${(m.state==='proposed'||m.state==='picked')&&m.when?html`<b>${m.when}</b> · ${t('{} min',m.minutes)}${m.video?` · ${m.video}?`:''}<br>`:''}${line}</p>`}
function meetActions(s){const id=s.id,m=s.meet;
 return html`<div class="actions">${m.mine_ok?'':html`<button class="primary" data-meet-do="book" data-meet-id="${id}">Book it</button>`}${m.role==='link'?'':html`<button class="ghost" data-meet-do="other" data-meet-id="${id}">Other time</button>`}<button class="quiet" data-meet-do="skip" data-meet-id="${id}"${m.role==='link'?html` data-meet-link="1"`:''}>Not needed</button></div>`}
function meetSetting(m){if(!m)return'';
 const opt=(key,value,label)=>html`<option value="${value}"${String(m[key])===String(value)?html` selected`:''}>${label}</option>`;
 const sel=(key,label,options)=>html`<label class="meet-pref"><span>${label}</span><select data-meet-pref="${key}"${key!=='allow'&&key!=='brand'&&m.allow==='off'?html` disabled`:''}>${options}</select></label>`;
 return html`<div class="meet-setting"><h3>Scheduling with other Machines</h3><p class="muted">When someone with a Machine asks to meet, your Machines find a time. Only free or busy is shared, and nothing is booked until you both tap Book it. <a class="learn" href="${HELP}friends#scheduling-with-other-machines" target="_blank" rel="noopener">Learn more</a></p><div class="meet-prefs">${
  sel('allow','What other Machines may ask mine',[opt('allow','freebusy','Free/busy for scheduling'),opt('allow','off','Off')])}${
  sel('minutes','Meeting length',[15,30,45,60,90].map(n=>opt('minutes',n,t('{} min',n))))}${
  sel('buffer','Buffer',[0,5,10,15,30].map(n=>opt('buffer',n,n?t('{} min',n):'None')))}${
  sel('prefer','Preferred times',[opt('prefer','any','Any time'),opt('prefer','morning','Mornings'),opt('prefer','afternoon','Afternoons')])}${
  sel('brand','Footer on booking links',[opt('brand',true,'On'),opt('brand',false,'Off')])}</div></div>`}
$('#suggestions').addEventListener('click',async e=>{const b=e.target.closest('[data-meet-do]');if(!b)return;b.disabled=true;
 try{const r=await fleetPost('meet_decide',{suggestion_id:b.dataset.meetId,choice:b.dataset.meetDo});
  toast(b.dataset.meetDo==='skip'?(b.dataset.meetLink?'Closed. The booking link is off.':'Closed. Their Machine is told.'):b.dataset.meetDo==='other'?'Looking for another time.':r?.state==='booked'?'Booked. The invite is on its way.':'Done. Waiting for them to tap Book it.');await refresh()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
$('#fleet-view').addEventListener('change',async e=>{const el=e.target.closest('[data-meet-pref]');if(!el)return;el.disabled=true;
 const key=el.dataset.meetPref,value=key==='minutes'||key==='buffer'?Number(el.value):key==='brand'?el.value==='true':el.value;
 try{await fleetPost('meet_setting',{[key]:value});toast(key==='allow'?(value==='off'?'Off. Other Machines can’t ask yours.':'On. Machines of people you email can ask for free times.'):'Saved.');await fleetView()}catch(err){errCaught(err);toast(err.message,true);await fleetView()}finally{el.disabled=false}});
