// Web Push for the installed dashboard app Node's built-in crypto only:
// VAPID (RFC 8292) signing and aes128gcm payload encryption (RFC 8291/8188).
// stdin {"action":"key"}  -> {"key": <VAPID public key, base64url>}, creating the key pair once.
// stdin {"action":"send","subscriptions":[{endpoint,p256dh,auth,shown}],"payload":{...}}
// shown goes in that device's payload: what it answers with once it showed it (sw.js).
//   -> {"results":[{endpoint,status}]}; status 0 means the push service was unreachable.
import crypto from 'node:crypto';
import {readFileSync, writeFileSync, existsSync} from 'node:fs';
import {homedir} from 'node:os';

const KEY_FILE = process.env.PUSH_VAPID_FILE || homedir() + '/.local/share/personal-assistant/vapid.json';
// VAPID contact: the dashboard URL (the service sets it from dashboard_host) or a mailto: address.
const SUBJECT = process.env.PUSH_VAPID_SUBJECT || 'https://assistant.example.com/';
const b64 = buf => Buffer.from(buf).toString('base64url');

export function vapidKeys(file = KEY_FILE) {
  if (!existsSync(file)) {
    const {privateKey} = crypto.generateKeyPairSync('ec', {namedCurve: 'prime256v1'});
    writeFileSync(file, JSON.stringify(privateKey.export({format: 'jwk'})), {mode: 0o600, flag: 'wx'});
  }
  const jwk = JSON.parse(readFileSync(file, 'utf8'));
  const raw = Buffer.concat([Buffer.from([4]), Buffer.from(jwk.x, 'base64url'), Buffer.from(jwk.y, 'base64url')]);
  return {privateKey: crypto.createPrivateKey({key: jwk, format: 'jwk'}), publicKey: b64(raw)};
}

export function vapidHeader(endpoint, keys, now = Date.now()) {
  const part = value => b64(JSON.stringify(value));
  const unsigned = part({typ: 'JWT', alg: 'ES256'}) + '.' + part({aud: new URL(endpoint).origin, exp: Math.floor(now / 1000) + 12 * 3600, sub: SUBJECT});
  const signature = crypto.sign('sha256', Buffer.from(unsigned), {key: keys.privateKey, dsaEncoding: 'ieee-p1363'});
  return `vapid t=${unsigned}.${b64(signature)}, k=${keys.publicKey}`;
}

export function encrypt(payload, p256dh, auth, salt = crypto.randomBytes(16), server = crypto.createECDH('prime256v1')) {
  if (!safe(() => server.getPrivateKey())) server.generateKeys();
  const client = Buffer.from(p256dh, 'base64url'), serverPublic = server.getPublicKey();
  const shared = server.computeSecret(client);
  const hkdf = (ikm, salt, info, length) => Buffer.from(crypto.hkdfSync('sha256', ikm, salt, info, length));
  const ikm = hkdf(shared, Buffer.from(auth, 'base64url'), Buffer.concat([Buffer.from('WebPush: info\0'), client, serverPublic]), 32);
  const key = hkdf(ikm, salt, Buffer.from('Content-Encoding: aes128gcm\0'), 16);
  const nonce = hkdf(ikm, salt, Buffer.from('Content-Encoding: nonce\0'), 12);
  const cipher = crypto.createCipheriv('aes-128-gcm', key, nonce);
  const body = Buffer.concat([cipher.update(Buffer.concat([Buffer.from(payload), Buffer.from([2])])), cipher.final(), cipher.getAuthTag()]);
  const header = Buffer.alloc(21); salt.copy(header); header.writeUInt32BE(4096, 16); header[20] = serverPublic.length;
  return Buffer.concat([header, serverPublic, body]);
}
const safe = f => { try { return f(); } catch { return null; } };

export async function send(subscription, payload, keys, fetcher = fetch) {
  try {
    const response = await fetcher(subscription.endpoint, {method: 'POST', signal: AbortSignal.timeout(10000), headers: {
      'Content-Encoding': 'aes128gcm', 'Content-Type': 'application/octet-stream', TTL: '86400', Urgency: 'high',
      Authorization: vapidHeader(subscription.endpoint, keys)}, body: encrypt(JSON.stringify(subscription.shown ? {...payload, shown: subscription.shown} : payload), subscription.p256dh, subscription.auth)});
    return response.status;
  } catch { return 0; }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  let input = ''; for await (const chunk of process.stdin) input += chunk;
  const request = JSON.parse(input), keys = vapidKeys();
  if (request.action === 'key') console.log(JSON.stringify({key: keys.publicKey}));
  else console.log(JSON.stringify({results: await Promise.all((request.subscriptions || []).map(async s => ({endpoint: s.endpoint, status: await send(s, request.payload, keys)})))}));
}
