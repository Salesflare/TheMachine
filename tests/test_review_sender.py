"""Who wrote a review's batch (machine/app/senders.py, the `sender` block of recall's review purpose): a sender the
Graph knows gets one line when the batch is claimed, an unknown one and the owner themself get none, a summary line
of the other area never appears, the block is left out whole when the reply has no room, and each line is logged."""
import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from seams import patch_everywhere

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('review_sender_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import person_summary  # noqa: E402
from machine.app import review as review_app, senders  # noqa: E402
from machine.app.recall import recall  # noqa: E402

NOW = dt.datetime(2026, 10, 16, 12, tzinfo=dt.timezone.utc)
ACCOUNTS = [{'id': 'work', 'service': 'gmail', 'email': 'sam@acme.com', 'boundary': 'work:Acme'},
            {'id': 'home', 'service': 'gmail', 'email': 'sam@home.example', 'boundary': 'personal:'}]
ANN, KIM, LEE = 'email:ann@client.com', 'email:kim@family.example', 'email:lee@globex.example'
SIDES = {'work': 'work', 'home': 'personal'}


def mail(account, n, hours, sender, title, to=None, labels=('INBOX',)):
    return {'account_id': account, 'source_id': f'{account}{n}', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(hours=hours)).isoformat(),
            'title': title, 'body': title + '.', 'deleted': False,
            'metadata': {'from': sender, 'to': to or ACCOUNTS[0 if account == 'work' else 1]['email'], 'cc': '', 'labels': list(labels),
                         'message-id': f'<{account}{n}@x>', 'thread_id': f't{account}{n}'}}


class ReviewSender(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.store.accounts = ACCOUNTS
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.fleet = None
        self.app.config = {'accounts': ACCOUNTS, 'database': str(Path(temp.name) / 'events.sqlite'), 'review_worker': {'enabled': True}}
        started = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        started.start()
        self.addCleanup(started.stop)
        # Ann, a customer, writes twice at work; Kim, the owner's sister, writes to the work mailbox; Lee is known by
        # name only; a stranger writes for the first time; the owner's own sent mail is in the batch too
        self.store.commit_page('work', {}, [mail('work', 1, 5, 'Ann Example <ann@client.com>', 'Pilot timing'),
                                            mail('work', 2, 4, 'Ann Example <ann@client.com>', 'Pilot budget'),
                                            mail('work', 3, 3, 'Kim Home <kim@family.example>', 'Saturday'),
                                            mail('work', 4, 2, 'Lee Park <lee@globex.example>', 'Invoice'),
                                            mail('work', 5, 2, 'Nobody Known <first@nowhere.example>', 'Hello'),
                                            mail('work', 6, 1, 'Sam <sam@acme.com>', 'Re: Pilot timing', to='ann@client.com', labels=('SENT',))])
        self.store.commit_page('home', {}, [mail('home', 1, 30, 'Kim Home <kim@family.example>', 'Birthday plans')])
        with self.store.connect() as db:
            db.isolation_level = None
            a.graph.build(db, self.app.config, NOW.isoformat())
        with self.store.connect() as db:
            self.ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
            a.graph.set_role(db, ANN, 'customer, runs the pilot', 'owner', NOW.isoformat())
            a.graph.set_role(db, KIM, 'sister', 'owner', NOW.isoformat())
            db.execute("UPDATE events SET analyzed_version=version WHERE account_id='home'")  # read before: not in the batch
        with self.store.connect() as db:
            db.isolation_level = None
            a.graph.build(db, self.app.config, NOW.isoformat())
        with self.store.connect() as db:
            db.execute('UPDATE graph_nodes SET strength=2.0 WHERE id=?', (ANN,))
            db.execute('UPDATE graph_nodes SET strength=1.5 WHERE id=?', (KIM,))
            db.execute('UPDATE graph_nodes SET strength=0.2 WHERE id=?', (LEE,))
            person_summary.save(db, ANN, [{'kind': 'who', 'text': 'Runs the pilot at the client and decides on its budget.', 'sources': [f"E{self.ids['work1']}"]}],
                                NOW.isoformat(), SIDES, NOW.isoformat())
            person_summary.save(db, KIM, [{'kind': 'now', 'text': 'Plans the family birthday for the end of the month.', 'sources': [f"E{self.ids['home1']}"]}],
                                NOW.isoformat(), SIDES, NOW.isoformat())

    def claim(self, run='run-1'):
        with self.store.connect() as db:
            db.execute("INSERT OR REPLACE INTO review_runs(run_id,status,started_at,updated_at,attempts,planned) VALUES(?,'running',?,?,0,1)",
                       (run, NOW.isoformat(), NOW.isoformat()))
        return self.app.events_action('begin_analysis', {'account_ids': ['work', 'home'], 'limit': 40, '_review_session': a.REVIEW_SESSION_PREFIX + run,
                                                         '_review_run': run})

    def log(self):
        with self.store.connect() as db:
            return [tuple(r) for r in db.execute('SELECT purpose,run_id,kind,row_id,how,chars FROM memory_use ORDER BY id')]

    def test_a_known_sender_gets_one_line_with_role_closeness_and_summary(self):
        result = self.claim()
        lines = result['senders'].split('\n')
        self.assertEqual(lines[0], senders.HEADER)
        ann = [line for line in lines if line.startswith('- Ann Example')]
        self.assertEqual(len(ann), 1)  # two messages, one line
        self.assertIn(f"(signals {self.ids['work1']}, {self.ids['work2']})", ann[0])
        self.assertIn('customer, runs the pilot', ann[0])
        self.assertIn('regular contact', ann[0])
        self.assertIn('summary: Runs the pilot at the client and decides on its budget.', ann[0])
        self.assertLess(lines.index(ann[0]), next(i for i, line in enumerate(lines) if line.startswith('- Kim Home')))  # the closest first
        self.assertLessEqual(len(result['senders']), senders.SENDER_CHARS)

    def test_an_unknown_sender_and_the_owner_get_no_line(self):
        text = self.claim()['senders']
        self.assertNotIn('Nobody Known', text)
        self.assertNotIn('nowhere.example', text)
        self.assertNotIn('Lee Park', text)  # in the Graph, but nothing specific: no role, no summary, a faint contact
        self.assertNotIn('- Sam', text)
        self.assertEqual(len(text.split('\n')), 3)  # the first line, Ann and Kim

    def test_nobody_known_means_no_block_and_no_log(self):
        with self.store.connect() as db:
            db.execute("UPDATE graph_nodes SET strength=0.1,info=json_remove(info,'$.role') WHERE kind='person'")
            db.execute('DELETE FROM person_summaries')
        self.assertNotIn('senders', self.claim())
        self.assertEqual(self.log(), [])

    def test_the_other_sides_summary_never_appears(self):
        text = self.claim()['senders']
        kim = next(line for line in text.split('\n') if line.startswith('- Kim Home'))
        self.assertIn('sister', kim)  # who she is to the owner
        self.assertNotIn('birthday', text)  # her summary's line came from a Personal account; this signal is a Work one
        self.assertNotIn('summary:', kim)
        with self.store.connect() as db:  # the same person writing at home: there the line may be read
            db.execute("UPDATE events SET analyzed_version=version WHERE account_id='work'")
            db.execute("UPDATE events SET analyzed_version=0 WHERE account_id='home'")
            db.execute("UPDATE analyses SET status='done'")
        home = self.claim('run-2')['senders']
        self.assertIn('summary: Plans the family birthday for the end of the month.', home)

    def test_a_sender_on_both_sides_in_one_batch_gets_no_one_sided_line(self):
        with self.store.connect() as db:
            db.execute("UPDATE events SET analyzed_version=0 WHERE account_id='home'")
        text = self.claim()['senders']
        kim = next(line for line in text.split('\n') if line.startswith('- Kim Home'))
        self.assertIn(f"(signals {self.ids['work3']}, {self.ids['home1']})", kim)
        self.assertNotIn('birthday', text)

    def test_the_block_is_dropped_whole_when_the_reply_has_no_room(self):
        with patch.object(review_app, 'REPLY_CUT', 3500):  # the claim's reply is already too close to the cut
            result = self.claim()
        self.assertNotIn('senders', result)
        self.assertEqual(self.log(), [])  # and nothing counts as read
        memory = recall(self.app, 'review', {'run': 'run-1', 'analysis': result['analysis_id']}, 1000)
        self.assertEqual(memory.fit('sender', 900), '')
        self.assertEqual(memory.rows(), [])

    def test_the_closest_senders_stay_when_the_block_is_full(self):
        analysis = self.claim()['analysis_id']
        text = senders.lines(self.app, analysis, limit=len(senders.HEADER) + 150)
        self.assertIn('- Ann Example', text)
        self.assertNotIn('- Kim Home', text)
        self.assertLessEqual(len(text), len(senders.HEADER) + 150)

    def test_each_line_is_logged_as_a_record_read_of_that_review(self):
        result = self.claim()
        lines = result['senders'].split('\n')[1:]
        self.assertEqual(self.log(), [('review', 'run-1', 'record', ANN, 'about', len(lines[0])),
                                      ('review', 'run-1', 'record', KIM, 'about', len(lines[1]))])
        with self.store.connect() as db:  # ids and numbers only: no text column to hold a line
            self.assertNotIn('text', {r[1] for r in db.execute('PRAGMA table_info(memory_use)')})

    def test_the_claim_is_the_same_apart_from_the_block(self):
        result = self.claim()
        with self.store.connect() as db:
            db.execute("UPDATE analyses SET status='abandoned',finished_at=? WHERE status='running'", (NOW.isoformat(),))
            db.execute('DELETE FROM memory_use')
        with patch.object(senders, 'lines', return_value=''):
            before = self.claim('run-2')
        self.assertEqual([e['id'] for e in before['events']], [e['id'] for e in result['events']])
        self.assertEqual(set(result) - set(before), {'senders'})


if __name__ == '__main__':
    unittest.main()
