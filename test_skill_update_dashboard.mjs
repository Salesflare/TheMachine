import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from './openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A skill card from notes is checked against the skills you have: a new one, a new one with a line on the related skill
// it sits next to, or Update <skill>, which opens its before and after and changes it only on Update skill there (with
// what was shown as `reviewed`). All mocked; SKILL_UPDATE_SHOTS=dir saves the cards and the dialog.
const dashboard=await readFile(process.env.SKILL_UPDATE_DASHBOARD||new URL('./dashboard.html',import.meta.url),'utf8');
const before=!!process.env.SKILL_UPDATE_BEFORE;  // the same cards as the previous version shaped them, for before shots
const now=new Date().toISOString(),posts=[];
const notes=n=>Array.from({length:n},(_,i)=>`For listing exchanges, rule ${i+1}: ask for their listing link before sending ours.`);
const body='## Steps\n1. Ask for their listing link first.\n2. Check the page is live and indexed.\n3. Send ours with the anchor text they asked for.';
const old='## When to use\nA partner agrees to swap listings.\n\n## Steps\n1. Check their site first.\n2. Write our entry in their format.';
const cards=[
 {id:'n1',title:'Turn 6 notes into a skill: Listing exchanges',status:'pending',scope:'work',created_at:now,event_ids:[1],labels:{accept:'Create skill',reject:'Not now'},
  body:'When a partner agrees to a listing exchange.\n\nI can keep these 6 notes together in a skill. Read the full instructions and notes before deciding. Create skill makes it, on, under Skills. Not now keeps them as they are.',
  skill_proposal:{name:'Listing exchanges',body,notes:notes(6)}},
 {id:'r1',title:'Turn 5 notes into a skill: Partner listing requests',status:'pending',scope:'work',created_at:now,event_ids:[2],labels:{accept:'Create skill',reject:'Not now'},
  body:'When a partner asks to be listed in one of our articles.'+(before?'':'\n\nRelated to Inclusion writer: that one is the other direction, our product in their articles.')+'\n\nI can keep these 5 notes together in a skill. Read the full instructions and notes before deciding. Create skill makes it, on, under Skills. Not now keeps them as they are.',
  skill_proposal:{name:'Partner listing requests',body,notes:notes(5),...(before?{}:{related:{name:'Inclusion writer',relation:'that one is the other direction, our product in their articles.'}})}},
 {id:'u1',title:before?'Add 6 notes to Listing swaps':'Update Listing swaps with 6 notes',status:'pending',scope:'work',created_at:now,event_ids:[3],
  labels:{accept:(before?'Add to ':'Update ')+'Listing swaps',reject:'Not now'},
  body:before?'When a partner agrees to swap listings.\n\nI can keep these 6 notes together in a skill. Read the full instructions and notes before deciding. Add to Listing swaps adds them to that skill. Not now keeps them as they are.'
   :'When a partner agrees to swap listings.\n\nThese 6 notes fit Listing swaps. Update shows the before and after first; only that skill changes. Not now keeps the notes as they are.',
  skill_proposal:{name:'Listing swaps',body,notes:notes(6),...(before?{}:{update:{skill:'Listing swaps',before:old,after:old+'\n\n'+body,added:body,review:'tok1'}})}}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]}});
const server=createServer(async(req,res)=>{let raw='';for await(const c of req)raw+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 if(req.method==='POST'&&raw){const b=JSON.parse(raw);posts.push({action:b.action,...b.args});
  if(b.action==='decide'&&b.args.reviewed==='stale'){res.statusCode=400;res.end(JSON.stringify({error:'Listing swaps changed since. Look at the before and after again'}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;const shots=process.env.SKILL_UPDATE_SHOTS;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390])for(const scheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-u1').waitFor();
  const tag=`${before?'before':'after'}-${width}-${scheme}`;
  if(shots){for(const id of ['n1','r1','u1']){const card=page.locator('#task-'+id);await card.locator('details.skill-notes').evaluate(d=>d.open=true);
   await card.screenshot({path:`${shots}/${tag}-${{n1:'new',r1:'related',u1:'update'}[id]}.png`});await card.locator('details.skill-notes').evaluate(d=>d.open=false)}}
  if(before){await context.close();continue}
  // New: Create skill, nothing about other skills
  assert.equal(await page.locator('#task-n1 .skill-related').count(),0);
  assert.equal(await page.locator('#task-n1 .actions button.primary').first().textContent(),'Create skill');
  // Related: one short line naming the skill, once (not again in the body), and the new one still offered
  assert.equal((await page.locator('#task-r1 .skill-related').textContent()).trim(),'Related to Inclusion writer: that one is the other direction, our product in their articles.');
  assert.equal(await page.locator('#task-r1 .body').getByText('Related to').count(),0);
  assert.equal(await page.locator('#task-r1 .actions button.primary').first().textContent(),'Create skill');
  // Update: the card's Read the change shows before and after; the button opens them first and posts nothing
  const card=page.locator('#task-u1');
  assert.match(await card.locator('details.skill-notes summary').textContent(),/^Read the change and 6 notes$/);
  const update=card.locator('[data-skill-update]');
  assert.equal(await update.textContent(),'Update Listing swaps');
  await update.click();
  const dialog=page.locator('#skill-update');await dialog.waitFor();
  assert.equal(await dialog.locator('h2').textContent(),'Update Listing swaps?');
  assert.deepEqual(await dialog.locator('.skill-ba h4').allTextContents(),['Before','After']);
  assert.equal(await dialog.locator('.skill-ba > div:first-child .skill-body').textContent(),old);
  assert.equal(await dialog.locator('ins').textContent(),body);
  assert.equal(posts.filter(p=>p.action==='decide').length,0,'nothing applied before Update skill');
  const box=await dialog.boundingBox();assert.ok(box.x>=0&&box.x+box.width<=width,'the dialog fits '+width);
  if(shots)await page.screenshot({path:`${shots}/${tag}-update-dialog.png`});
  await dialog.locator('#skill-update-cancel').click();
  assert.equal(await dialog.isVisible(),false);
  assert.equal(posts.filter(p=>p.action==='decide').length,0,'Cancel applies nothing');
  // A skill that changed meanwhile: the error stays in the dialog
  cards[2].skill_proposal.update.review='stale';
  await page.evaluate(()=>refresh());await update.click();await dialog.locator('#skill-update-ok').click();
  await page.locator('#skill-update-error').getByText('changed since').waitFor();
  cards[2].skill_proposal.update.review='tok1';
  await dialog.locator('#skill-update-cancel').click();await page.evaluate(()=>refresh());
  await update.click();await dialog.locator('#skill-update-ok').click();
  await page.waitForFunction(()=>!document.querySelector('#skill-update').open);
  const sent=posts.filter(p=>p.action==='decide').at(-1);
  assert.deepEqual([sent.suggestion_id,sent.choice,sent.reviewed],['u1','accept','tok1']);
  posts.length=0;await context.close();
 }
 assert.deepEqual(errors,[]);
 console.log('skill update dashboard ok');
}finally{await browser?.close();server.close()}
