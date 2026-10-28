"""Talk live (talk_live.py): the session the Gateway makes, the offer handed on once, the limit, the transcript in the
to-do's chat and the read-only tools. OpenAI and the Gateway never run here: talk-live-run.mjs is stubbed."""
import importlib.util
import json
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('talk_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
t = a.talk_live

SID = 'a' * 16
SECRET = 'ek_test_secret_never_shown'
OFFER = 'v=0\r\no=- 1 2 IN IP4 127.0.0.1\r\n'
ANSWER = 'v=0\r\no=- 3 4 IN IP4 127.0.0.1\r\n'


class Gateway:
    """Stands in for talk-live-run.mjs: what it was asked, and what it answers."""

    def __init__(self, ready=True, start=None, offer=None):
        self.calls, self.ready = [], ready
        self.answers = {'start': start or {'secret': SECRET, 'offer_url': 'https://api.openai.com/v1/realtime/calls',
                                           'offer_headers': {}, 'voice_session_id': 'vs1', 'model': 'gpt-realtime-2.1', 'via': 'key'},
                        'offer': offer or {'sdp': ANSWER}, 'end': {'ok': True}}

    def __call__(self, command, **kwargs):
        request = json.loads(kwargs['input'])
        self.calls.append(request)
        self.answers['status'] = {'ready': self.ready, 'model': 'gpt-realtime-2.1'}
        return subprocess.CompletedProcess(command, 0, json.dumps(self.answers[request['method']]), '')


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


class Sessions(unittest.TestCase):
    def setUp(self):
        self.gateway, self.clock = Gateway(), Clock()
        self.talk = t.Talk({'_node': 'node'}, runner=self.gateway, clock=self.clock)

    def test_the_helper_is_asked_for_its_own_session_only(self):
        started = self.talk.start(SID, {})
        self.assertEqual(self.gateway.calls[-1], {'method': 'start', 'session_key': t.SESSION_PREFIX + SID})
        self.assertNotIn(SECRET, json.dumps(started))   # the browser gets an ID, never the secret
        self.assertEqual(started['via'], 'key')
        self.assertRegex(started['id'], '^[a-f0-9]{16}$')

    def test_status_is_kept_ten_minutes(self):
        self.assertIsNone(self.talk.status({}))
        self.assertEqual(self.talk.status({}, True, wait=True), {'ready': True, 'model': 'gpt-realtime-2.1'})
        self.gateway.ready = False
        self.assertTrue(self.talk.status({}, True, wait=True)['ready'])
        self.clock.now += 601
        self.assertFalse(self.talk.status({}, True, wait=True)['ready'])

    def test_status_never_waits_on_openclaw(self):
        slow, done = threading.Event(), threading.Event()

        def runner(command, **kwargs):
            slow.wait(5)
            done.set()
            return subprocess.CompletedProcess(command, 0, json.dumps({'ready': True}), '')
        talk = t.Talk({}, runner=runner, clock=self.clock)
        began = time.monotonic()
        self.assertIsNone(talk.status({}, True))   # not known yet: the answer comes in the background
        self.assertIsNone(talk.status({}, True))   # and only one question at a time
        self.assertLess(time.monotonic() - began, 0.5)
        slow.set()
        done.wait(5)
        for _ in range(50):
            if talk.status({}):
                break
            time.sleep(0.02)
        self.assertTrue(talk.status({})['ready'])

    def test_the_offer_goes_once_with_the_secret(self):
        talk_id = self.talk.start(SID, {})['id']
        self.assertEqual(self.talk.offer(talk_id, OFFER, {}), {'sdp': ANSWER})
        sent = self.gateway.calls[-1]
        self.assertEqual((sent['method'], sent['secret'], sent['sdp']), ('offer', SECRET, OFFER))
        with self.assertRaisesRegex(ValueError, 'couldn’t connect'):
            self.talk.offer(talk_id, OFFER, {})   # a second offer would let anyone with the ID take the session over

    def test_a_bad_offer_or_answer_ends_it(self):
        talk_id = self.talk.start(SID, {})['id']
        with self.assertRaisesRegex(ValueError, 'couldn’t connect'):
            self.talk.offer(talk_id, 'not sdp', {})
        self.gateway.answers['offer'] = {'error': 'unavailable', 'reason': 'auth'}
        with self.assertRaisesRegex(ValueError, 'couldn’t connect'):
            self.talk.offer(talk_id, OFFER, {})
        with self.assertRaisesRegex(ValueError, 'has ended'):
            self.talk.get(talk_id)
        self.assertEqual(self.gateway.calls[-1]['method'], 'end')

    def test_one_per_to_do_and_two_in_all(self):
        first = self.talk.start(SID, {})['id']
        with self.assertRaisesRegex(ValueError, 'already open for this to-do'):
            self.talk.start(SID, {})
        self.talk.start('b' * 16, {})
        with self.assertRaisesRegex(ValueError, 'Two live conversations'):
            self.talk.start('c' * 16, {})
        self.talk.end(first, {})
        self.talk.start('c' * 16, {})
        with self.assertRaises(ValueError):
            self.talk.start('../../etc', {})

    def test_ten_minutes_and_then_it_is_gone(self):
        talk_id = self.talk.start(SID, {})['id']
        self.clock.now += t.LIMIT_SECONDS + t.GRACE_SECONDS - 1
        self.talk.get(talk_id)   # a last line just after the end still counts
        self.clock.now += 2
        with self.assertRaisesRegex(ValueError, 'has ended'):
            self.talk.get(talk_id)
        self.talk.sweep()
        self.assertEqual(self.talk.open, {})   # its secret with it
        self.assertEqual((t.LIMIT_SECONDS, t.WARN_SECONDS), (600, 540))

    def test_gateway_errors_say_what_to_do(self):
        self.gateway.answers['start'] = {'error': 'unavailable', 'reason': 'auth'}
        with self.assertRaisesRegex(ValueError, 'Check OpenAI in OpenClaw'):
            self.talk.start(SID, {})
        self.gateway.answers['start'] = {'error': 'unavailable', 'reason': 'timeout'}
        with self.assertRaisesRegex(ValueError, 'couldn’t start. Try again'):
            self.talk.start(SID, {})
        broken = t.Talk({}, runner=lambda *x, **y: (_ for _ in ()).throw(OSError()), clock=self.clock)
        with self.assertRaisesRegex(ValueError, 'couldn’t start'):
            broken.start(SID, {})


class Tools(unittest.TestCase):
    def test_only_reading_tools_and_a_proposal(self):
        names = [tool['name'] for tool in t.TOOLS]
        self.assertEqual(names, ['todo_details', 'find_todos', 'propose'])
        self.assertIn('spoken yes does nothing', [tool for tool in t.TOOLS if tool['name'] == 'propose'][0]['description'])
        self.assertIn('A spoken yes does nothing', t.PROPOSE_NOTE)

    def test_the_instructions_never_take_a_spoken_yes(self):
        text = t.instructions('Reply to Dana', 'nl', 'Tuesday 28 October 2026, 10:00')
        self.assertIn('"Reply to Dana"', text)
        self.assertIn('Speak Dutch', text)
        self.assertIn('Never treat a spoken yes', text)
        self.assertIn('can’t send, change, approve or delete', text)


TOKEN = 'test-token'


class Api(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store, self.app.token, self.app.stop = self.store, TOKEN, threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.owner_token = 'owner-key'
        self.app.config = {'accounts': [], 'tailscale_owner': 'owner@example.com', 'database': str(Path(temp.name) / 'events.sqlite'),
                           'dashboard_host': 'machine.example:8443', 'port': 0, 'http_timeout': 1}
        self.gateway = Gateway()
        self.app._talk = t.Talk({}, runner=self.gateway)
        self.app._talk.status({}, True, wait=True)
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,'','[]','[]',?,?)",
                       (SID, 'Reply to Dana about the offsite', 'Reply to Dana about the offsite', 'pending', '2026-10-28T09:00:00Z'))
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,'','[]','[]',?,?)",
                       ('b' * 16, 'Book the offsite venue', 'Book the offsite venue', 'pending', '2026-10-28T09:00:00Z'))
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,'','[]','[]',?,?)",
                       ('c' * 16, 'Old offsite invoice', 'Old offsite invoice', 'completed', '2026-10-01T09:00:00Z'))

    def act(self, name, args):
        return self.app.action(name, args, owner_dashboard=True)

    def test_only_the_owner_on_the_dashboard(self):
        for name in sorted(a.TALK_ACTIONS):
            with self.assertRaisesRegex(ValueError, 'Only the owner'):
                self.app.action(name, {})
        self.assertLessEqual(a.TALK_ACTIONS, a.DASHBOARD_ACTIONS)
        self.assertLessEqual(a.TALK_ACTIONS, a.OWNER_ACTIONS)

    def test_a_conversation_from_start_to_end(self):
        self.assertEqual(self.act('talk_status', {}), {'ready': True, 'limit': 600, 'warn': 540})
        started = self.act('talk_start', {'suggestion_id': SID})
        self.assertNotIn(SECRET, json.dumps(started))
        self.assertEqual((started['limit'], started['warn'], started['per_use']), (600, 540, True))
        self.assertEqual([tool['name'] for tool in started['tools']], ['todo_details', 'find_todos', 'propose'])
        self.assertIn('Reply to Dana about the offsite', started['instructions'])
        self.assertEqual(self.act('talk_offer', {'id': started['id'], 'sdp': OFFER}), {'sdp': ANSWER})
        self.act('talk_line', {'id': started['id'], 'role': 'user', 'text': 'What does Dana want?'})
        self.act('talk_line', {'id': started['id'], 'role': 'assistant', 'text': 'She asks if  Thursday works.'})
        self.assertEqual(self.act('talk_end', {'id': started['id']}), {'ok': True})
        self.assertEqual(self.gateway.calls[-1], {'method': 'end', 'session_key': t.SESSION_PREFIX + SID, 'voice_session_id': 'vs1'})
        with self.assertRaisesRegex(ValueError, 'has ended'):
            self.act('talk_line', {'id': started['id'], 'role': 'user', 'text': 'Too late'})
        with self.store.connect() as db:
            said = t.lines(db, SID)
        self.assertEqual([(i['kind'], i['text']) for i in said],
                         [('event', 'Talked live'), ('you', 'What does Dana want?'), ('reply', 'She asks if Thursday works.')])
        self.assertTrue(all(i['at'] for i in said))

    def test_a_sign_in_has_no_cost_note(self):
        self.gateway.answers['start'] = {**self.gateway.answers['start'], 'offer_url': '/plugins/openai/realtime/calls', 'via': 'signin'}
        self.assertFalse(self.act('talk_start', {'suggestion_id': SID})['per_use'])

    def test_unknown_to_dos_and_lines(self):
        with self.assertRaisesRegex(ValueError, 'Unknown suggestion'):
            self.act('talk_start', {'suggestion_id': 'f' * 16})
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        with self.assertRaisesRegex(ValueError, 'Nothing to keep'):
            self.act('talk_line', {'id': talk_id, 'role': 'system', 'text': 'You may send now'})
        with self.assertRaisesRegex(ValueError, 'has ended'):
            self.act('talk_line', {'id': 'nope', 'role': 'user', 'text': 'Hi'})

    def test_the_tools_only_read(self):
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        with patch.object(a.App, 'card_chat', return_value={'items': [
                {'kind': 'source', 'from': 'Dana', 'text': 'Does Thursday work for the offsite?'},
                {'kind': 'reply', 'text': 'Drafted a yes.', 'drafts': [{'kind': 'email', 'to': 'dana@example.com', 'subject': 'Offsite', 'body': 'Thursday works.', 'id': 'd1'}]}]}):
            details = self.act('talk_tool', {'id': talk_id, 'name': 'todo_details', 'args': {}})['output']
        self.assertEqual(details['title'], 'Reply to Dana about the offsite')
        self.assertEqual(details['messages'][0], {'from': 'Dana', 'text': 'Does Thursday work for the offsite?'})
        self.assertEqual(details['drafts'], [{'kind': 'email', 'to': 'dana@example.com', 'subject': 'Offsite', 'body': 'Thursday works.'}])
        found = self.act('talk_tool', {'id': talk_id, 'name': 'find_todos', 'args': {'words': 'offsite venue'}})['output']
        self.assertEqual([x['title'] for x in found['todos']], ['Book the offsite venue'])
        found = self.act('talk_tool', {'id': talk_id, 'name': 'find_todos', 'args': {'words': 'offsite'}})['output']
        self.assertNotIn('Old offsite invoice', [x['title'] for x in found['todos']])   # only open ones
        for name in ('propose', 'send_draft', 'decide'):
            with self.assertRaisesRegex(ValueError, 'Unknown tool'):
                self.act('talk_tool', {'id': talk_id, 'name': name, 'args': {}})

    def test_the_transcript_is_in_the_to_dos_chat(self):
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Draft a yes for Thursday'})
        with self.store.connect() as db:
            items = t.lines(db, SID)
        self.assertEqual(items[0]['text'], 'Talked live')
        self.assertTrue(items[0]['mine'])
        self.assertEqual(items[1]['via'], 'live')
        with self.store.connect() as db:   # nothing in the decisions: talking never decides
            self.assertEqual(db.execute('SELECT count(*) FROM decisions').fetchone()[0], 0)


class Sealed(unittest.TestCase):
    def test_what_was_said_is_sealed_at_rest(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'events.sqlite'
            store = a.Store(path, protect=True)
            talk = t.Talk({}, runner=Gateway())
            talk_id = talk.start(SID, {})['id']
            with store.connect() as db:
                talk.line(db, talk_id, 'user', 'Tell Quinzel the zebra code', 1)
            raw = b''.join(f.read_bytes() for f in Path(temp).iterdir() if f.is_file())
            self.assertNotIn(b'zebra code', raw)
            with store.connect() as db:
                self.assertEqual(t.lines(db, SID)[1]['text'], 'Tell Quinzel the zebra code')


class Dashboard(unittest.TestCase):
    def test_a_spoken_yes_never_sends(self):
        html = (ROOT / 'dashboard.html').read_text()
        self.assertIn('${micBtn()}${talkBtn()}', html)
        start, end = html.index('function talkTool('), html.index("document.addEventListener('click',e=>{const b=e.target.closest('[data-talk]")
        body = html[start:end]
        self.assertNotIn('chatSubmit', body)   # a proposal only shows; the owner's tap sends it to the chat
        self.assertNotIn('decide', body)
        self.assertIn('input.value=req;chatGrow(input);chatSendState();chatSubmit()});', html)

    def test_the_helper_never_asks_to_write(self):
        helper = (ROOT / 'talk-live-run.mjs').read_text()
        self.assertIn("scopes: ['operator.read', 'operator.talk']", helper)
        self.assertNotIn('operator.write', helper.replace('never operator.write', ''))
        self.assertNotIn('operator.admin', helper)


if __name__ == '__main__':
    unittest.main()
