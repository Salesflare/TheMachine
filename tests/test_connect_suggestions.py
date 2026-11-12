"""Connections, + Add: Suggested for you (machine/sources/suggest.py) and the groups below it (machine/sources/groups.py). A
suggestion needs a concrete signal the Machine already has, and none at all means no section; never a connected source."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

import assistant as a
import onboarding
from machine.sources import groups
from machine.sources.suggest import SHOWN, suggestions


def tile(name, connected=0, group='other'):
    return {'name': name, 'service': name, 'label': name.title(), 'group': group, 'connected': connected}


class Suggested(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.n = 0
        self.tiles = [tile(n) for n in ('stripe', 'zoom', 'google_meet', 'google_docs', 'github', 'trello', 'slack', 'intercom')]

    def event(self, kind, body='', metadata=None, days_ago=1):
        when = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days_ago)).isoformat()
        self.n += 1
        with self.store.connect() as db:
            db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) VALUES(?,?,?,?,?,?,?,?,?)',
                       ('acc', f's{self.n}', kind, when, 'Hi', body, json.dumps(metadata or {}), 'h', when))

    def mail(self, sender, n, days_ago=1):
        for _ in range(n):
            self.event('gmail.message', metadata={'from': f'Billing <invoices@{sender}>'}, days_ago=days_ago)

    def found(self, tiles=None, unfinished=()):
        with self.store.connect() as db:
            return suggestions(db, self.tiles if tiles is None else tiles, unfinished)

    def test_no_signal_means_no_suggestions(self):
        self.assertEqual(self.found(), [])
        self.event('gmail.message', body='Lunch on Friday?', metadata={'from': 'friend@example.org'})
        self.event('calendar.event', metadata={'location': 'Office'})
        self.assertEqual(self.found(), [])

    def test_weak_or_old_signals_are_not_enough(self):
        self.mail('stripe.com', 2)  # two mails: under the bar
        self.mail('stripe.com', 5, days_ago=60)  # older than 30 days
        self.mail('notstripe.com', 5)  # another domain that only contains the name
        for _ in range(2):
            self.event('calendar.event', metadata={'location': 'https://acme.zoom.us/j/123'})
        self.assertEqual(self.found(), [])

    def test_each_signal_with_its_count(self):
        self.mail('stripe.com', 4)
        for _ in range(3):
            self.event('calendar.event', metadata={'location': 'https://acme.zoom.us/j/123'})
        for _ in range(5):
            self.event('slack.message', body='See https://docs.google.com/document/d/abc for the plan')
        self.assertEqual(self.found(), [{'name': 'google_docs', 'why': 'links', 'count': 5}, {'name': 'stripe', 'why': 'mail', 'count': 4},
                                        {'name': 'zoom', 'why': 'meetings', 'count': 3}])

    def test_never_a_connected_source(self):
        self.mail('stripe.com', 6)
        tiles = [tile('stripe', connected=1), tile('zoom')]
        self.assertEqual(self.found(tiles, unfinished=['stripe']), [])

    def test_a_setup_that_did_not_finish_comes_first(self):
        self.mail('github.com', 8)
        self.assertEqual(self.found(unfinished=['trello', 'nope']), [{'name': 'trello', 'why': 'unfinished', 'count': 0},
                                                                    {'name': 'github', 'why': 'mail', 'count': 8}])

    def test_only_tiles_that_are_offered_and_at_most_a_few(self):
        self.mail('intercom.io', 3)
        self.assertEqual(self.found([tile('zoom')]), [])  # Intercom isn't a tile here
        for host in ('stripe.com', 'github.com', 'slack.com', 'intercom.io', 'trello.com'):
            self.mail(host, 3)
        self.assertEqual(len(self.found()), SHOWN)

    def test_connect_sources_carries_them_and_none_without_a_signal(self):
        app = object.__new__(a.App)
        app.config, app.store = {'accounts': [{'id': 'acc', 'service': 'gmail'}]}, self.store
        app.config_path = None
        self.assertEqual(app.action('connect_sources', {}, owner_dashboard=True)['suggested'], [])
        self.mail('github.com', 3)
        app._connect_suggested = None  # worked out again (it keeps one for 10 minutes)
        self.assertEqual(app.action('connect_sources', {}, owner_dashboard=True)['suggested'], [{'name': 'github', 'why': 'mail', 'count': 3}])


class Groups(unittest.TestCase):
    def setUp(self):
        onboarding._assistant = a

    def test_every_source_has_a_group_in_order(self):
        found = onboarding.catalog({})
        self.assertTrue(all(s['group'] in groups.GROUPS for s in found))
        of = {s['name']: s['group'] for s in found}
        self.assertEqual({n: of[n] for n in ('gmail', 'imap', 'calendar', 'slack', 'zoom', 'docs', 'stripe', 'crm', 'github', 'rss', 'gateway')},
                         {'gmail': 'mail', 'imap': 'mail', 'calendar': 'mail', 'slack': 'chat', 'zoom': 'meetings', 'docs': 'docs', 'stripe': 'customers',
                          'crm': 'customers', 'github': 'work', 'rss': 'other', 'gateway': 'other'})
        self.assertEqual(groups.GROUPS[-1], 'other')

    def test_an_unknown_source_is_other(self):
        self.assertEqual(groups.group_of('something_new'), 'other')
        self.assertEqual(groups.group_of('something_new', 'chat'), 'chat')  # a connector's own group
        self.assertEqual(groups.group_of('something_new', 'nonsense'), 'other')

    def test_the_dashboard_names_every_group(self):
        js = (Path(a.__file__).resolve().parent / 'dashboard' / 'connections-cards.js').read_text()
        line = next(x for x in js.splitlines() if x.startswith('const CONNECT_GROUPS='))
        self.assertEqual([k for k in groups.GROUPS], [p.split("'")[1] for p in line.split('[')[2:]])


if __name__ == '__main__':
    unittest.main()
