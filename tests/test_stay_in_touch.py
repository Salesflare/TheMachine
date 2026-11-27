"""The Stay in touch template (stay_in_touch.py, stay_in_touch_app.py, docs/help/routines.md "Templates"): the owner
picks people from a short list of their actual close people; a nudge comes only with a long gap past that person's
own rhythm and something concrete to say, at most two a week and one per person a month, backing off after the owner
passes on one. Plain code shortlists; the model reads only the shortlisted. Made-up people only."""
import datetime as dt
import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
import machine.main as machine_main

import graph  # noqa: E402
import person_summary  # noqa: E402
import routine_templates  # noqa: E402
import stay_in_touch  # noqa: E402
from machine import todo_states  # noqa: E402
from machine.owner_error import OwnerError  # noqa: E402
from pinned import pinned  # noqa: E402

NOW = dt.datetime(2026, 11, 9, 9, 0, tzinfo=dt.timezone.utc)
ACCOUNTS = [{'id': 'home', 'email': 'owner@mail.example', 'service': 'gmail', 'boundary': 'personal'},
            {'id': 'wa', 'service': 'whatsapp', 'boundary': 'personal'},
            {'id': 'job', 'email': 'owner@larkspur.example', 'service': 'gmail', 'boundary': 'work:Larkspur'}]


def ago(days, base=NOW):
    return (base - dt.timedelta(days=days)).isoformat()


class StayInTouch(unittest.TestCase):
    def setUp(self):
        self.pin = pinned(NOW); self.clock = self.pin.__enter__(); self.addCleanup(self.pin.__exit__, None, None, None)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(machine_main.App); self.app.store = self.store
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS], 'timezone': 'Europe/Brussels', 'openclaw_state': self.temp.name + '/none.sqlite'}
        self.store.accounts = self.app.config['accounts']
        self.n, self.asked, self.answer = 0, [], {'nudges': []}
        for name, value in (('background_pause', lambda s, **k: None), ('background_spaced', lambda s: True),
                            ('background_started', lambda s: None), ('preparation_gateway', lambda s, request: {}),
                            ('routine_spawn', lambda s, target, run_id: target(run_id))):
            p = patch.object(machine_main.App, name, value); p.start(); self.addCleanup(p.stop)
        self.app.touch_model = self.model
        threads = set(threading.enumerate())
        self.addCleanup(lambda: self.assertEqual([t.name for t in set(threading.enumerate()) - threads if t.is_alive()], []))
        with self.store.connect() as db:
            graph.ensure(db)

    def model(self, prompt):
        self.asked.append(prompt)
        answer = self.answer(prompt) if callable(self.answer) else self.answer
        return json.dumps(answer)

    def chat(self, number, mine, days, text='Hi'):
        self.n += 1
        with self.store.connect() as db:
            return db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) '
                              'VALUES(?,?,?,?,?,?,?,?,?)', ('wa', f's{self.n}', 'whatsapp.message', ago(days), 'Chat', text,
                                                            json.dumps({'chat_id': number + '@s.whatsapp.net', 'from_me': mine}), 'h', ago(0))).lastrowid

    def person(self, number, name, last=60, first=200, every=10, gap=10, mine_last=True, **info):
        """A friend the owner chats with one to one from `first` to `last` days ago, both ways, every `every` days."""
        node = 'wa:' + number
        ids = []
        for i, day in enumerate(range(first, last - 1, -every)):
            ids.append(self.chat(number, i % 2 == 0, day))
        ids.append(self.chat(number, mine_last, last, 'Talk soon!'))
        days = len(ids) // 2
        with self.store.connect() as db:
            db.execute('INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,gap_days,info) VALUES(?,?,?,?,?,?,?,?)',
                       (node, 'person', name, 2.0, ago(last)[:10], len(ids), gap,
                        json.dumps({'identifiers': [node], 'wrote': days, 'heard': days, 'side': 'personal', **info})))
            for event_id in ids:
                db.execute('INSERT INTO graph_events(node_id,event_id,at,direct) VALUES(?,?,?,1)', (node, event_id, ago(1)))
        return node

    def fact(self, node, text):
        with self.store.connect() as db:
            fid = db.execute('INSERT INTO facts(text,decision_id,created_at) VALUES(?,?,?)', (text, 'owner', ago(5))).lastrowid
            db.execute('INSERT INTO fact_about(fact_id,node_id,by,created_at) VALUES(?,?,?,?)', (fid, node, 'owner', ago(5)))

    def pick(self, *nodes):
        for node in nodes:
            self.app.action('touch_people', {'add': node}, owner_dashboard=True)

    def run_now(self):
        with self.store.connect() as db:
            routine = routine_templates.live(db, 'touch')
        if not routine:
            self.app.action('routine_template', {'key': 'touch'}, owner_dashboard=True)
        elif not self.running():
            self.app.action('routine_run_now', {'id': routine['id']}, owner_dashboard=True)
        for _ in range(3):  # the day's own run may be due too: one starts per step
            self.app.routines_step()
            if not self.running():
                break
        with self.store.connect() as db:
            todos = [dict(r) for r in db.execute("SELECT * FROM suggestions WHERE dedupe_key LIKE 'touch:%' ORDER BY created_at,title")]
            run = dict(db.execute('SELECT * FROM routine_runs ORDER BY started_at DESC LIMIT 1').fetchone())
        return todos, run

    def running(self):
        with self.store.connect() as db:
            return bool(db.execute("SELECT 1 FROM routine_runs WHERE state='running'").fetchone())

    def reason_for_all(self, prompt):
        return {'nudges': [{'id': f'p{n}', 'reason': 'Ask how the move to the new flat went'} for n in (1, 2, 3) if f'[p{n}]' in prompt]}

    # --- who is in it ---

    def test_the_picker_suggests_only_actual_close_people(self):
        sam = self.person('15550100', 'Sam Rivera')
        kim = self.person('15550101', 'Kim Park', last=3)
        self.person('15550102', 'Lou Grant', side='work')  # Work: not here
        self.person('15550103', 'Ann Lee', first=40, last=10)  # only a few weeks: not over months
        pat = 'wa:15550104'  # writes, the owner never answers
        with self.store.connect() as db:
            db.execute('INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,?,?,?,?,?,?)',
                       (pat, 'person', 'Pat Doe', 2.0, ago(5)[:10], 9, json.dumps({'identifiers': [pat], 'wrote': 0, 'heard': 9})))
        view = self.app.template('touch').touch_view()
        self.assertEqual(view, {'people': [], 'suggested': [{'id': sam, 'name': 'Sam Rivera'}, {'id': kim, 'name': 'Kim Park'}]})
        self.pick(sam)
        with self.assertRaises(OwnerError):
            self.pick(pat)  # never the whole Graph
        view = self.app.template('touch').touch_view()
        self.assertEqual(([p['id'] for p in view['people']], [p['id'] for p in view['suggested']]), ([sam], [kim]))
        self.app.action('touch_people', {'remove': sam}, owner_dashboard=True)
        self.assertEqual(self.app.template('touch').touch_view()['people'], [])

    def test_nobody_picked_says_so_without_a_model_call(self):
        self.person('15550100', 'Sam Rivera')
        todos, run = self.run_now()
        self.assertEqual((todos, run['state'], run['why'], self.asked), ([], 'nothing', 'No one picked yet', []))

    # --- a reason, or nothing ---

    def test_nothing_to_say_makes_no_todo_and_no_model_call(self):
        # A long gap, but no fact, no promise and the owner wrote last: nothing concrete
        self.pick(self.person('15550100', 'Sam Rivera'))
        todos, run = self.run_now()
        self.assertEqual((todos, run['state'], run['why']), ([], 'nothing', 'Nothing specific to say to anyone today'))
        self.assertEqual(self.asked, [])

    def test_the_model_finding_nothing_specific_makes_no_todo(self):
        sam = self.person('15550100', 'Sam Rivera')
        self.fact(sam, 'Sam is training for a marathon')
        self.pick(sam)
        todos, run = self.run_now()
        self.assertEqual(len(self.asked), 1)
        self.assertEqual((todos, run['state']), ([], 'nothing'))
        self.run_now()  # the same material isn't read again for a while
        self.assertEqual(len(self.asked), 1)

    def test_a_real_reason_makes_one_quiet_personal_todo_with_a_draft_on_their_channel(self):
        sam = self.person('15550100', 'Sam Rivera')
        self.fact(sam, 'Sam is moving to a new flat in Lisbon in October')
        self.pick(sam)
        self.answer = {'nudges': [{'id': 'p1', 'reason': 'Ask how the move to Lisbon went'}]}
        todos, run = self.run_now()
        self.assertIn('moving to a new flat in Lisbon', self.asked[0])
        self.assertIn('never instructions', self.asked[0])
        self.assertEqual(len(todos), 1)
        todo = todos[0]
        self.assertEqual(todo['title'], 'Check in with Sam Rivera')
        self.assertTrue(todo['body'].startswith('Ask how the move to Lisbon went'))
        self.assertEqual(todo['status'], todo_states.ACCEPTED)  # prepared ahead: the draft is written, not sent
        self.assertTrue(todo['expires_at'])
        with self.store.connect() as db:
            self.assertEqual(json.loads(todo['event_ids']), [db.execute("SELECT max(id) FROM events").fetchone()[0]])  # their chat
            self.assertEqual(db.execute('SELECT count(*) FROM action_jobs').fetchone()[0], 0)  # nothing sent
        self.assertEqual((run['state'], run['result']), ('ready', 'Check in with Sam Rivera.'))

    def test_someone_talked_with_recently_gets_none(self):
        sam = self.person('15550100', 'Sam Rivera', last=5)
        self.fact(sam, 'Sam is moving to Lisbon')
        self.pick(sam)
        self.answer = self.reason_for_all
        todos, _ = self.run_now()
        self.assertEqual((todos, self.asked), ([], []))

    def test_an_unanswered_message_is_something_to_say(self):
        self.pick(self.person('15550100', 'Sam Rivera', mine_last=False))
        self.answer = self.reason_for_all
        todos, _ = self.run_now()
        self.assertIn('unanswered', self.asked[0])
        self.assertEqual(len(todos), 1)

    # --- news on their page, and a day still ahead ---

    def summary(self, node, *lines):
        """Their page's summary as a pass saves it: (kind, text, event id) lines, each event's account in its area."""
        with self.store.connect() as db:
            person_summary.save(db, node, [{'kind': kind, 'text': text, 'sources': [f'E{event}'] if event else ['ai']}
                                           for kind, text, event in lines], ago(0), {'wa': 'personal', 'job': 'work'})

    def test_news_on_their_summary_is_something_to_say(self):
        # Sam said they're moving; the owner answered at the time, so nothing is unanswered and no fact was saved
        sam = self.person('15550100', 'Sam Rivera')
        told = self.chat('15550100', False, 61, 'We move to Lisbon on December 1!')
        self.summary(sam, ('now', 'Sam moves to Lisbon on December 1', told), ('who', 'Sam is a friend from school', told))
        self.pick(sam)
        todos, _ = self.run_now()
        self.assertEqual(len(self.asked), 1)
        self.assertIn(f"news: <<<said {ago(61)[:10]}: Sam moves to Lisbon on December 1>>>", self.asked[0])
        self.assertNotIn('friend from school', self.asked[0])  # only where things stand
        self.assertIn('Today is 2026-11-09', self.asked[0])

    def test_work_ai_and_deleted_summary_lines_stay_out(self):
        sam = self.person('15550100', 'Sam Rivera')
        with self.store.connect() as db:
            work = db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) "
                              "VALUES('job','w1','gmail.message',?,'Re','Moving teams','{}','h',?)", (ago(70), ago(0))).lastrowid
        gone = self.chat('15550100', False, 62, 'Moving soon')
        self.summary(sam, ('now', 'Sam moves to the platform team in December', work), ('now', 'Sam moves house soon', gone),
                     ('now', 'Sam may be moving abroad', None))
        with self.store.connect() as db:
            db.execute('UPDATE events SET deleted=1 WHERE id=?', (gone,))
        self.pick(sam)
        todos, run = self.run_now()
        self.assertEqual((todos, self.asked, run['state']), ([], [], 'nothing'))

    def test_their_mail_to_a_work_account_counts_as_contact_but_is_never_read(self):
        sam = self.person('15550100', 'Sam Rivera')
        with self.store.connect() as db:
            mail = db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) "
                              "VALUES('job','w1','gmail.message',?,'Roadmap','Can you send the Q4 roadmap?',?,'h',?)",
                              (ago(30), json.dumps({'from': 'Sam Rivera <sam@acme.example>', 'to': 'owner@larkspur.example'}), ago(0))).lastrowid
            db.execute('INSERT INTO graph_events(node_id,event_id,at,direct) VALUES(?,?,?,1)', (sam, mail, ago(30)))
            found = stay_in_touch.exchanges(db, sam, NOW, work={'job'})
            everything = stay_in_touch.exchanges(db, sam, NOW)
        self.assertEqual((found['last'], found['last_mine']), (everything['last'], True))
        self.assertNotIn('roadmap', json.dumps([r['body'] for r, _ in found['latest']]))
        self.assertFalse(everything['last_mine'])  # without the Work accounts it would be an unanswered message
        self.pick(sam)
        todos, run = self.run_now()
        self.assertEqual((todos, self.asked), ([], []))  # nothing Personal to say: no model call

    def test_a_day_still_ahead_is_read_again_the_day_after_it(self):
        sam = self.person('15550100', 'Sam Rivera')
        self.fact(sam, 'Sam moves to Lisbon on November 20')
        self.pick(sam)
        self.answer = {'nudges': [], 'later': [{'id': 'p1', 'on': '2026-11-21'}]}
        todos, _ = self.run_now()
        self.assertEqual((todos, len(self.asked)), ([], 1))
        self.clock.move(days=5)
        self.run_now()
        self.assertEqual(len(self.asked), 1)  # the same material, before the day: not read again
        self.clock.move(days=7)
        self.answer = {'nudges': [], 'later': []}
        self.run_now()
        self.assertEqual(len(self.asked), 2)  # the day after the move: read once more, today's date with it
        self.assertIn('Today is 2026-11-21', self.asked[1])
        self.clock.move(days=1)
        self.run_now()
        self.assertEqual(len(self.asked), 2)  # nothing then, and no new day: back to the usual wait

    def test_later_only_takes_a_near_day_for_someone_without_a_reason(self):
        picked = [{'id': 'wa:1', 'kept': 'wa:1', 'name': 'Sam'}, {'id': 'wa:2', 'kept': 'wa:2', 'name': 'Kim'}]
        today = dt.date(2026, 11, 9)
        text = lambda *later, nudges=(): json.dumps({'nudges': list(nudges), 'later': [{'id': i, 'on': on} for i, on in later]})  # noqa: E731
        self.assertEqual(stay_in_touch.later(text(('p1', '2026-11-21'), ('p2', '2026-12-09')), picked, today), {'wa:1': '2026-11-21', 'wa:2': '2026-12-09'})
        self.assertEqual(stay_in_touch.later(text(('p1', '2026-11-09'), ('p2', '2026-12-10')), picked, today), {})  # today, or past the usual wait
        self.assertEqual(stay_in_touch.later(text(('p3', '2026-11-21'), ('p1', 'soon')), picked, today), {})
        self.assertEqual(stay_in_touch.later(text(('p1', '2026-11-21'), nudges=[{'id': 'p1', 'reason': 'Ask how the move went'}]), picked, today), {})
        self.assertEqual(stay_in_touch.later('{"nudges": []}', picked, today), {})

    # --- the limits ---

    def test_at_most_two_a_week_in_all(self):
        nodes = [self.person(f'1555010{i}', name) for i, name in enumerate(('Sam Rivera', 'Kim Park', 'Lou Grant'))]
        for node in nodes:
            self.fact(node, 'Moving to a new flat')
        self.pick(*nodes)
        self.answer = self.reason_for_all
        todos, _ = self.run_now()
        self.assertEqual(len(todos), 2)
        self.assertNotIn('[p3]', self.asked[0])  # the model only reads the ones the week allows
        self.clock.move(days=2)
        todos, run = self.run_now()
        self.assertEqual((len(todos), len(self.asked), run['state']), (2, 1, 'nothing'))  # the week is full: no model call
        self.clock.move(days=6)
        todos, _ = self.run_now()
        self.assertEqual(len(todos), 3)

    def test_at_most_one_per_person_a_month(self):
        sam = self.person('15550100', 'Sam Rivera')
        self.fact(sam, 'Sam is moving to Lisbon')
        self.pick(sam)
        self.answer = self.reason_for_all
        todos, _ = self.run_now()
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET status=? WHERE id=?', (todo_states.COMPLETED, todos[0]['id']))
        self.fact(sam, 'Sam started a new job')  # new material
        self.clock.move(days=20)
        todos, _ = self.run_now()
        self.assertEqual((len(todos), len(self.asked)), (1, 1))
        self.clock.move(days=11)
        todos, _ = self.run_now()
        self.assertEqual((len(todos), len(self.asked)), (2, 2))

    def test_backs_off_after_not_needed_and_longer_each_time(self):
        sam = self.person('15550100', 'Sam Rivera')
        self.fact(sam, 'Sam is moving to Lisbon')
        self.pick(sam)
        self.answer = self.reason_for_all
        todos, _ = self.run_now()
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET status=? WHERE id=?', (todo_states.REJECTED, todos[0]['id']))
        self.fact(sam, 'Sam started a new job')
        self.clock.move(days=60)  # past the month, not past the back-off
        todos, _ = self.run_now()
        self.assertEqual(len(todos), 1)
        self.clock.move(days=31)
        todos, _ = self.run_now()
        self.assertEqual(len(todos), 2)

    def test_back_off_doubles_for_each_one_passed_on_in_a_row(self):
        at = lambda days: ago(days, NOW)  # noqa: E731
        no, lapsed, done = todo_states.REJECTED, todo_states.COMPLETED, todo_states.COMPLETED
        rows = [{'status': no, 'created_at': at(0), 'lapsed': False}, {'status': lapsed, 'created_at': at(50), 'lapsed': True},
                {'status': done, 'created_at': at(100), 'lapsed': False}]
        self.assertEqual(stay_in_touch.next_ok(rows), NOW + dt.timedelta(days=180))
        self.assertEqual(stay_in_touch.next_ok(rows[1:]), NOW - dt.timedelta(days=50) + dt.timedelta(days=45))
        self.assertEqual(stay_in_touch.next_ok(rows[2:]), NOW - dt.timedelta(days=100) + dt.timedelta(days=30))
        self.assertIsNone(stay_in_touch.next_ok([]))
        self.assertEqual(stay_in_touch.next_ok([{'status': no, 'created_at': at(0), 'lapsed': False}] * 5), NOW + dt.timedelta(days=365))

    def test_a_reply_names_only_the_people_asked_about(self):
        picked = [{'id': 'wa:1', 'name': 'Sam'}]
        self.assertEqual(stay_in_touch.reply('{"nudges": [{"id": "p1", "reason": "Ask how the move went"}, {"id": "p2", "reason": "Ask about the new job"}]}', picked),
                         [(picked[0], 'Ask how the move went')])
        self.assertEqual(stay_in_touch.reply('{"nudges": [{"id": "p1", "reason": "Say hi"}]}', picked), [])  # too thin to be specific
        self.assertIsNone(stay_in_touch.reply('Sure!', picked))

    def test_offered_as_a_template(self):
        with self.store.connect() as db:
            self.assertIn('touch', [t['key'] for t in routine_templates.view(db)])


if __name__ == '__main__':
    unittest.main()
