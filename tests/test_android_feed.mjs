import assert from 'node:assert/strict';
import { readFile as readSource } from 'node:fs/promises';
// The plugin imports the OpenClaw SDK by package name (resolved inside the Gateway); here the
// queue and config reads are replaced by fixtures before loading the module.
let feedSource=await readSource(new URL('../openclaw-plugin/android-feed.ts',import.meta.url),'utf8');
feedSource=feedSource.replace(/import \* as systemEvents from '[^']+';/,"const systemEvents=globalThis.__feedEvents;");
assert.ok(feedSource.includes('globalThis.__feedEvents'));
// The queue: peek, and (on Gateways that have it) removal of chosen events by id, as the SDK does it.
globalThis.__feedEvents={peekSystemEventEntries:()=>globalThis.__feedTest.entries,
  consumeSelectedSystemEventEntries:(key,chosen)=>{const t=globalThis.__feedTest;t.consumed.push({key,ids:chosen.map(e=>e.id)});
    t.onConsume?.(chosen);t.entries=t.entries.filter(e=>!chosen.some(c=>c.id===e.id));}};
feedSource=feedSource.replace("import { readFile } from 'node:fs/promises';", "const readFile=async()=>JSON.stringify(globalThis.__feedTest.config);");
const feedModule=await import('data:text/javascript;base64,'+Buffer.from((await import('node:module')).stripTypeScriptTypes(feedSource)).toString('base64'));
const {notificationEnvelope}=feedModule;
const node='0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef';
const event=(text)=>({id:'one',ts:100,contextKey:'notification:key',text});
let parsed=notificationEnvelope(event(`Notification posted (node=${node} key=secret-key package=com.example): Sender - Hi`),node);
assert.equal(parsed.change,'posted');assert.equal(parsed.text,'Sender - Hi');assert.equal(parsed.package_name,'com.example');assert.ok(!JSON.stringify(parsed).includes('secret-key'));
assert.equal(notificationEnvelope(event('Notification posted (node=another key=k package=com.example): Hi'),node),null);
assert.equal(notificationEnvelope(event(`Notification posted (node=${node} key=k package=ai.openclaw.app): Hi`),node),null);
parsed=notificationEnvelope(event(`Notification removed (node=${node} key=k package=com.example)`),node);assert.equal(parsed.change,'removed');assert.equal(parsed.text,'');
parsed=notificationEnvelope(event(`Notification posted (node=${node} key=k package=sms): Verification code 123456`),node);assert.ok(!JSON.stringify(parsed).includes('123456'));
assert.equal(notificationEnvelope({id:'x',ts:100,contextKey:'other',text:'Hi'},node),null);
console.log('Android existing-feed parsing, exact device/account, removal, code omission and private key hashing passed.');

// Service-level proof with a real temporary SQLite DB and only mocked upstream
// queue/config access. Restart must not replay a processed removal-only event.
const {readFile, mkdtemp, rm} = await import('node:fs/promises');
const {tmpdir} = await import('node:os');
const {join} = await import('node:path');
const {DatabaseSync} = await import('node:sqlite');
const directory=await mkdtemp(join(tmpdir(),'android-feed-test-'));
try {
  const dbPath=join(directory,'events.sqlite');
  const db=new DatabaseSync(dbPath);
  db.exec('CREATE TABLE android_inbox(id TEXT PRIMARY KEY,payload TEXT,received_at TEXT); CREATE TABLE android_feed_health(id INTEGER PRIMARY KEY,last_checked TEXT,last_recorded TEXT,error TEXT); CREATE TABLE android_receipts(id TEXT PRIMARY KEY,account_id TEXT,processed_at TEXT)');
  globalThis.__feedTest={consumed:[],entries:[event(`Notification removed (node=${node} key=k package=com.example)`)],config:{database:dbPath,accounts:[{id:'personal-android',transport:'openclaw-feed',node_id:node}]}};
  const {registerAndroidFeed}=feedModule;
  const start=async()=>{
    let service; const hooks=[];
    registerAndroidFeed({registerService:s=>service=s,on:(name,fn)=>hooks.push([name,fn])});
    service.start({serviceHealth:{clearFailure(){},reportFailure(){}}});
    await new Promise(resolve=>setTimeout(resolve,15));service.stop();
    assert.ok(hooks.some(([name])=>name==='before_prompt_build'));
  };
  await start();assert.equal(db.prepare('SELECT count(*) n FROM android_inbox').get().n,1);
  db.exec("DELETE FROM android_inbox; INSERT INTO android_receipts VALUES('one','personal-android','2026-10-10')");
  await start();assert.equal(db.prepare('SELECT count(*) n FROM android_inbox').get().n,0);
  assert.equal(db.prepare('SELECT error FROM android_feed_health').get().error,null);
  // With the app's message key next to the database, the waiting text is sealed, and the app opens it.
  const {writeFile}=await import('node:fs/promises');
  const {execFileSync}=await import('node:child_process');
  const key=Buffer.alloc(32,7).toString('base64');
  await writeFile(join(directory,'message-content.key'),key+'\n',{mode:0o600});
  db.exec('DELETE FROM android_receipts');
  globalThis.__feedTest.entries=[{...event(`Notification posted (node=${node} key=k2 package=com.example): Zanzibar quill contract ready`),id:'two'}];
  await start();
  const payload=JSON.parse(db.prepare("SELECT payload FROM android_inbox WHERE id='two'").get().payload);
  assert.ok(payload.text.startsWith('mci1:'));assert.ok(!JSON.stringify(payload).includes('Zanzibar'));
  assert.equal(payload.notification_key_hash.length,64);
  const opened=execFileSync('python3',['-c','import base64,sys,message_seal as m;print(m.Sealer(base64.b64decode(sys.argv[1])).open_inbox(sys.argv[2]),end="")',key,payload.text],
    {cwd:new URL('..',import.meta.url),encoding:'utf8'});
  assert.equal(opened,'Zanzibar quill contract ready');
  globalThis.__feedTest.config={...globalThis.__feedTest.config,message_protection:false};
  globalThis.__feedTest.entries=[{...event(`Notification posted (node=${node} key=k3 package=com.example): Plain on purpose`),id:'three'}];
  await start();
  assert.equal(JSON.parse(db.prepare("SELECT payload FROM android_inbox WHERE id='three'").get().payload).text,'Plain on purpose');
  // Few events waiting: the feed only peeks, so the main chat still sees them all.
  assert.deepEqual(globalThis.__feedTest.consumed,[]);

  // A full queue drops new phone notifications, and with the heartbeat off only an owner's message empties it. Once more
  // than ROOM events wait, the oldest saved phone notifications leave it until ROOM are left; other events always stay.
  const {ROOM,savedToRelease}=feedModule;
  db.exec('DELETE FROM android_inbox; DELETE FROM android_receipts');
  const mine=Array.from({length:14},(_,i)=>({id:'n'+i,ts:1000+i,contextKey:'notification:k'+i,text:`Notification posted (node=${node} key=k${i} package=com.example): Hello ${i}`}));
  const others=[{id:'exec',ts:1,contextKey:'exec:1',text:'Exec finished'},{id:'cron',ts:2,contextKey:null,text:'A reminder from another plugin'},
    {id:'elsewhere',ts:3,contextKey:'notification:x',text:'Notification posted (node=another key=x package=com.example): Not this phone'},
    {id:'app',ts:4,contextKey:'notification:y',text:`Notification posted (node=${node} key=y package=ai.openclaw.app): Not saved`}];
  globalThis.__feedTest.entries=[...others.slice(0,2),...mine.slice().reverse(),...others.slice(2)];
  globalThis.__feedTest.onConsume=chosen=>{for(const {id} of chosen)assert.ok(db.prepare('SELECT 1 FROM android_inbox WHERE id=?').get(id),'saved before it leaves the queue: '+id);};
  await start();
  assert.equal(db.prepare('SELECT count(*) n FROM android_inbox').get().n,14);
  assert.deepEqual(globalThis.__feedTest.consumed,[{key:'agent:main:main',ids:['n0','n1','n2','n3','n4','n5','n6','n7']}]);
  assert.equal(globalThis.__feedTest.entries.length,ROOM);
  for(const {id} of others)assert.ok(globalThis.__feedTest.entries.some(e=>e.id===id),id);
  // Already at ROOM: nothing more leaves. And nothing unsaved ever does, whatever its text says.
  globalThis.__feedTest.consumed=[];await start();assert.deepEqual(globalThis.__feedTest.consumed,[]);
  assert.deepEqual(savedToRelease([...others,...mine],new Set(),ROOM),[]);
  assert.deepEqual(savedToRelease(mine.slice(0,ROOM),new Set(mine.map(e=>e.id)),ROOM),[]);
  // An older Gateway without targeted removal: the feed still saves and only peeks.
  const consume=globalThis.__feedEvents.consumeSelectedSystemEventEntries;delete globalThis.__feedEvents.consumeSelectedSystemEventEntries;
  try {
    globalThis.__feedTest.entries=[...mine.map(e=>({...e,id:'old-'+e.id})),...others];
    await start();assert.equal(globalThis.__feedTest.entries.length,18);
    assert.ok(db.prepare("SELECT 1 FROM android_inbox WHERE id='old-n13'").get());
  } finally {globalThis.__feedEvents.consumeSelectedSystemEventEntries=consume;}
  db.close();
  console.log('Android bridge restart replay protection, scoped prompt hook and sealed waiting text passed.');
} finally {delete globalThis.__feedTest;delete globalThis.__feedEvents;await rm(directory,{recursive:true,force:true});}
