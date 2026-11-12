"""A new email from a click on an address (MailApp.compose_from_action, compose_email_action; docs/help/email-composer.md):
the From choices are the owner's mailboxes that can send, the one for the person's area first; Send makes the email a
draft on a to-do of its own, checked like any draft, and only Store.confirm_action queues it. Nothing is sent here:
the outbox never runs, and no transport is called. Made-up data."""
import json
import tempfile
import unittest
from pathlib import Path

import assistant as a

WORK = {'id': 'work', 'email': 'owner@acme.example', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:acme.example'}
HOME = {'id': 'home', 'email': 'owner@mail.example', 'service': 'gmail', 'transport': 'gog', 'boundary': 'personal'}
OUT = {'id': 'out', 'email': 'owner@other.example', 'service': 'outlook', 'transport': 'graph', 'boundary': 'personal'}
SLACK = {'id': 'slack', 'service': 'slack', 'boundary': 'work:acme.example'}


class ComposeEmail(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        with self.store.connect() as db:
            for node, name, email, side, accounts in (('p_sam', 'Sam Lee', 'sam@client.example', 'work', ['work']),
                                                      ('p_dana', 'Dana Roe', 'dana@family.example', 'personal', ['home'])):
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person',?,1,1,?)",
                           (node, name, json.dumps({'emails': [email], 'side': side, 'accounts': accounts})))

    def app(self, accounts=(WORK, HOME, SLACK)):
        app = object.__new__(a.App)
        app.store, app.config = self.store, {'accounts': [dict(x) for x in accounts]}
        return app

    def offer(self, app, to):
        return app.compose_from_action('compose_from', {'to': to}, owner_dashboard=True)

    def jobs(self):
        with self.store.connect() as db:
            return [(r['suggestion_id'], r['status']) for r in db.execute('SELECT * FROM action_jobs')]

    def test_from_starts_on_the_mailbox_of_the_persons_area(self):
        app = self.app()
        work = self.offer(app, 'sam@client.example')
        self.assertEqual((work['default'], work['to_name'], work['node_id']), ('owner@acme.example', 'Sam Lee', 'p_sam'))
        self.assertEqual([(c['account_id'], c['from'], c['area']) for c in work['from']],
                         [('work', 'owner@acme.example', 'Work'), ('home', 'owner@mail.example', 'Personal')])
        home = self.offer(app, 'Dana@Family.example')
        self.assertEqual((home['default'], home['to_name']), ('owner@mail.example', 'Dana Roe'))
        self.assertEqual(home['from'][0]['from'], 'owner@mail.example')
        stranger = self.offer(app, 'new@unknown.example')
        self.assertEqual((stranger['to_name'], stranger['node_id']), ('', None))
        self.assertIn(stranger['default'], {'owner@acme.example', 'owner@mail.example'})

    def test_only_mailboxes_that_may_send(self):
        off = {**HOME, 'actions': False}  # Can do things off
        shared = {**OUT, 'shared': True}  # a Fleet's sign-in only reads
        reads = {**WORK, 'transport': 'imap-read'}  # not a sending mailbox (yet)
        got = self.offer(self.app([reads, off, shared, SLACK]), 'sam@client.example')
        self.assertEqual(got['from'], [])  # the dashboard opens the mail app instead
        self.assertEqual([c['from'] for c in self.offer(self.app([off, OUT]), 'dana@family.example')['from']], ['owner@other.example'])

    def test_an_other_email_mailbox_with_smtp_is_offered_and_sends_the_same_way(self):
        smtp = {'id': 'other', 'email': 'owner@own.example', 'service': 'imap', 'transport': 'imap', 'boundary': 'personal',
                'smtp_host': 'smtp.own.example', 'smtp_port': 465, 'smtp_security': 'ssl'}
        read_only = {**smtp, 'id': 'ro', 'email': 'owner@ro.example', 'smtp_host': ''}  # no SMTP server: it only reads
        refused = {**smtp, 'id': 'no', 'email': 'owner@no.example', 'smtp_refused': True}  # signing in to SMTP failed
        app = self.app([WORK, smtp, read_only, refused])
        got = self.offer(app, 'dana@family.example')
        self.assertEqual([(c['account_id'], c['from'], c['area']) for c in got['from']],
                         [('other', 'owner@own.example', 'Personal'), ('work', 'owner@acme.example', 'Work')])
        made = app.compose_email_action('compose_email', {'to': 'dana@family.example', 'account_id': 'other', 'subject': 'Sunday',
                                                          'body': 'Lunch at noon?'}, owner_dashboard=True)
        with self.store.connect() as db:
            draft = json.loads(db.execute('SELECT next_action FROM suggestions WHERE id=?', (made['suggestion_id'],)).fetchone()[0])
        self.assertEqual((draft['account_id'], draft['from'], draft['to']), ('other', 'owner@own.example', ['dana@family.example']))
        self.assertEqual(self.jobs(), [])
        self.store.confirm_action(made['suggestion_id'], made['revision'], 'tap-1', 'dashboard')
        self.assertEqual(self.jobs(), [(made['suggestion_id'], 'queued')])

    def test_send_makes_a_draft_on_its_own_todo_and_only_confirm_queues_it(self):
        app = self.app()
        made = app.compose_email_action('compose_email', {'to': 'sam@client.example', 'account_id': 'work', 'subject': '  Lunch   next week ',
                                                          'body': 'Hi Sam,\n\n**Thursday** works?\n\nAlex'}, owner_dashboard=True)
        with self.store.connect() as db:
            row = db.execute('SELECT title,status,origin,next_action FROM suggestions WHERE id=?', (made['suggestion_id'],)).fetchone()
            event = db.execute("SELECT analyzed_version,metadata FROM events WHERE kind='owner.card'").fetchone()
        draft = json.loads(row['next_action'])
        self.assertEqual((row['title'], row['status'], row['origin']), ('Email to Sam Lee: Lunch next week', 'prepared', 'owner'))
        self.assertEqual((draft['kind'], draft['account_id'], draft['from'], draft['to'], draft['subject'], draft['revision'], draft['signature']),
                         ('email', 'work', 'owner@acme.example', ['sam@client.example'], 'Lunch next week', made['revision'], True))
        self.assertIn('**Thursday** works?', draft['body'])
        self.assertEqual(event['analyzed_version'], 1)  # no review or run reads it
        self.assertEqual([x['id'] for x in json.loads(event['metadata'])['about']], ['p_sam'])  # on their Graph page
        self.assertEqual(self.jobs(), [])  # nothing queued until the owner's Send is confirmed
        self.store.confirm_action(made['suggestion_id'], made['revision'], 'tap-1', 'dashboard')
        self.assertEqual(self.jobs(), [(made['suggestion_id'], 'queued')])

    def test_refused_without_the_owner_a_mailbox_a_subject_or_a_message(self):
        app = self.app()
        good = {'to': 'sam@client.example', 'account_id': 'work', 'subject': 'Hi', 'body': 'Hello'}
        for args, owner in ((good, False), ({**good, 'account_id': 'slack'}, True), ({**good, 'account_id': 'nope'}, True),
                            ({**good, 'subject': ' '}, True), ({**good, 'body': '\n'}, True), ({**good, 'to': 'not an address'}, True),
                            ({**good, 'to': 'a@b.example, c@d.example'}, True)):
            with self.subTest(args=args, owner=owner), self.assertRaises(ValueError):
                app.compose_email_action('compose_email', args, owner_dashboard=owner)
        with self.assertRaises(ValueError):
            app.compose_from_action('compose_from', {'to': 'sam@client.example'})  # not the dashboard
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM suggestions').fetchone()[0], 0)
        self.assertEqual(self.jobs(), [])

    def test_owner_and_dashboard_only(self):
        for name in ('compose_email', 'compose_from'):
            self.assertIn(name, a.OWNER_ACTIONS)
            self.assertIn(name, a.DASHBOARD_ACTIONS)


if __name__ == '__main__':
    unittest.main()
