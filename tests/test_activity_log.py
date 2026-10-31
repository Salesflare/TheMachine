"""Activity (activity_log.py): one read-only list of everything The Machine did, newest first, from what each part
already keeps: the outbox (sent, blocked, failed, undone; by the owner's OK, by voice, by itself), coding agents, Fleet
questions both ways, learnings sent and withdrawn, skills, Graph imports and connections added or removed. Filters by
kind, several kinds (Fleet, Activity), refused or blocked, and one actor; another module plugs in with register()."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_assistant import assistant as a, event
import activity_log
import fleet

GMAIL = {'id': 'work', 'service': 'gmail', 'email': 'sam@acme.example'}


class Activity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [event()])
        with patch.object(a, 'now', return_value='2026-10-30T08:00:00+00:00'):
            self.card = self.store.suggest('task-1', 'Reply to Robin', 'Body', [1])['id']
        self.config = {'accounts': [GMAIL]}

    def job(self, n, payload, status, at, source='dashboard'):
        with self.store.connect() as db:
            db.execute('INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id)'
                       ' VALUES(?,?,?,?,?,?,?,?,?,?)', (f'job{n}', self.card, f'r{n}', json.dumps(payload), status, at, at, 'ok', source, ''))

    def page(self, **kw):
        with self.store.connect() as db:
            return activity_log.page(db, self.config, **kw)

    def test_outbox_lines_say_what_where_how_it_went_and_who_started_it(self):
        self.job(1, {'kind': 'email', 'to': ['Robin <robin@globex.example>'], 'subject': 'Pricing', 'account_id': 'work'}, 'sent', '2026-10-30T09:00:00+00:00')
        self.job(2, {'kind': 'slack', 'to': 'Robin', 'account_id': 'work'}, 'blocked', '2026-10-30T10:00:00+00:00', 'voice')
        self.job(3, {'kind': 'doc_write', 'op': 'create', 'title': 'Plan'}, 'sent', '2026-10-30T11:00:00+00:00')
        self.job(4, {'kind': 'merge', 'label': 'Fix the digest'}, 'sent', '2026-10-30T12:00:00+00:00', 'auto')
        self.job(5, {'kind': 'email', 'to': ['robin@globex.example'], 'subject': 'Again'}, 'undone', '2026-10-30T13:00:00+00:00')
        items = self.page()['items']
        self.assertEqual([x['id'] for x in items], ['messages:job5', 'fixes:job4', 'docs:job3', 'messages:job2', 'messages:job1'])
        sent = items[-1]
        self.assertEqual((sent['what'], sent['outcome'], sent['status'], sent['by']), ('Email to Robin: Pricing', 'done', 'Sent', 'After your OK'))
        self.assertIn('sam@acme.example', sent['where'])
        self.assertEqual(sent['todo'], {'id': self.card, 'title': 'Reply to Robin'})
        self.assertEqual((items[3]['outcome'], items[3]['status'], items[3]['by']), ('refused', 'Blocked', 'Approved by voice'))
        self.assertEqual((items[2]['what'], items[2]['status']), ('New doc: Plan', 'Created'))
        self.assertEqual((items[1]['kind'], items[1]['by']), ('fixes', 'By itself'))
        self.assertEqual((items[0]['outcome'], items[0]['status']), ('undone', 'Undone'))
        for line in items:
            self.assertFalse(line['what'].startswith('You'))

    def test_filters_by_kind_several_kinds_and_refused(self):
        self.job(1, {'kind': 'email', 'to': ['a@b.example']}, 'sent', '2026-10-30T09:00:00+00:00')
        self.job(2, {'kind': 'calendar', 'label': 'Lunch'}, 'failed', '2026-10-30T10:00:00+00:00')
        self.job(3, {'kind': 'whatsapp', 'to': 'Robin'}, 'blocked', '2026-10-30T11:00:00+00:00')
        with self.store.connect() as db:
            fleet.ensure(db)
            db.execute("INSERT INTO fleet_log(at,direction,fleet,member_id,name,kind,what,outcome) VALUES('2026-10-30T12:00:00+00:00','in','fl','m','Kim','meeting','Who is joining?','declined by your rules')")
        page = self.page()
        self.assertEqual(set(page['kinds']), {'messages', 'calendar', 'fleet'})
        self.assertEqual([x['id'] for x in self.page(kind='calendar')['items']], ['calendar:job2'])
        self.assertEqual({x['kind'] for x in self.page(kind='fleet,messages')['items']}, {'fleet', 'messages'})
        refused = self.page(outcome='refused')['items']
        self.assertEqual({x['kind'] for x in refused}, {'messages', 'fleet'}, 'what was blocked and what a rule declined')
        self.assertEqual(set(self.page(kind='calendar')['kinds']), {'messages', 'calendar', 'fleet'}, 'the filter still knows every kind')
        for bad in ({'kind': 'nope'}, {'outcome': 'nope'}, {'offset': 'x'}):
            with self.assertRaises(ValueError):
                self.page(**bad)

    def test_learnings_sent_and_withdrawn_keep_withdraw_and_what_went(self):
        sent = {'auto': True, 'named': False, 'items': [{'text': 'Drafts introduce the context first.', 'example': 'A first email says who we are.',
                                                          'log': '', 'use_cases': [{'given': 'a new customer', 'when': 'a draft', 'then': 'an intro'}]},
                                                         {'text': 'Meeting notes need decisions on top.'}], 'withdrawn': {'2': '2026-10-30T12:00:00+00:00'}}
        with self.store.connect() as db:
            db.execute("INSERT INTO team_learnings(id,status,items,created_at,decided_at,sent) VALUES('tl_1','sent','[]','2026-10-30T09:00:00+00:00','2026-10-30T10:00:00+00:00',?)", (json.dumps(sent),))
        lines = {x['id']: x for x in self.page(kind='learnings')['items']}
        first, second = lines['learnings:tl_1:1'], lines['learnings:tl_1:2']
        self.assertEqual((first['status'], first['by'], first['withdraw']), ('Sent', 'By itself', {'id': 'tl_1', 'n': 1}))
        self.assertEqual(first['sent']['use_cases'], ['a new customer · a draft · an intro'])
        self.assertEqual((second['outcome'], second['status'], second['withdraw']), ('undone', 'Withdrawn', None))

    def test_connections_added_and_removed(self):
        with self.store.connect() as db:
            activity_log.note_accounts(db, [GMAIL], '2026-10-30T09:00:00+00:00')  # the first look only remembers
            self.assertEqual(self.page(kind='connections')['items'], [])
            slack = {'id': 'team', 'service': 'slack', 'slack_host': 'acme.slack.com'}
            activity_log.note_accounts(db, [GMAIL, slack], '2026-10-30T10:00:00+00:00')
            activity_log.note_accounts(db, [slack], '2026-10-30T11:00:00+00:00')
        lines = self.page(kind='connections')['items']
        self.assertEqual([(x['what'], x['status']) for x in lines], [('Connection removed', 'Removed'), ('Connection added', 'Added')])
        self.assertIn('sam@acme.example', lines[0]['where'])

    def test_another_module_plugs_in_as_one_more_kind_with_its_own_actor(self):
        def calls(db, limit):
            yield {'id': 'ai:1', 'kind': 'ai', 'at': '2026-10-30T09:00:00+00:00', 'what': 'list_todos', 'where': 'Claude',
                   'outcome': 'done', 'status': '3 to-dos', 'by': None, 'actor': 'conn_a', 'todo': None, 'detail': None}
            yield {'id': 'ai:2', 'kind': 'ai', 'at': '2026-10-30T10:00:00+00:00', 'what': 'create_todo', 'where': 'Cursor',
                   'outcome': 'refused', 'status': 'Refused', 'by': None, 'actor': 'conn_b', 'todo': None, 'detail': None}
            raise RuntimeError('a broken source is left out, never the whole list')
        activity_log.register('ai', calls)
        self.addCleanup(activity_log._sources.pop, 'ai', None)
        self.assertEqual([x['id'] for x in self.page(kind='ai')['items']], ['ai:2', 'ai:1'])
        self.assertEqual([x['id'] for x in self.page(actor='conn_a')['items']], ['ai:1'])
        self.assertEqual([x['id'] for x in self.page(outcome='refused')['items']], ['ai:2'])
        with self.assertRaises(ValueError):
            activity_log.register('nope', calls)

    def test_pages_newest_first_with_a_cursor(self):
        for n in range(75):
            self.job(n, {'kind': 'email', 'to': ['a@b.example']}, 'sent', f'2026-10-30T{9 + n // 60:02d}:{n % 60:02d}:00+00:00')
        first = self.page()
        self.assertEqual(len(first['items']), activity_log.PAGE)
        rest = self.page(offset=first['next'])
        ids = [x['id'] for x in first['items'] + rest['items']]
        self.assertEqual(len(ids), 75); self.assertEqual(len(set(ids)), 75)
        self.assertIsNone(rest['next'])

    def test_a_done_to_do_opens_from_its_line(self):
        self.store.decide(self.card, 'complete', '', 'done-1', 'dashboard')
        with patch.object(a, 'now', return_value='2026-10-30T09:00:00+00:00'):
            other = self.store.suggest('task-2', 'Other', 'Body', [1])['id']
        self.store.decide(other, 'complete', '', 'done-2', 'dashboard')
        self.assertEqual([c['id'] for c in self.store.done_page(only=self.card)['cards']], [self.card])


if __name__ == '__main__':
    unittest.main()
