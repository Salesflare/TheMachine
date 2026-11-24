// A lazy part (dashboard_parts.LAZY 'sendlater'): Send later. The Snooze picker picks when an approved message goes (the
// send dialog's Send later, go: its Send with that time), and Change time, Cancel and Send now act on one that waits
// (s.send_later). The Machine holds it and checks for a reply right before it goes (machine/store/send_later.py).
function laterPick(at,go){const d=$('#snooze-dialog'),title=$('#snooze-title'),quick=$('.snooze-presets'),was=[...quick.childNodes],name=title.textContent;
 const day=n=>new Date(new Date().setDate(new Date().getDate()+n)),on=(x,label)=>{const [h,m]=(state.hours?.morning||'09:00').split(':');x.setHours(+h,+m,0,0);return [x,label+' · '+fmtHM(x)]};
 const monday=(8-new Date().getDay())%7||7,times=[[new Date(Date.now()+72e5),t('In 2 hours')],on(day(1),t('Tomorrow')),...(monday>1?[on(day(monday),localeDate(day(monday),DL,{weekday:'long'}))]:[])];
 toastNotAbout('');setHTML(quick,html`${times.map(([x,label])=>html`<button type="button" data-snooze="${x.toISOString()}">${label}</button>`)}`);
 title.textContent=t(at?'Change time':'Send later');
 const note=make('p',{id:'later-note'},t('If they write first, it waits for you. If The Machine is off then, it goes when it’s back, up to an hour late. After that it asks.'));
 $('#snooze-error').before(note);
 snoozePick=async pick=>{try{const x=pick||snoozeAt();if(!x)return;if(Date.parse(x)<=Date.now())throw Error(t('Choose a time that hasn’t passed.'));d.close();await go(x)}catch(e){errCaught(e);$('#snooze-error').textContent=e.message}};
 // The picker is Snooze's again once it closes
 d.addEventListener('close',()=>{snoozePick=null;note.remove();title.textContent=name;quick.replaceChildren(...was)},{once:true});
 snoozeShow(at,!!at);if(at){const x=new Date(at);$('#snooze-time').value=[x.getHours(),x.getMinutes()].map(n=>String(n).padStart(2,'0')).join(':')}}
async function laterAct(choice,id){const s=state.suggestions.find(x=>x.id===id),w=s?.send_later;if(!w)return;
 const post=async(go,said)=>{try{await go();said();await refresh()}
  catch(e){errCaught(e);toast(e.message,true);refresh().catch(()=>{})}};
 if(choice==='send-time')return laterPick(w.send_at,later=>post(()=>fleetPost('send_later_move',{suggestion_id:id,later}),()=>toast(t('Sends {}.',chatUntil(later)))));
 if(choice==='send-cancel')return post(()=>fleetPost('send_later_cancel',{suggestion_id:id}),()=>toastOpen(t('Canceled. The draft waits in the to-do.'),id));
 await post(()=>fleetPost('send_later_now',{suggestion_id:id}),()=>{toast(t(w.n>1?'Sending your {} approved drafts…':'Sending your approved draft…',w.n));const a=taskActions(s).find(x=>w.revisions.includes(x.revision));if(a)sentWatch.set(id,{revision:a.revision,kind:a.kind,at:Date.now()})})}
