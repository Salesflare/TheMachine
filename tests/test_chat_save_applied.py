"""What a run's save in a to-do's chat actually changed. The reply said a to-do was snoozed, its due date moved or it
was done when the save hadn't done that (a due date the save never reads, a snooze_until without outcome:'snoozed', a
result that stays open). The saved result now lists applied and not_applied, and the instructions say to report only
that, like title_note for a rename (tests/test_chat_rename.py). Synthetic data only."""
import datetime as dt
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

import machine.main as machine_main
from machine.app import card_actions

ROOT = Path(__file__).parent.parent
TITLE = 'Send Sam the bounty receipt'


def mail(n, body, day=21):
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': f'2026-10-{day}T09:00:00+00:00',
            'title': 'Bounty', 'body': body, 'deleted': False,
            'metadata': {'from': 'Sam <sam@example.com>', 'to': 'owner@example.com', 'thread_id': 't1', 'labels': ['INBOX']}}


class ChatSaveApplied(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'work', 'service': 'gmail', 'transport': 'gog', 'email': 'owner@example.com', 'boundary': 'work:Example'}]}
        self.store.commit_page('work', {}, [mail(1, 'Thanks, it arrived. Could you send me a receipt?')])
        self.sid = self.store.suggest('bounty', TITLE, 'Sam asks for a receipt. I can send it.', [1])['id']

    def status(self):
        with self.store.connect() as db:
            return db.execute('SELECT status FROM suggestions WHERE id=?', (self.sid,)).fetchone()[0]

    def turn(self, text, key):
        self.store.decide(self.sid, 'other', text, key, 'dashboard')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running'")
            return db.execute('SELECT job_id FROM preparations').fetchone()[0]

    def save(self, job, **extra):
        return self.app.action('prepare', {'suggestion_id': self.sid, 'job_id': job, 'body': 'The receipt is still to send.',
                                           'outcome': 'needs_you', 'needs': 'send the receipt', 'note_kind': 'continue', **extra})

    def test_a_due_date_the_save_never_reads_says_it_did_not_change(self):
        saved = self.save(self.turn('Move the due date to Friday', 'chat-1'), due='2026-10-30', deadline='2026-10-30')
        self.assertEqual(saved['applied'], ['result saved; the to-do stays open'])
        self.assertEqual(saved['not_applied'], ['the due date did not change'])
        self.assertEqual(self.status(), 'prepared')

    def test_a_snooze_says_when_in_their_time(self):
        zone = ZoneInfo('Europe/Brussels')
        until = (dt.datetime.now(zone) + dt.timedelta(days=7)).replace(hour=9, minute=0, second=0, microsecond=0)
        with patch.object(card_actions, 'local_tz', return_value=zone):
            saved = self.save(self.turn('Remind me about this next week', 'chat-1'), outcome='snoozed', needs=None,
                              snooze_until=until.isoformat())
        self.assertEqual(self.status(), 'snoozed')
        self.assertEqual(saved['applied'], [f'snoozed until {until:%a %Y-%m-%d} 09:00 (their time)'])
        self.assertNotIn('not_applied', saved)

    def test_a_snooze_time_without_the_snoozed_outcome_is_not_a_snooze(self):
        saved = self.save(self.turn('Remind me about this next week', 'chat-1'), snooze_until='2030-10-25T09:00')
        self.assertEqual(self.status(), 'prepared')
        self.assertEqual(saved['applied'], ['result saved; the to-do stays open'])
        self.assertEqual(saved['not_applied'], ["not snoozed: snooze_until counts only with outcome:'snoozed'"])

    def test_a_finish_that_is_not_verified_keeps_it_open_and_says_so(self):
        self.assertEqual(card_actions.what_applied({'status': 'prepared'}, {'finish_state': 'uncertain'}),
                         {'applied': ['result saved; the to-do stays open'], 'not_applied': ['the final step is not done (uncertain)']})
        self.assertEqual(card_actions.what_applied({'status': 'completed'}, {'finish_state': 'completed'}),
                         {'applied': ['the to-do is done and left their list']})

    def test_sends_steps_and_docs_say_what_happened(self):
        self.assertEqual(card_actions.what_applied({'status': 'prepared', 'send': {'status': 'queued'}, 'done_now': {'status': 'cancelled'},
                                                    'doc_created': 'waits for the owner'}, {}),
                         {'applied': ['result saved; the to-do stays open', 'the draft is queued to send'],
                          'not_applied': ['the step did not run', 'the new doc waits for the owner']})
        self.assertEqual(card_actions.what_applied({'status': 'prepared', 'doc_created': 'being made now in the owner’s own Drive'}, {})['applied'][-1],
                         'the new doc being made now in the owner’s own Drive')

    def test_the_instructions_say_it(self):
        text = (ROOT / 'machine/app/preparation.py').read_text()
        self.assertIn("Tell the owner only the changes the saved result's applied lists", text)
        self.assertIn('Each not_applied line is something that did not change', text)


if __name__ == '__main__':
    unittest.main()
