import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// A sign-in from before a newer feature (machine/app/reconnect_asks.py): one to-do of The Machine's own in For you, in
// its account's area. Reconnect leads and opens that account's sign-in; Not needed is under …; never Do it or Plan it.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),posts=[];
const card={id:'rc1',title:'Reconnect Microsoft to show your colleagues’ and contacts’ photos',body:'sam@acme.example was connected before your Machine read colleagues and contacts. Reconnect it to add their photos, read-only.',
 status:'pending',scope:'personal',origin:'machine',owner_step:1,created_at:now,event_ids:[1],reconnect:{provider:'microsoft',email:'sam@acme.example'}};
const state=()=>({suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[{id:'o1',service:'outlook',email:'sam@acme.example',display_name:'Mail',hosted_signin:'microsoft',status:'ok'}],manage_url:'https://app.example.invalid/account',fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(req.method==='POST'&&body){try{const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:state().manage_url,paired:false,
   sources:[{name:'outlook',label:'Outlook',service:'outlook',hosted_signin:'microsoft',what:'Your mail.'}]}));return}}catch{}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS||'';
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390])for(const colorScheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height:900},colorScheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);const todo=page.locator('#task-rc1');await todo.waitFor();
  const shown=await todo.locator('.actions>:is(button,a.open,.more-actions):not([hidden])').evaluateAll(n=>n.map(x=>x.tagName==='DETAILS'?'More':x.textContent.trim()));
  assert.deepEqual(shown.slice(0,2),['Reconnect','Mark done'],shown.join(' | '));
  assert.ok(!shown.includes('Do it')&&!shown.includes('Plan it'));
  assert.equal(await todo.locator('.actions>button.primary').innerText(),'Reconnect');
  const menu=await todo.locator('.more-menu>button').evaluateAll(n=>n.map(x=>x.textContent.trim()));
  assert.ok([...shown,...menu].includes('Not needed'),[...shown,...menu].join(' | '));
  assert.ok(!menu.includes('Plan it'));
  assert.match(await todo.innerText(),/sam@acme\.example was connected before your Machine read colleagues and contacts/);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  const box=await todo.evaluate(e=>e.getBoundingClientRect().toJSON());assert.ok(box.right<=width+0.5,'the to-do fits');
  if(shots){await todo.screenshot({path:`${shots}/reconnect-todo-${width}-${colorScheme}.png`});await page.screenshot({path:`${shots}/reconnect-page-${width}-${colorScheme}.png`})}
  if(width===1440&&colorScheme==='light'){
   // Reconnect opens Microsoft's sign-in for that address, the one Connections' card has
   await todo.locator('.actions>button.primary').click();
   await page.waitForFunction(()=>typeof connectSignin!=='undefined'&&connectSignin?.provider==='microsoft',null,{timeout:5000});
   assert.equal(await page.evaluate(()=>connectSignin.email),'sam@acme.example');
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('reconnect to-do ok');
