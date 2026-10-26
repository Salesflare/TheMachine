// Web Push sender: a phone-side decryption of the payload and a verified VAPID signature.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {mkdtempSync, statSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {vapidKeys, vapidHeader, encrypt, send} from '../push-send.mjs';

const keyFile = mkdtempSync(tmpdir() + '/push-') + '/vapid.json';
const keys = vapidKeys(keyFile);
assert.equal(statSync(keyFile).mode & 0o777, 0o600);
assert.equal(vapidKeys(keyFile).publicKey, keys.publicKey, 'the key pair is created once and reused');
assert.equal(Buffer.from(keys.publicKey, 'base64url').length, 65);

// What the phone does (RFC 8291): decrypt with its own private key and auth secret.
const phone = crypto.createECDH('prime256v1'); phone.generateKeys();
const auth = crypto.randomBytes(16);
const payload = JSON.stringify({title: 'Ready: Wise top-up', body: 'Draft is ready', url: 'https://x/assistant/#result=0123456789abcdef'});
const message = encrypt(payload, phone.getPublicKey().toString('base64url'), auth.toString('base64url'));
const salt = message.subarray(0, 16), rs = message.readUInt32BE(16), idlen = message[20];
assert.equal(rs, 4096); assert.equal(idlen, 65);
const serverPublic = message.subarray(21, 21 + idlen), sealed = message.subarray(21 + idlen);
const hkdf = (ikm, s, info, n) => Buffer.from(crypto.hkdfSync('sha256', ikm, s, info, n));
const ikm = hkdf(phone.computeSecret(serverPublic), auth, Buffer.concat([Buffer.from('WebPush: info\0'), phone.getPublicKey(), serverPublic]), 32);
const decipher = crypto.createDecipheriv('aes-128-gcm', hkdf(ikm, salt, Buffer.from('Content-Encoding: aes128gcm\0'), 16), hkdf(ikm, salt, Buffer.from('Content-Encoding: nonce\0'), 12));
decipher.setAuthTag(sealed.subarray(-16));
const plain = Buffer.concat([decipher.update(sealed.subarray(0, -16)), decipher.final()]);
assert.equal(plain.at(-1), 2, 'single final record delimiter');
assert.equal(plain.subarray(0, -1).toString(), payload);

// VAPID: the push service verifies the JWT with the public key from the same header.
const header = vapidHeader('https://fcm.googleapis.com/fcm/send/abc', keys);
const [, token, k] = /^vapid t=([^,]+), k=(.+)$/.exec(header);
assert.equal(k, keys.publicKey);
const [h, c, sig] = token.split('.');
const claims = JSON.parse(Buffer.from(c, 'base64url'));
assert.equal(claims.aud, 'https://fcm.googleapis.com'); assert.ok(claims.exp > Date.now() / 1000);
const raw = Buffer.from(k, 'base64url');
const publicKey = crypto.createPublicKey({key: {kty: 'EC', crv: 'P-256', x: raw.subarray(1, 33).toString('base64url'), y: raw.subarray(33).toString('base64url')}, format: 'jwk'});
assert.ok(crypto.verify('sha256', Buffer.from(h + '.' + c), {key: publicKey, dsaEncoding: 'ieee-p1363'}, Buffer.from(sig, 'base64url')));

// Delivery result: the push service status, or 0 when it can't be reached.
const subscription = {endpoint: 'https://push.example/x', p256dh: phone.getPublicKey().toString('base64url'), auth: auth.toString('base64url')};
let seen;
assert.equal(await send(subscription, {title: 't'}, keys, async (url, init) => { seen = init; return {status: 201}; }), 201);
assert.equal(seen.headers['Content-Encoding'], 'aes128gcm'); assert.equal(seen.headers.TTL, '86400');
assert.equal(await send(subscription, {title: 't'}, keys, async () => { throw new Error('offline'); }), 0);
console.log('push sender ok');
