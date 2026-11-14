"""A to-do's moves between statuses (machine/store/todo_moves.py): transition() checks each against
machine/todo_states.MOVES, keeps it in the to-do's history and otherwise writes what the UPDATE it replaces wrote.
Synthetic data only."""
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from machine import todo_states as ts  # noqa: E402
from machine.store import todo_moves  # noqa: E402
from pinned import pinned  # noqa: E402

NOW = '2026-11-14T10:00:00+00:00'


class TodoMoves(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db.row_factory = sqlite3.Row
        self.addCleanup(self.db.close)
        self.db.execute("CREATE TABLE suggestions(id TEXT PRIMARY KEY,status TEXT NOT NULL DEFAULT 'pending',early INTEGER,"
                        'outcome TEXT,closed_from TEXT)')
        todo_moves.ensure(self.db)
        self.db.execute("INSERT INTO suggestions(id,status,early,outcome) VALUES('s1','pending',0,'{}')")

    def status(self, sid='s1'):
        return self.db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0]

    @pinned(NOW)
    def test_a_move_changes_the_status_and_keeps_it_in_the_history(self):
        self.assertEqual(todo_moves.transition(self.db, 's1', ts.ACCEPTED, 'do_it'), 1)
        self.assertEqual(self.status(), 'accepted')
        self.assertEqual(todo_moves.history(self.db, 's1'),
                         [{'at': NOW, 'from': 'pending', 'to': 'accepted', 'reason': 'do_it'}])

    def test_other_columns_set_just_before_the_move_read_the_status_before(self):
        with self.db:
            self.db.execute('UPDATE suggestions SET closed_from=status,early=1,outcome=NULL WHERE id=?', ('s1',))
            todo_moves.transition(self.db, 's1', ts.REJECTED, 'merged')
        row = dict(self.db.execute('SELECT * FROM suggestions').fetchone())
        self.assertEqual((row['status'], row['closed_from'], row['early'], row['outcome']), ('rejected', 'pending', 1, None))

    def test_only_leaves_it_as_it_is_like_the_guard_it_replaces(self):
        self.assertEqual(todo_moves.transition(self.db, 's1', ts.COMPLETED, 'x', only=ts.PREPARED), 0)
        self.assertEqual(todo_moves.transition(self.db, 's1', ts.COMPLETED, 'x', only=ts.TAKEN_ON), 0)
        self.assertEqual(todo_moves.transition(self.db, 'gone', ts.COMPLETED, 'x'), 0)
        self.assertEqual((self.status(), todo_moves.history(self.db, 's1')), ('pending', []))
        self.assertEqual(todo_moves.transition(self.db, 's1', ts.COMPLETED, 'done', only=ts.NOT_STARTED), 1)
        self.assertEqual(self.status(), 'completed')

    def test_staying_put_counts_and_writes_no_history(self):
        self.assertEqual(todo_moves.transition(self.db, 's1', ts.PENDING, 'touch'), 1)
        self.assertEqual(todo_moves.transition(self.db, 's1', ts.PENDING, 'touch', only=ts.CLOSED), 0)
        self.assertEqual(todo_moves.history(self.db, 's1'), [])

    def test_a_move_not_declared_raises_and_changes_nothing(self):
        todo_moves.transition(self.db, 's1', ts.COMPLETED, 'done')
        for to in (ts.SNOOZED, ts.REJECTED, 'archived'):
            with self.subTest(to=to), self.assertRaises(todo_moves.MoveNotAllowed):
                todo_moves.transition(self.db, 's1', to, 'x')
        self.assertEqual(self.status(), 'completed')
        self.assertEqual(len(todo_moves.history(self.db, 's1')), 1)
        self.assertIsInstance(todo_moves.MoveNotAllowed('x'), ValueError)

    def test_moves_name_known_statuses_and_every_status_has_its_moves(self):
        self.assertEqual(set(ts.MOVES), set(ts.ALL))
        for before, after in ts.MOVES.items():
            with self.subTest(status=before):
                self.assertTrue(set(after) <= set(ts.ALL))
                self.assertNotIn(before, after)
                self.assertTrue(ts.allowed(before, before))
        self.assertFalse(ts.allowed(ts.PENDING, 'archived'))
        # Every open status can be closed either way, and every closed one can come back
        for before in ts.OPEN:
            self.assertTrue(set(ts.CLOSED) <= set(ts.MOVES[before]), before)
        for before in ts.CLOSED:
            self.assertIn(ts.PENDING, ts.MOVES[before])

    def test_the_store_makes_the_history_table(self):
        from test_assistant import assistant
        with tempfile.TemporaryDirectory() as tmp:
            store = assistant.Store(Path(tmp) / 'events.sqlite')
            with store.connect() as db:
                columns = [r[1] for r in db.execute('PRAGMA table_info(todo_moves)')]
        self.assertEqual(columns, ['id', 'suggestion_id', 'at', 'from_status', 'to_status', 'reason'])


if __name__ == '__main__':
    unittest.main()
