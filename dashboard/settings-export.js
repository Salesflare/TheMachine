// Settings, General, Export: Knowledge for another AI (machine/app/knowledge_export.py, docs/knowledge-export.md). Export
// opens its options: message text and private and Careful content, both off, and an optional passphrase. Download packs
// it on the Machine (action knowledge_export) and fetches the file once by its token; nothing is kept on the device.
{const rows=()=>document.querySelectorAll('#settings-export .export-opt'),note=$('#export-note');
 // open, the top button turns into a quiet Cancel, so Download is the one action
 $('#export-knowledge').onclick=e=>{const b=e.currentTarget,open=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',String(open));
  b.textContent=open?t('Cancel'):t('Export');b.classList.toggle('quiet',open);
  for(const r of rows())r.hidden=!open;note.textContent='';if(open)$('#export-download').focus()};
 for(const id of ['#export-messages','#export-private'])$(id).onclick=e=>{const b=e.currentTarget;b.setAttribute('aria-checked',String(b.getAttribute('aria-checked')!=='true'))};
 $('#export-download').onclick=async e=>{const b=e.currentTarget,pass=$('#export-pass').value,on=id=>$(id).getAttribute('aria-checked')==='true';
  if(pass&&pass.length<10){note.textContent=t('Pick a passphrase of at least {} characters, or none.',10);return}
  b.disabled=true;note.textContent=t('Packing it…');
  try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'knowledge_export',args:{messages:on('#export-messages'),private:on('#export-private'),passphrase:pass}})});
   const res=await fetch('api/knowledge-export?token='+encodeURIComponent(r.token),{cache:'no-store'});if(!res.ok)throw Error(t('That export is gone. Export it again.'));
   const a=document.createElement('a');a.href=URL.createObjectURL(await res.blob());a.download=r.name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),60000);
   $('#export-pass').value='';note.textContent=pass?t('Downloaded. Keep the passphrase: without it the file can’t be opened.'):t('Downloaded.')}
  catch(err){errCaught(err);note.textContent=err.message}finally{b.disabled=false}}}
