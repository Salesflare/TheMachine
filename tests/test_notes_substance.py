"""Notes in sections show only with substance (section_notes.drafts, USEFUL; note_pages.drop_empty_folder): a kind
shows once its parts hold two lines that say something, never for dates from the calendar alone, and the folder note
The Machine made for it goes when its parts do. Made-up data only; the model is a stand-in, nothing is sent."""
import json
import tempfile
import unittest
from pathlib import Path
import machine.main as machine_main

import health_notes  # noqa: E402
import note_pages  # noqa: E402
import section_notes  # noqa: E402
from pinned import pinned  # noqa: E402

HOME = {'id': 'home', 'email': 'sam@example.com', 'boundary': 'personal'}
AT = '2026-11-14T10:00:00+00:00'
DATES = [{'key': 'appt:a', 'item': 'appointment', 'text': 'Dentist check-up: coming up', 'at': '2026-12-02'},
         {'key': 'appt:b', 'item': 'appointment', 'text': 'GP visit: last time', 'at': '2026-10-20'},
         {'key': 'appt:c', 'item': 'appointment', 'text': 'Physio: coming up', 'at': '2026-11-20'}]


class NotesSubstance(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [HOME], 'notes_enabled': True}
        self.places = {}
        self.app.section_notes_model = self.model
        pin = pinned(AT)
        pin.__enter__()
        self.addCleanup(pin.__exit__, None, None, None)

    def model(self, prompt):
        lines = prompt.split('<<<\n', 1)[1].split('\n>>>', 1)[0].splitlines()
        out = []
        for line in lines:
            item = json.loads(line)
            said = item.get('from') or item.get('name') or item.get('text')
            out.append({'n': item['n'], 'section': next((s for k, s in self.places.items() if k in said), '')})
        return json.dumps({'places': out})

    def fact(self, text):
        with self.store.connect() as db:
            return db.execute("INSERT INTO facts(text,decision_id,created_at,kind) VALUES(?,'owner:chat',?,'fact')", (text, AT)).lastrowid

    def names(self):
        with self.store.connect() as db:
            return sorted(x['name'] for x in note_pages.listing(db, '2026-11-14'))

    def before(self, lines):
        """A Health part as an earlier round left it, under the Health folder The Machine made."""
        with self.store.connect() as db:
            section_notes.ensure(db)
            note_pages.sync(db, 'health', [{'key': 'appointments', 'title': 'Appointments', 'under': ['Health'], 'lines': lines}], AT)

    def round(self):
        with self.store.connect() as db:
            db.execute('DELETE FROM section_state')
        self.app.section_notes_run(health_notes.KIND)

    def test_dates_alone_are_no_substance_and_the_folder_goes_with_its_parts(self):
        self.before(DATES)
        self.assertEqual(self.names(), ['Appointments', 'Health'])
        with self.store.connect() as db:
            found, _ = section_notes.drafts(db, health_notes.KIND, [])
        self.assertEqual(found, [])
        self.round()
        self.assertEqual(self.names(), [], 'no empty Health folder left behind')

    def test_one_useful_line_is_not_enough_and_two_are(self):
        self.places = {'penicillin': 'Allergies and conditions', 'hay fever': 'Allergies and conditions'}
        self.fact('Allergic to penicillin')
        self.round()
        self.assertEqual(self.names(), [])
        self.fact('Has hay fever every spring')
        self.round()
        self.assertEqual(self.names(), ['Allergies and conditions', 'Health'])

    def test_two_parts_with_one_line_each_show_nothing(self):
        self.places = {'penicillin': 'Allergies and conditions', 'ibuprofen': 'Medicines'}
        self.fact('Allergic to penicillin')
        self.fact('Takes ibuprofen for back pain')
        self.round()
        self.assertEqual(self.names(), [])

    def test_what_the_owner_keeps_stays(self):
        self.before(DATES)
        with self.store.connect() as db:
            part = db.execute("SELECT id FROM note_pages WHERE key='health:appointments'").fetchone()['id']
        self.app.note_action('note_line_add', {'id': part, 'text': 'Dentist: every six months'}, owner_dashboard=True)
        self.round()
        self.assertEqual(self.names(), ['Appointments', 'Health'], 'their own line keeps the part and its folder')

    def test_a_folder_the_owner_renamed_or_filled_stays(self):
        with self.store.connect() as db:
            note_pages.ensure(db)
            folder = note_pages._folder(db, ['Health'], AT)
            note_pages.edit(db, folder, AT, title='My health')
            self.assertIsNone(note_pages.drop_empty_folder(db, ['Health']))
            other = note_pages._folder(db, ['Kids'], AT)
            note_pages.line_add(db, other, 'Pick-up at 15:30', AT)
            self.assertIsNone(note_pages.drop_empty_folder(db, ['Kids']))
            empty = note_pages._folder(db, ['Home'], AT)
            self.assertEqual(note_pages.drop_empty_folder(db, ['Home']), note_pages.node_id(empty))


if __name__ == '__main__':
    unittest.main()
