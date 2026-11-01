"""Scheduling between Machines, when the other person has no Machine: a link to pick a time
(docs/scheduling-between-machines.md, "No Machine: a link to pick a time"). Mixed into fleet.Fleet next to meet.Meet.

When the proposer's ask falls back (no Machine found, no answer, no time that fits both, too many rounds), this Machine
makes a link to a page where the other person picks one of the owner's free times, and adds it to the email draft on
the to-do. Nothing leaves before the owner taps Send on that draft.

- The page is a task link of kind schedule (task_invites.py, the cloud's /t/<id>): sealed here with a fresh key that
  only travels in the link's #fragment, so the cloud keeps an opaque blob. It holds the owner's first name, the length,
  free start times only (the same rules as an answer to another Machine: work hours, buffer, the 15-minute grid, at most
  14 days ahead) and whether to show the footer line. No event, title or anything else about the owner.
- The pick comes back sealed with a key derived from the link's (the Network round). It is only a start time, and
  only one of those offered and still free. It becomes a to-do with Book it and Not needed. Book it is the owner's
  calendar write with the invite to the address the to-do's email went to, never one from the page.
- The link ends once the meeting is booked or not needed (revoked: the cloud deletes it at once), and after 14 days at
  most. The times on it follow the calendar (sealed again at most hourly). Each step is a line in Activity.
- Footer: "<Name>'s Machine found these times. Get yours." on the page only, on by default, off in the setting. The
  email carries no branding: it stays the owner's own words, with the link behind "Pick a time".

The app wires meet_link_draft(card_id, email, lines) -> bool: adds the lines to the to-do's email draft to that
address while it is a draft (False: tried again next round, for DRAFT_DAYS)."""
from __future__ import annotations

import datetime as dt
import json
import logging
import uuid

import task_invites
from i18n import t
import meet as m

LOG = logging.getLogger('personal-assistant')
SCHEMA = ('CREATE TABLE IF NOT EXISTS meet_links(session TEXT PRIMARY KEY,card_id TEXT,pick_card TEXT,state TEXT NOT NULL,'
          'record TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL)')
NOTES = ('no_machine', 'no_answer', 'keys', 'no_slot', 'rounds', 'failed')  # why the ask fell back: a link helps
PER_DAY = 6        # starts offered on one day
TOTAL = 40         # starts on one page
STEP = 30          # minutes between offered starts
REFRESH = 3600     # seconds between looks at the calendar for the page's times
DRAFT_DAYS = 3     # the link waits this long for its email draft, then ends
OFFER_HOURS = 24   # a fallback this recent gets a link


def ensure(db):
    db.execute(SCHEMA)


def starts(free, minutes, liked=(), tz=dt.timezone.utc, per_day=PER_DAY, total=TOTAL):
    """Start times to offer: on the grid, every STEP minutes, where `minutes` fit inside a free span. Preferred ones
    first on each day, at most per_day a day (in the owner's time zone) and total in all, in time order."""
    length = dt.timedelta(minutes=minutes)
    liked_spans = m._spans(liked)
    days = {}
    for a, b in m._spans(free):
        cursor = m.ceil_grid(a)
        while cursor + length <= b:
            days.setdefault(cursor.astimezone(tz).date(), []).append(cursor)
            cursor += dt.timedelta(minutes=STEP)
    out = []
    for day in sorted(days):
        found = sorted(days[day], key=lambda c: (not m._inside(liked_spans, c, c + length), c))[:per_day]
        out += sorted(found)
    return [m.slot_text(c) for c in out[:total]]


def first_name(name):
    return (str(name or '').split() or [''])[0][:40]


def email_lines(link):
    """What goes into the email draft: one line, the link behind the words "Pick a time" (next_actions mail marks: in
    the HTML part a link, in the plain-text part the words with the address on its own line). No branding: the email
    stays the owner's own words; the footer line is on the page only (the setting)."""
    return [f'[Pick a time]({link})']


def with_lines(body, lines):
    """The email with the link's lines, just before the sign-off (or at the end). Once."""
    if lines[0] in body:
        return body
    block = '\n'.join(lines)
    i = body.rfind('\n\nBest,')
    return body[:i] + f'\n\n{block}' + body[i:] if i >= 0 else body.rstrip() + f'\n\n{block}'


def open_pick(sealed, key, offered):
    """A pick from the page: one of the start times offered, or ValueError. Nothing else is read from it."""
    found = task_invites._open(sealed, task_invites.derived(key, 'reply'))
    slot = found.get('slot') if isinstance(found, dict) and found.get('answer') == 'pick' else None
    if not isinstance(slot, str) or slot not in offered:
        raise ValueError('not a time this link offered')
    return slot


def _kept(record):
    """A record once its link ended: no key or link stays."""
    return {k: v for k, v in record.items() if k not in ('key', 'link')}


class MeetLink:
    """Mixed into fleet.Fleet with meet.Meet. meet_link_draft is set by the app (meet_app.py)."""
    meet_link_draft = None

    def _link_save(self, session, state, record, card_id=None, pick_card=None):
        at = m.stamp(self._meet_now())
        with self.connect() as db:
            ensure(db)
            db.execute('INSERT INTO meet_links(session,card_id,pick_card,state,record,created_at,updated_at) VALUES(?,?,?,?,?,?,?) '
                       'ON CONFLICT(session) DO UPDATE SET state=excluded.state,record=excluded.record,updated_at=excluded.updated_at,'
                       'pick_card=COALESCE(excluded.pick_card,meet_links.pick_card)',
                       (session, card_id, pick_card, state, json.dumps(record, ensure_ascii=False), at, at))

    def _link_row(self, session=None, card=None):
        with self.connect() as db:
            ensure(db)
            row = db.execute('SELECT * FROM meet_links WHERE session=?', (session,)).fetchone() if session else \
                db.execute('SELECT * FROM meet_links WHERE pick_card=? ORDER BY updated_at DESC LIMIT 1', (card,)).fetchone()
        return (row, json.loads(row['record'])) if row else (None, None)

    def _link_log(self, what, record, args, outcome, card_id):
        with self.connect() as db:
            self._meet_log(db, what, record.get('name') or record.get('email'), args, outcome, None, card_id)

    def _link_times(self, record):
        with self.connect() as db:
            free, liked = self._meet_mine(db, {'start': record['start'], 'days': record['days']})
        return starts(free, record['minutes'], liked, tz=self._meet_tz())

    def _link_page(self, record):
        return {'kind': 'schedule', 'from_name': first_name(self.config.get('owner_name')), 'minutes': record['minutes'],
                'slots': record['slots'], 'brand': bool(record.get('brand'))}

    # -- making one: for a fallen-back ask
    def meet_link_offers(self):
        """Links for asks that fell back lately and have none yet. Never fails the round."""
        if not self.meet_link_draft:
            return 0
        since = m.stamp(self._meet_now() - dt.timedelta(hours=OFFER_HOURS))
        with self.connect() as db:
            m.ensure(db)
            ensure(db)
            rows = db.execute(f"SELECT s.* FROM meet_sessions s LEFT JOIN meet_links l ON l.session=s.id WHERE s.role='asker' AND s.state='fallback' "
                              f"AND s.note IN ({','.join('?' * len(NOTES))}) AND s.updated_at>? AND l.session IS NULL LIMIT 10", (*NOTES, since)).fetchall()
        made = 0
        for row in rows:
            try:
                made += bool(self.meet_link_offer(row))
            except Exception as error:  # noqa: BLE001 - the to-do keeps its plain email draft; tried next round
                LOG.info('meet link not made error=%s', type(error).__name__)
        return made

    def meet_link_offer(self, row):
        if row['role'] != 'asker' or row['note'] not in NOTES or not row['email'] or not row['card_id']:
            return None
        record = {'start': row['start'], 'days': row['days'], 'minutes': row['minutes'], 'email': row['email'], 'name': row['name'] or '',
                  'brand': self.meet_setting().get('brand', True), 'version': 1, 'seen': 0, 'drafted': False, 'picks': 0}
        record['slots'] = self._link_times(record)
        if not record['slots']:
            self._link_save(row['id'], 'closed', record, card_id=row['card_id'])  # nothing free to offer: the plain draft stays
            return None
        last = dt.date.fromisoformat(record['start']) + dt.timedelta(days=record['days'])
        days = 7 if last <= (self._meet_now() + dt.timedelta(days=6)).date() else 14
        sealed, key = task_invites.seal(self._link_page(record))
        made = self.relay.call('POST', '/task-invite', {'action': 'create', 'kind': 'schedule', 'sealed': sealed, 'days': days,
                                                       'request_id': uuid.uuid5(uuid.NAMESPACE_URL, 'meet-link:' + row['id']).hex,
                                                       'check': task_invites.derived(key, 'check')}, timeout=20)
        record.update(invite_id=made['id'], key=key, link=made['url'] + '#k=' + key, until=str(made.get('expires_at') or '')[:10],
                      looked_at=m.stamp(self._meet_now()))
        self._link_save(row['id'], 'open', record, card_id=row['card_id'])
        self._link_log('link', record, [m.window_text(record)], 'made', row['card_id'])
        self._link_draft(row['id'], row['card_id'], record)
        return record['link']

    def _link_draft(self, session, card_id, record):
        """Adds the link to the to-do's email draft once there is one (the owner sees it before Send)."""
        try:
            added = self.meet_link_draft(card_id, record['email'], email_lines(record['link']))
        except Exception as error:  # noqa: BLE001 - tried again next round
            LOG.info('meet link draft error=%s', type(error).__name__)
            added = False
        if added:
            record['drafted'] = True
            self._link_save(session, 'open', record)
        return bool(added)

    def _link_end(self, row, record, state):
        try:
            self.relay.call('POST', '/task-invite', {'action': 'revoke', 'id': record['invite_id']}, timeout=20)
        except Exception as error:  # noqa: BLE001 - it ends by itself by its date
            LOG.info('meet link revoke error=%s', type(error).__name__)
        self._link_save(row['session'], state, _kept(record))

    # -- the round: picks, the page kept current, links that end
    def meet_links_round(self):
        if not self.meet_on or not self.meet_link_draft:
            return 0
        self.meet_link_offers()
        current = self._meet_now()
        with self.connect() as db:
            ensure(db)
            rows = db.execute("SELECT * FROM meet_links WHERE state IN ('open','picked')").fetchall()
        live = {}
        for row in rows:
            record = json.loads(row['record'])
            if record.get('until') and record['until'] < current.date().isoformat():
                self._link_save(row['session'], 'expired', _kept(record))
                self._link_log('link_ended', record, [m.window_text(record)], 'expired', row['card_id'])
                continue
            if not record.get('drafted') and not self._link_draft(row['session'], row['card_id'], record):
                if row['created_at'] < m.stamp(current - dt.timedelta(days=DRAFT_DAYS)):  # its email never got it: nobody has it
                    self._link_end(row, record, 'closed')
                    self._link_log('link_ended', record, [m.window_text(record)], 'unused', row['card_id'])
                continue
            live[record['invite_id']] = (row, record)
        if not live:
            return 0
        try:
            found = self.relay.call('POST', '/task-invite', {'action': 'status', 'ids': list(live)[:50],
                                                            'seen': {i: r['seen'] for i, (_, r) in live.items() if r.get('seen')}}, timeout=20)
        except Exception as error:  # noqa: BLE001 - next round
            LOG.info('meet link status error=%s', type(error).__name__)
            return 0
        taken = 0
        replies_by = (found.get('replies') or {}) if isinstance(found, dict) else {}
        for invite_id, (row, record) in live.items():
            replies = replies_by.get(invite_id) or []
            fresh = None
            for reply in sorted((r for r in replies if isinstance(r, dict) and isinstance(r.get('n'), int)), key=lambda r: r['n']):
                if reply['n'] <= record.get('seen', 0):
                    continue
                record['seen'] = reply['n']
                try:
                    fresh = open_pick(str(reply.get('sealed') or ''), record['key'], record['slots'])
                except (ValueError, TypeError, KeyError):
                    LOG.warning('meet link pick did not open')
            if fresh:  # their latest pick counts
                taken += self._link_picked(row, record, fresh)
                row, record = self._link_row(row['session'])
            elif replies:
                self._link_save(row['session'], row['state'], record)
            if (record.get('looked_at') or '') < m.stamp(current - dt.timedelta(seconds=REFRESH)):
                self._link_refresh(row, record)
        return taken

    def _link_refresh(self, row, record):
        """The page shows the owner's current free times (a pick still has to be free when it comes back)."""
        try:
            record['looked_at'] = m.stamp(self._meet_now())
            fresh = self._link_times(record)
            if fresh != record['slots']:
                record['slots'], record['version'] = fresh, record['version'] + 1
                sealed, _ = task_invites.seal(self._link_page(record), task_invites._unb64(record['key']))
                self.relay.call('POST', '/task-invite', {'action': 'update', 'id': record['invite_id'], 'sealed': sealed, 'version': record['version']}, timeout=20)
            self._link_save(row['session'], row['state'], record)
        except Exception as error:  # noqa: BLE001 - next round
            LOG.info('meet link refresh error=%s', type(error).__name__)

    def _link_picked(self, row, record, slot):
        """Their pick: one to-do for the owner with Book it, when the time is still free. Else Activity says so."""
        tz = self._meet_tz()
        start = m.parse_slot(slot)
        end = start + dt.timedelta(minutes=record['minutes'])
        when = m.when_text(start, tz)
        with self.connect() as db:
            free, _ = self._meet_mine(db, {'start': start.astimezone(tz).date().isoformat(), 'days': 1})
        if not m._inside(m._spans(free), start, end):
            self._link_save(row['session'], row['state'], record)
            self._link_log('picked_in', record, [when], 'taken', row['pick_card'] or row['card_id'])
            return 0
        old = row['pick_card']
        record['pick'], record['picks'] = [slot, m.slot_text(end)], record.get('picks', 0) + 1
        record.pop('note', None)
        name = record['name'] or record['email']
        card = None
        if self.meet_card:
            card = self.meet_card({'id': f"{row['session']}-pick{record['picks']}", 'name': name, 'email': record['email'],
                                   'title': m.todo_title(name),
                                   'body': t('{} picked this time on your booking link.', name)})
        self._link_save(row['session'], 'picked', record, pick_card=card)
        if old and old != card and self.meet_close:
            self.meet_close(old, t('They picked another time'))
        self._link_log('picked_in', record, [when], 'waiting', card or row['card_id'])
        return 1

    # -- the owner's taps on the pick's to-do
    def meet_link_decide(self, card_id, choice):
        """Book it or Not needed on a to-do from a pick. None when the to-do is not one."""
        row, record = self._link_row(card=str(card_id))
        if not row:
            return None
        if row['state'] != 'picked' or not record.get('pick'):
            raise ValueError('That time is no longer open')
        name = record['name'] or record['email']
        when = m.when_text(m.parse_slot(record['pick'][0]), self._meet_tz())
        if choice == 'skip':
            self._link_end(row, record, 'closed')
            self._link_log('canceled', record, [when], 'canceled', row['pick_card'])
            if self.meet_close:
                self.meet_close(row['pick_card'], t('Not needed'))
            return {'state': 'canceled'}
        if choice != 'book':
            raise ValueError('Book it or Not needed')
        result = {'status': 'failed'}
        if self.meet_book:
            try:  # the invite goes to the address the to-do's email went to, never one from the page
                result = self.meet_book({'id': row['session'], 'email': record['email'], 'name': record['name'],
                                         'slot': json.dumps(record['pick']), 'video': None}) or result
            except Exception as error:  # noqa: BLE001 - said on the to-do; Book it again tries again
                LOG.warning('meet link book error=%s', type(error).__name__)
        if result.get('status') != 'done':
            record['note'] = 'failed'
            self._link_save(row['session'], 'picked', record)
            self._link_log('booked', record, [when], 'failed', row['pick_card'])
            return {'state': 'failed'}
        record.pop('note', None)
        self._link_end(row, record, 'booked')
        self._link_log('booked', record, [when], 'booked', row['pick_card'])
        if self.meet_close:
            self.meet_close(row['pick_card'], t('Booked with {}', name))
        return {'state': 'booked'}

    def annotate_links(self, db, suggestions):
        """The link on its to-dos: the first one (the link in its email draft) and the pick's (Book it)."""
        ids = [s['id'] for s in suggestions if s.get('id')]
        if not ids or not db.execute("SELECT 1 FROM sqlite_master WHERE name='meet_links'").fetchone():
            return
        tz = self._meet_tz()
        by_card = {}
        for r in db.execute('SELECT * FROM meet_links WHERE card_id IN (SELECT value FROM json_each(?)) OR pick_card IN (SELECT value FROM json_each(?)) '
                            'ORDER BY updated_at', (json.dumps(ids), json.dumps(ids))):
            record = json.loads(r['record'])
            base = {'role': 'link', 'name': record.get('name') or record.get('email'), 'minutes': record.get('minutes'), 'video': None,
                    'mine_ok': False, 'their_ok': False, 'note': record.get('note')}
            if r['pick_card'] and record.get('pick'):
                start = m.parse_slot(record['pick'][0])
                by_card[r['pick_card']] = {**base, 'state': 'picked' if r['state'] == 'picked' else r['state'], 'when': m.when_text(start, tz),
                                           'start': record['pick'][0]}
            if r['card_id'] and record.get('drafted'):
                by_card[r['card_id']] = {**base, 'state': 'link', 'link_state': r['state'], 'until': record.get('until')}
        for s in suggestions:
            if s.get('id') in by_card:
                s['meet'] = by_card[s['id']]
