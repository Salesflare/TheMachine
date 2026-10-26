import importlib.util
from pathlib import Path
import tempfile
import time
import unittest

spec = importlib.util.spec_from_file_location('assistant_slack_first', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

DAY = 86400


class FirstImport(unittest.TestCase):
    """Slack allows about one history read a minute, so the first import reads where the activity is:
    the last day of active conversations first, then the rest of the week, quiet ones last."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.account = {'id': 'slack', 'user_id': 'U1', 'service': 'slack', 'boundary': 'work:Example',
                        'email': 'me@example.com', 'slack_host': 'example.slack.com'}
        now = time.time()
        ts = lambda age: f'{now - age:.6f}'
        self.conversations = [
            {'id': 'D0', 'is_im': True, 'user': 'U1'},             # my notes, nothing this week
            {'id': 'CA', 'name': 'aaa-announcements'},              # alphabetically first, but nobody reads it
            {'id': 'CB', 'name': 'busy'},                          # read an hour ago
            {'id': 'DA', 'is_im': True, 'user': 'U2'},             # message an hour ago
            {'id': 'DO', 'is_im': True, 'user': 'U3'},             # last message a month ago
            {'id': 'DW', 'is_im': True, 'user': 'U4'},             # last message three days ago
            {'id': 'GW', 'name': 'mpdm-team', 'is_mpim': True},    # read three days ago
        ]
        self.info = {'D0': {'latest': {'ts': ts(30 * DAY)}}, 'CA': {'last_read': ts(40 * DAY)},
                     'CB': {'last_read': ts(3600)}, 'DA': {'latest': {'ts': ts(3600)}},
                     'DO': {'latest': {'ts': ts(30 * DAY)}}, 'DW': {'latest': {'ts': ts(3 * DAY)}},
                     'GW': {'last_read': ts(3 * DAY)}}
        self.now = now

    def source(self, history=None):
        calls, info, conversations = [], self.info, self.conversations
        history = history or {}
        class Fake:
            def profile(self): pass
            def get(self, method, params):
                calls.append((method, params.copy()))
                if method == 'users.conversations':
                    return {'channels': conversations}
                if method == 'conversations.info':
                    return {'channel': info[params['channel']]}
                result = history.get(params['channel'])
                if isinstance(result, Exception):
                    raise result
                return {'messages': result or []}
        return Fake(), calls

    def run_all(self, source):
        for _ in range(100):
            if not a.sync_slack(self.store, {}, self.account, source)['more']:
                return
        self.fail('first import did not finish')

    def test_order_follows_activity_and_reads_the_last_day_first(self):
        source, calls = self.source({'DA': [{'ts': f'{self.now - 3600:.6f}', 'text': 'Can you send the contract?', 'user': 'U2'}]})
        a.sync_slack(self.store, {}, self.account, source)  # discovery
        self.assertEqual(self.store.checkpoint('slack')['phase'], 'triage')
        a.sync_slack(self.store, {}, self.account, source)  # one cheap look at every conversation
        self.assertEqual([m for m, _ in calls], ['users.conversations'] + ['conversations.info'] * 7)
        self.run_all(source)
        reads = [(p['channel'], float(p['oldest']), float(p['latest'])) for m, p in calls if m == 'conversations.history']
        self.assertEqual([r[0] for r in reads], ['DA', 'CB', 'DA', 'CB', 'DW', 'GW', 'CA'])
        # The last day first, for the active ones; then the older part of the week, without rereading the day.
        self.assertAlmostEqual(reads[0][1], self.now - DAY, delta=60)
        self.assertAlmostEqual(reads[2][1], self.now - 7 * DAY, delta=60)
        self.assertEqual(reads[2][2], reads[0][1])
        self.assertAlmostEqual(reads[4][1], self.now - 7 * DAY, delta=60)  # this week's: the whole window at once
        self.assertNotIn('DO', [r[0] for r in reads])  # a direct message with nothing this week isn't read
        self.assertNotIn('D0', [r[0] for r in reads])
        state = self.store.checkpoint('slack')
        self.assertEqual(state['mode'], 'incremental')
        self.assertNotIn('step', state)
        channels = {c['id']: c for c in state['channels']}
        self.assertTrue(all(c.get('last_scan') for c in channels.values()))
        self.assertNotIn('deepen', channels['DA'])
        self.assertGreater(float(channels['DA']['last_scan']), self.now - 60)  # the deeper read didn't move it back
        self.assertEqual(state['channels'][0]['name'], 'My notes')
        self.assertEqual(len(self.store.events(['slack'])), 1)

    def test_card_shows_where_the_first_import_is(self):
        source, _ = self.source()
        a.sync_slack(self.store, {}, self.account, source)
        a.sync_slack(self.store, {}, self.account, source)
        progress = lambda: self.store.snapshot([self.account])['connectors'][0]['first_import']
        self.assertEqual(progress(), {'step': 'recent', 'done': 0, 'total': 2, 'quiet': 1})
        a.sync_slack(self.store, {}, self.account, source)
        self.assertEqual(progress(), {'step': 'recent', 'done': 1, 'total': 2, 'quiet': 1})
        a.sync_slack(self.store, {}, self.account, source)
        self.assertEqual(progress(), {'step': 'deepen', 'done': 0, 'total': 4, 'quiet': 1})
        self.run_all(source)
        self.assertIsNone(progress())

    def test_unavailable_conversation_is_marked_and_the_import_moves_on(self):
        source, calls = self.source({'DA': a.SourceError('slack_not_in_channel:conversations.history')})
        a.sync_slack(self.store, {}, self.account, source)
        a.sync_slack(self.store, {}, self.account, source)
        with self.assertRaises(a.SourceError):
            a.sync_slack(self.store, {}, self.account, source)
        state = self.store.checkpoint('slack')
        self.assertEqual({c['id']: c for c in state['channels']}['DA']['error'], 'slack_not_in_channel')
        a.sync_slack(self.store, {}, self.account, source)
        self.assertEqual(calls[-1][1]['channel'], 'CB')

    def test_regular_rounds_keep_their_state_and_only_change_order(self):
        old = f'{self.now - 40 * DAY:.6f}'
        channels = [{'id': 'CA', 'name': 'aaa', 'type': 'channel', 'threads': [], 'last_scan': old, 'last_activity': float(old)},
                    {'id': 'DA', 'name': 'DM U2', 'type': 'dm', 'threads': [], 'last_scan': f'{self.now:.6f}',
                     'last_activity': self.now - 3600, 'next_full': self.now + DAY}]
        self.store.commit_page('slack', {'mode': 'incremental', 'phase': 'discover', 'channels': channels, 'index': 0,
                                         'after': f'{self.now - 90 * DAY:.6f}', 'next_discovery': 0}, [])
        self.conversations = [{'id': 'CA', 'name': 'aaa'}, {'id': 'DA', 'is_im': True, 'user': 'U2'}]
        source, calls = self.source()
        a.sync_slack(self.store, {}, self.account, source)
        state = self.store.checkpoint('slack')
        self.assertEqual([m for m, _ in calls], ['users.conversations'])
        self.assertEqual([c['id'] for c in state['channels']], ['DA', 'CA'])
        self.assertEqual(state['channels'][1]['last_scan'], old)
        self.assertEqual((state['mode'], state['phase']), ('incremental', 'scan'))
        self.assertNotIn('step', state)

    def test_first_import_begun_in_name_order_continues_by_activity(self):
        done = {'id': 'CA', 'name': 'aaa-announcements', 'type': 'channel', 'threads': [], 'last_scan': f'{self.now - 600:.6f}'}
        rest = [{'id': c, 'name': n, 'type': k, 'threads': []} for c, n, k in
                [('CB', 'busy', 'channel'), ('DA', 'DM U2', 'dm'), ('DO', 'DM U3', 'dm')]]
        self.store.commit_page('slack', {'mode': 'bootstrap', 'phase': 'scan', 'channels': [done] + rest, 'index': 1,
                                         'after': f'{self.now - 7 * DAY:.6f}', 'next_discovery': self.now + DAY}, [])
        fake, calls = self.source()
        class Live(a.Slack):  # the old order is only left on a real connection
            def __init__(self): self.account = {'user_id': 'U1'}
            def profile(self): pass
            def get(self, method, params=None): return {} if method == 'users.info' else fake.get(method, params)
        self.run_all(Live())
        reads = [p['channel'] for m, p in calls if m == 'conversations.history']
        self.assertEqual(reads, ['DA', 'CB', 'DA', 'CB'])  # CA was already read; DO has nothing this week
        state = self.store.checkpoint('slack')
        self.assertEqual(state['mode'], 'incremental')
        self.assertEqual({c['id']: c for c in state['channels']}['CA']['last_scan'], done['last_scan'])


if __name__ == '__main__':
    unittest.main()
