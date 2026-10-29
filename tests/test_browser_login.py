"""The sign-in dialog's path: fields found and filled in a real (headless) browser, the saved sign-ins encrypted, and
the actions for the owner on the dashboard only. Made-up credentials only."""
import http.server, json, os, shutil, socket, subprocess, sys, tempfile, threading, time, unittest, urllib.request
from pathlib import Path

import browser_login
import moving

USER, SECRET, CODE = 'test-user@example.invalid', 'not-a-real-password-123', '424242'

PAGES = {
    '/login': b'''<!doctype html><meta charset="utf-8"><title>Log in</title><form action="/after" method="post">
        <input name="email" type="email"><input name="pw" type="password"><button>Log in</button></form>''',
    '/after': b'<!doctype html><title>Code</title><form action="/home" method="post"><input name="otp" autocomplete="one-time-code"><button>Verify</button></form>',
    '/home': b'<!doctype html><title>Home</title><p>Welcome</p>',
    '/stuck': b'''<!doctype html><meta charset="utf-8"><title>Log in</title><form onsubmit="event.preventDefault()">
        <input name="username"><input type="password"><button>Sign in</button></form>''',
    '/news': b'<!doctype html><title>News</title><form><input name="q"><button>Search</button></form>',
    # One-time code pages, each saying in its own words which code it wants.
    '/sms': '''<!doctype html><meta charset="utf-8"><title>Verify</title><meta property="og:site_name" content="Stripe"><main><h1>Two-step authentication</h1>
        <p>Enter the code we sent to <b>\u2022\u2022\u2022\u2022 12</b>.</p>
        <form action="/sms-check" method="post"><input name="code" autocomplete="one-time-code" inputmode="numeric"><button>Continue</button></form>
        <p>Didn't get it? <button type="button" onclick="document.title='resent'">Resend code</button></p>
        <a href="/totp">Use authenticator app instead</a> <a href="https://elsewhere.invalid/x">Use another method</a> <a href="/out">Sign out</a></main>'''.encode(),
    '/sms-check': '''<!doctype html><meta charset="utf-8"><title>Verify</title><main><h1>Two-step authentication</h1><p>Enter the code we sent to \u2022\u2022\u2022\u2022 12.</p>
        <p role="alert">That code isn't right. Try again.</p>
        <form action="/home" method="post"><input name="code" autocomplete="one-time-code" aria-invalid="true"><button>Continue</button></form></main>'''.encode(),
    '/totp': b'''<!doctype html><meta charset="utf-8"><title>Verify</title><div class="card"><h2>Authentication app</h2><label for="t">Enter the 6-digit code from your authenticator app</label>
        <form action="/home" method="post"><input id="t" name="otp"><button>Verify</button></form><a href="/sms">Text me a code instead</a></div>''',
    '/email': '''<!doctype html><meta charset="utf-8"><title>Check your inbox</title><section><h1>Check your email</h1><p>We emailed a code to j\u2022\u2022\u2022@example.com.</p>
        <form action="/home" method="post"><input name="verification" autocomplete="one-time-code"><button>Verify</button></form></section>'''.encode(),
    '/unknown': b'''<!doctype html><meta charset="utf-8"><title>Verify</title><form action="/home" method="post"><p>Enter your verification code to continue.</p>
        <input name="passcode"><button>Submit</button></form><p>Questions? Write to help@example.com</p>''',
    # LinkedIn's way: after the password, nothing to type, "approve the sign-in in your app" on a checkpoint address
    '/applogin': b'''<!doctype html><title>Sign in</title><form action="/checkpoint/challenge/x" method="post">
        <input name="session_key" type="email"><input name="session_password" type="password"><button>Sign in</button></form>''',
    '/checkpoint/challenge/x': b'<!doctype html><title>Check your app</title><p>Open your app to approve this sign-in.</p>',
    # LinkedIn's way from a new device: the password, then a code it emails, on a checkpoint page of its own
    '/li/login': b'''<!doctype html><title>LinkedIn Login</title><form action="/checkpoint/challenge/pin" method="post">
        <input id="username" name="session_key" type="text" autocomplete="username"><input id="password" name="session_password" type="password">
        <button type="submit">Sign in</button></form>''',
    '/checkpoint/challenge/pin': '''<!doctype html><meta charset="utf-8"><title>Security Verification</title><meta property="og:site_name" content="LinkedIn">
        <main><h1>Let’s do a quick security check</h1><form id="email-pin-challenge" action="/feed" method="post">
        <p>The verification code has been sent to j•••@example.com.</p>
        <label for="input__email_verification_pin">Enter code</label><input id="input__email_verification_pin" name="pin" type="text" maxlength="6">
        <button type="button" id="resend">Resend code</button><button type="submit" id="email-pin-submit-button">Submit</button></form></main>'''.encode(),
    '/feed': b'<!doctype html><title>Feed</title><p>Home</p>',
    # the code taken, and then the sign-in again from the start: the site stopped it
    '/checkpoint/challenge/stop': '''<!doctype html><meta charset="utf-8"><title>Security Verification</title><form action="/li/login" method="post">
        <p>The verification code has been sent to j•••@example.com.</p><input name="pin" id="input__email_verification_pin" maxlength="6">
        <button type="submit">Submit</button></form>'''.encode(),
    # a robot check after the password: nothing to type, a challenge frame on a checkpoint address
    '/li/robot': b'''<!doctype html><title>LinkedIn Login</title><form action="/checkpoint/challenge/robot" method="post">
        <input name="session_key" type="email"><input name="session_password" type="password"><button>Sign in</button></form>''',
    '/checkpoint/challenge/robot': b'<!doctype html><title>Security Verification</title><iframe src="/captcha-frame" width="300" height="200"></iframe>',
}


class Site(http.server.BaseHTTPRequestHandler):
    posted = []

    def do_GET(self):
        self.reply()

    def do_POST(self):
        Site.posted.append((self.path, self.rfile.read(int(self.headers['Content-Length'])).decode()))
        self.reply()

    def reply(self):
        body = PAGES.get(self.path.split('?')[0], b'')
        self.send_response(200 if body else 404)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass


def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


CHROME = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome-stable') or shutil.which('chromium-browser')


@unittest.skipUnless(CHROME, 'needs Chrome or Chromium')
class FillTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Site)
        threading.Thread(target=cls.site.serve_forever, daemon=True).start()
        cls.origin = 'http://127.0.0.1:%d' % cls.site.server_address[1]
        cls.profile = tempfile.mkdtemp()
        port = free_port()
        cls.chrome = subprocess.Popen([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--remote-debugging-port=%d' % port,
                                       '--user-data-dir=' + cls.profile, 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cls.config = {'browser_cdp_url': 'http://127.0.0.1:%d' % port, 'accounts': []}
        for _ in range(600):  # a first start on macOS waits for the app check
            try:
                urllib.request.urlopen(cls.config['browser_cdp_url'] + '/json/version', timeout=1)
                break
            except OSError:
                time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.chrome.terminate()
        cls.chrome.wait()
        cls.site.shutdown()
        shutil.rmtree(cls.profile, ignore_errors=True)

    def open(self, path):
        base = self.config['browser_cdp_url']
        for tab in browser_login.browser_cdp._http(base, '/json/list'):
            if tab.get('type') == 'page':
                browser_login.browser_cdp.close_tab(base, tab['id'])
        browser_login.browser_cdp.open_tab(base, self.origin + path)
        time.sleep(1)

    def test_fills_submits_and_takes_the_code_next(self):
        Site.posted.clear()
        self.open('/news')  # not a sign-in page: not offered
        self.assertEqual(browser_login.pages(self.config), [])
        self.open('/login')
        other = {**self.config, 'accounts': [{'id': 'li-2', 'browser_cdp': 'http://127.0.0.1:%d' % free_port()}]}
        self.assertEqual(browser_login.pages(other, account='li-2'), [])  # only that account's own browser
        self.assertEqual(len(browser_login.pages(other)), 1)
        [page] = browser_login.pages(self.config)
        self.assertEqual((page['username'], page['password'], page['code']), (True, True, False))
        self.assertNotIn(SECRET, json.dumps(page))
        done = browser_login.fill(self.config, page['id'], page['host'], USER, SECRET, settle=5)
        self.assertEqual(done['result'], 'next')
        self.assertTrue(done['page']['code'])
        self.assertIn(('/after', 'email=test-user%40example.invalid&pw=not-a-real-password-123'), Site.posted)
        done = browser_login.fill(self.config, page['id'], page['host'], code=CODE, settle=5)
        self.assertEqual(done, {'result': 'done', 'page': None})
        self.assertIn(('/home', 'otp=' + CODE), Site.posted)

    def test_approving_in_the_sites_app_is_waited_on_not_called_done(self):
        self.open('/applogin')
        [page] = browser_login.pages(self.config)
        done = browser_login.fill(self.config, page['id'], page['host'], USER, SECRET, settle=5)
        self.assertEqual(done['result'], 'approve')
        self.assertEqual(done['page']['id'], page['id'])
        self.assertEqual(browser_login.watch(self.config, page['id']), {'state': 'waiting'})
        base, target = self.config['browser_cdp_url'], page['id'].split(':', 1)[1]
        browser_login.browser_cdp.navigate(base, target, self.origin + '/home')  # approved on the phone: the site moves on
        time.sleep(1)
        self.assertEqual(browser_login.watch(self.config, page['id']), {'state': 'done'})
        browser_login.browser_cdp.navigate(base, target, self.origin + '/login')
        time.sleep(1)
        self.assertEqual(browser_login.watch(self.config, page['id'])['state'], 'form')
        with self.assertRaises(ValueError):
            browser_login.watch(self.config, '0:gone')

    def test_a_page_that_stays_gets_its_password_emptied(self):
        self.open('/stuck')
        [page] = browser_login.pages(self.config)
        done = browser_login.fill(self.config, page['id'], page['host'], USER, SECRET, settle=2)
        self.assertEqual(done['result'], 'still_here')
        value = browser_login.browser_cdp.evaluate(self.config['browser_cdp_url'], page['id'].split(':', 1)[1],
                                                   "() => document.querySelector('input[type=password]').value")
        self.assertEqual(value, '')

    def test_another_site_is_refused_without_quoting_anything(self):
        self.open('/login')
        [page] = browser_login.pages(self.config)
        with self.assertRaises(ValueError) as caught:
            browser_login.fill(self.config, page['id'], 'evil.example', USER, SECRET)
        self.assertNotIn(SECRET, str(caught.exception))
        with self.assertRaises(ValueError):
            browser_login.fill(self.config, '7:nope', page['host'], USER, SECRET)


    def test_says_which_code_the_page_wants(self):
        for path, kind, sent in (('/sms', 'sms', 'ending in 12'), ('/totp', 'app', ''), ('/email', 'email', 'j\u2022\u2022\u2022@example.com'),
                                 ('/unknown', 'unknown', '')):
            self.open(path)
            [page] = browser_login.pages(self.config)
            self.assertEqual((page['code'], page['code_kind'], page['sent_to']), (True, kind, sent), path)
            self.assertNotIn('field', page)
        self.open('/sms')
        [page] = browser_login.pages(self.config)
        self.assertEqual(page['brand'], 'Stripe')
        self.assertEqual(page['ask'], 'Two-step authentication \u00b7 Enter the code we sent to \u2022\u2022\u2022\u2022 12 .')
        # Its own ways to another method or a new code, on this site only; never Sign out or a submit button.
        self.assertEqual(page['others'], ['Resend code', 'Use authenticator app instead'])
        self.assertEqual(page['error'], '')

    def test_another_method_is_a_click_in_the_page(self):
        self.open('/sms')
        [page] = browser_login.pages(self.config)
        done = browser_login.choose(self.config, page['id'], page['host'], 'Use authenticator app instead', settle=1)
        self.assertEqual((done['result'], done['page']['code_kind']), ('next', 'app'))
        with self.assertRaises(ValueError):
            browser_login.choose(self.config, page['id'], page['host'], 'Sign out', settle=0)
        with self.assertRaises(ValueError):  # another site
            browser_login.choose(self.config, page['id'], 'evil.example', 'Text me a code instead', settle=0)

    def test_a_rejected_code_shows_the_sites_words(self):
        Site.posted.clear()
        self.open('/sms')
        [page] = browser_login.pages(self.config)
        done = browser_login.fill(self.config, page['id'], page['host'], code='000000', settle=3)
        self.assertEqual(done['result'], 'next')
        self.assertEqual(done['page']['error'], "That code isn't right. Try again.")
        self.assertNotIn('000000', json.dumps(done))
        self.assertNotIn("isn't right", done['page']['ask'])


    def test_linkedins_emailed_code_signs_in_while_a_reader_looks_in_another_tab(self):
        # The connect looks in a tab of its own while the owner signs in. It opens behind: the sign-in tab stays in
        # front (no flicker in the viewer, the typing stays in it) and the code goes into the page that asked for it.
        Site.posted.clear()
        self.open('/li/login')
        base = self.config['browser_cdp_url']
        [page] = browser_login.pages(self.config)
        done = browser_login.fill(self.config, page['id'], page['host'], USER, SECRET, settle=5)
        self.assertEqual(done['result'], 'next')
        self.assertEqual((done['page']['code'], done['page']['code_kind'], done['page']['sent_to'], done['page']['brand']),
                         (True, 'email', 'j•••@example.com', 'LinkedIn'))
        target = page['id'].split(':', 1)[1]
        reader = browser_login.browser_cdp.open_background_tab(base, 'about:blank#reader')
        try:
            self.assertNotEqual(reader, target)
            self.assertEqual(browser_login.browser_cdp.evaluate(base, target, '() => document.visibilityState'), 'visible')
            done = browser_login.fill(self.config, page['id'], page['host'], code=CODE, settle=5)
        finally:
            browser_login.browser_cdp.close_tab(base, reader)
        self.assertEqual(done, {'result': 'done', 'page': None})
        self.assertIn(('/feed', 'pin=' + CODE), Site.posted)  # its Submit, not Resend code

    def test_the_site_stopping_the_sign_in_or_a_robot_check_is_said_so(self):
        self.open('/checkpoint/challenge/stop')
        [page] = browser_login.pages(self.config)
        done = browser_login.fill(self.config, page['id'], page['host'], code=CODE, settle=5)
        self.assertEqual(done['result'], 'blocked')  # back to the username and password: the dialog says so, with the form
        self.assertTrue(done['page']['password'])
        self.open('/li/robot')
        [page] = browser_login.pages(self.config)
        done = browser_login.fill(self.config, page['id'], page['host'], USER, SECRET, settle=5)
        self.assertEqual(done['result'], 'captcha')
        self.assertEqual(browser_login.watch(self.config, page['id']), {'state': 'captcha'})
        self.open('/checkpoint/challenge/x')  # approving in the app: no frame, still waited on
        tab = [t for t in browser_login.browser_cdp._http(self.config['browser_cdp_url'], '/json/list') if t.get('type') == 'page'][0]
        self.assertEqual(browser_login.watch(self.config, '0:' + tab['id']), {'state': 'waiting'})

    def test_a_tab_opened_from_the_json_endpoint_takes_the_front_a_background_one_does_not(self):
        self.open('/news')
        base = self.config['browser_cdp_url']
        [front] = [t['id'] for t in browser_login.browser_cdp._http(base, '/json/list') if t.get('type') == 'page']
        shown = lambda: browser_login.browser_cdp.evaluate(base, front, '() => document.visibilityState')
        behind = browser_login.browser_cdp.open_background_tab(base, 'about:blank')
        self.assertEqual(shown(), 'visible')
        browser_login.browser_cdp.close_tab(base, behind)
        ahead = browser_login.browser_cdp.open_tab(base, 'about:blank')  # what readers did: the owner's page went behind
        self.assertEqual(shown(), 'hidden')
        browser_login.browser_cdp.close_tab(base, ahead)


class CodeKindTest(unittest.TestCase):
    def test_by_what_the_page_says(self):
        cases = {
            'Enter the code we sent to \u2022\u2022\u2022\u2022 12': ('sms', 'ending in 12'),
            'We texted a 6-digit code to (***) ***-**34': ('sms', 'ending in 34'),
            'We sent a code to the phone number ending in 4821': ('sms', 'ending in 4821'),
            'We sent a code to your phone': ('sms', ''),
            'Enter the code from the authenticator app on your phone': ('app', ''),
            'Open Google Authenticator and enter the code': ('app', ''),
            'Check your email \u00b7 We sent a code to j\u2022\u2022\u2022@example.com': ('email', 'j\u2022\u2022\u2022@example.com'),
            'Enter the code. Questions? support@example.com': ('unknown', ''),
            'Insert your security key': ('key', ''),
            'Enter the 6-digit code': ('unknown', ''),
        }
        for ask, (kind, sent) in cases.items():
            self.assertEqual(browser_login.code_kind(ask), kind, ask)
            self.assertEqual(browser_login.sent_to(ask, kind), sent, ask)
        self.assertEqual(browser_login.code_kind('Enter the code', 'sms_code', ''), 'sms')  # then the field and the step
        self.assertEqual(browser_login.code_kind('Enter the code', 'otp', '/login/totp'), 'app')

    def test_brand(self):
        self.assertEqual([browser_login.brand(h) for h in ('dashboard.stripe.com', 'shop.example.co.uk', '127.0.0.1:8000')],
                         ['Stripe', 'Example', '127.0.0.1'])
        self.assertEqual(browser_login.brand('x.example.com', 'Example Pay'), 'Example Pay')


class EndpointTest(unittest.TestCase):
    def test_loopback_browsers_only(self):
        config = {'browser_cdp_url': 'http://127.0.0.1:9222', 'accounts': [{'browser_cdp': 'http://127.0.0.1:9333'},
                  {'browser_cdp': 'http://10.0.0.5:9222'}, {'browser_cdp': 'http://127.0.0.1:9222/'}, {}]}
        self.assertEqual(browser_login.endpoints(config), ['http://127.0.0.1:9222', 'http://127.0.0.1:9333'])


@unittest.skipUnless(shutil.which('openssl'), 'needs openssl')
class StoreTest(unittest.TestCase):
    def test_saved_encrypted_listed_without_password_and_forgotten(self):
        with tempfile.TemporaryDirectory() as folder:
            store = browser_login.LoginStore(folder)
            store.save('www.example.invalid', USER, None)  # a two-step sign-in: the username first
            store.save('example.invalid', None, SECRET)
            self.assertEqual(store.get('example.invalid')['password'], SECRET)
            self.assertNotIn(SECRET.encode(), (Path(folder) / browser_login.STORE).read_bytes())
            self.assertNotIn(USER.encode(), (Path(folder) / browser_login.STORE).read_bytes())
            for name in (browser_login.STORE, browser_login.KEY):
                self.assertEqual(os.stat(Path(folder) / name).st_mode & 0o777, 0o600)
            [entry] = store.list()
            self.assertEqual((entry['site'], entry['username']), ('example.invalid', USER))
            self.assertNotIn('password', entry)
            self.assertIs(entry['password_saved'], True)
            self.assertNotIn(SECRET, json.dumps(store.list()))
            store.save('other.invalid', USER, None)  # a username only: says so
            self.assertIs([e for e in store.list() if e['site'] == 'other.invalid'][0]['password_saved'], False)
            store.forget('other.invalid')
            self.assertTrue(store.forget('example.invalid'))
            self.assertEqual(store.list(), [])

    def test_moves_only_with_a_passphrase(self):
        self.assertTrue({browser_login.SEALED, browser_login.STORE, browser_login.KEY} <= moving.SECRET_NAMES)


def message_key(folder):
    import base64, secrets as random
    path = Path(folder) / browser_login.message_seal.KEY_NAME
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as handle:
        handle.write(base64.b64encode(random.token_bytes(32)).decode() + '\n')
    return path


class SealedStoreTest(unittest.TestCase):
    """With a message key, saved sign-ins are sealed with it and no key of their own is ever on the disk."""

    def test_sealed_with_the_message_key_and_no_key_of_their_own(self):
        with tempfile.TemporaryDirectory() as folder:
            message_key(folder)
            store = browser_login.LoginStore(folder)
            store.save('example.invalid', USER, SECRET)
            sealed = (Path(folder) / browser_login.SEALED).read_bytes()
            self.assertTrue(browser_login.message_seal.is_sealed_bytes(sealed))
            self.assertNotIn(SECRET.encode(), sealed)
            self.assertNotIn(USER.encode(), sealed)
            self.assertEqual(os.stat(Path(folder) / browser_login.SEALED).st_mode & 0o777, 0o600)
            self.assertFalse((Path(folder) / browser_login.KEY).exists())
            self.assertFalse((Path(folder) / browser_login.STORE).exists())
            self.assertEqual(browser_login.LoginStore(folder).get('www.example.invalid')['password'], SECRET)
            self.assertEqual([e['site'] for e in store.list()], ['example.invalid'])
            self.assertTrue(store.forget('example.invalid'))
            self.assertEqual(store.list(), [])

    @unittest.skipUnless(shutil.which('openssl'), 'needs openssl')
    def test_older_store_moves_over_and_its_key_is_gone(self):
        with tempfile.TemporaryDirectory() as folder:
            browser_login.LoginStore(folder).save('example.invalid', USER, SECRET)  # no message key: a key of its own
            self.assertTrue((Path(folder) / browser_login.KEY).exists())
            message_key(folder)
            store = browser_login.LoginStore(folder)
            self.assertTrue(store.migrate())
            self.assertFalse(store.migrate())
            for name in (browser_login.KEY, browser_login.STORE):
                self.assertFalse((Path(folder) / name).exists(), name)
            self.assertTrue(browser_login.message_seal.is_sealed_file(Path(folder) / browser_login.SEALED))
            saved = store.get('example.invalid')
            self.assertEqual((saved['username'], saved['password']), (USER, SECRET))

    def test_a_hosted_key_not_here_yet_is_waited_for_never_replaced(self):
        with tempfile.TemporaryDirectory() as folder, tempfile.TemporaryDirectory() as memory:
            held = Path(memory) / browser_login.message_seal.KEY_NAME
            (Path(folder) / browser_login.message_seal.KEY_NAME).symlink_to(held)
            store = browser_login.LoginStore(folder)
            with self.assertRaisesRegex(ValueError, 'wait'):
                store.save('example.invalid', USER, SECRET)
            self.assertEqual(sorted(p.name for p in Path(folder).iterdir()), [browser_login.message_seal.KEY_NAME])
            self.assertEqual(store.list(), [])
            message_key(memory)  # the hosting puts it in memory
            store.save('example.invalid', USER, SECRET)
            os.unlink(held)  # a restart empties memory: sealed sign-ins wait, nothing is quoted
            with self.assertRaises(ValueError) as caught:
                store.get('example.invalid')
            self.assertIn('not here yet', str(caught.exception))
            self.assertNotIn(SECRET, str(caught.exception))

    def test_an_imported_plain_store_is_sealed_at_the_next_start(self):
        with tempfile.TemporaryDirectory() as folder:
            message_key(folder)
            (Path(folder) / browser_login.SEALED).write_text(json.dumps({'example.invalid': {'username': USER, 'password': SECRET}}))
            self.assertTrue(browser_login.LoginStore(folder).migrate())
            self.assertNotIn(SECRET.encode(), (Path(folder) / browser_login.SEALED).read_bytes())
            self.assertEqual(browser_login.LoginStore(folder).get('example.invalid')['password'], SECRET)

    def test_an_export_holds_them_opened_inside_its_encryption(self):
        with tempfile.TemporaryDirectory() as folder:
            message_key(folder)
            browser_login.LoginStore(folder).save('example.invalid', USER, SECRET)
            opened = moving._open_file(Path(folder) / browser_login.SEALED, {'database': str(Path(folder) / 'events.sqlite')})
            self.assertEqual(json.loads(opened)['example.invalid']['password'], SECRET)


@unittest.skipUnless(shutil.which('openssl'), 'needs openssl')
class ListActionTest(unittest.TestCase):
    def test_the_dashboard_list_has_no_password_value_or_length(self):
        import assistant
        with tempfile.TemporaryDirectory() as folder:
            browser_login.LoginStore(folder).save('example.invalid', USER, SECRET)
            app = assistant.App.__new__(assistant.App)
            app.config = {'accounts': [], 'database': str(Path(folder) / 'events.sqlite')}
            sent = app.action('browser_logins', {}, owner_dashboard=True)
            self.assertEqual(sent['logins'], [{'site': 'example.invalid', 'username': USER, 'password_saved': True,
                                              'saved_at': sent['logins'][0]['saved_at']}])
            self.assertNotIn(SECRET, json.dumps(sent))


class OwnerOnlyTest(unittest.TestCase):
    def test_not_for_the_agent_or_the_cli(self):
        import assistant
        for name in ('browser_login_pages', 'browser_login_fill', 'browser_login_choose', 'browser_logins', 'browser_login_forget'):
            self.assertIn(name, assistant.OWNER_ACTIONS)
            app = assistant.App.__new__(assistant.App)
            app.config = {'accounts': [], 'database': '/nonexistent/x.db'}
            with self.assertRaisesRegex(ValueError, 'Only the owner'):
                app.action(name, {'page': '0:x', 'host': 'example.invalid', 'password': SECRET})


if __name__ == '__main__':
    unittest.main()
