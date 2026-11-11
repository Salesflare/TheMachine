"""Who a to-do is for, and what is no to-do. A test persona's handoff to-do came from a client's email, but it showed a
closer colleague of theirs as its person, only because he was on the review meeting the to-do also held; and a booking
confirmation for the owner's own trip became a to-do to move their own gym slot. No live calls."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from seams import patch_everywhere  # noqa: E402,F401

spec = importlib.util.spec_from_file_location('lead_person_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class LeadPerson(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite')
        with self.store.connect() as db:
            for node, name, strength in (('email:lena@client.example', 'Lena Ortiz', 0.8), ('email:marco@client.example', 'Marco Bell', 1.3)):
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person',?,?,1,'{}')", (node, name, strength))
            # 1: Lena's handoff request, 2: the review meeting both are on, 3: Marco's own question in another thread
            for node, event in (('email:lena@client.example', 1), ('email:lena@client.example', 2), ('email:marco@client.example', 2),
                                ('email:marco@client.example', 3)):
                db.execute("INSERT INTO graph_events(node_id,event_id,at,direct) VALUES(?,?,'2026-11-09T00:00:00+00:00',1)", (node, event))

    def people(self, ids):
        with self.store.connect() as db:
            return [p['name'] for p in a.graph.card_people(db, ids)[0]]

    def test_the_main_sources_person_comes_first(self):
        self.assertEqual(self.people([1, 2, 3]), ['Lena Ortiz', 'Marco Bell'])

    def test_closest_first_among_the_rest(self):
        self.assertEqual(self.people([2]), ['Marco Bell', 'Lena Ortiz'])  # a meeting's own to-do: nobody leads it

    def test_the_rules_are_in_the_prompts(self):
        self.assertTrue('Automated mail alone makes a to-do only when it asks the owner to act' in a.review_prompt('r1', ['work']))
        self.assertTrue('nor a message you only read to answer the owner' in a.preparation_prompt({'job_id': 'j', 'suggestion_id': 's'}))


if __name__ == '__main__':
    unittest.main()
