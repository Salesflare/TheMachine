"""The night pause (machine/night_pause.py): reviews of new signals wait in the quiet hours and catch up before
morning; any use of the Machine lets them run; setup, the first look and Check now never wait; held signals are not
counted as missed; a chat's earlier message that a newer one in the batch shows reaches the review as one line."""
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('night_pause_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

import missed_work  # noqa: E402
import notify  # noqa: E402
import timeutil  # noqa: E402
from machine import night_pause  # noqa: E402
from machine.store.review import claim_weight  # noqa: E402

ZONE = timeutil.local_tz()


def local(hour, minute=0, day=18):
    return dt.datetime(2026, 11, day, hour, minute, tzinfo=ZONE)


class Runner:
    def __init__(self, *results):
        self.results, self.requests = list(results), []

    def __call__(self, request):
        self.requests.append(request)
        return {'status': self.results.pop(0)}


class Window(unittest.TestCase):
    def setUp(self):
        timeutil.set_work_hours({})
        self.addCleanup(timeutil.set_work_hours, {})

    def test_the_quiet_hours_pause_until_half_an_hour_before_they_end(self):
        self.assertEqual(night_pause.held_until(local(2), (0, 7), '08:30'), local(6, 30))
        self.assertEqual(night_pause.held_until(local(0), (0, 7), '08:30'), local(6, 30))
        self.assertEqual(night_pause.held_until(local(6, 29), (0, 7), '08:30'), local(6, 30))
        for outside in (local(6, 30), local(7), local(12), local(23, 59)):
            self.assertIsNone(night_pause.held_until(outside, (0, 7), '08:30'), outside)

    def test_an_early_morning_summary_or_early_hours_bring_the_catch_up_forward(self):
        self.assertEqual(night_pause.held_until(local(2), (0, 7), '07:00'), local(6))  # an hour before the summary
        early = timeutil.work_hours({'start': '06:00', 'morning': '06:00'})
        self.assertEqual(night_pause.held_until(local(2), (0, 7), '08:30', early), local(6))
        self.assertIsNone(night_pause.held_until(local(2), (0, 7), '00:30'))  # nothing left to pause

    def test_the_owners_hours_are_never_night(self):
        always = timeutil.work_hours({'start': '00:00', 'end': '00:00'})
        self.assertIsNone(night_pause.held_until(local(3), (0, 7), '08:30', always))
        nights = timeutil.work_hours({'start': '22:00', 'end': '06:00'})
        self.assertIsNone(night_pause.held_until(local(3), (0, 7), '08:30', nights))

    def test_quiet_hours_over_midnight_and_none(self):
        self.assertEqual(night_pause.held_until(local(23, 30, 17), (22, 6), '08:30',
                                                timeutil.work_hours({'end': '22:00'})), local(5, 30))
        self.assertIsNone(night_pause.held_until(local(3), (5, 5), '08:30'))

    def test_quiet_hours_come_from_the_one_setting_the_nightly_update_uses(self):
        import installer
        for value, hours in (('1-6', (1, 6)), ('22-6', (22, 6)), ('night', (0, 7)), ('', (0, 7))):
            with patch.dict(os.environ, {'ASSISTANT_QUIET_HOURS': value}):
                self.assertEqual(timeutil.quiet_hours(), hours)
                self.assertEqual(installer.quiet_hours(), hours)

    def test_idle_for_an_hour(self):
        self.assertTrue(night_pause.used_lately(1000, 1000 + 3599))
        self.assertFalse(night_pause.used_lately(1000, 1000 + 3600))
        self.assertFalse(night_pause.used_lately(0, 5000))


class Reviews(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        env = patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop('ASSISTANT_QUIET_HOURS', None)
        timeutil.set_work_hours({})
        self.addCleanup(timeutil.set_work_hours, {})
        notify.reset_active()
        self.addCleanup(notify.reset_active)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.quick_first_review = lambda db: 0
        self.app.config = {'accounts': [{'id': 'work'}], 'digest_at': '08:30',
                           'review_worker': {'enabled': True, 'min_signals': 40, 'max_wait_minutes': 15, 'gap_seconds': 600, 'timeout_seconds': 1500}}
        old = local(12, day=10).astimezone(dt.timezone.utc).isoformat()
        with self.store.connect() as db:
            db.execute("UPDATE milestones SET at=? WHERE name='tracking_since'", (old,))
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,finished_at) VALUES(?, 'ok', ?, ?, ?)", ('0' * 32, old, old, old))
        self.signal('one', local(1))

    def signal(self, source_id, at, kind='gmail.message', body='Can we meet on Friday?', metadata=None):
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': source_id, 'kind': kind, 'occurred_at': at.astimezone(dt.timezone.utc).isoformat(),
                                             'title': 'Hi', 'body': body, 'metadata': metadata or {}, 'deleted': False}])
        with self.store.connect() as db:
            db.execute('UPDATE events SET ingested_at=? WHERE source_id=?', (at.astimezone(dt.timezone.utc).isoformat(), source_id))

    def step(self, at, runner=None):
        with patch_everywhere(a, 'now', return_value=at.astimezone(dt.timezone.utc).isoformat()):
            return self.app.review_step(runner or Runner('admitted'))

    def queue(self, at):
        with patch_everywhere(a, 'now', return_value=at.astimezone(dt.timezone.utc).isoformat()), self.store.connect() as db:
            return self.app.review_queue(db, at.astimezone(dt.timezone.utc))

    def runs(self):
        with self.store.connect() as db:
            return db.execute("SELECT count(*) FROM review_runs WHERE run_id<>?", ('0' * 32,)).fetchone()[0]

    def test_signals_wait_at_night_and_are_caught_up_before_morning(self):
        self.assertIsNone(self.step(local(2)))  # waited an hour: a review would start by day
        self.assertIsNone(self.step(local(6, 29)))
        self.assertEqual(self.runs(), 0)
        queue = self.queue(local(3))
        self.assertEqual((queue['why'], queue['waiting']), ('night', 1))
        self.assertEqual(dt.datetime.fromisoformat(queue['starts_at']), local(6, 30))
        self.assertEqual(self.step(local(6, 30)), 'admitted')  # the catch-up, one review for the night
        self.assertEqual(self.runs(), 1)

    def test_by_day_nothing_changes(self):
        self.assertEqual(self.step(local(13)), 'admitted')

    def test_using_the_machine_at_night_lets_reviews_run_until_idle_for_an_hour(self):
        at = local(3)
        notify.mark_active(lambda: at.timestamp(), client='desk', on=True)  # the dashboard or the app, in use
        self.assertNotEqual(self.queue(at + dt.timedelta(minutes=59))['why'], 'night')
        self.assertEqual(self.queue(at + dt.timedelta(hours=1, minutes=5))['why'], 'night')  # idle for an hour: paused again
        self.assertEqual(self.step(at + dt.timedelta(minutes=1)), 'admitted')  # what waited goes right away

    def test_a_chat_or_telegram_message_or_a_tap_on_a_to_do_counts_as_use(self):
        at = local(3)
        self.app.owner_wrote_at = at.timestamp()
        self.assertNotEqual(self.queue(at + dt.timedelta(minutes=10))['why'], 'night')
        self.app.owner_wrote_at = 0
        self.assertEqual(self.queue(at + dt.timedelta(minutes=10))['why'], 'night')
        with self.store.connect() as db:
            db.execute('PRAGMA foreign_keys=OFF')
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d1','s1','accept','','telegram',?)",
                       (at.astimezone(dt.timezone.utc).isoformat(),))
        self.assertNotEqual(self.queue(at + dt.timedelta(minutes=10))['why'], 'night')

    def test_a_feedback_reply_or_web_chat_message_notes_the_owner_wrote(self):
        self.app.web_chat_said_action('web_chat_said', {'message_id': 'm1', 'text': 'hello'})
        self.assertGreater(self.app.owner_wrote_at, 0)

    def test_setup_the_first_look_and_check_now_never_wait(self):
        with self.store.connect() as db:  # no review finished yet: the first look
            db.execute("DELETE FROM review_runs")
        self.assertEqual(self.step(local(2)), 'admitted')

    def test_a_new_install_s_first_day_never_waits(self):
        with self.store.connect() as db:
            db.execute("UPDATE milestones SET at=? WHERE name='tracking_since'", (local(22, day=17).astimezone(dt.timezone.utc).isoformat(),))
        self.assertEqual(self.step(local(2)), 'admitted')

    def test_check_now_goes_at_night(self):
        with patch.object(a.time, 'time', return_value=local(2).timestamp()):
            self.app.review_asked = local(2).timestamp()
            self.assertEqual(self.step(local(2)), 'admitted')

    def test_it_can_be_turned_off(self):
        self.app.config['review_worker']['night_pause'] = False
        self.assertEqual(self.step(local(2)), 'admitted')

    def test_held_signals_are_not_counted_as_missed(self):
        self.signal('two', local(2))
        self.assertIsNone(self.step(local(3)))
        with self.store.connect() as db:
            found, _ = missed_work.candidates(db, self.app.config['accounts'], local(0).astimezone(dt.timezone.utc).isoformat())
            self.assertEqual(found, [])
            self.assertEqual(missed_work.set_aside(db, local(0).astimezone(dt.timezone.utc).isoformat()), {})


class Conversations(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')

    def chat(self, source_id, minutes, body, channel='C1', **extra):
        at = (local(2) + dt.timedelta(minutes=minutes)).astimezone(dt.timezone.utc).isoformat()
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': source_id, 'kind': 'slack.message', 'occurred_at': at,
                                             'title': 'Slack', 'body': body, 'metadata': {'channel_id': channel, 'user_id': 'U1', **extra}, 'deleted': False}])

    def claim(self):
        claim = self.store.begin_analysis(['work'], 120)
        with self.store.connect() as db:
            items = json.loads(db.execute('SELECT items FROM analyses WHERE id=?', (claim['analysis_id'],)).fetchone()[0])
            ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
        return claim, items, ids

    def test_a_chat_s_earlier_messages_that_a_newer_one_shows_go_as_one_line_next_to_it(self):
        self.chat('a', 0, 'Can you send the deck?')
        self.chat('b', 5, 'Before Friday please')
        self.chat('c', 60, 'Thanks!')
        self.chat('long', 1, 'x' * 300, channel='C2')
        self.chat('later', 2, 'ok', channel='C2')
        self.chat('file', 1, 'Here it is', channel='C3', files=[{'name': 'deck.pdf'}])
        self.chat('after', 3, 'ok?', channel='C3')
        claim, items, ids = self.claim()
        by = {i['id']: i for i in items}
        self.assertEqual((by[ids['a']].get('with'), by[ids['b']].get('with')), (ids['c'], ids['c']))
        self.assertNotIn('with', by[ids['c']])
        self.assertNotIn('with', by[ids['long']])  # its text doesn't fit the newer one's line: shown whole
        self.assertNotIn('with', by[ids['file']])  # more than words: shown whole
        self.assertEqual(claim_weight(items), 5 + 2 * 0.25)
        page =self.store.analysis_page(claim['analysis_id'], 0)
        views = {v['id']: v for v in page['events']}
        self.assertIn('Can you send the deck?', ' '.join(views[ids['c']]['earlier_in_conversation']))
        self.assertIn(str(ids['c']), views[ids['a']]['title_only'])
        self.assertNotIn('body', views[ids['a']])
        order = [v['id'] for v in page['events']]
        self.assertEqual(order[order.index(ids['c']) + 1:order.index(ids['c']) + 3], sorted([ids['a'], ids['b']], key=order.index))
        # the review finishes them all, as one batch
        self.store.finish_analysis(claim['analysis_id'], 'Reviewed')
        self.assertEqual(self.store.events(['work'], pending=True), [])


if __name__ == '__main__':
    unittest.main()
