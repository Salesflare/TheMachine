"""App's domain mixins (<domain>_app.py, APP_MIXINS in assistant.py) and the actions they handle (docs/code-map.md).

A mixin holds a domain's App methods and maps the actions it handles to them (its ACTIONS). App.action looks there first
and otherwise goes through its own branches. Who may call an action stays the reviewed sets in assistant.py."""
import ast
import functools
import importlib.util
import inspect
import json
from pathlib import Path
import re
import sys
import tempfile
import textwrap
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


def template_parts(cls):
    """The classes a template is made of (its own and what it is composed from), not the Template base."""
    import routine_templates
    return [part for part in cls.__mro__ if part not in (routine_templates.Template, object)]


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
        self.assertEqual(set(a.MailApp.ACTIONS) - {'mail_attachment'}, set(a.task_pages.ACTIONS) | a.COMPOSE_ACTIONS)
        self.assertEqual(set(a.SkillsApp.ACTIONS), a.SKILL_ACTIONS | {'skill_propose', 'skill_import_report'})
        self.assertEqual(set(a.AgentsApp.ACTIONS), a.AGENT_ACTIONS - {'set_agents'})  # App.action saves the settings
        self.assertEqual(set(a.GBrainApp.ACTIONS), a.GBRAIN_ACTIONS)
        self.assertEqual(set(a.SharedGraphApp.ACTIONS), a.GRAPH_SHARE_ACTIONS)
        self.assertEqual(set(a.MeetApp.ACTIONS), a.MEET_ACTIONS)
        self.assertEqual({n for n, m in a.ConnectApp.ACTIONS.items() if m == 'connect_owner_action'}, set(a.CONNECT_ACTIONS))
        repeat = {n for n, m in a.RecurringApp.ACTIONS.items()}
        self.assertEqual({n for n, m in a.CardActionsApp.ACTIONS.items() if m == 'card_owner_action'}, a.CARD_ACTIONS - repeat)
        self.assertEqual({n for n, m in a.SettingsActionsApp.ACTIONS.items() if m == 'learnings_action'},
                         a.LEARNING_ACTIONS - set(a.MissedWorkApp.ACTIONS) - set(a.BringInApp.ACTIONS))

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

    def test_routine_templates_are_declared_whole(self):
        # each Template (ROUTINE_TEMPLATES) runs catalog keys no other one runs, every catalog key has one, each names a
        # to-do kind the registry has and maps its actions to its own methods, none of them a mixin's too
        from machine import todo_kinds
        import routine_templates
        keys = [key for cls in a.ROUTINE_TEMPLATES for key in cls.KEYS]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(set(keys), set(routine_templates.TEMPLATES))
        for cls in a.ROUTINE_TEMPLATES:
            with self.subTest(template=cls.__name__):
                self.assertTrue(issubclass(cls, routine_templates.Template))
                self.assertIn(cls.KIND, {k.key for k in todo_kinds.KINDS})
                self.assertEqual(set(cls.ACTIONS), {n for part in template_parts(cls) for n in vars(part).get('ACTIONS', {})})
                for name, method in cls.ACTIONS.items():
                    self.assertNotIn(name, a.App.ACTION_HANDLERS)
                    self.assertTrue(callable(getattr(cls, method, None)), f'{name}: {cls.__name__} has no method {method}')
                    self.assertIs(a.App.TEMPLATE_ACTIONS[name], cls)

    def test_a_template_never_hides_an_app_member(self):
        # a template reads the App's members as its own (self.store): one of the same name on the template would hide it
        for cls in a.ROUTINE_TEMPLATES:
            with self.subTest(template=cls.__name__):
                mine = {name for part in template_parts(cls) for name in own(part)}
                self.assertEqual(sorted(mine & set(dir(a.App)) - {'ACTIONS'}), [])

    def test_what_a_template_sets_on_itself_only_it_reads(self):
        # a write through the template (self._x = ...) lands on the template, never on the App: a name it sets must be
        # read nowhere but in that template, or the App (or another template) would never see the new value
        def names(classes, writes):
            found = set()
            for part in classes:
                for node in ast.walk(ast.parse(textwrap.dedent(inspect.getsource(part)))):
                    if writes and isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                        for target in (node.targets if isinstance(node, ast.Assign) else [node.target]):
                            if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == 'self':
                                found.add(target.attr)
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('setattr', 'getattr', 'hasattr') \
                            and node.args and isinstance(node.args[0], ast.Name) and node.args[0].id == 'self' \
                            and len(node.args) > 1 and isinstance(node.args[1], ast.Constant) and (node.func.id == 'setattr') == writes:
                        found.add(node.args[1].value)
                    if not writes and isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == 'self':
                        found.add(node.attr)
            return found
        sets = {cls: names(template_parts(cls), True) for cls in a.ROUTINE_TEMPLATES}
        self.assertIn('_routine_offers_at', sets[a.CleanupTemplate])  # the check sees the one write there is
        for cls, written in sets.items():
            others = [a.App, *a.APP_MIXINS] + [p for other in a.ROUTINE_TEMPLATES if other is not cls for p in template_parts(other)]
            with self.subTest(template=cls.__name__):
                self.assertEqual(sorted(written & names(others, False)), [])

    def test_a_template_action_reaches_its_template(self):
        app = bare_app()
        with patch.object(a.DigestTemplate, 'digest_interest_action', lambda s, name, args, owner: (s, name, args, owner)):
            template, name, args, owner = app.action('digest_interest', {'topic': 'x'}, owner_dashboard=True)
        self.assertIs(template, app.template('digest'))
        self.assertIs(template.app, app)
        self.assertEqual((name, args, owner), ('digest_interest', {'topic': 'x'}, True))
        self.assertIs(app.template('newsletters'), app.template('spam'))  # one per App, whichever key loads it
        self.assertEqual(app.templates(), [app.template(k) for k in ('spam', 'digest', 'birthdays', 'subscriptions')])
        self.assertIsNone(app.template('gone'))
        # Birthdays' two modules are one template: its Facebook import's action reaches it
        with patch.object(a.BirthdaysTemplate, 'birthdays_facebook_action', lambda s, name, args, owner: s):
            self.assertIs(app.action('birthdays_facebook', {}, owner_dashboard=True), app.template('birthdays'))

    def test_moved_members_are_found_on_app(self):
        self.assertIs(a.App.bug_with_report, a.SupportApp.bug_with_report)
        self.assertEqual(a.App.REPORT_BUDGET, 20)


if __name__ == '__main__':
    unittest.main()
