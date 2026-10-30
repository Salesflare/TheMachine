"""The weekly recap is something to act on: what needs the owner first, the week ahead, what changed, then one-tap
choices that change only the owner's own filters and cards. No live calls: Telegram and pushes are stubbed."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo
import test_ux as ux
a = ux.a
dt = a.dt

FRIDAY = '2026-10-23T14:05:00+00:00'  # 16:05 in Brussels
WA = {'id': 'wa', 'service': 'whatsapp', 'display_name': 'Phone WhatsApp', 'boundary': 'personal:Owner'}
MAIL = {'id': 'work', 'service': 'gmail', 'email': 'owner@example.com', 'boundary': 'work:Example'}
CAL = {'id': 'cal', 'service': 'calendar', 'email': 'owner@example.com', 'boundary': 'work:Example'}


def ago(hours):
    return (dt.datetime.fromisoformat(FRIDAY) - dt.timedelta(hours=hours)).isoformat()


class WeeklyRecap(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        for p in (patch.object(a, 'LOCAL_TZ', ZoneInfo('Europe/Brussels')), patch.object(a, 'now', return_value=FRIDAY)):
            p.start()
            self.addCleanup(p.stop)
        self.path = Path(self.tmp.name) / 'config.json'
        self.config = {'accounts': [WA, MAIL, CAL], 'dashboard_host': 'm.example', 'dashboard_path': '/assistant/', 'telegram_owner': '1',
                       'weekly_recap': {'enabled': True}, 'database': str(Path(self.tmp.name) / 'events.sqlite')}
        self.path.write_text(json.dumps(self.config))
        self.store = a.Store(self.config['database'])
        self.app = object.__new__(a.App)
        self.app.store, self.app.config, self.app.config_path = self.store, json.loads(self.path.read_text()), self.path
        self.store.exclusions = {}
        # A busy WhatsApp group that never led to a card, and a person's own chat that is never a filter candidate.
        self.store.commit_page('wa', {}, [{'account_id': 'wa', 'source_id': f'g{i}', 'kind': 'whatsapp.message', 'occurred_at': ago(5), 'title': 'x', 'body': 'y',
                                           'metadata': {'chat_id': '123@g.us', 'chat_name': 'School parents', 'sender_id': f'3247{i % 15}@s.whatsapp.net'},
                                           'deleted': False} for i in range(30)]
                               + [{'account_id': 'wa', 'source_id': f'p{i}', 'kind': 'whatsapp.message', 'occurred_at': ago(5), 'title': 'x', 'body': 'y',
                                   'metadata': {'chat_id': '32470@s.whatsapp.net', 'chat_name': 'Ann'}, 'deleted': False} for i in range(30)])
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': ago(30), 'title': 'Contract',
                                             'body': 'I will send it.', 'metadata': {'from': 'sam@client.example'}, 'deleted': False}])
        with self.store.connect() as db:
            self.mail_event = db.execute("SELECT id FROM events WHERE source_id='m1'").fetchone()[0]

    def promise(self, direction, who, what, due=None, made=ago(30), check_at=None, card=None, status='open'):
        source = f'p{direction}{who}'
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': source, 'kind': 'gmail.message', 'occurred_at': made, 'title': 'Re',
                                             'body': 'Will do.', 'metadata': {'from': 'sam@client.example'}, 'deleted': False}])
        with self.store.connect() as db:
            event = db.execute('SELECT id FROM events WHERE source_id=?', (source,)).fetchone()[0]
            db.execute('INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,status,suggestion_id,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                       (direction, who, what, due, check_at or (due or '2026-10-30') + 'T07:30:00+00:00', event, 'work', status, card, made, made))

    def snoozed_card(self, title, times=2):
        sid = self.store.suggest('s-' + title, title, 'Body.', [self.mail_event])['id']
        for i in range(times):
            self.store.decide(sid, 'snooze', '', f'{sid}-snooze-{i}', 'telegram')
            if i < times - 1:
                self.store.decide(sid, 'accept', '', f'{sid}-back-{i}', 'telegram')  # Unsnooze, then snoozed again
        return sid

    def send(self):
        """The recap (message 555), then each choice as its own message (556, 557, ...), as sent to Telegram."""
        sent = []
        with patch.object(a, 'telegram_request', side_effect=lambda config, args: sent.append(args) or {'messageId': str(555 + len(sent) - 1)}):
            self.assertEqual(self.app.recap_step(current=dt.datetime.fromisoformat(FRIDAY)), 'sent')
        self.assertTrue(sent[0]['message'].startswith('**Your week with The Machine**'))
        self.assertEqual([m['action'] for m in sent], ['send'] * len(sent))
        return sent

    @staticmethod
    def labels(message):
        return [[b['label'] for b in r['buttons']] for r in message['presentation']['blocks'] if r['buttons']]

    def tap(self, item, choice, message_id=None, decision='telegram:1'):
        message_id = message_id or next(i['message_id'] for i in self.items() if i['id'] == item)
        with patch.object(a, 'telegram_request', side_effect=lambda config, args: self.edits.append(args) or {'messageId': args.get('messageId')}), \
                patch.object(a.threading, 'Thread', side_effect=lambda target, args, daemon: type('T', (), {'start': lambda s: target(*args)})()):
            return self.app.action('recap_decide', {'id': item, 'choice': choice, 'source': 'telegram', 'message_id': message_id, 'decision_id': decision})

    def items(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM recap_items ORDER BY n')]

    def test_what_needs_the_owner_comes_first_with_names_dates_and_promise_links(self):
        card = self.store.suggest('late', 'Chase Sam for the contract', 'Body.', [self.mail_event])['id']
        self.promise('theirs', 'Sam Lee', 'send the signed contract', due='2026-10-20', card=card, status='carded')
        self.promise('theirs', 'Kim', 'review the deck', made=ago(24 * 9), check_at=ago(24))  # undated, past its check: late too
        self.promise('mine', 'Alex', 'send the Q3 deck', due='2026-10-26')
        self.promise('theirs', 'Bo', 'call back', due='2026-10-27')  # not late: in the week ahead instead
        self.promise('theirs', 'Alex', 'send the Q3 deck', due='2026-10-26')  # the same plan from both sides shows once, as the owner's
        self.promise('theirs', 'Dee', 'sign the form', due='2026-10-23')  # due today: still on time, in neither
        self.promise('theirs', 'Eli', 'pay the invoice', due='2026-10-31')  # Saturday after next: past the week ahead
        text = a.weekly_recap(self.store, self.config, dt.datetime.fromisoformat(FRIDAY))
        lines = text.split('\n')
        self.assertEqual(lines[0], '**Your week with The Machine** · Oct 16–23')
        self.assertEqual(lines[2], '**Needs you**')
        with self.store.connect() as db:  # a promise links to its own page, never to its card (the page links the card)
            page = {(r[0], r[1]): f'https://m.example/assistant/#promise/{r[2]}' for r in db.execute('SELECT who,direction,id FROM promises')}
        self.assertEqual(lines[3], f"• Waiting on Sam Lee: [send the signed contract]({page['Sam Lee', 'theirs']}), due Tue, Oct 20")
        self.assertNotIn('#chat=' + card, text)
        self.assertEqual(lines[4], f"• Waiting on Kim: [review the deck]({page['Kim', 'theirs']}), since Wed, Oct 14")
        self.assertEqual(lines[5], f"• Promised Alex: [send the Q3 deck]({page['Alex', 'mine']}), due Mon, Oct 26")
        self.assertIn(f"**Next week**\n• Tue, Oct 27: Bo said they'd [call back]({page['Bo', 'theirs']})", text)
        self.assertNotIn('Dee', text)
        self.assertNotIn('Eli', text)
        self.assertEqual(text.count('send the Q3 deck'), 1)
        self.assertFalse([l for l in lines if l.lstrip('•0123456789. ').startswith('You ')])  # event lines never open with "You"

    def test_week_ahead_has_meetings_with_people_and_their_prep(self):
        def meeting(source_id, title, at, **meta):
            return {'account_id': 'cal', 'source_id': source_id, 'kind': 'calendar.event', 'occurred_at': at, 'title': title, 'body': '', 'deleted': False,
                    'metadata': {'attendees': [{'email': 'owner@example.com', 'self': True, 'responseStatus': meta.pop('me', 'accepted')}, {'email': 'pat@acme.example'}], **meta}}
        self.store.commit_page('cal', {}, [meeting('b', 'Board meeting', '2026-10-28T08:00:00+00:00'),
                                           meeting('w', 'Weekly one-on-one', '2026-10-27T08:00:00+00:00', recurring_event_id='r1'),
                                           meeting('d', 'Declined lunch', '2026-10-27T11:00:00+00:00', me='declined'),
                                           meeting('n', 'Next month', '2026-11-20T08:00:00+00:00'),
                                           meeting('t', 'Team offsite', '2026-10-29T08:00:00+00:00', ical_uid='u1')])
        # A partner's calendar shared with the owner: there 'self' is the partner. Their own appointments aren't the owner's;
        # one the owner is invited to is, and shows once next to the owner's own copy.
        shared = lambda source_id, title, at, guests, **meta: {'account_id': 'cal', 'source_id': source_id, 'kind': 'calendar.event', 'occurred_at': at,
            'title': title, 'body': '', 'deleted': False, 'metadata': {'access': 'shared_read_only', 'credential_account': 'owner@example.com',
            'attendees': [{'email': 'partner@example.com', 'self': True, 'responseStatus': 'accepted'}, *guests], **meta}}
        self.store.commit_page('cal', {}, [shared('s1', 'Dentist with Robin', '2026-10-27T13:00:00+00:00', [{'email': 'dentist@example.com'}]),
                                           shared('s2', 'Team offsite', '2026-10-29T08:00:00+00:00', [{'email': 'owner@example.com', 'responseStatus': 'accepted'}, {'email': 'pat@acme.example'}], ical_uid='u1'),
                                           shared('s3', 'Parents evening', '2026-10-30T16:00:00+00:00', [{'email': 'owner@example.com', 'responseStatus': 'needsAction'}, {'email': 'school@example.com'}])])
        with self.store.connect() as db:
            board = db.execute("SELECT id FROM events WHERE source_id='b'").fetchone()[0]
        prep = self.store.suggest('prep', 'Prep notes for the board', 'Body.', [board])['id']
        text = a.weekly_recap(self.store, self.config, dt.datetime.fromisoformat(FRIDAY))
        self.assertIn(f'**Next week**\n• Wed, Oct 28 09:00 Board meeting, 1 person · [to-do](https://m.example/assistant/#chat={prep})', text)
        self.assertEqual(text.count('Team offsite'), 1)
        self.assertIn('• Fri, Oct 30 17:00 Parents evening, 2 people', text)  # the partner and the school, not the owner
        for routine in ('Weekly one-on-one', 'Declined lunch', 'Next month', 'Dentist with Robin'):
            self.assertNotIn(routine, text)

    def test_new_people_by_name_only(self):
        with self.store.connect() as db:
            for node, name, org in (('email:lena@aliru.example', 'Lena Zwick', 'org:aliru.example'), ('email:support@codehubsupport.example', 'CodeHub', 'org:codehubsupport.example'),
                                    ('email:dana@bounce.example', 'dana@bounce.example', 'org:bounce.example'), ('email:zeb@clickup.example', 'Zeb', 'org:clickup.example')):
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,gap_days,quiet,trend,info) VALUES(?,'person',?,1,?,2,NULL,0,0,?)",
                           (node, name, ago(2), json.dumps({'org': org})))
            db.execute("INSERT OR REPLACE INTO graph_state(id,built_at,signals,took_ms) VALUES(1,?,10,1)", (FRIDAY,))
        text = a.weekly_recap(self.store, self.config, dt.datetime.fromisoformat(FRIDAY))
        line = next(l for l in text.split('\n') if l.startswith('• New people'))
        self.assertEqual(line, '• New people: Lena Zwick, Zeb, and 1 more known only by address')  # no address, no company desk as a person

    def test_worth_it_and_what_changed_in_plain_lines(self):
        for i, (choice, then) in enumerate((('accept', None), ('accept', 'other'), ('reject', None))):
            sid = self.store.suggest(f'q{i}', f'Card {i}', 'Body.', [self.mail_event])['id']
            self.store.decide(sid, choice, '', f'q{i}a', 'telegram')
            if then:
                self.store.decide(sid, then, 'Shorter please', f'q{i}b', 'telegram')
        with self.store.connect() as db:
            db.execute("INSERT INTO rule_changes(at,kind,text) VALUES(?,'draft_rule','Draft rule: keep it short')", (ago(3),))
        text = a.weekly_recap(self.store, self.config, dt.datetime.fromisoformat(FRIDAY) + dt.timedelta(minutes=1))
        self.assertIn('**What changed**\n• 67% of to-dos worth it (2 of 3). Do it was right first time in 1 of 2.\n• Adjusted: 1 writing rule.\n', text)
        self.assertNotIn('got it right the first time', text)
        recap = a.weekly_recap_message(self.store, self.config, dt.datetime.fromisoformat(FRIDAY) + dt.timedelta(minutes=1))['text']
        self.assertEqual(recap.split('\n')[-1], '_Behind the scenes: 0 signals reviewed this week, 61 still waiting._')  # one short line, at the end
        self.assertEqual(text.count('Behind the scenes'), 1)

    def test_no_brief_ever_shows_a_cost(self):
        # The recap may go to anyone with a Machine: what it reviewed, never an API price estimate, on Telegram or the push.
        self.snoozed_card('Pay the painter', 3)
        self.assertNotRegex(a.weekly_recap(self.store, self.config, dt.datetime.fromisoformat(FRIDAY)), r'[$€]|list price|subscription')
        self.assertFalse(hasattr(a, 'assistant_token_usage'))
        sent = self.send()
        self.assertFalse([m for m in sent if '$' in m['message'] or 'price' in m['message']])

    def test_filter_and_keep_are_one_tap_and_only_change_the_owners_filters(self):
        self.edits = []
        recap, choice = self.send()
        self.assertTrue(recap['message'].endswith('\n\n_Choices follow below. Nothing changes until you tap._'))
        self.assertEqual(self.labels(recap), [])  # the recap itself has no buttons
        self.assertNotIn('School parents', recap['message'])
        # The choice is its own message: what it is about, and buttons that say what they do, without a number.
        self.assertEqual(choice['message'], '**Busy without results**\nSchool parents (Phone WhatsApp): 30 this week, no to-dos')
        self.assertNotIn('Ann', choice['message'])  # a person's own chat is never offered as noise
        rows = choice['presentation']['blocks']
        item = self.items()[0]
        self.assertEqual(item['message_id'], '556')
        self.assertEqual(self.labels(choice), [['Stop reviewing', 'Keep reviewing']])
        self.assertEqual(rows[0]['buttons'][0]['action'], {'type': 'callback', 'value': f"assistant:recap:{item['id']}:filter"})
        self.assertLessEqual(len(('tgcb1:xxxxx:' + rows[0]['buttons'][0]['action']['value']).encode()), 64)  # Telegram's callback limit
        with self.assertRaisesRegex(ValueError, 'not the recap'):
            self.tap(item['id'], 'filter', message_id='555')  # the recap itself, not the choice's own message
        self.assertEqual(json.loads(self.path.read_text())['accounts'][0].get('exclude'), None)  # refused: nothing changed

        self.assertEqual(self.tap(item['id'], 'filter')['status'], 'filtered')
        self.assertEqual(json.loads(self.path.read_text())['accounts'][0]['exclude'], [{'chats': ['123@g.us']}])
        self.assertEqual(self.store.exclusions['wa'], [{'chats': ['123@g.us']}])  # new messages from it are skipped from now on
        edit = self.edits.pop()
        self.assertEqual((edit['action'], edit['messageId']), ('edit', '556'))  # the choice's own message shows it; nothing new is sent
        self.assertEqual(edit['message'], '**Busy without results**\nSchool parents (Phone WhatsApp): 30 this week, no to-dos · **No longer reviewed**')
        self.assertEqual(self.labels(edit), [['Undo']])
        self.assertEqual(self.tap(item['id'], 'keep', decision='telegram:2').get('reason'), 'Already done: no longer reviewed.')
        self.assertEqual(self.tap(item['id'], 'filter', decision='telegram:1').get('duplicate'), True)  # a replayed tap

        self.assertEqual(self.tap(item['id'], 'undo', decision='telegram:3')['status'], 'open')
        self.assertEqual(json.loads(self.path.read_text())['accounts'][0]['exclude'], [])
        self.assertEqual(self.tap(item['id'], 'keep', decision='telegram:4')['status'], 'kept')
        with self.store.connect() as db:
            self.assertEqual([r[0] for r in db.execute("SELECT text FROM rule_changes WHERE kind='filter' ORDER BY id")],
                             ['Filter: School parents (Phone WhatsApp)', 'Removed filter: School parents (Phone WhatsApp)'])
            db.execute('DELETE FROM recaps')
        self.assertNotIn('School parents', a.weekly_recap(self.store, self.config, dt.datetime.fromisoformat(FRIDAY)))  # kept: not asked again

    def test_group_chats_of_friends_and_family_are_never_offered_as_noise(self):
        def chat(chat_id, name, n, senders, mine=0):
            return [{'account_id': 'wa', 'source_id': f'{chat_id}-{i}', 'kind': 'whatsapp.message', 'occurred_at': ago(5), 'title': 'x', 'body': 'y',
                     'metadata': {'chat_id': chat_id, 'chat_name': name, **({'from_me': True} if i < mine else {'sender_id': f'{chat_id}-s{i % senders}'})},
                     'deleted': False} for i in range(n)]
        self.store.commit_page('wa', {}, chat('9@g.us', 'Weekend crew', 40, 12, mine=3)  # the owner writes in it: their own chat
                               + chat('8@g.us', 'Cousins', 40, 5)  # a handful of people: a circle, even when the owner only reads
                               + chat('7@g.us', 'Street announcements', 25, 20))  # many people, the owner never writes: a feed
        text = a.weekly_recap(self.store, self.config, dt.datetime.fromisoformat(FRIDAY))
        busy = [m.split('\n')[1] for m in text.split('\n\n') if m.startswith('**Busy without results**')]
        self.assertEqual(busy, ['School parents (Phone WhatsApp): 30 this week, no to-dos', 'Street announcements (Phone WhatsApp): 25 this week, no to-dos'])

    def test_cards_snoozed_again_and_again_drop_do_it_now_or_keep(self):
        self.edits = []
        drop, now, keep = (self.snoozed_card(t, n) for t, n in (('Share the tow-bar cost', 4), ('Pay the painter', 3), ('Book the dentist', 2)))
        sent = self.send()
        self.assertEqual(sent[2]['message'], f'**Snoozed more than once**\n[Share the tow-bar cost](https://m.example/assistant/#chat={drop}), 4 times')
        items = {i['ref']: i for i in self.items() if i['kind'] == 'snoozed'}
        self.assertEqual(self.labels(sent[2]), [['Drop', 'Do it now', 'Keep']])
        self.assertEqual([items[x]['message_id'] for x in (drop, now, keep)], ['557', '558', '559'])
        with self.store.connect() as db:
            status = lambda sid: db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0]
            self.assertEqual([status(x) for x in (drop, now, keep)], ['snoozed'] * 3)  # nothing changed by sending it
        self.assertEqual(self.tap(items[drop]['id'], 'drop')['status'], 'dropped')
        self.assertEqual(self.tap(items[now]['id'], 'now', decision='telegram:2')['status'], 'started')
        self.assertEqual(self.tap(items[keep]['id'], 'keep', decision='telegram:3')['status'], 'kept')
        with self.store.connect() as db:
            status = lambda sid: db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0]
            self.assertEqual([status(x) for x in (drop, now, keep)], ['rejected', 'accepted', 'snoozed'])
            self.assertEqual(db.execute('SELECT count(*) FROM action_jobs').fetchone()[0], 0)  # Do it prepares; nothing is sent
        self.assertEqual([(e['messageId'], e['message'].split(' · ')[-1], self.labels(e)) for e in self.edits],
                         [('557', '**Dropped**', []), ('558', '**Started**', []), ('559', '**Kept**', [])])  # each edit on its own message
        with self.assertRaisesRegex(ValueError, 'not the recap'):
            self.tap(items[now]['id'], 'keep', message_id='557', decision='telegram:5')  # another choice's message
        with self.store.connect() as db:
            db.execute('DELETE FROM recaps')
        self.assertNotIn('Book the dentist', a.weekly_recap(self.store, self.config, dt.datetime.fromisoformat(FRIDAY)))  # kept until snoozed again

    def test_taps_come_only_from_telegram_on_that_message(self):
        self.edits = []
        self.send()
        item = self.items()[0]
        with self.assertRaisesRegex(ValueError, 'come from the recap message'):
            self.app.action('recap_decide', {'id': item['id'], 'choice': 'filter', 'source': 'assistant'})
        with self.assertRaisesRegex(ValueError, 'Unknown choice'):
            self.tap(item['id'], 'drop')
        self.assertIn('recap_decide', a.OWNER_ACTIONS)  # the plugin's owner key, never the API token alone

    def test_without_telegram_the_push_leads_with_what_needs_the_owner(self):
        self.promise('mine', 'Alex', 'send the Q3 deck', due='2026-10-26')
        self.app.config['telegram_owner'] = ''
        pushed = []
        with self.store.connect() as db:
            db.execute("INSERT INTO push_subscriptions(endpoint,p256dh,auth,created_at) VALUES('https://push.example/1','k','a',?)", (FRIDAY,))
        with patch.object(a, 'push_node', side_effect=lambda config, request: pushed.append(request) or {'results': []}), \
                patch.object(a, 'telegram_request', side_effect=AssertionError('no Telegram')):
            self.assertEqual(self.app.recap_step(current=dt.datetime.fromisoformat(FRIDAY)), 'sent')
        self.assertTrue(pushed[0]['payload']['body'].startswith('Needs you • Promised Alex: send the Q3 deck, due Mon, Oct 26'), pushed[0]['payload']['body'])
        self.assertEqual(self.items(), [])  # no buttons to tap without Telegram
        self.assertNotIn('Choices follow', pushed[0]['payload']['body'])

    def test_a_choice_that_did_not_go_out_is_forgotten(self):
        self.snoozed_card('Pay the painter', 3)
        sent = []
        def deliver(config, args):
            sent.append(args)
            if len(sent) == 2:
                raise a.DeliveryNotSent('delivery_not_admitted')
            return {'messageId': str(554 + len(sent))}
        with patch.object(a, 'telegram_request', side_effect=deliver):
            self.assertEqual(self.app.recap_step(current=dt.datetime.fromisoformat(FRIDAY)), 'sent')
        self.assertEqual([(i['kind'], i['message_id']) for i in self.items()], [('snoozed', '557')])  # the busy source comes up next week

    def test_a_recap_sent_before_keeps_its_numbered_buttons(self):
        # Sent by an older version: the choices are lines in the recap, their buttons under it. A tap still works there.
        self.edits = []
        with self.store.connect() as db:
            db.execute("INSERT INTO recaps(week,status,created_at,text,message_id) VALUES('2026-W43','sent',?,?,'444')",
                       (FRIDAY, '**Busy without results**\n1. School parents (Phone WhatsApp): 30 this week, no to-dos\nNothing changes until you tap.'))
            db.execute("INSERT INTO recap_items(id,week,n,kind,ref,line,data,status) VALUES('r_0123456789ab','2026-W43',1,'noise','wa',?,?,'open')",
                       ('1. School parents (Phone WhatsApp): 30 this week, no to-dos', json.dumps({'account': 'wa', 'rule': {'chats': ['123@g.us']}, 'label': 'School parents'})))
        self.assertEqual(self.tap('r_0123456789ab', 'filter', message_id='444')['status'], 'filtered')
        edit = self.edits.pop()
        self.assertEqual(edit['messageId'], '444')
        self.assertIn('1. School parents (Phone WhatsApp): 30 this week, no to-dos · **Filtered**', edit['message'])
        self.assertEqual(self.labels(edit), [['Undo 1']])

    def test_layout_dump(self):
        """The brief as Telegram gets it, message by message with its button rows (printed with RECAP_DUMP=1)."""
        import os
        self.promise('mine', 'Alex', 'send the Q3 deck', due='2026-10-26')
        for title, n in (('Order leaf-basket supplies', 3), ('Pay the painter', 2)):
            self.snoozed_card(title, n)
        sent = self.send()
        dump = '\n\n'.join(f"--- message {i + 1} ---\n{m['message']}" + ''.join(f"\n  [ {' | '.join(r)} ]" for r in self.labels(m)) for i, m in enumerate(sent))
        if os.environ.get('RECAP_DUMP'):
            print('\n' + dump)
        self.assertEqual(len(sent), 4)
        self.assertNotRegex(dump, r'\[ (Filter|Keep|Drop|Undo) \d')  # no numbered buttons


if __name__ == '__main__':
    unittest.main()
