"""Intercom to-dos close by themselves only once Intercom shows for certain that the team handled them. Made-up data,
no live calls.

Handled: someone on the team (the owner or a teammate, an admin) closed the conversation after the to-do was made, or
replied to the customer after it and the customer hasn't written since, when a reply is all the to-do asks. Never: the
customer wrote again, a note, a snooze, an assignment, a bot or Fin, or a to-do that asks for more than a reply."""
import importlib.util
import json
import tempfile
import time
import types
import unittest
from pathlib import Path

from connectors import intercom

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('handled_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

OWN = {'id': 'ic', 'service': 'intercom', 'transport': 'api', 'workspace_id': 'ws1', 'admin_id': '42', 'region': 'us',
       'email': 'owner@example.com'}
HELPERS = types.SimpleNamespace(SourceError=a.SourceError, iso=a.CONNECTOR_HELPERS.iso)
T = int(time.time()) + 600  # after the to-do is made
CUSTOMER = {'type': 'user', 'id': 'u1', 'email': 'customer@example.com', 'name': 'Casey'}
REPLY = {'kind': 'intercom', 'account_id': 'ic', 'conversation_id': '7', 'body': 'Yes, under Settings, Export.'}


def conversation(*parts, state='open', created=100):
    parts = list(parts)
    return {'id': '7', 'updated_at': max([p['created_at'] for p in parts] or [created]), 'created_at': created, 'title': 'Export question',
            'state': state, 'open': state == 'open', 'admin_assignee_id': None, 'team_assignee_id': None,
            'source': {'body': '<p>Can I export?</p>', 'author': CUSTOMER},
            'conversation_parts': {'conversation_parts': parts, 'total_count': len(parts)}}


def part(kind, at, author, body='<p>Done</p>', **extra):
    return {'id': f'{kind}{at}', 'created_at': at, 'part_type': kind, 'body': body, 'author': author, **extra}


def admin(aid='51', name='Sam Lee'):
    return {'type': 'admin', 'id': aid, 'name': name, 'email': f'{aid}@example.com'}


OWNER = admin('42', 'Owner')
BOT = {'type': 'bot', 'id': '9', 'name': 'Fin'}


class Facts(unittest.TestCase):
    def facts(self, raw):
        m = intercom.event(OWN, raw, HELPERS)['metadata']
        return {k: m[k] for k in ('team_closed', 'team_reply', 'customer_at')}

    def test_only_people_on_the_team_count(self):
        f = self.facts(conversation(part('comment', T, admin()), part('note', T + 5, admin('52')), part('comment', T + 9, BOT),
                                    part('comment', T + 10, admin('53'), from_ai_agent=True)))
        self.assertEqual(f['team_reply'], {'at': T, 'admin_id': '51', 'name': 'Sam Lee'})
        self.assertEqual((f['team_closed'], f['customer_at']), (None, 100))
        f = self.facts(conversation(part('comment', T, admin()), part('comment', T + 5, CUSTOMER), part('close', T + 9, BOT, body=None), state='closed'))
        self.assertEqual((f['team_closed'], f['customer_at']), (None, T + 5))  # a bot closing it: not the team
        f = self.facts(conversation(part('close', T, admin(), body=None), state='closed'))
        self.assertEqual(f['team_closed'], {'at': T, 'admin_id': '51', 'name': 'Sam Lee'})

    def test_parts_cut_off_tell_nothing(self):
        raw = conversation(part('comment', T, admin()), part('close', T + 1, admin()), state='closed')
        raw['conversation_parts']['total_count'] = 900
        self.assertEqual(self.facts(raw), {'team_closed': None, 'team_reply': None, 'customer_at': 100})


class Store(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = [OWN, {'id': 'mail', 'service': 'gmail', 'email': 'owner@example.com'}]
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': self.store.accounts, 'database': str(Path(self.temp.name) / 'events.sqlite'),
                           'openclaw_config': str(Path(self.temp.name) / 'openclaw.json')}
        self.sync(conversation())
        self.sid = self.store.suggest('c7', 'Answer Casey about export', 'Casey asks whether they can export.', [1])['id']
        self.step(REPLY)

    def sync(self, raw):
        self.store.commit_page('ic', {}, [intercom.event(OWN, raw, HELPERS)])

    def step(self, *steps, done_when=None):
        value = steps[0] if len(steps) == 1 else {'kind': 'menu', 'actions': list(steps)}
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET next_action=?,done_when=? WHERE id=?', (json.dumps(value), done_when, self.sid))

    def status(self):
        with self.store.connect() as db:
            return db.execute('SELECT status FROM suggestions WHERE id=?', (self.sid,)).fetchone()[0]

    def lines(self):
        with self.store.connect() as db:
            return [i['text'] for i in self.app.card_chat_service(db, self.sid)[0] if i['kind'] == 'event']

    def stays(self, raw):
        self.sync(raw)
        self.assertEqual(self.store.close_handled_intercom(), [])
        self.assertEqual(self.status(), 'pending')

    def test_closed_by_a_teammate_closes_it_with_their_name_and_undo_once(self):
        self.sync(conversation(part('comment', T, admin()), part('close', T + 1, admin(), body=None), state='closed'))
        self.assertEqual(self.store.close_handled_intercom(), [self.sid])
        self.assertEqual(self.store.close_handled_intercom(), [])
        self.assertEqual(self.status(), 'completed')
        self.assertEqual(self.lines(), ['Closed in Intercom by Sam Lee'])
        self.assertFalse(any(line.startswith('You') for line in self.lines()))
        self.assertEqual(self.store.decide(self.sid, 'undo', '', 'u1', 'dashboard')['status'], 'pending')
        self.assertEqual(self.store.close_handled_intercom(), [])  # the same close never closes it again
        self.assertEqual(self.status(), 'pending')
        # Reopened and closed again later: that is new, it closes again
        self.sync(conversation(part('close', T + 1, admin(), body=None), part('open', T + 50, CUSTOMER),
                               part('close', T + 90, admin(), body=None), state='closed'))
        self.assertEqual(self.store.close_handled_intercom(), [self.sid])

    def test_closed_by_the_owner_reads_plainly(self):
        self.sync(conversation(part('close', T, OWNER, body=None), state='closed'))
        self.assertEqual(self.store.close_handled_intercom(), [self.sid])
        self.assertEqual(self.lines(), ['Closed in Intercom'])

    def test_closed_even_when_the_to_do_asks_for_more(self):
        self.step({'kind': 'finish', 'label': 'Send quote'})
        self.sync(conversation(part('close', T, admin(), body=None), state='closed'))
        self.assertEqual(self.store.close_handled_intercom(), [self.sid])

    def test_a_teammates_reply_answers_a_reply_to_do(self):
        self.sync(conversation(part('comment', T, admin()), part('note', T + 5, admin('52'))))
        self.assertEqual(self.store.close_handled_intercom(), [self.sid])
        self.assertEqual(self.lines(), ['Answered in Intercom by Sam Lee'])

    def test_a_reply_by_mail_to_the_customer_counts_as_a_reply(self):
        self.step({'kind': 'email', 'account_id': 'mail', 'to': ['customer@example.com'], 'subject': 'Export', 'body': 'Yes.'})
        self.sync(conversation(part('comment', T, OWNER)))
        self.assertEqual(self.store.close_handled_intercom(), [self.sid])
        self.assertEqual(self.lines(), ['Answered in Intercom'])

    def test_the_customer_wrote_again(self):
        self.stays(conversation(part('comment', T, admin()), part('comment', T + 5, CUSTOMER)))

    def test_a_note_a_snooze_or_an_assignment_alone(self):
        self.stays(conversation(part('note', T, admin())))
        self.stays(conversation(part('snoozed', T, admin(), body=None), state='snoozed'))
        raw = conversation(part('assignment', T, admin(), body=None))
        raw['admin_assignee_id'] = '42'
        self.stays(raw)

    def test_a_bot_fin_or_automatic_message(self):
        self.stays(conversation(part('comment', T, BOT)))
        self.stays(conversation(part('comment', T, admin(), is_ai_answer=True)))
        self.stays(conversation(part('close', T, BOT, body=None), state='closed'))

    def made_now(self):
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET created_at=? WHERE id=?', (a.now(), self.sid))

    def test_before_the_to_do_was_made(self):
        # Read in before the to-do was made: the review that made it saw them, so they never close it
        for raw in (conversation(part('comment', 200, admin())), conversation(part('close', 200, admin(), body=None), state='closed')):
            self.sync(raw)
            self.made_now()
            self.stays(raw)
        # Something else changing later (a note) keeps the reply as seen before the to-do
        replied = conversation(part('comment', 200, admin()))
        self.sync(replied)
        self.made_now()
        self.stays(conversation(part('comment', 200, admin()), part('note', 300, admin('52'))))

    def test_a_reply_sent_before_the_to_do_but_read_in_after_it_answers_it(self):
        # The owner answered in Intercom while the review ran; the next sync brought it in after the to-do was made
        sent = int(time.time()) - 360
        self.sync(conversation(part('comment', sent, OWNER)))
        self.assertEqual(self.store.close_handled_intercom(), [self.sid])
        self.assertEqual(self.lines(), ['Answered in Intercom'])

    def test_a_close_read_in_after_the_to_do_closes_it(self):
        self.sync(conversation(part('close', int(time.time()) - 360, admin(), body=None), state='closed'))
        self.assertEqual(self.store.close_handled_intercom(), [self.sid])
        self.assertEqual(self.lines(), ['Closed in Intercom by Sam Lee'])

    def test_a_reply_read_in_late_still_needs_the_customer_quiet_and_a_reply_only_to_do(self):
        sent = int(time.time()) - 360
        self.stays(conversation(part('comment', sent, OWNER), part('comment', sent + 5, CUSTOMER)))
        self.step({'kind': 'finish', 'label': 'Send quote'})
        self.stays(conversation(part('comment', sent, OWNER)))

    def test_a_reply_kept_before_stamps_existed_never_counts_as_unseen(self):
        replied = conversation(part('comment', 200, admin()))
        self.sync(replied)
        with self.store.connect() as db:
            old = json.loads(db.execute('SELECT metadata FROM events WHERE id=1').fetchone()[0])
            old['team_reply'].pop('seen')
            db.execute('UPDATE events SET metadata=? WHERE id=1', (json.dumps(old),))
        self.made_now()
        self.stays(replied)
        with self.store.connect() as db:
            self.assertNotIn('seen', json.loads(db.execute('SELECT metadata FROM events WHERE id=1').fetchone()[0])['team_reply'])

    def test_a_reply_is_not_enough_for_more(self):
        handled = conversation(part('comment', T, admin()))
        self.step({'kind': 'finish', 'label': 'Send quote'})
        self.stays(handled)
        self.step(REPLY, {'kind': 'finish', 'label': 'Send quote'})
        self.stays(handled)
        self.step({**REPLY, 'kind': 'email', 'to': ['customer@example.com'], 'attachments': [{'name': 'quote.pdf'}]})
        self.stays(handled)
        self.step({'kind': 'email', 'to': ['someone@else.example'], 'body': 'Hi'})
        self.stays(handled)
        self.step(REPLY, done_when='They confirm the export works')
        self.stays(handled)
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET next_action=NULL,done_when=NULL WHERE id=?', (self.sid,))
        self.stays(handled)  # nothing drafted: unsure what it asks, so it stays

    def test_other_evidence_too_stays(self):
        self.store.commit_page('mail', {}, [{'account_id': 'mail', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Export', 'body': 'Also by mail', 'deleted': False, 'metadata': {'from': 'customer@example.com'}}])
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET event_ids=? WHERE id=?', ('[1, 2]', self.sid))
        self.stays(conversation(part('close', T, admin(), body=None), state='closed'))

    def test_open_to_dos_conversations_are_read_again_once_without_a_new_review(self):
        with self.store.connect() as db:
            old = json.loads(db.execute('SELECT metadata FROM events WHERE id=1').fetchone()[0])
            for key in ('team_closed', 'team_reply', 'customer_at'):
                old.pop(key)
            db.execute('UPDATE events SET metadata=? WHERE id=1', (json.dumps(old),))
        self.assertEqual(self.store.intercom_rereads('ic'), ['7'])
        self.sync(conversation())  # the same conversation: kept, no new version for the review
        with self.store.connect() as db:
            row = db.execute('SELECT version,metadata FROM events WHERE id=1').fetchone()
        self.assertEqual(row[0], 1)
        self.assertIn('customer_at', json.loads(row[1]))
        self.assertEqual(self.store.intercom_rereads('ic'), [])

    def test_the_sync_rereads_them_once(self):
        with self.store.connect() as db:
            old = json.loads(db.execute('SELECT metadata FROM events WHERE id=1').fetchone()[0])
            old.pop('customer_at')
            db.execute('UPDATE events SET metadata=? WHERE id=1', (json.dumps(old),))
        asked = []

        class Fake:
            def profile(self):
                return {}

            def request(self, method, path, payload=None):
                asked.append(path)
                if path == '/conversations/search':
                    return {'conversations': [], 'pages': {}, 'total_count': 0}
                return conversation(part('close', T, admin(), body=None), state='closed')
        helpers = a.CONNECTOR_HELPERS
        intercom.sync(self.store, {'bootstrap_days': 7}, OWN, helpers, source=Fake())
        self.assertEqual(asked, ['/conversations/search', '/conversations/7'])
        self.assertEqual(self.store.close_handled_intercom(), [self.sid])
        asked.clear()
        intercom.sync(self.store, {'bootstrap_days': 7}, OWN, helpers, source=Fake())
        self.assertEqual(asked, ['/conversations/search'])

    def test_the_lines_are_in_every_language(self):
        for lang in ('en', 'nl', 'fr', 'de', 'es', 'it', 'pt-BR', 'zh-CN', 'ja', 'ko', 'ru'):
            catalog = json.loads((ROOT / 'i18n' / f'{lang}.json').read_text())
            for key in ('Closed in Intercom', 'Answered in Intercom', 'Closed in Intercom by {}', 'Answered in Intercom by {}'):
                self.assertIn(key, catalog)


if __name__ == '__main__':
    unittest.main()
