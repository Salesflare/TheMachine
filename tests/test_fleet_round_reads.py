"""The Fleet's background rounds read the directory and the owner's own addresses once per round (Fleet.round_reads):
claims and handled asked for them some 3,000 times a round, a database connection each, about 20 s of a core every two
minutes on a busy Machine (2026-11-10). A new directory is read again at once, also one another thread saved; a slow part
of a round is logged with its name, time and bytes read, never anything it read."""
import contextlib
import threading
import unittest
from unittest import mock

import test_fleet

fleet = test_fleet.fleet


class RoundReads(unittest.TestCase):
    setUp = test_fleet.Fleet.setUp

    def counted(self):
        """The Fleet's connect, counting the connections it opens."""
        opened, connect = [], self.fleet.connect

        @contextlib.contextmanager
        def counting():
            opened.append(1)
            with connect() as db:
                yield db
        self.fleet.connect = counting
        return opened

    def test_a_round_reads_the_directory_and_own_addresses_once(self):
        opened = self.counted()
        with self.fleet.round_reads():
            for _ in range(50):
                self.fleet.fleets(), self.fleet.teammates('work'), self.fleet.my_emails(), self.fleet.own_domains()
        self.assertLessEqual(len(opened), 3)  # the directory, the owner's addresses, their company's domains
        opened.clear()
        for _ in range(5):
            self.fleet.fleets()
        self.assertEqual(len(opened), 5)  # outside a round, every read goes to the database as before

    def test_a_new_directory_is_read_again_within_the_round(self):
        with self.fleet.round_reads():
            self.assertEqual([m['member_id'] for m in self.fleet.teammates('work')], ['pat1'])
            two = self.fleet.meta('directory')
            two['fleets'][0]['members'].append({'member_id': 'lee1', 'name': 'Lee', 'role': 'member', 'emails': ['lee@acme.example']})
            saved = threading.Thread(target=self.fleet.set_meta, args=('directory', two))  # the dashboard, say
            saved.start(); saved.join()
            self.assertEqual([m['member_id'] for m in self.fleet.teammates('work')], ['pat1', 'lee1'])
            self.fleet.meta('directory')['fleets'].clear()  # a caller changing its copy changes nobody else's
            self.assertEqual(len(self.fleet.fleets()), 1)

    def test_claims_and_handled_answer_the_same_within_a_round(self):
        self.fleet.step(wait=0)
        before = list(self.relay.calls)
        self.relay.calls.clear()
        with self.fleet.round_reads():
            self.fleet.claims_round(), self.fleet.handled_round()
        within = list(self.relay.calls)
        self.relay.calls.clear()
        self.fleet.claims_round(), self.fleet.handled_round()
        self.assertEqual(within, self.relay.calls)
        self.assertTrue(before)

    def test_a_slow_part_is_logged_by_name_only(self):
        with mock.patch.object(fleet, 'ROUND_LOG_SECONDS', 0.0), mock.patch.object(fleet.LOG, 'info') as info:
            self.assertEqual(self.fleet.timed('claims', lambda: 'answer'), 'answer')
        line = info.call_args[0]
        self.assertTrue(line[0].startswith('fleet round slow part=%s took=%.1fs read=%s'))
        self.assertEqual(line[1], 'claims')
        with mock.patch.object(fleet.LOG, 'info') as info:
            self.fleet.timed('claims', lambda: None)
        info.assert_not_called()  # a quick part says nothing


if __name__ == '__main__':
    unittest.main()
