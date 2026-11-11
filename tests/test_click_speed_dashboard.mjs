import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {measure, median, BASELINE, SETTLE} from './click-speed.mjs';
import {dashboardPage} from './dashboard-page.mjs';

// Every click answers in about 100 ms (docs/vision.md). The dashboard's most common clicks (tests/click-speed.mjs: Do it,
// Done, Snooze, open and close a to-do, the tabs, the Work/Personal filter, search, a chat message) are timed on made-up
// data at 1440x900, and at 390x844 with the CPU 4x slower, and none may be clearly slower than its baseline
// (tests/click-speed-baseline.json). Clearly: more than twice the baseline and 60 ms over it, after the baseline is
// scaled to how fast this computer is right now (each size's calibration), so a busy test run doesn't fail it.
// After a change that makes a click slower or faster on purpose: node tests/click-speed.mjs --baseline (15 runs).
// A tap this soon after a scroll only ends that scroll (the page's chatRealTap): the benchmark waits longer
// after scrolling a target into view, or its tap on a to-do's Chat link opens nothing on a fast, quiet computer.
const tapAfterScroll=+/scrolled:Date\.now\(\)-chatScrolledAt<(\d+)/.exec(await dashboardPage())?.[1];
assert.ok(tapAfterScroll>0&&SETTLE>=tapAfterScroll+100,`the benchmark waits ${SETTLE} ms after a scroll, the page ignores taps for ${tapAfterScroll} ms`);
const baseline=JSON.parse(await readFile(BASELINE,'utf8'));
const runs={desk:5,phone:3};
const slower=[],missing=[];
for(const size of Object.keys(baseline)){
 const {times,calibration,errors}=await measure({runs:runs[size]||3,sizes:[size]});
 const scale=Math.max(1,calibration[size]/baseline[size].calibration);
 for(const [click,base] of Object.entries(baseline[size].clicks)){const got=median(times[size][click]||[]);
  if(got==null){missing.push(`${size} ${click}`);continue}
  const limit=Math.round(Math.max(base*2,base+60)*scale);
  if(process.env.TIMINGS)console.log(size,click,got,'ms (baseline',base,'limit',limit+')');
  if(got>limit)slower.push(`${size} ${click}: ${got} ms, baseline ${base} ms (limit ${limit} ms at ${scale.toFixed(2)}x)`)}
 assert.deepEqual(missing,[],'every click answers: '+errors.join('; '))}
assert.deepEqual(slower,[],'a click got clearly slower than its baseline');
console.log('click speed dashboard ok');
