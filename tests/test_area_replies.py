"""A to-do placed in another area still replies in its own threads, from the account each message came in on, as
next_actions.reply_home has it for email. Its accounts (its area: Work or Personal, sharing) stay as placed, and nothing
else outside its area opens up: no other account, no new message. Offline, made-up data: nothing is sent."""
import json
import tempfile
import types
import unittest
from pathlib import Path
import linear_writes
import machine.main as machine_main
import next_actions as n
import teams_send
import todo_areas

OTHER_LI = {'id': 'other-li', 'service': 'linkedin', 'boundary': 'work:linkedin'}
SLACK = {'id': 'acme-slack', 'service': 'slack', 'boundary': 'work:Acme', 'user_id': 'UOWNER1'}
ACCOUNTS = [
    {'id': 'acme-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@acme.example', 'boundary': 'work:Acme'},
    {'id': 'acme-x', 'service': 'x', 'handle': 'acme', 'boundary': 'work:Acme'},
    {'id': 'acme-teams', 'service': 'teams', 'boundary': 'work:Acme'},
    {'id': 'acme-ic', 'service': 'intercom', 'boundary': 'work:Acme', 'credential': 'read', 'reply_credential': 'reply', 'reply_admin_id': '42'},
    {'id': 'acme-docs', 'service': 'docs', 'boundary': 'work:Acme'},
    {'id': 'side-x', 'service': 'x', 'handle': 'side', 'boundary': 'work:Side', 'scope': 'personal'},
    {'id': 'side-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@side.example', 'boundary': 'work:Side', 'scope': 'personal'},
    {'id': 'me-li', 'service': 'linkedin', 'boundary': 'work:linkedin'}, OTHER_LI, SLACK,
]
CONV = 'urn:li:msg_conversation:(urn:li:fsd_profile:' + 'A' * 60 + ',2-' + 'b' * 60 + '==)'  # as long as the real ones
CONFIG = {'accounts': ACCOUNTS}
SIDE = ['side-x', 'side-mail']


def message(source_id='m1', conversation=CONV, name='Ada Lovelace', account='me-li'):
    return {'account_id': account, 'source_id': source_id, 'kind': 'linkedin.message', 'occurred_at': '2026-11-20T09:00:00+00:00',
            'title': name, 'body': 'Can we talk about Side on Friday?', 'deleted': False,
            'metadata': {'conversation_id': conversation, 'chat_name': name, 'from': name}}


class LinkedIn(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = ACCOUNTS
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': ACCOUNTS, 'prepare_ahead': False, 'database': str(Path(self.temp.name) / 'e.sqlite')}
        self.store.config = self.app.config

    def placed(self, *messages):
        for m in messages or (message(),):
            self.store.commit_page(m['account_id'], {}, [m])
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute('SELECT id FROM events')]
        return self.app.action('suggest', {'dedupe_key': 'ada:side', 'title': 'Answer Ada', 'body': 'Ada asks about **Side**.',
                                           'event_ids': ids, 'company': 'work:Side'})['id']

    def row(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())

    def start(self, sid):
        self.store.decide(sid, 'accept', '', 'click-' + sid, 'dashboard')
        sent = []
        self.app.preparation_step(lambda req: sent.append(req) or {'status': 'admitted'})
        with self.store.connect() as db:
            self.job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (sid,)).fetchone()['job_id']
        return sent[-1]['message']

    def save(self, sid, **draft):
        action = {'kind': 'linkedin', 'label': 'Send reply', 'account_id': 'me-li', 'body': 'Friday works.', **draft}
        self.app.action('prepare', {'suggestion_id': sid, 'job_id': self.job, 'body': 'Reply ready.', 'next_action': action, 'outcome': 'needs_you',
                                    'needs': 'approve the send'})
        return json.loads(self.row(sid)['next_action'])

    def test_a_reply_goes_from_the_account_it_came_in_on_and_the_area_stays(self):
        sid = self.placed()
        before = {k: self.row(sid)[k] for k in ('account_ids', 'area')}
        self.assertEqual((json.loads(before['account_ids']), before['area']), (SIDE, 'work:Side'))
        message = self.start(sid)
        self.assertIn('on me-li', message)
        self.assertIn('thread ' + CONV, message)  # whole: a reply names it
        action = self.save(sid, conversation_id=CONV)
        self.assertEqual((action['account_id'], action['conversation_id'], action['to_name']), ('me-li', CONV, 'Ada Lovelace'))
        self.assertEqual({k: self.row(sid)[k] for k in before}, before)  # still Side's: Personal, never shared with Acme's team
        row = self.row(sid)
        with self.store.connect() as db:
            self.store.card_views(db, [row])
        self.assertEqual(row['scope'], 'personal')

    def test_nothing_else_outside_its_area_opens_up(self):
        sid = self.placed(message(), message('m2', 'urn:li:msg_conversation:(other)', 'Sam Sender', 'other-li'))
        self.start(sid)
        for bad in ({'account_id': 'other-li', 'conversation_id': CONV},           # the owner's other profile
                    {'conversation_id': 'urn:li:msg_conversation:(unknown)'},      # a conversation that isn't the to-do's
                    {'profile': 'ada-l', 'to_name': 'Ada Lovelace'},               # a new message: only its area's accounts
                    {'account_id': 'acme-x', 'conversation_id': CONV}):
            with self.assertRaisesRegex(ValueError, 'LinkedIn account belonging to this task|Reply only in a LinkedIn conversation', msg=bad):
                self.save(sid, **bad)

    def test_the_errors_say_what_to_send(self):
        sid = self.placed()
        self.start(sid)
        with self.assertRaisesRegex(ValueError, r'LinkedIn message fields: event_id\. Leave them out; it takes account_id, body, conversation_id'):
            self.save(sid, conversation_id=CONV, event_id=1)
        with self.assertRaises(ValueError) as caught:
            self.save(sid, conversation_id=CONV[:79] + '…')  # a shortened one, as an older job message had it
        self.assertIn(f'{CONV} (Ada Lovelace, account_id me-li)', str(caught.exception))

    def test_the_only_conversation_is_filled_in_and_never_a_guess(self):
        sid = self.placed()
        self.start(sid)
        self.assertEqual(self.save(sid, to_name='Ada')['conversation_id'], CONV)
        with self.assertRaises(ValueError):  # someone else's name
            self.save(sid, to_name='Sam Sender')

    def test_two_conversations_need_a_name(self):
        sid = self.placed(message(), message('m2', 'urn:li:msg_conversation:(sam)', 'Sam Sender'))
        self.start(sid)
        with self.assertRaises(ValueError):
            self.save(sid)
        self.assertEqual(self.save(sid, to_name='Sam Sender')['conversation_id'], 'urn:li:msg_conversation:(sam)')


class OtherChannels(unittest.TestCase):
    """The same for each kind of send; `found` is what the service read from the to-do's own messages."""

    def check(self, action, **found):
        return n.validate({'body': 'Yes, that works.', **action}, CONFIG, SIDE, **found)

    def test_x(self):
        threads = {'mentions': {'19': {'account_id': 'acme-x', 'screen_name': 'ada', 'name': 'Ada'}}, 'dms': {'4-2': {'account_id': 'acme-x', 'name': 'Ada'}}}
        for spot in ({'reply_to': '19'}, {'conversation_id': '4-2'}):
            self.assertEqual(self.check({'kind': 'x', 'account_id': 'acme-x', **spot}, x_threads=threads)['account_id'], 'acme-x')
            with self.assertRaises(ValueError):  # its area's own account, but not where the thread is
                self.check({'kind': 'x', 'account_id': 'side-x', **spot}, x_threads=threads)
            with self.assertRaises(ValueError):  # not one of its messages
                self.check({'kind': 'x', 'account_id': 'acme-x', **spot}, x_threads={})

    def test_teams_intercom_and_doc_comments(self):
        for kind, account, key, name in (('teams', 'acme-teams', 'chat_id', 'teams_chats'), ('intercom', 'acme-ic', 'conversation_id', 'intercom_conversations'),
                                         ('doc_reply', 'acme-docs', 'comment_id', 'doc_comments')):
            mine = {'7': {'account_id': account, 'name': 'Ada', 'replies': True, 'file_id': 'doc1'}}
            action = {'kind': kind, 'account_id': account, key: '7'}
            self.assertEqual(self.check(action, **{name: mine})['account_id'], account, kind)
            for bad in ({}, {'7': {**mine['7'], 'account_id': 'elsewhere'}}):
                with self.assertRaises(ValueError, msg=kind):
                    self.check(action, **{name: bad})
        self.assertNotIn('allowed_accounts', teams_send.check.__code__.co_varnames)

    def test_an_email_around_an_intercom_conversation_is_still_steered_to_it(self):
        chats = {'7': {'account_id': 'acme-ic', 'contact': 'casey@example.org', 'name': 'Casey'}}
        with self.assertRaisesRegex(ValueError, 'reply there'):
            self.check({'kind': 'email', 'account_id': 'side-mail', 'to': ['casey@example.org'], 'subject': 'Hi', 'label': 'Send'}, intercom_conversations=chats)

    def test_slack_answers_who_wrote_and_nobody_else(self):
        spot = {'service': 'slack', 'account_id': 'acme-slack', 'evidence': True, 'channel_id': 'D0ADA12345', 'ts': '1.2', 'thread_ts': '1.2', 'dm': True,
                'channel_name': 'DM Ada Lovelace', 'sender_id': 'U0ADA1234', 'sender_name': 'Ada Lovelace', 'own': False, 'members': ['U0ADA1234'], 'later': False}
        draft = {'kind': 'slack', 'account_id': 'acme-slack', 'user_id': 'U0ADA1234', 'to_name': 'Ada Lovelace'}
        self.assertEqual(self.check(draft, reply_spots=[spot])['user_id'], 'U0ADA1234')
        for bad, spots in (({'user_id': 'U0SAM1234'}, [spot]), ({'user_id': 'U0SAM1234', 'to_name': 'Sam Sender'}, [spot]), ({}, []),
                           ({}, [{**spot, 'evidence': False}]),  # carried in by a teammate's Machine, not its own message
                           ({'delegate': True}, [spot])):
            with self.assertRaisesRegex(ValueError, 'Slack account of this task'):
                self.check({**draft, **bad}, reply_spots=spots)

    def test_linear_changes_its_own_issue_and_makes_none_there(self):
        import abilities
        linear = {'id': 'acme-linear', 'service': 'linear', 'boundary': 'work:Acme'}
        self.addCleanup(setattr, abilities, 'actions_on', abilities.actions_on)
        abilities.actions_on = lambda account: True
        connector = types.SimpleNamespace(writes_on=lambda config, account, helpers: {'comment', 'create'})
        area = {'boundaries': ['work:Side']}
        issues = {'i1': {'account_id': 'acme-linear'}}
        found = {'accounts': linear_writes.accounts({'accounts': [linear]}, connector, None, area, {'acme-linear'}), 'issues': issues}
        self.assertTrue(found['accounts']['acme-linear']['outside'])
        self.assertIsNone(linear_writes.create_account(found, {}))
        self.assertIsNone(linear_writes.create_account(found, {'account_id': 'acme-linear'}))
        self.assertEqual(linear_writes.accounts({'accounts': [linear]}, connector, None, area), {})  # none of its issues there


class Areas(unittest.TestCase):
    def test_placing_never_widens_the_accounts(self):
        self.assertEqual(todo_areas.company_accounts('work:Side', ACCOUNTS), SIDE)


if __name__ == '__main__':
    unittest.main()
