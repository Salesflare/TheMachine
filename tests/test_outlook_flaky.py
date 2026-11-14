"""An Outlook mail round against a Graph that fails part of its requests (machine/sources/gmail.py Round, ms_graph.budget).

For hours Graph can answer about half of one mailbox's requests with a 5xx or not at all, whatever the request, and serve
each on another try. A round makes many requests in a row, so a round that failed on its first 5xx never finished and no
mail came in. Now each read is retried a few times within the round's time, a message that still fails waits for the
next round while what was read is kept and the cursor moves on, and every message is read exactly once.
No network: urlopen is the fake Graph of test_ms_graph."""
import collections
import datetime as dt
import io
import json
import random
import unittest
import urllib.error
import urllib.parse
from unittest import mock

import ms_graph
from machine.sources import gmail
import test_ms_graph as t

a = t.a


class FlakyGraph(t.FakeGraph):
    """The fake Graph, failing the Graph requests `fails(n)` picks (n counts them from 1), with a 502 or no answer.
    `served` counts each message's MIME as it was handed out, `graph` every Graph request asked."""

    def __init__(self):
        super().__init__()
        self.fails, self.graph, self.failed, self.served = None, 0, 0, collections.Counter()

    def __call__(self, request, timeout=None):
        if request.full_url.startswith(t.G):
            self.graph += 1
            if self.fails and self.fails(self.graph):
                self.failed += 1
                if self.graph % 3 == 0:
                    raise TimeoutError()
                raise t.http_error(request.full_url, 502)
        answer = super().__call__(request, timeout)
        path = urllib.parse.urlsplit(request.full_url).path
        if path.endswith('/$value') and '/attachments/' not in path:
            self.served[urllib.parse.unquote(path.split('/')[4])] += 1
        return answer


class FlakyBase(t.Base):
    def setUp(self):
        super().setUp()
        self.fake = FlakyGraph()
        patcher = mock.patch.object(ms_graph.urllib.request, 'urlopen', self.fake); patcher.start(); self.addCleanup(patcher.stop)
        pauses = mock.patch.object(ms_graph, '_pause'); self.pause = pauses.start(); self.addCleanup(pauses.stop)
        a.sync_gmail(self.store, self.config, self.mail)  # an empty mailbox's first import: incremental from here
        a.sync_gmail(self.store, self.config, self.mail)
        self.assertEqual(self.store.checkpoint('acme-outlook')['mode'], 'incremental')
        self.fake.graph = 0

    def add(self, count, start=0):
        for i in range(start, start + count):
            stamp = f'2099-01-01T08:{i:02d}:00Z'
            self.fake.add(f'm{i}', t.INBOX, stamp, stamp, t.mime(f'Note {i}', 'Bo <bo@client.test>', 'alex@acme.test', f'Body {i}', f'<m{i}@client.test>'))
        return {f'm{i}' for i in range(start, start + count)}

    def stored(self):
        with self.store.connect() as db:
            return collections.Counter(r[0] for r in db.execute("SELECT source_id FROM events WHERE account_id='acme-outlook'"))

    def errors(self):
        with self.store.connect() as db:
            row = db.execute("SELECT error, failures FROM checkpoints WHERE account_id='acme-outlook'").fetchone()
        return (row[0], row[1] or 0)


class FlakyGraphRounds(FlakyBase):
    def test_every_other_request_failing_reads_each_message_once_in_one_round(self):
        wanted = self.add(8)
        self.fake.fails = lambda n: n % 2 == 0
        result = a.sync_gmail(self.store, self.config, self.mail)
        self.assertEqual(set(self.stored()), wanted)
        self.assertEqual(set(self.fake.served), wanted)
        self.assertEqual(set(self.fake.served.values()), {1})  # each message's content read once
        self.assertGreater(self.fake.failed, 0)
        self.assertNotIn('waiting', self.store.checkpoint('acme-outlook'))
        self.assertEqual(self.errors(), (None, 0))
        self.assertNotIn('more', result)

    def test_rounds_keep_what_they_read_and_read_every_message_exactly_once(self):
        """Half of all requests failing at random, also each read's retries: every round with anything from Graph is a
        success, and within a few rounds every message is in, each read once."""
        wanted = self.add(30)
        chance = random.Random(1393)
        self.fake.fails = lambda n: chance.random() < 0.5
        rounds = 0
        while rounds < 40 and (set(self.stored()) != wanted or self.store.checkpoint('acme-outlook').get('waiting')):
            rounds += 1
            before = len(self.stored())
            try:
                result = a.sync_gmail(self.store, self.config, self.mail)
            except a.SourceError as error:  # nothing from Graph at all: a transient failure, nothing lost
                self.assertTrue(a.transient(error))
                self.assertEqual(len(self.stored()), before)
                continue
            self.assertEqual(self.errors(), (None, 0))  # a partial round is a success, not a failure
        self.assertLess(rounds, 40)
        self.assertGreater(rounds, 1)
        self.assertEqual(set(self.stored()), wanted)
        self.assertEqual(set(self.stored().values()), {1})
        self.assertEqual(set(self.fake.served), wanted)
        self.assertEqual(set(self.fake.served.values()), {1})

    def test_a_message_graph_keeps_failing_waits_and_never_holds_up_the_rest(self):
        wanted = self.add(5)
        self.fake.fail['GET /me/messages/m2/$value'] = 502
        for _ in range(3):
            result = a.sync_gmail(self.store, self.config, self.mail)
        self.assertEqual(set(self.stored()), wanted - {'m2'})
        state = self.store.checkpoint('acme-outlook')
        self.assertEqual(list(state['waiting']), ['m2'])
        self.assertEqual(state['waiting']['m2']['tries'], 3)
        self.assertEqual(state['history_id'], '2099-01-01T08:04:00Z')  # the cursor moved on past it
        self.assertEqual((result['waiting'], self.errors()), (1, (None, 0)))  # noted, not failing the rounds
        since = state['waiting']['m2']['since']
        del self.fake.fail['GET /me/messages/m2/$value']
        self.fake.graph = 0
        a.sync_gmail(self.store, self.config, self.mail)
        self.assertEqual(set(self.stored()), wanted)
        self.assertEqual(set(self.fake.served.values()), {1})
        self.assertEqual(self.fake.graph, 1 + 2)  # the listing, then m2: the rest isn't read again
        self.assertNotIn('waiting', self.store.checkpoint('acme-outlook'))
        self.assertTrue(since)

    def test_a_message_gone_while_waiting_is_tombstoned(self):
        self.add(2)
        self.fake.fail['GET /me/messages/m1/$value'] = 504
        a.sync_gmail(self.store, self.config, self.mail)
        del self.fake.fail['GET /me/messages/m1/$value']
        del self.fake.messages['m1']
        a.sync_gmail(self.store, self.config, self.mail)
        self.assertNotIn('waiting', self.store.checkpoint('acme-outlook'))

    def test_a_dead_graph_fails_the_round_and_loses_nothing(self):
        wanted = self.add(4)
        self.fake.fails = lambda n: True
        with self.assertRaises(a.SourceError) as got:
            a.sync_gmail(self.store, self.config, self.mail)
        self.assertTrue(a.transient(got.exception))
        self.assertLessEqual(self.fake.graph, ms_graph.READ_TRIES)  # the listing's tries, nothing more
        self.fake.fails = None
        a.sync_gmail(self.store, self.config, self.mail)
        self.assertEqual(set(self.stored()), wanted)

    def test_graph_failing_every_read_stops_the_round_after_a_few_messages(self):
        self.add(10)
        self.fake.fails = lambda n: n > 1  # the listing answers, then nothing does
        a.sync_gmail(self.store, self.config, self.mail)  # listed: a success, every message waiting
        tried = self.fake.graph
        self.assertLessEqual(tried, 1 + gmail.FAILED_IN_A_ROW * ms_graph.READ_TRIES)
        state = self.store.checkpoint('acme-outlook')
        self.assertEqual(len(state['waiting']), 10)
        self.assertEqual(sum(v['tries'] for v in state['waiting'].values()), gmail.FAILED_IN_A_ROW)
        self.fake.fails = lambda n: True
        with self.assertRaises(a.SourceError):  # nothing new listed or read: a failure (counted, reported only if it lasts)
            a.sync_gmail(self.store, self.config, self.mail)
        self.assertEqual(len(self.store.checkpoint('acme-outlook')['waiting']), 10)  # nothing dropped

    def test_the_rounds_time_up_leaves_the_rest_waiting(self):
        wanted = self.add(3)
        with mock.patch.object(gmail, 'ROUND_SECONDS', 0):
            a.sync_gmail(self.store, self.config, self.mail)
        self.assertEqual(len(self.store.checkpoint('acme-outlook')['waiting']), 3)
        self.assertFalse(self.stored())
        a.sync_gmail(self.store, self.config, self.mail)
        self.assertEqual(set(self.stored()), wanted)
        self.assertEqual(set(self.fake.served.values()), {1})

    def test_a_healthy_graph_costs_no_extra_requests(self):
        self.add(3)
        a.sync_gmail(self.store, self.config, self.mail)
        folders = len(self.fake.folders)  # the well-known folders, looked up once per run
        self.assertEqual(self.fake.graph, 1 + folders + 3 * 2)
        self.fake.graph = 0
        result = a.sync_gmail(self.store, self.config, self.mail)
        self.assertEqual(self.fake.graph, 1)  # the listing only: the last change isn't read again
        self.assertEqual((result['events'], self.fake.failed), (0, 0))
        self.pause.assert_not_called()
        self.fake.messages['m2']['lastModifiedDateTime'] = '2099-01-01T09:00:00Z'  # changed: read again
        a.sync_gmail(self.store, self.config, self.mail)
        self.assertEqual(self.fake.served['m2'], 2)


class ReadRetries(FlakyBase):
    def answers(self, *statuses):
        replies = list(statuses)

        def urlopen(request, timeout=None):
            status = replies.pop(0)
            if status == 'timeout':
                raise TimeoutError()
            if status != 200:
                raise urllib.error.HTTPError(t.G, status, 'no', {'Retry-After': '30'} if status == 429 else {}, io.BytesIO())
            return t.Response(json.dumps({'mail': 'alex@acme.test'}).encode())
        return mock.patch.object(ms_graph.urllib.request, 'urlopen', urlopen), replies

    def me(self):
        return ms_graph.call(self.config, a.credential, self.mail, 'me')

    def test_a_read_in_a_round_is_tried_again_on_a_5xx_or_no_answer(self):
        patcher, left = self.answers(504, 'timeout', 200)
        with patcher, mock.patch.object(ms_graph, 'token', return_value='test'), ms_graph.budget(60):
            self.assertEqual(self.me()['mail'], 'alex@acme.test')
        self.assertEqual((left, self.pause.call_count), ([], 2))

    def test_three_tries_at_most(self):
        patcher, left = self.answers(502, 500, 503, 200)
        with patcher, mock.patch.object(ms_graph, 'token', return_value='test'), ms_graph.budget(60):
            with self.assertRaises(ms_graph.GraphError) as got:
                self.me()
        self.assertEqual((got.exception.status, left), (503, [200]))

    def test_outside_a_round_a_long_retry_after_or_another_error_it_is_tried_once(self):
        for statuses, budget in (((504, 200), None), ((429, 200), 60), ((400, 200), 60)):
            patcher, left = self.answers(*statuses)
            with patcher, mock.patch.object(ms_graph, 'token', return_value='test'):
                with self.assertRaises(ms_graph.GraphError), ms_graph.budget(budget) if budget else mock.MagicMock():
                    self.me()
            self.assertEqual(left, [200])
        self.pause.assert_not_called()

    def test_a_write_is_never_repeated(self):
        patcher, left = self.answers(504, 200)
        with patcher, mock.patch.object(ms_graph, 'token', return_value='test'), ms_graph.budget(60):
            with self.assertRaises(ms_graph.GraphError):
                ms_graph.call(self.config, a.credential, self.mail, 'sendMail', {}, body={}, write=True)
        self.assertEqual(left, [200])

    def test_a_short_retry_after_is_honored(self):
        with mock.patch.object(ms_graph, 'left', return_value=60):
            self.assertEqual(ms_graph._again(503, {'Retry-After': '4'}, 1), 4)
            self.assertIsNone(ms_graph._again(503, {'Retry-After': '120'}, 1))
            self.assertLessEqual(ms_graph._again(502, {}, 2), 3)
        with mock.patch.object(ms_graph, 'left', return_value=0.5):
            self.assertIsNone(ms_graph._again(502, {}, 2))  # never waits past the round


class OtherGraphRounds(t.Base):
    """The calendar, photos and birthdays read Graph in rounds too: a read Graph fails now and then is tried again there."""

    def setUp(self):
        super().setUp()
        self.fake = FlakyGraph()
        patcher = mock.patch.object(ms_graph.urllib.request, 'urlopen', self.fake); patcher.start(); self.addCleanup(patcher.stop)
        pauses = mock.patch.object(ms_graph, '_pause'); self.pause = pauses.start(); self.addCleanup(pauses.stop)
        self.fake.delta = [{'value': [{'id': 'e1', 'subject': 'Demo', 'isAllDay': False,
                                       'start': {'dateTime': '2099-01-03T09:00:00.0000000', 'timeZone': 'UTC'},
                                       'end': {'dateTime': '2099-01-03T10:00:00.0000000', 'timeZone': 'UTC'}}],
                            '@odata.deltaLink': t.G + '/me/calendarView/delta?$deltatoken=one'}]

    def test_a_calendar_round_reads_on_through_a_5xx_and_no_answer(self):
        self.fake.fails = lambda n: n in (1, 3)  # the calendar's own read answers 502, the delta not at all, each once
        with t.patch_everywhere(a, 'now', return_value='2099-01-01T00:00:00+00:00'):
            result = a.sync_calendar(self.store, self.config, self.cal)
        self.assertEqual((result['events'], self.fake.failed, self.pause.call_count), (1, 2, 2))
        with self.store.connect() as db:
            row = db.execute('SELECT error, failures FROM checkpoints WHERE account_id=?', (self.cal['id'],)).fetchone()
        self.assertEqual((row[0], row[1] or 0), (None, 0))  # nothing failed, so nothing reaches the error feed

    def test_a_calendar_round_that_keeps_failing_is_a_passing_failure(self):
        self.fake.fails = lambda n: True
        with t.patch_everywhere(a, 'now', return_value='2099-01-01T00:00:00+00:00'), self.assertRaises(a.SourceError) as got:
            a.sync_calendar(self.store, self.config, self.cal)
        self.assertEqual(self.fake.graph, ms_graph.READ_TRIES)
        self.assertTrue(a.transient(got.exception))  # only reported when it keeps happening

    def test_photos_and_birthdays_read_inside_a_round(self):
        import birthdays_app
        import ms_photos
        rounds = []

        def call(*args, **kwargs):
            rounds.append(ms_graph.left())
            return {'value': [{'id': 'b', 'name': 'Birthdays'}]}
        with mock.patch.object(ms_graph, 'call', call), mock.patch.object(ms_graph, 'grant', lambda *args: (set(), set())):
            ms_photos.step(self.store.connect, {'accounts': [self.mail]}, None, '2099-01-01T00:00:00+00:00')
            self.assertEqual(rounds, [])  # nothing granted, nothing read
            with mock.patch.object(ms_photos, '_domains', lambda *args: rounds.append(ms_graph.left()) or set()), \
                    mock.patch.object(ms_graph, 'grant', lambda *args: ({next(iter(ms_graph.ANSWERS[ms_photos.COLLEAGUE]))}, set())):
                ms_photos.step(self.store.connect, {'accounts': [self.mail]}, None, '2099-01-03T00:00:00+00:00')  # checked again
            app = mock.MagicMock(config=self.config)
            birthdays_app.Birthdays.birthdays_outlook(app, dt.date(2099, 1, 1), dt.timezone.utc)
        self.assertEqual(len(rounds), 3)
        self.assertTrue(all(left and left > 0 for left in rounds))


if __name__ == '__main__':
    unittest.main()
