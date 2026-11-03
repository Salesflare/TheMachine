import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtemp,rm,readdir,mkdir,writeFile} from 'node:fs/promises';
import {existsSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';

// The helpers the service runs read and write only paths the service hands them as absolute, already normal paths:
// a relative folder or one with .. in it is refused before anything is read, made or sent.
const root=new URL('..',import.meta.url).pathname,dir=await mkdtemp(join(tmpdir(),'assistant-paths-')),work=join(dir,'work');
// A stand-in OpenClaw: loading it leaves a mark and then fails, so a request that gets past the checks never sends
const fake=join(dir,'openclaw'),mark=join(dir,'loaded');await mkdir(join(fake,'dist','plugin-sdk'),{recursive:true});await mkdir(work);
await writeFile(join(fake,'dist','plugin-sdk','runtime-config-snapshot.js'),`import {writeFileSync} from 'node:fs';writeFileSync(${JSON.stringify(mark)},'1');throw Error('stand-in');`);
const run=(file,input,env={})=>{const r=spawnSync(process.execPath,[join(root,file)],{input:JSON.stringify(input),encoding:'utf8',cwd:work,timeout:30000,
 env:{PATH:process.env.PATH,HOME:work,OPENCLAW_PACKAGE_DIR:fake,...env}});return {code:r.status,out:JSON.parse(r.stdout||'{}')}};
try{
 // change-prompt-run.mjs: the receipt folder comes in the request; only an absolute, normal one is taken
 const prompt=receipt_dir=>({receipt_key:'a'.repeat(64),card_id:'7',text:'Synthetic',receipt_dir,target:'1000001'});
 for(const bad of ['receipts','./receipts',dir+'/x/../../escape',dir+'/../escape',42,null]){
  const r=run('change-prompt-run.mjs',prompt(bad));
  assert.equal(r.code,1,String(bad));
  assert.deepEqual(r.out,{error:'prompt_unconfirmed',definitely_not_sent:true},String(bad));
  assert.ok(!existsSync(mark),'refused before OpenClaw is loaded: '+bad);
 }
 assert.deepEqual(await readdir(work),[],'nothing made for a refused folder');
 // a normal absolute folder gets past the checks (and the stand-in stops it there, unsent)
 assert.deepEqual(run('change-prompt-run.mjs',prompt(join(dir,'receipts'))).out,{error:'prompt_unconfirmed',definitely_not_sent:true});
 assert.ok(existsSync(mark),'an absolute, normal folder is taken');
 assert.ok(!existsSync(join(dir,'..','escape')));
 // chat-history-run.mjs: its state folder and OpenClaw's config come from the environment, and the same rule applies
 const ask={session_key:'agent:main:assistant-review-preparation-'+'0'.repeat(32),limit:10};
 for(const env of [{ASSISTANT_STATE_DIR:'state'},{ASSISTANT_STATE_DIR:dir+'/x/../state'},
   {ASSISTANT_STATE_DIR:dir,OPENCLAW_CONFIG_PATH:'openclaw.json'},{ASSISTANT_STATE_DIR:dir,OPENCLAW_CONFIG_PATH:dir+'/../openclaw.json'}]){
  const r=run('chat-history-run.mjs',ask,env);
  assert.deepEqual(r.out,{error:'invalid_request'},JSON.stringify(env));
 }
 assert.deepEqual(await readdir(work),[],'no device identity written for a refused folder');
 console.log('ok helper paths: relative and .. paths refused before any read or write');
}finally{await rm(dir,{recursive:true,force:true})}
