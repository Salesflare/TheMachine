"""Bring these in (bring_in.py): the lines of someone's OpenClaw notes (MEMORY.md, USER.md) worth keeping as facts are
offered on Learning, and only the ones the owner ticks are saved. The files are only read; empty and template files
cost nothing and show nothing; keys and tokens never reach the model; one small pass, cached by each file's content
hash; a dismissed candidate does not come back. All notes here are made up."""
import base64
import importlib.util
import json
import os
from pathlib import Path
import re
import sqlite3
import tempfile
import unittest
import unittest.mock

spec = importlib.util.spec_from_file_location('bring_in_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import bring_in
import message_seal
import onboarding

MEMORY = '''# MEMORY.md

## People

- Mira at Lumenfold wants every quote as a PDF, never a link.
- Tomas from the school board only reads messages after 8 pm.
- Bought milk on Tuesday.

## Setup

- API key: MADE_UP_KEY
- Wifi password is hunter2hunter2 for the office
- (add more here)
- Role:

```
python3 ~/bin/backup.py --all the things
```
'''.replace('MADE_UP_KEY', 'sk-' + 'test_' + 'abcdefghijklmnop' + '1234')  # in pieces: no key-like literal in the repository
OPENCLAW_TEMPLATE = '# USER.md - User Model\n\n- Prefer ...\n- Avoid ...\n'


def judge(picks):
    """A stand-in judge: keeps the lines whose text holds one of `picks` (text -> kind). Records what it was given."""
    def ask(prompt):
        ask.prompts.append(prompt)
        found = []
        for n, text in re.findall(r'^\[(\d+)\] [A-Z]+\.md(?: \([^)]*\))?: (.*)$', prompt.split('Lines:\n<<<\n', 1)[1], re.M):
            for needle, kind in picks.items():
                if needle in text:
                    found.append({'n': int(n), 'text': text, 'kind': kind})
        return 'Here you go:\n' + json.dumps(found)
    ask.prompts = []
    return ask


class BringIn(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.workspace = Path(self.temp.name) / 'workspace'
        self.workspace.mkdir()
        self.config = {'owner_name': 'Robin Example', 'timezone': 'Europe/Brussels', 'accounts': []}

    def write(self, name, text):
        (self.workspace / name).write_text(text)

    def run_pass(self, ask):
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            state = bring_in.prepare(db, self.workspace, self.config)
            return bring_in.conclude(db, state, ask(state['prompt'])) if state['prompt'] else None

    def offered(self):
        with self.store.connect() as db:
            return bring_in.offered(db)

    def due(self, **more):
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            return bring_in.due(db, self.workspace, self.config, **more)

    def test_nothing_usable_means_no_pass_and_nothing_shown(self):
        self.assertFalse(self.due())  # no files at all
        self.write('MEMORY.md', '# MEMORY.md\n\n## Notes\n\n- (add more here)\n- Role:\n\n<!-- nothing yet -->\n')
        self.write('USER.md', OPENCLAW_TEMPLATE)
        self.assertFalse(self.due())
        self.assertEqual(bring_in.status(self.store.connect), [])
        self.assertNotIn('bring_in', self.store.snapshot([]))  # so the page draws nothing for it
        # The Machine's own starter and profile draft in USER.md say nothing it does not know already
        starter = onboarding.starter_user_md(self.config)
        self.assertTrue(onboarding.user_md_is_template(self.workspace / 'USER.md'))
        self.write('USER.md', starter + '\n' + onboarding.PROFILE_HEADING + '\n' + onboarding.PROFILE_MARK + '2026-01-05 -->\n\n- Tone: short and warm with customers\n')
        self.assertEqual(bring_in.usable('USER.md', (self.workspace / 'USER.md').read_text(), self.config), [])
        self.assertFalse(self.due())

    def test_keys_and_placeholders_never_reach_the_model(self):
        lines = [text for _, text in bring_in.usable('MEMORY.md', MEMORY)]
        self.assertEqual(lines, ['Mira at Lumenfold wants every quote as a PDF, never a link.', 'Tomas from the school board only reads messages after 8 pm.',
                                 'Bought milk on Tuesday.', 'Wifi password is hunter2hunter2 for the office'])
        self.write('MEMORY.md', MEMORY)
        ask = judge({'Wifi password': 'fact', 'Lumenfold': 'preference'})
        self.run_pass(ask)
        self.assertNotIn('sk-test_', ask.prompts[0])
        self.assertNotIn('backup.py', ask.prompts[0])
        self.assertIn('[1] MEMORY.md (People): Mira at Lumenfold', ask.prompts[0])
        self.assertIn('password', bring_in.JUDGE)  # a secret in plain words is the judge's to leave out, by meaning
        # a candidate that reads like a key is refused whatever the judge says
        self.assertEqual(bring_in.parse(json.dumps([{'n': 1, 'text': 'The token is ghp_abcdefghijklmnop123456', 'kind': 'fact'}]), 4), [])

    def test_only_ticked_ones_are_saved_with_their_source(self):
        self.write('MEMORY.md', MEMORY)
        self.assertTrue(self.due())
        self.assertEqual(self.run_pass(judge({'Lumenfold': 'preference', 'school board': 'fact', 'milk': 'rule'})), {'offered': 3})
        items = self.offered()
        self.assertEqual([(i['file'], i['kind']) for i in items], [('MEMORY.md', 'preference'), ('MEMORY.md', 'fact'), ('MEMORY.md', 'rule')])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM facts').fetchone()[0], 0)  # candidates are not facts
        self.assertEqual(len(self.store.snapshot([])['bring_in']), 3)
        done = bring_in.decide(self.store, keep=[items[0]['id'], items[2]['id']])
        self.assertEqual(done, {'saved': 2, 'dismissed': 0})
        facts = {f['text']: f for f in self.store.snapshot([])['facts']}
        kept = facts[items[0]['text']]
        self.assertEqual((kept['kind'], kept['fact_kind'], kept['source']), ('fact', 'preference', 'notes:MEMORY.md'))
        self.assertEqual(facts[items[2]['text']]['kind'], 'draft')  # a rule lands under How to do things
        self.assertEqual([i['id'] for i in self.offered()], [items[1]['id']])
        self.assertEqual(bring_in.decide(self.store, keep=[items[0]['id']]), {'saved': 0, 'dismissed': 0})  # once
        # the owner's own, not a connected AI's: reviews and preparations read it with the other facts
        self.assertIn(items[0]['text'], self.store.facts_text())
        self.assertNotIn(a.AI_FACTS_HEAD, self.store.facts_text())
        self.assertIn(items[0]['text'], self.store.facts_for('no-such-to-do'))
        # and it goes like any other
        self.store.forget_fact(kept['id'])
        self.assertNotIn(items[0]['text'], {f['text'] for f in self.store.snapshot([])['facts']})
        self.assertEqual([i['id'] for i in self.offered()], [items[1]['id']])  # removed is not offered again
        with self.assertRaises(ValueError):
            self.store.remember_fact('Mira wants quotes as a PDF.', 'notes:USER.md:1', source='notes:MEMORY.md')  # the id names its file

    def test_dismissed_ones_stay_away_and_new_lines_come_quietly(self):
        self.write('MEMORY.md', MEMORY)
        ask = judge({'Lumenfold': 'preference', 'school board': 'fact'})
        self.run_pass(ask)
        first, second = self.offered()
        self.assertEqual(bring_in.decide(self.store, dismiss=[first['id'], second['id']]), {'saved': 0, 'dismissed': 2})
        self.assertEqual(self.offered(), [])
        later = a.dt.datetime.now(a.dt.timezone.utc) + a.dt.timedelta(days=2)
        self.assertFalse(self.due(current=later))  # the file did not change: no model reads it again
        self.write('MEMORY.md', MEMORY + '\n- Quarterly numbers go to Ines at Quillstone before the board call.\n')
        self.assertFalse(self.due())  # not twice within a day
        self.assertTrue(self.due(current=later))
        ask = judge({'Lumenfold': 'preference', 'Quillstone': 'fact'})
        self.assertEqual(self.run_pass(ask), {'offered': 1})
        self.assertEqual(len(re.findall(r'^\[\d+\]', ask.prompts[0], re.M)), 1)  # only the new line is read
        self.assertIn('Mira at Lumenfold', ask.prompts[0].split('Offered before:')[1].split('Lines:')[0])
        self.assertEqual([i['text'] for i in self.offered()], ['Quarterly numbers go to Ines at Quillstone before the board call.'])
        self.assertEqual(self.run_pass(lambda prompt: json.dumps([{'n': 1, 'text': first['text'], 'kind': 'fact'}])), None)

    def test_known_facts_are_given_and_not_offered_again(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind) VALUES(?,'d1',NULL,?,'fact')",
                       ('Tomas from the school board only reads messages after 8 pm.', a.now()))
        self.write('MEMORY.md', MEMORY)
        ask = judge({'school board': 'fact'})
        self.assertEqual(self.run_pass(ask), {'offered': 0})
        self.assertIn('Tomas from the school board', ask.prompts[0].split('Already known:')[1].split('Offered before:')[0])
        self.assertEqual(self.offered(), [])

    def test_a_failed_pass_tries_again_then_lets_the_lines_be(self):
        self.write('MEMORY.md', MEMORY)
        later = a.dt.datetime.now(a.dt.timezone.utc)
        for attempt in range(bring_in.TRIES):
            later += a.dt.timedelta(days=2)
            self.assertTrue(self.due(current=later), attempt)
            self.assertEqual(self.run_pass(lambda prompt: 'no list here' if attempt else None), {'error': 'bad_answer' if attempt else 'no_answer'})
        self.assertFalse(self.due(current=later + a.dt.timedelta(days=2)))
        self.assertEqual(self.offered(), [])

    def test_user_md_is_marked_and_a_long_file_is_read_over_days(self):
        self.write('USER.md', '# About me\n\n- Northwind Freight is our oldest customer: their mails go first.\n')
        self.write('MEMORY.md', '\n'.join(f'- Supplier number {n} delivers on weekday {n % 5 + 1} before noon, always.' for n in range(300)))
        ask = judge({})
        self.run_pass(ask)
        self.assertLess(len(ask.prompts[0]), bring_in.PASS_CHARS + len(bring_in.JUDGE) + 500)
        self.assertIn('USER.md are already read whole', ask.prompts[0])
        with self.store.connect() as db:
            rest, _ = bring_in.unread(db, self.workspace, self.config)
        self.assertTrue(rest)  # the rest waits for another day
        self.assertEqual(rest[-1]['file'], 'USER.md')

    def test_the_files_are_only_read(self):
        self.write('MEMORY.md', MEMORY)
        self.write('USER.md', '# About me\n\n- Northwind Freight is our oldest customer: their mails go first.\n')
        before = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.workspace.iterdir()}
        self.run_pass(judge({'Lumenfold': 'preference', 'Northwind': 'fact'}))
        items = self.offered()
        bring_in.decide(self.store, keep=[items[0]['id']], dismiss=[items[1]['id']])
        self.assertEqual({p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.workspace.iterdir()}, before)
        source = Path(bring_in.__file__).read_text() + Path(a.__file__).with_name('bring_in_app.py').read_text()
        self.assertIsNone(re.search(r'write_text|write_bytes|\.unlink|\.rename|shutil|os\.remove|open\([^)]*[\'"][wa+]', source))

    def test_once_a_day_within_the_budget_and_only_the_owner_decides(self):
        self.write('MEMORY.md', MEMORY)
        app = object.__new__(a.App)
        app.store, app.config, app.fleet, app.bring_in_dir = self.store, self.config, None, self.workspace
        app.background_at = 0
        helpers = {'model': lambda config: None}
        app.background_pause = lambda **k: None
        self.assertFalse(app.bring_in_step(helpers))  # not before the first look
        self.store.first_magic_done = lambda db: True
        app.background_pause = lambda **k: {'window': '5h'}
        self.assertFalse(app.bring_in_step(helpers))  # the budget holds it
        app.background_pause = lambda **k: None
        app.bring_in_model = judge({'Lumenfold': 'preference'})
        self.assertTrue(app.bring_in_step(helpers))
        app.bring_in_thread.join(10)
        self.assertEqual(len(app.bring_in_model.prompts), 1)
        app.background_at = 0
        self.assertFalse(app.bring_in_step(helpers))  # not again today
        item = self.offered()[0]
        with self.assertRaises(ValueError):
            app.action('bring_in_decide', {'keep': [item['id']]})  # the owner's, on the dashboard
        done = app.action('bring_in_decide', {'keep': [item['id']]}, owner_dashboard=True)
        self.assertEqual((done['saved'], done['bring_in']), (1, []))
        self.assertIn('bring_in_decide', a.DASHBOARD_ACTIONS)
        self.assertIn('bring_in_decide', a.OWNER_ACTIONS)

    def test_the_demo_state_has_nothing_to_bring_in(self):
        import sys
        sys.path.insert(0, str(Path(a.__file__).parent / 'sandbox'))
        import load
        self.assertNotIn('notes', load.parse_states('all'))  # the site's demo is recorded from `all`
        self.assertIn('notes', load.STATES)


class Locked(unittest.TestCase):
    """A sealed Machine whose message key is missing or is another one: its candidates cannot be read. The dashboard
    keeps the section hidden and says so once in the log; a pass and the owner's tick fail, so sealed bytes are never
    offered again, shown or saved as a fact."""
    def setUp(self):
        patcher = unittest.mock.patch.dict(os.environ)  # sealed here, whatever the suite runs as
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop('MESSAGE_PROTECTION_TEST', None)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'events.sqlite'
        self.workspace = Path(self.temp.name) / 'workspace'
        self.workspace.mkdir()
        (self.workspace / 'MEMORY.md').write_text(MEMORY)
        store = a.Store(self.path, protect=True)
        with store.connect() as db:
            bring_in.ensure(db)
        with store.connect() as db:
            state = bring_in.prepare(db, self.workspace, {})
            self.assertEqual(bring_in.conclude(db, state, judge({'Lumenfold': 'preference'})(state['prompt'])), {'offered': 1})
            self.item = bring_in.offered(db)[0]
        (self.workspace / 'MEMORY.md').write_text(MEMORY + '\n- Odile at Brightwater signs off every invoice herself.\n')  # a new line to read
        self.key = message_seal.key_path(self.path)
        bring_in._warned = False
        self.addCleanup(setattr, bring_in, '_warned', False)

    def unchanged(self):
        with sqlite3.connect(self.path) as raw:
            self.assertEqual(raw.execute('SELECT status,typeof(text),fact_id FROM bring_in_items').fetchall(), [('offered', 'blob', None)])
            self.assertEqual(raw.execute('SELECT count(*) FROM facts').fetchone()[0], 0)

    def another_key(self):
        self.key.write_bytes(base64.b64encode(os.urandom(32)) + b'\n')
        return a.Store(self.path)

    def test_the_dashboard_keeps_the_section_hidden_and_says_so_once(self):
        store = self.another_key()
        with self.assertLogs('personal-assistant', 'WARNING') as logged:
            self.assertEqual(bring_in.status(store.connect), [])
        self.assertEqual(len(logged.output), 1)
        self.assertNotIn(self.item['text'], logged.output[0])
        with self.assertNoLogs('personal-assistant', 'WARNING'):
            self.assertEqual(bring_in.status(store.connect), [])  # once, not at every load of the page
        self.assertNotIn('bring_in', store.snapshot([]))  # and the rest of the status is still there
        self.unchanged()

    def test_without_the_key_nothing_is_shown_either(self):
        self.key.unlink()

        def keyless():
            db = sqlite3.connect(self.path)
            db.row_factory = sqlite3.Row
            return db
        with keyless() as db, self.assertRaises(message_seal.SealError):
            bring_in.offered(db, made=True)
        with self.assertLogs('personal-assistant', 'WARNING'):
            self.assertEqual(bring_in.status(keyless), [])
        self.unchanged()

    def test_a_pass_fails_rather_than_offer_on_top_of_what_it_cannot_read(self):
        store = self.another_key()
        with store.connect() as db:
            self.assertTrue(bring_in.due(db, self.workspace, {}, current=bring_in.dt.datetime.now(bring_in.dt.timezone.utc) + bring_in.dt.timedelta(days=2)))
            with self.assertRaises(message_seal.SealError):
                bring_in.prepare(db, self.workspace, {})
        app = object.__new__(a.App)
        app.store, app.config, app.fleet, app.bring_in_dir = store, {}, None, self.workspace
        app.bring_in_model = judge({'Brightwater': 'fact'})
        with self.assertLogs('personal-assistant', 'WARNING'):
            self.assertEqual(app.bring_in_run({}), {'error': 'SealError'})
        self.assertEqual(app.bring_in_model.prompts, [])  # no turn was spent
        with store.connect() as db:
            self.assertFalse(bring_in.due(db, self.workspace, {}))  # and not at every step: a day later at the earliest
        self.unchanged()

    def test_a_tick_fails_rather_than_save_what_does_not_open(self):
        store = self.another_key()
        with self.assertRaises(message_seal.SealError):
            bring_in.decide(store, keep=[self.item['id']])
        app = object.__new__(a.App)
        app.store, app.config, app.fleet = store, {}, None
        with self.assertRaises(message_seal.SealError):
            app.action('bring_in_decide', {'keep': [self.item['id']]}, owner_dashboard=True)
        self.unchanged()


if __name__ == '__main__':
    unittest.main()
