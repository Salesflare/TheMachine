// What the app reads to know of a newer version: node latest.mjs <folder with the files and their .sig> [release tag].
// With a tag, the files are that release's own (releases/download/<tag>/), so a newer release published meanwhile never
// pairs this version with another one's file. Nothing of it is public until it is on a release (desktop.yml, publish).
import {readFileSync} from 'node:fs';
import {join} from 'node:path';

const conf = JSON.parse(readFileSync(new URL('../tauri.conf.json', import.meta.url)));
const [folder, tag] = process.argv.slice(2);
if (tag && !/^release-\d{8}-\d{4}$/.test(tag)) throw new Error(`${tag} is not a release tag`);
const at = tag ? `https://github.com/Salesflare/TheMachine/releases/download/${tag}/` : conf.plugins.updater.endpoints[0];
const of = file => ({signature: readFileSync(join(folder, file + '.sig'), 'utf8').trim(), url: new URL(file, at).href});
const mac = of('the-machine-desktop-mac.app.tar.gz'), windows = of('the-machine-desktop-setup.exe');
console.log(JSON.stringify({version: conf.version, platforms: {'darwin-aarch64': mac, 'darwin-x86_64': mac, 'windows-x86_64': windows}}, null, 2));
