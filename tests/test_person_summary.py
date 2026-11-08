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
CHECK = '\nLines:\n'


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
        self.checks = []
        self.check = lambda line: None  # the check's verdict on one line: None passes, else why
        self.app.summary_model = lambda config, prompt: (self.prompts.append(prompt), self.judge(prompt) if CHECK in prompt else self.answer(prompt))[1]
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

    def judge(self, prompt):
        """The stand-in check turn: self.check's verdict on each line it is given."""
        items = json.loads(prompt.split(CHECK, 1)[1])
        self.checks.append(items)
        return json.dumps({'lines': [{'id': x['id'], 'ok': True} if self.check(x) is None else {'id': x['id'], 'ok': False, 'why': self.check(x)}
                                     for x in items]})

    def lines(self, *extra):
        e = self.events
        return {'people': [{'node_id': ANN, 'lines': [
            {'kind': 'who', 'text': 'Customer — runs ops at Acme.', 'sources': [f'E{e[0]}']},
            {'kind': 'now', 'text': 'Legal reviews the contract next week.', 'sources': [f'E{e[2]}', 'E999999']},
            {'kind': 'open', 'text': 'You promised to send the contract by Friday.', 'sources': [f'P{self.promise}']},
            {'kind': 'now', 'text': 'Prefers calls before 10.', 'sources': [f'F{self.fact}']},
            {'kind': 'now', 'text': 'Invited you to a birthday party.', 'sources': [f'E{e[3]}']},
            {'kind': 'now', 'text': 'Made up without a source.', 'sources': []}, *extra]}]}

    def test_a_line_that_only_repeats_the_page_is_dropped(self):
        """The page shows their role, organization and how often you talk: a line saying only that adds nothing."""
        page = {'node_id': ANN, 'name': 'Ann Example', 'role': 'customer', 'organization': 'Acme', 'title': 'Head of operations',
                'facts': [], 'open_promises': [], 'signals': [{'id': 'E1'}, {'id': 'E2'}]}
        answer = {'people': [{'node_id': ANN, 'lines': [
            {'kind': 'who', 'text': 'A customer at Acme; you write regularly.', 'sources': ['E1']},  # role and cadence only
            {'kind': 'who', 'text': 'Head of operations at Acme.', 'sources': ['E1']},  # the header's title and organization
            {'kind': 'now', 'text': 'You talk every few days.', 'sources': ['E2']},  # the rhythm line
            {'kind': 'who', 'text': 'Introduced you to their CFO in March.', 'sources': ['E1']},
            {'kind': 'now', 'text': 'Waiting on their signed order form.', 'sources': ['E2']}]}]}
        found = person_summary.parse(json.dumps(answer), [page])
        self.assertEqual([line['text'] for line in found[ANN]], ['Introduced you to their CFO in March.', 'Waiting on their signed order form.'])
        prompt = person_summary.prompt([page])
        self.assertIn('Never repeat those', prompt)

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
        self.assertIn('owner_edited', [x for x in self.prompts if CHECK not in x][-1])
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

    def all_day_party(self, zone):
        """A made-up all-day party on Dec 5 next year, stored as the calendar connector does with the owner in `zone`."""
        import timeutil
        timeutil.set_timezone(zone)
        year = self.now.year + 1
        raw = {'id': f'party-{zone}', 'summary': 'Birthday party', 'start': {'date': f'{year}-12-05'}, 'end': {'date': f'{year}-12-06'},
               'attendees': [{'email': 'ann@acme.example'}, {'email': 'owner@example.com', 'self': True}], 'status': 'confirmed'}
        event = a.calendar_event({'id': 'home', 'email': 'owner@example.com'}, raw, 'UTC')
        with self.store.connect() as db:
            event_id = db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) VALUES(?,?,?,?,?,?,?,'h',?)",
                                  ('home', raw['id'], 'calendar.event', event['occurred_at'], 'Birthday party', '', json.dumps(event['metadata']), a.now())).lastrowid
            db.execute('INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,0,1)', (ANN, event_id, event['occurred_at']))
        return event_id, f'{year}-12-05'

    def test_an_all_day_event_reaches_the_summary_on_its_own_date_east_and_west(self):
        """Brussels: the party's midnight is Dec 4 23:00 UTC. Los Angeles: Dec 5 08:00 UTC. The turn gets Dec 5 both times."""
        import timeutil
        zone = timeutil.LOCAL_TZ
        self.addCleanup(setattr, timeutil, 'LOCAL_TZ', zone)
        for owner in ('Europe/Brussels', 'America/Los_Angeles'):
            with self.subTest(owner=owner):
                event_id, day = self.all_day_party(owner)
                with self.store.connect() as db:
                    person = next(p for p in person_summary.active(db, self.now) if p['id'] == ANN)
                    page = person_summary.evidence(db, graph.Owner({'accounts': self.accounts}, db), person, graph.person_evidence)
                party = next(m for m in page['signals'] if m['id'] == f'E{event_id}')
                self.assertEqual((party['date'], party.get('all_day')), (day, True))
                self.assertEqual(page['today'], timeutil.local_day_text(a.now()))
                with self.store.connect() as db:
                    db.execute('DELETE FROM graph_events WHERE event_id=?', (event_id,))
        self.assertIn('an all_day meeting is on its date', person_summary.prompt([page]))

    def test_a_kept_promise_leaves_the_summary_and_the_person_is_due_again(self):
        """A promise on a to-do that is done is kept: the next turn doesn't get it as open, and a line standing only on it
        no longer shows (the person is due for a rewrite). One still open stays."""
        self.answer = lambda prompt: json.dumps(self.lines())
        self.run_pass()
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES('s2','s2','Send it','','[]','[\"work\"]','accepted',?)", (a.now(),))
            db.execute("UPDATE promises SET status='carded',suggestion_id='s2' WHERE id=?", (self.promise,))
            texts = [line['text'] for line in person_summary.view(db, ANN)['lines']]
            self.assertIn('You promised to send the contract by Friday.', texts)  # its to-do is still out: still open
            person = next(p for p in person_summary.active(db, self.now) if p['id'] == ANN)
            owner = graph.Owner({'accounts': self.accounts}, db)
            self.assertEqual([p['id'] for p in person_summary.evidence(db, owner, person, graph.person_evidence)['open_promises']], [f'P{self.promise}'])
            db.execute("UPDATE suggestions SET status='completed' WHERE id='s2'")
            self.assertEqual(person_summary.evidence(db, owner, person, graph.person_evidence)['open_promises'], [])
            texts = [line['text'] for line in person_summary.view(db, ANN)['lines']]
            self.assertNotIn('You promised to send the contract by Friday.', texts)
            self.assertIn('Prefers calls before 10.', texts)
            self.assertEqual(person_summary.prep_lines(db, ANN, ['work', 'personal']).count('You promised to send the contract by Friday.'), 0)
            db.execute('UPDATE person_summary_runs SET started_at=?', ((self.now - dt.timedelta(hours=2)).isoformat(),))
            db.execute('UPDATE person_summaries SET written_at=?,evidence_at=?', ((self.now - dt.timedelta(days=1)).isoformat(), '9999'))
            self.assertEqual([p['id'] for p in person_summary.due(db)], [ANN])

    def test_every_line_is_checked_a_rejected_one_is_written_again_once_then_dropped(self):
        """Quality or nothing: a model check judges each line on the rubric (specific, everyone named, no guessed roles)
        with the evidence it cites. A rejected line gets one rewrite with the reason; one still failing is dropped."""
        e = self.events
        first = {'people': [{'node_id': ANN, 'lines': [
            {'kind': 'who', 'text': 'You share work updates and thoughts on projects together.', 'sources': [f'E{e[0]}']},
            {'kind': 'now', 'text': 'He would need help, but liked the idea of doing it with his dad.', 'sources': [f'E{e[2]}']},
            {'kind': 'open', 'text': 'You promised Ann the contract by Friday.', 'sources': [f'P{self.promise}']}]}]}
        again = {'people': [{'node_id': ANN, 'lines': [
            {'kind': 'now', 'text': 'You keep in touch about all sorts of things.', 'sources': [f'E{e[0]}']},
            {'kind': 'now', 'text': "Ann's legal team reviews the contract next week.", 'sources': [f'E{e[2]}']}]}]}
        self.answer = lambda prompt: json.dumps(again if 'rejected_lines' in prompt else first)
        verdicts = {'You share work updates and thoughts on projects together.': 'generic, no concrete fact',
                    'He would need help, but liked the idea of doing it with his dad.': 'unnamed "he", guessed role "his dad"',
                    'You keep in touch about all sorts of things.': 'generic'}
        self.check = lambda item: verdicts.get(item['line'])
        self.assertEqual(self.run_pass(), 1)
        self.assertEqual(len(self.prompts), 4)  # write, check, write the rejected ones again, check those
        write, check, rewrite, recheck = self.prompts
        self.assertIn('Specific:', check)
        self.assertIn('Named:', check)
        self.assertIn('Grounded:', check)
        self.assertIn('not on the words it uses', check)
        cited = {x['line']: x for x in self.checks[0]}
        self.assertEqual(cited['You promised Ann the contract by Friday.']['about'], 'Ann Example')
        self.assertEqual([i['id'] for i in cited['You promised Ann the contract by Friday.']['evidence']], [f'P{self.promise}'])
        self.assertEqual(cited['He would need help, but liked the idea of doing it with his dad.']['evidence'][0]['text'],
                         'Thanks, legal reviews it next week.')
        asked = json.loads(rewrite.split('\nPeople:\n', 1)[1])[0]
        self.assertEqual(asked['kept_lines'], ['You promised Ann the contract by Friday.'])
        self.assertEqual({x['why'] for x in asked['rejected_lines']}, {'generic, no concrete fact', 'unnamed "he", guessed role "his dad"'})
        self.assertEqual(len(self.checks[1]), 2)  # only the rewritten lines are checked again
        with self.store.connect() as db:
            texts = [line['text'] for line in person_summary.view(db, ANN)['lines']]
            stored = json.loads(person_summary._row(db, ANN)['lines'])
        self.assertEqual(texts, ["Ann's legal team reviews the contract next week.", 'You promised Ann the contract by Friday.'])
        self.assertFalse([k for line in stored for k in line if k.startswith('_')])  # what the check read is not kept

    def test_the_prompt_asks_for_names_and_specifics_not_they(self):
        prompt = person_summary.prompt([{'node_id': ANN, 'name': 'Ann Example', 'signals': []}])
        self.assertNotIn('Say "they" for the person', prompt)
        self.assertIn('the person this page is about by their first name', prompt)
        self.assertIn('An organization or project by its short name', prompt)
        self.assertIn('A first name counts as named', person_summary.RUBRIC)
        self.assertIn('Fewer lines are better than vague ones', prompt)
        self.assertIn(person_summary.RUBRIC, prompt)

    def test_nothing_specific_left_means_no_summary(self):
        """A summary The Machine wrote before goes when a new pass finds nothing specific to say: no section at all."""
        self.answer = lambda prompt: json.dumps(self.lines())
        self.run_pass()
        with self.store.connect() as db:
            self.assertTrue(person_summary.view(db, ANN))
            db.execute('UPDATE person_summary_runs SET started_at=?', ((self.now - dt.timedelta(hours=2)).isoformat(),))
            db.execute('UPDATE person_summaries SET written_at=?,evidence_at=?', ((self.now - dt.timedelta(days=2)).isoformat(),) * 2)
        self.check = lambda item: 'generic'
        self.prompts.clear()
        self.run_pass()
        self.assertEqual(len(self.prompts), 4)
        with self.store.connect() as db:
            self.assertIsNone(person_summary.view(db, ANN))
            self.assertIsNone(graph.detail(db, ANN)['summary'])

    def test_an_unreadable_check_saves_nothing_and_the_person_stays_due(self):
        self.answer = lambda prompt: json.dumps(self.lines())
        self.judge = lambda prompt: 'Sorry, I can only answer in prose.'
        self.run_pass()
        with self.store.connect() as db:
            self.assertIsNone(person_summary.view(db, ANN))
            self.assertEqual(db.execute('SELECT status FROM person_summary_runs').fetchone()[0], 'failed')
            db.execute('UPDATE person_summary_runs SET started_at=?', ((self.now - dt.timedelta(hours=2)).isoformat(),))
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

    # Early refresh: a matter that moved later the same day ---------------------------------------------------------

    def message(self, node, body, hours_ago=0.0, direct=1):
        """A new message from someone (a made-up one), in their graph, `hours_ago` hours back."""
        at = (self.now - dt.timedelta(hours=hours_ago)).isoformat(timespec='seconds')
        with self.store.connect() as db:
            event_id = db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) VALUES('work',?,'gmail.message',?,'Proposal',?,?,'h',?)",
                                  (f'm{body}{hours_ago}', at, body, json.dumps({'from': 'Ann <ann@acme.example>'}), at)).lastrowid
            db.execute('INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,0,?)', (node, event_id, at, direct))
        return event_id

    def written(self, hours_ago):
        """Ann's summary as written `hours_ago` hours back, the last pass long enough ago for the next."""
        with self.store.connect() as db:
            stamp = (self.now - dt.timedelta(hours=hours_ago)).isoformat(timespec='seconds')
            db.execute('UPDATE person_summaries SET written_at=?,evidence_at=?', (stamp, stamp))
            db.execute('UPDATE person_summary_runs SET started_at=?', ((self.now - dt.timedelta(hours=2)).isoformat(),))

    def made(self, hours_ago):
        """The to-dos and decisions so far as made `hours_ago` hours back."""
        stamp = (self.now - dt.timedelta(hours=hours_ago)).isoformat(timespec='seconds')
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET created_at=? WHERE created_at>?', (stamp, stamp))
            db.execute('UPDATE decisions SET created_at=? WHERE created_at>?', (stamp, stamp))

    def due_now(self):
        with self.store.connect() as db:
            return [p['id'] for p in person_summary.due(db)]

    def test_an_escalation_the_review_puts_on_a_to_do_makes_them_due_early(self):
        """Ann asks for the proposal by Monday; the summary says so. Later that day she needs it today: the review brings
        the to-do up to date, and her summary is rewritten early, not 20 hours later."""
        self.answer = lambda prompt: json.dumps(self.lines())
        self.run_pass()
        ask = self.message(ANN, 'Could you send the proposal by Monday?', hours_ago=6)
        card = self.store.suggest('proposal-ann', 'Send Ann the proposal', 'Ann asks for the proposal by Monday.', [ask], match=True)['id']
        self.made(6)
        self.written(5)  # written after that to-do, 5 hours ago
        self.message(ANN, 'Just a nudge: still on track?', hours_ago=1)
        self.assertEqual(self.due_now(), [])  # a new message alone waits for the 20 hours
        later = self.message(ANN, 'We need it today, or the board slot moves a month.', hours_ago=0.5)
        saved = self.store.suggest('proposal-ann-today', 'Send Ann the proposal today', 'Ann needs it today.', [later], card_id=card, match=True, urgent=True)
        self.assertTrue(saved.get('updated'))
        self.assertEqual(self.due_now(), [ANN])  # the review moved the matter: due early
        self.made(1.5)
        self.written(1)  # written an hour ago, after that change: nothing new to catch up on
        self.assertEqual(self.due_now(), [])
        self.made(0.5)
        self.written(1)  # a change after it, but the summary is under EARLY_HOURS old
        self.assertEqual(self.due_now(), [])
        self.written(2.5)
        self.assertEqual(self.due_now(), [ANN])

    def test_a_to_do_closed_or_a_promise_rescheduled_makes_them_due_early(self):
        """A request taken back (its to-do closed) or a new deadline on a promise changes what the summary says is open."""
        self.answer = lambda prompt: json.dumps(self.lines())
        self.run_pass()
        ask = self.message(ANN, 'Can you drop off the samples?', hours_ago=8)
        card = self.store.suggest('samples-ann', 'Drop off the samples', 'Ann asks for the samples.', [ask], match=True)['id']
        self.made(7)
        self.written(6)
        self.assertEqual(self.due_now(), [])
        self.store.decide(card, 'reject', '', 'no-longer-needed', 'dashboard')  # she took it back
        self.assertEqual(self.due_now(), [ANN])
        self.made(4)
        self.written(3)  # rewritten since
        self.assertEqual(self.due_now(), [])
        with self.store.connect() as db:
            from machine.store.promises import promise_logged
            db.execute('UPDATE promises SET due=? WHERE id=?', ((self.now + dt.timedelta(days=3)).date().isoformat(), self.promise))
            promise_logged(db, self.promise, 'due', 'later')  # a new date for the contract
        self.assertEqual(self.due_now(), [ANN])

    def test_someone_only_in_cc_or_an_unrelated_change_is_not_due_early(self):
        """Only people a message came from or went to directly; a to-do about someone else leaves Ann's summary alone."""
        self.answer = lambda prompt: json.dumps(self.lines())
        self.run_pass()
        self.written(5)
        other = self.message('email:cy@other.example', 'Can you review the brief?', hours_ago=1)
        copied = self.message(ANN, 'cc', hours_ago=1, direct=0)
        with self.store.connect() as db:
            db.execute('INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,0,0)', (ANN, other, a.now()))
            db.execute('DELETE FROM graph_events WHERE event_id=? AND node_id=?', (copied, ANN))
        self.store.suggest('brief-cy', 'Review the brief', 'Cy asks for a review.', [other], match=True, separate=True)
        self.assertEqual(self.due_now(), [])
        with self.store.connect() as db:
            self.assertNotIn(ANN, person_summary.changes(db, (self.now - dt.timedelta(hours=20)).isoformat()))

    def test_early_ones_go_first_and_a_pass_keeps_its_limits(self):
        """A person due early is first in the pass; the pass still runs at most once an hour."""
        self.answer = lambda prompt: json.dumps(self.lines())
        self.run_pass()
        ask = self.message(ANN, 'Can you confirm the venue?', hours_ago=0.5)
        self.written(4)
        self.store.suggest('venue-ann', 'Confirm the venue', 'Ann asks to confirm the venue.', [ask], match=True)
        with self.store.connect() as db:
            self.assertEqual([p['id'] for p in person_summary.due(db, limit=1)], [ANN])
            db.execute('UPDATE person_summary_runs SET started_at=?', (a.now(),))
            self.assertEqual(person_summary.due(db), [])  # a pass ran within the hour

    def test_past_the_days_passes_only_early_ones_and_spread_out(self):
        """Eight passes used by noon: a change in the afternoon still gets a pass of only early ones, a few a day, spread out."""
        self.answer = lambda prompt: json.dumps(self.lines())
        self.run_pass()
        self.written(5)
        with self.store.connect() as db:
            old = (self.now - dt.timedelta(hours=6)).isoformat(timespec='seconds')
            for _ in range(person_summary.PASSES_PER_DAY):
                person_summary.start_run(db, 6, old)
            bo = 'email:bo@x.example'  # someone else regular-due, who must wait for tomorrow's passes
            db.execute('UPDATE graph_nodes SET strength=1.0 WHERE id=?', (bo,))
        for n in range(2):
            self.message(bo, f'note {n}', hours_ago=2 + n, direct=1)
        self.assertEqual(self.due_now(), [])  # nothing moved for Ann
        ask = self.message(ANN, 'Can you move the call to today?', hours_ago=0.5)
        self.store.suggest('call-ann', 'Move the call', 'Ann asks to move the call to today.', [ask], match=True)
        with self.store.connect() as db:
            people = person_summary.due(db)
            self.assertEqual([(p['id'], p.get('extra')) for p in people], [(ANN, True)])  # only Ann, marked extra
            person_summary.start_run(db, 1, (self.now - dt.timedelta(hours=1)).isoformat(timespec='seconds'), extra=True)
            self.assertEqual(person_summary.due(db), [])  # one extra pass every EARLY_PASS_HOURS
            db.execute('UPDATE person_summary_runs SET started_at=? WHERE extra=1', ((self.now - dt.timedelta(hours=4)).isoformat(timespec='seconds'),))
            self.assertEqual([p['id'] for p in person_summary.due(db)], [ANN])
            for _ in range(person_summary.EARLY_PASSES - 1):
                person_summary.start_run(db, 1, (self.now - dt.timedelta(hours=4)).isoformat(timespec='seconds'), extra=True)
            self.assertEqual(person_summary.due(db), [])  # and at most EARLY_PASSES a day
            db.execute('DELETE FROM person_summary_runs')
            self.assertEqual([p['id'] for p in person_summary.due(db)], [ANN, bo])  # with passes left, Bo too, after Ann


if __name__ == '__main__':
    unittest.main()
