// The X reader and sender on made-up pages of X's two web apps: the new one (its token in the page), the one before it
// (its token in the main script) and a page with neither. No browser or network.
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=dirname(dirname(fileURLToPath(import.meta.url)));
const code=JSON.parse(execFileSync('python3',['-c',`import importlib.util,json,sys
s=importlib.util.spec_from_file_location('test_x',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(json.dumps({'read':m.JS,'send':m.SEND_JS,'compose':m.COMPOSE_JS}))`,resolve(root,'integrations/x_inbox.py')],{encoding:'utf8'}));
const token=c=>'A'.repeat(21)+c.repeat(20);
const OLD='<link href="https://abs.twimg.com/responsive-web/client-web/icon-ios.1.png"><script src="https://abs.twimg.com/responsive-web/client-web/main.abc.js"></script>';
// What the new one looks like: its own static files, the headers of its first requests, and posts (their quotes escaped)
const post=String.raw`"text":"say \"Authorization\":\"Bearer ${token('p')}\""`;
const NEW=`<link rel="icon" href="https://abs.twimg.com/responsive-web/client-web/icon-ios.1.png"><link rel="stylesheet" href="https://abs.twimg.com/x-web/x-web/assets/styles-1.css"><script>self.s={${post},"headers":{"Authorization":"Bearer ${token('n')}","x":"1"}}</script>`;
const main='e.exports={token:"'+token('o')+'"},{queryId:"q1",operationName:"TweetResultByRestId",operationType:"query",metadata:{featureSwitches:["a"],fieldToggles:["b"]}}';
globalThis.location={host:'x.com'};
globalThis.document={readyState:'complete',cookie:'ct0=synthetic; twid=%22u%3D1%22',querySelector:()=>null};
let page,asked=[];
globalThis.fetch=async(url,opts={})=>{
 let json={},text='';
 if(url==='/')text=page;
 else if(url.endsWith('/main.abc.js'))text=main;
 else{asked.push([url.split('?')[0],opts.headers.authorization,opts.method||'GET']);
  if(url.includes('account/multi/list'))json={users:[{user_id:'1',screen_name:'Owner',name:'Owner'}]};
  else if(url.includes('notifications/mentions'))json={globalObjects:{tweets:{},users:{}},timeline:{}};
  else if(url.includes('dm/inbox_initial_state'))json={inbox_initial_state:{entries:[],users:{},conversations:{},cursor:'dm'}};
  else if(url.includes('dm/conversation/'))json={conversation_timeline:{users:{2:{name:'Ada',screen_name:'ada'}},conversations:{'1-2':{participants:[{user_id:'1'},{user_id:'2'}]}}}};
  else if(url.includes('/graphql/'))json={data:{tweetResult:{result:{__typename:'Tweet',rest_id:'5',legacy:{user_id_str:'2',full_text:'Hello?'}}}}};
  else throw Error('Unexpected synthetic request: '+url)}
 return {ok:true,text:async()=>text,json:async()=>json};
};
const run=(which,params)=>{asked=[];return eval('('+code[which].replace('__PARAMS__',JSON.stringify(params))+')')()};
const sync={mode:'sync',handle:'Owner',primary:'Owner',state:{},since:0};

for(const [name,html,used] of [['new',NEW,token('n')],['old',OLD,token('o')]]){
 page=html;
 const r=await run('read',sync);
 assert.equal(r.error,undefined,name);
 assert.equal(r.state.dm_cursor,'dm',name);
 assert.ok(asked.length>=3,name);
 assert.deepEqual([...new Set(asked.map(a=>a[1]+' '+a[2]))],['Bearer '+used+' GET'],name); // the app's own token; only reads
}
// Neither app's token: said as such before any request to X's API, and a post that quotes one is never taken for it.
for(page of ['<title>Something else</title>',`<script>self.s={${post}}</script>`]){
 const r=await run('read',sync);
 assert.equal(r.detail,'web client token not found');
 assert.equal(asked.length,0);
}

// Sending: a DM's conversation and, with the old app, the post a reply is to are found. With the new app a reply stops
// there, before anything is written.
const resolveDm={mode:'resolve',handle:'Owner',primary:'Owner',conversation:'1-2',reply_to:'',switch:true},resolveReply={...resolveDm,conversation:'',reply_to:'5',switch:false};
page=NEW;
assert.equal((await run('send',resolveDm)).conversation.with,'Ada');
assert.equal((await run('send',resolveReply)).error,'new-client');
assert.ok(asked.every(a=>a[2]==='GET'));
page=OLD;
assert.equal((await run('send',resolveReply)).reply_to.text,'Hello?');
// The composer of the new app, when it comes up right after the old one answered: nothing is clicked.
let clicked=false;
globalThis.document.querySelector=s=>/x-web/.test(s)?{}:{click(){clicked=true}};
assert.equal((await run('compose',{account_id:'1',reply_to:'5',author:'ada',text:'Hi',send:true})).error,'new-client');
assert.equal(clicked,false);
console.log('X web client: both apps read with their own token, none found is said, replies wait on the old app, DMs go on both.');
