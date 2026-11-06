// Reviews off (a new install, before --activate or the hosted "Turn it on" step): said on every tab, with the way to turn them on; with cards already there, that they came from the one-time first look.
// Hosted, still setting up: the step that is missing on its setup page (no AI yet, or no mail), since reviews turn on by themselves after it.
// A new hosted Machine (reviews_auto): reviews turn on by themselves once its AI and mail are connected, so it never
// says "Checks are off" or offers to turn them on; only a step that is really missing, else how far it is (SETUP_LINE).
const startsByItself=()=>state.reviews_on===false&&!!state.manage_url&&!!state.reviews_auto;
const SETUP_LINE='Reading your mail, first to-dos in a few minutes';
// The AI the owner is signing in to on the setup page right now (ChatGPT, Claude), while the first look still waits for a
// model: "Connecting ChatGPT…" in place of "Pick your AI", which comes back only when that sign-in fails or runs out.
const aiConnecting=()=>{const live=state.review_live;return state.manage_url&&state.reviews_on===false&&live?.first_look?.why==='model'&&live.ai_connecting?.name||null};
const setupLine=()=>{const ai=aiConnecting();return ai?t('Connecting {}…',ai):t(SETUP_LINE)};
const setupStep=()=>{const why=state.manage_url&&state.reviews_on===false&&state.review_live?.first_look?.why,mail=(state.connectors||[]).some(c=>['gmail','outlook'].includes(c.service));
 if(why==='model'&&aiConnecting())return null;
 return why==='model'?{url:state.manage_url+'#model',action:'Pick your AI',text:'Pick your AI to get your first to-dos.'}:(why==='sources'||startsByItself())&&!mail?{url:state.manage_url+'#google',action:'Connect mail',text:'Connect your mail to get your first to-dos.'}:null};
const turnOn=()=>{const step=setupStep();return step?{url:step.url,action:step.action}:state.manage_url?{url:state.manage_url+'#turn-on',action:'Turn on checks'}:{action:'Run: ./install.sh --activate'}};
// Whose sign-in a source's sign-in problem is: Google (Gmail, Calendar) or Microsoft (Outlook and its calendar), else ''
const accountOf=c=>c.error==='docs_not_connected'?'':/google_signin_expired/.test(c.error||'')||['gmail','calendar'].includes(c.service)?'Google'
 :/microsoft_signin_expired/.test(c.error||'')||['outlook','outlook_calendar'].includes(c.service)?'Microsoft':'';
function renderNeedsYou(){const items=[...(state.needs_you||[])],manage=state.manage_url;
if(state.reviews_on===false&&(!startsByItself()||setupStep()))items.unshift({home:'health',text:setupStep()?.text||((state.suggestions||[]).length?'Checks are off: the to-dos here come from a one-time first look, and no new ones arrive yet.':'Checks are off, so no to-dos arrive yet.'),...turnOn()});
for(const c of state.connectors||[])if(c.signed_out)items.push({home:'health',conn:1,text:t('Signed out of {} ({}).',service(c.service),c.display_name||c.id),url:c.sign_in_url||null,action:c.sign_in_url?'Sign in again':'Show',tab:c.sign_in_url?null:'health',blank:true});
else if(c.error==='android_offline')items.push({home:'health',conn:1,text:t('{} is not connected. Open the OpenClaw app on it.',c.display_name||c.id),action:'Show',tab:'health'});
else if(c.error&&connectorHealth(c).tone==='orange'){
 // One line per account, not per service: a Google or Microsoft sign-in covers all of its services (Gmail and Calendar
 // share one sign-in), so one Reconnect restores them all
 const who=accountOf(c),key=who&&who+'|'+(c.email||c.display_name||c.id),same=key&&items.find(i=>i.key===key);if(same)continue;
 items.push({home:'health',conn:1,key,text:who?t('Sign in to {} again. {}',who,c.email||c.display_name||c.id):c.error==='docs_not_connected'?(c.docs_provider==='google'?'Google Docs waits for your OK to read your files.':'Microsoft OneDrive waits for your OK to read your files.'):`${c.display_name||c.id} needs you to sign in again.`,url:manage?(c.hosted_signin?null:c.account_page||'#connections=add'):null,action:manage||c.connect_name?(c.error==='docs_not_connected'?'Connect':'Reconnect'):'Show',reconnect:!manage&&c.connect_name?c:null,hosted:manage&&c.hosted_signin?c:null,tab:manage?null:'health'});}
if(state.skills?.waiting)items.push({home:'settings:skills',text:state.skills.waiting===1?'A skill waits for you to read it.':`${state.skills.waiting} skills wait for you to read them.`,tab:'skills',action:'Show'});
// A new owner's first views: only the hello and the prepared work (Store.greeting). A setup step still missing and a
// signed-out or broken connection stay: without them the Machine can't work
if(state.greeting&&state.reviews_on!==false)items.splice(0,items.length,...items.filter(i=>i.conn));
const box=$('#needs-you');
box.replaceChildren(...items.length?[make('strong',{},'Needs you'),make('ul',{},items.map(i=>make('li',{'data-home':i.home||''},make('span',{},i.text),needsYouAction(i))))]:[]);needsYouPlace()}
// The one link or button on a Needs you line
const needsYouAction=i=>i.url?make('a',{class:'head-link',href:i.url,...i.blank?{target:'_blank',rel:'noopener'}:{}},i.action||'Open'):i.hosted?hostedReconnectNode(i.hosted,i.action||'Reconnect','head-link')
 :i.reconnect?make('button',{type:'button',class:'head-link','data-reconnect':i.reconnect.connect_name??'','data-account':i.reconnect.id??'',...i.reconnect.signin?{'data-signin':i.reconnect.signin}:{}},i.action||'Reconnect')
 :i.tab?make('button',{type:'button',class:'head-link','data-show':i.tab},i.action):i.action?make('code',{},i.action.replace(/^Run: /,'')):'';
// Each thing that needs you shows on Suggestions, and on the tab it belongs to (a source on Connections, skills on
// Settings › Skills); never on every tab, and never stacked over another tab's own notice
function needsYouPlace(){const box=$('#needs-you');if(!box)return;const tab=[...document.querySelectorAll('main>section')].find(x=>!x.hidden)?.id||'inbox',here=tab==='settings'?'settings:'+settingsNow:tab;let n=0;
 for(const li of box.querySelectorAll('li')){const on=tab==='inbox'||li.dataset.home===tab||li.dataset.home===here;li.hidden=!on;n+=on}box.hidden=!n}
$('#needs-you').onclick=e=>{const b=e.target.closest('[data-show]');if(!b)return;if(b.dataset.show==='skills'){showSettings('skills');return}document.querySelector(`nav button[data-tab="${b.dataset.show}"]`)?.click()};
