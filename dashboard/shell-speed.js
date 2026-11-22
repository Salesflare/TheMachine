// How fast this page opened on To-dos, for the Machine's daily summary (load_speed.py; a hosted Machine passes it on
// with its activity counts). shell-render.js marks the first drawing (tm-warm or tm-cold) and its end (tm-tap). A lazy
// part (dashboard_parts.LAZY 'newtodo'), so it runs once the page is quiet: never on the way to the first drawing. Each
// load waits on this device until there are 3, or the oldest is an hour old, and they go in one request: two times in
// ms, warm or cold, phone or desktop, app or browser. Nothing else: no address, no counts, no user agent.
(()=>{const at=n=>performance.getEntriesByName(n)[0]?.startTime,warm=at('tm-warm')!=null,drawn=at(warm?'tm-warm':'tm-cold'),tap=at('tm-tap'),paint=at('first-contentful-paint');
 // no marks: not opened on To-dos (or every part is inline, as in tests and the demo). A page opened in the background
 // drew before it was shown (its first paint comes later): no measure of anything a person waited for
 if(drawn==null||tap==null||paint>drawn+500||tap>6e4)return;
 const KEY='tm-speed',now=Date.now();let kept=[];try{kept=JSON.parse(localStorage.getItem(KEY)||'[]').slice(-19)}catch{}
 kept.push({drawn:Math.round(drawn),tap:Math.round(tap),warm,phone:onPhone(),app:DEV.phoneApp||inApp(),at:now});
 devStore.set(KEY,JSON.stringify(kept));if(!csrfLive||kept.length<3&&now-kept[0].at<36e5&&devStore.get(KEY))return;
 // a plain fetch, not request(): a measure that fails waits for the next time, and costs no retries or error reports
 fetch('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrfLive},body:JSON.stringify({action:'load_speed',args:{loads:kept.map(({at,...l})=>l)}})})
  .then(r=>{if(r.ok&&/json/.test(r.headers.get('content-type')))devStore.set(KEY,null)},()=>{})})();
