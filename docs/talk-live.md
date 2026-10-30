# Talk live

A spoken conversation with The Machine in a to-do's chat, with OpenAI's Realtime voice. It can read the to-do and
look up other to-dos, hand a request to the to-do's chat (which follows its usual rules), and send its draft after
reading it out in full, a confirm question and a clear yes. **Talk** in the sidebar reaches the whole Machine. The help
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
3. On the data channel the dashboard sends `session.update` with the instructions, the tools, input transcription,
   noise reduction, the turn detection and the voice and speed; then a second one asking for the transcript's logprobs
   (`include`), alone, so a refusal leaves the rest in place. See [Hearing the owner](#hearing-the-owner).
4. What each side says (`conversation.item.input_audio_transcription.completed`, `response.output_audio_transcript.done`)
   is posted as `talk_line` (the voice's lines once their response is done, so an interrupted fragment isn't kept) and kept in `talk_lines`; the to-do's chat shows it after a **Talked live** line.
   A line of the owner's that is noise (`talkNoise`) isn't posted, and neither is the voice's reply to it.
5. **End**, leaving the chat, or 10 minutes end it (`talk_end`, `talk.client.close`). The timer warns a minute before.
   **Mute** turns the microphone track off.

At most one conversation per to-do and two in all. A session's secret is forgotten at its end, or 30 s after its limit.

## Tools

`talk_live.TOOLS`, called by the voice as Realtime function calls:

- `todo_details`: the to-do's title, state, its last 25 messages and who its drafts go to, through `talk_tool` (read
  only). Never a draft's text: `read_draft` reads one out (Sending by voice).
- `find_todos`: to-dos by words in their title, by `state`, or both (read only), each with its state in plain words
  (`talk_live.STATES`: ready, to decide, preparing, waiting on others, snoozed, looks done; `todo_state` places it the
  way the dashboard's lists do), what needs the owner first, at most 20, with `count`. Words that name a state and match
  no title ("anything preparing?") find that state. Closed ones (`talk_live.CLOSED`: done, dismissed) come from the
  Done / dismissed list (`Store.done_rows`, latest closed first) when asked for by state or by name, or when no open one
  matches.
- `create_todo`: a new to-do, handled in the browser (`talkCreate`) with New to-do's own `card_new` (title, then the
  note on the next line; Work or Personal as the list's filter, as New to-do). Nothing is sent and the focus stays. For
  anything new or about something else: `ask_chat` is only for the to-do in focus, and the instructions say so.
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
- `read_draft`, `ask_to_send`, `ask_to_send_all`, `send_answer` and `undo_send`: sending by voice, below. `do_it`,
  `undo_last_action` and `report_bug`: What Talk does itself, below.
- A doc write (`doc_write`, a new doc or an edit) counts as a
  draft here: the voice reads the whole change (`doc_writes.spoken`, every change before and after) and asks "Save these
  changes to “<doc>”?" or "Create this doc?". A change too long to read in full (over 4,000 characters) is refused by voice.

## Talk: the main conversation

**Talk** in the sidebar (`#side-talk`, in the drawer on a phone; shown once `talk_status` says ready) starts one
conversation that isn't tied to a to-do (`talk_start` with `main: true`, session key
`agent:main:assistant-talk-main`). One at a time; a to-do's own Talk live can run beside it (two in all).

- Tools (`talk_live.MAIN_TOOLS`): `list_todos` (the page's own: every open to-do the lists show, in their order: Ready,
  To decide, Preparing, Waiting on others, Later, Look done; at most 30, each with its id, state, title and who it's
  from, and `counts` per state), `open_todo` (the page shows that to-do in Talk's view, tells the Machine with `talk_focus`, and
  returns `todo_details`; a closed one too, even one the page hasn't loaded), then the same `todo_details`, `find_todos`
  (with ids here), `ask_chat`, `ask_to_send` and `send_answer`, `create_todo` and `end_talk`, and the tools in
  [The rest of the Machine](#the-rest-of-the-machine). Instructions: `talk_live.main_instructions` (the same voice and rules,
  plus going through the to-dos one by one: ready and to decide first, then in a few words how many are still
  preparing; one that is preparing can be opened, but has no draft to send yet). Replies are one or two sentences,
  without lists of options.
- Focus: the conversation works on the to-do on screen. The Machine keeps it (`Talk.focus`); `todo_details`,
  `talk_ask_send` and `talk_send` act on it only, and before one is open they refuse. When the owner opens another
  to-do, the page moves the focus there (`openChatLink`); a confirm question about the previous one is dropped, so a
  yes can only send the draft the voice read out. All the rules in [Sending by voice](#sending-by-voice) hold as they are.
- Talk's view (`#talk-view`, hash `#talk`): Talk opens its own page with one transcript for the whole conversation
  (kept in the page, `talkLog`), a small mark when it moves to another to-do, and a card on top with the to-do it's
  about (**Talking about**, its title, its current draft and **Open the chat**). The card stays in sight while the
  transcript scrolls. The draft shows whole, as a block that scrolls inside the card (up to `clamp(9.5em, 36dvh, 26em)`:
  a normal email reads on a phone with room left for the transcript); a line clamp there laid later lines over earlier
  ones. `open_todo` changes the card, never the page, so the owner isn't moved from chat to chat. The
  draft in the card, when it shows, is the one `ask_to_send` asks about, as in a chat (`.chat-draft.current`, its
  revision). `ask_chat`
  follows the chat in the background (`talkFollow`, `card_chat`) when it isn't open. After **End** the view keeps the
  transcript with **Start again**.
- Lines: `talk_line` keeps each line under the to-do in focus, so each to-do's chat shows what was said about it,
  after its own **Talked live** line. Lines before any to-do is open are kept with no to-do (not shown in a chat).
- The bar: at the bottom of Talk's view; in an open chat's message box; on any other page it floats at the bottom
  (`#talk-dock`). Leaving the view or a chat doesn't end Talk; **Talk** in the sidebar goes back to the view, and **T**
  ends it.
- New to-dos: a to-do that shows up in Ready or To decide while Talk is live is told to the voice as a system note
  (`talk_live.NEW_NOTE`), once, when neither side is talking (`response.done`, and 1.2 s after
  `input_audio_buffer.speech_stopped`). One that was preparing gets `talk_live.READY_NOTE` instead ("is ready now"),
  also once (`v.known`; `v.prep` remembers what was preparing). One Talk made itself (`create_todo`) isn't told, and
  the transcript gets a mark: **Added a to-do: …**.
- The bar's hint, **Say yes to send it.**, shows only while a send question is open (`ask_to_send` asked, not
  answered, under `ASK_SECONDS`); **Muted** while muted; otherwise none.
- Ending: when the owner clearly says they're done, the voice says one short goodbye and calls `end_talk` (also in a
  to-do's own Talk live). The page sends no new response, waits until the goodbye has played
  (`output_audio_buffer.stopped`, at most 10 s), then ends as **End** does.

## The rest of the Machine

Talk can reach what the dashboard shows, not only the to-dos. Read tools answer from the stores and views the pages
already read (`App.talk_machine_tool`, `talk_live.MACHINE_TOOLS`, main conversation only), short and with ids:

- `search` (`words`, `kind`: anything, person, organization, project, message, meeting, promise): the Graph's search
  (`graph_find`), Events (the `events` action, meetings by `calendar.event`, messages by meaning) or open promises.
- `open_record` (`id`): one person, organization or project (`graph_action`: who, when you last talked, open to-dos,
  recent lines), a meeting (`Store.meeting`, what the Calendar shows, not the invite's notes), a message or a promise
  (`promise_page`). Its `card` is the page's: Talk's transcript shows it as a small card linking to its page or opening
  the meeting or message. The to-do in focus stays.
- `calendar` (`day`, `days` up to 14): meetings from `Store.calendar` in the owner's time zone, at most 25.
- `machine_status` (the page's own): each connection's health as Connections shows it (`connectorHealth`), the
  reviews, and what **Needs you** lists.

Doing things:

- `todo_action` (the page's own, `talkDo`): what a to-do's buttons do, through the same actions and the same checks
  (`decide`, through `decideOrWait` for the outbox's choices, and `card_rename`): `mark_done` (complete), `dismiss`
  (reject, with `why`), `snooze` (`snooze` option or `snooze_until`), `unsnooze` (accept on a snoozed one), `reopen`
  (as the Done / dismissed list: `reopen` for a done one, `undo` inside the undo window; one dismissed longer ago can't
  come back, as on the page), `rename`, `do_it` (accept on one that waits for a decision), `try_again` (retry when
  preparing is stuck) and `not_done` (one that looks done). Each only where the page offers it. Never a send.
- `ask_machine` (`talkMachine`): anything else. It makes a new to-do the way New to-do does (`card_new`) and hands the
  request to that to-do's chat as a decision `other` whose id starts with `talk_live.ASK_PREFIX`, shown there as the
  owner's message. The chat's prompt gets `RELAY_NOTE` and `ASK_MACHINE_NOTE`: do it now, look things up, change the
  Graph, snooze or mark to-dos done, never send, and mark this to-do done when nothing is left. The page follows that
  chat (`talkWatch`) and tells the voice its answer (`DONE_NOTE`, or `STOPPED_NOTE`). The to-do in focus is never used
  for it.

The instructions (`# The rest of the Machine`) say to use the direct tool when one fits, never to guess about someone
before looking them up, and to use `ask_machine`, never `ask_chat`, for anything not about the to-do in focus.

## In the background

Talk keeps going when the page isn't on screen, on computers and on Android (Chrome or the installed app):

- The screen stays on while it is live (`navigator.wakeLock.request('screen')`), taken again when the page shows again
  and let go at the end.
- The Media Session shows it on the lock screen or in the notification (**Talk**, The Machine, the app icon): pause and
  play mute and unmute, stop and hang up end it (`setMicrophoneActive` follows Mute where it exists). The voice plays
  through an audio element, so Android shows the controls.
- Browsers slow timers in the background, so what happens at a moment runs on the voice's own events
  (`talkDue` on each one: the goodbye heard, the limit from the wall clock) and when the page shows again; `talkTick` is
  a backstop.
- Back on screen it checks the connection, the data channel and the microphone. One that went away while hidden ends
  cleanly with **Talk stopped while in the background.** and **Start again**. On an iPhone the microphone stops when the
  app leaves the screen, and it ends the same way.

Where a browser has none of this, nothing changes.
- Limit: 30 minutes (`MAIN_LIMIT_SECONDS`), a warning a minute before. OpenAI allows a Realtime session up to 60
  minutes; 30 keeps an API key's per-minute cost bounded.


`talk_voice` in the voice settings picks the Realtime voice (`voice_input.TALK_VOICES`), passed to
`talk.client.create`. The default is `cedar`. ChatGPT's Cove isn't offered on `gpt-realtime` models (only on the
ChatGPT-only `gpt-live-1-codex` route, where the Gateway owns the tools), so `cedar` is the closest. Settings plays a
short sample for each, `brand/voices/<voice>.mp3`, recorded once from the Realtime API.

OpenAI recommends `marin` and `cedar` for best quality; `cedar` stays the default. The page sets
`audio.output.speed` to `talk_live.SPEED` (1.1, a little quicker than OpenAI's 1.0: 0.95 sounded slow) in its `session.update`:
`talk.client.create` takes no speed. Speed only changes playback, so how the voice talks is in
`talk_live.instructions`, laid out as OpenAI's Realtime prompting guide suggests: labeled sections (personality and tone,
length, pacing, variety, speaking not reading) before the rules, which are unchanged. It talks in short, warm turns with
contractions, varies its openers, says what a to-do is about instead of reading its title, and never reads out lists or
links, except a draft it is asked to read in full before a send question. A plain acknowledgment ("okay", "all
right") gets a word at most, or nothing; before a tool it says one short line at most, once. One reply per turn, said
once, never a second one restating it; no em or en dashes (the page also turns any into a comma in the transcript);
when the chat's answer comes (`DONE_NOTE`) it says what is new once and doesn't repeat what it already told the owner.

Turn detection: the Gateway's `talk.client.create` sets `server_vad` (silence only) and takes no other kind, so the page
sets `audio.input.turn_detection` to `talk_live.TURN` in its `session.update`: `semantic_vad` with `eagerness: low`.
It judges from the words whether the owner has finished, so a short filler or a pause mid-thought doesn't start a reply.
OpenAI's [VAD guide](https://developers.openai.com/api/docs/guides/realtime-vad): "low will let the user take their time
to speak".

## Hearing the owner

With auto-detection, a rustle or a breath was written down as Korean ("음력?"), Thai ("แก") or a made-up word, and the
voice answered it ("Right."). Now:

- **Their languages.** `talk_start` gets the browser's `navigator.languages`; `talk_live.spoken` takes the UI language,
  Voice input's language (Settings), the locale's and the browser's, those the app speaks, at most three (English when
  none fits). `talk_live.transcription` pins `language` when there is one (OpenAI: better accuracy and latency). With
  several it names them in the `prompt` instead: `language` takes one code, and pinning English turns a Dutch sentence
  into a wrong transcript. The model is `gpt-4o-transcribe` (`talk_live.TRANSCRIBE_MODEL`). A second `session.update`
  of its own then asks for `gpt-transcribe` (`talk_live.transcription_next`, OpenAI's newest, $0.0045 a minute) with
  every language in `languages`, which pins them all; it is documented for WebSocket sessions, so a session that refuses
  it keeps `gpt-4o-transcribe` and nothing else changes. When it says which language it heard (`languages` on the
  transcript) and that isn't one of the owner's, the line is dropped as below. `gpt-realtime-2.1` itself doesn't write
  down what the owner said: transcription is always a separate model. Dictation (Voice input) stays
  `openai/gpt-4o-transcribe` through OpenClaw, whose catalog has nothing newer, with Whisper on the Machine offline. The instructions name the languages and say a noise, a cut-off word or a few
  words in another language get no answer.
- **Noise reduction.** `audio.input.noise_reduction` is `talk_live.NOISE`, `far_field` (a phone in the hand or on the
  table, or a laptop; `near_field` is for a headset). It cleans the audio before turn detection and the model hear it,
  so fewer noises start a turn. Turn detection stays `semantic_vad` with `eagerness: low` (it has no threshold to raise).
- **Dropping noise** (`talkNoise`, `talkHeard` in `dashboard/todos-chat.js`). A transcript is noise when it has no
  letters or digits, when most of its letters aren't Latin script (every app language writes in it), when it is the
  transcription prompt echoed back, or when it is three words or fewer and its average logprob is under -1.2. A noise
  line isn't shown or kept, its item is deleted from the conversation (`conversation.item.delete`), and a reply the
  voice is still giving to it is cancelled (`response.cancel`, `output_audio_buffer.clear`). The page knows which reply
  answers which words (`input_audio_buffer.committed`, then `response.created`); a reply that ends before its words are
  written down waits for them (at most 4 s) and is dropped with them.
- **Short answers always pass.** "yes", "no", "ok", "send it", "stop", "undo", "ja", "nee", "doe maar" and the like
  (`TALK_SHORT`, three words or fewer) are never noise, however unsure the transcript.
- **Another language** (`talkForeign`). A few words with marker words of only an app language the owner doesn't speak
  ("Ja, liebe den Movon." for someone speaking English and Dutch) are dropped like noise, and the voice says only
  "Sorry, say that again?" (`talk_live.AGAIN_NOTE`). So is a line with a letter none of their languages writes
  (`TALK_LETTERS`: "Güzel." for English and Dutch) and no word of their own ("Send it to José." stays).
- **No dashes.** The instructions forbid em dashes; `talkNoDash` replaces any left in either side's transcript.

## Sending by voice

The rule is the same as for a tap: only what the owner has seen or heard, and approved. It works without the screen: a
phone in a pocket, another page, or Talk's view without the card.

1. **Hearing the draft.** `todo_details` never carries a draft's text, so the voice can't read one out on its own (it
   once did, and then the send read it again). "Read it to me" is `read_draft`: the browser posts `talk_ask_send` with
   `read: true`, the Machine pins the revision and records the reading (`Talk.reading`), and the voice reads the full
   draft out word for word.
2. **The question.** The owner asks to send. `ask_to_send` (browser, `talkAskSend`) posts `talk_ask_send`: with the
   revision of the draft that shows (this to-do's `.chat-draft.current`, in its chat or Talk's card), else none, and
   then the Machine picks the to-do's only draft, or asks which by number when there are several (`draft`). The service
   checks the draft is ready, a kind that goes to people (`talk_live.SEND_KINDS`) and with its recipients set (no
   `to_options`), and pins it: the revision, a digest of who, how and what (`talk_live.digest`), and the time. When
   the owner has already **seen** this revision (`draft_seen`, below) or **heard** it (read out in this session: the
   voice's lines since the reading hold most of its words, `talk_live.read_out`), the voice only asks the question
   ("Send it to Nick at DragApp?"). Otherwise it gets the whole draft to read out first. The same pinned revision is
   never read twice.
3. **The answer.** After the owner answers, the voice calls `send_answer`. The browser waits until the owner's words
   are kept (`talk_line`, up to about 10 s), then posts `talk_send`. The service reads its own record (`talk_lines`
   since the question): the voice's line that asked it (it must name the recipient), then the owner's last line, which
   must be a clear yes in the owner's languages (`talk_live.clear_answer`): every word from a short list of yes words
   and fillers (`talk_live.YES`: "yes", "yeah", "ok, send it", "go ahead", "ja", "ja hoor", "doe maar", "verstuur
   maar", "please", the recipient's name…), no negation, no question. "Jasne.", "Ja, ist gut, das endet." or "yes, but
   change the date" send nothing. `no` drops the question; `unclear` keeps it open and the voice asks again in a few
   words ("Say yes to send it to Dana."), without reading the draft again. The question expires after `ASK_SECONDS`
   (3 minutes) and is dropped when the focus moves. While it is open, turn detection runs at `eagerness: high`
   (`talkEager`), so a lone "yes" ends the turn at once.
4. **The send.** A yes for the pinned draft, unchanged, goes through `confirm_action` with source `voice` and its own
   approval `voice:<id>`, held `UNDO_SECONDS` (10) through the job's `retry_at`, so pacing and the outbox's checks
   apply as for a tap. Talk's bar shows **Sending in 10 s** with **Undo**, then **Sent** (or **Canceled. It won’t be
   sent.**); the chat shows **Approved by voice** with **Undo**. Both use `talk_undo` (`Store.undo_voice_send`). Saying
   "undo", "stop", "wait" or "don't send" calls `undo_send`, which cancels every send of that yes. A changed draft is
   refused (`changed`) and read out again; one never shown or read is refused too (`not_read`).

**Seen on screen** (`draftSeenTick` in `dashboard/todos-chat.js`): a draft on its to-do, in its chat or on Talk's card
that showed in full for 1.5 s (top and end on screen, not cut short by Show more, its own scroll box scrolled to the end)
is posted as `draft_seen` with the text it showed. The Machine keeps it (`draft_seen` table: suggestion, revision and
digest) only when that text matches the current draft (`Assistant.draft_seen`); a changed draft has a new digest and
counts as unseen.

**Several at once** (main Talk only): "send all the ready follow-ups" or "send both" is `ask_to_send_all` with at most
5 to-do ids. One question names every recipient ("Send all 3, to Dana, Sam and Nick?"); only unseen drafts are read
out, and the answer waits until they have been. One clear yes sends each with its own pinned revision and approval,
and Undo in Talk cancels all of them.

"Send without asking" settings are not touched. `confirm_action` from the dashboard still only takes the owner's
controls (an approval ID of their own); `voice:` comes only from `talk_send`.

## What Talk does itself

- **Do it vs done.** "Do it", "go ahead and do it", "handle it", "start it" are `do_it` (`talkDoIt`): the to-do's own
  **Do it** (`decide accept`, or `retry` when stuck), which starts The Machine's job, browser work included; the voice
  says it started and that it can be followed on the to-do. "Mark it done", "it's done", "I did it" are
  `todo_action mark_done`. A job already running is left to run. A draft waiting goes through `ask_to_send`.
- **Corrections.** Talk keeps the last action it took (`v.last`: to-do, action, title). "No, I meant…" right after is
  `undo_last_action`: the action is taken back on that to-do (reopen, unsnooze, the old title), which opens again, and
  the voice says what it undid before doing what was meant. "Do this and move on" moves on only after the tool said ok.
- **Navigation.** "Next one", "move on", "previous", "go back", "stop", "leave it" are Talk's own (`list_todos`,
  `open_todo`, nothing). `ask_chat` refuses them (`TALK_NAV`), so they never reach a chat: "move on to the next one"
  once had a payroll to-do's chat research the next to-do. `ask_chat` carries a clean instruction about the focused
  to-do, and `RELAY_NOTE` tells the chat to work on that to-do only. "Continue" on a to-do not started is its Do it.
- **Chat answers.** The answer is told with the to-do's title (`DONE_NOTE`). A to-do closed or snoozed meanwhile (by
  Talk or on screen) drops what its chat was on, silently, also after a reopen. A chat that stopped on its own is told
  once (`STOPPED_NOTE`, with what was asked, so "ask again" asks that again with `ask_chat`, never `create_todo`).
- **Report a bug.** "Report a bug" or "send feedback" is `report_bug` (`talkBug`), never a to-do. It sends the same
  report as Help's **Report a bug** (`bug_send`, or the hosted path): "From Talk: " and the owner's words. The to-do
  in focus and the last 8 Talk lines go only when the owner agreed (`context`), the support report only when they
  agreed (`support_report`), the voice asks once. It says "Sent the bug report." and never that it is being looked into.
- **In a to-do's own Talk** (the wave in its chat): `todo_action` (mark done, dismiss, snooze, reopen; that to-do only)
  and `undo_last_action` too. "Mark this as done" is the owner's own decision, so Talk marks it done itself, with the
  to-do's usual undo, instead of handing it to the chat (which only offered **Mark done** buttons). The chat stays open.
- **Unclear words.** Before `create_todo`, `todo_action`, `do_it`, `undo_last_action`, `report_bug` or `ask_machine`,
  the page checks the owner's last words: a dropped noise, or one odd word ("Azk."), returns "Sorry, say that again?"
  and nothing is done. `end_talk` is checked the same way: a sound or one odd word is never a goodbye or a wrap-up
  ("Güzel." once ended a to-do's Talk). The instructions say never to claim an action no tool result confirmed.

## Tests

`tests/test_talk_live.py` (the Gateway helper stubbed: status, start, a single offer, the limit, the transcript in the
chat, the tools, owner only, the secret never returned; by voice: a yes after the question sends one draft, with Undo;
ending itself after a goodbye, the turn detection; a yes without a question, an unclear answer, a no, a changed draft and a question that doesn't name who all send
nothing; only a clear yes in the owner's languages counts; read once, then a yes sends without a second reading; a changed draft is read again; a draft seen on screen sends without reading; a batch of 3 with one unseen, and Undo cancelling it) and `tests/test_talk_live_dashboard.mjs` (a fake
`getUserMedia`, `RTCPeerConnection` and data channel; the same cases from the page, and Undo; screenshots at 390x844 and 1440x900, light and dark).
`tests/test_talk_hearing_dashboard.mjs` covers hearing the owner and the card: the session's transcription, noise reduction, turns, speed and
logprobs; what counts as noise (Korean, Thai, marks only, an unsure made-up word; a Dutch or French sentence and a short yes count); a noise
line dropped with the voice's reply to it (cancelled, or waiting for its words), a Dutch turn kept; no em dashes in the voice's lines; and a whole
email draft in the card with no line box overlapping another, at the top and scrolled to its end, tall enough and with room for the transcript
(390x844 and 1440x900, light and dark). `tests/test_talk_main_dashboard.mjs` covers Talk: the sidebar entry, the floating bar, Talk's view, listing and opening to-dos (the
card changes, the page doesn't; **Open the chat** and back), a send by voice about the to-do on screen, a new to-do told at a pause, following the owner to
another to-do, its 30-minute limit (its toast only then), End, **Start again** and `end_talk` (the goodbye kept in the transcript); a person and a meeting looked up
and shown as cards, `machine_status`, `ask_machine` (its own to-do, its answer back to the voice), the to-do actions and reopening a dismissed one; in the background
(mocked Wake Lock, Media Session, visibility and frozen timers): the lock screen's controls, the goodbye and the limit on events, and a clean end when the connection or
the microphone went away (390x844 and 1440x900, light and dark). `tests/test_talk_live.py` also covers search, records and the calendar, done and dismissed
to-dos, and sending without the screen: the pinned revision, a draft picked by number, a changed draft and an expired question.
`tests/test_talk_actions_dashboard.mjs` covers what Talk does itself: "do it" is Do it (not done, a running one left alone), a correction
reopens the to-do the last action touched, "next one" and "stop" never reach a chat and "let it continue" starts Do it, a dismissed to-do's
chat says nothing when it stops while one that stops on its own is told once, one odd word changes nothing, a short unsure "yes" is kept and
German words get "say that again", no dashes, `report_bug` with and without context, and Undo in Talk with its countdown for a batch,
tapped or said, then **Sent**; in a to-do's own Talk, "Güzel." dropped and never an end, and "mark this as done" marking it done with the chat
still open (390x844 and 1440x900, light and dark).
