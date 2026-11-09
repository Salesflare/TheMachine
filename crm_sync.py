"""Contact details kept current in a CRM the owner connected (docs/help/salesforce.md, "Update contact details").

When the Machine knows newer details for someone who is a contact in the CRM, it updates that contact there: job title,
phone and LinkedIn link. It is a setting on the connection, off until the owner turns it on, and turning it on first
shows what would change (preview, then the connector's own switch). The rules are the cautious ones:

- Only details in the person's own words (their LinkedIn, Slack or Google profile: enrichment.STATED) or set by the
  owner on the person's page. Never a look-up's guess, never another record (a CRM, the owner's address book).
- Only when that detail is newer than the contact's last change in the CRM, so an edit made there wins.
- Only fields that differ, and never a blank: a value the Machine doesn't have leaves the CRM's as it is.
- Never the email address (it is how a contact is matched) and never the company: moving a contact to another
  account is the owner's call in the CRM.
- A value written once and changed in the CRM afterwards is left alone from then on (written): no tug of war.
- At most MAX_WRITES contacts a run. Each change is a dated line on the person (crm.change, field crm_sync).

The connector reads the contacts and writes them; this module only plans (plan) and logs (logged)."""
from __future__ import annotations

import datetime as dt
import json
import re

import enrichment

FIELDS = ('title', 'phone', 'linkedin_url')
LABELS = {'title': 'Job title', 'phone': 'Phone', 'linkedin_url': 'LinkedIn'}
CRM_SOURCES = ('salesflare', 'salesforce')  # what a CRM said is never written back to one
MAX_WRITES = 20
MAX_PEOPLE = 400  # people looked at a run, the most recently active first
PREVIEW_MINUTES = 30  # the owner saw what would change this recently before turning it on
WRITTEN_KEEP = 2000


def parse(value):
    try:
        stamp = dt.datetime.fromisoformat(str(value or '').replace('Z', '+00:00').replace('+0000', '+00:00'))
    except ValueError:
        return None
    return stamp if stamp.tzinfo else stamp.replace(tzinfo=dt.timezone.utc)


def same(field, a, b):
    """Whether two values say the same: phones by their last 9 digits, links without their scheme and slash, text
    without case and extra spaces."""
    a, b = ' '.join(str(a or '').split()), ' '.join(str(b or '').split())
    if field == 'phone':
        return re.sub(r'\D', '', a)[-9:] == re.sub(r'\D', '', b)[-9:]
    if field == 'linkedin_url':
        a, b = (re.sub(r'^https?://(www\.)?', '', x).rstrip('/').casefold() for x in (a, b))
    return a.casefold() == b.casefold()


def people(db, emails):
    """{email: (person node id, its identifiers)} for the people in the Graph with these addresses."""
    wanted = sorted({str(e).strip().lower() for e in emails if '@' in str(e or '')})
    if not wanted:
        return {}
    found = {}
    for row in db.execute("SELECT n.id,n.info,j.value FROM graph_nodes n, json_each(n.info,'$.identifiers') j WHERE n.kind='person' "
                          "AND j.value IN (SELECT 'email:' || value FROM json_each(?))", (json.dumps(wanted),)):
        found[str(row[2])[6:]] = (row[0], sorted(set(json.loads(row[1] or '{}').get('identifiers') or ()) | {row[0]}))
    return found


def emails_worth_checking(db, limit=MAX_PEOPLE):
    """Addresses of people with a detail the Machine could write: in their own words, or set by the owner."""
    ids = set()
    try:
        ids |= {r[0] for r in db.execute(f"SELECT DISTINCT identifier FROM person_facts WHERE rank>=? AND field IN ({','.join('?' * len(FIELDS))}) "
                                         f"AND source NOT IN ({','.join('?' * len(CRM_SOURCES))})", (enrichment.STATED, *FIELDS, *CRM_SOURCES))}
        ids |= {r[0] for r in db.execute("SELECT identifier FROM person_edits WHERE json_extract(fields,'$.title') IS NOT NULL "
                                         "OR json_extract(fields,'$.linkedin_url') IS NOT NULL OR json_extract(fields,'$.phones') IS NOT NULL")}
    except Exception:  # noqa: BLE001 - a Machine without these tables yet has nothing to write
        return []
    if not ids:
        return []
    out = []
    for row in db.execute("SELECT n.info FROM graph_nodes n WHERE n.kind='person' AND EXISTS (SELECT 1 FROM json_each(n.info,'$.identifiers') j "
                          "WHERE j.value IN (SELECT value FROM json_each(?))) ORDER BY n.last_at DESC", (json.dumps(sorted(ids)),)):
        for identifier in json.loads(row[0] or '{}').get('identifiers') or ():
            if str(identifier).startswith('email:'):
                out.append(str(identifier)[6:].lower())
        if len(out) >= limit:
            break
    return list(dict.fromkeys(out))[:limit]


def known(db, ids):
    """{field: (value, at, from)}: the newest detail per field the Machine may write for a person with these
    identifiers, their own words (STATED) or the owner's own edit."""
    best = {}
    for identifier, facts in enrichment.people_facts(db, FIELDS, ids).items():
        for field, (value, rank, source, seen_at) in facts.items():
            if rank >= enrichment.STATED and source not in CRM_SOURCES and parse(seen_at):
                if field not in best or parse(seen_at) > parse(best[field][1]):
                    best[field] = (value, seen_at, enrichment.FACT_SOURCES.get(source, source))
    group = sorted(ids)
    rows = db.execute(f"SELECT fields,updated_at FROM person_edits WHERE identifier IN ({','.join('?' * len(group))}) ORDER BY updated_at",
                      group).fetchall() if group else []
    for fields, at in rows:
        edit = json.loads(fields or '{}')
        phones = (edit.get('phones') or {}).get('added') if isinstance(edit.get('phones'), dict) else None
        for field, value in (('title', edit.get('title')), ('linkedin_url', edit.get('linkedin_url')), ('phone', (phones or [None])[0])):
            if value and parse(at) and (field not in best or parse(at) >= parse(best[field][1])):
                best[field] = (str(value), at, 'you')
    return best


def plan(db, contacts, crm, written=None, fields=FIELDS, limit=MAX_WRITES):
    """What to change: [{'contact_id', 'node_id', 'name', 'email', 'changes': [{'field', 'old', 'new', 'from', 'at'}]}],
    for at most limit contacts. contacts: the CRM's own [{'id', 'email', 'name', 'modified', field: value}]; fields: the
    ones this CRM can take (no LinkedIn field there: no LinkedIn). written: {'<contact id>:<field>': value} this Machine
    wrote before."""
    written = written or {}
    found = people(db, [c.get('email') for c in contacts])
    out = []
    for contact in contacts:
        email = str(contact.get('email') or '').strip().lower()
        if email not in found:
            continue
        node_id, ids = found[email]
        details, modified = known(db, ids), parse(contact.get('modified'))
        changes = []
        for field in fields:
            if field not in details:
                continue
            value, at, origin = details[field]
            current = contact.get(field)
            if not str(value or '').strip() or same(field, value, current):
                continue
            before = written.get(f"{contact['id']}:{field}")
            if before is not None and not same(field, before, current):
                continue  # changed in the CRM after the Machine wrote it: theirs stays
            if modified and parse(at) <= modified:
                continue  # the CRM's record changed after the Machine learned this
            changes.append({'field': field, 'old': current or None, 'new': value, 'from': origin, 'at': at})
        if changes:
            out.append({'contact_id': contact['id'], 'node_id': node_id, 'name': contact.get('name') or email, 'email': email,
                        'crm': crm, 'changes': changes})
        if len(out) >= limit:
            break
    return out


def logged(db, item, now):
    """Each change is a dated line on the person's timeline (crm.record_changes, field crm_sync)."""
    import crm
    crm.ensure(db)
    for change in item['changes']:
        crm.change(db, item['node_id'], 'crm_sync', json.dumps({'value': change['old']}),
                   json.dumps({'crm': item['crm'], 'field': change['field'], 'value': change['new'], 'from': change['from']}), now)


def remember(written, item):
    for change in item['changes']:
        written[f"{item['contact_id']}:{change['field']}"] = change['new']
    while len(written) > WRITTEN_KEEP:
        written.pop(next(iter(written)))
    return written


def shown(items, limit=50):
    """The preview and the card's recent updates, as the dashboard lists them."""
    return [{'name': i['name'], 'email': i['email'], 'node_id': i.get('node_id'), 'at': i.get('done_at'),
             'changes': [{'field': c['field'], 'label': LABELS[c['field']], 'old': c['old'], 'new': c['new'], 'from': c['from']}
                         for c in i['changes']]} for i in items[:limit]]


def preview_fresh(state, now):
    seen = parse((state or {}).get('contact_preview_at'))
    return bool(seen) and (parse(now) - seen) <= dt.timedelta(minutes=PREVIEW_MINUTES)
