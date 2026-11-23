"""Refunds (refunds.py, docs/help/promises.md "Refunds"): money back a message promised the owner is kept as someone
else's promise with its amount, who pays it and its day, checked against the message; plain code watches for the money
back and, when it isn't in by that day, makes one quiet chase to-do with a draft to the contact. Money back closes it
by itself. Made-up shops and amounts, no model and no live calls."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

import test_ux as ux
import timeutil
from seams import patch_everywhere  # noqa: E402

import refunds  # noqa: E402
import machine.main as machine_main
import machine.prompts.review as machine_prompts_review

ROOT = Path(__file__).parent.parent
MAIL = {'id': 'home', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'personal'}
PHONE = {'id': 'phone', 'service': 'android', 'boundary': 'personal'}
MADE = '2026-11-02T09:00:00+00:00'  # a Monday
PROMISED = ('Your order A-1042 was canceled. We will refund EUR 42.00 to your card within 5-10 business days. '
            'Questions? Write to help@shop.example.')


def mail(source_id, sender, title, body, at=MADE, thread=None):
    return {'account_id': 'home', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': title, 'body': body,
            'deleted': False, 'metadata': {'from': sender, 'to': 'owner@example.com', 'thread_id': thread or 't-' + source_id,
                                           'labels': ['INBOX', 'CATEGORY_UPDATES'], 'message-id': f'<{source_id}@x>'}}


class Refunds(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = tmp
        zone = patch.object(timeutil, 'LOCAL_TZ', ZoneInfo('Europe/Brussels'))
        zone.start()
        self.addCleanup(zone.stop)
        self.clock = patch_everywhere(timeutil, 'now', return_value='2026-11-02T10:00:00+00:00')
        self.clock.start()
        self.addCleanup(lambda: self.clock.stop())
        self.store = machine_main.Store(Path(tmp.name) / 'events.sqlite', protect=True)
        self.store.commit_page('home', {}, [
            mail('shop', 'Example Shop <orders@shop.example>', 'Order A-1042 canceled', PROMISED),
            mail('noreply', 'Air Example <no-reply@air.example>', 'Claim approved',
                 'Your claim 88-1234 is approved. A refund of $250 will be paid by Nov 20, 2026.'),
            mail('vague', 'Studio <hi@studio.example>', 'About your booking', 'We will refund you soon.')])

    def at(self, stamp):
        self.clock.stop()
        self.clock = patch_everywhere(timeutil, 'now', return_value=stamp)
        self.clock.start()

    def id(self, source_id):
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (source_id,)).fetchone()[0]

    def app(self):
        app = object.__new__(machine_main.App)
        app.store = self.store
        app.config = {'accounts': [MAIL, PHONE], 'digest_at': '08:30', 'review_worker': {'enabled': True}, 'prepare_ahead': False,
                      'owner_name': 'Robin Example', 'openclaw_config': str(Path(self.tmp.name) / 'no-openclaw.json')}

        def no_model(config, text):
            raise AssertionError('a refund never asks a model')
        app.promise_check_model = no_model
        return app

    def record(self, source_id='shop', **extra):
        args = {'direction': 'theirs', 'event_id': self.id(source_id), 'who': 'Example Shop', 'what': 'refund the canceled order',
                'due': '2026-11-16', 'refund': {'amount': '42.00', 'currency': 'EUR', 'ref': 'A-1042', 'contact': 'help@shop.example'}}
        return self.app().action('promise', {**args, **extra})

    def promise(self, pid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM promises WHERE id=?', (pid,)).fetchone())

    def todos(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM suggestions WHERE dedupe_key LIKE 'promise:%'")]

    def due_step(self):
        self.at('2026-11-17T08:00:00+00:00')  # the morning after its day
        self.app().promise_step()

    def test_the_review_is_told_to_record_refunds_as_promises_never_to_dos(self):
        prompt = machine_prompts_review.review_prompt('r1', ['home'])
        for words in ('Refunds:', 'refund {"amount", "currency", "ref", "contact"}', '5-10 business days', 'Only when the amount',
                      'status kept', 'looks_handled paid:true'):
            self.assertIn(words, prompt)
        self.assertIn('## Refunds', (ROOT / 'docs/help/promises.md').read_text())

    def test_a_refund_is_kept_sealed_with_what_the_message_shows(self):
        pid = self.record()['id']
        self.assertEqual(json.loads(self.promise(pid)['refund']), {'amount': '42.00', 'currency': 'EUR', 'ref': 'A-1042',
                                                                  'contact': 'help@shop.example', 'site': 'shop.example'})
        self.assertIsNone(self.promise(pid)['watch'])  # a reply in the thread is no money back
        with self.store.connect() as db:
            db.row_factory = None
            self.assertNotIn(b'A-1042', db.execute('SELECT refund FROM promises WHERE id=?', (pid,)).fetchone()[0])

    def test_quality_or_nothing_amount_day_and_payer_must_show_in_the_message(self):
        with self.assertRaisesRegex(ValueError, 'refund amount and currency'):
            self.record(refund={'amount': '24.00', 'currency': 'EUR'})
        with self.assertRaisesRegex(ValueError, 'refund amount and currency'):
            self.record('vague', refund={'amount': '42.00', 'currency': 'EUR'})
        with self.assertRaisesRegex(ValueError, 'A refund needs due'):
            self.record(due=None)
        with self.assertRaisesRegex(ValueError, 'due is the last day'):
            self.record(due='2026-12-24')
        with self.assertRaisesRegex(ValueError, 'refund is'):
            self.record(refund={'amount': '42.00', 'currency': 'EUR', 'iban': 'x'})
        with self.assertRaisesRegex(ValueError, "direction 'theirs'"):
            self.record(direction='mine')
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM promises').fetchone()[0], 0)

    def test_a_made_up_order_number_or_a_no_reply_contact_is_left_out(self):
        pid = self.record('noreply', who='Air Example', due='2026-11-20',
                          refund={'amount': '250', 'currency': 'USD', 'ref': 'ZZ-999', 'contact': 'no-reply@air.example'})['id']
        refund = json.loads(self.promise(pid)['refund'])
        self.assertEqual((refund['ref'], refund['contact']), ('', ''))

    def test_spans_count_business_days_from_the_message(self):
        monday = dt.date(2026, 11, 2)
        self.assertEqual(refunds.business_days(monday, 10), dt.date(2026, 11, 16))
        self.assertTrue(refunds.due_shown(PROMISED, monday, dt.date(2026, 11, 16)))
        self.assertTrue(refunds.due_shown('Refund within 2 weeks.', monday, dt.date(2026, 11, 16)))
        self.assertTrue(refunds.due_shown('Terugbetaling uiterlijk 20/11.', monday, dt.date(2026, 11, 20)))
        self.assertFalse(refunds.due_shown('We will refund you soon.', monday, dt.date(2026, 11, 16)))
        self.assertEqual(refunds.money_text({'amount': '42.00', 'currency': 'EUR'}), '€42')
        self.assertEqual(refunds.money_text({'amount': '1250.50', 'currency': 'USD'}), '$1,250.50')
        self.assertEqual(refunds.money_text({'amount': '80.00', 'currency': 'CHF'}), '80 CHF')

    def test_one_due_long_ago_is_not_watched(self):
        self.at('2026-12-01T10:00:00+00:00')
        self.assertIn('skipped', self.record())

    def test_money_back_before_its_day_closes_it_with_no_to_do(self):
        pid = self.record()['id']
        self.store.commit_page('home', {}, [mail('done', 'Example Shop <orders@shop.example>', 'Refund processed',
                                                 'Refund for order A-1042: EUR 42.00 is on its way to your card.', '2026-11-09T09:00:00+00:00')])
        self.due_step()
        row = self.promise(pid)
        self.assertEqual(row['status'], 'kept')
        self.assertEqual(row['note'], 'The €42 refund came in')
        self.assertEqual(self.todos(), [])

    def test_a_message_that_moved_its_day_is_no_money_back(self):
        pid = self.record()['id']
        self.store.commit_page('home', {}, [mail('later', 'Example Shop <orders@shop.example>', 'Your refund',
                                                 'Order A-1042: your EUR 42.00 refund is delayed until Nov 20, 2026.', '2026-11-10T09:00:00+00:00')])
        self.app().action('promise', {'id': pid, 'due': '2026-11-20', 'event_id': self.id('later'), 'reason': 'Delayed'})
        self.at('2026-11-21T08:00:00+00:00')
        self.app().promise_step()
        self.assertEqual(self.promise(pid)['status'], 'carded')

    def test_the_draft_is_signed_also_without_owner_name(self):
        (Path(self.tmp.name) / 'USER.md').write_text('# About me\n\n- Name: Robin Vale\n', encoding='utf-8')
        plain = self.app

        def app():
            made = plain()
            made.config.update(owner_name='', openclaw_workspace=self.tmp.name)
            return made
        self.app = app
        self.record()
        self.due_step()
        self.assertTrue(json.loads(self.todos()[0]['next_action'])['body'].rstrip().endswith('Robin Vale'))

    def test_not_in_by_its_day_one_quiet_chase_to_do_with_a_draft(self):
        pid = self.record()['id']
        self.due_step()
        self.app().promise_step()  # once
        todos = self.todos()
        self.assertEqual(len(todos), 1)
        todo = todos[0]
        self.assertEqual(todo['title'], 'Chase the €42 refund from Example Shop')
        self.assertEqual(todo['body'], 'Promised on Mon, Nov 2 (A-1042), to be in by Mon, Nov 16. Nothing shows it came in yet.')
        self.assertIsNone(todo['due'])
        self.assertEqual(todo['status'], 'prepared')
        draft = json.loads(todo['next_action'])
        self.assertEqual((draft['kind'], draft['to']), ('email', ['help@shop.example']))
        self.assertEqual(draft['subject'], 'Refund for A-1042')
        self.assertIn('a refund of €42 (A-1042)', draft['body'])
        self.assertFalse(todo['outcome'])  # no "Needs you" line: Review and send says it
        self.assertTrue(draft['body'].rstrip().endswith('Robin Example'))
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM deliveries WHERE suggestion_id=?', (todo['id'],)).fetchone()[0], 'not_sent')
            self.assertEqual(db.execute("SELECT count(*) FROM action_jobs WHERE suggestion_id=? AND status IN ('queued','sending')", (todo['id'],)).fetchone()[0], 0)
        self.assertEqual(self.promise(pid)['status'], 'carded')

    def test_its_dates_are_written_as_the_dashboard_writes_them_for_the_owner(self):
        import locale_prefs
        locale_prefs.configure({'locale': 'en-BE'})
        self.addCleanup(locale_prefs.configure, {})
        self.record()
        self.due_step()
        todo = self.todos()[0]
        self.assertEqual(todo['body'], 'Promised on Mon 2 Nov (A-1042), to be in by Mon 16 Nov. Nothing shows it came in yet.')
        self.assertIn('On Mon 2 Nov you confirmed', json.loads(todo['next_action'])['body'])

    def test_money_back_later_closes_the_chase_to_do_by_itself_with_undo(self):
        self.record()
        self.due_step()
        sid = self.todos()[0]['id']
        self.at('2026-11-18T09:00:00+00:00')
        self.store.commit_page('home', {}, [mail('paypal', 'service@paypal.com', 'You received a refund',
                                                 'Example Shop sent you a refund of €42.00.', '2026-11-18T08:00:00+00:00')])
        self.app().promise_step()
        todo = self.todos()[0]
        self.assertEqual(todo['status'], 'completed')
        self.assertGreater(todo['undo_until'], '2026-11-18T09:00')

    def test_a_bank_apps_notification_counts_as_money_back(self):
        pid = self.record()['id']
        self.store.commit_page('phone', {}, [{'account_id': 'phone', 'source_id': 'bank', 'kind': 'android.notification',
                                              'occurred_at': '2026-11-12T09:00:00+00:00', 'title': 'Bank Example', 'deleted': False,
                                              'body': '+ 42,00 € from EXAMPLE SHOP', 'metadata': {'package_name': 'bank.example', 'app_name': 'Bank'}}])
        self.due_step()
        self.assertEqual(self.promise(pid)['status'], 'kept')

    def test_the_same_amount_from_someone_else_is_no_money_back(self):
        pid = self.record()['id']
        self.store.commit_page('home', {}, [mail('other', 'Other Store <sales@other.example>', 'Receipt',
                                                 'You paid EUR 42.00 for your order.', '2026-11-09T09:00:00+00:00')])
        self.due_step()
        self.assertEqual(self.promise(pid)['status'], 'carded')


if __name__ == '__main__':
    unittest.main()
