# Sources and collection

[Documentation index](../README.md). Current reference; dated repair evidence lives in [History](history.md).

## Sources

Collectors read existing source content. The optional Salesflare `join_pipelines` setting also adds your own user to matching CRM accounts; it is empty by default. Each collector runs in its own thread with its own checkpoint, so a slow or failing source never blocks the others. Absence from a later read is never treated as deletion.

| `service` | Needs | Account keys |
|---|---|---|
| `gmail` | `gog` OAuth for the account, or a token broker | `email`, `client` (gog OAuth client), `excluded_terms` (text that drops a message, e.g. a warmup tag) |
| `calendar` | `gog` OAuth, or a token broker | `email`, `client`, `calendar_id`, `excluded_title_terms`, `writable` (a shared calendar you may change events on) |
| `outlook` | Your own Entra app (`graph`), or a token broker | `transport`, `email`, `credential` (with `graph`), `connected_at` (with `broker`, set when connected), `excluded_terms` |
| `outlook_calendar` | The same sign-in as `outlook` | `transport`, `email`, `credential`, `calendar_id` (`primary`), `excluded_title_terms` |
| `slack` | A [Maton](https://maton.ai) Slack connection, or Sign in with Slack (The Machine's Slack app, user token through the `slack_broker`, `transport: broker`; only for workspaces the control plane opens it to, until the app is in the Slack Marketplace) | `team_id`, `user_id`, `email`, `slack_host`, `fair_incremental`; Maton only: `credential` + `credential_variable` (file with `MATON_API_KEY=`), `connection_id` (found in Maton during setup) |
| `salesflare` | Salesflare API key | `api_base`, `app_base`, `credential`, `credential_variable`, `user_id`, `team_id`, `email`, `owner_emails`, `join_pipelines`, `accounts_per_batch`, `meeting_window_days`, `timeout_seconds` |
| `android` | OpenClaw Android app paired as a node | `transport: openclaw-feed`, `node_id`, `reconcile_seconds`, `direct_fallback`, `fallback_seconds` |
| `whatsapp` | `wacli` with a synced local store | `store`, `identity_sha256` (sha256 of the linked JID; the collector refuses a different account) |
| `telegram` | Your Telegram account, logged in as a device by `telegram_mirror.py` (Telethon, pinned in `telegram-pin.json`) | `store` (the mirror's folder), `identity_sha256` (sha256 of `telegram:<user id>`; the collector refuses a different account), `telegram_include` (chat IDs to read although muted, archived or over 50 members); config `credentials.telegram_app` (file with `TELEGRAM_API_ID=` and `TELEGRAM_API_HASH=`) |
| `gateway` | journald | `unit` (default `openclaw-gateway.service`), `bootstrap_hours` |
| `github` (plugin) | `gh` CLI logged in as you | `login`, `repos` (optional filter), `ci_repos` + `ci_branch` (failed runs) |
| `stripe` (plugin) | Sign in with Stripe (The Machine's read-only Stripe app, through a token broker), a restricted read-only Stripe key, or a Maton Stripe connection | `transport` (`broker`, `api` or `maton`), `credential` (+ `credential_variable`, and `connection_id` found in Maton), `stripe_account`, `large_subscription_monthly` (500) |
| `intercom` (plugin) | Sign in with Intercom (the app The Machine): hosted, or on a self-hosted Machine paired with an account | `credential` (+ `credential_variable` for an env file); `workspace_id`, `workspace_name`, `region` and `admin_id` are read from the token when you connect; it is always Work, for the company the workspace names (`work:<workspace name>`, renamed like any account) |
| `linkedin` (plugin) | LinkedIn signed in to the OpenClaw browser | `active_hours` (`[7, 22]`, local time); config `linkedin_inbox` for the reader path |
| `x` (plugin) | X signed in to the OpenClaw browser | `handle`, `primary` (the account the browser is normally on), `active_hours` (`[7, 23]`), `long_posts` (X Premium: replies up to 25000 characters); config `x_inbox` for the reader path |
| `trello` (plugin) | Sign in with Trello (the app The Machine, scope read, no expiry): hosted, or on a self-hosted Machine paired with an account | `board` (URL or ID, one board per account, picked after signing in), `credential` (`{"key", "token"}`; a token alone with `api_key` still works), `bootstrap_days` (7) |
| `zoom` (plugin) | A Zoom sign-in through a token broker (a paid plan with AI Companion for summaries) | `transport: broker`, `email`, `bootstrap_days` (7); config `zoom_broker`, `zoom_transcripts` (true) |
| `google_meet` (plugin) | None: Connect Google Meet signs in with Meet's own Google app (`meetings.space.readonly`, `documents.readonly`), apart from Gmail (`transport` `broker`) | `email`, `bootstrap_days` (7, at most 30); config `google_meet_broker` |
| `docs` (plugin) | The owner's own Google (broker) or Microsoft sign-in for that address, plus a separate consent for files | `email`, `transport` (borrowed from the mail account), `provider` (`google` or `microsoft`, else from the mail account), `boundary` |
| `shortcut` (plugin) | A Shortcut API token | `workspace`, `credential` |
| `rss` (plugin) | none | `url` |

Add a plugin account with `assistant connect github` (or `stripe`, `intercom`, `x`, `linkedin`, `trello`, `google_meet`, `shortcut`, `rss`): it asks for the fields that connector needs. The dashboard does the same under Connections, **+ Add** (see [Usage](usage.md#adding-a-source)). You can also add accounts to `config.json` by hand, using the keys above (each connector's header has a full example), and restart the service.

## How each source reads

### Gmail and Calendar through a token broker

Instead of `gog`, a Gmail or Calendar account can use `"transport": "broker"`. A service you run (a hosted control plane, say) keeps the Google OAuth client and its secret. This machine keeps the account's refresh token (`mail_grants.py`: `mail-grants.json` next to the database, mode 600, sealed with the message key).

- **Setup:** set `google_broker.url` and put this machine's token in the `google-broker` credential.
- **Each call:** `google_api.py` asks the broker for a short-lived access token for that one account and scope, sending the refresh token along, then calls Google's REST API directly.
- **The protocol:** the broker answers `POST {"email", "scope", "refresh_token"}` with `{"access_token", "expires_in", "scopes"}` and keeps neither token (an account connected before this asks without `refresh_token` until its sign-in is moved here). It answers `POST {"email"}` with the granted `scopes`, and 403 for a scope the owner didn't grant.
- **Allowlist:** only a fixed list of Gmail and Calendar methods can be called; anything else is refused before a token is asked for.
- **Sending and snoozing** work only when the owner granted `gmail.send` or `gmail.modify` at the broker, as with `gog`. The hosted control-plane broker currently grants read-only plus optional send, not `gmail.modify`, so thread snoozing needs another already-granted route.
- **Paired self-hosted Machines** get the same from the dashboard's **Sign in with Google** (and Microsoft and Zoom). The broker is then the control plane's `/api/fleet/<provider>-token`, and the credential its own device token ([the Fleet](fleet.md)).

### Gmail

Follows Gmail history after a seven-day import, and replays the retained window when history expires. Replies keep their new text whole and only 3,000 characters of quoted history. Sending approved drafts and snoozing threads use separate workers and only scopes already granted.

### Outlook and Outlook Calendar

Microsoft 365 and Outlook.com. `ms_graph.py` reads them through Microsoft Graph with delegated scopes only: `User.Read`, `Mail.Read` and `Calendars.Read`, plus `Mail.ReadWrite` and `Mail.Send` when you turn sending on.

**Two transports:**

- `"broker"` works like the Google broker (`microsoft_broker.url`, the `microsoft-broker` credential, the same protocol with Graph scope names). The refresh token Microsoft rotates comes back as `refresh_token` and replaces the kept one.
- `"graph"` uses your own Entra app registration (`microsoft_graph.client_id`, `tenant`, public client flows on), a device-code sign-in, and a refresh token in a mode 600 credential file per account.

**Mail** follows changed messages after a seven-day import, and is stored like Gmail, so to-dos, replies, sending and snoozing work the same:

- A reply goes out as the exact message (threading headers kept).
- Snoozing moves the thread's Inbox messages to a `Snoozed` folder and back, unread, unless someone already replied.
- Not matched: messages deleted for good rather than moved to Deleted Items.
- Shared calendars sync by delta like the main one.

**Signing in right after connecting:** Microsoft can refuse a new sign-in for a few minutes while it takes the permissions. A broker account whose `connected_at` is less than 15 minutes old retries with backoff (`microsoft_signin_pending`), and a broker that answers 503 or 429 is asked again after its `Retry-After` (`microsoft_broker_busy`). Later refusals show `microsoft_signin_expired` and retry hourly, or as soon as you connect the account again.

### Signatures and attachments

- Graph has no signature API, so an Outlook signature is the one your recent sent mail ends with (found when at least three share it), or the one you set in Settings, Writing.
- There each mailbox has one signature with a small editor (bold, italic, underline, link, image by address, text color, clear, and the HTML itself). With nothing set, it imports the mailbox's own first: Gmail's signature (read with `gmail.readonly`, the scope the send check already uses) or the one Outlook's sent mail ends with.
- **Use mailbox signature** drops yours. What you save is cleaned to plain formatting, links and images.
- Preparations save email attachments (Gmail and Outlook) with `assistant attachment`. With message protection on they are kept encrypted ([configuration](configuration.md#email-attachments)).

### Calendar

Seven past and thirty future days, recurring events expanded, incremental sync token with a daily full refresh. A missing event is "unavailable", not "canceled". Context for email and preparation, not a reminder feed.

### Slack

Conversations you already belong to; it never joins channels or opens DMs. Per-conversation cursors, overlap rereads for edits, deferred retries for failed thread pages, and provider `Retry-After` honored across restarts (plus a random extra wait, so computers sharing a connection don't retry together).

**Slack's read limit.** Slack allows apps outside its Marketplace about one history or thread read a minute per workspace. A Slack sign-in or Maton connection gets no more than that, shared by everything on the same connection: this collector, another computer running The Machine for the same account, and your own scheduled posts that check a channel first. So:

- The collector spends at most one such read every `slack_read_seconds` and leaves the rest.
- It reads busy conversations within the hour and quiet ones once a day, and reads a direct message only when Slack says it has a new message.
- Posting isn't held back by this: a send Slack refuses as rate limited waits and goes out a few minutes later.

**The first import** reads where the activity is. A quick look at every conversation (a call outside that limit) shows when a direct message last had a message and when you last read each channel. Conversations active today get their last 24 hours read first, then the rest of the week, and quiet ones come last. A direct message with nothing in the window isn't read at all. Signals start within minutes; the whole first import of a large workspace still takes hours.

**Several Machines on one workspace** (a team's hosted Machines, or a laptop and a server) share that one read a minute, so each reads in its own minute of a round, on the clock. The round starts at `slack_read_seconds`. When Slack refuses a read for the rate limit, the Machine takes another minute and the round grows by one (up to 10 minutes), so Machines that picked the same minute drift apart and a team of five gets a minute each. After 30 reads without a refusal it shrinks by a minute again.

### Salesflare CRM

Only colleagues' emails that don't involve you (yours come from Gmail) and meetings with notes. With `join_pipelines`, it adds your own user to accounts linked to opportunities in those pipelines (a POST, never another user).

### Android

The plugin peeks OpenClaw's event queue for notifications from your phone node, with periodic direct reads to catch gaps. Repeated updates merge into one episode; one-time codes are omitted. Not a complete history.

### WhatsApp

Reads your existing `wacli` store (`auth status`, `messages list` only, always `--read-only`), rereading the last seven days. With `wacli sync --follow --profile-picture-budget 50`, it also asks that sync for the pictures of people in your Graph, at most 50 a day ([WhatsApp pictures](intelligence.md)). New messages arrive through the `wacli sync` that `assistant connect whatsapp` sets up (or your own).

### Telegram chats

`telegram_mirror.py`, a user service (`the-machine-<account>.service`, for example `the-machine-personal-telegram.service`), is the only process that holds the Telegram session. The collector reads its store read-only.

- **What it reads:** private chats and groups of up to 50 members; never channels, bots, Saved Messages or Telegram's service messages. It skips muted and archived chats unless listed in `telegram_include`.
- **First start:** the last `bootstrap_days` (7 by default, at most 30) of up to 100 chats, the window the other sources use, slowly. Then only what arrives.
- It never marks anything read and tells Telegram it is offline. Flood waits are kept.
- Message text and the session are sealed with a key derived from the message key (or the store's own `store.key`).
- **Sends** go through the store's outbox, keyed by the approved action, at least 20 seconds apart. A send that may have gone out is never repeated.
- When Telegram ends the login (`telegram_logged_out`) or stops accepting the app ID (`telegram_app_blocked`), the mirror stops for good and Connections says so. It never logs in again by itself.
- Disconnect (and `./install.sh --uninstall`) logs the device out at Telegram and deletes the store.

### OpenClaw Gateway

Failed agent runs on Telegram, refused hand-offs and failed Telegram sends, grouped per half hour with secrets redacted. The first Gateway source also carries **The Machine's own errors** (`machine.fault`): see [The Machine fixes itself](usage.md#the-machine-fixes-itself).

### GitHub

Notifications on threads you take part in (review requests, mentions, assignments, comments, threads you opened), each with the issue or PR and its latest comment. GET requests only; nothing is marked read. Each run checks that `gh` is logged in as `login`. Optional failed workflow runs per repository.

### Stripe

Only events worth a look are stored: failed payments, disputes, ended subscriptions, scheduled cancellations, past due or unpaid, and new subscriptions of at least `large_subscription_monthly` a month. GET on the account, events and customers only; it never refunds, retries or changes anything. Each run checks the key belongs to `stripe_account`. Signed in with Stripe, the refresh token stays on the Machine (like Zoom's) and a Work Fleet admin can share the account with the team. For a direct key, create a restricted key with read access to Events, Customers and Account.

### Intercom

Conversations updated in the last seven days (`bootstrap_days`), read in frozen search windows whose cursor commits with the conversations. Polls overlap six hours, the whole window is reread daily, and an expired cursor replays its window.

**Read-only by design:**

- REST with API version 2.11, and only `GET /me`, `GET /conversations/<id>` and the conversation search (a read-only POST). Anything else is refused before the token is read, so reading never writes.
- Replies are separate: see [Intercom replies](usage.md#intercom-replies).
- Connecting reads the workspace from the token on `GET /me` and keeps its ID and name, the admin and the region (US, EU or Australia). Every sync checks the workspace and admin again, exactly.
- A token from another workspace can't replace an account's own: add it as another account.

**Limits:** Intercom returns at most 500 parts per conversation. The opening message keeps up to 20,000 characters and the latest history fills the rest of a 40,000-character body; anything cut is flagged. Attachments aren't collected.

**Connecting:** Sign in with Intercom, through the app The Machine (Read conversations, Write conversations, Read one admin).

- From a hosted Machine's account page or dashboard. Its token reaches the Machine sealed and lands in the same private credential file, with the same allowlist. The dashboard's Add links there.
- A self-hosted Machine paired with an account can too, from its own dashboard: Connections, + Add, Intercom, then Sign in with Intercom (see [the Fleet](fleet.md)).
- There's no token to paste from a developer console.
- A Work Fleet's admins can share one Intercom with the team's Machines over The Machine Network, sealed ([Network](network.md#shared-connectors)).

### LinkedIn

Inbox conversations and messages (`connectors/linkedin.py` with `integrations/linkedin_inbox.py`), read through LinkedIn's own messaging API from a tab parked on `linkedin.com/robots.txt`, so nothing is marked read. No API key needed.

- **When:** hourly in waking hours only (`poll_seconds`, `active_hours`), to keep automated LinkedIn traffic low. Outside them Connections says when it reads again, and the night doesn't count as a stale sync.
- **Paging:** pages follow LinkedIn's own cursors and commit with the messages. An unfinished scan continues after 30 seconds and keeps its lower bound through outages, however long; only a completed scan advances it.
- Spam is skipped.
- **Signed out:** a busy browser retries in 10 minutes, a signed-out one hourly. Connections shows "Signed out of LinkedIn", and setup and doctor say in plain words that LinkedIn is signed out in that browser.
- **Tabs:** every tab the reader opens is closed when it's done, also tabs a stopped run left behind. A sign-in tab you opened yourself stays.
- LinkedIn's query IDs are pinned; `linkedin_inbox.py discover` refreshes them when LinkedIn changes its client.

**Which browser:** by default the reader uses OpenClaw's `openclaw` browser profile. A browser holds one LinkedIn sign-in per profile, so a second account gets a browser profile of its own: `"browser_profile"` on the account, or `"browser_cdp"` to read through a browser's DevTools address instead of OpenClaw's browser commands (like `http://127.0.0.1:9222`). It reads and sends there. Without those on the account, the reader takes `LINKEDIN_INBOX_BROWSER_PROFILE` and `LINKEDIN_INBOX_BROWSER_CDP` from its environment.

### X

Replies, mentions and the DM inbox for each X account signed in to the OpenClaw browser (`connectors/x.py` with `integrations/x_inbox.py`). It reads through the owner's own signed-in x.com session (the same requests x.com makes, not X's developer API) from a background tab, so nothing is marked seen. No API key needed.

- **Several accounts** can share the browser through X's account switcher. x-inbox switches to the one it reads and always back to `primary`, one run at a time, and only while no other job holds the browser lease.
- **When:** poll it hourly or less often (`poll_seconds`, default waking hours 07:00 to 23:00 via `active_hours`): X is sensitive to frequent automated reads. Outside its hours Connections says when it reads again, and the night doesn't count as a stale sync.
- Encrypted X Chat isn't read.
- **Signed out:** as with LinkedIn, Connections shows "Signed out of X" with a plain-language hint, and the reader closes the tabs it opened.
- Replies and DMs can be sent too, only after your approval (see [message actions](usage.md#x-replies-and-dms)).

**Which browser:** by default the reader uses OpenClaw's `openclaw` browser profile. A browser holds one X sign-in per profile, so an account can also have a browser profile of its own: `"browser_profile"` on the account, or `"browser_cdp"` to read through a browser's DevTools address instead of OpenClaw's browser commands (like `http://127.0.0.1:9222`). It reads and sends there. Without those on the account, the reader takes `X_INBOX_BROWSER_PROFILE` and `X_INBOX_BROWSER_CDP` from its environment.

### Trello

Actions on the cards of one board per account (created, moved, renamed, due dates, comments, a card deleted), GET only, so the board is never marked viewed. It connects with Sign in with Trello, through the app The Machine (scope read, expiration never), from a hosted Machine's account page or dashboard, or a paired self-hosted Machine's dashboard; the board is picked on the way back. Starts with the last seven days (`bootstrap_days`), then follows new actions with a short overlap; a long catch-up continues where it stopped.

### Google Meet

Generated transcripts (`google_meet.transcript`) and Gemini notes (`google_meet.notes`) of meetings the signed-in user organized, GET only: Meet conference records, their participants, transcript entries and smart notes (Meet REST API, `meetings.space.readonly`), and the Gemini notes Google Doc by its document id (Docs API `documents.get`, `documents.readonly`). No Drive scope. It never turns on transcription and writes nothing. Meet signs in on its own, with The Machine's Google Meet app (its own Google Cloud project and client, apart from the one for Gmail and Calendar), so Gmail need not be connected and Gmail's and `gog`'s scopes never change. It works like Zoom: the broker (`google_meet_broker.url`, the `google_meet-broker` credential) keeps the app and its secret, this machine keeps the refresh token in `mail_grants.py` (provider `google_meet`, revoked at Google on Disconnect), and `google_api.py` asks the broker for each access token. Each run replays the last seven days (`bootstrap_days`) for late or edited notes, and resumes from committed page checkpoints. Meet keeps conference records for 30 days. Each carries the call's `start_at`/`end_at`, so the calendar meeting at that time shows Gemini's notes under Notes and the transcript under Transcript, marked From Google Meet (`meeting_notes.py`, matched by time; never in place of the owner's).

### Zoom

The AI Companion summary of each meeting you hosted (`zoom.summary`), and its transcript when Zoom has one (`zoom.transcript`). GET only: nothing is written to Zoom. The matching calendar meeting shows the summary in its Notes and the transcript in its Transcript, marked From Zoom, next to what the owner added there (`meeting_notes.py`).

- **Sign-in:** your own (user-level OAuth through a Zoom Marketplace general app), not an account-wide Server-to-Server app, so it reads only your meetings.
- **Broker:** it works like the Microsoft broker. The broker (`zoom_broker.url`, the `zoom-broker` credential) keeps the app and its secret. This machine keeps the refresh token in `mail_grants.py`, and the one Zoom rotates on every refresh comes back as `refresh_token` and replaces it.
- **Scopes:** `user:read:user`, `meeting:read:list_summaries`, `meeting:read:summary`, `meeting:read:list_meetings`, `meeting:read:list_past_instances` and `cloud_recording:read:meeting_transcript`.
- **Each run** lists the summaries made since the last one, with a day of overlap for late or edited ones (the first run reads seven days back). When that list is closed to your sign-in, it lists your past meetings and their instances instead (or each one's latest instance, when the instances list is closed too; one-off meetings from before the window are skipped).
- Summaries need a paid plan, AI Companion on during the meeting, and no end-to-end encryption.
- **Matching:** `meeting_notes.py` matches notes to their calendar meeting by the Zoom meeting ID in the invite at about the same time, else by time (and the host among the guests). Two that fit equally match neither.

### Meeting notes

Notes can also be added to a meeting itself (`meeting.notes`, one per meeting, `source_id` `notes:<the meeting's event id>`, on the meeting's own calendar account):

- pasted or uploaded by the owner in the meeting's details in the Calendar;
- saved by a Do it run or the owner's own chat (`meeting_notes` on the `assistant_signals` tool, `assistant meeting-notes`), up to 400,000 characters of Markdown;
- written by The Machine from the meeting's transcript when the owner taps Generate notes on a meeting with a transcript and no notes (`meeting_writer.py`: on the service, in parts that each fit one model turn for a long transcript, on the owner's model and within its usage limits; marked `written_from: transcript`, dropped if notes come in meanwhile).

They carry the meeting's guests, so they are Work or Personal and shared as the meeting is. A signal review only reads them. Reviews then use the notes for that meeting's follow-ups, and fill in a Fleet follow-up split from them ([Fleet](fleet.md)).

### Docs

Comments, replies and @mentions on the owner's docs (`docs.comment`, `docs.mention`), suggested edits on docs they own (`docs.suggestion`, Google suggestions or Word tracked changes) and docs shared with them (`docs.shared`).

**Sign-in:**

- It borrows the sign-in of the owner's own Gmail/Calendar (broker transport only, never `gog`) or Outlook account for the same address, and adds no Gmail or `gog` scope.
- Microsoft documents need no Outlook. Without one, the Docs connection has a sign-in of its own (`own_grant`) with only the Docs scopes (`User.Read`, `Files.ReadWrite.All`, `offline_access`, sign-in), which the broker never answers for mail or calendar and the Outlook connectors never use.

**Google scopes:** reads ask the broker for `https://www.googleapis.com/auth/drive.readonly` (Drive files, comments, export, and Docs `documents.get` for suggestions). Posting a reply asks for `https://www.googleapis.com/auth/drive`, a separate opt-in, because `replies.create` takes no narrower scope that covers docs the app didn't open.

**Microsoft scopes:**

- Connecting Microsoft documents asks for `Files.ReadWrite.All` in one consent. A connection from before with `Files.Read.All` only gets **Allow edits** (the source `microsoft_docs_write`, refused when Microsoft doesn't grant it).
- Reads ask for `Files.Read.All` (`/me/drive`, its delta, `sharedWithMe`, and items on shared drives).
- `.docx` files are downloaded only from Microsoft's pre-signed hosts, without the token, to read comments, mentions and tracked changes.
- Microsoft Graph can't reply to Word comments, so those replies stay drafts.

**The files consent:** without it the sync fails with `docs_not_connected` and the to-do asks for it. A hosted Machine gets it from its account page's Docs tile, which the control plane announces with `docs_consent` (`true`, or the providers it offers it for, such as `["microsoft"]`). A paired self-hosted Machine signs in with the `microsoft_docs` source through the control plane, and `onboarding.connect_docs_grant` keeps the new sign-in and adds the Docs connection, Outlook connected or not.

**Reading:** the first run looks back 30 days and only learns existing suggestions; polls overlap two hours. Events link people by the commenter's email, and follow the account's Work/Personal label and the [Shared Graph](shared-graph.md) rules like mail.

**Acting on docs:**

- A to-do's preparation can read one doc's text with `assistant doc --event <id> --job <job>`, only while that job runs and only for the task's own doc events.
- A `doc_reply` next action goes through the same review and confirm as email (`next_actions.DocReplyTransport`: posted once, never re-sent on an unknown outcome).
- A `doc_write` next action creates a doc or edits one of the task's own docs, the same way ([Doc writes](#doc-writes)).

### Doc writes

`doc_writes.py` makes a new doc, or an edit to a doc of the task's own doc events, only after the owner's review and confirm. Telegram links to the dashboard's review, chat never writes in the same turn, and Talk reads the whole change aloud and waits for a yes.

**What an edit can do:** text only. Replace text within a paragraph (`{find, replace}`), add paragraphs after one (`{after, insert}`) or at the end (`{append}`); `# ` to `### ` lines become headings. Paragraphs with suggestions, tracked changes, fields or text boxes, and tables and images, are left alone.

**Writing once:** the draft pins the doc's version (Google `revisionId`, Word `cTag`). The send re-reads the doc, refuses when it changed, and writes once. An unclear outcome is checked by reading the doc back, never by writing again.

**Google:**

- Edits use Docs `documents.batchUpdate` with `writeControl.requiredRevisionId`, under the same `drive` opt-in as replies.
- A new doc needs only `drive.file`: a multipart Drive upload of HTML under an id from `files.generateIds`, so an unclear outcome is settled by looking that id up.
- The hosted Google sign-in asks for no Drive scope yet, so Google writes need a self-hosted broker that grants them.

**Microsoft:**

- `Files.ReadWrite.All`, its own incremental consent from Allow edits on the Docs connection (`microsoft_docs_write`; the control plane announces it with `docs_write_consent`), kept on reconnect.
- A Word edit downloads the `.docx`, changes the `w:t` text in place (no new dependency; DTDs refused), and puts it back with `If-Match` on the eTag read just before.
- A new doc is a small `.docx` uploaded with `conflictBehavior=fail` under a free name.

`assistant doc-draft` lets a preparation print a doc's paragraphs and check its draft first.

### RSS/Atom

The example plugin; see [Adding a source](adding-a-source.md).

### Shortcut

Story moves between workflow states (`shortcut.move`), with their owners and deadlines (`connectors/shortcut.py`). Connect it with `assistant connect shortcut`: the workspace URL or slug and an API token.

- Shortcut tokens have full account access (there is no read-only scope). This connector only reads: GET-only story search and story history, and it checks that the token belongs to the chosen workspace.
- It starts with the last seven days, searches with a one-day overlap and commits its paging checkpoints. The story's current context may be newer than a single move.

## The Machine's browser

### Watching it work

While a Do it run is on the browser, its Preparing to-do shows that tab live: a small picture every few seconds, right of its steps (below them on a phone), larger on a click, gone when the run moves on. The to-do's chat shows the same picture where its **Open the browser** link was; a click there opens the browser, as that link does.

- It is only ever a tab that task opened itself (by the target ID its own `open` step answered with): that run's, or one an earlier run of the same task left open and this run carries on in (after a sign-in, a retry or a Change). Never another task's tab or yours.
- It comes from the browser `browser_cdp_url` points at (127.0.0.1 only), over DevTools, without bringing anything to the front. A tab in the background shows no new picture until the run brings it forward.
- The pictures stay in the service's memory for a few seconds, only for the dashboard, and are never logged or saved.

### Stop from the browser

While a Do it run is using the browser, the Browser pane's header (and the viewer's own tab, `deploy/browser/machine-view.js`, on a phone) shows **Stop** with that to-do's title. `/api/browser-now` lists the running tasks on the browser, the one whose tab is in front (visible over DevTools) first.

Stop posts `chat_stop` with `via: 'browser'`:

1. the chat's own stop (the preparation waits as stopped, and every further tool call is refused);
2. the run's own tab stops loading (`Page.stopLoading`);
3. its Gateway run is aborted at once, instead of on the worker's next round.

The half-done step is not retried, and the chat shows "Stopped from the browser".

### When a task waits on the browser

A to-do whose Do it run has been in the browser for 45 seconds or more, or that stopped right after a browser step to ask for help (a sign-in, a captcha, a code), shows **Open the browser**.

- It brings the tab that task uses to the front on the computer the browser runs on, or opens the task's page again when that tab is gone (never another tab).
- With `browser_url` (or `browser_vnc`) it also opens that viewer, on Telegram too when it is an https page.

### View in browser

A ready to-do whose Do it run worked on a page in the assistant's browser (filled in a form, prepared something to submit, pay or book) gets **View in browser**.

- It shows only while that page is still open there. A run that closed its tab, or a tab closed since, gets none, and the run's own links to that site stay plain links.
- It brings that task's own tab to the front, as the run left it (or opens the page again when it closed after the to-do was drawn), and opens the viewer (`browser_url` or `browser_vnc`). You check and submit with the run's sign-in and entries, not in your own browser.
- A link the run added to the same site works the same way. On Telegram it opens the dashboard, which does the same.
- The to-do never carries the page's address; other links lose token-like query values.

### When a task waits on your sign-in

A Do it run that hands a sign-in to you (a password, a code, a passkey: its blocker says so, and it keeps that tab open) shows **Waiting for you to sign in** with a **Sign in** button on the to-do. On Telegram the to-do gets the same button and a **Needs you to sign in** notification (and phone push). Both open the dashboard's sign-in dialog for that task (`#signin-for=<task id>`, needs `dashboard_host`).

**Carrying on:**

- Signing in through the dialog carries the task on by itself, the same as **Continue**.
- Signing in in the browser itself does too. While a task waits, the service looks every 20 seconds at which sign-in forms the shared browser shows (which fields, never what is in them). Once the form on that task's site was seen and is gone, it carries on, once per blocked run.
- **Continue** stays as a fallback. The service never starts or retries a sign-in on its own.

**Per task:** the site comes from that task's own run steps (the address opened in the tab it last used, also in earlier runs of the same task). The dialog and **Open the browser** only offer that site, and a sign-in on one site never carries on a task waiting on another. When a task's site can't be told, the dialog names none and leaves it to the browser.

**The dialog** opens the task's sign-in page itself in the shared browser, also when its tab was closed (from the address its run left off at; it never types anything there), and waits up to 15 seconds for a form. A sign-in with nothing to type (itsme or eID, a passkey, a captcha, choosing an account) shows the browser's live view right in the dialog (with `browser_vnc`; otherwise **Open the browser**). Once that task's tab is back on its site past the sign-in, the task carries on by itself and the dialog closes.

### Sign in here

A small dialog that signs the assistant's browser in for you. It shows on a signed-out LinkedIn or X source in Connections, and as **Sign in** on a to-do only while its run waits on your sign-in right now (a run that is past that step and still working in the browser offers only **Open the browser**).

**How it works:**

- It asks for the username, password and, when the page wants one, a one-time code. It fills them into the sign-in page in the assistant's browser over DevTools (127.0.0.1 only), then submits.
- For a code it says which one the page wants (a text message, an authenticator app or an email), read from what the page itself says, with its sentence quoted and the number or address masked as the site masks it. It offers the page's own links for another method or a new code as buttons, and shows the site's own error when a code is rejected.
- When the site waits on something with nothing to type after the password (LinkedIn's "approve this sign-in in your app", a two-step or check page: no form left, but the tab is still at a sign-in address), the dialog says to approve it there and keeps checking every few seconds. **Continue** checks at once, and it goes on by itself once the tab is past it.
- For a captcha or anything unusual, use **Open the browser**.

**Who can use it:** only the owner on the dashboard; the agent, the model, the CLI and Telegram cannot. Nothing typed there is logged or quoted in an error. It only fills the site the dialog names, on https, and empties the password field again when the page does not move on.

**Save for next time:**

- Keeps that site's username and password in `browser-logins.sealed` in the data folder (mode 600), encrypted with the message key ([message protection](configuration.md#message-protection); a hosted Machine keeps that key off its disk), on this machine only.
- Without message protection they go in `browser-logins.enc` with a key of their own (`browser-logins.key`, mode 600), and move over to the message key once there is one.
- Connections, Sign-ins lists them: one row per site with its username, "Password saved" (never the password or its length) and the day it was saved, with **Forget**.
- When a site logs the Machine's browser out, the dialog's **Sign in as** fills them in with one tap.
- A move to another computer takes them along only with a passphrase. One-time codes are never saved.
- Anything running as the service's own user, the agent's shell included, can in principle read the key. So this keeps passwords out of the model's context, logs, support bundles and disk backups, not away from a compromised machine.

**From hosted setup:** a hosted setup page opens the dialog for one site (`#signin-site=linkedin` or `x`), titled "Sign in to LinkedIn on your Machine". Once in, it says so and setup connects by itself (a LinkedIn or X connect started there waits up to 10 minutes for the sign-in). Setup says a signed-out LinkedIn or X in plain words, never the raw error code.

### A browser on a server you can see

`./install.sh --browser-viewer` gives the assistant a Chrome of its own on a virtual display (Xtigervnc), shown in noVNC through websockify at `http://127.0.0.1:6080/`. The short address sets the viewer's settings itself; the long `vnc.html?...` keeps working.

- Ctrl+C / Ctrl+V (Cmd on a Mac) work between your computer and that browser.
- Everything listens on 127.0.0.1 only. Reach it through an SSH tunnel (`ssh -L 6080:127.0.0.1:6080 server`) or your own private proxy.
- It starts on first use and stops after 15 idle minutes.
- OpenClaw gets it as its `machine` browser profile (DevTools on 127.0.0.1:9222), and the dashboard links stuck to-dos to it.
- Needs `tigervnc-standalone-server websockify novnc matchbox-window-manager` and Chrome or Chromium.

### Your desktop's browser from anywhere

When the assistant's browser runs on a desktop you are not sitting at, the dashboard can show that screen live in noVNC and let you use it, from your phone too.

**Setup:**

1. Run a VNC server for the screen that only this computer can reach, ideally on a private unix socket, and set `browser_vnc` to it.
   - Wayland: `wayvnc --config=<file with enable_auth=false> --unix-socket <runtime dir>/vnc.sock` (a wayvnc with `--unix-socket`), with the socket in a 0700 directory, as a user service.
   - X11: for example `x11vnc -localhost -rfbport 5905 -forever -shared` and `browser_vnc` `127.0.0.1:5905`. A 127.0.0.1 port is open to every program on this computer, a unix socket only to you.
2. Get noVNC (your distribution's `novnc` package, or a release from its GitHub project) and build the viewer files with `python3 browser_viewer.py web ~/.local/share/machine-browser/web /path/to/novnc`.

**Using it:** **Open the browser** then opens `https://<dashboard_host>/browser` and brings the task's tab to the front. That short address takes its viewer settings from the dashboard's own noVNC `defaults.json` and `mandatory.json` (noVNC 1.5 or later; with an older one the link is the longer `/browser/vnc.html?...`, which keeps working).

- On Hyprland the view opens on the browser's own window (and focuses it there), fitted to a phone's width. Pinch to zoom, drag with one or two fingers to move around, tap to click, with buttons for the whole screen, zoom and the on-screen keyboard (for a password or a code).
- Elsewhere it opens on the whole screen.

**Security:** only the dashboard's owner gets that page, and the dashboard only connects its websocket for a page on the dashboard's own address, so another site can't use your tailnet identity to reach the screen. The VNC server needs no password of its own as long as only you can open its socket; never put it on a public or tailnet address without one.

### Signing in from a server

X and LinkedIn often refuse sign-ins, or keep asking for checks, from data-center addresses. If The Machine runs on a cloud server, let only its browser go out through a connection at your home or office: start Chrome with `--proxy-server=socks5://127.0.0.1:1055` and point that at Tailscale's userspace SOCKS5 proxy (`tailscaled --tun=userspace-networking --socks5-server=127.0.0.1:1055`, then `tailscale up --exit-node=<your home computer>`), or at a residential proxy of your own. The rest of the server keeps its own route. Sign in once through `x.com/login`; the session stays in the browser profile.

## Reliability and recovery

### Outlook

- Microsoft access tokens and folder lookups are cached per account, connection and credential file version. Reconnecting, or a rotated credential file, makes old cache entries unused.
- Attachment lists follow every Graph page. A response over 40 MB fails clearly rather than leaving a partial file.
- Graph throttling keeps the wait Microsoft asks for (`Retry-After`).
- Removing a tag a signature may not have, when it is a void tag such as `<meta>` or `<input>`, keeps the ordinary HTML after it.

### Google sign-in recovery

- After an expired Google sign-in, use the exact reconnect command shown on Connections, on the computer that runs this collector. It pins the account and client, and the same gog file keyring the service uses.
- While the source waits after a sign-in failure, the collector checks for a renewed sign-in every 15 seconds. It doesn't sleep through the retry hour first. Ordinary throttling and network backoff stay as they are.
- A successful committed sync clears the current warning; the failure stays in Recent syncs and Details. Coming back to the dashboard or getting a connection again refreshes it at once.

### Browser recovery

- An unresponsive managed browser (LinkedIn, X) is restarted only while The Machine holds the exclusive browser lease, and at most once every 15 minutes per browser profile.
- If another job is using the browser, recovery waits for the next sync without using up that 15-minute cooldown.
- It uses the configured lease helper (`browser_lease_script`), and leaves the Gateway, browsers read through their own DevTools address (`browser_cdp`) and real-Chrome extension profiles alone.
