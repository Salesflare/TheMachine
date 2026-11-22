"""The setup to-do's one suggestion with its reason (machine/app/setup_nudge.py): only in the owner's first two weeks, on a
day with at most one new to-do, never without a signal, one at a time and at most one new one a day, and its line says
a count at most, never what a message says or who sent it. Fake data only."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

import assistant as a
import machine.app.setup_card as setup_card
from machine.app import setup_nudge

NOW = dt.datetime(2026, 11, 20, 10, 0, tzinfo=dt.timezone.utc)
STARTED = '2026-11-15'


class SetupNudge(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        self.store = a.Store(self.dir / 'events.sqlite')
        self.notes = self.dir / 'needs-you.json'
        self.config = {'accounts': [{'id': 'me-gmail', 'service': 'gmail', 'email': 'sam@example.org'}],
                       'manage_url': 'https://app.example.test/setup', 'needs_you_file': str(self.notes)}
        self.n = 0

    def pick(self, current=NOW, started=STARTED, dismissed=(), failed=(), config=None):
        return setup_nudge.pick(self.store, config or self.config, started, dismissed, failed, current)

    def mail(self, sender, body='', title='Hello', n=1, days_ago=1, **metadata):
        when = (NOW - dt.timedelta(days=days_ago)).isoformat()
        with self.store.connect() as db:
            for _ in range(n):
                self.n += 1
                db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) VALUES(?,?,?,?,?,?,?,?,?)',
                           ('me-gmail', f's{self.n}', 'gmail.message', when, title, body, json.dumps({'from': sender, **metadata}), 'h', when))

    def todos(self, n, at=NOW):
        with self.store.connect() as db:
            for i in range(n):
                self.n += 1
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at) VALUES(?,?,?,?,'[]','[]',?)",
                           (f't{self.n}', f'd{self.n}', 'A to-do', '', at.isoformat()))

    def failed_note(self, source, why='expired', at=NOW):
        self.notes.write_text(json.dumps([{'id': 'connect-failed-' + source, 'connect_failed': source, 'why': why, 'at': at.isoformat()}]))

    def test_no_signal_no_suggestion(self):
        self.mail('Friend <friend@example.org>', body='Lunch on Friday?', n=5)
        self.assertIsNone(self.pick())

    def test_a_whatsapp_code_that_ran_out_is_offered_again(self):
        self.failed_note('whatsapp')
        nudge = self.pick()
        self.assertEqual(nudge, {'id': 'nudge-retry-whatsapp', 'title': 'Try WhatsApp again? The code ran out.', 'button': 'Try again',
                                 'href': '#connect=whatsapp', 'icon': 'whatsapp', 'replaces': 'whatsapp', 'nudge': True})

    def test_another_failed_sign_in_takes_the_place_of_more_connections(self):
        self.failed_note('linkedin', why='failed')
        nudge = self.pick()
        self.assertEqual((nudge['title'], nudge['replaces'], nudge['href']), ('Try LinkedIn again? The sign-in didn’t finish.', 'connect', '#connections=add'))
        # one that failed on this dashboard counts the same; an old note does not
        self.failed_note('linkedin', at=NOW - dt.timedelta(days=20))
        self.assertIsNone(self.pick(current=NOW + dt.timedelta(days=1)))
        self.assertEqual(self.pick(current=NOW + dt.timedelta(days=2), failed=('slack',))['id'], 'nudge-retry-slack')

    def test_a_source_connected_since_is_not_offered_again(self):
        self.failed_note('whatsapp')
        config = dict(self.config, accounts=[*self.config['accounts'], {'id': 'wa', 'service': 'whatsapp'}])
        self.assertIsNone(self.pick(config=config))

    def test_whatsapp_from_mail_by_people_with_a_count_only(self):
        self.mail('Robin <robin@example.org>', body='Text me: https://wa.me/32470000000', title='Garden plan for Saturday', n=2)
        self.mail('Kim <kim@example.net>', body='Shall we move this to WhatsApp?')
        # never counted: a mailing, a program's mail, WhatsApp's own, the owner's own
        self.mail('News <news@shop.example>', body='Follow us on WhatsApp', n=3, list_unsubscribe=True)
        self.mail('Bot <robot@example.com>', body='chat.whatsapp.com/abc', n=3, precedence='bulk')
        self.mail('WhatsApp <hello@whatsapp.com>', body='WhatsApp news', n=3)
        self.mail('Sam <sam@example.org>', body='wa.me/1', n=3, from_me=True)
        nudge = self.pick()
        self.assertEqual((nudge['id'], nudge['title'], nudge['replaces']), ('nudge-whatsapp', 'Connect WhatsApp? 3 emails mention it.', 'whatsapp'))
        for word in ('Robin', 'Kim', 'Garden', 'wa.me', 'example'):
            self.assertNotIn(word, json.dumps(nudge))

    def test_two_mentions_are_not_enough(self):
        self.mail('Robin <robin@example.org>', body='https://wa.me/32470000000', n=2)
        self.assertIsNone(self.pick())

    def test_whatsapp_only_where_it_signs_in(self):
        self.mail('Robin <robin@example.org>', body='https://wa.me/32470000000', n=4)
        self.assertIsNone(self.pick(config={k: v for k, v in self.config.items() if k != 'manage_url'}))

    def test_another_address_of_their_own(self):
        import own_addresses
        with self.store.connect() as db:
            own_addresses.ensure(db)
            db.execute("INSERT INTO own_addresses(address,sources,state,reason,updated_at) VALUES('sam@example.org','[\"account\"]','yours',NULL,?)", (NOW.isoformat(),))
            db.execute("INSERT INTO own_addresses(address,sources,state,reason,updated_at) VALUES('sam@alias.example','[\"alias\"]','yours',NULL,?)", (NOW.isoformat(),))
        self.assertIsNone(self.pick())  # an alias: its mail comes in already
        with self.store.connect() as db:
            db.execute("INSERT INTO own_addresses(address,sources,state,reason,updated_at) VALUES('sam@work.example','[\"calendar\"]','yours',NULL,?)", (NOW.isoformat(),))
        nudge = self.pick()
        self.assertEqual((nudge['id'], nudge['title'], nudge['href'], nudge['replaces']),
                         ('nudge-account', 'Add your other address too? Mail to it shows up here.', '#connections=add', 'account'))
        self.assertNotIn('work.example', json.dumps(nudge))

    def test_slack_from_the_suggested_for_you_count(self):
        self.mail('Slack <feedback@slack.com>', n=4)
        nudge = self.pick()
        self.assertEqual((nudge['id'], nudge['title'], nudge['href'], nudge['replaces']),
                         ('nudge-slack', 'Connect Slack? 4 emails from Slack this month.', '#connect=slack', 'connect'))

    def test_only_in_the_first_two_weeks(self):
        self.failed_note('whatsapp', at=NOW + dt.timedelta(days=8))
        self.assertIsNotNone(self.pick(current=NOW + dt.timedelta(days=8)))  # day 13 since sign-up
        self.assertIsNone(self.pick(current=NOW + dt.timedelta(days=10)))  # day 15

    def test_not_on_a_day_with_more_to_dos(self):
        self.failed_note('whatsapp')
        self.todos(1)
        self.assertIsNotNone(self.pick())
        self.todos(1)
        self.assertIsNone(self.pick())
        self.assertIsNotNone(self.pick(current=NOW + dt.timedelta(days=1)))  # the next day starts over

    def test_one_new_suggestion_a_day_and_closed_for_good(self):
        self.mail('Slack <feedback@slack.com>', n=4)
        self.assertEqual(self.pick()['id'], 'nudge-slack')
        self.failed_note('whatsapp')  # a stronger signal later that day waits for tomorrow
        self.assertEqual(self.pick()['id'], 'nudge-slack')
        closed = ['hint-nudge-slack']
        self.assertIsNone(self.pick(dismissed=closed))  # closed: none other that day
        tomorrow = NOW + dt.timedelta(days=1)
        self.failed_note('whatsapp', at=tomorrow)
        self.assertEqual(self.pick(current=tomorrow, dismissed=closed)['id'], 'nudge-retry-whatsapp')
        self.assertIsNone(self.pick(current=tomorrow, dismissed=[*closed, 'hint-nudge-retry-whatsapp']))

    def test_its_x_is_a_setup_row_like_any_other(self):
        self.assertEqual(setup_card.setup_dismiss(self.store, self.config, 'hint-nudge-retry-whatsapp')['setup_card']['dismissed'],
                         ['hint-nudge-retry-whatsapp'])

    def test_the_app_sends_it_with_the_setup_to_do(self):
        import machine.main as machine_main
        import timeutil
        app = object.__new__(machine_main.App)
        app.store, app.config = self.store, dict(self.config, started_at=(timeutil.clock() - dt.timedelta(days=2)).date().isoformat())
        self.failed_note('whatsapp', at=timeutil.clock())
        self.assertEqual(app.setup_nudge_view(setup_card.setup_card(self.store, app.config))['id'], 'nudge-retry-whatsapp')
        out = app.setup_card_action('setup_dismiss', {'step': 'hint-nudge-retry-whatsapp'}, True)['setup_card']
        self.assertEqual((out['dismissed'], out['nudge']), (['hint-nudge-retry-whatsapp'], None))  # closed: none other today
        # never without the card
        self.assertIsNone(app.setup_nudge_view(dict(setup_card.setup_card(self.store, app.config), closed=True)))


if __name__ == '__main__':
    unittest.main()
