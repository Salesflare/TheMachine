"""A working fallback billed apart from the main model sets the usage rules aside (model_fallback.py and its checks in
assistant.py): no pacing, no waiting for a reached limit, one short line on top; a fallback that fails, or a run that
still ended on the limit, brings the rules back. 2026-10-31: teammates' hosted Machines paused at 65% of the ChatGPT
5-hour window although their pay-per-use fallback could carry the work. No Gateway, no model call."""
import importlib.util
import json
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

import model_budget
import model_fallback as f

spec = importlib.util.spec_from_file_location('fallback_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

HOUR = 3600


def usage(short, week=10):
    now_s = time.time()
    return [{'provider': 'openai', 'name': 'ChatGPT', 'windows': [{'label': '5h', 'used': short, 'reset': now_s + 2 * HOUR},
                                                                  {'label': 'Week', 'used': week, 'reset': now_s + 5 * 86400}]}]


class Answer:
    def __init__(self, returncode=0, stdout=''):
        self.returncode, self.stdout = returncode, stdout


class Module(unittest.TestCase):
    def test_only_fallbacks_billed_apart_count(self):
        fallbacks = ['openai-codex/gpt-6.1-sol', 'work-api/gpt-6.1-sol', 'ollama/glm-5.3-flash']
        self.assertEqual(f.separate('openai/gpt-6.1-sol', fallbacks), ['work-api/gpt-6.1-sol', 'ollama/glm-5.3-flash'])
        self.assertEqual(f.separate('claude-cli/opus', ['anthropic/claude-opus', 'openai/gpt-6.1-sol']), ['openai/gpt-6.1-sol'])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, 'openclaw.json')
            path.write_text(json.dumps({'agents': {'defaults': {'model': {'primary': 'openai/gpt-6.1-sol', 'fallbacks': fallbacks}}}}))
            self.assertEqual(f.configured({'openclaw_config': str(path)}), ('openai/gpt-6.1-sol', fallbacks))
            path.write_text(json.dumps({'agents': {'defaults': {'model': 'openai/gpt-6.1-sol'}}}))
            self.assertEqual(f.configured({'openclaw_config': str(path)}), ('openai/gpt-6.1-sol', []))
            self.assertEqual(f.configured({'openclaw_config': str(Path(tmp, 'missing.json'))}), ('', []))

    def test_the_check_is_one_strict_tiny_turn_on_the_fallback_alone(self):
        seen = {}

        def run(args, **kw):
            seen['args'] = args
            return Answer(0, json.dumps({'ok': True, 'provider': 'work-api', 'outputs': [{'text': 'OK'}]}))
        self.assertTrue(f.probe({'openclaw': 'oc'}, 'work-api/gpt-6.1-sol', run))
        self.assertEqual(seen['args'], ['oc', 'infer', 'model', 'run', '--gateway', '--json', '--model', 'work-api/gpt-6.1-sol',
                                        '--prompt', f.PROMPT])
        self.assertFalse(f.probe({}, 'x/y', lambda *_, **__: Answer(1, json.dumps({'ok': False, 'error': {'message': 'Unknown model'}}))))
        self.assertFalse(f.probe({}, 'x/y', lambda *_, **__: Answer(0, json.dumps({'ok': True, 'outputs': []}))))

        def slow(*_, **__):
            raise subprocess.TimeoutExpired('oc', 1)
        self.assertFalse(f.probe({}, 'x/y', slow))

    def test_health_counts_a_recent_pass_until_something_fails_and_never_checks_too_often(self):
        answers = [True]
        calls = []
        health = f.Health(lambda config, model: calls.append(model) or answers[-1])
        now_s = time.time()
        self.assertIsNone(health.working(['b/x'], now_s))  # never checked: the rules apply
        self.assertEqual(health.refresh({}, ['b/x'], now_s), 'b/x')
        self.assertEqual(health.working(['b/x']), 'b/x')
        self.assertIsNone(health.working(['b/x'], time.time() + f.OK_SECONDS + 1))  # too old
        self.assertEqual(health.refresh({}, ['b/x']), 'b/x')
        self.assertEqual(calls, ['b/x'])  # still fresh: not checked again
        health.doubt()
        self.assertIsNone(health.working(['b/x']))
        self.assertIsNone(health.refresh({}, ['b/x']))  # checked within CHECK_GAP: waits
        answers.append(False)
        self.assertIsNone(health.refresh({}, ['b/x'], time.time() + f.CHECK_GAP + 1))
        self.assertEqual(calls, ['b/x', 'b/x'])
        self.assertIsNone(health.working(['b/x']))  # failing: the rules are back
        # The next fallback in the chain carries it instead
        answers.append(True)
        self.assertEqual(health.refresh({}, ['b/x', 'c/y'], time.time() + f.CHECK_GAP + 2), 'c/y')


class App(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        path = Path(self.tmp.name, 'openclaw.json')
        path.write_text(json.dumps({'agents': {'defaults': {'model': {'primary': 'openai/gpt-6.1-sol',
                                                                       'fallbacks': ['work-api/gpt-6.1-sol']}}}}))
        self.app = object.__new__(a.App)
        self.app.config = {'openclaw_config': str(path), 'review_worker': {'enabled': True}}
        self.app.usage_limit = None
        self.checks = []
        self.answer = True
        self.app._fallback_health = f.Health(lambda config, model: self.checks.append(model) or self.answer)

    def tearDown(self):
        self.tmp.cleanup()

    def test_without_a_working_fallback_the_usage_rules_hold(self):
        self.app.model_usage = usage(70)
        self.assertEqual(self.app.background_pause()['window'], '5h')
        self.assertTrue(self.app.follow_up_pause())
        self.assertTrue(self.app.history_paced())
        self.app.model_usage = usage(100)
        self.assertTrue(self.app.background_pause(owner=True)['limited'])
        self.assertNotIn('fallback', self.app.model_pause())

    def test_a_working_fallback_sets_pacing_and_reached_limits_aside(self):
        self.app.model_usage = usage(70, week=95)
        self.assertEqual(self.app.check_fallback(), 'work-api/gpt-6.1-sol')
        self.assertEqual(self.checks, ['work-api/gpt-6.1-sol'])
        self.assertIsNone(self.app.background_pause())
        self.assertIsNone(self.app.background_pause(first=True))
        self.assertIsNone(self.app.background_pause(signals=True))
        self.assertIsNone(self.app.follow_up_pause())
        self.assertFalse(self.app.history_paced())
        self.assertTrue(self.app.model_room())
        self.assertIsNone(self.app.short_window())  # the first review counts signals instead of the window
        self.app.review_paused = {'window': '5h', 'until': time.time() + HOUR, 'limited': False}
        self.assertIsNone(self.app.review_pause())
        # The limit reached: work goes on (OpenClaw answers with the fallback), and the banner says so in one line
        self.app.model_usage = usage(100)
        self.app.model_status = {'limit_reached': True, 'limit_resets_at': int(time.time()) + HOUR}
        self.assertIsNone(self.app.background_pause(owner=True))
        self.assertEqual(self.app.model_pause(), {'window': 'limit', 'until': self.app.model_status['limit_resets_at'],
                                                  'name': 'ChatGPT', 'fallback': True})

    def test_a_run_that_still_hit_the_limit_or_a_failing_fallback_brings_the_rules_back(self):
        self.app.model_usage = usage(100)
        self.app.check_fallback()
        self.assertIsNone(self.app.background_pause(owner=True))
        until = int(time.time()) + HOUR
        self.app.note_usage_limit({'status': 'error', 'error': 'usage_limited', 'retry_at': until})
        self.assertEqual(self.app.background_pause(owner=True), {'window': 'limit', 'until': until, 'limited': True})
        self.assertIsNone(self.app.check_fallback())  # checked a moment ago: not again within CHECK_GAP
        self.assertEqual(len(self.checks), 1)
        self.app._fallback_health.seen['work-api/gpt-6.1-sol']['tried'] -= model_fallback_gap()
        self.answer = False
        self.assertIsNone(self.app.check_fallback())
        self.assertTrue(self.app.background_pause(owner=True)['limited'])
        self.answer = True
        self.app._fallback_health.seen['work-api/gpt-6.1-sol']['tried'] -= model_fallback_gap()
        self.assertTrue(self.app.check_fallback())
        self.assertIsNone(self.app.background_pause(owner=True))

    def test_the_fallback_is_only_checked_while_the_limits_would_hold_work(self):
        self.app.model_usage = usage(20)
        self.assertIsNone(self.app.check_fallback())
        self.assertEqual(self.checks, [])
        self.app.model_usage = usage(model_budget.FOLLOW_UP_PAUSE)
        self.assertTrue(self.app.check_fallback())

    def test_a_fallback_on_the_same_sign_in_never_counts(self):
        Path(self.app.config['openclaw_config']).write_text(json.dumps({'agents': {'defaults': {'model': {
            'primary': 'openai/gpt-6.1-sol', 'fallbacks': ['openai-codex/gpt-6-astra']}}}}))
        self.app.model_usage = usage(70)
        self.assertIsNone(self.app.check_fallback())
        self.assertEqual(self.checks, [])
        self.assertEqual(self.app.background_pause()['window'], '5h')


def model_fallback_gap():
    return f.CHECK_GAP + 1


if __name__ == '__main__':
    unittest.main()
