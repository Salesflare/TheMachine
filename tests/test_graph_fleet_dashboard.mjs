import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Fleet members in the Graph: a marker on their row and detail ("Has a Machine · Work Fleet"), their Fleet name with
// Keep, See in Fleet and Ask your Fleet; the Fleet tab links back to them. No sideways scroll at 390 and 1280.
// GRAPH_FLEET_SHOTS=<prefix> saves screenshots.
const dashboard=await dashboardPage();
const FL='fl_'+'a'.repeat(16),FR='fr_'+'b'.repeat(16),at='2026-10-20T08:00:00+00:00',day=new Date().toISOString().slice(0,10);
const fleetMark={machine:true,named:true,name:'Kim Lee-Park',in:[{kind:'work',label:'Work Fleet',fleet:FL,fleet_name:'Acme',member_id:'fm_kim'},{kind:'friends',label:'Friend',fleet:FR,fleet_name:'Friends',member_id:'fp_kim'}]};
let kim={id:'email:kim@acme.example',kind:'person',name:'Kim Lee-Park',name_from_messages:'kim',strength:3.2,closeness:'close',last_at:day,signals:9,ids:['Slack','kim@acme.example'],
 role:'software developer',role_by:'review',fleet:fleetMark,links:[],open:{you_promised:[],they_promised:[],cards:[],facts:[]},recent:[],around:[]};
const pat={id:'email:pat@client.example',kind:'person',name:'Pat Client',strength:1.2,closeness:'regular',last_at:day,signals:4,ids:['pat@client.example']};
// A long name next to two groups: the pill is never cut; on a phone it moves to the start of the line under the name, which keeps its width. Found on the Network, in no Fleet: no pill, still "Has a Machine".
const alex={id:'email:alex@acme.example',kind:'person',name:'Alexandra-Ionela Constantinescu-Vandenberghe',strength:2.8,closeness:'close',last_at:day,signals:7,ids:['alex@acme.example'],role:'software developer',
 fleet:{machine:true,name:null,in:[{kind:'work',label:'Work Fleet',fleet:FL,fleet_name:'Acme',member_id:'fm_alex'},{kind:'friends',label:'Friend',fleet:FR,fleet_name:'Friends',member_id:'fp_alex'}]}};
const nia={id:'email:nia@studio.example',kind:'person',name:'Nia North',strength:2.1,closeness:'close',last_at:day,signals:5,ids:['nia@studio.example'],role:'board member',
 fleet:{machine:true,in:[],name:null,network:{email:'nia@studio.example',hint:'personal',requested:false,can_add:true}},links:[],open:{you_promised:[],they_promised:[],cards:[],facts:[]},recent:[],around:[]};
// Someone with no Machine the owner knows of: Invite to The Machine, the words to copy or open in email, and the Family invite
const sky={id:'email:sky@home.example',kind:'person',name:'Sky Rivers',strength:1.6,closeness:'regular',last_at:day,signals:3,ids:['sky@home.example'],side:'personal',
 invite:{name:'Sky Rivers',first:'Sky',email:'sky@home.example',family:{email:'sky@home.example',name:'Sky Rivers',url:'https://cp.example/account?tab=fleet&invite=family&to=sky%40home.example&name=Sky+Rivers#fleet'}},
 links:[],open:{you_promised:[],they_promised:[],cards:[],facts:[]},recent:[],around:[]};
const rules=()=>({relationships:{rule:'ask',details:false}});
const view={on:true,ask_meetings:false,brief:{every:'off',tell:false},kinds:{relationships:'who knows someone'},kind_rules:{relationships:['ask','always','never']},
 no_details:[],scoped:[],scopes:{},intro_offers:[],waiting:[],asked:[],log:[],notices:[],free:[],briefs:{},
 fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:['relationships','anything'],
   people:[{member_id:'fm_me',name:'Sam Doe',role:'owner',me:true,answers_with:'Self-hosted: Desk',email:'sam@acme.example'},
    {member_id:'fm_kim',name:'Kim Lee-Park',role:'member',answers_with:'Hosted: kim.example.test',email:'kim@acme.example',graph_node:'email:kim@acme.example'}],
   members:[{member_id:'fm_kim',name:'Kim Lee-Park',rules:rules()}],rules:rules(),exceptions:{}}],friends:null};
const calls=[],errors=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0}}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('node')===nia.id?nia:url.searchParams.get('node')===sky.id?sky:url.searchParams.get('node')?kim:{projects:[],people:[kim,alex,nia,pat,sky],quiet:[],new:[],orgs:[]}));return}
 if(url.pathname==='/api/fleet'){res.end(JSON.stringify(view));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='fleet_network')nia.fleet.network={...nia.fleet.network,requested:true,can_add:false};  // what the Machine says once it is sent
  if(call.action==='graph_rename'){kim={...kim,name:call.args.name,fleet:{...fleetMark,named:false}};delete kim.name_from_messages;res.end(JSON.stringify({node_id:kim.id,name:call.args.name}));return}res.end('{}');return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 await navClick(page.locator('nav [data-tab="people"]'));
 const row=page.locator('#people-view article[data-node="email:kim@acme.example"]');await row.waitFor();
 assert.equal(await row.locator('.fleet-chip-row').textContent(),'Fleet · Friend');
 assert.equal(await row.locator('.fleet-chip-row').getAttribute('title'),'Has a Machine · Work Fleet (Acme) · Friend');
 const shown=async r=>r.evaluate(a=>[...a.querySelectorAll('.fleet-chip')].filter(c=>c.getClientRects().length).map(c=>({where:c.classList.contains('fleet-chip-sub')?'sub':'row',
  whole:c.querySelector('.ct').scrollWidth<=c.querySelector('.ct').clientWidth&&c.getBoundingClientRect().right<=a.getBoundingClientRect().right,first:c.parentElement.firstElementChild===c})));
 const long=page.locator('#people-view article[data-node="email:alex@acme.example"]');
 for(const width of [320,390,1280]){await page.setViewportSize({width,height:844});
  for(const r of [row,long])assert.deepEqual(await shown(r),[{where:width<=600?'sub':'row',whole:true,first:width<=600}],`one whole pill at ${width}`);
  assert.ok(await row.locator('button.node').evaluate(b=>b.scrollWidth<=b.clientWidth),`a short name is whole at ${width}`);
  if(width<=600)assert.match(await row.locator('.graph-sub').textContent(),/^Fleet · FriendHas a Machine · /)}
 await page.setViewportSize({width:390,height:844});
 const found=page.locator('#people-view article[data-node="email:nia@studio.example"]');
 assert.equal(await found.locator('.fleet-chip').count(),0);  // in no Fleet: no empty pill
 assert.match(await found.locator('.graph-sub').textContent(),/^Has a Machine · Board member/);
 assert.match(await row.locator('.graph-sub').textContent(),/^Fleet · FriendHas a Machine · Software developer/);
 const pat=page.locator('#people-view article[data-node="email:pat@client.example"] .graph-sub');  // their addresses in the text's own font, not code
 assert.equal(await pat.locator('.mono').count(),0);assert.match(await pat.textContent(),/ · pat@client\.example$/);
 assert.equal(await page.locator('#people-view article[data-node="email:pat@client.example"] .fleet-chip').count(),0);
 const fits=async label=>{for(const width of [390,1280]){await page.setViewportSize({width,height:844});
  const s=await page.evaluate(()=>({page:document.documentElement.scrollWidth,viewport:innerWidth}));assert.ok(s.page<=s.viewport,`overflow at ${width} (${label})`);
  if(process.env.GRAPH_FLEET_SHOTS)for(const scheme of ['light','dark']){await page.emulateMedia({colorScheme:scheme});await page.waitForTimeout(500);
   await page.screenshot({path:`${process.env.GRAPH_FLEET_SHOTS}-${label}-${width}-${scheme}.png`,fullPage:true})}await page.emulateMedia({colorScheme:'light'})}await page.setViewportSize({width:390,height:844})};
 await fits('list');
 await row.locator('button.node').click();
 await page.locator('.fleet-mark').waitFor();
 assert.equal(await page.locator('.fleet-mark').textContent(),'Work Fleet (Acme) · Friend · Has a Machine');
 assert.match(await page.locator('#people-view').textContent(),/NameFrom your Fleet\. Your messages say “kim”\./);
 assert.equal(await page.locator('[data-fleet-ask]').count(),0);
 await page.setViewportSize({width:320,height:844});for(const sel of ['.fleet-mark','.fleet-named'])assert.ok(await page.locator(sel).evaluate(e=>e.scrollWidth<=e.clientWidth),sel+' wraps');await page.setViewportSize({width:390,height:844});  // no "who knows" for a teammate
 await fits('detail');
 await page.locator('[data-fleet-keep]').click();
 for(let i=0;i<100&&!calls.length;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls[0],{action:'graph_rename',args:{node_id:'email:kim@acme.example',name:'Kim Lee-Park'}});
 await page.waitForFunction(()=>!document.querySelector('[data-fleet-keep]'));
 await page.locator('[data-fleet-member="fm_kim"]').click();
 await page.locator('#fleet-m-fm_kim.flash').waitFor();
 assert.ok(await page.locator('#fleet-m-fm_kim').isVisible());
 await fits('fleet');
 const link=page.locator('#fleet-m-fm_kim [data-graph-open]');  // a quiet muted text link, not a bordered button
 assert.equal(await link.evaluate(e=>e.tagName),'A');assert.equal(await link.getAttribute('aria-label'),'Open Kim Lee-Park in your Graph');
 assert.equal(await link.evaluate(e=>getComputedStyle(e).borderStyle),'none');
 assert.ok(await link.evaluate(e=>e.getBoundingClientRect().height<24),'small');
 await link.click();
 await page.locator('.fleet-mark').waitFor();
 assert.equal(await page.locator('.graph-detail h3').textContent(),'Kim Lee-Park');
 await page.locator('[data-fleet-free]').click();
 await page.waitForFunction(()=>document.activeElement?.closest('.fleet-free-form'));
 await page.evaluate(()=>{location.hash='#people'});await page.locator('#people-view article[data-node="email:nia@studio.example"] button.node').click();
 await page.waitForFunction(()=>document.querySelector('.graph-detail h3')?.textContent==='Nia North');
 assert.equal(await page.locator('.person-about .fleet-mark').textContent(),'Has a Machine');  // found on the Network: said, with no Fleet buttons
 assert.equal(await page.locator('.person-about [data-fleet-member]').count(),0);
 assert.equal(await page.locator('.person-about [data-person-friend="friend"]').textContent(),'Add as a friend');  // in sight, next to "Has a Machine"
 assert.equal(await page.locator('[data-machine-invite]').count(),0);  // has a Machine: nothing to invite to
 const menu=page.locator('.person-page .person-menu');await menu.locator('summary').click();
 assert.deepEqual((await menu.locator('[data-person-friend]').allTextContents()),['Add as family']);  // Family in ⋯, like the Suggestions card's choice
 if(process.env.GRAPH_FLEET_SHOTS)for(const width of [390,1280])for(const scheme of ['light','dark']){await page.setViewportSize({width,height:844});await page.emulateMedia({colorScheme:scheme});await page.waitForTimeout(500);
  await page.screenshot({path:`${process.env.GRAPH_FLEET_SHOTS}-friend-${width}-${scheme}.png`})}
 await page.emulateMedia({colorScheme:'light'});await page.setViewportSize({width:390,height:844});
 const sent=calls.length;await menu.locator('[data-person-friend="family"]').click();
 for(let i=0;i<100&&calls.length===sent;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls[sent],{action:'fleet_network',args:{do:'connect',email:'nia@studio.example',relation:'family'}});
 await page.waitForFunction(()=>document.querySelector('.person-about .fleet-mark')?.textContent==='Has a Machine · Friend request sent');
 assert.equal(await page.locator('[data-person-friend]').count(),0);
 await page.waitForTimeout(800);assert.equal(await page.locator('.person-about .fleet-mark').textContent(),'Has a Machine · Friend request sent');  // still after the refresh
 await fits('network');
 // opened again later: said, nothing to press
 await page.evaluate(()=>{location.hash='#people'});await page.locator('#people-view article[data-node="email:nia@studio.example"] button.node').click();
 await page.waitForFunction(()=>document.querySelector('.person-about .fleet-mark')?.textContent==='Has a Machine · Friend request sent');
 await page.locator('.person-page .person-menu summary').click();assert.equal(await page.locator('[data-person-friend]').count(),0);
 await page.locator('.person-page .person-menu summary').click();
 assert.equal(await page.locator('[data-person-friend]').count(),0);
 // No Machine found: Invite to The Machine shows the words; nothing is sent, Open in email hands them to the owner's own mail app
 await page.evaluate(()=>{location.hash='#people'});await page.locator('#people-view article[data-node="email:sky@home.example"] button.node').click();
 await page.waitForFunction(()=>document.querySelector('.graph-detail h3')?.textContent==='Sky Rivers');
 assert.equal(await page.locator('.person-about .fleet-mark').textContent(),'No Machine found');
 assert.equal(await page.locator('[data-person-friend]').count(),0);
 const before=calls.length;await page.locator('[data-machine-invite]').click();
 const dialog=page.locator('#machine-invite[open]');await dialog.waitFor();
 assert.equal(await dialog.locator('h2').textContent(),'Invite Sky to The Machine');
 assert.match(await dialog.locator('.mi-preview').textContent(),/To: sky@home\.exampleSubject: Have a look at The MachineHi Sky,I use The Machine, .*https:\/\/themachine\.computer$/);
 const mail=await dialog.locator('[data-mi-mail]').getAttribute('data-mi-mail');
 assert.ok(mail.startsWith('mailto:sky%40home.example?subject=Have%20a%20look%20at%20The%20Machine&body=Hi%20Sky%2C'),mail);
 assert.equal(await dialog.locator('.mi-family a').getAttribute('href'),sky.invite.family.url);  // the account page's Family invite, prefilled
 if(process.env.GRAPH_FLEET_SHOTS)for(const width of [390,1440])for(const scheme of ['light','dark']){await page.setViewportSize({width,height:width<500?844:900});await page.emulateMedia({colorScheme:scheme});await page.waitForTimeout(400);
  await page.screenshot({path:`${process.env.GRAPH_FLEET_SHOTS}-invite-dialog-${width}-${scheme}.png`})}
 await page.emulateMedia({colorScheme:'light'});await page.setViewportSize({width:390,height:844});
 await dialog.locator('[data-mi-close]').click();await page.waitForFunction(()=>!document.querySelector('#machine-invite').open);
 assert.equal(calls.length,before);  // nothing went anywhere
 if(process.env.GRAPH_FLEET_SHOTS)for(const width of [390,1440])for(const scheme of ['light','dark']){await page.setViewportSize({width,height:width<500?844:900});await page.emulateMedia({colorScheme:scheme});await page.waitForTimeout(400);
  await page.locator('.person-about').scrollIntoViewIfNeeded();await page.screenshot({path:`${process.env.GRAPH_FLEET_SHOTS}-invite-${width}-${scheme}.png`})}
 await page.emulateMedia({colorScheme:'light'});await page.setViewportSize({width:390,height:844});
 await fits('invite');
 // With a mailbox that can send: the words to change, and Send through the owner's mailbox (person_invite_send), only on Send
 sky.invite.from='owner@home.example';
 await page.evaluate(()=>{location.hash='#people'});await page.locator('#people-view article[data-node="email:sky@home.example"] button.node').click();
 await page.waitForFunction(()=>document.querySelector('.graph-detail h3')?.textContent==='Sky Rivers');
 await page.locator('[data-machine-invite]').click();await dialog.waitFor();
 assert.equal(await dialog.locator('.fleet-fine').first().textContent(),'From owner@home.example. Nothing goes out until you press Send.');
 assert.equal(await dialog.locator('[data-mi-to]').inputValue(),'sky@home.example');
 assert.equal(await dialog.locator('[data-mi-subject]').inputValue(),'Have a look at The Machine');
 assert.match(await dialog.locator('[data-mi-body]').inputValue(),/^Hi Sky,\n\nI use The Machine, .*https:\/\/themachine\.computer$/);
 assert.equal(await dialog.locator('[data-mi-mail]').count(),0);  // it sends itself: no Open in email
 assert.deepEqual(await dialog.locator('.ed-actions button').allTextContents(),['Copy','Send']);
 if(process.env.GRAPH_FLEET_SHOTS)for(const width of [390,1440])for(const scheme of ['light','dark']){await page.setViewportSize({width,height:width<500?844:900});await page.emulateMedia({colorScheme:scheme});await page.waitForTimeout(400);
  await page.screenshot({path:`${process.env.GRAPH_FLEET_SHOTS}-invite-send-${width}-${scheme}.png`})}
 await page.emulateMedia({colorScheme:'light'});await page.setViewportSize({width:390,height:844});
 assert.equal(calls.length,before);  // opening it sent nothing
 await dialog.locator('[data-mi-body]').fill('Hi Sky,\n\nYou should try this.');
 await dialog.locator('[data-mi-send]').click();await page.waitForFunction(()=>!document.querySelector('#machine-invite').open);
 const send=calls.find(c=>c.action==='person_invite_send');
 assert.deepEqual({...send.args,approval_id:typeof send.args.approval_id},{node_id:sky.id,to:'sky@home.example',subject:'Have a look at The Machine',
  body:'Hi Sky,\n\nYou should try this.',approval_id:'string'});
 assert.deepEqual(errors,[]);
 console.log('graph fleet dashboard ok');
}finally{await browser?.close();server.close()}
