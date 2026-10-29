"""A to-do's source line and person chip never show a raw chat handle: a Slack DM ("#DM U0…") names the person, a
member id their name, a WhatsApp jid or a Telegram number is left out, and a lower-case Slack handle ("robin") gives
way to the name the person writes under elsewhere. Old cards stored the handle: they read right when shown."""
import collections
import datetime as dt
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('source_names_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph = a.graph
NOW = dt.datetime(2026, 10, 22, 12, tzinfo=dt.timezone.utc)
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.com'}, {'id': 'chat', 'service': 'whatsapp', 'email': 'Personal WhatsApp'},
                       {'id': 'tg', 'service': 'telegram'}, {'id': 'slack', 'service': 'slack', 'email': 'sam@acme.com', 'user_id': 'U0OWNER01'}]}
RAW = re.compile(r'[UWD][A-Z0-9]{8,}|#DM|@s\.whatsapp\.net|@g\.us|@lid|\d{6,}')


def event(account, source_id, kind, metadata, title='Hi'):
    return {'account_id': account, 'source_id': source_id, 'kind': kind, 'occurred_at': NOW.isoformat(), 'title': title, 'body': 'Can you send it?',
            'deleted': False, 'metadata': metadata}


SLACK_DM = event('slack', 'D0ROBIN01:1', 'slack.message', {'conversation_type': 'dm', 'channel_name': 'DM U0ROBIN01', 'channel_id': 'D0ROBIN01',
                                                          'user_id': 'U0ROBIN01'}, title='#DM U0ROBIN01: can you send it')
WHATSAPP = event('chat', 'w1', 'whatsapp.message', {'chat_id': '32470000001@g.us', 'from': '32470000002@s.whatsapp.net', 'from_me': False})
TELEGRAM = event('tg', 't1', 'telegram.message', {'chat_id': '700000001', 'from': '700000001', 'from_me': False})
MAIL = event('work', 'm1', 'gmail.message', {'from': 'Robin Example-Smith <robin@client.example>', 'to': 'sam@acme.com', 'labels': ['INBOX'],
                                             'message-id': '<1@x>', 'thread_id': 't1'}, title='Contract')


class SourceNames(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.now = a.now
        a.now = lambda: NOW.isoformat(); self.addCleanup(setattr, a, 'now', self.now)
        for e in (SLACK_DM, WHATSAPP, TELEGRAM, MAIL):
            self.store.commit_page(e['account_id'], {}, [e])
        with self.store.connect() as db:
            self.ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}

    def card(self, source_id):
        return self.store.suggest('k-' + source_id, 'Send it', 'They asked for it.', [self.ids[source_id]])['id']

    def shown(self):
        return {c['id']: c for c in self.store.snapshot([])['suggestions']}

    def test_lines_never_show_a_raw_handle(self):
        names = {'U0ROBIN01': 'Robin Example-Smith'}
        cases = {
            'Source: Slack from #DM U0ROBIN01 · Thu 22 Oct': 'Source: Slack DM with Robin Example-Smith · Thu 22 Oct',
            'Source: Slack from #DM U0NOBODY1 · Thu 22 Oct (+1 more)': 'Source: Slack · Thu 22 Oct (+1 more)',
            'Source: Slack from #DM Robin Example-Smith · Thu 22 Oct': 'Source: Slack DM with Robin Example-Smith · Thu 22 Oct',
            'Source: Slack from #DM robin · Thu 22 Oct': 'Source: Slack DM with Robin · Thu 22 Oct',
            'Source: Slack from U0ROBIN01 · Thu 22 Oct': 'Source: Slack from Robin Example-Smith · Thu 22 Oct',
            'Source: Slack from #general · Thu 22 Oct': 'Source: Slack from #general · Thu 22 Oct',  # a channel by its name stays
            'Source: WhatsApp from 32470000002@s.whatsapp.net · Thu 22 Oct': 'Source: WhatsApp · Thu 22 Oct',
            'Source: Telegram from 700000001 · Thu 22 Oct': 'Source: Telegram · Thu 22 Oct',
            'Source: email from Sam Lee · Thu 22 Oct': 'Source: email from Sam Lee · Thu 22 Oct',
        }
        for stored, want in cases.items():
            self.assertEqual(a.source_line_shown(stored, names), want)
        self.assertNotRegex(a.source_line_shown('Source: Slack from #DM U0ROBIN01 · Thu 22 Oct'), RAW)  # no names known (Telegram's card text)

    def test_the_dashboard_gets_names_for_slack_whatsapp_and_telegram_cards(self):
        cards = {s: self.card(s) for s in ('D0ROBIN01:1', 'w1', 't1')}
        with self.store.connect() as db:  # what an older Machine stored for these cards
            self.assertEqual(db.execute('SELECT source_line FROM suggestions WHERE id=?', (cards['D0ROBIN01:1'],)).fetchone()[0][:31],
                             'Source: Slack from #DM U0ROBIN0')
        shown = self.shown()
        self.assertEqual(shown[cards['D0ROBIN01:1']]['source_line'].split(' · ')[0], 'Source: Slack')  # no name known yet: just Slack
        self.store.remember_name('slack:U0ROBIN01', 'robin', 'robin@client.example')  # users.info: a lower-case handle as real_name
        with self.store.connect() as db:
            db.isolation_level = None
            graph.build(db, {**CONFIG, 'embeddings': {'model': 'test', 'dims': 4}}, NOW.isoformat())
        shown = self.shown()
        slack = shown[cards['D0ROBIN01:1']]
        self.assertEqual(slack['source_line'].split(' · ')[0], 'Source: Slack DM with Robin Example-Smith')
        self.assertEqual([p['name'] for p in slack['people']], ['Robin Example-Smith'])  # the chip: their name, not "robin"
        self.assertEqual(shown[cards['w1']]['source_line'].split(' · ')[0], 'Source: WhatsApp')
        self.assertEqual(shown[cards['t1']]['source_line'].split(' · ')[0], 'Source: Telegram')
        for card in (shown[c] for c in cards.values()):
            self.assertNotRegex(card['source_line'], RAW)
            for person in card.get('people') or ():
                self.assertNotRegex(person['name'], RAW)
                self.assertNotEqual(person['name'], person['name'].lower())

    def test_a_lower_case_handle_gives_way_to_a_name(self):
        C = collections.Counter
        self.assertEqual(graph.shown_name(C({'razvan': 3, 'Razvan-Ionut Example': 1})), 'Razvan-Ionut Example')
        self.assertEqual(graph.shown_name(C({'robin': 3, 'Robin': 2, 'Robin Example': 1})), 'Robin Example')
        self.assertEqual(graph.shown_name(C({'andrea': 3})), 'andrea')  # only a handle: a Fleet may know their name (incomplete_name)
        self.assertEqual((graph.handle_shown('andrea'), graph.handle_shown('steven example'), graph.handle_shown('Ann')), ('Andrea', 'Steven Example', 'Ann'))
        self.assertEqual(graph.shown_name(C({'Sam': 5, 'Samantha Jones': 1})), 'Sam')  # another name, not a fuller one
        self.assertEqual(graph.shown_name(C({'Ann Example': 4, 'Ann': 1})), 'Ann Example')


if __name__ == '__main__':
    unittest.main()
