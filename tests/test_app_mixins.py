"""App's domain mixins (<domain>_app.py, APP_MIXINS in assistant.py) and the actions they handle (docs/code-map.md).

A mixin holds a domain's App methods and maps the actions it handles to them (its ACTIONS). App.action looks there first
and otherwise goes through its own branches. Who may call an action stays the reviewed sets in assistant.py."""
import ast
import functools
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('assistant_app_mixins', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


sys.path.insert(0, str(ROOT))
import dashboard_parts  # noqa: E402


@functools.cache
def action_branches():
    # App.action's own if-branches (not the lookup in ACTION_HANDLERS), as (line, compiled test, names it spells out)
    found = []
    tree = ast.parse((ROOT / 'machine' / 'main.py').read_text(encoding='utf-8'))
    app = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'App')
    action = next(n for n in app.body if isinstance(n, ast.FunctionDef) and n.name == 'action')
    for node in action.body:
        if isinstance(node, ast.If) and 'ACTION_HANDLERS' not in ast.unparse(node.test):
            named = {c.value for c in ast.walk(node.test) if isinstance(c, ast.Constant) and isinstance(c.value, str)}
            found.append((node.lineno, compile(ast.Expression(node.test), 'App.action', 'eval'), named))
    return tuple(found)


def dashboard_actions():
    # every action name the dashboard posts to api/action: written out ({action:'name'}) or through a helper that
    # takes the action first (const skillAct=async(action,args)=>..., skillAct('skill_save', ...))
    page = dashboard_parts.assemble()
    names = set(re.findall(r"\baction:'([a-z0-9_]+)'", page))
    for helper in set(re.findall(r'(?:const|function)\s+(\w+)\s*=?\s*(?:async\s*)?\(\s*action\b', page)):
        names |= set(re.findall(r'\b' + helper + r"\(\s*'([a-z0-9_]+)'", page))
    return names


def resolves(name):
    class Self:
        def __getattr__(self, attr):
            return getattr(a.App, attr)
    if name in a.App.ACTION_HANDLERS:
        return True
    scope = dict(vars(a), name=name, args={}, owner_dashboard=True, accounts=[], selected=[], self=Self())
    return any(eval(test, scope) for _, test, _ in action_branches())  # noqa: S307 - App.action's own conditions


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
        # a mixin handles exactly the names of its reviewed set (plus the agent's own calls that went with them), so a
        # name added to one and not the other fails here
        self.assertEqual({n for n, m in a.SupportApp.ACTIONS.items() if m == 'support_dashboard_action'}, a.SUPPORT_ACTIONS)
        self.assertEqual(set(a.MailApp.ACTIONS) - {'mail_attachment'}, set(a.task_pages.ACTIONS))
        self.assertEqual(set(a.SkillsApp.ACTIONS), a.SKILL_ACTIONS | {'skill_propose', 'skill_import_report'})
        self.assertEqual(set(a.AgentsApp.ACTIONS), a.AGENT_ACTIONS - {'set_agents'})  # App.action saves the settings
        self.assertEqual(set(a.GBrainApp.ACTIONS), a.GBRAIN_ACTIONS)
        self.assertEqual(set(a.SharedGraphApp.ACTIONS), a.GRAPH_SHARE_ACTIONS)
        self.assertEqual(set(a.MeetApp.ACTIONS), a.MEET_ACTIONS)
        self.assertEqual({n for n, m in a.ConnectApp.ACTIONS.items() if m == 'connect_owner_action'}, set(a.CONNECT_ACTIONS))
        repeat = {n for n, m in a.RecurringApp.ACTIONS.items()}
        self.assertEqual({n for n, m in a.CardActionsApp.ACTIONS.items() if m == 'card_owner_action'}, a.CARD_ACTIONS - repeat)
        self.assertEqual({n for n, m in a.SettingsActionsApp.ACTIONS.items() if m == 'learnings_action'},
                         a.LEARNING_ACTIONS - set(a.MissedWorkApp.ACTIONS))

    def test_every_reviewed_action_resolves(self):
        # each name the reviewed sets let a caller send reaches a mixin's handler or one of App.action's own branches
        missing = [name for name in sorted(a.OWNER_ACTIONS | a.DASHBOARD_ACTIONS) if not resolves(name)]
        self.assertEqual(missing, [], 'actions in the reviewed sets that nothing in App.action handles')

    def test_every_action_the_dashboard_sends_has_a_handler(self):
        sent = dashboard_actions()
        self.assertIn('set_agents', sent)
        self.assertGreater(len(sent), 100)  # the scan still finds the helpers' calls
        self.assertEqual(sorted(sent - a.DASHBOARD_ACTIONS), [], 'actions the dashboard sends that its route refuses')
        self.assertEqual([name for name in sorted(sent) if not resolves(name)], [], 'actions the dashboard sends that nothing handles')

    def test_no_branch_of_app_action_is_shadowed_by_a_mixin(self):
        # App.action asks the mixins first: a branch that names an action a mixin also maps never runs (set_agents
        # went to the hand-off handler this way and failed with Unknown operation)
        shadowed = [(name, line) for line, _, named in action_branches() for name in sorted(named & set(a.App.ACTION_HANDLERS))]
        self.assertEqual(shadowed, [], 'actions both a mixin and a branch of App.action handle')

    def test_set_agents_saves_from_the_dashboard(self):
        # Settings, where agents run: saved by App.set_agents, also when handing off is off on this Machine
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'config.json'
            path.write_text(json.dumps({'accounts': []}))
            app = bare_app()
            app.config_path, app.agents = path, None
            with self.assertRaisesRegex(ValueError, 'Only the owner changes this'):
                app.action('set_agents', {'codex_env': 'env_123'})
            saved = app.action('set_agents', {'claude_session': 'https://claude.ai/code/session_01AbCdEfGh1234', 'codex_env': 'env_123'},
                               owner_dashboard=True)
            self.assertEqual((saved['claude_session'], saved['codex_env']), ('session_01AbCdEfGh1234', 'env_123'))
            self.assertEqual(json.loads(path.read_text())['agents']['codex'], {'place': 'cloud', 'env': 'env_123'})

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
