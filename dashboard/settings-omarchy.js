// Omarchy theme: on a Machine that runs on Omarchy, a computer's browser or desktop app can follow the Omarchy theme
// (Settings, General, This device). The colors come from api/omarchy-theme (machine/omarchy.py); the head script paints
// them (paintOmarchy) from the copy kept here, so a reload starts in them. While on and in view the page asks every
// two seconds, a cheap file read, so a theme switch shows here within moments, as in the rest of the desktop.
// Without Omarchy, on a phone or in the phone app, the row stays hidden and nothing is asked again.
const omarchyTheme={palette:null,timer:0};
const omarchyOn=()=>devStore.get('omarchy-theme')==='1';
function omarchyRender(){const row=$('#omarchy-row'),on=omarchyOn()&&!!omarchyTheme.palette;row.hidden=!omarchyTheme.palette;
 $('#omarchy-switch').setAttribute('aria-checked',String(on));$('#theme-toggle').closest('div').hidden=on}  // the theme sets light or dark then
async function omarchyFetch(){let p=null;try{const r=await request('api/omarchy-theme');p=r&&r.colors?r:null}catch{omarchyWatch();return}
 const was=devStore.get('omarchy-palette'),now=p?JSON.stringify(p):null;omarchyTheme.palette=p;devStore.set('omarchy-palette',now);
 if(now!==was&&omarchyOn()){document.documentElement.classList.add('omarchy-fade');applyTheme();setTimeout(()=>document.documentElement.classList.remove('omarchy-fade'),450)}
 omarchyRender();omarchyWatch()}
function omarchyWatch(){clearTimeout(omarchyTheme.timer);if(omarchyOn()&&omarchyTheme.palette&&!document.hidden)omarchyTheme.timer=setTimeout(omarchyFetch,2000)}
$('#omarchy-switch').onclick=()=>{devStore.set('omarchy-theme',omarchyOn()?null:'1');applyTheme();showTheme();omarchyRender();omarchyWatch()};
if(!DEV.mobile&&!DEV.phoneApp){omarchyFetch();document.addEventListener('visibilitychange',()=>{if(!document.hidden&&omarchyTheme.palette)omarchyFetch();else omarchyWatch()})}
