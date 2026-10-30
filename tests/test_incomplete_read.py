"""A connection that drops mid-body (http.client.IncompleteRead, not an OSError) is a normal network failure:
the same redacted error each site gives for an unreachable server, never a raw exception. The next sync round retries."""
import http.client
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

import enrichment
import google_api
import mail_grants
import ms_graph
from connectors import rss

spec = importlib.util.spec_from_file_location('incomplete_read_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class Dropped:
    """A response whose body stops early, as when the server or a proxy closes the connection mid-read."""

    headers = {}

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self, *args):
        raise http.client.IncompleteRead(b'{"par', 120)


def dropped(*args, **kwargs):
    return Dropped()


class IncompleteReadTest(unittest.TestCase):
    def test_salesflare_send_gives_a_network_source_error(self):
        account = {'id': 'work-crm', 'service': 'salesflare', 'api_base': 'https://crm.example'}
        with patch.object(a, 'credential', return_value='SALESFLARE_STAGING_API_KEY=test'), \
                patch.object(a.urllib.request, 'urlopen', dropped):
            with self.assertRaises(a.SourceError) as caught:
                a.Salesflare({}, account).send('/accounts', {'limit': 1})
        self.assertEqual(caught.exception.category, 'network:IncompleteRead:salesflare_read')
        self.assertIsNone(caught.exception.status)

    def test_other_reads_give_their_network_error(self):
        with patch.object(enrichment.urllib.request, 'urlopen', dropped):
            with self.assertRaisesRegex(enrichment.EnrichmentError, '^unreachable: IncompleteRead$'):
                enrichment.answer({}, 'https://enrich.example/x', 'key', 5)
        with patch.object(mail_grants.urllib.request, 'urlopen', side_effect=http.client.BadStatusLine('')):
            self.assertFalse(mail_grants._revoke_google('token'))
        with patch.object(google_api, 'token', return_value='test'), patch.object(google_api.urllib.request, 'urlopen', dropped), \
                patch.object(google_api, 'url_for', return_value=('GET', 'https://www.googleapis.com/x')):
            with self.assertRaises(google_api.BrokerError) as caught:
                google_api.call({}, None, {}, 'gmail.x', {}, 'scope')
        self.assertEqual(caught.exception.category, 'timeout')
        with patch.object(ms_graph, 'token', return_value='test'), patch.object(ms_graph.urllib.request, 'urlopen', dropped), \
                patch.object(ms_graph, 'url_for', return_value=('GET', 'Mail.Read', 'https://graph.microsoft.com/v1.0/me')):
            with self.assertRaises(ms_graph.GraphError) as caught:
                ms_graph.call({}, None, {}, 'me')
        self.assertEqual(caught.exception.category, 'timeout')
        with patch.object(rss.urllib.request, 'urlopen', dropped):
            with self.assertRaises(a.SourceError) as caught:
                rss.fetch('https://feed.example/rss', {}, a.SourceError)
        self.assertEqual(caught.exception.category, 'network:IncompleteRead:rss_read')


if __name__ == '__main__':
    unittest.main()
