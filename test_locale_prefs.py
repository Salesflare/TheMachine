"""Language and region (locale_prefs.py): the date order and clock follow the owner's region, Time format overrides the
clock, a Machine without a region keeps US dates and 24-hour times, and the dashboard formats like the server."""
import datetime as dt
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

import assistant
import calendar_writes
import family
import fleet_requests
import installer
import locale_prefs

ROOT = pathlib.Path(__file__).resolve().parent
AFTERNOON = dt.datetime(2026, 10, 24, 14, 5, 9)
MORNING = dt.datetime(2026, 10, 24, 0, 30)


class LocaleTest(unittest.TestCase):
    def tearDown(self):
        locale_prefs.configure({})

    def use(self, **config):
        locale_prefs.configure(config)

    def test_a_machine_without_a_region_keeps_us_dates_and_24_hour_times(self):
        self.use()
        self.assertEqual(locale_prefs.at_text(AFTERNOON), 'Sat, Oct 24 at 14:05')
        self.assertEqual(locale_prefs.view()['date_locale'], 'en-US')
        self.assertFalse(locale_prefs.view()['hour12'])

    def test_the_region_sets_the_date_order_and_the_usual_clock(self):
        self.use(locale='en-US')
        self.assertEqual(locale_prefs.at_text(AFTERNOON), 'Sat, Oct 24 at 2:05 PM')
        self.assertEqual(locale_prefs.clock_text(MORNING), '12:30 AM')
        self.assertEqual(locale_prefs.clock_text(AFTERNOON, seconds=True), '2:05:09 PM')
        self.use(locale='en-GB')
        self.assertEqual(locale_prefs.at_text(AFTERNOON), 'Sat 24 Oct at 14:05')
        self.assertEqual(locale_prefs.day_text(AFTERNOON, year=True), 'Sat 24 Oct 2026')
        self.use(locale='en-AU')
        self.assertEqual(locale_prefs.at_text(AFTERNOON), 'Sat 24 Oct at 2:05 PM')
        self.assertEqual(locale_prefs.view()['date_locale'], 'en-GB')

    def test_time_format_overrides_the_region(self):
        self.use(locale='en-US', clock='24h')
        self.assertEqual(locale_prefs.clock_text(AFTERNOON), '14:05')
        self.use(locale='en-BE', clock='12h')
        self.assertEqual(locale_prefs.clock_text(AFTERNOON), '2:05 PM')
        self.assertFalse(locale_prefs.view()['auto_hour12'])
        self.use(clock='12h')  # no region: US dates, the chosen clock
        self.assertEqual(locale_prefs.at_text(AFTERNOON), 'Sat, Oct 24 at 2:05 PM')
        self.use(locale='en-BE', clock='sometimes')  # a bad value is ignored
        self.assertEqual(locale_prefs.view()['clock'], 'auto')

    def test_tags_are_normalized_and_other_languages_read_english_for_now(self):
        self.assertEqual(locale_prefs.normalize('en_gb'), 'en-GB')
        self.assertEqual(locale_prefs.normalize('nl-BE'), 'en-BE')
        self.assertEqual(locale_prefs.normalize(''), '')
        self.assertIsNone(locale_prefs.normalize('english'))
        self.assertIsNone(locale_prefs.normalize('en-GB"><script>'))
        self.assertEqual(locale_prefs.settings({'locale': 'en-ie', 'clock': '24h'}), {'locale': 'en-IE', 'clock': '24h'})
        for bad in ({'locale': 'x'}, {'clock': '13h'}, {}):
            with self.assertRaises(ValueError):
                locale_prefs.settings(bad)

    def test_spans_and_ranges(self):
        self.use(locale='en-US')
        self.assertEqual(locale_prefs.span_text(dt.date(2026, 10, 19), dt.date(2026, 10, 23)), 'Oct 19–23')
        self.assertEqual(locale_prefs.range_text(AFTERNOON, AFTERNOON + dt.timedelta(hours=1)), '2:05 PM–3:05 PM')
        self.use(locale='en-GB')
        self.assertEqual(locale_prefs.span_text(dt.date(2026, 10, 19), dt.date(2026, 10, 23)), '19–23 Oct')
        self.assertEqual(locale_prefs.span_text(dt.date(2026, 10, 30), dt.date(2026, 11, 5)), '30 Oct – 5 Nov')

    def test_messages_follow_the_setting(self):
        self.use(locale='en-US')
        self.assertEqual(calendar_writes.when('2026-10-27T16:00:00+01:00', '2026-10-27T16:30:00+01:00', False),
                         'Tue, Oct 27, 2026, 4:00 PM to 4:30 PM')
        self.assertEqual(family._shown('2026-10-27T16:00:00'), 'Tue, Oct 27 4:00 PM')
        self.assertEqual(fleet_requests.how_text('email', 'Sam', '2026-10-23T10:12:00+00:00', dt.timezone.utc),
                         'emailed Sam, Fri 10:12 AM')
        self.use()
        self.assertEqual(calendar_writes.when('2026-10-27T16:00:00+01:00', '2026-10-27T16:30:00+01:00', False),
                         'Tue, Oct 27, 2026, 16:00 to 16:30')
        self.assertEqual(family.free_text(['2026-10-27T16:00:00+01:00', '2026-10-27T17:00:00+01:00']), 'Tue, Oct 27 16:00–17:00')


class SettingTest(unittest.TestCase):
    def setUp(self):
        self.dir = pathlib.Path(tempfile.mkdtemp())
        self.path = self.dir / 'config.json'
        self.path.write_text(json.dumps({'timezone': 'Europe/Brussels', 'other': 1}))
        self.app = assistant.App.__new__(assistant.App)
        self.app.config, self.app.config_path = json.loads(self.path.read_text()), self.path
        locale_prefs.configure({})

    def tearDown(self):
        locale_prefs.configure({})
        shutil.rmtree(self.dir)

    def test_the_owner_sets_region_and_time_format_and_it_is_saved(self):
        view = self.app.locale_view()
        self.assertIsNone(view['locale'])
        self.assertTrue(view['saveable'])
        view = self.app.set_locale({'locale': 'en-GB'})
        self.assertEqual((view['locale'], view['hour12'], view['date_locale']), ('en-GB', False, 'en-GB'))
        view = self.app.set_locale({'clock': '12h'})
        self.assertTrue(view['hour12'])
        saved = json.loads(self.path.read_text())
        self.assertEqual((saved['locale'], saved['clock'], saved['other']), ('en-GB', '12h', 1))
        self.assertEqual(locale_prefs.clock_text(AFTERNOON), '2:05 PM')
        with self.assertRaises(ValueError):
            self.app.set_locale({'locale': 'nowhere'})

    def test_without_a_config_file_it_cannot_be_saved(self):
        self.app.config_path = None
        self.assertFalse(self.app.locale_view()['saveable'])
        with self.assertRaises(ValueError):
            self.app.set_locale({'locale': 'en-GB'})


class InstallerTest(unittest.TestCase):
    def config(self, locale):
        values = {'owner_name': 'Alex Owner', 'timezone': 'Europe/Brussels', 'telegram_owner': '', 'tailscale_owner': 'alex@example.com',
                  'dashboard_host': 'machine.example.ts.net', 'connectors': 'none', 'email': '', 'gog_client': 'default',
                  'boundary': '', 'android_node_id': '', 'whatsapp_store': '', 'locale': locale}
        home = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, home)
        return installer.new_config(values, {}, installer.Paths(home))

    def test_signup_locale_reaches_a_new_machine(self):
        self.assertEqual(self.config('en-GB')['locale'], 'en-GB')
        self.assertNotIn('locale', self.config(''))
        self.assertNotIn('locale', self.config('not a locale'))
        self.assertEqual(installer.ENV['locale'], 'ASSISTANT_LOCALE')


@unittest.skipUnless(shutil.which('node'), 'needs node')
class DashboardTest(unittest.TestCase):
    """The dashboard's own helpers, run in node: the same strings as the server for the same setting."""
    def run_js(self, locale, script):
        html = (ROOT / 'dashboard.html').read_text()
        start = html.index("let DL='en-US',H12=false;")
        helpers = html[start:html.index('\n', html.index('const fmtDHM=', start))]
        cal = html[html.index('const calHourLabel='):].split('\n', 1)[0]
        code = helpers + '\n' + cal + f'\napplyLocale({json.dumps(locale)});const d=new Date(2026,9,24,14,5);\n' \
            + f'console.log(JSON.stringify({script}))'
        return json.loads(subprocess.run(['node', '-e', code], capture_output=True, text=True, check=True).stdout)

    def test_dashboard_times_follow_the_setting(self):
        locale_prefs.configure({'locale': 'en-US'})
        us = self.run_js(locale_prefs.view(), "[fmtHM(d),fmtDHM(d,{weekday:'short',day:'numeric',month:'short'}),calHourLabel(13),calHourLabel(0)]")
        self.assertEqual(us, ['2:05 PM', 'Sat, Oct 24, 2:05 PM', '1 PM', '12 AM'])
        locale_prefs.configure({'locale': 'en-GB'})
        gb = self.run_js(locale_prefs.view(), "[fmtHM(d),fmtDHM(d,{weekday:'short',day:'numeric',month:'short'}),calHourLabel(13)]")
        self.assertEqual(gb, ['14:05', 'Sat 24 Oct, 14:05', '13:00'])
        locale_prefs.configure({})
        legacy = self.run_js(None, "[fmtHM(d),fmtDHM(d,{weekday:'short',day:'numeric',month:'short'})]")
        self.assertEqual(legacy, ['14:05', 'Sat, Oct 24, 14:05'])

    def tearDown(self):
        locale_prefs.configure({})


if __name__ == '__main__':
    unittest.main()
