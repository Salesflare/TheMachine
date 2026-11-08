"""The agents' status stays lean (vision: as much intelligence as possible per token). Every review, preparation and
Do it read the whole status, about 100k characters on a Machine with a long Done list: past OpenClaw's tool-result
cut, so most open to-dos were never seen. Done to-dos now come in short after the open ones, and a to-do's own run
reads only its card."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

spec = importlib.util.spec_from_file_location('assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
assistant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assistant)

BODY = 'Drafted a reply with the numbers they asked for and checked the attachment opens. ' * 8  # ~650 characters
CUT = 64000  # OpenClaw's tool-result cut, about what the agents saw (2026-11-08)


class LeanAgentStatus(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = assistant.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': '1', 'kind': 'slack.message', 'title': 'A signal',
                                             'occurred_at': '2026-11-01T10:00:00+00:00', 'body': 'Evidence', 'metadata': {}, 'deleted': False}])
        self.app = object.__new__(assistant.App)
        self.app.store, self.app.config = self.store, {'accounts': []}

    def card(self, n, status='pending'):
        sid = self.store.suggest(f'matter:{n}', f'To-do number {n}', BODY, [1])['id']
        if status != 'pending':
            with self.store.connect() as db:
                db.execute('UPDATE suggestions SET status=? WHERE id=?', (status, sid))
                if status in ('completed', 'rejected'):
                    db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                               (uuid.uuid4().hex, sid, 'complete', '', 'dashboard', f'2026-11-0{1 + n % 8}T10:00:00+00:00'))
        return sid

    def long_done_list(self):
        done = [self.card(n, 'completed') for n in range(120)]
        open_ = [self.card(1000 + n) for n in range(26)]
        return done, open_

    def test_open_todos_come_first_and_all_fit_under_the_cut(self):
        done, open_ = self.long_done_list()
        status = self.app.action('status', {})
        size = len(assistant.encoded(status))
        ids = [s['id'] for s in status['suggestions']]
        self.assertEqual(set(ids[:len(open_)]), set(open_))  # every open to-do before any done one
        self.assertLess(size * 1.5, CUT, size)  # the agent reads it escaped once more inside the tool's reply
        for card in status['suggestions'][len(open_):]:
            self.assertIn(card['status'], ('completed', 'rejected'))
            self.assertNotIn('body', card)
            self.assertTrue(card['title'] and card['dedupe_key'])  # still enough to tell it is the same matter
        self.assertTrue(all(len(c['body']) <= 401 for c in status['suggestions'][:len(open_)]))

    def test_the_lean_status_is_far_smaller_than_before(self):
        self.long_done_list()
        snapshot = self.store.snapshot([], lean=True)
        before = dict(assistant.compact_status(snapshot))
        before['suggestions'] = [{**{k: s[k] for k in ('id', 'status', 'title', 'dedupe_key', 'created_at') if s.get(k)},
                                  'body': s.get('body', '')[:400]} for s in snapshot['suggestions']]
        after = assistant.compact_status(snapshot)
        self.assertLess(len(assistant.encoded(after)) * 2, len(assistant.encoded(before)))

    def test_one_todo_with_its_own_decisions(self):
        done, open_ = self.long_done_list()
        target = open_[3]
        self.store.decide(target, 'other', 'Use the October numbers', uuid.uuid4().hex, 'dashboard')
        found = self.app.action('status', {'suggestion_id': target})
        self.assertEqual(found['suggestion']['id'], target)
        self.assertEqual(found['suggestion']['body'], BODY)  # its whole body, not the first 400 characters
        self.assertTrue(found['decisions'])
        self.assertTrue(all(d['suggestion_id'] == target for d in found['decisions']))
        self.assertNotIn('suggestions', found)
        self.assertLess(len(assistant.encoded(found)), 3000)

    def test_an_old_done_todo_past_the_list_is_still_found(self):
        oldest = self.card(0, 'completed')
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET created_at='2026-01-01T00:00:00+00:00' WHERE id=?", (oldest,))
            db.execute("UPDATE decisions SET created_at='2026-01-01T00:00:00+00:00' WHERE suggestion_id=?", (oldest,))
        for n in range(1, 120):
            self.card(n, 'completed')
        self.assertNotIn(oldest, [s['id'] for s in self.store.snapshot([], lean=True)['suggestions']])
        found = self.app.action('status', {'suggestion_id': oldest})
        self.assertEqual((found['suggestion']['id'], found['suggestion']['status']), (oldest, 'completed'))

    def test_an_unknown_todo(self):
        self.assertIsNone(self.app.action('status', {'suggestion_id': 'nope'})['suggestion'])

    def test_preparations_are_told_to_read_their_own_card(self):
        rules = (Path(__file__).parent.parent / 'PREPARATION.md').read_text()
        self.assertIn('status with args {suggestion_id:', rules)
        self.assertNotIn('status first, find ONLY this suggestion', rules)


if __name__ == '__main__':
    unittest.main()
