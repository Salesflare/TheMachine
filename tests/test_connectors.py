"""Connector plugins: one file in connectors/ per service, loaded by name, never by path."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('assistant_plugins', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

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
    def __init__(self, body, headers=None):
        super().__init__(body)
        self.headers = headers or {}
    def __enter__(self): return self
    def __exit__(self, *_): self.close()


class ConnectorPlugins(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'test.sqlite3')

    def stored(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT kind,title,body,metadata,occurred_at FROM events ORDER BY occurred_at')]

    def test_rss_items_are_stored_once_and_rereads_add_nothing(self):
        with patch('urllib.request.urlopen', return_value=Response(RSS, {'ETag': '"v1"'})):
            self.assertEqual(a.sync_source(self.store, {}, FEED)['events'], 2)
        rows = self.stored()
        self.assertEqual([r['title'] for r in rows], ['Release 1.0', 'Release 2.0'])
        self.assertEqual(rows[1]['body'], 'New things')
        self.assertEqual(rows[1]['occurred_at'], '2026-10-14T07:00:00+00:00')
        self.assertEqual(json.loads(rows[1]['metadata'])['source_url'], 'https://example.com/2')
        self.assertEqual(self.store.checkpoint('work-feed')['etag'], '"v1"')
        with patch('urllib.request.urlopen', return_value=Response(RSS)):
            a.sync_source(self.store, {}, FEED)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*),max(version) FROM events').fetchone()[:], (2, 1))

    def test_not_modified_keeps_the_checkpoint_and_sends_it(self):
        with patch('urllib.request.urlopen', return_value=Response(RSS, {'ETag': '"v1"'})):
            a.sync_source(self.store, {}, FEED)
        def not_modified(request, timeout):
            self.assertEqual(request.get_header('If-none-match'), '"v1"')
            raise urllib.error.HTTPError(FEED['url'], 304, 'Not Modified', {}, None)
        with patch('urllib.request.urlopen', side_effect=not_modified):
            self.assertEqual(a.sync_source(self.store, {}, FEED)['events'], 0)
        self.assertEqual(self.store.checkpoint('work-feed')['etag'], '"v1"')
        self.assertEqual(len(self.stored()), 2)

    def test_atom_feeds_and_kind_labels(self):
        with patch('urllib.request.urlopen', return_value=Response(ATOM)):
            a.sync_source(self.store, {}, FEED)
        [row] = self.stored()
        self.assertEqual((row['kind'], row['title'], row['occurred_at']), ('rss.item', 'Post', '2026-10-15T08:30:00+00:00'))
        self.assertEqual(a.source_kind('rss.item'), 'feed')
        self.assertEqual(a.source_kind('gmail.message'), 'email')
        self.assertEqual(a.source_kind('nothing.here'), 'signal')

    def test_failures_are_source_errors_with_safe_labels(self):
        cases = [(urllib.error.HTTPError(FEED['url'], 500, 'secret page text', {}, None), 'rss_http:HTTP_500'),
                 (Response(b'<rss><channel><item>'), 'rss_invalid_xml')]
        for outcome, label in cases:
            kwargs = {'side_effect': outcome} if isinstance(outcome, Exception) else {'return_value': outcome}
            with self.subTest(label), patch('urllib.request.urlopen', **kwargs):
                with self.assertRaises(a.SourceError) as caught:
                    a.sync_source(self.store, {}, FEED)
                self.assertEqual(str(caught.exception), label)
        with self.assertRaises(a.SourceError) as caught:
            a.sync_source(self.store, {}, {**FEED, 'url': 'http://example.com/feed'})
        self.assertEqual(str(caught.exception), 'rss_missing_url')

    def test_setup_probe_reads_and_parses_without_saving_events_or_checkpoint(self):
        connector = a.load_connector('rss')
        for raw in (RSS, ATOM):
            with patch('urllib.request.urlopen', return_value=Response(raw)):
                self.assertIsNone(connector.check({}, FEED, a.CONNECTOR_HELPERS))
        self.assertEqual(self.stored(), [])
        self.assertIsNone(self.store.checkpoint('work-feed'))
        for raw, label in ((b'<html/>', 'rss_invalid_feed'), (b'<rss', 'rss_invalid_xml'),
                           (RSS.replace(b'Wed, 14 Oct 2026 09:00:00 +0200', b'not a date'), 'rss_invalid_timestamp')):
            with self.subTest(label), patch('urllib.request.urlopen', return_value=Response(raw)):
                with self.assertRaises(a.SourceError) as caught:
                    connector.check({}, FEED, a.CONNECTOR_HELPERS)
                self.assertEqual(str(caught.exception), label)

    def test_unknown_or_unsafe_service_names_are_unsupported(self):
        for service in ['nope', '../assistant', 'rss.py', 'RSS', '__init__', '']:
            with self.subTest(service), self.assertRaises(a.SourceError) as caught:
                a.sync_source(self.store, {}, {**FEED, 'service': service})
            self.assertEqual(str(caught.exception), 'unsupported_service')
        self.assertIn('rss', a.connector_services())


if __name__ == '__main__':
    unittest.main()


class ConnectorSetup(unittest.TestCase):
    def test_every_connector_says_in_one_line_what_it_reads(self):
        # The setup page shows this under the connector's name; a newly built connector needs one too.
        for path in sorted(Path(__file__).parent.parent.joinpath('connectors').glob('*.py')):
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
