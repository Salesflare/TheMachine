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
import re

ROOT = Path(__file__).resolve().parent
PAGE = 'dashboard.html'
FOLDER = 'dashboard'
KINDS = ('js', 'css', 'html')
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
