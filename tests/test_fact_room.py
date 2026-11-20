"""The list of what was learned never fills up and nothing leaves it for not being used (machine/store/facts.py): a
save past the old cap of 80 sets nothing aside, a review sets nothing aside, only a runaway list (FACTS_LIMIT) drops
the lowest-weight lines from other AIs and never the owner's own, facts set aside by earlier versions come back once,
a preparation's picks count as used, and a review's facts leave out the stalest, not the newest."""
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
from machine.store import facts as facts_module  # noqa: E402

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

    def test_nothing_is_set_aside_past_the_old_cap(self):
        ids = self.fill(81, OLD)  # more than the old cap of 80, none used in two months
        with self.at(NOW):
            new = self.store.remember_fact('One more general fact than the old list held.', 'owner-note', quote='we stopped using them')['id']
            self.store.retire_expired()  # a review's pass: only facts past their end day leave
        self.assertEqual(self.current(), set(ids) | {new})
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM facts WHERE merged_into IS NOT NULL").fetchone()[0], 0)
        with self.at(NOW):
            self.assertNotIn('facts_aside', self.store.snapshot([], lean=True))  # Learning has no Set aside section

    def test_a_runaway_list_drops_the_lowest_weight_lines_from_other_ais_never_the_owners(self):
        self.assertGreaterEqual(facts_module.FACTS_LIMIT, 1000)
        with self.store.connect() as db:
            owner = [db.execute("INSERT INTO facts(text,decision_id,created_at,kind,fact_kind) VALUES(?,'d',?,'fact','fact')",
                                (f'Owner fact number {i} about the house.', OLD)).lastrowid for i in range(6)]
            kept = db.execute("INSERT INTO facts(text,decision_id,created_at,kind,fact_kind,source,kept_at) VALUES(?,'i',?,'fact','fact','import:chatgpt',?)",
                              ('An imported line the owner edited.', '2025-01-01T00:00:00+00:00', OLD)).lastrowid
            older = db.execute("INSERT INTO facts(text,decision_id,created_at,kind,fact_kind,source) VALUES(?,'i',?,'fact','event','import:chatgpt')",
                               ('An imported event from long ago.', '2025-06-01T00:00:00+00:00')).lastrowid
            newer = db.execute("INSERT INTO facts(text,decision_id,created_at,kind,fact_kind,source) VALUES(?,'i',?,'fact','fact','import:chatgpt')",
                               ('An imported fact from this autumn.', OLD)).lastrowid
        with self.store.connect() as db:
            before = facts_module.general_count(db)
        self.assertEqual(len(self.current()), before)
        with patch.object(facts_module, 'FACTS_LIMIT', before), self.at(NOW), self.assertLogs(facts_module.LOG, 'WARNING') as logs:
            new = self.store.remember_fact('A new general fact past the limit.', 'owner-note', quote='we stopped using them')['id']
        current = self.current()
        self.assertNotIn(older, current)  # the lowest weight from another AI went
        self.assertLessEqual({newer, kept, new, *owner}, current)
        self.assertEqual(len(current), before)
        self.assertIn('facts at limit', ''.join(logs.output))
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT merged_into FROM facts WHERE id=?', (older,)).fetchone()[0], f'limit:{older}')
            self.assertTrue(db.execute('SELECT 1 FROM rule_changes WHERE ref=?', (f'limit:{older}',)).fetchone())
        with patch.object(facts_module, 'FACTS_LIMIT', 3), self.at(NOW), self.assertLogs(facts_module.LOG, 'WARNING'):
            self.store.remember_fact('Another general fact, far past the limit.', 'owner-note', quote='we stopped using them')
        current = self.current()
        self.assertNotIn(newer, current)  # only other AIs' lines go; the owner's own and kept ones stay, so the list grows
        self.assertLessEqual({kept, new, *owner}, current)

    def test_facts_set_aside_before_come_back_once_and_only_those(self):
        with self.store.connect() as db:
            add = lambda text, into, removed=OLD: db.execute(
                'INSERT INTO facts(text,decision_id,created_at,kind,removed_at,merged_into) VALUES(?,?,?,?,?,?)',
                (text, 'd', OLD, 'draft' if 'rule' in text else 'fact', removed, into)).lastrowid
            aside = add('Goes to the gym on Tuesdays.', None)
            rule = add('A draft rule: put the order number in the subject.', None)
            ended = add('Was on a trip last month.', None)
            merged = add('Prefers calls.', 'fact:1')
            removed = add('The owner removed this one.', None)
            db.execute("UPDATE facts SET merged_into='aside:'||id WHERE id IN (?,?)", (aside, rule))
            db.execute("UPDATE facts SET merged_into='expired:'||id WHERE id=?", (ended,))
            db.execute('DELETE FROM store_fixes WHERE name=?', (facts_module.ASIDE_BACK,))  # a database from before
        with self.at(NOW):
            store = assistant.Store(self.path)  # the start brings them back
        current = self.current()
        self.assertLessEqual({aside, rule}, current)
        self.assertFalse({ended, merged, removed} & current)
        with self.store.connect() as db:
            rows = db.execute('SELECT merged_into,kept_at FROM facts WHERE id IN (?,?)', (aside, rule)).fetchall()
            self.assertEqual([tuple(r) for r in rows], [(None, None), (None, None)])  # current, not marked kept
            note = db.execute('SELECT text FROM rule_changes WHERE ref=?', (facts_module.ASIDE_BACK,)).fetchall()
            self.assertEqual(len(note), 1)
            self.assertIn('Brought back 2 facts', note[0][0])
            db.execute("UPDATE facts SET removed_at=?,merged_into='aside:'||id WHERE id=?", (NOW, aside))
        self.assertEqual(store.bring_back_set_aside(), 0)  # once only
        assistant.Store(self.path)
        self.assertNotIn(aside, self.current())
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM rule_changes WHERE ref=?', (facts_module.ASIDE_BACK,)).fetchone()[0], 1)

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
