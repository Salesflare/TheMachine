"""Birthdays from Facebook (birthdays_facebook.py, birthdays_facebook_app.py, docs/help/routines.md "Templates"): the
Birthdays template offers one to-do, once, on a Machine with a browser. Only the owner's Import reads Facebook's
birthdays page, in a tab of its own that is closed after, scrolling until every month has loaded (or until its limits,
which the preview says, with the months that never loaded); a browser that isn't signed in is said and nothing is read. The
preview names who matched (the same full name as exactly one person), skips a name two people have, and only Save keeps
their birthdays, as facts with source facebook that the Birthdays run reads like Google's. Nothing else is kept. A
made-up page (tests/facebook-birthdays-fixture.html) and made-up people only; never the real Facebook."""
import datetime as dt
import http.server
import importlib.util
import json
import os
import shutil
import socket
import subprocess
import tempfile
import threading
import time
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('facebook_birthdays_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import birthdays  # noqa: E402
import birthdays_facebook as fb  # noqa: E402
import enrichment  # noqa: E402
import graph  # noqa: E402
import person_birthday  # noqa: E402

FIXTURE = Path(__file__).parent / 'facebook-birthdays-fixture.html'
TODAY = dt.date(2026, 11, 10)
CHROME = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome-stable') or shutil.which('chromium-browser')
FIRST = 'Ada Bram Cleo Dov Esme Finn Gia Hugo Ines Jules Kai Lena Milo Nora Otto Pia Quin Rhea Sami Tove Uma Vito Wren Xavi Yara'.split()
LAST = 'Arden Brook Calloway Dunmore Ellery Fairbank Garrow Hollis Ivers Jessup Kestrel Lowell Marsh Northam Orrin Pell Quarry Rook Stroud Thorne'.split()
MORE = 'Vane Wilde Yates Ziegler Abbott Bexley Corran Dace Eldred Fenwick'.split()
SIGN_IN = b'<!doctype html><title>Log in</title><form id="login_form" action="/login"><input name="email"><input name="pass" type="password"></form>'


class Page(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = SIGN_IN if self.path.startswith('/login') else FIXTURE.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):  # the page's graphql request (.../data/): answered with what it sent, as Facebook answers
        body = self.rfile.read(int(self.headers.get('Content-Length') or 0))
        self.send_response(200)
        self.send_header('Content-Type', 'text/javascript; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'for (;;);' + body)

    def log_message(self, *args):
        pass


class Labels(unittest.TestCase):
    def test_a_label_gives_a_name_and_a_day(self):
        for label, heading, want in (
                ('Sam Rivera (November 14)', '', ('Sam Rivera', '--11-14')),
                ('Sam Rivera, 14 November 1990', '', ('Sam Rivera', '1990-11-14')),
                ('Sam Rivera\nSaturday, November 14', '', ('Sam Rivera', '--11-14')),
                ('Sam Rivera 14 november', 'November', ('Sam Rivera', '--11-14')),  # Dutch
                ('Sam Rivera, 3. März', '', ('Sam Rivera', '--03-03')),
                ('Sam Rivera, 3 de marzo', '', ('Sam Rivera', '--03-03')),
                ('Sam Rivera 11/14', '', ('Sam Rivera', '--11-14')),
                ('Sam Rivera 3/4', 'March', ('Sam Rivera', '--03-04')),  # the month heading says which is the month
                ('Sam Rivera 3/4', '', None),  # March 4 or April 3: not guessed
                ('Robin Vale', "Today's birthdays", ('Robin Vale', '--11-10')),
                ('Robin Vale', 'Upcoming birthdays', None),  # a name alone, not under Today
                ('Robin (November 2)', '', None),  # a first name only
                ('Settings', '', None), ('Sam Rivera (February 30)', '', None)):
            self.assertEqual(fb.parse(label, heading, TODAY), want, label)

    def test_a_friend_from_the_pages_data_gives_a_name_and_a_day(self):
        for item, want in (({'name': 'Sam Rivera', 'month': 11, 'day': 14, 'year': None}, ('Sam Rivera', '--11-14')),
                           ({'name': 'Sam Rivera', 'month': 11, 'day': 14, 'year': 1990}, ('Sam Rivera', '1990-11-14')),
                           ({'name': 'Sam', 'month': 11, 'day': 14}, None), ({'name': 'Sam Rivera', 'month': 2, 'day': 30}, None),
                           ({'name': 'Sam Rivera', 'month': 'x', 'day': 1}, None)):
            self.assertEqual(fb.from_data(item, TODAY), want, item)

    def test_a_name_shown_with_two_days_is_left_out(self):
        found = fb.found([{'label': 'Sam Rivera (November 14)'}, {'label': 'Sam Rivera (December 1)'}, {'label': 'Jo Tanaka (December 3)'},
                          {'label': 'Jo Tanaka, December 3, 1990'}], TODAY)
        self.assertEqual(found, {'Jo Tanaka': '1990-12-03'})  # the one with a year


@unittest.skipUnless(CHROME, 'needs Chrome or Chromium')
class Read(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Page)
        threading.Thread(target=cls.site.serve_forever, daemon=True).start()
        cls.origin = 'http://127.0.0.1:%d' % cls.site.server_address[1]
        cls.profile = tempfile.mkdtemp()
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
        cls.chrome = subprocess.Popen([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--remote-debugging-port=%d' % port,
                                       '--user-data-dir=' + cls.profile, 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
        shutil.rmtree(cls.profile, ignore_errors=True)

    def ours(self):
        """The tabs on the made-up page still open (closing a tab takes the browser a moment)."""
        for _ in range(50):
            found = [t for t in fb.browser_cdp._http(self.base, '/json/list') if t.get('type') == 'page' and t.get('url', '').startswith(self.origin)]
            if not found:
                break
            time.sleep(0.1)
        return found

    FAST = {'pause': 300}  # the made-up page loads a chunk within 1.1 s; the real one gets 0.8 s and up to 5 s more

    @staticmethod
    def friends(total=500, skip=-1):
        """The made-up page's friends as the made-up page lists them: month by month from this one."""
        first, out = dt.date.today().month - 1, {}
        for k in range(total):
            offset = k * 12 // total
            if offset != skip:
                year = '1988-' if k % 50 == 0 else '--'
                name = '%s %s%s' % (FIRST[k % len(FIRST)], LAST[k // len(FIRST) % len(LAST)], '-' + MORE[k // 500 % len(MORE)] if k >= 500 else '')
                out[name] = '%s%02d-%02d' % (year, (first + offset) % 12 + 1, 1 + k * 7 % 28)
        return out

    def test_scrolls_until_every_month_has_loaded_and_reads_every_friend_then_closes_its_tab(self):
        result = fb.read(self.base, self.origin + '/events/birthdays/', self.FAST)
        self.assertEqual(self.ours(), [])  # its own tab is closed
        self.assertEqual((result['capped'], result['missing']), (False, []))
        found = fb.found(result['items'], TODAY)
        self.assertEqual(len(found), 501)  # 500 over 12 months, 20 at a time, and Robin today
        self.assertEqual(found, {'Robin Vale': '--11-10', **self.friends()})

    def test_a_month_nobody_has_is_named_after_the_page_stays_quiet(self):
        result = fb.read(self.base, self.origin + '/events/birthdays/small/skip5/', {**self.FAST, 'idle': 3000})
        self.assertFalse(result['capped'])
        self.assertEqual(result['missing'], [(dt.date.today().month + 4) % 12 + 1])
        self.assertEqual(len(fb.found(result['items'], TODAY)), 12)

    def test_the_limits_stop_it_and_say_which_months_never_loaded(self):
        result = fb.read(self.base, self.origin + '/events/birthdays/', {**self.FAST, 'items': 100})
        self.assertTrue(result['capped'])
        self.assertEqual(len(result['items']), 100)
        self.assertTrue(6 <= len(result['missing']) <= 10)  # about 2.5 of 12 months loaded
        self.assertNotIn(dt.date.today().month, result['missing'])

    def test_stops_soon_after_every_month_is_there_though_the_page_keeps_growing(self):
        for path in ('/events/birthdays/early/', '/events/birthdays/early/data/'):
            started = time.monotonic()
            result = fb.read(self.base, self.origin + path, self.FAST)
            took = time.monotonic() - started
            self.assertEqual((result['capped'], result['missing']), (False, []), path)
            self.assertLessEqual(result['extra'], 3, path)  # scrolls after every month was there: the settle, and no more
            self.assertLess(took, 15, path)  # the cap is minutes; it ends in seconds
            self.assertEqual(len(fb.found(result['items'], TODAY)), 501 if 'data' not in path else 500, path)

    def test_reads_every_friend_from_the_pages_data_on_a_long_page_that_drops_what_it_scrolled_past(self):
        for size, chunk in ((1700, 100), (5000, 250)):  # Facebook allows 5,000 friends
            result = fb.read(self.base, self.origin + '/events/birthdays/data/virtual/n%d/chunk%d/' % (size, chunk), self.FAST)
            self.assertEqual((result['capped'], result['missing']), (False, []), size)
            self.assertEqual(fb.found(result['items'], TODAY), self.friends(size), size)  # every one, with its day and year
            self.assertLessEqual(result['extra'], 5, size)  # the last month's last chunks, then the settle: a progress bar that never goes away doesn't hold it up

    def test_reads_every_label_on_a_page_that_drops_what_it_scrolled_past(self):
        result = fb.read(self.base, self.origin + '/events/birthdays/virtual/n1700/chunk100/', self.FAST)
        self.assertEqual((result['capped'], result['missing']), (False, []))
        self.assertEqual(fb.found(result['items'], TODAY), {'Robin Vale': '--11-10', **self.friends(1700)})

    def test_reads_the_tooltips_when_the_labels_have_no_dates(self):
        found = fb.found(fb.read(self.base, self.origin + '/events/birthdays/hover/small/', self.FAST)['items'], TODAY)
        self.assertEqual(found, self.friends(12))  # the Today picture has no tooltip in this made-up page

    def test_a_sign_in_page_is_said_and_nothing_is_read(self):
        self.assertEqual(fb.read(self.base, self.origin + '/login/?next=birthdays'), {'error': 'signed-out'})
        self.assertEqual(self.ours(), [])


class Import(unittest.TestCase):
    ITEMS = [{'label': 'Robin Vale', 'heading': "Today's birthdays"}, {'label': 'Sam Rivera (November 14)', 'heading': 'November'},
             {'label': 'Jo Tanaka (December 3)', 'heading': 'December'}, {'label': 'Pat Quinn (December 9)', 'heading': 'December'},
             {'label': 'Lee Okafor (January 5)', 'heading': 'January'}]

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'home', 'email': 'owner@mail.example', 'service': 'gmail', 'boundary': 'personal'}],
                           'timezone': 'Europe/Brussels', 'browser_cdp_url': 'http://127.0.0.1:9'}
        self.store.accounts = self.app.config['accounts']
        self.app.birthdays_facebook_inline = True
        self.reads, self.answer = [], {'items': self.ITEMS}
        for name, value in (('birthdays_facebook_base', lambda s: 'http://127.0.0.1:9'),):
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        p = patch.object(fb, 'read', lambda base, url=fb.PAGE, limits=None: self.reads.append(url) or self.answer); p.start(); self.addCleanup(p.stop)
        p = patch('subprocess.run', lambda *x, **k: subprocess.CompletedProcess(x, 0, '', '')); p.start(); self.addCleanup(p.stop)  # the lease
        with self.store.connect() as db:
            graph.ensure(db)
            for node, name in (('email:robin@mail.example', 'Robin Vale'), ('email:sam@mail.example', 'Sam Rivera'),
                               ('email:jo@mail.example', 'Jo Tanaka'), ('email:pat@one.example', 'Pat Quinn'), ('email:pat@two.example', 'Pat Quinn')):
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,'person',?,1,?,5,?)",
                           (node, name, '2026-11-01', json.dumps({'identifiers': [node], 'wrote': 3})))
            enrichment.offer_facts(db, [(['email:jo@mail.example'], {'birthday': '1990-12-03'}, enrichment.RECORD)], 'google', '2026-11-01')

    def offer(self):
        return self.app.birthdays_facebook_offer({'routine_id': 'r1'})

    def card(self, sid):
        with self.store.connect() as db:
            return fb.view(db, sid)

    def test_offered_once_and_nothing_read_before_the_owners_tap(self):
        sid = self.offer()
        self.assertTrue(sid)
        self.assertIsNone(self.offer())  # once per Machine
        self.assertEqual(self.card(sid), {'state': 'new'})
        self.assertEqual(self.reads, [])
        with self.assertRaises(ValueError):
            self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': 'read'}, owner_dashboard=False)
        self.assertEqual(self.reads, [])

    def test_no_browser_no_todo(self):
        with patch.object(a.App, 'birthdays_facebook_base', lambda s: None):
            self.assertIsNone(self.offer())
        self.assertTrue(self.offer())  # offered once it has one

    def test_preview_then_only_save_keeps_the_birthdays(self):
        sid = self.offer()
        self.assertEqual(self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': 'read'}, owner_dashboard=True), {'state': 'reading'})
        self.assertEqual(self.reads, [fb.PAGE])
        view = self.card(sid)
        self.assertEqual(view['state'], 'preview')
        self.assertEqual((view['found'], view['matched'], view['new'], view['unmatched']), (5, 3, 2, 1))  # Jo's was known already
        self.assertEqual(view['ambiguous'], ['Pat Quinn'])
        self.assertEqual({m['name'] for m in view['shown']}, {'Robin Vale', 'Sam Rivera', 'Jo Tanaka'})
        with self.store.connect() as db:
            self.assertNotIn('email:sam@mail.example', enrichment.people_facts(db, ('birthday',)))  # nothing kept yet
        done = self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': 'save'}, owner_dashboard=True)
        self.assertEqual(done['saved'], 2)
        self.assertEqual({p['name'] for p in done['people']}, {'Robin Vale', 'Sam Rivera'})  # linked on the to-do
        with self.store.connect() as db:
            facts = enrichment.people_facts(db, ('birthday',))
            row = db.execute('SELECT data,state FROM facebook_birthdays WHERE suggestion_id=?', (sid,)).fetchone()
            status = db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0]
            on_day = birthdays.fact_ids(db, dt.date(2026, 11, 14))
        self.assertEqual(facts['email:sam@mail.example']['birthday'][:3], ('--11-14', enrichment.RECORD, 'facebook'))
        self.assertEqual(facts['email:jo@mail.example']['birthday'][2], 'google')  # the same day, kept as it was
        self.assertFalse({'email:pat@one.example', 'email:pat@two.example'} & set(facts))
        self.assertIn(('email:sam@mail.example', 'contacts'), on_day)  # the Birthdays run reads it like Google's
        kept = json.loads(row['data'])
        self.assertEqual((row['state'], set(kept)), ('saved', {'saved', 'people', 'others', 'added'}))  # who was saved; the rest read is gone
        self.assertEqual(([o['name'] for o in kept['others']], kept['added']), (['Lee Okafor'], []))  # but friends nobody in the Graph has, for the Add button
        self.assertEqual({p['id'] for p in kept['people']}, {'email:robin@mail.example', 'email:sam@mail.example'})
        with self.store.connect() as db:
            self.assertEqual(person_birthday.get(db, 'email:sam@mail.example')['source'], 'facebook')  # the one on their page
        self.assertEqual(self.card(sid)['people'][0]['id'], 'email:robin@mail.example')
        self.assertEqual(status, 'completed')
        with self.assertRaises(ValueError):
            self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': 'save'}, owner_dashboard=True)  # saved once

    def test_a_birthday_the_owner_set_or_removed_stays(self):
        with self.store.connect() as db:
            person_birthday.set_birthday(db, 'email:sam@mail.example', {'month': 2, 'day': 1}, '2026-11-02')
            person_birthday.offer(db, 'email:robin@mail.example', '--03-04', 'google', '2026-11-02')  # removed over a contact's
            person_birthday.set_birthday(db, 'email:robin@mail.example', {'remove': True}, '2026-11-03')
        sid = self.offer()
        self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': 'read'}, owner_dashboard=True)
        self.assertEqual(self.card(sid)['new'], 0)  # Sam's and Robin's are the owner's, Jo's was known
        done = self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': 'save'}, owner_dashboard=True)
        self.assertEqual(done['saved'], 0)
        with self.store.connect() as db:
            self.assertEqual(person_birthday.get(db, 'email:sam@mail.example')['value'], '--02-01')
            self.assertIsNone(person_birthday.get(db, 'email:robin@mail.example'))  # removed stays removed

    def test_signed_out_is_said_and_import_again_is_the_owners_tap(self):
        sid = self.offer()
        self.answer = {'error': 'signed-out'}
        self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': 'read'}, owner_dashboard=True)
        self.assertEqual(self.card(sid), {'state': 'signed_out'})
        # Sign in to Facebook on the to-do: Facebook's sign-in page in the Machine's browser, for the dashboard's
        # sign-in dialog, the way LinkedIn and X sign in. Only from the dashboard, and nothing is read by it.
        cdp = a.browser_login.browser_cdp
        with patch.object(cdp, '_http', return_value=[]), patch.object(cdp, 'open_tab', return_value='t1') as opened, \
                patch.object(a.browser_viewer, 'focus') as focus:
            self.assertTrue(self.app.action('connect_site_signin', {'site': 'facebook'}, owner_dashboard=True)['opened'])
            with self.assertRaises(ValueError):
                self.app.action('connect_site_signin', {'site': 'facebook'}, owner_dashboard=False)
        self.assertEqual((opened.call_args.args[1], focus.call_args.kwargs['target']), ('https://www.facebook.com/login/', 't1'))
        self.assertEqual((self.card(sid), len(self.reads)), ({'state': 'signed_out'}, 1))
        self.answer = {'items': []}
        self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': 'read'}, owner_dashboard=True)
        self.assertEqual(self.card(sid), {'state': 'failed', 'empty': True})
        self.assertEqual(len(self.reads), 2)  # one read per tap, never by itself

    def test_a_read_cut_short_says_so_and_which_months_are_missing(self):
        sid = self.offer()
        self.answer = {'items': self.ITEMS, 'capped': True, 'missing': [3, 4, 'x']}
        self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': 'read'}, owner_dashboard=True)
        view = self.card(sid)
        self.assertEqual((view['found'], view['capped'], view['missing']), (5, True, [3, 4]))
        self.answer = {'items': self.ITEMS}
        self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': 'read'}, owner_dashboard=True)
        self.assertEqual((self.card(sid)['capped'], self.card(sid)['missing']), (False, []))

    def test_a_middle_name_on_one_side_still_matches_one_person(self):
        with self.store.connect() as db:
            for node, name in (('email:ann@mail.example', 'Ann Marie Lowell'), ('email:kim@one.example', 'Kim Ivers'),
                               ('email:kim@two.example', 'Kim Jo Ivers')):
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,'person',?,1,?,5,?)",
                           (node, name, '2026-11-01', json.dumps({'identifiers': [node], 'wrote': 3})))
            got = fb.match(db, {'Ann Lowell': '--03-04', 'Kim Ivers': '--05-06', 'Kim Lee Ivers': '--07-08', 'Ann Rook': '--01-02'})
        self.assertEqual([(m['id'], m['date']) for m in got['matched']], [('email:ann@mail.example', '--03-04'), ('email:kim@one.example', '--05-06')])
        self.assertEqual((got['ambiguous'], got['unmatched']), (['Kim Lee Ivers'], 1))  # two Kim Ivers by first and last name

    def test_a_read_that_never_ended_says_it_failed(self):
        sid = self.offer()
        with self.store.connect() as db:
            fb.put(db, sid, 'reading', {}, '2026-11-10T08:00:00+00:00')
            self.assertEqual(fb.view(db, sid, now=dt.datetime(2026, 11, 10, 8, 2, tzinfo=dt.timezone.utc)), {'state': 'reading'})
            self.assertEqual(fb.view(db, sid, now=dt.datetime(2026, 11, 10, 9, 0, tzinfo=dt.timezone.utc)), {'state': 'failed', 'empty': False})

    def test_the_todo_shows_its_import(self):
        sid = self.offer()
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            extra = self.store.suggestion_result(row, db)
        self.assertEqual(extra['facebook_birthdays'], {'state': 'new'})
        self.assertEqual(row['title'], 'Import birthdays from Facebook')


if __name__ == '__main__':
    unittest.main()
