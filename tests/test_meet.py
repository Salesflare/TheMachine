"""Scheduling between Machines (meet.py, docs/scheduling-between-machines.md): two sandbox Machines that share no Fleet
talk through a local stand-in for the Network's meet route. It finds a Machine by a hash of an address, routes sealed
envelopes it can't read, and passes on each sender's verified addresses, as the cloud does. No network, no calendar
writes: booking is a hook that records what it was asked."""
import contextlib
import datetime as dt
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

import fleet
import meet
import network_crypto as nc
import security_levels

MONDAY = dt.datetime(2026, 11, 2, 7, 0, tzinfo=dt.timezone.utc)
HOURS = {'days': [1, 2, 3, 4, 5], 'start': '09:00', 'end': '17:00'}


class MeetNetwork:
    """The cloud's meet route for a few people: allow, find, send, inbox, ack. It stores what it's given and can't open
    sealed bodies."""
    def __init__(self):
        self.people, self.mail, self.finds, self.sent = {}, [], 0, []

    def person(self, name, email):
        self.people[name] = {'id': 'mt_' + name + '000000', 'emails': [email], 'allow': None, 'keys': None}

    def by_id(self, rid):
        return next((n for n, p in self.people.items() if p['id'] == rid), None)


class Relay:
    def __init__(self, net, me):
        self.net, self.me, self.down = net, me, False

    def call(self, method, path, body=None, timeout=40):
        if self.down:
            raise fleet.Unavailable('away')
        route = path.split('?')[0]
        mine = self.net.people[self.me]
        if route == '/directory':
            return {'fleets': []}
        if route == '/keys':
            mine['keys'] = {k: body[k] for k in ('v', 'box', 'sign', 'sig')}
            return {'ok': True}
        if route != '/meet':
            return {'ok': True}
        op = body.get('op')
        if op == 'allow':
            mine['allow'] = body['allow']
            return {'id': mine['id']}
        if op == 'find':
            self.net.finds += 1
            for name, p in self.net.people.items():
                if name != self.me and p['allow'] == 'freebusy' and p['keys'] and body['hash'] in {meet.email_hash(e) for e in p['emails']}:
                    return {'found': {'id': p['id'], 'keys': p['keys'], 'name': name.title()}}
            return {'found': None}
        if op == 'send':
            to = self.net.by_id(body['to'])
            if not to or self.net.people[to]['allow'] != 'freebusy' and not any(m['from'] == self.net.people[to]['id'] and m['to'] == mine['id'] for m in self.net.sent):
                raise ValueError('nobody to send to')
            assert set(body['sealed']) <= {'v', 'alg', 'eph', 'n', 'ct', 'mac', 'to', 'sig'}  # sealed only
            msg = {'id': body['id'], 'from': mine['id'], 'to': body['to'], 'sealed': body['sealed']}
            self.net.mail.append(msg)
            self.net.sent.append(msg)
            return {'ok': True}
        if op == 'inbox':
            out = []
            for m in self.net.mail:
                if m['to'] == mine['id']:
                    sender = self.net.people[self.net.by_id(m['from'])]
                    out.append({'id': m['id'], 'from': m['from'], 'name': self.net.by_id(m['from']).title(), 'emails': sender['emails'],
                                'keys': sender['keys'], 'sealed': m['sealed']})
            return {'messages': out}
        if op == 'ack':
            self.net.mail = [m for m in self.net.mail if not (m['to'] == mine['id'] and m['id'] in body['ids'])]
            return {'ok': True}
        raise ValueError('op')


class Machine:
    def __init__(self, root, net, name, email):
        self.root = Path(root) / name
        self.root.mkdir(parents=True)
        self.path = self.root / 'db.sqlite'
        net.person(name, email)
        config = {'database': str(self.path), 'network_keys': str(self.root / 'network-keys.json'),
                  'accounts': [{'id': 'cal-' + name, 'service': 'calendar', 'email': email}], 'fleet': {'url': 'https://cp.example/api/fleet'}}
        with self.connect() as db:
            db.executescript('CREATE TABLE events(id INTEGER PRIMARY KEY,account_id TEXT,source_id TEXT,kind TEXT,occurred_at TEXT,title TEXT,'
                             'body TEXT,metadata TEXT,deleted INTEGER DEFAULT 0);'
                             'CREATE TABLE graph_nodes(id TEXT PRIMARY KEY,kind TEXT,name TEXT,strength REAL,info TEXT);')
        self.relay = Relay(net, name)
        self.box = fleet.Fleet(self.connect, config, lambda: 'token', relay=self.relay)
        self.box.relay._publish()  # its keys on the Network, as a directory round does
        self.cards, self.closed, self.booked, self.threads = {}, {}, [], True
        self.clock = MONDAY
        box = self.box
        box.meet_on = True
        box.meet_clock = lambda: self.clock
        box.meet_tz = lambda: dt.timezone.utc
        box.meet_hours = lambda: HOURS
        box.meet_thread = lambda emails: self.threads
        box.meet_card = self.card
        box.meet_book = self.book
        box.meet_close = lambda card_id, why: self.closed.__setitem__(card_id, why)

    @contextlib.contextmanager
    def connect(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def card(self, session):
        card_id = 'card-' + str(len(self.cards) + 1)
        self.cards[card_id] = session['title']
        return card_id

    def book(self, session):
        self.booked.append({'slot': json.loads(session['slot']), 'email': session['email'], 'video': session['video']})
        return {'status': 'done'}

    def busy(self, start, end, title='Board review', **meta):
        with self.connect() as db:
            db.execute("INSERT INTO events(account_id,kind,occurred_at,title,metadata) VALUES(?,'calendar.event',?,?,?)",
                       (self.box.config['accounts'][0]['id'], start, title, json.dumps({'end_at': end, **meta})))

    def session(self, role=None):
        with self.connect() as db:
            return db.execute('SELECT * FROM meet_sessions' + (" WHERE role=?" if role else '') + ' ORDER BY rowid DESC LIMIT 1',
                              (role,) if role else ()).fetchone()

    def log(self):
        with self.connect() as db:
            return [dict(r) for r in db.execute('SELECT what,outcome,args FROM meet_log ORDER BY id')]


class Scheduling(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.net = MeetNetwork()
        self.ann = Machine(self.temp.name, self.net, 'ann', 'ann@one.example')
        self.bob = Machine(self.temp.name, self.net, 'bob', 'bob@two.example')
        for m in (self.ann, self.bob):
            m.box.meet_tell()

    def run_both(self, times=2):
        for _ in range(times):
            self.bob.box.meet_round(hinted=True)
            self.ann.box.meet_round(hinted=True)

    def test_negotiation_and_both_tap_booking(self):
        self.ann.busy('2026-11-03T09:00:00+00:00', '2026-11-03T12:00:00+00:00', 'Secret merger call', visibility='private')
        self.bob.busy('2026-11-03T12:07:00+00:00', '2026-11-03T13:52:00+00:00', 'Dentist')
        self.assertEqual(self.ann.box.meet_start('c1', 'Bob@two.example', 'Bob', minutes=30, start='2026-11-03', days=3), 'asked')
        self.run_both()
        mine = self.ann.session('asker')
        slot = json.loads(mine['slot'])
        # after Ann's 9-12 (plus her 10-minute buffer) and Bob's dentist widened to 12:00-14:00 plus his buffer
        self.assertEqual(slot, ['2026-11-03T14:15Z', '2026-11-03T14:45Z'])
        self.assertEqual(mine['state'], 'proposed')
        self.assertEqual([c.replace('\xa0', ' ') for c in self.bob.cards.values()], ['Meet Ann'])
        # Nothing about either calendar crossed the Network in the clear
        wire = json.dumps(self.net.sent)
        for word in ('Secret', 'merger', 'Dentist', 'private', 'T14:15'):
            self.assertNotIn(word, wire)
        # One tap is not enough
        self.assertEqual(self.ann.box.meet_decide('c1', 'book'), {'state': 'proposed', 'waiting': True})
        self.run_both()
        self.assertEqual(self.ann.booked, [])
        card = next(iter(self.bob.cards))
        self.bob.box.meet_decide(card, 'book')
        self.run_both()
        self.assertEqual(self.ann.booked, [{'slot': slot, 'email': 'bob@two.example', 'video': None}])
        self.assertEqual(self.ann.session('asker')['state'], 'booked')
        self.assertEqual(self.bob.session('answerer')['state'], 'booked')
        self.assertIn('c1', self.ann.closed)
        self.assertIn(card, self.bob.closed)
        self.assertEqual([l['what'] for l in self.bob.log()], ['asked_in', 'proposed_in', 'booked_in'])
        self.assertEqual([l['outcome'] for l in self.ann.log()], ['answered', 'sent', 'booked'])

    def test_book_it_on_the_other_side_first_then_the_proposer(self):
        self.ann.box.meet_start('c1', 'bob@two.example', 'Bob', start='2026-11-03', days=1)
        self.run_both()
        self.bob.box.meet_decide(next(iter(self.bob.cards)), 'book')
        self.run_both()
        self.assertEqual(self.ann.booked, [])
        self.assertEqual(self.ann.box.meet_decide('c1', 'book'), {'state': 'booked'})
        self.assertEqual(len(self.ann.booked), 1)

    def test_other_time_renegotiates_on_the_same_todos(self):
        self.ann.box.meet_start('c1', 'bob@two.example', 'Bob', start='2026-11-03', days=2)
        self.run_both()
        first = json.loads(self.ann.session('asker')['slot'])
        card = next(iter(self.bob.cards))
        self.bob.box.meet_decide(card, 'other')
        self.assertEqual(self.bob.session('answerer')['state'], 'waiting')
        self.run_both()
        again = self.ann.session('asker')
        self.assertNotEqual(json.loads(again['slot']), first)
        self.assertEqual(again['round'], 1)
        self.assertEqual(len(self.bob.cards), 1)  # still one to-do, with the new time
        self.assertEqual(self.bob.session('answerer')['state'], 'proposed')
        # the owner's own Other time, twice more: the email draft
        self.ann.box.meet_decide('c1', 'other')
        self.ann.box.meet_decide('c1', 'other')
        self.assertEqual(self.ann.session('asker')['state'], 'fallback')
        self.run_both()
        self.assertEqual(self.bob.session('answerer')['state'], 'canceled')
        self.assertIn(card, self.bob.closed)

    def test_not_needed_closes_both(self):
        self.ann.box.meet_start('c1', 'bob@two.example', 'Bob', start='2026-11-03', days=1)
        self.run_both()
        self.bob.box.meet_decide(next(iter(self.bob.cards)), 'skip')
        self.run_both()
        self.assertEqual(self.ann.session('asker')['state'], 'fallback')  # Ann's to-do keeps its email draft
        self.assertEqual(self.ann.session('asker')['note'], 'declined')

    def test_no_machine_falls_back_to_the_email_draft(self):
        self.assertEqual(self.ann.box.meet_start('c1', 'carol@three.example', 'Carol'), 'fallback')
        self.assertEqual(self.ann.session()['note'], 'no_machine')
        self.assertEqual(self.net.sent, [])
        with self.ann.connect() as db:
            lines = meet.activity_lines(db, 10)
        self.assertEqual(lines[0]['what'], 'Email draft kept for Carol: ' + meet.window_text({'start': '2026-11-03', 'days': 7}))
        self.assertEqual(lines[0]['detail'], 'No Machine found for them')

    def test_no_answer_in_time_falls_back(self):
        self.ann.box.meet_start('c1', 'bob@two.example', 'Bob')
        self.ann.clock += dt.timedelta(seconds=meet.ANSWER_WAIT + 1)
        self.ann.box.meet_round()
        self.assertEqual(self.ann.session()['state'], 'fallback')
        self.assertEqual(self.ann.session()['note'], 'no_answer')

    def test_a_stranger_without_a_shared_thread_is_refused(self):
        self.bob.threads = False
        self.ann.box.meet_start('c1', 'bob@two.example', 'Bob', start='2026-11-03', days=2)
        self.run_both()
        self.assertEqual(self.ann.session()['state'], 'fallback')
        self.assertEqual(self.ann.session()['free'], None)
        self.assertEqual(self.bob.log(), [{'what': 'asked_in', 'outcome': 'thread', 'args': json.dumps([meet.window_text({'start': '2026-11-03', 'days': 2})])}])
        self.assertEqual(self.bob.cards, {})

    def test_the_default_thread_check_needs_mail_both_ways(self):
        self.bob.box.meet_thread = None
        with self.bob.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,info) VALUES('email:ann@one.example','person','Ann',1,?)",
                       (json.dumps({'wrote': 0, 'heard': 3}),))
            self.assertFalse(self.bob.box._meet_thread(db, ['ann@one.example']))
            db.execute("UPDATE graph_nodes SET info=? WHERE id='email:ann@one.example'", (json.dumps({'wrote': 1, 'heard': 3}),))
            self.assertTrue(self.bob.box._meet_thread(db, ['ann@one.example']))

    def test_rate_limits(self):
        for n in range(meet.PEER_PER_DAY + 1):
            self.ann.box.meet_start('c%d' % n, 'bob@two.example', 'Bob', start='2026-11-03', days=1)
            self.bob.box.meet_round(hinted=True)
        self.assertEqual([l['outcome'] for l in self.bob.log() if l['what'] == 'asked_in'][-1], 'limit')
        with self.ann.connect() as db:  # and this Machine asks others only so often a day
            db.execute("UPDATE meet_sessions SET created_at=?", (meet.stamp(MONDAY),))
            for n in range(meet.STARTS_PER_DAY):
                db.execute("INSERT INTO meet_sessions(id,peer,role,state,start,days,minutes,created_at,updated_at) "
                           "VALUES(?, '-', 'asker', 'fallback', '2026-11-03', 1, 30, ?, ?)", ('%032x' % n, meet.stamp(MONDAY), meet.stamp(MONDAY)))
        finds = self.net.finds
        self.assertEqual(self.ann.box.meet_start('cx', 'bob@two.example', 'Bob'), 'fallback')
        self.assertEqual(self.net.finds, finds)

    def test_free_busy_for_scheduling_is_the_default(self):
        self.assertEqual(self.ann.box.meet_setting()['allow'], 'freebusy')  # a new Machine
        with self.ann.connect() as db:  # one from before this setting: other security settings saved, this one not
            db.execute(security_levels.SCHEMA)
            db.execute("DELETE FROM security_prefs WHERE key='meet_asks'")
            db.execute("INSERT OR REPLACE INTO security_prefs(key,value) VALUES('notify_text','off')")
        self.assertEqual(self.ann.box.meet_setting()['allow'], 'freebusy')
        self.assertEqual(self.net.people['ann']['allow'], 'freebusy')  # and the cloud was told so

    def test_setting_off_answers_nobody(self):
        self.bob.box.meet_set(allow='off')
        self.assertEqual(self.net.people['bob']['allow'], 'off')
        self.assertEqual(self.ann.box.meet_start('c1', 'bob@two.example', 'Bob'), 'fallback')  # not found at all
        # and a Machine that found Bob before Off gets a refusal, not free times
        self.net.people['bob']['allow'] = 'freebusy'
        self.ann.box.meet_start('c2', 'bob@two.example', 'Bob')
        self.net.people['bob']['allow'] = 'off'
        self.run_both()
        self.assertEqual(self.bob.log()[-1]['outcome'], 'off')
        self.assertEqual(self.ann.session()['state'], 'fallback')

    def test_careful_sends_no_time_before_the_owners_tap(self):
        with self.ann.connect() as db:
            security_levels.apply(db, 'careful')
        self.assertEqual(self.ann.box.meet_setting()['allow'], 'off')  # Careful: nobody may ask this one
        self.ann.box.meet_start('c1', 'bob@two.example', 'Bob', start='2026-11-03', days=1)
        self.run_both()
        self.assertEqual(self.ann.session('asker')['state'], 'proposed')
        self.assertEqual(self.ann.session('asker')['sent'], 0)
        self.assertEqual(self.bob.cards, {})  # Bob's Machine has no time yet
        self.ann.box.meet_decide('c1', 'book')
        self.run_both()
        self.assertEqual(len(self.bob.cards), 1)
        self.bob.box.meet_decide(next(iter(self.bob.cards)), 'book')
        self.run_both()
        self.assertEqual(len(self.ann.booked), 1)

    def test_changed_keys_are_refused(self):
        self.ann.box.meet_start('c1', 'bob@two.example', 'Bob')
        self.run_both()
        self.bob.box.relay.private = nc.new_keys()
        self.bob.box.relay.public = nc.public_keys(self.bob.box.relay.private)
        self.bob.box.relay._publish()
        self.assertEqual(self.ann.box.meet_start('c2', 'bob@two.example', 'Bob'), 'fallback')
        self.assertEqual(self.ann.session()['note'], 'keys')


class Limits(unittest.TestCase):
    def test_the_window_is_at_most_14_days_and_near(self):
        today = dt.date(2026, 11, 2)
        self.assertEqual(meet.parse_window('2026-11-03', 14, today), {'start': '2026-11-03', 'days': 14})
        for start, days in (('2026-11-03', 15), ('2026-11-03', 0), ('2027-03-01', 1), ('2026-11-3', 2), ('2026-11-03', True)):
            self.assertIsNone(meet.parse_window(start, days, today))

    def test_answers_are_rounded_to_15_minutes_inside_work_hours(self):
        busy = [['2026-11-03T10:07Z', '2026-11-03T10:52Z']]
        free, liked = meet.free_times(busy, {'start': '2026-11-03', 'days': 1}, HOURS, dt.timezone.utc, 0, 'morning', MONDAY)
        self.assertEqual(free, [['2026-11-03T09:00Z', '2026-11-03T10:00Z'], ['2026-11-03T11:00Z', '2026-11-03T17:00Z']])
        self.assertEqual(liked, [['2026-11-03T09:00Z', '2026-11-03T10:00Z'], ['2026-11-03T11:00Z', '2026-11-03T12:00Z']])
        for a, b in free:
            self.assertEqual((int(a[14:16]) % 15, int(b[14:16]) % 15), (0, 0))
        # a weekend day and a window outside work hours give nothing
        self.assertEqual(meet.free_times([], {'start': '2026-11-07', 'days': 2}, HOURS, dt.timezone.utc, current=MONDAY)[0], [])

    def test_meetings_end_by_18_even_with_late_work_hours(self):
        free, _ = meet.free_times([], {'start': '2026-11-03', 'days': 1}, {**HOURS, 'end': '23:00'}, dt.timezone.utc, current=MONDAY)
        self.assertEqual(free[-1][1], '2026-11-03T18:00Z')

    def test_a_peers_times_are_kept_to_the_window_and_the_grid(self):
        window = {'start': '2026-11-03', 'days': 1}
        kept = meet.clean_times([['2026-11-03T09:00Z', '2026-11-03T10:00Z'], ['2026-11-03T09:07Z', '2026-11-03T10:00Z'],
                                 ['2026-11-20T09:00Z', '2026-11-20T10:00Z'], ['x', 'y'], 'nope'], window)
        self.assertEqual(kept, [['2026-11-03T09:00Z', '2026-11-03T10:00Z']])

    def test_pick_prefers_what_both_like(self):
        mine = [['2026-11-03T09:00Z', '2026-11-03T17:00Z']]
        theirs = [['2026-11-03T10:00Z', '2026-11-03T16:00Z']]
        liked = [['2026-11-03T13:00Z', '2026-11-03T17:00Z']]
        self.assertEqual(meet.pick(mine, theirs, 30), ['2026-11-03T10:00Z', '2026-11-03T10:30Z'])
        self.assertEqual(meet.pick(mine, theirs, 30, liked, liked), ['2026-11-03T13:00Z', '2026-11-03T13:30Z'])
        self.assertEqual(meet.pick(mine, theirs, 30, rejected=['2026-11-03T10:00Z']), ['2026-11-03T10:15Z', '2026-11-03T10:45Z'])
        self.assertIsNone(meet.pick(mine, [['2026-11-03T10:00Z', '2026-11-03T10:15Z']], 30))

    def test_the_lookup_never_carries_the_address(self):
        self.assertNotIn('bob', meet.email_hash('Bob@two.example'))
        self.assertEqual(meet.email_hash(' Bob@Two.example '), meet.email_hash('bob@two.example'))


if __name__ == '__main__':
    unittest.main()
