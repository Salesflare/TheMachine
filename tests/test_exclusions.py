import importlib.util,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('assistant_excl',Path(__file__).parent.parent.joinpath('assistant.py'));a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
def ev(sid,**metadata):return {'account_id':'acc','source_id':sid,'kind':'k','occurred_at':'2026-10-11T00:00:00+00:00','title':'t','body':'b','metadata':metadata,'deleted':False}
RULES=[{'channels':['development-log','error-log']},{'channels':['sales'],'bots_only':True},
       {'packages':['android','com.google.android.youtube']},{'senders':['product@analytics.example']},
       {'chats':['120363000000000001@g.us']}]

class Exclusions(unittest.TestCase):
    def test_rules(self):
        m=lambda **k:a.excluded_by_rules(RULES,{'metadata':k})
        self.assertTrue(m(channel_name='error-log',user_id='U1'))
        self.assertTrue(m(channel_name='sales',bot_id='B1'))
        self.assertFalse(m(channel_name='sales',user_id='U1'))  # people in #sales stay
        self.assertFalse(m(channel_name='leads',bot_id='B1'))
        self.assertTrue(m(package_name='android'));self.assertFalse(m(package_name='com.whatsapp.w4b'))
        self.assertTrue(m(**{'from':'AnalyticsVendor <product@analytics.example>'}));self.assertFalse(m(**{'from':'alerts@seo-tool.example'}))
        self.assertFalse(a.excluded_by_rules([],{'metadata':{'channel_name':'error-log'}}))
        self.assertTrue(m(chat_id='120363000000000001@g.us',chat_name='Family photo diary'))
        self.assertFalse(m(chat_id='other@g.us',chat_name='Family photo diary'))

    def test_routine_recurring_calendar_instances(self):
        rule=[{'routine_recurring':True}]
        def m(**k):return a.excluded_by_rules(rule,{'metadata':k})
        same={'dateTime':'2026-10-14T09:00:00+02:00'};utc={'dateTime':'2026-10-14T07:00:00Z'}
        self.assertTrue(m(recurring_event_id='r',start=same,original_start=same,status='confirmed'))
        self.assertTrue(m(recurring_event_id='r',start=utc,original_start=same))  # same moment, other notation
        self.assertFalse(m(recurring_event_id='r',start={'dateTime':'2026-10-14T10:00:00+02:00'},original_start=same))  # moved
        self.assertFalse(m(recurring_event_id='r',start=same,original_start=same,status='cancelled'))
        self.assertFalse(m(start=same))  # one-off meeting
        self.assertTrue(m(recurring_event_id='r',start={'date':'2026-10-14'},original_start={'date':'2026-10-14'}))
        system=[{'packages':['android'],'text':['is displaying over other apps','charging this device via usb']}]
        overlay={'title':'Some App is displaying over other apps','body':'If you don’t want…','metadata':{'package_name':'android'}}
        self.assertTrue(a.excluded_by_rules(system,overlay))
        self.assertFalse(a.excluded_by_rules(system,{'title':'Storage space running out','body':'','metadata':{'package_name':'android'}}))
        self.assertFalse(a.excluded_by_rules(system,{**overlay,'metadata':{'package_name':'com.other'}}))
        titled=[{'routine_recurring':True,'titles':['Lunch','Stand up']}]
        rec={'recurring_event_id':'r','start':same,'original_start':same}
        self.assertTrue(a.excluded_by_rules(titled,{'title':'lunch','metadata':rec}))
        self.assertFalse(a.excluded_by_rules(titled,{'title':'Growth meeting','metadata':rec}))
        self.assertFalse(a.excluded_by_rules(titled,{'title':'Lunch','metadata':{'start':same}}))  # a one-off lunch stays

    def test_defaults_every_owner_gets(self):
        config={'accounts':[{'id':'g','service':'gmail'},{'id':'w','service':'whatsapp'},{'id':'c','service':'calendar'},
                            {'id':'p','service':'android'}]}
        phone,calendar=config['accounts'][3],config['accounts'][2]
        rules=a.default_exclusions(config,phone)
        drop=lambda package,title='New message':a.excluded_by_rules(rules,{'title':title,'body':'','metadata':{'package_name':package}})
        self.assertFalse(drop('com.google.android.gm'));self.assertFalse(drop('com.whatsapp'));self.assertFalse(drop('com.whatsapp.w4b'))  # account coverage is unknown
        self.assertFalse(drop('com.Slack'))  # no Slack source: its phone notifications are the only copy
        self.assertFalse(drop('com.example.bank'))
        for notice in ('Chrome is displaying over other apps','Charging this device via USB','USB debugging connected',
                       'Wireless debugging connected','Serial console enabled'):
            self.assertTrue(drop('android',notice),notice)
        self.assertFalse(drop('android','Storage space running out'))
        same={'dateTime':'2026-10-14T12:00:00+02:00'}
        lunch={'title':'Lunch','metadata':{'recurring_event_id':'r','start':same,'original_start':same}}
        self.assertTrue(a.excluded_by_rules(a.default_exclusions(config,calendar),lunch))
        self.assertFalse(a.excluded_by_rules(a.default_exclusions(config,calendar),{**lunch,'title':'Lunch with Ann'}))
        self.assertEqual(a.default_exclusions(config,{**phone,'default_exclude':False}),[])
        self.assertEqual(a.default_exclusions(config,config['accounts'][0]),[])

    def test_work_mail_does_not_discard_personal_phone_mail(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        store=a.Store(Path(tmp.name)/'e.sqlite')
        phone={'id':'acc','service':'android'}
        config={'accounts':[{'id':'work','service':'gmail','email':'owner@work.example'},phone]}
        store.exclusions={'acc':a.default_exclusions(config,phone)}
        notification=ev('personal-mail',package_name='com.google.android.gm')
        notification.update(kind='android.notification',title='Personal message')
        store.commit_page('acc',{'cursor':'next'},[notification])
        self.assertEqual(len(store.events(['acc'])),1)
        self.assertEqual(store.checkpoint('acc'),{'cursor':'next'})
        store.exclusions['acc'].append({'packages':['com.google.android.gm']})
        store.commit_page('acc',{'cursor':'later'},[{**notification,'source_id':'explicitly-excluded'}])
        self.assertEqual(len(store.events(['acc'])),1)

    def test_excluded_signals_are_never_stored_and_old_copies_are_removed(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        store=a.Store(Path(tmp.name)/'e.sqlite')
        store.commit_page('acc',{},[ev('1',channel_name='error-log'),ev('2',channel_name='leads')])
        self.assertEqual(len(store.events(['acc'])),2)
        self.assertEqual(store.purge_excluded('acc',RULES),1)
        store.exclusions={'acc':RULES}
        store.commit_page('acc',{'cursor':'next'},[ev('3',channel_name='development-log'),ev('4',channel_name='sales',user_id='U1')])
        self.assertEqual(sorted(e['source_id'] for e in store.events(['acc'])),['2','4'])
        self.assertEqual(store.checkpoint('acc'),{'cursor':'next'})

if __name__=='__main__':unittest.main()
