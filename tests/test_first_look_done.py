"""The first look's ending (App.first_look_done): once it stopped digging, the dashboard says what it read in counts
(the groups its reviewer sorted the signals into, finish_analysis read) and offers the setup steps that fit. Counts and
codes only, never a message's text. No Gateway, nothing sent: the review is played through the Store."""
import datetime as dt, importlib.util, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('first_look_done_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)


def signal(source_id, account='work', kind='gmail.message', days_ago=1):
    when = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days_ago)).isoformat()
    return {'account_id': account, 'source_id': source_id, 'kind': kind, 'occurred_at': when, 'title': 'Your invoice is ready',
            'body': 'Nothing to do.', 'metadata': {'from': 'Billing <no-reply@billing.example>'}, 'deleted': False}


class FirstLookDone(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'gateway', 'service': 'gateway'}, {'id': 'work', 'service': 'outlook'},
                                        {'id': 'work-cal', 'service': 'outlook_calendar'}], 'review_worker': {'enabled': True}}

    def look(self, signals, read=None, run=None, **columns):
        """One first-look run that claims `signals` and finishes them, sorted as `read` says."""
        self.store.commit_page(signals[0]['account_id'], {}, signals)
        run = run or 'r1'
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute('SELECT id FROM events WHERE analyzed_version<version ORDER BY id')]
            cols = {'preview': 1, 'auto': 1, 'window_hours': 168, **columns}
            db.execute(f"INSERT INTO review_runs(run_id,status,started_at,updated_at,{','.join(cols)}) VALUES(?,'ok',?,?,{','.join('?' * len(cols))})",
                       (run, a.now(), a.now(), *cols.values()))
            items = [{'id': i, 'version': 1, 'page': 0} for i in ids]
            db.execute("INSERT INTO analyses(id,started_at,items,status,owner_session,owner_run) VALUES(?,?,?,'running',?,?)",
                       ('an-' + run, a.now(), json.dumps(items), a.REVIEW_SESSION_PREFIX + run, run))
        self.store.finish_analysis('an-' + run, '', a.REVIEW_SESSION_PREFIX + run, run, read=read(ids) if callable(read) else read)
        return ids

    def done(self, why='covered', at=None):
        with self.store.connect() as db:
            db.execute("INSERT OR REPLACE INTO milestones(name,at,detail) VALUES('first_dig_done',?,?)", (at or a.now(), why))

    def test_it_says_what_it_read_in_counts_and_the_steps_that_fit(self):
        ids = self.look([signal(f'm{n}') for n in range(8)])
        self.assertIsNone(self.app.first_look_done())  # still digging: no ending yet
        self.done()
        got = self.app.first_look_done()
        self.assertEqual(got['kinds'], {'email': 8})
        self.assertEqual(got['read'], {})  # the reviewer gave no groups: counts by kind only
        self.assertEqual((got['todos'], got['acted'], got['days']), (0, False, 7))
        self.assertEqual(got['next'], ['inbox'])  # a calendar is connected; one mailbox only
        self.assertNotIn('Your invoice', json.dumps(got))  # counts only, never a message's text
        self.assertEqual(len(ids), 8)

    def test_the_reviewers_groups_are_kept_and_counted_and_nonsense_is_left_out(self):
        self.store.commit_page('work', {}, [signal('x0')])  # a signal from outside the batches below
        with self.store.connect() as db:
            outside = db.execute('SELECT id FROM events').fetchone()[0]
            db.execute('UPDATE events SET analyzed_version=version')
        first = self.look([signal(f'm{n}') for n in range(5)] + [signal('meet', kind='outlook_calendar.event')],
                          read={'newsletters': [], 'bogus': [1], 'notifications': 'all'})
        # The dig's next batch, from another mailbox, sorted this time: its groups count, ids from outside the batch don't
        self.app.config['accounts'].append({'id': 'home', 'service': 'gmail'})
        more = self.look([signal(f'h{n}', account='home') for n in range(4)], run='r2', promising=1, window_hours=None, preview=0, auto=0,
                         read=lambda ids: {'people': [ids[0]], 'newsletters': [ids[1], str(ids[2])], 'notifications': [ids[3], outside, 'x'], 'bogus': [ids[0]]})
        with self.store.connect() as db:
            kept = {i['id']: i.get('read') for i in json.loads(db.execute("SELECT items FROM analyses WHERE id='an-r2'").fetchone()[0])}
            self.assertNotIn('read', db.execute("SELECT items FROM analyses WHERE id='an-r1'").fetchone()[0])
        self.assertEqual(kept, {more[0]: 'people', more[1]: 'newsletters', more[2]: 'newsletters', more[3]: 'notifications'})
        self.done()
        got = self.app.first_look_done()
        self.assertEqual(got['kinds'], {'email': 9, 'meeting': 1})
        self.assertEqual(got['read'], {'people': 1, 'newsletters': 2, 'notifications': 1})
        self.assertEqual(got['next'], [])  # a calendar and two mailboxes: nothing to add
        self.assertEqual(len(first), 6)

    def test_it_counts_the_first_looks_to_dos_and_whether_the_owner_acted(self):
        self.look([signal('m0'), signal('m1')])
        with self.store.connect() as db:
            for n in range(2):
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at) VALUES(?,?,?,?,?,?,?)",
                           (f's{n}', f'k{n}', 'Reply', '', '[1]', '["work"]', a.now()))
        self.done('cards')
        got = self.app.first_look_done()
        self.assertEqual((got['todos'], got['acted']), (2, False))
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d1','s0','complete','','dashboard',?)", (a.now(),))
        self.assertTrue(self.app.first_look_done()['acted'])

    def test_not_after_a_day_not_after_one_that_expired_and_not_without_a_first_look(self):
        self.done()
        self.assertIsNone(self.app.first_look_done())  # no first-look run: an install that reviewed before
        self.look([signal('m0')])
        self.assertIsNone(self.app.first_look_done())  # a review after it stopped digging is not the first look
        self.done()
        self.assertIsNotNone(self.app.first_look_done())
        later = dt.datetime.fromisoformat(a.now()) + dt.timedelta(hours=a.FIRST_LOOK_DONE_HOURS, minutes=1)
        self.assertIsNone(self.app.first_look_done(later))
        self.done('expired')
        self.assertIsNone(self.app.first_look_done())

    def test_no_mail_or_calendar_means_both_steps(self):
        self.app.config['accounts'] = [{'id': 'work-slack', 'service': 'slack'}]
        self.look([signal('c0', account='work-slack', kind='slack.message')])
        self.done()
        got = self.app.first_look_done()
        self.assertEqual(got['kinds'], {'message': 1})
        self.assertEqual(got['next'], ['calendar'])

    def test_only_the_first_looks_reviews_are_asked_to_sort_what_they_read(self):
        self.look([signal('m0')])
        self.assertTrue(self.store.first_look_run('r1'))
        with self.store.connect() as db:
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at) VALUES('regular','ok',?,?)", (a.now(), a.now()))
        self.assertFalse(self.store.first_look_run('regular'))
        self.done()
        self.assertFalse(self.store.first_look_run('r1'))  # once it stopped digging, no more
        self.assertIn('finish_analysis also add read', a.review_prompt('r1', ['work'], first_look=True))
        self.assertIn('Never make a to-do to have something to show', a.review_prompt('r1', ['work'], first_look=True))
        self.assertNotIn('also add read', a.review_prompt('r1', ['work']))

    def test_signal_families(self):
        self.assertEqual([a.signal_family(k) for k in ('gmail.message', 'outlook.message', 'calendar.event', 'outlook_calendar.event', 'zoom.transcript',
                                                        'slack.message', 'stripe.event', 'android.notification')],
                         ['email', 'email', 'meeting', 'meeting', 'meeting', 'message', 'other', 'other'])


if __name__ == '__main__':
    unittest.main()

    # With no to-dos the ending offers something concrete: a service that mails the owner often and isn't connected
    # (push.mailing_sources, the setup hints' own count), on a self-hosted Machine too.

    def test_a_service_that_mails_often_is_offered_when_it_found_nothing(self):
        slack = [dict(signal(f's{n}'), metadata={'from': 'Slack <notification@slack.com>'}) for n in range(3)]
        self.look([signal('m0')] + slack)
        self.done()
        self.assertEqual(self.app.first_look_done()['connect'], [{'service': 'slack', 'label': 'Slack'}])
        self.app.config['accounts'].append({'id': 'slack', 'service': 'slack'})
        self.assertEqual(self.app.first_look_done()['connect'], [])  # connected just now: gone at once

    def test_nothing_to_offer_with_to_dos_or_too_few_mails(self):
        self.look([signal('m0'), dict(signal('s0'), metadata={'from': 'GitHub <noreply@github.com>'})])
        self.done()
        self.assertEqual(self.app.first_look_done()['connect'], [])  # one mail from GitHub: not worth it yet
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at) VALUES('s0','k0','Reply','','[1]','[\"work\"]',?)", (a.now(),))
        self.assertEqual(self.app.first_look_done()['connect'], [])
