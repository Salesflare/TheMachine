"""model_service: search answers and Help take their model turns from one long-running helper, not a new OpenClaw
process per turn. One process serves turn after turn and several at once; a model that fails says so as the CLI path
did; a helper that can't start or stops mid-turn leaves the turn to the CLI. The helper is a stand-in script here."""
import json
import os
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

sys.path[:0] = [str(Path(__file__).resolve().parent.parent)]
import help_chat  # noqa: E402
import model_service  # noqa: E402

FAKE = r'''
import json, os, sys, threading, time
starts = os.environ['FAKE_STARTS']
open(starts, 'a').write('start\n')
print(json.dumps({'ready': True}), flush=True)
lock = threading.Lock()
def answer(req):
    p = req['prompt']
    if p == 'slow':
        time.sleep(0.4)
    if p == 'die':
        os._exit(1)
    reply = {'id': req['id'], 'error': 'timeout'} if p == 'late' else {'id': req['id'], 'error': 'unavailable'} if p == 'fail' else \
        {'id': req['id'], 'ok': True, 'text': 'Said: ' + p + (' with ' + req['model'] if req.get('model') else '') + (' at ' + req['thinking'] if req.get('thinking') else '')}
    with lock:
        print(json.dumps(reply), flush=True)
for line in sys.stdin:
    threading.Thread(target=answer, args=(json.loads(line),)).start()
'''


class ModelService(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.script = Path(self.temp.name) / 'fake.py'
        self.script.write_text(FAKE)
        self.starts = Path(self.temp.name) / 'starts'
        env = dict(os.environ, FAKE_STARTS=str(self.starts))
        self.service = model_service.Service([sys.executable, str(self.script)], env)
        self.addCleanup(self.stop)
        patch = mock.patch.object(model_service, 'service', lambda config: self.service)
        patch.start(); self.addCleanup(patch.stop)

    def stop(self):
        if self.service.proc and self.service.proc.poll() is None:
            self.service.proc.stdin.close()
            self.service.proc.wait(5)

    def started(self):
        return self.starts.read_text().count('start') if self.starts.exists() else 0

    def test_one_process_answers_turn_after_turn(self):
        with mock.patch.object(help_chat, 'openclaw_model_run', side_effect=AssertionError('no CLI')):
            self.assertEqual(model_service.run({}, 'hello'), 'Said: hello')
            self.assertEqual(model_service.run({}, 'again', 'openai/gpt-5.5', 'low'), 'Said: again with openai/gpt-5.5 at low')
        self.assertEqual(self.started(), 1)

    def test_turns_at_once_each_get_their_own_answer(self):
        out = {}
        threads = [threading.Thread(target=lambda p=p: out.__setitem__(p, model_service.run({}, p))) for p in ('slow', 'quick', 'third')]
        for th in threads:
            th.start()
        for th in threads:
            th.join(10)
        self.assertEqual(out, {'slow': 'Said: slow', 'quick': 'Said: quick', 'third': 'Said: third'})
        self.assertEqual(self.started(), 1)

    def test_a_failed_turn_says_so_as_before(self):
        with mock.patch.object(help_chat, 'openclaw_model_run', side_effect=AssertionError('no CLI')):
            with self.assertRaisesRegex(help_chat.Unavailable, 'can’t reach your model'):
                model_service.run({}, 'fail')
            with self.assertRaisesRegex(help_chat.Unavailable, 'took too long'):
                model_service.run({}, 'late')

    def test_a_helper_that_stops_leaves_the_turn_to_the_cli_and_starts_again(self):
        with mock.patch.object(help_chat, 'openclaw_model_run', return_value='From the CLI') as cli:
            self.assertEqual(model_service.run({}, 'die', timeout=5), 'From the CLI')
        cli.assert_called_once_with({}, 'die', None, None, timeout=5)
        self.assertEqual(model_service.run({}, 'next'), 'Said: next')
        self.assertEqual(self.started(), 2)

    def test_a_helper_that_cannot_start_leaves_the_turn_to_the_cli(self):
        self.service.command = [str(Path(self.temp.name) / 'missing')]
        with mock.patch.object(help_chat, 'openclaw_model_run', return_value='From the CLI'):
            self.assertEqual(model_service.run({}, 'hello'), 'From the CLI')


class Wiring(unittest.TestCase):
    def test_one_helper_per_process_started_only_when_needed(self):
        self.assertTrue(model_service.SCRIPT.exists())
        with mock.patch.dict(model_service._services, clear=True):
            one = model_service.service({'openclaw': '/opt/oc/bin/openclaw'})
            self.assertIs(model_service.service({'openclaw': '/opt/oc/bin/openclaw'}), one)
            self.assertEqual(one.command[1], str(model_service.SCRIPT))
            self.assertIsNone(one.proc)  # nothing starts until a turn or warm()

    def test_search_and_help_turns_go_through_the_helper(self):
        root = Path(__file__).resolve().parent.parent
        self.assertIn('model_service.run(self.config, text, model, thinking, timeout=search_ask.TIMEOUT)', (root / 'machine/app/search_ask.py').read_text())
        self.assertIn('model_service.run(self.config, text, model, thinking, timeout=search_ask.PLAN_TIMEOUT)', (root / 'machine/app/search_ask.py').read_text())
        self.assertIn('run=run or model_service.run', (root / 'support_app.py').read_text())


if __name__ == '__main__':
    unittest.main()
