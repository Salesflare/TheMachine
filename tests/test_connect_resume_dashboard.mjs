import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections, + Add, picking up where the owner left off (connect_running): a new Machine's Gmail setup through their
// own Google app, left at Google's step, opens there again on Connections after a reload, in plain words with a button
// for Google and never a file path. Cancel goes straight back to the list. Not paired yet, the Google sign-in says
// which account pairing is about. The form's Google address fills in an empty Company, which says what a freelancer
// puts there. SHOTS=<folder> saves screenshots.
const dashboard=await dashboardPage();
const EMAIL='jules@moreaudesign.example',URL_='https://accounts.google.com/o/oauth2/v2/auth?client_id=x&state=s1&login_hint=jules%40moreaudesign.example';
const RUN={session:'s1',state:'running',label:'Gmail',source:'gmail',lines:[],question:{id:2,kind:'ask',prompt:'The address Google sent you to',default:'',google:{url:URL_,email:EMAIL,again:false}}};
let calls=[],running=true;
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action,args}=JSON.parse(body);calls.push({action,args});
  if(action==='connect_running'){res.end(JSON.stringify(running?RUN:{}));return}
  if(action==='connect_poll'){res.end(JSON.stringify(running?RUN:{...RUN,state:'cancelled',question:null,error:'Stopped'}));return}
  if(action==='connect_cancel'){running=false;res.end(JSON.stringify({...RUN,state:'cancelled',question:null}));return}
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:null,paired:false,sources:[
   {name:'gmail',service:'gmail',label:'Gmail',group:'mail',what:'Your email, what comes in and what you send.',connected:0,broker:false,signin:'google',form:{ask:[['email','Google account']],secret:null,scope:true,company:''}},
   {name:'calendar',service:'calendar',label:'Google Calendar',group:'mail',what:'Your meetings.',connected:0,broker:false,signin:'google',form:{ask:[['email','Google account']],secret:null,scope:true,company:''}}]}));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const shot=async(page,name)=>{if(shots)await page.screenshot({path:`${shots}/${name}.png`})};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const [width,height] of [[1440,900],[390,844]]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>{errors.push(e.message);if(process.env.STACK)console.log(e.stack)});
  const tag=`${width}-${scheme}`,pane=page.locator('#connect-add');
  calls=[];running=true;

  // A reload with Google's step under way: Connections opens on + Add at that step, in the dashboard's own words
  await page.goto(base+'/#connections');
  const steps=pane.locator('.connect-google');await steps.waitFor();
  const text=await pane.innerText();
  assert.match(text,/Sign in as jules@moreaudesign\.example and allow read-only access\./);
  assert.match(text,/Copy its whole address and paste it here\./);
  assert.doesNotMatch(text,/keyring|\/home\/|gog |accounts\.google\.com|terminal/i);
  assert.equal(await pane.locator('a.btn-link',{hasText:'Open Google'}).getAttribute('href'),URL_);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`resume-google-${tag}`);

  // Cancel: straight back to the list, and the setup ends on the Machine
  await pane.locator('[data-connect-stop]').click();
  await pane.locator('[data-connect-signin="gmail"]').waitFor();
  assert.equal(await pane.locator('.connect-google').count(),0);
  assert.ok(calls.some(c=>c.action==='connect_cancel'&&c.args.session==='s1'));

  // Not paired: which account pairing is about, and your own app right under it
  await pane.locator('[data-connect-signin="gmail"]').click();
  await pane.locator('.connect-signin').waitFor();
  assert.match(await pane.innerText(),/Sign in with Google goes through your account on themachine\.computer\./);
  await shot(page,`pair-${tag}`);

  // The form: the Google address fills in an empty Company; one typed there stays
  assert.equal(await pane.locator('details.connect-other').getAttribute('open'),'');  // not paired: your own app shows open (#936)
  await pane.locator('[data-connect="gmail"]').click();
  const form=pane.locator('form[data-connect-setup="gmail"]');await form.waitFor();
  await form.locator('input[data-key="email"]').fill(EMAIL);
  assert.equal(await form.locator('input[name="company"]').inputValue(),'Moreaudesign');
  assert.match(await form.innerText(),/Working for yourself\? Use your business name\./);
  await shot(page,`form-${tag}`);
  await form.locator('input[name="company"]').fill('Moreau Design');
  await form.locator('input[data-key="email"]').fill('jules@studio.example.com');
  assert.equal(await form.locator('input[name="company"]').inputValue(),'Moreau Design');
  await form.locator('input[name="company"]').fill('');
  await form.locator('input[data-key="email"]').fill('jules@gmail.com');
  assert.equal(await form.locator('input[name="company"]').inputValue(),'');  // webmail: nothing to guess
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
