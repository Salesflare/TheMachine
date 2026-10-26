"""Voice and style learn only from what the owner wrote themselves (authorship.py): a draft sent from a to-do comes back
in their Sent mail or chat with their name on it, but The Machine wrote it. The profile, the voice study, the examples a
draft matches and the "answered it themselves" lessons skip it; a draft the owner changed teaches through that change,
and an agent's own rewrite of a draft teaches nothing. All local; nothing is sent."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('authorship_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import authorship

OWNER = 'Owner <owner@example.com>'
DRAFTED = 'Dear Sam,\n\nPlease find the signed contract attached. Let me know if anything is unclear.\n\nKind regards'


def mail(source_id, at, body, thread='t1', labels=('SENT',), message_id=''):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': 'Re: Contract',
            'body': body, 'deleted': False, 'metadata': {'from': OWNER, 'to': 'Sam <sam@example.com>', 'thread_id': thread,
                                                         'labels': list(labels), 'message-id': message_id}}


def chat(source_id, at, body, mine=True, chat_id='c1'):
    return {'account_id': 'phone', 'source_id': source_id, 'kind': 'whatsapp.message', 'occurred_at': at, 'title': 'Kim',
            'body': body, 'deleted': False, 'metadata': {'chat_id': chat_id, 'from_me': mine, 'chat_name': 'Kim', 'message_id': source_id}}


class Authorship(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = [{'id': 'work', 'service': 'gmail', 'email': 'owner@example.com'}, {'id': 'phone', 'service': 'whatsapp'}]
        self.store.commit_page('work', {}, [
            mail('in1', '2026-10-01T09:00:00+00:00', 'Can you send the contract?', labels=('INBOX',)),
            mail('own1', '2026-10-01T10:00:00+00:00', 'hey sam, here it is. cheers'),
            # Sent from a to-do: its Message-ID is the one the send set
            mail('sent1', '2026-10-01T11:00:00+00:00', DRAFTED + '\n\nOwner', message_id='<card-1@example.com>'),
            # Sent from a to-do, the id never came back: known by its text, signature and quoted history after it
            mail('sent2', '2026-10-01T12:00:00+00:00', 'Dear Lee,\n\nThank you for the quick turnaround on the invoice.\n\nOwner\n\n[Quoted earlier messages]\nold', thread='t2'),
        ])
        self.store.commit_page('phone', {}, [
            chat('w1', '2026-10-01T08:00:00+00:00', 'ja tuurlijk, tot straks'),
            chat('w2', '2026-10-01T08:30:00+00:00', 'Great, I will be there at eight o clock sharp.'),
            chat('w3', '2026-10-01T08:40:00+00:00', 'ok top'),  # short: theirs, even though a to-do once sent "ok top" too
        ])
        self.sid = self.store.suggest('contract', 'Send Sam the contract', 'Sam asked for it.', [1])['id']
        jobs = [('j1', {'kind': 'email', 'account_id': 'work', 'body': DRAFTED}, '<card-1@example.com>', 'gmail-sent1'),
                ('j2', {'kind': 'email', 'account_id': 'work', 'body': 'Dear Lee,\n\nThank you for the quick turnaround on the invoice.'}, '<card-2@example.com>', None),
                ('j3', {'kind': 'whatsapp', 'account_id': 'phone', 'chat_id': 'c1', 'body': 'Great, I will be there at eight o clock sharp.'}, '', 'whatsapp:w2'),
                ('j4', {'kind': 'whatsapp', 'account_id': 'phone', 'chat_id': 'c1', 'body': 'ok top'}, '', None),
                ('j5', {'kind': 'merge', 'head': 'abc'}, '', 'merge:abc')]
        with self.store.connect() as db:
            for n, (job_id, payload, rfc, message_id) in enumerate(jobs):
                db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id,message_id) "
                           "VALUES(?,?,?,?,'sent',?,?,'x','dashboard',?,?)", (job_id, self.sid, f'r{n}', json.dumps(payload), a.now(), a.now(), rfc, message_id))

    def test_sent_messages_are_told_apart_by_id_and_by_text(self):
        with self.store.connect() as db:
            sent = authorship.MachineSent.load(db)
            rows = {r['source_id']: r for r in db.execute('SELECT * FROM events')}
        self.assertTrue(sent.wrote(rows['sent1']))   # by its Message-ID
        self.assertTrue(sent.wrote(rows['sent2']))   # by its text, with the signature after it
        self.assertTrue(sent.wrote(rows['w2']))      # by the chat's message id
        self.assertFalse(sent.wrote(rows['own1']))
        self.assertFalse(sent.wrote(rows['w1']))
        self.assertFalse(sent.wrote(rows['w3']))     # too short to tell apart by text
        self.assertFalse(authorship.MachineSent().wrote(rows['sent1']))

    def test_the_profile_and_the_voice_study_read_only_the_owners_own_writing(self):
        texts = ' | '.join(m['text'] for m in self.store.own_messages())
        self.assertIn('hey sam, here it is', texts)
        self.assertIn('ja tuurlijk', texts)
        self.assertNotIn('Please find the signed contract', texts)
        self.assertNotIn('quick turnaround', texts)
        self.assertNotIn('eight o clock', texts)
        study = ' | '.join(m['text'] for m in self.store.voice_sample()['messages'])
        self.assertNotIn('Please find the signed contract', study)
        self.assertNotIn('eight o clock', study)

    def test_a_draft_matches_the_owners_own_examples_not_earlier_drafts(self):
        examples = ' | '.join(e['text'] for e in self.store.own_examples(self.sid))
        self.assertIn('hey sam, here it is', examples)
        self.assertNotIn('Please find the signed contract', examples)

    def test_another_to_dos_send_is_not_an_answer_the_owner_wrote_themselves(self):
        other = self.store.suggest('contract-2', 'Answer Sam', 'Sam asks again.', [1])['id']
        draft = {'kind': 'email', 'label': 'Send', 'account_id': 'work', 'to': ['sam@example.com'], 'subject': 'Re: Contract',
                 'body': 'Hi Sam, a short answer from the draft.', 'revision': 'q1', 'thread_id': 't1'}
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(draft), other))
            db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,created_at,updated_at) VALUES(?,'d','jp','done',?,?)",
                       (other, '2026-10-01T10:30:00+00:00', '2026-10-01T10:30:00+00:00'))
        with patch.object(a, 'now', return_value='2026-10-01T13:00:00+00:00'):
            self.assertEqual(self.store.learn_sent_elsewhere(), 0)  # the next message in t1 is the first to-do's send
        self.store.commit_page('work', {}, [mail('own2', '2026-10-01T12:30:00+00:00', 'sam, quick one: all fine. cheers')])
        with patch.object(a, 'now', return_value='2026-10-01T13:00:00+00:00'):
            self.assertEqual(self.store.learn_sent_elsewhere(), 1)  # their own reply teaches
        with self.store.connect() as db:
            self.assertIn('all fine', db.execute("SELECT after_body FROM draft_edits WHERE source='elsewhere'").fetchone()[0])

    def test_an_owner_edit_teaches_what_they_changed_and_an_agent_rewrite_teaches_nothing(self):
        with self.store.connect() as db:
            for edit_id, source, after in (('e1', 'dashboard', 'Hey Sam, contract attached. Cheers'), ('e2', 'agent', 'Dear Sam, as requested, the contract.')):
                db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_body,after_body,source,created_at) "
                           "VALUES(?,?,'a','b','email',?,?,?,?)", (edit_id, self.sid, DRAFTED, after, source, a.now()))
        lines = self.store.edits_to_learn('run1')
        self.assertIn('Hey Sam, contract attached', lines)
        self.assertIn('They changed it to', lines)
        self.assertNotIn('as requested', lines)


if __name__ == '__main__':
    unittest.main()
