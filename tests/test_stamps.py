import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

import assistant as a
from machine import stamps


class Stamps(unittest.TestCase):
    """What a request works out from a few tables is kept between requests and worked out again after any committed
    change to one of them: never from a change that is not committed, never for a table without its counters."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.db = sqlite3.connect(Path(self.temp.name) / 'k.sqlite')
        self.addCleanup(self.db.close)
        self.db.execute('CREATE TABLE people(id INTEGER PRIMARY KEY,name TEXT)')
        self.db.execute('CREATE TABLE notes(id INTEGER PRIMARY KEY,text TEXT)')
        stamps.watch(self.db, ('people', 'gone'))  # a table that isn't there is left out
        self.db.commit()
        self.kept, self.made = stamps.Kept(4), []

    def names(self):
        def make():
            self.made.append(1)
            return [r[0] for r in self.db.execute('SELECT name FROM people ORDER BY id')]
        return self.kept.get('names', stamps.stamp(self.db, ('people',)), make)

    def test_kept_until_an_insert_update_or_delete(self):
        self.assertEqual(self.names(), [])
        self.assertEqual(self.names(), [])
        self.assertEqual(len(self.made), 1)
        for change in ("INSERT INTO people(name) VALUES('Ann')", "UPDATE people SET name='Bo'", 'DELETE FROM people'):
            self.db.execute(change)
            self.db.commit()
            before = len(self.made)
            self.names()
            self.names()
            self.assertEqual(len(self.made), before + 1, change)
        self.db.execute("INSERT INTO notes(text) VALUES('x')")  # another table: still kept
        self.db.commit()
        self.names()
        self.assertEqual(len(self.made), 4)

    def test_nothing_kept_inside_a_transaction_or_for_a_table_without_counters(self):
        self.db.execute("INSERT INTO people(name) VALUES('Ann')")  # not committed: it could still roll back
        self.assertIsNone(stamps.stamp(self.db, ('people',)))
        self.assertEqual(self.names(), ['Ann'])
        self.db.rollback()
        self.assertEqual(self.names(), [])
        self.assertIsNone(stamps.stamp(self.db, ('notes',)))
        self.assertIsNone(stamps.stamp(sqlite3.connect(':memory:'), ('people',)))

    def test_two_databases_never_share_an_answer(self):
        other = sqlite3.connect(Path(self.temp.name) / 'other.sqlite')
        self.addCleanup(other.close)
        other.execute('CREATE TABLE people(id INTEGER PRIMARY KEY,name TEXT)')
        stamps.watch(other, ('people',))
        other.commit()
        self.assertNotEqual(stamps.stamp(self.db, ('people',)), stamps.stamp(other, ('people',)))

    def test_once_runs_again_after_a_schema_change_or_on_a_new_database_at_the_same_path(self):
        runs = []

        def make(db):
            runs.append(1)
            db.execute('CREATE TABLE IF NOT EXISTS made(x)')
        for _ in range(3):
            stamps.once(self.db, 'test', make, 'made')
        self.assertEqual(len(runs), 1)
        self.db.execute('CREATE TABLE later(x)')
        stamps.once(self.db, 'test', make, 'made')
        self.assertEqual(len(runs), 2)
        self.db.execute('DROP TABLE made')
        stamps.once(self.db, 'test', make, 'made')
        self.assertEqual(len(runs), 3)
        self.assertTrue(self.db.execute("SELECT 1 FROM sqlite_master WHERE name='made'").fetchone())


class PageQueries(unittest.TestCase):
    """A record's page, the to-do list and the Done list read by index, never a pass over every event or decision (each
    took a large part of a second on a real mailbox)."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 's.sqlite')

    def plan(self, sql, args=()):
        with self.store.connect() as db:
            return ' | '.join(r[3] for r in db.execute('EXPLAIN QUERY PLAN ' + sql, args))

    def test_the_queries_of_a_page_use_their_index(self):
        import shared_graph as sg
        scope = object.__new__(sg.Scope)
        scope.accounts, scope.mine, scope.internal = {'work'}, set(), set()
        seen = []
        with self.store.connect() as db:
            real = db.execute

            class Watch:
                def execute(self, sql, args=()):
                    seen.append(sql)
                    return real(sql, args)
            scope._db = Watch()
            scope.automated_only({'gm:t1', 'ic:9', 'ev:3'})
        plan = self.plan(seen[0], ('[]', '[]', '[]', '[]', '[]'))
        self.assertIn('events_thread_id', plan)
        self.assertIn('events_conversation', plan)
        for sql in ("SELECT metadata FROM events WHERE kind='owner.card' AND deleted=0",
                    "SELECT id FROM events WHERE kind='zoom.summary' AND deleted=0 AND occurred_at>=? AND occurred_at<=?",
                    "SELECT COUNT(*),MAX(id),SUM(version) FROM events WHERE kind='intercom.conversation' AND deleted=0",
                    "SELECT source_id FROM events WHERE kind='meeting.notes' AND deleted=0 AND source_id IN (SELECT ? || value FROM json_each(?))"):
            plan = self.plan(sql, ('a', 'b') if '?' in sql else ())
            self.assertIn('events_kind_', plan, sql)
            self.assertNotRegex(plan, r'SCAN events(?! USING INDEX events_kind_)', sql)
        # the Calendar tab's week: by the meetings' own index, not every message of every account
        week = self.plan("SELECT id FROM events WHERE kind='calendar.event' AND deleted=0 AND +account_id IN (?,?) AND occurred_at<? "
                         "AND coalesce(json_extract(metadata,'$.end_at'),occurred_at)>? ORDER BY occurred_at,id LIMIT 300", ('a', 'b', 'x', 'y'))
        self.assertIn('events_kind_calendar_event', week)
        self.assertNotIn('events_account_time', week)
        self.assertIn('decisions_suggestion', self.plan(
            "SELECT max(d.created_at) FROM decisions d WHERE d.suggestion_id=? AND d.choice IN ('complete','reject')", ('x',)))

    def test_the_hash_index_hashes_only_new_addresses_after_a_change(self):
        import shared_graph as sg
        import shared_graph_kept as kept
        keys = ('a' * 43 + '=', 'b' * 43 + '=')
        hashed = []

        def keyed(key, value):
            hashed.append(value)
            return sg.keyed(key, value)

        def plain(db, keys=keys):  # what it was: every address hashed with every key
            out = {}
            for row in db.execute("SELECT id,kind,info FROM graph_nodes WHERE kind IN ('person','org')"):
                info = json.loads(row['info'] or '{}')
                values = (['email:' + i[6:].lower() for i in [row['id'], *info.get('identifiers', [])] if str(i).startswith('email:')]
                          if row['kind'] == 'person' else (['domain:' + info['domain']] if info.get('domain') else []))
                for key in keys:
                    for v in values:
                        out.setdefault(sg.keyed(key, v), row['id'])
            return out
        with self.store.connect() as db:
            for node, kind, info in [('email:ann@acme.example', 'person', {'identifiers': ['email:Ann.B@acme.example']}),
                                     ('org:acme', 'org', {'domain': 'acme.example'}), ('wa:1', 'person', {'identifiers': ['wa:1']})]:
                db.execute('INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,?,?,1,1,?)', (node, kind, node, json.dumps(info)))
            self.assertEqual(kept.hash_index(db, keys, keyed), plain(db))
            self.assertEqual(len(hashed), 6)  # 3 addresses and domains, 2 keys
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('email:bo@b.example','person','Bo',1,1,'{}')")
            hashed.clear()
            self.assertEqual(kept.hash_index(db, keys, keyed), plain(db))
            self.assertEqual(hashed, ['email:bo@b.example'] * 2)  # only the new address
            hashed.clear()
            self.assertEqual(kept.hash_index(db, keys[:1], keyed), plain(db, keys[:1]))
            self.assertEqual(len(hashed), 4)  # other keys: hashed again

    def test_slack_names_are_kept_until_a_name_changes(self):
        from machine.sources.slack import slack_name_table
        with self.store.connect() as db:
            self.assertEqual(slack_name_table(db, {'U01234567'}), {})
            db.execute("INSERT INTO identity_names(identifier,name,checked_at) VALUES('slack:U01234567','Lee','2026-01-01')")
        with self.store.connect() as db:
            self.assertEqual(slack_name_table(db, {'U01234567'}), {'U01234567': 'Lee'})
            slack_name_table(db, {'U01234567'})['U01234567'] = 'changed by a caller'  # each caller gets its own copy
            self.assertEqual(slack_name_table(db, {'U01234567'}), {'U01234567': 'Lee'})
            db.execute("UPDATE identity_names SET name='Lee Park'")
        with self.store.connect() as db:
            self.assertEqual(slack_name_table(db, {'U01234567'}), {'U01234567': 'Lee Park'})

    def test_the_to_do_lists_slack_names_are_kept_until_a_person_changes(self):
        """Each status poll names the cards' Slack members (source_lines_shown): one pass over every person, kept until a
        person, a name or a member changes."""
        from unittest.mock import patch
        from machine.store import views
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('email:lee@example.com','person','Lee',1,0,?)",
                       ('{"identifiers": ["email:lee@example.com", "slack:U07654321"]}',))
        with patch.object(views, '_slack_people_names', wraps=views._slack_people_names) as made:
            for _ in range(3):
                with self.store.connect() as db:
                    self.assertEqual(views.slack_people_names(db, {'U07654321'}), {'U07654321': 'Lee'})
            self.assertEqual(made.call_count, 1)
            with self.store.connect() as db:
                views.slack_people_names(db, {'U07654321'})['U07654321'] = 'changed by a caller'  # each caller gets its own copy
                db.execute("UPDATE graph_nodes SET name='Lee Park'")
            with self.store.connect() as db:
                self.assertEqual(views.slack_people_names(db, {'U07654321'}), {'U07654321': 'Lee Park'})
            self.assertEqual(made.call_count, 2)

if __name__ == '__main__':
    unittest.main()
