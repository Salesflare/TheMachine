"""One way to read memory (machine/app/recall.py) and the log of what was read (memory_use.py)."""
import datetime as dt
import functools
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from seams import patch_everywhere

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('memory_use_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import memory_use  # noqa: E402
import retention  # noqa: E402
import search_ask  # noqa: E402
import work_removal  # noqa: E402
from machine.app import preparation as preparation_app, review as review_app, search_ask as ask_app  # noqa: E402
from machine.app import ask_memory  # noqa: E402
from machine.app.recall import recall  # noqa: E402
from machine.export import inventory  # noqa: E402

NOW = dt.datetime(2026, 10, 16, 12, tzinfo=dt.timezone.utc)
OLD = '2026-09-01T00:00:00+00:00'
SETTINGS = {'url': 'http://embed.invalid', 'model': 'm', 'dims': 2}
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.com'}], 'embeddings': SETTINGS, 'review_worker': {'enabled': True}}


def mail(n, days, sender, title, body):
    return {'account_id': 'work', 'source_id': f'p{n}', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(days=days)).isoformat(),
            'title': title, 'body': body, 'deleted': False,
            'metadata': {'from': sender, 'to': 'sam@acme.com', 'cc': '', 'labels': ['INBOX'], 'message-id': f'<p{n}@x>', 'thread_id': f'tp{n}'}}


def embed(settings, texts, timeout=120):
    return [[1.0, 0.0] if 'number 3 ' in t or 'number 7 ' in t or 'Answer Ann' in t else [0.0, 1.0] for t in texts]


class Before:
    """How the builders read memory before recall(): each picker called where its text goes, with the builder's own
    length check, and nothing kept of what was picked."""

    def __init__(self, app, purpose, about=None, budget=0):
        store, todo, known = app.store, (about or {}).get('todo'), a.embeddings.settings(app.config)
        self.budget = budget
        self.pickers = {
            'history': lambda: store.preference_summary(), 'promises': lambda: store.promises_text(),
            'facts': (lambda: store.facts_text(ids=True)) if purpose == 'review' else
                     (lambda: store.facts_for(todo, 'fact', known, accounts=app.config.get('accounts', []))),
            'rules': lambda: store.facts_for(todo, 'draft', known), 'records': lambda: app.graph_lines(todo),
            'skills': lambda rules, room: app.prep_skill_lines(todo, rules, room), 'team': lambda: app.fleet.lines(todo),
            'related': lambda: app.related_lines(todo), 'sources': search_ask.ask}
        if purpose == 'ask':  # what matches the question, each picker with (what it goes on, room)
            self.pickers.update({name: functools.partial(picker, app) for name, picker in ask_memory.BLOCKS.items()})

    def drop(self, block):
        pass

    def read(self, block, *args, **kwargs):
        return self.pickers[block](*args, **kwargs)

    text = read

    def fit(self, block, used, reserve=0, *args, **kwargs):
        lines = self.read(block, *args, **kwargs)
        return lines if used + len(lines) < self.budget - reserve else ''

    def rows(self):
        return []


class MemoryUseTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        self.store = a.Store(self.dir / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {**CONFIG, 'database': str(self.dir / 'events.sqlite'), 'openclaw_workspace': str(self.dir / 'ws')}
        for started in (patch_everywhere(a, 'now', lambda: NOW.isoformat()), patch.object(a.embeddings, 'embed', side_effect=embed),
                        patch.object(a.embeddings, 'related', return_value=[(2, 0.83)])):
            started.start()
            self.addCleanup(started.stop)
        search_ask._asked.clear()
        self.store.commit_page('work', {}, [mail(1, 3, 'Ann Example <ann@client.com>', 'Pilot timing', 'Can the pilot move to March?'),
                                            mail(2, 5, 'Ann Example <ann@client.com>', 'Pilot budget', 'The budget for the pilot is approved.'),
                                            mail(3, 9, 'Lee Park <lee@globex.example>', 'Invoice', 'The September invoice is still open.')])
        with self.store.connect() as db:
            db.isolation_level = None
            a.graph.build(db, self.app.config, NOW.isoformat())
        other = self.store.suggest('other', 'Pay the vendor', 'Body', [3])['id']
        self.store.decide(other, 'reject', 'we stopped using them', 'owner-note', 'dashboard')
        self.other = other
        for i in range(30):
            self.store.remember_fact(f'General fact number {i} about how the owner works with pilots.', 'owner-note')
        self.store.remember_fact('Keep replies under five sentences.', 'owner-note', 'draft')
        self.store.promise({'direction': 'theirs', 'event_id': 1, 'who': 'Ann Example', 'what': 'send the signed contract', 'due': '2026-10-23'})
        self.todo = self.store.suggest('pilot', 'Answer Ann about the pilot', 'Ann asks to move the pilot.', [1])['id']
        with self.store.connect() as db:
            db.execute('UPDATE facts SET used_at=?', (OLD,))
        self.store.decide(self.todo, 'accept', '', 'click', 'dashboard')

    def log(self, where='1=1', args=()):
        with self.store.connect() as db:
            return [tuple(r) for r in db.execute(f'SELECT purpose,kind,row_id,how,chars,run_id,suggestion_id,score FROM memory_use WHERE {where} ORDER BY id', args)]

    def prepare(self, status='admitted'):
        calls = []
        with self.store.connect() as db:  # a start the runner couldn't take is tried again at once here
            db.execute('UPDATE preparations SET retry_at=NULL')
        self.app.preparation_step(lambda r: calls.append(dict(r)) or {'status': status})
        return next(c for c in calls if c.get('message'))

    def review(self, status='admitted', run='review-1'):
        with self.store.connect() as db:
            db.execute("INSERT OR REPLACE INTO review_runs(run_id,status,started_at,updated_at,attempts,planned) VALUES(?,'starting',?,?,0,1)",
                       (run, NOW.isoformat(), NOW.isoformat()))
        calls = []
        self.app.review_step(lambda r: calls.append(dict(r)) or {'status': status})
        return next(c for c in calls if c.get('message'))

    def ask(self):
        prompts = []

        def model(config, text):
            if 'reply with one JSON object' in text:
                return json.dumps({'question': True, 'person': None, 'said_by': 'both', 'from': None, 'to': None, 'about': ''})
            prompts.append(text)
            return 'It moves to March [1].'
        self.app.ask_model = model
        search_ask._asked.clear()
        with patch.object(a.embeddings, 'related', return_value=[(1, 0.9), (2, 0.7)]):
            self.app.search_ask('When does the pilot move?', None, None)
        return prompts[0]

    # The model sees what it saw before

    def same(self, module, build):
        new = build()
        with patch.object(module, 'recall', Before):
            old = build()
        self.assertEqual(old, new)
        return new

    def test_the_preparation_prompt_is_the_same_text(self):
        message = self.same(preparation_app, lambda: self.prepare('unavailable')['message'])
        for part in ('Keep replies under five sentences.', 'General fact number 3 ', 'Ann Example (ann@client.com)', 'Pilot budget'):
            self.assertIn(part, message)  # rules, facts, records and related signals are all in the text compared

    def test_the_review_prompt_is_the_same_text(self):
        message = self.same(review_app, lambda: self.review('unavailable')['message'])
        for part in ('- [1] General fact number 0', 'Pay the vendor (owner wrote: "we stopped using them")', 'send the signed contract'):
            self.assertIn(part, message)

    def test_the_ask_prompt_is_the_same_text(self):
        text = self.same(ask_app, self.ask)
        for part in ('Pilot timing', '[P1] Promise by Ann Example to the owner, open, due 2026-10-23', '[F1] Learned 2026-10-16'):
            self.assertIn(part, text)  # the messages, and what the Machine keeps that matches the question

    # The log

    def test_a_preparation_logs_each_item_once_with_its_kind_id_and_how(self):
        request = self.prepare()
        rows = self.log()
        self.assertEqual(len(rows), len({r[1:3] for r in rows}))  # once each
        self.assertTrue(all(r[0] == 'preparation' and r[6] == self.todo and r[5] and r[4] > 0 for r in rows))
        by_kind = {}
        for r in rows:
            by_kind.setdefault(r[1], []).append(r)
        self.assertEqual([('31', 'always')], [r[2:4] for r in by_kind['rule']])
        self.assertEqual({('4', 'closeness'), ('8', 'closeness')}, {r[2:4] for r in by_kind['fact']})
        self.assertTrue(all(r[7] is not None for r in by_kind['fact']))
        self.assertEqual([('email:ann@client.com', 'about')], [r[2:4] for r in by_kind['record']])
        self.assertEqual([('2', 'closeness', 0.83)], [(r[2], r[3], r[7]) for r in by_kind['signal']])
        for r in by_kind['fact']:  # the characters are those of its line in the prompt
            self.assertIn(f'General fact number {int(r[2]) - 1} ', request['message'])
        self.assertNotIn('_memory', json.dumps([k for k in request if not k.startswith('_')]))

    def test_a_review_and_an_ask_log_what_they_read(self):
        message = self.review()['message']
        rows = self.log("purpose='review'")
        self.assertEqual(len(rows), len({r[1:3] for r in rows}))
        self.assertTrue(all(r[5] == 'review-1' and r[6] == '' for r in rows))
        listed = re.findall(r'^- \[(\d+)\] ', message, re.M)
        self.assertEqual(sorted(listed), sorted(r[2] for r in rows if r[1] == 'fact'))
        self.assertEqual({'always'}, {r[3] for r in rows if r[1] == 'fact'})
        self.assertEqual([('1', 'always')], [r[2:4] for r in rows if r[1] == 'promise'])
        self.assertIn((self.other, 'recency'), [r[2:4] for r in rows if r[1] == 'history'])
        self.ask()
        rows = self.log("purpose='ask'")
        self.assertEqual([('signal', '1', 'search'), ('signal', '2', 'search')], sorted(r[1:4] for r in rows if r[1] == 'signal'))
        self.assertEqual([('promise', '1', 'search')], [r[1:4] for r in rows if r[1] == 'promise'])  # the promise in a message it found
        facts = [r for r in rows if r[1] == 'fact']  # the closest in meaning to the question, with how close
        self.assertEqual((ask_memory.FACTS, {'closeness'}), (len(facts), {r[3] for r in facts}))
        self.assertTrue(all(r[7] is not None and r[7] >= ask_memory.FACT_FLOOR for r in facts))
        with self.store.connect() as db:  # read for a question: used, like one picked for a to-do
            self.assertEqual(ask_memory.FACTS, db.execute('SELECT count(*) FROM facts WHERE used_at>?', (OLD,)).fetchone()[0])

    def test_the_log_has_no_text(self):
        self.prepare()
        with self.store.connect() as db:
            columns = {c[1] for c in db.execute('PRAGMA table_info(memory_use)')}
            dump = json.dumps([list(r) for r in db.execute('SELECT * FROM memory_use')])
        self.assertEqual({'id', 'at', 'purpose', 'run_id', 'suggestion_id', 'kind', 'row_id', 'how', 'score', 'chars'}, columns)
        for text in ('General fact', 'five sentences', 'Pilot budget', 'Ann Example'):
            self.assertNotIn(text, dump)

    def test_a_prompt_that_was_not_sent_logs_nothing(self):
        self.prepare('unavailable')
        self.review('unavailable')
        self.assertEqual([], self.log())

    def test_a_failed_log_write_does_not_fail_the_build(self):
        with self.store.connect() as db:
            db.execute('DROP TABLE memory_use')
        with self.assertLogs(a.LOG, 'ERROR'):
            self.assertIn('General fact number 3 ', self.prepare()['message'])
        with self.store.connect() as db:
            self.assertEqual('running', db.execute('SELECT status FROM preparations WHERE suggestion_id=?', (self.todo,)).fetchone()[0])
        with self.assertLogs(a.LOG, 'ERROR'):
            self.assertEqual(0, memory_use.record(self.store, 'ask', [['signal', '1', 'search', None, 10, 0]]))

    def test_a_picker_outside_a_recall_notes_nothing(self):
        self.assertFalse(memory_use.collecting())
        memory_use.note('fact', 1, 'text', 'always')
        memory = recall(self.app, 'review')
        self.assertTrue(memory.text('facts'))
        self.assertEqual({'fact'}, set(memory.picked()))
        item = memory.picked()['fact'][0]
        self.assertEqual(('always', 'note', True), (item.how, item.source, item.text.startswith('- [')))
        self.assertFalse(memory_use.collecting())
        with self.assertRaises(ValueError):
            memory_use.Recalled('else')

    def test_a_block_that_does_not_fit_is_not_logged(self):
        memory = recall(self.app, 'preparation', {'todo': self.todo}, 1200)
        self.assertEqual('', memory.fit('records', 100, 1000))
        self.assertTrue(memory.fit('related', 100, 500))
        self.assertEqual({'signal'}, set(memory.picked()))

    # Last used

    def used(self):
        with self.store.connect() as db:
            return {r[0]: r[1] for r in db.execute('SELECT id,used_at FROM facts')}

    def test_used_at_follows_prompts_that_were_sent(self):
        self.prepare('unavailable')
        self.assertEqual({OLD}, set(self.used().values()))  # picked, but the prompt never ran
        self.review()
        self.assertEqual({OLD}, set(self.used().values()))  # a review lists them all: that is not a use
        self.prepare()
        used = self.used()
        self.assertEqual({4, 8}, {i for i, at in used.items() if at != OLD})  # the two picked as close to the to-do
        with self.store.connect() as db:
            self.assertEqual({'4', '8', '9'}, set(memory_use.last_used(db, 'fact', [4, 8, 9])))  # read: the review listed 9 too
            self.assertEqual({}, memory_use.last_used(db, 'skill'))
            self.assertEqual(['fact', 'history', 'promise', 'record', 'rule', 'signal'], sorted(memory_use.counts(db)['kinds']))

    # Retention, export, delete

    def test_retention_prunes_old_rows(self):
        for days in (61, 59):
            memory_use.record(self.store, 'ask', [['signal', str(days), 'search', None, 10, 0]], at=(NOW - dt.timedelta(days=days)).isoformat())
        report = retention.run(self.store.connect, str(self.dir / 'events.sqlite'), now=NOW, busy=0)
        self.assertEqual(1, report['memory_use'])
        self.assertEqual(['59'], [r[2] for r in self.log()])

    def test_the_export_has_it_and_it_stays_on_the_machine(self):
        self.assertEqual('memories', inventory.part_of('memory_use'))
        for name in ('shared_graph.py', 'shared_graph_app.py', 'shared_graph_kept.py', 'support.py', 'support_app.py', 'fleet_learnings.py'):
            text = (ROOT / name).read_text()
            self.assertNotIn('FROM memory_use', text, name)
            self.assertNotIn('memory_use.outcomes', text, name)
            self.assertNotIn('memory_use.summary', text, name)

    def test_removing_the_account_or_the_person_empties_it(self):
        self.prepare()
        self.assertTrue(self.log("kind='record'"))
        self.app.delete_person('email:ann@client.com', self.dir / 'ws')
        self.assertEqual([], self.log("kind='record'"))
        self.assertTrue(self.log())

    def test_removing_the_account_takes_its_to_dos_rows(self):
        self.prepare()
        memory_use.record(self.store, 'ask', [['signal', '1', 'search', None, 10, 0]])
        work_removal.purge(self.app.config, ['work'], self.store)
        self.assertEqual(['ask'], [r[0] for r in self.log()])  # an ask's rows are ids of signals, tied to no to-do

    # What the owner then did

    def test_outcomes_join_what_was_read_with_what_the_owner_did(self):
        todos = {name: self.store.suggest(name, f'To-do {name}', 'Body', [2])['id'] for name in ('plain', 'edited', 'dropped')}
        for n, (name, todo) in enumerate(todos.items()):
            rows = [['fact', '4', 'closeness', 0.9, 40, 1], ['signal', '2', 'closeness', 0.8, 60, 0]] + ([['rule', '31', 'weight', None, 30, 0]] if n else [])
            memory_use.record(self.store, 'preparation', rows, f'prep-{name}', todo)
        with self.store.connect() as db:
            for name in ('plain', 'edited'):
                db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) "
                           "VALUES(?,?,'r1','{}','sent',?,?,'ap','dashboard','<m>')", ('job-' + name, todos[name], NOW.isoformat(), NOW.isoformat()))
            db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_body,after_body,source,created_at) "
                       "VALUES('e1',?,'r0','r1','email','Before','After','dashboard',?)", (todos['edited'], NOW.isoformat()))
            db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_body,after_body,source,created_at) "
                       "VALUES('e2',?,'r0','r1','email','Before','After','agent',?)", (todos['plain'], NOW.isoformat()))
        self.store.decide(todos['dropped'], 'reject', 'not now', 'drop-note', 'dashboard')
        with self.store.connect() as db:
            got = {name: memory_use.outcomes(db, todo) for name, todo in todos.items()}
            summary = memory_use.summary(db)
            self.assertIsNone(memory_use.outcomes(db, 'nope'))
        self.assertEqual({'plain': 'sent_unchanged', 'edited': 'sent_edited', 'dropped': 'dismissed'}, {n: g['outcome'] for n, g in got.items()})
        self.assertEqual((1, 0, 1), (got['edited']['edits'], got['plain']['edits'], got['dropped']['decisions']['reject']))
        self.assertEqual([('fact', '4', 'closeness'), ('signal', '2', 'closeness'), ('rule', '31', 'weight')],
                         [(m['kind'], m['row_id'], m['how']) for m in got['edited']['memory']])
        self.assertEqual(1, got['edited']['prompts'])
        self.assertEqual({'prompts': 3, 'sent_unchanged': 1, 'sent_edited': 1, 'dismissed': 1, 'snoozed': 0, 'open': 0}, summary['kinds']['fact'])
        self.assertEqual({'prompts': 2, 'sent_unchanged': 0, 'sent_edited': 1, 'dismissed': 1, 'snoozed': 0, 'open': 0}, summary['items'][('rule', '31')])
        self.assertNotIn('To-do', json.dumps({'kinds': summary['kinds'], 'items': sorted(map(list, summary['items']))}))


if __name__ == '__main__':
    unittest.main()
