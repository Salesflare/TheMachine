# Architecture and reviews

[Documentation index](../README.md). Current reference; dated repair evidence lives in [History](history.md).

## Architecture

```text
Gmail · Google Calendar · Outlook · Slack · Salesflare CRM · Android notifications · WhatsApp · Telegram chats · OpenClaw Gateway
plugins: Docs · GitHub · Google Meet · Intercom · LinkedIn · RSS · Shortcut · Stripe · Trello · X · Zoom
                │  (read-only collectors, one thread and checkpoint per account)
                ▼
assistant.py (systemd user service) → private SQLite + full-text search, local API on 127.0.0.1
                │
                ▼
OpenClaw main agent, isolated review turns started by the service → to-dos
                │
                ▼
Telegram bot (via OpenClaw) ⇄ owner decisions ⇄ dashboard on your tailnet · `assistant` CLI
                │
                ▼
Do it → isolated preparation turn of the same agent → result, draft + Send, or blocker
```

| Path | Role |
|---|---|
| `assistant.py` | Collectors, SQLite store, local API, dashboard server, Telegram outbox, review and preparation workers |
| `dashboard.html` (its main script in parts in `dashboard/`, served as one page), `sw.js`, `manifest.webmanifest`, `brand/` | Owner dashboard and installable web app |
| `cli.py` | The `assistant` command line |
| `next_actions.py` | Approved sends: email (Gmail through `gog` or the token broker, Outlook through Microsoft Graph), Slack direct messages (Sign in with Slack, or Maton), LinkedIn messages and X replies and DMs (OpenClaw browser), WhatsApp messages (`wacli`) and Telegram messages (the outbox of `telegram_mirror.py`); calendar changes and doc writes go through `calendar_writes.py` and `doc_writes.py` |
| `preparation_state.py`, `rollout_health.py` | Preparation bookkeeping and health checks |
| `retention.py` | Nightly housekeeping: old sync history and preparation logs go, free space goes back to the disk, local database copies rotate |
| `openclaw-plugin/` | `personal-assistant-bridge`: the `assistant_signals` tool, Telegram buttons and replies, Android feed capture, review/preparation guards |
| `*.mjs` | Small Node helpers that call the OpenClaw Gateway (`openclaw-root.mjs` finds the installed package) |
| `integrations/browser-lease.py` | Shares the OpenClaw browser between concurrent Do it runs |
| `browser_viewer.py`, `deploy/browser/` | Optional: a browser of its own on a virtual display that you watch and use from yours (noVNC, 127.0.0.1 only), and bringing a tab to the front on a desktop |
| `mail_attachments.py` | Email attachments a preparation saves: encrypted on disk with the message key, a private readable copy for the run, encrypted in place after runs that saved them with `gog` |
| `browser_login.py` | The sign-in dialog: fills a sign-in page in the assistant's browser with what you type on the dashboard, and keeps saved sign-ins encrypted |
| `integrations/browser_cdp.py` | Talks to a browser's DevTools address directly, for the LinkedIn and X readers when one is set |
| `AGENTS.md`, `PREPARATION.md` | Instructions the plugin gives the agent for reviews and for Do it runs (templates; see below) |
| `source-notes/` | How to read each connector, one file per service; a review or Do it run gets only the notes for the sources this Machine has connected |
| `install.sh`, `installer.py` | Install, upgrade and uninstall |
| `config.example.json` | Every configuration key with example values |
| `embeddings.py` | Optional related signals by meaning, through a local embedding server |
| `graph.py` | People and projects: a living graph rebuilt from signals, to-do decisions, project labels and merges |
| `knowledge.py` | One brain behind every surface: who someone is, their latest messages, what is open with them and when you last talked, the same for the chat, Talk, connected AIs and the Graph pages, under each caller's rules (see below) |
| `crm.py`, `crm_import.py`, `crm_fixes.py` | The Graph as a CRM: owners, change history, filters and sorts done on the Machine, merged organizations with several websites, and CSV import with undo, easy fixes shown before and after, and a check by the owner's model (an `import` agent run that sees headers, a few values and unclear cells) |
| `voice_input.py`, `voice_worker.py`, `voice-requirements.txt` | [Voice input](voice.md): the mic in the dashboard's message boxes; speech to text with OpenAI when the Machine has it, else on the Machine (faster-whisper in its own virtualenv, prepared ahead of time once the Machine is live and quiet) |
| `talk_live.py`, `talk-live-run.mjs` | [Talk](talk-live.md): a spoken conversation in a to-do's chat with OpenAI's Realtime voice, started by the Gateway (ChatGPT sign-in or API key); read-only tools, requests to the to-do's chat, a send only after a confirm question and a clear yes (with Undo), the transcript kept in the chat |
| `crm_fields.py` | Custom fields per record type (text, number, date, choice; values sealed at rest) and tags, kept through rebuilds and merges |
| `meet.py`, `meet_app.py` | [Scheduling between Machines](scheduling-between-machines.md): a meeting request asks the other person's Machine, and **Book it** writes the owner's own calendar |
| `deploy/` | Example systemd units (the service, an optional local embedding server) and Caddyfile |
| `tests/` | Offline tests (`test_*.py`, `test_*.mjs`), run by `scripts/test.py` from the repository root |

This table lists the main pieces. Every module, and where new code goes: [Code map](code-map.md).

Python's standard library and SQLite are enough: no database server, queue, web framework or extra scheduler. Runtime data lives in `~/.local/share/personal-assistant/`: `config.json`, `events.sqlite`, tokens and receipts.

**Data model.** The main tables are `events` (with an `event_search` full-text index), `checkpoints`, `sync_activity`, `analyses` (reviews), `review_runs`, `suggestions` (to-dos), `decisions`, `deliveries` (the Telegram outbox), `preparations` and `action_jobs` (approved sends).

- Provider IDs deduplicate events per account. A changed event gets a new version and becomes reviewable again.
- Each source page commits its events and next cursor in one transaction, so a crash replays the page instead of losing or duplicating it.

**One brain.** The chat's tools, Talk, connected AIs (MCP) and the dashboard ask the same questions about people,
organizations and projects. `knowledge.py` answers them once:

- `find` and `record`: a name, address, handle or phone number, however it is written;
- `latest_messages`: what the record's Graph page timeline shows (every merged identity, an organization's people,
  never a meeting ahead);
- `search_messages`, `open_with` (promises both ways and open to-dos, an organization's people's too) and
  `last_contact`.

A `Caller` carries the rules. The owner sees everything. A connected AI sees its connection's area, never the owner's
own record or a teammate's, and no message the app holds back. Surfaces only format the answers.
`tests/knowledge_eval.py` asks every surface the same questions over the sandbox.

**Boundaries.** Every account has an explicit ID and `boundary` (`work:Acme`, `personal:phone`, `owner:system`…). Every read names its accounts explicitly; app names and chat labels never decide which company an item belongs to.

### On the device

The dashboard opens from the device and then refreshes. Until the first real data is known it shows a quiet outline of the to-dos (as many as last time, never their content). "All clear" shows only when the Machine itself says there are no to-dos, never from a kept copy.

- **The page.** `sw.js` keeps a copy of the dashboard page (the app shell) and every brand image and font, and opens the app from them. It stores all of them as soon as it runs, so offline looks the same as online.
  - The page never holds the CSRF token: the server leaves it out, and the service worker takes out one an older page still had. The page gets it from `api/session`, and a change waits for it.
  - On each start it first asks the Machine for the page with the copy's ETag and waits up to 1.5 s. A 304 opens the copy. A new page (a release) opens that page and replaces the copy, so a start or reload after an update never shows the old version.
  - Offline, or without an answer in time, it opens the copy at once and the answer replaces it later. The page then sees the new release in `api/status` and loads it as soon as nobody is using it (also in a background window nobody used for 45 s). A new release drops the copy before the page reloads.
- **The data.** The last to-dos (`api/status`), the open to-do's chat and the Graph's overview and the first page of each list are kept in IndexedDB.
  - Encrypted with AES-GCM under a non-extractable key that never leaves that browser's IndexedDB, each row bound to its name and owner.
  - Keys that look like secrets (`csrf`, `token`, `*_token`, `password`, `*_key` and the like) are removed first.
  - Read-only copies older than 7 days are dropped, one row is at most 3 MB, and read-only copies are trimmed within an 8 MB budget (oldest first). Waiting owner changes and unsent chat drafts are not evicted by that rule; they stay until sent, canceled or signed out.
  - Saves snapshot their input and commit in order for each record, so an older slow encryption can't replace a newer copy.
- **Compressed.** The page, `sw.js`, `api/status` and the other data answers go compressed (Brotli when the Python module is there, else zstd on Python 3.14+, else gzip; the browser's `Accept-Encoding` decides), with `Vary: Accept-Encoding` and an ETag per coding that still gives a 304. Only answers without a secret are compressed: a secret compressed next to text an outsider can influence (an email's words on a to-do) could be guessed from the size (BREACH). So the page carries no CSRF token, and `api/session`, file downloads, the browser view and streams go as they are. `api/status` also leaves out what the to-dos never read (a finished review's signal list, saved pre-close state).
- **Whose.** The page (and `api/session`) carries `cache_scope`, an HMAC of the Machine's token and its owner that says nothing about either. A different scope (another owner, or a new Machine) wipes what the device kept.
- **Wiped** on Sign out (before the sign-out request goes), when the session is gone (the sign-in gate's redirect or a 401/403 on `api/status` or `api/session`, also seen by the service worker), and on another owner. Nothing is kept inside a frame (the site's demo).
- **Stale.** A kept copy shown while the Machine can't be reached says so at the foot of the sidebar: "Offline · updated 10:42". A bar over every view says it too ("Offline. Showing what was here at 10:42.", or "Your Machine is restarting."), with how many changes wait and Try now.
- **Calendar.** Each week the Calendar read is kept the same way (`cal:<monday>`), so it opens offline with the meetings it had.
- **Waiting changes.** Offline (the browser says so, or a request fails with no answer or a 5xx), the owner's own decisions on a to-do wait on the device instead of failing: Snooze, Not needed, Mark done, Reopen, and a note or chat message to The Machine without files (`decide`).
  - Each is kept encrypted with the rest (`outbox`) and shown on its to-do or in the chat as waiting, with Cancel. A canceled chat message goes back into the box.
  - They go by themselves, oldest first, when the Machine answers again: the `online` event, the next good `api/status`, or a retry that waits 2 s, doubling up to a minute, with jitter.
  - Each carries its `decision_id`, so one sent again after a lost answer is saved once. One the Machine refuses (the to-do is gone) is dropped and explained, never called saved; its unsent chat text returns to the draft.
  - A waiting change is acknowledged only after its device-storage transaction commits. When storage is unavailable, the page says to keep it open: the change is in memory, not durable.
  - Nothing that goes to other people ever waits. Send (`confirm_action`) needs the Machine to answer while the owner looks, and says it is offline.
  - A change that has no CSRF token yet (a page from the device) fails at once when the browser is offline, and waits up to 8 s for `api/session` when only the Machine is away.
- **Typing.** A chat message being typed is kept per to-do (`chat-drafts`, encrypted, saved a moment after typing stops and on leaving the page), so a reload or a lost connection never loses it; sending it clears it.
- **Reconnecting.** `api/status` is retried after 2.5 s, doubling up to 30 s with jitter (or the server's `Retry-After`), and at once when the browser comes back online or the owner taps Try now.

The copy protects against someone reading the browser's files (a lost laptop's disk, a backup). Anyone using the unlocked browser profile itself sees what the dashboard shows anyway, so on a shared computer sign out when done.


## Reviews

### How a review runs

The service starts reviews itself (`review_worker.enabled`). When at least `min_signals` wait (40 by default), or the
oldest has waited `max_wait_minutes` (60), it starts one isolated turn of your main agent,
`agent:main:assistant-review-signals-<run>`, with message delivery off.

- **A new mailbox first.** A newly connected mailbox (Gmail or Outlook, on a new install or added later) doesn't wait:
  its first review starts as soon as its first import of the last 7 days is in, as one review. None starts halfway
  through the import, and never later than `max_wait_minutes`. Meanwhile the dashboard says "First review starts when
  your mail is in".
- **The turn.** The plugin adds `USER.md` and `AGENTS.md`. The agent claims up to 120 signals, reads them through the
  `assistant_signals` tool, checks decisions, earlier to-dos and related evidence, saves to-dos with `when`/`due`
  timing, and finishes the analysis.
- **One at a time.** One run at a time, with a gap between runs; failed runs back off. Unfinished claims move safely
  to the next run, and the service never restarts the Gateway. A version that was deferred stays searchable; two
  deferrals set a signal aside until it changes.
- **What you see.** Connections, **Reviews of new messages**, shows a running review at the top: how far it is (12 of
  40 signals), from which accounts, and its latest step from its own tool calls ("Reading 20 emails", "Looking up
  Globex", "3 suggestions so far"), updated every few seconds. Never message text or search words. Then when the next
  one starts. Finished runs move to **Recent runs**.

### One to-do per matter

A new signal about something that already has a to-do updates that to-do instead of starting another one.

- A later message in the same email or Slack thread finds the thread's to-do by itself. Across threads the review
  judges sameness by meaning (the same people and the same ask or commitment) and passes `card_id`.
- When open to-dos share people or the project with a new one, `suggest` asks the review which to-do it is
  (`card_id`) or whether it's a different matter (`separate:true`) before saving.
- An open to-do gets the new evidence, title and body. A snoozed one, or one waiting for a reply, comes back open with
  one new notification.
- A done or dismissed to-do reopens only when the review says it needs you again (`reopen:true`). Otherwise the
  message is kept on it as evidence.
- Each update is in the to-do's history, and the old key keeps pointing at the to-do.
- A title The Machine wrote stays current: a review update or a preparation result gives it a new one when the
  situation changed (not for a mere rewording). A title you chose yourself (`title_source` `user`) is never replaced.

### Things that slipped

Each review prompt also gets up to five "Possibly slipped" lines of each kind:

- **Your unanswered asks:** your own sent emails whose new text asks something (a ? in a link doesn't count) and whose
  thread has had nothing since, 4 to 21 days later. Only in threads the other person started, or to people who had
  written to you before you started the thread, so your outreach never shows up. Three or more emails sent the same
  day with the same subject pattern count as outreach too and are left out.
- **Questions to you:** questions addressed directly to you (at most two To recipients, not Gmail's Updates,
  Promotions, Social or Forums, from someone you have emailed before) with no reply from you in the thread after 2 to
  14 days.

Anything already on a to-do is skipped. The `slipped` table records which review got each one; it's offered again only
if that review didn't save within six hours. The review checks for an answer elsewhere before making a to-do.

### Promises

Reviews record every promise they find in a message, with `promise`, instead of making a to-do:

- one you made in something you sent (`mine`);
- one someone made to you (`theirs`, in their message, or in your ask they took on);
- with who, what, and a date when one was said.

Most promises are never spelled out and look different per person, language and relationship. So the review judges
what a message means in its conversation (reading the request in `earlier_in_conversation`), with examples as a guide
rather than words to look for.

Each goes into the `promises` table, once per message, person, direction and distinct promised action. A plan made
together (their "let's do it Sunday" and your yes) reads as a promise both ways: while one with that person for the
same action is open, the second is not recorded again, and the open one becomes yours, marked as made together. The
same open promise stored twice from before is kept once. Nothing shows up on Telegram yet.

- **When it's checked:** yours on the morning it's due (at `digest_at`, never sooner than three hours after it was
  recorded), theirs the morning after their date. Without a date: yours after 3 days, theirs after a week.
- **Closing by itself:** someone else's promise made by email closes when that sender replies in the original thread
  (sender-only fallback if no thread was recorded). Chats run on, so a later chat message is no sign it was kept: those
  stay open for the review or the check. Their new message is reviewed as usual, so a delay can become a new promise.
  Every review prompt lists the open promises, and the review closes one (`kept` or `dropped`, with the reason) or
  moves its date when a later message shows it.
- **The to-do:** a promise still open when it's checked becomes a to-do (`promise:<id>`), prepared ahead under the
  usual limits: for yours the thing you promised, for theirs a short nudge. If they answer while the to-do is on its
  way, it closes. At most 5 such to-dos a day. With reviews off (a new install, its first look included) a due promise
  waits: no to-do and nothing prepared until reviews are on.
- **Where you see them:** the To-dos page has a **Promises** list (You promised, Promised to you) with Done and Drop
  for open ones. Every promise link (that list, the Calendar, Open between you on a person, organization or project
  page) opens the promise's own page (`#promise/<id>`, read from `GET /api/promise?id=`): its state, the message it
  came from, the people, organization and project of that message, its to-do as a link, and a history from
  `promise_log` (kinds and dates only, never message text). Change date there is `promise_due`, owner only.
  `assistant promises` lists them, and the weekly recap counts kept and open ones.

### Follow-ups

`follow_ups.py` follows up on Graph projects when nobody replies, per board (`follow_up_rules` scope `board`) or per
project (scope `project`, which wins). Off by default. What the owner sets ([help](help/follow-ups.md)):

- the shortest and longest wait (3 and 7 days);
- at least and at most this many follow-ups (1 and 3);
- stages: all open ones, or per stage with its own wait;
- channels: connected ones that can send, the last conversation's channel first, switching on request;
- asking first, or a standing approval;
- **Only on work days**: on for Work and off for Personal unless set. The work days come from the owner's
  [work hours](usage.md#work-hours). On a day off nothing is drafted and nothing goes out by itself; what comes due
  moves to the next work day, at the start of the owner's hours;
- the move to the board's Stalled or declined row after the last one.

`schedule()` is the pure math over a project's messages (`event_projects` plus `graph_events`).

**The round.** Every five minutes the action worker runs `App.follow_up_step`:

- It settles open ones: sent, skipped, replied, won, lost, archived, a teammate's project, a stage turned off.
- It ends rounds past the maximum (`follow_up_ends`, plus the optional move with source `follow_up`).
- It drafts the due ones as early to-dos (`suggest(ahead=True)`, one per project; `follow_up_cards` remembers which).
  Drafting runs last in the preparation queue and pauses earlier than other work on usage
  (`model_budget.follow_up_pause`), unless the longest wait has passed. Follow-up drafts skip the one-draft-per-tick
  gap of other work prepared ahead: they have their own pacing.
- The preparation prompt adds the follow-up's number, channel and earlier texts. Past the minimum, the model judges
  from the thread whether another one is worth it and can save `already_done` with `follow_up: stop`. Before drafting,
  `newer_activity` skips projects with something newer.
- With a standing approval, a single unrepeated draft goes through `confirm_action` (approval
  `auto-follow-up:<id>:<revision>`, so it never sends twice), only in work hours and never in Careful mode. Anything
  else waits for the owner.
- A board's follow-ups show as one to-do from the start ("Writing 3 follow-ups…" while drafted), with a fast review
  once ready. Their phone notifications are grouped (delivery status `grouped`).
- The owner's earlier unanswered sends that were never collected (sent from another app before the mailbox was read)
  count in the round. `earlier_sends` reads the real thread once per waiting point (Gmail `threads.get` or the Outlook
  conversation, metadata only, cached in `follow_up_threads`), else the quoted reply headers in the owner's latest
  email, until the first quoted message from someone else.

**Bounces.** `bounces.py` records email addresses that bounce.

- `message_event` reads a delivery report from its structure (multipart/report with message/delivery-status:
  Final-Recipient, Action, Status; X-Failed-Recipients; the original's Message-ID from the attached message or
  In-Reply-To) into `metadata.bounce`.
- `scan()` records them per address (`email_bounces`), and on its first pass reads reports collected before from their
  stored text. Hard failures (5.x.x) count at once, soft ones (4.x.x, a full mailbox) after 3 over 7 days.
- `clear()` drops the flag when the address writes again, or a later send to it went 48 hours without a bounce.
- Where it shows: the person's page (`graph.with_bounces`). Drafts never get a bounced To when a working address is
  known (`steer`; the draft says "Bounced, now to <address>", `moved`). Follow-ups go to the working address, or skip
  email when there is none. A follow-up whose To bounced after its draft is held right before it goes and moved to the
  working address under a new revision (`follow_ups.hold_bounced`). The review gets it as a hint.

### What reviews learn from you

Your decisions and written reasons are summarized into every review prompt. Lasting facts you state are saved
(`remember_fact`) and listed, removable, under Learning. More on the Graph and facts: [Intelligence](intelligence.md).

**How you write** is kept per channel: a short block (up to five lines) each for Email, Slack, WhatsApp, Telegram, LinkedIn,
X DMs and any other channel, plus Everywhere. They're under Settings → Writing → **How you write**, where you can edit or
remove them.

- A voice study reads a sample of your own sent messages per channel (a few dozen emails across languages) and writes
  each block: greetings and sign-offs per language, length and structure, tone per kind of person, habits, with your
  style notes worked in. It runs once on its own and again every 30 days, and never touches a block you wrote yourself.
- A style note that holds beyond one to-do (length, greeting, sign-off, language, capitals, punctuation, links) is
  worked into that channel's block instead of piling up next to it.
- A review compares drafts you edited, or answered yourself instead of tapping Send, with what you wrote, and folds
  lasting habits into that block. Such an update keeps the rest of the block: it can't shrink it to one note.
- Every preparation gets all the blocks (its to-do's channel marked), your own recent messages on that channel within
  the to-do's source accounts (the same conversation first) as examples, and your earlier edits on that channel.

**Draft rules and facts.** How a kind of task is done (what to include, where things go) stays a **draft rule**.

- A preparation doesn't get everything learned. While the list is short it gets all of it. After that: the facts and
  draft rules learned on that to-do, plus the ones closest in meaning to it (with
  [local embeddings](intelligence.md#related-signals-optional-local-embeddings) on, else the newest).
- Each fact has a sort (event, commitment, preference or fact, given by the review that saves it) and can have an end
  day (`until`). An event without one ends after 30 days.
- A preparation weighs facts by how fresh they are: half-lives of 7 days for events, 90 for commitments and
  preferences, 365 for other facts, after GBrain's decay. A fact past its end day is left out; the next review retires
  it, and Learning lists it under **Ended** with **Bring back**.
- Facts about someone in the Graph don't count toward the cap of 80; the cap is for the rest.
- Now and then a review condenses the list. Notes that say the same thing or contradict each other become one (the
  newer wins), a note about how you write on one channel moves into that channel's block, and the originals stay
  behind it.

**Where you see it.**

- Learning → **What I've learned** lists it newest first, grouped as How you write, Facts and How to do things, with
  "Merged from N notes" and **Undo merge** on each condensed one. You can edit or remove each fact and rule there.
- A to-do's chat shows what its notes taught, read from the database (not from the reply): a quiet
  **Saved to what I’ve learned** line under the reply, with **Edit** and **Undo**.
- Five or more notes about one kind of task can become a skill, on a to-do you decide
  ([skills](skills.md#from-your-notes)).
- Each Do it result says whether it's finished or what it needs from you, and the run sorts your Change notes (style,
  missing fact, keep going, new ask). Learning → **How it's going** shows the split and Worth it over time, from the
  first decided to-do (per day for two weeks, then per week).
