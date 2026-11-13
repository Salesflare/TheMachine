import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Microsoft Teams on a hosted Machine (connectors/teams.py): + Add has a Teams tile; its form signs in with Microsoft
// (work only: no Work or personal question) and shows the Teams admin link (m365-admin-consent/teams). Its card says
// in one short line each what it can't read yet and why. Made-up data, a local fixture server, nothing signed in.
// 390 and 1440, light and dark; SHOTS=<folder> saves screenshots.
const LINK='https://themachine.computer/m365-admin-consent/teams';
const CP='https://app.example.test';
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const card={id:'teams',display_name:'Microsoft Teams',email:'owner@acme.example',service:'teams',transport:'broker',boundary:'work',events:42,recent_events:12,
 last_success:now,what:'Chats, meeting chats and meeting notes from Teams. Reads only.',hosted_signin:'microsoft_teams',
 teams_missing:{channels:'admin',transcripts:'admin',notes:'admin'}};
const posted=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/_machine/connect'){let body='';for await(const b of req)body+=b;posted.push(Object.fromEntries(new URLSearchParams(body)));res.setHeader('Content-Type','text/html');res.end('<title>Microsoft</title>');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[card],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],manage_url:CP+'/setup'}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:CP+'/setup',paired:true,sources:[
   {name:'outlook',service:'outlook',label:'Outlook',what:'Your Outlook email.',connected:0,broker:true,hosted_signin:'microsoft'},
   {name:'teams',service:'teams',group:'chat',label:'Microsoft Teams',what:'Chats, meeting chats and meeting notes from Teams. Reads only.',connected:0,broker:true,hosted_signin:'microsoft_teams'}]}));return}
  res.end('{}');return}
 res.end(url.pathname==='/api/events'?'[]':'{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const [width,height] of [[1440,900],[390,844]]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}-${scheme}`;
  // + Add: the Teams tile and its form
  await page.goto(base+'/#connections=add');
  // two tiles, one sign-in: its chats under Chat, Teams meetings under Meetings
  const tiles=page.locator('#connect-add [data-connect-signin="teams"]');await tiles.first().waitFor();
  assert.deepEqual(await page.evaluate(()=>[...document.querySelectorAll('#connect-add [data-connect-signin="teams"]')].map(n=>[n.closest('.connect-group').querySelector('h4').textContent,n.innerText.replace(/\s+/g,' ').trim()])),
   [['Chat','Microsoft Teams Chats and meeting chats from Teams. Read-only. ›'],['Meetings','Teams meetings Meeting notes and transcripts from Teams. Read-only. ›']]);
  if(shots)await page.locator('#connect-add').screenshot({path:`${shots}/teams-add-${tag}.png`});
  const tile=tiles.nth(width>500?0:1);  // either one signs in the same way
  await tile.click();
  const go=page.getByRole('button',{name:'Sign in with Microsoft'});await go.waitFor();
  const form=page.locator('#connect-add');
  assert.match(await form.innerText(),/Your chats and meeting chats\. Channels and meeting notes need your admin’s OK\. Reads only\./);
  assert.equal(await form.locator('input[name="signin-scope"]').count(),0,'Teams is work only: no Work or personal question');
  const admin=form.locator('.connect-admin a');
  assert.equal(await admin.getAttribute('href'),LINK);
  assert.equal(await admin.innerText(),'themachine.computer/m365-admin-consent/teams');
  assert.ok(!(await form.innerText()).includes('—'),'no em dashes');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  if(shots)await form.screenshot({path:`${shots}/teams-signin-${tag}.png`});
  posted.length=0;
  await go.click();
  await page.waitForURL(/\/_machine\/connect$/);
  assert.equal(posted[0].source,'microsoft_teams');
  assert.equal(posted[0].scope,undefined);
  // Its card: what it reads, and what it can't yet and why
  await page.goto(base+'/#connections');
  await page.evaluate(()=>document.querySelector('nav [data-tab="health"]')?.click());
  await page.evaluate(()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.textContent.trim()==='Other sources')?.click());
  const conn=page.locator('[data-conn="teams"]');await conn.waitFor();
  const lines=await conn.locator('.conn-what').allInnerTexts();
  assert.deepEqual(lines,['Chats, meeting chats and meeting notes from Teams. Reads only. Channels and meeting notes need your admin’s OK.']);  // the first OK only: all of what the admin's OK adds, in one line
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  if(shots){await conn.scrollIntoViewIfNeeded();await conn.screenshot({path:`${shots}/teams-card-${tag}.png`})}
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('ok');
}finally{await browser?.close();server.close()}
