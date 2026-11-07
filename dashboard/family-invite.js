// Inviting family at the right moment (family_invites.py): a quiet line on a family to-do with someone not in the
// owner's Family yet. Invite opens the account page's invite form, prefilled (or, without a Family yet, starting one);
// the owner sends it there. Not now hides it for 90 days. Settings, Fleet: Suggest inviting family turns these off.
// A hosted Machine: Invite is a one-time hop to the account (/_machine/account-hop) with who, signed in, like Settings' buttons.
const familyInviteGo=(s,f)=>{if(!state.manage_url)return html`<a class="link" href="${safeHref(f.url)}" target="_blank" rel="noopener" data-family-invite="open" data-card="${s.id}">${t('Invite')}</a>`;
 let q;try{q=new URL(f.url,location.href).searchParams}catch{q=new URLSearchParams()}
 return html`<form method="post" action="/_machine/account-hop" class="inline"><input type="hidden" name="to" value="family_invite"><input type="hidden" name="email" value="${q.get('to')||''}"><input type="hidden" name="name" value="${q.get('name')||''}"><button type="button" class="link" data-family-invite="open" data-card="${s.id}">${t('Invite')}</button></form>`};
const familyInviteNote=s=>{const f=!closed(s)&&s.family_invite;if(!f)return '';
 return html`<div class="note family-invite">${f.question} ${f.line} ${familyInviteGo(s,f)} <button type="button" class="link" data-family-invite="later" data-card="${s.id}">${t('Not now')}</button></div>`};  // a div: a form can't sit in a p
document.addEventListener('click',async e=>{const b=e.target.closest('[data-family-invite]');if(!b)return;const later=b.dataset.familyInvite==='later',hop=!later&&b.form;if(later||hop)b.disabled=true;
 // Invite: the link opens the account page in a new tab by itself (no popup to block); this only marks it as used.
 // A hosted Machine's hop: marked first, then this page goes to the account's step.
 try{await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'family_invite',args:{suggestion_id:b.dataset.card,do:later?'later':'open'}})});
  if(hop)return hop.submit();if(later)toast(t('Hidden for 90 days.'));await refresh()}catch(err){errCaught(err);toast(err.message,true);b.disabled=false}});
function familyInviteSwitch(){const b=$('#family-invite-switch');if(!b)return;b.setAttribute('aria-checked',String(state.fleet?.family_invites!==false))}
$('#family-invite-switch').onclick=async e=>{const b=e.currentTarget,on=b.getAttribute('aria-checked')!=='true';b.disabled=true;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'family_invite_setting',args:{on}})});if(state.fleet)state.fleet.family_invites=r.on;familyInviteSwitch();notice(t(r.on?'Family invites are suggested.':'Family invites are no longer suggested.'))}catch(err){errCaught(err);notice(err.message)}finally{b.disabled=false}};
