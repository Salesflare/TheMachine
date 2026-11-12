// The one way tests get a browser: playwright-core's chromium, with launch() fenced so a page can never open an app on
// the computer. Headless Chromium hands links it can't show itself (mailto:, tel:, custom schemes) to the desktop, and
// a test that clicks an email address would open the real mail app. So every launch here runs the browser cut off from
// the desktop: no session bus (the portal that opens links), no display, its own empty runtime, config and data
// folders (no mimeapps.list, no ~/.local/share/applications handlers), and a PATH whose xdg-open and siblings only write
// what they were asked to OPENED. tests/test_browser_guard.mjs checks that it holds and that no test loads
// playwright-core around it.
import {mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, delimiter} from 'node:path';
import {OPENCLAW} from '../openclaw-root.mjs';

// OpenClaw's own copy (or PLAYWRIGHT_CORE); sandbox/shots.mjs also runs where only an npm install of either package is
async function load() {
  const from = process.env.PLAYWRIGHT_CORE || OPENCLAW + '/node_modules/playwright-core/index.mjs';
  try { return await import(from); } catch (error) {
    for (const name of ['playwright-core', 'playwright']) { try { return await import(name); } catch {} }
    throw error;
  }
}
const core = await load();

const FENCE = mkdtempSync(join(tmpdir(), 'browser-fence-'));
export const OPENED = join(FENCE, 'opened.log');
const STUB = `#!/bin/sh\nprintf '%s\\n' "$*" >> '${OPENED}'\nexit 0\n`;
const OPENERS = ['xdg-open', 'xdg-email', 'xdg-settings', 'xdg-mime', 'gio', 'kde-open', 'kde-open5', 'gnome-open', 'exo-open', 'sensible-browser'];
const BIN = join(FENCE, 'bin');
for (const dir of [BIN, join(FENCE, 'run'), join(FENCE, 'config'), join(FENCE, 'data')]) mkdirSync(dir, {mode: 0o700});
for (const name of OPENERS) writeFileSync(join(BIN, name), STUB, {mode: 0o755});
process.on('exit', () => { try { rmSync(FENCE, {recursive: true, force: true}); } catch {} });

// What a fenced browser asked the desktop, oldest first
export const opened = () => { try { return readFileSync(OPENED, 'utf8').split('\n').filter(Boolean); } catch { return []; } };

// The browser's environment: the caller's, cut off from the desktop. Exported for the guard test.
export function fencedEnv(base = process.env) {
  const env = {...base};
  for (const key of ['DISPLAY', 'WAYLAND_DISPLAY', 'WAYLAND_SOCKET', 'DBUS_SYSTEM_BUS_ADDRESS']) delete env[key];
  Object.assign(env, {
    PATH: BIN + delimiter + (env.PATH || ''),
    BROWSER: join(BIN, 'xdg-open'),
    DBUS_SESSION_BUS_ADDRESS: 'unix:path=' + join(FENCE, 'no-bus'),
    XDG_RUNTIME_DIR: join(FENCE, 'run'),
    XDG_CONFIG_HOME: join(FENCE, 'config'),
    XDG_DATA_HOME: join(FENCE, 'data'),
    XDG_DATA_DIRS: join(FENCE, 'data'),
  });
  return env;
}
const fenced = (options = {}) => ({...options, env: fencedEnv({...process.env, ...(options.env || {})})});

// launch, launchServer and launchPersistentContext as playwright-core's own, called at call time (scripts/
// test_impact_js.mjs patches launch on the real object), with the fenced environment
const WRAPPED = {
  launch: (target) => (options) => target.launch(fenced(options)),
  launchServer: (target) => (options) => target.launchServer(fenced(options)),
  launchPersistentContext: (target) => (dir, options) => target.launchPersistentContext(dir, fenced(options)),
};
export const chromium = new Proxy(core.chromium, {
  get(target, key) {
    if (WRAPPED[key]) return WRAPPED[key](target);
    const value = target[key];
    return typeof value === 'function' ? value.bind(target) : value;
  },
});
export default core;
