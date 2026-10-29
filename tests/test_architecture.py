"""Guards for the code layout (docs/code-map.md): what keeps code moving between modules safe while assistant.py is
split up. Static checks of the source only; nothing is imported or run.

- every module defines or imports each global name it uses, so a function moved without its import fails here and
  not with a NameError at runtime;
- no module loads assistant.py except the entry points that do so today (tests may);
- each table is created by one module, its owner, and written only by its owner, apart from the writers listed in
  OTHER_WRITERS as they are today;
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
    'work_removal.py': 'lazy, for Store, credential and gog_token_path',
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
    'action_jobs': {'follow_ups.py'},
    'agent_jobs': {'agent_remote.py', 'assistant.py', 'sandbox/load.py'},
    'agent_result_receipts': {'agent_remote.py'},
    'analyses': {'graph.py', 'sandbox/load.py', 'work_removal.py'},
    'board_backfills': {'sandbox/load.py'},
    'board_offers': {'assistant.py'},
    'boards': {'shared_graph.py'},
    'chats': {'telegram_mirror.py'},
    'checkpoints': {'sandbox/load.py'},
    'crm_tags': {'crm_import.py'},
    'decisions': {'follow_ups.py', 'graph.py', 'sandbox/load.py', 'work_removal.py'},
    'deliveries': {'fleet.py', 'follow_ups.py', 'sandbox/load.py'},
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
    'follow_up_cards': {'assistant.py'},
    'follow_up_holds': {'assistant.py'},
    'follow_up_threads': {'assistant.py'},
    'graph_imports': {'crm_import.py'},
    'graph_names': {'crm.py', 'crm_import.py'},
    'graph_nodes': {'crm.py', 'crm_fields.py'},
    'graph_offers': {'assistant.py'},
    'graph_org_asks': {'assistant.py'},
    'graph_role_asks': {'assistant.py'},
    'identity_names': {'assistant.py'},
    'manual_nodes': {'crm_import.py'},
    'meeting_moves': {'assistant.py'},
    'meeting_writes': {'assistant.py'},
    'messages': {'telegram_mirror.py'},
    'network_people': {'graph.py'},
    'network_request_nodes': {'network.py'},
    'notify_digests': {'assistant.py'},
    'notify_queue': {'assistant.py'},
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
    'profile_runs': {'fleet_learnings.py', 'learning_loop.py', 'retention.py', 'team_learnings.py'},
    'project_moves': {'crm_import.py', 'follow_ups.py'},
    'projects': {'assistant.py', 'crm.py', 'crm_import.py', 'follow_ups.py', 'sandbox/load.py'},
    'promises': {'graph.py', 'sandbox/load.py'},
    'record_owners': {'crm_import.py'},
    'review_runs': {'sandbox/load.py'},
    'rule_changes': {'learning_loop.py'},
    'skills': {'sandbox/load.py'},
    'suggestions': {'fleet.py', 'follow_ups.py', 'graph.py', 'sandbox/load.py', 'work_removal.py'},
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


@functools.lru_cache(maxsize=None)
def schema_and_writes():
    """({table: {module: line}} of CREATE TABLE, {table: {module: line}} of INSERT/REPLACE/UPDATE/DELETE), for every
    module outside tests/. Statements with a computed table name (f'DELETE FROM {table}') aren't seen."""
    creates, writes = {}, {}
    for name in python_files(tests=False):
        for line, text in sql_strings(nodes(name)):
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

    def test_every_i18n_area_resolves(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        import i18n_extract
        source = i18n_extract.DASHBOARD.read_text(encoding='utf-8')
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
