"""A fact's stored vector (machine/store/facts.py facts_ranked) always belongs to its current text: an edit made while
the embedding request runs never gets the old text's vector back."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
assistant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assistant)
from machine.store import facts  # noqa: E402

SETTINGS = {'model': 'm', 'dims': 4}


def event():
    return {'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': '2026-10-09T10:00:00+00:00',
            'title': 'A subject', 'body': 'Original', 'metadata': {}, 'deleted': False}


class FactVectors(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = assistant.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [event()])
        sid = self.store.suggest('facts', 'Check the vendor', 'Body', [1])['id']
        self.store.decide(sid, 'reject', 'a note from the owner', 'owner-note', 'dashboard')
        self.edited = self.store.remember_fact('The office wifi password changes every quarter.', 'owner-note')['id']
        self.kept = self.store.remember_fact('Vendor newsletters can wait a week.', 'owner-note')['id']

    def stored(self):
        with self.store.connect() as db:
            return {r[0] for r in db.execute('SELECT fact_id FROM fact_vectors')}

    def test_an_edit_during_the_embedding_request_keeps_no_vector_of_the_old_text(self):
        def slow_embed(settings, texts, timeout=15):
            self.store.edit_fact(self.edited, 'The office alarm code changes every month now.')  # the owner edits meanwhile
            return [[1.0, 0.0, 0.0, 0.0] for _ in texts]
        with patch.object(facts.embeddings, 'embed', slow_embed):
            ranked = self.store.facts_ranked('a question', self.store.facts(), SETTINGS)
        self.assertEqual(len(ranked), 2)  # this ranking still has both
        self.assertEqual(self.stored(), {self.kept})  # but only the unchanged one's vector is kept
        texts = []
        with patch.object(facts.embeddings, 'embed', lambda settings, batch, timeout=15: texts.extend(batch) or [[0.0, 1.0, 0.0, 0.0] for _ in batch]):
            self.store.facts_ranked('a question', self.store.facts(), SETTINGS)
        self.assertTrue(any('alarm code' in t for t in texts[:-1]))  # the next one embeds the new text
        self.assertEqual(self.stored(), {self.kept, self.edited})


if __name__ == '__main__':
    unittest.main()
