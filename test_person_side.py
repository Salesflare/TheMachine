"""A person's automatic side (Work or Personal) comes from what The Machine knows of them, never from a missing work
address: the account a conversation came from, the projects they're on and the sharing review's calls on their threads.
Thin or split evidence leaves it unknown. The owner's own choice and Family/Friends stay as they are."""
import json
import unittest

import shared_graph
import test_graph as tg
from test_graph import CONFIG, NOW, graph, linkedin, mail  # functions and constants only: no test classes here

ACCOUNTS = CONFIG['accounts'] + [{'id': 'li', 'service': 'linkedin'}]


class PersonSide(unittest.TestCase):
    add, node, ids = tg.Graph.add, tg.Graph.node, tg.Graph.ids

    def setUp(self):
        tg.Graph.setUp(self)
        self.accounts = [dict(x) for x in ACCOUNTS]

    def place(self, account_id, boundary=None, scope=None):
        for x in self.accounts:
            if x['id'] == account_id:
                x.update({k: v for k, v in (('boundary', boundary), ('scope', scope)) if v})

    def build(self):
        with self.store.connect() as db:
            db.isolation_level = None
            return graph.build(db, {'accounts': self.accounts, 'embeddings': {'enabled': False}}, NOW.isoformat())

    def prospect(self, conv='c-kai', name='Kai Moss'):
        first = linkedin(5, conv, name, 'Saw your post about the CRM, could we get a demo?')
        self.add(first, linkedin(4, conv, name, 'Sure, how about Thursday?', mine=True))
        return 'li:' + conv, self.ids([first['source_id']])[0]

    def side(self, node_id):
        view = self.node(node_id)
        return view['side'], view['side_by']

    def judge(self, *calls):
        with self.store.connect() as db:
            shared_graph.ensure(db)
            shared_graph.judge(db, [{'event_id': e, 'share': verdict, 'line': 'x'} for e, verdict in calls])

    def test_a_linkedin_contact_without_a_work_address_is_not_personal_for_that(self):
        node, _ = self.prospect()
        self.build()
        self.assertEqual(self.side(node), (None, None))  # nothing to go on: unknown, not a guess
        self.place('li', boundary='work:linkedin')
        self.build()
        self.assertEqual((self.node(node)['side'], self.info(node)['side_why']), ('work', 'account'))
        self.place('li', boundary='personal:me')
        self.build()
        self.assertEqual(self.side(node), ('personal', None))

    def test_an_accounts_own_scope_wins_over_its_boundary_like_on_cards(self):
        node, _ = self.prospect()
        self.place('li', boundary='work:Side', scope='personal')
        self.build()
        self.assertEqual(self.side(node), ('personal', None))

    def test_conversations_on_both_a_work_and_a_personal_account_leave_it_unknown(self):
        self.place('work', boundary='work:Acme')
        self.place('chat', boundary='personal:me')
        self.add(mail(5, 'Pia Lund <pia.lund@gmail.com>', 'sam@acme.com'), mail(4, 'Sam <sam@acme.com>', 'pia.lund@gmail.com', ('SENT',)),
                 {**mail(3, 'Pia Lund <pia.lund@gmail.com>', 'sam@acme.com'), 'account_id': 'chat'})
        self.build()
        self.assertEqual((self.side('email:pia.lund@gmail.com'), self.info('email:pia.lund@gmail.com')['side_why']), ((None, None), 'mixed'))

    def test_a_project_on_a_board_makes_them_work(self):
        node, event_id = self.prospect()
        self.place('li', boundary='personal:me')  # even when the account says otherwise: what they're about comes first
        with self.store.connect() as db:
            db.execute("INSERT INTO boards(id,name,stages,source,created_at) VALUES(1,'Demos and trials','[]','owner',?)", (NOW.isoformat(),))
            db.execute("INSERT INTO projects(id,name,created_at,board_id) VALUES(1,'Kai demo',?,1)", (NOW.isoformat(),))
            db.execute("INSERT INTO event_projects(event_id,project_id,source,created_at) VALUES(?,1,'review',?)", (event_id, NOW.isoformat()))
        self.build()
        self.assertEqual((self.side(node), self.info(node)['side_why']), (('work', None), 'project'))

    def test_a_person_the_owner_put_on_a_project_off_any_board_takes_the_side_its_messages_came_from(self):
        node, event_id = self.prospect()
        self.place('work', boundary='work:Acme')
        self.add(mail(6, 'Ann <ann@client.example>', 'sam@acme.com', thread='t-ann'))
        with self.store.connect() as db:
            db.execute("INSERT INTO projects(id,name,created_at) VALUES(1,'Renewal',?)", (NOW.isoformat(),))
            ann = self.ids([db.execute("SELECT source_id FROM events WHERE kind='gmail.message'").fetchone()[0]])[0]
            db.execute("INSERT INTO event_projects(event_id,project_id,source,created_at) VALUES(?,1,'review',?)", (ann, NOW.isoformat()))
            db.execute('INSERT INTO project_people(project_id,node_id,created_at) VALUES(1,?,?)', (node, NOW.isoformat()))
        self.build()
        self.assertEqual((self.side(node), self.info(node)['side_why']), (('work', None), 'project'))

    def test_the_reviews_calls_on_their_threads_decide_before_the_account(self):
        self.place('work', boundary='personal:me')
        client = mail(5, 'Rob Hale <rob.hale@gmail.com>', 'sam@acme.com', thread='t-rob')
        self.add(client)
        self.judge((self.ids([client['source_id']])[0], 'client'))
        self.build()
        self.assertEqual((self.side('email:rob.hale@gmail.com'), self.info('email:rob.hale@gmail.com')['side_why']), (('work', None), 'review'))
        home = mail(4, 'Rob Hale <rob.hale@gmail.com>', 'sam@acme.com', thread='t-rob-home')
        self.add(home)
        self.judge((self.ids([home['source_id']])[0], 'personal'))
        self.build()
        self.assertEqual(self.side('email:rob.hale@gmail.com'), (None, None))  # a client and a friend: unknown, not a guess

    def test_a_thread_the_review_found_personal_makes_them_personal_also_on_a_work_account(self):
        self.place('work', boundary='work:Acme')
        own = mail(5, 'Lia <lia.berg@gmail.com>', 'sam@acme.com', thread='t-lia')
        self.add(own)
        self.judge((self.ids([own['source_id']])[0], 'personal'))
        self.build()
        self.assertEqual(self.side('email:lia.berg@gmail.com'), ('personal', None))

    def test_a_work_address_stays_work_and_unsure_or_other_says_nothing(self):
        self.add(mail(5, 'Ann <ann@client.example>', 'sam@acme.com'))
        other = mail(4, 'Bo <bo.dale@gmail.com>', 'sam@acme.com')
        self.add(other)
        self.judge((self.ids([other['source_id']])[0], 'other'))
        self.build()
        self.assertEqual((self.side('email:ann@client.example'), self.info('email:ann@client.example')['side_why']), (('work', None), 'address'))
        self.assertEqual(self.side('email:bo.dale@gmail.com'), (None, None))

    def test_the_owners_own_choice_is_never_changed(self):
        node, _ = self.prospect()
        self.place('li', boundary='work:linkedin')
        self.build()
        with self.store.connect() as db:
            graph.person_edit(db, node, {'side': 'personal'}, NOW.isoformat())
        self.build()
        self.assertEqual(self.side(node), ('personal', 'owner'))
        with self.store.connect() as db:
            self.assertFalse(db.execute('SELECT 1 FROM side_changes WHERE node_id=?', (node,)).fetchone())

    def test_family_and_friends_stay_personal_and_the_owners_word_still_wins(self):
        node, _ = self.prospect()
        self.place('li', boundary='work:linkedin')
        self.build()
        marks = {node: {'machine': 'm1', 'in': [{'kind': 'family', 'fleet_name': 'Family'}], 'name': None}}
        with self.store.connect() as db:
            self.assertEqual(graph.with_fleet(db, {'kind': 'person', 'id': node, 'side': 'work', 'side_by': None}, marks)['side'], 'personal')
            self.assertEqual(graph.with_fleet(db, {'kind': 'person', 'id': node, 'side': None, 'side_by': None}, marks)['side'], 'personal')
            self.assertEqual(graph.with_fleet(db, {'kind': 'person', 'id': node, 'side': 'work', 'side_by': 'owner'}, marks)['side'], 'work')

    def test_the_first_build_under_the_new_rule_records_what_it_changed_once(self):
        node, _ = self.prospect()
        owned, _ = self.prospect('c-ola', 'Ola Bright')
        self.place('li', boundary='work:linkedin')
        with self.store.connect() as db:
            graph.ensure(db)
            # the graph as the old rule left it: no work address, so personal; one the owner marked personal themselves
            for node_id, info in ((node, {'side': 'personal', 'side_by': None}), (owned, {'side': 'personal', 'side_by': 'owner'})):
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,quiet,info) VALUES(?,'person','x',1,1,0,?)", (node_id, json.dumps(info)))
            db.execute('INSERT INTO person_edits(identifier,fields,updated_at) VALUES(?,?,?)', (owned, json.dumps({'side': 'personal'}), NOW.isoformat()))
        self.build()
        with self.store.connect() as db:
            rows = [tuple(r) for r in db.execute('SELECT node_id,rule,before,after,why FROM side_changes')]
            self.assertEqual(rows, [(node, graph.SIDE_RULE, 'personal', 'work', 'account')])
            self.assertEqual(db.execute('SELECT rule FROM side_rule').fetchone()[0], graph.SIDE_RULE)
        self.place('li', boundary='personal:me')
        self.build()  # later changes are the rule at work, not a migration: not recorded again
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM side_changes').fetchone()[0], 1)
        self.assertEqual(self.side(owned), ('personal', 'owner'))

    def test_sharing_only_follows_the_owners_own_side(self):
        """Scope keeps out people the owner marked Personal and Family/Friends; an automatic side, any value, changes nothing."""
        node, _ = self.prospect()
        self.place('li', boundary='personal:me')
        self.add(mail(5, 'Ann <ann@client.example>', 'sam@acme.com'))
        self.build()
        self.assertEqual(self.side(node), ('personal', None))
        with self.store.connect() as db:
            shared_graph.ensure(db)
            self.assertFalse(shared_graph.Scope(db, ['work', 'li'], {'acme.com'}, {'sam@acme.com'}).private)
            graph.person_edit(db, 'email:ann@client.example', {'side': 'personal'}, NOW.isoformat())
        self.build()
        with self.store.connect() as db:
            self.assertEqual(shared_graph.Scope(db, ['work', 'li'], {'acme.com'}, {'sam@acme.com'}).private, {'email:ann@client.example'})

    def test_a_person_added_by_hand_without_messages_has_no_side_yet(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO manual_nodes(identifier,kind,name,created_at) VALUES('manual:lou','person','Lou Marsh',?)", (NOW.isoformat(),))
        self.build()
        self.assertEqual(self.side('manual:lou'), (None, None))

    def info(self, node_id):
        with self.store.connect() as db:
            return json.loads(db.execute('SELECT info FROM graph_nodes WHERE id=?', (node_id,)).fetchone()[0])


if __name__ == '__main__':
    unittest.main()
