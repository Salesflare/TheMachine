"""A to-do's moves between statuses (machine/store/todo_moves.py): transition() checks each against
machine/todo_states.MOVES, keeps it in the to-do's history and otherwise writes what the UPDATE it replaces wrote.
Synthetic data only."""
import ast
import re
import sqlite3
import subprocess
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

    def test_a_move_outside_moves_is_allowed_only_for_its_named_reason(self):
        for (before, after), reasons in ts.ALSO.items():
            with self.subTest(move=(before, after)):
                self.assertNotIn(after, ts.MOVES[before])
                self.assertTrue(reasons and all(why.strip() for why in reasons.values()))
                self.assertFalse(ts.allowed(before, after))
                self.assertFalse(ts.allowed(before, after, 'other'))
                for reason in reasons:
                    self.assertTrue(ts.allowed(before, after, reason))

    def test_the_store_makes_the_history_table(self):
        from machine.main import Store
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp) / 'events.sqlite')
            with store.connect() as db:
                columns = [r[1] for r in db.execute('PRAGMA table_info(todo_moves)')]
        self.assertEqual(columns, ['id', 'suggestion_id', 'at', 'from_status', 'to_status', 'reason'])


class OnlyTransitionMoves(unittest.TestCase):
    """Guard: a to-do's status changes only through todo_moves.transition(), so every move is a declared one and is in
    its history. A raw `UPDATE suggestions SET status=` anywhere else (tests set up rows as they like) fails here."""
    ROOT = Path(__file__).resolve().parents[1]
    SETS = re.compile(r'UPDATE\s+suggestions\s+SET\s(.*?)(?:\sWHERE\s|$)', re.S | re.I)
    STATUS = re.compile(r'(?:^|,)\s*status\s*=', re.I)

    @classmethod
    def raw_writes(cls, source, name='<code>'):
        found = []
        for node in ast.walk(ast.parse(source, name)):
            if isinstance(node, ast.Call) and node.args:
                parts = sorted((n for n in ast.walk(node.args[0]) if isinstance(n, ast.Constant) and isinstance(n.value, str)),
                               key=lambda n: (n.lineno, n.col_offset))  # the SQL as written, also when built from pieces
                sets = cls.SETS.search(' '.join(n.value for n in parts))
                if sets and cls.STATUS.search(sets.group(1)):
                    found.append(f'{name}:{node.lineno}')
        return found

    def test_no_raw_status_write_outside_transition(self):
        files = subprocess.run(['git', 'ls-files', '*.py'], cwd=self.ROOT, capture_output=True, text=True, check=True).stdout.split()
        self.assertIn('machine/store/decisions.py', files)
        raw = [hit for path in files if not path.startswith('tests/') and path != 'machine/store/todo_moves.py'
               for hit in self.raw_writes((self.ROOT / path).read_text(encoding='utf-8'), path)]
        self.assertEqual(raw, [], 'move a to-do with machine.store.todo_moves.transition(), not a raw status UPDATE')

    def test_the_guard_sees_the_shapes_a_write_takes(self):
        caught = '\n'.join((
            "db.execute(\"UPDATE suggestions SET status='done' WHERE id=?\", (1,))",
            "db.execute('UPDATE suggestions SET early=0, status=? WHERE id=?', (s, 1))",
            "db.execute('UPDATE suggestions SET ' + KEEP + ',body=?,' + ('a=?' if x else 'b=?') + \",status='prepared' WHERE id=?\", ())",
            "db.execute(f\"UPDATE suggestions SET outcome=NULL,status={s!r} WHERE id=?\", (1,))",
        ))
        self.assertEqual(len(self.raw_writes(caught)), 4)
        fine = '\n'.join((
            "db.execute(\"UPDATE suggestions SET outcome=CASE WHEN status=? THEN outcome END WHERE id=?\", (s, 1))",
            "db.execute(\"UPDATE suggestions SET early=0 WHERE id=? AND status='pending'\", (1,))",
            "db.execute(\"UPDATE preparations SET status='cancelled' WHERE suggestion_id=?\", (1,))",
            "db.execute(\"UPDATE suggestions SET resume_status=? WHERE id=?\", (s, 1))",
        ))
        self.assertEqual(self.raw_writes(fine), [])


if __name__ == '__main__':
    unittest.main()
