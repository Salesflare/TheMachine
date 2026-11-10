// Bring these in (bring_in.py): lines of the owner's OpenClaw notes (MEMORY.md, USER.md) worth keeping as facts, on
// top of What I've learned. Only what they tick is kept; the rest can be dismissed and does not come back. No
// candidates (state.bring_in is not there): nothing is drawn, not even a heading. The files are only ever read.
const bringTicked=new Set();
function bringSection(){const items=state?.bring_in||[];if(!items.length)return '';
 for(const id of [...bringTicked])if(!items.some(i=>i.id===id))bringTicked.delete(id);
 return html`<section class="learn-group" data-group="bring" aria-labelledby="learn-bring"><div class="learn-head"><h3 id="learn-bring">Bring these in <span class="count">${items.length}</span></h3><p>From your OpenClaw notes. Only what you tick is kept.</p></div><div class="list">${
  items.map(i=>html`<div><label class="fleet-option grow"><input type="checkbox" data-bring="${i.id}"${bringTicked.has(i.id)?html` checked`:''}><span class="grow">${i.text}<small>${t('From {}',i.file)}</small></span></label></div>`)
  }<div><span class="learn-acts"><button type="button" class="quiet" data-bring-dismiss>Dismiss the rest</button><button type="button" class="primary" data-bring-keep${bringTicked.size?'':html` disabled`}>Keep ticked</button></span></div></div></section>`}
$('#facts').addEventListener('change',e=>{const box=e.target.closest('[data-bring]');if(!box)return;const id=Number(box.dataset.bring);box.checked?bringTicked.add(id):bringTicked.delete(id);
 const keep=$('#facts [data-bring-keep]');if(keep)keep.disabled=!bringTicked.size});
$('#facts').addEventListener('click',async e=>{const b=e.target.closest('[data-bring-keep],[data-bring-dismiss]');if(!b)return;const keeping=b.matches('[data-bring-keep]'),ids=(state.bring_in||[]).map(i=>i.id);
 const args=keeping?{keep:ids.filter(id=>bringTicked.has(id))}:{dismiss:ids.filter(id=>!bringTicked.has(id))};if(!(args.keep||args.dismiss).length)return;
 for(const x of document.querySelectorAll('#facts [data-bring-keep],#facts [data-bring-dismiss]'))x.disabled=true;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'bring_in_decide',args})});
  state.bring_in=r.bring_in||[];if(keeping)bringTicked.clear();toast(keeping?'Kept.':'Dismissed.');refresh()}
 catch(err){errCaught(err);toast(err.message,true);if(learnEdit==null)setHTML($('#facts'),learnedList())}});
