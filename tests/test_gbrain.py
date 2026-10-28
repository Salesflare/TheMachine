"""GBrain (gbrain.py): optional and off by default; on only after the owner agreed. Sync both ways, idempotent, never
over the owner's own edits, within the Work/Personal and Team Graph boundaries, never message text."""
import datetime as dt
import json
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import gbrain
import graph
from test_assistant import assistant as a

ON = {'on': True, 'consent_at': '2026-10-28T08:00:00+00:00', 'linked': 'machine'}
SECRET_BODY = 'The quarterly numbers are confidential: 4.2M'


class FakeBrain:
    """GBrain's CLI as `gbrain call` answers it (checked against GBrain 0.60): get_page {content, revision}, put_page
    with a revision check (an existing page needs expected_revision), whois matches, list_pages a bare array."""
    def __init__(self):
        self.pages, self.calls, self.clock = {}, [], 0

    def page(self, slug, content):
        self.clock += 1
        self.pages[slug] = {'content': content, 'revision': f'r{self.clock}', 'updated': dt.datetime.now(dt.timezone.utc).isoformat()}

    def __call__(self, tool, params):
        self.calls.append((tool, json.loads(json.dumps(params))))
        if tool == 'get_page':
            p = self.pages.get(params['slug'])
            return {'slug': params['slug'], 'content': p['content'], 'revision': p['revision']} if p else None
        if tool == 'put_page':
            p = self.pages.get(params['slug'])
            if p and params.get('expected_revision') != p['revision']:
                raise gbrain.Conflict('revision_conflict' if params.get('expected_revision') else 'revision_required')
            self.page(params['slug'], params['content'])
            return {'slug': params['slug'], 'revision': self.pages[params['slug']]['revision'], 'status': 'created_or_updated'}
        if tool == 'whois':
            q = params['query'].lower()
            return {'matches': [{'slug': s, 'type': 'person'} for s, p in self.pages.items()
                                if s.startswith('people/') and (f'email: {q}' in p['content'].lower() or f'# {q}\n' in p['content'].lower())]}
        if tool == 'list_pages':
            return [{'slug': s, 'updated_at': p['updated']} for s, p in self.pages.items()
                    if s.startswith(params['slug_prefix']) and p['updated'] > params.get('updated_after', '')]
        raise AssertionError('unexpected call ' + tool)

    def writes(self):
        return [c for c in self.calls if c[0] == 'put_page']


def node(db, node_id, kind, name, strength=2.0, **info):
    db.execute('INSERT OR REPLACE INTO graph_nodes(id,kind,name,strength,last_at,signals,gap_days,quiet,trend,info) VALUES(?,?,?,?,?,?,?,?,?,?)',
               (node_id, kind, name, strength, '2026-10-20', 5, None, 0, None, json.dumps(info)))


def link(db, x, y, kind='project'):
    db.execute('INSERT OR REPLACE INTO graph_links(a,b,kind,strength,last_at) VALUES(?,?,?,?,?)', (x, y, kind, 1.0, '2026-10-20'))


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = sqlite3.connect(Path(self.tmp.name) / 'db.sqlite')
        self.db.row_factory = sqlite3.Row
        graph.ensure(self.db)
        self.db.execute('CREATE TABLE IF NOT EXISTS facts(id INTEGER PRIMARY KEY,text TEXT NOT NULL,decision_id TEXT NOT NULL,suggestion_id TEXT,'
                        'created_at TEXT NOT NULL,removed_at TEXT,merged_into TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,kind TEXT,subject TEXT,body TEXT)')
        self.db.execute('INSERT INTO events(id,kind,subject,body) VALUES(1,?,?,?)', ('gmail.message', 'Q3 numbers', SECRET_BODY))
        node(self.db, 'email:sis@example.org', 'person', 'Robin Lee', side='personal', emails=['sis@example.org'], role='sister',
             notes='Likes hiking')
        node(self.db, 'email:buyer@acme.test', 'person', 'Casey Buyer', side='work', org='org:acme.test', role='customer',
             emails=['buyer@acme.test'], profile={'title': 'Head of Ops'})
        node(self.db, 'email:mate@acme.test', 'person', 'Teammate Record', side='work', owner='fm_mate', owner_name='Mate')
        node(self.db, 'email:cc@example.org', 'person', 'Only Seen', side='personal', seen_only=True)
        node(self.db, 'email:faint@example.org', 'person', 'Faint Person', strength=0.1, side='personal')
        node(self.db, 'email:unknown@example.org', 'person', 'Unknown Side')
        node(self.db, 'org:acme.test', 'org', 'Acme', domain='acme.test', role='customer')
        self.db.execute("INSERT INTO projects(id,name,created_at) VALUES(1,'Garden','2026-10-01'),(2,'Acme rollout','2026-10-01')")
        self.db.execute('UPDATE projects SET board_id=7 WHERE id=2')
        node(self.db, 'project:1', 'project', 'Garden')
        node(self.db, 'project:2', 'project', 'Acme rollout')
        link(self.db, 'email:sis@example.org', 'project:1')
        link(self.db, 'email:buyer@acme.test', 'project:2')
        link(self.db, 'email:buyer@acme.test', 'org:acme.test', 'org')
        self.db.execute("INSERT INTO facts(text,decision_id,created_at) VALUES('Invoices go to the shared inbox','d1','2026-10-01')")
        self.db.execute("INSERT INTO facts(text,decision_id,created_at,removed_at) VALUES('A removed rule','d2','2026-10-01','2026-10-02')")
        self.db.commit()
        self.brain = FakeBrain()
        self.config = {'gbrain': dict(ON), 'dashboard_host': 'machine.example.test', 'dashboard_path': '/'}

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def all_text(self):
        return '\n'.join(p['content'] for p in self.brain.pages.values())


class OffByDefault(Base):
    def test_nothing_happens_without_the_owner_turning_it_on_and_agreeing(self):
        for config in ({}, {'gbrain': {}}, {'gbrain': {'on': True}}, {'gbrain': {'on': False, 'consent_at': 'x'}}, {'gbrain': 'on'}):
            self.assertFalse(gbrain.on(config))
            self.assertIsNone(gbrain.sync(self.db, config, self.brain))
        self.assertEqual(self.brain.calls, [])
        self.assertTrue(gbrain.on({'gbrain': ON}))

    def test_the_service_starts_no_sync_thread_while_off(self):
        app = object.__new__(a.App)
        app.config, app.stop = {}, None
        with patch.object(a.threading, 'Thread') as thread:
            self.assertFalse(app.gbrain_start())
        thread.assert_not_called()


class Boundaries(Base):
    def test_personal_only_by_default(self):
        names = {r['name'] for r in gbrain.records(self.db, self.config)}
        self.assertEqual(names, {'Robin Lee', 'Garden'})

    def test_work_too_when_turned_on_but_never_a_teammates_record(self):
        self.config['gbrain']['work'] = True
        names = {r['name'] for r in gbrain.records(self.db, self.config)}
        self.assertEqual(names, {'Robin Lee', 'Garden', 'Casey Buyer', 'Acme', 'Acme rollout'})
        self.assertNotIn('Teammate Record', names)  # a teammate owns it (Work Fleet)
        self.assertNotIn('Only Seen', names)
        self.assertNotIn('Unknown Side', names)     # unknown counts as Work-ish: never in a Personal brain

    def test_never_message_text_nor_team_tables(self):
        self.config['gbrain']['work'] = True
        self.db.execute('CREATE TABLE IF NOT EXISTS team_records(fleet TEXT,member TEXT,rid TEXT,kind TEXT,body TEXT,at TEXT)')
        self.db.execute("INSERT INTO team_records VALUES('f','m','r','person','{\"name\":\"Shared Teammate Contact\"}','x')")
        traced = []
        self.db.set_trace_callback(traced.append)
        while gbrain.push(self.db, self.config, self.brain)['left']:
            pass
        self.db.set_trace_callback(None)
        text = self.all_text()
        self.assertNotIn(SECRET_BODY, text)
        self.assertNotIn('Q3 numbers', text)
        self.assertNotIn('Shared Teammate Contact', text)
        self.assertFalse([q for q in traced if 'team_' in q or 'FROM events' in q])
        self.assertIn('Casey Buyer', text)

    def test_turning_work_off_takes_the_machines_part_off_those_pages(self):
        self.config['gbrain']['work'] = True
        gbrain.push(self.db, self.config, self.brain)
        page = self.brain.pages['people/casey-buyer']['content']
        self.assertIn(gbrain.MARK_START, page)
        self.brain.page('people/casey-buyer', page + '\nMy own line about Casey.\n')
        self.config['gbrain']['work'] = False
        done = gbrain.push(self.db, self.config, self.brain)
        self.assertGreaterEqual(done['withdrawn'], 1)
        page = self.brain.pages['people/casey-buyer']['content']
        self.assertNotIn(gbrain.MARK_START, page)
        self.assertIn('My own line about Casey.', page)  # the owner's text stays
        self.assertIn('people/robin-lee', self.brain.pages)


class Sync(Base):
    def test_pages_with_a_marked_section_and_a_link_back(self):
        gbrain.push(self.db, self.config, self.brain)
        page = self.brain.pages['people/robin-lee']['content']
        self.assertTrue(page.startswith('---\ntype: "person"'))
        self.assertIn('email: "sis@example.org"', page)
        self.assertIn('- Role: sister', page)
        self.assertIn('- Notes: Likes hiking', page)
        self.assertIn('[[projects/garden|Garden]]', page)
        self.assertIn('(https://machine.example.test/#graph/email%3Asis%40example.org)', page)
        self.assertIn('Written by The Machine', page)
        learned = self.brain.pages[gbrain.LEARNINGS_SLUG]['content']
        self.assertIn('Invoices go to the shared inbox', learned)
        self.assertNotIn('A removed rule', learned)

    def test_a_second_round_with_nothing_new_makes_no_call(self):
        gbrain.push(self.db, self.config, self.brain)
        self.brain.calls.clear()
        self.assertEqual(gbrain.push(self.db, self.config, self.brain), {'wrote': 0, 'kept': 0, 'withdrawn': 0, 'conflicts': 0, 'left': 0})
        self.assertEqual(self.brain.calls, [])
        # a change goes as one new write of that page only
        node(self.db, 'email:sis@example.org', 'person', 'Robin Lee', side='personal', emails=['sis@example.org'], role='sister', notes='Likes climbing')
        gbrain.push(self.db, self.config, self.brain)
        self.assertEqual([c[1]['slug'] for c in self.brain.writes()], ['people/robin-lee'])
        self.assertIn('Likes climbing', self.brain.pages['people/robin-lee']['content'])

    def test_the_owners_text_on_a_page_is_never_overwritten(self):
        self.brain.page('people/robin', '---\ntype: person\nemail: sis@example.org\n---\n\n# Robin\n\nMet at the lake. Allergic to cats.\n')
        gbrain.push(self.db, self.config, self.brain)
        self.assertNotIn('people/robin-lee', self.brain.pages)  # whois found their page: no second one
        page = self.brain.pages['people/robin']['content']
        self.assertTrue(page.startswith('---\ntype: person\nemail: sis@example.org\n---\n\n# Robin\n\nMet at the lake. Allergic to cats.\n'))
        self.assertIn(gbrain.MARK_START, page)
        # The owner edits their part meanwhile: the next write keeps it (revision checked)
        self.brain.page('people/robin', page.replace('Allergic to cats.', 'Allergic to cats and dogs.'))
        node(self.db, 'email:sis@example.org', 'person', 'Robin Lee', side='personal', emails=['sis@example.org'], role='sister', notes='New note')
        gbrain.push(self.db, self.config, self.brain)
        page = self.brain.pages['people/robin']['content']
        self.assertIn('Allergic to cats and dogs.', page)
        self.assertIn('New note', page)

    def test_an_edited_machine_section_is_left_as_the_owner_made_it(self):
        gbrain.push(self.db, self.config, self.brain)
        page = self.brain.pages['people/robin-lee']['content']
        self.brain.page('people/robin-lee', page.replace('- Role: sister', '- Role: sister (and best friend)'))
        node(self.db, 'email:sis@example.org', 'person', 'Robin Lee', side='personal', emails=['sis@example.org'], role='sibling')
        done = gbrain.push(self.db, self.config, self.brain)
        self.assertEqual(done['kept'], 1)
        self.assertIn('(and best friend)', self.brain.pages['people/robin-lee']['content'])
        self.assertNotIn('sibling', self.brain.pages['people/robin-lee']['content'])
        self.brain.calls.clear()
        gbrain.push(self.db, self.config, self.brain)
        self.assertEqual(self.brain.writes(), [])
        self.assertEqual(gbrain.counts(self.db)['kept'], 1)

    def test_a_deleted_page_is_not_made_again(self):
        gbrain.push(self.db, self.config, self.brain)
        del self.brain.pages['people/robin-lee']
        node(self.db, 'email:sis@example.org', 'person', 'Robin Lee', side='personal', emails=['sis@example.org'], role='friend')
        gbrain.push(self.db, self.config, self.brain)
        self.assertNotIn('people/robin-lee', self.brain.pages)

    def test_a_conflict_waits_for_the_next_round(self):
        gbrain.push(self.db, self.config, self.brain)
        node(self.db, 'email:sis@example.org', 'person', 'Robin Lee', side='personal', emails=['sis@example.org'], role='friend')
        real = self.brain.__call__

        def racing(tool, params):
            if tool == 'put_page':
                raise gbrain.Conflict('revision_conflict')
            return real(tool, params)
        self.assertEqual(gbrain.push(self.db, self.config, racing)['conflicts'], 1)
        self.assertNotIn('friend', self.brain.pages['people/robin-lee']['content'])
        gbrain.push(self.db, self.config, self.brain)
        self.assertIn('- Role: friend', self.brain.pages['people/robin-lee']['content'])

    def test_a_big_graph_goes_in_over_a_few_rounds(self):
        for i in range(40):
            node(self.db, f'email:p{i}@example.org', 'person', f'Person {i}', side='personal')
        first = gbrain.push(self.db, self.config, self.brain, limit=10)
        self.assertEqual(len(self.brain.writes()), 10)
        self.assertGreater(first['left'], 0)
        while gbrain.push(self.db, self.config, self.brain, limit=10)['left']:
            pass
        self.assertEqual(len([s for s in self.brain.pages if s.startswith('people/person-')]), 40)

    def test_what_the_owner_wrote_comes_back_for_reviews(self):
        gbrain.push(self.db, self.config, self.brain)
        self.assertEqual(gbrain.pull(self.db, self.brain), 2)  # the first pull reads every page that went in
        self.assertEqual(gbrain.notes(self.db, ['email:sis@example.org']), {})  # nothing of the owner's yet
        page = self.brain.pages['people/robin-lee']['content']
        self.brain.page('people/robin-lee', page.replace('# Robin Lee\n', '# Robin Lee\n\nMoving to Lisbon in March.\n'))
        self.brain.calls.clear()
        self.assertEqual(gbrain.pull(self.db, self.brain), 1)  # only what changed since
        self.assertEqual(gbrain.notes(self.db, ['email:sis@example.org']), {'email:sis@example.org': 'Moving to Lisbon in March.'})
        self.assertNotIn('the-machine', ' '.join(c[1].get('slug', '') for c in self.brain.calls))

    def test_sync_records_errors_and_turning_off_forgets_what_came_back(self):
        gbrain.sync(self.db, self.config, self.brain)
        self.db.execute("INSERT INTO gbrain_notes(node_id,slug,text,at) VALUES('email:sis@example.org','people/robin-lee','x','y')")

        def broken(tool, params):
            raise gbrain.BrainError('not_installed')
        node(self.db, 'email:sis@example.org', 'person', 'Robin Lee', side='personal', role='friend')
        with self.assertRaises(gbrain.BrainError):
            gbrain.sync(self.db, self.config, broken)
        self.assertEqual(gbrain.counts(self.db)['last_error'], 'not_installed')
        gbrain.forget(self.db)
        self.assertEqual(gbrain.notes(self.db, ['email:sis@example.org']), {})
        self.assertIn('people/robin-lee', self.brain.pages)  # the brain keeps its pages


class Cli(unittest.TestCase):
    def test_answers_as_gbrain_gives_them(self):
        self.assertEqual(gbrain.answer(0, '{"slug":"a","revision":"r1"}'), {'slug': 'a', 'revision': 'r1'})
        self.assertIsNone(gbrain.answer(1, '{"code":"page_not_found","message":"Page not found: a"}'))
        for code in ('revision_conflict', 'revision_required'):
            with self.assertRaises(gbrain.Conflict):
                gbrain.answer(1, json.dumps({'code': code, 'error': code}))
        with self.assertRaises(gbrain.Conflict):
            gbrain.answer(10, '{"code":"write_pending"}')
        with self.assertRaises(gbrain.BrainError):
            gbrain.answer(1, '', 'boom')
        self.assertEqual(gbrain.answer(0, '[{"slug":"a"}]'), [{'slug': 'a'}])

    def test_link_and_unlink_through_openclaw(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        binary = Path(tmp.name) / 'gbrain'
        binary.write_text('#!/bin/sh\n')
        binary.chmod(0o755)
        runs, servers = [], {}

        def run(argv, **kw):
            runs.append(argv[1:])
            if argv[1:3] == ['mcp', 'show']:
                return subprocess.CompletedProcess(argv, 0 if 'gbrain' in servers else 1, json.dumps(servers.get('gbrain', {'error': 'none'})), '')
            if argv[1:3] == ['plugins', 'inspect']:
                return subprocess.CompletedProcess(argv, 1, '', 'not found')
            if argv[1:3] == ['mcp', 'add']:
                servers['gbrain'] = {'command': argv[argv.index('--command') + 1]}
                return subprocess.CompletedProcess(argv, 0, '', '')
            if argv[1:3] == ['mcp', 'unset']:
                servers.pop('gbrain')
                return subprocess.CompletedProcess(argv, 0, '', '')
            raise AssertionError(argv)
        env = {'HOME': tmp.name, 'GBRAIN_BIN': str(binary)}
        brain = gbrain.Brain({'openclaw': 'openclaw'}, run=run, which=lambda _: None, environ=env)
        self.assertEqual(brain.link(), 'machine')
        add = next(r for r in runs if r[:2] == ['mcp', 'add'])
        self.assertEqual(add[add.index('--include') + 1].split(','), list(gbrain.READ_TOOLS))  # read tools only
        self.assertIn('--no-probe', add)
        self.assertEqual(brain.brain_path(), str(Path(tmp.name) / '.gbrain'))
        # Already there (the owner's own, or GBrain's plugin): used as it is, and never removed
        self.assertEqual(brain.link(), 'existing')
        self.assertFalse(gbrain.Brain({'gbrain': {'linked': 'existing'}}, run=run, which=lambda _: None, environ=env).unlink())
        self.assertIn('gbrain', servers)
        self.assertTrue(gbrain.Brain({'gbrain': {'linked': 'machine', 'bin': str(binary)}}, run=run, which=lambda _: None, environ=env).unlink())
        self.assertNotIn('gbrain', servers)


class Dashboard(unittest.TestCase):
    """The owner's switch: consent first, then on; off again keeps the brain."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'config.json'
        self.path.write_text(json.dumps({'database': 'x', 'accounts': []}))
        self.app = object.__new__(a.App)
        self.app.config_path, self.app.config = self.path, json.loads(self.path.read_text())
        self.app.store = a.Store(str(Path(self.tmp.name) / 'db.sqlite'))
        self.binary = Path(self.tmp.name) / 'gbrain'
        self.binary.write_text('#!/bin/sh\n')
        self.binary.chmod(0o755)

    def tearDown(self):
        self.tmp.cleanup()

    def test_off_by_default_and_only_the_owner(self):
        with patch.object(gbrain.Brain, 'binary', return_value=None):
            view = self.app.action('gbrain_status', {}, owner_dashboard=True)
        self.assertEqual((view['on'], view['installed']), (False, False))
        for name in ('gbrain_status', 'gbrain_on', 'gbrain_off', 'gbrain_work'):
            self.assertIn(name, a.DASHBOARD_ACTIONS)
            with self.assertRaises(ValueError):
                self.app.action(name, {'consent': True})  # not from the dashboard: the agent can't turn it on

    def test_consent_first_then_on_then_off(self):
        started = []
        with patch.object(gbrain.Brain, 'binary', return_value=str(self.binary)), patch.object(gbrain.Brain, 'version', return_value='0.60.479.0'), \
                patch.object(gbrain.Brain, 'link', return_value='machine') as linked, patch.object(gbrain.Brain, 'unlink', return_value=True) as unlinked, \
                patch.object(a.App, 'gbrain_start', lambda app: started.append(1)):
            for args in ({}, {'consent': 'yes'}, {'consent': False}):
                with self.assertRaises(ValueError):
                    self.app.action('gbrain_on', args, owner_dashboard=True)
            linked.assert_not_called()
            self.assertNotIn('gbrain', json.loads(self.path.read_text()))
            view = self.app.action('gbrain_on', {'consent': True}, owner_dashboard=True)
            self.assertTrue(view['on'])
            self.assertEqual(view['version'], '0.60.479.0')
            saved = json.loads(self.path.read_text())['gbrain']
            self.assertEqual((saved['on'], saved['work'], saved['linked'], saved['bin']), (True, False, 'machine', str(self.binary)))
            self.assertTrue(saved['consent_at'])
            self.assertEqual(started, [1])
            self.assertTrue(self.app.action('gbrain_work', {'on': True}, owner_dashboard=True)['work'])
            view = self.app.action('gbrain_off', {}, owner_dashboard=True)
            unlinked.assert_called_once()
        self.assertFalse(view['on'])
        self.assertEqual(json.loads(self.path.read_text())['gbrain'], {'on': False})
        self.assertFalse(gbrain.on(self.app.config))

    def test_not_installed(self):
        with patch.object(gbrain.Brain, 'binary', return_value=None):
            with self.assertRaisesRegex(ValueError, 'Install GBrain'):
                self.app.action('gbrain_on', {'consent': True}, owner_dashboard=True)


class Catchup(Base):
    def test_default_pull_drains_45_empty_pages_across_restart(self):
        for i in range(45):
            node(self.db, f'email:batch{i}@example.org', 'person', f'Batch Person {i}', side='personal')
        while gbrain.push(self.db, self.config, self.brain, limit=40)['left']:
            pass
        total = self.db.execute("SELECT count(*) FROM gbrain_pages WHERE node_id!='the-machine:learnings'").fetchone()[0]
        self.assertGreater(total, 40)
        self.assertEqual(gbrain.pull(self.db, self.brain), 40)
        self.assertIsNone(gbrain.meta(self.db, 'pulled_at'))
        self.db.commit()
        self.db.close()
        self.db = sqlite3.connect(Path(self.tmp.name) / 'db.sqlite')
        self.db.row_factory = sqlite3.Row
        self.assertEqual(gbrain.pull(self.db, self.brain), total - 40)
        self.assertIsNotNone(gbrain.meta(self.db, 'pulled_at'))
        self.assertIsNone(gbrain.meta(self.db, 'pull_pending'))


if __name__ == '__main__':
    unittest.main()
