// Missed to-dos (Learning, How it's going): the weekly check of messages that got no to-do (missed_work.py). One
// number (the share that likely needed one, with its range), the misses it found to check (each opens the message and
// takes the owner's Real miss or Not a miss, kept on this Machine).
const MW_CHANNEL={email:'Email',message:'Message',meeting:'Meeting'};
const mwPct=v=>v==null?null:Math.round(100*v);
const mwUrl=u=>typeof u==='string'&&/^https:\/\//.test(u)?u:null;  // only https links open, like the server keeps them
function missedNodes(m){if(!m)return [];const est=m.adjusted||m.raw;if(!est||est.rate==null)return [];
 const day=localeDate(new Date(m.at),DL,{day:'numeric',month:'short'});
 const row=x=>{const url=mwUrl(x.url),id=Number(x.event_id);return make('div',{class:'mw-row'},make('span',{class:'grow'},make('small',{},t(MW_CHANNEL[x.channel]||'Message')+' · '+(x.area==='Personal'?t('Personal'):x.area??'')),x.reason||''),
  make('span',{class:'mw-acts'},url?make('a',{href:url,target:'_blank',rel:'noopener noreferrer'},t('Open')):'',
   make('button',{type:'button','data-mw-label':'real','data-mw-id':id,'aria-pressed':x.label==='real'},t('Real miss')),
   make('button',{type:'button','data-mw-label':'not','data-mw-id':id,'aria-pressed':x.label==='not'},t('Not a miss'))))};

 return [make('h3',{class:'q-h'},t('Missed to-dos')),make('p',{class:'learn-intro'},t('Each week I check a sample of messages that got no to-do. Last check {}.',day)),
  make('div',{class:'q-tiles mw-tiles'},qTile(mwPct(est.rate),'Likely missed',t(['Of {} message with no to-do','Of {} messages with no to-do'],Number(m.population||0).toLocaleString(DL)),make('small',{class:'q-was'},t('Between {}% and {}%',mwPct(est.low),mwPct(est.high))))),
  ...m.misses?.length?[make('div',{class:'list mw-list'},m.misses.map(row))]:[]]}
// How it's going and Missed to-dos, drawn again from state
const renderQuality=()=>$('#quality').replaceChildren(...qualityNodes(state.quality),...missedNodes(state.missed_work));
$('#quality').addEventListener('click',async e=>{const b=e.target.closest('[data-mw-label]');if(!b)return;const on=b.getAttribute('aria-pressed')==='true';b.disabled=true;
 try{const r=await request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'missed_work_label',args:{event_id:Number(b.dataset.mwId),label:on?'':b.dataset.mwLabel}})});
  state.missed_work=r.missed_work;renderQuality()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
