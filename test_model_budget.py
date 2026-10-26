"""The usage budget for The Machine's own background turns (model_budget.py and its checks in assistant.py): pausing at
the 5-hour and weekly budget, waiting out a usage limit until it resets, the first look going first, and background work
never on the costliest model. 2026-10-25: a new owner's onboarding spent their 5-hour ChatGPT window in 11 minutes and
then retried every few minutes. No Gateway, no model call, nothing is sent."""
import importlib.util
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import model_budget as b

spec = importlib.util.spec_from_file_location('budget_assistant', Path(__file__).with_name('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

NOW = 1_800_000_000
HOUR, DAY = 3600, 86400


def usage(short=None, week=None, short_reset=NOW + 2 * HOUR, week_reset=NOW + 5 * DAY):
    windows = ([{'label': '5h', 'used': short, 'reset': short_reset}] if short is not None else []) + \
              ([{'label': 'Week', 'used': week, 'reset': week_reset}] if week is not None else [])
    return [{'provider': 'openai', 'name': 'ChatGPT', 'windows': windows}]


class Budget(unittest.TestCase):
    def test_the_5_hour_window_pauses_background_work_with_room_left_for_the_owner(self):
        self.assertIsNone(b.pause(usage(short=64), NOW))
        found = b.pause(usage(short=65), NOW)
        self.assertEqual((found['window'], found['until']), ('5h', NOW + 2 * HOUR))
        self.assertIsNone(b.pause(usage(short=80), NOW, first=True))  # the first look may go further
        self.assertEqual(b.pause(usage(short=85), NOW, first=True)['window'], '5h')
        self.assertIsNone(b.pause(usage(short=99, short_reset=NOW - 1), NOW))  # an old reading of a window that reset

    def test_the_week_is_paced_at_a_seventh_a_day_and_a_quiet_day_carries_over(self):
        # Day 3 of the week (2 days and a bit in): up to 3/7 = 42.9%
        reset = NOW + 4 * DAY + HOUR
        self.assertIsNone(b.pause(usage(week=42, week_reset=reset), NOW))
        found = b.pause(usage(week=43, week_reset=reset), NOW)
        self.assertEqual((found['window'], found['until']), ('week', reset - 4 * DAY))  # until the next day of the week
        self.assertIsNone(b.pause(usage(week=43, week_reset=reset), NOW, first=True))
        self.assertEqual(b.allowed_this_week(NOW + 10, NOW), b.WEEK_CAP)  # the last day: never past the cap
        self.assertEqual(b.pause(usage(week=95), NOW, first=True)['window'], 'week')

    def test_a_sign_in_without_usage_windows_is_never_paused(self):
        self.assertIsNone(b.pause(None, NOW))
        self.assertIsNone(b.pause([{'provider': 'openai', 'windows': []}], NOW))
        self.assertEqual(b.window_kind('168h'), 'week'); self.assertEqual(b.window_kind('5h'), 'short')

    def test_a_usage_limit_holds_until_the_reset_it_named_else_the_windows(self):
        self.assertEqual(b.limit_until(NOW + 600, None, NOW), NOW + 600)
        self.assertEqual(b.limit_until(None, usage(short=100, week=60), NOW), NOW + 2 * HOUR)
        self.assertEqual(b.limit_until(None, usage(short=40, week=100), NOW), NOW + 5 * DAY)
        self.assertEqual(b.limit_until(NOW + 30 * DAY, None, NOW), NOW + b.LIMIT_WAIT)  # not believed


class Runner:
    def __init__(self): self.requests = []
    def __call__(self, request): self.requests.append(request); return {'status': 'admitted'}


class Checks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'work', 'service': 'gmail'}], 'review_worker': {'enabled': True}}
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': f's{n}', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Question', 'body': 'Can you confirm?', 'metadata': {}, 'deleted': False} for n in range(3)])

    def test_reviews_wait_while_the_budget_is_spent_and_the_quick_look_may_go_further(self):
        self.app.model_usage = usage(short=70, short_reset=time.time() + HOUR)
        runner = Runner()
        self.assertEqual(self.app.review_step(runner), 'admitted')  # the quick first review is the first magic
        with self.store.connect() as db:
            db.execute("UPDATE review_runs SET status='ok',finished_at='2000-01-01T00:00:00+00:00'")
            db.execute("UPDATE events SET analyzed_version=0")
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': f'n{n}', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'New', 'body': 'Hi', 'metadata': {}, 'deleted': False} for n in range(50)])
        runner = Runner()
        self.assertIsNone(self.app.review_step(runner))
        self.assertEqual(runner.requests, [])
        self.app.model_usage = usage(short=30, short_reset=time.time() + HOUR)
        self.assertEqual(self.app.review_step(runner), 'admitted')

    def test_a_usage_limit_a_run_hit_holds_everything_until_it_resets(self):
        until = int(time.time()) + 2 * HOUR
        self.assertEqual(self.app.note_usage_limit({'status': 'error', 'error': 'usage_limited', 'retry_at': until}), until)
        self.assertEqual(self.app.background_pause(owner=True), {'window': 'limit', 'until': until, 'limited': True})
        self.assertIsNone(self.app.review_step(Runner()))
        self.app.config['openclaw_config'] = str(Path(self.temp.name) / 'openclaw.json')
        Path(self.app.config['openclaw_config']).write_text(json.dumps({'agents': {'defaults': {'model': 'openai/gpt-6.1-sol'}}}))
        self.assertEqual(self.app.model_pause(), {'window': 'limit', 'until': until, 'name': 'ChatGPT'})
        # A card the owner accepted waits too, in its place, and starts once the limit lifts
        sid = self.store.suggest('task', 'Reply to Sam', 'I can draft it.', [1])['id']
        self.store.decide(sid, 'accept', '', 'click', 'dashboard')
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        self.assertEqual(calls, [])
        self.app.usage_limit = None
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        self.assertEqual([c['action'] for c in calls], ['start'])

    def test_a_preparation_that_hits_the_usage_limit_waits_for_the_reset_without_using_its_retry(self):
        sid = self.store.suggest('task', 'Reply to Sam', 'I can draft it.', [1])['id']
        self.store.decide(sid, 'accept', '', 'click', 'dashboard')
        self.app.preparation_step(lambda r: {'status': 'admitted'})
        self.app.usage_limit = {'until': int(time.time()) + HOUR, 'at': int(time.time())}
        self.app.preparation_step(lambda r: {'status': 'error', 'error': 'usage_limited'})
        with self.store.connect() as db:
            row = dict(db.execute('SELECT status,error,auto_retries,retry_at FROM preparations WHERE suggestion_id=?', (sid,)).fetchone())
        self.assertEqual((row['status'], row['error'], row['auto_retries']), ('queued', 'usage_limited', 0))
        self.assertGreater(row['retry_at'], a.now())

    def test_drafts_prepared_ahead_go_one_at_a_time_after_the_first(self):
        made = [self.app.action('suggest', {'dedupe_key': f'k{n}', 'title': f'Reply {n}', 'body': 'I can draft it.', 'event_ids': [1],
                                            'when': 'now', 'prepare_ahead': True})['id'] for n in range(3)]
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        self.assertEqual(len(calls), 1)  # the first magic: one draft at once
        self.assertTrue(calls[0]['background'])
        calls.clear()
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at) VALUES('first_card_shown',?)", (a.now(),))
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'pending'})
        self.assertNotIn('start', [c['action'] for c in calls])  # the next one waits for the gap
        self.app.background_at = time.time() - a.BACKGROUND_GAP_SECONDS
        calls.clear()
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted' if r['action'] == 'start' else 'pending'})
        self.assertEqual([c['action'] for c in calls].count('start'), 1)
        self.assertEqual(len(made), 3)

    def test_background_turns_never_run_on_the_costliest_model(self):
        path = Path(self.temp.name) / 'openclaw.json'
        self.app.config['openclaw_config'] = str(path)
        path.write_text(json.dumps({'agents': {'defaults': {'model': {'primary': 'openai/gpt-6-astra'}}}}))
        self.assertEqual(a.background_model(self.app.config), ('openai', 'gpt-6.1-sol'))
        path.write_text(json.dumps({'agents': {'defaults': {'model': 'openai/gpt-6-astra', 'models': {'openai/gpt-6-astra': {}}}}}))
        self.assertIsNone(a.background_model(self.app.config))  # the owner's allowlist doesn't have it: theirs
        path.write_text(json.dumps({'agents': {'defaults': {'model': 'openai/gpt-6.1-sol'}}}))
        self.assertIsNone(a.background_model(self.app.config))
        path.write_text(json.dumps({'agents': {'defaults': {'model': 'openai/gpt-6-astra'}}}))
        sent = []
        def run(command, input=None, **kw):
            sent.append(json.loads(input))
            return type('R', (), {'returncode': 0, 'stdout': json.dumps({'status': 'error', 'error': 'usage_limited', 'retry_at': int(time.time()) + 900})})()
        with patch.object(a.subprocess, 'run', side_effect=run):
            self.app.preparation_gateway({'kind': 'review', 'action': 'start', 'job_id': 'a' * 32, 'message': 'x'})
            self.app.preparation_gateway({'kind': 'preparation', 'action': 'start', 'job_id': 'b' * 32, 'message': 'x'})
        self.assertEqual((sent[0]['provider'], sent[0]['model']), ('openai', 'gpt-6.1-sol'))
        self.assertNotIn('model', sent[1])  # a card the owner asked for runs on their own model
        self.assertTrue(self.app.background_pause(owner=True)['limited'])


if __name__ == '__main__':
    unittest.main()
