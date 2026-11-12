// No test can open an app on the computer (tests/browser.mjs). A page's mailto:, tel: and custom-scheme links reach only
// the fenced desktop tools: clicked, they land in the fence's log and nothing else runs. And every test and helper that
// drives a browser gets it from tests/browser.mjs, never from playwright-core directly.
import assert from 'node:assert/strict';
import {readFileSync, readdirSync} from 'node:fs';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium, opened} from './browser.mjs';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));

// 1. Nothing loads playwright-core around the fence
const direct = [];
for (const folder of ['tests', 'sandbox']) {
  for (const name of readdirSync(join(ROOT, folder))) {
    if (!name.endsWith('.mjs') || (folder === 'tests' && ['browser.mjs', 'test_browser_guard.mjs'].includes(name))) continue;
    if (/playwright-core|from ['"]playwright['"]|import\(['"]playwright['"]\)/.test(readFileSync(join(ROOT, folder, name), 'utf8'))) direct.push(`${folder}/${name}`);
  }
}
assert.deepEqual(direct, [], 'these load playwright-core themselves: get chromium from tests/browser.mjs');

// 2. Clicked external links stay inside the fence
const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage']});
try {
  const page = await browser.newPage();
  await page.setContent(['mailto:fence@example.invalid', 'tel:+15550100', 'machine-fence-check:hello']
    .map((href, i) => `<p><a id="l${i}" href="${href}">link ${i}</a></p>`).join(''));
  for (let i = 0; i < 3; i++) {
    await page.click(`#l${i}`);
    await page.click(`#l${i}`, {modifiers: ['Control']});
  }
  await page.evaluate(() => { window.open('mailto:fence@example.invalid'); location.href = 'mailto:fence@example.invalid'; });
  const until = Date.now() + 5000;
  while (!opened().some((line) => line.includes('mailto')) && Date.now() < until) await page.waitForTimeout(100);
  assert.ok(opened().some((line) => line.includes('mailto')), 'the browser asked the desktop about mailto: through the fence: ' + JSON.stringify(opened()));
} finally {
  await browser.close();
}
console.log('browser guard ok');
