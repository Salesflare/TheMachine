import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The Hand off sheet on a phone: with more teammates than fit a switch, "Hand off to" is a select, and it fits the
// sheet like the fields under it (a long name doesn't push it past the right edge), for a teammate and By email,
// in light and dark. Without any Gmail or Outlook account, By email says so in the sheet, with Prepare email off.
// SHOTS=<folder> saves screenshots at 390.
const dashboard=await dashboardPage();
const FL='fl_'+'a'.repeat(16);
const MEMBERS=['Maria-Elena Vasquez-Okonkwo','Pat Lee','Kim Lane','Sam Rivera','Alexandra Konstantinopoulou-Vanderbilt'].map((name,n)=>({member_id:'m'+n,name}));
const TASK='The customer needs every contact with its custom fields in one file for their quarterly review. Can you set up the export by Friday?';
function world(){
 const card={id:'c1',title:'Customer asks for a custom export',body:'They need it for their quarterly review.',status:'prepared',event_ids:[1],scope:'work',
  created_at:new Date().toISOString(),next_actions:[]};
 const state={suggestions:[card],connectors:[],suggestion_counts:{prepared:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0,take_line:true}};
 const view={on:true,kinds:{handoff:'handoffs'},ask_meetings:false,fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:['handoff'],people:[],
  members:MEMBERS.map(m=>({...m,rules:{}})),rules:{},exceptions:{}}],waiting:[],asked:[],intro_offers:[],splits:[],log:[],notices:[]};
 return {card,state,view};
}
let w=world(),mailbox=true;
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify(w.state));return}
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);
  if(call.action==='fleet_handoff_draft'){res.end(JSON.stringify({suggestion_id:'c1',title:w.card.title,summary:TASK,task:TASK,contact:'pat@client.example',sources:[{label:'Intercom from a customer · Sat 31 Oct',kind:'chat'}],
   fleets:[{id:FL,name:'Acme',members:MEMBERS}]}));return}
  if(call.action==='fleet_handoff_email_parts'){res.end(JSON.stringify({suggestion_id:'c1',shared:true,take:true,task:TASK,lines:[],links:[],files:[],draft:null,mailbox}));return}
  res.end(JSON.stringify({status:'answered',ids:{}}));return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(w.view));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});

// Every field of the sheet ends inside the sheet's content box, and the sheet inside the to-do
async function fits(page){
 return page.evaluate(()=>{const f=document.querySelector('.fleet-handoff-form'),card=f.closest('.card'),cs=getComputedStyle(f);
  const right=f.getBoundingClientRect().right-parseFloat(cs.paddingRight)-parseFloat(cs.borderRightWidth)+0.5;
  const out=[...f.querySelectorAll('select,input:not([type=hidden]):not([type=checkbox]),textarea,.agent-get')].filter(x=>x.getBoundingClientRect().right>right).map(x=>x.name||x.className||x.textContent);
  if(f.getBoundingClientRect().right>card.getBoundingClientRect().right+0.5)out.push('form');
  return out});
}
async function run(scheme,shots,withMail=true){
 w=world();mailbox=withMail;
 const page=await (await browser.newContext({viewport:{width:390,height:844},colorScheme:scheme})).newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const shot=async name=>{if(shots){await page.locator('.fleet-handoff-form').scrollIntoViewIfNeeded();await page.waitForTimeout(150);await page.screenshot({path:`${shots}/${name}-390-${scheme}.png`})}};
 await page.goto('http://127.0.0.1:'+server.address().port);
 const c=page.locator('#task-c1');await c.waitFor();
 await c.locator('.more-actions>summary').click();
 await c.locator('[data-fleet-handoff="c1"]').click();
 const pick=page.locator('.fleet-handoff-form select.handoff-pick');await pick.waitFor();
 assert.equal(await pick.inputValue(),FL+'|m0');
 await shot('fit-teammate');
 const bad={teammate:await fits(page)};
 await pick.selectOption('email');
 await page.locator('.fleet-handoff-form .handoff-email').waitFor();
 await shot(withMail?'fit-email':'fit-no-mailbox');
 bad.email=await fits(page);
 assert.deepEqual(bad,{teammate:[],email:[]});
 const form=page.locator('.fleet-handoff-form');
 assert.equal(await form.locator('.handoff-no-mailbox').count(),withMail?0:1);
 assert.equal(await form.locator('button.primary').isDisabled(),!withMail);
 if(!withMail)assert.equal(await form.locator('.handoff-no-mailbox').innerText(),'No Gmail or Outlook account to send it from. Connect one in Connections.');
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
 assert.deepEqual(errors,[]);
 await page.context().close();
}
try{
 const failed=[];for(const scheme of ['light','dark'])await run(scheme,process.env.SHOTS).catch(e=>failed.push(e));
 await run('dark',process.env.SHOTS,false).catch(e=>failed.push(e));
 if(failed.length)throw failed[0];
 console.log('ok');
}finally{await browser.close();server.close()}
