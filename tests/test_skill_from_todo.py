"""A to-do that asks for a skill: its run proposes one (skills-propose --job), the card shows what is in it and offers
Create skill (or Update skill), and only the owner's tap installs it. A corrected proposal from the same to-do replaces
the earlier one, the to-do is done once the skill is created, and the summary never ends on a pointer to a stripped path.
All local; nothing is sent."""
from pathlib import Path
import tempfile
import unittest

import skills
from test_voices import a, mail

BODY = '1. Open the payroll site.\n2. Enter the vacation days.\n3. Import, then submit.'


class SkillFromTodo(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = [{'id': 'work', 'service': 'gmail', 'email': 'owner@example.com'}]
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': self.store.accounts}
        self.workspace = Path(self.temp.name) / 'workspace'
        self.app.skills = skills.Skills(self.store.connect, self.workspace)
        self.store.commit_page('work', {}, [mail('in1', '2026-10-01T09:00:00+00:00', 'Make a payroll skill.')])
        self.sid = self.store.suggest('payroll', 'Create a payroll skill', 'Capture the payroll steps.', [1])['id']
        self.start_run('job1')

    def start_run(self, job):
        stamp = '2026-10-30T09:00:00+00:00'
        with self.store.connect() as db:
            db.execute('DELETE FROM preparations WHERE suggestion_id=?', (self.sid,))
            db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,created_at,updated_at) VALUES(?,?,?,'running',?,?)",
                       (self.sid, 'd-' + job, job, stamp, stamp))

    def finish_run(self, body):
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='done' WHERE suggestion_id=?", (self.sid,))
            db.execute("UPDATE suggestions SET status='prepared',body=? WHERE id=?", (body, self.sid))

    def propose(self, name, job='job1', **more):
        return self.app.action('skill_propose', {'name': name, 'description': 'Monthly payroll', 'body': BODY, 'job_id': job, **more})

    def card(self):
        return next(c for c in self.store.snapshot([])['suggestions'] if c['id'] == self.sid)

    def test_the_card_shows_the_proposed_skill_and_nothing_is_installed_before_create_skill(self):
        out = self.propose('Payroll')
        self.finish_run('Your payroll skill is ready for approval. The draft is at memory/assistant/261030-payroll.md.')
        shown = self.card()['proposed_skill']
        self.assertEqual((shown['id'], shown['name'], shown['description'], shown['body']), (out['id'], 'Payroll', 'Monthly payroll', BODY))
        self.assertNotIn('update', shown)
        self.assertEqual([s['status'] for s in self.app.skills.view()['skills']], ['proposed'])
        self.assertFalse((self.workspace / 'skills' / skills.FOLDER / 'payroll').exists())
        # Create skill: the owner's own Approve installs it and finishes the to-do
        self.app.action('skill_decide', {'id': out['id'], 'choice': 'approve'}, owner_dashboard=True)
        self.assertEqual([(s['name'], s['status']) for s in self.app.skills.view()['skills']], [('Payroll', 'on')])
        card = self.card()
        self.assertEqual(card['status'], 'completed')
        self.assertNotIn('proposed_skill', card)

    def test_a_corrected_proposal_from_the_same_todo_replaces_the_earlier_one(self):
        first = self.propose('Sales rep payroll')
        self.start_run('job2')
        second = self.propose('Company payroll', job='job2')
        self.finish_run('Corrected.')
        self.assertEqual([s['name'] for s in self.app.skills.view()['skills']], ['Company payroll'])
        self.assertEqual(self.card()['proposed_skill']['id'], second['id'])
        with self.assertRaisesRegex(ValueError, 'gone'):
            self.app.action('skill_decide', {'id': first['id'], 'choice': 'approve'}, owner_dashboard=True)

    def test_a_proposal_names_its_todo_only_from_that_todos_running_preparation(self):
        with self.assertRaisesRegex(ValueError, 'running preparation'):
            self.propose('Payroll', job='not-a-run')
        with self.assertRaisesRegex(ValueError, 'job_id'):
            self.propose('Payroll', job='bad job!')
        # Without a job it is the plain proposal it always was: Settings, Skills, no to-do
        out = self.app.action('skill_propose', {'name': 'Payroll', 'description': 'Monthly payroll', 'body': BODY})
        self.finish_run('Done.')
        self.assertTrue(out['id'])
        self.assertNotIn('proposed_skill', self.card())

    def test_an_update_from_a_todo_shows_the_before_and_after(self):
        mine = self.app.skills.save('', 'Payroll', 'Monthly payroll', '1. Open the payroll site.\n2. Submit it.')
        mine = next(s for s in mine['skills'] if s['name'] == 'Payroll')
        asked = self.propose('', update='Payroll', description='')
        out = self.propose('', update='Payroll', description='', base=asked['base'])
        self.finish_run('Updated.')
        shown = self.card()['proposed_skill']
        self.assertEqual(shown['update']['before'], '1. Open the payroll site.\n2. Submit it.')
        self.assertEqual(shown['update']['after'], BODY)
        self.app.action('skill_decide', {'id': out['id'], 'choice': 'approve', 'reviewed': shown['update']['review']}, owner_dashboard=True)
        self.assertEqual([(s['id'], s['status']) for s in self.app.skills.view()['skills']], [(mine['id'], 'on')])
        self.assertEqual(self.card()['status'], 'completed')

    def test_a_sentence_that_only_pointed_at_a_stripped_path_goes_too(self):
        self.assertEqual(a.strip_result_links('Proposed for approval, replacing the earlier version. The draft is at memory/assistant/x.md.'),
                         'Proposed for approval, replacing the earlier version.')
        self.assertEqual(a.strip_result_links('Saved [the notes](memory/assistant/x.md) for you.\nNext line.'), 'Saved for you.\nNext line.')


if __name__ == '__main__':
    unittest.main()
