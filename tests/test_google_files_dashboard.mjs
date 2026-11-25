// Google Docs on a hosted Machine: its card offers Allow Sheets and Slides once (google_files.py), in one quiet line; the
// button opens that sign-in for its own address, without a Work or Personal question, and comes back to it. Both allowed:
// the line says so and asks nothing. Not offered (the control plane's flag is off): the card is as before.
// Synthetic data, a local fixture server, nothing signed in. SHOTS=<folder> saves screenshots.
import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

const dashboard=await dashboardPage(),MANAGE='https://app.example.org/setup',posted=[],errors=[];
const docs=extra=>({id:'google-docs',display_name:'Google Docs',email:'owner@example.com',service:'docs',transport:'broker',boundary:'work',events:0,recent_events:0,
  signals:false,actions:true,abilities:['signals','actions'],ability_switches:['signals','actions'],
  last_success:new Date().toISOString(),docs_provider:'google',docs_linked_only:true,docs_writes:['create','edit'],hosted_signin:'google_docs',...extra});
let connectors=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],manage_url:MANAGE,connectors}));return}
 if(url.pathname==='/_machine/connect'){let b='';for await(const c of req)b+=c;const form=Object.fromEntries(new URLSearchParams(b));posted.push(form);
  res.statusCode=303;res.setHeader('Location','/#connect='+form.source+'/c_00000000000000cc');res.end();return}
 if(url.pathname==='/_machine/connect-state'){res.end(JSON.stringify({state:'done'}));return}
 if(url.pathname==='/api/action'){let b='';for await(const c of req)b+=c;
  res.end(JSON.stringify(JSON.parse(b).action==='connect_sources'?{saveable:true,manage_url:MANAGE,sources:[{name:'google_docs',service:'docs',group:'docs',label:'Google Docs',connected:1,hosted_signin:'google_docs'}]}:{}));return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port,shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height,scheme] of shots?[[390,844,'light'],[390,844,'dark'],[1440,900,'light'],[1440,900,'dark']]:[[390,844,'dark']]){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage(),tag=`${width}-${scheme}`;
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  // The card as this status makes it: `says` is what it ends up showing, or (a leading !) not showing
  const show=async(extra,says)=>{connectors=[docs(extra)];await page.evaluate(()=>refresh());
   await page.evaluate(()=>{document.querySelector('nav [data-tab="health"]').click();cardShow('google-docs')});
   const conn=page.locator('[data-conn="google-docs"]');await conn.waitFor();
   await page.waitForFunction(says=>{const text=document.querySelector('[data-conn="google-docs"]')?.innerText||'';
    return text&&(says[0]==='!'?!text.includes(says.slice(1)):text.includes(says))},says);return conn};
  connectors=[docs()];await page.goto(base);await page.waitForFunction(()=>typeof refresh==='function');
  await page.evaluate(()=>lazyPart('connections'));
  // Not offered: as before
  let conn=await show({},'!Sheets');
  assert.equal(await conn.locator('.conn-what').count(),1);
  assert.ok(!/Sheets/.test(await conn.textContent()));
  // Both allowed: said in the same paragraph, nothing to press
  conn=await show({docs_files:['sheets','slides']},'Reads linked Sheets and Slides.');
  assert.match(await conn.locator('.conn-what').innerText(),/Edits docs only after you OK each change\.\s+Reads linked Sheets and Slides\.$/);
  assert.equal(await conn.locator('button',{hasText:'Allow Sheets'}).count(),0);
  if(shots)await page.screenshot({path:`${shots}/card-allowed-${tag}.png`});
  // Offered: one button, on no line of its own when it fits
  conn=await show({docs_files:[],docs_files_signin:'google_docs_files'},'Allow Sheets');
  const allow=conn.locator('button',{hasText:'Allow Sheets and Slides'});
  assert.equal(await allow.count(),1);
  if(shots)await page.screenshot({path:`${shots}/card-offered-${tag}.png`});
  // Can do things off: it reads nothing, so it asks nothing
  conn=await show({actions:false,signals:true,docs_files_signin:'google_docs_files'},'!Allow Sheets');
  assert.equal(await allow.count(),0);
  conn=await show({docs_files:[],docs_files_signin:'google_docs_files'},'Allow Sheets');
  await allow.click();
  const box=page.locator('#connect-add');await box.getByText('Reads the Sheets and Slides your to-dos link to. Never changes them.').waitFor();
  assert.equal(await box.locator('.connect-scope').count(),0,'the connection has its Work or Personal already');
  if(shots)await page.screenshot({path:`${shots}/form-${tag}.png`,animations:'disabled'});
  posted.length=0;await box.getByRole('button',{name:'Sign in with Google'}).click();
  await box.getByText('Connected').first().waitFor({timeout:8000});
  assert.deepEqual(posted.map(f=>[f.source,f.email]),[['google_docs_files','owner@example.com']]);
  // Signed in from a link elsewhere
  await page.goto('about:blank');await page.goto(base+'/#signed-in=google_docs_files/again');
  await page.getByText('Reconnected to Google Docs.').waitFor({timeout:8000});
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
