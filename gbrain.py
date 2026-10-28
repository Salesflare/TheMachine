"""GBrain (optional): The Machine and the owner's own GBrain memory (github.com/garrytan/gbrain), both ways.

Off unless the owner turns it on in Connections, + Add, GBrain, and agrees to what goes in (config.json `gbrain`:
{on, consent_at, work, linked, bin}). Off, nothing here runs: no sync, no CLI call, no extra review tool
(the OpenClaw plugin's review gate reads the same `gbrain` key, review-recovery.ts reviewTools).

On:
- Link: the GBrain CLI the owner installed (GBRAIN_BIN, ~/.bun/bin/gbrain or PATH) is registered with OpenClaw as the
  MCP server `gbrain` (`openclaw mcp add`, only GBrain's read tools: READ_TOOLS), unless OpenClaw already has it (the
  owner's own `openclaw mcp add` or GBrain's OpenClaw plugin): then that one is used and left as it is. Turning off removes
  only a registration The Machine made. The brain itself (~/.gbrain or GBRAIN_HOME) is never touched.
- Reviews: may call GBrain's read tools (gbrain__search, gbrain__get_page, ...), never its write tools.
- Push: people, and with Work on also organizations and projects, become GBrain pages (people/, companies/,
  projects/), each with one section The Machine writes between MARK_START and MARK_END and a link back to its Graph
  page; what The Machine learned from the owner's notes goes to one page (LEARNINGS_SLUG). Only the Machine's section
  changes, with GBrain's revision check, so the owner's own text on a page is never overwritten. An owner who edits or
  removes that section keeps it that way: The Machine stops writing it (state 'kept'). An existing page about the same
  person (same email or name, GBrain's whois) gets the section instead of a second page. Incremental: a record whose
  section did not change costs no call.
- Pull: what the owner wrote on those pages outside the Machine's section comes back as a short note per record
  (gbrain_notes), shown to reviews and preparations with the Graph, as the owner's notes (data, not instructions).
  It stays on this Machine: the Shared Graph never sends it.

Boundaries: Personal people only, unless the owner turns Work on. Never a record a teammate owns (Work Fleet, crm
owner), nothing from teammates' shared records (team_* tables are never read), never message text, subjects, quotes
or drafts: only what the Graph says about someone (name, organization, role, title, how close, last contact date),
the owner's own notes on the record and the projects around it."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import unicodedata
import uuid
from pathlib import Path

# GBrain's read operations reviews may use (scope read, not mutating, in GBrain's operation manifest). Never put_page,
# remember, delete_* or any other write. The OpenClaw plugin keeps the same list (review-recovery.ts GBRAIN_READ_TOOLS).
READ_TOOLS = ('search', 'query', 'get_page', 'list_pages', 'get_links', 'get_backlinks', 'get_timeline', 'get_tags', 'whois',
              'recall', 'resolve_slugs', 'get_brain_identity')
SERVER = 'gbrain'           # the MCP server name in OpenClaw: tools are gbrain__<name>
PLUGIN_ID = 'gbrain-context-engine'  # GBrain's own OpenClaw plugin, when the owner installed it
MARK_START = '<!-- the-machine:start -->'
MARK_END = '<!-- the-machine:end -->'
LEARNINGS_SLUG = 'the-machine/learnings'
SYNC_EVERY = 1800           # seconds between rounds
SYNC_SOON = 120             # while pages are still waiting to go in
MAX_WRITES = 25             # pages written per round (each GBrain call takes a second or two): a big Graph goes in over a few rounds
MAX_PULLS = 40              # pages read back per round
WRITE_WAIT_MS = 25000       # how long GBrain may take to commit a write before it answers write_pending
MAX_PEOPLE, MAX_ORGS, MAX_PROJECTS = 600, 200, 200
MIN_STRENGTH = 0.3          # occasional contact or closer (graph.closeness)
NOTE_CHARS = 600
CALL_TIMEOUT = 60
SCHEMA = '''
CREATE TABLE IF NOT EXISTS gbrain_pages(node_id TEXT PRIMARY KEY,slug TEXT NOT NULL,section TEXT NOT NULL,state TEXT NOT NULL,
  revision TEXT,at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS gbrain_notes(node_id TEXT PRIMARY KEY,slug TEXT NOT NULL,text TEXT NOT NULL,at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS gbrain_meta(key TEXT PRIMARY KEY,value TEXT);
'''


class BrainError(ValueError):
    """GBrain or OpenClaw said no, or did not answer. `code` is a short label, never page text."""
    def __init__(self, code, message=None):
        self.code = code
        super().__init__(message or code)


class Conflict(BrainError):
    """The page changed since it was read: tried again next round."""


def ensure(db):
    db.executescript(SCHEMA)


def settings(config):
    value = (config or {}).get('gbrain')
    return value if isinstance(value, dict) else {}


def on(config):
    """On only when the owner turned it on and agreed to what goes in. Everything else in this module waits for this."""
    s = settings(config)
    return s.get('on') is True and bool(s.get('consent_at'))


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


# --- The CLI and OpenClaw ------------------------------------------------------------------------------------------

class Brain:
    """The owner's GBrain through its own CLI (`gbrain call <tool> <json>`), and its link in OpenClaw."""

    def __init__(self, config, run=subprocess.run, which=shutil.which, environ=None):
        self.config, self.run, self.which = config or {}, run, which
        self.environ = os.environ if environ is None else environ

    def binary(self):
        given = settings(self.config).get('bin') or self.environ.get('GBRAIN_BIN')
        home = Path(self.environ.get('HOME') or Path.home())
        for path in (given, str(home / '.bun' / 'bin' / 'gbrain'), self.which('gbrain')):
            if path and os.path.isfile(path) and os.access(path, os.X_OK):
                return str(Path(path).resolve())
        return None

    def openclaw(self):
        return str(self.config.get('openclaw') or self.which('openclaw') or 'openclaw')

    def brain_path(self):
        """Where the brain lives (GBrain's own rule: $GBRAIN_HOME/.gbrain, else ~/.gbrain)."""
        base = self.environ.get('GBRAIN_HOME') or self.environ.get('HOME') or str(Path.home())
        return str(Path(base) / '.gbrain')

    def _env(self):
        env = dict(self.environ)
        env.pop('GBRAIN_SOURCE', None)  # a pinned source would scope every read and write to it
        return env

    def _run(self, argv, timeout=CALL_TIMEOUT):
        try:
            return self.run(argv, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL, env=self._env())
        except subprocess.TimeoutExpired:
            raise BrainError('timeout') from None
        except OSError:
            raise BrainError('not_found') from None

    def version(self):
        binary = self.binary()
        if not binary:
            return None
        out = self._run([binary, '--version'], 30)
        found = re.search(r'\d+(?:\.\d+){1,3}', out.stdout or '')
        return found.group(0) if out.returncode == 0 and found else None

    def call(self, tool, params):
        binary = self.binary()
        if not binary:
            raise BrainError('not_installed')
        if tool in WRITES:  # the same request_id for the same write: a retry finishes a write GBrain queued (write_pending)
            params = {**params, 'wait_ms': WRITE_WAIT_MS,
                      'request_id': str(uuid.uuid5(uuid.NAMESPACE_URL, 'the-machine:' + json.dumps(params, sort_keys=True)))}
        out = self._run([binary, 'call', tool, json.dumps(params, ensure_ascii=False)])
        return answer(out.returncode, out.stdout, out.stderr)

    # OpenClaw's MCP registry: `openclaw mcp show/add/unset` (docs/cli/mcp/registry.md there)
    def server(self):
        out = self._run([self.openclaw(), 'mcp', 'show', SERVER, '--json'], 60)
        data = parse_json(out.stdout)
        return data if out.returncode == 0 and isinstance(data, dict) and not data.get('error') else None

    def plugin(self):
        out = self._run([self.openclaw(), 'plugins', 'inspect', PLUGIN_ID, '--json'], 60)
        return out.returncode == 0

    def link(self):
        """'existing' when OpenClaw already has GBrain (left as it is), else 'machine' after adding it read-only."""
        if self.server() or self.plugin():
            return 'existing'
        binary = self.binary()
        if not binary:
            raise BrainError('not_installed')
        argv = [self.openclaw(), 'mcp', 'add', SERVER, '--command', binary, '--arg', 'serve', '--include', ','.join(READ_TOOLS), '--no-probe']
        if self.environ.get('GBRAIN_HOME'):
            argv += ['--env', 'GBRAIN_HOME=' + self.environ['GBRAIN_HOME']]
        out = self._run(argv, 120)
        if out.returncode != 0:
            raise BrainError('openclaw_add_failed', 'OpenClaw did not add GBrain')
        return 'machine'

    def unlink(self):
        """Remove the registration only when The Machine made it and it still runs the same GBrain."""
        if settings(self.config).get('linked') != 'machine':
            return False
        found = self.server()
        if not found or str(found.get('command') or '') != str(settings(self.config).get('bin') or self.binary() or ''):
            return False
        return self._run([self.openclaw(), 'mcp', 'unset', SERVER], 60).returncode == 0


def parse_json(text):
    """The JSON document in a CLI's output (the last line that parses, or the whole text)."""
    text = (text or '').strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except ValueError:
        pass
    start = text.find('{')
    if start >= 0:
        try:
            return json.loads(text[start:])
        except ValueError:
            pass
    for line in reversed(text.splitlines()):
        try:
            return json.loads(line)
        except ValueError:
            continue
    return None


WRITES = ('put_page',)


def answer(returncode, stdout, stderr=''):
    """A `gbrain call` result: its JSON (stdout, whatever the exit code); None for a page that isn't there; Conflict when
    the page changed or a write is still queued (both: again next round); BrainError otherwise."""
    data = parse_json(stdout)
    if returncode == 0 and not (isinstance(data, dict) and data.get('error')):
        return data
    code = error_code(data) or error_code(parse_json(stderr)) or ('write_pending' if returncode == 10 else 'failed')
    if re.search(r'not_?found', code, re.I):
        return None
    if re.search(r'revision|conflict|stale|pending', code, re.I):
        raise Conflict(code[:80])
    raise BrainError(code[:80])


def error_code(data):
    if not isinstance(data, dict):
        return None
    if isinstance(data.get('code'), str) and data['code']:
        return data['code']
    error = data.get('error')
    if isinstance(error, dict):
        return str(error.get('code') or error.get('class') or error.get('type') or 'failed')
    return error if isinstance(error, str) and error else None


def page_content(page):
    """(markdown, revision) of a get_page answer, or (None, None) when the page isn't there."""
    if not isinstance(page, dict):
        return None, None
    content, revision = page.get('content'), page.get('revision') or page.get('knowledge_revision')
    return (content if isinstance(content, str) else None), (str(revision) if revision else None)


# --- What goes in ------------------------------------------------------------------------------------------------

def slugify(name):
    text = unicodedata.normalize('NFKD', str(name or '')).encode('ascii', 'ignore').decode().lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:60].strip('-') or 'unnamed'


def digest(text):
    """Of a section's words, so GBrain re-saving a page (its own front matter, line endings) doesn't look like an edit."""
    return hashlib.sha256(' '.join(str(text).split()).encode('utf-8')).hexdigest()[:32]


def graph_link(config, node_id):
    host = str((config or {}).get('dashboard_host') or '')
    if not host:
        return None
    import urllib.parse
    return 'https://' + host + str(config.get('dashboard_path') or '/') + '#graph/' + urllib.parse.quote(node_id, safe='')


def _info(row):
    try:
        value = json.loads(row['info'] or '{}')
    except (TypeError, ValueError):
        value = {}
    return value if isinstance(value, dict) else {}


def _day(value):
    return str(value or '')[:10] or None


def _closeness(value):
    return 'close' if value >= 3 else 'regular' if value >= 1 else 'occasional' if value >= 0.3 else 'faint'


def _project_sides(db):
    """A project's side: Work when it's on a board or shared with the team; else Personal when every person on it is
    Personal; else Work (unknown counts as Work, so it stays out of a Personal-only brain)."""
    have = {r[1] for r in db.execute('PRAGMA table_info(projects)')}
    rows = db.execute('SELECT id' + (',board_id' if 'board_id' in have else ',NULL') + (',visibility' if 'visibility' in have else ',NULL')
                      + ' FROM projects').fetchall()
    sides = {}
    for pid, board, visibility in rows:
        node = 'project:' + str(pid)
        if board is not None or visibility:
            sides[node] = 'work'
            continue
        people = db.execute("SELECT n.info FROM graph_links l JOIN graph_nodes n ON n.id=l.a AND n.kind='person' WHERE l.b=?", (node,)).fetchall()
        found = {_info({'info': p[0]}).get('side') for p in people}
        sides[node] = 'personal' if found == {'personal'} else 'work'
    return sides


def records(db, config):
    """What may go into the owner's GBrain now, by the boundary rules above: [{node_id, kind, name, side, lines, front}]."""
    work = settings(config).get('work') is True
    out = []
    people = db.execute("SELECT * FROM graph_nodes WHERE kind='person' ORDER BY strength DESC LIMIT ?", (MAX_PEOPLE * 3,)).fetchall()
    kept = []
    for row in people:
        info = _info(row)
        if info.get('owner') or info.get('seen_only'):
            continue  # a teammate's record, or someone only seen on a thread
        if row['strength'] < MIN_STRENGTH and not info.get('manual') and not info.get('edited'):
            continue
        side = info.get('side')
        if side != 'personal' and not (work and side == 'work'):
            continue
        kept.append((row, info, side))
        if len(kept) >= MAX_PEOPLE:
            break
    orgs, projects = [], []
    if work:
        for row in db.execute("SELECT * FROM graph_nodes WHERE kind='org' ORDER BY strength DESC LIMIT ?", (MAX_ORGS * 2,)):
            info = _info(row)
            if info.get('owner') or info.get('wrong'):
                continue
            if row['strength'] < MIN_STRENGTH and not info.get('manual'):
                continue
            orgs.append((row, info, 'work'))
            if len(orgs) >= MAX_ORGS:
                break
    sides = _project_sides(db) if db.execute("SELECT 1 FROM sqlite_master WHERE name='projects'").fetchone() else {}
    for row in db.execute("SELECT * FROM graph_nodes WHERE kind='project' ORDER BY strength DESC LIMIT ?", (MAX_PROJECTS * 2,)):
        info = _info(row)
        side = sides.get(row['id'], 'work')
        if info.get('owner') or info.get('closed_at') or (side == 'work' and not work):
            continue
        projects.append((row, info, side))
        if len(projects) >= MAX_PROJECTS:
            break
    going = {r['id'] for r, _, _ in kept + orgs + projects}
    names = {r['id']: r['name'] for r, _, _ in kept + orgs + projects}

    def linked(node_id, kind, limit=5):
        """Names of the records of this kind linked to it that go in too."""
        rows = db.execute('SELECT n.id FROM graph_links l JOIN graph_nodes n ON n.id=(CASE WHEN l.a=? THEN l.b ELSE l.a END) '
                          'WHERE (l.a=? OR l.b=?) AND n.kind=? ORDER BY l.strength DESC LIMIT 40', (node_id, node_id, node_id, kind)).fetchall()
        return [names[r[0]] for r in rows if r[0] in going][:limit]

    org_names = {}
    for row, info, side in kept:
        org = info.get('org')
        if org and org not in org_names:
            found = db.execute('SELECT name FROM graph_nodes WHERE id=?', (org,)).fetchone()
            org_names[org] = found[0] if found else None
    for row, info, side in kept:
        profile = info.get('profile') if isinstance(info.get('profile'), dict) else {}
        org = org_names.get(info.get('org'))
        lines = [('Side', 'Work' if side == 'work' else 'Personal')]
        if info.get('role'):
            lines.append(('Role', str(info['role'])))
        if org:
            lines.append(('Organization', f'[[companies/{slugify(org)}|{org}]]' if info.get('org') in going else org))
        if profile.get('title'):
            lines.append(('Title', str(profile['title'])))
        lines.append(('Contact', f"{_closeness(row['strength'])}, last {_day(row['last_at']) or 'unknown'}"))
        projects_of = linked(row['id'], 'project')
        if projects_of:
            lines.append(('Projects', ', '.join(f'[[projects/{slugify(p)}|{p}]]' for p in projects_of)))
        if info.get('notes'):
            lines.append(('Notes', ' '.join(str(info['notes']).split())[:600]))
        emails = [e for e in (info.get('emails') or []) if isinstance(e, str)] or \
            [i[6:] for i in (info.get('ids') or []) if isinstance(i, str) and i.startswith('email:')]
        front = {'type': 'person', 'title': row['name']}
        if emails:
            front['email'] = emails[0]
        out.append({'node_id': row['id'], 'kind': 'person', 'name': row['name'], 'side': side, 'lines': lines, 'front': front,
                    'emails': emails[:3]})
    for row, info, side in orgs:
        lines = [('Side', 'Work')]
        if info.get('role'):
            lines.append(('Role', str(info['role'])))
        if info.get('domain'):
            lines.append(('Website', str(info['domain'])))
        lines.append(('Contact', f"last {_day(row['last_at']) or 'unknown'}"))
        people_of = linked(row['id'], 'person', 6)
        if people_of:
            lines.append(('People', ', '.join(f'[[people/{slugify(p)}|{p}]]' for p in people_of[:6])))
        out.append({'node_id': row['id'], 'kind': 'org', 'name': row['name'], 'side': side, 'lines': lines,
                    'front': {'type': 'company', 'title': row['name']}, 'emails': []})
    for row, info, side in projects:
        lines = [('Side', 'Work' if side == 'work' else 'Personal'), ('Last activity', _day(row['last_at']) or 'unknown')]
        on_it = linked(row['id'], 'person', 6)
        if on_it:
            lines.append(('People', ', '.join(f'[[people/{slugify(p)}|{p}]]' for p in on_it)))
        out.append({'node_id': row['id'], 'kind': 'project', 'name': row['name'], 'side': side, 'lines': lines,
                    'front': {'type': 'project', 'title': row['name']}, 'emails': []})
    return out


def learnings(db):
    """What The Machine learned from the owner's notes (Learned: facts, rules), never removed or merged ones."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE name='facts'").fetchone():
        return []
    have = {r[1] for r in db.execute('PRAGMA table_info(facts)')}
    where = 'removed_at IS NULL' + (' AND merged_into IS NULL' if 'merged_into' in have else '')
    return [' '.join(str(r[0]).split())[:400] for r in db.execute(f'SELECT text FROM facts WHERE {where} ORDER BY id LIMIT 200')]


PREFIX = {'person': 'people/', 'org': 'companies/', 'project': 'projects/'}


def section(record, config):
    """The part of a page The Machine writes, markers included."""
    lines = [MARK_START, '## From The Machine', '']
    lines += [f'- {key}: {value}' for key, value in record['lines']]
    link = graph_link(config, record['node_id'])
    lines += ['', f'Source: [The Machine Graph]({link})' if link else 'Source: The Machine Graph',
              '_Written by The Machine. Edit or remove this part and The Machine leaves it as you made it._', MARK_END]
    return '\n'.join(lines)


def learnings_section(items):
    lines = [MARK_START, '## What The Machine learned', '']
    lines += [f'- {text}' for text in items] or ['- Nothing yet.']
    lines += ['', 'Source: The Machine, from your notes on its to-dos',
              '_Written by The Machine. Edit or remove this part and The Machine leaves it as you made it._', MARK_END]
    return '\n'.join(lines)


def new_page(front, title, part):
    head = ['---'] + [f'{k}: {json.dumps(v, ensure_ascii=False)}' for k, v in front.items()] + ['---', '', f'# {title}', '', part, '']
    return '\n'.join(head)


SECTION = re.compile(re.escape(MARK_START) + r'.*?' + re.escape(MARK_END), re.S)


def current_section(content):
    found = SECTION.search(content or '')
    return found.group(0) if found else None


def with_section(content, part):
    """The page with The Machine's section replaced (or added at the end); the rest exactly as it was."""
    if SECTION.search(content):
        return SECTION.sub(lambda _: part, content, count=1)
    return content.rstrip('\n') + '\n\n' + part + '\n'


def without_section(content):
    return re.sub(r'\n*' + SECTION.pattern + r'\n?', '\n', content, count=1, flags=re.S)


def owner_part(content):
    """What the owner (or GBrain) wrote on a page outside The Machine's section, short: no front matter, title or timeline."""
    text = SECTION.sub('', content or '')
    text = re.sub(r'\A---\n.*?\n---\n', '', text, flags=re.S)
    text = re.split(r'^---\s*$|^## Timeline\b', text, maxsplit=1, flags=re.M)[0]
    text = re.sub(r'^# .*$', '', text, count=1, flags=re.M)
    text = ' '.join(text.split())
    return text[:NOTE_CHARS].rstrip() + ('…' if len(text) > NOTE_CHARS else '')


# --- The sync ----------------------------------------------------------------------------------------------------

def meta(db, key, default=None):
    row = db.execute('SELECT value FROM gbrain_meta WHERE key=?', (key,)).fetchone()
    return row[0] if row else default


def set_meta(db, key, value):
    db.execute('INSERT INTO gbrain_meta(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key, value))


def _pick_slug(db, call, record):
    """An existing page about them (exact email or name, GBrain's whois) that no other record has, else a new slug."""
    taken = {r[0] for r in db.execute('SELECT slug FROM gbrain_pages')}
    if record['kind'] == 'person':
        for query in [*record.get('emails', [])[:1], record['name']]:
            try:
                found = call('whois', {'query': query, 'types': ['person']})
            except BrainError:
                found = None
            matches = found.get('matches') if isinstance(found, dict) else None
            if isinstance(matches, list) and len(matches) == 1 and isinstance(matches[0], dict) and matches[0].get('slug') \
                    and matches[0]['slug'] not in taken:
                return str(matches[0]['slug'])
    base = PREFIX[record['kind']] + slugify(record['name'])
    return base if base not in taken else base + '-' + digest(record['node_id'])[:6]


def _write(db, call, node_id, slug, part, row, create):
    """Write one section. Returns 'wrote', 'same', 'kept' (the owner changed it) or 'gone' (the owner deleted the page)."""
    content, revision = page_content(call('get_page', {'slug': slug, 'include_content': True}))
    stamp = now()
    if content is None:
        if row:  # the owner deleted the page: not made again
            db.execute("UPDATE gbrain_pages SET state='gone',at=? WHERE node_id=?", (stamp, node_id))
            return 'gone'
        call('put_page', {'slug': slug, 'content': create(), 'content_origin': 'tool_output'})
        db.execute('INSERT OR REPLACE INTO gbrain_pages(node_id,slug,section,state,revision,at) VALUES(?,?,?,?,?,?)',
                   (node_id, slug, digest(part), 'synced', None, stamp))
        return 'wrote'
    there = current_section(content)
    if row and (there is None or digest(there) != row['section']):
        db.execute("UPDATE gbrain_pages SET state='kept',at=? WHERE node_id=?", (stamp, node_id))
        return 'kept'
    updated = with_section(content, part)
    if updated != content:
        params = {'slug': slug, 'content': updated, 'content_origin': 'tool_output'}
        if revision:
            params['expected_revision'] = revision
        call('put_page', params)
    db.execute('INSERT OR REPLACE INTO gbrain_pages(node_id,slug,section,state,revision,at) VALUES(?,?,?,?,?,?)',
               (node_id, slug, digest(part), 'synced', revision, stamp))
    return 'wrote' if updated != content else 'same'


def push(db, config, call, limit=MAX_WRITES):
    """One round Machine to GBrain. {'wrote', 'kept', 'withdrawn', 'conflicts', 'left'}."""
    ensure(db)
    counts = {'wrote': 0, 'kept': 0, 'withdrawn': 0, 'conflicts': 0, 'left': 0}
    rows = {r['node_id']: r for r in db.execute('SELECT * FROM gbrain_pages')}
    wanted = records(db, config)
    items = [(r['node_id'], r, section(r, config)) for r in wanted]
    items.append(('the-machine:learnings', None, learnings_section(learnings(db))))
    budget = limit
    for node_id, record, part in items:
        row = rows.get(node_id)
        if row and (row['state'] in ('kept', 'gone') or row['section'] == digest(part)):
            continue  # unchanged, or the owner's now: no call at all
        if budget <= 0:
            counts['left'] += 1
            continue
        budget -= 1
        if record is None:
            slug = row['slug'] if row else LEARNINGS_SLUG
            create = lambda part=part: new_page({'type': 'note', 'title': 'What The Machine learned'}, 'What The Machine learned', part)
        else:
            slug = row['slug'] if row else _pick_slug(db, call, record)
            create = lambda record=record, part=part: new_page(record['front'], record['name'], part)
        try:
            done = _write(db, call, node_id, slug, part, row, create)
        except Conflict:
            counts['conflicts'] += 1
            continue
        finally:
            db.commit()  # each page on its own: a round takes minutes and must not hold the database meanwhile
        if done in ('wrote', 'kept'):
            counts[done] += 1
    # Records that may no longer go (Work turned off, a side changed, a teammate owns it now): their section comes out
    going = {node_id for node_id, _, _ in items}
    for node_id, row in rows.items():
        if node_id in going or row['state'] != 'synced':
            continue
        if budget <= 0:
            counts['left'] += 1
            continue
        budget -= 1
        try:
            if withdraw(db, call, node_id, row):
                counts['withdrawn'] += 1
        except Conflict:
            counts['conflicts'] += 1
        finally:
            db.commit()
    return counts


def withdraw(db, call, node_id, row):
    """Take The Machine's section off a page (only if it is still exactly what it wrote); the page and the rest stay."""
    content, revision = page_content(call('get_page', {'slug': row['slug'], 'include_content': True}))
    there = current_section(content) if content is not None else None
    if there is not None and digest(there) == row['section']:
        params = {'slug': row['slug'], 'content': without_section(content), 'content_origin': 'tool_output', 'allow_shrink': True}
        if revision:
            params['expected_revision'] = revision
        call('put_page', params)
    db.execute('DELETE FROM gbrain_pages WHERE node_id=?', (node_id,))
    db.execute('DELETE FROM gbrain_notes WHERE node_id=?', (node_id,))
    return there is not None


def pull(db, call, limit=MAX_PULLS):
    """GBrain to The Machine: what the owner wrote on the pages of records that went in, as short notes. Pages changed
    since the last pull only (list_pages updated_after); the first pull reads them all, a round at a time."""
    ensure(db)
    mapped = {r['slug']: r['node_id'] for r in db.execute("SELECT slug,node_id FROM gbrain_pages WHERE state!='gone'") if r['node_id'] != 'the-machine:learnings'}
    if not mapped:
        return 0
    since, started, changed = meta(db, 'pulled_at'), dt.datetime.now(dt.timezone.utc).isoformat(), []
    if since:
        for prefix in PREFIX.values():
            found = call('list_pages', {'slug_prefix': prefix, 'updated_after': since, 'limit': 100})
            pages = found.get('pages') if isinstance(found, dict) else found
            changed += [p.get('slug') for p in pages or [] if isinstance(p, dict) and p.get('slug') in mapped]
    else:
        done = {r[0] for r in db.execute('SELECT slug FROM gbrain_notes')}
        changed = [slug for slug in mapped if slug not in done]
    read = 0
    for slug in changed[:limit]:
        content, _ = page_content(call('get_page', {'slug': slug, 'include_content': True}))
        note = owner_part(content) if content else ''
        if note:
            db.execute('INSERT OR REPLACE INTO gbrain_notes(node_id,slug,text,at) VALUES(?,?,?,?)', (mapped[slug], slug, note, started))
        else:
            db.execute('DELETE FROM gbrain_notes WHERE node_id=?', (mapped[slug],))
        db.commit()
        read += 1
    if len(changed) <= limit:
        set_meta(db, 'pulled_at', started)
    return read


def sync(db, config, call):
    """One round both ways. Never runs unless on(config)."""
    if not on(config):
        return None
    ensure(db)
    try:
        counts = push(db, config, call)
        counts['pulled'] = pull(db, call)
        set_meta(db, 'last_error', None)
    except BrainError as error:
        set_meta(db, 'last_error', error.code)
        raise
    finally:
        set_meta(db, 'last_sync', now())
    return counts


def notes(db, node_ids):
    """{node_id: note} from GBrain for these records (empty when nothing came back)."""
    ids = [str(i) for i in node_ids or []]
    if not ids or not db.execute("SELECT 1 FROM sqlite_master WHERE name='gbrain_notes'").fetchone():
        return {}
    return {r[0]: r[1] for r in db.execute(f"SELECT node_id,text FROM gbrain_notes WHERE node_id IN ({','.join('?' * len(ids))})", ids)}


def counts(db):
    ensure(db)
    rows = dict(db.execute("SELECT state,count(*) FROM gbrain_pages WHERE node_id!='the-machine:learnings' GROUP BY state").fetchall())
    return {'pages': rows.get('synced', 0), 'kept': rows.get('kept', 0), 'last_sync': meta(db, 'last_sync'), 'last_error': meta(db, 'last_error')}


def forget(db):
    """Turned off: what came back from GBrain goes from this Machine (the brain and its pages stay as they are)."""
    ensure(db)
    db.execute('DELETE FROM gbrain_notes')
    db.execute("DELETE FROM gbrain_meta WHERE key IN ('pulled_at','last_error')")
