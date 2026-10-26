"""Finding people you know on the Network (discovery.py): off until turned on, contacts go out blinded, only matches are
looked up, a card only with a concrete reason, colleague read from structure, connect is a friend request, Not now,
Never, findable, and leaving. A fake Network stands in for the control plane; no network, no sends."""
import datetime as dt
import json
import secrets
import unittest

import test_fleet as tf
import test_friends as tfr
from test_fleet import CONFIG, NOW

discovery = tf.a.fleet.discovery
fleet = tf.a.fleet

ON_NETWORK = {'nia@nia.example': ('nia', 'Nia North', False), 'lou@lou.example': ('lou', 'Lou', True),
              'sam@acme.example': ('sam', 'Sam', False)}


class NetworkRelay(tfr.FriendsRelay):
    def __init__(self):
        super().__init__()
        self.b = secrets.randbits(256) | 1
        self.joined = []
        self.found = {e: discovery.hexed(pow(discovery.to_group(e), self.b, discovery.P)) for e in ON_NETWORK}

    def call(self, method, path, body=None, timeout=40):
        if path != '/discover':
            return super().call(method, path, body, timeout)
        self.calls.append((method, path, body))
        if body['action'] == 'match':
            return {'items': [discovery.hexed(pow(int(x, 16), self.b, discovery.P)) for x in body['items']],
                    'found': sorted(y for e, y in self.found.items() if discovery.bucket(e) in body['buckets'])}
        if body['action'] == 'resolve':
            return {'people': [{'email': e, 'username': ON_NETWORK[e][0], 'name': ON_NETWORK[e][1], 'friends': ON_NETWORK[e][2]}
                               for e in body['emails'] if e in ON_NETWORK]}
        if body['action'] == 'status':
            return {'discoverable': False, 'username': 'owner', 'joined': self.joined, 'at': '2026-10-21T12:00:00+00:00'}
        if body['action'] == 'discoverable':
            self.findable = body.get('emails') if body['on'] else []
            return {'discoverable': body['on'], 'addresses': ([{'email': 'owner@acme.example', 'source': 'account'}] if body['on'] else []) +
                    [{'email': e, 'source': 'machine'} for e in self.findable if e != 'owner@acme.example']}
        return {'left': True, 'friends_removed': 1}


class Discovery(unittest.TestCase):
    def setUp(self):
        tf.Fleet.setUp(self)
        self.relay = NetworkRelay()
        self.fleet = fleet.Fleet(self.store.connect, CONFIG, lambda: 'token', relay=self.relay)
        self.fleet.directory(refresh=True)
        meeting = NOW + dt.timedelta(days=3)
        self.store.commit_page('home', {}, [{'account_id': 'home', 'source_id': 'cal-nia', 'kind': 'calendar.event', 'occurred_at': meeting.isoformat(),
                                            'title': 'Picnic', 'body': '', 'deleted': False, 'metadata': {}}])
        with self.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id='cal-nia'").fetchone()[0]
            for node, name, emails, strength in [('p-nia', 'Nia North', ['nia@nia.example'], 5), ('p-lou', 'Lou', ['lou@lou.example'], 4),
                                                 ('p-sam', 'Sam', ['sam@acme.example'], 3), ('p-zed', 'Zed', ['zed@zed.example'], 2),
                                                 ('p-me', 'Owner', ['owner@gmail.com'], 9)]:
                db.execute('INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,?,?,?,?,?)',
                           (node, 'person', name, strength, 3, json.dumps({'identifiers': ['email:' + e for e in emails]})))
            db.execute('INSERT INTO graph_events(node_id,event_id,at) VALUES(?,?,?)', ('p-nia', event, meeting.isoformat()))

    def people(self):
        return {p['username']: p for p in self.fleet.network_view()['people']}

    def test_incomplete_match_response_does_not_commit_negative_matches(self):
        real = self.relay.call
        for answer in ({}, {'items': [], 'found': []}):
            with self.subTest(answer=answer):
                def incomplete(method, path, body=None, timeout=40):
                    return answer if path == '/discover' and body['action'] == 'match' else real(method, path, body, timeout)
                self.relay.call = incomplete
                result = self.fleet.network_action('find_on')
                self.assertIn('Looking up later', result['note'])
                with self.store.connect() as db:
                    self.assertEqual(db.execute('SELECT count(*) FROM network_looked').fetchone()[0], 0)
                self.assertIsNone(self.fleet.network_settings().get('last'))
        self.relay.call = real
        self.fleet.discovery_round()
        self.assertIn('nia', self.people())

    def test_unresolved_matches_remain_eligible_after_rate_limit(self):
        real = self.relay.call
        def limited(method, path, body=None, timeout=40):
            if path == '/discover' and body['action'] == 'resolve':
                raise ValueError('HTTP 429')
            return real(method, path, body, timeout)
        self.relay.call = limited
        self.fleet.network_action('find_on')
        with self.store.connect() as db:
            looked = {r[0] for r in db.execute('SELECT email FROM network_looked')}
        self.assertIn('zed@zed.example', looked)  # a confirmed non-match is done
        self.assertNotIn('nia@nia.example', looked)  # a match with no answer is not
        self.relay.call = real
        self.ago(new_at=discovery.NEW_EVERY + 1)
        self.fleet.discovery_round()
        self.assertIn('nia', self.people())

    def test_failed_known_person_refresh_is_retried_incrementally(self):
        self.fleet.network_action('find_on')
        self.ago(last=86401, refreshed=8 * 86400)
        real = self.relay.call
        def limited(method, path, body=None, timeout=40):
            if path == '/discover' and body['action'] == 'resolve':
                raise ValueError('HTTP 429')
            return real(method, path, body, timeout)
        self.relay.call = limited
        self.fleet.discovery_round()
        self.relay.call = real
        before = len([b for b in self.relay.sent('/discover') if b['action'] == 'resolve'])
        self.ago(new_at=discovery.NEW_EVERY + 1)
        self.fleet.discovery_round()
        self.assertGreater(len([b for b in self.relay.sent('/discover') if b['action'] == 'resolve']), before)

    def test_matches_beyond_the_per_round_cap_are_checked_next_round(self):
        contacts = [(f'person{i}@example.test', None, str(i)) for i in range(105)]
        self.fleet._set_network(find=True)
        from unittest.mock import patch
        with patch.object(self.fleet, 'network_contacts', return_value=contacts), \
                patch.object(discovery, 'blind', return_value=(1, [], [])), \
                patch.object(discovery, 'matches', side_effect=lambda emails, *args: emails):
            self.fleet.discovery_round(force=True)
            with self.store.connect() as db:
                self.assertEqual(db.execute('SELECT count(*) FROM network_looked').fetchone()[0], 100)
            self.ago(new_at=discovery.NEW_EVERY + 1)
            self.fleet.discovery_round()
            with self.store.connect() as db:
                self.assertEqual(db.execute('SELECT count(*) FROM network_looked').fetchone()[0], 105)

    def test_off_until_turned_on(self):
        self.assertEqual(self.fleet.discovery_round(force=True), 0)
        self.assertEqual(self.relay.sent('/discover'), [])
        view = self.fleet.view()['network']
        self.assertEqual(view, {'find': None, 'discoverable': None, 'asked': False, 'last': None, 'people': [], 'addresses': view['addresses']})
        self.assertFalse(any(a['findable'] for a in view['addresses']))

    def test_lookup_is_blinded_and_only_matches_are_resolved(self):
        self.fleet.network_action('find_on')
        match, resolve = self.relay.sent('/discover')
        self.assertEqual(match['action'], 'match')
        with self.store.connect() as db:
            contacts = [c[0] for c in self.fleet.network_contacts(db)]
        self.assertEqual(len(match['items']), len(contacts))
        self.assertNotIn('owner@gmail.com', contacts)  # the owner's own addresses stay out
        self.assertIn('zed@zed.example', contacts)
        self.assertNotIn('@', json.dumps(match))
        self.assertEqual(sorted(resolve['emails']), ['lou@lou.example', 'nia@nia.example', 'sam@acme.example'])  # not Zed
        people = self.people()
        self.assertEqual(people['lou']['status'], 'connected')
        self.assertEqual((people['nia']['status'], people['nia']['hint']), ('new', 'personal'))
        self.assertEqual([r['kind'] for r in people['nia']['reasons']], ['meeting'])
        self.assertEqual((people['sam']['hint'], people['sam']['reasons']), ('colleague', []))  # same work domain; no reason, no card
        # A day has not passed and nobody new: no second lookup
        self.fleet.discovery_round()
        self.assertEqual(len(self.relay.sent('/discover')), 2)
        with self.store.connect() as db:
            self.assertIn(f'Checked {len(contacts)} contacts privately; 3 on the Network', [r['what'] for r in db.execute('SELECT what FROM fleet_log')])

    def test_a_failing_lookup_is_logged_once_and_tried_again(self):
        import urllib.error
        self.fleet.network_action('find_on')
        self.fleet._set_network(last='2000-01-01T00:00:00+00:00')
        real, sent = self.relay.call, len(self.relay.sent('/discover'))

        def cut(method, path, body=None, timeout=40):
            if path == '/discover':
                raise urllib.error.URLError(ConnectionResetError(104, 'Connection reset by peer'))
            return real(method, path, body, timeout)
        self.relay.call = cut
        with self.assertLogs(fleet.LOG.name, 'INFO') as logs:
            for _ in range(3):
                self.fleet.discovery_step()  # the rest of the step goes on
            self.relay.call = real
            self.fleet.discovery_step()
        self.assertEqual([m.split(':', 2)[2] for m in logs.output],
                         ['network discovery failed error=URLError; tried again every round', 'network discovery works again'])
        self.assertEqual(len(self.relay.sent('/discover')), sent + 1)  # the lookup was done once it worked (the people found before: not again)

    def ago(self, **values):
        self.fleet._set_network(**{k: (dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=v)).isoformat(timespec='seconds')
                                   for k, v in values.items()})

    def lookups(self):
        return [b for b in self.relay.sent('/discover') if b['action'] == 'match']

    def person(self, node, email, strength=1):
        with self.store.connect() as db:
            db.execute('INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,?,?,?,?,?)',
                       (node, 'person', node, strength, 3, json.dumps({'identifiers': ['email:' + email]})))

    def test_daily_and_soon_after_someone_new_is_met(self):
        self.fleet.network_action('find_on')
        self.assertEqual(len(self.lookups()), 1)
        ON_NETWORK['kit@kit.example'] = ('kit', 'Kit', False)
        self.addCleanup(ON_NETWORK.pop, 'kit@kit.example')
        self.relay.found['kit@kit.example'] = discovery.hexed(pow(discovery.to_group('kit@kit.example'), self.relay.b, discovery.P))
        self.person('p-kit', 'kit@kit.example')  # someone new met
        self.fleet.discovery_round()
        self.assertEqual(len(self.lookups()), 1)  # not within NEW_EVERY of the last look
        self.ago(new_at=discovery.NEW_EVERY + 1)
        self.fleet.discovery_round()
        self.assertEqual(len(self.lookups()[-1]['items']), 1)  # only Kit, and only Kit is looked up by address
        self.assertEqual(self.relay.sent('/discover')[-1], {'action': 'resolve', 'emails': ['kit@kit.example']})
        self.assertEqual(self.people()['kit']['status'], 'new')
        self.ago(new_at=discovery.NEW_EVERY + 1)
        self.fleet.discovery_round()
        self.assertEqual(len(self.lookups()), 2)  # nobody new: nothing
        resolves = len([b for b in self.relay.sent('/discover') if b['action'] == 'resolve'])
        self.ago(last=86400 + 1)
        self.fleet.discovery_round()
        with self.store.connect() as db:
            contacts = self.fleet.network_contacts(db)
        self.assertEqual(len(self.lookups()[-1]['items']), len(contacts))  # the daily one: everyone
        self.assertEqual(len([b for b in self.relay.sent('/discover') if b['action'] == 'resolve']), resolves)  # all known: not again this week
        self.assertEqual(self.fleet.network_view()['last'][:10], dt.datetime.now(dt.timezone.utc).date().isoformat())

    def test_someone_newly_findable_looks_up_the_contacts_in_their_bucket(self):
        self.fleet.network_action('find_on')
        self.relay.joined = [discovery.bucket('zed@zed.example')]
        self.ago(new_at=discovery.NEW_EVERY + 1)
        self.fleet.discovery_round()
        status = [b for b in self.relay.sent('/discover') if b['action'] == 'status'][-1]
        self.assertTrue(status['joined_since'])
        self.assertEqual(len(self.lookups()), 2)
        same = [e for e in ('nia@nia.example', 'lou@lou.example', 'sam@acme.example', 'zed@zed.example') if discovery.bucket(e) == self.relay.joined[0]]
        self.assertEqual(len(self.lookups()[-1]['items']), len(same))
        self.assertEqual(self.lookups()[-1]['buckets'], self.relay.joined)
        self.assertEqual(self.fleet.network_settings()['joined_since'], '2026-10-21T12:00:00+00:00')  # the Network's clock
        self.ago(new_at=discovery.NEW_EVERY + 1)
        self.fleet.discovery_round()
        self.assertEqual(len(self.lookups()), 2)  # asked hourly only, and those buckets are done

    def test_connect_later_never(self):
        self.fleet.network_action('find_on')
        self.assertEqual(self.fleet.network_action('connect', 'nia@nia.example', 'family'), {'status': 'requested', 'relation': 'family'})
        self.assertEqual(self.relay.sent('/friends')[-1], {'action': 'add', 'username': 'nia'})
        self.assertEqual(self.people()['nia']['relation'], 'family')
        self.fleet.network_action('never', 'sam@acme.example')
        self.assertNotIn('sam', self.people())
        with self.assertRaises(ValueError):
            self.fleet.network_action('connect', 'zed@zed.example')

    def test_someone_in_a_fleet_together_is_not_suggested_until_they_leave(self):
        work = self.relay.directory['fleets'][0]
        work['members'].append({'member_id': 'nia1', 'name': 'Nia North', 'role': 'member', 'emails': ['nia@nia.example'], 'username': 'nia'})
        self.fleet.directory(refresh=True)
        self.fleet.network_action('find_on')
        self.assertNotIn('nia', self.people())  # connected already through the Fleet: no card, not under the Network block
        self.assertEqual(self.people()['lou']['status'], 'connected')  # a friendship stays as it is
        with self.store.connect() as db:
            self.assertIsNone(db.execute("SELECT 1 FROM network_people WHERE username='nia'").fetchone())
        # Known by username only (another address of theirs matched): the same
        work['members'][-1]['emails'] = ['nia@work.example']
        self.fleet.directory(refresh=True)
        self.fleet.discovery_round(force=True)
        self.assertNotIn('nia', self.people())
        # Nia leaves the Fleet: suggestable again, with the meeting as the reason
        work['members'].pop()
        self.fleet.directory(refresh=True)
        self.fleet.discovery_round(force=True)
        self.assertEqual((self.people()['nia']['status'], [r['kind'] for r in self.people()['nia']['reasons']]), ('new', ['meeting']))
        # Back in a Family Fleet: hidden again at once, before the next lookup
        self.relay.directory['fleets'].append({'id': 'fl_' + 'f' * 16, 'kind': 'family', 'name': 'Home', 'secret': 's' * 64, 'asks': [], 'members': [
            {'member_id': 'me2', 'name': 'Owner', 'role': 'owner', 'me': True, 'emails': ['owner@gmail.com']},
            {'member_id': 'nia2', 'name': 'Nia North', 'role': 'member', 'emails': ['nia@nia.example']}]})
        self.fleet.directory(refresh=True)
        self.assertNotIn('nia', self.people())

    def test_later_comes_back_only_with_something_new(self):
        self.fleet.network_action('find_on')
        self.fleet.network_action('later', 'nia@nia.example')
        self.fleet.discovery_round()
        self.assertEqual(self.people()['nia']['status'], 'later')  # the same meeting: stays hidden
        # An open card with them comes up: back, with that reason
        with self.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id='cal-nia'").fetchone()[0]
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,?,?,?,?,?)",
                       ('s-nia', 'k-nia', 'Bring the tent', '', json.dumps([event]), '["home"]', 'pending', NOW.isoformat()))
        self.fleet.discovery_round()
        nia = self.people()['nia']
        self.assertEqual((nia['status'], nia['reasons'][0]), ('new', {'kind': 'card', 'card': 's-nia', 'title': 'Bring the tent'}))

    def test_findable_and_leave(self):
        self.assertEqual(self.fleet.network_action('discoverable_on'), {'discoverable': True})
        self.fleet.network_action('find_on')
        self.assertEqual(self.fleet.network_action('leave'), {'left': True})
        self.assertEqual(self.relay.sent('/discover')[-1], {'action': 'leave'})
        view = self.fleet.network_view()
        self.assertEqual((view['find'], view['discoverable'], view['people']), (False, False, []))

    def test_findable_by_each_connected_address_and_each_can_be_turned_off(self):
        self.assertEqual(self.fleet.own_addresses(), ['owner@acme.example', 'owner@gmail.com'])
        self.fleet.network_action('discoverable_on')
        self.assertEqual(self.relay.sent('/discover')[-1],
                         {'action': 'discoverable', 'on': True, 'emails': ['owner@acme.example', 'owner@gmail.com']})
        view = self.fleet.network_view()['addresses']
        self.assertEqual([(a['email'], a['account'], a['on'], a['findable']) for a in view],
                         [('owner@acme.example', True, True, True), ('owner@gmail.com', False, True, True)])
        self.assertEqual(self.fleet.network_action('address_off', 'Owner@Gmail.com'), {'email': 'owner@gmail.com', 'findable': False})
        self.assertEqual(self.relay.sent('/discover')[-1]['emails'], ['owner@acme.example'])
        self.assertEqual([(a['on'], a['findable']) for a in self.fleet.network_view()['addresses']], [(True, True), (False, False)])
        with self.assertRaises(ValueError):
            self.fleet.network_action('address_off', 'someone@else.example')  # only the owner's own
        # A newly connected account goes out with the next round, without asking again
        sent = len(self.relay.sent('/discover'))
        self.fleet.discovery_round()
        self.assertEqual(len(self.relay.sent('/discover')), sent)  # nothing changed
        self.fleet.config = {**self.fleet.config, 'accounts': self.fleet.config['accounts'] + [
            {'id': 'side', 'email': 'owner@side.example', 'transport': 'gog'}, {'id': 'chat', 'email': 'owner@chat.example', 'service': 'slack'}]}
        self.fleet.discovery_round()
        self.assertEqual(self.relay.sent('/discover')[-1]['emails'], ['owner@acme.example', 'owner@side.example'])  # not the chat login
        self.fleet.network_action('discoverable_off')
        self.assertEqual(self.fleet.network_view()['addresses'][0]['findable'], False)

    def test_group_matches_the_network(self):
        a, items, buckets = discovery.blind(['x@example.com'], secret=7)
        self.assertEqual(items, [discovery.hexed(pow(discovery.to_group('X@Example.com '), 7, discovery.P))])
        self.assertEqual(buckets, [discovery.bucket('x@example.com')])


if __name__ == '__main__':
    unittest.main()
