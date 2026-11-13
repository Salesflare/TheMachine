"""A project's blockers are checked once a day without a review (ReviewStore.daily_blockers): a day with no new
messages still turns a project that went quiet, or an overdue promise on it, into its one to-do. Same keys and paths as
the review's check, so a review that day, or a second daily run, makes nothing new; a snoozed or closed to-do stays
quiet; only on work days within the owner's hours, only with reviews on. Made-up data; no model, nothing is sent."""
import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import timeutil
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('blockers_daily_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph, ps = a.graph, a.project_success
START = dt.datetime(2026, 10, 28, 12, 0, tzinfo=dt.timezone.utc)  # a Wednesday
QUIET = dt.datetime(2026, 11, 9, 12, 0, tzinfo=dt.timezone.utc)   # a Monday, 12 days later
counter = iter(range(1, 10**6))


def mail(when, sender, to, body, labels=('INBOX',), thread='listing'):
    n = next(counter)
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': when.isoformat(), 'title': 'Guest listing',
            'body': body, 'deleted': False, 'metadata': {'from': sender, 'to': to, 'labels': list(labels), 'message-id': f'<{n}@x>', 'thread_id': thread}}


class DailyBlockers(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = [{'id': 'work', 'service': 'gmail', 'email': 'robin@quillfeather.example'}]
        self.addCleanup(setattr, a.Store, 'accounts', [])
        for p in (patch.object(timeutil, 'LOCAL_TZ', dt.timezone.utc), patch.dict(timeutil.WORK_HOURS, timeutil.WORK_HOURS_DEFAULT)):
            p.start(); self.addCleanup(p.stop)
        self.at(START)
        with self.store.connect() as db:
            graph.save_board(db, {'name': 'Partner listings', 'stages': ['Contacted', 'Agreed', 'In review', 'Live'], 'about': 'Sites that list us'},
                             START.isoformat())
        # The owner pitched, they agreed, the owner asked for news: a review placed it with a Done when
        self.pitch, self.yes = self.add(mail(START - dt.timedelta(hours=30), 'Robin <robin@quillfeather.example>', 'kai@paperkite.example', 'Would you list us?', ('SENT',)),
                                        mail(START - dt.timedelta(hours=20), 'Kai <kai@paperkite.example>', 'robin@quillfeather.example', 'Happy to.'))
        self.review([{'project': 'Paperkite listing', 'board': 'Partner listings', 'stage': 'Agreed', 'reason': 'Kai agreed', 'event_id': self.yes,
                      'condition': 'Listing is live with a link to us', 'proof': 'link'}], replies=[{'event_id': self.yes, 'why': 'a yes'}])
        self.nudge, = self.add(mail(START - dt.timedelta(hours=1), 'Robin <robin@quillfeather.example>', 'kai@paperkite.example', 'Any news?', ('SENT',)))
        with self.store.connect() as db:
            graph.label(db, [self.nudge], 'Paperkite listing', 'review', START.isoformat())

    def at(self, when):
        clock = patch_everywhere(a, 'now', lambda: when.isoformat())
        clock.start(); self.addCleanup(clock.stop)

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])
        with self.store.connect() as db:
            return [db.execute('SELECT id FROM events WHERE source_id=?', (e['source_id'],)).fetchone()[0] for e in events]

    def review(self, stages=(), replies=()):
        claim = self.store.begin_analysis(['work'], 120)
        return self.store.finish_analysis(claim['analysis_id'], 'Listings', stages=list(stages), replies=list(replies))

    def todos(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute("SELECT id,title,status,dedupe_key FROM suggestions WHERE dedupe_key LIKE 'project-success:%' ORDER BY created_at")]

    def test_a_day_with_no_messages_still_gets_the_quiet_project_to_do_once(self):
        self.at(QUIET)
        self.assertTrue(self.store.daily_blockers())
        self.assertEqual([t['title'] for t in self.todos()], ['Nudge Paperkite listing: no reply in 12 days'])
        self.assertEqual(self.todos()[0]['status'], 'pending')  # to look at; nothing drafted or sent
        # A second run that day does nothing; the next day it checks again, and the open to-do is still the one
        self.at(QUIET + dt.timedelta(hours=3))
        self.assertFalse(self.store.daily_blockers())
        self.at(QUIET + dt.timedelta(days=1))
        self.assertTrue(self.store.daily_blockers())
        self.assertEqual(len(self.todos()), 1)

    def test_an_overdue_promise_on_the_project_gets_its_to_do_without_a_review(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,status,created_at,updated_at) "
                       "VALUES('theirs','Kai','send the draft','2026-11-02','2026-11-03',?,'work','open',?,?)", (self.yes, START.isoformat(), START.isoformat()))
        self.at(QUIET)
        self.assertTrue(self.store.daily_blockers())
        self.assertEqual([t['title'] for t in self.todos()], ['Ask Kai about: send the draft'])

    def test_a_review_that_day_and_the_daily_check_make_one_to_do(self):
        # The review checked today: the daily run leaves it
        self.at(QUIET)
        self.add(mail(QUIET - dt.timedelta(minutes=5), 'News <news@letters.example>', 'robin@quillfeather.example', 'This week in CRM', thread='n1'))
        self.review(replies=[])
        self.assertEqual(len(self.todos()), 1)
        self.assertFalse(self.store.daily_blockers())
        self.assertEqual(len(self.todos()), 1)
        # The daily check first, a review later the same day: still the one
        self.at(QUIET + dt.timedelta(days=1))
        self.assertTrue(self.store.daily_blockers())
        self.add(mail(QUIET + dt.timedelta(days=1, hours=1), 'News <news@letters.example>', 'robin@quillfeather.example', 'Next week in CRM', thread='n2'))
        self.at(QUIET + dt.timedelta(days=1, hours=2))
        self.review(replies=[])
        self.assertEqual(len(self.todos()), 1)

    def test_a_snoozed_or_closed_to_do_stays_quiet(self):
        self.at(QUIET)
        self.store.daily_blockers()
        todo, = self.todos()
        for status, day in (('snoozed', 1), ('rejected', 2), ('completed', 3)):
            with self.store.connect() as db:
                db.execute('UPDATE suggestions SET status=? WHERE id=?', (status, todo['id']))
            self.at(QUIET + dt.timedelta(days=day))
            self.assertTrue(self.store.daily_blockers())
            self.assertEqual([(t['id'], t['status']) for t in self.todos()], [(todo['id'], status)])

    def test_only_on_work_days_within_the_hours(self):
        for when in (QUIET - dt.timedelta(days=2), QUIET.replace(hour=5)):  # Saturday; before the hours start
            self.at(when)
            self.assertFalse(self.store.daily_blockers())
        self.assertEqual(self.todos(), [])

    def test_nothing_before_reviews_are_on(self):
        self.at(QUIET)
        app = object.__new__(a.App); app.store = self.store
        app.config = {'review_worker': {'enabled': False}}
        self.assertFalse(app.blockers_step())
        self.assertEqual(self.todos(), [])
        app.config = {'review_worker': {'enabled': True}}
        self.assertTrue(app.blockers_step())
        self.assertEqual(len(self.todos()), 1)


if __name__ == '__main__':
    unittest.main()
