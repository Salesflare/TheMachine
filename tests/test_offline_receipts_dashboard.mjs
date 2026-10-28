import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');
const raw=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const server=createServer((req,res)=>{const path=new URL(req.url,'http://fixture.invalid').pathname;
 if(path==='/'){res.setHeader('Content-Type','text/html');res.end(raw.replace('__CACHE_SCOPE__','a'.repeat(32)));return}
 res.setHeader('Content-Type','application/json');res.end(path==='/api/status'?JSON.stringify({suggestions:[],connectors:[],decisions:[],analyses:[],deliveries:[],review_runs:[],promises:[],review_health:{},fleet:{on:false}}):path==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
try{browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext(),page=await context.newPage();
 await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 await page.goto('http://127.0.0.1:'+server.address().port+'/');await page.waitForFunction(()=>!!state.fleet);
 const ordered=await page.evaluate(async()=>{
  await localCache.put('receipt-race',{text:'ready'});
  const encrypt=crypto.subtle.encrypt.bind(crypto.subtle);let n=0;
  crypto.subtle.encrypt=async(...args)=>{if(++n===1)await new Promise(r=>setTimeout(r,200));return encrypt(...args)};
  const old={text:'old',steps:[{feedback:'before'}]};
  const first=localCache.put('receipt-race',old);old.steps[0].feedback='mutated';
  const second=localCache.put('receipt-race',{text:'new'});await Promise.all([first,second]);
  crypto.subtle.encrypt=encrypt;return (await localCache.read('receipt-race')).value;
 });
 assert.deepEqual(ordered,{text:'new'},'a slow older encryption cannot replace the newer saved copy');
 const queued=await page.evaluate(async()=>{
  await outboxLoaded;clearTimeout(outbox.timer);netDown=true;csrfLive=false;
  const encrypt=crypto.subtle.encrypt.bind(crypto.subtle);let n=0;
  crypto.subtle.encrypt=async(...args)=>{if(++n===1)await new Promise(r=>setTimeout(r,180));return encrypt(...args)};
  const start=Date.now(),result=await decideOrWait('fixture',[{choice:'complete'}],'complete');
  const elapsed=Date.now()-start;crypto.subtle.encrypt=encrypt;clearTimeout(outbox.timer);
  const saved=await localCache.read('outbox');return {result,elapsed,saved:saved?.value?.[0]?.sid};
 });
 assert.equal(queued.result.waiting,true);assert.ok(queued.elapsed>=150,'waiting is acknowledged only after durable storage');
 assert.equal(queued.saved,'fixture');
 const refused=await page.evaluate(async()=>{
  clearTimeout(outbox.timer);outbox.items=[];const messages=[],prior=toast;
  toast=(s)=>messages.push(s);outbox.items.push({id:'refused',sid:'gone',kind:'complete',steps:[{choice:'complete'}]});
  const priorRequest=request;request=async()=>{throw Object.assign(Error('To-do removed'),{status:404})};
  await outboxFlush();request=priorRequest;toast=prior;return messages;
 });
 assert.ok(refused.some(s=>s.includes('couldn’t be saved')));
 assert.ok(!refused.some(s=>s.includes('Your waiting changes are saved')),'a refused change never gets a success toast');
 const draft=await page.evaluate(async()=>{
  clearTimeout(outbox.timer);outbox.items=[];const prior=toast;toast=()=>{};chatDraftKeep('gone-chat','typed since');
  outbox.items.push({id:'refused-note',sid:'gone-chat',kind:'other',text:'the waiting note',steps:[{choice:'other',feedback:'the waiting note'}]});
  const priorRequest=request;request=async()=>{throw Object.assign(Error('To-do removed'),{status:404})};
  await outboxFlush();await chatDraftsLoaded;await new Promise(r=>setTimeout(r,0));request=priorRequest;toast=prior;return chatDrafts.get('gone-chat');
 });
 assert.equal(draft,'the waiting note\n\ntyped since','a refused note comes back before the draft typed since, never over it');
 const wiped=await page.evaluate(async()=>{
  const encrypt=crypto.subtle.encrypt.bind(crypto.subtle);let n=0;
  crypto.subtle.encrypt=async(...args)=>{if(++n===1)await new Promise(r=>setTimeout(r,150));return encrypt(...args)};
  const writing=localCache.put('receipt-wipe',{text:'private fixture'});await localCache.wipe();await writing;
  crypto.subtle.encrypt=encrypt;return await localCache.read('receipt-wipe');
 });
 assert.equal(wiped,null,'an in-flight old write cannot resurrect data after sign-out');
}finally{await browser?.close();server.close()}
console.log('offline copies and owner changes have ordered, durable, truthful receipts');
