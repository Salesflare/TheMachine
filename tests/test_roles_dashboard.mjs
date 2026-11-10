import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A review's roles apply as read, on the page with the line they came from; Edit changes one (no Who's who, nothing to
// confirm); relations and organization roles; open cards made together ranked by who they're about.
const dashboard=await dashboardPage();
const made=new Date(Date.now()-3600e3).toISOString();
const suggestions=[{id:'aaaaaaaaaaaaaaaa',title:'Newsletter tweak',body:'Small thing.',status:'pending',event_ids:[1],scope:'work',created_at:made,weight:0.2},
 {id:'bbbbbbbbbbbbbbbb',title:'Answer your cofounder',body:'About the board deck.',status:'pending',event_ids:[2],scope:'work',created_at:made,weight:3.4}];
let pat={id:'email:pat@client.example',kind:'person',name:'Pat Doe',strength:2,closeness:'regular',last_at:made,signals:4,ids:['pat@client.example'],links:[],
 role:'CFO at Client Ltd',role_by:'review',role_quote:'As the CFO at Client Ltd I look after the renewal',role_event_id:41,
 relations:[{a:'email:ann@client.example',a_name:'Ann Assist',relation:'assistant of',b:'email:pat@client.example',b_name:'Pat Doe',by:'review'}],open:{},recent:[],around:[]};
const org={id:'org:client.example',kind:'org',name:'Client Ltd',strength:3,last_at:made,signals:3,role:'customer',role_by:'review',links:[],open:{},recent:[],around:[],
 about:'Logistics, 51-200 people, Ghent',profile:{industry:'Logistics',about:'Client Ltd moves boxes.',linkedin_url:'https://www.linkedin.com/company/client',website:'javascript:alert(1)'}};
let holdOrg=null,warmup=[{domain:'warmup-pool.example',name:'warmup-pool.example',source:'agent',created_at:made}];
const calls=[],errors=[],opened=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions,promises:[],connectors:[],suggestion_counts:{pending:2},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){const node=url.searchParams.get('node');if(node===org.id&&holdOrg)await holdOrg;res.end(JSON.stringify(node==='org:client.example'?org:node?pat:{projects:[],people:[],quiet:[],new:[],orgs:[{...org}],warmup}));return}
 if(url.pathname==='/api/event'||url.pathname==='/api/events'){opened.push(url.search);res.end(JSON.stringify([]));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);
  if(call.action==='graph_person_edit'&&call.args.fields.role){pat={...pat,role:call.args.fields.role,role_by:'owner'}}
  if(call.action==='graph_relation')pat={...pat,relations:[]};
  if(call.action==='graph_org_edit')await new Promise(r=>setTimeout(r,150));  // the owner can tap before a save replies
  if(call.action==='graph_warmup')warmup=warmup.filter(w=>w.domain!==call.args.domain);
  res.end('{}');return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 // Made by the same review: the card about the cofounder comes first.
 await page.locator('#task-bbbbbbbbbbbbbbbb').waitFor();
 const order=await page.locator('#suggestions article[id^="task-"]').evaluateAll(a=>a.map(x=>x.id));
 assert.deepEqual(order.slice(0,2),['task-bbbbbbbbbbbbbbbb','task-aaaaaaaaaaaaaaaa']);
 await navClick(page.locator('nav [data-tab="people"]'));
 const list=page.locator('#people-view');
 await list.locator('[data-graph-panel="orgs"]').waitFor({state:'attached'});
 // No Who's who: no row under Graph, no pane, no ✓ All are right
 assert.equal(await page.locator('.side-sub a[data-graph-sub="roles"]').count(),0);
 assert.equal(await list.locator('[data-graph-panel="roles"],.whos,[data-role-all]').count(),0);
 await navClick(page.locator('.side-sub a[data-graph-sub="orgs"]'));
 let text=await list.textContent();
 assert.ok(text.includes('Customer · Logistics · 3 people'));  // the organization's role and industry in its list  // the organization's role in its list
 const widths=[];
 for(const width of [320,390,768]){
  await page.setViewportSize({width,height:844});
  const sizes=await page.evaluate(()=>({page:document.documentElement.scrollWidth,viewport:innerWidth}));
  assert.ok(sizes.page<=sizes.viewport,'overflow at '+width);widths.push({width,...sizes});
  if(process.env.ROLES_SHOT)await page.screenshot({path:process.env.ROLES_SHOT+'-'+width+'.png',fullPage:true});
 }
 await page.setViewportSize({width:390,height:844});
 // With you on the person's page: the review's quote and its Read are markup, not printed tags.
 await page.evaluate(()=>people('email:pat@client.example'));
 const about=page.locator('.graph-detail .person-about .kv-role');
 await about.locator('.role-why').waitFor();
 assert.ok(!(await about.textContent()).includes('<'),await about.textContent());
 assert.ok(await about.locator('.role-why button[data-quote-event="41"]').isVisible());
 assert.equal(await about.locator('[data-role-confirm]').count(),0);  // it applies as read: nothing to confirm
 // Not right: Edit on their page has the role among the rest
 await page.locator('[data-org-edit]').click();
 await page.locator('.person-form:not([hidden]) [name=role]').waitFor();
 assert.equal(await page.locator('.person-form [name=role]').inputValue(),'CFO at Client Ltd');
 text=await list.textContent();
 assert.ok(text.includes('“As the CFO at Client Ltd I look after the renewal”')&&text.includes('Ann Assist is assistant of Pat Doe'));
 await page.locator('.person-form [name=role]').fill('finance lead at Client Ltd');
 await page.locator('[data-org-save]').click();
 for(let i=0;i<100&&calls.length<1;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls[0],{action:'graph_person_edit',args:{node_id:'email:pat@client.example',fields:{role:'finance lead at Client Ltd'}}});
 await page.locator('.person-about b',{hasText:'Finance lead'}).waitFor();
 await page.locator('[data-unrelate]').click();
 for(let i=0;i<100&&calls.length<2;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls[1],{action:'graph_relation',args:{node_id:'email:ann@client.example',related_to:'email:pat@client.example',relation:''}});
 for(let i=0;i<100&&await page.locator('.relation').count();i++)await page.waitForTimeout(20);
 assert.equal(await page.locator('.relation').count(),0);
 // An organization has a role row too.
 await page.evaluate(()=>people('org:client.example'));
 await page.locator('.graph-detail h3',{hasText:'Client Ltd'}).waitFor();
 assert.ok((await page.locator('.person-about .kv-role').textContent()).includes('Customer'));
 // What the enrichment service says about it, with only real links.
 const detail=await page.locator('.graph-detail').textContent();
 assert.ok(detail.includes('Logistics, 51-200 people, Ghent')&&detail.includes('Client Ltd moves boxes.'));
 assert.equal(await page.locator('.graph-detail a[href^="https://www.linkedin.com"]').count(),1);
 assert.equal(await page.locator('.graph-detail a[href^="javascript"]').count(),0);
 // One Edit for an organization: only the changed fields become the owner's; Wrong company clears a bad match.
 assert.equal(await page.locator('.graph-detail [data-name-edit]').count(),0);
 await page.locator('[data-org-edit]').click();
 await page.locator('.org-form input[name="industry"]').fill('Freight');
 await page.locator('.org-form input[name="name"]').fill('Client Group');
 let mark=calls.length;
 await page.locator('.graph-detail .name-row [data-org-save]').click();
 for(let i=0;i<100&&calls.length<=mark;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls.at(-1),{action:'graph_org_edit',args:{node_id:org.id,fields:{industry:'Freight'},name:'Client Group'}});
 assert.equal(await page.locator('[data-org-save]').isDisabled(),true);
 await page.locator('[data-org-edit]').waitFor();
 await page.locator('[data-org-edit]').click();
 page.once('dialog',d=>{assert.ok(d.message().startsWith('Clear the looked-up details?'));d.accept()});
 mark=calls.length;
 await page.locator('[data-org-wrong]').click();
 for(let i=0;i<100&&calls.length<=mark;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls.at(-1),{action:'graph_org_wrong',args:{node_id:org.id,wrong:true}});
 // The shown form is Pat's even when a slow navigation has selected another node.
 await page.evaluate(()=>people('email:pat@client.example'));
 await page.locator('.graph-detail h3',{hasText:'Pat Doe'}).waitFor();
 await page.locator('[data-org-edit]').click();
 await page.locator('.person-form [name=role]').fill('trusted colleague');
 let release;holdOrg=new Promise(r=>release=r);
 await page.evaluate(()=>{void people('org:client.example')});
 await page.locator('[data-org-save]').click();
 for(let i=0;i<100&&!calls.some(c=>c.args.fields?.role==='trusted colleague');i++)await page.waitForTimeout(20);
 assert.deepEqual(calls.find(c=>c.args.fields?.role==='trusted colleague'),{action:'graph_person_edit',args:{node_id:pat.id,fields:{role:'trusted colleague'}}});
 holdOrg=null;release();
 await page.waitForTimeout(100);
 await page.evaluate(()=>people('email:pat@client.example'));
 await page.locator('.graph-detail h3',{hasText:'Pat Doe'}).waitFor();
 await page.locator('[data-org-edit]').click();
 await page.locator('.person-form [name=name]').fill('Pat Owner Name');
 holdOrg=new Promise(r=>release=r);
 await page.evaluate(()=>{void people('org:client.example')});
 await page.locator('[data-org-save]').click();
 for(let i=0;i<100&&!calls.some(c=>c.args.fields?.name);i++)await page.waitForTimeout(20);
 assert.deepEqual(calls.find(c=>c.args.fields?.name),{action:'graph_person_edit',args:{node_id:pat.id,fields:{name:'Pat Owner Name'}}});
 holdOrg=null;release();
 // Warm-up domains a review hid: their own tab on Organizations (no count: nothing there needs the owner), each with Undo; the tab goes when empty.
 await navClick(page.locator('.side-sub a[data-graph-sub="orgs"]'));
 const warm=list.locator('[data-graph-panel="orgs"] [data-graph-list="warmup"]');
 assert.equal((await warm.textContent()).replace(/\s+/g,' ').trim(),'Warm up');
 await warm.click();
 const beforeUndo=calls.length;
 await list.locator('[data-warmup-undo="warmup-pool.example"]').click();
 for(let i=0;i<100&&calls.length<=beforeUndo;i++)await page.waitForTimeout(20);
 assert.deepEqual(calls.at(-1),{action:'graph_warmup',args:{domain:'warmup-pool.example',warmup:false}});
 for(let i=0;i<100&&await warm.count();i++)await page.waitForTimeout(20);
 assert.equal(await warm.count(),0);
 assert.equal(await list.locator('[data-graph-panel="orgs"] [data-graph-list="orgs"]').getAttribute('aria-selected'),'true','back on All');
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({widths,actions:calls.length,page_errors:errors}));
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r))}
