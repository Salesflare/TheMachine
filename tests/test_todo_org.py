"""A to-do's organization (2026-11-10): a Personal to-do from the owner's partner about painting the house showed the
partner's employer, only because they work there. A to-do now shows an organization only when it is about it: the
review names it on suggest (org), or its project is with one the owner or a review set. Never one that only comes from
where someone on it works: their employer, or a project organization the Machine filled in from its people."""
import unittest

import enrichment
import todo_org

import test_graph as tg
from test_graph import NOW, graph, mail

T = NOW.isoformat()


class TodoOrg(unittest.TestCase):
    setUp, add, build = tg.Graph.setUp, tg.Graph.add, tg.Graph.build

    def project(self, name, *mails):
        self.add(*mails)
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute('SELECT id FROM events ORDER BY id DESC LIMIT ?', (len(mails),))]
            graph.label(db, ids, name, 'review', T)
            return db.execute('SELECT id FROM projects WHERE name=?', (name,)).fetchone()[0]

    def card(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            self.store.card_views(db, [row], jobs=False)
        return row

    def event(self, address):
        with self.store.connect() as db:
            return db.execute("SELECT id FROM events WHERE json_extract(metadata,'$.from') LIKE ? ORDER BY id DESC", (f'%<{address}>',)).fetchone()[0]

    def test_a_todo_shows_the_organization_the_review_named_never_the_one_its_person_works_at(self):
        self.add(mail(4, 'Pat <pat@bigcorp.example>', 'sam@acme.com', thread='p'), mail(3, 'Lee <lee@brushworks.example>', 'sam@acme.com', thread='q'))
        self.build()
        home, quote = self.event('pat@bigcorp.example'), self.event('lee@brushworks.example')
        plain = self.store.suggest('k1', 'Wait for the painter’s new date', 'The painter can’t come on Wednesday.', [home], org='')['id']
        older = self.store.suggest('k2', 'Ask about the hallway', 'Pat asks about the hallway.', [home], separate=True)['id']
        named = self.store.suggest('k3', 'Accept the painting quote', 'Brushworks sent the quote.', [quote], org='brushworks.example')['id']
        by_name = self.store.suggest('k4', 'Pay the painting deposit', 'Brushworks asks for the deposit.', [quote], org='Brushworks', separate=True)['id']
        unknown = self.store.suggest('k5', 'Book the scaffolding', 'Lee asks to book it.', [quote], org='nowhere.example', separate=True)['id']
        card = self.card(plain)
        self.assertEqual(card['people'][0]['org']['id'], 'org:bigcorp.example')  # who Pat is stays on their chip's page
        self.assertNotIn('org_node', card)
        self.assertTrue(card['org_said'])
        self.assertFalse(self.card(older)['org_said'])  # no review word (an older to-do): the dashboard decides by its area
        self.assertEqual(self.card(named)['org_node'], {'id': 'org:brushworks.example', 'name': self.card(named)['org_node']['name']})
        self.assertEqual(self.card(by_name)['org_node']['id'], 'org:brushworks.example')
        self.assertNotIn('org_node', self.card(unknown))
        # A later review's word replaces it: about none now
        self.store.suggest('k3b', 'Accept the painting quote', 'Brushworks sent the quote; Pat agrees.', [quote, home], card_id=named, match=True, org='')
        self.assertNotIn('org_node', self.card(named))

    def test_a_todos_chips_carry_the_photo_and_logo_the_graph_shows(self):
        """Who and which organization a to-do is about show their picture on its chips: only a photo saved on this
        Machine, a logo also as the https link the Graph shows; nothing when the Graph shows none or the owner took it off."""
        self.add(mail(4, 'Pat <pat@bigcorp.example>', 'sam@acme.com', thread='p'), mail(3, 'Lee <lee@brushworks.example>', 'sam@acme.com', thread='q'))
        with self.store.connect() as db:
            db.execute('INSERT INTO person_photos(identifier,key,type,data,saved_at) VALUES(?,?,?,?,?)',
                       ('email:lee@brushworks.example', 'a' * 32, 'image/png', b'\x89PNG\r\n\x1a\n', T))
            db.execute('INSERT INTO person_photos(identifier,key,type,data,saved_at) VALUES(?,?,?,?,?)',
                       ('logo:brushworks.example', 'b' * 32, 'image/png', b'\x89PNG\r\n\x1a\n', T))
        self.build()
        home, quote = self.event('pat@bigcorp.example'), self.event('lee@brushworks.example')
        card = self.card(self.store.suggest('k1', 'Accept the painting quote', 'Brushworks sent the quote.', [quote], org='brushworks.example')['id'])
        self.assertEqual(card['people'][0]['photo'], 'api/person-photo?p=' + 'a' * 32)
        self.assertEqual(card['people'][0]['org']['logo'], 'api/person-photo?p=' + 'b' * 32)
        self.assertEqual(card['org_node']['logo'], 'api/person-photo?p=' + 'b' * 32)
        plain = self.card(self.store.suggest('k2', 'Wait for the painter', 'Pat writes.', [home], org='')['id'])
        self.assertNotIn('photo', plain['people'][0])  # none saved: the chip keeps its icon
        self.assertNotIn('logo', plain['people'][0]['org'])
        with self.store.connect() as db:
            self.assertIsNone(enrichment.node_picture('{"profile":{"photo":"https://media.example/p.jpg"}}', 'photo'))  # never the service's link
            self.assertEqual(enrichment.node_picture('{"profile":{"logo":"https://logo.example/a.png"}}', 'logo'), 'https://logo.example/a.png')
            self.assertIsNone(enrichment.node_picture('{"profile":{"logo":"javascript:alert(1)"}}', 'logo'))
            self.assertIsNone(enrichment.node_picture('not json', 'logo'))
            db.execute("INSERT INTO person_edits(identifier,fields,updated_at) VALUES('email:lee@brushworks.example','{\"photo\":\"none\"}',?)", (T,))
        self.build()
        card = self.card(self.store.suggest('k3', 'Pay the deposit', 'Lee asks for it.', [quote], org='brushworks.example', separate=True)['id'])
        self.assertNotIn('photo', card['people'][0])  # the owner took it off

    def test_the_review_passes_its_word_and_says_none_when_it_gives_none(self):
        self.add(mail(4, 'Pat <pat@bigcorp.example>', 'sam@acme.com', thread='p'), mail(3, 'Lee <lee@brushworks.example>', 'sam@acme.com', thread='q'))
        self.build()
        self.app.config = {**tg.CONFIG, 'prepare_ahead': False}
        home, quote = self.event('pat@bigcorp.example'), self.event('lee@brushworks.example')
        about = self.app.action('suggest', {'dedupe_key': 'r1', 'title': 'Accept the painting quote', 'body': 'Brushworks sent the quote.',
                                            'event_ids': [quote], 'org': 'org:brushworks.example', 'newer_checked': [home, quote]})['id']
        none = self.app.action('suggest', {'dedupe_key': 'r2', 'title': 'Wait for the painter’s new date', 'body': 'Pat says the painter moves.',
                                           'event_ids': [home], 'personal': True, 'newer_checked': [home, quote]})['id']
        self.assertEqual(self.card(about)['org_node']['id'], 'org:brushworks.example')
        card = self.card(none)
        self.assertEqual((card.get('org_node'), card['org_said']), (None, True))

    def test_a_todos_project_brings_its_organization_only_when_the_owner_or_a_review_set_it(self):
        pid = self.project('Hallway painting', mail(4, 'Lee <lee@brushworks.example>', 'sam@acme.com', thread='h'))
        self.build()
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT org,org_by FROM projects WHERE id=?', (pid,)).fetchone()[:], ('brushworks.example', 'backfill'))
            self.assertEqual(todo_org.project_org_view(db, graph.card_project_view(db, 'Hallway painting')), None)
            graph.save_project(db, {'node_id': f'project:{pid}', 'org': None}, T)
            graph.save_project(db, {'node_id': f'project:{pid}', 'org': 'org:brushworks.example'}, T)  # the owner's pick
            self.assertEqual(todo_org.project_org_view(db, graph.card_project_view(db, 'Hallway painting'))['id'], 'org:brushworks.example')


if __name__ == '__main__':
    unittest.main()
