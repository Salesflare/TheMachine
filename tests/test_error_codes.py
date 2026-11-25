"""Every fixed error code in the app's own source reaches the error reports readable (error_words.py), and nothing else
does. `imap_no_inbox` arrived as "<word>" because "inbox" isn't a word the reports know, while `imap_refused` came
through (2026-11-25). The codes are read from the source itself, so a new one can't be forgotten:

- a label error (a class that keeps its first argument as its category, label or code: SourceError, ImapError and so on,
  and Skips, which raises SourceError with its label): every value its argument can have. Where that can't be read from
  the source, OPEN says what it can be;
- any other error raised with one plain snake_case string."""
import ast
import functools
import itertools
import re
import unittest
from pathlib import Path

import error_feed as ef
import error_words
import google_api
from machine.sources.slack import SLACK_LABELS, Slack

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'tests', 'scripts', 'evals', 'sandbox', 'node_modules', 'i18n', 'docs'}
CODE = re.compile(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)+')
CARRIED = ()  # another error's label passed on: read where that one is raised
PLAIN = {'sheets', 'slides', 'embeddings'}  # words of everyday text, reported only inside a code (docs_sheets) or not at all: they stay masked
OUTSIDE = ()  # a service's own answer, not a code of ours: it stays masked unless every word of it is known
API = {method.split('.')[0] for method in {**google_api.READ, **google_api.WRITE}} - {'oauth2'}  # whose account it is: never a source
BROWSER = [s + c for s in ('x', 'linkedin') for c in ('_query_unavailable', '_query_failed', '_browser_unreachable', '_browser_failed', '_read_failed')]
# (file, the argument as written): what it can be. Add a line here when a new one can't be read from the source
OPEN = {
    ('connectors/x.py', 'code'): BROWSER,  # machine/browser.py browser_read_failure
    ('connectors/linkedin.py', 'code'): BROWSER,
    ('connectors/docs.py', "'docs_' + str(error.category)"): lambda found: ['docs_' + c for c in found['google_api.py'] - {'google_scope_not_granted'}],
    ('connectors/rss.py', 'READ_ERRORS.get(error.category, error.category)'): ('rss_address', 'rss_redirects', 'network:read:rss_read'),
    ('google_api.py', "method.split('.')[0]"): API,
    ('sources.py', 'api'): ('gmail', 'calendar'),  # what gog_read is asked for as a source
    ('sources.py', "api + ':google_signin_expired_run_gog_auth_add'"): ('gmail:google_signin_expired_run_gog_auth_add', 'calendar:google_signin_expired_run_gog_auth_add'),
    ('ics_feed.py', "error.category.replace('caldav', 'ics')"): CARRIED,
    ('machine/sources/calendar.py', "str(raw['unreadable'])"): ('outlook_invalid_event', 'calendar_invalid_event'),
    ('machine/sources/rows.py', 'self.most_common(1)[0][0]'): CARRIED,  # a row's SourceError, or the label Skips was given
    ('connectors/rss.py', 'skipped.most_common(1)[0][0]'): CARRIED,
    ('machine/sources/slack.py', "'slack_' + (label if label in SLACK_LABELS else 'invalid_response') + ':' + method"):
        [f'slack_{label}:{method}' for label in SLACK_LABELS | {'invalid_response'} for method in Slack.METHODS],
    ('machine/sources/slack.py', "'slack:' + method"): ['slack:' + m for m in Slack.METHODS],
    ('machine/sources/slack.py', "'network:' + name + ':' + method"): ['network:TimeoutError:' + m for m in Slack.METHODS],
    ('ms_graph.py', "'microsoft_signin:' + str(_error_code(error) or error.code)"): OUTSIDE,
    ('ms_graph.py', "'microsoft_signin:' + str(code or error.code)"): OUTSIDE,
    ('gbrain.py', 'code[:80]'): OUTSIDE,
}


def called(node):
    f = node.func
    return f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ''


def label_class(node):
    """The class keeps its first argument as its category, label or code."""
    init = next((f for f in node.body if isinstance(f, ast.FunctionDef) and f.name == '__init__'), None)
    return init is not None and len(init.args.args) > 1 and init.args.args[1].arg in ('category', 'label', 'code') and node.name.endswith('Error')


class Source:
    """One file's functions and calls, and what an expression in it can be as text."""
    def __init__(self, name, text):
        self.name, self.tree = name, ast.parse(text)
        self.calls = [n for n in ast.walk(self.tree) if isinstance(n, ast.Call)]

    @functools.cached_property
    def inside(self):
        """The innermost function of each node (ast.walk goes outside in)."""
        return {node: outer for outer in ast.walk(self.tree) if isinstance(outer, ast.FunctionDef)
                for node in ast.walk(outer) if node is not outer}

    def values(self, node, seen=()):
        """Every text `node` can be, or None when the source doesn't say."""
        if isinstance(node, ast.Constant):
            return {node.value} if isinstance(node.value, str) else set() if node.value is None else None
        if isinstance(node, ast.Call) and called(node) == 'type' or isinstance(node, ast.Attribute) and node.attr == '__name__':
            return {'TimeoutError'}  # an error's type: error_words.SAFE_TYPES says which are kept
        if isinstance(node, ast.Attribute) and node.attr in ('category', 'label') or ast.unparse(node) == 'str(error)':
            return set(CARRIED)
        if isinstance(node, ast.IfExp):
            given = node.test.comparators[0] if isinstance(node.test, ast.Compare) and isinstance(node.test.ops[0], ast.In) else None
            if isinstance(given, (ast.Tuple, ast.Set)) and ast.unparse(node.body) == ast.unparse(node.test.left):
                return self.either(given.elts + [node.orelse], seen)  # label if label in ('a', 'b') else 'c'
            return self.either([node.body, node.orelse], seen)
        if isinstance(node, ast.BoolOp):
            return self.either(node.values, seen)
        if isinstance(node, (ast.BinOp, ast.JoinedStr)):
            if isinstance(node, ast.BinOp) and not isinstance(node.op, ast.Add):
                return None
            parts = [node.left, node.right] if isinstance(node, ast.BinOp) else [getattr(v, 'value', v) if isinstance(v, ast.FormattedValue) else v for v in node.values]
            options = [self.values(p, seen) for p in parts]
            return None if None in options else {''.join(p) for p in itertools.product(*options)}
        if isinstance(node, ast.Call) and called(node) == 'get' and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Dict):
            return self.either(node.func.value.values + node.args[1:], seen)
        if isinstance(node, ast.Name):
            return self.name_values(node, seen)
        return None

    def either(self, nodes, seen):
        options = [self.values(n, seen) for n in nodes]
        return None if None in options else set().union(*options)

    def name_values(self, node, seen):
        """A local name: what it is assigned here, or, for the function's argument, what this file's calls give it."""
        function = self.inside.get(node)
        while function is not None:
            if (function, node.id) in seen:
                return set()
            seen += ((function, node.id),)
            args = function.args.args
            names = [a.arg for a in args]
            set_here = [a.value for a in ast.walk(function) if isinstance(a, ast.Assign) and any(isinstance(t, ast.Name) and t.id == node.id for t in a.targets)]
            if set_here:
                return self.either(set_here, seen)
            if node.id in names:
                at = names.index(node.id)
                defaults = dict(zip(names[len(names) - len(function.args.defaults):], function.args.defaults))
                given = [defaults[node.id]] if node.id in defaults else []
                for source, call in CALLS.get(function.name, ()):
                    if source is self or ast.unparse(call.func) == f'{Path(self.name).stem}.{function.name}':
                        given += [k.value for k in call.keywords if k.arg == node.id] + call.args[at:at + 1]
                return self.either(given, seen) if given else None
            function = self.inside.get(function)
        return None


CALLS = {}  # every call in the app, by name, with its file: a label's prefix given from another file (caldav_calendar.request(…, prefix='ics'))


def app_sources():
    out = []
    for path in sorted(ROOT.rglob('*.py')):
        parts = path.relative_to(ROOT).parts
        if not any(p in SKIP or p.startswith('.') for p in parts[:-1]):
            out.append(Source('/'.join(parts), path.read_text(encoding='utf-8')))
    return out


def read_codes(sources):
    """({file: codes}, [arguments nothing says the value of], the OPEN lines used)."""
    labels = {n.name for s in sources for n in ast.walk(s.tree) if isinstance(n, ast.ClassDef) and label_class(n)} | {'Skips'}
    found, unread, later, used = {}, [], [], set()
    CALLS.clear()
    for source in sources:
        for call in source.calls:
            CALLS.setdefault(called(call), []).append((source, call))
    for source in sources:
        codes = found.setdefault(source.name, set())
        for call in source.calls:
            name = called(call)
            if not call.args or not (name in labels or name.endswith(('Error', 'Exception'))):
                continue
            key = (source.name, ast.unparse(call.args[0]))
            if key in OPEN:
                used.add(key)
                later.append((codes, OPEN[key]))
                continue
            values = source.values(call.args[0])
            if name in labels:
                if values is None:
                    unread.append(f'{source.name}:{call.lineno} {name}({key[1]})')
                codes |= values or set()
            elif isinstance(call.args[0], (ast.Constant, ast.IfExp)):
                codes |= {v for v in values or () if CODE.fullmatch(v)}
    for codes, known in sorted(later, key=lambda line: callable(line[1])):  # one made of another file's codes after them
        codes |= set(known(found) if callable(known) else known)
    CALLS.clear()
    return found, unread, set(OPEN) - used


class Codes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.found, cls.unread, cls.unused = read_codes(app_sources())
        cls.codes = {c for codes in cls.found.values() for c in codes}

    def test_every_fixed_code_comes_through_readable(self):
        self.assertGreater(len(self.codes), 350)
        self.assertLessEqual({'imap_no_inbox', 'imap_refused', 'caldav_tls_failed', 'ics_not_found', 'slack_missing_scope:conversations.info',
                              'android_offline', 'docs_no_access', 'intercom_invalid_cursor'}, self.codes)
        masked = {}
        for name, codes in sorted(self.found.items()):
            for code in sorted(codes - PLAIN):
                for said, left in ((code, code), (code + ':HTTP_401', code.split(':HTTP_')[0] + ':HTTPunauthorized')):
                    out = ef.normalize(said)
                    if said.endswith('token:HTTP_401'):  # what follows a token is taken for one: the code still says it
                        left = code + ':<secret>'
                    if out.replace(' ', '') != left or not ef.allowed(out):
                        masked.setdefault(f'{name}: {code}', out)
        self.assertEqual(masked, {}, 'these reach the error reports masked: add each to error_words.CODES (lowercase letters and _, under 40 characters)')

    def test_every_label_can_be_read_here(self):
        self.assertEqual(self.unread, [], 'an error label built in a way this test can not read: add what it can be to OPEN')
        self.assertEqual(self.unused, set(), 'no longer in the source: take it out of OPEN')

    def test_only_codes_of_the_source_are_listed(self):
        """error_words.CODES is never a way in for other words: each is a whole code the source has, and needed."""
        words = {w for code in self.codes for w in re.split(r'[:]', code)}
        for code in sorted(error_words.CODES):
            with self.subTest(code=code):
                self.assertRegex(code, r'^[a-z]+(?:[_.][a-z]+)*$')
                self.assertIn(code, words, 'no code in the source: take it out of error_words.CODES')
        listed = error_words.SAFE_CODES
        try:
            error_words.SAFE_CODES = listed - error_words.CODES
            self.assertEqual([c for c in sorted(error_words.CODES) if error_words.safe_word(c)], [], 'its words are known: it needs no line')
        finally:
            error_words.SAFE_CODES = listed

    def test_what_a_listed_code_is_made_of_stays_masked(self):
        for text in (*sorted(PLAIN), 'inbox', 'folder', 'Riverbrook', 'imap_no_riverbrook', 'imap_no_inbox_riverbrook', 'riverbrook_imap_no_inbox',
                     'Imap_No_Inbox', 'no_inbox', 'imap_inbox', 'imap_no_inbox.riverbrook', 'caldav_riverbrook', 'ews_maple', 'ics_inbox'):
            with self.subTest(text=text):
                self.assertEqual(ef.normalize(text), '<word>')
        for text, left in (('imap_no_inbox: no folder Klanten/Riverbrook', 'imap_no_inbox: no <word> <path>'),
                           ('imap_no_inbox for sam.lee@globex.example', 'imap_no_inbox for <email>'),
                           ('imap_no_folder "Riverbrook 2026"', 'imap_no_folder "…"'),
                           ('imap_no_folder Sam Lee wrote about maple', 'imap_no_folder <word>'),
                           ('docs_not_connected https://globex.example/deal', 'docs_not_connected <url>'),
                           ('slack:users.info acme.info', 'slack: users.info <url>'),
                           ('slack:users.info.globex.com', 'slack: <url>'),
                           ('acme.users.info Users.info my-users.info', '<url>'),
                           ('teams_work_only +32 470 12 34 56', 'teams_work_only <n>')):
            with self.subTest(text=text):
                out = ef.normalize(text)
                self.assertEqual(out, left)
                self.assertTrue(ef.allowed(out))
        self.assertFalse(ef.allowed('imap_no_inbox riverbrook'))
        self.assertEqual(ef.normalize('imap_no_inbox ews', names=['ews']), 'imap_no_inbox <name>')


class Reading(unittest.TestCase):
    """The scan itself: a code it doesn't know is seen however it is raised."""
    def test_a_new_code_is_found(self):
        source = Source('connectors/acme.py', '''
class AcmeError(Exception):
    def __init__(self, category, status=None):
        super().__init__(category)
def check(kind, ok):
    if ok:
        raise AcmeError('acme_one')
    raise AcmeError('acme_two' if kind else 'acme_three', 404)
def fail(prefix):
    raise helpers.AcmeError(prefix + '_four')
def go(error):
    fail('acme')
    category = {400: 'acme_five'}.get(error.status)
    if category:
        raise AcmeError(category)
    raise RuntimeError('acme_six')
def other(row):
    raise AcmeError(row['label'])
''')
        found, unread, _ = read_codes([source])
        self.assertEqual(found['connectors/acme.py'], {'acme_one', 'acme_two', 'acme_three', 'acme_four', 'acme_five', 'acme_six'})
        self.assertEqual(len(unread), 1)
        for code in found['connectors/acme.py']:
            self.assertEqual(ef.normalize(code), '<word>')


if __name__ == '__main__':
    unittest.main()
