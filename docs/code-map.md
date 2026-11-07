# Code map

[Documentation index](../README.md). For contributors and coding agents: which module owns what, where new code goes,
and the checks that keep it that way. How the parts work together: [Architecture](architecture.md).

The app is a modular monolith in the making. `assistant.py` (the service, `python3 assistant.py serve`) and the
dashboard (`dashboard.html`, served as one page, with most of its script in parts in `dashboard/`) still hold most of
the code. Domains move out of them one at a time, each in its own pull request, with the code moved as is. Until a domain has moved, its code stays where this map says.

## Modules and the tables they own

Every module is flat at the repository root, apart from one package: `machine/`, where the code moving out of
`assistant.py` goes (`machine/store/`, `machine/sources/`, `machine/web/`, ...). Don't add other packages, and don't
name a root folder after a standard library module (`http/` would hide `http.server`). `assistant.py` stays the entry
file (`python3 assistant.py serve`) and keeps the names it hands out for the code and tests that use them. A table belongs to
the module that creates it, in that module's `ensure(db)` (or, for `assistant.py`, in `Store.__init__`). Only the owner
writes it; other modules call the owner's functions.

| domain | modules | tables (owner) |
|---|---|---|
| service core | `assistant.py`: sources and sync, `Store`, `App` (actions, workers), the HTTP `Handler`, notify delivery, prompts | `events` (sealed, the only writer), `suggestions` (to-dos), `decisions`, `deliveries`, `preparations`, `action_jobs`, `analyses`, `profile_runs`, `facts`, `promises`, `voices`, `checkpoints`, `faults` and the rest of its 45 |
| message sealing | `message_seal`, `message_keyring`, `network_crypto` | `event_search` |
| graph and CRM | `graph`, `crm`, `crm_fields`, `crm_import`, `crm_fixes`, `enrichment`, `own_addresses`, `bounces`, `places`, `signatures`, `person_summary`, `project_success` (a project's done-when, its proof and blocker), `knowledge` (what every surface asks about a record, no table) | `graph_*`, `projects`, `boards`, `board_*`, `person_*`, `org_*` (graph); `record_*`, `org_aliases` (crm); `crm_fields`, `crm_tags`, `crm_values`; `person_facts`, `enrich_prefs`, photo and logo tries (enrichment); `own_*`; `email_bounce*`; `person_summar*` (person_summary); `project_success` |
| follow-ups | `follow_ups`, `task_invites`, `task_pages` | `follow_up_*`, `task_pages` |
| recurring to-dos | `recurring`, `recurring_app` | `recurring_series`, `recurring_cards`, `recurring_offers` |
| do it and preparation | `next_actions`, `preparation_state`, `gap_note` (what isn't known about a to-do's people, no table), `agent_jobs`, `agent_remote`, `agents_app`, `codex_signin` (Codex's device sign-in, no table), `calendar_writes`, `calendar_app`, `doc_writes`, `meeting_writer`, `meeting_notes`, `browser_login`, `browser_viewer` | `preparation_runs`, `preparation_calls`, `agent_*`, `meeting_writes`, `meeting_moves` |
| reviews and learning | `learning_loop`, `missed_work`, `missed_work_app`, `corrections`, `corrections_app`, `learnings`, `team_learnings`, `fleet_learnings`, `embeddings`, `gbrain`, `gbrain_app` | `learning_changes`, `missed_audit*`, `team_learning*`, `fleet_learn*`, `event_vector*`, `gbrain_*` |
| chat, talk, voice | `chat_model`, `chat_files`, `file_text`, `talk_live`, `voice_input`, `voice_worker`, `help_chat` | `chat_models`, `chat_fast_sessions`, `chat_files`, `talk_lines`, `draft_seen` (talk_live), `voice_prefs` |
| WhatsApp photos | `whatsapp_images` (Read photos: which chats, keeping a photo, what it says joined to its message), `whatsapp_images_app` | `whatsapp_photos`, `whatsapp_photo_prefs` |
| fleet and network | `fleet`, `fleet_requests`, `fleet_reviews`, `fleet_trust`, `shared_graph`, `shared_graph_app`, `shared_connectors`, `network`, `friends`, `family`, `contact_share`, `discovery`, `meet`, `meet_app`, `security_levels` | `fleet_*`, `network_request_nodes` (fleet); `fleet_reviews` (fleet_reviews); `share_*`, `team_*` (shared_graph); `network_*` (network, discovery); `meet_*` (meet); `contact_*`; `security_prefs` |
| skills, support | `skills`, `skills_app`, `support`, `support_app`, `bug_queue`, `error_feed`, `help_topics` | `skills`, `skill_hints`, `error_feed*`, `help_topics` |
| connected AIs (MCP) | `ai_access`, `ai_app`, `pairing` (one-click pairing, no table), `ai_reach` (the address's certificate and dial-back, no table) | `ai_clients`, `ai_connections`, `ai_codes`, `ai_tokens`, `ai_activity`, `ai_writes` |
| notify, Telegram | `notify`, `telegram_mirror`, `telegram_store`, `pacing` | `notify_*`, `pacing_*`; `telegram_store` keeps its own database (`chats`, `messages`, `outbox`, ...) |
| setup and upkeep | `onboarding`, `installer`, `cli`, `service`, `portable`, `moving`, `work_removal`, `retention`, `rollout_health`; pinned downloads checked by hash: `openclaw_pin`, `telegram_release`, `wacli_release` | `retention_runs`, `sync_daily` |
| shared helpers | `timeutil` (the owner's time zone and hours, `now()`), `models` (which model OpenClaw runs, whether it can), `sources` (`SourceError`, credentials, `gog_read`, mail and calendar accounts), `i18n`, `locale_prefs`, `activity`, `activity_log` (Settings, Activity: reads the other tables, writes only its own), `authorship`, `model_budget`, `model_fallback`, `google_api`, `ms_graph`, `slack_api`, `mail_grants`, `mail_attachments` | `activity_seen`; `activity_accounts` (activity_log) |
| dashboard source | `dashboard_parts` (assembles `dashboard.html` with its parts in `dashboard/`) | none |
| connectors | `connectors/*.py`, `integrations/*.py` | none: they hand events to the service, never SQL |

The full list, computed from the code: `python3 tests/test_architecture.py --owners`.

## Where new code goes

- **A new action** (a dashboard button, a CLI or agent call): in a domain that has an App mixin (`<domain>_app.py`,
  listed in `APP_MIXINS` in `assistant.py`), a line in its `ACTIONS` (`'name': 'method'`) and the method there, called
  as `method(name, args, owner_dashboard)`; `App.action` looks there first. Otherwise its branch in `App.action`, with
  the code it calls in its domain's module when there is one. Either way, add the name to the right `*_ACTIONS` set in
  `machine/actions.py`, one name per line, sorted. Those sets are the security boundary and stay together there;
  a handler still checks `owner_dashboard` itself where its branch did.
- **App methods of a domain** (workers, reads, what its actions call): in its mixin when it has one. A mixin imports
  what it needs like any module, never `assistant`, and only `assistant.py` imports it. The mixins today:
  - `support_app.py` (`SupportApp`): Help and Report a bug.
  - `calendar_app.py` (`CalendarApp`): the Calendar's actions.
  - `skills_app.py` (`SkillsApp`): the skill actions and the skills kept here.
  - `agents_app.py` (`AgentsApp`): Hand to Claude Code / Codex (the hand-off actions and where agents run).
  - `gbrain_app.py` (`GBrainApp`): GBrain on and off, its view and its sync thread.
  - `shared_graph_app.py` (`SharedGraphApp`): the Shared Graph's controls (`GRAPH_SHARE_ACTIONS`).
  - `recurring_app.py` (`RecurringApp`): recurring to-dos (Repeat, Skip this one, the one-time offer) and their worker.
  - `corrections_app.py` (`CorrectionsApp`): fix it where it came from (a chat turn finds where a wrong thing came from
    and fixes it there).
  - `ai_app.py` (`AiApp`): connected AIs: `/mcp`, the OAuth endpoints, the consent page and its tools (`AI_ACTIONS`).
  - `missed_work_app.py` (`MissedWorkApp`): the weekly missed-work audit's background turn and the owner's label on a
    miss (`missed_work_label`).
  - `meet_app.py` (`MeetApp`): scheduling between Machines: the review's meeting request, the other side's to-do, Book it
    as a calendar write with the invite, and the setting (`MEET_ACTIONS`).
  - `whatsapp_images_app.py` (`WhatsAppImagesApp`): Read photos on a WhatsApp connection and the worker that downloads
    and reads each photo.
  - `machine/export/` (with `moving.py`): `inventory.py`, the one list of what an install keeps by part, and `walk()`,
    one iterator over it; `home.py`, OpenClaw's conversations and what else an export takes from outside the data
    folder; `hold.py`, what an import holds so nothing goes out by itself ([moving.md](moving.md)).
  - `machine/app/export.py` (`ExportApp`): Settings, Export: an export in the background, its download, an upload
    to import and its Import now (`EXPORT_ACTIONS`; `machine/export/staged.py` marks a staged import confirmed). Another
    way out is one entry of `EXPORT_OPTIONS` in `dashboard/settings-export.js`.
  - `machine/names.py`: what the owner calls a service, app or agent; every key from data shown on screen goes
    through it, so a tool underneath (gog, wacli, msgraph-cli) is never a name (`tests/test_owner_names.py`).
  - `machine/app/history.py` (`HistoryApp`): the history backfill's worker, when it may run and one step per source;
    `machine/store/history.py` owns `history_backfill` and the line between history and signal (`events.history`).
  - `machine/upkeep/agent_workspaces.py`: the nightly cleanup of Claude Code and Codex job folders nothing needs any
    more (retention.py runs it; it only reads `agent_jobs`, `suggestions` and `agent_relayed`).
  - `machine/app/knowledge_export.py` (`KnowledgeExportApp`): Knowledge for another AI (Settings, General, Export) and its
    one-time download; the format is `machine/export/knowledge.py` ([knowledge-export.md](knowledge-export.md)).
- **A question about a person, organization or project** (who they are, their latest messages, what is open with them,
  when the owner last talked to them), from any surface: through `knowledge.py` with the caller's `Caller`
  (`knowledge.owner()`, or `knowledge.connection(config, area)` for a connected AI), never a query of its own. Add a
  case to `tests/knowledge_eval.py` for every surface that answers it.
- **A new route:** `Handler.do_GET` or `do_POST` inside `App.serve`. JSON reads go through `App` methods; owner-only and
  CSP headers stay as the neighboring routes have them (`tests/test_owner_boundary.py`).
- **A new table:** in its domain module's `ensure(db)`, called from `Store.__init__`, with the functions that write it in
  that same module.
- **A new domain:** a new flat module at the root that the others import. It never imports `assistant`.
- **Code moved out of `assistant.py`:** in its area of `machine/`, in that area's layer (below). Nothing in `machine/`
  imports `assistant` or a module of a higher layer. Moved so far, besides the mixins above: `machine/config.py`
  (`ROOT`, `WORKSPACE`, `DEFAULT_CONFIG`, `LOG`, the brand assets and rule files), `machine/timing.py` (a request's
  timing, `SLOW_REQUEST_SECONDS`), `machine/text.py` (message text: quoted history, bodies, attachments, `clamp`,
  `encoded`, `seal_copy`), `machine/prompts/` (`review.py`: the review prompt, source notes, how facts are worded;
  `profile.py`: the profile, voices, skills, roles, organizations, history and import prompts), `machine/cards.py`
  (how a to-do reads: snooze times, titles, source lines, handoffs, ask and blocker text, controls, to-do states),
  `machine/browser.py` (browser leases, sign-in handoffs, tab peeks, safe links, preparation steps), `machine/chat.py`
  (a to-do's chat: its items, replies, drafts, handoffs and redaction), `machine/faults.py` (the Machine's own errors:
  where they happened, their scrubbed message, the code version and release, the fault log),
  `machine/sources/exclusions.py`, `salesflare.py` and `telegram.py` (the exclusion rules and the Salesflare and
  Telegram sources), `machine/sources/gmail.py` and `calendar.py` (the Gmail and Calendar sources with their sync,
  rooms, guests, owners and write helpers), `machine/model_usage.py` (the model's usage and resets, the Codex app
  server, Node and Telegram environment helpers), `machine/sources/android.py` and `gateway.py` (the Android
  notification feed and the Gateway journal source), `machine/sources/connectors.py` (connector plugins and helpers,
  hosted sign-ins, silent failures, read windows, the connector prompt lines) and `whatsapp.py` (the WhatsApp source),
  `machine/delivery/` (`push.py`: phone pushes, app notices, reminders and setup hints; `telegram.py`: Telegram sends;
  `deliver.py`: the delivery loop, Fleet pushes and uncertain sends), `machine/actions.py` (the `*_ACTIONS` sets: who
  may call which action), `machine/store/core.py` (`StoreCore`: opening the database, its schema, message protection,
  exclusion purges, connect; `Store` in `assistant.py` subclasses it).
- **Dashboard code:** in its area's part in `dashboard/` (`<area>-<what>.js`: shell, todos, settings, graph, calendar,
  connections, help, events, new, fleet), next to the functions it works with, never at the end of the script. The
  page's core is in the `shell-*` parts too: locale and error reports (`shell-core.js`), network and outbox, `render()`
  and `refresh()`, `toast()` and the start (`shell-start.js`), the i18n script's body (`shell-i18n.js`).
  `dashboard.html` itself holds the head (with its small theme script, which runs before paint), the page's
  elements that wrap the parts, and the include lines in order: what the page is made of, at a glance. A new top-level
  statement goes in a part only whole (each part parses on its own). Parts run in the page's order, as they were in
  the one file, so a part may use what an earlier one declares. New UI strings go in every catalog in `i18n/`.
- **Dashboard styles and markup:** the same way, in parts: a stylesheet part `dashboard/<area>-<what>.css` fills a
  line `/*@include dashboard/<name>.css*/` inside the page's `<style>`, a markup part `dashboard/<area>-<what>.html` a
  line `<!--@include dashboard/<name>.html-->` in the markup (`base` is the area of the shared design layer). A
  stylesheet part is whole rules and the parts follow each other in the page's order, so the cascade is the one of the
  whole sheet: a rule that overrides another comes after it, in the same part or a later one. A markup part is whole
  elements. `tests/test_dashboard_parts.py` checks both, and that each include line is in its place. The markup is in
  parts by area (`shell-sidebar.html`, `shell-main.html`, `settings-panels.html`, the dialogs); a new element goes in
  its area's part. The stylesheet
  is in parts already, in the page's order (`base-tokens.css` with the shared design tokens first); some runs still mix
  areas, as the sheet grew: a new rule goes in its area's part, after any rule it overrides.
- **Reading the dashboard's source** (a test, a script): through `dashboard_parts.assemble()` in Python or
  `dashboardPage()` from `tests/dashboard-page.mjs` in Node, never `dashboard.html` itself. The page is served as one
  document, but its source can be split into parts (`dashboard/<name>.js`, `.css` and `.html`, each filling its include
  line in `dashboard.html`), and only the assembled page has them all.
  `scripts/split_dashboard.py readers` rewrites a test that still reads the file. The service serves the assembled
  page (`dashboard_page()`), so the browser, the service worker's offline copy, the ETag and the CSP see one page as
  before; `dashboard/` itself is never served. `scripts/split_dashboard.py split`, `split-css` and `split-html` cut
  the script, the stylesheet and the markup into parts at named anchors, so a rebase re-runs them instead of merging
  moved lines by hand; `verify origin/main` proves the assembled page is byte for byte main's.
- **A big page or script** is split before it nears 450 KiB: Aikido skips big files (some just over 500 KiB already
  go unscanned), so a bigger one ships unchecked (see the size rule below).
- **Markup in the dashboard:** build elements with `make()`, or write markup with ``html`...` `` and put it in the page
  with `setHTML(el, h)`. In ``html`` `` every `${}` is escaped unless it is itself an ``html`` `` result (or `raw()` of
  a vetted constant), so no `esc()` call can be forgotten; `setHTML` takes nothing else. Older renderers that build
  strings with `esc()` move to ``html`` `` one at a time.

## The rules and their checks

Run them with `python3 scripts/test.py test_architecture.py test_message_seal.py test_dashboard_parts.py
test_app_mixins.py` (they run in CI with every suite).

| rule | check |
|---|---|
| Each module defines or imports every global name it uses. A function moved without its import fails here, not with a `NameError` at runtime. Covers every `*.py`, subfolders and tests included. | `tests/test_architecture.py` |
| No module loads `assistant.py`. The service runs it as `__main__`, so an import elsewhere makes a second copy with its own `Store` and globals. The entry points that do so today are listed in `LOADS_ASSISTANT`; tests may. Only `assistant.py` imports `*_app.py` modules. | `tests/test_architecture.py` |
| Each table is created by one module, its owner (today's few shared ones are in `SHARED_SCHEMA`). | `tests/test_architecture.py` |
| Only the owner writes a table. Today's other writers are listed in `OTHER_WRITERS`. That list may only shrink: a new writer fails with the owner's name, and an entry that no longer writes fails until it's removed. | `tests/test_architecture.py` |
| Only `assistant.py` writes `events`, the sealed table (and the sandbox's fixture loader, through the sealed connection). Covers subfolders. | `tests/test_message_seal.py` |
| Nothing reads `dashboard.html` itself; every part in `dashboard/` is included once, its include line is in its place (a script, the stylesheet, the markup), and it is whole (statements that parse on their own, whole rules, whole elements); the service serves the assembled page; Python and Node assemble the same page. | `tests/test_dashboard_parts.py` |
| No action is mapped by two mixins, no member is defined in two of them or in both `App` and a mixin, every handler is a method, every name in `OWNER_ACTIONS` or `DASHBOARD_ACTIONS` reaches a mixin's handler or a branch of `App.action`, no branch of `App.action` names an action a mixin maps (it would never run), and every action the dashboard sends is in `DASHBOARD_ACTIONS` and has a handler. | `tests/test_app_mixins.py` |
| Code in `machine/` imports only from its own layer or the ones below it, and any root module, never with `import *`; `machine/__init__.py` imports nothing. The layers, lowest first: `actions`, `config`, `names`, `text`, `timing`; `browser`, `cards`, `chat`, `faults`, `model_usage`, `prompts`, `sources`; `store`, `upkeep`; `delivery`, `export`, `web`; `app`, `main`. A new area gets its layer in `MACHINE_LAYERS`. | `tests/test_architecture.py` |
| Python files (tests aside) stay under 2,500 lines and 450 KiB. A bigger module is hard to review, and Aikido's scan skips it. `PY_OVER_BUDGET` lists today's bigger files with ceilings that only come down: a file that grows past its ceiling fails, one that shrinks well under it fails until the ceiling is lowered, and one back within the budget fails until its entry is removed. | `tests/test_architecture.py` |
| Every dashboard area in `scripts/i18n_extract.py` resolves. | `tests/test_architecture.py`, `python3 scripts/i18n_extract.py --area <name>` |
| Shipped `.html`, `.css`, `.js` and `.mjs` files stay under 450 KiB. Aikido's code scan skips big files (some just over 500 KiB already go unscanned), so a bigger one ships unchecked, and splitting it later turns up its findings all at once. The dashboard's source has smaller budgets: `dashboard.html` 24 KB, each part in `dashboard/` 160 KB (`.js`), 64 KB (`.css`) or 32 KB (`.html`); a part over its budget is split into another `<area>-<what>` part next to it. `OVER_BUDGET` lists today's bigger files with a ceiling that may only come down. The page as served stays under `PAGE_CEILING` (2,000,000 bytes), raised only on purpose. | `tests/test_architecture.py` |

The table checks read the SQL in each module's strings. A statement whose table name is computed
(`f'DELETE FROM {table}'`) isn't seen, so keep table names literal in new code.

## Moving code out of assistant.py

- Move code as is, one domain per pull request, with no other change in it.
- Keep names that other code or tests use from `assistant` available there until those callers move.
- When the move takes a table's writes along, update `OTHER_WRITERS` in the same pull request.
- Move with `scripts/move_code.py`, so a rebase is a rerun of the script on the newer `assistant.py`, not a merge by
  hand. `move_code.py --export assistant.py machine/text.py message_body QUOTED_MARK` moves top-level functions,
  classes and constants, text unchanged, to the end of the target, and imports them back in `assistant.py` (one name
  per line, sorted). `move_code.py assistant.py <domain>_app.py:<Class> App.<member> ...` moves App methods and class
  attributes to the end of a mixin's class. Each item goes with the comment lines above it; the script checks the text
  is the same. Then add the imports `tests/test_architecture.py` says the moved code lacks. Code that uses a helper
  defined in `assistant.py` stays until that helper has a module of its own.
- Lower `assistant.py`'s ceiling in `PY_OVER_BUDGET` to its new size in the same pull request.
- Tests patch names on `assistant` with `seams.patch_everywhere` (tests/seams.py), never plain `patch.object`: it
  also patches every module of the app that binds the same object, so code moved out of `assistant.py` sees the
  patch too. tests/test_seams.py fails on a plain patch; methods go through the class (`patch.object(a.App, ...)`).
- **Prefer plain modules to mixins.** A mixin still reaches into `App` (`self.store`, `self.config`, other mixins), so
  it moves code without separating it. New domain code goes to a flat module of plain functions that take `db`,
  `config` and the values they need as arguments (`notify.py`, `follow_ups.py`); `App` keeps a thin method that
  passes them in. The mixins above stay until their code moves that way.
- **Shared helpers** go to plain modules of plain functions that take what they need as arguments (`timeutil.py`,
  `models.py`, `sources.py`), never a mixin. `assistant.py` imports their names, so its own code and the
  tests that patch them on `assistant` keep working; state such as the zone or the hours lives in the helper module, so
  a test patches it there (`patch.object(timeutil, 'LOCAL_TZ', ...)`, `patch.dict(timeutil.WORK_HOURS, ...)`). When
  one helper calls another in the same module (`models.has_model` calls `model_ready`), a test that wants the patch
  seen there patches the helper module too.
- **A table's writes** go to its owner module as functions that take `db` (`notify.digest_claim`,
  `follow_ups.add_card`); the caller keeps its transaction. Then remove the caller from `OTHER_WRITERS`.
