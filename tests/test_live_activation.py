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

    def test_a_new_install_is_looked_at_often_while_its_first_mail_comes_in(self):
        self.assertEqual(self.app.review_tick(), a.REVIEW_TICK_SECONDS)  # nothing in yet
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
