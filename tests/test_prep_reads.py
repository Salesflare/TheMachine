"""A to-do's run reads less (machine/app/prep_reads.py): its job message says what the review found (the to-do's
messages with who wrote them, to whom, the subject and thread, never their text), and within one run a message read
whole already comes back as a short note instead of its text again. Offline, made-up data."""
import tempfile
import unittest
from pathlib import Path

import machine.main as machine_main
from machine.app import prep_reads

ACCOUNTS = [{'id': 'work-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@larkspur.example', 'boundary': 'work:Larkspur'}]
BODY = 'Could you send the signed quote by Friday? The board meets Monday. ' * 3


def mail(source_id, subject, sender, thread, body=BODY):
    return {'account_id': 'work-mail', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': '2026-11-20T09:15:00+00:00',
            'title': subject, 'body': body, 'deleted': False,
            'metadata': {'from': sender, 'to': 'Robin Hale <robin@larkspur.example>', 'thread_id': thread}}


class ReadLess(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = ACCOUNTS
        self.app = object.__new__(machine_main.App); self.app.store = self.store
        self.app.config = {'accounts': ACCOUNTS, 'prepare_ahead': False, 'database': str(Path(self.temp.name) / 'e.sqlite')}
        self.store.config = self.app.config
        self.store.commit_page('work-mail', {}, [mail('m1', 'Signed quote for the rebrand', 'Tobias Brandt <tobias@fjordline.example>', 'th-41'),
                                                 mail('m2', 'Board slides', 'Mia Okafor <mia@fjordline.example>', 'th-42', 'The slides are attached.')])

    def suggest(self):
        return self.app.action('suggest', {'dedupe_key': 'fjordline:quote', 'title': 'Send Tobias the signed quote',
                                           'body': 'Tobias needs the **signed quote** by Friday for Monday\'s board.',
                                           'event_ids': [1], 'org': 'Fjordline', 'due': '2026-11-27'})['id']

    def events(self, run=None, **args):
        return self.app.action('events', {'account_ids': ['work-mail'], **({'_prep_run': run} if run else {}), **args})

    def test_the_job_message_says_what_the_review_found_without_the_text(self):
        sid = self.suggest()
        with self.store.connect() as db:
            brief = prep_reads.review_brief(db, sid)
        self.assertIn('What the review found when it made this to-do', brief)
        self.assertIn('To-do: Send Tobias the signed quote', brief)
        self.assertIn('Due: 2026-11-27', brief)
        line = next(x for x in brief.splitlines() if x.startswith('- event 1 '))
        for part in ('gmail.message, Fri 2026-11-20', 'local time','from Tobias Brandt <tobias@fjordline.example>', 'to Robin Hale <robin@larkspur.example>',
                     '"Signed quote for the rebrand"', 'thread th-41'):
            self.assertIn(part, line)
        self.assertNotIn('The board meets Monday', brief)  # a header, never the message itself: the run reads that once
        self.assertNotIn('event 2 ', brief)  # only the messages it came from
        self.assertIn('look up only what is still missing', brief)
        self.assertIn('"already read above"', brief)
        with self.store.connect() as db:
            self.assertEqual(prep_reads.review_brief(db, 'nope'), '')

    def test_a_preparation_starts_from_it(self):
        sid = self.suggest()
        self.store.decide(sid, 'accept', '', 'click-1', 'dashboard')
        sent = []
        self.app.preparation_step(lambda req: sent.append(req) or {'status': 'admitted'})
        message = next(r['message'] for r in sent if r.get('message'))
        self.assertIn('What the review found when it made this to-do', message)
        self.assertIn('thread th-41', message)
        self.assertLess(message.index('Its accounts'), message.index('What the review found'))

    def test_a_run_reads_each_message_once(self):
        first = self.events('run-a', event_ids=[1, 2])
        self.assertEqual(sorted(e['id'] for e in first['events']), [1, 2])
        self.assertNotIn('already_read', first)
        again = self.events('run-a', event_ids=[1])
        self.assertEqual((again['events'], again['already_read']), ([], [1]))
        self.assertIn('again:true', again['note'])
        self.assertNotIn('board meets', str(again))
        # a search that finds one read already and nothing new: its id, not its text
        found = self.events('run-a', query='quote')
        self.assertEqual((found['events'], found['already_read']), ([], [1]))
        # again:true, another run, the dashboard (no run) and a later body part read in full, as before
        self.assertEqual([e['id'] for e in self.events('run-a', event_ids=[1], again=True)['events']], [1])
        self.assertEqual([e['id'] for e in self.events('run-b', event_ids=[1])['events']], [1])
        self.assertEqual([e['id'] for e in self.events(event_ids=[1])['events']], [1])
        self.assertEqual(self.events('run-a', event_ids=[1], body_offset=10)['events'][0]['id'], 1)
        # a message the run hasn't read yet comes whole next to the note for the one it has
        self.store.commit_page('work-mail', {}, [mail('m3', 'Re: Signed quote for the rebrand', 'Tobias Brandt <tobias@fjordline.example>', 'th-41', 'Any news?')])
        mixed = self.events('run-a', event_ids=[1, 3])
        self.assertEqual(([e['id'] for e in mixed['events']], mixed['already_read']), ([3], [1]))

    def test_only_a_page_shown_from_its_start_counts_as_read(self):
        reads = prep_reads.RunReads()
        reads.mark('r', [{'id': 1}, {'id': 2, 'body_offset': 400}, {'id': 3, 'body_matched': True}, {'id': 4, 'body_offset': 0, 'body_clipped': True}])
        self.assertEqual(reads.split('r', [{'id': i} for i in (1, 2, 3, 4)]), ([{'id': 2}, {'id': 3}], [1, 4]))

    def test_runs_are_forgotten_after_a_while_and_past_the_limit(self):
        now = [0.0]
        reads = prep_reads.RunReads(runs=2, seconds=60, clock=lambda: now[0])
        reads.mark('a', [{'id': 1}]); reads.mark('b', [{'id': 1}]); reads.mark('c', [{'id': 1}])
        self.assertEqual(reads.split('a', [{'id': 1}])[1], [])  # the oldest went to make room
        self.assertEqual(reads.split('c', [{'id': 1}])[1], [1])
        now[0] = 120
        self.assertEqual(reads.split('c', [{'id': 1}])[1], [])  # a restart or a long pause: read in full again

    def test_a_history_page_read_before_in_the_run_comes_back_unchanged(self):
        """Runs re-read preparation_history again and again; its pages only list earlier runs, so they don't change."""
        reads, page = prep_reads.RunReads(), {'history': '[{"tool":"browser"}]', 'next_offset': None, 'instruction': 'Earlier calls.'}
        self.assertEqual(prep_reads.history_once(reads, 'r1', {'offset': 0}, page), page)
        again = prep_reads.history_once(reads, 'r1', {'offset': 0}, page)
        self.assertEqual((again['unchanged'], again['next_offset']), (True, None))
        self.assertNotIn('history', again)
        self.assertEqual(prep_reads.history_once(reads, 'r1', {'offset': 0, 'again': True}, page), page)  # asked anew
        self.assertEqual(prep_reads.history_once(reads, 'r2', {'offset': 0}, page), page)  # another run
        self.assertEqual(prep_reads.history_once(reads, 'r1', {'offset': 24000}, page), page)  # another page
        changed = {**page, 'history': '[{"tool":"exec"}]'}
        self.assertEqual(prep_reads.history_once(reads, 'r1', {'offset': 0}, changed), changed)  # a new page reads whole
        self.assertEqual(prep_reads.history_once(reads, None, {'offset': 0}, page), page)


if __name__ == '__main__':
    unittest.main()
