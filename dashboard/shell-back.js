// Back closes what is open on a phone or tablet (below 1024px, as with the drawer): every modal dialog and sheet, and a
// to-do's menu sheet, puts a step on the history when it opens (the same address, state {layer}), so the back gesture
// or button closes the topmost one and the page stays. One closed another way (×, Esc, a button) takes its step back
// off, so back never lands on a step that does nothing; a step left under a later one (a link opened from the dialog)
// is stepped over when back reaches it. Back that closes nothing here is left to the routes (hash links, the drawer).
// The phone app asks machineBack() first (MainActivity), so a dialog opened by a push link, with no tap, closes too.
const backLayers=[];let backPops=0,backSeq=0;
const backLive=l=>l.el.isConnected&&l.el.open;
function backOpen(el,close){if(DESK.matches||backLayers.some(l=>l.el===el))return;backSeq=Math.max(backSeq+1,Date.now());
 const l={el,close,id:backSeq,url:location.href};backLayers.push(l);history.pushState({layer:l.id},'',l.url)}
function backShut(el){const i=backLayers.findIndex(l=>l.el===el);if(i<0)return;const [l]=backLayers.splice(i,1);
 if(history.state?.layer!==l.id)return;  // a later step is on top: stepped over when back reaches it
 if(location.href!==l.url){history.replaceState(null,'',location.href);return}  // the address moved on meanwhile: a plain step now
 backPops++;history.back()}
// Back on a dialog is Esc: its own cancel handling runs (the palette's), and one that stays open keeps a step
function backCancel(d){if(d.dispatchEvent(new Event('cancel',{cancelable:true}))&&d.open)d.close();if(d.open)backOpen(d,()=>backCancel(d))}
{const show=HTMLDialogElement.prototype.showModal;
 HTMLDialogElement.prototype.showModal=function(){const was=this.open;show.call(this);if(!was&&this.open)backOpen(this,()=>backCancel(this))}}
document.addEventListener('close',e=>{const d=e.target;if(d instanceof HTMLDialogElement&&!d.open)backShut(d)},true);  // still open: reopened since
document.addEventListener('toggle',e=>{const d=e.target;if(!(d instanceof HTMLDetailsElement)||!d.matches('.card .more-actions'))return;
 if(!d.open)backShut(d);else if(matchMedia('(max-width:560px)').matches)backOpen(d,()=>{d.open=false})},true);
if(history.state?.layer)history.replaceState(null,'',location.href);  // a reload: what it opened closed with the page
// First of the back handlers (capture), so a step that only closed something is no navigation for the others. A link
// followed from a dialog (a new step, another address) closes it too, and the routes still see that step.
addEventListener('popstate',e=>{if(backPops){backPops--;e.stopImmediatePropagation();return}
 const at=history.state?.layer||0;let popped=null,shut=null;
 while(backLayers.at(-1)?.id>at){const l=backLayers.pop();popped=l;if(backLive(l)){l.close();shut=l}}
 if(shut){if(location.href===shut.url)e.stopImmediatePropagation();return}
 // only gone ones (a menu redrawn away) or a step left behind: back goes on to the step before
 if(popped&&location.href===popped.url||at&&!backLayers.some(l=>l.id===at)){e.stopImmediatePropagation();history.back()}},true);
window.machineBack=()=>{for(let i=backLayers.length-1;i>=0;i--)if(backLive(backLayers[i])){backLayers[i].close();return true}return false};
