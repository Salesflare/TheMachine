"""Where a to-do comes from: a reply drafted to an older email of the thread answers its newest one, and the email it
answers leads the to-do (its source line and Read email); New to-do's Email pill searches emails only; who a to-do
is about carries their organization, also once it is done. No live calls."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('sources_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)


def mail(source_id, when, mid, thread='t1', sender='Mira Hart <mira@fund.example>', kind='gmail.message', title='Financials'):
    return {'account_id': 'w', 'source_id': source_id, 'kind': kind, 'occurred_at': when, 'title': title, 'body': 'Could you send the financials?',
            'metadata': {'from': sender, 'to': 'pat@acme.example', 'thread_id': thread, 'message-id': mid, 'labels': ['INBOX']}, 'deleted': False}


class Sources(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.commit_page('w', {}, [mail('old', '2026-10-19T11:05:00+00:00', '<old@mail>'), mail('new', '2026-10-26T11:14:00+00:00', '<new@mail>'),
                                         mail('chat', '2026-10-26T12:00:00+00:00', '', kind='slack.message', title='Financials?')])
        with self.store.connect() as db:
            self.ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}

    def test_a_reply_to_an_older_email_of_the_thread_answers_the_newest(self):
        with self.store.connect() as db:
            rows = db.execute("SELECT metadata FROM events WHERE kind='gmail.message' ORDER BY occurred_at DESC").fetchall()
        draft = {'kind': 'email', 'thread_id': 't1', 'in_reply_to': '<old@mail>', 'body': 'Here they are.'}
        self.assertEqual(a.reply_to_newest(rows, [draft])[0] | {}, {**draft, 'in_reply_to': '<new@mail>', 'references': '<old@mail> <new@mail>'})
        self.assertEqual(a.reply_to_newest(rows, {'kind': 'menu', 'actions': [draft]})['actions'][0]['in_reply_to'], '<new@mail>')
        # Already the newest, another thread, or no reply: left as it is
        for kept in ({**draft, 'in_reply_to': '<new@mail>'}, {**draft, 'thread_id': 't2'}, {'kind': 'email', 'body': 'Hi'}, {'kind': 'slack', 'in_reply_to': '<old@mail>'}):
            self.assertEqual(a.reply_to_newest(rows, kept), kept)

    def test_the_email_a_reply_answers_leads_the_to_do(self):
        card = self.store.suggest('w:financials', 'Mira requests financials', 'Send them.', [self.ids['new'], self.ids['old']], 'now')['id']
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET event_ids=? WHERE id=?', (json.dumps([self.ids['old'], self.ids['new']]), card))
            a.reply_lead(db, card, {'kind': 'menu', 'actions': [{'kind': 'email', 'in_reply_to': '<new@mail>'}]})
            row = db.execute('SELECT event_ids,source_line FROM suggestions WHERE id=?', (card,)).fetchone()
        self.assertEqual(json.loads(row['event_ids']), [self.ids['new'], self.ids['old']])
        self.assertRegex(row['source_line'], r'^Source: email from Mira Hart · ')

    def test_the_email_pill_searches_emails_only(self):
        found = self.store.events(['w'], 'financials', kinds=sorted(a.EMAIL_KINDS))
        self.assertEqual({r['kind'] for r in found}, {'gmail.message'})
        self.assertEqual({r['kind'] for r in self.store.events(['w'], 'financials')}, {'gmail.message', 'slack.message'})
        app = object.__new__(a.App); app.store = self.store; app.config = {'accounts': [{'id': 'w'}]}
        with self.assertRaisesRegex(ValueError, 'list of event kinds'):
            app.action('events', {'account_ids': ['w'], 'query': 'x', 'kinds': "gmail.message' OR 1"})

    def test_who_it_is_about_carries_their_organization(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('org:fund.example','org','Fund Partners',1,1,'{}')")
            db.execute("""INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('email:mira@fund.example','person','Mira Hart',2,1,'{"org":"org:fund.example"}')""")
            db.execute("INSERT INTO graph_events(node_id,event_id,at,direct) VALUES('email:mira@fund.example',?,'2026-10-26',1)", (self.ids['new'],))
            people, _ = a.graph.card_people(db, [self.ids['new']])
        self.assertEqual(people[0]['org'], {'id': 'org:fund.example', 'name': 'Fund Partners'})


if __name__ == '__main__':
    unittest.main()
