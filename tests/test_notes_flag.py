"""Notes behind notes_enabled (NotesApp.notes_on, docs/notes.md): off by default, no Notes anywhere and no notes model
call, the notes kept staying in the database and trips and events still in Calendar; the first round with it on
starts the notes from conversations over, the earlier ones kept readable under Earlier notes. Made-up data only; the
model is a stand-in, nothing is sent."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

import machine.main as machine_main
import note_pages  # noqa: E402
import topic_notes  # noqa: E402
from machine.store import whats_new  # noqa: E402
from pinned import pinned  # noqa: E402

HOME = {'id': 'home', 'email': 'sam@example.com', 'boundary': 'personal'}
AT = '2026-11-14T10:00:00+00:00'


class Flag(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [HOME]}
        self.asked = []
        for name in ('topic_notes_model', 'section_notes_model', 'note_writer_model', 'folder_overview_model', 'memory_seed_model'):
            setattr(self.app, name, self.model)
        self.app.background_pause = lambda **_: None
        self.app.background_spaced = lambda: True
        self.app.background_started = lambda: None
        self.app.bring_in_workspace = lambda: Path(temp.name)
        pin = pinned(AT)
        pin.__enter__()
        self.addCleanup(pin.__exit__, None, None, None)
        self.n = 0
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_pages.sync(db, 'trip', [{'key': 'lisbon', 'title': 'Lisbon trip', 'area': 'personal', 'starts': '2026-11-20', 'ends': '2026-11-23',
                                          'lines': [{'key': 'b1', 'text': 'Flight to Lisbon', 'event_id': self.mail('Flight to Lisbon', db)},
                                                    {'key': 'b2', 'text': 'Hotel in Lisbon', 'event_id': self.mail('Hotel in Lisbon', db)}]}], AT)
            lines = [{'key': f'conv:c{i}', 'text': f'Kitchen tiles {i}', 'event_id': self.mail(f'Kitchen tiles {i}', db)} for i in range(3)]
            note_pages.sync(db, 'topic', [{'key': 'kitchen', 'title': 'Kitchen renovation', 'area': 'personal', 'under': ['Home'], 'lines': lines}], AT)
            note_pages.sync(db, 'topic', [{'key': 'gala', 'title': 'Swim gala', 'area': 'personal', 'under': ['Kids'],
                                           'lines': [{'key': 'conv:g', 'text': 'Gala on Friday'}]}], AT, lambda k: True)
            note_pages.sync(db, 'home', [{'key': 'bills', 'title': 'Bills and subscriptions', 'area': 'personal', 'under': ['Home'],
                                          'lines': [{'key': 'bill:energy', 'text': 'Energy, every month'}]}], AT, lambda k: True)
            self.trip = db.execute("SELECT id FROM note_pages WHERE kind='trip'").fetchone()['id']
            self.kitchen = db.execute("SELECT id FROM note_pages WHERE key='topic:kitchen'").fetchone()['id']
            self.gala = db.execute("SELECT id FROM note_pages WHERE key='topic:gala'").fetchone()['id']
            self.own = note_pages.parse_id(note_pages.create(db, 'Garden', 'personal', AT, ['personal'], ['Hedge trimmed in spring'])['id'])
            note_pages.edit(db, note_pages.node_id(self.gala), AT, ['personal'], title='Gala season')  # the owner renamed it
            db.execute("INSERT INTO topic_routes(conv,place,kind,at) VALUES('c0','topic:kitchen','gmail.message',?)", (AT,))

    def model(self, prompt):
        self.asked.append(prompt)
        return json.dumps({'places': [], 'notes': [], 'pages': []})

    def mail(self, subject, db=None):
        self.n += 1
        sql = ('INSERT INTO events(account_id,source_id,kind,title,body,occurred_at,metadata,content_hash,ingested_at) VALUES(?,?,?,?,?,?,?,?,?)',
               ('home', f'e{self.n}', 'gmail.message', subject, subject, AT, json.dumps({'from': 'Example <desk@example.com>'}), f'h{self.n}', AT))
        if db is not None:
            return db.execute(*sql).lastrowid
        with self.store.connect() as own:
            return own.execute(*sql).lastrowid

    def steps(self):
        out = [self.app.topic_notes_step(), self.app.section_notes_step(), self.app.memory_seed_step(), self.app.note_writer_step(),
               self.app.folder_overview_step()]
        for name in ('topic_notes_thread', 'section_notes_thread', 'memory_seed_thread', 'note_writer_thread', 'folder_overview_thread'):
            thread = getattr(self.app, name, None)
            if thread:
                thread.join(10)
        return out

    def test_off_by_default_no_notes_anywhere_and_no_model_call(self):
        self.assertFalse(self.app.notes_on())
        self.assertEqual(self.steps(), [False] * 5)
        self.assertEqual(self.asked, [], 'no notes model call')
        with self.store.connect() as db:
            self.assertEqual(self.app.notes_list(db), [])
            self.assertEqual(db.execute("SELECT count(*) FROM note_pages WHERE kind<>'note'").fetchone()[0], 4, 'the notes kept stay')
            self.assertEqual(db.execute("SELECT count(*) FROM topic_routes").fetchone()[0], 1, 'no rebuild while off')
        with self.assertRaises(ValueError):
            self.app.note_page(note_pages.node_id(self.kitchen))
        with self.assertRaises(ValueError):
            self.app.note_page(note_pages.node_id(self.own))
        with self.assertRaises(ValueError):
            self.app.note_action('note_new', {'title': 'Car'}, owner_dashboard=True)

    def test_off_a_trip_still_shows_in_calendar_and_opens_from_there(self):
        bands = self.app.calendar_notes('2026-11-16T00:00:00+00:00', '2026-11-30T00:00:00+00:00')
        self.assertEqual([b['name'] for b in bands], ['Lisbon trip'])
        page = self.app.note_page(note_pages.node_id(self.trip))
        self.assertEqual([x['text'] for x in page['lines']], ['Flight to Lisbon', 'Hotel in Lisbon'])
        self.assertEqual(page['tree'], [], 'no other note through it')

    def test_off_whats_new_tells_nothing_about_notes(self):
        notes = [e for e in whats_new.ENTRIES if 'Notes' in e['title'] or 'note' in e['id']]
        self.assertTrue(notes and all(e.get('who') == 'notes' for e in notes))
        entries = [{'id': 'a', 'date': '2026-11-13', 'weight': 3, 'who': 'notes', 'title': 'Notes', 'text': 'Notes.'},
                   {'id': 'b', 'date': '2026-11-13', 'weight': 1, 'title': 'Other', 'text': 'Other.'}]
        with self.store.connect() as db:
            db.execute("INSERT OR REPLACE INTO milestones(name,at,detail) VALUES('first_dig_done','2026-11-01T08:00:00+00:00','{}')")
            current = dt.datetime.fromisoformat(AT)
            self.assertEqual([e['id'] for e in whats_new.candidates(db, current, entries)], ['b'])
            self.assertEqual([e['id'] for e in whats_new.candidates(db, current, entries, notes=True)], ['a', 'b'])

    def test_on_the_first_round_starts_over_and_keeps_the_earlier_notes_readable(self):
        self.app.config['notes_enabled'] = True
        self.app.topic_notes_step()
        thread = getattr(self.app, 'topic_notes_thread', None)
        if thread:
            thread.join(10)
        with self.store.connect() as db:
            self.assertIsNone(db.execute("SELECT 1 FROM topic_routes WHERE conv='c0' OR place LIKE 'topic:%'").fetchone(),
                              'every conversation is sorted again')
            kinds = {r['id']: (r['kind'], r['key']) for r in db.execute('SELECT id,kind,key FROM note_pages')}
            self.assertEqual(kinds[self.kitchen], ('archived', 'archived:topic:kitchen'))
            self.assertEqual(kinds[self.gala][0], 'topic', 'the owner renamed it: it stays as it is')
            self.assertEqual(kinds[self.trip][0], 'trip')
            self.assertEqual(kinds[self.own][0], 'note')
            home = [k for k in kinds.values() if k[1] == 'archived:home:bills']
            self.assertEqual(len(home), 1, 'Home, Health and Kids are subjects now: the old part is kept')
            page = note_pages.page(db, self.kitchen)
            self.assertEqual([p['name'] for p in page['path']], [note_pages.ARCHIVE])
            self.assertEqual(len(page['lines']), 3, 'readable as it was, nothing deleted')
            self.assertIn('Kitchen renovation', {x['name'] for x in self.app.notes_list(db)})
            db.execute("INSERT INTO topic_routes(conv,place,kind,at) VALUES('c9','topic:new','gmail.message',?)", (AT,))
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            self.assertFalse(topic_notes.rebuild(db, AT), 'once')
            self.assertIsNotNone(db.execute("SELECT 1 FROM topic_routes WHERE conv='c9'").fetchone())


if __name__ == '__main__':
    unittest.main()
