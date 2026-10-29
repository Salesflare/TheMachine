import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
// A queued to-do that has to wait says why and roughly when (s.preparation_hold from preparation_step), instead of
// "I'll start shortly." for minutes (2026-10-29: one sat there 8 minutes). Every line is in all seven catalogs.
const html=await readFile(new URL('../dashboard.html',import.meta.url),'utf8');
const fmt=html.slice(html.indexOf("let DL='en-US'"),html.indexOf('\n',html.indexOf('const fmtDHM=')));
const when=html.slice(html.indexOf('const pauseWhen='),html.indexOf('\n',html.indexOf('const pauseWhen=')));
const block=html.slice(html.indexOf('function holdNote('),html.indexOf('function preparationNote('));
const used=[];
const t=(k,...a)=>{used.push(k);let i=0;return k.replace(/\{\}/g,()=>a[i++])};
const holdNote=new Function('t',fmt+'\n'+when+'\n'+block+';return holdNote')(t);
assert.equal(holdNote(null),'');  // no reason: it starts within seconds, the card keeps "I'll start shortly."
assert.equal(holdNote({why:'after'}),'Starts after the current one.');
assert.equal(holdNote({why:'busy'}),'Starts when one of the running to-dos finishes.');
assert.equal(holdNote({why:'others'}),'Starts after the other to-dos.');
const soon=new Date();soon.setMinutes(soon.getMinutes()+20);
const at=Math.floor(soon/1000),day=soon.toDateString()===new Date().toDateString();
assert.match(holdNote({why:'limit',until:at}),day?/^Waiting for the usage limit to reset\. Starts around \d{1,2}:\d{2}( [AP]M)?\.$/:/^Waiting for the usage limit to reset\. Starts around /);
assert.equal(holdNote({why:'limit',until:null}),'Waiting for the usage limit to reset.');
assert.match(holdNote({why:'budget',until:at}),/^Saving usage for now\. Starts around /);
assert.equal(holdNote({why:'budget'}),'Saving usage for now. Starts when there’s room.');
assert.match(holdNote({why:'retry',until:at}),/^Trying again around /);
assert.equal(holdNote({why:'retry',until:Math.floor(Date.now()/1000)-60}),'');  // past: back to "I'll start shortly."
for(const lang of ['en','nl','fr','de','es','it','pt-BR']){
 const cat=JSON.parse(await readFile(new URL(`../i18n/${lang}.json`,import.meta.url),'utf8'));
 for(const k of new Set(used)){assert.ok(cat[k],`${lang}: ${k}`);assert.equal((cat[k].match(/\{\}/g)||[]).length,(k.match(/\{\}/g)||[]).length,`${lang}: ${k}`);assert.ok(!cat[k].includes('—'),`${lang}: no em dash`)}
}
// The queued note uses it first
assert.match(html,/if\(s\.preparation_status==='queued'\)return `<p class="note">\$\{esc\(holdNote\(s\.preparation_hold\)\|\|/);
console.log('preparation wait ok');
