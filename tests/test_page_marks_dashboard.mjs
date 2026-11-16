import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// What the whole page's layout follows is a class on <html> and <body> (m-chat, m-cal, ...), never a body:has() or
// html:has() rule: one of those made every change anywhere in the page check the whole page's style again. Each class
// tracks its state: on and off at the moment the state changes (in the same task for a tab switch and a chat), on a
// deep link, on back and forward, and for the states the page draws itself (Talk's bar, a Graph trail, a dialog).
const dashboard=await dashboardPage();
const now=new Date().toISOString();
const cards=[{id:'a1a1a1a1a1a1a1a1',title:'Check the payroll is ready',body:'Ready.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[1]},
 {id:'b2b2b2b2b2b2b2b2',title:'Book the room',body:'Booked.',status:'prepared',preparation_status:'ok',scope:'work',created_at:now,event_ids:[2]}];
const state=()=>({suggestions:cards,promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors:[],fleet:{on:false,fleets:[]}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base=`http://127.0.0.1:${server.address().port}/`;
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,locale:'en-US'});
 await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 const open=async hash=>{const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(base+(hash||''));
  await page.waitForFunction(()=>typeof drawnWhole!=='undefined'&&drawnWhole);return page};
 // The marks on <html> and on <body> (the same on both)
 const marks=page=>page.evaluate(()=>{const m=e=>[...e.classList].filter(c=>c.startsWith('m-')).sort().join(' ');
  const a=m(document.documentElement),b=m(document.body);if(a!==b)throw new Error(`html has "${a}", body "${b}"`);return a});
 const settle=page=>page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>r())));

 let page=await open();
 // No rule of the page's style sheets (its own, the lazy parts' and the ones its script adds) asks body:has() or html:has()
 const ruled=await page.evaluate(()=>{const out=[];const walk=rules=>{for(const r of rules){if(r.selectorText&&/(^|[\s,>+~(])(html|body)(\.[\w-]+|\[[^\]]*\])*:has\(/.test(r.selectorText))out.push(r.selectorText);if(r.cssRules)walk(r.cssRules)}};
  for(const s of document.styleSheets)try{walk(s.cssRules)}catch{}return out});
 assert.deepEqual(ruled,[],'no body:has() or html:has() rule');
 assert.equal(await marks(page),'','the To-dos list: no marks');

 // A chat on To-dos: m-chat in the same task as the render that opens it, gone on Back, there again on Forward
 assert.equal(await page.evaluate(id=>{history.replaceState(null,'','#chat='+id);openChatLink();return document.body.classList.contains('m-chat')},cards[1].id),true,'m-chat as the chat opens');
 await page.evaluate(()=>{history.replaceState(null,'',location.pathname);openChatLink()});await settle(page);
 assert.equal(await marks(page),'','closed');
 await page.evaluate(id=>{location.hash='#chat='+id},cards[0].id);await page.waitForFunction(()=>document.body.classList.contains('chat-open'));
 assert.equal(await marks(page),'m-chat','a chat link');
 await page.goBack();await page.waitForFunction(()=>!document.body.classList.contains('chat-open'));
 assert.equal(await marks(page),'','back to the list');
 await page.goForward();await page.waitForFunction(()=>document.body.classList.contains('chat-open'));
 assert.equal(await marks(page),'m-chat','forward to the chat');
 // Another tab over the open chat: the marks move in the same task as the switch, and back on To-dos the chat is there
 assert.equal(await page.evaluate(()=>{document.querySelector('nav [data-tab="calendar"]').click();return [...document.body.classList].filter(c=>c.startsWith('m-')).sort().join(' ')}),'m-cal','a tab switch moves the marks at once');
 assert.equal(await page.evaluate(()=>{document.querySelector('nav [data-tab="inbox"]').click();return [...document.body.classList].filter(c=>c.startsWith('m-')).sort().join(' ')}),'m-chat','back on To-dos with the chat');
 // A usage-limit banner over a chat
 await page.evaluate(()=>{$('#limit-banner').hidden=false});await settle(page);
 assert.equal(await marks(page),'m-chat m-limit','a limit banner over the chat');
 await page.evaluate(()=>{$('#limit-banner').hidden=true});await settle(page);
 assert.equal(await marks(page),'m-chat');
 await page.close();

 // Deep links: the mark is there once the page is drawn
 page=await open('#chat='+cards[1].id);await page.waitForFunction(()=>document.body.classList.contains('m-chat'));await page.close();
 page=await open('#calendar');await page.waitForFunction(()=>document.body.classList.contains('m-cal'));
 // The calendar's week: m-week as it draws it, gone in Agenda
 await page.evaluate(async()=>{await lazyPart('calendar');calSetMode('week')});await settle(page);
 assert.equal(await marks(page),'m-cal m-week','week');
 await page.evaluate(()=>calSetMode('agenda'));await settle(page);
 assert.equal(await marks(page),'m-cal','agenda');
 await page.close();

 page=await open();
 // Talk's own view, and its bar floating at the bottom of the page
 await page.evaluate(()=>{$('#talk-view').hidden=false});await settle(page);
 assert.equal(await marks(page),'m-talk');
 await page.evaluate(()=>{$('#talk-view').hidden=true;const d=document.createElement('div');d.id='talk-dock';document.body.append(d)});await settle(page);
 assert.equal(await marks(page),'m-dock');
 await page.evaluate(()=>$('#talk-dock').remove());await settle(page);
 assert.equal(await marks(page),'');
 // The browser pane
 await page.evaluate(()=>{for(const x of document.querySelectorAll('main>section'))x.hidden=x.id!=='browser-pane'});await settle(page);
 assert.equal(await marks(page),'m-browser');
 await page.evaluate(()=>document.querySelector('nav [data-tab="people"]').click());await settle(page);
 assert.equal(await marks(page),'','the Graph after the pane');
 // The Graph: a trail with a way back, a note's trail, a project board; each only while the Graph shows it
 await page.evaluate(()=>$('#people').insertAdjacentHTML('beforeend','<div class="graph-crumbs" id="t1"><a href="#graph" data-crumb="">Graph</a></div>'));await settle(page);
 assert.equal(await marks(page),'','a trail without a way back');
 await page.evaluate(()=>$('#t1 a').dataset.crumb='people');await settle(page);
 assert.equal(await marks(page),'m-trail');
 await page.evaluate(()=>{$('#t1').remove();$('#people').insertAdjacentHTML('beforeend','<div class="graph-crumbs note-crumbs" id="t2"></div><div class="sub-pane" id="t3"><div class="proj-board" hidden></div></div>')});await settle(page);
 assert.equal(await marks(page),'m-note-trail');
 await page.evaluate(()=>$('#t3 .proj-board').hidden=false);await settle(page);
 assert.equal(await marks(page),'m-board m-note-trail');
 await page.evaluate(()=>document.querySelector('nav [data-tab="inbox"]').click());await settle(page);
 assert.equal(await marks(page),'','the Graph hidden');
 await page.evaluate(()=>{$('#t2').remove();$('#t3').remove()});
 // Connections split in two (a category open, not the index)
 await page.evaluate(()=>{document.querySelector('nav [data-tab="health"]').click();const h=$('#health');h.classList.add('conn-split','conn-index')});await settle(page);
 assert.equal(await marks(page),'','the index');
 await page.evaluate(()=>$('#health').classList.remove('conn-index'));await settle(page);
 assert.equal(await marks(page),'m-conn-split');
 await page.evaluate(()=>document.querySelector('nav [data-tab="inbox"]').click());await settle(page);
 // Dialogs: a modal one (not the palette or New to-do), and the sign-in viewer full size
 await page.evaluate(()=>$('#skill-look').showModal());await settle(page);
 assert.equal(await marks(page),'m-modal');
 await page.evaluate(()=>$('#skill-look').close());await settle(page);
 assert.equal(await marks(page),'');
 await page.evaluate(()=>{const d=$('#signin-dialog');d.classList.add('signin-full');d.showModal()});await settle(page);
 assert.equal(await marks(page),'m-modal m-signin-full');
 await page.evaluate(()=>$('#signin-dialog').close());await settle(page);
 assert.equal(await marks(page),'');
 await page.close();
 assert.deepEqual(errors,[]);
 console.log('ok: page marks track their states');
}finally{await browser?.close();server.close()}
