import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, General, Language and region (locale_prefs.py): Region and Time format save at once, and every time on the
// page follows: Updated in the header, the sample under Region. A Machine without a region shows Not set and keeps
// 24-hour times, unless the browser says where it is: then that region is saved on first load. At 390px the row stays inside the screen. SHOTS=<folder> saves light and dark screenshots.
const dashboard=await dashboardPage();
const H12=new Set(['US','AU','CA']),view=(region,clock='auto')=>{const auto=H12.has(region);
 return {locale:region?'en-'+region:null,region:region||'',language:'en',clock,hour12:clock==='auto'?auto:clock==='12h',auto_hour12:auto,
  date_locale:!region||region==='US'||region==='CA'?'en-US':'en-GB',languages:{en:'English'},saveable:true}};
let locale=view(''),saved=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/action'){let body='';req.on('data',c=>body+=c);req.on('end',()=>{const {action,args}=JSON.parse(body);
  if(action!=='set_locale'){res.end('{}');return}saved.push(args);
  if(args.browser){const r={'Europe/Brussels':'BE'}[args.browser.zone]||(args.browser.language.split('-')[1]||'');if(r&&!locale.region)locale=view(r,locale.clock);res.end(JSON.stringify(locale));return}
  locale=view(args.locale?args.locale.split('-')[1]:locale.region,args.clock||locale.clock);res.end(JSON.stringify(locale))});return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
  hours:{days:[1,2,3,4,5],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC',saveable:true},locale}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const errors=[];let browser;
const sample=page=>page.locator('#locale-sample').innerText(),updated=page=>page.locator('#updated').textContent();
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const width of [1440,390]){
  locale=view('');saved=[];
  const context=await browser.newContext({viewport:{width,height:900},timezoneId:'UTC',locale:'en'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#settings/general');await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
  if(!(await page.locator('#settings-locale').isVisible()))await navClick(page.locator('#open-settings'));
  await page.locator('#settings-tabs [data-settings-tab="general"]').click();
  await page.locator('#settings-locale').waitFor();
  // No region yet: Not set, US dates, 24-hour.
  assert.equal(await page.locator('#locale-region').inputValue(),'');
  assert.match(await sample(page),/^\w{3}, \w{3} \d{1,2}, 14:05$/);
  assert.equal(await page.locator('#locale-clock').inputValue(),'auto');assert.equal(await page.locator('#locale-auto').innerText(),'Automatic: 14:05');
  assert.match(await updated(page),/\d\d:\d\d/);
  // The US: 12-hour, saved at once, the header's time follows.
  await page.locator('#locale-region').selectOption('US');
  await page.locator('#locale-sample',{hasText:'PM'}).waitFor();
  assert.deepEqual(saved.at(-1),{locale:'en-US'});
  assert.match(await sample(page),/^\w{3}, \w{3} \d{1,2}, 2:05 PM$/);
  assert.match(await updated(page),/\d{1,2}:\d\d [AP]M/);
  // Belgium: day first, 24-hour; then Time format 12-hour overrides the region.
  await page.locator('#locale-region').selectOption('BE');
  await page.locator('#locale-sample',{hasText:'14:05'}).waitFor();
  assert.match(await sample(page),/^\w{3} \d{1,2} \w{3}, 14:05$/);
  await page.locator('#locale-clock').selectOption('12h');
  await page.locator('#locale-sample',{hasText:'PM'}).waitFor();
  assert.deepEqual(saved.at(-1),{clock:'12h'});
  assert.equal(await page.locator('#locale-region').inputValue(),'BE');
  assert.equal(await page.locator('#locale-auto').innerText(),'Automatic: 14:05');  // Belgium's own
  const fits=await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
  assert.equal(fits,true,'Settings fits at '+width);
  if(process.env.SHOTS)for(const theme of ['light','dark']){
   await page.evaluate(t=>{document.cookie='theme='+t+';path=/';localStorage.setItem('theme',t);document.documentElement.dataset.theme=t},theme);
   await page.locator('#settings-locale').scrollIntoViewIfNeeded();
   await page.screenshot({path:`${process.env.SHOTS}/after-${width}-${theme}.png`})}
  await context.close()}
 // A Machine without a region, opened in Brussels: Belgium, saved once on first load, never over a choice.
 {locale=view('');saved=[];
  const context=await browser.newContext({viewport:{width:1440,height:900},timezoneId:'Europe/Brussels',locale:'en-US'}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/#settings/general');await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
  if(!(await page.locator('#settings-locale').isVisible()))await navClick(page.locator('#open-settings'));
  await page.locator('#settings-tabs [data-settings-tab="general"]').click();
  await page.waitForFunction(()=>document.querySelector('#locale-region')?.value==='BE');
  assert.deepEqual(saved,[{browser:{zone:'Europe/Brussels',language:'en-US'}}]);
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('locale dashboard: ok');
}finally{await browser?.close();server.close()}
