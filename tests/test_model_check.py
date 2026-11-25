"""The AI's real check before the first look (model_check.py, App.model_check_run, the first look's gate and fallback):
a sign-in that exists is not enough, one tiny fixed call must answer first. 2026-10-27: a new owner's first look started
while the Claude sign-in was still finishing, its tries failed, and the first to-do came 9.7 hours later. A stand-in
model and fake mail only: no Gateway, no model call, nothing is sent."""
import datetime as dt
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import model_check as mc
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('model_check_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

MAIN, OTHER = 'claude-cli/claude-opus-5-5', 'openai-codex/gpt-6.1-sol'


class Runner:
    def __init__(self, *results): self.results = list(results); self.requests = []
    def __call__(self, request): self.requests.append(request); return {'status': self.results.pop(0)}


class StandIn:
    """The stand-in model: answers per model ref (None: the main model) with (ok, error), and counts the calls."""
    def __init__(self, **answers): self.answers, self.calls = answers, []
    def __call__(self, config, model=None):
        self.calls.append(model)
        return self.answers.get(model or 'main', (False, 'no answer'))


class Answer:
    def __init__(self, returncode=0, stdout='', stderr=''):
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


def mail(source_id, days_ago=1):
    when = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days_ago)).isoformat()
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': when, 'title': 'Pricing question',
            'body': 'Can you confirm?', 'metadata': {'from': 'Sam Example <sam@example.com>'}, 'deleted': False}


class Probe(unittest.TestCase):
    def test_one_fixed_prompt_and_the_providers_own_error_without_keys(self):
        seen = []
        def run(args, **kw):
            seen.append(args)
            return Answer(1, json.dumps({'ok': False, 'error': {'message': 'invalid x-api-key sk-ant-abc123def456 for user sam@example.com'}}))
        ok, error = mc.probe({}, None, run=run)
        self.assertFalse(ok)
        self.assertIn('invalid x-api-key', error)
        self.assertNotIn('sk-ant-abc123def456', error)
        self.assertNotIn('sam@example.com', error)
        self.assertEqual(seen[0][seen[0].index('--prompt') + 1], mc.PROMPT)  # nothing of the owner's goes out
        self.assertNotIn('--model', seen[0])
        self.assertEqual(mc.probe({}, OTHER, run=lambda args, **kw: Answer(0, json.dumps({'ok': True, 'outputs': [{'text': 'OK'}]}))), (True, None))
        # Exit 0 with nothing said (a CLI's empty response) is no answer; stderr says why
        ok, error = mc.probe({}, None, run=lambda args, **kw: Answer(0, '{"ok": true, "outputs": []}', 'cli terminal failure\nCLI backend returned an empty response.'))
        self.assertFalse(ok)
        self.assertIn('empty response', error)
        def slow(args, **kw):
            raise subprocess.TimeoutExpired(args, 90)
        self.assertEqual(mc.probe({}, None, run=slow), (False, 'No answer within 90 seconds.'))


class Routes(unittest.TestCase):
    """2026-11-16: every Machine on a Claude sign-in failed the check ("No API key found for provider anthropic"):
    `infer model run` never takes the Claude CLI route, while reviews ran fine through Claude Code. A Gateway agent turn
    fixed it at about 48,000 tokens a check; Claude Code's own print mode takes about 550."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.made = 0

    def config(self, model, models=None):
        self.made += 1
        path = Path(self.temp.name) / f'openclaw-{self.made}.json'
        path.write_text(json.dumps({'agents': {'defaults': {'model': {'primary': model}, 'models': models or {}}}}))
        return {'openclaw': 'oc', 'claude': '/opt/claude', 'openclaw_config': str(path)}

    def claude_reply(self, text='OK.', error=False):
        return Answer(1 if error else 0, json.dumps({'type': 'result', 'is_error': error, 'result': text}))

    def test_a_claude_sign_in_is_checked_through_claude_code_alone_on_that_model(self):
        pinned = {'anthropic/*': {'agentRuntime': {'id': 'claude-cli'}}}
        for config, model, name in ((self.config('anthropic/claude-opus-5-5', pinned), None, 'claude-opus-5-5'),
                                    (self.config(MAIN), None, 'claude-opus-5-5'),
                                    (self.config(OTHER, pinned), 'anthropic/claude-sonnet-5', 'claude-sonnet-5')):
            seen = []
            def run(args, **kw):
                seen.append((args, kw))
                return self.claude_reply()
            self.assertEqual(mc.probe(config, model, run=run), (True, None))
            self.assertEqual(len(seen), 1)  # no Gateway session to make or delete
            args, kw = seen[0]
            self.assertEqual(args[:2], ['/opt/claude', '-p'])
            self.assertEqual(args[args.index('--model') + 1], name)
            self.assertEqual(args[args.index('--tools') + 1], '')
            self.assertEqual(kw['input'], mc.PROMPT)  # nothing of the owner's goes out
            self.assertNotIn('infer', args)

    def test_on_the_claude_route_claude_codes_own_error_or_a_timeout_is_no_answer(self):
        config = self.config(MAIN)
        self.assertEqual(mc.probe(config, None, run=lambda args, **kw: self.claude_reply(' ')), (False, 'Claude Code gave an empty answer.'))
        self.assertEqual(mc.probe(config, None, run=lambda args, **kw: self.claude_reply('Not logged in. Please run /login', True)),
                         (False, 'Not logged in. Please run /login'))
        def slow(args, **kw):
            raise subprocess.TimeoutExpired(args, 90)
        self.assertEqual(mc.probe(config, None, run=slow), (False, 'No answer within 90 seconds.'))
        def gone(args, **kw):
            raise OSError('missing')
        self.assertEqual(mc.probe(config, None, run=gone), (False, 'Claude Code could not be started.'))
        self.assertFalse(mc.model_fallback.probe(config, None, lambda args, **kw: self.claude_reply('x', True)))
        self.assertTrue(mc.model_fallback.probe(config, None, lambda args, **kw: self.claude_reply()))

    def test_keys_and_the_chatgpt_sign_in_keep_the_raw_model_call(self):
        pinned = {'openai/gpt-6.1-sol': {'agentRuntime': {'id': 'openclaw'}}, 'anthropic/*': {'agentRuntime': {'id': 'claude-cli'}}}
        for config, model in ((self.config('openai/gpt-6.1-sol', pinned), None), (self.config('anthropic/claude-opus-5-5'), None),
                              (self.config(MAIN), OTHER), (self.config('work-api/gpt-6.1-sol'), None)):
            seen = []
            def run(args, **kw):
                seen.append(args)
                return Answer(0, json.dumps({'ok': True, 'outputs': [{'text': 'OK'}]}))
            self.assertEqual(mc.probe(config, model, run=run), (True, None))
            self.assertEqual(len(seen), 1)
            self.assertEqual(seen[0][:6], ['oc', 'infer', 'model', 'run', '--gateway', '--json'])
            self.assertEqual('--model' in seen[0], bool(model))


class WarmUp(unittest.TestCase):
    def test_gateway_rpcs_only_and_the_throwaway_session_is_always_deleted(self):
        seen = []
        def run(args, **kw):
            seen.append(args)
            return Answer(1 if args[3] == 'tools.effective' else 0)
        ok, seconds = mc.warm_up({'openclaw': 'oc'}, run=run, clock=iter([10.0, 12.5]).__next__)
        self.assertEqual((ok, seconds), (False, 2.5))
        self.assertEqual([s[:4] for s in seen], [['oc', 'gateway', 'call', m] for m in ('sessions.create', 'tools.effective', 'sessions.delete')])
        self.assertEqual(json.loads(seen[2][seen[2].index('--params') + 1]), {'key': mc.WARM_KEY, 'deleteTranscript': True})
        self.assertFalse(any(word in s for s in seen for word in ('agent', 'infer', 'chat.send')))  # no model call
        def gone(args, **kw):
            raise OSError('no openclaw')
        self.assertFalse(mc.warm_up({}, run=gone)[0])


class Check(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.openclaw = Path(self.temp.name) / 'openclaw.json'
        self.openclaw.write_text(json.dumps({'agents': {'defaults': {'model': MAIN}}}))
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'gateway', 'service': 'gateway'}, {'id': 'work', 'service': 'gmail'}],
                           'review_worker': {'enabled': False}, 'delivery_enabled': False, 'openclaw_config': str(self.openclaw)}
        self.ready = True  # a sign-in or key exists (OpenClaw's `models status`)
        for name, value in (('main_model', lambda *x: MAIN), ('model_ready', lambda *x, **k: self.ready)):
            p = patch_everywhere(a, name, side_effect=value); p.start(); self.addCleanup(p.stop)
        self.app.chat_catalog = type('Catalog', (), {'refresh': lambda s, config: [{'ref': MAIN}, {'ref': OTHER}]})()
        self.store.commit_page('work', {}, [mail(f'm{n}', days_ago=3) for n in range(5)])

    def later(self, minutes):
        return patch_everywhere(a, 'now', return_value=(dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=minutes)).isoformat(timespec='seconds'))

    def look(self, minutes=0):
        with self.later(minutes), self.store.connect() as db:
            return self.app.first_look(db)

    def checked(self, model, minutes=0):
        with self.later(minutes):
            return self.app.model_check_run(MAIN, True, model)

    def due(self, minutes=0):
        with self.later(minutes), self.store.connect() as db:
            return mc.due(mc.last(db), MAIN, mc.sign_in_stamp(self.app.config), dt.datetime.fromisoformat(a.now()))

    def test_a_sign_in_still_pending_checks_nothing_and_the_first_look_waits(self):
        self.ready = False
        self.assertEqual(self.look()['why'], 'model')
        self.assertIsNone(self.app.model_check_kick())  # no sign-in yet: no call
        self.ready = True
        # Signed in, not checked yet: the first look still waits, for the check, not for a sign-in
        look = self.look()
        self.assertEqual((look['state'], look['why']), ('waiting', 'model_check'))
        self.assertNotIn('error', look)
        self.assertTrue(self.due())
        self.checked(StandIn(main=(True, None)))
        self.assertEqual(self.look()['state'], 'due')
        self.assertFalse(self.due(600))  # an AI that answered isn't checked again

    def test_a_failed_check_has_a_line_about_the_plan_only_where_the_account_may_be_why(self):
        status = {'model': MAIN, 'chatgpt': False, 'claude_plan': True, 'plan': None, 'limit_reached': False}
        with self.assertLogs(a.LOG, 'INFO'):
            self.checked(StandIn(main=(False, '403 forbidden')))
        self.assertNotIn('plan', self.look())  # no sign-in known: nothing said
        self.app.model_status = status
        self.assertEqual(self.look()['plan'], 'claude')
        self.assertNotIn('plan_free', self.look())
        found = {'model': MAIN, 'ok': False, 'error': '403 forbidden'}
        self.assertEqual(mc.plan_note(found, {**status, 'plan': 'free'}), {'plan': 'claude', 'plan_free': True})
        self.assertEqual(mc.plan_note(found, {**status, 'chatgpt': True, 'plan': 'Free ($0.00)'}), {'plan': 'chatgpt', 'plan_free': True})
        for plan in (None, 'go', 'plus', 'self serve business'):  # ChatGPT: only when it says the account is free
            self.assertEqual(mc.plan_note(found, {**status, 'chatgpt': True, 'claude_plan': False, 'plan': plan}), {}, plan)
        for error in mc.NOT_REACHED:  # our own trouble
            self.assertEqual(mc.plan_note({**found, 'error': error}, status), {})
        for other in ({'plan': 'max'}, {'plan': 'team'}, {'limit_reached': True}, {'model': OTHER}, {'claude_plan': False}):
            self.assertEqual(mc.plan_note(found, {**status, **other}), {}, other)

    def test_a_failed_call_keeps_the_owner_on_the_ai_step_and_a_reconnect_starts_the_first_look_at_once(self):
        with self.assertLogs(a.LOG, 'INFO'):
            self.checked(StandIn(main=(False, 'Claude Code is not signed in. Run claude login.')))
        look = self.look()
        self.assertEqual((look['why'], look['error']), ('model_check', 'Claude Code is not signed in. Run claude login.'))
        self.assertEqual(self.app.review_step(Runner()), None)  # no first look on an AI that doesn't answer
        with self.store.connect() as db:
            report = a.first_cards_report(db, self.app.config['accounts'])
        self.assertEqual((report['model_check']['ok'], report['model_check']['error']), (False, 'Claude Code is not signed in. Run claude login.'))
        # Comes round again by itself: a minute, two, then every five
        self.assertFalse(self.due(0.5))
        self.assertTrue(self.due(1.1))
        with self.assertLogs(a.LOG, 'INFO'):
            self.checked(StandIn(main=(False, 'still not')), 1.1)
        self.assertFalse(self.due(2.5))
        self.assertTrue(self.due(3.2))
        # The owner signs in again: checked at once, not after the backoff
        os.utime(self.openclaw, (1, 1))
        self.assertTrue(self.due(1.6))
        with self.assertLogs(a.LOG, 'INFO'):
            self.checked(StandIn(main=(True, None)), 1.6)
        self.assertEqual(self.look(1.6)['state'], 'due')
        runner = Runner('admitted')
        with self.later(2):
            self.assertEqual(self.app.review_step(runner), 'admitted')
        self.assertNotIn('model', runner.requests[0])  # on the main model

    def test_every_failed_check_counts_in_the_error_reports_as_one_signature(self):
        """A check that failed hundreds of times in a row only ever logged a line, so the error reports never showed it."""
        import error_feed
        with self.assertLogs(a.LOG, 'INFO'):
            self.checked(StandIn(main=(False, 'No API key found for provider "anthropic".')))
            self.checked(StandIn(main=(False, 'No API key found for provider "anthropic".')), 1.1)
            self.checked(StandIn(main=(True, None)), 3.2)
        with self.store.connect() as db:
            error_feed.ensure(db)
            rows = [dict(r) for r in db.execute('SELECT source,kind,location,count FROM error_feed')]
        self.assertEqual(rows, [{'source': 'service', 'kind': 'ModelCheckFailed', 'location': 'machine/app/first_look.py:model_check_run', 'count': 2}])

    def test_a_failed_first_look_comes_back_within_minutes(self):
        self.checked(StandIn(main=(True, None)))
        with self.later(1):
            self.assertEqual(self.app.review_step(Runner('admitted')), 'admitted')
        for minutes in (2, 10, 20, 30):  # failure after failure: never more than five minutes apart
            with self.later(minutes), self.store.connect() as db:
                db.execute("UPDATE review_runs SET status='error',error='runtime_error',finished_at=? WHERE finished_at IS NULL", (a.now(),))
            self.assertEqual(self.look(minutes + 0.5)['why'], 'retry')
            self.assertEqual(self.look(minutes + 5.1)['state'], 'due')
            with self.later(minutes + 5.1):
                self.assertEqual(self.app.review_step(Runner('admitted')), 'admitted')
        # A rate limit still waits out the limit
        with self.later(40), self.store.connect() as db:
            db.execute("UPDATE review_runs SET status='error',error='rate_limited',finished_at=? WHERE finished_at IS NULL", (a.now(),))
        self.assertEqual(self.look(46)['why'], 'retry')

    def test_with_reviews_on_a_failed_first_review_comes_back_within_minutes(self):
        self.app.config['review_worker'] = {'enabled': True}
        self.checked(StandIn(main=(True, None)))
        with self.later(1):
            self.assertEqual(self.app.review_step(Runner('admitted')), 'admitted')
        for n, minutes in enumerate((2, 8, 14, 20, 26)):
            with self.later(minutes), self.store.connect() as db:
                db.execute("UPDATE review_runs SET status='error',error='runtime_error',finished_at=? WHERE finished_at IS NULL", (a.now(),))
            with self.later(minutes + 5.1):
                self.assertEqual(self.app.review_step(Runner('admitted')), 'admitted', n)

    def test_another_signed_in_ai_carries_the_first_look_while_the_main_one_fails(self):
        model = StandIn(main=(False, '529 overloaded'), **{OTHER: (True, None)})
        with self.assertLogs(a.LOG, 'INFO'):
            self.checked(model)
        self.assertEqual(model.calls, [None, OTHER])  # the main model, then the other provider's
        self.assertEqual(self.look()['state'], 'due')
        runner = Runner('admitted')
        with self.later(1):
            self.assertEqual(self.app.review_step(runner), 'admitted')
        self.assertEqual((runner.requests[0]['provider'], runner.requests[0]['model']), ('openai-codex', 'gpt-6.1-sol'))
        # The main model answers again: the next first look goes back to it
        with self.later(2), self.store.connect() as db:
            db.execute("UPDATE review_runs SET status='error',error='runtime_error',finished_at=? WHERE finished_at IS NULL", (a.now(),))
        with self.later(3), self.assertLogs(a.LOG, 'INFO'):
            self.app.model_check_run(MAIN, True, StandIn(main=(True, None), **{OTHER: (True, None)}))
        with self.store.connect() as db:
            self.assertTrue(mc.passed(db, MAIN))

    def test_a_first_look_that_failed_on_a_working_main_model_tries_another_ai(self):
        self.checked(StandIn(main=(True, None)))
        with self.later(1):
            self.assertEqual(self.app.review_step(Runner('admitted')), 'admitted')
        with self.later(2), self.store.connect() as db:
            db.execute("UPDATE review_runs SET status='error',error='runtime_error',finished_at=? WHERE finished_at IS NULL", (a.now(),))
        other = StandIn(**{OTHER: (True, None)})
        with self.later(2.5), self.assertLogs(a.LOG, 'INFO'):
            self.app.model_check_run(MAIN, False, other)
        self.assertEqual(other.calls, [OTHER])  # the main model isn't checked again, the other one is
        runner = Runner('admitted')
        with self.later(7):
            self.assertEqual(self.app.review_step(runner), 'admitted')
        self.assertEqual(runner.requests[0]['model'], 'gpt-6.1-sol')

    def test_no_other_ai_signed_in_keeps_waiting_on_the_main_one(self):
        self.app.chat_catalog = type('Catalog', (), {'refresh': lambda s, config: [{'ref': 'claude-cli/claude-sonnet-5-5'}]})()
        model = StandIn(main=(False, 'expired'))
        with self.assertLogs(a.LOG, 'INFO'):
            self.checked(model)
        self.assertEqual(model.calls, [None])  # the same provider is no fallback
        self.assertEqual(self.look()['why'], 'model_check')

    def test_the_agent_runtime_is_warmed_once_after_a_passed_check_and_before_any_review(self):
        warmed = []
        self.app.model_warm_up = lambda config: warmed.append(config) or (True, 1.0)
        with self.assertLogs(a.LOG, 'INFO'):
            self.checked(StandIn(main=(False, 'expired')))
        self.assertEqual(warmed, [])  # a failed check warms nothing
        with self.assertLogs(a.LOG, 'INFO'):
            self.checked(StandIn(main=(True, None)), minutes=2)
            self.checked(StandIn(main=(True, None)), minutes=60)
        self.assertEqual(len(warmed), 1)  # once per start
        self.app._agent_warmed = False
        with self.store.connect() as db:
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at) VALUES('r1','ok',?,?)", (a.now(), a.now()))
        self.assertIsNone(self.app.agent_warm_up())  # a review already ran: nothing left to warm for
        self.assertEqual(len(warmed), 1)
        del self.app.model_warm_up
        self.app._agent_warmed = False
        self.assertIsNone(self.app.agent_warm_up(run=StandIn()))  # a stand-in check never reaches the real Gateway


if __name__ == '__main__':
    unittest.main()
