"""A fact is tied to the record it is about (fact_links.py, machine/store/facts.py): when it is saved, one time for
the facts already there (shown under Learning, Changes, with Undo), and a preparation picks facts by its to-do's
records first, never from the other side (work or personal)."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from seams import patch_everywhere

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('fact_links_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import fact_links  # noqa: E402
import memory_use  # noqa: E402
from machine.app.recall import recall  # noqa: E402

NOW = dt.datetime(2026, 10, 16, 12, tzinfo=dt.timezone.utc)
SETTINGS = {'url': 'http://embed.invalid', 'model': 'm', 'dims': 2}
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.example', 'boundary': 'work:acme'}], 'embeddings': SETTINGS}
ANN, LEE, GLOBEX = 'email:ann@client.example', 'email:lee@globex.example', 'org:globex.example'


def mail(n, sender, title, body):
    return {'account_id': 'work', 'source_id': f'p{n}', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(days=n)).isoformat(),
            'title': title, 'body': body, 'deleted': False,
            'metadata': {'from': sender, 'to': 'sam@acme.example', 'cc': '', 'labels': ['INBOX'], 'message-id': f'<p{n}@x>', 'thread_id': f'tp{n}'}}


def embed(settings, texts, timeout=120):
    return [[1.0, 0.0] if 'number 3 ' in t or 'number 7 ' in t or 'Answer Ann' in t else [0.0, 1.0] for t in texts]


class FactLinks(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {**CONFIG, 'database': str(Path(temp.name) / 'events.sqlite')}
        for started in (patch_everywhere(a, 'now', lambda: NOW.isoformat()), patch.object(a.embeddings, 'embed', side_effect=embed)):
            started.start()
            self.addCleanup(started.stop)
        self.store.commit_page('work', {}, [mail(1, 'Ann Example <ann@client.example>', 'Pilot timing', 'Can the pilot move to March?'),
                                            mail(2, 'Lee Park <lee@globex.example>', 'Invoice', 'The September invoice is still open.')])
        with self.store.connect() as db:
            db.isolation_level = None
            a.graph.build(db, self.app.config, NOW.isoformat())
            db.execute("UPDATE graph_nodes SET name='Globex' WHERE id=?", (GLOBEX,))
        self.todo = self.store.suggest('pilot', 'Answer Ann about the pilot', 'Ann asks to move the pilot.', [1])['id']
        self.other = self.store.suggest('other', 'Pay the vendor', 'Body', [2])['id']
        self.store.decide(self.other, 'reject', 'we stopped using them', 'owner-note', 'dashboard')

    def about(self, fact_id=None):
        with self.store.connect() as db:
            return [tuple(r) for r in db.execute('SELECT fact_id,node_id,by,removed_at IS NOT NULL FROM fact_about WHERE ? IS NULL OR fact_id=? ORDER BY fact_id,node_id',
                                                 (fact_id, fact_id))]

    def old_fact(self, text, todo=None):
        """A fact as it was saved before facts were tied by name."""
        with self.store.connect() as db:
            return db.execute("INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind) VALUES(?,'owner-note',?,?,'fact')",
                              (text, todo, NOW.isoformat())).lastrowid

    def node(self, node_id, name, kind='person', **info):
        with self.store.connect() as db:
            db.execute('INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,?,?,1,0,?)', (node_id, kind, name, json.dumps(info)))

    def named(self, text, near=()):
        with self.store.connect() as db:
            return fact_links.named(fact_links.index(db), text, near)

    def test_a_text_names_a_record_by_its_own_name_and_only_one(self):
        self.assertEqual(self.named('Ann Example wants invoices as a PDF.'), (ANN, 'one'))
        self.assertEqual(self.named("Send Ann Example's invoices to finance."), (ANN, 'one'))  # a possessive is still their name
        self.assertEqual(self.named('We pay Globex within 30 days.'), (GLOBEX, 'one'))
        self.assertEqual(self.named('Ann wants invoices as a PDF.'), (None, 'none'))  # a first name alone names no one
        self.assertEqual(self.named('ann example wants a pdf, and globex too.'), (None, 'none'))  # not their name as written
        self.assertEqual(self.named('Globexit is a word of its own.'), (None, 'none'))  # whole words only
        self.assertEqual(self.named('Ann Example and Lee Park both want a PDF.'), (None, 'several'))
        self.assertEqual(self.named('Replies stay under five sentences.'), (None, 'none'))

    def test_a_name_two_records_share_links_nothing_unless_one_is_on_the_facts_own_to_do(self):
        self.node('li:ann-example-2', 'Ann Example')
        self.assertEqual(self.named('Ann Example wants invoices as a PDF.'), (None, 'shared'))
        self.assertEqual(self.named('Ann Example wants invoices as a PDF.', {ANN}), (ANN, 'one'))
        self.assertEqual(self.named('Ann Example wants invoices as a PDF.', {ANN, 'li:ann-example-2'}), (None, 'shared'))
        self.node('org:globexlabs.example', 'Globex Labs', 'org')  # the longer name is the one that is named
        self.assertEqual(self.named('Globex Labs pays within 30 days.'), ('org:globexlabs.example', 'one'))
        # a record known under two ids is one record
        self.node('email:lee@home.example', 'Lee Park')
        with self.store.connect() as db:
            db.execute('UPDATE graph_nodes SET info=? WHERE id=?', (json.dumps({'identifiers': ['email:lee@home.example']}), LEE))
        self.assertEqual(self.named('Lee Park signs off on invoices.'), (LEE, 'one'))

    def test_a_saved_fact_is_tied_to_the_record_it_names_or_the_one_it_was_told(self):
        named = self.store.remember_fact('Ann Example wants invoices as a PDF.', 'owner-note')
        self.assertEqual((named['about'], self.about(named['id'])), ([ANN], [(named['id'], ANN, 'name', 0)]))
        general = self.store.remember_fact('Replies stay under five sentences.', 'owner-note')
        self.assertEqual((general.get('about'), self.about(general['id'])), (None, []))
        rule = self.store.remember_fact('For Globex, put the order number in the subject.', 'owner-note', 'draft')
        self.assertEqual(self.about(rule['id']), [])  # a rule is about a kind of task, never about a record
        # a preparation names who by the address or name its People and projects lines show; a review by node id
        told = self.store.remember_fact('Prefers a call over a long mail.', 'owner-note', about=['lee@globex.example'])
        self.assertEqual(self.about(told['id']), [(told['id'], LEE, 'review', 0)])
        self.assertEqual(self.store.remember_fact('Pays on the last day of the month.', 'owner-note', about=['Globex'])['about'], [GLOBEX])
        self.assertEqual(self.store.remember_fact('Reads mail in the morning only.', 'owner-note', about=[ANN])['about'], [ANN])
        with self.assertRaises(ValueError):
            self.store.remember_fact('Likes short updates.', 'owner-note', about=['Nobody Known'])
        # the same thing in other words still takes the place of the one tied by its name
        again = self.store.remember_fact('Ann Example wants invoices as a PDF, sent by mail.', 'owner-note')
        self.assertEqual(again.get('merged'), 1)
        self.assertEqual([r[1] for r in self.about(again['id'])], [ANN])

    def test_the_owner_saying_who_a_fact_is_not_about_holds_for_a_later_save(self):
        fact = self.store.remember_fact('Ann Example wants invoices as a PDF.', 'owner-note')
        self.store.fact_unlink(fact['id'], ANN)
        self.assertEqual(self.store.remember_fact('Ann Example wants invoices as a PDF.', 'owner-note')['id'], fact['id'])
        self.assertEqual(self.about(fact['id']), [(fact['id'], ANN, 'owner', 1)])
        with self.store.connect() as db:
            self.assertEqual(self.store.link_named(db, fact['id'], 'Ann Example wants invoices as a PDF.'), (None, 'tied'))

    def test_the_one_time_pass_ties_the_facts_already_there_and_one_undo_takes_it_back(self):
        self.node('li:lee-park-2', 'Lee Park')
        ann = self.old_fact('Ann Example wants invoices as a PDF.')
        org = self.old_fact('We pay Globex within 30 days.', self.other)
        shared = self.old_fact('Lee Park signs off on invoices.')           # two records have that name
        on_todo = self.old_fact('Lee Park reads mail in the morning.', self.other)  # one of them is on its own to-do
        both = self.old_fact('Ann Example introduced us to Globex.')
        plain = self.old_fact('Replies stay under five sentences.')
        kept = self.store.remember_fact('Prefers a call over a long mail.', 'owner-note', about=[LEE])['id']
        found = self.store.name_links_once()
        self.assertEqual((sorted(found['pairs']), found['shared'], found['several']), ([[ann, ANN], [org, GLOBEX], [on_todo, LEE]], 1, 1))
        self.assertEqual([r for r in self.about() if r[2] == 'name'], [(ann, ANN, 'name', 0), (org, GLOBEX, 'name', 0), (on_todo, LEE, 'name', 0)])
        self.assertEqual([self.about(i) for i in (shared, both, plain)], [[], [], []])
        self.assertIsNone(self.store.name_links_once())  # once
        # the owner sees it where they manage what was learned: on each fact, and as one change with Undo
        state = self.store.snapshot([])
        facts = {f['id']: f.get('about') for f in state['facts']}
        self.assertEqual((facts[ann], facts[org], facts[plain]), ([{'id': ANN, 'name': 'Ann Example'}], [{'id': GLOBEX, 'name': 'Globex'}], []))
        change = state['learning_changes'][0]
        self.assertEqual((change['kind'], change['line'], change['undone']), ('about', ['Facts that name one person, organization or project: {}', 3], False))
        self.store.fact_unlink(org, GLOBEX)  # one they took off themselves stays theirs
        self.store.undo_learning(change['id'])
        self.assertEqual(self.about(ann), [(ann, ANN, 'name', 1)])
        self.assertEqual(self.about(org), [(org, GLOBEX, 'owner', 1)])
        self.assertEqual(self.about(kept), [(kept, LEE, 'review', 0)])  # what a review tied is not this pass's
        state = self.store.snapshot([])
        self.assertEqual(({f['id']: f.get('about') for f in state['facts']}[ann], state['learning_changes'][0]['undone']), ([], True))
        with self.assertRaises(ValueError):
            self.store.undo_learning(change['id'])
        with self.store.connect() as db:  # and a later save of the same fact doesn't tie it again
            self.assertEqual(self.store.link_named(db, ann, 'Ann Example wants invoices as a PDF.'), (None, 'tied'))

    def test_the_one_time_pass_waits_for_a_graph_and_leaves_nothing_when_nothing_names_a_record(self):
        self.old_fact('Replies stay under five sentences.')
        with self.store.connect() as db:
            db.execute('DELETE FROM graph_nodes')
        self.assertIsNone(self.store.name_links_once())
        self.node(ANN, 'Ann Example')
        self.assertEqual(self.store.name_links_once(), {'pairs': [], 'shared': 0, 'several': 0})
        self.assertEqual(self.store.snapshot([])['learning_changes'], [])
        self.assertIsNone(self.store.name_links_once())

    def many(self):
        for i in range(30):
            self.store.remember_fact(f'General fact number {i} about how the owner works with pilots.', 'owner-note')

    def prep(self, todo=None):
        memory = recall(self.app, 'preparation', {'todo': todo or self.todo}, 14000)
        return memory, memory.text('facts'), memory.text('records')

    def test_a_preparation_gets_the_facts_about_its_records_first_within_the_same_top(self):
        self.many()
        ann = self.store.remember_fact('Ann Example wants invoices as a PDF.', 'owner-note')['id']
        told = self.store.remember_fact('Prefers a call over a long mail.', 'owner-note', about=[ANN])['id']
        lee = self.store.remember_fact('Lee Park signs off on invoices.', 'owner-note')['id']
        before = self.store.facts_for(self.todo, 'fact', SETTINGS, accounts=CONFIG['accounts'], top=2)
        memory, facts, records = self.prep()
        # not close in meaning to the to-do, and in: they are about the person it is with. Lee's is not.
        self.assertIn('- Ann Example wants invoices as a PDF.', facts)
        self.assertIn('- Prefers a call over a long mail. (about Ann Example)', facts)  # its words don't say who
        self.assertNotIn('Lee Park', facts)
        self.assertIn('number 3 ', facts)
        self.assertEqual(before.count('\n'), 1)  # the same top: with two places, both go to the facts about Ann
        self.assertNotIn('number 3 ', before)
        items = {i.row_id: i for i in memory.picked()['fact']}
        self.assertEqual((items[str(ann)].how, items[str(ann)].about, items[str(ann)].used), ('about', (ANN,), True))
        self.assertEqual((items[str(told)].how, items[str(told)].about), ('about', (ANN,)))
        self.assertNotIn(str(lee), items)
        closest = next(i for i in items.values() if 'number 3 ' in i.text)
        self.assertEqual((closest.how, closest.about), ('closeness', ()))
        self.assertIn(['fact', str(ann), 'about', None, len('- Ann Example wants invoices as a PDF.'), 1], memory.rows())
        # the record's own line doesn't say them again
        self.assertIn('Ann Example', records)
        self.assertNotIn('known:', records)
        self.assertIn('known: Prefers a call over a long mail.', self.app.graph_lines(self.todo))  # as before, read on its own
        # the log keeps ids and numbers, and the facts count as used
        memory_use.record(self.store, 'preparation', memory.rows(), 'run-1', self.todo)
        with self.store.connect() as db:
            self.assertEqual([tuple(r) for r in db.execute("SELECT row_id,how FROM memory_use WHERE how='about' AND kind='fact' ORDER BY row_id")],
                             sorted([(str(ann), 'about'), (str(told), 'about')]))
            self.assertEqual(db.execute('SELECT count(*) FROM facts WHERE used_at IS NOT NULL AND id IN (?,?)', (ann, told)).fetchone()[0], 2)

    def test_a_fact_about_someone_on_the_other_side_stays_out_of_the_prompt(self):
        self.many()
        self.store.remember_fact('Ann Example wants invoices as a PDF.', 'owner-note')
        self.store.remember_fact('We pay Globex within 30 days.', 'owner-note')

        def side(value):
            with self.store.connect() as db:
                db.execute('UPDATE graph_nodes SET info=json_set(info,?,?) WHERE id=?', ('$.side', value, ANN))
            return self.prep()[1]
        self.assertIn('Ann Example wants', side('work'))        # a work to-do, a work contact
        self.assertNotIn('Ann Example', side('personal'))       # a friend's fact never goes in a work prompt
        self.assertIn('Ann Example wants', side(None))          # no side known: as before
        few = self.store.facts_for(self.todo, 'fact', None, accounts=CONFIG['accounts'], all_under=10 ** 6)
        self.assertIn('Ann Example wants', few)
        side('personal')
        few = self.store.facts_for(self.todo, 'fact', None, accounts=CONFIG['accounts'], all_under=10 ** 6)
        self.assertNotIn('Ann Example', few)                    # also while everything learned still fits
        self.assertIn('General fact number 0', few)
        # the other way round: a personal to-do never gets a work contact's fact; one about an organization has no side
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET area='personal' WHERE id=?", (self.todo,))
        self.assertNotIn('Ann Example', side('work'))
        self.assertIn('Ann Example wants', side('personal'))

    def test_the_review_says_which_records_its_facts_are_about(self):
        ann = self.store.remember_fact('Ann Example wants invoices as a PDF.', 'owner-note')['id']
        memory = recall(self.app, 'review')
        text = memory.text('facts')
        self.assertIn(f'- [{ann}] Ann Example wants invoices as a PDF.', text)
        self.assertEqual([i.about for i in memory.picked()['fact']], [(ANN,)])


if __name__ == '__main__':
    unittest.main()
