import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('assistant_connectors', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

ANDROID = {'id':'personal-android','node_id':'phone'}


class NewConnectors(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.store=a.Store(Path(self.tmp.name)/'test.sqlite3')
    def tearDown(self): self.tmp.cleanup()


    def test_direct_fallback_is_throttled_and_not_used_with_healthy_feed(self):
        account={**ANDROID,'direct_fallback':True}
        src=a.Android({},account)
        snapshot={'enabled':True,'connected':True,'count':0,'notifications':[]}
        with patch.object(src,'snapshot',return_value=snapshot) as called:
            a.sync_android_preferred(self.store,{},account,src)
            self.assertEqual(called.call_count,1)
            with self.assertRaises(a.SourceError):a.sync_android_preferred(self.store,{},account,src)
            self.assertEqual(called.call_count,1)
            state=self.store.checkpoint(account['id']);state['fallback_last_attempt']=(a.dt.datetime.fromisoformat(a.now())-a.dt.timedelta(seconds=599)).isoformat()
            self.store.commit_page(account['id'],state,[],record_sync=False)
            with self.assertRaises(a.SourceError):a.sync_android_preferred(self.store,{},account,src)
            self.assertEqual(called.call_count,1)
            with self.store.connect() as db:db.execute('INSERT INTO android_feed_health VALUES(1,?,NULL,NULL)',(a.now(),))
            a.sync_android_preferred(self.store,{},account,src)
            self.assertEqual(called.call_count,1)
        self.assertEqual(self.store.checkpoint(account['id'])['transport'],'existing_openclaw_feed')

    def test_healthy_feed_reconciliation_is_ten_minute_capped_and_key_deduplicated(self):
        account={**ANDROID,'direct_fallback':True,'reconcile_seconds':600}
        raw={'key':'native-key','packageName':'com.example','postTimeMs':100000,'title':'Sender','text':'Hello'}
        key=a.hashlib.sha256(raw['key'].encode()).hexdigest()
        envelope={'id':'native-first','at_ms':100000,'change':'posted','package_name':'com.example',
                  'notification_key_hash':key,'text':'Sender - Hello'}
        with self.store.connect() as db:
            db.execute('INSERT INTO android_feed_health VALUES(1,?,NULL,NULL)',(a.now(),))
            db.execute('INSERT INTO android_inbox VALUES(?,?,?)',(envelope['id'],json.dumps(envelope),'2020-01-01T00:00:00+00:00'))
        src=a.Android({},account)
        snapshot={'enabled':True,'connected':True,'count':1,'notifications':[raw]}
        with patch.object(src,'snapshot',return_value=snapshot) as read:
            a.sync_android_preferred(self.store,{},account,src)
            first=self.store.events([account['id']])[0]
            self.assertEqual(first['version'],1)  # Snapshot baseline is metadata, not new evidence.
            a.sync_android_preferred(self.store,{},account,src);self.assertEqual(read.call_count,1)
            state=self.store.checkpoint(account['id']);state['fallback_last_attempt']='2020-01-01T00:00:00+00:00'
            self.store.commit_page(account['id'],state,[],record_sync=False)
            raw['text']='Updated while forwarding missed it'
            a.sync_android_preferred(self.store,{},account,src)
        rows=self.store.events([account['id']]);self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['id'],first['id']);self.assertEqual(rows[0]['version'],first['version']+1)
        self.assertEqual(rows[0]['body'],raw['text'])
        self.assertEqual(self.store.checkpoint(account['id'])['transport'],'existing_feed_with_reconciliation')

    def test_recovery_snapshot_then_native_feed_share_one_exact_key(self):
        raw={'key':'native-key','packageName':'com.example','postTimeMs':100000,'title':'Sender','text':'Hello'}
        src=a.Android({},ANDROID)
        with patch.object(src,'snapshot',return_value={'enabled':True,'connected':True,'count':1,'notifications':[raw]}):
            a.sync_android(self.store,{},ANDROID,src,reconcile=True)
        first=self.store.events([ANDROID['id']])[0]
        envelope={'id':'native-following','at_ms':100001,'change':'posted','package_name':'com.example',
            'notification_key_hash':a.hashlib.sha256(raw['key'].encode()).hexdigest(),'text':'Sender - Updated'}
        with self.store.connect() as db:
            db.execute('INSERT INTO android_feed_health VALUES(1,?,NULL,NULL)',(a.now(),))
            db.execute('INSERT INTO android_inbox VALUES(?,?,?)',(envelope['id'],json.dumps(envelope),'2020-01-01T00:00:00+00:00'))
        a.sync_android_feed(self.store,{},ANDROID)
        rows=self.store.events([ANDROID['id']]);self.assertEqual(len(rows),1);self.assertEqual(rows[0]['id'],first['id'])
        self.assertEqual(rows[0]['body'],'Sender - Updated')

    def test_forwarded_inbox_commit_and_retry_dedup(self):
        envelope={'id':'queued-event','at_ms':100000,'change':'posted','package_name':'com.example',
                  'notification_key_hash':'hash','text':'Real preview'}
        with self.store.connect() as db:
            db.execute('INSERT INTO android_feed_health VALUES(1,?,NULL,NULL)',(a.now(),))
            db.execute('INSERT INTO android_inbox VALUES(?,?,?)',(envelope['id'],json.dumps(envelope),'2020-01-01T00:00:00+00:00'))
        a.sync_android_feed(self.store,{},ANDROID)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM android_inbox').fetchone()[0],0)
            db.execute('INSERT INTO android_inbox VALUES(?,?,?)',(envelope['id'],json.dumps(envelope),'2020-01-01T00:00:00+00:00'))
        a.sync_android_feed(self.store,{},ANDROID)
        with self.store.connect() as db:
            self.assertEqual(tuple(db.execute('SELECT count(*),max(version) FROM events').fetchone()),(1,1))

    def test_forwarded_failure_retains_inbox_for_replay(self):
        envelope={'id':'queued','at_ms':100000,'change':'posted','package_name':'com.example',
                  'notification_key_hash':'hash','text':'Preview'}
        with self.store.connect() as db:
            db.execute('INSERT INTO android_feed_health VALUES(1,?,NULL,NULL)',(a.now(),))
            db.execute('INSERT INTO android_inbox VALUES(?,?,?)',(envelope['id'],json.dumps(envelope),a.now()))
        with patch.object(self.store,'commit_page',side_effect=RuntimeError('interrupted')):
            with self.assertRaises(RuntimeError):a.sync_android_feed(self.store,{},ANDROID)
        with self.store.connect() as db:self.assertEqual(db.execute('SELECT count(*) FROM android_inbox').fetchone()[0],1)
        self.assertIsNone(self.store.checkpoint(ANDROID['id']))

    def test_forwarded_health_is_not_inferred_from_absence(self):
        with self.assertRaises(a.SourceError):a.sync_android_feed(self.store,{},ANDROID)
        with self.store.connect() as db:db.execute('INSERT INTO android_feed_health VALUES(1,?,NULL,NULL)',('2020-01-01T00:00:00+00:00',))
        with self.assertRaises(a.SourceError):a.sync_android_feed(self.store,{},ANDROID)
        self.assertIsNone(self.store.checkpoint(ANDROID['id']))

    def test_android_offline_does_not_claim_success_and_recovery_records_gap(self):
        src=a.Android({},ANDROID)
        with patch.object(src,'snapshot',side_effect=a.SourceError('android_offline')):
            with self.assertRaises(a.SourceError): a.sync_android(self.store,{},ANDROID,src)
        with self.store.connect() as db:
            row=db.execute('SELECT last_success FROM checkpoints').fetchone()
            self.assertIsNone(row[0]);self.assertEqual(db.execute('SELECT count(*) FROM sync_activity').fetchone()[0],0)
        with patch.object(src,'snapshot',return_value={'enabled':True,'connected':True,'count':0,'notifications':[]}):
            a.sync_android(self.store,{},ANDROID,src)
        checkpoint=self.store.checkpoint(ANDROID['id'])
        self.assertEqual(len(checkpoint['gaps']),1);self.assertNotIn('offline_since',checkpoint)

    def test_android_snapshot_permission_count_and_identity_fail_closed(self):
        src=a.Android({},ANDROID)
        for invalid in ({'enabled':False,'connected':True,'count':0,'notifications':[]},
                        {'enabled':True,'connected':True,'count':1,'notifications':[]}):
            with patch.object(src,'snapshot',return_value=invalid),self.assertRaises(a.SourceError):
                a.sync_android(self.store,{},ANDROID,src)
        with self.store.connect() as db:self.assertEqual(db.execute('SELECT count(*) FROM events').fetchone()[0],0)

    def test_app_name_is_persisted_for_agent_retrieval_not_only_dashboard(self):
        raw={'key':'k','packageName':'com.google.android.gm','postTimeMs':100000,'title':'Hi','text':'Preview'}
        event=a.android_event(ANDROID,raw)
        self.assertEqual(event['metadata']['app_name'],'Gmail')
        self.store.commit_page(ANDROID['id'],{},[event])
        with self.store.connect() as db:
            metadata=json.loads(db.execute('SELECT metadata FROM events').fetchone()[0])
            self.assertEqual(metadata['app_name'],'Gmail');self.assertEqual(metadata['package_name'],'com.google.android.gm')
        raw['packageName']='com.unknown.app'
        self.assertEqual(a.android_event(ANDROID,raw)['metadata']['app_name'],'com.unknown.app')

    def test_android_replay_edit_and_new_occurrence_are_distinct(self):
        raw={'key':'private key','packageName':'com.example.app','postTimeMs':100000,'title':'Hello','text':'First'}
        event=a.android_event(ANDROID,raw)
        self.store.commit_page(ANDROID['id'],{},[event]);self.store.commit_page(ANDROID['id'],{},[event])
        raw['text']='Edited';edited=a.android_event(ANDROID,raw)
        self.store.commit_page(ANDROID['id'],{},[edited])
        raw['postTimeMs']+=1;self.store.commit_page(ANDROID['id'],{},[a.android_event(ANDROID,raw)])
        with self.store.connect() as db:
            self.assertEqual(tuple(db.execute('SELECT count(*),max(version) FROM events').fetchone()),(2,2))
        self.assertNotIn('private key',a.encoded(edited));self.assertEqual(edited['metadata']['source_account'],'unknown')

    def test_android_code_omitted_and_self_notifications_excluded(self):
        raw={'key':'k','packageName':'sms','postTimeMs':100000,'title':'Verification code 123456','text':'Use 123456'}
        event=a.android_event(ANDROID,raw);self.assertNotIn('123456',a.encoded(event))
        src=a.Android({},ANDROID)
        raw['packageName']='ai.openclaw.app'
        with patch.object(src,'snapshot',return_value={'enabled':True,'connected':True,'count':1,'notifications':[raw]}):
            a.sync_android(self.store,{},ANDROID,src)
        self.assertEqual(self.store.events([ANDROID['id']]),[])

if __name__=='__main__':unittest.main()
