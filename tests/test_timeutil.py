"""timeutil.py: the owner's time zone and hours, and the clock, as plain functions."""
import datetime as dt
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

import timeutil


class TimeUtil(unittest.TestCase):
    def setUp(self):
        hours, zone = dict(timeutil.WORK_HOURS), timeutil.LOCAL_TZ
        self.addCleanup(lambda: (timeutil.set_work_hours(hours), setattr(timeutil, 'LOCAL_TZ', zone)))

    def test_now_is_utc_iso(self):
        value = dt.datetime.fromisoformat(timeutil.now())
        self.assertEqual(value.utcoffset(), dt.timedelta(0))

    def test_timezone(self):
        timeutil.set_timezone('Europe/London')
        self.assertEqual(timeutil.local_tz(), ZoneInfo('Europe/London'))
        timeutil.set_timezone('')  # nothing set keeps the zone
        self.assertEqual(timeutil.local_tz().key, 'Europe/London')

    def test_clock(self):
        self.assertEqual(timeutil.clock('8:30'), (8, 30))
        self.assertEqual(timeutil.clock(' 23:05 '), (23, 5))
        with self.assertRaisesRegex(ValueError, 'The start must be a time like 09:00'):
            timeutil.clock('24:00', 'The start')

    def test_work_hours_are_checked_and_completed(self):
        self.assertEqual(timeutil.work_hours(), timeutil.WORK_HOURS_DEFAULT)
        self.assertEqual(timeutil.work_hours({'days': 'sun-thu', 'start': '7:00'}),
                         {'days': [1, 2, 3, 4, 7], 'start': '07:00', 'end': '23:00', 'morning': '09:00'})
        self.assertEqual(timeutil.work_hours({'days': ['mon', 3, 'Friday']})['days'], [1, 3, 5])
        for bad in ({'days': []}, {'days': [8]}, {'days': ['someday']}, {'end': '25:00'}, 'mon-fri'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                timeutil.work_hours(bad)

    def test_set_work_hours_changes_the_one_dict_in_place(self):
        shared = timeutil.WORK_HOURS  # what another module imported
        timeutil.set_work_hours({'days': [6, 7], 'morning': '10:15'})
        self.assertIs(timeutil.WORK_HOURS, shared)
        self.assertEqual((shared['days'], timeutil.morning_label()), ([6, 7], '10:15'))
        with self.assertRaises(ValueError):
            timeutil.set_work_hours({'days': []})
        self.assertEqual(shared['days'], [6, 7])  # a wrong value changes nothing

    def test_work_days(self):
        saturday = dt.datetime(2026, 10, 31, 9, 0)
        self.assertFalse(timeutil.is_work_day(saturday))
        self.assertEqual(timeutil.next_work_day(saturday), dt.datetime(2026, 11, 2, 9, 0))
        weekend = {'days': [6, 7]}
        self.assertTrue(timeutil.is_work_day(saturday, weekend))
        self.assertEqual(timeutil.next_work_day(saturday, weekend), saturday)

    def test_in_hours(self):
        at = lambda h, m=0: dt.datetime(2026, 11, 2, h, m)  # noqa: E731
        self.assertTrue(timeutil.in_hours(at(8)))
        self.assertFalse(timeutil.in_hours(at(23)))
        self.assertFalse(timeutil.in_hours(at(7, 59)))
        night = {'start': '22:00', 'end': '06:00'}  # wraps past midnight
        self.assertTrue(timeutil.in_hours(at(23), night))
        self.assertTrue(timeutil.in_hours(at(5, 59), night))
        self.assertFalse(timeutil.in_hours(at(12), night))
        self.assertTrue(timeutil.in_hours(at(3), {'start': '09:00', 'end': '09:00'}))  # the same: always
        with patch.dict(timeutil.WORK_HOURS, end='18:00'):
            self.assertFalse(timeutil.in_hours(at(18)))

    def test_morning_label(self):
        self.assertEqual(timeutil.morning_label(), '9:00')
        self.assertEqual(timeutil.morning_label({'morning': '07:30'}), '7:30')


if __name__ == '__main__':
    unittest.main()
