"""A run's start always fits what the runner takes, and one that can never go out ends at once (start_message.py)."""
import datetime as dt
import json
import logging
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from seams import patch_everywhere
from machine.app import start_message
import machine.app.preparation as preparation
import machine.main as machine_main
import timeutil

LIMIT = preparation.PROMPT_LIMIT
REFUSED = {'status': 'error', 'error': 'prompt_too_long', 'error_phase': 'runtime'}


class Message(unittest.TestCase):
    def test_the_least_needed_goes_first_and_the_order_stays(self):
        start = start_message.StartMessage(3000, 'TAIL')
        start.base = 'BASE'
        dropped = []
        start.add('records', 'r' * 900, start_message.RECORDS, lambda: dropped.append('records'))
        start.add('related', 'x' * 900, start_message.RELATED, lambda: dropped.append('related'))
        start.add('agent', 'a' * 900, start_message.OWNER)
        text = start.text()
        self.assertLessEqual(len(text), 3000)
        self.assertEqual(dropped, ['related'])
        self.assertTrue(text.startswith('BASE' + 'r' * 900 + 'a' * 900 + '\n\nLeft out of this message'))
        self.assertIn('(read with assistant_signals related)', text)
        self.assertTrue(text.endswith('TAIL'))

    def test_everything_fits_unchanged_without_a_note(self):
        start = start_message.StartMessage(3000, 'TAIL')
        start.base = 'BASE'
        start.add('agent', 'A', start_message.OWNER)
        start.add('none', '', start_message.OWNER)
        self.assertEqual(start.text(), 'BASEATAIL')

    def test_the_note_fits_its_reserve(self):
        self.assertLess(len(start_message.left_out(list(start_message.READS))), start_message.RESERVE)

    def test_the_instructions_give_up_their_parts_in_order(self):
        build = lambda p: 'fixed' + p['facts'] + p['style']
        self.assertEqual(start_message.trimmed(build, {'facts': 'f' * 9, 'style': 's' * 9}, ('style', 'facts'), 100), ('fixed' + 'f' * 9 + 's' * 9, []))
        self.assertEqual(start_message.trimmed(build, {'facts': 'f' * 9, 'style': 's' * 9}, ('style', 'facts'), 14), ('fixed' + 'f' * 9, ['style']))
        self.assertEqual(start_message.trimmed(build, {'facts': 'f' * 9, 'style': 's' * 9}, ('style', 'facts'), 5), ('fixed', ['style', 'facts']))


class Start(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': timeutil.now(),
                                             'title': 'Evidence', 'body': 'Actual evidence', 'metadata': {}, 'deleted': False}])
        self.sid = self.store.suggest('task', 'Prepare a useful draft', 'I can draft this.', [1])['id']
        self.app = object.__new__(machine_main.App)
        self.app.store, self.app.config = self.store, {'accounts': []}
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.calls = []

    def q(self, sql, *args):
        with self.store.connect() as db:
            return dict(db.execute(sql, args).fetchone())

    def job(self):
        return self.q('SELECT * FROM preparations WHERE suggestion_id=?', self.sid)

    def do(self, sql, *args):
        with self.store.connect() as db:
            db.execute(sql, args)

    def step(self, receipt=None):
        receipt = receipt or {'status': 'admitted'}
        self.calls.clear()
        self.app.preparation_step(lambda r: self.calls.append(r) or (receipt if r['action'] == 'start' else {'status': 'pending'}))
        return next((c for c in self.calls if c['action'] == 'start'), None)

    def continues(self):
        """The owner asks again: a new run in the same session."""
        self.step()
        self.do("UPDATE preparation_runs SET status='ok',finished_at=?", timeutil.now())
        self.do("UPDATE preparations SET job_id=?,session_job_id=job_id,status='queued',retry_at=NULL,started_at=NULL WHERE suggestion_id=?", 'b' * 32, self.sid)

    def rich(self, **blocks):
        """What the run would read of what was learned: {block: text}."""
        real = preparation.recall

        def recalled(app, purpose, about, budget):
            memory = real(app, purpose, about, budget)
            for name, text in blocks.items():
                memory.pickers[name] = lambda *a, text=text, **k: text
            return memory
        return patch_everywhere(preparation, 'recall', recalled)

    def test_a_continued_session_with_rich_memory_stays_within_the_limit(self):
        # 2026-11-24: related messages filled the start up to 500 short of the limit, the note that the session carries on
        # came after, and the runner refused it: "waiting for the AI" for 35 minutes. The newest agent work fell off too.
        self.continues()
        room = LIMIT - 24_000
        for size in range(room - 12_000, room + 6_000, 1_500):
            with self.subTest(size=size), self.rich(related='\n\nRELATED ' + 'x' * size, records='\n\nRECORDS ' + 'r' * 4000), \
                    patch.object(type(self.app), 'agent_work', lambda app, sid: '\nAgent work: newest.'):
                self.do("UPDATE preparation_runs SET status='ok',finished_at=?", timeutil.now())
                self.do("UPDATE preparations SET status='queued',retry_at=NULL,started_at=NULL")
                message = self.step()['message']
                self.assertLessEqual(len(message), LIMIT)
                self.assertIn('Agent work: newest.', message)
                self.assertTrue(message.endswith(preparation.SAME_SESSION))
                self.assertEqual('RELATED' in message, 'assistant_signals related)' not in message)

    def test_everything_at_once_still_fits(self):
        self.continues()
        big = {name: f'\n\n{name.upper()} ' + 'z' * 30_000 for name in ('facts', 'rules', 'retained', 'records', 'related', 'skills')}
        with self.rich(**big), patch.object(type(self.app), 'agent_work', lambda app, sid: '\nAgent work: newest.'), \
                patch.object(preparation.recurring, 'prep_lines', lambda *a, **k: '\nrecurring ' + 'y' * 30_000):
            message = self.step()['message']
        self.assertLessEqual(len(message), LIMIT)
        self.assertIn('Agent work: newest.', message)
        self.assertTrue(message.endswith(preparation.SAME_SESSION))

    def test_a_chat_message_fits_too(self):
        self.continues()
        self.do("UPDATE preparations SET decision_id='chat-one' WHERE suggestion_id=?", self.sid)
        with self.rich(new='n' * 40_000, retained='o' * 40_000):
            message = self.step()['message']
        self.assertLessEqual(len(message), LIMIT)
        self.assertTrue(message.startswith('The owner wrote to you in the chat'))
        self.assertTrue(message.endswith(preparation.SAME_SESSION))

    def test_what_is_left_out_does_not_count_as_read(self):
        with self.rich(related='x' * 50_000):
            request = self.step()
        self.assertNotIn('x' * 100, request['message'])
        self.assertFalse([r for r in request.get('_memory') or [] if r[0] == 'message'])

    def test_a_start_that_can_never_go_out_is_stuck_at_once(self):
        for code in sorted(start_message.REFUSED):
            with self.subTest(code=code):
                self.do("UPDATE preparations SET status='queued',retry_at=NULL,started_at=NULL,error=NULL")
                self.step({**REFUSED, 'error': code})
                job = self.job()
                self.assertEqual((job['status'], job['error'], job['auto_retries']), ('blocked', code, 0))
                self.assertTrue(job['reason'])
                self.assertNotIn('AI', job['reason'])
                self.assertIsNone(self.step())

    def test_an_update_tries_it_once_more(self):
        self.step(REFUSED)
        self.do('UPDATE preparations SET updated_at=?', (dt.datetime.fromisoformat(timeutil.now()) - dt.timedelta(hours=1)).isoformat())
        self.store.code_version = 'release-a'
        self.assertIsNotNone(self.step())

    def node(self, *receipts):
        self.sent, queue = [], list(receipts)

        def run(command, input=None, **kw):
            self.sent.append(json.loads(input))
            receipt = queue.pop(0)
            if isinstance(receipt, Exception):
                raise receipt
            return type('R', (), {'returncode': 0 if receipt else 1, 'stdout': json.dumps(receipt)})()
        return patch.object(subprocess, 'run', side_effect=run)

    def test_every_kind_too_long_never_reaches_the_runner(self):
        for kind in ('review', 'routine', 'profile', 'skills'):
            request = {'action': 'start', 'kind': kind, 'job_id': 'c' * 32, 'message': 'secret ' * LIMIT, 'model': 'm'}
            with self.node(), self.assertLogs(preparation.LOG, logging.ERROR) as logs:
                self.assertEqual(self.app.preparation_gateway(request)['error'], 'prompt_too_long')
            self.assertEqual(self.sent, [])
            self.assertNotIn('secret', str(logs.output))

    def test_a_kept_start_that_is_too_long_is_built_again(self):
        # one kept by an earlier release: it never reached the Gateway, so nothing runs under its key
        self.do('INSERT INTO gateway_starts(job_id,request,created_at) VALUES(?,?,?)', 'd' * 32,
                json.dumps({'action': 'start', 'kind': 'routine', 'job_id': 'd' * 32, 'message': 'x' * (LIMIT + 1)}), timeutil.now())
        request = {'action': 'start', 'kind': 'routine', 'job_id': 'd' * 32, 'message': 'short', 'model': 'm'}
        with self.node({'status': 'admitted'}):
            self.assertEqual(self.app.preparation_gateway(request)['status'], 'admitted')
        self.assertEqual(self.sent[0]['message'], 'short')

    def test_a_kept_start_that_may_be_running_is_resent_even_when_the_new_one_is_too_long(self):
        first = {'action': 'start', 'kind': 'routine', 'job_id': 'd' * 32, 'message': 'short', 'model': 'm'}
        with self.node({'status': 'unavailable', 'reason': 'timeout'}, {'status': 'admitted'}):
            self.app.preparation_gateway(dict(first))
            self.assertEqual(self.app.preparation_gateway({**first, 'message': 'x' * (LIMIT + 1)})['status'], 'admitted')
        self.assertEqual([s['message'] for s in self.sent], ['short', 'short'])

    def test_why_a_call_was_unavailable_is_logged_once_as_a_code(self):
        status = {'action': 'status', 'kind': 'routine', 'job_id': 'e' * 32}
        with self.node({'status': 'unavailable', 'reason': 'timeout'}, {'status': 'unavailable', 'reason': 'timeout'},
                       {'status': 'unavailable', 'reason': 'some private words'}, None, subprocess.TimeoutExpired('node', 1)), \
                self.assertLogs(preparation.LOG, logging.WARNING) as logs:
            answers = [self.app.preparation_gateway(dict(status)) for _ in range(5)]
        self.assertEqual({a['status'] for a in answers}, {'unavailable'})
        self.assertEqual([r.getMessage().rsplit('reason=')[1] for r in logs.records], ['timeout', 'other', 'runner_failed', 'runner_timeout'])


if __name__ == '__main__':
    unittest.main()
