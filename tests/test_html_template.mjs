import assert from 'node:assert/strict';
import vm from 'node:vm';
import {dashboardPage} from './dashboard-page.mjs';

// html`...` in dashboard.html: markup that escapes by construction. Every ${} is escaped as esc() does, except nested
// html`` results and raw() of a vetted constant; arrays join their items the same way; setHTML only takes html``.
// htmlT is t() for a sentence with markup in its {}; safeHref keeps only web, mail, phone and same-page links.
const page=await dashboardPage();
const line=start=>{const i=page.indexOf(start);assert.ok(i>=0,start);return page.slice(i,page.indexOf('\n',i))};
const src=[line('const esc='),line('class SafeHTML'),line('const raw='),line('const htmlPart='),line('const html='),line('const setHTML='),line('const htmlT='),line('const safeHref=')].join('\n');
// t() stands in for the catalog: a translation with an apostrophe, and {} filled in order
const t=(key,...a)=>{let i=0;return ({'Last sync {}':'Dernière synchro {}','Hi {}':"Salut {} l'ami"}[key]??key).replace(/\{\}/g,()=>String(a[i++]))};
const ctx={t,URL,location:{href:'https://machine.example/app/'}};vm.createContext(ctx);vm.runInContext(src+'\nObject.assign(globalThis,{esc,raw,html,setHTML,SafeHTML,htmlT,safeHref});',ctx);
const {html,raw,setHTML,SafeHTML,htmlT,safeHref}=ctx;
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

// htmlT: the sentence and its text values are escaped, its html`` values stay markup
assert.equal(s(htmlT('Last sync {}',html`<time>${'1h'}</time>`)),'Dernière synchro <time>1h</time>');
assert.equal(s(htmlT('Hi {}','<b>Sam</b>')),'Salut &lt;b&gt;Sam&lt;/b&gt; l&#39;ami');
assert.equal(s(htmlT('{} and {}',html`<i>a</i>`,'<b>')),'<i>a</i> and &lt;b&gt;');
assert.equal(s(htmlT('No values')),'No values');

// safeHref: web, mail, phone and this page's own links stay as they are; anything else becomes '#'
for(const ok of ['https://example.com/a?b=1&c="2"','http://example.com','HTTPS://EXAMPLE.COM','mailto:sam@example.com','tel:+3212345',
 '#card=d1','/support','support','?q=1','//machine.example/x','https://machine.example/app/#x'])assert.equal(safeHref(ok),ok,ok);
for(const bad of ['javascript:alert(1)','JavaScript:alert(1)',' javascript:alert(1)','java\tscript:alert(1)','\njavascript:alert(1)',
 'data:text/html,<b>x</b>','vbscript:x','blob:https://machine.example/x','file:///etc/passwd','http://[bad',null,undefined,'','  '])assert.equal(safeHref(bad),'#',String(bad));
assert.equal(safeHref(' https://example.com '),'https://example.com','trimmed');
assert.equal(s(html`<a href="${safeHref('javascript:alert(1)')}">x</a>`),'<a href="#">x</a>');
// The formatters build their links with html`` too: text is escaped, only web (and, in help, mail) links become links
const fn=(start,end)=>{const i=page.indexOf(start);assert.ok(i>=0,start);const j=page.indexOf(end,i);assert.ok(j>i,end);return page.slice(i,j+end.length)};
vm.runInContext(`const HELP='https://site.example/help/';${line('const linkify=')}\n${fn('function helpDoc(a)',"return html`${out}`}")}\nObject.assign(globalThis,{linkify,helpDoc});`,ctx);
const {linkify,helpDoc}=ctx;
assert.equal(s(linkify('See https://example.com/a?b=1&c=2, and <b>bold</b> javascript:alert(1) data:text/html,x')),
 'See <a href="https://example.com/a?b=1&amp;c=2" target="_blank" rel="noreferrer">https://example.com/a?b=1&amp;c=2</a>, and &lt;b&gt;bold&lt;/b&gt; javascript:alert(1) data:text/html,x');
assert.equal(s(linkify('"https://example.com/x"')),'&quot;<a href="https://example.com/x" target="_blank" rel="noreferrer">https://example.com/x</a>&quot;','a quote ends the link');
assert.equal(s(linkify(null)),'');
const doc=s(helpDoc({title:'T <b>',summary:'**a `c` b** [x](javascript:alert(1)) [d](data:text/html,x) [y](https://e.com/?a=1&b="2") [m](mailto:sam@example.com) [z](cards.md#a-b)',
 body:'## H <i>\n- **[l](https://x.y)**\n1. one\n```\n<script>\n```\npara & <x>',anchors:['a"b']}));
assert.equal(doc,'<h3>T &lt;b&gt;</h3><p class="help-sum"><b>a <code>c</code> b</b> x) d <a href="https://e.com/?a=1&amp;b=&quot;2&quot;" target="_blank" rel="noopener">y</a> <a href="mailto:sam@example.com" target="_blank" rel="noopener">m</a> <a href="https://site.example/help/cards#a-b" data-help-slug="cards" data-help-anchor="a-b">z</a></p>'
 +'<h4 id="help-a-a&quot;b">H &lt;i&gt;</h4><ul><li><b><a href="https://x.y" target="_blank" rel="noopener">l</a></b></li></ul><ol><li>one</li></ol><pre>&lt;script&gt;</pre><p>para &amp; &lt;x&gt;</p>');
console.log('html template ok');
