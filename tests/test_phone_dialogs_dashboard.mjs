import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Dialogs on a phone fill the screen: the title and × on top, the buttons at the bottom in sight without scrolling,
// and only what is between scrolls (a long email inside its own box), never the page behind. With the keyboard up
// (Android makes the page shorter) the buttons are still in sight. On a computer the Send dialog stays a centered box.
// SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const LONG='Hi Noor,\n\n'+Array(9).fill('Of the three options, the data enrichment page looks like the cleanest fit for our guide. Could you share monthly traffic for those pages?').join('\n\n')+'\n\nRegards,\nAlex';
const card={id:'l1',title:'Reply to Noor about the partnership',body:'Draft ready.',status:'prepared',scope:'work',created_at:now,preparation_status:'done',event_ids:[2],
 next_actions:[{kind:'email',revision:'v1',label:'Send to Noor',to:['noor@example.com'],to_name:'Noor',from:'alex@example.com',subject:'Re: Collaboration between Acme and Example Co',body:LONG,snooze_days:3}]};
const state={suggestions:[card],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}};
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const errors=[];
// Where the dialog, its title row and its buttons are, and what scrolls
const measure=(page,sel)=>page.evaluate(sel=>{const d=document.querySelector(sel),r=x=>x.getBoundingClientRect(),dr=r(d);
 const buttons=[...d.querySelectorAll('button')].filter(b=>b.offsetParent&&b.closest('.send-act,.actions'));
 const head=d.querySelector('.snooze-heading'),ed=document.querySelector('#send-rich-body');
 return {dialog:[dr.top,dr.bottom,dr.width].map(Math.round),inner:innerHeight,width:innerWidth,head:Math.round(r(head).top),
  buttons:buttons.map(b=>({label:b.textContent,top:Math.round(r(b).top),bottom:Math.round(r(b).bottom)})),
  editor:ed&&!ed.closest('[hidden]')?{scrolls:ed.scrollHeight>ed.clientHeight+1,top:Math.round(r(ed).top),bottom:Math.round(r(ed).bottom)}:null,
  dialogScrolls:d.scrollHeight>d.clientHeight+1,page:getComputedStyle(document.documentElement).overflow,pageScrollY:scrollY}},sel);
async function run(scheme,shots){
 const ctx=await browser.newContext({viewport:{width:390,height:844},colorScheme:scheme,locale:'en-US',isMobile:true,hasTouch:true});
 await ctx.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 const page=await ctx.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-l1').waitFor();
 await page.evaluate(()=>openSend('l1'));await page.locator('#send-rich-body').waitFor();await page.waitForTimeout(250);
 if(shots)await page.screenshot({path:`${shots}/phone-send-long-${scheme}.png`});
 let m=await measure(page,'#send-dialog');
 // the whole screen, title on top, no page scroll behind it
 assert.deepEqual(m.dialog,[0,844,390]);assert.equal(m.head,0);assert.equal(m.page,'hidden');
 // Send now and Ask for changes in sight, at the bottom; × closes, so no Cancel beside Send
 assert.deepEqual(m.buttons.map(b=>b.label),['Send now','Ask for changes']);
 for(const b of m.buttons){assert.ok(b.bottom<=844&&b.top>=844-120,JSON.stringify(b))}
 // the long email scrolls inside its own box, which fills the room between the fields and the buttons; the sheet itself doesn't scroll
 assert.ok(m.editor.scrolls,'the email scrolls inside');assert.equal(m.dialogScrolls,false);
 assert.ok(m.editor.bottom<=m.buttons[0].top&&m.editor.bottom-m.editor.top>300,JSON.stringify(m.editor));
 await page.locator('#send-rich-body').evaluate(x=>{x.scrollTop=x.scrollHeight});
 assert.ok(await page.locator('#send-rich-body').evaluate(x=>x.scrollTop>0));
 assert.equal(await page.evaluate(()=>scrollY),m.pageScrollY);
 // the note under the email is one short line
 assert.equal(await page.locator('#send-fine').innerText(),'Leaves your inbox for 3 days after sending, or until a reply.');
 // typing, with the keyboard up: the page gets shorter (interactive-widget=resizes-content) and the buttons stay in sight
 await page.locator('#send-rich-body').focus();await page.setViewportSize({width:390,height:470});await page.waitForTimeout(250);
 if(shots)await page.screenshot({path:`${shots}/phone-send-keyboard-${scheme}.png`});
 m=await measure(page,'#send-dialog');
 assert.deepEqual(m.dialog,[0,470,390]);
 for(const b of m.buttons)assert.ok(b.bottom<=470,JSON.stringify(b));
 await page.setViewportSize({width:390,height:844});
 // Remind me later: the whole screen too
 await page.evaluate(()=>{document.querySelector('#send-dialog').close();openSnooze('l1')});await page.locator('#snooze-dialog[open]').waitFor();
 m=await measure(page,'#snooze-dialog');assert.deepEqual(m.dialog,[0,844,390]);
 await ctx.close();
}
try{
 for(const scheme of ['light','dark'])await run(scheme,process.env.SHOTS);
 // a computer: the centered box it always was, Cancel beside Send
 const ctx=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
 await ctx.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
 const page=await ctx.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-l1').waitFor();
 await page.evaluate(()=>openSend('l1'));await page.locator('#send-rich-body').waitFor();
 const m=await measure(page,'#send-dialog');
 assert.equal(m.dialog[2],560);assert.ok(m.dialog[0]>0);
 assert.deepEqual(m.buttons.map(b=>b.label),['Send now','Ask for changes','Cancel']);
 assert.notEqual(m.page,'hidden');
 await ctx.close();
 assert.deepEqual(errors,[]);
 console.log('ok');
}finally{await browser.close();server.close()}
