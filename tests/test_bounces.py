"""Bounced email addresses (bounces.py): delivery reports read from their structure (a Gmail DSN, an Outlook NDR, a
soft bounce), recorded per address, cleared when the address works again, shown on the person, kept off drafts' To,
and used by automated follow-ups (another channel, or "Email bounced") and the review. No live sends."""
import base64
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

import bounces
import follow_ups
import graph
import ms_graph
import test_ux as ux
a = ux.a

GMAIL = {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Example'}
LINKEDIN = {'id': 'li', 'service': 'linkedin', 'transport': 'browser', 'boundary': 'work:Example'}
NOW = '2026-10-19T09:00:00+00:00'


def b64(text):
    return base64.urlsafe_b64encode(text.encode()).decode().rstrip('=')


def gmail_dsn(recipient='sam@client.example', status='5.1.1', action='failed', original='<orig-1@mail.example.com>'):
    """A Gmail "Delivery Status Notification" as the Gmail API's "full" format gives it."""
    report = (f'Reporting-MTA: dns; googlemail.com\nArrival-Date: Mon, 12 Oct 2026 02:00:00 -0700 (PDT)\n\n'
              f'Final-Recipient: rfc822; {recipient}\nAction: {action}\nStatus: {status}\n'
              'Diagnostic-Code: smtp; 550-5.1.1 The email account that you tried to reach does not exist.\n')
    headers = [{'name': 'From', 'value': 'Mail Delivery Subsystem <mailer-daemon@googlemail.com>'},
               {'name': 'To', 'value': 'owner@example.com'}, {'name': 'Subject', 'value': 'Delivery Status Notification (Failure)'},
               {'name': 'Message-ID', 'value': '<dsn-1@mx.google.com>'}, {'name': 'In-Reply-To', 'value': original},
               {'name': 'Content-Type', 'value': 'multipart/report; report-type=delivery-status; boundary="x"'}]
    if action == 'failed':
        headers.append({'name': 'X-Failed-Recipients', 'value': recipient})
    return {'mimeType': 'multipart/report', 'headers': headers, 'parts': [
        {'partId': '0', 'mimeType': 'multipart/related', 'parts': [
            {'partId': '0.0', 'mimeType': 'text/plain', 'body': {'data': b64("** Address not found **\n\nYour message wasn't delivered.")}}]},
        {'partId': '1', 'mimeType': 'message/delivery-status', 'body': {'data': b64(report)}},
        {'partId': '2', 'mimeType': 'message/rfc822', 'body': {'size': 0}, 'parts': [
            {'partId': '2.0', 'mimeType': 'text/plain', 'headers': [{'name': 'From', 'value': 'owner@example.com'},
                                                                   {'name': 'Message-ID', 'value': original}], 'body': {'data': b64('Hi Sam')}}]}]}


OUTLOOK_NDR = b"""From: Microsoft Outlook <postmaster@contoso.example>
To: <owner@example.com>
Subject: Undeliverable: Pilot
Message-ID: <ndr-1@contoso.example>
MIME-Version: 1.0
Content-Type: multipart/report; report-type=delivery-status; boundary="b1"

--b1
Content-Type: text/plain; charset=utf-8

Delivery has failed to these recipients or groups:
lee@contoso.example
The email address you entered couldn't be found.

--b1
Content-Type: message/delivery-status

Reporting-MTA: dns;AM0PR.eurprd.prod.outlook.com

Final-Recipient: rfc822;lee@contoso.example
Action: failed
Status: 5.1.10
Diagnostic-Code: smtp;550 5.1.10 RESOLVER.ADR.RecipientNotFound

--b1
Content-Type: message/rfc822

From: Owner <owner@example.com>
To: lee@contoso.example
Subject: Pilot
Message-ID: <orig-2@example.com>

Hi Lee
--b1--
"""


def mail(source_id, at, mine=False, who='sam@client.example', thread='t1', title='Pilot', body='About the pilot.', **meta):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': title, 'body': body,
            'deleted': False, 'metadata': {'from': 'Owen Owner <owner@example.com>' if mine else f'Sam Client <{who}>',
                                           'to': who if mine else 'owner@example.com', 'thread_id': thread,
                                           'labels': ['SENT'] if mine else ['INBOX'], **meta}}


def report(source_id, at, recipient='sam@client.example', thread='t1', status='5.1.1', action='failed', original='<orig-1@mail.example.com>'):
    found = bounces.read_report(gmail_dsn(recipient, status, action, original))
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': 'Delivery Status Notification (Failure)',
            'body': "** Address not found **", 'deleted': False,
            'metadata': {'from': 'Mail Delivery Subsystem <mailer-daemon@googlemail.com>', 'to': 'owner@example.com', 'thread_id': thread,
                         'labels': ['INBOX', 'CATEGORY_UPDATES'], 'in-reply-to': original, **({'bounce': found} if found else {})}}


class Reading(unittest.TestCase):
    """Delivery reports read from their structure, never their wording."""

    def test_a_gmail_dsn(self):
        found = bounces.read_report(gmail_dsn())
        self.assertEqual(found, {'recipients': [{'address': 'sam@client.example', 'kind': 'hard', 'status': '5.1.1'}],
                                 'original_id': '<orig-1@mail.example.com>', 'via': 'report'})

    def test_an_outlook_ndr_through_microsoft_graph(self):
        found = bounces.read_report(ms_graph.payload(OUTLOOK_NDR))
        self.assertEqual(found, {'recipients': [{'address': 'lee@contoso.example', 'kind': 'hard', 'status': '5.1.10'}],
                                 'original_id': '<orig-2@example.com>', 'via': 'report'})

    def test_a_soft_bounce_and_a_full_mailbox_are_soft(self):
        self.assertEqual(bounces.read_report(gmail_dsn(status='4.4.7', action='delayed'))['recipients'][0]['kind'], 'soft')
        self.assertEqual(bounces.read_report(gmail_dsn(status='5.2.2'))['recipients'][0]['kind'], 'soft')  # a full mailbox
        self.assertEqual(bounces.read_report(gmail_dsn(status='5.7.1'))['recipients'][0]['kind'], 'hard')
        self.assertIsNone(bounces.kind_of('2.0.0', 'delivered'))

    def test_a_normal_message_or_a_postmaster_notice_is_no_report(self):
        plain = {'mimeType': 'text/plain', 'headers': [{'name': 'From', 'value': 'postmaster@shop.example'}],
                 'body': {'data': b64('Your invoice 5.1.1 is ready. Write to billing@shop.example.')}}
        self.assertIsNone(bounces.read_report(plain))
        self.assertIsNone(bounces.from_event({'kind': 'gmail.message', 'body': 'Your invoice 5.1.1 is ready, billing@shop.example',
                                              'metadata': {'from': 'postmaster@shop.example', 'labels': ['INBOX']}}))

    def test_collection_keeps_the_report_with_the_message(self):
        raw = {'id': 'm1', 'threadId': 't1', 'labelIds': ['INBOX'], 'internalDate': '1760000000000', 'snippet': 'Address not found', 'payload': gmail_dsn()}
        event = a.message_event({'id': 'work', 'email': 'owner@example.com'}, raw)
        self.assertEqual(event['metadata']['bounce']['recipients'][0]['address'], 'sam@client.example')
        normal = {**raw, 'payload': {'mimeType': 'text/plain', 'headers': [{'name': 'From', 'value': 'sam@client.example'}], 'body': {'data': b64('Hi')}}}
        self.assertNotIn('bounce', a.message_event({'id': 'work', 'email': 'owner@example.com'}, normal)['metadata'])

    def test_the_text_is_only_a_fallback_for_the_address(self):
        no_fields = gmail_dsn()
        no_fields['parts'][1] = {'partId': '1', 'mimeType': 'message/delivery-status', 'body': {'data': b64('Reporting-MTA: dns; x\n')}}
        no_fields['headers'] = [h for h in no_fields['headers'] if h['name'] != 'X-Failed-Recipients']
        no_fields['parts'][0]['parts'][0]['body']['data'] = b64('Delivery to kim@other.example failed: 550 5.1.1 user unknown')
        self.assertEqual(bounces.read_report(no_fields)['recipients'], [{'address': 'kim@other.example', 'kind': 'hard', 'status': '5.1.1'}])


class Recording(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p = patch.object(a, 'LOCAL_TZ', ZoneInfo('Europe/Brussels'))
        p.start()
        self.addCleanup(p.stop)
        self.clock = patch.object(a, 'now', return_value=NOW)
        self.clock.start()
        self.addCleanup(lambda: self.clock.stop())
        unread = patch.object(a.Gmail, 'get', side_effect=a.SourceError('offline'))
        unread.start()
        self.addCleanup(unread.stop)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')

    def at(self, stamp):
        self.clock.stop()
        self.clock = patch.object(a, 'now', return_value=stamp)
        self.clock.start()

    def app(self, **config):
        app = object.__new__(a.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL], 'digest_at': '08:30', 'review_worker': {'enabled': True}, **config}
        app.model_usage = None
        app.usage_limit = None
        app.fleet = None
        app.teammate_addresses = lambda: []
        return app

    def add(self, *events, account='work'):
        self.store.commit_page(account, {}, list(events))
        with self.store.connect() as db:
            return {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}

    def build(self):
        with self.store.connect() as db:
            graph.build(db, self.app().config, a.now())

    def flags(self, *addresses):
        with self.store.connect() as db:
            return bounces.flags(db, addresses or ['sam@client.example'])

    def test_a_hard_bounce_is_recorded_on_the_address_and_shows_on_the_person(self):
        self.add(mail('out1', '2026-10-12T09:00:00+00:00', mine=True), report('dsn1', '2026-10-12T09:00:05+00:00'))
        self.assertEqual(self.app().bounce_step()['flagged'], 1)
        flag = self.flags()['sam@client.example']
        self.assertEqual((flag['at'], flag['kind'], flag['status']), ('2026-10-12T09:00:05+00:00', 'hard', '5.1.1'))
        self.build()
        with self.store.connect() as db:
            person = graph.with_fleet(db, graph.detail(db, 'email:sam@client.example'), {})
        row = person['emails'][0]
        self.assertEqual((row['value'], row['bounced_at'], row['bounce_kind']), ('sam@client.example', '2026-10-12T09:00:05+00:00', 'hard'))
        self.assertEqual(person['bounced'], {'sam@client.example': '2026-10-12T09:00:05+00:00'})
        self.assertEqual(self.app().bounce_step()['flagged'], 0)  # once

    def test_another_working_address_becomes_the_first(self):
        self.add(mail('out1', '2026-10-12T09:00:00+00:00', mine=True), report('dsn1', '2026-10-12T09:00:05+00:00'))
        self.build()
        with self.store.connect() as db:
            graph.person_edit(db, 'email:sam@client.example', {'emails': ['sam@client.example', 'sam@newco.example']}, a.now())
        self.build()
        self.app().bounce_step()
        with self.store.connect() as db:
            person = graph.with_fleet(db, graph.detail(db, 'email:sam@client.example'), {})
            self.assertEqual([e['value'] for e in person['emails']], ['sam@newco.example', 'sam@client.example'])
            self.assertEqual(bounces.working(db, 'sam@client.example'), 'sam@newco.example')

    def test_a_later_reply_clears_it(self):
        self.add(mail('out1', '2026-10-12T09:00:00+00:00', mine=True), report('dsn1', '2026-10-12T09:00:05+00:00'))
        self.app().bounce_step()
        self.add(mail('in1', '2026-10-14T09:00:00+00:00'))
        self.app().bounce_step()
        self.assertEqual(self.flags(), {})
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT cleared_by FROM email_bounces').fetchone()[0], 'reply')

    def test_a_later_send_clears_it_after_48_hours_without_a_bounce(self):
        self.add(mail('out1', '2026-10-12T09:00:00+00:00', mine=True), report('dsn1', '2026-10-12T09:00:05+00:00'),
                 mail('out2', '2026-10-17T10:00:00+00:00', mine=True))
        self.at('2026-10-18T09:00:00+00:00')
        self.app().bounce_step()
        self.assertIn('sam@client.example', self.flags())  # not 48 hours yet
        self.at('2026-10-19T11:00:00+00:00')
        self.app().bounce_step()
        self.assertEqual(self.flags(), {})

    def test_a_later_send_that_bounces_again_keeps_it(self):
        self.add(mail('out1', '2026-10-12T09:00:00+00:00', mine=True), report('dsn1', '2026-10-12T09:00:05+00:00'),
                 mail('out2', '2026-10-15T10:00:00+00:00', mine=True), report('dsn2', '2026-10-15T10:00:04+00:00', original='<o2@x>'))
        self.app().bounce_step()
        self.assertEqual(self.flags()['sam@client.example']['at'], '2026-10-15T10:00:04+00:00')

    def test_soft_bounces_count_only_three_times_over_a_week(self):
        soft = lambda sid, at: report(sid, at, status='4.4.7', action='delayed')
        self.add(mail('out1', '2026-10-01T09:00:00+00:00', mine=True), soft('s1', '2026-10-01T10:00:00+00:00'), soft('s2', '2026-10-02T10:00:00+00:00'),
                 soft('s3', '2026-10-03T10:00:00+00:00'))
        self.app().bounce_step()
        self.assertEqual(self.flags(), {})  # three, but within two days
        self.add(soft('s4', '2026-10-09T10:00:00+00:00'))
        self.app().bounce_step()
        self.assertEqual(self.flags()['sam@client.example']['kind'], 'soft')

    def test_the_owners_own_address_is_never_flagged(self):
        self.add(report('dsn1', '2026-10-12T09:00:05+00:00', recipient='owner@example.com'))
        self.app().bounce_step()
        self.assertEqual(self.flags('owner@example.com'), {})

    def test_the_backfill_reads_reports_collected_before_from_their_text(self):
        old = report('dsn1', '2026-10-12T09:00:05+00:00', recipient='lee@contoso.example', thread='t9', original='<o9@x>')
        old['metadata'].pop('bounce')  # collected before reports were read at collection
        old['body'] = ("** Address not found **\n\nYour message wasn't delivered to lee@contoso.example.\n\n"
                       'Final-Recipient: rfc822; lee@contoso.example\nAction: failed\nStatus: 5.1.3\n')
        notice = mail('ar24', '2026-10-12T10:00:00+00:00', who='postmaster@jewels.example', body='A document was sent to you. Ref 5.1.1, lee@contoso.example')
        self.add(mail('out9', '2026-10-12T09:00:00+00:00', mine=True, who='lee@contoso.example', thread='t9'), old, notice)
        self.assertEqual(self.app().bounce_step()['flagged'], 1)
        self.assertEqual(set(self.flags('lee@contoso.example')), {'lee@contoso.example'})
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT original_id,thread_id FROM email_bounce_events').fetchall()[0][:], ('<o9@x>', 't9'))

    def test_a_draft_never_picks_a_bounced_to_when_another_address_exists(self):
        self.add(mail('out1', '2026-10-12T09:00:00+00:00', mine=True), report('dsn1', '2026-10-12T09:00:05+00:00'))
        self.build()
        self.app().bounce_step()
        draft = {'kind': 'email', 'account_id': 'work', 'to': ['sam@client.example'], 'subject': 'Pilot', 'body': 'Hi Sam'}
        with self.store.connect() as db:
            # Their only address: kept, and the send sheet warns
            self.assertEqual(bounces.steer(db, draft, ['sam@client.example'])[0]['to'], ['sam@client.example'])
            self.assertEqual(bounces.mark_draft(db, draft)['bounced'], {'sam@client.example': '2026-10-12T09:00:05+00:00'})
            graph.person_edit(db, 'email:sam@client.example', {'emails': ['sam@client.example', 'sam@newco.example']}, a.now())
        self.build()
        with self.store.connect() as db:
            steered, options = bounces.steer(db, [draft], ['sam@client.example', 'kim@other.example'])
            self.assertEqual(steered[0]['to'], ['sam@newco.example'])
            self.assertEqual(options, ['sam@newco.example', 'kim@other.example'])
            self.assertNotIn('bounced', bounces.mark_draft(db, steered[0]))

    def test_a_bounced_person_is_looked_up_again(self):
        self.add(mail('out1', '2026-10-12T09:00:00+00:00', mine=True))
        self.build()
        with self.store.connect() as db:
            db.execute("INSERT INTO person_profiles(identifier,status,profile,fetched_at) VALUES('email:sam@client.example','found','{}','2026-10-10T00:00:00+00:00')")
        self.add(report('dsn1', '2026-10-12T09:00:05+00:00'))
        self.app().bounce_step()
        with self.store.connect() as db:
            self.assertLess(db.execute('SELECT fetched_at FROM person_profiles').fetchone()[0], '2000')

    def test_the_review_sees_the_bounce_and_whether_it_matters(self):
        ids = self.add(mail('out1', '2026-10-12T09:00:00+00:00', mine=True), report('dsn1', '2026-10-12T09:00:05+00:00'))
        with self.store.connect() as db:
            graph.label(db, [ids['out1']], 'Acme pilot', 'review', NOW)
        self.build()
        self.app().bounce_step()
        hints = self.store.bounce_hints({}, [ids['dsn1'], ids['out1']])
        self.assertEqual(list(hints), [ids['dsn1']])
        hint, = hints[ids['dsn1']]['bounce']
        self.assertEqual((hint['address'], hint['kind'], hint['projects'], hint['other_address']), ('sam@client.example', 'hard', ['Acme pilot'], None))


class FollowUpsAfterABounce(Recording):
    def setUp(self):
        super().setUp()
        self.ev = self.add(mail('in1', '2026-10-08T09:00:00+00:00'), mail('out1', '2026-10-13T09:00:00+00:00', mine=True))
        with self.store.connect() as db:
            self.board = graph.save_board(db, {'name': 'Alpha testers', 'stages': [{'name': 'Invited'}, {'name': 'Testing'}, {'name': 'Live'}],
                                               'about': 'People trying the alpha.'}, '2026-10-01T09:00:00+00:00')['board_id']
            self.acme = graph.label(db, [self.ev['in1'], self.ev['out1']], 'Acme pilot', 'review', NOW)
            db.execute("UPDATE projects SET board_id=?,stage='Invited',stage_by='review',stage_at='2026-10-01T09:00:00+00:00' WHERE id=?", (self.board, self.acme))

    def turn_on(self, **settings):
        return self.app(**self.config).action('follow_up_save', {'scope': 'board', 'id': self.board, 'settings': {'on': True, **settings}}, owner_dashboard=True)

    config = {}

    def plan(self):
        app = self.app(**self.config)
        with self.store.connect() as db:
            return {x['project']['id']: x for x in follow_ups.plan(db, a.now(), app.follow_up_sendable(), app.follow_up_mine(), app.follow_up_own(db))}

    def test_without_a_bounce_it_follows_up_by_email(self):
        self.turn_on()
        self.assertEqual((self.plan()[self.acme]['state'], self.plan()[self.acme]['channel']), ('due', 'email'))

    def test_a_bounce_stops_email_follow_ups_and_is_no_reply(self):
        ids = self.add(report('dsn1', '2026-10-13T09:00:05+00:00'))
        with self.store.connect() as db:
            graph.label(db, [ids['dsn1']], 'Acme pilot', 'review', NOW)  # the report is in the project's thread
        self.turn_on()
        self.app().bounce_step()
        item = self.plan()[self.acme]
        self.assertEqual((item['state'], item['reason']), ('off', 'bounced'))  # not "replied": a report is no reply
        self.assertEqual(self.app().follow_up_step()['drafted'], 0)
        with self.store.connect() as db:
            boards = graph.boards(db, a.now())
            self.app().follow_up_annotate(db, boards)
        self.assertEqual(boards[0]['projects'][0]['follow_up']['reason'], 'bounced')  # "Email bounced" on the project

    def test_with_linkedin_allowed_and_there_it_switches(self):
        self.config = {'accounts': [GMAIL, LINKEDIN]}
        self.add({'account_id': 'li', 'source_id': 'li1', 'kind': 'linkedin.message', 'occurred_at': '2026-10-09T09:00:00+00:00', 'title': 'Sam Client',
                  'body': 'Nice to meet you', 'deleted': False, 'metadata': {'conversation_id': 'c1', 'from': 'Sam Client', 'from_me': False}}, account='li')
        with self.store.connect() as db:
            li = db.execute("SELECT id FROM events WHERE source_id='li1'").fetchone()[0]
            graph.label(db, [li], 'Acme pilot', 'review', NOW)
        self.add(report('dsn1', '2026-10-13T09:00:05+00:00'))
        self.turn_on()
        self.app(**self.config).bounce_step()
        item = self.plan()[self.acme]
        self.assertEqual((item['state'], item['channel']), ('due', 'linkedin'))

    def test_an_open_email_draft_stops_and_a_sent_follow_up_that_bounced_is_marked(self):
        self.turn_on()
        self.assertEqual(self.app().follow_up_step()['drafted'], 1)
        with self.store.connect() as db:
            sid = db.execute('SELECT suggestion_id FROM follow_up_cards').fetchone()[0]
        self.add(report('dsn1', '2026-10-13T09:00:05+00:00'))
        self.app().bounce_step()
        self.app().follow_up_step()
        with self.store.connect() as db:
            card = db.execute('SELECT state,why FROM follow_up_cards WHERE suggestion_id=?', (sid,)).fetchone()
            self.assertEqual(tuple(card), ('stopped', 'bounced'))
            self.assertEqual(db.execute("SELECT feedback FROM decisions WHERE id=?", ('follow-up-bounced:' + sid,)).fetchone()[0],
                             'Email bounced, so follow-ups stopped.')
        self.assertEqual((self.plan()[self.acme]['state'], self.plan()[self.acme]['reason']), ('off', 'bounced'))

    def test_a_sent_follow_up_that_bounces_is_marked_the_same_way(self):
        self.turn_on()
        self.app().follow_up_step()
        with self.store.connect() as db:
            sid = db.execute('SELECT suggestion_id FROM follow_up_cards').fetchone()[0]
            draft = {'kind': 'email', 'account_id': 'work', 'from': 'owner@example.com', 'to': ['sam@client.example'], 'subject': 'Re: Pilot',
                     'body': 'Any news?', 'thread_id': 't1', 'revision': 'r1'}
            # As the outbox leaves it once sent (no live send here)
            db.execute("UPDATE follow_up_cards SET state='sent',closed_at=? WHERE suggestion_id=?", (NOW, sid))
            db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) "
                       "VALUES('j1',?,?,?,'sent',?,?,'tap','dashboard','<fu-1@example.com>')", (sid, 'r1', json.dumps(draft), NOW, NOW))
        self.add(mail('fu1', NOW, mine=True), report('dsn2', '2026-10-19T09:00:04+00:00', original='<fu-1@example.com>'))
        self.app().bounce_step()
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT why FROM follow_up_cards WHERE suggestion_id=?', (sid,)).fetchone()[0], 'bounced')
            self.assertEqual(follow_ups.cards_view(db, [sid])[sid]['bounced'], True)
            self.assertEqual(db.execute("SELECT choice FROM decisions WHERE id=?", ('follow-up-bounced:' + sid,)).fetchone()[0], 'bounced')



class AnotherAddress(FollowUpsAfterABounce):
    """The bounced person has a working address: email follow-ups go on there ("Bounced, now to <address>")."""

    def other_address(self):
        self.build()
        with self.store.connect() as db:
            graph.person_edit(db, 'email:sam@client.example', {'emails': ['sam@client.example', 'sam@newco.example']}, a.now())
        self.build()

    def test_the_follow_up_goes_on_by_email_to_the_working_address(self):
        self.add(report('dsn1', '2026-10-13T09:00:05+00:00'))
        self.other_address()
        self.turn_on()
        self.app().bounce_step()
        item = self.plan()[self.acme]
        self.assertEqual((item['state'], item['channel']), ('due', 'email'))
        self.assertEqual(self.app().follow_up_step()['drafted'], 1)  # the report in the thread holds nothing up
        draft = {'kind': 'email', 'account_id': 'work', 'to': ['sam@client.example'], 'subject': 'Re: Pilot', 'body': 'Any news?'}
        with self.store.connect() as db:
            steered = bounces.steer(db, draft, [])[0]
            self.assertEqual(steered['to'], ['sam@newco.example'])
            self.assertEqual(bounces.mark_draft(db, steered)['moved'], {'sam@newco.example': 'sam@client.example'})  # "Bounced, now to ..."
            self.assertEqual(db.execute('SELECT state FROM follow_up_cards').fetchone()[0], 'open')  # not stopped


# The follow-ups harness (a board, two projects, a fake outbox and mailbox), without running its own tests again here
import test_follow_ups as tfu
_Harness = type('_Harness', (tfu.FollowUps,), {k: None for k in dir(tfu.FollowUps) if k.startswith('test_')})


class HeldBeforeItGoes(_Harness):
    """A follow-up drafted before its address bounced is held by the check right before it goes (as for a new message)."""

    def bounce(self, at='2026-10-19T08:50:00+00:00'):
        self.store.commit_page('work', {}, [report('dsn1', at)])
        self.app().bounce_step()

    def draft_of(self, sid):
        with self.store.connect() as db:
            return json.loads(db.execute('SELECT next_action FROM suggestions WHERE id=?', (sid,)).fetchone()[0])

    def test_it_moves_to_the_working_address_and_waits_for_send_again(self):
        transport = tfu.FakeOutbox()
        acme, _ = self.drafted(auto=True)
        self.send(acme)
        for step in ('build', 'edit', 'build'):
            with self.store.connect() as db:
                if step == 'build':
                    graph.build(db, self.app().config, a.now())
                else:
                    graph.person_edit(db, 'email:sam@client.example', {'emails': ['sam@client.example', 'sam@newco.example']}, a.now())
        self.bounce()
        step = self.outbox(transport)
        self.assertEqual(step('2026-10-19T09:00:00+00:00'), 'held')
        self.assertEqual(transport.sent, [])
        self.assertEqual(self.hold_of(acme), {'status': 'blocked', 'error': 'Not sent: sam@client.example bounced.', 'why': 'bounced', 'card': 'prepared'})
        draft = self.draft_of(acme)
        self.assertEqual(draft['to'], ['sam@newco.example'])
        self.assertNotEqual(draft['revision'], 'r-' + acme[:6])
        with self.store.connect() as db:
            self.assertEqual(bounces.mark_draft(db, draft)['moved'], {'sam@newco.example': 'sam@client.example'})
        self.assertEqual({c['project_id']: c['state'] for c in self.cards()}[self.acme], 'open')
        self.assertNotIn(acme, [sid for sid, _ in self.app().follow_up_send()])  # Send without asking is on, but this one waits for the owner
        # The owner's Send: it goes to the working address, and the report in the thread is no new message
        self.assertEqual(self.store.confirm_action(acme, draft['revision'], 'tap-again', 'dashboard')['status'], 'queued')
        for at in ('2026-10-19T09:05:00+00:00', '2026-10-19T09:06:00+00:00'):  # the other project's went alone first, then a gap
            step(at)
        self.assertIn(acme, [sid for sid, _ in transport.sent])
        with self.store.connect() as db:
            sent = db.execute("SELECT payload FROM action_jobs WHERE suggestion_id=? AND status='sent'", (acme,)).fetchone()
        self.assertEqual(json.loads(sent[0])['to'], ['sam@newco.example'])

    def test_with_no_other_address_it_is_held_and_stops(self):
        transport = tfu.FakeOutbox()
        acme, _ = self.drafted()
        self.send(acme)
        self.bounce()
        self.assertEqual(self.outbox(transport)('2026-10-19T09:00:00+00:00'), 'held')
        self.assertEqual(transport.sent, [])
        self.assertEqual((self.hold_of(acme)['error'], self.hold_of(acme)['why']), ('Not sent: sam@client.example bounced.', 'bounced'))
        self.assertEqual(self.draft_of(acme)['to'], ['sam@client.example'])
        card = {c['project_id']: (c['state'], c['why']) for c in self.cards()}[self.acme]
        self.assertEqual(card, ('stopped', 'bounced'))  # "Email bounced"

    def test_a_delivery_report_in_the_thread_is_no_new_message(self):
        base = {'at': '2026-10-13T09:00:00+00:00', 'source_id': 'out1', 'seen': ['in1', 'out1']}
        dsn = tfu.FakeMailbox.head('dsn1', '2026-10-19T08:50:00+00:00', 'Mail Delivery Subsystem <mailer-daemon@googlemail.com>', ['INBOX'])
        self.assertEqual(follow_ups.thread_since({'messages': [dsn]}, base, {'owner@example.com'}), [])


if __name__ == '__main__':
    unittest.main()
