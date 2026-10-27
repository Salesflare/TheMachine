"""Sharing a contact (docs/help/share-contact.md): from a person's page, or your own card from About you, the owner sends
a name and the fields they pick (emails, phones, organization, role) with an optional note on why the two should talk,
to one teammate in a Work Fleet, or to one friend or Family member. Mixed into fleet.Fleet, next to friends.Friends.

How it goes: the Fleet's own `contact` question, sealed Machine to Machine like every message on the Network
(network.py). Nothing goes by itself: the owner sees exactly what will be sent (preview, with its digest) and Send
carries that digest, so what goes is what they saw. A Personal contact, or one kept private from the team, needs an
extra confirm first. There is no Always rule for it.

On the other side: a teammate's share shows in their Graph as a person shared by the sender; a friend's or Family
member's as a suggestion to add. Either waits for its owner's Add (made, or merged into the person with the same email
or phone: only adds, never removes or overwrites) or Dismiss. What they send is data, kept to a fixed form (parse),
shown as their words; nothing in it reaches a model, a tool or Do it."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import secrets

KIND = 'contact'
FIELDS = ('emails', 'phones', 'org', 'role')
NAME_CHARS, ORG_CHARS, ROLE_CHARS, NOTE_CHARS = 100, 100, 120, 300
MAX_EACH = 5  # emails, phones
OPEN_PER_SENDER = 20  # waiting shares from one person; more are declined
EMAIL = re.compile(r'[^@\s<>",;]+@[^@\s<>",;]+\.[^@\s<>",;]+')
PHONE = re.compile(r'\+?[\d\s().-]{6,40}')
SCHEMA = '''
CREATE TABLE IF NOT EXISTS contact_shares(id TEXT PRIMARY KEY,fleet TEXT NOT NULL,group_kind TEXT NOT NULL,member_id TEXT NOT NULL,
  name TEXT NOT NULL,card TEXT NOT NULL,status TEXT NOT NULL,node_id TEXT,at TEXT NOT NULL,decided_at TEXT);
CREATE TABLE IF NOT EXISTS contact_marks(identifier TEXT PRIMARY KEY,by_name TEXT NOT NULL,group_kind TEXT NOT NULL,note TEXT,at TEXT NOT NULL);
'''
WHERE = {'work': 'Work Fleet', 'family': 'Family', 'friends': 'Friends'}


def ensure(db):
    db.executescript(SCHEMA)


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def line(value, chars):
    """One plain line: no control or invisible characters, at most `chars`."""
    if not isinstance(value, str):
        return ''
    kept = ''.join(c if c.isprintable() else ' ' for c in value if c not in '​‌‍⁠﻿‪‫‬‭‮⁦⁧⁨⁩')
    return ' '.join(kept.split())[:chars]


def _list(values, pattern, chars):
    out, seen = [], set()
    for v in values if isinstance(values, list) else []:
        text = line(v, chars)
        key = re.sub(r'\D', '', text) if pattern is PHONE else text.casefold()
        if text and pattern.fullmatch(text) and key and key not in seen:
            seen.add(key)
            out.append(text)
    return out[:MAX_EACH]


def parse(question):
    """A shared contact in its fixed form, else None: a name, the fields that came, an optional note, and whether it's
    the sender's own card. Anything else in it is never read."""
    if not isinstance(question, dict):
        return None
    name = line(question.get('name'), NAME_CHARS)
    if not name:
        return None
    card = {'name': name}
    emails = _list(question.get('emails'), EMAIL, 200)
    phones = _list(question.get('phones'), PHONE, 40)
    org, role, note = line(question.get('org'), ORG_CHARS), line(question.get('role'), ROLE_CHARS), line(question.get('note'), NOTE_CHARS)
    if emails:
        card['emails'] = [e.lower() for e in emails]
    if phones:
        card['phones'] = phones
    if org:
        card['org'] = org
    if role:
        card['role'] = role
    if note:
        card['note'] = note
    if question.get('own') is True:
        card['own'] = True
    return card


def clean_answer(answer):
    return {'stage': answer['stage']} if isinstance(answer, dict) and answer.get('stage') in ('added', 'merged') else None


def question_text(question):
    q = question or {}
    return ('Shares their own contact' if q.get('own') else 'Shares a contact') + f": {q.get('name', '?')}"


def answer_text(answer):
    return {'added': 'added it', 'merged': 'added it to someone they had'}.get((answer or {}).get('stage'), 'no answer')


def digest(card):
    return hashlib.sha256(json.dumps(card, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def summary(card):
    """What the other side gets, line by line, as the preview and the receiver show it."""
    rows = [('Name', card['name'])]
    rows += [('Email', e) for e in card.get('emails', [])]
    rows += [('Phone', p) for p in card.get('phones', [])]
    if card.get('org'):
        rows.append(('Organization', card['org']))
    if card.get('role'):
        rows.append(('Role', card['role']))
    if card.get('note'):
        rows.append(('Note', card['note']))
    return [{'label': k, 'value': v} for k, v in rows]


class ContactShare:
    """Mixed into fleet.Fleet: sharing a contact with one teammate, friend or Family member, and the ones shared here."""

    graph_build = None  # rebuilds the graph after an Add (assistant.py)
    about_you = None  # the owner's own record, About you (assistant.py)

    # -- what can be sent
    def contact_targets(self):
        """Who a contact can go to: each teammate, friend and Family member whose group the Network carries contacts in."""
        import fleet as fleet_module
        out = []
        for ref, found in self.fleets().items():
            if KIND not in (found.get('asks') or ()):
                continue
            kind = found.get('kind')
            for m in self.teammates(ref):
                if m.get('machine') is False:
                    continue
                out.append({'fleet': ref, 'member_id': m['member_id'], 'name': fleet_module.clean(fleet_module.label(m), 120) or 'Someone',
                            'kind': kind, 'where': found.get('name') if kind == 'work' and found.get('name') else WHERE.get(kind, 'Fleet')})
        return out

    def contact_source(self, db, source):
        """What the owner can pick from for a person (a graph node id), or for their own card ('me'): every value, and
        whether it needs the extra confirm (a Personal contact, or one kept private from the team)."""
        import graph
        if source == graph.ME:  # the owner's own card, from About you
            about = self.about_you() if self.about_you else graph.about_you(db, self.config)
            name = line(about.get('owner_name'), NAME_CHARS) or next((line(m.get('name'), NAME_CHARS) for f in self.fleets().values()
                                                                       for m in f.get('members') or () if m.get('me') and m.get('name')), '')
            if not name:
                raise ValueError('Add your name first, in Settings')
            return {'name': name, 'emails': _list([e.get('value') for e in about.get('emails') or []], EMAIL, 200),
                    'phones': _list([p.get('value') for p in about.get('phones') or []], PHONE, 40), 'org': '', 'role': '', 'own': True, 'confirm': None}
        row = graph.resolve(db, source)
        if not row or row['kind'] != 'person':
            raise ValueError('Share a person from their page')
        view = graph.node_view(row)
        org = ''
        if view.get('org'):
            found = db.execute('SELECT name FROM graph_nodes WHERE id=?', (view['org'],)).fetchone()
            org = found['name'] if found else ''
        profile = view.get('profile') or {}
        org = org or line(profile.get('company'), ORG_CHARS)
        confirm = None
        if view.get('side') == 'personal':
            confirm = 'personal'
        elif graph._table(db, 'share_private') and db.execute('SELECT 1 FROM share_private WHERE node_id=?', (row['id'],)).fetchone():
            confirm = 'private'
        return {'node_id': row['id'], 'name': line(row['name'], NAME_CHARS),
                'emails': _list([e.get('value') for e in view.get('emails') or [] if isinstance(e, dict)], EMAIL, 200),
                'phones': _list([p.get('value') for p in view.get('phones') or [] if isinstance(p, dict)], PHONE, 40),
                'org': line(org, ORG_CHARS), 'role': line(profile.get('title'), ROLE_CHARS), 'own': False, 'confirm': confirm}

    def contact_card(self, source, pick, note=''):
        """The card exactly as it would go: only the values picked, from what the source has."""
        pick = pick if isinstance(pick, dict) else {}
        with self.connect() as db:
            have = self.contact_source(db, source)
        card = {'name': have['name']}
        for field in ('emails', 'phones'):
            wanted = {str(v) for v in pick.get(field) or [] if isinstance(v, str)}
            chosen = [v for v in have[field] if v in wanted]
            if chosen:
                card[field] = chosen
        for field in ('org', 'role'):
            if pick.get(field) is True and have[field]:
                card[field] = have[field]
        if line(note, NOTE_CHARS):
            card['note'] = line(note, NOTE_CHARS)
        if have.get('own'):
            card['own'] = True
        return parse(card), have

    def contact_options(self, source):
        """For the Share dialog: what can be picked, and who it can go to."""
        with self.connect() as db:
            have = self.contact_source(db, source)
        return {**have, 'targets': self.contact_targets()}

    def contact_preview(self, source, pick, note, fleet_ref, member_id):
        card, have = self.contact_card(source, pick, note)
        target = self._contact_target(fleet_ref, member_id)
        return {'card': card, 'rows': summary(card), 'digest': digest(card), 'to': target['name'], 'kind': target['kind'],
                'where': target['where'], 'confirm': have['confirm']}

    def _contact_target(self, fleet_ref, member_id):
        target = next((t for t in self.contact_targets() if t['fleet'] == fleet_ref and t['member_id'] == member_id), None)
        if not target:
            raise ValueError('Pick a teammate, friend or Family member')
        return target

    def contact_send(self, source, pick, note, fleet_ref, member_id, shown, confirmed=False):
        """Send: only the card the owner saw (shown, the preview's digest), and a Personal or private one only with
        confirmed. One person at a time."""
        card, have = self.contact_card(source, pick, note)
        target = self._contact_target(fleet_ref, member_id)
        if not shown or shown != digest(card):
            raise ValueError('That changed since the preview. Look it over again')
        if have['confirm'] and confirmed is not True:
            raise ValueError('This is a Personal contact. Confirm to share it anyway' if have['confirm'] == 'personal'
                             else 'You keep this contact private. Confirm to share it anyway')
        context = 'contact:' + ('me' if have.get('own') else have['node_id'])
        sent = self.ask(KIND, card, context=context, fleet=fleet_ref, to=[member_id])
        return {'sent': len(sent.get('ids', {})), 'to': target['name']}

    def contact_sent(self, source):
        """Where this contact went before, newest first: to whom and how it went."""
        label = {'asked': 'sent', 'waiting': 'not added yet', 'answered': 'added', 'declined': 'dismissed', 'expired': 'no answer'}
        with self.connect() as db:
            rows = db.execute("SELECT name,status,at FROM fleet_out WHERE kind=? AND context=? ORDER BY at DESC LIMIT 10",
                              (KIND, 'contact:' + str(source))).fetchall()
        return [{'name': r['name'], 'state': label.get(r['status'], r['status']), 'at': r['at']} for r in rows]

    # -- what comes in
    def take_contact(self, ask, teammate, fleet_ref, name):
        """A contact a teammate, friend or Family member shared: kept for the owner's Add or Dismiss. Returns the status
        the sender's Machine hears."""
        card = parse(ask.get('question'))
        status = 'declined'
        if teammate and card:
            with self.connect() as db:
                ensure(db)
                previous = db.execute('SELECT status FROM contact_shares WHERE id=?', (str(ask.get('id') or ''),)).fetchone()
                if previous:
                    status = 'waiting' if previous['status'] == 'waiting' else 'answered' if previous['status'] in ('added', 'merged') else 'declined'
                elif db.execute("SELECT COUNT(*) FROM contact_shares WHERE status='waiting' AND fleet=? AND member_id=?",
                                (fleet_ref, teammate['member_id'])).fetchone()[0] < OPEN_PER_SENDER:
                    db.execute('INSERT INTO contact_shares(id,fleet,group_kind,member_id,name,card,status,at) VALUES(?,?,?,?,?,?,?,?)',
                               (str(ask['id']), fleet_ref, self.kind_of(fleet_ref) or 'work', teammate['member_id'], line(name, 120) or 'Someone',
                                json.dumps(card), 'waiting', now()))
                    status = 'waiting'
        with self.connect() as db:
            self.log(db, 'in', fleet_ref, (teammate or {}).get('member_id') or ask.get('from'), name, KIND,
                     question_text(card) if card else 'a contact this Machine can\'t read', 'waiting for you' if status == 'waiting' else status)
        answer = None
        if status == 'answered':
            with self.connect() as db:
                answer = {'stage': db.execute('SELECT status FROM contact_shares WHERE id=?', (str(ask['id']),)).fetchone()['status']}
        self.relay.call('POST', '/answer', {'id': ask['id'], 'status': status, **({'answer': answer} if answer else {})})
        return status

    def contacts_in(self):
        """The shares waiting for the owner, newest first."""
        with self.connect() as db:
            ensure(db)
            rows = db.execute("SELECT * FROM contact_shares WHERE status='waiting' ORDER BY at DESC LIMIT 50").fetchall()
            out = []
            for r in rows:
                card = json.loads(r['card'])
                out.append({'id': r['id'], 'from': r['name'], 'kind': r['group_kind'], 'where': WHERE.get(r['group_kind'], 'Fleet'),
                            'card': card, 'rows': summary(card), 'at': r['at'], 'existing': self._existing(db, card)})
        return out

    @staticmethod
    def _existing(db, card):
        """The person in this Graph with one of the card's emails or phones, if any: {'id', 'name'}."""
        import graph
        for identifier in [*('email:' + e for e in card.get('emails', [])),
                           *('wa:' + re.sub(r'\D', '', p).lstrip('0') for p in card.get('phones', []) if len(re.sub(r'\D', '', p)) >= 6)]:
            row = graph.resolve(db, identifier)
            if row and row['kind'] == 'person':
                return {'id': row['id'], 'name': row['name']}
        return None

    def contact_decide(self, share_id, choice):
        """Add (made, or merged into the person who has one of its emails or phones) or Dismiss."""
        if choice not in ('add', 'dismiss'):
            raise ValueError('Choose add or dismiss')
        import graph
        stamp = now()
        with self.connect() as db:
            ensure(db)
            db.execute('BEGIN IMMEDIATE')
            row = db.execute("SELECT * FROM contact_shares WHERE id=? AND status='waiting'", (str(share_id),)).fetchone()
            if not row:
                raise ValueError('That one was added or dismissed already')
            card = json.loads(row['card'])
            node_id, stage = None, 'dismissed'
            if choice == 'add':
                found = self._existing(db, card)
                if found:
                    node_id, stage = found['id'], 'merged'
                    self._merge(db, found['id'], card, stamp)
                else:
                    made = graph.create_record(db, 'person', {'name': card['name'], 'email': (card.get('emails') or [''])[0], 'org': card.get('org', '')}, stamp)
                    if made.get('yours'):
                        raise ValueError('That’s your own address: it’s in About you')
                    node_id, stage = made['node_id'], 'added' if made.get('created') else 'merged'
                    if made.get('created'):
                        fields = {}
                        if card.get('emails', [])[1:]:
                            fields['emails'] = {'added': card['emails'][1:], 'removed': []}
                        if card.get('phones'):
                            fields['phones'] = {'added': card['phones'], 'removed': []}
                        if card.get('role'):
                            fields['title'] = card['role']
                        if row['group_kind'] == 'work':
                            fields['side'] = 'work'
                        if fields:
                            db.execute('INSERT OR REPLACE INTO person_edits(identifier,fields,updated_at) VALUES(?,?,?)', (node_id, json.dumps(fields), stamp))
                    else:
                        self._merge(db, node_id, card, stamp)
                db.execute('INSERT OR REPLACE INTO contact_marks(identifier,by_name,group_kind,note,at) VALUES(?,?,?,?,?)',
                           (node_id, row['name'], row['group_kind'], card.get('note'), stamp))
            db.execute('UPDATE contact_shares SET status=?,node_id=?,decided_at=? WHERE id=?', (stage, node_id, stamp, row['id']))
            self.log(db, 'in', row['fleet'], row['member_id'], row['name'], KIND, question_text(card),
                     {'added': 'added to your Graph', 'merged': 'added to someone in your Graph', 'dismissed': 'dismissed'}[stage])
        added = stage != 'dismissed'
        try:
            self.relay.call('POST', '/answer', {'id': row['id'], 'status': 'answered' if added else 'declined', **({'answer': {'stage': stage}} if added else {})})
        except (ValueError, OSError):
            pass  # the share is decided here; the sender sees "no answer" when their side expires
        if added and self.graph_build:
            self.graph_build()
        return {'status': stage, 'node_id': node_id, 'name': card['name']}

    @staticmethod
    def _merge(db, node_id, card, stamp):
        """Adds what the card has and the person doesn't: emails, phones, their role and organization when they have none.
        Never takes anything off or changes what's there."""
        import graph
        row = db.execute("SELECT info FROM graph_nodes WHERE id=? AND kind='person'", (node_id,)).fetchone()
        if not row:
            return
        info = json.loads(row['info'] or '{}')
        fields = {}
        for field in ('emails', 'phones'):
            have = [e.get('value') for e in info.get(field) or [] if isinstance(e, dict) and e.get('value')]
            keys = {graph.contact_key(field, v) for v in have}
            new = [v for v in card.get(field, []) if graph.contact_key(field, v) not in keys]
            if new:
                fields[field] = have + new
        if card.get('role') and not (info.get('profile') or {}).get('title'):
            fields['title'] = card['role']
        if fields:
            graph.person_edit(db, node_id, fields, stamp)
        if card.get('org') and not info.get('org'):
            graph.set_org(db, node_id, card['org'], 'owner', stamp)

    @staticmethod
    def contact_mark(db, node_id):
        """'Shared by <name>' on a person's page, with their note, when a share made or joined this person."""
        ensure(db)
        row = db.execute('SELECT info FROM graph_nodes WHERE id=?', (str(node_id or ''),)).fetchone()
        ids = sorted(set(json.loads(row['info'] or '{}').get('identifiers') or ()) | {str(node_id or '')}) if row else [str(node_id or '')]
        found = db.execute(f"SELECT by_name,group_kind,note,at FROM contact_marks WHERE identifier IN ({','.join('?' * len(ids))}) ORDER BY at DESC LIMIT 1",
                           ids).fetchone()
        return {'by': found['by_name'], 'kind': found['group_kind'], 'note': found['note'], 'at': found['at'][:10]} if found else None
