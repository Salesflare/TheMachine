import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, Signatures while the first look runs: its progress refreshes the page every few seconds. 2026-11-06: a new
// owner clicked into the signature, pasted one copied from Outlook, and it was gone: a refresh had drawn the editor
// again (the focused field with it), and a pasted Outlook signature, full of Word markup, was "too long" to save.
// Now a refresh keeps the editor someone is in, a paste keeps only the signature's own formatting, and Save stores it.
// Made-up fixtures, nothing sent.
const dashboard=await dashboardPage(),shots=process.env.SIG_SHOTS;
const now=new Date().toISOString();
let signatures=[{account_id:'work-outlook',email:'owner@example.com',service:'outlook',html:'',source:'detected',saveable:true}];
let count=0,statusCalls=0;const posts=[];
const live=()=>({runs:[{run_id:'r1',status:'running',started_at:now,preview:0,auto:1,window_hours:168,planned:20,done_count:count,claimed_count:20,duration_seconds:0,account_ids:['work-outlook'],steps:[]}],
 queue:null,first_look:null,first_dig:{read:count,total:64,todos:0,goal:3,days:7,pace:1},cards:{newest:'c'+count,count}});
const state=()=>({suggestions:[],promises:[],connectors:[{id:'work-outlook',display_name:'Work mail',service:'outlook'}],suggestion_counts:{},decisions:[],
 analyses:[],deliveries:[],review_health:{},review_runs:[],reviews_on:true,review_live:live(),signatures});
// What Outlook puts on the clipboard for a signature: Word markup, classes, conditional comments, a style block.
const WORD='<html xmlns:o="urn:schemas-microsoft-com:office:office"><head><style>'+'p.MsoNormal{margin:0cm;font-size:11pt;font-family:"Calibri",sans-serif;mso-fareast-language:EN-US}'.repeat(120)+
 '</style></head><body lang="EN-US"><!--StartFragment--><div class="WordSection1">'+
 '<p class="MsoNormal" style="mso-margin-top-alt:auto"><b><span lang="EN-US" style="font-size:10.0pt;font-family:Arial;color:#1F3864;mso-ansi-language:EN-US">Robin Example</span></b><o:p></o:p></p>'+
 '<p class="MsoNormal"><span style="font-size:9.0pt;color:gray;mso-fareast-language:NL">Example Inc · <a href="https://example.org"><span style="color:#0563C1">example.org</span></a></span><o:p></o:p></p>'+
 '<!--[if gte mso 9]><xml><o:OfficeDocumentSettings></o:OfficeDocumentSettings></xml><![endif]-->'.repeat(40)+
 '</div><!--EndFragment--></body></html>';
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){statusCalls++;res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/reviews/live'){count++;res.end(JSON.stringify(live()));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args,size:body.length});
  if(action==='detect_signature'){res.end(JSON.stringify({html:'',found:false,source:'detected',signatures}));return}
  if(action==='set_signature'){if(args.html.length>20000){res.statusCode=400;res.end(JSON.stringify({error:'That signature is too long'}));return}
   signatures=signatures.map(s=>s.account_id!==args.account_id?s:{...s,html:args.html,source:'owner'});res.end(JSON.stringify(signatures));return}
  res.end('{}');return}
 if(url.pathname.startsWith('/brand/')||url.pathname.startsWith('/assets/')){res.statusCode=404;res.end();return}
 res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of shots?[[1440,900],[1440,700],[390,844]]:[[1440,900]]){
  const context=await browser.newContext({viewport:{width,height}}),page=await context.newPage();
  await context.grantPermissions(['clipboard-read','clipboard-write'],{origin:'http://127.0.0.1:'+server.address().port});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await navClick(page.locator('#open-settings'));await page.locator('#settings-tabs [data-settings-tab="writing"]').click();
  const form=page.locator('#signatures .sig-form[data-account="work-outlook"]');await form.waitFor();
  const frame=page.frameLocator('#signatures .sig-form[data-account="work-outlook"] iframe.sig-paper'),body=frame.locator('body');
  await body.waitFor();
  const paper=async()=>page.evaluate(()=>{const f=document.querySelector('#signatures iframe.sig-paper');return f&&f.contentDocument?.body&&(f.contentDocument.body.dataset.mark||'')});
  // In the editor, nothing typed yet: progress refreshes come and go; the editor and its focus stay.
  await body.click();
  await page.evaluate(()=>{document.querySelector('#signatures iframe.sig-paper').contentDocument.body.dataset.mark='same'});
  const before=statusCalls;
  await page.evaluate(()=>refresh());await page.evaluate(()=>refresh());
  for(let i=0;i<120&&statusCalls<before+3;i++)await page.waitForTimeout(100);  // and the first look's own (cards move every 5 s)
  assert.ok(statusCalls>=before+3,'refreshes ran: '+(statusCalls-before));
  assert.equal(await paper(),'same','a refresh drew the editor again under the cursor');
  assert.equal(await page.evaluate(()=>document.activeElement?.classList.contains('sig-paper')),true,'the editor lost focus');
  // Paste an Outlook signature while progress keeps arriving.
  await page.evaluate(async h=>navigator.clipboard.write([new ClipboardItem({'text/html':new Blob([h],{type:'text/html'}),'text/plain':new Blob(['Robin Example'],{type:'text/plain'})})]),WORD);
  await page.keyboard.press('Control+V');
  await body.locator('b',{hasText:'Robin Example'}).waitFor();
  await page.evaluate(()=>refresh());await page.waitForTimeout(5500);
  const pasted=await body.innerHTML();
  assert.match(pasted,/Robin Example/);assert.match(pasted,/href="https:\/\/example.org\/?"/);
  assert.doesNotMatch(pasted,/Mso|mso-|<o:p|<style|<!--|class=/i,pasted.slice(0,300));
  assert.ok(pasted.length<2000,'pasted: '+pasted.length);
  await form.locator('.sig-save').waitFor();
  if(shots)await page.screenshot({path:`${shots}/sig-pasted-${width}x${height}.png`});
  await form.locator('.sig-save .primary').click();
  await page.locator('#notice',{hasText:'Signature saved.'}).waitFor({state:'attached'});
  const saved=posts.filter(p=>p.action==='set_signature').at(-1);
  assert.match(saved.args.html,/Robin Example/);
  await page.locator('#signatures .sig-form[data-account="work-outlook"] .sig-head',{hasText:'Custom'}).waitFor();
  assert.match(await body.innerHTML(),/Robin Example/);
  if(shots)await page.screenshot({path:`${shots}/sig-saved-${width}x${height}.png`});
  // The HTML view's textarea: a refresh keeps what is typed there too.
  await form.locator('[data-sig-tool="html"]').click();
  const src=form.locator('.sig-source');await src.fill(await src.inputValue()+'<div>Typed</div>');
  await page.evaluate(()=>refresh());await page.waitForTimeout(300);
  assert.match(await page.locator('#signatures .sig-source').inputValue(),/Typed/);
  await context.close();
  signatures=signatures.map(s=>({...s,html:'',source:'detected'}));
 }
 assert.deepEqual(errors,[]);
 console.log('signature paste live dashboard ok');
}finally{await browser?.close();server.close()}
