"""A reply from the other side on a board project always gets a to-do with its answer prepared: a stage move, its next
step or automated follow-ups never stand in for it (a review once moved a project whose partner asked for a placement
fee, wrote "Decide whether the fee fits" as the next step, and made no to-do). A fake review drives the real
begin_analysis, suggest and finish_analysis; no model and nothing is sent."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('board_replies_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph = a.graph
NOW = dt.datetime(2026, 10, 28, 20, 0, tzinfo=dt.timezone.utc)
STAGES = ['Contacted', 'Agreed', 'In review', 'Live']
counter = iter(range(1, 10**6))


def mail(hours_ago, sender, to, body, labels=('INBOX',), thread='deal', title='Listing x Acme'):
    n = next(counter)
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(hours=hours_ago)).isoformat(),
            'title': title, 'body': body, 'deleted': False,
            'metadata': {'from': sender, 'to': to, 'labels': list(labels), 'message-id': f'<{n}@x>', 'thread_id': thread}}


class BoardReplies(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.saved_now = a.now
        a.now = lambda: NOW.isoformat(); self.addCleanup(setattr, a, 'now', self.saved_now)
        with self.store.connect() as db:
            graph.save_board(db, {'name': 'Listings', 'stages': STAGES, 'about': 'Partners we list with'}, NOW.isoformat())

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])
        with self.store.connect() as db:
            return [db.execute('SELECT id FROM events WHERE source_id=?', (e['source_id'],)).fetchone()[0] for e in events]

    def outreach_and_terms(self):
        """The owner offers a commission; the partner answers: fine, plus a one-time fee, and more sites on offer."""
        return self.add(
            mail(4, 'Sam <sam@acme.com>', 'pat@listings.example', 'We pay 30% recurring commission. Would that work for your guide?', ('SENT',)),
            mail(1, 'Pat <pat@listings.example>', 'sam@acme.com', 'Your 30% commission seems reasonable, but our one-time editorial fee is $100. '
                 'I can also place you on other sites in my network.'))

    def move(self, event_id, stage='Contacted'):
        return {'project': 'Listings: Pat', 'board': 'Listings', 'stage': stage, 'reason': 'Pat quoted a $100 fee, nothing agreed yet',
                'event_id': event_id, 'next': 'Decide whether the fee fits'}

    def card_for(self, event_id):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute("SELECT s.id,s.status FROM suggestions s, json_each(s.event_ids) j WHERE j.value=?", (event_id,))]

    def test_terms_from_the_other_side_need_a_prepared_to_do_not_only_a_stage(self):
        _, terms = self.outreach_and_terms()
        with self.store.connect() as db:  # automated follow-ups on for the board, as on the owner's Machine
            a.follow_ups.save(db, 'board', db.execute("SELECT id FROM boards WHERE name='Listings'").fetchone()[0], {'on': True}, NOW.isoformat())
        claim = self.store.begin_analysis(['work'], 120)
        # What the review did on the owner's Machine: moved the board, wrote the decision as its next step, no to-do.
        with self.assertRaisesRegex(ValueError, rf'{terms} "Listing x Acme" \(Listings: Pat\).*prepare_ahead:true'):
            self.store.finish_analysis(claim['analysis_id'], 'Moved Pat', stages=[self.move(terms)])
        with self.store.connect() as db:  # refused as a whole: nothing moved, the signal is still to review
            self.assertIsNone(db.execute("SELECT stage FROM projects WHERE name='Listings: Pat'").fetchone())
            self.assertEqual(db.execute('SELECT analyzed_version FROM events WHERE id=?', (terms,)).fetchone()[0], 0)
        # Follow-ups on don't change it: they only nudge when the owner wrote last. The reply gets its to-do, prepared ahead.
        saved = self.store.suggest('work:listing-pat-fee', 'Answer Pat’s $100 listing fee', 'Pat accepts 30% but asks a one-time **$100** fee. '
                                   'I can draft your answer.', [terms], ahead=True, match=True, project='Listings: Pat')
        done = self.store.finish_analysis(claim['analysis_id'], 'Moved Pat, to-do for the fee', stages=[self.move(terms)])
        self.assertEqual(done['stages'][0]['stage'], 'Contacted')  # terms not agreed yet: the stage before Agreed
        self.assertEqual(self.card_for(terms), [{'id': saved['id'], 'status': 'accepted'}])  # accepted: prepared ahead, the answer drafted
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT next_step FROM projects WHERE name='Listings: Pat'").fetchone()[0], 'Decide whether the fee fits')

    def test_a_board_reply_on_no_move_is_caught_too_and_one_that_needs_nothing_says_why(self):
        _, thanks = self.outreach_and_terms()
        with self.store.connect() as db:
            graph.set_stage(db, 'Listings: Pat', 'Contacted', 'review', NOW.isoformat(), board='Listings', reason='asked', event_id=thanks - 1)
            graph.label(db, [thanks], 'Listings: Pat', 'review', NOW.isoformat())
        claim = self.store.begin_analysis(['work'], 120)
        with self.assertRaisesRegex(ValueError, 'Not finished yet'):
            self.store.finish_analysis(claim['analysis_id'], 'Nothing new')
        for bad in ([{'event_id': thanks}], [{'event_id': 999999, 'why': 'x'}], {'event_id': thanks, 'why': 'x'}):
            with self.assertRaises(ValueError):
                self.store.finish_analysis(claim['analysis_id'], 'Nothing new', replies=bad)
        self.store.finish_analysis(claim['analysis_id'], 'Nothing new', replies=[{'event_id': thanks, 'why': 'Only a thank-you'}])
        with self.store.connect() as db:  # the why stays with the review, to check later why there was no to-do
            items = json.loads(db.execute('SELECT items FROM analyses WHERE id=?', (claim['analysis_id'],)).fetchone()[0])
        self.assertEqual(next(i['no_reply'] for i in items if i['id'] == thanks), 'Only a thank-you')

    def test_bounces_answered_threads_and_projects_on_no_board_are_not_held(self):
        _, reply = self.outreach_and_terms()
        self.add(mail(0.5, 'Sam <sam@acme.com>', 'pat@listings.example', 'Thanks, we don’t pay fees.', ('SENT',)))
        bounce, = self.add(mail(0.4, 'Mail Delivery Subsystem <mailer-daemon@googlemail.com>', 'sam@acme.com', 'Address not found', thread='b'))
        loose, = self.add(mail(0.3, 'Kim <kim@other.example>', 'sam@acme.com', 'Can you do $50?', thread='loose'))
        claim = self.store.begin_analysis(['work'], 120)
        with self.store.connect() as db:
            graph.label(db, [loose], 'Kim deal', 'review', NOW.isoformat())  # a project, but on no board
        self.store.finish_analysis(claim['analysis_id'], 'Reviewed', stages=[self.move(reply), {**self.move(bounce), 'project': 'Listings: Bounced'}])

    def test_a_reply_after_a_follow_up_is_a_new_to_do_not_folded_into_the_follow_up(self):
        own, reply = self.outreach_and_terms()
        with self.store.connect() as db:
            node = graph.set_stage(db, 'Listings: Pat', 'Contacted', 'review', NOW.isoformat(), board='Listings', reason='asked', event_id=own)['node_id']
            # The follow-up to-do on the owner's email, sent from here (done) before Pat answered.
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at,status) VALUES('fu','follow-up:1','Follow up with Pat','B',?,?,?,'completed')",
                       (json.dumps([own]), json.dumps(['work']), (NOW - dt.timedelta(hours=3)).isoformat()))
            db.execute('INSERT INTO follow_up_cards(suggestion_id,project_id,board_id,grouped,n,of_max,channel,after_event,after_at,state,created_at) '
                       "VALUES('fu',?,1,0,1,3,'email',?,?,'sent',?)", (int(node.split(':')[1]), own, NOW.isoformat(), NOW.isoformat()))
        claim = self.store.begin_analysis(['work'], 120)
        saved = self.store.suggest('work:listing-pat-fee', 'Answer Pat’s $100 listing fee', 'Pat asks a one-time **$100** fee. I can draft your answer.',
                                   [reply], ahead=True, match=True)
        self.assertNotEqual(saved['id'], 'fu')
        self.assertFalse(saved.get('attached'))
        self.assertEqual(self.card_for(reply), [{'id': saved['id'], 'status': 'accepted'}])
        self.store.finish_analysis(claim['analysis_id'], 'To-do for the fee', stages=[self.move(reply)])

    def test_the_review_is_told(self):
        prompt = a.review_prompt('run', ['work'])
        self.assertIn('A stage and its next step never replace a to-do', prompt)
        self.assertIn('replies [{"event_id", "why"}]', prompt)
        rules = Path(__file__).parent.parent.joinpath('AGENTS.md').read_text()
        self.assertIn('**Replies that wait on the owner:**', rules)


if __name__ == '__main__':
    unittest.main()
