"""Time to clear (clear_pace.py): the owner's own pace from their dashboard decisions, with a default, and the line the
To-dos header and the morning digest share ("4 ready · about 2 min"). Made-up decisions only."""
import datetime as dt
import sqlite3
import unittest

import clear_pace

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 11, 7, 10, 0, tzinfo=UTC)


def stamps(*gaps, start=NOW - dt.timedelta(hours=1)):
    out, at = [start.isoformat()], start
    for g in gaps:
        at += dt.timedelta(seconds=g)
        out.append(at.isoformat())
    return out


class ClearPace(unittest.TestCase):
    def test_the_median_gap_of_a_sitting(self):
        self.assertEqual(clear_pace.pace(stamps(10, 20, 25, 40, 90)), 25)
        # a break (an hour) and a double tap (under two seconds) don't count
        self.assertEqual(clear_pace.pace(stamps(10, 3600, 20, 1, 25, 40, 90)), 25)
        # order doesn't matter, and odd values are left out
        self.assertEqual(clear_pace.pace(list(reversed(stamps(10, 20, 25, 40, 90))) + ['', None, 'soon']), 25)

    def test_the_default_until_there_is_enough_and_bounds(self):
        self.assertEqual(clear_pace.pace([]), clear_pace.DEFAULT)
        self.assertEqual(clear_pace.pace(stamps(10, 20, 30, 40)), clear_pace.DEFAULT)  # four gaps: not enough yet
        self.assertEqual(clear_pace.pace(stamps(2, 2, 2, 3, 3)), clear_pace.FLOOR)
        self.assertEqual(clear_pace.pace(stamps(500, 550, 590, 600, 580)), clear_pace.CEILING)

    def test_only_dashboard_decisions_of_the_last_weeks(self):
        db = sqlite3.connect(':memory:')
        db.execute('CREATE TABLE decisions(id TEXT,suggestion_id TEXT,choice TEXT,feedback TEXT,source TEXT,created_at TEXT)')
        rows = [(f'd{i}', 's', 'send', '', 'dashboard', at) for i, at in enumerate(stamps(12, 12, 12, 12, 12))]
        rows += [(f't{i}', 's', 'send', '', 'telegram', at) for i, at in enumerate(stamps(100, 100, 100, 100, 100, start=NOW - dt.timedelta(minutes=30)))]
        rows += [(f'o{i}', 's', 'send', '', 'dashboard', at) for i, at in enumerate(stamps(200, 200, 200, 200, 200, 200, start=NOW - dt.timedelta(days=40)))]
        db.executemany('INSERT INTO decisions VALUES(?,?,?,?,?,?)', rows)
        self.assertEqual(clear_pace.seconds(db, NOW), 12)

    def test_the_line(self):
        self.assertEqual(clear_pace.line(4, 30, lang='en'), '4 ready · about 2 min')
        self.assertEqual(clear_pace.line(1, 12, lang='en'), '1 ready · about 1 min')
        self.assertEqual(clear_pace.line(5, 45, lang='en'), '5 ready · about 4 min')  # as the dashboard rounds: up
        self.assertEqual(clear_pace.line(0, 30, lang='en'), '')
        self.assertEqual(clear_pace.line(4, 30, lang='nl'), '4 klaargezet · ongeveer 2 min')


if __name__ == '__main__':
    unittest.main()
