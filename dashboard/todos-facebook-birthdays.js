// The Import birthdays from Facebook to-do (birthdays_facebook_app.py, lazy). Import, then Save (birthdays and pictures,
// marks it done; saved people link to their pages). Signed out: the sign-in dialog, then a read.
const fbDay=v=>{const m=/^(?:(\d{4})|-)-(\d{2})-(\d{2})$/.exec(v||'');if(!m)return v||'';const d=new Date(Date.UTC(+(m[1]||2000),+m[2]-1,+m[3]));
 return new Intl.DateTimeFormat(DL,{month:'long',day:'numeric',...(m[1]?{year:'numeric'}:{}),timeZone:'UTC'}).format(d)};
const fbMonth=m=>new Date(2000,m-1,9).toLocaleString(DL,{month:'long'});
const fbPerson=p=>html`<a class="link" href="#graph/${encodeURIComponent(p.id)}" translate="no">${p.name}</a>`;
const fbN=n=>(+n||0).toLocaleString(DL);
const fbFine=x=>html`<p class="fine cl-fine">${x}</p>`;
const fbActs=x=>html`<p class="cl-acts">${x}</p>`;
const fbPics=n=>t(['Added {} profile picture.','Added {} profile pictures.'],fbN(n));
const fbDone=r=>r.saved||!r.photos?t(['Saved {} birthday.','Saved {} birthdays.'],fbN(r.saved)):fbPics(r.photos);
const fbBtn=(s,step,label,primary)=>html`<button type="button" class="${primary?'primary':'ghost'}" data-fb-step="${step}" data-fb-id="${s.id}">${label}</button>`;
function fbBirthdaysBox(s){const f=s.facebook_birthdays,open=!closed(s),o=f.others||f.added?lazyIn('fbpeople')?fbOthers(s,f,!f.new&&!f.photos):(lazyRun('fbpeople',render),''):'';
 if(f.state==='reading'){fbPoll();return html`<p class="cl-lead">${t('Reading Facebook’s birthdays page…')}</p><div class="send-progress" aria-hidden="true"><i></i></div>`}
 if(f.state==='preview'){const list=f.shown.map(m=>html`<li class="cl-row"><div class="cl-what"><b>${m.id?fbPerson(m):m.name}</b></div><span class="cl-end">${fbDay(m.date)}</span></li>`);
  return html`<p class="cl-lead">${t(['Found {} birthday on Facebook.','Found {} birthdays on Facebook.'],fbN(f.found))}</p>${f.capped?fbFine(t('The page was very long, so the import stopped before the end.')):''}${f.missing?.length?fbFine(t('These months didn’t load: {}.',f.missing.map(fbMonth).join(', '))):''}
  ${f.matched?html`${fbFine(t(['{} is already in your Graph.','{} are already in your Graph.'],fbN(f.matched)))}${f.new<f.matched&&f.new?fbFine(t('{} of them already have a birthday.',fbN(f.matched-f.new))):''}${list[0]?html`<ul class="cl-list">${list}</ul>`:''}${f.more?fbFine(t('And {} more.',fbN(f.more))):''}`:''}
  ${f.ambiguous[0]?fbFine(t('Skipped, more than one person with this name: {}.',f.ambiguous.join(', '))):''}
  ${f.new?'':f.matched?fbFine(t('Your Graph already has these birthdays.')):o?'':fbFine(t('None of them are in your Graph yet, so there’s nothing to save.'))}${f.photos?fbFine(t(['{} of them has no photo yet: Save adds their Facebook picture.','{} of them have no photo yet: Save adds their Facebook pictures.'],fbN(f.photos))):''}
  ${open&&(f.new||f.photos)?fbActs(fbBtn(s,'save',f.new?t(['Save {} birthday','Save {} birthdays'],fbN(f.new)):t(['Save {} picture','Save {} pictures'],fbN(f.photos)),true)):''}${o}${open?fbActs(fbBtn(s,'read',t('Import again'))):''}`}
 if(f.state==='saved')return html`<p class="cl-lead">${fbDone(f)}</p>${f.saved&&f.photos?fbFine(fbPics(f.photos)):''}${f.people?.length?fbFine(f.people.map((p,i)=>html`${i?', ':''}${fbPerson(p)}`)):''}${f.more?fbFine(t('And {} more.',fbN(f.more))):''}${o}${open?fbActs(fbBtn(s,'read',t('Import again'))):''}`;
 if(f.state==='signed_out')return html`<p class="cl-lead">${t('The Machine’s browser isn’t signed in to Facebook.')}</p>${open?fbActs(html`${fbBtn(s,'signin',t('Sign in to {}','Facebook'),true)}${fbBtn(s,'read',t('Try again'))}`):''}`;
 if(f.state==='failed')return html`<p class="cl-lead">${f.empty?t('No birthdays found on the page.'):t('Couldn’t read the page.')}</p>${open?fbActs(html`${fbBtn(s,'read',t('Try again'),true)}`):''}`;
 return html`<p class="cl-lead">${t('Reads the birthdays on Facebook’s birthdays page once, in The Machine’s browser. Nothing is saved before you say so.')}</p>${open?fbActs(html`${fbBtn(s,'read',t('Import'),true)}`):''}`}
function fbPoll(){if(fbPoll.t)return;fbPoll.t=setTimeout(async()=>{fbPoll.t=0;try{await refresh(true)}catch(err){errCaught(err)}},3000)}
async function fbStep(id,step){const r=await connectPost('birthdays_facebook',{suggestion_id:id,step});
 if(r?.state==='saved'){toast(fbDone(r));if(r.people?.length===1)$('#toast').append(' ',make('button',{type:'button','data-fb-person':r.people[0].id},r.people[0].name))}await refresh()}
async function fbSignin(id){await connectPost('connect_site_signin',{site:'facebook'});
 openSignin(null,true,null,null,'facebook',()=>fbStep(id,'read').catch(err=>{errCaught(err);toast(err.message,true)}))}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-fb-step]');if(!b)return;e.preventDefault();const id=b.dataset.fbId,s=(state.suggestions||[]).find(x=>x.id===id);if(!s?.facebook_birthdays)return;
 b.disabled=true;try{if(b.dataset.fbStep==='signin'){await fbSignin(id);b.disabled=false}else await fbStep(id,b.dataset.fbStep)}
 catch(err){errCaught(err);toast(err.message,true);b.disabled=false}});
$('#toast').addEventListener('click',e=>{const b=e.target.closest('[data-fb-person]');if(b)location.hash='#graph/'+encodeURIComponent(b.dataset.fbPerson)});
