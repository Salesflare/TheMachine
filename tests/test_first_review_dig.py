"""The first review digs until it has something to show. It starts with the week's most promising signals (whatever
their age within the week, no 48-hour cutoff), then goes on a batch at a time, at once, until it has FIRST_DIG_CARDS
to-dos, has looked through the week, or used FIRST_DIG_USAGE percent of the 5-hour window (FIRST_DIG_SIGNALS signals
on a sign-in without usage windows). A failed first review comes back within the backoff (at most half an hour), also
when its runtime reported a failure after the work was saved; a usage limit holds it until the reset. No Gateway,
nothing is sent."""
import datetime as dt, importlib.util, tempfile, time, unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('first_review_dig_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)


class Runner:
    def __init__(self, *results): self.results = list(results); self.requests = []
    def __call__(self, request):
        self.requests.append(request)
        result = self.results.pop(0)
        return result if isinstance(result, dict) else {'status': result}


def mail(source_id, sender='Sam <sam@example.org>', hours_ago=2, labels=()):
    when = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours_ago)).isoformat()
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': when, 'title': 'Hello',
            'body': 'Text', 'metadata': {'from': sender, 'to': 'me@example.com', 'labels': list(labels), 'thread_id': source_id}, 'deleted': False}


class FirstReviewDig(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        # Reviews on, as on a hosted Machine right after it turned them on by itself
        self.app.config = {'accounts': [{'id': 'gateway', 'service': 'gateway'}, {'id': 'work', 'service': 'gmail', 'email': 'me@example.com'}],
                           'review_worker': {'enabled': True}, 'delivery_enabled': True}
        a.Store.accounts = [{'id': 'work', 'service': 'gmail', 'email': 'me@example.com'}]
        self.addCleanup(setattr, a.Store, 'accounts', [])
        for name, value in (('has_model', True), ('openclaw_model', 'claude-cli/claude-opus-5-5')):
            p = patch.object(a, name, return_value=value); p.start(); self.addCleanup(p.stop)
        self.app.model_usage = None  # an API key or a sign-in that reports no windows, unless a test sets them

    def later(self, minutes):
        return patch.object(a, 'now', return_value=(dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=minutes)).isoformat(timespec='seconds'))

    def step(self, runner, minutes=0):
        with self.later(minutes):
            return self.app.review_step(runner)

    def runs(self):
        with self.store.connect() as db: return [dict(r) for r in db.execute('SELECT * FROM review_runs ORDER BY started_at')]

    def review(self, minutes, cards=0, status='ok', save=True, receipt=None):
        """The running review sees its batch, saves `cards` to-dos (each one shows at once) and saves the batch (or not),
        then ends with `status`."""
        run = self.runs()[-1]
        with self.later(minutes):
            claim = self.store.begin_analysis(['work'], 120, a.REVIEW_SESSION_PREFIX + run['run_id'], run['run_id'])
            ids = [e['id'] for e in claim['events']]
            for n in range(cards):
                self.store.suggest(f'{run["run_id"]}-{n}', f'Reply {n}', 'Asked.', [ids[n]])
            if save and ids:
                with self.store.connect() as db:
                    db.execute('UPDATE events SET analyzed_version=version WHERE id IN (' + ','.join('?' * len(ids)) + ')', ids)
                    db.execute("UPDATE analyses SET status='complete',finished_at=? WHERE id=?", (a.now(), claim['analysis_id']))
        self.assertEqual(self.step(Runner(receipt or status), minutes), status)
        return ids

    def dig(self, minutes=0):
        with self.later(minutes), self.store.connect() as db:
            return self.app.first_dig(db)

    def test_the_quick_review_takes_the_weeks_most_promising_whatever_their_age(self):
        # 2026-10-27/28: three of six new Machines got no to-do from their quick review: the 48 hours it looked at held
        # one message or a few newsletters, while people waiting on the owner wrote days earlier
        news = [mail(f'news{n}', 'Shop <news@shop.example>', hours_ago=1, labels=['CATEGORY_PROMOTIONS']) for n in range(30)]
        asks = [mail(f'ask{n}', f'P{n} <p{n}@example.org>', hours_ago=24 * (3 + n)) for n in range(3)]
        old = [mail('old', hours_ago=24 * 9)]
        self.store.commit_page('work', {}, news + asks + old)
        self.assertEqual(self.step(Runner('admitted')), 'admitted')
        run = self.runs()[0]
        self.assertEqual((run['window_hours'], run['budget'], run['planned']), (a.PREVIEW_DAYS * 24, a.QUICK_LOOK_SIGNALS, a.QUICK_LOOK_SIGNALS))
        claim = self.store.begin_analysis(['work'], 120, a.REVIEW_SESSION_PREFIX + run['run_id'], run['run_id'])
        with self.store.connect() as db:
            names = {i: s for i, s in db.execute('SELECT id,source_id FROM events')}
        order = [names[e['id']] for e in claim['events']]
        self.assertEqual(len(order), a.QUICK_LOOK_SIGNALS)  # the same small batch, not more reading
        self.assertEqual(order[:3], ['ask0', 'ask1', 'ask2'])  # who waits on the owner first, newest first
        self.assertNotIn('old', order)  # never past the week

    def test_a_quick_review_with_no_to_do_digs_on_at_once_until_the_week_is_looked_through(self):
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(45)])
        self.step(Runner('admitted'))
        self.review(2)  # nothing found
        # The next batch at once: no gap, no waiting for 40 signals or for the oldest to wait an hour
        self.assertEqual(self.step(Runner('admitted'), 2), 'admitted')
        nxt = self.runs()[1]
        self.assertEqual((nxt['window_hours'], nxt['budget'], nxt['promising'], nxt['planned']), (None, a.FIRST_LOOK_NEXT_SIGNALS, 1, 20))
        self.review(4)
        self.assertEqual(self.step(Runner('admitted'), 4), 'admitted')
        self.assertEqual(self.runs()[2]['planned'], 5)
        self.review(6)
        self.assertEqual(self.dig(6), {'done': 'covered'})  # (b) the whole week looked through
        self.assertIsNone(self.step(Runner(), 7))
        with self.store.connect() as db:
            self.assertEqual(a.first_cards_report(db, self.app.config['accounts'])['dig'], 'covered')

    def test_it_stops_digging_at_three_to_dos(self):
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(70)])
        self.step(Runner('admitted'))
        self.review(2, cards=1)
        self.assertEqual(self.dig(2), {'cards': 1, 'left': 50})
        self.step(Runner('admitted'), 2)
        self.review(4, cards=2)
        self.assertEqual(self.dig(4), {'done': 'cards'})  # (a) three to-dos
        # The rest of the week goes in the regular reviews, at their own pace
        self.assertIsNone(self.step(Runner(), 5))
        self.assertEqual(len(self.runs()), 2)

    def test_it_stops_digging_at_its_share_of_the_five_hour_window(self):
        reset = time.time() + 3 * 3600
        self.app.model_usage = [{'provider': 'anthropic', 'windows': [{'label': '5h', 'used': 10, 'reset': reset}]}]
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(100)])
        self.step(Runner('admitted'))  # the window stood at 10% when the first review started
        self.review(2)
        self.app.model_usage[0]['windows'][0]['used'] = 69
        self.assertIn('left', self.dig(2))  # 59% of the window so far: on
        self.app.model_usage[0]['windows'][0]['used'] = a.FIRST_DIG_USAGE + 10
        self.assertEqual(self.dig(3), {'done': 'usage'})  # (c) 60% of the 5-hour window
        self.assertIsNone(self.step(Runner(), 4))

    def test_a_window_that_reset_since_counts_whole(self):
        self.app.model_usage = [{'provider': 'anthropic', 'windows': [{'label': '5h', 'used': 50, 'reset': time.time() + 600}]}]
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(100)])
        self.step(Runner('admitted'))
        self.review(2)
        self.app.model_usage = [{'provider': 'anthropic', 'windows': [{'label': '5h', 'used': 30, 'reset': time.time() + 5 * 3600}]}]
        self.assertIn('left', self.dig(3))
        self.app.model_usage[0]['windows'][0]['used'] = a.FIRST_DIG_USAGE
        self.assertEqual(self.dig(3), {'done': 'usage'})

    def test_without_usage_windows_it_stops_at_a_matching_number_of_signals(self):
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n / 2 + 1) for n in range(a.FIRST_DIG_SIGNALS + 40)])
        self.step(Runner('admitted'))
        minutes = 2
        for _ in range(a.FIRST_DIG_SIGNALS // a.QUICK_LOOK_SIGNALS - 1):
            self.review(minutes)
            self.assertEqual(self.step(Runner('admitted'), minutes), 'admitted')
            minutes += 2
        self.review(minutes)
        self.assertEqual(self.dig(minutes), {'done': 'usage'})
        self.assertEqual(sum(r['planned'] for r in self.runs()), a.FIRST_DIG_SIGNALS)

    def test_an_install_whose_first_review_was_long_ago_does_not_start_digging(self):
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(60)])
        self.step(Runner('admitted'))
        self.review(2)
        self.assertEqual(self.dig(60 * (a.FIRST_DIG_HOURS + 1)), {'done': 'expired'})

    def test_a_first_review_a_claude_plan_reported_as_failed_is_not_left_hanging(self):
        # 2026-10-27, a hosted Machine on a Claude plan: the quick review and the next one each saved their batch, then
        # the runtime reported the silent NO_REPLY ending as runtime_error (receipts from before silent_end). No
        # review ever ended ok and nothing was left to review, so nothing ran for nine hours; the report said failed.
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(30)])
        self.step(Runner('admitted'))
        with self.assertLogs(a.LOG, 'WARNING'):
            self.review(8, status='error')  # saved, reported failed
        # Signals of the week left: the next batch comes within the backoff, it does not wait for new mail
        self.assertIsNone(self.step(Runner(), 8.5))
        self.assertEqual(self.step(Runner('admitted'), 9.1), 'admitted')
        with self.assertLogs(a.LOG, 'WARNING'):
            self.review(10, status='error')
        # Nothing of the week left: the first review is done, not waiting for its first "ok" forever
        self.assertEqual(self.dig(13), {'done': 'covered'})
        self.assertIsNone(self.step(Runner(), 13))

    def test_a_failed_first_review_comes_back_within_half_an_hour_however_often_it_failed(self):
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(30)])
        self.step(Runner('admitted'))
        minutes, gaps = 0, []
        for _ in range(8):
            with self.assertLogs(a.LOG, 'WARNING'):
                self.review(minutes + 1, status='error', save=False)  # failed before it saved anything
            finished = minutes + 1
            minutes = finished
            while self.step(Runner('admitted'), minutes) != 'admitted':
                minutes += 1
                self.assertLess(minutes - finished, 31)
            gaps.append(minutes - finished)
        self.assertEqual(max(gaps), 30)

    def test_a_usage_limit_holds_the_first_review_until_the_reset_and_says_so(self):
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(30)])
        self.step(Runner('admitted'))
        reset = int(time.time()) + 2 * 3600
        receipt = {'status': 'error', 'error': 'usage_limited', 'error_phase': 'model', 'retry_at': reset}
        self.app.note_usage_limit(receipt)  # what preparation_gateway does with every receipt
        with self.assertLogs(a.LOG, 'WARNING'):
            self.review(2, status='error', save=False, receipt=receipt)
        self.assertEqual(self.runs()[0]['error'], 'usage_limited')
        self.assertIsNone(self.step(Runner(), 40))  # held, not retried every few minutes
        self.assertEqual(self.app.model_pause()['until'], reset)  # the dashboard's banner: limit reached, resets then
        self.app.usage_limit['until'] = time.time() - 1  # the reset came
        self.assertIsNone(self.app.model_pause())
        self.assertEqual(self.step(Runner('admitted'), 121), 'admitted')


if __name__ == '__main__':
    unittest.main()
