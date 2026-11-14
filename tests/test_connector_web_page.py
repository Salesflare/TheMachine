"""Watch a page (connectors/web_page.py): fixture tests, every request replaced. A baseline on the first read that is
never reviewed, nothing on an unchanged read (so no model call), one reviewable signal with only what changed when the
text changed, dates and times never a change, robots.txt asked first, at most one read an hour, and only public https
addresses, checked on the socket itself."""
import json
from pathlib import Path
import socket
import tempfile
import time
import types
import unittest
from unittest.mock import patch

from test_connectors import a
from connectors import web_page

ACCOUNT = {**web_page.SETUP['account'], 'boundary': 'work:Acme', 'url': 'https://tools.example/pricing'}
NOW = '2026-11-14T09:00:00+00:00'


def html(*lines, title='Pricing | Example Tools', extra=''):
    body = ''.join(f'<p>{line}</p>' for line in lines)
    return (f'<!doctype html><html><head><title>{title}</title><script>var x=1</script></head><body>'
            f'<nav><a href="/">Home</a><a href="/pricing">Pricing</a></nav>{extra}<main>{body}</main>'
            '<footer>© Example Tools</footer></body></html>').encode()


PLANS = ('Simple pricing for every team.', 'Starter', '$19 per user a month', 'Pro', '$49 per user a month',
         'Billed yearly. Cancel anytime.', 'Enterprise', 'Talk to us for volume pricing and a dedicated manager.')


class Headers(dict):
    def get(self, key, default=None):
        return next((v for k, v in self.items() if k.lower() == key.lower()), default)


class WebPageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.helpers = types.SimpleNamespace(SourceError=a.SourceError, iso=a.CONNECTOR_HELPERS.iso, now=lambda: NOW)
        self.page, self.robots, self.requests = html(*PLANS), b'User-agent: *\nDisallow: /admin\n', []
        self.clock = 1_800_000_000.0
        patch.object(web_page, 'get', side_effect=self.respond).start()
        patch.object(web_page.time, 'time', side_effect=lambda: self.clock).start()
        self.addCleanup(patch.stopall)

    def respond(self, url, SourceError, headers=None, limit=web_page.MAX_BYTES):
        self.requests.append(url)
        if url.endswith('/robots.txt'):
            return (200, Headers({'Content-Type': 'text/plain'}), self.robots, url) if self.robots is not None else (404, Headers(), b'', url)
        if isinstance(self.page, int):
            return self.page, Headers(), b'', url
        return 200, Headers({'Content-Type': 'text/html; charset=utf-8'}), self.page, url

    def sync(self, hours=0):
        self.clock += hours * 3600
        return web_page.sync(self.store, {}, ACCOUNT, self.helpers)

    def rows(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM events')]

    def pending(self):
        return self.store.events([ACCOUNT['id']], pending=True)

    def test_first_read_is_a_baseline_that_is_never_reviewed(self):
        self.assertEqual(self.sync()['events'], 0)
        [row] = self.rows()
        self.assertEqual((row['kind'], row['title']), ('web_page.change', 'Pricing | Example Tools'))
        self.assertEqual(json.loads(row['metadata'])['source_url'], 'https://tools.example/pricing')
        self.assertEqual(self.pending(), [])  # stored as history: no review, no model call
        self.assertNotIn('Home', json.loads(row['metadata'])['page_text'])  # menus and footers are not the page
        self.assertNotIn('var x', json.loads(row['metadata'])['page_text'])

    def test_unchanged_reads_add_nothing(self):
        self.sync()
        for _ in range(3):
            self.assertEqual(self.sync(hours=6)['events'], 0)
        self.assertEqual(self.rows()[0]['version'], 1)
        self.assertEqual(self.pending(), [])

    def test_a_change_is_one_reviewable_signal_with_only_what_changed(self):
        self.sync()
        self.page = html(*[p.replace('$49', '$59') for p in PLANS])
        self.assertEqual(self.sync(hours=6)['events'], 1)
        [signal] = self.pending()
        self.assertEqual(signal['body'], 'Pro\n− $49 per user a month\n+ $59 per user a month\nBilled yearly. Cancel anytime.')
        self.assertIn('$59 per user a month', signal['metadata']['page_text'])  # the next change is read against this
        self.page = html(*[p.replace('$49', '$59').replace('$19', '$25') for p in PLANS])
        self.sync(hours=6)
        [again] = self.pending()
        self.assertEqual(again['body'], 'Starter\n− $19 per user a month\n+ $25 per user a month\nPro')

    def test_dates_and_times_alone_are_never_a_change(self):
        self.page = html(*PLANS, 'Updated Nov 13, 2026 at 10:42', 'Posted 3 hours ago')
        self.sync()
        self.page = html(*PLANS, 'Updated Nov 14, 2026 at 08:05', 'Posted 5 minutes ago')
        self.assertEqual(self.sync(hours=6)['events'], 0)
        self.assertEqual(self.pending(), [])

    def test_never_more_than_one_read_an_hour(self):
        self.sync()
        asked = len(self.requests)
        self.sync(hours=0.5)  # Check now, a restart: still within the hour
        self.assertEqual(len(self.requests), asked)
        self.sync(hours=1)
        self.assertEqual(len(self.requests), asked + 1)  # robots.txt is kept a day: only the page

    def test_robots_txt_is_asked_first_and_kept_a_day(self):
        self.robots = b'User-agent: *\nDisallow: /pricing\n'
        with self.assertRaisesRegex(a.SourceError, '^web_page_robots$'):
            self.sync()
        self.assertEqual(self.requests, ['https://tools.example/robots.txt'])
        self.robots = b'User-agent: TheMachine\nDisallow: /\n\nUser-agent: *\nAllow: /\n'
        with self.assertRaisesRegex(a.SourceError, '^web_page_robots$'):
            web_page.check({}, dict(ACCOUNT), self.helpers)
        self.robots = None  # no robots.txt at all: fine to read
        self.assertIsNone(web_page.check({}, dict(ACCOUNT), self.helpers))

    def test_errors_are_safe_labels(self):
        self.page = 404
        with self.assertRaisesRegex(a.SourceError, '^web_page_http:HTTP_404$'):
            self.sync()
        self.page = b'<html><body><div id="root"></div><script>render()</script></body></html>'
        with self.assertRaisesRegex(a.SourceError, '^web_page_empty$'):
            self.sync()
        with self.assertRaisesRegex(a.SourceError, '^web_page_address$'):
            web_page.sync(self.store, {}, {**ACCOUNT, 'url': 'ftp://tools.example/x'}, self.helpers)

    def test_setup_names_it_after_the_page_and_keeps_https(self):
        account = {**ACCOUNT, 'url': 'www.tools.example/pricing/'}
        self.assertIsNone(web_page.check({}, account, self.helpers))
        self.assertEqual((account['url'], account['display_name']), ('https://www.tools.example/pricing/', 'tools.example/pricing'))
        self.assertEqual(self.rows(), [])  # setup reads, never stores

    def test_cookie_boxes_and_ads_are_not_the_page(self):
        _, lines = web_page.page_text(html(*PLANS, extra='<div class="cookie-banner">We use cookies</div><aside>Ad</aside>').decode())
        self.assertEqual(lines, list(PLANS))


class Addresses(unittest.TestCase):
    def test_only_public_https_addresses(self):
        self.assertEqual(web_page.address('http://Tools.Example/pricing#plans'), 'https://tools.example/pricing')
        for bad in ('', 'ftp://tools.example', 'https://localhost/', 'https://127.0.0.1/', 'https://10.0.0.8/x',
                    'https://169.254.169.254/latest/meta-data', 'https://[::1]/', 'https://router.local/', 'https://tools.example:8443/',
                    'https://user:secret@tools.example/'):
            with self.subTest(address=bad), self.assertRaises(ValueError):
                web_page.address(bad)

    def test_a_name_that_resolves_to_a_private_address_is_refused_on_the_socket(self):
        class Sock:
            closed = False

            def getpeername(self):
                return ('10.1.2.3', 443)

            def close(self):
                Sock.closed = True
        with patch.object(socket, 'create_connection', return_value=Sock()):
            connection = web_page._connection('tools.example', 5, a.SourceError)
            with self.assertRaisesRegex(a.SourceError, '^web_page_address$'):
                connection.connect()
        self.assertTrue(Sock.closed)

    def test_a_redirect_to_a_private_address_is_refused(self):
        class Response:
            status = 302

            def getheader(self, name):
                return 'https://127.0.0.1/admin' if name == 'Location' else None

        class Connection:
            def __init__(self, *_args):
                pass

            def request(self, *_args, **_kwargs):
                pass

            def getresponse(self):
                return Response()

            def close(self):
                pass
        with patch.object(web_page, '_connection', side_effect=Connection):
            with self.assertRaisesRegex(a.SourceError, '^web_page_address$'):
                web_page.get('https://tools.example/pricing', a.SourceError)


if __name__ == '__main__':
    unittest.main()
