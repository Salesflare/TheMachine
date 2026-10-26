import importlib.util
from pathlib import Path
import datetime as dt,tempfile,unittest
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('assistant_gw',Path(__file__).parent.parent.joinpath('assistant.py'));a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
account={'id':'openclaw-gateway','service':'gateway'}
T=dt.datetime(2026,10,10,15,14,tzinfo=dt.timezone.utc)
RUN='2026-10-10T17:14:40.572+02:00 [telegram] embedded run agent end: runId=0b1e2c3d-1111-2222-3333-444455556666 isError=true model=gpt-6.1-sol provider=example-openai error=LLM request failed: DNS lookup failed'
HANDOFF='2026-10-10T17:14:40.572+02:00 [tools] openclaw failed: Gateway client authority closed before dispatching openclaw.chat. raw_params={"message":"how are the embeddings?"}'
SEND="2026-10-10T17:14:40.572+02:00 [telegram] sendRichMessage failed: Network request for 'sendRichMessage' failed!"

class FakeJournal:
 def __init__(self):self.entries=[];self.calls=[]
 def read(self,cursor=None,since=None):
  self.calls.append((cursor,since))
  if cursor=='bad':raise a.SourceError('journal_read_failed')
  start=0 if cursor is None else int(cursor)+1
  return [(str(i),at,m) for i,(at,m) in enumerate(self.entries) if i>=start]

class GatewayTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.store=a.Store(Path(self.tmp.name)/'a.sqlite')
 def tearDown(self):self.tmp.cleanup()
 def rows(self):
  with self.store.connect() as db:return [dict(r) for r in db.execute('SELECT source_id,title,body,version,metadata FROM events ORDER BY source_id')]

 def test_only_selected_kinds_are_collected(self):
  self.assertEqual(a.gateway_classify(RUN)[0],'agent_run_failed')
  self.assertEqual(a.gateway_classify(HANDOFF)[0],'handoff_failed')
  self.assertEqual(a.gateway_classify(SEND)[0],'telegram_send_failed')
  self.assertEqual(a.gateway_classify('[tools] tool_call failed: Gateway caller authority is no longer active.')[0],'handoff_failed')
  self.assertEqual(a.gateway_classify('[telegram] spooled update 257985001 failed; keeping for retry')[0],'telegram_send_failed')
  for noise in ['[telegram] embedded run agent end: runId=x isError=false model=m',
                '[telegram] reconnect delivery drain failed: gateway is draining for restart',
                '[telegram] fetch fallback: primary connection path failed; trying alternative Telegram API IP',
                '[diagnostics/memory] memory pressure: level=warning reason=rss_threshold',
                '[ws] ⇄ res ✗ chat.history 3ms errorCode=UNAVAILABLE errorMessage=chat.history unavailable during gateway restart',
                '[agent/embedded] transient same-model retry 1/2 for example-openai/gpt-6.1-sol reason=timeout']:
   self.assertIsNone(a.gateway_classify(noise),noise)

 def test_lines_are_cleaned_and_secrets_redacted(self):
  line=a.gateway_line("2026-10-10T17:14:40.572+02:00 [telegram] sendMessage failed: https://api.telegram.org/bot123456789:AAbbCCddEEffGGhhIIjjKKllMMnn/sendMessage token=abc123")
  self.assertTrue(line.startswith('[telegram]'));self.assertNotIn('AAbbCC',line);self.assertNotIn('abc123',line)
  self.assertIn('<id>',a.gateway_line(RUN))

 def test_burst_groups_and_grows_across_polls_then_resumes_from_cursor(self):
  j=FakeJournal();j.entries=[(T,RUN),(T+dt.timedelta(minutes=1),'[ws] noise'),(T+dt.timedelta(minutes=2),RUN),(T+dt.timedelta(minutes=3),HANDOFF)]
  with patch.object(a,'now',return_value=(T+dt.timedelta(minutes=5)).isoformat()):
   self.assertEqual(a.sync_gateway(self.store,{},account,j)['events'],2)
   rows=self.rows();self.assertEqual(len(rows),2)
   run=[r for r in rows if r['source_id'].startswith('agent_run_failed')][0]
   self.assertIn('(2×)',run['title']);self.assertIn('17:14:00',run['body'])
   j.entries.append((T+dt.timedelta(minutes=4),RUN))
   self.assertEqual(a.sync_gateway(self.store,{},account,j)['events'],1)
  self.assertEqual(j.calls[-1][0],'3')
  run=[r for r in self.rows() if r['source_id'].startswith('agent_run_failed')][0]
  self.assertIn('(3×)',run['title']);self.assertEqual(run['version'],2)
  self.assertEqual(len(self.rows()),2)

 def test_closed_windows_are_pruned_and_new_window_is_separate(self):
  j=FakeJournal();j.entries=[(T,SEND)]
  with patch.object(a,'now',return_value=T.isoformat()):a.sync_gateway(self.store,{},account,j)
  later=T+dt.timedelta(hours=2);j.entries.append((later,SEND))
  with patch.object(a,'now',return_value=later.isoformat()):a.sync_gateway(self.store,{},account,j)
  self.assertEqual(len(self.rows()),2)
  self.assertEqual(len(self.store.checkpoint('openclaw-gateway')['open_buckets']),1)

 def test_invalid_cursor_falls_back_to_last_seen_time(self):
  j=FakeJournal();j.entries=[(T,SEND)]
  with patch.object(a,'now',return_value=T.isoformat()):a.sync_gateway(self.store,{},account,j)
  state=self.store.checkpoint('openclaw-gateway');state['cursor']='bad'
  with self.store.connect() as db:db.execute('UPDATE checkpoints SET state=? WHERE account_id=?',(a.encoded(state),'openclaw-gateway'))
  with patch.object(a,'now',return_value=T.isoformat()):a.sync_gateway(self.store,{},account,j)
  self.assertEqual(j.calls[-1],(None,f'@{int(T.timestamp())}'))

 def test_first_read_uses_bootstrap_window(self):
  j=FakeJournal()
  a.sync_gateway(self.store,{},{**account,'bootstrap_hours':6},j)
  self.assertEqual(j.calls[0],(None,'-6h'))

if __name__=='__main__':unittest.main()
