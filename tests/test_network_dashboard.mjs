import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Network discovery (discovery.py): a permission card once; a person card under To-dos only with a concrete
// reason; colleague gets Connect, anyone else Friend or Family; the Fleet tab's Network block has the two switches,
// the quiet list and Leave. Never scrolls sideways (390px and 1000px, dark and light).
const dashboard=await dashboardPage();
const FR='fr_'+'b'.repeat(16);
const soon=new Date(Date.now()+3*864e5).toISOString();
const base={on:true,kinds:{},ask_meetings:false,kind_rules:{},no_details:[],scoped:[],scopes:{},
 fleets:[{id:FR,kind:'friends',label:'Friends',name:'Friends',asks:[],people:[{member_id:'fp_me',name:'Sam Doe',me:true}],members:[]}],
 friends:{id:FR,username:'sam',in:[],out:[],blocked:[]},waiting:[],asked:[],log:[],notices:[],splits:[]};
const ask={...base,network:{find:null,discoverable:null,asked:false,last:null,people:[]}};
const found={...base,meet:{allow:'freebusy',minutes:30,buffer:10,prefer:'any',brand:true},network:{find:true,discoverable:true,asked:true,last:'2026-10-20T10:00:00Z',people:[
 {email:'nia@nia.example',username:'nia',name:'Nia North',hint:'personal',role:null,relation:null,status:'new',found_at:'x',reasons:[{kind:'meeting',at:soon,title:'Picnic'}]},
 {email:'sam@acme.example',username:'samb',name:'Sam Beam',hint:'colleague',role:null,relation:null,status:'new',found_at:'x',reasons:[{kind:'card',card:'s1',title:'Send the quote'}]},
 {email:'zed@zed.example',username:'zed',name:'Zed Zee',hint:'personal',role:null,relation:null,status:'new',found_at:'x',reasons:[]}],
 addresses:[{email:'sam@work.example',account:true,on:true,findable:true},{email:'sam.doe-with-a-long-address@personal-mail.example',account:false,on:true,findable:true},
  {email:'sam@other.example',account:false,on:false,findable:false},{email:'info@work.example',account:false,on:false,findable:false,shared:true},
  {email:'+12025550101',account:false,on:true,findable:true,phone:true,source:'whatsapp'},{email:'+12025550100',account:false,on:false,findable:false,phone:true,source:'about_you'}]}};
const calls=[];let shown=ask,answer='{"ok":true}';
const firstCall=async()=>{for(let i=0;i<100&&!calls.length;i++)await new Promise(r=>setTimeout(r,50));return calls[0]};  // the call lands, also on a busy runner
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify({suggestions:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0}}));return}
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;calls.push(JSON.parse(body));res.end(answer);return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(shown));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
 for(const [scheme,width] of [['dark',390],['light',1000]]){
  shown=ask;
  const page=await (await browser.newContext({viewport:{width,height:900},colorScheme:scheme})).newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept());
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.locator('#net-ask').waitFor();
  assert.match(await page.locator('#net-ask').innerText(),/Which of your contacts have a Machine\?/);assert.match(await page.locator("#net-ask").innerText(),/Check my contacts/);
  calls.length=0;await page.locator('#net-ask [data-net-do="find_on"]').click();
  assert.deepEqual(await firstCall(),{action:'fleet_network',args:{do:'find_on',email:'',relation:''}});
  shown=found;await page.reload();await page.locator('#net-nia').waitFor();
  assert.equal(await page.locator('#net-ask').count(),0);
  assert.equal(await page.locator('#net-zed').count(),0);  // no reason, no card
  const nia=await page.locator('#net-nia').innerText();
  assert.match(nia,/Nia North is on the Network/);assert.match(nia,/You meet .*Picnic/);assert.match(nia,/Friend or family/);
  assert.match(await page.locator('#net-samb').innerText(),/Open: Send the quote/);
  assert.equal(await page.locator('#net-samb [data-net-do="connect"]').count(),1);
  calls.length=0;await page.locator('#net-nia [data-net-rel="family"]').click();
  assert.deepEqual(await firstCall(),{action:'fleet_network',args:{do:'connect',email:'nia@nia.example',relation:'family'}});
  // Friends already (their request accepted a moment ago): nothing is sent, and the toast says so
  answer='{"status":"connected","relation":"colleague"}';calls.length=0;await page.locator('#net-samb [data-net-do="connect"]').click();
  await page.locator('#toast.show',{hasText:'Already friends. Nothing was sent.'}).waitFor();answer='{"ok":true}';
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${scheme} ${width}px cards scroll sideways`);
  // Friend, Family, Not now and More share one row, and More is one line (it wrapped as "Mor / e" at 390px)
  assert.deepEqual(await page.evaluate(()=>{const bs=[...document.querySelectorAll('#net-nia .actions>button,#net-nia .actions>.more-actions')];
   return [new Set(bs.map(b=>Math.round(b.getBoundingClientRect().top))).size,document.querySelector('#net-nia .more-actions>summary').getBoundingClientRect().height<50]}),[1,true],`${scheme} ${width}px Network buttons`);
  await navClick(page.locator('nav [data-tab="fleet"]'));await page.locator('[data-fleet-pane="network"]').click();await page.locator('#fleet-network').waitFor();
  const block=page.locator('#fleet-network');
  assert.match(await block.innerText(),/Check which of my contacts have a Machine/);assert.match(await block.innerText(),/Zed Zee/);
  assert.ok(await block.locator('[data-net-toggle="find_off"]').isChecked());
  // Which addresses find them: the sign-in one says Always on (no switch that can't move), each connected one has its switch
  assert.match(await block.locator('.net-addrs').innerText(),/Findable by/);
  const acct=block.locator('.net-addr',{hasText:'sam@work.example'});
  assert.equal(await acct.locator('input').count(),0);assert.match(await acct.innerText(),/Sign-in email/);assert.match(await acct.innerText(),/Always on/);
  assert.equal(await block.locator('[data-net-addr="sam@other.example"]').isChecked(),false);
  assert.equal(await block.locator('[data-net-addr="info@work.example"]').isChecked(),false);  // shared: off unless turned on
  assert.match(await block.locator('.net-addr:has([data-net-addr="info@work.example"])').innerText(),/Shared address/);
  assert.doesNotMatch(await block.locator('.net-addr:has([data-net-addr="sam@other.example"])').innerText(),/Shared address/);
  // The owner's own numbers: each with its switch and where it came from; the main switch says "or number"
  assert.match(await block.locator('.net-switches').innerText(),/Let people who have my email or number find me/);
  assert.match(await block.locator('.net-addr:has([data-net-addr="+12025550101"])').innerText(),/^\s*\+1 202 555 0101\s+WhatsApp\s*$/);  // grouped for reading
  // Laid out like Settings: one heading style for both sections, the two switches stacked with a line each, every
  // switch and select on one right edge, the selects one width, and Leave apart at the very bottom
  const lay=await block.evaluate(el=>{const r=x=>x.getBoundingClientRect(),heads=[...el.querySelectorAll('.section-head h2')].map(h=>{const s=getComputedStyle(h);return s.fontFamily+s.fontSize+s.fontWeight});
   const rows=[...el.querySelectorAll('.net-row')],sels=[...el.querySelectorAll('[data-meet-pref]')],sw=[...el.querySelectorAll('.net-row input,.net-addr input')];
   const leave=el.querySelector('[data-net-do="leave"]'),last=el.lastElementChild;
   return {heads,stacked:rows.length===2&&r(rows[1]).top>=r(rows[0]).bottom-1,notes:rows.map(x=>!!x.querySelector('small')?.textContent.trim()),
    rights:[...new Set([...sw,...sels].map(x=>Math.round(r(x).right)))].length,sizes:[...new Set(sw.map(x=>Math.round(r(x).width)+'x'+Math.round(r(x).height)))].length,widths:[...new Set(sels.map(x=>Math.round(r(x).width)))].length,
    leaveLast:last.contains(leave)&&r(leave).top>r(el.querySelector('.meet-setting')).bottom+20}});
  assert.equal(lay.heads.length,2);assert.equal(lay.heads[0],lay.heads[1],'Network and Scheduling headings match');
  assert.ok(lay.stacked,`${scheme} ${width}px switches stacked`);assert.deepEqual(lay.notes,[true,true]);
  assert.equal(lay.rights,1,`${scheme} ${width}px switches and selects end on one edge`);assert.equal(lay.widths,1,`${scheme} ${width}px selects one width`);
  assert.equal(lay.sizes,1,`${scheme} ${width}px one switch size throughout`);
  assert.ok(lay.leaveLast,'Leave the Network apart at the bottom');
  assert.match(await block.locator('.net-addr:has([data-net-addr="+12025550100"])').innerText(),/About you/);
  assert.equal(await block.locator('[data-net-addr="+12025550100"]').isChecked(),false);
  calls.length=0;await block.locator('[data-net-addr="+12025550101"]').click();
  assert.deepEqual(await firstCall(),{action:'fleet_network',args:{do:'address_off',email:'+12025550101'}});
  calls.length=0;await block.locator('[data-net-addr="sam.doe-with-a-long-address@personal-mail.example"]').click();
  assert.deepEqual(await firstCall(),{action:'fleet_network',args:{do:'address_off',email:'sam.doe-with-a-long-address@personal-mail.example'}});
  calls.length=0;await block.locator('[data-net-toggle="discoverable_off"]').click();
  assert.deepEqual(await firstCall(),{action:'fleet_network',args:{do:'discoverable_off'}});
  calls.length=0;await block.locator('[data-net-do="leave"]').click();
  assert.deepEqual(await firstCall(),{action:'fleet_network',args:{do:'leave',email:'',relation:''}});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${scheme} ${width}px Fleet tab scrolls sideways`);
  if(process.env.SHOTS)await page.screenshot({path:`${process.env.SHOTS}/network-${scheme}-${width}.png`,fullPage:true});
  // Turned on by default (Standard): no extra line about it (the switch is the state), no card under To-dos
  shown={...found,network:{...found.network,asked:false,default_at:new Date().toISOString(),people:[]}};
  await page.reload();await navClick(page.locator('nav [data-tab="fleet"]'));await page.locator('[data-fleet-pane="network"]').click();
  const line=page.locator('#fleet-network .net-row:has([data-net-toggle="discoverable_off"])');await line.waitFor();
  assert.match(await line.innerText(),/Only the addresses below find you\./);
  assert.doesNotMatch(await page.locator('#fleet-network').innerText(),/Now findable|Turn off|by default/);
  calls.length=0;await line.locator('[data-net-toggle="discoverable_off"]').click();
  assert.deepEqual(await firstCall(),{action:'fleet_network',args:{do:'discoverable_off'}});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${scheme} ${width}px default line scrolls sideways`);
  if(process.env.SHOTS)await page.screenshot({path:`${process.env.SHOTS}/network-default-${scheme}-${width}.png`,fullPage:true});
  await navClick(page.locator('nav [data-tab="inbox"]'));
  assert.equal(await page.locator('.net-card').count(),0);
  assert.deepEqual(errors,[]);
 }
 console.log('ok network dashboard');
}finally{await browser.close();server.close()}
