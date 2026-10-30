import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Ask to review on the dashboard (dashboard/todos-review.js), both sides: the owner picks a teammate from More, sees
// "Waiting for Pat's review" with Withdraw, then Pat's tracked changes to accept (all or some) or ignore; the reviewer
// edits the draft on their own review to-do and sends it back. The fake server answers like the service would; no
// button here sends an email (no confirm action is ever called). REVIEW_SHOTS=<folder> also saves screenshots.
const dashboard=await dashboardPage(),SHOTS=process.env.REVIEW_SHOTS;
const FL='fl_'+'a'.repeat(16),now=new Date().toISOString();
const BODY='Hi Sam,\n\nThanks for your call today.\nThe price is 40 euro per seat.\n\nBest,\nOwner';
const draft={kind:'email',label:'Send to Sam',revision:'v1',account_id:'work',to:['sam@client.example'],to_name:'Sam',subject:'Pricing',body:BODY};
const owner={id:'c1',title:'Reply to Sam about pricing',body:'Sam asked for pricing. A reply is ready.',status:'prepared',event_ids:[1],scope:'work',created_at:now,next_actions:[draft]};
const reviewer={id:'r1',title:'Review: Reply to Sam about pricing',body:'Owner asks for your review. Their note: “Is the tone ok?”',status:'pending',event_ids:[2],scope:'work',created_at:now,
 review_in:{id:'q_1',from:'Owner Example',what:'draft',subject:'Pricing',to:'sam@client.example',note:'Is the tone ok?',body:BODY,stage:'open',open:true,reply:null}};
const state={suggestions:[owner],connectors:[],suggestion_counts:{prepared:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],fleet:{on:true,waiting:0,reviews:['work']}};
const view={on:true,kinds:{},fleets:[],waiting:[],asked:[],intro_offers:[],splits:[],log:[],notices:[]};
const hunks=[{id:'s',field:'subject',old:'Pricing',new:'Pricing for 40 seats',words:[['=','Pricing'],['+',' for 40 seats']]},
 {id:'b0',field:'body',old:'Thanks for your call today.\nThe price is 40 euro per seat.',new:'Thanks for the call today.\nThe price is 38 euro per seat.',
  words:[['=','Thanks for '],['-','your'],['+','the'],['=',' call today.\nThe price is '],['-','40'],['+','38'],['=',' euro per seat.']]},
 {id:'b1',field:'body',old:'',new:'PS: happy to talk.',words:[['+','PS: happy to talk.']]}];
const calls=[],last=()=>calls.filter(x=>x.action.startsWith('fleet_review')).at(-1);  // the page also says which drafts were seen (draft_seen)
const server=createServer(async(req,res)=>{res.setHeader('Content-Type','application/json');
 if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(req.url==='/api/status'){res.end(JSON.stringify(state));return}
 if(req.url==='/api/action'){let body='';for await(const b of req)body+=b;const call=JSON.parse(body);calls.push(call);const a=call.action;
  if(a==='fleet_review_options'){res.end(JSON.stringify({suggestion_id:'c1',scope:'work',what:'draft',title:owner.title,subject:'Pricing',to:'sam@client.example',body:BODY,
   fleets:[{id:FL,name:'Acme',members:[{member_id:'pat1',name:'Pat Doe'},{member_id:'lee1',name:'Lee Roe'}]}],sources:[{kind:'email',label:'Sam Lee: Pricing question'}],open:null}));return}
  if(a==='fleet_review_ask'){owner.review={id:'q_1',name:'Pat Doe',stage:'asked',line:'Waiting for Pat’s review',changes:0,decided:null,open:true,at:now}}
  if(a==='fleet_review_withdraw')delete owner.review;
  if(a==='fleet_review_view'){res.end(JSON.stringify({id:'q_1',name:'Pat Doe',stage:'changes',at:now,decided:null,what:'draft',comment:owner.review.comment,hunks,changed_since:false}));return}
  if(a==='fleet_review_apply'){Object.assign(owner.review,{decided:'partial',line:'Accepted some of Pat’s changes'});res.end(JSON.stringify({ok:true,applied:2,missed:0}));return}
  if(a==='fleet_review_reply'){Object.assign(reviewer,{status:'completed'});reviewer.review_in.stage=call.args.stage;res.end(JSON.stringify({ok:true,stage:call.args.stage,changes:2}));return}
  res.end(JSON.stringify({ok:true}));return}
 if(req.url.startsWith('/api/fleet')){res.end(JSON.stringify(view));return}
 res.statusCode=404;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const sizes=SHOTS?[[1440,900],[390,844]]:[[390,844]],schemes=SHOTS?['light','dark']:['light'];
const shot=async(page,card,name,w,scheme)=>{if(!SHOTS)return;await page.evaluate(()=>{clearTimeout(toastTimer);$('#toast').classList.remove('show')});await page.waitForFunction(()=>getComputedStyle($('#toast')).opacity==='0'||getComputedStyle($('#toast')).visibility==='hidden');await page.locator('#task-'+card).scrollIntoViewIfNeeded();
 await page.locator('#task-'+card).screenshot({path:`${SHOTS}/${name}-${w}-${scheme}.png`});await page.screenshot({path:`${SHOTS}/${name}-${w}-${scheme}-page.png`})};
const reset=()=>{delete owner.review;state.suggestions=[owner];state.suggestion_counts={prepared:1};Object.assign(reviewer,{status:'pending'});reviewer.review_in.stage='open'};
try{for(const [w,h] of sizes)for(const colorScheme of schemes){reset();
 const page=await (await browser.newContext({viewport:{width:w,height:h},colorScheme})).newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);
 const c=page.locator('#task-c1');await c.waitFor();
 // 1. More > Ask to review: the picker, with who, what goes and a note
 await c.locator('details.more-actions>summary').click();
 const ask=c.locator('[data-review-ask]');assert.equal(await ask.innerText(),'Ask to review');await ask.click();
 const form=c.locator('.review-form');await form.waitFor();
 assert.match(await form.innerText(),/Your draft[\s\S]*Pricing[\s\S]*40 euro/);
 assert.match(await form.innerText(),/Sam Lee: Pricing question/);
 assert.equal(await form.locator('input[name=to]').count(),2);
 await form.locator('textarea[name=note]').fill('Is the tone ok?');
 await shot(page,'c1','1-ask-picker',w,colorScheme);
 await form.locator('button.primary').click();await page.waitForTimeout(300);
 assert.deepEqual(last(),{action:'fleet_review_ask',args:{suggestion_id:'c1',fleet:FL,member_id:'pat1',note:'Is the tone ok?',sources:[0]}});
 // 2. Waiting: the line and Withdraw; Send stays the owner's and was not pressed
 await page.locator('#task-c1 .review-line').waitFor();
 assert.match(await page.locator('#task-c1 .review-line').innerText(),/Waiting for Pat’s review · Withdraw/);
 await shot(page,'c1','2-owner-waiting',w,colorScheme);
 // 3. The reviewer's own review to-do: the draft to edit, a comment, Approve / Send changes / Decline
 state.suggestions=[reviewer];state.suggestion_counts={pending:1};await page.evaluate(()=>refresh());
 const r=page.locator('#task-r1');await r.waitFor();
 const rf=r.locator('form.review-in');await rf.waitFor();
 assert.equal(await r.locator('[data-choice]').count(),0);  // none of the usual to-do buttons on an open review
 assert.equal(await rf.locator('button.primary').innerText(),'Approve');
 await rf.locator('textarea[name=body]').fill(BODY.replace('your call','the call').replace('40 euro','38 euro'));
 await rf.locator('textarea[name=comment]').fill('Lower price, they are a good fit.');
 assert.equal(await rf.locator('button.primary').innerText(),'Send changes');
 assert.match(await rf.innerText(),/Edited/);
 await shot(page,'r1','3-reviewer-editing',w,colorScheme);
 await rf.locator('button.primary').click();await page.waitForTimeout(300);
 assert.equal(last().action,'fleet_review_reply');assert.equal(last().args.stage,'changes');assert.match(last().args.body,/38 euro/);
 // 4. Back on the owner's to-do: Pat suggested changes, the tracked changes with boxes, Accept selected
 Object.assign(owner.review,{stage:'changes',line:'Pat suggested 3 changes',changes:3,open:false,comment:'Lower price, they are a good fit.'});
 state.suggestions=[owner];state.suggestion_counts={prepared:1};await page.evaluate(()=>refresh());
 await page.locator('#task-c1 [data-review-see]').click();
 const tc=page.locator('#task-c1 .review-changes');await tc.waitFor();
 assert.equal(await tc.locator('input[name=pick]').count(),3);
 assert.equal(await tc.locator('del').first().innerText(),'your');assert.equal(await tc.locator('ins').nth(1).innerText(),'the');
 assert.match(await page.locator('#task-c1').innerText(),/Lower price, they are a good fit\./);
 assert.equal(await tc.locator('[data-review-hide]').innerText().then(x=>/Pat’s changes/.test(x)),true);  // the header folds it; no Hide button
 assert.deepEqual(await tc.locator('.actions button').allInnerTexts(),['Accept all','Ignore']);  // all ticked: Accept selected would say the same
 await tc.locator('input[name=pick]').nth(1).uncheck();
 assert.equal(await tc.locator('.review-hunk').nth(1).getAttribute('class'),'review-hunk off');  // dimmed: it won't go in
 assert.deepEqual(await tc.locator('.actions button').allInnerTexts(),['Accept selected','Accept all','Ignore']);
 assert.equal(await tc.locator('button.primary').innerText(),'Accept selected');
 await shot(page,'c1','4-owner-changes',w,colorScheme);
 await tc.locator('[data-review-apply=some]').click();await page.waitForTimeout(300);
 assert.deepEqual(last(),{action:'fleet_review_apply',args:{suggestion_id:'c1',picks:['s','b1']}});
 assert.match(await page.locator('#task-c1 .review-line').innerText(),/Accepted some of Pat’s changes/);
 assert.ok(!calls.some(x=>/confirm|send/.test(x.action)),'nothing was sent');
 assert.deepEqual(errors,[]);
 await page.context().close()}
 console.log('fleet review dashboard ok')}
finally{await browser.close();server.close()}
