"""About you: the owner's own addresses and numbers are always the owner, never a person in the Graph. New person and
an import refuse them, a person made from one before is folded in (backed up first, its Keep private gone), and
Keep private isn't offered on it. Also: a person's or organization's picture, and where Also on Slack goes."""
import json
import unittest

import test_graph as tg

a, graph = tg.a, tg.graph
PNG = bytes.fromhex('89504e470d0a1a0a0000000d4948445200000001000000010806000000'
                    '1f15c4890000000d49444154789c6360000002000001e221bc330000000049454e44ae426082')


class AboutYou(unittest.TestCase):
    add = tg.Graph.add
    build = tg.Graph.build
    node = tg.Graph.node

    def setUp(self):
        tg.Graph.setUp(self)
        self.app.config = {**tg.CONFIG, 'owner_phones': ['+32 470 12 34 56']}
        self.app.own_addresses_view = lambda: {'yours': [{'address': 'sam@acme.com', 'sources': ['Work'], 'removable': False}]}

    def new(self, kind, **args):
        return self.app.action('graph_new', {'kind': kind, **args}, owner_dashboard=True)

    def test_the_owner_has_their_addresses_aliases_and_numbers(self):
        with self.store.connect() as db:
            owner = graph.Owner(self.app.config, db)
        for mine in ('email:sam@acme.com', 'wa:32470123456', 'slack:U0OWNER'):
            self.assertTrue(owner.has(mine), mine)
        for theirs in ('email:ann@client.com', 'wa:32470999999', 'slack:U0ANN', 'org:acme.com'):
            self.assertFalse(owner.has(theirs), theirs)

    def test_new_person_with_the_owners_own_address_is_about_you(self):
        made = self.new('person', name='Sam Test', email='Sam@Acme.com')
        self.assertEqual(made, {'node_id': graph.ME, 'name': 'About you', 'existing': True, 'yours': True})
        self.build()
        self.assertIsNone(self.node('email:sam@acme.com'))
        page = self.app.about_you()
        self.assertEqual((page['id'], page['name']), ('me', 'About you'))
        self.assertEqual([e['value'] for e in page['emails']], ['sam@acme.com'])
        self.assertTrue(self.app.about_you_node('email:sam@acme.com'))
        self.assertTrue(self.app.about_you_node('me'))
        self.assertFalse(self.app.about_you_node('email:ann@client.com'))

    def test_a_person_made_from_the_owners_address_before_is_folded_in_with_a_backup(self):
        with self.store.connect() as db:  # made the old way: New person had no check yet, and Keep private was on
            graph.create_record(db, 'person', {'name': 'Sam Test', 'email': 'sam@acme.com'}, tg.NOW.isoformat())
            db.execute("INSERT INTO person_edits(identifier,fields,updated_at) VALUES('email:sam@acme.com',?,?)",
                       (json.dumps({'phones': {'added': ['+44 7700 900123']}}), tg.NOW.isoformat()))
            db.execute("CREATE TABLE IF NOT EXISTS share_private(node_id TEXT PRIMARY KEY,at TEXT NOT NULL)")
            db.execute("INSERT INTO share_private(node_id,at) VALUES('email:sam@acme.com',?)", (tg.NOW.isoformat(),))
        self.build()
        self.assertIsNone(self.node('email:sam@acme.com'))
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM share_private").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM manual_nodes").fetchone()[0], 0)
            backup = db.execute("SELECT identifier,rows FROM self_record_backups").fetchall()
            self.assertEqual([r[0] for r in backup], ['email:sam@acme.com'])
            rows = json.loads(backup[0][1])
            self.assertLessEqual({'manual_nodes', 'person_edits', 'share_private'}, set(rows))
            self.assertEqual([r[0] for r in db.execute("SELECT number FROM owner_numbers")], ['+447700900123'])
            self.assertTrue(graph.Owner(self.app.config, db).has('wa:447700900123'))
        self.build()  # once: nothing left to fold
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM self_record_backups").fetchone()[0], 1)

    def test_keep_private_is_not_offered_on_about_you(self):
        self.app.fleet = None
        with self.assertRaisesRegex(ValueError, 'About you'):
            self.app.graph_share_action('graph_private', {'node_id': 'email:sam@acme.com', 'private': True})

    def test_an_import_keeps_the_owners_own_row_in_about_you(self):
        text = 'Name,Email,Phone\nSam Test,sam@acme.com,\nAnn Bell,ann@client.com,\nNo Mail,,+32 470 12 34 56\n'
        with self.store.connect() as db:
            seen = a.crm_import.preview(db, 'person', text, owner_emails={'sam@acme.com'})
        why = {r['record'].get('name'): (r['status'], r.get('why')) for r in seen['rows']}
        self.assertEqual(why['Sam Test'], ('skip', a.crm_import.YOURS))
        self.assertEqual(why['Ann Bell'][0], 'new')


class Pictures(unittest.TestCase):
    add = tg.Graph.add
    build = tg.Graph.build
    node = tg.Graph.node

    def setUp(self):
        tg.Graph.setUp(self)
        self.add(tg.mail(2, 'Ann Bell <ann@client.com>', 'sam@acme.com'), tg.mail(1, 'Sam <sam@acme.com>', 'ann@client.com', ('SENT',)))
        self.build()

    def picture(self, **args):
        out = self.app.action('graph_picture', args, owner_dashboard=True)
        self.build()
        return out

    def test_the_owner_uploads_and_removes_a_persons_picture(self):
        self.app.graph_build = self.build
        import base64
        done = self.picture(node_id='email:ann@client.com', data='data:image/png;base64,' + base64.b64encode(PNG).decode())
        self.assertRegex(done['picture'], r'^api/person-photo\?p=[0-9a-f]{32}$')
        self.assertEqual(self.node('email:ann@client.com')['profile']['photo'], done['picture'])
        self.picture(node_id='email:ann@client.com', remove=True)
        self.assertNotIn('photo', self.node('email:ann@client.com').get('profile') or {})

    def test_an_organizations_logo_and_only_images(self):
        self.app.graph_build = self.build
        import base64
        done = self.picture(node_id='org:client.com', data=base64.b64encode(PNG).decode())
        self.assertEqual(self.node('org:client.com')['profile']['logo'], done['picture'])
        with self.assertRaises(ValueError):
            self.picture(node_id='org:client.com', data=base64.b64encode(b'<svg onload=alert(1)>').decode())
        with self.assertRaises(ValueError):
            self.app.action('graph_picture', {'node_id': 'org:client.com', 'data': 'x'}, owner_dashboard=False)


class AlsoOnSlack(unittest.TestCase):
    add = tg.Graph.add
    build = tg.Graph.build

    def setUp(self):
        tg.Graph.setUp(self)
        self.add({'account_id': 'slack', 'source_id': 'sx1', 'kind': 'slack.message', 'occurred_at': tg.at(1), 'title': 'DM', 'body': 'hi', 'deleted': False,
                  'metadata': {'conversation_type': 'dm', 'channel_name': 'DM U0ANN', 'user_id': 'U0ANN', 'channel_id': 'D1'}})
        self.build()

    def test_their_slack_profile_in_the_workspace(self):
        self.app.config = {**tg.CONFIG, 'accounts': [*tg.CONFIG['accounts'][:2], {**tg.CONFIG['accounts'][2], 'slack_host': 'acme.slack.com'}]}
        self.assertEqual(self.app.slack_links({'id': 'slack:U0ANN', 'recent': []}), [{'url': 'https://acme.slack.com/team/U0ANN', 'label': 'Slack'}])

    def test_else_the_newest_thread_and_never_another_link(self):
        recent = [{'kind': 'slack.message', 'source_url': 'javascript:alert(1)'}, {'kind': 'slack.message', 'source_url': 'https://acme.slack.com/archives/D1/p1'}]
        self.assertEqual(self.app.slack_links({'id': 'slack:U0ANN', 'recent': recent}), [{'url': 'https://acme.slack.com/archives/D1/p1', 'label': 'Slack thread'}])
        self.assertEqual(self.app.slack_links({'id': 'slack:U0ANN', 'recent': recent[:1]}), [])


if __name__ == '__main__':
    unittest.main()
