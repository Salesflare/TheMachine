"""Connections: every card says what its source brings in (the + Add line: onboarding.WHAT, a connector's SETUP['what'])
and, where it can act, that it does so only after the owner's OK (assistant.connector_says)."""
import unittest

import onboarding
from connectors import intercom
from test_connectors import a

SHARED = {'fleet': 'f1', 'fleet_name': 'Example', 'grant': 'g1'}


class ConnectionLines(unittest.TestCase):
    def says(self, account):
        return a.connector_says(account, account.get('service', 'gmail'))

    def test_every_source_says_what_it_brings_in(self):
        for service in [*onboarding.LABELS, *a.connector_services()]:
            with self.subTest(service=service):
                what = self.says({'id': 'x', 'service': service}).get('what')
                self.assertTrue(what and what.endswith('.') and len(what) <= 80, what)
                self.assertNotIn('—', what)

    def test_what_it_can_do_only_where_it_can(self):
        cases = [
            ({'service': 'gmail', 'transport': 'gog'}, 'send'),
            ({'service': 'gmail', 'transport': 'broker'}, 'send'),
            ({'service': 'outlook', 'transport': 'graph'}, 'send'),
            ({'service': 'calendar', 'transport': 'broker'}, 'calendar'),
            ({'service': 'calendar', 'transport': 'broker', 'calendar_id': 'team@example.com'}, ''),  # someone else's, not marked writable
            ({'service': 'outlook_calendar', 'transport': 'graph'}, ''),  # Outlook calendars stay read-only
            ({'service': 'slack'}, 'reply'), ({'service': 'whatsapp'}, 'reply'), ({'service': 'telegram'}, 'reply'),
            ({'service': 'linkedin'}, 'reply'), ({'service': 'x'}, 'reply'),
            ({**intercom.SETUP['account'], 'reply_credential': 'intercom-reply', 'reply_admin_id': '42'}, 'reply'),
            (dict(intercom.SETUP['account']), ''),  # a pasted token: reads only
            ({'service': 'slack', 'shared': SHARED}, ''),  # a Fleet's share only reads
            ({'service': 'gmail', 'transport': 'broker', 'shared': SHARED}, ''),
            ({'service': 'salesflare'}, ''), ({'service': 'android'}, ''), ({'service': 'gateway'}, ''),
            ({'service': 'zoom'}, ''), ({'service': 'trello'}, ''), ({'service': 'google_meet'}, ''),
        ]
        for account, acts in cases:
            with self.subTest(account=account):
                self.assertEqual(self.says({'id': 'x', **account}).get('acts', ''), acts)

    def test_no_account_still_says_what(self):
        self.assertEqual(a.connector_says(None, 'zoom'), {'what': 'Meeting summaries and transcripts from Zoom.'})


if __name__ == '__main__':
    unittest.main()
