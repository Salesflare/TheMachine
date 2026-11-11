// The test-impact map's browser half (scripts/test_impact.py): which functions of the dashboard's parts each test file
// runs in Chromium. scripts/test.py loads it into every Node process of a recording run (CI's full run on main) with
// NODE_OPTIONS=--import=<this file> when THE_MACHINE_IMPACT_DIR is set. When a process loads playwright-core, each page
// it opens collects V8's function coverage, and before the page navigates or closes each function of a part
// (dashboard/<name>.js) is filed by its offsets in that part and whether it ran: "dashboard/x.js<TAB>start<TAB>end<TAB>1",
// and "dashboard/x.js<TAB>-1<TAB>-1<TAB>1" for a part whose top level ran (a page loads them all). A fifth field "L" marks
// what ran while the page loaded: from opening or navigating until the test's first action on it (a click, a key, an
// evaluate: anything but reading and waiting). scripts/test_select.py counts a function the test only ran then as the
// page's start, not as something the test exercises.
import * as nodeModule from 'node:module';  // registerHooks: Node 22.15 and newer; older ones (an action's own) skip it
import {appendFileSync, readFileSync, readdirSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname, join} from 'node:path';

const OUT = process.env.THE_MACHINE_IMPACT_DIR, TEST = process.env.THE_MACHINE_IMPACT_TEST;
const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));

if (OUT && TEST && !TEST.includes('/') && typeof nodeModule.registerHooks === 'function') {
  nodeModule.registerHooks({
    load(url, context, next) {
      const loaded = next(url, context);
      if (!url.endsWith('/playwright-core/index.mjs')) return loaded;
      const source = String(loaded.source);
      // index.mjs re-exports index.js's playwright object: patch that object once it's there
      return {...loaded, source: source + `\nimport {patchPlaywright as __impactPatch} from ${JSON.stringify(import.meta.url)};\n__impactPatch(playwright);\n`};
    },
  });
}

let parts;
function partTexts() {
  if (!parts) {
    parts = [];
    for (const name of readdirSync(join(ROOT, 'dashboard')).sort()) {
      if (name.endsWith('.js')) parts.push(['dashboard/' + name, readFileSync(join(ROOT, 'dashboard', name), 'utf8')]);
    }
  }
  return parts;
}

const placed = new Map();  // a script's source -> [[part, offset in the source, the part's text]]
function where(source) {
  if (!placed.has(source)) {
    const found = [];
    for (const [name, text] of partTexts()) {
      const at = source.indexOf(text);
      if (at >= 0) found.push([name, at, text]);
    }
    placed.set(source, found.sort((a, b) => a[1] - b[1]));
  }
  return placed.get(source);
}

// V8's offsets count UTF-16 units; the map's count characters (Python's), so a part with an emoji keeps its places
const pairs = new Map();
function chars(text, offset) {
  if (!pairs.has(text)) {
    const at = [];
    for (let i = 0; i < text.length; i++) {
      const c = text.charCodeAt(i);
      if (c >= 0xd800 && c < 0xdc00) at.push(i++);
    }
    pairs.set(text, at);
  }
  const at = pairs.get(text);
  let low = 0, high = at.length;
  while (low < high) { const mid = (low + high) >> 1; if (at[mid] < offset) low = mid + 1; else high = mid; }
  return offset - low;
}

const written = new Set();
function file(entries, phase) {
  const lines = new Set();
  for (const entry of entries || []) {
    if (!entry.source) continue;
    const inside = where(entry.source);
    if (!inside.length) continue;
    for (const fn of entry.functions || []) {
      const range = fn.ranges && fn.ranges[0];
      if (!range) continue;
      const ran = range.count ? 1 : 0;
      for (const [name, at, text] of inside) {
        const start = range.startOffset - at, end = range.endOffset - at;
        if (start <= 0 && end >= text.length) {
          if (ran && !fn.functionName && range.startOffset === 0) lines.add(`${name}\t-1\t-1\t1${phase}`);  // the script's top level
          continue;
        }
        if (start >= 0 && start < text.length) {
          lines.add(`${name}\t${chars(text, start)}\t${chars(text, Math.min(end, text.length))}\t${ran}${phase}`);
          break;
        }
      }
    }
  }
  const fresh = [...lines].filter(line => !written.has(line));
  fresh.forEach(line => written.add(line));
  if (fresh.length) appendFileSync(join(OUT, `${TEST}.${process.pid}.jsrec`), fresh.join('\n') + '\n');
}

// Function-level coverage straight from V8 (Playwright's page.coverage counts every block, which slows the page enough
// to upset tests that race it): which functions ran, taken before the page navigates away or closes.
async function collect(page, done) {
  const watch = page.__impact;
  if (!watch) return;
  if (done) page.__impact = null;
  try {
    const {result} = await watch.session.send('Profiler.takePreciseCoverage');
    const entries = [];
    for (const script of result) {
      if (!script.url || !script.functions.some(fn => fn.ranges[0] && fn.ranges[0].count)) continue;
      if (!watch.sources.has(script.scriptId)) {
        watch.sources.set(script.scriptId, (await watch.session.send('Debugger.getScriptSource', {scriptId: script.scriptId})).scriptSource);
      }
      entries.push({source: watch.sources.get(script.scriptId), functions: script.functions});
    }
    file(entries, watch.loading ? '\tL' : '');
    if (watch.loading && !done) {
      // a fresh start, so a function that ran while loading is noted again when the test runs it (binary coverage
      // notes each function once until coverage restarts)
      watch.loading = false;
      await watch.session.send('Profiler.stopPreciseCoverage');
      await watch.session.send('Profiler.startPreciseCoverage', {callCount: false, detailed: false});
    }
  } catch {}
}

// The test's first action on a page ends its loading. Reading and waiting don't: a test waits for the first render
// before it acts.
const READS = new Set(['waitForSelector', 'waitForFunction', 'waitForTimeout', 'waitForLoadState', 'waitForURL',
  'textContent', 'innerText', 'innerHTML', 'getAttribute', 'inputValue', 'isChecked', 'isVisible', 'isHidden',
  'isEnabled', 'isDisabled', 'isEditable', 'expect', 'querySelector', 'querySelectorAll', 'queryCount', 'title',
  'content', 'boundingBox', 'screenshot', 'ariaSnapshot', 'jsonValue', 'getProperty', 'getPropertyList', 'dispose',
  'ownerFrame', 'contentFrame', 'setViewportSize', 'emulateMedia', 'addInitScript', 'exposeBinding',
  'setExtraHTTPHeaders', 'setNetworkInterceptionPatterns', 'setWebSocketInterceptionPatterns', 'bringToFront',
  'consoleMessages', 'pageErrors', 'requests', 'updateSubscription']);
const NAVIGATIONS = new Set(['goto', 'reload', 'goBack', 'goForward', 'setContent']);
const pagesLoading = new Set();
function acting(object, method) {
  if (!pagesLoading.size || READS.has(method) || NAVIGATIONS.has(method)) return [];
  if (!['Frame', 'Page', 'ElementHandle', 'JSHandle'].includes(object && object._type)) return [];
  const page = object._type === 'Page' ? object : object._type === 'Frame' ? object._page : null;
  // a handle whose page isn't known ends every page's loading: what it does then counts as the test's own
  return page ? (pagesLoading.has(page) ? [page] : []) : [...pagesLoading];
}
async function loaded(pages) {
  for (const page of pages) {
    pagesLoading.delete(page);
    if (page.__impact && page.__impact.loading) await collect(page, false);
  }
}

async function watch(page) {
  try {
    const session = await page.context().newCDPSession(page);
    await session.send('Debugger.enable');
    await session.send('Debugger.setSkipAllPauses', {skip: true});
    await session.send('Profiler.enable');
    await session.send('Profiler.startPreciseCoverage', {callCount: false, detailed: false});
    page.__impact = {session, sources: new Map(), loading: true};
    pagesLoading.add(page);
    for (const name of NAVIGATIONS) {
      const original = page[name].bind(page);
      page[name] = async (...args) => {
        await collect(page, false);
        if (page.__impact) { page.__impact.loading = true; pagesLoading.add(page); }
        return original(...args);
      };
    }
    const close = page.close.bind(page);
    page.close = async (...args) => { pagesLoading.delete(page); await collect(page, true); return close(...args); };
  } catch {}
  return page;
}

function watchContext(context, pages) {
  const newPage = context.newPage.bind(context);
  context.newPage = async (...args) => { const page = await watch(await newPage(...args)); pages.add(page); return page; };
  const close = context.close.bind(context);
  context.close = async (...args) => { for (const page of pages) await collect(page, true); return close(...args); };
  return context;
}

function watchBrowser(browser) {
  const pages = new Set();
  const newContext = browser.newContext.bind(browser);
  browser.newContext = async (...args) => watchContext(await newContext(...args), pages);
  const newPage = browser.newPage.bind(browser);
  browser.newPage = async (...args) => { const page = await watch(await newPage(...args)); pages.add(page); return page; };
  const close = browser.close.bind(browser);
  browser.close = async (...args) => { for (const page of pages) await collect(page, true); return close(...args); };
  return browser;
}

export function patchPlaywright(playwright) {
  const chromium = playwright && playwright.chromium;
  if (!chromium || chromium.__impact) return;
  chromium.__impact = true;
  const connection = chromium._connection;
  if (connection && typeof connection.sendMessageToServer === 'function') {
    const send = connection.sendMessageToServer.bind(connection);
    connection.sendMessageToServer = (object, method, ...rest) => {
      const pages = acting(object, method);
      return pages.length ? loaded(pages).then(() => send(object, method, ...rest)) : send(object, method, ...rest);
    };
  }
  const launch = chromium.launch.bind(chromium);
  chromium.launch = async (...args) => watchBrowser(await launch(...args));
}
