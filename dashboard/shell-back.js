// Phone back closes the top dialog or sheet: each adds a history step, taken off if closed otherwise
const backLayers=[];let backPops=0,backSeq=0;
const backLive=l=>l.el.isConnected&&l.el.open;
function backOpen(el,close){if(DESK.matches||backLayers.some(l=>l.el===el))return;backSeq=Math.max(backSeq+1,Date.now());
 const l={el,close,id:backSeq,url:location.href};backLayers.push(l);history.pushState({layer:l.id},'',l.url)}
function backShut(el){const i=backLayers.findIndex(l=>l.el===el);if(i<0)return;const [l]=backLayers.splice(i,1);
 if(history.state?.layer!==l.id)return;if(location.href!==l.url){history.replaceState(null,'',location.href);return}
 backPops++;history.back()}
function backCancel(d){if(d.dispatchEvent(new Event('cancel',{cancelable:true}))&&d.open)d.close();if(d.open)backOpen(d,()=>backCancel(d))}  // as Esc
{const show=HTMLDialogElement.prototype.showModal;
 HTMLDialogElement.prototype.showModal=function(){const was=this.open;show.call(this);if(!was&&this.open)backOpen(this,()=>backCancel(this))}}
document.addEventListener('close',e=>{const d=e.target;if(d instanceof HTMLDialogElement&&!d.open)backShut(d)},true);
document.addEventListener('toggle',e=>{const d=e.target;if(!(d instanceof HTMLDetailsElement)||!d.matches('.card .more-actions'))return;
 if(!d.open)backShut(d);else if(matchMedia('(max-width:560px)').matches)backOpen(d,()=>{d.open=false})},true);
if(history.state?.layer)history.replaceState(null,'',location.href);
// the first popstate handler (shell-core.js)
function backPop(e){if(drawerPopping)return;if(backPops){backPops--;e.stopImmediatePropagation();return}
 const at=history.state?.layer||0;let popped=null,shut=null;
 while(backLayers.at(-1)?.id>at){const l=backLayers.pop();popped=l;if(backLive(l)){l.close();shut=l}}
 if(shut){if(location.href===shut.url)e.stopImmediatePropagation();return}
 if(popped&&location.href===popped.url||at&&!backLayers.some(l=>l.id===at)){e.stopImmediatePropagation();history.back()}}
window.machineBack=()=>{const l=backLayers.findLast(backLive);l?.close();return !!l};
