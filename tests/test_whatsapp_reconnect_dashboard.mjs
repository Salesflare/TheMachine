import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// WhatsApp logged the Machine out: Reconnect in Needs you opens WhatsApp's own setup in Chat, also when the list of
// sources hasn't come yet (it did open on Email, under an email's Disconnected lately row). It asks the phone number,
// never a store folder, and says "linked" only once linked. A step that took too long says so and what to do, never
// "stopped unexpectedly". All mocked. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const at=new Date().toISOString();
const connectors=[{id:'personal-whatsapp',service:'whatsapp',group:'chat',boundary:'personal',display_name:'Alex’s WhatsApp',error:'whatsapp_unlinked',
 error_at:at,retry_at:new Date(Date.now()+3e5).toISOString(),failures:3,connect_name:'whatsapp',sync_activity:[{at,status:'failed',error:'whatsapp:whatsapp_unlinked'}]}];
const disconnected=[{group:'mail',mark:'gmail',card_title:'old@example.com',card_subtitle:'Google account',at:new Date(Date.now()-864e6).toISOString(),state:'done',provider_name:'Google'}];
const RUN={session:'w1',state:'running',label:'WhatsApp',source:'whatsapp',group:'chat',reconnect:'personal-whatsapp',lines:[]};
const PHONE={...RUN,question:{id:1,kind:'ask',prompt:'Your WhatsApp phone number, with its country code (+32 470 12 34 56)',default:''}};
let step=PHONE,actions=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],connectors,disconnected}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);actions.push([action,args]);
  // the list of sources comes late, as on a phone that opened on To-dos: the setup must not wait on it for its kind
  if(action==='connect_sources'){await new Promise(r=>setTimeout(r,4000));res.end(JSON.stringify({saveable:true,manage_url:null,sources:[
   {name:'gmail',service:'gmail',label:'Gmail',group:'mail',what:'Your email.',connected:0,broker:false,form:{ask:[['email','Google account']],secret:null}},
   {name:'whatsapp',service:'whatsapp',label:'WhatsApp',group:'chat',what:'Your WhatsApp chats, as a linked device.',connected:1,broker:false,form:{ask:[],secret:null}}]}));return}
  if(action==='connect_start'||action==='connect_poll'||action==='connect_answer'){res.end(JSON.stringify(step));return}
  if(action==='connect_running'){res.end('{}');return}
  res.end('{}');return}
 if(url.pathname==='/api/events'){res.end('[]');return}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of [[390,844,'dark'],[1440,900,'dark'],...shots?[[390,844,'light'],[1440,900,'light']]:[]]){
  const phone=width<720,context=await browser.newContext({viewport:{width,height},colorScheme:scheme,...phone?{isMobile:true,hasTouch:true}:{}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const shot=async name=>{if(shots)await page.screenshot({path:`${shots}/${name}-${width}-${scheme}.png`,fullPage:false})};
  step=PHONE;actions=[];
  await page.goto(base);
  const banner=page.locator('#needs-you [data-reconnect="whatsapp"]');await banner.waitFor();
  await banner.click();
  const pane=page.locator('#connect-add');await pane.locator('#connect-answer').waitFor();
  assert.deepEqual(actions.find(a=>a[0]==='connect_start')[1],{name:'whatsapp',account:'personal-whatsapp'});
  assert.equal(await page.locator('#conn-title').textContent(),'Chat','WhatsApp’s own kind, not Email');
  assert.equal(await page.locator('#disconnected').textContent(),'','no email rows over the WhatsApp setup');
  const text=await pane.innerText();
  assert.match(text,/Your WhatsApp phone number/);
  assert.doesNotMatch(text,/store|wacli|\/home\/|linked, reading|stopped unexpectedly/i);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot('wa-reconnect-phone');
  // the code to enter in WhatsApp, Linked devices
  step={...RUN,code:{kind:'pair',code:'K7P2-9QX4'}};
  await pane.locator('#connect-answer').fill('+32 470 12 34 56');await pane.locator('[data-connect-form] button.primary').click();
  await pane.locator('.connect-code',{hasText:'K7P2-9QX4'}).waitFor();
  assert.match(await pane.innerText(),/Link with phone number instead/);
  assert.equal(await page.locator('#conn-title').textContent(),'Chat');
  await new Promise(r=>setTimeout(r,4500));  // the list of sources has come: still Chat
  assert.equal(await page.locator('#conn-title').textContent(),'Chat');
  await shot('wa-reconnect-code');
  // linked, then the setup failed after all: the Machine sends a failed setup without the steps that went well
  // (ConnectApp.connect_view), so "linked" never stands above the failure
  step={...RUN,lines:['WhatsApp: linked']};
  await pane.locator('.connect-lines li',{hasText:'WhatsApp: linked'}).waitFor({timeout:8000});
  step={...RUN,state:'failed',lines:[],error:'The setup stopped unexpectedly',fix:'try again'};
  await pane.locator('.alert').waitFor({timeout:8000});
  assert.doesNotMatch(await pane.innerText(),/linked/i);
  await shot('wa-reconnect-failed');
  step={...RUN,code:{kind:'pair',code:'K7P2-9QX4'}};await pane.locator('[data-connect="whatsapp"]').click();
  await pane.locator('.connect-code').waitFor({timeout:8000});
  // a step that took too long: what happened and what to do, with Try again for this account
  step={...RUN,state:'failed',error:'It took too long to answer',fix:'try again in a minute'};
  await pane.locator('.alert').waitFor({timeout:8000});
  assert.equal(await pane.locator('.alert').textContent(),'It took too long to answer. Try again in a minute.');
  assert.equal(await pane.locator('[data-connect="whatsapp"]').getAttribute('data-connect-account'),'personal-whatsapp');
  assert.doesNotMatch(await pane.innerText(),/linked, reading|stopped unexpectedly|terminal/i);
  await shot('wa-reconnect-timeout');
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
