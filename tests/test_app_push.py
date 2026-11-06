"""The mobile app's push (notify.app_push, assistant.app_wake) and Share to The Machine (machineShare in new-todo.js).
The app has no Web Push: the control plane wakes the owner's phones with a fixed text per kind, and the Android app asks
this Machine for the to-do's short line (GET /api/notice). Every request to it
here goes to a fake opener; nothing is sent."""
import http.client, io, json, re, subprocess, tempfile, threading, unittest
from pathlib import Path
from unittest.mock import patch
import assistant as a
import dashboard_parts
import notify
from seams import patch_everywhere  # noqa: E402

SUB = {'endpoint': 'https://fcm.googleapis.com/fcm/send/abc', 'keys': {'p256dh': 'B' + 'x' * 86, 'auth': 'y' * 22}}
TOKEN = 'fcm-token:' + 'A' * 140
UTC = a.dt.timezone.utc


class Answer(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *x): return False


class Cloud:
    """A fake control plane: records each /app-push request and answers per action."""
    def __init__(self, **answers):
        self.seen, self.answers = [], {'register': {'id': 'dev_1'}, 'unregister': {'removed': True}, 'list': {'devices': []},
                                       'wake': {'sent': 1, 'removed': 0}, **answers}

    def __call__(self, request, timeout):
        body = json.loads(request.data)
        self.seen.append({'url': request.full_url, 'auth': request.get_header('Authorization'), **body})
        answer = self.answers[body['action']]
        if isinstance(answer, int):
            raise notify.urllib.error.HTTPError(request.full_url, answer, 'no', {}, io.BytesIO())
        return Answer(json.dumps(answer).encode())

    def actions(self):
        return [s['action'] for s in self.seen]


class AppPush(unittest.TestCase):
    def setUp(self):
        notify.reset_active(); self.addCleanup(notify.reset_active)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.config = self.app.config = {'accounts': [], 'dashboard_host': 'the-machine.example', 'dashboard_path': '/assistant/',
                                         'credentials': {'fleet': 'fleet'}, 'fleet': {'url': 'https://cp.example/api/fleet'}}
        self.cloud = Cloud()
        for patcher in (patch_everywhere(a, 'credential', return_value='tok'),
                        patch.object(notify.urllib.request, 'urlopen', side_effect=lambda r, timeout: self.cloud(r, timeout))):
            patcher.start(); self.addCleanup(patcher.stop)
        self.web = []
        self.sender = lambda request: self.web.append(request) or {'results': [{'endpoint': s['endpoint'], 'status': 201} for s in request['subscriptions']]}

    def register(self, **extra):
        return self.app.action('app_push_register', {'platform': 'fcm', 'token': TOKEN, 'label': 'Pixel 8', **extra}, owner_dashboard=True)

    def wakes(self):
        return [s for s in self.cloud.seen if s['action'] == 'wake']

    # -- register and unregister
    def test_register_forwards_to_the_cloud_and_keeps_no_token(self):
        self.assertEqual(self.register(sandbox=True), {'registered': True, 'id': 'dev_1', 'platform': 'fcm', 'label': 'Pixel 8'})
        sent = self.cloud.seen[0]
        self.assertEqual(sent['url'], 'https://cp.example/api/fleet/app-push')
        self.assertEqual(sent['auth'], 'Bearer tok')
        self.assertEqual({k: sent[k] for k in ('action', 'platform', 'token', 'label', 'sandbox')},
                         {'action': 'register', 'platform': 'fcm', 'token': TOKEN, 'label': 'Pixel 8', 'sandbox': True})
        with self.store.connect() as db:
            rows = [dict(r) for r in db.execute('SELECT * FROM notify_app_devices')]
            dump = '\n'.join(db.iterdump())
        self.assertEqual([{k: r[k] for k in ('id', 'platform', 'label')} for r in rows], [{'id': 'dev_1', 'platform': 'fcm', 'label': 'Pixel 8'}])
        self.assertNotIn(TOKEN, dump)  # the token stays with the control plane
        self.assertNotIn('A' * 100, dump)
        self.register()  # each app start registers again: still one phone
        view = self.app.notify_view()
        self.assertEqual([d['id'] for d in view['app_devices']], ['dev_1'])
        self.assertEqual(view['push_devices'], 1)  # counted with the web push devices

    def test_only_the_owners_dashboard_and_valid_input(self):
        for name, args in (('app_push_register', {'platform': 'fcm', 'token': TOKEN}), ('app_push_unregister', {'id': 'dev_1'})):
            with self.assertRaises(ValueError):
                self.app.action(name, args)
        for bad in ({'platform': 'sms', 'token': TOKEN}, {'platform': 'fcm', 'token': 'short'}, {'platform': 'apns', 'token': 'x y' * 20},
                    {'platform': 'fcm', 'token': ['list']}, {'platform': 'fcm'}):
            with self.assertRaises(ValueError):
                self.app.action('app_push_register', bad, owner_dashboard=True)
        with self.assertRaises(ValueError):
            self.app.action('app_push_unregister', {'id': '../x'}, owner_dashboard=True)
        self.assertEqual(self.cloud.seen, [])
        # A label is plain text, short; without one the platform names it
        self.assertEqual(self.register(label='<b>My\nphone</b>' + 'x' * 100)['label'], 'b My phone /b ' + 'x' * 46)
        self.assertEqual(self.app.action('app_push_register', {'platform': 'apns', 'token': 'ab' * 32}, owner_dashboard=True)['label'], 'iPhone')
        self.assertIs(self.cloud.seen[-1]['sandbox'], False)
        for name in ('app_push_register', 'app_push_unregister'):
            self.assertIn(name, a.DASHBOARD_ACTIONS)

    def test_off_the_network_a_plain_answer_not_an_error(self):
        self.config.pop('fleet'); self.config['credentials'] = {}
        self.assertEqual(self.register(), {'registered': False, 'reason': 'network'})
        self.assertEqual(self.cloud.seen, [])
        self.assertFalse(self.app.notify_view()['app_push_ready'])
        self.cloud = Cloud(register={})  # the control plane answered without an id
        self.config.update(credentials={'fleet': 'fleet'}, fleet={'url': 'https://cp.example/api/fleet'})
        with self.assertRaisesRegex(ValueError, 'Try again'):
            self.register()
        with self.store.connect() as db:
            self.assertEqual(notify.app_devices(db), [])

    def test_unregister_removes_both(self):
        self.register()
        self.assertEqual(self.app.action('app_push_unregister', {'id': 'dev_1'}, owner_dashboard=True), {'removed': True})
        self.assertEqual(self.cloud.seen[-1]['action'], 'unregister')
        self.assertEqual(self.cloud.seen[-1]['id'], 'dev_1')
        self.assertEqual(self.app.notify_view()['app_devices'], [])
        # The cloud down: kept here, so it can be removed again; already gone there (404): gone here too
        self.register()
        self.cloud.answers['unregister'] = 503
        with self.assertLogs(a.LOG, 'WARNING'), self.assertRaisesRegex(ValueError, 'Try again'):
            self.app.action('app_push_unregister', {'id': 'dev_1'}, owner_dashboard=True)
        self.assertEqual(len(self.app.notify_view()['app_devices']), 1)
        self.cloud.answers['unregister'] = 404
        with self.assertLogs(a.LOG, 'WARNING'):
            self.app.action('app_push_unregister', {'id': 'dev_1'}, owner_dashboard=True)
        self.assertEqual(self.app.notify_view()['app_devices'], [])

    # -- wakeups
    def test_a_new_todo_wakes_the_phones_with_its_kind_and_tag_and_no_text(self):
        self.register()
        with self.assertLogs(a.LOG, 'INFO') as logs:
            results = a.push_notify(self.store, self.config, {'id': 'card_42', 'title': 'Pay the secret invoice', 'body': 'Hidden', 'status': 'pending'}, self.sender)
        self.assertEqual(results, [{'status': 200, 'app': 1}])  # no web push device: the app alone
        self.assertEqual(self.wakes(), [{'url': 'https://cp.example/api/fleet/app-push', 'auth': 'Bearer tok', 'action': 'wake', 'kind': 'todo', 'tag': 'card_42'}])
        self.assertNotIn('secret', json.dumps(self.cloud.seen))
        self.assertNotIn('tok', '\n'.join(logs.output).replace('kind=todo', ''))
        a.push_notify(self.store, self.config, {'id': 'card_42', 'title': 'T', 'body': 'B', 'status': 'prepared', '_result_notice': True}, self.sender)
        a.push_notify(self.store, self.config, {'id': 'card_43', 'title': 'T', 'body': 'B', 'status': 'pending', 'reminder': True}, self.sender)
        self.assertEqual([(w['kind'], w['tag']) for w in self.wakes()], [('todo', 'card_42'), ('result', 'card_42'), ('reminder', 'card_43')])
        # a later to-do of a batch is silent: no second wakeup
        a.push_notify(self.store, self.config, {'id': 'card_44', 'title': 'T', 'body': 'B', 'status': 'pending', '_silent': True}, self.sender)
        self.assertEqual(len(self.wakes()), 3)

    def test_the_app_line_says_what_is_ready_and_stays_here(self):
        self.register(fetch=True)
        self.assertIs(self.cloud.seen[0]['fetch'], True)  # Android's app shows the notification itself
        self.app.action('app_push_register', {'platform': 'apns', 'token': 'a' * 64, 'fetch': True}, owner_dashboard=True)
        self.assertIs(self.cloud.seen[-1]['fetch'], True)  # and the iPhone's Notification Service extension
        self.cloud.seen.clear()
        title = 'Reply to the landlord about the listing on Main Street, with the photos and the signed lease'
        cases = [({'status': 'prepared', '_result_notice': True}, 'result', 'ready', 'Ready: '),
                 ({'status': 'accepted', 'preparation_status': 'blocked', 'preparation_reason': 'Which time?', '_result_notice': True},
                  'result', 'needs', 'Needs your help: '),
                 ({'status': 'pending'}, 'todo', None, 'New to-do: '),
                 ({'status': 'pending', 'reminder': True}, 'reminder', None, 'Reminder: ')]
        for i, (row, kind, state, lead) in enumerate(cases):
            with self.subTest(kind=kind, state=state):
                a.push_notify(self.store, self.config, {'id': f'card_{i}', 'title': title, 'body': 'B', **row}, self.sender)
                wake = self.wakes()[-1]
                self.assertEqual((wake['kind'], wake['tag'], wake.get('state')), (kind, f'card_{i}', state))
                with self.store.connect() as db:
                    line = notify.app_line(db, f'card_{i}')
                self.assertTrue(line.startswith(lead + 'Reply to the landlord'), line)
                self.assertLessEqual(len(line), notify.APP_LINE)
                self.assertTrue(line.endswith('…'))
        # The title never goes to the cloud, only the kind, the state and the to-do's id
        self.assertNotIn('landlord', json.dumps(self.cloud.seen))
        # A short title stays whole
        a.push_notify(self.store, self.config, {'id': 'card_9', 'title': 'Pick a time with Sam', 'body': 'B', 'status': 'prepared',
                                                '_result_notice': True}, self.sender)
        with self.store.connect() as db:
            self.assertEqual(notify.app_line(db, 'card_9'), 'Ready: Pick a time with Sam')

    def test_text_in_notifications_off_keeps_the_app_line_plain(self):
        self.register(fetch=True)
        with patch.object(a.security_levels, 'notify_text', return_value=False):
            a.push_notify(self.store, self.config, {'id': 'card_1', 'title': 'Pay the secret invoice', 'body': 'B', 'status': 'prepared',
                                                    '_result_notice': True}, self.sender)
            a.push_notify(self.store, self.config, {'id': 'card_2', 'title': 'Pay the secret invoice', 'body': 'B', 'status': 'pending'}, self.sender)
        with self.store.connect() as db:
            self.assertEqual((notify.app_line(db, 'card_1'), notify.app_line(db, 'card_2')), ('Ready', 'New to-do'))
            self.assertNotIn('secret', json.dumps([list(r) for r in db.execute('SELECT * FROM notify_app_lines')]))

    def test_a_held_push_keeps_its_line_for_the_app(self):
        self.register(fetch=True)
        notify.mark_active(client='desk', on=True)
        a.push_notify(self.store, self.config, {'id': 'card_1', 'title': 'Pick a time with Sam', 'body': 'B', 'status': 'prepared',
                                                '_result_notice': True}, self.sender)
        self.assertEqual(self.wakes(), [])
        with self.store.connect() as db:
            payload = json.loads(db.execute("SELECT payload FROM notify_queue WHERE channel='push'").fetchone()[0])
        a.push_send(self.store, self.config, [{'endpoint': SUB['endpoint']}], payload, 'held', self.sender, kind='result', held=True)
        self.assertEqual(self.wakes()[-1].get('state'), 'ready')
        self.assertNotIn('_line', json.dumps(self.web))  # the web push gets its own payload only
        with self.store.connect() as db:
            self.assertEqual(notify.app_line(db, 'card_1'), 'Ready: Pick a time with Sam')

    def test_app_lines_are_short_recent_and_by_id_only(self):
        with self.store.connect() as db:
            notify.app_line_save(db, 'old', 'Ready: old', at=notify.wall() - 4 * 86400)
            notify.app_line_save(db, 'new', 'Ready: ' + 'x' * 100)
            self.assertEqual(notify.app_line(db, 'old'), '')
            self.assertEqual(len(notify.app_line(db, 'new')), notify.APP_LINE)
            self.assertEqual(notify.app_line(db, "new' OR 1=1"), '')
            for i in range(notify.APP_LINES + 5):
                notify.app_line_save(db, f't{i}', 'x', at=notify.wall() + i)
            self.assertEqual(db.execute('SELECT count(*) FROM notify_app_lines').fetchone()[0], notify.APP_LINES)
        self.assertEqual(notify.clip('Reply to Gianni about the listing'), 'Reply to Gianni about the listing')
        self.assertEqual(notify.clip('word ' * 20, 22), 'word word word word…')
        self.assertEqual(notify.clip('x' * 80, 10), 'x' * 9 + '…')
        self.assertEqual(notify.clip('a\nb\tc'), 'a b c')

    def test_the_app_asks_for_its_line_with_the_owners_sign_in(self):
        with self.store.connect() as db:
            notify.app_line_save(db, 'card_1', 'Ready: Pick a time with Sam')
        app = object.__new__(a.App)
        app.store, app.token, app.stop = self.store, 'test-token', threading.Event()
        app.graph_dirty = threading.Event()
        app.owner_token = 'owner-key'
        app.config = {'accounts': [], 'tailscale_owner': 'owner@example.com', 'dashboard_host': 'machine.example:8443', 'port': 0, 'http_timeout': 1}
        servers, real = [], a.http.server.ThreadingHTTPServer
        def capture(*args, **kwargs):
            servers.append(real(*args, **kwargs)); return servers[-1]
        for patcher in (patch.object(a.http.server, 'ThreadingHTTPServer', side_effect=capture), patch.object(a.signal, 'signal'),
                        patch.object(a.App, 'preparation_worker'), patch.object(a.App, 'delivery_worker')):
            patcher.start(); self.addCleanup(patcher.stop)
        thread = threading.Thread(target=app.serve, daemon=True)
        thread.start()
        while not servers:
            pass
        self.addCleanup(lambda: (app.stop.set(), thread.join(5)))
        def get(path, login='owner@example.com'):
            conn = http.client.HTTPConnection('127.0.0.1', servers[0].server_address[1], timeout=10)
            conn.request('GET', path, headers={'Host': 'machine.example:8443', 'Tailscale-User-Login': login})
            r = conn.getresponse()
            body = json.loads(r.read())
            conn.close()
            return r.status, body
        # a tag that is no to-do (the morning, a Fleet question): its kept line, no buttons
        self.assertEqual(get('/api/notice?tag=card_1'), (200, {'line': 'Ready: Pick a time with Sam', 'title': 'Ready: Pick a time with Sam', 'body': '', 'actions': []}))
        self.assertEqual(get('/api/notice?tag=card_2'), (200, {'line': '', 'title': '', 'body': '', 'actions': []}))
        self.assertEqual(get('/api/notice'), (200, {'line': '', 'title': '', 'body': '', 'actions': []}))
        sid = self.card('Pick a time with Sam')
        status, notice = get('/api/notice?tag=' + sid)
        self.assertEqual((status, notice['title'], notice['actions']), (200, 'New to-do: Pick a time with Sam', ['prepare', 'snooze', 'done']))
        with patch('sys.stderr'):
            self.assertEqual(get('/api/notice?tag=card_1', login='someone@example.com')[0], 403)

    # -- what the notification says, its buttons, and taking it away
    def event(self):
        with self.store.connect() as db:
            known = db.execute('SELECT id FROM events').fetchone()
        if not known:
            self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': '2026-10-20T08:00:00+00:00',
                                                 'title': 'Invoice', 'body': 'Please pay.', 'deleted': False, 'metadata': {'thread_id': 't1'}}])
            with self.store.connect() as db:
                known = db.execute('SELECT id FROM events').fetchone()
        return known[0]

    def card(self, title='Pay the Monizze invoice', body='The Monizze invoice of 120 EUR is due Friday. It came by email.', **fields):
        sid = self.store.suggest(title, title, body, [self.event()])['id']
        with self.store.connect() as db:
            for key, value in fields.items():
                db.execute(f'UPDATE suggestions SET {key}=? WHERE id=?', (value, sid))
        return sid

    def test_the_notice_has_the_title_and_next_step_and_the_buttons_for_where_it_is(self):
        new = a.app_notice(self.store, self.config, self.card())
        self.assertEqual((new['title'], new['body'], new['actions']),
                         ('New to-do: Pay the Monizze invoice', 'The Monizze invoice of 120 EUR is due Friday.', ['prepare', 'snooze', 'done']))
        self.assertEqual(new['labels'], {'prepare': 'Prepare', 'snooze': 'Snooze', 'done': 'Mark done', 'open': 'Open'})
        self.assertEqual(new['events'], {'prepare': 'Preparing it', 'snooze': 'Snoozed it', 'done': 'Marked it done',
                                         'failed': 'Couldn’t reach your Machine. Open the app to try again.'})
        self.assertEqual(new['line'], new['title'])  # what an older app shows
        reply = json.dumps({'kind': 'email', 'account_id': 'work', 'to': ['Sam Lee <sam@client.example>'], 'subject': 'Re: Meeting',
                            'body': 'Hi Sam,\n\nTuesday 10:00 works for me. See you then.', 'revision': 'r1'})
        ready = a.app_notice(self.store, self.config, self.card('Pick a time with Sam', status='prepared', next_action=reply))
        self.assertEqual((ready['title'], ready['body'], ready['actions']),
                         ('Ready: Pick a time with Sam', 'Send to Sam Lee: Tuesday 10:00 works for me.', ['snooze', 'done']))
        labelled = json.dumps({'kind': 'email', 'label': 'Reply to Sam', 'to': ['sam@client.example'], 'body': 'Confirm Tuesday 10:00.', 'revision': 'r1'})
        self.assertEqual(a.app_notice(self.store, self.config, self.card('Meeting', status='prepared', next_action=labelled))['body'],
                         'Reply to Sam: Confirm Tuesday 10:00.')
        asks = a.app_notice(self.store, self.config, self.card('Book the trip', status='prepared', outcome=json.dumps({'needs': 'Which dates work?'})))
        self.assertEqual(asks['body'], 'Which dates work?')
        self.assertEqual(a.app_notice(self.store, self.config, self.card('Draft the plan', status='accepted'))['title'], 'Preparing: Draft the plan')
        long = a.app_notice(self.store, self.config, self.card('Pay ' + 'the very long invoice ' * 3, 'Pay ' + 'y' * 300 + '.'))
        self.assertLessEqual((len(long['title']), len(long['body'])), (notify.APP_LINE, a.APP_BODY))
        for status in a.APP_GONE:
            self.assertEqual(a.app_notice(self.store, self.config, self.card('Gone ' + status, status=status)), {'gone': True})

    def test_ready_leads_only_where_something_was_prepared_to_review(self):
        # "Ready:" in front fits a draft or handoff waiting for the owner's OK, not a to-do about what someone
        # else promised them ("Waiting on Sam: ..."), nor one back from a snooze: judged by what the to-do is.
        event = self.event()
        with self.store.connect() as db:
            for direction in ('theirs', 'mine'):
                db.execute("INSERT INTO promises(direction,who,what,check_at,event_id,account_id,status,created_at,updated_at) "
                           "VALUES(?,'Sam Lee','the quote','2026-10-21T08:00:00+00:00',?,'work','carded','x','x')", (direction, event))
            theirs, mine = [r[0] for r in db.execute('SELECT id FROM promises ORDER BY id')]
        handoff = json.dumps({'kind': 'email', 'account_id': 'work', 'to': ['sam@client.example'], 'body': 'Any news on the quote?', 'revision': 'r1'})
        def promised(pid, title):
            sid = self.store.suggest('promise:%d' % pid, title, 'Promised on Monday.', [event])['id']
            with self.store.connect() as db:
                db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (handoff, sid))
            return sid
        waiting = promised(theirs, 'Waiting on Sam Lee: the quote')
        self.assertEqual(a.app_notice(self.store, self.config, waiting)['title'], 'Waiting on Sam Lee: the quote')
        self.assertEqual(a.app_notice(self.store, self.config, promised(mine, 'Send Sam the deck'))['title'], 'Ready: Send Sam the deck')
        back = self.card('Call the plumber', status='prepared', outcome=json.dumps({'state': 'snoozed'}))
        self.assertEqual(a.app_notice(self.store, self.config, back)['title'], 'Reminder: Call the plumber')
        # the web push, the phone's line and Telegram say the same
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        self.register(fetch=True)
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (waiting,)).fetchone(), _result_notice=True)
            row['_lead'] = a.result_lead(db, row)
        a.push_notify(self.store, self.config, row, self.sender)
        with self.store.connect() as db:
            self.assertEqual(notify.app_line(db, waiting), 'Waiting on Sam Lee: the quote')
        self.assertEqual(self.web[-1]['payload']['title'], 'Waiting on Sam Lee: the quote')
        with patch_everywhere(a, 'telegram_request', side_effect=lambda config, args: args):
            sent = a.telegram({**self.config, 'dashboard_host': 'machine.example'}, {**row, 'message_id': 'web-1'}, 'send')
        self.assertTrue(sent['message'].startswith('**Waiting on Sam Lee: the quote**'), sent['message'])
        with self.store.connect() as db:
            a.security_levels.set_pref(db, 'notify_text', 'off')
        self.assertEqual(a.app_notice(self.store, self.config, waiting)['title'], 'To-do')

    def test_text_in_notifications_off_the_notice_keeps_to_the_fixed_words(self):
        with self.store.connect() as db:
            a.security_levels.set_pref(db, 'notify_text', 'off')
        notice = a.app_notice(self.store, self.config, self.card('Pay the secret invoice', status='prepared'))
        self.assertEqual((notice['title'], notice['body'], notice['actions']), ('Ready', '', ['snooze', 'done']))
        self.assertNotIn('secret', json.dumps(notice))

    def test_a_todo_that_no_longer_waits_takes_its_notification_away_once(self):
        self.register()
        done, waiting = self.card('Done one'), self.card('Still waiting')
        for sid in (done, waiting):
            a.push_notify(self.store, self.config, {'id': sid, 'title': 'T', 'body': 'B', 'status': 'pending'}, self.sender)
        with self.store.connect() as db:
            notify.app_line_save(db, 'digest', 'Your morning')
        self.assertEqual(a.app_clear_step(self.store, self.config), [])
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='completed' WHERE id=?", (done,))
        self.assertEqual(a.app_clear_step(self.store, self.config), [done])
        self.assertEqual(self.wakes()[-1], {'url': 'https://cp.example/api/fleet/app-push', 'auth': 'Bearer tok', 'action': 'wake', 'kind': 'clear', 'tag': done})
        self.assertEqual(a.app_clear_step(self.store, self.config), [])  # once
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='snoozed' WHERE id=?", (waiting,))
            self.assertEqual(sorted(notify.app_lines(db)), sorted(['digest', waiting]))
        self.assertEqual(a.app_clear_step(self.store, self.config), [waiting])
        self.assertEqual(len([w for w in self.wakes() if w['kind'] == 'clear']), 2)

    def test_the_morning_notice_has_a_body_from_the_digest(self):
        # The phone showed "Your morning" with an empty body: the digest's line and body are kept for its wakeup and
        # GET /api/notice returns both. Neither goes to the cloud.
        self.register()
        a.push_send(self.store, self.config, [], {'title': 'Your morning', 'body': '2 to-dos: Reply to Sam, Pay the invoice · First meeting 10:00',
                                                  'url': '.', 'tag': 'digest', '_line': 'Your morning',
                                                  '_body': '2 to-dos: Reply to Sam, Pay the invoice · First meeting 10:00'}, 'digest', self.sender, wake='digest')
        self.assertEqual(self.wakes()[-1], {'url': 'https://cp.example/api/fleet/app-push', 'auth': 'Bearer tok', 'action': 'wake', 'kind': 'digest', 'tag': 'digest'})
        notice = a.app_notice(self.store, self.config, 'digest')
        self.assertEqual((notice['title'], notice['body']), ('Your morning', '2 to-dos: Reply to Sam, Pay the invoice · First meeting 10:00'))
        self.assertNotIn('Sam', json.dumps(self.wakes()))

    def test_the_morning_digest_wakes_the_phone_with_its_body(self):
        self.register()
        self.card('Reply to Sam about Tuesday')
        morning = a.dt.datetime(2026, 10, 12, 8, 40, tzinfo=a.dt.timezone.utc)
        with patch_everywhere(a, 'local_tz', return_value=a.dt.timezone.utc):
            self.app.digest_step(current=morning, push=self.sender)
        notice = a.app_notice(self.store, self.config, 'digest')
        self.assertEqual((notice['title'], notice['body']), ('Your morning', '1 to-do: Reply to Sam about Tuesday'))

    def test_a_clear_with_a_broken_cloud_is_quiet(self):
        self.register()
        sid = self.card()
        a.push_notify(self.store, self.config, {'id': sid, 'title': 'T', 'body': 'B', 'status': 'pending'}, self.sender)
        self.cloud.answers['wake'] = 500
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='completed' WHERE id=?", (sid,))
        self.assertEqual(a.app_clear_step(self.store, self.config), [sid])

    def test_web_push_and_app_together_and_a_broken_cloud_never_stops_web_push(self):
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        self.register()
        results = a.push_notify(self.store, self.config, {'id': 'c1', 'title': 'T', 'body': 'B', 'status': 'pending'}, self.sender)
        self.assertEqual(results, [{'endpoint': SUB['endpoint'], 'status': 201}, {'status': 200, 'app': 1}])
        self.cloud.answers['wake'] = 500
        with self.assertLogs(a.LOG, 'WARNING'):
            results = a.push_notify(self.store, self.config, {'id': 'c2', 'title': 'T', 'body': 'B', 'status': 'pending'}, self.sender)
        self.assertEqual(results, [{'endpoint': SUB['endpoint'], 'status': 201}])
        self.assertEqual(len(self.web), 2)
        # nothing registered: no request to the cloud at all
        with self.store.connect() as db:
            notify.app_device_remove(db, ['dev_1'])
        before = len(self.cloud.seen)
        a.push_notify(self.store, self.config, {'id': 'c3', 'title': 'T', 'body': 'B', 'status': 'pending'}, self.sender)
        self.assertEqual(len(self.cloud.seen), before)

    def test_prefs_and_holds_apply_to_the_app_too(self):
        self.register()
        self.app.action('notify_set', {'kind': 'todo', 'channel': 'push', 'on': False}, owner_dashboard=True)
        self.assertEqual(a.push_notify(self.store, self.config, {'id': 'c1', 'title': 'T', 'body': 'B', 'status': 'pending'}, self.sender), [])
        self.assertEqual(self.wakes(), [])
        self.app.action('notify_set', {'kind': 'todo', 'channel': 'push', 'on': True}, owner_dashboard=True)
        # A dashboard in use: held, then sent by notify_step once they are away, unless they saw it
        t0 = a.dt.datetime(2026, 10, 12, 10, 0, tzinfo=UTC).timestamp()
        notify.mark_active(lambda: t0, client='desk', on=True)
        notify.mark_active(lambda: t0 + 5, client='desk', on=False)  # just left: held for a minute
        with patch.object(notify.time, 'time', return_value=t0 + 10):
            a.push_notify(self.store, self.config, {'id': 'c1', 'title': 'T', 'body': 'B', 'status': 'pending'}, self.sender)
        self.assertEqual(self.wakes(), [])
        later = t0 + 5 + notify.AWAY_GRACE
        with patch.object(notify.time, 'time', return_value=later), patch_everywhere(a, 'local_tz', return_value=UTC):
            went = self.app.notify_step(current=a.dt.datetime.fromtimestamp(later, UTC), push=self.sender, mail=lambda *x: True)
        self.assertEqual(went, ['push'])
        self.assertEqual([(w['kind'], w['tag']) for w in self.wakes()], [('todo', 'c1')])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM notify_queue WHERE channel='push'").fetchone()[0], 0)

    def test_fleet_digest_and_held_fleet_keep_their_kind(self):
        self.register()
        rows = [{'id': 'q_1', 'name': 'Kim Lee', 'kind': 'intro', 'question': json.dumps({'about': 'Acme'})}]
        with patch.object(a.fleet, 'push_payload', return_value={'title': 'Kim asks', 'body': 'x', 'url': '.', 'tag': 'fleet-q_1'}):
            a.fleet_push(self.store, self.config, rows, self.sender)
        self.assertEqual((self.wakes()[-1]['kind'], self.wakes()[-1]['tag']), ('fleet', 'fleet-q_1'))
        # held while in use, it still wakes as a Fleet one later
        notify.mark_active(client='desk', on=True)
        with patch.object(a.fleet, 'push_payload', return_value={'title': 'Kim asks', 'body': 'x', 'url': '.', 'tag': 'fleet-q_2'}):
            a.fleet_push(self.store, self.config, rows, self.sender)
        with self.store.connect() as db:
            payload = json.loads(db.execute("SELECT payload FROM notify_queue WHERE channel='push'").fetchone()[0])
        self.assertEqual(payload['_wake'], 'fleet')
        a.push_send(self.store, self.config, [], payload, 'held', self.sender, kind='result', held=True)
        self.assertEqual((self.wakes()[-1]['kind'], self.wakes()[-1]['tag']), ('fleet', 'fleet-q_2'))
        # the digest; silent at the dashboard: no wakeup
        a.push_send(self.store, self.config, [], {'title': 'Your morning', 'body': '', 'url': '.', 'tag': 'digest'}, 'digest', self.sender, wake='digest')
        self.assertEqual(self.wakes()[-1]['kind'], 'digest')
        n = len(self.wakes())
        a.push_send(self.store, self.config, [], {'title': 'Your morning', 'tag': 'digest', 'silent': True}, 'digest', self.sender, wake='digest')
        self.assertEqual(len(self.wakes()), n)
        # a tag that isn't an id is never passed on
        a.push_send(self.store, self.config, [], {'title': 'x', 'tag': 'a b/c'}, 'x', self.sender, wake='digest')
        self.assertEqual(self.wakes()[-1]['tag'], 'digest')

    def test_the_brief_and_the_morning_name_their_own_view(self):
        """A tapped notification opens the dashboard at #chat=<tag> (mobile/www/inject.js); the dashboard's pushRoute
        sends a tag that is no to-do to its view (tests/test_push_links_dashboard.mjs). The brief's tag names its Fleet,
        and the morning's web push opens the Calendar's agenda, like the app's."""
        self.register()
        fl = 'fl_' + 'a' * 16
        self.app.fleet_notify_brief('Your Fleet this week\n\nGlobex waits', 'https://m.example/#fleet-brief=' + fl)
        self.assertEqual((self.wakes()[-1]['kind'], self.wakes()[-1]['tag']), ('fleet', 'fleet-brief-' + fl))
        self.app.fleet_notify_brief('Your Fleet this week', '')  # no address for the dashboard: the tag still opens a brief
        self.assertEqual(self.wakes()[-1]['tag'], 'fleet-brief')
        self.assertEqual(notify.compose([], [{'title': 'A'}], [], 'https://m.example/')['push']['url'], 'https://m.example/#calendar?view=agenda')
        self.assertEqual(notify.compose([], [{'title': 'A'}], [])['push']['url'], './#calendar?view=agenda')

    def test_the_team_brief_notification_has_a_body_from_its_items(self):
        # "What your Fleet saw" showed no line under it on the phone: its items' titles, as the brief shows them,
        # make the body; Text in notifications off: only how many. Kept on the Machine for the app, not sent to the cloud.
        self.register()
        fl = 'fl_' + 'b' * 16
        titles = ['Acme is waiting for a reply (3 emails)', 'Globex went quiet', 'Kim and Sam meet Initech on Tuesday']
        self.app.fleet_notify_brief('Your Fleet today\n• ...', 'https://m.example/#fleet-brief=' + fl, titles)
        notice = a.app_notice(self.store, self.config, 'fleet-brief-' + fl)
        self.assertEqual((notice['title'], notice['body']), ('What your Fleet saw', '3 things for the team: Acme is waiting for a reply (3 emails), Globex went quiet, …'))
        self.assertNotIn('Acme', json.dumps(self.wakes()))
        self.app.fleet_notify_brief('Your Fleet today', '', [])
        self.assertEqual(a.app_notice(self.store, self.config, 'fleet-brief')['body'], 'Nothing that needs the team.')
        with self.store.connect() as db:
            a.security_levels.set_pref(db, 'notify_text', 'off')
        self.app.fleet_notify_brief('Your Fleet today', 'https://m.example/#fleet-brief=' + fl, titles)
        self.assertEqual(a.app_notice(self.store, self.config, 'fleet-brief-' + fl)['body'], '3 things for the team')

    def test_devices_the_cloud_dropped_go_here_too(self):
        self.register()
        self.cloud.answers.update(register={'id': 'dev_2'})
        self.register(label='Old phone')
        self.cloud.answers.update(wake={'sent': 1, 'removed': 1}, list={'devices': [{'id': 'dev_1', 'platform': 'fcm', 'label': 'Pixel 8'}]})
        a.push_notify(self.store, self.config, {'id': 'c1', 'title': 'T', 'body': 'B', 'status': 'pending'}, self.sender)
        self.assertEqual([d['id'] for d in self.app.notify_view()['app_devices']], ['dev_1'])
        self.cloud.answers.update(wake={'sent': 0, 'removed': ['dev_1']})
        a.push_notify(self.store, self.config, {'id': 'c2', 'title': 'T', 'body': 'B', 'status': 'pending'}, self.sender)
        self.assertEqual(self.app.notify_view()['app_devices'], [])

    def test_reach_counts_the_app(self):
        self.assertEqual(a.reminder_channels(self.store, self.config)['push'], 0)
        self.register()
        self.assertEqual(a.reminder_channels(self.store, self.config)['push'], 1)
        self.assertTrue(self.app.fleet_pings())
        self.config['credentials'] = {}  # unpaired: the app can't be reached
        self.assertEqual(a.reminder_channels(self.store, self.config)['push'], 0)

    def test_push_test_from_the_app_wakes_that_phone_only(self):
        self.register()
        self.assertEqual(self.app.action('push_test', {'app_device': 'dev_1'}, owner_dashboard=True), {'sent': True})
        self.assertEqual(self.wakes()[-1], {'url': 'https://cp.example/api/fleet/app-push', 'auth': 'Bearer tok', 'action': 'wake',
                                            'kind': 'test', 'tag': 'push-test', 'id': 'dev_1'})
        with self.assertRaises(ValueError):
            self.app.action('push_test', {'app_device': 'dev_9'}, owner_dashboard=True)
        with self.assertRaises(ValueError):
            self.app.action('push_test', {'app_device': 'dev_1'})
        self.cloud.answers['wake'] = {'sent': 0, 'removed': 0}
        with self.assertRaisesRegex(ValueError, 'didn’t go through'):
            self.app.action('push_test', {'app_device': 'dev_1'}, owner_dashboard=True)


class PhoneApp(unittest.TestCase):
    """Settings, Phone app: a QR code of the app's connect link for a self-hosted Machine, a line for a hosted one."""
    def test_self_hosted_gets_the_connect_link_and_its_code(self):
        view = a.phone_app({'dashboard_host': 'machine.tailnet.ts.net', 'dashboard_path': '/assistant/'})
        self.assertEqual(view['url'], 'https://machine.tailnet.ts.net/assistant/')
        self.assertEqual(view['link'], 'computer.themachine.app://connect?u=https%3A%2F%2Fmachine.tailnet.ts.net%2Fassistant%2F')
        self.assertEqual(view['qr'], a.qr.encode(view['link']))
        self.assertEqual(set(view), {'hosted', 'url', 'link', 'qr'})  # nothing secret in it
        self.assertEqual(a.phone_app({'manage_url': 'https://app.example/manage', 'dashboard_host': 'x.example'}), {'hosted': True})
        self.assertEqual(a.phone_app({}), {'hosted': False})

    def test_on_the_network_it_signs_in_like_a_hosted_machine(self):
        config = {'dashboard_host': 'machine.tailnet.ts.net'}
        with patch_everywhere(a, 'cloud_target', return_value=('https://app.example', 'token')):
            self.assertEqual(a.phone_app(config), {'hosted': True})  # no code: the account finds it
        with patch_everywhere(a, 'cloud_target', return_value=None):
            self.assertIn('qr', a.phone_app(config))

    def test_the_dashboard_shows_it_and_the_network_line_once(self):
        source = (Path(a.ROOT) / 'dashboard' / 'settings-device.js').read_text(encoding='utf-8')
        body = re.search(r'^function phoneAppRender\(\).*?(?=^\S)', source, re.M | re.S)[0]
        self.assertIn('qrSvg(p.qr)', body)
        self.assertIn("t('Install the app, then scan this with the phone’s camera.')", body)
        self.assertIn("t('The app signs in with your account.')", body)
        self.assertIn("t('Not on the Network?')", body)  # the code only folded, for a Machine not on the Network
        self.assertLess(body.index("<details class=\"connect-alt phone-own\">"), body.index('qrSvg(p.qr)'))
        self.assertIn("devStore.set('app-push-network',1)", body)  # remembered: said once
        self.assertIn("t('Notifications in the app need The Machine Network. The app works without them.')", body)


class Share(unittest.TestCase):
    def test_new_todo_defines_machine_share_that_only_opens_the_dialog(self):
        source = (Path(a.ROOT) / 'dashboard' / 'new-todo.js').read_text(encoding='utf-8')
        page = dashboard_parts.assemble(Path(a.ROOT))
        self.assertIn('window.machineShare=function', page)
        body = re.search(r'window\.machineShare=function.*?return true};', source, re.S)[0]
        self.assertIn('ncOpen()', body)
        self.assertIn('ncAddFiles(files)', body)
        self.assertIn("$('#nc-text')", body)
        self.assertNotIn('ncCreate', body)  # the owner presses Add: nothing is created by itself
        self.assertNotIn('card_new', body)



class InApp(unittest.TestCase):
    """In the mobile app (Apple 3.1.3(b), Google Play the same) nothing leads to buying: the page marks itself .in-app
    from the WebView's user agent and hides every [data-buy]. Open account stays, for deleting the account (5.1.1(v))."""
    def test_detection_and_rule(self):
        page = dashboard_parts.assemble(Path(a.ROOT))
        head = page[:page.index('</script>')]  # set before anything renders
        self.assertIn("/ TheMachineApp\\/\\d/.test(navigator.userAgent))document.documentElement.classList.add('in-app')", head)
        self.assertIn('.in-app [data-buy]{display:none!important}', page)

    def test_account_buttons_that_buy_are_marked_and_open_account_is_not(self):
        source = (Path(a.ROOT) / 'dashboard' / 'settings-general.js').read_text(encoding='utf-8')
        code = '\n'.join(re.search(rf'^(?:const|function) {name}\b.*?$(?:\n .*$)*', source, re.M)[0] for name in ('ACCT_GO', 'ACCT_BUY', 'acctGo'))
        script = ('const esc=s=>String(s);' + code + ';const links={account:"https://a.example/a",plan:"https://a.example/p",portal:"https://a.example/b",'
                  'cancel:"https://a.example/c",fleet:"https://a.example/f",connections:"https://a.example/s"},actions=Object.keys(links);'
                  'const out={};for(const k of actions)out[k]=[acctGo({actions,links},k),acctGo({actions,links,hop:true},k)];console.log(JSON.stringify(out))')
        out = json.loads(subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True).stdout)
        for key, html in out.items():
            for one in html:
                self.assertEqual('data-buy' in one, key in ('plan', 'portal', 'cancel', 'fleet'), (key, one))
        self.assertIn('<div data-buy><span class="grow">Next invoice', source)
        self.assertIn('<small data-buy>${esc(p.price)}</small>', source)
        # The quiet end of the tab also holds Delete account, which the app keeps: each buying link is marked, and the
        # line goes when nothing in it is left to show
        self.assertIn("end.innerHTML=quiet.join('')", source)
        self.assertIn('.in-app .acct-danger:not(:has(>:not([data-buy]))){display:none}', dashboard_parts.assemble(Path(a.ROOT)))
        self.assertIn("const ACCT_BUY=new Set(['plan','portal','cancel','fleet','billing','withdraw']);", source)
        self.assertIn("b.toggleAttribute('data-buy',!paired)", source)  # Join the Network (a sign-up) when not paired


if __name__ == '__main__':
    unittest.main()
