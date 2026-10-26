import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Declining a teammate's handoff asks "Why? (optional)" with quick picks, and the note goes with the decline; Cancel
// keeps Accept and Decline. On the sender's side, the declined card says who declined and why, with Do it myself, Hand
// to someone else and Mark done. No network beyond this fake server.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const FL='fl_'+'a'.repeat(16),Q='q_'+'1'.repeat(16);
const view={on:true,kinds:{handoff:'handoffs'},ask_meetings:false,fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:['handoff'],people:[],
 members:[{member_id:'k',name:'Kim',rules:{}}],rules:{},exceptions:{}}],
 waiting:[{id:Q,fleet:FL,name:'Kim',kind:'handoff',question:'Can you take this on: Send Sam the pricing?'}],asked:[],intro_offers:[],splits:[],log:[],notices:[]};
const card={id:'c1',title:'Export leaks rows',body:'Kim was asked to take it.',status:'prepared',event_ids:[1],scope:'work',created_at:new Date().toISOString(),
 next_actions:[],fleet_handoff:{name:'Kim',stage:'declined',note:'Not mine: <b>ask ops</b>',back:true}};
const state={suggestions:[card],connectors:[],suggestion_counts:{prepared:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:1}};
const calls=[];
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify(state));return}
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='fleet_handoff_mine')card.fleet_handoff={...card.fleet_handoff,back:false};
  if(call.action==='fleet_decide')view.waiting=[];
  res.end(JSON.stringify({status:call.action==='fleet_decide'?'declined':'ok'}));return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(view));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
 const page=await (await browser.newContext({viewport:{width:390,height:900}})).newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 // The sender: who declined and why, shown as text, with what to do now.
 const c=page.locator('#task-c1');await c.waitFor();
 assert.match(await c.innerText(),/Kim declined: Not mine: <b>ask ops<\/b>/);
 assert.deepEqual(await c.locator('.actions>button').allInnerTexts(),['Do it myself','Hand to someone else','Mark done']);
 await c.locator('[data-handoff-mine]').click();await page.waitForTimeout(200);
 assert.deepEqual(calls.at(-1),{action:'fleet_handoff_mine',args:{suggestion_id:'c1'}});
 await page.waitForFunction(()=>!document.querySelector('#task-c1 [data-handoff-mine]'));
 assert.match(await c.innerText(),/Kim declined: Not mine/);  // the note stays; the card's own buttons are back
 // The receiver: Decline asks why first; Cancel brings Accept and Decline back.
 const ask=page.locator('#suggestions #fleet-'+Q);await ask.waitFor();
 await ask.locator('[data-choice-f="decline"]').click();
 const editor=ask.locator('.fleet-note-editor');await editor.waitFor();
 assert.match(await editor.innerText(),/Why\? Optional/);
 assert.deepEqual(await editor.locator('.reason').allInnerTexts(),['Not mine','Already done','No time this week']);
 assert.equal(calls.filter(x=>x.action==='fleet_decide').length,0);  // nothing sent yet
 await editor.locator('[data-fleet-note-cancel]').click();
 assert.deepEqual(await ask.locator('.actions>button').allInnerTexts(),['Accept','Decline']);
 await ask.locator('[data-choice-f="decline"]').click();
 await ask.locator('.reason',{hasText:'Already done'}).click();
 await ask.locator('.fleet-note-editor textarea').fill('sent it Monday');
 await ask.locator('[data-fleet-note-send]').click();await page.waitForTimeout(200);
 assert.deepEqual(calls.at(-1),{action:'fleet_decide',args:{id:Q,choice:'decline',note:'Already done: sent it Monday'}});
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'scrolls sideways');
 assert.deepEqual(errors,[]);
 console.log('fleet handoff decline dashboard: ok');
}finally{await browser.close();server.close()}
