import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Hand off by email (handoff_mail.py): the By email sheet lists what goes in the email, each part ticked, and sends
// only the ticked keys; Prepare email leaves an ordinary draft on the to-do to read and send; once sent, the to-do
// says who has it and tracks the promise. Settings > Fleet turns the "Take this on" line off. No network beyond this
// fake server, and nothing is sent. SHOTS=<folder> also saves screenshots at 390 and 1280, light and dark.
const dashboard=await dashboardPage();
const FL='fl_'+'a'.repeat(16),DUE=new Date(Date.now()+4*864e5).toISOString().slice(0,10);
const PARTS={suggestion_id:'c1',shared:true,take:true,task:'Send Sam the pricing',
 lines:[{key:'why',text:'Sam asked for the Q3 pricing before Friday.'},{key:'contact',text:'Contact: Sam Rivera'},{key:'due',text:'Due '+DUE,due:DUE}],
 draft:{key:'draft',to:['sam@client.example'],subject:'Q3 pricing'},links:[{key:'link:0',title:'Pricing sheet',url:'https://docs.example/pricing'}],
 files:[{key:'file:0',name:'pricing-q3.pdf',size:120000}]};
const BODY=['Hi there,','Could you take this on?','Send Sam the pricing','Sam asked for the Q3 pricing before Friday.\nContact: Sam Rivera\nIt would be great to have it by '+new Date(DUE+'T12:00:00Z').toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric',timeZone:'UTC'})+'.',
 'The draft is ready to send:\nTo: sam@client.example\nSubject: Q3 pricing\n\nHi Sam, here is the Q3 pricing.','Just reply to this email to let me know.','Best,\nAlex',
 'Take this on in your own Machine: https://themachine.computer/take/'+'T'.repeat(22)].join('\n\n');

function world(){
 const card={id:'c1',title:'Send Sam the pricing',body:'Sam asked for the Q3 pricing. The draft is ready.',status:'prepared',event_ids:[1],scope:'work',due:DUE,
  created_at:new Date().toISOString(),next_actions:[{kind:'email',revision:'v1',label:'Send to Sam',to:['sam@client.example'],to_name:'Sam',subject:'Q3 pricing',body:'Hi Sam, here is the Q3 pricing.'}]};
 const state={suggestions:[card],connectors:[],suggestion_counts:{prepared:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0,take_line:true}};
 const view={on:true,kinds:{handoff:'handoffs'},ask_meetings:false,fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:['handoff'],people:[],
  members:[{member_id:'p',name:'Pat',rules:{}}],rules:{},exceptions:{}}],waiting:[],asked:[],intro_offers:[],splits:[],log:[],notices:[]};
 return {card,state,view,calls:[]};
}
let w=world();
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify(w.state));return}
 if(req.url.startsWith('/api/invitees')){res.end(JSON.stringify({people:[{name:'Kim Lane',email:'kim@acme.example'}]}));return}
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);w.calls.push(call);
  if(call.action==='fleet_handoff_draft'){res.end(JSON.stringify({suggestion_id:'c1',title:w.card.title,summary:'Send Sam the pricing',contact:'Sam Rivera',due:DUE,sources:[],fleets:[{id:FL,name:'Acme',members:[{member_id:'p',name:'Pat'}]}]}));return}
  if(call.action==='fleet_handoff_email_parts'){res.end(JSON.stringify(PARTS));return}
  if(call.action==='fleet_handoff_take_line'){w.state.fleet.take_line=call.args.on;res.end(JSON.stringify({take_line:call.args.on}));return}
  if(call.action==='fleet_handoff_email'){  // what the service does: an ordinary email draft on the to-do, to read and send
   w.card.next_actions=[{kind:'email',revision:'v2',label:'Send to Kim Lane',to:['kim@acme.example'],to_name:'Kim Lane',subject:'Could you take this on: Send Sam the pricing',body:BODY,
    attachments:[{name:'pricing-q3.pdf',size:120000}]}];res.end(JSON.stringify({card_id:'c1'}));return}
  res.end(JSON.stringify({status:'answered',ids:{}}));return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(w.view));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});

async function run(width,scheme,shots){
 w=world();
 const page=await (await browser.newContext({viewport:{width,height:width<600?844:900},colorScheme:scheme})).newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const shot=async(name,loc)=>{if(shots){await loc.scrollIntoViewIfNeeded();await page.waitForTimeout(150);await page.screenshot({path:`${shots}/${name}-${width}-${scheme}.png`})}};
 await page.goto('http://127.0.0.1:'+server.address().port);
 const c=page.locator('#task-c1');await c.waitFor();
 await c.locator('.more-actions>summary').click();
 await c.locator('[data-fleet-handoff="c1"]').click();
 const form=page.locator('.fleet-handoff-form');await form.waitFor();
 await form.locator('label:has(input[name=to][value=email])').click();
 const parts=form.locator('.handoff-parts');await parts.waitFor();
 // Everything the email can carry, each ticked; Work and shared, so no "stays out" line
 assert.deepEqual(await parts.locator('[data-handoff-part]').evaluateAll(x=>x.map(i=>[i.dataset.handoffPart,i.checked])),
  [['why',true],['contact',true],['due',true],['draft',true],['link:0',true],['file:0',true],['take',true]]);
 assert.match(await parts.innerText(),/Sam asked for the Q3 pricing[\s\S]*Draft ready to send: Q3 pricing[\s\S]*Pricing sheet[\s\S]*pricing-q3\.pdf[\s\S]*Take this on in your own Machine/);
 assert.doesNotMatch(await form.innerText(),/stays out/);
 assert.equal(await form.locator('button.primary').innerText(),'Prepare email');
 await form.locator('input[name=email]').fill('ki');
 await form.locator('[data-team-email="kim@acme.example"]').click();
 await form.locator('[data-handoff-part="link:0"]').uncheck();
 await shot('1-picker',form);
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);  // no sideways scroll
 await form.locator('button.primary').click();
 await page.waitForFunction(()=>!document.querySelector('.fleet-handoff-form'));
 assert.deepEqual(w.calls.find(x=>x.action==='fleet_handoff_email').args,{suggestion_id:'c1',email:'kim@acme.example',title:'Send Sam the pricing',
  summary:'Send Sam the pricing',keep:['why','contact','due','file:0','draft'],take:true,name:'Kim Lane'});
 // The email waits on the to-do, as any email: read it, then send it yourself
 await page.waitForFunction(()=>/Could you take this on/.test(document.querySelector('#task-c1')?.innerText||''));
 assert.match(await c.innerText(),/Take this on in your own Machine: https:\/\/themachine\.computer\/take\//);
 assert.doesNotMatch(await c.innerText(),/docs\.example/);  // the unticked link stayed out
 if(shots){await page.evaluate(()=>$('#toast').classList.remove('show'));const more=c.getByText('Show more');if(await more.count())await more.first().click()}
 await shot('2-review',c.locator('.draft').first());
 // Sent: snoozed under Later, with whom it is and the promise
 Object.assign(w.card,{status:'snoozed',snoozed_until:new Date(Date.now()+3*864e5).toISOString(),next_actions:[],handoff_mail:{name:'Kim Lane',state:'waiting',promise:'open'}});
 w.state.suggestion_counts={snoozed:1};
 await page.evaluate(()=>refresh());
 await page.locator('#later-list>summary').click();
 const later=page.locator('#later-list #task-c1');await later.waitFor();
 assert.match(await later.innerText(),/Handed to Kim Lane by email[\s\S]*Kim takes this on/);
 await shot('3-after',later);
 w.card.handoff_mail.promise='kept';await page.evaluate(()=>refresh());
 await page.waitForFunction(()=>/Kim took this on/.test(document.querySelector('#later-list #task-c1')?.innerText||''));
 // Settings > Fleet: the take line, on by default, turns off
 const sw=page.locator('#settings-take-line');
 assert.equal(await sw.getAttribute('aria-checked'),'true');
 await sw.evaluate(b=>b.click());
 await page.waitForFunction(()=>document.querySelector('#settings-take-line').getAttribute('aria-checked')==='false');
 assert.deepEqual(w.calls.at(-1),{action:'fleet_handoff_take_line',args:{on:false}});
 assert.deepEqual(errors,[]);
 await page.context().close();
}
try{
 await run(390,'light',null);
 if(process.env.SHOTS)for(const width of [390,1280])for(const scheme of ['light','dark'])await run(width,scheme,process.env.SHOTS);
 console.log('ok');
}finally{await browser.close();server.close()}
