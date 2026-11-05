"""The long lists load a page at a time: Done cards (/api/cards/done) and the Graph tabs (/api/graph/list), each in
the order asked for, with a cursor to the next page, a total, and search across everything, not only what is loaded."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_assistant import assistant as a, event
import graph


class DonePages(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [event()])
        self.ids = []
        for n in range(75):
            with patch.object(a, 'now', return_value=f'2026-10-01T10:{n // 60:02d}:{n % 60:02d}+00:00'):
                sid = self.store.suggest(f'task-{n}', f'Card {n:02d}' + (' invoice' if n % 10 == 0 else ''), 'Body', [1])['id']
            self.ids.append(sid)
        for n, sid in enumerate(self.ids):  # closed in the reverse order they were made
            with patch.object(a, 'now', return_value=f'2026-10-02T10:{(74 - n) // 60:02d}:{(74 - n) % 60:02d}+00:00'):
                self.store.decide(sid, 'complete', '', 'done-' + sid, 'dashboard')
        self.store.suggest('task-open', 'Still open', 'Body', [1])

    def test_pages_of_thirty_latest_closed_first_until_the_end(self):
        seen, cursor = [], 0
        for size in (30, 30, 15):
            got = self.store.done_page(cursor)
            self.assertEqual(len(got['cards']), size)
            self.assertEqual(got['total'], 75)
            seen += [c['title'] for c in got['cards']]
            cursor = got['next']
        self.assertIsNone(cursor)
        self.assertEqual(seen, [f'Card {n:02d}' + (' invoice' if n % 10 == 0 else '') for n in range(75)])  # card 0 was closed last
        self.assertEqual(len(set(seen)), 75)
        card = self.store.done_page(0, 1)['cards'][0]
        self.assertEqual(card['status'], 'completed'); self.assertTrue(card['closed_at'].startswith('2026-10-02'))

    def test_search_finds_every_done_card_not_only_a_page(self):
        got = self.store.done_page(0, 30, 'INVOICE')
        self.assertEqual([c['title'] for c in got['cards']], [f'Card {n:02d} invoice' for n in range(0, 75, 10)])
        self.assertEqual(got['total'], 8); self.assertIsNone(got['next'])
        self.assertEqual(self.store.done_page(0, 30, 'nothing like it')['cards'], [])

    def test_status_counts_them_all_and_still_sends_a_hundred_at_most(self):
        snap = self.store.snapshot([])
        self.assertEqual(snap['done_counts']['all'], 75)
        self.assertEqual(sum(s['status'] == 'completed' for s in snap['suggestions']), 75)
        self.assertTrue(any(s['title'] == 'Still open' for s in snap['suggestions']))


class DoneByWhenClosed(unittest.TestCase):
    """Done starts with the one finished last: a to-do made long ago and sent just now is the newest done one, in the
    status payload too, with when it closed (the card says "Done 5 minutes ago"). A search finds it by who it went to."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [event()])
        self.ids = []
        for n in range(101):
            with patch.object(a, 'now', return_value=f'2026-10-01T10:{n // 60:02d}:{n % 60:02d}+00:00'):
                self.ids.append(self.store.suggest(f'task-{n}', f'Card {n:03d}', 'Body', [1])['id'])
        for n, sid in enumerate(self.ids[1:] + self.ids[:1]):  # the oldest one closed last, like a send tonight
            with patch.object(a, 'now', return_value=f'2026-10-02T10:{n // 60:02d}:{n % 60:02d}+00:00'):
                self.store.decide(sid, 'complete', '', 'done-' + sid, 'dashboard')

    def test_status_sends_the_hundred_closed_last_with_when(self):
        done = {s['id']: s for s in self.store.snapshot([])['suggestions'] if s['status'] == 'completed'}
        self.assertEqual(len(done), 100)
        self.assertIn(self.ids[0], done)  # made first, closed last
        self.assertNotIn(self.ids[1], done)  # closed first
        self.assertEqual(done[self.ids[0]]['closed_at'], '2026-10-02T10:01:40+00:00')
        self.assertEqual(self.store.done_page(0, 1)['cards'][0]['id'], self.ids[0])

    def test_search_finds_a_done_one_by_who_it_went_to(self):
        action = {'kind': 'email', 'revision': 'r1', 'label': 'Send', 'to': ['lena.moss@uni.example.edu'], 'to_name': 'Lena Moss',
                  'cc': ['ari@uni.example.edu'], 'subject': 'Agreements', 'body': 'Hi Lena'}
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET next_action=? WHERE id=?', (json.dumps(action), self.ids[5]))
        for q in ('lena', 'Moss', 'uni.example.edu', 'ari@'):
            self.assertEqual([c['id'] for c in self.store.done_page(0, 30, q)['cards']], [self.ids[5]], q)
        self.assertEqual(a.card_recipients(json.dumps({'kind': 'menu', 'actions': [action, {'kind': 'open', 'url': 'https://x.example'}]})),
                         'Lena Moss lena.moss@uni.example.edu ari@uni.example.edu')
        self.assertEqual(a.card_recipients(None), '')

    def test_one_that_looks_done_says_since_when(self):
        with patch.object(a, 'now', return_value='2026-10-03T09:00:00+00:00'):
            sid = self.store.suggest('task-hint', 'Answer Elif', 'Body', [1])['id']
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET handled_hint=? WHERE id=?', (json.dumps({'reason': 'Elif confirmed it', 'at': '2026-10-03T11:00:00+00:00'}), sid))
        card = next(s for s in self.store.snapshot([])['suggestions'] if s['id'] == sid)
        self.assertEqual(card['looks_done_at'], '2026-10-03T11:00:00+00:00')
        self.assertNotIn('looks_done_at', next(s for s in self.store.snapshot([])['suggestions'] if s['id'] == self.ids[0]))


class GraphTabs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store; self.app.config = {'accounts': []}
        with self.store.connect() as db:
            graph.ensure(db)
            db.execute("INSERT INTO graph_state VALUES(1,'2026-10-20T09:00:00+00:00',10,1)")
            for n in range(70):
                db.execute('INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,quiet,trend,info) VALUES(?,?,?,?,?,?,?,?,?)',
                           (f'email:p{n:02d}@example.com', 'person', f'Person {69 - n:02d}', 2 - n / 100, (f'2026-10-19T0{n}:00:00+00:00' if n < 5 else f'2026-10-{1 + n % 12:02d}T09:00:00+00:00'),
                            2 if n < 5 else 9, int(n % 7 == 0), None, '{}'))
            for n in range(4):
                db.execute('INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,quiet,trend,info) VALUES(?,?,?,?,?,?,?,?,?)',
                           (f'project:{n}', 'project', f'Project {n}', [0.2, 2, 1.5, 1][n], f'2026-10-1{n}T09:00:00+00:00', 5, 0, [None, 0.5, 1.0, 2.0][n],
                            json.dumps({'closed_at': '2026-10-01'} if n == 3 else {})))

    def test_each_tab_pages_by_cursor_in_its_order(self):
        first = self.app.graph_list('people')
        self.assertEqual(len(first['items']), 30); self.assertEqual(first['total'], 70); self.assertEqual(first['sort'], 'closest')
        self.assertEqual(first['items'][0]['id'], 'email:p00@example.com')
        rest = self.app.graph_list('people', 'closest', first['next']); last = self.app.graph_list('people', 'closest', rest['next'])
        self.assertEqual(len(last['items']), 10); self.assertIsNone(last['next'])
        ids = [x['id'] for x in first['items'] + rest['items'] + last['items']]
        self.assertEqual(len(set(ids)), 70)
        names = [x['name'] for x in self.app.graph_list('people', 'name', 0, 50)['items']]
        self.assertEqual(names, sorted(names)); self.assertEqual(names[0], 'Person 00')
        last_at = [x['last_at'] for x in self.app.graph_list('people', 'last', 0, 50)['items']]
        self.assertEqual(last_at, sorted(last_at, reverse=True))
        self.assertEqual(self.app.graph_list('quiet')['total'], 10)
        self.assertEqual(self.app.graph_list('new')['total'], 5)

    def test_projects_open_and_done_by_activity_or_stage(self):
        self.assertEqual([p['name'] for p in self.app.graph_list('projects')['items']], ['Project 2', 'Project 1', 'Project 0'])  # last activity
        self.assertEqual([p['state'] for p in self.app.graph_list('projects', 'stage')['items']], ['active', 'cooling', 'dormant'])
        self.assertEqual([p['name'] for p in self.app.graph_list('projects_done')['items']], ['Project 3'])
        self.assertEqual(self.app.graph_list('people', 'stage')['sort'], 'closest', 'stage is for projects only')

    def test_counts_for_the_tabs_and_search_by_page(self):
        with self.store.connect() as db:
            counts = graph.list_counts(db)
        self.assertEqual({k: counts[k] for k in ('people', 'quiet', 'new', 'orgs', 'projects', 'projects_done', 'warmup')},
                         {'people': 70, 'quiet': 10, 'new': 5, 'orgs': 0, 'projects': 3, 'projects_done': 1, 'warmup': 0})
        found = self.app.graph_find('person')
        self.assertEqual(len(found['found']), 30); self.assertEqual(found['next'], '30')
        self.assertEqual(len(self.app.graph_find('person', found['next'])['found']), 30)
        with self.assertRaises(ValueError):
            self.app.graph_list('events')


if __name__ == '__main__':
    unittest.main()
