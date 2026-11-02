import assert from 'node:assert/strict';
import vm from 'node:vm';
import {dashboardPage} from './dashboard-page.mjs';

// html`...` in dashboard.html: markup that escapes by construction. Every ${} is escaped as esc() does, except nested
// html`` results and raw() of a vetted constant; arrays join their items the same way; setHTML only takes html``.
const page=await dashboardPage();
const line=start=>{const i=page.indexOf(start);assert.ok(i>=0,start);return page.slice(i,page.indexOf('\n',i))};
const src=[line('const esc='),line('class SafeHTML'),line('const raw='),line('const htmlPart='),line('const html='),line('const setHTML=')].join('\n');
const ctx={};vm.createContext(ctx);vm.runInContext(src+'\nObject.assign(globalThis,{esc,raw,html,setHTML,SafeHTML});',ctx);
const {html,raw,setHTML,SafeHTML}=ctx;
const s=h=>{assert.ok(h instanceof SafeHTML);return String(h)};

// Every interpolation is escaped, in text and in attributes, with the same rules as esc()
const evil=`<img src=x onerror="alert(1)">'&`;
assert.equal(s(html`<p title="${evil}">${evil}</p>`),'<p title="&lt;img src=x onerror=&quot;alert(1)&quot;&gt;&#39;&amp;">&lt;img src=x onerror=&quot;alert(1)&quot;&gt;&#39;&amp;</p>');
assert.equal(s(html`${null}|${undefined}|${0}|${false}|${''}`),'||0|false|',"null and undefined are empty, like esc()");
assert.equal(s(html`plain`),'plain');
assert.equal(s(html``),'');

// A nested html`` result passes through as markup; its own values were escaped when it was made
const inner=html`<b>${'<i>'}</b>`;
assert.equal(s(html`<p>${inner}</p>`),'<p><b>&lt;i&gt;</b></p>');
assert.equal(s(html`<p>${html`<span>${html`<em>${'&'}</em>`}</span>`}</p>`),'<p><span><em>&amp;</em></span></p>');

// Arrays join without a separator; markup items pass, text items are escaped, nested arrays flatten
assert.equal(s(html`<ul>${['a','b'].map(x=>html`<li>${x}</li>`)}</ul>`),'<ul><li>a</li><li>b</li></ul>');
assert.equal(s(html`${['<', html`<br>`, ['>', html`<hr>`]]}`),'&lt;<br>&gt;<hr>');
assert.equal(s(html`${[]}`),'');

// A plain string never passes as markup, also not one built from an html`` result (that is text again)
assert.equal(s(html`${'<b>x</b>'}`),'&lt;b&gt;x&lt;/b&gt;');
assert.equal(s(html`${String(html`<b>x</b>`)}`),'&lt;b&gt;x&lt;/b&gt;');

// raw() marks a vetted constant as markup
assert.equal(s(html`<p>${raw('<br>')}</p>`),'<p><br></p>');

// setHTML writes html`` results and refuses everything else
const el={innerHTML:''};
setHTML(el,html`<b>${'<x>'}</b>`);assert.equal(el.innerHTML,'<b>&lt;x&gt;</b>');
for(const bad of ['<b>x</b>',null,undefined,{s:'<b>x</b>'},['<b>']])assert.throws(()=>setHTML(el,bad),{name:'TypeError'});
assert.equal(el.innerHTML,'<b>&lt;x&gt;</b>');
console.log('html template ok');
