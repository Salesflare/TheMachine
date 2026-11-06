"""scripts/move_code.py moves functions, classes, constants and class members with their text unchanged."""
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import move_code  # noqa: E402

SOURCE = '''"""The module."""
import os
from pathlib import Path

LIMIT = 3


# Why it's a helper
@staticmethod
def helper(x):
    return x + LIMIT


TABLE = {
    'a': 1,
}


class App:
    """The app."""
    SIZE = 2

    # A method
    def run(self):
        return helper(self.SIZE)

    def stop(self):
        return os.getpid()


def main():
    return App().run()
'''


class MoveCode(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        (self.root / 'src.py').write_text(SOURCE, encoding='utf-8')
        (self.root / 'pkg').mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def read(self, name):
        return (self.root / name).read_text(encoding='utf-8')

    def test_top_level_names_move_as_they_are(self):
        (self.root / 'pkg' / 'helpers.py').write_text('"""Helpers."""\n', encoding='utf-8')
        move_code.move('src.py', 'pkg/helpers.py', ['helper', 'TABLE'], root=self.root)
        self.assertEqual(self.read('pkg/helpers.py'), '"""Helpers."""\n\n\n# Why it\'s a helper\n@staticmethod\n'
                                                       'def helper(x):\n    return x + LIMIT\n\n\nTABLE = {\n    \'a\': 1,\n}\n')
        left = self.read('src.py')
        self.assertNotIn('helper(x)', left)
        self.assertNotIn('TABLE', left)
        self.assertIn('LIMIT = 3\n\n\nclass App:', left)  # the gap is closed with the spacing it had

    def test_members_go_to_the_end_of_the_target_class(self):
        (self.root / 'mixin.py').write_text('class Mixin:\n    """Its part."""\n', encoding='utf-8')
        move_code.move('src.py', 'mixin.py:Mixin', ['App.run', 'App.SIZE'], root=self.root)
        self.assertEqual(self.read('mixin.py'), 'class Mixin:\n    """Its part."""\n\n    # A method\n    def run(self):\n'
                                                '        return helper(self.SIZE)\n\n    SIZE = 2\n')
        self.assertIn('    """The app."""\n\n    def stop(self):', self.read('src.py'))

    def test_export_keeps_the_names_in_the_source(self):
        (self.root / 'pkg' / '__init__.py').write_text('', encoding='utf-8')
        (self.root / 'pkg' / 'text.py').write_text('', encoding='utf-8')
        move_code.move('src.py', 'pkg/text.py', ['main'], export=True, root=self.root)
        move_code.move('src.py', 'pkg/text.py', ['helper'], export=True, root=self.root)
        self.assertIn('from pathlib import Path\nfrom pkg.text import (\n    helper,\n    main,\n)\n', self.read('src.py'))
        self.assertTrue(self.read('pkg/text.py').startswith('def main():'))

    def test_it_refuses_what_it_cannot_move_as_is(self):
        (self.root / 'pkg' / 'x.py').write_text('', encoding='utf-8')
        for target, items, said in [('pkg/x.py', ['nothing'], 'has no nothing'), ('pkg/x.py', ['App.run'], 'class members'),
                                    ('pkg/missing.py', ['main'], 'does not exist'), ('pkg/x.py:X', ['main'], 'class members')]:
            with self.subTest(items=items), self.assertRaises(SystemExit) as raised:
                move_code.move('src.py', target, items, root=self.root)
            self.assertIn(said, str(raised.exception))
        self.assertEqual(self.read('src.py'), SOURCE)  # nothing half done


if __name__ == '__main__':
    unittest.main()
