"""Reviews turned on while the first look runs apply without restarting the app (App.follow_config, LIVE_CONFIG): the
hosting agent's reviews on restarted it 44 s into a first look (2026-11-04). And on a new install the review worker looks
every few seconds while its first mail comes in, so the first look starts right after the AI sign-in. No Gateway."""
import datetime as dt, importlib.util, json, os, tempfile, unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('live_activation_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)


def mail(source_id, hours_ago=2):
    when = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours_ago)).isoformat()
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': when, 'title': 'Hello',
            'body': 'Text', 'metadata': {'from': 'Sam <sam@example.org>', 'to': 'me@example.com', 'thread_id': source_id}, 'deleted': False}


class LiveActivation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'config.json'
        self.config = {'accounts': [{'id': 'work', 'service': 'gmail'}], 'port': 8787, 'delivery_enabled': False,
                       'review_worker': {'enabled': False}}
        self.path.write_text(json.dumps(self.config))
        self.app = object.__new__(a.App)
        self.app.config, self.app.config_path = dict(self.config), self.path
        self.app.config_stamp = self.path.stat().st_mtime_ns
        self.app.store = a.Store(Path(self.temp.name) / 'events.sqlite')

    def write(self, **changes):
        saved = {**json.loads(self.path.read_text()), **changes}
        self.path.write_text(json.dumps(saved))
        stamp = self.path.stat().st_mtime_ns + 1_000_000
        os.utime(self.path, ns=(stamp, stamp))

    def test_reviews_on_apply_while_the_app_runs(self):
        self.assertFalse(self.app.follow_config())  # nothing changed since it started
        self.write(delivery_enabled=True, review_worker={'enabled': True}, port=9999)
        with self.assertLogs(a.LOG, 'INFO'):
            self.assertTrue(self.app.follow_config())
        self.assertEqual((self.app.config['delivery_enabled'], self.app.config['review_worker']), (True, {'enabled': True}))
        self.assertEqual(self.app.config['port'], 8787)  # only the settings it can take live
        self.assertFalse(self.app.follow_config())  # once
        self.assertEqual(set(a.LIVE_CONFIG), {'delivery_enabled', 'review_worker'})  # what the hosting agent checks

    def test_an_unreadable_file_changes_nothing(self):
        self.path.write_text('{')
        stamp = self.path.stat().st_mtime_ns + 1_000_000
        os.utime(self.path, ns=(stamp, stamp))
        self.assertFalse(self.app.follow_config())
        self.assertEqual(self.app.config['review_worker'], {'enabled': False})

    def started(self):
        """Collectors the app starts, recorded instead of run."""
        self.app.stop = a.threading.Event()
        self.app.store.exclusions, self.app.store.owner_user_ids = {}, set()
        self.app.store.accounts = self.app.config['accounts']
        begun = []
        self.app.collector = lambda account: begun.append(account['id'])
        self.app.ability_checker = lambda account: begun.append('check:' + account['id'])
        return begun

    def test_a_new_account_starts_syncing_without_a_restart(self):
        # The account page connected Intercom and the restart after it left the Connections page on "Can't reach your
        # Machine" (2026-11-10). A new account now joins the running app: its settings, its collector, no restart.
        begun = self.started()
        self.app.config['credentials'] = {'api-token': '/keys/api'}
        intercom = {'id': 'work-intercom', 'service': 'intercom', 'transport': 'api', 'credential': 'intercom', 'boundary': 'work:Acme'}
        self.write(accounts=[*self.config['accounts'], intercom], credentials={'api-token': '/keys/api', 'intercom': '/keys/intercom'},
                   intercom_replies={'work-intercom': True})
        with self.assertLogs(a.LOG, 'INFO'):
            answer = self.app.action('accounts_follow', {})
        self.assertEqual(answer, {'accounts': ['work', 'work-intercom'], 'taken': True})
        for _ in range(100):
            if begun:
                break
            a.time.sleep(0.01)
        self.assertEqual(begun, ['work-intercom'])
        self.assertIs(self.app.store.accounts, self.app.config['accounts'])
        self.assertEqual(self.app.config['credentials'], {'api-token': '/keys/api', 'intercom': '/keys/intercom'})
        self.assertEqual(self.app.config['intercom_replies'], {'work-intercom': True})
        self.assertEqual(self.app.action('accounts_follow', {}), {'accounts': ['work', 'work-intercom'], 'taken': True})
        a.time.sleep(0.05)
        self.assertEqual(begun, ['work-intercom'])  # once

    def test_anything_but_a_plain_addition_still_restarts(self):
        begun = self.started()
        self.app.config['credentials'] = {'api-token': '/keys/api'}
        for change in ({'accounts': [{'id': 'work', 'service': 'gmail', 'boundary': 'personal'}]},  # an account edited
                       {'accounts': []},  # removed
                       {'accounts': [*self.config['accounts'], {'id': 'chat', 'service': 'whatsapp'}]},  # its own process
                       {'accounts': [*self.config['accounts'], {'id': 'new', 'service': 'rss'}], 'port': 9999},  # a setting changed
                       {'accounts': [*self.config['accounts'], {'id': 'new', 'service': 'rss'}], 'credentials': {'api-token': '/keys/other'}}):
            with self.subTest(change=change):
                self.path.write_text(json.dumps({**self.config, 'credentials': {'api-token': '/keys/api'}}))
                self.write(**change)
                answer = self.app.action('accounts_follow', {})
                self.assertFalse(answer['taken'])
                self.assertEqual(answer['accounts'], ['work'])
        self.assertEqual(begun, [])
        self.assertEqual(self.app.config['port'], 8787)

    def test_a_file_being_written_is_read_again(self):
        self.started()
        self.path.write_text('{"accounts": [')
        stamp = self.path.stat().st_mtime_ns + 1_000_000
        os.utime(self.path, ns=(stamp, stamp))
        self.assertFalse(self.app.follow_config())
        self.path.write_text(json.dumps({**self.config, 'accounts': [*self.config['accounts'], {'id': 'feed', 'service': 'rss'}]}))
        os.utime(self.path, ns=(stamp, stamp))  # the same time stamp, now whole
        with self.assertLogs(a.LOG, 'INFO'):
            self.assertTrue(self.app.follow_config())
        self.assertEqual([x['id'] for x in self.app.config['accounts']], ['work', 'feed'])

    def test_a_new_install_is_looked_at_often_while_its_first_mail_comes_in(self):
        self.app.config['accounts'] = []
        self.assertEqual(self.app.review_tick(), a.REVIEW_TICK_SECONDS)  # nothing connected yet
        self.app.config['accounts'] = [{'id': 'work', 'service': 'gmail'}]
        # Just connected, its first page not in yet: already looked at often, so the first look starts as the page lands
        # (a 15 s tick set before it held the first look up to 15 s, agent users 2026-11-08)
        self.assertEqual(self.app.review_tick(), a.FIRST_LOOK_TICK_SECONDS)
        with self.app.store.connect() as db:
            db.execute("UPDATE milestones SET at='2026-01-01T00:00:00+00:00' WHERE name='tracking_since'")
        self.assertEqual(self.app.review_tick(), a.REVIEW_TICK_SECONDS)  # an older install: the usual pace
        with self.app.store.connect() as db:
            db.execute("UPDATE milestones SET at=? WHERE name='tracking_since'", (a.now(),))
        self.app.store.commit_page('work', {}, [mail('m1')])
        self.assertEqual(self.app.review_tick(), a.FIRST_LOOK_TICK_SECONDS)  # mail is in: the first look starts at once
        self.app.config['review_worker'] = {'enabled': False, 'first_look': False}
        self.assertEqual(self.app.review_tick(), a.REVIEW_TICK_SECONDS)  # turned off by the owner
        self.app.config['review_worker'] = {'enabled': True}
        with self.app.store.connect() as db:
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,finished_at) VALUES('r','ok',?,?,?)", (a.now(),) * 3)
        self.assertEqual(self.app.review_tick(), a.REVIEW_TICK_SECONDS)  # it reviewed before


if __name__ == '__main__':
    unittest.main()
