"""machine/services.py, the one table of every service a connection reads: that each row is complete, that it is a leaf,
that the maps it replaced read exactly as they did when they were written out by hand (BEFORE below: the literals as
they were, so a change to a row that would change what one of them said fails here first), and a guard that fails on
a new map or list of services written out by hand.

The guard counts, per file, the lists of services spelled out in code: four or more service keys ('gmail', 'slack',
...) in a tuple, list, set or dict's keys, or in a dashboard array or object's keys, with at least one key no other
word could be (SURE). A list with 'email' or 'doc_reply' in it is a list of message kinds, counted by
tests/test_kinds.py instead. The files that have them today are in SERVICE_LISTS, with their count, which only comes
down: ask machine/services.py instead (services.of(group=services.MAIL), services.field('name'), the page's
SERVICE_ROWS), and lower the count when a list goes. `python3 tests/test_services.py --counts` prints today's."""
import ast
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import dashboard_parts  # noqa: E402
from machine import services  # noqa: E402

SKIP_DIRS = {'node_modules', '.git', '.venv', '__pycache__', 'tests'}
SERVICES_FILE = 'machine/services.py'
SERVICE_KEYS = frozenset(services.SERVICES)
# keys that are only ever a service ('calendar', 'docs', 'x', 'rss' are words of their own too)
SURE = SERVICE_KEYS - {'calendar', 'docs', 'x', 'rss', 'ics', 'imap', 'android', 'gateway', 'github'}
SEND_MARKERS = {'email', 'doc_reply'}
JS_ARRAY = re.compile(r'\[([^\[\]]*)\]')
JS_OBJECT = re.compile(r'\{([^{}]*)\}')
JS_STRING = re.compile(r"['\"]([a-z_]+)['\"]")
JS_KEY = re.compile(r"(?:^|[,{\s])['\"]?([a-z_]+)['\"]?\s*:")

# The hand-written lists of services each file has today: these only come down.
SERVICE_LISTS = {
    'abilities.py': 1,
    'calendar_app.py': 1,
    'calendar_clashes.py': 1,
    'discovery.py': 1,
    'enrichment.py': 1,
    'fleet.py': 1,
    'follow_ups.py': 1,
    'installer.py': 1,
    'machine/app/fleet.py': 1,
    'machine/app/history.py': 1,
    'machine/app/setup_card.py': 2,
    'machine/app/workers.py': 1,
    'machine/cards.py': 1,
    'machine/config.py': 1,
    'machine/names.py': 2,
    'machine/sources/calendar_setup.py': 6,
    'machine/sources/connectors.py': 3,
    'machine/sources/suggest.py': 1,
    'machine/store/message_view.py': 1,
    'mail_grants.py': 1,
    'next_actions.py': 1,
    'onboarding.py': 12,
    'routines_app.py': 1,
    'sandbox/check_fixture.py': 1,
    'sandbox/derive_profile.py': 1,
    'scripts/test.py': 1,
    'shared_graph.py': 2,
    'shared_graph_photos.py': 1,
    'sources.py': 1,
    'team_learnings.py': 1,
    'work_or_personal.py': 1,
    'dashboard/connections-cards.js': 3,
    'dashboard/events-email.js': 2,
    'dashboard/events-message.js': 1,
    'dashboard/graph-record.js': 1,
    'dashboard/setup-card.js': 1,
    'dashboard/todos-cards.js': 2,
    'dashboard/todos-logos.js': 1,
}


def service_list(values):
    """Whether these strings are a list of services: four or more service keys, one of them SURE, and no message kind
    marker."""
    values = set(values)
    return len(values & SERVICE_KEYS) >= 4 and bool(values & SURE) and not values & SEND_MARKERS


def python_service_lists(source, filename='<module>'):
    """[(line, literal)] of the lists of services spelled out in a Python module."""
    found = []
    for node in ast.walk(ast.parse(source, filename)):
        if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
            values = [e.value for e in node.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
        elif isinstance(node, ast.Dict):
            values = [k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
        else:
            continue
        if service_list(values):
            found.append((node.lineno, ast.unparse(node)[:120]))
    return sorted(found)


def js_service_lists(source):
    """[(line, literal)] of the lists of services spelled out in dashboard code: an array of them, or an object keyed
    by them (the innermost braces)."""
    found = []
    for pattern, values in ((JS_ARRAY, JS_STRING), (JS_OBJECT, JS_KEY)):
        for match in pattern.finditer(source):
            if service_list(values.findall(match.group(1))):
                found.append((source.count('\n', 0, match.start()) + 1, match.group(0)[:120]))
    return sorted(found)


def service_lists():
    """{file: [(line, literal)]} for every Python file outside tests and every dashboard script."""
    out = {}
    for path in sorted(ROOT.rglob('*.py')):
        rel = path.relative_to(ROOT)
        if SKIP_DIRS & set(rel.parts[:-1]) or rel.as_posix() == SERVICES_FILE:
            continue
        found = python_service_lists(path.read_text(encoding='utf-8'), rel.as_posix())
        if found:
            out[rel.as_posix()] = found
    for path in [ROOT / dashboard_parts.PAGE, *sorted((ROOT / 'dashboard').glob('*.js'))]:
        found = js_service_lists(path.read_text(encoding='utf-8'))
        if found:
            out[path.relative_to(ROOT).as_posix()] = found
    return out

# The hand-written maps machine/services.py replaced, as they were in the code, apart from the names settled since:
# Gmail is 'Gmail' and 'imap' 'Other email' on every line
BEFORE = {
    'names.SERVICES': {
        'gmail': 'Gmail', 'calendar': 'Google Calendar', 'outlook': 'Outlook', 'outlook_calendar': 'Outlook Calendar', 'imap': 'Other email',
        'icloud_calendar': 'iCloud Calendar', 'caldav': 'Calendar', 'proton_calendar': 'Proton Calendar', 'ics': 'Calendar', 'exchange': 'Exchange',
        'slack': 'Slack', 'teams': 'Microsoft Teams', 'salesflare': 'Salesflare', 'salesforce': 'Salesforce', 'android': 'Android',
        'whatsapp': 'WhatsApp', 'telegram': 'Telegram', 'signal': 'Signal', 'linkedin': 'LinkedIn', 'x': 'X', 'intercom': 'Intercom',
        'zoom': 'Zoom', 'stripe': 'Stripe', 'github': 'GitHub', 'trello': 'Trello', 'shortcut': 'Shortcut', 'linear': 'Linear', 'docs': 'Docs',
        'notion': 'Notion', 'granola': 'Granola', 'google_meet': 'Google Meet', 'rss': 'RSS', 'web_page': 'Web page', 'gateway': 'Machine health'},
    'names.TRANSPORT_SERVICES': {
        'gog': 'gmail', 'gogcli': 'gmail', 'wacli': 'whatsapp', 'wacli-local': 'whatsapp', 'existing_wacli_local_store': 'whatsapp',
        'openclaw-feed': 'android', 'existing_openclaw_feed': 'android', 'journald': 'gateway', 'telegram_mirror': 'telegram',
        'telegram_mirror_store': 'telegram', 'signal_mirror': 'signal', 'signal_mirror_store': 'signal', 'himalaya': 'gmail',
        'msgraph': 'outlook', 'msgraph-cli': 'outlook', 'gh': 'github', 'linkedin-inbox': 'linkedin', 'x-inbox': 'x',
        'salesflare-rest': 'salesflare'},
    'groups.GROUPS': ('mail', 'calendar', 'chat', 'meetings', 'docs', 'customers', 'work', 'other'),
    'groups.GROUP_OF': {
        'gmail': 'mail', 'outlook': 'mail', 'imap': 'mail', 'calendar': 'calendar', 'outlook_calendar': 'calendar',
        'icloud_calendar': 'calendar', 'caldav': 'calendar', 'proton_calendar': 'calendar', 'ics': 'calendar', 'exchange': 'calendar',
        'slack': 'chat', 'teams': 'chat', 'whatsapp': 'chat', 'telegram': 'chat', 'signal': 'chat', 'linkedin': 'chat', 'x': 'chat',
        'zoom': 'meetings', 'google_meet': 'meetings', 'docs': 'docs', 'google_docs': 'docs', 'salesflare': 'customers',
        'salesforce': 'customers', 'intercom': 'customers', 'stripe': 'customers', 'github': 'work', 'shortcut': 'work', 'trello': 'work', 'notion': 'docs', 'linear': 'work', 'granola': 'meetings'},
    'groups.CATCH_ALL': frozenset({'imap', 'caldav', 'ics'}),
    'fleet.SIGNIN_OF': {
        'intercom': 'intercom', 'gmail': 'google', 'calendar': 'google', 'outlook': 'microsoft', 'outlook_calendar': 'microsoft',
        'zoom': 'zoom', 'docs': 'microsoft_docs', 'teams': 'microsoft_teams', 'stripe': 'stripe', 'slack': 'slack', 'trello': 'trello',
        'google_meet': 'google_meet', 'salesforce': 'salesforce', 'shortcut': 'shortcut', 'notion': 'notion', 'linear': 'linear'},
    'onboarding.LABELS': {
        'gmail': 'Gmail', 'calendar': 'Google Calendar', 'outlook': 'Outlook', 'outlook_calendar': 'Outlook Calendar', 'imap': 'Other email',
        'slack': 'Slack', 'salesflare': 'Salesflare CRM', 'android': 'Android notifications', 'whatsapp': 'WhatsApp',
        'telegram': 'Telegram chats', 'signal': 'Signal chats', 'gateway': 'Machine health', 'icloud_calendar': 'iCloud Calendar',
        'caldav': 'Other calendar', 'proton_calendar': 'Proton Calendar', 'ics': 'Calendar link (ICS)', 'exchange': 'Exchange Server'},
    'calendar_setup.LABELS': {
        'icloud_calendar': 'iCloud Calendar', 'caldav': 'Other calendar', 'proton_calendar': 'Proton Calendar',
        'ics': 'Calendar link (ICS)', 'exchange': 'Exchange Server'},
    # tuples keep their order: code may read them in it
    'own_addresses.MAIL_SERVICES': ('gmail', 'outlook', 'imap'),
    'own_addresses.CALENDAR_SERVICES': ('calendar', 'outlook_calendar', 'icloud_calendar', 'caldav', 'proton_calendar', 'ics', 'exchange'),
    'sources.MAIL_SERVICES': ('gmail', 'outlook', 'imap'),
    'sources.MICROSOFT_SERVICES': ('outlook', 'outlook_calendar'),
    'sources.CALENDAR_SERVICES': ('calendar', 'outlook_calendar', 'icloud_calendar', 'caldav', 'proton_calendar', 'ics', 'exchange'),
    'machine.sources.scope_check.MAIL_SERVICES': ('gmail', 'outlook', 'imap'),
    'names.SIGNIN_SOURCES': {'google': 'gmail', 'microsoft': 'outlook', 'zoom': 'zoom', 'stripe': 'stripe', 'slack': 'slack',
                             'salesforce': 'salesforce'},
    'names.SIGNIN_KINDS': {'google': 'mail', 'microsoft': 'mail', 'zoom': 'meetings', 'stripe': 'customers', 'slack': 'chat',
                           'salesforce': 'customers'},
    'onboarding.GRANT_SERVICES': {'google': ('gmail', 'calendar'), 'microsoft': ('outlook', 'outlook_calendar'), 'zoom': ('zoom',),
                                  'stripe': ('stripe',), 'slack': ('slack',), 'google_meet': ('google_meet',), 'salesforce': ('salesforce',)},
    'meet.VIDEO': {'zoom': 'Zoom', 'meet': 'Google Meet', 'teams': 'Teams'},
    'meet.VIDEO_LINKS': {'zoom': ('zoom.us/',), 'meet': ('meet.google.com/',), 'teams': ('teams.microsoft.com/', 'teams.live.com/')},
}
# dicts whose order the code reads: meet.video_habit gives a tie to the first video service
ORDERED = {'meet.VIDEO': ['zoom', 'meet', 'teams'], 'meet.VIDEO_LINKS': ['zoom', 'meet', 'teams']}


# The dashboard's maps machine/services.py replaced, as they were in its scripts, with the names settled as above
BEFORE_PAGE = {
    # dashboard/todos-cards.js
    'SERVICE_NAMES': {
        'gmail': 'Gmail', 'imap': 'Other email', 'calendar': 'Calendar', 'outlook': 'Outlook', 'outlook_calendar': 'Outlook Calendar',
        'icloud_calendar': 'iCloud Calendar', 'caldav': 'Calendar', 'proton_calendar': 'Proton Calendar', 'ics': 'Calendar',
        'exchange': 'Exchange', 'slack': 'Slack', 'salesflare': 'Salesflare CRM', 'salesforce': 'Salesforce', 'whatsapp': 'WhatsApp',
        'telegram': 'Telegram chats', 'signal': 'Signal chats', 'linkedin': 'LinkedIn', 'android': 'Android notifications',
        'gateway': 'Machine health', 'github': 'GitHub', 'intercom': 'Intercom', 'zoom': 'Zoom', 'google_meet': 'Google Meet',
        'teams': 'Teams', 'trello': 'Trello', 'stripe': 'Stripe', 'rss': 'Feed', 'web_page': 'Web page', 'docs': 'Microsoft OneDrive',
        'shortcut': 'Shortcut', 'notion': 'Notion', 'linear': 'Linear', 'granola': 'Granola', 'x': 'X'},
    # dashboard/fleet-sharing.js
    'CONN_LABEL': {
        'gmail': 'Gmail', 'outlook': 'Outlook', 'calendar': 'Google Calendar', 'outlook_calendar': 'Outlook Calendar',
        'icloud_calendar': 'iCloud Calendar', 'caldav': 'Other calendar', 'proton_calendar': 'Proton Calendar', 'ics': 'Calendar link (ICS)',
        'exchange': 'Exchange Server', 'slack': 'Slack', 'salesflare': 'Salesflare', 'whatsapp': 'WhatsApp', 'intercom': 'Intercom',
        'linkedin': 'LinkedIn', 'x': 'X', 'telegram': 'Telegram', 'signal': 'Signal chats'},
    # dashboard/connections-cards.js connectorCard's unit (else 'messages')
    'unit': {
        'calendar': 'events', 'outlook_calendar': 'events', 'icloud_calendar': 'events', 'caldav': 'events', 'proton_calendar': 'events',
        'ics': 'events', 'exchange': 'events', 'intercom': 'conversations', 'android': 'notifications', 'gateway': 'alerts',
        'github': 'notifications', 'stripe': 'events', 'rss': 'items', 'docs': 'items', 'google_meet': 'meetings',
        'trello': 'card changes', 'salesforce': 'updates', 'web_page': 'updates', 'notion': 'items', 'linear': 'items', 'granola': 'meetings'},
    # dashboard/connections-cards.js and calendar-view.js (a set: read with includes)
    'CALENDAR_SERVICES': {'calendar', 'outlook_calendar', 'icloud_calendar', 'caldav', 'proton_calendar', 'ics', 'exchange'},
}


class Page(unittest.TestCase):
    def test_the_page_maps_read_as_before(self):
        """What shell-core.js and its callers make of the page's rows: the maps they wrote out by hand before."""
        rows = services.page()
        field = lambda name: {k: r[name] for k, r in rows.items() if r[name]}
        self.assertEqual(field('short'), BEFORE_PAGE['SERVICE_NAMES'])
        self.assertEqual(field('sharing'), BEFORE_PAGE['CONN_LABEL'])
        self.assertEqual(field('unit'), BEFORE_PAGE['unit'])
        self.assertEqual({k for k, r in rows.items() if r['group'] == 'calendar'}, BEFORE_PAGE['CALENDAR_SERVICES'])

    def test_the_scripts_ask_the_rows(self):
        read = lambda name: (ROOT / 'dashboard' / name).read_text(encoding='utf-8')
        core = read('shell-core.js')
        self.assertIn("SERVICE_NAMES=serviceField('short')", core)
        self.assertIn("CALENDAR_SERVICES=Object.keys(SERVICE_ROWS).filter(k=>SERVICE_ROWS[k].group==='calendar')", core)
        self.assertIn("const CONN_LABEL=serviceField('sharing');", read('fleet-sharing.js'))
        self.assertIn("const unit=SERVICE_ROWS[c.service]?.unit||'messages'", read('connections-cards.js'))
        for name in ('todos-cards.js', 'fleet-sharing.js'):
            self.assertNotIn("outlook_calendar:", read(name), f'{name}: a map keyed by service, written out by hand')
        for name in ('todos-cards.js', 'fleet-sharing.js', 'connections-cards.js', 'calendar-view.js'):
            self.assertNotIn("'outlook_calendar','icloud_calendar'", read(name), f'{name}: a list of calendars, written out by hand')


class Registry(unittest.TestCase):
    def test_every_row_is_complete(self):
        fields = {'name', 'label', 'short', 'sharing', 'unit', 'group', 'last', 'read_now', 'signin', 'transports', 'video', 'video_links'}
        for key, row in services.SERVICES.items():
            with self.subTest(key):
                self.assertEqual(set(row), fields)
                self.assertTrue(row['group'] is None or row['group'] in services.GROUPS)
                self.assertIsInstance(row['transports'], tuple)
                self.assertTrue(row['label'] is None or row['name'], 'a source with a label has a name')
        every = [t for row in services.SERVICES.values() for t in row['transports']]
        self.assertEqual(len(every), len(set(every)), 'a transport belongs to one service')
        self.assertFalse(set(every) & set(services.SERVICES), 'a transport is never a service key')

    def test_the_maps_it_replaced_read_as_before(self):
        import importlib
        for name, before in BEFORE.items():
            module, _, attr = name.rpartition('.')
            module = {'names': 'machine.names', 'groups': 'machine.sources.groups',
                      'calendar_setup': 'machine.sources.calendar_setup'}.get(module, module)
            with self.subTest(name):
                value = getattr(importlib.import_module(module), attr)
                self.assertEqual(value, before)
                if name in ORDERED:
                    self.assertEqual(list(value), ORDERED[name])

    def test_services_is_a_leaf(self):
        tree = ast.parse((ROOT / 'machine' / 'services.py').read_text(encoding='utf-8'))
        self.assertFalse([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))], 'machine/services.py imports nothing')

    def test_every_kind_names_a_service_here(self):
        from machine import kinds
        for kind, row in kinds.KINDS.items():
            with self.subTest(kind):
                self.assertTrue(row['service'] is None or row['service'] in services.SERVICES)


class Guard(unittest.TestCase):
    def test_no_new_hand_written_service_lists(self):
        found = service_lists()
        for name in sorted(set(found) | set(SERVICE_LISTS)):
            with self.subTest(name):
                have, allowed = len(found.get(name, ())), SERVICE_LISTS.get(name, 0)
                self.assertLessEqual(have, allowed, f'{name} spells out {have} lists of services ({allowed} allowed): '
                                     f'ask machine/services.py instead (code moved here from another file: move its count '
                                     f'in SERVICE_LISTS with it). Found: {found.get(name)}')
                self.assertGreaterEqual(have, allowed, f'{name} has {have} lists of services now: lower its count in '
                                        'SERVICE_LISTS to that')

    def test_the_guard_finds_lists_of_services(self):
        found = python_service_lists(
            "A = ('gmail', 'outlook', 'imap', 'slack')\n"
            "B = {'calendar': 'events', 'outlook_calendar': 'events', 'caldav': 'events', 'ics': 'events'}\n"
            "ok = ('gmail', 'outlook', 'imap'), ('email', 'slack', 'whatsapp', 'telegram'), ('calendar', 'docs', 'x', 'rss')\n")
        self.assertEqual([line for line, _ in found], [1, 2], found)
        js = js_service_lists("const A=['calendar','outlook_calendar','icloud_calendar','caldav'];\n"
                              "const B={gmail:'Email',imap:'Email',slack:'Slack',x:'X'};\n"
                              "const ok=['gmail','outlook'],m={email:'Send',slack:'Send',x:'Send',whatsapp:'Send'};\n")
        self.assertEqual([line for line, _ in js], [1, 2], js)


if __name__ == '__main__':
    if '--counts' in sys.argv:
        for name, found in service_lists().items():
            print(f'    {name!r}: {len(found)},')
    else:
        unittest.main()
