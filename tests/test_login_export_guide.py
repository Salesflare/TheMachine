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
import login_export_mail
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
    # LastPass's vault as it is now: Advanced options opens a list with Export in it (a second click folds it), and
    # Export starts the export: LastPass emails a link to confirm and the page doesn't change (no dialog, nothing new),
    # until a click after the link was opened asks the master password
    '/lp/vault9/': '<!doctype html><meta charset="utf-8"><title>Vault</title>' + SAVE + '''<nav><a href="#">Passwords</a>
        <button type="button" id="adv">Advanced options</button><ul id="more" hidden><li><button type="button" id="ex">Export</button></li>
        <li><button type="button">Import</button></li></ul></nav><p>''' + ON_PAGE + '''</p>
        <dialog id="dlg"><form method="dialog" onsubmit="save('lastpass_vault_export.csv', \'''' + LASTPASS_CSV + '''\')">
        <p>Enter your master password.</p><input type="password" id="mp"><button>Continue</button></form></dialog><script>
        window.started = 0; window.verified = false;
        document.getElementById('adv').onclick = () => { const m = document.getElementById('more'); m.hidden = !m.hidden; };
        document.getElementById('ex').onclick = () => { if (window.verified) document.getElementById('dlg').showModal(); else window.started++; };</script>''',
    # a folded navigation whose Advanced options folds it again and shows nothing the recipe knows: a loop
    '/lp/vault10/': '<!doctype html><meta charset="utf-8"><title>Vault</title><header><button type="button" aria-label="Open menu" id="m">=</button></header>' +
        '<nav id="nav" hidden><button type="button" id="adv">Advanced options</button></nav><p>' + ON_PAGE + '''</p><script>
        window.menus = 0; window.advs = 0;
        document.getElementById('m').onclick = () => { window.menus++; document.getElementById('nav').hidden = false; };
        document.getElementById('adv').onclick = () => { window.advs++; document.getElementById('nav').hidden = true; };</script>''',
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
                  patch.object(login_export_guide, 'AGAIN', 1), patch.object(login_export_guide, 'SETTLE', 1),
                  patch.object(login_export_guide, 'STARTED', 1), patch.object(login_import, 'VERIFY_POLL', 0)):
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

    def export(self, manager, page, mail=None):
        out, err = io.StringIO(), io.StringIO()
        with patch.dict(login_import.EXPORT_PAGES, {manager: self.origin + page}), redirect_stdout(out), redirect_stderr(err):
            watch = login_import.export_open(self.base, manager, self.folder, self.store, mail=mail)['watch']
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

    def test_lastpass_export_is_started_exactly_once_when_the_page_does_not_change(self):
        # LastPass emails a link to confirm on each click of Export: the guide clicks it once and then waits on the
        # owner's email, never back through the menu to it
        for watch in self.export('lastpass', '/lp/vault9/'):
            self.until(watch, 'email')
            for _ in range(8):  # more looks at a page that stays the same
                self.assertEqual(self.check(watch)['step'], 'email')
                time.sleep(0.5)
            self.assertEqual(self.owner(watch, '() => window.started'), 1, 'the click that starts the export, exactly once')
            log = self.log.getvalue()
            self.assertEqual(log.count('at=click step=2'), 1)
            self.assertEqual(log.count('at=click step=1'), 1, 'Advanced options not clicked again')
            self.assertIn('login export guide started manager=lastpass step=2\n', log)
            # the owner confirmed the email and exports again by hand
            self.owner(watch, '() => { window.verified = true; document.getElementById("ex").click(); return 1; }')
            self.until(watch, 'password')
            self.typed_master(watch)
            self.review(watch)

    def test_lastpass_verification_link_mailed_after_the_click_is_opened_once_then_export_once_more(self):
        asked, opened = [], []

        def mail(manager, since, seen):
            asked.append((manager, since))
            return 'https://lastpass.com/verify-export?fake=1'

        def open_link(base, link):  # stands in for LastPass's page behind the link: the export is confirmed
            opened.append(link)
            browser_login.browser_cdp.evaluate(self.base, login_import._exports[next(iter(login_import._exports))]['tab'],
                                               '() => { window.verified = true; return 1; }')
            return True

        clicked = time.time()
        with patch.object(login_import, '_open_link', open_link):
            for watch in self.export('lastpass', '/lp/vault9/', mail=mail):
                self.until(watch, 'password')
                self.assertEqual(self.owner(watch, '() => window.started'), 1, 'once before the link, once after it')
                self.typed_master(watch)
                self.review(watch)
        self.assertEqual(opened, ['https://lastpass.com/verify-export?fake=1'], 'one link per export')
        self.assertEqual(len(asked), 1)
        self.assertEqual(asked[0][0], 'lastpass')
        self.assertGreaterEqual(asked[0][1], clicked - 1, 'mails since the click only')
        log = self.log.getvalue()
        self.assertIn('login export verify opened manager=lastpass ok=yes\n', log)
        self.assertEqual(log.count('login export guide started manager=lastpass step=2'), 2)
        self.assertNotIn('fake=1', log, 'no link in the log')

    def test_a_page_that_loops_stops_clicking_and_hands_over_the_steps(self):
        for watch in self.export('lastpass', '/lp/vault10/'):
            self.until(watch, 'manual', seconds=30)
            self.assertEqual(self.owner(watch, '() => [window.menus, window.advs]'), [2, 2], 'one round back, not a second')
            self.assertIn('login export guide loop manager=lastpass step=0 rounds=2\n', self.log.getvalue())
            time.sleep(1.5)
            self.assertEqual(self.owner(watch, '() => [window.menus, window.advs]'), [2, 2], 'no clicks after handing over')
            self.assertEqual(self.check(watch), {'state': 'waiting', 'step': 'manual'}, 'the live view stays, waiting for the file')
            login_import.export_stop(watch)
            time.sleep(0.5)


APPROVE = '/export-tokens/00000000-0000-0000-0000-000000000000/approve'  # LastPass's verify link, a fake token
UTM = '?utm_source=trans_email&utm_medium=LastPassSecurityNotification%3AVerifyexport'


def fake_mail(sender='LastPass <no-reply@lastpass.com>', subject='LastPass Security Notification: Verify export',
              came=None, href='https://lastpass.com' + APPROVE + '?k=fake', auth='mx.example.invalid; dkim=pass header.d=lastpass.com',
              words='Continue export', parts=None):
    body = '<p>Someone asked to export.</p><a href="https://lastpass.com/help">Help</a> <a href="%s">%s</a>' % (href, words)
    headers = [{'name': 'From', 'value': sender}, {'name': 'Subject', 'value': subject}]
    if auth:
        headers.append({'name': 'Authentication-Results', 'value': auth})
    return {'internalDate': str(int((came if came is not None else time.time()) * 1000)),
            'payload': {'mimeType': 'multipart/alternative', 'headers': headers, 'parts': [
                {'mimeType': kind, 'body': {'data': base64.urlsafe_b64encode(text.encode()).decode().rstrip('=')}}
                for kind, text in (parts or [('text/html', body)])]}}


# The shape of LastPass's "Verify export" mail: its logo link carries "Verifyexport" in its query, before the real link
LASTPASS_TEXT = ('( https://lastpass.com/%s )\nSomeone asked to export your vault.\nContinue export ( https://lastpass.com%s%s )\n'
                 "No, it wasn't me\nhttp://link.lastpass.com/lastpass-account-has-been-compromised "
                 '( https://link.lastpass.com/lastpass-account-has-been-compromised%s )\n' % (UTM, APPROVE, UTM, UTM))
LASTPASS_HTML = ('<a href="https://lastpass.com/%s"><img alt=""></a><p>Someone asked to export your vault.</p>'
                 '<a href="https://lastpass.com/%s">Verify export</a> '
                 '<a href="https://link.lastpass.com/lastpass-account-has-been-compromised%s">Continue export</a> '
                 '<a href="https://lastpass.com%s%s">Continue export</a> '
                 '<a href="https://link.lastpass.com/lastpass-account-has-been-compromised%s">No, it wasn\'t me</a>'
                 % (UTM, UTM, UTM, APPROVE, UTM, UTM))


class VerifyMailTest(unittest.TestCase):
    """login_export_mail: only the manager's own verify mail since the click, its https link on the manager's hosts."""

    def test_the_verify_mail_after_the_click_gives_its_link(self):
        since = time.time() - 30
        link = 'https://lastpass.com' + APPROVE + '?k=fake'
        self.assertEqual(login_export_mail.pick(fake_mail(), 'lastpass', since)[1], link)
        self.assertEqual(login_export_mail.pick(fake_mail(auth=None), 'lastpass', since)[1], link,
                         'a mailbox that records no sender checks: the sender alone')
        self.assertEqual(login_export_mail.pick(fake_mail(sender='no-reply@mail.lastpass.eu', auth=None, href='https://lastpass.eu' + APPROVE),
                                                'lastpass', since)[1], 'https://lastpass.eu' + APPROVE)

    def test_lastpass_mail_gives_its_approve_link_never_the_logo_or_the_compromised_link(self):
        since, approve = time.time() - 30, 'https://lastpass.com' + APPROVE + UTM
        sender = 'LastPass <do-not-reply@mail.lastpass.com>'
        for name, parts in (('text only', [('text/plain', LASTPASS_TEXT)]), ('html only', [('text/html', LASTPASS_HTML)])):
            with self.subTest(name):
                self.assertEqual(login_export_mail.pick(fake_mail(sender=sender, parts=parts), 'lastpass', since)[1], approve)
                without = parts[0][1].replace('https://lastpass.com' + APPROVE, 'https://lastpass.com/export-tokens/x/deny')
                self.assertIsNone(login_export_mail.pick(fake_mail(sender=sender, parts=[(parts[0][0], without)]), 'lastpass', since),
                                  'no approve link: the owner confirms by hand, never the logo or the compromised link')

    def test_only_the_path_counts_never_the_words_or_the_query(self):
        since = time.time() - 30
        for name, href in (('words alone', 'https://lastpass.com/help'),
                           ('the query alone', 'https://lastpass.com/?next=' + APPROVE),
                           ('a longer path', 'https://lastpass.com' + APPROVE + '/more'),
                           ('a path in front', 'https://lastpass.com/x' + APPROVE)):
            with self.subTest(name):
                self.assertIsNone(login_export_mail.pick(fake_mail(href=href), 'lastpass', since))

    def test_wrong_sender_host_time_or_checks_give_nothing(self):
        since = time.time() - 30
        for name, mail in (('another sender', fake_mail(sender='LastPass <no-reply@lastpass.com.example.invalid>')),
                           ('a look-alike', fake_mail(sender='no-reply@notlastpass.com')),
                           ('another subject', fake_mail(subject='Your weekly report')),
                           ('before the click', fake_mail(came=since - 60)),
                           ('a failed check', fake_mail(auth='mx.example.invalid; dkim=fail header.d=lastpass.com; dmarc=fail')),
                           ('a pass for another domain', fake_mail(auth='mx.example.invalid; dkim=pass header.d=example.invalid')),
                           ('another host', fake_mail(href='https://lastpass.com.example.invalid' + APPROVE)),
                           ('plain http', fake_mail(href='http://lastpass.com' + APPROVE)),
                           ('a user in the address', fake_mail(href='https://x@lastpass.com' + APPROVE)),
                           ('another port', fake_mail(href='https://lastpass.com:8443' + APPROVE))):
            with self.subTest(name):
                self.assertIsNone(login_export_mail.pick(mail, 'lastpass', since))
        self.assertIsNone(login_export_mail.pick(fake_mail(), 'bitwarden', since), 'a manager without a verify mail')
        self.assertIsNone(login_export_mail.pick(fake_mail(), 'lastpass', None), 'no click, no mail')

    def test_the_newest_mail_in_the_owners_mailboxes_each_read_once(self):
        since = time.time() - 60
        mails = {'old': fake_mail(came=since - 5, href='https://lastpass.com' + APPROVE + '?k=old'),
                 'a': fake_mail(came=since + 10, href='https://lastpass.com' + APPROVE + '?k=a'),
                 'b': fake_mail(came=since + 20, href='https://lastpass.com' + APPROVE + '?k=b'),
                 'spoof': fake_mail(came=since + 30, sender='x@example.invalid', href='https://lastpass.com' + APPROVE + '?k=spoof')}
        reads = []

        def read(config, account, api, version, method, params, scope):
            self.assertEqual(scope, login_export_mail.SCOPE, 'the read the mailbox already has')
            reads.append((method, params.get('id')))
            if method == 'gmail.users.messages.list':
                self.assertEqual(params['q'], 'after:%d' % int(since))
                return {'messages': [{'id': k} for k in mails]}
            return mails[params['id']]

        config = {'accounts': [{'id': 'm1', 'service': 'gmail', 'email': 'owner@example.invalid'},
                               {'id': 'm2', 'service': 'gmail', 'email': 'team@example.invalid', 'shared': True}]}
        seen = set()
        with patch.object(login_export_mail.sources, 'gog_read', read):
            self.assertEqual(login_export_mail.link(config, 'lastpass', since, seen), 'https://lastpass.com' + APPROVE + '?k=b')
            self.assertIsNone(login_export_mail.link(config, 'lastpass', since, seen), 'each mail is read once')
            self.assertIsNone(login_export_mail.link(config, 'lastpass', None), 'no running export: nothing read')
            self.assertIsNone(login_export_mail.link({'accounts': []}, 'lastpass', since), 'no mailbox: the owner confirms')
        self.assertEqual(sum(1 for m, _ in reads if m == 'gmail.users.messages.get'), 4, 'only the owner\'s own mailbox, once each')


class VerifyTest(unittest.TestCase):
    """login_import._verify: only for a running export the guide started, once, within the window."""

    def watch(self, mail):
        return {'manager': 'lastpass', 'base': 'http://127.0.0.1:9', 'mail': mail, 'mails': set(), 'asked': None,
                'verify_opened': False, 'stop': threading.Event()}

    def test_no_click_no_mail_read(self):
        asked = []
        guide = login_export_guide.start()
        with patch.object(login_import, '_open_link') as opened:
            self.assertFalse(login_import._verify(self.watch(lambda *a: asked.append(a) or 'https://lastpass.com/v'), guide))
        self.assertEqual(asked, [], 'no export started on this run: nothing read')
        opened.assert_not_called()

    def test_a_link_is_opened_once_per_export_then_the_export_may_start_once_more(self):
        guide = login_export_guide.start()
        guide.update(started=time.monotonic(), started_at=time.time(), starts=0)
        watch = self.watch(lambda manager, since, seen: 'https://lastpass.com' + APPROVE + '?k=1')
        with patch.object(login_import, '_open_link', return_value=True) as opened, patch.object(login_import, 'VERIFY_POLL', 0):
            self.assertTrue(login_import._verify(watch, guide))
            self.assertEqual(guide['starts'], 1)
            self.assertIsNone(guide['started'])
            guide.update(started=time.monotonic(), starts=0)  # the guide's second start
            self.assertFalse(login_import._verify(watch, guide))
        opened.assert_called_once_with('http://127.0.0.1:9', 'https://lastpass.com' + APPROVE + '?k=1')
        login_export_guide.verified(guide)
        self.assertEqual(guide['starts'], 0, 'one verification per export')

    def test_a_link_on_another_host_or_after_the_window_is_never_opened(self):
        with patch.object(login_import, '_open_link') as opened, patch.object(login_import, 'VERIFY_POLL', 0):
            guide = login_export_guide.start()
            guide.update(started=time.monotonic(), started_at=time.time())
            self.assertFalse(login_import._verify(self.watch(lambda *a: 'https://evil.example.invalid/lastpass.com'), guide))
            late = login_export_guide.start()
            late.update(started=time.monotonic() - login_import.VERIFY_SECONDS - 1, started_at=time.time() - 700)
            asked = []
            self.assertFalse(login_import._verify(self.watch(lambda *a: asked.append(a)), late))
            self.assertEqual(asked, [])
        opened.assert_not_called()


class LoopTest(unittest.TestCase):
    """login_export_guide._may: what may be clicked after the step that starts the export and after a round back."""

    def test_nothing_up_to_the_export_start_is_clicked_again_until_a_verification(self):
        recipe, state, now = login_export_guide.RECIPES['lastpass'], login_export_guide.start(), time.monotonic()
        state.update(top=2, top_at=now - 60, started=now - 60, starts=0)
        self.assertEqual(login_export_guide._may(recipe, state, now), [False, False, False, True])
        login_export_guide.verified(state)
        self.assertEqual(login_export_guide._may(recipe, state, now), [True, True, True, True])

    def test_a_second_round_back_is_not_clicked(self):
        recipe, state, now = login_export_guide.RECIPES['lastpass'], login_export_guide.start(), time.monotonic()
        state.update(top=1, top_at=now - 1)
        self.assertEqual(login_export_guide._may(recipe, state, now)[:2], [False, False], 'waits a little for the next step')
        state['top_at'] = now - 60
        self.assertEqual(login_export_guide._may(recipe, state, now)[:2], [True, True], 'one round back')
        state['rounds'] = 1
        self.assertEqual(login_export_guide._may(recipe, state, now)[:3], [False, False, True], 'not a second, a later step still')


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
