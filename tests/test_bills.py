"""Bills (2026-11-12): a bill the owner still has to pay by hand becomes a to-do with what it takes to pay it, from any
country; one paid automatically, or shown paid later, makes none; and an open bill to-do closes by itself, with Undo,
once a newer message shows it paid. The review judges what a mail means (the prompt); the code keeps what it read
(bill on suggest), closes on its word (looks_handled paid:true) and matches the same bill on a Family member's
Machine also without an IBAN (family_done.bill_key). Made-up US, UK and EU bills, no live calls."""
import json
import tempfile
import unittest
from pathlib import Path

import test_ux as ux
from seams import patch_everywhere  # noqa: E402
a = ux.a

import family_done  # noqa: E402

ROOT = Path(__file__).parent.parent
MAIL = {'id': 'home', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'personal'}
NOW = '2026-11-09T09:00:00+00:00'
LATER = '2026-11-10T09:00:00+00:00'

US_BILL = ('Your water bill INV-2026-0042 is ready. Amount due: $1,250.00 by Dec 1. Pay by ACH: routing 011000015, '
           'account 000123456789, or mail a check payable to City Water Example.')
UK_BILL = ('School trip invoice 7781. Please pay GBP 1,250.00 by 28 November to sort code 00-00-00, account 12345678, '
           'reference TRIP7781.')
EU_BILL = 'Factuur 2026/118: te betalen EUR 37,77 op BE71 0961 2345 6769 met mededeling +++090/9337/55493+++ voor 19/11.'
DEBIT = 'Your invoice 5520 for EUR 40.00 is available. It will be collected by direct debit on Nov 20; no action needed.'
US_PAID = 'We received your payment of $1,250.00 for invoice INV-2026-0042. Thank you.'


def mail(source_id, sender, title, body, at=NOW):
    return {'account_id': 'home', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': title, 'body': body,
            'deleted': False, 'metadata': {'from': sender, 'to': 'owner@example.com', 'thread_id': 't-' + source_id,
                                           'labels': ['INBOX', 'CATEGORY_UPDATES'], 'message-id': f'<{source_id}@x>'}}


def at(text):
    return patch_everywhere(a, 'now', lambda: text)


class Bills(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = tmp
        clock = patch_everywhere(a, 'now', return_value=NOW)
        clock.start()
        self.addCleanup(clock.stop)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite', protect=True)
        self.store.commit_page('home', {}, [
            mail('us', 'City Water <billing@citywater.example>', 'Your water bill', US_BILL),
            mail('uk', 'Example School <accounts@school.example.co.uk>', 'School trip invoice', UK_BILL),
            mail('eu', 'Studio <factuur@studio.example>', 'Factuur 2026/118', EU_BILL),
            mail('debit', 'Power Co <billing@power.example>', 'Your invoice', DEBIT)])

    def id(self, source_id):
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (source_id,)).fetchone()[0]

    def app(self):
        app = object.__new__(a.App)
        app.store = self.store
        app.config = {'accounts': [MAIL], 'digest_at': '08:30', 'review_worker': {'enabled': True}, 'prepare_ahead': False,
                      'openclaw_config': str(Path(self.tmp.name) / 'no-openclaw.json')}  # no model here: never a live turn
        return app

    def suggest(self, source_id, **extra):
        return self.app().action('suggest', {'dedupe_key': 'bill:' + source_id, 'title': 'Pay the bill', 'body': 'Details.', 'when': 'now',
                                             'event_ids': [self.id(source_id)], 'newer_checked': list(range(1, 50)),
                                             'mail_asks': 'Pay this bill', **extra})

    def card(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())

    def paid(self, sid, event_ids, when=LATER):
        with at(when):
            return self.app().action('looks_handled', {'suggestion_id': sid, 'paid': True, 'reason': 'Payment received on Nov 10',
                                                       'event_ids': event_ids})

    def confirmation(self, when=LATER):
        with at(when):
            self.store.commit_page('home', {}, [mail('us-paid', 'City Water <billing@citywater.example>', 'Payment received', US_PAID, when)])
        return self.id('us-paid')

    def test_the_review_is_told_to_judge_bills_by_meaning_wherever_they_come_from(self):
        prompt = a.review_prompt('r1', ['home'])
        for words in ('Bills:', 'routing', 'sort code', 'BSB', 'check is payable to', 'pay link', 'autopay', 'direct debit',
                      'never by its format', 'paid:true', 'bill {"payee", "invoice", "amount"}'):
            self.assertIn(words, prompt)
        agents = (ROOT / 'AGENTS.md').read_text()
        self.assertIn('**Bills to pay by hand**', agents)
        self.assertIn('`paid:true`', agents)

    def test_a_bill_to_do_keeps_the_bill_the_review_read_sealed(self):
        sid = self.suggest('us', bill={'payee': 'City Water', 'invoice': 'INV-2026-0042', 'amount': '$1,250.00'})['id']
        self.assertEqual(json.loads(self.card(sid)['bill']), {'payee': 'City Water', 'invoice': 'INV-2026-0042', 'amount': '$1,250.00'})
        with self.store.connect() as db:
            db.row_factory = None
            self.assertNotIn(b'INV-2026', db.execute('SELECT bill FROM suggestions WHERE id=?', (sid,)).fetchone()[0])
        with self.assertRaisesRegex(ValueError, 'bill is'):
            self.suggest('uk', bill={'iban': 'GB00'})
        self.assertIsNone(self.card(self.suggest('eu')['id'])['bill'])

    def test_a_newer_paid_confirmation_closes_an_open_bill_to_do_by_itself_with_undo_once(self):
        sid = self.suggest('us')['id']
        newer = self.confirmation()
        self.assertTrue(self.paid(sid, [newer])['closed'])
        card = self.card(sid)
        self.assertEqual(card['status'], 'completed')
        self.assertGreater(card['undo_until'], '2026-11-11T08:00')
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT source FROM decisions WHERE suggestion_id=? AND choice='complete'", (sid,)).fetchone()[0], 'handled')
        with at('2026-11-10T09:05:00+00:00'):
            self.assertEqual(self.store.decide(sid, 'undo', '', 'u1', 'dashboard')['status'], 'pending')
        self.assertNotIn('closed', self.paid(sid, [newer], '2026-11-10T09:10:00+00:00'))  # the owner took it back: it only looks done
        self.assertNotEqual(self.card(sid)['status'], 'completed')

    def test_an_older_message_or_the_bills_own_mail_only_looks_handled(self):
        sid = self.suggest('us')['id']
        self.assertEqual(self.paid(sid, [self.id('us')]), {'saved': True})
        card = self.card(sid)
        self.assertEqual(card['status'], 'pending')
        self.assertTrue(card['handled_hint'])
        with self.assertRaisesRegex(ValueError, 'short plain reason'):
            self.app().action('looks_handled', {'suggestion_id': sid, 'paid': True, 'reason': 'no', 'event_ids': [self.id('us')]})


class SameBill(unittest.TestCase):
    """A Family member's to-do for the same bill: by IBAN and reference, or else by sender, invoice number and amount."""

    def test_an_eu_bill_matches_on_its_iban_and_reference(self):
        self.assertEqual(family_done.bill_of(EU_BILL), 'BE71096123456769|090933755493')
        self.assertIsNone(family_done.bill_of(US_BILL))
        self.assertIsNone(family_done.bill_of(UK_BILL))

    def test_us_and_uk_bills_match_on_sender_invoice_and_amount(self):
        us = family_done.bill_fields({'payee': 'City Water', 'invoice': 'INV-2026-0042', 'amount': '$1,250.00'})
        self.assertEqual(family_done.bill_key(us, 'City Water <billing@citywater.example>'), 'citywater.example|INV20260042|125000')
        self.assertEqual(family_done.bill_key(family_done.bill_fields({'invoice': 'inv 2026 0042', 'amount': 'USD 1250.00'}),
                                              'pay@mail.citywater.example'), 'citywater.example|INV20260042|125000')
        uk = family_done.bill_fields({'invoice': '7781', 'amount': '£1,250.00'})
        self.assertEqual(family_done.bill_key(uk, 'accounts@school.example.co.uk'), 'example.co.uk|7781|125000')
        self.assertIsNone(family_done.bill_key(family_done.bill_fields({'amount': '$1,250.00'}), 'billing@citywater.example'))
        self.assertIsNone(family_done.bill_key(us, ''))
        self.assertIsNone(family_done.bill_fields({}))

    def test_a_to_dos_sources_carry_the_bill_without_an_iban(self):
        case = Bills('test_a_bill_to_do_keeps_the_bill_the_review_read_sealed')
        case.setUp()
        self.addCleanup(case.doCleanups)
        sid = case.suggest('us', bill={'payee': 'City Water', 'invoice': 'INV-2026-0042', 'amount': '$1,250.00'})['id']
        eu = case.suggest('eu')['id']
        with case.store.connect() as db:
            us_sources = family_done.sources(db, db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            eu_sources = family_done.sources(db, db.execute('SELECT * FROM suggestions WHERE id=?', (eu,)).fetchone())
        self.assertIn('bill:citywater.example|INV20260042|125000', us_sources)
        self.assertIn('bill:BE71096123456769|090933755493', eu_sources)


if __name__ == '__main__':
    unittest.main()
