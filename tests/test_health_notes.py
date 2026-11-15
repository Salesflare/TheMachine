"""Health notes (health_notes.py, section_notes.py, NotesApp.section_notes_run): care bills and what was learned,
from any area, placed under Health by one small model call over what is new only; a calendar event is never a line.
Health is always Personal. Made-up data only; the model is a stand-in, nothing is sent."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('health_notes_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import health_notes  # noqa: E402
import note_pages  # noqa: E402
import section_notes  # noqa: E402
from pinned import pinned  # noqa: E402

HOME = {'id': 'home', 'email': 'sam@example.com', 'boundary': 'personal'}
JOB = {'id': 'job', 'email': 'sam@acme.example', 'boundary': 'work:Acme'}
AT = '2026-11-14T10:00:00+00:00'


class HealthNotes(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [HOME, JOB]}
        self.asked = []
        self.places = {}
        self.app.section_notes_model = self.model
        self.n = 0
        pin = pinned(AT)
        pin.__enter__()
        self.addCleanup(pin.__exit__, None, None, None)

    def model(self, prompt):
        self.asked.append(prompt)
        lines = prompt.split('<<<\n', 1)[1].split('\n>>>', 1)[0].splitlines()
        out = []
        for line in lines:
            item = json.loads(line)
            said = item.get('from') or item.get('name') or item.get('text')
            section, _, note = next((s for k, s in self.places.items() if k in said), '').partition('/')  # 'Appointments/Physio'
            out.append({'n': item['n'], 'section': section, **({'note': note} if note else {})})
        return json.dumps({'places': out})

    def event(self, title, day, account='home', **meta):
        self.n += 1
        with self.store.connect() as db:
            return db.execute('INSERT INTO events(account_id,source_id,kind,title,body,occurred_at,metadata,content_hash,ingested_at) '
                              "VALUES(?,?,'calendar.event',?,'',?,?,?,?)",
                              (account, f'cal{self.n}', title, f'{day}T09:00:00+00:00', json.dumps(meta), f'h{self.n}', AT)).lastrowid

    def bill(self, payee, day, account='home', amount='EUR 65,00'):
        self.n += 1
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at,bill) VALUES(?,?,?,?,?,?,?,?)",
                       (f's{self.n}', f'd{self.n}', 'Pay the bill', 'IBAN BE00 0000 0000 0000', json.dumps([1000 + self.n]), json.dumps([account]),
                        f'2026-{day}T09:00:00+00:00', json.dumps({'payee': payee, 'invoice': f'INV-{self.n}', 'amount': amount})))
        return f's{self.n}'

    def fact(self, text):
        with self.store.connect() as db:
            return db.execute("INSERT INTO facts(text,decision_id,created_at,kind) VALUES(?,'owner:chat',?,'fact')", (text, AT)).lastrowid

    def run_round(self):
        with self.store.connect() as db:
            db.execute('DELETE FROM section_state')
        self.app.section_notes_run(health_notes.KIND)
        with self.store.connect() as db:
            return {x['name']: note_pages.page(db, x['id']) for x in note_pages.listing(db, '2026-11-14') if x['kind'] == 'health'}

    def test_health_sections_from_any_area_always_personal_with_their_sources(self):
        self.places = {'Example Dental': 'Bills and insurance', 'Example Pharmacy': 'Bills and insurance',
                       'penicillin': 'Allergies and conditions', 'hay fever': 'Allergies and conditions'}
        dental = self.bill('Example Dental', '10-12')
        self.bill('Example Pharmacy', '09-01', account='job')  # a work address: Health is still Personal
        self.fact('Allergic to penicillin')
        self.fact('Has hay fever every spring')
        notes = self.run_round()
        self.assertEqual(sorted(notes), ['Allergies and conditions', 'Bills and insurance'])
        bills = notes['Bills and insurance']
        self.assertEqual([x['name'] for x in bills['path']], ['Health'])
        self.assertEqual({n['area'] for n in notes.values()}, {'personal'})
        self.assertCountEqual([x['text'] for x in bills['lines']],
                              ['Example Dental: one bill in the past year', 'Example Pharmacy: one bill in the past year'])
        page = self.app.note_page(bills['id'])
        self.assertIn(dental, [x.get('todo') for x in page['lines']], 'a bill\'s line opens its to-do')
        prompt = self.asked[0]
        self.assertNotIn('65,00', prompt)
        self.assertNotIn('IBAN', prompt)

    def test_a_calendar_event_is_never_a_line(self):
        self.places = {'Dentist': 'Appointments', 'GP': 'Appointments', 'Physio': 'Appointments'}
        self.event('Dentist check-up', '2026-12-02')
        self.event('GP visit', '2026-10-20', account='job')
        self.event('Physio', '2026-11-05', attendees=[{'email': 'sam@example.com', 'self': True}])
        notes = self.run_round()
        self.assertEqual(notes, {}, 'meetings and appointments alone start no note')
        self.assertFalse(self.asked, 'nothing to place: no model call')
        with self.store.connect() as db:
            self.assertEqual(note_pages.listing(db, '2026-11-14'), [])

    def test_appointment_lines_from_before_leave_the_notes(self):
        with self.store.connect() as db:  # what a round made before calendar events stopped being candidates
            section_notes.ensure(db)
            db.execute("INSERT INTO section_topics(kind,key,section,at) VALUES('health','appt:old1','Appointments',?)", (AT,))
            note_pages.sync(db, 'health', [{'key': 'appointments', 'title': 'Appointments', 'under': ['Health'], 'lines': [
                {'key': 'appt:old1', 'item': 'appointment', 'text': 'Dentist check-up: coming up', 'at': '2026-12-02'},
                {'key': 'appt:old2', 'item': 'appointment', 'text': 'GP visit: last time', 'at': '2026-10-20'}]}], AT)
        self.assertEqual(sorted(self.run_round()), [], 'the part with only appointments goes')
        with self.store.connect() as db:
            self.assertIsNone(db.execute("SELECT 1 FROM section_topics WHERE key LIKE 'appt:%'").fetchone())
            self.assertIsNone(db.execute("SELECT 1 FROM note_page_lines WHERE item='appointment'").fetchone())

    def test_one_line_starts_no_part_and_the_owners_own_note_gets_what_is_about_it(self):
        health = self.app.note_action('note_new', {'title': 'Health'}, owner_dashboard=True)['id']
        meds = self.app.note_action('note_new', {'title': 'Medicines', 'parent': health}, owner_dashboard=True)['id']
        inhaler = self.app.note_action('note_new', {'title': 'Inhaler', 'parent': meds, 'lines': ['Two puffs when needed']},
                                       owner_dashboard=True)['id']
        self.places = {'inhaler': 'Medicines/Inhaler', 'vitamin D': 'Medicines', 'magnesium': 'Medicines', 'penicillin': 'Allergies and conditions'}
        self.fact('Refills the inhaler every three months')
        self.fact('Takes vitamin D in winter')
        self.fact('Takes magnesium before sleep')
        self.fact('Allergic to penicillin')
        notes = self.run_round()
        self.assertIn('"Medicines": ["Inhaler"]', self.asked[0])
        self.assertNotIn('Allergies and conditions', notes, 'one line: no part yet')
        self.assertEqual(notes['Medicines']['id'], meds)
        with self.store.connect() as db:
            under = note_pages.page(db, meds)
            mine = note_pages.page(db, inhaler)
        self.assertCountEqual([x['text'] for x in under['lines']], ['Takes vitamin D in winter', 'Takes magnesium before sleep'])
        self.assertCountEqual([x['text'] for x in mine['lines']], ['Two puffs when needed', 'Refills the inhaler every three months'])


if __name__ == '__main__':
    unittest.main()
