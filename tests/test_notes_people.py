"""Facts brought in from the owner's notes go on who they are about, in the owner's words (notes_people.py): the turn
judges who by meaning among real people only, a fact about someone not in the Graph stays the owner's, a date of birth
becomes the person's kept birthday (which the Birthdays routine reads), and one entry under Learning, Changes undoes
it all. Facts about a Personal person never go to the team."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from seams import patch_everywhere

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('notes_people_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import birthdays  # noqa: E402
import notes_people  # noqa: E402
import team_learnings  # noqa: E402

NOW = dt.datetime(2026, 10, 16, 12, tzinfo=dt.timezone.utc)
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.example', 'boundary': 'work:acme'}], 'owner_name': 'Sam Owner'}
ANA, MIA, MIA_W, GLOBEX, ME = 'email:ana@home.example', 'email:mia@home.example', 'email:mia@globex.example', 'org:globex.example', 'email:sam@acme.example'


class NotesPeople(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.store.config = CONFIG
        self.app = object.__new__(a.App)
        self.app.store, self.app.config = self.store, CONFIG
        started = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        started.start()
        self.addCleanup(started.stop)
        self.node(GLOBEX, 'Globex', {}, 'org')
        self.node(ANA, 'Ana Example', {'role': 'Wife', 'side': 'personal', 'side_why': 'network'})
        self.node(MIA, 'Mia Sample', {'side': 'personal', 'side_why': 'project'})
        self.node(MIA_W, 'Mia Worker', {'org': GLOBEX, 'side': 'work', 'side_why': 'address'})
        self.node(ME, 'Sam Owner', {})

    def node(self, node_id, name, info, kind='person'):
        with self.store.connect() as db:
            db.execute('INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,?,?,1,0,?)', (node_id, kind, name, json.dumps(info)))

    def fact(self, text, n):
        with self.store.connect() as db:
            return db.execute("INSERT INTO facts(text,decision_id,created_at,kind,fact_kind,source) VALUES(?,?,?,'fact','fact','notes:USER.md')",
                              (text, f'notes:USER.md:{n}', NOW.isoformat())).lastrowid

    def rows(self, sql, args=()):
        with self.store.connect() as db:
            return [tuple(r) for r in db.execute(sql, args)]

    def text(self, fact_id):
        return self.rows('SELECT text FROM facts WHERE id=?', (fact_id,))[0][0]

    def ask(self, answers, seen=None):
        """A model that answers by fact text: {start of the fact: (candidate name or None, text, birthday)}."""
        def reply(prompt):
            facts = json.loads(prompt[prompt.rindex('<<<') + 3:prompt.rindex('>>>')])
            if seen is not None:
                seen.extend(facts)
            out = {}
            for f in facts:
                who, text, born = next(v for k, v in answers.items() if f['fact'].startswith(k))
                key = next((k for k, v in f['candidates'].items() if who and v.startswith(who)), who and 'z')
                out[str(f['id'])] = {'about': key, 'text': text, 'birthday': born}
            return json.dumps(out)
        return reply

    def test_facts_go_on_who_they_are_about_in_the_owners_words_and_a_birthday_is_kept(self):
        mia = self.fact("The owner's daughter, Mia, was born on 2021-03-04.", 1)
        ana = self.fact("The owner's wife, Ana, cannot eat gluten or onion.", 2)
        own = self.fact('The owner is the founder of Acme, a small software company.', 3)
        tom = self.fact("The owner's brother, Tom, lives in Lisbon.", 4)
        seen = []
        answers = {"The owner's daughter": ('Mia Sample', 'Your daughter Mia was born on 2021-03-04.', '2021-03-04'),
                   "The owner's wife": ('Ana Example', 'Your wife Ana cannot eat gluten or onion.', None),
                   'The owner is': (None, 'You are the founder of Acme, a small software company.', None),
                   "The owner's brother": ('Tom', 'Your brother Tom lives in Lisbon.', '1990-01-01')}  # Tom is no one here
        with self.store.connect() as db:
            self.assertTrue(notes_people.due(db))
        found = self.app.notes_people_run(ask=self.ask(answers, seen))
        self.assertEqual(found, {'linked': 2, 'reworded': 4, 'birthdays': 1})
        offered = {f['id']: sorted(f['candidates'].values()) for f in seen}
        self.assertEqual(offered[mia], ['Ana Example (Wife; Personal)', 'Mia Sample (Personal)', 'Mia Worker (works at Globex; Work)'])
        self.assertEqual(offered[tom], ['Ana Example (Wife; Personal)'])  # family by role; never the owner
        self.assertEqual(self.rows("SELECT fact_id,node_id FROM fact_about WHERE by='notes' ORDER BY fact_id"), [(mia, MIA), (ana, ANA)])
        self.assertEqual(self.text(own), 'You are the founder of Acme, a small software company.')
        self.assertEqual(self.text(tom), 'Your brother Tom lives in Lisbon.')  # nobody made up: still the owner's fact
        with self.store.connect() as db:
            self.assertEqual(birthdays.fact_ids(db, dt.date(2026, 3, 4)), [(MIA, 'contacts')])
            self.assertFalse(notes_people.due(db))  # read once
        facts = self.store.snapshot([])['facts']
        self.assertEqual({f['id'] for f in facts if f['kind'] != 'draft' and not f.get('about')}, {own, tom})  # Learning, Facts
        with self.store.connect() as db:  # the team never hears what is known about family
            kept = [r[0] for r in db.execute(f"SELECT id FROM facts WHERE removed_at IS NULL {team_learnings._owner_facts(db)} ORDER BY id")]
        self.assertEqual(kept, [own, tom])

        change = self.store.snapshot([])['learning_changes'][0]
        self.assertEqual((change['kind'], change['line']), ('about', ['Facts from your notes put on who they are about: {}', 4]))
        self.store.undo_learning(change['id'])
        self.assertEqual(self.text(mia), "The owner's daughter, Mia, was born on 2021-03-04.")
        self.assertEqual(self.text(own), 'The owner is the founder of Acme, a small software company.')
        self.assertEqual(self.rows("SELECT count(*) FROM fact_about WHERE removed_at IS NULL"), [(0,)])
        self.assertEqual(self.rows("SELECT count(*) FROM person_facts"), [(0,)])

    def test_the_owners_own_word_since_and_a_birthday_kept_before_stay(self):
        mia = self.fact("The owner's daughter, Mia, was born on 2021-03-04.", 1)
        ana = self.fact("The owner's wife, Ana, cannot eat gluten.", 2)
        with self.store.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS person_facts(identifier TEXT NOT NULL,field TEXT NOT NULL,value TEXT NOT NULL,rank INTEGER NOT NULL,"
                       "source TEXT NOT NULL,seen_at TEXT NOT NULL,PRIMARY KEY(identifier,field))")
            db.execute("INSERT INTO person_facts VALUES(?,'birthday','2021-03-05',1,'google',?)", (MIA, NOW.isoformat()))
        prompts = []

        def reply(prompt):
            prompts.append(prompt)
            with self.store.connect() as db:  # the owner edits it while the turn runs
                db.execute('UPDATE facts SET text=? WHERE id=?', ('Ana cannot eat gluten, ever.', ana))
            return json.dumps({str(mia): {'about': 'b', 'text': 'Your daughter Mia was born on 2021-03-04.', 'birthday': '2021-03-04'},
                               str(ana): {'about': 'a', 'text': 'Your wife Ana cannot eat gluten.', 'birthday': None}})

        found = self.app.notes_people_run(ask=reply)
        self.assertEqual(found['birthdays'], 0)
        self.assertEqual(self.text(ana), 'Ana cannot eat gluten, ever.')
        self.assertEqual(self.rows("SELECT node_id FROM fact_about WHERE fact_id=?", (ana,)), [])
        self.assertEqual(self.rows("SELECT value,source FROM person_facts WHERE identifier=?", (MIA,)), [('2021-03-05', 'google')])

    def test_a_pick_outside_the_candidates_or_a_bad_birthday_is_never_written(self):
        mia = self.fact("The owner's daughter, Mia, was born on 2021-03-04.", 1)
        reply = json.dumps({str(mia): {'about': ME, 'text': 'x', 'birthday': 'March 4'}})
        self.assertEqual(self.app.notes_people_run(ask=lambda prompt: reply), {'linked': 0, 'reworded': 0, 'birthdays': 0})
        self.assertEqual(self.rows('SELECT count(*) FROM fact_about'), [(0,)])
        self.assertEqual(self.store.snapshot([])['learning_changes'], [])

    def test_a_failed_turn_is_tried_a_few_times_and_a_new_fact_brings_it_back(self):
        self.fact("The owner's wife, Ana, cannot eat gluten.", 1)
        for _ in range(notes_people.TRIES):
            with self.store.connect() as db:
                self.assertTrue(notes_people.due(db))
            self.assertEqual(self.app.notes_people_run(ask=lambda prompt: 'Not sure.'), {'error': 'bad_answer'})
        with self.store.connect() as db:
            self.assertFalse(notes_people.due(db))
        self.fact('The owner runs every Sunday morning.', 2)
        with self.store.connect() as db:
            self.assertTrue(notes_people.due(db))

    def test_notes_are_judged_to_say_you_for_the_owner(self):
        import bring_in
        self.assertIn('"you" for the owner', bring_in.JUDGE)
        self.assertIn('"you" for the owner', notes_people.JUDGE)


if __name__ == '__main__':
    unittest.main()
