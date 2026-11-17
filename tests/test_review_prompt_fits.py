"""The review prompt always fits the runner's limit: the once-a-day board check takes only the room that is left, and
context a review can do without is left out before a review fails with prompt_too_long (which repeated on every retry,
so no signal turned into a to-do). No Gateway: the runner is a fake and nothing is sent."""
import datetime as dt, importlib.util, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

import graph
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('prompt_fits_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
from machine.app import review as review_app  # noqa: E402


class Runner:
    def __init__(self, *results): self.results = list(results); self.requests = []
    def __call__(self, request): self.requests.append(request); return {'status': self.results.pop(0)}


def signal(source_id, days_ago=1):
    when = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days_ago)).isoformat()
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': when, 'title': 'Pricing question',
            'body': 'Can you confirm?', 'metadata': {'from': 'Sam Example <sam@example.com>'}, 'deleted': False}


class ReviewPromptFits(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'gateway', 'service': 'gateway'}, {'id': 'work', 'service': 'gmail'}],
                           'review_worker': {'enabled': False}, 'delivery_enabled': False}
        model = patch_everywhere(a, 'has_model', return_value=True); model.start(); self.addCleanup(model.stop)

    def projects(self, count, size=40):
        with self.store.connect() as db:
            for n in range(count):
                graph.project_id(db, f'Example project {n:03d} ' + 'x' * size, a.now())

    def offered(self):
        with self.store.connect() as db:
            return db.execute('SELECT run_id FROM board_offers').fetchall()

    def later(self, minutes):
        return patch_everywhere(a, 'now', return_value=(dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=minutes)).isoformat(timespec='seconds'))

    def test_the_board_check_lists_the_newest_projects_that_fit_its_room(self):
        self.projects(200)
        text = self.store.boards_text('run1', chars=2000)
        self.assertLessEqual(len(text), 2000)
        self.assertIn('Example project 199', text)  # newest first
        self.assertNotIn('Example project 000', text)
        self.assertEqual(len(self.offered()), 1)

    def test_no_board_check_and_nothing_offered_when_three_projects_dont_fit(self):
        self.projects(10)
        self.assertEqual(self.store.boards_text('run1', chars=150), '')
        self.assertEqual(self.offered(), [])  # a review that never saw it isn't held to answer it

    def test_many_projects_on_no_board_never_push_the_review_over_the_limit(self):
        self.projects(300)  # about 21,000 characters of board check uncapped: more than the room left under this limit
        self.store.commit_page('work', {}, [signal(f'm{n}', days_ago=3) for n in range(30)])
        runner = Runner('admitted')
        with self.later(4), patch_everywhere(a, 'PROMPT_LIMIT', 40000):
            self.assertEqual(self.app.review_step(runner), 'admitted')
        message = runner.requests[0]['message']
        self.assertLessEqual(len(message), 40000)
        self.assertIn('boards to suggest', message)
        self.assertIn('Example project 299', message)  # the newest
        self.assertNotIn('Example project 000', message)
        self.assertEqual(len(self.offered()), 1)

    def test_context_a_review_can_do_without_goes_before_the_review_fails(self):
        self.store.commit_page('work', {}, [signal(f'm{n}', days_ago=3) for n in range(30)])
        big = 'Made-up history line. ' * 3000  # far more than the prompt has room for
        runner = Runner('admitted')
        with self.later(4), patch.object(a.Store, 'preference_summary', return_value=big), self.assertLogs(a.LOG, 'WARNING') as logs:
            self.assertEqual(self.app.review_step(runner), 'admitted')
        message = runner.requests[0]['message']
        self.assertLessEqual(len(message), a.PROMPT_LIMIT)
        self.assertNotIn('Made-up history line', message)
        self.assertTrue(any('left out preferences' in line for line in logs.output))
        self.assertNotIn('Made-up history line', ' '.join(logs.output))  # sizes only in the log, never the text

    def looking(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO board_backfills(board_id,state,started_at,ranked) VALUES(1,'running',?,'[]')", (a.now(),))

    def test_a_board_looking_through_the_history_takes_the_room_left_and_never_fails_the_review(self):
        # A new board's look used to be built at its full size before the rest was fit: every review went over the
        # limit until the look was done, which needed a review, so no signal became a to-do
        self.store.commit_page('work', {}, [signal(f'm{n}', days_ago=3) for n in range(30)])
        self.looking()
        asked = []
        def backfill(app, run_id, chars):
            asked.append(chars)
            return ('- Made-up counterpart (org:example.test): 4 messages\n' * 1000)[:chars]
        runner = Runner('admitted')
        with self.later(4), patch.object(a.App, 'backfill_text', backfill, create=True), \
                patch.object(review_app, 'source_notes', return_value='\n\nMade-up reading note. ' * 1200), \
                patch.object(a.Store, 'preference_summary', return_value='Made-up history line. ' * 1000):
            self.assertEqual(self.app.review_step(runner), 'admitted')
        message = runner.requests[0]['message']
        self.assertLessEqual(len(message), a.PROMPT_LIMIT - review_app.PROMPT_RESERVE)
        self.assertEqual(len(asked), 1)  # built once: it marks what it asks as asked of this run
        self.assertGreaterEqual(asked[0], review_app.BACKFILL_MIN_ROOM)  # room kept for it while context went
        self.assertIn('Made-up counterpart', message)
        self.assertNotIn('Made-up history line', message)

    def test_a_first_counterpart_bigger_than_its_room_leaves_out_more_context_instead(self):
        self.store.commit_page('work', {}, [signal(f'm{n}', days_ago=3) for n in range(30)])
        self.looking()
        over = lambda app, run_id, chars: 'Made-up counterpart line. ' * ((chars + 9000) // 26)
        runner = Runner('admitted')
        with self.later(4), patch.object(a.App, 'backfill_text', over, create=True), \
                patch.object(review_app, 'source_notes', return_value='\n\nMade-up reading note. ' * 1500), \
                self.assertLogs(a.LOG, 'WARNING') as logs:
            self.assertEqual(self.app.review_step(runner), 'admitted')
        message = runner.requests[0]['message']
        self.assertLessEqual(len(message), a.PROMPT_LIMIT)
        self.assertIn('Made-up counterpart line', message)
        self.assertNotIn('Made-up reading note', message)
        self.assertEqual(sum('left out' in line for line in logs.output), 1)  # one line for the run, sizes only
        self.assertIn('sources chars=', ' '.join(logs.output))

    def test_a_run_refused_for_its_size_makes_the_next_one_smaller_and_logs_once(self):
        self.store.commit_page('work', {}, [signal(f'm{n}', days_ago=3) for n in range(30)])
        requests = []
        def runner(request):
            requests.append(request)
            return {'status': 'error', 'error': 'runtime_error', 'reason': 'context_overflow'} if len(requests) == 1 else {'status': 'admitted'}
        history = 'Made-up history line. ' * 2000  # over the limit both times
        with patch.object(a.Store, 'preference_summary', return_value=history), self.assertLogs(a.LOG, 'WARNING') as logs:
            with self.later(4):
                self.app.review_step(runner)
            self.assertEqual(self.app.review_squeeze, review_app.SQUEEZE_STEP)
            with self.later(30):
                self.assertEqual(self.app.review_step(runner), 'admitted')
        self.assertEqual(len(requests), 2)  # the batch was never claimed: the next run reviews the same signals
        self.assertLessEqual(len(requests[1]['message']), (a.PROMPT_LIMIT - review_app.PROMPT_RESERVE) * review_app.SQUEEZE_STEP)
        self.assertEqual(sum('left out preferences' in line for line in logs.output), 1)  # not once per attempt

    def test_trimming_stops_once_it_fits_and_drops_what_went_from_memory(self):
        dropped = []
        memory = type('Memory', (), {'drop': lambda self, block: dropped.append(block)})()
        parts = {'preferences': 'p' * 50, 'promises': 'q' * 50, 'batch_facts': 'f' * 50, 'facts': 'k' * 10}
        build = lambda p: ''.join(p.values())
        got = review_app.fit_review_parts(build, parts, 120, memory)
        self.assertEqual((got['preferences'], got['promises'], got['batch_facts'], got['facts']), ('', 'q' * 50, 'f' * 50, 'k' * 10))
        self.assertEqual(dropped, ['history'])


if __name__ == '__main__':
    unittest.main()
