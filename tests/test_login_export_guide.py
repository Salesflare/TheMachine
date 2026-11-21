"""The export page's guide (login_export_guide.py) in a real headless browser, on made-up pages that look like LastPass's
vault, Bitwarden's web vault and Google Password Manager's settings when signed in: the script clicks on to the export
step and stops at the master password, the owner's part (played here by the test) brings the download, which is read
once and deleted; a page that changed gets the manual steps; nothing from the page reaches an answer or a log. Fake data
only, never a real password manager. The browser runs cut off from the desktop (no display, no session bus, its own
XDG folders, stub openers first on PATH), as tests/browser.mjs does for the JavaScript tests."""
import base64, http.server, io, json, logging, os, shutil, socket, subprocess, tempfile, threading, time, unittest, urllib.request
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import browser_login
import login_export_guide
import login_import

ON_PAGE = 'FIXTURE-VAULT-ITEM-Q7xz'  # shown on every fixture page: must never leave it
MASTER = 'fake-master-pass-55Lp'  # what the owner types (the test plays the owner): never read by the guide
PASS = 'fake-site-pass-80Wq'  # in the exported file

SAVE = '''<script>function save(name, text) { const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([text], {type: 'text/plain'})); a.download = name; document.body.append(a); a.click(); }</script>'''
LASTPASS_CSV = 'url,username,password,totp,extra,name,grouping,fav\\nhttps://shop.example.invalid,sam@example.invalid,' + PASS + ',,,Shop,,0\\n'
BITWARDEN_JSON = json.dumps({'encrypted': False, 'items': [{'type': 1, 'name': 'Shop', 'login': {
    'username': 'sam@example.invalid', 'password': PASS, 'uris': [{'uri': 'https://shop.example.invalid'}]}}]}).replace('"', '&quot;')
GOOGLE_CSV = 'name,url,username,password\\nShop,https://shop.example.invalid,sam@example.invalid,' + PASS + '\\n'

PAGES = {
    # LastPass: a sign-in, then the vault with Advanced Options folded, Export under it, and the master password asked
    # (a card like the real page's: email, master password and Log in stacked, so the phone's zoom has the whole form)
    '/lp/login': '''<!doctype html><meta charset="utf-8"><title>Log in</title><style>body{margin:0;font:15px sans-serif;background:#f3f4f6;color:#1f2937}
        form{width:340px;margin:48px auto;padding:24px;background:#fff;border-radius:8px;box-shadow:0 1px 4px #0002;display:grid;gap:6px}
        h1{margin:0 0 10px;font-size:22px}label{font-weight:600;margin-top:6px}input{font:inherit;padding:9px 10px;border:1px solid #9ca3af;border-radius:4px}
        button{margin-top:14px;padding:11px;font:inherit;font-weight:600;color:#fff;background:#d32d27;border:0;border-radius:4px}</style>
        <form onsubmit="event.preventDefault(); location = '/lp/vault/'"><h1>Log in</h1>
        <label for="email">Email</label><input type="email" id="email"><label for="pw">Master password</label><input type="password" id="pw">
        <button>Log in</button></form>''',
    '/lp/vault/': '<!doctype html><meta charset="utf-8"><title>Vault</title>' + SAVE + '''
        <nav><a href="#">All items</a><button type="button" onclick="document.getElementById('more').hidden = false"><svg width="8" height="8"></svg><span>Advanced Options</span></button>
        <ul id="more" hidden><li><button type="button" onclick="document.getElementById('dlg').showModal()">Export</button></li><li><button type="button">Import</button></li></ul></nav>
        <main><h1>All items</h1><p>''' + ON_PAGE + '''</p></main>
        <dialog id="dlg"><form method="dialog" onsubmit="save('lastpass_export.csv', \'''' + LASTPASS_CSV + '''\')">
        <p>Please re-enter your master password.</p><input type="password" id="mp"><button>Submit</button></form></dialog>''',
    # LastPass's newer vault on its own address: signed out it asks the email first (no password field yet), then the
    # master password; signed in, a narrow window folds the left navigation behind Menu, with Advanced options in it
    # LastPass signing in on one tab and opening the vault in another, whose left navigation is plain divs with click
    # handlers (no button, no role), their words split over pieces of text
    '/lp/login5': '''<!doctype html><meta charset="utf-8"><title>LastPass - Sign in</title><form id="f" onsubmit="event.preventDefault()">
        <input type="email"><input type="password" id="pw"><button>Log in</button></form>''',
    '/lp/vault4/': '<!doctype html><meta charset="utf-8"><title>My LastPass Vault</title>' + SAVE + '''<style>.it{cursor:pointer;padding:6px}</style>
        <aside><div class="it">All items</div><div class="it" onclick="document.getElementById('more').hidden = false"><i></i><span>Advanced</span> <span>options</span></div>
        <div id="more" hidden><h4>Manage your vault</h4><div class="it" onclick="document.getElementById('dlg').showModal()"><span>Export</span></div></div></aside>
        <main><p>''' + ON_PAGE + '''</p></main><dialog id="dlg"><form method="dialog" onsubmit="save('lastpass_vault_export.csv', \'''' + LASTPASS_CSV + '''\')">
        <p>Enter your master password.</p><input type="password" id="mp"><button>Continue</button></form></dialog>''',
    '/lp/vault3/': '<!doctype html><meta charset="utf-8"><title>Vault</title>' + SAVE + '''<div id="app"></div>
        <dialog id="dlg"><form method="dialog" onsubmit="save('lastpass_vault_export.csv', \'''' + LASTPASS_CSV + '''\')">
        <p>Enter your master password to continue.</p><input type="password" id="mp"><button>Continue</button></form></dialog><script>
        function render() { const app = document.getElementById('app');
          if (!sessionStorage.email) app.innerHTML = '<form id="f"><label>Email<input type="email" autocomplete="username"></label><button>Continue</button></form>';
          else if (!sessionStorage.in) app.innerHTML = '<form id="f"><label>Master password<input type="password" id="pw"></label><button>Log in</button></form>';
          else app.innerHTML = '<header><button type="button" aria-label="Open menu" id="m">=</button></header><nav id="nav" hidden><a href="#">Passwords</a>' +
            '<button type="button" id="adv">Advanced options</button><ul id="more" hidden><li><button type="button" id="ex">Export</button></li></ul></nav><p>''' + ON_PAGE + '''</p>';
          const f = document.getElementById('f'), m = document.getElementById('m');
          if (f) f.onsubmit = (e) => { e.preventDefault(); if (sessionStorage.email) sessionStorage.in = 1; else sessionStorage.email = 1; render(); };
          if (m) { m.onclick = () => { document.getElementById('nav').hidden = false; };
            document.getElementById('adv').onclick = () => { document.getElementById('more').hidden = false; };
            document.getElementById('ex').onclick = () => document.getElementById('dlg').showModal(); } }
        render();</script>''',
    # The vault's left navigation inside a frame: the same origin's (vault6, a frame placed off the corner) or another
    # origin's (vault8, the frame's address in ?f=: another port is another origin in the tab's own process, localhost
    # another site in a process of its own), whose Export asks the vault around it for the master password
    '/lp/vault6/': '<!doctype html><meta charset="utf-8"><title>Vault</title>' + SAVE + '''<p>''' + ON_PAGE + '''</p>
        <iframe src="/lp/nav6" style="position:absolute;left:140px;top:90px;width:260px;height:200px;border:3px solid #ccc"></iframe>
        <dialog id="dlg"><form method="dialog" onsubmit="save('lastpass_vault_export.csv', \'''' + LASTPASS_CSV + '''\')">
        <p>Enter your master password.</p><input type="password" id="mp"><button>Continue</button></form></dialog>''',
    '/lp/nav6': '''<!doctype html><meta charset="utf-8"><nav><a href="#">Passwords</a><button type="button" onclick="document.getElementById('more').hidden = false">
        Advanced options</button><ul id="more" hidden><li><button type="button" onclick="parent.document.getElementById('dlg').showModal()">Export</button></li></ul></nav>''',
    '/lp/vault8/': '<!doctype html><meta charset="utf-8"><title>Vault</title>' + SAVE + '''<p>''' + ON_PAGE + '''</p>
        <iframe id="nav" style="position:absolute;left:180px;top:120px;width:260px;height:200px;border:0"></iframe>
        <dialog id="dlg"><form method="dialog" onsubmit="save('lastpass_vault_export.csv', \'''' + LASTPASS_CSV + '''\')">
        <p>Enter your master password.</p><input type="password" id="mp"><button>Continue</button></form></dialog><script>
        document.getElementById('nav').src = new URLSearchParams(location.search).get('f');
        addEventListener('message', (e) => { if (e.data === 'export') document.getElementById('dlg').showModal(); });</script>''',
    '/lp/nav8': '''<!doctype html><meta charset="utf-8"><div style="height:60px"></div><nav><button type="button" onclick="document.getElementById('more').hidden = false">
        Advanced options</button><ul id="more" hidden><li><button type="button" onclick="parent.postMessage('export', '*')">Export</button></li></ul></nav>''',
    # The vault's navigation as web components, one inside the other (open shadow roots): Advanced options drawn by
    # the style sheet only, Export an icon with a title only
    '/lp/vault7/': '<!doctype html><meta charset="utf-8"><title>Vault</title>' + SAVE + '''<lp-app></lp-app><p>''' + ON_PAGE + '''</p>
        <dialog id="dlg"><form method="dialog" onsubmit="save('lastpass_vault_export.csv', \'''' + LASTPASS_CSV + '''\')">
        <p>Enter your master password.</p><input type="password" id="mp"><button>Continue</button></form></dialog><script>
        customElements.define('lp-nav', class extends HTMLElement { connectedCallback() { const r = this.attachShadow({mode: 'open'});
          r.innerHTML = '<style>.adv::before{content:"Advanced options"}.adv{cursor:pointer;padding:6px}</style><div role="navigation">' +
            '<div class="adv"></div><div id="more" hidden><span title="Export" style="display:inline-block;width:20px;height:20px;cursor:pointer"></span></div></div>';
          r.querySelector('.adv').onclick = () => { r.getElementById('more').hidden = false; };
          r.querySelector('[title]').onclick = () => document.getElementById('dlg').showModal(); } });
        customElements.define('lp-app', class extends HTMLElement { connectedCallback() {
          this.attachShadow({mode: 'open'}).innerHTML = '<section style="margin:40px 0 0 60px"><lp-nav></lp-nav></section>'; } });</script>''',
    # the same vault after a redesign: nothing the recipe knows
    '/lp/vault2/': '<!doctype html><meta charset="utf-8"><title>Vault</title><nav><button type="button">More tools</button></nav><p>' + ON_PAGE + '</p>',
    # Bitwarden: one page with hash routes; signed out it goes to #/login, signed in to #/vault (not the export)
    '/bw/': '<!doctype html><meta charset="utf-8"><title>Bitwarden</title>' + SAVE + '''<div id="app"></div>
        <dialog id="dlg"><form method="dialog" onsubmit="save('bitwarden_export.json', \'''' + BITWARDEN_JSON + '''\')"><h2>Confirm vault export</h2>
        <input type="password" id="mp"><button>Export vault</button></form></dialog><script>
        function render() { const h = location.hash, app = document.getElementById('app');
          if (!sessionStorage.in && !h.startsWith('#/login')) { location.hash = '#/login'; return; }
          if (h.startsWith('#/login')) app.innerHTML = '<form id="f"><input type="email"><input type="password"><button>Log in with master password</button></form>';
          else if (h.startsWith('#/tools/export')) app.innerHTML = '<tools-export><form id="x"><select id="format"><option value="json">.json</option></select><button type="submit">Export vault</button></form></tools-export>';
          else app.innerHTML = '<nav><a href="#/vault">Vaults</a><a href="#/sends">Send</a></nav><p>''' + ON_PAGE + '''</p>';
          const f = document.getElementById('f'), x = document.getElementById('x');
          if (f) f.onsubmit = (e) => { e.preventDefault(); sessionStorage.in = 1; location.hash = '#/vault'; };
          if (x) x.onsubmit = (e) => { e.preventDefault(); document.getElementById('dlg').showModal(); }; }
        addEventListener('hashchange', render); render();</script>''',
    # Google Password Manager: its settings, with Download file under Export passwords, and Google asking it's you
    '/gpm/options': '<!doctype html><meta charset="utf-8"><title>Settings</title>' + SAVE + '''
        <div jsaction="click:row"><div><div>Export passwords</div><div>Download a copy of your passwords</div></div>
        <button type="button" onclick="location = '/gacc/signin?next=/gpm/options%3Fgo%3D1'"><span>Download file</span></button></div><p>''' + ON_PAGE + '''</p>
        <script>if (location.search.includes('go=1')) save('Google Passwords.csv', \'''' + GOOGLE_CSV + '''\');</script>''',
    '/gacc/signin': '''<!doctype html><meta charset="utf-8"><title>Sign in</title><h1>Verify it's you</h1>
        <form onsubmit="event.preventDefault(); location = new URLSearchParams(location.search).get('next')"><input type="password" id="mp"><button>Next</button></form>''',
}

RECIPES = {
    'lastpass': {**login_export_guide.RECIPES['lastpass'], 'signin': r'/lp/login', 'vault': r'^http://127\.0\.0\.1:\d+/lp/vault'},
    'bitwarden': {**login_export_guide.RECIPES['bitwarden'], 'signin': r'/bw/#/(login|2fa|lock)', 'vault': r'^http://127\.0\.0\.1:\d+/bw/#/'},
    'chrome': {**login_export_guide.RECIPES['chrome'], 'signin': r'/gacc/', 'vault': r'^http://127\.0\.0\.1:\d+/gpm/',
               'at': r'/gpm/options', 'go': '/gpm/options'},
}


class Site(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = PAGES.get(self.path.split('?')[0], '').encode()
        self.send_response(200 if body else 404)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass


def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def fenced_env(fence):
    """The caller's environment cut off from the desktop, so a page can never open an app (see tests/browser.mjs)."""
    env = {k: v for k, v in os.environ.items() if k not in ('DISPLAY', 'WAYLAND_DISPLAY', 'WAYLAND_SOCKET', 'DBUS_SYSTEM_BUS_ADDRESS')}
    stubs = fence / 'bin'
    for folder in (stubs, fence / 'run', fence / 'config', fence / 'data'):
        folder.mkdir(mode=0o700, parents=True)
    for name in ('xdg-open', 'xdg-email', 'gio', 'kde-open', 'gnome-open', 'sensible-browser'):
        (stubs / name).write_text('#!/bin/sh\nexit 0\n')
        (stubs / name).chmod(0o755)
    env.update({'PATH': str(stubs) + os.pathsep + env.get('PATH', ''), 'BROWSER': str(stubs / 'xdg-open'),
                'DBUS_SESSION_BUS_ADDRESS': 'unix:path=' + str(fence / 'no-bus'), 'XDG_RUNTIME_DIR': str(fence / 'run'),
                'XDG_CONFIG_HOME': str(fence / 'config'), 'XDG_DATA_HOME': str(fence / 'data'), 'XDG_DATA_DIRS': str(fence / 'data')})
    return env


CHROME = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome-stable') or shutil.which('chromium-browser')


@unittest.skipUnless(CHROME, 'needs Chrome or Chromium')
class GuideTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Site)
        threading.Thread(target=cls.site.serve_forever, daemon=True).start()
        cls.origin = 'http://127.0.0.1:%d' % cls.site.server_address[1]
        cls.other = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Site)  # another origin, for frames
        threading.Thread(target=cls.other.serve_forever, daemon=True).start()
        cls.temp = Path(tempfile.mkdtemp())
        port = free_port()
        cls.chrome = subprocess.Popen([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--remote-debugging-port=%d' % port,
                                       '--user-data-dir=' + str(cls.temp / 'profile'), 'about:blank'],
                                      env=fenced_env(cls.temp / 'fence'),
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cls.base = 'http://127.0.0.1:%d' % port
        for _ in range(600):
            try:
                urllib.request.urlopen(cls.base + '/json/version', timeout=1)
                break
            except OSError:
                time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.chrome.terminate()
        cls.chrome.wait()
        cls.site.shutdown()
        cls.other.shutdown()
        shutil.rmtree(cls.temp, ignore_errors=True)

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name)
        key = self.folder / browser_login.message_seal.KEY_NAME
        key.write_text(base64.b64encode(os.urandom(32)).decode() + '\n')
        key.chmod(0o600)
        self.store = browser_login.LoginStore(self.folder)
        self.log, self.answers = io.StringIO(), []
        handler, root = logging.StreamHandler(self.log), logging.getLogger()
        handler.setLevel(logging.DEBUG)
        old = root.level
        root.addHandler(handler)
        root.setLevel(logging.DEBUG)
        self.addCleanup(lambda: (root.removeHandler(handler), root.setLevel(old)))
        for p in (patch.object(login_export_guide, 'RECIPES', RECIPES), patch.object(login_import, 'EXPORT_POLL', 0.3),
                  patch.object(login_export_guide, 'AGAIN', 1)):
            p.start()
            self.addCleanup(p.stop)

    def check(self, watch):
        got = login_import.export_check(watch)
        self.answers.append(got)
        return got

    def until(self, watch, want, seconds=20):
        """export_check until its step (or state) is `want`; fails on anything finished that isn't."""
        end, got = time.monotonic() + seconds, None
        while time.monotonic() < end:
            got = self.check(watch)
            if want in (got.get('step'), got['state']):
                return got
            self.assertEqual(got['state'], 'waiting', got)
            time.sleep(0.1)
        self.fail('never got to %s: %s' % (want, got))

    def owner(self, watch, script):
        """What the owner does on the page: sign in, type the master password. The test's own hands, not the guide."""
        tab = login_import._exports[watch]['tab']
        return browser_login.browser_cdp.evaluate(self.base, tab, script)

    def export(self, manager, page):
        out, err = io.StringIO(), io.StringIO()
        with patch.dict(login_import.EXPORT_PAGES, {manager: self.origin + page}), redirect_stdout(out), redirect_stderr(err):
            watch = login_import.export_open(self.base, manager, self.folder, self.store)['watch']
            yield watch
        for where, text in (('log', self.log.getvalue()), ('stdout', out.getvalue()), ('stderr', err.getvalue()),
                            ('answers', json.dumps(self.answers))):
            self.assertNotIn(ON_PAGE, text, where)
            self.assertNotIn(MASTER, text, where)
            self.assertNotIn(PASS, text, where)
        for got in self.answers:
            if got['state'] == 'waiting':
                self.assertEqual(set(got), {'state', 'step'})
        left = lambda: [p for p in self.folder.iterdir() if p.name.startswith('login-export-')]
        for _ in range(100):
            if not left():
                break
            time.sleep(0.05)
        self.assertEqual(left(), [], 'read once, then gone')

    def typed_master(self, watch):
        focused = self.owner(watch, '() => document.activeElement && document.activeElement.type')
        self.assertEqual(focused, 'password', 'the master password field is focused for the owner')
        self.assertEqual(self.owner(watch, '() => document.activeElement.value'), '', 'nothing typed into it')
        # where the owner types, for a phone's live view to zoom to: its place in the window, numbers only, around the field
        end = time.monotonic() + 5
        while not login_import.export_focus() and time.monotonic() < end:
            time.sleep(0.1)
        box = login_import.export_focus()
        self.assertEqual(set(box), {'x', 'y', 'w', 'h'}, box)
        self.assertTrue(all(isinstance(v, float) and 0 <= v <= 1 for v in box.values()), box)
        field = self.owner(watch, '() => { const b = document.activeElement.getBoundingClientRect(), W = outerWidth || innerWidth,'
                                  ' H = outerHeight || innerHeight, t = H - innerHeight; return [(b.left + b.width / 2) / W, (t + b.top + b.height / 2) / H]; }')
        self.assertTrue(box['x'] <= field[0] <= box['x'] + box['w'] and box['y'] <= field[1] <= box['y'] + box['h'], (box, field))
        return self.owner(watch, '() => { const f = document.activeElement; f.value = "' + MASTER + '"; f.form.requestSubmit(); return 1; }')

    def review(self, watch):
        end = time.monotonic() + 20
        while time.monotonic() < end:
            got = self.check(watch)
            if got['state'] != 'waiting':
                self.assertEqual(got['state'], 'review', got)
                self.assertEqual([(r['origin'], r['username']) for r in got['rows']], [('https://shop.example.invalid', 'sam@example.invalid')])
                return got
            time.sleep(0.1)
        self.fail('the download never came in')

    def test_lastpass_from_the_sign_in_through_advanced_options_to_the_master_password(self):
        for watch in self.export('lastpass', '/lp/login'):
            self.until(watch, 'signin')
            self.owner(watch, '() => { document.getElementById("pw").form.requestSubmit(); return 1; }')
            self.until(watch, 'password')
            self.typed_master(watch)
            self.review(watch)

    def test_bitwarden_from_its_vault_to_the_export_and_its_master_password(self):
        for watch in self.export('bitwarden', '/bw/#/tools/export'):
            self.until(watch, 'signin')
            self.owner(watch, '() => { document.getElementById("f").requestSubmit(); return 1; }')
            self.until(watch, 'password')
            self.typed_master(watch)
            self.review(watch)

    def test_google_password_manager_to_its_download_and_the_check_that_its_you(self):
        for watch in self.export('chrome', '/gpm/options'):
            self.until(watch, 'password')
            self.typed_master(watch)
            self.review(watch)

    def test_lastpass_opening_its_vault_in_another_tab_is_followed_there_and_its_plain_div_menu_clicked(self):
        cdp = browser_login.browser_cdp
        for watch in self.export('lastpass', '/lp/login5'):
            self.until(watch, 'signin')
            first = login_import._exports[watch]['tab']
            self.owner(watch, '() => { document.getElementById("f").requestSubmit(); return 1; }')
            cdp.open_tab(self.base, self.origin + '/lp/vault4/')  # what LastPass does on signing in
            self.until(watch, 'password')
            self.assertNotEqual(login_import._exports[watch]['tab'], first, 'follows the vault\'s tab')
            self.typed_master(watch)
            self.review(watch)
        open_now = {tab for tab, _ in cdp.pages(self.base)}
        self.assertNotIn(first, open_now, 'its tabs close with it')
        log = self.log.getvalue()
        self.assertIn('login export follows another tab manager=lastpass', log)
        self.assertIn('login export step manager=lastpass step=password', log)
        self.assertIn('login export guide manager=lastpass at=click step=1', log)
        self.assertNotIn('/lp/', log, 'no address in the log')

    def test_an_earlier_exports_tab_is_closed_when_the_next_starts(self):
        cdp = browser_login.browser_cdp
        for watch in self.export('lastpass', '/lp/login'):
            self.until(watch, 'signin')
            first = login_import._exports[watch]['tab']
            for again in self.export('lastpass', '/lp/login'):
                self.until(again, 'signin')
                self.assertNotIn(first, {tab for tab, _ in cdp.pages(self.base)}, 'no pile of export tabs')
                login_import.export_stop(again)

    def test_lastpass_asking_the_email_first_waits_on_the_owner_then_opens_the_folded_menu(self):
        with patch.object(login_export_guide, 'GIVE_UP', 1.5):  # the sign-in never counts toward giving up
            for watch in self.export('lastpass', '/lp/vault3/'):
                self.until(watch, 'signin')
                time.sleep(2.5)
                self.assertEqual(self.check(watch)['step'], 'signin', 'the email step is the owner\'s sign-in, not a page it doesn\'t know')
                self.owner(watch, '() => { document.getElementById("f").requestSubmit(); return 1; }')
                time.sleep(2.5)
                self.assertEqual(self.check(watch)['step'], 'signin')
                self.owner(watch, '() => { document.getElementById("pw").form.requestSubmit(); return 1; }')
                self.until(watch, 'password')
                self.typed_master(watch)
                self.review(watch)

    def signed_in_through(self, page):
        for watch in self.export('lastpass', page):
            self.until(watch, 'password')
            self.typed_master(watch)
            self.review(watch)
        return self.log.getvalue()

    def test_lastpass_with_its_navigation_in_a_frame_of_the_same_origin(self):
        log = self.signed_in_through('/lp/vault6/')
        self.assertIn('login export guide manager=lastpass at=click step=2', log)
        self.assertNotIn('guide miss', log, 'found without a miss')

    def test_lastpass_with_its_navigation_in_a_frame_of_another_origin_or_site(self):
        port = self.other.server_address[1]
        for frame in ('http://127.0.0.1:%d/lp/nav8' % port, 'http://localhost:%d/lp/nav8' % port):
            with self.subTest(frame=frame.split(':')[1]):
                self.log.seek(0), self.log.truncate(), self.answers.clear()
                log = self.signed_in_through('/lp/vault8/?f=' + frame)
                self.assertIn('login export guide manager=lastpass at=click step=2', log)
                self.assertNotIn('nav8', log, 'no address in the log')

    def test_lastpass_with_its_navigation_in_web_components_drawn_by_the_style_sheet(self):
        log = self.signed_in_through('/lp/vault7/')
        self.assertIn('login export guide manager=lastpass at=click step=1', log)
        self.assertIn('login export guide manager=lastpass at=click step=2', log)

    def test_a_changed_page_hands_the_owner_the_manual_steps(self):
        with patch.object(login_export_guide, 'GIVE_UP', 1.5):
            for watch in self.export('lastpass', '/lp/vault2/'):
                self.until(watch, 'manual')
                self.assertEqual(self.check(watch), {'state': 'waiting', 'step': 'manual'}, 'stays manual, still waiting for the file')
                # what kind of miss, in numbers: how much of the page the guide could look into
                self.assertRegex(self.log.getvalue(), r'login export guide miss manager=lastpass frames=0 other=0 shadow=0 custom=0 '
                                                      r'candidates=1 outside=0\n')
                login_import.export_stop(watch)
                time.sleep(0.5)


class AddressTest(unittest.TestCase):
    def test_a_page_that_stops_answering_hands_over_the_manual_steps_instead_of_a_spinner_for_good(self):
        state = login_export_guide.start()
        with patch.object(login_export_guide, 'look', return_value=None):
            self.assertIsNone(login_export_guide.step('http://127.0.0.1:9', 't', 'lastpass', state), 'a busy page: no new word yet')
            state['progress'] -= 3 * login_export_guide.GIVE_UP + 1
            self.assertEqual(login_export_guide.step('http://127.0.0.1:9', 't', 'lastpass', state), 'manual')

    def test_the_recipes_tell_the_sign_in_from_the_signed_in_vault(self):
        import re
        lp, bw, g = (login_export_guide.RECIPES[k] for k in ('lastpass', 'bitwarden', 'chrome'))
        for recipe, url, signin in ((lp, 'https://lastpass.com/?ac=1&lpnorefresh=1', True), (lp, 'https://lastpass.com/vault/', False),
                                    (bw, 'https://vault.bitwarden.com/#/login', True), (bw, 'https://vault.bitwarden.com/#/lock', True),
                                    (bw, 'https://vault.bitwarden.com/#/vault', False), (g, 'https://accounts.google.com/v3/signin', True),
                                    (g, 'https://passwords.google.com/options', False)):
            with self.subTest(url=url):
                self.assertEqual(bool(re.search(recipe['signin'], url, re.I)), signin)
                if not signin:
                    self.assertTrue(re.search(recipe['vault'], url, re.I))


if __name__ == '__main__':
    unittest.main()
