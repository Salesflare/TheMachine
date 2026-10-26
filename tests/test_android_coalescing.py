import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('assistant_coalescing', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
ACCOUNT = {'id':'personal-android'}


class AndroidCoalescing(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name)/'events.sqlite')

    def queue(self, eid, second, text='Preview', key='key', change='posted', received=None):
        stamp = f'2026-10-09T22:00:{second:02d}+00:00'
        envelope = {'id':eid, 'at_ms':int(a.dt.datetime.fromisoformat(stamp).timestamp()*1000),
                    'text':text, 'package_name':'com.openai.chatgpt',
                    'notification_key_hash':key, 'change':change}
        with self.store.connect() as db:
            db.execute('INSERT INTO android_inbox VALUES(?,?,?)',(eid,json.dumps(envelope),received or stamp))

    def sync(self, stamp='2026-10-09T22:02:00+00:00'):
        with patch.object(a,'now',return_value=stamp):
            with self.store.connect() as db:
                db.execute('INSERT OR REPLACE INTO android_feed_health VALUES(1,?,NULL,NULL)',(stamp,))
            return a.sync_android_feed(self.store,{},ACCOUNT)

    def test_rapid_updates_settle_then_merge_latest_and_removal_stays_quiet(self):
        self.queue('one',0,'Starting')
        self.queue('two',5,'Finished')
        self.sync('2026-10-09T22:00:30+00:00')
        self.assertEqual(self.store.events([ACCOUNT['id']]),[])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM android_inbox').fetchone()[0],2)
        self.sync()
        original = self.store.events([ACCOUNT['id']])[0]
        self.assertEqual(original['body'],'Finished')
        self.assertEqual(original['metadata']['app_name'],'ChatGPT')
        self.assertEqual(original['metadata']['updates_merged'],2)
        self.queue('same',6,'Finished')
        self.sync()
        self.assertEqual(self.store.events([ACCOUNT['id']])[0]['version'],original['version'])
        review = self.store.begin_analysis([ACCOUNT['id']]);self.store.finish_analysis(review['analysis_id'])
        self.queue('removed',7,'',change='removed')
        self.sync()
        row = self.store.events([ACCOUNT['id']])[0]
        self.assertEqual(row['body'],'Finished')
        self.assertFalse(row['metadata']['is_active'])
        self.assertEqual(row['version'],original['version'])
        self.assertEqual(self.store.events([ACCOUNT['id']],pending=True),[])

    def test_real_text_update_versions_same_signal_new_episode_and_key_are_distinct(self):
        self.queue('first',0,'Old');self.sync()
        initial=self.store.events([ACCOUNT['id']])[0]
        self.queue('changed',1,'New');self.sync()
        changed=self.store.events([ACCOUNT['id']])[0]
        self.assertEqual(changed['id'],initial['id'])
        self.assertEqual(changed['version'],initial['version']+1)
        self.queue('removed',2,change='removed')
        self.queue('new-episode',3,'Separate notification')
        self.queue('other-key',4,'Another message',key='other')
        self.sync()
        self.assertEqual(len(self.store.events([ACCOUNT['id']])),3)

    def test_replay_and_transaction_failure_cannot_acknowledge_early_or_duplicate(self):
        self.queue('first',0);self.sync()
        self.queue('first',0);self.sync()
        self.assertEqual(len(self.store.events([ACCOUNT['id']])),1)
        self.queue('changed',1,'New')
        original=self.store.record_sync_activity
        def fail(*args,**kwargs): raise RuntimeError('interrupted after event update')
        with patch.object(self.store,'record_sync_activity',side_effect=fail):
            with self.assertRaises(RuntimeError):self.sync()
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM android_inbox').fetchone()[0],1)
        self.assertEqual(self.store.events([ACCOUNT['id']])[0]['body'],'Preview')
        self.sync()
        self.assertEqual(self.store.events([ACCOUNT['id']])[0]['body'],'New')

    def test_continuous_updates_have_five_minute_cap_and_unknown_removal_is_not_signal(self):
        self.queue('oldest',0,received='2026-10-09T21:55:00+00:00')
        self.queue('latest',1,'Latest',received='2026-10-09T22:01:50+00:00')
        self.queue('clear-unknown',2,change='removed',key='unknown')
        self.sync()
        rows=self.store.events([ACCOUNT['id']])
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['body'],'Latest')

    def test_same_millisecond_clear_and_repost_stay_distinct(self):
        self.queue('post',0,'First');self.queue('clear',0,change='removed');self.queue('second',0,'Second')
        self.sync()
        self.assertEqual({r['body'] for r in self.store.events([ACCOUNT['id']])},{'First','Second'})

    def test_busy_key_does_not_hide_clear_or_another_key_after_100_updates(self):
        for i in range(105):self.queue('progress'+str(i),0,'Progress',received='2026-10-09T22:01:55+00:00')
        self.queue('finished',1,'Done',received='2026-10-09T22:01:56+00:00')
        self.queue('clear',2,change='removed',received='2026-10-09T22:01:57+00:00')
        self.queue('quiet',3,'Other',key='other')
        self.sync()
        rows=self.store.events([ACCOUNT['id']]);self.assertEqual({r['body'] for r in rows},{'Done','Other'})
        with self.store.connect() as db:self.assertEqual(db.execute('SELECT count(*) FROM android_inbox').fetchone()[0],0)

    def test_offline_bridge_still_commits_captured_inbox_and_receipts(self):
        self.queue('captured',0)
        with patch.object(a,'now',return_value='2026-10-09T22:02:00+00:00'):
            with self.assertRaises(a.SourceError):a.sync_android_feed(self.store,{},ACCOUNT)
        self.assertEqual(len(self.store.events([ACCOUNT['id']])),1)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM android_inbox').fetchone()[0],0)
            self.assertEqual(db.execute('SELECT count(*) FROM android_receipts').fetchone()[0],1)
        self.assertIn('feed_unavailable_since',self.store.checkpoint(ACCOUNT['id']))

    def test_unknown_removal_replay_is_durably_acknowledged(self):
        self.queue('clear',0,change='removed');self.sync()
        with self.store.connect() as db:self.assertEqual(db.execute('SELECT count(*) FROM android_receipts').fetchone()[0],1)
        self.queue('clear',0,change='removed');self.sync()
        self.assertEqual(self.store.events([ACCOUNT['id']]),[])

    def test_history_cleanup_preserves_latest_text_accounts_checkpoint_search_and_is_repeatable(self):
        originals=[]
        for eid, text, change, second in [('one','First','posted',0),('two','Latest','posted',1),('removed','','removed',2),('new','Separate','posted',3)]:
            originals.append({'account_id':ACCOUNT['id'],'source_id':'forwarded:'+eid,'kind':'android.notification',
                'occurred_at':f'2026-10-09T22:00:{second:02d}+00:00','title':text,'body':text,'deleted':False,
                'metadata':{'transport':'existing_openclaw_feed','notification_key_hash':'key','package_name':'com.openai.chatgpt','change':change}})
        self.store.commit_page(ACCOUNT['id'],{'cursor':'retained'},originals)
        other={**originals[0],'account_id':'other'};self.store.commit_page('other',{},[other])
        with patch.object(a,'now',return_value='2026-10-09T22:00:04+00:00'):
            result=self.store.coalesce_android_history(ACCOUNT)
        self.assertEqual(result,{'observations_before':4,'signals_after':2,'removed':2})
        self.assertEqual(self.store.checkpoint(ACCOUNT['id']),{'cursor':'retained'})
        rows=self.store.events([ACCOUNT['id']]);self.assertEqual({r['body'] for r in rows},{'Latest','Separate'})
        self.assertEqual(len(self.store.events(['other'])),1)
        self.assertEqual(self.store.events([ACCOUNT['id']],query='First'),[])
        self.assertEqual(self.store.coalesce_android_history(ACCOUNT)['removed'],0)
        with self.store.connect() as db:db.execute("INSERT INTO event_search(event_search,rank) VALUES('integrity-check',1)")


if __name__ == '__main__':unittest.main()
