"""Kids notes (kids_notes.py, section_notes.py, NotesApp.section_notes_run): what was learned about the owner's children
and their bills, from any area (never a calendar event alone), placed under Kids by one small model call over what is new only, a
child's lines in the owner's own note for that child. Kids is always Personal. Made-up data only; the model is a
stand-in, nothing is sent."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('kids_notes_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import kids_notes  # noqa: E402
import note_pages  # noqa: E402
import section_notes  # noqa: E402
from pinned import pinned  # noqa: E402

HOME = {'id': 'home', 'email': 'sam@example.com', 'boundary': 'personal'}
JOB = {'id': 'job', 'email': 'sam@acme.example', 'boundary': 'work:Acme'}
AT = '2026-11-14T10:00:00+00:00'


class KidsNotes(unittest.TestCase):
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
            section, _, note = next((s for k, s in self.places.items() if k in said), '').partition('/')  # 'School/Jules'
            out.append({'n': item['n'], 'section': section, **({'note': note} if note else {})})
        return json.dumps({'places': out})

    def person(self, name, role):
        node = 'person:' + name.split()[0].casefold()
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person',?,1,1,?)", (node, name, json.dumps({'role': role})))
        return node

    def fact(self, text, about=None):
        with self.store.connect() as db:
            fact = db.execute("INSERT INTO facts(text,decision_id,created_at,kind) VALUES(?,'owner:chat',?,'fact')", (text, AT)).lastrowid
            if about:
                db.execute("INSERT INTO fact_about(fact_id,node_id,by,created_at) VALUES(?,?,'machine',?)", (fact, about, AT))
        return fact

    def event(self, title, day, account='home'):
        self.n += 1
        with self.store.connect() as db:
            return db.execute('INSERT INTO events(account_id,source_id,kind,title,body,occurred_at,metadata,content_hash,ingested_at) '
                              "VALUES(?,?,'calendar.event',?,'',?,'{}',?,?)", (account, f'cal{self.n}', title, f'{day}T17:00:00+00:00', f'h{self.n}', AT)).lastrowid

    def bill(self, payee, day, account='home'):
        self.n += 1
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at,bill) VALUES(?,?,?,?,?,?,?,?)",
                       (f's{self.n}', f'd{self.n}', 'Pay the fees', 'IBAN BE00 0000 0000 0000', json.dumps([1000 + self.n]), json.dumps([account]),
                        f'2026-{day}T09:00:00+00:00', json.dumps({'payee': payee, 'invoice': f'INV-{self.n}', 'amount': 'EUR 120,00'})))
        return f's{self.n}'

    def run_round(self):
        with self.store.connect() as db:
            db.execute('DELETE FROM section_state')
        self.app.section_notes_run(kids_notes.KIND)
        with self.store.connect() as db:
            return {x['name']: note_pages.page(db, x['id']) for x in note_pages.listing(db, '2026-11-14') if x['kind'] == 'kids'}

    def test_a_child_is_someone_whose_role_says_so(self):
        for name, role in (('Jules Morgan', 'daughter'), ('Remy Morgan', 'my son'), ('Lou Morgan', 'Zoon'), ('Ana Lee', "Jules's teacher"),
                           ('Bo Hart', 'child psychologist'), ('Cy Dunn', 'friend'), ('Di Fox', '')):
            self.person(name, role)
        with self.store.connect() as db:
            self.assertEqual(sorted(section_notes.children(db).values()), ['Jules Morgan', 'Lou Morgan', 'Remy Morgan'])

    def test_kids_sections_with_a_childs_facts_their_events_and_fees_from_any_area(self):
        jules = self.person('Jules Morgan', 'daughter')
        teacher = self.person('Ana Lee', 'teacher at Example Primary')
        self.places = {'class': 'School', 'Parents': 'School', 'Example Primary': 'Bills and fees', 'Example Swim': 'Bills and fees',
                       'swims': 'Activities', 'Lee': ''}
        self.fact('Jules is in class 4B this year', about=jules)
        self.fact('Jules swims on Wednesdays', about=jules)  # one line: no Activities yet
        self.fact('Ms Lee prefers mail to calls', about=teacher)  # about someone who is not a child: their page
        self.fact('Parents evening for class 4B is on 26 November')
        self.event('Parents evening', '2026-11-26', account='job')  # a calendar event alone: never a line
        self.bill('Example Primary School', '09-05', account='job')
        self.bill('Example Swim Club', '10-02')
        notes = self.run_round()
        self.assertEqual(sorted(notes), ['Bills and fees', 'School'])
        school = notes['School']
        self.assertEqual([x['name'] for x in school['path']], ['Kids'])
        self.assertEqual({n['area'] for n in notes.values()}, {'personal'})
        self.assertCountEqual([x['text'] for x in school['lines']], ['Jules is in class 4B this year', 'Parents evening for class 4B is on 26 November'])
        self.assertNotIn('"kind": "calendar"', self.asked[0])
        line = next(x for x in school['lines'] if x['fact_id'])
        self.assertEqual(line['links'], [{'id': jules, 'name': 'Jules'}], 'links the child, as the line names them')
        prompt = self.asked[0]
        self.assertIn('"about": "Jules Morgan"', prompt)
        self.assertNotIn('Ms Lee', prompt)
        self.assertNotIn('120,00', prompt)
        page = self.app.note_page(notes['Bills and fees']['id'])
        self.assertEqual(sorted(x.get('todo') for x in page['lines']), ['s2', 's3'], 'a fee opens its to-do')

    def test_the_owners_note_for_one_child_gets_what_is_about_them(self):
        jules = self.person('Jules Morgan', 'daughter')
        remy = self.person('Remy Morgan', 'son')
        kids = self.app.note_action('note_new', {'title': 'Kids'}, owner_dashboard=True)['id']
        school = self.app.note_action('note_new', {'title': 'School', 'parent': kids}, owner_dashboard=True)['id']
        mine = self.app.note_action('note_new', {'title': 'Jules', 'parent': school, 'lines': ['Pick-up at 15:30']}, owner_dashboard=True)['id']
        self.places = {'Jules': 'School/Jules', 'Remy': 'School', 'term': 'School'}
        self.fact('Jules is in class 4B this year', about=jules)
        self.fact('Remy starts at Example Primary in September', about=remy)
        self.fact('The autumn term ends on 18 December')
        self.run_round()
        self.assertIn('"School": ["Jules"]', self.asked[0])
        with self.store.connect() as db:
            under = note_pages.page(db, school)
            hers = note_pages.page(db, mine)
            names = sorted(x['name'] for x in note_pages.listing(db, '2026-11-14'))
        self.assertEqual(names, ['Jules', 'Kids', 'School'], 'no second Kids or School, no note started for Remy')
        self.assertCountEqual([x['text'] for x in under['lines']], ['Remy starts at Example Primary in September', 'The autumn term ends on 18 December'])
        self.assertCountEqual([x['text'] for x in hers['lines']], ['Pick-up at 15:30', 'Jules is in class 4B this year'])


if __name__ == '__main__':
    unittest.main()
