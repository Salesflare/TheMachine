"""The status's Fleet change marker (machine/stamps.py fleet_view_stamp): it changes with what api/fleet shows
(a teammate's question, a rule, a notice, an answer) and not with the Team Graph round's bookkeeping or the to-dos'
claims, so the dashboard fetches api/fleet off the Fleet tab only when there is something new (it fetched it every 20
seconds). The dashboard side: test_fleet_stamp_dashboard.mjs."""
import json
import unittest

from machine import stamps
import test_fleet as t


class FleetViewStamp(unittest.TestCase):
    setUp, ask = t.Fleet.setUp, t.Fleet.ask  # its fixture (a fake relay), not its tests

    def view_stamp(self):
        with self.fleet.connect() as db:
            return stamps.fleet_view_stamp(db)

    def test_it_changes_with_what_the_fleet_view_shows_and_only_then(self):
        first = self.view_stamp()
        self.assertIsNotNone(first)
        self.fleet.view(); self.fleet.summary()
        self.assertEqual(self.view_stamp(), first, 'reading changes nothing')
        self.fleet.set_meta('graph_cursor', {'at': 'later'})  # the Team Graph round's bookkeeping
        with self.fleet.connect() as db:
            db.execute("INSERT INTO fleet_meta(key,value) VALUES('answer_receipt:q_1','{}')")
            db.execute("INSERT INTO fleet_claims(suggestion_id,key,mine,checked_at) VALUES('s1','k1',1,'2026-11-10')")
        self.assertEqual(self.view_stamp(), first, 'bookkeeping and claims are not shown in api/fleet')
        before = json.dumps(self.fleet.view(), sort_keys=True, default=str)
        self.ask('relationships', {'about': 'client.example'})  # a teammate's question waits for the owner
        second = self.view_stamp()
        self.assertNotEqual(second, first)
        self.assertNotEqual(json.dumps(self.fleet.view(), sort_keys=True, default=str), before)
        self.fleet.set_rule('work', 'pat1', 'meeting', 'always')
        third = self.view_stamp()
        self.assertNotEqual(third, second)
        self.fleet.decide('q1', 'once')
        self.assertNotEqual(self.view_stamp(), third)

    def test_the_status_carries_it(self):
        app = object.__new__(t.a.App)
        app.store, app.config_path, app.config, app.fleet = self.store, None, {**t.CONFIG}, self.fleet
        self.assertEqual(app.action('status', {'full': True})['fleet']['stamp'], self.view_stamp())

    def test_a_database_without_the_counter_gives_none(self):
        with self.fleet.connect() as db:
            db.execute("DELETE FROM data_stamps WHERE name='fleet_view'")
        self.assertIsNone(self.view_stamp())


if __name__ == '__main__':
    unittest.main()
