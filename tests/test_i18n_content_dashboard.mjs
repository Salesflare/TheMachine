import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The UI translator (the i18n script in dashboard.html) translates the app's words, never what someone wrote: a card's
// title and body, a chat message, an event's title. In Dutch "Change the intro." once read "the intro. wijzigen" (the
// frame "Change {}"). A card's source date reads in the UI language in the region's order, whichever language it was
// stored in ("di 27 okt" in an English UI with an en-BE locale reads "Tue 27 Oct"), and so do Done rows already loaded
// when the language changes. Words glued to a value ("Hand to Codex") read translated as a whole.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const cats={};for(const l of ['en','nl','fr','de','es','it','pt-BR'])cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const languages={en:'English',nl:'Nederlands',fr:'Français'};
const view=language=>({locale:'en-BE',region:'BE',language,language_set:true,clock:'auto',hour12:false,auto_hour12:false,
 date_locale:language==='en'?'en-GB':language+'-BE',languages,saveable:true});
const now=new Date().toISOString(),day=new Date(Date.now()-864e5*2);
const done=new Date(Date.UTC(day.getUTCFullYear(),day.getUTCMonth(),day.getUTCDate(),12)).toISOString();
const cards=[{id:'c1',title:'Change project',body:'Change the intro.',status:'pending',scope:'work',created_at:now,event_ids:[1],source_line:'Source: WhatsApp from Sam · di 27 okt'},
 {id:'c2',title:'Plan the offsite',body:'**Change the venue**\nThey want a bigger room.',status:'pending',scope:'work',created_at:now,event_ids:[2],source_line:'Source: email from Sam · Tue, Oct 27'}];
let locale=view('nl');
const doneCards=[{id:'d1',title:'Send the deck',body:'Sent.',status:'completed',scope:'work',created_at:done,closed_at:done,event_ids:[3]}];
const state=()=>({suggestions:[...cards,...doneCards],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]},agents:{tools:[{id:'codex',name:'Codex',ready:true}]},locale});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 res.setHeader('Content-Type','application/json');
 const cat=/^\/i18n\/(\w\w(?:-[A-Z]{2})?)\.json$/.exec(url.pathname);if(cat){res.end(cats[cat[1]]||'{}');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/cards/done'){res.end(JSON.stringify({cards:doneCards,next:null,total:1}));return}
 if(url.pathname==='/api/action'){const {action,args}=JSON.parse(body||'{}');if(action==='set_locale'){locale=view(args.language);res.end(JSON.stringify(locale));return}}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:900},timezoneId:'UTC',locale:'nl-BE'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-c1').waitFor();
 await page.waitForFunction(()=>document.documentElement.lang==='nl'&&(document.querySelector('#open-settings')?.innerText||'').includes('Instellingen'));
 const read=()=>page.evaluate(()=>({title:document.querySelector('#task-c1 h3').innerText.trim(),body:document.querySelector('#task-c1 .body').innerText.trim(),
  lead:document.querySelector('#task-c2 .lead-line')?.innerText.trim(),date:document.querySelector('#task-c1 .src-date')?.innerText.trim(),
  date2:document.querySelector('#task-c2 .src-date')?.innerText.trim(),
  // a frame's hole holds a name or a message as written, unless it is a catalog entry itself
  hole:I18N.cat?i18nLookup('Hand to Change the intro.'):null,
  hand:t('Hand to {}','Codex')}));
 let got=await read();
 assert.equal(got.title,'Change project');
 assert.equal(got.body,'Change the intro.');
 assert.equal(got.lead,'Change the venue');
 assert.equal(got.hand,'Overdragen aan Codex');
 assert.equal(got.hole,'Overdragen aan Change the intro.');
 assert.match(got.date,/^di 27 okt\.?$/);
 assert.match(got.date2,/^di 27 okt\.?$/);
 // English, en-BE: the date words follow the UI language, the region only the order
 await page.evaluate(()=>{document.querySelector('#open-settings').click()});
 await page.locator('#settings-tabs [data-settings-tab="general"]').click();
 await page.locator('#locale-language').selectOption('en');
 await page.waitForFunction(()=>document.documentElement.lang==='en');
 await page.locator('nav [data-tab="inbox"]').click();
 await page.waitForFunction(()=>/Tue/.test(document.querySelector('#task-c1 .src-date')?.innerText||''));
 got=await read();
 assert.equal(got.date,'Tue 27 Oct');
 assert.equal(got.date2,'Tue 27 Oct');
 assert.equal(got.body,'Change the intro.');
 // Done rows loaded in English read French after the switch (built again, not the kept English rows)
 await page.locator('#finished-list summary').click();
 await page.waitForFunction(()=>/Send the deck/.test(document.querySelector('[data-pager^="done:"] .pager-rows')?.innerText||''));
 const before=await page.locator('[data-pager^="done:"] .pager-rows').innerText();
 assert.match(before,/\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b|ago|Yesterday|days/,before);
 await page.evaluate(()=>{document.querySelector('#open-settings').click()});
 await page.locator('#settings-tabs [data-settings-tab="general"]').click();
 await page.locator('#locale-language').selectOption('fr');
 await page.waitForFunction(()=>document.documentElement.lang==='fr');
 await page.locator('nav [data-tab="inbox"]').click();
 await page.waitForFunction(()=>/mar\.? 27 oct/.test(document.querySelector('#task-c1 .src-date')?.innerText||''));
 got=await read();
 assert.equal(got.title,'Change project');
 assert.equal(got.body,'Change the intro.');
 const rows=await page.evaluate(()=>[...document.querySelectorAll('[data-pager^="done:"] .pager-rows')].map(e=>e.innerText));
assert.ok(rows.length&&rows.every(r=>/Send the deck/.test(r)),JSON.stringify(rows));
 for(const r of rows)assert.doesNotMatch(r,/\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b/,r);
 assert.deepEqual(errors,[]);
 console.log('i18n content dashboard: ok');
}finally{await browser?.close();server.close()}
