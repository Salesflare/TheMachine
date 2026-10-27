"""A task blocked on a sign-in reaches the owner as a Sign in prompt (dashboard card, Telegram button) and carries
on by itself once the owner is signed in. Offline: no browser, no Telegram, no site is contacted."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('signin_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

HANDOFF = 'Example is signed out; sign in on the example login tab in the browser, then tap Continue.'
SECRET = 'not-a-real-password-123'


class SigninHandoff(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Evidence', 'body': 'Please confirm your details', 'metadata': {}, 'deleted': False}])
        self.sid = self.store.suggest('task', 'Confirm your details', 'I can confirm them in your account.', [1])['id']
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [], 'database': str(Path(self.temp.name) / 'events.sqlite'), 'dashboard_host': 'machine.example'}
        self.store.config = self.app.config
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='100' WHERE suggestion_id=?", (self.sid,))
        self.store.decide(self.sid, 'accept', '', 'click', 'telegram')
        self.app.preparation_step(lambda req: {'status': 'admitted'})

    def job(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM preparations WHERE suggestion_id=?', (self.sid,)).fetchone())

    def steps(self, *calls):
        with self.store.connect() as db:
            for i, (tool, params) in enumerate(calls):
                db.execute('INSERT INTO preparation_calls(job_id,call_id,tool,params,started_at) VALUES(?,?,?,?,?)',
                           (self.job()['job_id'], str(i), tool, json.dumps(params), a.dt.datetime(2026, 10, 20, 8, 11, i, tzinfo=a.dt.timezone.utc).isoformat()))

    def block(self, reason=HANDOFF):
        # The handoff as the run makes it: the sign-in page, then releasing the browser lease, then saving the blocker.
        self.steps(('browser', {'action': 'open', 'targetUrl': 'https://www.example.com/login'}),
                   ('browser', {'action': 'act', 'kind': 'evaluate'}),
                   ('exec', {'command': 'python3 browser-lease.py release'}),
                   ('assistant_signals', {'action': 'status'}))
        self.store.preparation_blocked(self.sid, self.job()['job_id'], reason)

    def row(self):
        with self.store.connect() as db:
            row = dict(db.execute(a.EDIT_ROWS + ' AND s.id=?', (self.sid,)).fetchone())
            row.update(self.store.suggestion_result(row, db))
        return row

    def test_a_sign_in_handoff_after_releasing_the_lease_still_offers_the_sign_in(self):
        self.block()
        waiting = self.row()['preparation_browser']
        self.assertTrue(waiting['sign_in'])
        self.assertEqual(waiting['page'], 'https://www.example.com/login')
        self.assertEqual(waiting['signin_url'], 'https://machine.example/#signin-for=' + self.sid)

    def test_the_browser_viewer_note_says_which_task_waits_there(self):
        self.assertEqual(self.app.browser_now(), {'working': [], 'waiting': []})  # idle: the viewer explains itself
        self.block()
        self.assertEqual(self.app.browser_now(), {'working': [], 'waiting': [{'title': 'Confirm your details', 'site': 'example.com'}]})

    def test_the_browser_viewer_note_shows_a_running_task_that_uses_it(self):
        self.steps(('exec', {'command': 'ls'}))
        self.assertEqual(self.app.browser_now()['working'], [])  # not on the browser: nothing to say there
        with self.store.connect() as db:
            db.execute('DELETE FROM preparation_calls')
        self.steps(('browser', {'action': 'open', 'targetUrl': 'https://www.example.com/'}))
        with patch.object(a, 'preparation_steps', return_value=[{'title': 'Opening the account page', 'at': None}]):
            self.assertEqual(self.app.browser_now()['working'], [{'title': 'Confirm your details', 'step': 'Opening the account page'}])

    def test_another_blocker_after_a_command_does_not(self):
        self.block('The export failed with an error; try again later.')
        self.assertNotIn('preparation_browser', self.row())

    def test_a_running_wait_no_longer_breaks_the_dashboard(self):
        # Store had no config: every snapshot failed while a run waited on the browser (2026-10-20).
        self.steps(('browser', {'action': 'open', 'targetUrl': 'https://www.example.com/login'}))
        self.store.config = {}
        with patch.object(a, 'BROWSER_WAIT', 0):
            snapshot = self.store.snapshot([])
        card = next(s for s in snapshot['suggestions'] if s['id'] == self.sid)
        self.assertEqual(card['preparation_browser']['page'], 'https://www.example.com/login')
        self.assertFalse(card['preparation_browser']['sign_in'])

    def test_the_telegram_card_says_so_and_has_a_sign_in_button(self):
        self.block()
        row = self.row()
        self.assertIn('Waiting for you to sign in', a.card(row))
        buttons = [b for block in a.controls(row)['blocks'] for b in block['buttons']]
        self.assertEqual(buttons[0], {'label': 'Sign in', 'action': {'type': 'url', 'url': 'https://machine.example/#signin-for=' + self.sid}})
        self.assertIn('Continue', [b['label'] for b in buttons])  # tapping Continue still works too

    def test_the_blocker_notifies_on_telegram_with_the_button(self):
        self.block()
        sent = []
        with patch.object(a, 'in_hours', return_value=True), patch.object(a, 'telegram_request', side_effect=lambda config, args: (sent.append(args), {'messageId': '7'})[1]):
            a.deliver_one(self.store, self.app.config, edit_cards=True)  # the card is redrawn
            a.deliver_one(self.store, self.app.config, edit_cards=True)  # and a notification asks for the sign-in
        edit, notice = sent[0], sent[-1]
        self.assertEqual(edit['action'], 'edit')
        self.assertIn('Sign in', [b['label'] for block in edit['presentation']['blocks'] for b in block['buttons']])
        self.assertEqual((notice['action'], notice['replyTo']), ('send', '100'))
        self.assertTrue(notice['message'].startswith('Needs you to sign in: '))
        self.assertEqual(notice['presentation']['blocks'][0]['buttons'][0]['action']['url'], 'https://machine.example/#signin-for=' + self.sid)

    def test_the_phone_notification_opens_the_sign_in_too(self):
        self.block()
        with self.store.connect() as db:
            db.execute("INSERT INTO push_subscriptions VALUES('https://push.example.invalid/1','key','auth',?,NULL,NULL)", (a.now(),))
        sent = []
        row = {**self.row(), '_result_notice': True}
        a.push_notify(self.store, self.app.config, row, sender=lambda request: (sent.append(request), {'results': []})[1])
        payload = sent[0]['payload']
        self.assertTrue(payload['title'].startswith('Needs you to sign in: '))
        self.assertEqual(payload['url'], 'https://machine.example/#signin-for=' + self.sid)

    def test_without_a_dashboard_address_there_is_no_dead_button(self):
        self.app.config.pop('dashboard_host')
        self.block()
        labels = [b['label'] for block in a.controls(self.row())['blocks'] for b in block['buttons']]
        self.assertNotIn('Sign in', labels)
        self.assertIn('Continue', labels)

    def test_signing_in_from_the_dialog_carries_the_task_on(self):
        self.block()
        blocked = self.job()['job_id']
        with patch.object(a.browser_login, 'fill', return_value={'result': 'done', 'page': None}) as fill:
            done = self.app.action('browser_login_fill', {'page': '0:tab', 'host': 'www.example.com', 'password': SECRET,
                                                          'suggestion_id': self.sid}, owner_dashboard=True)
        fill.assert_called_once()
        self.assertEqual(done['resumed'], [self.sid])
        self.assertNotIn(SECRET, json.dumps(done))
        job = self.job()
        self.assertEqual(job['status'], 'queued')
        self.assertNotEqual(job['job_id'], blocked)
        with self.store.connect() as db:
            self.assertFalse(db.execute('SELECT 1 FROM decisions WHERE feedback LIKE ?', ('%' + SECRET + '%',)).fetchone())

    def test_a_dialog_sign_in_on_another_site_or_unfinished_carries_nothing_on(self):
        self.block()
        with patch.object(a.browser_login, 'fill', return_value={'result': 'done', 'page': None}):
            self.assertEqual(self.app.action('browser_login_fill', {'page': '0:tab', 'host': 'other.invalid', 'password': SECRET}, owner_dashboard=True)['resumed'], [])
        with patch.object(a.browser_login, 'fill', return_value={'result': 'next', 'page': {'host': 'www.example.com'}}):
            self.assertNotIn('resumed', self.app.action('browser_login_fill', {'page': '0:tab', 'host': 'www.example.com', 'code': '123456',
                                                                                'suggestion_id': self.sid}, owner_dashboard=True))
        self.assertEqual(self.job()['status'], 'blocked')

    def test_approving_in_the_sites_app_carries_the_task_on_once_the_dialog_sees_it_done(self):
        self.block()
        with patch.object(a.browser_login, 'fill', return_value={'result': 'approve', 'page': {'id': '0:tab', 'host': 'www.example.com'}}):
            self.assertNotIn('resumed', self.app.action('browser_login_fill', {'page': '0:tab', 'host': 'www.example.com', 'password': SECRET,
                                                                                'suggestion_id': self.sid}, owner_dashboard=True))
        with patch.object(a.browser_login, 'watch', return_value={'state': 'waiting'}):
            self.assertEqual(self.app.action('browser_login_pages', {'watch': '0:tab', 'host': 'www.example.com', 'suggestion_id': self.sid},
                                             owner_dashboard=True), {'state': 'waiting'})
        self.assertEqual(self.job()['status'], 'blocked')
        with patch.object(a.browser_login, 'watch', return_value={'state': 'done'}):
            done = self.app.action('browser_login_pages', {'watch': '0:tab', 'host': 'www.example.com', 'suggestion_id': self.sid}, owner_dashboard=True)
        self.assertEqual(done['resumed'], [self.sid])

    def test_the_same_site_by_host_alone(self):
        self.block()
        with patch.object(a.browser_login, 'fill', return_value={'result': 'done', 'page': None}):
            done = self.app.action('browser_login_fill', {'page': '0:tab', 'host': 'login.example.com', 'password': SECRET}, owner_dashboard=True)
        self.assertEqual(done['resumed'], [self.sid])

    def test_signing_in_in_the_browser_itself_carries_on_once_the_form_is_gone(self):
        self.block()
        forms = [[{'host': 'www.example.com'}], [{'host': 'www.example.com'}], []]
        with patch.object(a.browser_login, 'pages', side_effect=lambda config: forms.pop(0) if forms else []), \
                patch.object(a.App, 'signin_tabs', return_value=[{'id': 't', 'url': 'https://www.example.com/home'}]):
            for _ in range(3):
                self.app.watch_sign_ins(every=0)
                if _ < 2:
                    self.assertEqual(self.job()['status'], 'blocked')
        self.assertEqual(self.job()['status'], 'queued')

    def signed_in_in_the_browser(self):
        """The 2026-10-27 report: blocked on a sign-in, the owner signs in in the browser and the watcher carries on."""
        self.block()
        forms = [[{'host': 'www.example.com'}], []]
        with patch.object(a.browser_login, 'pages', side_effect=lambda config: forms.pop(0) if forms else []), \
                patch.object(a.App, 'signin_tabs', return_value=[{'id': 't', 'url': 'https://www.example.com/home'}]):
            self.app.watch_sign_ins(every=0)
            self.assertEqual(self.app.watch_sign_ins(every=0), [self.sid])
        self.assertEqual(self.job()['status'], 'queued')
        with self.store.connect() as db:  # the card says it signed in and starts shortly
            card = [dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())]
            self.store.card_views(db, card)
        self.assertTrue(card[0]['preparation_signed_in'])

    def decisions(self):
        with self.store.connect() as db:
            return [r[0] for r in db.execute('SELECT choice FROM decisions WHERE suggestion_id=? ORDER BY rowid', (self.sid,))]

    def test_try_again_on_a_card_drawn_before_it_carried_on_is_no_error(self):
        # Continue or Try again from the card still showing the sign-in: the run already carries on, so nothing new.
        self.signed_in_in_the_browser()
        job, before = self.job(), self.decisions()
        for status in ('queued', 'starting', 'running'):
            with self.store.connect() as db:
                db.execute('UPDATE preparations SET status=? WHERE suggestion_id=?', (status, self.sid))
            self.assertEqual(self.store.decide(self.sid, 'retry', '', 'tap-' + status, 'dashboard'), {'status': 'accepted', 'already': 'running'})
        self.assertEqual(self.job()['job_id'], job['job_id'])
        self.assertEqual(self.decisions(), before)

    def test_try_again_once_it_finished_says_it_is_done(self):
        self.signed_in_in_the_browser()
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='done' WHERE suggestion_id=?", (self.sid,))
            db.execute("UPDATE suggestions SET status='prepared' WHERE id=?", (self.sid,))
        self.assertEqual(self.store.decide(self.sid, 'retry', '', 'late', 'dashboard')['already'], 'done')

    def test_try_again_on_a_closed_card_is_a_stale_tap_not_an_error(self):
        self.signed_in_in_the_browser()
        self.store.decide(self.sid, 'complete', '', 'done', 'dashboard')
        for source in ('dashboard', 'telegram'):
            said = self.store.decide(self.sid, 'retry', '', 'late-' + source, source)
            self.assertEqual((said['status'], said['already'], said['skipped']), ('completed', 'closed', True))
        self.assertEqual(self.decisions()[-1], 'complete')

    def test_closing_the_browser_looks_at_once(self):
        # The pane or the dialog closed: the dashboard asks for a look now, not at the next round of the watcher.
        self.block()
        forms = [[{'host': 'www.example.com'}], []]
        with patch.object(a.browser_login, 'pages', side_effect=lambda config: forms.pop(0) if forms else []), \
                patch.object(a.App, 'signin_tabs', return_value=[{'id': 't', 'url': 'https://www.example.com/home'}]):
            self.app.watch_sign_ins()  # sees the form; the next round is 20 seconds away
            self.assertEqual(self.app.watch_sign_ins(), [])
            self.assertEqual(self.job()['status'], 'blocked')
            self.assertEqual(self.app.action('browser_login_check', {}, owner_dashboard=True), {'resumed': [self.sid]})
        self.assertEqual(self.job()['status'], 'queued')
        with self.assertRaises(ValueError):
            self.app.action('browser_login_check', {}, owner_dashboard=False)

    def test_the_watcher_never_resumes_without_having_seen_the_form(self):
        self.block()
        with patch.object(a.browser_login, 'pages', return_value=[]), \
                patch.object(a.App, 'signin_tabs', return_value=[{'id': 't', 'url': 'https://www.example.com/home'}]):
            for _ in range(3):
                self.app.watch_sign_ins(every=0)
        self.assertEqual(self.job()['status'], 'blocked')

    def test_the_watcher_waits_while_no_tab_of_the_site_is_past_the_sign_in(self):
        self.block()
        with patch.object(a.browser_login, 'pages', side_effect=[[{'host': 'www.example.com'}], [], []]), \
                patch.object(a.App, 'signin_tabs', return_value=[]):
            for _ in range(3):
                self.app.watch_sign_ins(every=0)
        self.assertEqual(self.job()['status'], 'blocked')

    def test_the_watcher_leaves_the_browser_alone_when_nothing_waits(self):
        with patch.object(a.browser_login, 'pages') as pages:
            self.app.watch_sign_ins(every=0)
        pages.assert_not_called()

    def test_a_blocked_sign_in_card_is_redrawn_once(self):
        self.block()
        with self.store.connect() as db:
            db.execute('UPDATE deliveries SET needs_edit=0')
        self.app.flag_browser_waits()
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT needs_edit FROM deliveries').fetchone()[0], 1)
            db.execute('UPDATE deliveries SET needs_edit=0')
        self.app.flag_browser_waits()
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT needs_edit FROM deliveries').fetchone()[0], 0)

    def test_same_site(self):
        self.assertTrue(a.same_site('login.wise.com', 'https://wise.com/home'))
        self.assertTrue(a.same_site('www.example.com', 'example.com'))
        self.assertFalse(a.same_site('example.com', 'https://other.invalid/login'))
        self.assertFalse(a.same_site('', 'example.com'))


class PerTaskSite(unittest.TestCase):
    """Two tasks blocked on different sites (one card's Sign in once offered the other task's site). Each task's dialog,
    Open the browser and carrying on follow the site its own run left off at."""

    job, steps, block, row = SigninHandoff.job, SigninHandoff.steps, SigninHandoff.block, SigninHandoff.row

    def add_task(self, key, calls, reason):
        sid = self.store.suggest(key, 'Task ' + key, 'I can do it.', [1])['id']
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='200' WHERE suggestion_id=?", (sid,))
        self.store.decide(sid, 'accept', '', 'click-' + key, 'telegram')
        self.app.preparation_step(lambda req: {'status': 'admitted'})
        with self.store.connect() as db:
            job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (sid,)).fetchone()[0]
            for i, (tool, params) in enumerate(calls):
                db.execute('INSERT INTO preparation_calls(job_id,call_id,tool,params,started_at) VALUES(?,?,?,?,?)',
                           (job, 'n' + str(i), tool, json.dumps(params), a.dt.datetime(2026, 10, 20, 8, 30, i, tzinfo=a.dt.timezone.utc).isoformat()))
        self.store.preparation_blocked(sid, job, reason)
        return sid, job

    def setUp(self):
        SigninHandoff.setUp(self)
        self.block('Wise is signed out; sign in on the Wise login tab, then tap Continue.')
        with self.store.connect() as db:
            for row in db.execute('SELECT rowid,params FROM preparation_calls').fetchall():  # in Python: params may be sealed
                db.execute('UPDATE preparation_calls SET params=? WHERE rowid=?', (row['params'].replace('www.example.com', 'wise.com'), row['rowid']))
        # The second task's latest run only reused a tab an earlier run of its session opened.
        self.other, job = self.add_task('profit', [('browser', {'action': 'focus', 'targetId': 'profit-tab'}),
                                                   ('exec', {'command': 'release lease'})],
                                        'Enter your six-digit authenticator code in the ProfitWell tab, then tap Continue.')
        with self.store.connect() as db:
            db.execute("INSERT INTO preparation_runs(job_id,suggestion_id,session_job_id,status,started_at) VALUES('old',?,'sess','lost','2026-10-20T08:09:00+00:00')", (self.other,))
            db.execute("UPDATE preparation_runs SET session_job_id='sess',started_at='2026-10-20T08:30:00+00:00' WHERE job_id=?", (job,))
            for i, params in enumerate([{'action': 'open', 'targetUrl': 'https://wise.com/login', 'label': 'unrelated-tab'},
                                        {'action': 'open', 'targetUrl': 'https://app.profit.example/login', 'label': 'profit-tab'},
                                        {'action': 'navigate', 'targetUrl': 'https://wise.com/home', 'targetId': 'unrelated-tab'}]):
                db.execute('INSERT INTO preparation_calls(job_id,call_id,tool,params,started_at) VALUES(?,?,?,?,?)',
                           ('old', str(i), 'browser', json.dumps(params), '2026-10-20T08:10:0%d+00:00' % i))
        self.forms = [{'host': 'wise.com', 'id': '0:w'}, {'host': 'app.profit.example', 'id': '0:p'}]

    def pages(self, sid):
        with patch.object(a.browser_login, 'pages', return_value=self.forms):
            return self.app.action('browser_login_pages', {'suggestion_id': sid}, owner_dashboard=True)

    def test_each_task_finds_its_own_site_from_its_own_runs(self):
        self.assertEqual(self.app.signin_page(self.other), 'https://app.profit.example/login')
        self.assertEqual(self.app.signin_page(self.sid), 'https://wise.com/login')

    def test_the_dialog_offers_only_the_tasks_own_sign_in(self):
        self.assertEqual(self.pages(self.other), {'pages': [self.forms[1]], 'task_site': 'app.profit.example'})
        self.assertEqual(self.pages(self.sid), {'pages': [self.forms[0]], 'task_site': 'wise.com'})

    def test_an_unknown_site_offers_nothing_rather_than_another_tasks(self):
        with self.store.connect() as db:
            db.execute("DELETE FROM preparation_calls WHERE job_id='old'")
        self.assertIsNone(self.app.signin_page(self.other))
        self.assertEqual(self.pages(self.other), {'pages': [], 'task_site': None})
        with patch.object(a.browser_viewer, 'focus') as focus:
            self.assertEqual(self.app.action('browser_focus', {'suggestion_id': self.other}, owner_dashboard=True), {'shown': False, 'unknown': True})
        focus.assert_not_called()
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.other,)).fetchone())
            self.assertIsNone(self.store.suggestion_result(row, db)['preparation_browser']['page'])

    def test_open_the_browser_brings_the_tasks_own_tab(self):
        with patch.object(a.browser_viewer, 'focus', return_value='x') as focus:
            self.app.action('browser_focus', {'suggestion_id': self.other, 'page': 'https://wise.com/home'}, owner_dashboard=True)
        self.assertEqual(focus.call_args[0][0], 'https://app.profit.example/login')

    def test_signing_in_to_one_site_never_carries_on_the_other_task(self):
        with patch.object(a.browser_login, 'fill', return_value={'result': 'done', 'page': None}):
            done = self.app.action('browser_login_fill', {'page': '0:w', 'host': 'wise.com', 'password': SECRET,
                                                          'suggestion_id': self.other}, owner_dashboard=True)
        self.assertEqual(done['resumed'], [self.sid])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM preparations WHERE suggestion_id=?', (self.other,)).fetchone()[0], 'blocked')

    def test_the_watcher_is_keyed_per_site(self):
        looks = [self.forms, [self.forms[1]]]  # the Wise form goes, the other stays
        tabs = [{'id': 'w', 'url': 'https://wise.com/home'}, {'id': 'p', 'url': 'https://app.profit.example/login'}]
        with patch.object(a.browser_login, 'pages', side_effect=lambda config: looks.pop(0) if looks else [self.forms[1]]), \
                patch.object(a.App, 'signin_tabs', return_value=tabs):
            for _ in range(3):
                self.app.watch_sign_ins(every=0)
        with self.store.connect() as db:
            states = dict(db.execute('SELECT suggestion_id,status FROM preparations').fetchall())
        self.assertEqual((states[self.sid], states[self.other]), ('queued', 'blocked'))


class SigninDialogOpens(unittest.TestCase):
    """The dialog opens the task's own sign-in itself (2026-10-20: it hung on "Looking for the sign-in page" once
    the task's tab was closed), and an itsme or eID sign-in carries on by itself once the owner is through."""

    job, steps = SigninHandoff.job, SigninHandoff.steps

    def setUp(self):
        SigninHandoff.setUp(self)

    def block(self, url, reason):
        self.steps(('browser', {'action': 'open', 'targetUrl': url}), ('exec', {'command': 'release lease'}))
        self.store.preparation_blocked(self.sid, self.job()['job_id'], reason)

    def open(self, tabs):
        with patch.object(a.App, 'signin_tabs', return_value=tabs), \
                patch.object(a.browser_login.browser_cdp, 'open_tab', return_value='new-tab') as open_tab, \
                patch.object(a.browser_viewer, 'focus') as focus:
            shown = self.app.action('browser_login_open', {'suggestion_id': self.sid}, owner_dashboard=True)
        return shown, open_tab, focus

    def test_a_closed_tab_is_reopened_at_the_tasks_own_sign_in(self):
        self.block('https://www.example.com/login', HANDOFF)
        shown, open_tab, focus = self.open([{'id': 'x', 'url': 'https://other.invalid/'}])
        self.assertEqual(open_tab.call_args[0][1], 'https://www.example.com/login')
        self.assertEqual(focus.call_args[0][0], 'https://www.example.com/login')
        self.assertEqual((shown['state'], shown['site']), ('opened', 'example.com'))
        self.assertEqual(self.app.signin_opened[self.sid], 'new-tab')

    def test_an_open_tab_is_brought_up_rather_than_a_second_one(self):
        self.block('https://www.example.com/login', HANDOFF)
        shown, open_tab, focus = self.open([{'id': 'mine', 'url': 'https://www.example.com/login?next=1'}])
        open_tab.assert_not_called()
        self.assertEqual(focus.call_args[0][0], 'https://www.example.com/login?next=1')
        self.assertEqual((shown['state'], self.app.signin_opened[self.sid]), ('open', 'mine'))

    def test_an_unknown_site_opens_nothing(self):
        self.steps(('exec', {'command': 'release lease'}))
        self.store.preparation_blocked(self.sid, self.job()['job_id'], HANDOFF)
        shown, open_tab, focus = self.open([])
        open_tab.assert_not_called()
        self.assertEqual(shown['state'], 'unknown')

    def test_no_browser_is_a_plain_error(self):
        self.block('https://www.example.com/login', HANDOFF)
        with patch.object(a.App, 'signin_tabs', side_effect=OSError('refused')):
            with self.assertRaisesRegex(ValueError, 'couldn’t reach the browser'):
                self.app.signin_open(self.sid)

    def test_itsme_or_eid_carries_on_once_back_on_the_site(self):
        reason = 'The Drone Portal asks for itsme or eID; sign in on the open Drone Portal tab, then tap Continue.'
        self.block('https://drones.example.be/login', reason)
        shown, _, _ = self.open([])
        self.assertEqual((shown['site'], shown['kind']), ('Drone Portal', 'eid'))
        tabs = [[{'id': 'new-tab', 'url': 'https://drones.example.be/login'}],
                [{'id': 'new-tab', 'url': 'https://idp.example.org/saml/sso?x=1'}],
                [{'id': 'new-tab', 'url': 'https://drones.example.be/dashboard'}]]
        with patch.object(a.browser_login, 'pages', return_value=[]), \
                patch.object(a.App, 'signin_tabs', side_effect=lambda: tabs.pop(0)):
            for step in range(3):
                self.app.watch_sign_ins(every=0)
                self.assertEqual(self.job()['status'], 'queued' if step == 2 else 'blocked')

    def test_kinds_names_and_sign_in_addresses(self):
        self.assertEqual(a.signin_kind('Sign in with itsme on the open tab'), 'eid')
        self.assertEqual(a.signin_kind('', ['https://idp.iamfas.belgium.be/x']), 'eid')
        self.assertEqual(a.signin_kind('Enter your six-digit authenticator code'), 'code')
        self.assertEqual(a.signin_kind('Zapier shows a switch-account page'), 'account')
        # A code offered next to a security key goes in the dialog; a security key alone is a passkey.
        self.assertEqual(a.signin_kind('Example requires your authenticator code or security key', ['https://accounts.example.com/2fa']), 'code')
        self.assertEqual(a.signin_kind('Example wants your security key', ['https://accounts.example.com/2fa']), 'passkey')
        self.assertEqual(a.signin_kind('Finish signing in', ['https://accounts.example.com/2fa']), 'code')
        self.assertIsNone(a.signin_kind(HANDOFF))
        self.assertEqual(a.signin_name('Enter the code in the ProfitWell tab, then tap Continue.', 'https://www2.profitwell.com/acc/login/'), 'ProfitWell')
        self.assertEqual(a.signin_name('', 'https://www.example.com/login'), 'example.com')
        self.assertTrue(a.signin_address('https://www.example.com/login', 'https://www.example.com/'))
        self.assertTrue(a.signin_address('https://idp.example.org/saml/sso', 'https://www.example.com/'))
        self.assertFalse(a.signin_address('https://www.example.com/dashboard', 'https://www.example.com/'))


class DashboardWiring(unittest.TestCase):
    def test_the_card_and_the_telegram_link_open_the_dialog_for_the_task(self):
        html = Path(__file__).parent.parent.joinpath('dashboard.html').read_text()
        self.assertIn('#signin-for=', html)
        self.assertIn('data-task="${esc(id)}"', html)
        self.assertIn('suggestion_id:signinTask', html)

    def test_the_dialog_opens_the_sign_in_itself_and_never_hangs(self):
        html = Path(__file__).parent.parent.joinpath('dashboard.html').read_text()
        self.assertIn("signinPost('browser_login_open',{suggestion_id:task})", html)
        self.assertIn('signinWithin(', html)
        self.assertIn('id="signin-frame"', html)
        self.assertIn('id="signin-retry"', html)
        self.assertIn("api/progress?id='+encodeURIComponent(signinTask)", html)

    def test_a_waiting_card_shows_it_carried_on_and_closing_the_browser_looks_at_once(self):
        html = Path(__file__).parent.parent.joinpath('dashboard.html').read_text()
        self.assertIn('setInterval(taskSigninPoll,5000)', html)
        self.assertIn("action:'browser_login_check'", html)
        self.assertIn('signinClosed()', html)


if __name__ == '__main__':
    unittest.main()
