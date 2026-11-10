"""A person's birthday (docs/help/graph.md, "Birthday"): one value per person, the one their page shows and the
Birthdays template reads (birthdays.py). Plain code, no model.

It is kept as a fact (enrichment.person_facts, field birthday) on one of the person's identities: from a Google contact,
a Facebook import, the owner's notes (notes_people.py, source notes) or the owner's own word (source owner). The owner's wins over every other and stays when a source
says otherwise later; their Remove is kept as an empty value, so a contact or an import, now or later, doesn't bring it
back. Otherwise the highest
rank wins, then the latest. An identity more than one person goes by (a shared number) is nobody's, as in
birthdays.by_identifier.

The API: get(db, node_id) reads it; offer(db, node_id, value, source, now) is how an importer (calendar birthday events,
Facebook) writes one; set_birthday is the owner's Edit and Remove; known(db, people) is the batch read for the routine.

A birthday is a month and a day, with the year when it is known: YYYY-MM-DD or --MM-DD. 29 February is a day without a
year, and with a leap year.

A date field the owner made named Birthday (before this was built in) is folded into it once (fold_fields), and a new
one isn't made (crm_fields.save_field): one place for it. A birthday is personal: never part of a record shared with
the team (crm_fields.shared leaves any field named like one out, shared_graph drops one that comes in)."""
from __future__ import annotations

import datetime as dt
import json
import re

FIELD = 'birthday'
SOURCE = 'owner'
OWNER = 3  # above enrichment.STATED (their own profile): the owner's word wins
FIRST_YEAR = 1900


def is_name(name):
    """Whether a field name means a birthday, in the languages the app speaks."""
    import birthdays
    return birthdays.fold(name) in birthdays.FIELD_NAMES


def clean(month, day, year=None, today=None):
    """The birthday as kept, from a month and a day and an optional year; ValueError when it isn't a real day."""
    try:
        month, day = int(month), int(day)
    except (TypeError, ValueError):
        raise ValueError('Pick a month and a day') from None
    text = str(year if year is not None else '').strip()
    if text and not re.fullmatch(r'\d{4}', text):
        raise ValueError('Year: four digits, like 1990')
    try:
        dt.date(int(text) if text else 2000, month, day)  # 2000 is a leap year: 29 February is a day without a year
    except ValueError:
        raise ValueError('That day isn’t in that month' if 1 <= month <= 12 else 'Pick a month and a day') from None
    if text and not FIRST_YEAR <= int(text) <= (today or dt.date.today()).year:
        raise ValueError('Year: not in the future, from 1900')
    return f'{text}-{month:02d}-{day:02d}' if text else f'--{month:02d}-{day:02d}'


def parts(value):
    """{month, day, year (None without it)} from a kept birthday, or None."""
    found = re.fullmatch(r'(\d{4}|-)-(\d{2})-(\d{2})', str(value or '').strip())
    if not found:
        return None
    year = int(found.group(1)) if found.group(1) != '-' else None
    try:
        dt.date(year or 2000, int(found.group(2)), int(found.group(3)))
    except ValueError:
        return None
    return {'month': int(found.group(2)), 'day': int(found.group(3)), 'year': year}


def _facts(db, ids=None):
    try:
        if ids is None:
            return db.execute('SELECT identifier,value,rank,source,seen_at FROM person_facts WHERE field=?', (FIELD,)).fetchall()
        return db.execute('SELECT identifier,value,rank,source,seen_at FROM person_facts WHERE field=? AND identifier IN '
                          '(SELECT value FROM json_each(?))', (FIELD, json.dumps(sorted(ids)))).fetchall()
    except Exception:  # noqa: BLE001 - no facts yet
        return []


def known(db, people, code=None):
    """{node id: {value, month, day, year, source, at}} for these people ({node id: {'info': ...}}, as
    birthdays.close_people), each the one birthday that counts; none for someone without one or whose birthday the
    owner removed. code: the owner's calling code, for a number kept without its own."""
    import birthdays
    fold_fields(db)
    rows = _facts(db)
    if not rows or not people:
        return {}
    owners = birthdays.by_identifier(db, people, {r[0] for r in rows}, code)
    best = {}
    for identifier, value, rank, source, seen_at in rows:
        node = owners.get(identifier)
        if node and (node not in best or (rank, seen_at) > (best[node][1], best[node][2])):
            best[node] = (value, rank, seen_at, source)
    out = {}
    for node, (value, rank, seen_at, source) in best.items():
        found = parts(value)
        if found:
            out[node] = {'value': value, **found, 'source': source, 'at': str(seen_at or '')[:10]}
    return out


def for_person(db, row, code=None):
    """The birthday on one person's page (a graph_nodes row), or None."""
    import birthdays
    info = json.loads(row['info'] or '{}')
    if not _facts(db, birthdays.person_ids(row['id'], info, code)) and not _legacy(db):
        return None  # nothing under any of their identities: no need to look at everyone else's
    return known(db, {row['id']: {'id': row['id'], 'name': row['name'], 'info': info}}, code).get(row['id'])


def get(db, node_id, code=None):
    """The birthday a person's page shows ({value, month, day, year, source, at}), or None. For importers and readers."""
    import graph
    row = graph.resolve(db, str(node_id or ''))
    return for_person(db, row, code) if row and row['kind'] == 'person' else None


def offer(db, node_id, value, source, now):
    """An importer's birthday for a person (a calendar's birthday event, a Facebook import): value YYYY-MM-DD or
    --MM-DD, source its short name ('google', 'facebook', ...). Kept on the person's node as a record about them; the
    owner's word (set or removed on the page) always stays, and a source never overrides a higher one. Returns whether
    it changed anything."""
    import enrichment
    import graph
    row = graph.resolve(db, str(node_id or ''))
    if not row or row['kind'] != 'person' or not parts(value) or not source or source == SOURCE:
        return False
    return bool(enrichment.offer_facts(db, [([row['id']], {FIELD: value}, enrichment.RECORD)], source, now))


def _put(db, identifier, value, now):
    import enrichment
    enrichment.put_fact(db, identifier, FIELD, value, OWNER, SOURCE, now)


def set_birthday(db, node_id, args, now, code=None):
    """The owner sets or corrects a person's birthday ({month, day, year}), or removes it ({remove: true}). Kept on the
    person's own node id, as the owner's (source owner): it wins over every source from now on."""
    import crm
    row = crm.node_row(db, node_id)
    if row['kind'] != 'person':
        raise ValueError('A birthday is for a person')
    import birthdays
    import enrichment
    ids = birthdays.person_ids(row['id'], json.loads(row['info'] or '{}'), code)
    if args.get('remove'):
        # Kept as removed (an empty value of the owner's), also when nothing else knows one now: a contact or an
        # import that comes later doesn't bring it back
        _put(db, row['id'], '', now)
        value = None
    else:
        value = clean(args.get('month'), args.get('day'), args.get('year'))
        _put(db, row['id'], value, now)
    enrichment.drop_facts(db, ids, FIELD, SOURCE, keep=row['id'])  # one word of the owner's per person, the latest
    return {'node_id': row['id'], 'birthday': for_person(db, row, code)}


def _legacy(db):
    try:
        return [r for r in db.execute("SELECT id,name FROM crm_fields WHERE kind='person' AND type='date'") if is_name(r['name'])]
    except Exception:  # noqa: BLE001 - no fields yet
        return []


def fold_fields(db):
    """A person date field named Birthday the owner made is the built-in birthday now: its dates become the owner's
    birthdays (where the owner hasn't set one), and the field goes. Once; nothing to do after that."""
    found = _legacy(db)
    if not found:
        return 0
    import crm_fields
    moved = 0
    for field in found:
        for row in db.execute('SELECT node_id,value,set_at FROM crm_values WHERE field_id=?', (field['id'],)).fetchall():
            value = str(row['value'] or '')[:10]
            have = [r for r in _facts(db, [row['node_id']]) if r[3] == SOURCE]
            if parts(value) and not have:
                _put(db, row['node_id'], value, row['set_at'] or dt.datetime.now(dt.timezone.utc).isoformat())
                moved += 1
        crm_fields.delete_field(db, field['id'])
    return moved
