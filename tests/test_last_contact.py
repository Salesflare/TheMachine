"""Last contact is an interaction with someone, on its own date: a message to or from them or a meeting, also one email
of many the owner sent one by one. A to-do the owner made about someone is no contact, and a person with no contact
at all has no last contact."""
import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('last_contact_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph = a.graph
import knowledge  # noqa: E402

NOW = dt.datetime(2026, 10, 16, 12, tzinfo=dt.timezone.utc)
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.example'}]}
OWNER = 'Sam Stone <sam@acme.example>'
counter = iter(range(1, 10**6))


def at(days_ago, minute=0):
    return (NOW - dt.timedelta(days=days_ago, minutes=minute)).isoformat()


def day(days_ago):
    return (NOW - dt.timedelta(days=days_ago)).astimezone(graph.owner_tz({})).date().isoformat()


def mail(days_ago, sender, to, title, labels=('INBOX',), minute=0):
    n = next(counter)
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': at(days_ago, minute), 'title': title, 'body': 'Hello',
            'deleted': False, 'metadata': {'from': sender, 'to': to, 'cc': '', 'labels': list(labels), 'message-id': f'<{n}@x>', 'thread_id': f't{n}'}}


def todo(source_id, days_ago, node_id, name):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'owner.card', 'occurred_at': at(days_ago), 'title': 'Follow up', 'body': '', 'deleted': False,
            'metadata': {'about': [{'kind': 'person', 'id': node_id, 'name': name}]}}


class LastContact(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        clock = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        clock.start()
        self.addCleanup(clock.stop)

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])

    def build(self):
        with self.store.connect() as db:
            db.isolation_level = None
            return graph.build(db, {**CONFIG, 'embeddings': {'model': 'test', 'dims': 4}}, NOW.isoformat())

    def node(self, node_id):
        with self.store.connect() as db:
            row = db.execute('SELECT * FROM graph_nodes WHERE id=?', (node_id,)).fetchone()
            return graph.node_view(row) if row else None

    def test_a_to_do_made_about_someone_is_no_contact(self):
        self.add(todo('card1', 1, 'email:kim@vendor.example', 'Kim Vale'), todo('card2', 1, 'email:lou@other.example', 'Lou Vale'),
                 mail(30, OWNER, 'Kim Vale <kim@vendor.example>', 'Contract', ('SENT',)))
        self.build()
        self.assertEqual(self.node('email:kim@vendor.example')['last_at'], day(30))  # the mail, not the day the to-do was made
        lou = self.node('email:lou@other.example')
        self.assertIsNotNone(lou)  # still in the Graph
        self.assertIsNone(lou['last_at'])  # only a to-do about them: no contact
        with self.store.connect() as db:
            self.assertTrue(knowledge.last_contact(db, 'email:kim@vendor.example').startswith(day(30)))
            self.assertIsNone(knowledge.last_contact(db, 'email:lou@other.example'))
            org = db.execute("SELECT last_at FROM graph_nodes WHERE id='org:other.example'").fetchone()
            self.assertIsNone(org['last_at'])

    def test_a_rebuild_clears_a_to_do_day_stored_before(self):
        self.add(todo('card3', 2, 'email:lou@other.example', 'Lou Vale'))
        with self.store.connect() as db:  # what an older build stored: the day the to-do was made
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES('email:lou@other.example','person','Lou Vale',0.05,?,1,'{}')",
                       (day(2),))
        self.build()
        self.assertIsNone(self.node('email:lou@other.example')['last_at'])

    def test_each_email_the_owner_sent_one_by_one_is_contact(self):
        # The owner's own email is contact, also one of many with one subject sent one by one, answered or not
        self.add(*[mail(40, OWNER, f'Lead Number{i} <lead{i}@prospect.example>', 'A quick idea', ('SENT',), minute=i) for i in range(25)])
        self.build()
        node = self.node('email:lead5@prospect.example')
        self.assertEqual(node['last_at'], day(40))
        self.assertFalse(node['seen_only'])


if __name__ == '__main__':
    unittest.main()
