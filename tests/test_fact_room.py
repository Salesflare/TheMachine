"""The list of what was learned never fills up (machine/store/facts.py set_aside): a save at the cap makes room instead
of failing, a review sets aside what wasn't used lately, a preparation's picks count as used, the owner's own edits and
Bring backs are kept, and a review's facts leave out the stalest, not the newest."""
import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
assistant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assistant)

OLD = '2026-09-01T10:00:00+00:00'
NOW = '2026-10-31T10:00:00+00:00'


def event():
    return {'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': '2026-08-09T10:00:00+00:00',
            'title': 'A real subject', 'body': 'Original', 'metadata': {}, 'deleted': False}


class FactRoom(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'events.sqlite'
        self.store = assistant.Store(self.path)
        self.store.commit_page('work', {}, [event()])
        self.sid = self.store.suggest('facts', 'Check the vendor', 'Body', [1])['id']
        self.store.decide(self.sid, 'reject', 'we stopped using them', 'owner-note', 'dashboard')

    def at(self, when):
        return patch_everywhere(assistant, 'now', return_value=when)

    def fill(self, n, when, start=0, kind=None):
        with self.at(when):
            return [self.store.remember_fact(f'General fact number {i} about how the owner works.', 'owner-note', kind, quote='we stopped using them')['id'] for i in range(start, start + n)]

    def current(self):
        with self.store.connect() as db:
            return {r[0] for r in db.execute('SELECT id FROM facts WHERE removed_at IS NULL')}

    def test_a_full_list_makes_room_instead_of_failing(self):
        ids = self.fill(assistant.FACTS_GENERAL_MAX, OLD)
        with self.at(NOW):
            new = self.store.remember_fact('One more general fact than the list holds.', 'owner-note', quote='we stopped using them')['id']
        current = self.current()
        self.assertIn(new, current)
        self.assertNotIn(ids[0], current)  # the one not used for longest made room
        self.assertEqual(len(current), assistant.FACTS_GENERAL_MAX)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT merged_into FROM facts WHERE id=?', (ids[0],)).fetchone()[0], f'aside:{ids[0]}')
            self.assertTrue(db.execute("SELECT 1 FROM rule_changes WHERE ref=?", (f'aside:{ids[0]}',)).fetchone())
        with self.at(NOW):  # Learning lists it with Bring back
            aside = self.store.snapshot([], lean=True)['facts_aside']
            self.assertEqual([f['id'] for f in aside], [ids[0]])
            self.assertEqual(self.store.unmerge_fact(expired=ids[0]), {'restored': 1})
        self.assertIn(ids[0], self.current())
        with self.at('2026-12-31T10:00:00+00:00'):  # brought back: the owner keeps it, it is never set aside again
            self.store.retire_expired()
            self.store.remember_fact('Yet another general fact for the list.', 'owner-note', quote='we stopped using them')
        self.assertIn(ids[0], self.current())

    def test_while_every_one_was_used_lately_the_list_grows_up_to_the_hard_cap(self):
        self.fill(assistant.FACTS_GENERAL_MAX, NOW)
        self.fill(1, NOW, start=500)  # all fresh: nothing goes, nothing fails
        self.assertEqual(len(self.current()), assistant.FACTS_GENERAL_MAX + 1)
        self.fill(assistant.FACTS_GENERAL_HARD - assistant.FACTS_GENERAL_MAX + 5, NOW, start=600)
        self.assertEqual(len(self.current()), assistant.FACTS_GENERAL_HARD)

    def test_a_review_sets_aside_what_was_not_used_and_keeps_what_was(self):
        ids = self.fill(assistant.FACTS_GENERAL_MAX, OLD)
        with self.at(NOW):
            self.store.mark_used(ids[:5])  # a preparation picked the oldest five lately
            self.store.edit_fact(ids[5], 'The owner rewrote this general fact in their own words.')
            self.store.retire_expired()
        current = self.current()
        self.assertEqual(len(current), assistant.FACTS_GENERAL_ROOM)
        self.assertLessEqual(set(ids[:6]), current)  # used, or kept by the owner
        self.assertFalse(set(ids[6:16]) & current)  # the ten not used for longest

    def test_a_preparation_marks_the_facts_it_picked_for_meaning_as_used(self):
        ids = self.fill(30, OLD)
        other = self.store.suggest('vendor', 'Pay the vendor', 'Body', [1])['id']  # not the card they were learned on
        settings = {'url': 'http://embed.invalid', 'model': 'm', 'dims': 2}

        def embed(settings, texts, timeout=120):
            return [[1.0, 0.0] if 'number 3 ' in t or 'Pay the vendor' in t else [0.0, 1.0] for t in texts]
        with self.at(NOW), patch.object(assistant.embeddings, 'embed', side_effect=embed):
            self.assertIn('number 3 ', self.store.facts_for(other, settings=settings, top=2))
        with self.store.connect() as db:
            used = {r[0] for r in db.execute('SELECT id FROM facts WHERE used_at=?', (NOW,))}
        self.assertEqual(used, {ids[3]})
        with self.at(NOW), patch.object(assistant.embeddings, 'embed', side_effect=assistant.embeddings.EmbeddingError('down')):
            self.store.facts_for(other, settings=settings)  # the newest instead: not a sign of use
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM facts WHERE used_at=?', (NOW,)).fetchone()[0], 1)

    def test_a_review_gets_the_newest_facts_when_they_dont_all_fit(self):
        self.fill(40, OLD)
        with self.at(NOW):
            self.store.remember_fact('The newest fact the owner told.', 'owner-note', quote='we stopped using them')
            text = self.store.facts_text(limit=600)
        self.assertTrue(text.startswith('- The newest fact the owner told.'), text[:80])
        self.assertIn('…', text)

    def test_an_old_database_counts_its_facts_as_used_when_tracking_starts(self):
        ids = self.fill(3, OLD)
        raw = sqlite3.connect(self.path)
        raw.executescript('ALTER TABLE facts DROP COLUMN used_at; ALTER TABLE facts DROP COLUMN kept_at;')
        raw.close()
        with self.at(NOW):
            store = assistant.Store(self.path)
            with store.connect() as db:
                self.assertEqual({r[0] for r in db.execute('SELECT id FROM facts WHERE used_at=?', (NOW,))}, set(ids))
            store.retire_expired()
        self.assertEqual(self.current(), set(ids))


if __name__ == '__main__':
    unittest.main()
