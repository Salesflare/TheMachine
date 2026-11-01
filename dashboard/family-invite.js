// Inviting family at the right moment (family_invites.py): a quiet line on a family to-do with someone not in the
// owner's Family yet. Invite opens the account page's invite form, prefilled; the owner sends it there. Not now hides it
// for 90 days. Settings, Fleet: Suggest inviting family turns these off.
const familyInviteNote=s=>{const f=!closed(s)&&s.family_invite;if(!f)return '';
 return `<p class="note family-invite">${esc(f.question)} ${esc(f.line)} <a class="link" href="${esc(f.url)}" target="_blank" rel="noopener" data-family-invite="open" data-card="${esc(s.id)}">${esc(t('Invite'))}</a> <button type="button" class="link" data-family-invite="later" data-card="${esc(s.id)}">${esc(t('Not now'))}</button></p>`};
document.addEventListener('click',async e=>{const b=e.target.closest('[data-family-invite]');if(!b)return;const later=b.dataset.familyInvite==='later';if(later)b.disabled=true;
 // Invite: the link opens the account page in a new tab by itself (no popup to block); this only marks it as used.
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'family_invite',args:{suggestion_id:b.dataset.card,do:later?'later':'open'}})});
  if(later)toast(t('Hidden for 90 days.'));await refresh()}catch(err){errCaught(err);toast(err.message,true);b.disabled=false}});
function familyInviteSwitch(){const b=$('#family-invite-switch');if(!b)return;b.setAttribute('aria-checked',String(state.fleet?.family_invites!==false))}
$('#family-invite-switch').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'family_invite_setting',args:{on}})});if(state.fleet)state.fleet.family_invites=r.on;familyInviteSwitch();notice(t(r.on?'Family invites are suggested.':'Family invites are no longer suggested.'))}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}};
