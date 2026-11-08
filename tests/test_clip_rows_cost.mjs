import assert from 'node:assert/strict';
import {dashboardPage} from './dashboard-page.mjs';
// A clipped list (Learning's Decisions, Connections' Deliveries, the checks) draws only the rows it shows: each redraw
// drew every row and kept three (396 deliveries and 100 decisions: some 3,700 elements thrown away per render()).
const html=await dashboardPage();
const line=start=>{const i=html.indexOf(start);assert.ok(i>=0,start);return html.slice(i,html.indexOf('\n',i))};
const code=line('const clipRows=')+'\n'+line('const clipNodes=');
const {clipRows,clipNodes,listShown}=new Function('make',`const listShown={};${code};return {clipRows,clipNodes,listShown}`)(
  (tag,attrs,...kids)=>({tag,attrs,kids}));
let drawn=0;
const rows=Array.from({length:400},(_,i)=>({id:i})),draw=d=>{drawn++;return {row:d.id}};
const out=clipNodes('deliveries',clipRows(rows,draw),()=>['none']);
assert.equal(drawn,3,'only the shown rows are drawn');
assert.deepEqual(out.slice(0,3),[{row:0},{row:1},{row:2}]);
assert.equal(out[3].attrs['data-more'],'deliveries');  // and "Show 10 more" still counts them all
assert.match(out[3].kids[0],/Show 10 more/);
listShown.deliveries=13;drawn=0;
assert.equal(clipNodes('deliveries',clipRows(rows,draw),()=>['none']).length,14);
assert.equal(drawn,13);
assert.deepEqual(clipNodes('x',clipRows([],draw),()=>['none']),['none']);
assert.deepEqual(clipNodes('y',['a','b','c','d'],()=>['none'],2).slice(0,2),['a','b']);  // drawn rows, as before
// every list on the page hands its rows to clipNodes undrawn
const drawnFirst=[...html.matchAll(/clipNodes\('([\w-]+)',(?!clipRows\()/g)].map(m=>m[1]);
assert.deepEqual(drawnFirst,[],'pass clipRows(items,draw), not items.map(draw)');
console.log('clip rows cost ok');
