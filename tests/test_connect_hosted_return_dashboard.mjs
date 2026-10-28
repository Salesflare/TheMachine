import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections, + Add on a hosted Machine: a sign-in started here comes back here (the control plane's /open to=connect)
// and the form says how it went: connected, or why the provider's answer was refused (#connect=<provider>/f_..., the
// reason asked from /_machine/connect-state, never read from the address). GitHub signs in right here: its code shows
// in the form, with GitHub's own device page only. SHOTS=<folder> saves screenshots.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const MANAGE='https://app.example.org/setup';
let states={},asked=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],manage_url:MANAGE}));return}
 if(url.pathname==='/_machine/connect-state'){const key=url.searchParams.get('s')+'/'+url.searchParams.get('c');asked.push(key);
  const next=states[key];if(!next){res.statusCode=404;res.end('{"error":"unknown"}');return}res.end(JSON.stringify(Array.isArray(next)?next.length>1?next.shift():next[0]:next));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:MANAGE,sources:[
   {name:'github',service:'github',label:'GitHub',what:'Review requests, mentions and failed CI runs.',connected:0,broker:false,hosted_signin:'github'},
   {name:'zoom',service:'zoom',label:'Zoom',what:'Your meetings.',connected:0,broker:true,hosted_signin:'zoom'},
   {name:'stripe',service:'stripe',label:'Stripe',what:'Payments.',connected:0,broker:false,hosted_signin:'stripe'},
   {name:'whatsapp',service:'whatsapp',label:'WhatsApp',connected:0,broker:false,account_page:'source-whatsapp'}]}));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const shot=async(page,name)=>{if(shots)await page.screenshot({path:`${shots}/${name}.png`})};
const box=page=>page.locator('#connect-add');
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // every size and theme for screenshots; a desktop and a phone otherwise (the waits are the form's own polling)
 const runs=shots?[['light',1440,900],['light',390,844],['dark',1440,900],['dark',390,844]]:[['light',1440,900],['dark',390,844]];
 for(const [scheme,width,height] of runs){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}-${scheme}`;
  // Refused at the provider: the reason, asked from the account for this very form, and Try again
  states={'zoom/f_0123456789abcdef':{state:'failed',error:'Zoom did not accept the sign-in. Connect again.'}};asked=[];
  await page.goto(base+'/#connect=zoom/f_0123456789abcdef');
  await box(page).getByText('Zoom did not accept the sign-in. Connect again.').waitFor({timeout:8000});
  assert.equal(await box(page).locator('h3').innerText(),'Zoom');
  await box(page).getByRole('button',{name:'Try again'}).waitFor();
  assert.ok(asked.includes('zoom/f_0123456789abcdef'));
  assert.equal(new URL(page.url()).hash,'','the address is cleaned up');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`return-failed-${tag}`);
  // Connected: the short note, in the form it was started from
  states={'stripe/c_0123456789abcdef':[{state:'connecting'},{state:'done'}]};
  await page.goto('about:blank');await page.goto(base+'/#connect=stripe/c_0123456789abcdef');
  await box(page).getByText('Connected.').waitFor({timeout:10000});
  assert.equal(await box(page).locator('h3').innerText(),'Stripe');
  await shot(page,`return-connected-${tag}`);
  // Stopped at the provider
  await page.goto('about:blank');await page.goto(base+'/#connect=stripe/stopped');
  await box(page).getByText('That sign-in didn’t finish.').waitFor();
  // GitHub: started on the dashboard, its code right here
  states={'github/c_00000000000000aa':[{state:'starting'},{state:'code',code:'ABCD-1234',url:'https://github.com/login/device'},{state:'code',code:'ABCD-1234',url:'https://github.com/login/device'},
   {state:'connecting'},{state:'done'}]};
  await page.goto('about:blank');await page.goto(base+'/#connect=github/c_00000000000000aa');
  await box(page).getByText('ABCD-1234').waitFor({timeout:10000});
  const open=box(page).getByRole('link',{name:'Open GitHub ↗'});
  assert.equal(await open.getAttribute('href'),'https://github.com/login/device');
  assert.equal(await open.getAttribute('target'),'_blank');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
  await shot(page,`github-code-${tag}`);
  await box(page).getByText('Connected.').waitFor({timeout:15000});
  // A code with anything but GitHub's own device page: no link to it
  states={'github/c_00000000000000bb':{state:'code',code:'ABCD-1234',url:'https://evil.example/login/device'}};
  await page.goto('about:blank');await page.goto(base+'/#connect=github/c_00000000000000bb');
  await box(page).getByText('Signed in. Connecting it now.').waitFor({timeout:8000});
  assert.equal(await box(page).locator('a[href*="evil"]').count(),0);
  // Anything else in the address is not a sign-in to follow
  asked=[];
  for(const hash of ['#connect=zoom/f_0123456789abcdef/x','#connect=zoom/https://evil.example','#connect=evil/f_0123456789abcdef']){
   await page.goto('about:blank');await page.goto(base+'/'+hash);await page.waitForTimeout(300);
   assert.ok(!(await box(page).innerText()).includes('did not accept'),hash);
  }
  assert.deepEqual(asked,[]);
  // GitHub in + Add: its own form here, never a link to the account page
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await box(page).locator('[data-connect-signin="github"]').click();
  await box(page).getByRole('button',{name:'Sign in with GitHub'}).waitFor();
  assert.equal(await box(page).locator(`a[href^="${MANAGE}"]`).count(),0);
  await shot(page,`github-intro-${tag}`);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
