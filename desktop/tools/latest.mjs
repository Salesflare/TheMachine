// What the app reads to know of a newer version: node latest.mjs <folder with the files and their .sig>. Nothing of it is
// public until it is uploaded as latest.json where tauri.conf.json says, next to the files.
import {readFileSync} from 'node:fs';
import {join} from 'node:path';

const conf = JSON.parse(readFileSync(new URL('../tauri.conf.json', import.meta.url)));
const of = file => ({signature: readFileSync(join(process.argv[2], file + '.sig'), 'utf8').trim(), url: new URL(file, conf.plugins.updater.endpoints[0]).href});
const mac = of('the-machine-desktop-mac.app.tar.gz'), windows = of('the-machine-desktop-setup.exe');
console.log(JSON.stringify({version: conf.version, platforms: {'darwin-aarch64': mac, 'darwin-x86_64': mac, 'windows-x86_64': windows}}, null, 2));
