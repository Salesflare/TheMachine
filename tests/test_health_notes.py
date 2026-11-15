"""Health notes (health_notes.py, section_notes.py, NotesApp.section_notes_run): the owner's own appointments from
the calendar, care bills and what was learned, from any area, placed under Health by one small model call over what is
new only. Health is always Personal. Made-up data only; the model is a stand-in, nothing is sent."""
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

    def test_appointments_only_the_owner_goes_to_with_their_next_or_last_time(self):
        self.event('Dentist check-up', '2026-05-10')
        coming = self.event('Dentist check-up', '2026-12-02')
        self.event('Physio', '2026-10-01', attendees=['sam@example.com'])
        last = self.event('Physio', '2026-10-08', attendees=[{'email': 'sam@example.com', 'self': True, 'responseStatus': 'accepted'}])
        self.event('Eye test', '2026-09-20', account='job')  # on the work calendar: still the owner's own health
        self.event('Team sync', '2026-11-03', attendees=['ana@acme.example'])  # someone else on it: a meeting
        self.event('Dentist cleaning', '2026-11-20', status='cancelled')
        self.event('Blood test', '2026-11-21', attendees=[{'email': 'sam@example.com', 'self': True, 'responseStatus': 'declined'}])
        self.event('Old allergist visit', '2025-01-10')  # before EVENTS_BACK
        self.event('Room booking', '2026-10-15', attendees=[{'email': 'room@acme.example', 'resource': True}])
        with self.store.connect() as db:
            import timeutil
            found = {c['name']: c for c in section_notes.own_events(db, [HOME, JOB], timeutil.today())}
        self.assertEqual(sorted(found), ['Dentist check-up', 'Eye test', 'Physio', 'Room booking'])
        self.assertEqual((found['Dentist check-up']['at'], found['Dentist check-up']['coming'], found['Dentist check-up']['event_id']),
                         ('2026-12-02', True, coming))
        self.assertEqual((found['Physio']['at'], found['Physio']['coming'], found['Physio']['event_id'], found['Physio']['count']),
                         ('2026-10-08', False, last, 2))

    def test_health_sections_from_any_area_always_personal_with_their_sources(self):
        self.places = {'Dentist': 'Appointments', 'Eye test': 'Appointments', 'Example Dental': 'Bills and insurance',
                       'Example Pharmacy': 'Bills and insurance', 'penicillin': 'Allergies and conditions', 'hay fever': 'Allergies and conditions',
                       'Team': ''}
        self.event('Dentist check-up', '2026-12-02')
        self.event('Eye test', '2026-09-20', account='job')
        self.event('Team lunch', '2026-11-03')  # alone on it but not health: the model says ""
        dental = self.bill('Example Dental', '10-12')
        self.bill('Example Pharmacy', '09-01', account='job')  # a work address: Health is still Personal
        self.fact('Allergic to penicillin')
        self.fact('Has hay fever every spring')
        notes = self.run_round()
        self.assertEqual(sorted(notes), ['Allergies and conditions', 'Appointments', 'Bills and insurance'])
        appts = notes['Appointments']
        self.assertEqual([x['name'] for x in appts['path']], ['Health'])
        self.assertEqual({n['area'] for n in notes.values()}, {'personal'})
        self.assertCountEqual([(x['text'], x['at']) for x in appts['lines']],
                              [('Dentist check-up: coming up', '2026-12-02'), ('Eye test: last time', '2026-09-20')])
        bills = notes['Bills and insurance']
        self.assertCountEqual([x['text'] for x in bills['lines']],
                              ['Example Dental: one bill in the past year', 'Example Pharmacy: one bill in the past year'])
        page = self.app.note_page(bills['id'])
        self.assertIn(dental, [x.get('todo') for x in page['lines']], 'a bill\'s line opens its to-do')
        prompt = self.asked[0]
        self.assertNotIn('65,00', prompt)
        self.assertNotIn('IBAN', prompt)
        self.assertIn('"kind": "calendar"', prompt)

    def test_one_line_starts_no_part_and_the_owners_own_note_gets_what_is_about_it(self):
        health = self.app.note_action('note_new', {'title': 'Health'}, owner_dashboard=True)['id']
        appts = self.app.note_action('note_new', {'title': 'Appointments', 'parent': health}, owner_dashboard=True)['id']
        physio = self.app.note_action('note_new', {'title': 'Physio', 'parent': appts, 'lines': ['Exercises: twice a day']},
                                      owner_dashboard=True)['id']
        self.places = {'Physio': 'Appointments/Physio', 'Dentist': 'Appointments', 'GP': 'Appointments', 'ibuprofen': 'Medicines'}
        self.event('Physio', '2026-11-05')
        self.event('Dentist check-up', '2026-12-02')
        self.event('GP visit', '2026-10-20')
        self.fact('Takes ibuprofen for back pain')
        notes = self.run_round()
        self.assertIn('"Appointments": ["Physio"]', self.asked[0])
        self.assertNotIn('Medicines', notes, 'one line: no Medicines yet')
        self.assertEqual(notes['Appointments']['id'], appts)
        with self.store.connect() as db:
            under = note_pages.page(db, appts)
            mine = note_pages.page(db, physio)
            names = sorted(x['name'] for x in note_pages.listing(db, '2026-11-14'))
        self.assertEqual(names, ['Appointments', 'Health', 'Physio'])
        self.assertCountEqual([x['text'] for x in under['lines']], ['Dentist check-up: coming up', 'GP visit: last time'])
        self.assertCountEqual([x['text'] for x in mine['lines']], ['Exercises: twice a day', 'Physio: last time'])

    def test_a_calendar_line_names_no_sender(self):
        self.places = {'Dentist': 'Appointments', 'GP': 'Appointments'}
        self.event('Dentist check-up', '2026-12-02', organizer='front-desk@dental.example')
        self.event('GP visit', '2026-10-20')
        notes = self.run_round()
        page = self.app.note_page(notes['Appointments']['id'])
        self.assertEqual({x['source']['kind'] for x in page['lines']}, {'calendar.event'})
        self.assertFalse(any('from' in x['source'] for x in page['lines']))


if __name__ == '__main__':
    unittest.main()
