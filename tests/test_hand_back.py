"""A step a run wrote is never lost on the way: the save after one that was refused, or held until Slack was read, gets it
back when it comes without it, once (machine/hand_back.py). No live calls."""
import json
import tempfile
import unittest
from pathlib import Path

import machine.main as machine_main
import next_actions
from machine import hand_back
from test_honest_status import GMAIL, SLACK, email

DRAFT = {'kind': 'email', 'label': 'Send reply', 'account_id': 'work', 'to': ['customer@client.example'], 'subject': 'Re: Documents',
         'body': 'Hi,\n\nOur VAT number is BE 0712.555.019.\n\nCheers,\n\nAlex', 'in_reply_to': '<m1@x>'}
FINISH = {'kind': 'finish', 'label': 'Pay the invoice', 'instructions': 'Pay it'}
LINK = {'kind': 'open', 'label': 'Open the document', 'url': 'https://docs.example/d/1'}
LOST = 'This save lost the email step “Send reply” that an earlier save of this run had'
BAD = {**DRAFT, 'label': 'x' * 200}
ENDS = ({'outcome': 'done'}, {'outcome': 'answered'}, {'outcome': 'needs_you', 'needs': 'confirm the retention period'},
        {'outcome': 'needs_you', 'needs': 'How long do you keep files?'})


class HandBack(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = machine_main.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [email('m1', '2026-10-15T08:00:00+00:00')])
        with self.store.connect() as db:
            event = db.execute('SELECT id FROM events').fetchone()[0]
        self.sid = self.store.suggest('documents', 'Send the documents Client asks for', 'They ask for documents.', [event])['id']
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [GMAIL, SLACK]}
        self.store.decide(self.sid, 'accept', '', 'd1', 'dashboard')
        with self.store.connect() as db:
            self.job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (self.sid,)).fetchone()[0]
        self.fresh()
        self.held = []  # what the conversation check says to the next saves with a step, in order
        self.app.handled_gate = lambda sid, job, actions, wait=0: self.held.pop(0) if self.held and actions else None

    def fresh(self):
        """The run is on its way, nothing saved yet."""
        self.app._unsaved_steps = {}
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running' WHERE suggestion_id=?", (self.sid,))
            db.execute("UPDATE suggestions SET status='accepted' WHERE id=?", (self.sid,))

    def save(self, *actions, **more):
        return self.app.action('prepare', {'suggestion_id': self.sid, 'job_id': self.job, 'body': 'Looked into the documents.',
                                           'next_actions': list(actions), 'outcome': 'needs_you', 'needs': 'check the draft and send it', **more})

    def stored(self):
        with self.store.connect() as db:
            row = db.execute('SELECT status,outcome,next_action FROM suggestions WHERE id=?', (self.sid,)).fetchone()
        return row['status'], json.loads(row['outcome'] or '{}').get('state'), [a['kind'] for a in next_actions.actions(json.loads(row['next_action'] or 'null'))]

    def hold(self, **more):
        self.held = ['Before this goes to the owner: Slack reads']
        with self.assertRaisesRegex(ValueError, 'Slack reads'):
            self.save(DRAFT, **more)

    def test_a_held_step_comes_back_whole_and_saves(self):
        self.hold()
        with self.assertRaisesRegex(ValueError, LOST) as caught:
            self.save(outcome='done')
        self.assertNotEqual(self.stored()[0], 'prepared')  # nothing was saved
        given = json.loads(str(caught.exception).split('next_actions:', 1)[1].split(' and save: as it was')[0])
        self.assertEqual(given, [DRAFT])  # as it was, whatever the run still remembers
        self.save(*given)
        self.assertEqual(self.stored(), ('prepared', 'needs_you', ['email']))
        self.assertEqual(self.app._unsaved_steps, {})

    def test_whatever_the_run_ends_with(self):
        for end in ENDS:
            for link in ((), (LINK,)):  # a link is not the step
                with self.subTest(end, link=bool(link)):
                    self.fresh()
                    self.hold()
                    with self.assertRaisesRegex(ValueError, LOST):
                        self.save(*link, **end)

    def test_a_refused_step_comes_back_to_be_corrected(self):
        with self.assertRaisesRegex(ValueError, 'label'):
            self.save(BAD)
        with self.assertRaisesRegex(ValueError, 'corrected when it was refused'):
            self.save(outcome='answered')
        self.save(DRAFT)
        self.assertEqual(self.stored(), ('prepared', 'needs_you', ['email']))

    def test_rightly_finished_it_goes_through_at_the_next_save(self):
        # A transfer the owner makes themselves, a post that did go out: the step is rightly gone
        for first, end in ((FINISH, {'outcome': 'needs_you', 'needs': 'make the transfer in your bank'}), (BAD, {'outcome': 'done'})):
            with self.subTest(end):
                self.fresh()
                hand_back.keep(self.app._unsaved_steps, self.job, {'next_actions': [first]}, next_actions.WAITING_KINDS)
                with self.assertRaisesRegex(ValueError, 'Only if the to-do is rightly finished without it, save this again as it is'):
                    self.save(**end)
                self.save(**end)
                self.assertEqual(self.stored(), ('prepared', end['outcome'], []))

    def test_said_once_also_when_a_later_save_is_refused(self):
        self.hold()
        with self.assertRaisesRegex(ValueError, LOST):
            self.save(outcome='done')
        with self.assertRaises(ValueError):
            self.save(BAD)
        self.save(outcome='done')
        self.assertEqual(self.stored(), ('prepared', 'done', []))

    def test_a_run_that_lost_nothing_is_never_stopped(self):
        for end in (*ENDS, {'outcome': 'already_done', 'needs': None}, {'outcome': 'waiting', 'needs': None, 'waiting_on': 'Client signing'}):
            with self.subTest(end):
                self.fresh()
                self.save(**end)
                self.assertEqual(self.stored()[0], 'prepared')

    def test_the_conversation_showed_it_done(self):
        for end in ({'outcome': 'already_done', 'needs': None}, {'outcome': 'waiting', 'needs': None, 'waiting_on': 'Client signing'}):
            with self.subTest(end):
                self.fresh()
                self.hold()
                self.save(**end)
                self.assertEqual(self.stored()[0], 'prepared')

    def test_only_waiting_steps_are_kept_and_the_memory_stays_small(self):
        memory, waiting = {}, next_actions.WAITING_KINDS
        hand_back.keep(memory, 'j1', {'next_actions': [LINK, 'x']}, waiting)
        hand_back.keep(memory, None, {'next_actions': [DRAFT]}, waiting)
        self.assertEqual(memory, {})
        hand_back.keep(memory, 'j1', {'next_action': {**DRAFT, 'body': 'x' * 9000}}, waiting)
        self.assertNotIn('next_actions:', hand_back.lost(memory, 'j1', 'done', [], waiting))  # too long to give back: named only
        for n in range(hand_back.KEPT + 50):
            hand_back.keep(memory, f'x{n}', {'next_actions': [DRAFT]}, waiting)
        self.assertEqual(len(memory), hand_back.KEPT)


if __name__ == '__main__':
    unittest.main()
