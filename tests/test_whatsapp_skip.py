import importlib.util
from pathlib import Path
import tempfile, unittest
from unittest.mock import patch
spec = importlib.util.spec_from_file_location('assistant_wa_skip', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
account = {'id': 'personal-whatsapp', 'identity_sha256': a.hashlib.sha256(b'123@s.whatsapp.net').hexdigest()}


def message(**changes):  # synthetic rows only, shaped like wacli's `messages list`
    raw = {'ChatJID': '12345@s.whatsapp.net', 'MsgID': 'SYNTHETIC-1', 'Timestamp': '2026-10-09T12:00:00Z', 'FromMe': False,
           'SenderJID': '12345@s.whatsapp.net', 'Text': 'Hello', 'ChatName': 'Sample chat'}
    raw.update(changes)
    return raw


class WhatsAppOddRowsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.store = a.Store(Path(self.tmp.name) / 'a.sqlite')

    def tearDown(self):
        self.tmp.cleanup()

    def sync(self, rows):
        src = a.WhatsApp({}, account)
        with patch.object(src, 'profile', return_value={}), patch.object(src, 'read', return_value={'messages': rows}):
            return a.sync_whatsapp(self.store, {}, account, src)

    def test_odd_rows_are_skipped_and_counted_not_failing_the_source(self):
        odd = [message(ChatJID='120363000000000000@newsletter', MsgID='SYNTHETIC-CHANNEL', MediaType='image'),  # a Channel post
               message(ChatJID='status@broadcast', MsgID='SYNTHETIC-STATUS'),
               message(MsgID='imported_synthetic'),
               message(MsgID='SYNTHETIC-NOZONE', Timestamp='2026-10-09T12:00:00'),
               message(MsgID='SYNTHETIC-BADTEXT', Text=['not', 'text']),
               'not a row']
        result = self.sync([message(), *odd, message(MsgID='SYNTHETIC-2', Text='Second')])
        self.assertEqual((result['events'], result['filtered']), (2, 6))
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE kind='whatsapp.message' AND deleted=0").fetchone()[0], 2)
        state = self.store.checkpoint(account['id'])
        self.assertEqual(state['mode'], 'incremental')
        self.assertEqual(state['skipped_messages'], {'whatsapp_invalid_content': 1, 'whatsapp_invalid_message': 4, 'whatsapp_missing_timezone': 1})

    def test_a_window_with_only_a_few_odd_rows_still_syncs(self):
        self.assertEqual(self.sync([message(ChatJID='1@newsletter')])['events'], 0)
        self.assertEqual(self.store.checkpoint(account['id'])['skipped_messages'], {'whatsapp_invalid_message': 1})

    def test_a_window_of_only_odd_rows_still_fails_visibly(self):
        with self.assertRaises(a.SourceError) as caught:
            self.sync([message(ChatJID='1@newsletter', MsgID=f'SYNTHETIC-{n}') for n in range(10)])
        self.assertEqual(caught.exception.category, 'whatsapp_invalid_message')
        self.assertIsNone(self.store.checkpoint(account['id']))


if __name__ == '__main__':
    unittest.main()
