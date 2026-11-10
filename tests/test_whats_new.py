import datetime as dt
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('whats_new_assistant', ROOT.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
spec = importlib.util.spec_from_file_location('whats_new_release', ROOT / 'scripts' / 'release.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)
sys.path.insert(0, str(ROOT))
import dashboard_parts  # noqa: E402
import timeutil  # noqa: E402
from machine.store import whats_new  # noqa: E402

UTC = dt.timezone.utc
STARTED = dt.datetime(2026, 3, 2, 9, 0, tzinfo=UTC)  # the day this person finished getting started
ENTRIES = [{'id': 'old', 'date': '2026-02-20', 'weight': 3, 'title': 'Old', 'text': 'From before they started.'},
           {'id': 'same-day', 'date': '2026-03-02', 'weight': 3, 'title': 'Same day', 'text': 'Shipped the day they started.'},
           {'id': 'one', 'date': '2026-03-05', 'weight': 2, 'title': 'One', 'text': 'The first new thing.',
            'action': {'label': 'Open Routines', 'run': 'go-routines'}, 'art': 'routines'},
           {'id': 'two', 'date': '2026-03-06', 'weight': 1, 'title': 'Two', 'text': 'The second.'},
           {'id': 'three', 'date': '2026-03-07', 'weight': 3, 'title': 'Three', 'text': 'The third.'},
           {'id': 'four', 'date': '2026-03-08', 'weight': 2, 'title': 'Four', 'text': 'The fourth.'}]


def at(day, hour=8, month=3):
    return dt.datetime(2026, month, day, hour, 0, tzinfo=UTC)


class WhatsNew(unittest.TestCase):
    """What's new (machine/store/whats_new.py): a pool of candidates; each morning the Machine picks up to five unseen
    ones (weight, then the newest) from after the person got started and at most three weeks old, and the dashboard
    shows that pick that day. Seen is kept per Machine and never shows again."""

    def setUp(self):
        zone = mock.patch.object(timeutil, 'LOCAL_TZ', ZoneInfo('UTC'))  # mornings in these tests are in UTC
        zone.start()
        self.addCleanup(zone.stop)
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

    def morning(self, day, store=None, entries=ENTRIES, hour=8, month=3, team=False):
        """The morning's pick, then what the dashboard shows later that day (ids, or None for no notice)."""
        store = store or self.store
        store.whats_new_pick(at(day, hour, month), entries, team)
        return self.ids(day, store, entries, month=month)

    def ids(self, day, store=None, entries=ENTRIES, hour=10, month=3):
        view = (store or self.store).whats_new(at(day, hour, month), entries)
        return [e['id'] for e in view['entries']] if view else None

    def close(self, day, store=None, entries=ENTRIES, hour=11, month=3):
        return (store or self.store).whats_new_seen(at(day, hour, month), entries)

    def test_one_new_entry_shows_with_its_button(self):
        self.store.whats_new_pick(at(5), ENTRIES)
        view = self.store.whats_new(at(5, 10), ENTRIES)
        self.assertEqual(view, {'entries': [{'id': 'one', 'title': 'One', 'text': 'The first new thing.',
                                             'action': {'label': 'Open Routines', 'run': 'go-routines'}, 'art': 'routines'}]})

    def test_the_pick_orders_by_weight_then_the_newest(self):
        self.assertEqual(self.morning(8), ['three', 'four', 'one', 'two'])
        many = ENTRIES + [{'id': f'n{i}', 'date': '2026-03-08', 'weight': 1, 'title': 'N', 'text': 'More.'} for i in range(3)]
        other = self.machine()
        picked = self.morning(8, other, many)
        self.assertEqual(len(picked), whats_new.PICKED)
        self.assertEqual(picked[:3], ['three', 'four', 'one'])  # every weight-1 one comes after them

    def test_what_is_not_picked_stays_for_a_later_morning(self):
        many = ENTRIES + [{'id': 'big', 'date': '2026-03-08', 'weight': 3, 'title': 'Big', 'text': 'A big one.'},
                          {'id': 'big2', 'date': '2026-03-08', 'weight': 3, 'title': 'Big 2', 'text': 'Another.'}]
        self.assertEqual(self.morning(8, entries=many), ['big', 'big2', 'three', 'four', 'one'])
        self.close(8, entries=many)
        self.assertEqual(self.morning(9, entries=many), ['two'])  # the one left out comes the next morning
        self.close(9, entries=many)
        self.assertIsNone(self.morning(10, entries=many))

    def test_nothing_qualifies_no_notice(self):
        self.assertIsNone(self.morning(4, entries=ENTRIES[:2]))  # only from before, or from the day, they got started
        with self.store.connect() as db:
            detail = json.loads(db.execute("SELECT detail FROM milestones WHERE name='whats_new_pick'").fetchone()[0])
        self.assertEqual(detail, {'day': '2026-03-04', 'ids': []})
        self.assertEqual(self.close(4, entries=ENTRIES[:2]), {'whats_new': None})
        with self.store.connect() as db:  # closing with nothing due writes nothing
            self.assertIsNone(db.execute("SELECT 1 FROM milestones WHERE name='whats_new'").fetchone())

    def test_old_candidates_expire_unseen(self):
        early = self.machine(started=dt.datetime(2026, 2, 1, 9, tzinfo=UTC))
        self.assertEqual(self.morning(13, early, ENTRIES[:1]), ['old'])  # 21 days after it shipped: still in
        late = self.machine(started=dt.datetime(2026, 2, 1, 9, tzinfo=UTC))
        self.assertIsNone(self.morning(14, late, ENTRIES[:1]))  # 22 days: expired without being shown

    def test_the_pick_is_made_in_the_morning_only_and_once(self):
        for hour in (3, 4, 12, 18):  # before five, or from noon: no pick, and nothing shows
            self.assertIsNone(self.store.whats_new_pick(at(5, hour), ENTRIES))
            self.assertIsNone(self.ids(5, hour=hour))
        self.assertEqual(self.store.whats_new_pick(at(6, 5), ENTRIES), ['one', 'two'])
        late = ENTRIES + [{'id': 'late', 'date': '2026-03-06', 'weight': 3, 'title': 'Late', 'text': 'Shipped that morning.'}]
        self.assertIsNone(self.store.whats_new_pick(at(6, 9), late))  # once a day: the morning's pick stands
        self.assertEqual(self.ids(6, entries=late, hour=20), ['one', 'two'])
        self.assertIsNone(self.ids(7, entries=late, hour=4))  # a new day before its pick: yesterday's isn't shown
        self.assertEqual(self.morning(7, entries=late), ['three', 'late', 'one', 'two'])

    def test_seen_never_shows_again(self):
        self.assertEqual(self.morning(5), ['one'])
        self.close(5)
        self.assertIsNone(self.ids(5, hour=15))  # closed: nothing more today
        self.assertEqual(self.morning(6), ['two'])
        self.close(6)
        self.assertEqual(self.morning(7), ['three'])
        with self.store.connect() as db:
            detail = db.execute("SELECT detail FROM milestones WHERE name='whats_new'").fetchone()[0]
        self.assertEqual(json.loads(detail), {'seen': ['one', 'two']})

    def test_seen_is_kept_per_person(self):
        # Each person has their own Machine (the owner, and every Fleet member theirs): closing it on one leaves the other's
        other = self.machine()
        self.assertEqual(self.morning(5), ['one'])
        self.assertEqual(self.morning(5, other), ['one'])
        self.close(5)
        self.assertIsNone(self.ids(5, hour=12))
        self.assertEqual(self.ids(5, other, hour=12), ['one'])

    def test_team_entries_only_in_a_work_fleet(self):
        team = ENTRIES + [{'id': 'boards', 'date': '2026-03-05', 'weight': 3, 'who': 'team', 'title': 'Boards', 'text': 'For a team.'}]
        self.assertEqual(self.morning(5, entries=team), ['one'])
        self.assertEqual(self.morning(5, self.machine(), team, team=True), ['boards', 'one'])

    def test_nobody_gets_a_backlog(self):
        new = self.machine(started=at(9))  # someone who started after all of them
        self.assertIsNone(self.morning(12, new))
        self.assertEqual(self.morning(13, new, ENTRIES + [{'id': 'five', 'date': '2026-03-11', 'weight': 1, 'title': 'Five', 'text': 'Later.'}]), ['five'])

    def test_not_while_getting_started(self):
        fresh = self.machine(started=None)  # nothing reviewed yet
        self.assertIsNone(self.morning(3, fresh))
        with fresh.connect() as db:  # its first look is going
            db.execute("INSERT INTO review_runs(run_id,started_at,updated_at,status,window_hours) VALUES('r1',?,?,'running',24)", (at(1).isoformat(), at(1).isoformat()))
        self.assertIsNone(self.morning(4, fresh))
        with fresh.connect() as db:
            fresh.first_look_ended(db, at(4, 7).isoformat())
        self.assertIsNone(self.morning(5, fresh, hour=6))  # its ending still shows: less than a day ago
        self.assertIsNone(self.ids(5, fresh, hour=9))  # that morning's pick was empty, and stands
        self.assertEqual(self.morning(6, fresh), ['one', 'two'])

    def test_an_install_from_before_first_looks_counts_from_its_first_review(self):
        old = self.machine(started=None)
        with old.connect() as db:
            db.execute("INSERT INTO review_runs(run_id,started_at,updated_at,finished_at,status) VALUES('r1',?,?,?,'ok')",
                       (at(4).isoformat(), at(4, 11).isoformat(), at(4, 11).isoformat()))
        self.assertEqual(self.morning(6, old), ['one', 'two'])

    def test_the_morning_worker_picks_with_the_team_flag(self):
        app = a.App.__new__(a.App)
        self.assertFalse(app.whats_new_team())
        app.fleet = mock.Mock(work_fleets=mock.Mock(return_value=['f1']))
        self.assertTrue(app.whats_new_team())

    def test_the_dashboard_closes_it_and_only_the_owner(self):
        self.assertIn('whats_new_seen', a.DASHBOARD_ACTIONS)
        self.assertIn('whats_new_seen', a.OWNER_ACTIONS)
        self.assertEqual(a.App.ACTION_HANDLERS['whats_new_seen'], 'whats_new_seen_action')
        app = a.App.__new__(a.App)
        app.store = self.store
        with self.assertRaises(ValueError):
            app.whats_new_seen_action('whats_new_seen', {})
        self.assertEqual(app.whats_new_seen_action('whats_new_seen', {}, owner_dashboard=True), {'whats_new': None})

    def test_a_bad_candidate_is_named(self):
        self.assertEqual(whats_new.problems(ENTRIES[2]), [])
        bad = {'id': 'Big One', 'date': '2026-3-1', 'weight': 5, 'title': 'Wow!', 'text': 'x', 'who': 'all', 'colour': 1}
        self.assertEqual(whats_new.problems(bad), ['unknown key colour', 'id: lowercase letters, digits and dashes only', 'date: YYYY-MM-DD',
                                                   'weight: 1, 2 or 3', "who: 'team' or left out", 'no em or en dashes and no exclamation marks'])
        self.assertEqual(whats_new.problems({'id': 'a', 'date': '2026-03-01', 'title': 'A', 'text': 'B'}), ['no weight'])

    def test_a_release_checks_only_its_new_candidates(self):
        source = lambda entries: 'import x\nENTRIES = ' + repr(entries) + '\nPICKED = 5\n'
        before = source(ENTRIES[:2])
        self.assertEqual(release.whats_new_problems(source(ENTRIES), before), [])
        broken = dict(ENTRIES[0], weight=None)  # already released: not this release's business
        new = [{'id': 'fresh', 'date': '2026-03-09', 'weight': 0, 'title': 'Fresh', 'text': 'New.'}]
        self.assertEqual(release.whats_new_problems(source(new + [broken, ENTRIES[1]]), source([broken, ENTRIES[1]])),
                         ['fresh: weight: 1, 2 or 3'])
        self.assertEqual(release.whats_new_problems(source(ENTRIES + ENTRIES[-1:]), before), ['four: id used twice'])
        self.assertEqual(release.whats_new_problems('ENTRIES = [x for x in y]\n', before), ['ENTRIES is not a plain list'])

    def test_the_shipped_entries_are_well_formed(self):
        ids = [e['id'] for e in whats_new.ENTRIES]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual([e['date'] for e in whats_new.ENTRIES], sorted((e['date'] for e in whats_new.ENTRIES), reverse=True))
        script = dashboard_parts.assemble()
        drawn = (ROOT / 'dashboard' / 'shell-whats-new.js').read_text(encoding='utf-8')
        pictures = set(re.findall(r'^ ([a-z]+):\(\)=>', drawn.split('const WN_ART={', 1)[1], re.M))
        self.assertIn('new', pictures)  # the stand-in for an entry without one
        self.assertIn('slice(0,5)', drawn)  # the dialog holds a whole pick
        self.assertEqual(whats_new.PICKED, 5)
        for e in whats_new.ENTRIES:
            with self.subTest(entry=e['id']):
                self.assertEqual(whats_new.problems(e), [])
                if e.get('art'):  # a picture the dashboard draws
                    self.assertIn(e['art'], pictures - {'new'})
                run = (e.get('action') or {}).get('run')
                if run and run != 'search':  # a palette command the dashboard has (the Settings tabs' ids are built from their names)
                    tab = re.fullmatch(r'go-settings-([a-z]+)', run)
                    self.assertTrue(f"id:'{run}'" in script or (tab and f"['{tab[1]}','" in script), run)


if __name__ == '__main__':
    unittest.main()
