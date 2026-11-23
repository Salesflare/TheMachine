import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {existsSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
import vm from 'node:vm';
import {dashboardPage} from './dashboard-page.mjs';
const {chromium}=await import('./browser.mjs');

// Which to-dos are in For you, and in which order, is todos-for-you.js alone: run by itself, outside any page (as the
// desktop robot runs it), it gives the same to-dos in the same order as the dashboard draws, with the same count, for
// every state a to-do can be in.
const DAY=864e5,at=d=>new Date(Date.now()+d*DAY).toISOString(),local=d=>{const x=new Date(Date.now()+d*DAY);return [x.getFullYear(),String(x.getMonth()+1).padStart(2,'0'),String(x.getDate()).padStart(2,'0')].join('-')};
let n=0;
const todo=(title,extra={})=>({id:(++n).toString(16).padStart(16,'c'),title,body:'Made up.',status:'pending',scope:'work',created_at:at(-1-n/100),event_ids:[n],...extra});
const draft=(extra={})=>({kind:'email',label:'Send',account_id:'work',from:'owner@example.com',to:['noor@example.com'],subject:'Re: Alpha',body:'Hi Noor',revision:'r'+n,...extra});
const follow=(title,board,extra={})=>todo(title,{status:'prepared',next_action:draft(),follow_up:{project:title,project_id:'project:'+n,board:board&&'Alpha testers',group:board,n:1,max:3,channel:'email',auto:false,state:'open'},...extra});
const said=state=>JSON.stringify({state,waiting_on:'the review'});
const FL='fl_'+'a'.repeat(16);
const todos=()=>{n=0;return [
 todo('New'),todo('New, Personal',{scope:'personal'}),todo('New, no area',{scope:null}),
 todo('Accepted',{status:'accepted'}),todo('Changes asked',{status:'instructions',preparation_status:'running'}),
 todo('Prepared',{status:'prepared',next_action:draft()}),todo('Prepared, needs the owner',{status:'prepared',needs_owner:true}),
 todo('Blocked',{status:'accepted',preparation_status:'blocked'}),
 todo('Done',{status:'completed',closed_at:at(-.1)}),todo('Not needed',{status:'rejected',closed_at:at(-.1)}),
 todo('Snoozed',{status:'snoozed',snoozed_until:at(2)}),
 todo('Snoozed, its time has passed',{status:'snoozed',snoozed_until:at(-.01),resume_status:'prepared'}),
 todo('Overdue',{due:local(-2)}),todo('Due tomorrow',{due:local(1),status:'prepared',next_action:draft()}),todo('Due next week',{due:local(7)}),
 todo('Due at a time that passed',{due:local(0),due_at:at(-.02)}),
 todo('Looks done, by its run',{status:'prepared',outcome:said('already_done'),looks_done_at:at(-.1)}),todo('Looks done, by a message',{handled_hint:'replied'}),
 todo('Waits on others',{status:'prepared',outcome:said('waiting')}),todo('Answered',{status:'prepared',outcome:said('answered')}),
 todo('Still needed?',{created_at:at(-9),still_needed:{id:'sn_1',since:at(-1),folded:false}}),todo('Still needed? folded',{created_at:at(-16),still_needed:{id:'sn_2',since:at(-8),folded:true}}),
 todo('Older',{created_at:at(-12),older:at(-9)}),todo('Older, and due',{created_at:at(-12),older:at(-9),due:local(0)}),
 todo('Older, its send on its way',{created_at:at(-12),older:at(-9),status:'prepared',next_action:draft(),action_status:{status:'queued'}}),
 todo('Its send on its way',{status:'prepared',next_action:draft(),action_status:{status:'sending'}}),
 todo('Its send failed, to try again',{status:'prepared',next_action:draft(),action_status:{status:'uncertain',retry_ok:true}}),
 todo('A digest',{digest:{items:[]}}),todo('A briefing',{briefing:{at:at(1)}}),
 todo('A cleanup, decided',{cleanup:{kind:'newsletters',items:[{n:1,from:'News',address:'news@letters.example',title:'This week',event:1,count:1,state:'done',plan:'one_click'}]}}),
 todo('Came back',{created_at:at(-20),reopened_at:at(-.2)}),
 todo('Same moment, b',{created_at:at(-3).slice(0,19)+'Z',weight:1}),todo('Same moment, a',{created_at:at(-3).slice(0,19)+'Z',weight:5}),todo('Same moment, c',{created_at:at(-3).slice(0,19)+'Z',weight:1}),
 follow('Follow-up one','board:1'),follow('Follow-up two','board:1'),follow('Follow-up three, being written','board:1',{status:'accepted',next_action:null}),
 follow('Follow-up stuck','board:1',{status:'pending'}),follow('Follow-up of another board, being written','board:2',{status:'accepted',next_action:null}),
 follow('Follow-up of a project',null),follow('Follow-up on its way','board:1',{action_status:{status:'queued'}})]};
const ask=(i,kind,extra={})=>({id:'q_'+String(i).repeat(16),fleet:FL,member_id:'p',name:'Pat',kind,status:'waiting',at:at(-1),question:'An intro to someone at client.example',...extra});
const fleet=()=>({on:true,kinds:{},fleets:[{id:FL,kind:'work',label:'Work Fleet',name:'Acme',asks:[],people:[],members:[{member_id:'p',name:'Pat',rules:{}}],rules:{},exceptions:{}}],friends:{id:'fl_'+'b'.repeat(16),name:'Friends',members:[],people:[]},
 waiting:[ask(1,'intro'),ask(2,'handoff'),ask(3,'brief'),ask(4,'relationships'),ask(5,'anything',{question:'Who knows the venue?',draft:{state:'ready',text:'',matches:[]}})],
 asked:[],intro_offers:[],log:[],notices:[{id:'n1',fleet:FL,text:'Robin wants to be friends',kind:'friend_request',buttons:[['accept','Accept'],['decline','Decline']],detail:'',reason:''},{id:'n2',fleet:FL,text:'Only a line',kind:'line',buttons:[]}],
 shared:{prompts:[{id:'p1',kind:'member',fleet:FL,name:'Kim',email:'kim@acme.example',fp:'ab12 cd34'}],shares:[],accounts:[],can_share:[],graph:[]},
 network:{find:true,discoverable:true,asked:true,last:at(-1),people:[]}});
const base=()=>({suggestions:todos(),follow_up_progress:[],promises:[],suggestion_counts:{},decisions:[],analyses:[],deliveries:[],review_health:{},review_runs:[],review_live:{runs:[]},connectors:[],
 fleet:{on:false,fleets:[]},locale:{language:'en',todo_scope:'all',saveable:true},hours:{days:[1,2,3,4,5],start:'08:00',end:'18:00',morning:'09:00',digest_at:'08:30',timezone:'UTC',saveable:true}});
const on={fleet:{on:true,waiting:6,stamp:'s1',fleets:[]}};
const lead=()=>({greeting:{line:{text:'Start with this one.',card:todos()[5].id}}});
const CASES={
 'everything':{},'Work':{locale:{language:'en',todo_scope:'work'}},'Personal':{...on,locale:{language:'en',todo_scope:'personal'}},
 'with Fleet items':on,'the hello leads':lead(),'a batch going out':{follow_up_progress:[{group:'board:1',board:'Alpha testers',batch:'b1',total:3,done:1,sent:1,going:true}]},
 'nothing':{suggestions:[]},
 'an older Machine, that says less':{suggestions:todos().map(({older,still_needed,reopened_at,weight,handled_hint,follow_up,...s})=>s),follow_up_progress:undefined,locale:undefined}};

// The rules by themselves, with the few names they ask of a page
const rules=await readFile(new URL('../dashboard/todos-for-you.js',import.meta.url),'utf8');
const NAMES=`class SafeHTML{constructor(title){this.title=title}}
const TODO={CLOSED:['completed','rejected'],OPEN_NOT_SNOOZED:['pending','accepted','prepared','instructions']},SENDS=['email','whatsapp'];
const t=(k,...a)=>(Array.isArray(k)?k[a.find(x=>!isNaN(+x))==1?0:1]:k).replace(/\\{\\}/g,()=>a.shift());
const fuGroupCard=(g,all)=>new SafeHTML(fuGroupTitle(all));let state={};
function forYou(status,fleet){state=status;wakeDue(state.suggestions);const scope=state.locale?.todo_scope||'all';
 return todoLists(scopeShown(state.suggestions,scope),scope==='personal'||!state.fleet?.on?[]:fleetRows(fleet).map(r=>new SafeHTML(r.title)),state.greeting?.line?.card).fuv.foryou.map(x=>x.title)}`;
const context=vm.createContext({});vm.runInContext(NAMES,context);vm.runInContext(rules,context);
const alone=async(status,fleet)=>JSON.parse(vm.runInContext(`JSON.stringify(forYou(${JSON.stringify(status)},${JSON.stringify(fleet)}))`,context));

// The desktop robot's copy, with the names its own page gives it: the same file, the same list
const ROBOT=process.env.ROBOT_UI?pathToFileURL(process.env.ROBOT_UI+'/'):new URL('../desktop/ui/',import.meta.url);
const robot=existsSync(new URL('list.js',ROBOT))&&vm.createContext({window:{}});
if(robot){const copy=await readFile(new URL('for-you.js',ROBOT),'utf8');
 assert.equal(copy,rules,'desktop/ui/for-you.js is dashboard/todos-for-you.js as it is: copy it again');
 vm.runInContext(await readFile(new URL('list.js',ROBOT),'utf8'),robot);vm.runInContext(copy,robot)}
const robots=(status,fleet)=>JSON.parse(vm.runInContext(`(()=>{const box=new window.ForYou();box.take({status:${JSON.stringify(status)},fleet:${JSON.stringify(fleet)}});return JSON.stringify(box.list().map(x=>x.title))})()`,robot));
const robotKnows=()=>JSON.parse(vm.runInContext('JSON.stringify({TODO,SENDS})',robot));

const dashboard=await dashboardPage();
let status=base();
const server=createServer(async(req,res)=>{for await(const _ of req);const url=new URL(req.url,'http://fixture.invalid');res.setHeader('Content-Type','application/json');
 if(url.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(dashboard);return}
 if(url.pathname==='/api/status'){res.end(JSON.stringify(status));return}
 if(url.pathname==='/api/fleet'){res.end(JSON.stringify(fleet()));return}
 res.statusCode=url.pathname.startsWith('/brand/')?404:200;res.end('{}')});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;const errors=[];
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 for(const [name,extra] of Object.entries(CASES)){
  status={...base(),...JSON.parse(JSON.stringify(extra,(k,v)=>v===undefined?null:v))};for(const k of Object.keys(status))if(status[k]===null)delete status[k];
  const expected=await alone(structuredClone(status),fleet());
  if(robot)assert.deepEqual(robots(structuredClone(status),fleet()),expected,name+', in the robot');
  const page=await browser.newPage({viewport:{width:1440,height:900}});
  await page.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
  page.on('pageerror',e=>errors.push(name+': '+e.message));page.on('console',m=>{if(m.type()==='error'&&!/Failed to load resource|MIME type|Manifest/.test(m.text()))errors.push(name+': '+m.text())});
  await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>Array.isArray(state.suggestions)&&!shownCached);
  if(status.fleet.on)await page.waitForFunction(()=>!!fleetData);
  // The articles under the heading, up to the next group: what the dashboard draws, not what its rules say
  const drawn=()=>page.evaluate(()=>{const head=document.querySelector('#section-foryou');if(!head)return {count:0,titles:[]};const titles=[];
   for(let el=head.nextElementSibling;el&&!el.matches('.section-head,details');el=el.nextElementSibling)if(el.matches('article')&&!el.id.startsWith('fu-sending'))titles.push(el.querySelector('h3')?.textContent.replace(/\s+/g,' ').trim());
   return {count:+head.querySelector('.count').textContent,titles}});
  let got;for(const end=Date.now()+20000;Date.now()<end;await new Promise(r=>setTimeout(r,100))){got=await drawn();if(got.titles.length===got.count&&(got.count===expected.length||!expected.length))break}
  assert.deepEqual(errors,[],name);assert.deepEqual(got.titles,expected,name);assert.equal(got.count,expected.length,name+': the count');
  if(name==='everything'){assert.ok(expected.length>20);
   if(robot){const own=await page.evaluate(()=>({TODO:{CLOSED:TODO.CLOSED,OPEN_NOT_SNOOZED:TODO.OPEN_NOT_SNOOZED},SENDS})),sorted=x=>JSON.parse(JSON.stringify(x),(k,v)=>Array.isArray(v)?[...v].sort():v);
    assert.deepEqual(sorted(robotKnows()),sorted(own),'the robot\'s list.js has the statuses and sends of the Machine')}
   for(const hidden of ['Done','Not needed','Snoozed','Looks done, by its run','Looks done, by a message','Waits on others','Still needed? folded','Older','Follow-up one'])assert.ok(!expected.includes(hidden),hidden);
   assert.deepEqual(expected.filter(x=>/^Same moment/.test(x)),['Same moment, a','Same moment, b','Same moment, c'])}
  if(name==='with Fleet items')assert.equal(expected.filter(x=>/Pat|Robin|Kim/.test(x)).length,6);
  if(name==='the hello leads')assert.equal(expected[0],'Prepared');
  await page.close()}
 console.log('For you by its rules alone is For you as drawn: '+Object.keys(CASES).length+' cases.');
}finally{await browser?.close();server.close()}
