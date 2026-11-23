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
import machine.store.decisions as machine_store_decisions
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

    def test_a_run_that_only_answered_with_nothing_ready_reads_needs_you(self):
        answered = {'outcome': json.dumps({'state': 'answered'})}
        self.assertEqual(machine_cards.needs_owner({**self.row(''), **answered}), 'Answered. Nothing done yet.')
        self.assertEqual(machine_cards.needs_owner({**self.row('', [LINK]), **answered}), 'Answered. Nothing done yet.')
        # an answer beside a ready draft, file or skill stays Prepared
        self.assertEqual(machine_cards.needs_owner({**self.row('', [DRAFT]), **answered}), '')
        self.assertEqual(machine_cards.needs_owner({**self.row('', result_files=[{'path': 'memory/assistant/r.md'}]), **answered}), '')
        self.assertEqual(machine_cards.needs_owner({**self.row('', proposed_skill={'id': 's1'}), **answered}), '')

    def test_other_states_are_not_this(self):
        self.assertEqual(machine_cards.needs_owner(self.row('x', status='pending')), '')
        self.assertEqual(machine_cards.needs_owner(self.row('x', preparation_status='blocked')), '')
        self.assertEqual(machine_cards.needs_owner(self.row('x', handled_hint='{"reason":"replied"}')), '')
        self.assertEqual(machine_cards.needs_owner({**self.row(''), 'outcome': '{"state":"done"}'}), '')
        self.assertEqual(machine_cards.needs_owner({**self.row(''), 'outcome': 'not json'}), '')


class Lead(unittest.TestCase):
    """result_ask: what is left is for the owner to say (Answer leads), or a step they do themselves (Mark done leads).
    The phone's buttons (quick_kind), Telegram's (controls) and the note's question (waiting_questions) agree."""
    row = Rule.row

    def lead(self, row):
        row = {'event_ids': '[]', 'source_links': '[]', 'next_action': None, **row}
        first = machine_cards.controls(row)['blocks'][0]['buttons'][0]['label']
        return first, machine_delivery_push.quick_kind(row, 'result')

    def test_a_need_nothing_on_it_settles_leads_with_answer_question_or_not(self):
        for needs in ('the signed contract from you', 'confirm which policy covers the office', 'Which date should I offer?'):
            with self.subTest(needs):
                self.assertEqual(machine_cards.result_ask(self.row(needs)), needs)
                self.assertEqual(self.lead(self.row(needs)), ('Answer', 'question'))

    def test_a_step_they_do_themselves_leads_with_mark_done(self):
        own = self.row('pay it in your bank', outcome=json.dumps({'state': 'needs_you', 'needs': 'pay it in your bank', 'owner_step': True}))
        self.assertEqual(machine_cards.result_ask(own), '')
        self.assertEqual(self.lead(own), ('Mark done', 'ready'))
        self.assertEqual(self.lead(self.row('bring the keys', owner_step=1))[0], 'Mark done')
        self.assertEqual(machine_cards.result_ask(self.row('get the readings', handoff_still={'name': 'Ann Baker'})), '')
        # asked as a question, it still asks
        self.assertEqual(machine_cards.result_ask(self.row('Which shop?', owner_step=1)), 'Which shop?')

    def test_what_is_on_it_leads_instead(self):
        draft = {**DRAFT, 'revision': 'r1'}
        for row, kind in ((self.row('check the draft and send it', [draft]), 'draft'), (self.row('Tuesday or Wednesday?', [draft]), 'draft'),
                          (self.row('check the doc', [LINK]), 'ready'), (self.row('check the report', result_files=[{'path': 'memory/assistant/r.md'}]), 'ready')):
            with self.subTest(kind):
                row['next_action'] = {'kind': 'menu', 'actions': row['next_actions']}
                first, quick = self.lead(row)
                self.assertNotEqual(first, 'Answer')
                self.assertEqual(quick, kind)
        self.assertEqual(self.lead(self.row('confirm it', handled_hint='{"reason":"replied"}')), ('Mark done', 'ready'))


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

    def test_a_need_without_a_question_asks_everywhere_and_a_step_of_theirs_does_not(self):
        self.save(outcome='needs_you', needs='confirm which policy covers the office')
        view = self.row()
        self.assertEqual(machine_cards.controls(view)['blocks'][0]['buttons'][0]['label'], 'Answer')
        notice = machine_delivery_push.app_notice(self.store, {'accounts': [GMAIL]}, self.sid, 'result', 2)
        self.assertEqual((notice['actions'][0], notice['body']), ('answer', 'confirm which policy covers the office'))
        with self.store.connect() as db:
            asked = machine_store_decisions.waiting_questions(db, db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())
        self.assertEqual(asked, ['confirm which policy covers the office'])  # the chat's "Asked:" line before their note
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'The deposit is due.', 'outcome': 'needs_you',
                                      'needs': 'pay the deposit in your bank', 'owner_step': True})
        view = self.row()
        self.assertIs(json.loads(view['outcome'])['owner_step'], True)
        self.assertEqual(view['needs_owner'], 'pay the deposit in your bank')
        self.assertEqual(machine_cards.controls(view)['blocks'][0]['buttons'][0]['label'], 'Mark done')
        notice = machine_delivery_push.app_notice(self.store, {'accounts': [GMAIL]}, self.sid, 'result', 2)
        self.assertEqual(notice['actions'], ['open', 'done', 'snooze2h'])

    def test_a_run_that_only_answered_reads_needs_you_everywhere(self):
        self.save(outcome='answered')
        view = self.row()
        self.assertEqual(view['status'], 'prepared')
        self.assertEqual(view['needs_owner'], 'Answered. Nothing done yet.')  # the card's chip reads Needs you
        self.assertIn('Answered. Nothing done yet.', machine_cards.card(view))  # Telegram's card keeps its own line
        self.assertEqual(machine_cards.todo_state(view), 'needs you')
        self.assertEqual(self.lead(), ('Needs you', 'Needs you'))  # never "Ready:" for a task still to do
        self.assertNotIn('ready', self.digest()['text'].split('\n')[0])

    def test_a_ready_draft_stays_prepared_everywhere(self):
        self.save(next_actions=[DRAFT], outcome='needs_you', needs='check the draft and send it')
        view = self.row()
        self.assertNotIn('needs_owner', view)
        self.assertIn('Check the draft and send it.', machine_cards.card(view))  # Telegram's card: the need, plain
        self.assertNotIn('Needs you', machine_cards.card(view))
        self.assertEqual(machine_cards.todo_state(view), 'prepared')
        self.assertEqual(self.lead(), ('Ready', 'Ready'))
        self.assertIn('1 reply is ready to send', self.digest()['text'].split('\n')[0])


if __name__ == '__main__':
    unittest.main()
