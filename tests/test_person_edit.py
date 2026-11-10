"""Editing a person: the owner's details win over a look-up and the messages, and stay through rebuilds, merges and Undo."""
import json
import threading
import time
import unittest

import test_graph as tg

a, graph = tg.a, tg.graph


class PersonEdit(unittest.TestCase):
    add = tg.Graph.add
    build = tg.Graph.build
    node = tg.Graph.node

    def setUp(self):
        tg.Graph.setUp(self)

    def edit(self, node, **fields):
        return self.app.action('graph_person_edit', {'node_id': node, 'fields': fields}, owner_dashboard=True)

    def look_up(self, identifier, **profile):
        with self.store.connect() as db:
            db.execute("INSERT OR REPLACE INTO person_profiles(identifier,status,profile,fetched_at) VALUES(?,'found',?,?)",
                       (identifier, json.dumps(profile), tg.NOW.isoformat()))

    def test_the_owners_details_win_over_the_look_up_and_stay_after_a_new_one(self):
        self.add(tg.mail(3, 'Ivy Park <ivy@globex.example>', 'sam@acme.com'), tg.mail(2, 'Sam <sam@acme.com>', 'Ivy Park <ivy@globex.example>', ('SENT',)))
        self.look_up('email:ivy@globex.example', title='Sales', city='Springfield', country='US', linkedin_url='https://www.linkedin.com/in/ivy-old')
        self.build()
        node = 'email:ivy@globex.example'
        self.assertEqual(self.node(node)['side'], 'work')  # a work address: Work, until the owner says otherwise
        done = self.edit(node, name='Ivy P. Park', title='Head of Sales', location='Ghent, Belgium', linkedin_url='linkedin.com/in/ivy-park',
                         role='partner', org='Globex Holdings', side='personal', phones=['+32 470 00 00 51'], emails=['ivy@globex.example', 'ivy.park@mail.example'])
        self.assertEqual(done['edited'], ['emails', 'linkedin_url', 'location', 'phones', 'side', 'title'])
        view = self.node(node)
        self.assertEqual((view['name'], view['role'], view['role_by'], view['side'], view['side_by']), ('Ivy P. Park', 'partner', 'owner', 'personal', 'owner'))
        self.assertEqual((view['profile']['title'], view['profile']['location'], view['profile']['linkedin_url']),
                         ('Head of Sales', 'Ghent, Belgium', 'https://linkedin.com/in/ivy-park'))
        self.assertEqual(view['org_by'], 'owner')
        self.assertEqual(view['phones'], [{'value': '+32 470 00 00 51', 'by': 'owner'}])
        self.assertEqual(view['emails'], [{'value': 'ivy@globex.example', 'by': 'messages'}, {'value': 'ivy.park@mail.example', 'by': 'owner'}])
        # A new look-up and later automatic updates don't overwrite what the owner set.
        self.look_up('email:ivy@globex.example', title='VP Sales', city='Paris', country='FR')
        self.app.graph_action({'node_id': node, 'org': 'Initech', 'quote': 'Ivy at Initech'})  # a review: the owner's word stays
        self.app.graph_action({'node_id': node, 'role': 'supplier'})
        self.build()
        view = self.node(node)
        self.assertEqual((view['profile']['title'], view['profile']['location'], view['role']), ('Head of Sales', 'Ghent, Belgium', 'partner'))
        # An empty field gives that one back to the look-up; the rest stays.
        self.edit(node, title='')
        view = self.node(node)
        self.assertEqual((view['profile']['title'], view['profile']['location']), ('VP Sales', 'Ghent, Belgium'))

    def test_a_save_answers_at_once_and_its_page_shows_it_before_the_graph_is_built(self):
        # A whole build before the answer held a Save some 16 s on a big Graph: the build is stubbed slow here, and
        # the Save answers without it, its page already showing what was saved; the graph worker builds the rest.
        self.add(tg.mail(3, 'Ivy Park <ivy@globex.example>', 'sam@acme.com'), tg.mail(2, 'Sam <sam@acme.com>', 'Ivy Park <ivy@globex.example>', ('SENT',)),
                 tg.mail(1, 'Rex Moon <rex@initech.example>', 'sam@acme.com'))
        self.look_up('email:ivy@globex.example', title='Sales', city='Springfield', country='US')
        self.build()
        node, built = 'email:ivy@globex.example', []
        real_build = self.app.graph_build
        self.app.graph_worker_on, self.app.graph_dirty = True, threading.Event()
        self.app.graph_build = lambda *a, **k: built.append(time.sleep(2))
        start = time.monotonic()
        self.edit(node, name='Ivy P. Park', title='Head of Sales', location='Ghent, Belgium', notes='Met at the fair', side='personal',
                  phones=['+32 470 00 00 51'], role='partner', org='Initech')
        self.assertLess(time.monotonic() - start, 0.3)
        self.assertEqual(built, [])
        self.assertTrue(self.app.graph_dirty.is_set())  # the worker builds the rest of the Graph
        keys = ('name', 'role', 'side', 'side_by', 'notes', 'phones', 'org', 'org_by')
        now_shown = {k: self.node(node).get(k) for k in keys}
        self.assertEqual(now_shown, {'name': 'Ivy P. Park', 'role': 'partner', 'side': 'personal', 'side_by': 'owner', 'notes': 'Met at the fair',
                                     'phones': [{'value': '+32 470 00 00 51', 'by': 'owner'}], 'org': 'org:initech.example', 'org_by': 'owner'})
        self.assertEqual((self.node(node)['profile']['title'], self.node(node)['profile']['location']), ('Head of Sales', 'Ghent, Belgium'))
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT b FROM graph_links WHERE a=? AND kind='member'", (node,)).fetchall()[0][0], 'org:initech.example')
        # An emptied field is the look-up's again at once; a new organization's name shows until the build makes it
        self.edit(node, title='', org='Brand New Co')
        self.assertEqual((self.node(node)['profile']['title'], self.node(node)['org']), ('Sales', 'org:named:brand-new-co'))
        self.assertEqual(self.app.graph_action({'node_id': node})['org_name'], 'Brand New Co')
        # The build that follows writes the same
        self.app.graph_build = real_build
        self.build()
        self.assertEqual((self.node(node)['name'], self.node(node)['profile']['title'], self.node(node)['org'], self.node(node)['notes']),
                         ('Ivy P. Park', 'Sales', 'org:named:brand-new-co', 'Met at the fair'))

    def test_an_address_the_owner_took_off_stays_off_and_a_new_one_still_shows(self):
        self.add(tg.mail(3, 'Ode Lin <ode@one.example>', 'sam@acme.com', cc='Ode Lin <ode.lin@two.example>'))
        self.build()
        node = next(iter(self.people()))
        self.assertEqual({e['value'] for e in self.node(node)['emails']}, {'ode@one.example', 'ode.lin@two.example'})
        self.edit(node, emails=['ode@one.example'])
        self.assertEqual([e['value'] for e in self.node(node)['emails']], ['ode@one.example'])
        self.add(tg.mail(1, 'Ode Lin <ode@one.example>', 'sam@acme.com', cc='Ode Lin <ode@three.example>'))
        self.build()
        self.assertEqual({e['value'] for e in self.node(node)['emails']}, {'ode@one.example', 'ode@three.example'})

    def test_a_number_a_connector_read_shows_and_can_be_taken_off(self):
        self.add(tg.mail(3, 'Ivy Park <ivy@globex.example>', 'sam@acme.com'))
        self.build()
        with self.store.connect() as db:
            a.enrichment.fact_tables(db)
            db.execute("INSERT INTO person_facts VALUES('email:ivy@globex.example','phone','+32 470 00 00 52',2,'slack',?)", (tg.NOW.isoformat(),))
            db.execute("INSERT INTO person_facts VALUES('email:ivy@globex.example','title','Buyer',2,'slack',?)", (tg.NOW.isoformat(),))
        self.build()
        node = 'email:ivy@globex.example'
        self.assertEqual(self.node(node)['phones'], [{'value': '+32 470 00 00 52', 'by': 'Slack'}])
        self.edit(node, phones=[], title='Head of Buying')  # the owner's word beats their own Slack profile too
        view = self.node(node)
        self.assertEqual((view['phones'], view['profile']['title'], view['profile']['sources']['title']['from']), ([], 'Head of Buying', 'you'))

    def people(self):
        with self.store.connect() as db:
            return {r['id']: json.loads(r['info'])['identifiers'] for r in db.execute("SELECT id,info FROM graph_nodes WHERE kind='person'")}

    def test_edits_stay_through_a_merge_and_its_undo(self):
        self.add(tg.mail(3, 'Kit Lane <kit@globex.example>', 'sam@acme.com'), tg.mail(2, 'Kit <k.lane@globex.example>', 'sam@acme.com'))
        self.build()
        self.edit('email:kit@globex.example', title='Buyer', side='personal')
        self.edit('email:k.lane@globex.example', location='Leuven')
        merge = lambda same: self.app.action('graph_same', {'a': 'email:k.lane@globex.example', 'b': 'email:kit@globex.example', 'same': same}, owner_dashboard=True)
        merge(True)
        merged, = [n for n, ids in self.people().items() if len(ids) == 2]
        view = self.node(merged)
        self.assertEqual((view['profile']['title'], view['profile']['location'], view['side']), ('Buyer', 'Leuven', 'personal'))
        # A save on the merged page moves that field there, once.
        self.edit(merged, title='Lead buyer')
        self.assertEqual(self.node(merged)['profile']['title'], 'Lead buyer')
        merge(False)  # Undo: each identity keeps what was saved on it
        self.assertEqual(len(self.people()), 2)
        kept = {n: self.node(n) for n in self.people()}
        self.assertEqual({n: ((v['profile'] or {}).get('title'), (v['profile'] or {}).get('location')) for n, v in kept.items()},
                         {merged: ('Lead buyer', 'Leuven' if merged == 'email:k.lane@globex.example' else None),
                          **{n: (None, 'Leuven' if n == 'email:k.lane@globex.example' else None) for n in kept if n != merged}})

    def test_only_the_owner_edits_and_bad_values_say_why(self):
        self.add(tg.mail(3, 'Ivy Park <ivy@globex.example>', 'sam@acme.com'))
        self.build()
        with self.assertRaisesRegex(ValueError, 'Only the owner'):
            self.app.action('graph_person_edit', {'node_id': 'email:ivy@globex.example', 'fields': {'title': 'X'}})
        for fields, why in (({'emails': ['not an address']}, 'not an email'), ({'phones': ['call me']}, 'not a phone'),
                            ({'side': 'both'}, 'Work or Personal'), ({'linkedin_url': 'https://example.com/ivy'}, 'linkedin.com'),
                            ({'title': 'x' * 121}, 'up to 120')):
            with self.assertRaisesRegex(ValueError, why):
                self.edit('email:ivy@globex.example', **fields)
        self.assertIn('graph_person_edit', a.OWNER_ACTIONS)

    def test_delete_permanently_takes_the_edits_too(self):
        self.add(tg.mail(3, 'Ivy Park <ivy@globex.example>', 'sam@acme.com'))
        self.build()
        self.edit('email:ivy@globex.example', title='Head of Sales')
        self.app.delete_person('email:ivy@globex.example')
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM person_edits').fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()
