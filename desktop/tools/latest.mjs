// What the app reads to know of a newer version: node latest.mjs <folder with the files and their .sig> [release tag].
// With a tag, the files are that release's own (releases/download/<tag>/), so a newer release published meanwhile never
// pairs this version with another one's file. Nothing of it is public until it is on a release (desktop.yml, publish).
import {readFileSync} from 'node:fs';
import {relative, resolve, sep} from 'node:path';

const conf = JSON.parse(readFileSync(new URL('../tauri.conf.json', import.meta.url)));
const [given, tag] = process.argv.slice(2);
if (!given) throw new Error('which folder?');
if (tag && !/^release-\d{8}-\d{4}$/.test(tag)) throw new Error(`${tag} is not a release tag`);
const folder = resolve(given);
const at = tag ? `https://github.com/Salesflare/TheMachine/releases/download/${tag}/` : conf.plugins.updater.endpoints[0];
// Only these three signatures are read, and only from inside the folder.
const SIGNED = {mac: 'the-machine-desktop-mac.app.tar.gz', windows: 'the-machine-desktop-setup.exe', linux: 'the-machine-desktop-x86_64.AppImage'};
const of = which => {
  const file = SIGNED[which];
  const path = resolve(folder, `${file}.sig`);
  const inside = relative(folder, path);
  if (!inside || inside.startsWith('..') || inside.includes(sep)) throw new Error(`${path} is not in ${folder}`);
  return {signature: readFileSync(path, 'utf8').trim(), url: new URL(file, at).href};
};
const mac = of('mac'), windows = of('windows'), linux = of('linux'); // linux: the AppImage, which alone replaces itself (updates.rs)
console.log(JSON.stringify({version: conf.version, platforms: {'darwin-aarch64': mac, 'darwin-x86_64': mac, 'windows-x86_64': windows, 'linux-x86_64': linux}}, null, 2));
