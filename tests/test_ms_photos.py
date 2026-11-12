"""Photos from Microsoft 365 and Outlook.com through Graph: colleagues by their work address on the organization's own
domains, Outlook contacts and their job titles, only for people in the graph without a photo, within a daily budget;
nothing without the scope; and the ask to reconnect an account connected before these scopes (machine/app/reconnect_asks.py)."""
import datetime as dt
import struct
import unittest
import zlib
from unittest import mock

import test_graph as tg

from machine.app import reconnect_asks, workers
import ms_graph
import ms_photos

a = tg.a
enrichment = a.enrichment
NOW = tg.NOW.isoformat()
SCOPES = {'User.Read', 'Mail.ReadWrite', 'User.ReadBasic.All', 'Contacts.Read'}
OUTLOOK = {'id': 'mail', 'service': 'outlook', 'transport': 'broker', 'email': 'sam@acme.com'}


def png(seed=0):
    """A real 1x1 PNG, made here."""
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    pixel = zlib.compress(bytes([0, seed % 256, 80, 120]))
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)) + chunk(b'IDAT', pixel) + chunk(b'IEND', b'')


def later(**delta):
    return (tg.NOW + dt.timedelta(**delta)).isoformat()


class Graph:
    """A fake Microsoft Graph: what the account granted and what each call answers, and every call made."""

    def __init__(self, granted=SCOPES, offered=(), photos=None, contacts=(), domains=('acme.com', 'acme.onmicrosoft.com', 'gmail.com')):
        self.granted, self.offered, self.photos, self.contacts, self.domains = set(granted), set(offered), photos or {}, list(contacts), domains
        self.calls = []

    def grant(self, config, credential, account):
        return set(self.granted), set(self.offered)

    def call(self, config, credential, account, method, params=None, raw=False, timeout=60, **_):
        self.calls.append((method, dict(params or {})))
        scope = ms_graph.READ[method][2]
        if not ms_graph.ANSWERS.get(scope, {scope}) & self.granted:
            raise ms_graph.GraphError('microsoft_scope_not_granted', 403)
        if method == 'organization':
            return {'value': [{'verifiedDomains': [{'name': d} for d in self.domains]}]}
        if method == 'contacts.list':
            return {'value': self.contacts}
        key = params.get('user') or params.get('id')
        if key in self.photos:
            return self.photos[key]
        raise ms_graph.GraphError('outlook', 404)

    def asked(self, method):
        return [p for m, p in self.calls if m == method]


class MicrosoftPhotos(unittest.TestCase):
    add, build = tg.Graph.add, tg.Graph.build

    def setUp(self):
        tg.Graph.setUp(self)
        self.config = {'accounts': [OUTLOOK]}

    def people(self, *addresses):
        self.add(*(tg.mail(1, f'Someone <{x}>', 'sam@acme.com') for x in addresses for _ in range(2)))
        self.build()

    def step(self, fake, now=NOW, config=None):
        with mock.patch.object(ms_graph, 'grant', fake.grant), mock.patch.object(ms_graph, 'call', fake.call):
            found = ms_photos.step(self.store.connect, config or self.config, None, now, ask=workers.outlook_photos_ask)
        reconnect_asks.todos(self.store, config or self.config)  # as the enrichment worker does after it
        return found

    def node(self, address):
        with self.store.connect() as db:
            return enrichment.graph_people(db).get('email:' + address)

    def saved(self):
        with self.store.connect() as db:
            return {r[0] for r in db.execute('SELECT identifier FROM person_photos')}

    def todos(self):
        with self.store.connect() as db:
            cards = [dict(r) for r in db.execute('SELECT * FROM suggestions ORDER BY created_at')]
            self.store.machine_fix_views(db, cards)
        return cards

    def test_colleagues_on_the_organizations_own_domains_get_their_photo_once(self):
        self.people('ann@acme.com', 'bo@partner.example', 'cy@gmail.com')
        fake = Graph(photos={'ann@acme.com': png(1)})
        saved, _ = self.step(fake)
        self.assertEqual(saved, 1)
        self.assertEqual(self.saved(), {self.node('ann@acme.com')})
        self.assertEqual([p['user'] for p in fake.asked('users.photo')], ['ann@acme.com'])  # never outside the organization
        self.assertEqual(fake.asked('users.photo')[0]['size'], '96x96')
        fake.calls.clear()
        self.step(fake, now=later(days=2))
        self.assertEqual(fake.asked('users.photo'), [])  # saved: never asked again

    def test_someone_without_a_photo_is_asked_again_after_30_days(self):
        self.people('dee@acme.com')
        fake = Graph()
        self.step(fake)
        self.assertEqual(len(fake.asked('users.photo')), 2)  # 96x96, then 48x48
        self.step(fake, now=later(days=29))
        self.assertEqual(len(fake.asked('users.photo')), 2)
        fake.photos['dee@acme.com'] = png(2)
        self.assertEqual(self.step(fake, now=later(days=31))[0], 1)
        self.assertEqual(self.saved(), {self.node('dee@acme.com')})

    def test_what_is_not_a_small_image_is_not_kept(self):
        self.people('eve@acme.com', 'fay@acme.com')
        fake = Graph(photos={'eve@acme.com': b'<html>not a photo</html>', 'fay@acme.com': png(3) + b'0' * enrichment.PHOTO_BYTES})
        self.assertEqual(self.step(fake)[0], 0)
        self.assertEqual(self.saved(), set())

    def test_at_most_the_days_budget(self):
        self.people(*(f'p{i}@acme.com' for i in range(12)))
        fake = Graph()
        with mock.patch.object(ms_photos, 'PER_DAY', 5):
            self.step(fake)
            self.step(fake, now=later(hours=3))
            self.assertEqual(len({p['user'] for p in fake.asked('users.photo')}), 5)
            self.step(fake, now=later(days=1))
            self.assertEqual(len({p['user'] for p in fake.asked('users.photo')}), 10)

    def test_a_personal_account_has_no_colleagues(self):
        self.people('gus@outlook.com')
        fake = Graph(domains=('outlook.com',), photos={'gus@outlook.com': png(4)})
        self.step(fake)
        self.assertEqual(fake.asked('users.photo'), [])

    def test_outlook_contacts_bring_their_photo_title_and_company(self):
        self.people('hal@partner.example')
        contacts = [{'id': 'c1', 'emailAddresses': [{'address': 'Hal@Partner.example'}], 'jobTitle': 'Buyer', 'companyName': 'Partner'},
                    {'id': 'c2', 'emailAddresses': [{'address': 'stranger@else.example'}], 'jobTitle': 'Chef'}]
        fake = Graph(contacts=contacts, photos={'c1': png(5)})
        saved, facts = self.step(fake)
        self.assertEqual(saved, 1)
        self.assertEqual(self.saved(), {self.node('hal@partner.example')})
        self.assertEqual([p['id'] for p in fake.asked('contacts.photo')], ['c1'])  # not someone outside the graph
        self.assertGreaterEqual(facts, 1)
        with self.store.connect() as db:
            got = {(r[0], r[1]) for r in db.execute("SELECT field,value FROM person_facts WHERE source='outlook'")}
        self.assertIn(('title', 'Buyer'), got)
        fake.calls.clear()
        self.step(fake, now=later(hours=2))
        self.assertEqual(fake.asked('contacts.list'), [])  # once a day

    def test_nothing_is_asked_without_its_scope(self):
        self.people('ivy@acme.com')
        fake = Graph(granted={'User.Read', 'Mail.ReadWrite'}, contacts=[{'id': 'c1', 'emailAddresses': [{'address': 'ivy@acme.com'}]}])
        self.assertEqual(self.step(fake), (0, 0))
        self.assertEqual([m for m, _ in fake.calls], [])

    def test_a_shared_account_is_never_used(self):
        self.people('jo@acme.com')
        fake = Graph(photos={'jo@acme.com': png(6)})
        self.step(fake, config={'accounts': [{**OUTLOOK, 'shared': True}]})
        self.assertEqual(fake.calls, [])

    def test_one_failing_account_never_stops_the_pass(self):
        fake = Graph()
        with mock.patch.object(ms_graph, 'grant', side_effect=RuntimeError('boom')):
            self.assertEqual(ms_photos.step(self.store.connect, self.config, None, NOW), (0, 0))

    def test_an_account_from_before_gets_one_quiet_to_do_that_closes_itself_once_reconnected(self):
        fake = Graph(granted={'User.Read', 'Mail.ReadWrite'}, offered=('User.ReadBasic.All', 'Contacts.Read'))
        self.step(fake)
        [card] = self.todos()
        self.assertEqual((card['title'], card['status'], card['origin']),
                         ('Reconnect Microsoft to show your colleagues’ and contacts’ photos', 'pending', 'machine'))
        self.assertEqual(card['reconnect'], {'provider': 'microsoft', 'email': 'sam@acme.com'})  # Reconnect opens its sign-in
        self.assertEqual(card['body'], 'Reconnect sam@acme.com to show colleagues’ and contacts’ photos. Read-only.')
        self.assertIsNone(card['source_line'])  # its text names the account: no "Signal · date" line
        with self.store.connect() as db:
            self.assertEqual([r[0] for r in db.execute('SELECT status FROM deliveries')], ['cancelled'])  # never pushed or mailed
        self.step(fake, now=later(minutes=10))
        self.assertEqual(len(self.todos()), 1)  # never a second one
        fake.granted, fake.offered = set(SCOPES), set()
        self.step(fake, now=later(minutes=20))
        self.assertEqual([c['status'] for c in self.todos()], ['completed'])  # reconnected: done within minutes
        fake.granted, fake.offered = {'User.Read', 'Mail.ReadWrite'}, {'Contacts.Read'}
        self.step(fake, now=later(days=2))
        self.assertEqual([c['status'] for c in self.todos()], ['completed'])  # created once, never again

    def test_not_needed_is_for_good(self):
        fake = Graph(granted={'User.Read', 'Mail.ReadWrite'}, offered=('Contacts.Read',))
        self.step(fake)
        [card] = self.todos()
        self.store.decide(card['id'], 'reject', '', 'd1', 'dashboard')
        self.step(fake, now=later(days=1, hours=1))
        self.assertEqual([c['status'] for c in self.todos()], ['rejected'])

    def test_an_organization_that_refused_them_is_never_asked(self):
        self.step(Graph(granted={'User.Read', 'Mail.ReadWrite'}, offered=()))
        self.assertEqual(self.todos(), [])

    def test_a_shared_account_is_never_asked(self):
        with self.store.connect() as db:
            workers.outlook_photos_ask(db, 'mail', ['Contacts.Read'], NOW)
        self.assertEqual(reconnect_asks.todos(self.store, {'accounts': [{**OUTLOOK, 'shared': True}]}), 0)
        self.assertEqual(reconnect_asks.todos(self.store, self.config), 1)

    def test_delete_permanently_forgets_the_asks(self):
        self.people('kim@acme.com')
        self.step(Graph())
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM ms_photo_asks').fetchone()[0], 1)
            a.graph.delete_person(db, 'email:kim@acme.com', tg.CONFIG, NOW)
            self.assertEqual(db.execute('SELECT count(*) FROM ms_photo_asks').fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()
