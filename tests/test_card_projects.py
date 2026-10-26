"""To-dos on projects: a to-do takes the project its thread or the people it is about are on (one open project, never
a guess between several), the owner can change it by hand (also to none) and that stays, the project's page and
board tile list its to-dos, and the team's Graph shares no more of a to-do than before."""
import json
import unittest
import uuid

import test_graph as tg
from test_graph import NOW, graph, mail

T = NOW.isoformat()


class CardProjects(unittest.TestCase):
    setUp, add, build = tg.Boards.setUp, tg.Boards.add, tg.Boards.build
    STAGES = tg.Boards.STAGES

    def ids(self, n):
        with self.store.connect() as db:
            return [r[0] for r in db.execute('SELECT id FROM events ORDER BY id DESC LIMIT ?', (n,))][::-1]

    def card(self, event_ids, title='Reply to Ann', status='pending'):
        sid = uuid.uuid4().hex[:16]
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,?,?,?,?,?)",
                       (sid, sid, title, '', json.dumps(event_ids), '["work"]', status, T))
        return sid

    def project_of(self, sid):
        with self.store.connect() as db:
            return tuple(db.execute('SELECT project,project_by FROM suggestions WHERE id=?', (sid,)).fetchone())

    def test_a_to_do_takes_its_threads_project_and_the_owners_choice_stays(self):
        self.add(mail(4, 'Ann <ann@partner.example>', 'sam@acme.com', thread='deal'), mail(3, 'Sam <sam@acme.com>', 'ann@partner.example', ('SENT',), thread='deal'),
                 mail(2, 'Ann <ann@partner.example>', 'sam@acme.com', thread='deal'))
        first, second, last = self.ids(3)
        with self.store.connect() as db:
            graph.label(db, [first], 'Paperkite', 'review', T)  # one message of the thread is on the project
            other = graph.label(db, [second], 'Other deal', 'review', T) and graph.project_id(db, 'Other deal', T)
        self.build()
        sid = self.card([first, last])
        with self.store.connect() as db:
            db.execute('DELETE FROM event_projects WHERE project_id=?', (other,))
            db.execute("DELETE FROM graph_events WHERE node_id=?", ('project:%d' % other,))
            self.assertEqual(graph.link_cards(db), 1)
        self.assertEqual(self.project_of(sid), ('Paperkite', 'auto'))
        with self.store.connect() as db:
            pid = db.execute("SELECT id FROM projects WHERE name='Other deal'").fetchone()[0]
            self.assertEqual(graph.set_card_project(db, sid, f'project:{pid}')['name'], 'Other deal')
            graph.link_cards(db)
        self.assertEqual(self.project_of(sid), ('Other deal', 'owner'))
        with self.store.connect() as db:
            self.assertIsNone(graph.set_card_project(db, sid, ''))
            graph.link_cards(db)
            with self.assertRaises(ValueError):
                graph.set_card_project(db, sid, 'No such project')
        self.assertEqual(self.project_of(sid), (None, 'owner'))  # "no project" by hand stays too

    def test_two_projects_on_the_thread_is_no_guess(self):
        self.add(mail(4, 'Ann <ann@partner.example>', 'sam@acme.com', thread='deal'), mail(3, 'Ann <ann@partner.example>', 'sam@acme.com', thread='deal'))
        a, b = self.ids(2)
        with self.store.connect() as db:
            graph.label(db, [a], 'Paperkite', 'review', T)
            graph.label(db, [b], 'Inkwell', 'review', T)
        sid = self.card([a, b])
        with self.store.connect() as db:
            self.assertEqual(graph.link_cards(db), 0)
        self.assertEqual(self.project_of(sid), (None, None))

    def test_the_people_it_is_about_bring_their_one_project(self):
        self.add(mail(4, 'Ann <ann@partner.example>', 'sam@acme.com', thread='deal'))
        deal, = self.ids(1)
        with self.store.connect() as db:
            graph.label(db, [deal], 'Paperkite', 'review', T)
        self.build()
        self.add(mail(1, 'Ann <ann@partner.example>', 'sam@acme.com', thread='new'))
        new, = self.ids(1)
        self.build()
        with self.store.connect() as db:
            linked = db.execute("SELECT 1 FROM graph_links WHERE kind='project' AND b LIKE 'project:%'").fetchone()
        if not linked:
            self.skipTest('this graph build links no people to projects')
        sid = self.card([new])
        with self.store.connect() as db:
            graph.link_cards(db)
        self.assertEqual(self.project_of(sid)[0], 'Paperkite')

    def test_the_review_never_overrides_the_owner(self):
        self.add(mail(2, 'Ann <ann@partner.example>', 'sam@acme.com', thread='deal'))
        e, = self.ids(1)
        saved = self.store.suggest('k1', 'Reply to Ann', 'Body', [e], project='Paperkite')
        self.assertEqual(self.project_of(saved['id']), ('Paperkite', 'review'))
        with self.store.connect() as db:
            graph.set_card_project(db, saved['id'], '')
        self.store.suggest('k1', 'Reply to Ann again', 'Body', [e], project='Paperkite')
        self.assertEqual(self.project_of(saved['id']), (None, 'owner'))

    def test_the_project_page_and_its_tile_list_its_to_dos(self):
        self.add(mail(4, 'Ann <ann@partner.example>', 'sam@acme.com', thread='deal'))
        e, = self.ids(1)
        with self.store.connect() as db:
            node = graph.set_stage(db, 'Paperkite', 'Agreed', 'review', T, board='Listings', reason='Ann agreed', event_id=e)['node_id']
            pid = int(node.split(':')[1])
        self.build()
        open_ = self.card([], 'Send the listing')
        done = self.card([], 'Call Ann', status='completed')
        other = self.card([], 'Unrelated')
        with self.store.connect() as db:
            graph.set_card_project(db, open_, node)
            graph.set_card_project(db, done, 'Paperkite')
            view = graph.detail(db, node)
            self.assertEqual([(c['title'], c['done']) for c in view['todos']], [('Send the listing', False), ('Call Ann', True)])
            self.assertNotIn('cards', view['open'])  # not twice on the page
            tile = next(p for b in graph.boards(db, T) for p in b['projects'] if p['id'] == node)
            self.assertEqual(tile['todos'], 1)
            self.assertEqual(graph.card_project_view(db, 'paperkite'), {'node_id': node, 'name': 'Paperkite'})
            self.assertIn({'id': node, 'name': 'Paperkite'}, graph.project_choices(db))
        self.assertNotIn(other, [c['id'] for c in view['todos']])
        del pid

    def test_the_teams_graph_shares_no_to_do_linked_by_hand(self):
        import shared_graph as sg
        with open(sg.__file__) as f:
            source = f.read()
        self.assertNotIn('s.project', source)  # the team's records read to-dos only through their shared signals
        self.assertNotIn('project_todos', source)
        self.assertNotIn('card_project', source)


if __name__ == '__main__':
    unittest.main()
