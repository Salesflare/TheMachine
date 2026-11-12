import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
const {chromium}=await import('./browser.mjs');

// The viewer's clipboard bridge (deploy/browser/machine-clipboard.js) on a stand-in noVNC. Pasting into the Machine's
// browser takes the text from the paste event itself, so it works without the clipboard-read permission (an installed
// app or a framed viewer often never showed that prompt, and Ctrl+V did nothing): the text goes to the browser there
// as its clipboard, then its own Ctrl+V. A phone's long-press Paste on the on-screen keyboard's box does the same. Only
// a browser that sends no paste event falls back to reading the clipboard. The pasted text is never logged.
const bridge=await readFile(new URL('../deploy/browser/machine-clipboard.js',import.meta.url),'utf8');
// noVNC's parts that the bridge uses: its connection object, recording what it sends to the VNC server
const ui=`const sent=window.sent=[];
const rfb={clipboardPasteFrom(text){sent.push(['clipboard',text])},sendKey(sym,code,down){sent.push(['key',code,down])},addEventListener(){}};
document.getElementById('noVNC_container').querySelector('canvas').addEventListener('keydown',e=>sent.push(['novnc',e.key]));  // noVNC's own keys
export default {rfb};`;
const page=`<!doctype html><html><head><script type="module" src="machine-clipboard.js"></script></head><body>
<div id="noVNC_container"><canvas tabindex="-1" width="400" height="300"></canvas><textarea id="noVNC_keyboardinput"></textarea></div>
<div id="noVNC_control_bar"><textarea id="noVNC_clipboard_text"></textarea></div></body></html>`;
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');
 const send=(type,body)=>{res.setHeader('Content-Type',type);res.end(body)};
 if(url.pathname==='/browser/')return send('text/html',page);
 if(url.pathname==='/browser/machine-clipboard.js')return send('text/javascript',bridge);
 if(url.pathname==='/browser/app/ui.js')return send('text/javascript',ui);
 res.statusCode=404;res.end()});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/browser/',SECRET='https://example.com/p?k=hunter2-not-logged',errors=[],said=[];let browser;
const sent=p=>p.evaluate(()=>{const s=window.sent.slice();window.sent.length=0;return s});
const pasted=text=>[['clipboard',text],['key','ControlLeft',true],['key','KeyV',true],['key','KeyV',false]];
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 // Only clipboard-write: reading the clipboard is never allowed here, as for an owner who never answered its prompt
 const context=await browser.newContext({viewport:{width:600,height:400}});
 await context.grantPermissions(['clipboard-write'],{origin:base});
 const p=await context.newPage();p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>said.push(m.text()));
 await p.goto(base);await p.waitForFunction(()=>window.sent);
 await p.evaluate(()=>{navigator.clipboard.readText=()=>{window.sent.push(['read']);return Promise.reject(new Error('not allowed'))}});
 await p.evaluate(t=>navigator.clipboard.writeText(t),SECRET);

 // Ctrl+V on the screen: the paste event's text, then Ctrl+V over there; noVNC never sees the V, no clipboard read
 await p.locator('canvas').focus();
 await p.keyboard.press('Control+V');await p.waitForTimeout(250);
 assert.deepEqual(await sent(p),[['novnc','Control'],...pasted(SECRET)],'Ctrl+V pastes the local clipboard there');

 // A phone's long-press Paste in the on-screen keyboard's box: the same, and the box itself stays empty
 await p.evaluate(t=>{const d=new DataTransfer();d.setData('text/plain',t);
  document.getElementById('noVNC_keyboardinput').dispatchEvent(new ClipboardEvent('paste',{clipboardData:d,bubbles:true,cancelable:true}))},'café ✓ 42');
 await p.waitForTimeout(150);
 assert.deepEqual(await sent(p),pasted('café ✓ 42'),'a long-press Paste on a phone');
 assert.equal(await p.inputValue('#noVNC_keyboardinput'),'');

 // noVNC's side panel clipboard box pastes as any text box: not taken over
 await p.locator('#noVNC_clipboard_text').focus();await p.keyboard.press('Control+V');await p.waitForTimeout(250);
 assert.deepEqual(await sent(p),[]);
 assert.equal(await p.inputValue('#noVNC_clipboard_text'),SECRET);

 // A browser that sends no paste event (a key press with no default action): it falls back to reading the clipboard,
 // and when that is refused still sends Ctrl+V, so the browser there pastes what it has
 await p.locator('canvas').focus();
 await p.evaluate(()=>document.querySelector('canvas').dispatchEvent(new KeyboardEvent('keydown',{key:'v',code:'KeyV',ctrlKey:true,bubbles:true,cancelable:true})));
 await p.waitForTimeout(300);
 assert.deepEqual(await sent(p),[['read'],['key','ControlLeft',true],['key','KeyV',true],['key','KeyV',false]],'the fallback');
 // ...and with the clipboard readable, its text goes over first
 await p.evaluate(()=>{navigator.clipboard.readText=()=>Promise.resolve('read text')});
 await p.evaluate(()=>document.querySelector('canvas').dispatchEvent(new KeyboardEvent('keydown',{key:'v',code:'KeyV',ctrlKey:true,bubbles:true,cancelable:true})));
 await p.waitForTimeout(300);
 assert.deepEqual(await sent(p),pasted('read text'));

 // Other Ctrl keys stay noVNC's (Ctrl+C copies there)
 await p.keyboard.press('Control+c');await p.waitForTimeout(100);
 assert.deepEqual(await sent(p),[['novnc','Control'],['novnc','c']]);

 assert.ok(!said.some(s=>s.includes('hunter2')),'the pasted text is never logged');
 assert.deepEqual(errors,[]);
 console.log('machine clipboard ok');
}finally{await browser?.close();server.close()}
