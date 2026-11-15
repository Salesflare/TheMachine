"""Notes in the Graph (note_pages.py, note_pages_app.py): the tree, links and Linked from, the owner's edits and how
The Machine's own notes keep them (sync), merges and Undo, and a line from a fact that edits the fact."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
import machine.main as machine_main

import note_pages  # noqa: E402
from machine import actions  # noqa: E402
from machine.owner_error import OwnerError  # noqa: E402

AT = '2026-11-14T10:00:00+00:00'
LATER = '2026-11-15T10:00:00+00:00'


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

    def new(self, title, parent=None, lines=()):
        return note_pages.create(self.db, title, None, AT, (), lines, parent=parent)['id']

    def test_the_tree_lists_each_note_after_the_one_it_is_under(self):
        home = self.new('Home')
        appliances = self.new('Appliances', parent=home)
        fridge = self.new('Fridge', parent=appliances, lines=['Bought in 2024, two years warranty'])
        self.new('Recipes')
        rows = note_pages.listing(self.db, '2026-11-14')
        order = [(x['name'], x['depth'], x['children']) for x in rows]
        self.assertLess(order.index(('Home', 0, 1)), order.index(('Appliances', 1, 1)))
        self.assertLess(order.index(('Appliances', 1, 1)), order.index(('Fridge', 2, 0)))
        page = note_pages.page(self.db, fridge)
        self.assertEqual([p['name'] for p in page['path']], ['Home', 'Appliances'])
        self.assertEqual(page['parent'], appliances)
        self.assertEqual(note_pages.count(self.db), 4)

    def test_the_path_shows_folders_as_the_owner_renamed_them(self):
        folder = note_pages._folder(self.db, ['Kids', 'Doctors and care'], AT)
        kids = self.db.execute('SELECT parent_id FROM note_pages WHERE id=?', (folder,)).fetchone()['parent_id']
        note_pages.edit(self.db, note_pages.node_id(kids), LATER, title='Children')
        note_pages.edit(self.db, note_pages.node_id(folder), LATER, title='Care')
        dentist = self.new('Dentist', parent=note_pages.node_id(folder))
        self.assertEqual([p['name'] for p in note_pages.page(self.db, dentist)['path']], ['Children', 'Care'])

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
        found = note_pages.find(self.db, 'lisbon')
        self.assertEqual([x['name'] for x in found], ['Lisbon'])
        self.assertIn('ABC123', note_pages.page(self.db, found[0]['id'])['lines'][0]['text'])

    def test_a_note_never_goes_under_itself_or_one_under_it(self):
        home = self.new('Home')
        appliances = self.new('Appliances', parent=home)
        with self.assertRaises(OwnerError):
            note_pages.edit(self.db, home, AT, parent=appliances)
        with self.assertRaises(OwnerError):
            note_pages.edit(self.db, home, AT, parent=home)
        note_pages.edit(self.db, appliances, AT, parent='')
        self.assertIsNone(note_pages.page(self.db, appliances)['parent'])

    def test_a_deleted_parent_leaves_its_notes_at_the_top_until_undo(self):
        home = self.new('Home')
        fridge = self.new('Fridge', parent=home)
        note_pages.remove(self.db, home, AT)
        self.assertEqual([(x['id'], x['depth']) for x in note_pages.listing(self.db, '2026-11-14')], [(fridge, 0)])
        note_pages.restore(self.db, home, LATER)
        self.assertEqual([x['id'] for x in note_pages.listing(self.db, '2026-11-14')], [home, fridge])

    def test_links_keep_only_names_in_the_words_and_show_as_linked_from(self):
        car = self.new('Car')
        trip_note = self.new('Weekend away')
        self.db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('person:robin@example.com','person','Robin Example',1,1,'{}')")
        note_pages.line_add(self.db, trip_note, 'Robin Example drives, the Car needs a check first', AT,
                            links=[{'id': car, 'name': 'Car'}, {'id': 'person:robin@example.com', 'name': 'Robin Example'},
                                   {'id': 'person:nobody@example.com', 'name': 'Nobody'}, {'id': trip_note, 'name': 'Weekend away'}])
        line = note_pages.page(self.db, trip_note)['lines'][0]
        self.assertEqual({x['id'] for x in line['links']}, {car, 'person:robin@example.com'})
        self.assertEqual([x['id'] for x in note_pages.linked_from(self.db, car)], [trip_note])
        self.assertEqual([x['id'] for x in note_pages.linked_from(self.db, 'person:robin@example.com')], [trip_note])
        note_pages.line_edit(self.db, line['id'], 'Robin Example drives', LATER)  # Car is no longer in the words
        self.assertEqual(note_pages.linked_from(self.db, car), [])
        note_pages.line_remove(self.db, line['id'], LATER)
        self.assertEqual(note_pages.linked_from(self.db, 'person:robin@example.com'), [])
        self.assertEqual(note_pages.page(self.db, car)['linked_from'], [])

    def test_sync_places_a_trip_under_trips_and_keeps_the_owners_changes(self):
        note_pages.sync(self.db, 'trip', [trip()], AT)
        rows = {x['name']: x for x in note_pages.listing(self.db, '2026-11-14')}
        self.assertEqual(rows['Lisbon']['parent'], rows['Trips']['id'])
        self.assertEqual((rows['Lisbon']['starts'], rows['Lisbon']['ends']), ('2026-12-03', '2026-12-06'))
        lisbon = rows['Lisbon']['id']
        page = note_pages.page(self.db, lisbon)
        flight, hotel = page['lines']
        note_pages.edit(self.db, lisbon, AT, title='Lisbon with the team', ends='2026-12-07', starts='2026-12-03')
        note_pages.line_edit(self.db, flight['id'], 'Flight TP 643, seat 12A, booking ABC123', AT)
        note_pages.line_remove(self.db, hotel['id'], AT)
        mine = note_pages.line_add(self.db, lisbon, 'Bring the adapter', AT)['lines'][0]
        work = self.new('Work')
        note_pages.edit(self.db, lisbon, AT, parent=work)
        # the bookings change: a later sync never undoes what the owner did
        note_pages.sync(self.db, 'trip', [trip(title='Lisbon trip', ends='2026-12-08', lines=[
            {'key': 'flight-out', 'text': 'Flight TP 645 Brussels to Lisbon, booking ABC123'},
            {'key': 'hotel', 'text': 'Hotel Rua Augusta, 4 nights'},
            {'key': 'train', 'text': 'Train to Sintra'}])], LATER)
        page = note_pages.page(self.db, lisbon)
        self.assertEqual((page['name'], page['ends'], page['parent']), ('Lisbon with the team', '2026-12-07', work))
        texts = [x['text'] for x in page['lines']]
        self.assertEqual(texts, ['Flight TP 643, seat 12A, booking ABC123', 'Train to Sintra', 'Bring the adapter'])
        self.assertTrue(page['lines'][0]['edited'])
        note_pages.line_reset(self.db, page['lines'][0]['id'], LATER)
        self.assertEqual(note_pages.page(self.db, lisbon)['lines'][0]['text'], 'Flight TP 645 Brussels to Lisbon, booking ABC123')
        self.assertIn(mine, [x['id'] for x in note_pages.page(self.db, lisbon)['lines']])

    def test_a_deleted_note_or_folder_stays_deleted(self):
        note_pages.sync(self.db, 'trip', [trip()], AT)
        rows = {x['name']: x['id'] for x in note_pages.listing(self.db, '2026-11-14')}
        note_pages.remove(self.db, rows['Lisbon'], AT)
        note_pages.remove(self.db, rows['Trips'], AT)
        note_pages.sync(self.db, 'trip', [trip(), trip(key='porto', title='Porto')], LATER)
        names = [(x['name'], x['parent']) for x in note_pages.listing(self.db, '2026-11-14')]
        self.assertEqual(names, [('Porto', None)])  # no Lisbon again, no second Trips: it goes where Trips was

    def test_a_renamed_or_moved_folder_is_where_later_notes_go(self):
        note_pages.sync(self.db, 'trip', [trip()], AT)
        rows = {x['name']: x['id'] for x in note_pages.listing(self.db, '2026-11-14')}
        travel = self.new('Travel')
        note_pages.edit(self.db, rows['Trips'], AT, title='Journeys', parent=travel)
        note_pages.sync(self.db, 'trip', [trip(), trip(key='porto', title='Porto')], LATER)
        rows2 = {x['name']: x for x in note_pages.listing(self.db, '2026-11-14')}
        self.assertNotIn('Trips', rows2)
        self.assertEqual(rows2['Porto']['parent'], rows['Trips'])
        self.assertEqual(rows2['Journeys']['parent'], travel)

    def test_merge_moves_lines_and_children_and_later_syncs_follow_and_undo_brings_it_back(self):
        note_pages.sync(self.db, 'trip', [trip()], AT)
        lisbon = {x['name']: x['id'] for x in note_pages.listing(self.db, '2026-11-14')}['Lisbon']
        portugal = self.new('Portugal', lines=['Learn some Portuguese'])
        sub = self.new('Restaurants', parent=lisbon)
        car = self.new('Car')
        note_pages.line_add(self.db, car, 'Rent one in Lisbon', AT, links=[{'id': lisbon, 'name': 'Lisbon'}])
        r = note_pages.merge(self.db, lisbon, portugal, AT)
        self.assertEqual(r['id'], portugal)
        page = note_pages.page(self.db, portugal)
        self.assertEqual(len(page['lines']), 3)
        self.assertEqual([x['id'] for x in page['children']], [sub])
        self.assertEqual([x['id'] for x in note_pages.linked_from(self.db, portugal)], [car])
        with self.assertRaises(OwnerError):
            note_pages.page(self.db, lisbon)
        note_pages.sync(self.db, 'trip', [trip(lines=[{'key': 'flight-out', 'text': 'Flight TP 643, now at 08:00'},
                                                      {'key': 'hotel', 'text': 'Hotel Rua Augusta, 3 nights'}])], LATER)
        texts = [x['text'] for x in note_pages.page(self.db, portugal)['lines']]
        self.assertIn('Flight TP 643, now at 08:00', texts)
        self.assertEqual(len(texts), 3)
        self.assertEqual(len([x for x in note_pages.listing(self.db, '2026-11-14') if x['name'] == 'Lisbon']), 0)
        note_pages.unmerge(self.db, lisbon, LATER)
        self.assertEqual(len(note_pages.page(self.db, lisbon)['lines']), 2)
        self.assertEqual([x['id'] for x in note_pages.page(self.db, lisbon)['children']], [sub])
        self.assertEqual([x['text'] for x in note_pages.page(self.db, portugal)['lines']], ['Learn some Portuguese'])

    def test_keep_false_deletes_a_machine_note_whose_source_is_gone(self):
        note_pages.sync(self.db, 'trip', [trip(), trip(key='porto', title='Porto')], AT)
        note_pages.sync(self.db, 'trip', [trip()], LATER, keep=lambda key: key != 'porto')
        self.assertNotIn('Porto', [x['name'] for x in note_pages.listing(self.db, '2026-11-14')])
        with self.assertRaises(ValueError):
            note_pages.sync(self.db, 'note', [], AT)

    def test_the_owner_starts_notes_only_of_their_own_kind_and_with_sane_input(self):
        with self.assertRaises(ValueError):
            note_pages.create(self.db, 'A trip', None, AT, kind='trip')
        with self.assertRaises(OwnerError):
            note_pages.create(self.db, '   ', None, AT)
        with self.assertRaises(OwnerError):
            note_pages.create(self.db, 'x' * 121, None, AT)
        with self.assertRaises(OwnerError):
            note_pages.create(self.db, 'Dates', None, AT, starts='2026-12-05', ends='2026-12-01')
        with self.assertRaises(ValueError):
            note_pages.create(self.db, 'Area', 'work:Elsewhere', AT, areas=['personal'])
        note = self.new('Garden')
        with self.assertRaises(OwnerError):
            note_pages.line_add(self.db, note, '   ', AT)
        self.assertEqual([x['name'] for x in note_pages.find(self.db, 'gard')], ['Garden'])
        self.assertEqual(note_pages.dated(self.db, '2026-12-01', '2026-12-31'), [])


class NotesAppTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'home', 'email': 'sam@example.com'}]}

    def test_the_actions_are_the_owners_from_their_dashboard(self):
        self.assertLessEqual(set(machine_main.App.ACTIONS) & {n for n in machine_main.App.ACTIONS if n.startswith('note_')}, actions.OWNER_ACTIONS)
        self.assertTrue({'note_new', 'note_line_edit', 'note_merge'} <= actions.DASHBOARD_ACTIONS)
        with self.assertRaises(ValueError):
            self.app.note_action('note_new', {'title': 'Garden'}, owner_dashboard=False)

    def test_editing_a_line_from_a_fact_edits_the_fact(self):
        with self.store.connect() as db:
            fact = db.execute("INSERT INTO facts(text,decision_id,created_at,kind) VALUES('The passport runs out in March 2027','owner:graph',?,'fact')",
                              (AT,)).lastrowid
            note_pages.sync(db, 'trip', [trip(lines=[{'key': 'passport', 'text': 'The passport runs out in March 2027', 'fact_id': fact}])], AT)
            line = db.execute('SELECT id FROM note_page_lines WHERE fact_id=?', (fact,)).fetchone()['id']
        r = self.app.note_action('note_line_edit', {'line': line, 'text': 'The passport runs out in May 2027'}, owner_dashboard=True)
        self.assertEqual(r['fact_id'], fact)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT text FROM facts WHERE id=?', (fact,)).fetchone()['text'], 'The passport runs out in May 2027')
        with self.assertRaises(OwnerError):  # what a fact can't hold, the line doesn't take either
            self.app.note_action('note_line_edit', {'line': line, 'text': 'x'}, owner_dashboard=True)

    def test_a_new_note_and_its_page(self):
        made = self.app.note_action('note_new', {'title': 'Garden', 'lines': ['Water the roses']}, owner_dashboard=True)
        page = self.app.note_page(made['id'])
        self.assertEqual((page['name'], [x['text'] for x in page['lines']]), ('Garden', ['Water the roses']))
        self.assertEqual([x['id'] for x in page['tree']], [made['id']])
        self.assertIsInstance(page['areas'], list)
