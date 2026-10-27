"""Sending from an alias (own_addresses.senders, next_actions.pick_sender, EmailTransport.alias_check): a draft may go
out from an alias of the owner's that Gmail confirms this mailbox sends as; a reply to mail that came to it starts
from it; the owner picks the From in the review; and the send checks Gmail again, sending nothing it doesn't confirm."""
import json
import unittest
from unittest.mock import patch

import ms_graph
import next_actions as n
import own_addresses as oa
import test_next_actions as tn

NOW = '2026-10-27T09:00:00+00:00'
MAILBOX = 'owner@example.com'
CONFIG = {'accounts': [{'id': 'work', 'email': MAILBOX, 'client': 'existing', 'service': 'gmail', 'transport': 'gog'},
                       {'id': 'ms', 'email': 'owner@corp.test', 'service': 'outlook', 'transport': 'graph'}]}


def gmail_list(*entries):
    return {'sendAs': [{'sendAsEmail': MAILBOX, 'isPrimary': True}, *entries]}


def keep(db, config=CONFIG, gmail=None, outlook=None, states=None, chosen=None):
    """The kept send-as lists, the detected addresses and the owner's choices, as a build and Settings leave them."""
    oa.ensure(db)
    oa.save_fetched(db, 'work', oa.send_as_entries(gmail or gmail_list(), MAILBOX), NOW)
    if outlook is not None:
        oa.save_fetched(db, 'ms', oa.send_as_entries(outlook, 'owner@corp.test'), NOW)
    for address, state in (states or {}).items():
        db.execute('INSERT OR REPLACE INTO own_addresses(address,sources,state,reason,updated_at) VALUES(?,?,?,?,?)',
                   (address, json.dumps(['alias']), state, None, NOW))
    for address, choice in (chosen or {}).items():
        db.execute('INSERT OR REPLACE INTO own_address_choices(address,choice,at) VALUES(?,?,?)', (address, choice, NOW))


class Senders(unittest.TestCase):
    def setUp(self):
        import sqlite3
        self.db = sqlite3.connect(':memory:')

    def test_only_verified_aliases_marked_mine_are_offered(self):
        keep(self.db, gmail=gmail_list({'sendAsEmail': 'partnerships@example.com', 'verificationStatus': 'accepted'},
                                       {'sendAsEmail': 'owner.l@example.com', 'verificationStatus': 'accepted'},
                                       {'sendAsEmail': 'pending@example.com', 'verificationStatus': 'pending'},
                                       {'sendAsEmail': 'unsure@example.com', 'verificationStatus': 'accepted'},
                                       {'sendAsEmail': 'sales@example.com', 'verificationStatus': 'accepted'},
                                       {'sendAsEmail': 'gone@example.com', 'verificationStatus': 'accepted'},
                                       {'sendAsEmail': 'relay@example.com', 'verificationStatus': 'accepted',
                                        'smtpMsa': {'host': 'smtp.other.test', 'username': 'someone@other.test'}}),
             states={'partnerships@example.com': 'maybe', 'owner.l@example.com': 'yours', 'pending@example.com': 'yours',
                     'unsure@example.com': 'maybe', 'sales@example.com': 'maybe', 'gone@example.com': 'yours',
                     'relay@example.com': 'yours'},
             chosen={'partnerships@example.com': 'confirm', 'sales@example.com': 'team', 'gone@example.com': 'remove'})
        # Mine (chosen) and found as theirs: offered. Pending at Gmail, never chosen, the team's, Not mine, or sent
        # through someone else's server: not.
        self.assertEqual(oa.senders(self.db, CONFIG)['work'], [MAILBOX, 'partnerships@example.com', 'owner.l@example.com'])

    def test_outlook_only_ever_offers_the_mailbox_address(self):
        answer = ms_graph.send_as({'mail': 'owner@corp.test', 'proxyAddresses': ['SMTP:owner@corp.test', 'smtp:sales@corp.test']})
        self.assertEqual([e['verified'] for e in oa.send_as_entries(answer, 'owner@corp.test')], [True, False])
        keep(self.db, outlook=answer, states={'sales@corp.test': 'maybe'}, chosen={'sales@corp.test': 'confirm'})
        self.assertEqual(oa.senders(self.db, CONFIG)['ms'], ['owner@corp.test'])

    def test_a_list_kept_before_verified_was_stored_offers_nothing_until_read_again(self):
        oa.ensure(self.db)
        old = [{'address': MAILBOX, 'primary': True, 'alias': True, 'name': '', 'other_server': False},
               {'address': 'partnerships@example.com', 'primary': False, 'alias': True, 'name': '', 'other_server': False}]
        oa.save_fetched(self.db, 'work', old, NOW)
        keep_states = {'partnerships@example.com': 'yours'}
        for address, state in keep_states.items():
            self.db.execute("INSERT INTO own_addresses VALUES(?,?,?,?,?)", (address, '["alias"]', state, None, NOW))
        self.assertEqual(oa.senders(self.db, CONFIG)['work'], [MAILBOX])


class DefaultFrom(unittest.TestCase):
    OPTIONS = [MAILBOX, 'partnerships@example.com']

    def test_a_reply_to_mail_that_came_to_the_alias_starts_from_it(self):
        self.assertEqual(n.pick_sender(MAILBOX, self.OPTIONS, {'to': ['partnerships@example.com'], 'from': 'pat@client.test'}),
                         'partnerships@example.com')

    def test_mail_to_the_mailbox_too_starts_from_the_mailbox(self):
        self.assertEqual(n.pick_sender(MAILBOX, self.OPTIONS, {'to': ['partnerships@example.com', MAILBOX]}), MAILBOX)

    def test_after_the_owners_own_message_it_keeps_the_address_they_sent_from(self):
        self.assertEqual(n.pick_sender(MAILBOX, self.OPTIONS, {'to': ['pat@client.test'], 'from': 'partnerships@example.com', 'sent': True}),
                         'partnerships@example.com')

    def test_new_mail_and_unknown_addresses_start_from_the_mailbox(self):
        self.assertEqual(n.pick_sender(MAILBOX, self.OPTIONS, None), MAILBOX)
        self.assertEqual(n.pick_sender(MAILBOX, self.OPTIONS, {'to': ['other@example.com']}), MAILBOX)
        self.assertEqual(n.pick_sender(MAILBOX, [MAILBOX], {'to': ['partnerships@example.com']}), MAILBOX)

    def test_validate_offers_the_picker_and_picks_the_default(self):
        draft = {'kind': 'email', 'account_id': 'work', 'to': ['pat@client.test'], 'subject': 'Re: Partnership', 'body': 'Thanks.',
                 'thread_id': 'abc123', 'in_reply_to': '<m1@client.test>'}
        senders = {'work': self.OPTIONS}
        replied = {'<m1@client.test>': {'to': ['partnerships@example.com'], 'from': 'pat@client.test', 'sent': False}}
        got = n.validate(draft, CONFIG, ['work'], senders=senders, replied=replied)
        self.assertEqual((got['from'], got['from_options']), ('partnerships@example.com', self.OPTIONS))
        new = n.validate({k: v for k, v in draft.items() if k not in ('thread_id', 'in_reply_to')}, CONFIG, ['work'], senders=senders)
        self.assertEqual(new['from'], MAILBOX)
        plain = n.validate(draft, CONFIG, ['work'], senders={'work': [MAILBOX]}, replied=replied)
        self.assertEqual(plain['from'], MAILBOX)
        self.assertNotIn('from_options', plain)
        # The draft can't name its own From
        with self.assertRaises(ValueError):
            n.validate({**draft, 'from': 'partnerships@example.com'}, CONFIG, ['work'], senders=senders, replied=replied)


class StrictCheck(unittest.TestCase):
    def action(self, sender='partnerships@example.com', options=(MAILBOX, 'partnerships@example.com')):
        return {'kind': 'email', 'account_id': 'work', 'from': sender, 'from_options': list(options), 'to': ['pat@client.test'],
                'cc': [], 'bcc': [], 'subject': 'Re: Partnership', 'body': 'Thanks.', 'signature': False}

    def preflight(self, action, alias_answer):
        def read(config, account, api, version, method, params, scope):
            self.assertEqual(scope, 'https://www.googleapis.com/auth/gmail.readonly')  # never a new scope
            if method == 'gmail.users.getProfile':
                return {'emailAddress': MAILBOX}
            if method == 'gmail.users.settings.sendAs.get':
                self.asked.append(params['sendAsEmail'])
                if isinstance(alias_answer, Exception):
                    raise alias_answer
                return alias_answer
            raise AssertionError(method)
        self.asked = []
        transport = n.EmailTransport(CONFIG, lambda *_: 'secret', read)
        with patch.object(n, 'granted_scopes', return_value=set(n.SEND_SCOPES)):
            return transport.preflight(action)

    def test_an_alias_gmail_confirms_right_now_passes(self):
        self.preflight(self.action(), {'sendAsEmail': 'partnerships@example.com', 'verificationStatus': 'accepted'})
        self.assertEqual(self.asked, ['partnerships@example.com'])

    def test_an_alias_gmail_does_not_confirm_sends_nothing(self):
        for answer in ({'sendAsEmail': 'partnerships@example.com', 'verificationStatus': 'pending'},
                       {'sendAsEmail': 'partnerships@example.com'},
                       {'sendAsEmail': 'other@example.com', 'verificationStatus': 'accepted'},
                       {'sendAsEmail': 'partnerships@example.com', 'verificationStatus': 'accepted',
                        'smtpMsa': {'host': 'smtp.other.test', 'username': 'someone@other.test'}},
                       {}, RuntimeError('404')):
            with self.subTest(answer=answer), self.assertRaisesRegex(ValueError, 'Nothing was sent'):
                self.preflight(self.action(), answer)

    def test_the_mailbox_address_needs_no_alias_check(self):
        self.preflight(self.action(sender=MAILBOX), AssertionError('not asked'))
        self.assertEqual(self.asked, [])

    def test_an_address_the_draft_did_not_offer_is_refused_before_asking(self):
        with self.assertRaisesRegex(ValueError, 'sender account changed'):
            self.preflight(self.action(sender='sales@example.com'), {'sendAsEmail': 'sales@example.com', 'verificationStatus': 'accepted'})
        with self.assertRaisesRegex(ValueError, 'sender account changed'):
            self.preflight(self.action(options=()), {'sendAsEmail': 'partnerships@example.com', 'verificationStatus': 'accepted'})
        self.assertEqual(self.asked, [])

    def test_outlook_never_sends_from_another_address(self):
        transport = n.EmailTransport(CONFIG, lambda *_: 'secret', lambda *a: self.fail('no read'))
        with self.assertRaisesRegex(ValueError, 'sender account changed'):
            transport.account({**self.action(), 'account_id': 'ms', 'from': 'sales@corp.test',
                               'from_options': ['owner@corp.test', 'sales@corp.test']})


class ReviewChoice(unittest.TestCase):
    """The owner's pick in the review travels with their approval, only from what the draft offered."""
    setUp, row, decide = tn.ux.UX.setUp, tn.ux.UX.row, tn.ux.UX.decide
    draft, ready, action_job, transport = tn.NextActions.draft, tn.NextActions.ready, tn.NextActions.action_job, tn.NextActions.transport

    def app(self):
        app = tn.NextActions.app(self)
        with self.store.connect() as db:
            keep(db, config=app.config, gmail=gmail_list({'sendAsEmail': 'partnerships@example.com', 'verificationStatus': 'accepted'},
                                                         {'sendAsEmail': 'sales@example.com', 'verificationStatus': 'accepted'}),
                 states={'partnerships@example.com': 'maybe', 'sales@example.com': 'maybe'}, chosen={'partnerships@example.com': 'confirm'})
        return app

    def approve(self, **extra):
        action = self.row()['next_action']
        return self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': action['revision'], 'approval_id': 'tap', **extra},
                                 owner_dashboard=True)

    def test_new_mail_offers_the_picker_from_the_mailbox(self):
        action = self.ready()
        self.assertEqual((action['from'], action['from_options']), (MAILBOX, [MAILBOX, 'partnerships@example.com']))

    def test_the_picked_alias_is_what_goes_out(self):
        self.ready()
        with self.assertRaisesRegex(ValueError, 'addresses offered'):
            self.approve(sender='sales@example.com')  # Gmail lists it, but it isn't the owner's
        self.approve(sender='partnerships@example.com')
        job = self.action_job()
        self.assertEqual(json.loads(job['payload'])['from'], 'partnerships@example.com')
        sent = []
        self.app().action_step(self.transport(send=lambda action, job: (sent.append(action['from']), {'message_id': 'ok'})[1]))
        self.assertEqual(sent, ['partnerships@example.com'])

    def test_no_pick_sends_from_the_default_shown(self):
        self.ready()
        self.approve()
        self.assertEqual(json.loads(self.action_job()['payload'])['from'], MAILBOX)


if __name__ == '__main__':
    unittest.main()
