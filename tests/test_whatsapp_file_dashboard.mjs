// A file on WhatsApp (todos-send.js): Send now's dialog shows the file the message carries, which opens from there,
// and its caption when it has one; a text message shows no file row.
// At 1440x900 and 390x844. Made-up data, a local fixture server, nothing sent. SHOTS=<folder> saves shots.
import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

const dashboard=await dashboardPage();
const sid='1234567890abcdef',revision='1234567890ab';
const file={name:'report.pdf',size:21213,sha256:'c'.repeat(64),type:'application/pdf'};
let body='',files=[file];
const action=()=>({kind:'whatsapp',label:'Send',revision,account_id:'home-whatsapp',chat_id:'32470000000@s.whatsapp.net',to_name:'Sam Example',body,max_length:files.length?1024:4000,...(files.length?{attachments:files}:{})});
const state=()=>({suggestions:[{id:sid,title:'Send the report to Sam',body:'Ready to send on WhatsApp.',status:'prepared',event_ids:[1],next_action:action(),next_actions:[action()],outcome:{kind:'needs_you',needs:'check it and send'},scope:'personal',created_at:new Date().toISOString()}],
 connectors:[],suggestion_counts:{prepared:1},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[]});
const calls=[],errors=[];
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/action'){let b='';for await(const c of req)b+=c;calls.push(JSON.parse(b));res.end('{"status":"queued"}');return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const shots=process.env.SHOTS;if(shots)await mkdir(shots,{recursive:true});
let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[1440,900],[390,844]]){
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  for([body,files] of [['',[file]],['Here is the report.',[file]],['Friday works.',[]]]){
   const at=`${width} ${body?'caption':'bare'} ${files.length?'file':'text'}`;
   await page.evaluate(()=>refresh());
   await page.evaluate(([id,r])=>openSend(id,r),[sid,revision]);await page.locator('#send-dialog').waitFor({state:'visible'});
   assert.equal(await page.locator('#send-title').textContent(),'Send this WhatsApp message?',at);
   assert.match(await page.locator('#send-head').textContent(),/Sam Example/,at);
   const link=page.locator('#send-files a.attachment');
   if(files.length){
    assert.ok(await page.locator('#send-files').isVisible(),at+': the file shows before Send now');
    assert.match(await link.textContent(),/report\.pdf.*21 KB/,at);
    assert.equal(await link.getAttribute('href'),`api/draft-attachment?id=${sid}&sha=${'c'.repeat(64)}`,at);
   }else assert.ok(await page.locator('#send-files').isHidden(),at+': a text message lists no file');
   const sizes=await page.evaluate(()=>({page:document.documentElement.scrollWidth,viewport:innerWidth,dialog:document.querySelector('#send-dialog').getBoundingClientRect().width}));
   assert.ok(sizes.page<=sizes.viewport&&sizes.dialog<=sizes.viewport,at+': no overflow '+JSON.stringify(sizes));
   if(shots)await page.screenshot({path:`${shots}/whatsapp-file-${width}-${body?'caption':'bare'}-${files.length?'file':'text'}.png`});
   await page.keyboard.press('Escape');
  }
  await context.close();
 }
 assert.deepEqual(calls.filter(c=>c.action==='confirm_action'),[],'nothing is sent');
 assert.deepEqual(errors,[]);
 console.log('WhatsApp file dashboard: the file shows in Send now at 1440 and 390, a text message lists none, nothing sent.');
}finally{await browser?.close();server.close()}
