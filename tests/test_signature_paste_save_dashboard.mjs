import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
import {navClick} from './nav-click.mjs';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// Settings, Signatures: Save shows for every change, not only for typing. 2026-11-06: an owner pasted the signature
// copied from Outlook and found no Save to press. Here: a paste carrying Outlook's HTML (the clipboard event itself), a
// plain-text paste from the keyboard, a drop, a change that brings no input event, undo, Safari's paste (no event at
// all, cleaned as it lands) and a paste in the HTML view; each shows Save, in view at a short window, and Save stores
// what was pasted, its lines as close as in Outlook. Clicking in without a change shows none.
// Made-up fixtures, nothing sent. SIG_SHOTS=<folder> also saves the editor after a paste at 390 and 1440, light and dark.
const dashboard=await dashboardPage(),shots=process.env.SIG_SHOTS;
const fresh=()=>[{account_id:'work-outlook',email:'owner@example.com',service:'outlook',html:'',source:'detected',saveable:true}];
let signatures=fresh();const posts=[];
const OUTLOOK='<html xmlns:o="urn:schemas-microsoft-com:office:office"><head><style>p.MsoNormal{margin:0cm;font-family:"Calibri",sans-serif}</style></head>'+
 '<body lang="EN-US"><!--StartFragment--><div class="WordSection1"><p class="MsoNormal"><b><span style="font-size:10.0pt;font-family:Arial;color:#1F3864;mso-ansi-language:EN-US">Robin Example</span></b><o:p></o:p></p>'+
 '<p class="MsoNormal"><span style="font-size:9.0pt;color:gray">Head of Sales · Example Inc</span><o:p></o:p></p>'+
 '<p class="MsoNormal"><span style="font-size:9.0pt">+32 470 00 00 00 · <a href="https://example.org"><span style="color:#0563C1">example.org</span></a></span><o:p></o:p></p>'+
 '<p class="MsoNormal"><img width="240" height="96" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAAwCAIAAABVDSmEAAAAXElEQVR42u3QQQ0AAAgEoGtiDQPZP4MtfDg2EpDq4UAUiBaNaNGiLYgWjWjRoi2IFo1o0aIRLRrRokUjWjSiRYtGtGhEixaNaNGIFi0a0aIRLVo0okUjWrRoRH+wYFhwcW6M/ScAAAAASUVORK5CYII=" alt="Example Inc"></p>'+
 '</div><!--EndFragment--></body></html>';
const server=createServer(async(req,res)=>{
 const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},
  connectors:[{id:'work-outlook',display_name:'Work mail',service:'outlook'}],review_runs:[],signatures}));return}
 if(url.pathname==='/api/action'){let body='';for await(const c of req)body+=c;const {action,args}=JSON.parse(body);posts.push({action,args});
  if(action==='detect_signature'){res.end(JSON.stringify({html:'',found:false,source:'detected',signatures}));return}
  if(action==='set_signature'){signatures=signatures.map(s=>s.account_id!==args.account_id?s:{...s,html:args.html,source:'owner'});res.end(JSON.stringify(signatures));return}
  res.end('{}');return}
 res.statusCode=404;res.end('{}');
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin='http://127.0.0.1:'+server.address().port,errors=[];let browser;
async function open(width,height,colorScheme='light'){
 const context=await browser.newContext({viewport:{width,height},colorScheme}),page=await context.newPage();
 await context.grantPermissions(['clipboard-read','clipboard-write'],{origin});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(origin);
 await navClick(page.locator('#open-settings'));await page.locator('#settings-tabs [data-settings-tab="writing"]').click();
 const form=page.locator('#signatures .sig-form[data-account="work-outlook"]');await form.waitFor();
 const body=page.frameLocator('#signatures .sig-form[data-account="work-outlook"] iframe.sig-paper').locator('body');await body.waitFor();
 await page.waitForFunction(()=>document.querySelector('#signatures iframe.sig-paper')?._fit);  // the editor is ready
 return {context,page,form,body,save:form.locator('.sig-save')};
}
// What a paste from Outlook brings: a paste event whose clipboard holds the HTML (and the plain text beside it).
const pasteHtml=(page,h)=>page.evaluate(h=>{const d=document.querySelector('#signatures iframe.sig-paper').contentDocument,w=d.defaultView,dt=new w.DataTransfer();
 dt.setData('text/html',h);dt.setData('text/plain','Robin Example');d.body.focus();
 return d.body.dispatchEvent(new w.ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}))},h);
const inView=page=>page.evaluate(()=>{const r=document.querySelector('#signatures .sig-save').getBoundingClientRect();return r.height>0&&r.top>=0&&r.bottom<=innerHeight});
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // A click into the editor changes nothing: no Save.
 {const {context,page,body,save}=await open(1440,700);
  await body.click();await page.waitForTimeout(300);assert.equal(await save.isHidden(),true,'Save without a change');
  // Paste from Outlook: the signature's own formatting stays, Save shows, in view even at a short window, and saves.
  assert.equal(await pasteHtml(page,OUTLOOK),false,'the paste is taken over to clean it');
  await body.locator('b',{hasText:'Robin Example'}).waitFor();
  const pasted=await body.innerHTML();
  assert.doesNotMatch(pasted,/Mso|mso-|<o:p|<style|<!--|class=/i,pasted.slice(0,300));
  assert.match(pasted,/<p style="margin:0/,'Word\'s paragraphs keep no margin');  // its style block said so
  await save.waitFor();
  for(let i=0;i<20&&!await inView(page);i++)await page.waitForTimeout(50);
  assert.equal(await inView(page),true,'Save is below the window after the paste');
  await save.locator('.primary').click();
  await page.locator('#notice',{hasText:'Signature saved.'}).waitFor({state:'attached'});
  const saved=posts.filter(p=>p.action==='set_signature').at(-1);
  assert.match(saved.args.html,/Robin Example/);assert.match(saved.args.html,/href="https:\/\/example\.org\/?"/);assert.match(saved.args.html,/<img /);
  assert.doesNotMatch(saved.args.html,/mso-|class=/i);
  await page.locator('#signatures .sig-head',{hasText:'Custom'}).waitFor();
  await context.close();signatures=fresh()}
 // A plain-text paste from the keyboard (the browser's own paste) shows Save too.
 {const {context,page,body,save}=await open(1440,900);
  await page.evaluate(()=>navigator.clipboard.writeText('Robin Example\nExample Inc'));
  await body.click();await page.keyboard.press('Control+V');
  await body.getByText('Example Inc').waitFor();await save.waitFor();
  // Undo takes the paste back: still a change from what was saved, Save stays.
  await page.keyboard.press('Control+Z');await page.waitForTimeout(200);assert.equal(await save.isVisible(),true);
  await context.close()}
 // A drop of Outlook's HTML is cleaned the same way and shows Save.
 {const {context,page,body,save}=await open(1440,900);
  const kept=await page.evaluate(h=>{const fr=document.querySelector('#signatures iframe.sig-paper'),d=fr.contentDocument,w=d.defaultView,dt=new w.DataTransfer();
   dt.setData('text/html',h);const r=d.body.getBoundingClientRect();
   return d.body.dispatchEvent(new w.DragEvent('drop',{dataTransfer:dt,clientX:r.left+20,clientY:r.top+20,bubbles:true,cancelable:true}))},OUTLOOK);
  assert.equal(kept,false,'the drop is taken over to clean it');
  await body.locator('b',{hasText:'Robin Example'}).waitFor();assert.doesNotMatch(await body.innerHTML(),/mso-|class=/i);
  await save.waitFor();await context.close()}
 // A change that brings no input event (what an insert after a paste does in some browsers) shows Save.
 {const {context,page,save}=await open(1440,900);
  await page.evaluate(()=>{const d=document.querySelector('#signatures iframe.sig-paper').contentDocument,p=d.createElement('p');p.textContent='Robin Example';d.body.append(p)});
  await save.waitFor();await context.close()}
 // Safari runs no listener in the editor (a sandboxed frame without scripts): its paste lands with no paste or input
 // event, the markup as the clipboard had it. Here that paste, Outlook's HTML put in with no event: Save shows, it is
 // cleaned as it lands (Safari's own page styles, -webkit-standard, go too), and Save stores it clean.
 {const {context,page,body,save}=await open(1440,700);
  await page.evaluate(h=>{const d=document.querySelector('#signatures iframe.sig-paper').contentDocument,t=d.createElement('template');
   t.innerHTML=new DOMParser().parseFromString(h,'text/html').body.innerHTML.replace('<div class="WordSection1">','<div class="WordSection1" style="font-family: -webkit-standard; color: rgb(0, 0, 0)">');
   d.body.append(t.content)},OUTLOOK);
  await save.waitFor();await body.locator('b',{hasText:'Robin Example'}).waitFor();
  const landed=await body.innerHTML();
  assert.doesNotMatch(landed,/Mso|mso-|<o:p|class=|-webkit-|<!--/i,landed.slice(0,300));assert.match(landed,/<p style="margin:0/);assert.match(landed,/<img /);
  for(let i=0;i<20&&!await inView(page);i++)await page.waitForTimeout(50);assert.equal(await inView(page),true,'Save in view after a Safari paste');
  await save.locator('.primary').click();await page.locator('#notice',{hasText:'Signature saved.'}).waitFor({state:'attached'});
  assert.doesNotMatch(posts.filter(p=>p.action==='set_signature').at(-1).args.html,/mso-|class=|-webkit-/i);
  // Typing after it, and bold from the toolbar, stay as they are.
  await body.click();await page.keyboard.type(' ok');await page.keyboard.press('Shift+Home');
  await page.locator('#signatures [data-sig-tool="bold"]').click();await page.waitForTimeout(100);
  assert.match(await body.innerHTML(),/font-weight|<b>/);
  await context.close();signatures=fresh()}
 // The HTML view: a paste there shows Save.
 {const {context,page,form,save}=await open(1440,900);
  await form.locator('[data-sig-tool="html"]').click();
  await page.evaluate(()=>navigator.clipboard.writeText('<b>Robin Example</b>'));
  await form.locator('.sig-source').click();await page.keyboard.press('Control+V');
  await save.waitFor();assert.match(await form.locator('.sig-source').inputValue(),/Robin Example/);
  await context.close()}
 // A form that can't be saved (a mailbox without the right access) stays without Save.
 {signatures=[{...fresh()[0],saveable:false,html:'<p>Robin Example</p>'}];
  const {context,page,save}=await open(1440,900);await page.waitForTimeout(300);
  assert.equal(await save.isHidden(),true);await context.close();signatures=fresh()}
 if(shots)for(const scheme of ['light','dark'])for(const [w,h] of [[390,844],[1440,900]]){
  const {context,page,body,save}=await open(w,h,scheme);await body.click();await pasteHtml(page,OUTLOOK);await save.waitFor();await page.waitForTimeout(400);
  await page.screenshot({path:`${shots}/sig-after-paste-${w}x${h}-${scheme}.png`});await context.close()}
 assert.deepEqual(errors,[]);
 console.log('signature paste save dashboard ok');
}finally{await browser?.close();server.close()}
