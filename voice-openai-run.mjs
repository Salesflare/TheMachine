// Voice input through the owner's OpenAI access (voice_input.py, OpenAIVoice): OpenClaw's own audio transcription,
// loaded once and kept for a few minutes, so a clip takes a second or two instead of the 8 to 10 seconds the
// `openclaw infer audio transcribe` CLI needs to start each time. OpenClaw holds the credentials (an API key, or a
// ChatGPT sign-in that allows audio); they never pass here or to the service.
//
// One JSON line in, one out: {"file": "<private clip path>", "language": "nl"} -> {"text": "..."} or {"error": "..."}.
// The first line out is {"ready": true}. Only files in the service's own clips folder are read.
import {OPENCLAW} from './openclaw-root.mjs';
import {createInterface} from 'node:readline';
import {basename, dirname, resolve} from 'node:path';

console.log = console.info = console.warn = console.error;   // OpenClaw's own notes go to stderr: stdout is the answers
const MODEL = {provider: 'openai', model: 'gpt-4o-transcribe'};   // as voice_input.OPENAI_MODEL
const LANGUAGES = ['de', 'en', 'es', 'fr', 'it', 'nl', 'pt'];
const CLIP = /^[a-f0-9]{16}\.wav$/;
const CLIPS = resolve(process.argv[2] || '.');
const say = value => process.stdout.write(JSON.stringify(value) + '\n');
const parsed = text => { try { return JSON.parse(text); } catch { return null; } };

let media, cfg, agentId, agentDir;
try {
  const sdk = name => import(`${OPENCLAW}/dist/plugin-sdk/${name}.js`);
  const [understanding, config, agents] = await Promise.all([sdk('media-understanding-runtime'), sdk('runtime-config-snapshot'), sdk('agent-runtime')]);
  media = understanding;
  cfg = config.getRuntimeConfig();
  agentId = agents.resolveDefaultAgentId(cfg);
  agentDir = agents.resolveAgentDir(cfg, agentId);
  if (typeof media.transcribeAudioFile !== 'function') throw new Error('missing');
} catch {
  say({error: 'unavailable'});
  process.exit(1);
}
say({ready: true});

for await (const line of createInterface({input: process.stdin})) {
  const request = parsed(line) || {};
  const file = typeof request.file === 'string' ? resolve(request.file) : '';
  if (!file || !CLIP.test(basename(file)) || dirname(dirname(file)) !== CLIPS) {
    say({error: 'invalid_request'});
    continue;
  }
  try {
    const result = await media.transcribeAudioFile({filePath: file, cfg, agentId, agentDir, activeModel: MODEL,
      ...(LANGUAGES.includes(request.language) ? {language: request.language} : {})});
    say({text: String(result?.text || '')});
  } catch {
    say({error: 'unavailable'});   // never the raw error: it can name paths or settings
  }
}
