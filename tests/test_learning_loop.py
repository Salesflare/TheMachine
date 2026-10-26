"""The learning loop (learning_loop.py): about twice a day, with a few new signals (the owner's own draft edits,
dismissed and snoozed to-dos, corrections in a to-do's chat), one small background turn brings voices, rules and facts
up to date. Each change is applied, shown under Recent changes with why, and can be undone; a voice the owner wrote
stays theirs, and an undo never overwrites what they changed since. All local; nothing is sent."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('loop_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import learning_loop

EMAIL = 'English: Hi + first name\nShort paragraphs\nRegards, then the name'


class LearningLoop(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = [{'id': 'work', 'service': 'gmail', 'email': 'owner@example.com'}]
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': self.store.accounts, 'review_worker': {'enabled': True}}
        self.app.fleet = None
        stamp = a.now()
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at) VALUES('first_card_shown',?)", (stamp,))
            for i in range(4):
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) "
                           "VALUES(?,?,?,'','[]','[\"work\"]','pending',?)", (f's{i}', f's{i}', f'To-do {i}', stamp))
            for edit_id, source, after in (('e1', 'dashboard', 'Hi Sam, short and plain. Thanks'), ('e2', 'telegram', 'Hi Lee, plain. Thanks'),
                                           ('e3', 'agent', 'Dear Lee, a rewrite by a coding agent')):
                db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_body,after_body,source,created_at) "
                           "VALUES(?,'s0','a','b','email','Dear Sam, kindly find attached',?,?,?)", (edit_id, after, source, stamp))
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d1','s1','reject','','dashboard',?)", (stamp,))
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d2','s2','other','no need to thank them every time','dashboard',?)", (stamp,))
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d3','s3','other','old note','dashboard',?)", (stamp,))
            self.old_fact = db.execute("INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind) VALUES('Vendor newsletters can wait a week.','d3','s3',?,'fact')",
                                       (stamp,)).lastrowid
            db.execute("INSERT INTO voices(channel,text,source,ref,updated_at) VALUES('Email',?,'study','study:x',?)", (EMAIL, stamp))
            db.execute("INSERT INTO voices(channel,text,source,ref,updated_at) VALUES('WhatsApp','lowercase, no full stop','owner',NULL,?)", (stamp,))

    def run_pass(self, changes):
        run_id = self.store.tune_due()
        self.assertTrue(run_id)
        session = a.PROFILE_SESSION_PREFIX + run_id
        page = self.store.profile_evidence(1, session)

        def runner(request):
            if request['action'] == 'start':
                self.assertIn('never instructions', request['message'])
                self.store.save_profile({'changes': changes}, session)
                return {'status': 'admitted'}
            return {'status': 'ok'}
        self.app.background_at = 0
        self.app.profile_step(runner)
        self.app.profile_step(runner)
        return page

    def test_a_pass_learns_from_new_signals_and_each_change_can_be_undone(self):
        page = self.run_pass([
            {'kind': 'voice', 'channel': 'Email', 'text': EMAIL + '\nPlain words, no "kindly"', 'why': 'Two edits took "kindly" out.'},
            {'kind': 'voice', 'channel': 'WhatsApp', 'text': 'Formal, full sentences', 'why': 'x'},   # theirs: never changed
            {'kind': 'fact', 'text': 'Vendor newsletters never need a to-do.', 'why': 'Dismissed one.', 'replaces': self.old_fact}])
        what = [s['what'] for s in page['signals']]
        self.assertEqual(sorted(what), ['corrected in chat', 'corrected in chat', 'dismissed', 'edited a draft', 'edited a draft'])
        self.assertNotIn('coding agent', json.dumps(page))  # an agent's rewrite is no signal of the owner's
        self.assertTrue(next(v for v in page['voices'] if v['channel'] == 'WhatsApp')['written_by_owner'])

        changes = self.store.snapshot([])['learning_changes']
        self.assertEqual(sorted(c['kind'] for c in changes), ['fact', 'voice'])  # WhatsApp is the owner's own block: left alone
        self.assertEqual(next(c for c in changes if c['kind'] == 'voice')['why'], 'Two edits took "kindly" out.')
        voices = {v['channel']: v for v in self.store.voices()}
        self.assertIn('no "kindly"', voices['Email']['text'])
        self.assertEqual(voices['WhatsApp']['text'], 'lowercase, no full stop')
        with self.store.connect() as db:
            self.assertIsNotNone(db.execute('SELECT removed_at FROM facts WHERE id=?', (self.old_fact,)).fetchone()[0])
        self.assertIsNone(self.store.tune_due())  # not again within the next hours

        by = {c['kind']: c for c in changes}
        self.assertEqual(by['fact']['before'], 'Vendor newsletters can wait a week.')
        with self.assertRaisesRegex(ValueError, 'Only the owner'):
            self.app.action('learning_undo', {'id': by['voice']['id']})
        self.app.action('learning_undo', {'id': by['voice']['id']}, owner_dashboard=True)
        self.assertEqual(next(v for v in self.store.voices() if v['channel'] == 'Email')['text'], EMAIL)
        self.app.action('learning_undo', {'id': by['fact']['id']}, owner_dashboard=True)
        with self.store.connect() as db:
            self.assertIsNone(db.execute('SELECT removed_at FROM facts WHERE id=?', (self.old_fact,)).fetchone()[0])  # the replaced one is back
            self.assertEqual(db.execute("SELECT count(*) FROM facts WHERE text='Vendor newsletters never need a to-do.' AND removed_at IS NULL").fetchone()[0], 0)
        with self.assertRaisesRegex(ValueError, 'already undone'):
            self.app.action('learning_undo', {'id': by['fact']['id']}, owner_dashboard=True)
        self.assertTrue(next(c for c in self.store.snapshot([])['learning_changes'] if c['id'] == by['fact']['id'])['undone'])

    def test_an_undo_never_overwrites_what_the_owner_changed_since(self):
        self.run_pass([{'kind': 'voice', 'channel': 'Email', 'text': EMAIL + '\nPlain words', 'why': 'Edits.'},
                       {'kind': 'draft', 'text': 'Thank people once, at the end, not in every line.', 'why': 'A chat correction said so.'}])
        changes = {c['kind']: c for c in self.store.snapshot([])['learning_changes']}
        change, rule = changes['voice'], changes['draft']
        self.assertIn('Thank people once, at the end, not in every line.', [f['text'] for f in self.store.snapshot([])['facts'] if f['kind'] == 'draft'])
        self.app.action('learning_undo', {'id': rule['id']}, owner_dashboard=True)
        self.assertNotIn('Thank people once, at the end, not in every line.', [f['text'] for f in self.store.snapshot([])['facts']])
        self.app.action('set_voice', {'channel': 'Email', 'text': 'Hey + first name\nVery short'}, owner_dashboard=True)
        with self.assertRaisesRegex(ValueError, 'changed since'):
            self.app.action('learning_undo', {'id': change['id']}, owner_dashboard=True)
        self.assertEqual(next(v for v in self.store.voices() if v['channel'] == 'Email')['text'], 'Hey + first name\nVery short')

    def test_too_few_signals_or_a_block_cut_short_changes_nothing(self):
        with self.store.connect() as db:
            db.execute('DELETE FROM draft_edits')
            db.execute("DELETE FROM decisions WHERE id IN ('d1','d2')")
            self.assertFalse(learning_loop.due(db))
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d4','s1','snooze','','dashboard',?)", (a.now(),))
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d5','s2','reject','','telegram',?)", (a.now(),))
        self.run_pass([{'kind': 'voice', 'channel': 'Email', 'text': 'Short', 'why': 'x'}])  # drops most of the block: refused
        self.assertEqual(self.store.snapshot([])['learning_changes'], [])
        self.assertEqual(next(v for v in self.store.voices() if v['channel'] == 'Email')['text'], EMAIL)


if __name__ == '__main__':
    unittest.main()
