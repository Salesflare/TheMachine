import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFileSync} from 'node:fs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Settings, General, Export (dashboard/settings-export.js, machine/app/export.py): one section with a row per way out
// (EXPORT_OPTIONS: Everything, then Knowledge for another AI with its two switches and passphrase) and Import below. Self-hosted:
// a passphrase form, the running line, then Download and Delete with the export code, the parts and what is not in it;
// an upload asks its passphrase; once staged, Replace with this export (a short confirm) restarts the Machine with it and
// Settings says Imported after the restart; without a service manager, the commands to run. Hosted: Everything is the account page's
// Export, and a staged import has Import now. At 1440x900, 1440x700 and 390x844, light and dark. Made-up data only.
// Set SHOTS=<dir> for screenshots.
const dashboard=await dashboardPage();
const hours={days:[0,1,2,3,4],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC'};
const parts=[{key:'messages',label:'Messages from all sources',rows:12840,files:3,bytes:9e7},{key:'todos',label:'To-dos, with their history and events',rows:1520,files:0,bytes:0},
 {key:'graph',label:'The Graph: people, organizations and projects',rows:940,files:0,bytes:0},{key:'attachments',label:'Attachments and photos',rows:0,files:212,bytes:4e7},
 {key:'settings',label:'Configuration',rows:0,files:2,bytes:4000}];
const not=[{what:'Telegram, Slack and other source tokens',why:'keys and tokens come along only when you include them'},{what:'Phone notifications',why:'each phone signs up with one Machine'}];
const until=new Date(Date.now()+864e5).toISOString();
const ready={state:'ready',id:'exp-example',name:'the-machine-export-2026-11-06.tar.gz.enc',bytes:13e7,size:'124.0 MB',until,includes_keys:false,parts,not_exported:not,with_code:true,code:'ABCD-EFGH-JKMN-PQRS-TUVW'};
const commands=['assistant service stop','assistant import --staged --force','assistant service start'];
const stagedImport={state:'staged',created_at:'2026-11-03T10:00:00+00:00',source:'local',includes_keys:false,parts,not_exported:not,replaces:true};
const views={
 idle:{hosted:false,export:null,import:null,commands},
 running:{hosted:false,export:{state:'running',started_at:new Date().toISOString(),bytes:4.2e7,size:'40.1 MB'},import:null,commands},
 ready:{hosted:false,export:ready,import:null,commands},
 uploaded:{hosted:false,export:null,import:{state:'uploaded',name:'the-machine-export-2026-11-03.tar.gz.enc',bytes:9e7,size:'85.8 MB',error:'Wrong passphrase or export code'},commands},
 staged:{hosted:false,export:null,import:stagedImport,commands,restart:true},
 'staged-commands':{hosted:false,export:null,import:stagedImport,commands,restart:false},
 'staged-failed':{hosted:false,export:null,import:{...stagedImport,error:'The import didn’t go through. The export is still here to try again.'},commands,restart:true},
 confirmed:{hosted:false,export:null,import:{...stagedImport,state:'confirmed'},commands,restart:true},
 imported:{hosted:false,export:null,import:{state:'imported',at:new Date().toISOString(),created_at:'2026-11-03T10:00:00+00:00',source:'local',sends:2,boards:1,reconnect:3},commands,restart:true},
 hosted:{hosted:true,export:null,import:null},
 'hosted-staged':{hosted:true,export:null,import:{...stagedImport,replaces:false}},
 'hosted-confirmed':{hosted:true,export:null,import:{...stagedImport,state:'confirmed',replaces:false}},
};
let mode='idle';const calls=[];let uploaded=0,polls=0;
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');let body='';
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 // The header's robot, as the Machine serves it (assistant.py BRAND_ASSETS), so the shots show it and not a broken image
 const brand={'/brand/avatar.png':'brand/app-icon-192.png','/brand/avatar-blink.png':'brand/avatar-blink.png'}[url.pathname];
 if(brand){res.setHeader('Content-Type','image/png');res.end(readFileSync(new URL('../'+brand,import.meta.url)));return}
 res.setHeader('Content-Type','application/json');
 if(url.pathname==='/api/import-upload'){for await(const c of req)uploaded+=c.length;calls.push(['upload',req.headers['x-file-name'],!!req.headers['x-csrf-token']]);mode='uploaded';res.end(JSON.stringify(views.uploaded));return}
 if(url.pathname==='/api/knowledge-export'){calls.push(['knowledge-download',url.searchParams.get('token')]);res.setHeader('Content-Type','application/zip');res.end('PK made-up');return}
 if(url.pathname==='/api/action'){for await(const c of req)body+=c;const r=JSON.parse(body);calls.push([r.action,r.args]);
  if(r.action==='knowledge_export'){res.end(JSON.stringify({token:'tok-example',name:'the-machine-knowledge-2026-11-06.zip'}));return}
  if(r.action==='export_start'){mode='running';res.end(JSON.stringify({started:true,export:views.running.export}));return}
  if(r.action==='export_delete'||r.action==='import_discard')mode=mode.startsWith('hosted')?'hosted':'idle';
  if(r.action==='import_confirm'){if(mode.startsWith('hosted'))mode='hosted-confirmed';else{mode='confirmed';polls=0;res.end(JSON.stringify({...views.confirmed,restarting:true}));return}}
  // Self-hosted, confirmed: the Machine restarts (one status that doesn't answer), then it says Imported
  if(r.action==='export_status'&&mode==='confirmed'&&++polls>=1){if(polls===1){res.statusCode=503;res.end(JSON.stringify({error:'restarting'}));return}mode='imported'}
  if(r.action==='import_stage')mode='staged';
  if(/^(export|import)_/.test(r.action)){res.end(JSON.stringify(views[mode]));return}
  res.end('{}');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],hours,
  skills:{skills:[],waiting:0,targets:[],folder:'skills/the-machine'},model_usage:[],model_status:{model:'openai/example-model',provider:'openai',windows:[],checked_at:new Date().toISOString()},
  ...(mode.startsWith('hosted')?{manage_url:'https://account.example/setup',account_url:'https://account.example/account'}:{})}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const shot=async(page,name)=>{if(process.env.SHOTS)await page.locator('#settings-export').screenshot({path:`${process.env.SHOTS}/${name}.png`})};
// Every button, link, field and command block sits inside the section's list (and the page), never cut off at its edge
const fits=page=>page.evaluate(()=>{const box=document.querySelector('#export-list').getBoundingClientRect();return document.documentElement.scrollWidth<=innerWidth&&[...document.querySelectorAll('#settings-export :is(button,a,input,pre)')].every(b=>{const x=b.getBoundingClientRect();return!x.width||x.right<=Math.min(innerWidth,box.right)+0.5&&x.left>=box.left-0.5})});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[1440,700],[390,844]])for(const scheme of ['light','dark']){
  const tag=`${width}x${height}-${scheme}`;
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const open=async m=>{mode=m;await page.goto('about:blank');await page.goto(base+'/#settings/general');await page.locator('#export-list [data-export-option="everything"]').waitFor();
   await page.locator('#settings-export').scrollIntoViewIfNeeded()};
  // Before: one section, Everything, Knowledge for another AI and Import
  await open('idle');
  assert.equal(await page.locator('#settings-tabs [aria-selected="true"]').innerText(),'General');
  assert.equal(await page.locator('#settings-export h2').innerText(),'Export');
  assert.deepEqual(await page.locator('#export-list [data-export-option] > .grow > strong').allInnerTexts(),['Everything','Knowledge for another AI']);
  assert.equal(await page.evaluate(()=>EXPORT_OPTIONS.map(o=>o.id).join()),'everything,knowledge');
  assert.equal(await page.locator('[data-export-option="knowledge"] a.learn').getAttribute('href'),'https://themachine.computer/help/knowledge-export');
  // One row pattern, also on a phone: words left, the button right of them (Export as Import's Choose file)
  assert.deepEqual(await page.locator('#export-list>div:has(>.grow)').evaluateAll(rs=>rs.map(r=>{const t=r.querySelector('.grow').getBoundingClientRect(),b=r.querySelector(':scope>button,:scope>a,:scope>form');if(!b)return 'none';const x=b.getBoundingClientRect();return x.left>=t.right-1&&x.top<t.bottom})),[true,true,true],tag);
  // Knowledge for another AI: Export opens two switches (off) and a passphrase; Download packs it and fetches it by token
  await page.locator('[data-export-go="knowledge:toggle"]').click();
  assert.deepEqual(await page.locator('[data-export-go^="knowledge:"][role=switch]').evaluateAll(b=>b.map(x=>x.getAttribute('aria-checked'))),['false','false']);
  assert.ok(await fits(page),tag);await shot(page,`export-knowledge-${tag}`);
  await page.locator('[data-export-go="knowledge:messages"]').click();
  assert.equal(await page.locator('[data-export-go="knowledge:messages"]').getAttribute('aria-checked'),'true');
  await page.locator('#knowledge-pass').fill('short');await page.locator('[data-export-go="knowledge:download"]').click();
  await page.locator('#export-list',{hasText:'Pick a passphrase of at least 10 characters, or none.'}).waitFor();
  await page.locator('#knowledge-pass').fill('');
  const [dl]=await Promise.all([page.waitForEvent('download'),page.locator('[data-export-go="knowledge:download"]').click()]);
  assert.equal(dl.suggestedFilename(),'the-machine-knowledge-2026-11-06.zip');
  await page.locator('#export-list',{hasText:'Downloaded.'}).waitFor();
  assert.deepEqual(calls.find(c=>c[0]==='knowledge_export')[1],{messages:true,private:false,passphrase:''});
  assert.ok(calls.some(c=>c[0]==='knowledge-download'&&c[1]==='tok-example'));
  await page.locator('[data-export-go="knowledge:toggle"]').click();
  assert.equal(await page.locator('#knowledge-pass').count(),0);
  assert.ok((await page.locator('#export-list').innerText()).includes('Bring in an export from another Machine.'));
  assert.ok(await fits(page),tag);await shot(page,`export-before-${tag}`);
  // Export: the form, keys refused without a passphrase, then a start
  await page.locator('[data-export-go="everything:form"]').click();await page.locator('#export-form').waitFor();
  assert.ok(await fits(page),tag);await shot(page,`export-form-${tag}`);
  const starts=calls.filter(c=>c[0]==='export_start').length;
  await page.locator('#export-keys').check();await page.locator('#export-form [type=submit]').click();
  await page.locator('#notice',{hasText:'Keys and tokens need a passphrase you pick.'}).waitFor();
  assert.equal(calls.filter(c=>c[0]==='export_start').length,starts);
  await page.locator('#export-keys').uncheck();await page.locator('#export-form [type=submit]').click();
  await page.locator('#export-list',{hasText:'Exporting… 40.1 MB so far.'}).waitFor();
  assert.deepEqual(calls.filter(c=>c[0]==='export_start').at(-1)[1],{passphrase:null,keys:false});
  await shot(page,`export-running-${tag}`);
  // Done: Download (its id), Delete, the export code once, the parts with counts, and what is not in it
  await open('ready');await page.locator('[data-export-download]').waitFor();
  assert.equal(await page.locator('[data-export-download]').getAttribute('href'),'api/export-download?id=exp-example');
  assert.equal(await page.locator('.export-code code').innerText(),'ABCD-EFGH-JKMN-PQRS-TUVW');
  const list=await page.locator('#export-list').innerText();
  for(const bit of ['Ready, 124.0 MB. Kept until','Messages from all sources','12,840 items','212 files','In it'])assert.ok(list.includes(bit),bit);
  assert.ok(!/—/.test(list)&&!/\bcard/i.test(list));
  await page.locator('.export-not summary').click();
  assert.ok((await page.locator('.export-not').innerText()).includes('signs up with one Machine'));
  assert.ok(await fits(page),tag);await shot(page,`export-ready-${tag}`);
  await page.locator('[data-export-go="everything:delete"]').click();await page.locator('[data-export-go="everything:form"]').waitFor();
  // Import: a file goes up as it is, then its passphrase; a wrong one says so
  await open('idle');
  await page.setInputFiles('#import-file',{name:'the-machine-export-2026-11-03.tar.gz.enc',mimeType:'application/octet-stream',buffer:Buffer.alloc(4096,1)});
  await page.locator('#import-form').waitFor();
  assert.deepEqual(calls.filter(c=>c[0]==='upload').at(-1),['upload','the-machine-export-2026-11-03.tar.gz.enc',true]);
  assert.ok((await page.locator('#import-form').innerText()).includes('Wrong passphrase or export code'));
  assert.ok(await fits(page),tag);await shot(page,`import-uploaded-${tag}`);
  const confirmsBefore=calls.length;
  await page.locator('#import-pass').fill('ABCD-EFGH-JKMN-PQRS-TUVW');await page.locator('#import-form [type=submit]').click();
  // Staged, self-hosted: Replace with this export, a short confirm, then the Machine restarts with it and says Imported
  const ask=page.locator('[data-import-ask="yes"]');await ask.waitFor();
  assert.equal(await ask.innerText(),'Replace with this export');
  assert.equal(await page.locator('.export-commands').count(),0);
  assert.ok(await fits(page),tag);await shot(page,`import-staged-selfhosted-${tag}`);
  await ask.click();await page.locator('.export-ask').waitFor();
  assert.ok((await page.locator('.export-ask').innerText()).includes('It replaces what this Machine has now. A copy of that is kept first.'));
  assert.ok(await fits(page),tag);await shot(page,`import-confirm-selfhosted-${tag}`);
  await page.locator('[data-import-ask="no"]').click();await ask.waitFor();
  assert.ok(!calls.some(c=>c[0]==='import_confirm'&&calls.indexOf(c)>=confirmsBefore));
  await ask.click();await page.locator('.export-ask [data-import-confirm]').click();
  await page.locator('#export-list',{hasText:'Importing. The Machine restarts with it in a minute or two.'}).waitFor();
  assert.ok(await fits(page),tag);await shot(page,`import-confirming-selfhosted-${tag}`);
  await page.locator('[data-import-done]').waitFor({timeout:20000});
  const done=await page.locator('#export-list').innerText();
  for(const line of ['Imported','The export from','is in place.','Some sources need you to sign in again.','2 sends that were waiting are held.','Follow-ups are paused on 1 board.'])assert.ok(done.includes(line),line+' in '+done);
  assert.ok(await fits(page),tag);await shot(page,`import-imported-selfhosted-${tag}`);
  await page.locator('[data-import-done] [data-import-discard]').click();await page.locator('[data-import-pick]').waitFor();
  // Without a service manager: the commands; an import that didn't go through says so and can be tried again
  await open('staged-commands');await page.locator('.export-commands').waitFor();
  assert.equal(await page.locator('.export-commands').innerText(),commands.join('\n'));
  assert.equal(await page.locator('[data-import-confirm],[data-import-ask]').count(),0);
  await open('staged-failed');
  assert.ok((await page.locator('.export-error[role=alert]').innerText()).includes('The import didn’t go through.'));
  assert.equal(await page.locator('[data-import-ask="yes"]').count(),1);
  // Hosted: Everything is the account page's Export (a hop in this tab); a staged import has Import now
  await open('hosted');
  assert.equal(await page.locator('[data-export-option="everything"] form[action="/_machine/account-hop"] [name=to]').inputValue(),'data');
  assert.equal(await page.locator('#export-form,[data-export-go="everything:form"]').count(),0);
  assert.ok(await fits(page),tag);await shot(page,`export-hosted-${tag}`);
  await open('hosted-staged');await page.locator('[data-import-confirm]').click();
  await page.locator('#export-list',{hasText:'Importing. The Machine restarts with it in a few minutes.'}).waitFor();
  assert.equal(calls.at(-1)[0],'import_confirm');
  await shot(page,`import-confirmed-hosted-${tag}`);
  await open('hosted-staged');assert.ok(await fits(page),tag);await shot(page,`import-staged-hosted-${tag}`);
  await context.close();
 }
 assert.ok(uploaded>=4096);
 assert.deepEqual(errors,[]);
 console.log('export dashboard ok');
}finally{await browser?.close();server.close()}
