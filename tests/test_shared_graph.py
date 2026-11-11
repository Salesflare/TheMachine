"""The Shared Graph (shared_graph.py, docs/shared-graph.md): a Work Fleet's Machines share their Work records, timelines
and client threads, sealed Machine to Machine. A fake Network stands in for the control plane, honest or not: it keeps
the sealed blobs until every Machine they were sealed for took them, and can't read, change, replay or forge them. No network, no model."""
import copy
import datetime as dt
import importlib.util
import json
import shutil
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

spec = importlib.util.spec_from_file_location('graph_share_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
fleet, graph = a.fleet, a.graph
import fleet_trust as ft
import message_seal
import network_crypto as nc
import shared_graph as sg
import shared_graph_logos as sgl
from kept_connections import kept_connections

FLEET = 'fl_' + '3' * 16
BODY = 'The renewal quote for 40 seats is attached, valid until Friday.'
HEALTH = 'I will be out for surgery next week, please keep this between us.'
INTERNAL = 'Can you cover my Tuesday standup?'
PERSONAL = 'Dinner at ours on Saturday?'
DEAL = 'Our offer values the company at twelve million.'


def ago(days, hours=0):
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days, hours=hours)).isoformat(timespec='seconds')


class FakeNetwork:
    """Membership, roles, public keys and trust statements, as the control plane keeps them, and the Network's mailbox:
    sealed blobs, with a wrap per recipient, paged by the wraps' own sequence, each gone once its Machine took it."""
    def __init__(self):
        self.people = {'own1': ('Olive', 'owner'), 'adm2': ('Ada', 'admin'), 'mem3': ('Mo', 'member')}
        self.keys, self.trust, self.calls, self.blobs, self.wraps = {}, [], [], {}, []
        self.extra_members, self.gone = [], set()

    def held(self):
        """The blobs the mailbox still holds: those with a wrap nobody took yet."""
        return {w[0] for n, w in enumerate(self.wraps, 1) if n not in self.gone}

    def expire(self, member):
        """30 days on: what waited for this Machine is gone from the mailbox."""
        self.gone |= {n for n, w in enumerate(self.wraps, 1) if w[1] == member}

    def directory(self, me):
        if me not in self.people:
            return {'fleets': []}
        members = [{'member_id': m, 'name': n, 'label': n, 'role': r, 'account_email': m + '@acme.example', 'emails': [m + '@acme.example'],
                    'keys': self.keys.get(m), **({'me': True} if m == me else {})} for m, (n, r) in self.people.items()]
        group = {'id': FLEET, 'kind': 'work', 'name': 'Acme', 'asks': ['relationships'], 'trust': copy.deepcopy(self.trust),
                 'members': members + copy.deepcopy(self.extra_members), 'shared': [],
                 **({'security': {'level': self.level}} if getattr(self, 'level', None) else {})}
        return {'fleets': [group]}

    def graph_get(self, me, after):
        items = []
        for wseq, (blob_id, to, wrap, by) in enumerate(self.wraps, 1):
            if wseq > after and to == me and wseq not in self.gone:
                b = self.blobs[blob_id]
                items.append({'cursor': wseq, 'header': copy.deepcopy(b['header']), 'ct': b['ct'], 'sig': b['sig'], 'wrap': wrap, 'by': by})
        return {'items': items[:50], 'more': len(items) > 50}


class FakeRelay:
    def __init__(self, net, me):
        self.net, self.me = net, me

    def call(self, method, path, body=None, timeout=40):
        route = path.split('?')[0]
        self.net.calls.append((self.me, method, route, copy.deepcopy(body)))
        if self.me not in self.net.people and route not in ('/directory', '/me', '/keys'):
            raise ValueError('not in a Fleet')
        if route == '/directory':
            return self.net.directory(self.me)
        if route == '/keys':
            self.net.keys[self.me] = {k: body[k] for k in ('v', 'box', 'sign', 'sig')}
            return {'ok': True}
        if route == '/trust':
            self.net.trust.append(body['item'])
            return {'ok': True}
        if route == '/graph' and method == 'POST':
            if body['op'] == 'put':
                blob = body['blob']
                header = blob['header']
                assert header['from'] == self.me  # the control plane checks the publisher is who calls
                for n, w in enumerate(self.net.wraps, 1):  # as the control plane: a new snapshot or tag replaces what wasn't taken
                    old = self.net.blobs[w[0]]['header']
                    if n in self.net.gone or old['from'] != self.me:
                        continue
                    if header['kind'] == 'snapshot' and old['kind'] in ('snapshot', 'delta') and (
                            not header.get('only') or (old.get('only') and old.get('tag') == header.get('tag'))):
                        self.net.gone.add(n)  # the team's snapshot ends every chain; a chain's own only its own
                    elif header['kind'] in ('mail', 'file', 'ask', 'want') and old['kind'] == header['kind'] and old.get('tag') == header.get('tag'):
                        self.net.gone.add(n)
                self.net.blobs[header['id']] = {k: blob[k] for k in ('header', 'ct', 'sig')}
                for to, wrap in blob['wraps'].items():
                    if to in self.net.people:  # only members of the Fleet
                        self.net.wraps.append((header['id'], to, wrap, self.me))
            elif body['op'] == 'relay':  # passed on as its publisher signed it, a key sealed again for who missed it
                blob = body['blob']
                header = blob['header']
                assert header['kind'] in ('snapshot', 'delta', 'mail', 'file')
                if header.get('only') and set(body['wraps']) - set(header['to']):
                    raise ValueError('shared by name: only to the members it was sealed for')  # the control plane refuses it
                self.net.blobs.setdefault(header['id'], {k: blob[k] for k in ('header', 'ct', 'sig')})
                waiting = {w[1] for n, w in enumerate(self.net.wraps, 1) if w[0] == header['id'] and n not in self.net.gone}
                for to, wrap in body['wraps'].items():
                    if to in self.net.people and to != self.me and to not in waiting:
                        self.net.wraps.append((header['id'], to, wrap, self.me))
            elif body['op'] == 'ack':
                ids = set(body['ids'])
                self.net.gone |= {n for n, w in enumerate(self.net.wraps, 1) if w[1] == self.me and w[0] in ids}
            return {'ok': True}
        if route == '/graph':
            after = int(path.split('after=')[1].split('&')[0])
            return self.net.graph_get(self.me, after)
        if route == '/inbox':
            return {'asks': [], 'answers': [], 'ack': True}
        return {'ok': True}


def mail(account, n, sender, to, title, body, days, thread, cc=''):
    return {'account_id': account, 'source_id': f'{account}-{n}', 'kind': 'gmail.message', 'occurred_at': ago(days), 'title': title, 'body': body,
            'deleted': False, 'metadata': {'from': sender, 'to': to, 'cc': cc, 'labels': ['INBOX'], 'message-id': f'<{account}{n}@x>', 'thread_id': thread}}


class SharedGraph(unittest.TestCase):
    PROTECT = None  # Sealed (below) runs the rules that read the messages themselves on a store with message protection on

    def machine(self, me, device='', kept=None):
        """A Machine of the made-up Fleet. kept: its Store's state when its database was copied (setUp): the Store opens
        that copy as it was, without its schema checks and migrations again, which took a third of each test."""
        root = Path(self.temp.name) / (me + device)
        root.mkdir(parents=True, exist_ok=True)
        email = me + '@acme.example'
        config = {'database': str(root / 'events.sqlite'), 'network_keys': str(root / 'network-keys.json'), 'credentials': {},
                  'fleet': {'url': 'https://cp.example/api/fleet'},
                  'accounts': [{'id': 'work', 'email': email, 'service': 'gmail', 'boundary': 'work:Acme'},
                               {'id': 'home', 'email': me + '@home.example', 'service': 'gmail', 'boundary': 'personal:Home'}]}
        if kept is None:
            store = a.Store(root / 'events.sqlite', protect=self.PROTECT)
        else:
            store = object.__new__(a.Store)
            store.__dict__.update(kept, path=root / 'events.sqlite')
            if store.sealer:  # the copy's own key file (the same key)
                store.sealer = message_seal.Sealer(message_seal.load_key(store.path))
        box = fleet.Fleet(kept_connections(store, self.addCleanup), config, lambda: 'token', relay=FakeRelay(self.net, me))
        box.member_id, box.store, box.email = me, store, email
        return box

    # The three Machines as setUp leaves them, kept once per variant of it and copied for every test: getting there
    # takes hundreds of key wraps and nine Graph rounds, which made this file take ten minutes.
    _ready = {}

    @classmethod
    def setUpClass(cls):
        cls._kept = tempfile.TemporaryDirectory(); cls.addClassCleanup(cls._kept.cleanup)
        cls._ready = {}

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        variant = (self._testMethodName.startswith('test_sharing_is_off_until'), self._testMethodName.startswith('test_the_first_share'))
        if variant in self._ready:
            folder, net, last, stores = self._ready[variant]
            shutil.copytree(folder, self.temp.name, dirs_exist_ok=True)
            self.net = copy.deepcopy(net)
            self.own, self.adm, self.mem = (self.machine(me, kept=stores[me]) for me in ('own1', 'adm2', 'mem3'))
            self.boxes = [self.own, self.adm, self.mem]
            for box in self.boxes:
                box.last = copy.deepcopy(last[box.member_id])
            hold = sg.HOLD; sg.HOLD = 0; self.addCleanup(setattr, sg, 'HOLD', hold)
            return
        self._set_up()
        for box in self.boxes:
            box.connect.close()  # all written to the database files before they are copied
        folder = Path(self._kept.name) / str(len(self._ready))
        shutil.copytree(self.temp.name, folder)
        self._ready[variant] = (folder, copy.deepcopy(self.net), {box.member_id: copy.deepcopy(box.last) for box in self.boxes},
                                {box.member_id: {k: v for k, v in vars(box.store).items() if k not in ('path', 'sealer')} | {'sealer': box.store.sealer}
                                 for box in self.boxes})

    def _set_up(self):
        self.net = FakeNetwork()
        self.own, self.adm, self.mem = self.machine('own1'), self.machine('adm2'), self.machine('mem3')
        self.boxes = [self.own, self.adm, self.mem]
        self.rounds()
        self.ok(self.own, 'admin', 'Ada')  # the owner's OK: Ada is an admin
        self.rounds()
        self.ok(self.adm, 'member', 'Mo')  # an admin's OK: Mo's Machine gets the team's Graph
        hold = sg.HOLD; sg.HOLD = 0; self.addCleanup(setattr, sg, 'HOLD', hold)  # its own test below
        if not self._testMethodName.startswith('test_sharing_is_off_until'):
            self.own.graph_pause(FLEET, False)  # an admin turned the team's Graph on (off by default: experimental)
        for box in self.boxes:
            if not self._testMethodName.startswith('test_the_first_share'):
                box.set_meta('graph_start:' + FLEET, {'shown': a.now(), 'started': a.now()})  # the owners looked it over
        self.rounds()

    def rounds(self, n=2):
        for _ in range(n):
            for box in self.boxes:
                box.directory(refresh=True)
                box.shared_round()
                box.graph_round(force=True)

    def ok(self, box, kind, name):
        prompt = next(p for p in box._prompts() if p['kind'] == kind and p['name'] == name)
        return box.share_ok(prompt['id'], 'yes')

    def add(self, box, *events):
        for e in events:
            box.store.commit_page(e['account_id'], {}, [e])
        with box.store.connect() as db:
            db.isolation_level = None
            graph.build(db, box.config, a.now())

    def event_id(self, box, source_id):
        with box.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (source_id,)).fetchone()[0]

    def judge(self, box, *calls):
        with box.store.connect() as db:
            sg.judge(db, [{'event_id': self.event_id(box, s), 'share': v, 'line': line} for s, v, line in calls])

    def team(self, box, table='team_records'):
        with box.store.connect() as db:
            sg.ensure(db)
            return [dict(r) for r in db.execute(f'SELECT * FROM {table}')]

    def olive_mail(self):
        """Olive's Machine: a client thread, a sensitive one with the same client, one with only colleagues, and her
        personal account."""
        self.add(self.own,
                 mail('work', 1, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Renewal quote', BODY, 3, 't-renewal'),
                 mail('work', 2, 'Olive <own1@acme.example>', 'lee@client.example', 'Re: Renewal quote', 'Thanks, Lee. Checking with finance.', 2, 't-renewal'),
                 mail('work', 3, 'Lee Park <lee@client.example>', 'own1@acme.example', 'A personal note', HEALTH, 2, 't-health'),
                 mail('work', 4, 'Ada <adm2@acme.example>', 'own1@acme.example', 'Standup', INTERNAL, 1, 't-standup'),
                 mail('home', 5, 'Sam Friend <sam@friends.example>', 'own1@home.example', 'Saturday', PERSONAL, 1, 't-dinner'))
        self.judge(self.own, ('work-1', 'client', 'Lee asked for the renewal quote'), ('work-3', 'sensitive', 'Lee wrote about something private'),
                   ('work-4', 'internal', 'Ada asked about the standup'))

    # -- the whole way
    def test_client_thread_reaches_teammates_and_the_network_reads_none_of_it(self):
        self.olive_mail()
        self.rounds()
        for box in (self.adm, self.mem):
            people = [json.loads(r['body']) for r in self.team(box) if r['kind'] == 'person']
            self.assertEqual([p['name'] for p in people], ['Lee Park'])
            self.assertIn('Lee asked for the renewal quote', [x['line'] for x in people[0]['timeline']])
            threads = [json.loads(r['body']) for r in self.team(box, 'team_mail')]
            full = next(t for t in threads if not t.get('private'))
            self.assertEqual(full['subject'], 'Renewal quote')
            self.assertEqual(full['messages'][0]['body'], BODY)
        sent = json.dumps(self.net.calls) + json.dumps(self.net.blobs)
        for text in (BODY, 'Lee Park', 'lee@client.example', 'client.example', 'Renewal quote', 'renewal', HEALTH):
            self.assertNotIn(text, sent)  # every call and all the Network held: sealed

    def brief(self, box):
        with box.store.connect() as db:
            return box.compute(db, 'brief', {'since': ago(30)[:10]}, False, FLEET)

    def personal_and_client(self):
        """A client thread and a personal one in the same work account, both with people Olive writes back to."""
        self.add(self.own,
                 mail('work', 21, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Renewal quote', BODY, 3, 't-c'),
                 mail('work', 22, 'Olive <own1@acme.example>', 'lee@client.example', 'Re: Renewal quote', 'Checking.', 2, 't-c'),
                 mail('work', 23, 'Kai Moss <kai@pal.example>', 'own1@acme.example', 'Your daughter', 'Congrats on the graduation!', 3, 't-p'),
                 mail('work', 24, 'Olive <own1@acme.example>', 'kai@pal.example', 'Re: Your daughter', 'Thank you!', 2, 't-p'))
        self.judge(self.own, ('work-21', 'client', 'Lee asked for the quote'), ('work-23', 'personal', 'Kai wrote'))

    def test_a_brief_answer_holds_only_what_the_team_graph_shares_never_a_personal_thread(self):
        # Brief facts in a Work Fleet follow the Team Graph's sharing: the client thread counts, the personal one in the
        # same work account never does, and the ask is answered by itself (no approval card).
        self.personal_and_client()
        facts = self.brief(self.own)
        self.assertIn('client.example', [x['domain'] for x in facts['touched']])
        self.assertNotIn('pal.example', json.dumps(facts))
        with self.own.connect() as db:
            self.assertEqual(self.own.rule(db, FLEET, 'adm2', 'brief')[0], 'always')
        self.own.set_rule(FLEET, fleet.ALL, 'brief', 'never')  # Share my brief facts with the team: off
        with self.own.connect() as db:
            self.assertEqual(self.own.rule(db, FLEET, 'adm2', 'brief')[0], 'never')

    def test_sharing_is_off_until_an_admin_turns_it_on_and_brief_facts_hold_nothing_meanwhile(self):
        self.personal_and_client()
        facts = self.brief(self.own)
        self.assertEqual((facts['touched'], facts['unanswered'], facts['meetings'], facts['quiet']), ([], [], [], []))

    def test_personal_never_shared_not_even_that_it_exists(self):
        self.olive_mail()
        self.rounds()
        received = json.dumps(self.team(self.mem) + self.team(self.mem, 'team_mail'))
        for text in ('Sam', 'friends.example', 'Saturday', PERSONAL):
            self.assertNotIn(text, received)
        with self.own.store.connect() as db:
            labels = self.own.thread_labels(db, [dict(r) for r in db.execute('SELECT * FROM events')])
            self.assertNotIn(self.event_id(self.own, 'home-5'), labels)  # no label at all on a personal account

    def test_labels_read_only_their_own_threads_for_automated_mail_and_say_the_same(self):
        """A person's page labels its threads Team or Only you: whether a thread is automated mail is read from that
        thread's own messages, never from every mail message (seconds per page on a real mailbox), with the same labels."""
        self.olive_mail()
        receipt = mail('work', 80, 'Tool Co <hello@toolco.example>', 'own1@acme.example', 'Your receipt', 'Receipt 99, paid.', 1, 't-r')
        receipt['metadata']['labels'] = ['CATEGORY_UPDATES', 'INBOX']
        self.add(self.own, receipt, mail('work', 81, 'Site Audit <no-reply@audit.example>', 'own1@acme.example', 'Audit', 'Broken links.', 1, 't-audit'),
                 mail('work', 82, 'Olive <own1@acme.example>', 'no-reply@audit.example', 'Re: Audit', 'Thanks.', 0, 't-audit'),  # answered: not automated
                 mail('work', 83, 'Alerts <alerts@bank.example>', 'own1@acme.example', 'Alert', 'Login.', 1, None))  # no thread id
        self.judge(self.own, ('work-80', 'client', 'A receipt'), ('work-81', 'client', 'An audit'), ('work-83', 'client', 'An alert'))
        full_set = sg.Scope.automated.fget

        def never_all(scope):
            if scope._automated is None:
                raise AssertionError('read every mail message')
            return full_set(scope)
        with self.own.store.connect() as db:
            rows = [dict(r) for r in db.execute('SELECT * FROM events')]
            with patch.object(sg.Scope, 'automated', property(never_all)):
                fast = self.own.thread_labels(db, rows)
                one = self.own.thread_labels(db, [r for r in rows if r['source_id'] == 'work-80'])
            with patch.object(sg.Scope, 'automated_only', lambda scope, threads: None):  # every mail message, as before
                before = self.own.thread_labels(db, rows)
        self.assertEqual(fast, before)
        receipt_id = self.event_id(self.own, 'work-80')
        self.assertEqual(one, {receipt_id: before[receipt_id]})
        self.assertEqual(before[receipt_id]['why'], 'Only you: not a client conversation')  # automated mail, by rule
        self.assertNotEqual(before[self.event_id(self.own, 'work-81')]['view'], 'other')  # answered by the owner

    def test_a_personal_thread_in_a_work_account_never_goes_not_by_hand_nor_a_later_review(self):
        self.add(self.own, mail('work', 6, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Your daughter', 'Congrats on the graduation!', 1, 't-p'))
        self.judge(self.own, ('work-6', 'personal', 'Lee wrote'))
        self.rounds()
        self.assertEqual(self.team(self.mem, 'team_mail'), [])
        with self.own.store.connect() as db:
            with self.assertRaisesRegex(ValueError, 'Personal'):
                sg.set_hand(db, self.event_id(self.own, 'work-6'), 'team')
            label = self.own.thread_labels(db, [dict(db.execute("SELECT * FROM events WHERE source_id='work-6'").fetchone())])
        self.assertEqual((label[self.event_id(self.own, 'work-6')]['fixed'], label[self.event_id(self.own, 'work-6')]['view']), (True, 'personal'))
        app = object.__new__(a.App); app.store, app.fleet, app.config = self.own.store, self.own, self.own.config
        with self.assertRaisesRegex(ValueError, 'Personal threads are never shared'):
            app.graph_share_action('graph_share', {'event_id': self.event_id(self.own, 'work-6'), 'share': 'team'})
        self.judge(self.own, ('work-6', 'client', 'Lee asked for a quote'), ('work-6', 'other', 'A note'), ('work-6', 'client', 'Lee wrote'))
        self.rounds()
        received = json.dumps(self.team(self.mem) + self.team(self.mem, 'team_mail'))
        for text in ('graduation', 'Your daughter', 'Lee asked for a quote', 'Lee wrote'):
            self.assertNotIn(text, received)  # not the thread, not a line about it

    def test_a_thread_later_sorted_personal_is_taken_back_and_stays_personal(self):
        self.add(self.own, mail('work', 7, 'Lee Park <lee@client.example>', 'own1@acme.example', 'New phone', 'Your new phone ships Friday.', 1, 't-phone'))
        self.judge(self.own, ('work-7', 'client', 'Lee wrote about a phone'))
        self.rounds()
        self.assertIn('New phone', json.dumps(self.team(self.mem, 'team_mail')))
        self.judge(self.own, ('work-7', 'personal', 'Lee wrote'))
        self.rounds()
        self.assertNotIn('New phone', json.dumps(self.team(self.mem, 'team_mail')))  # the owner's Machine took it back
        for later in ('sensitive', 'client', 'internal'):  # a later review never turns it back, not even into a line
            self.judge(self.own, ('work-7', later, 'Lee wrote'))
            self.rounds()
            self.assertEqual(self.team(self.mem, 'team_mail'), [])
        with self.own.store.connect() as db:
            self.assertEqual(db.execute('SELECT verdict FROM share_threads').fetchone()[0], 'personal')

    def test_family_friends_and_people_marked_personal_never_go(self):
        family = {'id': 'fl_' + '4' * 16, 'kind': 'family', 'name': 'Home', 'members': [
            {'member_id': 'fm_partner', 'name': 'Hana Lane', 'emails': ['hana@studio.example']}]}
        fleets = self.own.fleets
        self.own.fleets = lambda: {**fleets(), family['id']: family}
        self.add(self.own,
                 mail('work', 8, 'Hana Lane <hana@studio.example>', 'own1@acme.example', 'Weekend plans', 'The kids want the beach.', 1, 't-hana'),
                 mail('work', 9, 'Kim Moss <kim@pal.example>', 'own1@acme.example', 'Climbing trip', 'Trip is booked.', 1, 't-kim'),
                 mail('work', 10, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Renewal quote', BODY, 1, 't-renewal', cc='hana@studio.example'))
        with self.own.store.connect() as db:
            graph.person_edit(db, 'email:kim@pal.example', {'side': 'personal'}, a.now())
            db.commit()
            db.isolation_level = None
            graph.build(db, self.own.config, a.now())
        self.judge(self.own, ('work-8', 'client', 'Hana wrote'), ('work-9', 'client', 'Kim wrote'), ('work-10', 'client', 'Lee asked for a quote'))
        self.rounds()
        received = json.dumps(self.team(self.mem) + self.team(self.mem, 'team_mail'))
        for text in ('Hana', 'studio.example', 'beach', 'Kim', 'pal.example', 'Climbing', 'Renewal quote'):
            self.assertNotIn(text, received)  # a thread with a family member on it stays with the owner too
        with self.own.store.connect() as db:
            labels = self.own.thread_labels(db, [dict(r) for r in db.execute('SELECT * FROM events')])
        self.assertEqual({labels[self.event_id(self.own, s)]['share'] for s in ('work-8', 'work-9', 'work-10')}, {'only_you'})

    def test_a_shared_board_shares_every_project_and_someone_personal_on_one_stays_off_it(self):
        """Sharing a board shares every project on it. Someone Personal to the owner on one stays off it: no record, no
        mail, no line, and not their organization. Someone kept private by hand still keeps their project home."""
        self.add(self.own,
                 mail('work', 9, 'Kim Moss <kim@pal.example>', 'own1@acme.example', 'Climbing trip', 'Trip is booked.', 1, 't-kim'),
                 mail('work', 11, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Gym floor quote', BODY, 1, 't-floor'),
                 mail('work', 12, 'Rae Dunn <rae@vendor.example>', 'own1@acme.example', 'Wall panels', 'Panels ship Monday.', 1, 't-wall'))
        with self.own.store.connect() as db:
            graph.person_edit(db, 'email:kim@pal.example', {'side': 'personal'}, a.now())
        self.judge(self.own, ('work-9', 'client', 'Kim wrote'), ('work-11', 'client', 'Lee sent the floor quote'), ('work-12', 'client', 'Rae ships panels'))
        self.board(self.own, 'Gyms', 'team', {'Gym: Boulder': ['work-9', 'work-11'], 'Gym: Ridge': ['work-9'], 'Gym: Wall': ['work-12']})
        with self.own.store.connect() as db:
            sg.keep_private(db, 'email:rae@vendor.example')
        self.rounds()
        projects = self.projects_of(self.mem)
        self.assertEqual(sorted(projects), ['Gym: Boulder', 'Gym: Ridge'])  # Rae is kept private by hand: Wall stays home
        self.assertIn('Lee sent the floor quote', json.dumps(projects['Gym: Boulder']['timeline']))
        self.assertIsNone(projects['Gym: Ridge'].get('org'))  # Kim's own organization would say who they are
        received = json.dumps(self.team(self.mem) + self.team(self.mem, 'team_mail'))
        for text in ('Kim', 'pal.example', 'Climbing', 'Trip is booked', 'Rae', 'Panels'):
            self.assertNotIn(text, received)

    def test_internal_thread_is_never_shared_even_by_hand(self):
        self.olive_mail()
        with self.own.store.connect() as db:
            sg.set_hand(db, self.event_id(self.own, 'work-4'), 'team')
        self.rounds()
        self.assertNotIn(INTERNAL, json.dumps(self.team(self.mem, 'team_mail')))
        self.assertNotIn('Standup', json.dumps(self.team(self.mem, 'team_mail') + self.team(self.mem)))
        app = object.__new__(a.App); app.store, app.fleet, app.config = self.own.store, self.own, self.own.config
        with self.assertRaisesRegex(ValueError, 'Only colleagues'):
            app.graph_share_action('graph_share', {'event_id': self.event_id(self.own, 'work-4'), 'share': 'team'})
        with self.own.store.connect() as db:
            label = self.own.thread_labels(db, [dict(db.execute('SELECT * FROM events WHERE source_id=?', ('work-4',)).fetchone())])
        self.assertEqual(list(label.values())[0]['fixed'], True)

    def test_a_sensitive_thread_goes_nowhere_not_even_that_it_exists(self):
        self.olive_mail()
        self.rounds()
        held = [json.loads(r['body']) for r in self.team(self.mem, 'team_mail') if json.loads(r['body']).get('private')]
        self.assertEqual(held, [])  # not even that it exists
        self.assertNotIn('Private thread', json.dumps(self.team(self.mem)))
        received = json.dumps(self.team(self.mem) + self.team(self.mem, 'team_mail'))
        self.assertNotIn(HEALTH, received)
        self.assertNotIn('A personal note', received)
        self.assertNotIn('something private', received)  # the review's own line stays home too

    def test_override_by_hand_wins_both_ways(self):
        self.olive_mail()
        with self.own.store.connect() as db:
            sg.set_hand(db, self.event_id(self.own, 'work-3'), 'team')     # the review said sensitive; the owner shares it
            sg.set_hand(db, self.event_id(self.own, 'work-1'), 'private')  # the review said client; the owner keeps it
        self.rounds()
        threads = json.dumps(self.team(self.mem, 'team_mail'))
        self.assertIn(HEALTH, threads)
        self.assertNotIn(BODY, threads)
        # and a later review doesn't undo it
        self.judge(self.own, ('work-3', 'sensitive', 'Lee wrote'), ('work-1', 'client', 'Lee asked'))
        self.rounds()
        threads = json.dumps(self.team(self.mem, 'team_mail'))
        self.assertIn(HEALTH, threads)
        self.assertNotIn(BODY, threads)

    def test_a_later_review_never_turns_sensitive_into_client(self):
        self.olive_mail()
        self.judge(self.own, ('work-3', 'client', 'Lee wrote'))
        self.rounds()
        self.assertNotIn(HEALTH, json.dumps(self.team(self.mem, 'team_mail')))

    def test_keep_private_holds(self):
        self.olive_mail()
        self.rounds()
        self.assertTrue(self.team(self.mem))
        with self.own.store.connect() as db:
            sg.keep_private(db, 'org:client.example')
        self.rounds()
        self.assertEqual(self.team(self.mem), [])
        self.assertEqual(self.team(self.mem, 'team_mail'), [])

    def kickoff(self):
        """A client thread with Vera (kept private) in cc on its first message only; the reply quotes her."""
        self.add(self.own,
                 mail('work', 30, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Project kickoff', 'First message, with Vera on it.', 3, 't-mixed',
                      cc='vera@secret.example'),
                 mail('work', 31, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Re: Project kickoff', 'Vera said her budget is 90k.', 2, 't-mixed'))
        with self.own.store.connect() as db:
            sg.keep_private(db, 'email:vera@secret.example')
        self.judge(self.own, ('work-30', 'client', 'Lee kicked off the project'), ('work-31', 'client', 'Lee passed on the budget'))

    def labels(self, box):
        with box.store.connect() as db:
            rows = [dict(r) for r in db.execute('SELECT * FROM events')]
            found = box.thread_labels(db, rows)
            return {r['source_id']: found[r['id']] for r in rows if r['id'] in found}

    def test_someone_kept_private_on_one_message_keeps_the_whole_thread_also_what_arrives_later(self):
        self.olive_mail()
        self.kickoff()
        self.rounds()
        self.add(self.own, mail('work', 32, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Re: Project kickoff', 'One more thing about the 90k.', 0, 't-mixed'))
        self.judge(self.own, ('work-32', 'client', 'Lee added a detail'))
        self.rounds()
        for box in (self.adm, self.mem):
            got = self.received(box) + json.dumps(self.team(box))
            for text in ('90k', 'First message', 'Project kickoff', 'vera@secret.example', 'Lee passed on the budget', 'Lee added a detail'):
                self.assertNotIn(text, got)
            self.assertIn(BODY, got)  # the client's other thread, without her, goes as before
        labels = self.labels(self.own)
        for source in ('work-30', 'work-31', 'work-32'):
            self.assertEqual((labels[source]['share'], labels[source]['why']), ('only_you', 'Only you: kept private'))
        self.assertEqual(labels['work-1']['share'], 'team')
        with self.own.store.connect() as db:  # worked out once per scope, not once per message
            scope = sg.Scope(db, ['work'], {'acme.example'}, {'own1@acme.example'})
            reads, read = [], sg.Scope._read
            with patch.object(sg.Scope, '_read', lambda scope: reads.append(1) or read(scope)):  # with the automated threads, in one read
                views = {r['source_id']: sg.visibility(db, scope, {**dict(r), 'metadata': json.loads(r['metadata'])})
                         for r in db.execute("SELECT * FROM events WHERE account_id='work'")}
                self.assertEqual(sg.collect(db, scope.granted([], []), b'k' * 32, b's' * 32)[1].keys(), sg.collect(db, scope, b'k' * 32, b's' * 32)[1].keys())
            self.assertEqual(len(reads), 1)
            self.assertEqual({views[s] for s in ('work-30', 'work-31', 'work-32')}, {'private'})
            self.assertEqual(views['work-1'], 'team')
            sg.keep_private(db, 'email:vera@secret.example', False)  # no longer private: the thread goes like any other
            again = sg.Scope(db, ['work'], {'acme.example'}, {'own1@acme.example'})
            self.assertEqual(sg.visibility(db, again, {**dict(db.execute("SELECT * FROM events WHERE source_id='work-31'").fetchone()),
                                                       'metadata': {'from': 'lee@client.example', 'to': 'own1@acme.example', 'thread_id': 't-mixed'}}), 'team')

    def test_the_messages_read_for_someone_kept_private_give_what_reading_every_message_gives(self):
        """Only the messages they can be on are opened and checked (Scope._read). The same threads as opening every
        message, however they are on one: in cc on an old imported message, by Slack member id, in a Teams chat, as a
        guest of one meeting of a series, by link. On a sealed store SQLite sees none of cc, guests or kinds of chat."""
        self.olive_mail()
        self.kickoff()
        self.own.config['accounts'] += [{'id': 'sl', 'email': 'own1@acme.example', 'service': 'slack', 'boundary': 'work:Acme',
                                         'team_id': 'T0ACME0001', 'user_id': 'U0OLIVE001'},
                                        {'id': 'cal', 'email': 'own1@acme.example', 'service': 'calendar', 'boundary': 'work:Acme'}]
        meet = lambda n, who, series=None: {
            'account_id': 'cal', 'source_id': f'cal-{n}', 'kind': 'calendar.event', 'occurred_at': ago(1), 'title': 'Review', 'body': 'Agenda', 'deleted': False,
            'metadata': {'organizer': {'email': 'own1@acme.example'}, 'attendees': [{'email': who}], **({'recurring_event_id': series} if series else {})}}
        teams = lambda n, chat, who: {'account_id': 'tm', 'source_id': f'teams:{n}', 'kind': 'teams.message', 'occurred_at': ago(0, n), 'deleted': False,
                                      'title': 'Chat: hello', 'body': 'hello', 'metadata': {'chat_id': chat, 'chat_kind': 'oneOnOne', 'message_id': str(n),
                                                                                           'from': 'Olive Owner', 'from_me': True, 'to': [who]}}
        with self.own.store.connect() as db:
            # sealed where this class asks for it, and wherever the whole run is sealed (MESSAGE_PROTECTION_TEST)
            self.assertTrue(self.own.store.protected or not self.PROTECT)
            self.assertEqual(bool(db.execute("SELECT count(*) FROM events WHERE instr(metadata,'mc1_sealed')>0").fetchone()[0]), self.own.store.protected)
            db.executemany('INSERT OR REPLACE INTO identity_names(identifier,name,email,checked_at) VALUES(?,?,?,?)',
                           [('slack:U0VERA0001', 'Vera Stone', 'vera@secret.example', a.now()), ('slack:U0LEE00001', 'Lee Park', 'lee@client.example', a.now())])
        self.add(self.own,
                 mail('work', 40, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Old plan', 'From the import.', 300, 't-old', cc='Vera Stone <Vera@Secret.Example>'),
                 mail('work', 41, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Re: Old plan', 'A reply this week.', 1, 't-old'),
                 mail('work', 42, 'Zo\u00eb <zoe@client.example>', 'own1@acme.example', 'Lunch', 'Mentions vera@secret.example only in the text.', 1, 't-zoe'),
                 mail('work', 43, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Linked', 'About her, by link.', 1, 't-linked'),
                 self.slack(7, 'D0VERA0001', 'DM U0VERA0001', 'U0OLIVE001', 'Written to her'),
                 self.slack(8, 'D0VERA0001', 'DM U0VERA0001', 'U0VERA0001', 'Written by her'),
                 self.slack(9, 'C0TEAM0001', 'general', 'U0VERA0001', 'By her in a channel'),
                 self.lee_dm(10, 'Lee, without her'),
                 self.slack(11, 'D0VERA0002', 'DM U0VERA0001', 'U0OLIVE001', 'To her, in a chat she never wrote in'),
                 teams(1, '19:vera', 'vera@secret.example'), teams(2, '19:lee', 'lee@client.example'),
                 meet(1, 'vera@secret.example'), meet(2, 'lee@client.example'),
                 meet(3, 'vera@secret.example', 'weekly'), meet(4, 'lee@client.example', 'weekly'), meet(5, 'lee@client.example', 'monthly'))
        with self.own.store.connect() as db:
            db.execute("UPDATE events SET history=1 WHERE source_id='work-40'")
            db.execute('INSERT OR REPLACE INTO graph_events(node_id,event_id,at,probable) VALUES(?,?,?,0)',
                       ('email:vera@secret.example', self.event_id(self.own, 'work-43'), a.now()))
            row = lambda source: db.execute('SELECT * FROM events WHERE source_id=?', (source,)).fetchone()
            unit = lambda source: sg.unit_of(row(source)['kind'], json.loads(row(source)['metadata']), row(source)['id'])
            scope = lambda: sg.Scope(db, ['work', 'sl', 'cal', 'tm'], {'acme.example'}, {'own1@acme.example'})
            db.execute('DELETE FROM graph_events WHERE event_id=?', (row('D0VERA0002:11.000100')['id'],))  # as before the Graph linked it to her
            checked, mark = [], sg.Scope._mark
            with patch.object(sg.Scope, '_mark', lambda scope, e, *rest: checked.append(e['id']) or mark(scope, e, *rest)):
                narrow = scope().private_units
            full = scope()._private_full()
            # a direct message to her in a chat she never wrote in has her in a sealed part only: visibility reads it from
            # the message itself, as for every message it decides on
            alone = unit('D0VERA0002:11.000100')
            self.assertEqual(tuple(f - n for f, n in zip(full, narrow)), ({alone}, {alone}, set()))
            self.assertEqual(tuple(n - f for f, n in zip(full, narrow)), (set(), set(), set()))
            self.assertEqual(sg.visibility(db, scope(), {**dict(row('D0VERA0002:11.000100')), 'metadata': json.loads(row('D0VERA0002:11.000100')['metadata'])}), 'private')
            plain, items, linked = narrow
            for source in ('work-30', 'work-40', 'D0VERA0001:7.000100', 'D0VERA0001:8.000100', 'C0TEAM0001:9.000100', 'teams:1'):
                self.assertIn(unit(source), plain)
            self.assertEqual(unit('work-41'), unit('work-40'))  # the reply without her: the thread of the old message she is on
            self.assertEqual(unit('teams:1'), 'teams:19:vera')
            self.assertIn(unit('cal-1'), items - plain)
            self.assertEqual(unit('cal-4'), unit('cal-3'))  # the week she was not a guest: the series she is a guest of
            self.assertIn('cal:weekly', items - plain)
            self.assertIn(unit('work-43'), linked)
            for source in ('work-1', 'work-42', 'D0LEE00001:10.000100', 'cal-2', 'cal-5', 'teams:2'):
                self.assertNotIn(unit(source), plain | items)
            read = {r[0] for r in db.execute('SELECT source_id FROM events WHERE id IN (SELECT value FROM json_each(?))', (json.dumps(checked),))}
            self.assertFalse(read & {'work-1', 'cal-2', 'cal-5', 'D0LEE00001:10.000100', 'D0VERA0002:11.000100', 'teams:2'})
            # a page's lookup (labels) gives the same; a message that is its own thread is read by visibility itself
            asked = {unit(r[0]) for r in db.execute('SELECT source_id FROM events')}
            asked = {u for u in asked if not u.startswith('ev:')}
            self.assertEqual(tuple(part & asked for part in scope().private_among(asked, {'work', 'sl', 'cal', 'tm'})), tuple(part & asked for part in narrow))
            self.assertEqual(scope().private_among({'cal:monthly', unit('teams:2')}, {'tm'}), (set(), set(), set()))
            # a channel's and a chat's messages come from their own index, not from a pass over every message
            asks, looked = [], scope()
            real = looked._db

            class Watch:
                def execute(self, sql, args=()):
                    asks.append((sql, args))
                    return real.execute(sql, args)
            looked._db = Watch()
            looked.private_among({unit('C0TEAM0001:9.000100'), unit('teams:1')}, {'sl', 'tm'})
            plans = ' '.join(r[3] for sql, args in asks for r in db.execute('EXPLAIN QUERY PLAN ' + sql, args))
            self.assertIn('events_channel', plans)
            self.assertIn('events_chat', plans)
            sg.keep_private(db, 'org:client.example')  # a whole organization, by its domain
            narrow, full = scope().private_units, scope()._private_full()
            self.assertEqual(tuple(f - n for f, n in zip(full, narrow)), ({alone}, {alone}, set()))
            for source in ('work-1', 'D0LEE00001:10.000100', 'teams:2', 'cal-5'):
                self.assertIn(unit(source), narrow[1])
        labels = self.labels(self.own)
        self.assertEqual(labels['D0VERA0002:11.000100']['why'], 'Only you: kept private')

    def test_a_reply_that_went_before_is_taken_back_once_its_thread_has_someone_kept_private(self):
        """A Machine from before this rule shared the replies Vera wasn't on. After the update they leave the team's
        Machines by themselves, with what the records say of them."""
        self.kickoff()
        with patch.object(sg.Scope, 'private_on', return_value=False), patch.object(sg.Scope, 'private_linked', return_value=False):
            self.rounds()  # as it was: one message at a time
        for box in (self.adm, self.mem):
            self.assertIn('90k', self.received(box))
            self.assertNotIn('First message', self.received(box))
            self.assertIn('Lee Park', json.dumps(self.team(box)))
        self.rounds()
        for box in (self.adm, self.mem):
            self.assertEqual(self.team(box, 'team_mail'), [])
            self.assertEqual(self.team(box), [])
        with self.own.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM share_out WHERE kind IN ('thread','record')").fetchone()[0], 0)

    def lee_dm(self, n, text):
        return self.slack(n, 'D0LEE00001', 'DM U0LEE00001', 'U0LEE00001', text)

    def test_only_you_on_a_direct_message_holds_for_what_arrives_in_it_later(self):
        self.olive_mail()
        self.own.config['accounts'] += [{'id': 'sl', 'email': 'own1@acme.example', 'service': 'slack', 'boundary': 'work:Acme',
                                         'team_id': 'T0ACME0001', 'user_id': 'U0OLIVE001'}]
        with self.own.store.connect() as db:
            db.execute('INSERT OR REPLACE INTO identity_names(identifier,name,email,checked_at) VALUES(?,?,?,?)',
                       ('slack:U0LEE00001', 'Lee Park', 'lee@client.example', a.now()))
            db.execute('INSERT OR REPLACE INTO slack_members(user_id,outside,checked_at) VALUES(?,?,?)', ('U0LEE00001', 1, a.now()))
        self.add(self.own, self.lee_dm(4, 'Lee here: the renewal seats look right'))
        self.judge(self.own, ('D0LEE00001:4.000100', 'client', 'Lee confirmed the seats'))
        with self.own.store.connect() as db:
            sg.set_hand(db, self.event_id(self.own, 'D0LEE00001:4.000100'), 'private')
        self.add(self.own, self.lee_dm(5, 'Lee again: between us, we may cancel'))  # arrives after the choice
        self.board(self.own, 'Renewals', 'team', {'Renewal: Client': ['work-1', 'D0LEE00001:4.000100', 'D0LEE00001:5.000100']})
        self.judge(self.own, ('D0LEE00001:5.000100', 'client', 'Lee may cancel'))

        def views():
            with self.own.store.connect() as db:
                scope = sg.Scope(db, ['work', 'sl'], {'acme.example'}, {'own1@acme.example'})
                return {r['source_id'].split(':')[1][:1]: sg.visibility(db, scope, {**dict(r), 'metadata': json.loads(r['metadata'])})
                        for r in db.execute("SELECT * FROM events WHERE kind='slack.message'")}
        self.assertEqual(views(), {'4': 'private', '5': 'private'})
        self.assertEqual(self.labels(self.own)['D0LEE00001:5.000100']['why'], 'Only you: you chose this')
        self.rounds()
        for box in (self.adm, self.mem):
            self.assertNotIn('we may cancel', self.received(box) + json.dumps(self.team(box)))
            self.assertNotIn('Lee may cancel', json.dumps(self.team(box)))
        with self.own.store.connect() as db:
            shown = sg.overview(db, sg.Scope(db, ['work', 'sl'], {'acme.example'}, {'own1@acme.example'}))
            self.assertNotIn('cancel', json.dumps(shown['shared']))
            sg.set_hand(db, self.event_id(self.own, 'D0LEE00001:4.000100'), 'team')  # the owner's choice for all of it, both ways
        self.assertEqual(views(), {'4': 'team', '5': 'team'})
        self.add(self.own, self.lee_dm(6, 'Lee: one more'))
        self.assertEqual(views()['6'], 'pending')  # after Team nothing is held: the next one waits for the review, as before
        # A Teams one-on-one chat is one conversation too (a Teams message is its own thread); a group chat is not
        teams = lambda n, chat, kind: {'account_id': 'tm', 'source_id': f'teams:{n}', 'kind': 'teams.message', 'occurred_at': ago(0, n), 'deleted': False,
                                       'title': 'Lee: hello', 'body': 'hello', 'metadata': {'chat_id': chat, 'chat_kind': kind, 'message_id': str(n),
                                                                                           'from': 'Lee Park', 'to': ['lee@client.example']}}
        self.add(self.own, teams(1, '19:one', 'oneOnOne'), teams(2, '19:group', 'group'))
        with self.own.store.connect() as db:
            for n in (1, 2):
                sg.set_hand(db, self.event_id(self.own, f'teams:{n}'), 'private')
        self.add(self.own, teams(3, '19:one', 'oneOnOne'), teams(4, '19:group', 'group'))
        with self.own.store.connect() as db:
            scope = sg.Scope(db, ['work', 'tm'], {'acme.example'}, {'own1@acme.example'})
            hands = {r['source_id']: scope.hand(sg.thread_of(r['kind'], json.loads(r['metadata']), r['id']), r['kind'], json.loads(r['metadata']))
                     for r in db.execute("SELECT * FROM events WHERE kind='teams.message'")}
        self.assertEqual(hands, {'teams:1': 'private', 'teams:2': 'private', 'teams:3': 'private', 'teams:4': None})

    def taken_back_while(self, stop, start):
        """Sharing stops (stop), then the owner takes a thread back and new mail arrives: the thread and what the records
        say of it leave the team's Machines, and nothing new reaches them until sharing is back (start)."""
        self.olive_mail()
        self.add(self.own, mail('work', 40, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Seats', 'Ten more seats, please.', 2, 't-seats'))
        self.judge(self.own, ('work-40', 'client', 'Lee asked for more seats'))
        self.rounds()
        stop()
        lee = lambda box: next(json.loads(r['body']) for r in self.team(box) if r['kind'] == 'person')
        subjects = lambda box: {json.loads(r['body']).get('subject') for r in self.team(box, 'team_mail')}
        puts = lambda: [c[3]['blob'] for c in self.net.calls if c[0] == 'own1' and c[2] == '/graph' and c[3] and c[3].get('op') == 'put'
                        and c[3]['blob']['header']['kind'] in ('snapshot', 'delta', 'mail', 'file')]
        self.assertEqual({x['line'] for x in lee(self.mem)['timeline']}, {'Lee asked for the renewal quote', 'Lee asked for more seats'})
        self.add(self.own, mail('work', 41, 'Lee Park <lee@client.example>', 'own1@acme.example', 'After it stopped', 'Sent after sharing stopped.', 0, 't-after'),
                 mail('work', 42, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Re: Seats', 'Make it twelve seats.', 0, 't-seats'))
        self.judge(self.own, ('work-41', 'client', 'Lee wrote after it stopped'), ('work-42', 'client', 'Lee made it twelve'))
        before = len(puts())
        self.rounds()
        self.assertEqual(len(puts()), before)  # nothing taken back: nothing goes at all
        with self.own.store.connect() as db:
            sg.set_hand(db, self.event_id(self.own, 'work-1'), 'private')
        self.rounds()
        sent = puts()[before:]
        self.assertEqual(sorted((b['header']['kind'], bool(b['ct'])) for b in sent), [('delta', True), ('mail', False)])  # an empty blob for the thread, and less on the records
        for box in (self.adm, self.mem):
            self.assertEqual(subjects(box), {'Seats'})
            got = self.received(box) + json.dumps(self.team(box))
            for text in (BODY, 'Lee asked for the renewal quote', 'Sent after sharing stopped', 'Lee wrote after it stopped', 'twelve'):
                self.assertNotIn(text, got)
            self.assertEqual([x['line'] for x in lee(box)['timeline']], ['Lee asked for more seats'])
            self.assertEqual(len(lee(box)['threads']), 1)
        done = len(puts())
        self.rounds()
        self.assertEqual(len(puts()), done)  # once
        start()
        self.rounds()
        for box in (self.adm, self.mem):
            self.assertEqual(subjects(box), {'Seats', 'After it stopped'})
            self.assertIn('twelve', self.received(box))
            self.assertNotIn(BODY, self.received(box))
            self.assertEqual({x['line'] for x in lee(box)['timeline']}, {'Lee asked for more seats', 'Lee wrote after it stopped', 'Lee made it twelve'})

    def test_a_take_back_still_goes_while_this_machines_sharing_is_off_and_nothing_new_does(self):
        def stop():
            self.own.graph_optout(FLEET, True)
            self.rounds()
            self.ok(self.adm, 'optout', 'Olive')
            self.rounds()
            self.assertEqual(self.own.sharing()[0]['off'], 'off')
        self.taken_back_while(stop, lambda: self.own.graph_optout(FLEET, False))

    def test_a_take_back_still_goes_while_the_fleets_sharing_is_paused_and_nothing_new_does(self):
        def stop():
            self.adm.graph_pause(FLEET, True)
            self.rounds()
            self.assertTrue(self.own.sharing()[0]['paused'])
        self.taken_back_while(stop, lambda: self.adm.graph_pause(FLEET, False))

    def test_the_sharing_rules_are_kept_between_requests_until_one_of_their_tables_changes(self):
        """A person's page and the to-do list ask for the sharing rules on every request: worked out once (a pass over
        every person and organization) and kept, but a Keep private takes effect on the very next label."""
        self.olive_mail()
        self.rounds()
        made = []
        real = sg.Scope.__init__

        def counted(scope, *args, **kwargs):
            made.append(1)
            real(scope, *args, **kwargs)
        with patch.object(sg.Scope, '__init__', counted), self.own.store.connect() as db:
            rows = [dict(r) for r in db.execute("SELECT * FROM events WHERE account_id='work'")]
            first = self.own.thread_labels(db, rows)
            self.assertEqual(self.own.thread_labels(db, rows), first)
            self.assertEqual(len(made), 1)  # the second request reused the first one's rules
            self.assertIn('team', {x['share'] for x in first.values()})
            sg.keep_private(db, 'org:client.example')
            db.commit()
            after = self.own.thread_labels(db, rows)
        self.assertEqual(len(made), 2)  # worked out again after the change
        self.assertNotIn('team', {x['share'] for x in after.values()})

    def board(self, box, name, visibility, projects, stage='Talks'):
        with box.store.connect() as db:
            for project, sources in projects.items():
                graph.label(db, [self.event_id(box, x) for x in sources], project, 'review', a.now())
            graph.save_board(db, {'name': name, 'stages': [stage, 'Signed'], 'about': name, 'visibility': visibility,
                                  'projects': list(projects)}, a.now())
            board = db.execute('SELECT id FROM boards WHERE name=?', (name,)).fetchone()[0]
        with box.store.connect() as db:
            db.isolation_level = None
            graph.build(db, box.config, a.now())
        return board

    def projects_of(self, box):
        return {json.loads(r['body'])['name']: json.loads(r['body']) for r in self.team(box) if r['kind'] == 'project'}

    def test_team_project_summaries_do_not_repeat_withheld_signal_text(self):
        self.olive_mail()
        self.board(self.own, 'Renewals', 'team', {'Renewal: Lee': ['work-1', 'work-3', 'work-4']})
        for index, source in enumerate(('work-3', 'work-4')):
            with self.subTest(source=source):
                with self.own.store.connect() as db:
                    eid = self.event_id(self.own, source)
                    db.execute('UPDATE events SET occurred_at=? WHERE id=?', (ago(0, 2-index), eid))
                    graph.set_stage(db, 'project:1', 'Signed' if index == 0 else 'Talks', 'review', a.now(),
                                    reason='Withheld project reason', event_id=eid, next_step='Withheld project next step')
                self.rounds()
                record = self.projects_of(self.mem)['Renewal: Lee']
                self.assertIsNone(record['why'])
                self.assertIsNone(record['next'])
                self.assertNotIn('Withheld project', json.dumps(self.team(self.mem)))

    def test_same_stage_next_step_uses_its_own_sharing_provenance(self):
        self.olive_mail()
        self.board(self.own, 'Renewals', 'team', {'Renewal: Lee': ['work-1', 'work-3']})
        with self.own.store.connect() as db:
            graph.set_stage(db, 'project:1', 'Signed', 'review', a.now(), reason='Client signed',
                            event_id=self.event_id(self.own, 'work-1'), next_step='Send the client a welcome')
        self.rounds()
        self.assertEqual(self.projects_of(self.mem)['Renewal: Lee']['next'], 'Send the client a welcome')
        with self.own.store.connect() as db:
            graph.set_stage(db, 'project:1', 'Signed', 'review', a.now(), reason='Private health update',
                            event_id=self.event_id(self.own, 'work-3'), next_step='Private follow-up for surgery')
        self.rounds()
        record = self.projects_of(self.mem)['Renewal: Lee']
        self.assertEqual(record['why'], 'Client signed')
        self.assertIsNone(record['next'])
        self.assertNotIn('Private follow-up', json.dumps(self.team(self.mem)))

    def test_explicit_board_sharing_still_includes_its_authorized_sensitive_summary(self):
        self.olive_mail()
        board = self.board(self.own, 'Renewals', 'only_you', {'Renewal: Lee': ['work-1', 'work-3']})
        with self.own.store.connect() as db:
            graph.set_stage(db, 'project:1', 'Signed', 'review', a.now(), reason='Explicit sensitive reason',
                            event_id=self.event_id(self.own, 'work-3'), next_step='Explicit sensitive next step')
        self.own.graph_board_share(board, [{'fleet': FLEET, 'member': 'mem3'}])
        self.rounds()
        record = self.projects_of(self.mem)['Renewal: Lee']
        self.assertEqual(record['why'], 'Explicit sensitive reason')
        self.assertEqual(record['next'], 'Explicit sensitive next step')
        self.assertNotIn('Renewal: Lee', self.projects_of(self.adm))

    def test_an_only_you_board_its_projects_and_their_threads_never_reach_the_team_and_switching_retracts_them(self):
        self.olive_mail()
        board = self.board(self.own, 'Renewals', 'team', {'Renewal: Lee': ['work-1', 'work-2']})
        self.rounds()
        self.assertEqual(self.projects_of(self.mem)['Renewal: Lee']['board'], 'Renewals')
        self.assertIn('Renewal quote', [json.loads(r['body']).get('subject') for r in self.team(self.mem, 'team_mail')])
        with self.own.store.connect() as db:
            self.assertTrue(graph.visible_to_team(db, 'project:1'))
            graph.save_board(db, {'board_id': board, 'name': 'Renewals', 'stages': ['Talks', 'Signed'], 'about': 'Renewals', 'visibility': 'only_you'}, a.now())
            self.assertFalse(graph.visible_to_team(db, 'project:1'))
            self.assertEqual(graph.hidden_project_ids(db), {1})
        self.rounds()
        self.assertEqual(self.projects_of(self.mem), {})
        self.assertNotIn('Renewal quote', [json.loads(r['body']).get('subject') for r in self.team(self.mem, 'team_mail')])
        self.assertNotIn('Lee Park', [json.loads(r['body'])['name'] for r in self.team(self.mem) if r['kind'] == 'person'])
        # The project's own setting wins over its board's, both ways
        with self.own.store.connect() as db:
            graph.set_project_visibility(db, 'project:1', 'team')
            self.assertEqual(graph.hidden_project_ids(db), set())
            graph.set_project_visibility(db, 'project:1', None)
            self.assertEqual(graph.hidden_project_ids(db), {1})
            with self.assertRaises(ValueError):
                graph.set_project_visibility(db, 'project:1', 'everyone')
        with self.own.store.connect() as db:
            view = self.own.team_overview(db, {})
            self.assertEqual([b['name'] for b in view['boards']], [])

    def test_a_teammates_board_tile_says_what_happened_and_whether_it_is_yours(self):
        """On a teammate's Machine a shared board's tile carries its newest shared line (not only its owner's name), and
        Mine / Needs me: on a thread of it, or an open to-do about it. Nothing more is shared for it."""
        self.olive_mail()
        self.add(self.own, mail('work', 8, 'Kim Lo <kim@buyer.example>', 'own1@acme.example', 'Pilot terms', 'Can we start the pilot Monday?', 1, 't-pilot',
                                cc='mem3@acme.example'))
        self.judge(self.own, ('work-8', 'client', 'Kim asked to start the pilot Monday'))
        self.board(self.own, 'Renewals', 'team', {'Renewal: Lee': ['work-1'], 'Hire: Ada': ['work-4'], 'Pilot: Kim': ['work-8']})
        self.rounds()
        sent = json.dumps(self.team(self.mem))
        with self.mem.store.connect() as db:
            board = next(b for b in self.mem.team_overview(db, {})['boards'] if b['name'] == 'Renewals')
        tiles = {p['name']: p for p in board['projects']}
        self.assertEqual(tiles['Renewal: Lee']['line'], 'Lee asked for the renewal quote')
        self.assertTrue(tiles['Renewal: Lee']['line_at'])
        self.assertNotIn('line', tiles['Hire: Ada'])  # nothing of it was shared: its stage and date say what happened
        self.assertEqual((tiles['Renewal: Lee']['yours'], tiles['Renewal: Lee']['needs_you']), (False, False))
        self.assertEqual((tiles['Pilot: Kim']['yours'], tiles['Pilot: Kim']['needs_you']), (True, True))  # cc'd, and Kim wrote last
        with self.mem.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at,project) VALUES('c1','c1','Call Lee','',"
                       "'[]','[]','pending',?,'Renewal: Lee')", (a.now(),))
        with self.mem.store.connect() as db:
            view = self.mem.team_overview(db, {})
            tiles = {p['name']: p for b in view['boards'] for p in b['projects']}
        self.assertEqual((tiles['Renewal: Lee']['yours'], tiles['Renewal: Lee']['needs_you']), (True, True))
        # The team's list says the same (Mine / Needs me / All on the List as on the Board), and a tile has a state
        listed = {p['name']: p for p in view['projects']}
        for name in ('Renewal: Lee', 'Pilot: Kim', 'Hire: Ada'):
            self.assertEqual((listed[name]['yours'], listed[name]['needs_you']), (tiles[name]['yours'], tiles[name]['needs_you']), name)
            self.assertEqual(tiles[name]['state'], 'active')
        self.assertEqual(json.dumps(self.team(self.mem)), sent)  # what was shared stays as it was

    def test_a_teammates_board_tile_and_organization_show_its_logo(self):
        """A teammate's tile and organization show the logo the sharing Machine shows: a LinkedIn company logo goes with
        the record, any other address never does."""
        logo = 'https://media.licdn.com/dms/image/v2/C4D0BAQ/company-logo_200_200/0/1/client_logo?e=2147483647&v=beta&t=Ab_c-1'
        self.olive_mail()
        with self.own.store.connect() as db:
            db.execute("INSERT OR REPLACE INTO org_profiles(domain,status,profile,fetched_at) VALUES('client.example','found',?,?)",
                       (json.dumps({'name': 'Client Co', 'logo': logo}), a.now()))
        self.board(self.own, 'Renewals', 'team', {'Renewal: Lee': ['work-1']})
        with self.own.store.connect() as db:
            db.execute("UPDATE projects SET org='client.example' WHERE name='Renewal: Lee'")
        self.rounds()
        self.assertEqual(self.projects_of(self.mem)['Renewal: Lee']['org']['logo'], logo)
        with self.mem.store.connect() as db:
            view = self.mem.team_overview(db, {})
        tile = next(p for b in view['boards'] for p in b['projects'] if p['name'] == 'Renewal: Lee')
        self.assertEqual(tile['org']['logo'], logo)
        self.assertEqual(next(o for o in view['orgs'] if o.get('team_only'))['profile']['logo'], logo)
        # Only a LinkedIn company logo: a teammate's Machine never loads another address a teammate sent
        for bad in ('https://track.example/p.png', 'http://media.licdn.com/dms/image/x', 'https://media.licdn.com.evil.example/dms/image/x',
                    'https://static.licdn.com/aero-v1/sc/h/ghost', 'https://media.licdn.com/dms/image/x"onerror="y'):
            self.assertIsNone(sg.team_logo(bad), bad)
            cleaned = sg._clean_record({'r': 'a' * 32, 't': 'project', 'name': 'P', 'org': {'name': 'Client Co', 'd': 'b' * 32, 'logo': bad}})
            self.assertNotIn('logo', cleaned['org'])
            self.assertNotIn('logo', sg._clean_record({'r': 'a' * 32, 't': 'org', 'name': 'Client Co', 'd': ['b' * 32], 'logo': bad}))

    def test_a_board_says_whose_it_is_and_who_sees_it_and_its_owner_sees_what_stays_with_them(self):
        """A teammate's board says whose it is and whether the whole team has it or it was shared with them by name; the
        owner's says which of its projects never went (kept private here), so a teammate's board having fewer is no riddle."""
        deals = self.deal_board()
        self.board(self.own, 'Renewals', 'team', {'Renewal: Lee': ['work-1'], 'Hire: Ada': ['work-4']})
        with self.own.store.connect() as db:
            renewals = db.execute("SELECT id FROM boards WHERE name='Renewals'").fetchone()[0]
            kept = db.execute("SELECT id FROM projects WHERE name='Hire: Ada'").fetchone()[0]
            sg.keep_private(db, 'project:%d' % kept)
            self.assertIsNone(self.own.projects_went(db, ['project:%d' % kept]))  # nothing went yet: no project stays back
        self.own.graph_board_share(deals, [{'fleet': FLEET, 'member': 'mem3'}])
        self.rounds()
        with self.mem.store.connect() as db:
            boards = {b['name']: b for b in self.mem.team_overview(db, {})['boards']}
        self.assertEqual((boards['Renewals']['by'], boards['Renewals']['seen']), (['Olive'], 'team'))
        self.assertEqual((boards['Acquisition conversations']['by'], boards['Acquisition conversations']['seen']), (['Olive'], 'people'))
        self.assertNotIn('Hire: Ada', [p['name'] for p in boards['Renewals']['projects']])
        with self.mem.store.connect() as db:  # its organization links to the page this Machine has of it
            lee = next(p for p in boards['Renewals']['projects'] if p['name'] == 'Renewal: Lee')
            detail = self.mem.team_detail(db, lee['id'])
            self.assertEqual(detail['org_name'], 'Client')
            self.assertEqual(self.mem.team_detail(db, detail['org'])['name'], 'Client')
        with self.adm.store.connect() as db:
            self.assertNotIn('Acquisition conversations', [b['name'] for b in self.adm.team_overview(db, {})['boards']])  # Ada isn't on it
        with self.own.store.connect() as db:
            nodes = ['project:' + str(r[0]) for r in db.execute('SELECT id FROM projects WHERE board_id IN (?,?)', (renewals, deals))]
            went = self.own.projects_went(db, nodes)
        self.assertEqual(set(nodes) - went, {'project:%d' % kept})  # the deal went to Mo by name; Ada's hire stays with Olive

    def site_logo(self, box, domain, data):
        """A logo saved from an organization's own site (enrichment.site_logos_step), then the Graph built again."""
        with box.store.connect() as db:
            db.execute('INSERT OR REPLACE INTO person_photos(identifier,key,type,data,saved_at) VALUES(?,?,?,?,?)',
                       ('logo:' + domain, a.enrichment.photo_key('logo:' + domain), 'image/png', data, a.now()))
        self.add(box)

    def test_a_logo_from_an_organizations_own_site_goes_as_a_small_picture_once_and_again_only_when_it_changes(self):
        """A teammate sees the organization's own site's logo: a new PNG of its pixels only, at most 64 pixels, with
        the organization's record; never the site's address. It goes once, not in each round or daily snapshot, and
        again when it changes. The receiving Machine shows it from its own address."""
        import logo_image
        from test_logo_image import chunk, png
        self.olive_mail()
        source = png(160, 160, extra=chunk(b'tEXt', b'Source\x00https://www.client.example/apple-touch-icon.png'))
        self.site_logo(self.own, 'client.example', source)
        self.board(self.own, 'Renewals', 'team', {'Renewal: Lee': ['work-1']})
        with self.own.store.connect() as db:
            db.execute("UPDATE projects SET org='client.example' WHERE name='Renewal: Lee'")
        bodies = []
        put = self.own._put
        spy = lambda group, me, kind, body, to, **kw: (bodies.append((kind, json.dumps(body))), put(group, me, kind, body, to, **kw))[1]
        with patch.object(self.own, '_put', side_effect=spy):
            self.rounds(3)
            with_picture = [b for k, b in bodies if '"logo_img"' in b]
            self.assertEqual(len(with_picture), 1, 'once, not each round')
            records = ''.join(b for k, b in bodies if k in ('snapshot', 'delta'))
            self.assertNotIn('client.example', records)  # neither the site's address nor its domain (a shared thread's mail has its own)
            self.assertNotIn('apple-touch-icon', records)
            org = next(r for k, b in bodies if k in ('snapshot', 'delta') for r in json.loads(b)['records'] if r.get('logo_img'))
            self.assertLessEqual(len(org['logo_img']), logo_image.MAX_BYTES * 4 // 3 + 4)
            self.assertEqual(org['t'], 'org')
            # the daily snapshot: the record again, its picture not
            state = self.own.meta('graph_out:' + FLEET)
            self.own.set_meta('graph_out:' + FLEET, {**state, 'snapshot_at': 0})
            went = len(bodies)
            self.rounds()
            self.assertIn('snapshot', [k for k, _ in bodies[went:]])
            self.assertEqual(len([b for k, b in bodies if '"logo_img"' in b]), 1)
        with self.mem.store.connect() as db:
            view = self.mem.team_overview(db, {})
            tile = next(p for b in view['boards'] for p in b['projects'] if p['name'] == 'Renewal: Lee')
            logo = tile['org']['logo']
            self.assertRegex(logo, r'^api/person-photo\?p=[0-9a-f]{32}$')
            self.assertEqual(next(o for o in view['orgs'] if o.get('team_only'))['profile']['logo'], logo)
            served, kind = sgl.photo(db, logo[-32:])
        self.assertEqual(kind, 'image/png')
        self.assertEqual(logo_image.decode_png(served, max_side=64, strict=True)[:2], (64, 64))
        self.assertNotIn(b'client.example', served)
        # a new logo on the site: the picture goes again, once
        bodies.clear()
        self.site_logo(self.own, 'client.example', png(48, 48, rgba=bytes((10, 20, 30, 255)) * 48 * 48))
        with patch.object(self.own, '_put', side_effect=spy):
            self.rounds(3)
        self.assertEqual(len([b for k, b in bodies if '"logo_img"' in b]), 1)
        with self.mem.store.connect() as db:
            view = self.mem.team_overview(db, {})
            logo = next(o for o in view['orgs'] if o.get('team_only'))['profile']['logo']
            self.assertEqual(logo_image.decode_png(sgl.photo(db, logo[-32:])[0], strict=True)[:3],
                             (48, 48, bytes((10, 20, 30, 255)) * 48 * 48))
        # the Machine that knows the organization itself shows its own logo first
        own_logo = 'https://media.licdn.com/dms/image/v2/C4D/company-logo_200_200/0/1/own?e=1&v=beta&t=x'
        self.add(self.mem, mail('work', 9, 'Lee Park <lee@client.example>', 'mem3@acme.example', 'Hello', 'Hi Mo', 1, 't-mo'))
        with self.mem.store.connect() as db:
            db.execute("INSERT OR REPLACE INTO org_profiles(domain,status,profile,fetched_at) VALUES('client.example','found',?,?)",
                       (json.dumps({'name': 'Client Co', 'logo': own_logo}), a.now()))
        self.add(self.mem)
        with self.mem.store.connect() as db:
            view = self.mem.team_overview(db, {})
        self.assertEqual(next(p for b in view['boards'] for p in b['projects'] if p['name'] == 'Renewal: Lee')['org']['logo'], own_logo)

    def test_a_teammates_logo_picture_is_checked_and_drawn_again_and_a_picture_the_owner_set_never_goes(self):
        import logo_image
        from test_logo_image import chunk, png
        good = logo_image.thumbnail(png(64, 64), 'image/png')
        record = lambda img: sg._clean_record({'r': 'a' * 32, 't': 'org', 'name': 'Client Co', 'd': ['b' * 32], 'logo_h': 'c' * 32, 'logo_img': img})
        cleaned = record(nc.b64(good))
        self.assertEqual(logo_image.decode_png(nc.unb64(cleaned['logo_img']), strict=True), logo_image.decode_png(good, strict=True))
        self.assertRegex(cleaned['logo_key'], '^[0-9a-f]{32}$')
        svg = b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>'
        for why, img in {'oversized': nc.b64(good + b'\x00' * 9000), 'svg with script': nc.b64(svg), 'polyglot': nc.b64(good + b'<script>alert(1)</script>'),
                         'jpeg': nc.b64(b'\xff\xd8\xff\xe0' + b'\x00' * 100), 'too big': nc.b64(png(200, 200)),
                         'text chunk': nc.b64(png(8, 8, extra=chunk(b'tEXt', b'a\x00b'))), 'not base64': '<img src=x onerror=alert(1)>', 'not text': 5}.items():
            cleaned = record(img)
            self.assertNotIn('logo_img', cleaned, why)
            self.assertNotIn('logo_key', cleaned, why)
        self.assertNotIn('logo_h', sg._clean_record({'r': 'a' * 32, 't': 'org', 'name': 'C', 'd': [], 'logo_h': 'x"><script>'}))
        # Only a logo saved from the organization's own site: a picture the owner set is never read for it
        with self.own.store.connect() as db:
            db.execute("INSERT INTO person_photos(identifier,key,type,data,saved_at) VALUES('pic:x',?,'image/png',?,?)", ('d' * 32, png(8, 8), a.now()))
            self.assertIsNone(sgl.site_logo_thumb(db, 'api/person-photo?p=' + 'd' * 32))
            self.assertIsNone(sgl.site_logo_thumb(db, 'https://client.example/logo.png'))

    def test_a_project_on_a_team_board_goes_with_its_board_record_before_any_thread_of_it_is_shared(self):
        self.olive_mail()
        self.board(self.own, 'Hiring', 'team', {'Hire: Ada': ['work-4']}, stage='Screening')  # only colleagues on it
        self.rounds()
        project = self.projects_of(self.mem)['Hire: Ada']
        self.assertEqual((project['board'], project['stage'], project['timeline'], project['threads']), ('Hiring', 'Screening', [], []))
        self.assertNotIn('Standup', [json.loads(r['body']).get('subject') for r in self.team(self.mem, 'team_mail')])

    def test_the_first_share_goes_an_hour_after_the_owner_is_told_with_no_start_now(self):
        told = []
        self.own.tell = lambda text, anchor: told.append((text, anchor))
        for box in (self.adm, self.mem):
            box.set_meta('graph_start:' + FLEET, {'shown': a.now(), 'started': a.now()})
        self.own.set_meta('graph_start:' + FLEET, None)  # Olive's Machine, about to share with the team for the first time
        self.olive_mail()
        self.rounds()
        self.assertEqual(self.team(self.mem, 'team_mail'), [])  # the hour to look it over first
        self.assertEqual(told, [('Your Work goes to Acme within the hour. Look it over and keep anything private first.', 'shared-' + FLEET)])
        self.rounds()
        self.assertEqual(len(told), 1)  # told once: nothing to answer
        self.assertFalse(self.own.sharing()[0]['started'])
        people = {p['name']: p['state'] for p in self.adm.sharing()[0]['people']}  # an admin sees who hasn't shared yet
        self.assertEqual(people['Olive'], 'not_started')
        with self.own.store.connect() as db:
            sg.ensure(db)
        view = self.own.graph_overview(FLEET)
        self.assertEqual(view['preview']['threads'], 1)
        self.assertEqual(view['preview']['orgs'][0]['key'], '@client.example')
        self.assertTrue(all(x['why'].startswith('Goes within the hour') for x in view['threads']))
        start = self.own.meta('graph_start:' + FLEET)
        start['look'] = ago(0, 2)  # the hour went by, nobody tapped anything
        self.own.set_meta('graph_start:' + FLEET, start)
        self.rounds()
        self.assertIn(BODY, json.dumps(self.team(self.mem, 'team_mail')))
        self.assertTrue(self.own.sharing()[0]['started'])
        self.assertEqual({p['name']: p['state'] for p in self.adm.sharing()[0]['people']}['Olive'], 'sharing')
        self.assertEqual(len(told), 1)

    def test_the_first_share_skips_the_hour_on_start_now_and_an_updated_machine_gets_its_hour_too(self):
        for box in (self.adm, self.mem):
            box.set_meta('graph_start:' + FLEET, {'shown': a.now(), 'started': a.now()})
        self.own.set_meta('graph_start:' + FLEET, {'shown': ago(9)})  # waited for Start now before this version
        self.olive_mail()
        self.rounds()
        self.assertEqual(self.team(self.mem, 'team_mail'), [])  # an hour from now, not at once
        self.own.graph_start(FLEET)
        self.rounds()
        self.assertIn(BODY, json.dumps(self.team(self.mem, 'team_mail')))

    def test_the_first_share_keeps_what_its_owner_keeps_private_in_the_hour(self):
        for box in (self.adm, self.mem):
            box.set_meta('graph_start:' + FLEET, {'shown': a.now(), 'started': a.now()})
        self.olive_mail()
        self.rounds()
        self.own.graph_rule('@client.example', 'private', 'Client')
        start = self.own.meta('graph_start:' + FLEET)
        start['look'] = ago(0, 2)
        self.own.set_meta('graph_start:' + FLEET, start)
        self.rounds()
        self.assertTrue(self.own.sharing()[0]['started'])
        self.assertNotIn(BODY, json.dumps(self.team(self.mem, 'team_mail')))

    # -- all the Work history, a batch at a time
    def client_threads(self, box, n, days):
        self.add(box, *[mail('work', 100 + i, 'Lee Park <lee@client.example>', box.email, f'Order {i}', f'Order number {i}', days + i, f't-order-{i}')
                        for i in range(n)])
        self.judge(box, *[(f'work-{100 + i}', 'client', f'Lee placed order {i}') for i in range(n)])

    def mail_puts(self, box, kind='mail'):
        return [c[3]['blob']['header'] for c in self.net.calls
                if c[0] == box.member_id and c[2] == '/graph' and c[3] and c[3].get('op') == 'put' and c[3]['blob']['header']['kind'] == kind]

    def test_history_goes_as_far_back_as_the_machine_has_it(self):
        self.client_threads(self.own, 2, 500)  # well past a year
        self.rounds()
        subjects = {json.loads(r['body']).get('subject') for r in self.team(self.mem, 'team_mail')}
        self.assertEqual(subjects, {'Order 0', 'Order 1'})

    def test_the_backfill_is_batched_newest_first_and_resumes_where_it_stopped(self):
        self.client_threads(self.own, 6, 10)
        hour = sg.PER_HOUR
        sg.PER_HOUR = 4; self.addCleanup(setattr, sg, 'PER_HOUR', hour)
        self.own.set_meta('graph_puts', [])
        self.own.graph_round(force=True)  # the snapshot and three threads
        for box in (self.adm, self.mem):
            box.graph_round(force=True)
        first = sorted(json.loads(r['body'])['subject'] for r in self.team(self.mem, 'team_mail'))
        self.assertEqual(first, ['Order 0', 'Order 1', 'Order 2'])  # the newest
        self.own.graph_round(force=True)
        self.assertEqual(len(self.mail_puts(self.own)), 3)  # the budget is spent: nothing more this hour
        self.own.set_meta('graph_puts', [])  # an hour later
        self.rounds()
        self.assertEqual(len({json.loads(r['body'])['subject'] for r in self.team(self.mem, 'team_mail')}), 6)
        tags = [h['tag'] for h in self.mail_puts(self.own)]
        self.assertEqual(len(tags), len(set(tags)))  # each thread went once

    def test_the_history_pass_judges_old_threads_through_the_same_labels(self):
        self.add(self.own, mail('work', 7, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Old order', BODY, 300, 't-old'),
                 mail('work', 8, 'Ada <adm2@acme.example>', 'own1@acme.example', 'Old standup', INTERNAL, 300, 't-old-standup'))
        waiting = self.own.graph_unjudged()
        self.assertEqual([t['subject'] for t in waiting], ['Old order'])  # colleagues only: never asked about, never shared
        run = 'r' * 32
        with self.own.store.connect() as db:
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind,auto) VALUES(?,'running',?,?,?,'share',1)",
                       (run, a.now(), a.now(), json.dumps({'threads': waiting, 'page_size': 20})))
        self.assertEqual(self.own.store.profile_evidence(1, a.PROFILE_SESSION_PREFIX + run)['threads'][0]['subject'], 'Old order')
        with self.assertRaises(ValueError):  # only threads this pass was given
            self.own.store.save_profile({'team': [{'event_id': self.event_id(self.own, 'work-8'), 'share': 'client', 'line': 'x'}]}, a.PROFILE_SESSION_PREFIX + run)
        self.own.store.save_profile({'team': [{'event_id': waiting[0]['event_id'], 'share': 'client', 'line': 'Lee placed an old order'}]},
                                    a.PROFILE_SESSION_PREFIX + run)
        self.assertEqual(self.own.graph_unjudged(), [])
        self.rounds()
        self.assertIn('Old order', {json.loads(r['body']).get('subject') for r in self.team(self.mem, 'team_mail')})

    # -- attachments go with a whole client thread
    def files(self, box, big=False):
        asked = []
        def fetch(event_id, part=None):
            asked.append((event_id, part))
            if part is None:
                return [{'id': 'p1', 'name': 'quote.pdf', 'mime': 'application/pdf', 'size': 9, 'kind': 'file'},
                        {'id': 'p2', 'name': 'logo.png', 'mime': 'image/png', 'size': 10, 'kind': 'file', 'inline': True},
                        {'id': 'p3', 'name': 'all-hands.mp4', 'mime': 'video/mp4', 'size': sg.MAX_FILE + 1, 'kind': 'file'}]
            return b'%PDF-1.4 ' if part == 'p1' else b'x' * (sg.MAX_FILE + 1)
        box.mail_files = fetch
        return asked

    def test_attachments_go_with_a_shared_client_thread_sealed_and_never_with_a_sensitive_one(self):
        self.olive_mail()
        asked = self.files(self.own)
        self.rounds()
        renewal, health = self.event_id(self.own, 'work-1'), self.event_id(self.own, 'work-3')
        self.assertNotIn(health, [e for e, _ in asked])  # a sensitive thread: no files, not even looked up
        self.assertNotIn('p3', [p for _, p in asked])  # too large: not even read
        with self.mem.store.connect() as db:
            rows = db.execute('SELECT fleet,member,tag,body FROM team_mail').fetchall()
            tid = next(f"{r['fleet']}:{r['member']}:{r['tag']}" for r in rows if not json.loads(r['body']).get('private'))
            thread = self.mem.team_thread(db, tid)
            listed = thread['messages'][0]['attachments']
            self.assertEqual([(x['name'], bool(x.get('file')), bool(x.get('too_large'))) for x in listed],
                             [('quote.pdf', True, False), ('all-hands.mp4', False, True)])
            self.assertEqual(self.mem.team_file(db, tid, listed[0]['file']), (b'%PDF-1.4 ', 'application/pdf', 'quote.pdf'))
            with self.assertRaises(ValueError):
                self.mem.team_file(db, tid, 'f' * 32)
        self.assertNotIn(nc.b64(b'%PDF-1.4 '), json.dumps(self.net.blobs))  # the Network had it sealed only
        self.assertNotIn('quote.pdf', json.dumps(self.net.blobs))
        files = len(self.mail_puts(self.own, 'file'))
        self.assertEqual(files, 2)  # one per message that has it
        self.rounds()
        self.assertEqual(len(self.mail_puts(self.own, 'file')), files)  # once, not every round

    def test_a_careful_fleet_shares_client_threads_without_their_attachments(self):
        self.net.level = 'careful'  # the Fleet's security level (security_levels.py)
        self.olive_mail()
        asked = self.files(self.own)
        self.rounds()
        self.assertFalse([p for _, p in asked if p])  # no attachment is even read
        self.assertEqual(self.mail_puts(self.own, 'file'), [])
        with self.mem.store.connect() as db:
            rows = db.execute('SELECT fleet,member,tag,body FROM team_mail').fetchall()
            tid = next(f"{r['fleet']}:{r['member']}:{r['tag']}" for r in rows if not json.loads(r['body']).get('private'))
            listed = self.mem.team_thread(db, tid)['messages'][0]['attachments']
        self.assertEqual([(x['name'], bool(x.get('file')), bool(x.get('not_shared'))) for x in listed],
                         [('quote.pdf', False, True), ('all-hands.mp4', False, True)])

    # -- stopping takes an admin's OK, like in any CRM
    def test_stopping_needs_an_admins_ok_and_what_went_before_stays(self):
        self.olive_mail()
        self.rounds()
        self.assertEqual(self.own.graph_optout(FLEET, True)['off'], 'asked')
        self.add(self.own, mail('work', 20, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Asked meanwhile', BODY, 0, 't-meanwhile'))
        self.judge(self.own, ('work-20', 'client', 'Lee wrote again'))
        self.rounds()
        subjects = lambda: {json.loads(r['body']).get('subject') for r in self.team(self.mem, 'team_mail')}
        self.assertIn('Asked meanwhile', subjects())  # still on until an admin agrees
        self.assertFalse([p for p in self.own._prompts() if p['kind'] == 'optout'])  # nobody approves their own
        self.assertFalse([p for p in self.mem._prompts() if p['kind'] == 'optout'])  # not an admin
        self.assertEqual(self.ok(self.adm, 'optout', 'Olive'), {'ok': True, 'done': True})
        self.rounds()
        self.assertEqual(self.own.sharing()[0]['off'], 'off')
        self.add(self.own, mail('work', 21, 'Lee Park <lee@client.example>', 'own1@acme.example', 'After the OK', BODY, 0, 't-after'))
        self.judge(self.own, ('work-21', 'client', 'Lee wrote after'))
        self.rounds()
        self.assertNotIn('After the OK', subjects())
        self.assertIn('Renewal quote', subjects())  # what was shared before stays with the Fleet
        self.assertEqual(self.own.graph_optout(FLEET, False)['off'], None)  # sharing again: at once
        self.rounds()
        self.assertIn('After the OK', subjects())

    def test_the_network_cant_stop_someones_sharing(self):
        self.olive_mail()
        self.rounds()
        self.own.graph_optout(FLEET, True)
        wish = self.own.meta('graph_off:' + FLEET)['at']
        forged = ft.sign(self.mem._private(), ft.optout(FLEET, 'own1', self.net.keys['own1']['sign'], 'mem3', wish, a.now()))  # not an admin
        own_ok = ft.sign(self.own._private(), ft.optout(FLEET, 'own1', self.net.keys['own1']['sign'], 'own1', wish, a.now()))  # their own
        other = ft.sign(self.adm._private(), ft.optout(FLEET, 'own1', self.net.keys['own1']['sign'], 'adm2', 'an earlier ask', a.now()))
        self.net.trust += [forged, own_ok, other]
        self.rounds()
        self.assertEqual(self.own.sharing()[0]['off'], 'asked')

    def test_member_who_left_gets_no_new_updates(self):
        self.olive_mail()
        self.rounds()
        self.assertTrue(self.team(self.mem))
        before = len(self.net.wraps)
        del self.net.people['mem3']
        self.rounds()
        self.add(self.own, mail('work', 7, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Signed', 'Signed order form attached.', 0, 't-renewal'))
        self.judge(self.own, ('work-7', 'client', 'Lee signed the order form'))
        self.rounds()
        self.assertFalse([w for w in self.net.wraps[before:] if w[1] == 'mem3'])
        later = [c[3]['blob'] for c in self.net.calls if c[2] == '/graph' and c[3] and c[3].get('op') == 'put'
                 and c[3]['blob']['header']['id'] not in {w[0] for w in self.net.wraps[:before]}]
        self.assertTrue(later)
        self.assertFalse([b for b in later if 'mem3' in b['wraps'] or 'mem3' in b['header']['to']])  # nothing sealed for them at all
        self.assertEqual(self.team(self.mem), [])  # and their Machine dropped what it had of this Fleet
        self.assertEqual(self.team(self.mem, 'team_mail'), [])
        kv_now, _ = self.own.graph_key(FLEET)
        self.assertNotIn('mem3', self.own.graph_keys(FLEET)[kv_now]['to'])  # a new graph key, without them

    def test_what_someone_who_left_shared_stays_with_the_fleet(self):
        self.add(self.mem, mail('work', 8, 'Kim Wu <kim@globex.example>', 'mem3@acme.example', 'Pilot', 'Pilot starts Monday.', 2, 't-pilot'))
        self.judge(self.mem, ('work-8', 'client', 'Kim confirmed the pilot'))
        self.rounds()
        self.assertIn('Kim Wu', json.dumps(self.team(self.own)))
        del self.net.people['mem3']
        self.rounds()
        self.assertIn('Kim Wu', json.dumps(self.team(self.own)))
        with self.own.store.connect() as db:
            self.assertTrue(db.execute('SELECT left_at FROM team_sources WHERE member=?', ('mem3',)).fetchone()['left_at'])
            self.assertIn('(left)', self.own.team_overview(db, {})['people'][0]['via'])

    # -- the Network as a mailbox, and catching up Machine to Machine
    def away(self, box, days):
        """A Machine that was off for this many days: the Network let go of what waited for it."""
        self.net.expire(box.member_id)
        box.set_meta('graph_fetched_at', ago(days))
        want = box.meta('graph_want:' + FLEET)
        if want:
            box.set_meta('graph_want:' + FLEET, {**want, 'at': ago(days)})

    def relays(self, to=None):
        return [c for c in self.net.calls if c[2] == '/graph' and c[3] and c[3].get('op') == 'relay' and (to is None or to in c[3]['wraps'])]

    def test_a_blob_goes_from_the_network_once_every_machine_took_it(self):
        self.olive_mail()
        self.rounds()
        for box in self.boxes:
            box.graph_fetch()
        self.assertEqual(self.net.held(), set())  # each Machine took what was sealed for it: the Network keeps nothing
        self.assertIn('Renewal quote', json.dumps([json.loads(r['body']) for r in self.team(self.mem, 'team_mail')]))
        kept = {r['kind'] for r in self.team(self.mem, 'team_blobs')}
        self.assertTrue({'snapshot', 'mail'} <= kept)  # the Machines keep it, to pass on to a teammate who missed it
        self.assertFalse(kept & {'key', 'ask', 'want'})

    def test_a_machine_away_longer_than_the_network_keeps_catches_up_from_a_teammate(self):
        self.boxes.remove(self.mem)  # away
        self.olive_mail()
        self.add(self.adm, mail('work', 9, 'Kim Wu <kim@globex.example>', 'adm2@acme.example', 'Pilot', 'Pilot starts Monday.', 1, 't-pilot'))
        self.judge(self.adm, ('work-9', 'client', 'Kim confirmed the pilot'))
        self.rounds()
        self.away(self.mem, 40)  # 30 days on: what waited for it is gone
        self.assertEqual(self.team(self.mem, 'team_mail'), [])
        self.boxes.append(self.mem)
        self.rounds(3)
        threads = json.dumps([json.loads(r['body']) for r in self.team(self.mem, 'team_mail')])
        self.assertIn('Renewal quote', threads)
        self.assertIn('Pilot', threads)
        names = json.dumps(self.team(self.mem))
        self.assertIn('Lee Park', names)
        self.assertIn('Kim Wu', names)
        self.assertTrue(self.relays('mem3'))  # passed on by teammates' Machines, still signed by their publishers
        self.assertNotIn(HEALTH, json.dumps(self.net.calls) + json.dumps(self.net.blobs))
        self.assertFalse([c for c in self.relays() if c[3]['blob']['header']['kind'] not in ('snapshot', 'delta', 'mail', 'file')])

    def test_a_new_member_gets_what_went_before_from_teammates(self):
        self.olive_mail()
        self.add(self.mem, mail('work', 8, 'Kim Wu <kim@globex.example>', 'mem3@acme.example', 'Pilot', 'Pilot starts Monday.', 2, 't-pilot'))
        self.judge(self.mem, ('work-8', 'client', 'Kim confirmed the pilot'))
        self.rounds()
        del self.net.people['mem3']  # Mo leaves: what they shared stays with the Fleet
        self.boxes.remove(self.mem)
        self.rounds()
        self.net.people['mem4'] = ('Noor', 'member')
        noor = self.machine('mem4'); self.boxes.append(noor)
        self.rounds()
        self.ok(self.adm, 'member', 'Noor')
        before = len(self.net.calls)
        self.rounds(4)
        threads = json.dumps([json.loads(r['body']) for r in self.team(noor, 'team_mail')])
        self.assertIn('Renewal quote', threads)
        self.assertIn('Pilot', threads)  # from someone who left, passed on by an admin's Machine
        self.assertIn('Lee Park', json.dumps(self.team(noor)))
        mo = [c for c in self.relays('mem4') if c[3]['blob']['header']['from'] == 'mem3']
        self.assertTrue(mo)
        self.assertEqual({c[0] for c in mo} - {'own1', 'adm2'}, set())
        later = [c[3]['blob']['header'] for c in self.net.calls[before:] if c[2] == '/graph' and c[3] and c[3].get('op') == 'put']
        self.assertFalse([h for h in later if h['kind'] == 'mail'])  # nobody published their threads again for Noor

    def test_share_with_all_signs_everyone_in_one_go_and_seals_after_the_request(self):
        """Share with all: one member statement each and one directory read in the request; the graph round (key, snapshot,
        catching up) runs once after it, not once per person while the owner waits."""
        joined = []
        for mid, name in (('mem4', 'Noor'), ('mem5', 'Ravi'), ('mem6', 'Sam')):
            self.net.people[mid] = (name, 'member')
            box = self.machine(mid); self.boxes.append(box); joined.append(box)
        self.rounds()
        self.assertEqual(sorted(p['name'] for p in self.own._prompts() if p['kind'] == 'member'), ['Noor', 'Ravi', 'Sam'])
        later = []
        self.own.soon = later.append  # the app runs it on its own thread, after the request
        before = len(self.net.calls)
        result = self.own.graph_share_all(FLEET)
        calls = self.net.calls[before:]
        self.assertEqual(result['done'], 3)
        self.assertEqual(sorted(result['names']), ['Noor', 'Ravi', 'Sam'])
        self.assertEqual(sorted(c[3]['item']['s']['member'] for c in calls if c[2] == '/trust'), ['mem4', 'mem5', 'mem6'])
        self.assertEqual([c for c in calls if c[2] == '/graph'], [])  # nothing sealed in the request
        self.assertEqual(sum(1 for c in calls if c[2] == '/directory'), 1)
        self.assertEqual([p for p in self.own._prompts() if p['kind'] == 'member'], [])  # every ask gone at once
        self.assertEqual(len(later), 1)  # one round for all of them
        self.assertEqual(self.own.sharing()[0]['sending'], 3)  # "Sharing with 3…"
        later[0]()
        self.assertEqual(self.own.sharing()[0]['sending'], 0)
        keys = [c[3]['blob']['header'] for c in self.net.calls if c[0] == 'own1' and c[2] == '/graph' and c[3] and c[3].get('op') == 'put']
        self.assertEqual(sum(1 for h in keys[-50:] if h['kind'] == 'snapshot' and {'mem4', 'mem5', 'mem6'} <= set(h['to'])), 1)
        for box in joined:  # each new Machine has the team's graph key from that one round
            box.directory(refresh=True)
            box.graph_fetch()
            self.assertTrue(box.graph_keys(FLEET))

    def test_a_member_ok_returns_before_the_round_and_oks_during_it_share_one_more(self):
        self.net.people['mem4'] = ('Noor', 'member')
        noor = self.machine('mem4'); self.boxes.append(noor)
        self.rounds()
        later = []
        self.own.soon = later.append
        before = len(self.net.calls)
        self.assertTrue(self.ok(self.own, 'member', 'Noor')['done'])
        self.assertEqual([c for c in self.net.calls[before:] if c[2] == '/graph'], [])
        self.assertEqual(self.own.sharing()[0]['sending'], 1)
        rounds = []
        real = self.own.graph_round

        def graph_round(force=False):  # another OK lands while this round runs: it is shared right after, by this thread
            rounds.append(force)
            if len(rounds) == 1:
                self.own.graph_soon(FLEET, ['Noor'])
                self.assertEqual(len(later), 2)
                later[1]()  # finds the round busy: asks for one more instead of a second round alongside
            return real(force=force)
        with patch.object(self.own, 'graph_round', graph_round):
            later[0]()
        self.assertEqual(rounds, [True, True])
        self.assertEqual(self.own.sharing()[0]['sending'], 0)

    def test_a_round_that_never_ended_stops_saying_it_is_sharing(self):
        self.own.set_meta('graph_sending:' + FLEET, {'names': ['Noor'], 'at': ago(1)})
        self.assertEqual(self.own.sharing()[0]['sending'], 0)

    def test_only_an_admin_passes_on_what_someone_who_left_shared(self):
        self.add(self.mem, mail('work', 8, 'Kim Wu <kim@globex.example>', 'mem3@acme.example', 'Pilot', 'Pilot starts Monday.', 2, 't-pilot'))
        self.judge(self.mem, ('work-8', 'client', 'Kim confirmed the pilot'))
        self.rounds()
        self.net.people['mem4'] = ('Noor', 'member')
        noor = self.machine('mem4'); self.boxes.append(noor)
        self.rounds()
        self.ok(self.adm, 'member', 'Noor')
        self.rounds(4)
        self.assertIn('Pilot', json.dumps(self.team(noor, 'team_mail')))
        del self.net.people['mem3']
        self.rounds()
        with noor.store.connect() as db:
            sg.ensure(db)
            row = dict(db.execute("SELECT * FROM team_blobs WHERE member='mem3' AND kind='mail'").fetchone())
        header = json.loads(row['header'])
        wrap = nc.seal({'dk': row['dk'], 'h': row['sha'], 'from_key': self.net.keys['mem3']['sign']}, noor._private(), self.net.keys['adm2'],
                       sg.wrap_context(header, 'mem4', 'adm2'))
        with self.assertRaisesRegex(ValueError, 'admin'):  # Noor is a member, not an admin
            self.adm.graph_take({'header': header, 'ct': row['ct'], 'sig': row['sig'], 'wrap': wrap, 'by': 'mem4'})

    def test_catching_up_goes_newest_first_a_batch_a_round_and_resumes(self):
        for n in range(6):
            self.add(self.own, mail('work', 30 + n, 'Lee Park <lee@client.example>', 'own1@acme.example', f'Order {n}', BODY, 20 - n, f't-order{n}'))
            self.judge(self.own, (f'work-{30 + n}', 'client', f'Lee placed order {n}'))
        self.boxes.remove(self.mem)
        self.rounds(4)
        self.away(self.mem, 40)
        self.boxes.append(self.mem)
        old = sg.SERVE_BATCH
        sg.SERVE_BATCH = 2
        self.addCleanup(setattr, sg, 'SERVE_BATCH', old)
        before = len(self.net.calls)
        self.rounds(8)
        subjects = [json.loads(r['body'])['subject'] for r in self.team(self.mem, 'team_mail')]
        self.assertEqual(sorted(s for s in subjects if s.startswith('Order')), [f'Order {n}' for n in range(6)])
        mail_relays = [c for c in self.net.calls[before:] if c in self.relays('mem3') and c[3]['blob']['header']['kind'] == 'mail' and c[0] == 'own1']
        seqs = [c[3]['blob']['header']['seq'] for c in mail_relays]
        self.assertEqual(seqs, sorted(seqs, reverse=True))  # the newest first
        self.assertEqual(len(seqs), len(set(seqs)))  # each once: it went on where it stopped
        self.assertGreater(len({c[3]['blob']['header']['id'] for c in mail_relays}), 2)

    # -- a dishonest control plane
    def test_a_changed_blob_or_a_forged_one_is_refused(self):
        self.olive_mail()
        self.rounds()
        self.assertTrue(self.team(self.mem))
        blob_id, _, wrap, by = next(w for w in self.net.wraps if w[1] == 'mem3' and self.net.blobs[w[0]]['header']['kind'] == 'snapshot')
        b = self.net.blobs[blob_id]
        item = {'header': copy.deepcopy(b['header']), 'ct': b['ct'], 'sig': b['sig'], 'wrap': wrap, 'by': by}
        data = bytearray(nc.unb64(b['ct'])); data[60] ^= 1
        changes = [
            ('changed text', {**item, 'ct': nc.b64(bytes(data))}),
            ('another sender', {**item, 'header': {**item['header'], 'from': 'adm2'}}),
            ('another seq', {**item, 'header': {**item['header'], 'seq': item['header']['seq'] + 10**9}}),
            ('a replay', item),  # the same snapshot again: older than or equal to the one taken
            ('re-sealed by a member', {**item, 'by': 'mem3'}),
        ]
        for why, forged in changes:
            with self.subTest(why), self.assertRaises((nc.SealError, ValueError)):
                self.mem.graph_take(forged)

    def test_the_network_cant_add_a_member_or_an_admin(self):
        """The control plane lists a Machine of its own with its own keys and signs a member statement for it: no
        teammate's Machine seals anything for it, and nothing it publishes is taken."""
        self.olive_mail()
        evil = nc.new_keys()
        public = nc.public_keys(evil)
        self.net.extra_members = [{'member_id': 'cp9', 'name': 'Support', 'label': 'Support', 'role': 'admin', 'account_email': 'x@acme.example',
                                   'emails': [], 'keys': public}]
        self.net.trust.append(ft.sign(evil, ft.statement('member', FLEET, 'cp9', public['sign'], 'cp9')))
        self.net.trust.append(ft.sign(evil, ft.statement('admin', FLEET, 'cp9', public['sign'], 'own1')))
        self.rounds()
        self.assertFalse([w for w in self.net.wraps if w[1] == 'cp9'])
        for c in self.net.calls:
            if c[2] == '/graph' and c[3] and c[3].get('op') == 'put':
                self.assertNotIn('cp9', c[3]['blob']['wraps'])
        header = {'v': 1, 'fleet': FLEET, 'from': 'cp9', 'id': 'ab' * 16, 'seq': 10**13, 'kind': 'snapshot', 'at': a.now(), 'to': ['mem3'], 'kv': 'x'}
        blob, _ = sg.make(evil, header, {'records': [{'r': 'cd' * 16, 't': 'person', 'name': 'Planted'}]},
                          {'mem3': self.net.keys['mem3']})
        with self.assertRaisesRegex(ValueError, 'confirmed member'):
            self.mem.graph_take({**blob, 'wrap': blob['wraps']['mem3'], 'by': 'cp9'})
        self.assertNotIn('Planted', json.dumps(self.team(self.mem)))

    def test_a_blob_from_a_teammate_not_confirmed_yet_waits_and_is_taken_once_they_are(self):
        self.net.people['mem4'] = ('Kim', 'member')
        kim = self.machine('mem4'); self.boxes.append(kim)
        self.rounds()
        header = {'v': 1, 'fleet': FLEET, 'from': 'mem4', 'id': 'ef' * 16, 'seq': 10**12, 'kind': 'snapshot', 'at': a.now(), 'to': ['own1'], 'kv': None}
        blob, _ = sg.make(kim.relay.private, header, {'records': [{'r': 'cd' * 16, 't': 'person', 'name': 'Noa Quill', 'score': 1}], 'threads': []},
                          {'own1': self.net.keys['own1']})
        self.net.blobs[header['id']] = {k: blob[k] for k in ('header', 'ct', 'sig')}
        self.net.wraps.append((header['id'], 'own1', blob['wraps']['own1'], 'mem4'))
        self.own.graph_fetch()
        self.assertNotIn('Noa Quill', json.dumps(self.team(self.own)))
        self.ok(self.own, 'member', 'Kim')
        self.rounds()
        self.assertIn('Noa Quill', json.dumps(self.team(self.own)))

    # -- conflicts
    def test_conflict_hand_wins_else_the_closest(self):
        entry = {'kind': 'person', 'sources': [
            {'fleet': FLEET, 'member': 'adm2', 'name': 'Ada', 'left': False, 'record': {'name': 'Lee Park', 'role': 'Buyer', 'score': 4.0}},
            {'fleet': FLEET, 'member': 'mem3', 'name': 'Mo', 'left': False, 'record': {'name': 'Lee P.', 'role': 'CFO', 'score': 1.0}}]}
        out = sg.resolve(entry)
        self.assertEqual((out['name'], out['role'], out['owner']), ('Lee Park', 'Buyer', 'adm2'))
        entry['sources'][1]['record']['role_hand'] = True
        self.assertEqual(sg.resolve(entry)['role'], 'CFO')
        self.assertEqual(sg.via(entry['sources']), 'via Ada and Mo')
        stage = sg.pick_stage([{'value': 'Proposal', 'at': '2026-10-20', 'hand': False}, {'value': 'Signed', 'at': '2026-10-18', 'hand': False},
                               {'value': 'Lost', 'at': '2026-10-01', 'hand': False}])
        self.assertEqual(stage['value'], 'Proposal')  # the newest move a message showed
        stage = sg.pick_stage([{'value': 'Proposal', 'at': '2026-10-20', 'hand': False}, {'value': 'Signed', 'at': '2026-10-18', 'hand': True}])
        self.assertEqual(stage['value'], 'Signed')  # a move by hand stands

    def test_the_closer_teammate_owns_a_shared_person(self):
        self.olive_mail()
        self.add(self.adm, *[mail('work', 10 + i, 'Lee Park <lee@client.example>', 'adm2@acme.example', f'Call {i}', 'Notes from the call.', i, f't-call{i}')
                             for i in range(1, 9)],
                 *[mail('work', 30 + i, 'Ada <adm2@acme.example>', 'lee@client.example', f'Re: Call {i}', 'Thanks!', i, f't-call{i}') for i in range(1, 9)])
        self.judge(self.adm, *[(f'work-{10 + i}', 'client', 'Lee and Ada spoke') for i in range(1, 9)])
        self.rounds(3)
        with self.mem.store.connect() as db:
            people = self.mem.team_overview(db, {})['people']
            entry = next(e for e in self.mem.team_graph(db) if e['kind'] == 'person')
        lee = next(p for p in people if p['name'] == 'Lee Park')
        self.assertEqual(lee['via'], 'via Ada and Olive')  # one person, both teammates, the closest first
        self.assertEqual(sg.resolve(entry)['owner'], 'adm2')

    # -- the review's call
    def test_finish_analysis_takes_team_calls_only_for_its_batch(self):
        store = self.own.store
        self.add(self.own, mail('work', 40, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Hello', 'Hi', 1, 't-h'))
        claim = store.begin_analysis(['work'], 10, 'agent:main:assistant-review-x', 'run1')
        event = self.event_id(self.own, 'work-40')
        with self.assertRaisesRegex(ValueError, 'belong to this batch'):
            store.finish_analysis(claim['analysis_id'], 'ok', 'agent:main:assistant-review-x', 'run1', team=[{'event_id': 999999, 'share': 'client'}])
        with self.assertRaisesRegex(ValueError, 'share'):
            store.finish_analysis(claim['analysis_id'], 'ok', 'agent:main:assistant-review-x', 'run1', team=[{'event_id': event, 'share': 'public'}])
        store.finish_analysis(claim['analysis_id'], 'ok', 'agent:main:assistant-review-x', 'run1', team=[{'event_id': event, 'share': 'client', 'line': 'Lee said hello'}])
        with store.connect() as db:
            self.assertEqual(db.execute('SELECT verdict FROM share_threads').fetchone()['verdict'], 'client')

    def test_a_review_cant_set_team_or_only_you_by_hand(self):
        self.olive_mail()
        app = object.__new__(a.App); app.store, app.fleet, app.config = self.own.store, self.own, self.own.config
        with self.assertRaisesRegex(ValueError, 'finish_analysis team'):
            app.graph_action({'event_id': self.event_id(self.own, 'work-3'), 'share': 'team', '_review_session': 'agent:main:assistant-review-x'})
        with self.assertRaisesRegex(ValueError, 'finish_analysis team'):
            app.graph_action({'node_id': 'org:client.example', 'keep_private': False, '_review_session': 'agent:main:assistant-review-x'})
        app.graph_action({'event_id': self.event_id(self.own, 'work-3'), 'share': 'team'})  # the owner in chat
        with self.own.store.connect() as db:
            self.assertEqual(db.execute("SELECT hand FROM share_threads WHERE thread='gm:t-health'").fetchone()['hand'], 'team')

    def test_weekly_report_line(self):
        self.olive_mail()
        self.rounds()
        lines = a.recap_share_lines(self.own.store, {'dashboard_host': 'box.example', 'dashboard_path': '/'})
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], f"• Shared 1 thread with Acme this week, 1 held back. [What's shared](https://box.example/#shared={FLEET})")


    def test_empty_removal_blobs_remove_threads_files_and_catchup_requests(self):
        self.olive_mail()
        self.files(self.own)
        self.rounds()
        group = self.own._group(FLEET)
        me = self.own._me_in(group)
        thread = next(r for r in self.team(self.mem, 'team_mail')
                      if r['member'] == 'own1' and not json.loads(r['body']).get('private'))
        tag = thread['tag']
        old_id, _, wrap, by = next(w for w in self.net.wraps if w[1] == 'mem3' and self.net.blobs[w[0]]['header'].get('tag') == tag)
        old_item = {**copy.deepcopy(self.net.blobs[old_id]), 'wrap': wrap, 'by': by}
        attachments = [r['tag'] for r in self.team(self.mem, 'team_files') if r['member'] == 'own1']
        self.assertTrue(attachments)
        for ftag in attachments:
            self.own._put(group, me, 'file', None, ['mem3'], tag=ftag)
        self.own._put(group, me, 'mail', None, ['mem3'], tag=tag)
        self.own._put(group, me, 'want', {'at': a.now(), 'snap': {}, 'got': {}}, ['mem3'], tag='a' * 32)
        self.mem.graph_fetch()
        self.assertFalse([r for r in self.team(self.mem, 'team_mail') if r['tag'] == tag])
        self.assertFalse([r for r in self.team(self.mem, 'team_files') if r['tag'] in attachments])
        self.assertTrue([r for r in self.team(self.mem, 'team_wants') if r['member'] == 'own1'])
        self.own._put(group, me, 'want', None, ['mem3'], tag='a' * 32)
        self.mem.graph_fetch()
        self.assertFalse([r for r in self.team(self.mem, 'team_wants') if r['member'] == 'own1'])
        # The signed tombstones, not the old content, remain available for an offline teammate's catch-up.
        kept = [r for r in self.team(self.mem, 'team_blobs') if r['tag'] == tag]
        self.assertEqual(len(kept), 1)
        self.assertEqual(kept[0]['ct'], '')
        with self.assertRaisesRegex(ValueError, 'older'):
            self.mem.graph_take(old_item)

    @patch.object(sg, 'SERVE_BATCH', 3)  # same signed catch-up path, a smaller per-round budget keeps this fixture quick
    def test_catchup_chain_larger_than_one_round_advances_in_order(self):
        group = self.own._group(FLEET)
        me = self.own._me_in(group)
        initial = next(r for r in self.team(self.mem, 'team_sources') if r['member'] == 'own1')['seq']
        previous = self.own._put(group, me, 'snapshot', {'records': [], 'threads': []}, ['adm2', 'mem3'])
        for _ in range(sg.SERVE_BATCH + 1):
            previous = self.own._put(group, me, 'delta', {'prev': previous['seq'], 'records': [], 'threads': []}, ['adm2', 'mem3'])
        self.adm.graph_fetch()
        self.net.expire('mem3')
        self.mem._put(self.mem._group(FLEET), self.mem._me_in(self.mem._group(FLEET)), 'want',
                      {'at': a.now(), 'snap': {}, 'got': {}}, ['adm2'], tag='b' * 32)
        self.adm.graph_fetch()
        self.adm.set_meta('graph_puts', [])
        adm_group = self.adm._group(FLEET)
        found, trusted, _ = self.adm.confirmed(adm_group)
        self.adm._graph_serve(adm_group, self.adm._me_in(adm_group), found, trusted)
        self.mem.graph_fetch()
        source = next(r for r in self.team(self.mem, 'team_sources') if r['member'] == 'own1')
        self.assertGreater(source['seq'], initial)
        self.assertLess(source['seq'], previous['seq'])
        self.adm._graph_serve(adm_group, self.adm._me_in(adm_group), found, trusted)
        self.mem.graph_fetch()
        source = next(r for r in self.team(self.mem, 'team_sources') if r['member'] == 'own1')
        self.assertEqual(source['seq'], previous['seq'])

    def test_records_sent_after_a_want_are_passed_on_only_when_still_missing(self):
        group, mem_group = self.own._group(FLEET), self.mem._group(FLEET)
        me, mem_me = self.own._me_in(group), self.mem._me_in(mem_group)
        asked = ago(1)  # mem3 asked a day ago and is back: what goes to it now reaches it directly

        def want():  # as _graph_want_round: what mem3 has of each teammate now, under the same ask
            snap = {r['member']: r['seq'] for r in self.team(self.mem, 'team_sources')}
            self.mem._put(mem_group, mem_me, 'want', {'at': asked, 'snap': snap, 'got': {}}, ['adm2'], tag='b' * 32)
            self.adm.graph_fetch()

        def serve():
            self.adm.set_meta('graph_puts', [])
            adm_group = self.adm._group(FLEET)
            found, trusted, _ = self.adm.confirmed(adm_group)
            self.adm._graph_serve(adm_group, self.adm._me_in(adm_group), found, trusted)
            self.mem.graph_fetch()

        def passed_on():
            return [c for c in self.relays('mem3') if c[3]['blob']['header']['from'] == 'own1' and c[3]['blob']['header']['kind'] in ('snapshot', 'delta')]

        def seq():
            return next(r for r in self.team(self.mem, 'team_sources') if r['member'] == 'own1')['seq']

        want()
        previous = self.own._put(group, me, 'snapshot', {'records': [], 'threads': []}, ['adm2', 'mem3'])
        for _ in range(2):
            previous = self.own._put(group, me, 'delta', {'prev': previous['seq'], 'records': [], 'threads': []}, ['adm2', 'mem3'])
        self.adm.graph_fetch()
        self.mem.graph_fetch()
        self.assertEqual(seq(), previous['seq'])
        with self.assertNoLogs('personal-assistant', level='INFO'):
            serve()  # mem3 took them itself: not passed on again, so no second copy to drop
        self.assertEqual(passed_on(), [])
        want()
        last = self.own._put(group, me, 'delta', {'prev': previous['seq'], 'records': [], 'threads': []}, ['adm2', 'mem3'])
        self.adm.graph_fetch()
        self.net.expire('mem3')  # lost on the way to mem3: a gap in its chain
        serve()
        self.assertEqual(passed_on(), [])  # not yet: it may still come directly
        with patch.object(sg, 'SERVE_SETTLE', 0):  # a while later, the want still says it lacks it
            serve()
        self.assertEqual([c[3]['blob']['header']['seq'] for c in passed_on()], [last['seq']])
        self.assertEqual(seq(), last['seq'])

    def test_a_second_copy_of_a_delta_is_dropped_quietly(self):
        group = self.own._group(FLEET)
        me = self.own._me_in(group)
        had = next(r for r in self.team(self.mem, 'team_sources') if r['member'] == 'own1')['seq']
        header = self.own._put(group, me, 'delta', {'prev': had, 'records': [], 'threads': []}, ['mem3'])
        item = next(i for i in self.net.graph_get('mem3', 0)['items'] if i['header']['id'] == header['id'])
        self.mem.graph_take(item)
        with self.assertRaises(sg.Had):
            self.mem.graph_take(item)

    def test_a_temporary_attachment_listing_failure_is_retried_without_new_mail(self):
        self.olive_mail()
        self.files(self.own)
        fetch = self.own.mail_files
        self.own.mail_files = lambda *args: (_ for _ in ()).throw(OSError('temporary provider outage'))
        self.rounds()
        self.assertFalse(self.team(self.mem, 'team_files'))
        self.own.mail_files = fetch
        self.rounds()
        self.assertTrue(self.team(self.mem, 'team_files'))

    # The rest of this file's tests are in tests/test_shared_graph_more.py, a file of their own so the two halves run side
    # by side; the helpers below are theirs (and some of the tests above use them too).

    # -- seamless, and still safe: removal, new devices, pause
    def new_thread(self, n, subject, body, days=0):
        self.add(self.own, mail('work', n, 'Lee Park <lee@client.example>', 'own1@acme.example', subject, body, days, f't-new-{n}'))
        self.judge(self.own, (f'work-{n}', 'client', 'Lee wrote'))

    def received(self, box):
        return json.dumps(self.team(box, 'team_mail'))

    def from_others(self, box):
        """What teammates shared with this Machine and it still has, per table."""
        return {table: n for table in ('team_records', 'team_mail', 'team_files', 'team_sources', 'team_blobs')
                if (n := len([r for r in self.team(box, table) if r['member'] != box.member_id]))}

    # -- what goes, judged per thread: when unsure, not
    def peers(self):
        """Fictional unsure threads: two listing swaps with software companies, a fund asking about a stake, one ungrouped."""
        self.add(self.own, mail('work', 40, 'Pat <pat@listy.example>', 'own1@acme.example', 'Listy x Acme', 'Shall we add each other to our comparison pages?', 3, 't-listy'),
                 mail('work', 41, 'Kim <kim@rankr.example>', 'own1@acme.example', 'Rankr x Acme', 'A backlink swap for our CRM roundup?', 2, 't-rankr'),
                 mail('work', 42, 'Ola <ola@northfund.example>', 'own1@acme.example', 'Quick catch-up', 'Would you consider selling a stake this year?', 1, 't-fund'),
                 mail('work', 43, 'Ray <ray@misc.example>', 'own1@acme.example', 'Hello', 'Hi there, a question for you.', 1, 't-misc'))
        with self.own.store.connect() as db:
            sg.judge(db, [{'event_id': self.event_id(self.own, 'work-40'), 'share': 'unsure', 'line': '', 'group': 'Partner and listing exchanges', 'suggest': 'team'},
                          {'event_id': self.event_id(self.own, 'work-41'), 'share': 'unsure', 'line': '', 'group': ' Partner and  listing exchanges ', 'suggest': 'team'},
                          {'event_id': self.event_id(self.own, 'work-42'), 'share': 'unsure', 'line': '', 'group': 'Investors and buyers', 'suggest': 'people'},
                          {'event_id': self.event_id(self.own, 'work-43'), 'share': 'unsure', 'line': '', 'suggest': 'whatever'}])

    # -- what went wrong in a live Fleet: these are its cases, with made-up names
    def side_company(self, box=None):
        """A second company of Olive's, connected as Work too: its own mailbox, at its own domain."""
        box = box or self.own
        box.config['accounts'].append({'id': 'side', 'email': 'olive@sidecorp.example', 'boundary': 'work:Sidecorp', 'client': 'x', 'transport': 'gog'})
        self.add(box, mail('side', 1, 'Pat Moss <pat@buyer.example>', 'olive@sidecorp.example', 'Clinic pilot', 'Sidecorp pilot for three clinics.', 1, 't-side'),
                 mail('side', 2, 'Olive <olive@sidecorp.example>', 'pat@buyer.example', 'Re: Clinic pilot', 'Happy to start in May.', 0, 't-side'))
        self.judge(box, ('side-1', 'client', 'Pat asked about a pilot'))

    # -- a board or a thread shared with chosen teammates, by name
    def deal_board(self):
        """Olive's Only you M&A board: a buyer's terms (sensitive), the buyer's billing robot, a personal note from the
        buyer, and the deal's thread in her second company's mailbox."""
        self.olive_mail()
        self.side_company()
        self.add(self.own,
                 mail('work', 20, 'Bo Hale <bo@buyer.example>', 'own1@acme.example', 'Acquisition terms', DEAL, 3, 't-deal'),
                 mail('work', 21, 'Olive <own1@acme.example>', 'bo@buyer.example', 'Re: Acquisition terms', 'Thanks, we will review.', 2, 't-deal'),
                 mail('work', 22, 'Buyer <billing-noreply@buyer.example>', 'own1@acme.example', 'Data room invoice', 'Invoice 88 for the data room.', 2, 't-room'),
                 mail('work', 23, 'Bo Hale <bo@buyer.example>', 'own1@acme.example', 'Our kids', 'Family weekend plans.', 2, 't-kids'))
        self.judge(self.own, ('work-20', 'sensitive', 'Bo sent the acquisition terms'), ('work-22', 'client', 'An invoice'), ('work-23', 'personal', 'Family'))
        return self.board(self.own, 'Acquisition conversations', 'only_you',
                          {'Sale: Buyer': ['work-20', 'work-21', 'work-22', 'work-23', 'side-1']})

    def only_blobs(self):
        return [c[3]['blob'] for c in self.net.calls if c[2] == '/graph' and c[3] and c[3].get('op') in ('put', 'relay')
                and c[3]['blob']['header'].get('only')]

    def deal_timeline(self):
        """The M&A board's project with its whole timeline: a meeting with the buyer and its Zoom notes, an Intercom
        conversation, and the same deal in Olive's second company's calendar and on her personal calendar."""
        board = self.deal_board()
        self.own.config['accounts'] += [{'id': 'cal', 'email': 'own1@acme.example', 'service': 'calendar', 'boundary': 'work:Acme'},
                                        {'id': 'zoom', 'service': 'zoom', 'boundary': 'work:Acme'},
                                        {'id': 'ic', 'service': 'intercom', 'boundary': 'work:Acme'},
                                        {'id': 'sidecal', 'email': 'olive@sidecorp.example', 'service': 'calendar', 'boundary': 'work:Sidecorp'},
                                        {'id': 'homecal', 'email': 'own1@home.example', 'service': 'calendar', 'boundary': 'personal:Home'}]
        meeting = lambda acct, n, title, body, who: {'account_id': acct, 'source_id': f'{acct}-{n}', 'kind': 'calendar.event', 'occurred_at': ago(1), 'title': title,
                                                     'body': body, 'deleted': False, 'metadata': {'organizer': {'email': who}, 'attendees': [
                                                         {'email': who}, {'email': 'bo@buyer.example'}], 'end_at': ago(1)}}
        self.add(self.own,
                 meeting('cal', 1, 'Due diligence call', 'Agenda: walk through the data room.', 'own1@acme.example'),
                 {'account_id': 'zoom', 'source_id': 'zoom-1', 'kind': 'zoom.summary', 'occurred_at': ago(1), 'title': 'Due diligence call',
                  'body': 'Bo wants the closing in June.', 'deleted': False, 'metadata': {'host_email': 'own1@acme.example', 'meeting_id': '9'}},
                 {'account_id': 'ic', 'source_id': 'ic-1', 'kind': 'intercom.conversation', 'occurred_at': ago(1), 'title': 'Buyer question',
                  'body': 'Can our team test the API before closing?', 'deleted': False,
                  'metadata': {'conversation_id': 'c1', 'from': 'Bo Hale <bo@buyer.example>'}},
                 meeting('sidecal', 1, 'Sidecorp board', 'Sidecorp board prep for the sale.', 'olive@sidecorp.example'),
                 meeting('homecal', 1, 'Dinner with Bo', 'Dinner at home, kids too.', 'own1@home.example'))
        with self.own.store.connect() as db:
            graph.label(db, [self.event_id(self.own, x) for x in ('cal-1', 'zoom-1', 'ic-1', 'sidecal-1', 'homecal-1')], 'Sale: Buyer', 'review', a.now())
            graph.set_stage(db, 'Sale: Buyer', 'Signed', 'review', a.now(), reason='Bo signed the letter of intent', event_id=self.event_id(self.own, 'work-20'))
            graph.set_stage(db, 'Sale: Buyer', 'Talks', 'review', a.now(), reason='Sidecorp board wants to wait', event_id=self.event_id(self.own, 'sidecal-1'))
            db.isolation_level = None
            graph.build(db, self.own.config, a.now())
        return board

    def slack(self, n, channel, name, user, text, connect=False):
        return {'account_id': 'sl', 'source_id': f'{channel}:{n}.000100', 'kind': 'slack.message', 'occurred_at': ago(1, n), 'deleted': False,
                'title': f'#{name}: {text}', 'body': text,
                'metadata': {'channel_id': channel, 'channel_name': name, 'conversation_type': 'dm' if name.startswith('DM ') else 'channel',
                             'user_id': user, 'message_ts': f'{n}.000100', 'thread_ts': f'{n}.000100', **({'slack_connect': True} if connect else {})}}

    # -- whose it is: each Machine shares what its own owner took part in
    def crm(self, account, n, sender, to, title, body, days, thread, kind='salesflare.email', host=None):
        """A CRM's copy of someone's email (or a meeting they logged): its From/To in the body, as the CRM keeps it."""
        meta = {'from': sender.split('<')[-1].rstrip('>'), 'thread_id': thread, 'mailbox_user_id': 7,
                'contacts': [{'name': 'Lee Park', 'email': 'lee@client.example'}], **({'host': host} if host else {})}
        return {'account_id': account, 'source_id': f'crm-{n}', 'kind': kind, 'occurred_at': ago(days), 'title': title,
                'body': f'From: {sender}\nTo: {to}\n\n{body}', 'deleted': False, 'metadata': meta}

    # -- team learnings from team conversations (fleet_learnings.py), and asks answered from what the Team Graph shares
    CLIENTS = [('Lee Park', 'lee', 'client.example'), ('Ana Ruiz', 'ana', 'buyer.example'), ('Tom Berg', 'tom', 'shop.example'),
               ('Kim Ito', 'kim', 'store.example')]
    GRADUATION = 'Congrats on the graduation of your daughter at Springfield High!'

    def learn_mail(self):
        """Four client threads about refunds, each with a reply from Olive, and a personal thread in the same work account."""
        events, calls = [], []
        for i, (name, first, domain) in enumerate(self.CLIENTS):
            n = 60 + 2 * i
            events += [mail('work', n, f'{name} <{first}@{domain}>', 'own1@acme.example', 'Refund request', f'Hi, can I get a refund for invoice 4471{i}? {name}', 3, f't-l{i}'),
                       mail('work', n + 1, 'Olive <own1@acme.example>', f'{first}@{domain}', 'Re: Refund request',
                            'Thanks for asking. Refunds go through the support inbox with the refund template.', 2, f't-l{i}')]
            calls.append((f'work-{n}', 'client', f'{name.split()[0]} asked for a refund'))
        events += [mail('work', 90, 'Kai Moss <kai@pal.example>', 'own1@acme.example', 'Your daughter', self.GRADUATION, 3, 't-pp'),
                   mail('work', 91, 'Olive <own1@acme.example>', 'kai@pal.example', 'Re: Your daughter', 'Thank you so much!', 2, 't-pp')]
        self.add(self.own, *events)
        self.judge(self.own, *calls, ('work-90', 'personal', 'Kai wrote'))

    def learn_evidence(self, box):
        import fleet_learnings
        import team_learnings
        with box.connect() as db:
            inputs = box.learn_inputs(db, FLEET)
            names = team_learnings.known_names(db, box.config)
            return (inputs and fleet_learnings.evidence(db, FLEET, inputs['gate'], inputs['accounts'], inputs['team_side'], inputs['company'], names)), names

    def learn_run(self, box, evidence, names, learnings):
        import fleet_learnings
        run_id = a.uuid.uuid4().hex
        with box.connect() as db:
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind,auto,draft) VALUES(?,'ok',?,?,?,'fleet_learn',1,?)",
                       (run_id, a.now(), a.now(), json.dumps(evidence), json.dumps({'learnings': learnings})))
            return fleet_learnings.finish(db, run_id, names, log=box.log)

    REFUNDS = {'kind': 'process', 'text': 'Refund requests are answered from the support inbox with the refund template.', 'confidence': 0.9, 'threads': [1, 2, 3]}

    # -- when one person learns, everyone does: team learnings in a teammate's Work to-do preparations
    def todo(self, box, sid, title, body, accounts):
        with box.store.connect() as db:
            db.execute('INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,?,?,?,?,?)',
                       (sid, sid, title, body, '[]', json.dumps(accounts), 'accepted', a.now()))
        return sid

    def shared_refunds(self):
        self.learn_mail()
        evidence, names = self.learn_evidence(self.own)
        self.learn_run(self.own, evidence, names, [self.REFUNDS])
        self.rounds()

    def teammate_asks(self, box, about, ask_id):
        calls = []  # the answer as it would be sealed for the teammate's Machine
        with patch.object(box.relay, 'call', side_effect=lambda method, path, body=None, timeout=40: calls.append((path, body)) or {'ok': True}):
            status = box.take_ask({'id': ask_id, 'fleet': FLEET, 'from': 'adm2', 'kind': 'relationships', 'question': {'about': about}})
        self.sealed = json.dumps(calls)
        sent = [body for path, body in calls if path == '/answer' and body['id'] == ask_id]
        return status, (sent[-1].get('answer') if sent else None)


class StaticSql(unittest.TestCase):
    def test_the_shared_graph_builds_no_sql_from_strings(self):
        """Every query is a fixed string: lists go in as one JSON parameter (json_each), tables by a fixed statement each."""
        import ast
        for name in ('shared_graph.py',):
            tree = ast.parse(Path(__file__).parent.parent.joinpath(name).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and getattr(node.func, 'attr', '') in ('execute', 'executemany') and node.args:
                    self.assertNotIsInstance(node.args[0], ast.JoinedStr, f'{name}:{node.lineno} builds SQL with an f-string')

    def test_a_list_parameter_matches_like_the_placeholders_did(self):
        import sqlite3
        db = sqlite3.connect(':memory:')
        db.execute('CREATE TABLE event_projects(event_id, project_id)'); db.execute('CREATE TABLE graph_events(event_id, node_id, probable)')
        db.executemany('INSERT INTO event_projects VALUES (?,?)', [(1, 7), (2, 8), (3, 9)])
        db.executemany('INSERT INTO graph_events VALUES (?,?,?)', [(4, 'project:7', 0), (5, 'project:8', 1), (6, "project:7') OR 1=1 --", 0)])
        self.assertEqual(graph.project_event_ids(db, {7, 8}), {1, 2, 4})
        self.assertEqual(graph.project_event_ids(db, set()), set())
        self.assertEqual(set(sg.FLEET_DELETE), {'team_records', 'team_mail', 'team_files', 'team_asks', 'team_sources', 'team_blobs', 'team_wants', 'share_out',
                                                'fleet_learnings', 'fleet_learn_seen', 'fleet_learn_read', 'fleet_learn_removed'})


class AutomatedOnly(unittest.TestCase):
    """Scope.automated_only says for each thread asked what the full `automated` set says, on a sealed database: Gmail and
    CRM threads by their id (a number too), Intercom conversations, messages without a thread, deleted messages and
    another account's messages in the same thread."""

    def test_each_thread_as_the_full_set_says(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        store = a.Store(Path(temp.name) / 'events.sqlite', protect=True)

        def event(account, n, kind, sender, deleted=False, labels=('INBOX',), **meta):
            return {'account_id': account, 'source_id': f'{account}-{n}', 'kind': kind, 'occurred_at': ago(1), 'title': f'Message {n}', 'body': 'Text',
                    'deleted': deleted, 'metadata': {'from': sender, 'to': 'own1@acme.example', 'labels': list(labels), 'message-id': f'<{n}@x>', **meta}}
        events = [event('work', 1, 'gmail.message', 'Audit <no-reply@audit.example>', thread_id='t-auto'),
                  event('work', 2, 'gmail.message', 'Audit <no-reply@audit.example>', thread_id='t-auto'),
                  event('work', 3, 'gmail.message', 'Lee <lee@client.example>', thread_id='t-human'),
                  event('work', 4, 'gmail.message', 'Audit <no-reply@audit.example>', thread_id='t-mixed'),
                  event('work', 5, 'gmail.message', 'Olive <own1@acme.example>', labels=('SENT',), thread_id='t-mixed'),
                  event('work', 6, 'gmail.message', 'Shop <deals@shop.example>', labels=('CATEGORY_PROMOTIONS',), thread_id='t-promo'),
                  event('work', 7, 'gmail.message', 'Alerts <alerts@bank.example>', labels=('CATEGORY_UPDATES',)),  # no thread id
                  event('work', 8, 'gmail.message', 'Lee <lee@client.example>', deleted=True, thread_id='t-gone'),
                  event('work', 9, 'gmail.message', 'Billing <billing@tool.example>', thread_id='t-gone'),
                  event('home', 10, 'gmail.message', 'Sam <sam@friends.example>', thread_id='t-auto'),  # another account
                  event('crm', 11, 'salesflare.email', 'Billing <billing@tool.example>', thread_id=123),
                  event('crm', 12, 'salesflare.email', 'Lee <lee@client.example>', thread_id=124),
                  event('desk', 13, 'intercom.conversation', 'Notifications <notifications@tool.example>', conversation_id=456),
                  event('desk', 14, 'intercom.conversation', 'Kim <kim@client.example>', conversation_id='457')]
        for e in events:
            store.commit_page(e['account_id'], {}, [e])
            if e['deleted']:
                with store.connect() as db:
                    db.execute('UPDATE events SET deleted=1 WHERE source_id=?', (e['source_id'],))
        accounts = ['work', 'crm', 'desk']
        raw = sqlite3.connect(store.path)
        self.addCleanup(raw.close)
        self.assertIn('mc1_sealed', raw.execute("SELECT metadata FROM events WHERE source_id='work-1'").fetchone()[0])  # sealed on disk
        with store.connect() as db:
            sg.ensure(db)
            scope = lambda: sg.Scope(db, accounts, {'acme.example'}, {'own1@acme.example'})
            full = scope().automated
            rows = [dict(r) for r in db.execute('SELECT id,kind,metadata FROM events')]
            threads = {sg.thread_of(r['kind'], json.loads(r['metadata']), r['id']) for r in rows} | {'gm:nowhere', 'ev:999999'}
            for thread in sorted(threads):
                self.assertEqual(thread in scope().automated_only([thread]), thread in full, thread)
            self.assertEqual(scope().automated_only(threads), full & threads)
        self.assertEqual(sorted(full & threads), sorted(['gm:t-auto', 'gm:t-promo', 'gm:t-gone', 'sf:123', 'ic:456',
                                                         'ev:' + str(next(r['id'] for r in rows if 'thread_id' not in json.loads(r['metadata']) and r['kind'] == 'gmail.message'))]))


class Sealed(SharedGraph):
    """The rules that read the messages themselves, on a store with message protection on: SQLite sees only the plain
    keys of a message there (message_seal.PLAIN_METADATA), so what they read in SQL has to be among those."""
    PROTECT = True


for _name in dir(SharedGraph):
    if _name.startswith('test_') and _name not in (
            'test_someone_kept_private_on_one_message_keeps_the_whole_thread_also_what_arrives_later',
            'test_the_messages_read_for_someone_kept_private_give_what_reading_every_message_gives',
            'test_a_reply_that_went_before_is_taken_back_once_its_thread_has_someone_kept_private',
            'test_only_you_on_a_direct_message_holds_for_what_arrives_in_it_later'):
        setattr(Sealed, _name, None)  # tests/test_shared_graph_more.py runs its own with message protection on


if __name__ == '__main__':
    unittest.main()
