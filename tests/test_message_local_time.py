"""A relative day in a message counts from the day it was sent. A to-do said a committee "has passed" against an email
that asked for a pre-read "this evening" before "tomorrow's" committee: a review and a Do it turn read each message's
time only as UTC (occurred_at), a day apart from the owner's near midnight, and had no rule for "tomorrow" in an
older message. Each message they read now carries its moment in the owner's zone, with its weekday (local_time), and
both prompts say a relative day counts from it. No live calls."""
import importlib.util
from pathlib import Path
import unittest
from seams import patch_everywhere  # noqa: E402,F401

spec = importlib.util.spec_from_file_location('local_time_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import timeutil  # noqa: E402


def mail(at):
    return {'id': 7, 'account_id': 'w', 'source_id': 'm7', 'kind': 'gmail.message', 'occurred_at': at, 'title': 'Steering committee pre-read',
            'body': 'Please send the pre-read this evening; I need it before tomorrow\'s 10:00 committee.',
            'metadata': {'from': 'Client <client@example.com>', 'to': 'owner@example.com', 'labels': ['INBOX']}}


class LocalTime(unittest.TestCase):
    def setUp(self):
        was = timeutil.LOCAL_TZ
        self.addCleanup(setattr, timeutil, 'LOCAL_TZ', was)
        timeutil.set_timezone('Europe/Brussels')

    def test_a_message_carries_the_day_it_was_sent_in_the_owners_zone(self):
        # Sent on a Monday evening in Brussels: still Monday in UTC
        self.assertEqual(a.review_view(mail('2026-11-09T20:54:00+00:00'))['local_time'], 'Mon 2026-11-09 21:54')
        # Sent just after midnight in Brussels: still the day before in UTC, so "tomorrow" there is a day later than UTC's
        self.assertEqual(a.review_view(mail('2026-11-09T23:30:00+00:00'))['local_time'], 'Tue 2026-11-10 00:30')
        self.assertIsNone(a.review_view({**mail('soon'), 'id': 8}).get('local_time'))  # an unreadable time gives none

    def test_an_all_day_event_keeps_its_own_day(self):
        event = {**mail('2026-12-04T23:00:00+00:00'), 'kind': 'calendar.event',
                 'metadata': {'all_day': True, 'start': {'date': '2026-12-05'}, 'end': {'date': '2026-12-06'}}}
        view = a.review_view(event)
        self.assertEqual(view['all_day_on'], '2026-12-05')
        self.assertNotIn('local_time', view)

    def test_both_prompts_count_a_relative_day_from_its_message(self):
        self.assertIn('counts from the day it was sent (its local_time)', a.review_prompt('r1', ['work']))
        self.assertIn('counts from the day it was sent (its local_time)', a.preparation_prompt({'job_id': 'j', 'suggestion_id': 's'}))


if __name__ == '__main__':
    unittest.main()
