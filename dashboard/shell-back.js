// Phone back closes the top dialog or sheet: each adds a history step; closed otherwise, back skips that step
let backLayers=[],backSeq=0,backSkip=0;
const backLive=l=>l.el.isConnected&&l.el.open,backIn=id=>backLayers.some(l=>l.id===id);
function backOpen(el,close){if(DESK.matches||backLayers.some(l=>l.el===el))return;backSeq=Math.max(backSeq+1,Date.now());
 history.replaceState({...history.state,under:backSeq},'');backLayers.push({el,close,id:backSeq,url:location.href});history.pushState({layer:backSeq},'')}
const backShut=el=>{backLayers=backLayers.filter(l=>l.el!==el)};
function backCancel(d){if(d.dispatchEvent(new Event('cancel',{cancelable:true}))&&d.open)d.close();if(d.open)backOpen(d,()=>backCancel(d))}  // as Esc
{const show=HTMLDialogElement.prototype.showModal;
 HTMLDialogElement.prototype.showModal=function(){const was=this.open;show.call(this);if(!was&&this.open)backOpen(this,()=>backCancel(this))}}
document.addEventListener('close',e=>{const d=e.target;if(!d.open)backShut(d)},true);
document.addEventListener('toggle',e=>{const d=e.target;if(!(d instanceof HTMLDetailsElement)||!d.matches('.card .more-actions'))return;
 if(!d.open)backShut(d);else if(matchMedia('(max-width:560px)').matches)backOpen(d,()=>{d.open=false})},true);
if(history.state?.under)history.replaceState({...history.state,under:0},'');
// the first popstate handler (shell-core.js)
function backPop(e){if(drawerPopping)return;const s=history.state||{},at=s.layer||0,skip=backSkip;backSkip=0;let shut;
 while(backLayers.at(-1)?.id>at){const l=backLayers.pop();if(backLive(l)){l.close();shut=l}}
 if(shut){if(location.href===shut.url)e.stopImmediatePropagation()}
 else if(at&&!backIn(at)||!skip&&s.under){e.stopImmediatePropagation();backSkip=1;history.back();return}
 if(s.under)history.replaceState({...s,under:0},'')}
window.machineBack=()=>{const l=backLayers.findLast(backLive);l?.close();return !!l};
