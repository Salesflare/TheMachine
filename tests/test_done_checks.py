"""Done checks (machine/store/done_checks.py): a to-do waiting for a result a public page will show reads that page when
its time to chase comes, before it comes back to the owner. Shown: it closes by itself with Undo. Not there, unread or
moved on meanwhile: it comes back as before, never closed on a guess. Shown is checked against what was agreed first
(test_result_checks.py); here that turn says it matches. Made-up data; fake page reads; nothing is sent."""
import datetime as dt
import json
import unittest

import test_outcomes as to
from seams import patch_everywhere  # noqa: E402
from machine.store import done_checks, outcomes  # noqa: E402
from machine.store.cards import return_waiting  # noqa: E402
from machine.app import done_checks as app_checks  # noqa: E402
from sources import SourceError
import timeutil

URL = 'https://partner.example/best-crm-tools'
ASK = 'Happy to add Example CRM to our list at https://partner.example/best-crm-tools by Friday.'
RESULT = 'partner.example/best-crm-tools lists Example CRM'
CHECK = {'url': URL, 'expect': ['Example CRM']}
LIVE = ['Best CRM tools', 'Other CRM: for teams', 'Example CRM: for small teams']
BEFORE = ['Best CRM tools', 'Other CRM: for teams']
MATCHES = {'state': 'matches', 'checked': 'with the description you sent', 'shows': 'Example CRM: for small teams',
           'agreed': 'add Example CRM to our list'}  # both quotes really in the page and the thread (result_check.grounded)


def later(stamp, **delta):
    return (dt.datetime.fromisoformat(stamp) + dt.timedelta(**delta)).isoformat()


class DoneChecks(unittest.TestCase):
    row, decide, shown_body = to.Outcomes.row, to.Outcomes.decide, to.Outcomes.shown_body
    app, suggestion, send, checked = to.Outcomes.app, to.Outcomes.suggestion, to.Outcomes.send, to.Outcomes.checked

    def setUp(self):
        to.Outcomes.setUp(self)
        self.store.commit_page('work', {}, [to.email('m1', '2026-10-15T08:00:00+00:00', sender='sam@partner.example', body=ASK)])

    def waiting(self, check=CHECK, due=None, baseline=BEFORE):
        """The owner's ask went out and the to-do waits for the listing, with its page to check, read once as it is."""
        if due:
            with self.store.connect() as db:
                db.execute('UPDATE suggestions SET due=? WHERE id=?', (due, self.sid))
        with patch_everywhere(timeutil, 'now', return_value='2026-10-16T09:00:00+00:00'):
            self.send(done_when=RESULT)
        if check:
            with self.store.connect() as db:
                done_checks.set_check(db, self.sid, done_checks.clean(check), 'review')
            if baseline:
                self.assertTrue(str(self.step('2026-10-16T09:01:00+00:00', baseline)[0]).startswith('baseline:'))
        return json.loads(self.suggestion()['outcome'])['until']

    def test_a_page_that_already_shows_the_words_is_never_checked(self):
        until = self.waiting(baseline=LIVE)  # say an old article already lists it: the page can't tell the result
        self.assertEqual(json.loads(self.suggestion()['done_check'])['baseline']['state'], 'shown')
        kept, reads, back = self.step(later(until, minutes=1), LIVE)
        self.assertEqual((kept, reads, back), (None, [], 1))  # comes back as before, never closed
        self.assertEqual(self.suggestion()['status'], 'pending')

    def test_a_baseline_that_cant_be_read_leaves_no_check(self):
        until = self.waiting(baseline=None)
        at = '2026-10-16T09:01:00+00:00'
        for n in range(done_checks.MAX_ATTEMPTS):
            kept, reads, _ = self.step(at, error=SourceError('web_page_http'))
            self.assertEqual(reads, [URL])
            at = later(at, hours=1, minutes=1)
        self.assertEqual(kept, 'baseline:unread')
        kept, reads, back = self.step(later(until, minutes=1), LIVE)
        self.assertEqual((kept, reads, back), (None, [], 1))

    def step(self, at, lines=None, error=None, answer=MATCHES):
        """One done-check step at `at`; a page that shows the words is then checked (a stand-in turn), then return_waiting."""
        reads = []

        def read(url):
            reads.append(url)
            if error:
                raise error
            return lines
        app = self.app()
        with patch_everywhere(timeutil, 'now', return_value=at):
            kept = app.done_check_step(read=read)
            if kept == 'checking':
                kept = self.checked(answer)
            with self.store.connect() as db:
                back = return_waiting(db)
        return kept, reads, back

    def chat(self):
        with self.store.connect() as db:
            return json.dumps(self.app().card_chat_service(db, self.sid), ensure_ascii=False)

    def test_a_live_listing_closes_it_by_itself_with_undo_and_no_nudge(self):
        until = self.waiting()
        kept, reads, back = self.step(later(until, minutes=1), LIVE)
        row = self.suggestion()
        self.assertEqual((kept, reads, back), ('closed', [URL], 0))
        self.assertEqual(row['status'], 'completed')
        self.assertTrue(row['undo_until'])
        self.assertIsNone(row['chat_asks'])  # no nudge offered
        self.assertIn('Closed by itself: partner.example/best-crm-tools shows Example CRM', self.chat())
        with self.store.connect() as db:
            self.assertIsNone(db.execute("SELECT 1 FROM deliveries WHERE suggestion_id=? AND status='queued'", (self.sid,)).fetchone())
            jobs = db.execute('SELECT count(*) FROM action_jobs WHERE suggestion_id=?', (self.sid,)).fetchone()[0]
        self.assertEqual(jobs, 1)  # only the owner's own send: a check never queues one
        self.assertEqual(self.step(later(until, hours=3), LIVE)[1], [])  # closed: never read again

    def test_without_a_check_it_comes_back_as_before(self):
        until = self.waiting(check=None)
        kept, reads, back = self.step(later(until, minutes=1), LIVE)
        self.assertEqual((kept, reads, back), (None, [], 1))
        self.assertEqual(json.loads(self.suggestion()['outcome'])['state'], 'still_waiting')

    def test_not_there_yet_comes_back_with_the_nudge_and_says_it_checked(self):
        until = self.waiting()
        kept, reads, back = self.step(later(until, minutes=1), BEFORE)
        row = self.suggestion()
        self.assertEqual((kept, back), ('back', 1))
        self.assertEqual((row['status'], json.loads(row['outcome'])['state']), ('pending', 'still_waiting'))
        self.assertIn('Write a short nudge', json.loads(row['chat_asks']))
        self.assertIn('Checked partner.example/best-crm-tools: not there yet', self.chat())

    def test_a_part_of_the_result_is_not_the_result(self):
        until = self.waiting(check={'url': URL, 'expect': ['Example CRM', 'example.com']})
        self.assertEqual(self.step(later(until, minutes=1), LIVE)[0], 'back')  # the name, but not the link to the owner
        self.assertEqual(self.suggestion()['status'], 'pending')
        self.assertFalse(done_checks.shows(['Example CRMs and more'], ['Example CRM']))  # whole words only
        self.assertTrue(done_checks.shows(['Example   crm,', 'next'], ['example CRM']))

    def test_before_the_deadline_it_reads_once_more_after_it_before_coming_back(self):
        until = self.waiting(due='2026-10-30')
        kept, reads, back = self.step(later(until, minutes=1), BEFORE)
        self.assertEqual((kept, back), ('recheck', 0))
        self.assertEqual(self.suggestion()['status'], 'prepared')  # still waiting: no interruption yet
        plan = json.loads(self.suggestion()['done_check'])
        self.assertGreater(plan['run']['next_at'], '2026-10-30T23:00:00+00:00')  # the morning after the deadline
        self.assertEqual(self.step(later(until, hours=5), BEFORE)[:3], (None, [], 0))  # not before then
        kept, reads, back = self.step(later(plan['run']['next_at'], minutes=1), BEFORE)
        self.assertEqual((kept, reads, back), ('back', [URL], 1))
        self.assertEqual(self.suggestion()['status'], 'pending')

    def test_a_page_that_cannot_be_read_never_closes_it(self):
        until = self.waiting()
        at = later(until, minutes=1)
        for n in range(done_checks.MAX_ATTEMPTS):
            kept, reads, back = self.step(at, error=SourceError('web_page_http', 503))
            self.assertEqual((kept, back), ('retry' if n < done_checks.MAX_ATTEMPTS - 1 else 'back', 0 if n < done_checks.MAX_ATTEMPTS - 1 else 1))
            self.assertNotEqual(self.suggestion()['status'], 'completed')
            at = later(at, hours=1, minutes=1)
        self.assertEqual(self.suggestion()['status'], 'pending')
        self.assertIn('Couldn’t open partner.example/best-crm-tools', self.chat())
        self.assertEqual(self.step(later(at, hours=2), LIVE)[1], [])  # used up for this wait: no more reads

    def test_any_read_failure_is_unknown_too(self):
        until = self.waiting()
        self.assertEqual(self.step(later(until, minutes=1), error=OSError('reset'))[0], 'retry')
        self.assertEqual(self.suggestion()['status'], 'prepared')

    def test_an_address_its_messages_dont_give_is_never_kept(self):
        self.send(done_when=RESULT)
        with self.store.connect() as db, self.assertRaises(ValueError):
            done_checks.set_check(db, self.sid, done_checks.clean({'url': 'https://elsewhere.example/list', 'expect': ['Example CRM']}), 'review')
        self.assertIsNone(self.suggestion()['done_check'])
        with self.store.connect() as db:  # without https:// in the message is the same address
            self.assertTrue(done_checks.in_evidence(URL, ['see partner.example/best-crm-tools.']))
            self.assertFalse(done_checks.in_evidence(URL, ['see partner.example/best-crm-tools-2024']))
        for bad in ({'url': 'http://localhost/x', 'expect': ['a b']}, {'url': URL, 'expect': []}, {'url': URL, 'expect': ['x']},
                    {'url': URL, 'expect': ['a', 'b', 'c', 'd']}, 'https://x.example'):
            with self.assertRaises(ValueError):
                done_checks.clean(bad)

    def test_the_review_keeps_a_check_only_from_its_messages(self):
        app = self.app()
        app.config = {**app.config, 'digest_at': '08:30'}
        with self.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id='m1'").fetchone()[0]
        args = {'dedupe_key': 'listing', 'title': 'Get listed on partner.example', 'body': 'Sam will add us by Friday.',
                'event_ids': [event], 'done_when': RESULT}
        saved = app.action('suggest', {**args, 'done_check': CHECK})
        with self.store.connect() as db:
            self.assertEqual(json.loads(db.execute('SELECT done_check FROM suggestions WHERE id=?', (saved['id'],)).fetchone()[0])['url'], URL)
        self.store.commit_page('work', {}, [{**to.email('m9', '2026-10-15T09:00:00+00:00', sender='kim@review.example',
                                                         body='We will feature Example CRM in our top ten soon.'),
                                             'metadata': {'from': 'kim@review.example', 'thread_id': 'b2', 'labels': ['INBOX']}}])
        with self.store.connect() as db:
            other = db.execute("SELECT id FROM events WHERE source_id='m9'").fetchone()[0]
        made_up = app.action('suggest', {**args, 'dedupe_key': 'other', 'title': 'Get featured in the top ten', 'event_ids': [other],
                                         'body': 'Kim will feature us.', 'done_check': {'url': 'https://made-up.example/top', 'expect': ['Example CRM']}})
        self.assertNotEqual(made_up['id'], saved['id'])
        self.assertIn('Not kept', made_up['done_check'])
        with self.store.connect() as db:
            self.assertIsNone(db.execute('SELECT done_check FROM suggestions WHERE id=?', (made_up['id'],)).fetchone()[0])

    def test_a_new_result_line_drops_the_old_check(self):
        self.waiting()
        with self.store.connect() as db:
            outcomes.set_done_when(db, self.sid, 'Sam sent the signed form', 'run')
        self.assertIsNone(self.suggestion()['done_check'])

    def test_a_crash_mid_read_is_taken_again_and_bounded(self):
        until = self.waiting()
        at = later(until, minutes=1)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            self.assertEqual(len(done_checks.claim(db, at)), 1)  # claimed, then the Machine stopped before settle
        with self.store.connect() as db:
            self.assertEqual(done_checks.claim(db, later(at, minutes=5)), [])  # its lease holds
            self.assertEqual(return_waiting_at(db, later(at, minutes=5)), 0)  # and it isn't returned under it
        kept, reads, back = self.step(later(at, minutes=16), LIVE)  # the lease ran out: read again, once
        self.assertEqual((kept, reads), ('closed', [URL]))

    def test_a_check_that_never_runs_still_lets_it_come_back(self):
        until = self.waiting()  # its step broken or the Machine busy: after HOLD it comes back as before
        with self.store.connect() as db:
            self.assertEqual(return_waiting_at(db, later(until, minutes=1)), 0)
            self.assertEqual(return_waiting_at(db, later(until, hours=6, minutes=1)), 1)

    def test_a_result_counts_only_for_its_claim_on_a_to_do_that_still_waits(self):
        until = self.waiting()
        at = later(until, minutes=1)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            job = done_checks.claim(db, at)[0]
        self.decide('snooze', 'snooze-1')  # the owner moved it while the page was read
        with self.store.connect() as db:
            self.assertIsNone(done_checks.settle(db, job, 'met', later(at, minutes=1), fingerprint='f'))
        self.assertNotEqual(self.suggestion()['status'], 'completed')

    def test_the_same_page_closes_once_and_the_owners_undo_stands(self):
        until = self.waiting()
        at = later(until, minutes=1)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            job = done_checks.claim(db, at)[0]
        with self.store.connect() as db:
            self.assertEqual(done_checks.settle(db, job, 'met', at, fingerprint='f', lines=LIVE), 'checking')
        with self.store.connect() as db:  # the same result kept twice (a retried write): nothing more
            self.assertIsNone(done_checks.settle(db, job, 'met', at, fingerprint='f'))
        with patch_everywhere(timeutil, 'now', return_value=at):
            self.assertEqual(self.checked(MATCHES), 'closed')
        body = self.suggestion()['body']
        self.assertEqual(self.shown_body(), f'Done: {RESULT}, with the description you sent.')  # the card says the result, not the wait it was in
        self.assertEqual(self.suggestion()['body'], body)  # only shown: its own text stays
        with patch_everywhere(timeutil, 'now', return_value=later(at, hours=1)):
            self.decide('undo', 'undo-1')  # the owner says it isn't done
        self.assertNotEqual(self.suggestion()['status'], 'completed')
        self.assertEqual(self.shown_body(), body)
        kept, reads, _ = self.step(later(at, hours=2), LIVE)
        self.assertEqual((kept, reads), (None, []))  # never read or closed again for this wait
        self.assertNotEqual(self.suggestion()['status'], 'completed')

    def test_the_read_goes_through_the_polite_page_reader(self):
        calls = []

        def read(url, state, error):
            calls.append((url, state))
            return 200, 'Best CRM tools', LIVE
        with patch_everywhere(app_checks.web_page, 'read', side_effect=read):
            self.assertEqual(app_checks.read_page(URL), LIVE)
        self.assertEqual(calls, [(URL, {})])  # a fresh read: no cached copy stands in for the page now


def return_waiting_at(db, at):
    with patch_everywhere(timeutil, 'now', return_value=at):
        return return_waiting(db)


if __name__ == '__main__':
    unittest.main()
