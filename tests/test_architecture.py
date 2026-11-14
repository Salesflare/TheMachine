"""Guards for the code layout (docs/code-map.md): what keeps code moving between modules safe while assistant.py is
split up. Static checks of the source only; nothing is imported or run.

- every module defines or imports each global name it uses, so a function moved without its import fails here and
  not with a NameError at runtime;
- no module loads assistant.py except the entry points that do so today (tests may);
- each table is created by one module, its owner, and written only by its owner, apart from the writers listed in
  OTHER_WRITERS as they are today;
- modules in machine/ import only from their own layer or the ones below it (MACHINE_LAYERS), never `*`;
- to-do statuses are named from machine/todo_states.py, never spelled out as a list in code or SQL;
- only timeutil.py reads the real clock (datetime.now, date.today), apart from today's reads in tests/clock_reads.json,
  whose counts only come down;
- Python files stay under PY_LINE_BUDGET lines and PY_BYTE_BUDGET bytes, apart from today's bigger ones in
  PY_OVER_BUDGET, whose ceilings only come down;
- i18n_extract's dashboard AREAS all resolve.

`python3 tests/test_architecture.py --owners` prints each module with the tables it owns."""
import ast
import builtins
import functools
import gzip
import json
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
    'kinds': 0,        # every kind of event and of message, with what the code knows of each (a leaf)
    'names': 0,        # what the owner calls a service, app or agent (never the tool underneath)
    'omarchy': 0,      # the Omarchy desktop theme's colors, read only (a leaf)
    'owner_error': 0,  # OwnerError: a message for the owner, not a bug (a leaf)
    'stamps': 0,       # change counters per table, so a request's answer is kept until its tables change
    'system_logs': 0,  # the computer's own logs: journald and crash dumps, read only
    'text': 0,         # message parsing
    'timing': 0,       # request timing, shared by web and store
    'todo_states': 0,  # every to-do status and its named groups (a leaf)
    'browser': 1,
    'cards': 1,
    'chat': 1,
    'faults': 1,
    'model_usage': 1,
    'prompts': 1,
    'sources': 1,
    'store': 2,
    'graph': 2,        # the Graph build's passes (graph.build): one function each, imports none of machine/
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


# --- to-do statuses --------------------------------------------------------------------------------------------------

# machine/todo_states.py declares every to-do status and the groups the code asks about. Two or more of them spelled
# out somewhere else, as a tuple, list or set, or as an SQL IN list in a string, is a second definition that can drift
# from the first: name a group from todo_states there (a new one, with its reason, when a module means something else).
TODO_STATES_FILE = 'machine/todo_states.py'
TODO_STATUSES = {'pending', 'accepted', 'prepared', 'instructions', 'snoozed', 'completed', 'rejected'}
SQL_WORD_LIST = re.compile(r"\(\s*'[a-z_]+'(?:\s*,\s*'[a-z_]+')+\s*\)")


def todo_status_literals(source, filename='<module>'):
    """[(line, literal)] of to-do status lists spelled out in a module's code or its SQL strings."""
    found = []
    for node in ast.walk(ast.parse(source, filename)):
        if isinstance(node, (ast.Tuple, ast.List, ast.Set)) and len(node.elts) >= 2 and all(
                isinstance(e, ast.Constant) and isinstance(e.value, str) and e.value in TODO_STATUSES for e in node.elts):
            found.append((node.lineno, ast.unparse(node)))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            for match in SQL_WORD_LIST.finditer(node.value):
                if set(re.findall(r"'([a-z_]+)'", match.group(0))) <= TODO_STATUSES:
                    found.append((node.lineno, match.group(0)))
    return sorted(found)


# --- the clock -------------------------------------------------------------------------------------------------------

# timeutil.clock() is the one place the app reads the current time, so a test can pin it (tests/pinned.py). Anywhere
# else, datetime.now(), datetime.utcnow(), datetime.today() and date.today() read the real clock past the pin: use
# timeutil.clock() (aware, UTC by default; clock(None) is naive local time) and timeutil.today(). Tests, scripts/ and
# sandbox/ (tools run beside the app; the sandbox can drive an older installed app) may read it. CLOCK_READS_FILE lists
# today's direct reads per file until they move; its counts only come down.
CLOCK_FILE = 'timeutil.py'
CLOCK_READS_FILE = 'tests/clock_reads.json'
CLOCK_FREE_DIRS = ('tests/', 'scripts/', 'sandbox/')


def clock_reads(tree_nodes):
    """Lines that read the real clock directly: datetime.now / utcnow / today and date.today, called or passed on."""
    found = []
    for node in tree_nodes:
        if isinstance(node, ast.Attribute) and node.attr in ('now', 'utcnow', 'today'):
            owner = node.value.attr if isinstance(node.value, ast.Attribute) else getattr(node.value, 'id', None)
            if owner == 'datetime' or (owner == 'date' and node.attr == 'today'):
                found.append(node.lineno)
    return sorted(found)


def clock_reading_files():
    """{file: direct reads of the real clock} for the files the clock rule covers."""
    out = {}
    for name in python_files(tests=False):
        if name != CLOCK_FILE and not name.startswith(CLOCK_FREE_DIRS):
            count = len(clock_reads(nodes(name)))
            if count:
                out[name] = count
    return out


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
    'action_jobs': {'follow_ups.py', 'machine/app/action_runs.py', 'machine/app/preparation.py',
                    'machine/export/hold.py'},
    'agent_jobs': {'agent_remote.py', 'assistant.py', 'sandbox/load.py'},
    'agent_result_receipts': {'agent_remote.py'},
    'analyses': {'graph.py', 'machine/app/review.py', 'sandbox/load.py', 'work_removal.py'},
    'board_backfill_asks': {'graph_board_reviews.py'},  # a review's board checks, moved out of graph.py (its line budget)
    'board_backfills': {'graph_board_reviews.py', 'sandbox/load.py'},
    'board_fit_undo': {'graph_board_reviews.py'},
    'board_fits': {'graph_board_reviews.py'},
    'board_offers': {'assistant.py'},
    'boards': {'shared_graph.py'},
    'calendar_writes': {'machine/app/meeting_writes.py'},
    'chats': {'telegram_mirror.py'},
    'checkpoints': {'machine/app/sync.py', 'sandbox/load.py'},
    'crm_tags': {'crm_import.py'},
    'decisions': {'follow_ups.py', 'graph.py', 'machine/app/action_runs.py', 'machine/app/follow_ups.py',
                  'machine/store/faults.py', 'sandbox/load.py', 'work_removal.py'},
    'deliveries': {'fleet.py', 'follow_ups.py', 'machine/app/action_runs.py', 'machine/app/browser.py',
                   'machine/app/card_actions.py', 'machine/app/follow_ups.py', 'machine/app/preparation.py',
                   'machine/delivery/deliver.py', 'machine/export/hold.py', 'machine/store/faults.py',
                   'sandbox/load.py', 'skills_app.py'},
    'draft_edits': {'graph.py'},
    'edits_offered': {'machine/app/review.py'},
    'enrich_prefs': {'security_levels.py'},
    'event_projects': {'graph_board_reviews.py', 'project_split.py'},  # Split up moves threads between projects (graph.py is at its line budget); graph_board_reviews: Add on a maybe
    'event_search': {'assistant.py'},
    'events': {'sandbox/load.py', 'work_removal.py'},
    'facts': {'learning_loop.py', 'skills_app.py'},
    'fault_versions': {'machine/store/faults.py'},
    'faults': {'machine/store/faults.py'},
    'feedback_prompts': {'machine/app/feedback.py'},
    'fleet_briefs': {'sandbox/run.py'},
    'fleet_in': {'fleet_requests.py'},
    'fleet_learn_read': {'shared_graph.py'},
    'fleet_learn_removed': {'shared_graph.py'},
    'fleet_learn_seen': {'shared_graph.py'},
    'fleet_learnings': {'shared_graph.py'},
    'fleet_meta': {'family.py', 'fleet_requests.py', 'security_levels.py', 'shared_graph.py'},
    'fleet_rules': {'fleet_requests.py'},
    'graph_events': {'graph_publish.py'},  # a build's publish, as the changes only (graph.py is at its line budget)
    'graph_imports': {'crm_import.py'},
    'graph_links': {'graph_publish.py', 'graph_show.py', 'project_split.py'},  # an edit on its page before the next build (graph.py is at its line budget); project_split: a person taken off a project it splits up
    'graph_names': {'crm.py', 'crm_import.py'},
    'graph_nodes': {'crm.py', 'crm_fields.py', 'graph_publish.py', 'graph_show.py'},
    'graph_offers': {'assistant.py'},
    'graph_org_asks': {'assistant.py'},
    'graph_role_asks': {'assistant.py'},
    'graph_same': {'graph_publish.py'},
    'graph_unnamed': {'graph_publish.py'},
    'identity_names': {'assistant.py'},
    'manual_nodes': {'crm_import.py'},
    'meeting_moves': {'assistant.py'},
    'meeting_writes': {'machine/app/meeting_writes.py'},
    'merge_effects': {'machine/app/action_runs.py'},
    'messages': {'telegram_mirror.py'},
    'milestones': {'machine/app/first_look.py', 'machine/app/preparation.py'},
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
    'preparation_runs': {'assistant.py', 'machine/app/action_runs.py', 'machine/app/preparation.py'},
    'preparations': {'follow_ups.py', 'machine/app/action_runs.py', 'machine/app/preparation.py',
                     'preparation_state.py'},
    'profile_runs': {'fleet_learnings.py', 'learning_loop.py', 'machine/app/card_actions.py', 'machine/app/fleet.py',
                     'machine/app/profile.py', 'retention.py', 'skills_app.py', 'team_learnings.py'},
    'project_moves': {'crm_import.py', 'follow_ups.py'},
    'project_people': {'project_split.py'},  # Split up moves people between projects (graph.py is at its line budget)
    'projects': {'crm.py', 'crm_import.py', 'follow_ups.py', 'graph_board_reviews.py', 'machine/app/graph_actions.py', 'project_about.py', 'project_org_checks.py', 'project_split.py', 'sandbox/load.py'},  # project_about: only its about_* columns; project_org_checks: org, org_by; project_split: the projects it makes, on the original's board
    'promises': {'graph.py', 'machine/app/mail.py', 'machine/app/promise_checks.py', 'sandbox/load.py'},
    'push_subscriptions': {'machine/app/notifications.py', 'machine/delivery/push.py', 'machine/export/hold.py'},
    'recap_items': {'machine/app/recap.py'},
    'recaps': {'machine/app/recap.py'},
    'record_owners': {'crm_import.py'},
    'review_runs': {'machine/app/review.py', 'sandbox/load.py'},
    'rule_changes': {'learning_loop.py', 'machine/app/recap.py', 'skills_app.py'},
    'skill_clusters': {'skills_app.py'},
    'skills': {'sandbox/load.py'},
    'suggestions': {'fleet.py', 'follow_ups.py', 'graph.py', 'machine/app/action_runs.py', 'machine/app/feedback.py',
                    'machine/app/mail.py', 'machine/app/new_cards.py', 'machine/app/promise_checks.py',
                    'machine/delivery/deliver.py', 'machine/store/faults.py', 'sandbox/load.py', 'skills_app.py',
                    'work_removal.py'},
    'sync_activity': {'retention.py', 'sandbox/load.py'},
    'team_learning_prefs': {'security_levels.py'},
    'thread_snoozes': {'machine/app/action_runs.py', 'machine/app/workers.py'},
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
               'machine/store/facts.py', 'machine/store/first_look.py', 'machine/store/machine_cards.py', 'machine/store/profile.py', 'machine/store/promises.py',
               'machine/store/review.py', 'machine/store/views.py', 'machine/store/voices.py', 'machine/store/whats_new.py',
               'machine/store/done_milestones.py', 'machine/store/outcomes.py',
               'machine/main.py'}  # Store and App themselves, out of assistant.py


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
# What a phone downloads before To-dos shows: the first load (the page and its main script, without the parts that load
# when first needed, dashboard_parts.LAZY), and each of those groups when it's first opened. Counted as gzip of the text
# without its whole-line comments (served_size), so a comment costs nothing and only shipped code counts.
# dashboard/budgets.json holds their budgets: about 3% over the size when they were set (at least 500 bytes). They don't
# follow the size down; a weekly look can lower them. Don't raise one for a feature: a new page, panel, dialog or
# anything that only runs once the owner opens or clicks something goes in a part that loads when first needed
# (dashboard_parts.LAZY, lazyRun in shell-core.js). Only a change to what To-dos draws first raises the first load's,
# on purpose, in a pull request that says why. Their history is in git.
SIZE_BUDGETS = ROOT / 'dashboard' / 'budgets.json'
WHOLE_LINE_COMMENT = re.compile(r'^[ \t]*(?://[^\n]*|/\*(?:[^*]|\*(?!/))*\*/[ \t]*)\n', re.M)


def served_size(text):
    """Bytes of text gzipped (level 9, as the service compresses it at best), without its whole-line // and /* */
    comments: what a change adds to a download, comments aside. The page itself is served with them (a measure, not
    a minifier)."""
    return len(gzip.compress(WHOLE_LINE_COMMENT.sub('', text).encode('utf-8'), 9, mtime=0))


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
    'fleet.py': (3_800, PY_BYTE_BUDGET),
    'graph.py': (4_300, PY_BYTE_BUDGET),
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
            if name in ('assistant.py', 'machine/main.py'):  # main.py composes App; assistant.py re-exports the mixins
                continue
            lines = loads_module(nodes(name), lambda m: m.endswith('_app'))
            with self.subTest(module=name):
                self.assertEqual(lines, [], f'{name} imports a *_app module (App methods); only machine/main.py composes them')

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
                            self.fail(f'{module}:{line} writes events, the sealed table: only the Store and App may '
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

    def test_the_served_dashboard_stays_under_its_ceilings(self):
        budgets = json.loads(SIZE_BUDGETS.read_text(encoding='utf-8'))
        first, lazy = dashboard_parts.assemble_split(ROOT)
        size = served_size(first)
        self.assertLessEqual(size, budgets['first_load'], f'The dashboard\'s first load is {size} bytes gzipped, over '
                             f'its budget ({budgets["first_load"]}, first_load in dashboard/budgets.json): every phone '
                             'downloads it before To-dos shows. Make it smaller, load a part when first needed '
                             '(dashboard_parts.LAZY), or raise the budget on purpose in a pull request that says why.')
        self.assertEqual(sorted(lazy), sorted(budgets['lazy']), 'every LAZY group has a budget in dashboard/budgets.json')
        for group, script in lazy.items():
            with self.subTest(group=group):
                size = served_size(script)
                self.assertLessEqual(size, budgets['lazy'][group], f'The {group} part that loads when first needed is '
                                     f'{size} bytes gzipped, over its budget ({budgets["lazy"][group]}, in '
                                     'dashboard/budgets.json): make it smaller, or raise its budget on purpose in a '
                                     'pull request that says why.')

    def test_the_size_measure_leaves_out_whole_line_comments_only(self):
        code = 'let a = 1; // kept: not a whole line\nconst u = "http://x";\n'
        commented = ('  // a whole-line comment\n' + code + '/* one\n   more */\n\t/* a rule */  \n'
                     '/* not whole */ b();\n')
        self.assertEqual(WHOLE_LINE_COMMENT.sub('', commented), code + '/* not whole */ b();\n')
        self.assertEqual(served_size(commented), served_size(code + '/* not whole */ b();\n'))
        self.assertLess(served_size(code), served_size(code + 'b();\n'))

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

    def test_todo_statuses_are_named_from_todo_states(self):
        for name in python_files(tests=False):
            if name != TODO_STATES_FILE:
                with self.subTest(module=name):
                    self.assertEqual(todo_status_literals((ROOT / name).read_text(encoding='utf-8'), name), [],
                                     f'{name}: name a group from {TODO_STATES_FILE} instead')

    def test_the_todo_status_check_finds_spelled_out_lists(self):
        found = todo_status_literals(
            "OPEN = ('pending', 'snoozed')\nif s in ['completed', 'rejected']:\n    pass\n"
            "db.execute(\"SELECT id FROM suggestions WHERE status IN ('accepted','instructions')\")\n"
            "db.execute(f\"SELECT 1 WHERE s.status NOT IN ('completed','rejected') AND x={x}\")\n"
            "ok = ('snoozed',), ('queued', 'running'), (todo_states.PENDING, todo_states.PREPARED)\n"
            "db.execute(\"SELECT 1 WHERE status IN ('pending','declined')\")\n")
        self.assertEqual([line for line, _ in found], [1, 2, 4, 5], found)
        sys.path.insert(0, str(ROOT))
        from machine import todo_states
        self.assertEqual(set(todo_states.ALL), TODO_STATUSES)
        self.assertEqual(todo_states.sql(todo_states.NOT_STARTED, todo_states.REJECTED), "('pending','snoozed','rejected')")
        with self.assertRaises(ValueError):
            todo_states.sql('pending', "x') OR 1=1 --")

    def test_only_timeutil_reads_the_clock(self):
        allowed = json.loads((ROOT / CLOCK_READS_FILE).read_text(encoding='utf-8'))
        found = clock_reading_files()
        for name in sorted(set(found) | set(allowed)):
            with self.subTest(module=name):
                count, ceiling = found.get(name, 0), allowed.get(name, 0)
                self.assertLessEqual(count, ceiling, f'{name}: read the time with timeutil.clock() or timeutil.today(), '
                                                     'not datetime.now() or date.today(), so tests can pin it')
                self.assertEqual(count, ceiling, f'{name} reads the real clock {count} times now: set that in '
                                                 f'{CLOCK_READS_FILE} (take it out at 0)')

    def test_the_clock_check_finds_direct_reads(self):
        source = ('import datetime as dt\nfrom datetime import date, datetime\nimport timeutil\n'
                  'a = dt.datetime.now(dt.timezone.utc)\nb = datetime.now()\nc = dt.date.today()\nd = date.today()\n'
                  'e = dt.datetime.utcnow()\nf = sorted(xs, key=dt.datetime.now)\ng = timeutil.clock()\n'
                  'h = timeutil.today()\ni = dt.datetime.fromisoformat(x).date()\nj = self.now()\nk = today\n')
        self.assertEqual(clock_reads(ast.walk(ast.parse(source))), [4, 5, 6, 7, 8, 9])

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

    def test_every_name_the_string_extractor_reads_is_in_its_file(self):
        """SERVER_TEXT and CAPITALIZED name constants and functions by file: one that moves must move there too."""
        sys.path.insert(0, str(ROOT / 'scripts'))
        import i18n_extract
        for table in (i18n_extract.SERVER_TEXT, i18n_extract.CAPITALIZED):
            for path, names in table.items():
                tree = ast.parse((ROOT / path).read_text(encoding='utf-8'))
                defined = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
                defined |= {t.id for n in tree.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}
                with self.subTest(path=path):
                    self.assertEqual([n for n in names if n not in defined], [], f'not defined in {path}: update i18n_extract')

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
