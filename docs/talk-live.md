# Talk live

A spoken conversation with The Machine in a to-do's chat, with OpenAI's Realtime voice. It can read the to-do and
look up other to-dos, and it can hand a request to the to-do's chat, which follows its usual rules: nothing is sent from a conversation. The help
article is [docs/help/talk-live.md](help/talk-live.md); the code is `talk_live.py`, `talk-live-run.mjs` and the
`talk*` functions in `dashboard.html`.

## Who can use it

OpenAI has to be set up in OpenClaw. The Gateway (`talk.catalog`) says whether its OpenAI realtime provider is
configured and can open a browser session; the wave next to the mic in a to-do's chat shows only then, and Settings,
General, Voice input says whether it's ready.

- **A ChatGPT sign-in** (the Codex OAuth profile): OpenClaw's docs say GA Realtime browser sessions work over a ChatGPT
  subscription "when the account has access". The Gateway mints the session through its broker and the offer goes to
  the Gateway's own `/plugins/openai/realtime/calls` (single-use, 60 s). No per-use cost note is shown.
- **An OpenAI API key**: an ephemeral client secret from OpenAI; the offer goes to
  `https://api.openai.com/v1/realtime/calls`. OpenAI bills the key per minute, so the bar shows one short line saying so.

When both are set up, OpenClaw uses the key; it doesn't offer a way to prefer the sign-in per session.

OpenAI's server-side turn detection lets the owner interrupt: the voice stops and listens.

The model is OpenAI's GA `gpt-realtime-2.1`, not GPT-Live (`gpt-live-1`, `gpt-live-1-codex`). With GPT-Live the Gateway
owns the conversation's tools and its own agent, and OpenClaw's voice gate lets a spoken "yes" confirm a high-impact
action. Here the dashboard sets its own tools instead, and a spoken "yes" never counts.

## How a conversation runs

1. `talk_start` (owner, dashboard only): the service asks the Gateway for a session (`talk.client.create`, scopes
   `operator.read` and `operator.talk` only, never `operator.write`), for the session key
   `agent:main:assistant-talk-<to-do id>`. It keeps the session's secret in memory and returns an ID, the tools and the
   instructions (the to-do's title, the dashboard language, the time). The secret and the key never reach the browser.
2. The browser opens the microphone, makes a WebRTC offer with an `oai-events` data channel and posts it as
   `talk_offer`. The service hands it on once, with the secret, and returns OpenAI's answer. The dashboard's CSP keeps
   `connect-src 'self'`; the audio then goes directly between the browser and OpenAI over WebRTC.
3. On the data channel the dashboard sends `session.update` with the instructions, the tools and input transcription.
4. What each side says (`conversation.item.input_audio_transcription.completed`, `response.output_audio_transcript.done`)
   is posted as `talk_line` and kept in `talk_lines`; the to-do's chat shows it after a **Talked live** line.
5. **End**, leaving the chat, or 10 minutes end it (`talk_end`, `talk.client.close`). The timer warns a minute before.
   **Mute** turns the microphone track off.

At most one conversation per to-do and two in all. A session's secret is forgotten at its end, or 30 s after its limit.

## Tools

`talk_live.TOOLS`, called by the voice as Realtime function calls:

- `todo_details`: the to-do's title, status, its last 25 messages and its current draft, through `talk_tool` (read only).
- `find_todos`: open to-dos whose title has the words (read only).
- `ask_chat`: handled in the browser (`talkAsk`). The request goes to the to-do's chat the way a typed message does
  (`decideOrWait`, a decision `other`, so it can also wait offline), and the chat shows it. The chat's own rules hold: it
  can change the draft, snooze or mark the to-do done, and a draft waits for **Approve** on screen. The voice is told
  that a spoken yes does nothing, and to tell the owner to tap Approve.

## Tests

`tests/test_talk_live.py` (the Gateway helper stubbed: status, start, a single offer, the limit, the transcript in the
chat, the tools, owner only, the secret never returned) and `tests/test_talk_live_dashboard.mjs` (a fake
`getUserMedia`, `RTCPeerConnection` and data channel; screenshots at 390x844 and 1440x900, light and dark).
