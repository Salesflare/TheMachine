"""A to-do being prepared says what the run is doing in one plain line per kind of step, decided from the step itself
(the tool and its action), never from the title the model wrote for it. Plumbing shows nothing, an unknown kind shows
one neutral line, and a line that repeats shows once. Offline: fixture calls only, no model, no browser."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import i18n_extract  # noqa: E402

spec = importlib.util.spec_from_file_location('preparing_lines_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

from machine import browser as b  # noqa: E402

RAW = 'Claim browser and inspect PDF stream'  # a title as the model writes it: never shown
LEASE = 'python3 /opt/machine/integrations/browser-lease.py'


def signals(action, **args):
    return ('assistant_signals', {'action': action, 'args': args, 'title': RAW})


class Lines(unittest.TestCase):
    def test_each_kind_of_step_has_its_line(self):
        for (tool, params), line in [
            (signals('events', mailbox=True, query='invoice'), 'Reading the mail'),
            (signals('events', kinds=['gmail.message']), 'Reading the mail'),
            (signals('events', query='invoice'), 'Reading the messages'),
            (signals('slack_read', channel='C1'), 'Reading the messages'),
            (signals('events', kinds=['calendar.event']), 'Checking the calendar'),
            (('exec', {'command': 'gog -a sam@example.com --readonly calendar events'}), 'Checking the calendar'),
            (('exec', {'command': 'TZ=UTC gog -a sam@example.com --readonly gmail get m1'}), 'Reading the mail'),
            (signals('mail_attachment', event_id=1, save=0), 'Reading the attachment'),
            (signals('mail_attachment', open='/tmp/job/Invoice 12.PDF'), 'Reading the PDF'),
            (('read', {'path': '/tmp/job/invoice.pdf'}), 'Reading the PDF'),
            (('pdf', {'path': '/tmp/job/invoice'}), 'Reading the PDF'),
            (('read', {'path': '/tmp/job/notes.txt'}), 'Reading a file'),
            (('web_search', {'query': 'parking rules'}), 'Searching the web'),
            (('web_fetch', {'url': 'https://example.com/rules'}), 'Reading a web page'),
            (('browser', {'action': 'open', 'targetUrl': 'https://example.com/'}), 'Opening a page'),
            (('browser', {'action': 'navigate', 'url': 'https://example.com/'}), 'Opening a page'),
            (('browser', {'action': 'snapshot'}), 'Reading the page'),
            (('browser', {'action': 'act', 'request': {'kind': 'click', 'ref': 'e1'}}), 'Working on the page'),
            (signals('graph', query='Sam'), 'Looking up people and projects'),
            (signals('status', suggestion_id='s1'), 'Checking the to-do'),
            (signals('preparation_history', offset=0), 'Reading earlier work on this to-do'),
            (signals('prepare', body='Drafted.', next_actions=[{'kind': 'email', 'body': 'Hi Sam'}]), 'Writing the draft'),
            (signals('prepare', body='Checked.', next_actions=[]), 'Saving the result'),
            (('write', {'path': '/tmp/job/notes.md'}), 'Writing notes'),
            (('memory_search', {'query': 'parking'}), 'Searching memory'),
            (('crm__get_account', {'id': '1'}), 'Checking a connected app'),
        ]:
            with self.subTest(tool=tool, params=params):
                self.assertEqual(b.preparing_line(tool, {**params, 'title': RAW}), line)

    def test_plumbing_shows_nothing(self):
        for tool, params in [
            ('exec', {'command': LEASE + ' claim job-1'}),
            ('exec', {'command': LEASE + ' release job-1'}),
            ('exec', {'command': 'sleep 90'}),
            ('browser', {'action': 'tabs'}),
            ('browser', {'action': 'focus', 'targetId': 't1'}),
            ('browser', {'action': 'close', 'targetId': 't1'}),
            ('browser', {'action': 'status'}),
            ('browser', {'action': 'act', 'request': {'kind': 'wait', 'timeMs': 2000}}),
            ('browser', {'action': 'act', 'kind': 'wait'}),
            ('wait', {'runId': 'r1'}),
            ('process', {'action': 'poll', 'sessionId': 'x'}),
            ('skills_read', {'name': 'accepted-suggestion'}),
            ('tool_search', {'query': 'gmail'}),
        ]:
            with self.subTest(tool=tool, params=params):
                self.assertIsNone(b.preparing_line(tool, {**params, 'title': RAW}))

    def test_an_unknown_kind_says_the_neutral_line_never_its_own_text(self):
        for tool, params in [
            ('brand_new_tool', {'title': RAW}),
            ('exec', {'command': 'python3 decode.py statement.bin', 'title': RAW}),
            ('exec', {'command': 'echo "unclosed', 'title': RAW}),
            ('exec', {'code': 'text(await browser({action:"open"}))', 'title': RAW}),
            ('browser', {'action': 'something_new', 'title': RAW}),
            ('browser', {'title': RAW}),
            ('assistant_signals', {'action': 'something_new', 'title': RAW}),
            ('assistant_signals', {'title': RAW}),
            ('exec', None),
        ]:
            with self.subTest(tool=tool, params=params):
                self.assertEqual(b.preparing_line(tool, params), 'Working on it')

    def test_a_word_in_the_models_text_never_picks_the_line(self):
        # The same words as a mail or calendar step, but only in what the model wrote: the step itself decides
        self.assertEqual(b.preparing_line('exec', {'command': 'echo gog gmail calendar', 'title': 'Reading the mail'}), 'Working on it')
        self.assertEqual(b.preparing_line('assistant_signals', {'action': 'status', 'args': {'note': 'calendar pdf'}, 'title': 'Checking the calendar'}),
                         'Checking the to-do')

    def test_a_clipped_record_still_knows_its_action(self):
        clipped = {'clipped': True, 'preview': '{"action":"prepare","args":{"body":"A long draft that mentions \\"action\\":\\"events\\"', 'full': 'retained session transcript'}
        self.assertEqual(b.preparing_line('assistant_signals', clipped), 'Saving the result')

    def test_every_line_is_in_the_catalog_short_and_plain(self):
        lines = {v for table in (b.PREPARING_TOOLS, b.PREPARING_BROWSER, b.PREPARING_ACTIONS, b.PREPARING_PROGRAMS, b.PREPARING_GOG) for v in table.values() if v}
        lines |= {b.PREPARING_OTHER, b.PREPARING_CONNECTED, b.PREPARING_MAIL, b.PREPARING_CALENDAR, b.PREPARING_DRAFT, b.PREPARING_PDF}
        for lang in ('en', 'nl', 'fr', 'de', 'es', 'it', 'pt-BR', 'zh-CN', 'ja', 'ko', 'ru'):
            catalog = i18n_extract.catalog(lang)
            for line in lines:
                with self.subTest(lang=lang, line=line):
                    self.assertTrue(catalog.get(line), 'not translated')
                    self.assertLessEqual(len(catalog[line]), 45)
                    self.assertNotIn('—', catalog[line])
        for line in lines:
            self.assertNotRegex(line, r'(?i)\b(you|your|browser|command|tab|tool)\b')


class Steps(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Parking invoice', 'body': 'Please check the invoice', 'metadata': {}, 'deleted': False}])
        self.sid = self.store.suggest('task', 'Check the parking invoice', 'I can check it against the statement.', [1])['id']
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [], 'database': str(Path(self.temp.name) / 'events.sqlite'), 'dashboard_host': 'machine.example'}
        self.store.config = self.app.config
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='100' WHERE suggestion_id=?", (self.sid,))
        self.store.decide(self.sid, 'accept', '', 'click', 'telegram')
        self.app.preparation_step(lambda req: {'status': 'admitted'})
        with self.store.connect() as db:
            self.job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (self.sid,)).fetchone()[0]
        self.n = 0

    def calls(self, *calls):
        with self.store.connect() as db:
            for tool, params in calls:
                self.n += 1
                db.execute('INSERT INTO preparation_calls(job_id,call_id,tool,params,started_at) VALUES(?,?,?,?,?)',
                           (self.job, str(self.n), tool, json.dumps({**params, 'title': RAW}),
                            (a.dt.datetime(2026, 10, 20, 8, 0, tzinfo=a.dt.timezone.utc) + a.dt.timedelta(seconds=self.n)).isoformat()))

    def titles(self):
        return [s['title'] for s in self.app.preparation_progress(self.sid)['steps']]

    def test_the_to_do_shows_plain_lines_and_never_the_models_title(self):
        self.assertEqual(self.titles(), [])  # nothing done yet: only Preparing…
        self.calls(('exec', {'command': LEASE + ' claim job-1'}))
        self.assertEqual(self.titles(), [])  # plumbing only: still nothing
        self.calls(signals('events', event_ids=[1]),
                   signals('mail_attachment', event_id=1, save=0),
                   ('read', {'path': '/tmp/job/invoice.pdf'}),
                   ('browser', {'action': 'tabs'}),
                   ('exec', {'command': LEASE + ' release job-1'}))
        self.assertEqual(self.titles(), ['Reading the mail', 'Reading the attachment', 'Reading the PDF'])  # a message read by ID is told by its kind
        self.assertNotIn('Claim', json.dumps(self.app.preparation_progress(self.sid)))

    def test_a_line_that_repeats_shows_once(self):
        self.calls(('browser', {'action': 'open', 'targetUrl': 'https://example.com/'}),
                   ('browser', {'action': 'snapshot'}), ('browser', {'action': 'act', 'request': {'kind': 'wait'}}),
                   ('browser', {'action': 'snapshot'}), ('wait', {'runId': 'r'}), ('browser', {'action': 'screenshot'}),
                   ('brand_new_tool', {}), ('another_new_tool', {}))
        self.assertEqual(self.titles(), ['Opening a page', 'Reading the page', 'Working on it'])

    def test_only_the_latest_few_lines_and_only_this_run(self):
        with self.store.connect() as db:
            db.execute('INSERT INTO preparation_calls(job_id,call_id,tool,params,started_at) VALUES(?,?,?,?,?)',
                       ('another-job', 'x', 'web_search', '{}', '2026-10-20T09:00:00+00:00'))
        self.calls(('web_search', {}), ('web_fetch', {}), ('browser', {'action': 'open'}), ('browser', {'action': 'snapshot'}),
                   signals('prepare', body='Done', next_actions=[{'kind': 'email'}]))
        self.assertEqual(self.titles(), ['Reading a web page', 'Opening a page', 'Reading the page', 'Writing the draft'])

    def test_the_browser_note_says_the_same_plain_line(self):
        self.calls(('browser', {'action': 'open', 'targetUrl': 'https://www.example.com/'}), ('browser', {'action': 'tabs'}))
        self.assertEqual(self.app.browser_now()['working'], [{'id': self.sid, 'title': 'Check the parking invoice', 'step': 'Opening a page'}])

    def test_the_raw_title_stays_in_the_run_record(self):
        self.calls(('browser', {'action': 'open', 'targetUrl': 'https://www.example.com/'}))
        with self.store.connect() as db:
            self.assertIn(RAW, db.execute('SELECT params FROM preparation_calls WHERE job_id=?', (self.job,)).fetchone()[0])


if __name__ == '__main__':
    unittest.main()
