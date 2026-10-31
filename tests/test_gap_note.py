"""What we don't know (gap_note.py): the facts a preparation gets about the people on a to-do, computed from synced
signals only, and the one short line the to-do shows where it helps."""
import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('gap_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph, gap_note, enrichment = a.graph, a.gap_note, a.enrichment
NOW = dt.datetime(2026, 10, 31, 12, tzinfo=dt.timezone.utc)
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.com'}]}
counter = iter(range(1, 10**6))


def mail(days_ago, sender, to, labels=('INBOX',), thread=None):
    n = next(counter)
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(days=days_ago)).isoformat(),
            'title': f'Mail {n}', 'body': 'Hello', 'deleted': False,
            'metadata': {'from': sender, 'to': to, 'labels': list(labels), 'message-id': f'<{n}@x>', 'thread_id': thread or f't{n}'}}


class GapNote(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.owner_user_ids = set()
        self.store.accounts = CONFIG['accounts']
        self.app = object.__new__(a.App); self.app.store = self.store; self.app.config = CONFIG
        self.now = a.now
        a.now = lambda: NOW.isoformat(); self.addCleanup(setattr, a, 'now', self.now)

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])
        with self.store.connect() as db:
            return [db.execute('SELECT id FROM events WHERE source_id=?', (e['source_id'],)).fetchone()[0] for e in events]

    def build(self):
        with self.store.connect() as db:
            db.isolation_level = None
            graph.build(db, {**CONFIG, 'embeddings': {'model': 'test', 'dims': 4}}, NOW.isoformat())

    def card(self, card_id):
        with self.store.connect() as db:  # what the dashboard gets for it (the status payload's card_views)
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (card_id,)).fetchone())
            self.store.card_views(db, [row], jobs=False)
        return row

    def test_last_contact_from_them_twelve_days_ago_nothing_since(self):
        ask, = self.add(mail(12, 'Ann Example <ann@client.com>', 'sam@acme.com', thread='deal'))
        self.build()
        card = self.store.suggest('ann-1', 'Answer Ann', 'Ann asked about pricing.', [ask])
        lines = self.app.gap_lines(card['id'])
        self.assertIn("What we don't know", lines)
        self.assertIn('Last contact 12 days ago by email; nothing since.', lines)  # the example the result may use
        self.assertIn('- Ann Example: last contact Mon, Oct 19 (12 days ago) by email, from them; nothing synced since', lines)
        self.assertNotIn('not synced here', lines)  # no sign she uses another channel
        self.assertNotIn('gap', self.card(card['id']))  # twelve days, and she wrote last: no line on the to-do yet

    def test_the_owner_wrote_last_with_no_reply_and_promises_both_ways(self):
        ask, reply = self.add(mail(9, 'Ann Example <ann@client.com>', 'sam@acme.com', thread='deal'),
                              mail(4, 'Sam <sam@acme.com>', 'Ann Example <ann@client.com>', ('SENT',), thread='deal'))
        self.app.action('promise', {'direction': 'mine', 'event_id': reply, 'who': 'Ann', 'what': 'send the deck', 'due': '2026-11-03'})
        self.app.action('promise', {'direction': 'theirs', 'event_id': ask, 'who': 'Ann', 'what': 'sign the contract'})
        self.build()
        card = self.store.suggest('ann-1', 'Follow up with Ann', 'No answer yet.', [ask])
        lines = self.app.gap_lines(card['id'])
        self.assertIn('last contact Tue, Oct 27 (4 days ago) by email, from the owner; no reply synced since (their last message: Thu, Oct 22 by email)', lines)
        self.assertIn('open: the owner promised to send the deck by Tue, Nov 3', lines)
        self.assertIn('open: they promised to sign the contract', lines)
        # Waiting on her is what this to-do says already: no line. With a number for her and no WhatsApp here, the line
        # says where an answer may be that this Machine can't see.
        self.assertNotIn('gap', self.card(card['id']))
        with self.store.connect() as db:
            db.execute(enrichment.FACT_SCHEMA)
            db.execute("INSERT INTO person_facts(identifier,field,value,rank,source,seen_at) VALUES('email:ann@client.com','phone','+32 470 00 00 00',2,'google',?)", (NOW.isoformat(),))
        self.assertEqual(self.card(card['id'])['gap'], {'name': 'Ann Example', 'days': 4, 'channel': 'email', 'wrote_last': True, 'unsynced': ['WhatsApp']})
        # Done or dismissed to-dos get no line
        self.store.decide(card['id'], 'complete', '', 'd-done', 'dashboard')
        with self.store.connect() as db:
            done = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (card['id'],)).fetchone())
            self.store.card_views(db, [done], jobs=False)
        self.assertNotIn('gap', done)

    def test_a_quiet_contact_and_channels_this_machine_does_not_sync(self):
        old, = self.add(mail(20, 'Ann Example <ann@client.com>', 'sam@acme.com', thread='deal'))
        self.build()
        with self.store.connect() as db:
            db.execute(enrichment.FACT_SCHEMA)
            db.execute("INSERT INTO person_facts(identifier,field,value,rank,source,seen_at) VALUES('email:ann@client.com','phone','+32 470 00 00 00',2,'google',?)", (NOW.isoformat(),))
            db.execute("INSERT INTO person_facts(identifier,field,value,rank,source,seen_at) VALUES('email:ann@client.com','linkedin_url','https://www.linkedin.com/in/ann-example',2,'google',?)", (NOW.isoformat(),))
        card = self.store.suggest('ann-1', 'Prep the call with Ann', 'Call on Monday.', [old])
        self.assertIn('not synced here: WhatsApp, LinkedIn (they may have answered there)', self.app.gap_lines(card['id']))
        self.assertEqual(self.card(card['id'])['gap'], {'name': 'Ann Example', 'days': 20, 'channel': 'email', 'wrote_last': False,
                                                        'unsynced': ['WhatsApp', 'LinkedIn']})
        # With WhatsApp connected, only LinkedIn is unknown
        with self.store.connect() as db:
            self.assertEqual(gap_note.unsynced(db, 'email:ann@client.com', ['gmail', 'whatsapp']), ['LinkedIn'])

    def test_fresh_conversations_and_cards_without_people_stay_quiet(self):
        ask, robot = self.add(mail(1, 'Ann Example <ann@client.com>', 'sam@acme.com'), mail(30, 'Robot <noreply@service.com>', 'sam@acme.com'))
        self.build()
        card = self.store.suggest('ann-1', 'Answer Ann', 'Ann asked.', [ask])
        self.assertNotIn('gap', self.card(card['id']))
        alone = self.store.suggest('robot-1', 'Renew the plan', 'The plan ends soon.', [robot])  # nobody it is about
        self.assertEqual(self.app.gap_lines(alone['id']), '')
        self.assertNotIn('gap', self.card(alone['id']))
        self.assertEqual(gap_note.prompt_lines([]), '')

    def test_the_preparation_gets_the_gap_note(self):
        prompt = a.preparation_prompt({'suggestion_id': 's1', 'job_id': 'j' * 32}, gaps='\n\nWhat we don\'t know (x):\n- Ann: last contact')
        self.assertIn("What we don't know (x):\n- Ann: last contact", prompt)
        self.assertNotIn("What we don't know", a.preparation_prompt({'suggestion_id': 's1', 'job_id': 'j' * 32}))
        rules = (Path(a.ROOT) / 'PREPARATION.md').read_text()
        self.assertIn('"What we don\'t know"', rules)


if __name__ == '__main__':
    unittest.main()
