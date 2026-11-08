// Turn one old OpenClaw job off (routines_app.py routine_old_job), on the owner's tap only: the job stays in OpenClaw,
// off, and can be turned on again there. Nothing else in OpenClaw changes. No credentials here.
import {gatewayRuntime} from './openclaw-root.mjs';
const {callGatewayFromCli}=await gatewayRuntime();
let input=''; for await (const chunk of process.stdin) input+=chunk;
const request=JSON.parse(input);
if (!/^[A-Za-z0-9-]{8,64}$/.test(request.id || '')) throw new Error('Invalid request');
try {
  await callGatewayFromCli('cron.update',{timeout:'15000'},{id:request.id,patch:{enabled:false}},{scopes:['operator.admin','operator.write']});
  process.stdout.write(JSON.stringify({status:'off'}));
} catch {
  process.stdout.write(JSON.stringify({status:'unavailable'}));
}
