import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Scheduling with someone who has no Machine (meet_link.py, dashboard/todos-meet.js): the to-do's email draft carries a
// booking link ("Pick a time", no footer line), said under the to-do; their pick is a to-do with Book it and Not needed only,
// each the owner's own tap (meet_decide). The footer setting sits in the Network pane. Never scrolls sideways (390px and
// 1280px, light and dark). Optional SHOT_DIR: screenshots of each.
const dashboard=await dashboardPage();
const SHOTS=process.env.SHOT_DIR||'',now=new Date().toISOString();
const LINK='https://themachine.computer/t/'+'A'.repeat(22)+'#k='+'k'.repeat(43);
const BODY='Hi Carol,\n\nHappy to meet next week.\n\n[Pick a time]('+LINK+')\n\nBest,\nSam';
const FR='fr_'+'b'.repeat(16);
let picked,setting;
const cards=()=>[
 {id:'c1',title:'Reply to Carol about next week',body:'Carol asked to meet next week.',status:'prepared',scope:'work',created_at:now,event_ids:[1],
  next_actions:[{kind:'email',label:'Send',revision:'e00000000002',account_id:'work',to:['carol@three.example'],subject:'Re: Next week',body:BODY}],
  meet:{state:'link',link_state:'open',role:'link',name:'Carol Sample',minutes:30,video:null,mine_ok:false,their_ok:false,note:null,until:'2026-11-09'}},
 {id:'p1',title:'Meet Carol Sample',body:'Carol Sample picked this time on your booking link.',status:'pending',scope:'work',
  created_at:now,event_ids:[2],meet:picked}];
const fleet=()=>({on:true,kinds:{},kind_rules:{},no_details:[],scoped:[],scopes:{},waiting:[],asked:[],log:[],notices:[],splits:[],
 fleets:[{id:FR,kind:'friends',label:'Friends',name:'Friends',asks:[],people:[{member_id:'fp_me',name:'Sam Doe',me:true}],members:[]}],
 friends:{id:FR,username:'sam',in:[],out:[],blocked:[]},network:{find:true,discoverable:true,asked:true,last:null,people:[],addresses:[]},meet:setting});
const calls=[];
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 const asset={'/brand/avatar.png':'brand/app-icon-192.png','/brand/serif.woff2':'brand/fonts/source-serif-4-latin.woff2','/brand/sans.woff2':'brand/fonts/inter-latin.woff2'}[url.pathname];
 if(asset){res.setHeader('Content-Type',asset.endsWith('png')?'image/png':'font/woff2');res.end(await readFile(new URL('../'+asset,import.meta.url)));return}
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status')return res.end(JSON.stringify({suggestions:cards(),promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],connectors:[],fleet:{on:true,waiting:0}}));
 if(url.pathname.startsWith('/api/fleet'))return res.end(JSON.stringify(fleet()));
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='meet_decide'&&call.args.choice==='book'){picked={...picked,state:'booked'};return res.end(JSON.stringify({state:'booked'}))}
  if(call.action==='meet_setting'){setting={...setting,...call.args};return res.end(JSON.stringify(setting))}
  return res.end('{"ok":true}')}
 res.end(url.pathname==='/api/events'?'[]':'{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const sideways=page=>page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
try{
 for(const [width,height] of [[1280,900],[390,844]])for(const scheme of ['light','dark']){
  picked={state:'picked',role:'link',name:'Carol Sample',minutes:30,video:null,mine_ok:false,their_ok:false,note:null,when:'Wed 4 Nov 15:00',start:'2026-11-04T14:00Z'};
  setting={allow:'freebusy',minutes:30,buffer:10,prefer:'any',brand:true};calls.length=0;
  const phone=width<600,context=await browser.newContext({viewport:{width,height},isMobile:phone,hasTouch:phone,colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage(),errors=[],tag=`${width}-${scheme}`;page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  // The draft with the link: the owner sees it, and Send stays theirs
  const draft=page.locator('#task-c1');await draft.waitFor();
  assert.match(await draft.locator('.meet-line').textContent(),/Booking link in the email draft\. Carol Sample can pick a time\./);
  const pick=draft.locator('a',{hasText:'Pick a time'});  // the link behind its words, no long address in the email
  assert.equal(await pick.count(),1);
  assert.equal(await pick.getAttribute('href'),LINK);
  assert.doesNotMatch(await draft.innerText(),/Get yours|\/t\//);  // no branding in the email: the footer is on the page only
  assert.equal(await draft.locator('[data-meet-do]').count(),0);
  assert.ok(await sideways(page)<=0,'no sideways scroll on the draft');
  if(SHOTS)await draft.screenshot({path:`${SHOTS}/meet-link-draft-${tag}.png`});
  // Their pick: Book it and Not needed, no Other time
  const todo=page.locator('#task-p1');await todo.waitFor();
  assert.equal((await todo.locator('h3').first().textContent()).trim(),'Meet Carol Sample');
  assert.match(await todo.locator('.meet-line').textContent(),/Wed 4 Nov 15:00 · 30 min/);
  assert.match(await todo.locator('.meet-line').textContent(),/Nothing is booked until you tap Book it\./);
  assert.deepEqual(await todo.locator('[data-meet-do]').evaluateAll(n=>n.map(x=>x.textContent)),['Book it','Not needed']);
  if(SHOTS)await todo.screenshot({path:`${SHOTS}/meet-link-picked-${tag}.png`});
  await todo.locator('[data-meet-do="book"]').click();
  await page.locator('#toast',{hasText:'Booked. The invite is on its way.'}).waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args]),[['meet_decide',{suggestion_id:'p1',choice:'book'}]]);
  // The footer setting, in the Network pane: on by default, and changed with the owner's own pick
  await navClick(page.locator('nav [data-tab="fleet"]'));await page.locator('[data-fleet-pane="network"]').click();
  const box=page.locator('.meet-setting');await box.waitFor();
  assert.equal(await box.locator('[data-meet-pref="brand"]').inputValue(),'true');
  if(SHOTS){await box.scrollIntoViewIfNeeded();await box.screenshot({path:`${SHOTS}/meet-link-setting-${tag}.png`})}
  calls.length=0;await box.locator('[data-meet-pref="brand"]').selectOption('false');
  await page.locator('#toast',{hasText:'Saved.'}).waitFor();
  assert.deepEqual(calls.map(c=>[c.action,c.args]),[['meet_setting',{brand:false}]]);
  assert.ok(await sideways(page)<=0,'no sideways scroll in the Network pane');
  assert.deepEqual(errors,[]);
  await context.close();
 }
 console.log('meet link dashboard ok');
}finally{await browser.close();server.close()}
