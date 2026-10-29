import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Share a contact (contact_share.py): ⋯, Share contact… on a person's page opens a dialog to pick one person and the
// fields that go. A Personal contact keeps Preview off until "Share it anyway" is ticked. Preview shows the exact card,
// and Send carries that preview's digest and only the picked fields. Contacts shared with the owner wait at the top of
// People with Add and Dismiss. Nothing here reaches a real Machine: the server below is a fixture.
const dashboard=await dashboardPage();
const person={id:'email:sam@client.example',kind:'person',name:'Sam Lee',strength:2,last_at:new Date().toISOString(),signals:4,ids:['sam@client.example'],
 side:'personal',side_by:'owner',edited:[],emails:[{value:'sam@client.example',by:'messages'}],phones:[{value:'+15550100',by:'owner'}],profile:{title:'Founder'},
 links:[],recent:[],around:[],open:{},can_share:true};
const options={name:'Sam Lee',emails:['sam@client.example'],phones:['+15550100'],org:'Client Co',role:'Founder',own:false,confirm:'personal',sent:[],
 targets:[{fleet:'f1',member_id:'pat1',name:'Pat',kind:'work',where:'Acme'},{fleet:'fr',member_id:'lou1',name:'Lou (@lou)',kind:'friends',where:'Friends'}]};
const waiting=[{id:'c1',from:'Pat',kind:'work',where:'Work Fleet',existing:null,card:{name:'Rae Moss',emails:['rae@north.example'],note:'Ask about the API'},
 rows:[{label:'Name',value:'Rae Moss'},{label:'Email',value:'rae@north.example'},{label:'Note',value:'Ask about the API'}]}];
let shared=[];const calls=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){res.end(JSON.stringify(url.searchParams.get('node')?person:{projects:[],people:[person],quiet:[],new:[],orgs:[],contacts_in:shared}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='fleet_contact_options'){res.end(JSON.stringify(options));return}
  if(call.action==='fleet_contact_preview'){res.end(JSON.stringify({card:{name:'Sam Lee',emails:call.args.pick.emails},rows:[{label:'Name',value:'Sam Lee'},...call.args.pick.emails.map(value=>({label:'Email',value}))],
   digest:'d1',to:'Pat',kind:'work',where:'Acme',confirm:'personal'}));return}
  if(call.action==='fleet_contact_send'){res.end(JSON.stringify({sent:1,to:'Pat'}));return}
  if(call.action==='fleet_contact_decide'){shared=[];res.end(JSON.stringify({status:'added',name:'Rae Moss'}));return}
  res.end('{}');return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]]){
  calls.length=0;shared=waiting;
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const base='http://127.0.0.1:'+server.address().port+'/';
  await page.goto(base+'#graph/'+encodeURIComponent(person.id));
  await page.locator('#people-view .person-page').waitFor();
  await page.locator('.person-page .person-menu summary').click();
  const item=page.locator('.person-page [data-contact-share]');
  assert.equal(await item.isVisible(),true,'Share contact… in the person menu');
  await item.click();
  const form=page.locator('#contact-share-form');await form.locator('[data-cs-to]').waitFor();
  assert.equal(calls.find(c=>c.action==='fleet_contact_options').args.node,person.id);
  assert.deepEqual(await form.locator('[data-cs-to] option').allTextContents(),['Pat · Acme','Lou (@lou) · Friends']);
  // Personal: Preview waits for the extra tick
  const go=form.locator('button.primary');
  assert.equal(await go.isDisabled(),true,'a Personal contact needs Share it anyway first');
  await form.locator('[data-cs-confirm]').check();
  assert.equal(await go.isDisabled(),false);
  // Only the email (on by default); untick the organization
  await form.locator('[data-cs-field="org"]').uncheck();
  assert.equal(await form.locator('[data-cs-field="phones"]').isChecked(),false,'phones are off unless picked');
  await form.locator('[data-cs-note]').fill('You both sell to clinics');
  await go.click();
  await form.getByText('Pat gets exactly this:').waitFor();
  const preview=calls.find(c=>c.action==='fleet_contact_preview').args;
  assert.deepEqual(preview.pick,{emails:['sam@client.example'],phones:[]});
  assert.equal(preview.note,'You both sell to clinics');
  assert.equal(calls.some(c=>c.action==='fleet_contact_send'),false,'Preview sends nothing');
  await form.locator('button.primary',{hasText:'Send'}).click();
  await page.locator('#toast',{hasText:'Sent to Pat.'}).waitFor();
  const send=calls.find(c=>c.action==='fleet_contact_send').args;
  assert.deepEqual([send.node,send.member_id,send.shown,send.confirmed],[person.id,'pat1','d1',true]);
  assert.deepEqual(send.pick,preview.pick);
  // Shared with you, at the top of People
  await page.goto('about:blank');await page.goto(base+'#graph');  // a fresh load: People reads Shared with you again
  const card=page.locator('.contact-in');await card.waitFor();
  assert.match(await card.textContent(),/Shared by Pat · Work Fleet/);
  assert.match(await card.textContent(),/“Ask about the API”/);
  await card.locator('[data-contact-in="add"]').click();
  await page.locator('#toast',{hasText:'Added Rae Moss.'}).waitFor();
  assert.deepEqual(calls.find(c=>c.action==='fleet_contact_decide').args,{id:'c1',choice:'add'});
  await page.locator('.contact-in').waitFor({state:'detached'});
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  assert.equal(overflow,false,`no sideways scroll at ${width}`);
  assert.deepEqual(errors,[]);
  await context.close();
 }
 console.log('contact share dashboard ok');
}finally{await browser?.close();server.close()}
