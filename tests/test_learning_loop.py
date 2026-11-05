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

    def test_the_why_and_what_is_learned_say_you_never_the_owners_name(self):
        # "Jeroen explicitly corrected the Canadian tax review task" under a change: the prompts ask for "you" and no
        # filler; an older line that names the owner reads "You corrected …" on Learning, the stored line unchanged.
        self.assertIn('never their name', learning_loop.prompt('r1'))
        self.assertIn('"explicitly"', learning_loop.prompt('r1'))
        self.assertIn(a.OWNER_YOU, a.FACT_KIND_HINT)
        self.assertIn(a.FACTS_YOU, a.review_prompt('run', ['work'], '', '- You prefer short replies.'))
        cases = {'Sam explicitly corrected the tax review to-do: “use the portal”.': 'You corrected the tax review to-do: “use the portal”.',
                 'On October 31, Sam corrected the coffee to-do. Sam’s note said online.': 'On October 31, you corrected the coffee to-do. Your note said online.',
                 'In the venue chat, Sam repeatedly asked for a doc.': 'In the venue chat, you repeatedly asked for a doc.',
                 'The owner wrote back twice.': 'You wrote back twice.',
                 'Sam wants to meet online.': 'Sam wants to meet online.',  # no safe "you" form: left alone
                 'Samuel asked for it.': 'Samuel asked for it.'}
        for before, after in cases.items():
            self.assertEqual(learning_loop.to_you(before, ['Sam']), after)
        workspace = Path(self.temp.name) / 'workspace'
        workspace.mkdir()
        (workspace / 'USER.md').write_text('# USER.md - About Sam\n\n- Name: Sam Rivera\n', encoding='utf-8')
        self.app.config['openclaw_workspace'] = str(workspace)
        self.assertEqual(self.app.owner_first_names(), ['Sam'])
        with self.store.connect() as db:
            learning_loop.record(db, 'r1', 'fact', '1', None, 'You prefer online meetings.', 'Sam explicitly corrected the coffee to-do.')
        shown = self.app.learning_changes_shown(self.store.snapshot([])['learning_changes'])[0]
        self.assertEqual(shown['why'], 'You corrected the coffee to-do.')
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT why FROM learning_changes').fetchone()[0], 'Sam explicitly corrected the coffee to-do.')

    def test_each_decision_carries_its_to_dos_title_also_past_the_suggestions_list(self):
        # Learning, Decisions titled rows "48a9a3c08f304bdc": a done to-do older than the 100 newest done ones was not in
        # the snapshot's suggestions, so the row fell back to the id.
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) "
                       "VALUES('old1','old1','Ana accepts the venue wording','','[]','[\"work\"]','completed','2026-01-01T09:00:00+00:00')")
            for i in range(105):
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) "
                           "VALUES(?,?,?,'','[]','[\"work\"]','completed',?)", (f'n{i}', f'n{i}', f'Newer {i}', a.now()))
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d9','old1','complete','Sent: Send reply','assistant','2026-01-01T10:00:00+00:00')")  # closed long ago too
        snap = self.store.snapshot([])
        self.assertNotIn('old1', {s['id'] for s in snap['suggestions']})
        titles = {d['id']: d['title'] for d in snap['decisions']}
        self.assertEqual(titles['d9'], 'Ana accepts the venue wording')
        self.assertEqual(titles['d2'], 'To-do 2')



class DurableSignals(LearningLoop):
    """Signal loss (2026-11-02): a pass read the 30 newest signals since the last pass started, so a busy half day lost
    the rest for good, and a pass that failed lost its whole batch. Each signal now stays pending until a pass that read
    it is applied, oldest first in batches; a failed pass leaves its batch for a retry."""

    def setUp(self):
        super().setUp()
        self.clock = a.dt.datetime.fromisoformat(a.now())

    def add(self, n, at=None, prefix='x', feedback=''):
        base = at or self.clock - a.dt.timedelta(days=3)
        with self.store.connect() as db:
            for i in range(n):
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,'s1',?,?,'dashboard',?)",
                           (f'{prefix}{i:03}', 'other' if feedback else 'reject', feedback, (base + a.dt.timedelta(minutes=i)).isoformat()))
        return [f'{prefix}{i:03}' for i in range(n)]

    def later(self, hours=13):
        self.clock += a.dt.timedelta(hours=hours)
        return self.clock

    def step(self, runner):
        self.app.background_at = 0
        self.app.profile_step(runner)
        self.app.profile_step(runner)

    def one_pass(self, changes=(), fail=False, hours=13):
        """One pass at the next due time: its page, or None when none is due."""
        run_id = self.store.tune_due(self.later(hours))
        if not run_id:
            return None
        with self.store.connect() as db:  # started on this test's clock, for the cadence
            db.execute('UPDATE profile_runs SET started_at=? WHERE run_id=?', (self.clock.isoformat(), run_id))
        session = a.PROFILE_SESSION_PREFIX + run_id
        page = self.store.profile_evidence(1, session)

        def runner(request):
            if request['action'] == 'start':
                if not (fail(page) if callable(fail) else fail):
                    self.store.save_profile({'changes': list(changes)}, session)
                return {'status': 'admitted'}
            return {'status': 'ok'}  # ended without a draft: the pass failed
        self.step(runner)
        return page

    def states(self):
        with self.store.connect() as db:
            return {r['ref']: (r['status'], r['tries']) for r in db.execute("SELECT * FROM learning_signals WHERE kind='decision'")}

    def test_overflow_every_signal_is_read_once_oldest_first_across_passes(self):
        ids = self.add(100)
        pages = []
        while (page := self.one_pass(hours=2)) is not None:  # a backlog: the next batch within SOON_HOURS, not 12 hours
            pages.append(page)
        self.assertEqual([len(p['signals']) for p in pages], [30, 30, 30])
        pages.append(self.one_pass(hours=10))  # one batch left: about twice a day again
        self.assertEqual([len(p['signals']) for p in pages], [30, 30, 30, 15])  # 100 + the 5 from setUp
        self.assertEqual([s['at'] for s in pages[0]['signals']], sorted(s['at'] for s in pages[0]['signals']))
        self.assertTrue(all(s['to_do'] == 'To-do 1' for s in pages[0]['signals']))  # the oldest come first
        seen = [s['at'] + s['what'] + s.get('to_do', '') for p in pages for s in p['signals']]
        states = self.states()
        self.assertTrue(all(states[i] == ('done', 0) for i in ids))
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM learning_signals WHERE status='done'").fetchone()[0], 105)
            self.assertEqual(learning_loop.waiting(db, learning_loop.floor(db)), 0)
        self.assertEqual(sum(len(p['signals']) for p in pages), 105)
        self.assertEqual(len(seen), 105)
        self.add(3, at=self.clock, prefix='y')
        self.assertIsNone(self.store.tune_due(self.later(2)))  # no backlog: back to about twice a day
        self.assertTrue(self.one_pass(hours=12))

    def test_restart_after_the_turn_before_applying_loses_and_duplicates_nothing(self):
        changes = [{'kind': 'fact', 'text': 'Vendor newsletters never need a to-do.', 'why': 'Dismissed one.'},
                   {'kind': 'voice', 'channel': 'Email', 'text': EMAIL + '\nPlain words', 'why': 'Edits.'},
                   {'kind': 'voice', 'channel': 'WhatsApp', 'text': 'Formal, full sentences', 'why': 'x'}]
        apply_tune = self.store.apply_tune

        def stop(run_id):  # the service stops right after the turn ended, before applying it
            with self.store.connect() as db:
                if db.execute('SELECT status FROM profile_runs WHERE run_id=?', (run_id,)).fetchone()[0] == 'ok':
                    raise RuntimeError('stopped')
            return apply_tune(run_id)
        with patch.object(self.store, 'apply_tune', side_effect=stop):
            with self.assertRaises(RuntimeError):
                self.one_pass(changes)
        self.assertEqual(self.store.snapshot([])['learning_changes'], [])
        self.assertEqual({v for v, _ in self.states().values()}, {'claimed'})
        real = self.store.tune_voice
        with patch.object(self.store, 'tune_voice', side_effect=lambda *x: real(*x) if x[0] != 'Email' else 1 / 0):  # and mid-apply
            with self.assertRaises(ZeroDivisionError):
                self.store.tune_due(self.later())
        self.assertEqual(self.store.snapshot([])['learning_changes'], [])  # rolled back whole, the fact too
        self.assertEqual({v for v, _ in self.states().values()}, {'claimed'})
        self.assertIsNone(self.store.tune_due(self.later()))  # after the restart: applied once, nothing left to read
        self.assertIsNone(self.store.tune_due(self.later()))
        changes = self.store.snapshot([])['learning_changes']
        self.assertEqual(sorted(c['kind'] for c in changes), ['fact', 'voice'])  # the owner's WhatsApp voice stays theirs
        self.assertEqual({v for v, _ in self.states().values()}, {'done'})
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM facts WHERE text='Vendor newsletters never need a to-do.'").fetchone()[0], 1)
        self.assertEqual(next(v for v in self.store.voices() if v['channel'] == 'WhatsApp')['text'], 'lowercase, no full stop')
        self.app.action('learning_undo', {'id': next(c['id'] for c in changes if c['kind'] == 'voice')}, owner_dashboard=True)
        self.assertEqual(next(v for v in self.store.voices() if v['channel'] == 'Email')['text'], EMAIL)

    def test_a_failed_pass_is_retried_with_the_same_batch(self):
        first = self.one_pass(fail=True)
        with self.store.connect() as db:
            learning_loop.settle(db)
        self.assertEqual({v for v in self.states().values()}, {('pending', 1)})
        self.add(3, at=self.clock, prefix='new')  # newer signals wait until the failed batch went through
        second = self.one_pass([{'kind': 'fact', 'text': 'Vendor newsletters never need a to-do.', 'why': 'Dismissed one.'}])
        self.assertEqual(second['signals'], first['signals'])
        states = self.states()
        self.assertEqual({states[i] for i in ('d1', 'd2', 'd3')}, {('done', 1)})
        self.assertEqual({states.get(i) for i in ('new000', 'new001', 'new002')}, {None})
        self.assertEqual([c['kind'] for c in self.store.snapshot([])['learning_changes']], ['fact'])
        third = self.one_pass()
        self.assertEqual(len(third['signals']), 3)

    def test_a_turn_that_never_started_spends_no_try(self):
        run_id = self.store.tune_due(self.later())
        with self.store.connect() as db:
            db.execute("UPDATE profile_runs SET status='error',error='openclaw_unavailable' WHERE run_id=?", (run_id,))
        self.assertTrue(self.store.tune_due(self.later()))
        self.assertEqual({v for v in self.states().values()}, {('claimed', 0)})

    def test_a_poison_signal_is_given_up_after_max_tries_and_never_blocks_the_rest(self):
        self.add(1, at=self.clock - a.dt.timedelta(hours=1), prefix='poison', feedback='POISON')
        failed = 0
        for _ in range(20):
            page = self.one_pass(fail=lambda page: 'POISON' in json.dumps(page))
            if page is None:
                break
            failed += 'POISON' in json.dumps(page)
        self.assertEqual(failed, learning_loop.MAX_TRIES)
        states = self.states()
        self.assertEqual(states['poison000'], ('skipped', learning_loop.MAX_TRIES))
        self.assertEqual([k for k, (state, _) in states.items() if state == 'skipped'], ['poison000'])
        self.add(3, at=self.clock, prefix='y')
        while self.one_pass() is not None:
            pass
        self.assertEqual({state for state, _ in self.states().values()}, {'done', 'skipped'})
        with self.store.connect() as db:  # every one of the owner's edits went through too
            self.assertEqual(db.execute("SELECT count(*) FROM learning_signals WHERE kind='edit' AND status='done'").fetchone()[0], 2)

    def test_an_existing_machine_starts_from_its_last_pass(self):
        before = (self.clock - a.dt.timedelta(hours=20)).isoformat()
        self.add(40, at=self.clock - a.dt.timedelta(days=2), prefix='old')  # read (or skipped) by the old loop: history
        with self.store.connect() as db:
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,kind,auto) VALUES('old','ok',?,?,'tune',1)", (before, before))
        page = self.one_pass()
        self.assertEqual(len(page['signals']), 5)
        self.assertFalse(any(k.startswith('old') for k in self.states()))
        with self.store.connect() as db:
            self.assertEqual(learning_loop.floor(db), before)

    def test_an_existing_machine_recovers_what_its_failed_passes_after_the_last_good_one_read(self):
        good, failed = (self.clock - a.dt.timedelta(hours=30)).isoformat(), (self.clock - a.dt.timedelta(hours=10)).isoformat()
        self.add(40, at=self.clock - a.dt.timedelta(hours=40), prefix='old')  # before the last good pass: history
        lost = self.add(4, at=self.clock - a.dt.timedelta(hours=20), prefix='lost')  # read by a pass that then failed
        with self.store.connect() as db:
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,kind,auto) VALUES('good','ok',?,?,'tune',1)", (good, good))
            db.execute("INSERT INTO profile_runs(run_id,status,error,started_at,updated_at,kind,auto) VALUES('bad','error','lost',?,?,'tune',1)",
                       (failed, failed))
        page = self.one_pass()
        self.assertEqual(len(page['signals']), 9)  # the 4 the failed pass lost, then the 5 since
        states = self.states()
        self.assertTrue(all(states[i] == ('done', 0) for i in lost))
        self.assertFalse(any(k.startswith('old') for k in states))
        with self.store.connect() as db:
            self.assertEqual(learning_loop.floor(db), good)

if __name__ == '__main__':
    unittest.main()
