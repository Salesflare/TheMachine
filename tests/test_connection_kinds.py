"""Connections by kind, registry-wide: every source maps to exactly one kind (machine/sources/groups.py), every connected
one shows in its kind's list at the top (also one with no card of its own there: Codex, GBrain, Google Docs on the
owner's Google sign-in), and each disconnected account shows under its own kind only (names.disconnected_rows).
tests/test_connection_kinds_dashboard.mjs checks the same on the page."""
import re
import types
import unittest
from pathlib import Path

import onboarding
from machine import names
from machine.sources import connectors, groups
from machine.store import views

ROOT = Path(__file__).resolve().parent.parent
JS = (ROOT / 'dashboard' / 'connections-cards.js').read_text(encoding='utf-8')


class EverySourceOneKind(unittest.TestCase):
    def test_every_source_in_the_registry_has_exactly_one_kind(self):
        found = onboarding.catalog({})
        self.assertTrue(found)
        for s in found:
            with self.subTest(s['name']):
                self.assertIn(s['group'], groups.GROUPS)
                self.assertEqual(views.source_group(s['service']), s['group'], 'its card sits where + Add lists it')
        self.assertTrue(set(groups.GROUP_OF.values()) <= set(groups.GROUPS))
        # every connector plugin too, and the sources + Add lists beside the catalog
        for service in sorted(connectors.connector_services()):
            with self.subTest(service):
                self.assertIn(views.source_group(service), groups.GROUPS)
        self.assertEqual(groups.group_of('google_docs'), 'docs')
        self.assertIn("add('work','Codex'", JS)
        self.assertIn("add('other','GBrain'", JS)

    def test_a_connected_source_without_a_card_in_its_kind_gets_a_row_there(self):
        # + Add notes each connected tile (its kind and source); one no card of its kind covers becomes a row at the top
        self.assertRegex(JS, r'if\(x\?\.connected\)on\.push\(\[g,x\]\)')
        self.assertRegex(JS, r"on\.filter\(\(\[g,x\]\)=>!\(state\.connectors\|\|\[\]\)\.some\(c=>healthGroup\(c\)===g&&c\.service===x\.service\)\)")
        for tile in ('codexSource()', "{name:'gbrain'", "{...x,label:t('Teams meetings')}", "x.last,x)"):
            with self.subTest(tile):
                self.assertIn(tile, JS, 'every tile hands its source to add()')
        self.assertIn('${connExtra.map(e=>', JS)


class GoogleDocsOnAGoogleSignin(unittest.TestCase):
    ACCOUNT = {'id': 'work-gmail', 'transport': 'gog', 'email': 'alex@acme.example', 'client': 'default'}

    def setUp(self):
        connectors.GOG_DOCS.clear()
        self.addCleanup(connectors.GOG_DOCS.clear)
        self.asked = []
        self.scopes = {'create'}
        plugin = types.SimpleNamespace(writes_on=lambda config, account, helpers: self.asked.append(account['id']) or set(self.scopes))
        original = connectors.load_connector
        connectors.load_connector = lambda name: plugin if name == 'docs' else original(name)
        self.addCleanup(setattr, connectors, 'load_connector', original)

    def test_a_google_signin_with_drive_is_google_docs_under_docs_and_files(self):
        [found] = connectors.gog_docs_sources({'accounts': [self.ACCOUNT]})
        self.assertEqual((found['name'], found['group'], found['connected'], found['via']), ('google_docs', 'docs', 1, ['work-gmail']))
        self.assertEqual(found['label'], 'Google Docs')

    def test_without_drive_or_shared_or_with_actions_off_it_is_not_listed(self):
        self.scopes = set()
        self.assertEqual(connectors.gog_docs_sources({'accounts': [self.ACCOUNT]}), [])
        self.scopes = {'create'}
        connectors.GOG_DOCS.clear()
        for account in ({**self.ACCOUNT, 'shared': {'fleet_name': 'Acme'}}, {**self.ACCOUNT, 'actions': False},
                        {**self.ACCOUNT, 'transport': 'broker'}, {**self.ACCOUNT, 'service': 'calendar'}):
            self.assertEqual(connectors.gog_docs_sources({'accounts': [account]}), [])

    def test_it_asks_gog_at_most_every_ten_minutes(self):
        clock = [1000.0]
        for _ in range(3):
            connectors.gog_docs_sources({'accounts': [self.ACCOUNT]}, clock=lambda: clock[0])
        self.assertEqual(self.asked, ['work-gmail'])
        clock[0] += connectors.GOG_DOCS_SECONDS + 1
        connectors.gog_docs_sources({'accounts': [self.ACCOUNT]}, clock=lambda: clock[0])
        self.assertEqual(self.asked, ['work-gmail', 'work-gmail'])

    def test_its_tile_opens_the_card_it_rests_on(self):
        self.assertIn('if(x.via)return html`<button type="button" class="connect-source" data-connect-card="${x.via[0]}">', JS)
        self.assertIn('x.via?x.via.includes(c.id)', JS)


class DisconnectedUnderItsOwnKind(unittest.TestCase):
    def test_every_signin_provider_has_its_kind(self):
        kinds = {}
        for provider in names.SIGNINS:
            [row] = names.disconnected_rows([{'provider': provider, 'email': 'sam@acme.example', 'state': 'removed', 'at': '2026-11-01T10:00:00+00:00'}])
            kinds[provider] = row['group']
        self.assertTrue(set(kinds.values()) <= set(groups.GROUPS) - {'other'})
        self.assertEqual(kinds, {'google': 'mail', 'google_meet': 'mail', 'google_docs': 'mail', 'microsoft': 'mail', 'zoom': 'meetings',
                                 'stripe': 'customers', 'slack': 'chat', 'salesforce': 'customers'})
        self.assertEqual(names.SIGNIN_KINDS, {p: groups.group_of(s) for p, s in names.SIGNIN_SOURCES.items()})

    def test_the_page_shows_each_under_its_own_kind_only(self):
        self.assertIn('(state.disconnected||[]).filter(r=>r.group===connShown)', JS)
        panels = (ROOT / 'dashboard' / 'connections-panels.html').read_text(encoding='utf-8')
        self.assertRegex(panels, r'id="disconnected" data-health-for="cat"')
        self.assertNotRegex(panels, r'id="disconnected" data-health-for="[^"]*(mail|other)')


class OneDriveMark(unittest.TestCase):
    def test_the_onedrive_row_has_onedrives_own_mark(self):
        svg = (ROOT / 'dashboard' / 'logos' / 'mono' / 'docs.svg').read_text(encoding='utf-8')
        color = (ROOT / 'dashboard' / 'logos' / 'docs.svg').read_text(encoding='utf-8')
        # its two clouds, as in the colored OneDrive logo + Add shows, not a generic cloud
        front = re.search(r'd="(M14\.38 37\.97[^"]+)"', color).group(1)
        self.assertIn(front, svg)
        self.assertIn('clip-path', svg)


if __name__ == '__main__':
    unittest.main()
