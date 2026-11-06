"""Importers skip and count a row they can't take instead of failing the whole page or poll (machine/sources/rows.py).
Synthetic rows only, no live reads."""
import base64
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

from machine.sources.rows import SKIPPED, Skips
from seams import patch_everywhere
import ms_graph
from test_connectors import FEED, RSS, Response, a

H = a.CONNECTOR_HELPERS


class SkipsTests(unittest.TestCase):
    def test_counts_refused_rows_by_reason_and_keeps_the_rest(self):
        def convert(row):
            if row == 'odd':
                raise a.SourceError('sample_invalid_row')
            return row['n']
        skipped = Skips('sample_malformed')
        self.assertEqual(skipped.every([{'n': 1}, 'odd', {}, {'n': 2}], convert), [(1, {'n': 1}), (2, {'n': 2})])
        self.assertEqual(dict(skipped), {'sample_invalid_row': 1, 'sample_malformed': 1})
        state = {'skipped_rows': {'sample_invalid_row': 3}}
        self.assertEqual(skipped.check().note(state), 2)
        self.assertEqual(state['skipped_rows'], {'sample_invalid_row': 4, 'sample_malformed': 1})

    def test_a_failed_read_is_no_odd_row(self):
        for error in (a.SourceError('sample_http', 503), a.SourceError('network:TimeoutError:sample')):
            with self.subTest(error=str(error)), self.assertRaises(a.SourceError):
                Skips('sample_malformed').take(lambda: (_ for _ in ()).throw(error))
        with self.assertRaises(KeyError):  # without a malformed reason, a missing field still raises
            Skips().take(lambda: {}['n'])

    def test_a_page_of_only_refused_rows_fails_visibly(self):
        skipped = Skips('sample_malformed')
        self.assertEqual(skipped.every([{}] * 9, lambda row: row['n']), [])
        self.assertIs(skipped.check(), skipped)  # a few odd rows: fine
        skipped.take(lambda: {}['n'])
        with self.assertRaises(a.SourceError) as caught:
            skipped.check()
        self.assertEqual(caught.exception.category, 'sample_malformed')
        self.assertIs(Skips().take(lambda: (_ for _ in ()).throw(a.SourceError('x'))), SKIPPED)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'a.sqlite')

    def kept(self, account_id):
        return self.store.events([account_id])


TELEGRAM = {'id': 'personal-telegram', 'service': 'telegram'}


def telegram_row(mid, **changes):
    return {'chat_id': '1001', 'msg_id': mid, 'occurred_at': '2026-10-09T12:00:00+00:00', 'from_me': False, 'text': 'Hello',
            'chat_name': 'Sample chat', 'chat_kind': 'dm', 'sender_name': 'Sample person', 'sender_id': '7', **changes}


class TelegramTests(Base):
    def sync(self, rows):
        source = types.SimpleNamespace(profile=lambda: {}, messages=lambda after: rows)
        with patch_everywhere(a, 'now', return_value='2026-10-10T12:00:00+00:00'):
            return a.sync_telegram(self.store, {}, TELEGRAM, source)

    def test_odd_rows_are_skipped_and_counted(self):
        result = self.sync([telegram_row(1), telegram_row('two'), telegram_row(3, occurred_at='2026-10-09T12:00:00'),
                            telegram_row(4, occurred_at=None), telegram_row(5)])
        self.assertEqual((result['events'], result['skipped']), (2, 3))
        self.assertEqual(len(self.kept(TELEGRAM['id'])), 2)
        self.assertEqual(self.store.checkpoint(TELEGRAM['id'])['skipped_rows'],
                         {'telegram_invalid_message': 2, 'telegram_missing_timezone': 1})

    def test_only_odd_rows_still_fail(self):
        with self.assertRaises(a.SourceError):
            self.sync([telegram_row(str(n)) for n in range(10)])
        self.assertIsNone(self.store.checkpoint(TELEGRAM['id']))


SLACK = {'id': 'work-slack', 'service': 'slack', 'slack_host': 'example.slack.com', 'user_id': 'U1'}


class SlackTests(Base):
    def test_a_message_without_a_timestamp_is_skipped_not_failing_the_channel(self):
        self.store.commit_page(SLACK['id'], {'mode': 'bootstrap', 'phase': 'scan', 'index': 0, 'after': '0',
                                             'channels': [{'id': 'C1', 'name': 'general', 'type': 'channel', 'threads': []}]},
                               [], record_sync=False)
        messages = [{'ts': '1791000000.000100', 'user': 'U2', 'text': 'First'}, {'ts': 'soon', 'text': 'Odd'},
                    {'subtype': 'message_deleted'}, {'ts': '1791000001.000100', 'user': 'U2', 'text': 'Second'}]
        source = types.SimpleNamespace(profile=lambda: {}, get=lambda method, params: {'messages': messages, 'has_more': False})
        result = a.sync_slack(self.store, {}, SLACK, source)
        self.assertEqual((result['events'], result['skipped']), (2, 2))
        self.assertEqual(sorted(r['body'] for r in self.kept(SLACK['id'])), ['First', 'Second'])
        self.assertEqual(self.store.checkpoint(SLACK['id'])['skipped_rows'], {'invalid_slack_timestamp': 1, 'slack_invalid_message': 1})


MAIL = {'id': 'work-mail', 'email': 'owner@example.com'}


def mail(mid, data):
    return {'id': mid, 'threadId': 't-' + mid, 'internalDate': '1791000000000', 'labelIds': ['INBOX'],
            'payload': {'mimeType': 'text/plain', 'headers': [{'name': 'Subject', 'value': 'Sample ' + mid},
                                                             {'name': 'From', 'value': 'sample@example.com'}],
                        'body': {'data': data}}}


class GmailTests(Base):
    def test_a_message_it_cannot_decode_is_skipped_and_the_page_moves_on(self):
        good = base64.urlsafe_b64encode(b'Hello').decode()
        messages = {'m1': mail('m1', good), 'm2': mail('m2', 'A'), 'm3': {**mail('m3', good), 'internalDate': None}}

        class Fake:
            def __init__(self, *_): pass
            def profile(self): return {'historyId': '9'}
            def get(self, resource, params=None):
                return {'messages': [{'id': m} for m in messages]} if resource == 'messages' else messages[resource.split('/')[1]]
        with patch_everywhere(a, 'Gmail', Fake):
            result = a.sync_gmail(self.store, {}, MAIL)
        self.assertEqual((result['events'], result['skipped']), (1, 2))
        self.assertEqual([r['source_id'] for r in self.kept(MAIL['id'])], ['m1'])
        state = self.store.checkpoint(MAIL['id'])
        self.assertEqual(state['mode'], 'incremental')  # the window finished: no page held up by one message
        self.assertEqual(state['skipped_rows'], {'invalid_message': 1, 'invalid_message_encoding': 1})


CALENDAR = {'id': 'work-calendar', 'email': 'owner@example.com', 'service': 'calendar'}


def appointment(source, start='2026-10-12T09:00:00+02:00'):
    return {'id': source, 'summary': 'Sample meeting', 'status': 'confirmed', 'start': {'dateTime': start},
            'end': {'dateTime': start.replace('09:00', '10:00')}, 'htmlLink': 'https://calendar.google.com/calendar/event?eid=x'}


class CalendarTests(Base):
    def test_an_event_it_cannot_read_is_skipped_and_not_removed_as_absent(self):
        self.store.commit_page(CALENDAR['id'], {}, [a.calendar_event(CALENDAR, appointment('kept-before'), 'UTC')])
        items = [appointment('good'), {**appointment('no-start'), 'start': {}},
                 {'id': 'kept-before', 'unreadable': 'outlook_invalid_event'}]

        class Fake:
            def __init__(self, *_): pass
            def profile(self): return {'id': 'owner@example.com', 'timeZone': 'Europe/Brussels'}
            def get(self, method, params): return {'items': items, 'nextSyncToken': 'done'}
        with patch_everywhere(a, 'Calendar', Fake), patch_everywhere(a, 'now', return_value='2026-10-09T12:00:00+00:00'):
            result = a.sync_calendar(self.store, {}, CALENDAR)
        self.assertEqual(result['skipped'], 2)
        self.assertEqual(sorted(r['source_id'] for r in self.kept(CALENDAR['id']) if not r['deleted']), ['good', 'kept-before'])
        self.assertEqual(self.store.checkpoint(CALENDAR['id'])['skipped_rows'],
                         {'calendar_invalid_event': 1, 'outlook_invalid_event': 1})

    def test_an_outlook_event_without_a_start_comes_as_unreadable_not_failing_the_page(self):
        good = {'id': 'g1', 'subject': 'Sample', 'start': {'dateTime': '2026-10-12T09:00:00.0000000', 'timeZone': 'UTC'},
                'end': {'dateTime': '2026-10-12T10:00:00.0000000', 'timeZone': 'UTC'}}
        items = ms_graph.calendar_items([good, {'id': 'g2', 'subject': 'Odd', 'start': {}, 'end': {}}, 'not an event'], 'owner@example.com')
        self.assertEqual(items[0]['id'], 'g1')
        self.assertEqual(items[1:], [{'id': 'g2', 'unreadable': 'outlook_invalid_event'}, {'id': '', 'unreadable': 'outlook_invalid_event'}])


ANDROID = {'id': 'personal-android', 'node_id': 'phone'}


class AndroidTests(Base):
    def test_a_notification_it_cannot_take_is_skipped(self):
        rows = [{'key': 'k1', 'packageName': 'com.example.chat', 'postTimeMs': 1791000000000, 'title': 'Sample'},
                {'key': 'k2', 'packageName': 'com.example.chat', 'postTimeMs': 'soon'}, 'not a notification']
        source = types.SimpleNamespace(snapshot=lambda: {'enabled': True, 'connected': True, 'count': 3, 'notifications': rows})
        result = a.sync_android(self.store, {}, ANDROID, source)
        self.assertEqual((result['events'], result['skipped']), (1, 2))
        self.assertEqual(self.store.checkpoint(ANDROID['id'])['skipped_rows'], {'android_invalid_notification': 2})


class FeedTests(Base):
    def test_a_feed_item_without_a_date_is_skipped(self):
        feed = RSS.replace(b'Wed, 14 Oct 2026 09:00:00 +0200', b'not a date')
        rss = a.load_connector('rss')
        with patch('urllib.request.urlopen', side_effect=lambda *_, **__: Response(feed)):
            self.assertIsNone(rss.check({}, FEED, H))  # one odd item is no reason to refuse the feed at setup
            result = a.sync_source(self.store, {}, FEED)
        self.assertEqual((result['events'], result['skipped']), (1, 1))
        self.assertEqual(self.store.checkpoint(FEED['id'])['skipped_rows'], {'rss_invalid_timestamp': 1})


LINKEDIN = {'id': 'linkedin-sample', 'service': 'linkedin'}


class LinkedInTests(unittest.TestCase):
    def test_an_odd_message_is_skipped_and_counted(self):
        li = a.load_connector('linkedin')
        good = {'urn': 'urn:li:msg_message:1', 'conversation': 'urn:li:msg_conversation:2', 'at': 1791000000000, 'fromMe': False}
        skipped = H.Skips('linkedin_invalid_message')
        found = li.events(LINKEDIN, {'messages': [good, {**good, 'at': 'soon'}, None]}, H, skipped)
        self.assertEqual(len(found), 1)
        self.assertEqual(dict(skipped), {'linkedin_invalid_message': 2})
        with self.assertRaises(a.SourceError):
            li.events(LINKEDIN, {'messages': [None] * 10}, H)


if __name__ == '__main__':
    unittest.main()
