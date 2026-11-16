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
        self.app.config = {'accounts': [HOME, JOB, CHAT, TEAM], 'notes_enabled': True}
        self.asked, self.routes, self.n, self.looked, self.same = [], {}, 0, [], []
        self.app.topic_notes_model = self.model
        self.app.section_notes_model = lambda prompt: json.dumps({'places': []})
        pin = pinned(AT)
        pin.__enter__()
        self.addCleanup(pin.__exit__, None, None, None)

    def model(self, prompt):
        """Answers by title: self.routes maps a title's words to {'place': a path} | {'record': a name} | {'new': ...}.
        The look for notes about the same thing (topic_notes.merge_prompt) goes to self.looked and answers self.same:
        [([paths], title)]."""
        if prompt.startswith("These are the owner's notes"):
            self.looked.append(prompt)
            ids = {json.loads(line)['path']: json.loads(line)['id'] for line in prompt.split('<<<\n', 1)[1].split('\n>>>', 1)[0].splitlines()}
            return json.dumps({'same': [{'notes': [ids.get(p, 'N999') for p in paths], 'title': title} for paths, title in self.same]})
        self.asked.append(prompt)
        places = {}
        for line in prompt.split('The subjects that have a place already, one JSON object per line:\n', 1)[1].split('The conversations, one', 1)[0].splitlines():
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
    def test_the_call_reads_what_was_said_in_any_mailbox_or_chat_and_a_part_is_no_place(self):
        """A part of Home, Health or Kids is a category, not a matter: no conversation goes there (only the owner's own
        notes in it are places)."""
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
        self.assertNotIn(('kids', 'School'), notes)
        self.assertEqual(set(self.routed().values()), {''})
        prompt = self.asked[0]
        self.assertNotIn('"path": "Kids > School"', prompt)
        self.assertIn('Lunch boxes', prompt, 'a notification nobody answered reaches the call too')
        self.assertIn('Bring a packed lunch.', prompt, 'the call reads what was said')
        self.assertIn('Owner: Thanks, she will be there.', prompt)
        for cut in ('Kind regards', '+32 000', '> The class goes'):
            self.assertNotIn(cut, prompt, 'quoted history and the signature are left out')
        self.assertIn('"source": "WhatsApp"', prompt)
        self.assertIn('Swimming moves to 17:00', prompt)

    def test_every_subject_named_is_a_note_and_one_under_kids_is_personal(self):
        """No count of replies or conversations: a school's notices nobody answered make a subject, the page writer's
        bar decides what shows. Under Home, Health, Kids or Pets it is Personal, wherever the mail came in."""
        self.routes = {'Term dates': {'new': {'title': "Ava's school", 'under': 'Kids'}},
                       'Swimming gala': {'new': {'title': "Ava's school", 'under': 'Kids'}},
                       'Office move': {'new': {'title': 'Office move', 'under': 'Work'}}}
        self.mail('Example Primary <noreply@example-primary.be>', 'Term dates for spring', '2026-10-01', account='job', thread_id='a',
                  list_unsubscribe=True, body='Spring term runs from 6 January to 3 April.')
        self.mail('Example Primary <noreply@example-primary.be>', 'Swimming gala on Friday', '2026-10-03', account='job', thread_id='b',
                  body='Bring a towel and goggles; the bus leaves at 9:00.')
        self.mail('Example Movers <desk@example-movers.be>', 'Office move: a quote', '2026-10-05', account='job', thread_id='c')
        self.mail('Example Cloud <billing@cloud.example>', 'Office move: your invoice', '2026-10-06', account='job', thread_id='d')
        notes = self.round()
        self.assertNotIn(('topic', 'Office move'), notes, 'at work, notices alone are no relationship: no note until the owner writes')
        self.mail('Sam <sam@acme.example>', 'Re: Office move: a quote', '2026-10-07', account='job', thread_id='c', labels=['SENT'])
        notes = self.round()
        school = notes[('topic', "Ava's school")]
        self.assertEqual([x['name'] for x in school['path']], ['Kids'])
        self.assertEqual(school['area'], 'personal', 'under Kids: Personal, though it came in on the work mailbox')
        self.assertEqual([x['text'] for x in school['lines']], ['Swimming gala on Friday', 'Term dates for spring'], 'newest first')
        self.assertEqual(notes[('topic', 'Office move')]['area'], 'work:Acme', 'one conversation the owner wrote in is enough to start')
        self.assertEqual(len(notes[('topic', 'Office move')]['lines']), 2, 'and its notices come with it')

    def test_notifications_reach_the_call_bounces_and_automatic_replies_dont(self):
        self.mail('Example Primary <office@example-primary.be>', 'Note to all parents', '2026-10-06', thread_id='n', list_id='<parents.example-primary.be>')
        self.mail('Example Shop <no-reply@shop.example>', 'Your order shipped', '2026-10-06', thread_id='o', precedence='bulk')
        self.mail('Example Clinic <desk@example-clinic.be>', 'Appointment on 12 November at 9:30', '2026-10-06', thread_id='p', auto_submitted='auto-generated')
        self.mail('Mail Delivery Subsystem <mailer-daemon@example.com>', 'Delivery Status Notification (Failure)', '2026-10-07', thread_id='x')
        self.mail('Dana <dana@example.net>', 'Out of office', '2026-10-08', thread_id='d', auto_submitted='auto-replied')
        self.round()
        prompt = '\n'.join(self.asked)
        for kept in ('Note to all parents', 'Your order shipped', 'Appointment on 12 November'):
            self.assertIn(kept, prompt, 'a notification holds the facts a note is made of')
        for left in ('Delivery Status', 'Out of office'):
            self.assertNotIn(left, prompt)

    def test_one_busy_sender_cannot_fill_the_calls(self):
        for i in range(topic_notes.NOTICES_EACH + 5):
            self.mail('Example Shop <no-reply@shop.example>', f'Order {i} shipped', f'2026-10-{i + 1:02d}', thread_id=f'o{i}')
        with self.store.connect() as db:
            waiting = topic_notes.unasked(db, topic_notes.conversations(db, self.app.config['accounts'], __import__('datetime').date(2026, 11, 14), ()))
        self.assertEqual(len(waiting), topic_notes.NOTICES_EACH)
        self.assertEqual(waiting[0]['title'], f'Order {topic_notes.NOTICES_EACH + 4} shipped', 'the newest')

    def test_a_notice_sent_back_by_its_page_goes_to_its_own_subject(self):
        """The page writer found it is about another child (topic_notes.unroute): asked once more, told where it was,
        and the call can't put it back there."""
        self.routes = {'Class trip': {'new': {'title': "Ava's school", 'under': 'Kids'}}}
        self.mail('Example Primary <office@example-primary.be>', 'Class trip for year 3', '2026-10-06', thread_id='n')
        self.round()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            topic_notes.unroute(db, next(iter(r['conv'] for r in db.execute('SELECT conv FROM topic_routes'))))
        self.routes = {'Class trip': {'new': {'title': "Leo's school", 'under': 'Kids'}}}
        notes = self.round()
        self.assertIn('"not": "Kids > Ava', self.asked[-1])
        self.assertIn(('topic', "Leo's school"), notes)
        self.assertNotIn(('topic', "Ava's school"), notes, 'nothing is placed in it any more: it goes')

    def test_the_place_a_page_sent_it_back_from_is_refused(self):
        self.routes = {'Class trip': {'new': {'title': "Ava's school", 'under': 'Kids'}}}
        self.mail('Example Primary <office@example-primary.be>', 'Class trip for year 3', '2026-10-06', thread_id='n')
        self.round()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            topic_notes.unroute(db, next(iter(r['conv'] for r in db.execute('SELECT conv FROM topic_routes'))))
        self.routes = {'Class trip': {'place': "Kids > Ava's school"}}
        self.round()
        self.assertEqual(list(self.routed().values()), [''], 'the same place again: nowhere')

    def test_a_conversation_placed_in_a_trip_is_a_line_of_it(self):
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_pages.sync(db, 'trip', [{'key': 'lisbon', 'title': 'Lisbon trip', 'area': 'personal', 'starts': '2026-12-01', 'ends': '2026-12-04',
                                          'lines': [{'key': 'b1', 'text': 'Flight to Lisbon'}]}], AT)
        self.routes = {'Airport transfer': {'place': 'Lisbon trip'}}
        self.mail('Example Transfers <bookings@transfers.example>', 'Airport transfer confirmed', '2026-11-02', thread_id='t')
        notes = self.round()
        self.assertIn('Airport transfer confirmed', [x['text'] for x in notes[('trip', 'Lisbon trip')]['lines']])

    def test_a_title_never_carries_a_reference_and_one_that_is_only_a_reference_is_no_subject(self):
        self.assertEqual(topic_notes.clean_title('Example Shop order 302-3037924-2949104'), 'Example Shop order')
        self.assertEqual(topic_notes.clean_title('Holiday park reservation 00526018702'), 'Holiday park reservation')
        self.assertEqual(topic_notes.clean_title('Cloud billing account 0180A3-CB8A25-B85193'), 'Cloud billing account')
        self.assertEqual(topic_notes.clean_title('Flights KX7P2Q (Porto)'), 'Flights (Porto)')
        self.assertEqual(topic_notes.clean_title('Order #4410'), 'Order')
        for kept in ('Hiring in 2027', 'Lenovo M75s G2', 'Parking space P51'):
            self.assertEqual(topic_notes.clean_title(kept), kept, 'a year or a model is a name')
        self.routes = {'Your order': {'new': {'title': 'Example Shop 302-3037924', 'under': 'Home'}},
                       'Receipt': {'new': {'title': '#88213', 'under': 'Home'}}}
        self.mail('Example Shop <orders@shop.example>', 'Your order 302-3037924 shipped', '2026-11-02', thread_id='o1')
        self.mail('Example Shop <orders@shop.example>', 'Your order 302-9999999 shipped', '2026-11-03', thread_id='o2')
        self.mail('Example Café <desk@cafe.example>', 'Receipt 88213', '2026-11-03', thread_id='r')
        notes = self.round()
        self.assertEqual([k for k in notes if k[0] == 'topic'], [('topic', 'Example Shop')], 'orders from one shop: one note about the shop')
        self.assertIn('Never one order, delivery, receipt', self.asked[0])

    def test_notes_about_the_same_thing_become_one_and_a_later_call_naming_one_goes_there(self):
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_pages.sync(db, 'trip', [{'key': 'park', 'title': 'Holiday park trip', 'area': 'personal', 'starts': '2026-12-01', 'ends': '2026-12-04',
                                          'lines': [{'key': 'b1', 'text': 'Cabin booked'}]}], AT)
        self.routes = {'Cabin': {'new': {'title': 'Holiday park cabin', 'under': 'Trips'}},
                       'Listing': {'new': {'title': 'Example Co listing', 'under': 'Work'}},
                       'Affiliate': {'new': {'title': 'Example Co affiliate deal', 'under': 'Work'}},
                       'Article': {'new': {'title': 'Example Co guest article', 'under': 'Work'}}}
        self.mail('Holiday Park <desk@park.example>', 'Cabin check-in times', '2026-11-02', thread_id='c')
        self.mail('Ana <ana@example.co>', 'Listing update', '2026-11-03', account='job', thread_id='l')
        self.mail('Ana <ana@example.co>', 'Affiliate terms', '2026-11-04', account='job', thread_id='a')
        self.mail('Ana <ana@example.co>', 'Article draft', '2026-11-05', account='job', thread_id='g')
        for subject, thread in (('Listing update', 'l'), ('Affiliate terms', 'a'), ('Article draft', 'g')):
            self.mail('Sam <sam@acme.example>', 'Re: ' + subject, '2026-11-05', account='job', thread_id=thread, labels=['SENT'])
        self.same = [(['Trips > Holiday park cabin', 'Holiday park trip'], 'Holiday park'),
                     (['Work > Example Co listing', 'Work > Example Co affiliate deal', 'Work > Example Co guest article'], 'Example Co partnership 12345')]
        notes = self.round()
        self.assertEqual(len(self.looked), 1)
        self.assertNotIn(('topic', 'Holiday park cabin'), notes)
        self.assertIn('Cabin check-in times', [x['text'] for x in notes[('trip', 'Holiday park trip')]['lines']], 'the trip from the booking takes it')
        work = [k for k in notes if k[0] == 'topic']
        self.assertEqual(work, [('topic', 'Example Co partnership')], 'one company at work: one note, its title without the number')
        self.assertEqual(len(notes[work[0]]['lines']), 3)
        self.routes = {'Invoice': {'new': {'title': 'Example Co affiliate deal', 'under': 'Work'}}}
        self.same = []
        self.mail('Ana <ana@example.co>', 'Invoice for October', '2026-11-06', account='job', thread_id='i')
        notes = self.round()
        self.assertEqual([k for k in notes if k[0] == 'topic'], [('topic', 'Example Co partnership')], 'the merged title leads to the note it went in')
        self.assertEqual(len(notes[('topic', 'Example Co partnership')]['lines']), 4)

    def test_the_same_name_in_two_folders_is_one_note_without_asking(self):
        self.routes = {'Vouchers': {'new': {'title': 'Example Vouchers', 'under': 'Work'}}, 'Card': {'new': {'title': 'Example vouchers', 'under': 'Home'}},
                       'Topup': {'new': {'title': 'Example Vouchers', 'under': 'Work'}}}
        self.mail('Example Vouchers <desk@vouchers.example>', 'Vouchers for November', '2026-11-02', account='job', thread_id='v')
        self.mail('Example Vouchers <desk@vouchers.example>', 'Topup done', '2026-11-03', account='job', thread_id='t')
        self.mail('Example Vouchers <desk@vouchers.example>', 'Card blocked', '2026-11-04', thread_id='c')
        self.mail('Sam <sam@acme.example>', 'Re: Topup done', '2026-11-04', account='job', thread_id='t', labels=['SENT'])
        notes = self.round()
        self.assertEqual([k for k in notes if k[0] == 'topic'], [('topic', 'Example Vouchers')], 'the one with the most sources takes the other')
        self.assertEqual(len(notes[('topic', 'Example Vouchers')]['lines']), 3)

    def test_a_vendors_notices_and_a_persons_name_make_no_note(self):
        """A vendor's billing and notices at work make no note (no working relationship until the owner writes); a title
        that is a person's name goes to their page in the Graph, never a note."""
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('person:ana','person','Ana Example',1,3,'{}')")
        self.routes = {'Usage': {'new': {'title': 'Example Cloud', 'under': 'Work'}}, 'Invoice': {'new': {'title': 'Example Cloud', 'under': 'Work'}},
                       'Coffee': {'new': {'title': 'Ana Example', 'under': 'Work'}}}
        self.mail('Example Cloud <billing@cloud.example>', 'Invoice for October', '2026-11-02', account='job', thread_id='i')
        self.mail('Example Cloud <alerts@cloud.example>', 'Usage alert', '2026-11-03', account='job', thread_id='u')
        self.mail('Ana <ana@example.co>', 'Coffee next week?', '2026-11-03', account='job', thread_id='c')
        self.mail('Sam <sam@acme.example>', 'Re: Coffee next week?', '2026-11-04', account='job', thread_id='c', labels=['SENT'])
        notes = self.round()
        self.assertEqual([k for k in notes if k[0] == 'topic'], [])
        self.assertEqual(self.routed()['Coffee next week?'], 'record:person:ana', "on the person's page")
        for rule in ('A vendor or service the owner uses', 'A person is never a subject'):
            self.assertIn(rule, self.asked[0])

    def test_a_subject_keeps_its_name_when_the_conversation_that_named_it_leaves(self):
        self.routes = {'Tiles': {'new': {'title': 'Kitchen', 'under': 'Home'}}, 'Worktop': {'place': 'Home > Kitchen'}, 'Sink': {'place': 'Home > Kitchen'}}
        self.mail('Dana <dana@build.example>', 'Tiles', '2026-11-02', thread_id='t')
        self.round()
        self.mail('Dana <dana@build.example>', 'Worktop', '2026-11-03', thread_id='w')
        self.mail('Dana <dana@build.example>', 'Sink', '2026-11-04', thread_id='s')
        self.round()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            topic_notes.unroute(db, next(r['conv'] for r in db.execute("SELECT conv FROM topic_routes WHERE title='Tiles'")))
            topic_notes.unroute(db, next(r['conv'] for r in db.execute("SELECT conv FROM topic_routes WHERE title='Tiles'")))
            self.assertEqual(topic_notes.drafts(db)[0]['title'], 'Kitchen', 'its name stays with the others')
            self.assertEqual(topic_notes.drafts(db)[0]['under'], ['Home'])
            db.execute("UPDATE topic_routes SET note=NULL WHERE place LIKE 'topic:%'")
            self.assertEqual(topic_notes.drafts(db), [], 'a subject without a name is no note')
            self.assertEqual([p for p in topic_notes.places(db, []) if not p['path']], [], 'and no place a call is offered')

    def test_a_work_folder_note_from_a_personal_mailbox_needs_the_owner_to_write_too(self):
        self.routes = {'Profile': {'new': {'title': 'Example Listing', 'under': 'Work'}}}
        self.mail('Example Listing <reports@listing.example>', 'Profile report', '2026-11-02', thread_id='p')
        self.mail('Example Listing <reports@listing.example>', 'Profile report for October', '2026-11-03', thread_id='q')
        self.assertEqual([k for k in self.round() if k[0] == 'topic'], [])

    def test_the_look_for_twins_sees_when_each_notes_messages_came_in(self):
        self.routes = {'Cabin': {'new': {'title': 'Holiday park', 'under': 'Trips'}}, 'Birthday': {'new': {'title': 'Holiday park birthday trip', 'under': 'Trips'}}}
        self.mail('Holiday Park <desk@park.example>', 'Cabin booked', '2026-10-02', thread_id='c')
        self.mail('Holiday Park <desk@park.example>', 'Birthday package', '2026-10-09', thread_id='b')
        self.same = [(['Trips > Holiday park', 'Trips > Holiday park birthday trip'], 'Holiday park')]
        notes = self.round()
        self.assertIn('"period": "2026-10-02 to 2026-10-02"', self.looked[0])
        self.assertIn('without dates, the same destination', self.looked[0])
        self.assertEqual([k for k in notes if k[0] == 'topic'], [('topic', 'Holiday park')])

    def test_a_note_the_owner_wrote_in_is_never_merged_away(self):
        self.routes = {'Tiles': {'new': {'title': 'Kitchen tiles', 'under': 'Home'}}, 'Worktop': {'new': {'title': 'Kitchen worktop', 'under': 'Home'}}}
        self.mail('Dana <dana@build.example>', 'Tiles', '2026-11-02', thread_id='t')
        self.mail('Dana <dana@build.example>', 'Worktop', '2026-11-03', thread_id='w')
        self.round()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            tiles = db.execute("SELECT id FROM note_pages WHERE title='Kitchen tiles'").fetchone()['id']
            note_pages.edit(db, note_pages.node_id(tiles), AT, ['personal'], title='Tiles we picked')
        self.mail('Dana <dana@build.example>', 'Sink', '2026-11-04', thread_id='s')
        self.routes['Sink'] = {'new': {'title': 'Kitchen sink', 'under': 'Home'}}
        self.same = [(['Home > Tiles we picked', 'Home > Kitchen worktop'], 'Kitchen renovation')]
        notes = self.round()
        titles = sorted(k[1] for k in notes if k[0] == 'topic')
        self.assertIn('Tiles we picked', titles, 'the owner named it: it takes the other, keeps its name')
        self.assertNotIn('Kitchen worktop', titles)

    def test_a_matter_the_graph_has_goes_to_that_record_not_a_second_note(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('project:p1','project','Example Rollout',1,3,'{}')")
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('org:example.org','org','Example Org',1,3,'{}')")
        first = self.mail('Ana <ana@example.org>', 'Rollout plan', '2026-10-01', account='job', thread_id='r')
        self.mail('Sam <sam@acme.example>', 'Re: Rollout plan', '2026-10-01', account='job', thread_id='r', labels=['SENT'])
        self.mail('Ana <ana@example.org>', 'Rollout week two', '2026-10-08', account='job', thread_id='s')
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_events(node_id,event_id,at,direct) VALUES('project:p1',?,?,1)", (first, AT))
        self.routes = {'Rollout plan': {'record': 'Example Rollout'}, 'Rollout week two': {'new': {'title': 'example org', 'under': 'Work'}, 'ongoing': True}}
        notes = self.round()
        self.assertIn('"name": "Example Rollout", "kind": "project"', self.asked[0])
        self.assertEqual(self.routed(), {'Rollout plan': 'record:project:p1', 'Rollout week two': 'record:org:example.org'})
        self.assertFalse([k for k in notes if k[0] == 'topic'])

    def test_each_conversation_is_asked_about_once_and_its_later_messages_follow_it(self):
        self.routes = {'Boiler': {'new': {'title': 'Boiler', 'under': 'Home'}}, 'Gutter': {'new': {'title': 'Gutter', 'under': 'Home'}}}
        self.mail('Example Plumber <office@example-plumber.be>', 'Boiler service', '2026-10-20', thread_id='b')
        self.mail('Sam <sam@example.com>', 'Re: Boiler service', '2026-10-20', thread_id='b', labels=['SENT'])
        self.mail('Example Roofer <office@example-roofer.be>', 'Gutter repair', '2026-10-21', thread_id='g')
        self.mail('Sam <sam@example.com>', 'Re: Gutter repair', '2026-10-21', thread_id='g', labels=['SENT'])
        self.round()
        self.assertEqual(len(self.asked), 1)
        later = self.mail('Example Plumber <office@example-plumber.be>', 'Re: Boiler service', '2026-11-02', thread_id='b')
        self.round()
        self.assertEqual(len(self.asked), 1, 'nothing new: no call')
        with self.store.connect() as db:
            route = db.execute("SELECT last_at,event_id FROM topic_routes WHERE title='Boiler service'").fetchone()
        self.assertEqual((str(route['last_at'])[:10], route['event_id']), ('2026-11-02', later))

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
    """Bulk never reaches a call or a note: spam always; Gmail's marketing tabs, automatic replies and bounces unless
    the owner wrote in the thread or it carries a booking; bots, broadcasts and lone chat messages."""

    def test_bulk_mail_and_bulk_chat_are_left_out_before_any_call(self):
        self.mail('Example Clinic <desk@example-clinic.be>', 'Your referral letter', '2026-10-08', thread_id='ref')
        self.mail('Sam <sam@example.com>', 'Re: Your referral letter', '2026-10-08', thread_id='ref', labels=['SENT'])
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
        for notice in ('Your referral letter', 'Clinic newsletter', 'Member update', 'Weekly digest', 'Rate your visit'):
            self.assertIn(notice, prompt, 'a notification reaches the call: the call leaves out the ones with nothing for the owner')
        for bulk in ('Autumn offer', 'Free whitening', 'build passed', 'Deal of the day', '"title": "Ana"'):
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
        self.routes = {'Board review': {'new': {'title': 'Board review', 'under': 'Work'}}, 'Pottery': {'new': {'title': 'Board review', 'under': 'Work'}}}
        self.mail('Example Org <ana@example.org>', 'Invitation: Pottery class @ Tue Nov 3, 2026 18:00 - 19:00 (CET)', '2026-10-01', thread_id='i0')
        self.mail('Example Org <ana@example.org>', 'Updated invitation: Pottery class @ Tue Nov 3, 2026 18:30', '2026-10-02', thread_id='i1')
        with mock.patch.object(topic_notes, 'meeting_mail', lambda *a: False):  # before it knew: placed
            self.round()
        self.assertIn('Invitation: Pottery class @ Tue Nov 3, 2026 18:00 - 19:00 (CET)', self.routed())
        self.asked.clear()
        for n, subject in enumerate(('Invitation: Board review @ Fri Nov 20, 2026 09:00 - 10:00 (CET)', 'Accepted: Board review',
                                     'Nieuwe afspraak: Board review op vr 20 nov 2026 09:00', 'Canceled event: Board review @ Fri Nov 20, 2026')):
            self.mail('Ana <ana@example.org>', subject, f'2026-11-0{n + 1}', thread_id=f'm{n}')
        self.mail('Sam <sam@example.com>', 'Accepted: Board review', '2026-11-06', thread_id='m9', labels=['SENT'])
        self.round()
        prompt = '\n'.join(self.asked)
        for invite in ('Invitation:', 'Accepted:', 'Nieuwe afspraak', 'Canceled event'):
            self.assertNotIn(invite, prompt)
        self.assertNotIn('Pottery', ' '.join(self.routed()), 'placed before: forgotten')
        self.assertEqual(sorted(self.routed()), ['Board review', 'Board review: the numbers for it'])

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
            self.mail('Sam <sam@example.com>', f'Re: Order {i}', '2026-10-06', thread_id=f'o{i}', labels=['SENT'])

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
        self.mail('Sam <sam@example.com>', 'Re: Your car service', '2026-11-14T09:00:00+00:00', thread_id='g1', labels=['SENT'])
        self.again()
        self.assertEqual(self.step(), asked, 'one fresh conversation waits for more')
        with self.store.connect() as db:
            self.assertEqual(len(topic_notes.unasked(db, topic_notes.conversations(db, self.app.config['accounts'], note_pages_app.today(), ()))), 1)
        self.mail('Example Garage <desk@garage.example>', 'Tyres', '2026-11-13T20:00:00+00:00', thread_id='g2')  # from someone the owner wrote to
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
