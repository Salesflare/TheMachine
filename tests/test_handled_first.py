"""Fewer to-dos that are done already by the time the owner sees them (2026-11-05): before a new to-do, what came
after its evidence is read first (also with the same people on other conversations); a promise that came due is
checked against what happened since before it becomes a to-do; and a "Waiting on" to-do whose run only drafted a
nudge waits under Waiting on others. Made-up data, no live calls."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test_ux as ux
from seams import patch_everywhere  # noqa: E402
a = ux.a

GMAIL = {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Example'}
SLACK = {'id': 'slack', 'service': 'slack', 'transport': 'maton', 'boundary': 'work:Example', 'user_id': 'UOWNER1'}
MONDAY = '2026-10-19T09:00:00+00:00'


def email(source_id, at, sent=False, who='sam@client.example', thread='t1', title='Contract', body='Could you send the contract?'):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': title, 'body': body, 'deleted': False,
            'metadata': {'from': 'owner@example.com' if sent else f'Sam Lee <{who}>', 'to': who if sent else 'owner@example.com',
                         'thread_id': thread, 'labels': ['SENT'] if sent else ['INBOX'], 'message-id': f'<{source_id}@x>'}}


class HandledFirst(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = patch_everywhere(a, 'now', return_value=MONDAY)
        self.clock.start()
        self.addCleanup(lambda: self.clock.stop())
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.owner_user_ids = {'UOWNER1'}
        self.commit(email('ask', '2026-10-19T08:00:00+00:00'))
        self.ask = self.event('ask')

    def at(self, stamp):
        self.clock.stop()
        self.clock = patch_everywhere(a, 'now', return_value=stamp)
        self.clock.start()

    def commit(self, *events):
        self.store.commit_page('work', {}, list(events))
        with self.store.connect() as db:
            a.graph.build(db, {'accounts': [GMAIL, SLACK]}, a.now())

    def event(self, source_id):
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (source_id,)).fetchone()[0]

    def app(self):
        app = object.__new__(a.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL, SLACK], 'digest_at': '08:30', 'review_worker': {'enabled': True}, 'prepare_ahead': False,
                      'openclaw_config': str(Path(self.tmp.name) / 'no-openclaw.json')}  # no model here: never a live turn
        return app

    def cards(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM suggestions ORDER BY created_at')]

    # what came after: in the conversation, and with the same person elsewhere

    def test_what_came_after_includes_the_same_person_in_another_conversation(self):
        self.commit(email('elsewhere', '2026-10-19T08:20:00+00:00', sent=True, thread='t2', title='Contract attached'),
                    email('stranger', '2026-10-19T08:25:00+00:00', who='pat@other.example', thread='t3'),
                    email('older', '2026-10-18T08:00:00+00:00', sent=True, thread='t4'))
        with self.store.connect() as db:
            found = a.activity_since(db, [self.ask], {'UOWNER1'})
        self.assertEqual([(x['id'], x['who'], x['where']) for x in found], [(self.event('elsewhere'), 'the owner', 'elsewhere')])
        self.assertIn('on another channel', a.activity_lines(found))
        self.assertNotIn('Contract attached', a.activity_lines(found))  # who and when only

    # a new to-do from a review

    def suggest(self, **extra):
        return self.app().action('suggest', {'dedupe_key': 'work:contract', 'title': 'Send Sam the contract', 'body': 'Sam asks for it.',
                                             'event_ids': [self.ask], 'when': 'now', **extra})

    def test_a_new_to_do_with_nothing_after_its_evidence_saves_at_once(self):
        self.assertTrue(self.suggest()['id'])

    def test_a_new_to_do_reads_what_came_after_its_evidence_first(self):
        self.commit(email('reply', '2026-10-19T08:30:00+00:00', sent=True, title='Re: Contract', body='Attached.'))
        reply = self.event('reply')
        with self.assertRaisesRegex(ValueError, rf'event {reply}: gmail, .* from the owner'):
            self.suggest()
        self.assertEqual(self.cards(), [])
        # The review read it and something is still open: it says so and the to-do saves
        self.assertTrue(self.suggest(newer_checked=[reply])['id'])
        self.assertEqual(len(self.cards()), 1)

    def test_an_update_to_an_existing_to_do_is_not_held(self):
        card = self.suggest()['id']
        self.commit(email('later', '2026-10-19T08:40:00+00:00', title='Re: Contract', body='Any news?'))
        self.app().action('suggest', {'dedupe_key': 'work:contract-2', 'title': 'Sam asks again', 'body': 'Again.', 'event_ids': [self.event('later')],
                                      'when': 'now', 'card_id': card})
        self.assertEqual(len(self.cards()), 1)

    # a promise that came due

    def promise(self, direction='theirs', **args):
        if direction == 'mine':  # the owner's own promise is in their reply
            self.commit(email('yes', '2026-10-19T08:05:00+00:00', sent=True, title='Re: Contract', body='Sure, I will send it.'))
        return self.app().action('promise', {'direction': direction, 'event_id': self.event('yes') if direction == 'mine' else self.ask, 'who': 'Sam Lee', 'what': 'send the signed contract',
                                             'due': '2026-10-21', **args})['id']

    def promise_row(self, pid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM promises WHERE id=?', (pid,)).fetchone())

    def run_step(self, app):
        app.promise_step()
        thread = getattr(app, '_promise_check_thread', None)
        if thread:
            thread.join(10)

    def test_a_due_promise_with_nothing_since_becomes_a_to_do_without_a_check(self):
        pid = self.promise()
        app = self.app()
        app.promise_check_model = lambda config, text: self.fail('no check without anything new')
        self.at('2026-10-22T07:00:00+00:00')
        self.run_step(app)
        self.assertEqual(self.promise_row(pid)['status'], 'carded')

    def test_a_due_promise_kept_since_closes_without_a_to_do(self):
        pid = self.promise(direction='mine')
        self.commit(email('sent', '2026-10-20T10:00:00+00:00', sent=True, thread='t2', title='Signed contract', body='Here is the signed contract.'))
        sent = self.event('sent')
        prompts = []
        app = self.app()
        app.promise_check_model = lambda config, text: (prompts.append(text), json.dumps(
            [{'promise': pid, 'state': 'kept', 'event_id': sent, 'reason': 'Sent Sam the signed contract on Oct 20'}]))[1]
        self.at('2026-10-22T07:00:00+00:00')
        self.run_step(app)
        self.assertIn('<<<Signed contract — Here is the signed contract.>>>', prompts[0])  # message text as data
        row = self.promise_row(pid)
        self.assertEqual((row['status'], row['note']), ('kept', 'Sent Sam the signed contract on Oct 20'))
        self.run_step(app)
        self.assertEqual(self.cards(), [])
        page = self.store.promise_page(pid)
        self.assertNotIn('checked', [h['kind'] for h in page['history']])

    def test_a_due_promise_still_open_after_the_check_becomes_a_to_do(self):
        pid = self.promise()
        self.commit(email('nudge', '2026-10-20T10:00:00+00:00', sent=True, title='Re: Contract', body='Any news on the contract?'))
        app = self.app()
        calls = []
        app.promise_check_model = lambda config, text: (calls.append(1), json.dumps([{'promise': pid, 'state': 'open'}]))[1]
        self.at('2026-10-22T07:00:00+00:00')
        self.run_step(app)
        self.assertEqual(self.promise_row(pid)['status'], 'carded')
        self.assertEqual(len(calls), 1)

    def test_a_check_in_the_background_holds_the_to_do_one_pass(self):
        pid = self.promise()
        self.commit(email('nudge', '2026-10-20T10:00:00+00:00', sent=True, title='Re: Contract', body='Any news on the contract?'))
        app = self.app()
        app.background_pause = lambda **kw: None
        ran = []
        app.promise_check_run = lambda pages: ran.append([p['id'] for p, _ in pages])
        self.at('2026-10-22T07:00:00+00:00')
        with patch_everywhere(a, 'openclaw_model', return_value='openai/gpt-test'), patch.object(a.threading, 'Thread') as thread:
            thread.return_value.is_alive.return_value = False
            self.assertEqual(app.promise_checks(self.due()), {pid})
            thread.assert_called_once()
            # no room in the usage budget: no turn, the to-do comes as before
            app.background_pause = lambda **kw: {'window': '5h', 'until': 0}
            app._promise_check_thread = None
            self.assertEqual(app.promise_checks(self.due()), set())
        # no model known (a fresh install): the to-do comes as before
        with patch_everywhere(a, 'openclaw_model', return_value=None):
            self.assertEqual(app.promise_checks(self.due()), set())

    def due(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute("SELECT p.*,e.occurred_at made_at FROM promises p JOIN events e ON e.id=p.event_id WHERE p.status='open'")]

    def test_kept_needs_a_listed_message_and_a_reason(self):
        pid = self.promise()
        self.commit(email('reply', '2026-10-20T10:00:00+00:00', sent=True, title='Re: Contract', body='Thanks!'))
        app = self.app()
        app.promise_check_model = lambda config, text: json.dumps([{'promise': pid, 'state': 'kept', 'event_id': 999999, 'reason': 'Done'}])
        self.at('2026-10-22T07:00:00+00:00')
        self.run_step(app)
        self.assertEqual(self.promise_row(pid)['status'], 'carded')

    def test_a_model_that_cannot_answer_leaves_the_to_do_as_before(self):
        pid = self.promise()
        self.commit(email('reply', '2026-10-20T10:00:00+00:00', sent=True, title='Re: Contract', body='Thanks!'))
        app = self.app()
        import help_chat
        app.promise_check_model = lambda config, text: (_ for _ in ()).throw(help_chat.Unavailable('no model'))
        self.at('2026-10-22T07:00:00+00:00')
        self.run_step(app)
        self.assertEqual(self.promise_row(pid)['status'], 'carded')

    # Waiting on them: a nudge ready, under Waiting on others

    def prepared(self, direction='theirs', asked=False):
        pid = self.promise(direction=direction)
        self.at('2026-10-22T07:00:00+00:00')
        app = self.app()
        app.config['prepare_ahead'] = True
        self.run_step(app)
        sid = self.promise_row(pid)['suggestion_id']
        if asked:
            self.store.decide(sid, 'other', 'Nudge Sam about it', 'd-1', 'dashboard')
        with self.store.connect() as db:
            job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (sid,)).fetchone()[0]
            db.execute("UPDATE preparations SET status='running' WHERE suggestion_id=?", (sid,))  # its run took it
        nudge = {'kind': 'email', 'label': 'Send nudge', 'account_id': 'work', 'to': ['sam@client.example'], 'subject': 'Re: Contract',
                 'body': 'Hi Sam,\n\nHow is the contract coming along?\n\nAlex', 'in_reply_to': '<ask@x>'}
        self.app().action('prepare', {'suggestion_id': sid, 'job_id': job, 'body': 'A short nudge is ready.', 'next_actions': [nudge],
                                      'outcome': 'needs_you', 'needs': 'check the nudge and send it', **({'note_kind': 'continue'} if asked else {})})
        return next(c for c in self.cards() if c['id'] == sid)

    def test_waiting_on_them_with_only_a_nudge_waits_on_others(self):
        card = self.prepared()
        self.assertEqual(json.loads(card['outcome']), {'state': 'waiting', 'waiting_on': 'Sam Lee'})
        self.assertEqual(a.todo_state(card), 'waiting on others')
        self.assertTrue(card['next_action'])  # the nudge is still there to send

    def test_a_nudge_the_owner_asked_for_stays_ready(self):
        card = self.prepared(asked=True)
        self.assertEqual(json.loads(card['outcome'])['state'], 'needs_you')

    def test_the_owners_own_promise_stays_ready(self):
        card = self.prepared(direction='mine')
        self.assertEqual(json.loads(card['outcome'])['state'], 'needs_you')


if __name__ == '__main__':
    unittest.main()
