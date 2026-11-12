"""The last check of new messages, on To-dos (check_now.mail_check, dashboard/todos-mail-check.js mailCheckBlock): an owner saw
"new emails picked up" and no to-dos and thought it was broken, while the review had read every new email and judged,
per thread, that nothing needed them (only cc'd, a meeting already set, already answered). The review now says why per
thread (finish_analysis no_todo) and To-dos shows it. The line covered only email while the review also reads chats,
phone notifications and the rest: it now counts and lists every source the check read. A fake review drives the real
begin_analysis, suggest and finish_analysis; no model and nothing is sent. Every name and address is made up."""
import datetime as dt
import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from seams import patch_everywhere

import check_now

spec = importlib.util.spec_from_file_location('mail_check_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
NOW = dt.datetime(2026, 11, 9, 15, 11, tzinfo=dt.timezone.utc)
OWNER = 'owner@lumen.example'
counter = iter(range(1, 10**6))


def mail(sender, title, thread, kind='gmail.message', minutes_ago=30, to=OWNER):
    n = next(counter)
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': kind, 'occurred_at': (NOW - dt.timedelta(minutes=minutes_ago)).isoformat(),
            'title': title, 'body': 'Body text.', 'deleted': False,
            'metadata': {'from': sender, 'to': to, 'labels': ['INBOX'], 'message-id': f'<{n}@x.example>', 'thread_id': thread}}


def other(account, kind, title, body, meta, minutes_ago=30):
    """A message that isn't email: a chat, a phone notification, a calendar change, a log line of The Machine's own."""
    n = next(counter)
    return {'account_id': account, 'source_id': f'o{n}', 'kind': kind, 'occurred_at': (NOW - dt.timedelta(minutes=minutes_ago)).isoformat(),
            'title': title, 'body': body, 'deleted': False, 'metadata': meta}


class MailCheck(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.clock = NOW
        clock = patch_everywhere(a, 'now', lambda: self.clock.isoformat())
        clock.start(); self.addCleanup(clock.stop)

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])
        with self.store.connect() as db:
            return [db.execute('SELECT id FROM events WHERE source_id=?', (e['source_id'],)).fetchone()[0] for e in events]

    def view(self, at=NOW, times=False):
        """The view, each row's time (its newest message) left out unless `times`: every row has one."""
        with self.store.connect() as db:
            got = check_now.mail_check(db, at, own=[OWNER])
        for row in (got or {}).get('threads', []):
            self.assertTrue(row['at'])
            if not times:
                del row['at']
        return got

    def test_a_check_says_what_it_read_its_new_to_do_held_until_later_and_why_each_other_thread_needed_nothing(self):
        cc, meeting, vague, pricing, reply, chat = self.add(
            mail('Robin Vale <robin@acme.example>', 'Re: Trial seats', 'cc', to='kim@acme.example'),
            mail('"Yara Oak" <yara@salt.example>', 'Re: Coffee next week', 'meet'),
            mail('Bulk Sender <news@digest.example>', 'This week in tools', 'news'),
            mail('Mila Under <mila@north.example>', 'Pricing for our team', 'pricing', minutes_ago=40),
            mail(f'Owner <{OWNER}>', 'Re: Pricing for our team', 'pricing', minutes_ago=35),
            mail('Sam Ridge <U123>', 'standup', 'c1', kind='slack.message'))
        same = self.add(*[mail(f'P{i} <p{i}@x.example>', f'Note {i}', f'same{i}') for i in range(3)])
        claim = self.store.begin_analysis(['work'], 120)
        held = self.store.suggest('work:pricing', 'Send Mila annual pricing', 'They asked for **25 seats**.', [pricing], when='digest')
        self.assertGreater(held['deliver_after'], NOW.isoformat())  # it waits for the morning summary
        self.store.finish_analysis(claim['analysis_id'], 'Saved one to-do.', no_todo=[
            {'event_id': cc, 'why': 'Only cc’d, Robin is answering'}, {'event_id': meeting, 'why': 'Coffee   already set for Thu 10:00'},
            {'event_id': vague, 'why': 'No action.'}, *[{'event_id': i, 'why': 'Nothing needed here.'} for i in same]])
        got = self.view()
        self.assertEqual({k: got[k] for k in ('at', 'read', 'counts', 'todos', 'held', 'more')},
                         {'at': NOW.isoformat(), 'read': 8, 'counts': {'email': 7, 'chat': 1}, 'todos': 1, 'held': 1, 'more': 0})  # the owner's reply is nothing new
        self.assertEqual(got['held_until'], held['deliver_after'])
        rows = {r['subject']: r for r in got['threads']}
        self.assertEqual(got['threads'][0]['todo'], 'Send Mila annual pricing')  # the thread with a to-do comes first
        self.assertEqual(rows['Re: Pricing for our team'], {'from': 'Mila Under', 'subject': 'Re: Pricing for our team', 'todo': 'Send Mila annual pricing',
                                                            'held_until': held['deliver_after'], 'source': 'email', 'kind': 'gmail.message',
                                                            'event': pricing, 'account': 'work'})  # who wrote to the owner, and their message opens, not the owner's reply
        self.assertEqual(rows['Re: Trial seats']['why'], 'Only cc’d, Robin is answering')
        self.assertEqual(rows['Re: Coffee next week'], {'from': 'Yara Oak', 'subject': 'Re: Coffee next week', 'why': 'Coffee already set for Thu 10:00',
                                                        'source': 'email', 'kind': 'gmail.message', 'event': meeting, 'account': 'work'})
        # Quality or nothing: a two-word label and one reason given for three threads are left out, the thread still listed
        self.assertNotIn('why', rows['This week in tools'])
        self.assertTrue(all('why' not in rows[f'Note {i}'] for i in range(3)))
        self.assertEqual(len(got['threads']), 8)
        self.assertEqual(rows['Body text.'], {'from': 'Sam Ridge', 'subject': 'Body text.', 'source': 'chat', 'kind': 'slack.message', 'event': chat, 'account': 'work'})
        self.assertIsNone(self.view(NOW + dt.timedelta(hours=check_now.MAIL_CHECK_HOURS, minutes=1)))  # an old check says nothing

    def test_a_sender_known_only_by_address_shows_by_the_graphs_name_and_an_unknown_one_by_address(self):
        known, unknown, named = self.add(mail('avery@booths.example', 'Booth plan', 'b1'), mail('nobody@unknown.example', 'Hello', 'b2'),
                                         mail('Sam Rivera <sam@client.example>', 'Checking in', 'b3'))
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('email:avery@booths.example','person','Avery Stone',1,1,?)",
                       (json.dumps({'identifiers': ['email:avery@booths.example'], 'emails': ['avery@booths.example']}),))
        claim = self.store.begin_analysis(['work'], 120)
        self.store.finish_analysis(claim['analysis_id'], 'Nothing new.', no_todo=[])
        self.assertEqual({r['event']: r['from'] for r in self.view()['threads']},
                         {known: 'Avery Stone', unknown: 'nobody@unknown.example', named: 'Sam Rivera'})

    def test_a_reason_never_refuses_a_review_and_a_check_with_nothing_new_shows_the_last_one_that_had_something(self):
        first, = self.add(mail('Mila Under <mila@north.example>', 'Question', 't1'))
        claim = self.store.begin_analysis(['work'], 120)
        done = self.store.finish_analysis(claim['analysis_id'], 'Nothing new', no_todo=[{'event_id': first}, {'why': 'x'}, 'bad', {'event_id': 'x', 'why': 'y'}])
        self.assertEqual(done['status'], 'complete')
        self.assertEqual(self.view()['threads'], [{'from': 'Mila Under', 'subject': 'Question', 'source': 'email', 'kind': 'gmail.message', 'event': first, 'account': 'work'}])
        self.clock = NOW + dt.timedelta(minutes=20)
        self.add(other('work', 'machine.system_log', 'Disk 80% full', 'Disk 80% full', {}),
                 other('work', 'slack.message', '#general: Owner', 'On my way', {'channel_id': 'C1', 'from_me': True}))
        claim = self.store.begin_analysis(['work'], 120)
        self.store.finish_analysis(claim['analysis_id'], 'Nothing new', no_todo='bad')
        # a check that read only The Machine's own log and the owner's own chat message read nothing new: the one before shows
        self.assertEqual(self.view(self.clock)['at'], NOW.isoformat())

    def test_every_source_the_check_read_is_counted_and_listed_with_its_reason_and_the_message_to_open(self):
        wa1, wa2, slack, phone, cal, own_chat, log, letter = self.add(
            other('home', 'whatsapp.message', 'Book club', 'Did anyone   finish chapter 4?', {'chat_id': 'g1', 'chat_name': 'Book club', 'sender_display': 'Noor Pell'}, 40),
            other('home', 'whatsapp.message', 'Book club', 'Bringing snacks on Friday', {'chat_id': 'g1', 'chat_name': 'Book club', 'sender_display': 'Ivo Lark'}, 20),
            other('work', 'slack.message', '#deals: Rae Fenn', 'Can you approve the Delta discount today?', {'channel_id': 'C9', 'channel_name': 'deals', 'sender_display': 'Rae Fenn'}),
            other('phone', 'android.notification', 'Parcel', 'Delivered to your door', {'app_name': 'Parcels', 'package_name': 'com.parcels.example'}),
            other('work', 'calendar.event', 'Planning review', '', {'from': 'Ola Brisk <ola@lumen.example>'}),
            other('home', 'whatsapp.message', 'Book club', 'Sounds good', {'chat_id': 'g1', 'chat_name': 'Book club', 'from_me': True}, 10),
            other('work', 'machine.system_log', 'Restarted', 'Restarted', {}),
            mail('Mila Under <mila@north.example>', 'Contract draft', 'contract'))
        claim = self.store.begin_analysis(['work', 'home', 'phone'], 120)
        self.store.suggest('work:delta', 'Approve the Delta discount', 'Rae asks for it today.', [slack], when='now')
        self.store.finish_analysis(claim['analysis_id'], 'Saved one to-do.', no_todo=[
            {'event_id': wa2, 'why': 'Group chat chatter, nothing asked of you'}, {'event_id': phone, 'why': 'A delivery notice, the parcel is in'},
            {'event_id': cal, 'why': 'Your own meeting, nothing changed for you'}])
        got = self.view()
        # the owner's own chat message and The Machine's own log aren't new; a chat's two messages are one row
        self.assertEqual((got['read'], got['counts'], got['todos']), (6, {'chat': 3, 'notification': 1, 'update': 1, 'email': 1}, 1))
        self.assertEqual(got['threads'][0], {'from': 'Rae Fenn', 'subject': 'Can you approve the Delta discount today?', 'source': 'chat',
                                             'kind': 'slack.message', 'event': slack, 'account': 'work', 'todo': 'Approve the Delta discount'})
        rows = {r['kind']: r for r in got['threads'][1:]}
        self.assertEqual(rows['whatsapp.message'], {'from': 'Ivo Lark', 'subject': 'Bringing snacks on Friday', 'source': 'chat', 'kind': 'whatsapp.message',
                                                    'event': wa2, 'account': 'home', 'why': 'Group chat chatter, nothing asked of you', 'n': 2})  # the newest message, not the owner's
        self.assertEqual(rows['android.notification'], {'from': 'Parcels', 'subject': 'Parcel: Delivered to your door', 'source': 'notification',
                                                        'kind': 'android.notification', 'event': phone, 'account': 'phone', 'app': 'com.parcels.example', 'why': 'A delivery notice, the parcel is in'})
        self.assertEqual(rows['calendar.event'], {'from': 'Ola Brisk', 'subject': 'Planning review', 'source': 'update', 'kind': 'calendar.event',
                                                  'event': cal, 'account': 'work', 'why': 'Your own meeting, nothing changed for you'})
        self.assertEqual(rows['gmail.message'], {'from': 'Mila Under', 'subject': 'Contract draft', 'source': 'email', 'kind': 'gmail.message', 'event': letter, 'account': 'work'})
        self.assertNotIn(own_chat, [r['event'] for r in got['threads']])
        self.assertNotIn(log, [r['event'] for r in got['threads']])
        self.assertEqual(len(got['threads']), 5)
        self.assertNotIn(wa1, [r['event'] for r in got['threads']])

    def test_rows_read_like_an_inbox_apps_by_name_slack_by_name_never_an_id_and_a_phone_echo_once(self):
        """An owner's list showed phone apps by package ("com.linkedin.android"), a Slack DM as "DM U0…" with "<@U0…>" and
        "<https://…>" in its words, a LinkedIn notification right above the LinkedIn message it was about, and a total
        its rows didn't add up to. Now: apps by name, Slack members by name (or a "Slack DM" with no id), plain words,
        the echo once, and each row's count of new messages."""
        phone = lambda package, title, body, minutes=30: other('phone', 'android.notification', title, body,
                                                                {'package_name': package, 'app_name': package}, minutes)
        with self.store.connect() as db:
            db.execute("INSERT INTO identity_names(identifier,name,email,checked_at) VALUES('slack:U0FENNRAE12','Rae Fenn',NULL,?)", (NOW.isoformat(),))
        dm = {'channel_id': 'D1', 'channel_name': 'DM U0ABCDE1234', 'conversation_type': 'im', 'user_id': 'U0ABCDE1234'}
        ids = self.add(
            phone('com.linkedin.android', '1 new message: Ola Brisk', '1 new message: Ola Brisk - Hi there, we last spoke at the fair in May about a p'),
            other('work', 'linkedin.message', 'Ola Brisk', 'Hi there, we last spoke at the fair in May about a pilot for your team.',
                  {'conversation_id': 'li1', 'sender_display': 'Ola Brisk'}, 31),
            phone('com.linkedin.android', 'Ivo Lark viewed your profile', 'Ivo Lark viewed your profile', 20),
            phone('com.kbc.mobile.android.phone.kbc', 'Payment received', 'Payment received: 12,00 EUR', 21),
            phone('computer.themachine.app', 'Done: Post the launch note', 'Done: Post the launch note', 22),
            phone('com.acme.mobile.android', 'Your order shipped', 'Your order shipped', 23),
            phone('com.whatsapp', 'Noor Pell', 'Noor Pell: the train is late', 24),
            other('work', 'slack.message', '#DM U0ABCDE1234: Ping', 'Ping <@U0ABCDE1234> about <https://docs.example/a/b> and <https://plan.example/x|the plan>, *today*', dm, 25),
            other('work', 'slack.message', '#DM U0ABCDE1234: ok', 'ok   thx', dm, 15),
            other('work', 'slack.message', '#support: x', 'Can you look at <#C77|billing> &amp; ping <@U0FENNRAE12>?',
                  {'channel_id': 'C9', 'channel_name': 'support', 'user_id': 'U0FENNRAE12'}, 26))
        claim = self.store.begin_analysis(['work', 'phone'], 120)
        self.store.finish_analysis(claim['analysis_id'], 'Nothing new')
        got = self.view(times=True)
        rows = got['threads']
        # a phone notification's app is kept by its package only to pick its mark (the dashboard's MONO_APPS), never shown
        self.assertEqual(rows[1]['app'], 'com.linkedin.android')
        shown = json.dumps([{k: v for k, v in r.items() if k != 'app'} for r in rows])
        self.assertNotRegex(shown, r'U0[A-Z0-9]{8}')  # never a Slack member id
        self.assertNotIn('com.', shown)  # never a package name
        self.assertNotIn('<', shown)  # no Slack markup
        by_app = {r['from']: r['subject'] for r in rows if r['source'] == 'notification'}
        self.assertEqual(by_app, {'LinkedIn': 'Ivo Lark viewed your profile', 'KBC Mobile': 'Payment received: 12,00 EUR',
                                  'The Machine': 'Done: Post the launch note', 'Acme': 'Your order shipped', 'WhatsApp': 'Noor Pell: the train is late'})
        # LinkedIn's notification about Ola's message is that message: one row, counted once
        self.assertEqual([r['from'] for r in rows if r['kind'] == 'linkedin.message'], ['Ola Brisk'])
        self.assertNotIn(ids[0], [r['event'] for r in rows])
        self.assertEqual(got['read'], 9)
        self.assertEqual(sum(r.get('n', 1) for r in rows), got['read'])  # the rows add up to the line's total
        dm_row, = [r for r in rows if r['kind'] == 'slack.message' and r.get('dm')]
        self.assertEqual({k: dm_row[k] for k in ('from', 'subject', 'n', 'event')}, {'from': '', 'subject': 'ok thx', 'n': 2, 'event': ids[8]})
        channel, = [r for r in rows if r['kind'] == 'slack.message' and not r.get('dm')]
        self.assertEqual((channel['from'], channel['subject']), ('Rae Fenn', 'Can you look at #billing & ping @Rae Fenn?'))
        self.assertTrue(all(r['at'] for r in rows))

    def test_a_payment_a_group_mail_and_a_support_chat_read_like_the_viewer(self):
        """A payment saved with only its customer's address shows by their organization's name when no person's name is
        known, a Google Group's mail by the person and the group as the viewer says it, and a support chat by its plain
        words, never a part's raw time and type."""
        paid, group, chat, mail_only = self.add(
            other('work', 'stripe.event', 'Invoice paid: €49.00', 'Invoice paid', {'from': 'ops@orbit.example', 'customer_name': 'ops@orbit.example'}, 20),
            mail("\"'Lena Fair' via sales@lumen.example readers\" <sales@lumen.example>", 'Partner listing question', 'g1'),
            other('work', 'intercom.conversation', 'Export stops again',
                  'Export stops again\n1762000100 · Fin · comment: Which plan are you on?\n1762000200 · kai@kestrel.example · comment: Growth.',
                  {'conversation_id': 'c9', 'from': 'kai@kestrel.example', 'contact_email': 'kai@kestrel.example', 'created_at': 1762000000}, 22),
            mail('ops@orbit.example', 'Receipt', 'r1'))
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('email:ops@orbit.example','person','ops@orbit.example',1,1,?)",
                       (json.dumps({'org': 'org:orbit.example'}),))
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('org:orbit.example','org','Orbit',1,1,'{}')")
        claim = self.store.begin_analysis(['work'], 120)
        self.store.finish_analysis(claim['analysis_id'], 'Nothing new.', no_todo=[])
        rows = {r['event']: r for r in self.view()['threads']}
        self.assertEqual(rows[paid]['from'], 'Orbit')
        self.assertEqual(rows[mail_only]['from'], 'ops@orbit.example')  # an email keeps its From
        self.assertEqual(rows[group]['from'], 'Lena Fair via sales')
        self.assertEqual(rows[chat]['subject'], 'Export stops again · Which plan are you on? · Growth.')

    def test_a_support_chat_shows_its_people_by_name_and_a_phone_notification_never_its_package_id(self):
        """An owner's list showed Intercom conversations by address (a customer's, and the Operator bot's
        operator+…@intercom.io) while Intercom gave their names, and a phone's group summary notification by its package
        id as the subject ("com.acme.shop"). Now: the name the source gives, the customer of a bot-opened conversation,
        the bot by name when there is no customer, and a notification with no words of its own shows only its app."""
        convo = lambda cid, meta, minutes: other('work', 'intercom.conversation', 'Exports stop at 1,000 rows', 'Exports stop at 1,000 rows',
                                                 {'conversation_id': cid, **meta}, minutes)
        phone = lambda package, app, title, body, minutes: other('phone', 'android.notification', title, body,
                                                                 {'package_name': package, 'app_name': app}, minutes)
        bot = 'operator+abc123@intercom.io'
        ids = self.add(
            convo('c1', {'from': 'rae@delta.example', 'from_name': 'Rae Fenn', 'contact_email': 'rae@delta.example', 'contact_name': 'Rae Fenn'}, 20),
            convo('c2', {'from': bot, 'from_name': 'Fin', 'contact_email': 'ola@north.example', 'contact_name': 'Ola Brisk'}, 21),
            convo('c3', {'from': bot, 'from_name': 'Fin', 'contact_email': '', 'contact_name': ''}, 22),
            convo('c4', {'from': 'lead@mossgate.example', 'from_name': 'lead@mossgate.example', 'contact_email': 'lead@mossgate.example',
                         'contact_name': 'lead@mossgate.example'}, 23),
            phone('com.acmeshop.app', 'com.acmeshop.app', 'com.acmeshop.app', '', 24),
            phone('com.google.android.apps.wellbeing', 'Digital Wellbeing', 'com.google.android.apps.wellbeing', '', 25),
            phone('com.acmeshop.app', 'com.acmeshop.app', 'Small gifts for every budget', 'Small gifts for every budget', 26))
        claim = self.store.begin_analysis(['work', 'phone'], 120)
        self.store.finish_analysis(claim['analysis_id'], 'Nothing new')
        rows = {r['event']: r for r in self.view()['threads']}
        self.assertEqual([rows[i]['from'] for i in ids[:4]], ['Rae Fenn', 'Ola Brisk', 'Fin', 'lead@mossgate.example'])
        self.assertEqual([(rows[i]['from'], rows[i]['subject']) for i in ids[4:]],
                         [('Acmeshop', ''), ('Digital Wellbeing', ''), ('Acmeshop', 'Small gifts for every budget')])
        shown = json.dumps([{k: v for k, v in r.items() if k != 'app'} for r in rows.values()])
        self.assertNotIn('intercom.io', shown)
        self.assertNotRegex(shown, r'\bcom\.\w+\.')  # never a package id
        # stored anew, such a notification's title is its app by name, never the package
        from machine.sources.android import android_event
        made = android_event({'id': 'phone'}, {'key': 'k1', 'packageName': 'com.acmeshop.app', 'postTimeMs': 1762700000000})
        self.assertEqual(made['title'], 'Acmeshop')
        events, _ = self.store.android_feed_batch({'id': 'phone'}, [{'id': 'r1', 'received_at': NOW.isoformat(), 'payload': json.dumps(
            {'id': 'n1', 'notification_key_hash': 'h1', 'package_name': 'com.acmeshop.app', 'at_ms': 1762700000000, 'change': 'posted', 'text': ''})}],
            read_existing=False, settle=False)
        self.assertEqual([e['title'] for e in events], ['Acmeshop'])

    def test_slack_markup_reads_as_plain_words_and_an_app_without_a_known_label_gets_a_name(self):
        from machine.sources.android import android_app_shown
        from machine.sources.slack import slack_plain
        self.assertEqual(slack_plain('Ping <@U0ABCDE1234> about <https://docs.example/a/b> and <https://plan.example/x|the plan>, *today*'),
                         'Ping @someone on Slack about docs.example/… and the plan, today')
        self.assertEqual(slack_plain('<!here> see <#C1|deals>, <mailto:sam@x.example|Sam> or <https://www.x.example> &lt;3 _soon_ ~no~'),
                         '@here see #deals, Sam or x.example <3 soon no')
        self.assertEqual(slack_plain('2*3*4 and snake_case_name stay'), '2*3*4 and snake_case_name stay')
        self.assertEqual([android_app_shown(p) for p in ('com.linkedin.android', 'com.android.vending', 'computer.themachine.app',
                                                         'com.kbc.mobile.android.phone.kbc', 'com.acme.mobile.android', 'nl.abn.ab', 'com.google.android.apps.fit', '')],
                         ['LinkedIn', 'Google Play', 'The Machine', 'KBC Mobile', 'Acme', 'ABN', 'Google Fit', 'Unknown app'])
        self.assertEqual(android_app_shown('com.acme.app', 'Acme Shop'), 'Acme Shop')  # a label the phone gave wins
        # the same name on a to-do's source line
        from machine.store.cards import source_text
        line = source_text({'kind': 'android.notification', 'occurred_at': NOW.isoformat(),
                            'metadata': {'package_name': 'com.linkedin.android', 'app_name': 'com.linkedin.android'}})
        self.assertIn(' from LinkedIn · ', line)

    def test_on_a_sealed_database_the_words_stay_sealed_at_rest_and_the_app_reads_them(self):
        # message_protection on: a chat's words and the review's reason are blobs in the file, and the view opens them
        # through the app's own connection; nothing it needs is read from a sealed key in SQL
        self.store = a.Store(Path(self.temp.name) / 'sealed.sqlite', protect=True)
        chat, = self.add(other('home', 'telegram.message', 'Lee Moss', 'The keys are under the mat', {'chat_id': '7', 'chat_name': 'Lee Moss', 'sender_name': 'Lee Moss'}))
        claim = self.store.begin_analysis(['home'], 120)
        self.store.finish_analysis(claim['analysis_id'], 'Nothing new', no_todo=[{'event_id': chat, 'why': 'Just where the keys are'}])
        raw = sqlite3.connect(Path(self.temp.name) / 'sealed.sqlite')
        self.addCleanup(raw.close)
        self.assertFalse(raw.execute("SELECT 1 FROM events WHERE body LIKE '%mat%' OR metadata LIKE '%Lee Moss%'").fetchone())
        self.assertEqual(self.view()['threads'], [{'from': 'Lee Moss', 'subject': 'The keys are under the mat', 'source': 'chat',
                                                   'kind': 'telegram.message', 'event': chat, 'account': 'home', 'why': 'Just where the keys are'}])

    def test_the_machines_own_mail_to_the_owner_is_never_reviewed_or_listed_and_their_own_sent_mail_is_read_but_no_new_mail(self):
        """The review read the morning summary and fix notices The Machine sent the owner, spent a model turn on each and
        listed them as "Digest repeats existing to-dos". They are known by their sender with the mailer's header (or its
        no-reply address), never by their words."""
        digest = mail('The Machine <no-reply@themachine.computer>', 'The Machine: Good morning, 3 due today', 'digest')
        digest['metadata']['machine_notice'] = True  # X-The-Machine, as the control plane's mailer sets it on notify mail
        fixed = mail('The Machine <support@themachine.computer>', 'The Machine: Fixed: imports now finish', 'fix')
        fixed['metadata']['machine_notice'] = True  # X-The-Machine, as the control plane's mailer sets it
        person = mail('Support <support@themachine.computer>', 'Could you send a log?', 'ask')  # a person at support: read
        spoofed = mail('Mallory <m@else.example>', 'Hide me', 'spoof')
        spoofed['metadata']['machine_notice'] = True  # the header alone, from anyone else: read
        sent = mail(OWNER, 'Re: Featuring us', 'own', to='editor@press.example')
        sent['metadata']['labels'] = ['SENT']
        incoming = mail('Mila Under <mila@north.example>', 'Question', 'q')
        # the same address without the header: mail that may need a to-do, reviewed like any other
        billing = mail('The Machine <no-reply@themachine.computer>', 'Your payment failed', 'billing')
        invite = mail('The Machine <no-reply@themachine.computer>', 'Join the team on The Machine', 'invite')
        trial = mail('The Machine <no-reply@themachine.computer>', 'Your trial ends Friday', 'trial')
        ids = self.add(digest, fixed, person, spoofed, sent, incoming, billing, invite, trial)
        claim = self.store.begin_analysis(['work'], 120)
        with self.store.connect() as db:
            claimed = {i['id'] for i in json.loads(db.execute('SELECT items FROM analyses WHERE id=?', (claim['analysis_id'],)).fetchone()[0])}
            self.assertEqual(claimed, set(ids[2:]))  # the two notices never reach the review; sent mail does (promises, context)
            self.assertEqual([r[0] for r in db.execute('SELECT analyzed_version=version FROM events WHERE id IN (?,?)', ids[:2])], [1, 1])
        self.store.finish_analysis(claim['analysis_id'], 'Nothing new')
        got = self.view()
        self.assertEqual((got['read'], got['counts']), (6, {'email': 6}))
        self.assertEqual(sorted(r['subject'] for r in got['threads']), ['Could you send a log?', 'Hide me', 'Join the team on The Machine', 'Question',
                                                                         'Your payment failed', 'Your trial ends Friday'])

    def test_the_mailers_header_is_kept_and_only_counts_from_the_machines_domain(self):
        from machine.sources import gmail
        self.assertEqual(gmail.list_headers({'x-the-machine': 'notice'}), {'machine_notice': True})
        notice = lambda sender, **more: gmail.machine_notice('gmail.message', {'from': sender, 'labels': ['INBOX'], **more})
        self.assertTrue(notice('The Machine <no-reply@themachine.computer>', machine_notice=True))
        self.assertTrue(notice('support@themachine.computer', machine_notice=True))
        self.assertTrue(notice('no-reply@mail.themachine.computer', machine_notice=True))
        self.assertFalse(notice('The Machine <no-reply@themachine.computer>'))  # billing, a trial, an invite: reviewed
        self.assertFalse(notice('support@themachine.computer'))
        self.assertFalse(notice('no-reply@themachine.computer.evil.example', machine_notice=True))
        self.assertFalse(notice('no-reply@notthemachine.computer'))
        self.assertFalse(notice('no-reply@themachine.computer', labels=['SENT'], machine_notice=True))
        self.assertFalse(gmail.machine_notice('slack.message', {'from': 'no-reply@themachine.computer', 'machine_notice': True}))

    def test_the_review_is_asked_for_a_reason_per_thread_and_the_dashboard_shows_the_line(self):
        prompt = a.review_prompt('run', ['work'])
        self.assertIn('no_todo ([{"event_id", "why"}])', prompt)
        self.assertIn('never an id', prompt)
        import dashboard_parts
        page = dashboard_parts.assemble(Path(__file__).parent.parent)
        self.assertIn('${mailCheckSlot()}', page)
        self.assertIn('todos-mail-check.js', dashboard_parts.LAZY['mailcheck'])
        self.assertIn('state?.mail_check', page)


if __name__ == '__main__':
    unittest.main()
