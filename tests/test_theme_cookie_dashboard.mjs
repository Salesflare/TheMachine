import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Light or dark keeps working when the browser holds more than one "theme" cookie this page can see. A dashboard at
// my.example.test puts its choice on example.test; a hosted one at owner.app.example.test sees that one next to its
// own on app.example.test, and the first one read won: the switch looked stuck. Picking one now replaces every copy
// this page can see, so the next read is the one just picked.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const server=createServer((req,res)=>{const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard.replace('__BASE__','/'));return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],connectors:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]}));return}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const port=server.address().port;
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--host-resolver-rules=MAP *.example.test 127.0.0.1']});
 const context=await browser.newContext({colorScheme:'dark'});
 await context.route('**/*',route=>['127.0.0.1'].includes(new URL(route.request().url()).hostname)||new URL(route.request().url()).hostname.endsWith('example.test')?route.continue():route.abort());
 // left by a dashboard on my.example.test, before this one was ever used: the oldest, so read first
 await context.addCookies([{name:'theme',value:'dark',domain:'.example.test',path:'/'}]);
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 const theme=()=>page.evaluate(()=>[document.documentElement.dataset.theme,document.documentElement.dataset.themeMode]);
 const copies=async()=>(await context.cookies()).filter(c=>c.name==='theme').map(c=>c.domain+'='+c.value).sort();
 await page.goto(`http://owner.app.example.test:${port}/`);await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
 assert.deepEqual(await theme(),['dark','dark']);
 const pick=()=>page.evaluate(()=>{document.querySelector('#theme-toggle').click();return document.documentElement.dataset.theme});
 assert.equal(await pick(),'light');assert.deepEqual(await theme(),['light','light']);
 assert.deepEqual(await copies(),['.app.example.test=light']);  // one copy, on the app's domain
 assert.equal(await pick(),'dark');assert.equal(await pick(),'light');
 await page.reload();await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});assert.deepEqual(await theme(),['light','light']);
 // A stale copy on this host only (an older dashboard put it there) goes too
 await context.addCookies([{name:'theme',value:'dark',domain:'owner.app.example.test',path:'/'}]);
 assert.equal(await pick(),'dark');assert.equal(await pick(),'light');assert.deepEqual(await copies(),['.app.example.test=light']);
 // On a dashboard right under example.test the choice goes on example.test, as before
 await page.goto(`http://my.example.test:${port}/`);await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
 assert.deepEqual(await theme(),['dark','auto']);assert.equal(await pick(),'light');assert.ok((await copies()).includes('.example.test=light'));
 // On 127.0.0.1 (no domain above it) it stays on the host, and works the same
 await page.goto(`http://127.0.0.1:${port}/`);await page.locator('#updated',{hasText:/\d/}).waitFor({state:'attached'});
 const first=await pick();assert.notEqual(await pick(),first);
 assert.deepEqual(errors,[]);
 console.log('theme cookie dashboard test passed');
}finally{await browser?.close();server.close()}
