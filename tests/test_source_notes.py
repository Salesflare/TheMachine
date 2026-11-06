import datetime as dt
import importlib.util
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402

spec=importlib.util.spec_from_file_location('source_notes_assistant',Path(__file__).parent.parent.joinpath('assistant.py'))
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
T=dt.datetime(2026,10,11,8,0,tzinfo=dt.timezone.utc)
# Services a Machine can have, as config.json names them; every note file belongs to one.
SERVICES={'gmail','outlook','calendar','outlook_calendar','slack','salesflare','android','whatsapp','gateway','linkedin','x',
          'github','stripe','intercom','zoom','trello','shortcut','rss','docs'}


class SourceNotes(unittest.TestCase):
    def test_only_connected_sources_get_their_notes(self):
        text=a.source_notes(['gmail','slack'])
        self.assertIn('**Gmail.**',text);self.assertIn('**Slack.**',text)
        for other in ('**Intercom**','**X**','**Stripe**','**WhatsApp.**','**The Machine itself**'):
            self.assertNotIn(other,text)
        self.assertIn('**Intercom**',a.source_notes(['intercom']))
        self.assertIn('**The Machine itself**',a.source_notes(['gateway']))  # faults come through the Gateway source

    def test_aliases_duplicates_and_unknown_services(self):
        self.assertEqual(a.source_notes(['outlook_calendar']),a.source_notes(['calendar']))
        self.assertEqual(a.source_notes(['calendar','calendar','outlook_calendar']).count('**Calendar.**'),1)
        self.assertEqual(a.source_notes([]),'')
        self.assertEqual(a.source_notes([None,'rss','../AGENTS','Gmail']),'')  # no note, or not a service name
        self.assertEqual(a.source_notes(['x','gmail']),a.source_notes(['gmail','x']))  # a fixed order

    def test_note_files_are_one_per_service_and_left_out_of_agents_md(self):
        files=sorted(a.SOURCE_NOTES.glob('*.md'))
        self.assertGreaterEqual(len(files),12)
        agents=(a.ROOT/'AGENTS.md').read_text()
        for path in files:
            self.assertIn(path.stem,SERVICES)
            text=path.read_text().strip()
            self.assertTrue(text.startswith('- **'),path.name);self.assertNotIn('—',text)
            first=text.splitlines()[0]
            self.assertNotIn(first,agents)  # each note lives in one place
        self.assertIn('source-notes/<service>.md',agents)
        cap=int(re.search(r"contextFile\('AGENTS', '[^']*', (\d+)[,)]",(a.ROOT/'openclaw-plugin/review-recovery.ts').read_text())[1])
        self.assertLess(len(agents.strip()),cap-5000)

    def test_account_services(self):
        config={'accounts':[{'id':'w','service':'gmail'},{'id':'i','service':'intercom'},{'id':'odd'}]}
        self.assertEqual(a.account_services(config),['gmail','intercom','gmail'])  # an account with no service is Gmail
        self.assertEqual(a.account_services(config,['i']),['intercom'])
        self.assertEqual(a.account_services(config,[]),[])


class Runner:
    def __init__(self,*results):self.results=list(results);self.requests=[]
    def __call__(self,request):self.requests.append(request);return {'status':self.results.pop(0)}


class PromptsCarryTheirNotes(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.store=a.Store(Path(self.temp.name)/'events.sqlite')
        self.app=object.__new__(a.App);self.app.store=self.store
        self.app.quick_first_review=lambda db:0
        self.app.config={'accounts':[{'id':'work'},{'id':'help','service':'intercom'}],  # no service: Gmail
                         'review_worker':{'enabled':True,'gap_seconds':120,'timeout_seconds':1500,'min_signals':1}}
        self.store.commit_page('work',{},[{'account_id':'work','source_id':'one','kind':'gmail.message','occurred_at':a.now(),'title':'Hi','body':'Text','metadata':{},'deleted':False}])

    def test_review_gets_the_notes_of_this_machines_sources_only(self):
        runner=Runner('admitted')
        with patch_everywhere(a,'now',return_value=T.isoformat()):self.app.review_step(runner)
        message=runner.requests[0]['message']
        self.assertIn('**Gmail.**',message);self.assertIn('**Intercom**',message)
        self.assertNotIn('**X**',message);self.assertNotIn('**Stripe**',message);self.assertNotIn('**Slack.**',message)

    def test_preparation_gets_the_notes_of_its_cards_sources(self):
        sid=self.store.suggest('task','Reply to the customer','I can draft a reply.',[1])['id']
        self.store.decide(sid,'accept','','click','telegram')
        calls=[];self.app.preparation_step(lambda r:calls.append(r) or {'status':'admitted'})
        message=next(c['message'] for c in calls if c.get('message'))
        self.assertIn('**Gmail.**',message)
        self.assertNotIn('**Intercom**',message)  # connected, but not this card's source


class OlderMailInEveryChat(unittest.TestCase):
    """A mail older than what is collected (one the owner sent weeks ago) is looked up in the mailbox itself, read-only
    (App.mailbox_lookup), from the main chat and from an Outlook to-do's chat too, not only a Gmail to-do's run."""
    def test_outlook_to_dos_learn_the_mailbox_search(self):
        text=a.source_notes(['outlook'])
        self.assertIn('mailbox:true',text);self.assertIn('read-only',text)
        self.assertIn('mailbox:true',a.source_notes(['gmail']))

    def test_the_main_chat_is_told_to_search_the_mailbox_before_saying_a_mail_is_not_there(self):
        plugin=(a.ROOT/'openclaw-plugin/index.ts').read_text()
        self.assertIn("'events'",plugin.split('const TOOL_ACTIONS',1)[1].split('\n',1)[0])
        tool=plugin.split("name: 'assistant_signals'",1)[1].split('parameters:',1)[0]
        self.assertIn('events with mailbox:true',tool);self.assertIn('read-only',tool)
        self.assertIn('never say a mail isn’t there before both searches',tool)

    def test_a_chat_search_of_every_account_reaches_the_mailboxes(self):
        app=object.__new__(a.App)
        app.config={'accounts':[{'id':'work'},{'id':'home','service':'outlook'}]}
        calls=[]
        app.mailbox_lookup=lambda ids,query,limit=5:calls.append((list(ids),query,limit)) or ([],{})
        found=app.action('events',{'account_ids':['all'],'mailbox':True,'query':'to:sam in:sent'})
        self.assertEqual(calls,[(['work','home'],'to:sam in:sent',5)])
        self.assertEqual(found['events'],[]);self.assertIn('Nothing in those mailboxes',found['note'])


if __name__=='__main__':
    unittest.main()
