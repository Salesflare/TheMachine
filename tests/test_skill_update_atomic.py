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

    def test_sync_cannot_put_back_instructions_older_than_an_owner_edit(self):
        original = 'Read the source and check the facts before drafting.'
        latest = 'Use my corrected procedure and keep the verified receipt.'
        skill = self.mine('Source checks', 'When the source needs checking', original)
        done, errors = threading.Event(), []
        real_render = skills.render
        def edit():
            try:
                self.keeper.save(skill['id'], skill['name'], skill['description'], latest)
            except Exception as error:
                errors.append(error)
            finally:
                done.set()
        writer = threading.Thread(target=edit)
        def during_render(row):
            if writer.ident is None:
                writer.start()
                done.wait(.25)  # old sync could publish its snapshot after the newer edit and its sync finished
            return real_render(row)
        with patch.object(skills, 'render', side_effect=during_render):
            try:
                self.keeper.sync()
            finally:
                writer.join(5)
        self.assertFalse(writer.is_alive())
        self.assertEqual(errors, [])
        self.assertEqual(self.keeper.get(skill['id'])['body'], latest)
        text = (self.root / 'source-checks' / 'SKILL.md').read_text()
        self.assertIn(latest, text)
        self.assertNotIn(original, text)

if __name__ == '__main__':
    unittest.main()
