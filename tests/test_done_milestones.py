"""Milestones on done to-dos (machine/store/done_milestones.py): the latest round number passed shows once on To-dos,
never a backlog, and closing it keeps it closed on every device."""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('done_milestones_assistant', ROOT.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
sys.path.insert(0, str(ROOT))
from machine.store import done_milestones  # noqa: E402


class DoneMilestones(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.done = 0

    def finish(self, n, status='completed'):
        """n more to-dos done (or dismissed: the Done list counts both)."""
        with self.store.connect() as db:
            db.executemany("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,?,'[]','[]',?,?)",
                           [(f'{i:016x}', f'k{i}', 'A to-do', 'Body', status, '2026-11-01T10:00:00+00:00') for i in range(self.done, self.done + n)])
        self.done += n

    def due(self):
        return self.store.done_milestone(self.store.snapshot([])['done_counts']['all'])  # as the status asks for it

    def test_levels_are_round_and_rising(self):
        self.assertEqual(done_milestones.LEVELS, (10, 50, 100, 250, 500, 1000, 2500, 5000, 10000))
        self.assertEqual([done_milestones.reached(n) for n in (0, 9, 10, 49, 50, 438, 500, 99999)], [0, 0, 10, 10, 50, 250, 500, 10000])

    def test_crossing_a_level_shows_it(self):
        self.finish(9)
        self.assertIsNone(self.due())
        self.finish(1)
        self.assertEqual(self.due(), {'count': 10})
        self.finish(5, status='rejected')  # Not needed counts too, as on the Done list
        self.assertEqual(self.due(), {'count': 10})

    def test_a_machine_past_several_gets_only_the_latest_once(self):
        self.finish(438)
        self.assertEqual(self.due(), {'count': 250})
        self.assertEqual(self.store.done_milestone_seen(250), {'done_milestone': None})
        self.assertIsNone(self.due())  # no 10, 50 or 100 after it
        self.finish(61)
        self.assertIsNone(self.due())  # 499
        self.finish(1)
        self.assertEqual(self.due(), {'count': 500})

    def test_closed_stays_closed(self):
        self.finish(50)
        self.store.done_milestone_seen(50)
        self.assertIsNone(self.due())
        self.assertIsNone(self.store.done_milestone(50))  # a later status, another device: still closed
        with self.store.connect() as db:
            self.assertEqual(done_milestones.seen(db), 50)
        # Closing a lower one, one not reached yet or not a level at all changes nothing
        for level in (10, 100, 77, 'x', None):
            self.store.done_milestone_seen(level)
            with self.store.connect() as db:
                self.assertEqual(done_milestones.seen(db), 50)
        self.finish(50)
        self.assertEqual(self.due(), {'count': 100})

    def test_only_the_owner_closes_it_from_the_dashboard(self):
        self.finish(10)
        app = a.App.__new__(a.App)
        app.store = self.store
        self.assertIn('done_milestone_seen', a.DASHBOARD_ACTIONS)
        self.assertIn('done_milestone_seen', a.OWNER_ACTIONS)
        self.assertEqual(a.App.ACTION_HANDLERS['done_milestone_seen'], 'done_milestone_seen_action')
        with self.assertRaises(ValueError):
            app.done_milestone_seen_action('done_milestone_seen', {'count': 10})
        self.assertEqual(app.done_milestone_seen_action('done_milestone_seen', {'count': 10}, owner_dashboard=True), {'done_milestone': None})


if __name__ == '__main__':
    unittest.main()
