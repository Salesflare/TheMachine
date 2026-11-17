"""The Shared Graph's collect in a process of its own (shared_graph_apart): the child hands back exactly what collecting
in the server's process gives, on a plain and on a protected (sealed) store; where no child can run, or it fails, the
caller collects in-process; and the pipe carries plain values only."""
import datetime as dt
import pickle
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import test_graph as tg
import assistant as a
import shared_graph as sg
import shared_graph_apart as apart
import timeutil

KEYS, SECRET = [b'k' * 32, b'o' * 32], b's' * 32


class Apart(unittest.TestCase):
    PROTECT = None

    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite', protect=self.PROTECT)
        timeutil.pin(tg.NOW); self.addCleanup(timeutil.pin, None)
        clock = tg.patch_everywhere(a, 'now', lambda: tg.NOW.isoformat()); clock.start(); self.addCleanup(clock.stop)
        with self.store.connect() as db:
            tg.graph.save_board(db, {'name': 'Listings', 'stages': tg.Boards.STAGES}, tg.NOW.isoformat())
        for e in (tg.mail(9, 'Sam <sam@acme.com>', 'ann@partner.example', ('SENT',), thread='deal'),
                  tg.mail(3, 'Ann <ann@partner.example>', 'sam@acme.com', thread='deal'),
                  tg.mail(1, 'Sam <sam@acme.com>', 'bo@other.example', ('SENT',), thread='other')):
            self.store.commit_page(e['account_id'], {}, [e])
        with self.store.connect() as db:
            sg.ensure(db)
            ids = [r[0] for r in db.execute('SELECT id FROM events ORDER BY occurred_at')]
            node = tg.graph.set_stage(db, 'Paperkite', 'Agreed', 'review', tg.NOW.isoformat(), board='Listings',
                                      reason='Ann agreed', event_id=ids[1], next_step='Publish the listing')['node_id']
        tg.Graph.build(self)
        with self.store.connect() as db:
            sg.judge(db, [{'event_id': i, 'share': 'client', 'line': 'A line'} for i in ids])
            db.execute("UPDATE share_threads SET sorted_at='2026-01-01T00:00:00+00:00'")  # sorted long ago: past the hold
            threads = sorted(r[0] for r in db.execute('SELECT DISTINCT thread FROM share_threads'))
        self.scope = (['work'], ['acme.com'], ['sam@acme.com'], [])
        self.grants = [([int(node.split(':')[1])], []), ([], threads[:1])]
        self.kept = set(threads[1:])

    def here(self):
        with self.store.connect() as db:
            return apart.collect(db, {'scope': self.scope, 'keys': KEYS, 'secret': SECRET, 'kept': self.kept, 'grants': self.grants})

    def test_the_child_gives_what_collecting_here_gives(self):
        here = self.here()
        self.assertTrue(here[0][0] and here[0][1], 'something to share')
        self.assertEqual(len(here), 1 + len(self.grants))
        apart_ = apart.run(self.store, self.scope, KEYS, SECRET, self.kept, self.grants)
        self.assertIsNotNone(apart_, 'the child ran')
        self.assertEqual(sg.canon([[r, t, s, f, sorted(h)] for r, t, s, f, h in apart_]),
                         sg.canon([[r, t, s, f, sorted(h)] for r, t, s, f, h in here]))

    def test_the_child_also_says_which_tables_it_read_and_the_people_it_looked_at(self):
        found, read, looked = apart.run(self.store, self.scope, KEYS, SECRET, self.kept, self.grants, reads=True)
        self.assertEqual(sg.canon([[r, t, s, f, sorted(h)] for r, t, s, f, h in found]),
                         sg.canon([[r, t, s, f, sorted(h)] for r, t, s, f, h in self.here()]))
        self.assertTrue({'events', 'graph_nodes', 'graph_links', 'share_threads', 'projects'} <= set(read), read)
        with self.store.connect() as db:
            people = [r[0] for r in db.execute("SELECT id FROM graph_nodes WHERE kind='person' ORDER BY strength DESC LIMIT ?", (sg.MAX_RECORDS,))]
        self.assertEqual(sorted(looked['top']), sorted(people))

    def test_where_no_program_may_start_it_says_so_and_the_caller_collects_here(self):
        with mock.patch.object(subprocess, 'Popen', side_effect=PermissionError('sandbox: no programs')):
            self.assertIsNone(apart.run(self.store, self.scope, KEYS, SECRET, self.kept, self.grants))

    def test_a_child_that_fails_gives_none_and_logs_only_the_kind_of_error(self):
        broken = mock.Mock(path=Path(self.store.path).parent / 'missing' / 'events.sqlite', _seal_key=self.store._seal_key,
                           sealer=self.store.sealer, protected=False)
        with self.assertLogs('personal-assistant', 'WARNING') as logs:
            self.assertIsNone(apart.run(broken, self.scope, KEYS, SECRET, self.kept, self.grants))
        self.assertIn('reason=child_exit', logs.output[0])
        self.assertNotIn('missing', logs.output[0])


class SealedApart(Apart):
    PROTECT = True

    def test_the_child_reads_the_sealed_messages_with_the_same_key(self):
        self.assertTrue(self.store.sealer and self.store._seal_key)
        self.test_the_child_gives_what_collecting_here_gives()


class Plain(unittest.TestCase):
    def test_plain_values_cross_and_any_object_is_refused(self):
        value = {'a': [1, 2.5, 'x', b'y', None, True], 'b': {('t', 1)}, 'c': frozenset({3})}
        self.assertEqual(apart._loads(apart._dumps(value)), value)
        for thing in (dt.datetime(2026, 1, 1), Path('/x'), mock.Mock):
            with self.assertRaises(pickle.UnpicklingError):
                apart._loads(pickle.dumps(thing))


if __name__ == '__main__':
    unittest.main()
