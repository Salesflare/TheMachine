// A final step that posts a chat message: the card shows the exact text (like an email draft), Edit in the Submit
// dialog changes it, and Confirm submits the edited revision. A sent card shows only its sent status. Synthetic data,
// a local fixture server, nothing sent.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

const dashboard=await dashboardPage();
const sid='1234567890abcdef',legacy='fedcba0987654321',sent='0011223344556677',revision='1234567890ab',edited='abcdefabcdef';
const message='Hi Sam,\n\nThanks, the export is fixed.\n\nBest,\nAlex';
const chat={kind:'finish',label:'Submit inbox reply',revision,instructions:'Open conversation 7 and post the message.',preview:'Customer-visible reply in conversation 7.',
  url:'https://inbox.example.invalid/conversation/7',to_name:'Sam Example',message};
const old={kind:'finish',label:'Submit chat reply',revision:'999999999999',instructions:'Post the text in the preview.',preview:'Hey Robin,\n\nLegacy preview text.',url:'https://chat.example.invalid/c/1'};
const mail={kind:'email',label:'Send',revision:'555555555555',from:'alex@example.invalid',to:['robin@example.invalid'],subject:'Re: listing',body:'Hi Robin, sounds good.',
  state:{status:'sent',message_id:'m1',sent_at:new Date().toISOString()}};
const card=(id,title,a,extra={})=>({id,title,body:'Drafted the reply.',status:'prepared',event_ids:[1],next_action:a,next_actions:[a],outcome:JSON.stringify({state:'needs_you',needs:'Approve the reply'}),scope:'work',created_at:new Date().toISOString(),...extra});
const state=()=>({suggestions:[card(sid,'Customer asks about the export',chat),card(legacy,'Chat reply ready',old),card(sent,'Listing exchange agreed',mail,{status:'completed',outcome:null,body:'Drafted a short reply.'})],
  connectors:[],suggestion_counts:{prepared:2},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]});
const calls=[],errors=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  res.end(JSON.stringify(call.action==='revise_draft'?{status:'revised',revision:edited}:{status:'queued'}));return}
 res.statusCode=url.pathname.startsWith('/api/')?200:404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.evaluate(()=>refresh());
 const box=page.locator(`#task-${sid} .draft`);
 // The card itself shows the exact message and who gets it.
 assert.equal(await box.locator('.db').textContent(),message);
 assert.equal(await box.locator('.dm').textContent(),'Submit inbox reply · To: Sam Example');
 assert.equal(await box.getAttribute('aria-label'),'Message to post');
 // A step without a separate message shows what goes out.
 assert.ok((await page.locator(`#task-${legacy} .draft .db`).textContent()).includes('Legacy preview text.'));
 // A sent card: one green status, no needs-you line, no draft to approve.
 const done=page.locator(`#task-${sent}`);
 assert.equal(await done.count(),1);assert.equal(await done.locator('.outcome').count(),0);
 assert.match(await done.textContent(),/Email sent( at \d\d:\d\d)?\./);assert.ok(!(await done.textContent()).includes('Needs you'));
 assert.equal(await done.isVisible(),false,'a sent card leaves Ready for you');
 const widths=[];
 for(const width of [390,1280]){
  await page.setViewportSize({width,height:900});
  const sizes=await page.evaluate(id=>({page:document.documentElement.scrollWidth,viewport:innerWidth,box:document.querySelector(`#task-${id} .draft`).getBoundingClientRect().width,card:document.querySelector(`#task-${id}`).getBoundingClientRect().width}),sid);
  assert.ok(sizes.page<=sizes.viewport,'page overflow '+width);assert.ok(sizes.box<=sizes.card,'draft overflow '+width);
  widths.push({width,...sizes});
  if(process.env.SHOT_DIR)await page.locator(`#task-${sid}`).screenshot({path:`${process.env.SHOT_DIR}/chat-card-${width}.png`});
 }
 await page.setViewportSize({width:390,height:844});
 // Submit… keeps its Confirm dialog, now with Edit.
 await page.locator(`#task-${sid} [data-smart="${revision}"]`).click();
 await page.locator('#send-dialog').waitFor({state:'visible'});
 assert.equal(await page.locator('#send-title').textContent(),'Submit inbox reply?');
 assert.equal(await page.locator('#send-preview').textContent(),message);
 assert.equal(await page.locator('#send-confirm').textContent(),'Confirm');
 assert.ok(await page.locator('#send-edit').isVisible());
 assert.ok((await page.locator('#send-head').textContent()).includes('Sam Example'));
 if(process.env.SHOT_DIR)await page.locator('#send-dialog').screenshot({path:`${process.env.SHOT_DIR}/chat-dialog-390.png`});
 await page.locator('#send-edit').click();
 assert.ok(await page.locator('#send-subject-label').isHidden());
 assert.equal(await page.locator('#send-body').inputValue(),message);
 await page.locator('#send-body').fill('Hi Sam,\n\nIt works again now.\n\nAlex');
 await page.locator('#send-confirm').click();
 for(let i=0;i<100&&calls.length<2;i++)await page.waitForTimeout(20);
 assert.equal(calls.length,2);
 assert.deepEqual(calls[0],{action:'revise_draft',args:{suggestion_id:sid,revision,body:'Hi Sam,\n\nIt works again now.\n\nAlex'}});
 assert.equal(calls[1].action,'confirm_action');assert.equal(calls[1].args.revision,edited);
 // Unedited: Confirm goes straight through with the prepared revision.
 calls.length=0;await page.evaluate(()=>refresh());
 await page.locator(`#task-${legacy} [data-smart]`).click();await page.locator('#send-dialog').waitFor({state:'visible'});
 assert.ok(await page.locator('#send-edit').isVisible());
 await page.locator('#send-confirm').click();
 for(let i=0;i<100&&!calls.length;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls.map(c=>c.action),['confirm_action']);assert.equal(calls[0].args.revision,'999999999999');
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({widths,page_errors:errors},null,2));
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r))}
