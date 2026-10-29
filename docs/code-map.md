# Code map

[Documentation index](../README.md). For contributors and coding agents: which module owns what, where new code goes,
and the checks that keep it that way. How the parts work together: [Architecture](architecture.md).

The app is a modular monolith in the making. `assistant.py` (the service, `python3 assistant.py serve`) and
`dashboard.html` (the whole dashboard, one page) still hold most of the code. Domains move out of them one at a time,
each in its own pull request, with the code moved as is. Until a domain has moved, its code stays where this map says.

## Modules and the tables they own

Every module is flat at the repository root (tools and guards read root `*.py`; don't add packages). A table belongs to
the module that creates it, in that module's `ensure(db)` (or, for `assistant.py`, in `Store.__init__`). Only the owner
writes it; other modules call the owner's functions.

| domain | modules | tables (owner) |
|---|---|---|
| service core | `assistant.py`: sources and sync, `Store`, `App` (actions, workers), the HTTP `Handler`, notify delivery, prompts | `events` (sealed, the only writer), `suggestions` (to-dos), `decisions`, `deliveries`, `preparations`, `action_jobs`, `analyses`, `profile_runs`, `facts`, `promises`, `voices`, `checkpoints`, `faults` and the rest of its 45 |
| message sealing | `message_seal`, `message_keyring`, `network_crypto` | `event_search` |
| graph and CRM | `graph`, `crm`, `crm_fields`, `crm_import`, `crm_fixes`, `enrichment`, `own_addresses`, `bounces`, `places`, `signatures` | `graph_*`, `projects`, `boards`, `board_*`, `person_*`, `org_*` (graph); `record_*`, `org_aliases` (crm); `crm_fields`, `crm_tags`, `crm_values`; `person_facts`, `enrich_prefs`, photo and logo tries (enrichment); `own_*`; `email_bounce*` |
| follow-ups | `follow_ups`, `task_invites`, `task_pages` | `follow_up_*`, `task_pages` |
| do it and preparation | `next_actions`, `preparation_state`, `agent_jobs`, `agent_remote`, `calendar_writes`, `meeting_writer`, `meeting_notes`, `browser_login`, `browser_viewer` | `preparation_runs`, `preparation_calls`, `agent_*`, `meeting_writes`, `meeting_moves` |
| reviews and learning | `learning_loop`, `learnings`, `team_learnings`, `fleet_learnings`, `embeddings`, `gbrain` | `learning_changes`, `team_learning*`, `fleet_learn*`, `event_vector*`, `gbrain_*` |
| chat, talk, voice | `chat_model`, `chat_files`, `talk_live`, `voice_input`, `voice_worker`, `help_chat` | `chat_models`, `chat_files`, `talk_lines`, `voice_prefs` |
| fleet and network | `fleet`, `fleet_requests`, `fleet_trust`, `shared_graph`, `shared_connectors`, `network`, `friends`, `family`, `contact_share`, `discovery`, `security_levels` | `fleet_*`, `network_request_nodes` (fleet); `share_*`, `team_*` (shared_graph); `network_*` (network, discovery); `contact_*`; `security_prefs` |
| skills, support | `skills`, `support`, `bug_queue`, `error_feed`, `help_topics` | `skills`, `skill_hints`, `error_feed*`, `help_topics` |
| notify, Telegram | `notify`, `telegram_mirror`, `telegram_store`, `pacing` | `notify_*`, `pacing_*`; `telegram_store` keeps its own database (`chats`, `messages`, `outbox`, ...) |
| setup and upkeep | `onboarding`, `installer`, `cli`, `service`, `portable`, `moving`, `work_removal`, `retention`, `rollout_health` | `retention_runs`, `sync_daily` |
| shared helpers | `i18n`, `locale_prefs`, `activity`, `authorship`, `model_budget`, `google_api`, `ms_graph`, `slack_api`, `mail_grants`, `mail_attachments` | `activity_seen` |
| connectors | `connectors/*.py`, `integrations/*.py` | none: they hand events to the service, never SQL |

The full list, computed from the code: `python3 tests/test_architecture.py --owners`.

## Where new code goes

- **A new action** (a dashboard button, a CLI or agent call): its branch in `App.action` in `assistant.py`, with the code
  it calls in its domain's module when there is one. Add the name to the right `*_ACTIONS` set in `assistant.py`, one
  name per line, sorted. Those sets are the security boundary and stay together in `assistant.py`.
- **A new route:** `Handler.do_GET` or `do_POST` inside `App.serve`. JSON reads go through `App` methods; owner-only and
  CSP headers stay as the neighboring routes have them (`tests/test_owner_boundary.py`).
- **A new table:** in its domain module's `ensure(db)`, called from `Store.__init__`, with the functions that write it in
  that same module.
- **A new domain:** a new flat module at the root that the others import. It never imports `assistant`.
- **Dashboard code:** next to the functions of its area (the areas in `scripts/i18n_extract.py` `AREAS`: shell, to-dos,
  settings, graph, calendar, connections, help, events, new), never at the end of the script. New UI strings go in
  every catalog in `i18n/`.

## The rules and their checks

Run them with `python3 scripts/test.py test_architecture.py test_message_seal.py` (both run in CI with every suite).

| rule | check |
|---|---|
| Each module defines or imports every global name it uses. A function moved without its import fails here, not with a `NameError` at runtime. Covers every `*.py`, subfolders and tests included. | `tests/test_architecture.py` |
| No module loads `assistant.py`. The service runs it as `__main__`, so an import elsewhere makes a second copy with its own `Store` and globals. The entry points that do so today are listed in `LOADS_ASSISTANT`; tests may. Only `assistant.py` imports `*_app.py` modules. | `tests/test_architecture.py` |
| Each table is created by one module, its owner (today's few shared ones are in `SHARED_SCHEMA`). | `tests/test_architecture.py` |
| Only the owner writes a table. Today's other writers are listed in `OTHER_WRITERS`. That list may only shrink: a new writer fails with the owner's name, and an entry that no longer writes fails until it's removed. | `tests/test_architecture.py` |
| Only `assistant.py` writes `events`, the sealed table (and the sandbox's fixture loader, through the sealed connection). Covers subfolders. | `tests/test_message_seal.py` |
| Every dashboard area in `scripts/i18n_extract.py` resolves. | `tests/test_architecture.py`, `python3 scripts/i18n_extract.py --area <name>` |

The table checks read the SQL in each module's strings. A statement whose table name is computed
(`f'DELETE FROM {table}'`) isn't seen, so keep table names literal in new code.

## Moving code out of assistant.py

- Move code as is, one domain per pull request, with no other change in it.
- Keep names that other code or tests use from `assistant` available there until those callers move.
- When the move takes a table's writes along, update `OTHER_WRITERS` in the same pull request.
