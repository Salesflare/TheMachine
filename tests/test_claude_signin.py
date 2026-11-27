"""A Claude sign-in that ended (machine/claude_signin.py): read without blocking the poll, said on Needs you with the
one step that signs in again, and told once on the phone and in Telegram (machine/app/ai_signin.py)."""
import datetime as dt
import json
from pathlib import Path
import re
import subprocess
import tempfile
import time
import unittest
from unittest import mock

import assistant
from machine import claude_signin
from machine.app import ai_signin
from machine.app import status as machine_app_status

NOW = time.time()


def iso(seconds):
    return dt.datetime.fromtimestamp(NOW + seconds, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')


def status_run(logged_in=True, ends=10 * 86400, calls=None):
    def run(command, **_):
        if calls is not None:
            calls.append(command)
        return subprocess.CompletedProcess(command, 0, json.dumps({'loggedIn': logged_in, 'authMethod': 'claude.ai', 'email': 'x@example.com',
                                                                   'subscriptionType': 'max', 'loginExpiresAt': iso(ends)}), '')
    return run


class Reading(unittest.TestCase):
    def setUp(self):
        claude_signin.reset()
        self.addCleanup(claude_signin.reset)
        self.config = {'claude': '/bin/claude'}

    def test_keeps_only_whether_the_plan_and_the_end(self):
        found = claude_signin.parse(status_run()(['x']).stdout, NOW)
        self.assertEqual(set(found), {'signed_in', 'plan', 'expires_at'})
        self.assertEqual((found['signed_in'], found['plan']), (True, 'max'))
        self.assertNotIn('example.com', json.dumps(found))
        self.assertIsNone(claude_signin.parse('not json', NOW))
        self.assertIsNone(claude_signin.parse('{"loggedIn": "yes"}', NOW))

    def test_past_its_end_it_is_signed_out_though_claude_code_still_says_logged_in(self):
        # Claude Code says loggedIn until a refresh fails; its `claude -p` then fails with "OAuth session expired"
        found = claude_signin.parse(status_run(ends=-60)(['x']).stdout, NOW)
        self.assertEqual((found['signed_in'], found['plan']), (False, None))
        self.assertFalse(claude_signin.parse(status_run(logged_in=False)(['x']).stdout, NOW)['signed_in'])

    def test_days_left_only_within_three_days(self):
        def left(seconds):
            return claude_signin.days_left(claude_signin.parse(status_run(ends=seconds)(['x']).stdout, NOW), NOW)
        self.assertIsNone(left(10 * 86400))
        self.assertEqual(left(2.5 * 86400), 2)
        self.assertEqual(left(30 * 3600), 1)
        self.assertEqual(left(3600), 0)
        self.assertIsNone(left(-60))

    def test_read_at_most_hourly_while_signed_in_and_again_after_a_failed_check(self):
        calls, clock = [], [1000.0]
        run = status_run(calls=calls)
        self.assertTrue(claude_signin.read(self.config, run, lambda: clock[0])['signed_in'])
        clock[0] += 600
        claude_signin.read(self.config, run, lambda: clock[0])
        self.assertEqual(len(calls), 1)
        claude_signin.stale()  # the AI failed its check (first_look.model_check_run)
        claude_signin.read(self.config, run, lambda: clock[0])
        self.assertEqual(len(calls), 2)
        clock[0] += 3600
        claude_signin.read(self.config, run, lambda: clock[0])
        self.assertEqual(len(calls), 3)

    def test_the_poll_never_waits_on_claude_code(self):
        started = []

        def run(command, **_):
            started.append(command)
            return status_run(ends=-60)(command)
        with mock.patch('threading.Thread') as thread:
            self.assertIsNone(claude_signin.read(self.config, run, wait=False))
        self.assertEqual(started, [])  # only the background thread runs it
        thread.return_value.start.assert_called_once()


SIGNED_OUT_TEXTS = ('Failed to authenticate: OAuth session expired and could not be refreshed',  # 2026-11-27, Claude Code 2.1
                    'Not logged in · Please run /login', 'OAuth token has expired. Please obtain a new token',
                    'OAuth token has been revoked')
OTHER_TEXTS = ('No API key found for provider "anthropic".', 'No answer within 60 seconds.', 'Overloaded', 'The model gave an empty answer.')


class SaidSignedOut(unittest.TestCase):
    """A refresh that failed before the sign-in's end: Claude Code's `claude -p` says so while `claude auth status`
    still says loggedIn with a later end (it only looks for a token)."""
    def setUp(self):
        claude_signin.reset()
        self.addCleanup(claude_signin.reset)

    def test_claude_codes_words_for_a_sign_in_it_cant_use(self):
        for text in SIGNED_OUT_TEXTS:
            self.assertTrue(claude_signin.said_signed_out(text), text)
        for text in OTHER_TEXTS + (None, ''):
            self.assertFalse(claude_signin.said_signed_out(text), text)

    def test_the_review_runner_names_the_same_words_auth_failed(self):
        source = (Path(__file__).parent.parent / 'preparation-run.mjs').read_text()
        pattern = next(line for line in source.splitlines() if line.rstrip().endswith("/i,'auth_failed'],"))
        runner = re.compile(pattern.strip()[2:-len("/i,'auth_failed'],")].replace('\\/', '/'), re.I)
        for text in SIGNED_OUT_TEXTS:
            self.assertTrue(runner.search(text), text)

    def test_a_refusal_counts_as_signed_out_until_a_new_sign_in_or_a_check_that_passes(self):
        config, stamp = {'claude': '/bin/claude'}, [100]
        with mock.patch.object(claude_signin, 'stamp', side_effect=lambda: stamp[0]):
            self.assertTrue(claude_signin.read(config, status_run())['signed_in'])
            claude_signin.refused()
            found = claude_signin.read(config, status_run())
            self.assertEqual((found['signed_in'], found['plan']), (False, None))
            self.assertIsNone(claude_signin.days_left(found, NOW))
            self.assertEqual(ai_signin.lapse(found), found['expires_at'])  # told once for this sign-in
            claude_signin.answered()
            self.assertTrue(claude_signin.read(config, status_run())['signed_in'])
            claude_signin.refused()
            stamp[0] = 200  # signed in again: Claude Code wrote its credentials
            self.assertTrue(claude_signin.read(config, status_run())['signed_in'])


class NeedsYou(unittest.TestCase):
    def setUp(self):
        claude_signin.reset()
        self.addCleanup(claude_signin.reset)
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name, 'openclaw.json')
        path.write_text(json.dumps({'agents': {'defaults': {'model': 'claude-cli/claude-opus-5-5'}}}))
        self.config = {'claude': '/bin/claude', 'openclaw_config': str(path)}

    def item(self, ends=10 * 86400, logged_in=True, manage='https://app.example.com/setup'):
        claude_signin.read(self.config, status_run(logged_in, ends))
        return machine_app_status.claude_signin_item(self.config, manage)

    def test_signed_out_says_so_with_sign_in_again(self):
        item = self.item(ends=-60)
        self.assertEqual(item['id'], 'claude-signed-out')
        self.assertEqual(item['text'], 'Claude is signed out, so nothing new gets checked or prepared.')
        self.assertEqual((item['url'], item['action']), ('https://app.example.com/setup#model', 'Sign in again'))
        claude_signin.reset()
        self.assertEqual(self.item(ends=-60, manage='')['action'], 'Run: claude auth login')

    def test_a_check_that_said_signed_out_says_so_while_claude_code_still_says_logged_in(self):
        self.assertIsNone(self.item())
        claude_signin.refused()  # first_look.model_check_run: "OAuth session expired and could not be refreshed"
        self.assertEqual(self.item()['id'], 'claude-signed-out')

    def test_three_days_ahead_too_and_nothing_while_it_holds(self):
        self.assertEqual(self.item(ends=3600)['text'], 'Your Claude sign-in ends today.')
        claude_signin.reset()
        self.assertEqual(self.item(ends=30 * 3600)['id'], 'claude-signin-ends')
        claude_signin.reset()
        self.assertIsNone(self.item())

    def test_only_on_the_claude_cli_route(self):
        Path(self.config['openclaw_config']).write_text(json.dumps({'agents': {'defaults': {'model': 'openai/gpt-6-astra'}}}))
        self.assertIsNone(self.item(ends=-60))

    def test_needs_you_has_it(self):
        claude_signin.read(self.config, status_run(ends=-60))
        with mock.patch.object(machine_app_status, 'main_model', return_value=None):
            items = machine_app_status.needs_you({**self.config, 'accounts': [], 'manage_url': 'https://app.example.com/setup'})
        self.assertIn('claude-signed-out', [i['id'] for i in items])


class ToldOnce(unittest.TestCase):
    def setUp(self):
        claude_signin.reset()
        self.addCleanup(claude_signin.reset)
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name, 'openclaw.json')
        path.write_text(json.dumps({'agents': {'defaults': {'model': 'claude-cli/claude-opus-5-5'}}}))
        self.app = mock.Mock()
        self.app.config = {'claude': '/bin/claude', 'openclaw_config': str(path), 'manage_url': 'https://app.example.com/setup',
                           'telegram_owner': '1', 'database': str(Path(folder.name, 'a.sqlite'))}
        self.app.store = assistant.Store(self.app.config['database'])
        self.app.notify_on.return_value = True
        self.pushes, self.telegrams = [], []
        reach = mock.patch.object(ai_signin, 'push_reach', return_value=([{'endpoint': 'x'}], 1))
        reach.start()
        self.addCleanup(reach.stop)
        self.noon = dt.datetime.now().astimezone().replace(hour=12, minute=0)

    def step(self, when=None):
        return ai_signin.step(self.app, when or self.noon, push=lambda *a, **k: self.pushes.append((a, k)) or [{'status': 201}],
                              telegram=lambda config, message: self.telegrams.append(message))

    def test_a_lapse_is_told_once_on_the_phone_and_in_telegram(self):
        claude_signin.read(self.app.config, status_run(ends=-60))
        self.assertEqual(self.step(), ['push', 'telegram'])
        payload = self.pushes[0][0][3]
        self.assertEqual((payload['title'], payload['url']), ('Claude is signed out', 'https://app.example.com/setup#model'))
        self.assertEqual(self.pushes[0][1]['kind'], 'result')
        self.assertEqual(self.telegrams[0]['buttons'], [[{'text': 'Sign in again', 'url': 'https://app.example.com/setup#model'}]])
        self.assertEqual(self.step(), [])
        self.assertEqual((len(self.pushes), len(self.telegrams)), (1, 1))

    def test_nothing_while_signed_in_and_a_lapse_waits_for_work_hours(self):
        claude_signin.read(self.app.config, status_run())
        self.assertEqual(self.step(), [])
        claude_signin.reset()
        claude_signin.read(self.app.config, status_run(ends=-60))
        self.assertEqual(self.step(self.noon.replace(hour=3)), [])
        self.assertEqual(self.step(), ['push', 'telegram'])

    def test_telegram_follows_the_owners_choice(self):
        self.app.notify_on.return_value = False
        claude_signin.read(self.app.config, status_run(ends=-60))
        self.assertEqual(self.step(), ['push'])


if __name__ == '__main__':
    unittest.main()
