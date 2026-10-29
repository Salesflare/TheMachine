# Talk live

A spoken conversation with The Machine in a to-do's chat, with OpenAI's Realtime voice. It can read the to-do and
look up other to-dos, hand a request to the to-do's chat (which follows its usual rules), and send the draft on screen
after a confirm question and a clear yes. The help
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
action as the agent sees fit. Here the dashboard sets its own tools instead, and a spoken yes counts only under the rules in
[Sending by voice](#sending-by-voice).

## How a conversation runs

1. `talk_start` (owner, dashboard only): the service asks the Gateway for a session (`talk.client.create`, scopes
   `operator.read` and `operator.talk` only, never `operator.write`), for the session key
   `agent:main:assistant-talk-<to-do id>`. It keeps the session's secret in memory and returns an ID, the tools and the
   instructions (the to-do's title, the dashboard language, the time) and the voice and speed. The secret and the key never reach the browser.
2. The browser opens the microphone, makes a WebRTC offer with an `oai-events` data channel and posts it as
   `talk_offer`. The service hands it on once, with the secret, and returns OpenAI's answer. The dashboard's CSP keeps
   `connect-src 'self'`; the audio then goes directly between the browser and OpenAI over WebRTC.
3. On the data channel the dashboard sends `session.update` with the instructions, the tools, input transcription and
   the voice and speed.
4. What each side says (`conversation.item.input_audio_transcription.completed`, `response.output_audio_transcript.done`)
   is posted as `talk_line` (the voice's lines once their response is done, so an interrupted fragment isn't kept) and kept in `talk_lines`; the to-do's chat shows it after a **Talked live** line.
5. **End**, leaving the chat, or 10 minutes end it (`talk_end`, `talk.client.close`). The timer warns a minute before.
   **Mute** turns the microphone track off.

At most one conversation per to-do and two in all. A session's secret is forgotten at its end, or 30 s after its limit.

## Tools

`talk_live.TOOLS`, called by the voice as Realtime function calls:

- `todo_details`: the to-do's title, status, its last 25 messages and its current draft, through `talk_tool` (read only).
- `find_todos`: open to-dos whose title has the words (read only).
- `ask_chat`: handled in the browser (`talkAsk`). The request goes to the to-do's chat as a decision `other`
  (`decideOrWait`, so it can also wait offline) whose id starts with `talk_live.RELAY_PREFIX`. That hand-off is
  invisible: `card_chat` leaves it out, so the chat only shows what the owner said and **Working on it…**. The
  preparation gets `talk_live.RELAY_NOTE` (look it up on the web or in the browser when needed, answer in two or three
  plain sentences, say where it was found). The chat's own rules hold: it can change the draft, snooze or mark the to-do
  done, never send.
- One hand-off runs at a time. An ask while the chat is busy waits in the browser (`v.queue`) and goes once the turn
  ends, so a follow-up never replaces a running turn. When the turn ends (`chatPoll`, or `talkTick` as a backstop), the
  browser sends the chat's new reply to the session as a system message (`talk_live.DONE_NOTE`, or `STOPPED_NOTE`)
  with `response.create`, so the voice says the answer at once. The voice says one short line while waiting and never
  polls. If the voice is speaking, the note waits for `response.done`.
- `ask_to_send` and `send_answer`: sending by voice, below.

## Voice

`talk_voice` in the voice settings picks the Realtime voice (`voice_input.TALK_VOICES`), passed to
`talk.client.create`. The default is `cedar`. ChatGPT's Cove isn't offered on `gpt-realtime` models (only on the
ChatGPT-only `gpt-live-1-codex` route, where the Gateway owns the tools), so `cedar` is the closest. Settings plays a
short sample for each, `brand/voices/<voice>.mp3`, recorded once from the Realtime API.

OpenAI recommends `marin` and `cedar` for best quality; `cedar` stays the default. The page sets
`audio.output.speed` to `talk_live.SPEED` (0.95, a touch under OpenAI's 1.0, never slow) in its `session.update`:
`talk.client.create` takes no speed. Speed only changes playback, so how the voice talks is in
`talk_live.instructions`, laid out as OpenAI's Realtime prompting guide suggests: labeled sections (personality and tone,
length, pacing, variety, speaking not reading) before the rules, which are unchanged. It talks in short, warm turns with
contractions, varies its openers, says what a to-do is about instead of reading its title, and never reads out lists or
links, except a draft it is asked to read in full before a send question.

## Sending by voice

The rule is the same as for a tap: only what the owner has seen or heard, and approved.

1. **The question.** The owner asks to send. `ask_to_send` (browser, `talkAskSend`) works only for the current draft
   shown in this to-do's chat (`.chat-draft.current`, not with the send sheet open) and scrolls it into view. It posts
   that draft's revision as `talk_ask_send`, with `read_aloud` on a phone or with the page hidden. The service checks
   the draft is ready, a kind that goes to people (`talk_live.SEND_KINDS`) and with its recipients set (no
   `to_options`), and keeps the question in memory: the revision, a digest of who, how and what
   (`talk_live.digest`), and the time. The voice gets the question naming who and how ("Send this reply to Lotte by
   email?"), to ask in the owner's language, after reading the draft out in full when `read_aloud` is set.
2. **The answer.** After the owner answers, the voice calls `send_answer`. The browser checks the same draft is still on
   screen, waits until the owner's words are kept (`talk_line`), then posts `talk_send`. The service reads its own
   record (`talk_lines` since the question): the voice's line that asked it (it must name the recipient), then the
   owner's next utterance. `talk_live.judge_answer` asks the model (`openclaw infer model run`, the background model)
   whether that answer clearly means yes, in any language, and accepts only one of three exact JSON answers; anything
   else, or no model, is `unclear`. The question is used up by any answer.
3. **The send.** A yes for an unchanged draft goes through `confirm_action` with source `voice` and approval
   `voice:<id>`, held `UNDO_SECONDS` (10) through the job's `retry_at`, so pacing and the outbox's checks before sending
   apply as for a tap. The chat shows **Approved by voice** with **Undo** while it waits (`talk_undo`,
   `Store.undo_voice_send`, which cancels the job). Otherwise the voice is told why nothing went: `no`, `unclear` (ask
   again), `changed` (the draft changed after the question: ask again), `not_asked` or `no_answer`.

One yes sends one draft: there is no "send all" by voice here. "Send without asking" settings are not touched.
`confirm_action` from the dashboard still only takes the owner's controls (an approval ID of their own); `voice:` comes
only from `talk_send`.

## Tests

`tests/test_talk_live.py` (the Gateway helper stubbed: status, start, a single offer, the limit, the transcript in the
chat, the tools, owner only, the secret never returned; by voice: a yes after the question sends one draft, with Undo;
a yes without a question, an unclear answer, a no, a changed draft and a question that doesn't name who all send
nothing; the judge accepts only exact JSON) and `tests/test_talk_live_dashboard.mjs` (a fake
`getUserMedia`, `RTCPeerConnection` and data channel; the same cases from the page, and Undo; screenshots at 390x844 and 1440x900, light and dark).
