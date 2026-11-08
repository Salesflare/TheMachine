"""Automated and bulk signals wait for a batch review (machine/store/review_wait.py); signals from people start one as
before. Classified without a model; unsure is a person's."""
import datetime as dt
from pathlib import Path
import tempfile
import unittest

from seams import patch_everywhere  # noqa: E402
import review_day

a = review_day.load()
from machine.store import review_wait as w  # noqa: E402

T = dt.datetime(2026, 11, 7, 8, 0, tzinfo=dt.timezone.utc)


def row(kind, title='Hello', **metadata):
    return {'kind': kind, 'title': title, 'metadata': metadata, 'deleted': 0}


def mail(title='Hello', **metadata):
    return row('gmail.message', title, **{'to': 'owner@example.com', 'labels': ['INBOX'], **metadata})


class Known:
    """People for the test: alex@example.org is a person in the Graph, hi@club.example.com a mailing it left out."""
    def person(self, address):
        return address == 'alex@example.org'

    def mailing(self, address):
        return address == 'hi@club.example.com'


class Classify(unittest.TestCase):
    def waits(self, r):
        return w.can_wait(r, Known())

    def test_automated_and_bulk_mail_waits(self):
        self.assertEqual(self.waits(mail('Weekly digest', **{'from': 'Digest <weekly@news.example.com>', 'list_unsubscribe': True})), 'list')
        self.assertEqual(self.waits(mail('Updates', **{'from': 'Club <club@example.com>', 'precedence': 'bulk'})), 'precedence')
        self.assertEqual(self.waits(mail('Out of office', **{'from': 'Pat <pat@example.com>', 'auto_submitted': True})), 'automated')
        self.assertEqual(self.waits(mail('Your order has shipped', **{'from': 'Shop <no-reply@shop.example.com>'})), 'system')
        self.assertEqual(self.waits(mail('Your receipt', **{'from': 'Shop <receipts@shop.example.com>'})), 'system')
        self.assertEqual(self.waits(mail('VAT receipt: pay within 14 days', **{'from': 'Billing <billing@shop.example.com>'})), 'system')
        self.assertEqual(self.waits(mail('News', **{'from': 'Club <hi@club.example.com>'})), 'mailing')
        self.assertEqual(self.waits(mail('Sale', **{'from': 'Shop <hi@shop.example.com>', 'labels': ['CATEGORY_PROMOTIONS']})), 'category')
        self.assertEqual(self.waits(mail('Sale ends today', **{'from': 'Shop <hi@shop.example.com>', 'labels': ['CATEGORY_PROMOTIONS']})), 'category')

    def test_mail_from_people_and_anything_unsure_does_not_wait(self):
        self.assertIsNone(self.waits(mail('Quick question', **{'from': 'Robin Roe <robin@example.net>'})))  # someone new, in Primary
        self.assertIsNone(self.waits(mail('Re: plan', **{'from': 'Owner <owner@example.com>', 'labels': ['SENT']})))
        self.assertIsNone(self.waits(mail('Re: plan', **{'from': 'Owner <owner@example.com>', 'from_me': True})))
        # a reply, also from a ticket system with list headers: a thread someone is in
        self.assertIsNone(self.waits(mail('Re: your ticket', **{'from': 'Help <no-reply@help.example.com>', 'in-reply-to': '<a@b>', 'list_id': 'x'})))
        # someone the owner knows, also when Gmail put them in Updates or their mail has a list header
        self.assertIsNone(self.waits(mail('Notes', **{'from': 'Alex Doe <alex@example.org>', 'labels': ['CATEGORY_UPDATES'], 'list_unsubscribe': True})))
        # a calendar invitation is a person's, sent by the calendar
        self.assertIsNone(self.waits(mail('Invitation: Call', **{'from': 'Sam <calendar-notification@google.com>'})))
        self.assertIsNone(self.waits(mail('Updated invitation', **{'from': 'Sam <sam@group.calendar.google.com>', 'labels': ['CATEGORY_UPDATES']})))
        self.assertIsNone(self.waits(mail('Hello', **{'from': ''})))

    def test_a_time_sensitive_title_does_not_wait_except_in_promotions(self):
        for title in ('Payment failed for your plan', 'Security alert: new sign-in', 'Action required: verify your account',
                      'Invoice due today', 'Your meeting starts in 10 minutes', 'Dringend: factuur'):
            self.assertIsNone(self.waits(mail(title, **{'from': 'Shop <no-reply@shop.example.com>', 'labels': ['CATEGORY_UPDATES']})), title)

    def test_phone_notifications_from_chat_and_calendar_apps_do_not_wait(self):
        self.assertEqual(self.waits(row('android.notification', 'Rain at 4 pm', package_name='com.example.weather')), 'phone')
        self.assertEqual(self.waits(row('android.notification', 'New episode', package_name='com.example.podcasts', category='promo')), 'phone')
        for package in ('com.whatsapp', 'org.telegram.messenger', 'com.google.android.apps.messaging', 'com.google.android.dialer',
                        'com.Slack', 'com.google.android.calendar'):
            self.assertIsNone(self.waits(row('android.notification', 'Sam', package_name=package)), package)
        self.assertIsNone(self.waits(row('android.notification', 'Sam', package_name='com.example.chat', category='msg')))
        self.assertIsNone(self.waits(row('android.notification', 'Missed call', package_name='com.example.voip', category='missed_call')))
        self.assertIsNone(self.waits(row('android.notification', 'Unknown')))  # which app is not known: unsure

    def test_chats_wait_only_when_no_person_wrote_them(self):
        self.assertIsNone(self.waits(row('whatsapp.message', 'Sam', chat_id='32470000000@s.whatsapp.net')))
        self.assertIsNone(self.waits(row('whatsapp.message', 'Family', chat_id='1203630@g.us')))
        self.assertEqual(self.waits(row('whatsapp.message', 'A channel', chat_id='1203630@newsletter')), 'channel')
        self.assertIsNone(self.waits(row('slack.message', 'Sam', user_id='U1')))
        self.assertEqual(self.waits(row('slack.message', 'Deploy finished', bot_id='B1', subtype='bot_message')), 'bot')
        self.assertIsNone(self.waits(row('slack.message', 'URGENT: site down', bot_id='B1')))

    def test_system_kinds_wait_and_everything_else_does_not(self):
        self.assertEqual(self.waits(row('stripe.event', 'Payment succeeded', type='charge.succeeded')), 'system')
        self.assertIsNone(self.waits(row('stripe.event', 'Dispute opened', type='charge.dispute.created')))
        self.assertEqual(self.waits(row('github.ci', 'CI failed on main')), 'system')
        self.assertEqual(self.waits(row('rss.item', 'A post')), 'system')
        for kind in ('calendar.event', 'intercom.conversation', 'linkedin.message', 'telegram.message', 'x.mention', 'github.notification',
                     'owner.card', 'salesflare.email', 'machine.fault', 'teams.message', 'zoom.summary', 'something.new'):
            self.assertIsNone(self.waits(row(kind)), kind)

    def test_batch_wait_setting(self):
        self.assertEqual(w.batch_wait({}), w.BATCH_WAIT_MINUTES)
        self.assertEqual(w.batch_wait({'batch_wait_minutes': 30}), 30)
        for off in (0, False, None, -5, 'x'):
            self.assertEqual(w.batch_wait({'batch_wait_minutes': off}), 0, off)
        # with the gap after a run (10 min) and the run itself, a batched to-do is there within the hour
        self.assertLessEqual(w.BATCH_WAIT_MINUTES + 10, 55)


class Runner:
    def __init__(self, *results):
        self.results, self.requests = list(results), []

    def __call__(self, request):
        self.requests.append(request)
        return {'status': self.results.pop(0)}


class Worker(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.quick_first_review = lambda db: 0
        self.app.config = {'accounts': [{'id': 'work'}], 'review_worker': {'enabled': True, 'min_signals': 40, 'max_wait_minutes': 15,
                                                                           'gap_seconds': 600, 'timeout_seconds': 1500}}

    def add(self, at, source_id, **metadata):
        with patch_everywhere(a, 'now', return_value=at.isoformat()):
            self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at.isoformat(),
                                                 'title': metadata.pop('title', 'Hello'), 'body': 'Text', 'metadata': metadata, 'deleted': False}])

    def step(self, runner, at):
        with patch_everywhere(a, 'now', return_value=at.isoformat()):
            return self.app.review_step(runner)

    def queue(self, at):
        with patch_everywhere(a, 'now', return_value=at.isoformat()), self.store.connect() as db:
            return self.app.review_queue(db, at)

    def newsletter(self, at, n=1):
        for i in range(n):
            self.add(at, f'news-{at.minute}-{i}', **{'from': 'Digest <weekly@news.example.com>', 'list_unsubscribe': True, 'labels': ['INBOX']})

    def test_a_newsletter_alone_waits_for_the_batch_not_15_minutes(self):
        self.newsletter(T)
        self.assertIsNone(self.step(Runner(), T + dt.timedelta(minutes=16)))
        self.assertEqual(self.queue(T + dt.timedelta(minutes=16))['starts_at'], (T + dt.timedelta(minutes=w.BATCH_WAIT_MINUTES)).isoformat())
        self.assertIsNone(self.step(Runner(), T + dt.timedelta(minutes=w.BATCH_WAIT_MINUTES - 1)))
        self.assertEqual(self.step(Runner('admitted'), T + dt.timedelta(minutes=w.BATCH_WAIT_MINUTES)), 'admitted')

    def test_a_person_starts_the_review_after_15_minutes_and_waiting_newsletters_join_it(self):
        self.newsletter(T, 3)
        self.add(T + dt.timedelta(minutes=5), 'person', **{'from': 'Robin Roe <robin@example.net>', 'labels': ['INBOX']})
        self.assertEqual(self.queue(T + dt.timedelta(minutes=6))['starts_at'], (T + dt.timedelta(minutes=20)).isoformat())
        self.assertIsNone(self.step(Runner(), T + dt.timedelta(minutes=19)))
        runner = Runner('admitted')
        self.assertEqual(self.step(runner, T + dt.timedelta(minutes=20)), 'admitted')
        job = runner.requests[0]['job_id']
        with patch_everywhere(a, 'now', return_value=(T + dt.timedelta(minutes=20)).isoformat()):
            claim = self.store.begin_analysis(['work'], 120, a.REVIEW_SESSION_PREFIX + job, job)
        self.assertEqual(claim['claimed'], 4)  # the person's mail and the three newsletters, in one review

    def test_a_receipt_with_a_deadline_is_reviewed_within_the_hour(self):
        self.add(T, 'vat', title='VAT receipt: pay within 14 days', **{'from': 'Billing <billing@shop.example.com>', 'labels': ['INBOX']})
        self.assertIsNone(self.step(Runner(), T + dt.timedelta(minutes=30)))
        self.assertEqual(self.step(Runner('admitted'), T + dt.timedelta(minutes=w.BATCH_WAIT_MINUTES)), 'admitted')

    def test_a_time_sensitive_automated_mail_goes_like_a_persons(self):
        self.add(T, 'alert', title='Security alert: new sign-in', **{'from': 'Acct <no-reply@acct.example.com>', 'labels': ['INBOX']})
        self.assertEqual(self.step(Runner('admitted'), T + dt.timedelta(minutes=15)), 'admitted')

    def test_enough_waiting_starts_a_review_whatever_they_are(self):
        self.newsletter(T, 40)
        self.assertEqual(self.step(Runner('admitted'), T + dt.timedelta(minutes=1)), 'admitted')

    def test_without_a_batch_every_signal_waits_15_minutes_as_before(self):
        self.app.config['review_worker']['batch_wait_minutes'] = 0
        self.newsletter(T)
        self.assertIsNone(self.step(Runner(), T + dt.timedelta(minutes=14)))
        self.assertEqual(self.step(Runner('admitted'), T + dt.timedelta(minutes=15)), 'admitted')


class Day(unittest.TestCase):
    """A day of a test persona's signals (tests/review_day.py), before (no batch) and after."""

    @classmethod
    def setUpClass(cls):
        cls.before, cls.after = review_day.replay(a, batch_wait_minutes=0, step_minutes=2), review_day.replay(a, step_minutes=2)

    def test_fewer_reviews_and_tokens(self):
        # chats from people come in all day and keep their 15 minutes, so the saving is the reviews automated
        # signals started on their own: about a sixth on this day
        self.assertLess(self.after['reviews'], self.before['reviews'] * 0.9)
        self.assertLess(self.after['tokens']['fresh'], self.before['tokens']['fresh'] * 0.9)

    def test_every_signal_is_reviewed_and_none_waits_past_the_hour(self):
        for result in (self.before, self.after):
            self.assertEqual(len(result['waits']), result['signals'])
        self.assertLessEqual(max(m for _, m in self.after['waits'].values()), 60)

    def test_no_signal_from_a_person_waits_past_the_usual_15_minutes_and_the_gap(self):
        # a person's signal starts a review once it waited 15 minutes, as before (a newsletter no longer starts one
        # early for it, so some wait longer than they happened to before, never past the 15 minutes)
        before = max(m for p, m in self.before['waits'].values() if p)
        after = max(m for p, m in self.after['waits'].values() if p)
        self.assertLessEqual(after, max(before, 15 + 2))  # 2: the replay's step


if __name__ == '__main__':
    unittest.main()
