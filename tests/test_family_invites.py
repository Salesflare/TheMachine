"""Inviting family at the right moment (family_invites.py, docs/family.md): a to-do the review marks as family
coordination with someone (family_with) gets "Invite Sasha?" once, Not now hides it for 90 days, the switch turns it
off, and Work contacts, Family members and people with an open invite never get it. Nothing is sent from here."""
import datetime as dt
import json
import unittest
import urllib.parse

import test_fleet as tf
from test_fleet import CONFIG, a

fleet, family_invites = a.fleet, a.fleet.family.family_invites
FAM = 'fl_' + 'f' * 16
WORK_ID = 'fl_' + 'b' * 16
HOSTED = {**CONFIG, 'manage_url': 'https://cp.example/setup'}


class Relay(tf.FakeRelay):
    def __init__(self, role='owner', family=True):
        super().__init__()
        self.directory['fleets'][0]['id'] = WORK_ID
        if family:
            self.directory['fleets'].append({
                'id': FAM, 'kind': 'family', 'name': 'Home', 'secret': 'f' * 64, 'asks': ['availability', 'todo', 'event'],
                'me': {'member_id': 'fm_me', 'role': role}, 'invited': ['nora@mail.example'],
                'members': [{'member_id': 'fm_me', 'name': 'Owner', 'role': role, 'me': True, 'emails': ['owner@gmail.com']},
                            {'member_id': 'fm_robin', 'name': 'Robin', 'role': 'member', 'emails': ['robin@home.example'], 'machine': True}]})


class FamilyInvites(unittest.TestCase):
    def setUp(self):
        tf.Fleet.setUp(self)
        self.use(Relay())
        with self.store.connect() as db:
            for node, name, email, side in (('p_sasha', 'Sasha Lane', 'sasha@mail.example', 'personal'),
                                            ('p_robin', 'Robin', 'robin@home.example', 'personal'),
                                            ('p_pat', 'Pat', tf.TEAM, 'work'),
                                            ('p_nora', 'Nora', 'nora@mail.example', 'personal'),
                                            ('p_lee', 'Lee Ray', 'lee@client.example', 'work')):
                db.execute("INSERT OR REPLACE INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person',?,1,1,?)",
                           (node, name, json.dumps({'identifiers': ['email:' + email], 'side': side})))
        self.cards = iter(range(100, 10**6))

    def use(self, relay, config=HOSTED):
        self.relay = relay
        self.fleet = fleet.Fleet(self.store.connect, config, lambda: 'token', relay=relay)
        self.fleet.directory(refresh=True)

    def offer(self, node='p_sasha', work=False):
        card = str(next(self.cards))
        return card, self.fleet.family_invite_offer(card, node, work)

    def shown(self, card, status='pending', scope='personal'):
        cards = [{'id': card, 'status': status, 'scope': scope}]
        with self.store.connect() as db:
            self.fleet.family_invite_annotate(db, cards)
        return cards[0].get('family_invite')

    def activity(self):
        with self.store.connect() as db:
            return [line['what'] for line in family_invites.activity_lines(db, 20)]

    def test_the_suggestion_appears_on_the_todo_with_the_prefilled_invite(self):
        card, why = self.offer()
        self.assertEqual(why, 'offered')
        shown = self.shown(card)
        self.assertEqual(shown['question'], 'Invite Sasha?')
        self.assertEqual(shown['line'], 'Your Machines can sort this out without you asking each other.')
        url = urllib.parse.urlsplit(shown['url'])
        self.assertEqual((url.scheme, url.netloc, url.path, url.fragment), ('https', 'cp.example', '/account', f'invites-{FAM}'))
        self.assertEqual(urllib.parse.parse_qs(url.query), {'tab': ['fleet'], 'invite': ['family'], 'to': ['sasha@mail.example'],
                                                            'name': ['Sasha Lane']})
        self.assertEqual(self.activity(), ['Suggested inviting Sasha Lane to the Family'])
        self.assertIsNone(self.shown(card, status='completed'))  # a done to-do no longer asks

    def test_invite_opens_the_account_page_and_sends_nothing(self):
        card, _ = self.offer()
        before = list(self.relay.calls)
        done = self.fleet.family_invite(card, 'open')
        self.assertEqual(done['state'], 'invited')
        self.assertIn('to=sasha%40mail.example', done['url'])
        self.assertEqual(self.relay.calls, before)  # nothing went to the Network: the owner sends it on the account page
        self.assertIsNone(self.shown(card))
        self.assertEqual(self.offer()[1], 'once')  # and never again for her
        self.assertEqual(self.activity()[0], 'Opened the Family invite for Sasha Lane')

    def test_once_per_person(self):
        first, _ = self.offer()
        second, why = self.offer()
        self.assertEqual(why, 'once')
        self.assertTrue(self.shown(first))
        self.assertIsNone(self.shown(second))

    def test_not_now_hides_it_for_90_days(self):
        card, _ = self.offer()
        done = self.fleet.family_invite(card, 'later')
        self.assertEqual(done['state'], 'later')
        self.assertIsNone(self.shown(card))
        self.assertEqual(self.offer()[1], 'once')
        self.assertEqual(self.activity()[0], 'Not now: inviting Sasha Lane to the Family')
        later = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=91)).isoformat(timespec='seconds')
        with self.store.connect() as db:
            self.assertEqual(family_invites.offer(db, '900', 'p_sasha', self.fleet.fleets(), fleet.account_url(HOSTED), now=later), 'offered')
            soon = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=89)).isoformat(timespec='seconds')
            db.execute("UPDATE family_invite_offers SET state='later',until=?", (soon,))
            self.assertEqual(family_invites.offer(db, '901', 'p_sasha', self.fleet.fleets(), fleet.account_url(HOSTED)), 'once')

    def test_the_setting_turns_it_off(self):
        card, _ = self.offer()
        self.assertEqual(self.fleet.family_invite_set(False), {'on': False})
        self.assertIsNone(self.shown(card))
        self.assertEqual(self.offer('p_lee')[1], 'off')
        self.fleet.family_invite_set(True)
        self.assertTrue(self.shown(card))

    def test_never_for_work_contacts(self):
        self.assertEqual(self.offer('p_pat')[1], 'work')  # in the Work Fleet, on the Work side
        self.assertEqual(self.offer('p_lee')[1], 'work')  # the Graph's Work side
        self.assertEqual(self.offer('p_sasha', work=True)[1], 'work')  # a Work to-do
        card, _ = self.offer()
        self.assertIsNone(self.shown(card, scope='work'))

    def test_never_for_a_family_member_or_an_open_invite(self):
        self.assertEqual(self.offer('p_robin')[1], 'member')  # has a Machine in the Family already
        self.assertEqual(self.offer('p_nora')[1], 'invited')  # an open invite, from the directory
        card, _ = self.offer()
        self.relay.directory['fleets'][1]['members'].append({'member_id': 'fm_j', 'name': 'Sasha', 'role': 'member',
                                                             'emails': ['sasha@mail.example'], 'machine': True})
        self.fleet.directory(refresh=True)
        self.assertIsNone(self.shown(card))  # she joined since

    def test_only_where_the_family_fleet_feature_is(self):
        self.use(Relay(role='member'))  # can't invite to someone else's Family
        self.assertEqual(self.offer()[1], 'no family invites')
        self.use(Relay(), config=CONFIG)  # no account page: no Family Fleet feature
        self.assertEqual(self.offer()[1], 'no family invites')
        self.use(Relay(family=False))  # no Family yet: the account page starts one
        card, why = self.offer()
        self.assertEqual(why, 'offered')
        self.assertTrue(self.shown(card)['url'].endswith('#fleet'))
        self.assertEqual(self.offer('nobody')[1], 'no address')

    def test_the_review_passes_family_with_and_the_app_wires_it(self):
        app = object.__new__(a.App)
        app.store, app.config, app.fleet = self.store, {**HOSTED, 'digest_at': '08:30'}, self.fleet
        with self.store.connect() as db:
            home = db.execute("SELECT id FROM events WHERE account_id='home'").fetchone()[0]
        saved = app.action('suggest', {'dedupe_key': 'pickup', 'title': 'Who picks up the kids on Wednesday?',
                                       'body': 'Sasha asked who does Wednesday.', 'event_ids': [home], 'family_with': 'p_sasha'})
        self.assertEqual(saved['family_invite'], 'offered')
        self.assertIn('family_invite', a.FAMILY_ACTIONS)
        self.assertIn('family_with', a.review_prompt('r1', ['home']))
        with self.assertRaisesRegex(ValueError, 'dashboard'):  # the owner's own taps, never the agent's
            app.action('family_invite', {'suggestion_id': saved['id'], 'do': 'open'})
        self.assertEqual(app.action('family_invite_setting', {'on': False}, owner_dashboard=True), {'on': False})


class PersonInvite(unittest.TestCase):
    """Invite to The Machine on a person's page (family_invites.person_invite): only for someone with no Machine the owner
    knows of, never the owner; the Family invite as one way for someone it fits. Nothing is sent from here."""
    setUp, use = FamilyInvites.setUp, FamilyInvites.use

    def invite(self, node, mark=None, side=None, config=HOSTED, owner=('owner@gmail.com',)):
        app = object.__new__(a.App)
        app.store, app.config, app.fleet = self.store, {**config, 'owner_emails': list(owner)}, self.fleet
        page = {'id': node, 'kind': 'person', **({'fleet': mark} if mark else {}), **({'side': side} if side else {})}
        return app.person_invite(page)

    def test_someone_with_no_machine_gets_the_words_and_the_family_invite(self):
        before = list(self.relay.calls)
        found = self.invite('p_sasha', side='personal')
        self.assertEqual({k: found[k] for k in ('name', 'first', 'email')}, {'name': 'Sasha Lane', 'first': 'Sasha', 'email': 'sasha@mail.example'})
        url = urllib.parse.urlsplit(found['family']['url'])
        self.assertEqual((url.path, url.fragment), ('/account', f'invites-{FAM}'))
        self.assertEqual(urllib.parse.parse_qs(url.query)['to'], ['sasha@mail.example'])
        self.assertEqual(self.relay.calls, before)  # nothing sent, nothing asked of the Network

    def test_no_family_invite_for_work_contacts_or_without_an_account_page(self):
        self.assertIsNone(self.invite('p_lee', side='work')['family'])  # still Invite to The Machine, not to the Family
        self.assertIsNone(self.invite('p_sasha', config=CONFIG)['family'])
        self.use(Relay(role='member'))
        self.assertIsNone(self.invite('p_sasha')['family'])

    def test_nothing_for_someone_with_a_machine_or_the_owner(self):
        self.assertIsNone(self.invite('p_robin', mark={'machine': True, 'in': [{'kind': 'family'}]}))  # Family already
        self.assertIsNone(self.invite('p_sasha', mark={'machine': True, 'in': [], 'network': {'can_add': True}}))  # found: Add as a friend
        self.assertIsNone(self.invite('p_sasha', owner=('sasha@mail.example',)))  # the owner's own address
        self.assertIsNone(self.invite('nobody'))
        with self.store.connect() as db:
            self.assertIsNone(family_invites.person_invite(db, {'id': 'p_sasha', 'kind': 'org'}))

    def test_a_shared_address_is_not_one_to_invite_at(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('p_desk','person','Desk',1,1,?)",
                       (json.dumps({'identifiers': ['email:info@shop.example']}),))
        found = self.invite('p_desk')
        self.assertEqual((found['email'], found['family']), ('', None))  # Copy only
