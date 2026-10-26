"""Bulk mail and the review: promotions, list mail, updates and forums reach the review as a compact title line (sender,
subject, a short snippet), many per turn, so the model still judges each and any can become a card; nothing is skipped
on its headers alone. A person writing stays out of the bulk rules. Made-up mail only; nothing is sent, no Gateway, no
model."""
import base64, datetime as dt, email.message, importlib.util, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('bulk_mail_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
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

    def test_bulk_mail_reaches_the_review_as_a_title_line_with_a_snippet(self):
        rows = self.ingest(raw('promo', 'Shop <deals@shop.example>', 'Autumn sale', labels=['CATEGORY_PROMOTIONS', 'INBOX'], body='Forty percent off ' * 100),
                           raw('digest', 'Weekly <newsletter@digest.example>', 'This week', headers=[UNSUB]),
                           raw('junk', 'Someone <someone@list.example>', 'Offer', headers=[('Precedence', 'junk')]),
                           raw('update', 'Tracker <updates@tracker.example>', 'Your weekly report', labels=['CATEGORY_UPDATES']),
                           raw('forum', 'Ann <ann@example.org>', 'Group: meetup notes', labels=['CATEGORY_FORUMS'], headers=[('List-Id', '<group.example>')]),
                           raw('ask', 'Sam <sam@example.org>', 'Can we meet?', labels=['CATEGORY_PERSONAL', 'INBOX']))
        self.assertTrue(all(r['analyzed_version'] < r['version'] for r in rows.values()))  # nothing skipped on headers alone
        views = self.reviewed()
        self.assertEqual(set(views), set(rows))
        for name in ('promo', 'digest', 'junk', 'update', 'forum'):
            view = views[name]
            self.assertTrue(view['title_only'])
            self.assertNotIn('body', view)
            self.assertIn('@', view['from'])
            self.assertLessEqual(len(view['snippet']), a.BRIEF_SNIPPET_CHARS + 1)  # with the ellipsis
            self.assertEqual({'id', 'account_id', 'source_id', 'version', 'occurred_at', 'title'} - set(view), set())
        self.assertTrue(views['promo']['snippet'].startswith('Forty percent off'))
        self.assertGreater(len(views['ask']['body']), 1000)
        # The whole signal stays readable through the events tool
        full = a.event_page([r for r in self.store.events(['work'], limit=10) if r['source_id'] == 'update'])
        self.assertGreater(len(full['events'][0]['body']), 1000)

    def test_a_notice_that_matters_sent_as_bulk_mail_is_judged_and_can_become_a_card(self):
        app = object.__new__(a.App); app.store = self.store
        app.config = {'accounts': [WORK], 'review_worker': {'enabled': False}}
        rows = self.ingest(raw('notice', 'Builder <noreply@pages.example>', 'Important: unusual sign-in to your account',
                               labels=['CATEGORY_PROMOTIONS'], headers=[UNSUB, ('Precedence', 'bulk')],
                               body='We noticed a sign-in from a new device. If this was not you, reset your password. ' * 10))
        view = self.reviewed()['notice']
        self.assertTrue(view['title_only'])
        self.assertIn('new device', view['snippet'])
        card = app.action('suggest', {'dedupe_key': 'notice', 'title': 'Check the new sign-in', 'body': 'Confirm it was you.',
                                      'event_ids': [rows['notice']['id']], 'when': 'now'})
        self.assertTrue(card.get('id'))

    def test_many_title_lines_fit_in_one_turn(self):
        self.ingest(*[raw(f'promo{n}', 'Shop <deals@shop.example>', f'Sale {n}', labels=['CATEGORY_PROMOTIONS']) for n in range(40)],
                    raw('ask', 'Sam <sam@example.org>', 'Can we meet?', labels=['INBOX']))
        claim = self.store.begin_analysis(['work'], 20)
        self.assertEqual(claim['claimed'], 41)  # a title line counts a quarter of a signal: 1 + 40/4 = 11 of 20
        self.assertEqual(claim['pages'], 1)
        with self.store.connect() as db:
            items = json.loads(db.execute('SELECT items FROM analyses').fetchone()[0])
        self.assertEqual(a.claim_weight(items), 11)

    def test_a_person_writing_stays_out_of_the_bulk_rules(self):
        reply = ('In-Reply-To', '<root@group.example>')
        # A person's reply on a mailing list, filed in Forums: a title line the review can open
        list_reply = raw('list-reply', 'Ann <ann@example.org>', 'Re: meetup', labels=['CATEGORY_FORUMS'], headers=[UNSUB, reply, ('Precedence', 'list')])
        # A system sender's reply in a thread the owner wrote in: a full look
        own = raw('own', 'Owner <owner@example.com>', 'Help with my order', labels=['SENT'], thread='t1')
        ticket = raw('ticket', 'Helpdesk <support@vendor.example>', 'Re: Help with my order', labels=['CATEGORY_UPDATES'], headers=[UNSUB, reply], thread='t1')
        # Newsletter-looking mail in Primary from a person, and a reply in Primary: a full look
        primary = raw('primary', 'Cy <cy@example.org>', 'My monthly letter', labels=['CATEGORY_PERSONAL', 'INBOX'], headers=[UNSUB])
        answer = raw('answer', 'Desk <support@desk.example>', 'Re: your request', labels=['INBOX'], headers=[UNSUB, reply])
        self.ingest(list_reply, own, ticket, primary, answer)
        views = self.reviewed()
        self.assertTrue(views['list-reply'].get('title_only'))
        for name in ('ticket', 'primary', 'answer', 'own'):
            self.assertIn('body', views[name], name)

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
        self.assertEqual(a.bulk_kind(event['kind'], event['metadata'], event['title']), 'update')  # Other: a title line
        focused = {**event['metadata'], 'labels': ms_graph.labels({**meta, 'inferenceClassification': 'focused'}, known)}
        person = {**focused, 'from': 'Ann <ann@example.org>'}
        self.assertIsNone(a.bulk_kind('gmail.message', person, 'Team lunch'))  # Focused counts as Primary: a person gets a full look
        self.assertEqual(a.bulk_kind('gmail.message', {**focused, 'from': 'News <noreply@brand.example>'}, event['title']), 'bulk')  # list mail from a system sender


if __name__ == '__main__':
    unittest.main()
