import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections, + Add, Microsoft: a work organization that lets only approved apps in needs its admin's approval first.
// The form says so in one line with the short link (themachine.computer/m365-admin-consent, never Microsoft's long one)
// and Copy link, on a hosted Machine and a self-hosted one alike, and again when the sign-in comes back unfinished or
// refused (Microsoft's "Need admin approval", AADSTS90094; on a hosted Machine the cloud's reason by f_ ref). Google and Docs don't show it. SHOTS=<folder> saves screenshots.
const LINK='https://themachine.computer/m365-admin-consent';
const dashboard=await dashboardPage();
const nl=await readFile(new URL('../i18n/nl.json',import.meta.url),'utf8');
let mode='self',language='en';
const CP='https://app.example.test';
const locale=()=>({locale:'en-BE',region:'BE',language,clock:'auto',hour12:false,auto_hour12:false,date_locale:'en-GB',languages:{en:'English',nl:'Nederlands'},saveable:true});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/i18n/nl.json'){res.end(nl);return}
 if(url.pathname==='/connect/start/'+'A'.repeat(32)){res.setHeader('Content-Type','text/html');res.end('<title>Microsoft</title>consent');return}
 if(url.pathname==='/_machine/connect-state'){assert.equal(url.searchParams.get('s'),'microsoft');res.end(JSON.stringify({state:'failed',error:'Your organization needs its admin to approve The Machine first.'}));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],
  locale:locale(),...(mode==='hosted'?{manage_url:CP+'/setup'}:{})}));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);
  if(action==='connect_sources'){const hosted=mode==='hosted';res.end(JSON.stringify({saveable:true,manage_url:hosted?CP+'/setup':null,paired:true,pair_url:CP+'/account?tab=fleet#devices',sources:[
   {name:'gmail',service:'gmail',label:'Gmail',what:'Your email.',connected:0,broker:false,...(hosted?{hosted_signin:'google'}:{signin:'google'})},
   {name:'outlook',service:'outlook',label:'Outlook',what:'Your Outlook email.',connected:0,broker:false,...(hosted?{hosted_signin:'microsoft'}:{signin:'microsoft'})},
   {name:'docs',service:'docs',label:'Docs',what:'Comments and shares on your docs.',connected:0,broker:true,signin:'microsoft_docs'}]}));return}
  if(action==='connect_signin'){res.end(JSON.stringify({url:base+'/connect/start/'+'A'.repeat(32),state:'started'}));return}
  if(action==='connect_signin_state'){res.end(JSON.stringify({state:'failed',error:'AADSTS90094: Admin consent is required'}));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const hint=page=>page.locator('#connect-add .connect-admin');
async function checkHint(page,what){
 const p=hint(page);await p.waitFor();
 assert.equal(await p.count(),1,what);
 assert.equal(await p.locator('p').innerText(),'Need your admin’s approval? Send them this link.',what);
 const a=p.locator('a');
 assert.equal(await a.getAttribute('href'),LINK,what);
 assert.equal(await a.innerText(),'themachine.computer/m365-admin-consent',what);
 assert.equal(await a.getAttribute('target'),'_blank');
 assert.equal(await a.getAttribute('rel'),'noopener');
 assert.ok(!(await page.locator('#connect-add').innerHTML()).includes('login.microsoftonline.com'),'only the short link, never Microsoft’s own');
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no sideways scroll');
 const box=await p.boundingBox(),pane=await page.locator('#connect-add').boundingBox();
 assert.ok(box.x>=pane.x-1&&box.x+box.width<=pane.x+pane.width+1,'the line fits the form');
}
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const scheme of ['light','dark'])for(const [width,height] of [[1440,900],[390,844]])for(const m of ['hosted','self']){
  mode=m;language='en';
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme});
  await context.grantPermissions(['clipboard-read','clipboard-write'],{origin:base});
  const page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const tag=`${m}-${width}-${scheme}`;
  await page.goto(base+'/#connections=add');
  await page.locator('#connect-add [data-connect-signin="outlook"]').click();
  await page.getByRole('button',{name:'Sign in with Microsoft'}).waitFor();
  await checkHint(page,'the Microsoft form');
  if(shots)await page.locator('#connect-add').screenshot({path:`${shots}/ms-admin-${tag}.png`});
  // Copy link puts the short link on the clipboard
  await hint(page).getByRole('button',{name:'Copy link'}).click();
  await page.getByText('Copied.').waitFor();
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),LINK);
  // Google's form has no such line
  await page.locator('#connect-add [data-connect-back]').click();
  await page.locator('#connect-add [data-connect-signin="gmail"]').click();
  await page.getByRole('button',{name:'Sign in with Google'}).waitFor();
  assert.equal(await hint(page).count(),0,'not on Google');
  if(m==='self'){
   // Docs from Microsoft asks for something else (Files.Read.All): no admin line there either
   await page.locator('#connect-add [data-connect-back]').click();
   await page.locator('#connect-add [data-connect-signin="docs"]').click();
   await page.getByRole('button',{name:'Sign in with Microsoft'}).waitFor();
   assert.equal(await hint(page).count(),0,'not on Docs');
   // Back from Microsoft refused (Need admin approval): the error, Try again, and the link right there
   await page.locator('#connect-add [data-connect-back]').click();
   await page.locator('#connect-add [data-connect-signin="outlook"]').click();
   const [tab]=await Promise.all([context.waitForEvent('page'),page.getByRole('button',{name:'Sign in with Microsoft'}).click()]);
   await tab.close();
   await page.getByText('AADSTS90094: Admin consent is required').waitFor({timeout:8000});
  }else{
   // Back on the dashboard after a sign-in that didn't finish (the control plane's #connect=microsoft/stopped)
   await page.goto('about:blank');await page.goto(base+'/#connect=microsoft/stopped');
   await page.getByText('That sign-in didn’t finish.').waitFor();
   await page.getByRole('button',{name:'Try again'}).waitFor();
   await checkHint(page,'after an unfinished sign-in');
   // Refused because the organization wants its admin first (the cloud's #connect=microsoft/f_…): why, and the link
   await page.goto('about:blank');await page.goto(base+'/#connect=microsoft/f_'+'0123456789abcdef');
   await page.getByText('Your organization needs its admin to approve The Machine first.').waitFor();
  }
  await page.getByRole('button',{name:'Try again'}).waitFor();
  await checkHint(page,'after a refused sign-in');
  if(shots)await page.locator('#connect-add').screenshot({path:`${shots}/ms-admin-error-${tag}.png`});
  await context.close();
 }
 // In Dutch: the line reads translated, the link stays as it is
 mode='hosted';language='nl';
 const context=await browser.newContext({viewport:{width:1440,height:900}}),page=await context.newPage();
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/#connections=add');
 await page.locator('#connect-add [data-connect-signin="outlook"]').click();
 await page.getByText('Goedkeuring van je beheerder nodig? Stuur hem of haar deze link.').waitFor();
 assert.equal(await hint(page).locator('a').innerText(),'themachine.computer/m365-admin-consent');
 await hint(page).getByRole('button',{name:'Link kopiëren'}).waitFor();
 await context.close();
 assert.deepEqual(errors,[]);
 console.log('ok');
}finally{await browser?.close();server.close()}
