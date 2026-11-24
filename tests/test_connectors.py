"""Connector plugins: one file in connectors/ per service, loaded by name, never by path."""
import gzip
import importlib.util
import io
import json
import re
from pathlib import Path
import socket
import tempfile
import types
import unittest
from unittest.mock import patch

import assistant_on_use
import machine.app.sync as machine_app_sync
import machine.main as machine_main
import machine.sources.android as machine_sources_android
import machine.sources.calendar as machine_sources_calendar
import machine.sources.connectors as machine_sources_connectors
import machine.sources.gmail as machine_sources_gmail
import machine.sources.salesflare as machine_sources_salesflare
import machine.sources.signal_chats as machine_sources_signal_chats
import machine.sources.slack as machine_sources_slack
import machine.sources.telegram as machine_sources_telegram
import machine.sources.whatsapp as machine_sources_whatsapp
import machine.store.cards as machine_store_cards
import sources
from connectors import web_page  # noqa: E402 - after the app's modules, as the connectors load them

__getattr__ = assistant_on_use.handed_out('a', 'assistant_plugins')  # `a` for the tests that still import it from here

# What onboarding reads through onboarding.assistant(), from their own modules: tests patch it in
# (onboarding.assistant returning it, or onboarding._assistant) to hand setup these very objects.
FOR_ONBOARDING = types.SimpleNamespace(
    Android=machine_sources_android.Android, Calendar=machine_sources_calendar.Calendar,
    CONNECTOR_HELPERS=machine_sources_connectors.CONNECTOR_HELPERS, Gmail=machine_sources_gmail.Gmail,
    Salesflare=machine_sources_salesflare.Salesflare, Signal=machine_sources_signal_chats.Signal,
    Slack=machine_sources_slack.Slack, SourceError=sources.SourceError, Telegram=machine_sources_telegram.Telegram,
    WhatsApp=machine_sources_whatsapp.WhatsApp, connector_services=machine_sources_connectors.connector_services,
    credential=sources.credential, load_connector=machine_sources_connectors.load_connector)

FEED = {'id': 'work-feed', 'service': 'rss', 'transport': 'http', 'boundary': 'work', 'url': 'https://example.com/feed.xml'}
RSS = b"""<?xml version="1.0"?><rss version="2.0"><channel><title>Example</title>
<item><title>Release 2.0</title><link>https://example.com/2</link><guid>r2</guid>
<pubDate>Wed, 14 Oct 2026 09:00:00 +0200</pubDate><description>&lt;p&gt;New &lt;b&gt;things&lt;/b&gt;&lt;/p&gt;</description></item>
<item><title>Release 1.0</title><link>https://example.com/1</link><guid>r1</guid>
<pubDate>Mon, 12 Oct 2026 09:00:00 GMT</pubDate><description>First</description></item>
</channel></rss>"""
ATOM = b"""<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Example</title>
<entry><title>Post</title><link href="https://example.com/post"/><id>tag:example.com,2026:post</id>
<updated>2026-10-15T08:30:00Z</updated><summary>Hello</summary></entry></feed>"""


class Response(io.BytesIO):
    """A urlopen response with a body and headers: the other connectors' tests import it from here."""
    def __init__(self, body, headers=None):
        super().__init__(body)
        self.headers = headers or {}
    def __enter__(self): return self
    def __exit__(self, *_): self.close()


def served(body=b'', headers=None, status=200, asked=None):
    """The feed's server, as the reader (web_page.get) answers: (status, headers, body, final url). `asked` collects
    the request headers of each read."""
    def get(url, SourceError, request_headers=None, limit=web_page.MAX_BYTES):
        if asked is not None:
            asked.append(request_headers or {})
        return status, headers or {}, body if status == 200 else b'', url
    return patch.object(web_page, 'get', side_effect=get)


class ConnectorPlugins(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = machine_main.Store(Path(self.tmp.name) / 'test.sqlite3')

    def stored(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT kind,title,body,metadata,occurred_at FROM events ORDER BY occurred_at')]

    def later(self):
        """As if the last read was longer ago than the connector's floor (rss.MIN_SECONDS)."""
        state = self.store.checkpoint('work-feed')
        self.store.commit_page('work-feed', {**state, 'read_at': state['read_at'] - 901}, [])

    def test_rss_items_are_stored_once_and_rereads_add_nothing(self):
        with served(RSS, {'ETag': '"v1"'}):
            self.assertEqual(machine_app_sync.sync_source(self.store, {}, FEED)['events'], 2)
        rows = self.stored()
        self.assertEqual([r['title'] for r in rows], ['Release 1.0', 'Release 2.0'])
        self.assertEqual(rows[1]['body'], 'New things')
        self.assertEqual(rows[1]['occurred_at'], '2026-10-14T07:00:00+00:00')
        self.assertEqual(json.loads(rows[1]['metadata'])['source_url'], 'https://example.com/2')
        self.assertEqual(self.store.checkpoint('work-feed')['etag'], '"v1"')
        self.later()
        with served(RSS):
            machine_app_sync.sync_source(self.store, {}, FEED)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*),max(version) FROM events').fetchone()[:], (2, 1))

    def test_not_modified_keeps_the_checkpoint_and_sends_it(self):
        with served(RSS, {'ETag': '"v1"'}):
            machine_app_sync.sync_source(self.store, {}, FEED)
        self.later()
        asked = []
        with served(status=304, asked=asked):
            self.assertEqual(machine_app_sync.sync_source(self.store, {}, FEED)['events'], 0)
        self.assertEqual(asked[0]['If-None-Match'], '"v1"')
        self.assertEqual(self.store.checkpoint('work-feed')['etag'], '"v1"')
        self.assertEqual(len(self.stored()), 2)

    def test_a_feed_is_never_read_more_often_than_the_floor(self):
        # Whatever poll_seconds or a quick retry asks: one read per rss.MIN_SECONDS, as the Web page connector does
        asked = []
        with served(RSS, asked=asked):
            machine_app_sync.sync_source(self.store, {}, {**FEED, 'poll_seconds': 5})
            self.assertEqual(machine_app_sync.sync_source(self.store, {}, {**FEED, 'poll_seconds': 5})['events'], 0)
            self.assertEqual(len(asked), 1)
            self.later()
            machine_app_sync.sync_source(self.store, {}, FEED)
        self.assertEqual(len(asked), 2)

    def test_a_gzipped_feed_is_unpacked(self):
        with served(gzip.compress(ATOM), {'Content-Encoding': 'gzip'}):
            self.assertEqual(machine_app_sync.sync_source(self.store, {}, FEED)['events'], 1)

    def test_atom_feeds_and_kind_labels(self):
        with served(ATOM):
            machine_app_sync.sync_source(self.store, {}, FEED)
        [row] = self.stored()
        self.assertEqual((row['kind'], row['title'], row['occurred_at']), ('rss.item', 'Post', '2026-10-15T08:30:00+00:00'))
        self.assertEqual(machine_store_cards.source_kind('rss.item'), 'feed')
        self.assertEqual(machine_store_cards.source_kind('gmail.message'), 'email')
        self.assertEqual(machine_store_cards.source_kind('nothing.here'), 'signal')

    def test_failures_are_source_errors_with_safe_labels(self):
        cases = [(served(status=500), 'rss_http:HTTP_500'), (served(b'<rss><channel><item>'), 'rss_invalid_xml'),
                 (served(b'x' * 5_000_001), 'rss_feed_too_large')]
        for server, label in cases:
            with self.subTest(label), server:
                with self.assertRaises(sources.SourceError) as caught:
                    machine_app_sync.sync_source(self.store, {}, {**FEED, 'id': label})
                self.assertEqual(str(caught.exception), label)
        with self.assertRaises(sources.SourceError) as caught:
            machine_app_sync.sync_source(self.store, {}, {**FEED, 'url': 'http://example.com/feed'})
        self.assertEqual(str(caught.exception), 'rss_missing_url')

    def test_only_public_addresses_are_read(self):
        # A hosted Machine runs on a cloud server: no feed address, name or redirect may point it at that server, its
        # network or the cloud's metadata address. The same reader as the Web page connector (web_page.get).
        connector = machine_sources_connectors.load_connector('rss')
        for url in ('https://127.0.0.1/feed', 'https://169.254.169.254/latest/meta-data', 'https://10.0.0.8/feed',
                    'https://[::1]/feed', 'https://localhost/feed', 'https://router.local/feed', 'https://example.com:8443/feed'):
            with self.subTest(url), patch.object(socket, 'create_connection', side_effect=AssertionError('connected')):
                with self.assertRaises(sources.SourceError) as caught:
                    machine_app_sync.sync_source(self.store, {}, {**FEED, 'url': url})
                self.assertEqual(str(caught.exception), 'rss_address')
                with self.assertRaisesRegex(sources.SourceError, '^rss_address$'):
                    connector.check({}, {**FEED, 'url': url}, machine_sources_connectors.CONNECTOR_HELPERS)

        class Sock:  # a public name that resolves to a private address: refused on the socket, before a byte is sent
            def getpeername(self):
                return ('10.1.2.3', 443)

            def close(self):
                pass
        with patch.object(socket, 'create_connection', return_value=Sock()):
            with self.assertRaisesRegex(sources.SourceError, '^rss_address$'):
                connector.check({}, FEED, machine_sources_connectors.CONNECTOR_HELPERS)

        class Redirect:
            status = 302

            def getheader(self, name):
                return 'https://169.254.169.254/latest/meta-data' if name == 'Location' else None

        class Connection:
            def __init__(self, *_args):
                pass

            def request(self, *_args, **_kwargs):
                pass

            def getresponse(self):
                return Redirect()

            def close(self):
                pass
        with patch.object(web_page, '_connection', side_effect=Connection):
            with self.assertRaisesRegex(sources.SourceError, '^rss_address$'):
                connector.check({}, FEED, machine_sources_connectors.CONNECTOR_HELPERS)
        self.assertEqual(connector.SETUP['hints']['rss_address'], web_page.SETUP['hints']['web_page_address'])

    def test_setup_probe_reads_and_parses_without_saving_events_or_checkpoint(self):
        connector = machine_sources_connectors.load_connector('rss')
        for raw in (RSS, ATOM):
            with served(raw):
                self.assertIsNone(connector.check({}, FEED, machine_sources_connectors.CONNECTOR_HELPERS))
        self.assertEqual(self.stored(), [])
        self.assertIsNone(self.store.checkpoint('work-feed'))
        for raw, label in ((b'<html/>', 'rss_invalid_feed'), (b'<rss', 'rss_invalid_xml'),
                           (RSS.replace(b'Wed, 14 Oct 2026 09:00:00 +0200', b'not a date').replace(b'Mon, 12 Oct 2026 09:00:00 GMT', b'nor this'), 'rss_invalid_timestamp')):
            with self.subTest(label), served(raw):
                with self.assertRaises(sources.SourceError) as caught:
                    connector.check({}, FEED, machine_sources_connectors.CONNECTOR_HELPERS)
                self.assertEqual(str(caught.exception), label)

    def test_unknown_or_unsafe_service_names_are_unsupported(self):
        for service in ['nope', '../assistant', 'rss.py', 'RSS', '__init__', '']:
            with self.subTest(service), self.assertRaises(sources.SourceError) as caught:
                machine_app_sync.sync_source(self.store, {}, {**FEED, 'service': service})
            self.assertEqual(str(caught.exception), 'unsupported_service')
        self.assertIn('rss', machine_sources_connectors.connector_services())


if __name__ == '__main__':
    unittest.main()


def connector_files():
    paths = sorted(Path(__file__).parent.parent.joinpath('connectors').glob('*.py'))
    assert len(paths) > 5, 'connectors/ holds the connectors'
    return paths


class ConnectorSetup(unittest.TestCase):
    def test_every_connector_says_in_one_line_what_it_reads(self):
        # The setup page shows this under the connector's name; a newly built connector needs one too.
        for path in connector_files():
            if path.name.startswith('_'):
                continue
            spec = importlib.util.spec_from_file_location('connector_' + path.stem, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            setup = getattr(module, 'SETUP', None)
            if setup is None:
                continue
            with self.subTest(connector=path.stem):
                what = setup.get('what')
                self.assertTrue(isinstance(what, str) and what.strip(), f"connectors/{path.name}: add SETUP['what'], one line on what it reads")
                self.assertLessEqual(len(what), 120)
                self.assertNotIn('\n', what)


    def test_every_source_on_the_add_list_says_what_it_brings(self):
        # The dashboard's Add tab and a hosted setup page show this line under each name, built-in sources included.
        import onboarding
        for source in onboarding.catalog({'accounts': []}):
            with self.subTest(source=source['name']):
                what = source.get('what')
                self.assertTrue(isinstance(what, str) and what.strip(), f"{source['name']}: no 'what' line")
                self.assertLessEqual(len(what), 70, 'one short line, so it fits a tile in two lines')
                self.assertNotIn('—', what)


# Services that offer OAuth (docs/adding-a-source.md, Signing in: OAuth first): a connector for one signs in with it.
OAUTH_SERVICES = re.compile(r'\b(google|gmail|youtube|microsoft|outlook|office|onedrive|sharepoint|teams|azure|slack|github|'
                            r'gitlab|bitbucket|notion|hubspot|zoom|calendly|intercom|stripe|salesforce|pipedrive|asana|'
                            r'linear|atlassian|jira|confluence|trello|dropbox|box|airtable|clickup|monday|figma|miro|'
                            r'zendesk|freshdesk|xero|quickbooks|shopify|discord|todoist|typeform|webflow|docusign|'
                            r'mailchimp|spotify|linkedin|twitter|x)\b')
ASKS_KEY = re.compile(r'\b(token|api[ _-]?key|access[ _-]?key|secret|client[ _-]?(id|secret))\b', re.I)
# Developer consoles, API explorers and OAuth playgrounds: never somewhere an owner is sent to connect.
CONSOLE = re.compile(r'console\.cloud\.google\.com|oauthplayground|developers\.google\.com|portal\.azure\.com|entra\.microsoft\.com|'
                     r'api\.slack\.com/apps|github\.com/settings/(tokens|developers|apps)|marketplace\.zoom\.us/develop|'
                     r'app\.hubspot\.com/private-apps|power-ups/admin|developer (hub|console|portal)|playground', re.I)
# Connectors from before this rule, until each signs in with OAuth (remove the entry then). Never add one here:
# a new connector states its reason in SETUP['no_oauth'] instead.
OAUTH_PENDING = {'google_meet'}


class ConnectorSignIn(unittest.TestCase):
    def test_connectors_for_oauth_services_sign_in_with_oauth(self):
        for path in connector_files():
            if path.name.startswith('_') or path.stem in OAUTH_PENDING:
                continue
            spec = importlib.util.spec_from_file_location('connector_signin_' + path.stem, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            setup = getattr(module, 'SETUP', None) or {}
            reason = str(setup.get('no_oauth') or '').strip()
            if len(reason) >= 20:  # a stated reason, not a placeholder
                continue
            with self.subTest(connector=path.stem):
                name = f"{path.stem} {setup.get('label', '')}".replace('_', ' ').lower()
                oauth = OAUTH_SERVICES.search(name)
                offered = setup.get('broker') or setup.get('account_page') or setup.get('account', {}).get('transport') == 'broker'
                asks = [str(setup.get('secret') or '')] + [' '.join(map(str, q[:2])) for q in setup.get('ask') or []]
                if oauth and not offered:
                    self.assertFalse(any(ASKS_KEY.search(text) for text in asks),
                                     f"connectors/{path.name}: {oauth.group(1)} has OAuth; sign in with it, or say why not in SETUP['no_oauth']")
                self.assertIsNone(CONSOLE.search(str(setup.get('note') or '')),
                                  f"connectors/{path.name}: never send the owner to a developer console or playground to connect")

    def test_the_check_catches_a_pasted_token_for_an_oauth_service(self):
        self.assertTrue(OAUTH_SERVICES.search('google meet google meet'))
        self.assertTrue(ASKS_KEY.search('Google OAuth access token'))
        self.assertTrue(CONSOLE.search('Get an access token at https://developers.google.com/oauthplayground/'))
        self.assertFalse(OAUTH_SERVICES.search('shortcut shortcut'))
        self.assertFalse(CONSOLE.search('Create a token at https://app.shortcut.com/settings/account/api-tokens'))

    def test_the_reason_is_for_reviewers_not_a_string_to_translate(self):
        import ast
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
        import i18n_extract
        node = ast.parse("{'label': 'Example service', 'no_oauth': 'Example has no OAuth, only personal tokens.'}").body[0].value
        self.assertEqual(i18n_extract._const_strings(node), ['Example service'])
