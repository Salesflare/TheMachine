"""The card chat's Stop button and the files added to a message (chat_files.py): Stop ends the running reply at once
and keeps what it said; files are checked, kept in the app's data folder, go with their message, and reach the run
(images as images, every file in its attachments folder)."""
import base64
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('chat_stop_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
chat_files = a.chat_files

PNG = b'\x89PNG\r\n\x1a\n' + b'\0' * 64
PDF = b'%PDF-1.4\n' + b'x' * 64
b64 = lambda data: base64.b64encode(data).decode()


class ChatStopFiles(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = a.Store(self.root / 'events.sqlite')
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Evidence', 'body': 'Actual evidence', 'metadata': {}, 'deleted': False}], None)
        self.sid = self.store.suggest('task', 'Reply to the venue', 'I can draft this.', [1])['id']
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [], 'database': str(self.root / 'events.sqlite')}
        workspace = patch.object(a, 'WORKSPACE', self.root / 'workspace')
        workspace.start()
        self.addCleanup(workspace.stop)

    def job(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM preparations WHERE suggestion_id=?', (self.sid,)).fetchone())

    def upload(self, name, data):
        return self.app.action('chat_upload', {'suggestion_id': self.sid, 'name': name, 'data': b64(data)}, owner_dashboard=True)

    def say(self, text, files=None, key='chat-1'):
        return self.app.action('decide', {'suggestion_id': self.sid, 'choice': 'other', 'feedback': text, 'decision_id': key,
                                          **({'files': files} if files else {})}, owner_dashboard=True)

    def run_turn(self):
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        return next(c for c in calls if c.get('action') == 'start')

    # Stop

    def test_stop_ends_the_run_at_once_and_keeps_what_it_said(self):
        self.say('Make it shorter')
        self.run_turn()
        job = self.job()
        self.assertEqual(job['status'], 'running')
        flight = {'messages': [], 'inFlightRun': {'runId': job['job_id'], 'text': 'Here is a shorter version: Dear venue'}}
        with patch.object(self.app, 'card_chat_gateway', return_value=flight):
            self.assertEqual(self.app.action('chat_stop', {'suggestion_id': self.sid}, owner_dashboard=True), {'stopped': True})
        job = self.job()
        self.assertEqual((job['status'], job['error'], job['reason']), ('blocked', 'stopped', a.CHAT_STOPPED))
        # The run may not do anything more, and the worker aborts it in its session right away (no settle wait)
        with self.store.connect() as db:
            refused = a.preparation_state.tool_intent(db, {'job_id': job['job_id'], 'call_id': 'c1', 'tool': 'browser', 'params': {}}, a.now())
        self.assertFalse(refused['active'])
        asked = []
        self.app.stop_stale_runs(lambda r: asked.append(r) or {'status': 'aborted'})
        self.assertEqual([(r['action'], r['job_id']) for r in asked], [('stop', job['job_id'])])
        # The chat keeps the partial answer, then says it stopped; nothing runs and Try again carries on
        with patch.object(self.app, 'card_chat_gateway', return_value={'messages': []}):
            chat = self.app.card_chat(self.sid)
        self.assertFalse(chat['active'])
        said = [(i['kind'], i['text']) for i in chat['items']][-3:]
        self.assertEqual(said, [('you', 'Make it shorter'), ('reply', 'Here is a shorter version: Dear venue'), ('event', 'Stopped')])
        self.store.decide(self.sid, 'retry', '', 'retry-1', 'dashboard')
        self.assertEqual(self.job()['status'], 'queued')

    def test_a_partial_answer_the_session_kept_shows_once(self):
        self.say('Make it shorter')
        self.run_turn()
        job = self.job()
        with patch.object(self.app, 'card_chat_gateway', return_value={'inFlightRun': {'text': 'Half an answer'}}):
            self.app.chat_stop(self.sid)
        history = {'messages': [{'role': 'assistant', 'content': [{'type': 'text', 'text': 'Half an answer'}], 'timestamp': a.chat_ms(a.now()),
                                 '__openclaw': {'runId': job['job_id']}}]}
        with patch.object(self.app, 'card_chat_gateway', return_value=history):
            chat = self.app.card_chat(self.sid)
        self.assertEqual([i['text'] for i in chat['items'] if i['kind'] == 'reply'], ['Half an answer'])

    def test_stop_after_the_reply_finished_changes_nothing(self):
        self.say('Make it shorter')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='done'")
        with patch.object(self.app, 'card_chat_gateway', side_effect=AssertionError('not asked')):
            self.assertEqual(self.app.chat_stop(self.sid), {'stopped': False})
        self.assertEqual(self.job()['status'], 'done')
        with self.assertRaises(ValueError):
            self.app.chat_stop('../x')

    def test_a_new_message_after_stop_starts_a_new_turn(self):
        self.say('Make it shorter')
        self.run_turn()
        with patch.object(self.app, 'card_chat_gateway', return_value={}):
            self.app.chat_stop(self.sid)
        self.say('Actually, make it warmer', key='chat-2')
        self.assertEqual(self.job()['status'], 'queued')

    # Files

    def test_files_go_with_their_message_and_reach_the_run(self):
        image = self.upload('screenshot.png', PNG)
        doc = self.upload('../../Quote.pdf', PDF)
        self.assertEqual((image['type'], doc['name'], doc['type']), ('image/png', 'Quote.pdf', 'application/pdf'))
        stored = Path(self.app.config['database']).parent / 'chat-files' / image['id']
        self.assertEqual(stored.read_bytes(), PNG)
        self.assertEqual(stored.stat().st_mode & 0o777, 0o600)
        self.say('What does this quote say?', [image['id'], doc['id']])
        start = self.run_turn()
        self.assertEqual(start['attachments'], [{'type': 'image', 'mimeType': 'image/png', 'fileName': 'screenshot.png', 'content': b64(PNG)}])
        folder = self.root / 'workspace' / 'data' / 'assistant-attachments' / self.job()['job_id'] / 'from-owner'
        self.assertEqual((folder / 'Quote.pdf').read_bytes(), PDF)
        self.assertIn(str(folder / 'Quote.pdf'), start['message'])
        self.assertIn('attached these files', start['message'])
        # The chat shows them with the message, and the dashboard can open each one
        with patch.object(self.app, 'card_chat_gateway', return_value={'messages': []}):
            you = next(i for i in self.app.card_chat(self.sid)['items'] if i['kind'] == 'you')
        self.assertEqual([f['name'] for f in you['files']], ['screenshot.png', 'Quote.pdf'])
        with self.store.connect() as db:
            self.assertEqual(chat_files.read(db, self.app.config, doc['id']), (PDF, 'application/pdf', 'Quote.pdf'))

    def test_only_files_is_a_message_too(self):
        image = self.upload('photo.jpg', b'\xff\xd8\xff' + b'1' * 10)
        self.say('', [image['id']])
        with patch.object(self.app, 'card_chat_gateway', return_value={'messages': []}):
            you = next(i for i in self.app.card_chat(self.sid)['items'] if i['kind'] == 'you')
        self.assertEqual((you['text'], len(you['files'])), ('', 1))
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT feedback FROM decisions WHERE id='chat-1'").fetchone()[0], a.CHAT_FILES_ONLY[0])

    def test_what_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'too big .*Images can be up to 5.0 MB'):
            self.upload('big.png', PNG + b'0' * chat_files.IMAGE_BYTES)
        with self.assertRaisesRegex(ValueError, 'can’t read that type'):
            self.upload('page.html', b'<script>alert(1)</script>')
        with self.assertRaisesRegex(ValueError, 'can’t read that type'):
            self.upload('fake.png', b'<svg onload=alert(1)>')  # a type is checked against its first bytes
        with self.assertRaisesRegex(ValueError, 'empty'):
            self.upload('empty.txt', b'')
        with self.assertRaises(ValueError):
            self.app.action('chat_upload', {'suggestion_id': '0' * 16, 'name': 'a.txt', 'data': b64(b'hi')}, owner_dashboard=True)
        # A file of another card, one sent already, or too many for one message never go along
        other = self.store.suggest('other-task', 'Another', 'Body', [1])['id']
        theirs = self.app.action('chat_upload', {'suggestion_id': other, 'name': 'a.txt', 'data': b64(b'hi')}, owner_dashboard=True)
        with self.assertRaisesRegex(ValueError, 'gone'):
            self.say('See this', [theirs['id']])
        mine = self.upload('a.txt', b'hi')
        self.say('See this', [mine['id']])
        with self.assertRaisesRegex(ValueError, 'gone'):
            self.say('Again', [mine['id']], key='chat-2')
        many = [self.upload(f'{n}.txt', b'hi')['id'] for n in range(chat_files.MAX_FILES + 1)]
        with self.assertRaisesRegex(ValueError, 'up to 5 files'):
            self.say('All of them', many, key='chat-3')
        # A refused message leaves its files waiting: nothing was bound
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM chat_files WHERE decision_id IS NULL AND suggestion_id=?', (self.sid,)).fetchone()[0], len(many))

    def test_an_upload_taken_back_and_old_unsent_ones_go(self):
        kept = self.upload('a.txt', b'hi')
        gone = self.upload('b.txt', b'bye')
        self.app.action('chat_file_remove', {'suggestion_id': self.sid, 'id': gone['id']}, owner_dashboard=True)
        folder = Path(self.app.config['database']).parent / 'chat-files'
        self.assertFalse((folder / gone['id']).exists())
        later = (a.dt.datetime.fromisoformat(a.now()) + a.dt.timedelta(hours=25)).isoformat()
        with self.store.connect() as db:
            self.assertEqual(chat_files.sweep(db, self.app.config, later), 1)
        self.assertFalse((folder / kept['id']).exists())

    def test_the_actions_are_the_owners_from_the_dashboard(self):
        for name in ('chat_stop', 'chat_upload', 'chat_file_remove'):
            self.assertIn(name, a.OWNER_ACTIONS)
            self.assertIn(name, a.DASHBOARD_ACTIONS)
        self.assertGreater(chat_files.REQUEST_BYTES, chat_files.FILE_BYTES * 4 // 3)


if __name__ == '__main__':
    unittest.main()
