"""To-dos that only wait on someone else (2026-11-22): someone else's promise that came due goes straight to Waiting
on others, with no draft prepared ahead, so the day's room for preparing ahead stays for the owner's own work. Only
when nothing on the matter is the owner's: their own promise, one made together, a step only they can do, a refund to
chase, or an open to-do of theirs in the same conversation all keep it on the list. It comes back, and can be prepared
again, when a new message on it arrives, when its time to chase comes, or when the owner presses Nudge. Made-up
data; no model, nothing is sent."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

import test_ux as ux  # noqa: F401  (puts the app on the path)
from seams import patch_everywhere  # noqa: E402
import machine.cards as machine_cards
import machine.main as machine_main
from machine.store.cards import return_waiting
import timeutil

GMAIL = {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Example'}
SLACK = {'id': 'slack', 'service': 'slack', 'transport': 'maton', 'boundary': 'work:Example', 'user_id': 'UOWNER1'}
MONDAY = '2026-10-19T09:00:00+00:00'
DUE_DAY = '2026-10-21T07:00:00+00:00'  # the morning after their date (2026-10-20): the promise is checked


def email(source_id, at, sent=False, who='sam@client.example', thread='t1', title='Contract', body='I will send the signed contract by Tuesday.'):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': title, 'body': body, 'deleted': False,
            'metadata': {'from': 'owner@example.com' if sent else f'Sam Lee <{who}>', 'to': who if sent else 'owner@example.com',
                         'thread_id': thread, 'labels': ['SENT'] if sent else ['INBOX'], 'message-id': f'<{source_id}@x>'}}


def dm(source_id, at, owner=False, channel='D1', text='I will get you the invoice numbers by Tuesday.'):
    return {'account_id': 'slack', 'source_id': source_id, 'kind': 'slack.message', 'occurred_at': at, 'title': text, 'body': text, 'deleted': False,
            'metadata': {'channel_id': channel, 'user_id': 'UOWNER1' if owner else 'USAM1', 'ts': source_id}}


class WaitingAhead(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        zone = patch.object(timeutil, 'LOCAL_TZ', ZoneInfo('Europe/Brussels'))
        zone.start()
        self.addCleanup(zone.stop)
        self.clock = patch_everywhere(timeutil, 'now', return_value=MONDAY)
        self.clock.start()
        self.addCleanup(lambda: self.clock.stop())
        self.store = machine_main.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.owner_user_ids = {'UOWNER1'}
        self.commit(email('theirs', '2026-10-19T08:00:00+00:00'))

    def at(self, stamp):
        self.clock.stop()
        self.clock = patch_everywhere(timeutil, 'now', return_value=stamp)
        self.clock.start()

    def commit(self, *events, account='work'):
        self.store.commit_page(account, {}, list(events))

    def event(self, source_id):
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (source_id,)).fetchone()[0]

    def app(self):
        app = object.__new__(machine_main.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL, SLACK], 'digest_at': '08:30', 'review_worker': {'enabled': True}, 'prepare_ahead': True,
                      'openclaw_config': str(Path(self.tmp.name) / 'no-openclaw.json')}
        app.promise_check_model = lambda config, text: '[]'  # the check before a to-do: nothing kept
        return app

    def promise(self, direction='theirs', source='theirs', who='Sam Lee', what='send the signed contract', **args):
        return self.app().action('promise', {'direction': direction, 'event_id': self.event(source), 'who': who, 'what': what,
                                             'due': '2026-10-20', **args})['id']

    def due(self, app=None):
        self.at(DUE_DAY)
        (app or self.app()).promise_step()

    def card_of(self, pid):
        with self.store.connect() as db:
            sid = db.execute('SELECT suggestion_id FROM promises WHERE id=?', (pid,)).fetchone()[0]
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone()) if sid else None

    def ahead_used(self):
        with self.store.connect() as db:
            return db.execute("SELECT count(*) FROM decisions WHERE choice='prepare_ahead'").fetchone()[0]

    def assert_waits(self, card):
        self.assertEqual(machine_cards.todo_state(card), 'waiting on others')
        self.assertEqual((card['status'], card['early']), ('prepared', 0))
        with self.store.connect() as db:
            self.assertIsNone(db.execute("SELECT 1 FROM preparations WHERE suggestion_id=? AND status!='cancelled'", (card['id'],)).fetchone())
            self.assertEqual(db.execute('SELECT status FROM deliveries WHERE suggestion_id=?', (card['id'],)).fetchone()[0], 'cancelled')

    def assert_owners(self, card):
        self.assertNotIn(machine_cards.todo_state(card), ('waiting on others', 'looks done'))

    # Their promise alone: straight to Waiting on others, no slot used

    def test_their_promise_alone_waits_on_others_without_a_slot(self):
        pid = self.promise()
        self.due()
        card = self.card_of(pid)
        self.assert_waits(card)
        outcome = json.loads(card['outcome'])
        self.assertEqual(outcome['waiting_on'], 'Sam Lee')
        self.assertEqual(outcome['until'][:10], '2026-10-28')  # comes back to chase them after a week
        self.assertEqual(json.loads(card['chat_asks']), ['Write a short nudge'])
        self.assertEqual(self.ahead_used(), 0)
        self.assertEqual(card['title'], 'Waiting on Sam Lee: send the signed contract')

    def test_the_owners_own_promise_is_still_prepared_ahead(self):
        self.commit(email('yes', '2026-10-19T08:05:00+00:00', sent=True, title='Re: Contract', body='Sure, I will send the deck Tuesday.'))
        pid = self.promise(direction='mine', source='yes', what='send the deck')
        self.at('2026-10-20T07:00:00+00:00')  # the owner's own comes the morning before its date
        self.app().promise_step()
        card = self.card_of(pid)
        self.assertEqual((card['status'], card['early']), ('accepted', 1))
        self.assertEqual(self.ahead_used(), 1)

    # (a) Anything the owner owes keeps it on the list

    def test_a_plan_made_together_stays_with_the_owner(self):
        pid = self.promise(what='go over the contract together')
        with self.store.connect() as db:
            db.execute("UPDATE promises SET together=1,direction='mine' WHERE id=?", (pid,))
        self.due()
        self.assert_owners(self.card_of(pid))

    def test_a_step_only_the_owner_can_do_stays_with_the_owner(self):
        pid = self.promise(owner_step=True)
        with self.store.connect() as db:
            db.execute('UPDATE promises SET owner_step=1 WHERE id=?', (pid,))
        self.due()
        self.assert_owners(self.card_of(pid))

    def test_a_mixed_thread_stays_with_the_owner(self):
        """"I'll send the deck; can you confirm the date?" and their "I'll confirm by Tuesday": the owner still owes the
        deck, so their promise in the same thread doesn't hide the matter under Waiting on others."""
        self.commit(email('ask', '2026-10-19T07:00:00+00:00', sent=True, title='Contract', body="I'll send the deck Friday; can you confirm the date?"),
                    email('confirm', '2026-10-19T08:10:00+00:00', body='I will confirm the date by Tuesday.'))
        self.promise(direction='mine', source='ask', what='send the deck', due='2026-10-23')
        pid = self.promise(source='confirm', what='confirm the date')
        self.due()
        card = self.card_of(pid)
        self.assert_owners(card)

    def test_a_reply_the_owner_owes_in_the_thread_keeps_it_on_the_list(self):
        """Their message promised the contract and asked the owner something (which billing address): the review made a
        to-do for the reply the owner owes, so the promise joins that open to-do, which stays on the list. A later
        message of theirs in the thread closes the promise itself (answered): no to-do waits on it."""
        todo = self.store.suggest('work:address', 'Tell Sam the billing address', 'Sam asked for it.', [self.event('theirs')], 'now')['id']
        pid = self.promise()
        self.due()
        card = self.card_of(pid)
        self.assertEqual(card['id'], todo)
        self.assert_owners(card)
        self.at(MONDAY)
        later = self.promise(what='send the order form')
        self.commit(email('question', '2026-10-19T09:20:00+00:00', body='Also, which billing address should we use?'))
        self.due()
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status,suggestion_id FROM promises WHERE id=?', (later,)).fetchone()[:], ('answered', None))

    def test_a_payment_the_owner_owes_in_the_same_chat_keeps_it_on_the_list(self):
        """They promised the invoice numbers in a Slack DM where the owner promised a payment: the owner still owes
        something in that conversation, so it stays."""
        self.commit(dm('numbers', '2026-10-19T08:00:00+00:00'), dm('pay', '2026-10-19T08:30:00+00:00', owner=True, text='I will pay the deposit by Friday.'),
                    account='slack')
        self.promise(direction='mine', source='pay', what='pay the deposit', due='2026-10-23')
        pid = self.promise(source='numbers', what='get the invoice numbers')
        self.due()
        self.assert_owners(self.card_of(pid))

    def test_the_owners_promise_in_the_same_message_keeps_it_on_the_list(self):
        """One message holding both sides ("I'll send the deck, and you agreed to send the numbers"): stays with the owner."""
        self.commit(email('both', '2026-10-19T08:40:00+00:00', sent=True, thread='t5', body='As agreed: I will send the deck, you send the numbers by Tuesday.'))
        self.promise(direction='mine', source='both', what='send the deck', due='2026-10-23')
        pid = self.promise(source='both', what='send the numbers')
        self.due()
        self.assert_owners(self.card_of(pid))

    def test_what_the_owner_owes_the_same_person_elsewhere_is_its_own_to_do(self):
        """The owner promised Sam a payment in another conversation: that promise becomes its own to-do on its day, so
        this one, about Sam's contract, still waits on Sam."""
        self.commit(dm('pay', '2026-10-19T08:30:00+00:00', owner=True, text='I will pay the deposit by Friday.'), account='slack')
        mine = self.promise(direction='mine', source='pay', what='pay the deposit', due='2026-10-23')
        pid = self.promise()
        self.due()
        self.assert_waits(self.card_of(pid))
        self.at('2026-10-22T07:00:00+00:00')
        self.app().promise_step()
        self.assert_owners(self.card_of(mine))

    def test_a_deadline_or_decision_of_the_owners_in_the_same_chat_keeps_it_on_the_list(self):
        """Their promise in a chat where the owner has an open to-do with a deadline (decide on the offer by Friday)."""
        self.commit(dm('numbers', '2026-10-19T08:00:00+00:00'), dm('offer', '2026-10-19T08:01:00+00:00', text='Can you decide on the offer by Friday?'),
                    account='slack')
        self.store.suggest('slack:offer', 'Decide on the offer', 'Sam needs a decision by Friday.', [self.event('offer')], 'now', due='2026-10-23')
        pid = self.promise(source='numbers', who='Pat Doe', what='get the invoice numbers')
        self.due()
        self.assert_owners(self.card_of(pid))

    def test_an_owners_to_do_on_another_matter_doesnt_keep_it(self):
        """Something of the owner's in another conversation with someone else is another matter."""
        self.commit(email('other', '2026-10-19T08:30:00+00:00', who='kim@else.example', thread='t9', title='Invoice', body='Please pay the invoice.'))
        self.store.suggest('work:invoice', 'Pay the invoice', 'Kim asked.', [self.event('other')], 'now')
        pid = self.promise()
        self.due()
        self.assert_waits(self.card_of(pid))

    def test_an_owners_to_do_that_itself_waits_doesnt_keep_it(self):
        """An open to-do in the thread that is itself under Waiting on others holds nothing of the owner's."""
        self.commit(email('earlier', '2026-10-18T08:00:00+00:00', sent=True, body='Could you send the contract?'))
        todo = self.store.suggest('work:contract-ask', 'Get the contract from Sam', 'Asked Sam.', [self.event('earlier')], 'now')['id']
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',outcome=? WHERE id=?", (json.dumps({'state': 'waiting', 'waiting_on': 'Sam Lee'}), todo))
        pid = self.promise()
        self.due()
        self.assertEqual(self.card_of(pid)['id'], todo)  # it joined that one (promise_home), which keeps waiting
        self.assertEqual(machine_cards.todo_state(self.card_of(pid)), 'waiting on others')

    def test_a_refund_to_chase_stays_a_quiet_to_do(self):
        pid = self.promise()
        with self.store.connect() as db:
            db.execute('UPDATE promises SET refund=? WHERE id=?', (json.dumps({'amount': '42', 'currency': 'EUR', 'payer': 'Acme'}), pid))
            row = dict(db.execute('SELECT p.*,e.occurred_at made_at FROM promises p JOIN events e ON e.id=p.event_id WHERE p.id=?', (pid,)).fetchone())
        self.at(DUE_DAY)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            self.app().promise_card(row, _db=db, quiet=True)
        self.assert_owners(self.card_of(pid))

    # A direct Do it or Nudge still prepares it

    def test_nudge_before_its_day_prepares_it_at_once(self):
        pid = self.promise()
        app = self.app()
        app.action('promise_todo', {'id': pid}, owner_dashboard=True)
        card = self.card_of(pid)
        self.assertEqual(card['status'], 'accepted')
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT choice FROM decisions WHERE suggestion_id=? AND id LIKE 'promise-ask:%'", (card['id'],)).fetchone()[0], 'accept')

    def test_nudge_on_one_waiting_drafts_it_there(self):
        pid = self.promise()
        self.due()
        sid = self.card_of(pid)['id']
        saved = self.app().action('promise_todo', {'id': pid}, owner_dashboard=True)
        self.assertEqual(saved['card'], sid)
        card = self.card_of(pid)
        self.assertEqual(card['status'], 'accepted')  # its run drafts the nudge; it shows as being prepared
        self.assertNotEqual(machine_cards.todo_state(card), 'waiting on others')
        self.assertEqual(self.ahead_used(), 0)  # the owner's own ask, never a slot

    def test_do_it_on_one_waiting_still_works(self):
        pid = self.promise()
        self.due()
        sid = self.card_of(pid)['id']
        self.store.decide(sid, 'accept', '', 'doit-1', 'dashboard')
        card = self.card_of(pid)
        self.assertEqual(card['status'], 'accepted')
        with self.store.connect() as db:
            self.assertTrue(db.execute("SELECT 1 FROM preparations WHERE suggestion_id=? AND status='queued'", (sid,)).fetchone())

    def test_a_full_day_of_slots_is_not_touched(self):
        """With the day's room nearly used, the waiting one takes none, and the owner's own still gets the last one."""
        pid = self.promise()
        self.commit(email('other', '2026-10-19T08:30:00+00:00', who='kim@else.example', thread='t9', title='Invoice', body='Please pay the invoice.'))
        other = self.store.suggest('work:invoice', 'Pay the invoice', 'Kim asked.', [self.event('other')], 'now')['id']
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='completed' WHERE id=?", (other,))
            for i in range(9):
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)",
                           (f'ahead:{i}', other, 'prepare_ahead', '', 'assistant', DUE_DAY))
        self.due()
        self.assert_waits(self.card_of(pid))
        self.assertEqual(self.ahead_used(), 9)
        self.assertTrue(self.store.ahead_room(10, urgent=True))

    def test_the_review_leaving_a_to_do_waiting_takes_no_slot(self):
        """The review's own word that a to-do waits on someone else (waiting_on) never starts a draft, even when it
        also asked for one prepared ahead."""
        todo = self.store.suggest('work:contract', 'Send Sam the contract', 'Sam asked for it.', [self.event('theirs')], 'now')['id']
        self.commit(email('back', '2026-10-19T10:00:00+00:00', body='Thanks, I will check with legal and come back to you.'))
        self.app().action('suggest', {'dedupe_key': 'work:contract', 'card_id': todo, 'title': 'Send Sam the contract', 'body': 'Sam checks with legal.',
                                      'event_ids': [self.event('back')], 'waiting_on': 'Sam to come back after legal', 'prepare_ahead': True})
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (todo,)).fetchone())
        self.assertEqual(machine_cards.todo_state(row), 'waiting on others')
        self.assertEqual(self.ahead_used(), 0)

    # (c) Moving back

    def test_their_reply_brings_it_back_and_it_can_be_prepared_again(self):
        pid = self.promise()
        self.due()
        sid = self.card_of(pid)['id']
        self.at('2026-10-21T10:00:00+00:00')
        self.commit(email('reply', '2026-10-21T09:30:00+00:00', title='Re: Contract', body='Sorry for the delay. Which entity should the contract be for?'))
        saved = self.app().action('suggest', {'dedupe_key': 'work:contract-entity', 'card_id': sid, 'title': 'Tell Sam which entity the contract is for',
                                              'body': 'Sam asks which entity to use.', 'event_ids': [self.event('reply')], 'prepare_ahead': True})
        self.assertEqual(saved['id'], sid)
        card = self.card_of(pid)
        self.assert_owners(card)
        self.assertEqual((card['status'], card['early']), ('accepted', 1))  # prepared ahead again: the next step is the owner's
        self.assertEqual(self.ahead_used(), 1)

    def test_their_reply_without_a_draft_brings_it_back_to_the_list(self):
        pid = self.promise()
        self.due()
        sid = self.card_of(pid)['id']
        self.at('2026-10-21T10:00:00+00:00')
        self.commit(email('reply', '2026-10-21T09:30:00+00:00', title='Re: Contract', body='Can we move the start date first?'))
        self.app().action('suggest', {'dedupe_key': 'work:contract-start', 'card_id': sid, 'title': 'Answer Sam about the start date',
                                      'body': 'Sam asks to move the start date.', 'event_ids': [self.event('reply')]})
        card = self.card_of(pid)
        self.assertEqual(card['status'], 'pending')
        self.assertIsNone(card['outcome'])
        self.assert_owners(card)

    def test_the_time_to_chase_brings_it_back_with_a_nudge(self):
        pid = self.promise()
        self.due()
        sid = self.card_of(pid)['id']
        self.at('2026-10-28T08:00:00+00:00')
        with self.store.connect() as db:
            self.assertEqual(return_waiting(db), 1)
        card = self.card_of(pid)
        self.assertEqual((card['id'], card['status'], json.loads(card['outcome'])['state']), (sid, 'pending', 'still_waiting'))
        self.assertIn('Write a short nudge', json.loads(card['chat_asks']))
        self.assert_owners(card)

    def test_not_back_before_its_time(self):
        pid = self.promise()
        self.due()
        self.at('2026-10-25T08:00:00+00:00')
        with self.store.connect() as db:
            self.assertEqual(return_waiting(db), 0)
        self.assert_waits(self.card_of(pid))

    def test_the_result_coming_in_closes_it_by_itself(self):
        pid = self.promise()
        self.due()
        sid = self.card_of(pid)['id']
        self.commit(email('signed', '2026-10-21T09:30:00+00:00', title='Re: Contract', body='Signed contract attached.'))
        self.assertTrue(self.store.looks_handled(sid, 'Sam sent the signed contract', [self.event('signed')]).get('closed'))
        self.assertEqual(self.card_of(pid)['status'], 'completed')


if __name__ == '__main__':
    unittest.main()
