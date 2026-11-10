import datetime as dt
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('whats_new_assistant', ROOT.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
sys.path.insert(0, str(ROOT))
import dashboard_parts  # noqa: E402
from machine.store import whats_new  # noqa: E402

UTC = dt.timezone.utc
STARTED = dt.datetime(2026, 3, 2, 9, 0, tzinfo=UTC)  # the day this person finished getting started
ENTRIES = [{'id': 'old', 'date': '2026-02-20', 'title': 'Old', 'text': 'From before they started.'},
           {'id': 'same-day', 'date': '2026-03-02', 'title': 'Same day', 'text': 'Shipped the day they started.'},
           {'id': 'one', 'date': '2026-03-05', 'title': 'One', 'text': 'The first new thing.',
            'action': {'label': 'Open Routines', 'run': 'go-routines'}},
           {'id': 'two', 'date': '2026-03-06', 'title': 'Two', 'text': 'The second.'},
           {'id': 'three', 'date': '2026-03-07', 'title': 'Three', 'text': 'The third.'},
           {'id': 'four', 'date': '2026-03-08', 'title': 'Four', 'text': 'The fourth.'}]


def at(day, hour=10):
    return dt.datetime(2026, 3, day, hour, 0, tzinfo=UTC)


class WhatsNew(unittest.TestCase):
    """What's new (machine/store/whats_new.py): only entries from after a person got started, once a day, three at most,
    seen per Machine."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.n = 0
        self.store = self.machine()

    def machine(self, started=STARTED):
        """One person's Machine; `started`: when its first look stopped digging (None: it never had one)."""
        self.n += 1
        store = a.Store(Path(self.temp.name) / f'events{self.n}.sqlite')
        if started:
            with store.connect() as db:
                store.first_look_ended(db, started.isoformat())
        return store

    def ids(self, day, store=None, entries=ENTRIES, hour=10):
        view = (store or self.store).whats_new(at(day, hour), entries)
        return [e['id'] for e in view['entries']] if view else None

    def test_one_new_entry_shows_with_its_button(self):
        view = self.store.whats_new(at(5), ENTRIES)
        self.assertEqual(view, {'entries': [{'id': 'one', 'title': 'One', 'text': 'The first new thing.',
                                             'action': {'label': 'Open Routines', 'run': 'go-routines'}}]})
        self.assertIsNone(self.store.whats_new(at(6), ENTRIES[:2]))  # nothing new: no notice

    def test_nobody_gets_a_backlog(self):
        # Entries from before, or from the day, they finished getting started never show
        self.assertEqual(self.ids(6), ['two', 'one'])
        new = self.machine(started=at(9))  # someone who started after all of them
        self.assertIsNone(self.ids(12, new))
        self.assertEqual(self.ids(12, new, ENTRIES + [{'id': 'five', 'date': '2026-03-11', 'title': 'Five', 'text': 'Later.'}]), ['five'])

    def test_not_while_getting_started(self):
        fresh = self.machine(started=None)  # nothing reviewed yet
        self.assertIsNone(self.ids(8, fresh))
        with fresh.connect() as db:  # its first look is going
            db.execute("INSERT INTO review_runs(run_id,started_at,updated_at,status,window_hours) VALUES('r1',?,?,'running',24)", (at(1).isoformat(), at(1).isoformat()))
        self.assertIsNone(self.ids(8, fresh))
        with fresh.connect() as db:
            fresh.first_look_ended(db, at(7, 12).isoformat())
        self.assertIsNone(self.ids(8, fresh))           # its ending still shows: less than a day ago
        self.assertEqual(self.ids(9, fresh, hour=13), ['four'])

    def test_an_install_from_before_first_looks_counts_from_its_first_review(self):
        old = self.machine(started=None)
        with old.connect() as db:
            db.execute("INSERT INTO review_runs(run_id,started_at,updated_at,finished_at,status) VALUES('r1',?,?,?,'ok')",
                       (at(4).isoformat(), at(4, 11).isoformat(), at(4, 11).isoformat()))
        self.assertEqual(self.ids(6, old), ['two', 'one'])

    def test_three_at_most_newest_first_and_the_rest_count_as_seen(self):
        self.assertEqual(self.ids(8), ['four', 'three', 'two'])
        self.store.whats_new_seen(at(8), ENTRIES)
        self.assertIsNone(self.ids(9))  # 'one' was left out, and never comes back
        with self.store.connect() as db:
            detail = db.execute("SELECT detail FROM milestones WHERE name='whats_new'").fetchone()[0]
        self.assertEqual(json.loads(detail), {'seen': ['four', 'one', 'three', 'two']})

    def test_once_a_day(self):
        self.assertEqual(self.ids(5), ['one'])
        self.assertEqual(self.store.whats_new_seen(at(5), ENTRIES), {'whats_new': None})
        self.assertIsNone(self.ids(5, hour=11))
        self.assertIsNone(self.ids(6, hour=11, entries=ENTRIES[:3]))
        # Something new the same day waits for the next day
        self.store.whats_new_seen(at(6, 9), ENTRIES)
        late = ENTRIES + [{'id': 'late', 'date': '2026-03-06', 'title': 'Late', 'text': 'Shipped later that day.'}]
        self.assertIsNone(self.ids(6, hour=15, entries=late))
        self.assertEqual(self.ids(7, entries=late[:4] + late[-1:]), ['late'])

    def test_closing_with_nothing_due_writes_nothing(self):
        self.store.whats_new_seen(at(3), ENTRIES)
        with self.store.connect() as db:
            self.assertIsNone(db.execute("SELECT 1 FROM milestones WHERE name='whats_new'").fetchone())
        self.assertEqual(self.ids(5), ['one'])

    def test_seen_is_kept_per_person(self):
        # Each person has their own Machine (the owner, and every Fleet member theirs): closing it on one leaves the other's
        other = self.machine()
        self.store.whats_new_seen(at(5), ENTRIES)
        self.assertIsNone(self.ids(5, hour=12))
        self.assertEqual(self.ids(5, other, hour=12), ['one'])

    def test_the_dashboard_closes_it_and_only_the_owner(self):
        self.assertIn('whats_new_seen', a.DASHBOARD_ACTIONS)
        self.assertIn('whats_new_seen', a.OWNER_ACTIONS)
        self.assertEqual(a.App.ACTION_HANDLERS['whats_new_seen'], 'whats_new_seen_action')
        app = a.App.__new__(a.App)
        app.store = self.store
        with self.assertRaises(ValueError):
            app.whats_new_seen_action('whats_new_seen', {})
        self.assertEqual(app.whats_new_seen_action('whats_new_seen', {}, owner_dashboard=True), {'whats_new': None})

    def test_the_shipped_entries_are_well_formed(self):
        ids = [e['id'] for e in whats_new.ENTRIES]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual([e['date'] for e in whats_new.ENTRIES], sorted((e['date'] for e in whats_new.ENTRIES), reverse=True))
        script = dashboard_parts.assemble()
        for e in whats_new.ENTRIES:
            with self.subTest(entry=e['id']):
                self.assertRegex(e['id'], r'^[a-z0-9-]+$')
                dt.date.fromisoformat(e['date'])
                for text in (e['title'], e['text'], (e.get('action') or {}).get('label', '')):
                    self.assertIsNone(re.search('[—–!]', text), text)
                self.assertLessEqual(len(e['title']), 40)
                self.assertLessEqual(len(e['text']), 160)
                run = (e.get('action') or {}).get('run')
                if run and run != 'search':  # a palette command the dashboard has (the Settings tabs' ids are built from their names)
                    tab = re.fullmatch(r'go-settings-([a-z]+)', run)
                    self.assertTrue(f"id:'{run}'" in script or (tab and f"['{tab[1]}','" in script), run)


if __name__ == '__main__':
    unittest.main()
