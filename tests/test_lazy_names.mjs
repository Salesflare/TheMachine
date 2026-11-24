import assert from 'node:assert/strict';
import {execFileSync, spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

// A script of the dashboard uses only the names that are there when it runs: its own, the main script's, and those of a
// part that is in by then, which the code shows (lazy-names.mjs) or dashboard_parts.LAZY_WITH says. The follow-ups'
// review, opened before the Graph's part was in, once read a name of that part and didn't open. A few names in one
// place, read before that part is in, need to be in the main script instead.
if(!process.execArgv.includes('--expose-internals')){
  const run=spawnSync(process.execPath,['--expose-internals',fileURLToPath(import.meta.url)],{stdio:'inherit'});
  process.exit(run.status??1);
}
const {lazyNames}=await import('./lazy-names.mjs');

// What it finds: a use of b's name x, from the main script or from part a
const b='const x=1;function bGo(){}';
const uses=(first,a)=>lazyNames(first,{a,b}).map(u=>(u.from||'main')+'>'+u.part+':'+u.name);
for(const js of ['const go=()=>x','const row=s=>html`<p>${s.on?x:0}</p>`','function f(){if(y)return bGo()}const y=1','const o={x}','let z=x+1','[1].map(v=>v+x)',
  'const go=()=>lazyIn("c")&&x','const go=()=>lazyRun("c",()=>x)','async function f(){x;await lazyPart("b")}','const go=()=>x&&lazyIn("b")','const o={[x]:1}','const go=({k=x})=>k']){
  const name=/bGo/.test(js)?'bGo':'x';
  assert.deepEqual(uses('',js),['a>b:'+name],js);assert.deepEqual(uses(js,''),['main>b:'+name],js);
}
// What it leaves alone
for(const js of ['const go=x=>x','const go=()=>{const x=1;return x}','const o={x:1},v=o.x','const go=()=>lazyRun("b",()=>bGo(x))','const go=()=>lazyPart("b").then(()=>x)',
  'async function f(){await lazyPart("b");return x}','async function f(){const [r]=await Promise.all([1,lazyPart("b")]);return x}','const go=()=>lazyIn("b")?x:0','const on=lazyIn("b");if(on)bGo()',
  'if(typeof x!=="undefined")bGo()','const go=()=>self.bGo&&x','const go=()=>self.bGo?.()','for(const x of [1])x','try{}catch(x){x}','function f({x},[y]){return x+y}','class K{x(){return 1}}','x:for(;;)break x']){
  assert.deepEqual(uses('',js),[],js);assert.deepEqual(uses(js,''),[],js);
}
assert.deepEqual(uses('const x=0','const go=()=>x'),[],'the main script has it too');

// The dashboard
const [page,lazy,withs]=JSON.parse(execFileSync('python3',['-c','import json,dashboard_parts as d;print(json.dumps([*d.assemble_split(),d.LAZY_WITH]))'],
  {cwd:fileURLToPath(new URL('..',import.meta.url)),encoding:'utf8',maxBuffer:1<<27}));
const first=[...page.matchAll(/<script(?![^>]*(?:type="application|src=))[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
assert.ok(first.length&&Object.keys(lazy).length>20);
const found=lazyNames(first,lazy),key=u=>u.from+'>'+u.part,said=new Set(Object.entries(withs).flatMap(([from,parts])=>parts.map(part=>from+'>'+part)));
const open=found.filter(u=>!said.has(key(u))).map(u=>`${u.from?`the part '${u.from}'`:'the main script'} (line ${u.line}) reads ${u.name}, which only the part '${u.part}' has`);
assert.deepEqual(open,[],'read before that part is in, it throws: move the name to the main script, or load the part first (lazyRun, lazyPart, lazyIn)');
assert.deepEqual([...said].filter(x=>!found.some(u=>key(u)===x)),[],'dashboard_parts.LAZY_WITH names a part nothing needs it for any more');
console.log('lazy names ok: '+found.length+' uses of another part, all in LAZY_WITH');
