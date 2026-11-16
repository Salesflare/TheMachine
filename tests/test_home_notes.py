"""Home notes (home_notes.py, section_notes.py, NotesApp.section_notes_run): regular Personal bills, subscriptions and what was learned,
placed under Home by one small model call over what is new only, each line pointing to its to-do, mail or fact instead
of copying it. Made-up data only; the model is a stand-in, nothing is sent."""
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock
import machine.main as machine_main

import home_notes  # noqa: E402
import section_notes  # noqa: E402
import note_pages  # noqa: E402
import subscriptions  # noqa: E402

HOME = {'id': 'home', 'email': 'sam@example.com', 'boundary': 'personal'}
JOB = {'id': 'job', 'email': 'sam@acme.example', 'boundary': 'work:Acme'}
AT = '2026-11-14T10:00:00+00:00'


class HomeNotes(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [HOME, JOB], 'notes_enabled': True}
        self.asked = []
        self.places = {}
        self.app.section_notes_model = self.model
        self.n = 0

    def model(self, prompt):
        self.asked.append(prompt)
        lines = prompt.split('<<<\n', 1)[1].split('\n>>>', 1)[0].splitlines()
        out = []
        for line in lines:
            item = json.loads(line)
            said = item.get('from') or item.get('name') or item.get('text')
            section, _, note = next((s for k, s in self.places.items() if k in said), '').partition('/')  # 'Appliances/Dishwasher'
            out.append({'n': item['n'], 'section': section, **({'note': note} if note else {})})
        return json.dumps({'places': out})

    def bill(self, payee, day, account='home', amount='EUR 84,20'):
        self.n += 1
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at,bill) VALUES(?,?,?,?,?,?,?,?)",
                       (f's{self.n}', f'd{self.n}', 'Pay the bill', 'IBAN BE00 0000 0000 0000', json.dumps([1000 + self.n]), json.dumps([account]),
                        f'2026-{day}T09:00:00+00:00', json.dumps({'payee': payee, 'invoice': f'INV-{self.n}', 'amount': amount})))
        return f's{self.n}'

    def fact(self, text, about=None):
        with self.store.connect() as db:
            fact = db.execute("INSERT INTO facts(text,decision_id,created_at,kind) VALUES(?,'owner:chat',?,'fact')", (text, AT)).lastrowid
            if about:
                db.execute("INSERT INTO fact_about(fact_id,node_id,by,created_at) VALUES(?,?,'machine',?)", (fact, about, AT))
        return fact

    def run_round(self):
        with self.store.connect() as db:
            db.execute('DELETE FROM section_state')
        self.app.section_notes_run(home_notes.KIND)
        with self.store.connect() as db:
            return {x['name']: note_pages.page(db, x['id']) for x in note_pages.listing(db, '2026-11-14') if x['kind'] == 'home'}

    def test_regular_personal_bills_and_facts_make_sections_under_home_that_point_to_their_to_do(self):
        self.places = {'Example Energy': 'Bills and subscriptions', 'Example Water': 'Bills and subscriptions', 'dishwasher': 'Appliances',
                       'fridge': 'Appliances', 'Lisbon': ''}
        self.bill('Example Energy', '09-03')
        last = self.bill('Example Energy', '10-03')
        self.bill('Example Water', '05-10')
        self.bill('Example Water', '08-10')
        self.bill('Example Gym', '10-01')  # once: not a regular bill
        self.bill('Example Office Rent', '09-01', account='job')
        self.bill('Example Office Rent', '10-01', account='job')  # Work: never on Home
        washer = self.fact('The dishwasher is a Example DW-500, bought in March 2024')
        self.fact('The fridge warranty runs until June 2027')
        self.fact('Prefers a window seat to Lisbon')
        self.fact('Sam\'s dishwasher at the office leaks', about='person:sam')  # about someone: their page
        notes = self.run_round()
        self.assertEqual(sorted(notes), ['Appliances', 'Bills and subscriptions'])
        bills = notes['Bills and subscriptions']
        self.assertEqual([x['name'] for x in bills['path']], ['Home'])
        self.assertEqual(bills['area'], 'personal')
        texts = [x['text'] for x in bills['lines']]
        self.assertEqual(texts, ['Example Energy: a bill every month', 'Example Water: a bill every three months'])
        self.assertEqual([x['at'] for x in bills['lines']], ['2026-10-03', '2026-08-10'], 'the day of the last one')
        self.assertFalse(any('84' in x or 'IBAN' in x or 'INV' in x for x in texts), 'the amount and payment details stay on the to-do')
        self.assertEqual(bills['lines'][0]['data'], {'todo': last})
        self.assertEqual(self.app.note_page(bills['id'])['lines'][0]['todo'], last)
        appliances = notes['Appliances']
        self.assertEqual([x['fact_id'] for x in appliances['lines']][0], washer)
        prompt = self.asked[0]
        self.assertNotIn('Example Gym', prompt)
        self.assertNotIn('Office Rent', prompt)
        self.assertNotIn('at the office', prompt)
        self.assertNotIn('84,20', prompt)

    def test_a_due_round_is_not_starved_by_background_work_that_runs_more_often(self):
        """The step comes round every ten minutes, and the space between background turns is ten minutes too: reviews
        and drafts ahead took it every time and no round ever came. After SPACED_WAIT_SECONDS it goes anyway, but never
        while the budget holds background work."""
        import note_pages_app
        self.places = {'Example Energy': 'Bills and subscriptions'}
        self.bill('Example Energy', '09-02')
        self.bill('Example Energy', '10-02')
        clock = [10000.0]
        self.app.background_pause = lambda **_: None
        self.app.background_at = time.time()  # another background turn just went, and keeps going
        started = []
        self.app.background_started = lambda: started.append(clock[0])
        with mock.patch.object(note_pages_app, 'monotonic', lambda: clock[0]):
            for _ in range(5):  # rounds every ten minutes while other work keeps taking the space
                self.assertFalse(self.app.section_notes_step())
                clock[0] += 600
            clock[0] += note_pages_app.SPACED_WAIT_SECONDS
            self.assertTrue(self.app.section_notes_step())
            self.app.section_notes_thread.join(10)
            self.assertEqual(started, [clock[0]])
            with self.store.connect() as db:
                self.assertEqual([r[0] for r in db.execute('SELECT kind FROM section_state ORDER BY kind')], ['health', 'home', 'kids'])
            self.assertFalse(self.app.section_notes_step())  # not due again for six hours
            with self.store.connect() as db:
                db.execute('DELETE FROM section_state')
            self.bill('Example Water', '10-05')
            self.bill('Example Water', '11-05')  # something new to ask about
            self.app.background_pause = lambda **_: {'window': 'memory', 'until': None}
            clock[0] += 10 * note_pages_app.SPACED_WAIT_SECONDS
            self.assertFalse(self.app.section_notes_step())  # the budget or a quiet window always holds it
            self.app.background_pause = lambda **_: None
            self.assertFalse(self.app.section_notes_step())  # and the wait for space starts over after a round

    def test_each_candidate_is_asked_about_once(self):
        self.places = {'Example Energy': 'Bills and subscriptions', 'Example Water': 'Bills and subscriptions'}
        for day in ('09-03', '10-03'):
            self.bill('Example Energy', day)
        self.run_round()
        self.assertEqual(len(self.asked), 1)
        self.run_round()
        self.assertEqual(len(self.asked), 1, 'nothing new: no model call')
        for day in ('09-10', '10-10'):
            self.bill('Example Water', day)
        notes = self.run_round()
        self.assertEqual(len(self.asked), 2)
        self.assertNotIn('Example Energy', self.asked[1])
        self.assertEqual(len(notes['Bills and subscriptions']['lines']), 2)

    def test_an_answer_that_isnt_one_keeps_nothing_and_asks_again(self):
        for day in ('09-03', '10-03'):
            self.bill('Example Energy', day)
        self.app.section_notes_model = lambda prompt: self.asked.append(prompt) or 'Sorry, I can\'t help with that.'
        self.assertEqual(self.run_round(), {})
        self.app.section_notes_model = self.model
        self.places = {'Example Energy': 'Bills and subscriptions'}
        self.run_round()
        self.assertEqual(len(self.asked), 2)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT section FROM section_topics WHERE kind='home'").fetchone()['section'], 'Bills and subscriptions')

    def test_one_line_starts_no_section_and_a_section_goes_with_its_last_line_unless_the_owner_wrote_in_it(self):
        self.places = {'dishwasher': 'Appliances', 'fridge': 'Appliances', 'boiler': 'Repairs and upkeep', 'gutters': 'Repairs and upkeep'}
        washer = self.fact('The dishwasher is a Example DW-500')
        fridge = self.fact('The fridge warranty runs until June 2027')
        self.fact('The boiler is serviced every October by Example Heating')
        notes = self.run_round()
        self.assertEqual(sorted(notes), ['Appliances'], 'one line: no Repairs and upkeep yet')
        self.fact('The gutters are cleaned in November')
        notes = self.run_round()
        self.assertEqual(sorted(notes), ['Appliances', 'Repairs and upkeep'])
        self.app.note_action('note_line_add', {'id': notes['Repairs and upkeep']['id'], 'text': 'Ask about the roof too'}, owner_dashboard=True)
        with self.store.connect() as db:
            db.execute("UPDATE facts SET removed_at=? WHERE text LIKE '%boiler%' OR text LIKE '%gutters%' OR id IN (?,?)", (AT, washer, fridge))
        notes = self.run_round()
        self.assertEqual(sorted(notes), ['Repairs and upkeep'], 'Appliances had nothing left; the owner wrote in the other one')
        self.assertEqual([x['text'] for x in notes['Repairs and upkeep']['lines']], ['Ask about the roof too'])

    def test_the_owners_own_home_and_appliances_notes_are_filled_in_not_doubled(self):
        home = self.app.note_action('note_new', {'title': 'home'}, owner_dashboard=True)['id']
        mine = self.app.note_action('note_new', {'title': 'Appliances', 'parent': home, 'lines': ['Manuals are in the blue box']}, owner_dashboard=True)['id']
        self.app.note_action('note_new', {'title': 'Dishwasher', 'parent': mine}, owner_dashboard=True)
        self.places = {'dishwasher': 'Appliances', 'fridge': 'Appliances'}
        self.fact('The dishwasher is a Example DW-500')
        self.fact('The fridge warranty runs until June 2027')
        notes = self.run_round()
        with self.store.connect() as db:
            names = sorted(x['name'] for x in note_pages.listing(db, '2026-11-14'))
            page = note_pages.page(db, mine)
        self.assertEqual(names, ['Appliances', 'Dishwasher', 'home'], 'no second Home or Appliances')
        self.assertEqual(notes['Appliances']['id'], mine)
        self.assertCountEqual([x['text'] for x in page['lines']], ['The dishwasher is a Example DW-500', 'The fridge warranty runs until June 2027',
                                                                  'Manuals are in the blue box'])
        self.assertEqual((page['kind'], page['name']), ('home', 'Appliances'), 'now kept current, under their name')
        self.assertEqual([x['name'] for x in page['children']], ['Dishwasher'])
        with self.store.connect() as db:  # nothing left from the Machine: their note, line and Dishwasher stay
            db.execute('UPDATE facts SET removed_at=?', (AT,))
        self.run_round()
        with self.store.connect() as db:
            self.assertEqual([x['text'] for x in note_pages.page(db, mine)['lines']], ['Manuals are in the blue box'])

    def test_a_fact_about_a_thing_with_its_own_note_goes_in_that_note_never_beside_it_too(self):
        home = self.app.note_action('note_new', {'title': 'Home'}, owner_dashboard=True)['id']
        mine = self.app.note_action('note_new', {'title': 'Appliances', 'parent': home}, owner_dashboard=True)['id']
        washer = self.app.note_action('note_new', {'title': 'Dishwasher', 'parent': mine, 'lines': ['Filter cleaned every month']},
                                      owner_dashboard=True)['id']
        self.places = {'dishwasher': 'Appliances/Dishwasher', 'fridge': 'Appliances', 'oven': 'Appliances/Oven'}
        model = self.fact('The dishwasher is a Example DW-500')
        self.fact('The fridge warranty runs until June 2027')
        self.fact('The oven is a Example OV-2')  # no Oven note: The Machine starts none, it goes in Appliances
        self.run_round()
        self.assertIn('"Appliances": ["Dishwasher"]', self.asked[0], 'the call sees the owner\'s notes by name')
        with self.store.connect() as db:
            under = note_pages.page(db, mine)
            dish = note_pages.page(db, washer)
            names = sorted(x['name'] for x in note_pages.listing(db, '2026-11-14'))
        self.assertEqual(names, ['Appliances', 'Dishwasher', 'Home'])
        self.assertCountEqual([x['text'] for x in under['lines']], ['The fridge warranty runs until June 2027', 'The oven is a Example OV-2'])
        self.assertCountEqual([x['text'] for x in dish['lines']], ['Filter cleaned every month', 'The dishwasher is a Example DW-500'])
        self.assertEqual(dish['name'], 'Dishwasher')
        with self.store.connect() as db:  # the fact goes: so does its line there; their note and line stay
            db.execute('UPDATE facts SET removed_at=? WHERE id=?', (AT, model))
        self.run_round()
        with self.store.connect() as db:
            self.assertEqual([x['text'] for x in note_pages.page(db, washer)['lines']], ['Filter cleaned every month'])

    def test_a_line_from_a_message_says_who_it_came_from_not_its_subject(self):
        import note_pages_app
        mine = {'sam@example.com'}
        self.assertEqual(note_pages_app._sender(json.dumps({'from': '"Example Energy" <billing@energy.example>'}), mine), 'Example Energy')
        self.assertEqual(note_pages_app._sender(json.dumps({'from': 'billing@energy.example'}), mine), 'billing@energy.example')
        self.assertEqual(note_pages_app._sender(json.dumps({'from': 'Sam <SAM@example.com>'}), mine), '', 'the owner\'s own: its subject')
        self.assertEqual(note_pages_app._sender('{}', mine), '')
        self.assertEqual(note_pages_app._sender({'from': 'Example Water <bills@water.example>'}, mine), 'Example Water', 'as Store.events reads it')

    def test_homes_own_tables_from_before_move_over_once(self):
        with self.store.connect() as db:
            db.execute('DROP TABLE section_topics')
            db.execute('DROP TABLE section_state')
            db.execute("CREATE TABLE home_topics(key TEXT PRIMARY KEY, section TEXT NOT NULL, note TEXT NOT NULL DEFAULT '', at TEXT NOT NULL)")
            db.execute('CREATE TABLE home_state(id INTEGER PRIMARY KEY CHECK(id=1), at TEXT NOT NULL)')
            db.execute("INSERT INTO home_topics VALUES('bill:x','Appliances','Dishwasher',?)", (AT,))
            db.execute('INSERT INTO home_state VALUES(1,?)', (AT,))
            section_notes.ensure(db)
            section_notes.ensure(db)
            self.assertEqual([tuple(r) for r in db.execute('SELECT kind,key,section,note FROM section_topics')], [('home', 'bill:x', 'Appliances', 'Dishwasher')])
            self.assertFalse(section_notes.due(db, home_notes.KIND, AT), 'its last round is kept')
            self.assertFalse(db.execute("SELECT 1 FROM sqlite_master WHERE name IN ('home_topics','home_state')").fetchone())

    def test_a_canceled_subscription_isnt_on_home(self):
        with self.store.connect() as db:
            subscriptions.ensure(db)  # made by the Subscriptions routine's first run
            rows = [{'key': 'stream.example', 'name': 'Example Stream', 'period': 'month', 'area': 'personal'},
                    {'key': 'news.example', 'name': 'Example News', 'period': 'year', 'area': 'personal'},
                    {'key': 'tool.example', 'name': 'Example Tool', 'period': 'month', 'area': 'work'}]
            event = db.execute("INSERT INTO events(account_id,source_id,kind,title,body,occurred_at,metadata,content_hash,ingested_at) VALUES('home','subs','routine.subscriptions','Subscriptions','',?,?,'h',?)",
                               (AT, json.dumps({'subs': True, 'rows': rows}), AT)).lastrowid
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at) VALUES('subs1','subs1','Subscriptions','',?,?,?)",
                       (json.dumps([event]), json.dumps(['home']), AT))
            for n, row in enumerate(rows):
                db.execute('INSERT INTO subs_items(suggestion_id,item,key,next,updated_at) VALUES(?,?,?,?,?)', ('subs1', n, row['key'], '2026-12-01', AT))
            db.execute("INSERT INTO subs_kept(key,choice,at) VALUES('news.example','cancel',?)", (AT,))
            found = section_notes.subscriptions(db, [HOME, JOB])
        self.assertEqual([(x['name'], x['period'], x['todo']) for x in found], [('Example Stream', 'month', 'subs1')])


if __name__ == '__main__':
    unittest.main()
