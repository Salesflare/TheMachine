// Settings, Security: Support access (Report a bug in help-panel.js offers it too), drawn before Activity, which lists its looks.
SETTINGS_OF['settings-support']='security';
{const d=document.createElement('div');d.id='settings-support';d.hidden=true;
 d.innerHTML=`<div class="section-head"><h2>Support access</h2><p>Let The Machine team read this Machine’s logs and settings to fix a problem. Read-only, never your messages or keys. <a class="learn" href="https://themachine.computer/help/get-support#support-access" target="_blank" rel="noopener">Learn more</a></p></div><div class="list settings-list"><div><span class="grow"><strong id="sa-state">Off</strong><small id="sa-note">Ends by itself after 24 hours.</small></span><button type="button" class="ghost" id="sa-toggle">Allow for 24 hours</button></div></div><p class="sa-log"><button type="button" class="link" id="sa-activity">See each look in Activity</button></p>`;
 $('#settings-share').after(d)}
let saAt=0,saData=null,saShown=false;
// A self-hosted Machine paired with the Network (status fleet) asks its app; if it isn't paired after all, it answers with an error (4xx) and the section stays hidden
const saLocal=allow=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'support_access',args:allow===undefined?{}:{allow}})});
async function supportAccessLoad(force){if(!bugHosted()&&!state.fleet){saShown=false;$('#settings-support').hidden=true;return}if(!force&&Date.now()-saAt<30000)return;saAt=Date.now();
 try{if(bugHosted()){const r=await fetch('/_machine/support-access',{credentials:'same-origin',redirect:'manual'});if(!r.ok)throw Error();saData=await r.json()}else saData=await saLocal();saShown=true}
 catch(e){errCaught(e);saData={error:true};if(!bugHosted()&&e.status>=400&&e.status<500)saShown=false}supportAccessRender()}
// Support access is given where it's needed, with the support report in Report a bug; Settings shows it only while it's on, to end it.
// Each look (and each one refused) is a line in Settings, Activity (settings-activity.js), under Support access.
const saOn=()=>!!saData?.until&&new Date(saData.until)>new Date(),saCan=()=>(bugHosted()||saShown)&&!saData?.error;
async function supportAccessSet(allow){if(bugHosted()){const r=await fetch('/_machine/support-access',{method:'POST',headers:{'Content-Type':'application/json'},credentials:'same-origin',redirect:'manual',body:JSON.stringify({allow})});if(!r.ok)throw Error();saData=await r.json()}else saData=await saLocal(allow);saAt=Date.now();supportAccessRender()}
function supportAccessRender(){const d=saData||{},on=saOn(),b=$('#sa-toggle');$('#settings-support').hidden=!(bugHosted()||saShown)||!on;
 $('#sa-state').textContent=d.error?'Can’t check right now':on?t('On until {}',fmtDHM(d.until,{weekday:'short',month:'short',day:'numeric'})):'Off';
 $('#sa-note').textContent=on?'Read-only. Turn it off any time.':'Ends by itself after 24 hours.';b.textContent=on?'Turn off':'Allow for 24 hours';b.dataset.on=on?'1':'';b.disabled=!!d.error;
 if(typeof actDraw==='function'&&settingsNow==='activity')actDraw()}
$('#sa-activity').onclick=()=>lazyRun('settings',()=>{act.filter='access';act.items=[];act.next=null;showSettings('activity');actLoad()});
$('#sa-toggle').onclick=async()=>{const b=$('#sa-toggle'),was=!!b.dataset.on;b.disabled=true;
 try{await supportAccessSet(!was);toast(was?'Support access is off.':'Support access is on for 24 hours.')}
 catch{toast('That didn’t work. Try again.',true)}finally{saAt=Date.now();supportAccessRender()}};
new MutationObserver(()=>{if(!$('#settings').hidden)supportAccessLoad()}).observe($('#settings'),{attributes:true,attributeFilter:['hidden']});
