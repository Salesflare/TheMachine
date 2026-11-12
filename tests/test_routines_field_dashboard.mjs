import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {mkdirSync} from 'node:fs';
import {readFile} from 'node:fs/promises';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// The Routines page's field (dashboard/routines-page.js rtGrow) looks like a one-line field and grows with its words. With
// classic scrollbars (Windows), a height a fraction of a pixel short of its text showed the scrollbar arrows in an empty
// field; it scrolls only once it is at its tallest. Run with SHOTS=<dir> for screenshots.
const dashboard=await dashboardPage();
const now=new Date().toISOString(),ID='c4'.repeat(16);
const routines=JSON.stringify({routines:[{id:ID,name:'Shipped this week',instructions:'Check what shipped in the project repository and write a short post',rule:{unit:'week',n:1},
 anchor:'2026-11-13',at:'16:00',state:'on',next_due:'2026-11-13',runs:[{id:'r1',state:'ready',started_at:now,result:'**Three things shipped**.'}]}],suggested:[],trying:[]});
let language='en';
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:true,fleets:[]},
 locale:{locale:language+'-BE',region:'BE',language,language_set:true,clock:'auto',hour12:false,auto_hour12:false,date_locale:language+'-BE',languages:{en:'English',nl:'Nederlands'},saveable:true}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/routines'){res.end(routines);return}
 const cat=/^\/i18n\/(\w\w)\.json$/.exec(url.pathname);if(cat){res.end(await readFile(new URL(`../i18n/${cat[1]}.json`,import.meta.url),'utf8').catch(()=>'{}'));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)mkdirSync(shots,{recursive:true});
const errors=[];let browser;
// What the field shows: its height, and whether its text is taller than its box (a classic scrollbar then shows)
const look=x=>x.evaluate(e=>({h:e.getBoundingClientRect().height,over:e.scrollHeight-e.clientHeight,bar:e.offsetWidth-e.clientWidth-parseFloat(getComputedStyle(e).borderLeftWidth)-parseFloat(getComputedStyle(e).borderRightWidth),
 y:getComputedStyle(e).overflowY,max:parseFloat(getComputedStyle(e).maxHeight)}));
try{
 // Classic scrollbars, as on Windows: they take room and show their arrows whenever anything overflows (Playwright hides
 // them by default when headless). At 150% display scaling, common on Windows laptops, a height that rounds a fraction of
 // a pixel short showed them even when scrollHeight equals clientHeight.
 for(const dsf of ['1','1.5']){await browser?.close();
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,ignoreDefaultArgs:['--hide-scrollbars'],
  args:['--no-sandbox','--disable-dev-shm-usage','--disable-features=OverlayScrollbar','--force-device-scale-factor='+dsf]});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark'])for(const lang of ['en','nl']){language=lang;
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme,locale:lang+'-BE'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port+'/#routines');await page.locator(`[data-rt="${ID}"]`).waitFor();
  if(lang!=='en')await page.waitForFunction(l=>document.documentElement.lang===l,lang);
  const w=page.locator('#rt-words'),at=`${width} ${scheme} ${lang} at ${dsf}x`,form=page.locator('.rt-new');
  if(lang==='nl')await page.waitForFunction(()=>document.querySelector('#rt-words')?.placeholder==='Elke dag, vat mijn deals samen');
  // Empty, with its placeholder: one line, nothing to scroll
  const empty=await look(w);assert.ok(empty.over<=0&&empty.bar<2,`${at}: the empty field has no scrollbar (${JSON.stringify(empty)})`);
  if(shots&&lang==='nl'&&dsf==='1.5')await form.screenshot({path:`${shots}/routines-field-${width}-${scheme}-empty.png`});
  // Focused, then one line typed: the same height, still nothing to scroll
  await w.focus();assert.equal((await look(w)).h,empty.h,`${at}: focus keeps its height`);
  await w.pressSequentially('Elke dag');const one=await look(w);
  assert.equal(one.h,empty.h,`${at}: one line keeps its height`);assert.ok(one.over<=0&&one.bar<2,`${at}: one line has no scrollbar (${JSON.stringify(one)})`);
  // A long placeholder that wraps on a phone, and an empty field again
  await w.fill('');await w.evaluate(e=>{e.placeholder='Elke werkdag om acht uur, vat de deals samen die deze week van fase veranderden';e.dispatchEvent(new Event('input',{bubbles:true}))});
  const ph=await look(w);assert.ok(ph.over<=0&&ph.bar<2,`${at}: a long placeholder has no scrollbar (${JSON.stringify(ph)})`);
  // Three lines: it grows to fit them, still without a scrollbar
  await w.fill('Elke maandag om negen uur\nvat mijn deals van vorige week samen\nen zet de grootste bovenaan');const three=await look(w);
  assert.ok(three.h>empty.h*2,`${at}: three lines grow the field (${three.h} vs ${empty.h})`);assert.ok(three.over<=0&&three.bar<2,`${at}: three lines have no scrollbar (${JSON.stringify(three)})`);
  if(shots&&lang==='nl'&&dsf==='1.5')await form.screenshot({path:`${shots}/routines-field-${width}-${scheme}-three-lines.png`});
  // Far more than fits: at its tallest, and then it scrolls
  await w.fill('Vat mijn deals samen en zet de grootste bovenaan.\n'.repeat(20));const long=await look(w);
  assert.ok(Math.abs(long.h-long.max)<=1,`${at}: a long text stops at the tallest (${JSON.stringify(long)})`);
  assert.ok(long.over>0&&long.y==='auto'&&long.bar>5,`${at}: a long text scrolls (${JSON.stringify(long)})`);
  // Back to one line: back to one line's height, without a scrollbar
  await w.fill('Elke dag');const back=await look(w);assert.equal(back.h,empty.h,`${at}: back to one line`);assert.ok(back.over<=0&&back.bar<2,`${at}: no scrollbar again (${JSON.stringify(back)})`);
  // Edit on a routine uses the same field
  if(lang==='en'){const card=page.locator(`[data-rt="${ID}"]`);await card.locator('.more-actions>summary').click();await card.locator('[data-rt-do="edit"]').click();
   const x=card.locator('.rt-form textarea'),e=await look(x);assert.ok(e.over<=0&&e.bar<2,`${at}: Edit's field has no scrollbar (${JSON.stringify(e)})`)}
  await context.close()}}
 assert.deepEqual(errors,[]);
 console.log('routines field: no scrollbar until its tallest, at 1440 and 390, light and dark');
}finally{await browser?.close();server.close()}
