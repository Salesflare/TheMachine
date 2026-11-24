"""What the checks that close to-dos and promises by themselves read of a message (machine/store/judged_words.py): its
own words past the old 400 characters, a mark when still cut, and its files where the source keeps them. Made-up
messages only, no model."""
import json
import tempfile
import unittest
from pathlib import Path

import machine.main as machine_main
from machine.store import judged_words

QUOTED = '\n\nOn Mon, 2 Mar 2026 at 10:00, Sam Lee <sam@acme.example> wrote:\n> Where is the contract?\n> Sam'


class Judged(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite')
        self.n = 0

    def event(self, kind='gmail.message', title='Contract', body='', **meta):
        self.n += 1
        self.store.commit_page('a', {}, [{'account_id': 'a', 'source_id': f'm{self.n}', 'kind': kind, 'occurred_at': '2026-03-03T09:00:00+00:00',
                                         'title': title, 'body': body, 'metadata': meta, 'deleted': False}])
        with self.store.connect() as db:
            return db.execute('SELECT max(id) FROM events').fetchone()[0]

    def judged(self, *a, **k):
        eid = self.event(*a, **k)
        with self.store.connect() as db:
            return judged_words.judged(db, [eid])[eid]

    def test_an_email_is_its_subject_and_own_words_whole_past_400_characters(self):
        long = 'We looked at every page. ' * 30
        said = self.judged(body=f'Hi Sam,\n\n{long}\n\nThe contract only follows next week.\n-- \nRobin\nLarkspur' + QUOTED)
        self.assertTrue(said.startswith('<<<Contract — Hi Sam, We looked'))
        self.assertTrue(said.endswith('The contract only follows next week.>>>'))
        self.assertNotIn('cut:', said)
        self.assertNotIn('Larkspur', said)

    def test_a_forward_keeps_what_it_forwards(self):
        said = self.judged(title='Fwd: Contract', body='FYI\n\n---------- Forwarded message ---------\nFrom: Sam Lee <sam@acme.example>\nDate: Mon\n\nSigned!')
        self.assertIn('Signed!', said)

    def test_a_longer_one_shows_its_start_and_end_and_says_it_is_cut(self):
        said = judged_words.cut('start ' + 'x' * 5000 + ' end')
        self.assertTrue(said.startswith('start x'))
        self.assertTrue(said.endswith('x end'))
        self.assertIn('[…cut: 3,510 characters left out…]', said)
        self.assertLess(len(said), judged_words.WORDS + 60)
        self.assertEqual(judged_words.cut('y' * judged_words.WORDS), 'y' * judged_words.WORDS)

    def test_a_mails_files_by_name_and_no_files_only_where_that_is_known(self):
        self.assertTrue(self.judged(attachments=[{'name': 'Contract signed.pdf', 'type': 'application/pdf'}]).endswith('>>>, files: <<<Contract signed.pdf>>>'))
        self.assertEqual(judged_words.files('gmail.message', {'attachments': []}), [])
        self.assertIsNone(judged_words.files('gmail.message', {}))  # collected before files were kept

    def test_a_stored_mail_without_files_still_says_so_when_read_back(self):
        self.assertTrue(self.judged(body='Attached!', attachments=[]).endswith(', no files'))

    def test_chats_say_what_was_sent_where_they_keep_it(self):
        self.assertEqual(judged_words.files('whatsapp.message', {'media_type': 'document'}), ['document'])
        self.assertEqual(judged_words.files('whatsapp.message', {'media_type': ''}), [])
        self.assertIsNone(judged_words.files('telegram.message', {'media_type': 'other'}))
        self.assertIsNone(judged_words.files('whatsapp.message', {}))
        self.assertEqual(judged_words.files('teams.message', {}, 'Here\n[file] Plan.docx'), ['Plan.docx'])
        self.assertIsNone(judged_words.files('teams.message', {'truncated': True}, 'Here'))
        for kind in ('slack.message', 'linkedin.message', 'intercom.message'):
            self.assertIsNone(judged_words.files(kind, {}))

    def test_a_slack_message_is_said_once_and_says_nothing_about_files(self):
        said = self.judged('slack.message', '#launch: Here is the plan', 'Here is the plan\nMore below', channel_id='C1', channel_name='launch', user_id='U1')
        self.assertEqual(said, '<<<#launch — Here is the plan More below>>>')

    def test_both_checks_page_the_whole_message_with_its_files(self):
        app = object.__new__(machine_main.App)
        app.store, app.config = self.store, {'accounts': []}
        body = 'Nearly there. ' * 50 + 'It only goes out on Monday.'
        found = [{'id': self.event(body=body, attachments=[{'name': 'Draft.pdf', 'type': 'application/pdf'}]),
                  'at': '2026-03-03T09:00:00+00:00', 'channel': 'gmail', 'where': 'same conversation', 'who': 'the owner'}]
        promise = {'id': 1, 'who': 'Sam Lee', 'what': 'send the signed contract', 'direction': 'mine', 'together': 0,
                   'made_at': '2026-03-02T09:00:00+00:00', 'due': None}
        with self.store.connect() as db:
            for page in (app.handled_check_text(db, [({'id': 's1', 'title': 'Send the contract', 'next_action': None}, found)]),
                         app.promise_check_text(db, [(promise, found)])):
                self.assertIn('It only goes out on Monday.>>>, files: <<<Draft.pdf>>>', page)
                self.assertIn(judged_words.RULE, page)


class Cases(unittest.TestCase):
    def test_the_evals_cases_are_whole(self):
        spec = json.loads((Path(__file__).resolve().parent.parent / 'evals/closing-checks/cases.json').read_text())
        ids = [c['id'] for c in spec['cases']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual({c['want'] for c in spec['cases']}, {'open', 'done'})


if __name__ == '__main__':
    unittest.main()
