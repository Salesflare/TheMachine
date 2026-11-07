"""History in the Graph (machine/graph_history.py): older mail counts toward closeness, last talked, who knows whom and
the people and organizations, by counting only; never toward projects, "new", reviews, lookups or the Network, and
Fleet answers read it under the same rules as signals. Nothing of it before a graph pass took it in."""
import json
import unittest

import test_graph as tg
import fleet
import person_summary
from machine import graph_history

a, graph, mail = tg.a, tg.graph, tg.mail
HOME = {'id': 'home', 'email': 'sam@home.example', 'boundary': 'personal:Home'}
CONFIG = {**tg.CONFIG, 'accounts': [*tg.CONFIG['accounts'], HOME]}


def old(days_ago, sender, to, account='work', **extra):
    return {**mail(days_ago, sender, to, **extra), 'account_id': account}


class HistoryGraph(unittest.TestCase):
    node = tg.Graph.node

    def setUp(self):
        tg.Graph.setUp(self)
        self.app.config = CONFIG
        self.live = mail(2, 'Kim Lee <kim@client.example>', 'sam@acme.com', thread='deal')
        self.store.commit_page('work', {}, [self.live, mail(1, 'Sam <sam@acme.com>', 'kim@client.example', ('SENT',), thread='deal')])
        history = [old(200, 'Kim Lee <kim@client.example>', 'sam@acme.com', thread='deal'),
                   old(150, 'Sam <sam@acme.com>', 'kim@client.example', labels=('SENT',)),
                   old(120, 'Sam <sam@acme.com>', 'ann@client.example, kim@client.example', labels=('SENT',)),
                   old(110, 'Ann Bell <ann@client.example>', 'sam@acme.com'),
                   old(100, 'Robot <noreply@service.example>', 'sam@acme.com'),
                   old(90, 'Pat Home <pat@gmail.com>', 'sam@home.example', account='home'),
                   old(80, 'Sam <sam@home.example>', 'pat@gmail.com', account='home', labels=('SENT',))]
        for e in history:
            self.store.commit_page(e['account_id'], None, [e], record_sync=False, history=True)
        with self.store.connect() as db:
            db.execute("INSERT INTO projects(id,name,created_at) VALUES(1,'Deal',?)", (tg.NOW.isoformat(),))
            live_id = db.execute('SELECT id FROM events WHERE source_id=?', (self.live['source_id'],)).fetchone()[0]
            db.execute("INSERT INTO event_projects(event_id,project_id,source,created_at) VALUES(?,1,'review',?)", (live_id, tg.NOW.isoformat()))
            self.history_ids = {r[0] for r in db.execute('SELECT id FROM events WHERE history=1')}

    def build(self):
        with self.store.connect() as db:
            db.isolation_level = None
            return graph.build(db, CONFIG, tg.NOW.isoformat(), history=True)

    def advance(self, step=graph_history.STEP):
        horizon = (tg.NOW - tg.dt.timedelta(days=graph.HORIZON_DAYS)).isoformat()
        with self.store.connect() as db:
            return graph_history.advance(db, horizon, tg.NOW.isoformat(), step)

    def test_no_history_before_a_graph_pass_took_it_in(self):
        self.assertEqual(self.build()['history'], 0)
        self.assertIsNone(self.node('email:ann@client.example'))
        kim = self.node('email:kim@client.example')
        self.assertEqual(kim['signals'], 2)

    def test_each_pass_takes_in_a_bounded_slice_newest_first(self):
        self.assertTrue(self.advance(step=2))
        self.assertEqual(self.build()['history'], 2)
        self.assertTrue(self.advance(step=2))
        self.assertEqual(self.build()['history'], 4)
        while self.advance(step=2):
            pass
        self.assertEqual(self.build()['history'], 7)
        self.assertFalse(self.advance(step=2))

    def test_history_counts_toward_people_closeness_and_who_knows_whom_only(self):
        self.build()
        before = self.node('email:kim@client.example')
        self.advance()
        self.build()
        kim, ann = self.node('email:kim@client.example'), self.node('email:ann@client.example')
        self.assertGreater(kim['strength'], before['strength'])
        self.assertEqual(kim['signals'], 2)  # its signals; history counted apart
        self.assertEqual((ann['name'], ann['org']), ('Ann Bell', 'org:client.example'))
        self.assertIsNone(self.node('email:noreply@service.example'))  # automated senders stay out, as with signals
        with self.store.connect() as db:
            info = json.loads(db.execute("SELECT info FROM graph_nodes WHERE id='email:ann@client.example'").fetchone()[0])
            self.assertEqual((info['live'], info['history']), (0, 2))
            self.assertTrue(db.execute("SELECT 1 FROM graph_links WHERE kind='together' AND a='email:ann@client.example' AND b='email:kim@client.example'").fetchone())
            # graph_events (what reviews, preparations, to-dos and the Team Graph read) holds signals only
            self.assertFalse({r[0] for r in db.execute('SELECT event_id FROM graph_events')} & self.history_ids)
            self.assertEqual({r[0] for r in db.execute("SELECT event_id FROM graph_history_events WHERE node_id LIKE 'project:%'")}, set())
            project = {r[0] for r in db.execute("SELECT event_id FROM graph_events WHERE node_id='project:1'")}
            self.assertEqual(project & self.history_ids, set())  # an old mail in the deal's thread never joins the project
            # never "new", never a review's or a summary's pick, never looked up
            self.assertNotIn('email:ann@client.example', [p['id'] for p in graph.overview(db)['new']])
            picked = db.execute(f"SELECT id FROM graph_nodes WHERE kind='person' AND {graph_history.live()}>=0.01").fetchall()
            self.assertNotIn('email:ann@client.example', [r[0] for r in picked])
            self.assertNotIn('email:ann@client.example', [p['id'] for p in person_summary.active(db, tg.NOW)])

    def test_fleet_who_knows_reads_work_history_and_never_personal_history(self):
        self.advance()
        self.build()
        work = fleet.work_accounts(CONFIG)
        with self.store.connect() as db:
            self.assertTrue(fleet.relationships(db, 'ann@client.example', work, False)['knows'])
            self.assertFalse(fleet.relationships(db, 'pat@gmail.com', work, False)['knows'])  # only personal history
            # a Team Graph gate that shares nothing: history goes nowhere a signal wouldn't
            self.assertFalse(fleet.relationships(db, 'ann@client.example', work, False, ok=lambda row: False)['knows'])
            pat = json.loads(db.execute("SELECT info FROM graph_nodes WHERE id='email:pat@gmail.com'").fetchone()[0])
        self.assertEqual(pat['side'], 'personal')


if __name__ == '__main__':
    unittest.main()
