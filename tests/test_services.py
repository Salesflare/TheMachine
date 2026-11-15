"""machine/services.py, the one table of every service a connection reads: that each row is complete, that it is a leaf,
and that the maps it replaced read exactly as they did when they were written out by hand (BEFORE below: the literals
as they were, so a change to a row that would change what one of them said fails here first)."""
import ast
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from machine import services  # noqa: E402

# The hand-written maps machine/services.py replaced, as they were in the code
BEFORE = {
    'names.SERVICES': {
        'gmail': 'Gmail', 'calendar': 'Google Calendar', 'outlook': 'Outlook', 'outlook_calendar': 'Outlook Calendar', 'imap': 'Email',
        'icloud_calendar': 'iCloud Calendar', 'caldav': 'Calendar', 'proton_calendar': 'Proton Calendar', 'ics': 'Calendar', 'exchange': 'Exchange',
        'slack': 'Slack', 'teams': 'Microsoft Teams', 'salesflare': 'Salesflare', 'salesforce': 'Salesforce', 'android': 'Android',
        'whatsapp': 'WhatsApp', 'telegram': 'Telegram', 'signal': 'Signal', 'linkedin': 'LinkedIn', 'x': 'X', 'intercom': 'Intercom',
        'zoom': 'Zoom', 'stripe': 'Stripe', 'github': 'GitHub', 'trello': 'Trello', 'shortcut': 'Shortcut', 'docs': 'Docs',
        'google_meet': 'Google Meet', 'rss': 'RSS', 'web_page': 'Web page', 'gateway': 'Machine health'},
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
        'salesforce': 'customers', 'intercom': 'customers', 'stripe': 'customers', 'github': 'work', 'shortcut': 'work', 'trello': 'work'},
    'groups.CATCH_ALL': frozenset({'imap', 'caldav', 'ics'}),
    'fleet.SIGNIN_OF': {
        'intercom': 'intercom', 'gmail': 'google', 'calendar': 'google', 'outlook': 'microsoft', 'outlook_calendar': 'microsoft',
        'zoom': 'zoom', 'docs': 'microsoft_docs', 'teams': 'microsoft_teams', 'stripe': 'stripe', 'slack': 'slack', 'trello': 'trello',
        'google_meet': 'google_meet', 'salesforce': 'salesforce'},
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
}


# The dashboard's maps machine/services.py replaced, as they were in its scripts
BEFORE_PAGE = {
    # dashboard/todos-cards.js
    'SERVICE_NAMES': {
        'gmail': 'Email', 'imap': 'Email', 'calendar': 'Calendar', 'outlook': 'Outlook', 'outlook_calendar': 'Outlook Calendar',
        'icloud_calendar': 'iCloud Calendar', 'caldav': 'Calendar', 'proton_calendar': 'Proton Calendar', 'ics': 'Calendar',
        'exchange': 'Exchange', 'slack': 'Slack', 'salesflare': 'Salesflare CRM', 'salesforce': 'Salesforce', 'whatsapp': 'WhatsApp',
        'telegram': 'Telegram chats', 'signal': 'Signal chats', 'linkedin': 'LinkedIn', 'android': 'Android notifications',
        'gateway': 'Machine health', 'github': 'GitHub', 'intercom': 'Intercom', 'zoom': 'Zoom', 'google_meet': 'Google Meet',
        'teams': 'Teams', 'trello': 'Trello', 'stripe': 'Stripe', 'rss': 'Feed', 'web_page': 'Web page', 'docs': 'Microsoft OneDrive',
        'shortcut': 'Shortcut', 'x': 'X'},
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
        'trello': 'card changes', 'salesforce': 'updates', 'web_page': 'updates'},
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
        fields = {'name', 'label', 'short', 'sharing', 'unit', 'group', 'last', 'signin', 'transports'}
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
                self.assertEqual(getattr(importlib.import_module(module), attr), before)

    def test_services_is_a_leaf(self):
        tree = ast.parse((ROOT / 'machine' / 'services.py').read_text(encoding='utf-8'))
        self.assertFalse([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))], 'machine/services.py imports nothing')

    def test_every_kind_names_a_service_here(self):
        from machine import kinds
        for kind, row in kinds.KINDS.items():
            with self.subTest(kind):
                self.assertTrue(row['service'] is None or row['service'] in services.SERVICES)


if __name__ == '__main__':
    unittest.main()
