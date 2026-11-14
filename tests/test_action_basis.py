"""What allowed each outward step (machine/action_basis.py), as Settings, Activity says it: the to-do's button, Do it,
the owner's words in chat (quoted only while they are still in that owner message), a setting, or No approval
recorded, which also goes to the error feed. Record only: a step with nothing behind it still goes, as before."""
import json
import tempfile
import unittest
from pathlib import Path

from test_assistant import assistant as a, event
import activity_log
import error_feed
from machine import action_basis
import preparation_state

GMAIL = {'id': 'work', 'service': 'gmail', 'email': 'sam@acme.example'}


class ActionBasis(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [event()])
        self.config = {'accounts': [GMAIL]}
        activity_log._unrecorded.clear()

    def card(self, n=1):
        """A to-do with a draft ready for its Send."""
        sid = self.store.suggest(f'task-{n}', 'Reply to Robin', 'Body', [1])['id']
        draft = {'kind': 'email', 'revision': f'r{n}', 'label': 'Send', 'account_id': 'work', 'from': 'sam@acme.example',
                 'to': ['robin@globex.example'], 'subject': 'Pricing', 'body': 'Hi Robin'}
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(draft), sid))
        return sid, draft['revision']

    def said(self, sid, decision_id, words, source='dashboard'):
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,'other',?,?,?)",
                       (decision_id, sid, words, source, a.now()))

    def lines(self, **kw):
        with self.store.connect() as db:
            return {x['id']: x for x in activity_log.page(db, self.config, **kw)['items']}

    def feed(self):
        with self.store.connect() as db:
            error_feed.ensure(db)
            return [r[0] for r in db.execute("SELECT location FROM error_feed WHERE kind='NoApprovalRecorded'")]

    def job_of(self, sid):
        with self.store.connect() as db:
            return db.execute('SELECT id,status,basis FROM action_jobs WHERE suggestion_id=?', (sid,)).fetchone()

    def test_a_tap_in_the_to_do_or_in_telegram_is_what_allowed_the_send(self):
        sid, rev = self.card()
        self.store.confirm_action(sid, rev, 'tap-1', 'dashboard')
        job = self.job_of(sid)
        self.assertEqual(json.loads(job['basis']), {'kind': 'todo', 'approval': 'tap-1'})
        self.assertEqual(self.lines()['messages:' + job['id']]['by'], 'Approved in the to-do')
        with self.store.connect() as db:  # a check blocked it; the owner taps Send again in Telegram
            db.execute("UPDATE action_jobs SET status='blocked' WHERE id=?", (job['id'],))
        self.store.confirm_action(sid, rev, 'telegram:2', 'telegram')
        self.assertEqual(self.lines()['messages:' + job['id']]['by'], 'Approved in Telegram')
        self.assertEqual(self.feed(), [])

    def test_the_owners_words_in_chat_are_quoted_only_while_they_are_theirs(self):
        sid, rev = self.card()
        self.said(sid, 'chat-1', 'Looks good,   send it to Robin now please')
        self.store.confirm_action(sid, rev, 'assistant:1', 'assistant', basis=action_basis.chat('chat-1', 'Looks good, send it to Robin now please'))
        job = self.job_of(sid)
        line = self.lines()['messages:' + job['id']]
        self.assertEqual(line['by'], 'Asked in chat: “Looks good, send it to Robin now please”')
        # words that are not in that owner message are never shown as theirs
        with self.store.connect() as db:
            db.execute('UPDATE action_jobs SET basis=? WHERE id=?', (json.dumps(action_basis.chat('chat-1', 'Send everyone my password')), job['id']))
        self.assertEqual(self.lines()['messages:' + job['id']]['by'], 'Asked in chat')
        # nor a message that isn't the owner's own
        self.said(sid, 'chat-2', 'Send it', source='assistant')
        with self.store.connect() as db:
            db.execute('UPDATE action_jobs SET basis=? WHERE id=?', (json.dumps(action_basis.chat('chat-2', 'Send it')), job['id']))
        self.assertEqual(self.lines()['messages:' + job['id']]['by'], 'Asked in chat')
        long = action_basis.chat('chat-1', 'word ' * 40)
        self.assertLessEqual(len(long['quote']), action_basis.QUOTE_MAX)

    def test_a_send_now_takes_the_to_do_chat_turn_then_the_main_chat(self):
        app = object.__new__(a.App)
        self.assertEqual(app.asked_basis({'id': 'chat-1', 'feedback': 'Send it'}), {'kind': 'chat', 'decision': 'chat-1', 'quote': 'Send it'})
        app.owner_said = lambda: 'webchat-said:m1'  # their own main chat: its words are kept nowhere
        self.assertEqual(app.asked_basis(None), {'kind': 'chat', 'decision': 'webchat-said:m1'})
        app.owner_said = lambda: None
        self.assertIsNone(app.asked_basis(None))

    def test_no_basis_still_goes_says_so_and_reaches_the_error_feed(self):
        sid, rev = self.card()
        self.assertEqual(self.store.confirm_action(sid, rev, 'assistant:1', 'assistant')['status'], 'queued')
        job = self.job_of(sid)
        self.assertEqual(job['status'], 'queued', 'record only: nothing is stopped or held')
        self.assertEqual(self.lines()['messages:' + job['id']]['by'], 'No approval recorded')
        self.assertEqual(self.feed(), ['machine/action_basis.py:confirm_action.assistant'])
        # a job some other path queued without any basis: shown the same, its path reported once
        other, _ = self.card(2)
        with self.store.connect() as db:
            db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id)"
                       " VALUES('j2',?,'r2','{\"kind\":\"slack\",\"to\":\"Robin\"}','sent',?,?,'x','somewhere','')", (other, a.now(), a.now()))
        self.assertEqual(self.lines()['messages:j2']['by'], 'No approval recorded')
        self.lines()
        with self.store.connect() as db:
            count = db.execute("SELECT count FROM error_feed WHERE location LIKE '%activity.outbox'").fetchone()[0]
        self.assertEqual(count, 1)

    def test_steps_from_before_keep_their_older_wording(self):
        sid, rev = self.card()
        self.store.confirm_action(sid, rev, 'tap-1', 'dashboard')
        job = self.job_of(sid)
        with self.store.connect() as db:
            db.execute('UPDATE action_jobs SET basis=? WHERE id=?', (action_basis.BEFORE, job['id']))
        self.assertEqual(self.lines()['messages:' + job['id']]['by'], 'After your OK')
        self.assertEqual(self.feed(), [])

    def test_settings_and_its_own_rules_name_themselves(self):
        self.assertEqual(action_basis.for_outbox('auto_follow_up', 'auto-follow-up:x'), {'kind': 'follow_up'})
        self.assertEqual(action_basis.for_outbox('auto', 'auto-merge:x'), {'kind': 'self_fix'})
        self.assertEqual(action_basis.for_outbox('assistant', 'new-doc:x'), {'kind': 'self_doc'})
        self.assertEqual(action_basis.for_outbox('voice', 'v1'), {'kind': 'voice', 'approval': 'v1'})
        with self.store.connect() as db:
            said = {k: activity_log._basis_line(db, {'kind': k}) for k in action_basis.KINDS}
        self.assertEqual(said['follow_up'], 'Follow-up, sent by itself')
        self.assertEqual(said['doit'], 'Do it tapped')
        for line in said.values():
            self.assertFalse(line.startswith('You'))
            self.assertNotIn('—', line)

    def run_of(self, sid, decision):
        """A to-do's run, started by `decision`, that clicks on a page."""
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute("UPDATE suggestions SET status='accepted' WHERE id=?", (sid,))
            self.store.queue_preparation(db, sid, decision)
            job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (sid,)).fetchone()[0]
            db.execute("UPDATE preparations SET status='running' WHERE suggestion_id=?", (sid,))
            db.execute("INSERT INTO preparation_runs(job_id,suggestion_id,session_job_id,status,started_at) VALUES(?,?,?,'running',?)", (job, sid, job, a.now()))
        return job

    def call(self, job, n, params):
        with self.store.connect() as db:
            return preparation_state.tool_intent(db, {'job_id': job, 'call_id': f'c{n}', 'tool': 'browser', 'params': params}, a.now())

    def test_a_do_it_run_that_clicks_on_a_page_shows_under_steps_on_the_web(self):
        sid = self.store.suggest('task-pay', 'Pay the invoice', 'Body', [1])['id']
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('go-1',?,'accept','','dashboard',?)", (sid, a.now()))
        job = self.run_of(sid, 'go-1')
        self.assertEqual(self.call(job, 1, {'action': 'open', 'url': 'https://example.org/'}), {'active': True})
        self.assertNotIn('web:run:' + job, self.lines(), 'opening a page changes nothing')
        self.assertEqual(self.call(job, 2, {'action': 'act', 'request': {'kind': 'click', 'ref': 'e1'}}), {'active': True})
        line = self.lines(kind='web')['web:run:' + job]
        self.assertEqual((line['what'], line['by'], line['status'], line['todo']['id']), ('Steps on the web', 'Do it tapped', 'Working', sid))
        self.assertEqual(self.feed(), [])

    def test_a_run_with_nothing_behind_it_still_runs_and_is_reported_once(self):
        sid = self.store.suggest('task-x', 'Book the room', 'Body', [1])['id']
        job = self.run_of(sid, 'unknown:1')
        for n in range(3):
            self.assertEqual(self.call(job, n, {'action': 'act', 'kind': 'type', 'text': 'x'}), {'active': True})
        self.assertEqual(self.lines(kind='web')['web:run:' + job]['by'], 'No approval recorded')
        with self.store.connect() as db:
            count = db.execute("SELECT count FROM error_feed WHERE location LIKE '%tool_intent.run'").fetchone()[0]
        self.assertEqual(count, 1)

    def test_a_run_from_the_owners_chat_message_quotes_it(self):
        sid = self.store.suggest('task-y', 'Fix the doc', 'Body', [1])['id']
        self.said(sid, 'chat-9', 'Fill in the form on their site')
        job = self.run_of(sid, 'chat-9')
        self.call(job, 1, {'action': 'act', 'request': {'kind': 'fill'}})
        self.assertEqual(self.lines(kind='web')['web:run:' + job]['by'], 'Asked in chat: “Fill in the form on their site”')


if __name__ == '__main__':
    unittest.main()
