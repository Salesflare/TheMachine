"""Facebook friends nobody in the Graph has, added as people (birthdays_facebook.add and remove, the Import birthdays from
Facebook to-do's Add button, docs/help/routines.md "Templates"): only on the owner's tap, each a Personal person
with their name and birthday (source facebook), never shared with a Work Fleet. Matched again at that moment: a name a
person in the Graph has now, or two people have, is skipped. One transaction, one Graph build after it, and nothing
looked up for them. Undo takes exactly those people away. Made-up people only."""
import datetime as dt
import importlib.util
import json
import sqlite3
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('facebook_people_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import birthdays  # noqa: E402
import birthdays_facebook as fb  # noqa: E402
import enrichment  # noqa: E402
import graph  # noqa: E402
import graph_show  # noqa: E402
import person_birthday  # noqa: E402
import shared_graph  # noqa: E402

NOW = '2026-11-10T09:00:00+00:00'
FIRST = 'Ada Bram Cleo Dov Esme Finn Gia Hugo Ines Jules Kai Lena Milo Nora Otto Pia Quin Rhea Sami Tove Uma Vito Wren Xavi Yara'.split()
LAST = 'Arden Brook Calloway Dunmore Ellery Fairbank Garrow Hollis Ivers Jessup Kestrel Lowell Marsh Northam Orrin Pell Quarry Rook Stroud Thorne'.split()


class AddPeople(unittest.TestCase):
    ITEMS = [{'name': 'Sam Rivera', 'month': 11, 'day': 14}, {'name': 'Pat Quinn', 'month': 12, 'day': 9},
             {'name': 'Mira Holt', 'month': 1, 'day': 5, 'year': 1990}, {'name': 'Theo Brandt', 'month': 2, 'day': 7},
             {'name': 'Cher', 'month': 3, 'day': 3}, {'name': '', 'month': 4, 'day': 4}]

    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'home', 'email': 'owner@mail.example', 'service': 'gmail', 'boundary': 'personal'}],
                           'timezone': 'Europe/Brussels', 'browser_cdp_url': 'http://127.0.0.1:9'}
        self.store.accounts = self.app.config['accounts']
        self.app.birthdays_facebook_inline = True
        self.answer, self.builds = {'items': self.ITEMS}, []
        for name, value in (('birthdays_facebook_base', lambda s: 'http://127.0.0.1:9'), ('graph_later', lambda s: self.builds.append(1))):
            owner = a.BirthdaysTemplate if hasattr(a.BirthdaysTemplate, name) else a.App  # the template's own, else the App's
            p = patch.object(owner, name, value); p.start(); self.addCleanup(p.stop)
        p = patch.object(fb, 'read', lambda base, url=fb.PAGE, limits=None: self.answer); p.start(); self.addCleanup(p.stop)
        p = patch('subprocess.run', lambda *x, **k: subprocess.CompletedProcess(x, 0, '', '')); p.start(); self.addCleanup(p.stop)  # the lease
        with self.store.connect() as db:
            graph.ensure(db)
            for node, name in (('email:sam@mail.example', 'Sam Rivera'), ('email:pat@one.example', 'Pat Quinn'), ('email:pat@two.example', 'Pat Quinn')):
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,'person',?,1,?,5,?)",
                           (node, name, '2026-11-01', json.dumps({'identifiers': [node], 'wrote': 3})))

    def step(self, sid, step):
        return self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': step}, owner_dashboard=True)

    def read(self):
        sid = self.app.template('birthdays').birthdays_facebook_offer({'routine_id': 'r1'})
        self.step(sid, 'read')
        return sid

    def card(self, sid):
        with self.store.connect() as db:
            return fb.view(db, sid)

    def people(self):
        with self.store.connect() as db:
            return {r['name']: (r['id'], json.loads(r['info'])) for r in db.execute("SELECT id,name,info FROM graph_nodes WHERE kind='person'")}

    def build(self):
        with self.store.connect() as db:
            db.isolation_level = None
            graph.build(db, {'accounts': self.app.config['accounts'], 'embeddings': {'enabled': False}}, NOW)

    def test_the_preview_names_the_others_and_nothing_is_added_before_the_tap(self):
        sid = self.read()
        view = self.card(sid)
        self.assertEqual((view['matched'], view['ambiguous'], view['others'], view['others_shown'], view['added']),
                         (1, ['Pat Quinn'], 2, ['Mira Holt', 'Theo Brandt'], 0))  # no one-word or empty name
        self.assertEqual(set(self.people()), {'Sam Rivera', 'Pat Quinn'})
        with self.assertRaises(ValueError):
            self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': 'add'}, owner_dashboard=False)

    def test_add_makes_personal_people_with_their_birthday_never_shared(self):
        sid = self.read()
        self.assertEqual(self.step(sid, 'add'), {'state': 'preview', 'added': 2})
        self.assertEqual(self.builds, [1])  # one build for all of them, in the worker
        people = self.people()
        node, info = people['Mira Holt']
        self.assertTrue(node.startswith('manual:'))
        self.assertEqual((info['side'], info['side_by'], info['manual']), ('personal', 'owner', True))  # on their page at once
        with self.store.connect() as db:
            self.assertEqual(person_birthday.get(db, node)['value'], '1990-01-05')
            self.assertEqual(person_birthday.get(db, node)['source'], 'facebook')
            self.assertEqual(person_birthday.get(db, people['Theo Brandt'][0])['value'], '--02-07')
        self.assertEqual(self.card(sid)['added'], 2)
        with self.assertRaises(ValueError):
            self.step(sid, 'add')  # once
        self.build()
        people = self.people()
        self.assertTrue(graph.own_life(people['Mira Holt'][1]))  # Personal by the owner's word, after a build too
        with self.store.connect() as db:
            shared_graph.ensure(db)
            private = shared_graph.Scope(db, ['home'], set(), {'owner@mail.example'}).private
        self.assertTrue({people['Mira Holt'][0], people['Theo Brandt'][0]} <= private)
        self.assertNotIn('email:sam@mail.example', private)

    def test_a_name_the_graph_has_by_now_is_skipped(self):
        sid = self.read()
        with self.store.connect() as db:  # added by hand between the read and the tap
            db.execute('BEGIN IMMEDIATE')
            graph.create_record(db, 'person', {'name': 'Theo  Brandt'}, NOW)
            db.execute('COMMIT')
        self.build()
        self.assertEqual(self.step(sid, 'add')['added'], 1)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM manual_nodes WHERE name LIKE 'Theo%'").fetchone()[0], 1)

    def test_undo_takes_exactly_those_people_away(self):
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            mine = graph.create_record(db, 'person', {'name': 'Lou Garrow'}, NOW)['node_id']  # the owner's own, before
            db.execute('COMMIT')
        sid = self.read()
        self.step(sid, 'add')
        self.build()
        added = [i for n, (i, _) in self.people().items() if n in ('Mira Holt', 'Theo Brandt')]
        self.assertEqual(len(added), 2)
        self.assertEqual(self.step(sid, 'undo_add'), {'state': 'preview', 'undone': 2})
        self.assertEqual(set(self.people()) & {'Mira Holt', 'Theo Brandt', 'Lou Garrow'}, {'Lou Garrow'})  # gone at once
        with self.store.connect() as db:
            for table, column in (('manual_nodes', 'identifier'), ('graph_names', 'node_id'), ('person_edits', 'identifier'), ('person_facts', 'identifier')):
                self.assertEqual(db.execute(f'SELECT count(*) FROM {table} WHERE {column} IN (?,?)', added).fetchone()[0], 0, table)
            self.assertTrue(db.execute('SELECT 1 FROM manual_nodes WHERE identifier=?', (mine,)).fetchone())
        self.build()
        self.assertEqual(set(self.people()) & {'Mira Holt', 'Theo Brandt', 'Lou Garrow'}, {'Lou Garrow'})
        self.assertEqual((self.card(sid)['others'], self.card(sid)['added']), (2, 0))  # can be added again
        with self.assertRaises(ValueError):
            self.step(sid, 'undo_add')
        self.assertEqual(self.step(sid, 'add')['added'], 2)

    def delete(self, name):
        node = self.people()[name][0]
        self.app.delete_person(node, workspace=Path(self.store.path).parent / 'workspace')

    def test_someone_deleted_permanently_is_not_added_again_by_name(self):
        with self.store.connect() as db:  # the owner had them by name only (a hand-added person), and with a middle name
            db.execute('BEGIN IMMEDIATE')
            done = graph.create_record(db, 'person', {'name': 'Mira Jane Holt'}, NOW)
            graph_show.show_new_record(db, done, 'person')
            db.execute('COMMIT')
        self.delete('Mira Jane Holt')
        sid = self.read()
        view = self.card(sid)
        self.assertEqual((view['others'], view['others_shown']), (1, ['Theo Brandt']))  # the count on Add leaves them out
        self.assertEqual(self.step(sid, 'add')['added'], 1)
        self.assertNotIn('Mira Holt', self.people())
        self.assertEqual(self.step(sid, 'undo_add')['undone'], 1)  # Undo still takes exactly the one it added
        self.assertEqual(set(self.people()), {'Sam Rivera', 'Pat Quinn'})
        self.assertEqual(self.card(sid)['others'], 1)

    def test_someone_deleted_after_the_read_drops_off_the_count_and_add(self):
        with self.store.connect() as db:  # known by their address, then deleted while the to-do waits
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,'person',?,1,?,5,?)",
                       ('email:theo@mail.example', 'Theo Brandt', '2026-11-01', json.dumps({'identifiers': ['email:theo@mail.example'], 'wrote': 3})))
        sid = self.read()
        self.assertEqual(self.card(sid)['others'], 1)  # Theo matches the person they are now
        with self.store.connect() as db:
            fb.put(db, sid, 'preview', {**fb.get(db, sid)[1], 'others': [{'name': 'Mira Holt', 'date': '1990-01-05'},
                                                                        {'name': 'Theo Brandt', 'date': '--02-07'}]}, NOW)
        self.delete('Theo Brandt')
        self.assertEqual((self.card(sid)['others'], self.card(sid)['others_shown']), (1, ['Mira Holt']))
        self.assertEqual(self.step(sid, 'add')['added'], 1)
        self.assertEqual(set(self.people()), {'Sam Rivera', 'Pat Quinn', 'Mira Holt'})
        self.assertEqual(self.step(sid, 'undo_add')['undone'], 1)

    def test_add_after_save_on_the_done_todo(self):
        sid = self.read()
        self.assertEqual(self.step(sid, 'save')['saved'], 1)
        view = self.card(sid)
        self.assertEqual((view['state'], view['others'], view['others_shown']), ('saved', 2, ['Mira Holt', 'Theo Brandt']))
        self.assertEqual(self.step(sid, 'add'), {'state': 'saved', 'added': 2})
        self.assertEqual(self.card(sid)['added'], 2)
        self.assertEqual(self.step(sid, 'undo_add')['undone'], 2)

    def test_five_thousand_at_once_are_quick_and_nothing_is_looked_up_for_them(self):
        names = [f'{f} {m} {l}' for f in FIRST for m in FIRST[:10] for l in LAST][:5000]
        self.answer = {'items': [{'name': n, 'month': 1 + i % 12, 'day': 1 + i % 28} for i, n in enumerate(names)]}
        sid = self.read()
        self.assertEqual(self.card(sid)['others'], 5000)
        start = time.monotonic()
        self.assertEqual(self.step(sid, 'add')['added'], 5000)
        took = time.monotonic() - start
        self.assertLess(took, 20, f'adding 5,000 took {took:.1f} s')
        self.assertEqual(self.builds, [1])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM graph_nodes WHERE kind='person' AND id LIKE 'manual:%'").fetchone()[0], 5000)
            due = {p['identifier'] for p in enrichment.people_due(db, NOW, 6000)}
            self.assertFalse({i for i in due if i.startswith('manual:')})
            self.assertEqual(len(due), 3)  # only the people with an address: none of them is looked up
            self.assertFalse([i for i in birthdays.close_people(db) if i.startswith('manual:')])  # no messages: no birthday to-dos for them
        start = time.monotonic()
        self.assertEqual(self.step(sid, 'undo_add')['undone'], 5000)
        self.assertLess(time.monotonic() - start, 20)

    # A to-do read before the friends nobody in the Graph were kept: its preview or Save has the matched ones and only a
    # count of the rest. At start the same read as Import again fills them in, in the background and without a tap.

    def old(self, state):
        sid = self.app.template('birthdays').birthdays_facebook_offer({'routine_id': 'r1'}) or 'saved-before'  # offered once: the other one by hand
        with self.store.connect() as db:
            match = fb.match(db, fb.found(self.ITEMS, dt.date(2026, 11, 10)))
            data = {'found': 4, 'matched': match['matched'], 'new': 1, 'ambiguous': match['ambiguous'], 'unmatched': 4,
                    'capped': False, 'missing': []} if state == 'preview' else {'saved': 1, 'people': [{'id': 'email:sam@mail.example', 'name': 'Sam Rivera'}]}
            fb.put(db, sid, state, data, '2026-11-09T08:00:00+00:00')
        return sid

    def test_an_older_preview_and_save_get_their_friends_at_start_and_keep_the_rest(self):
        preview, saved = self.old('preview'), self.old('saved')
        self.assertEqual((self.card(preview)['others'], self.card(saved)['others']), (0, 0))
        self.app.stop = threading.Event()
        self.app.template('birthdays').birthdays_facebook_fill_old()
        for sid, state in ((preview, 'preview'), (saved, 'saved')):
            view = self.card(sid)
            self.assertEqual((view['state'], view['others'], view['others_shown'], view['added']), (state, 2, ['Mira Holt', 'Theo Brandt'], 0))
            with self.store.connect() as db:
                self.assertEqual(fb.get(db, sid)[2], '2026-11-09T08:00:00+00:00')  # it reads as it did: no newer to-do
        self.assertEqual(self.card(preview)['matched'], 1)
        self.assertEqual(self.card(saved)['saved'], 1)
        self.assertEqual(set(self.people()), {'Sam Rivera', 'Pat Quinn'})  # nothing is added without the tap
        self.assertEqual(self.step(preview, 'add')['added'], 2)  # and Add works on it
        with self.store.connect() as db:
            self.assertEqual(fb.to_fill(db), [])
        self.answer = {'items': []}
        self.app.template('birthdays').birthdays_facebook_fill_old()  # once only
        self.assertEqual(self.card(preview)['others'], 2)

    def test_a_failed_read_leaves_none_and_no_browser_waits_for_the_next_start(self):
        sid = self.old('preview')
        self.app.stop = threading.Event()
        with patch.object(a.BirthdaysTemplate, 'birthdays_facebook_base', lambda s: None), patch('birthdays_facebook_app.FILL_WAIT', 0):
            self.app.template('birthdays').birthdays_facebook_fill_old()
        with self.store.connect() as db:
            self.assertEqual(fb.to_fill(db), [sid])  # no browser yet: tried again at the next start
        self.answer = {'error': 'signed-out'}
        with patch('birthdays_facebook_app.FILL_AGAIN', 0), self.assertLogs('personal-assistant', 'INFO') as logs:
            self.app.template('birthdays').birthdays_facebook_fill_old()
        view = self.card(sid)
        self.assertEqual((view['state'], view['matched'], view['others']), ('preview', 1, 0))
        self.assertEqual(len(logs.output), fb.FILL_READS)  # signed out: read again a few times, then none; Import again reads anew
        self.assertIn('short, kept as it is found=0 others=0', logs.output[-1])
        with self.store.connect() as db:
            self.assertEqual(fb.to_fill(db), [])

    # A fill's read that came back short (cut at its limits, months missing, the page never answering its scrolls, or
    # clearly fewer than the to-do's own read found) keeps what it found and is read again later, a few times at most.

    def fill(self, *answers):
        reads = list(answers)
        p = patch.object(fb, 'read', lambda base, url=fb.PAGE, limits=None: reads.pop(0) if len(reads) > 1 else reads[0])
        with p, patch('birthdays_facebook_app.FILL_AGAIN', 0), self.assertLogs('personal-assistant', 'INFO') as logs:
            self.app.template('birthdays').birthdays_facebook_fill_old()
        return [line.split(':', 2)[2] for line in logs.output]

    def test_a_short_read_keeps_what_it_found_and_is_read_again_until_it_is_whole(self):
        sid = self.old('preview')
        with self.store.connect() as db:  # the to-do's own read found 40 friends: 36 nobody in the Graph has
            fb.put(db, sid, 'preview', {**fb.get(db, sid)[1], 'found': 40}, '2026-11-09T08:00:00+00:00')
        whole = {'items': self.ITEMS + [{'name': '%s %s' % (FIRST[k % 25], LAST[k // 25]), 'month': 1 + k % 12, 'day': 3} for k in range(36)],
                 'capped': False, 'missing': [], 'woke': True, 'rounds': 30, 'ms': 40000}
        self.app.stop = threading.Event()
        logs = self.fill({**whole, 'items': whole['items'][:12], 'rounds': 2, 'ms': 3000},  # a cold start: a few, all quiet
                         {**whole, 'missing': [3, 4]}, whole)
        self.assertEqual(logs, ['facebook birthdays fill short, read again later found=10 others=8 capped=False missing=0 woke=True rounds=2 ms=3000 try=1',
                                'facebook birthdays fill short, read again later found=40 others=38 capped=False missing=2 woke=True rounds=30 ms=40000 try=2',
                                'facebook birthdays fill done found=40 others=38 capped=False missing=0 woke=True rounds=30 ms=40000 try=3'])
        self.assertEqual(self.card(sid)['others'], 38)
        with self.store.connect() as db:
            fill = fb.get(db, sid)[1]['fill']
            self.assertEqual((fill['found'], fill['capped'], fill['missing'], fill['done']), (40, False, [], True))
            self.assertEqual(fb.to_fill(db), [])
        self.step(sid, 'save')
        with self.store.connect() as db:
            data = fb.get(db, sid)[1]
            self.assertEqual((data['found'], data['fill']['found'], len(data['others'])), (40, 40, 38))  # the report stays on Save
            self.assertEqual(fb.to_fill(db), [])

    def test_reads_that_stay_short_stop_after_a_few_and_keep_the_most_they_found(self):
        sid = self.old('saved')
        self.app.stop = threading.Event()
        logs = self.fill({'items': self.ITEMS, 'capped': True}, {'items': self.ITEMS[:2], 'woke': False}, {'items': self.ITEMS[:3], 'missing': [5]},
                         {'items': self.ITEMS})
        self.assertEqual(len(logs), fb.FILL_READS)
        self.assertTrue(logs[-1].startswith('facebook birthdays fill short, kept as it is found=3 others=2 '), logs[-1])
        self.assertEqual(self.card(sid)['others'], 2)  # the first read's two, not the later reads' fewer
        with self.store.connect() as db:
            self.assertEqual(fb.to_fill(db), [])  # bounded: not at the next start either

    def test_a_todo_filled_short_before_gets_one_more_fill(self):
        sid, saved = self.old('preview'), self.old('saved')
        with self.store.connect() as db:  # filled before fills kept their report: one friend of the 3 its read didn't match
            for todo in (sid, saved):
                fb.put(db, todo, *fb.get(db, todo)[:1], {**fb.get(db, todo)[1], 'others': [{'name': 'Mira Holt', 'date': '1990-01-05'}], 'added': []},
                       '2026-11-09T08:00:00+00:00')
            self.assertEqual(sorted(fb.to_fill(db)), sorted([sid, saved]))  # the Save kept no count: it gets one too
        self.app.stop = threading.Event()
        self.assertEqual(len(self.fill({'items': self.ITEMS})), 2)
        self.assertEqual((self.card(sid)['others'], self.card(saved)['others']), (2, 2))
        with self.store.connect() as db:
            self.assertEqual(fb.to_fill(db), [])
            # one filled before whose others are about all its read didn't match is left as it is
            whole = {k: v for k, v in fb.get(db, sid)[1].items() if k != 'fill'}
            fb.put(db, sid, 'preview', {**whole, 'unmatched': 2}, '2026-11-09T08:00:00+00:00')
            self.assertEqual(fb.to_fill(db), [])
        self.step(sid, 'read')  # and so is a read of its own (Import again), with its report
        with self.store.connect() as db:
            self.assertEqual(fb.get(db, sid)[1]['read'], {'capped': False, 'missing': [], 'woke': True, 'rounds': 0, 'ms': 0})
            self.assertEqual(fb.to_fill(db), [])

    # Import again after Add: the to-do keeps who it added (Undo), and the read after it stays quick with every friend a
    # person with a birthday. A step after the page that goes wrong or takes too long says so and keeps the same.

    def kept(self, sid):
        with self.store.connect() as db:
            return fb.get(db, sid)[1]

    def test_import_again_keeps_who_was_added_and_undo_still_takes_them_away(self):
        sid = self.read()
        self.assertEqual(self.step(sid, 'add')['added'], 2)
        added = self.kept(sid)['added']
        self.step(sid, 'save')
        self.assertEqual(self.step(sid, 'read'), {'state': 'reading'})  # Import again
        data = self.kept(sid)
        self.assertEqual((data['added'], data['saved'], len(data['people'])), (added, 1, 1))
        view = self.card(sid)
        self.assertEqual((view['state'], view['added'], view['matched'], view['new']), ('preview', 2, 3, 0))  # theirs came from this import
        with self.assertRaises(ValueError):
            self.step(sid, 'add')  # still once
        self.assertEqual(self.step(sid, 'undo_add'), {'state': 'preview', 'undone': 2})
        self.assertEqual(set(self.people()), {'Sam Rivera', 'Pat Quinn'})

    def test_a_step_after_the_page_that_fails_or_runs_long_says_so_and_keeps_the_todo(self):
        sid = self.read()
        self.step(sid, 'add')
        added = self.kept(sid)['added']
        with patch('birthdays_facebook_app.POST_READ_SECONDS', 0), self.assertLogs('personal-assistant', 'INFO') as logs:
            self.step(sid, 'read')
        data = self.kept(sid)
        self.assertEqual((self.card(sid)['state'], data['reason'], data['added']), ('failed', 'timeout', added))
        self.assertIn('reason=timeout', logs.output[-1])
        with patch.object(fb, 'preview', side_effect=RuntimeError('boom')):
            self.step(sid, 'read')  # Try again
        data = self.kept(sid)
        self.assertEqual((data['reason'], data['added'], len(data['others'])), ('RuntimeError', added, 2))
        self.step(sid, 'read')
        self.assertEqual(self.step(sid, 'undo_add')['undone'], 2)

    def test_import_again_with_every_friend_a_person_with_a_birthday_is_quick(self):
        names = [f'{f} {m} {l}' for f in FIRST for m in FIRST[:10] for l in LAST][:1300]
        self.answer = {'items': [{'name': n, 'month': 1 + i % 12, 'day': 1 + i % 28} for i, n in enumerate(names)]}
        sid = self.read()
        self.assertEqual(self.step(sid, 'add')['added'], 1300)
        with self.store.connect() as db:  # a few the owner knew another day for, or set by hand
            nodes = {r['name']: r['id'] for r in db.execute("SELECT id,name FROM graph_nodes WHERE kind='person' AND id LIKE 'manual:%'")}
            enrichment.offer_facts(db, [([nodes[names[0]]], {'birthday': '--06-06'}, enrichment.RECORD)], 'google', NOW)
            person_birthday.set_birthday(db, nodes[names[1]], {'month': 7, 'day': 7}, NOW)
        self.build()
        scans, people_scans = [], []
        facts, owners = person_birthday._facts, birthdays.by_identifier
        with patch.object(person_birthday, '_facts', lambda db, ids=None: (scans.append(ids) if ids is None else None) or facts(db, ids)), \
                patch.object(birthdays, 'by_identifier', lambda *x, **k: people_scans.append(1) or owners(*x, **k)):
            start = time.monotonic()
            self.step(sid, 'read')  # Import again
            read = time.monotonic() - start
            view = self.card(sid)
            self.assertEqual((view['state'], view['matched'], view['new'], view['added']), ('preview', 1300, 1, 1300))
            self.assertEqual(([m['name'] for m in view['shown']], view['more']), ([names[0]], 0))  # only what Save writes
            free = []

            def fresh(db, matched, real=fb.fresh):  # the slow part runs with no write lock held: another writer gets in at once
                other = sqlite3.connect(self.store.path, timeout=0.2)
                other.isolation_level = None
                other.execute('BEGIN IMMEDIATE')
                other.execute('COMMIT')
                other.close()
                free.append(not db.in_transaction)
                return real(db, matched)
            start = time.monotonic()
            with patch.object(fb, 'fresh', fresh):
                self.assertEqual(self.step(sid, 'save')['saved'], 1)  # the one known for another day; the owner's stays
            save = time.monotonic() - start
            self.assertEqual(free, [True])  # worked out once, before the write
        self.assertLessEqual((len(scans), len(people_scans)), (2, 2))  # every birthday and every person looked at once per step
        self.assertLess(read + save, 20, f'Import again took {read:.1f} s, Save {save:.1f} s')
        with self.store.connect() as db:
            self.assertEqual(person_birthday.get(db, nodes[names[0]])['value'], '--01-01')
            self.assertEqual(person_birthday.get(db, nodes[names[1]])['value'], '--07-07')
        self.assertEqual(self.step(sid, 'undo_add')['undone'], 1300)

    def test_saving_1300_new_birthdays_holds_the_database_a_moment(self):
        names = [f'{f} {m} {l}' for f in FIRST for m in FIRST[:10] for l in LAST][:1300]
        self.answer = {'items': [{'name': n, 'month': 1 + i % 12, 'day': 1 + i % 28} for i, n in enumerate(names)]}
        sid = self.read()
        self.step(sid, 'add')
        with self.store.connect() as db:  # people in the Graph without a birthday yet
            db.execute("DELETE FROM person_facts WHERE field='birthday'")
        self.build()
        self.step(sid, 'read')
        view = self.card(sid)
        self.assertEqual((view['new'], len(view['shown']), view['more']), (1300, fb.SHOWN, 1300 - fb.SHOWN))
        held, write = [], fb.write_saved

        def timed(db, picks, stamp):
            start = time.monotonic()
            try:
                return write(db, picks, stamp)
            finally:
                held.append(time.monotonic() - start)
        start = time.monotonic()
        with patch.object(fb, 'write_saved', timed):
            self.assertEqual(self.step(sid, 'save')['saved'], 1300)
        took = time.monotonic() - start
        self.assertEqual(len(held), 1)  # one write for all of them
        self.assertLess(held[0], 3, f'the write held the database {held[0]:.2f} s')
        self.assertLess(took, 20, f'Save took {took:.1f} s')
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM person_facts WHERE field='birthday' AND source='facebook'").fetchone()[0], 1300)


if __name__ == '__main__':
    unittest.main()
