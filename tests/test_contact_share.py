"""Sharing a contact (contact_share.py): the owner picks the fields, sees exactly what goes, and sends it to one
teammate, friend or Family member; a Personal contact needs an extra confirm. On the other side it waits for Add (made,
or merged into the same person) or Dismiss, and the person is marked shared by the sender. A fake relay stands in for
the Network; nothing is sent anywhere."""
import unittest

import test_fleet as tf
import test_friends as tfr
from test_fleet import CONFIG, a

fleet, graph, contact_share = a.fleet, a.graph, a.fleet.contact_share
SAM = 'email:sam@client.example'


class ContactShare(unittest.TestCase):
    def setUp(self):
        tf.Fleet.setUp(self)
        self.relay = tfr.FriendsRelay()
        for group in self.relay.directory['fleets']:
            group['asks'] = list(fleet.ASKS[group['kind']])
        self.fleet = fleet.Fleet(self.store.connect, {**CONFIG, 'owner_name': 'Alex Owner'}, lambda: 'token', relay=self.relay)
        self.fleet.directory(refresh=True)
        self.builds = 0

        def build():
            self.builds += 1
            with self.store.connect() as db:
                db.isolation_level = None
                graph.build(db, CONFIG, tf.NOW.isoformat())
        self.fleet.graph_build = build
        self.work = self.fleet.ref('work')

    def edit_sam(self, **fields):
        with self.store.connect() as db:
            graph.person_edit(db, SAM, fields, tf.NOW.isoformat())
            db.isolation_level = None
            graph.build(db, CONFIG, tf.NOW.isoformat())

    def take(self, question, ask_id='c1', sender='pat1', group='work'):
        return self.fleet.take_ask({'id': ask_id, 'fleet': group if group == 'work' else tfr.FR, 'from': sender, 'kind': 'contact', 'question': question})

    def person(self, node_id):
        with self.store.connect() as db:
            row = graph.resolve(db, node_id)
            return graph.node_view(row) if row else None

    def test_only_the_fields_picked_go_and_only_as_previewed(self):
        self.edit_sam(phones=['+32 470 12 34 56'], title='Head of Sales')
        options = self.fleet.contact_options(SAM)
        self.assertEqual((options['name'], options['emails'], options['phones'], options['role']),
                         ('Sam Lee', ['sam@client.example'], ['+32 470 12 34 56'], 'Head of Sales'))
        self.assertEqual({(t['kind'], t['name']) for t in options['targets']}, {('work', 'Pat'), ('friends', 'Lou (@lou)')})
        pick = {'emails': ['sam@client.example'], 'role': True}
        shown = self.fleet.contact_preview(SAM, pick, 'You both run sales in Benelux', self.work, 'pat1')
        self.assertEqual(shown['card'], {'name': 'Sam Lee', 'emails': ['sam@client.example'], 'role': 'Head of Sales', 'note': 'You both run sales in Benelux'})
        self.assertEqual([r['label'] for r in shown['rows']], ['Name', 'Email', 'Role', 'Note'])
        # Send carries what was seen: a different pick is refused, nothing goes
        with self.assertRaisesRegex(ValueError, 'changed since the preview'):
            self.fleet.contact_send(SAM, {**pick, 'phones': ['+32 470 12 34 56']}, 'You both run sales in Benelux', self.work, 'pat1', shown['digest'])
        self.assertEqual(self.relay.sent('/ask'), [])
        out = self.fleet.contact_send(SAM, pick, 'You both run sales in Benelux', self.work, 'pat1', shown['digest'])
        self.assertEqual(out, {'sent': 1, 'to': 'Pat'})
        ask = self.relay.sent('/ask')[-1]
        self.assertEqual((ask['kind'], ask['to'], ask['question']), ('contact', ['pat1'], shown['card']))
        self.assertNotIn('phones', ask['question'])
        self.assertEqual(self.fleet.contact_sent(SAM)[0]['name'], 'Pat')

    def test_a_personal_contact_needs_the_extra_confirm(self):
        self.edit_sam(side='personal')
        shown = self.fleet.contact_preview(SAM, {}, '', self.work, 'pat1')
        self.assertEqual(shown['confirm'], 'personal')
        with self.assertRaisesRegex(ValueError, 'Personal contact. Confirm'):
            self.fleet.contact_send(SAM, {}, '', self.work, 'pat1', shown['digest'])
        self.assertEqual(self.relay.sent('/ask'), [])
        self.fleet.contact_send(SAM, {}, '', self.work, 'pat1', shown['digest'], confirmed=True)
        self.assertEqual(self.relay.sent('/ask')[-1]['question'], {'name': 'Sam Lee'})

    def test_only_to_one_person_where_the_network_carries_contacts(self):
        shown = self.fleet.contact_preview(SAM, {}, '', self.work, 'pat1')
        with self.assertRaisesRegex(ValueError, 'Pick a teammate'):
            self.fleet.contact_send(SAM, {}, '', self.work, 'stranger', shown['digest'])
        for group in self.relay.directory['fleets']:
            group['asks'] = [k for k in group['asks'] if k != 'contact']
        self.fleet.directory(refresh=True)
        self.assertEqual(self.fleet.contact_targets(), [])

    def test_own_card_from_about_you(self):
        options = self.fleet.contact_options('me')
        self.assertEqual((options['name'], options['own'], options['confirm']), ('Alex Owner', True, None))
        self.assertEqual(sorted(options['emails']), ['owner@acme.example', 'owner@gmail.com'])
        shown = self.fleet.contact_preview('me', {'emails': ['owner@gmail.com']}, '', tfr.FR, 'fp_lou')
        self.assertEqual(shown['card'], {'name': 'Alex Owner', 'emails': ['owner@gmail.com'], 'own': True})
        self.fleet.contact_send('me', {'emails': ['owner@gmail.com']}, '', tfr.FR, 'fp_lou', shown['digest'])
        self.assertEqual(self.relay.sent('/ask')[-1]['fleet'], tfr.FR)

    def test_a_teammates_share_waits_then_adds_a_person_marked_shared_by_them(self):
        question = {'name': 'Rae Moss', 'emails': ['RAE@north.example', 'not an email'], 'phones': ['+44 20 7946 0000'], 'org': 'North Ltd',
                    'role': 'CTO', 'note': 'Ask her about the API', 'run': 'rm -rf /', 'own': 'yes'}
        self.assertEqual(self.take(question), 'waiting')
        self.assertEqual(self.relay.sent('/answer')[-1], {'id': 'c1', 'status': 'waiting'})
        waiting = self.fleet.contacts_in()
        self.assertEqual(len(waiting), 1)
        self.assertEqual((waiting[0]['from'], waiting[0]['kind'], waiting[0]['existing']), ('Pat', 'work', None))
        self.assertEqual(waiting[0]['card'], {'name': 'Rae Moss', 'emails': ['rae@north.example'], 'phones': ['+44 20 7946 0000'], 'org': 'North Ltd',
                                              'role': 'CTO', 'note': 'Ask her about the API'})  # nothing else of it is kept
        done = self.fleet.contact_decide(waiting[0]['id'], 'add')
        self.assertEqual(done['status'], 'added')
        self.assertEqual(self.builds, 1)
        self.assertEqual(self.relay.sent('/answer')[-1], {'id': 'c1', 'status': 'answered', 'answer': {'stage': 'added'}})
        rae = self.person('email:rae@north.example')
        self.assertEqual(rae['name'], 'Rae Moss')
        self.assertIn('+44 20 7946 0000', [p['value'] for p in rae['phones']])
        self.assertEqual((rae['profile'] or {}).get('title'), 'CTO')
        self.assertEqual(rae['side'], 'work')
        with self.store.connect() as db:
            mark = self.fleet.contact_mark(db, rae['id'])
        self.assertEqual((mark['by'], mark['kind'], mark['note']), ('Pat', 'work', 'Ask her about the API'))
        self.assertEqual(self.fleet.contacts_in(), [])
        with self.assertRaisesRegex(ValueError, 'already'):
            self.fleet.contact_decide(waiting[0]['id'], 'add')

    def test_a_share_of_someone_known_is_merged_and_changes_nothing_there(self):
        self.edit_sam(title='Founder')
        self.take({'name': 'Samuel L.', 'emails': ['sam@client.example'], 'phones': ['+32 470 99 88 77'], 'role': 'Intern'})
        waiting = self.fleet.contacts_in()[0]
        self.assertEqual(waiting['existing']['name'], 'Sam Lee')
        self.assertEqual(self.fleet.contact_decide(waiting['id'], 'add')['status'], 'merged')
        sam = self.person(SAM)
        self.assertEqual((sam['name'], sam['profile']['title']), ('Sam Lee', 'Founder'))  # their name and role stay
        self.assertEqual(sorted(e['value'] for e in sam['emails']), ['sam@client.example'])
        self.assertIn('+32 470 99 88 77', [p['value'] for p in sam['phones']])
        self.assertEqual(self.relay.sent('/answer')[-1]['answer'], {'stage': 'merged'})

    def test_dismiss_and_junk(self):
        self.take({'name': 'Rae Moss'}, ask_id='c1')
        self.assertEqual(self.fleet.contact_decide('c1', 'dismiss')['status'], 'dismissed')
        self.assertEqual(self.relay.sent('/answer')[-1], {'id': 'c1', 'status': 'declined'})
        self.assertIsNone(self.person('email:rae@north.example'))
        self.assertEqual(self.take({'emails': ['x@y.example']}, ask_id='c2'), 'declined')  # no name
        self.assertEqual(self.take('Rae', ask_id='c3'), 'declined')
        self.assertEqual(self.take({'name': 'Rae'}, ask_id='c4', sender='stranger'), 'declined')
        self.assertEqual(self.fleet.contacts_in(), [])

    def test_a_friends_share_is_a_suggestion_to_add(self):
        self.assertEqual(self.take({'name': 'Lou Own', 'emails': ['lou@lou.example'], 'own': True}, ask_id='f1', sender='fp_lou', group='friends'), 'waiting')
        waiting = self.fleet.contacts_in()[0]
        self.assertEqual((waiting['kind'], waiting['where'], waiting['card']['own']), ('friends', 'Friends', True))
        self.assertEqual(contact_share.question_text(waiting['card']), 'Shares their own contact: Lou Own')
        self.fleet.contact_decide('f1', 'add')
        lou = self.person('email:lou@lou.example')
        self.assertIsNone(lou['side_by'])  # a friend's contact gets its side as anyone does, never made Work by the share

    def test_an_answer_shows_how_it_went(self):
        shown = self.fleet.contact_preview(SAM, {}, '', self.work, 'pat1')
        self.fleet.contact_send(SAM, {}, '', self.work, 'pat1', shown['digest'])
        self.assertEqual(self.fleet.contact_sent(SAM)[0]['state'], 'sent')
        with self.store.connect() as db:
            out = db.execute("SELECT id FROM fleet_out WHERE kind='contact'").fetchone()['id']
        self.fleet.take_answer({'id': out, 'status': 'answered', 'answer': {'stage': 'added', 'extra': 'x'}})
        self.assertEqual(self.fleet.contact_sent(SAM)[0]['state'], 'added')


if __name__ == '__main__':
    unittest.main()
