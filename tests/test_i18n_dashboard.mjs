import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Languages (i18n/, the i18n script in dashboard.html): a Machine whose language was never chosen takes the browser's on
// the first load and saves it once; Settings, General, Language switches the whole page at once, text that renders later
// included, and back to English without a reload. Words around filled-in parts ("{} · {} today") and plurals read
// translated too, and rows of parts joined by " · " part by part; t() is the same lookup for code. English is untouched when the language is English.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const cats={};for(const l of ['en','nl','fr','de','es'])cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const languages={en:'English',nl:'Nederlands',fr:'Français',de:'Deutsch',es:'Español'};
const view=(language,set=true)=>({locale:'en-BE',region:'BE',language,language_set:set,clock:'auto',hour12:false,auto_hour12:false,
 date_locale:language==='en'?'en-GB':language+'-BE',languages,saveable:true});
let locale=view('en',false),saved=[],asked=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 const cat=/^\/i18n\/(\w\w)\.json$/.exec(url.pathname);if(cat){asked.push(cat[1]);res.end(cats[cat[1]]||'{}');return}
 if(url.pathname==='/api/action'){let body='';req.on('data',c=>body+=c);req.on('end',()=>{const {action,args}=JSON.parse(body);
  if(action!=='set_locale'){res.end('{}');return}saved.push(args);if(args.language)locale=view(args.language);res.end(JSON.stringify(locale))});return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
  hours:{days:[1,2,3,4,5],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC',saveable:true},locale}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const open=async(lang)=>{const context=await browser.newContext({viewport:{width:1440,height:900},timezoneId:'UTC',locale:lang}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));await page.goto(base+'/');await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});return [context,page]};
const settingsLabel=page=>page.locator('#open-settings').innerText();
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // Never chosen: the browser's language (de-DE), saved once, and the page reads German.
 let [context,page]=await open('de-DE');
 await page.waitForFunction(()=>document.documentElement.lang==='de');
 assert.deepEqual(saved,[{language:'de'}]);
 assert.equal((await settingsLabel(page)).trim(),'Einstellungen');
 // Settings, General: French, then back to English, without a reload.
 await navClick(page.locator('#open-settings'));
 await page.locator('#settings-tabs [data-settings-tab="general"]').click();
 assert.equal(await page.locator('#locale-language').inputValue(),'de');
 assert.equal(await page.locator('#locale-language option[value="fr"]').innerText(),'Français');
 await page.locator('#locale-language').selectOption('fr');
 await page.waitForFunction(()=>document.documentElement.lang==='fr');
 assert.deepEqual(saved.at(-1),{language:'fr'});
 assert.equal((await settingsLabel(page)).trim(),'Paramètres');
 assert.equal(await page.locator('#settings-locale strong').first().innerText(),'Langue');
 assert.equal(await page.locator('#locale-language-note').innerText(),'Quelques écrans sont encore en anglais.');
 // Text rendered later, with filled-in parts and plurals, and t() for code.
 const later=await page.evaluate(()=>{const p=document.createElement('p');p.textContent='Forgot 1 saved sign-in.';document.body.append(p);
  const q=document.createElement('p');q.textContent='Forgot 3 saved sign-ins.';document.body.append(q);
  return new Promise(r=>setTimeout(()=>r([p.textContent,q.textContent,t('Language'),t('Forgot {} saved sign-ins.',2),t('Not in a catalog {}',4),i18nLookup('Connected account · Your calendar · alex@example.com')]),50))});
 assert.deepEqual(later,['1 identifiant enregistré oublié.','3 identifiants enregistrés oubliés.','Langue','2 identifiants enregistrés oubliés.','Not in a catalog 4','Compte connecté · Votre agenda · alex@example.com']);
 await page.locator('#locale-language').selectOption('en');
 await page.waitForFunction(()=>document.documentElement.lang==='en');
 assert.equal((await settingsLabel(page)).trim(),'Settings');
 assert.equal(await page.locator('#settings-locale strong').first().innerText(),'Language');
 assert.equal(await page.locator('#locale-language-note').innerText(),'');
 await context.close();
 // Chosen already (English) with a Dutch browser: stays English, nothing saved, no catalog fetched.
 locale=view('en');saved=[];asked=[];
 [context,page]=await open('nl-BE');
 await page.waitForTimeout(300);
 assert.deepEqual(saved,[]);assert.deepEqual(asked,[]);
 assert.equal((await settingsLabel(page)).trim(),'Settings');
 await context.close();
 // Chosen Dutch: the next start reads Dutch at once, from the copy kept on the device.
 locale=view('nl');
 [context,page]=await open('en-US');
 await page.waitForFunction(()=>document.documentElement.lang==='nl');
 assert.equal((await settingsLabel(page)).trim(),'Instellingen');
 await page.reload();
 assert.equal(await page.evaluate(()=>document.documentElement.lang),'nl');  // before any state arrives
 await context.close();
 assert.deepEqual(errors,[]);
 console.log('i18n dashboard: ok');
}finally{await browser?.close();server.close()}
