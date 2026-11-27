"""Connected AIs, what the owner taught The Machine: get_learnings and the brief (docs/ai-connections.md, Learnings and
the brief). On unless the config's FLAG is false (on()).

get_learnings gives the owner's rules, general facts (about no one in the Graph) and voice per channel, as Learning,
What I've learned has them, in the connection's area. The brief is a few lines for the start of a chat: who the owner
is, their top rules and facts, and what changed since this connection's last visit (its own activity log). Neither
carries message subjects or text, whatever Messages is.

Who wrote a learning decides how it goes out (origin): the owner's own words (a note, their chat, their OpenClaw notes,
an edit) and their voice go as they are; a connected AI's or an unedited import's is that AI's claim, and one the
learning loop wrote from what happened (other people's messages among it) is The Machine's reading of their messages,
so both go inside <untrusted> (ai_access.untrusted). Pure functions of the database: ai_app.py hands them the area."""
from __future__ import annotations

import datetime as dt
import re
import sqlite3

from machine.store import facts as fact_store
import timeutil

FLAG = 'ai_learnings'  # config: get_learnings, get_brief, save_learning and the brief in the server's instructions
LIMIT, MOST = 30, 100  # rules and facts per list: given, and the most asked
VOICE_CHARS = 1500  # of one channel's voice
FIRST_DAYS = 7  # a first visit's brief looks back this far
DUE_DAYS = 7  # promises due within this many days, overdue ones too
AGAIN_MINUTES = 10  # a brief within this of the last one is no new line in Activity
BRIEF_RULES, BRIEF_FACTS, BRIEF_TODOS, BRIEF_PEOPLE, BRIEF_PROMISES = 4, 3, 3, 5, 3
LINE_CHARS = 140  # of a rule, fact, to-do or promise in the brief
SCAN = 500  # newest to-dos and people looked at for the brief


def on(config):
    """Whether connected AIs get the learnings tools and the brief: yes, unless the config says false."""
    return config.get(FLAG, True) is not False


def origin(row):
    """untrusted's source for a learning, or None for the owner's own: 'ai' for a connected AI's or an import the owner
    didn't edit (facts.ai_fact_by), 'messages' for one the learning loop wrote ('tune:<run>') and the owner didn't edit."""
    if fact_store.ai_fact_by(row):
        return 'ai'
    if str(row.get('decision_id') or '').startswith('tune:') and not row.get('kept_at'):
        return 'messages'
    return None


def area(row, accounts):
    """A learning's area: an AI's fact its side; one learned on a to-do that to-do's (suggestion_scope, as everywhere);
    else None, both."""
    if row.get('side') in ('work', 'personal'):
        return row['side']
    if row.get('suggestion_id') and row.get('account_ids') is not None:
        return fact_store.suggestion_scope(row['account_ids'], accounts, row.get('todo_area'))
    return None


def rows(db, accounts, want):
    """The current rules and general facts (about no one in the Graph, not past their end day) this area sees, the ones
    said or used last first: (rules, facts), each row with its origin. One the learning loop scoped to a person or
    organization never goes out; one scoped to an area or a channel says so (item)."""
    found = [dict(r) for r in db.execute(
        'SELECT f.id,f.text,f.kind,f.fact_kind,f.valid_until,f.created_at,f.confirmed_at,f.source,f.side,f.kept_at,f.decision_id,f.scope,'
        "f.suggestion_id,s.account_ids,s.area todo_area,max(f.created_at,coalesce(f.confirmed_at,''),coalesce(f.used_at,'')) last_use FROM facts f LEFT JOIN suggestions s ON s.id=f.suggestion_id "
        "WHERE f.removed_at IS NULL AND f.kind IN ('fact','draft') "
        'AND f.id NOT IN (SELECT fact_id FROM fact_about WHERE removed_at IS NULL)')]
    today = timeutil.clock().date().isoformat()
    found = [r for r in found if not fact_store.fact_expired(r, today) and (want is None or area(r, accounts) in (None, want))
             and not str(r.get('scope') or '').startswith('with:')]
    for r in found:
        r['origin'] = origin(r)
    found.sort(key=lambda r: (r['last_use'] or '', r['id']), reverse=True)
    return [r for r in found if r['kind'] == 'draft'], [r for r in found if r['kind'] == 'fact']


def voices(db):
    try:
        return [dict(r) for r in db.execute('SELECT channel,text,source,updated_at FROM voices ORDER BY channel')]
    except sqlite3.OperationalError:
        return []  # a Machine that never learned a voice


def words(query):
    return re.findall(r'\w+', str(query or '').casefold())


def matches(text, asked):
    text = str(text or '').casefold()
    return all(w in text for w in asked)


def item(row, mark):
    out = {'id': row['id'], 'text': mark(row['text'], row['origin']) if row['origin'] else row['text']}
    if row['origin']:
        out['source'] = row['origin']
    if row['kind'] == 'fact' and row.get('fact_kind') not in (None, 'fact'):
        out['sort'] = row['fact_kind']
    if row.get('valid_until'):
        out['until'] = row['valid_until']
    if str(row.get('scope') or '').startswith('channel:'):  # where it holds (learning_loop.scope_of)
        out['channel'] = row['scope'][8:]
    elif row.get('scope') == 'area':
        out['area'] = row['side']
    return out


def learnings(db, accounts, want, mark, query=None, limit=LIMIT):
    """get_learnings' answer: rules, facts and voices, those that hold every word of query when one is given."""
    asked = words(query)
    rules, facts = rows(db, accounts, want)
    rules = [r for r in rules if matches(r['text'], asked)]
    facts = [r for r in facts if matches(r['text'], asked)]
    said = [{'channel': 'Everywhere' if v['channel'] == 'All' else v['channel'], 'text': str(v['text'])[:VOICE_CHARS]}
            for v in voices(db) if matches(v['channel'] + ' ' + v['text'], asked)]
    out = {'rules': [item(r, mark) for r in rules[:limit]], 'facts': [item(r, mark) for r in facts[:limit]], 'voices': said}
    if len(rules) > limit or len(facts) > limit:
        out['more'] = f'The {limit} used last of each. Give a query or a higher limit (up to {MOST}) for others.'
    out['total'] = {'rules': len(rules), 'facts': len(facts)}
    return out


def clip(text, size=LINE_CHARS):
    text = ' '.join(str(text or '').split())
    return text if len(text) <= size else text[:size - 1].rstrip() + '…'


def since(db, connection_id):
    """This connection's last visit: its newest call in Activity (not the owner's settings or a sign-in), else None."""
    row = db.execute("SELECT max(at) FROM ai_activity WHERE connection_id=? AND tool NOT IN ('connect','settings','sign-in')",
                     (connection_id,)).fetchone()
    return row[0] if row and row[0] else None


def briefed_lately(db, connection_id):
    """Whether this connection's newest line in Activity is a brief from the last AGAIN_MINUTES (a client that starts
    over for every call makes one line, not one each time)."""
    row = db.execute('SELECT tool,at FROM ai_activity WHERE connection_id=? ORDER BY id DESC LIMIT 1', (connection_id,)).fetchone()
    edge = (timeutil.clock() - dt.timedelta(minutes=AGAIN_MINUTES)).isoformat(timespec='seconds')
    return bool(row) and row['tool'] == 'brief' and row['at'] >= edge


def brief_text(name, owner, rules, facts, changes, last, mark):
    """The brief: about 200 words. owner: {'name', 'timezone', 'language'}; changes: what changed since last (None: a
    first visit, FIRST_DAYS back): {'todos': (n, titles), 'promises': (n, lines), 'people': (n, names), 'learned': [..]}."""
    lines = [f'Brief from The Machine for {name}.']
    who = ', '.join(filter(None, (owner.get('name'), owner.get('timezone') and 'time zone ' + owner['timezone'],
                                  owner.get('language') and 'language ' + owner['language'])))
    if who:
        lines.append('The owner: ' + who + '.')
    show = lambda r: mark(clip(r['text']), r['origin']) if r['origin'] else clip(r['text'])
    if rules:
        lines += ['Their rules:'] + ['- ' + show(r) for r in rules[:BRIEF_RULES]]
    if facts:
        lines += ['About them:'] + ['- ' + show(r) for r in facts[:BRIEF_FACTS]]
    head = f'Since your last visit ({last[:10]}):' if last else f'In the last {FIRST_DAYS} days:'
    new = []
    for key, one, many in (('todos', 'new to-do', 'new to-dos'), ('promises', f'promise due within {DUE_DAYS} days', f'promises due within {DUE_DAYS} days'),
                           ('people', 'new person', 'new people')):
        count, shown = changes[key]
        if count:
            new.append(f'- {count} {one if count == 1 else many}' + (': ' + '; '.join(shown) if shown else ''))
    if changes['learned']:
        new.append('- Learned: ' + ', '.join(changes['learned']))
    lines += [head] + new if new else [head + ' nothing new.']
    lines.append('Call get_learnings before you draft anything for the owner, search_graph before you answer about someone, '
                 'and list_todos for the rest.')
    return '\n'.join(lines)


def learned_since(rules, facts, said, at):
    """What Learning took in since at: new rules and facts (this area's), and voices updated, as short phrases."""
    out = []
    for got, one, many in ((rules, 'rule', 'rules'), (facts, 'fact', 'facts')):
        n = sum(1 for r in got if (r['created_at'] or '') > at)
        if n:
            out.append(f'{n} new {one if n == 1 else many}')
    channels = [('Everywhere' if v['channel'] == 'All' else v['channel']) for v in said if (v['updated_at'] or '') > at]
    if channels:
        out.append('voice updated (' + ', '.join(channels[:4]) + ')')
    return out


def new_people(db, at, ok, view):
    """(how many, up to BRIEF_PEOPLE names) of the people first seen after at, the closest first; ok(view): this area's."""
    try:
        found = db.execute("SELECT n.* FROM graph_nodes n WHERE n.kind='person' AND EXISTS (SELECT 1 FROM graph_events g WHERE g.node_id=n.id) "
                           'AND NOT EXISTS (SELECT 1 FROM graph_events g WHERE g.node_id=n.id AND g.at<=?) ORDER BY n.strength DESC LIMIT ?',
                           (at, SCAN)).fetchall()
    except sqlite3.OperationalError:
        return 0, []  # no Graph yet
    views = [v for v in (view(r) for r in found) if ok(v)]
    return len(views), [clip(v['name'], 60) for v in views[:BRIEF_PEOPLE]]
