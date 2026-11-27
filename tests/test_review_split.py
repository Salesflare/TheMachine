"""A review batch that fails every run (machine/store/review_split.py) and an AI that stops answering (model_check.py):
one signal can't hold the rest back, nothing is set aside while the AI itself fails, and its comeback restarts the
reviews at once."""
import datetime as dt
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('review_split_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import model_check  # noqa: E402
from machine.store import review_split  # noqa: E402
from machine.store.first_look import note_model_check  # noqa: E402
T = dt.datetime(2026, 11, 27, 8, 0, tzinfo=dt.timezone.utc)


class Model:
    """The Gateway and the model in one: a start is admitted; at its next status the review claims its batch and
    fails when `fails(batch)` says so (as preparation-run.mjs reports it), else saves it."""
    def __init__(self, store, fails, receipt=None):
        self.store, self.fails, self.started, self.batches = store, fails, set(), []
        self.receipt = receipt or {'status': 'error', 'error': 'runtime_error', 'error_phase': 'runtime', 'reason': 'unclassified'}

    def __call__(self, request):
        job = request['job_id']
        if request['action'] == 'start':
            self.started.add(job)
            return {'status': 'admitted'}
        session = a.REVIEW_SESSION_PREFIX + job
        claim = self.store.begin_analysis(['work'], 120, session, job)
        if not claim.get('analysis_id'):
            return {'status': 'ok'}
        with self.store.connect() as db:
            titles = sorted(db.execute('SELECT title FROM events WHERE id=?', (i['id'],)).fetchone()[0]
                            for i in __import__('json').loads(db.execute('SELECT items FROM analyses WHERE id=?', (claim['analysis_id'],)).fetchone()[0]))
        self.batches.append(titles)
        if self.fails(titles):
            return dict(self.receipt)
        self.store.finish_analysis(claim['analysis_id'], 'Checked', session, job)
        return {'status': 'ok'}


class ReviewSplit(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.quick_first_review = lambda db: 0
        self.app.night_hold = lambda db, current=None: None
        self.app.background_pause = lambda **kwargs: None
        self.app.config = {'accounts': [{'id': 'work'}], 'review_worker': {'enabled': True, 'gap_seconds': 120, 'timeout_seconds': 1500, 'min_signals': 1}}
        stamp = patch.object(model_check, 'sign_in_stamp', return_value='s'); stamp.start(); self.addCleanup(stamp.stop)
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': str(n), 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': title, 'body': 'Text', 'metadata': {}, 'deleted': False}
                                            for n, title in enumerate(['a', 'b', 'bad', 'c', 'd', 'e', 'f', 'g'])])
        with self.store.connect() as db:
            note_model_check(db, {'model': 'm', 'ok': True, 'at': (T - dt.timedelta(days=1)).isoformat(), 'stamp': 's', 'failed': 0})

    def check(self, at, answers):
        """The model check's thread (App.model_check_kick) when one is due: answers or not."""
        with self.store.connect() as db:
            found = model_check.last(db)
            if model_check.due(found, 'm', 's', at):
                note_model_check(db, model_check.check(found, {}, 'm', at.isoformat(), lambda config, ref: (answers, None if answers else 'Not logged in')))

    def work(self, model, minutes, answers=lambda at: True):
        """The review worker every 30 s for `minutes`, the model check beside it. The review_step results."""
        out = []
        for tick in range(minutes * 2):
            at = T + dt.timedelta(seconds=30 * tick)
            with patch_everywhere(a, 'now', return_value=at.isoformat()):
                out.append(self.app.review_step(model))
                self.check(at, answers(at))
        return out

    def pending(self):
        with self.store.connect() as db:
            return sorted(r[0] for r in db.execute('SELECT title FROM events WHERE analyzed_version<version AND deferrals<?', (a.SET_ASIDE_AFTER,)))

    def test_one_signal_every_run_fails_on_no_longer_holds_the_rest_back(self):
        # Before: the failed batch went back whole and every next run resumed exactly it, so one message the model kept
        # failing on held every signal behind it, for good, while the dashboard said it retries.
        model = Model(self.store, lambda titles: 'bad' in titles)
        self.work(model, 90)
        self.assertEqual(self.pending(), [])  # every other signal reviewed
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT deferrals FROM events WHERE title='bad'").fetchone()[0], a.SET_ASIDE_AFTER)  # under Set aside
            kinds = {r[0]: r[1] for r in db.execute("SELECT kind,message FROM error_feed WHERE source='review'")}
        self.assertEqual(kinds, {'runtime_error.unclassified': 'runtime retry chunk'})  # classified, not a bare "runtime"
        self.assertEqual(model.batches[0], ['a', 'b', 'bad', 'c', 'd', 'e', 'f', 'g'])
        self.assertLessEqual(len(model.batches), 2 + 3 + 1 + 3)  # two tries, a half per failure, then the rest
        self.assertIn(['bad'], model.batches)

    def test_while_the_ai_itself_fails_nothing_is_set_aside_and_its_comeback_restarts_reviews_at_once(self):
        # Claude Code signed out: every batch fails alike and the AI fails its check too. Nothing may be blamed on a
        # signal; once it answers again the next review goes at once, not after the half hour the back-off reached.
        back = T + dt.timedelta(hours=3)
        model = Model(self.store, lambda titles: dt.datetime.fromisoformat(a.now()) < back)
        self.work(model, 200, answers=lambda at: at >= back)
        self.assertEqual(self.pending(), [])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT max(deferrals) FROM events').fetchone()[0], 0)
            finished = [r[0] for r in db.execute("SELECT finished_at FROM review_runs WHERE status='ok' ORDER BY finished_at")]
        # the check answers at `back` (due within 5 minutes of its last failure); the review that saves follows within a minute
        self.assertLess(dt.datetime.fromisoformat(finished[0]), back + dt.timedelta(minutes=7))

    def test_a_sign_in_or_provider_failure_is_never_counted_on_the_batch(self):
        for reason in ('auth_failed', 'billing', 'provider_overloaded', 'mcp_runtime_limit'):
            self.assertFalse(review_split.batch_failure('runtime_error', reason), reason)
        for error in ('rate_limited', 'usage_limited', 'connection_error', 'runtime_lost', 'prompt_too_long'):
            self.assertFalse(review_split.batch_failure(error), error)
        self.assertTrue(review_split.batch_failure('runtime_error', 'unclassified'))
        self.assertTrue(review_split.batch_failure('model_idle_timeout'))
        receipt = {'status': 'error', 'error': 'runtime_error', 'error_phase': 'runtime', 'reason': 'auth_failed'}
        model = Model(self.store, lambda titles: True, receipt)
        self.work(model, 30, answers=lambda at: False)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT failures FROM analyses').fetchone()[0], 0)
            self.assertEqual(len(__import__('json').loads(db.execute('SELECT items FROM analyses').fetchone()[0])), 8)  # never split
            __import__('error_feed').ensure(db)
            kinds = {r[0]: r[1] for r in db.execute("SELECT kind,message FROM error_feed WHERE source='review'")}
            check = model_check.last(db)
        # The owner's sign-in, not a bug: never in the error reports (it was "runtime_error.auth_failed"), as a usage
        # limit isn't; the check shows it
        self.assertEqual(kinds, {})
        self.assertEqual((check['ok'], check['error']), (False, 'Not logged in'))  # the sign-in shows as a failed check

    def test_a_provider_failure_still_reaches_the_error_reports(self):
        receipt = {'status': 'error', 'error': 'runtime_error', 'error_phase': 'runtime', 'reason': 'provider_error'}
        self.work(Model(self.store, lambda titles: True, receipt), 2)
        with self.store.connect() as db:
            kinds = {r[0]: r[1] for r in db.execute("SELECT kind,message FROM error_feed WHERE source='review'")}
        self.assertEqual(kinds, {'runtime_error.provider_error': 'runtime retry'})

    def test_the_model_check_is_made_again_once_after_a_review_failed_and_notes_a_comeback(self):
        at = T.isoformat()
        ok = {'model': 'm', 'ok': True, 'at': at, 'stamp': 's', 'failed': 0}
        self.assertFalse(model_check.due(ok, 'm', 's', T + dt.timedelta(hours=1)))
        self.assertFalse(model_check.due({**ok, 'recheck': True}, 'm', 's', T + dt.timedelta(seconds=5)))
        self.assertTrue(model_check.due({**ok, 'recheck': True}, 'm', 's', T + dt.timedelta(seconds=30)))
        passed = model_check.check({**ok, 'recheck': True}, {}, 'm', at, lambda config, ref: (True, None))
        self.assertNotIn('recheck', passed); self.assertNotIn('recovered_at', passed)  # it never failed: no comeback
        failed = model_check.check(passed, {}, 'm', at, lambda config, ref: (False, 'x'))
        back = model_check.check(failed, {}, 'm', '2026-11-27T09:00:00+00:00', lambda config, ref: (True, None))
        self.assertEqual(back['recovered_at'], '2026-11-27T09:00:00+00:00')
        self.assertEqual(model_check.check(back, {}, 'm', '2026-11-27T10:00:00+00:00', lambda config, ref: (True, None))['recovered_at'], back['recovered_at'])
        with self.store.connect() as db:
            note_model_check(db, failed); model_check.ask_recheck(db)
            self.assertNotIn('recheck', model_check.last(db))  # a failed check is made again by itself
            note_model_check(db, back); model_check.ask_recheck(db)
            self.assertTrue(model_check.last(db)['recheck'])
            self.assertFalse(model_check.answered_since(db, '2026-11-27T08:30:00+00:00'))  # asked again: not yet
            self.assertTrue(model_check.recovered_since(db, '2026-11-27T08:30:00+00:00'))


if __name__ == '__main__':
    unittest.main()
