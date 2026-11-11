"""A partner listing is done only with its proof (project_success.py): its success condition in plain words, suggested
by a review and the owner's to change; a move to the last stage needs a live page that links to the owner (or, when the
condition says so, their message), otherwise it stays one stage before; the owner's own Won still stands. The same
review run keeps the blocker current and makes at most one to-do per project, never one that sends. Made-up data; a
fake review drives the real begin_analysis and finish_analysis; no model, no network, nothing is sent."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('project_success_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph, ps = a.graph, a.project_success
import graph_updates, record_log  # noqa: E402
from machine.app import claim_reply  # noqa: E402
NOW = dt.datetime(2026, 10, 28, 20, 0, tzinfo=dt.timezone.utc)
STAGES = ['Contacted', 'Agreed', 'In review', 'Live']
LIVE = 'https://blog.paperkite.example/best-crm-tools'
counter = iter(range(1, 10**6))


def mail(hours_ago, sender, to, body, labels=('INBOX',), thread='listing', title='Guest listing'):
    n = next(counter)
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(hours=hours_ago)).isoformat(),
            'title': title, 'body': body, 'deleted': False,
            'metadata': {'from': sender, 'to': to, 'labels': list(labels), 'message-id': f'<{n}@x>', 'thread_id': thread}}


class Fixture:
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = [{'id': 'work', 'service': 'gmail', 'email': 'robin@quillfeather.example'}]
        self.addCleanup(setattr, a.Store, 'accounts', [])
        clock = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        clock.start()
        self.addCleanup(clock.stop)
        self.pages = {}
        self.saved_fetch = ps.fetch_page
        ps.fetch_page = lambda url: self.pages.get(url)
        self.addCleanup(setattr, ps, 'fetch_page', self.saved_fetch)
        with self.store.connect() as db:
            graph.save_board(db, {'name': 'Partner listings', 'stages': STAGES, 'about': 'Sites that list us'}, NOW.isoformat())

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])
        with self.store.connect() as db:
            return [db.execute('SELECT id FROM events WHERE source_id=?', (e['source_id'],)).fetchone()[0] for e in events]

    def review(self, stages, replies=()):
        claim = self.store.begin_analysis(['work'], 120)
        return self.store.finish_analysis(claim['analysis_id'], 'Listings', stages=stages, replies=list(replies))

    def project(self, name='Paperkite listing'):
        with self.store.connect() as db:
            row = db.execute('SELECT * FROM projects WHERE name=?', (name,)).fetchone()
            return dict(row), graph.project_moves(db, 'project:' + str(row['id']))



class ProjectSuccess(Fixture, unittest.TestCase):
    def agreed(self):
        """Robin pitched; Paperkite agreed to list them. The review places it with a suggested condition."""
        pitch, yes = self.add(mail(200, 'Robin <robin@quillfeather.example>', 'kai@paperkite.example', 'Would you list Quillfeather in your CRM guide?', ('SENT',)),
                              mail(190, 'Kai <kai@paperkite.example>', 'robin@quillfeather.example', 'Happy to. I will send the link once it is up.'))
        self.review([{'project': 'Paperkite listing', 'board': 'Partner listings', 'stage': 'Agreed', 'reason': 'Kai agreed to list us', 'event_id': yes,
                      'next': 'Wait for the link', 'condition': 'Listing is live with a link to us', 'proof': 'link'}],
                    replies=[{'event_id': yes, 'why': 'a yes, nothing to answer'}])
        return pitch, yes

    def test_a_listing_is_live_only_when_its_page_loads_and_links_to_the_owner(self):
        self.agreed()
        row, board = self.project()
        self.assertEqual(row['stage'], 'Agreed')
        self.assertEqual(board['success']['condition'], 'Listing is live with a link to us')
        self.assertEqual((board['success']['proof'], board['success']['by'], board['success']['done']), ('link', 'review', False))
        # "It's live" with a link, but the page has no link to the owner yet: not proven, one stage before Live
        live, = self.add(mail(3, 'Kai <kai@paperkite.example>', 'robin@quillfeather.example', f'It is live: {LIVE}. Thanks!'))
        self.pages[LIVE] = b'<html><a href="https://othercrm.example">Other CRM</a></html>'
        move = {'project': 'Paperkite listing', 'board': 'Partner listings', 'stage': 'Live', 'reason': 'Kai says it is live', 'event_id': live, 'url': LIVE,
                'next': 'Share it'}
        done = self.review([move], replies=[{'event_id': live, 'why': 'a confirmation'}])
        self.assertEqual((done['stages'][0]['stage'], done['stages'][0]['not_proven']), ('In review', 'unlinked'))
        row, board = self.project()
        self.assertEqual(row['stage'], 'In review')
        self.assertEqual((board['success']['done'], board['success']['not_proven'], board['success']['evidence']), (False, 'unlinked', None))
        # The page links to the owner now: Live, with the message and the page as its proof
        self.pages[LIVE] = b'<html><a href="https://www.quillfeather.example/?ref=paperkite">Quillfeather</a></html>'
        again, = self.add(mail(1, 'Kai <kai@paperkite.example>', 'robin@quillfeather.example', f'Fixed the link: {LIVE}'))
        done = self.review([{**move, 'event_id': again, 'reason': 'Kai fixed the link'}], replies=[{'event_id': again, 'why': 'a confirmation'}])
        self.assertNotIn('not_proven', done['stages'][0])
        row, board = self.project()
        self.assertEqual(row['stage'], 'Live')
        self.assertEqual((board['success']['done'], board['success']['done_by']), (True, 'evidence'))
        self.assertEqual(board['success']['evidence'], {'event_id': again, 'url': LIVE, 'at': (NOW - dt.timedelta(hours=1)).isoformat()})

    def test_a_link_the_message_does_not_give_is_never_opened(self):
        self.agreed()
        live, = self.add(mail(2, 'Kai <kai@paperkite.example>', 'robin@quillfeather.example', 'It is live now.'))
        opened = []
        ps.fetch_page = lambda url: opened.append(url) or b'quillfeather.example'
        done = self.review([{'project': 'Paperkite listing', 'board': 'Partner listings', 'stage': 'Live', 'reason': 'Kai says it is live', 'event_id': live,
                             'url': LIVE}], replies=[{'event_id': live, 'why': 'a confirmation'}])
        self.assertEqual((opened, done['stages'][0]['stage'], done['stages'][0]['not_proven']), ([], 'In review', 'unsaid'))
        # A review can't swap the page check for "their message says so"
        said, = self.add(mail(1, 'Kai <kai@paperkite.example>', 'robin@quillfeather.example', 'Really, it is up.'))
        done = self.review([{'project': 'Paperkite listing', 'board': 'Partner listings', 'stage': 'Live', 'reason': 'Kai says it is live', 'event_id': said,
                             'proof': 'message'}], replies=[{'event_id': said, 'why': 'a confirmation'}])
        self.assertEqual(done['stages'][0]['stage'], 'In review')

    def test_the_owner_sets_the_condition_and_can_still_mark_it_done_by_hand(self):
        self.agreed()
        row, _ = self.project()
        node = 'project:' + str(row['id'])
        with self.store.connect() as db:
            graph.save_project(db, {'node_id': node, 'condition': 'Kai confirms the listing is published', 'proof': 'message'}, NOW.isoformat())
            self.assertEqual(graph.project_card(db, node)['condition'], 'Kai confirms the listing is published')
        # A later review's suggestion never replaces the owner's word
        nudge, = self.add(mail(5, 'Kai <kai@paperkite.example>', 'robin@quillfeather.example', 'Draft is in review with our editor.'))
        self.review([{'project': 'Paperkite listing', 'board': 'Partner listings', 'stage': 'In review', 'reason': 'Draft with their editor', 'event_id': nudge,
                      'condition': 'Something else', 'proof': 'link'}], replies=[{'event_id': nudge, 'why': 'an update'}])
        _, board = self.project()
        self.assertEqual((board['success']['condition'], board['success']['proof'], board['success']['by']), ('Kai confirms the listing is published', 'message', 'owner'))
        # Their message is the proof the owner asked for; the owner's own message never is
        mine, = self.add(mail(2, 'Robin <robin@quillfeather.example>', 'kai@paperkite.example', 'Is it published?', ('SENT',)))
        done = self.review([{'project': 'Paperkite listing', 'board': 'Partner listings', 'stage': 'Live', 'reason': 'asked', 'event_id': mine}])
        self.assertEqual((done['stages'][0]['stage'], done['stages'][0]['not_proven']), ('In review', 'from_owner'))
        # Won by hand: done, by the owner, with no proof
        with self.store.connect() as db:
            graph.set_outcome(db, node, 'won', 'Saw it myself', NOW.isoformat())
        _, board = self.project()
        self.assertEqual((board['success']['done'], board['success']['done_by'], board['success']['evidence']), (True, 'owner', None))

    def test_no_reply_gets_one_to_do_and_an_open_to_do_or_follow_ups_mean_none(self):
        pitch, yes = self.agreed()
        nudge, = self.add(mail(24 * 12, 'Robin <robin@quillfeather.example>', 'kai@paperkite.example', 'Any news on the listing?', ('SENT',)))
        # A message newer than Kai's yes, so the owner is waiting since this one... but the yes came later: move it back
        with self.store.connect() as db:
            db.execute('UPDATE events SET occurred_at=? WHERE id=?', ((NOW - dt.timedelta(days=20)).isoformat(), yes))
            db.execute('UPDATE events SET occurred_at=? WHERE id=?', ((NOW - dt.timedelta(days=21)).isoformat(), pitch))
            graph.label(db, [nudge], 'Paperkite listing', 'review', NOW.isoformat())
            self.store.project_blockers(db)
            self.store.project_blockers(db)  # each review run: still one
            todos = db.execute("SELECT id,title,status FROM suggestions WHERE dedupe_key LIKE 'project-success:%'").fetchall()
        self.assertEqual([t['title'] for t in todos], ['Nudge Paperkite listing: no reply in 12 days'])
        self.assertEqual(todos[0]['status'], 'pending')  # a to-do to look at, nothing drafted or sent
        _, board = self.project()
        self.assertEqual(board['success']['blocker']['kind'], 'no_reply')
        self.assertEqual(board['success']['blocker']['todo'], {'id': todos[0]['id'], 'title': todos[0]['title']})
        # Done: no new one, also not after it was closed
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='completed' WHERE id=?", (todos[0]['id'],))
            self.store.project_blockers(db)
            self.assertEqual(db.execute("SELECT count(*) FROM suggestions WHERE dedupe_key LIKE 'project-success:%'").fetchone()[0], 1)
            # Follow-ups on for the board: they chase a quiet one, so the blocker shows and no to-do is made
            a.follow_ups.save(db, 'board', db.execute("SELECT id FROM boards").fetchone()[0], {'on': True}, NOW.isoformat())
            self.assertEqual(ps.monitor(db, NOW.isoformat()), [])
            self.assertTrue(json.loads(db.execute('SELECT blocker FROM project_success').fetchone()[0])['follow_ups'])

    def test_an_overdue_promise_on_the_project_is_its_blocker_and_its_own_to_do_is_reused(self):
        _, yes = self.agreed()
        with self.store.connect() as db:
            db.execute("INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,status,created_at,updated_at) "
                       "VALUES('theirs','Kai','send the draft','2026-10-20','2026-10-21',?,'work','open',?,?)", (yes, NOW.isoformat(), NOW.isoformat()))
            wanted = ps.monitor(db, NOW.isoformat())
            self.assertEqual([w['title'] for w in wanted], ['Ask Kai about: send the draft'])
            # An open to-do on the project already: that one shows with the blocker, no second one
            own = self.store.suggest('work:kai-draft', 'Chase Kai for the draft', 'Kai said Oct 20.', [yes], project='Paperkite listing', _db=db)
            self.assertEqual(ps.monitor(db, NOW.isoformat()), [])
        _, board = self.project()
        self.assertEqual((board['success']['blocker']['kind'], board['success']['blocker']['who'], board['success']['blocker']['due']),
                         ('promise_theirs', 'Kai', '2026-10-20'))
        self.assertEqual(board['success']['blocker']['todo']['id'], own['id'])

    def test_a_project_without_a_condition_moves_as_before_and_the_brief_lists_conditions(self):
        _, yes = self.agreed()
        other, = self.add(mail(2, 'Lee <lee@bramblebox.example>', 'robin@quillfeather.example', 'Your listing is up!', thread='bb'))
        done = self.review([{'project': 'Bramblebox listing', 'board': 'Partner listings', 'stage': 'Live', 'reason': 'Lee says it is up', 'event_id': other}],
                           replies=[{'event_id': other, 'why': 'a confirmation'}])
        self.assertEqual(done['stages'][0]['stage'], 'Live')
        with self.store.connect() as db:
            brief = graph.boards_brief(db)
        self.assertEqual(brief[0]['done_when'], {'Paperkite listing': 'Listing is live with a link to us'})

    def test_page_check_matches_the_domain_not_a_longer_one(self):
        self.assertTrue(ps.page_links_to(b'<a href="https://quillfeather.example/">', {'quillfeather.example'}))
        self.assertFalse(ps.page_links_to(b'<a href="https://quillfeather.example.evil.example/">x</a> notquillfeather.example', {'quillfeather.example'}))



class OffBoard(Fixture, unittest.TestCase):
    """A project on no board has a Done when too (2026-11-11): its proof marks it done (outcome 'won', called Done for work
    that isn't a deal) with Undo under Recent changes; a stall on it gets the same one to-do, which waits for the result."""

    def plan(self, condition='Lee confirms the guest post is published', proof='message'):
        """A project on no board with the owner's condition, and the pitch it started from."""
        pitch, = self.add(mail(300, 'Robin <robin@quillfeather.example>', 'lee@bramblebox.example', 'Could we write a guest post for you?', ('SENT',), thread='gp'))
        with self.store.connect() as db:
            graph.label(db, [pitch], 'Bramblebox guest post', 'review', NOW.isoformat())
            node = 'project:' + str(db.execute("SELECT id FROM projects WHERE name='Bramblebox guest post'").fetchone()[0])
            graph.save_project(db, {'node_id': node, 'condition': condition, 'proof': proof}, NOW.isoformat())
            self.assertIsNone(db.execute("SELECT board_id FROM projects WHERE name='Bramblebox guest post'").fetchone()[0])
        return node, pitch

    def page(self, node):
        with self.store.connect() as db:
            log = record_log.recent(db, {'id': node, 'kind': 'project', 'info': None})  # its Recent changes (no graph build needed)
            return graph.project_card(db, node), ps.page(db, node), log

    def test_a_matching_message_marks_it_done_with_undo_and_reopen_stands(self):
        node, _ = self.plan()
        card, success, _ = self.page(node)
        self.assertEqual((card['condition'], card['deal'], success['done']), ('Lee confirms the guest post is published', False, False))
        # The owner's own message never proves it
        mine, = self.add(mail(5, 'Robin <robin@quillfeather.example>', 'lee@bramblebox.example', 'Is it up yet?', ('SENT',), thread='gp'))
        done = self.review([{'project': 'Bramblebox guest post', 'done': True, 'event_id': mine, 'reason': 'asked'}])
        self.assertEqual(done['stages'][0]['not_proven'], 'from_owner')
        self.assertIsNone(self.project('Bramblebox guest post')[0]['outcome'])
        # Lee's message meets it: done, with the message as its proof, and Undo on the page
        yes, = self.add(mail(2, 'Lee <lee@bramblebox.example>', 'robin@quillfeather.example', 'Your guest post is published today.', thread='gp'))
        done = self.review([{'project': 'Bramblebox guest post', 'done': True, 'event_id': yes, 'reason': 'Lee says it is published'}],
                           replies=[{'event_id': yes, 'why': 'a confirmation'}])
        self.assertEqual((done['stages'][0]['outcome'], done['stages'][0]['deal']), ('won', False))
        row, board = self.project('Bramblebox guest post')
        self.assertEqual((row['outcome'], row['outcome_reason'], board), ('won', 'Lee says it is published', None))
        card, success, log = self.page(node)
        self.assertEqual((success['done'], success['done_by'], success['evidence']['event_id']), (True, 'evidence', yes))
        marked = [x for x in log if x['kind'] == 'done']
        self.assertEqual(len(marked), 1)
        self.assertEqual((marked[0]['deal'], marked[0]['act'], marked[0]['source']['id']), (False, {'reopen': node}, yes))
        with self.store.connect() as db:
            self.assertIn((node, NOW.isoformat(), {'kind': 'done', 'deal': False}), graph_updates._changes(db, graph_updates.since(NOW)))  # Updated today
        # Undo is the owner's Reopen: open again, the line goes, and the same message never marks it done again
        with self.store.connect() as db:
            self.assertFalse(graph.set_outcome(db, node, None, '', NOW.isoformat())['deal'])
        card, success, log = self.page(node)
        self.assertEqual((card['outcome'], success['done'], [x for x in log if x['kind'] == 'done']), (None, False, []))
        with self.store.connect() as db:
            again = ps.done_off_board(db, {'project': 'Bramblebox guest post', 'done': True, 'event_id': yes, 'reason': 'Lee says it is published'}, {}, 'review',
                                      NOW.isoformat())
        self.assertEqual(again['kept'], 'The owner reopened it after this message')

    def test_a_live_page_proves_it_and_a_deal_ends_won(self):
        node, _ = self.plan('The partner page is live with a link to us', 'link')
        with self.store.connect() as db:
            graph.save_project(db, {'node_id': node, 'value': '4000'}, NOW.isoformat())
        live, = self.add(mail(1, 'Lee <lee@bramblebox.example>', 'robin@quillfeather.example', f'It is live: {LIVE}', thread='gp'))
        self.pages[LIVE] = b'<html><a href="https://quillfeather.example">Quillfeather</a></html>'
        # The claim lists the project's done when, so the review knows what to look for
        claim = self.store.begin_analysis(['work'], 120)
        with self.store.connect() as db:
            mine = claim_reply.claimed_projects(db, claim_reply.claim_ids(db, claim['analysis_id']), {})
            self.assertEqual(claim_reply.done_when(db, mine), {'Bramblebox guest post': 'The partner page is live with a link to us'})
        done = self.store.finish_analysis(claim['analysis_id'], 'Live', stages=[{'project': 'Bramblebox guest post', 'done': True, 'event_id': live,
                                                                                 'reason': 'Lee says it is live', 'url': LIVE}],
                                          replies=[{'event_id': live, 'why': 'a confirmation'}])
        self.assertEqual((done['stages'][0]['outcome'], done['stages'][0]['deal']), ('won', True))
        _, success, log = self.page(node)
        self.assertEqual(success['evidence']['url'], LIVE)
        self.assertTrue(next(x for x in log if x['kind'] == 'done')['deal'])

    def test_a_review_sets_a_condition_through_graph_but_never_over_the_owners(self):
        pitch, = self.add(mail(30, 'Robin <robin@quillfeather.example>', 'sam@tealpond.example', 'Shall we sign the reseller agreement?', ('SENT',), thread='rs'))
        with self.store.connect() as db:
            graph.label(db, [pitch], 'Tealpond reseller', 'review', NOW.isoformat())
            said = ps.done_off_board(db, {'project': 'Tealpond reseller', 'condition': 'Sam sends the signed agreement', 'proof': 'message'}, {}, 'review', NOW.isoformat())
            self.assertEqual(said['condition'], 'Sam sends the signed agreement')
            node = said['node_id']
            graph.save_project(db, {'node_id': node, 'condition': 'Signed and paid', 'proof': 'message'}, NOW.isoformat())
            ps.done_off_board(db, {'project': 'Tealpond reseller', 'condition': 'Something else'}, {}, 'review', NOW.isoformat())
            self.assertEqual(graph.project_card(db, node)['condition'], 'Signed and paid')
            with self.assertRaises(ValueError):  # neither a board nor a condition: as before, say which board
                ps.done_off_board(db, {'project': 'Tealpond reseller'}, {}, 'review', NOW.isoformat())

    def test_a_stall_on_a_project_on_no_board_gets_one_to_do_that_waits_for_the_result(self):
        node, pitch = self.plan()
        with self.store.connect() as db:
            db.execute('UPDATE events SET occurred_at=? WHERE id=?', ((NOW - dt.timedelta(days=12)).isoformat(), pitch))
            self.store.project_blockers(db)
            self.store.project_blockers(db)  # each review run: still one
            todos = db.execute("SELECT id,title,status,done_when,done_when_by FROM suggestions WHERE dedupe_key LIKE 'project-success:%'").fetchall()
        self.assertEqual([t['title'] for t in todos], ['Nudge Bramblebox guest post: no reply in 12 days'])
        self.assertEqual((todos[0]['done_when'], todos[0]['done_when_by']), ('Lee confirms the guest post is published', 'project'))
        _, success, _ = self.page(node)
        self.assertEqual((success['blocker']['kind'], success['blocker']['days'], success['blocker']['todo']['id']), ('no_reply', 12, todos[0]['id']))
        # Done: nothing stands in its way any more
        yes, = self.add(mail(1, 'Lee <lee@bramblebox.example>', 'robin@quillfeather.example', 'Published it this morning.', thread='gp'))
        self.review([{'project': 'Bramblebox guest post', 'done': True, 'event_id': yes, 'reason': 'Lee published it'}], replies=[{'event_id': yes, 'why': 'a confirmation'}])
        _, success, _ = self.page(node)
        self.assertEqual((success['done'], success['blocker']), (True, None))

    def test_a_new_done_when_reaches_its_to_do_and_drops_what_the_old_one_said(self):
        node, pitch = self.plan('The partner page is live with a link to us', 'link')
        said, = self.add(mail(30, 'Lee <lee@bramblebox.example>', 'robin@quillfeather.example', 'It is up now.', thread='gp'))
        with self.store.connect() as db:
            db.execute('UPDATE events SET occurred_at=? WHERE id=?', ((NOW - dt.timedelta(days=12)).isoformat(), pitch))
            self.store.project_blockers(db)
        self.review([{'project': 'Bramblebox guest post', 'done': True, 'event_id': said, 'reason': 'Lee says it is up'}])
        self.assertEqual(self.page(node)[1]['not_proven'], 'no_url')
        with self.store.connect() as db:
            graph.save_project(db, {'node_id': node, 'condition': 'Lee pays the invoice', 'proof': 'message'}, NOW.isoformat())
            todo = db.execute("SELECT done_when,done_when_by,body FROM suggestions WHERE dedupe_key LIKE 'project-success:%'").fetchone()
        # The blocker to-do waits for the new result, and why the old one wasn't proven is gone with it
        self.assertEqual((todo['done_when'], todo['done_when_by'], todo['body']), ('Lee pays the invoice', 'project', 'Done when: Lee pays the invoice'))
        self.assertIsNone(self.page(node)[1]['not_proven'])
        with self.store.connect() as db:  # a line the run set (the owner's word in its chat) stays theirs
            db.execute("UPDATE suggestions SET done_when='Paid in full',done_when_by='run' WHERE dedupe_key LIKE 'project-success:%'")
            graph.save_project(db, {'node_id': node, 'condition': 'Lee pays the deposit'}, NOW.isoformat())
            self.assertEqual(db.execute("SELECT done_when FROM suggestions WHERE dedupe_key LIKE 'project-success:%'").fetchone()[0], 'Paid in full')

    def test_a_done_its_proof_made_follows_the_goal_and_a_done_by_hand_stays(self):
        node, _ = self.plan()
        yes, = self.add(mail(2, 'Lee <lee@bramblebox.example>', 'robin@quillfeather.example', 'Your guest post is published today.', thread='gp'))
        self.review([{'project': 'Bramblebox guest post', 'done': True, 'event_id': yes, 'reason': 'Lee says it is published'}])
        with self.store.connect() as db:  # the same goal in other letters: still done
            graph.save_project(db, {'node_id': node, 'condition': 'lee confirms the guest post is published'}, NOW.isoformat())
        self.assertEqual(self.page(node)[0]['outcome'], 'won')
        with self.store.connect() as db:  # now it asks for a live page, which a message alone never proved
            graph.save_project(db, {'node_id': node, 'condition': 'lee confirms the guest post is published', 'proof': 'link'}, NOW.isoformat())
        card, success, log = self.page(node)
        self.assertEqual((card['outcome'], success['done']), (None, False))
        line = next(x for x in log if x['kind'] == 'reopened')
        self.assertEqual((line['source']['id'], 'act' in line, [x for x in log if x['kind'] == 'done']), (yes, False, []))
        # A newer message that meets the new goal marks it done again
        live, = self.add(mail(1, 'Lee <lee@bramblebox.example>', 'robin@quillfeather.example', f'It is live: {LIVE}', thread='gp'))
        self.pages[LIVE] = b'<html><a href="https://quillfeather.example">Quillfeather</a></html>'
        self.review([{'project': 'Bramblebox guest post', 'done': True, 'event_id': live, 'reason': 'Lee says it is live', 'url': LIVE}])
        self.assertEqual(self.page(node)[1]['done_by'], 'evidence')
        with self.store.connect() as db:  # the goal reworded: that proof was for another goal
            graph.save_project(db, {'node_id': node, 'condition': 'Lee links us from the homepage'}, NOW.isoformat())
        self.assertIsNone(self.page(node)[0]['outcome'])
        # The owner's Done stands whatever the goal becomes
        with self.store.connect() as db:
            graph.set_outcome(db, node, 'won', '', NOW.isoformat())
            graph.save_project(db, {'node_id': node, 'condition': 'Something else entirely', 'proof': 'message'}, NOW.isoformat())
        _, success, _ = self.page(node)
        self.assertEqual((self.page(node)[0]['outcome'], success['done_by']), ('won', 'owner'))
        # A review that sends a new goal with its proof in one entry ends done by that proof
        with self.store.connect() as db:
            graph.set_outcome(db, node, None, '', NOW.isoformat())
            db.execute('UPDATE project_success SET reopened_at=NULL WHERE project_id=?', (int(node.split(':')[1]),))
        again, = self.add(mail(0.5, 'Lee <lee@bramblebox.example>', 'robin@quillfeather.example', 'Homepage link added.', thread='gp'))
        done = self.review([{'project': 'Bramblebox guest post', 'done': True, 'event_id': again, 'reason': 'Lee added the link',
                             'condition': 'Lee says the homepage links to us'}])
        self.assertEqual(done['stages'][0].get('outcome'), 'won')

    def test_a_done_with_a_new_proof_in_the_same_entry_is_checked_against_that_proof(self):
        pitch, = self.add(mail(30, 'Robin <robin@quillfeather.example>', 'kai@fernhollow.example', 'Could you list us?', ('SENT',), thread='fh'))
        with self.store.connect() as db:
            graph.label(db, [pitch], 'Fernhollow listing', 'review', NOW.isoformat())
            node = ps.done_off_board(db, {'project': 'Fernhollow listing', 'condition': 'Kai confirms the listing', 'proof': 'message'}, {}, 'review',
                                     NOW.isoformat())['node_id']
        said, = self.add(mail(2, 'Kai <kai@fernhollow.example>', 'robin@quillfeather.example', 'You are listed now.', thread='fh'))
        # The review's own goal becomes a live page in the same entry that marks it done: a message alone no longer does it
        done = self.review([{'project': 'Fernhollow listing', 'done': True, 'event_id': said, 'reason': 'Kai says it is listed',
                             'condition': 'The listing page links to us', 'proof': 'link'}])
        self.assertEqual(done['stages'][0].get('not_proven'), 'no_url')
        self.assertIsNone(self.page(node)[0]['outcome'])
        # And back: a message is the proof again, and the same entry's message meets it
        said, = self.add(mail(1, 'Kai <kai@fernhollow.example>', 'robin@quillfeather.example', 'Listed for good.', thread='fh'))
        done = self.review([{'project': 'Fernhollow listing', 'done': True, 'event_id': said, 'reason': 'Kai says it is listed',
                             'condition': 'Kai confirms the listing', 'proof': 'message'}])
        self.assertEqual(done['stages'][0].get('outcome'), 'won')

    def test_the_owners_proof_stands_when_a_review_marks_done_with_another(self):
        node, _ = self.plan('The partner page is live with a link to us', 'link')
        said, = self.add(mail(2, 'Lee <lee@bramblebox.example>', 'robin@quillfeather.example', 'It is up now.', thread='gp'))
        done = self.review([{'project': 'Bramblebox guest post', 'done': True, 'event_id': said, 'reason': 'Lee says it is up',
                             'condition': 'Lee says it is up', 'proof': 'message'}])
        self.assertEqual(done['stages'][0].get('not_proven'), 'no_url')
        self.assertEqual(self.page(node)[0]['condition'], 'The partner page is live with a link to us')


if __name__ == '__main__':
    unittest.main()
