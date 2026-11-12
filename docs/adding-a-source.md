# Adding a source

A source (connector) reads one account of one service and stores what it finds as **events**. Reviews then decide what deserves a to-do.

A connector only reads. It adds no AI interpretation and no writes nobody asked for: no replies, no marking as read. (The opt-in Salesflare account join and Salesforce's opt-in Update contact details, which shows what would change first, are the exceptions, and not a reason to add writes to another source.)

There are two ways to add one:

- **A connector plugin**: one Python file in `connectors/`, named after its service. No changes to `assistant.py`. This is the way for most sources. Examples:
  - [`rss.py`](../connectors/rss.py): a complete, small example.
  - [`github.py`](../connectors/github.py): reads through a CLI.
  - [`stripe.py`](../connectors/stripe.py): an API, filtering what's worth storing.
  - [`trello.py`](../connectors/trello.py): pages an API with cursors and an overlap window.
  - [`intercom.py`](../connectors/intercom.py): reads a search API in frozen windows and allows only its read routes.
  - [`x.py`](../connectors/x.py) and [`linkedin.py`](../connectors/linkedin.py): read through the signed-in browser.
- **A built-in source**: a branch in `sync_source` in `assistant.py`, for sources that need deeper integration (realtime threads, special review handling).

This guide covers the plugin.

## 1. The account in `config.json`

```json
{"id": "work-feed", "service": "rss", "transport": "http", "boundary": "work:Acme",
 "url": "https://example.com/feed.xml", "poll_seconds": 1800}
```

- `id` is the account's own ID. Its checkpoint, health and events are keyed by it.
- `service` picks the connector: `rss` loads `connectors/rss.py`.
- `boundary` (`work:<Company>` or `personal:<name>`) keeps signals apart in reviews and on the dashboard; only `work:` ones count as work (work to-dos wait for a work day). In `SETUP`, a bare `work` makes `assistant connect` ask which company.
- Any other keys (`url` here) are yours to read in the connector. Keep secrets out of `config.json`: name a credential (`"credential": "stripe"`) and read it with `helpers.credential`.

## 2. The module

```python
KINDS = {'rss.item': 'feed'}          # event kind -> short label for to-dos and reviews

def sync(store, config, account, helpers):
    state = store.checkpoint(account['id']) or {}
    ...                                # read new items since state
    store.commit_page(account['id'], state, events)
    return {'mode': 'incremental', 'events': len(events)}
```

The service calls `sync` every `poll_seconds` (default 300) in the account's own thread. `helpers` has:

| Helper | Use |
|---|---|
| `helpers.SourceError(category, status=None, retry_after=None)` | Raise on any failure. `category` is a short label like `rss_http`; it's shown on the dashboard, so never put message content or secrets in it. `retry_after` (seconds) delays the next try. |
| `helpers.Skips(malformed=None)` | Counts the rows a page can't take instead of failing the whole page: `skipped.every(rows, convert)` gives `[(event, row)]` for the rows `convert` took and counts each one it refused with `SourceError` (or, given `malformed`, with a missing field or wrong type) by its label. `skipped.check()` still fails when every row of a page of 10 or more was refused, and `skipped.note(state)` keeps the counts in the checkpoint (`skipped_rows`). Return `'skipped': sum(skipped.values())` so the sync log shows them. A failed read (a network error, an HTTP status) still raises. |
| `helpers.iso(timestamp)` | A Unix timestamp as the UTC ISO string `occurred_at` expects. |
| `helpers.now()` | The current time as that string. |
| `helpers.local_tz()` | The owner's time zone (config `timezone`), for things like active hours. |
| `helpers.credential(config, name)` | The secret named `name` in `config['credentials']` (or systemd's `LoadCredential`), as text. Use it for API keys instead of reading files yourself. |

### Signing in: OAuth first

When the service offers OAuth, the connector signs in with it. Nobody pastes a token or key, and nobody is sent to a developer console, an API explorer or an OAuth playground.

- Reuse The Machine's own sign-ins instead of registering a new app: Google through the token broker ([`google_api.py`](../google_api.py), `transport: broker`), Microsoft through [`ms_graph.py`](../ms_graph.py), Zoom, Slack, Intercom and Stripe through the hosted account pages (`broker`, `account_page`), GitHub through `gh auth login`.
- Ask for the narrowest read-only scopes that do the job. For Google, prefer scopes that aren't restricted or sensitive (`drive.file` over `drive.readonly`), since restricted ones need a security assessment.
- A scope or API call the shared sign-in doesn't allow yet: write the connector for it anyway, and name the scope and calls in the pull request; a maintainer adds them to that sign-in.
- A token or key only when the service has no OAuth, or has OAuth but The Machine has no app for it yet. Say why in `SETUP['no_oauth']` and in the pull request. `tests/test_connectors.py` fails a connector for a known OAuth service that asks for a key or links a developer console without that reason.

### Setup: `assistant connect <service>`

Setup verifies a real read before it saves the account:

- A plugin can define `check(config, account, helpers)`, returning `None` on success or raising `helpers.SourceError` with a content-free label. The check must not write source data or move checkpoints. `Source.verify()` or `Source.profile()` work too.
- Without a read check, setup says verification is unavailable instead of calling the account connected.
- A source that answers it is busy or rate limited (`x_browser_busy`, `linkedin_browser_busy`, `x_rate_limited`) is saved anyway with a note; the first sync reads it.

Declare `SETUP` so the owner can add an account without editing JSON:

```python
SETUP = {'label': 'RSS feed',                          # name in prompts, doctor and next steps
         'account': {'id': 'feed', 'service': 'rss', 'transport': 'http', 'boundary': 'work', 'poll_seconds': 1800},
         'what': 'Posts from the feeds you follow.',     # one line: what it reads, shown next to the source in setup screens
         'note': 'Shown before the questions. Give full https:// links; setup pages make them clickable.',
         'ask': [('url', 'Feed URL (RSS or Atom)')],     # (key, prompt[, default]); defaults can use '{other_key}'
         'detect': {},                                   # key -> command whose output is the default, e.g. ['gh', 'api', 'user', '--jq', '.login']
         'secret': None,                                 # a prompt here asks for a key without echo into the `credential` file (mode 600)
         'no_oauth': None,                               # with a key for a service that has OAuth: why it can't sign in with OAuth (see above)
         'hints': {},                                    # error prefix -> plain fix, e.g. {'myapi:HTTP_401': 'MyAPI rejected the key'}
         'browser': None,                                # for sources read through the shared browser: its site ('linkedin', 'x'); an error ending in _signed_out then shows 'Signed out' with a way to sign in again
         'broker': False,                                # True when a hosting control plane signs it in (Zoom): the Add tab links to that page instead
         'family': None,                                 # e.g. 'MYAPI_': offer keys named MYAPI_…KEY/TOKEN the owner already saved
         'maton': None}                                  # truthy offers reading through Maton instead; the connection is found with the key ('maton_app' names the Maton app if not the service)
```

`assistant connect` then:

1. adds the account from `account` and asks each `ask` key (an empty answer stops it);
2. stores the secret (with `credential_variable` in `account`, as `VARIABLE=value`, leaving other lines in that file as they were);
3. verifies a real read, saves `config.json` and shows the first sync. The running service takes a new account at once (`App.follow_config`); a changed one restarts it.

When the owner already has an account of this service, the new one starts from it instead of `account`, without the identity keys (`id`, `email`, `handle`, `login`, `url`, `connection_id`, … and your first `ask` key). `assistant doctor` treats a missing `ask` key or credential file as not set up.

A test checks every connector has a complete `SETUP`, including its one-line `what` (short enough to fit a tile in two lines). A built-in source's line is in `WHAT` in `onboarding.py`. The dashboard's Add tab and a hosted setup page show the line under the name.

## 3. Events

Use this common event shape; optional metadata is source-specific. Check parsing/validation in the store rather than assuming every provider payload already has this shape:

| Field | Meaning |
|---|---|
| `account_id` | `account['id']`. `commit_page` refuses events for another account. |
| `source_id` | Stable ID of the item in the source. The same item must always get the same ID; hash it if it's long or contains personal data. |
| `kind` | `<service>.<type>`, e.g. `rss.item`. Add it to `KINDS`. |
| `occurred_at` | When it happened, UTC ISO. |
| `title` | A short line (max 1000 chars): subject, chat name, item title. |
| `body` | The text (max 40000 chars). Plain text; strip HTML. Omit one-time codes and passwords. |
| `metadata` | JSON with what reviews need: `source_url` (an https link to open the original, shown as Open), sender, thread or conversation IDs, `from_me` for the owner's own messages. |
| `deleted` | `True` when the item was removed at the source. |

Message text goes in `title`, `body` and metadata only. With [message protection](configuration.md#message-protection) on, `commit_page` seals all three; only the lookup keys `thread_id`, `from`, `to`, `labels`, `from_me`, `user_id`, `channel_id`, `chat_id`, `conversation_id` and `notification_key_hash` and the routing keys `end_at` (a time), `status` (a calendar event's `confirmed`, `tentative` or `cancelled`), `recurring_event_id` (an id) and `chat_kind` (dm, group and the like) stay readable, so keep text out of those (a status in the source's own words gets a name of its own, as Salesforce's `task_status`), `source_id`, `kind` and your cursor. `MESSAGE_SEAL_AUDIT=1` makes `commit_page` refuse an event that does (`test_message_seal.py` runs every connector suite that way). Store only through `commit_page`, never with your own SQL.

When an item changes, send it again with the same `source_id`: the service stores a new version and reviews see it again. Unchanged items are skipped by content hash, so rereading is cheap and safe.

## 4. Checkpoints

`store.commit_page(account_id, state, events)` stores the events **and** the new `state` in one transaction. If the process dies mid-read, the next run starts from the old state and rereads the same page; nothing is lost or doubled.

- Put your cursor in `state`: a page token, a `since` time, an ETag. It's JSON, read back with `store.checkpoint(account_id)`.
- For a long backlog, commit page by page, each with the cursor of the next page.
- When the provider explicitly rejects an expired cursor, record that expiry and replay the supported bounded window (`config.get('bootstrap_days', 7)`) with deduplication. Do not clear a valid retained continuation because a request timed out or was rate limited; disclose any unrecoverable coverage gap.
- On the first run, read only that recent window, not years of history.

## 5. Dashboard and noise rules

- The account appears under Connections with its health, last read and errors.
- Every source has a one-color mark for the small icons in rows (the last check above the to-dos, a to-do's source, search, a record's timeline, chat, learned styles): `dashboard/logos/mono/<service>.svg`, its key in `MONO` in [`dashboard/todos-logos.js`](../dashboard/todos-logos.js) and its source and terms in `dashboard/logos/mono/NOTICE.md`. Take it from the same mark as the colored logo (Simple Icons, CC0, when it has one; else a simplified one-color version), one color with no fill of its own, so it masks in the text's color. [`tests/test_source_icons.py`](../tests/test_source_icons.py) fails for a connector without one. The colored logo for + Add is separate (`dashboard/logos/`).
- `exclude` rules (`senders`, `titles`, `text`) work on plugin events too. See Noise rules in [Configuration](configuration.md).
- Every event opens in the dashboard's message viewer with its title, sender (`sender_display` or `from`, "You" when `from_me`) and body. How it reads there is up to you; see How a message reads below.

### How a message reads

Every kind reads in one of four views ([`machine/store/message_view.py`](../machine/store/message_view.py)). Declare each kind's view and the app its link opens in next to `KINDS`:

```python
VIEWS = {'rss.item': 'card'}   # email, chat, notification or card
APP = 'GitHub'                 # "Open in GitHub"; '' for "Open original"; or {'host.example': 'Name'} by the link's host
```

- **email**: mail. The subject is the title; the sender by name with the address quiet, To and Cc as their own lines, Details for the full addresses. A body that starts with `From:`/`To:` lines has them moved to the header.
- **chat**: a conversation. Turns by who said them, the owner's side (and a support team's) on the right, a bot marked as one.
- **notification**: a phone notification or alert. The app, the time, its title and text, once each.
- **card**: an item with a state (an issue, a task, a deal, a payment, a doc comment, meeting notes). Its title, where it is, a state, who made it, why it reached the owner, the text rendered.

The rules every view keeps, whatever the source sends:

1. No raw ids, Unix timestamps or internal type names on screen. An app's package id (`com.acme.shop`) is never a title, a subject or a sender: the app by its name, or nothing.
2. Nothing said twice across the title, the header, Details and the body.
3. Markup renders (markdown, Slack mrkdwn, sanitized HTML): no literal `**`, backticks or `<url|label>` brackets. Name a markdown kind in `MARKDOWN_KINDS`.
4. People by name where a name exists, and the real author rather than the bot that sent the notification. An address the source sends without a name shows by the name the Graph knows for it, everywhere a sender shows (the viewer, a to-do's source line, the last check's list, a person's Graph timeline); the address only when no name is known. When your `from` is an address, put the name the service gives next to it (`from_name`, `sender_display`, `contact_name` or `customer_name`; `NAME_KEYS`), never an address as that name: `sender_name` in [`machine/store/message_view.py`](../machine/store/message_view.py) reads it. A relay or bot address (Intercom's `operator+…@intercom.io`, a noreply) never shows outside email: the customer by name when the source names one, else the bot or teammate by the name the service gives.
5. A short title, whole: no `[repo]` prefixes, never cut mid-word.
6. Long bodies fold behind Show more.
7. "Open in …" sits left, under the content, for every kind.

[`tests/test_message_view.py`](../tests/test_message_view.py) fails a connector without `VIEWS` and `APP`, and a kind without a made-up message in its `SAMPLES`, which it then checks against these rules; [`tests/test_message_view_dashboard.mjs`](../tests/test_message_view_dashboard.mjs) opens each one in the viewer and checks what shows.
- To tell reviews how to read your source (what is noise, when it needs the owner, how a reply goes out), add `source-notes/<service>.md`: one bullet like the others there. Reviews and Do it runs get it only on Machines that have that source connected; `AGENTS.md` keeps the rules for every source.
- To put the people in your events on the Graph tab, add a branch for your `kind` to `touches()` in [`graph.py`](../graph.py): it returns who took part, with a stable identifier (`email:`, `wa:`, or your own prefix), a name and their role (you wrote to them, they wrote to you, a meeting, or just present). Without it the source works as before; it just adds no people.

## 6. Tests

Test with saved fixtures, not live accounts, in `tests/test_connector_<service>.py`. [`tests/test_connectors.py`](../tests/test_connectors.py) shows the pattern for `rss.py`: it fakes the HTTP response and checks

- the events and their fields,
- that a second run with the same feed adds nothing,
- that `304 Not Modified` keeps the checkpoint,
- that errors raise `SourceError` with a safe label.

After fixture tests, the owner can run `assistant connect <service>`: setup verifies the account, the running service starts reading it (a changed account restarts it) and setup shows its first read. A busy source remains explicitly unverified until that read succeeds. Check it later with `assistant sources`, `assistant doctor` or on the dashboard.

## 7. Help article and translations

A connector is a feature people see, so it ships with what every feature ships with (see [CONTRIBUTING](../CONTRIBUTING.md#pull-requests)):

- A help article, `docs/help/<service>.md` (dashes for underscores), in the form of [`docs/help/rss.md`](help/rss.md): `covers: connector:<service>` and `code: connectors/<service>.py` in its front matter, then what it reads, what it can do, how to connect it and how to remove it. The same article in every other language, under `docs/help/<language>/`.
- Every text it shows (`SETUP` and `KINDS`) in every string catalog in `i18n/`: `python3 scripts/i18n_extract.py --add` adds the English, then translate it in each language following `i18n/glossary.md`, and run `python3 scripts/i18n_extract.py --sort`. Add strings only; never change one that is there.

Before you open the pull request, run the checks it would fail on, not only your own tests:

```sh
python3 scripts/test.py test_connector_<service>.py test_connectors.py test_new_connectors.py test_i18n.py test_help.py test_us_english.py
```

## Checklist

- [ ] OAuth through The Machine's existing sign-ins when the service has it, with the narrowest scopes; a key only with `no_oauth` saying why.
- [ ] Read-only credential for exactly this account, with the least access that works.
- [ ] Stable `source_id`; `kind` listed in `KINDS`, its view in `VIEWS`, its app in `APP`, and a made-up message of it in `tests/test_message_view.py`.
- [ ] Message text only in `title`, `body` and metadata, never in ids, lookup keys or the cursor.
- [ ] Events and cursor committed together; replays don't duplicate.
- [ ] Failures raise `SourceError` with a content-free label.
- [ ] Fixture tests for parsing, replays, expired cursors and errors.
- [ ] `SETUP` with what `assistant connect` should ask, plus a supported read-only setup check.
- [ ] Reading notes in `source-notes/<service>.md` when reviews need to know more than the event says.
- [ ] A one-color mark in `dashboard/logos/mono/` and `MONO` (`test_source_icons.py`).
- [ ] A help article in every language and every text it shows in every catalog, with `test_i18n.py` and `test_help.py` passing.
