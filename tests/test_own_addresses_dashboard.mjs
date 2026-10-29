import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, Account, Your addresses (own_addresses.py): the owner's addresses with where each came from, Remove on the
// ones found (never on a connected account), and the maybes with three choices, none picked for them: Mine, The team's
// and Not mine, each with what it changes. A chosen one moves to its list and keeps Change on its row. One tap, then
// the list as the service returns it. In Dutch too (the reasons and choices read translated), and at 390px nothing
// leaves the screen.
const dashboard=await dashboardPage();
const nl=await readFile(new URL('../i18n/nl.json',import.meta.url),'utf8'),en=await readFile(new URL('../i18n/en.json',import.meta.url),'utf8');
const hours={days:[0,1,2,3,4],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC',saveable:true};
const languages={en:'English',nl:'Nederlands'};
const yours=[{address:'sam@acme.example',sources:['Connected account','Slack profile'],removable:false},
 {address:'sam.lee@acme-labs.example',sources:['Gmail alias','Your calendar'],removable:true},
 {address:'samuel.lee.longer.address@subsidiary.acme-international.example',sources:['Gmail alias'],removable:true}];
let addresses,posted=[],lang='en';
const reset=()=>{addresses={yours:[...yours],maybe:[{address:'partnerships@acme.example',sources:['Gmail alias'],why:'Looks like a team address'},
 {address:'support@acme.example',sources:['Gmail send-as','Mail you sent'],why:'Looks like a team address'}],team:[],not_mine:[],
 domains:[{domain:'acme.example',added:false}]};posted=[]};
// The service's own moves (own_addresses.view): a choice takes the address out of every list and into its own
function choose({address,choice}){const all=[...addresses.yours,...addresses.maybe,...addresses.team,...addresses.not_mine],a=all.find(x=>x.address===address);
 const out=x=>x.filter(y=>y.address!==address),plain={address,sources:a.sources.filter(s=>s!=='You confirmed it'),choice};
 addresses={yours:out(addresses.yours),maybe:out(addresses.maybe),team:out(addresses.team),not_mine:out(addresses.not_mine),domains:addresses.domains};
 if(choice==='confirm')addresses.yours.push({...plain,sources:[...plain.sources,'You confirmed it'],removable:true});
 else addresses[choice==='team'?'team':'not_mine'].push(plain)}
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/nl.json'){res.end(nl);return}
 if(url.pathname==='/i18n/en.json'){res.end(en);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],hours,own_addresses:addresses,
  locale:{locale:'en-BE',region:'BE',language:lang,language_set:true,clock:'auto',hour12:false,auto_hour12:false,date_locale:lang==='en'?'en-GB':'nl-BE',languages,saveable:true}}));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posted.push([action,args]);
  if(action==='own_address')choose(args);
  if(action==='own_domain')addresses.domains=args.on?[...addresses.domains,{domain:args.domain,added:true}]:addresses.domains.filter(d=>d.domain!==args.domain);res.end(JSON.stringify({own_addresses:addresses}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const shot=async(page,name)=>{if(!process.env.SHOTS)return;
 await page.evaluate(()=>{const m=document.querySelector('#addr-maybe:not([hidden])')||document.querySelector('#addr-team:not([hidden])')||document.querySelector('#settings-addresses');m.scrollIntoView({block:'start'});scrollBy(0,-90)});
 await page.screenshot({path:`${process.env.SHOTS}/${name}.png`})};
const fits=page=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth&&[...document.querySelectorAll('#settings-addresses button')].filter(b=>b.offsetParent).every(b=>{const r=b.getBoundingClientRect();return r.right<=innerWidth&&r.left>=0}));
const pick=(page,list,address,choice)=>page.locator(`${list} [data-addr="${address}"][data-addr-choice="${choice}"]`);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[1440,700],[390,844]]){
  reset();lang='en';
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept());
  await page.goto(base);await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
  await navClick(page.locator('#open-settings'));await page.locator('#settings-tabs [data-settings-tab="account"]:not([hidden])').waitFor();
  assert.equal(await page.locator('#settings-tabs [aria-selected="true"]').innerText(),'Account');
  assert.equal(await page.locator('#settings-addresses').isVisible(),true);
  const rows=await page.locator('#addr-list>div').allInnerTexts();
  assert.equal(rows.length,3);assert.match(rows[0],/sam@acme\.example\s+Connected account · Slack profile/);assert.match(rows[1],/Gmail alias · Your calendar\s+Remove/);
  assert.equal(await page.locator('#addr-list>div').first().locator('button').count(),0);  // a connected account stays
  // Three choices per maybe, each with what it changes, and none picked for the owner
  const first=page.locator('#addr-maybe-list>div').first();
  assert.match(await first.innerText(),/^partnerships@acme\.example\nLooks like a team address · Gmail alias\nMine: only I answer it\nIts mail can become your to-dos\.\nThe team’s: others answer it too\nA shared inbox, like support@\. No to-dos from it\. Its mail still fills in the Graph\.\nNot mine\nIt won’t count as yours\.$/);
  assert.equal(await first.getByRole('radiogroup',{name:'Whose is partnerships@acme.example?'}).count(),1);
  assert.deepEqual(await page.locator('#addr-maybe-list [role="radio"]').evaluateAll(b=>b.map(x=>x.getAttribute('aria-checked'))),Array(6).fill('false'));
  assert.equal(await page.locator('#addr-team').isHidden(),true);
  assert.equal(await fits(page),true);
  await shot(page,`after-choose-${width}x${height}`);
  // Mine for partnerships@, The team's for support@
  await pick(page,'#addr-maybe-list','partnerships@acme.example','confirm').click();
  await page.locator('#addr-list>div',{hasText:'partnerships@acme.example'}).waitFor();
  assert.deepEqual(posted.at(-1),['own_address',{address:'partnerships@acme.example',choice:'confirm'}]);
  assert.match(await page.locator('#addr-list>div',{hasText:'partnerships@acme.example'}).innerText(),/^partnerships@acme\.example\nMine · Gmail alias\nChange$/);
  await pick(page,'#addr-maybe-list','support@acme.example','team').click();
  await page.locator('#addr-team-list>div',{hasText:'support@acme.example'}).waitFor();
  assert.equal(await page.locator('#addr-maybe').isHidden(),true);
  assert.equal(await page.locator('#notice').innerText(),'Marked as the team’s. No to-dos from it.');
  assert.match(await page.locator('#addr-team-list>div').innerText(),/^support@acme\.example\nThe team’s · No to-dos from it · Gmail send-as · Mail you sent\nChange$/);
  assert.equal(await fits(page),true);
  await shot(page,`after-chosen-${width}x${height}`);
  // Change on the row: the three choices again, the current one checked; picking the same one just closes it
  await page.locator('#addr-team-list [data-addr-open]').click();
  assert.equal(await pick(page,'#addr-team-list','support@acme.example','team').getAttribute('aria-checked'),'true');
  assert.equal(await page.evaluate(()=>document.activeElement?.dataset.addrChoice),'confirm');
  assert.equal(await fits(page),true);
  await shot(page,`after-change-${width}x${height}`);
  const before=posted.length;await pick(page,'#addr-team-list','support@acme.example','team').click();
  assert.equal(posted.length,before);assert.equal(await page.locator('#addr-team-list .addr-pick').count(),0);
  await page.locator('#addr-team-list [data-addr-open]').click();await pick(page,'#addr-team-list','support@acme.example','remove').click();
  await page.locator('#addr-not-list>div',{hasText:'support@acme.example'}).waitFor();
  assert.equal(await page.locator('#addr-team').isHidden(),true);
  // Remove on a found one asks first, then it's under Not yours with Change
  await page.locator('#addr-list [data-addr="sam.lee@acme-labs.example"]').click();
  await page.locator('#addr-not-list>div',{hasText:'sam.lee@acme-labs.example'}).waitFor();
  assert.deepEqual(posted.map(p=>p[1].choice),['confirm','team','remove','remove']);
  // Your company's domains: the found one stays; one the owner adds has Remove (a second domain, never a client)
  assert.equal(await page.locator('#settings-domains').isVisible(),true);assert.match(await page.locator('#addr-domain-list').innerText(),/^acme\.example\nFrom your addresses\nAdd$/);
  await page.locator('#addr-domain-form input').fill('acme-two.example');await page.locator('#addr-domain-form button').click();
  await page.locator('#addr-domain-list [data-domain-remove="acme-two.example"]').click();
  await page.locator('#addr-domain-list [data-domain-remove]').waitFor({state:'detached'});
  assert.deepEqual(posted.slice(-2),[['own_domain',{domain:'acme-two.example',on:true}],['own_domain',{domain:'acme-two.example',on:false}]]);
  assert.equal(await fits(page),true);
  await context.close();
 }
 // Dutch and dark, the way the owner reads it: every reason, choice and line translated, and at 390px it all fits
 for(const [width,height] of [[1440,900],[390,844]]){
  reset();lang='nl';
  const context=await browser.newContext({viewport:{width,height},locale:'nl-BE',colorScheme:'dark'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
  await page.locator('html[lang="nl"]').waitFor({state:'attached'}).catch(()=>{});
  await navClick(page.locator('#open-settings'));await page.locator('#addr-maybe-list>div').first().waitFor();
  await page.waitForFunction(()=>/Van mij/.test(document.querySelector('#addr-maybe-list').innerText));
  const text=await page.locator('#addr-maybe-list>div').first().innerText();
  assert.match(text,/Lijkt een teamadres · Gmail-alias\nVan mij: alleen ik beantwoord het\nDe mail ervan kan je to-do's worden\.\nVan het team: anderen beantwoorden het ook\nEen gedeelde inbox, zoals support@\. Geen to-do's ervan\. De mail vult de Graph nog steeds aan\.\nNiet van mij\nHet telt niet als van jou\./);
  assert.equal(await fits(page),true);
  await shot(page,`after-nl-${width}x${height}`);
  await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('own addresses dashboard ok');
}finally{await browser?.close();server.close()}
