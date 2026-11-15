"""Notes from conversations (topic_notes.py, NotesApp.topic_notes_run): every mail thread and chat, from every mailbox
and chat service, read from what was said and sorted by one call per ASK_MAX into a part of Home, Health or Kids, a note
of its own, a record in the Graph, or nowhere. Bulk is left out in plain code first. Made-up data only; the model is a
stand-in, nothing is sent."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import machine.main as machine_main

import note_pages  # noqa: E402
import note_pages_app  # noqa: E402
import section_notes  # noqa: E402
import topic_notes  # noqa: E402
from machine import kinds as event_kinds  # noqa: E402
from pinned import pinned  # noqa: E402

HOME = {'id': 'home', 'email': 'sam@example.com', 'boundary': 'personal'}
JOB = {'id': 'job', 'email': 'sam@acme.example', 'boundary': 'work:Acme'}
CHAT = {'id': 'chat', 'service': 'whatsapp', 'boundary': 'personal'}
TEAM = {'id': 'team', 'service': 'slack', 'user_id': 'U0SAM00001', 'boundary': 'work:Acme'}
AT = '2026-11-14T10:00:00+00:00'


class Conversations(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [HOME, JOB, CHAT, TEAM]}
        self.asked, self.routes, self.n = [], {}, 0
        self.app.topic_notes_model = self.model
        self.app.section_notes_model = lambda prompt: json.dumps({'places': []})
        pin = pinned(AT)
        pin.__enter__()
        self.addCleanup(pin.__exit__, None, None, None)

    def model(self, prompt):
        """Answers by title: self.routes maps a title's words to {'place': a path} | {'record': a name} | {'new': ...}."""
        self.asked.append(prompt)
        places = {}
        for line in prompt.split('The places that exist, one JSON object per line:\n', 1)[1].split('\nThe conversations', 1)[0].splitlines():
            p = json.loads(line)
            places[p['path']] = p['id']
        out = []
        for line in prompt.split('<<<\n', 1)[1].split('\n>>>', 1)[0].splitlines():
            item = json.loads(line)
            route = next((r for k, r in self.routes.items() if k in item['title']), None)
            if not route:
                continue
            if 'place' in route:
                out.append({'n': item['n'], 'place': places.get(route['place'], 'P999')})
            elif 'record' in route:
                rec = next((r['id'] for r in item.get('records', []) if r['name'] == route['record']), None)
                out.append({'n': item['n'], 'record': rec})
            else:
                out.append({'n': item['n'], **route})
        return json.dumps({'places': out})

    def event(self, kind, title, day, account='home', body='', **meta):
        self.n += 1
        when = day if 'T' in day else f'{day}T08:00:00+00:00'
        with self.store.connect() as db:
            return db.execute('INSERT INTO events(account_id,source_id,kind,title,body,occurred_at,metadata,content_hash,ingested_at) '
                              'VALUES(?,?,?,?,?,?,?,?,?)', (account, f'e{self.n}', kind, title, body, when, json.dumps(meta), f'h{self.n}', AT)).lastrowid

    def mail(self, sender, subject, day, account='home', body='', **meta):
        return self.event('gmail.message', subject, day, account, body, **{'from': sender, **meta})

    def round(self):
        with self.store.connect() as db:
            db.execute('DELETE FROM topic_state')
        self.app.topic_notes_run()
        with self.store.connect() as db:
            return {(x['kind'], x['name']): note_pages.page(db, x['id']) for x in note_pages.listing(db, '2026-11-14') if x['kind'] != 'note'}

    def routed(self):
        with self.store.connect() as db:
            return {r['title']: r['place'] for r in db.execute('SELECT title,place FROM topic_routes')}


class SortedByWhatWasSaid(Conversations):
    def test_a_conversation_from_any_mailbox_or_chat_goes_in_the_part_it_is_about(self):
        self.routes = {'Trip to the zoo': {'place': 'Kids > School'}, 'Lunch boxes': {'place': 'Kids > School'},
                       'Swimming': {'place': 'Kids > Activities'}, 'Coach Robin': {'place': 'Kids > Activities'}}
        self.mail('Example Primary <office@example-primary.be>', 'Trip to the zoo on 21 November', '2026-11-03', thread_id='t1',
                  body='Dear parents,\nThe class goes to the zoo on Friday 21 November. Bring a packed lunch.\n\nKind regards,\nMs. Lee\nExample Primary\n+32 000 00 00')
        self.mail('Sam <sam@acme.example>', 'Re: Trip to the zoo on 21 November', '2026-11-04', account='job', thread_id='t1', labels=['SENT'],
                  body='Thanks, she will be there.\n\nOn Mon, 3 Nov 2026, Ms. Lee <office@example-primary.be> wrote:\n> The class goes to the zoo')
        self.mail('Example Primary <office@example-primary.be>', 'Lunch boxes', '2026-11-05', account='job', thread_id='t2', body='Please label the lunch boxes.')
        self.event('whatsapp.message', 'Coach Robin', '2026-11-06T18:00:00+00:00', 'chat', 'Swimming moves to 17:00 on Wednesday', chat_id='3200@s.whatsapp.net',
                   chat_name='Coach Robin', sender_display='Coach Robin')
        self.event('whatsapp.message', 'Coach Robin', '2026-11-06T18:05:00+00:00', 'chat', 'Great, thanks', chat_id='3200@s.whatsapp.net',
                   chat_name='Coach Robin', from_me=True)
        notes = self.round()
        school = notes[('kids', 'School')]
        self.assertEqual([x['name'] for x in school['path']], ['Kids'])
        self.assertCountEqual([x['text'] for x in school['lines']], ['Trip to the zoo on 21 November', 'Lunch boxes'],
                              'one line per conversation, the work mailbox too')
        self.assertEqual([x['item'] for x in school['lines']], ['conversation', 'conversation'])
        self.assertNotIn(('kids', 'Activities'), notes, 'one conversation: not a part yet (MIN_LINES)')
        prompt = self.asked[0]
        self.assertIn('Bring a packed lunch.', prompt, 'the call reads what was said')
        self.assertIn('Owner: Thanks, she will be there.', prompt)
        for cut in ('Kind regards', '+32 000', '> The class goes'):
            self.assertNotIn(cut, prompt, 'quoted history and the signature are left out')
        self.assertIn('"source": "WhatsApp"', prompt)
        self.assertIn('Swimming moves to 17:00', prompt)

    def test_a_new_note_starts_with_two_conversations_or_one_ongoing_matter(self):
        self.routes = {'Office move': {'new': {'title': 'Office move', 'under': 'Work'}},
                       'Hiring a designer': {'new': {'title': 'Hiring a designer', 'under': 'Work'}, 'ongoing': True},
                       'Pool': {'new': {'title': 'Pool', 'under': 'Home'}, 'ongoing': True},
                       'Kitchen': {'new': {'title': 'Kitchen renovation', 'under': 'Home'}}}
        self.mail('Example Movers <desk@example-movers.be>', 'Office move: a quote', '2026-10-01', account='job', thread_id='a')
        self.mail('Example Landlord <desk@example-landlord.be>', 'Kitchen tiles', '2026-10-02', thread_id='k')
        self.mail('Example Agency <ana@example-agency.be>', 'Hiring a designer: three profiles', '2026-10-03', account='job', thread_id='h')
        self.mail('Sam <sam@acme.example>', 'Re: Hiring a designer: three profiles', '2026-10-04', account='job', thread_id='h', labels=['SENT'])
        self.mail('Example Pools <desk@example-pools.be>', 'Pool: your quote', '2026-10-03', thread_id='p')
        notes = self.round()
        self.assertIn(('topic', 'Hiring a designer'), notes, 'one ongoing matter the owner wrote in is enough')
        self.assertNotIn(('topic', 'Pool'), notes, "the call's word alone starts no note")
        self.assertNotIn(('topic', 'Kitchen renovation'), notes)
        self.assertNotIn(('topic', 'Office move'), notes, 'one conversation: not yet a note')
        self.mail('Example Movers <desk@example-movers.be>', 'Office move: the date', '2026-10-09', account='job', thread_id='b')
        notes = self.round()
        self.assertIn('Work > Office move', self.asked[1], 'the next call sees the topic proposed before')
        move = notes[('topic', 'Office move')]
        self.assertEqual([x['name'] for x in move['path']], ['Work'])
        self.assertEqual(move['area'], 'work:Acme')
        self.assertEqual([x['text'] for x in move['lines']], ['Office move: the date', 'Office move: a quote'], 'newest first')

    def test_a_matter_the_graph_has_goes_to_that_record_not_a_second_note(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('project:p1','project','Example Rollout',1,3,'{}')")
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('org:example.org','org','Example Org',1,3,'{}')")
        first = self.mail('Ana <ana@example.org>', 'Rollout plan', '2026-10-01', account='job', thread_id='r')
        self.mail('Ana <ana@example.org>', 'Rollout week two', '2026-10-08', account='job', thread_id='s')
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_events(node_id,event_id,at,direct) VALUES('project:p1',?,?,1)", (first, AT))
        self.routes = {'Rollout plan': {'record': 'Example Rollout'}, 'Rollout week two': {'new': {'title': 'example org', 'under': 'Work'}, 'ongoing': True}}
        notes = self.round()
        self.assertIn('"name": "Example Rollout", "kind": "project"', self.asked[0])
        self.assertEqual(self.routed(), {'Rollout plan': 'record:project:p1', 'Rollout week two': 'record:org:example.org'})
        self.assertFalse([k for k in notes if k[0] == 'topic'])

    def test_each_conversation_is_asked_about_once_and_its_later_messages_follow_it(self):
        self.routes = {'Boiler': {'place': 'Home > Repairs and upkeep'}, 'Gutter': {'place': 'Home > Repairs and upkeep'}}
        self.mail('Example Plumber <office@example-plumber.be>', 'Boiler service', '2026-10-20', thread_id='b')
        self.mail('Example Roofer <office@example-roofer.be>', 'Gutter repair', '2026-10-21', thread_id='g')
        self.round()
        self.assertEqual(len(self.asked), 1)
        later = self.mail('Example Plumber <office@example-plumber.be>', 'Re: Boiler service', '2026-11-02', thread_id='b')
        notes = self.round()
        self.assertEqual(len(self.asked), 1, 'nothing new: no call')
        line = next(x for x in notes[('home', 'Repairs and upkeep')]['lines'] if x['text'] == 'Boiler service')
        self.assertEqual((line['at'], line['event_id']), ('2026-11-02', later))

    def test_a_reply_that_isnt_one_keeps_nothing(self):
        self.app.topic_notes_model = lambda prompt: 'not now'
        self.mail('Example Primary <office@example-primary.be>', 'Weekly letter', '2026-10-06')
        self.assertEqual(self.app.topic_notes_run(), 0)
        self.assertEqual(self.routed(), {})

    def test_mail_placed_by_sender_before_goes(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO section_topics(kind,key,section,note,at) VALUES('kids','mail:x','School','',?)", (AT,))
            section_notes.ensure(db)
            self.assertIsNone(db.execute("SELECT 1 FROM section_topics WHERE key LIKE 'mail:%'").fetchone())


class LeftOutFirst(Conversations):
    """Bulk never reaches a call or a note: spam always; promotions, list mail, mail a program sent and system senders
    unless the owner wrote in the thread or it carries a booking; bots, broadcasts and lone chat messages."""

    def test_bulk_mail_and_bulk_chat_are_left_out_before_any_call(self):
        self.mail('Example Clinic <desk@example-clinic.be>', 'Your referral letter', '2026-10-08')
        self.mail('Example Clinic <desk@example-clinic.be>', 'Clinic newsletter', '2026-10-09', list_unsubscribe=True)
        self.mail('Example Clinic <desk@example-clinic.be>', 'Autumn offer', '2026-10-10', labels=['CATEGORY_PROMOTIONS', 'INBOX'])
        self.mail('Example Clinic <desk@example-clinic.be>', 'Member update', '2026-10-11', list_id='<members.example-clinic.be>')
        self.mail('Example Clinic <desk@example-clinic.be>', 'Weekly digest', '2026-10-12', precedence='bulk')
        self.mail('Example Clinic <no-reply@example-clinic.be>', 'Rate your visit', '2026-10-14')
        self.mail('Example Clinic <desk@example-clinic.be>', 'Free whitening', '2026-10-15', labels=['SPAM'])
        self.event('slack.message', '#alerts: build passed', '2026-10-16', 'team', 'build passed', channel_id='C1', channel_name='alerts',
                   message_ts='1.0', bot_id='B1', subtype='bot_message')
        self.event('whatsapp.message', 'Example Deals', '2026-10-16', 'chat', 'Deal of the day', chat_id='1@newsletter', chat_name='Example Deals')
        self.event('whatsapp.message', 'Ana', '2026-10-17', 'chat', 'hi!', chat_id='3201@s.whatsapp.net', chat_name='Ana')
        self.round()
        prompt = '\n'.join(self.asked)
        self.assertIn('Your referral letter', prompt)
        for bulk in ('Clinic newsletter', 'Autumn offer', 'Member update', 'Weekly digest', 'Rate your visit', 'Free whitening',
                     'build passed', 'Deal of the day', '"title": "Ana"'):
            self.assertNotIn(bulk, prompt)

    def test_a_thread_the_owner_wrote_in_a_booking_and_a_chat_they_answered_stay(self):
        self.mail('Example School <office@example-school.be>', 'Trip forms', '2026-10-01', list_unsubscribe=True, thread_id='t1')
        self.mail('Sam <sam@example.com>', 'Re: Trip forms', '2026-10-02', from_me=True, labels=['SENT'], thread_id='t1')
        self.mail('Example School <noreply@example-school.be>', 'Theater tickets', '2026-10-05',
                  bookings=[{'type': 'event', 'name': 'School play', 'start': '2026-12-01'}])
        self.event('whatsapp.message', 'Ana', '2026-10-17T08:00:00+00:00', 'chat', 'Are you coming Saturday?', chat_id='3201@s.whatsapp.net', chat_name='Ana')
        self.event('whatsapp.message', 'Ana', '2026-10-17T08:10:00+00:00', 'chat', 'Yes!', chat_id='3201@s.whatsapp.net', chat_name='Ana', from_me=True)
        self.round()
        prompt = self.asked[0]
        for kept in ('Trip forms', 'Theater tickets', 'Are you coming Saturday?'):
            self.assertIn(kept, prompt)

    def test_a_meetings_own_mail_stays_in_calendar_and_leaves_a_note_it_was_in(self):
        """An invitation, a reply to it, an update or a cancellation, in any language, never reaches a call or a note;
        mail that only shares the meeting's title is people talking and stays. Placed before: its line goes."""
        self.event('calendar.event', 'Board review', '2026-11-20T09:00:00+00:00', 'home')
        self.event('calendar.event', 'Pottery class', '2026-11-03T18:00:00+00:00', 'home')
        self.mail('Example Org <ana@example.org>', 'Board review', '2026-10-20', thread_id='talk')  # people talking
        self.mail('Sam <sam@example.com>', 'Re: Board review', '2026-10-21', thread_id='talk', labels=['SENT'])
        self.mail('Example Org <ana@example.org>', 'Board review: the numbers for it', '2026-10-22', thread_id='plan')
        self.routes = {'Board review': {'place': 'Home > Repairs and upkeep'}, 'Pottery': {'place': 'Home > Repairs and upkeep'}}
        self.mail('Ana <ana@example.org>', 'Invitation: Pottery class @ Tue Nov 3, 2026 18:00 - 19:00 (CET)', '2026-10-01', thread_id='i0')
        self.mail('Ana <ana@example.org>', 'Updated invitation: Pottery class @ Tue Nov 3, 2026 18:30', '2026-10-02', thread_id='i1')
        with mock.patch.object(topic_notes, 'meeting_mail', lambda *a: False):  # before it knew: placed
            self.round()
        self.assertIn('Invitation: Pottery class @ Tue Nov 3, 2026 18:00 - 19:00 (CET)', self.routed())
        self.asked.clear()
        for n, subject in enumerate(('Invitation: Board review @ Fri Nov 20, 2026 09:00 - 10:00 (CET)', 'Accepted: Board review',
                                     'Nieuwe afspraak: Board review op vr 20 nov 2026 09:00', 'Canceled event: Board review @ Fri Nov 20, 2026')):
            self.mail('Ana <ana@example.org>', subject, f'2026-11-0{n + 1}', thread_id=f'm{n}')
        self.mail('Sam <sam@example.com>', 'Accepted: Board review', '2026-11-06', thread_id='m9', labels=['SENT'])
        notes = self.round()
        prompt = '\n'.join(self.asked)
        for invite in ('Invitation:', 'Accepted:', 'Nieuwe afspraak', 'Canceled event'):
            self.assertNotIn(invite, prompt)
        self.assertNotIn('Pottery', ' '.join(self.routed()), 'placed before: forgotten')
        self.assertEqual(sorted(self.routed()), ['Board review', 'Board review: the numbers for it'])
        self.assertCountEqual([x['text'] for x in notes[('home', 'Repairs and upkeep')]['lines']], ['Board review', 'Board review: the numbers for it'])

    def test_a_chat_that_went_quiet_starts_a_new_conversation_and_a_slack_thread_is_one(self):
        for day in ('2026-10-01', '2026-10-01', '2026-10-10', '2026-10-10'):
            self.event('whatsapp.message', 'Ana', f'{day}T0{self.n % 9}:00:00+00:00', 'chat', 'hello', chat_id='3201@s.whatsapp.net', chat_name='Ana')
        self.event('slack.message', '#launch: plan', '2026-10-01', 'team', 'plan', channel_id='C2', channel_name='launch', message_ts='1.0', thread_ts='1.0', reply_count=1,
                   user_id='U0ANA00001')
        self.event('slack.message', '#launch: ok', '2026-10-20', 'team', 'ok', channel_id='C2', channel_name='launch', message_ts='9.0', thread_ts='1.0', user_id='U0SAM00001')
        with self.store.connect() as db:
            found = topic_notes.conversations(db, self.app.config['accounts'], __import__('datetime').date(2026, 11, 14), {'U0SAM00001'})
        self.assertEqual(sorted((c['kind'], c['count'], c['replied']) for c in found),
                         [('slack.message', 2, True), ('whatsapp.message', 2, False), ('whatsapp.message', 2, False)])


class Sources(unittest.TestCase):
    def test_every_conversation_kind_comes_from_the_registries(self):
        found = set(topic_notes.conversation_kinds())
        self.assertTrue({'gmail.message', 'outlook.message', 'slack.message', 'whatsapp.message', 'telegram.message', 'signal.message',
                         'linkedin.message', 'teams.message', 'intercom.conversation', 'x.dm', 'zoom.summary', 'meeting.transcript'} <= found)
        for kind in ('salesflare.email', 'calendar.event', 'android.notification', 'github.notification', 'fleet.message'):
            self.assertNotIn(kind, found)
        with mock.patch.dict(event_kinds.KINDS, {'example.message': {**event_kinds.KINDS['signal.message'], 'service': 'whatsapp'}}):
            self.assertIn('example.message', topic_notes.conversation_kinds(), 'a new chat kind comes in by its row')


class FirstFill(Conversations):
    """The first fill goes faster: more calls a round and rounds every FIRST_EVERY, outside the quiet hours and under
    the budget, then back to CALLS every EVERY."""

    def setUp(self):
        super().setUp()
        for x in (mock.patch.object(topic_notes, 'ASK_MAX', 2), mock.patch.object(note_pages_app, 'quiet_hours', lambda: (0, 0))):
            x.start()
            self.addCleanup(x.stop)
        self.holds = []
        self.app.background_pause = lambda **_: self.holds.pop(0) if self.holds else None
        self.app.background_spaced = lambda: True
        self.app.background_started = lambda: None
        self.app.section_notes_step = lambda: False

    def threads(self, n, start=0):
        for i in range(start, start + n):
            self.mail(f'Example Shop {i} <office@shop{i}.example>', f'Order {i}', '2026-10-06', thread_id=f'o{i}')

    def step(self):
        self.assertTrue(self.app.topic_notes_step())
        self.app.topic_notes_thread.join(10)
        return len(self.asked)

    def filled(self):
        with self.store.connect() as db:
            return bool(db.execute('SELECT 1 FROM topic_state WHERE name=?', (topic_notes.FILLED,)).fetchone())

    def again(self):
        with self.store.connect() as db:
            db.execute("DELETE FROM topic_state WHERE name='round'")

    def test_the_first_fill_makes_more_calls_then_goes_back_to_the_usual_pace(self):
        self.threads(20)
        self.assertEqual(self.step(), topic_notes.FIRST_CALLS, 'first fill: more calls a round')
        self.assertFalse(self.app.topic_notes_step(), 'not due before FIRST_EVERY')
        self.again()
        self.assertEqual(self.step(), 10, 'the rest')
        self.assertFalse(self.filled())
        self.again()
        self.step()  # nothing waits after some were placed: the first fill ends
        self.assertTrue(self.filled())
        self.threads(20, start=100)
        self.again()
        self.assertEqual(self.step(), 10 + topic_notes.CALLS, 'after the first fill: CALLS again')

    def test_after_the_first_fill_a_few_new_conversations_wait_for_more_or_half_a_day(self):
        self.threads(2)
        self.step()
        self.again()
        self.step()
        self.assertTrue(self.filled())
        asked = len(self.asked)
        self.mail('Example Garage <desk@garage.example>', 'Your car service', '2026-11-14T09:00:00+00:00', thread_id='g1')
        self.again()
        self.assertEqual(self.step(), asked, 'one fresh conversation waits for more')
        with self.store.connect() as db:
            self.assertEqual(len(topic_notes.unasked(db, topic_notes.conversations(db, self.app.config['accounts'], note_pages_app.today(), ()))), 1)
        self.mail('Example Garage <desk@garage.example>', 'Tyres', '2026-11-13T20:00:00+00:00', thread_id='g2')
        self.again()
        self.assertEqual(self.step(), asked + 1, 'one waiting for half a day is asked, with the rest')

    def test_the_budget_and_the_quiet_hours_hold_the_first_fill(self):
        self.threads(20)
        self.holds = [None, {'window': '5h', 'until': None}]  # the step goes, the second call waits for the budget
        self.assertEqual(self.step(), 1)
        self.again()
        with mock.patch.object(note_pages_app, 'quiet_hours', lambda: (0, 24)):
            self.assertEqual(self.step(), 1 + topic_notes.CALLS, 'quiet hours: the usual pace')


if __name__ == '__main__':
    unittest.main()
