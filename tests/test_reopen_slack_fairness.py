import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import unittest.mock
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402

spec=importlib.util.spec_from_file_location('assistant_fairness',Path(__file__).parent.parent.joinpath('assistant.py'))
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
from machine.app import sync as slack_sync  # noqa: E402
from machine.sources import slack as slack_source  # noqa: E402


class ReopenAndSlack(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.store=a.Store(Path(self.temp.name)/'events.sqlite')

    def test_reopen_preserves_draft_and_history_and_edits_one_card_idempotently(self):
        event={'account_id':'work','source_id':'one','kind':'gmail.message','occurred_at':a.now(),
               'title':'Evidence','body':'Evidence','metadata':{},'deleted':False}
        self.store.commit_page('work',{},[event]);eid=self.store.events(['work'])[0]['id']
        sid=self.store.suggest('topic','Prepare reply','A short suggestion',[eid])['id']
        self.store.decide(sid,'accept','','accept','dashboard');self.store.prepare(sid,'The prepared reply')
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='123' WHERE suggestion_id=?",(sid,))
        self.store.decide(sid,'complete','Actually finished','done','dashboard')
        with self.assertRaises(ValueError):self.store.decide(sid,'reopen','','agent','agent')
        self.assertEqual(self.store.decide(sid,'reopen','','owner','dashboard')['status'],'prepared')
        self.assertTrue(self.store.decide(sid,'reopen','','owner','dashboard')['duplicate'])
        self.assertTrue(self.store.decide(sid,'reopen','','double-click','dashboard')['duplicate'])
        state=self.store.snapshot([])
        self.assertEqual(state['suggestions'][0]['body'],'The prepared reply')
        self.assertEqual(len(state['decisions']),3)
        self.assertEqual(state['deliveries'][0]['message_id'],'123')
        self.assertEqual(state['deliveries'][0]['status'],'sent')
        with patch_everywhere(a,'telegram',return_value={'messageId':'123'}) as telegram:
            a.deliver(self.store,{})
        self.assertEqual(telegram.call_args.args[2],'edit')
        self.assertEqual(telegram.call_count,1)

    def test_legacy_completion_restores_accepted_and_pending_cannot_reopen(self):
        self.store.commit_page('work',{},[{'account_id':'work','source_id':'one','kind':'gmail.message',
            'occurred_at':a.now(),'title':'Real','body':'Real','metadata':{},'deleted':False}])
        sid=self.store.suggest('topic','Reply','Reply',[self.store.events(['work'])[0]['id']])['id']
        with self.assertRaises(ValueError):self.store.decide(sid,'reopen','','bad','dashboard')
        with self.store.connect() as db:db.execute("UPDATE suggestions SET status='completed' WHERE id=?",(sid,))
        self.assertEqual(self.store.decide(sid,'reopen','','owner','dashboard')['status'],'accepted')

    def test_agent_cannot_spoof_dashboard_source_for_reopen(self):
        app=object.__new__(a.App);app.config={'accounts':[]};app.store=self.store
        with self.assertRaisesRegex(ValueError,'owner dashboard'):
            app.action('decide',{'suggestion_id':'id','choice':'reopen','source':'dashboard','decision_id':'agent'})

    def test_incremental_rotates_one_old_thread_and_keeps_new_channel_messages(self):
        account={'id':'slack','fair_incremental':True,'slack_host':'example.slack.com'}
        channels=[{'id':'C1','name':'team','type':'channel','threads':['1001.000001','1002.000001','1003.000001'],
                   'last_scan':'2000.000000','next_full':a.time.time()+86400},
                  {'id':'C2','name':'other','type':'channel','threads':[], 'last_scan':'2000.000000',
                   'next_full':a.time.time()+86400}]
        state={'mode':'incremental','phase':'scan','after':'1000.000000','channels':channels,'index':0,
               'next_discovery':a.time.time()+86400}
        self.store.commit_page('slack',state,[])
        calls=[]
        class Source:
            def profile(self):pass
            def get(self,method,params):
                calls.append((method,params.copy()))
                if method=='conversations.history' and params['channel']=='C2':
                    return {'messages':[{'ts':'3000.000001','text':'A newly arrived message'}]}
                return {'messages':[]}
        source=Source();config={'slack_thread_retention_days':10**6}  # epoch-era fixture timestamps
        a.sync_slack(self.store,config,account,source)
        scan=self.store.checkpoint('slack')['scan'];self.assertEqual(scan['threads'],['1001.000001'])
        a.sync_slack(self.store,config,account,source)
        cp=self.store.checkpoint('slack');self.assertEqual(cp['index'],1)
        self.assertEqual(cp['channels'][0]['threads'],channels[0]['threads'])
        a.sync_slack(self.store,config,account,source)
        self.assertEqual(self.store.events(['slack'])[0]['body'],'A newly arrived message')
        # The round is done and both conversations rest: nothing is read until one is due again.
        reads=len(calls)
        self.assertFalse(a.sync_slack(self.store,config,account,source)['more'])
        self.assertEqual(len(calls),reads)
        cp=self.store.checkpoint('slack')
        self.assertGreater(cp['channels'][1]['due'],a.time.time()+3000)  # C2 just had a message: within the hour
        for c in cp['channels']:c['due']=0
        self.store.commit_page('slack',cp,[])
        a.sync_slack(self.store,config,account,source)
        self.assertEqual(self.store.checkpoint('slack')['scan']['threads'],['1002.000001'])

    def test_quiet_conversations_rest_and_dms_are_read_only_with_news(self):
        account={'id':'slack','fair_incremental':True,'slack_host':'example.slack.com'}
        now=a.time.time()
        channels=[{'id':'D1','name':'DM U2','type':'dm','threads':[],'last_scan':f'{now-60:.6f}','next_full':now+86400,'last_activity':now-3600},
                  {'id':'D2','name':'DM U3','type':'dm','threads':[],'last_scan':f'{now-60:.6f}','next_full':now+86400,'last_activity':now-3600},
                  {'id':'C1','name':'quiet','type':'channel','threads':[],'last_scan':f'{now-60:.6f}','next_full':now+86400,'due':now+3600}]
        self.store.commit_page('slack',{'mode':'incremental','phase':'scan','after':'1000.000000','channels':channels,'index':0,
                                        'next_discovery':now+86400},[])
        calls=[]
        class Source(a.Slack):
            def __init__(self):pass
            def profile(self):pass
            def get(self,method,params):
                calls.append((method,params['channel']))
                if method=='conversations.info':
                    return {'channel':{'latest':{'ts':f'{now-3600:.6f}' if params['channel']=='D1' else f'{now-10:.6f}'}}}
                return {'messages':[{'ts':f'{now-10:.6f}','text':'New','user':'U3'}]}
        source=Source()
        names=patch_everywhere(a,'remember_slack_names');names.start();self.addCleanup(names.stop)
        a.sync_slack(self.store,{},account,source)  # D1 has nothing new; D2 does
        self.assertEqual(calls,[('conversations.info','D1'),('conversations.info','D2'),('conversations.history','D2')])
        while a.sync_slack(self.store,{},account,source)['more']:pass
        self.assertNotIn(('conversations.history','D1'),calls)
        self.assertNotIn(('conversations.history','C1'),calls)  # not due for another hour
        cp=self.store.checkpoint('slack')
        self.assertEqual(cp['index'],0)
        self.assertAlmostEqual(cp['channels'][1]['last_activity'],now-10,places=3)

    def test_a_dm_that_cannot_be_opened_does_not_block_the_others(self):
        # conversations.info said channel_not_found for one direct message, and every sync failed on it (2026-11-09).
        account={'id':'slack','fair_incremental':True,'slack_host':'example.slack.com'}
        now=a.time.time()
        channels=[{'id':'D1','name':'DM U2','type':'dm','threads':[],'last_scan':f'{now-60:.6f}','next_full':now+86400,'last_activity':now-3600},
                  {'id':'D2','name':'DM U3','type':'dm','threads':[],'last_scan':f'{now-60:.6f}','next_full':now+86400,'last_activity':now-3600}]
        self.store.commit_page('slack',{'mode':'incremental','phase':'scan','after':'1000.000000','channels':channels,'index':0,
                                        'next_discovery':now+86400},[])
        calls=[]
        class Source(a.Slack):
            def __init__(self):pass
            def profile(self):pass
            def get(self,method,params):
                calls.append((method,params['channel']))
                if method=='conversations.info':
                    if params['channel']=='D1':raise a.SourceError('slack_channel_not_found:conversations.info')
                    return {'channel':{'latest':{'ts':f'{now-10:.6f}'}}}
                return {'messages':[{'ts':f'{now-10:.6f}','text':'New','user':'U3'}]}
        names=patch_everywhere(a,'remember_slack_names');names.start();self.addCleanup(names.stop)
        while a.sync_slack(self.store,{},account,Source())['more']:pass
        self.assertIn(('conversations.history','D2'),calls)
        self.assertEqual(sum(c==('conversations.info','D1') for c in calls),1)  # it rests, not asked again each sync
        cp=self.store.checkpoint('slack')
        self.assertEqual(cp['channels'][0]['error'],'slack_channel_not_found')
        self.assertGreater(cp['channels'][0]['due'],now)
        # Any other failure still stops the sync, as before.
        cp['channels'][0]['due']=0
        self.store.commit_page('slack',cp,[])
        class Down(Source):
            def get(self,method,params):raise a.SourceError('network:TimeoutError:conversations.info')
        with self.assertRaises(a.SourceError):a.sync_slack(self.store,{},account,Down())

    def test_one_dm_check_timing_out_does_not_fail_the_sync(self):
        # conversations.info timed out for one direct message and the whole sync failed (2026-11-11).
        account={'id':'slack','fair_incremental':True,'slack_host':'example.slack.com'}
        now=a.time.time()
        channels=[{'id':'D1','name':'DM U2','type':'dm','threads':[],'last_scan':f'{now-60:.6f}','next_full':now+86400,'last_activity':now-3600},
                  {'id':'D2','name':'DM U3','type':'dm','threads':[],'last_scan':f'{now-60:.6f}','next_full':now+86400,'last_activity':now-3600}]
        self.store.commit_page('slack',{'mode':'incremental','phase':'scan','after':'1000.000000','channels':channels,'index':0,
                                        'next_discovery':now+86400},[])
        calls=[]
        class Source(a.Slack):
            def __init__(self):pass
            def profile(self):pass
            def get(self,method,params):
                calls.append((method,params['channel']))
                if method=='conversations.info':
                    if params['channel']=='D1':raise a.SourceError('network:TimeoutError:conversations.info')
                    return {'channel':{'latest':{'ts':f'{now-10:.6f}'}}}
                return {'messages':[{'ts':f'{now-10:.6f}','text':'New','user':'U3'}]}
        names=patch_everywhere(a,'remember_slack_names');names.start();self.addCleanup(names.stop)
        while a.sync_slack(self.store,{},account,Source())['more']:pass
        self.assertIn(('conversations.history','D2'),calls)
        cp=self.store.checkpoint('slack')
        self.assertNotIn('error',cp['channels'][0])  # not set aside: checked again shortly
        self.assertLessEqual(cp['channels'][0]['due'],a.time.time()+slack_source.SLACK_HICCUP_REST)
        # A rate limit still stops the sync: it waits for Slack's Retry-After.
        cp['channels'][0]['due']=0;cp['channels'][1]['due']=0
        self.store.commit_page('slack',cp,[])
        class Limited(Source):
            def get(self,method,params):
                if method=='conversations.info' and params['channel']=='D1':raise a.SourceError('slack:conversations.info',429,60)
                return super().get(method,params)
        with self.assertRaises(a.SourceError):a.sync_slack(self.store,{},account,Limited())

    def test_a_users_info_hiccup_after_a_passed_check_does_not_fail_the_sync(self):
        # Slack answered internal_error to users.info for half an hour and every sync failed on the identity check (2026-11-11).
        account={'id':'slack','team_id':'T1','user_id':'U1','email':'owner@example.com'}
        answers={'users.info':[]}
        class Source(a.Slack):
            def get(self,method,params=None):
                if method=='auth.test':return {'team_id':'T1','user_id':'U1'}
                if answers['users.info']:raise answers['users.info'].pop(0)
                return {'user':{'profile':{'email':'Owner@example.com'}}}
        source=Source({},account)
        hiccup=a.SourceError('slack_internal_error:users.info')
        answers['users.info']=[hiccup]
        with self.assertRaises(a.SourceError):source.profile()  # never checked yet: fails closed
        source.profile()  # passes
        source.verified_until=0
        for error in (hiccup,a.SourceError('network:TimeoutError:users.info'),a.SourceError('slack:users.info',503)):
            answers['users.info']=[error];source.profile()  # Slack or the network: the reads go on
            self.assertEqual(source.verified_until,0)  # and the next sync checks again
        for error in (a.SourceError('slack_invalid_auth:users.info'),a.SourceError('slack:users.info',429,60)):
            answers['users.info']=[error]
            with self.assertRaises(a.SourceError):source.profile()
        source.email_verified_at-=source.EMAIL_GRACE+1
        answers['users.info']=[hiccup]
        with self.assertRaises(a.SourceError):source.profile()  # a check long ago carries nothing
        class Other(Source):
            def get(self,method,params=None):
                return {'user':{'profile':{'email':'someone@example.com'}}} if method=='users.info' else super().get(method,params)
        other=Other({},account);other.email_verified_at=a.time.monotonic()
        with self.assertRaisesRegex(a.SourceError,'account_identity_mismatch'):other.profile()  # a wrong email still fails

    def test_a_busy_channel_is_read_before_a_daily_batch_of_quiet_conversations(self):
        # Quiet conversations all come due for their daily read at about the same time. Walking the list in order
        # spent every read on them (one every few minutes) while a busy channel further down waited for hours.
        account={'id':'slack','fair_incremental':True,'slack_host':'example.slack.com'}
        now=a.time.time()
        quiet=[{'id':f'G{i}','name':f'quiet {i}','type':'group','threads':[],'last_scan':f'{now-90000:.6f}',
                'next_full':now+86400,'due':now-7200} for i in range(5)]
        dead_dm={'id':'D9','name':'DM U9','type':'dm','threads':[],'last_scan':f'{now-90000:.6f}',
                 'next_full':now-3600,'due':now-7200}
        busy={'id':'C1','name':'busy','type':'channel','threads':[],'last_scan':f'{now-5400:.6f}',
              'next_full':now+86400,'last_activity':now-5400,'due':now-1800}
        self.store.commit_page('slack',{'mode':'incremental','phase':'scan','after':f'{now-30*86400:.6f}',
                                        'channels':quiet+[dead_dm,busy],'index':0,'next_discovery':now+86400},[])
        calls=[]
        class Source(a.Slack):
            def __init__(self):pass
            def profile(self):pass
            def get(self,method,params):
                calls.append((method,params['channel']))
                if method=='conversations.info':
                    return {'channel':{'latest':{'ts':f'{now-40*86400:.6f}'}}}
                return {'messages':[{'ts':f'{now-60:.6f}','text':'A new message','user':'U3'}] if params['channel']=='C1' else []}
        names=patch_everywhere(a,'remember_slack_names');names.start();self.addCleanup(names.stop)
        a.sync_slack(self.store,{},account,Source())
        reads=[c for c in calls if c[0]=='conversations.history']
        self.assertEqual(reads,[('conversations.history','C1')])
        self.assertEqual([e['body'] for e in self.store.events(['slack'])],['A new message'])
        # The direct message had nothing in the window: its daily full read is a free check, not a history read.
        while a.sync_slack(self.store,{},account,Source())['more']:pass
        self.assertNotIn(('conversations.history','D9'),calls)
        self.assertEqual(sum(c==('conversations.info','D9') for c in calls),1)
        cp=self.store.checkpoint('slack')
        self.assertGreater(cp['channels'][5]['next_full'],now+80000)
        self.assertEqual({c[1] for c in calls if c[0]=='conversations.history'},{'C1','G0','G1','G2','G3','G4'})

    def test_failed_thread_page_is_preserved_without_starving_other_channels(self):
        account={'id':'slack','fair_incremental':True,'slack_host':'example.slack.com'}
        channels=[{'id':'C1','name':'one','type':'channel','last_scan':'2000.000000','threads':['1001.000001']},
                  {'id':'C2','name':'two','type':'channel','last_scan':'2000.000000','threads':[]}]
        scan={'phase':'threads','oldest':'1000.000000','latest':'3000.000000','full':False,
              'threads':['1001.000001'],'known_threads':['1001.000001'],'thread_index':0,'thread_start':0,'cursor':'saved-page'}
        self.store.commit_page('slack',{'mode':'incremental','phase':'scan','after':'1000.000000','index':0,
            'channels':channels,'scan':scan,'next_discovery':a.time.time()+86400},[])
        class Broken:
            def profile(self):pass
            def get(self,*args):raise a.SourceError('network:TimeoutError:conversations.replies')
        with self.assertRaises(a.SourceError):a.sync_slack(self.store,{},account,Broken())
        state=self.store.checkpoint('slack')
        self.assertEqual(state['index'],1)
        self.assertNotIn('scan',state)
        saved=state['channels'][0]['deferred_thread']
        self.assertEqual(saved['cursor'],'saved-page')
        self.assertEqual(saved['latest'],'3000.000000')
        self.assertEqual(saved['ts'],'1001.000001')
        state['index']=0
        saved['retry_at']=0
        self.store.commit_page('slack',state,[],record_sync=False)
        calls=[]
        class Healthy:
            def profile(self):pass
            def get(self,method,params):calls.append((method,params.copy()));return {'messages':[]}
        a.sync_slack(self.store,{},account,Healthy())
        a.sync_slack(self.store,{},account,Healthy())
        self.assertEqual(calls[-1][1]['cursor'],'saved-page')
        self.assertEqual(calls[-1][1]['oldest'],'1000.000000')
        self.assertEqual(calls[-1][1]['latest'],'3000.000000')
        self.assertNotIn('deferred_thread',self.store.checkpoint('slack')['channels'][0])


class RefusedConversation(unittest.TestCase):
    """A conversation Slack won't let the owner read (they left it, or were removed) says so and rests; the others are
    read all the same. It used to stay the most overdue one, so every sync read it again and nothing else (2026-11-09)."""

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.store=a.Store(Path(self.temp.name)/'events.sqlite')
        self.account={'id':'slack','user_id':'U1','slack_host':'example.slack.com'}
        self.now=now=a.time.time()
        self.channels=[{'id':'C1','name':'left','type':'channel','threads':[],'last_scan':f'{now-7200:.6f}','next_full':now+86400,
                        'last_activity':now-3600,'due':now-60},
                       {'id':'C2','name':'busy','type':'channel','threads':[],'last_scan':f'{now-7200:.6f}','next_full':now+86400,
                        'last_activity':now-3600,'due':now-30}]
        names=patch_everywhere(a,'remember_slack_names');names.start();self.addCleanup(names.stop)
        self.calls=[]

    def state(self,**changes):
        self.store.commit_page('slack',{'mode':'incremental','phase':'scan','after':'1000.000000','channels':self.channels,'index':0,
                                        'next_discovery':self.now+86400,'titles_named':True,**changes},[])

    def source(self,answer):
        """answer(method, params): a SourceError to raise, a page to return, or None for a page with one new message."""
        calls,now=self.calls,self.now
        class Source(a.Slack):
            def __init__(self):pass
            def profile(self):pass
            def get(self,method,params):
                calls.append((method,params['channel']) if 'channel' in params else (method,))
                found=answer(method,params)
                if isinstance(found,Exception):raise found
                return found if found is not None else {'messages':[{'ts':f'{now-10:.6f}','text':'New','user':'U3'}]}
        return Source()

    def refusing(self,label,channel='C1'):
        return self.source(lambda method,params:a.SourceError(label+':'+method) if params.get('channel')==channel else None)

    def channel(self,channel_id='C1'):
        return {c['id']:c for c in self.store.checkpoint('slack')['channels']}.get(channel_id)

    def failure(self):
        with self.store.connect() as db:
            return db.execute("SELECT error FROM checkpoints WHERE account_id='slack'").fetchone()['error']

    def test_a_conversation_the_owner_left_is_set_aside_and_the_others_are_read(self):
        # The owner left C1; C2 is busy. Eight syncs in a row all read C1 and never C2.
        self.state();source=self.refusing('slack_not_in_channel')
        for _ in range(8):
            a.sync_slack(self.store,{},self.account,source)  # one refused conversation is no failed sync
        self.assertEqual(self.calls,[('conversations.history','C1'),('conversations.history','C2')])
        self.assertEqual([e['body'] for e in self.store.events(['slack'])],['New'])
        left=self.channel()
        self.assertEqual((left['error'],left['refused']),('slack_not_in_channel',1))
        self.assertGreater(left['due'],self.now+3000)  # it rests: not read again every sync
        self.assertEqual(left['last_scan'],self.channels[0]['last_scan'])  # never marked read
        cp=self.store.checkpoint('slack')
        self.assertEqual((cp['index'],'scan' in cp),(0,False))
        self.assertIsNone(self.failure())  # the Slack card counts it as unavailable; the connection itself is fine
        health=self.store.snapshot([{**self.account,'service':'slack','boundary':'work:Example'}])['connectors'][0]
        self.assertEqual(health['conversation_errors'],1)

    def test_any_answer_about_one_conversation_moves_on(self):
        # A label Slack.read doesn't know comes as slack_invalid_response; a missing scope is per kind of conversation.
        # Both kept the scan and the index where they were, so the same page was read forever.
        for label in ('slack_invalid_response','slack_missing_scope','slack_channel_not_found','slack_thread_not_found'):
            with self.subTest(label):
                self.calls.clear();self.state();source=self.refusing(label)
                for _ in range(8):
                    a.sync_slack(self.store,{},self.account,source)
                self.assertEqual(self.calls,[('conversations.history','C1'),('conversations.history','C2')])
                self.assertEqual(self.channel()['error'],label)
                self.assertNotIn('scan',self.store.checkpoint('slack'))
        # a page that says there is more without a cursor: the same, nothing of it is half kept
        self.calls.clear();self.state()
        source=self.source(lambda method,params:{'messages':[{'ts':f'{self.now-20:.6f}','text':'Half'}],'has_more':True} if params['channel']=='C1' else None)
        for _ in range(8):
            a.sync_slack(self.store,{},self.account,source)
        self.assertEqual(self.calls,[('conversations.history','C1'),('conversations.history','C2')])
        self.assertEqual(self.channel()['error'],'slack_missing_cursor')

    def test_a_rate_limit_still_fails_the_sync_and_keeps_its_wait(self):
        for error in (a.SourceError('slack:conversations.history',429,95),a.SourceError('slack_ratelimited:conversations.history',retry_after=60)):
            with self.subTest(str(error)):
                self.calls.clear();self.state();source=self.source(lambda method,params:error)
                for _ in range(8):
                    with self.assertRaises(a.SourceError) as raised:a.sync_slack(self.store,{},self.account,source)
                    self.assertEqual(raised.exception.retry_after,error.retry_after)
                self.assertEqual(self.calls,[('conversations.history','C1')]*8)  # the same read, when Slack allows it again
                cp=self.store.checkpoint('slack')
                self.assertEqual((cp['index'],cp['scan']['phase']),(0,'history'))
                self.assertNotIn('failed',cp['scan'])
                self.assertNotIn('error',self.channel())
                self.assertEqual(self.channel()['due'],self.channels[0]['due'])

    def test_the_sign_in_or_the_workspace_still_fails_the_sync(self):
        for label in ('slack_token_revoked','slack_invalid_auth','slack_token_expired','slack_account_inactive','slack_ekm_access_denied'):
            with self.subTest(label):
                self.calls.clear();self.state();source=self.refusing(label)
                for _ in range(3):
                    with self.assertRaises(a.SourceError):a.sync_slack(self.store,{},self.account,source)
                self.assertEqual(self.calls,[('conversations.history','C1')]*3)
                self.assertNotIn('error',self.channel())

    def test_slack_labels_keep_their_name(self):
        # Slack.read names what is about the account or Slack itself, so the sync can tell it from one conversation's answer.
        client=a.Slack({},{**self.account,'credential':'slack','credential_variable':'KEY','connection_id':'c1'})
        def answer(label):
            reply=unittest.mock.MagicMock();reply.__enter__.return_value=reply
            reply.headers={'Maton-Connection':'c1'};reply.read.return_value=json.dumps({'ok':False,'error':label}).encode()
            with patch.object(client,'pace'),patch_everywhere(a,'credential',return_value='KEY=fake'),patch.object(a.urllib.request,'urlopen',return_value=reply):
                with self.assertRaises(a.SourceError) as raised:client.get('conversations.history',{'channel':'C1'})
            return raised.exception
        self.assertEqual(str(answer('account_inactive')),'slack_account_inactive:conversations.history')
        self.assertFalse(slack_source.slack_refused(answer('account_inactive')))
        self.assertFalse(slack_source.slack_refused(answer('internal_error')))
        self.assertEqual(str(answer('access_denied')),'slack_invalid_response:conversations.history')
        self.assertTrue(slack_source.slack_refused(answer('access_denied')))
        self.assertTrue(slack_source.slack_refused(answer('not_in_channel')))
        self.assertEqual(answer('ratelimited').retry_after,60)

    def test_a_conversation_that_comes_back_is_read_again(self):
        self.state();a.sync_slack(self.store,{},self.account,self.refusing('slack_not_in_channel'))
        first=self.channel()['due']
        cp=self.store.checkpoint('slack');cp['channels'][0]['due']=0;self.store.commit_page('slack',cp,[],record_sync=False)
        a.sync_slack(self.store,{},self.account,self.refusing('slack_not_in_channel'))
        again=self.channel()
        self.assertEqual(again['refused'],2)
        self.assertGreater(again['due']-a.time.time(),(first-self.now)*1.5)  # refused again: a longer rest
        cp=self.store.checkpoint('slack');cp['channels'][0]['due']=0;self.store.commit_page('slack',cp,[],record_sync=False)
        self.calls.clear()
        a.sync_slack(self.store,{},self.account,self.source(lambda method,params:None))  # the owner was added again
        self.assertEqual(self.calls,[('conversations.history','C1')])
        back=self.channel()
        self.assertNotIn('error',back);self.assertNotIn('refused',back)
        self.assertGreater(float(back['last_scan']),self.now-5)
        self.assertLess(back['due'],a.time.time()+3700)  # and at its usual pace

    def test_when_slack_refuses_every_conversation_the_connection_says_so(self):
        self.state();source=self.source(lambda method,params:a.SourceError('slack_missing_scope:'+method))
        a.sync_slack(self.store,{},self.account,source)  # C1: C2 may still be readable
        with self.assertRaises(a.SourceError):a.sync_slack(self.store,{},self.account,source)
        self.assertEqual({c['id'] for c in self.store.checkpoint('slack')['channels'] if c.get('error')},{'C1','C2'})
        self.assertFalse(a.sync_slack(self.store,{},self.account,source)['more'])  # both rest

    def test_a_thread_that_is_gone_leaves_the_list_and_its_conversation_reads_on(self):
        old,kept=f'{self.now-9000:.6f}',f'{self.now-8000:.6f}'
        self.channels[0]['threads']=[old,kept]
        self.state()
        source=self.source(lambda method,params:a.SourceError('slack_thread_not_found:'+method) if params.get('ts')==old else {'messages':[]})
        while a.sync_slack(self.store,{'slack_thread_retention_days':10**6},self.account,source)['more']:pass
        one=self.channel()
        self.assertEqual(one['threads'],[kept])
        self.assertNotIn('error',one)
        self.assertGreater(float(one['last_scan']),self.now-5)
        self.assertIn(('conversations.history','C2'),self.calls)
        fair={**self.account,'fair_incremental':True}  # one known thread a turn: the same
        self.channels[0]['threads']=[old,kept];self.calls.clear();self.state()
        while a.sync_slack(self.store,{'slack_thread_retention_days':10**6},fair,source)['more']:pass
        self.assertEqual(self.channel()['threads'],[kept])
        self.assertNotIn('error',self.channel())

    def test_a_read_that_keeps_failing_gives_the_others_their_turn(self):
        # Slack's 500 or a timeout at one conversation: the same page again, but not forever while the others wait.
        self.state()
        source=self.source(lambda method,params:a.SourceError('slack:'+method,500) if params['channel']=='C1' else None)
        for _ in range(slack_sync.SLACK_STUCK_AFTER):
            with self.assertRaises(a.SourceError):a.sync_slack(self.store,{},self.account,source)
        self.assertEqual(self.calls,[('conversations.history','C1')]*slack_sync.SLACK_STUCK_AFTER)
        stuck=self.channel()
        self.assertNotIn('error',stuck)  # not refused: it comes back after its usual rest
        self.assertGreater(stuck['due'],self.now+3000)
        a.sync_slack(self.store,{},self.account,source)
        self.assertEqual(self.calls[-1],('conversations.history','C2'))
        # a page that works in between starts the count again
        self.calls.clear();self.state()
        answers=[a.SourceError('slack:conversations.history',500)]*(slack_sync.SLACK_STUCK_AFTER-1)+[{'messages':[],'response_metadata':{'next_cursor':'more'}}]+[a.SourceError('slack:conversations.history',500)]
        source=self.source(lambda method,params:answers.pop(0))
        for _ in range(len(answers)):
            try:a.sync_slack(self.store,{},self.account,source)
            except a.SourceError:pass
        self.assertEqual(self.store.checkpoint('slack')['scan']['failed'],1)

    def test_triage_and_the_dm_check_take_an_unknown_answer_for_one_conversation(self):
        # conversations.info with a label Slack.read doesn't know: the first import's look ahead stayed on that conversation.
        self.channels=[{'id':'C1','name':'odd','type':'channel','threads':[]},{'id':'C2','name':'busy','type':'channel','threads':[]}]
        self.state(mode='bootstrap',phase='triage',triage=0)
        self.store.commit_page('slack',{k:v for k,v in self.store.checkpoint('slack').items() if k!='index'},[])
        source=self.source(lambda method,params:a.SourceError('slack_invalid_response:'+method) if params['channel']=='C1'
                           else {'channel':{'last_read':f'{self.now-60:.6f}'}} if method=='conversations.info' else None)
        a.sync_slack(self.store,{},self.account,source)
        cp=self.store.checkpoint('slack')
        self.assertEqual((cp['phase'],cp.get('step')),('scan','recent'))
        for _ in range(12):
            if not a.sync_slack(self.store,{},self.account,source)['more']:break
        cp=self.store.checkpoint('slack')
        self.assertEqual(cp['mode'],'incremental')
        odd=self.channel()
        self.assertEqual(odd['error'],'slack_invalid_response')
        self.assertGreater(odd['due'],self.now+3000)  # after the first import too: it has a rest, so it isn't first every sync
        self.assertEqual(sum(c==('conversations.history','C1') for c in self.calls),1)
        self.assertIn(('conversations.history','C2'),self.calls)

    def test_discovery_drops_one_that_stays_refused_and_is_no_longer_listed(self):
        def discover(listed,pages=1,**changes):
            self.channels=[{'id':'C1','name':'left','type':'channel','threads':[],'error':'slack_not_in_channel','refused':slack_source.SLACK_GONE_AFTER,'due':self.now+9000},
                           {'id':'C2','name':'busy','type':'channel','threads':[],'last_scan':f'{self.now-60:.6f}','due':self.now+9000},
                           {'id':'C3','name':'once','type':'channel','threads':[],'error':'slack_not_in_channel','refused':1,'due':self.now+9000},
                           {'id':'C4','name':'archived','type':'channel','threads':[],'last_scan':f'{self.now-60:.6f}','due':self.now+9000}]
            self.state(phase='discover',**changes)
            answers=[{'channels':[{'id':i,'name':i} for i in listed],**({'response_metadata':{'next_cursor':'next'}} if n+1<pages else {})} for n in range(pages)]
            source=self.source(lambda method,params:answers.pop(0))
            for _ in range(pages):
                a.sync_slack(self.store,{},self.account,source)
            cp=self.store.checkpoint('slack')
            self.assertNotIn('listed',cp)
            return sorted(c['id'] for c in cp['channels'])
        # Refused three times in a row and not in the owner's list any more: gone. One refusal, or no error: kept.
        self.assertEqual(discover(['C2']),['C2','C3','C4'])
        self.assertEqual(discover(['C2'],pages=2),['C2','C3','C4'])
        self.assertEqual(discover(['C1','C2']),['C1','C2','C3','C4'])  # still listed: Slack may let it be read again
        self.assertEqual(discover([]),['C1','C2','C3','C4'])  # an empty list drops nothing
        # a discovery that was under way when this version arrived saw only its last pages: it drops nothing
        self.assertEqual(discover(['C2'],page_token='half-way'),['C1','C2','C3','C4'])


if __name__=='__main__':unittest.main()
