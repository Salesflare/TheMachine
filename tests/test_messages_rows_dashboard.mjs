import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Messages rows, on made-up data, as the service sends them (message_view.list_row, tests/test_message_view.py checks
// every kind there): the account by its Connections name (Work, not its address; the address only when two accounts of
// one app would read the same), a transcript as speaker turns without stamps, and "Open in …" in the same place on
// every row that has a link, none on a row without one. At 390 and 1440.
const dashboard=await dashboardPage();
const now=Date.now(),ago=h=>new Date(now-h*36e5).toISOString();
const row=(title,who,text,url='',app='',more={})=>({title,who,text,url,app,...more});
const ROWS=[
 {id:1,account_id:'work-mail',kind:'gmail.message',title:'Booth quote',occurred_at:ago(1),body:'Here is the quote.',metadata:{from:'Avery Stone <avery@booths.example>',source_url:'https://mail.example/1'},
  row:row('Booth quote','Avery Stone','Here is the quote.','https://mail.example/1','Gmail')},
 {id:2,account_id:'work-cal',kind:'meeting.transcript',title:'Weekly sync',occurred_at:ago(2),body:'[0:00:00] Kit Navarro: Morning all.\n[0:00:06] Robin Hale: Morning.',metadata:{},
  row:row('Weekly sync','','Kit Navarro: Morning all.\nRobin Hale: Morning.','','',{turns:[{from:'Kit Navarro',body:'Morning all.'},{from:'Robin Hale',body:'Morning.'}]})},
 {id:3,account_id:'chat',kind:'whatsapp.message',title:'Climbing crew',occurred_at:ago(3),body:'Who is in for Saturday?',metadata:{},row:row('Climbing crew','Sasha Brook','Who is in for Saturday?')},
 {id:4,account_id:'side-mail',kind:'gmail.message',title:'Fair stand sizes',occurred_at:ago(4),body:'Two sizes.',metadata:{source_url:'https://mail.example/4'},
  row:row('Fair stand sizes','Lee Park','Two sizes.','https://mail.example/4','Gmail')},
 {id:5,account_id:'feed',kind:'rss.item',title:'Release notes',occurred_at:ago(5),body:'Faster exports.',metadata:{source_url:'https://blog.example/5'},
  row:row('Release notes','','Faster exports.','https://blog.example/5','')}];
const connectors=[{id:'work-mail',service:'gmail',card_title:'sam@acme.example',card_subtitle:'Work'},{id:'work-cal',service:'calendar',card_title:'sam@acme.example',card_subtitle:'Work'},
 {id:'chat',service:'whatsapp',card_title:'WhatsApp',card_subtitle:'Personal'},{id:'side-mail',service:'gmail',card_title:'sam@side.example',card_subtitle:'Work'},
 {id:'feed',service:'rss',card_title:'Acme blog',card_subtitle:'Work'}];
const state=()=>({suggestions:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},
 connectors,fleet:{on:false,fleets:[]},model_status:{model:'acme/lm-2'}});
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(state()));return}
 if(url.pathname==='/api/events'){res.end(JSON.stringify(ROWS));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/';
const errors=[];let browser;
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [width,height] of [[390,844],[1440,900]]){const mobile=width<600;
  const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,locale:'en-US',timezoneId:'Europe/Brussels'});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  const page=await context.newPage();page.on('pageerror',e=>errors.push(width+': '+e.message));
  await page.goto(base+'#messages');await page.locator('#results article').nth(ROWS.length-1).waitFor();
  const rows=await page.$$eval('#results article',as=>as.map(a=>{const link=a.querySelector('a.open'),body=a.querySelector('.body');
   return {title:a.querySelector('h3').textContent,meta:a.querySelector('small').textContent,body:body?.innerText||'',turns:!!a.querySelector('.ev-turns b'),
    open:link?.textContent||'',href:link?.getAttribute('href')||'',linkAfterBody:!link||link.previousElementSibling===body,
    linkLeft:link?Math.round(link.getBoundingClientRect().left-a.getBoundingClientRect().left):null}}));
  const by=Object.fromEntries(rows.map(r=>[r.title,r]));
  // the account by its card's name: Work, never the address, unless another Gmail would read the same
  assert.match(by['Weekly sync'].meta,/^Work · /,width+': a calendar account by its scope');
  assert.match(by['Climbing crew'].meta,/^Personal · .* · From Sasha Brook$/,width+': the app’s name is the icon’s, not the meta line’s');
  assert.match(by['Booth quote'].meta,/^sam@acme\.example · .* · Avery Stone$/,width+': two Work Gmails are told apart by address');
  assert.match(by['Release notes'].meta,/^Acme blog · /,width+': a named account by its name');
  for(const r of rows)assert.doesNotMatch(r.meta+r.body,/work-mail|side-mail|\[0:\d/,width+': no ids or stamps: '+r.title);
  // a transcript reads as who said what
  assert.ok(by['Weekly sync'].turns,width+': a transcript shows its speakers');
  assert.match(by['Weekly sync'].body,/^Kit Navarro Morning all\.\nRobin Hale Morning\.$/);
  // every row with a link has it, under its text, at the same left; a row with none has none
  assert.deepEqual(rows.map(r=>r.open),['Open in Gmail ↗','','','Open in Gmail ↗','Open original'],width+': '+JSON.stringify(rows.map(r=>r.open)));
  assert.ok(rows.every(r=>r.linkAfterBody),width+': the link sits under the text');
  assert.equal(new Set(rows.filter(r=>r.open).map(r=>r.linkLeft)).size,1,width+': every link at the same left');
  assert.equal(by['Release notes'].href,'https://blog.example/5');
  await context.close()}
 assert.deepEqual(errors,[]);
}finally{await browser?.close();server.close()}
console.log('ok');
