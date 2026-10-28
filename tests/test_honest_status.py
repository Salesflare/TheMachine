"""Learnings from Machines (2026-10-28): a to-do keeps prepared, sent, done and "still needs you" apart; before a
follow-up or handoff it looks at what is already synced in its own conversations; a prepared result links to what it
made; and a step stopped by a code or a missing permission says exactly what is needed. No live calls."""
import tempfile
import unittest
from pathlib import Path

import next_actions as n
import test_ux as ux
a = ux.a

GMAIL = {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Example'}
SLACK = {'id': 'slack', 'service': 'slack', 'transport': 'maton', 'boundary': 'work:Example', 'user_id': 'UOWNER1'}


def email(source_id, at, sender='customer@client.example', thread='t1', labels=('INBOX',)):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': 'Invoice question',
            'body': 'Can someone check our invoice?', 'deleted': False,
            'metadata': {'from': sender, 'thread_id': thread, 'labels': list(labels), 'message-id': f'<{source_id}@x>'}}


class HonestStatus(unittest.TestCase):
    row = ux.UX.row
    decide = ux.UX.decide

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.owner_user_ids = {'UOWNER1'}
        self.store.commit_page('work', {}, [email('m1', '2026-10-15T08:00:00+00:00')])
        with self.store.connect() as db:
            self.event_id = db.execute('SELECT id FROM events').fetchone()[0]
        self.sid = self.store.suggest('invoice-question', 'Invoice question from Client', 'They ask about an invoice.', [self.event_id])['id']

    def app(self):
        app = object.__new__(a.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL, SLACK]}
        return app

    DRAFT = {'kind': 'email', 'label': 'Send reply', 'account_id': 'work', 'to': ['customer@client.example'], 'subject': 'Re: Invoice',
             'body': 'Hi,\n\nThe invoice is fixed.\n\nCheers,\n\nAlex'}

    def save(self, **args):
        return self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Reply drafted.', **args})

    def test_done_is_refused_while_a_draft_still_waits(self):
        self.decide('accept')
        with self.assertRaisesRegex(ValueError, 'Not done yet'):
            self.save(next_actions=[self.DRAFT], outcome='done')
        self.assertNotEqual(self.row()['status'], 'prepared')
        self.save(next_actions=[self.DRAFT], outcome='needs_you', needs='check the draft and send it')
        self.assertIn('Needs you: check the draft and send it.', a.card(self.row()))
        # Nothing waiting: done is done.
        self.decide('accept')
        self.save(body='Looked it up: paid on Monday.', outcome='done')
        self.assertIn('Finished. Mark it done if it looks right.', a.card(self.row()))

    def test_an_older_done_with_a_waiting_draft_reads_as_ready_not_finished(self):
        self.decide('accept')
        self.save(next_actions=[self.DRAFT], outcome='needs_you', needs='check the draft and send it')
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET outcome='{\"state\":\"done\"}' WHERE id=?", (self.sid,))
        text = a.card(self.row())
        self.assertIn('Ready to approve. Nothing goes out until you do.', text)
        self.assertNotIn('Finished', text)

    def test_newer_messages_in_the_thread_are_listed_without_text(self):
        self.store.commit_page('work', {}, [
            email('m2', '2026-10-16T09:00:00+00:00', sender='Dana <dana@example.com>'),
            email('m3', '2026-10-16T10:00:00+00:00', sender='owner@example.com', labels=('SENT',)),
            email('m4', '2026-10-16T11:00:00+00:00', sender='other@client.example', thread='t2'),
            email('m0', '2026-10-14T11:00:00+00:00', sender='old@client.example')])
        with self.store.connect() as db:
            found = a.newer_activity(db, [self.event_id], {'UOWNER1'}, {'dana@example.com': 'Dana'}, ['example.com'])
        self.assertEqual([x['who'] for x in found], ['Dana (a teammate)', 'the owner'])  # not the other thread, not older ones
        lines = a.newer_activity_lines(found)
        self.assertIn("outcome:'already_done'", lines)
        self.assertNotIn('Can someone check', lines)  # who and when only
        with self.store.connect() as db:
            self.assertEqual(a.newer_activity(db, [], {'UOWNER1'}), [])
            only_domain = a.newer_activity(db, [self.event_id], set(), {}, ['example.com'])
        self.assertEqual(only_domain[0]['who'], 'dana@example.com (same company)')
        self.assertEqual(a.newer_activity_lines([]), '')

    def test_the_job_message_asks_for_these(self):
        self.decide('accept')
        with self.store.connect() as db:
            job = dict(db.execute('SELECT * FROM preparations WHERE suggestion_id=?', (self.sid,)).fetchone())
        prompt = a.preparation_prompt(job)
        self.assertIn('Keep prepared, sent and done apart', prompt)
        self.assertIn('Before a follow-up, nudge or handoff, check the conversation for newer activity', prompt)
        self.assertIn("{kind:open,label:'Open <what it is>'", prompt)
        self.assertIn('login code, a two-step code or a missing permission', prompt)
        self.assertEqual(n.validate({'kind': 'open', 'label': 'Open the proposal doc', 'url': 'https://docs.google.com/document/d/x'}, {'accounts': []}, [])['kind'], 'open')


if __name__ == '__main__':
    unittest.main()
