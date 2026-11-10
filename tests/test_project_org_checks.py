"""A project's organization comes from what the project is about, not from where its people work (2026-11-10). The
Machine still fills one in from the people (fill_orgs), and a review then keeps or drops it by meaning: a home
internet project with a friend's employer loses it, a trial at that company keeps it. Existing ones are checked the
same way, a batch per review; what the owner set is never asked about; a drop is logged and can be undone."""
import unittest

import project_org_checks as poc
import test_graph as tg
from test_graph import NOW, graph, mail
from machine.prompts.review import review_prompt

T = NOW.isoformat()


class ProjectOrgChecks(unittest.TestCase):
    setUp, add, build = tg.Boards.setUp, tg.Boards.add, tg.Boards.build
    STAGES = tg.Boards.STAGES

    def project(self, name, *mails):
        self.add(*mails)
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute('SELECT id FROM events ORDER BY id DESC LIMIT ?', (len(mails),))]
            graph.label(db, ids, name, 'review', T)
            return db.execute('SELECT id FROM projects WHERE name=?', (name,)).fetchone()[0]

    def row(self, pid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT org,org_by FROM projects WHERE id=?', (pid,)).fetchone())

    def two(self):
        internet = self.project('Home internet', mail(4, 'Pat <pat@bigcorp.example>', 'sam@acme.com', thread='h'))
        trial = self.project('Bigcorp trial', mail(3, 'Pat <pat@bigcorp.example>', 'sam@acme.com', thread='t'))
        self.build()
        self.assertEqual((self.row(internet), self.row(trial)), ({'org': 'bigcorp.example', 'org_by': 'backfill'},) * 2)
        return internet, trial

    def test_a_review_keeps_the_organization_a_project_is_about_and_drops_one_that_is_only_an_employer(self):
        internet, trial = self.two()
        with self.store.connect() as db:
            brief = poc.org_check_brief(db, 'r1')
            self.assertIn(f'- Home internet (project:{internet}): ', brief)
            self.assertIn('Bigcorp (where they work: Pat)', brief)
            with self.assertRaisesRegex(ValueError, f'answer Home internet \\(project:{internet}\\)'):
                poc.org_check_answer(db, 'r1', [{'project': f'project:{trial}', 'org': 'keep'}], T)
            with self.assertRaisesRegex(ValueError, 'keep.*drop'):
                poc.org_check_answer(db, 'r1', [{'project': f'project:{internet}', 'org': 'maybe'}], T)
            self.assertEqual(poc.org_check_answer(db, 'r1', [{'project': f'project:{internet}', 'org': 'drop'},
                                                                {'project': f'project:{trial}', 'org': 'keep'}], T), 1)
        self.assertEqual(self.row(internet), {'org': None, 'org_by': 'review'})
        self.assertEqual(self.row(trial), {'org': 'bigcorp.example', 'org_by': 'review'})
        self.build()  # the Machine doesn't fill it in again
        self.assertEqual(self.row(internet), {'org': None, 'org_by': 'review'})
        with self.store.connect() as db:
            self.assertEqual(poc.org_check_brief(db, 'r2'), '')  # each asked once
            self.assertEqual(poc.undo_org_checks(db), 1)  # logged, so it can be put back
        self.assertEqual(self.row(internet), {'org': 'bigcorp.example', 'org_by': 'backfill'})

    def test_what_the_owner_set_is_never_asked_and_a_change_since_stays(self):
        internet, trial = self.two()
        with self.store.connect() as db:
            graph.save_project(db, {'node_id': f'project:{trial}', 'org': None}, T)
            graph.save_project(db, {'node_id': f'project:{trial}', 'org': 'org:bigcorp.example'}, T)  # the owner's pick
            brief = poc.org_check_brief(db, 'r1')
            self.assertNotIn('Bigcorp trial', brief)
            graph.save_project(db, {'node_id': f'project:{internet}', 'org': 'org:bigcorp.example'}, T)  # set by hand meanwhile
            graph.save_project(db, {'node_id': f'project:{internet}', 'org': None}, T)
            poc.org_check_answer(db, 'r1', [{'project': 'Home internet', 'org': 'keep'}], T)
        self.assertEqual(self.row(internet), {'org': None, 'org_by': 'owner'})
        self.assertEqual(self.row(trial), {'org': 'bigcorp.example', 'org_by': 'owner'})

    def test_one_no_review_answers_is_left_as_it_is_after_a_few_tries(self):
        internet, _ = self.two()
        with self.store.connect() as db:
            for run in ('r1', 'r2', 'r3'):
                self.assertIn('Home internet', poc.org_check_brief(db, run))
            self.assertNotIn('Home internet', poc.org_check_brief(db, 'r4'))
            self.assertEqual(poc.org_check_answer(db, 'r4', None, T), 0)
        self.assertEqual(self.row(internet), {'org': 'bigcorp.example', 'org_by': 'backfill'})

    def test_the_prompt_asks_for_them_only_when_there_are_some(self):
        self.assertNotIn('Project organizations to check', review_prompt('r1', ['work']))
        prompt = review_prompt('r1', ['work'], orgs='- Home internet (project:1): Bigcorp (where they work: Pat (friend))')
        self.assertIn('Project organizations to check', prompt)
        self.assertIn('finish_analysis orgs', prompt)
        self.assertLess(prompt.index('This turn: review run r1') , prompt.index('Project organizations to check'))


if __name__ == '__main__':
    unittest.main()
