"""One more look for set-aside messages (machine/store/review_last_look.py): a message the review put off twice that may
need the owner (from who wrote to whom, never the words) gets exactly one more look, three days after it came in, inside
a regular review and at most LAST_LOOK_CAP per review. That look ends it: reviewed (a to-do through suggest, with its
dedupe) or put off again and closed for good. Automated mail and mail to many get none; what the owner decided stays
decided; the missed-work audit counts set-aside messages; Connections, Checks lists them with what each waits for."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('last_look_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import missed_work as mw
from machine.store import review_last_look as last_look

OWNER = 'owner@example.com'
ACCOUNTS = [{'id': 'work', 'service': 'gmail', 'email': OWNER, 'boundary': 'work:Acme'}]


def ago(days):
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).isoformat()


class LastLook(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = ACCOUNTS
        self.n = 0

    def add(self, deferrals=2, days=4, kind='gmail.message', **meta):
        """A message the review put off `deferrals` times, in `days` ago."""
        self.n += 1
        meta = {'thread_id': f't{self.n}', 'from': f'Person {self.n} <p{self.n}@other.example>', 'to': OWNER, 'labels': ['INBOX'], **meta}
        with self.store.connect() as db:
            return db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,version,analyzed_version,ingested_at,deferrals) '
                              'VALUES(?,?,?,?,?,?,?,?,1,0,?,?)', ('work', f's{self.n}', kind, ago(days), f'Message {self.n}', 'Can we talk Friday?',
                                                                 json.dumps(meta), f'h{self.n}', ago(days), deferrals)).lastrowid

    def review(self, run, reviewed=lambda batch: [], limit=40):
        """One regular review: the ids it was given and the ones it was told are a last look."""
        batch = self.store.begin_analysis(['work'], limit=limit, owner_session='private', owner_run=run)
        if not batch.get('analysis_id'):
            return [], []
        pages = [batch] + [self.store.analysis_page(batch['analysis_id'], p) for p in range(1, batch.get('pages', 1))]
        views = [e for page in pages for e in page['events']]
        self.store.finish_analysis(batch['analysis_id'], 'Assessed', 'private', run, reviewed(batch))
        return [e['id'] for e in views], [e['id'] for e in views if e.get('last_look')]

    def state(self, event_id):
        with self.store.connect() as db:
            return tuple(db.execute('SELECT analyzed_version>=version, deferrals FROM events WHERE id=?', (event_id,)).fetchone())

    def test_put_off_twice_gets_exactly_one_more_look_then_closes(self):
        stuck = self.add()
        self.assertEqual(self.review('one')[1], [stuck])  # put off again at its last look
        self.assertEqual(self.state(stuck), (0, last_look.CLOSED_AFTER))
        self.assertEqual(self.review('two'), ([], []))  # never offered again
        with self.store.connect() as db:
            self.assertEqual([(x['id'], x['state']) for x in last_look.listing(self.store, db)], [(stuck, 'closed')])

    def test_reviewed_at_its_last_look_is_done(self):
        stuck = self.add()
        self.assertEqual(self.review('one', lambda b: [e['id'] for e in b['events']])[1], [stuck])
        self.assertEqual(self.state(stuck)[0], 1)
        self.assertEqual(self.review('two'), ([], []))

    def test_not_before_three_days_and_not_when_too_old(self):
        fresh, old = self.add(days=1), self.add(days=last_look.LAST_LOOK_MAX_DAYS + 1)
        self.assertEqual(self.review('one'), ([], []))
        with self.store.connect() as db:
            listed = {x['id']: x for x in last_look.listing(self.store, db)}
        self.assertEqual(listed[fresh]['state'], 'look')
        self.assertGreater(listed[fresh]['look_at'], ago(0))  # on its day, two days from now
        self.assertIn(old, listed)

    def test_automated_or_group_mail_gets_no_more_look(self):
        newsletter = self.add(list_unsubscribe='<https://shop.example/u>', **{'from': 'News <news@shop.example>'})
        many = self.add(to=f'{OWNER}, a@x.example, b@x.example, c@x.example')
        sent = self.add(labels=['SENT'], **{'from': OWNER})
        self.assertEqual(self.review('one'), ([], []))
        with self.store.connect() as db:
            self.assertEqual({x['id']: x['state'] for x in last_look.listing(self.store, db)}, {newsletter: 'left', many: 'left', sent: 'left'})
        self.assertEqual(self.state(many), (0, 2))  # left as it was

    def test_a_customer_conversation_gets_one_unless_a_teammate_took_it(self):
        open_one = self.add(kind='intercom.conversation', conversation_id='c1')
        taken = self.add(kind='intercom.conversation', conversation_id='c2', admin_assignee_id='42', assignee_email='mate@acme.example',
                         assignee_name='A teammate')
        self.store.accounts = [*ACCOUNTS, {'id': 'work', 'service': 'intercom', 'admin_id': '7'}]
        self.assertEqual(self.review('one')[1], [open_one])
        self.assertEqual(self.state(taken), (0, 2))

    def test_what_the_owner_decided_is_never_raised_again(self):
        dismissed, snoozed_thread, on_todo = self.add(), self.add(), self.add()
        later_in_snoozed = self.add(thread_id=f't{snoozed_thread}')
        with self.store.connect() as db:
            for sid, status, ids in (('s1', 'rejected', [dismissed]), ('s2', 'snoozed', [snoozed_thread]), ('s3', 'pending', [on_todo])):
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,'A to-do','b',?,'[\"work\"]',?,?)",
                           (sid, sid, json.dumps(ids), status, ago(5)))
            db.execute('UPDATE events SET metadata=? WHERE id=?', (json.dumps({'thread_id': f't{snoozed_thread}', 'from': 'Q <q@other.example>', 'to': OWNER}), snoozed_thread))
            db.execute('UPDATE events SET metadata=? WHERE id=?', (json.dumps({'thread_id': f't{snoozed_thread}', 'from': 'Q <q@other.example>', 'to': OWNER}), later_in_snoozed))
        self.assertEqual(self.review('one'), ([], []))
        for event_id in (dismissed, snoozed_thread, on_todo, later_in_snoozed):
            self.assertEqual(self.state(event_id), (0, 2))

    def test_at_most_the_cap_per_review(self):
        ids = [self.add() for _ in range(last_look.LAST_LOOK_CAP + 3)]
        first = self.review('one')[1]
        self.assertEqual(first, ids[:last_look.LAST_LOOK_CAP])  # oldest in first
        self.assertEqual(self.review('two')[1], ids[last_look.LAST_LOOK_CAP:])
        self.assertEqual(self.review('three'), ([], []))
        more = [self.add() for _ in range(3)]
        self.assertEqual(len(self.review('four', limit=4)[1]), 1)  # a small claim keeps most of its room for new messages
        self.assertEqual(len(more), 3)

    def test_last_look_shares_the_claim_with_new_messages(self):
        stuck = self.add()
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'new', 'kind': 'gmail.message', 'occurred_at': ago(0), 'title': 'New',
                                             'body': 'Hi', 'metadata': {'thread_id': 'tn', 'from': 'N <n@other.example>', 'to': OWNER}, 'deleted': False}])
        given, looks = self.review('one', lambda b: [e['id'] for e in b['events']])
        self.assertEqual(looks, [stuck])
        self.assertEqual(len(given), 2)  # one review for both, no run of its own

    def test_no_second_to_do_after_the_last_look(self):
        stuck = self.add()

        def save(batch):
            self.store.suggest('reply-p', 'Reply about Friday', 'Body', [stuck])
            return [stuck]
        self.assertEqual(self.review('one', save)[1], [stuck])
        self.assertTrue(self.store.suggest('reply-p', 'Reply about Friday', 'Body', [stuck])['duplicate'])
        self.assertEqual(self.review('two'), ([], []))
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM suggestions').fetchone()[0], 1)

    def test_the_audit_counts_set_aside_messages(self):
        stuck, closed, fresh_review = self.add(days=2), self.add(days=2, deferrals=last_look.CLOSED_AFTER), self.add(days=2, deferrals=0)
        with self.store.connect() as db:
            found, _ = mw.candidates(db, ACCOUNTS, ago(7), frozenset({OWNER}), a.calendar_owned, a.bulk_kind)
        flagged = {c['id']: c.get('set_aside') for c in found}
        self.assertEqual(flagged, {stuck: True, closed: True})  # a message waiting its first review is no candidate
        self.assertEqual(mw.patterns([{'what': 'reply', 'channel': 'email', 'area': 'Acme', 'set_aside': True}])['set_aside'], 1)
        self.assertNotIn(fresh_review, flagged)

    def test_the_count_and_list_under_checks(self):
        self.add(), self.add(days=1)
        health = self.store.snapshot(ACCOUNTS)['review_health']
        self.assertEqual(health['set_aside'], 2)
        self.assertEqual([x['state'] for x in health['set_aside_list']], ['look', 'look'])
        self.assertNotIn('set_aside_list', self.store.snapshot(ACCOUNTS, lean=True)['review_health'])


if __name__ == '__main__':
    unittest.main()
