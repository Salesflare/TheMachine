"""The dashboard's source, assembled: dashboard.html with its parts filled in.

The dashboard is served as one page (one document, its scripts inline: the service worker keeps it whole for offline
starts, and its CSP, ETag and compression are per page). Its source can still be split by area: a whole line

    /*@include dashboard/<name>.js*/

in dashboard.html stands for the file dashboard/<name>.js, which holds those lines as they were (the file ends with a
newline, which ends the line the marker took). Only names of lowercase letters, digits and dashes inside dashboard/,
and parts don't include other parts. assemble() puts them back, so the page served is byte for byte the page before the
split. Everything that reads the dashboard's source (the service, tests, scripts) reads it through here
(tests/dashboard-page.mjs is the same for the Node tests); tests/test_dashboard_parts.py checks that.

A leaf module: no imports from the app."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PAGE = 'dashboard.html'
FOLDER = 'dashboard'
MARKER = re.compile(r'/\*@include dashboard/([a-z0-9-]+\.js)\*/')


def marker(name):
    """The line (without its newline) that stands for dashboard/<name> in dashboard.html."""
    if not MARKER.fullmatch(f'/*@include {FOLDER}/{name}*/'):
        raise ValueError(f'not a dashboard part name: {name}')
    return f'/*@include {FOLDER}/{name}*/'


def includes(source):
    """The part names dashboard.html's source includes, in order."""
    return [m[1] for line in source.split('\n') if (m := MARKER.fullmatch(line))]


def expand(source, folder):
    """source with every include line replaced by its part from folder (a Path to the dashboard/ folder)."""
    if '@include' not in source:
        return source
    out = []
    for line in re.split(r'(?<=\n)', source):
        m = MARKER.fullmatch(line.rstrip('\n'))
        if not m:
            out.append(line)
            continue
        part = (Path(folder) / m[1]).read_text(encoding='utf-8')
        if not part.endswith('\n') or f'/*@include {FOLDER}/' in part:
            raise ValueError(f'{FOLDER}/{m[1]}: a part ends with a newline and includes no other part')
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
