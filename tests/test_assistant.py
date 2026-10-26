import importlib.util
import json
import os
import threading
import types
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
assistant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assistant)


def event(account='work', source='one', body='Original'):
    return {'account_id': account, 'source_id': source, 'kind': 'gmail.message',
            'occurred_at': '2026-10-09T10:00:00+00:00', 'title': 'A real subject',
            'body': body, 'metadata': {}, 'deleted': False}


def appointment(source='meeting', start='2026-10-12T09:00:00+02:00'):
    return {'id': source, 'summary': 'Customer meeting', 'status': 'confirmed',
            'start': {'dateTime': start}, 'end': {'dateTime': start.replace('09:00', '10:00')},
            'htmlLink': 'https://calendar.google.com/calendar/event?eid=example',
            'description': '<p>Prepare the pricing proposal</p>'}


class Invariants(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = assistant.Store(Path(self.temp.name) / 'events.sqlite')

    def test_replayed_page_is_idempotent(self):
        for _ in range(3):
            self.store.commit_page('work', {'history_id': '1'}, [event()])
        rows = self.store.events(['work'])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['version'], 1)

    def test_sync_counts_changes_not_duplicates_and_failed_fetches(self):
        account = {'id': 'work', 'email': 'owner@example.com', 'boundary': 'work:Example'}
        with patch.object(assistant, 'now', return_value='2026-10-07T12:00:00+00:00'):
            self.store.commit_page('work', {}, [event(source='old'), event(source='updated')])
        with patch.object(assistant, 'now', return_value='2026-10-09T12:00:00+00:00'):
            self.store.commit_page('work', {}, [event(source='updated', body='Changed'), event(source='new'), event(source='new')])
            state = self.store.snapshot([account])['connectors'][0]
            self.assertEqual(state['last_sync_signals'], 2)
            self.assertEqual(state['signals_24h'], 2)
            self.store.commit_page('work', {'page': 'next'}, [event(source='updated', body='Changed')])
            state = self.store.snapshot([account])['connectors'][0]
            self.assertEqual(state['last_sync_signals'], 0)
            self.assertEqual(state['signals_24h'], 2)
            self.store.failed('work', assistant.SourceError('timeout'))
            self.store.commit_page('work', {'page': 'retry'}, [], record_sync=False)
            state = self.store.snapshot([account])['connectors'][0]
            self.assertEqual(state['last_sync_signals'], 0)
            self.assertEqual(state['last_success'], '2026-10-09T12:00:00+00:00')
            self.assertEqual(state['error'], 'timeout')

    def test_failed_commit_cannot_change_sync_counts(self):
        self.store.commit_page('work', {}, [event()])
        bad=event(source='bad');del bad['title']
        with self.assertRaises(KeyError):self.store.commit_page('work', {}, [event(body='Changed'), bad])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT last_sync_signals FROM checkpoints WHERE account_id='work'").fetchone()[0],1)

    def test_provider_retry_deadline_survives_restart_and_clears_on_success(self):
        self.store.commit_page('work', {'cursor': 'saved'}, [event()])
        with patch.object(assistant, 'now', return_value='2026-10-09T12:00:00+00:00'):
            self.store.failed('work', assistant.SourceError('slack', 429, 120))
        reopened = assistant.Store(Path(self.temp.name) / 'events.sqlite')
        with reopened.connect() as db:
            row = db.execute("SELECT retry_at,last_sync_signals,error FROM checkpoints WHERE account_id='work'").fetchone()
            self.assertEqual(row['retry_at'], '2026-10-09T12:02:00+00:00')
            self.assertEqual(row['last_sync_signals'], 1)
            self.assertEqual(row['error'], 'slack:HTTP_429')
        self.assertEqual(reopened.checkpoint('work')['cursor'], 'saved')
        reopened.commit_page('work', {'cursor': 'next'}, [])
        with reopened.connect() as db:
            row = db.execute("SELECT retry_at,last_sync_signals,error FROM checkpoints WHERE account_id='work'").fetchone()
            self.assertIsNone(row['retry_at'])
            self.assertEqual(row['last_sync_signals'], 0)
            self.assertIsNone(row['error'])

    def test_sync_history_keeps_failure_after_recovery_and_commit_is_atomic(self):
        account={'id':'work','email':'owner@example.com','boundary':'work:Example'}
        with patch.object(assistant,'now',return_value='2026-10-09T12:00:00+00:00'):
            self.store.commit_page('work',{'cursor':'one'},[event()])
        with patch.object(assistant,'now',return_value='2026-10-09T12:01:00+00:00'):
            self.store.failed('work',assistant.SourceError('network',retry_after=300))
        with patch.object(assistant,'now',return_value='2026-10-09T12:06:00+00:00'):
            self.store.commit_page('work',{'cursor':'two'},[])
            view=self.store.snapshot([account])['connectors'][0]
            self.assertIsNone(view['error'])
            self.assertEqual(view['failures_24h'],1)
            self.assertEqual(view['last_failure']['error'],'network')
            self.assertEqual([r['status'] for r in view['sync_activity']],['success','failed','success'])
            self.assertEqual(view['sync_activity'][1]['retry_at'],'2026-10-09T12:06:00+00:00')
            bad=event(source='bad');del bad['title']
            with self.assertRaises(KeyError):self.store.commit_page('work',{},[bad])
            self.store.commit_page('work',{'cursor':'internal'},[],record_sync=False)
            self.assertEqual(len(self.store.snapshot([account])['connectors'][0]['sync_activity']),3)
        reopened=assistant.Store(Path(self.temp.name)/'events.sqlite')
        with patch.object(assistant,'now',return_value='2026-10-11T12:06:00+00:00'):
            self.assertEqual(reopened.snapshot([account])['connectors'][0]['failures_24h'],0)
            self.assertEqual(reopened.snapshot([account])['connectors'][0]['last_failure']['error'],'network')

    def test_failed_commit_rolls_back_events_and_checkpoint(self):
        self.store.commit_page('work', {'history_id': '1'}, [event()])
        bad = event(source='bad'); del bad['title']
        with self.assertRaises(KeyError):
            self.store.commit_page('work', {'history_id': '2'}, [event(body='changed'), bad])
        self.assertEqual(self.store.checkpoint('work')['history_id'], '1')
        self.assertEqual(self.store.events(['work'])[0]['body'], 'Original')

    def test_account_boundaries_and_same_source_id(self):
        self.store.commit_page('work', {}, [event()])
        self.store.commit_page('work2', {}, [event('work2', body='Private')])
        self.assertEqual([r['body'] for r in self.store.events(['work'])], ['Original'])
        self.assertEqual(len(self.store.events(['work', 'work2'])), 2)
        with self.assertRaises(ValueError): self.store.events([])

    def test_update_during_review_remains_pending(self):
        self.store.commit_page('work', {}, [event()])
        review = self.store.begin_analysis(['work'])
        self.store.commit_page('work', {}, [event(body='New reply')])
        self.store.finish_analysis(review['analysis_id'], 'Reviewed original')
        self.assertEqual(len(self.store.events(['work'], pending=True)), 1)
        next_review = self.store.begin_analysis(['work'])
        self.store.finish_analysis(next_review['analysis_id'])
        self.assertEqual(self.store.events(['work'], pending=True), [])

    def test_abandoned_review_replays_and_finish_is_idempotent(self):
        self.store.commit_page('work', {}, [event()])
        first = self.store.begin_analysis(['work'])
        self.assertTrue(self.store.begin_analysis(['work'])['busy'])
        with self.store.connect() as db:
            db.execute("UPDATE analyses SET started_at='2020-01-01' WHERE id=?", (first['analysis_id'],))
        second = self.store.begin_analysis(['work'])
        self.assertEqual(len(second['events']), 1)
        self.store.finish_analysis(second['analysis_id'])
        self.assertTrue(self.store.finish_analysis(second['analysis_id'])['replayed'])

    def test_suggestion_and_click_replay_do_not_duplicate(self):
        self.store.commit_page('work', {}, [event()])
        a = self.store.suggest('work:thread:follow-up', 'Follow up', 'Prepare a reply', [1])
        b = self.store.suggest('work:thread:follow-up', 'Different text', 'Duplicate', [1])
        self.assertEqual(a['id'], b['id']); self.assertTrue(b['duplicate'])
        self.store.decide(a['id'], 'accept', 'Useful', 'callback1', 'telegram')
        self.assertTrue(self.store.decide(a['id'], 'accept', 'Useful', 'callback1', 'telegram')['duplicate'])
        state = self.store.snapshot([])
        self.assertEqual(len(state['decisions']), 1)
        self.assertEqual(state['suggestions'][0]['status'], 'accepted')

    def test_fetch_failure_does_not_advance_cursor(self):
        self.store.commit_page('work', {'mode': 'incremental', 'history_id': '1', 'after': 1}, [event()])
        class Fake:
            def __init__(self, *_):pass
            def profile(self):return {'historyId':'9'}
            def get(self, resource, params):
                if resource=='history':return {'historyId':'9','history':[{'messagesAdded':[{'message':{'id':'new'}}]}]}
                raise assistant.SourceError('network')
        with patch.object(assistant, 'Gmail', Fake):
            with self.assertRaises(assistant.SourceError): assistant.sync_gmail(self.store, {}, {'id':'work'})
        self.assertEqual(self.store.checkpoint('work')['history_id'], '1')

    def test_expired_history_records_replay_not_false_deletion(self):
        self.store.commit_page('work', {'mode':'incremental','history_id':'1','after':100}, [event()])
        class Fake:
            def __init__(self,*_):pass
            def profile(self):return {'historyId':'99'}
            def get(self,*_):raise assistant.SourceError('gmail',404)
        with patch.object(assistant,'Gmail',Fake):
            self.assertEqual(assistant.sync_gmail(self.store, {}, {'id':'work'})['mode'],'resync')
        self.assertEqual(self.store.checkpoint('work')['base_history'],'99')
        self.assertEqual(len(self.store.events(['work'])),1)

    def test_deleted_mail_is_not_suggestible(self):
        self.store.commit_page('work', {}, [event()])
        self.store.commit_page('work', {}, [self.store.tombstone('work','one')])
        self.assertEqual(self.store.events(['work']),[])
        with self.assertRaises(ValueError): self.store.suggest('deleted','No','No',[1])

    def test_uncertain_delivery_not_resent(self):
        self.store.commit_page('work', {}, [event()])
        suggestion=self.store.suggest('one','One','Prepare only',[1])
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='uncertain' WHERE suggestion_id=?",(suggestion['id'],))
        with patch.object(assistant.subprocess,'run') as run:
            assistant.deliver(self.store, {'openclaw':'unused','telegram_owner':'owner'})
            run.assert_not_called()

    def test_verified_no_send_returns_to_queue_without_spacing_or_losing_reminder(self):
        self.store.commit_page('work',{},[event()])
        suggestion=self.store.suggest('retry','Retry','Prepare',[1])
        class Daytime(assistant.dt.datetime):
            @classmethod
            def now(cls,tz=None):return cls(2026,10,10,10,0,tzinfo=tz or assistant.dt.timezone.utc)
        with patch.object(assistant.dt,'datetime',Daytime),patch.object(assistant,'telegram',side_effect=assistant.DeliveryNotSent('gateway_preflight_failed')) as send:
            assistant.deliver(self.store,{'telegram_owner':'owner'});self.assertEqual(send.call_count,1)
        with self.store.connect() as db:
            row=db.execute('SELECT * FROM deliveries WHERE suggestion_id=?',(suggestion['id'],)).fetchone()
            self.assertEqual(row['status'],'queued');self.assertIsNone(row['last_notified_at'])
        with self.store.connect() as db:db.execute("UPDATE deliveries SET updated_at='2020-01-01' WHERE suggestion_id=?",(suggestion['id'],))
        with patch.object(assistant.dt,'datetime',Daytime),patch.object(assistant,'telegram',return_value={'messageId':'888'}):
            assistant.deliver(self.store,{'telegram_owner':'owner'})
        self.assertEqual(self.store.snapshot([])['deliveries'][0]['status'],'sent')

    def test_group_delivery_does_not_suppress_second_card(self):
        self.store.commit_page('work',{},[event()])
        for i in range(3):self.store.suggest('batch'+str(i),'Card'+str(i),'Prepare',[1])
        class Daytime(assistant.dt.datetime):
            @classmethod
            def now(cls,tz=None):return cls(2026,10,10,10,0,tzinfo=tz or assistant.dt.timezone.utc)
        with patch.object(assistant.dt,'datetime',Daytime),patch.object(assistant,'telegram',side_effect=[{'messageId':str(900+i)} for i in range(3)]) as send:
            assistant.deliver(self.store,{'telegram_owner':'owner'});self.assertEqual(send.call_count,3)
        self.assertEqual({r['status'] for r in self.store.snapshot([])['deliveries']},{'sent'})

    def test_deliveries_list_newest_first(self):
        self.store.commit_page('work',{},[event()])
        ids=[self.store.suggest('order'+str(i),'Card'+str(i),'Prepare',[1])['id'] for i in range(3)]
        with self.store.connect() as db:
            for i,sid in enumerate(ids):db.execute('UPDATE deliveries SET updated_at=? WHERE suggestion_id=?',(f'2026-10-0{i+1}T09:00:00+00:00',sid))
        self.assertEqual([d['suggestion_id'] for d in self.store.snapshot([])['deliveries']],ids[::-1])

    def test_bounded_review_is_fair_across_accounts(self):
        self.store.commit_page('work',{},[event(source=str(i)) for i in range(8)])
        self.store.commit_page('work2',{},[event('work2',source=str(i)) for i in range(8)])
        review=self.store.begin_analysis(['work','work2'],limit=4)
        self.assertEqual([r['account_id'] for r in review['events']],['work','work2','work','work2'])

    def test_preparation_needs_real_decision_and_executes_nothing(self):
        self.store.commit_page('work',{},[event()])
        suggestion=self.store.suggest('prepare','Prepare','No action yet',[1])
        with self.assertRaises(ValueError):self.store.prepare(suggestion['id'],'A draft')
        self.store.decide(suggestion['id'],'accept','Please prepare','real-decision','dashboard')
        self.assertEqual(self.store.prepare(suggestion['id'],'A concrete local draft')['status'],'prepared')
        self.assertEqual(self.store.snapshot([])['suggestions'][0]['body'],'A concrete local draft')

    def test_other_normal_reply_and_replay(self):
        self.store.commit_page('work',{},[event()]);s=self.store.suggest('feedback','One','One',[1])
        self.store.request_feedback(s['id'],'click-other',after_message_id='100')
        self.assertTrue(self.store.feedback_reply('Shorter suggestions please','123')['handled'])
        self.assertTrue(self.store.feedback_reply('Shorter suggestions please','123')['duplicate'])
        self.assertFalse(self.store.feedback_reply('Unrelated later message','124')['handled'])
        self.assertEqual(self.store.snapshot([])['decisions'][0]['feedback'],'Shorter suggestions please')

    def test_accept_cancels_pending_feedback(self):
        self.store.commit_page('work',{},[event()]);s=self.store.suggest('feedback','One','One',[1])
        self.store.request_feedback(s['id'],'other',after_message_id='100')
        self.store.decide(s['id'],'accept','','accept','telegram')
        self.assertFalse(self.store.feedback_reply('Normal chat','123')['handled'])

    def test_other_ignores_old_queued_message_and_wrong_reply_target(self):
        self.store.commit_page('work',{},[event()]);s=self.store.suggest('feedback-order','One','One',[1])
        self.store.request_feedback(s['id'],'other',after_message_id='2979',card_message_id='2980')
        self.store.bind_feedback_prompt(s['id'],'other','2982')
        self.assertFalse(self.store.feedback_reply('Earlier browser error','2979')['handled'])
        self.assertFalse(self.store.feedback_reply('Reply to unrelated message','2983',reply_to_id='2978')['handled'])
        self.assertFalse(self.store.feedback_reply('Old timestamp','2984',timestamp=1)['handled'])
        self.assertTrue(self.store.feedback_reply('I fixed it already','2984',reply_to_id='2982')['handled'])
        self.assertEqual(self.store.snapshot([])['suggestions'][0]['latest_feedback']['feedback'],'I fixed it already')

    def test_other_without_safe_message_boundary_does_not_capture_chat(self):
        self.store.commit_page('work',{},[event()]);s=self.store.suggest('feedback-missing','One','One',[1])
        self.store.request_feedback(s['id'],'other')
        self.assertFalse(self.store.feedback_reply('Ordinary chat','1')['handled'])

    def test_incorrect_feedback_annotation_preserves_history_but_not_active_request(self):
        self.store.commit_page('work',{},[event()]);s=self.store.suggest('correction','One','One',[1])
        self.store.decide(s['id'],'other','Wrong unrelated text','wrong','telegram')
        self.store.decide(s['id'],'complete','Already fixed it','right','telegram')
        with self.store.connect() as db:
            db.execute("INSERT INTO decision_annotations VALUES('wrong','misassociated','Earlier message; not a reply','right')")
        snapshot=self.store.snapshot([])
        self.assertEqual(snapshot['suggestions'][0]['latest_feedback']['feedback'],'Already fixed it')
        corrected=next(d for d in snapshot['decisions'] if d['id']=='wrong')
        self.assertEqual(corrected['feedback'],'')
        self.assertEqual(corrected['annotation']['status'],'misassociated')
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT feedback FROM decisions WHERE id='wrong'").fetchone()[0],'Wrong unrelated text')

    def test_edit_cannot_clear_a_newer_preparation(self):
        self.store.commit_page('work', {}, [event()])
        suggestion = self.store.suggest('edit-race', 'One', 'One', [1])
        sid = suggestion['id']
        self.store.decide(sid, 'accept', '', 'owner-click', 'telegram')
        self.store.prepare(sid, 'First short draft')
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='123',needs_edit=1 WHERE suggestion_id=?", (sid,))
        def changed_during_edit(*_, **__):
            self.store.prepare(sid, 'A newer short draft')
            class Result:
                returncode = 0
                stdout = '{"messageId":"123"}' 
            return Result()
        with patch.object(assistant.subprocess, 'run', side_effect=changed_during_edit):
            assistant.deliver(self.store, {'openclaw': 'unused', 'telegram_owner': 'owner'})
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT needs_edit FROM deliveries WHERE suggestion_id=?', (sid,)).fetchone()[0], 1)

    def test_dashboard_decision_updates_existing_telegram_card(self):
        self.store.commit_page('work', {}, [event()])
        sid = self.store.suggest('dashboard-sync', 'One', 'Prepare a reply', [1])['id']
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='123' WHERE suggestion_id=?", (sid,))
        self.store.decide(sid, 'reject', 'Not useful', 'dashboard-click', 'dashboard')
        class Result:
            returncode = 0
            stdout = '{"messageId":"123"}' 
        with patch.object(assistant.subprocess, 'run', return_value=Result()) as run:
            assistant.deliver(self.store, {'openclaw': 'unused', 'telegram_owner': 'owner'})
        command = run.call_args.args[0]
        payload=json.loads(run.call_args.kwargs['input'])
        self.assertEqual(payload['action'],'edit')
        self.assertEqual(payload['messageId'],'123')
        self.assertIn('Not needed.',payload['message'])
        self.assertEqual([b['label'] for b in payload['presentation']['blocks'][0]['buttons']],['Undo'])
        state = self.store.snapshot([])
        self.assertEqual(state['suggestions'][0]['status'], 'rejected')
        self.assertEqual(state['deliveries'][0]['needs_edit'], 0)
        self.assertEqual(state['decisions'][0]['source'], 'dashboard')

    def test_originals_returns_source_messages_without_unsafe_links(self):
        self.store.commit_page('work', {}, [event()])
        sid=self.store.suggest('orig','One','Body',[1])['id']
        [item]=self.store.originals(sid)
        self.assertEqual(item['kind'],'email');self.assertIn('body',item);self.assertIn(item['url'],(None,)) if not str(item['url'] or '').startswith('https://') else None
        with self.store.connect() as db:db.execute("UPDATE events SET metadata=json_set(metadata,'$.source_url','javascript:alert(1)')")
        self.assertIsNone(self.store.originals(sid)[0]['url'])
        with self.assertRaises(ValueError):self.store.originals('missing')

    def test_facts_come_only_from_owner_notes_and_reach_both_prompts(self):
        self.store.commit_page('work', {}, [event()])
        sid=self.store.suggest('translateco','Check TranslateCo','Body',[1])['id']
        self.store.decide(sid,'reject','we stopped using TranslateCo','owner-note','dashboard')
        with self.assertRaises(ValueError):self.store.remember_fact('We stopped using TranslateCo.','made-up-id')
        with self.store.connect() as db:db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,created_at,source) VALUES('agent-note',?,'other','x',?,'agent')",(sid,assistant.now()))
        with self.assertRaises(ValueError):self.store.remember_fact('Agents cannot invent facts.','agent-note')
        first=self.store.remember_fact('  We stopped   using TranslateCo. ','owner-note')
        self.assertTrue(self.store.remember_fact('we stopped using translateco.','owner-note')['duplicate'])
        self.assertEqual(self.store.facts_text(),'- We stopped using TranslateCo.')
        self.assertIn('We stopped using TranslateCo.',assistant.review_prompt('run',['work'],'',self.store.facts_text()))
        self.assertIn('We stopped using TranslateCo.',assistant.preparation_prompt({'suggestion_id':sid,'job_id':'j'},self.store.facts_text()))
        self.assertNotIn('Facts the owner told you',assistant.preparation_prompt({'suggestion_id':sid,'job_id':'j'}))
        self.assertEqual([f['text'] for f in self.store.snapshot([])['facts']],['We stopped using TranslateCo.'])
        app=object.__new__(assistant.App);app.store=self.store;app.config={'accounts':[]}
        with self.assertRaises(ValueError):app.action('forget_fact',{'id':first['id']})
        app.action('forget_fact',{'id':first['id']},owner_dashboard=True)
        self.assertEqual(self.store.facts_text(),'')
        self.assertTrue(self.store.remember_fact('we stopped using translateco.','owner-note')['suppressed'])
        self.assertEqual(self.store.facts_text(),'')
        with self.store.connect() as db:
            db.execute("INSERT INTO decision_annotations(decision_id,status,reason) VALUES('owner-note','excluded','wrong prompt')")
        with self.assertRaises(ValueError):self.store.remember_fact('We use another service now.','owner-note')
        self.assertIn('forget_fact',assistant.OWNER_ACTIONS)

    def test_looks_handled_is_a_hint_that_holds_undelivered_cards(self):
        self.store.commit_page('work', {}, [event(source='ask'),event(source='signed')])
        sid=self.store.suggest('sign','Sign the jury agreement','Body',[1])['id']
        with self.assertRaises(ValueError):self.store.looks_handled(sid,'Signed',[99])
        self.store.looks_handled(sid,'Scrive confirmed the e-signature.',[2])
        row=self.store.snapshot([])['suggestions'][0]
        self.assertEqual(row['status'],'pending')  # never an owner decision
        self.assertIn('Looks handled: Scrive confirmed the e-signature.',assistant.card(row))
        self.assertEqual(assistant.card(row).count('Looks handled'),1)  # one status line, not stacked on another
        with patch.object(assistant.subprocess,'run') as run:
            assistant.deliver(self.store,{'openclaw':'unused','telegram_owner':'owner'})
        run.assert_not_called()
        self.store.decide(sid,'complete','','done-click','dashboard')
        self.assertEqual(self.store.looks_handled(sid,'Signed again later.',[2]),{'skipped':'already closed'})

    def test_telegram_card_keeps_markdown_links_for_telegram_formatting(self):
        # The Gateway turns Markdown into Telegram's HTML (http(s), mailto, tel only), so links pass through untouched.
        self.store.commit_page('work', {}, [event(source='ask')])
        body='Updated your [Google Doc](https://docs.google.com/document/d/abc/edit): removed Sources.'
        self.store.suggest('doc','Agreed to the listing exchange',body,[1])
        row=self.store.snapshot([])['suggestions'][0]
        self.assertIn(body,assistant.card(row))

    def test_any_event_opens_on_its_own_without_a_card(self):
        mine={**event(source='wa',body='See you at 8'),'kind':'whatsapp.message','metadata':{'from_me':True,'chat_name':'Anna'}}
        self.store.commit_page('work', {}, [event(), mine])
        [item]=self.store.event_views(['2'])
        self.assertEqual((item['event_id'],item['from'],item['body']),(2,'You','See you at 8'))
        self.assertEqual([i['event_id'] for i in self.store.event_views([2,1])],[2,1])
        with self.assertRaises(ValueError):self.store.event_views(['nope'])
    def test_originals_follow_the_reviewers_order_main_evidence_first(self):
        old={**event(source='debit',body='Add money'),'title':'Add money for your Direct Debit','occurred_at':'2026-10-12T13:18:00+00:00'}
        new={**event(source='stripe',body='Money in'),'title':'Money received','occurred_at':'2026-10-12T13:24:00+00:00'}
        self.store.commit_page('work', {}, [old,new])
        sid=self.store.suggest('order','Top up','Body',[1,2])['id']
        self.assertEqual([i['title'] for i in self.store.originals(sid)],['Add money for your Direct Debit','Money received'])
        sid=self.store.suggest('order2','Top up','Body',[2,1])['id']
        self.assertEqual(self.store.originals(sid)[0]['title'],'Money received')

    def test_attachments_skip_embedded_images_and_only_serve_this_cards_files(self):
        payload={'parts':[{'partId':'0','mimeType':'text/plain','body':{'data':'aGk='}},
            {'partId':'1','filename':'deck.pdf','mimeType':'application/pdf','body':{'attachmentId':'A1','size':2048},'headers':[{'name':'Content-Disposition','value':'attachment'}]},
            {'partId':'2','filename':'image003.png','mimeType':'image/png','body':{'attachmentId':'A2','size':900},'headers':[{'name':'Content-ID','value':'<cid1>'},{'name':'Content-Disposition','value':'inline'}]},
            {'partId':'3','filename':'photo.jpg','mimeType':'image/jpeg','body':{'data':'AAEC','size':3},'headers':[{'name':'Content-ID','value':'<cid2>'},{'name':'Content-Disposition','value':'attachment'}]}]}
        self.assertEqual([a['name'] for a in assistant.message_attachments(payload)],['deck.pdf','photo.jpg'])
        self.store.commit_page('work', {}, [event()])
        sid=self.store.suggest('att','One','Body',[1])['id']
        with self.store.connect() as db:db.execute("UPDATE events SET kind='gmail.message'")
        app=object.__new__(assistant.App);app.store=self.store;app.config={'accounts':[{'id':'work','email':'o@example.com','transport':'gog','client':'c'}]}
        reads=[]
        def read(config,account,api,version,method,params,scope):
            reads.append((method,scope))
            return {'payload':payload} if method.endswith('messages.get') else {'data':'cGRm'}
        with patch.object(assistant,'gog_read',side_effect=read):
            [item]=app.originals(sid);self.assertEqual([a['part'] for a in item['attachments']],['1','3'])
            self.assertNotIn('gmail',item)
            self.assertEqual(app.attachment(sid,item['event_id'],'1'),(b'pdf','application/pdf','deck.pdf'))
            self.assertEqual(app.attachment(sid,item['event_id'],'3')[0],b'\x00\x01\x02')
            self.assertEqual(app.attachment(sid,item['event_id'],'2')[1],'image/png')  # embedded image, for the HTML view
            self.assertEqual(app.email_view(sid,item['event_id'])['images'],{'cid1':'2','cid2':'3'})
            for bad in [(sid,item['event_id'],'0'),(sid,999,'1')]:
                with self.assertRaises(ValueError):app.attachment(*bad)
        self.assertTrue(all(scope.endswith('gmail.readonly') for _,scope in reads))

    def test_an_undecided_item_can_be_marked_done_without_preparing(self):
        self.store.commit_page('work', {}, [event()])
        sid=self.store.suggest('handled','Two','Already handled',[1])['id']
        row=self.store.snapshot([])['suggestions'][0]
        self.assertIn('Mark done',[b['label'] for block in assistant.controls(row)['blocks'] for b in block['buttons']])
        self.assertEqual(self.store.decide(sid,'complete','','handled-myself','dashboard')['status'],'completed')
        self.store.decide(sid,'reopen','','reopen','dashboard')
        self.assertEqual(self.store.snapshot([])['suggestions'][0]['status'],'pending')
        with self.store.connect() as db:self.assertIsNone(db.execute('SELECT 1 FROM preparations WHERE suggestion_id=?',(sid,)).fetchone())

    def test_mark_done_is_owner_feedback_not_preparation_or_execution(self):
        self.store.commit_page('work', {}, [event()])
        sid=self.store.suggest('completion', 'One', 'Prepare a reply', [1])['id']
        self.store.decide(sid,'accept','','accept','telegram')
        self.store.prepare(sid,'Short draft')
        self.assertEqual(self.store.snapshot([])['suggestions'][0]['status'],'prepared')
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='123' WHERE suggestion_id=?",(sid,))
        self.store.decide(sid,'complete','Finished','done','dashboard')
        self.assertTrue(self.store.decide(sid,'complete','','second-click','dashboard')['duplicate'])
        with self.assertRaises(ValueError):self.store.decide(sid,'accept','','old-telegram-click','telegram')
        with self.assertRaises(ValueError):self.store.request_feedback(sid,'old-other-click')
        with self.assertRaises(ValueError):self.store.prepare(sid,'Stale agent draft')
        class Result:
            returncode=0
            stdout='{"messageId":"123"}' 
        with patch.object(assistant.subprocess,'run',return_value=Result()) as run:
            assistant.deliver(self.store,{'openclaw':'unused','telegram_owner':'owner'})
        command=run.call_args.args[0]
        payload=json.loads(run.call_args.kwargs['input'])
        self.assertEqual(payload['action'],'edit')
        self.assertIn('Done.',payload['message'])
        self.assertEqual(len(self.store.snapshot([])['decisions']),2)
        self.assertEqual(self.store.snapshot([])['suggestions'][0]['status'],'completed')

    def test_snooze_presets_custom_timezone_and_resume_prepared_state(self):
        self.store.commit_page('work',{},[event()])
        sid=self.store.suggest('snooze','One','A draft',[1])['id']
        self.store.decide(sid,'accept','','accept','telegram');self.store.prepare(sid,'Prepared')
        with patch.object(assistant,'now',return_value='2026-10-24T20:00:00+00:00'):
            self.assertEqual(assistant.snooze_time('tomorrow'),'2026-10-25T08:00:00+00:00')
            self.assertEqual(assistant.snooze_time('2h'),'2026-10-24T22:00:00+00:00')
            self.assertEqual(assistant.snooze_time('3d'),'2026-10-27T08:00:00+00:00')
            self.assertEqual(assistant.snooze_time('1w'),'2026-10-31T08:00:00+00:00')
        with patch.object(assistant,'now',return_value='2026-03-27T22:00:00+00:00'):
            self.assertEqual(assistant.snooze_time('3d'),'2026-03-30T07:00:00+00:00')
            self.assertEqual(assistant.snooze_time('1w'),'2026-04-03T07:00:00+00:00')
        with patch.object(assistant,'now',return_value='2026-10-24T20:00:00+00:00'):
            self.store.decide(sid,'snooze','','snooze','dashboard',snoozed_until='2026-10-25T09:30:00+01:00')
            self.assertEqual(self.store.snapshot([])['suggestions'][0]['snoozed_until'],'2026-10-25T08:30:00+00:00')
            with self.assertRaises(ValueError):assistant.snooze_time(explicit='2026-10-24T09:00:00+00:00')
            with self.assertRaises(ValueError):assistant.snooze_time(explicit='2026-10-25T09:30:00')
        self.store.decide(sid,'accept','','bring-back','dashboard')
        self.assertEqual(self.store.snapshot([])['suggestions'][0]['status'],'prepared')

    def test_elapsed_snooze_queues_one_reminder_and_done_cancels_it(self):
        self.store.commit_page('work',{},[event()])
        sid=self.store.suggest('reminder','One','Prepare a reply',[1])['id']
        self.store.decide(sid,'accept','','accept','telegram')
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='123',last_notified_at='2026-10-07' WHERE suggestion_id=?",(sid,))
        with patch.object(assistant,'now',return_value='2026-10-09T10:00:00+00:00'):
            self.store.decide(sid,'snooze','','snooze','dashboard',snooze_option='2h')
        with patch.object(assistant,'now',return_value='2026-10-09T12:01:00+00:00'):
            self.assertEqual(self.store.wake_snoozed(),1)
            self.assertEqual(self.store.wake_snoozed(),0)
        with self.store.connect() as db:
            row=db.execute('SELECT reminder,status FROM deliveries WHERE suggestion_id=?',(sid,)).fetchone()
            self.assertEqual((row['reminder'],row['status']),(1,'queued'))
        self.store.decide(sid,'complete','','done','dashboard')
        with patch.object(assistant,'telegram',return_value={'messageId':'123'}) as send:
            assistant.deliver(self.store,{'telegram_owner':'owner'})
        self.assertTrue(all(call.args[2]=='edit' for call in send.call_args_list))

    def test_snooze_reminder_sends_once_retains_original_and_replay_does_not_spam(self):
        self.store.commit_page('work',{},[event()])
        sid=self.store.suggest('once','One','One',[1])['id']
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='123',last_notified_at='2026-10-01' WHERE suggestion_id=?",(sid,))
            db.execute("UPDATE suggestions SET status='snoozed',snoozed_until='2026-10-01',resume_status='pending' WHERE id=?",(sid,))
        class Daytime(assistant.dt.datetime):
            @classmethod
            def now(cls,tz=None):return cls(2026,10,9,12,tzinfo=assistant.dt.timezone.utc)
        with patch.object(assistant.dt,'datetime',Daytime),patch.object(assistant,'telegram',return_value={'messageId':'456'}) as send:
            assistant.deliver(self.store,{'telegram_owner':'owner'})
            assistant.deliver(self.store,{'telegram_owner':'owner'})
        self.assertEqual([call.args[2] for call in send.call_args_list],['edit','send'])
        state=self.store.snapshot([])
        self.assertEqual(len(state['suggestions']),1)
        self.assertEqual(state['deliveries'][0]['message_id'],'456')
        self.assertEqual(json.loads(state['deliveries'][0]['previous_message_ids']),['123'])

    def test_quiet_hours_defer_snooze_reminder_but_restore_dashboard(self):
        self.store.commit_page('work',{},[event()])
        sid=self.store.suggest('quiet','One','One',[1])['id']
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='123',last_notified_at='2026-10-01' WHERE suggestion_id=?",(sid,))
            db.execute("UPDATE suggestions SET status='snoozed',snoozed_until='2026-10-01' WHERE id=?",(sid,))
        class Night(assistant.dt.datetime):
            @classmethod
            def now(cls,tz=None):return cls(2026,10,9,23,tzinfo=assistant.dt.timezone.utc)
        with patch.object(assistant.dt,'datetime',Night),patch.object(assistant,'telegram',return_value={'messageId':'123'}) as send:
            assistant.deliver(self.store,{'telegram_owner':'owner'})
        self.assertEqual([call.args[2] for call in send.call_args_list],['edit'])
        state=self.store.snapshot([])
        self.assertEqual(state['suggestions'][0]['status'],'pending')
        self.assertEqual(state['deliveries'][0]['status'],'queued')


class CalendarInvariants(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = assistant.Store(Path(self.temp.name) / 'events.sqlite')
        self.account = {'id': 'work-calendar', 'email': 'owner@example.com',
                        'client': 'existing', 'transport': 'gog', 'service': 'calendar'}
        self.clock = patch.object(assistant, 'now', return_value='2026-10-09T12:00:00+00:00')
        self.clock.start(); self.addCleanup(self.clock.stop)

    def source(self, pages):
        calls = []
        class Fake:
            def __init__(self, *_): pass
            def profile(self): return {'id': 'owner@example.com', 'timeZone': 'Europe/Amsterdam'}
            def get(self, method, params):
                calls.append(params)
                item = pages.pop(0)
                if isinstance(item, Exception): raise item
                return item
        return patch.object(assistant, 'Calendar', Fake), calls

    def test_calendar_pages_commit_and_replay_without_duplicates(self):
        fake, calls = self.source([
            {'items': [appointment()], 'nextPageToken': 'page2'},
            assistant.SourceError('timeout'),
            {'items': [appointment('second')], 'nextSyncToken': 'complete'},
            {'items': [appointment('second')], 'nextSyncToken': 'new'}])
        with fake:
            assistant.sync_calendar(self.store, {}, self.account)
            checkpoint = self.store.checkpoint(self.account['id'])
            self.assertEqual(checkpoint['page_token'], 'page2')
            self.assertNotIn('sync_token', checkpoint)
            with self.assertRaises(assistant.SourceError): assistant.sync_calendar(self.store, {}, self.account)
            self.assertEqual(self.store.checkpoint(self.account['id']), checkpoint)
            assistant.sync_calendar(self.store, {}, self.account)
            assistant.sync_calendar(self.store, {}, self.account)
        rows = self.store.events([self.account['id']])
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r['version'] == 1 for r in rows))
        self.assertEqual(calls[-1]['syncToken'], 'complete')
        self.assertNotIn('timeMin', calls[-1]); self.assertNotIn('timeMax', calls[-1])

    def test_complete_calendar_scan_preserves_other_kinds_on_same_account(self):
        other = {'account_id': self.account['id'], 'source_id': 'fleet-question',
                 'kind': 'fleet.request', 'occurred_at': assistant.now(), 'title': 'Question',
                 'body': 'Synthetic team request', 'metadata': {}, 'deleted': False}
        self.store.commit_page(self.account['id'], {}, [other])
        fake, _ = self.source([{'items': [appointment()], 'nextSyncToken': 'complete'}])
        with fake:
            assistant.sync_calendar(self.store, {}, self.account)
        rows = self.store.events([self.account['id']])
        self.assertEqual({r['kind'] for r in rows}, {'fleet.request', 'calendar.event'})
        self.assertEqual(self.store.checkpoint(self.account['id'])['sync_token'], 'complete')

    def test_calendar_expired_token_does_not_delete_until_complete_scan(self):
        fake, _ = self.source([
            {'items': [appointment()], 'nextSyncToken': 'old'},
            assistant.SourceError('calendar', 410),
            {'items': [], 'nextPageToken': 'remaining'},
            {'items': [], 'nextSyncToken': 'replacement'}])
        with fake:
            assistant.sync_calendar(self.store, {}, self.account)
            assistant.sync_calendar(self.store, {}, self.account)
            self.assertEqual(len(self.store.events([self.account['id']])), 1)
            assistant.sync_calendar(self.store, {}, self.account)
            self.assertEqual(len(self.store.events([self.account['id']])), 1)
            assistant.sync_calendar(self.store, {}, self.account)
        self.assertEqual(self.store.events([self.account['id']]), [])
        removed = self.store.events([self.account['id']], pending=True)[0]
        self.assertEqual(removed['metadata']['removal_reason'], 'absent_from_complete_window')
        self.assertNotEqual(removed['metadata']['status'], 'cancelled')

    def test_calendar_cancelled_occurrence_and_moved_meeting(self):
        fake, _ = self.source([
            {'items': [appointment()], 'nextSyncToken': 'one'},
            {'items': [appointment(start='2027-10-12T09:00:00+02:00'),
                       appointment('outside', '2028-10-12T09:00:00+02:00')], 'nextSyncToken': 'two'},
            {'items': [{'id': 'meeting', 'status': 'cancelled'},
                       {'id': 'unknown', 'status': 'cancelled'}], 'nextSyncToken': 'three'}])
        with fake:
            assistant.sync_calendar(self.store, {}, self.account)
            assistant.sync_calendar(self.store, {}, self.account)
            rows = self.store.events([self.account['id']])
            self.assertEqual(len(rows), 1); self.assertTrue(rows[0]['occurred_at'].startswith('2027'))
            assistant.sync_calendar(self.store, {}, self.account)
        self.assertEqual(self.store.events([self.account['id']]), [])
        row = self.store.events([self.account['id']], pending=True)[0]
        self.assertEqual(row['metadata']['status'], 'cancelled')
        self.assertIn('start', row['metadata'])

    def test_calendar_all_day_dst_and_recurring_identity(self):
        raw = appointment('series_20261025')
        raw.update(start={'date': '2026-10-25'}, end={'date': '2026-10-26'},
                   recurringEventId='series', originalStartTime={'date': '2026-10-25'})
        result = assistant.calendar_event(self.account, raw, 'Europe/Amsterdam')
        self.assertEqual(result['occurred_at'], '2026-10-24T22:00:00+00:00')
        self.assertEqual(result['metadata']['end_at'], '2026-10-25T23:00:00+00:00')
        self.assertTrue(result['metadata']['all_day'])
        self.assertEqual(result['metadata']['recurring_event_id'], 'series')

    def test_calendar_next_appointments_first(self):
        rows = [assistant.calendar_event(self.account, appointment(str(day), f'2026-10-{day}T09:00:00+02:00'), 'Europe/Amsterdam')
                for day in ('10', '12', '20')]
        self.store.commit_page(self.account['id'], {}, rows)
        self.assertEqual([r['source_id'] for r in self.store.events([self.account['id']])], ['10', '12', '20'])

    def test_calendar_scope_and_account_fail_closed(self):
        class Result:
            returncode = 6; stderr = 'HTTP 410: private endpoint or token here'; stdout = ''
        with patch.object(assistant, 'credential', return_value='secret'), patch.object(assistant.subprocess, 'run', return_value=Result()) as run:
            with self.assertRaises(assistant.SourceError) as error:
                assistant.Calendar({'gog': 'gog'}, self.account).profile()
            self.assertEqual(str(error.exception), 'calendar:HTTP_410')
            command = run.call_args.args[0]
            self.assertIn('--readonly', command); self.assertIn('--no-input', command)
            self.assertIn('https://www.googleapis.com/auth/calendar.readonly', command)
            self.assertEqual(command[command.index('--account') + 1], self.account['email'])
        with patch.object(assistant, 'gog_read', return_value={'id': 'another@example.com'}):
            with self.assertRaises(assistant.SourceError): assistant.Calendar({}, self.account).profile()

    def test_expired_google_signin_says_so_and_backs_off(self):
        class Result:
            returncode = 4; stdout = ''
            stderr = 'read-only transport: refresh token expired or revoked: oauth2: "invalid_grant" "Token has been expired or revoked."; owner@example.com'
        with patch.object(assistant, 'credential', return_value='secret'), patch.object(assistant.subprocess, 'run', return_value=Result()):
            with self.assertRaises(assistant.SourceError) as error:
                assistant.Calendar({'gog': 'gog'}, self.account).profile()
        self.assertEqual(str(error.exception), 'calendar:google_signin_expired_run_gog_auth_add')
        self.assertNotIn('@', str(error.exception))
        self.assertEqual(error.exception.retry_after, 3600)

    def test_expired_google_signin_shows_the_file_keyring_command(self):
        config = {'credentials': {'gog-password': '~/private/keyring password'}}
        command = assistant.gog_signin_command(config, self.account)
        path = str(Path('~/private/keyring password').expanduser())
        self.assertEqual(command, f"GOG_KEYRING_BACKEND=file GOG_KEYRING_PASSWORD=\"$(cat '{path}')\" gog auth add owner@example.com --client existing")
        self.assertEqual(assistant.gog_signin_command({}, self.account), 'gog auth add owner@example.com --client existing')

    def test_expired_google_signin_retries_once_signed_in_again(self):
        keyring = Path(self.temp.name) / 'keyring'; keyring.mkdir()
        app = object.__new__(assistant.App)
        app.config, app.store, app.stop = {'gog_keyring_dir': str(keyring)}, self.store, threading.Event()
        self.store.failed(self.account['id'], assistant.SourceError('calendar:google_signin_expired_run_gog_auth_add', retry_after=3600))
        with self.store.connect() as db:
            row = db.execute('SELECT retry_at,error,error_at FROM checkpoints WHERE account_id=?', (self.account['id'],)).fetchone()
        token = assistant.gog_token_path(app.config, self.account)
        self.assertEqual(token.parent, keyring)
        token.write_text('old'); os.utime(token, (0, 0))  # written before the failure: keep waiting
        waits = []
        def wait(seconds):
            waits.append(seconds)
            if len(waits) == 2: token.write_text('new')  # the owner signs in again meanwhile
            return False
        app.stop.wait = wait
        self.assertFalse(app.wait_for_retry(self.account, row))
        self.assertEqual(waits, [15, 15])
        with self.store.connect() as db:
            self.assertIsNone(db.execute('SELECT retry_at FROM checkpoints WHERE account_id=?', (self.account['id'],)).fetchone()[0])

    def test_collector_notices_renewed_google_login_without_sleeping_for_the_retry_hour(self):
        keyring = Path(self.temp.name) / 'keyring'; keyring.mkdir()
        app = object.__new__(assistant.App)
        app.config, app.store, app.stop = {'gog_keyring_dir': str(keyring)}, self.store, threading.Event()
        token = assistant.gog_token_path(app.config, self.account)
        token.write_text('old'); os.utime(token, (0, 0))
        waits, calls = [], []
        def wait(seconds):
            waits.append(seconds)
            if len(waits) == 2: token.write_text('renewed')
            return app.stop.is_set()
        def sync(store, config, account):
            calls.append(account['id'])
            if len(calls) == 1:
                raise assistant.SourceError('calendar:google_signin_expired_run_gog_auth_add', retry_after=3600)
            store.commit_page(account['id'], {'mode': 'incremental', 'cursor': 'kept'}, [])
            app.stop.set()
            return {'mode': 'incremental', 'events': 0}
        app.stop.wait = wait
        with patch.object(app, 'resume_wait', return_value=0), patch.object(assistant, 'sync_source', side_effect=sync):
            app.collector(self.account)
        self.assertEqual(calls, [self.account['id'], self.account['id']])
        self.assertEqual(waits[:2], [15, 15])
        with self.store.connect() as db:
            row = db.execute('SELECT error,retry_at FROM checkpoints WHERE account_id=?', (self.account['id'],)).fetchone()
        self.assertIsNone(row['error']); self.assertIsNone(row['retry_at'])
        self.assertEqual(self.store.checkpoint(self.account['id'])['cursor'], 'kept')

    def test_collector_still_honors_rate_limit_backoff(self):
        app = object.__new__(assistant.App)
        app.config, app.store, app.stop = {}, self.store, threading.Event()
        waits = []
        def wait(seconds):
            waits.append(seconds); app.stop.set(); return True
        app.stop.wait = wait
        with patch.object(app, 'resume_wait', return_value=0), patch.object(assistant, 'sync_source',
                side_effect=assistant.SourceError('calendar', 429, retry_after=3600)) as sync:
            app.collector(self.account)
        self.assertEqual(sync.call_count, 1)
        self.assertEqual(waits, [3600])

    def test_shared_calendar_is_exact_and_credentials_stay_separate(self):
        account = {**self.account, 'calendar_id': 'shared@example.com', 'boundary': 'personal:shared'}
        with patch.object(assistant, 'gog_read', return_value={'id': 'shared@example.com'}) as read:
            source = assistant.Calendar({}, account)
            source.profile()
            self.assertEqual(read.call_args.args[1]['email'], 'owner@example.com')
            self.assertEqual(read.call_args.args[5]['calendarId'], 'shared@example.com')
            with self.assertRaises(assistant.SourceError): source.get('events.insert', {})
            with self.assertRaises(assistant.SourceError): source.get('events.list', {'calendarId': 'other@example.com'})
        with patch.object(assistant, 'gog_read', return_value={'id': 'other@example.com'}):
            with self.assertRaises(assistant.SourceError): assistant.Calendar({}, account).profile()
        e = assistant.calendar_event(account, appointment(), 'Europe/Amsterdam')
        self.assertEqual(e['metadata']['calendar_id'], 'shared@example.com')
        self.assertEqual(e['metadata']['credential_account'], 'owner@example.com')

    def test_birthday_exclusion_replay_and_existing_cleanup(self):
        normal = appointment('normal')
        birthday = appointment('birthday'); birthday['summary'] = "Alex’s Birthday"
        self.store.commit_page(self.account['id'], {}, [assistant.calendar_event(self.account, birthday, 'Europe/Amsterdam')])
        review = self.store.begin_analysis([self.account['id']])
        account = {**self.account, 'excluded_title_terms': ["'s birthday"]}
        other = {**self.account, 'id': 'other'}
        self.store.commit_page(other['id'], {}, [assistant.calendar_event(other, birthday, 'Europe/Amsterdam')])
        fake, _ = self.source([{'items': [birthday, normal], 'nextSyncToken': 'one'},
                               {'items': [birthday], 'nextSyncToken': 'two'}])
        with fake:
            result = assistant.sync_calendar(self.store, {}, account)
            assistant.sync_calendar(self.store, {}, account)
        self.assertEqual(result['filtered'], 1)
        self.assertEqual([r['source_id'] for r in self.store.events([account['id']])], ['normal'])
        self.assertEqual(len(self.store.events([other['id']])), 1)
        self.assertEqual(self.store.checkpoint(account['id'])['sync_token'], 'two')
        with self.store.connect() as db:
            items = json.loads(db.execute('SELECT items FROM analyses WHERE id=?', (review['analysis_id'],)).fetchone()[0])
            self.assertTrue(items[0]['excluded'])
        self.assertFalse(assistant.calendar_title_excluded(account, 'Birthday planning'))
        self.assertFalse(assistant.calendar_title_excluded(self.account, "Alex's birthday"))
        self.store.commit_page(account['id'], self.store.checkpoint(account['id']), [assistant.calendar_event(account, birthday, 'Europe/Amsterdam')])
        checkpoint = self.store.checkpoint(account['id'])
        self.assertEqual(self.store.purge_calendar_exclusions(account), {'removed': 1})
        self.assertEqual(self.store.purge_calendar_exclusions(account), {'removed': 0})
        self.assertEqual(self.store.checkpoint(account['id']), checkpoint)

    def test_calendar_daily_refresh_waits_for_incremental_pages(self):
        fake, calls = self.source([
            {'items': [appointment()], 'nextSyncToken': 'one'},
            {'items': [], 'nextPageToken': 'page2'},
            {'items': [], 'nextSyncToken': 'two'},
            {'items': [appointment()], 'nextSyncToken': 'fresh'}])
        with fake:
            assistant.sync_calendar(self.store, {}, self.account)
            assistant.sync_calendar(self.store, {}, self.account)
            self.clock.stop()
            with patch.object(assistant, 'now', return_value='2026-10-11T12:00:00+00:00'):
                assistant.sync_calendar(self.store, {}, self.account)
                self.assertEqual(calls[-1]['pageToken'], 'page2')
                assistant.sync_calendar(self.store, {}, self.account)
                self.assertIn('timeMin', calls[-1]); self.assertNotIn('syncToken', calls[-1])

    def test_calendar_missing_cursor_does_not_commit_page(self):
        fake, _ = self.source([{'items': [appointment()]}])
        with fake:
            with self.assertRaises(assistant.SourceError): assistant.sync_calendar(self.store, {}, self.account)
        self.assertEqual(self.store.events([self.account['id']]), [])
        self.assertEqual(self.store.checkpoint(self.account['id'])['mode'], 'bootstrap')


# Conversations never rest between rounds here, as before slack_interval existed.
RESTLESS = {'slack_active_minutes': 0, 'slack_recent_hours': 0, 'slack_quiet_hours': 0, 'slack_dm_check_minutes': 0}


class SlackInvariants(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = assistant.Store(Path(self.temp.name) / 'events.sqlite')
        self.account = {'id': 'work-slack', 'email': 'owner@example.com', 'slack_host': 'example.slack.com',
                        'team_id': 'T1', 'user_id': 'U1', 'connection_id': 'connection',
                        'service': 'slack', 'boundary': 'work:Example'}
        self.channel = {'id': 'C1', 'name': 'team', 'type': 'channel', 'threads': []}

    def state(self, **changes):
        state = {'mode': 'bootstrap', 'phase': 'scan', 'channels': [self.channel],
                 'after': '1000.000000', 'index': 0, 'next_discovery': assistant.time.time()+86400}
        state.update(changes); self.store.commit_page(self.account['id'], state, [])

    def source(self, responses):
        calls = []
        class Fake:
            def profile(self): pass
            def get(self, method, params):
                calls.append((method, params.copy()));r=responses.pop(0)
                if isinstance(r, Exception):raise r
                return r
        return Fake(), calls

    def test_slack_threads_and_pages_are_atomic_and_idempotent(self):
        self.state()
        parent = {'ts': '2000.000001', 'text': 'Prepare a proposal', 'reply_count': 1}
        reply = {'ts': '2001.000001', 'thread_ts': parent['ts'], 'text': 'Updated deadline'}
        source, calls = self.source([
            {'messages': [parent], 'response_metadata': {'next_cursor': 'page2'}},
            assistant.SourceError('network'), {'messages': []},
            {'messages': [parent, reply]}, {'messages': [parent]}, {'messages': [parent, reply]}])
        assistant.sync_slack(self.store, RESTLESS, self.account, source)
        cp = self.store.checkpoint(self.account['id'])
        with self.assertRaises(assistant.SourceError):assistant.sync_slack(self.store, RESTLESS, self.account, source)
        self.assertEqual(self.store.checkpoint(self.account['id']), cp)
        for _ in range(4):assistant.sync_slack(self.store, RESTLESS, self.account, source)
        rows = self.store.events([self.account['id']]);self.assertEqual(len(rows), 2)
        self.assertTrue(all(r['version'] == 1 for r in rows))
        self.assertEqual(calls[3][0], 'conversations.replies')
        self.assertEqual(calls[3][1]['ts'], parent['ts'])
        self.assertEqual(self.store.checkpoint(self.account['id'])['mode'], 'incremental')

    def test_slack_first_pass_reads_every_conversation_before_thread_replies(self):
        other = {'id': 'C2', 'name': 'other', 'type': 'channel', 'threads': []}
        self.state(channels=[self.channel, other])
        now = assistant.time.time()
        parent = {'ts': f'{now - 3600:.6f}', 'text': 'Prepare a proposal', 'reply_count': 1}
        reply = {'ts': f'{now - 1800:.6f}', 'thread_ts': parent['ts'], 'text': 'Updated deadline'}
        source, calls = self.source([{'messages': [parent]}, {'messages': [{'ts': f'{now - 60:.6f}', 'text': 'Hello'}]},
                                     {'messages': []}, {'messages': [parent, reply]}])
        assistant.sync_slack(self.store, RESTLESS, self.account, source)
        assistant.sync_slack(self.store, RESTLESS, self.account, source)
        self.assertEqual([(m, p['channel']) for m, p in calls], [('conversations.history', 'C1'), ('conversations.history', 'C2')])
        cp = self.store.checkpoint(self.account['id'])
        self.assertEqual(cp['mode'], 'incremental')
        self.assertTrue(cp['channels'][0]['threads_waiting'])
        self.assertEqual(cp['channels'][0]['threads'], [parent['ts']])
        assistant.sync_slack(self.store, RESTLESS, self.account, source)  # C1 again: its new messages, then the thread
        assistant.sync_slack(self.store, RESTLESS, self.account, source)
        self.assertEqual(calls[3][0], 'conversations.replies')
        self.assertEqual(calls[3][1]['ts'], parent['ts'])
        self.assertLess(float(calls[3][1]['oldest']), float(parent['ts']))  # the whole window, not the overlap
        self.assertNotIn('threads_waiting', self.store.checkpoint(self.account['id'])['channels'][0])
        self.assertEqual(len(self.store.events([self.account['id']])), 3)

    def test_slack_missing_cursor_cannot_finish_a_scan(self):
        self.state();source, _ = self.source([{'messages': [{'ts': '2000.000001', 'text': 'Hello'}], 'has_more': True}])
        with self.assertRaises(assistant.SourceError):assistant.sync_slack(self.store, RESTLESS, self.account, source)
        self.assertEqual(self.store.events([self.account['id']]), [])
        self.assertNotIn('last_scan', self.store.checkpoint(self.account['id'])['channels'][0])

    def test_slack_edits_and_explicit_deletion(self):
        self.state();source, _ = self.source([
            {'messages': [{'ts': '2000.000001', 'text': 'Original'}]},
            {'messages': [{'ts': '2000.000001', 'text': 'Edited', 'edited': {'ts': '2001.000001'}}]},
            {'messages': [{'subtype': 'message_deleted', 'deleted_ts': '2000.000001'}]}])
        assistant.sync_slack(self.store, RESTLESS, self.account, source)
        assistant.sync_slack(self.store, RESTLESS, self.account, source)
        self.assertEqual(self.store.events([self.account['id']])[0]['version'], 2)
        assistant.sync_slack(self.store, RESTLESS, self.account, source)
        self.assertEqual(self.store.events([self.account['id']]), [])

    def test_slack_membership_discovery_dedupes_and_does_not_open_dms(self):
        source, calls = self.source([
            {'channels': [{'id': 'D1', 'is_im': True, 'user': 'U1'}], 'response_metadata': {'next_cursor': 'more'}},
            {'channels': [{'id': 'D1', 'is_im': True, 'user': 'U1'}, {'id': 'C1', 'name': 'team'}]}])
        assistant.sync_slack(self.store, RESTLESS, self.account, source)
        assistant.sync_slack(self.store, RESTLESS, self.account, source)
        cp=self.store.checkpoint(self.account['id'])
        self.assertEqual(len(cp['channels']), 2)
        self.assertEqual(cp['channels'][0]['name'], 'My notes')
        self.assertTrue(all(m=='users.conversations' for m,_ in calls))
        self.assertEqual(calls[0][1]['user'], 'U1')

    def test_slack_unavailable_channel_is_visible_not_successful(self):
        self.state();source, _=self.source([assistant.SourceError('slack_not_in_channel')])
        with self.assertRaises(assistant.SourceError):assistant.sync_slack(self.store, RESTLESS, self.account, source)
        health=self.store.snapshot([self.account])['connectors'][0]
        self.assertEqual(health['conversation_errors'], 1)
        self.assertEqual(health['conversations_collected'], 0)

    def test_slack_api_blocks_writes_and_wrong_identity(self):
        client=assistant.Slack({},self.account)
        with self.assertRaises(assistant.SourceError):client.get('chat.postMessage')
        with patch.object(client,'get',return_value={'team_id':'OTHER','user_id':'U1'}):
            with self.assertRaises(assistant.SourceError):client.profile()
        with patch.object(client,'get',side_effect=[{'team_id':'T1','user_id':'U1'}, {'user':{'profile':{'email':'other@example.com'}}}]):
            with self.assertRaises(assistant.SourceError):client.profile()

    def test_slack_rate_pacing_and_restart_warmup(self):
        with patch.object(assistant.time, 'monotonic', return_value=100), patch.object(assistant.time, 'sleep') as sleep:
            client = assistant.Slack({}, self.account)
            client.pace('conversations.replies')
            sleep.assert_called_with(180)
        with patch.object(assistant.time, 'monotonic', return_value=110), patch.object(assistant.time, 'sleep') as sleep:
            client.pace('conversations.history')  # history and replies share one budget
            sleep.assert_called_with(170)
        with patch.object(assistant.time, 'monotonic', return_value=111), patch.object(assistant.time, 'sleep') as sleep:
            client.pace('conversations.info')  # not limited to one a minute: only the 2-second spacing
            sleep.assert_called_with(1)
        with patch.object(assistant.time, 'monotonic', return_value=200), patch.object(assistant.time, 'sleep') as sleep:
            restarted = assistant.Slack({'slack_read_seconds': 30}, self.account)  # never below Slack's own minute
            restarted.pace('conversations.history')
            sleep.assert_called_with(65)

    def test_slack_wait_cancels_before_request_on_shutdown(self):
        import threading
        stop = threading.Event(); stop.set()
        client = assistant.Slack({}, self.account, stop)
        with patch.object(assistant.urllib.request, 'urlopen') as fetch:
            with self.assertRaises(assistant.SourceError):client.get('conversations.replies')
            fetch.assert_not_called()

    def test_slack_network_diagnostic_keeps_only_class_and_read_method(self):
        account={**self.account,'credential':'slack','credential_variable':'KEY'}
        client=assistant.Slack({},account)
        with patch.object(client,'pace'),patch.object(assistant,'credential',return_value='KEY=secret'):
            for error,name in [(TimeoutError('private endpoint and secret'),'TimeoutError'),
                               (assistant.urllib.error.URLError(ConnectionResetError('private endpoint')),'ConnectionResetError')]:
                with patch.object(assistant.urllib.request,'urlopen',side_effect=error):
                    with self.assertRaises(assistant.SourceError) as raised:client.get('conversations.replies')
                    self.assertEqual(str(raised.exception),'network:'+name+':conversations.replies')
                    self.assertNotIn('private',str(raised.exception))

    def test_slack_rate_limit_identifies_method_without_content(self):
        account={**self.account,'credential':'slack','credential_variable':'KEY'}
        client=assistant.Slack({},account)
        error=assistant.urllib.error.HTTPError('https://private.invalid',429,'private text',{'Retry-After':'120'},None)
        with patch.object(client,'pace'),patch.object(assistant,'credential',return_value='KEY=fake'),patch.object(assistant.urllib.request,'urlopen',side_effect=error):
            with self.assertRaises(assistant.SourceError) as raised:client.get('conversations.replies')
        self.assertEqual(str(raised.exception),'slack:conversations.replies:HTTP_429')
        self.assertTrue(125 <= raised.exception.retry_after <= 180)  # Slack's wait plus a spread so computers sharing the connection don't retry together

    def test_slack_old_known_thread_is_refreshed_after_overlap(self):
        self.channel.update(last_scan='40000.000001',next_full=assistant.time.time()+86400,threads=['1100.000001'])
        self.state(mode='incremental');source,calls=self.source([
            {'messages': []}, {'messages':[{'ts':'40001.000001','thread_ts':'1100.000001','text':'New reply to old topic'}]}])
        config={'slack_thread_retention_days':10**6}  # epoch-era fixture timestamps
        assistant.sync_slack(self.store,config,self.account,source)
        assistant.sync_slack(self.store,config,self.account,source)
        self.assertEqual(calls[1][0],'conversations.replies')
        self.assertEqual(calls[1][1]['ts'],'1100.000001')
        self.assertEqual(len(self.store.events([self.account['id']])),1)


if __name__ == '__main__': unittest.main()


class ModelUsage(unittest.TestCase):
    def test_only_names_labels_percentages_and_reset_times_are_kept(self):
        reply = {'providers': [{'provider': 'openai', 'displayName': 'OpenAI', 'plan': 'plus', 'accountEmail': 'someone@example.com',
                                'windows': [{'label': '5h', 'usedPercent': 41.6, 'resetAt': 1793008294000}, {'label': 'Week', 'usedPercent': 180}]},
                               {'provider': 'xai', 'windows': [], 'error': 'Timeout'}]}
        run = lambda command, **kw: types.SimpleNamespace(stdout=json.dumps(reply))
        usage = assistant.model_usage({'openclaw': '/bin/openclaw'}, run=run)
        self.assertEqual(usage, [{'provider': 'openai', 'name': 'OpenAI', 'windows': [{'label': '5h', 'used': 42, 'reset': 1793008294},
                                                                                       {'label': 'Week', 'used': 100, 'reset': None}]}])
        self.assertNotIn('example.com', json.dumps(usage))
        self.assertIsNone(assistant.model_usage({}, run=lambda command, **kw: types.SimpleNamespace(stdout='gateway timeout')))



import os
import time

FAKE_CODEX = r"""#!/usr/bin/env python3
import json, os, sys
log = open(os.environ['FAKE_CODEX_LOG'], 'a')
email = os.environ.get('FAKE_CODEX_EMAIL', 'someone@example.com')
for line in sys.stdin:
    msg = json.loads(line)
    log.write(json.dumps(msg) + chr(10)); log.flush()
    if 'id' not in msg:
        continue
    m = msg['method']
    result = ({'userAgent': 'fake'} if m == 'initialize' else
              {'account': {'type': 'chatgpt', 'email': email, 'planType': 'plus'}} if m == 'account/read' else
              {'ordinaryUsageAllowed': False, 'rateLimitResetCredits': {'availableCount': 2, 'credits': [
                  {'id': 'c1', 'status': 'available', 'title': 'Full reset', 'expiresAt': 1800000000},
                  {'id': 'c0', 'status': 'redeemed'}]}} if m == 'account/rateLimits/read' else
              {'outcome': 'reset'} if m == 'account/rateLimitResetCredit/consume' else None)
    print(json.dumps({'id': msg['id'], 'result': result} if result else {'id': msg['id'], 'error': {'message': 'no'}}), flush=True)
"""


class ModelResets(unittest.TestCase):
    """The resets come from the Codex CLI's own app-server (mocked here: a fake one speaking its JSON-RPC), only when
    it is signed in to the account OpenClaw uses. Nothing reaches the network."""
    reply = {'providers': [{'provider': 'openai', 'plan': 'plus', 'accountEmail': 'Someone@example.com',
                            'windows': [{'label': '5h', 'usedPercent': 100, 'resetAt': (int(time.time()) + 3600) * 1000}]}]}

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.codex = Path(self.dir.name) / 'codex'
        self.codex.write_text(FAKE_CODEX)
        self.codex.chmod(0o755)
        self.log = Path(self.dir.name) / 'log'
        os.environ['FAKE_CODEX_LOG'] = str(self.log)
        os.environ.pop('FAKE_CODEX_EMAIL', None)
        self.config = {'codex': str(self.codex), 'openclaw_config': str(Path(self.dir.name) / 'openclaw.json')}
        Path(self.config['openclaw_config']).write_text(json.dumps({'agents': {'defaults': {'model': {'primary': 'openai/example'}}}}))

    def tearDown(self):
        self.dir.cleanup()

    def sent(self):
        return [json.loads(l)['method'] for l in self.log.read_text().splitlines()]

    def test_reads_the_resets_from_the_same_account_and_keeps_no_ids(self):
        resets = assistant.model_resets(self.config, self.reply)
        self.assertEqual(resets, {'available': 2, 'credits': [{'title': 'Full reset', 'expires': 1800000000}], 'allowed': False})
        self.assertEqual(self.sent(), ['initialize', 'initialized', 'account/read', 'account/rateLimits/read'])
        usage = assistant.model_usage({}, reply=self.reply)
        status = assistant.model_status(self.config, self.reply, usage, resets)
        self.assertEqual((status['model'], status['provider'], status['plan'], status['chatgpt']), ('openai/example', 'openai', 'plus', True))
        self.assertTrue(status['limit_reached'])
        self.assertEqual(status['limit_resets_at'], usage[0]['windows'][0]['reset'])
        self.assertTrue(status['can_reset'])
        self.assertEqual(status['usage_page'], 'https://chatgpt.com/codex/cloud/settings/usage')
        self.assertNotIn('example.com', json.dumps(status))

    def test_another_account_is_not_read_and_cannot_be_reset(self):
        os.environ['FAKE_CODEX_EMAIL'] = 'other@example.com'
        self.assertIsNone(assistant.model_resets(self.config, self.reply))
        self.assertNotIn('account/rateLimits/read', self.sent())
        with self.assertRaisesRegex(ValueError, 'Use a reset in ChatGPT'):
            assistant.use_model_reset(self.config, self.reply, 'same-click-0002')
        self.assertNotIn('account/rateLimitResetCredit/consume', self.sent())
        status = assistant.model_status(self.config, self.reply, assistant.model_usage({}, reply=self.reply), None)
        self.assertFalse(status['can_reset'])
        self.assertTrue(status['limit_reached'])

    def test_using_a_reset_sends_the_idempotency_key(self):
        click = 'same-click-0001'
        self.assertEqual(assistant.use_model_reset(self.config, self.reply, click), 'reset')
        consume = [json.loads(l) for l in self.log.read_text().splitlines() if 'consume' in l]
        self.assertEqual(consume[0]['params']['idempotencyKey'], click)

    def test_a_claude_plan_through_claude_code_is_named_as_such(self):
        path = Path(self.config['openclaw_config'])
        self.assertFalse(assistant.model_status(self.config, {'providers': []}, None, None)['claude_plan'])
        path.write_text(json.dumps({'agents': {'defaults': {'model': {'primary': 'anthropic/claude-sonnet-9-1'},
                                                            'models': {'anthropic/*': {'agentRuntime': {'id': 'claude-cli'}}}}}}))
        self.assertTrue(assistant.model_status(self.config, {'providers': []}, None, None)['claude_plan'])
        path.write_text(json.dumps({'agents': {'defaults': {'model': 'anthropic/claude-sonnet-9-1',
                                                            'models': {'anthropic/claude-sonnet-9-1': {'agentRuntime': {'id': 'openclaw'}},
                                                                       'anthropic/*': {'agentRuntime': {'id': 'claude-cli'}}}}}}))
        self.assertFalse(assistant.model_status(self.config, {'providers': []}, None, None)['claude_plan'])  # an API key route

    def test_without_a_codex_cli_nothing_is_known(self):
        self.assertIsNone(assistant.model_resets({'codex': str(Path(self.dir.name) / 'missing')}, self.reply))
        self.assertIsNone(assistant.model_resets({'codex': False}, self.reply))
        status = assistant.model_status({}, {'providers': []}, None, None)
        self.assertFalse(status['limit_reached'])
        self.assertIsNone(status['usage_page'])

    def test_a_silent_app_server_hits_the_deadline(self):
        self.codex.write_text('#!/bin/sh\nsleep 30\n')
        started = time.time()
        self.assertIsNone(assistant.model_resets(self.config, self.reply, server_factory=lambda c: assistant.CodexAppServer(c, timeout=1)))
        self.assertLess(time.time() - started, 10)

    def test_dashboard_only_actions(self):
        self.assertIn('model_reset', assistant.OWNER_ACTIONS)
        self.assertIn('model_usage_refresh', assistant.OWNER_ACTIONS)

class NeedsYou(unittest.TestCase):
    def test_unfinished_sources_and_hosting_notes_show_on_the_dashboard(self):
        with tempfile.TemporaryDirectory() as folder:
            notes = Path(folder) / 'needs-you.json'
            notes.write_text(json.dumps([{'id': 'connector-linear', 'text': 'Your Linear connector is ready.',
                                          'url': 'https://app.example.com/setup#source-linear', 'action': 'Connect it'},
                                         {'text': 'Not a safe link', 'url': 'javascript:alert(1)'}, 'junk']))
            config = {'manage_url': 'https://app.example.com/setup', 'needs_you_file': str(notes), 'credentials': {},
                      'accounts': [{'id': 'work-slack', 'service': 'slack', 'credential': 'maton', 'display_name': 'Work Slack'}]}
            items = assistant.needs_you(config)
        self.assertEqual(items[0]['url'], 'https://app.example.com/setup#sources')
        self.assertIn('Work Slack is not fully set up yet', items[0]['text'])
        self.assertEqual(items[1], {'id': 'connector-linear', 'text': 'Your Linear connector is ready.',
                                    'url': 'https://app.example.com/setup#source-linear', 'action': 'Connect it'})
        self.assertIsNone(items[2]['url'])
        self.assertEqual(len(items), 3)
        self.assertEqual(assistant.needs_you({'accounts': []}), [])

class BrowserFailureDiagnostics(unittest.TestCase):
    def test_fixed_codes_never_keep_page_or_account_details(self):
        for text,want in [('X read failed: web client token not found','x_query_unavailable'),
                          ('X read failed: query-failed (HTTP 403)','x_query_failed:HTTP_403'),
                          ('browser command failed: private title','x_browser_failed'),
                          ('private text and private@email.invalid','x_read_failed')]:
            self.assertEqual(assistant.browser_read_failure('x',text),want)
