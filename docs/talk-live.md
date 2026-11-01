# Talk live

A spoken conversation with The Machine, with OpenAI's Realtime voice. There are two kinds:

- **Talk live in a to-do's chat** (the wave next to the mic): about that one to-do. It reads the to-do, looks up other
  to-dos, hands a request to the to-do's chat, and sends the draft after reading it out, a confirm question and a clear
  yes.
- **Talk** in the sidebar: one conversation that goes through the to-dos and reaches the rest of the Machine.

The help article is [docs/help/talk-live.md](help/talk-live.md). The code is `talk_live.py` (the service side),
`talk-live-run.mjs` (the Gateway helper) and the `talk*` functions in `dashboard/todos-chat.js`.

## Who can use it

OpenAI has to be set up in OpenClaw. The Gateway (`talk.catalog`) says whether its OpenAI realtime provider is configured
and can open a browser session. Only then does the wave show, and Settings, General, Voice input says whether Talk is
ready.

- **A ChatGPT sign-in** (the Codex OAuth profile): the Gateway mints the session through its broker, and the offer goes
  to the Gateway's own `/plugins/openai/realtime/calls` (single-use, 60 s). OpenClaw's docs say this works "when the
  account has access". No cost note is shown.
- **An OpenAI API key**: an ephemeral client secret from OpenAI; the offer goes to
  `https://api.openai.com/v1/realtime/calls`. OpenAI bills the key per minute, so the bar shows one short line saying so.

When both are set up, OpenClaw uses the key.

**The model** is OpenAI's GA `gpt-realtime-2.1`, not GPT-Live (`gpt-live-1`, `gpt-live-1-codex`). With GPT-Live the
Gateway owns the tools and its own agent, and a spoken "yes" could confirm a high-impact action as that agent sees fit.
Here the dashboard sets its own tools, and a spoken yes counts only under [Sending by voice](#sending-by-voice).

## How a conversation runs

1. **Start.** `talk_start` (owner, dashboard only) asks the Gateway for a session (`talk.client.create`, scopes
   `operator.read` and `operator.talk` only, never `operator.write`) for the session key
   `agent:main:assistant-talk-<to-do id>`. The service keeps the session's secret in memory and returns an ID, the tools,
   the instructions (the to-do's title, the dashboard language, the time), the voice and the speed. The secret and the
   key never reach the browser.
2. **Connect.** The browser opens the microphone, makes a WebRTC offer with an `oai-events` data channel and posts it as
   `talk_offer`. The service hands it on once, with the secret, and returns OpenAI's answer. The dashboard's CSP keeps
   `connect-src 'self'`; the audio goes directly between the browser and OpenAI.
3. **Set up.** On the data channel the dashboard sends `session.update` with the instructions, tools, input
   transcription, noise reduction, turn detection, voice and speed. A second one asks for the transcript's logprobs on
   its own, so a refusal leaves the rest in place.
4. **Keep the transcript.** What each side says is posted as `talk_line` and kept in `talk_lines`. The voice's lines are
   posted once their response is done, so an interrupted fragment isn't kept. The to-do's chat shows them after a
   **Talked live** line. A line of the owner's that is noise isn't posted, and neither is the voice's reply to it.
5. **End.** **End**, leaving the chat, or the limit ends it (`talk_end`, `talk.client.close`), with a warning a minute
   before. **Mute** turns the microphone track off.

**Limits.** 10 minutes for a to-do's Talk live (`LIMIT_SECONDS`), 30 minutes for Talk (`MAIN_LIMIT_SECONDS`; OpenAI
allows 60, and 30 keeps an API key's cost bounded). At most one conversation per to-do and two in all. A session's secret
is forgotten at its end, or 30 s after its limit.

OpenAI's server-side turn detection lets the owner interrupt: the voice stops and listens.

## How it sounds

- **Voice.** `talk_voice` in Settings picks the Realtime voice (`voice_input.TALK_VOICES`), passed to
  `talk.client.create`. The default is `cedar`, which OpenAI recommends with `marin` for quality. ChatGPT's Cove isn't
  offered on `gpt-realtime` models. Settings plays a short sample of each (`brand/voices/<voice>.mp3`).
- **Speed.** `audio.output.speed` is `talk_live.SPEED` (1.1), set in the page's `session.update` since
  `talk.client.create` takes no speed.
- **Style.** `talk_live.instructions` follows OpenAI's Realtime prompting guide: labeled sections (personality and tone,
  length, pacing, variety, speaking not reading) before the rules. Short, warm turns with contractions; it says what a
  to-do is about instead of reading its title, and never reads out lists or links, except a draft before a send
  question. An "okay" gets a word at most. Before a tool it says one short line at most. One reply per turn, never a
  second one restating it. When the chat's answer comes it says what is new, once.
- **No dashes.** The instructions forbid em and en dashes, and `talkNoDash` turns any left into a comma in the
  transcript.
- **Turns.** The Gateway sets `server_vad` (silence only), so the page sets `audio.input.turn_detection` to
  `talk_live.TURN`: `semantic_vad` with `eagerness: low`. It judges from the words whether the owner has finished, so a
  filler or a pause mid-thought doesn't start a reply. While a send question is open it runs at `eagerness: high`
  (`talkEager`), so a lone "yes" ends the turn at once.

## Tools in a to-do's Talk live

`talk_live.TOOLS`, called by the voice as Realtime function calls:

- `todo_details`: the to-do's title, state, last 25 messages and who its drafts go to (read only, through `talk_tool`).
  Never a draft's text: `read_draft` reads one out.
- `find_todos`: to-dos by words in their title, by `state`, or both, each with its state in plain words
  (`talk_live.STATES`: ready, to decide, preparing, waiting on others, snoozed, looks done), what needs the owner first,
  at most 20, with `count`. Words that name a state and match no title ("anything preparing?") find that state. Done and
  dismissed ones (`talk_live.CLOSED`) come from the Done / dismissed list when asked for by state or name, or when no
  open one matches.
- `create_todo`: a new to-do, made in the browser (`talkCreate`) with New to-do's own `card_new`. Nothing is sent and the
  focus stays. For anything new or about something else; `ask_chat` is only for the to-do in focus.
- `ask_chat`: hands a request to the to-do's chat ([Chat hand-offs](#chat-hand-offs)).
- `todo_action` and `undo_last_action`: mark done, dismiss, snooze, reopen (that to-do only), and take the last one back
  ([What Talk does itself](#what-talk-does-itself)).
- `read_draft`, `ask_to_send`, `send_answer`, `send_status`, `undo_send`: [Sending by voice](#sending-by-voice).
- `report_bug` and `end_talk`.

A doc write (`doc_write`, a new doc or an edit) counts as a draft: the voice reads the whole change
(`doc_writes.spoken`) and asks "Save these changes to “<doc>”?" or "Create this doc?". A change over 4,000 characters
is refused by voice.

### Chat hand-offs

`ask_chat` (`talkAsk`) sends the request to the to-do's chat as a decision `other` (`decideOrWait`, so it can also wait
offline) whose id starts with `talk_live.RELAY_PREFIX`.

- The hand-off is invisible: `card_chat` leaves it out, so the chat shows only what the owner said and **Working on
  it…**.
- The preparation gets `talk_live.RELAY_NOTE`: look it up on the web or in the browser when needed, answer in two or
  three plain sentences, say where it was found, and work on this to-do only. The chat's own rules hold: it can change
  the draft, snooze or mark the to-do done, never send.
- One hand-off runs at a time. An ask while the chat is busy waits in the browser (`v.queue`) and goes once the turn
  ends.
- When the turn ends (`chatPoll`, or `talkTick` as a backstop), the browser sends the chat's reply to the session as a
  system message (`DONE_NOTE`, with the to-do's title, or `STOPPED_NOTE`) with `response.create`, so the voice says it at
  once. If the voice is speaking, the note waits for `response.done`. The voice never polls.
- A to-do closed or snoozed meanwhile drops what its chat was on, silently, also after a reopen. A chat that stopped on
  its own is told once, with what was asked, so "ask again" asks that again.
- Navigation words ("next one", "move on", "go back", "stop", "leave it") are refused by `ask_chat` (`TALK_NAV`), so
  they never reach a chat.

## Talk: the main conversation

**Talk** in the sidebar (`#side-talk`, in the drawer on a phone; shown once `talk_status` says ready) starts one
conversation not tied to a to-do (`talk_start` with `main: true`, session key `agent:main:assistant-talk-main`). One at
a time; a to-do's own Talk live can run beside it.

**Tools** (`talk_live.MAIN_TOOLS`):

- `list_todos` (the page's own): every open to-do in the order the lists show (Ready, To decide, Preparing, Waiting on
  others, Later, Look done), at most 30, each with its id, state, title and who it's from, and `counts` per state.
- `open_todo`: the page shows that to-do in Talk's view, tells the Machine (`talk_focus`) and returns `todo_details`; a
  closed one too, even one the page hasn't loaded.
- The to-do tools above, about the to-do in focus (`find_todos` with ids here), plus `ask_to_send_all`.
- The tools in [The rest of the Machine](#the-rest-of-the-machine).

**Instructions** (`talk_live.main_instructions`): the same voice and rules, plus going through the to-dos one by one:
ready and to decide first, then in a few words how many are still preparing. Replies are one or two sentences, without
lists of options.

**Focus.** The conversation works on the to-do on screen. The Machine keeps it (`Talk.focus`); `todo_details`,
`talk_ask_send` and `talk_send` act on it only and refuse before one is open. When the owner opens another to-do, the
focus moves there (`openChatLink`) and a confirm question about the previous one is dropped.

**Talk's view** (`#talk-view`, hash `#talk`):

- One transcript for the whole conversation (`talkLog`), with a small mark when it moves to another to-do.
- A card on top: **Talking about**, the to-do's title, its current draft (whole, from its first line) and **Open the
  chat**. It scrolls with the page, so it never covers a line. After a send by voice it shows **Sent to Sam · 11:42**
  instead of the draft.
- `open_todo` changes the card, never the page. `ask_chat` follows the chat in the background (`talkFollow`).
- After **End** the view keeps the transcript with **Start again**.

**Lines.** `talk_line` keeps each line under the to-do in focus, so each to-do's chat shows what was said about it.
Lines before any to-do is open are kept with no to-do.

**The bar.** At the bottom of Talk's view, in an open chat's message box, and floating on any other page (`#talk-dock`).
Leaving the view doesn't end Talk; **Talk** in the sidebar goes back, and **T** ends it. Its hint, **Say yes to send
it.**, shows only while a send question is open; **Muted** while muted.

**New to-dos.** One that shows up in Ready or To decide is told to the voice once (`talk_live.NEW_NOTE`), when neither
side is talking (`response.done`, and 1.2 s after `input_audio_buffer.speech_stopped`). One that was preparing gets
`READY_NOTE` ("is ready now"). One Talk made itself isn't told; the transcript gets **Added a to-do: …**.

**Ending.** When the owner clearly says they're done, the voice says one short goodbye and calls `end_talk` (also in a
to-do's own Talk live). The page waits until the goodbye has played (`output_audio_buffer.stopped`, at most 10 s), then
ends as **End** does.

## The rest of the Machine

In the main conversation Talk reaches what the dashboard shows. Read tools answer from the stores and views the pages
already read (`App.talk_machine_tool`, `talk_live.MACHINE_TOOLS`), short and with ids:

- `search` (`words`, `kind`: anything, person, organization, project, message, meeting, promise): the Graph's search,
  Events (meetings by `calendar.event`, messages by meaning) or open promises.
- `open_record` (`id`): a person, organization or project (who, last contact, open to-dos, recent lines), a meeting (what
  the Calendar shows, not the invite's notes), a message or a promise. The transcript shows it as a small card linking
  to its page. The to-do in focus stays.
- `calendar` (`day`, `days` up to 14): meetings in the owner's time zone, at most 25.
- `machine_status` (the page's own): each connection's health as Connections shows it, the reviews, and what **Needs
  you** lists.

Doing things:

- `todo_action` (the page's own, `talkDo`): what a to-do's buttons do, through the same actions and checks: `mark_done`,
  `dismiss` (with `why`), `snooze`, `unsnooze`, `reopen` (as the Done / dismissed list does), `rename`, `do_it`,
  `try_again` and `not_done`. Each only where the page offers it. Never a send.
- `ask_machine` (`talkMachine`): anything else. It makes a new to-do the way New to-do does and hands the request to that
  to-do's chat (id prefix `talk_live.ASK_PREFIX`), shown there as the owner's message. The chat gets `RELAY_NOTE` and
  `ASK_MACHINE_NOTE`: do it now, look things up, change the Graph, snooze or mark to-dos done, never send, and mark this
  to-do done when nothing is left. The page follows that chat (`talkWatch`) and tells the voice its answer. The to-do in
  focus is never used for it.

The instructions say to use the direct tool when one fits, never to guess about someone before looking them up, and to
use `ask_machine`, never `ask_chat`, for anything not about the to-do in focus.

## In the background

Talk keeps going when the page isn't on screen, on computers and on Android (Chrome or the installed app):

- The screen stays on while it is live (`navigator.wakeLock`), taken again when the page shows again.
- The Media Session shows it on the lock screen or in the notification: pause and play mute and unmute, stop and hang up
  end it. The voice plays through an audio element, so Android shows the controls.
- Browsers slow timers in the background, so timed steps run on the voice's own events (`talkDue`: the goodbye heard,
  the limit from the wall clock) and when the page shows again. `talkTick` is a backstop.
- Back on screen it checks the connection, the data channel and the microphone. One that went away ends cleanly with
  **Talk stopped while in the background.** and **Start again**. On an iPhone the microphone stops when the app leaves
  the screen, and it ends the same way.

Where a browser has none of this, nothing changes.

## Hearing the owner

Without these steps, a rustle or a breath could be written down as another language or a made-up word, and the voice
answered it.

- **Their languages.** `talk_start` gets the browser's `navigator.languages`. `talk_live.spoken` takes the UI language,
  Voice input's language, the locale's and the browser's, those the app speaks, at most three (English when none fits).
  `talk_live.transcription` pins `language` when there is one; with several it names them in the `prompt` instead.
- **Transcription models.** `gpt-4o-transcribe` (`TRANSCRIBE_MODEL`) first. A second `session.update` then asks for
  `gpt-transcribe` (`transcription_next`) with every language in `languages`. A session that refuses it keeps
  `gpt-4o-transcribe`. `gpt-realtime-2.1` itself doesn't transcribe the owner. Dictation is separate
  ([Voice input](voice.md)).
- **Noise reduction.** `audio.input.noise_reduction` is `talk_live.NOISE`, `far_field` (a phone or a laptop), so fewer
  noises start a turn.
- **Dropping noise** (`talkNoise`, `talkHeard`). A transcript is noise when it has no letters or digits, when most of its
  letters aren't Latin script, when it is the transcription prompt echoed back, or when it is three words or fewer with
  an average logprob under -1.2. A noise line isn't shown or kept, its item is deleted (`conversation.item.delete`), and a
  reply to it is canceled (`response.cancel`, `output_audio_buffer.clear`). A reply that ends before its words are
  written down waits for them (at most 4 s).
- **Short answers always pass.** "yes", "no", "ok", "send it", "stop", "undo", "ja", "nee" and the like (`TALK_SHORT`)
  are never noise.
- **Another language** (`talkForeign`). A few words with marker words of only an app language the owner doesn't speak
  are dropped, and the voice says only "Sorry, say that again?" (`AGAIN_NOTE`). So is a line with a letter none of their
  languages writes (`TALK_LETTERS`) and no word of their own. `languages` on the transcript (read by `talkLang`) drops a
  line in a language that isn't theirs.
- **Never a loop.** The first line that doesn't come through gets "Sorry, say that again?". A second in a row, or a
  failed transcription, gets one plain line (`UNHEARD_NOTE`: check the microphone or type in the chat). Then it stays
  quiet until a line comes through (`talkMiss`).

## Sending by voice

The rule is the same as for a tap: only what the owner has seen or heard, and approved. It works without the screen.

1. **Hearing the draft.** `todo_details` never carries a draft's text. "Read it to me" is `read_draft`: the browser posts
   `talk_ask_send` with `read: true`, the Machine pins the revision and records the reading (`Talk.reading`), and the
   voice reads the draft out word for word.
2. **The question.** `ask_to_send` (`talkAskSend`) posts `talk_ask_send` with the revision of the draft on screen, if
   any; else the Machine picks the to-do's only draft, or asks which by number. The service checks the draft is ready, of
   a kind that goes to people (`SEND_KINDS`), with its recipients set, and pins it: the revision, a digest of who, how and
   what (`talk_live.digest`), and the time. When the owner has already seen or heard this revision, the voice only asks
   ("Send it to Sam at Acme?"). Otherwise it reads the draft first. The same revision is never read twice.
3. **The answer.** The voice calls `send_answer`. The browser waits until the owner's words are kept (`talk_line`, up to
   about 10 s), then posts `talk_send`. The service reads its own record: the voice's line that asked (it must name the
   recipient), then the owner's last line, which must be a clear yes in their languages (`talk_live.clear_answer`: only
   words from `talk_live.YES`, no negation, no question). "yes, but change the date" sends nothing. `no` drops the
   question; `unclear` keeps it open and the voice asks again in a few words. The question expires after `ASK_SECONDS`
   (3 minutes) and is dropped when the focus moves.
4. **The send.** A yes for the pinned, unchanged draft goes through `confirm_action` with source `voice` and its own
   approval `voice:<id>`, held `UNDO_SECONDS` (10) through the job's `retry_at`, so pacing and the outbox's checks apply as
   for a tap. `talk_send` returns the seconds really left (`undo_ms`), so the voice ("Sending in 10 seconds. Say undo to
   stop it.") and the bar's countdown agree.
5. **Undo.** The bar shows **Sending to Sam in 10 s** (a batch: **Sending 3 emails in 10 s**) with **Undo**; the chat
   shows **Approved by voice** with **Undo**. Saying "undo", "stop", "wait" or "don't send" calls `undo_send`. Both use
   `talk_undo` (`Store.undo_voice_send`) and cancel every send of that yes: **Canceled. It won’t be sent.**
6. **Is it sent?** After the window the bar shows **Sending…** and follows the outbox (`talkSentWatch`) until the job
   settles: **Sent to Sam · 11:42** (the voice says only "Sent.", `SENT_NOTE`), or **Didn’t go out.** with why
   (`NOT_SENT_NOTE`). `send_status` reads the latest outbox job (`Assistant.talk_send_status`): waiting, sending, sent,
   failed, blocked, canceled, unsure or none. The voice says what it returns and never guesses.

A changed draft is refused (`changed`) and read out again; one never shown or read is refused too (`not_read`).

**Seen on screen** (`draftSeenTick`): a draft that showed in full for 1.5 s (top and end on screen, not cut short by Show
more, its own scroll box scrolled to the end) is posted as `draft_seen` with the text it showed. The Machine keeps it
(`draft_seen` table) only when that text matches the current draft; a changed draft counts as unseen.

**Heard** means read out in this session: the voice's lines since the reading hold most of its words
(`talk_live.read_out`).

**Several at once** (Talk only): "send all the ready follow-ups" is `ask_to_send_all` with at most 5 to-do ids. One
question names every recipient ("Send all 3, to Dana, Sam and Kim?"); only unseen drafts are read out. One clear yes
sends each with its own pinned revision and approval, and Undo cancels all of them.

"Send without asking" settings are not touched. `confirm_action` from the dashboard still only takes the owner's own
approvals; `voice:` comes only from `talk_send`.

## What Talk does itself

- **Do it vs done.** "Do it", "handle it", "start it" are `do_it` (`talkDoIt`): the to-do's own **Do it** (`decide
  accept`, or `retry` when stuck), which starts The Machine's job. "Mark it done", "I did it" are `todo_action
  mark_done`. A running job is left alone. A waiting draft goes through `ask_to_send`. "Continue" on a to-do not started
  is its Do it.
- **Corrections.** Talk keeps the last action it took (`v.last`). "No, I meant…" right after is `undo_last_action`: the
  action is taken back (reopen, unsnooze, the old title), and the voice says what it undid before doing what was meant.
- **Navigation.** "Next one", "previous", "stop", "leave it" are Talk's own (`list_todos`, `open_todo`, or nothing).
- **In a to-do's own Talk live**, "mark this as done" is the owner's own decision, so Talk marks it done itself (with the
  to-do's usual undo) instead of handing it to the chat. The chat stays open.
- **Report a bug.** "Report a bug" or "send feedback" is `report_bug` (`talkBug`), never a to-do. It sends the same
  report as Help's **Report a bug**: "From Talk: " and the owner's words. The to-do in focus and the last 8 lines go only
  when the owner agreed (`context`), the support report too (`support_report`); the voice asks once. It says "Sent the
  bug report." and never that it is being looked into.
- **Unclear words.** Before `create_todo`, `todo_action`, `do_it`, `undo_last_action`, `report_bug`, `ask_machine` or
  `end_talk`, the page checks the owner's last words: a dropped noise or one odd word returns "Sorry, say that again?"
  and nothing is done. The instructions say never to claim an action no tool result confirmed.

## Tests

All with the Gateway helper stubbed, and the page tests with a fake `getUserMedia`, `RTCPeerConnection` and data channel,
with screenshots at 390x844 and 1440x900, light and dark:

- `tests/test_talk_live.py`: the service side. Start, the single offer, limits, the transcript, owner only, the secret
  never returned; search, records and the calendar; sending by voice (only a clear yes after a question that names who,
  a changed draft, reading once, seen on screen, a batch, Undo, an expired question).
- `tests/test_talk_live_dashboard.mjs`: a to-do's Talk live from the page, sending and Undo.
- `tests/test_talk_hearing_dashboard.mjs`: transcription, noise reduction, turns, speed and logprobs; what counts as
  noise; no dashes; the draft card's layout.
- `tests/test_talk_main_dashboard.mjs`: Talk: the sidebar, the bar, the view, listing and opening to-dos, a send by
  voice, new to-dos, the limit, End and **Start again**, lookups as cards, `machine_status`, `ask_machine`, to-do
  actions, and running in the background.
- `tests/test_talk_actions_dashboard.mjs`: what Talk does itself: Do it vs done, corrections, navigation, chat answers,
  unclear words, `report_bug`, Undo for a batch.
