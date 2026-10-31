"""Fixed where it came from (corrections.py, corrections_app.py): the owner says in a to-do's chat that something is
wrong ("she's not the CEO", "we don't use that template anymore", "he left the company"); the chat turn finds where it
came from and fixes it there, as the owner's word. Each fix shows in the chat as "Fixed: …" and under Recent changes,
with Undo; an undo puts back exactly what was there unless it changed since; a fixed note adds no rule on top later."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('corrections_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import corrections
import graph
import learning_loop

ROOT = Path(__file__).resolve().parent.parent
ANA = 'email:ana@acme.example'
SAM = 'email:sam@globex.example'


class Corrections(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': []}
        self.rebuilt = 0
        build = patch.object(a.App, 'graph_build', side_effect=lambda: setattr(self, 'rebuilt', self.rebuilt + 1))
        build.start()
        self.addCleanup(build.stop)
        stamp = a.now()
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) "
                       "VALUES('s1','s1','Reply to Ana about the proposal','','[]','[]','pending',?)", (stamp,))
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) "
                       "VALUES('s2','s2','Another to-do','','[]','[]','pending',?)", (stamp,))
            for decision, sid, note, source in (('d1', 's1', "she's not the CEO, she's Head of Sales", 'dashboard'),
                                                ('d2', 's1', "we don't use the Q3 template anymore", 'dashboard'),
                                                ('d3', 's2', 'unrelated', 'dashboard'), ('d4', 's1', 'model text', 'agent')):
                db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                           (decision, sid, 'other', note, source, stamp))
            self.rule = db.execute("INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind) "
                                   "VALUES('Proposals use the Q3 template.','d3','s2',?,'draft')", (stamp,)).lastrowid
            for node, name, role in ((ANA, 'Ana Silva', 'CEO'), (SAM, 'Sam Lee', None)):
                info = {'identifiers': [node], 'role': role, 'role_by': 'review' if role else None, 'role_id': node if role else None,
                        'profile': {'title': 'Chief Executive', 'sources': {'title': {'from': 'a look-up'}}}, 'org': 'org:acme.example'}
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,'person',?,0.6,?,3,?)",
                           (node, name, stamp, json.dumps(info)))
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES('org:acme.example','org','Acme',0.5,?,3,'{}')", (stamp,))
            db.execute("INSERT INTO person_roles(identifier,role,source,created_at,quote,checked_at) VALUES(?,'CEO','review',?,'Ana Silva, CEO',?)",
                       (ANA, stamp, stamp))
            board = graph.board_row(db, 'Sales', ['Lead', 'Proposal', 'Signed'], 'owner', stamp)
            self.project = db.execute("INSERT INTO projects(name,created_at,board_id,stage,stage_by,stage_reason,stage_at) "
                                      "VALUES('Acme deal',?,?,'Signed','review','Ana signed the order form',?)", (stamp, board['id'], stamp)).lastrowid

    def fix(self, **args):
        return self.app.action('fix_source', {'suggestion_id': 's1', 'decision_id': 'd1', **args})

    def chat(self):
        with self.store.connect() as db:
            return corrections.chat_items(db, 's1')

    def undo(self, change_id):
        return self.app.action('learning_undo', {'id': change_id}, owner_dashboard=True)

    def test_sources_say_where_each_thing_came_from(self):
        found = self.app.action('correction_sources', {'suggestion_id': 's1', 'words': 'Q3 template', 'node_ids': [ANA, 'project:' + str(self.project)]})
        ana = found['people'][0]
        self.assertEqual(ana['role']['value'], 'CEO')
        self.assertIn('a review', ana['role']['came_from'])
        self.assertIn('Ana Silva, CEO', ana['role']['came_from'])
        self.assertEqual(ana['role']['fix'], {'kind': 'role', 'target': ANA})
        self.assertEqual(ana['org']['value'], 'Acme')
        self.assertEqual(ana['title']['came_from'], 'a look-up')
        self.assertEqual(found['projects'][0]['stage']['value'], 'Signed')
        self.assertEqual([f['id'] for f in found['facts']], [self.rule])
        self.assertEqual(found['facts'][0]['what'], 'rule')
        self.assertEqual(found['to_do']['fix'], {'kind': 'project', 'target': 's1'})

    def test_a_wrong_role_is_fixed_at_the_source_shown_in_the_chat_and_undone(self):
        done = self.fix(kind='role', target=ANA, value='Head of Sales', came_from='her email signature')
        self.assertEqual(done['fixed'], 'Ana Silva’s role is Head of Sales')
        self.assertEqual(self.rebuilt, 1)
        with self.store.connect() as db:
            role = db.execute('SELECT role,source FROM person_roles WHERE identifier=?', (ANA,)).fetchone()
            self.assertEqual(tuple(role), ('Head of Sales', 'owner'))  # the owner's word: a later review keeps it
            self.assertEqual(graph.set_role(db, ANA, 'CEO', 'review', a.now()).get('kept'), 'The owner set this role; it stays.')
            self.assertEqual([tuple(r) for r in db.execute('SELECT old_role,new_role FROM role_corrections')], [('CEO', 'Head of Sales')])
        line = self.chat()
        self.assertEqual(line[0]['line'], ['{}’s role is {}', 'Ana Silva', 'Head of Sales'])
        self.assertEqual(line[0]['from'], 'her email signature')
        self.assertFalse(line[0]['undone'])
        recent = self.store.snapshot([])['learning_changes']
        self.assertEqual(recent[0]['kind'], 'source')
        self.assertEqual(recent[0]['before'], 'CEO')

        self.undo(done['id'])
        self.assertEqual(self.rebuilt, 2)
        with self.store.connect() as db:
            self.assertEqual(tuple(db.execute('SELECT role,source,quote FROM person_roles WHERE identifier=?', (ANA,)).fetchone()),
                             ('CEO', 'review', 'Ana Silva, CEO'))
            self.assertEqual(db.execute('SELECT count(*) FROM role_corrections').fetchone()[0], 0)
        self.assertTrue(self.chat()[0]['undone'])
        with self.assertRaisesRegex(ValueError, 'already undone'):
            self.undo(done['id'])

    def test_an_undo_never_overwrites_what_the_owner_changed_since(self):
        done = self.fix(kind='role', target=ANA, value='Head of Sales')
        with self.store.connect() as db:
            graph.set_role(db, ANA, 'VP Sales', 'owner', a.now())
        with self.assertRaisesRegex(ValueError, 'changed since'):
            self.undo(done['id'])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT role FROM person_roles WHERE identifier=?', (ANA,)).fetchone()[0], 'VP Sales')

    def test_an_undo_puts_back_only_real_columns_never_stored_sql(self):
        done = self.fix(kind='role', target=ANA, value='Head of Sales')
        with self.store.connect() as db:
            before = json.loads(db.execute('SELECT before FROM learning_changes WHERE id=?', (done['id'],)).fetchone()[0])
            before['state']['rows'] = [{'identifier': ANA, 'role) VALUES(1);DROP TABLE facts;--': 'x'}]
            db.execute('UPDATE learning_changes SET before=? WHERE id=?', (json.dumps(before), done['id']))
        with self.assertRaisesRegex(ValueError, 'Not a table a fix puts back'):
            self.undo(done['id'])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT role FROM person_roles WHERE identifier=?', (ANA,)).fetchone()[0], 'Head of Sales')
            self.assertEqual(db.execute('SELECT count(*) FROM facts').fetchone()[0], 1)
            for table in ('facts', 'person_roles'):
                with self.assertRaisesRegex(ValueError, 'Not a table a fix puts back'):
                    graph.put_back_person_rows(db, table if table == 'facts' else 'person_roles', [ANA],
                                               [{'identifier': ANA}] if table == 'facts' else [{'nope': 1}])

    def test_a_rule_the_owner_says_is_wrong_is_removed_and_comes_back_on_undo(self):
        done = self.fix(decision_id='d2', kind='fact', target=self.rule, value='', came_from='a note on another to-do')
        with self.store.connect() as db:
            self.assertIsNotNone(db.execute('SELECT removed_at FROM facts WHERE id=?', (self.rule,)).fetchone()[0])
        self.assertEqual(self.chat()[0]['line'], ['Removed “{}” from what I’ve learned', 'Proposals use the Q3 template.'])
        self.assertEqual(self.rebuilt, 0)  # nothing in the Graph changed
        self.undo(done['id'])
        with self.store.connect() as db:
            self.assertIsNone(db.execute('SELECT removed_at FROM facts WHERE id=?', (self.rule,)).fetchone()[0])

    def test_a_reworded_fact_shows_itself(self):
        done = self.fix(decision_id='d2', kind='fact', target=self.rule, value='Proposals use the Q4 template.')
        self.assertEqual(done['fixed'], 'Proposals use the Q4 template.')
        self.assertIsNone(self.chat()[0]['line'])
        self.undo(done['id'])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT text FROM facts WHERE id=?', (self.rule,)).fetchone()[0], 'Proposals use the Q3 template.')

    def test_someone_who_left_and_a_wrong_title_and_stage(self):
        left = self.fix(kind='org', target=ANA, value='', came_from='an old signature')
        self.assertEqual(left['fixed'], 'Ana Silva no longer works at Acme')
        title = self.fix(kind='title', target=ANA, value='Head of Sales')
        stage = self.fix(kind='stage', target='project:' + str(self.project), value='Proposal', came_from='a review')
        self.assertEqual(stage['fixed'], 'Acme deal moved to Proposal')
        with self.store.connect() as db:
            self.assertEqual(tuple(db.execute('SELECT org,source FROM person_orgs WHERE identifier=?', (ANA,)).fetchone()), ('', 'owner'))
            self.assertEqual(graph.person_edits_for(db, [ANA])['title'], 'Head of Sales')
            self.assertEqual(tuple(db.execute('SELECT stage,stage_by FROM projects WHERE id=?', (self.project,)).fetchone()), ('Proposal', 'owner'))
        for change in (stage, title, left):
            self.undo(change['id'])
        with self.store.connect() as db:
            self.assertIsNone(db.execute('SELECT 1 FROM person_orgs WHERE identifier=?', (ANA,)).fetchone())
            self.assertEqual(graph.person_edits_for(db, [ANA]), {})
            self.assertEqual(tuple(db.execute('SELECT stage,stage_by,stage_reason FROM projects WHERE id=?', (self.project,)).fetchone()),
                             ('Signed', 'review', 'Ana signed the order form'))
            self.assertEqual(db.execute('SELECT count(*) FROM project_moves').fetchone()[0], 0)

    def test_the_to_dos_project(self):
        done = self.fix(kind='project', target='s1', value='Acme deal')
        self.assertEqual(done['fixed'], 'Moved this to-do to Acme deal')
        self.undo(done['id'])
        with self.store.connect() as db:
            self.assertEqual(tuple(db.execute('SELECT project,project_by FROM suggestions WHERE id=?', ('s1',)).fetchone()), (None, None))

    def test_only_from_the_owners_own_note_on_this_to_do(self):
        for decision in ('d3', 'd4', 'nope'):  # another to-do's note, a model's text, none
            with self.assertRaisesRegex(ValueError, "owner's own note"):
                self.fix(decision_id=decision, kind='role', target=ANA, value='Head of Sales')
        with self.assertRaisesRegex(ValueError, 'kind is where'):
            self.fix(kind='enrichment', target=ANA, value='x')
        with self.assertRaises(ValueError):
            self.app.action('learning_undo', {'id': 1})  # Undo is the owner's, on the dashboard
        self.assertEqual(self.fix(kind='role', target=SAM, value=''), {'unchanged': True})

    def test_a_note_fixed_at_the_source_is_no_signal_for_the_learning_loop(self):
        with self.store.connect() as db:
            before = [s['to_do'] for s in learning_loop.signals(db, '2000-01-01') if s['what'] == 'corrected in chat']
        self.fix(kind='role', target=ANA, value='Head of Sales')
        with self.store.connect() as db:
            after = [s['to_do'] for s in learning_loop.signals(db, '2000-01-01') if s['what'] == 'corrected in chat']
        self.assertEqual(len(before) - len(after), 1)

    def test_the_turns_are_told_and_the_tools_are_there(self):
        prompt = a.chat_prompt({'job_id': 'j' * 32, 'suggestion_id': 's1'}, {})
        self.assertIn('correction_sources', prompt)
        self.assertIn('fix_source', prompt)
        self.assertIn('stays theirs', corrections.PROMPT)  # the owner's own text on a GBrain page
        plugin = (ROOT / 'openclaw-plugin' / 'index.ts').read_text()
        self.assertIn("'correction_sources', 'fix_source'", plugin)
        self.assertNotIn('fix_source', a.DASHBOARD_ACTIONS)  # the agent's call, never the page's
        self.assertEqual(set(a.CorrectionsApp.ACTIONS), {'correction_sources', 'fix_source'})


if __name__ == '__main__':
    unittest.main()
