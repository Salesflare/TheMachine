"""The quoted-history marker (trim_quoted_history) is for the model only: the chat, the original's dialog, the Events
list and the Graph show an email without it, the reply's new text apart from its quoted history; the model's own
view of the body keeps it."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location('quoted_marker_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

FIRST = ('Here are my link details. Once approved, I will move forward with the insertion.\n'
         'Post: blog.example.com\nLink: example.net\nRegards\nSam Z')
FIRST_MAIL = FIRST + '\n\nOn Mon, 26 Oct 2026 at 10:00, Owner <me@example.com> wrote:\n> Sounds good, send me the details.\n> Owner'
# A later email from the same person: their own new text, then the first email quoted under it
SECOND_MAIL = ('For ABC exchange, here is the alternative.\nLink: https://example.org/\nRegards\nSam Z\n\n'
               'On Wed, 28 Oct 2026 at 08:40, Sam Z <sam@example.net> wrote:\n' + '\n'.join('> ' + line for line in FIRST_MAIL.split('\n')))


def fixture(folder):
    """Two emails from Sam on one to-do, stored the way mail sync stores them (with the marker); the dashboard test
    (test_quoted_history_dashboard.mjs) reads its chat and originals from here."""
    store = a.Store(Path(folder) / 'events.sqlite')
    bodies = [a.trim_quoted_history(FIRST_MAIL, 'Re: Link')[0], a.trim_quoted_history(SECOND_MAIL, 'Re: Link')[0]]
    event = lambda sid, body, at: {'account_id': 'work', 'source_id': sid, 'kind': 'gmail.message', 'occurred_at': at, 'title': 'Re: Link',
                                   'body': body, 'metadata': {'from': 'Sam Z <sam@example.net>'}, 'deleted': False}
    store.commit_page('work', {}, [event('m1', bodies[0], '2026-10-28T08:40:00+00:00'), event('m2', bodies[1], '2026-10-28T08:47:00+00:00')], None)
    sid = store.suggest('task', 'Reply to Sam', 'Sam sent the link details.', [1, 2])['id']
    app = object.__new__(a.App)
    app.store = store
    app.config = {'accounts': [], 'database': str(Path(folder) / 'events.sqlite')}
    return app, sid, bodies


class QuotedMarker(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.app, self.sid, self.bodies = fixture(temp.name)
        self.store = self.app.store
        self.assertTrue(all('[Quoted earlier messages:' in b for b in self.bodies))

    def test_shown_body_drops_the_marker_and_keeps_the_history(self):
        body, clipped = a.shown_body(self.bodies[0])
        self.assertEqual(body, FIRST + '\n\nOn Mon, 26 Oct 2026 at 10:00, Owner <me@example.com> wrote:\n> Sounds good, send me the details.\n> Owner')
        self.assertFalse(clipped)
        long = a.trim_quoted_history('Thanks!\n\nOn Mon, Ann <a@b.c> wrote:\n' + '> old line\n' * 1000)[0]
        self.assertEqual(a.shown_body(long)[1], True)
        self.assertNotIn('Quoted earlier', a.shown_body(long)[0])
        self.assertEqual(a.shown_body('Plain [note]'), ('Plain [note]', False))

    def test_chat_shows_each_new_message_with_its_history_apart(self):
        with self.store.connect() as db:
            owner, _ = self.app.card_chat_service(db, self.sid)
        sources = [i for i in owner if i['kind'] == 'source']
        self.assertNotIn('Quoted earlier', json.dumps(owner))
        self.assertNotIn('separate signals', json.dumps(owner))
        self.assertEqual([s['text'] for s in sources], [FIRST, 'For ABC exchange, here is the alternative.\nLink: https://example.org/\nRegards\nSam Z'])
        # The second block is a later email of its own; the first one is in its quoted history
        self.assertTrue(sources[1]['quoted'].startswith('On Wed, 28 Oct 2026 at 08:40, Sam Z <sam@example.net> wrote:\n> Here are my link details.'))
        self.assertTrue(sources[0]['quoted'].startswith('On Mon, 26 Oct 2026'))

    def test_originals_events_and_graph_rows_have_no_marker(self):
        shown = self.app.originals(self.sid)
        self.assertEqual(len(shown), 2)
        self.assertFalse(any('Quoted earlier' in o['body'] for o in shown))
        self.assertTrue(shown[1]['body'].startswith('For ABC exchange') and 'Sam Z <sam@example.net> wrote:' in shown[1]['body'])
        short = {'kind': 'gmail.message', 'metadata': {}, 'body': 'Ok!\n\n[Quoted earlier messages: first 9 of 9 characters kept. Earlier messages in this thread are separate signals.]\nOn x wrote:'}
        self.assertNotIn('Quoted earlier', a.event_glance(short, [])['preview'])

    def test_the_model_still_reads_the_marker(self):
        self.assertTrue(all('[Quoted earlier messages:' in v['body'] for v in self.store.event_views([1, 2])))
        self.assertTrue(all('[Quoted earlier messages:' in r['body'] for r in self.store.events(['work'], '', 10)))


if __name__ == '__main__':
    unittest.main()
