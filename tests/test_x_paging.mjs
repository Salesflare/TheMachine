// Execute the actual X reader with synthetic web-client replies; no browser or network.
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=dirname(dirname(fileURLToPath(import.meta.url)));
const js=execFileSync('python3',['-c',`import importlib.util,sys
s=importlib.util.spec_from_file_location('test_x',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(m.JS)`,resolve(root,'integrations/x_inbox.py')],{encoding:'utf8'});
globalThis.location={host:'x.com'};
globalThis.document={readyState:'complete',cookie:'ct0=synthetic; twid=%22u%3D1%22'};
const top=1978000000000000000n;
const mention=i=>({id_str:String(top-BigInt(i)),created_at:'Fri Oct 16 12:00:00 +0000 2026',
  user_id_str:'2',full_text:'A synthetic mention',entities:{user_mentions:[{id_str:'1'}]}});
let tweets=[],calls=[],failDm=false;
globalThis.fetch=async url=>{
  let json={},text='';
  if(url==='/')text='<script src="https://abs.twimg.com/responsive-web/client-web/main.abc.js"></script>';
  else if(url.startsWith('https://abs.twimg.com'))text='"'+'A'.repeat(32)+'"';
  else if(url.includes('account/multi/list'))json={users:[{user_id:'1',screen_name:'Owner',name:'Owner'}]};
  else if(url.includes('notifications/mentions')){
    const cursor=new URL(url,'https://x.com').searchParams.get('cursor');calls.push(cursor);
    const start=cursor?tweets.findIndex(t=>t.id_str===cursor)+1:0;
    const data=tweets.slice(start,start+40),last=data.at(-1)?.id_str;
    json={globalObjects:{tweets:Object.fromEntries(data.map(t=>[t.id_str,t])),users:{'2':{screen_name:'sender'}}},
      timeline:last?{cursor:{value:last,cursorType:'Bottom'}}:{}};
  }else if(url.includes('dm/inbox_initial_state')){
    if(failDm)throw Error('synthetic read failure');
    json={inbox_initial_state:{entries:[],users:{},conversations:{},cursor:'dm'}};
  }else if(url.includes('dm/user_updates'))json={user_events:{entries:[],users:{},conversations:{},cursor:'dm'}};
  else throw Error('Unexpected synthetic request: '+url);
  return {ok:true,text:async()=>text,json:async()=>json};
};
const run=(state={},since=0)=>eval('('+js.replace('__PARAMS__',JSON.stringify({mode:'sync',handle:'Owner',primary:'Owner',state,since}))+')')();

// A full four-page read saves a bottom cursor, not a completed top watermark.
tweets=Array.from({length:180},(_,i)=>mention(i));
const first=await run({mention_since_id:'1'});
assert.equal(first.mentions.length,160);
assert.equal(first.state.mention_since_id,'1');
assert.equal(first.state.mention_catchup.cursor,tweets[159].id_str);
const saved=JSON.parse(JSON.stringify(first.state)); // the persisted checkpoint survives restart
const newer={...mention(-1),created_at:'Fri Oct 16 12:01:00 +0000 2026'};
tweets.unshift(newer);
const second=await run(saved,Date.parse('2026-10-17T12:00:00Z')); // resumes the original time window
assert.equal(second.mentions.length,20);
assert.equal(second.state.mention_catchup,undefined);
assert.equal(second.state.mention_since_id,String(top));
assert.equal(calls[4],first.state.mention_catchup.cursor);
assert.equal(new Set([...first.mentions,...second.mentions].map(t=>t.id)).size,180);
const third=await run(second.state);
assert.deepEqual(third.mentions.map(t=>t.id),[newer.id_str]);
const fourth=await run(third.state);
assert.equal(fourth.mentions.length,0);

// A failing later component makes the whole source read unsuccessful; the caller retains
// its old checkpoint. Replaying from that checkpoint still returns the same source IDs.
failDm=true;tweets=Array.from({length:60},(_,i)=>mention(i));calls=[];
const failed=await run();
assert.equal(failed.error,'query-failed');
failDm=false;
const retry=await run();
assert.deepEqual(retry.mentions.map(t=>t.id),failed.mentions.map(t=>t.id));
assert.equal(retry.error,undefined);
console.log('X paging: bounded catch-up, persisted cursor, frozen time floor, new arrivals and failed-read replay passed.');
