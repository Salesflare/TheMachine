"""The review worker's own word on whether reviews of new signals wait by design, kept for the hosting agent
(machine/store/review_pause.py): the same answer for every kind of sign-in. A hosted Machine on a Claude plan got a
stall alert while its reviews may only have paced: the usage windows of that plan are known to the app alone."""
import datetime as dt
import json
import sqlite3
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant as a
from machine.app import model_pacing
from machine.store import review_pause
from machine.upkeep import memory_rebuild
import model_fallback
from seams import patch_everywhere
import timeutil

HOUR, DAY = 3600, 86400
NOW = int(time.time())


def claude(short, week=10):
    stamp = lambda s: dt.datetime.fromtimestamp(s, dt.timezone.utc).isoformat()
    return {'rate_limits_available': True, 'rate_limits': {
        'five_hour': {'utilization': short, 'resets_at': stamp(NOW + 2 * HOUR)},
        'seven_day': {'utilization': week, 'resets_at': stamp(NOW + 4 * DAY)}}}


def provider(name, short, week=10):
    return {'provider': name, 'windows': [{'label': '5h', 'usedPercent': short, 'resetAt': (NOW + 2 * HOUR) * 1000},
                                          {'label': 'Week', 'usedPercent': week, 'resetAt': (NOW + 4 * DAY) * 1000}]}


class Runner:
    def __call__(self, request):
        return {'status': 'admitted'}


class ReviewPause(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'events.sqlite'
        self.store = a.Store(self.path)
        self.openclaw = Path(self.temp.name) / 'openclaw.json'
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'work', 'service': 'gmail'}], 'review_worker': {'enabled': True},
                           'codex': False, 'openclaw_config': str(self.openclaw)}
        self.app._fallback_health = model_fallback.Health(lambda config, model: True)
        with self.store.connect() as db:  # past the first look: regular reviews of new signals
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,finished_at) VALUES('a','ok',?,?,'2000-01-01T00:00:00+00:00')", (a.now(), a.now()))
            db.execute("INSERT INTO milestones(name,at,detail) VALUES('first_dig_done',?,'cards')", (a.now(),))
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': f'n{n}', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'New', 'body': 'Private words', 'metadata': {}, 'deleted': False} for n in range(50)])

    def signed_in(self, model, status=(), claude_usage=None, fallbacks=()):
        """The AI sign-in as the usage worker reads it: OpenClaw's usage.status and, on a Claude plan, Claude Code's."""
        self.openclaw.write_text(json.dumps({'agents': {'defaults': {'model': {'primary': model, 'fallbacks': list(fallbacks)}}}}))
        with patch.object(model_pacing, 'usage_status', lambda config: {'providers': list(status)}), \
                patch('machine.model_usage.claude_code_usage', lambda config: claude_usage), \
                patch.object(model_pacing.ai_training, 'claude_plan', lambda config: 'pro'):
            self.app.refresh_model_usage()

    def report(self):
        db = sqlite3.connect(self.path)  # as the agent: another process, a plain connection
        try:
            return review_pause.report(db)
        finally:
            db.close()

    def step(self, window, until=None):
        self.assertEqual(self.app.review_step(Runner()), None if window else 'admitted')
        found = self.report()
        self.assertEqual((found['window'], found['until']), (window, until))
        with self.store.connect() as db:
            db.execute("UPDATE review_runs SET status='ok',finished_at='2000-01-01T00:00:00+00:00'")
        return found

    def test_a_claude_plan_through_claude_code(self):
        self.signed_in('claude-cli/claude-opus-5-5', claude_usage=claude(66))
        found = self.step('5h', NOW + 2 * HOUR)
        self.assertEqual(set(found), {'window', 'until', 'since', 'checked_at'})
        self.signed_in('claude-cli/claude-opus-5-5', claude_usage=claude(64, 91))
        self.step('week', NOW + 4 * DAY)
        self.signed_in('claude-cli/claude-opus-5-5', claude_usage=claude(64, 89))
        self.step(None)

    def test_the_claude_plan_is_read_again_through_the_anthropic_names_claude_code_runs(self):
        self.signed_in('anthropic/claude-opus-5-5')
        self.openclaw.write_text(json.dumps({'agents': {'defaults': {'model': {'primary': 'anthropic/claude-opus-5-5'},
                                                                     'models': {'anthropic/*': {'agentRuntime': {'id': 'claude-cli'}}}}}}))
        with patch.object(model_pacing, 'usage_status', lambda config: {'providers': []}), \
                patch('machine.model_usage.claude_code_usage', lambda config: claude(70)), \
                patch.object(model_pacing.ai_training, 'claude_plan', lambda config: 'pro'):
            self.app.refresh_model_usage()
        self.step('5h', NOW + 2 * HOUR)

    def test_claude_code_that_says_nothing_does_not_pause(self):
        self.signed_in('claude-cli/claude-opus-5-5')
        self.step(None)

    def test_claude_through_openclaw_s_anthropic_provider(self):
        self.signed_in('anthropic/claude-opus-5-5', [provider('anthropic', 70)])
        self.step('5h', NOW + 2 * HOUR)

    def test_chatgpt_and_another_provider_s_windows_do_not_count(self):
        self.signed_in('openai/gpt-6.1-sol', [provider('openai-codex', 70), provider('anthropic', 5)])
        self.step('5h', NOW + 2 * HOUR)
        self.signed_in('anthropic/claude-opus-5-5', [provider('openai-codex', 70), provider('anthropic', 5)])
        self.step(None)

    def test_an_api_key_is_never_paused(self):
        self.signed_in('openai/gpt-6.1-sol')
        self.step(None)

    def test_a_usage_limit_a_run_hit_with_no_windows_known(self):
        self.signed_in('openai/gpt-6.1-sol')
        until = self.app.note_usage_limit({'status': 'error', 'error': 'usage_limited'})
        self.step('limit', until)
        self.app.usage_limit = None
        self.step(None)

    def test_a_full_window(self):
        self.signed_in('claude-cli/claude-opus-5-5', claude_usage=claude(100))
        self.step('5h', NOW + 2 * HOUR)

    def test_a_working_fallback_carries_the_reviews(self):
        self.signed_in('claude-cli/claude-opus-5-5', claude_usage=claude(70), fallbacks=['openai/gpt-6.1-sol'])
        self.step('5h', NOW + 2 * HOUR)
        self.assertEqual(self.app.check_fallback(), 'openai/gpt-6.1-sol')
        self.step(None)

    def test_the_quiet_night_for_the_memory_rebuild(self):
        self.signed_in('openai/gpt-6.1-sol')
        memory_rebuild.write_state(Path(self.temp.name), {'opened': time.time(), 'until': NOW + HOUR, 'jobs': []})
        self.step('memory', NOW + HOUR)

    def test_the_night_pause(self):
        self.signed_in('openai/gpt-6.1-sol')
        until = dt.datetime.fromtimestamp(NOW + 3 * HOUR, dt.timezone.utc)
        with patch.object(a.App, 'night_hold', lambda app, db, current=None: until):
            self.step('night', NOW + 3 * HOUR)
        self.step(None)

    def test_the_owner_s_review_now_ends_it(self):
        self.signed_in('claude-cli/claude-opus-5-5', claude_usage=claude(70))
        self.step('5h', NOW + 2 * HOUR)
        self.app.action('review_now', {}, owner_dashboard=True)
        self.step(None)

    def test_since_stays_while_the_same_pause_goes_on_and_the_last_look_is_kept_fresh(self):
        clock = [dt.datetime(2026, 11, 24, 9, tzinfo=dt.timezone.utc)]
        start, end = clock[0].isoformat(), int(clock[0].timestamp()) + 2 * HOUR

        def look(found, minutes=0):
            clock[0] += dt.timedelta(minutes=minutes)
            with self.store.connect() as db:
                review_pause.note(db, found)
            return self.report()
        with patch_everywhere(timeutil, 'now', new=lambda: clock[0].isoformat()):
            self.assertIsNone(self.report())  # an app that never looked says nothing
            self.assertEqual(look({'window': '5h', 'until': end}), {'window': '5h', 'until': end, 'since': start, 'checked_at': start})
            self.assertEqual(look({'window': '5h', 'until': end}, 2)['checked_at'], start)  # unchanged: not written every minute
            found = look({'window': '5h', 'until': end}, 9)
            self.assertEqual((found['since'], found['checked_at']), (start, clock[0].isoformat()))
            self.assertEqual(look({'window': '5h', 'until': end + 60}, 1)['since'], start)  # a reset read a minute later
            self.assertEqual(look({'window': '5h', 'until': end + 5 * HOUR}, 1)['since'], clock[0].isoformat())  # the next window
            self.assertEqual(look({'window': 'week', 'until': None}, 1), {'window': 'week', 'until': None, 'since': clock[0].isoformat(),
                                                                          'checked_at': clock[0].isoformat()})
            week = clock[0].isoformat()
            self.assertEqual(look({'window': 'week', 'until': None}, 120)['since'], week)  # no reset known: since stays
            self.assertEqual(look(None, 1), {'window': None, 'until': None, 'since': None, 'checked_at': clock[0].isoformat()})
            self.assertEqual(look({'window': 'week', 'until': None}, 1)['since'], clock[0].isoformat())

    def test_a_row_that_can_t_be_read_says_nothing(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at,detail) VALUES('review_pause',?,'not json')", (a.now(),))
        self.assertIsNone(self.report())
        self.signed_in('openai/gpt-6.1-sol')
        self.step(None)


if __name__ == '__main__':
    unittest.main()
