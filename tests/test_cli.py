import importlib.util
from pathlib import Path
import contextlib,io,json,unittest
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('assistant_cli',Path(__file__).parent.parent.joinpath('cli.py'));cli=importlib.util.module_from_spec(spec);spec.loader.exec_module(cli)
config={'port':0,'accounts':[{'id':'work'},{'id':'home'}]}
def task(id,status,**extra):return {'id':id,'status':status,'title':'Task '+id,'body':'Body','created_at':'2026-10-10T10:00:00+00:00','account_ids':'["work"]','event_ids':'[1]',**extra}
STATUS={'suggestions':[task('aaa111','pending'),task('aab222','prepared'),task('bbb333','snoozed',snoozed_until='2026-10-12T07:00:00+00:00'),task('ccc444','completed')],
        'decisions':[{'suggestion_id':'aaa111','choice':'other','source':'telegram','feedback':'shorter please','created_at':'2026-10-10T11:00:00+00:00'}],
        'connectors':[],'analyses':[],'review_health':{}}

class CliTests(unittest.TestCase):
 def run_cli(self,*argv,responses=None):
  calls=[]
  def fake(cfg,action,args=None):
   calls.append((action,args))
   if action in cli.assistant.OWNER_ACTIONS:raise cli.CliError('refused')
   return (responses or {}).get(action,STATUS)
  out=io.StringIO()
  with patch.object(cli,'call',side_effect=fake),patch.object(cli,'load_config',return_value=config),contextlib.redirect_stdout(out):
   cli.main(list(argv))
  return out.getvalue(),calls

 def test_tasks_default_matches_dashboard_outstanding(self):
  out,_=self.run_cli('tasks','--json');self.assertEqual([t['id'] for t in json.loads(out)],['aaa111','aab222'])
  out,_=self.run_cli('tasks','--later','--json');self.assertEqual([t['id'] for t in json.loads(out)],['bbb333'])
  out,_=self.run_cli('tasks','--all','--json');self.assertEqual(len(json.loads(out)),4)

 def test_show_accepts_unique_prefix_and_reads_task_evidence_only(self):
  out,calls=self.run_cli('show','bbb','--json',responses={'status':STATUS,'events':[{'id':1}]})
  self.assertEqual(json.loads(out)['task']['id'],'bbb333')
  self.assertIn(('events',{'account_ids':['work'],'event_ids':[1],'limit':1,'full':True}),calls)
  with self.assertRaises(SystemExit):self.run_cli('show','aa')  # ambiguous
  with self.assertRaises(SystemExit):self.run_cli('show','zzz')

 def test_show_lists_written_feedback(self):
  out,_=self.run_cli('show','aaa','--no-evidence');self.assertIn('shorter please',out)

 def test_search_defaults_to_all_configured_accounts(self):
  _,calls=self.run_cli('search','pricing',responses={'events':[]})
  self.assertEqual(calls[0],('events',{'account_ids':['work','home'],'query':'pricing','limit':20,'full':True}))

 def test_owner_decisions_are_refused_before_reaching_the_service(self):
  with patch.object(cli.urllib.request,'urlopen') as urlopen,self.assertRaises(cli.CliError):
   cli.call(config,'decide',{'suggestion_id':'aaa111','choice':'complete'})
  urlopen.assert_not_called()

 def test_prepare_sends_full_task_id(self):
  _,calls=self.run_cli('prepare','aab','--body','  Short brief.  ',responses={'status':STATUS,'prepare':{'status':'prepared'}})
  self.assertEqual(calls[-1],('prepare',{'suggestion_id':'aab222','body':'Short brief.'}))

 def test_reviews_exposes_saved_outcome_and_run_history(self):
  status={**STATUS,'review_runs':[{'run_id':'abc','status':'error','started_at':'2026-10-13T08:00:00+00:00',
      'review_saved':True,'checked_count':40,'pending_count':0,'duration_seconds':90,
      'error':'model_idle_timeout','error_phase':'model'}]}
  out,_=self.run_cli('reviews','--json',responses={'status':status})
  self.assertEqual(json.loads(out)['runs'][0]['checked_count'],40)
  out,_=self.run_cli('reviews',responses={'status':status})
  self.assertIn('40 signal versions saved',out);self.assertIn('model_idle_timeout (model)',out)

 def test_fleet_pair_keeps_its_token_private_and_points_the_config_at_it(self):
  import os,tempfile
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'config.json';path.write_text(json.dumps({'database':str(Path(d)/'events.sqlite'),'accounts':[{'id':'work','email':'me@acme.example','boundary':'work:Acme'}],'credentials':{},'fleet_relay_url':'https://old.example'}))
   with patch.object(cli.assistant.fleet,'pair',return_value={'token':'fd_secret','label':'Laptop'}) as pair,contextlib.redirect_stdout(io.StringIO()) as out:
    cli.main(['--config',str(path),'fleet-pair','ABCD-EFGH','--label','Laptop','--relay','https://ignored.example'])
   pair.assert_called_once_with('ABCD-EFGH','Laptop',['me@acme.example'])
   saved=json.loads(path.read_text());token=Path(saved['credentials']['fleet'])
   self.assertEqual(('fleet_relay_url' in saved,token.read_text().strip(),oct(token.stat().st_mode&0o777)),(False,'fd_secret','0o600'))
   self.assertNotIn('fd_secret',out.getvalue())
   with patch.object(cli.assistant.fleet,'pair',return_value={'token':'fd_secret','label':'Laptop'}),contextlib.redirect_stdout(io.StringIO()):
    cli.main(['--config',str(path),'fleet-pair','ABCD-EFGH','--network','https://ignored.example'])  # the new name of --relay
   with self.assertRaises(SystemExit):cli.main(['--config',str(Path(d)/'none.json'),'fleet-pair','X'])

if __name__=='__main__':unittest.main()
