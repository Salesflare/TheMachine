"""Every source reads well in the message viewer (machine/store/message_view.py, dashboard/events-email.js): each event
kind declares its view (email, chat, notification or card), and one made-up message of every kind keeps the rules:
no raw ids, Unix times or internal type names; nothing said twice; Slack's link brackets and ids gone; mail headers out
of the body; the real author, not the notifying bot. A new connector kind fails here until it has a view and a sample.
The dashboard test (test_message_view_dashboard.mjs) renders the same samples (dump()). All names and data are made up."""
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location('message_view_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
from machine.store import message_view, views  # noqa: E402
from machine.sources.connectors import connector_services, load_connector  # noqa: E402

AT = '2026-11-10T14:01:00+00:00'
GH_ISSUE = ('Exports stop at 10,000 rows. Steps:\n\n1. Open **Reports**\n2. Run `export --all`\n\n'
            '```\nError: limit reached\n```\n\nExpected: every row, see [the docs](https://docs.example/exports).')


def ev(account, sid, kind, title, body, **meta):
    return {'account_id': account, 'source_id': sid, 'kind': kind, 'occurred_at': AT, 'title': title, 'body': body,
            'deleted': False, 'metadata': meta}


# One message of every kind the viewer opens. Key: the kind (a second sample of a kind as kind#name).
SAMPLES = {
    'gmail.message': ev('mail', 'g1', 'gmail.message', 'Booth quote for the spring fair',
                        'Hi Robin,\n\nHere is the quote for the booth.\nIt includes the stand and two chairs.\n\nBest,\nAvery',
                        **{'from': 'Avery Stone <avery@booths.example>', 'to': 'Robin Hale <robin@owner.example>, Dana Reyes <dana@owner.example>',
                           'cc': 'Mira Holt <mira@owner.example>', 'source_url': 'https://mail.google.com/mail/u/0/#all/g1'}),
    'gmail.message#bare': ev('mail', 'g2', 'gmail.message', 'Fair stand sizes',
                             'Hi,\n\nThe stand comes in two sizes.\n\nAvery',
                             **{'from': 'avery@booths.example', 'to': 'robin@owner.example, nobody@unknown.example',
                                'source_url': 'https://mail.google.com/mail/u/0/#all/g2'}),
    'gmail.message#group': ev('mail', 'g3', 'gmail.message', 'Stand for the autumn fair',
                              'Hi,\n\nIs there still a stand free?\n\nPat',
                              **{'from': "\"'Pat Shop' via hello@team.example readers\" <hello@team.example>", 'to': 'hello@team.example',
                                 'source_url': 'https://mail.google.com/mail/u/0/#all/g3'}),
    # Details only when it adds something: To that is the address the header line shows ('"x" <x>'), a Reply-To to the
    # sender itself and a Sender on the sender's own domain add nothing, so no Details at all
    'gmail.message#to-only': ev('mail', 'g4', 'gmail.message', 'Volunteer day in spring',
                                'Hello,\n\nWe are planning a volunteer day.\n\nLee',
                                **{'from': 'Lee Park <lee@cause.example>', 'to': '"desk@owner.example" <desk@owner.example>',
                                   'reply-to': 'lee@cause.example', 'sender': 'bounces@lists.cause.example',
                                   'source_url': 'https://mail.google.com/mail/u/0/#all/g4'}),
    # a Reply-To elsewhere and a mail service's Sender: Details has those two rows, and no To row
    'gmail.message#reply-to': ev('mail', 'g5', 'gmail.message', 'This week in the paper',
                                 'Hi,\n\nHere is what we wrote this week.\n\nThe desk',
                                 **{'from': 'News Desk <news@paper.example>', 'to': 'desk@owner.example',
                                    'reply-to': 'Reader Team <readers@paper.example>', 'sender': 'bounce-77@mail2.sendhub.example',
                                    'source_url': 'https://mail.google.com/mail/u/0/#all/g5'}),
    # Cc with a name the header line shortens: a Cc row, no To row
    'gmail.message#cc': ev('mail', 'g6', 'gmail.message', 'Studio photos are ready',
                           'Hi,\n\nThe photos from the shoot are ready to pick.\n\nKai',
                           **{'from': 'Kai Brook <kai@studio.example>', 'to': 'desk@owner.example',
                              'cc': 'Noor Vance <noor@studio.example>, ops@studio.example', 'bcc': 'archive@owner.example',
                              'source_url': 'https://mail.google.com/mail/u/0/#all/g6'}),
    # Outlook mail reads through the same headers: it opens in Outlook, with Outlook's mark
    'gmail.message#outlook': ev('mail', 'g7', 'gmail.message', 'Room booking for Thursday',
                                'Hi,\n\nThe meeting room is booked for Thursday.\n\nJo',
                                **{'from': 'Jo Marsh <jo@office.example>', 'to': 'desk@owner.example',
                                   'source_url': 'https://outlook.office.com/mail/inbox/id/g7'}),
    'salesflare.email': ev('crm', 'email:1', 'salesflare.email', 'Checking in on your setup',
                           'From: Sam Rivera <sam@client.example>\nTo: Dana Reyes <dana@team.example>\nTo: Mira Holt <mira@team.example>\n\n'
                           'Hi Dana,\n\nHow is the setup going?\nAnything we can help with?\n\nThanks,\nSam',
                           **{'from': 'sam@client.example', 'source_url': 'https://app.salesflare.example/accounts/1'}),
    'slack.message': ev('slack', 'C1:1.1', 'slack.message', '#development-planning: Planning for :spiral_calendar_pad: next week',
                        'Planning for :spiral_calendar_pad: next week\nFeatures: <@U0KITNAVA1> and <@U0NOBODY01>, see <https://tracker.example/b/12|the board>'
                        ' and <https://tracker.example/b/13>. *Ship it* _soon_ ~maybe~ in <#C0GENERAL1|general> <!here>',
                        **{'channel_name': 'development-planning', 'conversation_type': 'channel', 'channel_id': 'C1',
                           'user_id': 'U0ROBIN001', 'sender_display': 'Rowan Vale', 'source_url': 'https://acme.slack.example/archives/C1/p11'}),
    'whatsapp.message': ev('wa', 'w1', 'whatsapp.message', 'Climbing crew', 'Who is in for *Saturday*?',
                           **{'chat_name': 'Climbing crew', 'chat_id': '1203@g.us', 'sender_display': 'Sasha Brook', 'from': 'Sasha Brook'}),
    'telegram.message': ev('tg', 't1', 'telegram.message', 'Milo Grant', 'Landed, see you at 6',
                           **{'chat_name': 'Milo Grant', 'chat_id': '42', 'sender_display': 'Milo Grant'}),
    'teams.message': ev('teams', 'tm1', 'teams.message', 'Launch room: Ready for review', 'Ready for review',
                        **{'chat_name': 'Launch room', 'sender_display': 'Kit Navarro', 'source_url': 'https://teams.example/l/1'}),
    'linkedin.message': ev('li', 'l1', 'linkedin.message', 'Dana Wolfe', 'Thanks for connecting!',
                           **{'chat_name': 'Dana Wolfe', 'conversation_id': 'c1', 'sender_display': 'Dana Wolfe'}),
    'x.dm': ev('x', 'xd1', 'x.dm', 'Pat Lowe', 'Is the beta still open?', **{'chat_name': 'Pat Lowe', 'conversation_id': 'x1', 'sender_display': 'Pat Lowe'}),
    'x.mention': ev('x', 'xm1', 'x.mention', 'Pat Lowe mentioned @owner', 'Loving the new release, @owner', **{'from': 'Pat Lowe'}),
    'intercom.conversation': ev('ic', '9101', 'intercom.conversation', 'Hi, how do I export my contacts?',
                                'Jordan Lake\nFacebook\nHi, how do I export my contacts?\n'
                                '1794488402 · Fin · conversation_attribute_updated_by_admin: \n'
                                '1794488430 · Fin · comment: I can help with that. Which plan are you on?\n'
                                '1794488463 · Andrea Cole · assignment: Hi Jordan, what is the email of your account?\n'
                                '1794488500 · Jordan Lake · comment: jordan@lake.example',
                                **{'conversation_id': '9101', 'from': 'jordan@lake.example', 'from_name': 'Jordan Lake',
                                   'contact_name': 'Jordan Lake', 'created_at': 1794488400, 'channel': 'facebook',
                                   'source_url': 'https://app.intercom.example/a/inbox/w1/inbox/shared/all/conversation/9101'}),
    # opened by Intercom's Operator bot: stored from its relay address, the customer named beside it
    'intercom.conversation#bot': ev('ic', '9102', 'intercom.conversation', 'Question about invoices',
                                    'Question about invoices\n1794488430 · Fin · comment: Happy to help. What is the invoice number?',
                                    **{'conversation_id': '9102', 'from': 'operator+abc123@intercom.io', 'from_name': 'Fin',
                                       'contact_email': 'sam@reed.example', 'contact_name': 'Sam Reed', 'created_at': 1794488400,
                                       'source_url': 'https://app.intercom.example/a/inbox/w1/inbox/shared/all/conversation/9102'}),
    'android.notification': ev('phone', 'n1', 'android.notification', 'Your daily digest is ready', 'Your daily digest is ready',
                               **{'package_name': 'com.medium.reader', 'app_name': 'Medium'}),
    # a group's summary notification, stored with its package id as the title (as older events were)
    'android.notification#summary': ev('phone', 'n2', 'android.notification', 'com.acmeshop.app', '',
                                       **{'package_name': 'com.acmeshop.app', 'app_name': 'com.acmeshop.app'}),
    'github.notification': ev('gh', 'n:1', 'github.notification', '[widgets] Exports stop at 10,000 rows when the report has filters',
                              'Issue in acme/widgets (open); why you got it: author.\n\n' + GH_ISSUE +
                              '\n\nLatest comment by sweeper[bot]:\nThis issue has had no activity for 30 days and will be closed.',
                              **{'repo': 'acme/widgets', 'reason': 'author', 'type': 'Issue', 'number': 812, 'state': 'open',
                                 'from': 'sweeper[bot]', 'source_url': 'https://github.example/acme/widgets/issues/812'}),
    'github.ci': ev('gh', 'ci:1', 'github.ci', '[widgets] Tests failed on main', 'Commit: Fix the export limit\nBy: kit',
                    **{'repo': 'acme/widgets', 'from': 'kit', 'source_url': 'https://github.example/acme/widgets/actions/runs/1'}),
    'shortcut.move': ev('sc', 's1', 'shortcut.move', 'Export to CSV', 'Moved: In progress → Done',
                        **{'source_url': 'https://app.shortcut.example/story/1'}),
    'trello.action': ev('tr', 'tr1', 'trello.action', 'Venue shortlist', 'Venue shortlist\nMoved to Doing by Kit Navarro',
                        **{'source_url': 'https://trello.example/c/1'}),
    'stripe.event': ev('st', 'st1', 'stripe.event', 'Payment failed: Harbor Ltd, €49.00',
                       'Payment failed: Harbor Ltd, €49.00.\nEmail: billing@harbor.example\nAttempt 2 of 4',
                       **{'source_url': 'https://dashboard.stripe.example/invoices/in_1'}),
    'salesforce.opportunity': ev('sf', 'o1', 'salesforce.opportunity', 'Deal: Harbor renewal', 'Stage: Proposal\nAmount: 12,000',
                                 **{'source_url': 'https://acme.salesforce.example/006'}),
    'salesforce.task': ev('sf', 't1', 'salesforce.task', 'Call back about pricing', 'Due: Friday\nWith: Sam Rivera', **{}),
    'salesforce.activity': ev('sf', 'a1', 'salesforce.activity', 'Intro meeting', 'With: Sam Rivera\n\nNotes:\nWants a demo', **{}),
    'salesflare.meeting': ev('crm', 'meeting:1', 'salesflare.meeting', 'Intro call', 'Notes: wants pricing', **{}),
    'zoom.summary': ev('zoom', 'z1', 'zoom.summary', 'Weekly sync', '## Summary\n- Ship the export fix\n- Plan the fair', **{}),
    'zoom.transcript': ev('zoom', 'z2', 'zoom.transcript', 'Weekly sync', 'Kit: Morning all\nRobin: Morning', **{}),
    'google_meet.notes': ev('meet', 'm1', 'google_meet.notes', 'Design review', '**Decisions**\n- Keep the blue', **{}),
    'google_meet.transcript': ev('meet', 'm2', 'google_meet.transcript', 'Design review', 'Kit: Shall we start?', **{}),
    'teams.notes': ev('teams', 'tn1', 'teams.notes', 'Planning', 'Action items: send the deck', **{}),
    'teams.transcript': ev('teams', 'tt1', 'teams.transcript', 'Planning', 'Kit: Hello', **{}),
    # a transcript the owner pasted on a meeting (meeting_notes.py), with its raw stamps
    'meeting.transcript': ev('cal', 'transcript:1', 'meeting.transcript', 'Weekly sync',
                             '[0:00:00] Kit Navarro: Morning all.\n[0:00:03] Kit Navarro: Shall we start with the export fix?\n'
                             '[0:00:06] Robin Hale: Yes, it shipped yesterday.\n[0:01:30] Kit Navarro: Great, then the fair.', **{}),
    'docs.comment': ev('docs', 'd1', 'docs.comment', 'Q4 plan', 'On: “launch in May”\n\nKit Navarro: Should this be June?',
                       **{'source_url': 'https://docs.google.com/document/d/1'}),
    'docs.mention': ev('docs', 'd2', 'docs.mention', 'Q4 plan', 'Kit Navarro: @Robin can you check the numbers?',
                       **{'source_url': 'https://docs.google.com/document/d/1'}),
    'docs.suggestion': ev('docs', 'd3', 'docs.suggestion', 'Q4 plan', 'Kit Navarro suggested: replace “May” with “June”', **{}),
    'docs.shared': ev('docs', 'd4', 'docs.shared', 'Budget 2027', 'Kit Navarro shared it with you',
                      **{'source_url': 'https://acme.sharepoint.com/x'}),
    'rss.item': ev('rss', 'r1', 'rss.item', 'Release notes 4.2', 'Faster exports and a new dark mode.', **{'source_url': 'https://blog.example/4-2'}),
}

TIMESTAMP = re.compile(r'(?<!\d)1[5-9]\d{8}(?!\d)')
INTERNAL = re.compile(r'\b(?:conversation_attribute_updated\w*|part_type|admin_assignee_id|why you got it|[a-z]+\.[a-z_]+\.?(?:message|notification|event))\b')
RAW = re.compile(r'<[@#!][A-Z0-9^]|<https?://|\b[UWC]0[A-Z0-9]{8,10}\b|\bcom\.\w+\.\w+|operator\+\S*@intercom\.io')


def fixture(folder):
    store = a.Store(Path(folder) / 'events.sqlite')
    by_account = {}
    for key, e in SAMPLES.items():
        by_account.setdefault(e['account_id'], []).append(e)
    for account, events in by_account.items():
        store.commit_page(account, {}, events, None)
    with store.connect() as db:
        ids = {(r['account_id'], r['source_id']): r['id'] for r in db.execute('SELECT id,account_id,source_id FROM events')}
        db.execute("INSERT INTO identity_names(identifier,name,checked_at) VALUES('slack:U0KITNAVA1','Kit Navarro','2026-11-10')")
        # People the graph knows by name, under their address (a sender stored by address shows by this name)
        for node, name in (('email:avery@booths.example', 'Avery Stone'), ('email:robin@owner.example', 'Robin Hale')):
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person',?,1,1,?)",
                       (node, name, json.dumps({'identifiers': [node], 'emails': [node[6:]]})))
    app = object.__new__(a.App)
    app.store = store
    app.store.accounts = []
    app.config = {'accounts': [], 'database': str(Path(folder) / 'events.sqlite')}
    return app, {key: ids[(e['account_id'], e['source_id'])] for key, e in SAMPLES.items()}


def dump(folder):
    """{kind: original} for the dashboard test."""
    app, ids = fixture(folder)
    return json.dumps({k: app.originals('', event_id=i)[0] for k, i in ids.items()})


def shown(o):
    """Every string the viewer shows for one original (a chat with turns shows its turns, not its stored text)."""
    out = [o.get('title'), o.get('from'), None if o.get('turns') else o.get('body'), o.get('sub'), o.get('context'), o.get('chat'), o.get('via')]
    out += [t.get('from') for t in o.get('turns') or ()] + [t.get('body') for t in o.get('turns') or ()]
    out += [v for v in (o.get('card') or {}).values() if isinstance(v, str)]
    return [str(s) for s in out if s]


class Registry(unittest.TestCase):
    def test_every_connector_kind_declares_a_view_and_an_app(self):
        for service in connector_services():
            plugin = load_connector(service)
            kinds = getattr(plugin, 'KINDS', None) or {}
            views = getattr(plugin, 'VIEWS', None)
            self.assertIsInstance(views, dict, f'connectors/{service}.py: add VIEWS (see docs/adding-a-source.md)')
            self.assertEqual(set(views), set(kinds), f'connectors/{service}.py: VIEWS names every kind in KINDS')
            self.assertTrue(set(views.values()) <= set(message_view.VIEWS), service)
            self.assertTrue(hasattr(plugin, 'APP'), f'connectors/{service}.py: add APP, the app its links open in')

    def test_every_connector_kind_has_a_sample_here(self):
        kinds = {k for s in connector_services() for k in (getattr(load_connector(s), 'KINDS', None) or {})}
        self.assertEqual(kinds - {k.split('#')[0] for k in SAMPLES}, set(),
                         'add a made-up message of the new kind to SAMPLES: it is checked against the viewer rules')


class Rules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        app, ids = fixture(cls.temp.name)
        cls.items = {k: app.originals('', event_id=i)[0] for k, i in ids.items()}
        cls.app = app

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_people_by_name_the_address_only_when_none_is_known(self):
        o = self.items['gmail.message#bare']
        self.assertEqual(o['from'], 'Avery Stone <avery@booths.example>')
        self.assertEqual(o['to'], 'Robin Hale <robin@owner.example>, nobody@unknown.example')
        # a to-do's source line, stored with the address, says the name too
        cards = [{'source_line': 'Source: email from avery@booths.example · Sun, Nov 8 (+1 more)'},
                 {'source_line': 'Source: email from nobody@unknown.example · Sun, Nov 8'},
                 {'source_line': 'Source: email from Avery Stone · Sun, Nov 8'}]
        with self.app.store.connect() as db:
            views.source_lines_shown(db, cards)
        self.assertEqual([c['source_line'] for c in cards], ['Source: email from Avery Stone · Sun, Nov 8 (+1 more)',
                                                              'Source: email from nobody@unknown.example · Sun, Nov 8',
                                                              'Source: email from Avery Stone · Sun, Nov 8'])

    def test_every_kind_reads_in_its_declared_view(self):
        for kind, o in self.items.items():
            self.assertEqual(o['view'], message_view.view_of(kind.split('#')[0]), kind)

    def test_no_raw_ids_times_or_type_names(self):
        for kind, o in self.items.items():
            for s in shown(o):
                self.assertIsNone(TIMESTAMP.search(s), (kind, s))
                self.assertIsNone(INTERNAL.search(s), (kind, s))
                self.assertIsNone(RAW.search(s), (kind, s))

    def test_nothing_said_twice(self):
        for kind, o in self.items.items():
            lines = [line for s in [o.get('title'), o.get('from'), o.get('sub'), o.get('via')] + (o.get('body') or '').split('\n')
                     if s for line in [s] if line.strip()]
            if o['view'] == 'chat':  # titled by its conversation (events-email.js chatTitle), then what was said
                lines = [o.get('subject') or o.get('chat'), *(t['body'] for t in o.get('turns') or [{'body': o['body']}])]
            norm = [message_view.re.sub(r'[\W_]+', ' ', str(x).casefold()).strip() for x in lines if x]
            self.assertEqual(len(norm), len(set(norm)), (kind, lines))

    def test_mail_headers_in_a_body_move_to_the_header(self):
        o = self.items['salesflare.email']
        self.assertEqual(o['view'], 'email')
        self.assertEqual(o['from'], 'Sam Rivera <sam@client.example>')
        self.assertEqual(o['to'], 'Dana Reyes <dana@team.example>, Mira Holt <mira@team.example>')
        self.assertTrue(o['body'].startswith('Hi Dana,'), o['body'])
        self.assertEqual(o['app'], 'Salesflare')

    def test_email_details_carry_only_what_the_header_doesnt_say(self):
        quiet = self.items['gmail.message#to-only']
        self.assertNotIn('reply_to', quiet)  # Reply-To is the sender itself
        self.assertNotIn('sent_via', quiet)  # sent from the sender's own domain
        self.assertNotIn('sender', quiet)
        loud = self.items['gmail.message#reply-to']
        self.assertEqual(loud['reply_to'], 'Reader Team <readers@paper.example>')
        self.assertEqual(loud['sent_via'], 'sendhub.example')
        self.assertEqual(self.items['gmail.message#cc']['bcc'], 'archive@owner.example')
        shaped = lambda **o: message_view.shape('gmail.message', {'title': 'Hi', 'body': 'Hello', **o}, {})
        self.assertNotIn('sent_via', shaped(**{'from': 'Pat via hello@team.example <hello@team.example>', 'sender': 'hello+bnc@team.example'}))
        self.assertEqual(shaped(**{'from': 'Shop <news@shop.example>', 'sender': 'b@em.mailer.co.uk'})['sent_via'], 'mailer.co.uk')
        # a CRM copy's Reply-To and Bcc header lines move to the header like To and Cc
        crm = message_view.shape('salesflare.email', {'title': 'Hi', 'from': 'sam@client.example', 'body':
                                 'From: Sam <sam@client.example>\nTo: dana@team.example\nBcc: log@team.example\nReply-To: help@client.example\n\nHello'}, {})
        self.assertEqual((crm['bcc'], crm['reply_to'], crm['body']), ('log@team.example', 'help@client.example', 'Hello'))

    def test_a_google_group_sender_reads_as_people_say_it(self):
        shown = lambda sender: message_view.shape('gmail.message', {'title': 'Hi', 'body': 'Hello', 'from': sender}, {})['from']
        self.assertEqual(shown("\"'Pat Shop' via hello@team.example readers\" <hello@team.example>"), 'Pat Shop via hello@team.example <hello@team.example>')
        self.assertEqual(shown("'Sam Lee' via Sales <sales@acme.example>"), 'Sam Lee via Sales <sales@acme.example>')
        self.assertEqual(shown('Sam Lee <sam@acme.example>'), 'Sam Lee <sam@acme.example>')

    def test_a_header_like_line_inside_the_text_stays(self):
        self.assertEqual(message_view.header_lines('Hi\nTo: whom it may concern'), ({}, 'Hi\nTo: whom it may concern'))
        self.assertEqual(message_view.header_lines('To: the team\nplease read'), ({}, 'To: the team\nplease read'))

    def test_slack_reads_as_markdown_with_names_and_plain_links(self):
        o = self.items['slack.message']
        self.assertEqual((o['view'], o['from'], o['chat']), ('chat', 'Rowan Vale', '#development-planning'))
        self.assertIn('[the board](https://tracker.example/b/12)', o['body'])
        self.assertIn(' https://tracker.example/b/13.', o['body'])
        self.assertIn('**Ship it** *soon* ~~maybe~~ in #general @here', o['body'])
        self.assertIn('@someone on Slack', o['body'])
        # the title in plain words, never Slack's link markup
        shown = lambda title: message_view.shape('slack.message', {'title': title, 'body': ''}, {})['title']
        self.assertEqual(shown('#sales: ask <mailto:pat@client.example|pat@client.example> about <https://tracker.example/b/12|the board>'),
                         '#sales: ask pat@client.example about the board')
        self.assertEqual(shown('#sales: *ship* it in <#C0GENERAL1|general>'), '#sales: ship it in #general')

    def test_an_unnamed_slack_sender_is_never_the_channel(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        store = a.Store(Path(temp.name) / 'e.sqlite')
        store.accounts = []
        e = dict(SAMPLES['slack.message'], source_id='C1:2.2', metadata={**SAMPLES['slack.message']['metadata'], 'sender_display': ''})
        store.commit_page('slack', {}, [e], None)
        with store.connect() as db:
            [i] = [r[0] for r in db.execute('SELECT id FROM events')]
        self.assertEqual(store.event_views([i])[0]['from'], '')

    def test_a_sender_known_only_by_address_shows_by_the_graphs_name_outside_email_too(self):
        sender_name = message_view.sender_name
        self.assertEqual(sender_name('stripe.event', {'from': 'billing@harbor.example', 'customer_name': 'Harbor Ltd'}), 'Harbor Ltd')
        self.assertEqual(sender_name('stripe.event', {'from': 'billing@harbor.example', 'customer_name': 'billing@harbor.example'}),
                         'billing@harbor.example')
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        app, _ = fixture(temp.name)  # the graph knows avery@booths.example as Avery Stone
        store = app.store
        pay = ev('st', 'st9', 'stripe.event', 'Invoice paid', 'Invoice paid', **{'from': 'avery@booths.example'})
        chat = ev('ic', '9109', 'intercom.conversation', 'Hi', 'Hi\n1794488500 · avery@booths.example · comment: thanks',
                  **{'conversation_id': '9109', 'from': 'avery@booths.example', 'contact_email': 'avery@booths.example', 'created_at': 1794488400})
        store.commit_page('st', {}, [pay], None)
        store.commit_page('ic', {}, [chat], None)
        with store.connect() as db:
            ids = [db.execute('SELECT id FROM events WHERE source_id=?', (s,)).fetchone()[0] for s in ('st9', '9109')]
        paid, talk = store.event_views(ids)
        self.assertEqual(paid['from'], 'Avery Stone')
        self.assertEqual((talk['from'], talk['chat']), ('Avery Stone', 'Avery Stone'))
        self.assertTrue(talk['turns'])
        self.assertNotIn('avery@booths.example', [t['from'] for t in talk['turns']])

    def test_intercom_is_a_chat_with_sides_and_no_system_parts(self):
        o = self.items['intercom.conversation']
        self.assertEqual((o['chat'], o['via']), ('Jordan Lake', 'Facebook'))
        self.assertEqual([(t['from'], t['role'], t['body']) for t in o['turns']], [
            ('Jordan Lake', 'customer', 'Hi, how do I export my contacts?'),
            ('Fin', 'bot', 'I can help with that. Which plan are you on?'),
            ('Andrea Cole', 'team', 'Hi Jordan, what is the email of your account?'),
            ('Jordan Lake', 'customer', 'jordan@lake.example')])

    def test_github_names_the_author_not_the_bot_and_the_comment_leads(self):
        o = self.items['github.notification']
        self.assertEqual(o['title'], 'Exports stop at 10,000 rows when the report has filters')
        self.assertEqual(o['card']['ref'], 'acme/widgets #812')
        self.assertEqual((o['card']['state'], o['card']['reason'], o['card']['comment_by'], o['card']['comment_bot']),
                         ('open', 'author', 'sweeper[bot]', True))
        self.assertTrue(o['body'].startswith('This issue has had no activity'))
        self.assertEqual(o['context'], GH_ISSUE)
        self.assertEqual(o['app'], 'GitHub')

    def test_a_notification_says_its_text_once(self):
        o = self.items['android.notification']
        self.assertEqual((o['view'], o['app_name'], o['title'], o['body'], o['from']), ('notification', 'Medium', 'Your daily digest is ready', '', ''))

    def test_a_package_id_is_never_a_notifications_title_and_a_bot_address_never_a_sender(self):
        o = self.items['android.notification#summary']
        self.assertEqual((o['app_name'], o['title'], o['body']), ('Acmeshop', '', ''))
        o = self.items['intercom.conversation#bot']
        self.assertEqual(o['from'], 'Sam Reed')  # the customer of the conversation the bot opened
        self.assertNotIn('intercom.io', json.dumps(shown(o)))
        from machine.store.message_view import sender_name
        self.assertEqual(sender_name('intercom.conversation', {'from': 'operator+x1@intercom.io', 'from_name': 'Fin'}), 'Fin')
        self.assertEqual(sender_name('intercom.conversation', {'from': 'ann@x.example', 'from_name': 'Ann Ray'}), 'Ann Ray')
        self.assertEqual(sender_name('intercom.conversation', {'from': 'ann@x.example', 'from_name': 'ann@x.example'}), 'ann@x.example')
        self.assertEqual(sender_name('gmail.message', {'from': 'GitHub <noreply@github.example>'}), 'GitHub')
        self.assertEqual(sender_name('gmail.message', {'from': 'noreply@shop.example'}), 'noreply@shop.example')  # email keeps its From
        self.assertEqual(sender_name('slack.message', {'from': 'Kit Navarro <U0KITNAVA1>'}), 'Kit Navarro')

    def test_cards_drop_a_first_line_that_repeats_the_title(self):
        self.assertTrue(self.items['trello.action']['body'].startswith('Moved to Doing'))
        self.assertTrue(self.items['stripe.event']['body'].startswith('Email:'))

    def test_docs_open_in_the_app_their_link_names(self):
        self.assertEqual(self.items['docs.comment']['app'], 'Google Docs')
        self.assertEqual(self.items['docs.shared']['app'], 'OneDrive')

    def test_a_transcript_reads_as_speaker_turns_at_times_of_day(self):
        o = self.items['meeting.transcript']
        self.assertEqual([(t['from'], t['occurred_at'][11:19]) for t in o['turns']],
                         [('Kit Navarro', '14:01:00'), ('Robin Hale', '14:01:06'), ('Kit Navarro', '14:02:30')])
        self.assertEqual(o['turns'][0]['body'], 'Morning all. Shall we start with the export fix?')  # a speaker's run, joined
        self.assertEqual(o['chat'], 'Weekly sync')
        self.assertNotIn('[0:', json.dumps(shown(o)))


# A turn written each way transcripts come: pasted, Zoom's and Teams' WebVTT, "Name (00:01):" and plain "Name: words"
TRANSCRIPTS = ['[0:00:00] Kit: Hello\n[0:00:06] Robin: Hi there', '00:00:00 Kit: Hello\n00:00:06 Robin: Hi there',
               'Kit (00:00): Hello\nRobin (00:06): Hi there', 'Kit 0:00: Hello\nRobin 0:06: Hi there',
               'WEBVTT\n\n1\n00:00:00.000 --> 00:00:04.000\nKit: Hello\n\n2\n00:00:06.000 --> 00:00:09.000\nRobin: Hi there',
               '- [00:00] Kit: Hello\n- [00:06] Robin: Hi there']


class Rows(unittest.TestCase):
    """A row in Messages (message_view.list_row, events-list.js) keeps the viewer's rules for every kind in the registry."""

    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        app, _ = fixture(cls.temp.name)  # the Graph knows some senders by name
        with app.store.connect() as db:
            cls.shown = dict(zip(SAMPLES, message_view.list_rows(db, [{**e, 'kind': k.split('#')[0]} for k, e in SAMPLES.items()])))

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def rows(self):
        return self.shown

    def test_every_kind_with_a_link_opens_it_in_the_same_way(self):
        for key, row in self.rows().items():
            url = SAMPLES[key]['metadata'].get('source_url') or ''
            self.assertEqual(row['url'], url if url.startswith('https://') else '', key)
            if row['url']:  # "Open in <app> ↗" or "Open original": never a made-up name
                self.assertIsInstance(row['app'], str, key)
                self.assertEqual(row['app'], message_view.app_of(key.split('#')[0], url), key)
        self.assertEqual(message_view.list_row('gmail.message', 'Hi', 'Hi', {'source_url': 'javascript:alert(1)'})['url'], '')

    def test_no_raw_ids_stamps_markup_or_repeats(self):
        for key, row in self.rows().items():
            for s in (row['title'], row['who'], row['text'], *(t['from'] + ' ' + t['body'] for t in row.get('turns') or ())):
                self.assertIsNone(TIMESTAMP.search(s), (key, s))
                self.assertIsNone(INTERNAL.search(s), (key, s))
                self.assertIsNone(RAW.search(s), (key, s))
                self.assertIsNone(re.search(r'\[\d{1,2}:\d{2}', s), (key, s))
                self.assertIsNone(re.search(r'\*\*|\]\(|```|<https?:|\|[^|\s]+>', s), (key, s))  # markup reads as words
            self.assertNotIn('@', row['who'].replace('@owner', ''), key)  # who by name, never an address
            if row['who']:
                self.assertFalse(message_view.words_in(row['who']) <= message_view.words_in(row['title']), (key, row))
            self.assertTrue(row['title'], key)

    def test_notifications_by_their_app_never_a_package(self):
        rows = self.rows()
        self.assertEqual((rows['android.notification']['title'], rows['android.notification']['text'], rows['android.notification']['who']),
                         ('Your daily digest is ready', '', 'Medium'))
        self.assertEqual(rows['android.notification#summary']['title'], 'Acmeshop')

    def test_mail_and_chat_senders_by_name(self):
        rows = self.rows()
        self.assertEqual(rows['gmail.message#bare']['who'], 'Avery Stone')  # stored by address, named by the Graph
        self.assertNotIn('<', rows['slack.message']['text'])

    def test_transcripts_in_every_format_read_as_turns(self):
        for body in TRANSCRIPTS:
            turns = message_view.transcript_turns(body, AT)
            self.assertEqual([(t['from'], t['body'], t['occurred_at'][11:19]) for t in turns],
                             [('Kit', 'Hello', '14:01:00'), ('Robin', 'Hi there', '14:01:06')], body)
            row = message_view.list_row('zoom.transcript', 'Weekly sync', body, {}, AT)
            self.assertEqual(row['turns'], [{'from': 'Kit', 'body': 'Hello'}, {'from': 'Robin', 'body': 'Hi there'}], body)
        # a summary that mentions a time is no transcript: it reads as written
        self.assertEqual(message_view.transcript_turns('We met at 10:30 and agreed on the plan.\nNext: send the deck by Friday to everyone.', AT), [])

    def test_a_long_meeting_keeps_each_turns_own_words_and_time(self):
        said = [(0, 'Dana', 'Shall we start with the pilot?'), (14, 'Kit', 'It has been live for two weeks.'),
                (95, 'Dana', 'How many use it every day?'), (410, 'Robin', 'IT sent the security questions.'),
                (760, 'Dana', 'We can answer those by Thursday.'), (1790, 'Kit', 'Then the second team starts on the 15th.')]
        hms = lambda s, sep='': f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}{sep}'
        formats = {'webvtt': 'WEBVTT\n\n' + '\n\n'.join(f'{i}\n{hms(s, ".000")} --> {hms(s + 4, ".000")}\n{w}: {x}' for i, (s, w, x) in enumerate(said, 1)),
                   'name (mm:ss)': '\n'.join(f'{w} ({s // 60:02d}:{s % 60:02d}): {x}' for s, w, x in said),
                   'plain': '\n'.join(f'{w}: {x}' for s, w, x in said)}
        for name, body in formats.items():
            turns = message_view.transcript_turns(body, '2026-11-10T14:00:00+00:00')
            self.assertEqual([(t['from'], t['body']) for t in turns], [(w, x) for _, w, x in said], name)
            times = [t['occurred_at'] for t in turns if not t.get('untimed')]
            if name == 'plain':  # no stamps: no times, rather than the meeting's start on every turn
                self.assertEqual(times, [], name)
            else:
                self.assertEqual(len(times), len(said), name)
                self.assertTrue(all(a < b for a, b in zip(times, times[1:])), (name, times))
                self.assertEqual(times[-1][11:19], '14:29:50', name)


if __name__ == '__main__':
    unittest.main()
