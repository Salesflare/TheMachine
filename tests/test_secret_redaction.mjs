// Credentials a tool printed are not kept in the agent's session transcripts (openclaw-plugin/secret-redaction.ts).
import assert from 'node:assert/strict';
import {redactSecrets, redactMessage, registerSecretRedaction} from '../openclaw-plugin/secret-redaction.ts';

// Made-up values in the shapes providers use, put together here so no scanner mistakes this file for a leak.
const fill = (n, c = 'a') => c.repeat(n);
const fakes = {
  slack: 'xox' + 'c-' + fill(12, '1') + '-' + fill(24),
  github: 'gh' + 'p_' + fill(36, 'B'),
  openai: 's' + 'k-proj-' + fill(40, 'C'),
  google: 'ya' + '29.' + fill(40, 'd'),
  refresh: '1/' + '/0' + fill(40, 'e'),
  jwt: 'ey' + 'J' + fill(20, 'f') + '.ey' + 'J' + fill(20, 'g') + '.' + fill(20, 'h'),
  key: '-----BEGIN ' + 'PRIVATE KEY-----\n' + fill(64, 'K') + '\n-----END ' + 'PRIVATE KEY-----',
  telegram: '123456789:AA' + fill(33, 'T'),
};
for (const [name, value] of Object.entries(fakes)) {
  const out = redactSecrets(`found ${value} here`);
  assert.ok(!out.includes(value), name);
  assert.match(out, /^found \[redacted[^\]]*\] here$/, name);
}
const lines = ['Authorization: Bearer ' + fill(30, 'z'), 'Cookie: session=' + fill(20, 'y') + '; other=1',
  '"password": "' + fill(10, 'p') + '9"', '--client_secret=' + fill(20, 'q'), 'X-Api-Key: ' + fill(20, 'w')];
for (const line of lines) assert.ok(!/(zzzz|yyyy|pppp|qqqq|wwww)/.test(redactSecrets(line)), line);

// Ordinary text, ids and hashes stay as they are.
for (const text of ['The password is on the sticky note.', 'Ask for the api key tomorrow', 'commit 3f2a9c1b8e7d6f5a4b3c2d1e0f9a8b7c6d5e4f3a',
  'session abc-123', 'run 9b1d3c3e-1c2b-4c55-9f0a-2c5d1e7f8a90', 'skills, sk-1, task-list', 'secret: always follow up']) {
  assert.equal(redactSecrets(text), text, text);
}

// Messages: text parts and tool-call arguments are cleaned; thinking, signatures and unchanged messages stay as they are.
const result = {role: 'toolResult', toolCallId: 'call_1', content: [{type: 'text', text: 'token ' + fakes.slack}, {type: 'image', data: 'AAAA'}]};
const clean = redactMessage(result);
assert.notEqual(clean, result);
assert.ok(!JSON.stringify(clean).includes(fakes.slack));
assert.equal(clean.toolCallId, 'call_1');
assert.deepEqual(clean.content[1], result.content[1]);
const call = {role: 'assistant', content: [{type: 'thinking', thinking: 'x', thinkingSignature: fakes.jwt},
  {type: 'toolCall', id: 't1', name: 'exec', arguments: {command: 'curl -H "Authorization: Bearer ' + fill(30, 'z') + '"'}}]};
const cleaned = redactMessage(call);
assert.equal(cleaned.content[0], call.content[0]);
assert.ok(!cleaned.content[1].arguments.command.includes(fill(30, 'z')));
const plain = {role: 'assistant', content: [{type: 'text', text: 'All done.'}]};
assert.equal(redactMessage(plain), plain);
assert.equal(redactMessage({role: 'user', content: 'pw ' + fakes.github}).content, 'pw [redacted token]');

// Both transcript writes go through it; nothing to change means no result.
const hooks = {};
registerSecretRedaction({on(name, fn) { hooks[name] = fn; }});
assert.ok(!JSON.stringify(hooks.tool_result_persist({message: result})).includes(fakes.slack));
assert.ok(!JSON.stringify(hooks.before_message_write({message: result})).includes(fakes.slack));
assert.equal(hooks.before_message_write({message: plain}), undefined);
console.log('secret redaction ok');
