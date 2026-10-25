"""A skill update and its review are one write; a later owner edit must survive."""
import threading
import unittest
from unittest.mock import patch
import test_skills as fixtures

skills = fixtures.skills

class SkillUpdateAtomic(unittest.TestCase):
    setUp = fixtures.Skills.setUp
    mine = fixtures.Skills.mine

    def test_an_owner_edit_during_approval_is_not_overwritten(self):
        original = '## Steps\n1. Read the source.\n2. Check the facts.'
        proposed = original + '\n3. Keep the receipt.'
        latest = original + '\n3. Use my corrected procedure instead.'
        skill = self.mine('Source checks', 'When the source needs checking', original)
        base = self.keeper.propose('', '', fixtures.BODY, update=skill['name'])['base']
        proposal = self.keeper.propose('', '', proposed, update=skill['name'], base=base)
        shown = next(s for s in self.keeper.view()['skills'] if s['id'] == proposal['id'])['update']
        done, errors = threading.Event(), []
        real_view = skills.update_view
        def edit():
            try:
                self.keeper.save(skill['id'], skill['name'], skill['description'], latest)
            except Exception as error:
                errors.append(error)
            finally:
                done.set()
        writer = threading.Thread(target=edit)
        def during_review(*args):
            if writer.ident is None:
                writer.start()
                done.wait(.25)  # before the fix this write finishes between the read and the update
            return real_view(*args)
        with patch.object(self.keeper, 'sync'), patch.object(skills, 'update_view', side_effect=during_review):
            try:
                self.keeper.decide(proposal['id'], 'approve', shown['review'])
            finally:
                writer.join(5)
        self.assertFalse(writer.is_alive())
        self.assertEqual(errors, [])
        self.assertEqual(self.keeper.get(skill['id'])['body'], latest)

if __name__ == '__main__':
    unittest.main()
