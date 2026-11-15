"""The graph worker's build in a process of its own (graph_apart): the child builds exactly the graph a build in the
server's process makes, on a plain and on a protected (sealed) store; an edit meanwhile is Outdated there as here;
where no child can run, or it fails, the caller builds in-process."""
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import test_graph as tg
import assistant as a
import graph
import graph_apart as apart
import timeutil
import machine.main as machine_main

CONFIG = {**tg.CONFIG, 'embeddings': {'model': 'test', 'dims': 4}}
GRAPH = ('SELECT id,kind,name,strength,signals FROM graph_nodes ORDER BY id', 'SELECT * FROM graph_links ORDER BY 1,2,3',
         'SELECT node_id,event_id,probable,direct FROM graph_events ORDER BY 1,2')


class Apart(unittest.TestCase):
    PROTECT = None

    def setUp(self):
        timeutil.pin(tg.NOW); self.addCleanup(timeutil.pin, None)
        self.stores = [self.store()]

    def store(self):
        """A store with the same three messages each time."""
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        store = machine_main.Store(Path(temp.name) / 'events.sqlite', protect=self.PROTECT)
        for e in (tg.mail(9, 'Sam <sam@acme.com>', 'Ann Lee <ann@partner.example>', ('SENT',), thread='deal'),
                  tg.mail(3, 'Ann Lee <ann@partner.example>', 'sam@acme.com', thread='deal', title='Re: the listing'),
                  tg.mail(1, 'Sam <sam@acme.com>', 'Bo <bo@other.example>', ('SENT',), thread='other')):
            store.commit_page(e['account_id'], {}, [e])
        return store

    def built(self, store):
        with store.connect() as db:
            return [[tuple(r) for r in db.execute(q)] for q in GRAPH]

    def here(self, store):
        with store.connect() as db:
            db.isolation_level = None
            return graph.build(db, CONFIG, tg.NOW.isoformat(), set(), {}, history=True)

    def test_the_child_builds_what_building_here_builds(self):
        self.stores.append(self.store())
        here = self.here(self.stores[0])
        there = apart.run(self.stores[1], CONFIG, tg.NOW.isoformat(), set(), {}, history=True, lock_last=True)
        self.assertIsNotNone(there, 'the child ran')
        self.assertTrue(self.built(self.stores[0])[0], 'people to compare')
        self.assertEqual(self.built(self.stores[1]), self.built(self.stores[0]))
        self.assertEqual({k: v for k, v in there.items() if k not in ('took_ms', 'passes_ms')},
                         {k: v for k, v in here.items() if k not in ('took_ms', 'passes_ms')})

    def test_an_edit_meanwhile_is_outdated_as_here(self):
        with mock.patch.object(apart, '_loads', side_effect=[{'outdated': True}]):
            with self.assertRaises(graph.Outdated):
                apart.run(self.stores[0], CONFIG, tg.NOW.isoformat(), set(), {}, history=True, lock_last=False)
        with mock.patch.object(graph, 'build', side_effect=graph.Outdated()):  # the child says so, and nothing else
            self.assertEqual(apart.build(None, {'config': CONFIG, 'now': '', 'team': set(), 'kin': {}, 'history': True, 'lock_last': False}),
                             {'outdated': True})

    def test_where_no_program_may_start_the_caller_builds_here(self):
        with mock.patch.object(subprocess, 'Popen', side_effect=PermissionError('sandbox: no programs')):
            self.assertIsNone(apart.run(self.stores[0], CONFIG, tg.NOW.isoformat(), set(), {}, history=True, lock_last=True))

    def test_a_child_that_fails_gives_none_and_logs_only_the_kind_of_error(self):
        store = self.stores[0]
        broken = mock.Mock(path=Path(store.path).parent / 'missing' / 'events.sqlite', _seal_key=store._seal_key,
                           sealer=store.sealer, protected=False)
        with self.assertLogs('personal-assistant', 'WARNING') as logs:
            self.assertIsNone(apart.run(broken, CONFIG, tg.NOW.isoformat(), set(), {}, history=True, lock_last=True))
        self.assertIn('reason=child_exit', logs.output[0])
        self.assertNotIn('missing', logs.output[0])

    def test_the_worker_builds_apart_and_here_when_no_child_can(self):
        app = mock.Mock(store=self.stores[0], config=CONFIG, fleet_addresses=set, fleet_circles=dict)
        with mock.patch.object(apart, 'run', return_value=None) as run:
            summary = machine_main.App.graph_build(app, apart=True)
        run.assert_called_once()
        self.assertTrue(summary['people'], 'built here instead')
        with mock.patch.object(apart, 'run') as run:
            machine_main.App.graph_build(app)
        run.assert_not_called()  # an owner's edit that waits on the build (graph_build) builds here, as before


class SealedApart(Apart):
    """The child writes a protected store with the same key."""
    PROTECT = True

    def setUp(self):
        super().setUp()
        self.assertTrue(self.stores[0].sealer and self.stores[0]._seal_key)


if __name__ == '__main__':
    unittest.main()
