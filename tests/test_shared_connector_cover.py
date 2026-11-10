"""A Fleet-shared Intercom (or Stripe) the owner also connects themselves: one reader, and replies there.

Seen on a teammate's hosted Machine (2026-11-10): an admin shared the company's Intercom through the Work Fleet, which
only reads. The teammate then signed in with Intercom themselves (replies on). Both connections read the same
workspace, so every conversation came in twice, and a to-do drafted before kept its email with "Intercom is shared with
you to read only", as if Intercom still couldn't reply. Now the share rests while the owner's own connection reads that
workspace, what it brought in becomes the own connection's (each conversation kept once), and such a to-do is drafted
again as a reply in Intercom, once, for the owner's Send. The share's card says it rests, and a connection without an
address of its own is called what it is ("Intercom"), never its id. No live calls: Intercom is the fake of
test_intercom_replies, which records every request."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from connectors import intercom
from machine import names
from machine.app import serve
import shared_connectors as sc
from test_intercom_replies import ACCOUNT, Fake, READ, REPLY, SHARED, a, conversation
import types

MAIL = {'id': 'mail', 'service': 'gmail', 'transport': 'gog', 'email': 'alex@example.com', 'boundary': 'work:Example Support'}
STRIPE_SHARED = {'id': 'stripe-f1', 'service': 'stripe', 'transport': 'api', 'stripe_account': 'acct_1', 'credential': 'shared-stripe-f1',
                 'shared': {'fleet': 'f1', 'service': 'stripe', 'grant': 'g2'}}


class Covered(unittest.TestCase):
    def test_a_share_is_covered_by_the_owners_own_connection_to_the_same_workspace(self):
        accounts = [dict(SHARED), dict(ACCOUNT)]
        self.assertEqual(sc.covered_by(accounts, accounts[0]), 'intercom')
        self.assertIsNone(sc.covered_by(accounts, accounts[1]))  # the own one is never covered
        self.assertIsNone(sc.covered_by([SHARED, {**ACCOUNT, 'workspace_id': 'other'}], SHARED))  # another workspace
        self.assertIsNone(sc.covered_by([SHARED, {**ACCOUNT, 'signals': False}], SHARED))  # the own one doesn't read: the share does
        self.assertIsNone(sc.covered_by([SHARED, {**ACCOUNT, 'shared': {'fleet': 'f2', 'grant': 'g9'}}], SHARED))  # two shares
        sharer = {**ACCOUNT, 'shared': {'fleet': 'f1', 'origin': True}}  # the admin who shares it reads it as their own
        self.assertIsNone(sc.covered_by([sharer, SHARED], sharer))
        self.assertEqual(sc.covered_by([sharer, SHARED], SHARED), 'intercom')
        own_stripe = {'id': 'work-stripe', 'service': 'stripe', 'transport': 'broker', 'stripe_account': 'acct_1'}
        self.assertEqual(sc.covered_by([STRIPE_SHARED, own_stripe], STRIPE_SHARED), 'work-stripe')
        self.assertIsNone(sc.covered_by([STRIPE_SHARED, {**own_stripe, 'stripe_account': 'acct_2'}], STRIPE_SHARED))

    def test_a_covered_share_starts_no_sync(self):
        source = Path(serve.__file__).read_text(encoding='utf-8')
        self.assertIn('shared_connectors.merge_covered(self.config', source)
        self.assertLess(source.index('shared_connectors.merge_covered('), source.index('if shared_connectors.covered_by(self.config'))
        self.assertLess(source.index('if shared_connectors.covered_by(self.config'), source.index('target=self.collector'))


class Names(unittest.TestCase):
    def test_a_connection_without_an_address_is_called_what_it_is(self):
        shared = {k: v for k, v in SHARED.items() if k != 'email'}
        self.assertEqual(names.account_name(shared, [shared, MAIL]), 'Intercom')
        self.assertEqual(names.account_name(STRIPE_SHARED, [STRIPE_SHARED]), 'Stripe')
        self.assertEqual(names.account_name(shared, [shared, ACCOUNT]), 'Intercom')  # the same workspace: its card says it rests
        # Two workspaces: the workspace tells them apart
        self.assertEqual(names.account_name(shared, [shared, {**ACCOUNT, 'workspace_id': 'other', 'workspace_name': 'Other Co'}]), 'Intercom · Example Support')
        self.assertEqual(names.account_name({**ACCOUNT, 'email': 'alex@example.com'}, [shared, ACCOUNT]), 'alex@example.com')
        self.assertEqual(names.account_name({'id': 'trello-x', 'service': 'trello'}, [], 'Trello board'), 'Trello board')
        for account in (shared, STRIPE_SHARED):
            self.assertNotIn(account['id'], names.account_name(account, [account]))


class OwnSignIn(unittest.TestCase):
    """The teammate's day: a to-do from the shared Intercom drafted by email, then their own sign-in."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.fake = Fake(self)
        patch('urllib.request.OpenerDirector.open', side_effect=self.fake.respond).start()
        self.addCleanup(patch.stopall)
        tokens = {'intercom': READ, 'intercom-reply': REPLY, 'shared-intercom-f1': READ}
        self.helpers = types.SimpleNamespace(SourceError=a.SourceError, Skips=a.CONNECTOR_HELPERS.Skips, iso=a.CONNECTOR_HELPERS.iso,
                                             credential=lambda config, name: tokens[name])
        self.accounts = [dict(SHARED), dict(MAIL)]  # only the share at first
        self.store.accounts = self.accounts
        self.store.commit_page(SHARED['id'], {}, [intercom.event(SHARED, conversation(), self.helpers)])
        self.store.commit_page(SHARED['id'], {}, [intercom.event(SHARED, {**conversation(), 'id': '9', 'title': 'Other'}, self.helpers)])
        with self.store.connect() as db:
            self.shared_event = db.execute("SELECT id FROM events WHERE source_id='7'").fetchone()[0]
        self.sid = self.store.suggest('ic-task', 'Answer Casey', 'Casey asks about exporting.', [self.shared_event])['id']
        self.store.decide(self.sid, 'accept', '', 'accept-' + self.sid, 'dashboard')

    def app(self):
        app = object.__new__(a.App)
        app.store, app.config = self.store, {'accounts': self.accounts}
        return app

    def save(self, action):
        return self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Reply ready.', 'next_action': action})

    def email(self, **extra):
        self.save({'kind': 'email', 'account_id': 'mail', 'to': ['casey@example.org'], 'subject': 'Your export question',
                   'body': 'Yes, under Settings > Export.', **extra})

    def row(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())

    def prepared(self):
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='done' WHERE suggestion_id=?", (self.sid,))
            db.execute("UPDATE suggestions SET status='prepared' WHERE id=?", (self.sid,))

    def sign_in(self):
        """The owner signs in with Intercom themselves: an own connection with replies, whose first read finds the same
        conversation (a twin of the share's) and another."""
        self.accounts.append(dict(ACCOUNT))
        self.store.commit_page('intercom', {}, [intercom.event(ACCOUNT, conversation(), self.helpers),
                                                intercom.event(ACCOUNT, {**conversation(), 'id': '10', 'title': 'New'}, self.helpers)])

    def test_the_email_drafted_while_intercom_only_read_becomes_a_reply_there(self):
        self.email()
        self.assertEqual(json.loads(self.row()['next_action'])['intercom_fallback'], 'shared')
        self.prepared()
        self.assertEqual(self.store.redraft_intercom_emails(), [])  # nothing can reply yet
        self.sign_in()
        moved = sc.merge_covered(self.accounts, self.store)
        self.assertEqual(moved, {SHARED['id']: 2})
        with self.store.connect() as db:
            rows = [tuple(r) for r in db.execute("SELECT id,account_id,source_id FROM events WHERE kind='intercom.conversation' ORDER BY source_id")]
        # each conversation once, all the own connection's; the to-do's message is the one it had
        self.assertEqual([(r[1], r[2]) for r in rows], [('intercom', '10'), ('intercom', '7'), ('intercom', '9')])
        self.assertIn((self.shared_event, 'intercom', '7'), rows)
        card = self.row()
        self.assertEqual((json.loads(card['event_ids']), json.loads(card['account_ids'])), ([self.shared_event], ['intercom']))
        self.assertEqual(sc.merge_covered(self.accounts, self.store), {})  # once

        self.assertEqual(self.store.redraft_intercom_emails(), [self.sid])
        card = self.row()
        self.assertEqual(card['status'], 'accepted')
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM preparations WHERE suggestion_id=?', (self.sid,)).fetchone()[0], 'queued')
            self.assertEqual(db.execute("SELECT choice,source FROM decisions WHERE id=?", ('intercom-replies:' + self.sid,)).fetchone()[:],
                             ('prepare_ahead', 'intercom_replies'))
            owner, _ = self.app().card_chat_service(db, self.sid)
        self.assertIn('Intercom replies are on: writing the reply there', [e['text'] for e in owner if e.get('kind') == 'event'])
        # The new run: an email to the customer is refused now, the reply in the conversation is taken
        with self.assertRaisesRegex(ValueError, 'reply there'):
            self.email()
        self.save({'kind': 'intercom', 'label': 'Send reply', 'account_id': 'intercom', 'conversation_id': '7', 'body': 'Yes, under Settings > Export.'})
        action = json.loads(self.row()['next_action'])
        self.assertEqual((action['kind'], action['account_id'], action['admin_id']), ('intercom', 'intercom', '42'))
        self.prepared()
        self.assertEqual(self.store.redraft_intercom_emails(), [])  # once
        self.assertEqual(self.fake.writes(), [])  # nothing went anywhere: a draft waits for the owner's Send

    def test_a_to_do_made_from_the_own_copy_points_at_the_kept_one(self):
        self.sign_in()
        with self.store.connect() as db:
            twin = db.execute("SELECT id FROM events WHERE account_id='intercom' AND source_id='7'").fetchone()[0]
        other = self.store.suggest('ic-twin', 'Answer Casey again', 'The same conversation, from the own connection.', [twin])['id']
        sc.merge_covered(self.accounts, self.store)
        with self.store.connect() as db:
            self.assertIsNone(db.execute('SELECT 1 FROM events WHERE id=?', (twin,)).fetchone())
            self.assertEqual(json.loads(db.execute('SELECT event_ids FROM suggestions WHERE id=?', (other,)).fetchone()[0]), [self.shared_event])

    def test_a_sent_or_closed_to_do_is_left_alone(self):
        self.email()
        self.prepared()
        self.sign_in()
        sc.merge_covered(self.accounts, self.store)
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='completed' WHERE id=?", (self.sid,))
        self.assertEqual(self.store.redraft_intercom_emails(), [])

    def test_the_shares_card_says_it_rests_and_names_no_id(self):
        self.sign_in()
        self.store.config = {'accounts': self.accounts}
        cards = {c['id']: c for c in self.store.snapshot(self.accounts)['connectors']}
        self.assertEqual(cards[SHARED['id']]['covered_by'], 'Intercom')
        self.assertIsNone(cards['intercom']['covered_by'])
        self.assertNotIn(SHARED['id'], cards[SHARED['id']]['display_name'])


if __name__ == '__main__':
    unittest.main()
