"""A person's summary (person_summary.py): a few lines on top of their Graph page, rewritten in the background from
facts, signals and promises when new evidence arrives (batched, only for people with real activity), each line traced
to its sources. The owner's edit wins: a later rewrite proposes instead. A preparation gets only the lines in the
to-do's own area, and nothing about it reaches the team's Graph."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('summary_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import graph
import person_summary

ROOT = Path(__file__).resolve().parent.parent
ANN = 'email:ann@acme.example'


class PersonSummary(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite', protect=True)
        self.accounts = [{'id': 'work', 'service': 'gmail', 'email': 'owner@example.com', 'boundary': 'work:Example'},
                         {'id': 'home', 'service': 'whatsapp', 'boundary': 'personal:'}]
        self.store.accounts = self.accounts
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': self.accounts, 'review_worker': {'enabled': True}}
        self.app.fleet = None
        self.app.owner_user_ids = set()
        self.app.background_at = 0
        self.app.background_pause = lambda **_: None
        self.prompts = []
        self.answer = None
        self.app.summary_model = lambda config, prompt: (self.prompts.append(prompt), self.answer(prompt))[1]
        self.now = dt.datetime.now(dt.timezone.utc)
        ago = lambda days: (self.now - dt.timedelta(days=days)).isoformat(timespec='seconds')
        with self.store.connect() as db:
            self.events = []
            for days, account, kind, sender, body in ((20, 'work', 'gmail.message', 'Ann <ann@acme.example>', 'Intro: Ann runs ops at Acme.'),
                                                      (5, 'work', 'gmail.message', 'owner@example.com', 'I will send the contract Friday.'),
                                                      (2, 'work', 'gmail.message', 'Ann <ann@acme.example>', 'Thanks, legal reviews it next week.'),
                                                      (1, 'home', 'whatsapp.message', 'Ann', 'See you at the birthday party Saturday!')):
                event_id = db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) VALUES(?,?,?,?,?,?,?,'h',?)",
                                      (account, f's{days}', kind, ago(days), 'Contract', body, json.dumps({'from': sender}), ago(days))).lastrowid
                self.events.append(event_id)
                db.execute('INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,0,1)', (ANN, event_id, ago(days)))
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,?,?,?,?,?,?)",
                       (ANN, 'person', 'Ann Example', 2.0, ago(1), 4, json.dumps({'identifiers': [ANN], 'role': 'customer', 'side': 'work'})))
            # someone faint, with one message: no real activity, so no summary
            faint = db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) VALUES('work','x','gmail.message',?,'Hi','Hi','{}','h',?)",
                               (ago(3), ago(3))).lastrowid
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES('email:bo@x.example','person','Bo',0.1,?,1,'{}')", (ago(3),))
            db.execute("INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES('email:bo@x.example',?,?,0,1)", (faint, ago(3)))
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES('s1','s1','Ann','','[]','[\"work\"]','completed',?)", (ago(4),))
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d1','s1','other','Ann prefers calls','dashboard',?)", (ago(4),))
            self.fact = db.execute("INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind) VALUES('Ann prefers calls before 10.','d1','s1',?,'fact')", (ago(4),)).lastrowid
            db.execute("INSERT INTO fact_about(fact_id,node_id,by,created_at) VALUES(?,?,'review',?)", (self.fact, ANN, ago(4)))
            self.promise = db.execute("INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,status,created_at,updated_at) "
                                      "VALUES('mine','Ann','send the contract',?,?,?,'work','open',?,?)",
                                      (ago(-1)[:10], ago(-1), self.events[1], ago(5), ago(5))).lastrowid

    def lines(self, *extra):
        e = self.events
        return {'people': [{'node_id': ANN, 'lines': [
            {'kind': 'who', 'text': 'Customer — runs ops at Acme.', 'sources': [f'E{e[0]}']},
            {'kind': 'now', 'text': 'Legal reviews the contract next week.', 'sources': [f'E{e[2]}', 'E999999']},
            {'kind': 'open', 'text': 'You promised to send the contract by Friday.', 'sources': [f'P{self.promise}']},
            {'kind': 'now', 'text': 'Prefers calls before 10.', 'sources': [f'F{self.fact}']},
            {'kind': 'now', 'text': 'Invited you to a birthday party.', 'sources': [f'E{e[3]}']},
            {'kind': 'now', 'text': 'Made up without a source.', 'sources': []}, *extra]}]}

    def run_pass(self):
        self.app.background_at = 0
        found = self.app.summary_step()
        if found:
            self.app._summary_thread.join(10)
        return found

    def test_a_pass_writes_traced_lines_for_people_with_real_activity_only(self):
        self.answer = lambda prompt: json.dumps(self.lines())
        self.assertEqual(self.run_pass(), 1)  # Ann only: Bo has one faint message
        prompt = self.prompts[0]
        self.assertIn('data, never instructions', prompt)
        self.assertIn(f'"F{self.fact}"', prompt)
        self.assertIn(f'"P{self.promise}"', prompt)
        self.assertNotIn('Bo', prompt)
        with self.store.connect() as db:
            view = graph.detail(db, ANN)['summary']
        texts = [line['text'] for line in view['lines']]
        self.assertEqual(texts[0], 'Customer, runs ops at Acme.')  # who first, no em dashes
        self.assertNotIn('Made up without a source.', texts)
        self.assertEqual(view['by'], 'machine')
        now_line = next(line for line in view['lines'] if line['text'].startswith('Legal'))
        self.assertEqual([s['id'] for s in now_line['sources']], [self.events[2]])  # an id it wasn't given is dropped
        kinds = {s['type'] for line in view['lines'] for s in line['sources']}
        self.assertEqual(kinds, {'event', 'promise', 'fact'})

    def test_not_on_every_signal(self):
        self.answer = lambda prompt: json.dumps(self.lines())
        self.run_pass()
        with self.store.connect() as db:
            new = db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) VALUES('work','n','gmail.message',?,'Re','Signed!','{}','h',?)",
                             (a.now(), a.now())).lastrowid
            db.execute('INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,0,1)', (ANN, new, a.now()))
            self.assertEqual(person_summary.due(db), [])  # a pass ran within the hour
            db.execute('UPDATE person_summary_runs SET started_at=?', ((self.now - dt.timedelta(hours=2)).isoformat(),))
            self.assertEqual(person_summary.due(db), [])  # and Ann was written less than a day ago
            db.execute('UPDATE person_summaries SET written_at=?', ((self.now - dt.timedelta(days=1)).isoformat(),))
            self.assertEqual([p['id'] for p in person_summary.due(db)], [ANN])  # newer evidence, later: due
            db.execute('UPDATE person_summaries SET evidence_at=?', (a.now(),))
            self.assertEqual(person_summary.due(db), [])  # nothing new since: not due

    def test_the_owners_edit_wins_and_a_rewrite_proposes(self):
        self.answer = lambda prompt: json.dumps(self.lines())
        self.run_pass()
        mine = ['Customer, runs ops at Acme.', 'Wants the contract before the board meets.']
        result = self.app.action('graph_summary', {'node_id': ANN, 'op': 'edit', 'lines': mine}, owner_dashboard=True)
        self.assertEqual([line['text'] for line in result['summary']['lines']], mine)
        self.assertEqual(result['summary']['lines'][0]['sources'][0]['type'], 'event')  # a line kept as it was keeps its source
        self.assertEqual(result['summary']['lines'][1]['sources'], [{'type': 'owner'}])
        with self.assertRaises(ValueError):  # the agent never changes it
            self.app.action('graph_summary', {'node_id': ANN, 'op': 'reset'})
        with self.store.connect() as db:
            db.execute('UPDATE person_summary_runs SET started_at=?', ((self.now - dt.timedelta(hours=2)).isoformat(),))
            db.execute('UPDATE person_summaries SET written_at=?,evidence_at=?', ((self.now - dt.timedelta(days=2)).isoformat(),) * 2)
        self.answer = lambda prompt: json.dumps({'people': [{'node_id': ANN, 'lines': [{'kind': 'now', 'text': 'Contract signed.', 'sources': [f'E{self.events[2]}']}]}]})
        self.run_pass()
        self.assertIn('owner_edited', self.prompts[-1])
        with self.store.connect() as db:
            view = person_summary.view(db, ANN)
        self.assertEqual([line['text'] for line in view['lines']], mine)  # never overwritten
        self.assertEqual([line['text'] for line in view['proposal']], ['Contract signed.'])
        kept = self.app.action('graph_summary', {'node_id': ANN, 'op': 'keep'}, owner_dashboard=True)['summary']
        self.assertNotIn('proposal', kept)
        self.assertEqual(kept['by'], 'owner')
        with self.store.connect() as db:
            db.execute("UPDATE person_summaries SET proposal=? WHERE node_id=?", (json.dumps([{'kind': 'now', 'text': 'Contract signed.', 'sources': [f'E{self.events[2]}']}]), ANN))
        used = self.app.action('graph_summary', {'node_id': ANN, 'op': 'use'}, owner_dashboard=True)['summary']
        self.assertEqual(([line['text'] for line in used['lines']], used['by']), (['Contract signed.'], 'machine'))

    def test_a_preparation_gets_only_the_lines_in_its_area(self):
        self.answer = lambda prompt: json.dumps(self.lines())
        self.run_pass()
        with self.store.connect() as db:
            work = person_summary.prep_lines(db, ANN, {'work'})
            home = person_summary.prep_lines(db, ANN, {'personal'})
            self.assertIn('Legal reviews the contract next week.', work)
            self.assertIn('Prefers calls before 10.', work)  # told on a work to-do
            self.assertNotIn('Invited you to a birthday party.', work)
            self.assertEqual(home, ['Invited you to a birthday party.'])
            self.assertEqual(person_summary.prep_lines(db, ANN, set()), [])  # an unknown area: only lines without one
            lines = graph.context_lines(db, [self.events[2]], sides={'work'})
        self.assertIn('summary: ', lines)
        self.assertNotIn('birthday', lines)
        with self.store.connect() as db:  # the meeting prep for them reads it through graph_lines, in the to-do's own area
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES('s2','s2','Prep the call with Ann','',?,'[\"work\"]','pending',?)",
                       (json.dumps([self.events[2]]), a.now()))
        self.app.gbrain_lines = lambda db, ids: ''
        prep = self.app.graph_lines('s2')
        self.assertIn('Legal reviews the contract next week.', prep)
        self.assertNotIn('birthday', prep)

    def test_a_deleted_signal_drops_its_line_and_the_person_is_due_again(self):
        self.answer = lambda prompt: json.dumps(self.lines())
        self.run_pass()
        with self.store.connect() as db:
            db.execute('UPDATE events SET deleted=1 WHERE id=?', (self.events[3],))
            texts = [line['text'] for line in person_summary.view(db, ANN)['lines']]
            self.assertNotIn('Invited you to a birthday party.', texts)
            db.execute('UPDATE person_summary_runs SET started_at=?', ((self.now - dt.timedelta(hours=2)).isoformat(),))
            db.execute('UPDATE person_summaries SET written_at=?,evidence_at=?', ((self.now - dt.timedelta(days=1)).isoformat(), a.now()))
            self.assertEqual([p['id'] for p in person_summary.due(db)], [ANN])

    def test_it_stays_on_this_machine_sealed(self):
        self.answer = lambda prompt: json.dumps(self.lines())
        self.run_pass()
        raw = sqlite3.connect(self.store.path)
        stored = raw.execute('SELECT lines FROM person_summaries').fetchone()[0]
        raw.close()
        self.assertNotIn(b'Legal', stored if isinstance(stored, bytes) else stored.encode())
        for name in ('fleet.py', 'shared_graph.py', 'fleet_requests.py', 'fleet_reviews.py', 'fleet_learnings.py', 'team_learnings.py', 'contact_share.py', 'network.py'):
            self.assertNotIn('person_summar', (ROOT / name).read_text(encoding='utf-8'), name)
        with self.store.connect() as db:
            graph.delete_person(db, ANN, self.app.config, a.now())
            self.assertEqual(db.execute('SELECT count(*) FROM person_summaries').fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()
