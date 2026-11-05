"""A Slack reply to a to-do from a Slack message goes in that message's thread (DM or channel), a WhatsApp reply quotes
its message, and the draft says so. A message carried in through a Fleet that this Machine has itself is found too.
Made-up data, no live sends: the transports' calls are patched."""
import datetime
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import next_actions as n
import test_ux as ux
a = ux.a

GMAIL = {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Example'}
SLACK = {'id': 'slack', 'service': 'slack', 'transport': 'maton', 'boundary': 'work:Example', 'credential': 'maton',
         'credential_variable': 'KEY', 'connection_id': 'conn-1', 'user_id': 'UOWNER1'}
WHATSAPP = {'id': 'wa', 'service': 'whatsapp', 'store': '/nonexistent/wacli', 'boundary': 'personal'}
DM, CHANNEL = 'D0SAM1234', 'C0GENERAL1'


def slack(source_id, at, user, ts, channel=DM, text='Can you test the merged changes?', thread=None, name='DM Sam Peeters',
          sender='Sam Peeters', kind='dm'):
    return {'account_id': 'slack', 'source_id': source_id, 'kind': 'slack.message', 'occurred_at': at, 'title': '#' + name,
            'body': text, 'deleted': False,
            'metadata': {'channel_id': channel, 'channel_name': name, 'conversation_type': kind, 'user_id': user,
                         'message_ts': ts, 'thread_ts': thread or ts, 'sender_display': sender}}


def whatsapp(source_id, at, mid, chat='32470000001@s.whatsapp.net', text='Are we still on for Friday?', from_me=False):
    return {'account_id': 'wa', 'source_id': source_id, 'kind': 'whatsapp.message', 'occurred_at': at, 'title': 'Sam',
            'body': text, 'deleted': False,
            'metadata': {'chat_id': chat, 'chat_name': 'Sam', 'message_id': mid, 'from_me': from_me,
                         'sender_id': None if from_me else '32470000001@s.whatsapp.net'}}


class ReplyPlace(unittest.TestCase):
    row = ux.UX.row
    decide = ux.UX.decide

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.owner_user_ids = {'UOWNER1'}

    def card(self, account, events, evidence=None):
        self.store.commit_page(account, {}, events)
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute('SELECT id FROM events WHERE source_id IN (%s)' % ','.join('?' * len(evidence or events)),
                                            [e['source_id'] for e in evidence or events])]
        self.sid = self.store.suggest('card-' + events[0]['source_id'], 'Reply to Sam', 'Sam asked something.', ids)['id']

    def app(self):
        app = object.__new__(a.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL, SLACK, WHATSAPP]}
        return app

    def ready(self, action, **extra):
        self.decide('accept')
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Reply ready.', 'next_action': action, 'outcome': 'needs_you',
                                      'needs': 'approve the send', **extra})
        return self.row()['next_action']

    def slack_action(self, **extra):
        return {'kind': 'slack', 'label': 'Send to Sam', 'account_id': 'slack', 'to_email': 'sam@example.com', 'to_name': 'Sam Peeters',
                'body': 'Tested, no issues', **extra}

    def test_a_reply_to_an_older_dm_goes_in_its_thread(self):
        old = slack('s1', '2026-10-29T19:30:39.457159+00:00', 'UOWNER1', '1793302239.457159', text='I can test after dinner')
        later = slack('s2', '2026-11-02T10:00:00+00:00', 'U0SAM1234', '1793613600.000100', text='Something else')
        self.card('slack', [old, later], evidence=[old])
        action = self.ready(self.slack_action())
        self.assertEqual(action['thread'], {'channel_id': DM, 'ts': '1793302239.457159', 'dm': True})
        self.assertIn('Slack message to Sam Peeters (sam@example.com), in thread', n.preview(action))

    def test_the_last_message_of_a_dm_gets_a_plain_reply(self):
        self.card('slack', [slack('s1', '2026-11-05T09:00:00+00:00', 'U0SAM1234', '1793869200.000100')])
        action = self.ready(self.slack_action())
        self.assertNotIn('thread', action)
        self.assertNotIn('in thread', n.preview(action))

    def test_a_message_already_in_a_thread_is_answered_there(self):
        self.card('slack', [slack('s1', '2026-11-05T09:00:00+00:00', 'U0SAM1234', '1793869200.000100', thread='1793860000.000200')])
        self.assertEqual(self.ready(self.slack_action(user_id='U0SAM1234', to_email=None))['thread']['ts'], '1793860000.000200')

    def test_a_channel_message_is_answered_in_its_thread_there(self):
        self.card('slack', [slack('s1', '2026-11-05T09:00:00+00:00', 'U0SAM1234', '1793869200.000100', channel=CHANNEL, name='general', kind='channel')])
        action = self.ready(self.slack_action(user_id='U0SAM1234', to_email=None))
        self.assertEqual(action['thread'], {'channel_id': CHANNEL, 'ts': '1793869200.000100', 'dm': False, 'channel_name': 'general'})
        self.assertIn('in thread in #general', n.preview(action))

    def test_someone_else_or_an_unknown_message_keeps_the_direct_message(self):
        self.card('slack', [slack('s1', '2026-11-05T09:00:00+00:00', 'U0ALEX123', '1793869200.000100', channel=CHANNEL, name='general',
                                  sender='Alex Moreau', kind='channel')])
        self.assertNotIn('thread', self.ready(self.slack_action()))  # a DM to Sam about Alex's channel message: not Alex's thread
        with self.assertRaises(ValueError):  # a draft never names a thread itself
            n.validate(self.slack_action(thread={'channel_id': CHANNEL, 'ts': '1.2'}), {'accounts': [SLACK]}, ['slack'])

    def test_a_message_carried_through_a_fleet_finds_the_owners_own_copy(self):
        old = slack('s1', '2026-10-29T19:30:39.457159+00:00', 'UOWNER1', '1793302239.457159', text='I can test after dinner :sweat_smile:')
        later = slack('s2', '2026-11-02T10:00:00+00:00', 'U0SAM1234', '1793613600.000100', text='Something else')
        self.store.commit_page('slack', {}, [old, later])
        carried = {'account_id': 'work', 'source_id': 'fleet:q1:0', 'kind': 'fleet.message', 'occurred_at': old['occurred_at'],
                   'title': '#DM Owner: I can test after dinner', 'body': 'I can test after dinner :sweat_smile:', 'deleted': False,
                   'metadata': {'from': 'Unknown sender', 'carried_by': 'Sam Peeters', 'fleet_kind': 'handoff'}}
        self.card('work', [carried])
        self.assertEqual(self.ready(self.slack_action())['thread']['ts'], '1793302239.457159')

    def test_a_carried_message_it_doesnt_have_asks_for_context(self):
        carried = {'account_id': 'work', 'source_id': 'fleet:q2:0', 'kind': 'fleet.message', 'occurred_at': '2026-10-20T09:00:00+00:00',
                   'title': '#general: release tomorrow?', 'body': 'Release tomorrow?', 'deleted': False,
                   'metadata': {'from': 'Unknown sender', 'carried_by': 'Sam Peeters', 'fleet_kind': 'handoff'}}
        self.card('work', [carried])
        self.decide('accept')
        with self.assertRaises(ValueError) as caught:
            self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Reply ready.', 'next_action': self.slack_action(),
                                          'outcome': 'needs_you', 'needs': 'approve the send'})
        self.assertIn("can't go in the thread of the message it answers (from 2026-10-20)", str(caught.exception))
        # once it says what it answers, the run saves it on purpose
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Reply ready.', 'outcome': 'needs_you', 'needs': 'approve the send',
                                      'next_action': self.slack_action(body='About the release you asked about: tested, no issues'), 'checked': True})
        self.assertNotIn('thread', self.row()['next_action'])

    def test_a_whatsapp_reply_quotes_its_message_when_more_came_since(self):
        first = whatsapp('w1', '2026-11-01T09:00:00+00:00', '3EB0AAAA0001')
        then = whatsapp('w2', '2026-11-03T09:00:00+00:00', '3EB0AAAA0002', text='Other news', from_me=True)
        self.card('wa', [first, then], evidence=[first])
        action = self.ready({'kind': 'whatsapp', 'label': 'Send reply', 'account_id': 'wa', 'chat_id': '32470000001@s.whatsapp.net',
                             'body': 'Yes, Friday works'})
        self.assertEqual(action['quote'], {'message_id': '3EB0AAAA0001', 'sender_id': '32470000001@s.whatsapp.net'})
        self.assertIn('WhatsApp message to Sam, as a reply', n.preview(action))


class Transports(unittest.TestCase):
    def slack_send(self, action, replies):
        calls = []

        class Response(io.BytesIO):
            def __init__(self, body):
                super().__init__(json.dumps(body).encode())
                self.headers = {'Maton-Connection': 'conn-1'}
            def __enter__(self): return self
            def __exit__(self, *_): self.close()

        def urlopen(request, timeout):
            method = request.full_url.split('/api/')[1].split('?')[0]
            calls.append((method, json.loads(request.data) if request.data else request.full_url))
            return Response(replies[method])
        sender = n.SlackTransport({'accounts': [SLACK]}, lambda config, name: 'KEY=secret')
        with patch('urllib.request.urlopen', urlopen):
            return sender.send(action, {'id': 'job', 'created_at': '2026-11-05T09:00:00+00:00'}), calls

    USER = {'ok': True, 'user': {'id': 'U0SAM1234', 'real_name': 'Sam Peeters'}}
    BASE = {'kind': 'slack', 'account_id': 'slack', 'user_id': 'U0SAM1234', 'to_name': 'Sam Peeters', 'body': 'Tested, no issues'}

    def test_a_dm_thread_posts_with_its_thread_ts(self):
        action = {**self.BASE, 'thread': {'channel_id': DM, 'ts': '1793302239.457159', 'dm': True}}
        result, calls = self.slack_send(action, {'users.info': self.USER, 'conversations.open': {'ok': True, 'channel': {'id': DM, 'is_im': True, 'user': 'U0SAM1234'}},
                                                 'chat.postMessage': {'ok': True, 'ts': '1793900000.000100'}})
        self.assertEqual(result['message_id'], f'slack:{DM}:1793900000.000100')
        self.assertEqual((calls[-1][0], calls[-1][1]['channel'], calls[-1][1]['thread_ts']), ('chat.postMessage', DM, '1793302239.457159'))

    def test_a_dm_thread_in_another_conversation_posts_nothing(self):
        action = {**self.BASE, 'thread': {'channel_id': 'D0OTHER99', 'ts': '1.2', 'dm': True}}
        result, calls = self.slack_send(action, {'users.info': self.USER, 'conversations.open': {'ok': True, 'channel': {'id': DM, 'is_im': True}},
                                                 'chat.postMessage': {'ok': True, 'ts': '9.9'}})
        self.assertEqual(result, {'rejected': 'wrong_conversation'})
        self.assertNotIn('chat.postMessage', [c[0] for c in calls])

    def test_a_channel_thread_posts_there_without_opening_a_dm(self):
        action = {**self.BASE, 'thread': {'channel_id': CHANNEL, 'ts': '1793869200.000100', 'dm': False, 'channel_name': 'general'}}
        result, calls = self.slack_send(action, {'users.info': self.USER, 'chat.postMessage': {'ok': True, 'ts': '9.9'}})
        self.assertEqual([c[0] for c in calls], ['users.info', 'chat.postMessage'])
        self.assertEqual((calls[-1][1]['channel'], calls[-1][1]['thread_ts']), (CHANNEL, '1793869200.000100'))
        self.assertEqual(result['channel_id'], CHANNEL)

    def test_without_a_thread_the_post_is_as_before(self):
        _, calls = self.slack_send(self.BASE, {'users.info': self.USER, 'conversations.open': {'ok': True, 'channel': {'id': DM}},
                                               'chat.postMessage': {'ok': True, 'ts': '9.9'}})
        self.assertNotIn('thread_ts', calls[-1][1])

    def test_a_thread_reply_is_reconciled_from_the_thread(self):
        sender = n.SlackTransport({'accounts': [SLACK]}, lambda config, name: 'KEY=secret')
        action = {**self.BASE, 'thread': {'channel_id': CHANNEL, 'ts': '1793869200.000100', 'dm': False, 'channel_name': 'general'}}
        seen = []
        replies = {'users.info': self.USER, 'conversations.replies': {'ok': True, 'messages': [
            {'user': 'U0SAM1234', 'text': 'Can you test?', 'ts': '1793869200.000100'}, {'user': 'UOWNER1', 'text': 'Tested, no issues', 'ts': '9.9'}]}}
        with patch.object(sender, 'call', side_effect=lambda action, method, params: seen.append((method, params)) or replies[method]):
            self.assertEqual(sender.reconcile(action, {'id': 'job', 'created_at': '2026-11-05T09:00:00+00:00'})['message_id'], f'slack:{CHANNEL}:9.9')
        self.assertEqual(seen[-1][1]['ts'], '1793869200.000100')

    def test_whatsapp_quotes_with_reply_to(self):
        sender = n.WhatsAppTransport({'accounts': [WHATSAPP]})
        action = {'kind': 'whatsapp', 'account_id': 'wa', 'chat_id': '120363000000000001@g.us', 'body': 'Yes, Friday works',
                  'quote': {'message_id': '3EB0AAAA0001', 'sender_id': '32470000001@s.whatsapp.net'}}
        done = subprocess.CompletedProcess([], 0, json.dumps({'success': True, 'data': {'sent': True, 'id': '3EB0BBBB0001'}}), '')
        with patch.object(sender, 'run', return_value=done) as run:
            self.assertEqual(sender.send(action, {'id': 'job'}), {'message_id': 'whatsapp:3EB0BBBB0001'})
        args = run.call_args[0][1]
        self.assertEqual(args[args.index('--reply-to') + 1], '3EB0AAAA0001')
        self.assertEqual(args[args.index('--reply-to-sender') + 1], '32470000001@s.whatsapp.net')
        with patch.object(sender, 'run', return_value=done) as run:
            sender.send({**action, 'quote': None}, {'id': 'job'})
        self.assertNotIn('--reply-to', run.call_args[0][1])


if __name__ == '__main__':
    unittest.main()
