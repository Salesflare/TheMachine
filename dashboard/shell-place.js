// The page stays where the reader is. A refresh that draws a list anew, a late picture, a banner or a fitted header
// above the part on screen would push it down or pull it up (also in browsers without scroll anchoring, and where a
// list drawn anew takes the browser's anchor away): what sits under the top bar is noted while the page is still and
// put back in its place after any change, before the next paint. A page the change made too short keeps its height a
// moment, so the rows that load next come back where they were. Anything that scrolled meanwhile (the reader, a link,
// Back, the app opening a card) wins and is noted instead; so does content hidden on purpose (another tab, a fold).
// At the very top nothing is held, so a new card or a banner shows.
const place={mark:null,hold:0,holdEnd:0,touch:false,lifted:0,glide:0,opened:0};
const placeScroll=window.scrollTo.bind(window);
const placeShown=n=>n.isConnected&&n.getClientRects().length>0;
const placeTop=()=>{const t=document.querySelector('.topbar'),r=t?.getBoundingClientRect();return r&&r.height&&r.bottom>0&&getComputedStyle(t).position!=='static'?r.bottom:0};
const placeSig=n=>[...n.attributes].filter(a=>!/^(class|style|hidden|open|tabindex|aria-|data-fit)/.test(a.name)).map(a=>a.name+'='+a.value).join(' ');
const placeText=n=>n.textContent.trim().slice(0,160);
function placeNote(){if(scrollY<1){place.mark=null;return}  // at the very top nothing is held (placeKeep): nothing to measure
 const y=placeTop()+1,levels=[];let el=document.body;
 for(let d=0;d<40;d++){let next=null,i=0;
  for(const k of el.children){const r=k.getBoundingClientRect();if(r.height>0&&r.bottom>y&&!['SCRIPT','STYLE','DIALOG'].includes(k.tagName)){const p=getComputedStyle(k).position;if(p!=='fixed'&&p!=='sticky'){next=k;break}}i++}
  if(!next)break;levels.push({node:next,id:next.id,idx:i,tag:next.tagName,sig:placeSig(next),top:next.getBoundingClientRect().top});el=next;if(next.getBoundingClientRect().top>=y)break}
 for(const l of levels.slice(-6))l.text=placeText(l.node);
 place.mark=levels.length?{y:scrollY,levels}:null}
// The same element, or the one drawn in its place: by id, else the same attributes and words, else the same attributes nearest its old spot
function placeChild(el,l){if(l.id){const k=document.getElementById(l.id);return k?.parentElement===el?k:null}
 const same=[...el.children].map((k,i)=>[k,i]).filter(([k])=>k.tagName===l.tag&&placeSig(k)===l.sig);if(!same.length)return null;
 const worded=l.text!=null&&same.filter(([k])=>placeText(k)===l.text);const pool=worded&&worded.length?worded:same;
 return pool.reduce((a,b)=>Math.abs(b[1]-l.idx)<Math.abs(a[1]-l.idx)?b:a)[0]}
function placeFind(levels){let at=-1;for(let i=levels.length-1;i>=0;i--)if(levels[i].node.isConnected){at=i;break}
 if(at>=0&&!placeShown(levels[at].node))return null;  // hidden on purpose: another tab, a fold
 let el=at>=0?levels[at].node:document.body;
 for(let j=at+1;j<levels.length;j++){const k=placeChild(el,levels[j]);if(!k||!placeShown(k))break;el=k;at=j}
 return at>0&&at>=levels.length-3?{el,top:levels[at].top}:null}  // only the same content, drawn anew: a different view (another pane) is a move
function placeKeep(){const m=place.mark;if(!m||m.y<1||Date.now()<place.glide)return placeNote();
 const max=document.documentElement.scrollHeight-innerHeight,clamped=scrollY<m.y-.5&&scrollY>=max-1&&Date.now()>place.opened;  // a page just opened may be shorter
 if(Math.abs(scrollY-m.y)>=1&&!clamped)return placeNote();  // someone scrolled: the reader, a link, the app
 const f=placeFind(m.levels);if(!f)return placeNote();
 const d=f.el.getBoundingClientRect().top-f.top;
 if(Math.abs(d)>=1){const want=Math.max(0,scrollY+d);
  if(want>document.documentElement.scrollHeight-innerHeight){document.body.style.minHeight=Math.ceil(want+innerHeight)+'px';place.holdEnd=Date.now()+8000;placeLetGo()}
  placeScroll(scrollX,want)}
 placeNote()}
// The held height goes once the page has been still a moment (the rows came back), and after a few seconds at most. Where the
// shorter page then lands is the new place: noted at once, or the next change (a blink, a refresh) would take the browser's
// clamp for a list that shrank and hold the height again, the page jumping up and back every few seconds.
function placeLetGo(){clearTimeout(place.hold);place.hold=setTimeout(()=>{document.body.style.minHeight='';placeNote()},Math.max(0,Math.min(1500,place.holdEnd-Date.now())))}
let placeQueued=false;
addEventListener('scroll',()=>{if(placeQueued)return;placeQueued=true;requestAnimationFrame(()=>{placeQueued=false;placeNote()})},{passive:true});
addEventListener('resize',()=>requestAnimationFrame(placeNote));
new MutationObserver(rows=>{if(rows.some(r=>!(r.target===document.body&&r.attributeName==='style'))){placeKeep();if(document.body.style.minHeight)placeLetGo()}}).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['hidden','class','open','style','src']});
document.addEventListener('load',e=>{if(e.target.tagName==='IMG')placeKeep()},true);
document.fonts?.addEventListener?.('loadingdone',()=>placeKeep());
// A finger on the glass or a page still gliding: a background refresh waits for it to settle
addEventListener('touchstart',()=>{place.touch=true},{passive:true,capture:true});
for(const t of ['touchend','touchcancel'])addEventListener(t,e=>{if(!e.touches.length){place.touch=false;place.lifted=Date.now()}},{passive:true,capture:true});
// The app's own moves (a scroll call, scrollIntoView, focus, a link, Back) are the new place, never undone; a smooth one is let glide
const placeMoved=(f,self,a)=>{const y=scrollY,r=f.apply(self,a);if(a.some(o=>o?.behavior==='smooth'))place.glide=Date.now()+1200;if(Math.abs(scrollY-y)>=1)placeNote();return r};
for(const [o,n] of [[window,'scrollTo'],[window,'scroll'],[window,'scrollBy'],[Element.prototype,'scrollIntoView'],[HTMLElement.prototype,'focus']]){const f=o[n];o[n]=function(...a){return placeMoved(f,this,a)}}
for(const t of ['hashchange','popstate'])addEventListener(t,()=>{place.opened=Date.now()+5000},true);
for(const t of ['touchstart','wheel','keydown','mousedown'])addEventListener(t,()=>{place.opened=0},{passive:true,capture:true});
const placeBusy=()=>place.touch||Date.now()-place.lifted<1000;
// A view drawn in place of a longer one (+ Add's grid swapped for one source's form): its top just under the top bar when
// it is out of sight or far down, then focus on it (the field given, else its heading), and that is the new place.
function viewTop(el,focus){if(!el?.isConnected)return;const r=el.getBoundingClientRect(),top=placeTop();
 if(r.top<top||r.top>innerHeight*.5)scrollTo(scrollX,Math.max(0,scrollY+r.top-top-12));
 const f=focus||el.querySelector('h1,h2,h3');if(f){if(!focus&&!f.hasAttribute('tabindex'))f.tabIndex=-1;f.focus({preventScroll:true})}
 placeNote()}
// Folds the reader opened themselves (a diff, a card's details, a history) stay open when a refresh draws their list anew
document.addEventListener('click',e=>{const s=e.isTrusted&&e.target.closest?.('summary'),d=s?.parentElement;if(d?.tagName==='DETAILS')d._mine=!d.open},true);
function foldsKeep(box){const key=d=>{const a=d.parentElement?.closest('[id]');return a&&box.contains(a)?[a.id,a.className,a.dataset.status,d.className,d.querySelector(':scope>summary')?.textContent.trim()].join('|'):null};  // the same fold in the same card, while the card is in the same state
 const open=new Set([...box.querySelectorAll('details[open]')].filter(d=>d._mine&&!d.matches('.more-actions')&&!d.querySelector('[role=menu]')).map(key).filter(Boolean));
 return ()=>{if(open.size)for(const d of box.querySelectorAll('details:not([open])'))if(open.has(key(d))){d.open=true;d._mine=true}}}
