// Revokes the Apple Development certificate an iOS upload run made for itself.
// Xcode's automatic signing on a fresh runner creates a new "Apple Development: Created via API" certificate on every
// archive, and its private key goes away with the runner. Left alone they pile up until Apple's limit, and the next
// archive fails with "Your account has reached the maximum number of certificates". This revokes the ones created in
// the last day (a certificate runs a year, so its expiry tells when it was made); nothing else on the team is touched.
// Env: ASC_KEY_ID, ASC_ISSUER_ID, ASC_KEY_FILE (the .p8 path).
import { createSign, createPrivateKey } from 'node:crypto';
import { readFileSync } from 'node:fs';

const b64 = o => Buffer.from(JSON.stringify(o)).toString('base64url');
const now = Math.floor(Date.now() / 1000);
const head = b64({ alg: 'ES256', kid: process.env.ASC_KEY_ID, typ: 'JWT' });
const body = b64({ iss: process.env.ASC_ISSUER_ID, iat: now, exp: now + 600, aud: 'appstoreconnect-v1' });
const key = createPrivateKey(readFileSync(process.env.ASC_KEY_FILE));
const sig = createSign('SHA256').update(`${head}.${body}`).sign({ key, dsaEncoding: 'ieee-p1363' }).toString('base64url');
const auth = { Authorization: `Bearer ${head}.${body}.${sig}` };
const api = 'https://api.appstoreconnect.apple.com/v1/certificates';

const r = await fetch(`${api}?filter[certificateType]=DEVELOPMENT&fields[certificates]=name,expirationDate&limit=200`, { headers: auth });
if (!r.ok) { console.log(`::warning::could not list certificates (${r.status})`); process.exit(0); }
const since = Date.now() + (365 - 1) * 86400e3;
const ours = (await r.json()).data.filter(c => c.attributes.name === 'Apple Development: Created via API'
  && Date.parse(c.attributes.expirationDate) > since);
for (const c of ours) {
  const d = await fetch(`${api}/${c.id}`, { method: 'DELETE', headers: auth });
  console.log(`revoked this run's development certificate ${c.id}: ${d.status}`);
}
if (!ours.length) console.log('no development certificate from this run to revoke');
