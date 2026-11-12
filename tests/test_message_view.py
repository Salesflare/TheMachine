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


if __name__ == '__main__':
    unittest.main()
