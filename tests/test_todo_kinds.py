"""machine/todo_kinds.py: the core paths ask the registry, and each kind's traits keep what those paths did before."""
import ast
import pathlib
import sqlite3
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from machine import todo_kinds  # noqa: E402

# The paths that once named each kind's module, and the modules they named
CORE = ('machine/delivery/deliver.py', 'machine/cards.py', 'machine/store/views.py', 'machine/app/card_actions.py',
        'machine/app/notifications.py')


class TodoKindsTest(unittest.TestCase):
    def test_each_kind_names_functions_its_module_has(self):
        for kind in todo_kinds.KINDS:
            with self.subTest(kind=kind.key):
                code = kind.code()
                self.assertTrue(callable(getattr(code, kind.view_name)))
                if kind.test_name:
                    self.assertTrue(callable(getattr(code, kind.test_name)))

    def test_the_traits_keep_what_each_path_did(self):
        traits = {k.key: (k.quiet, k.reading, k.close_only, bool(k.refused), bool(k.reads)) for k in todo_kinds.KINDS}
        self.assertEqual(traits, {
            'cleanup': (True, True, True, True, True),
            'subs': (True, False, False, True, False),  # its card keeps every choice, an area's digest keeps it
            'digest': (True, True, True, True, True),
            'facebook_birthdays': (False, False, False, False, False),  # only its view is its own
        })
        # the owner's decision asked cleanup, then Subscriptions, then the digest
        self.assertEqual([k.key for k in todo_kinds.KINDS if k.refused], ['cleanup', 'subs', 'digest'])

    def test_core_paths_ask_the_registry_not_a_kinds_module(self):
        modules = {k.module for k in todo_kinds.KINDS}
        for rel in CORE:
            tree = ast.parse((ROOT / rel).read_text(encoding='utf-8'))
            imported = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
            with self.subTest(path=rel):
                self.assertEqual(imported & modules, set())

    def test_a_database_before_the_tables(self):
        db = sqlite3.connect(':memory:')
        db.row_factory = sqlite3.Row
        db.execute('CREATE TABLE events(id INTEGER PRIMARY KEY,deleted INTEGER)')
        self.assertFalse(todo_kinds.quiet(db, 's1'))
        self.assertIsNone(todo_kinds.refused(db, 's1'))
        self.assertEqual(todo_kinds.reads(db, '["s1"]'), {})
        self.assertEqual(todo_kinds.reading_ids(db), set())
        self.assertEqual(todo_kinds.views(db, 's1', []), {})

    def test_reads_and_views_agree_with_one_by_one(self):
        import mail_cleanup
        import reading_digest
        import subscriptions
        db = sqlite3.connect(':memory:')
        db.row_factory = sqlite3.Row
        db.execute('CREATE TABLE events(id INTEGER PRIMARY KEY,deleted INTEGER)')
        for module in (mail_cleanup, reading_digest, subscriptions):
            module.ensure(db)
        mail_cleanup.record(db, 'c1', 'newsletters', [{'account': 'a', 'address': 'n@x.example'}], 'T')
        reading_digest.record(db, 'd1', [{'event': None, 'account': 'a', 'address': 'n@x.example', 'topic': 't'}], 'T')
        subscriptions.record(db, 'u1', [{'key': 'k', 'next': '2026-12-01'}], 'T')
        metas = {'c1': [{'cleanup': 'newsletters', 'items': [{'from': 'N', 'address': 'n@x.example'}]}],
                 'd1': [{'digest': True, 'items': [{'title': 'A piece'}]}],
                 'u1': [{'subs': True, 'rows': [{'name': 'S', 'amount': '1', 'currency': 'EUR'}]}]}
        pre = todo_kinds.reads(db, '["c1","d1","u1"]')
        self.assertEqual(set(pre), {'cleanup', 'digest'})
        for sid, key in (('c1', 'cleanup'), ('d1', 'digest'), ('u1', 'subs')):
            with self.subTest(todo=sid):
                one = todo_kinds.views(db, sid, metas[sid])
                self.assertEqual(list(one), [key])
                self.assertEqual(one, todo_kinds.views(db, sid, metas[sid], pre))
                self.assertTrue(todo_kinds.quiet(db, sid))
                self.assertTrue(todo_kinds.refused(db, sid))
                self.assertEqual(todo_kinds.close_only(one), key != 'subs')
        self.assertEqual(todo_kinds.reading_ids(db), {'c1', 'd1'})
        self.assertFalse(todo_kinds.quiet(db, 'other'))


if __name__ == '__main__':
    unittest.main()
