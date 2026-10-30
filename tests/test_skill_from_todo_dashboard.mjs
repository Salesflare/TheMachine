import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A to-do whose run proposed a skill (proposed_skill): the card shows what is in it and leads with Create skill, or
// Update skill with its before and after first. Never Copy draft or "can't be sent from here": a skill isn't a message.
// Only the owner's tap sends the Approve (skill_decide). The summary doesn't end on "The draft is at" once the path is gone.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),name='Payroll <img src=x onerror="window.pwned=1">';
const body='Your corrected payroll skill is proposed for approval, replacing the earlier version. The draft is at memory/assistant/261030-payroll.md.';
const update={skill:'Expenses',before:'1. Old step.',after:'1. Old step.\n2. New step.',changes:[],review:'rev-1'};
let cards=[
 {id:'s1',title:'Create a payroll skill',body,status:'prepared',scope:'work',origin:'owner',created_at:now,event_ids:[1],outcome:'{"state":"needs_you","needs":"approve the payroll skill"}',
  result_files:[{name:'261030-payroll.md',path:'memory/assistant/261030-payroll.md'}],
  proposed_skill:{id:'sk_1',name,description:'Each month, when payroll is due',body:'1. Open the payroll site.\n2. Enter the vacation days.'}},
 {id:'s2',title:'Improve the expenses skill',body:'The update is ready. The draft is at memory/assistant/261030-expenses.md.',status:'prepared',scope:'work',origin:'owner',created_at:now,event_ids:[2],
  result_files:[{name:'261030-expenses.md',path:'memory/assistant/261030-expenses.md'}],proposed_skill:{id:'sk_2',name:'Expenses',description:'Expenses',body:update.after,update}},
 {id:'s4',title:'Create an onboarding skill',body:'Your onboarding skill is proposed for approval. The draft is at memory/assistant/261030-onboarding.md.',status:'prepared',scope:'work',origin:'owner',created_at:now,event_ids:[4],
  result_files:[{name:'261030-onboarding.md',path:'memory/assistant/261030-onboarding.md'}],proposed_skill:{dismissed:true,name:'Onboarding'}},
 {id:'s3',title:'Write the team note',body:'Here is the note. The draft is at memory/assistant/261030-note.md.',status:'prepared',scope:'work',created_at:now,event_ids:[3],
  result_files:[{name:'261030-note.md',path:'memory/assistant/261030-note.md'}]}];
const skillsView={skills:[{id:'sk_1',name,description:'Each month',status:'proposed',origin:'proposed',update:false,note:'',version:1,chars:40},
 {id:'sk_2',name:'Expenses',description:'Expenses',status:'proposed',origin:'proposed',update,note:'',version:1,chars:40}],waiting:2,targets:[],hints:[]};
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]},skills:skillsView});
const actions=[];
const server=createServer(async(req,res)=>{let raw='';for await(const c of req)raw+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){const a=JSON.parse(raw);actions.push(a);
  if(a.action==='skill_decide'){const card=cards.find(c=>c.proposed_skill?.id===a.args.id);cards=cards.map(c=>c===card?{...c,status:'completed',proposed_skill:undefined}:c);
   res.end(JSON.stringify({...skillsView,skills:skillsView.skills.map(s=>s.id===a.args.id?{...s,status:'on'}:s)}));return}
  res.end('{}');return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900}});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-s1').waitFor();
 const s1=page.locator('#task-s1');
 // Create skill leads; nothing about copying or sending
 assert.equal((await s1.locator('.actions button.primary').first().textContent()).trim(),'Create skill');
 assert.equal(await s1.locator('[data-result="copy"]').count(),0);
 assert.equal(await s1.locator('.copy-why').count(),0);
 assert.doesNotMatch(await s1.textContent(),/Copy draft|can’t be sent from here/);
 // The summary ends where the sentence before the stripped path ended
 const text=(await s1.locator('.body').textContent()).trim();
 assert.ok(text.endsWith('replacing the earlier version.'),text);
 assert.doesNotMatch(text,/The draft is at/);
 // What is in the skill, before the tap; its name stays text
 assert.equal((await s1.locator('details.skill-notes summary').textContent()).trim(),'Read the skill');
 await s1.locator('details.skill-notes summary').click();
 assert.match(await s1.locator('details.skill-notes').textContent(),/Enter the vacation days/);
 assert.equal(await s1.locator('img[src="x"]').count(),0);
 assert.equal(actions.filter(a=>a.action==='skill_decide').length,0);
 // The owner's tap: the Approve, then the to-do is done
 await s1.locator('[data-skill-create]').click();
 await page.waitForFunction(()=>!document.querySelector('#task-s1 [data-skill-create]'));
 assert.deepEqual(actions.filter(a=>a.action==='skill_decide').map(a=>a.args),[{id:'sk_1',choice:'approve'}]);
 // An update: Update skill opens the before and after; only its button there sends the Approve, with what was shown
 const s2=page.locator('#task-s2');
 assert.equal((await s2.locator('.actions button.primary').first().textContent()).trim(),'Update skill');
 assert.equal((await s2.locator('details.skill-notes summary').textContent()).trim(),'Read the change');
 assert.equal(await s2.locator('[data-result="copy"]').count(),0);
 await s2.locator('[data-skill-update]').click();
 await page.locator('#skill-update').waitFor({state:'visible'});
 assert.equal(actions.filter(a=>a.action==='skill_decide').length,1);
 await page.locator('#skill-update-ok').click();
 await page.waitForFunction(()=>!document.querySelector('#skill-update').open);
 assert.deepEqual(actions.filter(a=>a.action==='skill_decide').map(a=>a.args)[1],{id:'sk_2',choice:'approve',reviewed:'rev-1'});
 // Dismissed in Settings, Skills: the to-do says so, Mark done leads, never Copy draft; it stays open
 const s4=page.locator('#task-s4');
 assert.equal((await s4.locator('.skill-dismissed').textContent()).trim(),'Skill dismissed');
 assert.equal(await s4.locator('.actions button.primary').first().getAttribute('data-choice'),'complete');
 assert.equal(await s4.locator('[data-result="copy"]').count(),0);
 assert.equal(await s4.locator('.copy-why').count(),0);
 assert.equal(await s4.locator('[data-skill-create],[data-skill-update],details.skill-notes').count(),0);
 // A real draft without a send path still leads with Copy draft
 const s3=page.locator('#task-s3');
 assert.equal((await s3.locator('.actions button.primary').first().textContent()).trim(),'Copy draft');
 assert.equal(await s3.locator('.copy-why').count(),1);
 assert.equal(await page.evaluate(()=>window.pwned),undefined);
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('skill from to-do dashboard ok');
