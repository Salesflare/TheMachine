"""Actual Git/SQLite recovery and final-step regressions; no live services/accounts."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import test_self_fix as sf
import test_preparation as p

STEP={'kind':'finish','label':'Submit expense claim','url':'https://expenses.invalid/E42',
      'instructions':'Submit ONLY E42 for EUR 42.50, 16 Oct 2026, Travel, receipt.pdf.',
      'preview':'E42, EUR 42.50, Travel, 16 Oct 2026, receipt.pdf.'}


class Finish(unittest.TestCase):
    setUp=p.Preparation.setUp
    job=p.Preparation.job
    accept=p.Preparation.accept
    def start_finish(self):
        self.accept();self.app.preparation_step(lambda r:{'status':'admitted'})
        self.app.action('prepare',{'suggestion_id':self.sid,'job_id':self.job()['job_id'],'body':'Ready to submit.',
                                  'next_actions':[STEP],'outcome':'needs_you','needs':'Confirm'})
        self.ended()
        with self.store.connect() as db:action=p.a.next_actions.actions(db.execute('SELECT next_action FROM suggestions').fetchone()[0])[0]
        self.app.action('confirm_action',{'suggestion_id':self.sid,'revision':action['revision'],'approval_id':'confirm'},owner_dashboard=True)
        self.app.preparation_step(lambda r:{'status':'admitted'})
        return action

    def ended(self):
        with self.store.connect() as db:db.execute("UPDATE preparation_runs SET status='ok',finished_at=?",(p.a.now(),))

    def message(self):
        calls=[];self.app.preparation_step(lambda r:calls.append(r) or {'status':'admitted'})
        return next(r['message'] for r in calls if r.get('message'))

    def test_finish_owner_retry_retains_exact_contract_after_database_reopen(self):
        self.start_finish();old=self.job()
        self.store.preparation_blocked(self.sid,old['job_id'],'The site is unavailable.');self.ended()
        self.store=p.a.Store(self.store.path);self.app.store=self.store
        self.store.decide(self.sid,'retry','','retry','dashboard')
        message=self.message()
        self.assertIn(STEP['instructions'],message);self.assertIn(STEP['preview'],message)
        self.assertEqual(self.job()['action_id'],old['action_id'])

    def test_finish_auto_continuation_keeps_the_same_action(self):
        self.start_finish();old=self.job();self.ended()
        self.app.preparation_run_step(old,lambda r:{'status':'ok'})
        with self.store.connect() as db:db.execute('UPDATE preparations SET retry_at=NULL')
        message=self.message();self.assertIn(STEP['instructions'],message);self.assertIn(STEP['preview'],message)

    def test_finish_signin_then_confirm_requeues_the_unperformed_step_once(self):
        action=self.start_finish()
        self.app.action('prepare',{'suggestion_id':self.sid,'job_id':self.job()['job_id'],'body':'Sign in; nothing was submitted.',
                                  'next_actions':[STEP],'outcome':'needs_you','needs':'Sign in','finish_state':'not_performed'})
        self.ended()
        with self.store.connect() as db:self.assertEqual(db.execute('SELECT status FROM action_jobs').fetchone()[0],'needs_input')
        result=self.app.action('confirm_action',{'suggestion_id':self.sid,'revision':action['revision'],'approval_id':'after-login'},owner_dashboard=True)
        self.assertEqual(result,{'status':'queued'})
        first=self.job()['job_id']
        with self.assertRaises(ValueError):self.app.action('confirm_action',{'suggestion_id':self.sid,'revision':action['revision'],'approval_id':'double'},owner_dashboard=True)
        self.assertEqual(self.job()['job_id'],first);self.assertIn(STEP['instructions'],self.message())
        with self.store.connect() as db:self.assertEqual(db.execute('SELECT count(*) FROM action_jobs').fetchone()[0],1)

    def test_unknown_finish_is_reconciled_not_blindly_submitted(self):
        action=self.start_finish()
        self.app.action('prepare',{'suggestion_id':self.sid,'job_id':self.job()['job_id'],'body':'The response was lost.',
                                  'next_actions':[STEP],'outcome':'needs_you','needs':'Check outcome'})
        self.ended()
        self.app.action('confirm_action',{'suggestion_id':self.sid,'revision':action['revision'],'approval_id':'check'},owner_dashboard=True)
        message=self.message();self.assertIn('UNKNOWN outcome',message);self.assertIn('do not repeat it',message)
        self.assertIn(STEP['instructions'],message)

    def test_completed_finish_stays_completed_and_its_button_is_hidden(self):
        action=self.start_finish()
        self.app.action('prepare',{'suggestion_id':self.sid,'job_id':self.job()['job_id'],'body':'Submitted; receipt E42-OK.',
                                  'next_actions':[STEP],'outcome':'done','finish_state':'completed'})
        self.ended()
        row=self.store.snapshot([])['suggestions'][0]
        self.assertNotIn(STEP['label'],[b['label'] for block in p.a.controls(row)['blocks'] for b in block['buttons']])
        self.assertTrue(self.app.action('confirm_action',{'suggestion_id':self.sid,'revision':action['revision'],'approval_id':'again'},owner_dashboard=True)['duplicate'])
        self.assertEqual(self.job()['status'],'done')

    def test_new_change_does_not_inherit_old_finish(self):
        self.start_finish();self.ended()
        self.store.decide(self.sid,'other','Draft another claim instead.','change','dashboard')
        message=self.message();self.assertNotIn(STEP['instructions'],message);self.assertIsNone(self.job()['action_id'])

    def test_finish_replaced_by_change_can_be_confirmed_again_after_a_check(self):
        action=self.start_finish();self.ended()
        self.store.decide(self.sid,'other','Use the Travel category.','change','dashboard')
        self.app.preparation_step(lambda r:{'status':'admitted'})
        self.app.action('prepare',{'suggestion_id':self.sid,'job_id':self.job()['job_id'],'body':'Ready again.',
                                  'next_actions':[STEP],'outcome':'needs_you','needs':'Confirm','note_kind':'fact'})
        self.ended()
        row=self.store.snapshot([])['suggestions'][0]
        self.assertIn(STEP['label'],[b['label'] for block in p.a.controls(row)['blocks'] for b in block['buttons']])
        self.assertEqual(self.app.action('confirm_action',{'suggestion_id':self.sid,'revision':action['revision'],'approval_id':'again'},owner_dashboard=True),{'status':'queued'})
        message=self.message();self.assertIn('UNKNOWN outcome',message);self.assertIn(STEP['instructions'],message)
        with self.store.connect() as db:self.assertEqual(db.execute('SELECT count(*) FROM action_jobs').fetchone()[0],1)


class MergeRecovery(unittest.TestCase):
    setUp=sf.AutoMerge.setUp
    merged=sf.AutoMerge.merged
    save=sf.AutoMerge.save
    fix=sf.AutoMerge.fix
    fix_clone=sf.AutoMerge.fix_clone
    transport=sf.AutoMerge.transport
    row=sf.AutoMerge.row
    labels=sf.AutoMerge.labels
    decide=sf.AutoMerge.decide
    setUp_merge=sf.AutoMerge.setUp_merge
    setUp_ux=sf.Merge.setUp_ux
    def test_undo_after_git_commit_interruption_recovers_without_another_revert(self):
        self.merged();self.store.undo_merge(self.sid,'undo','dashboard')
        real=self.transport()
        class Interrupted:
            def revert(self,action):real.revert(action);raise SystemExit('restart before SQLite')
        with self.assertRaises(SystemExit):self.app.undo_step(Interrupted())
        commit=sf.git(self.app_dir,'rev-parse','HEAD');self.assertIn('Machine-Undo:',sf.git(self.app_dir,'show','-s','--format=%B','HEAD'))
        self.store=sf.a.Store(self.store.path);self.app.store=self.store
        self.assertEqual(self.app.undo_step(real),'undone')
        self.assertEqual(sf.git(self.app_dir,'rev-parse','HEAD'),commit)
        with self.store.connect() as db:self.assertEqual(db.execute('SELECT status FROM action_jobs').fetchone()[0],'undone')

    def test_restart_observes_committed_undo_and_effect_receipts(self):
        self.merged();self.store.undo_merge(self.sid,'undo','dashboard')
        observed=[]
        def restart():
            with self.store.connect() as db:
                observed.append((db.execute('SELECT status FROM action_jobs').fetchone()[0],db.execute("SELECT status FROM merge_effects WHERE operation='undo'").fetchone()[0]))
            raise SystemExit('actual restart')
        with self.assertRaises(SystemExit):self.app.undo_step(sf.n.MergeTransport(self.config,restart))
        self.assertEqual(observed,[('undone','done')])
        self.assertIsNone(self.app.undo_step(self.transport()))

    def test_restart_observes_committed_merge_receipt_and_proof(self):
        self.save(self.fix());seen=[]
        def restart():
            with self.store.connect() as db:
                row=db.execute('SELECT status,payload FROM action_jobs').fetchone()
                seen.append((row[0],bool(json.loads(row[1]).get('proof')),db.execute("SELECT status FROM merge_effects WHERE operation='merge'").fetchone()[0]))
            return True
        self.app.action_step(sf.n.ActionTransport(None,None,merge=sf.n.MergeTransport(self.config,restart)))
        self.assertEqual(seen,[('sent',True,'done')])

    def test_unrelated_import_failure_does_not_prove_the_recorded_bug(self):
        clone=self.fix_clone()
        (clone/'graph.py').write_text('def rebuild(rows):\n    return rows["missing"]\n\ndef ping():\n    return "pong"\n')
        (clone/'test_graph.py').write_text('import unittest\nfrom graph import ping\nclass Graph(unittest.TestCase):\n    def test_ping(self):\n        self.assertEqual(ping(),"pong")\n')
        sf.git(clone,'add','.');sf.git(clone,'commit','-qm','Unrelated helper')
        self.save(clone);self.assertEqual(self.app.action_step(sf.next_actions_transport(self)),'blocked')
        self.assertEqual(sf.git(self.app_dir,'log','-1','--format=%s'),'Start');self.assertEqual(self.restarts,[])

    def test_old_version_recurrence_outside_hour_does_not_undo(self):
        head=self.merged();now=sf.a.dt.datetime.fromisoformat(sf.a.now())
        self.store.record_fault('other','TypeError',[],'digest','old')
        with self.store.connect() as db:
            db.execute('UPDATE faults SET first_at=?',((now-sf.a.dt.timedelta(hours=5)).isoformat(),))
            db.execute('UPDATE action_jobs SET updated_at=?',((now-sf.a.dt.timedelta(hours=2)).isoformat(),))
        self.store.record_fault('other','TypeError',[],'digest',head[:12])
        self.assertEqual(self.store.misbehaving_merges(),[])
        self.store.record_fault('fp-graph','KeyError',[],'graph',head[:12])
        self.assertEqual(len(self.store.misbehaving_merges()),1)  # same fixed fault retains 24h rule

    def test_full_diff_remains_exact_when_clone_branch_moves(self):
        clone=self.fix()
        (clone/'large.py').write_text('long_text='+repr('x'*70000)+'\n')
        sf.git(clone,'add','.');sf.git(clone,'commit','-qm','Large change')
        action=sf.n.validate({'kind':'merge','clone':str(clone),'summary':'Large reviewed change.'},self.config,[])
        original=sf.git(clone,'diff',action['base'],action['head'])+'\n'
        self.assertTrue(action['diff_clipped']);self.assertEqual(sf.n.full_merge_diff(action),original)
        (clone/'large.py').write_text('newer=1\n');sf.git(clone,'commit','-qam','Moved clone')
        self.assertEqual(sf.n.full_merge_diff(action),original)

    def test_tracked_edit_during_tests_blocks_activation(self):
        (self.app_dir/'settings.py').write_text('enabled=True\n');sf.git(self.app_dir,'add','.');sf.git(self.app_dir,'commit','-qm','Settings')
        clone=self.fix();action=sf.n.validate({'kind':'merge','clone':str(clone),'summary':'Fix missing keys.'},self.config,[])
        self.config['self_test']=[sys.executable,'-c','from pathlib import Path;import sys;Path(sys.argv[1]).write_text("enabled=False\\n")',str(self.app_dir/'settings.py')]
        with self.assertRaisesRegex(ValueError,'uncommitted'):self.transport().preflight(action)
        self.assertEqual(sf.git(self.app_dir,'rev-parse','HEAD'),action['base']);self.assertEqual(self.restarts,[])

    def test_clone_or_app_edits_after_tests_block_merge(self):
        clone=self.fix();action=sf.n.validate({'kind':'merge','clone':str(clone),'summary':'Fix missing keys.'},self.config,[])
        transport=self.transport();transport.preflight(action)
        (clone/'graph.py').write_text('changed after tests\n')
        self.assertTrue(transport.send(action,{'id':'job'}).get('rejected'))
        self.assertEqual(sf.git(self.app_dir,'rev-parse','HEAD'),action['base'])


if __name__=='__main__':unittest.main()
