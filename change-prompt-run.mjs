// One short-lived sender using the existing OpenClaw account, cache and transport.
// SQLite owns admission; a private receipt survives a lost stdout/binding response.
import {open,rename,mkdir} from 'node:fs/promises';
import {join,isAbsolute} from 'node:path';
import {OPENCLAW} from './openclaw-root.mjs';
let sending=false;
// The receipt folder is the service's own: an absolute, already normal path (no .. or relative parts), or no send.
const folderOk=d=>typeof d==='string'&&isAbsolute(d)&&!d.split(/[\\/]/).slice(1).some(x=>x===''||x==='.'||x==='..');
try{
 let input='';for await(const chunk of process.stdin)input+=chunk;
 const request=JSON.parse(input);
 if(!/^[a-f0-9]{64}$/.test(request.receipt_key)||!/^\d+$/.test(request.card_id)||typeof request.text!=='string'||!folderOk(request.receipt_dir)||!/^-?\d+$/.test(String(request.target||'')))throw Error('Invalid prompt request');
 // Loaded here, not statically: after an OpenClaw/Node update a missing module must be
 // reported as "not sent" (the service then sends its plain prompt), not as a silent crash.
 const [{getRuntimeConfig},{sendChangePrompt}]=await Promise.all([
  import(`${OPENCLAW}/dist/plugin-sdk/runtime-config-snapshot.js`),import('./openclaw-plugin/change-prompt.ts')]);
 const cfg=getRuntimeConfig();
 sending=true;  // sendChangePrompt classifies its own failures from here on
 const id=await sendChangePrompt(cfg,request.card_id,request.text,async messageId=>{
  const folder=request.receipt_dir;
  await mkdir(folder,{recursive:true,mode:0o700});
  const dest=join(folder,request.receipt_key+'.json'),temp=dest+'.tmp';
  const file=await open(temp,'w',0o600);
  try{await file.writeFile(JSON.stringify({messageId}));await file.sync();}finally{await file.close();}
  await rename(temp,dest);
 },String(request.target),process.env.ASSISTANT_TELEGRAM_ACCOUNT||'default');
 process.stdout.write(JSON.stringify({messageId:id}));
}catch(error){
 process.stdout.write(JSON.stringify({error:'prompt_unconfirmed',
  definitely_not_sent:!sending||error?.definitelyNotSent===true}));
 process.exitCode=1;
}
