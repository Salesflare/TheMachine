"""Prepared or Needs you (a study of Do it, 2026-11): a to-do says Prepared only when its run left a draft or result to
approve. One whose run ended needing the owner (a decision, a fact only they have, a sign-in, a choice) with nothing
ready says Needs you, with the run's own needs as the reason: on the card (needs_owner in its view), in the chat's
state, in its notification and in the morning digest. No live calls."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

import test_ux as ux
import machine.cards as machine_cards
import machine.delivery.push as machine_delivery_push
import machine.main as machine_main
from test_honest_status import GMAIL, SLACK, email

DRAFT = {'kind': 'email', 'label': 'Send reply', 'account_id': 'work', 'to': ['customer@client.example'], 'subject': 'Re: Invoice',
         'body': 'Hi,\n\nThe invoice is fixed.\n\nCheers,\n\nAlex', 'in_reply_to': '<m1@x>'}
LINK = {'kind': 'open', 'label': 'Open the invoice', 'url': 'https://billing.example/inv/1'}


class Rule(unittest.TestCase):
    """needs_owner itself: from the run's outcome and what it left, never from the words."""

    def row(self, needs, actions=(), **more):
        return {'id': 'c1', 'status': 'prepared', 'body': 'Looked into it.', 'next_actions': list(actions),
                'outcome': json.dumps({'state': 'needs_you', 'needs': needs}), **more}

    def test_nothing_ready_reads_needs_you_with_its_reason(self):
        self.assertEqual(machine_cards.needs_owner(self.row('the signed contract from you')), 'the signed contract from you')
        self.assertEqual(machine_cards.needs_owner(self.row('Which date should I offer?')), 'Which date should I offer?')
        # a question with only a link beside it still asks first (ask_question's rule)
        self.assertEqual(machine_cards.needs_owner(self.row('Which plan do you want?', [LINK])), 'Which plan do you want?')

    def test_a_draft_step_file_or_skill_stays_prepared(self):
        self.assertEqual(machine_cards.needs_owner(self.row('check the draft and send it', [DRAFT])), '')
        self.assertEqual(machine_cards.needs_owner(self.row('Tuesday or Wednesday?', [DRAFT])), '')  # drafted for the likelier answer
        self.assertEqual(machine_cards.needs_owner(self.row('check the doc', [LINK])), '')  # a link to what it made
        self.assertEqual(machine_cards.needs_owner(self.row('check the report', result_files=[{'path': 'memory/assistant/r.md'}])), '')
        self.assertEqual(machine_cards.needs_owner(self.row('check the report', body='Done: [Report](memory/assistant/r.md)')), '')
        self.assertEqual(machine_cards.needs_owner(self.row('approve the skill', proposed_skill={'id': 's1'})), '')

    def test_other_states_are_not_this(self):
        self.assertEqual(machine_cards.needs_owner(self.row('x', status='pending')), '')
        self.assertEqual(machine_cards.needs_owner(self.row('x', preparation_status='blocked')), '')
        self.assertEqual(machine_cards.needs_owner(self.row('x', handled_hint='{"reason":"replied"}')), '')
        self.assertEqual(machine_cards.needs_owner({**self.row(''), 'outcome': '{"state":"done"}'}), '')
        self.assertEqual(machine_cards.needs_owner({**self.row(''), 'outcome': 'not json'}), '')


class Everywhere(unittest.TestCase):
    row = ux.UX.row
    decide = ux.UX.decide

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = machine_main.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [email('m1', '2026-10-15T08:00:00+00:00')])
        with self.store.connect() as db:
            self.event_id = db.execute('SELECT id FROM events').fetchone()[0]
        self.sid = self.store.suggest('invoice-question', 'Invoice question from Client', 'They ask about an invoice.', [self.event_id])['id']

    def app(self):
        app = object.__new__(machine_main.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL, SLACK]}
        return app

    def save(self, **args):
        self.decide('accept')
        return self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Looked into the invoice.', **args})

    def lead(self):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())
            return machine_delivery_push.result_lead(db, row), machine_delivery_push.result_lead(db, {**row, **self.store.suggestion_result(row, db)})

    def digest(self):
        app = object.__new__(machine_main.App)
        app.store, app.config = self.store, {'accounts': [GMAIL]}
        return app.digest(dt.datetime(2026, 10, 16, 7, 0, tzinfo=dt.timezone.utc))

    def test_a_run_that_needs_a_fact_reads_needs_you_everywhere(self):
        self.save(outcome='needs_you', needs='Which invoice number do they mean?')
        view = self.row()
        self.assertEqual(view['status'], 'prepared')
        self.assertEqual(view['needs_owner'], 'Which invoice number do they mean?')  # the card's chip and its reason
        self.assertIn('Needs you: Which invoice number do they mean?', machine_cards.card(view))  # Telegram's card
        self.assertEqual(machine_cards.todo_state(view), 'needs you')  # the chat's and Talk's state
        with self.store.connect() as db:
            light = dict(db.execute('SELECT id,status,outcome,body,next_action FROM suggestions WHERE id=?', (self.sid,)).fetchone())
            self.assertEqual(machine_cards.todo_state(light, db), 'needs you')
        self.assertEqual(self.lead(), ('Needs you', 'Needs you'))  # its notification: "Needs you: <title>", never "Ready:"
        headline = self.digest()['text'].split('\n')[0]
        self.assertNotIn('ready', headline)  # not counted as ready in the morning digest

    def test_a_ready_draft_stays_prepared_everywhere(self):
        self.save(next_actions=[DRAFT], outcome='needs_you', needs='check the draft and send it')
        view = self.row()
        self.assertNotIn('needs_owner', view)
        self.assertEqual(machine_cards.todo_state(view), 'prepared')
        self.assertEqual(self.lead(), ('Ready', 'Ready'))
        self.assertIn('1 reply is ready to send', self.digest()['text'].split('\n')[0])


if __name__ == '__main__':
    unittest.main()
