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
# and idle after its load event, so they never slow the start).
# The source keeps every part in its place, so assemble(), the tests and the demo have them all inline and
# lazyPart() is done at once there. A group's parts run after the main script, so the main script reads none of their
# names while it loads, and calls into them only through lazyRun() or behind lazyIn() (shell-core.js).
# A group's .css parts: the page keeps each one's rules outside its /*@lazy*/ ... /*@eager*/ runs (the rules for
# what only the group's own scripts draw), in a <style data-lazy-css="<name>"> of its own at the part's place, and the
# group's file starts by putting the whole part there: the rules keep their order, so the cascade is as before, and
# they're in before anything of the group draws. tests/test_dashboard_parts.py checks that every rule in a lazy run
# names a class, id or data- attribute only the group's scripts write.
# tests/test_lazy_parts_dashboard.mjs checks the page with them held back and with them refused.
LAZY = {
    'calendar': ('calendar-view.css', 'calendar-view.js'),
    'clearrun': ('todos-clear.css', 'todos-clear-run.js'),
    'connections': ('base-layout.css', 'connections-cards.js'),
    'fleet': ('fleet-manage.css', 'fleet-rules.js', 'fleet-sharing.js', 'fleet-tabs.js', 'fleet-manage.js'),
    'fbpeople': ('todos-facebook-people.js',),
    'game': ('todos-game.js',),
    'graph': ('graph-pages.css', 'graph-crm.css', 'graph-lists.js', 'graph-boards.js', 'graph-record.js', 'graph-tabs.js',
              'graph-crm.js'),
    'help': ('help-panel.js',),
    'learned': ('todos-first-learned.css', 'todos-first-learned.js'),
    'settings': ('settings-ai.css', 'settings-export.css', 'settings-general.js', 'settings-skills.js', 'settings-ai.js',
                 'settings-export.js', 'settings-upkeep.js', 'settings-apps.js'),
    'learning': ('learning-bring.js', 'learning-missed.js'),
    'mailcheck': ('todos-mail-check.css', 'todos-mail-check.js'),
    'recipe': ('todos-recipe.css', 'todos-recipe.js'),
    'routines': ('routines-page.css', 'routines-page.js'),
    'routinetodos': ('todos-cleanup.css', 'todos-cleanup.js', 'todos-routine-change.js', 'todos-facebook-birthdays.js'),
    'talk': ('todos-chat-talk-live.js',),
    'whatsnew': ('shell-whats-new.css', 'shell-whats-new.js'),
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


def assemble(root=None, page=None):
    """The dashboard page's source as served (before the service fills in __BASE__ and the like). root: the app's
    folder (default: this one); page: another dashboard.html to assemble instead (its parts beside it, in dashboard/)."""
    path = Path(page) if page else Path(root or ROOT) / PAGE
    return expand(path.read_text(encoding='utf-8'), path.parent / FOLDER)


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
    return expand(''.join(out), path.parent / FOLDER), {group: ''.join(parts) for group, parts in lazy.items()}
