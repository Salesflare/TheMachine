"""The one-time pass that ties loose facts to who they are about (fact_ties.py): only facts with real candidates reach
a model, a pick outside a fact's own candidates is never written, the owner and their own organization are never
candidates, and one entry under Learning, Changes undoes it. And a fact a model says is about the owner stays general."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from seams import patch_everywhere

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('fact_ties_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import fact_ties  # noqa: E402

NOW = dt.datetime(2026, 10, 16, 12, tzinfo=dt.timezone.utc)
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.example', 'boundary': 'work:acme'}], 'owner_name': 'Sam Owner'}
ANN, ANNA, GLOBEX, OWN, ME = 'email:ann@client.example', 'email:ann@other.example', 'org:globex.example', 'org:acme.example', 'email:sam@acme.example'


class FactTies(unittest.TestCase):
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
        for node, name, kind in ((ANN, 'Ann Example', 'person'), (ANNA, 'Ann Other', 'person'), (GLOBEX, 'Globex', 'org'),
                                 (OWN, 'Acme', 'org'), (ME, 'Sam Owner', 'person')):
            self.node(node, name, kind)
        with self.store.connect() as db:
            db.execute("INSERT INTO learning_state(key,value) VALUES('facts_named','{}')")  # the name pass ran
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'p1', 'kind': 'gmail.message', 'occurred_at': NOW.isoformat(),
                                             'title': 'Invoice', 'body': 'Open.', 'deleted': False,
                                             'metadata': {'from': 'Lee <lee@vendor.example>', 'to': 'sam@acme.example', 'cc': '', 'labels': ['INBOX'],
                                                          'message-id': '<p1@x>', 'thread_id': 'tp1'}}])
        self.store.decide(self.store.suggest('note', 'Pay the vendor', 'Body', [1])['id'], 'reject', 'a note', 'owner-note', 'dashboard')

    def node(self, node_id, name, kind='person'):
        with self.store.connect() as db:
            db.execute('INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,?,?,1,0,?)', (node_id, kind, name, '{}'))

    def fact(self, text):
        with self.store.connect() as db:
            return db.execute("INSERT INTO facts(text,decision_id,created_at,kind) VALUES(?,'owner-note',?,'fact')", (text, NOW.isoformat())).lastrowid

    def about(self):
        with self.store.connect() as db:
            return [tuple(r) for r in db.execute('SELECT fact_id,node_id,by,removed_at IS NOT NULL FROM fact_about ORDER BY fact_id,node_id')]

    def test_only_real_candidates_reach_the_model_and_only_a_given_candidate_is_written(self):
        ann = self.fact('Calls with Ann work best before ten.')     # two people called Ann: the model judges
        self.fact('Ann likes short calls.')                         # a short word that only starts a sentence: no candidate
        org = self.fact('Their finance team at Globex pays late.')
        own = self.fact('Acme closes the books on the 5th.')        # the owner's own company: no candidate
        plain = self.fact('Replies stay under five sentences.')     # no record shares a word: never asked
        untied = self.fact('Globex wants quotes as a PDF.')
        self.store.fact_unlink(untied, GLOBEX)                      # the owner said it isn't: never asked again
        prompts = []

        def ask(prompt):
            prompts.append(prompt)
            asked = json.loads(prompt[prompt.index('['):])
            self.assertEqual({f['id'] for f in asked}, {ann, org})
            self.assertEqual({f['id']: sorted(f['candidates'].values()) for f in asked},
                             {ann: ['Ann Example (person)', 'Ann Other (person)'], org: ['Globex (org)']})
            key = next(k for k, v in next(f for f in asked if f['id'] == ann)['candidates'].items() if v.startswith('Ann Example'))
            return json.dumps({str(ann): key, str(org): 'z', str(own): 'a', str(plain): 'a'})  # z: no such candidate

        with self.store.connect() as db:
            self.assertTrue(fact_ties.due(db))
        self.assertEqual(self.app.fact_ties_run(ask), {'linked': 1})
        self.assertEqual(len(prompts), 1)
        self.assertEqual([r for r in self.about() if r[2] == 'tie'], [(ann, ANN, 'tie', 0)])
        with self.store.connect() as db:
            self.assertFalse(fact_ties.due(db))  # once
        change = self.store.snapshot([])['learning_changes'][0]
        self.assertEqual((change['kind'], change['line']), ('about', ['Facts tied to who they are about: {}', 1]))
        self.store.undo_learning(change['id'])
        self.assertEqual([r for r in self.about() if r[0] == ann], [(ann, ANN, 'tie', 1)])  # gone, and stays gone

    def test_a_reply_that_is_not_the_json_asked_writes_nothing_and_is_tried_again_a_few_times(self):
        self.fact('Calls with Ann work best before ten.')
        for n in range(fact_ties.TRIES):
            with self.store.connect() as db:
                self.assertTrue(fact_ties.due(db))
            self.assertEqual(self.app.fact_ties_run(lambda prompt: 'I am not sure.'), {'error': 'bad_answer'})
        self.assertEqual(self.about(), [])
        with self.store.connect() as db:
            self.assertFalse(fact_ties.due(db))

    def test_with_nothing_to_ask_no_model_turn_and_no_change(self):
        self.fact('Replies stay under five sentences.')
        self.assertEqual(self.app.fact_ties_run(lambda prompt: self.fail('no turn')), {'linked': 0})
        self.assertEqual(self.store.snapshot([])['learning_changes'], [])

    def test_a_fact_said_to_be_about_the_owner_or_their_company_stays_general(self):
        self.assertNotIn('about', self.store.remember_fact('Closes the books on the 5th.', 'owner-note', about=[OWN]))
        self.assertNotIn('about', self.store.remember_fact('Likes short replies.', 'owner-note', about=[ME]))
        self.assertEqual(self.store.remember_fact('Pays late.', 'owner-note', about=[GLOBEX, OWN])['about'], [GLOBEX])
        fact = self.fact('Works from home on Fridays.')
        with self.assertRaises(ValueError):
            self.store.fact_about(fact, [ME])


if __name__ == '__main__':
    unittest.main()
