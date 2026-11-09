"""graph_joins: which identities a name may join. A shared address (a list, a role inbox, one read under two people's
names) is no join key, and a name alone never joins a work contact with a personal chat: that is a "Same person?"
question, with the owner's Merge and Not the same kept through every rebuild."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('joins_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph = a.graph
import shared_graph  # noqa: E402

NOW = dt.datetime(2026, 11, 9, 12, tzinfo=dt.timezone.utc)
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.example'}, {'id': 'chat', 'service': 'whatsapp', 'email': 'Personal WhatsApp'},
                       {'id': 'slack', 'service': 'slack', 'email': 'sam@acme.example', 'user_id': 'U0OWNER'}]}
counter = iter(range(1, 10**6))


def at(days_ago):
    return (NOW - dt.timedelta(days=days_ago)).isoformat()


def mail(days_ago, sender, to, labels=('INBOX',), cc='', thread=None, account='work', **extra):
    n = next(counter)
    return {'account_id': account, 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': at(days_ago), 'title': f'Mail {n}', 'body': 'Hello',
            'deleted': False, 'metadata': {'from': sender, 'to': to, 'cc': cc, 'labels': list(labels), 'message-id': f'<{n}@x>',
                                           'thread_id': thread or f't{n}', **extra}}


def chat(days_ago, phone, name):
    n = next(counter)
    return {'account_id': 'chat', 'source_id': f'w{n}', 'kind': 'whatsapp.message', 'occurred_at': at(days_ago), 'title': name, 'body': 'Hi',
            'deleted': False, 'metadata': {'chat_id': phone + '@s.whatsapp.net', 'chat_name': name, 'from_me': False, 'from': name,
                                           'sender_id': phone + '@s.whatsapp.net'}}


def slack(days_ago, user):
    n = next(counter)
    return {'account_id': 'slack', 'source_id': f's{n}', 'kind': 'slack.message', 'occurred_at': at(days_ago), 'title': f'#DM {user}: hi', 'body': 'hi',
            'deleted': False, 'metadata': {'conversation_type': 'dm', 'channel_name': f'DM {user}', 'user_id': user, 'channel_id': 'D' + user}}


class Joins(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.config = CONFIG
        clock = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        clock.start()
        self.addCleanup(clock.stop)

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])

    def build(self):
        with self.store.connect() as db:
            db.isolation_level = None
            return graph.build(db, {**self.config, 'embeddings': {'model': 'test', 'dims': 4}}, NOW.isoformat())

    def people(self):
        """{node id: (name, its identifiers)} for every person in the graph."""
        with self.store.connect() as db:
            return {r['id']: (r['name'], sorted(json.loads(r['info'])['identifiers'])) for r in db.execute("SELECT id,name,info FROM graph_nodes WHERE kind='person'")}

    def asked(self):
        with self.store.connect() as db:
            return [(r['a'], r['b'], r['why']) for r in db.execute('SELECT a,b,why FROM graph_same ORDER BY a,b')]

    def say(self, one, other, same, source='owner'):
        with self.store.connect() as db:
            graph.merge(db, one, other, same, NOW.isoformat(), source)

    # Shared addresses don't join people

    def test_a_list_address_does_not_fuse_the_people_who_wrote_through_it(self):
        """The reviewer's case: a list rewrites From to "Name via Founders <list address>", and two members reply in
        their own conversations, once from their own address and once through the list."""
        self.add(mail(5, 'Sam <sam@acme.example>', 'founders@lists.example', ('SENT',), thread='tA'),
                 mail(4, 'Jane Doe <jane@one.example>', 'sam@acme.example', thread='tA'),
                 mail(3, 'Jane Doe via Founders <founders@lists.example>', 'sam@acme.example', thread='tA'),
                 mail(5, 'Sam <sam@acme.example>', 'founders@lists.example', ('SENT',), thread='tB'),
                 mail(2, 'Bob Lee <bob@two.example>', 'sam@acme.example', thread='tB'),
                 mail(1, 'Bob Lee via Founders <founders@lists.example>', 'sam@acme.example', thread='tB'))
        self.build()
        self.assertEqual(self.people(), {'email:jane@one.example': ('Jane Doe', ['email:jane@one.example']),
                                         'email:bob@two.example': ('Bob Lee', ['email:bob@two.example']),
                                         # nobody's own name is on the list: it goes by its address, and is no "Same person?"
                                         'email:founders@lists.example': ('founders@lists.example', ['email:founders@lists.example'])})
        self.assertEqual(self.asked(), [])

    def test_the_address_a_list_id_names_is_no_join_key_under_one_name_either(self):
        self.add(mail(4, 'Sam <sam@acme.example>', 'crew@groups.example', ('SENT',), thread='tA'),
                 mail(3, 'Jane Doe <jane@one.example>', 'sam@acme.example', thread='tA'),
                 mail(2, 'Jane Doe via Crew <crew@groups.example>', 'sam@acme.example', thread='tA', list_id='Crew <crew.groups.example>'))
        self.build()
        self.assertEqual(set(self.people()), {'email:jane@one.example', 'email:crew@groups.example'})
        self.assertEqual(self.asked(), [])

    def test_a_role_address_or_one_under_two_names_does_not_join_by_name_across_channels(self):
        self.add(mail(5, 'Jane Doe <desk@vendor.example>', 'sam@acme.example'), chat(4, '00000000011', 'Jane Doe'),
                 mail(3, 'Bob Lee <desk@vendor.example>', 'sam@acme.example'), chat(2, '00000000012', 'Bob Lee'),
                 mail(2, 'Jan Peeters <info@client.example>', 'sam@acme.example'), chat(1, '00000000021', 'Jan Peeters'))
        self.build()
        self.assertEqual({k: v[1] for k, v in self.people().items()}, {i: [i] for i in (
            'email:desk@vendor.example', 'wa:00000000011', 'wa:00000000012', 'email:info@client.example', 'wa:00000000021')})
        # A role inbox one person answers can still be asked about; a mailbox two people answer has no name to ask about.
        self.assertEqual(self.asked(), [('email:info@client.example', 'wa:00000000021', 'Same name')])

    def test_two_colleagues_on_one_mailbox_stay_two_in_a_conversation(self):
        self.add(mail(5, 'Jane Doe <desk@vendor.example>', 'sam@acme.example', thread='tA'),
                 mail(4, 'Jane Doe <jane@vendor.example>', 'sam@acme.example', thread='tA'),
                 mail(3, 'Bob Lee <desk@vendor.example>', 'sam@acme.example', thread='tA'),
                 mail(2, 'Bob Lee <bob@vendor.example>', 'sam@acme.example', thread='tA'))
        self.build()
        self.assertEqual({k: v[1] for k, v in self.people().items()}, {i: [i] for i in (
            'email:desk@vendor.example', 'email:jane@vendor.example', 'email:bob@vendor.example')})

    def test_an_address_under_one_name_still_joins_as_before(self):
        self.add(mail(4, 'Jane Doe <jane@one.example>', 'sam@acme.example', thread='tA'),  # one conversation, two addresses
                 mail(3, 'Jane Doe <jane.doe@home.example>', 'sam@acme.example', thread='tA'),
                 mail(2, 'Kim Park <kim@two.example>', 'sam@acme.example', cc='Kim Park <kim@park.example>'),  # one message
                 mail(1, 'Ann Bell <a.bell@three.example>', 'sam@acme.example', thread='tC'),  # a mailbox one person answers
                 mail(1, 'Ann Bell <ann@three.example>', 'sam@acme.example', thread='tC'))
        self.build()
        self.assertEqual({k: v[1] for k, v in self.people().items()}, {
            'email:jane.doe@home.example': ['email:jane.doe@home.example', 'email:jane@one.example'],
            'email:kim@park.example': ['email:kim@park.example', 'email:kim@two.example'],
            'email:a.bell@three.example': ['email:a.bell@three.example', 'email:ann@three.example']})

    # A name alone doesn't merge a work contact with a personal chat

    def test_a_work_contact_and_a_personal_chat_with_one_name_are_a_question(self):
        """The reviewer's case: a client by mail and a friend on WhatsApp carry the same full name."""
        self.add(mail(2, 'Jan Peeters <jan@client.example>', 'sam@acme.example'),
                 mail(1, 'Sam <sam@acme.example>', 'jan@client.example', ('SENT',)), chat(1, '00000000021', 'Jan Peeters'))
        self.build()
        self.assertEqual({k: v[1] for k, v in self.people().items()}, {'email:jan@client.example': ['email:jan@client.example'], 'wa:00000000021': ['wa:00000000021']})
        self.assertEqual(self.asked(), [('email:jan@client.example', 'wa:00000000021', 'Same name')])
        with self.store.connect() as db:
            pair, = graph.same_people(db)  # People: both names, and where each one is from
            self.assertEqual([(p['name'], p['ids']) for p in (pair['a'], pair['b'])], [('Jan Peeters', ['jan@client.example']), ('Jan Peeters', ['+00000000021'])])
            page = graph.detail(db, 'email:jan@client.example')  # their page: the other one's name and where they are from
            self.assertEqual(page['same'], [{'id': 'wa:00000000021', 'why': 'Same name', 'from': '+00000000021', 'name': 'Jan Peeters'}])
            self.assertEqual(graph.detail(db, 'wa:00000000021')['same'][0]['from'], 'jan@client.example')

    # ... unless something besides the name agrees

    JAN = {'email:jan@client.example': ['email:jan@client.example', 'wa:32470000021']}

    def jan(self, *more):
        """A client by mail and a chat under the same full name, and whatever else is known."""
        self.add(mail(2, 'Jan Peeters <jan@client.example>', 'sam@acme.example'), chat(1, '32470000021', 'Jan Peeters'), *more)

    def one(self, expected=None):
        for _ in range(2):
            self.build()
            self.assertEqual({k: v[1] for k, v in self.people().items()}, expected or self.JAN)
            self.assertEqual(self.asked(), [])
        with self.store.connect() as db:
            return [j['by'] for j in graph.detail(db, next(iter(expected or self.JAN)))['joined']]

    def test_the_chat_number_a_connector_read_for_the_work_contact_keeps_them_one(self):
        self.jan()
        with self.store.connect() as db:
            db.execute("INSERT INTO person_facts(identifier,field,value,rank,source,seen_at) VALUES('email:jan@client.example','phone','+32 470 00 00 21',2,'google',?)", (NOW.isoformat(),))
        self.assertEqual(self.one(), ['name'])

    def test_the_chat_number_the_owner_put_on_the_work_contact_keeps_them_one(self):
        self.jan()
        with self.store.connect() as db:  # written the national way: the same number
            db.execute("INSERT INTO person_edits(identifier,fields,updated_at) VALUES('email:jan@client.example',?,?)", (json.dumps({'phones': {'added': ['0470 00 00 21']}}), NOW.isoformat()))
        self.one()

    def test_another_number_on_the_work_contact_is_no_evidence(self):
        self.jan()
        with self.store.connect() as db:
            db.execute("INSERT INTO person_facts(identifier,field,value,rank,source,seen_at) VALUES('email:jan@client.example','phone','+32 470 99 99 99',2,'google',?)", (NOW.isoformat(),))
        self.build()
        self.assertEqual(self.asked(), [('email:jan@client.example', 'wa:32470000021', 'Same name')])

    def test_a_shared_project_keeps_them_one(self):
        self.jan()
        with self.store.connect() as db:
            db.execute("INSERT INTO projects(id,name,created_at) VALUES(7,'Rollout',?)", (NOW.isoformat(),))
            for event_id, in db.execute('SELECT id FROM events').fetchall():  # the mail and the chat are on one project
                db.execute("INSERT INTO event_projects(event_id,project_id,source,created_at) VALUES(?,7,'review',?)", (event_id, NOW.isoformat()))
        self.one()

    def test_a_project_on_one_side_only_is_no_evidence(self):
        self.jan()
        with self.store.connect() as db:
            db.execute("INSERT INTO projects(id,name,created_at) VALUES(7,'Rollout',?)", (NOW.isoformat(),))
            db.execute("INSERT INTO event_projects(event_id,project_id,source,created_at) SELECT id,7,'review',? FROM events WHERE kind='gmail.message'", (NOW.isoformat(),))
        self.build()
        self.assertEqual(self.asked(), [('email:jan@client.example', 'wa:32470000021', 'Same name')])

    def test_the_same_organization_keeps_them_one(self):
        self.jan()
        with self.store.connect() as db:  # the chat said where they work: the company the address is at
            db.execute("INSERT INTO person_orgs(identifier,org,org_id,source,created_at) VALUES('wa:32470000021','Client','org:client.example','owner',?)", (NOW.isoformat(),))
        self.one()

    def test_another_organization_is_no_evidence(self):
        self.jan()
        with self.store.connect() as db:
            db.execute("INSERT INTO person_orgs(identifier,org,org_id,source,created_at) VALUES('wa:32470000021','Elsewhere',NULL,'owner',?)", (NOW.isoformat(),))
        self.build()
        self.assertEqual(self.asked(), [('email:jan@client.example', 'wa:32470000021', 'Same name')])

    def test_a_signal_with_both_on_it_keeps_them_one(self):
        """No connector puts an address and a chat number on one signal today, so this is asked of the rule itself."""
        with self.store.connect() as db:
            keys = graph.graph_joins.Keys(self.config, graph.Owner(self.config, db), graph.plain_name, graph.account_side, graph.FREEMAIL)
            keys.see(1, 'work', 'gmail.message', {}, [('email:jan@client.example', 'Jan Peeters', 1, 'them')], 't1', True)
            keys.see(2, 'chat', 'whatsapp.message', {}, [('wa:32470000021', 'Jan Peeters', 1, 'them')], 'wa:1', False)
            self.assertFalse(keys.agree(db, {'email:jan@client.example'}, {'wa:32470000021'}))
            keys.see(3, 'work', 'calendar.event', {}, [('email:jan@client.example', 'Jan Peeters', 1, 'met'), ('wa:32470000021', 'Jan Peeters', 1, 'met')], None, False)
            self.assertTrue(keys.agree(db, {'email:jan@client.example'}, {'wa:32470000021'}))

    def test_a_colleague_with_only_the_name_stays_one(self):
        self.add(mail(2, 'Kim Colleague <kim@acme.example>', 'sam@acme.example'), chat(1, '32470000041', 'Kim Colleague'))
        self.one({'email:kim@acme.example': ['email:kim@acme.example', 'wa:32470000041']})

    def test_an_outside_contact_with_only_the_name_is_asked(self):
        self.jan()
        self.build()
        self.assertEqual({k: v[1] for k, v in self.people().items()}, {'email:jan@client.example': ['email:jan@client.example'], 'wa:32470000021': ['wa:32470000021']})
        self.assertEqual(self.asked(), [('email:jan@client.example', 'wa:32470000021', 'Same name')])

    def test_not_the_same_is_never_rejoined_by_evidence(self):
        self.jan()
        self.build()
        self.say('wa:32470000021', 'email:jan@client.example', False)
        with self.store.connect() as db:
            db.execute("INSERT INTO person_facts(identifier,field,value,rank,source,seen_at) VALUES('email:jan@client.example','phone','+32 470 00 00 21',2,'google',?)", (NOW.isoformat(),))
            db.execute("INSERT INTO person_orgs(identifier,org,org_id,source,created_at) VALUES('wa:32470000021','Client','org:client.example','owner',?)", (NOW.isoformat(),))
        for _ in range(2):
            self.build()
            self.assertEqual(set(self.people()), {'email:jan@client.example', 'wa:32470000021'})
            self.assertEqual(self.asked(), [])

    def test_evidence_that_goes_away_asks_and_never_undoes_a_merge(self):
        self.jan()
        with self.store.connect() as db:
            db.execute("INSERT INTO person_facts(identifier,field,value,rank,source,seen_at) VALUES('email:jan@client.example','phone','+32 470 00 00 21',2,'google',?)", (NOW.isoformat(),))
        self.one()
        with self.store.connect() as db:
            db.execute('DELETE FROM person_facts')
        self.build()  # the number is gone: two people and a question, not a silent split
        self.assertEqual(self.asked(), [('email:jan@client.example', 'wa:32470000021', 'Same name')])
        self.say('wa:32470000021', 'email:jan@client.example', True, 'agent')  # the agent's merge counts as the owner's
        self.one()

    def test_merge_by_the_owner_survives_rebuilds_and_is_not_asked_again(self):
        self.add(mail(2, 'Jan Peeters <jan@client.example>', 'sam@acme.example'), chat(1, '00000000021', 'Jan Peeters'))
        self.build()
        self.say('wa:00000000021', 'email:jan@client.example', True)
        for _ in range(2):
            self.build()
            self.assertEqual({k: v[1] for k, v in self.people().items()}, {'email:jan@client.example': ['email:jan@client.example', 'wa:00000000021']})
            self.assertEqual(self.asked(), [])
        self.add(mail(0, 'Jan Peeters <jan@client.example>', 'sam@acme.example'), chat(0, '00000000021', 'Jan Peeters'))
        self.build()  # new signals: still one
        self.assertEqual(list(self.people()), ['email:jan@client.example'])

    def test_not_the_same_is_remembered_and_not_asked_again(self):
        self.add(mail(2, 'Jan Peeters <jan@client.example>', 'sam@acme.example'), chat(1, '00000000021', 'Jan Peeters'))
        self.build()
        self.say('wa:00000000021', 'email:jan@client.example', False)
        self.assertEqual(self.asked(), [])  # gone at once
        for _ in range(2):
            self.add(chat(0, '00000000021', 'Jan Peeters'))
            self.build()
            self.assertEqual(set(self.people()), {'email:jan@client.example', 'wa:00000000021'})
            self.assertEqual(self.asked(), [])
            with self.store.connect() as db:
                self.assertEqual(graph.detail(db, 'email:jan@client.example')['same'], [])

    def test_the_same_name_in_two_work_accounts_joins_as_before(self):
        self.add(mail(2, 'Ann Example <ann@client.example>', 'sam@acme.example'), slack(1, 'U0ANN'))
        self.store.remember_name('slack:U0ANN', 'Ann Example', None)  # no address from Slack: only the name says so
        self.build()
        self.assertEqual({k: v[1] for k, v in self.people().items()}, {'email:ann@client.example': ['email:ann@client.example', 'slack:U0ANN']})
        with self.store.connect() as db:
            self.assertEqual([j['by'] for j in graph.detail(db, 'email:ann@client.example')['joined']], ['name'])

    def test_an_account_placed_by_the_owner_decides_the_side(self):
        self.add(mail(2, 'Jan Peeters <jan@client.example>', 'sam@acme.example'), chat(1, '00000000021', 'Jan Peeters'),
                 mail(2, 'Bo Friend <bo@gmail.com>', 'sam@home.example', account='home'), chat(1, '00000000031', 'Bo Friend'))
        # WhatsApp connected for work: both are work contacts. A private mailbox and that WhatsApp are two sides again.
        self.config = {'accounts': [{'id': 'work', 'email': 'sam@acme.example', 'boundary': 'work:acme'},
                                    {'id': 'chat', 'service': 'whatsapp', 'email': 'Work WhatsApp', 'scope': 'work'},
                                    {'id': 'home', 'email': 'sam@home.example', 'boundary': 'personal:home'}]}
        self.build()
        self.assertEqual({k: v[1] for k, v in self.people().items()}, {
            'email:jan@client.example': ['email:jan@client.example', 'wa:00000000021'], 'email:bo@gmail.com': ['email:bo@gmail.com'], 'wa:00000000031': ['wa:00000000031']})
        self.config = {'accounts': [dict(x, scope='personal') if x['id'] == 'chat' else x for x in self.config['accounts']]}
        self.build()  # a personal WhatsApp: the friend is one person on the personal side, the client a question
        self.assertEqual({k: v[1] for k, v in self.people().items()}, {
            'email:jan@client.example': ['email:jan@client.example'], 'wa:00000000021': ['wa:00000000021'], 'email:bo@gmail.com': ['email:bo@gmail.com', 'wa:00000000031']})
        self.assertEqual(self.asked(), [('email:jan@client.example', 'wa:00000000021', 'Same name')])

    # People an older build fused

    def test_what_the_owner_joined_by_hand_stays_joined_and_what_they_kept_stays_with_them(self):
        """An install from before this rule: a list address fused with a member, a client fused with a friend's chat.
        The owner merged the list address into Jane by hand, wrote a note on the client and keeps them private."""
        self.add(mail(4, 'Jane Doe <jane@one.example>', 'sam@acme.example', thread='tA'),
                 mail(3, 'Jane Doe via Founders <founders@lists.example>', 'sam@acme.example', thread='tA'),
                 mail(2, 'Bob Lee via Founders <founders@lists.example>', 'sam@acme.example', thread='tB'),
                 mail(2, 'Jan Peeters <jan@client.example>', 'sam@acme.example'), chat(1, '00000000021', 'Jan Peeters'))
        self.build()
        with self.store.connect() as db:  # as the older build left it: one person of the client and the chat, kept private
            fused = json.dumps({'identifiers': ['email:jan@client.example', 'wa:00000000021'], 'ids': ['+00000000021', 'jan@client.example']})
            db.execute("UPDATE graph_nodes SET info=? WHERE id='email:jan@client.example'", (fused,))
            db.execute("DELETE FROM graph_nodes WHERE id='wa:00000000021'")
            shared_graph.ensure(db)
            shared_graph.keep_private(db, 'email:jan@client.example')
            db.execute("INSERT INTO person_edits(identifier,fields,updated_at) VALUES('email:jan@client.example',?,?)", (json.dumps({'notes': 'Met at the fair'}), NOW.isoformat()))
        self.say('email:founders@lists.example', 'email:jane@one.example', True)
        for _ in range(2):
            self.build()
            people = self.people()
            self.assertEqual(sorted(v[1] for v in people.values()), [
                ['email:founders@lists.example', 'email:jane@one.example'],  # the owner's merge stands, list address or not
                ['email:jan@client.example'], ['wa:00000000021']])  # told apart by itself
            with self.store.connect() as db:
                self.assertEqual(json.loads(db.execute("SELECT fields FROM person_edits WHERE identifier='email:jan@client.example'").fetchone()[0]), {'notes': 'Met at the fair'})
                self.assertEqual({r[0] for r in db.execute('SELECT node_id FROM share_private')}, {'email:jan@client.example', 'wa:00000000021'})
                self.assertEqual([tuple(r) for r in db.execute('SELECT a,b,same,source FROM graph_merges')],
                                 [('email:founders@lists.example', 'email:jane@one.example', 1, 'owner')])
        self.assertEqual(self.asked(), [('email:jan@client.example', 'wa:00000000021', 'Same name')])
        self.say('email:jan@client.example', 'wa:00000000021', True)  # they were one after all: one Merge brings it all back
        self.build()
        with self.store.connect() as db:
            self.assertEqual(self.people()['email:jan@client.example'][1], ['email:jan@client.example', 'wa:00000000021'])
            self.assertTrue(db.execute("SELECT 1 FROM share_private WHERE node_id='email:jan@client.example'").fetchone())
            self.assertEqual(graph.detail(db, 'email:jan@client.example')['notes'], 'Met at the fair')


if __name__ == '__main__':
    unittest.main()
