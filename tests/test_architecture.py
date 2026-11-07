"""Guards for the code layout (docs/code-map.md): what keeps code moving between modules safe while assistant.py is
split up. Static checks of the source only; nothing is imported or run.

- every module defines or imports each global name it uses, so a function moved without its import fails here and
  not with a NameError at runtime;
- no module loads assistant.py except the entry points that do so today (tests may);
- each table is created by one module, its owner, and written only by its owner, apart from the writers listed in
  OTHER_WRITERS as they are today;
- modules in machine/ import only from their own layer or the ones below it (MACHINE_LAYERS), never `*`;
- Python files stay under PY_LINE_BUDGET lines and PY_BYTE_BUDGET bytes, apart from today's bigger ones in
  PY_OVER_BUDGET, whose ceilings only come down;
- i18n_extract's dashboard AREAS all resolve.

`python3 tests/test_architecture.py --owners` prints each module with the tables it owns."""
import ast
import builtins
import functools
import pathlib
import re
import symtable
import sys
import unittest

import dashboard_parts

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {'node_modules', '.git', '.venv', '__pycache__'}


def python_files(tests=True):
    """Every Python file in the repository (relative path, posix), subfolders included, so code moved into a folder
    stays covered."""
    out = []
    for path in sorted(ROOT.rglob('*.py')):
        parts = path.relative_to(ROOT).parts
        if SKIP_DIRS & set(parts[:-1]) or (not tests and parts[0] == 'tests'):
            continue
        out.append(path.relative_to(ROOT).as_posix())
    return out


@functools.lru_cache(maxsize=None)
def nodes(name):
    """Every node of a file's syntax tree (walked once, the guards share it)."""
    return list(ast.walk(ast.parse((ROOT / name).read_text(encoding='utf-8'), name)))


# --- names -----------------------------------------------------------------------------------------------------------

# names a module has without defining them
MODULE_NAMES = set(dir(builtins)) | {'__file__', '__name__', '__doc__', '__spec__', '__loader__', '__package__',
                                     '__builtins__', '__path__', '__annotations__', '__dict__', '__cached__'}
# names the compiler adds to scopes in some Python versions (class cells, annotation scopes)
COMPILER_NAMES = {'__class__', '__classcell__', '__classdict__', '__conditional_annotations__', '__annotate__'}


def undefined_names(source, filename='<module>'):
    """[(name, line)] of global names the module uses (at its top level or in any function, class, lambda or
    comprehension) that it never defines, imports or assigns (`global x; x = ...` counts)."""
    top = symtable.symtable(source, filename, 'exec')
    defined, used = set(), set()
    for symbol in top.get_symbols():
        if symbol.is_assigned() or symbol.is_imported() or symbol.is_namespace():
            defined.add(symbol.get_name())
        elif symbol.is_referenced():
            used.add(symbol.get_name())

    def walk(table):
        for child in table.get_children():
            for symbol in child.get_symbols():
                if not symbol.is_global():
                    continue
                if symbol.is_declared_global() and symbol.is_assigned():
                    defined.add(symbol.get_name())
                if symbol.is_referenced():
                    used.add(symbol.get_name())
            walk(child)
    walk(top)
    if '*' in defined:  # `from x import *`: can't tell
        return []
    missing = {n for n in used - defined - MODULE_NAMES - COMPILER_NAMES if not n.startswith('.')}
    if not missing:
        return []
    lines = {}
    for node in ast.walk(ast.parse(source, filename)):
        if isinstance(node, ast.Name) and node.id in missing:
            lines[node.id] = min(lines.get(node.id, node.lineno), node.lineno)
    return sorted((name, lines.get(name, 0)) for name in missing)


# --- assistant.py ----------------------------------------------------------------------------------------------------

# Modules that load assistant.py today. assistant.py is the composition root: the service runs it as `__main__`, so an
# `import assistant` elsewhere makes a second copy with its own Store, SourceError and globals. Move what a module
# needs out of assistant.py instead of adding a module here. Tests may load it.
LOADS_ASSISTANT = {
    'cli.py': 'the command line, an entry point (spec_from_file_location)',
    'onboarding.py': 'loads it on first use for sources and credentials (spec_from_file_location)',
    'retention.py': 'lazy, for Store: the service\'s own sealed connection',
    'sandbox/load.py': 'the sandbox, an entry point',
    'sandbox/run.py': 'the sandbox, an entry point',
    'work_removal.py': 'lazy, for Store',
}
LOADERS = {'spec_from_file_location', 'import_module', '__import__', 'load_source', 'run_path'}


def loads_module(found, wanted):
    """Lines where the module imports a module for which wanted(name) is true: import, from-import, or a loader call
    (importlib, runpy) naming it or its file."""
    lines = []
    for node in found:
        names = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and not node.level:
            names = [node.module or '']
        elif isinstance(node, ast.Call):
            func = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, 'id', '')
            if func in LOADERS:
                names = [c.value.removesuffix('.py') for c in ast.walk(node)
                         if isinstance(c, ast.Constant) and isinstance(c.value, str)]
        if any(wanted(name) for name in names):
            lines.append(node.lineno)
    return lines


# --- machine/ layers -------------------------------------------------------------------------------------------------

# The package assistant.py's code moves into (docs/code-map.md). Each top-level module or folder of machine/ has a layer;
# a module imports only from its own layer or the ones below it (and any root module), so the code can't grow a cycle
# and Store and App's helpers stay importable without them. A new area gets its layer here in the pull request that adds
# it. Lazy imports inside a function count too.
MACHINE_LAYERS = {
    'actions': 0,      # the *_ACTIONS sets, the security boundary
    'config': 0,
    'names': 0,        # what the owner calls a service, app or agent (never the tool underneath)
    'stamps': 0,       # change counters per table, so a request's answer is kept until its tables change
    'text': 0,         # message parsing
    'timing': 0,       # request timing, shared by web and store
    'browser': 1,
    'cards': 1,
    'chat': 1,
    'faults': 1,
    'model_usage': 1,
    'prompts': 1,
    'sources': 1,
    'store': 2,
    'upkeep': 2,       # housekeeping of the data folder: agent job folders (retention.py runs it)
    'delivery': 3,
    'export': 3,       # export and import: what an install keeps (inventory), the hold after an import
    'web': 3,
    'app': 4,
    'main': 4,
}


def machine_area(module):
    """'store' for machine.store.cards, None for a module outside machine/ (or machine itself)."""
    parts = module.split('.')
    return parts[1] if len(parts) > 1 and parts[0] == 'machine' else None


def machine_layer_problems(rel, source):
    """[(line, problem)] of a machine/ module's imports that break the layer rule, or of `import *`."""
    parts = rel.removesuffix('.py').split('/')
    package = parts[:-1]  # what a relative import starts from (an __init__'s own package)
    if parts[-1] == '__init__':
        parts = parts[:-1]
    own = machine_area('.'.join(parts))
    problems = []
    if own is None:  # machine/__init__.py stays empty, so importing one area never loads another
        return [(n.lineno, 'machine/__init__.py imports nothing') for n in ast.walk(ast.parse(source, rel))
                if isinstance(n, (ast.Import, ast.ImportFrom))]
    if own not in MACHINE_LAYERS:
        return [(1, f'machine/{own} has no layer: add it to MACHINE_LAYERS in tests/test_architecture.py')]
    for node in ast.walk(ast.parse(source, rel)):
        wanted = []
        if isinstance(node, ast.Import):
            wanted = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if any(alias.name == '*' for alias in node.names):
                problems.append((node.lineno, 'no `import *` in machine/: name what it uses'))
            if node.level:
                if node.level > len(package):
                    problems.append((node.lineno, 'a relative import above machine/'))
                    continue
                base = package[:len(package) - node.level + 1]
                module = '.'.join(base + ([node.module] if node.module else []))
            else:
                module = node.module or ''
            # `from machine import store` and `from . import store` name the area in the imported names
            wanted = [f'{module}.{alias.name}' for alias in node.names] if machine_area(module) is None else [module]
        for name in wanted:
            area = machine_area(name)
            if area is None or area == own:
                continue
            if area not in MACHINE_LAYERS:
                problems.append((node.lineno, f'imports machine.{area}, which has no layer in MACHINE_LAYERS'))
            elif MACHINE_LAYERS[area] > MACHINE_LAYERS[own]:
                problems.append((node.lineno, f'machine.{own} (layer {MACHINE_LAYERS[own]}) imports machine.{area} '
                                              f'(layer {MACHINE_LAYERS[area]}): move what it needs down a layer, or '
                                              'pass it in'))
    return sorted(problems)


# --- tables ----------------------------------------------------------------------------------------------------------

CREATE = re.compile(r'\bCREATE\s+(?:VIRTUAL\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?["`\[]?([A-Za-z_]\w*)\b(?!\.)')
WRITE = re.compile(r'\b(?:INSERT(?:\s+OR\s+[A-Z]+)?\s+INTO|REPLACE\s+INTO|DELETE\s+FROM)\s+["`\[]?([A-Za-z_]\w*)\b(?!\.)'
                   r'|\bUPDATE(?:\s+OR\s+[A-Z]+)?\s+["`\[]?([A-Za-z_]\w*)["`\]]?\s+SET\b')

SQL_WORD = re.compile('CREATE|INSERT|REPLACE|UPDATE|DELETE')

# Tables more than one module creates today: the owner. The others' CREATE stays allowed until the code moves.
SHARED_SCHEMA = {
    'contact_photo_links': ('enrichment.py', {'graph.py'}),
    'enrich_prefs': ('enrichment.py', {'graph.py', 'security_levels.py'}),
    'event_search': ('message_seal.py', {'assistant.py'}),
    'person_facts': ('enrichment.py', {'graph.py'}),
    'person_photo_tries': ('enrichment.py', {'graph.py'}),
    'team_learning_prefs': ('team_learnings.py', {'security_levels.py'}),
}

# Modules that write a table another module owns, as of 2026-10-29. Each is a place where a move can break an
# invariant the owner keeps (sealing, cards' state, counts), so the list may only shrink: write through a function of
# the owner instead. One table per line, sorted, so parallel pull requests merge.
OTHER_WRITERS = {
    'action_jobs': {'follow_ups.py', 'machine/export/hold.py'},
    'agent_jobs': {'agent_remote.py', 'assistant.py', 'sandbox/load.py'},
    'agent_result_receipts': {'agent_remote.py'},
    'analyses': {'graph.py', 'sandbox/load.py', 'work_removal.py'},
    'board_backfills': {'sandbox/load.py'},
    'board_offers': {'assistant.py'},
    'boards': {'shared_graph.py'},
    'chats': {'telegram_mirror.py'},
    'checkpoints': {'sandbox/load.py'},
    'crm_tags': {'crm_import.py'},
    'decisions': {'follow_ups.py', 'graph.py', 'machine/app/follow_ups.py', 'sandbox/load.py', 'work_removal.py'},
    'deliveries': {'fleet.py', 'follow_ups.py', 'machine/app/follow_ups.py', 'machine/delivery/deliver.py', 'machine/export/hold.py',
                   'sandbox/load.py'},
    'draft_edits': {'graph.py'},
    'enrich_prefs': {'security_levels.py'},
    'event_search': {'assistant.py'},
    'events': {'sandbox/load.py', 'work_removal.py'},
    'facts': {'learning_loop.py'},
    'fleet_briefs': {'sandbox/run.py'},
    'fleet_in': {'fleet_requests.py'},
    'fleet_learn_read': {'shared_graph.py'},
    'fleet_learn_removed': {'shared_graph.py'},
    'fleet_learn_seen': {'shared_graph.py'},
    'fleet_learnings': {'shared_graph.py'},
    'fleet_meta': {'family.py', 'fleet_requests.py', 'security_levels.py', 'shared_graph.py'},
    'fleet_rules': {'fleet_requests.py'},
    'graph_imports': {'crm_import.py'},
    'graph_names': {'crm.py', 'crm_import.py'},
    'graph_nodes': {'crm.py', 'crm_fields.py'},
    'graph_offers': {'assistant.py'},
    'graph_org_asks': {'assistant.py'},
    'graph_role_asks': {'assistant.py'},
    'identity_names': {'assistant.py'},
    'manual_nodes': {'crm_import.py'},
    'meeting_moves': {'assistant.py'},
    'meeting_writes': {'machine/app/meeting_writes.py'},
    'messages': {'telegram_mirror.py'},
    'milestones': {'machine/app/first_look.py'},
    'network_people': {'graph.py'},
    'network_request_nodes': {'network.py'},
    'org_edits': {'crm.py', 'crm_import.py'},
    'org_profiles': {'enrichment.py', 'sandbox/load.py'},
    'outbox': {'next_actions.py', 'telegram_mirror.py'},
    'person_edits': {'contact_share.py', 'crm_import.py'},
    'person_orgs': {'crm_import.py'},
    'person_photos': {'enrichment.py'},
    'person_profiles': {'bounces.py', 'enrichment.py'},
    'photo_asks': {'telegram_mirror.py'},
    'preparation_calls': {'retention.py'},
    'preparation_runs': {'assistant.py'},
    'preparations': {'follow_ups.py', 'preparation_state.py'},
    'profile_runs': {'fleet_learnings.py', 'learning_loop.py', 'machine/app/fleet.py', 'retention.py', 'team_learnings.py'},
    'project_moves': {'crm_import.py', 'follow_ups.py'},
    'projects': {'crm.py', 'crm_import.py', 'follow_ups.py', 'machine/app/graph_actions.py', 'sandbox/load.py'},
    'promises': {'graph.py', 'machine/app/promise_checks.py', 'sandbox/load.py'},
    'push_subscriptions': {'machine/delivery/push.py', 'machine/export/hold.py'},
    'recap_items': {'machine/app/recap.py'},
    'recaps': {'machine/app/recap.py'},
    'record_owners': {'crm_import.py'},
    'review_runs': {'sandbox/load.py'},
    'rule_changes': {'learning_loop.py', 'machine/app/recap.py'},
    'skills': {'sandbox/load.py'},
    'suggestions': {'fleet.py', 'follow_ups.py', 'graph.py', 'machine/app/promise_checks.py', 'machine/delivery/deliver.py',
                    'sandbox/load.py', 'work_removal.py'},
    'sync_activity': {'retention.py', 'sandbox/load.py'},
    'team_learning_prefs': {'security_levels.py'},
    'voices': {'learning_loop.py'},
}


def sql_strings(found):
    """(line, text) of every string in the module that isn't a docstring; an f-string's holes become {}."""
    docs = set()
    for node in found:
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                docs.add(id(first.value))
    parts = set()
    for node in found:
        if isinstance(node, ast.JoinedStr):
            parts.update(id(v) for v in node.values)
            yield node.lineno, ''.join(v.value if isinstance(v, ast.Constant) else '{}' for v in node.values)
    skip = docs | parts
    for node in found:
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in skip:
            yield node.lineno, node.value


# The Store moves out of assistant.py in parts (refactor PRs 13-18). Until it is whole in machine/store/, its parts
# are one owner with assistant.py: a table the Store creates or writes from one of them is assistant.py's, as before.
STORE_PARTS = {'machine/store/cards.py', 'machine/store/core.py', 'machine/store/decisions.py', 'machine/store/events.py',
               'machine/store/facts.py', 'machine/store/first_look.py', 'machine/store/profile.py', 'machine/store/promises.py',
               'machine/store/review.py', 'machine/store/views.py', 'machine/store/voices.py'}


@functools.lru_cache(maxsize=None)
def schema_and_writes():
    """({table: {module: line}} of CREATE TABLE, {table: {module: line}} of INSERT/REPLACE/UPDATE/DELETE), for every
    module outside tests/. Statements with a computed table name (f'DELETE FROM {table}') aren't seen. STORE_PARTS
    count as assistant.py."""
    creates, writes = {}, {}
    for path in python_files(tests=False):
        name = 'assistant.py' if path in STORE_PARTS else path
        for line, text in sql_strings(nodes(path)):
            if not SQL_WORD.search(text):
                continue
            for m in CREATE.finditer(text):
                creates.setdefault(m.group(1), {}).setdefault(name, line)
            for m in WRITE.finditer(text):
                if text[m.end():m.end() + 1] != '.':  # temp.x, main.x
                    writes.setdefault(m.group(1) or m.group(2), {}).setdefault(name, line)
    return creates, writes


def owner(table, creates):
    if table in SHARED_SCHEMA:
        return SHARED_SCHEMA[table][0]
    found = creates.get(table) or {}
    return next(iter(found)) if len(found) == 1 else None


# --- tests -----------------------------------------------------------------------------------------------------------

# Aikido's code scan skips big files (some just over 500 KiB already go unscanned), so a page or script that big
# ships unchecked. Shipped .html, .css, .js and .mjs files (tests aside) stay under SCAN_LIMIT, with room to spare. The
# dashboard's source has smaller budgets by kind (BUDGETS): dashboard.html holds the order of its parts, and each part in
# dashboard/ one area's script, styles or markup (docs/code-map.md). OVER_BUDGET lists today's bigger files with a
# ceiling that may only come down: one that grows fails, and one back under its budget fails until it's removed.
SCAN_LIMIT = 450 * 1024
BUDGETS = {'dashboard.html': 24 * 1024, 'dashboard/*.js': 160 * 1024, 'dashboard/*.css': 64 * 1024,
           'dashboard/*.html': 32 * 1024}
OVER_BUDGET = {}
# The page as served (dashboard.html with its parts): what a phone downloads. Not a scan rule, a watch: a ceiling that
# may only come down; raise it on purpose, in a pull request that says why.
# 2,000,000 -> 2,100,000 (2026-11-07): main passed 2,000,000 with no single big piece to take out (no inline assets,
# no string table). The real fix is the dashboard split of the code refactor (load parts when they're used); this is
# headroom while that lands, so main stays green. Bring it back down with the split.
PAGE_CEILING = 2_100_000


def budget(name):
    """The size a shipped file stays under: its kind's budget in the dashboard's source, SCAN_LIMIT elsewhere."""
    if name in BUDGETS:
        return BUDGETS[name]
    folder, _, file = name.rpartition('/')
    return BUDGETS.get(f'{folder}/*.{file.rpartition(".")[2]}', SCAN_LIMIT) if folder == 'dashboard' else SCAN_LIMIT


# Python files: the same scan limit, and a line budget that keeps a module small enough to read and review. A new
# module that would go over is split first. PY_OVER_BUDGET lists today's bigger files with (lines, bytes) ceilings
# that may only come down: a file that grows past its ceiling fails; one that shrinks more than PY_RATCHET_SLACK under
# it fails until the ceiling is lowered to its new size (round up a little); one back under the budget fails until its
# entry is removed. Each pull request that moves code out of assistant.py lowers its ceiling. Tests aside.
PY_LINE_BUDGET = 2_500
PY_BYTE_BUDGET = 450 * 1024
PY_RATCHET_SLACK = (500, 50_000)
PY_OVER_BUDGET = {
    'assistant.py': (8_000, 550_000),
    'fleet.py': (3_800, PY_BYTE_BUDGET),
    'graph.py': (5_400, PY_BYTE_BUDGET),
    'next_actions.py': (2_650, PY_BYTE_BUDGET),
    'onboarding.py': (3_100, PY_BYTE_BUDGET),
    'shared_graph.py': (3_200, PY_BYTE_BUDGET),
}


def python_sizes():
    """{file: (lines, bytes)} of every Python file outside tests/."""
    out = {}
    for name in python_files(tests=False):
        data = (ROOT / name).read_bytes()
        out[name] = (data.count(b'\n'), len(data))
    return out


def py_budget_problems(sizes, over=None, budget=None, slack=PY_RATCHET_SLACK):
    """[problem] for files over the budget or their ceiling, and PY_OVER_BUDGET entries to lower or remove."""
    over = PY_OVER_BUDGET if over is None else over
    budget = (PY_LINE_BUDGET, PY_BYTE_BUDGET) if budget is None else budget
    problems = []
    for name, size in sorted(sizes.items()):
        limit = over.get(name, budget)
        for what, have, most in zip(('lines', 'bytes'), size, limit):
            if have > most:
                hint = ('split it (docs/code-map.md); the ceiling in PY_OVER_BUDGET only comes down' if name in over
                        else 'split it into modules (docs/code-map.md)')
                problems.append(f'{name} has {have} {what}, over {most}: {hint}')
    for name, limit in sorted(over.items()):
        size = sizes.get(name)
        if size is None:
            problems.append(f'{name} is gone: take it out of PY_OVER_BUDGET')
            continue
        if all(have <= most for have, most in zip(size, budget)):
            problems.append(f'{name} is within the budget now ({size[0]} lines, {size[1]} bytes): take it out of '
                            'PY_OVER_BUDGET')
            continue
        for what, have, most, room, base in zip(('lines', 'bytes'), size, limit, slack, budget):
            if most > base and have < most - room:
                problems.append(f'{name} is down to {have} {what}: lower its ceiling in PY_OVER_BUDGET from {most} to '
                                f'about {have}')
    return problems


def shipped_sizes():
    skip = {'.git', 'node_modules', 'tests', '__pycache__'}
    return {str(path.relative_to(ROOT)): path.stat().st_size for path in ROOT.rglob('*')
            if path.suffix in {'.html', '.css', '.js', '.mjs'} and path.is_file() and not skip & set(path.relative_to(ROOT).parts)}


class Architecture(unittest.TestCase):
    def test_every_global_name_is_defined_or_imported(self):
        for name in python_files():
            with self.subTest(module=name):
                missing = undefined_names((ROOT / name).read_text(encoding='utf-8'), name)
                self.assertEqual(missing, [], f'{name} uses names it never defines or imports (name, first line): '
                                              f'{missing}. Import them where the code now lives.')

    def test_the_name_check_finds_what_a_move_leaves_behind(self):
        source = ('import os\nX = 1\ndef f(a):\n    global Y\n    Y = 2\n    return os, X, Y, gone(a), [z for z in a if q]\n'
                  'class C:\n    attr = in_class\n    def m(self):\n        return C, (lambda: in_lambda)\n'
                  'def g():\n    def inner():\n        return outer + deep\n    outer = 1\n    return inner\n')
        self.assertEqual(undefined_names(source), [('deep', 13), ('gone', 6), ('in_class', 8), ('in_lambda', 10), ('q', 6)])

    def test_no_new_module_loads_assistant(self):
        found = {}
        for name in python_files(tests=False):
            if name == 'assistant.py':
                continue
            lines = loads_module(nodes(name), lambda m: m == 'assistant')
            if lines:
                found[name] = lines
        new = sorted(set(found) - set(LOADS_ASSISTANT))
        self.assertEqual(new, [], f'{new} load assistant.py (lines {[found[n] for n in new]}). Nothing new may: move what '
                                  'they need out of assistant.py into a module both import (docs/code-map.md).')
        gone = sorted(set(LOADS_ASSISTANT) - set(found))
        self.assertEqual(gone, [], f'{gone} no longer load assistant.py: remove them from LOADS_ASSISTANT in this file.')

    def test_only_assistant_imports_the_app_mixins(self):
        for name in python_files(tests=False):
            if name == 'assistant.py':
                continue
            lines = loads_module(nodes(name), lambda m: m.endswith('_app'))
            with self.subTest(module=name):
                self.assertEqual(lines, [], f'{name} imports a *_app module (App methods); only assistant.py composes them')

    def test_each_table_is_created_by_one_module(self):
        creates, _ = schema_and_writes()
        for table, modules in sorted(creates.items()):
            with self.subTest(table=table):
                if table in SHARED_SCHEMA:
                    first, others = SHARED_SCHEMA[table]
                    self.assertEqual(set(modules), {first} | others, f'{table}: update SHARED_SCHEMA in this file')
                else:
                    self.assertEqual(len(modules), 1, f'{table} is created in {sorted(modules)}. One module owns a table '
                                                      'and creates it in its ensure(db); the others call that.')

    def test_only_the_owner_writes_a_table(self):
        creates, writes = schema_and_writes()
        for table, modules in sorted(writes.items()):
            first = owner(table, creates)
            with self.subTest(table=table):
                self.assertIsNotNone(first, f'{table} is written ({sorted(modules)}) but no module creates it')
                for module, line in sorted(modules.items()):
                    if module != first and module not in OTHER_WRITERS.get(table, ()):
                        if table == 'events':
                            self.fail(f'{module}:{line} writes events, the sealed table: only assistant.py may '
                                      '(tests/test_message_seal.py). Call the Store method that does it.')
                        self.fail(f'{module}:{line} writes table {table}, which {first} owns. Call a function of '
                                  f'{first} that does it (add one there if needed). Only if that can\'t be, add '
                                  f'{module!r} to OTHER_WRITERS[{table!r}] in tests/test_architecture.py and say why '
                                  'in the pull request (docs/code-map.md).')

    def test_listed_other_writers_still_write(self):
        creates, writes = schema_and_writes()
        for table, modules in sorted(OTHER_WRITERS.items()):
            with self.subTest(table=table):
                stale = sorted(modules - set(writes.get(table, {})))
                self.assertEqual(stale, [], f'{stale} no longer write {table}: remove them from OTHER_WRITERS[{table!r}]')
                self.assertNotIn(owner(table, creates), modules, f'{table}: its owner is listed as another writer')

    def test_the_table_scan_sees_writes(self):
        tree = ast.parse('def f(db):\n    """INSERT INTO docs_only"""\n    db.execute("INSERT OR REPLACE INTO a(x) VALUES(1)")\n'
                         '    db.execute(f"UPDATE b SET x={1} WHERE y=1")\n    db.execute("DELETE FROM temp.c")\n'
                         '    db.execute("REPLACE INTO d VALUES(1)")\n    db.execute("UPDATE OR IGNORE e SET x=1 ON CONFLICT DO UPDATE SET x=2")\n')
        found = sorted(m.group(1) or m.group(2) for _, text in sql_strings(list(ast.walk(tree))) for m in WRITE.finditer(text)
                       if text[m.end():m.end() + 1] != '.')
        self.assertEqual(found, ['a', 'b', 'd', 'e'])

    def test_shipped_pages_and_scripts_stay_small_enough_to_scan(self):
        sizes = shipped_sizes()
        self.assertIn('dashboard.html', sizes)
        for name, size in sizes.items():
            with self.subTest(file=name):
                limit = OVER_BUDGET.get(name, budget(name))
                part = ' into another <area>-<what> part next to it (docs/code-map.md)' if name.startswith('dashboard') else ''
                self.assertLessEqual(size, limit, f'{name} is {size} bytes, over {limit}: split it{part} (the scanner skips '
                                                  'big files, and small parts merge and review better)')
        for name, ceiling in OVER_BUDGET.items():
            with self.subTest(listed=name):
                self.assertGreater(sizes.get(name, 0), budget(name), f'{name} is under its budget now: take it out of OVER_BUDGET')
                self.assertGreater(ceiling, budget(name))
        self.assertEqual(budget('dashboard/todos-x.css'), 64 * 1024)
        self.assertEqual(budget('dashboard/todos-x.html'), 32 * 1024)
        self.assertEqual(budget('dashboard/todos-x.js'), 160 * 1024)
        self.assertEqual(budget('sw.js'), SCAN_LIMIT)

    def test_the_served_dashboard_stays_under_its_ceiling(self):
        size = len(dashboard_parts.assemble(ROOT).encode('utf-8'))
        self.assertLessEqual(size, PAGE_CEILING, f'The dashboard page as served is {size} bytes, over PAGE_CEILING '
                                                 f'({PAGE_CEILING}): every phone downloads it. Make it smaller, or raise '
                                                 'the ceiling on purpose in a pull request that says why.')

    def test_python_files_stay_within_the_budget(self):
        sizes = python_sizes()
        self.assertIn('assistant.py', sizes)
        self.assertEqual(py_budget_problems(sizes), [])

    def test_the_budget_is_a_ratchet(self):
        over, budget, slack = {'big.py': (3000, 100)}, (2500, 100), (200, 20)
        check = functools.partial(py_budget_problems, over=over, budget=budget, slack=slack)
        self.assertEqual(check({'big.py': (2950, 50), 'small.py': (2500, 100)}), [])
        self.assertIn('over 3000', check({'big.py': (3001, 50)})[0])          # it grew
        self.assertIn('over 2500', check({'big.py': (2950, 50), 'new.py': (2501, 10)})[0])  # a new one too big
        self.assertIn('over 100', check({'big.py': (2950, 50), 'new.py': (10, 101)})[0])
        self.assertIn('lower its ceiling', check({'big.py': (2700, 50)})[0])  # it shrank: the ceiling follows
        self.assertIn('take it out', check({'big.py': (2400, 50)})[0])        # back within the budget
        self.assertIn('is gone', check({})[0])

    def test_machine_modules_import_down_the_layers(self):
        for name in python_files(tests=False):
            if name.startswith('machine/'):
                with self.subTest(module=name):
                    self.assertEqual(machine_layer_problems(name, (ROOT / name).read_text(encoding='utf-8')), [])

    def test_the_layer_check_finds_upward_imports(self):
        found = machine_layer_problems('machine/sources/slack.py', (
            'import os\nimport graph\nfrom machine import config\nfrom machine.text import x\nfrom . import gmail\n'
            'from .gmail import y\nfrom ..store import Store\nimport machine.web.handler\nfrom machine import app, text\n'
            'def f():\n    from machine.delivery import push\n    from machine.nowhere import z\nfrom machine.chat import *\n'))
        self.assertEqual([line for line, _ in found], [7, 8, 9, 11, 12, 13], found)
        self.assertIn('layer 1) imports machine.store (layer 2)', found[0][1])
        self.assertEqual(machine_layer_problems('machine/store/__init__.py', 'from . import cards\nfrom .. import config\n'), [])
        self.assertIn('no layer', machine_layer_problems('machine/newthing.py', 'x = 1\n')[0][1])
        self.assertTrue(machine_layer_problems('machine/__init__.py', 'from . import store\n'))
        self.assertEqual(machine_layer_problems('machine/__init__.py', ''), [])

    def test_the_tools_that_read_the_code_see_machine(self):
        """The help chat, help_check and the string extractor read the app's code in machine/ too."""
        import tempfile
        sys.path[:0] = [str(ROOT), str(ROOT / 'scripts')]
        import help_chat
        import help_check
        import i18n_extract
        with tempfile.TemporaryDirectory() as tmp:
            folder = pathlib.Path(tmp) / 'machine' / 'sources'
            folder.mkdir(parents=True)
            (folder / 'mail.py').write_text('"""Reads the mail."""\n\ndef sync():\n    raise ValueError(\'The mailbox is not there\')\n')
            self.assertIn('machine/sources/mail.py', [s['path'] for s in help_chat.code_snippets(tmp)])
            self.assertIn('The mailbox is not there', i18n_extract.server_strings(pathlib.Path(tmp)).get('machine/sources/mail.py', []))
        self.assertIn('machine/**/*.py', help_check.TEXT_FILES)
        import inspect
        self.assertIn("glob('machine/**/*.py')", inspect.getsource(help_check.app_files))

    def test_every_i18n_area_resolves(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        import i18n_extract
        source = i18n_extract.dashboard_parts.assemble(ROOT)
        for area in i18n_extract.AREAS:
            with self.subTest(area=area):
                self.assertTrue(i18n_extract.area_strings(area, source), f'area {area} finds no strings')


def owners_report():
    creates, writes = schema_and_writes()
    tables = {}
    for table in sorted(set(creates) | set(writes)):
        tables.setdefault(owner(table, creates) or '(none)', []).append(table)
    return '\n'.join(f'{module} ({len(names)}): {", ".join(names)}' for module, names in sorted(tables.items()))


if __name__ == '__main__':
    if sys.argv[1:] == ['--owners']:
        print(owners_report())
    else:
        unittest.main()
