"""Who a to-do is for, and what is no to-do. A test persona's handoff to-do came from a client's email, but it showed a
closer colleague of theirs as its person, only because he was on the review meeting the to-do also held; and a booking
confirmation for the owner's own trip became a to-do to move their own gym slot. Later the same handoff showed the
colleague on copy as its person, and a proposal to-do that led with the owner's own channel post showed a teammate from
an internal meeting instead of the client who asked. No live calls."""
import tempfile
import unittest
from pathlib import Path
from seams import patch_everywhere  # noqa: E402,F401
import graph
import machine.app.preparation as machine_app_preparation
import machine.main as machine_main
import machine.prompts.review as machine_prompts_review


def ask(source_id):
    """The client's email asking the owner, with their colleague on copy."""
    return {'account_id': 'w', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': '2026-11-08T12:00:00+00:00', 'title': 'Screens',
            'body': 'Could you share the revised screens by Monday?', 'deleted': False,
            'metadata': {'from': 'Lena Ortiz <lena@client.example>', 'to': 'owner@studio.example', 'cc': 'Marco Bell <marco@client.example>',
                         'thread_id': 't-' + source_id, 'labels': ['INBOX']}}


def post():
    """The owner's own post in a project channel."""
    return {'account_id': 'w', 'source_id': 'post', 'kind': 'slack.message', 'occurred_at': '2026-11-09T09:00:00+00:00', 'title': '#proj: screens',
            'body': 'Working on the screens today.', 'deleted': False, 'metadata': {'user_id': 'U0OWNER01', 'channel_name': 'proj'}}


class LeadPerson(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = machine_main.Store(Path(tmp.name) / 'events.sqlite')
        with self.store.connect() as db:
            for node, name, strength in (('email:lena@client.example', 'Lena Ortiz', 0.8), ('email:marco@client.example', 'Marco Bell', 1.3)):
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person',?,?,1,'{}')", (node, name, strength))
            # 101: Lena's handoff request, 102: the review meeting both are on, 103: Marco's own question in another thread
            for node, event in (('email:lena@client.example', 101), ('email:lena@client.example', 102), ('email:marco@client.example', 102),
                                ('email:marco@client.example', 103)):
                db.execute("INSERT INTO graph_events(node_id,event_id,at,direct) VALUES(?,?,'2026-11-09T00:00:00+00:00',1)", (node, event))

    def people(self, ids, unlinked=True):
        """As the to-do's chip shows them (unlinked: its sender also before the graph links their message)."""
        with self.store.connect() as db:
            return [p['name'] for p in graph.card_people(db, ids, unlinked=unlinked)[0]]

    def test_the_main_sources_person_comes_first(self):
        self.assertEqual(self.people([101, 102, 103]), ['Lena Ortiz', 'Marco Bell'])

    def test_closest_first_among_the_rest(self):
        self.assertEqual(self.people([102]), ['Marco Bell', 'Lena Ortiz'])  # a meeting's own to-do: nobody leads it

    def test_who_asked_leads_over_a_closer_colleague_on_copy_and_before_the_graph_links_them(self):
        # A client's request with a closer colleague of theirs on copy, both on it; then a nudge the graph hasn't linked yet
        nudge = {**ask('nudge'), 'occurred_at': '2026-11-09T12:00:00+00:00'}
        self.store.commit_page('w', {}, [ask('ask'), nudge, post()])
        with self.store.connect() as db:
            new = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
            for node in ('email:lena@client.example', 'email:marco@client.example'):
                db.execute("INSERT INTO graph_events(node_id,event_id,at,direct) VALUES(?,?,'2026-11-09T00:00:00+00:00',1)", (node, new['ask']))
        self.assertEqual(self.people([new['ask'], 103]), ['Lena Ortiz', 'Marco Bell'])
        self.assertEqual(self.people([new['nudge'], 102, 103]), ['Lena Ortiz', 'Marco Bell'])
        # A same-matter check keeps to what the graph linked: only the colleague's own question has nobody else
        self.assertEqual(self.people([new['nudge'], 103], unlinked=False), ['Marco Bell'])
        # A to-do about the colleague's own matter leads with his message, and so with him
        self.assertEqual(self.people([103, new['ask']]), ['Marco Bell', 'Lena Ortiz'])

    def test_the_owners_own_post_first_names_nobody_so_the_next_message_leads(self):
        # The owner's own channel post, then the client's meeting, then an internal one with a teammate closer to the owner
        self.store.commit_page('w', {}, [post()])
        with self.store.connect() as db:
            own = db.execute("SELECT id FROM events WHERE source_id='post'").fetchone()[0]
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('email:ada@studio.example','person','Ada Kim',3.8,1,'{}')")
            db.execute("INSERT INTO graph_events(node_id,event_id,at,direct) VALUES('email:ada@studio.example',104,'2026-11-09T00:00:00+00:00',1)")
        self.assertEqual(self.people([own, 103, 104]), ['Marco Bell', 'Ada Kim'])

    def test_a_meeting_of_the_owners_own_team_names_none_of_them(self):
        # A stand-up's briefing named the colleague closest to the owner, whoever its points were about
        def stand_up(source, people):
            self.store.commit_page('w', {}, [{'account_id': 'w', 'source_id': source, 'kind': 'calendar.event', 'occurred_at': '2026-11-10T09:30:00+00:00',
                                              'title': 'Stand up', 'body': '', 'deleted': False, 'metadata': {'attendees': [{'email': e} for e, _ in people]}}])
            with self.store.connect() as db:
                event = db.execute('SELECT id FROM events WHERE source_id=?', (source,)).fetchone()[0]
                for node, strength in people:
                    db.execute("INSERT OR IGNORE INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person',?,?,1,'{\"colleague\": true}')",
                               ('email:' + node, node.split('@')[0].title(), strength))
                    db.execute("INSERT INTO graph_events(node_id,event_id,at,direct) VALUES(?,?,'2026-11-09T00:00:00+00:00',1)", ('email:' + node, event))
            return event
        team = stand_up('su', [('ada@studio.example', 6.0), ('ben@studio.example', 2.0), ('cy@studio.example', 1.0)])
        with self.store.connect() as db:
            people, weight = graph.card_people(db, [team], unlinked=True)
            self.assertEqual((people, weight), ([], 6.0))  # ranked as before
            # A same-matter check still sees everyone on it
            self.assertEqual(len(graph.card_people(db, [team], limit=10)[0]), 3)
        self.assertEqual(self.people([team, 103]), ['Marco Bell'])  # a later message's sender still shows
        self.assertEqual(self.people([stand_up('one', [('ada@studio.example', 6.0)])]), ['Ada'])  # a 1:1 names them
        mixed = stand_up('mixed', [('ada@studio.example', 6.0), ('ben@studio.example', 2.0)])
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_events(node_id,event_id,at,direct) VALUES('email:lena@client.example',?,'2026-11-09T00:00:00+00:00',1)", (mixed,))
        self.assertEqual(self.people([mixed]), ['Lena Ortiz', 'Ada', 'Ben'])  # someone from outside on it leads, then colleagues

    def test_the_rules_are_in_the_prompts(self):
        self.assertTrue('Automated mail alone makes a to-do only when it asks the owner to act' in machine_prompts_review.review_prompt('r1', ['work']))
        self.assertTrue('nor a message you only read to answer the owner' in machine_app_preparation.preparation_prompt({'job_id': 'j', 'suggestion_id': 's'}))


if __name__ == '__main__':
    unittest.main()
