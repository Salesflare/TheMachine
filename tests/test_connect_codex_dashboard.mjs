import assert from 'node:assert/strict';
import {readFile,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_CORE||OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Connections, + Add, Codex (codex_signin.py): Codex signs in with its own device code, shown right in the form with
// OpenAI's page, never a command to type. A hosted Machine's control plane runs that sign-in on its server (POST
// /_machine/connect, followed by /_machine/connect-state, like GitHub); a self-hosted Machine runs it itself
// (codex_signin, codex_signin_state). The tile says whether Codex is signed in. In Dutch every line reads Dutch.
// SHOTS=<folder> saves screenshots.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const cats={};for(const l of ['nl'])cats[l]=await readFile(new URL(`../i18n/${l}.json`,import.meta.url),'utf8');
const MANAGE='https://app.example.org/setup';
const DEVICE='https://auth.openai.com/codex/device';
let hosted=true,lang='en',codex='signed_out',states={},posted=[],local=[],actions=[];
const locale=()=>({locale:'en-BE',region:'BE',language:lang,language_set:true,clock:'auto',hour12:false,auto_hour12:false,
 date_locale:lang==='en'?'en-GB':lang+'-BE',languages:{en:'English',nl:'Nederlands'},saveable:true});
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname.startsWith('/brand/')){const f=url.pathname==='/brand/avatar.png'?'app-icon-192.png':url.pathname.slice(7);res.setHeader('Content-Type','image/png');
  try{res.end(await readFile(new URL('../brand/'+f.replace(/[^\w.-]/g,''),import.meta.url)))}catch{res.statusCode=404;res.end()}return}
 const cat=/^\/i18n\/(\w\w(?:-[A-Z]{2})?)\.json$/.exec(url.pathname);if(cat){res.end(cats[cat[1]]||'{}');return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],
  review_health:{},review_runs:[],locale:locale(),...(hosted?{manage_url:MANAGE}:{})}));return}
 if(url.pathname==='/_machine/connect'){let body='';for await(const b of req)body+=b;const form=Object.fromEntries(new URLSearchParams(body));posted.push(form);
  res.statusCode=303;res.setHeader('Location','/#connect='+form.source+'/c_00000000000000cc');res.end();return}
 if(url.pathname==='/_machine/connect-state'){const next=states[url.searchParams.get('s')+'/'+url.searchParams.get('c')];
  if(!next){res.statusCode=404;res.end('{"error":"unknown"}');return}res.end(JSON.stringify(next.length>1?next.shift():next[0]));return}
 if(url.pathname==='/api/action'){let body='';for await(const b of req)body+=b;const {action}=JSON.parse(body);actions.push(action);
  if(action==='connect_sources'){res.end(JSON.stringify({saveable:true,manage_url:hosted?MANAGE:null,paired:!hosted,codex:{status:codex},sources:[
   {name:'github',service:'github',label:'GitHub',what:'Review requests, mentions and failed CI runs.',connected:0,broker:false,...(hosted?{hosted_signin:'github'}:{})},
   {name:'slack',service:'slack',label:'Slack',connected:0,broker:false}]}));return}
  if(action==='codex_signin'||action==='codex_signin_state'){const next=local.length>1?local.shift():local[0]||{state:'none'};if(next.state==='done')codex='connected';res.end(JSON.stringify(next));return}
  res.end('{}');return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
const errors=[];let browser;
const shot=async(page,name)=>{if(shots)await page.screenshot({path:`${shots}/${name}.png`})};
const box=page=>page.locator('#connect-add');
const fits=page=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const runs=shots?[['light',1440,900],['light',1440,700],['light',390,844],['dark',1440,900],['dark',390,844]]:[['light',1440,900],['dark',390,844]];
 for(const [scheme,width,height] of runs){
  const context=await browser.newContext({viewport:{width,height},colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  const tag=`${width}x${height}-${scheme}`;
  // Hosted: the tile says Signed out; Get a code posts to this dashboard, which follows the server's sign-in
  hosted=true;lang='en';codex='signed_out';posted=[];
  await page.goto(base+'/#connections=add');
  const tile=box(page).locator('[data-codex-signin]');await tile.waitFor({timeout:10000});
  assert.match(await tile.innerText(),/Codex[\s\S]*Coding to-dos on your ChatGPT plan[\s\S]*Signed out/);
  if(width===1440&&height===900)await shot(page,`codex-add-list-${tag}`);
  await tile.click();
  assert.equal(await box(page).locator('h3').innerText(),'Codex');
  await box(page).getByRole('button',{name:'Get a code'}).waitFor();
  assert.equal(await box(page).locator('input[name="signin-scope"]').count(),0,'no Work or Personal for Codex');
  assert.ok(!(await box(page).innerText()).includes('codex login'),'no command to type');
  await shot(page,`codex-intro-${tag}`);
  states={'codex/c_00000000000000cc':[{state:'starting'},{state:'code',code:'ABCD-12345',url:DEVICE},{state:'code',code:'ABCD-12345',url:DEVICE},{state:'code',code:'ABCD-12345',url:DEVICE},
   {state:'connecting'},{state:'done'}]};
  await box(page).getByRole('button',{name:'Get a code'}).click();
  await page.waitForURL(u=>!u.hash);
  assert.equal(posted.at(-1).source,'codex');
  assert.equal(posted.at(-1).scope,undefined);
  await box(page).getByText('ABCD-12345').waitFor({timeout:10000});
  await box(page).getByText('Enter this code at OpenAI to sign in:').waitFor();
  const open=box(page).getByRole('link',{name:'Open OpenAI ↗'});
  assert.equal(await open.getAttribute('href'),DEVICE);
  assert.equal(await open.getAttribute('target'),'_blank');
  assert.ok(await fits(page),'no sideways scroll');
  const heights=await box(page).locator('.code-actions>*').evaluateAll(els=>els.map(e=>Math.round(e.getBoundingClientRect().height)));
  assert.equal(new Set(heights).size,1,'Copy code and Open OpenAI are one height: '+heights);
  await shot(page,`codex-code-hosted-${tag}`);
  await box(page).getByText('Hand a coding to-do to Codex to use it.').waitFor({timeout:20000});
  await shot(page,`codex-done-${tag}`);
  // A code with any page but OpenAI's own device page: no link to it
  states={'codex/c_00000000000000dd':[{state:'code',code:'ABCD-12345',url:'https://evil.example/codex/device'}]};
  await page.goto('about:blank');await page.goto(base+'/#connect=codex/c_00000000000000dd');
  await box(page).getByText('Signed in. Connecting it now.').waitFor({timeout:8000});
  assert.equal(await box(page).locator('a[href*="evil"]').count(),0);
  // Turned down or expired: why, Try again, and where OpenAI's switch is
  states={'codex/c_00000000000000ee':[{state:'failed',error:'The sign-in code expired or was not approved.'}]};
  await page.goto('about:blank');await page.goto(base+'/#connect=codex/c_00000000000000ee');
  await box(page).getByText('The sign-in code expired or was not approved.').waitFor({timeout:8000});
  await box(page).getByRole('button',{name:'Try again'}).waitFor();
  assert.equal(await box(page).locator('a[href="https://chatgpt.com/settings/security"]').count(),1);
  // Self-hosted: this Machine runs the sign-in itself, and the tile says Connected after
  hosted=false;codex='signed_out';actions=[];
  local=[{state:'starting'},{state:'code',code:'WXYZ-98765',url:DEVICE},{state:'code',code:'WXYZ-98765',url:DEVICE},{state:'done'}];
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await box(page).locator('[data-codex-signin]').click();
  await box(page).getByRole('button',{name:'Get a code'}).click();
  await box(page).getByText('WXYZ-98765').waitFor({timeout:10000});
  assert.equal(await box(page).getByRole('link',{name:'Open OpenAI ↗'}).getAttribute('href'),DEVICE);
  assert.ok(actions.includes('codex_signin'));
  await shot(page,`codex-code-self-hosted-${tag}`);
  await box(page).getByText('Hand a coding to-do to Codex to use it.').waitFor({timeout:15000});
  await box(page).getByRole('button',{name:'Back'}).click();
  await page.waitForFunction(()=>/Connected/.test(document.querySelector('[data-codex-signin]')?.innerText||''));
  // No Codex here yet: how to install it, then Try again
  codex=null;local=[{state:'missing'}];
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await box(page).locator('[data-codex-signin]').click();
  await box(page).getByRole('button',{name:'Get a code'}).click();
  await box(page).getByText('npm install -g @openai/codex').first().waitFor({timeout:8000});
  // Dutch: the tile and the form read Dutch, nothing English around the code
  hosted=true;lang='nl';codex='signed_out';
  states={'codex/c_00000000000000ff':[{state:'code',code:'ABCD-12345',url:DEVICE}]};
  await page.goto('about:blank');await page.goto(base+'/#connections=add');
  await page.waitForFunction(()=>document.documentElement.lang==='nl');
  const nlTile=box(page).locator('[data-codex-signin]');await nlTile.waitFor({timeout:10000});
  await page.waitForFunction(()=>/Uitgelogd/.test(document.querySelector('[data-codex-signin]')?.innerText||''));
  assert.match(await nlTile.innerText(),/Codeer-to-do's op je ChatGPT-abonnement/);
  await nlTile.click();
  await box(page).getByRole('button',{name:'Code ophalen'}).waitFor();
  await box(page).getByText('Draag codeer-to-do\'s over aan Codex, op je ChatGPT-abonnement.',{exact:false}).waitFor();
  await shot(page,`codex-intro-nl-${tag}`);
  await page.goto('about:blank');await page.goto(base+'/#connect=codex/c_00000000000000ff');
  await box(page).getByText('Vul deze code in bij OpenAI om in te loggen:').waitFor({timeout:10000});
  await box(page).getByRole('link',{name:'OpenAI openen ↗'}).waitFor();
  await box(page).getByText('Weigert OpenAI de code?').waitFor();
  await shot(page,`codex-code-nl-${tag}`);
  await context.close();
 }
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
