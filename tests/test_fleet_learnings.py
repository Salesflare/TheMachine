"""Team learnings from team conversations (fleet_learnings.py): what a pass may keep. The way through the Team Graph,
the switch and removals are in test_shared_graph.py. No network, no model."""
import base64
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
import unittest.mock

spec = importlib.util.spec_from_file_location('fleet_learn_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import fleet
import fleet_learnings as fl
import message_seal

EVIDENCE = {'companies': {'1': 'a' * 16, '2': 'b' * 16, '3': 'a' * 16}}
NAMES = [('Lee Park', 'person'), ('Lee', 'person'), ('Globex', 'org')]
GOOD = {'kind': 'process', 'text': 'Refund requests are answered from the support inbox with the refund template.', 'confidence': 0.9, 'threads': [1, 2]}


def check(**change):
    return fl.check({**GOOD, **change}, EVIDENCE, NAMES)


class Check(unittest.TestCase):
    def test_a_general_learning_is_kept_with_its_label(self):
        item, why = check()
        self.assertIsNone(why)
        self.assertEqual(item, {'kind': 'process', 'text': GOOD['text'], 'confidence': 0.9, 'source': 'team_conversations'})
        for kind in ('tool', 'style', 'routing', 'Process '):
            self.assertIsNone(check(kind=kind)[1], kind)

    def test_product_feedback_customer_specific_and_personal_are_dropped(self):
        for kind in ('product_feedback', 'customer_specific', 'personal'):
            self.assertEqual(check(kind=kind), (None, kind))
        self.assertEqual(check(kind='feature_request'), (None, 'kind'))  # any other label too

    def test_low_confidence_is_dropped_not_asked_about(self):
        self.assertEqual(check(confidence=0.6), (None, 'low_confidence'))
        self.assertEqual(check(confidence='sure'), (None, 'confidence'))

    def test_one_company_is_not_a_pattern(self):
        self.assertEqual(check(threads=[1, 3]), (None, 'one_company'))  # two threads, the same company
        self.assertEqual(check(threads=[]), (None, 'one_company'))
        self.assertEqual(check(threads=[1, 9]), (None, 'one_company'))  # a thread it never saw

    def test_anything_that_identifies_someone_is_dropped_not_edited(self):
        for text in ('Lee Park handles every refund request from the support inbox.',
                     'Refunds for Globex go through the support inbox with the template.',
                     'Refund requests are answered from refunds@acme.example with the template.',
                     'Refunds over 4000 dollars need the finance template first.',
                     'A customer said "just refund me" and the team used the refund template.'):
            self.assertEqual(check(text=text), (None, 'identifying'), text)

    def test_known_and_removed_ones_are_not_made_again_also_when_worded_a_little_differently(self):
        again = 'Refund requests are answered from the support inbox using the refund template.'
        self.assertEqual(fl.check({**GOOD, 'text': again}, EVIDENCE, NAMES, known=[GOOD['text']]), (None, 'known'))
        self.assertEqual(fl.check({**GOOD, 'text': again}, EVIDENCE, NAMES, gone=[GOOD['text']]), (None, 'known'))
        self.assertEqual(fl.fingerprint(GOOD['text']), fl.fingerprint(GOOD['text'].upper() + '  '))

    def test_markup_in_the_turns_text_ends_up_as_plain_words(self):
        for text in ('Renewal questions go to the <b>account owner</b>, not the support inbox.',
                     'Renewal questions go to the &lt;b&gt;account owner&lt;/b&gt;, not the support inbox.',
                     'Renewal questions go to the <a href="x">account owner</a> , not the support inbox.'):
            item, why = check(text=text)
            self.assertIsNone(why, text)
            self.assertEqual(item['text'], 'Renewal questions go to the account owner, not the support inbox.')
        self.assertEqual(fl.plain('<script>alert(1)</script> Use the template > first'), 'alert(1) Use the template first')

    def test_length_bounds(self):
        self.assertEqual(check(text='Use the template.'), (None, 'length'))
        self.assertEqual(check(text='word ' * 60), (None, 'length'))


class Records(unittest.TestCase):
    def test_a_teammates_record_is_taken_only_in_its_fixed_form(self):
        fp = fl.fingerprint(GOOD['text'])
        good = {'r': 'x', 't': 'learning', 'fp': fp, 'kind': 'process', 'text': GOOD['text'], 'confidence': 2, 'at': '2026-10-27T10:00'}
        self.assertEqual(fl.clean_record(good)['confidence'], 1.0)
        self.assertIsNone(fl.clean_record({**good, 'text': 'Something else entirely, sent with the old fingerprint.'}))
        self.assertIsNone(fl.clean_record({**good, 'kind': 'product_feedback'}))
        self.assertIsNone(fl.clean_record({**good, 'fp': 'nope'}))
        marked = fl.clean_record({**good, 'text': '<i>' + GOOD['text'] + '</i>'})  # a teammate's, with markup: plain words
        self.assertEqual(marked['text'], GOOD['text'])
        self.assertEqual(fl.clean_record({'r': 'y', 't': 'unlearn', 'fp': fp, 'text': 'ignored'}), {'r': 'y', 't': 'unlearn', 'fp': fp})

    def test_the_draft_belongs_to_its_running_pass(self):
        db = sqlite3.connect(':memory:')
        db.row_factory = sqlite3.Row
        db.execute('CREATE TABLE profile_runs(run_id TEXT,kind TEXT,status TEXT,draft TEXT,updated_at TEXT)')
        db.execute("INSERT INTO profile_runs VALUES('r1','fleet_learn','running',NULL,'')")
        with self.assertRaises(ValueError):
            fl.save_draft(db, 'r1', {'learnings': 'x'})
        with self.assertRaises(ValueError):
            fl.save_draft(db, 'r2', {'learnings': []})
        self.assertEqual(fl.save_draft(db, 'r1', {'learnings': [GOOD] * 20})['learnings'], fl.MAX_NEW * 3)
        self.assertEqual(json.loads(db.execute('SELECT draft FROM profile_runs').fetchone()[0])['learnings'][0]['kind'], 'process')


class StubFleet:
    """A Standard Work Fleet as Fleet.learn_inputs gives it: the gate stands in for the Team Graph's labels."""
    def __init__(self, shared):
        self.shared, self.logged = shared, []

    def work_fleets(self):
        return ['fl_team']

    def learn_inputs(self, db, ref):
        return {'gate': lambda e: e['metadata'].get('thread_id') in self.shared, 'accounts': ['work'],
                'team_side': lambda m: 'owner@acme.example' in m.get('from', ''), 'company': lambda m: m.get('to', '').rsplit('@', 1)[-1]}

    def log(self, db, *row):
        self.logged.append(row)


class Pass(unittest.TestCase):
    """The daily pass through the service: what it reads, its turn's page and draft, and what it keeps."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = [{'id': 'work', 'service': 'gmail', 'email': 'owner@acme.example'}]
        self.app = object.__new__(a.App)
        self.app.store, self.app.config = self.store, {'accounts': self.store.accounts, 'review_worker': {'enabled': True}}
        self.app.fleet = StubFleet({f't{n}' for n in range(5)})
        at = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)).isoformat()
        for n in range(6):  # five shared threads with five companies, and t5: not shared with the team
            self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': at, 'deleted': False,
                                                 'title': 'Refund', 'body': 'Refunds go through the support inbox.' if n < 5 else 'My private note',
                                                 'metadata': {'from': 'owner@acme.example', 'to': f'x@c{n}.example', 'thread_id': f't{n}'}}])

    def test_a_pass_reads_only_shared_threads_and_its_turn_keeps_what_passes_the_check(self):
        run_id = self.app.fleet_learn_due()
        self.assertTrue(run_id)
        self.assertIsNone(self.app.fleet_learn_due())  # at most once an hour, and once a day
        session = a.PROFILE_SESSION_PREFIX + run_id
        page = self.store.profile_evidence(1, session)
        self.assertEqual(len(page['threads']), 5)
        self.assertNotIn('private', json.dumps(page))
        self.assertNotIn('example', json.dumps(page))  # never which company
        self.assertIn('NO_REPLY', fl.prompt(run_id))
        self.store.save_profile({'learnings': [{**GOOD, 'threads': [1, 2]}, {**GOOD, 'kind': 'product_feedback', 'text': 'Customers want a darker theme for the app.'}]}, session)
        with self.store.connect() as db:
            db.execute("UPDATE profile_runs SET status='ok' WHERE run_id=?", (run_id,))
            kept = fl.finish(db, run_id, [], log=self.app.fleet.log)
            self.assertEqual([k['text'] for k in kept], [GOOD['text']])
            self.assertEqual([r['text'] for r in fl.own(db, 'fl_team')], [GOOD['text']])
            # the turn's draft goes once it is read: only how many it drafted stays on the run, also for a dropped one
            self.assertEqual(db.execute('SELECT draft FROM profile_runs WHERE run_id=?', (run_id,)).fetchone()[0], '{"drafted": 2}')
            self.assertEqual(fl.finish(db, run_id, [], log=self.app.fleet.log), [])
        self.assertEqual(self.app.fleet.logged[0][3:], ('your Fleet', 'learning', GOOD['text'], 'shared with the team, from team conversations'))


class Locked(unittest.TestCase):
    """A sealed Machine whose message key is missing or is another one: its team learnings cannot be read, and that is
    an error everywhere, never an empty list that looks like a team that learned nothing."""
    def setUp(self):
        patcher = unittest.mock.patch.dict(os.environ)  # sealed here, whatever the suite runs as
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop('MESSAGE_PROTECTION_TEST', None)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'events.sqlite'
        store = a.Store(self.path, protect=True)
        with store.connect() as db:
            fl.ensure(db)
        with store.connect() as db:
            db.execute("INSERT INTO fleet_learnings(fleet,fp,kind,text,confidence,run_id,at) VALUES('f1',?,'process',?,0.9,'r','2026-11-01')",
                       (fl.fingerprint(GOOD['text']), GOOD['text']))
            db.execute("INSERT INTO fleet_learn_removed(fleet,fp,text,by,at) VALUES('f1',?,'A removed team learning about refunds.','me','2026-11-01')", ('b' * 32,))
            self.assertEqual([r['text'] for r in fl.own(db, 'f1')], [GOOD['text']])
        self.key = message_seal.key_path(self.path)

    def readers(self, db):
        return {'own': lambda: fl.own(db, 'f1'), 'removed': lambda: fl.removed(db, 'f1'), 'view': lambda: fl.view(db, 'f1', {}),
                'usable': lambda: fl.usable(db, 'f1'), 'pick': lambda: fl.pick(db, 'f1', 'Refund request', 'A refund via the support inbox.'),
                'records': lambda: fl.records(db, 'f1', lambda local: local),
                'remove': lambda: fl.remove(db, 'f1', fl.fingerprint(GOOD['text']))}

    def test_without_the_key_the_app_does_not_start_and_a_reader_gets_an_error_not_an_empty_list(self):
        self.key.unlink()
        with self.assertRaises(message_seal.SealError) as stopped:
            a.Store(self.path)
        self.assertIn('message-content.key is missing', str(stopped.exception))
        self.assertEqual([p[0] for p in message_seal.problems(self.path)], ['message-key-missing'])  # what Needs you and doctor say
        with sqlite3.connect(self.path) as db:  # a tool that opens the file without the key
            db.row_factory = sqlite3.Row
            for name, read in self.readers(db).items():
                with self.subTest(reader=name), self.assertRaises(message_seal.SealError):
                    read()

    def test_with_another_key_the_fleet_tab_and_the_team_graph_round_fail_rather_than_show_or_send_nothing(self):
        self.key.write_bytes(base64.b64encode(os.urandom(32)) + b'\n')
        store = a.Store(self.path)
        with store.connect() as db:
            for name, read in self.readers(db).items():
                with self.subTest(reader=name), self.assertRaises(message_seal.SealError):
                    read()
        tab = type('Tab', (), {'connect': store.connect, 'teammates': lambda self, ref: []})()
        with self.assertRaises(message_seal.SealError):
            fleet.Fleet.learnings_view(tab, 'f1')
        with sqlite3.connect(self.path) as raw:  # nothing was changed by the failed reads
            self.assertEqual(raw.execute('SELECT count(*),typeof(text) FROM fleet_learnings').fetchone(), (1, 'blob'))


if __name__ == '__main__':
    unittest.main()
