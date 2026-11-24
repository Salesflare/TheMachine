// Whether a file's signature (<file>.sig) is by the key the app trusts (../tauri.conf.json): node verify.mjs <file>...
import {createHash, createPublicKey, verify} from 'node:crypto';
import {readFileSync} from 'node:fs';

const conf = JSON.parse(readFileSync(new URL('../tauri.conf.json', import.meta.url)));
const lines = text => Buffer.from(text.trim(), 'base64').toString().split('\n');
const key = Buffer.from(lines(conf.plugins.updater.pubkey)[1], 'base64'); // 2 of the kind, 8 of its id, 32 of the key
const open = createPublicKey({key: Buffer.concat([Buffer.from('302a300506032b6570032100', 'hex'), key.subarray(10)]), format: 'der', type: 'spki'});
for (const file of process.argv.slice(2)) {
  const of = lines(readFileSync(file + '.sig', 'utf8')), sig = Buffer.from(of[1], 'base64');
  const said = createHash('blake2b512').update(readFileSync(file)).digest();
  const ok = sig.subarray(0, 2).toString() === 'ED' && sig.subarray(2, 10).equals(key.subarray(2, 10)) && verify(null, said, open, sig.subarray(10))
    && verify(null, Buffer.concat([sig.subarray(10), Buffer.from(of[2].replace('trusted comment: ', ''))]), open, Buffer.from(of[3], 'base64'));
  console.log(file, ok ? 'is signed by its key' : 'is NOT signed by its key');
  if (!ok) process.exit(1);
}
