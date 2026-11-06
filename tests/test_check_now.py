"""Check now (check_now.py and its wiring in assistant.py, cli.py and the dashboard): every source reads now and a review
of what came in starts right away, whatever the time of day. 2026-11-05: an owner saw "Checked 19 minutes ago. Back to
my nap." on an empty list and asked how to make it check now. No Gateway, no model call, nothing is sent."""
import importlib.util
import threading
import time
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from seams import patch_everywhere

import check_now
import cli
import dashboard_parts

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('check_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)


class Runner:
    def __init__(self): self.requests = []
    def __call__(self, request): self.requests.append(request); return {'status': 'admitted'}


class FastStop:
    """The service's stop event, with waits cut short so a check runs through in a moment."""
    def __init__(self): self.event = threading.Event()
    def is_set(self): return self.event.is_set()
    def set(self): self.event.set()
    def wait(self, seconds): return self.event.wait(min(seconds, 0.02))


def event(n, prefix='s'):
    return {'account_id': 'work', 'source_id': f'{prefix}{n}', 'kind': 'gmail.message', 'occurred_at': a.now(), 'title': 'Question',
            'body': 'Can you confirm?', 'metadata': {}, 'deleted': False}


class CheckNow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'work', 'service': 'gmail'}, {'id': 'li', 'service': 'linkedin'},
                                        {'id': 'docs', 'service': 'google_docs', 'signals': False}], 'review_worker': {'enabled': True}}
        self.app.stop = FastStop()
        self.app.check, self.app.collector_wakes, self.app.collector_reads, self.app.collector_resting = check_now.Check(), {}, {}, set()
        self.addCleanup(lambda: self.app.stop.set())

    def test_one_check_at_a_time_and_a_press_just_after_shows_that_one(self):
        check = check_now.Check()
        self.assertTrue(check.start(1000))
        self.assertEqual(check.phase(), 'reading')
        self.assertFalse(check.start(1001))  # a second tap while it runs joins it
        check.read = 1010
        self.assertEqual(check.phase(), 'reviewing')
        check.ended = 1020
        self.assertIsNone(check.phase())
        self.assertFalse(check.start(1020 + check_now.REST_SECONDS - 1))
        self.assertTrue(check.start(1020 + check_now.REST_SECONDS))

    def test_slow_sources_and_action_only_connections_keep_their_own_pace(self):
        config = self.app.config
        self.assertTrue(check_now.fast(config, {'id': 'w', 'service': 'gmail'}))
        self.assertTrue(check_now.fast(config, {'id': 's', 'service': 'slack'}))
        self.assertFalse(check_now.fast(config, {'id': 'l', 'service': 'linkedin'}))
        self.assertFalse(check_now.fast(config, {'id': 'c', 'service': 'salesflare', 'poll_seconds': 60}))
        self.assertFalse(check_now.fast(config, {'id': 'r', 'service': 'rss', 'poll_seconds': 1800}))
        self.assertFalse(check_now.fast(config, {'id': 'd', 'service': 'google_docs', 'signals': False}))

    def test_the_head_says_when_messages_were_reviewed_and_when_the_next_review_is_due(self):
        # The source reads every few minutes are not what the owner waits for; the review into to-dos is
        with self.store.connect() as db:
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,finished_at) VALUES('r1','ok',?,?,?)",
                       (a.now(), a.now(), '2026-11-06T10:05:00+00:00'))
        view = self.app.check_view()
        self.assertEqual((view['reviewed'], view['waiting'], view['next_review'], view['soon']), ('2026-11-06T10:05:00+00:00', 0, None, False))
        self.store.commit_page('work', {}, [event(n) for n in range(12)])
        view = self.app.check_view()
        self.assertEqual((view['waiting'], view['soon']), (12, False))
        due = a.dt.datetime.fromisoformat(view['next_review']) - a.dt.datetime.now(a.dt.timezone.utc)
        self.assertAlmostEqual(due.total_seconds(), 3600, delta=60)  # once the oldest waited an hour
        self.store.commit_page('work', {}, [event(n, 'b') for n in range(20)])
        self.assertTrue(self.app.check_view()['soon'])  # 32 of 40: the batch is nearly full
        self.assertEqual(self.app.check_view()['phase'], None)

    def test_a_resting_collector_reads_at_once_and_then_a_review_starts(self):
        reads = []
        def sync(store, config, account):
            reads.append(account['id'])
            store.commit_page(account['id'], {'mode': 'incremental'}, [event(len(reads), 'r')])
            return {'mode': 'incremental', 'events': 1}
        account = {'id': 'work', 'service': 'gmail', 'poll_seconds': 300}
        self.app.config['accounts'][0] = account
        self.app.stop = threading.Event()
        with patch.object(self.app, 'resume_wait', return_value=0), patch_everywhere(a, 'sync_source', side_effect=sync):
            collector = threading.Thread(target=self.app.collector, args=(account,), daemon=True); collector.start()
            self.wait_for(lambda: 'work' in self.app.collector_resting)
            self.assertEqual(reads, ['work'])  # the first read; the next is 5 minutes away
            with patch_everywhere(check_now, 'REVIEW_START_WAIT', 0.5):
                started = self.app.action('check_now', {})
                self.assertTrue(started['started'])
                self.assertIn(started['check']['phase'], ('reading', 'reviewing'))  # a quick read may be done already
                self.assertFalse(self.app.action('check_now', {})['started'])  # taps don't stack
                self.wait_for(lambda: len(reads) == 2)
                self.wait_for(lambda: getattr(self.app, 'review_asked', 0))  # the review goes without waiting for a batch
                self.assertEqual(self.app.check.phase(), 'reviewing')
                self.assertEqual(self.app.review_step(Runner()), 'admitted')
                with self.store.connect() as db:
                    db.execute("UPDATE review_runs SET status='ok',finished_at=?", (a.now(),))
                    db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at) VALUES('s1','k1','Reply','','[]','[]',?)", (a.now(),))
                self.wait_for(lambda: self.app.check.phase() is None)
        view = self.app.action('check_now', {'status': True})['check']
        self.assertEqual((view['phase'], view['found']), (None, 1))
        self.assertTrue(view['ended'] and view['rest_until'])
        self.app.stop_all()
        collector.join(2)
        self.assertFalse(collector.is_alive())  # resting collectors stop at once
        self.assertEqual(len(reads), 2)

    def test_reviews_off_or_nothing_new_ends_after_the_reads(self):
        self.app.config['review_worker'] = {'enabled': False}
        self.store.commit_page('work', {}, [event(1)])
        self.assertTrue(self.app.check.start(time.time()))
        check_now.run(self.app.check, self.app)  # nothing resting: no read to wait for
        self.assertIsNone(self.app.check.phase())
        self.assertEqual(getattr(self.app, 'review_asked', 0), 0)
        self.app.config['review_worker'] = {'enabled': True}
        with self.store.connect() as db:
            db.execute('UPDATE events SET analyzed_version=version')
        self.app.check = check_now.Check(); self.app.check.start(time.time())
        check_now.run(self.app.check, self.app)
        self.assertEqual((self.app.check.phase(), self.app.check.found, getattr(self.app, 'review_asked', 0)), (None, 0, 0))

    def test_a_usage_limit_that_holds_the_review_ends_the_check(self):
        self.store.commit_page('work', {}, [event(1)])
        self.app.check.start(time.time())
        def paused():
            self.wait_for(lambda: getattr(self.app, 'review_asked', 0))
            self.app.review_paused = {'window': '5h', 'until': time.time() + 3600}
        threading.Thread(target=paused, daemon=True).start()
        check_now.run(self.app.check, self.app)
        self.assertIsNone(self.app.check.phase())

    def test_the_dashboard_the_phone_app_and_chat_may_ask_but_it_is_no_owner_decision(self):
        self.assertIn('check_now', a.DASHBOARD_ACTIONS)
        self.assertNotIn('check_now', a.OWNER_ACTIONS)  # the agent's `assistant check` may call it too
        args = cli.parser().parse_args(['check', '--wait'])
        self.assertEqual((args.func, args.wait), (cli.cmd_check, True))
        page = dashboard_parts.assemble(ROOT)
        self.assertIn('checkHead()', page)
        self.assertIn("action:'check_now'", page)

    def wait_for(self, done, seconds=5):
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            if done():
                return
            time.sleep(0.02)
        self.fail('timed out')


if __name__ == '__main__':
    unittest.main()
