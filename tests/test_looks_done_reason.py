"""A review's Looks done reason is an event line under the to-do: never with "You" as its subject ("Explained that…",
not "You explained that…"). The review prompt says so, and a reason that still starts with "You " is stored without
it. Made-up data, no live calls."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from machine.prompts.review import review_prompt
from machine.text import no_you

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('looks_done_reason_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class Reason(unittest.TestCase):
    def test_the_prompt_asks_for_no_you(self):
        self.assertIn('never "You" as its subject', review_prompt('run1', ['g']))

    def test_a_leading_you_goes(self):
        self.assertEqual(no_you('You explained that the export is fixed'), 'Explained that the export is fixed')
        self.assertEqual(no_you('you  paid it on Nov 4'), 'Paid it on Nov 4')
        for kept in ('Sam e-signed it on Tuesday', 'Your invoice was paid', 'You and Sam agreed to skip it', 'Youth club booked', ''):
            self.assertEqual(no_you(kept), kept)

    def test_a_stored_reason_never_starts_with_you(self):
        with tempfile.TemporaryDirectory() as temp:
            store = a.Store(Path(temp) / 'e.sqlite')
            store.commit_page('g', {}, [{'account_id': 'g', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                         'title': 'Export', 'body': 'Is the export fixed?', 'deleted': False,
                                         'metadata': {'from': 'Casey <casey@example.com>', 'thread_id': 't1'}}])
            sid = store.suggest('export', 'Answer Casey about the export', 'Casey asks about the export.', [1])['id']
            self.assertEqual(store.looks_handled(sid, 'You explained that the export is fixed', [1]), {'saved': True})
            with store.connect() as db:
                hint = json.loads(db.execute('SELECT handled_hint FROM suggestions WHERE id=?', (sid,)).fetchone()[0])
            self.assertEqual(hint['reason'], 'Explained that the export is fixed')


if __name__ == '__main__':
    unittest.main()
