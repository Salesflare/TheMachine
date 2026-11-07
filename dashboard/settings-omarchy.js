// Omarchy theme: on a Machine that runs on Omarchy, the dashboard follows the Omarchy theme, as Omarchy's own apps do
// (Settings, General, This device). On by default in a browser or desktop app on that computer itself (the answer's
// `here`, machine/omarchy.py same_host); off until picked on any other device. The switch keeps an explicit choice:
// 'omarchy-theme' is '1' (on), '0' (off) or 'auto' (on by default here). The colors come from api/omarchy-theme; the
// head script paints them (paintOmarchy) from the copy kept here, so a reload starts in them. While on and in view the
// page asks every two seconds with the last ETag: a 304 from a stat until the theme changes, so a switch in Omarchy
// shows here within moments. Without Omarchy, on a phone or in the phone app, the row stays hidden and nothing is asked.
const omarchyTheme={palette:null,etag:'',timer:0};
const omarchyOn=()=>['1','auto'].includes(devStore.get('omarchy-theme'));
function omarchyRender(){const row=$('#omarchy-row'),on=omarchyOn()&&!!omarchyTheme.palette;row.hidden=!omarchyTheme.palette;
 $('#omarchy-switch').setAttribute('aria-checked',String(on));$('#theme-toggle').closest('div').hidden=on}  // the theme sets light or dark then
async function omarchyFetch(){let r;
 try{r=await fetch('api/omarchy-theme',{headers:omarchyTheme.etag?{'If-None-Match':omarchyTheme.etag}:{},credentials:'same-origin'})}catch{omarchyWatch();return}
 if(r.status===304){omarchyWatch();return}
 if(!r.ok){omarchyWatch();return}
 let p=null;try{const j=await r.json();p=j&&j.colors?j:null}catch{omarchyWatch();return}
 omarchyTheme.etag=p&&r.headers.get('ETag')||'';
 if(p?.here&&devStore.get('omarchy-theme')==null)devStore.set('omarchy-theme','auto');  // first time on this computer: on
 if(p)delete p.here;
 const was=devStore.get('omarchy-palette'),now=p?JSON.stringify(p):null;omarchyTheme.palette=p;devStore.set('omarchy-palette',now);
 if(now!==was&&omarchyOn()){const root=document.documentElement;if(was)root.classList.add('omarchy-fade');applyTheme();window.showTheme?.();setTimeout(()=>root.classList.remove('omarchy-fade'),450)}
 omarchyRender();omarchyWatch()}
function omarchyWatch(){clearTimeout(omarchyTheme.timer);if(omarchyOn()&&omarchyTheme.palette&&!document.hidden)omarchyTheme.timer=setTimeout(omarchyFetch,2000)}
$('#omarchy-switch').onclick=()=>{devStore.set('omarchy-theme',omarchyOn()?'0':'1');applyTheme();window.showTheme?.();omarchyRender();omarchyWatch()};
if(!DEV.mobile&&!DEV.phoneApp){omarchyFetch();document.addEventListener('visibilitychange',()=>{if(!document.hidden&&omarchyTheme.palette)omarchyFetch();else omarchyWatch()})}
