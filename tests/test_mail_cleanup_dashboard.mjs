import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {mkdir,readFile} from 'node:fs/promises';
import {join,basename} from 'node:path';
import {fileURLToPath} from 'node:url';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Routine templates (routine_templates.py, mail_cleanup.py): under Templates on the Routines page, Add turns one on and it
// leaves the list. Its to-do has a row per newsletter with Keep or Unsubscribe; nothing is sent until the one confirm, which
// names how many go, and then each row says how it went. A cleanup to-do has no Do it. Spam in read-only Gmail links to
// the mail in Gmail after the confirm, for the owner to mark there.
//   SHOTS=<folder> also saves each step at 390 and 1440, light and dark.
const SHOTS=process.env.SHOTS;if(SHOTS)await mkdir(SHOTS,{recursive:true});
const dashboard=await dashboardPage();
const now=new Date().toISOString(),posts=[];
const TEMPLATES=()=>[{key:'newsletters',name:'Newsletter cleanup',what:'Every morning, one to-do with the past day’s newsletters. Keep or unsubscribe each one.',added:false},
 {key:'spam',name:'Spam cleanup',what:'Every morning, one to-do with spam that got through. Mark each one as spam or not.',added:false}];
const news=()=>({id:'cl1',title:'5 newsletters: keep or unsubscribe?',status:'pending',scope:'work',created_at:now,event_ids:[1],
 body:'Pick Keep or Unsubscribe for each one, then confirm. Nothing changes before that.\n\n- Brightpath Weekly: This week in gardening',
 cleanup:{kind:'newsletters',items:[
  {n:1,from:'Brightpath Weekly',address:'news@brightpath.example',title:'This week in gardening',event:11,count:3,state:'open',plan:'one_click'},
  {n:2,from:'Fieldkit Team',address:'hello@fieldkit.example',title:'New tents are in',count:1,state:'open',plan:'mailto'},
  {n:3,from:'Parcelly Deals',address:'deals@parcelly.example',title:'48 hours only',count:1,state:'open',plan:'page'},
  {n:4,from:'Lumen Labels',address:'news@lumen.example',title:'Custom labels, cut to shape',count:1,state:'open',plan:'page'},
  // came through a group with no unsubscribe of the sender's own: the owner's from the start, no pick (mail_cleanup.record);
  // Unsubscribe by hand opens its mail, for its own footer
  {n:5,from:'Lee Lamps via Info',address:'news@lamps.example',title:'Lamp news',event:15,count:1,state:'yours',how:'group',plan:'hand'}]}});
// what the Machine's browser made of each unsubscribe page (unsubscribe_page.py): Parcelly's needs a login, Lumen's it finished
const PAGES={3:{state:'yours',how:'login',link:'https://parcelly.example/unsubscribe'},4:{state:'done',how:'page'}};
const spam=()=>({id:'cl2',title:'2 emails look like spam',status:'pending',scope:'work',created_at:now,event_ids:[2],
 body:'Pick Spam or Not spam for each one, then confirm. Nothing changes before that.',
 cleanup:{kind:'spam',items:[
  {n:1,from:'Prize Desk',address:'win@prize.example',title:'You have been selected',event:21,why:'Prize claim from a sender never seen',count:1,state:'open',plan:'junk'},
  {n:2,from:'Crypto Gains',address:'x@gains.example',title:'Double your money',why:'Investment pitch from an unknown sender',count:1,state:'open',plan:'junk'}]}});
// Spam in Gmail connected read-only (in_mail): Spam is the owner's own step, a link to the mail in Gmail (mail_cleanup.mail_link)
const GMAIL='https://mail.google.com/mail/u/?authuser=owner%40example.com#all/18c0ffee00000031';
const readOnly=()=>({id:'cl3',title:'1 email looks like spam',status:'pending',scope:'personal',created_at:now,event_ids:[3],
 body:'Pick Spam or Not spam for each one, then confirm. Nothing changes before that.',
 cleanup:{kind:'spam',items:[{n:0,from:'Lead Lists',address:'sales@leads.example',title:'Verified leads',why:'Cold sales pitch',count:1,state:'open',plan:'in_mail'}]}});
let templates,cards;
// the mails as the viewer gets them (api/originals); a row without event has no kept mail and no link
const ORIGINALS={11:{kind:'email',event_id:11,from:'Brightpath Weekly <news@brightpath.example>',to:'owner@example.com',occurred_at:now,title:'This week in gardening',body:'Tomatoes, at last.'},
 15:{kind:'email',event_id:15,from:'Lee Lamps via Info <news@lamps.example>',to:'owner@example.com',occurred_at:now,title:'Lamp news',body:'New shades this week.'},
 21:{kind:'email',event_id:21,from:'Prize Desk <win@prize.example>',to:'owner@example.com',occurred_at:now,title:'You have been selected',body:'Claim your prize today.'}};
// their full HTML, each with remote content: an image, a background, a font (a tracking pixel would tell the sender the
// address is live, so a mail opened from Spam cleanup loads none of it; a newsletter loads as anywhere else)
const remote=n=>`<style>@font-face{font-family:t;src:url(https://pixel.example/${n}.woff)}p{font-family:t}</style>`+
 `<div style="background:url(https://pixel.example/${n}-bg.png)"><img src="https://pixel.example/${n}.gif" width="1" height="1">`;
const HTML={11:remote('news')+'<p>Tomatoes, at last.</p></div>',15:'<p>New shades this week.</p>',21:remote('spam')+'<p>Claim your prize today.</p></div>'};
const reset=()=>{templates=TEMPLATES();cards=[news(),spam(),readOnly()];posts.length=0};reset();
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:'en-US',region:'US',language:'en',language_set:true,clock:'auto',hour12:true,auto_hour12:true,date_locale:'en-US',languages:{en:'English'},saveable:true}});
const routines=()=>JSON.stringify({routines:[],suggested:[],trying:[],templates});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/routines'){res.end(routines());return}
 if(url.pathname==='/api/originals'){const o=ORIGINALS[url.searchParams.get('event')];res.end(JSON.stringify({originals:o?[o]:[]}));return}
 if(url.pathname==='/api/email'){res.end(JSON.stringify({html:HTML[url.searchParams.get('event')]||''}));return}
 if(url.pathname.startsWith('/brand/')){try{const f=basename(url.pathname)==='avatar.png'?'app-icon-192.png':basename(url.pathname);res.setHeader('Content-Type',f.endsWith('.png')?'image/png':f.endsWith('.webp')?'image/webp':'application/octet-stream');res.end(await readFile(fileURLToPath(new URL('../brand/'+f,import.meta.url))))}catch{res.statusCode=404;res.end()}return}  // the app's own images, as machine/config.py serves them
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='routine_template'){templates=templates.map(x=>x.key===b.args.key?{...x,added:true}:x);res.end(routines());return}
  if(b.action==='routine_cleanup'){const c=cards.find(x=>x.id===b.args.suggestion_id);
   c.cleanup.items=c.cleanup.items.map(i=>{const p=b.args.picks[i.n];return p==='keep'?{...i,state:'kept'}:p!=='go'?i:i.plan==='page'?{...i,...PAGES[i.n]}:i.plan==='in_mail'?{...i,state:'yours',how:'in_mail',link:GMAIL}:{...i,state:'done',how:i.plan}});
   res.end('{"ok":true}');return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const text=async l=>(await l.innerText()).replace(/\s+/g,' ').trim();
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [390,1440])for(const scheme of SHOTS?['light','dark']:['light']){reset();const mobile=width<500;
  const context=await browser.newContext({viewport:{width,height:900},colorScheme:scheme,...(mobile?{isMobile:true,hasTouch:true}:{})});
  const outside=[];await context.route('**/*',route=>{const u=new URL(route.request().url());if(u.hostname==='127.0.0.1')return route.continue();outside.push(u.href);return route.abort()});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const shot=async name=>{if(SHOTS)await page.screenshot({path:join(SHOTS,`${name}-${width}-${scheme}.png`)})};
  await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');
  // Templates: both, with Add; an added one leaves the list
  const tpl=page.locator('#routines-view article.rt-tpl');await tpl.first().waitFor();
  assert.deepEqual(await tpl.locator('h3').allInnerTexts(),['Newsletter cleanup','Spam cleanup']);
  await tpl.first().scrollIntoViewIfNeeded();await shot('templates');
  await tpl.first().locator('[data-rt-tpl="newsletters"]').click();
  await page.locator('.toast',{hasText:'Routine added'}).waitFor();
  assert.deepEqual(await page.locator('#routines-view article.rt-tpl h3').allInnerTexts(),['Spam cleanup']);
  assert.deepEqual(posts.filter(p=>p.action==='routine_template'),[{action:'routine_template',key:'newsletters'}]);
  // The newsletter to-do: a row each, no Do it, confirm off until a pick
  await page.goto('http://127.0.0.1:'+server.address().port+'/#todos');
  const card=page.locator('#task-cl1');await card.waitFor();
  assert.equal(await card.locator('.cl-row').count(),5);
  assert.equal(await card.locator('.cl-row').nth(4).locator('[data-cl]').count(),0,'a row by hand has nothing to pick');
  assert.equal((await text(card.locator('.cl-row').nth(4).locator('.cl-end'))),'Came through a group Unsubscribe by hand');
  assert.equal(await text(card.locator('.cl-row').first().locator('.cl-what')),'Brightpath Weekly 3 emails · This week in gardening');  // the count in words, on the subtitle line
  assert.equal(await card.getByRole('button',{name:'Do it',exact:true}).count(),0,'a cleanup to-do has no Do it');
  assert.equal(await card.locator('[data-cl-open]').count(),3,'only a row with a kept mail opens');
  await card.locator('.cl-hand').click();
  await page.frameLocator('#email-dialog iframe.email-frame').getByText('New shades this week.').waitFor();
  await page.keyboard.press('Escape');await page.locator('#email-dialog').waitFor({state:'hidden'});
  await card.locator('[data-cl-open="11"]').click();
  await page.frameLocator('#email-dialog iframe.email-frame').getByText('Tomatoes, at last.').waitFor();
  await page.waitForTimeout(500);
  assert.ok(outside.some(u=>u.startsWith('https://pixel.example/news')),'a newsletter loads its images as anywhere else (the check below can see a request)');
  await page.keyboard.press('Escape');await page.locator('#email-dialog').waitFor({state:'hidden'});
  const go=card.locator('[data-cl-go]');assert.equal(await go.isDisabled(),true);
  await card.locator('[data-cl-n="1"][data-cl-to="go"]').click();
  await card.locator('[data-cl-n="2"][data-cl-to="keep"]').click();
  await card.locator('[data-cl-n="3"][data-cl-to="go"]').click();
  await card.locator('[data-cl-n="4"][data-cl-to="go"]').click();
  assert.equal(await text(card.locator('[data-cl-go]')),'Unsubscribe from 3');
  assert.equal(await card.locator('[data-cl-all]').count(),0,'every row picked: no Unsubscribe from all');
  assert.equal(await card.locator('[data-cl-n="1"][data-cl-to="go"]').getAttribute('aria-pressed'),'true');
  assert.equal(posts.filter(p=>p.action==='routine_cleanup').length,0,'nothing goes before the confirm');
  await card.scrollIntoViewIfNeeded();await shot('newsletters-todo');
  await card.locator('[data-cl-go]').click();
  await card.locator('.cl-end.ok').first().waitFor();
  assert.deepEqual(posts.filter(p=>p.action==='routine_cleanup'),[{action:'routine_cleanup',suggestion_id:'cl1',picks:{1:'go',2:'keep',3:'go',4:'go'}}]);
  // a page the Machine finished says Unsubscribed like the rest; one it couldn't says why, with its link
  assert.deepEqual((await card.locator('.cl-end').allInnerTexts()).map(s=>s.replace(/\s+/g,' ').trim()),
   ['Unsubscribed','Kept','Needs a login Open unsubscribe page ↗','Unsubscribed','Came through a group Unsubscribe by hand']);
  assert.equal(await card.locator('.cl-end a').getAttribute('href'),'https://parcelly.example/unsubscribe');
  await shot('newsletters-done');
  // Spam (only where mail can move to spam): Mark all as spam picks every row
  const sp=page.locator('#task-cl2');await sp.scrollIntoViewIfNeeded();
  assert.equal(await text(sp.locator('.cl-fine')),'Spam moves it to your spam folder.');
  // a row's sender and subject open its mail in the viewer; nothing is posted and the picks stay; no kept mail, no link
  assert.equal(await sp.locator('.cl-row').nth(1).locator('[data-cl-open]').count(),0);
  assert.equal(await text(sp.locator('.cl-row').nth(1).locator('.cl-what')),'Crypto Gains Investment pitch from an unknown sender');
  await sp.locator('[data-cl-n="2"][data-cl-to="keep"]').click();
  const sent=posts.length;
  await sp.locator('.cl-row').first().locator('[data-cl-open]').click();
  const dialog=page.locator('#email-dialog');await page.frameLocator('#email-dialog iframe.email-frame').getByText('Claim your prize today.').waitFor();
  await page.waitForTimeout(500);
  assert.deepEqual(outside.filter(u=>u.includes('pixel.example/spam')),[],'a mail opened from Spam cleanup loads nothing from outside');
  assert.equal(await page.locator('#email-title').textContent(),'You have been selected');
  await shot('spam-open');
  await page.keyboard.press('Escape');await dialog.waitFor({state:'hidden'});
  assert.equal(posts.length,sent,'opening a mail posts nothing');
  assert.equal(await sp.locator('[data-cl-n="2"][data-cl-to="keep"]').getAttribute('aria-pressed'),'true');
  assert.equal(await sp.locator('[data-cl-n="1"][data-cl-to="go"]').getAttribute('aria-pressed'),'false');
  await sp.locator('[data-cl-n="2"][data-cl-to="keep"]').click();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal scroll at '+width);
  await sp.locator('[data-cl-all]').click();
  assert.equal(await text(sp.locator('[data-cl-go]')),'Mark 2 as spam');
  assert.equal(await sp.locator('[data-cl-all]').count(),0,'every row picked: one button');
  // none picked as spam: the confirm saves Not spam
  await sp.locator('[data-cl-n="1"][data-cl-to="keep"]').click();await sp.locator('[data-cl-n="2"][data-cl-to="keep"]').click();
  assert.equal(await text(sp.locator('[data-cl-go]')),'Save picks');
  await sp.locator('[data-cl-n="1"][data-cl-to="go"]').click();await sp.locator('[data-cl-n="2"][data-cl-to="go"]').click();
  assert.equal(await text(sp.locator('[data-cl-go]')),'Mark 2 as spam');
  await shot('spam-todo');
  // read-only Gmail: the line says what Spam does there; after the confirm, the row links to the mail in Gmail
  const ro=page.locator('#task-cl3');await ro.scrollIntoViewIfNeeded();
  assert.equal(await text(ro.locator('.cl-fine')),'Gmail is read-only here, so Spam gives a link to mark it in Gmail.');
  await ro.locator('[data-cl-n="0"][data-cl-to="go"]').click();
  await shot('spam-read-only-todo');
  await ro.locator('[data-cl-go]').click();
  const mark=ro.locator('.cl-end a');await mark.waitFor();
  assert.equal(await text(mark),'Mark as spam in Gmail ↗');
  assert.equal(await mark.getAttribute('href'),GMAIL);
  assert.deepEqual(posts.filter(p=>p.suggestion_id==='cl3'),[{action:'routine_cleanup',suggestion_id:'cl3',picks:{0:'go'}}]);
  assert.match(await text(ro),/Done, except 1 to mark as spam yourself\./);
  await shot('spam-read-only-done');
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('mail cleanup dashboard ok');
}finally{await browser?.close();server.close()}
