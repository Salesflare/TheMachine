"""Saved sign-ins with several accounts per site, bound to exact origins; the move from one sign-in per site; bringing
them in from a password manager (CSV exports and the op and lpass tools, both mocked: no real vault is ever called);
and a planted fake password that must never show up in an answer, a log, an error, the database or a prompt.
Made-up credentials and temporary folders only."""
import base64, io, json, logging, os, shutil, sqlite3, tempfile, threading, time, unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import browser_login
import login_import
import machine.main as machine_main
import machine.app.preparation as machine_app_preparation

USER, SECRET = 'test-user@example.invalid', 'not-a-real-password-123'
PLANTED = 'planted-fake-secret-Zq81xV'  # must never leave the store


def message_key(folder):
    import secrets as random
    path = Path(folder) / browser_login.message_seal.KEY_NAME
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as handle:
        handle.write(base64.b64encode(random.token_bytes(32)).decode() + '\n')


class Folder(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name)
        message_key(self.folder)
        self.store = browser_login.LoginStore(self.folder)


class OriginTest(unittest.TestCase):
    def test_the_origin_is_scheme_host_and_port_as_a_browser_says_it(self):
        o = browser_login.origin
        self.assertEqual(o('https://Example.com/login?next=/'), 'https://example.com')
        self.assertEqual(o('https://example.com:443/x'), 'https://example.com')
        self.assertEqual(o('https://example.com:8443/x'), 'https://example.com:8443')
        self.assertEqual(o('example.com'), 'https://example.com')  # a bare host is https
        self.assertEqual(o('http://127.0.0.1:8000/'), 'http://127.0.0.1:8000')
        self.assertEqual(o('https://exаmple.com'), 'https://xn--exmple-4nf.com')  # a Cyrillic a: its own punycode host
        for bad in ('', 'javascript:alert(1)', 'android://app', 'ftp://example.com', 'https://', 'https://user:pw@example.com',
                    'https://exa mple.com', None):
            self.assertIsNone(o(bad), bad)

    def test_lookalikes_subdomains_and_http_are_other_origins(self):
        real = browser_login.origin('https://example.com')
        for other in ('https://login.example.com', 'https://example.com.evil.invalid', 'https://examp1e.com',
                      'https://exаmple.com', 'http://example.com', 'https://example.com:8443', 'https://example.co',
                      'https://wwwexample.com'):
            self.assertNotEqual(browser_login.origin(other), real, other)


class FakeTab:
    """A browser tab over DevTools: answers the sign-in scripts like a page at `at` would, and records what was typed."""

    def __init__(self, at, typed):
        self.at, self.typed = at, typed

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def run(self, fn, *args):
        here = browser_login.origin(self.at)
        if fn == '(' + browser_login.DETECT + ')':
            return {'host': here.split('://', 1)[1], 'origin': here, 'secure': here.startswith('https://'),
                    'username': True, 'password': True, 'code': False}
        if fn in (browser_login.FOCUS, browser_login.SUBMIT):
            origins = args[2]
            if args[0] != here.split('://', 1)[1] or (origins and here not in origins):
                return 'moved'
            return 'ok' if fn == browser_login.FOCUS else 'clicked'
        if fn == browser_login.SETTLED:
            return 'moved'
        return None

    def call(self, method, params=None):
        if method == 'Input.insertText':
            self.typed.append(params['text'])
        return {}


class BindingTest(unittest.TestCase):
    """A saved password goes only into a page on one of its exact origins."""

    def fill(self, at, origins):
        typed = []
        with patch.object(browser_login.browser_cdp, 'Session', lambda *a, **k: FakeTab(at, typed)), \
                patch.object(browser_login.browser_cdp, 'evaluate', return_value=None), \
                patch.object(browser_login, '_wall', return_value=False), patch.object(browser_login, '_checkpoint', return_value=False), \
                patch.object(browser_login.time, 'sleep'):
            host = browser_login.origin(at).split('://', 1)[1]
            seen = {}
            done = browser_login.fill({}, '0:tab', host, USER, SECRET, settle=0, origins=origins, seen=seen)
        return done, typed, seen

    def test_filled_on_its_own_origin(self):
        done, typed, seen = self.fill('https://example.com/login', ['https://example.com'])
        self.assertEqual(done['result'], 'done')
        self.assertEqual(typed, [USER, SECRET])
        self.assertEqual(seen, {'origin': 'https://example.com'})

    def test_refused_on_any_other_origin_and_nothing_typed(self):
        for at in ('https://login.example.com/', 'https://example.com.evil.invalid/', 'https://examp1e.com/',
                   'https://xn--exmple-4nf.com/', 'https://example.com:8443/'):
            with self.subTest(at=at):
                with self.assertRaises(ValueError) as caught:
                    self.fill(at, ['https://example.com'])
                self.assertIn('another address', str(caught.exception))
                self.assertNotIn(SECRET, str(caught.exception))

    def test_no_origins_means_nothing_to_fill(self):
        with self.assertRaisesRegex(ValueError, 'no address'):
            self.fill('https://example.com/', [])


class AccountsTest(Folder):
    def test_several_named_accounts_per_site_never_overwrite_each_other(self):
        work = self.store.save('https://shop.example.invalid', 'me@work.example.invalid', 'work-pass-1', account='Work')
        home = self.store.save('https://shop.example.invalid', 'me@home.example.invalid', 'home-pass-1', account='Personal')
        self.assertNotEqual(work, home)
        self.assertEqual(self.store.save('https://shop.example.invalid', None, 'work-pass-2', account='work'), work)  # same account
        self.assertEqual(self.store.get(work)['password'], 'work-pass-2')
        self.assertEqual(self.store.get(home)['password'], 'home-pass-1')
        listed = self.store.list()
        self.assertEqual([(x['account'], x['username']) for x in listed], [('Personal', 'me@home.example.invalid'), ('Work', 'me@work.example.invalid')])
        self.assertNotIn('password', json.dumps(listed).replace('password_saved', ''))
        self.assertEqual(self.store.for_origin('https://shop.example.invalid'),
                         [{'id': home, 'account': 'Personal', 'username': 'me@home.example.invalid'},
                          {'id': work, 'account': 'Work', 'username': 'me@work.example.invalid'}])
        self.assertEqual(self.store.for_origin('https://www.shop.example.invalid'), [])  # exact origin only
        self.assertTrue(self.store.forget(work))
        self.assertEqual([x['account'] for x in self.store.list()], ['Personal'])

    def test_a_moved_over_default_gets_its_side_but_never_a_name_taken_there(self):
        site = 'https://crm.example.invalid'
        old = self.store.save(site, 'me@acme.example.invalid', 'o')  # as one moved over: Default
        work = self.store.save(site, 'me@home.example.invalid', 'w', account='Work')
        with self.assertRaisesRegex(ValueError, 'already has'):
            self.store.rename(old, 'work')
        self.assertTrue(self.store.rename(old, 'Personal'))
        self.assertFalse(self.store.rename(old, 'Personal'))
        self.assertEqual([(x['id'], x['account']) for x in self.store.list()], [(old, 'Personal'), (work, 'Work')])
        self.assertEqual(self.store.get(old)['password'], 'o')
        with self.assertRaisesRegex(ValueError, 'any more'):
            self.store.rename('0' * 16, 'Work')
        self.assertEqual([browser_login.side_of(a) for a in (None, 'personal', 'work', 'work:Acme')], [None, 'Personal', 'Work', 'Work'])

    def test_a_wrong_side_is_changed_or_cleared_and_to_dos_pick_by_the_new_one(self):
        site = 'https://crm.example.invalid'
        home = self.store.save(site, 'me@home.example.invalid', 'h', account='Work')  # marked Work by mistake
        acme = self.store.save(site, 'me@acme.example.invalid', 'w', account='Personal')
        self.assertEqual(self.store.pick(site, 'task-w', 'work'), home)
        self.store.remember('task-w', home)  # used once from the dialog
        self.assertTrue(self.store.rename(acme, 'Default'))  # cleared: not set again
        self.assertTrue(self.store.rename(home, 'Personal'))
        self.assertTrue(self.store.rename(acme, 'Work'))
        self.assertEqual({x['id']: x['account'] for x in self.store.list()}, {home: 'Personal', acme: 'Work'})
        self.assertEqual(self.store.pick(site, 'task-w', 'work'), acme)  # the to-do follows the new mark
        self.assertEqual(self.store.pick(site, 'task-p', 'personal'), home)
        self.assertEqual(self.store.get(home)['password'], 'h')

    def test_a_to_do_picks_by_meaning_or_asks_once(self):
        site = 'https://crm.example.invalid'
        work = self.store.save(site, 'me@acme.example.invalid', 'w', account='Work')
        self.assertEqual(self.store.pick(site, 'task-1', None), work)  # the only one
        home = self.store.save(site, 'me@home.example.invalid', 'h', account='Personal')
        self.assertEqual(self.store.pick(site, 'task-1', 'personal'), home)
        self.assertEqual(self.store.pick(site, 'task-1', 'work:Acme'), work)
        self.assertEqual(self.store.pick(site, 'task-1', 'work'), work)
        self.assertIsNone(self.store.pick(site, 'task-1', None))  # unclear: the dialog asks
        acme = self.store.save(site, 'ops@acme.example.invalid', 'a', account='Acme')
        self.assertIsNone(self.store.pick(site, 'task-1', 'work:Acme'))  # Work and Acme both fit: ask
        self.store.remember('task-1', acme)  # asked once
        self.assertEqual(self.store.pick(site, 'task-1', 'personal'), acme)  # the owner's choice stands for that to-do
        self.assertEqual(self.store.pick(site, 'task-2', 'personal'), home)
        self.store.remember('task-3', 'not-an-id')
        self.assertIsNone(self.store.pick(site, 'task-3', None))
        self.assertIsNone(self.store.pick('https://other.example.invalid', 'task-1', 'work'))


def older_file(folder, logins):
    """The file an older version kept: one sign-in per site, sealed with the message key."""
    key = browser_login.message_seal.load_key(Path(folder) / browser_login.SEALED)
    (Path(folder) / browser_login.SEALED).write_bytes(browser_login.message_seal.Sealer(key).seal_bytes(json.dumps(logins).encode()))


class MigrationTest(Folder):
    OLDER = {'example.invalid': {'username': USER, 'password': SECRET, 'saved_at': '2026-01-02T03:04:05+00:00'},
             'portal.example.invalid': {'username': 'second-user', 'password': 'second-pass'}}

    def test_each_site_becomes_one_default_account_and_the_older_file_stays_as_the_backup(self):
        older_file(self.folder, self.OLDER)
        backup = (self.folder / browser_login.SEALED).read_bytes()
        before = self.store.list()  # read as accounts before anything moved, with the same ids
        self.assertTrue(self.store.migrate())
        self.assertEqual(self.store.list(), before)
        self.assertEqual((self.folder / browser_login.SEALED).read_bytes(), backup)  # untouched: the backup
        self.assertTrue(browser_login.message_seal.is_sealed_file(self.folder / browser_login.ACCOUNTS))
        self.assertEqual([(x['site'], x['account'], x['username']) for x in before],
                         [('example.invalid', 'Default', USER), ('portal.example.invalid', 'Default', 'second-user')])
        entry = self.store.get(before[0]['id'])
        self.assertEqual(entry['origins'], ['https://example.invalid', 'https://www.example.invalid'])  # the older key had dropped the www
        self.assertEqual((entry['password'], entry['saved_at']), (SECRET, '2026-01-02T03:04:05+00:00'))
        self.assertEqual(self.store.get('www.example.invalid')['password'], SECRET)  # an older dashboard's host still finds it

    def test_running_it_again_changes_nothing(self):
        older_file(self.folder, self.OLDER)
        self.assertTrue(self.store.migrate())
        after = (self.folder / browser_login.ACCOUNTS).read_bytes()
        self.assertFalse(self.store.migrate())
        self.assertFalse(browser_login.LoginStore(self.folder).migrate())
        self.assertEqual((self.folder / browser_login.ACCOUNTS).read_bytes(), after)

    def test_revert_goes_back_to_the_older_file(self):
        older_file(self.folder, self.OLDER)
        self.store.migrate()
        self.store.save('https://example.invalid', USER, 'another-pass', account='Work')
        self.assertEqual(len(self.store.list()), 3)
        self.assertTrue(self.store.revert())
        self.assertFalse((self.folder / browser_login.ACCOUNTS).exists())
        self.assertEqual([(x['site'], x['account']) for x in self.store.list()], [('example.invalid', 'Default'), ('portal.example.invalid', 'Default')])
        self.assertFalse(self.store.revert())
        self.assertTrue(self.store.migrate())  # and forward again
        self.assertEqual(len(self.store.list()), 2)

    def test_forget_takes_it_out_of_the_backup_too(self):
        older_file(self.folder, self.OLDER)
        self.store.migrate()
        first = self.store.list()[0]['id']
        self.assertTrue(self.store.forget(first))
        key = browser_login.message_seal.load_key(self.folder / browser_login.SEALED)
        older = json.loads(browser_login.message_seal.Sealer(key).open_bytes((self.folder / browser_login.SEALED).read_bytes()))
        self.assertEqual(list(older), ['portal.example.invalid'])
        self.store.revert()
        self.assertEqual([x['site'] for x in self.store.list()], ['portal.example.invalid'])
        self.assertEqual(self.store.forget_all(), 1)
        self.assertEqual(sorted(p.name for p in self.folder.iterdir()), [browser_login.message_seal.KEY_NAME])

    @unittest.skipUnless(shutil.which('openssl'), 'needs openssl')
    def test_without_message_protection_the_older_files_key_is_kept_while_either_needs_it(self):
        with tempfile.TemporaryDirectory() as folder:
            store = browser_login.LoginStore(folder)
            store._write_file(store.sealed_path, store.path, self.OLDER)  # an older install with a key of its own
            self.assertTrue(store.migrate())
            for name in (browser_login.STORE, browser_login.ACCOUNTS_STORE, browser_login.KEY):
                self.assertTrue((Path(folder) / name).exists(), name)
            self.assertEqual(len(store.list()), 2)
            message_key(folder)  # message protection turned on: both move over and the key of their own goes
            self.assertTrue(store.migrate())
            self.assertEqual(sorted(p.name for p in Path(folder).iterdir()),
                             sorted([browser_login.message_seal.KEY_NAME, browser_login.SEALED, browser_login.ACCOUNTS]))
            self.assertEqual(store.get('example.invalid')['password'], SECRET)


EXPORTS = {
    '1password': ('Title,Url,Username,Password,OTPAuth,Favorite,Archived,Tags,Notes\n'
                  'Example,https://example.invalid/login,me@example.invalid,{p},,false,false,,\n'
                  'Router,http://192.0.2.1/,admin,{p},,false,false,,\n'
                  '"Quoted, title",https://quoted.example.invalid,"me, too",{p},,false,false,,"a\nnote"\n'),
    'lastpass': ('url,username,password,totp,extra,name,grouping,fav\n'
                 'https://example.invalid/,me@example.invalid,{p},,,Example,Shopping,0\n'
                 'http://sn,,,,secure note text,A note,Notes,0\n'),
    'bitwarden': ('folder,favorite,type,name,notes,fields,reprompt,login_uri,login_username,login_password,login_totp\n'
                  ',,login,Example,,,0,"https://example.invalid,https://app.example.invalid:8443/x",me@example.invalid,{p},\n'
                  ',,note,A note,secret note,,0,,,,\n'),
    'chrome': ('name,url,username,password,note\n'
               'example.invalid,https://example.invalid/,me@example.invalid,{p},\n'
               'android,android://hash@com.example.app/,me,{p},\n'),
}


class CsvTest(unittest.TestCase):
    def test_each_managers_export(self):
        expected = {'1password': (['https://example.invalid', 'https://quoted.example.invalid'], 1),
                    'lastpass': (['https://example.invalid'], 1),
                    'bitwarden': (['https://app.example.invalid:8443', 'https://example.invalid'], 1),
                    'chrome': (['https://example.invalid'], 1)}
        for kind, text in EXPORTS.items():
            with self.subTest(kind=kind):
                found, rows, skipped = login_import.parse(text.format(p=SECRET))
                self.assertEqual(found, kind)
                self.assertEqual((sorted(r['origin'] for r in rows), skipped), expected[kind])
                self.assertTrue(all(r['password'] == SECRET and r['username'].startswith('me') for r in rows))
        _, rows, _ = login_import.parse(EXPORTS['1password'].format(p=SECRET))
        self.assertEqual([r['username'] for r in rows if 'quoted' in r['origin']], ['me, too'])

    def test_a_bom_firefoxs_columns_and_duplicates(self):
        text = '﻿"url","username","password","httpRealm"\n"https://example.invalid","me","{p}",""\n"https://example.invalid","me","{p}",""\n'
        kind, rows, _ = login_import.parse(text.format(p=SECRET))
        self.assertEqual((kind, len(rows)), ('csv', 1))

    def test_what_isnt_an_export_is_refused_without_quoting_it(self):
        for text in ('', 'just some words ' + PLANTED, 'a,b,c\n1,2,' + PLANTED + '\n', 'x' * (6 * 1024 * 1024)):
            with self.assertRaises(ValueError) as caught:
                login_import.parse(text)
            self.assertNotIn(PLANTED, str(caught.exception))


class FakeTools:
    """Stands in for the op and lpass tools: `state` per tool is missing, signed_out or ready. Never a real vault."""

    def __init__(self, state, secret=SECRET):
        self.state, self.secret, self.calls = state, secret, []

    def which(self, name):
        tool = {'op': '1password', 'lpass': 'lastpass'}.get(name)
        return None if not tool or self.state.get(tool, 'missing') == 'missing' else '/fake/bin/' + name

    def run(self, args, timeout=30):
        self.calls.append(list(args))
        tool, verb = Path(args[0]).name, args[1]
        if self.state['1password' if tool == 'op' else 'lastpass'] != 'ready':
            return 1, ''
        if (tool, verb) in (('op', 'whoami'), ('lpass', 'status')):
            return 0, ''
        if tool == 'op' and verb == 'item' and args[2] == 'list':
            return 0, json.dumps([{'id': 'abc123', 'title': 'Example', 'additional_information': 'me@example.invalid',
                                   'urls': [{'href': 'https://example.invalid/login', 'primary': True}, {'href': 'http://insecure.example.invalid'}]},
                                  {'id': 'def456', 'title': 'No address', 'urls': []}])
        if tool == 'op' and verb == 'item' and args[2] == 'get':
            return 0, json.dumps({'id': args[3], 'fields': [{'id': 'username', 'purpose': 'USERNAME', 'value': 'me@example.invalid'},
                                                            {'id': 'password', 'purpose': 'PASSWORD', 'value': self.secret}]})
        if tool == 'lpass' and verb == 'ls':
            return 0, '\x1f'.join(('1234', 'Example', 'https://example.invalid/', 'me@example.invalid')) + '\n'
        if tool == 'lpass' and verb == 'show':
            return 0, json.dumps([{'id': args[-1], 'username': 'me@example.invalid', 'password': self.secret}])
        return 1, ''

    def __enter__(self):
        self.patches = [patch.object(login_import.shutil, 'which', self.which), patch.object(login_import, '_run', self.run)]
        for p in self.patches:
            p.start()
        return self

    def __exit__(self, *a):
        for p in self.patches:
            p.stop()


class PickerTest(Folder):
    def test_missing_or_signed_out_says_so_and_never_signs_in(self):
        for state in ('missing', 'signed_out'):
            with FakeTools({'1password': state, 'lastpass': state}) as tools:
                for manager in ('1password', 'lastpass'):
                    self.assertEqual(login_import.tool_state(manager), state)
                    with self.assertRaisesRegex(ValueError, 'isn’t installed' if state == 'missing' else 'Sign in to'):
                        login_import.tool_list(manager)
                verbs = {tuple(c[1:2]) for c in tools.calls}
                self.assertFalse(verbs & {('signin',), ('login',), ('account',)}, 'never signs in')
        self.assertEqual(self.store.list(), [])

    def test_ready_lists_without_passwords_and_reads_only_what_is_kept(self):
        with FakeTools({'1password': 'ready', 'lastpass': 'ready'}) as tools:
            review = login_import.start('1password', login_import.tool_list('1password'), 0, self.store)
            self.assertEqual([(r['site'], r['username']) for r in review['rows']], [('example.invalid', 'me@example.invalid')])
            self.assertNotIn(SECRET, json.dumps(review))
            self.assertFalse(any(c[1:3] == ['item', 'get'] for c in tools.calls), 'no password read before Keep')
            kept = login_import.keep(self.store, review['token'], [review['rows'][0]['key']], 'Work')
            self.assertEqual(kept, 1)
            self.assertEqual([c[3] for c in tools.calls if c[1:3] == ['item', 'get']], ['abc123'])
            review = login_import.start('lastpass', login_import.tool_list('lastpass'), 0, self.store)
            self.assertEqual(review['rows'][0]['saved'], ['Work'])
            login_import.keep(self.store, review['token'], [r['key'] for r in review['rows']], 'Personal')
            for call in tools.calls:
                self.assertNotIn('--password', call[:2])
        self.assertEqual([(x['account'], x['source']) for x in self.store.list()], [('Personal', 'lastpass'), ('Work', '1password')])
        with self.assertRaisesRegex(ValueError, 'expired'):
            login_import.keep(self.store, review['token'], [], 'Work')  # a review is kept once

    def test_tool_runs_have_no_terminal_and_no_pinentry(self):
        seen = {}

        def run(args, **kw):
            seen.update(kw)
            raise OSError('not here')
        with patch.object(login_import.subprocess, 'run', run):
            self.assertEqual(login_import._run(['/fake/bin/lpass', 'status']), (1, ''))
        self.assertIs(seen['stdin'], login_import.subprocess.DEVNULL)
        self.assertEqual(seen['env']['LPASS_DISABLE_PINENTRY'], '1')


class CsvImportTest(Folder):
    def test_review_then_keep_only_the_ticked_ones_under_the_chosen_account(self):
        kind, rows, skipped = login_import.parse(EXPORTS['bitwarden'].format(p=SECRET))
        review = login_import.start(kind, rows, skipped, self.store)
        self.assertEqual((review['manager'], review['skipped'], len(review['rows'])), ('Bitwarden', 1, 2))
        self.assertNotIn(SECRET, json.dumps(review))
        keep = [r['key'] for r in review['rows'] if r['origin'] == 'https://example.invalid']
        self.assertEqual(login_import.keep(self.store, review['token'], keep, 'Personal'), 1)
        self.assertEqual([(x['origin'], x['account'], x['source']) for x in self.store.list()],
                         [('https://example.invalid', 'Personal', 'csv:bitwarden')])

    def test_a_dropped_or_old_review_holds_nothing(self):
        kind, rows, skipped = login_import.parse(EXPORTS['chrome'].format(p=SECRET))
        review = login_import.start(kind, rows, skipped, self.store)
        self.assertTrue(login_import.drop(review['token']))
        self.assertFalse(any(review['token'] == t for t in login_import._pending))
        review = login_import.start(kind, rows, skipped, self.store)
        with patch.object(login_import.time, 'monotonic', return_value=login_import.time.monotonic() + 3600):
            with self.assertRaisesRegex(ValueError, 'expired'):
                login_import.keep(self.store, review['token'], [rows[0]['key']], None)


class PasswordStep(FakeTab):
    """The second page of a two-step sign-in: a password field, no username field."""

    def run(self, fn, *args):
        found = super().run(fn, *args)
        return {**found, 'username': False} if fn == '(' + browser_login.DETECT + ')' else found


class TwoStepTest(unittest.TestCase):
    """Username, Next, then the password on its own page: Save for next time at the password step keeps the username
    typed before (save_username), and never types it into the page."""

    def test_the_earlier_username_is_saved_with_the_password(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        data = Path(temp.name)
        message_key(data)
        app = object.__new__(machine_main.App)
        app.store, app.config = machine_main.Store(data / 'events.sqlite'), {'accounts': [], 'database': str(data / 'events.sqlite')}
        typed = []
        with patch.object(browser_login.browser_cdp, 'Session', lambda *a, **k: PasswordStep('https://example.invalid/login', typed)), \
                patch.object(browser_login.browser_cdp, 'evaluate', return_value=None), \
                patch.object(browser_login, '_wall', return_value=False), patch.object(browser_login, '_checkpoint', return_value=False), \
                patch.object(browser_login.time, 'sleep'), patch.object(app, 'resume_signed_in', return_value=[]):
            app.action('browser_login_fill', {'page': '0:tab', 'host': 'example.invalid', 'password': SECRET, 'save': True,
                                              'save_username': USER, 'account': 'Work'}, owner_dashboard=True)
            app.action('browser_login_fill', {'page': '0:tab', 'host': 'example.invalid', 'password': SECRET, 'save': True,
                                              'save_username': 'two\nlines', 'account': 'Personal'}, owner_dashboard=True)
        self.assertEqual(typed, [SECRET, SECRET])  # the username is never typed on the password page
        listed = {x['account']: x['username'] for x in app.action('browser_logins', {}, owner_dashboard=True)['logins']}
        self.assertEqual(listed, {'Work': USER, 'Personal': ''})


class ExportFileKindsTest(Folder):
    def test_a_lastpass_or_1password_file_keeps_its_own_passwords_without_their_tools(self):
        with FakeTools({'1password': 'missing', 'lastpass': 'missing'}) as tools:
            for kind in ('lastpass', '1password'):
                found, rows, skipped = login_import.parse(EXPORTS[kind].format(p=SECRET))
                review = login_import.start(found, rows, skipped, self.store)
                self.assertGreater(login_import.keep(self.store, review['token'], [r['key'] for r in review['rows']], kind.title()), 0)
            self.assertEqual(tools.calls, [], 'a file never asks a tool')
        self.assertEqual(sorted(x['account'] for x in self.store.list() if x['origin'] == 'https://example.invalid'), ['1Password', 'Lastpass'])

    def test_bitwardens_json_and_an_encrypted_one(self):
        doc = {'encrypted': False, 'items': [
            {'type': 1, 'name': 'Example', 'login': {'username': 'me@example.invalid', 'password': SECRET,
                                                     'uris': [{'uri': 'https://example.invalid/login'}, {'uri': 'http://insecure.example.invalid'}]}},
            {'type': 2, 'name': 'A note', 'notes': 'note text'}]}
        kind, rows, skipped = login_import.parse(json.dumps(doc))
        self.assertEqual((kind, [r['origin'] for r in rows], skipped), ('bitwarden', ['https://example.invalid'], 1))
        with self.assertRaisesRegex(ValueError, 'encrypted') as caught:
            login_import.parse(json.dumps({'encrypted': True, 'items': [{'type': 1, 'login': {'password': PLANTED}}]}))
        self.assertNotIn(PLANTED, str(caught.exception))


class FakeBrowser:
    """Stands in for the Machine's browser over DevTools: records the calls and tabs; never a real browser."""

    def __init__(self):
        self.calls, self.opened, self.closed, self.tabs = [], [], [], {}

    def session(self, base, timeout=30):
        fake = self

        class Session:
            ws = type('WS', (), {'close': lambda self: fake.calls.append(('close', None))})()

            def call(self, method, params=None):
                fake.calls.append((method, params))
                return {}
        return Session()

    def folder(self):
        """The export's download folder, once its own thread has opened the page (export_open answers before)."""
        for _ in range(250):
            found = [p['downloadPath'] for m, p in list(self.calls) if m == 'Browser.setDownloadBehavior' and p['behavior'] == 'allow']
            if found and self.opened:
                return Path(found[0])
            time.sleep(0.02)
        raise AssertionError('the export page never opened')

    def __enter__(self):
        cdp = browser_login.browser_cdp
        self.patches = [patch.object(cdp.Session, 'browser', self.session),
                        patch.object(cdp, 'open_tab', lambda base, url: self.opened.append(url) or self.tabs.update({'tab-1': url}) or 'tab-1'),
                        patch.object(cdp, 'close_tab', lambda base, tab: self.closed.append(tab) or self.tabs.pop(tab, None)),
                        patch.object(cdp, 'pages', lambda base, timeout=10: list(self.tabs.items())),
                        patch.object(login_import, 'EXPORT_POLL', 0.02)]
        for p in self.patches:
            p.start()
        return self

    def __exit__(self, *a):
        for p in self.patches:
            p.stop()


def wait_for(check, token, seconds=5):
    until = time.monotonic() + seconds
    while time.monotonic() < until:
        got = check(token)
        if got['state'] != 'waiting':
            return got
        time.sleep(0.02)
    return got


class ExportPageTest(Folder):
    def test_the_download_is_read_once_deleted_and_the_browser_put_back(self):
        with FakeBrowser() as browser:
            opened = login_import.export_open('http://127.0.0.1:9', 'bitwarden', self.folder, self.store)
            folder = browser.folder()
            self.assertEqual(browser.opened, [login_import.EXPORT_PAGES['bitwarden']])
            self.assertEqual(folder.parent, self.folder)
            self.assertEqual(folder.stat().st_mode & 0o777, 0o700)
            self.assertEqual(login_import.export_check(opened['watch'])['state'], 'waiting')
            (folder / 'export.csv.crdownload').write_text('half')  # still coming: not read
            (folder / 'export.csv.crdownload').rename(folder / 'bitwarden_export.csv')
            (folder / 'bitwarden_export.csv').write_text(EXPORTS['bitwarden'].format(p=SECRET))
            review = wait_for(login_import.export_check, opened['watch'])
            self.assertEqual((review['state'], review['manager'], len(review['rows'])), ('review', 'Bitwarden', 2))
            self.assertNotIn(SECRET, json.dumps(review))
            for _ in range(100):
                if not folder.exists():
                    break
                time.sleep(0.02)
            self.assertFalse(folder.exists(), 'the file and its folder are gone from disk')
            self.assertIn(('Browser.setDownloadBehavior', {'behavior': 'default'}), browser.calls)
            self.assertEqual(browser.closed, ['tab-1'])
            self.assertEqual(login_import.export_check(opened['watch'])['state'], 'expired', 'answered once')
            self.assertEqual(login_import.keep(self.store, review['token'], [review['rows'][0]['key']], 'Work'), 1)

    def test_a_file_that_isnt_an_export_says_so_and_is_deleted_too(self):
        with FakeBrowser() as browser:
            opened = login_import.export_open('http://127.0.0.1:9', 'lastpass', self.folder, self.store)
            folder = browser.folder()
            (folder / 'notes.csv').write_text('a,b\n1,' + PLANTED + '\n')
            got = wait_for(login_import.export_check, opened['watch'])
            self.assertEqual(got['state'], 'failed')
            self.assertNotIn(PLANTED, got['error'])

    def test_stop_puts_the_browser_back_and_an_unknown_manager_opens_nothing(self):
        with FakeBrowser() as browser:
            opened = login_import.export_open('http://127.0.0.1:9', 'chrome', self.folder, self.store)
            folder = browser.folder()
            self.assertTrue(login_import.export_stop(opened['watch']))
            for _ in range(250):  # the export's thread closes the session, then removes the folder: wait for both
                if ('close', None) in browser.calls and not folder.exists():
                    break
                time.sleep(0.02)
            self.assertIn(('Browser.setDownloadBehavior', {'behavior': 'default'}), browser.calls)
            self.assertIn(('close', None), browser.calls)
            self.assertFalse(folder.exists())
            with self.assertRaisesRegex(ValueError, 'Which password manager'):
                login_import.export_open('http://127.0.0.1:9', '1password', self.folder, self.store)
            self.assertEqual(browser.opened, [login_import.EXPORT_PAGES['chrome']])

    def test_the_call_answers_at_once_while_the_browser_takes_its_time_and_a_page_that_never_opens_says_so(self):
        # The dashboard's call timed out while the Machine's browser started: export_open now answers before it opens.
        gate = threading.Event()

        def slow(base, timeout=30):
            gate.wait(5)
            raise browser_login.browser_cdp.CdpError('browser not reachable')
        with patch.object(browser_login.browser_cdp.Session, 'browser', slow), patch.object(login_import, 'OPEN_SECONDS', 0.2):
            began = time.monotonic()
            opened = login_import.export_open('http://127.0.0.1:9', 'lastpass', self.folder, self.store)
            self.assertLess(time.monotonic() - began, 1, 'answers without waiting on the browser')
            self.assertEqual(login_import.export_check(opened['watch']), {'state': 'waiting', 'step': 'opening'})
            time.sleep(0.3)
            self.assertEqual(login_import.export_check(opened['watch']),
                             {'state': 'failed', 'error': 'I couldn’t open the export page in your Machine’s browser'})
            gate.set()
        with patch.object(browser_login.browser_cdp.Session, 'browser', slow):
            opened = login_import.export_open('http://127.0.0.1:9', 'lastpass', self.folder, self.store)
            got = wait_for(login_import.export_check, opened['watch'])
            self.assertEqual(got['state'], 'failed', 'a browser that answers with an error fails at once, in a sentence')
        left = lambda: [p for p in self.folder.iterdir() if p.name.startswith('login-export-')]
        for _ in range(100):
            if not left():
                break
            time.sleep(0.02)
        self.assertEqual(left(), [], 'no folder left')

    def test_a_closed_export_tab_says_so_instead_of_waiting(self):
        with FakeBrowser() as browser, patch.object(browser_login.browser_cdp, 'pages', return_value=[('another-tab', 'about:blank')]):
            opened = login_import.export_open('http://127.0.0.1:9', 'bitwarden', self.folder, self.store)
            browser.folder()
            got = wait_for(login_import.export_check, opened['watch'])
            self.assertEqual(got, {'state': 'failed', 'error': 'The export page was closed. Try again.'})


class LeakScanTest(unittest.TestCase):
    """A planted fake password goes in through every way in (an export, both tools, the dialog), is used, and must
    never show up in an answer, a log line, stdout or stderr, an error, the database or the model's prompts."""

    def test_the_planted_secret_never_leaves_the_store(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        data = Path(temp.name)
        message_key(data)
        store = machine_main.Store(data / 'events.sqlite')
        app = object.__new__(machine_main.App)
        app.store, app.config = store, {'accounts': [], 'database': str(data / 'events.sqlite')}
        with store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,account_ids,event_ids,title,body,status,created_at) "
                       "VALUES('s1','renew:1','[]','[]','Renew the plan','Renew it on the portal','open','2026-01-01')")
        captured, answers, errors = io.StringIO(), [], []
        handler = logging.StreamHandler(captured)
        handler.setLevel(logging.DEBUG)
        root = logging.getLogger()
        old_level = root.level
        root.addHandler(handler)
        root.setLevel(logging.DEBUG)
        self.addCleanup(lambda: (root.removeHandler(handler), root.setLevel(old_level)))
        act = lambda name, args: answers.append(app.action(name, args, owner_dashboard=True)) or answers[-1]

        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err), FakeTools({'1password': 'ready', 'lastpass': 'ready'}, secret=PLANTED):
            review = act('browser_login_import', {'do': 'file', 'text': EXPORTS['1password'].format(p=PLANTED)})
            act('browser_login_import', {'do': 'keep', 'token': review['token'], 'keys': [r['key'] for r in review['rows']], 'account': 'Work'})
            for manager in ('1password', 'lastpass'):
                review = act('browser_login_import', {'do': 'tool', 'manager': manager})
                act('browser_login_import', {'do': 'keep', 'token': review['token'], 'keys': [r['key'] for r in review['rows']], 'account': 'Personal'})
            # the export page in the Machine's browser: its download read, kept and gone from disk
            with FakeBrowser() as browser, patch('browser_viewer.focus', return_value=None):
                started = act('browser_login_import', {'do': 'export', 'manager': 'bitwarden'})
                (browser.folder() / 'bitwarden_export.csv').write_text(EXPORTS['bitwarden'].format(p=PLANTED))
                review = wait_for(lambda w: act('browser_login_import', {'do': 'export_check', 'watch': w}), started['watch'])
                act('browser_login_import', {'do': 'keep', 'token': review['token'], 'keys': [r['key'] for r in review['rows']], 'account': 'Work'})
                for _ in range(250):
                    if not any(p.name.startswith('login-export-') for p in data.iterdir()):
                        break
                    time.sleep(0.02)
            act('browser_login_import', {'do': 'tools'})
            listed = act('browser_logins', {})
            # each way it could go wrong: a bad file, a stale review, a fill on a lookalike
            for name, args in (('browser_login_import', {'do': 'file', 'text': 'a,b\n' + PLANTED}),
                               ('browser_login_import', {'do': 'keep', 'token': 'gone', 'keys': []})):
                try:
                    act(name, args)
                except ValueError as error:
                    errors.append(str(error))
            login = next(x['id'] for x in listed['logins'] if x['origin'] == 'https://example.invalid' and x['account'] == 'Work')
            typed = []
            for at in ('https://example.invalid/login', 'https://example.invalid.evil.invalid/login'):
                with patch.object(browser_login.browser_cdp, 'Session', lambda *a, **k: FakeTab(at, typed)), \
                        patch.object(browser_login.browser_cdp, 'evaluate', return_value=None), \
                        patch.object(browser_login, '_wall', return_value=False), patch.object(browser_login, '_checkpoint', return_value=False), \
                        patch.object(browser_login.time, 'sleep'), patch.object(app, 'resume_signed_in', return_value=[]):
                    try:
                        act('browser_login_fill', {'page': '0:tab', 'host': browser_login.origin(at).split('://', 1)[1], 'use_saved': login, 'suggestion_id': 's1'})
                    except ValueError as error:
                        errors.append(str(error))
        self.assertEqual(typed, ['me@example.invalid', PLANTED])  # it was used, on its own origin only
        self.assertEqual(len(errors), 3)

        with store.connect() as db:
            job = {'job_id': 'j1', 'suggestion_id': 's1'}
            prompts = [machine_app_preparation.preparation_prompt(job, store.facts_text(), app.config),
                       machine_app_preparation.chat_prompt({**job, 'message': 'Sign in and renew it'}, app.config)]
        places = {'answers': json.dumps(answers), 'logs': captured.getvalue(), 'stdout': out.getvalue(), 'stderr': err.getvalue(),
                  'errors': ' '.join(errors), 'prompts': ' '.join(prompts)}
        for where, text in places.items():
            self.assertNotIn(PLANTED, text, where)
        for path in data.iterdir():  # the database (and its journal), and every file but the sealed store
            if path.is_file():
                self.assertNotIn(PLANTED.encode(), path.read_bytes(), path.name)
        self.assertNotIn(PLANTED, ' '.join(map(str, login_import._pending.values())))


if __name__ == '__main__':
    unittest.main()
