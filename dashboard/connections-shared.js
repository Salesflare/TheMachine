// Connections' shared part: what the rest of the page uses from Connections (a source's health and tone for badges and
// cards, Reconnect buttons, the QR code, posting to connect) and the way in: connectOpen, connectAdd and links. The
// Connections tab's own views (connections-cards.js) load when first needed (dashboard_parts.LAZY).
// A source with read hours (X, LinkedIn: read_window from the server) rests outside them: it says when it reads again,
// not that it's stale (a busy browser left from its last read waits quietly too), and once its hours open its staleness
// counts from the opening, not from last night's read.
function connectorHealth(c){
const w=c.read_window,again=w?.reads_again_at&&Date.parse(w.reads_again_at)>Date.now()?w.reads_again_at:null,
 resting={tone:'mint',text:again&&t('Reads again at {}',fmtHM(again)),resting:true};
if(c.salesflare?.stopped)return {tone:'muted',text:'Stopped'};
if(c.covered_by)return {tone:'muted',text:t('Rests while your own connection {} reads the same.',c.covered_by),resting:true};  // a Fleet share the owner also connected
if(c.error==='docs_not_connected')return {tone:'orange',text:'Waiting for your OK to read docs'};
if(c.error&&/_signed_out$/.test(c.error))return {tone:'orange',text:'Signed out of '+service(c.service)};
if(TELEGRAM_STOP[c.error])return {tone:'orange',text:TELEGRAM_STOP[c.error]};
if(c.error==='android_offline')return {tone:'orange',text:'Phone disconnected'};
if(c.error){const help=/(auth|unauthor|forbidden|permission|invalid_grant|signin_expired|HTTP_40[13])/.test(c.error);return help?{tone:'orange',text:'Needs your help'}:c.last_success&&again?resting:{tone:'amber',text:'Reconnecting automatically'}}
if(c.salesflare?.no_access_all||c.salesflare?.feed_off)return {tone:'orange',text:'Needs your help'};  // its key opens no account, or the team's feed is off
if(c.signals===false)return {tone:'mint',text:'Connected'};  // action-only: nothing to sync, so never "waiting"
if(!c.last_success)return {tone:'muted',text:'Waiting for first sync'};
if(again)return resting;
const since=Math.max(Date.parse(c.last_success),Date.parse(w?.reads_again_at||w?.opened_at||'')||0);
if(Date.now()-since>Math.max(900000,(c.poll_seconds||300)*3000))return {tone:'amber',text:'Waiting for a fresh sync'};
if(c.service==='slack'&&(c.conversation_errors||c.deferred_threads))return {tone:'amber',text:'Connected · some conversations waiting'};
if(syncFlaky(c))return {tone:'amber',text:/HTTP_(429|5\d\d)|network|timeout/i.test(c.last_failure.error||'')?t('Connected · {} is slow at times',service(c.service)):t('Connected · some syncs fail')};
return {tone:'mint',text:'Connected'}
}
function connectorTone(c){return connectorHealth(c).tone}
// Keeps failing, though retries get through: no longer a blip that recovered
const syncFlaky=c=>c.failures_24h>=6&&!!c.last_failure&&Date.now()-Date.parse(c.last_failure.at)<3*3600e3;
let healthPane=(localStorage.getItem('health-pane')||'').replace(/^phone$/,'other'),healthPicked=false,savedLoginCount=0;
// Connections, Add: every source this install can add, set up right here with the same steps as `assistant connect`;
// its questions show one at a time. On a hosted machine Google, Microsoft, Zoom, Stripe, Intercom and Trello sign in right
// here too (hosted_signin): a POST to /_machine/connect starts the account's own sign-in for it, and the provider comes
// back to this page (#connect=<provider>/<command>), where the form follows the connecting. Others with a tile on the
// account page (GitHub, WhatsApp) link to it. On a self-hosted
// one such a source signs in through The Machine's own app (fleet.py connect_start), once this Machine is paired with
// an account, and its row follows how that goes; pasting a key stays, folded away, where the service has one (Intercom and
// Trello sign in only).
let connectList=null,connectListAt=0,connectRun=null,connectTimer=0,connectSignin=null,signinTimer=0,connectForm=null,connectSiteShown=null,connectGbrain=null;
const connectPost=(action,args={})=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args})});
const hostedReconnectNode=(c,label,cls)=>make('button',{type:'button',class:cls,'data-hosted-reconnect':c.hosted_signin??'',...c.email?{'data-email':c.email}:{},...c.service==='whatsapp'?{'data-account':c.id??''}:{}},label);
// A code the connect shows to sign in with: GitHub's device sign-in, or WhatsApp's pairing code for Linked devices.
// A QR code the Machine sends as rows of 0 and 1 (Telegram's login), drawn here: no image from anywhere else.
function qrSvg(rows){const n=rows.length,q=2,size=n+2*q;let d='';rows.forEach((r,y)=>{for(let x=0;x<r.length;x++)if(r[x]==='1')d+=`M${x+q} ${y+q}h1v1h-1z`});
 return html`<svg class="connect-qr" viewBox="0 0 ${size} ${size}" role="img" aria-label="${t('QR code')}" shape-rendering="crispEdges"><rect width="${size}" height="${size}" fill="#fff"/><path d="${d}" fill="#000"/></svg>`}
document.addEventListener('click',e=>{const a=e.target.closest('[data-connect-open]');if(!a)return;e.preventDefault();connectOpen(a.dataset.connectOpen)});
function showHealthPane(id){healthPane=id;healthPicked=true;localStorage.setItem('health-pane',id);if(lazyIn('connections'))renderHealthTabs()}
// The way into Connections' views, which load when first needed: each waits for them (offline: says so) and goes on.
async function connectAdd(force){if(!lazyIn('connections'))try{await lazyPart('connections')}catch(e){toast(e.message,true);return}return connectAddNow(force)}
async function connectOpen(name){if(!lazyIn('connections'))try{await lazyPart('connections')}catch(e){toast(e.message,true);return}return connectOpenNow(name)}
function openConnectLink(){if(/^#connect=/.test(location.hash))lazyRun('connections',()=>openConnectLinkNow())}
// Reconnect buttons elsewhere (cards, Needs you) work before the views are in: the click waits for them, then goes on.
document.addEventListener('click',e=>{if(lazyIn('connections'))return;const b=e.target.closest('[data-reconnect],[data-hosted-reconnect]');if(!b)return;
 e.preventDefault();e.stopImmediatePropagation();lazyRun('connections',()=>b.click())},true);
