"""Teams replies from a to-do (teams_send.py): drafted into the Teams chat the to-do came from, seen, Send, then one post
as the owner. A connection without ChatMessage.Send says it needs a Reconnect and sends nothing; a channel thread is not
a chat reply. No live calls: the connector's Sender is a fake that records what it would post."""
from pathlib import Path
import tempfile
import unittest

import machine.cards as machine_cards
import machine.main as machine_main
from machine.sources.connectors import CONNECTOR_HELPERS
import ms_graph
import next_actions as n
import teams_send
import test_ux as ux

CHAT, CHANNEL = '19:a1b2c3_d4e5@unq.gbl.spaces', '19:general@thread.tacv2'
ACCOUNT = {'id': 'teams', 'service': 'teams', 'email': 'owner@acme.example', 'transport': 'broker', 'boundary': 'work:Acme'}


def event(chat, kind, mid, body):
    return {'account_id': 'teams', 'source_id': 'teams:' + mid, 'kind': 'teams.message', 'occurred_at': '2026-11-05T10:00:00+00:00',
            'title': 'Sam Sender: ' + body, 'body': body, 'deleted': False,
            'metadata': {'chat_id': chat, 'chat_kind': kind, 'chat_name': 'Sam Sender' if kind != 'channel' else 'Acme > General',
                         'message_id': mid, 'from': 'Sam Sender', 'from_email': 'sam@partner.example', 'from_me': False}}


class Teams:
    """The fake connector: its Sender posts nowhere, records each post, and finds what it was told is in the chat."""

    def __init__(self):
        self.posts, self.found, self.fail, self.granted = [], [], None, True
        teams = self

        class Sender:
            def __init__(self, config, account, helpers):
                if account.get('shared'):
                    raise helpers.SourceError('teams_send_shared')

            def ready(self, chat_id):
                if not teams.granted:
                    raise CONNECTOR_HELPERS.SourceError('teams_send_not_granted', 403)
                return {'id': chat_id}

            def post(self, chat_id, text):
                if not teams.granted:
                    raise CONNECTOR_HELPERS.SourceError('teams_not_granted', 403)
                if teams.fail:
                    raise ms_graph.GraphError('graph_http', teams.fail)
                teams.posts.append((chat_id, text))
                return {'id': 'm%d' % len(teams.posts)}

            def find(self, chat_id, text, since):
                return list(teams.found)

        self.Sender = Sender


class Send(unittest.TestCase):
    row = ux.UX.row
    decide = ux.UX.decide

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.teams = Teams()
        self.accounts = [dict(ACCOUNT)]
        self.store.commit_page('teams', {'missing': {'channels': 'admin'}}, [event(CHAT, 'oneOnOne', 'm1', 'Can you send the quote today?'),
                                                                             event(CHANNEL, 'channel', 'c1', 'Who has the deck?')])
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute('SELECT id FROM events')]
        self.sid = self.store.suggest('teams-task', 'Answer Sam', 'Sam asks for the quote in Teams.', ids)['id']

    def app(self):
        app = object.__new__(machine_main.App)
        app.store, app.config = self.store, {'accounts': self.accounts}
        return app

    def save(self, **draft):
        action = {k: v for k, v in {'kind': 'teams', 'label': 'Send', 'account_id': 'teams', 'chat_id': CHAT,
                                    'body': 'Yes, it goes out by noon.', **draft}.items() if v is not None}
        return self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Reply ready.', 'next_action': action})

    def ready(self, **draft):
        self.decide('accept')
        self.save(**draft)
        return self.row()['next_action']

    def confirm(self, key='owner-approval'):
        return self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': self.row()['next_action']['revision'],
                                                    'approval_id': key}, owner_dashboard=True)

    def transport(self):
        return n.ActionTransport(None, None, teams=teams_send.TeamsTransport(self.app().config, self.teams, CONNECTOR_HELPERS))

    def job(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM action_jobs ORDER BY created_at DESC LIMIT 1').fetchone())

    def step(self):
        with self.store.connect() as db:
            db.execute('UPDATE action_jobs SET retry_at=NULL')
        self.app().action_step(self.transport())

    def test_the_draft_goes_to_its_own_chat_and_never_a_channel(self):
        action = self.ready()
        self.assertEqual((action['kind'], action['chat_id'], action['to_name']), ('teams', CHAT, 'Sam Sender'))
        self.assertEqual(n.preview(action), 'Teams message to Sam Sender\n\nYes, it goes out by noon.')
        self.assertEqual(n.label(action), 'Send')
        for bad in ({'chat_id': CHANNEL}, {'chat_id': '19:other@unq.gbl.spaces'}, {'label': 'Post it'}, {'body': ' '},
                    {'body': 'a' * (teams_send.MAX_LENGTH + 1)}, {'to_name': 'Sam'}):
            with self.assertRaises(ValueError, msg=bad):
                self.save(**bad)

    def test_nothing_goes_out_without_the_owners_send_and_then_once(self):
        self.ready()
        self.app().action_step(self.transport())
        self.assertEqual(self.teams.posts, [])
        with self.assertRaises(ValueError):  # the agent can't approve it
            self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': self.row()['next_action']['revision'], 'approval_id': 'x'})
        self.confirm()
        self.confirm(key='second-click')
        self.step()
        self.step()
        self.assertEqual(self.teams.posts, [(CHAT, 'Yes, it goes out by noon.')])
        self.assertEqual((self.job()['status'], self.job()['message_id']), ('sent', f'teams:{CHAT}:m1'))
        self.assertIn('✓ Teams message sent', str(machine_cards.card(self.row())))

    def test_a_connection_from_before_send_asks_to_reconnect(self):
        self.store.commit_page('teams', {'missing': {'replies': 'reconnect'}}, [])
        self.decide('accept')
        with self.assertRaises(ValueError) as caught:  # the planner keeps the text and asks for the Reconnect instead
            self.save()
        self.assertIn('Reconnect Microsoft Teams', str(caught.exception))
        # A draft from before the scope went missing: refused before anything is posted, with the way out
        self.store.commit_page('teams', {'missing': {}}, [])
        self.save()
        self.teams.granted = False
        self.confirm()
        self.step()
        self.assertEqual(self.teams.posts, [])
        self.assertEqual(self.job()['status'], 'blocked')
        self.assertEqual(self.job()['error'], 'Reconnect Microsoft Teams to send replies. Nothing was sent.')

    def test_an_unclear_outcome_is_looked_for_and_never_resent(self):
        self.ready()
        self.confirm()
        self.teams.fail = 502
        self.step()
        self.assertEqual(self.job()['status'], 'uncertain')
        self.teams.fail = None
        self.step()
        self.assertEqual((self.job()['status'], self.teams.posts), ('uncertain', []))  # not found: still never resent
        self.teams.found = ['m9']  # it did go through
        self.step()
        self.assertEqual((self.job()['status'], self.job()['message_id']), ('sent', f'teams:{CHAT}:m9'))
        self.assertEqual(self.teams.posts, [])

    def test_a_refusal_or_throttle_from_teams(self):
        transport = teams_send.TeamsTransport({'accounts': self.accounts}, self.teams, CONNECTOR_HELPERS)
        action, job = {'kind': 'teams', 'account_id': 'teams', 'chat_id': CHAT, 'body': 'Hi'}, {'created_at': '2026-11-05T10:00:00+00:00'}
        self.teams.fail = 403
        self.assertEqual(transport.send(action, job), {'rejected': 403})
        self.teams.fail = 429
        self.assertEqual(transport.send(action, job), {'not_sent': True})
        self.teams.fail = 504
        self.assertEqual(transport.send(action, job), {})
        self.teams.fail, self.teams.found = None, ['a', 'b']
        self.assertEqual(transport.reconcile(action, job), {})  # two alike: unclear, so neither is claimed
        self.accounts[0]['shared'] = {'fleet': 'f1'}
        with self.assertRaises(ValueError):
            transport.preflight(action)
        self.assertEqual(self.teams.posts, [])


if __name__ == '__main__':
    unittest.main()
