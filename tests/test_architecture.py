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
    'omarchy': 0,      # the Omarchy desktop theme's colors, read only (a leaf)
    'stamps': 0,       # change counters per table, so a request's answer is kept until its tables change
    'system_logs': 0,  # the computer's own logs: journald and crash dumps, read only
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
# The page as served (dashboard.html with its parts): what a phone downloads. Not a scan rule, a watch: a ceiling that
# may only come down; raise it on purpose, in a pull request that says why.
# 2,000,000 -> 2,100,000 (2026-11-07): main passed 2,000,000 with no single big piece to take out (no inline assets,
# no string table). The real fix is the dashboard split of the code refactor (load parts when they're used); this is
# headroom while that lands, so main stays green. Bring it back down with the split.
# 2,100,000 -> 2,110,000 (2026-11-08): the Routines page (about 7.7 KB) is a whole new page; the split loads it
# only when opened, and brings this back down.
# Also Connections › Add redesign (Jeroen picked A); split of the dashboard into on-demand parts follows.
# 2,110,000 -> 2,120,000 (2026-11-08): Routines took the headroom meant for the + Add redesign (about 6.5 KB, logos
# already moved out to files). Same reason: the split brings this back down.
# 2,120,000 -> 2,100,000 (2026-11-08): the ceiling is the first load now, the page and its main script without the
# parts that load when first needed (dashboard_parts.LAZY); each of those groups has a ceiling of its own.
# 2,100,000 -> 2,040,000 (2026-11-08): Calendar and Learning load when first needed too (about 78 KB off the first load).
# 1,770,000 -> 1,774,000 (2026-11-08): "Connect your mail" first (#936, 0.7 KB over on main) and setup picks up where
# it left off (#963, about 2.9 KB after trimming its comments).
# 1,774,000 -> 1,775,000 (2026-11-09): main was already 0.1 KB over (#997), and a routine's recipe shows read-only
# under Advanced (about 0.5 KB after trimming).
# 1,775,000 -> 1,698,000 (2026-11-09): Settings' general, export and upkeep panels load when first needed (first load
# 1,774,595 -> 1,696,442).
# 1,698,000 -> 1,700,000 (2026-11-09): Work or Personal from the address (about 1.7 KB): the line that says what it was
# set to, with Change, and the setup to-do's row when the mail says the other. The company field and its autofill stay:
# Zoom, Teams and Google Meet still ask an address and a company up front.
# 1,700,000 -> 1,614,000 (2026-11-09): the Fleet tab's views load when first needed (first load 1,698,510 -> 1,612,616).
# 1,614,000 -> 1,527,000 (2026-11-09): the Connections tab's views load when first needed (first load 1,612,918 ->
# 1,525,351).
# 1,527,000 -> 1,491,000 (2026-11-09): Settings' Skills panel loads when first needed, with Settings' other panels (first
# load 1,525,351 -> 1,489,064).
# 1,491,000 -> 1,494,000 (2026-11-09): the sidebar to-do menu's Mark done, Snooze and Not needed, with keyboard use and
# placement on a phone (about 3 KB after trimming); main was 1.3 KB under.
# 1,494,000 -> 1,497,000 (2026-11-09): a routine's to-do names its routine with a link to it and its step on the button,
# on To-dos itself (about 2.5 KB; first load 1,496,486).
# 1,497,000 -> 1,500,000 (2026-11-09): a Fixed line asks Works now or Still not right, with a close; the box for what is
# still off and its image load with Help (about 3.3 KB of buttons and styles; first load 1,499,738).
# 1,500,000 -> 1,502,000 (2026-11-09): a routine's to-do offers Also change the routine, on To-dos itself (about 1.8 KB;
# first load 1,501,675).
# 1,502,000 -> 1,504,000 (2026-11-09): Edit names a routine too, in its title's place (about 1.3 KB; first load 1,502,991).
# +300 (2026-11-09): a suggested routine also says what it saw for forwards and replies, on Routines (1,504,300).
# 1,504,300 -> 1,423,000 (2026-11-09): Routines, Talk's session and Calendar's rules load when first needed, and more of
# the Graph's rules wait for its part (first load about 1,503,000 -> 1,417,982).
# Don't raise this for a feature: a new page, panel, dialog or anything that only runs once the owner opens or clicks
# something goes in a part that loads when first needed (dashboard_parts.LAZY, lazyRun in shell-core.js), and what
# To-dos draws first stays small. Only a change to that first draw itself may raise it, saying why.
# 2026-11-09: main had reached this ceiling (1,423,014, then 1,421,700). Settings' Connected AIs and Apps panels
# (settings-ai.js, settings-ai.css, settings-apps.js) load when first needed, with Settings' other panels (first load
# 1,421,700 -> 1,406,533). The ceiling stays: the room is for what's queued.
# 2026-11-10: main was over again (1,423,060). Go through's dialog (todos-clear-run.js and its rules) loads when first
# needed; the header's Go through and its time stay (first load 1,423,060 -> 1,415,719). The ceiling stays.
# 1,423,000 -> 1,391,000 (2026-11-11): main sat a few hundred bytes under it and every UI change hit it. A follow-up
# group's fast review (LAZY 'followups'), a project's follow-ups and Done when, a board's follow-ups line and the
# follow-up settings dialog (the Graph's part) load when first needed (first load 1,421,711 -> 1,380,493). The
# ceiling is that plus 10 KB, and FIRST_LOAD_ROOM keeps it close: room that opens up is taken in.
# 1,391,000 -> 1,392,000 (2026-11-12): main sat 9 bytes under it. A Daily digest's place in the list itself (its To
# read chip, Done as its first button, not counted as needing the owner) is first draw (+561); its items load when
# first needed (LAZY 'digest').
# 1,392,000 -> 1,393,000 (2026-11-12): someone new in a Work Fleet sees whose OK the team's Graph waits for, and the
# page looks again every 5 seconds until it comes (+about 700, used by both the Graph's and the Fleet's parts).
# 1,393,000 -> 1,394,000 (2026-11-12): main sat 288 bytes under it. Five calendar sources (iCloud, CalDAV, Proton, a
# calendar link, Exchange) need their names, icons, marks and sync errors in words wherever a to-do or error line
# shows them (+905); their connect sheets and cards load with Connections.
# 1,394,000 -> 1,395,000 (2026-11-12): Signal chats is a send and draft kind like WhatsApp in the to-do lists, the send
# dialog and the viewer, which draw first (about 0.9 KB).
# 1,395,000 -> 1,250,000 (2026-11-12): main sat at it. What a tap opens and To-dos doesn't draw loads when first
# needed, the parts a tap on To-dos opens first: New to-do's dialog (LAZY 'newtodo'), Search and Ask (LAZY 'palette'),
# the send dialog (with the composer, LAZY 'compose'), the sign-in dialog (LAZY 'signin'), a to-do's messages (with
# their frame, LAZY 'emailframe') and voice recording (LAZY 'voice'); also Talk's bar and view (LAZY 'talk'), Settings'
# Notifications and Model panels, Learning's Share learnings and votes, and what only the Fleet, Graph and Learning
# parts draw (first load about 1,394,000 -> 1,243,221). The ceiling is about that plus 7 KB.
FIRST_LOAD_CEILING = 1_250_000
# At most this much room under the ceiling: a change that makes the first load smaller lowers the ceiling with it, so
# the room it made stays room, not a buffer for the next feature to fill.
FIRST_LOAD_ROOM = 32_000
# graph 336,000 -> 344,000 (2026-11-09): the Graph's rules that moved out of the first load now count in its part.
# settings 124,000 -> 136,000 (2026-11-09): Connected AIs and Apps joined Settings' part.
# whatsnew 12,000 (2026-11-10): its pictures are drawn in it (about 5 KB of SVG).
# graph 344,000 -> 348,000 (2026-11-10): a project's description, its Edit and Keep it updated (about 2.5 KB).
# graph 348,000 -> 350,000 (2026-11-10): a board's header says who sees it, and the owner's locks (about 1.2 KB).
# graph 350,000 -> 348,000 (2026-11-10): team boards no longer fold look-alike projects.
# graph 356,000 -> 360,000 (2026-11-10): the lists' Updated today line and its dot, drawn and styled in this part, not
# in the first load (a few KB).
# milestone 20,000 (2026-11-10): the milestone card on done to-dos, its share dialog and the image it draws.
# clearrun 12,000 (2026-11-10): Go through's dialog (about 8.4 KB).
# recipe 4,000 (2026-11-10): a repeating to-do's kept way, its chat line with Edit and Undo (about 3 KB).
# fbpeople 4,000 (2026-11-10): Facebook's friends nobody in the Graph has, adding them as personal contacts and its Undo (about 2 KB).
# emailframe 6,000 (2026-11-11): an email's HTML in its frame, its dark mode and its links (about 4.3 KB), out of
# the first load when a link fix put it over its ceiling.
# split 12,000 (2026-11-10): Split up's dialog, its preview and Undo (about 9.7 KB), loaded when first used.
# routines 33,000 (2026-11-11): a routine form stays while its Save is on the way (was 31.7 KB of 32,000).
# compose 6,000 (2026-11-12): a new email from a click on an address, in the send dialog (about 4.4 KB).
# ask 3,000 (2026-11-12): a to-do's questions, a pick and the one Answer that sends them all (about 1.4 KB), loaded on
# the first pick or Answer; the questions themselves draw with the to-do.
# msgview 18,000 (2026-11-12): how each kind of message reads in the viewer and a chat as one thread (about 15.7 KB),
# out of the first load when the viewer's per-kind reading put it over its ceiling.
LAZY_CEILING = {'ask': 3_000, 'calendar': 96_000, 'clearrun': 12_000, 'compose': 6_000, 'digest': 8_000, 'emailframe': 6_000, 'connections': 108_000, 'fbpeople': 4_000, 'fleet': 96_000, 'game': 12_000, 'graph': 360_000, 'help': 40_000, 'learning': 24_000, 'mailcheck': 8_000, 'milestone': 20_000, 'msgview': 18_000, 'recipe': 4_000, 'routines': 33_000, 'routinetodos': 12_000, 'settings': 136_000, 'split': 12_000, 'talk': 52_000, 'whatsnew': 14_000}  # whatsnew: 14,000 for the pictures of each new candidate (#1156)


def budget(name):
    """The size a shipped file stays under: its kind's budget in the dashboard's source, SCAN_LIMIT elsewhere."""
    if name in BUDGETS:
        return BUDGETS[name]
    folder, _, file = name.rpartition('/')
    return BUDGETS.get(f'{folder}/*.{file.rpartition(".")[2]}', SCAN_LIMIT) if folder == 'dashboard' else SCAN_LIMIT


# routinetodos 12,000 -> 14,000 (2026-11-11): Also change the routine in a to-do's chat too, and all its styles, which
# moved here out of the first load (about 1.8 KB).
LAZY_CEILING['routinetodos'] = 14_000
# routinetodos 14,000 -> 15,000 (2026-11-11): a cleanup to-do's row opens its mail in the viewer (about 0.6 KB).
LAZY_CEILING['routinetodos'] = 15_000
# followups 28,000 (2026-11-11): a follow-up group's fast review (about 23.9 KB), out of the first load.
# graph 360,000 -> 384,000 (2026-11-11): a project's follow-ups and Done when, a board's follow-ups line and the
# follow-up settings dialog, which only the Graph's pages open (about 17.6 KB), out of the first load.
LAZY_CEILING.update(followups=28_000, graph=384_000)
# connections 108,000 -> 110,000 (2026-11-12): + Add shows Suggested for you on top again, as well as in each group, and
# puts catch-all sources last (about 0.9 KB).
LAZY_CEILING['connections'] = 110_000
# connections 110,000 -> 111,000 (2026-11-12): Signal chats' QR step, its two stop notes and its no-older-messages note
# on the card (about 0.35 KB), after the calendar sources took the room.
LAZY_CEILING['connections'] = 111_000
# brief 7,000 (2026-11-12): the team brief's lines as to-dos (about 5 KB), loaded when one is on screen.
LAZY_CEILING['brief'] = 7_000
# settings 136,000 -> 140,000 (2026-11-12): Work hours' Morning digest follows Snoozes land at, with its note under the
# field (about 1.8 KB); main was 4 bytes under the old ceiling.
LAZY_CEILING['settings'] = 140_000
# 2026-11-12: out of the first load (FIRST_LOAD_CEILING 1,248,000), each part about this much bigger or new:
# newtodo 26,000: New to-do's dialog (about 24.7 KB). palette 20,000: Search and Ask (about 18.8 KB).
# compose 6,000 -> 34,000: the send dialog and a doc write's review (about 28.3 KB).
# signin 18,000: the sign-in dialog (about 16.3 KB). voice 16,000: recording and writing it out (about 14.8 KB).
# emailframe 6,000 -> 10,000: the messages dialog (about 4.4 KB). talk 52,000 -> 56,000: Talk's bar and view (about 11 KB).
# settings 140,000 -> 151,000: Notifications and Model (about 10.6 KB). learning 24,000 -> 42,000: Share learnings and
# votes, and the quality charts only Learning draws (about 17.8 KB). fleet 96,000 -> 100,000 and graph 384,000 ->
# 386,000: what only their pages draw (about 4.8 and 2.9 KB).
LAZY_CEILING.update(newtodo=26_000, palette=20_000, compose=34_000, signin=18_000, voice=16_000, emailframe=10_000,
                    talk=56_000, settings=151_000, learning=42_000, fleet=100_000, graph=386_000)
LAZY_CEILING['areadigest'] = 4_000  # the Work and Personal digest view with its Copy buttons
# areadigest 4,000 -> 7,000 (2026-11-13): a digest notification or its email's link opens that digest as it went (about 1.5 KB)
LAZY_CEILING['areadigest'] = 7_000


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
    'graph.py': (4_800, PY_BYTE_BUDGET),
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
        first, lazy = dashboard_parts.assemble_split(ROOT)
        size = len(first.encode('utf-8'))
        self.assertLessEqual(size, FIRST_LOAD_CEILING, f'The dashboard\'s first load is {size} bytes, over '
                                                       f'FIRST_LOAD_CEILING ({FIRST_LOAD_CEILING}): every phone downloads '
                                                       'it before To-dos shows. Make it smaller, load a part when first '
                                                       'needed (dashboard_parts.LAZY), or raise the ceiling on purpose in '
                                                       'a pull request that says why.')
        self.assertLessEqual(FIRST_LOAD_CEILING - size, FIRST_LOAD_ROOM, f'The dashboard\'s first load is {size} bytes, '
                             f'more than {FIRST_LOAD_ROOM} under FIRST_LOAD_CEILING ({FIRST_LOAD_CEILING}): lower the '
                             'ceiling to about its size plus 10 KB, so the room stays room.')
        self.assertEqual(sorted(lazy), sorted(LAZY_CEILING))
        for group, script in lazy.items():
            with self.subTest(group=group):
                size = len(script.encode('utf-8'))
                self.assertLessEqual(size, LAZY_CEILING[group], f'The {group} part that loads when first needed is '
                                     f'{size} bytes, over its LAZY_CEILING ({LAZY_CEILING[group]}): make it smaller, '
                                     'or raise its ceiling on purpose in a pull request that says why.')

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
