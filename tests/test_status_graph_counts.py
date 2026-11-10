"""The sidebar's Graph counts come with the status (graph_counts), the same numbers the Graph overview has: a page load
used to fetch the whole overview (some 600 KB on a busy Machine) just for them. The dashboard side:
test_graph_counts_status_dashboard.mjs."""
import datetime as dt
import tempfile
import unittest
from pathlib import Path

import assistant as a
import graph

NOW = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
WORK = {'id': 'work', 'email': 'owner@acme.example', 'service': 'gmail', 'boundary': 'work:Acme'}


def mail(n, sender):
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(days=n)).isoformat(),
            'title': f'Mail {n}', 'body': 'Hello', 'deleted': False,
            'metadata': {'from': sender, 'to': 'owner@acme.example', 'labels': ['INBOX'], 'message-id': f'<{n}@x>', 'thread_id': f't{n}'}}


class StatusGraphCounts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store, self.app.config_path, self.app.config = self.store, None, {'accounts': [WORK]}

    def test_status_has_the_counts_the_graph_overview_has(self):
        self.assertEqual(self.app.action('status', {'full': True})['graph_counts'], {'person': 0, 'org': 0, 'project': 0})
        self.store.commit_page('work', {}, [mail(1, 'Sam Lee <sam@client.example>'), mail(2, 'Kim Ito <kim@other.example>')])
        with self.store.connect() as db:
            db.isolation_level = None
            graph.build(db, {'accounts': [WORK]}, NOW.isoformat())
        counts = self.app.action('status', {'full': True})['graph_counts']
        with self.store.connect() as db:
            overview = graph.overview(db)['counts']
        self.assertEqual(counts, overview)
        self.assertGreaterEqual(counts['person'], 2)

    def test_the_agents_compact_status_leaves_them_out(self):
        self.assertNotIn('graph_counts', self.app.action('status', {}))


if __name__ == '__main__':
    unittest.main()
