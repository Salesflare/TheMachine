"""Plans that changed: a newer message overturns what The Machine believed, and it updates its own records itself.

A to-do built on a plan a newer message dropped (the party moved to another venue, the booking was canceled) closes by
itself as Not needed, its chat saying "Updated: <why>", with Undo; the same messages never close it again once the owner
took it back, and the owner's own word after them stands. A fact a newer message overturned ends like one past its end
day, under Ended with Bring back. The review sees each fact's id so it can end one. Made-up names, no live calls."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

from seams import patch_everywhere  # noqa: E402

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('plan_changed_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def at(text):
    return patch_everywhere(a, 'now', lambda: text)


def mail(source_id, when, body):
    return {'account_id': 'g', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': when,
            'title': 'Birthday party on December 12', 'body': body, 'deleted': False,
            'metadata': {'from': 'Riverside Hall <hello@riverside.example>', 'thread_id': 't1'}}


class PlanChanged(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'g'}], 'prepare_ahead': False,
                           'database': str(Path(self.temp.name) / 'e.sqlite'), 'openclaw_config': str(Path(self.temp.name) / 'openclaw.json')}
        with at('2026-11-01T10:00:00+00:00'):
            self.store.commit_page('g', {}, [mail('m1', '2026-11-01T09:00:00+00:00', 'Room for 20 children, 11 euro each.')])
            self.sid = self.store.suggest('party-venue', 'Book Riverside Hall for the party', 'Draft asks about the headcount deadline.', [1])['id']

    def overturn(self, when='2026-11-08T19:00:00+00:00'):
        """The owner writes to the venue that they go elsewhere: a newer message in the same thread."""
        with at(when):
            self.store.commit_page('g', {}, [mail('m' + when, when, 'We changed plans and will celebrate somewhere else. Thanks!')])
        with self.store.connect() as db:
            return db.execute('SELECT max(id) FROM events').fetchone()[0]

    def card(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())

    def changed(self, event_ids, when='2026-11-08T19:05:00+00:00', reason='The party moved to another venue'):
        with at(when):
            return self.app.action('looks_handled', {'suggestion_id': self.sid, 'plan_changed': True, 'reason': reason, 'event_ids': event_ids})

    def test_a_to_do_on_a_dropped_plan_closes_by_itself_as_not_needed_with_one_line_and_undo_once(self):
        newer = self.overturn()
        self.assertEqual(self.changed([newer]), {'closed': True})
        card = self.card()
        self.assertEqual((card['status'], card['closed_from'], card['expired_at']), ('completed', 'pending', '2026-11-08T19:05:00+00:00'))
        self.assertGreater(card['undo_until'], '2026-11-09T18:00')
        self.assertIn('Not needed.', a.card(card))
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM deliveries WHERE suggestion_id=?', (self.sid,)).fetchone()[0], 'cancelled')
            lines = [i['text'] for i in self.app.card_chat_service(db, self.sid)[0] if i['kind'] == 'event']
        self.assertEqual(lines, ['Updated: The party moved to another venue'])
        # Undo brings it back, and the same messages never close it again
        with at('2026-11-08T19:10:00+00:00'):
            self.assertEqual(self.store.decide(self.sid, 'undo', '', 'u1', 'dashboard')['status'], 'pending')
        self.assertEqual((self.card()['status'], self.card()['expired_at']), ('pending', None))
        self.assertIn('skipped', self.changed([newer], when='2026-11-08T19:20:00+00:00'))
        self.assertEqual(self.card()['status'], 'pending')

    def test_only_a_message_newer_than_the_to_do_and_the_owners_own_word_counts(self):
        self.assertIn('made after these messages', self.changed([1])['skipped'])  # its own evidence
        newer = self.overturn('2026-11-08T19:00:00+00:00')
        with at('2026-11-08T20:00:00+00:00'):
            self.store.decide(self.sid, 'other', 'Still ask them about the cake', 'n1', 'dashboard')
        self.assertIn('their word stands', self.changed([newer], when='2026-11-08T20:05:00+00:00')['skipped'])
        self.assertNotEqual(self.card()['status'], 'completed')
        with self.assertRaisesRegex(ValueError, 'short plain reason'):
            self.changed([newer], reason='no')
        with self.assertRaisesRegex(ValueError, 'exist'):
            self.changed([newer, 999])

    def test_a_closed_to_do_stays_as_it_is(self):
        newer = self.overturn()
        self.store.decide(self.sid, 'complete', '', 'd1', 'dashboard')
        self.assertEqual(self.changed([newer], when='2026-11-08T21:00:00+00:00'), {'skipped': 'already closed'})

    def test_without_plan_changed_it_stays_a_hint(self):
        newer = self.overturn()
        with at('2026-11-08T19:05:00+00:00'):
            self.app.action('looks_handled', {'suggestion_id': self.sid, 'reason': 'They booked elsewhere', 'event_ids': [newer]})
        self.assertEqual(self.card()['status'], 'pending')


class FactOverturned(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'g'}]}
        with at('2026-11-01T10:00:00+00:00'):
            self.store.commit_page('g', {}, [mail('m1', '2026-11-01T09:00:00+00:00', 'Room for 20 children.')])
            sid = self.store.suggest('party', 'Party venue', 'Body', [1])['id']
            self.store.decide(sid, 'other', 'the party is at Riverside Hall on December 12', 'owner-note', 'dashboard')
            self.fact = self.store.remember_fact("Robin's birthday party is at Riverside Hall on December 12.", 'owner-note', 'event', until='2026-12-12', quote='the party is at Riverside Hall')['id']
            self.other = self.store.remember_fact('Robin likes dinosaurs.', 'owner-note', quote='the party is at Riverside Hall')['id']

    def newer(self, when):
        with at(when):
            self.store.commit_page('g', {}, [mail('m' + when, when, 'We will celebrate somewhere else.')])
        with self.store.connect() as db:
            return db.execute('SELECT max(id) FROM events').fetchone()[0]

    def end(self, event_ids, when='2026-11-08T19:05:00+00:00'):
        with at(when):
            return self.app.action('remember_fact', {'id': self.fact, 'ended': True, 'reason': 'They moved the party elsewhere', 'event_ids': event_ids})

    def test_the_review_sees_ids_and_ends_an_overturned_fact_under_ended_with_bring_back(self):
        with at('2026-11-08T19:00:00+00:00'):
            self.assertIn(f"- [{self.fact}] Robin's birthday party is at Riverside Hall", self.store.facts_text(ids=True))
            self.assertNotIn('[', self.store.facts_text())  # preparations and the rest: as before
            self.assertIn('plan_changed:true', a.review_prompt('run', ['g'], '', self.store.facts_text(ids=True)))
        self.assertIn('skipped', self.end([1]))  # older than the fact: it stands
        newer = self.newer('2026-11-08T19:00:00+00:00')
        self.assertEqual(self.end([newer]), {'ended': self.fact})
        with at('2026-11-08T19:06:00+00:00'):
            text = self.store.facts_text(ids=True)
            ended = self.store.snapshot([])['facts_ended']
        self.assertNotIn('Riverside', text)
        self.assertIn('Robin likes dinosaurs.', text)
        self.assertEqual([f['id'] for f in ended], [self.fact])
        with self.store.connect() as db:
            change = db.execute("SELECT text FROM rule_changes WHERE ref=?", ('expired:' + str(self.fact),)).fetchone()[0]
        self.assertTrue(change.endswith('Updated: They moved the party elsewhere'))
        # Bring back: kept by the owner, and the same message can't end it again
        with at('2026-11-08T20:00:00+00:00'):
            self.store.unmerge_fact(expired=self.fact)
        self.assertIn('Riverside', self.store.facts_text())
        with self.assertRaisesRegex(ValueError, 'Unknown fact'):
            self.app.action('remember_fact', {'id': 999, 'ended': True, 'reason': 'Moved elsewhere', 'event_ids': [newer]})
        self.assertIn('skipped', self.end([newer], when='2026-11-08T20:05:00+00:00'))
        self.assertIn('Riverside', self.store.facts_text())


if __name__ == '__main__':
    unittest.main()
