"""To-dos offers a usage limit reset before work stops (model_budget.held_back, ModelPacingApp.reset_nudge, shown by
dashboard/todos-reset-nudge.js): only once a window holds background work back (the 5-hour one at SHORT_PAUSE, the
weekly one at WEEK_CAP) or a limit is reached, and only with resets left. Hosted Team seats reached the weekly limit days
before it reset. Fake usage readings only: no Gateway, no Codex, no reset is ever used."""
import importlib.util
import json
import tempfile
import time
import unittest
from pathlib import Path

import model_budget as b

spec = importlib.util.spec_from_file_location('nudge_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

NOW = 1_800_000_000
HOUR, DAY = 3600, 86400


def usage(short=None, week=None, short_reset=None, week_reset=None, provider='openai'):
    windows = ([{'label': '5h', 'used': short, 'reset': short_reset}] if short is not None else []) + \
              ([{'label': 'Week', 'used': week, 'reset': week_reset}] if week is not None else [])
    return [{'provider': provider, 'name': 'ChatGPT', 'windows': windows}]


class HeldBack(unittest.TestCase):
    def test_only_at_the_points_where_the_budget_holds_work(self):
        at = lambda **k: b.held_back(usage(short_reset=NOW + HOUR, week_reset=NOW + DAY, **k), NOW)
        self.assertIsNone(at(short=b.SHORT_PAUSE - 1, week=b.WEEK_CAP - 1))
        self.assertEqual(at(short=b.SHORT_PAUSE)['window'], '5h')
        # the week's daily share is not it (a quiet day carries over): only the cap
        self.assertIsNone(at(week=60))
        found = at(week=92)
        self.assertEqual((found['window'], found['used'], found['until'], found['name']), ('week', 92, NOW + DAY, 'ChatGPT'))
        self.assertEqual(at(short=80, week=95)['window'], 'week')  # the weekly one first: it holds work longest

    def test_an_old_reading_of_a_window_that_reset_is_not_held(self):
        self.assertIsNone(b.held_back(usage(short=90, short_reset=NOW - 1), NOW))
        self.assertIsNone(b.held_back(None, NOW))


class Nudge(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.app = object.__new__(a.App)
        self.app.config = {'openclaw_config': str(Path(self.temp.name) / 'openclaw.json')}
        self.model('openai/gpt-6.1-sol')
        self.app.model_status = {'can_reset': True, 'resets': {'available': 2, 'credits': []}, 'limit_reached': False}

    def model(self, ref):
        Path(self.app.config['openclaw_config']).write_text(json.dumps({'agents': {'defaults': {'model': ref}}}))

    def test_close_to_the_limit_with_resets_left(self):
        reset = int(time.time()) + 3 * DAY
        self.app.model_usage = usage(short=10, week=b.WEEK_CAP - 1, short_reset=reset, week_reset=reset)
        self.assertIsNone(self.app.reset_nudge())
        self.app.model_usage = usage(short=10, week=92, short_reset=reset, week_reset=reset)
        self.assertEqual(self.app.reset_nudge(), {'window': 'week', 'used': 92, 'until': reset, 'name': 'ChatGPT',
                                                  'resets': 2, 'reached': False})
        self.app.model_usage = usage(short=b.SHORT_PAUSE, short_reset=reset)
        self.assertEqual(self.app.reset_nudge()['window'], '5h')

    def test_nothing_new_without_resets(self):
        self.app.model_usage = usage(week=100, week_reset=int(time.time()) + DAY)
        for status in ({'can_reset': False, 'resets': {'available': 0, 'credits': []}, 'limit_reached': True},
                       {'can_reset': False, 'resets': None, 'limit_reached': True}, None):
            self.app.model_status = status
            self.assertIsNone(self.app.reset_nudge())
        self.assertEqual(self.app.model_pause()['window'], 'week')  # the limit banner stays as it is

    def test_a_limit_reached_with_resets_left_offers_one(self):
        until = int(time.time()) + 2 * HOUR
        self.app.model_usage = usage(short=100, short_reset=until)
        found = self.app.reset_nudge()
        self.assertTrue(found['reached'])
        self.assertEqual((found['window'], found['resets']), ('5h', 2))

    def test_not_for_another_plan_nor_while_a_fallback_carries_the_work(self):
        self.app.model_usage = usage(week=95, week_reset=int(time.time()) + DAY, provider='anthropic')
        self.model('anthropic/claude-sonnet-4-5')
        self.assertIsNone(self.app.reset_nudge())  # the resets are ChatGPT's
        self.model('openai/gpt-6.1-sol')
        self.app.model_usage = usage(week=95, week_reset=int(time.time()) + DAY)
        self.app.fallback_covers = lambda: {'model': 'other/model'}
        self.assertIsNone(self.app.reset_nudge())

    def test_a_hosted_machine_without_codex_signed_in_offers_to_turn_resets_on(self):
        setup = 'https://app.example.com/setup#codex'
        self.app.model_status = {'can_reset': False, 'resets': None, 'reset_setup': setup, 'limit_reached': False}
        reset = int(time.time()) + 3 * DAY
        self.app.model_usage = usage(week=b.WEEK_CAP - 1, week_reset=reset)
        self.assertIsNone(self.app.reset_nudge())
        self.app.model_usage = usage(week=92, week_reset=reset)
        self.assertEqual(self.app.reset_nudge(), {'window': 'week', 'used': 92, 'until': reset, 'name': 'ChatGPT',
                                                  'resets': None, 'reached': False, 'setup': setup})
        self.app.model_usage = usage(week=100, week_reset=reset)  # reached: the same way to turn them on
        self.assertEqual((self.app.reset_nudge()['reached'], self.app.reset_nudge()['setup']), (True, setup))
        self.app.model_status = {**self.app.model_status, 'reset_setup': None}  # a self-hosted Machine: nothing new
        self.assertIsNone(self.app.reset_nudge())


if __name__ == '__main__':
    unittest.main()
