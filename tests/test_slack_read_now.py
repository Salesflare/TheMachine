"""A to-do's run reads Slack through the Slack connection, never the browser, and a stuck to-do never sends the owner
into the Machine's settings (agent users 2026-11-09: a founder's Halvorsen to-do said "Browser access is still
disabled; enable it in your Machine's OpenClaw settings" while Slack was connected). The cause: Leo's message came in
on a quiet channel a minute after its last read, and a quiet channel rests a day between reads, so the run found
nothing collected and reached for the browser. Now the run asks the Slack connection to read that conversation next
(slack_read), and a source that isn't connected is one plain tap on the to-do (Connect Slack). Offline: nothing sent."""
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
import machine.app.sync as machine_app_sync
import machine.main as machine_main
import sources

from machine.sources import slack as slack_source  # noqa: E402
from machine.app import sync as app_sync  # noqa: E402

DAY = 86400
SLACK = {'id': 'work-slack', 'service': 'slack', 'user_id': 'U0RILEY01', 'email': 'riley@studio.example',
         'slack_host': 'studio.slack.com', 'boundary': 'work:Studio'}
MAIL = {'id': 'work-gmail', 'service': 'gmail', 'transport': 'gog', 'email': 'riley@studio.example', 'boundary': 'work:Studio'}


class Fake:
    """Slack's Web API for one workspace: #general (busy), #proj-halvorsen (quiet) and a direct message."""

    def __init__(self, messages):
        self.messages, self.calls = messages, []

    def profile(self):
        pass

    def get(self, method, params=None):
        self.calls.append((method, dict(params or {})))
        found = self.messages.get((params or {}).get('channel'), []) if method == 'conversations.history' else []
        return {'ok': True, 'messages': found, 'has_more': False, 'response_metadata': {'next_cursor': ''}}


class Base(unittest.TestCase):
    accounts = [SLACK, MAIL]

    def setUp(self):
        slack_source.READ_NOW.clear(); self.addCleanup(slack_source.READ_NOW.clear)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = self.accounts
        self.app = object.__new__(machine_main.App); self.app.store = self.store
        self.app.config = {'accounts': self.accounts, 'prepare_ahead': False, 'database': str(Path(self.temp.name) / 'e.sqlite')}
        self.store.config = self.app.config


class ReadNow(Base):
    def setUp(self):
        super().setUp()
        now = self.now = time.time()
        # Read a minute ago, nothing then; Leo wrote right after. A quiet channel's next read is tomorrow.
        self.store.commit_page('work-slack', {
            'mode': 'incremental', 'phase': 'scan', 'index': 0, 'after': f'{now - 7 * DAY:.6f}', 'next_discovery': now + DAY,
            'titles_named': True, 'channels': [
                {'id': 'C0GENERAL1', 'name': 'general', 'type': 'channel', 'threads': [], 'last_scan': f'{now - 600:.6f}',
                 'last_activity': now - 3000, 'due': now + 3000, 'next_full': now + DAY},
                {'id': 'C0HALVORS1', 'name': 'proj-halvorsen', 'type': 'channel', 'threads': [], 'last_scan': f'{now - 60:.6f}',
                 'due': now + DAY, 'next_full': now + DAY},
                {'id': 'D0LEO00001', 'name': 'DM U0LEO0002', 'type': 'dm', 'threads': [], 'last_scan': f'{now - 60:.6f}',
                 'due': now + 600, 'next_full': now + DAY}]}, [])
        self.slack = Fake({'C0HALVORS1': [{'type': 'message', 'ts': f'{now - 30:.6f}', 'user': 'U0LEO0002',
                                          'text': 'Two homepage directions for Halvorsen are ready for a first look.'}]})

    def read(self, **args):
        return self.app.action('slack_read', {'channel': '#proj-halvorsen', **args})

    def test_a_quiet_channel_waits_a_day_unless_a_run_asks_for_it(self):
        self.assertFalse(machine_app_sync.sync_slack(self.store, {}, SLACK, self.slack)['more'])
        self.assertEqual(self.slack.calls, [])  # nothing due: Leo's message would wait until tomorrow
        asked = self.read()
        self.assertEqual((asked['status'], asked['channel'], asked['account_id']), ('reading', 'proj-halvorsen', 'work-slack'))
        self.assertIn('call slack_read again', asked['note'])
        self.assertEqual(self.read()['status'], 'reading')  # asking again changes nothing until the read is in
        machine_app_sync.sync_slack(self.store, {}, SLACK, self.slack)
        self.assertEqual([(m, p['channel']) for m, p in self.slack.calls], [('conversations.history', 'C0HALVORS1')])  # first, before #general
        found = self.read()
        self.assertEqual(found['status'], 'read')
        events = self.store.events(['work-slack'], event_ids=found['event_ids'])
        self.assertEqual([e['body'] for e in events], ['Two homepage directions for Halvorsen are ready for a first look.'])
        self.assertIn('events', found['note'])
        machine_app_sync.sync_slack(self.store, {}, SLACK, self.slack)
        self.assertEqual(len(self.slack.calls), 1)  # once read, it rests as before

    def test_with_the_plugin_s_wait_one_call_waits_for_the_read_and_a_repeat_lists_only_what_is_new(self):
        """A run slept with exec, polled that process and asked again, each turn resending its whole session (most
        of its slack_read calls were such repeats): with _wait the call waits for the read itself."""
        self.addCleanup(setattr, slack_source, 'WAIT_STEP', slack_source.WAIT_STEP)
        slack_source.WAIT_STEP = 0.02
        late = self.read(job_id='run1', _wait=0.1)  # Slack's turn doesn't come in time: ask again, no sleep first
        self.assertEqual(late['status'], 'reading')
        self.assertIn('This call waited for it already: call slack_read again', late['note'])
        self.assertNotIn('Sleep', late['note'])

        def read_while_waiting():
            reader = threading.Timer(0.1, machine_app_sync.sync_slack, (self.store, {}, SLACK, self.slack))
            reader.start()
            try:
                return self.read(job_id='run1', _wait=5)
            finally:
                reader.join()
        found = read_while_waiting()
        self.assertEqual(found['status'], 'read')
        self.assertEqual(len(found['event_ids']), 1)
        again = read_while_waiting()  # read anew, nothing new in it since
        self.assertEqual((again['status'], again['event_ids'], again['listed_before']), ('read', [], 1))
        self.assertIn('Nothing new since your last read', again['note'])
        self.assertEqual(self.read(job_id='run2')['status'], 'reading')  # another run starts its own

    def test_by_id_too_and_a_conversation_they_are_not_in_is_named_plainly(self):
        self.assertEqual(self.read(channel='slack:C0HALVORS1')['status'], 'reading')
        gone = self.read(channel='#design-crit')
        self.assertEqual(gone['status'], 'not_found')
        self.assertIn('#proj-halvorsen', gone['conversations'])
        with self.assertRaisesRegex(ValueError, 'channel'):
            self.read(channel=' ')

    def test_a_channel_slack_refuses_ends_the_ask(self):
        class Refusing(Fake):
            def get(self, method, params=None):
                raise sources.SourceError('slack_not_in_channel:' + method)
        self.read()
        machine_app_sync.sync_slack(self.store, {}, SLACK, Refusing({}))  # the other conversations are read as before
        self.assertEqual(self.read()['status'], 'cannot_read')
        self.assertFalse(slack_source.READ_NOW)


class Paged(Fake):
    """Every history read has another page (a busy conversation's daily replay), unless it only asks for the last day."""

    def __init__(self, now, messages=None):
        super().__init__(messages or {})
        self.now = now

    def get(self, method, params=None):
        page = super().get(method, params)
        if method == 'conversations.history' and float(params['oldest']) < self.now - DAY and params.get('cursor') != 'p4':
            cursor = 'p%d' % (int(str(params.get('cursor') or 'p0')[1:]) + 1)
            page.update(has_more=True, response_metadata={'next_cursor': cursor})
        return page


class Quick(Base):
    """A run that waits on Slack reads waited through other conversations' daily replays, a page every few minutes, and the
    asked one's own (five reads for one conversation, 2026-11-25): twelve minutes in, its turn was stopped."""

    def setUp(self):
        super().setUp()
        now = self.now = time.time()
        self.known = [f'{now - 2 * DAY:.6f}', f'{now - 3 * DAY:.6f}']
        self.store.commit_page('work-slack', {
            'mode': 'incremental', 'phase': 'scan', 'index': 0, 'after': f'{now - 7 * DAY:.6f}', 'next_discovery': now + DAY,
            'titles_named': True, 'channels': [
                {'id': 'C0GENERAL1', 'name': 'general', 'type': 'channel', 'threads': [], 'last_scan': f'{now - 600:.6f}',
                 'last_activity': now - 3000, 'due': now - 60, 'next_full': now - 60},
                {'id': 'C0HALVORS1', 'name': 'proj-halvorsen', 'type': 'channel', 'threads': list(self.known),
                 'last_scan': f'{now - 7200:.6f}', 'due': now + 60, 'next_full': now - 60, 'next_thread_index': 1}]}, [])

    def sync(self, slack, account=SLACK):
        return machine_app_sync.sync_slack(self.store, {}, account, slack)

    def channel(self, channel_id='C0HALVORS1'):
        return next(c for c in self.store.checkpoint('work-slack')['channels'] if c['id'] == channel_id)

    def ask(self):
        return self.app.action('slack_read', {'channel': '#proj-halvorsen'})

    def test_one_read_takes_one_turn_and_leaves_the_replay_and_the_threads_for_its_own(self):
        for account in (SLACK, {**SLACK, 'fair_incremental': True}):
            with self.subTest(fair=account.get('fair_incremental')):
                self.setUp()
                slack, before = Paged(self.now), self.channel()
                self.ask()
                self.sync(slack, account)
                self.assertEqual([(m, p['channel']) for m, p in slack.calls], [('conversations.history', 'C0HALVORS1')])
                self.assertEqual(self.ask()['status'], 'read')
                after = self.channel()
                self.assertEqual((after['threads'], after['due'], after['next_full'], after['next_thread_index']),
                                 (self.known, before['due'], before['next_full'], 1))
                slack_source.READ_NOW.clear()

    def test_a_thread_with_a_new_reply_is_read_with_it_and_one_without_is_not(self):
        started, quiet = f'{self.now - 8000:.6f}', f'{self.now - 8100:.6f}'
        slack = Paged(self.now, {'C0HALVORS1': [
            {'type': 'message', 'ts': quiet, 'user': 'U0LEO0002', 'text': 'Done', 'reply_count': 1, 'latest_reply': f'{self.now - 8050:.6f}'},
            {'type': 'message', 'ts': started, 'user': 'U0LEO0002', 'text': 'Look', 'reply_count': 2, 'latest_reply': f'{self.now - 30:.6f}'}]})
        self.ask()
        self.sync(slack)
        self.assertEqual(self.ask()['status'], 'reading')  # its thread is still to come
        self.sync(slack)
        self.assertEqual([(m, p.get('ts')) for m, p in slack.calls], [('conversations.history', None), ('conversations.replies', started)])
        self.assertEqual(self.ask()['status'], 'read')
        self.assertEqual(set(self.channel()['threads']), {*self.known, quiet, started})  # known for its own turns

    def test_a_replay_under_way_is_set_aside_and_carries_on_where_it_was(self):
        slack = Paged(self.now)
        self.sync(slack)
        self.sync(slack)  # general's daily replay, two of its five pages
        self.ask()
        self.sync(slack)
        self.assertEqual([(p['channel'], p.get('cursor')) for _, p in slack.calls],
                         [('C0GENERAL1', None), ('C0GENERAL1', 'p1'), ('C0HALVORS1', None)])
        self.assertEqual(self.ask()['status'], 'read')
        while self.sync(slack)['more']:
            pass
        self.assertEqual([p.get('cursor') for _, p in slack.calls if p['channel'] == 'C0GENERAL1'], [None, 'p1', 'p2', 'p3', 'p4'])
        self.assertGreater(self.channel('C0GENERAL1')['next_full'], self.now)
        self.assertNotIn('set_aside', self.store.checkpoint('work-slack'))

    def test_the_asked_conversation_s_own_replay_is_set_aside_too_and_its_newest_read_stands(self):
        state = self.store.checkpoint('work-slack')
        state['channels'][1]['due'] = self.now - 9 * DAY  # its replay comes first
        self.store.commit_page('work-slack', state, [])
        slack = Paged(self.now)
        self.sync(slack)
        self.ask()
        self.sync(slack)
        newest = self.channel()['last_scan']
        self.assertEqual(self.ask()['status'], 'read')
        for _ in range(12):
            self.sync(slack)
        self.assertGreaterEqual(float(self.channel()['last_scan']), float(newest))
        self.assertEqual(sum(p['channel'] == 'C0HALVORS1' and p['oldest'] < f'{self.now - DAY:.6f}' for m, p in slack.calls
                             if m == 'conversations.history'), 5)  # its five pages, each once

    def test_the_asked_conversation_s_first_read_is_never_set_aside(self):
        """No quick read comes before it: set aside, it started over in full, and then the old one carried on too."""
        for first in ({'last_scan': None}, {}):
            with self.subTest(first=first):
                self.setUp()
                state = self.store.checkpoint('work-slack')
                state['channels'][1].update(due=self.now - 9 * DAY, threads=[], **first)
                if not first:
                    state['step'] = 'deepen'
                self.store.commit_page('work-slack', state, [])
                slack = Paged(self.now)
                if not first:  # a first import's step, under way for this conversation
                    state['channels'][1]['deepen'] = f'{self.now - DAY:.6f}'
                    state.update(index=1, scan={'oldest': f'{self.now - 7 * DAY:.6f}', 'latest': f'{self.now - DAY:.6f}', 'phase': 'history', 'thread_index': 0,
                                                'threads': [], 'full': True, 'step': 'deepen'})
                    self.store.commit_page('work-slack', state, [])
                self.sync(slack)
                self.ask()
                self.sync(slack)
                self.assertNotIn('set_aside', self.store.checkpoint('work-slack'))
                for _ in range(8):
                    self.sync(slack)
                pages = [p.get('cursor') for m, p in slack.calls if p['channel'] == 'C0HALVORS1' and m == 'conversations.history' and float(p['oldest']) < self.now - DAY]
                self.assertEqual(pages[:5], [None, 'p1', 'p2', 'p3', 'p4'])
                self.assertEqual(pages.count('p4'), 1)  # its pages once
                slack_source.READ_NOW.clear()

    def test_the_asked_conversation_s_own_set_aside_first_read_carries_on_where_it_was(self):
        state = self.store.checkpoint('work-slack')
        state['channels'][1].update(due=self.now - 9 * DAY, threads=[], last_scan=None)
        self.store.commit_page('work-slack', state, [])
        slack = Paged(self.now)
        self.sync(slack)  # its first page
        self.app.action('slack_read', {'channel': '#general'})
        self.sync(slack)  # general's quick read first
        self.ask()
        for _ in range(8):
            self.sync(slack)
        self.assertEqual([p.get('cursor') for m, p in slack.calls if p['channel'] == 'C0HALVORS1' and float(p['oldest']) < self.now - DAY],
                         [None, 'p1', 'p2', 'p3', 'p4'])

    def test_a_first_import_s_threads_still_wait_for_their_turn(self):
        state = self.store.checkpoint('work-slack')
        state['channels'][1]['threads_waiting'] = True
        self.store.commit_page('work-slack', state, [])
        self.ask()
        self.sync(Paged(self.now))
        self.assertEqual(self.ask()['status'], 'read')
        self.assertTrue(self.channel()['threads_waiting'])

    def test_a_conversation_they_left_meanwhile_is_let_go(self):
        slack = Paged(self.now)
        self.sync(slack)
        self.ask()
        self.sync(slack)
        state = self.store.checkpoint('work-slack')
        state['channels'] = state['channels'][1:]
        self.store.commit_page('work-slack', state, [])
        self.ask()
        self.sync(slack)
        self.assertNotIn('set_aside', self.store.checkpoint('work-slack'))


class NotConnected(Base):
    accounts = [MAIL]

    def test_no_slack_means_one_plain_tap_to_connect_it(self):
        out = self.app.action('slack_read', {'channel': '#proj-halvorsen'})
        self.assertEqual((out['status'], out['connect']), ('not_connected', 'slack'))
        self.assertIn('Never the browser', out['note'])


class Blocker(Base):
    accounts = [MAIL]

    def card(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            self.store.card_views(db, [row])
        return row

    def start(self):
        self.store.commit_page('work-gmail', {}, [{
            'account_id': 'work-gmail', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': '2026-11-08T15:00:00+00:00',
            'title': 'Revised homepage proposal', 'body': 'Could we see the revised homepage by Tuesday?',
            'metadata': {'from': 'Jonas <jonas@halvorsen.example>', 'thread_id': 't1'}, 'deleted': False}])
        sid = self.app.action('suggest', {'dedupe_key': 'halvorsen:handoff', 'title': 'Hand the Halvorsen homepage to Leo',
                                          'body': 'Leo has **two directions** ready.', 'event_ids': [1]})['id']
        self.store.decide(sid, 'accept', '', 'click-' + sid, 'dashboard')
        sent = []
        self.app.preparation_step(lambda req: sent.append(req) or {'status': 'admitted'})
        with self.store.connect() as db:
            job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (sid,)).fetchone()['job_id']
        return sid, job, sent[-1]['message']

    def test_a_run_that_needs_slack_offers_connect_slack_and_never_a_setting(self):
        sid, job, message = self.start()
        self.assertIn('connect=<that source', message)
        self.assertIn("This Machine's own setup is never their step", message)
        self.assertNotIn('assistant_signals slack_read', message)  # no Slack here: nothing to read it with
        for wrong in ('gateway', 'Slack!', 3):
            with self.assertRaisesRegex(ValueError, 'connect'):
                self.store.preparation_blocked(sid, job, "Slack isn't connected.", connect=wrong)
        with self.assertRaisesRegex(ValueError, 'one of them'):
            self.store.preparation_blocked(sid, job, "Slack isn't connected.", connect='slack', move_to='personal')
        with self.assertRaisesRegex(ValueError, 'gmail is connected already'):
            self.store.preparation_blocked(sid, job, 'The mailbox is off.', connect='gmail')
        self.app.action('preparation_blocked', {'suggestion_id': sid, 'job_id': job, 'connect': 'slack', 'questions': [],
                                                'reason': "Slack isn't connected, so I can't read Leo's reply. Connect it and I'll pick this up."})
        card = self.card(sid)
        self.assertEqual((card['preparation_status'], card['preparation_connect']), ('blocked', 'slack'))
        self.assertEqual(self.store.resume_connected(), [])  # still not connected: it waits
        self.assertEqual(self.card(sid)['preparation_status'], 'blocked')
        self.store.accounts = self.app.config['accounts'] = [SLACK, MAIL]  # they connect Slack
        self.app.preparation_step(lambda req: {'status': 'admitted'})  # it carries on by itself: no Try again to find
        card = self.card(sid)
        self.assertNotEqual(card['preparation_status'], 'blocked')
        self.assertIsNone(card['preparation_connect'])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT source FROM decisions WHERE suggestion_id=? AND choice='retry'", (sid,)).fetchone()['source'], 'connected')
        self.assertEqual(self.store.resume_connected(), [])  # once


class Connected(Blocker):
    accounts = [SLACK, MAIL]

    def test_a_run_with_slack_connected_reads_it_there(self):
        sid, job, message = self.start()
        self.assertIn('assistant_signals slack_read', message)
        self.assertIn('Never open Slack in the browser', message)
        with self.assertRaisesRegex(ValueError, 'slack is connected already.*slack_read.*never the browser'):
            self.store.preparation_blocked(sid, job, "Slack isn't connected.", connect='slack')

    test_a_run_that_needs_slack_offers_connect_slack_and_never_a_setting = None


class TwoReads(Blocker):
    """A run asked for two group DMs with teammates before it wrote anything (so it wouldn't redo their work), slept one
    read's time, found both still reading and stopped: "paste any update here", and the to-do showed Stuck. Slack reads
    one conversation every few minutes, asked ones first, so two take two reads. Now the wait counts them, a blocker
    while they are still coming is refused, and one that stands anyway carries on by itself once they are in."""
    accounts = [SLACK, MAIL]
    GROUPS = ('G0TEAMA001', 'G0TEAMB002')
    test_a_run_that_needs_slack_offers_connect_slack_and_never_a_setting = None

    def setUp(self):
        super().setUp()
        now = time.time()
        self.store.commit_page('work-slack', {
            'mode': 'incremental', 'phase': 'scan', 'index': 0, 'after': f'{now - 7 * DAY:.6f}', 'next_discovery': now + DAY,
            'titles_named': True, 'channels': [
                {'id': g, 'name': 'mpdm-team-' + g[-1], 'type': 'group', 'threads': [], 'last_scan': f'{now - DAY:.6f}',
                 'due': now + DAY, 'next_full': now + DAY} for g in self.GROUPS]}, [])
        self.slack = Fake({g: [{'type': 'message', 'ts': f'{now - 30:.6f}', 'user': 'U0SAM00002', 'text': 'On it, replying today.'}]
                           for g in self.GROUPS})

    def read(self, job, channel):
        return self.app.action('slack_read', {'channel': channel, 'job_id': job})

    def block(self, sid, job, reason='I need the price they agreed on.'):
        return self.app.action('preparation_blocked', {'suggestion_id': sid, 'job_id': job, 'reason': reason, 'questions': []})

    def test_the_wait_counts_the_reads_still_to_come(self):
        sid, job, _ = self.start()
        first, second = self.read(job, self.GROUPS[0]), self.read(job, self.GROUPS[1])
        self.assertEqual((first['status'], second['status']), ('reading', 'reading'))
        self.assertEqual(first['wait_seconds'], 180 + slack_source.READ_WAIT_MARGIN)  # one read every 3 minutes
        self.assertEqual(second['wait_seconds'], slack_source.READ_WAIT_MAX)  # two reads, at most READ_WAIT_MAX before asking again
        self.assertIn('never a blocker', second['note'])
        self.assertEqual(slack_source.slack_read_wait({'slack_read_seconds': 65}, SLACK, 2), 2 * 65 + slack_source.READ_WAIT_MARGIN)

    def test_reads_still_coming_are_a_wait_never_a_blocker(self):
        sid, job, _ = self.start()
        for g in self.GROUPS:
            self.assertEqual(self.read(job, g)['status'], 'reading')
        with self.assertRaisesRegex(ValueError, r'Not recorded: Slack is still reading mpdm-team-1, mpdm-team-2.*never a question for the owner'):
            self.block(sid, job, 'I still could not read the team discussion; paste any update here.')
        self.assertNotEqual(self.card(sid)['preparation_status'], 'blocked')
        machine_app_sync.sync_slack(self.store, {}, SLACK, self.slack)  # one read: the first group
        with self.assertRaisesRegex(ValueError, r'still reading mpdm-team-2 for'):
            self.block(sid, job)
        machine_app_sync.sync_slack(self.store, {}, SLACK, self.slack)  # the second, ahead of anything due
        self.assertEqual([p['channel'] for _, p in self.slack.calls], list(self.GROUPS))
        self.assertEqual([self.read(job, g)['status'] for g in self.GROUPS], ['read', 'read'])
        self.assertEqual(self.block(sid, job)['status'], 'blocked')  # a real blocker, once nothing is coming
        self.assertEqual(self.app.__dict__.get('_slack_read_resumes') or {}, {})  # and no resume for it

    def test_a_blocker_after_the_long_wait_carries_on_by_itself_once_the_reads_are_in(self):
        sid, job, _ = self.start()
        for g in self.GROUPS:
            self.read(job, g)
        asked = self.app.run_slack_reads()[job]
        for key in asked:
            asked[key] -= app_sync.RUN_READ_WAIT + 1
        self.assertEqual(self.block(sid, job)['status'], 'blocked')  # waited long enough: it may stand
        self.app.preparation_step(lambda req: {'status': 'admitted'})
        self.assertEqual(self.card(sid)['preparation_status'], 'blocked')  # still coming: it waits
        machine_app_sync.sync_slack(self.store, {}, SLACK, self.slack); machine_app_sync.sync_slack(self.store, {}, SLACK, self.slack)
        self.app.preparation_step(lambda req: {'status': 'admitted'})  # both in: no Try again to find
        self.assertNotEqual(self.card(sid)['preparation_status'], 'blocked')
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT source FROM decisions WHERE suggestion_id=? AND choice='retry'", (sid,)).fetchone()['source'], 'slack_read')
        self.assertEqual(self.app.resume_slack_reads(), [])  # once

    def test_reads_that_never_came_leave_try_again_to_the_owner(self):
        sid, job, _ = self.start()
        self.read(job, self.GROUPS[0])
        asked = self.app.run_slack_reads()[job]
        for key in asked:
            asked[key] -= app_sync.RUN_READ_WAIT + 1
        self.assertEqual(self.block(sid, job)['status'], 'blocked')
        for key in asked:
            asked[key] -= slack_source.READ_NOW_MAX
        self.assertEqual(self.app.resume_slack_reads(), [])  # given up: no run started on reads that never came
        self.assertEqual(self.app.__dict__['_slack_read_resumes'], {})
        self.assertEqual(self.card(sid)['preparation_status'], 'blocked')

    def test_a_refused_read_is_a_plain_blocker(self):
        class Refusing(Fake):
            def get(self, method, params=None):
                raise sources.SourceError('slack_not_in_channel:' + method)
        sid, job, _ = self.start()
        self.read(job, self.GROUPS[0])
        machine_app_sync.sync_slack(self.store, {}, SLACK, Refusing({}))
        self.assertEqual(self.read(job, self.GROUPS[0])['status'], 'cannot_read')
        self.assertEqual(self.block(sid, job, "Slack wouldn't let me read the team's group message, so paste its latest update here.")['status'], 'blocked')


if __name__ == '__main__':
    unittest.main()
