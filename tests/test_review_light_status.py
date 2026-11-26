"""A signal review's status is light and read once (machine/app/review_status.py): every open to-do in short, every done one
as a line, under the cut of a review's replies; a second status in the same review only what changed; the open to-dos on
the batch's own threads, chats and senders whole in the claim's reply. Chats, the CLI and a to-do's run keep the status
they had. Made-up data only, on a store as a Machine keeps it."""
import json
from pathlib import Path
import tempfile
import unittest
import uuid

import machine.app.status as machine_app_status
import machine.main as machine_main
import machine.text as machine_text
from machine import todo_states
from machine.app import review_status

SESSION = 'agent:main:assistant-review-signals-' + 'a' * 32
CUT = 64000  # OpenClaw's tool-result cut
BODY = 'Robin waits for the revised quote with the oak option and the lower patio before their board meets next week. ' * 7  # ~700


def message(n, kind='gmail.message', **meta):
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': kind, 'title': f'Message {n}', 'occurred_at': '2026-11-20T10:00:00+00:00',
            'body': f'Message number {n}', 'metadata': meta, 'deleted': False}


class Store(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite', protect=True)  # sealed, as every Machine is by default
        self.app = object.__new__(machine_main.App)
        self.app.store, self.app.config = self.store, {'accounts': []}

    def events(self, *rows):
        self.store.commit_page('work', {}, list(rows))
        with self.store.connect() as db:
            return {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}

    def card(self, n, evidence, status='pending', title=None):
        sid = self.store.suggest(f'matter:{n}', (title or f'Send the revised quote, matter {n}')[:89], BODY[:699], [evidence])['id']
        if status != 'pending':
            with self.store.connect() as db:
                db.execute('UPDATE suggestions SET status=? WHERE id=?', (status, sid))
                db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                           (uuid.uuid4().hex, sid, 'complete', '', 'dashboard', '2026-11-21T10:00:00+00:00'))
        return sid

    def status(self, **args):
        return self.app.action('status', args)


class LightStatus(Store):
    def setUp(self):
        super().setUp()
        ids = self.events(message(1))
        self.open = [self.card(n, ids['m1'], title='x' * 89) for n in range(150)]
        self.done = [self.card(1000 + n, ids['m1'], 'completed') for n in range(100)]

    def test_a_review_gets_every_open_to_do_in_short_under_the_cut(self):
        light = self.status(_review_session=SESSION)
        self.assertEqual({c['id'] for c in light['suggestions']}, set(self.open))  # every open one, by id and title
        self.assertTrue(all('body' not in c and len(c.get('body_start', '')) <= review_status.BODY_START + 1 for c in light['suggestions']))
        self.assertTrue(all(isinstance(d, str) for d in light['done']))
        self.assertLessEqual(len(machine_text.encoded(light)), review_status.REVIEW_PAGE_CHARS)
        self.assertLess(len(machine_text.encoded(light)) * 1.3, CUT)  # read escaped once more inside the tool's reply
        if len(light['done']) < len(self.done):
            self.assertIn('left_out', light)  # what went is said

    def test_the_status_today_ran_past_the_cut_on_this_list(self):
        # why: with 150 open to-dos compact_status's 400 characters each no longer fit, and the end was cut unread
        today = self.status()
        self.assertGreater(len(machine_text.encoded(today)), CUT)

    def test_fit_keeps_every_open_to_do_and_says_what_went(self):
        compact = machine_app_status.compact_status(self.store.snapshot([], lean=True))
        tight = review_status.fit(review_status.light(compact), limit=20000)
        self.assertEqual({c['id'] for c in tight['suggestions']}, set(self.open))
        self.assertEqual(tight['done'], [])
        self.assertIn('body_start of', tight['left_out'])


class ReadOnce(Store):
    def setUp(self):
        super().setUp()
        ids = self.events(message(1))
        self.evidence = ids['m1']
        self.first = self.card(1, ids['m1'])
        self.card(2, ids['m1'], 'completed')

    def test_a_second_status_in_the_same_review_gives_only_what_changed(self):
        whole = self.status(_review_session=SESSION)
        self.assertEqual(len(whole['suggestions']), 1)
        again = self.status(_review_session=SESSION)
        self.assertEqual((again['suggestions'], again['done']), ([], []))
        self.assertIn('2 to-dos', again['already_read'])
        new = self.card(3, self.evidence)  # the review saved one
        self.assertEqual([c['id'] for c in self.status(_review_session=SESSION)['suggestions']], [new])
        later = self.events(message(2))['m2']
        self.store.suggest('matter:1', 'Send the revised quote, now with the lower patio', BODY[:699], [later], card_id=self.first, match=True)
        self.assertEqual([c['id'] for c in self.status(_review_session=SESSION)['suggestions']], [self.first])  # changed: shown again

    def test_again_reads_it_whole_and_another_review_reads_it_whole(self):
        self.status(_review_session=SESSION)
        self.assertEqual(len(self.status(_review_session=SESSION, again=True)['suggestions']), 1)
        self.assertEqual(len(self.status(_review_session=SESSION[:-1] + 'b')['suggestions']), 1)

    def test_chats_the_cli_and_a_to_dos_run_keep_todays_status(self):
        for args in ({}, {'_review_session': 'agent:main:assistant-review-preparation-' + 'a' * 32}, {'_review_session': 'agent:main:main'}):
            for _ in range(2):  # and read as often as asked
                got = self.status(**args)
                self.assertIn('body', got['suggestions'][0], args)
                self.assertNotIn('already_read', got)
        self.assertEqual(self.status(_review_session=SESSION, suggestion_id=self.first)['suggestion']['id'], self.first)  # one in full

    def test_the_plugin_passes_the_session_of_a_signal_review_only(self):
        plugin = (Path(__file__).resolve().parent.parent / 'openclaw-plugin' / 'index.ts').read_text()
        self.assertIn("if (params.action === 'status' && /^agent:main:assistant-review-signals-/.test(key)) args._review_session = key;", plugin)
        self.assertTrue(SESSION.startswith('agent:main:assistant-review-signals-'))


class OpenHere(Store):
    def test_the_open_to_dos_on_the_batchs_threads_chats_and_senders_come_whole(self):
        ids = self.events(message(1, thread_id='t1', **{'from': 'Robin <robin@acme.example>'}),
                          message(2, 'whatsapp.message', chat_id='c1@g.us'),
                          message(3, 'slack.message', channel_id='C1', conversation_type='channel'),
                          message(4, thread_id='t9', **{'from': 'Kim <kim@other.example>'}),
                          message(5, thread_id='t2', **{'from': 'Robin <robin@acme.example>'}),
                          message(6, 'whatsapp.message', chat_id='c1@g.us'),
                          message(7, 'slack.message', channel_id='C1', conversation_type='channel'),
                          message(8, thread_id='t1', **{'from': 'Sam <sam@acme.example>'}))
        mail, chat, channel, other = (self.card(n, ids[f'm{n}']) for n in (1, 2, 3, 4))
        self.card(9, ids['m1'], 'completed')  # done: not here
        with self.store.connect() as db:
            found = review_status.here(db, [ids['m5'], ids['m6'], ids['m7'], ids['m8']], todo_states.OPEN)
        by = {c['id']: c for c in found}
        self.assertEqual(set(by), {mail, chat})  # the same sender and thread; the same chat; a Slack channel is too wide
        self.assertEqual(by[mail]['shares_with_signals'], sorted([ids['m5'], ids['m8']]))
        self.assertLessEqual(len(by[chat]['body']), 401)  # its first 400 characters
        self.assertNotIn(other, by)
        self.assertNotIn(channel, by)

    def test_the_claim_carries_them_and_only_while_it_fits(self):
        ids = self.events(message(1, 'whatsapp.message', chat_id='c1@g.us'))
        mine = self.card(1, ids['m1'])
        self.events(message(2, 'whatsapp.message', chat_id='c1@g.us'))
        self.app.config = {'accounts': [{'id': 'work'}]}
        self.app.fleet = None
        claim = self.app.events_action('begin_analysis', {'account_ids': ['work'], 'limit': 120})
        self.assertEqual([c['id'] for c in claim['open_todos_here']], [mine])
        self.assertLessEqual(len(machine_text.encoded(claim)), CUT - 2000)

    def test_at_most_ten_and_within_their_room(self):
        ids = self.events(message(1, 'whatsapp.message', chat_id='c1@g.us'), message(2, 'whatsapp.message', chat_id='c1@g.us'))
        for n in range(30):
            self.card(n, ids['m1'])
        with self.store.connect() as db:
            found = review_status.here(db, [ids['m2']], todo_states.OPEN)
        self.assertLessEqual(len(found), review_status.HERE_MAX)
        self.assertLessEqual(len(json.dumps(found, ensure_ascii=False)), review_status.HERE_CHARS)
        with self.store.connect() as db:
            self.assertEqual(review_status.here(db, [], todo_states.OPEN), [])


if __name__ == '__main__':
    unittest.main()
