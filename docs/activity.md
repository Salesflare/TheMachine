# Activity

One list of everything The Machine did for its owner, newest first: Settings, **Activity** (`activity_log.py`,
`dashboard/settings-activity.js`, `GET /api/activity`). What the owner sees is in [the help article](help/activity.md).

It is read-only. It reads what each part already keeps and adds no step, check or permission to any action. It never
changes what The Machine or a coding agent may do.

## Where each line comes from

| kind | what | source (owner) |
|---|---|---|
| `messages` | emails, replies and messages on every channel; auto follow-ups; blocked, failed, undone and canceled ones | `action_jobs` (assistant.py), `follow_up_sends` |
| `docs` | docs created or edited | `action_jobs` (`doc_write`; a reply in a doc is a message) |
| `calendar` | calendar changes | `action_jobs` (`calendar`) |
| `web` | steps on the web (Do it's browser steps) | `action_jobs` (`finish`) |
| `fixes` | fixes The Machine merged by itself | `action_jobs` (`merge`, source `auto`) |
| `agents` | work handed to Claude Code or Codex | `agent_jobs` |
| `fleet` | questions and requests to and from teammates, with what the rules answered or declined | `fleet_log` (fleet.py) |
| `learnings` | learnings sent to The Machine team (with Withdraw), withdrawn ones, votes | `team_learnings`, `team_learning_votes` |
| `skills` | skills added, the owner's or a teammate's | `skills` |
| `graph` | imports into the Graph, undone ones | `graph_imports` (crm.py) |
| `connections` | a connection added or removed | `activity_accounts` (this module: a snapshot of the configured accounts, taken when the service starts and on each read) |
| `access` | each look by The Machine team under Support access, and refused ones | the control plane (`/_machine/support-access`) or the Fleet (self-hosted); the dashboard adds them from what Settings, Security reads |
| `ai` | calls from AIs connected over MCP, refused ones included | the MCP module, through `register('ai', read)` |

Each source stays the owner of its table; `activity_log` only reads them (`tests/test_architecture.py`).

## One list, not two

- **Fleet, Activity** shows this list for `kind=fleet,learnings`, with Withdraw on a learning. Its old Log and "Sent to
  The Machine team" boxes are gone.
- **Settings, Security, Support access** links to this list filtered to `access` instead of keeping its own log.
- **A to-do's chat** keeps its own event lines (the story of that to-do); each line here links to its to-do, and a done
  one opens through `GET /api/cards/done?id=`.
- **What I've learned, Recent changes** stays: it is what The Machine learned, not something it did.
- **An AI connection's own activity** (Settings, Connected AIs) is this list with `actor=<connection id>`.

## The line

Every source returns lines of one shape (`activity_log` docstring):

```
{'id': '<kind>:<the source's own id>', 'kind': one of KINDS, 'at': ISO time,
 'what': one line in the owner's language, never starting with "You",
 'where': the account or app, or None, 'outcome': 'done' | 'refused' | 'failed' | 'undone' | 'pending',
 'status': the outcome in a word or two, 'by': who started it, or None,
 'actor': optional stable id of who did it (an AI connection), 'todo': {'id', 'title'} or None,
 'detail': an optional second line}
```

`outcome: 'refused'` is what the **Refused or blocked** filter shows: a send a check stopped, a Fleet question a rule
declined, a refused look, an AI call above its access.

## Adding a source

```python
import activity_log

def calls(db, limit):          # newest first, at most limit lines, in the shape above
    for row in db.execute('SELECT ... ORDER BY at DESC LIMIT ?', (limit,)):
        yield {'id': f"ai:{row['id']}", 'kind': 'ai', 'at': row['at'], 'what': row['tool'], 'where': row['client'],
               'outcome': 'refused' if row['refused'] else 'done', 'status': row['said'], 'by': None,
               'actor': row['connection'], 'todo': None, 'detail': None}

activity_log.register('ai', calls)
```

A new kind also needs its label in `ACT_KINDS` (settings-activity.js) and in the i18n catalogs. A source that fails is
logged by its kind and left out; the rest of the list still shows. Sealed columns are opened by the source itself.

## Paging

`GET /api/activity?kind=&outcome=&actor=&cursor=` answers `{'items', 'next', 'kinds'}`, 50 lines a page, newest first.
Each source reads only as far as the page needs (`offset + limit + 1`), at most 2000 lines back. `kinds` lists the kinds
this Machine has lines for, so the filter only offers those.
