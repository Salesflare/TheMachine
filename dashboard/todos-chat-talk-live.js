// Talk live's session (todos-chat-talk.js has the rest: its button, its view and its bar), which loads when first
// needed (dashboard_parts.LAZY): starting a conversation loads it first. Everything here runs only while one is open.
async function talkStart(main,first=null){const s=main?null:chatOpen();if(talk||!main&&!s||main&&!talkOk())return;talkToastClear();micCancel();
 const v=talk={main:!!main,sid:s?.id||null,state:'start',muted:false,secs:0,limit:600,warn:540,per_use:false,said:new Set(),posting:Promise.resolve(),queue:[],relay:null,heard:{},responding:false,tell:[],pending:new Set(),dropped:new Set(),respFor:{},after:{},known:new Set(talkNeeds().map(x=>x.id)),prep:new Set(),sent:null,last:null,told:new Set(),lastUser:''};talkPaint();talkSide();talkViewPaint();
 try{v.stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,channelCount:1}})}
 catch(e){if(e?.name==='NotAllowedError'||e?.name==='SecurityError'){const d=await micDenied();if(talk!==v)return;if(!d){talkEnd();return}
   v.settings=!!d.settings;talkFail(v,d.msg);return}
  talkFail(v,e?.name==='NotFoundError'||e?.name==='OverconstrainedError'?t('No microphone found. Connect one and try again.'):t('The microphone couldn’t start. Try again.'));return}
 if(talk!==v){v.stream.getTracks().forEach(x=>x.stop());return}
 try{const r=await micPost('talk_start',{...(main?{main:true}:{suggestion_id:s.id}),languages:[...(navigator.languages||[])].slice(0,8)});if(talk!==v){micPost('talk_end',{id:r.id}).catch(()=>{});return}
  Object.assign(v,{id:r.id,limit:r.limit||600,warn:r.warn||540,per_use:!!r.per_use,tools:r.tools||[],instructions:r.instructions||'',note:r.ask_note||'',notes:r.notes||{},voice:r.voice||'',speed:r.speed||0,turn:r.turn||null,noise:r.noise||null,transcription:r.transcription||null,transcriptionNext:r.transcription_next||null,languages:r.languages||['en']});talkPaint();
  if(v.main&&(first||chatOpen()))talkFocus(v,first||chatOpen().id);  // started from a to-do's chat: that one first
  const pc=v.pc=new RTCPeerConnection();v.audio=document.createElement('audio');v.audio.autoplay=true;v.audio.hidden=true;document.body.append(v.audio);
  pc.ontrack=e=>{v.audio.srcObject=e.streams[0];v.audio.play?.().catch(()=>{})};pc.addTrack(v.stream.getAudioTracks()[0],v.stream);
  pc.onconnectionstatechange=()=>{if(talk===v&&['failed','disconnected'].includes(pc.connectionState))talkLost(v)};
  v.stream.getAudioTracks()[0]?.addEventListener('ended',()=>talkLost(v));  // iPhone stops the mic when the app leaves the screen
  const dc=v.dc=pc.createDataChannel('oai-events');dc.onopen=()=>talkReady(v);dc.onmessage=e=>talkEvent(v,e.data);
  const offer=await pc.createOffer();await pc.setLocalDescription(offer);
  const a=await micPost('talk_offer',{id:v.id,sdp:offer.sdp});if(talk!==v)return;await pc.setRemoteDescription({type:'answer',sdp:a.sdp})}
 catch(err){if(err.offline)netSet(true,err.restarting);talkFail(v,err.offline&&!err.slow?t('Offline. Start it again when you’re back online.'):err.message||t('Talk live couldn’t start. Try again.'))}}
// The voice's own setup: this page's instructions and tools (never the Gateway's agent), and what the owner says written down
function talkReady(v){if(talk!==v)return;v.state='live';v.t0=Date.now();talkWake(v);talkMedia(v);
 v.dc.send(JSON.stringify({type:'session.update',session:{type:'realtime',instructions:v.instructions,tools:v.tools,tool_choice:'auto',audio:{input:{transcription:v.transcription||{model:'gpt-4o-mini-transcribe'},...(v.noise?{noise_reduction:v.noise}:{}),...(v.turn?{turn_detection:v.turn}:{})},output:{...(v.voice?{voice:v.voice}:{}),...(v.speed?{speed:v.speed}:{})}}}}));
 v.dc.send(JSON.stringify({type:'session.update',session:{type:'realtime',include:['item.input_audio_transcription.logprobs']}}));
 if(v.transcriptionNext)v.dc.send(JSON.stringify({type:'session.update',session:{type:'realtime',audio:{input:{transcription:v.transcriptionNext}}}}));  // the newer model with every language pinned; refused, the one above stays  // how sure the transcript is (talkNoise); alone, so a refusal changes nothing else
 v.tick=setInterval(()=>talkTick(v),250);talkPaint()}
function talkTick(v){if(talk!==v)return;if(!v.main&&chatOpen()?.id!==v.sid){talkEnd();return}
 if(talkDue(v))return;
 if(v.relay&&!chat?.active&&Date.now()-v.relay.at>20000)talkTurnDone();  // a turn that ended between two looks
 if(v.main)talkNew(v);
 talkPaint()}
// What has to happen at a moment, from the clock (wall time since it went live), not from counting ticks: timers
// slow down in the background, so this also runs on the voice's events and when the page shows again (talkTick is
// the backstop). end_talk ends once its goodbye has been heard; the limit ends it; a waiting note goes when it can.
function talkDue(v,flush=true){if(talk!==v||v.state!=='live')return false;v.secs=(Date.now()-v.t0)/1000;
 if(v.ending&&(Date.now()-v.ending>10000||!v.playing&&!v.responding&&(v.byeHeard||Date.now()-v.ending>1500))){talkEnd();return true}
 if(v.secs>=v.limit){talkEnd();talkLimitToast=v.main?t('Talk ends after 30 minutes. Start it again to go on.'):t('Talk live ends after 10 minutes. Start it again to go on.');toast(talkLimitToast);return true}
 if(flush)talkTellNext(v);return false}
// The connection or the microphone went away. In the background (a phone's lock screen, an iPhone leaving the app)
// it ends cleanly and says so, with Start again; on screen it shows the error.
function talkLost(v){if(talk!==v||v.closed)return;if(document.hidden||v.hiddenAt){talkEnd();toast(t('Talk stopped while in the background.'))}
 else talkFail(v,t('Talk live lost its connection. Start it again to go on.'))}
// Keeps going in the background: the screen stays on while it is live (Wake Lock, taken again when the page shows),
// and the lock screen or notification shows it with Mute and End (Media Session). Where a browser has neither,
// nothing happens.
async function talkWake(v){const on=talk===v&&v.state==='live'&&!v.closed&&!document.hidden;
 if(!on){const w=v.wake;v.wake=null;try{await w?.release()}catch{}return}
 if(v.wake&&!v.wake.released||!navigator.wakeLock?.request)return;
 try{v.wake=await navigator.wakeLock.request('screen');if(talk!==v||v.closed){v.wake.release().catch(()=>{});v.wake=null}}catch{}}
function talkMedia(v){const m=navigator.mediaSession;if(!m)return;const on=talk===v&&v.state==='live'&&!v.closed;
 const handle=(name,fn)=>{try{m.setActionHandler(name,on?fn:null)}catch{}};
 try{m.metadata=on&&typeof MediaMetadata==='function'?new MediaMetadata({title:t('Talk'),artist:'The Machine',artwork:[{src:new URL('brand/app-icon-192.png',document.baseURI).href,sizes:'192x192',type:'image/png'}]}):null}catch{}
 handle('pause',()=>talkMute(v,true));handle('play',()=>talkMute(v,false));handle('stop',()=>talkEnd());handle('hangup',()=>talkEnd());
 handle('togglemicrophone',()=>talkMute(v,!v.muted));
 try{m.playbackState=on?v.muted?'paused':'playing':'none'}catch{}
 // A promise: Chrome refuses an unmute without a tap on the page (talkReady runs when the connection opens, the lock
 // screen's play is no tap). The microphone itself started from the tap on Talk; only the browser's indicator waits.
 try{if(on)m.setMicrophoneActive?.(!v.muted)?.catch?.(()=>{})}catch{}}
document.addEventListener('visibilitychange',()=>{const v=talk;if(!v)return;
 if(document.hidden){v.hiddenAt=Date.now();return}
 v.hiddenAt=0;if(v.state!=='live')return;
 // Back on screen: is it still there? A connection or microphone that went away while hidden ends cleanly.
 const mic=v.stream?.getAudioTracks()[0];
 if(['failed','closed','disconnected'].includes(v.pc?.connectionState)||v.dc&&v.dc.readyState!=='open'||mic?.readyState==='ended'){v.hiddenAt=1;talkLost(v);return}
 if(!talkDue(v)){talkWake(v);talkPaint()}});
// Talk works on the to-do on screen: the one the voice opens, or the one the owner opens. A send question about another is dropped.
function talkFocus(v,id){if(talk!==v||v.sid===id)return v.focusing;v.sid=id;v.asked=null;v.askedAt=0;v.queue=[];v.relay=null;talkEager(v,false);
 if(v.main){talkLog.push({about:id,title:String(state.suggestions?.find(x=>x.id===id)?.title||'').slice(0,200)});talkViewPaint()}
 return v.focusing=micPost('talk_focus',{id:v.id,suggestion_id:id}).catch(()=>{})}
// Every open to-do, in the order the dashboard shows them, each with its state in plain words (talk_live.STATES; one that
// looks done sits in Done and isn't here):
// what needs the owner (For you) first. At most 30; counts has them all.
const talkWho=s=>String((s.people||[])[0]?.name||'').slice(0,80);
const TALK_STATE={ready:'prepared',needs:'needs you',read:'to read',preparing:'preparing',waiting:'waiting on others',later:'snoozed'};
const talkNeeds=()=>talkTodos.filter(([,l])=>l==='ready'||l==='needs').map(([s])=>s);
function talkList(){const counts={};for(const [,l] of talkTodos)counts[TALK_STATE[l]]=(counts[TALK_STATE[l]]||0)+1;
 return {todos:talkTodos.slice(0,30).map(([s,l])=>({id:s.id,state:TALK_STATE[l],title:String(s.title||'').slice(0,200),...(talkWho(s)?{from:talkWho(s)}:{}),...(s.handoff_still?.name?{with:String(s.handoff_still.name).slice(0,80)}:{})})),count:talkTodos.length,counts}}
async function talkOpen(v,id){if(!/^[a-f0-9]{16}$/.test(id))return {error:'No to-do with that id. Use list_todos or find_todos.'};  // a closed one too (Done / dismissed)
 const known=state.suggestions?.some(s=>s.id===id);
 if(!known)try{await micPost('talk_focus',{id:v.id,suggestion_id:id})}catch{return {error:'No to-do with that id. Use list_todos or find_todos.'}}
 if(chatOpen()&&chatOpen().id!==id)talkGoView();await talkFocus(v,id);
 try{const out=(await micPost('talk_tool',{id:v.id,name:'todo_details',args:{}})).output;
  const mark=talkLog.findLast(x=>x.about===id);if(mark&&!mark.title&&out?.title){mark.title=String(out.title).slice(0,200);const l=$('#talk-view .talk-log');if(l)l.dataset.k='';talkViewPaint()}  // one the page hasn't loaded
  return out}catch(err){return {error:err.message}}}
// A new to-do, by voice: the same as New to-do (card_new, Work or Personal as the list shows), never sent anywhere.
// The voice stays on the to-do in focus; the transcript gets a mark, and it isn't announced as new.
async function talkCreate(v,args){const title=String(args.title||'').replace(/\s+/g,' ').trim().slice(0,200),note=String(args.note||'').trim().slice(0,1500);
 if(!title)return {error:'Say what the to-do is.'};
 try{const made=await micPost('card_new',{text:title+(note?'\n'+note:''),scope:scopeFilter==='work'||scopeFilter==='personal'?scopeFilter:null,due:null,due_at:null,about:[],attach:[]});
  v.known.add(made.id);if(talk===v&&v.main){talkLog.push({made:made.id,title});talkViewPaint()}refresh().catch(()=>{});
  return {ok:true,id:made.id,title,note:'Added to their list. Say so in a few words. The to-do in focus is still the same.'}}
 catch(err){return {error:err.message||'Couldn’t add the to-do.'}}}
// A to-do's own buttons, by voice (todo_action): the same decide and card_rename actions the card and the Done /
// dismissed list use, offered only where the page offers them. Never a send.
const talkGo=(id,choice,extra={},feedback='')=>{const step={choice,feedback,decision_id:crypto.randomUUID(),...extra};
 return OUTBOX_CHOICES.includes(choice)?decideOrWait(id,[step],choice):decidePost(id,step)};
// What Talk did last (undo_last_action takes it back on that to-do). A to-do Talk closes or snoozes takes what its chat
// was still on with it: no answer, no "the chat stopped" later.
function talkDid(v,id,act,s){if(act==='reopen'||act==='unsnooze')v.told.delete('quiet:'+id);v.last={id,act,title:String(s?.title||'').slice(0,200),at:Date.now()};if(['mark_done','dismiss','snooze'].includes(act))talkDrop(v,id)}
function talkDrop(v,id){if(v.relay?.sid===id)v.relay=null;if(v.sid===id)v.queue=[];v.told.add('quiet:'+id)}
// A snooze by voice, for any time the owner says: minutes from now, or a local time the Machine reads in the owner's
// time zone (a time without an offset is theirs, never UTC), or a preset. The time said back is local there too.
function talkSnoozeWhen(args){const m=Math.round(Number(args.snooze_minutes)),until=String(args.snooze_until||'').trim();
 if(m>0)return {snoozed_until:new Date(Date.now()+Math.min(m,525600)*60000).toISOString()};
 if(until)return {snoozed_until:until};
 return {snooze_option:['2h','tomorrow','3d','1w'].includes(args.snooze)?args.snooze:'tomorrow'}}
const talkZone=()=>state?.hours?.timezone||Intl.DateTimeFormat().resolvedOptions().timeZone;
function talkLocal(v){const tz=talkZone(),d=new Date(v);try{return d.toLocaleString('en-US',{timeZone:tz,weekday:'long',month:'long',day:'numeric',hour:'numeric',minute:'2-digit'})}catch{return d.toLocaleString('en-US')}}
async function talkDo(v,args){const id=String(args.id||v.sid||''),act=String(args.action||''),s=state.suggestions?.find(x=>x.id===id);
 if(!/^[a-f0-9]{16}$/.test(id))return {error:'Say which to-do: open it first, or give its id.'};
 const say=(text,extra={})=>{refresh().catch(()=>{});talkDid(v,id,act,s);return {ok:true,...extra,note:text}};
 const go=(choice,extra={},feedback='')=>talkGo(id,choice,extra,feedback);
 const open=s&&!closed(s);
 try{
  if(act==='rename'){const title=String(args.title||'').replace(/\s+/g,' ').trim().slice(0,200);if(!title)return {error:'Say the new title.'};
   await micPost('card_rename',{suggestion_id:id,title,reset:false,decision_id:crypto.randomUUID()});return say('Renamed. Say so in a few words.',{title})}
  if(act==='reopen'){const undo=s?.undo_until&&Date.parse(s.undo_until)>Date.now();
   if(s&&!closed(s))return {error:'It is open already.'};
   if(s?.status==='rejected'&&!undo||!s&&args.dismissed)return {error:'It was dismissed too long ago to bring back. Offer to add it again with create_todo.'};
   if(s){await go(s.status==='completed'&&!(undo&&s.expired_at)?'reopen':'undo');return say('Reopened. Say so in a few words.')}
   try{await go('reopen')}catch{try{await go('undo')}catch{return {error:'It was dismissed too long ago to bring back. Offer to add it again with create_todo.'}}}
   return say('Reopened. Say so in a few words.')}
  if(!open)return {error:s?'It is closed. Reopen it first.':'No open to-do with that id. Use list_todos or find_todos.'};
  if(act==='mark_done'){await go('complete');return say('Marked done. Say so in a few words.')}
  if(act==='dismiss'){await go('reject',{},String(args.why||'').trim().slice(0,1000));return say('Marked not needed. Say so in a few words.')}
  if(act==='snooze'){const r=await go('snooze',talkSnoozeWhen(args));
   return r?.snoozed_until?say('Snoozed until {until}, the owner’s local time. Say so in a few words.'.replace('{until}',talkLocal(r.snoozed_until)),{until:talkLocal(r.snoozed_until),time_zone:talkZone()}):say('Snoozed. Say so in a few words.')}
  if(act==='unsnooze'){if(s.status!=='snoozed')return {error:'It isn’t snoozed.'};await go('accept');return say('Back on the list. Say so in a few words.')}
  if(act==='try_again'){if(s.preparation_status!=='blocked')return {error:'Nothing is stuck there.'};await go('retry');return say('Trying again. Say so in a few words.')}
  if(act==='not_done'){if(!looksDone(s))return {error:'It doesn’t look done.'};await go('not_done');return say('Back on the list. Say so in a few words.')}
  return {error:'Unknown action.'}}
 catch(err){refresh().catch(()=>{});return {error:err.message||'That didn’t work.'}}}
// The to-do's Do it, by voice (do_it): the same accept the button sends, where the page offers it (waiting for a decision,
// or a result that only answered). The Machine's job does the work, browser included, and shows on the to-do. "Continue"
// on one that is already running lets it run.
const talkRunning=s=>['queued','starting','running'].includes(s.preparation_status)||['queued','starting','running'].includes(s.agent?.status);
const talkAnswered=s=>{try{return s.status==='prepared'&&JSON.parse(s.outcome||'{}').state==='answered'}catch{return false}};
async function talkDoIt(v,args={}){const id=String(args.id||v.sid||''),s=state.suggestions?.find(x=>x.id===id);
 if(!/^[a-f0-9]{16}$/.test(id)||!s)return {error:'Say which to-do: open it first, or give its id.'};
 if(closed(s))return {error:'It is closed. Reopen it first (todo_action reopen).'};
 if(talkRunning(s))return {ok:true,running:true,note:'It is already running. Let it run: say so in a few words, and that they can follow it on the to-do.'};
 if(s.status==='snoozed')return {error:'It is snoozed. Bring it back first (todo_action unsnooze).'};
 if(s.status==='prepared'&&!talkAnswered(s)&&s.preparation_status!=='blocked')return {error:'It has a draft ready. Sending goes through ask_to_send; changes through ask_chat.'};
 if(s.status!=='pending'&&!talkAnswered(s)&&s.preparation_status!=='blocked')return {error:'There is nothing to start on it.'};
 try{await talkGo(id,s.preparation_status==='blocked'&&s.status!=='pending'?'retry':'accept');s.preparation_status='queued';refresh().catch(()=>{});talkDid(v,id,'do_it',s);  // started: a second "do it" before the refresh lets it run
  return {ok:true,started:true,note:'The Machine started on it, browser work included. Say so in a few words, and that they can follow it on the to-do.'}}
 catch(err){refresh().catch(()=>{});return {error:err.message||'That didn’t work.'}}}
// A correction right after an action (undo_last_action): taken back on the to-do that action touched, which opens again
const TALK_UNDO={mark_done:['reopen','Marked done'],dismiss:['reopen','Marked not needed'],snooze:['unsnooze','Snoozed'],rename:['rename','Renamed']};
async function talkUndoLast(v){const l=v.last;if(!l||Date.now()-l.at>600000)return {error:'Nothing you did is left to undo.'};
 const how=TALK_UNDO[l.act];if(!how)return {error:l.act==='do_it'?'The Machine’s job has started; it can be stopped on the to-do itself.':'That can’t be undone from here.'};
 const r=await talkDo(v,{id:l.id,action:how[0],...(l.act==='rename'?{title:l.title}:{})});v.last=null;if(r.error)return r;
 if(v.main)await talkOpen(v,l.id);
 return {ok:true,undid:how[1],id:l.id,title:l.title,note:`Undid "${how[1]}" on "${l.title}" and opened it again. Say what you undid in a few words, then do what the owner meant on this to-do.`}}
// Undo, by voice or on the bar: every send still waiting from Talk's last yes (talk_undo, as the chat's Undo)
async function talkUndoSend(v){const x=v.sent;if(!x||x.undone||Date.now()>x.until)return {error:'Nothing is waiting to send any more.'};x.undone=true;talkPaint();let n=0;
 for(const item of x.items)try{await micPost('talk_undo',{suggestion_id:item.suggestion_id,approval_id:item.approval_id});n++}catch{}
 refresh().catch(()=>{});if(chatOpen())chatPoll();
 return n?{ok:true,canceled:n,note:'Canceled. Nothing was sent. Say so in a few words.'}:{error:'It was already on its way.'}}
// Report a bug, by voice (report_bug): the same report Help's Report a bug sends, with what the owner agreed to add
async function talkBug(v,args={}){const summary=String(args.summary||'').trim().slice(0,3000);if(!summary)return {error:'Say what went wrong first.'};
 await lazyPart('help').catch(()=>{});  // the bug report's sending is in Help (help-panel.js), which loads when first needed
 if(typeof bugHosted!=='function'||!bugHosted()&&!state.fleet)return {error:'This Machine isn’t linked to an account, so the report can’t go from here. Say they can email support@themachine.computer.'};
 const s=v.sid&&state.suggestions?.find(x=>x.id===v.sid),parts=[`From Talk: ${summary}`];
 if(args.context===true){if(s)parts.push(`To-do in focus: ${String(s.title||'').slice(0,200)}`);if(v.recent?.length)parts.push('Last lines in Talk:\n'+v.recent.join('\n'))}
 const body={description:parts.join('\n\n').slice(0,8000),screenshot:null},diag=args.support_report===true;
 const saved={ok:true,status:'saved',note:'Saved, it goes out by itself soon. Say exactly that in a few words, nothing more.'};
 try{const r=bugHosted()?await bugHostedKeep(body,diag):await bugAction('bug_send',{...body,diagnostics:diag});
  if(r?.queued)return saved;
  if(r?.completed){const done=await Promise.race([r.completed,new Promise(ok=>setTimeout(()=>ok({later:true}),10000))]);
   if(done.error)return {error:`The report didn’t go out: ${String(done.error.message||'').slice(0,200)}`};if(done.later||done.sent?.queued)return saved}
  return {ok:true,status:'sent',note:'Say only: "Sent the bug report." Don’t say it is being looked into or fixed.'}}
 catch(err){return {error:err.message||'The report didn’t go out.'}}}
// How the Machine is doing, as Connections and Needs you show it (machine_status)
function talkStatus(){const rh=state.review_health||{};
 return {connections:(state.connectors||[]).slice(0,30).map(c=>{const h=connectorHealth(c);return {name:String(c.display_name||c.email||c.id).slice(0,80),source:service(c.service),state:String(h.text||'Connected').slice(0,120),...(h.tone==='orange'?{needs_owner:true}:{})}}),
  reviews:{on:state.reviews_on!==false,waiting:rh.pending||0,...(rh.last_completed?{last:rh.last_completed}:{})},
  needs_owner:[...document.querySelectorAll('#needs-you li>span')].map(x=>x.textContent.trim()).filter(Boolean).slice(0,8)}}
// Anything else, by voice (ask_machine): a new to-do the way New to-do makes one, with the request handed to its chat
// (talk_live.ASK_PREFIX: the chat's own rules, it never sends). Its turn is followed here; the answer goes to the voice.
async function talkMachine(v,req){
 try{const made=await micPost('card_new',{text:req,scope:scopeFilter==='work'||scopeFilter==='personal'?scopeFilter:null,due:null,due_at:null,about:[],attach:[]});v.known.add(made.id);
  if(talk===v){talkLog.push({made:made.id,title:req.split('\n')[0].slice(0,200)});talkViewPaint()}
  const r=await decideOrWait(made.id,[{choice:'other',feedback:req,decision_id:'chat-voice-'+crypto.randomUUID()}],'other');
  refresh().catch(()=>{});talkWatch(v,made.id,req);
  return {ok:true,waiting:!!r?.waiting,note:v.note}}
 catch(err){return {error:err.message||'Couldn’t add the to-do.'}}}
// Its answer is the chat's reply; a turn that ended without one, or never started in two minutes, says it stopped.
async function talkWatch(v,id,req=''){const at=Date.now();let busy=false;
 for(let n=0;n<400&&talk===v;n++){await new Promise(ok=>setTimeout(ok,1500));if(talk!==v)return;
  const r=await talkChatRead(id);if(!r||r.unavailable)continue;if(r.active){busy=true;continue}
  const said=talkReplies(r.items||[]).map(i=>String(i.text||'').trim()).filter(Boolean);
  if(said.length||busy||Date.now()-at>120000){await refresh().catch(()=>{});talkChatSaid(v,id,said.join(' ').slice(0,3000),req);return}}}
// A to-do that comes to need the owner while Talk is open (in For you): a short heads-up at the next pause
// (talkTellNext waits while either side talks), once. One that was preparing says it's ready now (notes.ready).
function talkNew(v){if(!v.dc||v.state!=='live')return;for(const [s,l] of talkTodos)if(l==='preparing')v.prep.add(s.id);
 for(const s of talkNeeds())if(!v.known.has(s.id)){v.known.add(s.id);const note=v.prep.has(s.id)&&v.notes.ready||v.notes.new||'{title}';
  talkTell(v,note.replace('{title}',String(s.title||'').slice(0,200)).replace('{from}',talkWho(s)||'unknown'))}}
// What the voice says is kept once its response is done, unless the owner talked over it (OpenAI stops it): a cut-off start
// ("The chat is on…") never lands in the chat.
async function talkEvent(v,data){if(talk!==v)return;let e;try{e=JSON.parse(data)}catch{return}
 if(e.type==='input_audio_buffer.speech_started')v.speaking=true;
 else if(e.type==='input_audio_buffer.speech_stopped'){v.speaking=false;setTimeout(()=>talkTellNext(v),1200)}
 else if(e.type==='input_audio_buffer.committed'){v.lastItem=e.item_id;if(e.item_id)v.pending.add(e.item_id)}
 else if(e.type==='conversation.item.input_audio_transcription.completed')talkHeard(v,e);
 else if(e.type==='conversation.item.input_audio_transcription.failed')talkHeard(v,{item_id:e.item_id,transcript:'',failed:true,error:e.error});
 else if(e.type==='response.created'){v.responding=true;if(e.response?.id&&v.lastItem)v.respFor[e.response.id]=v.lastItem;v.lastItem=null}
 else if(e.type==='response.output_audio_transcript.done')(v.heard[e.response_id]||=[]).push([e.transcript,e.item_id]);
 else if(e.type==='response.done'){v.responding=false;const id=e.response?.id,said=v.heard[id]||[],to=v.respFor[id];delete v.heard[id];delete v.respFor[id];
  if(e.response?.status!=='cancelled'&&!v.dropped.has(to)){const keep=()=>said.forEach(([text,item])=>talkLine(v,'assistant',text,item));
   if(to&&v.pending.has(to)){(v.after[to]||=[]).push(keep);setTimeout(()=>talkHeard(v,{item_id:to,transcript:null}),4000)}else keep()}  // a reply to words not yet written down waits for them
  talkTellNext(v)}
 else if(e.type==='output_audio_buffer.started')v.playing=true;
 else if(e.type==='output_audio_buffer.stopped'||e.type==='output_audio_buffer.cleared')v.playing=false;
 else if(e.type==='response.function_call_arguments.done')talkTool(v,e);
 if(v.ending&&e.type==='output_audio_buffer.stopped')v.byeHeard=true;
 talkDue(v,false)}  // every event of the voice's: the goodbye heard, the limit (a waiting note goes on response.done)
// What the owner said, once written down. A noise, a sound or a few words in a script the owner's languages don't use
// (gpt-realtime heard "음력?" or "แก" in a rustle) isn't kept, and the voice's reply to it is stopped and dropped too.
// transcript null: the transcript never came (a reply waiting on it is kept).
function talkHeard(v,e){const item=e.item_id;if(!v.pending.has(item)&&e.transcript==null)return;v.pending.delete(item);
 const heardIn=Array.isArray(e.languages)?e.languages.map(talkLang).filter(Boolean):[],mine=(v.languages||['en']).map(talkLang);
 const noise=e.transcript!=null&&talkNoise(e.transcript,e.logprobs,v.transcription?.prompt,v.languages),foreign=!noise&&e.transcript!=null&&!talkShort(e.transcript)&&(talkForeign(e.transcript,v.languages)||heardIn.length>0&&!heardIn.some(l=>mine.includes(l)));  // gpt-transcribe says which language it heard
 if(noise||foreign){v.dropped.add(item);if(v.dc?.readyState==='open'){
   if(item)v.dc.send(JSON.stringify({type:'conversation.item.delete',item_id:item}));  // out of what the voice remembers
   for(const [id,to] of Object.entries(v.respFor))if(to===item&&v.responding){v.dc.send(JSON.stringify({type:'response.cancel',response_id:id}));v.dc.send(JSON.stringify({type:'output_audio_buffer.clear'}))}}
  if(e.failed&&e.error)console.warn('Talk: transcription failed',e.error?.code||'',e.error?.message||'');
  if(foreign||e.failed)talkMiss(v,e.failed)}
 else if(e.transcript){v.misses=0;v.unheardTold=false;v.lastUser=String(e.transcript).trim();talkLine(v,'user',e.transcript,item)}
 const after=v.after[item]||[];delete v.after[item];if(!noise&&!foreign)after.forEach(f=>f())}
// Words that didn't come through (another language, or a transcription that failed): the first time "Sorry, say that
// again?" (notes.again). Twice in a row, or a failed transcription, says once what's wrong instead (notes.unheard: it
// can't make out their words, check the microphone or type), then stays quiet until a line comes through, never a loop.
function talkMiss(v,failed){v.misses=(v.misses||0)+1;
 if(v.unheardTold)return;
 if(!failed&&v.misses<2){talkTell(v,v.notes.again||'');return}
 v.unheardTold=true;talkTell(v,v.notes.unheard||v.notes.again||'')}
// A language gpt-transcribe says it heard: [{code:'fr'}] in its events, an ISO 639-1 code ('fr', 'pt-BR') or a 639-3
// one ('fra'); a plain string too. Read as 'fr', or as the 639-3 code when the app has no such language.
const TALK_ISO3={eng:'en',nld:'nl',dut:'nl',deu:'de',ger:'de',fra:'fr',fre:'fr',spa:'es',ita:'it',por:'pt',zho:'zh',chi:'zh',cmn:'zh',jpn:'ja',kor:'ko',rus:'ru'};
const talkLang=x=>{const c=String((x&&typeof x==='object'?x.code??x.language:x)??'').trim().toLowerCase().split(/[-_]/)[0];
 return /^[a-z]{2,3}$/.test(c)?TALK_ISO3[c]||c:''};
// The short answers and commands Talk listens for (yes, no, ok, send it, stop, undo, next…, in the app's languages): never
// taken for noise, however unsure the transcript is (talk_live.YES has the same yes words)
const TALK_SHORT=new Set(`yes yeah yep yup ok okay sure send it go ahead no nope nah stop undo wait cancel next previous back skip done dismiss snooze again please now do them all both ja jawel jep oke okee nee neen niet doe maar verstuur stuur hoor prima goed klopt wacht volgende vorige terug klaar nein jawohl klar genau gut bitte oui non daccord si vale claro sim nao certo bye goodbye thanks thank cheers doei dag bedankt tschuss danke merci ciao grazie adios gracias tchau obrigado да нет ок хорошо стоп отмена дальше спасибо はい いいえ うん 送って 待って ありがとう 네 예 아니요 아니 보내 잠깐 고마워요 감사합니다 好 好的 是的 不 不要 发吧 等等 谢谢`.normalize('NFKD').replace(/\p{M}/gu,'').split(' '));  // as talkWords reads them (Hangul in its letters)
const talkWords=text=>String(text||'').toLowerCase().normalize('NFKD').replace(/\p{M}/gu,'').replace(/[’']/g,'').match(/[\p{L}\p{N}]+/gu)||[];
const talkShort=text=>{const w=talkWords(text);return w.length>0&&w.length<=3&&w.every(x=>TALK_SHORT.has(x))};
// Whether a transcript is noise rather than words: nothing but marks, mostly letters of another script than the owner's
// (Latin, and Cyrillic, Chinese, Japanese or Korean for those languages), the transcription prompt itself, or a short line the model was unsure of (its
// average logprob, when OpenAI sends them). A short answer or command ("yes", "ja", "send it", "undo") is never noise.
const TALK_SCRIPTS={ru:/\p{Script=Cyrillic}/u,zh:/\p{Script=Han}/u,ja:/[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}ー]/u,ko:/[\p{Script=Hangul}\p{Script=Han}]/u};
const talkOwnScript=(c,languages)=>/\p{Script=Latin}/u.test(c)||(languages||[]).some(l=>TALK_SCRIPTS[talkLang(l)]?.test(c));
function talkNoise(text,logprobs,prompt,languages){const s=String(text||'').normalize('NFC').trim();
 const letters=s.match(/\p{L}/gu)||[];if(!letters.length&&!/\p{N}/u.test(s))return true;
 const own=letters.filter(c=>talkOwnScript(c,languages)).length;if(own*2<letters.length)return true;
 if(talkShort(s))return false;
 const flat=x=>String(x||'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim();if(prompt&&flat(s)&&flat(prompt).includes(flat(s))&&flat(s).split(' ').length>2)return true;
 const lp=(Array.isArray(logprobs)?logprobs:[]).map(x=>+x?.logprob).filter(Number.isFinite);
 return lp.length>0&&s.split(/\s+/).length<=3&&lp.reduce((a,b)=>a+b,0)/lp.length<-1.2}
// A few words in a language the owner doesn't speak ("Ja, liebe den Movon.", "Nun liebt's." when they speak English and
// Dutch): the transcription guessed from noise or a mumble. Words only one app language uses tell; shared ones ("ja") don't.
const TALK_MARK={en:'the and you this that what with have please thanks yes yeah okay next send would could should',
 nl:'het een ik niet wat dat maar voor ook nog wel toch goed doe stuur volgende graag hoor alsjeblieft bedankt zeker jij',
 de:'ich nicht und ist das nun auch wir mit auf fur aber noch schon sehr bitte danke liebe liebt gibt doch kein keine jetzt mich dich uns euch haben habe hat wird gut endet ein eine einen dem',
 fr:'je tu nous vous est le la les une oui mais avec pour cest merci tres ca qui que quoi dans sur du des au aux il elle',
 es:'el los las una por para con pero muy gracias esta yo usted hola bueno como porque tambien',
 it:'lo gli che sono non ma grazie ciao molto questo questa perche anche',
 pt:'nao sim obrigado obrigada voce uma isso estou tudo bem tambem'};
const talkMarks=(()=>{const seen={},out={};for(const [l,w] of Object.entries(TALK_MARK))for(const x of w.split(' '))(seen[x]||=new Set()).add(l);
 for(const [x,ls] of Object.entries(seen))if(ls.size===1)out[x]=[...ls][0];return out})();
// Letters with marks each app language writes; one none of the owner's languages has ("Güzel." for English and Dutch,
// Turkish from a mumble) tells too, unless a word of their own is in the line ("send it to José").
const TALK_LETTERS={en:'',nl:'éëïèóáêöç',de:'äöüß',fr:'éèêàâçëïîôûùœÿ',es:'áéíóúñü',it:'àèéìòù',pt:'áâãàçéêíóôõú'};
function talkForeign(text,languages){const mine=new Set((languages||['en']).map(x=>String(x).slice(0,2))),w=talkWords(text);if(!w.length||w.length>10||talkShort(text))return false;
 const langs=w.map(x=>talkMarks[x]).filter(Boolean);if(langs.some(l=>mine.has(l)))return false;if(langs.length)return true;
 const ok=new Set([...mine].map(l=>TALK_LETTERS[l]||'').join('')),odd=[...String(text).toLowerCase().normalize('NFC')].filter(c=>/\p{L}/u.test(c)&&!/[a-z]/.test(c)&&!(/\P{Script=Latin}/u.test(c)&&talkOwnScript(c,languages)));
 return w.length<=4&&odd.some(c=>!ok.has(c))}
// What one side said goes into the chat as an ordinary message (and is kept by the Machine, talk_line)
const talkNoDash=text=>String(text||'').replace(/\s*\u2014\s*|\s+\u2013\s+/g,', ').replace(/,\s*([.,!?])/g,'$1').replace(/^,\s*/,'');
function talkLine(v,role,text,item){text=talkNoDash(String(text||'').trim());  // spoken style: no dashes, either side
 const key=role+':'+(item||text);if(!text||v.said.has(key))return;v.said.add(key);
 v.posting=Promise.all([v.posting,micPost('talk_line',{id:v.id,role,text}).catch(()=>{})]);  // kept before the Machine judges an answer
 (v.recent||=[]).push((role==='user'?'Owner: ':'Talk: ')+text.slice(0,300));v.recent=v.recent.slice(-8);
 if(v.main){talkLog.push({role,text});talkViewPaint()}
 if(chat&&chatOpen()?.id===v.sid){chat={...chat,items:[...(chat.items||[]),{kind:role==='user'?'you':'reply',text,via:'live',at:Date.now()}]};paintChat();chatToEnd()}}
// Before anything that changes something: the owner's latest words must be words. A noise dropped after their last line,
// or one odd word ("azk" taken as "ask"), gets "Sorry, say that again?" and nothing is done.
const TALK_CHANGES=['create_todo','todo_action','do_it','undo_last_action','report_bug','ask_machine'];
const talkUnclear=(v,e)=>v.dropped.has(v.respFor[e.response_id])||!!v.lastUser&&talkWords(v.lastUser).length===1&&!talkShort(v.lastUser);
async function talkTool(v,e){let args={},output;try{args=JSON.parse(e.arguments||'{}')}catch{}
 // The owner said they're done: it ends the way End does, once its goodbye has been heard (talkTick)
 if(e.name==='end_talk'&&talkUnclear(v,e)){if(v.dc?.readyState==='open'){v.dc.send(JSON.stringify({type:'conversation.item.create',item:{type:'function_call_output',call_id:e.call_id,output:JSON.stringify({error:'What the owner said wasn’t clear, so Talk goes on.',note:v.notes.again||'Say only: "Sorry, say that again?"'})}}));v.dc.send(JSON.stringify({type:'response.create'}))}return}
 if(e.name==='end_talk'){v.ending=Date.now();if(v.dc?.readyState==='open')v.dc.send(JSON.stringify({type:'conversation.item.create',item:{type:'function_call_output',call_id:e.call_id,output:JSON.stringify({ok:true})}}));return}
 if(TALK_CHANGES.includes(e.name)&&talkUnclear(v,e))output={error:'What the owner said wasn’t clear, so nothing was done.',note:v.notes.again||'Say only: "Sorry, say that again?"'};
 else if(e.name==='ask_chat'){const req=String(args.request||'').trim().slice(0,2000);output=req?await talkAsk(v,req):{error:'Say what to ask.'};if(output.ok&&!output.note)output.note=output.queued?v.notes.queued||v.note:v.note}
 else if(e.name==='list_todos'&&v.main)output=talkList();
 else if(e.name==='create_todo')output=await talkCreate(v,args);
 else if(e.name==='machine_status'&&v.main)output=talkStatus();
 else if(e.name==='todo_action')output=await talkDo(v,v.main?args:{...args,id:v.sid});  // a to-do's own Talk: that to-do only
 else if(e.name==='do_it'&&v.main)output=await talkDoIt(v,args);
 else if(e.name==='undo_last_action')output=await talkUndoLast(v);
 else if(e.name==='undo_send')output=await talkUndoSend(v);
 else if(e.name==='report_bug')output=await talkBug(v,args);
 else if(e.name==='ask_machine'&&v.main){const req=String(args.request||'').trim().slice(0,2000);output=req?await talkMachine(v,req):{error:'Say what to ask.'}}
 else if(e.name==='open_todo'&&v.main)output=await talkOpen(v,String(args.id||''));
 else if(e.name==='ask_to_send_all'&&v.main)output=await talkAskSend(v,{ids:Array.isArray(args.ids)?args.ids.map(String).slice(0,8):[]});
 else if(v.main&&!v.sid&&['ask_chat','read_draft','ask_to_send'].includes(e.name))output={error:'No to-do is open. Call open_todo first.'};
 else if(e.name==='read_draft')output=await talkAskSend(v,{...args,read:true});
 else if(e.name==='ask_to_send')output=await talkAskSend(v,args);
 else if(e.name==='send_answer')output=await talkAnswer(v);
 else try{output=(await micPost('talk_tool',{id:v.id,name:e.name,args})).output}catch(err){output={error:err.message}}
 if(output?.card){const card=output.card;delete output.card;if(talk===v&&v.main){talkLog.push({record:card});talkViewPaint()}}  // open_record: shown in the transcript
 if(talk!==v||v.dc?.readyState!=='open')return;
 v.dc.send(JSON.stringify({type:'conversation.item.create',item:{type:'function_call_output',call_id:e.call_id,output:JSON.stringify(output)}}));
 v.dc.send(JSON.stringify({type:'response.create'}))}
// The draft the voice may ask to send: the current one in this chat, on screen (scrolled into view). On a phone or with
// the screen off, the owner may not see it, so the voice reads it out in full before the question.
const talkShown=v=>$('#send-dialog')?.open?null:chatOpen()?.id===v.sid?document.querySelector('#chat-log .chat-draft.current [data-smart]')
 :v.main&&v.sid&&talkViewOn()?document.querySelector(`#talk-view .talk-about[data-about="${CSS.escape(v.sid)}"] .chat-draft.current [data-smart]`):null;
// A send question is open: asked, not yet answered, and not too old
const talkAsking=v=>!!v.asked&&Date.now()-(v.askedAt||0)<180000;  // the Machine's question is open (talk_live.ASK_SECONDS)
// The voice reads the whole draft out, so the screen isn't needed (a phone in a pocket, another page). When this
// to-do's draft shows (Talk's card, its chat), that one is asked about; else the Machine picks it (its only one, or the
// number the voice gives). The Machine pins the revision; a changed draft is asked about again.
async function talkAskSend(v,args={}){const b=args.ids?null:talkShown(v);b?.closest('.chat-draft')?.scrollIntoView({block:'nearest'});
 try{const r=await micPost('talk_ask_send',{id:v.id,...(args.ids?{ids:args.ids}:{}),...(b?{revision:b.dataset.smart}:{}),...(Number.isInteger(args.draft)?{draft:args.draft}:{}),...(args.read?{read:true}:{})});
  if(r.question){v.asked=r.revision||'all';v.askedAt=Date.now();talkEager(v,true)}return r}
 catch(err){return {error:err.message}}}
// While a yes or no is expected, the turn ends sooner after a short answer (semantic_vad's high eagerness): a lone "yes"
// isn't left waiting for more, so the owner doesn't say it twice. Otherwise Talk waits patiently (low).
function talkEager(v,on){if(!v.turn||v.dc?.readyState!=='open'||!!v.eager===on)return;v.eager=on;
 v.dc.send(JSON.stringify({type:'session.update',session:{type:'realtime',audio:{input:{turn_detection:on?{...v.turn,eagerness:'high'}:v.turn}}}}))}
// The owner answered: what was said is kept first, then the Machine judges it (its own record, not the voice's word).
// The answer can still be on its way from OpenAI, so it asks again for a few seconds.
async function talkAnswer(v){let r={status:'not_asked'};
 for(let i=0,tries=v.asked?14:1;i<tries&&talk===v;i++){  // the owner's words can still be on their way from OpenAI (up to ~10 s)
  await v.posting;try{r=await micPost('talk_send',{id:v.id})}catch(err){return {error:err.message}}
  if(!['no_answer','not_asked'].includes(r.status))break;await new Promise(ok=>setTimeout(ok,700))}
 if(r.status==='queued'){v.asked=null;v.sent={items:r.sent||[{suggestion_id:v.sid,approval_id:r.approval_id}],until:Date.now()+(r.undo_ms??(r.undo_seconds||10)*1000)};talkPaint();await refresh();if(chatOpen()?.id===v.sid)chatPoll()}
 else if(!['no_answer','not_asked','unclear'].includes(r.status))v.asked=null;
 if(!v.asked)talkEager(v,false);
 return r}
// What the voice asks the chat goes the way a typed message does (chatSubmit's decideOrWait, so it can wait offline
// too), as a hand-off (talk_live.RELAY_PREFIX): the chat doesn't show it as the owner's message (what they said is
// there already), and its drafts wait for their Approve. A request while the chat is still on one never stops it:
// it waits and goes when that turn ends. Then the chat's answer goes straight to the voice, which tells the owner.
// Talk's own commands never go to a chat: moving between to-dos, stopping, leaving it ("next one" once had the payroll
// chat research the next to-do). "Continue" on one whose Do it hasn't started is its Do it; on a running one, nothing.
const TALK_NAV=/^(?:(?:ok(?:ay)?|oké|ja|yes|so|alright|right|and|en)[,.!]?\s+)?(?:let'?s\s+|laten we\s+)?(?:(?:go\s+(?:to\s+)?)?(?:the\s+)?next(?:\s+one)?|move\s+on(?:\s+to\s+(?:the\s+)?next(?:\s+one)?)?|skip(?:\s+(?:it|this(?:\s+one)?))?|(?:the\s+)?previous(?:\s+one)?|go\s+back|back|stop|leave\s+it|never\s?mind|(?:de\s+)?volgende|ga\s+(?:maar\s+)?door(?:\s+naar\s+de\s+volgende)?|vorige|terug|overslaan|laat\s+(?:het|maar)(?:\s+maar)?|stop\s+maar)(?:\s+(?:please|now|then|maar|dan|alsjeblieft))*[.!]?$/i;
const TALK_GO_ON=/^(?:(?:ok(?:ay)?|ja|yes)[,.!]?\s+)?(?:(?:please\s+)?(?:continue|carry\s+on|let\s+it\s+(?:continue|run|go\s+on)|go\s+on\s+with\s+it|ga\s+verder|doorgaan|laat\s+(?:het|hem)\s+(?:maar\s+)?(?:verder\s+gaan|doorgaan|lopen)))(?:\s+(?:please|now|maar))?[.!]?$/i;
async function talkAsk(v,req){const s=state.suggestions?.find(x=>x.id===v.sid);if(!s)return {error:'This to-do is gone.'};
 if(TALK_NAV.test(req.trim()))return {error:'That is for you, not the chat: move between to-dos with list_todos and open_todo, and for "stop" or "leave it" do nothing more. Nothing was asked.'};
 if(TALK_GO_ON.test(req.trim())&&v.main){const r=await talkDoIt(v,{id:s.id});return r.error&&!talkRunning(s)?{error:`Nothing to continue there. ${r.error}`}:r}
 if(v.relay||chat?.active&&chatOpen()?.id===s.id){v.queue.push(req);return {ok:true,queued:true}}
 return talkRelay(v,s,[req])}
const talkReplies=(items=chat?.items||[])=>items.filter(i=>i.kind==='reply'&&i.via!=='live');
const talkChatRead=id=>micPost('card_chat',{suggestion_id:id}).catch(()=>null);
async function talkRelay(v,s,reqs){const here=chatOpen()?.id===s.id,seen=here?null:await talkChatRead(s.id);if(talk!==v||v.sid!==s.id)return {error:'This to-do is no longer open.'};
 const relay=v.relay={at:Date.now(),replies:talkReplies(here?undefined:seen?.items||[]).length,sid:s.id,request:reqs.join(' ').slice(0,300)};
 const steps=[...(s.status==='completed'?[{choice:'reopen',feedback:'',decision_id:crypto.randomUUID()}]:[]),{choice:'other',feedback:reqs.join('\n'),decision_id:'chat-talk-'+crypto.randomUUID()}];
 try{const r=await decideOrWait(s.id,steps,'other');
  if(chatOpen()?.id===s.id){chat={...(chat||{}),active:!r?.waiting,cursor:null};changing.delete(s.id)}
  if(!r?.waiting){await refresh();if(chatOpen()?.id===s.id){paintChat();chatToEnd();chatPoll()}else talkFollow(v,relay)}
  return {ok:true,waiting:!!r?.waiting}}
 catch(err){v.relay=null;return {error:err.message}}}
// The chat's turn ended: its answer goes to the voice at once (no checking back), then what waited goes
// The chat isn't on screen (Talk's own view, another page): its turn is followed here, the way an open chat polls it
async function talkFollow(v,relay){let busy=false;
 for(let n=0;n<400&&talk===v&&v.relay===relay;n++){await new Promise(ok=>setTimeout(ok,1500));if(talk!==v||v.relay!==relay||chatOpen()?.id===relay.sid)return;  // an open chat takes over
  const r=await talkChatRead(relay.sid);if(!r||r.unavailable||talk!==v||v.relay!==relay)continue;if(r.active){busy=true;continue}
  if(busy||talkReplies(r.items||[]).length>relay.replies||Date.now()-relay.at>20000){await refresh().catch(()=>{});talkTurnDone(r.items||[]);return}}}
