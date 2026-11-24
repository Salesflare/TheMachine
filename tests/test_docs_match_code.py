"""The reference docs list what the code has, and nothing it no longer has. Static and fast: no network, no model.

- every top-level config.json key the code reads is in docs/configuration.md, and every key there is still read;
- every `assistant` command is in docs/usage.md's Command line, each choice it takes is in its row, and a choice the
  row lists is one the command takes; `assistant connect --help` names every built-in source; docs name only commands
  that exist;
- every source (onboarding.SERVICES and the connector plugins) has a row in docs/sources.md and a place in
  docs/architecture.md's diagram, and neither lists a source that is gone. (Its help article: scripts/help_check.py.)

When one fails, update the doc in the same pull request; never add to the lists below to get it green unless the
thing really isn't the owner's (a key of another program's config, say)."""
import argparse
import ast
import importlib.util
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
# How the code names the Machine's config: config.get('key'), self.config['key'], app.config.setdefault('key') ...
READ = re.compile(r"(?:\b(?:self\.app\.config|self\.config|app\.config|config)|\(config or \{\}\))(?:\.get\(|\.setdefault\(|\.pop\(|\[)\s*['\"]([a-z][a-z0-9_]*)['\"]")
# Keys read through a variable called config that is another program's config, with where
NOT_OURS = {
    'commands': "OpenClaw's openclaw.json (moving.py, who may talk to the bot)",
}
# Sources the diagram in docs/architecture.md names by another name than their label (onboarding.label)
DIAGRAM_NAMES = {
    'caldav': 'CalDAV', 'icloud_calendar': 'CalDAV', 'proton_calendar': 'ICS', 'ics': 'ICS', 'exchange': 'Exchange',
    'imap': 'Other email (IMAP)', 'docs': 'Docs', 'gateway': 'OpenClaw Gateway', 'salesflare': 'Salesflare CRM', 'rss': 'RSS',
}


def code_files():
    return [p for p in [*ROOT.glob('*.py'), *ROOT.glob('machine/**/*.py'), *ROOT.glob('connectors/*.py'),
                        *ROOT.glob('integrations/*.py')] if not p.name.startswith('test')]


def config_reads():
    """{key: [files]} of every top-level config key the code reads."""
    found = {}
    for path in code_files():
        for m in READ.finditer(path.read_text(encoding='utf-8')):
            found.setdefault(m[1], []).append(path.relative_to(ROOT).as_posix())
    assert len(found) > 100, 'READ finds the keys the code reads'
    return {k: v for k, v in found.items() if k not in NOT_OURS}


def table_keys(text, first_column=True):
    """The `keys` in the first column of a doc's Markdown tables."""
    keys = set()
    for line in text.splitlines():
        if line.startswith('| `'):
            keys |= set(re.findall(r'`([a-z][a-z0-9_]*)`', line.split('|')[1]))
    assert len(keys) > 20, 'the tables list their keys in backticks, first column'
    return keys


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def services():
    """Every source id: onboarding.SERVICES' and the connector plugins' (the ones with a SETUP)."""
    for node in ast.parse((ROOT / 'onboarding.py').read_text(encoding='utf-8')).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'SERVICES':
            built_in = set(ast.literal_eval(node.value).values())
    plugins = {p.stem for p in (ROOT / 'connectors').glob('*.py') if 'SETUP' in p.read_text(encoding='utf-8')}
    return built_in, plugins


class ConfigKeys(unittest.TestCase):
    def test_every_key_the_code_reads_is_documented(self):
        documented = set(re.findall(r'`([a-z][a-z0-9_]*)`', (DOCS / 'configuration.md').read_text(encoding='utf-8')))
        missing = {k: v[:2] for k, v in config_reads().items() if k not in documented}
        self.assertEqual(missing, {}, 'config keys the code reads with no row in docs/configuration.md')

    def test_every_documented_key_is_still_read(self):
        code = '\n'.join(p.read_text(encoding='utf-8', errors='replace') for p in
                         [*code_files(), *ROOT.glob('*.mjs'), *ROOT.glob('openclaw-plugin/*.ts'), *ROOT.glob('*.sh'), ROOT / 'install.ps1'])
        gone = sorted(k for k in table_keys((DOCS / 'configuration.md').read_text(encoding='utf-8'))
                      if not re.search(r'''['"]''' + k + r'''['"]''', code))
        self.assertEqual(gone, [], 'docs/configuration.md lists keys no code reads any more')

    def test_the_scan_sees_reads_and_leaves_out_other_configs(self):
        self.assertEqual(READ.findall("a = (config or {}).get('epsilon') or view(db, config or {})['zeta']"), ['epsilon'])
        text = "x = config.get('alpha')\ny = self.config['beta']\nz = self.app.config.setdefault('gamma', 1)\nw = cfg.get('delta')\n"
        self.assertEqual([m[1] for m in READ.finditer(text)], ['alpha', 'beta', 'gamma'])


class CommandLine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cli = load('cli')
        sub = next(a for a in cls.cli.parser()._actions if isinstance(a, argparse._SubParsersAction))
        cls.commands = dict(sub.choices)
        usage = (DOCS / 'usage.md').read_text(encoding='utf-8')
        cls.section = usage[usage.index('## Command line'):]
        cls.section = cls.section[:cls.section.index('\n## ', 3)]

    def row(self, name):
        return next((line for line in self.section.splitlines() if line.startswith(f'| `assistant {name}')), None)

    def test_every_command_is_in_the_docs(self):
        missing = [name for name in self.commands if not self.row(name) and f'`{name}`' not in self.section]
        self.assertEqual(missing, [], "commands with no row (or mention) in docs/usage.md's Command line")

    def test_every_choice_a_command_takes_is_in_its_row_and_back(self):
        rows = 0
        for name, command in self.commands.items():
            row = self.row(name) or ''
            for action in command._actions:
                if action.choices and not action.option_strings:
                    for choice in action.choices:
                        self.assertIn(choice, row, f'assistant {name} takes {choice}, which its row in docs/usage.md leaves out')
                    listed = re.match(r'\| `assistant [a-z-]+ ([a-z-]+(?:\\\|[a-z-]+)+)', row)
                    rows += bool(listed)
                    for choice in (listed[1].split('\\|') if listed else []):
                        self.assertIn(choice, action.choices, f'docs/usage.md lists assistant {name} {choice}, which it doesn\'t take')
        self.assertGreater(rows, 1, 'rows that list their choices as a\\|b')

    def test_connect_names_every_built_in_source(self):
        source = next(a for a in self.commands['connect']._actions if a.dest == 'source')
        hidden = {'salesflare', 'outlook-calendar', 'telegram-chats'}  # onboarding.sources(): crm, outlook_calendar, telegram
        built_in = sorted(set(self.cli.onboarding.SERVICES) - hidden)
        self.assertEqual([s for s in built_in if not re.search(r'\b' + s + r'\b', source.help)], [],
                         'assistant connect --help leaves out built-in sources')

    def test_docs_name_only_commands_that_exist(self):
        names = set(self.commands) | {'connect'}
        said = [(p.name, m) for p in DOCS.glob('*.md') for m in re.findall(r'`assistant ([a-z][a-z-]*)', p.read_text(encoding='utf-8'))]
        self.assertGreater(len(said), 50, 'the commands the docs name')
        wrong = sorted({f'{name}: assistant {m}' for name, m in said if m not in names})
        self.assertEqual(wrong, [], 'docs name assistant commands cli.py does not have')


class Sources(unittest.TestCase):
    def test_every_source_has_one_row_in_sources_md(self):
        built_in, plugins = services()
        rows = table_keys((DOCS / 'sources.md').read_text(encoding='utf-8')) - {'service'}
        self.assertEqual(sorted((built_in | plugins) - rows), [], 'sources with no row in docs/sources.md')
        self.assertEqual(sorted(rows - built_in - plugins), [], 'docs/sources.md has rows for sources that are gone')

    def test_the_architecture_diagram_names_every_source_and_no_other(self):
        onboarding = load('onboarding')
        built_in, plugins = services()
        text = (DOCS / 'architecture.md').read_text(encoding='utf-8')
        diagram = text[text.index('```text') + 7:]
        lines = diagram[:diagram.index('│')].strip().splitlines()
        items = [i.strip() for line in lines for i in line.removeprefix('plugins:').split('·') if i.strip()]
        names = {s: {DIAGRAM_NAMES.get(s), onboarding.label(s), s.replace('_', ' ').capitalize()} - {None}
                 for s in built_in | plugins}
        self.assertEqual(sorted(s for s, n in names.items() if not any(x in ' · '.join(items) for x in n)), [],
                         "sources docs/architecture.md's diagram leaves out")
        known = set().union(*names.values())
        self.assertEqual([i for i in items if not any(n in i for n in known)], [],
                         "docs/architecture.md's diagram names sources that are gone")


if __name__ == '__main__':
    unittest.main()
