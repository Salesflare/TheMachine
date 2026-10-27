import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {OPENCLAW} from '../openclaw-root.mjs';
const {chromium}=await import(OPENCLAW+'/node_modules/playwright-core/index.mjs');

// The email editor: a draft is edited as it will look (bold, italic, lists, links), never as marks or HTML. The
// dashboard draws an email's marks exactly as the send writes them (mail_format_cases.json, also checked against
// next_actions.mail_html); what the editor holds reads back into those marks, and Send only sends when the read-back
// draws the same as the page. A paste comes in as plain text, a link must be https, formatting an email can't carry is
// taken out before anything goes, and a text the save tidied shows before it is sent.
const dashboard=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const CASES=JSON.parse(await readFile(new URL('./mail_format_cases.json',import.meta.url),'utf8'));
const now=new Date().toISOString(),posts=[];
const BODY='Hi Noor,\n\nThe plan:\n- **Monday**: kickoff\n- the [brief](https://example.com/brief)\n\nAlex';
const card=()=>({id:'r1',title:'Send Noor the plan',body:'Draft ready.',status:'prepared',scope:'work',created_at:now,preparation_status:'done',event_ids:[2],
 next_actions:[{kind:'email',revision:'v1',label:'Send to Noor',to:['noor@example.com'],to_name:'Noor',from:'alex@example.com',subject:'Plan',body:BODY}]});
let cards=[card()],tidy=null;
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{let body='';for await(const c of req)body+=c;const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname.startsWith('/brand/')){res.statusCode=404;res.end();return}
 if(req.method==='POST'&&body){const b=JSON.parse(body);posts.push({action:b.action,...b.args});
  if(b.action==='revise_draft'){const saved=tidy?tidy(b.args.body):b.args.body;res.end(JSON.stringify({status:'revised',revision:'v'+(posts.length+1),body:saved,subject:b.args.subject}));return}}
 res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const errors=[];let browser;
const sent=()=>posts.filter(p=>p.action==='confirm_action');
const revised=()=>posts.filter(p=>p.action==='revise_draft');
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1280,height:900},locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#task-r1').waitFor();
 // The dashboard draws every recorded case exactly as the send writes it, and reading a drawn case back changes nothing
 {const out=await page.evaluate(cases=>cases.map(c=>{const html=mailHtml(c.body,false),d=document.createElement('div');d.innerHTML=html;const m=mailModel(d),again=mailModelOf(mailBody(m));
   return {html,same:JSON.stringify(again)===JSON.stringify(m)}}),CASES);
  CASES.forEach((c,i)=>{assert.equal(out[i].html,c.html,'drawn like the send: '+JSON.stringify(c.body));assert.ok(out[i].same,'reads back the same: '+JSON.stringify(c.body))})}
 // The card shows the email as it will look: a real list, bold, a link
 const db=page.locator('#task-r1 .db');
 assert.equal(await db.locator('li').count(),2);assert.equal(await db.locator('li b').innerText(),'Monday');assert.equal(await db.locator('a').getAttribute('href'),'https://example.com/brief');
 assert.doesNotMatch(await db.innerText(),/\*\*|\]\(/);
 const open=async()=>{await page.locator('#task-r1 [data-smart]').first().click();await page.locator('#send-dialog[open]').waitFor();await page.locator('#send-rich-body').waitFor()};
 const rich=page.locator('#send-rich-body');
 const body=()=>page.evaluate(()=>mailBody(mailModel(mailRich())));
 // Opens in the editor with the formatting, the toolbar beside it; untouched it sends as drafted, without a save
 await open();
 assert.equal(await rich.getAttribute('contenteditable'),'true');assert.equal(await rich.locator('ul li').count(),2);assert.equal(await rich.locator('b').innerText(),'Monday');
 assert.deepEqual(await page.locator('[data-mail-tool]').evaluateAll(b=>b.map(x=>x.getAttribute('aria-label'))),['Bold','Italic','Bulleted list','Numbered list','Link']);
 assert.equal(await page.evaluate(()=>document.activeElement.id),'send-rich-body');
 await page.locator('#send-confirm').click();await page.locator('#send-dialog').waitFor({state:'hidden'});
 assert.equal(revised().length,0);assert.equal(sent().at(-1).revision,'v1');
 // Formatting from the keyboard and the toolbar: bold, italic, a numbered list, a link; it goes out as the marks
 await open();
 await rich.click();await page.keyboard.press('Control+End');await page.keyboard.press('Enter');
 await page.keyboard.press('Control+b');await page.keyboard.type('Note');await page.keyboard.press('Control+b');await page.keyboard.type(': read it ');
 await page.keyboard.press('Control+i');await page.keyboard.type('today');await page.keyboard.press('Control+i');await page.keyboard.press('Enter');
 assert.equal(await page.locator('[data-mail-tool="b"]').getAttribute('aria-pressed'),'false');
 await page.locator('[data-mail-tool="ol"]').click();await page.keyboard.type('first');await page.keyboard.press('Enter');await page.keyboard.type('second');
 await page.keyboard.press('Enter');await page.keyboard.press('Enter');
 await page.keyboard.type('Plain * star, a_b and [brackets] stay text. ');
 await page.keyboard.press('Control+k');await page.locator('#send-rich-url').waitFor();
 // a link is an https address: javascript: is refused, a bare name gets https://
 await page.locator('#send-rich-url').fill('javascript:alert(1)');await page.keyboard.press('Enter');
 assert.ok(await page.locator('#send-rich-link').isVisible(),'refused');assert.equal(await rich.locator('a[href^="javascript"]').count(),0);
 await page.locator('#send-rich-url').fill('example.com/docs');await page.keyboard.press('Enter');
 assert.ok(await page.locator('#send-rich-link').isHidden());assert.equal(await rich.locator('a[href="https://example.com/docs"]').count(),1);
 const expected='Hi Noor,\n\nThe plan:\n- **Monday**: kickoff\n- the [brief](https://example.com/brief)\n\nAlex\n**Note**: read it _today_\n1. first\n2. second\nPlain \\* star, a\\_b and \\[brackets\\] stay text. https://example.com/docs';
 assert.equal(await body(),expected);
 await page.locator('#send-confirm').click();await page.locator('#send-dialog').waitFor({state:'hidden'});
 assert.equal(revised().at(-1).body,expected);
 {const i=posts.findLastIndex(p=>p.action==='revise_draft'),j=posts.findLastIndex(p=>p.action==='confirm_action');assert.equal(j,i+1,'saved, then sent');assert.equal(posts[j].revision,'v'+(i+2))}
 // What the editor showed is what the send draws: the saved text, drawn as the mail, reads the same as the page did
 assert.ok(await page.evaluate(b=>{const d=document.createElement('div');d.innerHTML=mailHtml(b,false);return d.querySelectorAll('ol li').length===2&&d.querySelector('i').textContent==='today'},expected));
 // A paste is plain text: no images, scripts, styles or foreign links come in
 cards=[card()];await page.evaluate(()=>refresh());await open();
 await rich.locator('div',{hasText:/^Alex$/}).click();await page.keyboard.press('Home');
 await rich.evaluate(n=>{const dt=new DataTransfer();dt.setData('text/html','<img src=x onerror="window.pwned=1"><b style="color:red">Pasted</b> <a href="javascript:alert(1)">link</a><script>window.pwned=2</script>');dt.setData('text/plain','Pasted link\nsecond line');
  n.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}))});
 assert.equal(await rich.locator('img,script,a[href^="javascript"],[style*="color"]').count(),0);assert.equal(await page.evaluate(()=>window.pwned),undefined);
 assert.match(await body(),/\n\nPasted link\nsecond lineAlex$/);
 // Formatting an email can't carry (a heading, underline, a color, an image) is taken out first; Send waits, then sends that
 await rich.evaluate(n=>n.insertAdjacentHTML('beforeend','<h1>Big</h1><div><u>under</u> <span style="color:red">red</span><img src="https://example.com/x.png"></div>'));
 const before=posts.length;
 await page.locator('#send-confirm').click();await page.waitForFunction(()=>/can’t go in an email/.test(document.querySelector('#send-error').textContent));
 assert.equal(posts.length,before,'nothing saved or sent');assert.ok(await page.locator('#send-dialog').evaluate(d=>d.open));
 assert.equal(await rich.locator('h1,u,img,[style*="color"]').count(),0,'the page now shows what goes out');
 await page.locator('#send-confirm').click();await page.locator('#send-dialog').waitFor({state:'hidden'});
 assert.match(revised().at(-1).body,/\nBig\nunder red$/);
 // A save that tidies the text (a blank line before the name): it shows, and Send sends it on the next tap, unchanged
 cards=[card()];await page.evaluate(()=>refresh());tidy=b=>b.replace(/\nAlex$/,'\n\nAlex');await open();
 await rich.locator('div',{hasText:/^Alex$/}).click();await page.keyboard.press('Home');await page.keyboard.type('Cheers,');await page.keyboard.press('Enter');
 await page.keyboard.press('ArrowUp');await page.keyboard.press('ArrowUp');await page.keyboard.press('End');await page.keyboard.press('Backspace');
 const n0=revised().length,s0=sent().length;
 await page.locator('#send-confirm').click();await page.waitForFunction(()=>/small change/.test(document.querySelector('#send-error').textContent));
 assert.equal(revised().length,n0+1);assert.equal(sent().length,s0,'not sent yet');
 assert.match(await body(),/Cheers,\n\nAlex$/);
 await page.locator('#send-confirm').click();await page.locator('#send-dialog').waitFor({state:'hidden'});
 assert.equal(revised().length,n0+1,'no second save');assert.equal(sent().at(-1).revision,'v'+(posts.findLastIndex(p=>p.action==='revise_draft')+2));tidy=null;
 // Phone: the toolbar and the text fit the screen
 await page.setViewportSize({width:390,height:844});cards=[card()];await page.evaluate(()=>refresh());await open();
 assert.ok(await page.evaluate(()=>{const d=document.querySelector('#send-dialog').getBoundingClientRect(),t=document.querySelector('.mail-tools').getBoundingClientRect();return t.right<=d.right&&document.documentElement.scrollWidth<=innerWidth}));
 if(process.env.SHOT_DIR)await page.screenshot({path:process.env.SHOT_DIR+'/email-editor-phone.png'});
 await context.close();
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('email editor ok');
