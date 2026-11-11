"""Automated mail informs a to-do but never makes one on its own (2026-11-11). A test persona's train booking
confirmation, read with their own gym slot on the calendar, became a to-do to move the gym slot: every source behind it
was a booking, a receipt or a notification. A new to-do whose evidence is automated mail alone is told back once; the
review saves it only when that mail itself asks the owner to act (mail_asks). Judged from the headers, never from words
in the mail. Made-up data, no live calls."""
import tempfile
import unittest
from pathlib import Path

import test_ux as ux
from seams import patch_everywhere  # noqa: E402
a = ux.a

from machine.store import review_requeue, review_saves  # noqa: E402

MAIL = {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Example'}
CAL = {'id': 'work-cal', 'email': 'owner@example.com', 'service': 'calendar', 'transport': 'gog', 'boundary': 'work:Example'}
NOW = '2026-11-09T09:00:00+00:00'


def mail(source_id, sender, title, body, at='2026-11-09T08:00:00+00:00', labels=('INBOX',), **extra):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': title, 'body': body,
            'deleted': False, 'metadata': {'from': sender, 'to': 'owner@example.com', 'thread_id': 't-' + source_id,
                                           'labels': list(labels), 'message-id': f'<{source_id}@x>', **extra}}


def entry(source_id, title, start, attendees=()):
    return {'account_id': 'work-cal', 'source_id': source_id, 'kind': 'calendar.event', 'occurred_at': start, 'title': title, 'body': '',
            'deleted': False, 'metadata': {'start': {'dateTime': start}, 'end': {'dateTime': start}, 'status': 'confirmed',
                                           'attendees': [{'email': e, 'responseStatus': 'accepted'} for e in attendees],
                                           'organizer': {'email': 'owner@example.com', 'self': True}}}


class AutomatedMailAlone(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = tmp
        clock = patch_everywhere(a, 'now', return_value=NOW)
        clock.start()
        self.addCleanup(clock.stop)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [
            mail('booking', 'Rail Travel <bookings@rail.example>', 'Your train booking is confirmed', 'Outbound Tuesday 08:15, return 17:40.',
                 labels=('INBOX', 'CATEGORY_UPDATES'), list_unsubscribe=True),
            mail('receipt', 'Shop <orders@shop.example>', 'Your order', 'Thanks for your order.', precedence='bulk'),
            mail('invoice', 'Billing <billing@hosting.example>', 'Invoice 1042', 'Please pay by bank transfer before Nov 20.',
                 labels=('INBOX', 'CATEGORY_UPDATES')),
            mail('person', 'Robin Vale <robin@client.example>', 'Tuesday visit', 'Can you bring the floor plans on Tuesday?'),
            mail('sent', 'owner@example.com', 'Re: booking', 'Booked the train.', labels=('SENT',), precedence='bulk'),
        ])
        self.store.commit_page('work-cal', {}, [entry('gym', 'Gym', '2026-11-10T16:00:00+00:00'),
                                                entry('visit', 'Site visit', '2026-11-10T09:00:00+00:00', ['robin@client.example'])])

    def id(self, source_id):
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (source_id,)).fetchone()[0]

    def app(self):
        app = object.__new__(a.App)
        app.store = self.store
        app.config = {'accounts': [MAIL, CAL], 'digest_at': '08:30', 'review_worker': {'enabled': True}, 'prepare_ahead': False,
                      'openclaw_config': str(Path(self.tmp.name) / 'no-openclaw.json')}  # no model here: never a live turn
        return app

    def suggest(self, sources, **extra):
        return self.app().action('suggest', {'dedupe_key': 'k:' + '-'.join(sources), 'title': 'A to-do', 'body': 'Body.', 'when': 'now',
                                             'event_ids': [self.id(s) for s in sources], 'newer_checked': list(range(1, 50)), **extra})

    def cards(self):
        with self.store.connect() as db:
            return db.execute('SELECT count(*) FROM suggestions').fetchone()[0]

    def test_a_booking_and_the_owners_own_calendar_make_no_to_do(self):
        with self.assertRaisesRegex(ValueError, '^' + review_saves.AUTOMATED_GUIDANCE):
            self.suggest(['booking', 'gym'])
        with self.assertRaisesRegex(ValueError, 'mail_asks'):
            self.suggest(['receipt'])
        self.assertEqual(self.cards(), 0)

    def test_mail_that_asks_the_owner_to_act_saves_when_the_review_says_what_it_asks(self):
        self.assertTrue(self.suggest(['invoice'], mail_asks='Pay invoice 1042 by Nov 20')['id'])
        self.assertEqual(self.cards(), 1)

    def test_a_person_a_meeting_with_someone_or_the_owners_own_mail_is_never_held(self):
        self.assertTrue(self.suggest(['booking', 'person'])['id'])
        self.assertTrue(self.suggest(['booking', 'visit'])['id'])
        self.assertTrue(self.suggest(['sent'])['id'])
        self.assertTrue(self.suggest(['gym'])['id'])  # no mail at all: not this check's to judge

    def test_an_update_to_an_existing_to_do_is_not_held(self):
        card = self.suggest(['person'])['id']
        self.assertTrue(self.suggest(['booking'], card_id=card)['id'])

    def test_being_told_back_is_a_step_not_a_failed_save(self):
        with self.assertRaises(ValueError):
            self.suggest(['booking'])
        with self.store.connect() as db:
            review_saves.ensure(db)
            self.assertEqual(db.execute('SELECT count(*) FROM review_save_failures').fetchone()[0], 0)
        told = {'role': 'toolResult', 'isError': True, 'content': [{'type': 'text', 'text': a_message()}]}
        self.assertFalse(review_requeue.failed(told))

    def test_the_rule_is_in_the_review_prompt(self):
        self.assertIn('Automated mail alone makes a to-do only when it asks the owner to act (add mail_asks)', a.review_prompt('r1', ['work']))


def a_message():
    from machine.app.review_saves import AUTOMATED_ONLY
    return AUTOMATED_ONLY


if __name__ == '__main__':
    unittest.main()
