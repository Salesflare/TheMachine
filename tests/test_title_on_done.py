"""A to-do's title says what needs doing. It changes while the to-do is open when that changes (a new ask, a new next
step), never because the to-do got finished: a result that only finishes it (done, done already, its final step or an
approved send went through), a review update on a done or dismissed to-do, the review filling in an owner's to-do that
is already done, and marking it done all leave the title as it was. How it ended goes in the line under the title in
Done (what went out, or "Done: <the sign it was handled>"), so Done still shows what each to-do was (2026-10-29)."""
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import dashboard_parts

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('title_on_done_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

TITLE = 'Send Sam the bounty receipt'


def mail(n, body, sender='Sam <sam@example.com>', day=21):
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': f'2026-10-{day}T09:00:00+00:00',
            'title': 'Bounty', 'body': body, 'deleted': False,
            'metadata': {'from': sender, 'to': 'owner@example.com', 'thread_id': 't1', 'labels': ['INBOX']}}


class TitleOnDone(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'work', 'service': 'gmail', 'transport': 'gog', 'email': 'owner@example.com', 'boundary': 'work:Example'}]}
        self.store.commit_page('work', {}, [mail(1, 'Thanks, it arrived. Could you send me a receipt?')])
        self.sid = self.store.suggest('bounty', TITLE, 'Sam asks for a receipt. I can send it.', [1])['id']

    def card(self, sid=None):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid or self.sid,)).fetchone())

    def job(self):
        self.store.decide(self.sid, 'accept', '', 'n1', 'dashboard')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running'")
            return db.execute('SELECT job_id FROM preparations').fetchone()[0]

    def prepare(self, **extra):
        return self.app.action('prepare', {'suggestion_id': self.sid, 'job_id': self.job(), 'body': 'Sent Sam the receipt.', **extra})

    def close(self, choice='complete'):
        self.store.decide(self.sid, choice, '', 'close-1', 'dashboard')

    # A result that only finishes it

    def test_a_done_result_keeps_the_title(self):
        self.prepare(outcome='done', title='Receipt sent to Sam')
        card = self.card()
        self.assertEqual(card['title'], TITLE)
        self.assertEqual(json.loads(card['outcome'])['state'], 'done')  # the status line says it, not the title
        self.assertEqual(card['body'], 'Sent Sam the receipt.')

    def test_a_done_already_result_keeps_the_title(self):
        self.prepare(outcome='already_done', title='Confirm the receipt is done', body='Sam has it: their reply on Tuesday says so.')
        self.assertEqual(self.card()['title'], TITLE)
        self.assertEqual(json.loads(self.card()['outcome'])['state'], 'already_done')

    def test_a_result_that_still_needs_them_can_retitle_an_open_to_do(self):
        # The needed action changed (a new next step): that is what a new title is for.
        self.prepare(outcome='needs_you', needs='pick the amount', title='Pick the receipt amount for Sam')
        self.assertEqual(self.card()['title'], 'Pick the receipt amount for Sam')

    def test_a_completed_final_step_or_an_approved_send_keeps_the_title(self):
        for kwargs in ({'finish_state': 'completed'}, {'send_now': True}):
            self.assertTrue(a.title_kept(**kwargs))
            with self.subTest(**kwargs):
                with self.store.connect() as db:
                    db.execute("UPDATE suggestions SET status='accepted',title=? WHERE id=?", (TITLE, self.sid))
                self.store.prepare(self.sid, 'Done.', title='Receipt sent to Sam', **kwargs)
                self.assertEqual(self.card()['title'], TITLE)
        self.assertFalse(a.title_kept({'state': 'needs_you', 'needs': 'x'}))

    # Updates on a done or dismissed to-do

    def test_a_review_update_on_a_done_to_do_keeps_its_title(self):
        self.close()
        self.store.commit_page('work', {}, [mail(2, 'Got the receipt, thanks!', day=22)])
        saved = self.store.suggest('bounty-done', 'Confirm the receipt is done', 'Sam got the receipt.', [2], card_id=self.sid, match=True)
        self.assertTrue(saved['attached'])
        card = self.card()
        self.assertEqual((card['title'], card['status']), (TITLE, 'completed'))

    def test_a_reopen_without_anything_new_keeps_the_title(self):
        self.close('reject')
        saved = self.store.suggest('bounty-old', 'Confirm the receipt is done', 'Sam asked for it.', [1], card_id=self.sid, match=True, reopen=True)
        self.assertEqual(self.card()['title'], TITLE)
        self.assertEqual(saved['status'], 'rejected')

    def test_a_new_ask_that_reopens_it_may_retitle_it(self):
        self.close()
        with self.store.connect() as db:  # closed before the new ask came in
            db.execute("UPDATE decisions SET created_at='2026-10-21T10:00:00+00:00' WHERE id='close-1'")
        self.store.commit_page('work', {}, [mail(3, 'Could you also send the invoice?', day=23)])
        saved = self.store.suggest('bounty-invoice', 'Send Sam the bounty invoice', 'Sam now asks for the invoice too.', [2],
                                   card_id=self.sid, match=True, reopen=True)
        self.assertTrue(saved.get('reopened'))
        self.assertEqual(self.card()['title'], 'Send Sam the bounty invoice')

    def test_the_review_filling_in_a_done_owner_to_do_keeps_its_title(self):
        made = self.app.action('card_new', {'text': 'Pay Sam'}, owner_dashboard=True)
        self.store.decide(made['id'], 'complete', '', 'own-done', 'dashboard')
        before = self.card(made['id'])['title']
        filled = self.app.action('suggest', {'dedupe_key': 'own', 'title': 'Sam is paid', 'body': 'Paid Sam on Tuesday.',
                                             'event_ids': [made['event_id']]})
        self.assertTrue(filled['owner_card'])
        card = self.card(made['id'])
        self.assertEqual((card['title'], card['status']), (before, 'completed'))
        self.assertEqual(card['body'], 'Paid Sam on Tuesday.')

    def test_looks_done_then_marked_done_keeps_the_title_and_the_reason(self):
        self.store.commit_page('work', {}, [mail(4, 'Got it, thanks.', day=22)])
        self.store.looks_handled(self.sid, 'Sam confirmed it arrived', [2])
        self.close()
        card = self.card()
        self.assertEqual(card['title'], TITLE)
        self.assertEqual(json.loads(card['handled_hint'])['reason'], 'Sam confirmed it arrived')  # Done shows it under the title

    def test_the_instructions_say_it(self):
        self.assertIn('A title says what needs doing, never how it ended', (ROOT / 'AGENTS.md').read_text())
        self.assertIn('never to say it is done, sent or handled', (ROOT / 'assistant.py').read_text())


@unittest.skipUnless(shutil.which('node'), 'needs node')
class DoneLine(unittest.TestCase):
    """The line under a done to-do's title: the sign that it was handled. What went out has its own line already."""
    def line(self, card):
        html = dashboard_parts.assemble(ROOT)
        start = html.index('const doneLine=')
        code = (html[start:html.index('\n', html.index("return why?", start))]
                + "\nconst t=(s,...x)=>x.reduce((o,v)=>o.replace('{}',v),s),esc=s=>s;"
                + f'\nconsole.log(JSON.stringify(doneLine({json.dumps(card)})))')
        return json.loads(subprocess.run(['node', '-e', code], capture_output=True, text=True, check=True).stdout)

    def test_handled(self):
        out = self.line({'status': 'completed', 'handled_hint': json.dumps({'reason': 'Sam confirmed it arrived'})})
        self.assertIn('Done: Sam confirmed it arrived', out)
        self.assertIn('done-line', out)

    def test_nothing_to_say_or_dismissed(self):
        self.assertEqual(self.line({'status': 'completed'}), '')
        self.assertEqual(self.line({'status': 'rejected', 'handled_hint': json.dumps({'reason': 'x'})}), '')

if __name__ == '__main__':
    unittest.main()
