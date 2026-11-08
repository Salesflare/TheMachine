"""Work or Personal checked against the mail once it is in (machine/sources/scope_check.py): an account + Add had to ask
about, or one guessed Personal in doubt, gets one setup to-do row when the people its owner writes to clearly say the
other; Change or × closes it for good, and it never switches by itself. From the plain From and To only."""
import json
import tempfile
import types
import unittest
from pathlib import Path

import assistant as a
from machine.app.setup_card import SETUP_STEP_RE
from machine.sources import scope_check

ME = 'jules@moreaudesign.io'
FRIENDS = ['ann@gmail.com', 'bo@outlook.com', 'cy@yahoo.com', 'di@icloud.com', 'ed@gmx.de', 'fi@hotmail.com']
CLIENTS = ['ann@initech.dev', 'bo@globex.dev', 'cy@hooli.dev', 'di@umbrella.dev', 'ed@initech.dev']


class ScopeCheck(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.account = {'id': 'moreau-gmail', 'service': 'gmail', 'email': ME, 'boundary': 'work:Moreaudesign',
                        'boundary_by': 'owner', 'scope_check': True}
        self.config = {'accounts': [self.account]}
        self.n = 0

    def sent(self, *to, sender=ME):
        with self.store.connect() as db:
            for address in to:
                self.n += 1
                when = f'2026-11-08T10:{self.n:02d}:00+00:00'
                db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) '
                           'VALUES(?,?,?,?,?,?,?,?,?)', (self.account['id'], f'm{self.n}', 'gmail.message', when, 'Hi', '',
                                                         json.dumps({'from': f'Jules <{sender}>', 'to': f'Someone <{address}>'}), 'h', when))

    def hints(self, team=()):
        return scope_check.scope_hints(self.store, self.config, team)

    def test_an_own_domain_answered_work_whose_mail_is_personal_gets_one_row_until_closed(self):
        self.assertEqual(self.hints(), [])  # no mail yet: nothing to say
        self.sent(*FRIENDS, 'mum@moreaudesign.io')  # family on the family domain says nothing either way
        [hint] = self.hints()
        self.assertEqual(hint['title'], ME + ' looks like personal mail. Change it to Personal?')
        self.assertEqual((hint['button'], hint['scope']), ('Change', {'account': 'moreau-gmail', 'boundary': 'personal:me'}))
        self.assertRegex('hint-' + hint['id'], SETUP_STEP_RE)  # a row the setup to-do can close
        self.assertEqual(self.config['accounts'][0]['boundary'], 'work:Moreaudesign')  # never switched by itself
        self.store.setup_closed('hint-' + hint['id'])  # Change closes it too (setup-card.js), as its × does
        self.sent('gi@gmail.com')
        self.assertEqual(self.hints(), [])

    def test_a_guessed_personal_one_whose_mail_is_work_asks_to_change_it_to_work(self):
        self.account.update(boundary='personal:me', boundary_by='guess')
        self.sent(*CLIENTS)
        [hint] = self.hints()
        self.assertEqual((hint['title'], hint['scope']['boundary']),
                         (ME + ' looks like work mail. Change it to Work?', 'work:Moreaudesign'))
        self.account['boundary'] = 'work:Moreaudesign'  # changed: the mail agrees now
        self.assertEqual(self.hints(), [])

    def test_only_clear_mail_says_anything(self):
        self.account.update(boundary='personal:me')
        self.sent(*CLIENTS[:4])
        self.assertEqual(self.hints(), [])  # too few people
        self.sent('gi@gmail.com')
        self.assertEqual(self.hints(), [])  # mixed: not clear
        self.sent(*FRIENDS, sender='ann@gmail.com')  # mail it got, not mail the owner wrote
        self.assertEqual(self.hints(), [])
        # a Work Fleet teammate's company among them, none at a mail provider: work
        self.assertEqual(scope_check.mailbox_says(self.account, {'a@acme.dev', 'b@acme.dev', 'c@acme.dev', 'd@acme.dev', 'e@acme.dev'},
                                                  {'acme.dev'}), 'work')
        self.assertIsNone(scope_check.mailbox_says(self.account, {'a@acme.dev', 'b@acme.dev', 'c@acme.dev', 'd@acme.dev', 'e@acme.dev'}))

    def test_only_accounts_marked_for_it(self):
        self.sent(*FRIENDS)
        for change in ({'scope_check': False}, {'service': 'calendar'}, {'shared': {'by': 'Kim'}}, {'boundary': 'owner:machine'}):
            with self.subTest(change=change):
                self.config = {'accounts': [{**self.account, **change}]}
                self.assertEqual(self.hints(), [])

    def test_the_setup_todo_shows_it_on_a_self_hosted_machine_too(self):
        self.sent(*FRIENDS)
        app = types.SimpleNamespace(store=self.store, config=self.config, team_domains=lambda: set())
        hints = a.App.setup_hints_view(app)
        self.assertEqual([h['id'] for h in hints], [scope_check.hint_id(self.account)])  # no manage_url: no other hints


if __name__ == '__main__':
    unittest.main()
