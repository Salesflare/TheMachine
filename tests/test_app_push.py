"""The mobile app's push (notify.app_push, assistant.app_wake) and Share to The Machine (machineShare in new-todo.js).
The app has no Web Push: the control plane wakes the owner's phones with a fixed text per kind. Every request to it
here goes to a fake opener; nothing is sent."""
import io, json, re, subprocess, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import assistant as a
import dashboard_parts
import notify

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
        for patcher in (patch.object(a, 'credential', return_value='tok'),
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
        self.assertEqual(self.register(sandbox=True), {'id': 'dev_1', 'platform': 'fcm', 'label': 'Pixel 8'})
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

    def test_without_the_cloud_a_clear_error(self):
        self.config.pop('fleet'); self.config['credentials'] = {}
        with self.assertRaisesRegex(ValueError, 'paired with an account'):
            self.register()
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
        with patch.object(notify.time, 'time', return_value=later), patch.object(a, 'local_tz', return_value=UTC):
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
        self.assertIn('<div class="acct-cancel" data-buy>', source)
        self.assertIn("b.toggleAttribute('data-buy',!paired)", source)  # Join the Network (a sign-up) when not paired


if __name__ == '__main__':
    unittest.main()
