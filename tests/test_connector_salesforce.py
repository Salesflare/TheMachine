"""Salesforce fixture tests: a made-up org behind a faked HTTP layer, nothing reaches Salesforce or a broker. Reads are
GETs on the allowlist; the one write is a PATCH of a Contact's title, phone or LinkedIn field, only with Update contact
details on, and only what crm_sync.py plans."""
import json
from pathlib import Path
import tempfile
import types
import unittest
import urllib.error
import urllib.parse
from unittest.mock import patch

from test_connectors import a, Response
from connectors import salesforce
import crm
import crm_sync
import enrichment
import mail_grants

NOW = '2026-11-09T12:00:00+00:00'
ACCOUNT = {**salesforce.SETUP['account'], 'email': 'owner@acme.example'}
INSTANCE = 'https://acme-dev-ed.my.salesforce.com'
USER = '005000000000001AAA'
ANN = '003000000000001AAA'
BOB = '003000000000002AAA'


def acct(name='Globex', site='https://www.globex.example'):
    return {'Name': name, 'Website': site}


class FakeOrg:
    """What a made-up org answers, by SOQL object."""
    def __init__(self):
        self.opportunities = [
            {'Id': '006000000000001AAA', 'Name': 'Globex rollout', 'StageName': 'Proposal', 'Amount': 12000, 'CloseDate': '2026-12-15',
             'IsClosed': False, 'IsWon': False, 'Description': 'Wants SSO first.', 'LastModifiedDate': '2026-11-09T10:00:00.000+0000',
             'SystemModstamp': '2026-11-09T10:00:00.000+0000', 'CreatedDate': '2026-11-08T09:00:00.000+0000',
             'AccountId': '001000000000001AAA', 'Account': acct(), 'Owner': {'Name': 'Owner', 'Email': 'owner@acme.example'},
             'OpportunityContactRoles': {'records': [{'Role': 'Decision Maker', 'Contact': {'Id': ANN, 'Name': 'Ann Example',
                                                                                             'Email': 'ann@globex.example', 'Title': 'CTO'}}]}},
            {'Id': '006000000000002AAA', 'Name': 'Old deal', 'StageName': 'Negotiation', 'Amount': 5000, 'CloseDate': '2026-11-30',
             'IsClosed': False, 'IsWon': False, 'LastModifiedDate': '2026-11-09T09:00:00.000+0000',
             'SystemModstamp': '2026-11-09T09:00:00.000+0000', 'CreatedDate': '2026-01-01T09:00:00.000+0000',
             'AccountId': '001000000000002AAA', 'Account': acct('Initech', 'initech.example'), 'Owner': {'Name': 'Rep'}}]
        self.tasks = [
            {'Id': '00T000000000001AAA', 'Subject': 'Send the security questionnaire', 'Status': 'Not Started', 'ActivityDate': '2026-11-12',
             'IsClosed': False, 'OwnerId': USER, 'Owner': {'Name': 'Owner'}, 'Who': {'Type': 'Contact', 'Name': 'Ann Example', 'Email': 'ann@globex.example'},
             'WhatId': '006000000000001AAA', 'What': {'Name': 'Globex rollout'}, 'AccountId': '001000000000001AAA', 'Account': acct(),
             'LastModifiedDate': '2026-11-09T08:00:00.000+0000', 'SystemModstamp': '2026-11-09T08:00:00.000+0000'},
            {'Id': '00T000000000002AAA', 'Subject': 'Call', 'Description': 'Budget approved for Q1.', 'Status': 'Completed', 'IsClosed': True,
             'TaskSubtype': 'Call', 'CompletedDateTime': '2026-11-09T07:00:00.000+0000', 'OwnerId': '005000000000009AAA',
             'Owner': {'Name': 'Rep'}, 'Who': {'Type': 'Contact', 'Name': 'Bob Example', 'Email': 'bob@initech.example'},
             'LastModifiedDate': '2026-11-09T07:00:00.000+0000', 'SystemModstamp': '2026-11-09T07:00:00.000+0000'},
            {'Id': '00T000000000003AAA', 'Subject': 'Email: Re: pricing', 'Description': 'Owner mail', 'Status': 'Completed', 'IsClosed': True,
             'TaskSubtype': 'Email', 'OwnerId': USER, 'LastModifiedDate': '2026-11-09T06:00:00.000+0000',
             'SystemModstamp': '2026-11-09T06:00:00.000+0000'},
            {'Id': '00T000000000004AAA', 'Subject': 'Follow up', 'Status': 'Completed', 'IsClosed': True, 'OwnerId': '005000000000009AAA',
             'LastModifiedDate': '2026-11-09T06:00:00.000+0000', 'SystemModstamp': '2026-11-09T06:00:00.000+0000'}]
        self.meetings = [
            {'Id': '00U000000000001AAA', 'Subject': 'Demo', 'Description': 'They liked the reports.', 'StartDateTime': '2026-11-08T14:00:00.000+0000',
             'OwnerId': USER, 'Owner': {'Email': 'owner@acme.example'}, 'Who': {'Type': 'Contact', 'Name': 'Ann Example', 'Email': 'ann@globex.example'},
             'AccountId': '001000000000001AAA', 'Account': acct(), 'SystemModstamp': '2026-11-08T15:00:00.000+0000'},
            {'Id': '00U000000000002AAA', 'Subject': 'No notes', 'StartDateTime': '2026-11-08T16:00:00.000+0000', 'OwnerId': USER,
             'SystemModstamp': '2026-11-08T16:00:00.000+0000'}]
        self.contacts = [
            {'Id': ANN, 'Name': 'Ann Example', 'Email': 'ann@globex.example', 'Title': 'VP Engineering', 'Phone': '+32 470 00 00 01',
             'LastModifiedDate': '2026-10-01T09:00:00.000+0000', 'LinkedIn__c': None},
            {'Id': BOB, 'Name': 'Bob Example', 'Email': 'bob@initech.example', 'Title': 'Buyer', 'Phone': None,
             'LastModifiedDate': '2026-11-09T11:00:00.000+0000', 'LinkedIn__c': None}]
        self.linkedin_field = True


class OrgCase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite')
        self.config = {'database': str(Path(tmp.name) / 'events.sqlite'), 'salesforce_broker': {'url': 'https://cp.example/api/salesforce/token'}}
        mail_grants.put(self.config, 'salesforce', 'owner@acme.example', 'refresh-1')
        salesforce._tokens.clear()
        self.offered = []
        self.helpers = types.SimpleNamespace(SourceError=a.SourceError, Skips=a.CONNECTOR_HELPERS.Skips, now=lambda: NOW, iso=a.CONNECTOR_HELPERS.iso,
                                             credential=lambda config, name: 'app-token' if name == 'salesforce-broker' else 1 / 0,
                                             remember_profiles=lambda store, source, offers: self.offered.extend(offers) or a.remember_profiles(store, source, offers))
        self.org, self.instance = FakeOrg(), INSTANCE
        self.reads, self.writes, self.broker_calls, self.patch_status = [], [], [], 204
        patch('urllib.request.urlopen', side_effect=self.respond).start()
        self.addCleanup(patch.stopall)

    def respond(self, request, timeout):
        url = urllib.parse.urlsplit(request.full_url)
        if url.netloc == 'cp.example':
            self.assertEqual(request.get_method(), 'POST')
            self.assertEqual(request.get_header('Authorization'), 'Bearer app-token')
            self.broker_calls.append(json.loads(request.data))
            return Response(json.dumps({'access_token': 'access-1', 'instance_url': self.instance}).encode())
        self.assertEqual(url.scheme + '://' + url.netloc, INSTANCE)
        self.assertNotIn('refresh', request.full_url)
        self.assertEqual(request.get_header('Authorization'), 'Bearer access-1')
        if request.get_method() == 'PATCH':
            self.writes.append((url.path, json.loads(request.data)))
            if self.patch_status != 204:
                raise urllib.error.HTTPError(request.full_url, self.patch_status, 'no', {}, None)
            return Response(b'')
        self.assertEqual(request.get_method(), 'GET')
        self.reads.append(url.path)
        if url.path == '/services/oauth2/userinfo':
            return Response(json.dumps({'user_id': USER, 'organization_id': '00D000000000001AAA', 'email': 'owner@acme.example'}).encode())
        if url.path == '/services/data/v62.0/sobjects/Contact/describe':
            fields = [{'name': 'Title', 'label': 'Title', 'type': 'string', 'updateable': True, 'custom': False}]
            if self.org.linkedin_field:
                fields.append({'name': 'LinkedIn__c', 'label': 'LinkedIn profile', 'type': 'url', 'updateable': True, 'custom': True})
            return Response(json.dumps({'fields': fields}).encode())
        if url.path == '/services/data/v62.0/query':
            soql = urllib.parse.parse_qs(url.query)['q'][0]
            if ' FROM Opportunity ' in soql:
                rows = self.org.opportunities
            elif ' FROM Task ' in soql:
                rows = self.org.tasks
            elif ' FROM Event ' in soql:
                rows = self.org.meetings
            elif ' FROM Contact ' in soql:
                rows = [c for c in self.org.contacts if f"'{c['Email']}'" in soql]
            else:
                raise AssertionError('unexpected query ' + soql)
            return Response(json.dumps({'done': True, 'totalSize': len(rows), 'records': rows}).encode())
        raise AssertionError('unexpected request ' + request.full_url)

    def sync(self, account=ACCOUNT):
        return salesforce.sync(self.store, self.config, account, self.helpers)

    def rows(self):
        with self.store.connect() as db:
            return {r['source_id']: dict(r, metadata=json.loads(r['metadata'])) for r in db.execute('SELECT * FROM events')}

    def person(self, email, node='email:ann@globex.example', facts=(), edits=None):
        with self.store.connect() as db:
            db.execute('INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,?,?,?,?,?,?)',
                       (node, 'person', 'Ann Example', 1.0, '2026-11-09', 3, json.dumps({'identifiers': [node, 'li:ann-1']})))
            enrichment.fact_tables(db)
            for identifier, field, value, rank, source, seen in facts:
                db.execute('INSERT INTO person_facts VALUES(?,?,?,?,?,?)', (identifier, field, value, rank, source, seen))
            if edits:
                db.execute('INSERT INTO person_edits(identifier,fields,updated_at) VALUES(?,?,?)', (node, json.dumps(edits), '2026-11-05T10:00:00+00:00'))


class SalesforceTests(OrgCase):
    def test_brings_in_deals_tasks_and_activity_as_signals(self):
        result = self.sync()
        rows = self.rows()
        # New deal (made in the window), the owner's open task, a colleague's call with notes, a meeting with notes. Not:
        # a deal first seen that isn't new, the owner's own logged email, a task done without notes, a meeting without notes.
        self.assertEqual(set(rows), {'opportunity:006000000000001AAA:Proposal:12000', 'task:00T000000000001AAA',
                                     'task:00T000000000002AAA', 'event:00U000000000001AAA'})
        deal = rows['opportunity:006000000000001AAA:Proposal:12000']
        self.assertEqual(deal['title'], 'New deal: Globex rollout')
        self.assertEqual(deal['metadata']['crm_account'], {'id': '001000000000001AAA', 'name': 'Globex', 'domain': 'globex.example'})
        self.assertEqual(deal['metadata']['contacts'][0]['email'], 'ann@globex.example')
        self.assertEqual(deal['metadata']['source_url'], INSTANCE + '/lightning/r/006000000000001AAA/view')
        self.assertIn('Amount: 12,000', deal['body'])
        self.assertEqual(rows['task:00T000000000001AAA']['kind'], 'salesforce.task')
        self.assertEqual(rows['task:00T000000000002AAA']['kind'], 'salesforce.activity')
        self.assertIn('Budget approved', rows['task:00T000000000002AAA']['body'])
        self.assertEqual(result['events'], 4)
        self.assertEqual(self.writes, [])  # Update contact details is off: nothing is written
        # The deal is a Graph project, its signal on it
        with self.store.connect() as db:
            self.assertEqual([r[0] for r in db.execute('SELECT p.name FROM projects p JOIN event_projects ep ON ep.project_id=p.id')], ['Globex rollout'])
        # The CRM's job title for the people on what was kept, as a record about them
        self.assertIn((['email:ann@globex.example'], {'title': 'CTO'}, 1), [(o['ids'], o['facts'], o['rank']) for o in self.offered])

    def test_stage_and_amount_changes_are_new_signals_and_replay_adds_nothing(self):
        self.sync()
        self.sync()
        self.assertEqual(len([s for s in self.rows() if s.startswith('opportunity:')]), 1)
        self.org.opportunities[1]['StageName'] = 'Closed Won'
        self.org.opportunities[0]['Amount'] = 15000
        self.sync()
        rows = self.rows()
        moved = rows['opportunity:006000000000002AAA:Closed Won:5000']
        self.assertEqual(moved['title'], 'Deal moved: Old deal')
        self.assertIn('Stage: Closed Won (was Negotiation)', moved['body'])
        bigger = rows['opportunity:006000000000001AAA:Proposal:15000']
        self.assertEqual(bigger['title'], 'Deal amount changed: Globex rollout')
        self.assertIn('Amount: 15,000 (was 12,000)', bigger['body'])

    def test_the_owners_task_once_done_updates_its_signal(self):
        self.sync()
        self.org.tasks[0].update(IsClosed=True, Status='Completed', CompletedDateTime='2026-11-09T11:30:00.000+0000')
        self.sync()
        task = self.rows()['task:00T000000000001AAA']
        self.assertEqual(task['kind'], 'salesforce.task')
        self.assertTrue(task['metadata']['closed'])

    def test_the_token_goes_only_to_a_salesforce_host(self):
        for bad in ('https://evil.example', 'http://acme.my.salesforce.com', 'https://acme.my.salesforce.com.evil.example',
                    'https://user@acme.my.salesforce.com', 'https://acme.my.salesforce.com:8443'):
            self.assertIsNone(salesforce.instance_url(bad), bad)
        self.assertEqual(salesforce.instance_url('https://acme.my.salesforce.com/'), 'https://acme.my.salesforce.com')
        self.instance = 'https://evil.example'
        with self.assertRaises(a.SourceError) as caught:
            self.sync()
        self.assertEqual(caught.exception.category, 'salesforce_broker')

    def test_reads_and_writes_stay_on_the_allowlist(self):
        source = salesforce.Source(self.config, ACCOUNT, self.helpers)
        for path in ('/services/data/v62.0/sobjects/Contact/' + ANN, '/services/data/v62.0/sobjects/User', '/services/apexrest/x'):
            with self.assertRaises(a.SourceError):
                source.get(path)
        for contact, fields in ((ANN, {'Email': 'x@y.example'}), (ANN, {'AccountId': '001000000000009AAA'}), (ANN, {'Title': ''}),
                                ('006000000000001AAA', {'Title': 'CTO'}), (ANN, {})):
            with self.assertRaises(a.SourceError):
                source.update(contact, fields)
        self.assertEqual(self.writes, [])
        self.assertEqual(salesforce.quoted("o'neil@x.example"), "'o\\'neil@x.example'")

    def test_wrong_signin_is_refused(self):
        mail_grants.put(self.config, 'salesforce', 'someone@else.example', 'refresh-2')
        with self.assertRaises(a.SourceError) as caught:
            self.sync({**ACCOUNT, 'email': 'someone@else.example'})
        self.assertEqual(caught.exception.category, 'account_identity_mismatch')


class ContactSyncTests(OrgCase):
    """Update contact details: only newer details in the person's own words or the owner's, only what changed, never a
    blank, never email or account; preview first; a dated line on the person per change."""

    def facts(self):
        return [('li:ann-1', 'title', 'CTO', enrichment.STATED, 'linkedin', '2026-11-08T09:00:00+00:00'),
                ('li:ann-1', 'linkedin_url', 'https://www.linkedin.com/in/ann-example', enrichment.STATED, 'linkedin', '2026-11-08T09:00:00+00:00'),
                ('email:ann@globex.example', 'phone', '+32470000001', enrichment.STATED, 'slack', '2026-11-08T09:00:00+00:00'),  # the same number
                ('email:ann@globex.example', 'company', 'Umbrella', enrichment.STATED, 'linkedin', '2026-11-08T09:00:00+00:00')]

    def turn_on(self):
        app = types.SimpleNamespace(config={**self.config, 'accounts': [ACCOUNT]}, store=self.store, sync_lock=lambda _: __import__('threading').Lock(),
                                    sync_soon=lambda _: None)
        bound = lambda args: a.App.connector_contact_sync(app, args)
        with patch('machine.app.sync.CONNECTOR_HELPERS', self.helpers):
            with self.assertRaises(ValueError):
                bound({'account': ACCOUNT['id'], 'do': 'on'})  # not before the owner saw what would change
            shown = bound({'account': ACCOUNT['id'], 'do': 'preview'})
            self.assertEqual(self.writes, [])
            on = bound({'account': ACCOUNT['id'], 'do': 'on'})
        self.assertTrue(on['crm']['contact_sync'])
        return shown

    def test_preview_then_on_updates_only_what_changed(self):
        self.person('ann@globex.example', facts=self.facts())
        shown = self.turn_on()
        self.assertEqual([(c['field'], c['old'], c['new']) for c in shown['changes'][0]['changes']],
                         [('title', 'VP Engineering', 'CTO'), ('linkedin_url', None, 'https://www.linkedin.com/in/ann-example')])
        self.sync()
        self.assertEqual(self.writes, [(f'/services/data/v62.0/sobjects/Contact/{ANN}',
                                        {'Title': 'CTO', 'LinkedIn__c': 'https://www.linkedin.com/in/ann-example'})])
        with self.store.connect() as db:
            node = db.execute("SELECT * FROM graph_nodes WHERE id='email:ann@globex.example'").fetchone()
            lines = crm.changes(db, node)
        self.assertEqual({(c['field'], c['new']['field'], c['new']['value'], c['at'][:10]) for c in lines},
                         {('crm_sync', 'title', 'CTO', '2026-11-09'), ('crm_sync', 'linkedin_url', 'https://www.linkedin.com/in/ann-example', '2026-11-09')})
        card = salesforce.card(ACCOUNT, self.store.checkpoint(ACCOUNT['id']))
        self.assertEqual(card['contact_updates'][0]['name'], 'Ann Example')

    def test_a_change_made_in_salesforce_after_wins(self):
        self.person('ann@globex.example', facts=self.facts())
        self.org.contacts[0]['LastModifiedDate'] = '2026-11-09T09:00:00.000+0000'  # edited there after the Machine learned it
        self.assertEqual(self.turn_on()['changes'], [])
        self.sync()
        self.assertEqual(self.writes, [])

    def test_guesses_and_crm_records_are_never_written_and_nothing_is_blanked(self):
        self.person('ann@globex.example', facts=[
            ('li:ann-1', 'title', 'Head of IT', enrichment.RECORD, 'google', '2026-11-08T09:00:00+00:00'),     # a record, not their words
            ('email:ann@globex.example', 'title', 'Chief', enrichment.STATED, 'salesflare', '2026-11-08T09:00:00+00:00')])  # a CRM's
        self.assertEqual(self.turn_on()['changes'], [])
        with self.store.connect() as db:
            plan = crm_sync.plan(db, [{'id': ANN, 'email': 'ann@globex.example', 'title': 'CTO', 'modified': None}], 'Salesforce')
        self.assertEqual(plan, [])

    def test_the_owners_own_edit_counts_and_no_linkedin_field_means_no_linkedin(self):
        self.org.linkedin_field = False
        self.person('ann@globex.example', facts=self.facts(), edits={'title': 'Chief Technology Officer'})
        shown = self.turn_on()
        self.assertEqual([(c['field'], c['new'], c['from']) for c in shown['changes'][0]['changes']], [('title', 'CTO', 'LinkedIn')])
        with self.store.connect() as db:  # the owner's edit, newer than the LinkedIn title, wins
            db.execute("UPDATE person_edits SET updated_at='2026-11-09T09:00:00+00:00'")
        self.store.commit_page(ACCOUNT['id'], {**self.store.checkpoint(ACCOUNT['id']), 'contact_preview_at': NOW, 'linkedin_checked': None}, [])
        shown = self.turn_on()
        self.assertEqual([(c['field'], c['new'], c['from']) for c in shown['changes'][0]['changes']], [('title', 'Chief Technology Officer', 'you')])

    def test_a_refused_update_is_skipped_and_a_later_edit_there_is_left_alone(self):
        self.person('ann@globex.example', facts=self.facts())
        self.turn_on()
        self.patch_status = 400  # a validation rule in the org
        self.sync()
        self.assertEqual(salesforce.card(ACCOUNT, self.store.checkpoint(ACCOUNT['id']))['contact_failed'], 1)
        self.patch_status = 204
        state = self.store.checkpoint(ACCOUNT['id'])
        state.pop('contact_sync_at')
        self.store.commit_page(ACCOUNT['id'], state, [])
        self.sync()
        self.assertEqual(len(self.writes), 2)
        # Someone sets another title in Salesforce afterwards: the Machine doesn't write its own back
        self.org.contacts[0].update(Title='CTO and co-founder', LastModifiedDate='2026-10-02T09:00:00.000+0000')
        with self.store.connect() as db:
            plan = crm_sync.plan(db, [{'id': ANN, 'email': 'ann@globex.example', 'title': 'CTO and co-founder', 'modified': '2026-10-02T09:00:00+00:00'}],
                                 'Salesforce', self.store.checkpoint(ACCOUNT['id'])['contact_written'], fields=('title',))
        self.assertEqual(plan, [])

    def test_off_stops_it_and_a_shared_connection_never_writes(self):
        self.person('ann@globex.example', facts=self.facts())
        self.turn_on()
        state = self.store.checkpoint(ACCOUNT['id'])
        self.sync({**ACCOUNT, 'shared': {'fleet_name': 'Acme'}})
        self.assertEqual(self.writes, [])
        self.assertFalse(salesforce.card({**ACCOUNT, 'shared': {'fleet_name': 'Acme'}}, state)['contact_sync'])
        state.pop('contact_sync')
        self.store.commit_page(ACCOUNT['id'], state, [])
        self.sync()
        self.assertEqual(self.writes, [])


if __name__ == '__main__':
    unittest.main()
