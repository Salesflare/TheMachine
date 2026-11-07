import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, General, Version and Settings, Model, Search by meaning (dashboard/settings-upkeep.js). Hosted: the control
// plane's summary (/_machine/account version, meaning) with Update now and the switch, each a POST to its own
// /_machine/ path; a control plane that doesn't send them yet shows neither. Self-hosted: the release from source_url and
// the embeddings block's state, read-only. At 1440x900 and 390x844, light and dark. Made-up data only. SHOTS=<dir> for
// screenshots.
const dashboard=await dashboardPage();
const hours={days:[1,2,3,4,5],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC'};
const release='release-20261105-0900';
const summary={email:'alex@example.com',hop:true,plan:null,server:null,connections:[],fleets:[],actions:['account','fleet'],links:{}};
let mode='hosted',version,meaning;const calls=[];
const reset=()=>{calls.length=0;version={release,commit:'a0eac0f',state:'behind',failed:false};meaning={on:false,want:false,note:null,error:false,big:false,memory_gb:4}};
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');let body='';for await(const c of req)body+=c;
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');
 const hosted=mode.startsWith('hosted');
 if(url.pathname==='/_machine/account'){res.end(JSON.stringify(mode==='hosted-old'?summary:{...summary,version,meaning}));return}
 if(url.pathname==='/_machine/update'&&req.method==='POST'){calls.push(['update',req.headers.origin===undefined||!!req.headers.origin,body]);version={...version,state:'updating'};res.end(JSON.stringify(version));return}
 if(url.pathname==='/_machine/update'){res.end(JSON.stringify(version));return}
 if(url.pathname==='/_machine/meaning'&&req.method==='POST'){const on=JSON.parse(body).on;calls.push(['meaning',on]);meaning={...meaning,want:on};res.end(JSON.stringify(meaning));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],hours,
  skills:{skills:[],waiting:0,targets:[],folder:'skills/the-machine'},model_usage:[],model_status:{model:'openai/example-model',provider:'openai',windows:[],checked_at:new Date().toISOString()},
  source_url:'https://github.com/Salesflare/TheMachine/tree/'+(mode==='selfhosted-dev'?'':release),meaning:{on:mode!=='selfhosted-off'},
  ...(hosted?{manage_url:'https://account.example/setup',account_url:'https://account.example/account'}:{})}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const shot=async(page,sel,name)=>{if(process.env.SHOTS)await page.locator(sel).screenshot({path:`${process.env.SHOTS}/${name}.png`})};
const fits=(page,sel)=>page.evaluate(s=>{const box=document.querySelector(s).getBoundingClientRect();return document.documentElement.scrollWidth<=innerWidth&&[...document.querySelectorAll(s+' :is(button,a)')].every(b=>{const x=b.getBoundingClientRect();return!x.width||x.right<=Math.min(innerWidth,box.right)+0.5&&x.left>=box.left-0.5})},sel);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){
  const tag=`${width}-${scheme}`;
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const open=async(m,tab)=>{mode=m;await page.goto('about:blank');await page.goto(base+'/#settings/'+tab);await page.locator(`#settings-tabs [data-settings-tab="${tab}"][aria-selected="true"]`).waitFor();await page.waitForTimeout(150)};
  // Hosted, behind: the release, A newer version is ready, Update now; pressing it posts once and says Updating
  reset();await open('hosted','general');
  const v=page.locator('#settings-version');await v.locator('#version-update').waitFor();
  assert.equal(await v.locator('h2').innerText(),'Version');
  assert.equal(await v.locator('#version-list strong').allInnerTexts().then(x=>x.join()),'The Machine');
  assert.equal(await v.locator('#version-list small').first().innerText(),'Release 20261105 · A newer version is ready.');
  assert.equal(await v.locator('a.learn').getAttribute('href'),'https://themachine.computer/help/settings#version');
  assert.ok(!(await v.innerText()).includes('OpenClaw'));
  await v.locator('#version-update').scrollIntoViewIfNeeded();assert.ok(await fits(page,'#settings-version'),tag);await shot(page,'#settings-version',`version-hosted-behind-${tag}`);
  await v.locator('#version-update').click();await v.locator('button[disabled]',{hasText:'Updating…'}).waitFor();
  assert.equal(calls.filter(c=>c[0]==='update').length,1);
  assert.ok((await v.innerText()).includes('Updating, a few minutes. Your data stays.'));
  await shot(page,'#settings-version',`version-hosted-updating-${tag}`);
  // Up to date, and a failed update says so
  version={...version,state:'current',failed:true};await open('hosted','general');await v.locator('#version-list small').first().waitFor();
  assert.equal(await v.locator('#version-update').count(),0);
  assert.ok((await v.innerText()).includes('Release 20261105 · Up to date'));
  assert.ok((await v.locator('.upkeep-error').innerText()).includes('The last update didn’t finish.'));
  await shot(page,'#settings-version',`version-hosted-failed-${tag}`);
  // Hosted, Search by meaning off on 4 GB: the switch turns it on (Turning on… until the Machine reports it)
  await open('hosted','model');const m=page.locator('#settings-meaning');await m.locator('#meaning-switch').waitFor();
  assert.equal(await m.locator('h3').innerText(),'Search by meaning');
  assert.equal(await m.locator('#meaning-switch').getAttribute('aria-checked'),'false');
  assert.ok((await m.innerText()).includes('A small AI on your own Machine does it. Nothing is sent anywhere.'));
  assert.ok((await m.innerText()).includes('It uses about half a gigabyte of your 4 GB, so a busy Machine can slow down.'));
  await m.scrollIntoViewIfNeeded();assert.ok(await fits(page,'#settings-meaning'),tag);await shot(page,'#settings-meaning',`meaning-hosted-off-${tag}`);
  await m.locator('#meaning-switch').click();await m.locator('#meaning-switch[aria-checked="true"]').waitFor();
  assert.deepEqual(calls.filter(c=>c[0]==='meaning').at(-1),['meaning',true]);
  assert.equal(await m.locator('#meaning-list strong').innerText(),'Turning on…');
  await shot(page,'#settings-meaning',`meaning-hosted-turning-on-${tag}`);
  meaning={...meaning,on:true,want:true,note:'first'};await open('hosted','model');await m.locator('#meaning-switch[aria-checked="true"]').waitFor();
  assert.equal(await m.locator('#meaning-list strong').innerText(),'On');
  assert.ok((await m.innerText()).includes('Reading your notes and conversations for the first time…'));
  await shot(page,'#settings-meaning',`meaning-hosted-on-${tag}`);
  // A control plane that doesn't send them yet: neither shows (its Overview still has them)
  await open('hosted-old','general');await page.waitForTimeout(300);
  assert.ok(await v.isHidden());assert.ok(await m.isHidden());
  // Self-hosted: the release it runs, read-only, and the embeddings block's state with where to change it
  await open('selfhosted','general');await v.locator('#version-list small').waitFor();
  assert.equal(await v.locator('#version-list small').innerText(),'Release 20261105');
  assert.equal(await v.locator('button').count(),0);
  await shot(page,'#settings-version',`version-selfhosted-${tag}`);
  await open('selfhosted','model');await m.locator('#meaning-list strong').waitFor();
  assert.equal(await m.locator('#meaning-list strong').innerText(),'On');
  assert.equal(await m.locator('#meaning-switch').count(),0);
  assert.ok(await m.locator('#meaning-private').isHidden());  // its config may point anywhere: no "nothing is sent" promise
  assert.ok((await m.innerText()).includes('Change it in config.json (embeddings) on this computer.'));
  await shot(page,'#settings-meaning',`meaning-selfhosted-${tag}`);
  await open('selfhosted-dev','general');await page.waitForTimeout(200);
  assert.ok(await v.isHidden());  // not a release: nothing to say
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('settings upkeep ok');
}finally{await browser?.close();server.close()}
