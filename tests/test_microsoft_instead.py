"""+ Add, Other email or Exchange Server: an address on Microsoft 365 goes to Sign in with Microsoft instead of a password
(connect_address_signin in machine/app/connect.py, imap_presets.microsoft_365). Found from the domain's MX records, and
for Exchange also Microsoft's autodiscover; a few seconds at most, and nothing found keeps the password form. Fake DNS
answers only: nothing here reaches the network."""
import json
import threading
import time
import unittest
from unittest import mock

import assistant
import ews_calendar
import imap_presets
from machine.app import connect
from machine.owner_error import OwnerError


def mx(*hosts):
    """A fake DNS-over-HTTPS answer with these mail servers, in this order."""
    answer = [{'type': 15, 'data': f'{10 * (i + 1)} {h}.'} for i, h in enumerate(hosts)]
    return lambda url: json.dumps({'Answer': answer})


class Microsoft365(unittest.TestCase):
    def test_mx_at_microsoft_365(self):
        self.assertTrue(imap_presets.microsoft_365('alex@cloudco.test', fetch=mx('cloudco-test.mail.protection.outlook.com')))
        self.assertTrue(imap_presets.microsoft_365('alex@cloudco.test', fetch=mx('filter.acme.test', 'cloudco-test.mail.protection.outlook.com')))

    def test_own_server_google_or_no_answer_is_not(self):
        self.assertFalse(imap_presets.microsoft_365('alex@acme.test', fetch=mx('mail.acme.test')))
        self.assertFalse(imap_presets.microsoft_365('alex@acme.test', fetch=mx('aspmx.l.google.com')))
        self.assertFalse(imap_presets.microsoft_365('alex@acme.test', fetch=lambda url: None))
        self.assertFalse(imap_presets.microsoft_365('alex@acme.test', fetch=lambda url: 'not json'))
        self.assertFalse(imap_presets.microsoft_365('not an address', fetch=mx('x.mail.protection.outlook.com')))

    def test_outlook_com_and_gmail_need_no_lookup(self):
        asked = mock.Mock(side_effect=AssertionError('no lookup'))
        self.assertTrue(imap_presets.microsoft_365('alex@hotmail.com', fetch=asked))
        self.assertFalse(imap_presets.microsoft_365('alex@gmail.com', fetch=asked))

    def test_only_the_domain_is_asked_with_a_short_timeout(self):
        with mock.patch.object(imap_presets._OPENER, 'open', side_effect=OSError) as opened:
            self.assertFalse(imap_presets.microsoft_365('alex@acme.test'))
        request = opened.call_args.args[0]
        self.assertTrue(request.full_url.startswith(imap_presets.DOH))
        self.assertNotIn('alex', request.full_url)
        self.assertEqual(opened.call_args.kwargs['timeout'], imap_presets.QUICK)


class Signin(unittest.TestCase):
    def test_exchange_goes_to_outlook_calendar_and_imap_to_outlook(self):
        with mock.patch.object(imap_presets, 'microsoft_365', return_value=True):
            self.assertEqual(connect.microsoft_signin('exchange', ' Alex@CloudCo.test '), 'outlook_calendar')
            self.assertEqual(connect.microsoft_signin('imap', 'alex@cloudco.test'), 'outlook')
            self.assertIsNone(connect.microsoft_signin('caldav', 'alex@cloudco.test'))  # only these two forms
            self.assertIsNone(connect.microsoft_signin('imap', 'alex'))

    def test_exchange_also_asks_autodiscover_and_imap_does_not(self):
        with mock.patch.object(imap_presets, 'microsoft_365', return_value=False), \
                mock.patch.object(ews_calendar, 'microsoft_365', return_value=True) as autodiscover:
            self.assertEqual(connect.microsoft_signin('exchange', 'alex@hybrid.test'), 'outlook_calendar')
            self.assertIsNone(connect.microsoft_signin('imap', 'alex@hybrid.test'))
        self.assertEqual(autodiscover.call_count, 1)

    def test_on_prem_keeps_the_password_form(self):
        with mock.patch.object(imap_presets, 'microsoft_365', return_value=False), \
                mock.patch.object(ews_calendar, 'microsoft_365', return_value=False):
            self.assertIsNone(connect.microsoft_signin('exchange', 'alex@acme.test'))

    def test_a_slow_lookup_keeps_the_password_form(self):
        done = threading.Event()
        self.addCleanup(done.set)
        with mock.patch.object(imap_presets, 'microsoft_365', side_effect=lambda email: done.wait(5)):
            started = time.monotonic()
            self.assertIsNone(connect.microsoft_signin('exchange', 'alex@slow.test', wait=0.2))
            self.assertLess(time.monotonic() - started, 2)

    def test_the_action_is_the_owners_from_the_dashboard(self):
        app = object.__new__(assistant.App)
        app.config = {'accounts': []}
        with mock.patch.object(imap_presets, 'microsoft_365', return_value=True):
            self.assertEqual(app.action('connect_address_signin', {'name': 'exchange', 'email': 'alex@cloudco.test'}, owner_dashboard=True),
                             {'signin': 'outlook_calendar'})
            self.assertEqual(app.action('connect_address_signin', {'name': 'exchange', 'email': ['x']}, owner_dashboard=True),
                             {'signin': None})
            with self.assertRaises(OwnerError):  # never the CLI the agent can run
                app.action('connect_address_signin', {'name': 'exchange', 'email': 'alex@cloudco.test'})


if __name__ == '__main__':
    unittest.main()
