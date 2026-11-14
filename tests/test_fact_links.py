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

    def named(self, text, near=(), config=None):
        with self.store.connect() as db:
            return fact_links.named(fact_links.index(db, config), text, near)

    def test_a_text_names_a_record_by_its_own_name_and_only_one(self):
        self.assertEqual(self.named('Ann Example wants invoices as a PDF.'), (ANN, 'one'))
        self.assertEqual(self.named("Send Ann Example's invoices to finance."), (ANN, 'one'))  # a possessive is still their name
        self.assertEqual(self.named('We pay Globex within 30 days.', {GLOBEX}), (GLOBEX, 'one'))
        self.assertEqual(self.named('We pay Globex within 30 days.'), (None, 'none'))  # one word, and not on its to-do: too weak
        self.assertEqual(self.named('Ann Example introduced us to Globex.'), (None, 'several'))
        self.assertEqual(self.named('Ann wants invoices as a PDF.'), (None, 'none'))  # a first name alone names no one
        self.assertEqual(self.named('ann example wants a pdf, and globex too.'), (None, 'none'))  # not their name as written
        self.assertEqual(self.named('Globexit is a word of its own.'), (None, 'none'))  # whole words only
        self.assertEqual(self.named('Ann Example and Lee Park both want a PDF.'), (None, 'several'))
        self.assertEqual(self.named('Replies stay under five sentences.'), (None, 'none'))

    def test_one_word_at_a_sentence_start_names_nothing(self):
        self.node('org:close.example', 'Close', 'org')
        self.node('org:monday.example', 'Monday', 'org')
        self.node('org:closelabs.example', 'Close Labs', 'org')
        for text in ('Close the deal by Friday.', 'Monday is my no-meeting day.', 'Send the offer first. Close wants it by Friday.',
                     'Two things: Monday is for planning.', 'Globex pays within 30 days.'):
            self.assertEqual(self.named(text), (None, 'none'), text)  # every sentence starts with a capital: no evidence
        self.assertEqual(self.named('We moved the pipeline to Close last year.', {'org:close.example'}), ('org:close.example', 'one'))
        self.assertEqual(self.named('Close the deal by Friday.', {'org:close.example'}), (None, 'none'))  # also on its own to-do
        self.assertEqual(self.named('Close Labs pays within 30 days.'), ('org:closelabs.example', 'one'))  # several words: a name
        self.assertEqual(self.named('Ann Example wants invoices as a PDF.'), (ANN, 'one'))
        self.assertIsNone(self.store.remember_fact('Close the deal by Friday when a client asks.', 'owner-note', quote='we stopped using them').get('about'))

    def test_a_name_the_machine_works_with_is_the_tool_not_the_company(self):
        self.assertIn('slack', fact_links.tools())  # from the product's own lists of sources, connectors and channels
        self.assertTrue({'gmail', 'whatsapp', 'telegram', 'outlook', 'linkedin', 'zoom', 'teams', 'stripe', 'salesflare'} <= fact_links.tools())
        self.assertNotIn('globex', fact_links.tools())
        self.node('org:slack.example', 'Slack', 'org')
        self.node('org:salesflare.example', 'Salesflare', 'org')
        self.node('org:teams.example', 'Microsoft Teams', 'org')
        self.assertEqual(self.named('Never message me on Slack after 8.', config=CONFIG), (None, 'none'))
        self.assertEqual(self.named('The pipeline lives in Salesflare for now.', config=CONFIG), (None, 'none'))
        self.assertEqual(self.named('Calls with clients go over Microsoft Teams only.', config=CONFIG), (None, 'none'))
        self.assertEqual(self.named('We pay Globex within 30 days.', {GLOBEX}, CONFIG), (GLOBEX, 'one'))
        self.assertEqual(self.named('Never message me on Slack after 8.', {'org:slack.example'}, CONFIG), (None, 'none'))
        self.store.config = CONFIG
        self.assertIsNone(self.store.remember_fact('Never message me on Slack after 8.', 'owner-note', quote='we stopped using them').get('about'))
        with self.store.connect() as db:
            old = db.execute("INSERT INTO facts(text,decision_id,created_at,kind) VALUES('Send files over Slack, not by mail.','owner-note',?,'fact')", (NOW.isoformat(),)).lastrowid
        self.assertEqual(self.store.name_links_once()['pairs'], [])  # the one-time pass holds the same rule
        self.assertEqual(self.about(old), [])
        # the model saying who by name is its own call: the company can still be told
        self.assertEqual(self.store.remember_fact('Their sales team answers within a day.', 'owner-note', about=['Slack'], quote='we stopped using them')['about'], ['org:slack.example'])

    def test_the_owners_own_person_and_organization_are_never_what_a_fact_is_about(self):
        config = {**CONFIG, 'owner_name': 'Sam Owner'}
        self.node('email:sam@acme.example', 'Sam Owner')          # their own address
        self.node('li:sam-owner', 'Sam Owner')                    # their name on another network
        self.node('org:acme.example', 'Acme', 'org')              # their mail domain's organization
        self.node('org:acmegroup.example', 'Acme Group', 'org')   # where a colleague is
        self.node('email:kim@acmegroup.example', 'Kim Mate', colleague=True, org='org:acmegroup.example')
        for text in ('Lee asked whether Sam Owner signs the contracts.', 'Invoices from Acme go out on the 5th.', 'At Acme Group the books close on the 5th.'):
            self.assertEqual(self.named(text, config=config), (None, 'none'), text)
        self.assertEqual(self.named('Kim Mate signs the contracts.', config=config), ('email:kim@acmegroup.example', 'one'))  # a colleague is a person
        self.assertEqual(self.named('We pay Globex within 30 days.', {GLOBEX}, config), (GLOBEX, 'one'))
        self.assertEqual(self.named('Invoices from Acme go out on the 5th.', {'org:acme.example'}, config), (None, 'none'))
        with self.store.connect() as db:
            db.execute("UPDATE graph_nodes SET id='crm:77' WHERE id='org:acme.example'")  # their company under another id
        self.assertEqual(self.named('Invoices from Acme go out on the 5th.', {'crm:77'}, config), (None, 'none'))
        self.store.config = config
        self.assertIsNone(self.store.remember_fact('Invoices from Acme go out on the 5th.', 'owner-note', quote='we stopped using them').get('about'))
        self.assertIsNone(self.store.remember_fact('Lee asked whether Sam Owner signs the contracts.', 'owner-note', quote='we stopped using them').get('about'))

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
        named = self.store.remember_fact('Ann Example wants invoices as a PDF.', 'owner-note', quote='we stopped using them')
        self.assertEqual((named['about'], self.about(named['id'])), ([ANN], [(named['id'], ANN, 'name', 0)]))
        general = self.store.remember_fact('Replies stay under five sentences.', 'owner-note', quote='we stopped using them')
        self.assertEqual((general.get('about'), self.about(general['id'])), (None, []))
        rule = self.store.remember_fact('For Globex, put the order number in the subject.', 'owner-note', 'draft', quote='we stopped using them')
        self.assertEqual(self.about(rule['id']), [])  # a rule is about a kind of task, never about a record
        # a preparation names who by the address or name its People and projects lines show; a review by node id
        told = self.store.remember_fact('Prefers a call over a long mail.', 'owner-note', about=['lee@globex.example'], quote='we stopped using them')
        self.assertEqual(self.about(told['id']), [(told['id'], LEE, 'review', 0)])
        self.assertEqual(self.store.remember_fact('Pays on the last day of the month.', 'owner-note', about=['Globex'], quote='we stopped using them')['about'], [GLOBEX])
        self.assertEqual(self.store.remember_fact('Reads mail in the morning only.', 'owner-note', about=[ANN], quote='we stopped using them')['about'], [ANN])
        with self.assertRaises(ValueError):
            self.store.remember_fact('Likes short updates.', 'owner-note', about=['Nobody Known'], quote='we stopped using them')
        # the same thing in other words still takes the place of the one tied by its name
        again = self.store.remember_fact('Ann Example wants invoices as a PDF, sent by mail.', 'owner-note', quote='we stopped using them')
        self.assertEqual(again.get('merged'), 1)
        self.assertEqual([r[1] for r in self.about(again['id'])], [ANN])

    def test_the_owner_saying_who_a_fact_is_not_about_holds_for_a_later_save(self):
        fact = self.store.remember_fact('Ann Example wants invoices as a PDF.', 'owner-note', quote='we stopped using them')
        self.store.fact_unlink(fact['id'], ANN)
        self.assertEqual(self.store.remember_fact('Ann Example wants invoices as a PDF.', 'owner-note', quote='we stopped using them')['id'], fact['id'])
        self.assertEqual(self.about(fact['id']), [(fact['id'], ANN, 'owner', 1)])
        with self.store.connect() as db:
            self.assertEqual(self.store.link_named(db, fact['id'], 'Ann Example wants invoices as a PDF.'), (None, 'tied'))

    def test_the_record_page_is_where_its_facts_live_add_edit_not_about_them_and_remove(self):
        app = a.App.__new__(a.App)
        app.store, app.config = self.store, self.app.config
        with self.assertRaises(ValueError):  # only the owner, on the dashboard
            app.action('graph_fact_add', {'node_id': ANN, 'text': 'Ann Example runs the pilot team.'})
        added = app.action('graph_fact_add', {'node_id': ANN, 'text': '  Ann Example runs   the pilot team. '}, owner_dashboard=True)
        self.assertEqual(self.about(added['id']), [(added['id'], ANN, 'owner', 0)])
        with self.store.connect() as db:
            row = db.execute('SELECT text,kind,kept_at IS NOT NULL kept,source FROM facts WHERE id=?', (added['id'],)).fetchone()
            self.assertEqual(tuple(row), ('Ann Example runs the pilot team.', 'fact', 1, None))  # their own words: kept, never set aside
            page = a.graph.detail(db, ANN)['open']['known']
        self.assertEqual([f['text'] for f in page], ['Ann Example runs the pilot team.'])
        # the same text again ties the one already learned instead of saving it twice; also to a second record
        self.assertEqual(app.action('graph_fact_add', {'node_id': GLOBEX, 'text': 'ann example runs the pilot team.'}, owner_dashboard=True),
                         {'id': added['id'], 'about': [GLOBEX], 'duplicate': True})
        for bad in ({'node_id': 'email:nobody@nowhere.example', 'text': 'Someone we never met.'}, {'node_id': ANN, 'text': 'Hi'}):
            with self.assertRaises(ValueError):
                app.action('graph_fact_add', bad, owner_dashboard=True)
        # Not about them: while another record holds it, it only leaves this page; off the last one, a general fact again
        self.assertEqual(self.store.fact_unlink(added['id'], GLOBEX), {'unlinked': True, 'general': False})
        self.assertEqual(self.store.fact_unlink(added['id'], ANN), {'unlinked': True, 'general': True})
        general = {f['id']: f['about'] for f in self.store.snapshot([])['facts']}
        self.assertEqual(general[added['id']], [])
        # adding it again on the page brings back the link the owner removed: they said so themselves
        app.action('graph_fact_add', {'node_id': ANN, 'text': 'Ann Example runs the pilot team.'}, owner_dashboard=True)
        self.assertEqual(self.about(added['id']), [(added['id'], ANN, 'owner', 0), (added['id'], GLOBEX, 'owner', 1)])
        # a page lists every fact about the record, not just the few a prompt line reads
        for n in range(8):
            self.store.fact_add(ANN, f'Ann Example detail number {n}.')
        with self.store.connect() as db:
            self.assertEqual(len(a.graph.detail(db, ANN)['open']['known']), 9)
            self.assertEqual(len(a.graph.open_between(db, ANN)['known']), 6)

    def test_the_one_time_pass_ties_the_facts_already_there_and_one_undo_takes_it_back(self):
        self.node('li:lee-park-2', 'Lee Park')
        ann = self.old_fact('Ann Example wants invoices as a PDF.')
        org = self.old_fact('We pay Globex within 30 days.', self.other)
        shared = self.old_fact('Lee Park signs off on invoices.')           # two records have that name
        on_todo = self.old_fact('Lee Park reads mail in the morning.', self.other)  # one of them is on its own to-do
        both = self.old_fact('Ann Example introduced us to Globex.')
        plain = self.old_fact('Replies stay under five sentences.')
        kept = self.store.remember_fact('Prefers a call over a long mail.', 'owner-note', about=[LEE], quote='we stopped using them')['id']
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
            self.store.remember_fact(f'General fact number {i} about how the owner works with pilots.', 'owner-note', quote='we stopped using them')

    def prep(self, todo=None):
        memory = recall(self.app, 'preparation', {'todo': todo or self.todo}, 14000)
        return memory, memory.text('facts'), memory.text('records')

    def test_a_preparation_gets_the_facts_about_its_records_first_within_the_same_top(self):
        self.many()
        ann = self.store.remember_fact('Ann Example wants invoices as a PDF.', 'owner-note', quote='we stopped using them')['id']
        told = self.store.remember_fact('Prefers a call over a long mail.', 'owner-note', about=[ANN], quote='we stopped using them')['id']
        lee = self.store.remember_fact('Lee Park signs off on invoices.', 'owner-note', quote='we stopped using them')['id']
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
        self.store.remember_fact('Ann Example wants invoices as a PDF.', 'owner-note', quote='we stopped using them')
        self.store.remember_fact('We pay Globex within 30 days.', 'owner-note', quote='we stopped using them')

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
        ann = self.store.remember_fact('Ann Example wants invoices as a PDF.', 'owner-note', quote='we stopped using them')['id']
        memory = recall(self.app, 'review')
        text = memory.text('facts')
        self.assertIn(f'- [{ann}] Ann Example wants invoices as a PDF.', text)
        self.assertEqual([i.about for i in memory.picked()['fact']], [(ANN,)])


if __name__ == '__main__':
    unittest.main()
