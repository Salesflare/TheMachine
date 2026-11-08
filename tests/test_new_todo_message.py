"""New to-do's Message chip: it attaches any message the Machine has (email, Slack, Teams, WhatsApp, Telegram and
the rest), found by its words or its sender, and a to-do made with a Slack message works the whole way: its source
line and link, its evidence for the review and the drafting step, a reply that goes back to Slack in that message's
thread, and the task page's check. No live calls or sends."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('message_attach_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
from machine.app.new_cards import ATTACH_KINDS  # noqa: E402
import task_pages  # noqa: E402

ACCOUNTS = [{'id': 'w', 'service': 'gmail', 'boundary': 'work:Acme'}, {'id': 'sl', 'service': 'slack', 'boundary': 'work:Acme', 'user_id': 'U0OWNER001'},
            {'id': 'tm', 'service': 'teams', 'boundary': 'work:Acme'}, {'id': 'wa', 'service': 'whatsapp', 'boundary': 'personal:me'},
            {'id': 'tg', 'service': 'telegram', 'boundary': 'personal:me'}]
TS = '1793790256.828209'


def event(account, source_id, kind, when, title, body, **meta):
    return {'account_id': account, 'source_id': source_id, 'kind': kind, 'occurred_at': when, 'title': title, 'body': body,
            'metadata': meta, 'deleted': False}


def slack(ts, text, user, when, display=None):
    return event('sl', 'C0DEALS001:' + ts, 'slack.message', when, '#deals: ' + text, text, channel_id='C0DEALS001', channel_name='deals',
                 conversation_type='channel', user_id=user, message_ts=ts, thread_ts=ts,
                 source_url='https://acme.slack.com/archives/C0DEALS001/p' + ts.replace('.', ''), **({'sender_display': display} if display else {}))


class MessageChip(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.owner_user_ids = {'U0OWNER001'}
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS], 'prepare_ahead': False}
        self.store.accounts = self.app.config['accounts']
        self.store.commit_page('w', {}, [
            event('w', 'm1', 'gmail.message', '2026-10-20T09:00:00+00:00', 'Acme contract', 'Here is the contract.', **{'from': 'Sam Lee <sam@client.example>'}),
            event('w', 'cal', 'calendar.event', '2026-10-21T09:00:00+00:00', 'Contract call', 'Go through the contract.')])
        self.store.commit_page('sl', {}, [slack(TS, 'can you check the contract before the call?', 'U0MIRA0001', '2026-10-21T15:00:00+00:00', 'Mira Hart'),
                                          slack('1793790300.000100', 'Lunch at noon?', 'U0MIRA0001', '2026-10-21T16:00:00+00:00', 'Mira Hart')])
        self.store.commit_page('tm', {}, [event('tm', 't1', 'teams.message', '2026-10-19T09:00:00+00:00', 'Legal: the contract redlines',
                                                'The contract redlines are in.', sender_display='Alex Chen', chat_id='19:legal')])
        self.store.commit_page('wa', {}, [event('wa', 'wa1', 'whatsapp.message', '2026-10-18T09:00:00+00:00', 'Robin', 'Contract signed!',
                                                sender_display='Robin', chat_id='3161@s.whatsapp.net', message_id='M1')])
        self.store.commit_page('tg', {}, [event('tg', 'tg1', 'telegram.message', '2026-10-17T09:00:00+00:00', 'Jo', 'Did the contract go out?',
                                                sender_display='Jo', chat_id='42')])
        with self.store.connect() as db:
            self.ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
            # Mira in the Graph, with her Slack messages: her name finds a message without the word in it
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('slack:U0MIRA0001','person','Mira Hart',1,2,'{}')")
            for sid in ('C0DEALS001:' + TS, 'C0DEALS001:1793790300.000100'):
                db.execute("INSERT INTO graph_events(node_id,event_id,at,direct) VALUES('slack:U0MIRA0001',?,'2026-10-21',1)", (self.ids[sid],))
        self.slack_id = self.ids['C0DEALS001:' + TS]

    def row(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())

    def test_the_search_covers_every_kind_of_message(self):
        for kind in ('gmail.message', 'ms_graph.message', 'outlook.message', 'slack.message', 'teams.message', 'whatsapp.message',
                     'telegram.message', 'linkedin.message', 'x.dm', 'intercom.conversation', 'fleet.message', 'fleet.email'):
            self.assertIn(kind, ATTACH_KINDS)
        for kind in ('calendar.event', 'owner.card', 'android.notification'):
            self.assertNotIn(kind, ATTACH_KINDS)
        self.app.action('card_new', {'text': 'Read the contract'}, owner_dashboard=True)  # the owner's own to-do is no message
        found = self.app.message_hits(['all'], 'contract')
        self.assertEqual([r['kind'] for r in found], ['slack.message', 'gmail.message', 'teams.message', 'whatsapp.message', 'telegram.message'])  # newest first
        self.assertEqual(found[0]['metadata']['sender_display'], 'Mira Hart')
        # By sender: Mira's messages, also one without the word, each once
        by_name = self.app.message_hits(['all'], 'mira')
        self.assertEqual([r['body'] for r in by_name], ['Lunch at noon?', 'can you check the contract before the call?'])
        self.assertEqual(self.app.message_hits(['all'], 'nothing here'), [])
        with self.assertRaisesRegex(ValueError, 'explicit configured account_ids'):
            self.app.message_hits(['elsewhere'], 'contract')

    def test_a_to_do_with_a_slack_message_attached_works_end_to_end(self):
        made = self.app.action('card_new', {'text': 'Answer Mira about the contract', 'attach': [self.slack_id]}, owner_dashboard=True)
        card = self.row(made['id'])
        # Its place is the message's: the Slack account of the company, Work
        self.assertEqual(json.loads(card['account_ids']), ['sl'])
        self.assertEqual(json.loads(card['event_ids']), [made['event_id'], self.slack_id])
        self.assertTrue(card['source_line'].startswith('Source: Slack from Mira'), card['source_line'])
        shown = next(s for s in self.store.snapshot([])['suggestions'] if s['id'] == made['id'])
        self.assertEqual(shown['scope'], 'work')
        # Read message opens it, with its link to Slack
        original = next(o for o in self.store.originals(made['id']) if o['event_id'] == self.slack_id)
        self.assertEqual(original['url'], 'https://acme.slack.com/archives/C0DEALS001/p1793790256828209')
        self.assertIn('check the contract', json.dumps(original))
        # The review reads it as the to-do's evidence and fills the to-do in
        filled = self.app.action('suggest', {'dedupe_key': 'sl:contract', 'title': 'Answer Mira about the contract', 'when': 'now',
                                             'body': 'Mira asked in #deals to check the contract before the call.',
                                             'event_ids': [made['event_id'], self.slack_id]})
        self.assertTrue(filled['owner_card'])
        self.assertEqual(json.loads(self.row(made['id'])['event_ids']), [made['event_id'], self.slack_id])
        # The drafting step: a reply goes back to Slack, in the thread of that message, never as an email
        self.store.decide(made['id'], 'accept', '', 'n1', 'dashboard')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running'")
            job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (made['id'],)).fetchone()[0]
        self.app.action('prepare', {'suggestion_id': made['id'], 'job_id': job, 'body': 'Drafted a reply to Mira.', 'outcome': 'needs_you',
                                    'needs': 'check the reply', 'next_action': {'kind': 'slack', 'account_id': 'sl', 'user_id': 'U0MIRA0001',
                                                                                'to_name': 'Mira Hart', 'body': 'Checked it, good to sign.'}})
        with self.store.connect() as db:
            row = self.row(made['id'])
            (action,) = self.store.suggestion_result(row, db)['next_actions']
        self.assertEqual((action['kind'], action['account_id'], action['body']), ('slack', 'sl', 'Checked it, good to sign.'))
        self.assertEqual((action['thread']['channel_id'], action['thread']['ts']), ('C0DEALS001', TS))
        # A channel it can't draft in (Teams) gets no draft of its own; an email from the Slack to-do is refused too
        with self.assertRaises(ValueError):
            self.app.action('prepare', {'suggestion_id': made['id'], 'job_id': job, 'body': 'Drafted it.', 'outcome': 'needs_you', 'needs': 'send it',
                                        'next_action': {'kind': 'teams', 'account_id': 'tm', 'body': 'Checked it.'}})
        # The task page never repeats the attached message
        pages = task_pages.TaskPages(self.app)
        self.assertIn('can you check the contract before the call?', pages.sources(made['id']))

    def test_a_whatsapp_or_telegram_message_puts_the_to_do_in_personal(self):
        for source_id in ('wa1', 'tg1'):
            made = self.app.action('card_new', {'text': 'Reply about the contract', 'attach': [self.ids[source_id]]}, owner_dashboard=True)
            card = self.row(made['id'])
            self.assertEqual(json.loads(card['account_ids']), [source_id[:2]])
            self.assertEqual(json.loads(card['event_ids'])[1], self.ids[source_id])
        with self.assertRaisesRegex(ValueError, 'That message is no longer there'):
            self.app.action('card_new', {'text': 'x', 'attach': [999999]}, owner_dashboard=True)


if __name__ == '__main__':
    unittest.main()
