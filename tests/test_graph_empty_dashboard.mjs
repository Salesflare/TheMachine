import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// A Graph page with nothing on it yet still opens when its row is clicked: Projects with no projects (a bug report: the
// row did nothing and People stayed), Organizations with none, People with nobody. Each says in one short line how it
// fills, and its head keeps + New. EMPTY_SHOT=<dir> writes screenshots (desktop and phone, light and dark).
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const sticker=await readFile(new URL('../brand/thinking.webp',import.meta.url));
const ann={id:'email:ann@client.example',kind:'person',name:'Ann Example',strength:2,closeness:'regular',last_at:new Date().toISOString(),signals:3,ids:['ann@client.example']};
let anyone=true;
const server=createServer(async(req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/brand/thinking.webp'){res.setHeader('Content-Type','image/webp');res.end(sticker);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 if(url.pathname==='/api/graph'){const n=anyone?1:0;res.end(JSON.stringify({list_counts:{people:n,quiet:0,new:0,orgs:0,warmup:0,projects:0,projects_done:0},counts:{person:n,org:0,project:0},boards:[],board_suggestions:[]}));return}
 if(url.pathname==='/api/graph/list'){res.end(JSON.stringify({items:anyone&&url.searchParams.get('list')==='people'?[ann]:[],next:null,total:anyone?1:0}));return}
 res.statusCode=url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/',shotDir=process.env.EMPTY_SHOT,errors=[];let browser;
const shown=page=>page.locator('#people-view [data-graph-panel]:not([hidden])');
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]])for(const scheme of ['light','dark']){const mobile=width<600,tag=`${width}-${scheme}`;anyone=true;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-GB',colorScheme:scheme}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(tag+': '+e.message));await page.goto(base);await page.waitForFunction(()=>typeof people==='function');
  await navClick(page.locator('nav [data-tab="people"]'));await page.locator('#people-view article[data-node="email:ann@client.example"]').waitFor();
  // Projects, with people but no projects: it opens, says so, and offers + New project
  await navClick(page.locator('.side-sub a[data-graph-sub="projects"]'));
  await page.locator('#people-view [data-graph-panel="projects"]:not([hidden]) .graph-empty').waitFor();
  assert.equal(await shown(page).getAttribute('data-graph-panel'),'projects',tag);
  assert.equal((await shown(page).innerText()).replace(/\s+/g,' ').trim(),'No projects yet. Reviews name them from your messages and to-dos.',tag);
  if(!mobile)assert.match(await page.locator('#page-head').innerText(),/Projects[\s\S]*\+ New project/,tag);  // a phone's head has no room for + New
  assert.equal(await page.locator('.side-sub a[data-graph-sub="projects"][aria-current="page"]').count(),1,`the Projects row is the current one ${tag}`);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`no sideways scroll ${tag}`);
  if(shotDir){await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`${shotDir}/projects-empty-${tag}.png`})}
  // Organizations, none yet
  await navClick(page.locator('.side-sub a[data-graph-sub="orgs"]'));
  await page.locator('#people-view [data-graph-panel="orgs"]:not([hidden]) .graph-empty').waitFor();
  assert.equal((await shown(page).innerText()).replace(/\s+/g,' ').trim(),'No organizations yet. They come from the people you’re in touch with.',tag);
  if(!mobile)assert.match(await page.locator('#page-head').innerText(),/\+ New organization/,tag);  // a phone's head has no room for + New
  if(shotDir)await page.screenshot({path:`${shotDir}/orgs-empty-${tag}.png`});
  // Back to People, with someone on it
  await navClick(page.locator('.side-sub a[data-graph-sub="people"]'));await page.locator('#people-view [data-graph-panel="people"]:not([hidden]) article[data-node]').waitFor();
  // Nobody at all: People says so too, and Projects still opens
  anyone=false;await page.evaluate(()=>{pagerDrop('graph');return people('')});
  await page.locator('#people-view [data-graph-panel="people"]:not([hidden]) .graph-empty').waitFor();
  assert.equal((await shown(page).innerText()).replace(/\s+/g,' ').trim(),'Nothing mapped yet. People appear as messages and meetings come in.',tag);
  if(!mobile)assert.match(await page.locator('#page-head').innerText(),/\+ New person/,tag);  // a phone's head has no room for + New
  if(shotDir)await page.screenshot({path:`${shotDir}/people-empty-${tag}.png`});
  await navClick(page.locator('.side-sub a[data-graph-sub="projects"]'));
  await page.locator('#people-view [data-graph-panel="projects"]:not([hidden]) .graph-empty').waitFor();
  await context.close()}
 assert.deepEqual(errors,[]);
 console.log('Graph pages with nothing on them open with a short empty line');
}finally{await browser?.close();server.close()}
