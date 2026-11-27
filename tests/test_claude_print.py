"""One-shot turns on a Claude sign-in (claude_print.py): Help and the other one-shot features failed there with "No API
key found", since `infer model run` never takes the Claude CLI route. A stand-in Claude Code only: nothing is sent."""
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import claude_print
import help_chat
import model_service


class Answer:
    def __init__(self, returncode=0, stdout='', stderr=''):
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


def reply(text='OK', error=False):
    return Answer(1 if error else 0, json.dumps({'type': 'result', 'is_error': error, 'result': text}))


class ClaudePrint(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.made = 0

    def config(self, model, models=None):
        self.made += 1
        path = Path(self.temp.name) / f'openclaw-{self.made}.json'
        path.write_text(json.dumps({'agents': {'defaults': {'model': {'primary': model}, 'models': models or {}}}}))
        return {'openclaw': 'oc', 'claude': '/opt/claude', 'openclaw_config': str(path)}

    def test_only_the_claude_cli_route_goes_through_claude_code(self):
        pinned = {'anthropic/*': {'agentRuntime': {'id': 'claude-cli'}}}
        self.assertEqual(claude_print.ref(self.config('anthropic/claude-opus-5-5', pinned)), 'anthropic/claude-opus-5-5')
        self.assertEqual(claude_print.ref(self.config('claude-cli/claude-opus-5-5')), 'claude-cli/claude-opus-5-5')
        self.assertEqual(claude_print.ref(self.config('openai/gpt-6.1-sol', pinned), 'anthropic/claude-sonnet-5'), 'anthropic/claude-sonnet-5')
        self.assertIsNone(claude_print.ref(self.config('anthropic/claude-opus-5-5')))  # an API key
        self.assertIsNone(claude_print.ref(self.config('openai/gpt-6.1-sol')))
        self.assertIsNone(claude_print.ref(self.config('claude-cli/claude-opus-5-5'), 'openai/gpt-6.1-sol'))

    def test_a_bare_turn_no_tools_no_settings_the_prompt_on_stdin_and_no_api_key(self):
        seen = {}
        def call(args, **kw):
            seen.update(args=args, **kw)
            return reply('OK.')
        with mock.patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'x', 'ANTHROPIC_BASE_URL': 'y', 'HOME': os.environ.get('HOME', '/')}):
            self.assertEqual(claude_print.run({'claude': '/opt/claude'}, 'Reply with OK.', 'anthropic/claude-opus-5-5', 'off', call=call), 'OK.')
        args = seen['args']
        self.assertEqual(args[:2], ['/opt/claude', '-p'])
        self.assertEqual(args[args.index('--model') + 1], 'claude-opus-5-5')
        self.assertEqual(args[args.index('--tools') + 1], '')
        self.assertEqual(args[args.index('--setting-sources') + 1], '')
        self.assertEqual(args[args.index('--effort') + 1], 'low')
        for flag in ('--strict-mcp-config', '--disable-slash-commands', '--no-session-persistence'):
            self.assertIn(flag, args)
        self.assertNotIn('Reply with OK.', args)
        self.assertEqual(seen['input'], 'Reply with OK.')
        self.assertFalse({'ANTHROPIC_API_KEY', 'ANTHROPIC_BASE_URL'} & set(seen['env']))
        self.assertFalse(os.path.exists(seen['cwd']))  # an empty folder, gone afterwards

    def test_a_setup_token_sign_in_in_its_user_settings_is_handed_on_and_nothing_else(self):
        # the cloud's agent keeps a hosted Machine's year-long sign-in there; a turn here reads no settings file
        home = Path(self.temp.name) / 'home'
        (home / '.claude').mkdir(parents=True)
        seen = {}
        def call(args, **kw):
            seen.update(kw)
            return reply('OK.')
        with mock.patch.dict(os.environ, {'HOME': str(home), 'CLAUDE_CODE_OAUTH_TOKEN': 'from-the-environment'}):
            claude_print.run({'claude': 'c'}, 'x', 'claude-cli/m', call=call)
            self.assertNotIn('CLAUDE_CODE_OAUTH_TOKEN', seen['env'])  # cleared, as OpenClaw does
            (home / '.claude' / 'settings.json').write_text(json.dumps({'env': {'CLAUDE_CODE_OAUTH_TOKEN': 'sk-ant-oat01-kept', 'OTHER': 'x'}}))
            claude_print.run({'claude': 'c'}, 'x', 'claude-cli/m', call=call)
            self.assertEqual(seen['env']['CLAUDE_CODE_OAUTH_TOKEN'], 'sk-ant-oat01-kept')
            self.assertNotIn('OTHER', seen['env'])
            # the AI's check signs in as OpenClaw's Gateway does, which never gets that token: it said ok while every
            # Gateway turn was "Not logged in" (2026-11-27)
            claude_print.run({'claude': 'c'}, 'x', 'claude-cli/m', call=call, gateway=True)
            self.assertNotIn('CLAUDE_CODE_OAUTH_TOKEN', seen['env'])
            for broken in ('not json', '[]', '{"env": []}'):
                (home / '.claude' / 'settings.json').write_text(broken)
                claude_print.run({'claude': 'c'}, 'x', 'claude-cli/m', call=call)
                self.assertNotIn('CLAUDE_CODE_OAUTH_TOKEN', seen['env'])

    def test_the_ai_s_check_and_the_fallback_checks_sign_in_as_the_gateway_does(self):
        import model_fallback
        with mock.patch.object(claude_print, 'run', return_value='OK') as run:
            self.assertTrue(model_fallback.turn(self.config('claude-cli/claude-opus-5-5'))[0])
        self.assertIs(run.call_args.kwargs.get('gateway'), True)  # one-shot features keep the hand-on (the test above)

    def test_its_own_error_or_why_there_was_none(self):
        fail = lambda answer: (lambda args, **kw: answer)
        with self.assertRaisesRegex(claude_print.Failed, 'selected model'):
            claude_print.run({'claude': 'c'}, 'x', 'claude-cli/m', call=fail(reply("There's an issue with the selected model (m).", True)))
        with self.assertRaisesRegex(claude_print.Failed, 'Not logged in'):
            claude_print.run({'claude': 'c'}, 'x', 'claude-cli/m', call=fail(Answer(1, '', 'Not logged in. Run claude login.')))
        with self.assertRaisesRegex(claude_print.Failed, 'empty answer'):
            claude_print.run({'claude': 'c'}, 'x', 'claude-cli/m', call=fail(reply(' ')))
        def gone(args, **kw):
            raise OSError('missing')
        with self.assertRaisesRegex(claude_print.Failed, 'could not be started'):
            claude_print.run({'claude': 'c'}, 'x', 'claude-cli/m', call=gone)
        with mock.patch.object(claude_print, 'binary', return_value=None), self.assertRaisesRegex(claude_print.Failed, 'not installed'):
            claude_print.run({}, 'x', 'claude-cli/m', call=gone)

    def test_help_and_the_other_one_shot_turns_take_it_on_a_claude_sign_in(self):
        config = self.config('claude-cli/claude-opus-5-5')
        calls = []
        def stand_in(args, **kw):
            calls.append(args)
            self.assertEqual(args[0], '/opt/claude')  # never `infer model run`
            return reply('A short answer.')
        with mock.patch.object(subprocess, 'run', side_effect=stand_in):
            self.assertEqual(help_chat.openclaw_model_run(config, 'question'), 'A short answer.')
            self.assertEqual(model_service.run(config, 'question'), 'A short answer.')  # never the helper's Gateway call
        self.assertEqual(len(calls), 2)
        with mock.patch.object(subprocess, 'run', side_effect=subprocess.TimeoutExpired('claude', 1)):
            with self.assertRaisesRegex(help_chat.Unavailable, 'too long'):
                help_chat.openclaw_model_run(config, 'question')
        with mock.patch.object(subprocess, 'run', return_value=reply('Not logged in', True)):
            with self.assertRaisesRegex(help_chat.Unavailable, 'reach your model'):
                help_chat.openclaw_model_run(config, 'question')
        # Keys and the ChatGPT sign-in keep `infer model run`
        seen = []
        def infer(args, **kw):
            seen.append(args)
            return Answer(0, json.dumps({'ok': True, 'outputs': [{'text': 'Hi'}]}))
        with mock.patch.object(subprocess, 'run', side_effect=infer):
            self.assertEqual(help_chat.openclaw_model_run(self.config('openai/gpt-6.1-sol'), 'question'), 'Hi')
        self.assertEqual(seen[0][1:4], ['infer', 'model', 'run'])


if __name__ == '__main__':
    unittest.main()
