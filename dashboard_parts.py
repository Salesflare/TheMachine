"""The dashboard's source, assembled: dashboard.html with its parts filled in.

The dashboard is served as one page and one script file: the page with its stylesheet and small scripts inline (its CSP,
ETag and compression are per page), and its main script as a file named by its contents, which browsers keep with its
compiled code (machine/web/serving.py dashboard_script); the service worker keeps both for offline starts. Its source is
one page all the same, and can still be split by area: a whole line

    /*@include dashboard/<name>.js*/        in a script
    /*@include dashboard/<name>.css*/       in the stylesheet
    <!--@include dashboard/<name>.html-->   in the markup

in dashboard.html stands for the file dashboard/<name>.<kind>, which holds those lines as they were (the file ends with
a newline, which ends the line the marker took). Only names of lowercase letters, digits and dashes inside dashboard/,
and parts don't include other parts. assemble() puts them back, so the page served is byte for byte the page before the
split. Everything that reads the dashboard's source (the service, tests, scripts) reads it through here
(tests/dashboard-page.mjs is the same for the Node tests); tests/test_dashboard_parts.py checks that.

A leaf module: no imports from the app."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
PAGE = 'dashboard.html'
FOLDER = 'dashboard'
KINDS = ('js', 'css', 'html')
# Parts the served page loads when they're first needed, not with the main script (machine/web/serving.py
# dashboard_script): each group's parts leave the main script and are served as one file of their own, named by its
# contents, that lazyPart(group) in shell-core.js loads (and the page fetches in the background once it's drawn whole
# and idle after its load event and the owner has left it alone for a few seconds, so they never slow the start).
# The source keeps every part in its place, so assemble(), the tests and the demo have them all inline and
# lazyPart() is done at once there. A group's parts run after the main script, so the main script reads none of their
# names while it loads, and calls into them only through lazyRun() or behind lazyIn() (shell-core.js).
# A group's .css parts: the page keeps each one's rules outside its /*@lazy*/ ... /*@eager*/ runs (the rules for
# what only the group's own scripts draw), in a <style data-lazy-css="<name>"> of its own at the part's place, and the
# group's file starts by putting the whole part there: the rules keep their order, so the cascade is as before, and
# they're in before anything of the group draws. tests/test_dashboard_parts.py checks that every rule in a lazy run
# names a class, id or data- attribute only the group's scripts write.
# tests/test_lazy_parts_dashboard.mjs checks the page with them held back and with them refused.
# The page fetches them in this order: what a tap on To-dos opens comes first (New to-do, Search, Send, a sign-in).
LAZY = {
    'newtodo': ('new-todo-dialog.js', 'shell-speed.js'),  # shell-speed.js: first in line, so it runs soon after the page is quiet
    'palette': ('shell-palette.js',),
    'compose': ('todos-send.js', 'todos-compose.js'),
    'kept': ('todos-kept.css', 'todos-kept.js'),
    'signin': ('connections-signin-dialog.js',),
    'logins': ('connections-logins.css', 'connections-logins.js'),
    'loginimport': ('connections-login-import.css', 'connections-login-import.js'),
    'emailframe': ('events-email-frame.js',),
    'msgview': ('events-message.css', 'events-message.js'),
    'voice': ('todos-chat-voice-rec.js',),
    'ask': ('todos-ask.js',),
    'calendar': ('calendar-view.css', 'calendar-view.js'),
    'clearrun': ('todos-clear.css', 'todos-clear-run.js'),
    'connections': ('base-layout.css', 'connections-cards.js'),
    'fleet': ('fleet-manage.css', 'fleet-rules.js', 'fleet-sharing.js', 'fleet-tabs.js', 'fleet-manage.js'),
    'fleetask': ('fleet-questions.css', 'fleet-questions.js'),
    'fbpeople': ('todos-facebook-people.css', 'todos-facebook-people.js'),
    'brief': ('fleet-brief-todo.js',),
    'game': ('todos-game.js',),
    'followups': ('graph-followups-review.css', 'graph-followups-review.js'),
    'graph': ('graph-pages.css', 'graph-crm.css', 'graph-notes.css', 'graph-lists.js', 'graph-boards.js',
              'graph-followups-settings.js', 'graph-record.js', 'graph-tabs.js', 'graph-crm.js', 'graph-notes.js'),
    'fudialog': ('graph-followups-dialog.js',),
    'help': ('help-panel.js',),
    'split': ('graph-split.css', 'graph-split.js'),
    'settings': ('settings-ai.css', 'settings-export.css', 'settings-general.js', 'settings-skills.js', 'settings-ai.js',
                 'settings-export.js', 'settings-notify.js', 'settings-upkeep.js', 'settings-apps.js',
                 'settings-activity.js'),
    'learning': ('learning-missed.css', 'learning-bring.js', 'learning-share.js', 'learning-missed.js'),
    'memimport': ('learning-import.css', 'learning-import.js'),
    'mailcheck': ('todos-mail-check.css', 'todos-reset-nudge.css', 'todos-mail-check.js', 'todos-reset-nudge.js'),
    'milestone': ('todos-milestone.css', 'todos-milestone.js'),
    'msshare': ('todos-milestone-share.css', 'todos-milestone-share.js'),
    'recipe': ('todos-recipe.css', 'todos-recipe.js'),
    'routines': ('routines-page.css', 'routines-page.js'),
    'routinetodos': ('todos-cleanup.css', 'todos-cleanup.js', 'todos-routine-change.js', 'todos-facebook-birthdays.js'),
    'digest': ('todos-digest.css', 'todos-digest.js'),
    'secondhand': ('todos-secondhand.css', 'todos-secondhand.js'),
    'subs': ('todos-subs.css', 'todos-subs.js'),
    'reorder': ('todos-reorder.css', 'todos-reorder.js'),
    'older': ('todos-older.css', 'todos-older.js'),
    'areadigest': ('todos-area-digest.css', 'todos-area-digest.js'),
    'talk': ('todos-chat-talk-view.js', 'todos-chat-talk-live.js'),
    'compact': ('todos-compact.css', 'todos-compact.js'),
    'whatsnew': ('shell-whats-new.css', 'shell-whats-new.js'),
}
# Groups the page fetches together with its main script (a preload link, serving.py) and runs at start: they draw over the
# to-dos, so coming in after the first to-dos they pushed them down. A first drawing that needs one still on its way
# waits for it (render in shell-render.js)
LAZY_EARLY = ('mailcheck', 'milestone')
# {group: the groups whose names its scripts use without asking for them in the code (lazyRun, lazyPart, lazyIn)}, ''
# for the main script: they are in whenever that code runs, for the reason beside it. tests/test_lazy_names.mjs holds
# every script to the main script's names, its own and these.
LAZY_WITH = {
    # the main script: only once its part set or opened what it acts on (talk, mic, fr, aiView, Help's own model box)
    '': ('talk', 'voice', 'followups', 'settings', 'help',
         # a to-do's box: todos-cards.js asks lazyIn(box), box one of these
         'routinetodos', 'digest', 'subs', 'secondhand', 'reorder'),
    # drawn or opened only by that part
    'digest': ('routines',), 'fbpeople': ('routinetodos',), 'fleetask': ('fleet',),
    'logins': ('signin',), 'msgview': ('emailframe',), 'msshare': ('milestone',), 'split': ('graph',),
    'emailframe': ('msgview',),  # emailOpen waits for it
    'fleet': ('settings', 'connections'),  # fleetView waits for Settings', connectAdd for Connections'
    'kept': ('compose', 'followups'),  # only while their dialogs are open
}
LAZY_RUN = re.compile(r'/\*@lazy\*/\n.*?(?:/\*@eager\*/\n|\Z)', re.S)
FENCE = re.compile(r'/\*@(?:lazy|eager)\*/\n')
MARKER = re.compile(r'/\*@include dashboard/([a-z0-9-]+\.(?:js|css))\*/|<!--@include dashboard/([a-z0-9-]+\.html)-->')


def marker(name):
    """The line (without its newline) that stands for dashboard/<name> in dashboard.html."""
    line = f'<!--@include {FOLDER}/{name}-->' if name.endswith('.html') else f'/*@include {FOLDER}/{name}*/'
    if not MARKER.fullmatch(line):
        raise ValueError(f'not a dashboard part name: {name}')
    return line


def included(line):
    """The part name a line (without its newline) stands for, or None."""
    m = MARKER.fullmatch(line)
    return m and (m[1] or m[2])


def includes(source):
    """The part names dashboard.html's source includes, in order."""
    return [name for line in source.split('\n') if (name := included(line))]


def expand(source, folder, kinds=KINDS):
    """source with every include line replaced by its part from folder (a Path to the dashboard/ folder). kinds: only
    the parts of these kinds ('js', 'css', 'html'); the other include lines stay."""
    if '@include' not in source:
        return source
    out = []
    for line in re.split(r'(?<=\n)', source):
        name = included(line.rstrip('\n'))
        if not name or name.rsplit('.', 1)[1] not in kinds:
            out.append(line)
            continue
        part = (Path(folder) / name).read_text(encoding='utf-8')
        if not part.endswith('\n') or f'@include {FOLDER}/' in part:
            raise ValueError(f'{FOLDER}/{name}: a part ends with a newline and includes no other part')
        out.append(part if line.endswith('\n') else part[:-1])
    return ''.join(out)


# The page's <script id="source-kinds" type="application/json">: every kind of event and of message the app knows
# (machine/kinds.py), the to-do status groups (machine/todo_states.py), the services (machine/services.py) and voice
# input's languages (locale_prefs.LANGUAGE_TABLE), for the page's scripts to read instead of
# lists of their own. The same for every owner, so it's filled in here, where the demo and the tests get it too.
KINDS_MARK = '__SOURCE_KINDS__'


def _leaf(root, name, folder='machine'):
    """<folder>/<name>.py of the app in root, a leaf that imports none of the app; beside this file when root has none."""
    import importlib.util
    path = Path(root or ROOT) / folder / f'{name}.py'
    if not path.is_file():
        path = ROOT / folder / f'{name}.py'
    spec = importlib.util.spec_from_file_location(f'app_{folder or "root"}_{name}', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def todo_groups(module):
    """todo_states' named groups (ALL, OPEN, CLOSED, ...): every upper-case tuple of statuses."""
    return {name: list(value) for name, value in vars(module).items()
            if name.isupper() and isinstance(value, tuple) and value and set(value) <= set(module.ALL)}


def kinds_json(root=None):
    """machine/kinds.py, machine/todo_states.py and machine/services.py of the app in root as the page's JSON: {"kinds":
    {...}, "sends": {...}, "todo": {"CLOSED": [...], ...}, "services": {"gmail": {"short": "Email", ...}, ...}}. Read from that folder's own files (leaves with no imports), so a page
    assembled from another checkout gets that checkout's; a folder with only the page and its parts (a copy a test
    makes) gets the ones beside this file. "mic": voice input's languages, locale_prefs.mic_languages() ([code, name,
    BCP-47 tag], in the menu's order)."""
    kinds, states, services = _leaf(root, 'kinds'), _leaf(root, 'todo_states'), _leaf(root, 'services')
    mic = _leaf(root, 'locale_prefs', '').mic_languages()
    # </ can't end the script element early: no kind or name has one, and < keeps it so if one ever did
    return json.dumps({'kinds': kinds.KINDS, 'sends': kinds.SENDS, 'todo': todo_groups(states), 'services': services.page(),
                       'mic': mic}, separators=(',', ':'), sort_keys=True).replace('<', '\\u003c')


def assemble(root=None, page=None):
    """The dashboard page's source as served (before the service fills in __BASE__ and the like). root: the app's
    folder (default: this one); page: another dashboard.html to assemble instead (its parts beside it, in dashboard/)."""
    path = Path(page) if page else Path(root or ROOT) / PAGE
    return expand(path.read_text(encoding='utf-8'), path.parent / FOLDER).replace(KINDS_MARK, kinds_json(path.parent), 1)


def files(root=None):
    """dashboard.html and the parts it includes: what a change to the page's source changes."""
    root = Path(root or ROOT)
    return [root / PAGE] + [root / FOLDER / name for name in includes((root / PAGE).read_text(encoding='utf-8'))]


def assemble_split(root=None):
    """(page, {group: script}): the page's source as assemble() gives it, without the LAZY parts, and each LAZY
    group's parts joined in the source's order. A .css part stays in the page without its lazy runs, in a style
    element of its own; the group's script starts by putting the whole part in there (see LAZY)."""
    path = Path(root or ROOT) / PAGE
    group_of = {name: group for group, names in LAZY.items() for name in names}
    lazy, styles, out = {group: [] for group in LAZY}, {group: [] for group in LAZY}, []
    for line in re.split(r'(?<=\n)', path.read_text(encoding='utf-8')):
        name = included(line.rstrip('\n'))
        if name in group_of and name.endswith('.css'):
            css = (path.parent / FOLDER / name).read_text(encoding='utf-8')
            out.append(f'</style><style data-lazy-css="{name}">\n' + LAZY_RUN.sub('', css) + '</style><style>\n')
            styles[group_of[name]].append([name, FENCE.sub('', css)])
        elif name in group_of:
            lazy[group_of[name]].append(expand(line if line.endswith('\n') else line + '\n', path.parent / FOLDER))
        else:
            out.append(line)
    for group, css in styles.items():
        if css:
            lazy[group].insert(0, 'for(const [n,c] of ' + json.dumps(css, ensure_ascii=False) + ')'
                               '{const s=document.querySelector(`style[data-lazy-css="${n}"]`);if(s)s.textContent=c}\n')
    return (expand(''.join(out), path.parent / FOLDER).replace(KINDS_MARK, kinds_json(path.parent), 1),
            {group: ''.join(parts) for group, parts in lazy.items()})
