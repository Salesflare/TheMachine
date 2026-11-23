// Installs a page's web app in Chrome or Edge as their own Install does, or takes it away. For windows.py.
//   node webapp.mjs <browser.exe> <its data folder> <install|uninstall> <address>
// The browser takes these commands on a pipe only, and not with its usual data folder.
import {spawn} from 'node:child_process';
const [browser, data, what, address] = process.argv.slice(2);
const child = spawn(browser, [`--user-data-dir=${data}`, '--profile-directory=Default', '--no-first-run', '--no-default-browser-check', '--remote-debugging-pipe', 'about:blank'],
  {stdio: ['ignore', 'ignore', 'ignore', 'pipe', 'pipe']});
let text = '', last = 0;
const asked = new Map();
child.stdio[4].on('data', d => {
  text += d;
  for (let end; (end = text.indexOf('\0')) >= 0; text = text.slice(end + 1)) {
    const m = JSON.parse(text.slice(0, end));
    asked.get(m.id)?.(m);
  }
});
const ask = (method, params = {}) => new Promise((done, failed) => {
  asked.set(++last, m => (m.error ? failed(new Error(`${method}: ${m.error.message}`)) : done(m.result)));
  child.stdio[3].write(JSON.stringify({id: last, method, params}) + '\0');
});
setTimeout(() => { console.log('no answer'); child.kill(); process.exit(1) }, 60000).unref();
const gone = new Promise(done => child.on('exit', done));
try {
  console.log((await ask('Browser.getVersion')).product);
  if (what === 'install') {
    await ask('PWA.install', {manifestId: address, installUrlOrBundleUrl: address});
    await ask('PWA.changeAppUserSettings', {manifestId: address, displayMode: 'standalone'});
  } else {
    await ask('PWA.uninstall', {manifestId: address});
  }
  await new Promise(done => setTimeout(done, 12000)); // it writes its entries meanwhile
  if (what === 'install') console.log(JSON.stringify(await ask('PWA.getOsAppState', {manifestId: address})));
} catch (error) {
  console.log(error.message);
  process.exitCode = 1;
}
await Promise.race([ask('Browser.close').catch(() => {}), gone]);
await Promise.race([gone, new Promise(done => setTimeout(done, 8000))]);
child.kill();
process.exit();
