"""Knowledge for another AI (machine/export/knowledge.py, docs/knowledge-export.md): what The Machine learned, as
Markdown, JSONL and CSV that another AI understands without The Machine.

- Completeness: every table of the database is exported or left out for a stated reason (coverage.py), and every
  kind of Graph record, link, fact, rule and summary line has its place, so a new kind fails here until the export
  carries it.
- Readability: tests/knowledge_export_eval.py, run isolated on the folder alone, answers questions about the owner,
  their people and work from it.
- Privacy: never a credential; message text only when asked; private threads, Only-you projects and a Careful
  Fleet's content only when asked.

Synthetic data only."""
import csv
import datetime as dt
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))

spec = importlib.util.spec_from_file_location('knowledge_export_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import graph  # noqa: E402
import knowledge as brain  # noqa: E402
import person_summary  # noqa: E402
import shared_graph  # noqa: E402
import skills  # noqa: E402
from machine.export import coverage  # noqa: E402
from machine.export import knowledge  # noqa: E402

AVERY, BO, CY = 'email:avery@lumen.example', 'email:bo@lumen.example', 'email:cy@north.example'
ORG = 'org:lumen.example'
TOKEN = '-'.join(('xoxb', '1111111111', '2222222222', 'abcdefghijklmnop'))  # a made-up token, built here so scanners skip it: never in the export
SECRET_BODY = 'BODY-SENTINEL the pricing sheet comes Monday'
PRIVATE_BODY = 'PRIVATE-SENTINEL about the quiet merger'


# Past facts and rules (text, kind, sort, about, to-do, until, removed days ago, how): merged_into is '<how>:<own id>'
# for expired and aside, the target for call, skill, voice and record; None with removed is forgotten, without removed
# a current fact past its end day; forgot: merged into the forgotten one above it.
PAST_FACTS = (('Was based in the old office.', 'fact', 'fact', AVERY, 'pricing', '2026-01-31', 30, 'expired'),
              ('Had a trial until last spring.', 'fact', 'event', AVERY, 'pricing', '2025-05-01', None, None),
              ('Liked long reports.', 'fact', 'preference', None, 'done', None, 20, 'aside'),
              ('Open drafts with the weather.', 'draft', None, None, 'done', None, 20, 'aside'),
              ('Prefers calls.', 'fact', 'preference', AVERY, 'pricing', None, 10, 'call'),
              ('Books the onboarding call within a week.', 'fact', 'fact', None, 'done', None, 9, 'skill'),
              ('Signs emails with Cheers.', 'fact', 'preference', None, 'done', None, 8, 'voice'),
              ("Cy's number is +32 470 00 00 00.", 'fact', 'fact', None, 'done', None, 7, 'record'),
              ('FORGOTTEN-SENTINEL never say this', 'fact', 'fact', AVERY, 'pricing', None, 5, None),
              ('FORGOTTEN-TOO-SENTINEL condensed into the forgotten one', 'fact', 'fact', AVERY, 'pricing', None, 6, 'forgot'),
              ('MERGER-PAST-SENTINEL was in talks', 'fact', 'fact', AVERY, 'merger', None, 6, 'call'))


class FakeFleet:
    def briefs(self):
        return {'f1': {'text': 'Your Fleet this week: two renewals are waiting on legal.', 'built_at': '2026-11-02T08:00:00+00:00'},
                'f2': {'text': 'CAREFUL-SENTINEL brief', 'built_at': '2026-11-02T08:00:00+00:00'}}


def build(folder):
    """A small Machine: three people, an organization, two projects (one Only you), facts, a rule, writing style, a
    signature, a skill, summary lines, a promise, open to-dos, team briefs, chat notes and a private thread."""
    folder = Path(folder)
    config = {'database': str(folder / 'events.sqlite'), 'owner_name': 'Sam Owner', 'timezone': 'Europe/Brussels',
              'accounts': [{'id': 'work', 'service': 'gmail', 'email': 'sam@owner.example', 'boundary': 'work:Owner', 'token': TOKEN},
                           {'id': 'home', 'service': 'whatsapp', 'boundary': 'personal:'}],
              'slack_bot_token': TOKEN}
    store = a.Store(config['database'], protect=True)
    store.accounts = config['accounts']
    now = dt.datetime.now(dt.timezone.utc)
    ago = lambda days: (now - dt.timedelta(days=days)).isoformat(timespec='seconds')
    with store.connect() as db:
        import crm_fields
        import fleet
        shared_graph.ensure(db)
        fleet.ensure(db)
        crm_fields.ensure(db)
        events = {}
        for key, days, account, body, thread in (('pricing', 6, 'work', SECRET_BODY, 't-1'), ('intro', 20, 'work', 'Bo helps Avery with the calendar.', 't-2'),
                                                 ('stage', 3, 'work', 'Proposal is with their team.', 't-3'), ('merger', 2, 'work', PRIVATE_BODY, 't-9')):
            events[key] = db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) "
                                     "VALUES(?,?,?,?,?,?,?,'h',?)", (account, 'gm-' + key, 'gmail.message', ago(days), 'Re: ' + key, body,
                                                                    json.dumps({'from': 'Avery <avery@lumen.example>', 'thread_id': thread}), ago(days))).lastrowid
        people = ((AVERY, 'Avery Quill', 2.5, {'role': 'customer', 'side': 'work', 'org': ORG, 'emails': ['avery@lumen.example'],
                                                'profile': {'title': 'Head of Operations'}, 'notes': 'Met at the spring fair.',
                                                'relations': [{'a': BO, 'a_name': 'Bo Tern', 'relation': 'assistant of', 'b': AVERY, 'b_name': 'Avery Quill', 'by': 'owner'}]}),
                  (BO, 'Bo Tern', 1.2, {'side': 'work', 'org': ORG, 'emails': ['bo@lumen.example'],
                                        'relations': [{'a': BO, 'a_name': 'Bo Tern', 'relation': 'assistant of', 'b': AVERY, 'b_name': 'Avery Quill', 'by': 'owner'}]}),
                  (CY, 'Cy North', 0.8, {'side': 'personal', 'emails': ['cy@north.example']}))
        for node, name, strength, info in people:
            db.execute('INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,?,?,?,?,?,?)',
                       (node, 'person', name, strength, ago(3), 5, json.dumps({'ids': [node], **info})))
        db.execute('INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,?,?,?,?,?,?)',
                   (ORG, 'org', 'Lumen Works', 2.0, ago(3), 9, json.dumps({'domain': 'lumen.example', 'role': 'customer'})))
        board = db.execute("INSERT INTO boards(name,stages,source,created_at) VALUES('Deals','[\"Contacted\",\"Proposal\",\"Won\"]','owner',?)", (ago(30),)).lastrowid
        open_project = db.execute('INSERT INTO projects(name,created_at,board_id,stage,stage_reason,stage_event_id,next_step) VALUES(?,?,?,?,?,?,?)',
                                  ('Harbor Rollout', ago(30), board, 'Proposal', 'They have the proposal', events['stage'], 'Follow up on legal')).lastrowid
        quiet = db.execute("INSERT INTO projects(name,created_at,visibility) VALUES('Quiet Merger',?,'only_you')", (ago(10),)).lastrowid
        for pid, name in ((open_project, 'Harbor Rollout'), (quiet, 'Quiet Merger')):
            db.execute('INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,trend,info) VALUES(?,?,?,?,?,?,?,?)',
                       (f'project:{pid}', 'project', name, 1.5, ago(2), 4, 1.0, '{}'))
        db.execute('INSERT INTO event_projects(event_id,project_id,source,created_at) VALUES(?,?,?,?)', (events['merger'], quiet, 'review', ago(2)))
        for x, y, kind in ((AVERY, ORG, 'member'), (BO, ORG, 'member'), (AVERY, f'project:{open_project}', 'project'), (AVERY, BO, 'together'),
                           (BO, AVERY, 'relation'), (AVERY, f'project:{quiet}', 'project')):
            db.execute('INSERT INTO graph_links(a,b,kind,strength,last_at) VALUES(?,?,?,?,?)', (x, y, kind, 1.0, ago(3)))
        db.execute("INSERT INTO graph_relations(a,b,relation,source,event_id,created_at) VALUES(?,?,'assistant of','owner',?,?)", (BO, AVERY, events['intro'], ago(20)))
        for key, node in (('pricing', AVERY), ('intro', BO), ('stage', f'project:{open_project}'), ('merger', AVERY)):
            db.execute('INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,0,1)', (node, events[key], ago(3)))
        db.execute("INSERT INTO share_threads(thread,verdict,hand,event_id,at) VALUES(?,'sensitive',NULL,?,?)",
                   (shared_graph.thread_of('gmail.message', {'thread_id': 't-9'}, events['merger']), events['merger'], ago(2)))
        todos = {}
        for key, title, status, events_of, project in (('pricing', 'Send Avery the pricing sheet', 'pending', ['pricing'], 'Harbor Rollout'),
                                                        ('merger', 'Reply about the quiet merger', 'pending', ['merger'], None),
                                                        ('done', 'An old one', 'completed', ['intro'], None)):
            todos[key] = 's-' + key
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at,due,project) VALUES(?,?,?,?,?,?,?,?,?,?)",
                       (todos[key], todos[key], title, 'From the thread with Avery.', json.dumps([events[k] for k in events_of]), '["work"]', status, ago(5),
                        '2026-11-10' if key == 'pricing' else None, project))
        facts = (('Prefers meetings after 10:00.', 'fact', 'preference', None, 'done', None),
                 ('Prefers a call over email.', 'fact', 'preference', AVERY, 'pricing', None),
                 ('Needs the pricing sheet before the board meets.', 'fact', 'fact', AVERY, 'pricing', None),
                 ('Is moving offices in December.', 'fact', 'event', AVERY, 'pricing', ago(-30)[:10]),  # still ahead, whatever today is
                 ('Promised to review the contract this month.', 'fact', 'commitment', BO, 'done', None),
                 ('Wants the merger kept quiet.', 'fact', 'fact', AVERY, 'merger', None),
                 ('Keep drafts under five sentences.', 'draft', None, None, 'done', None))
        for text, kind, sort, about, todo, until in facts:
            fid = db.execute('INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind,fact_kind,valid_until) VALUES(?,?,?,?,?,?,?)',
                             (text, 'd-' + todo, todos[todo], ago(4), kind, sort, until)).lastrowid
            if about:
                db.execute("INSERT INTO fact_about(fact_id,node_id,by,created_at) VALUES(?,?,'review',?)", (fid, about, ago(4)))
        db.execute("INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind,fact_kind,source,side) VALUES('Likes short agendas.','ai:c1',NULL,?,'fact','preference','ai:Claude','work')", (ago(1),))
        db.execute("INSERT INTO fact_about(fact_id,node_id,by,created_at) VALUES(last_insert_rowid(),?,'ai',?)", (BO, ago(1)))
        call_id = db.execute("SELECT id FROM facts WHERE text='Prefers a call over email.'").fetchone()[0]
        for text, kind, sort, about, todo, until, removed, into in PAST_FACTS:
            fid = db.execute('INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind,fact_kind,valid_until,removed_at,merged_into) VALUES(?,?,?,?,?,?,?,?,?)',
                             (text, 'd-' + todo, todos[todo], ago(40), kind, sort, until, removed and ago(removed), None)).lastrowid
            if into is None and removed:
                forgot_id = fid
            target = {'call': f'fact:{call_id}', 'skill': 'skill:onboarding-call', 'voice': 'voice:Email', 'record': 'record:' + CY}.get(into)
            target = f'fact:{forgot_id}' if into == 'forgot' else target
            db.execute('UPDATE facts SET merged_into=? WHERE id=?', (target or (f'{into}:{fid}' if into else None), fid))
            if about:
                db.execute("INSERT INTO fact_about(fact_id,node_id,by,created_at) VALUES(?,?,'review',?)", (fid, about, ago(40)))
        db.execute("INSERT INTO voices(channel,text,source,updated_at) VALUES('Email','Short and warm. Signs off with Cheers.','owner',?)", (ago(2),))
        db.execute("INSERT INTO voices(channel,text,source,updated_at) VALUES('Slack','Lowercase, no greeting.','review',?)", (ago(2),))
        promise_cols = {r[1] for r in db.execute('PRAGMA table_info(promises)')}
        assert 'together' in promise_cols
        db.execute("INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,status,suggestion_id,created_at,updated_at) "
                   "VALUES('mine','Avery Quill','Send the pricing sheet','2026-11-10',?,?,'work','open',?,?,?)", (ago(-4), events['pricing'], todos['pricing'], ago(6), ago(6)))
        db.execute("INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,status,created_at,updated_at) "
                   "VALUES('theirs','Avery Quill','Share the merger terms',NULL,?,?,'work','open',?,?)", (ago(-4), events['merger'], ago(2), ago(2)))
        person_summary.ensure(db)
        lines = [{'kind': k, 'text': t, 'sources': s, 'sides': ['work']} for k, t, s in (
            ('who', 'Runs operations at Lumen Works.', [f"E{events['intro']}"]), ('now', 'Waiting on the pricing sheet.', [f"E{events['pricing']}"]),
            ('open', 'Asked about the quiet merger.', [f"E{events['merger']}"]))]
        db.execute("INSERT INTO person_summaries(node_id,lines,by,written_at) VALUES(?,?,'machine',?)", (AVERY, json.dumps(lines), ago(1)))
        skills.ensure(db)
        for slug, name, status in (('onboarding-call', 'Onboarding call', 'on'), ('idea', 'Proposed idea', 'proposed')):
            db.execute('INSERT INTO skills(id,slug,name,description,body,status,origin,sha,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)',
                       (slug, slug, name, 'When a new customer starts.', '1. Book 30 minutes.\n2. Share the checklist.\n3. Send the recap the same day.',
                        status, 'owner', 'x', ago(9), ago(9)))
        db.execute("INSERT INTO crm_fields(kind,name,type,position,created_at) VALUES('person','Renewal month','text',0,?)", (ago(9),))
        db.execute("INSERT INTO crm_values(node_id,field_id,value,set_at) VALUES(?,last_insert_rowid(),'March',?)", (AVERY, ago(9)))
        db.execute("INSERT INTO crm_tags(node_id,tag,at) VALUES(?,'vip',?)", (AVERY, ago(9)))
        db.execute("INSERT OR REPLACE INTO fleet_meta(key,value) VALUES('directory',?)",
                   (json.dumps({'fleets': [{'id': 'f1', 'kind': 'work', 'name': 'Owner Co'}, {'id': 'f2', 'kind': 'work', 'name': 'Strict Co', 'security': {'level': 'careful'}}]}),))
    (folder / 'signatures.json').write_text(json.dumps({'work': {'html': '<div>Sam Owner<br>Owner Co</div>', 'source': 'owner', 'updated_at': ago(5)}}))
    space = folder / 'workspace'
    (space / 'memory').mkdir(parents=True)
    (space / 'USER.md').write_text('# About Sam\n\nWorks from Ghent. Coffee, no sugar.\n')
    (space / 'memory/2026-11-01.md').write_text(f'Talked about the trip.\napi_key = "{TOKEN}"\n')
    return store, config, space


class KnowledgeExport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.store, cls.config, cls.space = build(cls.temp.name)
        cls.reader = knowledge.StoreReader(cls.store, cls.config, FakeFleet(), cls.space)
        cls.bundle = knowledge.collect(cls.reader)
        cls.out = Path(cls.temp.name) / 'export'
        cls.files = knowledge.write(cls.bundle, cls.out)
        cls.text = '\n'.join(d.decode() for d in cls.files.values())

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    # -- completeness --------------------------------------------------------------------------------------------------

    def test_every_table_is_exported_or_left_out_for_a_reason(self):
        import test_architecture
        creates, _ = test_architecture.schema_and_writes()
        known = coverage.classified()
        missing = sorted(set(creates) - set(known))
        self.assertEqual(missing, [], 'New tables: say in machine/export/coverage.py where Knowledge for another AI puts them, or why not')
        self.assertEqual(sorted(set(known) - set(creates)), [], 'coverage.py names tables that no longer exist')
        names = [*coverage.EXPORTED, *coverage.READ, *coverage.FOLDED, *(t for v in coverage.LEFT_OUT.values() for t in v)]
        self.assertEqual(len(names), len(set(names)), 'a table is in two places in coverage.py')

    def test_every_kind_has_its_place(self):
        self.assertEqual(knowledge.FACT_SORTS, a.FACT_SORTS)
        self.assertEqual(set(a.FACT_KINDS), {'fact', 'draft'}, 'a new kind of fact: export it (facts or rules) in collect()')
        self.assertEqual(set(brain.KINDS), set(knowledge.KIND_FOLDERS))
        built = set(re.findall(r"links\.append\(\([^\n]*?'([a-z_]+)', round", (ROOT / 'graph.py').read_text()))
        self.assertTrue(built and built <= set(knowledge.LINKS), f'link kinds without a label: {built - set(knowledge.LINKS)}')
        self.assertEqual(set(skills.STATUSES) - set(knowledge.SKILL_STATUSES), {'proposed', 'incoming'})
        exported = {f['sort'] for f in self.bundle['facts']}
        self.assertEqual(exported, set(a.FACT_SORTS))
        self.assertEqual({s['kind'] for s in self.bundle['summaries']}, set(person_summary.KINDS) - {'open'})  # the open line is the private one
        self.assertEqual({e['kind'] for e in self.bundle['entities']}, set(brain.KINDS))
        self.assertEqual({r['kind'] for r in self.bundle['relationships']}, set(knowledge.LINKS))
        for key in ('entities', 'relationships', 'facts', 'rules', 'fact_history', 'writing_style', 'signatures', 'skills', 'summaries', 'promises',
                    'todos', 'team_briefs', 'notes', 'sources'):
            self.assertTrue(self.bundle[key], key)
            self.assertIn(f'records/{key}.jsonl', self.files) if key != 'notes' else None

    def test_layout(self):
        names = set(self.files)
        for name in ('README.md', 'manifest.json', 'owner/profile.md', 'people/avery-quill.md', 'people/bo-tern.md', 'people/cy-north.md',
                     'organizations/lumen-works.md', 'projects/harbor-rollout.md', 'skills/onboarding-call.md', 'team-briefs/owner-co.md',
                     'notes/USER.md', 'notes/memory/2026-11-01.md', 'tables/contacts.csv', 'tables/organizations.csv', 'tables/todos.csv',
                     'tables/promises.csv'):
            self.assertIn(name, names)
        manifest = json.loads(self.files['manifest.json'])
        self.assertEqual((manifest['schema_version'], manifest['format']), (knowledge.SCHEMA_VERSION, 'the-machine-knowledge'))
        self.assertEqual(manifest['files'], sorted(names))
        for line in self.files['records/entities.jsonl'].decode().splitlines():
            self.assertIn(json.loads(line)['file'], names)
        contacts = list(csv.DictReader(io.StringIO(self.files['tables/contacts.csv'].decode())))
        self.assertEqual({c['name'] for c in contacts}, {'Avery Quill', 'Bo Tern', 'Cy North'})
        avery = self.files['people/avery-quill.md'].decode()
        self.assertIn('[Lumen Works](../organizations/lumen-works.md)', avery)
        self.assertIn('- Renewal month: March', avery)
        self.assertIn('- Tags: vip', avery)
        self.assertNotIn('Proposed idea', self.text)  # a skill the owner never took on

    def test_another_ai_answers_from_the_folder_alone(self):
        done = subprocess.run([sys.executable, '-I', str(ROOT / 'tests/knowledge_export_eval.py'), str(self.out)], capture_output=True, text=True,
                              cwd=self.out, timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr)
        got = json.loads(done.stdout)
        self.assertEqual(got['What does the owner prefer for meetings?'], ['Prefers meetings after 10:00.'])
        self.assertEqual(got['What does Avery prefer for contact?'], ['Prefers a call over email.'])
        self.assertEqual(sorted(got['Who is Bo and how do they relate to Avery?']), ['Avery Quill often together with Bo Tern', 'Bo Tern assistant of Avery Quill'])
        self.assertEqual(got['What did Avery prefer before, and what replaced it?'], [['Prefers calls.', 'merged', 'Prefers a call over email.']])
        self.assertEqual(got['Where does Avery work?'], ['Lumen Works'])
        self.assertEqual(got['What did the owner promise Avery, and by when?'], [['Send the pricing sheet', '2026-11-10']])
        self.assertEqual(got['Which open to-dos are on Harbor Rollout?'], ['Send Avery the pricing sheet'])
        self.assertEqual(got['Where does Harbor Rollout stand?'], ['Deals', 'Proposal'])
        self.assertEqual(got['How does the owner write email?'], 'Short and warm. Signs off with Cheers.')
        self.assertEqual(got["What is the owner's signature?"], 'Sam Owner\nOwner Co')
        self.assertEqual(got['Which rules do drafts follow?'], ['Keep drafts under five sentences.'])
        self.assertEqual(got['Where did the fact about the pricing sheet come from?'], [{'kind': 'gmail.message', 'at': self.day(6), 'has_text': False}])
        self.assertIn('Share the checklist', got['How is an onboarding call done?'])
        self.assertEqual(got['What does the team brief say?'], ['Your Fleet this week: two renewals are waiting on legal.'])
        self.assertEqual(got['Who is Avery, in short?'], ['Runs operations at Lumen Works.', 'Waiting on the pricing sheet.'])
        for question in ("Does Avery's page say where they work?", "Does Bo's page say how they relate to Avery?", 'Does the README tell an AI where to start?'):
            self.assertIs(got[question], True, question)

    @staticmethod
    def day(days):
        return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).date().isoformat()

    def test_sources_are_stable_ids_with_dates(self):
        again = knowledge.collect(self.reader, now=dt.datetime(2030, 1, 1, tzinfo=dt.timezone.utc))
        self.assertEqual([s['id'] for s in again['sources']], [s['id'] for s in self.bundle['sources']])
        for s in self.bundle['sources']:
            self.assertRegex(s['id'], r'^m-[0-9a-f]{16}$')
            self.assertTrue(s['at'] and s['kind'] and s['provider_id'])
            self.assertNotIn('text', s)
        fact = next(f for f in self.bundle['facts'] if 'pricing sheet' in f['text'])
        self.assertEqual(fact['sources'], [knowledge.source_id('gmail.message', 'sam@owner.example', 'gm-pricing')])
        ai = next(f for f in self.bundle['facts'] if f['text'] == 'Likes short agendas.')
        self.assertEqual(ai['said_by'], 'ai:Claude')
        self.assertIn('Likes short agendas. (said by Claude)', self.files['people/bo-tern.md'].decode())

    def test_fact_history_with_status_dates_source_and_replacement(self):
        past = {f['text']: f for f in self.bundle['fact_history']}
        current = {f['text']: f['id'] for f in self.bundle['facts']}
        self.assertEqual({t: (f['status'], f['replaced_by']) for t, f in past.items()}, {
            'Was based in the old office.': ('ended', None), 'Had a trial until last spring.': ('ended', None),
            'Liked long reports.': ('set_aside', None), 'Open drafts with the weather.': ('set_aside', None),
            'Prefers calls.': ('merged', current['Prefers a call over email.']),
            'Books the onboarding call within a week.': ('moved', 'skill-onboarding-call'),
            'Signs emails with Cheers.': ('moved', 'style-email'), "Cy's number is +32 470 00 00 00.": ('moved', CY)})
        self.assertNotIn('FORGOTTEN-', self.text)  # forgotten by the owner, or condensed into one they forgot: never exported
        self.assertEqual(past['Open drafts with the weather.']['id'][:5], 'rule-')
        self.assertEqual((past['Open drafts with the weather.']['kind'], past['Liked long reports.']['kind']), ('rule', 'fact'))
        ended = past['Was based in the old office.']
        self.assertEqual((ended['about'], ended['sort'], ended['valid_until'], ended['ended_at'][:10]), ([AVERY], 'fact', '2026-01-31', self.day(30)))
        self.assertEqual(past['Had a trial until last spring.']['ended_at'], '2025-05-01')  # past its end day, not retired yet
        self.assertEqual(past['Liked long reports.']['set_aside_at'][:10], self.day(20))
        self.assertEqual(past['Prefers calls.']['merged_at'][:10], self.day(10))
        self.assertEqual(past['Prefers calls.']['learned_at'][:10], self.day(40))  # saved
        self.assertEqual(past['Prefers calls.']['sources'], [knowledge.source_id('gmail.message', 'sam@owner.example', 'gm-pricing')])
        self.assertEqual({f['said_by'] for f in past.values()}, {'owner'})
        styles = [json.loads(line) for line in self.files['records/writing_style.jsonl'].decode().splitlines()]
        self.assertIn('style-email', [s['id'] for s in styles])
        manifest = json.loads(self.files['manifest.json'])
        self.assertEqual(manifest['counts']['fact_history'], len(past))
        self.assertIn('records/fact_history.jsonl', manifest['files'])
        self.assertIn('fact_history.jsonl', self.files['README.md'].decode())
        everything = knowledge.collect(self.reader, knowledge.Options(private=True))
        self.assertIn('MERGER-PAST-SENTINEL was in talks', [f['text'] for f in everything['fact_history']])

    def test_fact_history_names_who_saved_it(self):
        reader = self.reader

        class Past(knowledge.StoreReader):
            def fact_history(self):
                rows = reader.fact_history()
                return [{**rows[0], 'source': 'ai:Claude', 'side': 'work'}, {**rows[1], 'condensed': True}, {**rows[2], 'condensed': True, 'kept_at': 'x'}]

        got = knowledge.collect(Past(self.store, self.config, FakeFleet(), self.space))['fact_history']
        self.assertEqual([f['said_by'] for f in got], ['ai:Claude', 'the-machine', 'owner'])

    # -- privacy -------------------------------------------------------------------------------------------------------

    def test_never_a_credential(self):
        self.assertNotIn(TOKEN, self.text)
        self.assertNotIn('xoxb-', self.text)
        self.assertIn(knowledge.REMOVED, self.files['notes/memory/2026-11-01.md'].decode())
        everything = knowledge.write(knowledge.collect(self.reader, knowledge.Options(messages=True, private=True)), Path(self.temp.name) / 'all')
        self.assertNotIn(TOKEN, '\n'.join(d.decode() for d in everything.values()))
        for line in ('password: hunter2hunter2hunter2', 'Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456', 'sk-abcdefghijklmnopqrstuvwx'):
            self.assertNotIn(line.split()[-1], knowledge.scrub('note ' + line))

    def test_message_text_only_when_asked(self):
        self.assertNotIn('BODY-SENTINEL', self.text)
        self.assertNotIn('Re: pricing', self.text)
        with_text = knowledge.render(knowledge.collect(self.reader, knowledge.Options(messages=True)))
        sources = [json.loads(line) for line in with_text['records/sources.jsonl'].decode().splitlines()]
        self.assertIn(SECRET_BODY, [s.get('text') for s in sources])
        self.assertIn('The message text is included.', with_text['README.md'].decode())

    def test_private_and_careful_content_only_when_asked(self):
        for left in ('Quiet Merger', 'Wants the merger kept quiet.', 'Reply about the quiet merger', 'Share the merger terms', 'Asked about the quiet merger',
                     'CAREFUL-SENTINEL', PRIVATE_BODY):
            self.assertNotIn(left, self.text)
        self.assertEqual(self.bundle['left_out'], {'private_projects': 1, 'private_facts': 1, 'private_fact_history': 1, 'private_summary_lines': 1,
                                                   'private_promises': 1, 'private_todos': 1, 'careful_team_briefs': 1})
        self.assertIn('Private threads, Only-you projects and Careful team content are left out', self.files['README.md'].decode())
        everything = '\n'.join(d.decode() for d in knowledge.render(knowledge.collect(self.reader, knowledge.Options(messages=True, private=True))).values())
        for found in ('Quiet Merger', 'Wants the merger kept quiet.', 'Reply about the quiet merger', 'Share the merger terms', 'CAREFUL-SENTINEL', PRIVATE_BODY):
            self.assertIn(found, everything)

    # -- files and the dashboard ---------------------------------------------------------------------------------------

    def test_zip_and_encrypted_zip(self):
        data = knowledge.zipped(self.bundle)
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            self.assertIn(f'{knowledge.FOLDER}/README.md', archive.namelist())
            self.assertTrue(all(n.startswith(knowledge.FOLDER + '/') for n in archive.namelist()))
        self.assertEqual(knowledge.zipped(self.bundle), data)  # the same export, the same bytes
        with self.assertRaisesRegex(ValueError, 'at least'):
            knowledge.encrypt(data, 'short')
        sealed = knowledge.encrypt(data, 'a long passphrase')
        self.assertNotIn(b'README', sealed)
        opened = subprocess.run(['openssl', 'enc', '-d', '-aes-256-cbc', '-pbkdf2', '-iter', '600000', '-md', 'sha256', '-pass', 'env:P'],
                                input=sealed, capture_output=True, env={**os.environ, 'P': 'a long passphrase'})
        self.assertEqual(opened.stdout, data)

    def test_dashboard_action_packs_once_for_the_owner(self):
        app = object.__new__(a.App)
        app.store, app.config, app.fleet = self.store, self.config, FakeFleet()
        self.assertIn('knowledge_export', a.OWNER_ACTIONS)
        self.assertIn('knowledge_export', a.DASHBOARD_ACTIONS)
        with self.assertRaisesRegex(ValueError, 'dashboard'):
            app.knowledge_export_action('knowledge_export', {}, False)
        with self.assertRaisesRegex(ValueError, 'at least'):
            app.knowledge_export_action('knowledge_export', {'passphrase': 'short'}, True)
        made = app.knowledge_export_action('knowledge_export', {'messages': True}, True)
        self.assertRegex(made['name'], r'^the-machine-knowledge-\d{4}-\d{2}-\d{2}\.zip$')
        self.assertIsNone(app.knowledge_take('wrong'))
        name, data = app.knowledge_take(made['token'])
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            self.assertIn(f'{knowledge.FOLDER}/README.md', archive.namelist())
        made = app.knowledge_export_action('knowledge_export', {'passphrase': 'a long passphrase'}, True)
        name, data = app.knowledge_take(made['token'])
        self.assertTrue(name.endswith('.zip.enc'))
        self.assertEqual(len(data), made['bytes'])
        self.assertIsNone(app.knowledge_take(made['token']))  # once


if __name__ == '__main__':
    unittest.main()
