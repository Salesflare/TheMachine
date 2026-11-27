"""Training on the owner's chats (machine/ai_training.py): a personal ChatGPT or Claude plan gets one quiet line in
Settings, Model linking to the provider's own switch; Done hides it for good (config.json). Business, team and
enterprise plans, API keys, other providers and an unknown plan get nothing."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from machine import ai_training, claude_signin
from machine.app.settings_actions import SettingsActionsApp
from machine.model_usage import model_status
from machine.owner_error import OwnerError


class State(unittest.TestCase):
    def test_personal_plans_are_asked(self):
        for status, provider in (({'chatgpt': True, 'plan': 'plus'}, 'chatgpt'), ({'chatgpt': True, 'plan': 'pro'}, 'chatgpt'),
                                 ({'chatgpt': True, 'plan': 'free'}, 'chatgpt'), ({'chatgpt': True, 'plan': 'go'}, 'chatgpt'),
                                 ({'claude_plan': True, 'plan': 'Max (20x)'}, 'claude'), ({'claude_plan': True, 'plan': 'pro'}, 'claude')):
            found = ai_training.state(status)
            self.assertEqual(found['state'], 'todo', status)
            self.assertEqual(found['provider'], provider)
            self.assertEqual(found['url'], ai_training.SETTINGS[provider])
            self.assertTrue(found['url'].startswith('https://'))

    def test_work_plans_keys_and_unknown_plans_are_not(self):
        for status in ({'chatgpt': True, 'plan': 'team'}, {'chatgpt': True, 'plan': 'business'}, {'chatgpt': True, 'plan': 'enterprise'},
                       {'chatgpt': True, 'plan': 'edu'}, {'chatgpt': True, 'plan': None}, {'claude_plan': True, 'plan': 'team'},
                       {'claude_plan': True, 'plan': 'enterprise'}, {'claude_plan': True}, {'provider': 'mistral', 'plan': None},
                       {'provider': 'openai', 'plan': 'plus'}, {}, None):  # a ChatGPT plan name without the sign-in: an API key
            self.assertEqual(ai_training.state(status), {'state': 'na'}, status)

    def test_done_is_per_provider(self):
        self.assertEqual(ai_training.state({'chatgpt': True, 'plan': 'plus'}, {'chatgpt'})['state'], 'done')
        self.assertEqual(ai_training.state({'claude_plan': True, 'plan': 'max'}, {'chatgpt'})['state'], 'todo')

    def test_done_is_read_from_the_file_too(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d, 'config.json')
            path.write_text(json.dumps({'ai_training_off': ['claude', 'other']}))
            self.assertEqual(ai_training.done_for({}, path), {'claude'})
            self.assertEqual(ai_training.done_for({'ai_training_off': ['chatgpt']}), {'chatgpt'})
            self.assertEqual(ai_training.done_for({'ai_training_off': 'chatgpt'}), set())


class ClaudePlan(unittest.TestCase):
    def setUp(self):
        claude_signin.reset()
        self.addCleanup(claude_signin.reset)

    def test_reads_only_the_plan_kind_and_keeps_it_an_hour(self):
        calls = []

        def run(command, **_):
            calls.append(command)
            return subprocess.CompletedProcess(command, 0, json.dumps({'loggedIn': True, 'email': 'x@example.com', 'subscriptionType': 'max'}), '')
        clock = [1000.0]
        self.assertEqual(ai_training.claude_plan({'claude': '/bin/claude'}, run, lambda: clock[0]), 'max')
        self.assertEqual(calls, [['/bin/claude', 'auth', 'status', '--json']])
        clock[0] += 60
        self.assertEqual(ai_training.claude_plan({'claude': '/bin/claude'}, run, lambda: clock[0]), 'max')
        self.assertEqual(len(calls), 1)

    def test_signed_out_or_unreadable_is_unknown(self):
        def run(command, **_):
            return subprocess.CompletedProcess(command, 0, 'not json', '')
        self.assertIsNone(ai_training.claude_plan({'claude': '/bin/claude'}, run, lambda: 5000.0))

    def test_model_status_names_the_claude_plan(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d, 'openclaw.json')
            path.write_text(json.dumps({'agents': {'defaults': {'model': 'claude-cli/claude-opus-5-5'}}}))
            config = {'openclaw_config': str(path)}
            self.assertEqual(model_status(config, {'providers': []}, None, None, claude_plan='pro')['plan'], 'pro')
            reply = {'providers': [{'provider': 'anthropic', 'plan': 'Max (20x)'}]}
            self.assertEqual(model_status(config, reply, None, None, claude_plan='pro')['plan'], 'Max (20x)')
            path.write_text(json.dumps({'agents': {'defaults': {'model': 'openai/gpt-6.1-sol'}}}))
            self.assertIsNone(model_status(config, {'providers': []}, None, None, claude_plan='pro')['plan'])


class Done(unittest.TestCase):
    def test_done_is_kept_in_config_and_only_from_the_owner(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d, 'config.json')
            path.write_text(json.dumps({'language': 'en'}))
            app = SettingsActionsApp()
            app.config, app.config_path = {'language': 'en'}, str(path)
            app.model_status = {'chatgpt': True, 'plan': 'plus'}
            with self.assertRaises(OwnerError):
                app.ai_training_done_action('ai_training_done', {'provider': 'chatgpt'})
            with self.assertRaises(ValueError):
                app.ai_training_done_action('ai_training_done', {'provider': 'elsewhere'}, owner_dashboard=True)
            out = app.ai_training_done_action('ai_training_done', {'provider': 'chatgpt'}, owner_dashboard=True)
            self.assertEqual(out, {'ai_training': {'state': 'done', 'provider': 'chatgpt', 'url': ai_training.SETTINGS['chatgpt']}})
            self.assertEqual(json.loads(path.read_text()), {'language': 'en', 'ai_training_off': ['chatgpt']})


if __name__ == '__main__':
    unittest.main()
