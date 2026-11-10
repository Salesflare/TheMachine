// Lazy part 'fbpeople' (dashboard_parts.LAZY), drawn by the Import birthdays from Facebook to-do (todos-facebook-birthdays.js):
// the friends nobody in the Graph has. How many, a few names, and Add … as personal contacts (birthdays_facebook.add:
// Personal, with their birthday), also after Save. Then how many it added, with Undo here and on the toast (birthdays_facebook.remove).
const fbAdded=n=>t(['Added {} personal contact.','Added {} personal contacts.'],fbN(n));
// {line, btn, note}: main makes Add the main button (the preview has no Save). Once added, Undo takes its place.
const fbpBtn=(s,step,label,main)=>html`<button type="button" class="${main?'primary':'ghost'}" data-fbp="${step}" data-fb-id="${s.id}">${label}</button>`;
function fbOthers(s,f,main){
 if(f.added)return {line:fbFine(fbAdded(f.added)),btn:fbpBtn(s,'undo_add',t('Undo'))};
 const left=f.others-f.others_shown.length,names=f.others_shown.join(', ');
 return {line:html`${f.matched||f.saved?fbFine(t(['{} Facebook friend isn’t in your Graph yet.','{} Facebook friends aren’t in your Graph yet.'],fbN(f.others))):''}${fbFine(html`<span translate="no">${left?t('{} and {} more',names,fbN(left)):names}</span>`)}`,
  btn:fbpBtn(s,'add',t(['Add {} as a personal contact','Add {} as personal contacts'],fbN(f.others)),main),note:fbFine(t('With their birthday. Reminders only come for people you write to.'))}}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-fbp]');if(!b)return;e.preventDefault();b.disabled=true;
 try{const r=await connectPost('birthdays_facebook',{suggestion_id:b.dataset.fbId,step:b.dataset.fbp});
  if(r?.added!=null){toast(fbAdded(r.added));if(r.added)$('#toast').append(' ',make('button',{type:'button','data-fbp':'undo_add','data-fb-id':b.dataset.fbId},t('Undo')));clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),15000)}else toast(t('Undone.'));
  await refresh()}
 catch(err){errCaught(err);toast(err.message,true);b.disabled=false}});
