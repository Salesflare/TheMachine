"""App's domain mixins (<domain>_app.py, APP_MIXINS in assistant.py) and the actions they handle (docs/code-map.md).

A mixin holds a domain's App methods and maps the actions it handles to them (its ACTIONS). App.action looks there first
and otherwise goes through its own branches. Who may call an action stays the reviewed sets in assistant.py."""
import ast
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('assistant_app_mixins', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def own(cls):
    return {name for name in vars(cls) if not (name.startswith('__') and name.endswith('__'))}


def bare_app():
    app = object.__new__(a.App)
    app.config = {'accounts': []}
    return app


class AppMixins(unittest.TestCase):
    def test_no_action_is_mapped_twice(self):
        seen = {}
        for mixin in a.APP_MIXINS:
            for name in mixin.ACTIONS:
                self.assertNotIn(name, seen, f'{name} is in {seen.get(name)} and {mixin.__name__}')
                seen[name] = mixin.__name__
        self.assertEqual(set(seen), set(a.App.ACTION_HANDLERS))

    def test_no_member_is_defined_twice(self):
        # App's own definition would win over a mixin's without a word, and of two mixins the first one would
        owners = {}
        for cls in (a.App, *a.APP_MIXINS):
            for name in own(cls) - {'ACTIONS'}:
                self.assertNotIn(name, owners, f'{name} is in {owners.get(name)} and {cls.__name__}')
                owners[name] = cls.__name__

    def test_every_handler_is_a_method(self):
        for name, method in a.App.ACTION_HANDLERS.items():
            with self.subTest(action=name):
                self.assertTrue(callable(getattr(a.App, method, None)), f'{name}: App has no method {method}')

    def test_mixin_actions_keep_their_reviewed_sets(self):
        self.assertEqual(set(a.SupportApp.ACTIONS), a.SUPPORT_ACTIONS)
        for name in a.App.ACTION_HANDLERS:
            with self.subTest(action=name):
                self.assertIn(name, a.OWNER_ACTIONS | a.DASHBOARD_ACTIONS, 'an action no reviewed set lets anyone call')

    def test_every_reviewed_action_resolves(self):
        # each name the reviewed sets let a caller send reaches a mixin's handler or one of App.action's own branches
        tree = ast.parse((ROOT / 'assistant.py').read_text(encoding='utf-8'))
        app = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'App')
        action = next(n for n in app.body if isinstance(n, ast.FunctionDef) and n.name == 'action')
        tests = [compile(ast.Expression(node.test), 'App.action', 'eval') for node in action.body if isinstance(node, ast.If)]

        class Self:
            def __getattr__(self, name):
                return getattr(a.App, name)
        missing = []
        for name in sorted(a.OWNER_ACTIONS | a.DASHBOARD_ACTIONS):
            scope = dict(vars(a), name=name, args={}, owner_dashboard=True, accounts=[], selected=[], self=Self())
            if not any(eval(test, scope) for test in tests):  # noqa: S307 - App.action's own conditions
                missing.append(name)
        self.assertEqual(missing, [], 'actions in the reviewed sets that nothing in App.action handles')

    def test_support_actions_from_the_dashboard_only(self):
        with patch.object(a.App, 'support_action', return_value={'ok': True}) as support:
            with self.assertRaisesRegex(ValueError, 'Help and bug reports come from the dashboard'):
                bare_app().action('help_ask', {'question': 'x'})
            support.assert_not_called()
            self.assertEqual(bare_app().action('help_article', {'slug': 's'}, owner_dashboard=True), {'ok': True})
            support.assert_called_once_with('help_article', {'slug': 's'})

    def test_calendar_actions(self):
        with patch.object(a.App, 'calendar_write', return_value='written') as write, \
                patch.object(a.App, 'meeting_notes', return_value='notes') as notes, \
                patch.object(a.App, 'meeting_write', return_value='writing') as writing:
            with self.assertRaisesRegex(ValueError, 'Calendar changes come from your tap in the dashboard'):
                bare_app().action('calendar_write', {})
            with self.assertRaisesRegex(ValueError, 'Only the owner asks for notes to be written, in the Calendar'):
                bare_app().action('meeting_notes_write', {})
            write.assert_not_called()
            writing.assert_not_called()
            self.assertEqual(bare_app().action('calendar_write', {'id': 1}, owner_dashboard=True), 'written')
            write.assert_called_once_with({'id': 1})
            self.assertEqual(bare_app().action('meeting_notes', {'id': 2}), 'notes')
            notes.assert_called_once_with({'id': 2}, False)
            self.assertEqual(bare_app().action('meeting_notes_write', {'id': 3}, True), 'writing')
            writing.assert_called_once_with({'id': 3})

    def test_moved_members_are_found_on_app(self):
        self.assertIs(a.App.bug_with_report, a.SupportApp.bug_with_report)
        self.assertEqual(a.App.REPORT_BUDGET, 20)


if __name__ == '__main__':
    unittest.main()
