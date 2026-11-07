"""The first review digs until it has something to show. It starts with the week's most promising signals (whatever
their age within the week, no 48-hour cutoff), then goes on a batch at a time, at once, until it has FIRST_DIG_CARDS
to-dos, has looked through the week, or used FIRST_DIG_USAGE percent of the 5-hour window (FIRST_DIG_SIGNALS signals
on a sign-in without usage windows). A failed first review comes back within the backoff (at most half an hour), also
when its runtime reported a failure after the work was saved; a usage limit holds it until the reset. No Gateway,
nothing is sent."""
import datetime as dt, importlib.util, tempfile, time, unittest
from pathlib import Path
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402

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
            p = patch_everywhere(a, name, return_value=value); p.start(); self.addCleanup(p.stop)
        self.app.model_usage = None  # an API key or a sign-in that reports no windows, unless a test sets them

    def later(self, minutes):
        return patch_everywhere(a, 'now', return_value=(dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=minutes)).isoformat(timespec='seconds'))

    def step(self, runner, minutes=0):
        with self.later(minutes):
            return self.app.review_step(runner)

    def runs(self):
        with self.store.connect() as db: return [dict(r) for r in db.execute('SELECT * FROM review_runs ORDER BY started_at')]

    def review(self, minutes, cards=0, status='ok', save=True, receipt=None, counted=None):
        """The running review sees its batch, saves `cards` to-dos (each one shows at once) and saves the batch (or not),
        then ends with `status` (`counted`: what the run counts as, when not that)."""
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
        self.assertEqual(self.step(Runner(receipt or status), minutes), counted or status)
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
        # who waits on the owner first: the one waiting longest leads (its draft is ready on arrival), then newest first
        self.assertEqual(order[:3], ['ask2', 'ask0', 'ask1'])
        self.assertNotIn('old', order)  # never past the week

    def test_a_quick_review_with_no_to_do_digs_on_at_once_until_the_week_is_looked_through(self):
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(45)])
        self.step(Runner('admitted'))
        self.review(2)  # nothing found
        # The next batch at once: no gap, no waiting for 40 signals or for the oldest to wait an hour
        self.assertEqual(self.step(Runner('admitted'), 2), 'admitted')
        nxt = self.runs()[1]
        self.assertEqual((nxt['window_hours'], nxt['budget'], nxt['promising'], nxt['planned']), (None, a.FIRST_LOOK_NEXT_SIGNALS, 1, 25))
        self.review(4)
        self.assertEqual(self.dig(4), {'done': 'covered'})  # (b) the whole week looked through
        self.assertIsNone(self.step(Runner(), 5))
        with self.store.connect() as db:
            self.assertEqual(a.first_cards_report(db, self.app.config['accounts'])['dig'], 'covered')

    def test_the_dashboard_sees_one_count_over_the_week_also_between_batches(self):
        # 2026-11-04: a small Outlook mailbox showed "0 of 20 signals", then the sleepy All clear while the first look
        # was still digging, a batch at a time: between batches nothing said it was still looking
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(70)])
        with self.store.connect() as db:
            self.assertIsNone(self.app.first_dig_live(db))  # no first look yet
        self.step(Runner('admitted'))
        with self.store.connect() as db:
            live = self.app.first_dig_live(db)
        self.assertEqual((live['read'], live['total'], live['todos'], live['goal'], live['pace']),
                         (0, 70, 0, a.FIRST_DIG_CARDS, a.FIRST_DIG_PACE_SECONDS))
        self.review(2)
        with self.later(2), self.store.connect() as db:  # between batches: still digging, the count kept
            live = self.app.first_dig_live(db)
        self.assertEqual((live['read'], live['total'], live['todos']), (20, 70, 0))
        self.assertGreaterEqual(live['pace'], 1)
        with self.later(2):
            self.assertEqual(self.app.review_live()['first_dig']['read'], 20)
        self.step(Runner('admitted'), 2)
        self.review(4, cards=3)
        with self.later(4), self.store.connect() as db:  # found its to-dos: it stopped, the dashboard shows the ending
            self.assertIsNone(self.app.first_dig_live(db))
            self.assertEqual(self.app.first_dig(db), {'done': 'cards'})

    def test_the_rest_of_the_week_up_to_half_a_batch_more_goes_in_one_batch(self):
        # 2026-11-04: 106 signals went as 20, 40, 40 and 6; the batch of 6 still took a whole turn and its start (51 s)
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n / 2 + 1) for n in range(a.QUICK_LOOK_SIGNALS + a.FIRST_LOOK_NEXT_SIGNALS + a.FIRST_LOOK_TAIL_SIGNALS)])
        self.step(Runner('admitted'))
        self.review(2)
        self.step(Runner('admitted'), 2)
        nxt = self.runs()[1]
        self.assertEqual((nxt['planned'], nxt['budget']), (60, 60))  # all that is left, not 40 and then 20
        claim = self.store.begin_analysis(['work'], 120, a.REVIEW_SESSION_PREFIX + nxt['run_id'], nxt['run_id'])
        self.assertEqual(len(claim['events']), 60)
        # one more than that: batches of 40 as before
        self.assertEqual(a.first_look_batch(a.FIRST_LOOK_NEXT_SIGNALS + a.FIRST_LOOK_TAIL_SIGNALS + 1), a.FIRST_LOOK_NEXT_SIGNALS)
        self.assertEqual(a.first_look_batch(5), a.FIRST_LOOK_NEXT_SIGNALS)

    def test_the_live_first_look_names_who_it_reads_about_and_its_first_to_do(self):
        # The live first look: a few names from the batch it reads now (as the Graph knows them, never the owner or an
        # address), whether it reads only mail, and the first to-do's title once saved. Never a word of a message.
        people = [mail('a1', 'Mila Hart <mila@acme-freight.example>', 1), mail('a2', 'Jonah Reyes <jonah@example.org>', 2),
                  mail('a3', 'noreply@shop.example', 3), mail('own', 'Robin <me@example.com>', 4)]
        people[3]['metadata']['to'] = 'Caspian <caspian@example.net>'
        self.store.commit_page('work', {}, people + [mail(f'm{n}', f'P{n} Lane <p{n}@example.org>', hours_ago=n + 5) for n in range(30)])
        with self.store.connect() as db:
            db.isolation_level = None
            a.graph.build(db, self.app.config, a.now())
        self.step(Runner('admitted'))
        with self.store.connect() as db:
            live = self.app.first_dig_live(db)
        self.assertEqual((live['unit'], live['names'], live['first']), ('email', [], None))  # nothing claimed yet
        run = self.runs()[-1]
        claim = self.store.begin_analysis(['work'], 120, a.REVIEW_SESSION_PREFIX + run['run_id'], run['run_id'])
        with self.store.connect() as db:
            live = self.app.first_dig_live(db)
        self.assertLessEqual(len(live['names']), a.FIRST_LOOK_NAMES)
        self.assertTrue({'Mila', 'Jonah'} <= set(live['names']), live['names'])
        for name in live['names']:
            self.assertNotIn('@', name)
            self.assertNotIn(name, ('Robin', 'Caspian', 'noreply', 'Hello', 'Text'))  # never the owner, whom they wrote to, an address or the message
        ids = [e['id'] for e in claim['events']]
        self.store.suggest('first-1', 'Send Mila the pricing sheet', 'Mila asked.', [ids[0]])
        with self.store.connect() as db:
            live = self.app.first_dig_live(db)
        self.assertEqual((live['todos'], live['first']['title']), (1, 'Send Mila the pricing sheet'))
        self.assertNotIn('Mila asked.', str(live))
        self.app.config['accounts'].append({'id': 'chat', 'service': 'telegram'})
        with self.store.connect() as db:
            self.assertEqual(self.app.first_dig_live(db)['unit'], 'message')

    def test_the_bar_moves_at_the_last_batchs_time_over_the_batch_that_runs(self):
        # A batch takes about as long whatever its size (its steps, not its signals): 2026-11-04, 20 signals took 135 s and
        # 40 took 91 s, while the bar went on at the first batch's 9 s a signal and stood far behind
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n / 2 + 1) for n in range(150)])
        self.step(Runner('admitted'))
        self.review(2)  # the quick batch of 20 took 2 minutes
        self.step(Runner('admitted'), 2)
        with self.later(2), self.store.connect() as db:
            self.assertEqual(self.app.first_dig_live(db)['pace'], 3)  # 120 s over the 40 of the batch that runs

    def test_the_worker_looks_often_while_the_first_look_runs_and_starts_its_next_batch_at_once(self):
        self.assertEqual(self.app.review_tick(), a.REVIEW_TICK_SECONDS)  # nothing to watch
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n / 2 + 1) for n in range(150)])
        self.step(Runner('admitted'))
        self.assertEqual(self.app.review_tick(), a.FIRST_LOOK_TICK_SECONDS)  # its quick batch runs
        self.review(2)
        self.assertEqual(self.app.review_tick(), a.FIRST_LOOK_TICK_SECONDS)  # between batches, still digging
        waits, steps, others = [], [], []
        class Stop:
            def wait(self, seconds):
                waits.append(seconds)
                return len(waits) > 2
        self.app.stop = Stop()
        results = iter(['ok', 'admitted', 'running'])
        self.app.review_step = lambda: steps.append(1) or next(results)
        for name in ('profile_step', 'first_profile_step', 'orgs_backfill_step', 'share_history_step', 'recap_step'):
            setattr(self.app, name, lambda name=name: others.append(name))
        self.app.review_worker()
        self.assertEqual(waits[:2], [a.FIRST_LOOK_TICK_SECONDS] * 2)
        self.assertEqual(len(steps), 3)  # a batch ended: the next one started in the same round, then checked a tick later
        self.assertEqual(others.count('profile_step'), 1)  # the other steps keep their own 15 s
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at,detail) VALUES('first_dig_done',?,'cards')", (a.now(),))
            db.execute("UPDATE review_runs SET status='ok',finished_at=?", (a.now(),))
        self.assertEqual(self.app.review_tick(), a.REVIEW_TICK_SECONDS)  # done digging: back to the usual pace

    def test_the_first_looks_reviewer_is_asked_to_keep_its_steps_few(self):
        prompt = a.review_prompt('r1', ['work'], first_look=True)
        self.assertIn('call status and begin_analysis in one step', prompt)
        self.assertIn('Save each to-do with suggest as soon as it is checked', prompt)
        self.assertNotIn('call status and begin_analysis in one step', a.review_prompt('r1', ['work']))

    def test_a_batch_saved_while_its_run_still_ends_keeps_the_total(self):
        # 2026-11-04: "20 of 82 signals", then "22 of 102": a saved batch had left the week's unread signals while
        # its run had not ended yet, so it was in neither count for a moment
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(70)])
        self.step(Runner('admitted'))
        run = self.runs()[-1]
        claim = self.store.begin_analysis(['work'], 120, a.REVIEW_SESSION_PREFIX + run['run_id'], run['run_id'])
        ids = [e['id'] for e in claim['events']]
        with self.store.connect() as db:
            db.execute('UPDATE events SET analyzed_version=version WHERE id IN (' + ','.join('?' * len(ids)) + ')', ids)
            db.execute("UPDATE analyses SET status='complete',finished_at=? WHERE id=?", (a.now(), claim['analysis_id']))
            self.assertEqual(db.execute('SELECT status FROM review_runs WHERE run_id=?', (run['run_id'],)).fetchone()[0], 'running')
            live = self.app.first_dig_live(db)
        self.assertEqual((live['read'], live['total']), (20, 70))

    def test_a_big_week_counts_toward_the_first_looks_share_not_the_whole_week(self):
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n / 4 + 1) for n in range(500)])
        self.step(Runner('admitted'))
        with self.store.connect() as db:
            self.assertEqual(self.app.first_dig_live(db)['total'], a.FIRST_DIG_SIGNALS)

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
        for _ in range((a.FIRST_DIG_SIGNALS - a.QUICK_LOOK_SIGNALS) // a.FIRST_LOOK_NEXT_SIGNALS):
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
        # A first look's batch that was saved is a finished pass now, whatever the runtime said after it.
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(30)])
        self.step(Runner('admitted'))
        with self.assertLogs(a.LOG, 'WARNING') as logs:
            self.review(8, cards=1, status='error', counted='ok')  # saved, reported failed
        self.assertIn('error=runtime_error phase=runtime saved_claims=1 counted=ok', logs.output[-1])
        first = self.runs()[0]
        self.assertEqual((first['status'], first['error'], first['last_error']), ('ok', None, 'runtime_error'))
        with self.store.connect() as db:  # the error class still reaches the error reports
            self.assertEqual(db.execute("SELECT kind FROM error_feed WHERE source='review'").fetchall()[0][0], 'runtime_error')
        # Signals of the week left: the next batch comes at once, no backoff as after a failure
        self.assertEqual(self.step(Runner('admitted'), 8), 'admitted')
        with self.assertLogs(a.LOG, 'WARNING'):
            self.review(10, status='error', counted='ok')
        # Nothing of the week left: the first review is done, and the report says the quick look went well
        self.assertEqual(self.dig(13), {'done': 'covered'})
        self.assertIsNone(self.step(Runner(), 13))
        with self.store.connect() as db:
            report = a.first_cards_report(db, self.app.config['accounts'])
        self.assertEqual((report['quick']['status'], report['quick']['cards'], report['cards']), ('ok', 1, 1))

    def test_a_first_look_pass_that_fails_after_saving_to_dos_keeps_them(self):
        # The to-dos a failed pass saved stay on the list; the pass is tried again only for what it did not save
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(30)])
        self.step(Runner('admitted'))
        run = self.runs()[-1]
        with self.later(2):
            claim = self.store.begin_analysis(['work'], 120, a.REVIEW_SESSION_PREFIX + run['run_id'], run['run_id'])
            self.store.suggest('kept-1', 'Reply to Sam', 'Asked.', [claim['events'][0]['id']])
        with self.assertLogs(a.LOG, 'WARNING'):
            self.assertEqual(self.step(Runner('error'), 3), 'error')  # its batch not saved: a real failure
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT status FROM suggestions WHERE dedupe_key='kept-1'").fetchone()[0], 'pending')
            self.assertEqual(db.execute("SELECT status FROM analyses").fetchone()[0], 'retryable')
            self.assertEqual(a.first_cards_report(db, self.app.config['accounts'])['cards'], 1)

    def test_a_regular_review_that_fails_after_saving_stays_a_failure(self):
        # Only the first look's passes count as finished that way; afterwards a failure stays one (backoff, ops alert)
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at,detail) VALUES('first_dig_done',?,'cards')", (a.now(),))
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(45)])
        self.step(Runner('admitted'))
        with self.assertLogs(a.LOG, 'WARNING'):
            self.review(2, status='error')
        self.assertEqual((self.runs()[0]['status'], self.runs()[0]['error']), ('error', 'runtime_error'))

    def test_a_first_look_that_keeps_failing_says_so(self):
        # The dashboard's first look: "Reading on" while it works, the backoff's "tries again shortly" after a failure,
        # and from the third failure in a row a line that says the tries keep failing (first_dig_live.failing)
        self.store.commit_page('work', {}, [mail(f'm{n}', hours_ago=n + 1) for n in range(30)])
        self.step(Runner('admitted'))
        minutes = 0
        for n in range(1, 4):
            with self.assertLogs(a.LOG, 'WARNING'):
                self.review(minutes + 1, status='error', save=False)
            with self.later(minutes + 1), self.store.connect() as db:
                self.assertEqual(self.app.first_dig_live(db)['failing'], n)
            minutes += 1
            while self.step(Runner('admitted'), minutes) != 'admitted':
                minutes += 1
                self.assertLess(minutes, 60)
        self.review(minutes + 1)  # it went well: the line goes
        with self.later(minutes + 1), self.store.connect() as db:
            self.assertEqual(self.app.first_dig_live(db)['failing'], 0)

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
