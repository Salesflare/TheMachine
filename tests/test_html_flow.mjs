import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {readFile, readdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dashboardPage} from './dashboard-page.mjs';

// No html`` result of the dashboard is used as plain text, where its markup would show on screen (html-flow.mjs): a
// Family plan once read '<span class="muted">Waiting: Alex</span>', joined with ' · '. It parses with Node's own parser.
if(!process.execArgv.includes('--expose-internals')){
  const run=spawnSync(process.execPath,['--expose-internals',fileURLToPath(import.meta.url)],{stdio:'inherit'});
  process.exit(run.status??1);
}
const {htmlFlow}=await import('./html-flow.mjs');
const why=js=>htmlFlow(js).map(x=>x.why);
const PLAIN='markup as a plain string in html``',ATTR='markup in an attribute';

// What it finds
for(const [js,want] of [
  ["const a=p=>html`<li>${[p.yes?t('In'):'',p.w.length?html`<i>${p.w}</i>`:''].filter(Boolean).join(' · ')}</li>`",PLAIN],  // the Family plan
  ["const a=x=>html`<b>${html`<i>${x}</i>`+' · '+x}</b>`",PLAIN],
  ["const a=x=>html`<b>${`${html`<i>${x}</i>`} · ${x}`}</b>`",PLAIN],
  ["const a=x=>html`<b>${String(html`<i>${x}</i>`)}</b>`",PLAIN],
  ["const a=x=>html`<b>${x.map(y=>html`<i>${y}</i>`).join('')}</b>`",PLAIN],
  ["function row(x){const s=[];s.push(html`<i>${x}</i>`);const line=s.join(', ');return html`<b>${line}</b>`}",PLAIN],
  ["const it=x=>html`<i>${x}</i>`;function row(x){let out='';for(const y of x)out+=it(y);return html`<b>${out}</b>`}",PLAIN],
  ["const row=parts=>html`<b>${parts.join(' ')}</b>`;row(['a',html`<i>b</i>`])",PLAIN],
  ["const a=x=>{const o={sub:html`<i>${x}</i>`};return o};const b=x=>html`<b>${a(x).sub+'!'}</b>`",PLAIN],
  ["const a=x=>html`<b>${esc(x)}</b>`",PLAIN],  // escaped twice
  ["const a=x=>html`<b>${'<i>'+x+'</i>'}</b>`",PLAIN],
  ["const a=x=>html`<b>${t('Hi {}',html`<i>${x}</i>`)}</b>`",'markup passed to t()'],
  ["const a=x=>toast(html`<i>${x}</i>`)",'markup passed to toast()'],
  ["const a=x=>make('p',{},html`<i>${x}</i>`)",'markup passed to make()'],
  ["const a=(e,x)=>{e.textContent=html`<i>${x}</i>`}",'markup set as textContent'],
  ["const a=(e,x)=>e.append(html`<i>${x}</i>`)",'markup passed to append()'],
  ["const when=x=>htmlT('Last {}',html`<time>${x}</time>`);const a=x=>html`<b title=\"${when(x)}\">${x}</b>`",ATTR],
])assert.ok(why(js).includes(want),js+'\n'+why(js));

// What it leaves alone: pieces that stay html``, text that stays text, class names, and what isn't put in html``
for(const js of [
  "const a=p=>html`<li>${[p.yes?t('In'):'',html`<i>${p.w}</i>`].filter(Boolean).map((x,i)=>html`${i?' · ':''}${x}`)}</li>`",
  "const a=x=>html`<b>${x.map(y=>html`<i>${y}</i>`)}</b>`",
  "const a=x=>html`<b class=\"row${x.on?html` on`:''}\" title=\"${[x.a,x.b].join(' · ')}\"${x.off?html` disabled`:''}>${x.name+' · '+t('Hi {}',x.y)}</b>`",
  "const a=x=>htmlT('Last {}',html`<time>${x}</time>`)",
  "const a=(e,x)=>{e.innerHTML=`<b>${esc(x)}${html`<i>${x}</i>`}</b>`}",
  "const a=(e,h)=>{const m=html`<i>${h}</i>`;if(e.was!==String(m)){setHTML(e,m);e.was=String(m)}}",
  "const a=x=>html`<b>${raw('<i></i>')}</b>`",
])assert.deepEqual(why(js),[],js);

// The page: each script of it, with the file of each line
const page=await dashboardPage(),dir=new URL('../dashboard/',import.meta.url),parts=[];
for(const name of (await readdir(dir)).filter(f=>f.endsWith('.js')))parts.push([name,(await readFile(new URL(name,dir),'utf8')).replace(/\r\n?/g,'\n')]);
let lines=0;
for(const [,attrs,js] of page.matchAll(/<script(\s[^>]*)?>([\s\S]*?)<\/script>/g)){
  if(/application\/json/.test(attrs||''))continue;
  const where=new Map();
  for(const [name,text] of parts){const at=js.indexOf(text.trimEnd());if(at<0)continue;
    const first=js.slice(0,at).split('\n').length;text.split('\n').forEach((_,i)=>where.set(first+i,[name,i+1]))}
  const found=htmlFlow(js,line=>where.get(line)?.[0]||'');
  assert.deepEqual(found.map(x=>`dashboard/${(where.get(x.line)||['dashboard.html',x.line]).join(':')} ${x.why}: ${x.code}`),[]);
  lines+=where.size;
}
assert.ok(lines>5000,'the parts were found in the page: '+lines);
