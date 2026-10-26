"""Bulk mail and the review: promotions and list mail from a system sender are marked reviewed without a model call,
updates and forum mail reach the review as a title line, and bills, security alerts and Stripe always get a full look.
A person writing stays out of the bulk rules. Made-up mail only; nothing is sent, no Gateway, no model."""
import base64, datetime as dt, email.message, importlib.util, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('bulk_mail_assistant', Path(__file__).with_name('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
ms_graph = a.ms_graph
WORK = {'id': 'work', 'service': 'gmail', 'email': 'owner@example.com'}


def raw(source, sender, subject='Hello', labels=(), headers=(), body='Some text ' * 300, thread=None):
    """A Gmail message in the API's "full" shape."""
    heads = [{'name': 'From', 'value': sender}, {'name': 'To', 'value': 'owner@example.com'}, {'name': 'Subject', 'value': subject},
             *({'name': k, 'value': v} for k, v in headers)]
    return {'id': source, 'threadId': thread or source, 'labelIds': list(labels), 'internalDate': str(int(dt.datetime.now().timestamp() * 1000) - 3600000),
            'snippet': '', 'payload': {'headers': heads, 'mimeType': 'text/plain',
                                       'body': {'data': base64.urlsafe_b64encode(body.encode()).decode()}}}


UNSUB = ('List-Unsubscribe', '<https://shop.example/unsubscribe?u=abc123>, <mailto:leave@shop.example>')


class BulkMail(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')

    def ingest(self, *messages):
        self.store.commit_page('work', {'history_id': '1'}, [a.message_event(WORK, m) for m in messages])
        with self.store.connect() as db:
            return {r['source_id']: dict(r) for r in db.execute('SELECT * FROM events')}

    def reviewed(self):
        """What a review is shown: the views of every page of its claim."""
        claim = self.store.begin_analysis(['work'], 40)
        views = list(claim['events'])
        for page in range(1, claim.get('pages', 1)):
            views += self.store.analysis_page(claim['analysis_id'], page)['events']
        with self.store.connect() as db:
            names = {i: s for i, s in db.execute('SELECT id,source_id FROM events')}
        return {names[v['id']]: v for v in views}

    def test_headers_are_kept_as_presence_never_the_link(self):
        event = a.message_event(WORK, raw('n', 'Shop <news@shop.example>', headers=[UNSUB, ('List-Id', 'Shop news <news.shop.example>'), ('Precedence', 'Bulk')]))
        m = event['metadata']
        self.assertEqual((m['list_unsubscribe'], m['list_id'], m['precedence']), (True, 'Shop news <news.shop.example>', 'bulk'))
        self.assertNotIn('unsubscribe?u=', json.dumps(event))
        self.assertNotIn('leave@shop.example', json.dumps(event))
        plain = a.message_event(WORK, raw('p', 'Sam <sam@example.org>'))['metadata']
        self.assertFalse({'list_unsubscribe', 'list_id', 'precedence'} & set(plain))

    def test_promotions_and_bulk_are_marked_reviewed_without_a_model_call(self):
        rows = self.ingest(raw('promo', 'Shop <deals@shop.example>', 'Autumn sale', labels=['CATEGORY_PROMOTIONS', 'INBOX']),
                           raw('digest', 'Weekly <newsletter@digest.example>', 'This week', labels=['CATEGORY_UPDATES'], headers=[UNSUB]),
                           raw('junk', 'Someone <someone@list.example>', 'Offer', labels=['CATEGORY_UPDATES'], headers=[('Precedence', 'junk')]),
                           raw('ask', 'Sam <sam@example.org>', 'Can we meet?', labels=['CATEGORY_PERSONAL', 'INBOX']))
        self.assertEqual({k: (r['auto_reviewed'], r['analyzed_version'] == r['version']) for k, r in rows.items()},
                         {'promo': ('promo', True), 'digest': ('bulk', True), 'junk': ('bulk', True), 'ask': (None, False)})
        self.assertEqual(set(self.reviewed()), {'ask'})
        self.assertEqual(self.store.unmark_bulk([rows['promo']['id']]), 1)  # undone: waits for the next review again
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT auto_reviewed,analyzed_version<version FROM events WHERE id=?', (rows['promo']['id'],)).fetchone()[:], (None, 1))

    def test_updates_and_forums_reach_the_review_as_a_title_line(self):
        self.ingest(raw('update', 'Tracker <updates@tracker.example>', 'Your weekly report', labels=['CATEGORY_UPDATES']),
                    raw('forum', 'Ann <ann@example.org>', 'Group: meetup notes', labels=['CATEGORY_FORUMS'], headers=[('List-Id', '<group.example>')]),
                    raw('ask', 'Sam <sam@example.org>', 'Can we meet?', labels=['INBOX']))
        views = self.reviewed()
        for name in ('update', 'forum'):
            view = views[name]
            self.assertTrue(view['title_only'])
            self.assertNotIn('body', view)
            self.assertIn('@', view['from'])
            self.assertEqual({'id', 'account_id', 'source_id', 'version', 'occurred_at', 'title'} - set(view), set())
        self.assertGreater(len(views['ask']['body']), 1000)
        # The whole signal stays readable through the events tool
        full = a.event_page([r for r in self.store.events(['work'], limit=10) if r['source_id'] == 'update'])
        self.assertGreater(len(full['events'][0]['body']), 1000)

    def test_bills_security_alerts_and_stripe_get_a_full_look(self):
        cases = [raw('bill', 'Power Co <noreply@power.example>', 'Your October bill is ready', labels=['CATEGORY_UPDATES'], headers=[UNSUB]),
                 raw('invoice', 'Tools <billing@tools.example>', 'Invoice INV-104 for your plan', labels=['CATEGORY_PROMOTIONS'], headers=[UNSUB]),
                 raw('due', 'Lease <hello@lease.example>', 'Payment due on Friday', labels=['CATEGORY_UPDATES'], headers=[('Precedence', 'bulk')]),
                 raw('signin', 'Accounts <no-reply@accounts.example>', 'Security alert: new sign-in on Linux', labels=['CATEGORY_UPDATES'], headers=[UNSUB]),
                 raw('reset', 'App <noreply@app.example>', 'Reset your password', labels=['CATEGORY_UPDATES']),
                 raw('payout', 'Stripe <notifications@stripe.com>', 'Your weekly summary', labels=['CATEGORY_UPDATES'], headers=[UNSUB]),
                 raw('dispute', 'Stripe <support@mail.stripe.com>', 'A dispute was opened', labels=['CATEGORY_PROMOTIONS'])]
        rows = self.ingest(*cases)
        self.assertTrue(all(r['auto_reviewed'] is None and r['analyzed_version'] < r['version'] for r in rows.values()))
        views = self.reviewed()
        self.assertEqual(set(views), set(rows))
        self.assertFalse([k for k, v in views.items() if v.get('title_only') or 'body' not in v])
        self.assertFalse(a.bulk_kind('gmail.message', {'from': 'Shop <deals@shop.example>', 'labels': ['CATEGORY_PROMOTIONS']}, 'Last day: 40% off') is None)

    def test_a_person_writing_stays_out_of_the_bulk_rules(self):
        reply = ('In-Reply-To', '<root@group.example>')
        # A person's reply on a mailing list: never marked; in Forums it is a title line the review can open
        list_reply = raw('list-reply', 'Ann <ann@example.org>', 'Re: meetup', labels=['CATEGORY_FORUMS'], headers=[UNSUB, reply, ('Precedence', 'list')])
        # A list reply filed as a promotion still reaches the review
        promo_reply = raw('promo-reply', 'Bo <bo@example.org>', 'Re: your question', labels=['CATEGORY_PROMOTIONS'], headers=[UNSUB, reply])
        # A system sender's reply in a thread the owner wrote in: a full look
        own = raw('own', 'Owner <owner@example.com>', 'Help with my order', labels=['SENT'], thread='t1')
        ticket = raw('ticket', 'Helpdesk <support@vendor.example>', 'Re: Help with my order', labels=['CATEGORY_UPDATES'], headers=[UNSUB, reply], thread='t1')
        # Newsletter-looking mail in Primary from a person: a full look
        primary = raw('primary', 'Cy <cy@example.org>', 'My monthly letter', labels=['CATEGORY_PERSONAL', 'INBOX'], headers=[UNSUB])
        # A helpdesk's reply with a list header, the owner's question not in this mailbox: never marked either
        helpdesk = raw('helpdesk', 'Desk <support@desk.example>', 'Re: your request', labels=['CATEGORY_UPDATES'], headers=[UNSUB, reply])
        rows = self.ingest(list_reply, promo_reply, own, ticket, primary, helpdesk)
        self.assertEqual({k: r['auto_reviewed'] for k, r in rows.items()}, dict.fromkeys(rows))
        views = self.reviewed()
        self.assertTrue(views['list-reply'].get('title_only'))
        self.assertTrue(views['promo-reply'].get('title_only'))
        self.assertIn('body', views['ticket'])
        self.assertIn('body', views['primary'])
        self.assertTrue(views['helpdesk'].get('title_only'))

    def test_stored_mail_waiting_for_a_review_is_marked_once_on_upgrade(self):
        rows = self.ingest(raw('promo', 'Shop <deals@shop.example>', 'Sale', labels=['CATEGORY_PROMOTIONS']),
                           raw('ask', 'Sam <sam@example.org>', 'Question', labels=['INBOX']))
        with self.store.connect() as db:  # as stored before this change: nothing marked, no column
            db.execute('UPDATE events SET analyzed_version=0')
            db.execute('ALTER TABLE events DROP COLUMN auto_reviewed')
        store = a.Store(self.store.path)
        with store.connect() as db:
            self.assertEqual({r['source_id']: r['auto_reviewed'] for r in db.execute('SELECT source_id,auto_reviewed FROM events')},
                             {'promo': 'promo', 'ask': None})
            self.assertEqual(db.execute('SELECT count(*) FROM events WHERE analyzed_version<version').fetchone()[0], 1)

    def test_microsoft_other_and_list_mail(self):
        mime = email.message.EmailMessage()
        mime['From'], mime['To'], mime['Subject'] = 'News <newsletter@brand.example>', 'owner@example.com', 'Our news'
        mime['List-Unsubscribe'] = '<https://brand.example/u/xyz>'
        mime.set_content('Hello ' * 300)
        meta = {'id': 'm1', 'conversationId': 'c1', 'parentFolderId': 'inbox-id', 'isRead': False, 'receivedDateTime': '2026-10-20T08:00:00Z',
                'bodyPreview': 'Hello', 'webLink': 'https://outlook.office.com/mail/m1', 'inferenceClassification': 'other'}
        known = {'inbox': 'inbox-id', 'sentitems': 'sent-id'}
        message = {'id': 'm1', 'threadId': 'c1', 'labelIds': ms_graph.labels(meta, known), 'internalDate': '1792483200000', 'snippet': 'Hello',
                   'webLink': meta['webLink'], 'payload': ms_graph.payload(mime.as_bytes())}
        outlook = {**WORK, 'service': 'outlook'}
        event = a.message_event(outlook, message)
        self.assertEqual(event['metadata']['list_unsubscribe'], True)
        self.assertNotIn('brand.example/u/', json.dumps(event))
        self.assertEqual(a.bulk_kind(event['kind'], event['metadata'], event['title']), 'bulk')  # Other, with a list header, from a system sender
        focused = {**event['metadata'], 'labels': ms_graph.labels({**meta, 'inferenceClassification': 'focused'}, known)}
        self.assertIsNone(a.bulk_kind('gmail.message', focused, event['title']))  # Focused counts as Primary
        other = {**event['metadata'], 'from': 'Ann <ann@example.org>', 'list_unsubscribe': False}
        self.assertEqual(a.bulk_kind('gmail.message', other, 'Team lunch'), 'update')  # Other from a person: a title line

    def test_first_look_counts_leave_marked_mail_out(self):
        app = object.__new__(a.App); app.store = self.store
        app.config = {'accounts': [{'id': 'gateway', 'service': 'gateway'}, WORK], 'review_worker': {'enabled': False}}
        self.ingest(*[raw(f'promo{n}', 'Shop <deals@shop.example>', 'Sale', labels=['CATEGORY_PROMOTIONS']) for n in range(30)],
                    *[raw(f'digest{n}', 'Weekly <newsletter@digest.example>', 'Digest', labels=['CATEGORY_UPDATES'], headers=[UNSUB]) for n in range(10)],
                    raw('ask', 'Sam <sam@example.org>', 'Can we meet?', labels=['INBOX']))
        with patch.object(a, 'has_model', return_value=True), self.store.connect() as db:
            state = app.first_look(db)
            pending = db.execute('SELECT count(*) FROM events WHERE analyzed_version<version').fetchone()[0]
        self.assertEqual(pending, 1)
        self.assertEqual(state['waiting'], 1)


if __name__ == '__main__':
    unittest.main()
