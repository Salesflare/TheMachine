import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The … menu's hand-off part (dashboard/todos-cards.js) in each mode: one way to hand off is a plain item with its whole
// name (Ask to review, Hand off, Hand to <agent>), several open the "Hand off…" sheet. Ask to review alone once threw
// "h.replace is not a function" (its button is markup, not a string) and the card's menu never opened. Nothing is pressed
// beyond opening the menu.
const dashboard=await dashboardPage(),now=new Date().toISOString();
const card=scope=>({id:'c1',title:'Reply to Sam about pricing',body:'Sam asked for pricing.',status:'prepared',event_ids:[1],scope,created_at:now,next_actions:[]});
const base={connectors:[],suggestion_counts:{prepared:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]};
const tools=[{id:'claude',name:'Claude Code',place:'local'}];
const modes=[
 {name:'review only',state:{...base,suggestions:[card('personal')],fleet:{on:true,waiting:0,reviews:['personal']}},item:'[data-review-ask]',text:'Ask to review'},
 {name:'teammate only',state:{...base,suggestions:[card('work')],fleet:{on:true,waiting:0,reviews:[]}},item:'[data-fleet-handoff]',text:'Hand off'},
 {name:'agent only',state:{...base,suggestions:[card('personal')],agent_tools:tools},text:'Hand to Claude Code'},
 {name:'several',state:{...base,suggestions:[card('work')],fleet:{on:true,waiting:0,reviews:['work']},agent_tools:tools},sub:['A teammate','Claude Code','Ask to review']}];
let state;
const view={on:true,kinds:{},fleets:[],waiting:[],asked:[],intro_offers:[],splits:[],log:[],notices:[]};
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify(state));return}
 if(req.url==='/api/action'){for await(const _ of req);res.end(JSON.stringify({ok:true}));return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(view));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{for(const m of modes){state=m.state;
 const page=await (await browser.newContext({viewport:{width:390,height:844}})).newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 const c=page.locator('#task-c1');await c.waitFor();
 await c.locator('details.more-actions>summary').click();
 const menu=c.locator('details.more-actions');
 if(m.sub){const open=menu.locator('[data-mm-open="handoff"]');assert.equal((await open.innerText()).trim(),'Hand off…',m.name);await open.click();
  const sub=menu.locator('.mm-sub');assert.ok(await sub.isVisible(),m.name);const text=await sub.innerText();
  for(const s of m.sub)assert.ok(text.includes(s),`${m.name}: ${s} in ${text}`)}
 else{assert.equal(await menu.locator('[data-mm-open]').count(),0,m.name);
  const items=(await menu.locator('button').allInnerTexts()).map(s=>s.trim());
  assert.ok(items.includes(m.text),`${m.name}: ${m.text} in ${items}`);
  if(m.item)assert.ok(await menu.locator(m.item).first().isVisible(),m.name)}
 assert.deepEqual(errors,[],m.name);
 await page.context().close()}
 console.log('hand-off menu: ok in',modes.length,'modes')}
finally{await browser.close();server.close()}
