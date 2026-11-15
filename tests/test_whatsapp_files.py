# A file on WhatsApp (2026-11-15): the owner asked a to-do to send a file to someone on WhatsApp, which was linked. The
# WhatsApp action took text only, so the run's save was refused, it opened WhatsApp Web in the browser instead, and
# asked the owner to link WhatsApp and scan a QR code. Now the action carries one file, the owner sees it before Send
# now, wacli sends exactly those bytes, and a run is told its linked chat apps are linked. wacli is always faked.
from pathlib import Path
import subprocess,unittest
from unittest.mock import patch
from test_whatsapp import WhatsAppSend,WA,CHAT,ok,n
from machine.sources.connectors import chats_prompt
import machine.app.preparation as machine_app_preparation
import machine.main as machine_main


class WhatsAppFile(WhatsAppSend):
 def setUp(self):
  super().setUp()
  root=Path(self.tmp.name);self.src=root/'job-files';self.src.mkdir();self.files=root/'attachment-store'
  (self.src/'report.pdf').write_bytes(b'%PDF-1 fake report..')
  (self.src/'other.pdf').write_bytes(b'%PDF-1 other')
  config={'accounts':self.accounts,'attachment_sources':[str(self.src)],'attachment_dir':str(self.files)}
  app=object.__new__(machine_main.App);app.store=self.store;app.config=config;self.app=lambda:app

 def test_one_file_with_or_without_a_caption_shows_before_send(self):
  action=self.ready(body=None,attachments=[str(self.src/'report.pdf')])
  record=action['attachments'][0]
  self.assertEqual((action['body'],record['name'],action['max_length']),('','report.pdf',1024))
  self.assertEqual((self.files/record['sha256']).read_bytes(),b'%PDF-1 fake report..')
  self.assertEqual(n.preview(action),'WhatsApp message to Sam\n\nFile: report.pdf (20 B)')
  captioned=self.ready(body='Here it is.',attachments=[str(self.src/'report.pdf')])
  self.assertTrue(n.preview(captioned).endswith('File: report.pdf (20 B)\n\nHere it is.'))
  self.assertNotEqual(action['revision'],captioned['revision'])  # the file is part of what the owner approves
  self.assertEqual(machine_main.App.draft_attachment(self.app(),self.sid,record['sha256'])[2],'report.pdf')  # it opens from the card
  for bad in ({'attachments':[str(self.src/'report.pdf'),str(self.src/'other.pdf')]},{'attachments':[]},
              {'attachments':['/etc/hostname']},{'body':'a'*1025,'attachments':[str(self.src/'report.pdf')]},{'body':None}):
   with self.assertRaises(ValueError,msg=bad):self.save(**bad)

 def test_message_that_promises_a_file_without_one_is_caught(self):
  self.decide('accept')
  with self.assertRaisesRegex(ValueError,'mentions a file but has none'):self.save(body='Here is the file, see attached.')
  self.save(body='Here is the report.',attachments=[str(self.src/'report.pdf')])  # with the file it saves

 def test_send_file_sends_the_approved_bytes_once_and_leaves_no_copy(self):
  action=self.ready(body='Here it is.',attachments=[str(self.src/'report.pdf')])
  seen=[]
  def run(args,**kw):
   path=args[args.index('--file')+1];seen.append((args,kw['env'].get('WACLI_READONLY'),Path(path).read_bytes()))
   return ok({'sent':True,'to':CHAT,'id':'3EB0FILE'})
  t=n.WhatsAppTransport({**self.app().config,'wacli':'/opt/wacli'})
  with patch.object(n.subprocess,'run',side_effect=run):self.assertEqual(t.send(action,{'id':'J'}),{'message_id':'whatsapp:3EB0FILE'})
  (args,env,data),=seen
  self.assertNotIn('--read-only',args);self.assertIsNone(env);self.assertEqual(data,b'%PDF-1 fake report..')
  rest=args[args.index('send'):]
  self.assertEqual(rest[:3],['send','file','--to']);self.assertEqual(rest[3],CHAT)
  self.assertEqual(rest[rest.index('--filename')+1],'report.pdf');self.assertEqual(rest[rest.index('--caption')+1],'Here it is.')
  self.assertEqual(rest[rest.index('--mime')+1],'application/pdf')
  self.assertFalse(Path(args[args.index('--file')+1]).exists())  # the plain copy is gone after the send
  self.assertEqual([p.name for p in self.files.iterdir()],[action['attachments'][0]['sha256']])
  # Without a caption, no --caption; an unclear outcome still never resends and still cleans up
  bare=self.ready(body=None,attachments=[str(self.src/'report.pdf')])
  with patch.object(n.subprocess,'run',side_effect=subprocess.TimeoutExpired('wacli',150)) as run:self.assertEqual(t.send(bare,{'id':'J'}),{})
  self.assertNotIn('--caption',run.call_args[0][0]);self.assertEqual(len(list(self.files.iterdir())),1)
  # A stored file that changed after the owner saw it is never sent
  (self.files/action['attachments'][0]['sha256']).write_bytes(b'tampered')
  with patch.object(n.subprocess,'run') as run,self.assertRaisesRegex(ValueError,'Nothing was sent'):t.send(action,{'id':'J'})
  run.assert_not_called()

 def test_reconcile_finds_the_one_file_message(self):
  action=self.ready(body='',attachments=[str(self.src/'report.pdf')])
  action['proof']={'whatsapp_dispatched_at':'2026-10-19T10:00:00+00:00','whatsapp_before_ids':['OLD']}
  mine={'MsgID':'F1','FromMe':True,'Text':'','MediaType':'document','MediaCaption':'','Filename':'report.pdf','Timestamp':'2026-10-19T10:00:02Z'}
  t=n.WhatsAppTransport({**self.app().config,'wacli':'/opt/wacli'})
  for rows,expected in (([mine],{'message_id':'whatsapp:F1'}),([{**mine,'Filename':''}],{'message_id':'whatsapp:F1'}),
                        ([{**mine,'Filename':'other.pdf'}],{}),([{**mine,'MediaType':''}],{}),([{**mine,'MediaCaption':'Hi'}],{}),
                        ([mine,{**mine,'MsgID':'F2'}],{}),([{**mine,'MsgID':'OLD'}],{})):
   with patch.object(n.subprocess,'run',return_value=ok({'messages':rows})):self.assertEqual(t.reconcile(action,{'id':'J'}),expected,rows)


class LinkedChatsPrompt(unittest.TestCase):
 def test_a_linked_chat_app_is_never_sent_to_its_web_version_or_a_qr_code(self):
  line=chats_prompt({'accounts':[WA,{'id':'tg','service':'telegram'},{'id':'mail','service':'gmail'}]})
  self.assertIn('WhatsApp (personal-whatsapp), Telegram (tg)',line)
  self.assertIn('attachments:[<path>]',line);self.assertIn('Telegram carry text only',line)
  self.assertIn("Never use these apps' web versions in the browser",line);self.assertIn('scan a QR code',line)
  self.assertEqual(chats_prompt({'accounts':[{'id':'mail','service':'gmail'}]}),'')
  self.assertEqual(chats_prompt({'accounts':[{**WA,'shared':True}]}),'')
  self.assertNotIn('attachments',chats_prompt({'accounts':[{'id':'sg','service':'signal'}]}))

 def test_the_do_it_prompt_carries_it(self):
  job={'job_id':'job-1','suggestion_id':'s1'}
  self.assertIn("Linked here: WhatsApp (personal-whatsapp)",machine_app_preparation.preparation_prompt(job,config={'accounts':[WA]}))
  self.assertNotIn('Linked here',machine_app_preparation.preparation_prompt(job,config={'accounts':[]}))


if __name__=='__main__':unittest.main()
