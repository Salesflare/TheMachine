import datetime as dt
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402

spec=importlib.util.spec_from_file_location('review_worker_assistant',Path(__file__).parent.parent.joinpath('assistant.py'))
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
T=dt.datetime(2026,10,11,8,0,tzinfo=dt.timezone.utc)

class Runner:
    def __init__(self,*results):self.results=list(results);self.requests=[]
    def __call__(self,request):self.requests.append(request);return {'status':self.results.pop(0)}

class ReviewWorker(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.store=a.Store(Path(self.temp.name)/'events.sqlite')
        self.app=object.__new__(a.App);self.app.store=self.store
        self.app.quick_first_review=lambda db:0  # the regular reviews only; test_fast_first_look has the quick first one
        self.app.config={'accounts':[{'id':'work'},{'id':'home'}],'review_worker':{'enabled':True,'gap_seconds':120,'timeout_seconds':1500,'min_signals':1}}
        self.store.commit_page('work',{},[{'account_id':'work','source_id':'one','kind':'gmail.message','occurred_at':a.now(),'title':'Hi','body':'Text','metadata':{},'deleted':False}])

    def step(self,runner,at):
        with patch_everywhere(a,'now',return_value=at.isoformat()):return self.app.review_step(runner)

    def runs(self):
        with self.store.connect() as db:return [dict(r) for r in db.execute('SELECT * FROM review_runs ORDER BY started_at')]

    def test_starts_one_isolated_review_monitors_it_and_waits_before_the_next(self):
        runner=Runner('admitted','pending','ok','admitted')
        self.assertEqual(self.step(runner,T),'admitted')
        start=runner.requests[0]
        self.assertEqual((start['kind'],start['action']),('review','start'))
        self.assertIn('"work", "home"',start['message']);self.assertIn('limit 120',start['message'])
        self.assertEqual(self.step(runner,T+dt.timedelta(minutes=1)),'pending')
        self.assertEqual(runner.requests[1],{'kind':'review','job_id':start['job_id'],'action':'status'})
        self.assertEqual(self.step(runner,T+dt.timedelta(minutes=8)),'ok')
        self.assertIsNone(self.step(runner,T+dt.timedelta(minutes=9)))  # within the gap
        self.assertEqual(self.step(runner,T+dt.timedelta(minutes=11)),'admitted')
        self.assertNotEqual(runner.requests[-1]['job_id'],start['job_id'])

    def test_runs_that_claim_nothing_back_off_instead_of_starting_again_at_once(self):
        # A model that couldn't reach its tools ended each review with "Done.": ok, nothing claimed. While the first
        # review dug on (no gap) it started again every minute, about 100k tokens a run.
        self.app.first_dig=lambda db,stamp:{'left':20}
        runner=Runner('admitted','ok','admitted','ok','admitted','ok','admitted')
        at=lambda minutes:T+dt.timedelta(minutes=minutes)
        self.assertEqual(self.step(runner,at(0)),'admitted');self.assertEqual(self.step(runner,at(1)),'ok')
        self.assertIsNone(self.step(runner,at(1.5)))  # a minute after the first empty run
        self.assertEqual(self.step(runner,at(2.1)),'admitted');self.assertEqual(self.step(runner,at(3)),'ok')
        self.assertIsNone(self.step(runner,at(4.5)))  # two after the second
        self.assertEqual(self.step(runner,at(5.1)),'admitted')
        job=runner.requests[-1]['job_id']  # this one claims its batch: the dig goes on right away again
        claim=self.store.begin_analysis(['work'],120,a.REVIEW_SESSION_PREFIX+job,job)
        self.store.finish_analysis(claim['analysis_id'],'Reviewed',a.REVIEW_SESSION_PREFIX+job,job)
        self.store.commit_page('work',{},[{'account_id':'work','source_id':'two','kind':'gmail.message','occurred_at':a.now(),'title':'Hi','body':'More','metadata':{},'deleted':False}])
        self.assertEqual(self.step(runner,at(6)),'ok')
        self.assertEqual(self.step(runner,at(6.1)),'admitted')

    def test_unconfirmed_start_retries_with_the_same_id_after_a_minute(self):
        runner=Runner('unavailable','admitted')
        self.step(runner,T)
        self.assertIsNone(self.step(runner,T+dt.timedelta(seconds=30)))
        self.step(runner,T+dt.timedelta(minutes=2))
        self.assertEqual(runner.requests[0]['job_id'],runner.requests[1]['job_id'])
        self.assertEqual(runner.requests[1]['action'],'start');self.assertEqual(self.runs()[0]['status'],'running')

    def test_idle_without_reviewable_backlog_or_while_another_review_runs(self):
        with self.store.connect() as db:db.execute('UPDATE events SET deferrals=?',(a.SET_ASIDE_AFTER,))
        self.assertIsNone(self.step(Runner(),T))
        with self.store.connect() as db:
            db.execute('UPDATE events SET deferrals=0')
            db.execute("INSERT INTO analyses(id,started_at,items,status) VALUES('manual',?,'[]','running')",(T.isoformat(),))
        self.assertIsNone(self.step(Runner(),T+dt.timedelta(minutes=5)))
        self.assertEqual(self.runs(),[])

    def test_a_run_that_never_ends_gets_grace_then_exact_stop_before_release(self):
        runner=Runner('admitted','pending','timed_out')
        self.step(runner,T)
        self.step(runner,T+dt.timedelta(minutes=30))
        self.assertEqual(self.runs()[0]['status'],'running')
        self.step(runner,T+dt.timedelta(minutes=36))
        self.assertEqual(runner.requests[-1]['action'],'stop')
        self.assertEqual(self.runs()[0]['status'],'timed_out')

    def test_a_run_lost_in_a_gateway_restart_ends_at_the_next_check_not_after_the_timeout(self):
        runner=Runner('admitted','pending','lost','admitted')
        self.step(runner,T)
        self.step(runner,T+dt.timedelta(minutes=1))
        self.assertNotIn('probe',runner.requests[1])  # just admitted: may still be queued
        self.step(runner,T+dt.timedelta(minutes=3))
        self.assertEqual((runner.requests[2]['action'],runner.requests[2]['probe']),('status',True))
        run=self.runs()[0]
        self.assertEqual((run['status'],run['error']),('lost','runtime_lost'))
        self.step(runner,T+dt.timedelta(minutes=5))  # the next run after the usual back-off, not 35 minutes later
        self.assertEqual(runner.requests[-1]['action'],'start')
        self.assertNotEqual(runner.requests[-1]['job_id'],runner.requests[0]['job_id'])

    def test_a_review_interrupted_mid_batch_by_a_restart_is_resumed_by_the_next_run_never_lost(self):
        # Its turn ends with a fixed line, not NO_REPLY (OpenClaw asked twice more after that); the recovery is the
        # service's own: the lost run's claim moves to the next run, which resumes the same batch
        runner=Runner('admitted','pending','lost','admitted')
        self.step(runner,T)
        self.assertIn('End with exactly the line Done.',runner.requests[0]['message'])
        self.assertNotIn('NO_REPLY',runner.requests[0]['message'])
        old=self.runs()[0]['run_id'];old_session=a.REVIEW_SESSION_PREFIX+old
        with patch_everywhere(a,'now',return_value=(T+dt.timedelta(seconds=30)).isoformat()):
            claim=self.store.begin_analysis(['work','home'],120,old_session,old)
        self.step(runner,T+dt.timedelta(minutes=1))
        self.step(runner,T+dt.timedelta(minutes=3))  # the probe: the Gateway restarted and the run is gone
        self.assertEqual(self.runs()[0]['status'],'lost')
        self.assertEqual(self.store.events(['work'],pending=True)[0]['analyzed_version'],0)  # nothing marked reviewed
        self.step(runner,T+dt.timedelta(minutes=5))
        new=self.runs()[-1]['run_id'];self.assertNotEqual(new,old)
        self.assertEqual(runner.requests[-1]['action'],'start')
        resumed=self.store.begin_analysis(['work','home'],120,a.REVIEW_SESSION_PREFIX+new,new)
        self.assertTrue(resumed['resumed']);self.assertEqual(resumed['analysis_id'],claim['analysis_id'])
        self.store.finish_analysis(claim['analysis_id'],'Reviewed',a.REVIEW_SESSION_PREFIX+new,new)
        self.assertEqual(self.store.events(['work'],pending=True),[])

    def errors(self):
        with self.store.connect() as db:
            a.error_feed.ensure(db)
            return [dict(r) for r in db.execute("SELECT kind,location FROM error_feed WHERE source='review'")]

    def test_a_review_a_gateway_restart_interrupted_is_carried_on_by_restart_recovery_not_reported_lost(self):
        # A Gateway restart (an out-of-memory kill) ends the review's turn; OpenClaw's restart recovery resumes its
        # session a minute later under a new run id. The probe found the run gone first and ended it as runtime_lost:
        # an error report, a failed run in the back-off, and the recovered turn found the claim busy.
        runner=Runner('admitted','absent','pending','absent','absent','lost')
        self.step(runner,T)
        old=self.runs()[0]['run_id'];session=a.REVIEW_SESSION_PREFIX+old
        with patch_everywhere(a,'now',return_value=(T+dt.timedelta(seconds=30)).isoformat()):
            claim=self.store.begin_analysis(['work','home'],120,session,old)
        self.step(runner,T+dt.timedelta(minutes=3))  # the probe, right after the restart: gone, nothing runs there yet
        self.assertEqual(runner.requests[1]['probe'],True)
        run=self.runs()[0];self.assertEqual((run['status'],run['error']),('running','run_absent'))
        recovered='81a266ed-aa86-4b3b-af8c-0de891960330'  # the turn restart recovery started in the same session
        resumed=self.store.begin_analysis(['work','home'],120,session,recovered)
        self.assertTrue(resumed.get('resumed'));self.assertEqual(resumed['analysis_id'],claim['analysis_id'])
        self.step(runner,T+dt.timedelta(minutes=4))  # recovery's turn runs in the session: still this review
        self.assertEqual((self.runs()[0]['status'],self.runs()[0]['error']),('running',None))
        self.store.finish_analysis(claim['analysis_id'],'Reviewed',session,recovered)
        self.assertEqual(self.store.events(['work'],pending=True),[])
        self.step(runner,T+dt.timedelta(minutes=5))  # its turn ended: nothing runs in the session
        self.step(runner,T+dt.timedelta(minutes=7))
        self.assertEqual(runner.requests[-1]['action'],'status')  # within RESTART_RECOVERY_SECONDS of the first sighting
        self.step(runner,T+dt.timedelta(minutes=8,seconds=1))
        self.assertEqual(runner.requests[-1]['action'],'stop')
        run=self.runs()[0];self.assertEqual((run['status'],run['error']),('ok',None))
        self.assertEqual(self.errors(),[])

    def test_a_review_no_restart_recovery_resumes_is_stopped_as_lost_after_the_wait(self):
        runner=Runner('admitted','absent','absent','lost','admitted')
        self.step(runner,T)
        old=self.runs()[0]['run_id'];session=a.REVIEW_SESSION_PREFIX+old
        with patch_everywhere(a,'now',return_value=(T+dt.timedelta(seconds=30)).isoformat()):
            claim=self.store.begin_analysis(['work','home'],120,session,old)
        self.step(runner,T+dt.timedelta(minutes=3))
        self.step(runner,T+dt.timedelta(minutes=5))
        self.assertEqual((runner.requests[-1]['action'],self.runs()[0]['status']),('status','running'))
        self.step(runner,T+dt.timedelta(minutes=6,seconds=1))
        self.assertEqual(runner.requests[-1]['action'],'stop')
        run=self.runs()[0];self.assertEqual((run['status'],run['error']),('lost','runtime_lost'))
        self.assertEqual([e['kind'] for e in self.errors()],['runtime_lost'])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM analyses WHERE id=?',(claim['analysis_id'],)).fetchone()[0],'retryable')
        self.step(runner,T+dt.timedelta(minutes=8))  # the next run takes the batch over
        self.assertEqual(runner.requests[-1]['action'],'start')

    def test_a_turn_in_another_session_never_takes_a_review_claim_over(self):
        # Only a turn in the review's own session carries it on: another session's run stays out (service_run)
        runner=Runner('admitted')
        self.step(runner,T)
        old=self.runs()[0]['run_id']
        claim=self.store.begin_analysis(['work','home'],120,a.REVIEW_SESSION_PREFIX+old,old)
        other='b'*32
        self.assertTrue(self.store.begin_analysis(['work','home'],120,a.REVIEW_SESSION_PREFIX+other,other).get('busy'))
        with self.assertRaises(ValueError):
            self.store.finish_analysis(claim['analysis_id'],'Reviewed',a.REVIEW_SESSION_PREFIX+other,other)
        self.assertTrue(self.store.begin_analysis(['work','home'],120,'agent:main:main','x').get('busy'))

    def test_extended_outage_enters_recovery_and_reconciles_same_run_on_return(self):
        runner=Runner('admitted','unavailable','unavailable','lost','admitted')
        self.step(runner,T)
        self.step(runner,T+dt.timedelta(seconds=11))
        self.assertEqual(self.runs()[0]['status'],'running')
        self.assertIsNone(self.step(runner,T+dt.timedelta(seconds=25)))
        self.step(runner,T+dt.timedelta(minutes=36))
        self.assertEqual(self.runs()[0]['status'],'recovering')
        self.assertEqual(len(self.runs()),1)
        self.assertIsNone(self.step(runner,T+dt.timedelta(minutes=36,seconds=11)))
        self.step(runner,T+dt.timedelta(minutes=38))
        self.assertEqual(runner.requests[-1]['action'],'stop')
        self.assertEqual(self.runs()[0]['status'],'lost')
        self.step(runner,T+dt.timedelta(minutes=40))
        self.assertNotEqual(runner.requests[-1]['job_id'],runner.requests[0]['job_id'])

    def test_failed_claim_transfers_after_a_minute_without_hour_or_batch_wait(self):
        self.app.config['review_worker'].update(min_signals=40,max_wait_minutes=60)
        with self.store.connect() as db:db.execute('UPDATE events SET ingested_at=?',((T-dt.timedelta(hours=2)).isoformat(),))
        runner=Runner('admitted','error','admitted')
        self.step(runner,T)
        old=self.runs()[0]['run_id'];old_session=a.REVIEW_SESSION_PREFIX+old
        with patch_everywhere(a,'now',return_value=T.isoformat()):
            claim=self.store.begin_analysis(['work','home'],120,old_session,old)
        self.step(runner,T+dt.timedelta(minutes=2))
        self.assertIsNone(self.step(runner,T+dt.timedelta(minutes=2,seconds=30)))
        self.step(runner,T+dt.timedelta(minutes=3))
        new=self.runs()[-1]['run_id'];new_session=a.REVIEW_SESSION_PREFIX+new
        resumed=self.store.begin_analysis(['work','home'],120,new_session,new)
        self.assertTrue(resumed['resumed']);self.assertEqual(resumed['analysis_id'],claim['analysis_id'])
        self.assertEqual(self.store.events(['work'],pending=True)[0]['analyzed_version'],0)
        with self.assertRaises(ValueError):self.store.finish_analysis(claim['analysis_id'],'stale',old_session,old)
        self.store.finish_analysis(claim['analysis_id'],'Reviewed',new_session,new)
        self.assertEqual(self.store.events(['work'],pending=True),[])

    def test_unconfirmed_stop_never_transfers_claim_or_launches_a_competitor(self):
        runner=Runner('admitted','unavailable','unavailable')
        self.step(runner,T)
        old=self.runs()[0]['run_id']
        self.store.begin_analysis(['work'],120,a.REVIEW_SESSION_PREFIX+old,old)
        self.step(runner,T+dt.timedelta(minutes=36))
        self.step(runner,T+dt.timedelta(hours=2))
        self.assertEqual(len(self.runs()),1)
        self.assertFalse(any(r['action']=='start' for r in runner.requests[1:]))
        with self.store.connect() as db:self.assertEqual(db.execute('SELECT status FROM analyses').fetchone()[0],'running')
        with self.store.connect() as db:db.execute("UPDATE analyses SET started_at='2020-01-01T00:00:00+00:00'")
        self.assertTrue(self.store.begin_analysis(['work'],120,'manual','new')['busy'])

    def test_waits_for_a_batch_or_the_oldest_signal_to_age(self):
        self.app.config['review_worker'].update(min_signals=40,max_wait_minutes=15)
        with self.store.connect() as db:db.execute('UPDATE events SET ingested_at=?',(T.isoformat(),))
        self.assertIsNone(self.step(Runner(),T+dt.timedelta(minutes=10)))  # 1 signal, 10 minutes old
        self.store.commit_page('work',{},[{'account_id':'work','source_id':str(i),'kind':'gmail.message','occurred_at':a.now(),'title':'Hi','body':'Text','metadata':{},'deleted':False} for i in range(40)])
        self.assertEqual(self.step(Runner('admitted'),T+dt.timedelta(minutes=11)),'admitted')  # 41 waiting

    def test_starts_for_a_single_signal_after_15_minutes(self):
        with self.store.connect() as db:db.execute('UPDATE events SET ingested_at=?',(T.isoformat(),))
        self.app.config['review_worker'].update(min_signals=40)
        self.assertIsNone(self.step(Runner(),T+dt.timedelta(minutes=14)))
        self.assertEqual(self.step(Runner('admitted'),T+dt.timedelta(minutes=16)),'admitted')

    def test_the_old_shipped_60_minutes_in_a_config_means_the_new_default_another_value_is_kept(self):
        # Every install copied "max_wait_minutes": 60 from config.example.json: that was the default, not a choice
        self.assertEqual(a.review_max_wait({'max_wait_minutes':60}),15)
        self.assertEqual(a.review_max_wait({}),15);self.assertEqual(a.review_max_wait(None),15)
        self.assertEqual(a.review_max_wait({'max_wait_minutes':45}),45)
        self.app.config['review_worker'].update(min_signals=40,max_wait_minutes=60)
        with self.store.connect() as db:db.execute('UPDATE events SET ingested_at=?',(T.isoformat(),))
        self.assertEqual(self.step(Runner('admitted'),T+dt.timedelta(minutes=16)),'admitted')

    def test_failed_runs_back_off_instead_of_retrying_every_minute(self):
        with self.store.connect() as db:
            for n,minute in enumerate((0,10,20)):
                stamp=(T+dt.timedelta(minutes=minute)).isoformat()
                db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,finished_at) VALUES(?, 'error', ?, ?, ?)",(f'{n}'*32,stamp,stamp,stamp))
        last=T+dt.timedelta(minutes=20)
        self.assertIsNone(self.step(Runner(),last+dt.timedelta(minutes=3)))  # three failures: wait 4 minutes
        self.assertEqual(self.step(Runner('admitted'),last+dt.timedelta(minutes=5)),'admitted')

    def test_disabled_by_default(self):
        self.app.config.pop('review_worker')
        with patch_everywhere(a,'has_model',return_value=False):  # no first look either (test_first_look)
            self.assertIsNone(self.step(Runner(),T))

    def test_terminal_failure_retains_category_phase_and_saved_claim(self):
        self.step(Runner('admitted'),T)
        run=self.runs()[0]['run_id'];session=a.REVIEW_SESSION_PREFIX+run
        claim=self.store.begin_analysis(['work'],120,session,run)
        self.store.finish_analysis(claim['analysis_id'],'Checked',session,run)
        self.step(lambda request:{'status':'error','error':'model_idle_timeout','error_phase':'model'},T+dt.timedelta(minutes=2))
        row=self.runs()[0]
        self.assertEqual((row['status'],row['error'],row['error_phase']),('error','model_idle_timeout','model'))
        snapshot=self.store.snapshot([]);history=snapshot['review_runs'][0]
        self.assertTrue(history['review_saved']);self.assertEqual(history['checked_count'],1)
        self.assertEqual(history['pending_count'],0);self.assertEqual(history['duration_seconds'],120)
        with self.store.connect() as db:self.assertEqual(db.execute('SELECT status FROM analyses').fetchone()[0],'complete')
        self.assertEqual(self.store.events(['work'],pending=True),[])

    def test_silent_end_on_a_cli_runtime_is_a_finished_review_once_its_batch_saved(self):
        # Claude Code (claude-cli) fails the review's exact NO_REPLY ending as an empty response, after the work
        # (a new Machine on a Claude plan, 2026-10-27): with its batch saved the run is ok, without it still an error.
        silent={'status':'error','error':'runtime_error','error_phase':'runtime','silent_end':True}
        self.step(Runner('admitted'),T)
        run=self.runs()[0]['run_id'];session=a.REVIEW_SESSION_PREFIX+run
        claim=self.store.begin_analysis(['work'],120,session,run)
        self.store.finish_analysis(claim['analysis_id'],'Checked',session,run)
        self.assertEqual(self.step(lambda request:silent,T+dt.timedelta(minutes=2)),'ok')
        row=self.runs()[0]
        self.assertEqual((row['status'],row['error'],row['error_phase'],row['last_error']),('ok',None,None,None))
        with self.store.connect() as db:self.assertEqual(db.execute('SELECT count(*) FROM error_feed').fetchone()[0],0)
        self.store.commit_page('work',{},[{'account_id':'work','source_id':'two','kind':'gmail.message','occurred_at':a.now(),'title':'More','body':'Text','metadata':{},'deleted':False}])
        self.step(Runner('admitted'),T+dt.timedelta(minutes=10))
        run=self.runs()[1]['run_id'];self.store.begin_analysis(['work'],120,a.REVIEW_SESSION_PREFIX+run,run)  # claimed, never finished
        self.assertEqual(self.step(lambda request:silent,T+dt.timedelta(minutes=12)),'error')
        self.assertEqual((self.runs()[1]['status'],self.runs()[1]['error']),('error','runtime_error'))

    def test_failure_history_reports_unfinished_claim_without_raw_errors(self):
        self.step(Runner('admitted'),T)
        run=self.runs()[0]['run_id'];session=a.REVIEW_SESSION_PREFIX+run
        self.store.begin_analysis(['work'],120,session,run)
        self.step(lambda request:{'status':'error','error':'private token=abc','error_phase':'private_url'},T+dt.timedelta(minutes=1))
        row=self.runs()[0]
        self.assertEqual((row['error'],row['error_phase']),('runtime_error','runtime'))
        history=self.store.snapshot([])['review_runs'][0]
        self.assertFalse(history['review_saved']);self.assertEqual(history['pending_count'],1)
        self.assertEqual(history['claimed_count'],1)
        with self.store.connect() as db:self.assertEqual(db.execute('SELECT status FROM analyses').fetchone()[0],'retryable')

    def test_runtime_error_logs_its_reason_from_the_fixed_list_only(self):
        # 2026-10-30: every review failed for hours as a bare runtime_error; the Gateway's MCP runtime limit was the cause.
        self.step(Runner('admitted'),T)
        with self.assertLogs(a.LOG,'WARNING') as logs:
            self.step(lambda request:{'status':'error','error':'runtime_error','error_phase':'runtime','reason':'mcp_runtime_limit'},T+dt.timedelta(minutes=1))
        self.assertIn('error=runtime_error phase=runtime saved_claims=0 reason=mcp_runtime_limit',logs.output[-1])
        self.step(Runner('admitted'),T+dt.timedelta(hours=2))
        with self.assertLogs(a.LOG,'WARNING') as logs:
            self.step(lambda request:{'status':'error','error':'runtime_error','reason':'private token=abc'},T+dt.timedelta(hours=2,minutes=1))
        self.assertNotIn('reason=',logs.output[-1]);self.assertNotIn('private',logs.output[-1])

    def test_success_clears_outage_error_and_history_survives_reopen(self):
        self.step(Runner('admitted','unavailable'),T)
        self.step(Runner('unavailable'),T+dt.timedelta(seconds=11))
        self.step(Runner('ok'),T+dt.timedelta(minutes=2))
        row=self.runs()[0];self.assertIsNone(row['error']);self.assertIsNone(row['error_phase'])
        self.assertEqual((row['last_error'],row['last_error_phase']),('connection_error','connection'))
        self.assertIsNotNone(row['error_at'])
        reopened=a.Store(Path(self.temp.name)/'events.sqlite')
        self.assertEqual(reopened.snapshot([])['review_runs'][0]['run_id'],row['run_id'])

    def test_saved_partial_review_keeps_deferred_signal_visible(self):
        self.step(Runner('admitted'),T)
        run=self.runs()[0]['run_id'];session=a.REVIEW_SESSION_PREFIX+run
        claim=self.store.begin_analysis(['work'],120,session,run)
        self.store.finish_analysis(claim['analysis_id'],'Needs more context',session,run,reviewed_ids=[])
        self.step(Runner('ok'),T+dt.timedelta(minutes=1))
        history=self.store.snapshot([])['review_runs'][0]
        self.assertTrue(history['review_saved']);self.assertEqual(history['checked_count'],0)
        self.assertEqual(history['pending_count'],1)


    def test_a_board_waiting_to_be_sorted_starts_a_review_within_minutes_without_a_full_batch(self):
        import graph
        self.app.config['review_worker'].update(min_signals=40, gap_seconds=600, max_wait_minutes=60)
        with patch_everywhere(a,'now',return_value=T.isoformat()):
            self.store.commit_page('work',{},[{'account_id':'work','source_id':'two','kind':'gmail.message','occurred_at':T.isoformat(),'title':'Hi','body':'Text','metadata':{},'deleted':False}])
        self.assertIsNone(self.step(Runner(),T))  # one young signal: it waits for a batch
        with self.store.connect() as db:
            event=db.execute('SELECT id FROM events ORDER BY id DESC LIMIT 1').fetchone()[0]
            graph.label(db,[event],'Paperkite','review',T.isoformat())
            graph.save_board(db,{'name':'Partners','stages':['Contacted','Live'],'about':'Partners','projects':['Paperkite']},T.isoformat())
        runner=Runner('admitted')
        self.assertEqual(self.step(runner,T+dt.timedelta(minutes=1)),'admitted')
        self.assertIn('Boards to sort',runner.requests[0]['message'])
        self.assertIn(f'Paperkite (project:',runner.requests[0]['message'])

if __name__=='__main__':unittest.main()
