import test_ux as ux
a=ux.a
from unittest.mock import patch
import unittest,json,sqlite3,subprocess

class FeedbackPrompts(unittest.TestCase):
    setUp=ux.UX.setUp
    row=ux.UX.row
    job=ux.UX.job
    decide=ux.UX.decide
    # Use setup helpers without inheriting the unrelated UX tests.
    def app(self):
        app=object.__new__(a.App);app.store=self.store
        app.config={'telegram_owner':'1000001','accounts':[], 'prompt_receipts':str(self.root/'receipts'),'openclaw_state':str(self.root/'native.sqlite')}
        return app
    def request(self,app,request_id='cb1'):
        return app.action('request_feedback',{'suggestion_id':self.sid,'request_id':request_id,'card_message_id':'40','managed_prompt':True})
    def prompt(self):
        with self.store.connect() as db:return dict(db.execute('SELECT * FROM feedback_prompts').fetchone())
    def later(self):
        return patch.object(a,'now',return_value=(a.dt.datetime.fromisoformat(a.now())+a.dt.timedelta(seconds=90)).isoformat())
    def test_repeated_click_and_callback_replay_have_one_admission(self):
        app=self.app();self.request(app);self.request(app);self.request(app,'second-click')
        calls=[]
        app.feedback_prompt_step(sender=lambda row:(calls.append(row),{'messageId':'41'})[1])
        app.feedback_prompt_step(sender=lambda row:(calls.append(row),{'messageId':'42'})[1])
        self.assertEqual(len(calls),1);self.assertEqual(self.prompt()['message_id'],'41')
    def test_unknown_native_outcome_is_held_without_fallback(self):
        app=self.app();self.request(app)
        with patch.object(a,'telegram_request') as plain:
            self.assertEqual(app.feedback_prompt_step(sender=lambda row:{}),'uncertain')
            self.request(app)
            with self.later():app.feedback_prompt_step(sender=lambda row:self.fail('Repeated native send'))
            plain.assert_not_called()
        self.assertEqual(self.prompt()['status'],'uncertain')
    def test_confirmed_receipt_survives_failed_binding_and_service_restart(self):
        app=self.app();self.request(app)
        with patch.object(self.store,'bind_feedback_prompt',side_effect=sqlite3.OperationalError('Synthetic binding failure')):
            with self.assertRaises(sqlite3.OperationalError):app.feedback_prompt_step(sender=lambda row:{'messageId':'41'})
        self.assertEqual(self.prompt()['status'],'native_sending')
        restarted=self.app();restarted.feedback_prompt_step(sender=lambda row:self.fail('Repeated send after binding failure'))
        self.assertEqual(self.prompt()['status'],'sent');self.assertEqual(self.row()['feedback_prompt_message_id'],'41')
    def test_plain_unknown_response_never_resends(self):
        app=self.app();self.request(app);app.feedback_prompt_step(sender=lambda row:{'definitely_not_sent':True})
        with self.later(),patch.object(a,'telegram_request',side_effect=subprocess.TimeoutExpired('Synthetic response lost',60)) as send:
            app.feedback_prompt_step();self.request(app);app.feedback_prompt_step()
            self.assertEqual(send.call_count,1)
        with self.later():app.feedback_prompt_step(sender=lambda row:self.fail('Resend'))
        self.assertEqual(self.prompt()['status'],'uncertain')
    def test_second_tap_reports_an_unconfirmed_earlier_prompt(self):
        app=self.app()
        self.assertNotIn('earlier_prompt',self.request(app))
        app.feedback_prompt_step(sender=lambda row:{})
        self.assertEqual(self.request(app,'second-tap')['earlier_prompt'],'uncertain')
    def test_runner_that_cannot_start_is_reported_as_not_sent(self):
        # Invalid input fails before any send, like a missing OpenClaw module after an update.
        app=self.app();app.config['openclaw']='/nonexistent/openclaw/bin/openclaw'
        reply=app.native_change_prompt({'request_id':'cb1','card_id':'not-a-card','title':'Synthetic'})
        self.assertIs(reply['definitely_not_sent'],True)
    def test_legacy_unconfirmed_fallback_never_sends(self):
        app=self.app();args={'suggestion_id':self.sid,'request_id':'old','card_message_id':'40'}
        app.action('request_feedback',{**args,'defer_prompt':True})
        with patch.object(a,'telegram_request') as send:
            app.action('request_feedback',{**args,'fallback_prompt':True});app.feedback_prompt_step()
            send.assert_not_called()
        self.assertEqual(self.prompt()['status'],'uncertain')
    def test_exact_cached_prompt_recovers_but_wrong_chat_does_not(self):
        app=self.app();self.request(app)
        # Telegram cannot deliver before send admission; cross a second deterministically.
        attempted=(a.dt.datetime.fromisoformat(self.prompt()['created_at'])+a.dt.timedelta(seconds=2)).isoformat()
        with patch.object(a,'now',return_value=attempted):app.feedback_prompt_step(sender=lambda row:{})
        base={'message_id':41,'date':int(a.dt.datetime.fromisoformat(self.prompt()['attempted_at']).timestamp()),'from':{'is_bot':True},'chat':{'id':1000001},'reply_to_message':{'message_id':40},'text':a.prompt_text('Prepare a draft')}
        with sqlite3.connect(app.config['openclaw_state']) as db:
            db.execute('CREATE TABLE plugin_state_entries(plugin_id,namespace,value_json)')
            db.execute('INSERT INTO plugin_state_entries VALUES(?,?,?)',('telegram','telegram.message-cache',json.dumps({"sourceMessage":{**base,'chat':{'id':123}}})))
        self.assertIsNone(app.recovered_prompt_receipt(self.prompt()))
        with sqlite3.connect(app.config['openclaw_state']) as db:
            db.execute('DELETE FROM plugin_state_entries');db.execute('INSERT INTO plugin_state_entries VALUES(?,?,?)',('telegram','telegram.message-cache',json.dumps({"sourceMessage":base})))
        with self.later():app.feedback_prompt_step()
        self.assertEqual(self.row()['feedback_prompt_message_id'],'41')
    def test_multiple_cached_candidates_and_wrong_card_are_held(self):
        app=self.app();self.request(app);app.feedback_prompt_step(sender=lambda row:{})
        base={'date':int(a.dt.datetime.fromisoformat(self.prompt()['attempted_at']).timestamp()),'from':{'is_bot':True},'chat':{'id':1000001},'reply_to_message':{'message_id':40},'text':a.prompt_text('Prepare a draft')}
        with sqlite3.connect(app.config['openclaw_state']) as db:
            db.execute('CREATE TABLE plugin_state_entries(plugin_id,namespace,value_json)')
            for mid in (41,42):db.execute('INSERT INTO plugin_state_entries VALUES(?,?,?)',('telegram','telegram.message-cache',json.dumps({'sourceMessage':{**base,'message_id':mid}})))
        self.assertIsNone(app.recovered_prompt_receipt(self.prompt()))
        with sqlite3.connect(app.config['openclaw_state']) as db:
            db.execute('DELETE FROM plugin_state_entries');db.execute('INSERT INTO plugin_state_entries VALUES(?,?,?)',('telegram','telegram.message-cache',json.dumps({'sourceMessage':{**base,'message_id':41,'reply_to_message':{'message_id':39}}})))
        self.assertIsNone(app.recovered_prompt_receipt(self.prompt()))
    def test_owner_cancellation_during_send_keeps_receipt_without_reopening(self):
        app=self.app();self.request(app)
        def sender(row):self.decide('reject');return {'messageId':'41'}
        app.feedback_prompt_step(sender=sender)
        self.assertEqual(self.row()['status'],'rejected');self.assertIsNone(self.row()['feedback_until'])
        self.assertIsNone(self.row()['feedback_prompt_message_id']);self.assertEqual(self.prompt()['message_id'],'41')
    def test_cancelled_owner_request_is_never_sent(self):
        app=self.app();self.request(app);self.decide('reject')
        app.feedback_prompt_step(sender=lambda row:self.fail('Send after cancellation'))
        self.assertEqual(self.prompt()['status'],'cancelled')
    def test_queued_intent_is_committed_with_request_and_restart_catches_up(self):
        app=self.app();self.request(app);self.assertEqual(self.prompt()['status'],'queued')
        self.app().feedback_prompt_step(sender=lambda row:{'messageId':'41'})
        self.assertEqual(self.row()['feedback_prompt_message_id'],'41')

if __name__=='__main__':unittest.main()
