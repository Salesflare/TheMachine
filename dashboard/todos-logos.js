// Every source's one-color mark: one set, keyed by source, for every small icon that says where something came from (the
// last check's rows, a to-do's source and its send button, search, a record's timeline, chat, Connections' cards). The
// same brands as the colored logos in + Add, drawn in the text's color so they sit quietly in a line. Each is a file,
// dashboard/logos/mono/<key>.svg (sources and terms in its NOTICE.md), loaded only when shown, as the mask of a
// .via-ico. A new connector ships with its mark here: tests/test_source_icons.py fails on one without.
const MONO='airbnb android bol calendar discord docs dropbox facebook gateway gbrain github gmail google_docs google_meet googlechrome googledrive googlekeep googlemaps googlemessages googlephotos googleplay googletasks hubspot instagram intercom linkedin medium messenger netflix notion openai outlook outlook_calendar paypal pinterest reddit revolut rss salesflare salesforce shortcut signal slack snapchat source spotify stripe tailscale teams telegram tiktok trello whatsapp x youtube zoom'.split(' ');
// Other names for a mark: a connector's own key, the older via- names; mail, cal and the rest are the line icons in
// todos-chat.css (Other email is the plain envelope)
const MONO_ALIAS={crm:'salesflare',codex:'openai',gdocs:'google_docs',gcal:'calendar',imap:'mail',email:'mail',chatgpt:'openai',google:'gmail',microsoft:'outlook'};
// A phone notification by the app that posted it, when it's a brand with a mark here (machine/sources/android.py names them)
const MONO_APPS={'com.google.android.gm':'gmail','com.google.android.apps.tasks':'googletasks','com.openai.chatgpt':'openai','com.tailscale.ipn':'tailscale',
 'org.telegram.messenger':'telegram','com.whatsapp':'whatsapp','com.whatsapp.w4b':'whatsapp','com.android.chrome':'googlechrome','com.google.android.calendar':'calendar',
 'computer.themachine.app':'gateway','com.android.vending':'googleplay','com.linkedin.android':'linkedin','com.Slack':'slack','com.microsoft.teams':'teams',
 'com.microsoft.office.outlook':'outlook','com.google.android.apps.messaging':'googlemessages','com.instagram.android':'instagram','com.facebook.orca':'messenger',
 'com.facebook.katana':'facebook','com.twitter.android':'x','org.thoughtcrime.securesms':'signal','com.spotify.music':'spotify','com.google.android.youtube':'youtube',
 'com.google.android.apps.maps':'googlemaps','com.google.android.apps.photos':'googlephotos','com.google.android.apps.docs':'googledrive','com.google.android.keep':'googlekeep',
 'com.google.android.apps.meetings':'google_meet','com.google.android.apps.tachyon':'google_meet','us.zoom.videomeetings':'zoom','com.intercom.android':'intercom',
 'com.stripe.android.dashboard':'stripe','com.github.android':'github','com.medium.reader':'medium','com.bol.shop':'bol','com.discord':'discord','com.reddit.frontpage':'reddit',
 'com.netflix.mediaclient':'netflix','com.airbnb.android':'airbnb','com.paypal.android.p2pmobile':'paypal','com.revolut.revolut':'revolut','notion.id':'notion',
 'com.dropbox.android':'dropbox','com.zhiliaoapp.musically':'tiktok','com.snapchat.android':'snapchat','com.pinterest':'pinterest','com.trello':'trello',
 'com.google.android.apps.docs.editors.docs':'google_docs','com.microsoft.skydrive':'docs','com.hubspot.android':'hubspot','com.salesforce.chatter':'salesforce'};
const monoKey=k=>MONO.includes(k)?k:MONO_ALIAS[k]||'';
{const st=document.createElement('style'),url=k=>`url("brand/logos/mono/${k}.svg")`;
 st.textContent=MONO.map(k=>`.via-${k}{--ico:${url(k)}}`).join('')+Object.entries(MONO_ALIAS).map(([a,k])=>`.via-${a}{--ico:${MONO.includes(k)?url(k):`var(--i-${k})`}}`).join('');
 document.head.append(st)}
document.documentElement.style.setProperty('--i-handoff','url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'black\' stroke-width=\'1.8\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3E%3Ccircle cx=\'9\' cy=\'8\' r=\'3.5\'/%3E%3Cpath d=\'M3 19.5c.8-3.2 3.2-5 6-5s5.2 1.8 6 5\'/%3E%3Cpath d=\'M16 9h6m-2.5-2.5L22 9l-2.5 2.5\'/%3E%3C/svg%3E")');
// A connected account's mark: its service, Docs by its provider (Google Docs, else Microsoft's)
const accountMark=id=>{const c=(state?.connectors||[]).find(c=>c.id===id);return !c?'':c.service==='docs'&&c.docs_provider==='google'?'google_docs':c.service||''};
// What a message's mark is: its kind ('slack.message'), the account it came in on (Gmail, Outlook or other mail; Google
// or Outlook Calendar) and, for a phone notification, the app that posted it. Unknown: the neutral mark.
const KIND_MARK={'meeting.notes':'cal','meeting.transcript':'cal','gateway.alert':'gateway','gateway.log':'gateway','owner.card':'note','invoice.payment_failed':'stripe'};
function sourceMark(kind,account,app){const k=String(kind||''),head=k.split('.')[0],svc=account?accountMark(account):'';
 if(k==='android.notification')return MONO_APPS[app]||'android';
 if(!k||head==='gmail'||head==='email')return ['gmail','outlook','imap'].includes(svc)?svc:'mail';
 if(k==='calendar.event')return ['calendar','outlook_calendar'].includes(svc)?svc:'cal';
 if(head==='docs')return svc==='google_docs'?'google_docs':'docs';
 if(KIND_MARK[k])return KIND_MARK[k];
 return head==='machine'?'gateway':monoKey(head)?head:'source'}
// The mark as a picture in a row (aria-hidden: the row names its source in words)
const markIco=k=>html`<i class="via-ico via-${monoKey(k)||['mail','cal','note','chat'].includes(k)&&k||'source'}" aria-hidden="true"></i>`;
