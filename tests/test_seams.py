"""tests/seams.py: a patch reaches every module of the app that binds the name, and every patch of a name on an
assistant module goes through it, so no test quietly runs on the real clock, credentials or sends once code moves."""
import ast
import sys
import types
import unittest
from pathlib import Path
from unittest import mock

from seams import ROOT, patch_everywhere, replace_everywhere


def real_now():
    return 'real'


class Seams(unittest.TestCase):
    def setUp(self):
        # an owner module, the assistant module that imported its name, and code that moved elsewhere and did too
        self.modules = {}
        for name, path in (('owner_mod', 'timeutil_x.py'), ('assistant_copy', 'assistant.py'), ('machine.moved', 'machine/moved.py')):
            module = types.ModuleType(name)
            module.__file__ = str(ROOT / path)
            module.now = real_now
            exec('def when():\n    return now()\n', vars(module))
            sys.modules[name] = self.modules[name] = module
        outside = types.ModuleType('outside_pkg')
        outside.__file__ = '/usr/lib/python3/outside_pkg.py'
        outside.now = real_now
        sys.modules['outside_pkg'] = self.modules['outside_pkg'] = outside
        self.addCleanup(lambda: [sys.modules.pop(name, None) for name in self.modules])

    def whens(self):
        return [self.modules[name].when() for name in ('owner_mod', 'assistant_copy', 'machine.moved')]

    def test_with_reaches_every_binding_and_puts_them_back(self):
        a = self.modules['assistant_copy']
        with patch_everywhere(a, 'now', return_value='fake') as fake:
            self.assertEqual(self.whens(), ['fake'] * 3)
            self.assertIs(self.modules['outside_pkg'].now, real_now)  # never outside the app
        self.assertEqual(fake.call_count, 3)
        self.assertEqual(self.whens(), ['real'] * 3)

    def test_a_different_object_of_the_same_name_is_left_alone(self):
        own = self.modules['machine.moved']
        own.now = lambda: 'its own'
        with patch_everywhere(self.modules['assistant_copy'], 'now', lambda: 'fake'):
            self.assertEqual(self.whens(), ['fake', 'fake', 'its own'])
        self.assertEqual(own.when(), 'its own')

    def test_start_stop_and_decorators(self):
        a = self.modules['assistant_copy']
        patcher = patch_everywhere(a, 'now', lambda: 'started')
        patcher.start()
        self.assertEqual(self.whens(), ['started'] * 3)
        patcher.stop()
        self.assertEqual(self.whens(), ['real'] * 3)

        @patch_everywhere(a, 'now', return_value='decorated')
        @mock.patch.object(self.modules['outside_pkg'], 'now', return_value='plain')
        def run(plain, fake):  # mock's order: the decorator nearest the function first
            return plain(), fake(), self.whens()
        self.assertEqual(run(), ('plain', 'decorated', ['decorated'] * 3))
        self.assertEqual(self.whens(), ['real'] * 3)

        @patch_everywhere(a, 'now', lambda: 'class')
        class Case:
            def test_one(self):
                return Seams.whens(outer)
        outer = self
        self.assertEqual(Case().test_one(), ['class'] * 3)
        self.assertEqual(self.whens(), ['real'] * 3)

    def test_replace_everywhere_is_for_good(self):
        changed = replace_everywhere(self.modules['assistant_copy'], 'now', lambda: 'stub')
        self.assertEqual(sorted(m.__name__ for m in changed), ['machine.moved', 'owner_mod'])
        self.assertEqual(self.whens(), ['stub'] * 3)


# --- every patch of an assistant module's name goes through seams ------------------------------------------------------

PATCH_OBJECT = {'patch.object', 'mock.patch.object', 'unittest.mock.patch.object'}


def assistant_aliases(tree):
    """Names a test file binds to a copy of assistant.py: loaded from its file, imported, or taken from another test."""
    def says_assistant(call):  # a loader call that names assistant: spec_from_file_location(.., 'assistant.py'), load('x_assistant')
        words = [c.value for c in ast.walk(call) if isinstance(c, ast.Constant) and isinstance(c.value, str)]
        return (any(w in ('assistant', 'assistant.py') or w.endswith('_assistant') for w in words)
                and not any(w.endswith('.py') and w != 'assistant.py' for w in words))
    found, specs = set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) and says_assistant(node.value):
            specs |= {t.id for t in node.targets if isinstance(t, ast.Name)}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Tuple)
                and isinstance(node.value, ast.Tuple) and len(node.targets[0].elts) == len(node.value.elts)):
            found |= {t.id for t, v in zip(node.targets[0].elts, node.value.elts)  # a, graph = tg.a, tg.graph
                      if isinstance(t, ast.Name) and isinstance(v, ast.Attribute) and v.attr in ('a', 'assistant')}
        elif isinstance(node, ast.Assign):
            names = {t.id for t in node.targets if isinstance(t, ast.Name)}
            if isinstance(node.value, ast.Call) and (says_assistant(node.value) or 'module_from_spec' in ast.unparse(node.value.func)
                                                     and any(isinstance(x, ast.Name) and x.id in specs for x in node.value.args)):
                found |= names
            elif isinstance(node.value, ast.Attribute) and node.value.attr in ('a', 'assistant'):
                found |= names
        elif isinstance(node, ast.Import):
            found |= {a.asname or a.name for a in node.names if a.name == 'assistant'}
        elif isinstance(node, ast.ImportFrom) and not node.level:
            found |= {a.asname or a.name for a in node.names if a.name in ('a', 'assistant')}
    return found


def plain_patches(source, name='<test>'):
    """[(line, attribute)] of patch.object(<assistant alias>, ...) and <assistant alias>.X = ... in a test file."""
    tree = ast.parse(source, name)
    aliases = assistant_aliases(tree)

    def is_assistant(node):  # a, or another test module's copy reached through it: tg.a.X = ...
        return (isinstance(node, ast.Name) and node.id in aliases
                or isinstance(node, ast.Attribute) and node.attr in ('a', 'assistant') and isinstance(node.value, ast.Name)
                and node.value.id != 'self')
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and ast.unparse(node.func) in PATCH_OBJECT and node.args and is_assistant(node.args[0]):
            out.append((node.lineno, ast.unparse(node.args[1]) if len(node.args) > 1 else '?'))
        elif isinstance(node, (ast.Assign, ast.AugAssign)):
            for target in node.targets if isinstance(node, ast.Assign) else [node.target]:
                if isinstance(target, ast.Attribute) and is_assistant(target.value):
                    out.append((node.lineno, target.attr))
        elif isinstance(node, ast.Call) and ast.unparse(node.func) == 'setattr' and node.args and is_assistant(node.args[0]):
            out.append((node.lineno, ast.unparse(node.args[1]) if len(node.args) > 1 else '?'))
    return sorted(out)


class EveryPatchGoesThroughSeams(unittest.TestCase):
    def test_no_plain_patch_on_assistant(self):
        for path in sorted((ROOT / 'tests').glob('*.py')):
            if path.name in ('seams.py', 'test_seams.py'):
                continue
            with self.subTest(file=path.name):
                found = plain_patches(path.read_text(encoding='utf-8'), path.name)
                self.assertEqual(found, [], f'{path.name} patches names on assistant directly (line, name): {found}. Use '
                                            'seams.patch_everywhere, so the patch also reaches code that moved out of '
                                            'assistant.py. Methods go through the class: patch.object(a.App, ...).')

    def test_the_check_sees_each_way_of_patching(self):
        source = ("import importlib.util\nfrom unittest import mock\nfrom unittest.mock import patch\nimport graph\n"
                  "spec = importlib.util.spec_from_file_location('x_assistant', 'assistant.py')\n"
                  "a = importlib.util.module_from_spec(spec)\nfrom test_fleet import a as b\n"
                  "with patch.object(a, 'now'): pass\nwith mock.patch.object(b, 'telegram'): pass\na.WORKSPACE = 1\n"
                  "setattr(b, 'now', 2)\nwith patch.object(a.App, 'run'): pass\nwith patch.object(graph, 'now'): pass\n"
                  "import test_graph as tg\nc, g = tg.a, tg.graph\nc.now = 3\ntg.a.now = 4\nself.a.now = 5\n")
        self.assertEqual(plain_patches(source), [(8, "'now'"), (9, "'telegram'"), (10, 'WORKSPACE'), (11, "'now'"),
                                                 (16, 'now'), (17, 'now')])


if __name__ == '__main__':
    unittest.main()
