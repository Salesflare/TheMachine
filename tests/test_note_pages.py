"""Trips and events (note_pages.py, note_pages_app.py): how sync keeps them under Trips with what an owner changed
before on top, their Calendar bands and their page; and the notes of the Notes feature that is gone, which stay in
the database untouched and show nowhere. Made-up data only."""
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

import machine.main as machine_main
import note_pages  # noqa: E402
from machine import actions  # noqa: E402
from machine.owner_error import OwnerError  # noqa: E402
from pinned import pinned  # noqa: E402

AT = '2026-11-14T10:00:00+00:00'
LATER = '2026-11-15T10:00:00+00:00'
HOME = {'id': 'home', 'email': 'sam@example.com', 'boundary': 'personal'}


def trip(key='lisbon', title='Lisbon', lines=None, **more):
    return {'key': key, 'title': title, 'starts': '2026-12-03', 'ends': '2026-12-06', 'under': ['Trips'],
            'lines': lines if lines is not None else [
                {'key': 'flight-out', 'text': 'Flight TP 643 Brussels to Lisbon, booking ABC123', 'at': '2026-12-03T07:10'},
                {'key': 'hotel', 'text': 'Hotel Rua Augusta, 3 nights', 'at': '2026-12-03'}], **more}


class NotePagesTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite')
        self.db = self.enterContext(self.store.connect())

    def rows(self):
        return {r['owner_title'] or r['title']: r for r in self.db.execute('SELECT * FROM note_pages WHERE removed_at IS NULL')}

    def test_their_words_are_sealed_at_rest(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite', protect=True)
        self.db = self.enterContext(self.store.connect())
        note_pages.sync(self.db, 'trip', [trip()], LATER)
        self.db.commit()
        raw = sqlite3.connect(self.store.path)
        stored = [*raw.execute('SELECT title FROM note_pages'), *raw.execute('SELECT text FROM note_page_lines')]
        raw.close()
        for (value,) in stored:
            self.assertNotIn(b'Lisbon', value if isinstance(value, bytes) else value.encode())
            self.assertNotIn(b'ABC123', value if isinstance(value, bytes) else value.encode())
        lisbon = self.rows()['Lisbon']['id']
        self.assertIn('ABC123', note_pages.page(self.db, lisbon)['lines'][0]['text'])

    def test_sync_places_a_trip_under_trips_and_keeps_what_an_owner_changed_before(self):
        note_pages.sync(self.db, 'trip', [trip()], AT)
        rows = self.rows()
        self.assertEqual(rows['Lisbon']['parent_id'], rows['Trips']['id'])
        lisbon = rows['Lisbon']['id']
        flight, hotel = note_pages.page(self.db, lisbon)['lines']
        # what an owner did while Notes could still edit a trip: renamed it, changed its end, a line in their words, one removed
        self.db.execute("UPDATE note_pages SET owner_title='Lisbon with the team',ends='2026-12-07',owner_dates=1 WHERE id=?", (lisbon,))
        self.db.execute("UPDATE note_page_lines SET owner_text='Flight TP 643, seat 12A' WHERE id=?", (flight['id'],))
        self.db.execute('UPDATE note_page_lines SET removed_at=? WHERE id=?', (AT, hotel['id']))
        note_pages.sync(self.db, 'trip', [trip(title='Lisbon trip', ends='2026-12-08', lines=[
            {'key': 'flight-out', 'text': 'Flight TP 645 Brussels to Lisbon, booking ABC123'},
            {'key': 'hotel', 'text': 'Hotel Rua Augusta, 4 nights'},
            {'key': 'train', 'text': 'Train to Sintra'}])], LATER)
        page = note_pages.page(self.db, lisbon)
        self.assertEqual((page['name'], page['ends'], page['dated']), ('Lisbon with the team', '2026-12-07', True))
        self.assertEqual([x['text'] for x in page['lines']], ['Flight TP 643, seat 12A', 'Train to Sintra'])
        self.assertTrue(page['lines'][0]['edited'])

    def test_a_removed_trip_or_folder_stays_removed(self):
        note_pages.sync(self.db, 'trip', [trip()], AT)
        rows = self.rows()
        self.db.execute('UPDATE note_pages SET removed_at=? WHERE id IN (?,?)', (AT, rows['Lisbon']['id'], rows['Trips']['id']))
        note_pages.sync(self.db, 'trip', [trip(), trip(key='porto', title='Porto')], LATER)
        self.assertEqual([(name, r['parent_id']) for name, r in self.rows().items()], [('Porto', None)])  # it goes where Trips was

    def test_a_renamed_folder_is_still_where_trips_go(self):
        note_pages.sync(self.db, 'trip', [trip()], AT)
        trips = self.rows()['Trips']['id']
        self.db.execute("UPDATE note_pages SET owner_title='Journeys' WHERE id=?", (trips,))
        note_pages.sync(self.db, 'trip', [trip(), trip(key='porto', title='Porto')], LATER)
        rows = self.rows()
        self.assertNotIn('Trips', rows)
        self.assertEqual(rows['Porto']['parent_id'], trips)

    def test_a_merged_trips_lines_go_on_where_it_was_merged(self):
        note_pages.sync(self.db, 'trip', [trip(), trip(key='porto', title='Porto', lines=[])], AT)
        rows = self.rows()
        self.db.execute('UPDATE note_pages SET merged_into=?,removed_at=? WHERE id=?', (rows['Porto']['id'], AT, rows['Lisbon']['id']))
        note_pages.sync(self.db, 'trip', [trip()], LATER)
        self.assertEqual(len(note_pages.page(self.db, rows['Porto']['id'])['lines']), 2)

    def test_keep_false_deletes_a_trip_whose_source_is_gone_and_only_trips_and_events_sync(self):
        note_pages.sync(self.db, 'trip', [trip(), trip(key='porto', title='Porto')], AT)
        note_pages.sync(self.db, 'trip', [trip()], LATER, keep=lambda key: key != 'porto')
        self.assertNotIn('Porto', self.rows())
        for kind in ('note', 'topic', 'home'):
            with self.assertRaises(ValueError):
                note_pages.sync(self.db, kind, [], AT)
        with self.assertRaises(OwnerError):
            note_pages.sync(self.db, 'trip', [trip(starts='2026-12-05', ends='2026-12-01')], AT)

    def test_the_notes_kept_from_before_show_nowhere_and_their_tables_stay(self):
        note_pages.sync(self.db, 'trip', [trip()], AT)
        kept = self.db.execute("INSERT INTO note_pages(kind,key,title,area,starts,ends,by,created_at,updated_at) "
                               "VALUES('topic','topic:kitchen','Kitchen','personal','2026-12-01','2026-12-31','machine',?,?)", (AT, AT)).lastrowid
        self.assertEqual([x['name'] for x in note_pages.dated(self.db, '2026-12-01', '2026-12-31')], ['Lisbon'])
        with self.assertRaises(ValueError):
            note_pages.page(self.db, kept)
        tables = {r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertLessEqual({'topic_routes', 'topic_aliases', 'topic_state', 'section_topics', 'section_state', 'note_writeups',
                              'folder_overviews', 'memory_seed_pages', 'memory_seed_state'}, tables)


class NotesAppTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [HOME]}
        pin = pinned(AT)
        pin.__enter__()
        self.addCleanup(pin.__exit__, None, None, None)
        with self.store.connect() as db:
            event = db.execute('INSERT INTO events(account_id,source_id,kind,title,body,occurred_at,metadata,content_hash,ingested_at) VALUES(?,?,?,?,?,?,?,?,?)',
                               ('home', 'e1', 'gmail.message', 'Flight to Lisbon', 'Flight to Lisbon', AT,
                                json.dumps({'from': 'Example Air <desk@example.com>'}), 'h1', AT)).lastrowid
            note_pages.sync(db, 'trip', [{'key': 'lisbon', 'title': 'Lisbon trip', 'area': 'personal', 'starts': '2026-11-20', 'ends': '2026-11-23',
                                          'under': ['Trips'], 'lines': [{'key': 'b1', 'text': 'Flight to Lisbon', 'event_id': event}]}], AT)
            self.trip = db.execute("SELECT id FROM note_pages WHERE kind='trip'").fetchone()['id']
            self.trips = db.execute("SELECT id FROM note_pages WHERE key='folder:trips'").fetchone()['id']

    def test_no_note_actions_and_no_notes_steps(self):
        self.assertEqual({n for n in machine_main.App.ACTIONS if n.startswith('note_')}, set())
        self.assertEqual({n for n in actions.DASHBOARD_ACTIONS | actions.OWNER_ACTIONS if n.startswith('note_')}, set())
        for name in ('notes_on', 'notes_list', 'note_action', 'topic_notes_step', 'note_writer_step', 'folder_overview_step', 'memory_seed_step'):
            self.assertFalse(hasattr(machine_main.App, name), name)

    def test_a_trip_shows_in_calendar_and_opens_from_there(self):
        bands = self.app.calendar_notes('2026-11-16T00:00:00+00:00', '2026-11-30T00:00:00+00:00')
        self.assertEqual([b['name'] for b in bands], ['Lisbon trip'])
        page = self.app.note_page(note_pages.node_id(self.trip))
        self.assertEqual([(x['text'], x['source']['from']) for x in page['lines']], [('Flight to Lisbon', 'Example Air')])
        self.assertIsInstance(page['areas'], list)
        self.assertNotIn('tree', page)
        with self.assertRaises(ValueError):  # its folder is no page of its own any more
            self.app.note_page(note_pages.node_id(self.trips))


if __name__ == '__main__':
    unittest.main()
