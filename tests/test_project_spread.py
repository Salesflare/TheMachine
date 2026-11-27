"""Catch-all projects (project_spread.py): a review's label keeps a thread that shares nobody with a project off it once
the project holds a few one-way groups, or is a catch-all; the owner's own labels and the chat's never pass the guard.
A catch-all's page says so; Split up then proposes one project per counterpart that answered (no model turn) and takes
the one-way messages off, with Undo; Keep as one stops it. Made-up people and companies; nothing is sent."""
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest

import machine.main as machine_main

import graph
import project_split
import project_spread

OWNER = 'owner@example.com'


class Spread(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite', protect=True)
        self.accounts = [{'id': 'work', 'service': 'gmail', 'email': OWNER, 'boundary': 'work:Example'}]
        self.store.accounts = self.accounts
        self.store.config = {'accounts': self.accounts}
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': self.accounts}
        self.app.fleet = None
        self.app.graph_build = lambda *_, **__: None
        self.app.split_model = lambda config, prompt: self.fail('a catch-all is split without a model turn')
        self.base = dt.datetime(2026, 9, 1, 9, tzinfo=dt.timezone.utc)
        self.n = 0
        with self.store.connect() as db:
            graph.ensure(db)

    def mail(self, db, thread, day, sender, to, cc=()):
        self.n += 1
        meta = {'from': sender, 'to': ', '.join(to), 'thread_id': thread, 'labels': ['SENT'] if sender == OWNER else ['INBOX']}
        if cc:
            meta['cc'] = ', '.join(cc)
        at = (self.base + dt.timedelta(days=day, minutes=self.n)).isoformat()
        return db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) "
                          "VALUES('work',?,'gmail.message',?,'Subject','',?,'h',?)", (f'm{self.n}', at, json.dumps(meta), at)).lastrowid

    def owner(self, db):
        return graph.Owner({'accounts': self.accounts}, db)

    def label(self, db, name, ids):
        return project_spread.label(db, {name: ids}, self.owner(db), self.base.isoformat()).get(name, 0)

    def on(self, db, name):
        return {r[0] for r in db.execute('SELECT event_id FROM event_projects ep JOIN projects p ON p.id=ep.project_id WHERE p.name=?', (name,))}

    def invites(self, db, count, start=0):
        return [self.mail(db, f'inv-{i}', 1, OWNER, [f'Tester {i} <t{i}@co{i}.example>']) for i in range(start, start + count)]

    def test_outreach_stops_at_a_few_one_way_contacts_and_replies_still_join(self):
        with self.store.connect() as db:
            sent = self.invites(db, 8)
            self.assertEqual(self.label(db, 'Alpha testing', sent), 5)
            self.assertEqual(self.on(db, 'Alpha testing'), set(sent[:project_spread.ONE_WAY]))
            # a reply from someone already on it joins; so does a thread with nobody outside (a note to self)
            reply = self.mail(db, 'inv-0', 4, 'Tester 0 <t0@co0.example>', [OWNER])
            note = self.mail(db, 'self', 4, OWNER, [OWNER])
            self.assertEqual(self.label(db, 'Alpha testing', [reply, note]), 0)
            # a one-way message to a colleague-free newcomer is still kept off; one they answered is not yet a catch-all
            answer = self.mail(db, 'inv-6', 5, 'Tester 6 <t6@co6.example>', [OWNER])
            self.assertEqual(self.label(db, 'Alpha testing', [answer]), 0)
            self.assertIn(answer, self.on(db, 'Alpha testing'))

    def test_a_deal_with_partner_customer_and_lawyer_is_not_touched(self):
        with self.store.connect() as db:
            ids = [self.mail(db, 'intro', 1, OWNER, ['Mara <mara@northwind.example>', 'Ivo <ivo@integra.example>']),
                   self.mail(db, 'scope', 2, OWNER, ['Mara <mara@northwind.example>']),
                   self.mail(db, 'plan', 3, OWNER, ['Ivo <ivo@integra.example>']),
                   self.mail(db, 'legal', 4, OWNER, ['Lena <lena@voslaw.example>']),
                   self.mail(db, 'sec', 5, OWNER, ['Desk <sec@auditly.example>']),
                   self.mail(db, 'legal', 6, 'Lena <lena@voslaw.example>', [OWNER])]
            for i in ids:  # one review batch a day
                self.assertEqual(self.label(db, 'Northwind rollout', [i]), 0)
            found, _ = project_spread.shape(db, graph.project_id(db, 'Northwind rollout', self.base.isoformat()), self.owner(db))
            self.assertEqual((len(found.groups), found.one_way, found.catch_all()), (3, 2, False), 'the lawyer answered; the rest only heard from the owner')

    def test_old_labels_and_the_owners_own_word_stay(self):
        with self.store.connect() as db:
            sent = self.invites(db, 10)
            graph.label(db, sent, 'Old bundle', 'review', self.base.isoformat())  # made before the guard
            pid = graph.project_id(db, 'Old bundle', self.base.isoformat())
            self.assertEqual(self.on(db, 'Old bundle'), set(sent), 'nothing already on a project comes off by itself')
            self.assertEqual(project_spread.page(db, pid, self.owner(db)), {'groups': 10, 'one_way': 10})
            more = self.invites(db, 2, start=10)
            self.assertEqual(self.label(db, 'Old bundle', more), 2, 'a catch-all takes no newcomer from a review')
            graph.label(db, more, 'Old bundle', 'owner', self.base.isoformat())
            self.assertLessEqual(set(more), self.on(db, 'Old bundle'), "the owner's label is never refused")

    def test_keep_as_one_lets_it_grow_until_it_doubles(self):
        with self.store.connect() as db:
            sent = self.invites(db, 6)
            graph.label(db, sent, 'Launch list', 'review', self.base.isoformat())
            pid = graph.project_id(db, 'Launch list', self.base.isoformat())
        self.assertEqual(self.app.project_split_action('project_split', {'op': 'keep', 'node_id': f'project:{pid}'}, owner_dashboard=True), {'kept': 6})
        with self.store.connect() as db:
            self.assertIsNone(project_spread.page(db, pid, self.owner(db)))
            self.assertEqual(self.label(db, 'Launch list', self.invites(db, 5, start=6)), 0)
            self.assertEqual(project_spread.page(db, pid, self.owner(db)), None, '11 groups: under twice what it had')
            self.assertEqual(self.label(db, 'Launch list', self.invites(db, 1, start=11)), 0)
            self.assertEqual(project_spread.page(db, pid, self.owner(db)), {'groups': 12, 'one_way': 12}, 'twice what it had: a catch-all again')
            self.assertEqual(self.label(db, 'Launch list', self.invites(db, 1, start=12)), 1)
        with self.assertRaises(Exception):
            self.app.project_split_action('project_split', {'op': 'keep', 'node_id': f'project:{pid}'})  # only the owner, on the dashboard

    def test_split_proposes_one_project_per_answer_and_undo_puts_it_back(self):
        with self.store.connect() as db:
            sent = self.invites(db, 9)
            replies = [self.mail(db, f'inv-{i}', 3, f'Tester {i} <t{i}@co{i}.example>', [OWNER]) for i in (1, 4)]
            note = self.mail(db, 'self', 3, OWNER, [OWNER])
            graph.label(db, sent + replies + [note], 'Alpha testing', 'review', self.base.isoformat())
            pid = graph.project_id(db, 'Alpha testing', self.base.isoformat())
            # someone already has their own project: their part goes there
            mine = graph.label(db, [self.mail(db, 'own-4', 2, 'Tester 4 <t4@co4.example>', [OWNER])], 'Co4 trial', 'owner', self.base.isoformat())
            db.execute("UPDATE projects SET org='co4.example' WHERE id=?", (mine,))
            before = sorted(tuple(r) for r in db.execute('SELECT * FROM event_projects'))
        found = self.app.project_split_action('project_split', {'op': 'propose', 'node_id': f'project:{pid}'}, owner_dashboard=True)
        self.assertEqual(sorted(p['name'] for p in found['parts']), ['Co4 trial', 'co1.example'])
        self.assertEqual(found['drop'], ['g:none'])
        self.assertEqual((found['items']['g:none']['label'], found['items']['g:none']['sub']), ('Messages nobody answered', '7 conversations'))
        with self.store.connect() as db:
            self.assertEqual(sorted(tuple(r) for r in db.execute('SELECT * FROM event_projects')), before, 'a proposal changes nothing')
        done = self.app.project_split_action('project_split', {'op': 'apply', 'node_id': f'project:{pid}', 'parts': found['parts'], 'drop': found['drop']},
                                             owner_dashboard=True)
        self.assertEqual(sorted(p['name'] for p in done['projects']), ['Co4 trial', 'co1.example'])
        self.assertFalse(done['archived'], 'the note to self stays on it')
        with self.store.connect() as db:
            self.assertEqual(self.on(db, 'Alpha testing'), {note})
            self.assertEqual(self.on(db, 'co1.example'), {sent[1], replies[0]})
            self.assertLessEqual({sent[4], replies[1]}, self.on(db, 'Co4 trial'))
            self.assertEqual(db.execute('SELECT count(*) FROM events WHERE deleted=0').fetchone()[0], 13, 'nothing deleted')
        self.app.project_split_action('project_split', {'op': 'undo', 'split_id': done['split_id']}, owner_dashboard=True)
        with self.store.connect() as db:
            self.assertEqual(sorted(tuple(r)[:2] for r in db.execute('SELECT * FROM event_projects')), sorted(r[:2] for r in before))
            self.assertIsNone(db.execute("SELECT 1 FROM projects WHERE name='co1.example'").fetchone())
            self.assertTrue(db.execute("SELECT 1 FROM projects WHERE name='Co4 trial'").fetchone(), 'the project that was there stays')

    def test_a_review_through_graph_is_guarded_and_the_chat_is_not(self):
        with self.store.connect() as db:
            sent = self.invites(db, 6)
        self.app.graph_read = lambda args, changed=False: {}
        self.app.graph_later = lambda: None
        self.app.graph_action({'project': 'Beta list', 'event_ids': sent, '_review_session': 'agent:main:assistant-review-signals-x'})
        with self.store.connect() as db:
            self.assertEqual(len(self.on(db, 'Beta list')), project_spread.ONE_WAY)
        self.app.graph_action({'project': 'Beta list', 'event_ids': sent})
        with self.store.connect() as db:
            self.assertEqual(self.on(db, 'Beta list'), set(sent), "the chat labels what the owner asked")


if __name__ == '__main__':
    unittest.main()
