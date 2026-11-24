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
import machine.app.preparation as machine_app_preparation
import machine.cards as machine_cards
import machine.delivery.push as machine_delivery_push
import machine.main as machine_main
import notify
import machine.store.decisions as machine_store_decisions
from test_honest_status import GMAIL, SLACK, email

DRAFT = {'kind': 'email', 'label': 'Send reply', 'account_id': 'work', 'to': ['customer@client.example'], 'subject': 'Re: Invoice',
         'body': 'Hi,\n\nThe invoice is fixed.\n\nCheers,\n\nAlex', 'in_reply_to': '<m1@x>'}
HOLDING = {**DRAFT, 'label': 'Send reply', 'body': 'Hi,\n\nThanks, I’ll get back to you with the quote.\n\nAlex', 'still_owed': {'what': 'send the quote', 'due': '2026-10-20'}}
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

    def test_work_that_cant_be_used_before_the_answer_reads_needs_you(self):
        files = [{'path': 'memory/assistant/p.md'}]
        first = {'outcome': json.dumps({'state': 'needs_you', 'needs': 'What price and scope?', 'needs_first': True})}
        for made in ({'result_files': files}, {'next_actions': [DRAFT]}, {'proposed_skill': {'id': 's1'}}, {'body': '[Proposal](memory/assistant/p.md)'}, {}):
            with self.subTest(made):
                self.assertEqual(machine_cards.needs_owner({**self.row(''), **first, **made}), 'What price and scope?')
        # written as a statement too: blanks in a draft are still blanks
        blanks = {'outcome': json.dumps({'state': 'needs_you', 'needs': 'fill in the two dates', 'needs_first': True})}
        self.assertEqual(machine_cards.needs_owner({**self.row('', [DRAFT]), **blanks}), 'fill in the two dates')
        # a question next to only a file, where the run didn't say (a run from before): it asks, as its Answer already did
        self.assertEqual(machine_cards.needs_owner(self.row('What price and scope?', result_files=files)), 'What price and scope?')
        self.assertEqual(machine_cards.needs_owner(self.row('What price and scope?', result_files=files, proposed_skill={'id': 's1'})), '')

    def test_work_that_can_go_as_it_is_stays_prepared(self):
        can = {'outcome': json.dumps({'state': 'needs_you', 'needs': 'Tuesday or Wednesday?', 'needs_first': False})}
        for made in ({'next_actions': [DRAFT]}, {'result_files': [{'path': 'memory/assistant/p.md'}]}):
            with self.subTest(made):
                row = {**self.row(''), **can, **made}
                self.assertEqual(machine_cards.needs_owner(row), '')
                self.assertEqual(machine_cards.result_ask(row), '')
                self.assertEqual(machine_cards.ready_as_is(row), 'Tuesday or Wednesday?')
        # with nothing made it is a question after all
        self.assertEqual(machine_cards.needs_owner({**self.row(''), **can}), 'Tuesday or Wednesday?')
        self.assertEqual(machine_cards.result_ask({**self.row(''), **can}), 'Tuesday or Wednesday?')
        # only its own true or false counts
        odd = {'outcome': json.dumps({'state': 'needs_you', 'needs': 'Tuesday or Wednesday?', 'needs_first': 'yes'})}
        self.assertEqual(machine_cards.needs_owner({**self.row('', [DRAFT]), **odd}), '')

    def test_a_run_that_only_answered_with_nothing_ready_reads_needs_you(self):
        answered = {'outcome': json.dumps({'state': 'answered'})}
        self.assertEqual(machine_cards.needs_owner({**self.row(''), **answered}), 'Answered. Nothing done yet.')
        self.assertEqual(machine_cards.needs_owner({**self.row('', [LINK]), **answered}), 'Answered. Nothing done yet.')
        # an answer beside a ready draft, file or skill stays Prepared
        self.assertEqual(machine_cards.needs_owner({**self.row('', [DRAFT]), **answered}), '')
        self.assertEqual(machine_cards.needs_owner({**self.row('', result_files=[{'path': 'memory/assistant/r.md'}]), **answered}), '')
        self.assertEqual(machine_cards.needs_owner({**self.row('', proposed_skill={'id': 's1'}), **answered}), '')

    def test_only_a_holding_reply_ready_reads_needs_you_with_the_work_still_to_do(self):
        held = 'Holding reply ready. Still to do: send the quote.'
        for outcome in ({'state': 'needs_you', 'needs': 'check the reply and send it'}, {'state': 'done'}, {'state': 'answered'}, None):
            with self.subTest(outcome):
                row = {**self.row(''), 'outcome': json.dumps(outcome) if outcome else None}
                self.assertEqual(machine_cards.needs_owner({**row, 'next_actions': [HOLDING, LINK]}), held)
                self.assertEqual(machine_cards.result_ask({**row, 'next_actions': [HOLDING]}), '')  # Send leads, not Answer
                # the same words without still_owed are a reply that does the work: judged by its own mark, never the text
                self.assertEqual(machine_cards.needs_owner({**row, 'next_actions': [{k: v for k, v in HOLDING.items() if k != 'still_owed'}]}), '')
        # its question for the work goes after it; one the draft can't go without keeps leading
        self.assertEqual(machine_cards.needs_owner(self.row('Which price per tray?', [HOLDING])), held + ' Which price per tray?')
        first = {'outcome': json.dumps({'state': 'needs_you', 'needs': 'Which day can you promise?', 'needs_first': True})}
        self.assertEqual(machine_cards.needs_owner({**self.row('', [HOLDING]), **first}), 'Which day can you promise?')

    def test_a_holding_reply_beside_real_work_or_on_its_way_is_not_that(self):
        send = 'check the reply and send it'
        for more in ({'next_actions': [HOLDING, DRAFT]}, {'next_actions': [HOLDING], 'result_files': [{'path': 'memory/assistant/q.md'}]},
                     {'next_actions': [HOLDING], 'proposed_skill': {'id': 's1'}}, {'next_actions': [{**HOLDING, 'state': {'status': 'queued'}}]}):
            with self.subTest(more):
                self.assertEqual(machine_cards.needs_owner({**self.row(send), **more}), '')

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

    def test_a_draft_that_waits_on_the_answer_reads_needs_you_everywhere(self):
        self.save(next_actions=[DRAFT], outcome='needs_you', needs='What price and scope do I quote?', needs_first=True)
        view = self.row()
        self.assertEqual(view['needs_owner'], 'What price and scope do I quote?')
        self.assertIn('Needs you: What price and scope do I quote?', machine_cards.card(view))
        self.assertEqual(machine_cards.todo_state(view), 'needs you')
        self.assertEqual(self.lead(), ('Needs you', 'Needs you'))
        labels = [b['label'] for b in sum((x['buttons'] for x in machine_cards.controls(view)['blocks']), [])]
        self.assertEqual(labels[0], 'Answer')
        self.assertIn('Send reply', labels)  # the draft stays a tap away
        self.assertEqual(labels.count('Answer'), 1)
        notice = machine_delivery_push.app_notice(self.store, {'accounts': [GMAIL]}, self.sid, 'result', 2)
        self.assertEqual((notice['actions'][0], notice['body']), ('answer', 'What price and scope do I quote?'))
        with self.store.connect() as db:
            asked = machine_store_decisions.waiting_questions(db, db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())
        self.assertEqual(asked, ['What price and scope do I quote?'])
        self.assertTrue(notify.asks(view['outcome']))
        self.assertNotIn('ready', self.digest()['text'].split('\n')[0])
        # they put the price in themselves: it can go, so it is Prepared again with Send in front
        self.store.revise_draft(self.sid, view['next_actions'][0]['revision'], 'dashboard', body='Hi,\n\nIt is 900 euros.\n\nCheers,\n\nAlex')
        view = self.row()
        self.assertNotIn('needs_owner', view)
        self.assertEqual(machine_cards.todo_state(view), 'prepared')
        self.assertEqual(machine_cards.controls(view)['blocks'][0]['buttons'][0]['label'], 'Send reply')

    def test_a_draft_that_can_go_as_it_is_says_so_before_its_question(self):
        self.save(next_actions=[DRAFT], outcome='needs_you', needs='Which budget range fits?', needs_first=False)
        view = self.row()
        self.assertNotIn('needs_owner', view)
        self.assertIn('The draft is ready. One question: Which budget range fits?', machine_cards.card(view))
        self.assertEqual(self.lead(), ('Ready', 'Ready'))
        self.assertEqual(machine_cards.controls(view)['blocks'][0]['buttons'][0]['label'], 'Send reply')
        notice = machine_delivery_push.app_notice(self.store, {'accounts': [GMAIL]}, self.sid, 'result', 2)
        self.assertIn('The invoice is fixed', notice['body'])  # what is ready, not the question
        self.assertFalse(notify.asks(view['outcome']))  # one to clear at a tap
        self.assertIn('1 reply is ready to send', self.digest()['text'].split('\n')[0])

    def test_a_holding_reply_reads_needs_you_everywhere_and_send_still_leads(self):
        self.save(next_actions=[HOLDING], outcome='needs_you', needs='check the reply and send it')
        view = self.row()
        held = 'Holding reply ready. Still to do: send the quote.'
        self.assertEqual(view['needs_owner'], held)
        self.assertIn(held, machine_cards.card(view))
        self.assertNotIn('Check the reply', machine_cards.card(view))
        self.assertEqual(machine_cards.todo_state(view), 'needs you')
        self.assertEqual(self.lead(), ('Needs you', 'Needs you'))
        self.assertEqual(machine_cards.controls(view)['blocks'][0]['buttons'][0]['label'], 'Send reply')
        notice = machine_delivery_push.app_notice(self.store, {'accounts': [GMAIL]}, self.sid, 'result', 2)
        self.assertEqual((notice['actions'][0], notice['title']), ('draft', 'Needs you: Invoice question from Client'))
        self.assertNotIn('ready', self.digest()['text'].split('\n')[0])

    def test_one_prepared_ahead_says_so_too(self):
        self.save(next_actions=[HOLDING], outcome='needs_you', needs='check the reply and send it')
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET early=1,outcome=NULL')
        self.assertIn('Holding reply ready. Still to do: send the quote.', machine_cards.card(self.row()))

    def test_their_ok_is_never_an_answer_first(self):
        # "Approve the send" is a need too: only something missing from what the run made waits on an answer
        prompt = machine_app_preparation.preparation_prompt({'job_id': 'j', 'suggestion_id': 's'})
        self.assertIn('needs_first:true only when something is missing from it', prompt)
        self.assertIn('their OK to send, check or sign is never that', prompt)
        with self.assertRaisesRegex(ValueError, 'never for their OK to send, check or sign'):
            self.save(outcome='needs_you')

    def test_a_step_of_theirs_is_never_also_an_answer_first(self):
        self.save(next_actions=[DRAFT], outcome='needs_you', needs='pay the deposit in your bank', owner_step=True, needs_first=True)
        self.assertNotIn('needs_first', json.loads(self.row()['outcome']))

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
