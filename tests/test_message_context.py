"""A to-do's source message opens with what was said around it (machine/store/conversation.py, machine/app/conversation.py):
the messages before it in the same Slack DM, channel or thread, WhatsApp or Telegram chat or email thread (at most ten,
the same day's run for a chat, never fewer than three when there are any), the replies after it, and Show earlier for
older ones. Only the same connection and kind: a Work to-do never shows a Personal message, a Slack thread's replies stay
in their thread, and Show earlier pages only that conversation. An email thread with older mail the Machine never stored
reads the rest live, read-only, once. The dashboard test (test_message_context_dashboard.mjs) reads dump(). All names
and messages are made up."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location('message_context_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

DAY, EVE = '2026-11-04T', '2026-11-03T'
SLACK_DM = [  # (when, from the owner, text); the to-do's message is the one marked
    (EVE + '16:40', False, 'Did the beta build go out to the testers yet?'),
    (DAY + '12:52', False, 'Quick one about the bug reports from the phone app'),
    (DAY + '12:53', False, 'A tester says the report button does nothing on Android'),
    (DAY + '12:53', False, 'No to-do showed up for it on our side either'),
    (DAY + '12:59', True, 'Odd. Did they send a screenshot?'),
    (DAY + '13:05', False, 'Yes, it shows the form filled in and then nothing'),
    (DAY + '13:12', True, 'I’ll have an agent dig into it'),  # the to-do's message
    (DAY + '13:25', False, 'Great, thanks :pray:'),
    (DAY + '13:26', False, 'Let me know if you need the tester’s device details'),
]
ANCHOR = 6


def fixture(folder):
    """Three to-dos (a Slack DM, a WhatsApp group, an email thread) with their conversations stored around them, and
    noise that must never show: another Slack channel, another thread's replies, a Personal chat with the same id."""
    store = a.Store(Path(folder) / 'events.sqlite')

    def slack(i, at, me, text, channel='D0TESTER', thread=None):
        ts = f'17937{i:05d}.000100'
        return {'account_id': 'work-slack', 'source_id': f'{channel}:{ts}', 'kind': 'slack.message', 'occurred_at': at + ':00+00:00',
                'title': '#DM Kai Moreno: ' + text, 'body': text, 'deleted': False,
                'metadata': {'channel_name': 'DM Kai Moreno' if channel == 'D0TESTER' else 'mobile', 'conversation_type': 'dm' if channel == 'D0TESTER' else 'channel',
                             'channel_id': channel, 'from_me': me, 'sender_display': '' if me else 'Kai Moreno', 'message_ts': ts, 'thread_ts': thread or ts,
                             'source_url': f'https://acme.slack.example/archives/{channel}/p{i}'}}
    dm = [slack(i, at, me, text) for i, (at, me, text) in enumerate(SLACK_DM)]
    noise = [slack(50, DAY + '13:00', False, 'Standup moves to 10:00 tomorrow', channel='C0MOBILE'),
             # a reply in a thread under an earlier DM message: its own thread, not the DM's run
             slack(51, DAY + '13:10', False, 'Testers list attached in this thread', thread=dm[1]['metadata']['message_ts'])]
    store.commit_page('work-slack', {}, dm + noise, None)

    def whatsapp(i, at, who, text, account='home-wa', chat='1203@g.us'):
        return {'account_id': account, 'source_id': f'{account}-wa{i}', 'kind': 'whatsapp.message', 'occurred_at': DAY + at + ':00+00:00',
                'title': 'Garden club', 'body': text, 'deleted': False,
                'metadata': {'chat_name': 'Garden club', 'chat_id': chat, 'from_me': who == 'You', 'sender_display': who, 'from': who}}
    store.commit_page('home-wa', {}, [
        whatsapp(1, '07:58', 'Nell Ortiz', 'Who has the long ladder?'),
        whatsapp(2, '08:01', 'Bo Lindqvist', 'Mine is in the shed, happy to lend it'),
        whatsapp(3, '08:03', 'Nell Ortiz', 'Can someone bring it Saturday at 9?'),
        whatsapp(4, '08:20', 'You', 'I can pick it up Friday evening'),
        whatsapp(5, '08:22', 'Bo Lindqvist', 'Perfect, I’ll leave it by the gate')], None)
    store.commit_page('work-wa', {}, [whatsapp(9, '08:02', 'Someone at work', 'Work chat that shares the id', account='work-wa')], None)

    def mail(i, at, who, text, reply=True):
        return {'account_id': 'work', 'source_id': f'm{i}', 'kind': 'gmail.message', 'occurred_at': at + ':00+00:00',
                'title': 'Booth for the spring fair', 'body': text, 'deleted': False,
                'metadata': {'from': who, 'to': 'alex@lumen.example', 'thread_id': 'T1', 'in-reply-to': '<x@y>' if reply else ''}}
    store.commit_page('work', {}, [
        mail(1, EVE + '09:10', 'Avery Stone <avery@booths.example>', 'Hi Alex,\n\nHere is the quote for the fair booth: 2,400 for three days.\n\nBest,\nAvery', reply=False),
        mail(2, EVE + '15:30', 'Alex Kim <alex@lumen.example>', 'Thanks Avery. Does that include the lighting?'),
        mail(3, DAY + '08:45', 'Avery Stone <avery@booths.example>', 'Lighting is 300 extra. Shall I book it?'),
        mail(4, DAY + '10:02', 'Alex Kim <alex@lumen.example>', 'Let me check with the team today.')], None)
    with store.connect() as db:
        ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
    cards = {'slack': store.suggest('slack-card', 'Look into the missing bug report to-do', 'Kai asked.', [ids[dm[ANCHOR]['source_id']]])['id'],
             'whatsapp': store.suggest('wa-card', 'Pick up the ladder from Bo on Friday', 'Promised in the group.', [ids['home-wa-wa4']])['id'],
             'email': store.suggest('mail-card', 'Tell Avery if the booth lighting is a go', 'Avery asked.', [ids['m3']])['id']}
    app = object.__new__(a.App)
    app.store = store
    app.config = {'accounts': [{'id': 'work', 'service': 'gmail', 'email': 'alex@lumen.example'}], 'database': str(Path(folder) / 'events.sqlite')}
    store.accounts = app.config['accounts']
    return app, cards, ids


def dump(folder):
    """Each to-do's originals and the conversation around them, as the dashboard reads them (api/originals?id=)."""
    app, cards, _ = fixture(folder)
    out = {k: {'id': sid, 'originals': app.originals(sid), 'around': app.message_context_quiet(sid)} for k, sid in cards.items()}
    for v in out.values():  # Show earlier's answer, from the oldest message shown
        if v['around']['earlier']:
            v['earlier'] = {'from': v['around']['before'][0]['event_id'], 'around': app.message_context(v['id'], v['around']['before'][0]['event_id'])}
    return json.dumps(out)


def bodies(items):
    return [i['body'] for i in items]


class MessageContext(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.app, self.cards, self.ids = fixture(temp.name)

    def test_a_slack_dm_shows_the_same_days_run_before_it_and_the_replies_after(self):
        around = self.app.message_context(self.cards['slack'])
        self.assertEqual(bodies(around['before']), [t for _, _, t in SLACK_DM[1:ANCHOR]])  # not yesterday's, not the channel, not the thread reply
        self.assertEqual(bodies(around['after']), [t for _, _, t in SLACK_DM[ANCHOR + 1:]])
        self.assertTrue(around['earlier'])
        self.assertEqual({(i['chat'], i['dm']) for i in around['before']}, {('Kai Moreno', True)})
        self.assertEqual(around['before'][3]['from'], 'You')

    def test_show_earlier_pages_back_in_the_same_conversation(self):
        first = self.app.message_context(self.cards['slack'])['before'][0]['event_id']
        older = self.app.message_context(self.cards['slack'], first)
        self.assertEqual(bodies(older['before']), [SLACK_DM[0][2]])
        self.assertFalse(older['earlier'])

    def test_show_earlier_never_reads_another_conversation(self):
        for source in ('C0MOBILE:1793700050.000100', 'home-wa-wa1', 'm1'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                self.app.message_context(self.cards['slack'], self.ids[source])

    def test_a_slack_thread_reply_shows_its_thread(self):
        reply = self.ids['D0TESTER:1793700051.000100']
        sid = self.app.store.suggest('thread-card', 'Send the testers list', 'In a thread.', [reply])['id']
        around = self.app.message_context(sid)
        self.assertEqual(bodies(around['before']), [SLACK_DM[1][2]])  # its parent only
        self.assertEqual(around['after'], [])

    def test_a_chat_keeps_at_least_three_before_across_days(self):
        first_today = self.ids['D0TESTER:1793700001.000100']
        sid = self.app.store.suggest('early-card', 'About the bug reports', 'Kai asked.', [first_today])['id']
        self.assertEqual(bodies(self.app.message_context(sid)['before']), [SLACK_DM[0][2]])

    def test_whatsapp_shows_its_chat_and_never_another_accounts(self):
        around = self.app.message_context(self.cards['whatsapp'])
        self.assertEqual(bodies(around['before']), ['Who has the long ladder?', 'Mine is in the shed, happy to lend it', 'Can someone bring it Saturday at 9?'])
        self.assertEqual(bodies(around['after']), ['Perfect, I’ll leave it by the gate'])
        self.assertNotIn('Work chat that shares the id', json.dumps(around))
        self.assertFalse(around['earlier'])

    def test_an_email_thread_shows_its_earlier_mail_and_replies(self):
        around = self.app.message_context(self.cards['email'])
        self.assertEqual([i['from'] for i in around['before']], ['Avery Stone <avery@booths.example>', 'You'])
        self.assertEqual(bodies(around['after']), ['Let me check with the team today.'])
        self.assertFalse(around['earlier'])  # its oldest message starts the thread: nothing to read live

    def test_an_email_thread_older_than_the_import_reads_the_rest_live_once(self):
        with self.app.store.connect() as db:
            db.execute("UPDATE events SET deleted=1 WHERE source_id IN ('m1','m2')")
        around = self.app.message_context(self.cards['email'])
        self.assertEqual(around['before'], [])
        self.assertTrue(around['earlier'])  # m3 answers an earlier message
        raw = {'messages': [
            {'id': 'm0', 'threadId': 'T1', 'internalDate': '1793600000000', 'snippet': '',
             'payload': {'mimeType': 'text/plain', 'headers': [{'name': 'From', 'value': 'Avery Stone <avery@booths.example>'},
                                                               {'name': 'Subject', 'value': 'Booth for the spring fair'}],
                         'body': {'data': 'SGVsbG8gZnJvbSBiZWZvcmUgdGhlIGltcG9ydA'}}},
            {'id': 'm3', 'threadId': 'T1', 'internalDate': '1793782000000', 'payload': {'headers': []}}]}
        with mock.patch.object(a.Gmail, 'get', return_value=raw) as read:
            older = self.app.message_context(self.cards['email'], self.ids['m3'])
            self.app.message_context(self.cards['email'], self.ids['m3'])
        read.assert_called_once_with('threads/T1', {'format': 'full'})
        self.assertEqual([(o['body'], o['live'], o['event_id']) for o in older['before']], [('Hello from before the import', True, None)])

    def test_a_live_read_that_fails_shows_nothing_more(self):
        with self.app.store.connect() as db:
            db.execute("UPDATE events SET deleted=1 WHERE source_id IN ('m1','m2')")
        with mock.patch.object(a.Gmail, 'get', side_effect=a.SourceError('offline')):
            self.assertEqual(self.app.message_context(self.cards['email'], self.ids['m3'])['before'], [])

    def test_the_conversation_query_is_fixed_sql_with_the_key_bound(self):
        """The metadata key and the side never go into the SQL text: one fixed query per side, the JSON path bound."""
        from machine.store import conversation
        seen = []
        with self.app.store.connect() as db:
            anchor = self.app.store.context_anchor(db, self.cards['whatsapp'])
            real = db.execute

            class Spy:
                def execute(self, sql, params=()):
                    seen.append((sql, params))
                    return real(sql, params)
            for side in ('before', 'after'):
                self.app.store.conversation_ids(Spy(), anchor, side)
        self.assertEqual([s for s, _ in seen], [conversation._SIDE_SQL['before'], conversation._SIDE_SQL['after']])
        self.assertTrue(all(p[2] == '$.chat_id' for _, p in seen))
        self.assertNotIn('chat_id', ''.join(conversation._SIDE_SQL.values()))

    def test_a_chat_id_with_quotes_reads_only_its_chat(self):
        with self.app.store.connect() as db:
            db.execute("UPDATE events SET metadata=json_set(metadata,'$.chat_id',?) WHERE account_id='home-wa'", ("1203' OR '1'='1",))
        around = self.app.message_context(self.cards['whatsapp'])
        self.assertEqual(bodies(around['after']), ['Perfect, I’ll leave it by the gate'])
        self.assertEqual(len(around['before']), 3)

    def test_a_source_without_a_conversation_has_none(self):
        self.app.store.commit_page('work-stripe', {}, [{'account_id': 'work-stripe', 'source_id': 'ch1', 'kind': 'stripe.event', 'title': 'Payment',
                                                         'occurred_at': DAY + '09:00:00+00:00', 'body': 'Paid', 'deleted': False, 'metadata': {}}], None)
        with self.app.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id='ch1'").fetchone()[0]
        sid = self.app.store.suggest('stripe-card', 'Check the payment', 'Paid.', [event])['id']
        self.assertIsNone(self.app.message_context(sid))


if __name__ == '__main__':
    unittest.main()
