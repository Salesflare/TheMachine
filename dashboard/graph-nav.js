// Graph's rows: People, Organizations and Projects open the Graph on that pane, the address says which (#graph=orgs), the
// row of the pane on screen is lit, and the group folds (remembered).
const GRAPH_SUBS={people:'People',orgs:'Organizations',projects:'Projects',roles:'Who’s who',held:'Held back'};let graphCounts=null;
function graphCountsSet(c){if(!c)return;graphCounts=c;for(const [k,n] of Object.entries({people:c.person,orgs:c.org,projects:c.project})){const b=$('#count-'+k);if(b)b.textContent=n?String(n):''}graphSubLabels();pageHead()}
let rolesWaiting=0;
function rolesRow(on,n){rolesWaiting=on?n||0:0;const a=$('.side-sub a[data-graph-sub="roles"]');a.hidden=!on;$('#count-roles').textContent=on&&n?String(n):'';graphSubLabels();if(!$('#people').hidden)pageHead()}
function graphSubLabels(){for(const a of document.querySelectorAll('.side-sub a')){const n=a.querySelector('.badge').textContent.trim(),label=GRAPH_SUBS[a.dataset.graphSub]+(n?' · '+n:'');if(a.getAttribute('aria-label')!==label)a.setAttribute('aria-label',label)}}
function graphSubSync(){pageHead();const on=!$('#people').hidden,graph=$('nav [data-tab="people"]');let lit=false;
 const shown=graphNode&&!/^promise:/.test(graphNode)?graphNodePane(graphNode):graphShown;
 for(const a of document.querySelectorAll('.side-sub a')){const me=on&&a.dataset.graphSub===shown;lit||=me;if(me)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')}graph.classList.toggle('sub-on',lit)}
function graphHashSync(){if($('#people').hidden||graphNode||!graphShown)return;const h=location.hash;if(h&&!/^#(graph|people)(=[a-z]+)?$/.test(h))return;const want='#graph='+graphShown;if(h!==want)history.replaceState(null,'',location.pathname+location.search+want)}
$('#graph-sub').addEventListener('click',e=>{const a=e.target.closest('a[data-graph-sub]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey)return;e.preventDefault();const url=location.pathname+location.search+'#graph='+a.dataset.graphSub;
 if(history.state?.drawer)history.replaceState(null,'',url);else if(location.hash!=='#graph='+a.dataset.graphSub)history.pushState(null,'',url);openTabLink();graphSubSync();if(!DESK.matches)scrollTo(0,0)});
{const fold=$('#graph-fold'),lab=fold.parentNode.querySelector('.nl'),place=()=>{const w=lab.offsetLeft+lab.offsetWidth;if(w)fold.style.setProperty('--fold-x',w+(matchMedia('(max-width:1023px)').matches?2:4)+'px')  /* just after the label, its box never under the text */};
 new ResizeObserver(place).observe(lab);place();
 const set=open=>{fold.setAttribute('aria-expanded',String(open));fold.setAttribute('aria-label',open?'Hide People, Organizations and Projects':'Show People, Organizations and Projects');$('#graph-sub').hidden=!open};
 set(sideStore.get('graph-sub')!=='closed');fold.onclick=()=>{const open=fold.getAttribute('aria-expanded')!=='true';set(open);sideStore.set('graph-sub',open?'open':'closed')}}
// The counts come with the Graph; fetch it once at the start so the rows show them before it is opened
setTimeout(()=>{if(!graphCounts)request('api/graph').then(g=>graphCountsSet(g?.counts)).catch(()=>{})},1500);

