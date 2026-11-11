# Knowledge for another AI: the format

Everything an owner's Machine learns belongs to them. **Knowledge for another AI** (Settings, General, Export, or
`assistant export-knowledge`) writes it as plain, open files any AI or person can read without The Machine:
Markdown for reading, JSONL for records, CSV for tables. This page is the schema. Help article:
[docs/help/knowledge-export.md](help/knowledge-export.md). The full export to move a Machine is a different thing
(`assistant export`, [operations.md](operations.md#moving-to-another-computer)).

Code: `machine/export/knowledge.py` (collect, render, zip, encrypt), `machine/export/coverage.py` (where every table
goes, or why it stays out), `machine/app/knowledge_export.py` (the dashboard action and its one-time download),
`cli.py` (`export-knowledge`). Tests: `tests/test_knowledge_export.py`, with `tests/knowledge_export_eval.py`, a reader
that knows nothing of The Machine and answers questions from the folder alone.

## Version

`manifest.json` has `"format": "the-machine-knowledge"` and `"schema_version": 1`. A change that removes or renames a
field, or changes what one means, raises the version. Adding a field or a file does not; readers ignore what they don't
know. Dates are ISO 8601 (`2026-11-03`, or `2026-11-03T09:15:00+00:00` with a time, UTC).

## Layout

```
the-machine-knowledge/
  README.md              what this is, the layout and how an AI should use it
  manifest.json          format, schema_version, created_at, options, left_out counts, counts, files
  owner/profile.md       the owner: preferences, facts, rules, how they write, signatures, their promises
  people/<slug>.md       one page per person
  organizations/<slug>.md
  projects/<slug>.md
  skills/<slug>.md       one procedure per file
  team-briefs/<slug>.md  the latest brief of each work team
  notes/                 the chat's own notes (USER.md, MEMORY.md, memory/*.md), when there are any
  records/*.jsonl        every record, one JSON object per line
  tables/*.csv           contacts, organizations, todos, promises
```

The download is a zip with this folder at its root, or that zip encrypted with a passphrase (`.zip.enc`: OpenSSL
`enc -aes-256-cbc -pbkdf2 -iter 600000 -md sha256`, the same as the full export; open it with
`openssl enc -d -aes-256-cbc -pbkdf2 -iter 600000 -md sha256 -in <file> -out knowledge.zip`).

## Ids

Every record has a stable `id`; records point at each other by id.

- Entities: `email:<address>` or another identity for a person, `org:<domain>` for an organization, `project:<n>` for a project.
- Sources: `m-` and 16 hex characters, the same for the same message in every export.
- Others: `fact-<n>`, `rule-<n>` (one keeps its id when it moves to `fact_history.jsonl`), `style-<channel>`, `promise-<n>`, `todo-<id>`, `skill-<slug>`, `brief-<fleet>`, `summary-<entity>-<n>`.

## Records

`said_by` is `owner` (the owner said or wrote it), `the-machine` (learned by the owner's Machine) or `ai:<name>` (saved
by a connected AI). `sources` is a list of source ids.

| File | One line is | Fields |
|---|---|---|
| `entities.jsonl` | a person, organization or project | `id`, `kind` (person, org, project), `name`, `file`, `last_contact`; `tags`, `fields` (custom fields, name to value), `owned_by` (a teammate's record); person: `emails`, `phones`, `organization`, `organization_name`, `role`, `title`, `location`, `side` (work, personal), `closeness`, `next_meeting`, `notes`; org: `domain`, `domains`, `role`, `about`; project: `board`, `stage`, `stage_reason`, `next_step`, `notes`, `state`, `closed`, `value`, `outcome`, `close_date`, `sources`. Empty fields are left out |
| `relationships.jsonl` | a link between two entities | `from`, `to` (entity ids), `kind` (member, project, together, relation), `label` (reads "from label to": works at, works on, often together with, or the owner's words), `strength`, `last_at`, `said_by`, `sources` |
| `facts.jsonl` | something known | `id`, `text`, `sort` (fact, preference, commitment, event), `about` (entity ids; empty is the owner), `side`, `said_by`, `said_at`, `learned_at`, `valid_until`, `sources` |
| `rules.jsonl` | a rule the owner's drafts follow | `id`, `text`, `applies_to`, `said_by`, `said_at`, `learned_at`, `sources` |
| `fact_history.jsonl` | a fact or rule that no longer holds | `id` (`fact-<n>` or `rule-<n>`), `kind` (fact, rule), `status` (ended: past its end day or overturned by a newer message; set_aside: not used lately; merged: a newer one took its place; moved: into a skill, a writing style or a person's record), `text`, `sort`, `about`, `side`, `said_by`, `said_at`, `learned_at` (saved), `valid_until`, `ended_at`, `set_aside_at`, `merged_at`, `replaced_by` (the id of what took its place: a fact, rule, skill, writing style or entity; empty when that is not in the export), `sources`. One the owner forgot is never here, nor what was merged into it |
| `writing_style.jsonl` | how the owner writes on one channel | `id` (`style-<channel>`), `channel`, `text`, `said_by`, `updated_at` |
| `signatures.jsonl` | a mailbox's signature | `account`, `text`, `html`, `source`, `updated_at` |
| `skills.jsonl` | a procedure | `id`, `slug`, `name`, `description`, `body` (Markdown steps), `status` (on, off), `origin`, `version`, `updated_at` |
| `summaries.jsonl` | a summary line about an entity | `id`, `about`, `kind`, `text`, `said_by`, `sources`, `facts`, `promises` |
| `promises.jsonl` | a promise | `id`, `direction` (mine: the owner promised; theirs: promised to the owner), `who`, `what`, `due`, `state`, `made_at`, `about`, `todo`, `together`, `sources` |
| `todos.jsonl` | an open to-do | `id`, `title`, `text`, `status`, `due`, `snoozed_until`, `area`, `project`, `about`, `created_at`, `sources` |
| `team_briefs.jsonl` | a work team's latest brief | `id`, `fleet`, `text`, `built_at` |
| `sources.jsonl` | a message something came from | `id`, `kind` (like gmail.message), `at`, `account`, `provider_id`, `thread`, `side`, `about`; `title`, `sender` and `text` only with message text on |

## Tables

| File | Columns |
|---|---|
| `contacts.csv` | id, name, organization, role, title, emails, phones, side, closeness, last_contact, tags, file |
| `organizations.csv` | id, name, domain, role, last_contact, tags, file |
| `todos.csv` | id, title, status, due, area, project, created_at, about |
| `promises.csv` | id, direction, who, what, due, state, made_at |

Several values in one cell are separated by `; `.

## What goes in, and what stays out

- Never: passwords, keys, tokens, sign-ins. Text that looks like a key anywhere in the export reads
  `[removed: looked like a key]`.
- Forgotten: a fact or rule the owner removed is not in the export, also not in `fact_history.jsonl`, and
  neither is what was merged into it.
- Message text: off by default. Then `sources` holds only ids, kinds, dates, mailbox and thread, enough to find the
  message in the owner's own mailbox.
- Private and Careful: off by default. Then Only-you projects and what is only on them, private or sensitive threads
  and what came only from them, and teammates' records and briefs of Careful Fleets are left out. `manifest.json`
  `left_out` counts them.
- Out always: other Machines' and teammates' data, settings, photos, proposals the owner has not taken on, and how
  The Machine runs (queues, logs, caches). `machine/export/coverage.py` lists every table with where it goes or why it
  stays out, and `tests/test_knowledge_export.py` fails on a new table that is in neither.
