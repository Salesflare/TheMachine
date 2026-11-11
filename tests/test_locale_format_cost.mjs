import assert from 'node:assert/strict';
import {dashboardPage} from './dashboard-page.mjs';
// Dates and times on the dashboard come from kept formatters (shell-core.js localeFmt): the same text as the browser's
// toLocaleDateString and toLocaleTimeString, without making a new formatter for every stamp (a list redraw stamps
// hundreds of times, and a new formatter costs a fraction of a millisecond each: some 400 ms per redraw on a busy list).
const html=await dashboardPage();
const fmt=html.slice(html.indexOf("let DL='en-US'"),html.indexOf('\n',html.indexOf('const fmtDHM=')));
let made=0;
class CountedFormat extends Intl.DateTimeFormat{constructor(...a){super(...a);made++}}
const fake={...Intl,DateTimeFormat:CountedFormat};
const {localeDate,localeTime,fmtHM,fmtDHM,applyLocale}=new Function('Intl',fmt+'\n;return {localeDate,localeTime,fmtHM,fmtDHM,applyLocale}')(fake);

const options=[undefined,{},{weekday:'short'},{month:'short',day:'numeric'},{hour:'2-digit'},{month:'long',year:'numeric'},
  {hour:'2-digit',minute:'2-digit',hourCycle:'h23'},{hour:'numeric',minute:'2-digit',hour12:true},{timeZone:'UTC'},{weekday:'long',hour:'numeric'}];
for(const loc of [undefined,'en-US','en-GB','nl-BE','de-DE','fr-FR'])for(const o of options)for(const v of ['2026-11-07T23:46:00Z',0,1793900000000,'not a date']){
  assert.equal(localeDate(v,loc,o),new Date(v).toLocaleDateString(loc,o),`date ${loc} ${JSON.stringify(o)} ${v}`);
  assert.equal(localeTime(v,loc,o),new Date(v).toLocaleTimeString(loc,o),`time ${loc} ${JSON.stringify(o)} ${v}`);
}
assert.equal(localeDate('2026-11-07',undefined,{dateStyle:'medium'}),new Date('2026-11-07').toLocaleDateString(undefined,{dateStyle:'medium'}));

applyLocale({date_locale:'en-GB',hour12:false});
made=0;
for(let i=0;i<2000;i++){fmtHM(Date.UTC(2026,10,7,i%24,i%60));fmtDHM(Date.UTC(2026,10,1+i%28),{month:'short',day:'numeric',year:'numeric'})}
assert.ok(made<=3,`2000 stamps made ${made} formatters, not one per stamp`);
assert.ok(!/\.toLocale(Date|Time)?String\(/.test(fmt),'the shared helpers never make a formatter per call');
// nor does the rest of the page: a date or time is stamped with localeDate or localeTime (one render() stamped 143)
const perCall=[...html.matchAll(/\.toLocale(Date|Time)String\(/g)].map(m=>html.slice(Math.max(0,m.index-60),m.index+30));
assert.deepEqual(perCall,[],'use localeDate(d,DL,{...}) or localeTime(d,DL,{...}) instead');
// The saving is the formatter count above, checked by count, not a stopwatch: a wall-clock ratio fails on a busy runner.
console.log('locale format cost ok');
