"""A review's claim (begin_analysis) stays whole: the boards come with only the projects the claim's signals are in
(the rest is one graph lookup), and the reply never grows past the page size, whatever the boards hold. Made-up
data; no model, no network."""
import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('claim_reply_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph, ps = a.graph, a.project_success
from machine.app import claim_reply  # noqa: E402
from machine.prompts.review import review_prompt  # noqa: E402

NOW = dt.datetime(2026, 11, 9, 9, 0, tzinfo=dt.timezone.utc).isoformat()
STAGES = ['Contacted', 'Agreed', 'In review', 'Live']
CUT = 64000  # where OpenClaw cuts a tool result


def signal(number, body='Their edits are in.'):
    return {'account_id': 'work', 'source_id': f's{number}', 'kind': 'slack.message', 'occurred_at': f'2026-11-09T08:{number % 60:02}:00+00:00',
            'title': 'A signal', 'body': body, 'metadata': {}, 'deleted': False}


def mail(number, sender, thread, to='robin@quillfeather.example'):
    return {'account_id': 'work', 'source_id': f'm{number}', 'kind': 'gmail.message', 'occurred_at': f'2026-11-0{number}T08:00:00+00:00', 'title': 'Your listing',
            'body': 'About the listing.', 'deleted': False, 'metadata': {'from': sender, 'to': to, 'labels': ['INBOX'], 'message-id': f'<{number}@x>', 'thread_id': thread}}


class ClaimReply(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store, self.app.config, self.app.fleet = self.store, {'accounts': [{'id': 'work'}]}, None

    def board(self, count, name='Partner listings', prefix='Partner'):
        """A board with count projects on it, none of them in any signal."""
        with self.store.connect() as db:
            for n in range(count):
                node = f"project:{graph.project_id(db, f'{prefix} number {n:03} listing', NOW)}"
                graph.set_stage(db, node, STAGES[n % 3], 'owner', NOW, board=name, stages=STAGES)
            db.execute('UPDATE boards SET about=? WHERE name=?', ('One project per partner whose page lists us.', name))

    def claim(self):
        return self.app.events_action('begin_analysis', {'account_ids': ['work'], 'limit': 120})

    def test_a_claim_lists_only_its_own_projects_and_counts_the_rest(self):
        self.board(150)
        self.store.commit_page('work', {}, [signal(n) for n in range(3)])
        with self.store.connect() as db:
            first, second = [r[0] for r in db.execute('SELECT id FROM events ORDER BY id LIMIT 2')]
            graph.label(db, [first], 'Partner number 007 listing', 'review', NOW)  # named into it
            pid = db.execute("SELECT id FROM projects WHERE name='Partner number 031 listing'").fetchone()[0]
            graph.label(db, [second], 'Partner number 031 listing', 'review', NOW)
            ps.set_condition(db, pid, 'Listing is live with a link to us', 'link', 'review', NOW)
            ps.set_condition(db, db.execute("SELECT id FROM projects WHERE name='Partner number 090 listing'").fetchone()[0],
                             'Their page names us', 'link', 'review', NOW)
            whole = graph.boards_brief(db)
        reply = self.claim()
        board, = reply['boards']
        self.assertEqual((board['board'], board['stages'][:4], board['about']), ('Partner listings', STAGES, 'One project per partner whose page lists us.'))
        self.assertEqual(board['projects'], {'Partner number 007 listing': 'Agreed', 'Partner number 031 listing': 'Agreed'})
        self.assertEqual(board['done_when'], {'Partner number 031 listing': 'Listing is live with a link to us'})  # only the listed ones'
        self.assertEqual(board['others'], 148)
        self.assertIn('graph {"board"', reply['boards_note'])
        self.assertNotIn('left_out', reply)
        self.assertLess(len(a.encoded(reply['boards'])) * 10, len(a.encoded(whole)))  # a small fraction of the whole boards
        # The rest is one lookup away, through the graph tool the review already has
        found = self.app.graph_action({'board': 'partner listings', '_review_session': 'agent:main:assistant-review-signals-x'})
        self.assertEqual(len(found['projects']), 150)
        self.assertEqual(found['projects']['Partner number 090 listing'], 'Contacted')
        self.assertEqual(found['done_when']['Partner number 090 listing'], 'Their page names us')
        self.assertEqual(found['stages'][:4], STAGES)
        self.assertEqual(self.app.graph_action({'boards': True})['boards'][0]['projects'], 150)
        missed = self.app.graph_action({'board': 'No such board'})  # a wrong name answers with the boards there are
        self.assertEqual((missed['no_board'], [b['board'] for b in missed['boards']]), ('No such board', ['Partner listings']))

    def test_a_board_longer_than_the_old_list_still_shows_the_claims_project(self):
        self.board(170)
        self.store.commit_page('work', {}, [signal(1)])
        with self.store.connect() as db:
            db.execute("UPDATE projects SET stage_at='2020-01-01T00:00:00+00:00' WHERE name='Partner number 004 listing'")  # the oldest move
            self.assertNotIn('Partner number 004 listing', graph.boards_brief(db)[0]['projects'])
            graph.label(db, [db.execute('SELECT id FROM events').fetchone()[0]], 'Partner number 004 listing', 'review', NOW)
        board, = self.claim()['boards']
        self.assertEqual((board['projects'], board['others']), ({'Partner number 004 listing': 'Agreed'}, 169))

    def test_a_signal_the_graph_has_not_linked_yet_still_brings_its_project(self):
        """A reply that just came in is in no project until the next graph build: its thread and its sender show it."""
        self.board(40)
        config = {'accounts': [{'id': 'work', 'service': 'gmail', 'email': 'robin@quillfeather.example'}], 'embeddings': {'model': 'test', 'dims': 4}}
        self.app.config = config
        self.store.commit_page('work', {}, [mail(1, 'Ann Reed <ann@paperkite.example>', 'thread-a'), mail(2, 'Robin <robin@quillfeather.example>', 'thread-a', to='ann@paperkite.example'),
                                            mail(3, 'Lee Moss <lee@bramblebox.example>', 'thread-b'), mail(4, 'Robin <robin@quillfeather.example>', 'thread-b', to='lee@bramblebox.example')])
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute('SELECT id FROM events ORDER BY id')]
            graph.label(db, ids[:2], 'Partner number 005 listing', 'review', NOW)
            graph.label(db, ids[2:], 'Partner number 011 listing', 'review', NOW)
            db.execute('UPDATE events SET analyzed_version=version')
            db.isolation_level = None
            graph.build(db, config, NOW)
            db.execute("UPDATE projects SET org='fernhollow.example' WHERE name='Partner number 020 listing'")
        # After the build: Kai, new to the graph, answers in Ann's thread; Lee writes in a thread of their own; someone
        # new writes from the organization a third project is with
        self.store.commit_page('work', {}, [mail(5, 'Kai Dorn <kai@otherplace.example>', 'thread-a'), mail(6, 'Lee Moss <lee@bramblebox.example>', 'thread-c'),
                                            mail(7, 'Noor Vale <noor@mail.fernhollow.example>', 'thread-d')])
        with self.store.connect() as db:
            new = [r[0] for r in db.execute('SELECT id FROM events ORDER BY id DESC LIMIT 3')]
            self.assertEqual(graph.projects_for(db, new), {})  # the graph has not seen them
        reply = self.claim()
        self.assertEqual(sorted(e['id'] for e in reply['events']), sorted(new))
        board, = reply['boards']
        self.assertEqual(board['projects'], {'Partner number 005 listing': 'In review', 'Partner number 011 listing': 'In review', 'Partner number 020 listing': 'In review'})
        self.assertEqual(board['others'], 37)

    def test_no_board_no_note(self):
        self.store.commit_page('work', {}, [signal(1)])
        reply = self.claim()
        self.assertEqual(reply['boards'], [])
        self.assertNotIn('boards_note', reply)
        self.assertNotIn('left_out', reply)

    def test_a_full_claim_with_big_boards_stays_under_the_page_size(self):
        for n, name in enumerate(['Partner listings', 'Hiring', 'Onboardings', 'Buyers']):
            self.board(150, name, f'{name} counterpart {n}')
        self.store.commit_page('work', {}, [signal(n, 'Long evidence text. ' * 400) for n in range(120)])
        reply = self.claim()
        self.assertGreater(reply['pages'], 1)
        self.assertLessEqual(len(a.encoded(reply)), a.REVIEW_PAGE_CHARS)
        self.assertLess(len(a.json.dumps(a.encoded(reply))), CUT)  # also as the escaped string a Code Mode result holds
        self.assertEqual([b['others'] for b in reply['boards']], [150] * 4)
        page = self.store.analysis_page(reply['analysis_id'], 0)
        self.assertEqual([e['id'] for e in reply['events']], [e['id'] for e in page['events']])  # every signal of the page

    def test_when_it_still_does_not_fit_the_signals_stay_and_the_reply_says_what_went(self):
        self.board(150)
        self.store.commit_page('work', {}, [signal(n, 'Long evidence text. ' * 400) for n in range(120)])
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute('SELECT id FROM events ORDER BY id')]
            for n, event_id in enumerate(ids):  # every signal in its own project on the board
                graph.label(db, [event_id], f'Partner number {n:03} listing', 'review', NOW)
        reply = self.claim()
        self.assertLessEqual(len(a.encoded(reply)), a.REVIEW_PAGE_CHARS)
        page = self.store.analysis_page(reply['analysis_id'], 0)
        self.assertEqual([e['id'] for e in reply['events']], [e['id'] for e in page['events']])
        self.assertIn('Left out to keep this reply whole', reply['left_out'])
        self.assertIn('graph', reply['left_out'])  # with how to get it
        board, = reply['boards']
        self.assertEqual((board['stages'][:4], board.get('projects'), board['others']), (STAGES, None, 150))

    def test_fit_drops_in_order_and_signals_last(self):
        events = [{'id': n, 'body': 'x' * 300} for n in range(1, 11)]
        full = {'analysis_id': 'r', 'events': events, 'projects': ['p' * 20] * 30, 'share_groups': ['g' * 20] * 30,
                'boards': [{'board': 'B', 'stages': ['One', 'Two'], 'projects': {'q' * 30 + str(n): 'One' for n in range(30)}, 'others': 2}]}
        copy = lambda: a.json.loads(a.json.dumps(full))
        self.assertEqual(claim_reply.fit(copy(), 100000).get('left_out'), None)
        base = len(a.encoded(copy())) + len(claim_reply.BOARDS_NOTE) + 20
        one = claim_reply.fit(copy(), base - 300)
        self.assertNotIn('projects', one)
        self.assertEqual(len(one['boards'][0]['projects']), 30)
        two = claim_reply.fit(copy(), base - 1200)
        self.assertEqual((two['boards'][0].get('projects'), two['boards'][0]['others'], 'share_groups' in two), (None, 32, True))
        four = claim_reply.fit(copy(), len(a.encoded(events)) + 400)
        self.assertEqual((len(four['events']), 'boards' in four, 'share_groups' in four, 'boards_note' in four), (10, False, False, False))
        self.assertIn('graph {"boards": true}', four['left_out'])
        last = claim_reply.fit(copy(), 2500)
        self.assertLessEqual(len(a.encoded(last)), 2500)
        self.assertLess(len(last['events']), 10)
        self.assertIn(f"signals {list(range(len(last['events']) + 1, 11))} of this page", last['left_out'])

    def test_the_rules_say_where_the_rest_of_a_board_is(self):
        text = review_prompt('run', [{'id': 'work'}])
        self.assertIn('only the ones this batch touches', text)
        self.assertIn('graph {"board": "<name>"}', text)
        self.assertIn('graph {"board": "<name>"}', claim_reply.BOARDS_NOTE)  # and the reply itself says it


if __name__ == '__main__':
    unittest.main()
