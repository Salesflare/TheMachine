"""The owner's edits in the Graph answer at once: a whole build before the answer held each one 15 to 25 s on a big
Graph. With the graph worker running, each edit is on its page in the edit's own transaction and the build follows in
the worker; the build is stubbed slow here, so an edit that still waited for it would fail the timing."""
import base64
import threading
import time
import unittest

import test_graph as tg

a, graph = tg.a, tg.graph
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==')


class AnswersFast(unittest.TestCase):
    add = tg.Graph.add
    build = tg.Graph.build
    node = tg.Graph.node

    def setUp(self):
        tg.Graph.setUp(self)
        self.add(tg.mail(3, 'Ivy Park <ivy@globex.example>', 'sam@acme.com'), tg.mail(2, 'Sam <sam@acme.com>', 'Ivy Park <ivy@globex.example>', ('SENT',)),
                 tg.mail(1, 'Rex Moon <rex@initech.example>', 'sam@acme.com', cc='Ivy Park <ivy@globex.example>'))
        self.build()
        self.builds = []
        self.app.graph_build = lambda *a, **k: self.builds.append(time.sleep(2))
        self.app.graph_worker_on, self.app.graph_dirty = True, threading.Event()

    def act(self, action, **args):
        self.app.graph_dirty.clear()
        start = time.monotonic()
        done = self.app.action(action, args, owner_dashboard=True)
        self.assertLess(time.monotonic() - start, 0.3, action)
        self.assertEqual(self.builds, [], action)
        self.assertTrue(self.app.graph_dirty.is_set(), action)  # the graph worker builds the rest
        return done

    def page(self, node):
        return self.app.graph_action({'node_id': node})

    def test_an_organization_edit_its_name_and_wrong_company(self):
        self.act('graph_org_edit', node_id='org:globex.example', fields={'industry': 'Logistics', 'notes': 'Key account'}, name='Globex Group')
        view = self.page('org:globex.example')
        self.assertEqual((view['name'], view['profile']['industry'], view['profile']['website']), ('Globex Group', 'Logistics', 'https://globex.example'))
        self.assertIn('industry', view['edited'])
        self.act('graph_org_wrong', node_id='org:globex.example', wrong=True)
        self.assertTrue(self.node('org:globex.example')['wrong'])

    def test_a_new_person_and_a_new_organization_open_at_once(self):
        made = self.act('graph_new', kind='person', name='Nia Vale', email='nia@initech.example')
        view = self.page(made['node_id'])
        self.assertEqual((view['name'], view['org']), ('Nia Vale', 'org:initech.example'))  # their work address says where
        made = self.act('graph_new', kind='person', name='Olu Rae', org='Brand New Co')
        view = self.page(made['node_id'])
        self.assertEqual((view['name'], view['org_name'], view['org_by']), ('Olu Rae', 'Brand New Co', 'owner'))
        org = self.act('graph_new', kind='org', name='Hollow Pine', website='hollowpine.example')
        view = self.page(org['node_id'])
        self.assertEqual((view['name'], view['profile']['website']), ('Hollow Pine', 'https://hollowpine.example'))
        self.act('graph_org_delete', node_id=org['node_id'])
        self.assertIsNone(self.node(org['node_id']))
        # The build that follows keeps them
        self.app.graph_build = lambda *a, **k: None
        self.build()
        self.assertEqual(self.node(made['node_id'])['name'], 'Olu Rae')

    def test_a_rename_a_picture_their_organization_and_a_relation(self):
        node = 'email:ivy@globex.example'
        self.act('graph_rename', node_id=node, name='Ivy P. Park')
        self.act('graph_rename', node_id='org:initech.example', name='Initech Labs')
        self.assertEqual((self.node(node)['name'], self.node('org:initech.example')['name']), ('Ivy P. Park', 'Initech Labs'))
        done = self.act('graph_picture', node_id=node, data='data:image/png;base64,' + base64.b64encode(PNG).decode())
        self.assertEqual(self.node(node)['profile']['photo'], done['picture'])
        self.act('graph_person_org', node_id=node, org='Initech Labs')
        self.assertEqual((self.node(node)['org'], self.node(node)['org_by']), ('org:initech.example', 'owner'))
        self.app.graph_build = lambda *a, **k: None
        self.app.graph_action({'node_id': node, 'related_to': 'email:rex@initech.example', 'relation': 'assistant of'}, source='owner')
        self.build()
        self.assertTrue(self.node(node)['relations'])
        self.app.graph_build = lambda *a, **k: self.builds.append(time.sleep(2))
        self.act('graph_relation', node_id=node, related_to='email:rex@initech.example', relation='')
        self.assertEqual((self.node(node)['relations'], self.node('email:rex@initech.example')['relations']), ([], []))

    def test_a_project_save_and_delete_permanently(self):
        made = self.act('project_save', name='Quillfeather', people=['email:ivy@globex.example'])
        view = self.page(made['node_id'])
        self.assertEqual(view['name'], 'Quillfeather')
        with self.store.connect() as db:
            self.assertTrue(db.execute("SELECT 1 FROM graph_links WHERE a='email:ivy@globex.example' AND b=? AND kind='project'", (made['node_id'],)).fetchone())
        self.act('project_save', node_id=made['node_id'], name='Quillfeather Deal')
        self.assertEqual(self.node(made['node_id'])['name'], 'Quillfeather Deal')
        self.act('graph_person_delete', node_id='email:rex@initech.example')
        self.assertIsNone(self.node('email:rex@initech.example'))


if __name__ == '__main__':
    unittest.main()
