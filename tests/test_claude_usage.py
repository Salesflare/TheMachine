"""A Claude plan's usage, read through Claude Code itself (machine/model_usage.py): OpenClaw's usage.status reports
none for its Claude CLI route, so the Machine asks Claude Code's own stream-json control request `get_usage`, maps
its 5-hour and weekly windows to the usual model_usage shape, and the bars, the pacing (model_budget) and the health
report use them unchanged. A fake Claude Code answers here: no network, no sign-in, no model call."""
import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from machine import model_usage as mu
from machine.app import model_pacing
import model_budget

NOW = int(time.time())
FIVE_RESET, WEEK_RESET = NOW + 3600, NOW + 4 * 86400


def iso(seconds):
    return time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime(seconds))


USAGE = {'session': {'total_cost_usd': 0}, 'subscription_type': 'max', 'rate_limits_available': True, 'behaviors': None,
         'rate_limits': {'five_hour': {'utilization': 66.4, 'resets_at': iso(FIVE_RESET)},
                         'seven_day': {'utilization': 12, 'resets_at': iso(WEEK_RESET)},
                         'seven_day_opus': None, 'model_scoped': [{'display_name': 'Opus', 'utilization': 40, 'resets_at': None}]}}

# A fake Claude Code speaking its stream-json control protocol: it logs what it got (args, env, requests) and answers
FAKE_CLAUDE = r"""#!/usr/bin/env python3
import json, os, sys
log = open(os.environ['FAKE_CLAUDE_LOG'], 'a')
log.write(json.dumps({'args': sys.argv[1:], 'api_key': 'ANTHROPIC_API_KEY' in os.environ, 'cwd': os.getcwd()}) + chr(10))
mode = os.environ.get('FAKE_CLAUDE_MODE', 'ok')
print(json.dumps({'type': 'system', 'subtype': 'commands_changed'}), flush=True)
for line in sys.stdin:
    msg = json.loads(line)
    log.write(json.dumps(msg['request']) + chr(10)); log.flush()
    sub, rid = msg['request']['subtype'], msg['request_id']
    if mode == 'silent':
        continue
    if sub == 'initialize':
        body = {'subtype': 'success', 'request_id': rid, 'response': {'commands': []}}
    elif sub == 'get_usage' and mode == 'ok':
        body = {'subtype': 'success', 'request_id': rid, 'response': json.loads(os.environ['FAKE_CLAUDE_USAGE'])}
    else:
        body = {'subtype': 'error', 'request_id': rid, 'error': 'Unknown control request: ' + sub}
    print('not json', flush=True)
    print(json.dumps({'type': 'control_response', 'response': body}), flush=True)
"""


class ClaudeCodeUsage(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.claude = Path(self.dir.name) / 'claude'
        self.claude.write_text(FAKE_CLAUDE)
        self.claude.chmod(0o755)
        self.log = Path(self.dir.name) / 'log'
        self.env = patch.dict(os.environ, {'FAKE_CLAUDE_LOG': str(self.log), 'FAKE_CLAUDE_USAGE': json.dumps(USAGE),
                                           'FAKE_CLAUDE_MODE': 'ok', 'ANTHROPIC_API_KEY': 'not-a-real-key'})
        self.env.start()
        self.openclaw = Path(self.dir.name) / 'openclaw.json'
        self.config = {'claude': str(self.claude), 'openclaw_config': str(self.openclaw)}
        self.main_model('claude-cli/claude-opus-5-5')

    def tearDown(self):
        self.env.stop()
        self.dir.cleanup()

    def main_model(self, model):
        self.openclaw.write_text(json.dumps({'agents': {'defaults': {'model': {'primary': model}}}}))

    def logged(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_reads_the_plan_windows_from_claude_code_without_a_prompt(self):
        data = mu.claude_code_usage(self.config)
        self.assertEqual(data['rate_limits']['five_hour']['utilization'], 66.4)
        started, *requests = self.logged()
        self.assertEqual(requests, [{'subtype': 'initialize'}, {'subtype': 'get_usage', 'skip_behaviors': True}])
        args = started['args']
        self.assertEqual(args[:5], ['-p', '--input-format', 'stream-json', '--output-format', 'stream-json'])
        self.assertEqual(args[args.index('--tools') + 1], '')
        self.assertIn('--no-session-persistence', args)
        self.assertNotIn('--model', args)  # no turn is started
        self.assertFalse(started['api_key'])  # Claude Code answers with its own sign-in, as OpenClaw runs it
        self.assertFalse(Path(started['cwd']).exists())  # an empty folder, gone afterwards

    def test_maps_the_5_hour_and_weekly_windows_to_the_usual_shape(self):
        entry = mu.claude_usage_entry(mu.claude_code_usage(self.config))
        self.assertEqual(entry, {'provider': 'anthropic', 'displayName': 'Claude', 'windows': [
            {'label': '5h', 'usedPercent': 66.4, 'resetAt': FIVE_RESET * 1000},
            {'label': 'Week', 'usedPercent': 12, 'resetAt': WEEK_RESET * 1000}]})
        self.assertEqual(mu.model_usage({}, reply={'providers': [entry]}), [{'provider': 'anthropic', 'name': 'Claude', 'windows': [
            {'label': '5h', 'used': 66, 'reset': FIVE_RESET}, {'label': 'Week', 'used': 12, 'reset': WEEK_RESET}]}])

    def test_no_plan_limits_no_claude_code_or_an_older_one_is_unknown(self):
        self.assertIsNone(mu.claude_usage_entry({**USAGE, 'rate_limits_available': False, 'rate_limits': None}))
        self.assertIsNone(mu.claude_usage_entry({'rate_limits_available': True, 'rate_limits': {'five_hour': None}}))
        self.assertIsNone(mu.claude_usage_entry(None))
        self.assertIsNone(mu.claude_code_usage({'claude': False}))
        self.assertIsNone(mu.claude_code_usage({'claude': str(Path(self.dir.name) / 'missing')}))
        os.environ['FAKE_CLAUDE_MODE'] = 'old'
        self.assertIsNone(mu.claude_code_usage(self.config))

    def test_a_silent_claude_code_hits_the_deadline(self):
        os.environ['FAKE_CLAUDE_MODE'] = 'silent'
        started = time.time()
        self.assertIsNone(mu.claude_code_usage(self.config, timeout=1))
        self.assertLess(time.time() - started, 10)

    def test_only_a_claude_plan_route_without_windows_asks_claude_code(self):
        asked = []
        read = lambda config: asked.append(1) or USAGE
        chatgpt = {'provider': 'openai', 'accountEmail': 'someone@example.com', 'windows': [{'label': 'Week', 'usedPercent': 30}]}
        reply = mu.with_claude_usage(self.config, {'providers': [chatgpt, {'provider': 'anthropic', 'windows': [], 'error': 'x'}]}, read)
        self.assertEqual([p['provider'] for p in reply['providers']], ['openai', 'anthropic'])
        self.assertEqual(len(reply['providers'][1]['windows']), 2)
        self.assertEqual(mu.with_claude_usage(self.config, None, read)['providers'][0]['provider'], 'anthropic')
        own = {'providers': [{'provider': 'anthropic', 'windows': [{'label': '5h', 'usedPercent': 1}]}]}
        self.assertIs(mu.with_claude_usage(self.config, own, read), own)  # OpenClaw read it itself
        self.assertEqual(len(asked), 2)
        self.main_model('openai/gpt-6.2-sol')
        self.assertIs(mu.with_claude_usage(self.config, own, read), own)
        self.assertEqual(len(asked), 2)

    def test_the_bars_and_the_pacing_follow_the_claude_plan(self):
        chatgpt = {'provider': 'openai', 'plan': 'plus', 'accountEmail': 'someone@example.com',
                   'windows': [{'label': 'Week', 'usedPercent': 99, 'resetAt': WEEK_RESET * 1000}]}
        app = model_pacing.ModelPacingApp()
        app.config = self.config
        with patch.object(model_pacing, 'usage_status', lambda config: {'providers': [chatgpt]}), \
                patch.object(model_pacing, 'model_resets', side_effect=AssertionError('no ChatGPT resets on a Claude plan')), \
                patch.object(model_pacing.ai_training, 'claude_plan', lambda config: 'max'), \
                patch.object(model_pacing.ai_training, 'state', lambda *a: {'state': 'na'}), \
                patch.object(model_pacing.ai_training, 'done_for', lambda *a: set()):
            app.refresh_model_usage()
        status = app.model_status
        self.assertEqual([(w['label'], w['used']) for w in status['windows']], [('5h', 66), ('Week', 12)])
        self.assertEqual((status['claude_plan'], status['chatgpt'], status['plan'], status['usage_page']), (True, False, 'max', None))
        self.assertNotIn('example.com', json.dumps([status, app.model_usage]))
        paused = model_budget.pause(model_budget.for_model(app.model_usage, 'claude-cli/claude-opus-5-5'), NOW)
        self.assertEqual((paused['provider'], paused['window'], paused['until']), ('anthropic', '5h', FIVE_RESET))


if __name__ == '__main__':
    unittest.main()
