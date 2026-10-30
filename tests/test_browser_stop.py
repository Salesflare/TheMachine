"""Stop in the Browser view: the same stop as the chat's Stop (chat_stop), for the task on the tab the browser shows.
The run is refused any further step at once, its tab stops loading, its Gateway run is aborted right away (not on the
worker's next round), the half-done step is not retried, and its chat says "Stopped from the browser". Offline: no
browser, Gateway or site is contacted."""
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('browser_stop_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

TAB = 'A0F20ED451EA2A1247613CAB889F3BCB'
OTHER = 'DF829ED2FFBB4631972AF70080134B94'


def opened(target, label, port=9222):
    answer = {'targetId': target, 'url': 'https://example.org/', 'wsUrl': f'ws://127.0.0.1:{port}/devtools/page/{target}',
              'type': 'page', 'suggestedTargetId': label, 'tabId': 't1', 'label': label}
    text = '\n<<<EXTERNAL_UNTRUSTED_CONTENT id="x">>>\nSource: Browser\n---\n' + json.dumps(answer) + '\n<<<END_EXTERNAL_UNTRUSTED_CONTENT id="x">>>'
    return {'content': [{'type': 'text', 'text': text}]}


class FakeTab:
    """A DevTools session on one tab: records each call; says which tab is visible."""
    calls, visible = [], None

    def __init__(self, base, target, timeout=None):
        self.target = target

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def call(self, method, params=None):
        FakeTab.calls.append((self.target, method))
        if method == 'Runtime.evaluate':
            return {'result': {'value': 'visible' if self.target == FakeTab.visible else 'hidden'}}
        return {}


class BrowserStop(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = a.Store(self.root / 'events.sqlite')
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Evidence', 'body': 'Please pay the invoice', 'metadata': {}, 'deleted': False},
                                            {'account_id': 'work', 'source_id': 'two', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Room', 'body': 'Please book the room', 'metadata': {}, 'deleted': False}], None)
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [], 'database': str(self.root / 'events.sqlite')}
        FakeTab.calls, FakeTab.visible = [], None
        for p in (patch.object(a.browser_login.browser_cdp, 'Session', FakeTab),
                  patch.object(a, 'preparation_steps', return_value=[{'title': 'Filling in the payment form', 'at': None}])):
            p.start()
            self.addCleanup(p.stop)

    def task(self, title, target, label):
        """A to-do whose Do it run is going, on a tab it opened itself and then typed in."""
        sid = self.store.suggest('task-' + label, title, 'I can do this on the website.', [2 if target == OTHER else 1])['id']
        self.app.action('decide', {'suggestion_id': sid, 'choice': 'accept', 'feedback': '', 'decision_id': 'go-' + sid}, owner_dashboard=True)
        self.app.preparation_step(lambda r: {'status': 'admitted'})
        job = self.job(sid)['job_id']
        with self.store.connect() as db:
            self.assertEqual(a.preparation_state.tool_intent(db, {'job_id': job, 'call_id': 'o', 'tool': 'browser',
                                                                  'params': {'action': 'open', 'url': 'https://example.org/'}}, a.now()), {'active': True})
            a.preparation_state.tool_result(db, {'job_id': job, 'call_id': 'o', 'result': opened(target, label)}, a.now())
        with self.store.connect() as db:
            self.assertEqual(a.preparation_state.tool_intent(db, {'job_id': job, 'call_id': 't', 'tool': 'browser',
                                                                  'params': {'action': 'act', 'targetId': label, 'kind': 'type'}}, a.now()), {'active': True})
        return sid

    def job(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM preparations WHERE suggestion_id=?', (sid,)).fetchone())

    def stop(self, sid):
        """Stop as the Browser view presses it; returns what the immediate abort asked the Gateway."""
        asked, done = [], threading.Event()
        gateway = lambda r: asked.append(r) or done.set() or {'status': 'aborted'}
        with patch.object(self.app, 'preparation_gateway', gateway), \
                patch.object(self.app, 'card_chat_gateway', return_value={'messages': [], 'inFlightRun': None}):
            self.assertEqual(self.app.action('chat_stop', {'suggestion_id': sid, 'via': 'browser'}, owner_dashboard=True), {'stopped': True})
            self.assertTrue(done.wait(5), 'the run is aborted right away, not on the worker\'s next round')
            for t in [t for t in threading.enumerate() if t.name == 'browser-stop']:
                t.join(5)
        return asked

    def test_stop_from_the_browser_ends_the_run_at_once(self):
        sid = self.task('Pay the invoice', TAB, 'pay')
        now = self.app.browser_now()['working']
        self.assertEqual([(w['id'], w['title']) for w in now], [(sid, 'Pay the invoice')])  # what the Stop button stops
        job = self.job(sid)['job_id']
        asked = self.stop(sid)
        # The same stop as the chat's: waiting, stopped, with Try again; no further step is let through
        after = self.job(sid)
        self.assertEqual((after['status'], after['error'], after['reason']), ('blocked', 'stopped', a.CHAT_STOPPED))
        with self.store.connect() as db:
            refused = a.preparation_state.tool_intent(db, {'job_id': job, 'call_id': 'c', 'tool': 'browser',
                                                           'params': {'action': 'act', 'targetId': 'pay', 'kind': 'click'}}, a.now())
            self.assertFalse(refused['active'])
            run = db.execute('SELECT status,finished_at FROM preparation_runs WHERE job_id=?', (job,)).fetchone()
        # Its own tab stopped loading, and its exact run was aborted in its session
        self.assertIn((TAB, 'Page.stopLoading'), FakeTab.calls)
        self.assertEqual([(r['action'], r['job_id']) for r in asked], [('stop', job)])
        self.assertEqual(run['status'], 'aborted')
        self.assertTrue(run['finished_at'])
        # Nothing on the browser any more, and the worker doesn't start it again or retry the step it was on
        self.assertEqual(self.app.browser_now()['working'], [])
        started = []
        self.app.preparation_step(lambda r: started.append(r) or {'status': 'admitted'})
        self.assertEqual([r for r in started if r.get('action') == 'start'], [])
        self.assertEqual((self.job(sid)['status'], self.job(sid)['job_id']), ('blocked', job))
        # The chat says where it was stopped, once, as the owner's own event line
        with patch.object(self.app, 'card_chat_gateway', return_value={'messages': []}):
            items = self.app.card_chat(sid, None)['items']
        events = [i for i in items if i['kind'] == 'event' and 'Stopped' in i['text']]
        self.assertEqual([(i['text'], i.get('mine')) for i in events], [('Stopped from the browser', True)])
        self.assertFalse([i for i in items if i.get('stopped')])  # it had said nothing: no empty "Stopped" reply under it

    def test_the_chats_own_stop_is_unchanged(self):
        sid = self.task('Pay the invoice', TAB, 'pay')
        with patch.object(self.app, 'card_chat_gateway', return_value={'messages': [], 'inFlightRun': None}), \
                patch.object(self.app, 'preparation_gateway', side_effect=AssertionError('the chat waits for the worker')):
            self.assertEqual(self.app.action('chat_stop', {'suggestion_id': sid}, owner_dashboard=True), {'stopped': True})
        self.assertEqual(FakeTab.calls, [])
        with patch.object(self.app, 'card_chat_gateway', return_value={'messages': []}):
            items = self.app.card_chat(sid, None)['items']
        self.assertFalse([i for i in items if i['kind'] == 'event' and i['text'] == 'Stopped from the browser'])
        self.assertTrue([i for i in items if i.get('stopped')])

    def test_with_two_tasks_on_the_browser_the_one_in_front_is_first(self):
        first = self.task('Pay the invoice', TAB, 'pay')
        second = self.task('Book the room', OTHER, 'room')
        for visible, expect in ((TAB, [first, second]), (OTHER, [second, first])):
            FakeTab.visible = visible
            self.assertEqual([w['id'] for w in self.app.browser_now()['working']], expect)
        # Stopping the one in front leaves the other running
        self.stop(second)
        self.assertEqual(self.job(first)['status'], 'running')
        self.assertEqual([w['id'] for w in self.app.browser_now()['working']], [first])

    def test_stop_after_the_run_ended_does_nothing(self):
        sid = self.task('Pay the invoice', TAB, 'pay')
        self.store.preparation_blocked(sid, self.job(sid)['job_id'], 'The site asks for a code.')
        with patch.object(self.app, 'preparation_gateway', side_effect=AssertionError('nothing to abort')):
            self.assertEqual(self.app.action('chat_stop', {'suggestion_id': sid, 'via': 'browser'}, owner_dashboard=True), {'stopped': False})


if __name__ == '__main__':
    unittest.main()
