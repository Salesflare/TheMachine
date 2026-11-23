"""A to-do's source message opens with what was said around it (machine/store/conversation.py, machine/app/conversation.py):
the messages before it in the same Slack DM, channel or thread, WhatsApp or Telegram chat or email thread (at most ten,
the same day's run for a chat, never fewer than three when there are any), the replies after it, and Show earlier for
older ones. Only the same connection and kind: a Work to-do never shows a Personal message, a Slack thread's replies stay
in their thread, and Show earlier pages only that conversation. An email thread with older mail the Machine never stored
reads the rest live, read-only, once. A message opened by itself (the check on To-dos, search, the Graph) reads the same
way, all the new ones of its row with it. The dashboard tests (test_message_context_dashboard.mjs,
test_message_opened_dashboard.mjs) read dump() and dump_opened(). All names and messages are made up."""
import json
import sys
import tempfile
import unittest
import urllib.parse
from pathlib import Path
from unittest import mock
import machine.main as machine_main
import machine.sources.gmail as machine_sources_gmail
import sources
from machine.store.conversation import CONTEXT_KEYS
from machine.web.handler import make_handler

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

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
LISTS = [  # (when, from the owner, text): questions, numbered answers, then a numbered reply in a thread under the answers
    (DAY + '15:36', False, 'Four questions about the digest:\n1. Should it go in notifications?\n2. Tasks too?\n3. A limit per day?\n4. Shown on phones?'),
    (DAY + '15:37', False, 'No rush on these'),
    (DAY + '15:38', True, '1. yes, in notifications\n2. good question, tasks are in it too\n3. good idea\n4. could get busy, let’s think about it'),
    (DAY + '15:39', False, 'Unrelated: lunch at noon?'),
    (DAY + '15:40', True, 'Sure'),
    (DAY + '15:45', False, '1. then the settings screen needs a rework\n2. leave it for now\n3. I’ll log a release blocker\n4. a maximum could work, I’ll look into it'),
]


def fixture(folder):
    """Three to-dos (a Slack DM, a WhatsApp group, an email thread) with their conversations stored around them, and
    noise that must never show: another Slack channel, another thread's replies, a Personal chat with the same id."""
    store = machine_main.Store(Path(folder) / 'events.sqlite')

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
    lists = [slack(60 + i, at, me, text, channel='D0LISTS') for i, (at, me, text) in enumerate(LISTS)]
    for m in lists:
        m['metadata'].update(channel_name='DM Rui Costa', conversation_type='dm', sender_display='' if m['metadata']['from_me'] else 'Rui Costa')
        m['title'] = '#DM Rui Costa: ' + m['body']
    lists[-1]['metadata']['thread_ts'] = lists[2]['metadata']['message_ts']
    store.commit_page('work-slack', {}, lists, None)

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
             'email': store.suggest('mail-card', 'Tell Avery if the booth lighting is a go', 'Avery asked.', [ids['m3']])['id'],
             'thread': store.suggest('lists-card', 'Log the release blocker', 'Rui answered.', [ids[lists[-1]['source_id']]])['id']}
    app = object.__new__(machine_main.App)
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


def asked(app, query):
    """What api/originals answers the dashboard: (status, body)."""
    got = []

    class Request:
        def output(self, status, body):
            got.append((status, body))
    make_handler(app).get_api_originals(Request(), urllib.parse.urlsplit('/api/originals?' + query))
    return got[0]


def dump_opened(folder):
    """Messages opened from a list, as api/originals answers each question test_message_opened_dashboard.mjs asks."""
    app, _, ids = fixture(folder)
    wa = [ids[f'home-wa-wa{i}'] for i in range(1, 6)]
    dm = [ids[f'D0TESTER:17937{i:05d}.000100'] for i in range(len(SLACK_DM))]
    reply, mail = ids['D0TESTER:1793700051.000100'], [ids[f'm{i}'] for i in range(1, 5)]
    ask = {'wa': f'event={wa[2]}', 'two': f'events={wa[2]},{wa[4]}&near={wa[4]}', 'dm': f'event={dm[7]}', 'dm_earlier': f'event={dm[7]}&before={dm[1]}',
           'threads': f'events={reply},{dm[7]},{dm[8]}&near={dm[8]}', 'mail': f'event={mail[2]}', 'run': f'events={wa[3]},{wa[4]}&near={wa[4]}'}
    return json.dumps({k: {'query': q, **asked(app, q)[1]} for k, q in ask.items()})


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
        self.assertFalse(any(v.get('thread') for v in around['before'] + around['after']))  # a channel message: no thread line
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

    def test_a_slack_thread_reply_shows_its_thread_and_the_channel_before_it(self):
        reply = self.ids['D0TESTER:1793700051.000100']
        sid = self.app.store.suggest('thread-card', 'Send the testers list', 'In a thread.', [reply])['id']
        around = self.app.message_context(sid)
        # its thread's first message, and what was said before that one (at least three when there are any)
        self.assertEqual(bodies(around['before']), [SLACK_DM[0][2], SLACK_DM[1][2]])
        self.assertEqual(around['after'], [])
        self.assertFalse(around['earlier'])

    def test_a_thread_reply_reads_with_the_questions_it_answers(self):
        """The reported shape: questions in a DM, the owner's numbered answers, and the other person's numbered reply in
        a thread under those answers. The reply opens with the questions, the answers, then itself."""
        around = self.app.message_context(self.cards['thread'])
        self.assertEqual(bodies(around['before']), [t for _, _, t in LISTS[:3]])  # not the unrelated messages after the answers
        self.assertEqual(around['after'], [])
        self.assertFalse(around['earlier'])
        # the thread's own messages are marked, so the viewer shows where the thread begins
        self.assertEqual([bool(v.get('thread')) for v in around['before']], [False, False, True])

    def test_show_earlier_on_a_thread_reply_pages_the_channel_before_its_thread(self):
        reply = self.ids['D0TESTER:1793700051.000100']
        sid = self.app.store.suggest('thread-card', 'Send the testers list', 'In a thread.', [reply])['id']
        with self.app.store.connect() as db:
            db.execute("UPDATE events SET occurred_at=? WHERE source_id='D0TESTER:1793700000.000100'", (DAY + '12:50:00+00:00',))
        self.app.store.commit_page('work-slack', {}, [{'account_id': 'work-slack', 'source_id': f'D0TESTER:17936{i:05d}.000100', 'kind': 'slack.message',
                                                       'occurred_at': f'2026-11-0{i}T09:00:00+00:00', 'title': 'Old', 'body': f'Old {i}', 'deleted': False,
                                                       'metadata': {'channel_id': 'D0TESTER', 'message_ts': f'17936{i:05d}.000100', 'thread_ts': f'17936{i:05d}.000100'}}
                                                      for i in (1, 2, 3)], None)
        around = self.app.message_context(sid)
        self.assertEqual(bodies(around['before'])[-2:], [SLACK_DM[0][2], SLACK_DM[1][2]])
        self.assertEqual(len(around['before']), 4)  # at least three before the thread's first message
        self.assertTrue(around['earlier'])
        older = self.app.message_context(sid, around['before'][0]['event_id'])
        self.assertEqual(bodies(older['before']), ['Old 1'])
        self.assertFalse(older['earlier'])
        with self.assertRaises(ValueError):
            self.app.message_context(sid, self.ids['C0MOBILE:1793700050.000100'])

    def test_a_teams_chat_shows_what_was_said_before(self):
        def teams(i, at, text, chat='19:chat@thread.v2'):
            return {'account_id': 'work-teams', 'source_id': f'teams:{i}', 'kind': 'teams.message', 'occurred_at': DAY + at + ':00+00:00',
                    'title': 'Launch: ' + text, 'body': text, 'deleted': False,
                    'metadata': {'chat_id': chat, 'chat_kind': 'group', 'chat_name': 'Launch', 'message_id': str(i), 'from': 'Ana Ruiz', 'sender_display': 'Ana Ruiz'}}
        self.app.store.commit_page('work-teams', {}, [teams(1, '09:00', 'Which date works?'), teams(2, '09:05', 'Tuesday or Thursday'),
                                                      teams(3, '09:06', 'Other chat', chat='19:other@thread.v2'), teams(4, '09:10', 'Thursday then')], None)
        with self.app.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id='teams:4'").fetchone()[0]
        sid = self.app.store.suggest('teams-card', 'Book Thursday', 'Ana said.', [event])['id']
        self.assertEqual(bodies(self.app.message_context(sid)['before']), ['Which date works?', 'Tuesday or Thursday'])

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
        with mock.patch.object(machine_sources_gmail.Gmail, 'get', return_value=raw) as read:
            older = self.app.message_context(self.cards['email'], self.ids['m3'])
            self.app.message_context(self.cards['email'], self.ids['m3'])
        read.assert_called_once_with('threads/T1', {'format': 'full'})
        self.assertEqual([(o['body'], o['live'], o['event_id']) for o in older['before']], [('Hello from before the import', True, None)])

    def test_a_live_read_that_fails_shows_nothing_more(self):
        with self.app.store.connect() as db:
            db.execute("UPDATE events SET deleted=1 WHERE source_id IN ('m1','m2')")
        with mock.patch.object(machine_sources_gmail.Gmail, 'get', side_effect=sources.SourceError('offline')):
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


class MessageOpened(unittest.TestCase):
    """A message opened from a list (api/originals?event=, or events=…&near= for the new ones of one row)."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.app, _, self.ids = fixture(temp.name)

    def add(self, account, kind, key, rows, **more):
        """rows: (source id, minute of the day, text), in one conversation `key` of this kind."""
        self.app.store.commit_page(account, {}, [
            {'account_id': account, 'source_id': f'{account}:{name}', 'kind': kind, 'occurred_at': f'{DAY}{minute // 60:02d}:{minute % 60:02d}:00+00:00',
             'title': 'Trip', 'body': text, 'deleted': False, 'metadata': {CONTEXT_KEYS[kind]: key, 'from': 'Ana Ruiz', 'sender_display': 'Ana Ruiz', **more}}
            for name, minute, text in rows], None)
        with self.app.store.connect() as db:
            return [db.execute('SELECT id FROM events WHERE source_id=?', (f'{account}:{name}',)).fetchone()[0] for name, _, _ in rows]

    def opened(self, *ids):
        query = f'events={",".join(map(str, ids))}&near={ids[-1]}' if len(ids) > 1 else f'event={ids[0]}'
        status, found = asked(self.app, query)
        self.assertEqual(status, 200)
        return found

    def test_every_kind_reads_with_what_was_said_around_it_and_never_another_accounts(self):
        """Work and Personal connections whose conversations share an id: each reads only its own."""
        for kind in CONTEXT_KEYS:
            with self.subTest(kind=kind):
                said = [(f'{kind}{i}', 600 + i, f'{kind} {i}') for i in range(4)]
                mine = self.add('work-' + kind, kind, 'shared-id', said)
                self.add('home-' + kind, kind, 'shared-id', [(n, m, 'Personal ' + t) for n, m, t in said])
                found = self.opened(mine[1])
                self.assertEqual(bodies(found['originals']), [said[1][2]])
                self.assertEqual(found['around']['event_id'], mine[1])
                self.assertEqual(bodies(found['around']['before']), [said[0][2]])
                self.assertEqual(bodies(found['around']['after']), [said[2][2], said[3][2]])

    def test_a_rows_new_messages_open_together_with_what_came_before_the_first(self):
        """The reported shape: a chat with two new messages, the owner's own between them; both read, in their chat."""
        found = self.opened(self.ids['home-wa-wa3'], self.ids['home-wa-wa5'])
        self.assertEqual(bodies(found['originals']), ['Can someone bring it Saturday at 9?', 'Perfect, I’ll leave it by the gate'])
        self.assertEqual(bodies(found['around']['before']), ['Who has the long ladder?', 'Mine is in the shed, happy to lend it',
                                                            'Can someone bring it Saturday at 9?', 'I can pick it up Friday evening'])
        self.assertEqual(found['around']['after'], [])

    def test_new_messages_further_apart_than_the_window_are_all_there_in_order(self):
        rows = [(f'n{i:02d}', 600 + i, f'Message {i}') for i in range(40)]
        ids = self.add('home-tg', 'telegram.message', 'c1', rows)
        around = self.opened(*ids[5:])['around']
        self.assertEqual(bodies(around['before']), [t for _, _, t in rows[2:39]])  # three before the first new one, then all of them
        self.assertTrue(around['earlier'])
        status, older = asked(self.app, f'event={ids[-1]}&before={around["before"][0]["event_id"]}')
        self.assertEqual((status, bodies(older['around']['before']), older['around']['earlier']), (200, ['Message 0', 'Message 1'], False))
        around = self.opened(ids[30], ids[0])['around']  # later ones than the one read around
        self.assertEqual(bodies(around['after'])[-1], 'Message 30')

    def test_an_id_from_another_conversation_or_account_adds_nothing_around(self):
        wa, work, dm = self.ids['home-wa-wa2'], self.ids['work-wa-wa9'], self.ids['D0TESTER:1793700008.000100']
        around = self.opened(work, dm, wa)['around']
        self.assertNotIn('rest', around)
        self.assertEqual(bodies(around['before'] + around['after']), bodies(self.opened(wa)['around']['before'] + self.opened(wa)['around']['after']))

    def test_a_slack_row_with_a_thread_reply_reads_the_channel_and_the_thread(self):
        dm, reply = [self.ids[f'D0TESTER:17937{i:05d}.000100'] for i in range(9)], self.ids['D0TESTER:1793700051.000100']
        around = self.opened(reply, dm[7], dm[8])['around']
        self.assertEqual(around['event_id'], dm[8])
        self.assertIn('Great, thanks :pray:', bodies(around['before']))
        self.assertNotIn('Testers list attached in this thread', bodies(around['before']))
        thread, = around['rest']
        self.assertEqual((thread['event_id'], thread['ids'], thread['thread']), (reply, [reply], True))
        self.assertEqual(bodies(thread['before']), [SLACK_DM[1][2]])  # what the thread is under

    def test_a_slack_thread_reply_opened_alone_reads_its_thread_and_what_it_answers(self):
        around = self.opened(self.ids['D0LISTS:1793700065.000100'])['around']
        self.assertEqual(bodies(around['before']), [t for _, _, t in LISTS[:3]])
        self.assertEqual([bool(v.get('thread')) for v in around['before']], [False, False, True])

    def test_an_email_opens_with_its_thread(self):
        found = self.opened(self.ids['m3'])
        self.assertEqual([i['from'] for i in found['around']['before']], ['Avery Stone <avery@booths.example>', 'You'])
        self.assertEqual(bodies(found['around']['after']), ['Let me check with the team today.'])
        alone, = self.add('work', 'gmail.message', 'T9', [('single', 700, 'Just this one')])
        around = self.opened(alone)['around']
        self.assertEqual((around['before'], around['after'], around['earlier']), ([], [], False))  # nothing around it: it reads as it did

    def test_deleted_messages_stay_out_and_one_deleted_itself_opens_nothing_around(self):
        with self.app.store.connect() as db:
            db.execute("UPDATE events SET deleted=1 WHERE source_id IN ('home-wa-wa2','home-wa-wa5')")
        self.assertNotIn('Mine is in the shed, happy to lend it', json.dumps(self.opened(self.ids['home-wa-wa4']), ensure_ascii=False))
        self.assertIsNone(self.opened(self.ids['home-wa-wa5'])['around'])

    def test_a_kind_with_no_conversation_and_a_teammates_shared_message_open_as_before(self):
        self.app.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': kind, 'kind': kind, 'title': 'One', 'occurred_at': DAY + '09:00:00+00:00',
                                                 'body': 'Said', 'deleted': False, 'metadata': {'chat_id': 'x', 'thread_id': 'T1', 'channel_id': 'D0TESTER'}}
                                                for kind in ('fleet.message', 'android.notification', 'stripe.event')], None)
        with self.app.store.connect() as db:
            ids = [r[0] for r in db.execute("SELECT id FROM events WHERE kind IN ('fleet.message','android.notification','stripe.event')")]
        for event in ids:
            self.assertIsNone(self.opened(event)['around'])

    def test_show_earlier_only_pages_the_opened_conversation(self):
        for source in ('C0MOBILE:1793700050.000100', 'work-wa-wa9', 'm1'):
            status, body = asked(self.app, f'event={self.ids["home-wa-wa4"]}&before={self.ids[source]}')
            self.assertEqual((status, body), (404, {'error': 'Original not available'}))

    def test_reading_one_changes_nothing_stored(self):
        with self.app.store.connect() as db:
            before = list(db.iterdump())
        self.opened(self.ids['home-wa-wa3'], self.ids['home-wa-wa5'])
        with self.app.store.connect() as db:
            self.assertEqual(list(db.iterdump()), before)

    def test_several_without_one_to_read_around_open_as_they_are(self):
        """A person's sources (openSources): the messages themselves."""
        status, found = asked(self.app, f'events={self.ids["m1"]},{self.ids["home-wa-wa1"]}')
        self.assertEqual((status, set(found)), (200, {'originals'}))
        self.assertEqual(len(found['originals']), 2)


if __name__ == '__main__':
    unittest.main()
