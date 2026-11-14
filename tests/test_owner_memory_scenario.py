"""One owner preference through its whole life, in order, on the real store and app paths with made-up data (no model,
no sends; the embedding server is a fake): learned from the owner's own chat, picked for a preparation of a to-do it
fits, corrected through a note on a to-do (the review saves it with replaces), set aside after weeks unused, brought
back, and still picked after the embedding model changes. Then the same flow without embeddings.

The preparation's facts are read the way a preparation reads them (machine/app/recall.py, then memory_use.record once
the run is admitted, which stamps them as used).

What it found: a correction saved with replaces took the old fact's note as its source, so Learning credited the old
chat message with the new value and reviews kept being offered the correcting note as not learned yet. A correction
now comes from the note that made it (Store.remember_fact)."""
import importlib.util
import re
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch

from seams import patch_everywhere

spec = importlib.util.spec_from_file_location('owner_memory_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import memory_use  # noqa: E402
from machine.app.recall import recall  # noqa: E402

EMBED = {'url': 'http://embed.invalid', 'model': 'model-one', 'dims': 256}
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.com'}], 'telegram_owner': '1000001'}
LEARNED = 'You prefer client calls in the morning, before ten.'
CORRECTED = 'You prefer client calls in the afternoon, after two.'
FILLERS = 75  # more than FACTS_GENERAL_ROOM about no one, and longer than a preparation's limit, so picking matters
EARLIER = '2026-08-01T09:00:00+00:00'  # what the Machine had learned before
T0, T1, T2, T3, T4, T5 = ('2026-09-01T09:00:00+00:00', '2026-09-02T09:00:00+00:00', '2026-09-05T09:00:00+00:00',
                          '2026-10-20T09:00:00+00:00', '2026-10-31T09:00:00+00:00', '2026-11-02T09:00:00+00:00')


PLAIN = {'title', 'text', 'none', 'the', 'a', 'in', 'for', 'about', 'with', 'is', 'how'}  # prompt and filler words


def fake_request(settings, texts, timeout=120):
    """Bag-of-words vectors, laid out differently per model: shared words mean close, and a vector of one model means
    nothing next to another's."""
    out = []
    for text in texts:
        vector = [0.0] * 768
        for word in re.findall(r'[a-z]+', text.lower()):
            if word not in PLAIN:
                vector[zlib.crc32((settings['model'] + word).encode()) % 255] += 1.0
        vector[255] += 0.01
        out.append(vector)
    return out


def mail(n):
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': T0, 'title': f'Subject {n}',
            'body': 'Body', 'metadata': {}, 'deleted': False}


class OwnerMemoryScenario(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        requests = patch.object(a.embeddings, 'request', side_effect=fake_request)
        self.requests = requests.start()
        self.addCleanup(requests.stop)

    def at(self, when):
        return patch_everywhere(a, 'now', return_value=when)

    def todo(self, key, title, body):
        self.store.commit_page('work', {}, [mail(key)])
        with self.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id=?", (f'm{key}',)).fetchone()[0]
        return self.store.suggest(key, title, body, [event])['id']

    def prepare(self, todo):
        """The facts a preparation of this to-do gets, as its prompt reads them; logged as an admitted run."""
        memory = recall(self.app, 'preparation', {'todo': todo}, 30000)
        text = memory.text('facts')
        memory_use.record(self.store, 'preparation', memory.rows(), 'job-' + todo, todo)
        return text

    def row(self, fact_id):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM facts WHERE id=?', (fact_id,)).fetchone())

    def assert_applied(self, calls, other, text):
        picked = self.prepare(calls)
        self.assertIn(text, picked)
        if text != LEARNED:
            self.assertNotIn(LEARNED, picked)
        if a.embeddings.settings(self.app.config):  # by meaning: not for a to-do it has nothing to do with
            self.assertNotIn(text, self.prepare(other))

    def retrieve_again(self, fact_id, todo, other):
        """Set aside, it still reaches a preparation of a to-do it fits through the shared retrieval (recall's retained
        block, machine/app/retained_facts.py), as the fact it still is, and not one it has nothing to do with; then
        the owner brings it back from Learning."""
        aside = [f['id'] for f in self.store.snapshot([], lean=True)['facts_aside']]
        self.assertEqual(aside, [fact_id])
        text = self.row(fact_id)['text']
        self.assertIn('- ' + text, recall(self.app, 'preparation', {'todo': todo}, 30000).text('retained'))
        self.assertNotIn(text, recall(self.app, 'preparation', {'todo': other}, 30000).text('retained'))
        self.assertEqual(self.row(fact_id)['merged_into'], f'aside:{fact_id}')  # reading it is not a use: still set aside
        self.assertEqual(self.app.action('unmerge_fact', {'expired': fact_id}, owner_dashboard=True), {'restored': 1})

    def flow(self, embed):
        self.app.config = {**CONFIG, **({'embeddings': EMBED} if embed else {})}
        with self.at(EARLIER):
            filler_todo = self.todo('chores', 'Tidy the shared drive', 'Old folders')
            self.store.decide(filler_todo, 'reject', 'we keep the drive as it is', 'note-0', 'dashboard')
            fillers = [self.store.remember_fact(f'General fact number {i} about how the owner works.', 'note-0', quote='we keep the drive as it is')['id']
                       for i in range(FILLERS)]
        with self.at(T0):
            calls = self.todo('calls', 'Plan client calls for the renewal', 'Set up calls with the client team about the renewal')
            other = self.todo('hosting', 'Pay the hosting invoice', 'The hosting invoice for October is due')
            moved = self.todo('moved', 'Answer the client about the call', 'They ask when the call can be')

        # 1. Learned from the owner's own chat ("remember…"), as the chat's remember_fact saves it
        with self.at(T0):
            self.app.action('feedback_reply', {'text': 'remember that I like client calls early', 'message_id': '501', 'timestamp': 0, 'reply_to_id': ''})
            first = self.app.action('remember_fact', {'text': LEARNED, 'kind': 'preference', '_owner_chat': True, 'quote': 'I like client calls early'})['id']
        self.assertEqual(self.row(first)['decision_id'], 'telegram-said:501')

        # 2. Applied: picked for a preparation of a to-do it fits
        with self.at(T1):
            self.assert_applied(calls, other, LEARNED)

        # 3. Corrected: a note on another to-do, which the review saves in place of the old one (replaces)
        with self.at(T2):
            self.store.decide(moved, 'snooze', 'client calls work better in the afternoon now', 'note-1', 'dashboard')
            fixed = self.app.action('remember_fact', {'text': CORRECTED, 'kind': 'preference', 'decision_id': 'note-1', 'replaces': [first],
                                                      'quote': 'client calls work better in the afternoon'})
            corrected = fixed['id']
            self.assertEqual(fixed['merged'], 1)
            self.assertEqual(self.row(corrected)['decision_id'], 'note-1')  # it came from the newer note, not the old chat message
            self.assertNotIn('note-1', self.store.notes_to_learn())  # so later reviews aren't offered that note again
            self.assert_applied(calls, other, CORRECTED)
        self.assertEqual(self.row(first)['merged_into'], f'fact:{corrected}')

        # 4. Set aside after weeks unused (the review's room pass), while other facts were used; then brought back
        with self.at(T3):
            self.store.mark_used(fillers)  # preparations of other to-dos picked these lately
        with self.at(T4):
            self.store.retire_expired()
            self.assertEqual(self.row(corrected)['merged_into'], f'aside:{corrected}')
            self.assertNotIn(CORRECTED, self.prepare(calls))
            self.retrieve_again(corrected, calls, other)
            self.assert_applied(calls, other, CORRECTED)

        # 5. Another embedding model: the vectors are made again, and the right preference is still picked
        if embed:
            self.app.config = {**CONFIG, 'embeddings': {**EMBED, 'model': 'model-two'}}
            with self.at(T5):
                self.assert_applied(calls, other, CORRECTED)
            with self.store.connect() as db:
                models = {r[0] for r in db.execute('SELECT model FROM fact_vectors WHERE fact_id IN (SELECT id FROM facts WHERE removed_at IS NULL)')}
                vector = a.embeddings.unpack(db.execute('SELECT vector FROM fact_vectors WHERE fact_id=?', (corrected,)).fetchone()[0])
            self.assertEqual(models, {'model-two:256'})
            fresh = a.embeddings.embed(self.app.config['embeddings'], [a.embeddings.document('none', CORRECTED)])[0]
            self.assertAlmostEqual(a.embeddings.cosine(vector, fresh), 1.0, places=5)

        # Never revived: the old value stays behind the correction through every step
        self.assertEqual(self.row(first)['merged_into'], f'fact:{corrected}')
        self.assertNotIn(LEARNED, [f['text'] for f in self.store.facts()])
        self.assertEqual(self.requests.called, embed)

    def test_with_embeddings(self):
        self.flow(True)

    def test_without_embeddings(self):
        self.flow(False)


if __name__ == '__main__':
    unittest.main()
