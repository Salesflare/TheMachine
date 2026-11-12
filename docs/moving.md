# Export and import

Everything your AI learns belongs to you. You can take it all with you, also when you stop using The Machine.

`assistant export` (or Settings, Export) writes one encrypted file with everything The Machine knows and has done.
`assistant import` puts it back on a fresh install, self-hosted or hosted, without losing anything. How to run them:
[operations.md](operations.md#moving-to-another-computer). Code: `moving.py` and `machine/export/`.

## What is in it

`machine/export/inventory.py` is the one list of what a Machine keeps, by part. The export, the import and any other way
out read from it.

| Part | What |
|---|---|
| messages | Messages from every source (`events`), their sync state, bounces, Telegram chats, meetings |
| conversations | OpenClaw's conversations, transcripts, memory index, scheduled jobs and plugin memory |
| todos | To-dos with their history and events: moves, reviews, recaps, snoozes, preparations, follow-ups, recurring to-dos |
| drafts | Drafts with their edits, sends and their undo history, calendar and doc writes, the X and LinkedIn send logs |
| decisions, promises | Decisions with their notes, promises with their log |
| memories | Facts, person summaries, notes |
| preferences | What it learned: rules, voices, pacing, security and notification choices |
| graph | People, organizations, projects, boards, CRM fields, merges and your edits |
| skills | Skills, hints and the workshop's skills |
| agents | Agent jobs, their folders, and Claude Code's and Codex's transcripts of their sessions |
| attachments | Chat files, email attachments, WhatsApp photos, photos and files in OpenClaw's chats |
| sharing | Fleet, Network, shared Graph and AI connections |
| activity | Activity, faults, error reports, notifications |
| settings | `config.json`, your own connectors |
| workspace | Your OpenClaw workspace (`AGENTS.md`, `USER.md`, memory notes) |
| index | Search and similarity indexes (rebuilding them would take hours) |

Ids, links between records, timestamps and edit and undo history are the rows themselves, so they come back as they
were.

## The manifest

`manifest.json` is the last file in the archive:

- `parts`: per part, its label and how many tables, rows, files and bytes;
- `tables`: per `<database>/<table>`, its part, row count and a sha256 over its rows in a stable order;
- `files`: per file in the archive, its size and sha256 (an import checks them all before it replaces anything);
- `not_exported`: what could not come along, why, and what to do after the import;
- `left_out`: what a computer rebuilds (packages, caches, older copies, deleted conversations), with sizes.

## What is not exported

- Sign-ins to Google and Microsoft through the hosted service: they only work there.
- Your AI plan sign-in and API keys, Telegram, Slack and other source tokens, and the Network identity, unless you
  include keys (with a passphrase you pick). OpenClaw's own sign-in tables are emptied in the copy too.
- WhatsApp's device link: WhatsApp links one device at a time. Link it again; your messages are in the export.
- AI connections (ChatGPT and Claude connectors) and phone notifications: their tokens are for the old address.
- Conversations you deleted, installed programs, caches and browser sessions.

## Credentials

Only on request: `assistant export --keys`, or the Include keys and tokens choice in Settings. Keys need a passphrase
you pick; an export code alone never carries them. The whole archive is encrypted either way (AES-256 with PBKDF2).

## After an import

`machine/export/hold.py` runs once, before the service starts on the imported data:

- Sends that were queued are blocked with "Not sent: The Machine moved to this computer." Their to-dos show Send again.
  One that was going out at that moment is uncertain and never resent. The Telegram and Signal chats' outboxes stop the same way.
- Local agent jobs that ran or waited end with their work kept in their folder.
- Automated follow-ups are paused on every board that has them, until you resume them.
- Notifications for the old Machine are dropped; without keys, so are AI connector tokens and phone sign-ups.
- `moved_in` records the export's moment. What a source brings in after the move that happened before it is history
  (`machine/store/history.py`), never a signal: no review, first look or to-do picks up an old message again.

## Documented differences after a round trip

`tests/test_export_roundtrip.py` exports a fully seeded install, imports it into a fresh one and compares every table
and file. Apart from the hold above (`action_jobs`, `deliveries`, `agent_jobs`, `activity_blocks`, `follow_up_pauses`,
`notify_queue`, `ai_tokens`, `ai_codes`, `push_subscriptions`, `moved_in`, the Telegram `outbox`) they are the same.
Also different by design: message text is opened in the export and sealed again with the new install's own key, and
OpenClaw's sign-in tables keep the new install's own sign-ins, and `data_stamps` (change counters for answers kept
between requests) counts the hold's own changes.

`tests/test_export_complete.py` fails when the code creates a table, or writes to a place under the home folder,
that the inventory doesn't name, so the export stays complete as The Machine grows.

## Reading an export's data in code

`machine.export.inventory.walk(config_path, workspace=None, openclaw_home=None)` is one iterator over everything an
install keeps: each row of each table (`Item(kind='row', part, db, table, row)`, message text opened) and each file
(`Item(kind='file', part, path, name)`). Keys are never in it. It streams, so it runs on a small hosted Machine.
