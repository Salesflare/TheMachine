"""A connection card's title and subtitle (Connections), for every kind of connection there is: the built-in ones, every
connector file and everything + Add offers, read from the registry, so a new connector is checked the day it lands.

Each kind is tried with the accounts it can come with: a bare one (only an id like personal-signal and a device
boundary like personal:signal), one with a config key as its name, one with an address, one whose provider told its
name, and two of the same kind. Its title is never an id or a config key; its subtitle never names the provider or
its kind again, never a raw key, and never repeats a word of the title."""
import importlib.util
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location('card_names_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import onboarding  # noqa: E402
from machine import names  # noqa: E402
from machine.sources import connectors  # noqa: E402

SLUG = re.compile(r'[a-z0-9]+(?:[-_.][a-z0-9]+)+|[a-z0-9_-]+')
SCOPE = {'work', 'personal'}
LABELS = {'work:acme.com': 'Work · acme.com', 'work:Acme': 'Work · Acme'}


def registry():
    """Every kind of connection: names.SERVICES, the connector files and what + Add lists."""
    kinds = set(names.SERVICES) | set(connectors.connector_services())
    kinds |= {onboarding.SERVICES.get(n, n) for n in onboarding.sources()}
    return sorted(kinds)


def fixtures(service):
    """The accounts a kind can come with (made-up)."""
    base = {'service': service, 'transport': 'api'}
    return [
        ('bare', {**base, 'id': f'personal-{service}', 'boundary': f'personal:{service}'}, [], {}),
        ('key as name', {**base, 'id': f'work-{service}', 'display_name': f'work-{service}', 'boundary': 'work:acme.com'}, [], {}),
        ('kind as name', {**base, 'id': f'{service}-2', 'display_name': service, 'boundary': 'personal:me'}, [], {}),
        ('address', {**base, 'id': f'{service}-mail', 'email': 'sam@acme.com', 'boundary': 'work:acme.com'}, [], {}),
        ('handle', {**base, 'id': f'{service}-h', 'handle': 'acmehq', 'login': 'acmehq', 'boundary': 'work:Acme'}, [], {}),
        ('named', {**base, 'id': f'{service}-n', 'display_name': 'Acme on ' + (names.SERVICES.get(service) or service), 'boundary': 'work:Acme'}, [], {}),
        ('plain work', {**base, 'id': f'{service}-w', 'display_name': names.SERVICES.get(service) or service, 'boundary': 'work'}, [], {}),
        ('told', {**base, 'id': f'{service}-t', 'boundary': f'personal:{service}'}, [], {'account_name': 'Sam Example'}),
        ('second', {**base, 'id': f'{service}-b', 'boundary': 'personal:me'}, [{**base, 'id': f'{service}-a'}, {**base, 'id': f'{service}-b'}], {}),
    ]


class CardNames(unittest.TestCase):
    def test_the_registry_holds_every_connector(self):
        kinds = registry()
        for service in ('gmail', 'calendar', 'slack', 'signal', 'telegram', 'whatsapp', 'x', 'intercom', 'docs', 'teams', 'zoom', 'salesflare'):
            self.assertIn(service, kinds)
        self.assertGreater(len(kinds), 25)

    def test_every_kind_reads_as_a_name_with_a_plain_subtitle(self):
        for service in registry():
            kinds = names.kind_words(service)
            for case, account, accounts, state in fixtures(service):
                with self.subTest(service=service, case=case):
                    card = names.account_card(account, accounts or [account], state, LABELS)
                    title, subtitle = card['card_title'], card['card_subtitle']
                    self.assertTrue(title.strip())
                    self.assertNotEqual(title, account['id'])
                    self.assertFalse(SLUG.fullmatch(title) and '@' not in title, f'{title!r} reads as a key')
                    parts = subtitle.split(' · ') if subtitle else []
                    self.assertEqual(len(parts), len(set(parts)), subtitle)
                    self.assertNotIn(parts[0] if parts else '', ('work', 'personal'), f'{subtitle!r}: Work and Personal read capitalized')
                    for part in parts:
                        self.assertNotEqual(part, service)
                        self.assertFalse(SLUG.fullmatch(part) and '@' not in part and part not in ('acme.com',), f'{part!r} in {subtitle!r} is a raw key')
                        self.assertFalse(names.words(part) & kinds - SCOPE, f'{subtitle!r} names the kind again')
                    shared = (names.words(title) & names.words(subtitle)) - SCOPE
                    self.assertFalse(shared, f'{title!r} / {subtitle!r} repeat {shared}')
                    self.assertLessEqual(len(parts), 3, subtitle)  # Work (· its company) and one detail at most
                    self.assertIn(parts[0] if parts else 'Work', ('Work', 'Personal'), subtitle)

    def test_what_the_owner_saw(self):
        accounts = [{'id': 'personal-signal', 'service': 'signal', 'boundary': 'personal:signal', 'transport': 'signal_mirror'},
                    {'id': 'telegram-telegram', 'service': 'telegram', 'boundary': 'personal:telegram', 'display_name': 'Sam’s Telegram'},
                    {'id': 'acme-x', 'service': 'x', 'boundary': 'work:acme.com', 'display_name': 'Acme on X', 'handle': 'acme'},
                    {'id': 'machine-x', 'service': 'x', 'boundary': 'work:BrightLabs', 'display_name': 'Bright Labs on X', 'handle': 'HeyBrightLabs'}]
        card = lambda i, state=None: names.account_card(accounts[i], accounts, state, {'work:acme.com': 'Work · acme.com', 'work:BrightLabs': 'Work · BrightLabs'})
        self.assertEqual(card(0), {'card_title': 'Signal', 'card_subtitle': 'Personal'})
        self.assertEqual(card(0, {'account_name': 'Sam Example'}), {'card_title': 'Sam’s Signal', 'card_subtitle': 'Personal'})
        self.assertEqual(card(1), {'card_title': 'Sam’s Telegram', 'card_subtitle': 'Personal'})
        self.assertEqual(card(2), {'card_title': 'Acme', 'card_subtitle': 'Work'})
        self.assertEqual(card(2, {'account_name': 'Acme Inc'}), {'card_title': 'Acme Inc', 'card_subtitle': 'Work'})
        self.assertEqual(card(3), {'card_title': 'Bright Labs', 'card_subtitle': 'Work'})  # @HeyBrightLabs says the title again
        named = {**accounts[3], 'display_name': 'Robin Example', 'handle': 'rex'}
        self.assertEqual(names.account_card(named, [named], None, {}), {'card_title': 'Robin Example', 'card_subtitle': 'Work · BrightLabs · @rex'})
        oddly = {'id': 'openclaw-gateway', 'service': 'gateway', 'boundary': 'owner:system', 'email': 'the-machine'}
        self.assertEqual(names.account_card(oddly, [oddly]), {'card_title': 'Machine health', 'card_subtitle': ''})

    def test_a_detail_shows_only_what_the_title_does_not(self):
        cal = {'id': 'family-calendar', 'service': 'calendar', 'boundary': 'personal:Robin', 'display_name': 'Robin’s calendar', 'email': 'sam@acme.com'}
        self.assertEqual(names.account_card(cal, [cal]), {'card_title': 'Robin’s calendar', 'card_subtitle': 'Personal · sam@acme.com'})
        mail = {'id': 'work-gmail', 'boundary': 'work:Acme', 'email': 'sam@acme.com'}
        self.assertEqual(names.account_card(mail, [mail], None, {'work:Acme': 'Work · Acme'}), {'card_title': 'sam@acme.com', 'card_subtitle': 'Work'})
        other = {'id': 'work-gmail', 'boundary': 'work:Globex', 'email': 'sam@acme.com'}
        self.assertEqual(names.account_card(other, [other], None, {'work:Globex': 'Work · Globex'}), {'card_title': 'sam@acme.com', 'card_subtitle': 'Work · Globex'})
        # calendars and Exchange on a plain work boundary: never "Calendar · work" or "Exchange · work"
        for service, title in (('exchange', 'Exchange'), ('calendar', 'Google Calendar'), ('ics', 'Other calendar'), ('caldav', 'Team calendar')):
            plain = {'id': f'work-{service}', 'service': service, 'boundary': 'work', 'display_name': title}
            self.assertEqual(names.account_card(plain, [plain]), {'card_title': title, 'card_subtitle': 'Work'}, service)
        # a workspace named after its company: the company is in the title, so the subtitle is just Work
        desk = {'id': 'intercom', 'service': 'intercom', 'boundary': 'work:Acme', 'display_name': 'Acme'}
        self.assertEqual(names.account_card(desk, [desk], None, {'work:Acme': 'Work · Acme'}), {'card_title': 'Acme', 'card_subtitle': 'Work'})
        health = {'id': 'openclaw-gateway', 'service': 'gateway', 'boundary': 'owner:system'}
        self.assertEqual(names.account_card(health, [health]), {'card_title': 'Machine health', 'card_subtitle': ''})


def page(accounts, labels=None):
    """The cards Connections shows for these accounts, as status makes them: each named, then told apart on its tab."""
    from machine.store import views
    cards = [{'id': x['id'], 'group': views.source_group(names.account_service(x)),
              **names.account_card(x, accounts, None, labels or LABELS)} for x in accounts]
    return names.tell_apart(cards, accounts)


class NeverTheSame(unittest.TestCase):
    def assertApart(self, cards):
        seen = {}
        for card in cards:
            key = (names.page_tab(card['group']), card['card_title'], card['card_subtitle'])
            self.assertNotIn(key, seen, f'{card["id"]} and {seen.get(key)} both read {key[1:]!r}')
            seen[key] = card['id']

    def test_no_two_cards_on_a_tab_read_the_same_for_any_kind(self):
        # every kind twice under one name, as two workspaces of one company would be, and once more bare
        accounts = []
        for service in registry():
            base = {'service': service, 'transport': 'api', 'boundary': 'work:Acme', 'display_name': 'Acme'}
            accounts += [{**base, 'id': f'{service}-1', 'email': 'sam@acme.com'}, {**base, 'id': f'{service}-2', 'email': 'robin@acme.com'},
                         {**base, 'id': f'{service}-3'}, {'service': service, 'transport': 'api', 'id': f'{service}-bare', 'boundary': 'personal:me'}]
        cards = page(accounts)
        self.assertApart(cards)
        # nothing of their own differs: told apart all the same
        twins = [{'id': f'slack-{n}', 'service': 'slack', 'boundary': 'work:Acme', 'display_name': 'Acme'} for n in (1, 2)]
        self.assertApart(page(twins))

    def test_what_the_owner_saw(self):
        slack = {'id': 'acme-slack', 'service': 'slack', 'boundary': 'work:Acme', 'display_name': 'Acme', 'email': 'sam@acme.com', 'slack_host': 'acme.slack.com'}
        x = {'id': 'acme-x', 'service': 'x', 'boundary': 'work:Acme', 'display_name': 'Acme on X', 'email': '@acme', 'handle': 'acme'}
        desk = {'id': 'acme-intercom', 'service': 'intercom', 'boundary': 'work:Acme', 'display_name': 'Acme', 'workspace_name': 'Acme'}
        shown = {c['id']: (c['card_title'], c['card_subtitle']) for c in page([slack, x, desk])}
        # Slack and X on Chat: the provider; Intercom alone with that name on Other sources: as it was
        self.assertEqual(shown, {'acme-slack': ('Acme', 'Work · Slack'), 'acme-x': ('Acme', 'Work · X'), 'acme-intercom': ('Acme', 'Work')})
        # two workspaces of one name: each by its address
        eu = {**slack, 'id': 'acme-eu-slack', 'slack_host': 'acme-eu.slack.com'}
        shown = {c['id']: c['card_subtitle'] for c in page([slack, eu])}
        self.assertEqual(shown, {'acme-slack': 'Work · acme.slack.com', 'acme-eu-slack': 'Work · acme-eu.slack.com'})
        # without one: by who is signed in
        shown = {c['id']: c['card_subtitle'] for c in page([{**slack, 'slack_host': ''}, {**eu, 'slack_host': '', 'email': 'robin@acme.com'}])}
        self.assertEqual(shown, {'acme-slack': 'Work · sam@acme.com', 'acme-eu-slack': 'Work · robin@acme.com'})
        # the same address on Email and Calendar: their own tabs tell them apart already
        mail = {'id': 'work-mail', 'boundary': 'work:Acme', 'email': 'sam@acme.com'}
        cal = {**mail, 'id': 'work-cal', 'service': 'calendar'}
        self.assertEqual([c['card_subtitle'] for c in page([mail, cal])], ['Work', 'Work'])

    def test_a_github_card_reads_its_name_else_its_handle(self):
        hub = {'id': 'github', 'service': 'github', 'transport': 'gh', 'boundary': 'work:Acme', 'display_name': 'GitHub', 'email': 'SamExample', 'login': 'SamExample'}
        self.assertEqual(names.account_card(hub, [hub], None, LABELS), {'card_title': '@SamExample', 'card_subtitle': 'Work · Acme'})
        self.assertEqual(names.account_card(hub, [hub], {'account_name': 'Sam Example'}, LABELS), {'card_title': 'Sam Example', 'card_subtitle': 'Work · Acme'})
        named = {**hub, 'login': 'robin-x', 'email': 'robin-x'}  # a login that looks like a key is still a handle
        self.assertEqual(names.account_card(named, [named], None, LABELS)['card_title'], '@robin-x')
        self.assertEqual(names.account_card(named, [named], {'account_name': 'Sam Example'}, LABELS)['card_subtitle'], 'Work · Acme · @robin-x')


class StatusCarriesThem(unittest.TestCase):
    def test_the_card_shows_what_the_machine_named_it(self):
        js = (ROOT / 'dashboard' / 'connections-cards.js').read_text(encoding='utf-8')
        self.assertIn('const connTitle=c=>c.card_title||', js)
        # the row: its name, then the subtitle, which is only ever the Machine's: a page-side fallback once read "Acme"
        # over "Work · Acme"
        row = '<span class="conn-name">${connTitle(c)}</span><small>${c.card_subtitle?html`<span class="conn-sub">${c.card_subtitle}</span> · `:\'\'}'
        self.assertIn(row, js)
        self.assertNotIn('connSubtitle', js)
        self.assertIn('display_names.account_card(', (ROOT / 'machine' / 'app' / 'status.py').read_text(encoding='utf-8'))

    def test_status_gives_each_card_its_title_and_subtitle(self):
        import tempfile
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        app = object.__new__(a.App)
        signal = {'id': 'personal-signal', 'service': 'signal', 'boundary': 'personal:signal', 'transport': 'signal_mirror'}
        mail = {'id': 'work', 'email': 'owner@acme.example', 'service': 'gmail', 'boundary': 'work:Acme'}
        app.store, app.config_path, app.config = a.Store(Path(temp.name) / 'events.sqlite'), None, {'accounts': [mail, signal]}
        app.store.commit_page('personal-signal', {'account_name': 'Sam Example'}, [])
        cards = {c['id']: (c.get('card_title'), c.get('card_subtitle')) for c in app.status_built(None)['connectors']}
        self.assertEqual(cards, {'work': ('owner@acme.example', 'Work'), 'personal-signal': ('Sam’s Signal', 'Personal')})
        from machine.app import status
        self.assertEqual(status.checkpoint_state({'state': '{"account_name": "Sam Example"}'}), {'account_name': 'Sam Example'})
        self.assertEqual(status.checkpoint_state({'state': 'not json'}), {})
        self.assertEqual(status.checkpoint_state({}), {})


if __name__ == '__main__':
    unittest.main()
