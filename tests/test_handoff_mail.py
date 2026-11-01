"""Hand off by email to a colleague who isn't on The Machine (handoff_mail.py): only Work to-dos, only what the Team
Graph shares, exactly the parts the owner ticked, the "Take this on in your own Machine" line and its setting, the
promise that closes with the to-do, and the move into their Machine once they joined the Work Fleet through the link.
A fake Network stands in for the control plane; nothing is sent anywhere (no email, Telegram or push)."""
import json
import re
import unittest

import activity_log
import handoff_mail
import task_invites
import task_pages
import test_fleet_requests as tr
from test_fleet import NOW

TAKE = re.compile(r'Take this on in your own Machine: (https://\S+/take/([A-Za-z0-9_-]{22}))$')
RFC = '<hand-1@acme.example>'


class HandoffMail(unittest.TestCase):
    handed_card, card_row = tr.Requests.handed_card, tr.Requests.card_row

    def setUp(self):
        tr.Requests.setUp(self)
        self.app.task_pages = task_pages.TaskPages(self.app)
        self.app.handoff_mail.soon = lambda fn: None  # the test runs each round itself
        self.share = 'team'  # what the Team Graph says of the to-do's messages; None: no Team Graph
        self.fleet.thread_labels = lambda db, rows: {r['id']: {'share': self.share} for r in rows} if self.share else {}
        self.members = {}
        plain = self.relay.call

        def call(method, path, body=None, timeout=40):
            if path != '/task-invite':
                return plain(method, path, body, timeout)
            self.relay.calls.append((method, path, body))
            if body['action'] == 'create':
                return {'id': body['id'], 'url': 'https://cp.example/t/' + body['id'], 'take_url': 'https://cp.example/take/' + body['id'],
                        'expires_at': '2099-01-01T00:00:00+00:00'}
            if body['action'] == 'status':
                return {'stages': {}, 'replies': {}, **({'members': self.members} if self.members else {})}
            return {}
        self.relay.call = call

    def hand(self, card, **extra):
        self.app.action('fleet_handoff_email', {'suggestion_id': card, 'email': 'Kim@Other.example', 'name': 'Kim Lane', 'title': 'Send Sam the pricing',
                                                'summary': 'Sam wants pricing for 40 seats.', **extra}, owner_dashboard=True)
        return json.loads(self.card_row(card)['next_action'])

    def parts(self, card):
        return self.app.action('fleet_handoff_email_parts', {'suggestion_id': card}, owner_dashboard=True)

    def with_draft(self, card):
        """The to-do already holds a reply to Sam, ready to send."""
        import next_actions
        action = next_actions.validate({'kind': 'email', 'label': 'Send reply', 'account_id': 'work', 'to': ['sam@client.example'],
                                        'subject': 'Pricing for 40 seats', 'body': 'Hi Sam,\n\nHere is the pricing.\n\nBest,\nOwner'},
                                       tr.CONFIG, ['work'])
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='accepted' WHERE id=?", (card,))
        self.store.prepare(card, 'A reply to Sam with the pricing.', next_action=action, outcome={'state': 'needs_you', 'needs': 'send'})

    def send(self, card, action):
        """What the outbox does once the owner pressed Send and it went out."""
        self.store.confirm_action(card, action['revision'], 'tap-1', 'dashboard')
        with self.store.connect() as db:
            job = dict(db.execute('SELECT * FROM action_jobs WHERE suggestion_id=?', (card,)).fetchone())
            db.execute("UPDATE action_jobs SET status='sent',rfc_message_id=? WHERE id=?", (RFC, job['id']))
            self.assertTrue(self.app.handoff_mail.sent(db, json.loads(job['payload']), job, {'rfc_message_id': RFC}))

    def synced(self, card):
        """The sent email as the next sync brings it in."""
        sent = tr.mail('work', 0, 'owner@acme.example', 'kim@other.example', message_id=RFC)
        sent['metadata']['labels'] = ['SENT']
        sent['occurred_at'] = NOW.isoformat()
        self.store.commit_page('work', {}, [sent])

    def promise(self, card):
        record = self.app.handoff_mail.load(card)[1]
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM promises WHERE id=?', (record['promise_id'],)).fetchone())

    def view(self, card):
        found = [{'id': card, 'status': self.card_row(card)['status']}]
        with self.store.connect() as db:
            self.app.handoff_mail.annotate(db, found)
        return found[0].get('handoff_mail')

    def test_only_a_work_to_do_goes_by_email(self):
        home = tr.mail('home', 1, 'Mum <mum@family.example>', 'owner@gmail.com')
        self.store.commit_page('home', {}, [home])
        with self.store.connect() as db:
            event = db.execute('SELECT id FROM events WHERE source_id=?', (home['source_id'],)).fetchone()[0]
        card = self.store.suggest('k-home', 'Book the dinner', 'Mum asked.', [event])['id']
        for name, args in (('fleet_handoff_email_parts', {}), ('fleet_handoff_email', {'email': 'kim@other.example'})):
            with self.assertRaisesRegex(ValueError, 'Work to-dos'):
                self.app.action(name, {'suggestion_id': card, **args}, owner_dashboard=True)
        self.assertEqual(self.card_row(card)['next_action'], None)

    def test_context_from_the_to_dos_messages_goes_only_when_the_team_graph_shares_them(self):
        card = self.handed_card()
        self.with_draft(card)
        shared = self.parts(card)
        self.assertTrue(shared['shared'])
        self.assertEqual([x['key'] for x in shared['lines']], ['contact', 'due'])  # prepared: its text is the Machine's outcome
        self.assertEqual(shared['draft']['subject'], 'Pricing for 40 seats')
        for share in ('only_you', None):  # Only you, or no Team Graph at all: the task in the owner's words and the date only
            self.share = share
            found = self.parts(card)
            self.assertEqual((found['shared'], [x['key'] for x in found['lines']], found['draft'], found['links']), (False, ['due'], None, []))
            body = self.hand(card, take=False)['body']
            self.assertNotIn('sam@client.example', body)
            self.assertNotIn('Here is the pricing', body)
            self.assertIn('Sam wants pricing for 40 seats.', body)  # what the owner wrote
            self.with_draft(card)
        # A pending to-do's own text is context too, when shared
        self.share = 'team'
        other = self.handed_card('k-two')
        self.assertEqual([x['key'] for x in self.parts(other)['lines']], ['why', 'contact', 'due'])

    def test_the_email_holds_exactly_what_the_owner_left_ticked(self):
        card = self.handed_card()
        self.with_draft(card)
        action = self.hand(card, keep=['contact', 'evil'], take=False)
        self.assertEqual((action['kind'], action['account_id'], action['to']), ('email', 'work', ['Kim@Other.example']))
        self.assertEqual(action['subject'], 'Could you take this on: Send Sam the pricing')
        body = action['body']
        self.assertIn('Contact: sam@client.example', body)
        for left_out in ('It would be great to have it by', 'Here is the pricing', 'Subject: Pricing for 40 seats', 'http', '<img'):
            self.assertNotIn(left_out, body)  # no tracking pixel, and nothing unticked
        self.assertEqual(self.relay.sent('/task-invite'), [])  # nothing left this Machine: it is a draft for the owner
        self.assertEqual(self.card_row(card)['status'], 'prepared')
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM action_jobs WHERE status!='local_preparation'").fetchone()[0], 0)
        # Everything ticked: the ready draft goes along as it is
        self.with_draft(card)
        body = self.hand(card, take=False)['body']
        self.assertIn('The draft is ready to send:\nTo: sam@client.example\nSubject: Pricing for 40 seats\n\nHi Sam,\n\nHere is the pricing.', body)
        self.assertIn('It would be great to have it by Tuesday, November 3.', body)

    def test_the_take_line_is_on_by_default_and_turns_off_in_settings(self):
        card = self.handed_card()
        self.assertTrue(self.parts(card)['take'])
        body = self.hand(card)['body']
        found = TAKE.search(body)
        self.assertTrue(found, body)
        self.assertTrue(found.group(1).startswith('https://cp.example/take/'))  # this Machine's Network (themachine.computer on the real one)
        self.assertEqual(self.relay.sent('/task-invite'), [])  # registered only once the email went out
        self.assertEqual(self.app.action('fleet_handoff_take_line', {'on': False}, owner_dashboard=True), {'take_line': False})
        self.assertFalse(self.parts(card)['take'])
        self.assertNotIn('Take this on', self.hand(card)['body'])
        self.assertIn('Take this on', self.hand(card, take=True)['body'])  # the owner's tick in the sheet wins
        self.assertEqual(handoff_mail.take_link({'fleet': {'url': 'https://network.themachine.computer/api/fleet'}}, 'x' * 22),
                         'https://themachine.computer/take/' + 'x' * 22)

    def test_after_the_send_it_is_a_promise_that_closes_with_the_to_do(self):
        card = self.handed_card()
        action = self.hand(card)
        take_id = TAKE.search(action['body']).group(2)
        self.send(card, action)
        row = self.card_row(card)
        self.assertEqual(row['status'], 'snoozed')  # waits under Later, back to check in if nothing comes
        self.assertEqual(self.view(card), {'name': 'Kim Lane', 'state': 'waiting', 'promise': 'open'})
        # The take link goes to the Network now: the Work Fleet and a hash of the address, never the address
        self.app.handoff_mail.round()
        made = self.relay.sent('/task-invite')[0]
        self.assertEqual((made['id'], made['join']), (take_id, {'fleet': self.ref, 'to': task_invites.hashed_email('kim@other.example')}))
        self.assertNotIn('kim', json.dumps(made).lower())
        self.assertNotIn('pricing', json.dumps(made).lower())
        self.app.handoff_mail.round()
        self.assertEqual(len([b for b in self.relay.sent('/task-invite') if b['action'] == 'create']), 1)  # once
        # The sent email synced: the promise "Kim takes this on", on this to-do
        self.synced(card)
        self.app.handoff_mail.round()
        promise = self.promise(card)
        self.assertEqual((promise['direction'], promise['who'], promise['status'], promise['watch']),
                         ('theirs', 'Kim Lane', 'open', None))  # only the review closes it, by what their reply means
        self.assertIn(promise['event_id'], json.loads(self.card_row(card)['event_ids']))
        self.assertIn('Kim Lane → you: take this on: Send Sam the pricing', self.store.promises_text())
        # Their reply says it's done: the review keeps the promise, and the to-do closes
        self.store.update_promise({'id': promise['id'], 'status': 'kept', 'reason': 'Kim wrote that the pricing went out'})
        self.app.handoff_mail.round()
        self.assertEqual(self.card_row(card)['status'], 'completed')
        self.assertEqual(self.view(card), {'name': 'Kim Lane', 'state': 'done', 'promise': 'kept'})
        with self.store.connect() as db:
            lines = [x for x in activity_log.page(db, kind='fleet')['items'] if x['id'] == 'fleet:handoff-mail:' + card]
        self.assertEqual([(x['what'], x['status'], x['todo']['id']) for x in lines], [('To Kim Lane: Send Sam the pricing', 'Done', card)])

    def test_marking_the_to_do_done_keeps_the_promise(self):
        card = self.handed_card()
        self.send(card, self.hand(card, take=False))
        self.synced(card)
        self.app.handoff_mail.round()
        self.assertEqual(self.relay.sent('/task-invite'), [])  # no take line, no link to register
        self.store.decide(card, 'complete', '', 'done-1', 'dashboard')
        self.app.handoff_mail.round()
        self.assertEqual(self.promise(card)['status'], 'kept')

    def test_once_they_join_the_work_fleet_through_the_link_the_to_do_moves_to_their_machine(self):
        card = self.handed_card()
        action = self.hand(card)
        take_id = TAKE.search(action['body']).group(2)
        self.send(card, action)
        self.synced(card)
        self.app.handoff_mail.round()
        self.members = {take_id: {'fleet': 'another-fleet', 'member_id': 'pat1'}}
        self.app.handoff_mail.round()
        self.assertEqual(self.relay.sent('/ask'), [])  # only into the Fleet the link was for
        self.members = {take_id: {'fleet': self.ref, 'member_id': 'pat1'}}
        self.app.handoff_mail.round()
        ask = self.relay.sent('/ask')[-1]
        self.assertEqual((ask['kind'], ask['to'], ask['question']['title']), ('handoff', ['pat1'], 'Send Sam the pricing'))
        self.assertNotIn('sources', ask['question'])
        self.assertEqual(self.app.handoff_mail.load(card)[0], 'moved')
        self.assertEqual(self.promise(card)['status'], 'dropped')
        self.app.handoff_mail.round()
        self.assertEqual(len(self.relay.sent('/ask')), 1)


if __name__ == '__main__':
    unittest.main()
