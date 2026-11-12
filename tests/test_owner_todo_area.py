"""A to-do the owner adds without an area (New to-do, no Work or Personal picked) goes where it belongs, never to the
Machine's own source: its only area, or the area its people point to; when nothing tells, it is unplaced and the review
places it by meaning (company or personal), or the message it follows up on does. A run on an unplaced one may look
for that message in every area, the mailboxes themselves too (events mailbox:true), and a move it asks for happens by
itself. Made-up data; offline: the mailbox search reads a fake mailbox and nothing is sent."""
import base64
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('owner_area_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import ms_graph  # noqa: E402

GATEWAY = {'id': 'gateway', 'service': 'gateway', 'boundary': 'owner:system'}
WORK = [{'id': 'acme-mail', 'service': 'gmail', 'transport': 'broker', 'email': 'robin@acme.example', 'boundary': 'work:Acme'},
        {'id': 'acme-calendar', 'service': 'calendar', 'transport': 'broker', 'email': 'robin@acme.example', 'boundary': 'work:Acme'}]
HOME = [{'id': 'home-mail', 'service': 'gmail', 'transport': 'broker', 'email': 'robin@home.example', 'boundary': 'personal:robin@home.example'}]


def mail(source_id, account='acme-mail', when='2026-10-12T09:00:00+00:00'):
    return {'account_id': account, 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': when, 'title': 'Pricing for the pilot',
            'body': 'Hi Sam, here is the pricing for the pilot we discussed.',
            'metadata': {'from': 'Robin <robin@acme.example>', 'to': 'Sam Lee <sam@prospect.example>', 'thread_id': 't-' + source_id, 'labels': ['SENT']},
            'deleted': False}


def raw(message_id, subject='Pricing for the pilot', when_ms=1760259600000):
    data = base64.urlsafe_b64encode(b'Hi Sam, here is the pricing for the pilot we discussed.').decode()
    return {'id': message_id, 'threadId': 'thread-' + message_id, 'labelIds': ['SENT'], 'internalDate': str(when_ms),
            'payload': {'mimeType': 'text/plain', 'body': {'data': data},
                        'headers': [{'name': 'From', 'value': 'Robin <robin@acme.example>'}, {'name': 'To', 'value': 'Sam Lee <sam@prospect.example>'},
                                    {'name': 'Subject', 'value': subject}, {'name': 'Date', 'value': 'Sun, 12 Oct 2026 09:00:00 +0000'}]}}


class Base(unittest.TestCase):
    accounts = [GATEWAY, *WORK, *HOME]

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = [dict(x) for x in self.accounts]
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': self.store.accounts, 'prepare_ahead': False, 'database': str(Path(self.temp.name) / 'e.sqlite')}
        self.store.config = self.app.config

    def new(self, **args):
        return self.app.action('card_new', {'text': 'Follow up with Sam on the pricing mail I sent', **args}, owner_dashboard=True)

    def row(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())

    def card(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            self.store.card_views(db, [row])
        return row

    def owner_event(self, made):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM events WHERE id=?', (made['event_id'],)).fetchone())

    def fill(self, sid, event_ids, **args):
        return self.app.action('suggest', {'dedupe_key': 'acme:follow-up:' + sid, 'title': 'Follow up with Sam on the pilot pricing',
                                           'body': 'You sent Sam the pricing on Oct 12. I can draft the follow-up.', 'event_ids': event_ids,
                                           'card_id': sid, **args})


class OnlyWork(Base):
    # A hosted Machine with only a work mailbox: the Machine's own source (the Gateway log) comes first in its config
    accounts = [GATEWAY, *WORK]

    def test_it_goes_to_their_only_area_not_the_machines_own_source(self):
        made = self.new()
        card = self.card(made['id'])
        self.assertEqual(json.loads(card['account_ids']), ['acme-mail'])
        self.assertEqual((card['scope'], card['area']), ('work', 'work:Acme'))
        self.assertNotIn('area_open', json.loads(self.owner_event(made)['metadata']))
        # Its run reads and sends from the Acme mailbox; there is no other area to ask for
        self.assertEqual(a.area_prompt(self.app.config, card['account_ids']), '')


class BothAreas(Base):
    def graph(self, *nodes):
        with self.store.connect() as db:
            db.executemany('INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,?,?,1,1,?)',
                           [(i, k, n, json.dumps(info)) for i, k, n, info in nodes])

    def test_the_people_on_it_point_to_its_area(self):
        self.graph(('person:sam', 'person', 'Sam Lee', {'side': 'work', 'accounts': ['acme-mail']}),
                   ('person:kai', 'person', 'Kai Rivera', {'side': 'personal', 'accounts': ['home-mail']}),
                   ('org:prospect.example', 'org', 'Prospect', {'domain': 'acme.example'}))
        for about, area in ((['person:sam'], 'work:Acme'), (['person:kai'], 'personal'), (['org:prospect.example'], 'work:Acme')):
            made = self.new(about=about)
            self.assertEqual(self.card(made['id'])['area'], area)
            self.assertNotIn('area_open', json.loads(self.owner_event(made)['metadata']))

    def test_unclear_it_is_unplaced_and_the_review_places_it_by_meaning(self):
        made = self.new()
        card = self.card(made['id'])
        self.assertEqual(json.loads(card['account_ids']), ['acme-mail'])  # their first connection with an area, never the Gateway log
        # That area is a stand-in until the review reads it: the to-do says neither Work nor Personal, and stays private
        self.assertIsNone(card['scope'])
        import team_learnings
        with self.store.connect() as db:
            self.assertEqual(team_learnings.personal_cards(db, [made['id']], self.store.accounts), {made['id']})
        event = self.owner_event(made)
        self.assertEqual(json.loads(event['metadata'])['area_open'], ['personal', 'work:Acme'])
        rule = a.review_view(event)['owner_card']['rule']
        self.assertIn('company=<work:Acme>', rule)
        self.assertIn('mailbox:true', rule)  # and to look the message up in the mailboxes when nothing collected matches
        with self.store.connect() as db:
            self.assertEqual(a.owner_area_open(db, made['id']), ['personal', 'work:Acme'])
        # The review says it is the owner's own life: Personal, with that area's accounts, and placed for good
        self.fill(made['id'], [made['event_id']], personal=True)
        card = self.card(made['id'])
        self.assertEqual((json.loads(card['account_ids']), self.row(made['id'])['area'], card['scope']), (['home-mail'], 'personal', 'personal'))
        with self.store.connect() as db:
            self.assertEqual(a.owner_area_open(db, made['id']), [])

    def test_placed_by_the_review_as_work_it_says_work(self):
        made = self.new()
        self.fill(made['id'], [made['event_id']], company='work:Acme')
        self.assertEqual(self.card(made['id'])['scope'], 'work')
        import team_learnings
        with self.store.connect() as db:
            self.assertEqual(team_learnings.personal_cards(db, [made['id']], self.store.accounts), set())

    def test_the_mail_it_follows_up_on_places_it(self):
        made = self.new(scope=None)
        # put it on the Personal side first, as a config with the personal mailbox first would
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET account_ids=? WHERE id=?', ('["home-mail"]', made['id']))
        self.store.commit_page('acme-mail', {}, [mail('old-1')])
        found = next(e['id'] for e in self.app.action('events', {'account_ids': ['all'], 'query': 'pricing'})['events'] if e['kind'] == 'gmail.message')
        self.fill(made['id'], [found, made['event_id']])
        card = self.card(made['id'])
        self.assertEqual((json.loads(card['account_ids']), self.row(made['id'])['area'], card['scope']), (['acme-mail', 'acme-calendar'], 'work:Acme', 'work'))
        self.assertEqual(card['origin'], 'owner')

    def test_an_area_the_owner_picked_is_not_reopened(self):
        made = self.new(scope='personal')
        self.assertNotIn('area_open', json.loads(self.owner_event(made)['metadata']))
        with self.store.connect() as db:
            self.assertEqual(a.owner_area_open(db, made['id']), [])

    def test_its_words_place_it_a_company_or_a_mailbox_they_name(self):
        for text, area in (('Search the Acme inbox for the pilot mail', 'work:Acme'),
                           ('Find what robin@acme.example sent Sam', 'work:Acme'),
                           ('Ask jo@acme.example about the pilot', 'work:Acme'),  # a colleague at the company's domain
                           ('Reply from robin@home.example to the landlord', 'personal')):
            made = self.new(text=text)
            self.assertEqual(self.card(made['id'])['area'], area, text)
            self.assertNotIn('area_open', json.loads(self.owner_event(made)['metadata']))
        # a free mail address, a company named inside a word or an address, or two areas at once: no guess
        for text in ('Write sam@gmail.com back', 'Check the Acmeville order', 'Mail robin@acme.example and robin@home.example'):
            made = self.new(text=text)
            self.assertIn('area_open', json.loads(self.owner_event(made)['metadata']), text)

    def test_a_person_it_names_by_address_places_it(self):
        self.graph(('person:kai', 'person', 'Kai Rivera', {'side': 'personal', 'emails': ['kai@mail.example'], 'accounts': ['home-mail']}))
        made = self.new(text='Send Kai@mail.example the photos')
        self.assertEqual(self.card(made['id'])['area'], 'personal')

    def test_unclear_it_starts_in_their_most_used_area_still_open(self):
        for _ in range(3):
            self.new(scope='personal')
        self.new(scope='work')
        made = self.new()
        self.assertEqual(json.loads(self.card(made['id'])['account_ids']), ['home-mail'])  # most of theirs are Personal
        self.assertEqual(json.loads(self.owner_event(made)['metadata'])['area_open'], ['personal', 'work:Acme'])  # the review still places it
        self.assertIsNone(a.todo_areas.most_used([('["home-mail"]', None), ('["acme-mail"]', None)], self.accounts))  # a tie: no pick

    def blocked(self, sid, move_to):
        self.store.decide(sid, 'accept', '', 'click-' + sid, 'dashboard')
        self.app.preparation_step(lambda req: {'status': 'admitted'})
        with self.store.connect() as db:
            job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (sid,)).fetchone()['job_id']
        return self.store.preparation_blocked(sid, job, 'The pricing mail is in the Acme mailbox.', move_to=move_to)

    def test_a_run_on_an_unplaced_to_do_moves_it_itself_and_carries_on(self):
        made = self.new()
        with self.store.connect() as db:  # it started on the Personal side
            db.execute('UPDATE suggestions SET account_ids=? WHERE id=?', ('["home-mail"]', made['id']))
        card = self.card(made['id'])
        prompt = a.area_prompt(self.app.config, card['account_ids'], unplaced=True)
        self.assertIn('moves there by itself', prompt)
        self.assertIn('mailbox:true', prompt)
        said = self.blocked(made['id'], 'work:Acme')
        self.assertEqual((said['status'], said['area'], said['resumed']), ('moved', 'work:Acme', True))
        card = self.card(made['id'])
        self.assertEqual((json.loads(card['account_ids']), card['area'], card['preparation_status']), (['acme-mail', 'acme-calendar'], 'work:Acme', 'queued'))
        with self.store.connect() as db:
            owner, _ = self.app.card_chat_service(db, made['id'])
        moved = [i for i in owner if i.get('text') == 'Moved to Work']
        self.assertEqual([i.get('mine') for i in moved], [False])  # it moved itself, a line of its own, no "You"

    def test_a_placed_to_do_still_asks_for_the_move(self):
        made = self.new(scope='personal')
        said = self.blocked(made['id'], 'work:Acme')
        self.assertEqual(said['status'], 'blocked')
        card = self.card(made['id'])
        self.assertEqual((self.row(made['id'])['area'], card['preparation_move_to']), (None, 'work:Acme'))  # the one-tap move on the to-do


class MailboxSearch(Base):
    def fake(self, listed, store):
        def get(source, resource, params=None):
            store.append((source.account['id'], resource, dict(params or {})))
            if resource == 'profile':
                return {'emailAddress': source.account['email'], 'historyId': '1'}
            if resource == 'messages':
                return {'messages': [{'id': i} for i in listed]}
            return raw(resource.split('/')[1])
        return get

    def test_older_mail_is_found_in_the_mailbox_and_kept_as_reviewed_context(self):
        calls = []
        with patch.object(a.Gmail, 'get', autospec=True, side_effect=self.fake(['m-old'], calls)):
            found = self.app.action('events', {'account_ids': ['acme-mail', 'acme-calendar', 'gateway'], 'mailbox': True,
                                               'query': 'to:sam@prospect.example subject:pricing in:sent'})
        self.assertEqual(calls[1], ('acme-mail', 'messages', {'q': 'to:sam@prospect.example subject:pricing in:sent', 'maxResults': 5}))
        self.assertEqual({c[0] for c in calls}, {'acme-mail'})  # only mail accounts among those asked for
        self.assertEqual([e['title'] for e in found['events']], ['Pricing for the pilot'])
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM events WHERE source_id=?', ('m-old',)).fetchone())
            self.assertIsNone(db.execute('SELECT 1 FROM checkpoints WHERE account_id=?', ('acme-mail',)).fetchone())  # no cursor moved
        self.assertEqual((row['account_id'], row['analyzed_version'], row['version']), ('acme-mail', 1, 1))  # context, never a review signal
        # The same search again keeps one copy
        with patch.object(a.Gmail, 'get', autospec=True, side_effect=self.fake(['m-old'], [])):
            again = self.app.action('events', {'account_ids': ['acme-mail'], 'mailbox': True, 'query': 'pricing'})
        self.assertEqual([e['id'] for e in again['events']], [row['id']])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE source_id='m-old'").fetchone()[0], 1)

    def test_a_mailbox_that_fails_says_so_and_a_shared_one_is_never_searched(self):
        self.store.accounts.append({'id': 'team-mail', 'service': 'gmail', 'transport': 'broker', 'email': 'team@acme.example',
                                    'boundary': 'work:Acme', 'shared': True})
        def get(source, resource, params=None):
            raise a.SourceError('google_signin_expired', 401)
        with patch.object(a.Gmail, 'get', autospec=True, side_effect=get) as called:
            found = self.app.action('events', {'account_ids': ['all'], 'mailbox': True, 'query': 'pricing'})
        self.assertEqual(found['mailbox_errors'], {'acme-mail': 'google_signin_expired', 'home-mail': 'google_signin_expired'})
        self.assertNotIn('team-mail', {c.args[0].account['id'] for c in called.call_args_list})
        self.assertEqual(found['events'], [])
        with self.assertRaisesRegex(ValueError, 'query'):
            self.app.action('events', {'account_ids': ['all'], 'mailbox': True, 'query': ' '})

    def test_outlook_searches_with_graphs_own_search(self):
        seen = []
        with patch.object(ms_graph, 'call', side_effect=lambda *args, **kw: seen.append(args[4]) or {'value': [{'id': 'x1', 'conversationId': 'c1'}]}):
            out = ms_graph.gmail_call({}, None, {'id': 'o'}, 'gmail.users.messages.list', {'q': 'from:sam subject:"pilot pricing" in:sent', 'maxResults': 5})
        self.assertEqual(seen, [{'$search': '"from:sam subject: pilot pricing"', '$select': 'id,conversationId', '$top': 5}])
        self.assertEqual(out['messages'], [{'id': 'x1', 'threadId': 'c1'}])


if __name__ == '__main__':
    unittest.main()
