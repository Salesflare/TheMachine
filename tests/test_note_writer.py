"""A note's written page (note_writer.py, NotesApp.note_writer_step): a summary, facts, decisions, open items and a
timeline above the note's lines, every bullet citing the lines it stands on, read from what was said in each
conversation. Written only when the lines changed, quality or nothing. Made-up data only; the model is a stand-in,
nothing is sent."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import machine.main as machine_main
import note_pages  # noqa: E402
import note_writer  # noqa: E402
import topic_notes  # noqa: E402
from pinned import pinned  # noqa: E402

HOME = {'id': 'home', 'email': 'sam@example.com', 'boundary': 'personal'}
AT = '2026-11-14T10:00:00+00:00'


class Pages(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [HOME]}
        self.app.note_writer_model = self.model
        self.app.background_pause = lambda **_: None
        self.app.background_spaced = lambda: True
        self.app.background_started = lambda: None
        self.asked, self.answer, self.n = [], None, 0
        pin = pinned(AT)
        pin.__enter__()
        self.addCleanup(pin.__exit__, None, None, None)

    def model(self, prompt):
        self.asked.append(prompt)
        notes = json.loads(prompt.split('Notes:\n', 1)[1])
        return json.dumps({'notes': [self.answer(n) for n in notes]}) if callable(self.answer) else self.answer

    def mail(self, sender, subject, day, body, thread, **meta):
        self.n += 1
        with self.store.connect() as db:
            return db.execute('INSERT INTO events(account_id,source_id,kind,title,body,occurred_at,metadata,content_hash,ingested_at) VALUES(?,?,?,?,?,?,?,?,?)',
                              ('home', f'e{self.n}', 'gmail.message', subject, body, f'{day}T08:00:00+00:00',
                               json.dumps({'from': sender, 'thread_id': thread, **meta}), f'h{self.n}', AT)).lastrowid

    def note(self, kind='topic', lines=None):
        """A note The Machine keeps with a line per conversation (its newest message), each conversation's messages kept
        on its route as topic_notes does."""
        first = self.mail('Example Movers <desk@example-movers.be>', 'Office move: a quote', '2026-10-01',
                          'We can move you on Saturday 24 October for 2,400 euros.\n\nKind regards,\nPat\nExample Movers', 'a')
        reply = self.mail('Sam <sam@example.com>', 'Re: Office move: a quote', '2026-10-02',
                          'Saturday works. Please book it.\n\nOn Thu, Pat wrote:\n> We can move you on Saturday', 'a', labels=['SENT'])
        lease = self.mail('Example Realty <desk@example-realty.be>', 'Lease signed', '2026-10-05', 'The lease for 12 Example Street is signed.', 'b')
        crates = self.mail('Example Movers <desk@example-movers.be>', 'Office move: crates', '2026-10-12',
                           'Forty crates arrive on Thursday 22 October; pack them by Friday evening.', 'c')
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            for conv, ids in (('c1', [first, reply]), ('c2', [lease]), ('c3', [crates])):
                db.execute("INSERT INTO topic_routes(conv,place,kind,event_id,at,events) VALUES(?,'topic:x','gmail.message',?,?,?)",
                           (conv, ids[-1], AT, json.dumps(ids)))
            drafts = [{'key': 'move', 'title': 'Office move', 'area': 'personal', 'under': ['Work'], **({'starts': '2026-10-24', 'ends': '2026-10-24'} if kind == 'trip' else {}),
                       'lines': lines or [{'key': 'conv:c1', 'text': 'Office move: a quote', 'at': '2026-10-02', 'event_id': reply},
                                          {'key': 'conv:c2', 'text': 'Lease signed', 'at': '2026-10-05', 'event_id': lease},
                                          {'key': 'conv:c3', 'text': 'Office move: crates', 'at': '2026-10-12', 'event_id': crates}]}]
            note_pages.sync(db, kind, drafts, AT)
            note_id = db.execute('SELECT id FROM note_pages WHERE key=?', (kind + ':move',)).fetchone()['id']
            ids = {str(r['key']).removeprefix('conv:'): r['id'] for r in db.execute('SELECT id,key FROM note_page_lines WHERE note_id=?', (note_id,))}
        return note_id, ids

    def written(self, ids, **more):
        quote, lease, crates = ('S' + str(ids[c]) for c in ('c1', 'c2', 'c3'))
        return lambda n: {'note': n['note'], 'summary': {'text': 'Moving the office to 12 Example Street; the movers come on Saturday 24 October.', 'sources': [quote, lease]},
                          'who': [{'text': 'Pat, the movers', 'sources': [quote]}],
                          'facts': [{'text': 'The move costs 2,400 euros.', 'sources': [quote]}, {'text': 'A bullet with nothing behind it.', 'sources': ['S999']},
                                    {'text': 'Forty crates arrive on Thursday 22 October.', 'sources': [crates]}],
                          'decisions': [{'text': 'Saturday over Sunday, since the building is closed then.', 'sources': [quote]}],
                          'open': [], 'timeline': [{'date': '2026-10-05', 'text': 'Lease signed for 12 Example Street.', 'sources': [lease]},
                                                    {'date': '2026-10-02', 'text': 'You booked the movers.', 'sources': [quote]}], **more}

    def step(self):
        self.app.note_writer_next = 0
        started = self.app.note_writer_step()
        if started:
            self.app.note_writer_thread.join(10)
        return started

    def test_a_note_gets_a_page_from_what_was_said_each_bullet_citing_its_lines(self):
        note_id, ids = self.note()
        self.answer = self.written(ids)
        self.assertTrue(self.step())
        prompt = self.asked[0]
        self.assertIn('2,400 euros', prompt, 'the messages themselves, not only their subjects')
        self.assertIn('Owner: Saturday works', prompt)
        for cut in ('Kind regards', '> We can move'):
            self.assertNotIn(cut, prompt)
        page = self.app.note_page(note_pages.node_id(note_id))['page']
        self.assertEqual(page['summary']['sources'], [ids['c1'], ids['c2']])
        self.assertEqual([b['text'] for b in page['facts']], ['The move costs 2,400 euros.', 'Forty crates arrive on Thursday 22 October.'],
                         'a bullet citing no line it was given goes')
        self.assertEqual([b['text'] for b in page['who']], ['Pat, the movers'])
        self.assertEqual([b['date'] for b in page['timeline']], ['2026-10-02', '2026-10-05'], 'oldest first')
        self.assertNotIn('open', page)
        with self.store.connect() as db:
            listed = {x['name']: x for x in self.app.notes_list(db)}
        self.assertTrue(listed['Office move']['about'].startswith('Moving the office'))
        self.assertNotIn('about', listed['Work'])

    def test_nothing_concrete_means_no_page_and_no_second_ask_until_the_lines_change(self):
        note_id, ids = self.note()
        self.answer = lambda n: {'note': n['note'], 'summary': {'text': '', 'sources': []}}
        self.assertTrue(self.step())
        self.assertNotIn('page', self.app.note_page(note_pages.node_id(note_id)))
        self.assertFalse(self.step(), 'the same lines: nothing to ask')
        with mock.patch.object(note_writer, 'NOTE_HOURS', 0), self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_pages.line_add(db, note_pages.node_id(note_id), 'Keys go to the new landlord', AT)
        self.answer = self.written(ids)
        with mock.patch.object(note_writer, 'NOTE_HOURS', 0):
            self.assertTrue(self.step(), 'a new line: written again')
        self.assertIn('page', self.app.note_page(note_pages.node_id(note_id)))

    def test_the_next_page_starts_from_the_current_one(self):
        note_id, ids = self.note()
        self.answer = self.written(ids)
        self.step()
        with mock.patch.object(note_writer, 'NOTE_HOURS', 0):
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                note_pages.line_add(db, note_pages.node_id(note_id), 'Keys go to the new landlord', AT)
            self.step()
        self.assertIn('"current_page"', self.asked[1])
        self.assertIn('The move costs 2,400 euros.', self.asked[1].split('Notes:', 1)[1])

    def test_a_removed_line_takes_the_bullets_that_stood_only_on_it(self):
        note_id, ids = self.note()
        self.answer = self.written(ids)
        self.step()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_pages.line_remove(db, ids['c2'], AT)
        page = self.app.note_page(note_pages.node_id(note_id))['page']
        self.assertEqual(page['summary']['sources'], [ids['c1']])
        self.assertEqual([b['text'] for b in page['timeline']], ['You booked the movers.'])
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_pages.line_remove(db, ids['c1'], AT)
        self.assertNotIn('page', self.app.note_page(note_pages.node_id(note_id)), 'its summary stood on nothing left: no page')

    def test_an_answer_that_isnt_one_keeps_the_page_and_waits(self):
        note_id, ids = self.note()
        self.answer = self.written(ids)
        self.step()
        with mock.patch.object(note_writer, 'NOTE_HOURS', 0), self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_pages.line_add(db, note_pages.node_id(note_id), 'Keys go to the new landlord', AT)
        self.answer = 'Sorry, I cannot help with that.'
        with mock.patch.object(note_writer, 'NOTE_HOURS', 0):
            self.step()
        self.assertIn('page', self.app.note_page(note_pages.node_id(note_id)))
        self.assertFalse(self.step(), 'it tried: it waits NOTE_HOURS')

    def test_a_conversation_not_about_the_matter_leaves_the_note_and_is_never_cited(self):
        note_id, ids = self.note()
        self.answer = self.written(ids, belongs=['S' + str(ids['c1']), 'S' + str(ids['c2'])])
        self.step()
        self.assertNotIn('page', self.app.note_page(note_pages.node_id(note_id)),
                         'two conversations of the matter left: under MIN_CONVERSATIONS, no page')
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT place FROM topic_routes WHERE conv='c3'").fetchone()['place'], '', 'it is asked about no more')
            self.assertEqual(db.execute("SELECT place FROM topic_routes WHERE conv='c1'").fetchone()['place'], 'topic:x')
            self.assertNotIn('Office move', {x['name'] for x in self.app.notes_list(db)}, 'a matter without a page is not listed')

    def test_a_source_left_out_of_belongs_is_never_cited(self):
        notes = [{'note': 'N7', 'title': 'Office move', 'sources': [{'id': f'S{i}'} for i in (1, 2, 3, 4)], '_convs': [1, 2, 3, 4]}]
        bullet = {'text': 'Forty crates arrive on Thursday 22 October.', 'sources': ['S4']}
        answer = {'notes': [{'note': 'N7', 'belongs': ['S1', 'S2', 'S3'], 'summary': {'text': 'The office moves to the second floor on December 1.', 'sources': ['S1']},
                             'facts': [{'text': 'Invoice 4411 for the movers: 900 euros, paid.', 'sources': ['S1']}, bullet],
                             'decisions': [{'text': 'Mila picked the December 1 date.', 'sources': ['S2']}],
                             'open': [{'text': 'Keys go back to the landlord by December 3.', 'sources': ['S3', 'S4']}]}]}
        page = note_writer.parse(json.dumps(answer), notes)[7]
        self.assertEqual(page['off'], [4])
        self.assertEqual(len(page['facts']), 1)
        self.assertEqual(page['open'][0]['sources'], [3])

    def test_a_thin_page_is_no_page(self):
        note_id, ids = self.note()
        full = self.written(ids)
        self.answer = lambda n: {**full(n), 'facts': [], 'decisions': []}
        self.step()
        self.assertNotIn('page', self.app.note_page(note_pages.node_id(note_id)), 'fewer than MIN_BULLETS facts, decisions and open items')
        with self.store.connect() as db:
            self.assertNotIn('Office move', {x['name'] for x in self.app.notes_list(db)})
            db.execute('BEGIN IMMEDIATE')
            note_pages.line_add(db, note_pages.node_id(note_id), 'Keys go to the new landlord', AT)
        with self.store.connect() as db:
            self.assertIn('Office move', {x['name'] for x in self.app.notes_list(db)}, 'the owner wrote in it: it is theirs to see')

    def test_trips_and_notes_with_one_message_get_no_page(self):
        self.note(kind='trip')
        with self.store.connect() as db:
            self.assertEqual(note_writer.candidates(db), [])
        self.assertFalse(self.step())
        self.assertEqual(self.asked, [])

    def test_the_day_cap_holds(self):
        self.note()
        with mock.patch.object(note_writer, 'DAY_CAP', 0), self.store.connect() as db:
            self.assertEqual(note_writer.due(db), [])

    def test_a_page_says_each_thing_once_and_without_links(self):
        notes = [{'note': 'N7', 'title': 'Office move', 'sources': [{'id': 'S1'}, {'id': 'S2'}]}]
        answer = {'notes': [{'note': 'N7', 'summary': {'text': 'The office moves to the second floor on December 1.', 'sources': ['S1']},
                             'facts': [{'text': 'Invoice 4411 for the movers: 900 euros, paid.', 'sources': ['S1']},
                                       {'text': 'The call is at https://meet.example/abc-def for the movers.', 'sources': ['S2']}],
                             'decisions': [{'text': 'The second floor, since the first is let.', 'sources': ['S2']}],
                             'open': [{'text': 'Keys go back to the landlord by December 3.', 'sources': ['S2']}],
                             'timeline': [{'date': '2026-11-02', 'text': 'Movers sent invoice 4411: 900 euros, paid.', 'sources': ['S1']},
                                          {'date': '2026-11-05', 'text': 'Mila agreed on the December 1 date.', 'sources': ['S2']}]}]}
        page = note_writer.parse(json.dumps(answer), notes)[7]
        self.assertEqual([b['text'] for b in page['facts']], ['Invoice 4411 for the movers: 900 euros, paid.'])
        self.assertEqual([b['text'] for b in page['timeline']], ['Mila agreed on the December 1 date.'])


class Conversations(unittest.TestCase):
    def test_a_line_reads_the_conversation_it_ends_and_a_lone_message_itself(self):
        with tempfile.TemporaryDirectory() as temp:
            store = machine_main.Store(Path(temp) / 'events.sqlite')
            with store.connect() as db:
                db.execute("INSERT INTO topic_routes(conv,place,event_id,at,events) VALUES('c','',7,?,'[5,6,7]')", (AT,))
                self.assertEqual(topic_notes.events_of(db, [7, 9]), {7: [5, 6, 7], 9: [9]})


if __name__ == '__main__':
    unittest.main()
