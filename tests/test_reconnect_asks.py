"""Google contacts through the broker (a hosted Machine's sign-in): photos and job titles read with the read-only
contacts scopes its owner granted, and a sign-in from before them, once the broker offers them, gets one to-do to
reconnect (machine/app/reconnect_asks.py): Reconnect leads, it closes itself once reconnected, Not needed is for good."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant as a
import enrichment
import google_api
from machine.app import reconnect_asks
from machine.app import workers

NOW = '2026-01-12T09:00:00+00:00'  # before any file's real mtime in the test: a sign-in saved "just now" is later
LATER = '2026-01-12T10:00:00+00:00'
READ_ONLY = 'https://www.googleapis.com/auth/contacts.readonly'
OTHER = 'https://www.googleapis.com/auth/contacts.other.readonly'
MAIL = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar.readonly']
OFFERED = MAIL + [READ_ONLY, OTHER]  # what the broker's connect asks for now


class BrokerContacts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.account = {'id': 'g1', 'service': 'gmail', 'transport': 'broker', 'email': 'Sam@acme.example', 'boundary': 'personal'}
        self.config = {'database': str(Path(self.temp.name) / 'events.sqlite'),
                       'accounts': [self.account, {'id': 'c1', 'service': 'calendar', 'transport': 'broker', 'email': 'sam@acme.example'}]}
        self.asked = []

    def read(self, config, account, api, version, method, params, scope):
        self.asked.append((method, scope))
        return {}

    def run_with(self, granted, at=NOW, offered=OFFERED):
        found = workers.google_contacts_run(self.store.connect, self.config, self.account, at, read=self.read, granted=granted, offered=offered)
        reconnect_asks.todos(self.store, self.config)  # as the enrichment worker does after its runs
        return found

    def todos(self):
        with self.store.connect() as db:
            cards = [dict(r) for r in db.execute('SELECT * FROM suggestions ORDER BY created_at')]
            self.store.machine_fix_views(db, cards)
        return cards

    def taps(self, card):
        return [b['action']['value'].rsplit(':', 1)[1] for block in a.controls(card)['blocks'] for b in block['buttons']]

    def test_hosted_sign_ins_are_read_too_but_never_one_shared_from_a_fleet(self):
        shared = {'id': 's', 'service': 'gmail', 'transport': 'broker', 'email': 'team@acme.example', 'shared': {'fleet_name': 'Team'}}
        outlook = {'id': 'o', 'service': 'outlook', 'transport': 'broker', 'email': 'o@acme.example'}
        self.assertEqual(workers.google_photo_accounts({'accounts': [*self.config['accounts'], shared, outlook]}), [self.account])

    def test_a_grant_with_the_contacts_scopes_reads_both_lists_read_only_and_never_the_directory(self):
        self.run_with(OFFERED)
        self.assertEqual(self.asked, [('people.connections.list', READ_ONLY), ('otherContacts.list', OTHER)])
        self.assertEqual(self.todos(), [])
        with self.store.connect() as db:
            self.assertFalse(enrichment.contact_run_due(db, 'google:sam@acme.example', NOW))  # once a day, as through gog

    def test_no_to_do_while_the_broker_does_not_offer_the_scopes_yet(self):
        self.run_with(MAIL, offered=MAIL)  # the cloud side isn't live: reconnecting couldn't add them
        self.run_with(MAIL, offered=[])  # a broker from before `offered`
        self.assertEqual((self.asked, self.todos()), ([], []))

    def test_a_grant_from_before_gets_one_quiet_to_do_whose_reconnect_opens_that_sign_in(self):
        self.assertEqual(self.run_with(MAIL), 0)
        self.assertEqual(self.asked, [])  # never asked for a token it wasn't granted: no 403s, no error loop
        [card] = self.todos()
        self.assertEqual(card['title'], 'Reconnect Google to show your contacts’ photos')
        self.assertEqual(card['body'], 'Sam@acme.example was connected before your Machine read contacts. Reconnect it to add their photos, read-only.')
        self.assertEqual((card['status'], card['origin'], json.loads(card['account_ids'])), ('pending', 'machine', ['g1']))  # its account's area
        self.assertEqual(card['reconnect'], {'provider': 'google', 'email': 'Sam@acme.example'})
        self.assertEqual(self.taps(card), ['complete', 'snooze', 'reject'])  # the dashboard's Reconnect leads; Not needed too
        with self.store.connect() as db:
            self.assertEqual([r[0] for r in db.execute('SELECT status FROM deliveries')], ['cancelled'])  # never pushed or in a digest
            self.assertFalse(workers.google_contacts_due(db, self.config, self.account, NOW))  # not again today
        self.run_with(MAIL, LATER)
        self.assertEqual(len(self.todos()), 1)  # never a second one

    def test_signed_in_again_it_is_checked_at_once_and_the_to_do_closes_as_done(self):
        self.run_with(MAIL)
        grants = Path(self.temp.name) / 'mail-grants.json'
        grants.write_text('{}')
        os.utime(grants, (0, 0))  # a sign-in saved before the check: nothing new
        with self.store.connect() as db:
            self.assertFalse(workers.google_contacts_due(db, self.config, self.account, NOW))
        os.utime(grants)  # the reconnect saved a new sign-in just now
        with self.store.connect() as db:
            self.assertTrue(workers.google_contacts_due(db, self.config, self.account, NOW))
        self.run_with(OFFERED, LATER)
        [card] = self.todos()
        self.assertEqual(card['status'], 'completed')
        self.assertNotIn('reconnect', card)
        self.assertEqual([m for m, _ in self.asked], ['people.connections.list', 'otherContacts.list'])

    def test_not_needed_is_for_good(self):
        self.run_with(MAIL)
        [card] = self.todos()
        self.store.decide(card['id'], 'reject', '', 'd1', 'dashboard')
        self.run_with(MAIL, LATER)
        self.assertEqual([c['status'] for c in self.todos()], ['rejected'])

    def test_one_scope_unticked_reads_the_other_and_still_asks(self):
        self.run_with(MAIL + [READ_ONLY])
        self.assertEqual(self.asked, [('people.connections.list', READ_ONLY)])
        self.assertEqual(len(self.todos()), 1)

    def test_a_broker_that_cant_say_tries_the_next_day_quietly(self):
        with patch.object(google_api, 'grant', side_effect=google_api.BrokerError('google_broker_unreachable')), \
                self.assertNoLogs(level='WARNING'):
            self.assertEqual(workers.google_contacts_run(self.store.connect, self.config, self.account, NOW, read=self.read), 0)
        self.assertEqual((self.asked, self.todos()), ([], []))
        with self.store.connect() as db:
            self.assertFalse(enrichment.contact_run_due(db, 'google:sam@acme.example', NOW))

    def test_an_ask_of_an_account_no_longer_here_or_shared_makes_no_to_do(self):
        workers.google_contacts_run(self.store.connect, self.config, self.account, NOW, read=self.read, granted=MAIL, offered=OFFERED)
        self.assertEqual(reconnect_asks.todos(self.store, {'accounts': []}), 0)
        self.assertEqual(reconnect_asks.todos(self.store, {'accounts': [{**self.account, 'shared': {'fleet_name': 'Team'}}]}), 0)
        self.assertEqual(self.todos(), [])


class PeopleUrls(unittest.TestCase):
    def test_the_people_api_is_read_on_its_own_host_with_people_me_in_the_path(self):
        verb, url = google_api.url_for('people.connections.list', {'resourceName': 'people/me', 'pageSize': 1000, 'personFields': 'photos'})
        self.assertEqual((verb, url), ('GET', 'https://people.googleapis.com/v1/people/me/connections?pageSize=1000&personFields=photos'))
        self.assertEqual(google_api.url_for('otherContacts.list', {'readMask': 'photos'})[1], 'https://people.googleapis.com/v1/otherContacts?readMask=photos')
        for bad in ('people/../me', '../x', 'people//me', 'people/me?x=1', ''):
            with self.subTest(bad=bad), self.assertRaises(google_api.BrokerError):
                google_api.url_for('people.connections.list', {'resourceName': bad})
        with self.assertRaises(google_api.BrokerError):
            google_api.url_for('people.listDirectoryPeople', {})  # the directory isn't read through the broker
        # a plain {name} still escapes a slash
        self.assertIn('/calendars/a%2Fb/events', google_api.url_for('calendar.events.list', {'calendarId': 'a/b'})[1])

    def test_a_broker_says_what_it_offers_or_nothing(self):
        with patch.object(google_api, '_broker', return_value={'scopes': MAIL, 'offered': [READ_ONLY, 7]}):
            self.assertEqual(google_api.grant({}, None, {'email': 'x@acme.example'}), (set(MAIL), {READ_ONLY}))
        with patch.object(google_api, '_broker', return_value={'scopes': MAIL}):
            self.assertEqual(google_api.grant({}, None, {'email': 'x@acme.example'})[1], set())


if __name__ == '__main__':
    unittest.main()
