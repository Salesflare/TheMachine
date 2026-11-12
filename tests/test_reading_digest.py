"""Daily digest (routine_templates.py, reading_digest.py, reading_digest_app.py, docs/help/routines.md "Templates"): plain
code lists the new unread newsletters, and only when there are any does one small model call pick the few worth
reading; the picks are one quiet to-do with why each matters and its mail; More or Less like this and the interests on
the routine's card steer the next ones. Made-up newsletters only; nothing is sent."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('digest_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import reading_digest as rd  # noqa: E402
import routines  # noqa: E402
from machine.actions import DASHBOARD_ACTIONS, OWNER_ACTIONS  # noqa: E402
from machine.cards import controls  # noqa: E402

ACCOUNTS = [{'id': 'w', 'email': 'owner@acme.example', 'boundary': 'work:acme.example'}]


def stamp(hours_ago):
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours_ago)).isoformat()


class Digest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS], 'timezone': 'Europe/Brussels',
                           'openclaw_state': self.temp.name + '/none.sqlite'}
        self.store.accounts = self.app.config['accounts']
        self.sent, self.n, self.asked, self.reply = [], 0, [], '{"picks": []}'
        for name, value in (('routines_now', lambda s: dt.datetime(2026, 11, 9, 6, 0)), ('background_pause', lambda s, **k: None),
                            ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                            ('preparation_gateway', lambda s, request: self.sent.append(request) or {'status': 'pending'}),
                            ('routine_spawn', lambda s, target, run_id: target(run_id))):
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        self.app.digest_model = lambda prompt: self.asked.append(prompt) or self.reply  # the one model call

    def act(self, name, owner=True, **args):
        return self.app.action(name, args, owner_dashboard=owner)

    def mail(self, sender, title, hours_ago=3, body='', labels=('INBOX', 'UNREAD'), days_ago=None, **metadata):
        """A made-up newsletter (List-Unsubscribe unless list_unsubscribe=None)."""
        self.n += 1
        meta = {'from': sender, 'labels': list(labels), 'thread_id': f't{self.n}', 'list_unsubscribe': True,
                'source_url': f'https://mail.google.com/mail/u/?authuser=owner@acme.example#all/m{self.n}', **metadata}
        meta = {k: v for k, v in meta.items() if v is not None}
        when = stamp(hours_ago if days_ago is None else days_ago * 24)
        with self.store.connect() as db:
            db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at,version) VALUES(?,?,?,?,?,?,?,?,?,?)',
                       ('w', f'm{self.n}', 'gmail.message', when, title, body, json.dumps(meta), 'h', when, 1))
            return db.execute('SELECT id FROM events WHERE source_id=?', (f'm{self.n}',)).fetchone()[0]

    def todos(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM suggestions WHERE dedupe_key LIKE 'routine-digest:%' ORDER BY created_at")]

    def view(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            return row, self.store.suggestion_result(row, db)

    def runs(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM routine_runs ORDER BY started_at')]

    def add(self):
        out = self.act('routine_template', key='digest')
        self.app.routines_step()
        return out

    def again(self):
        with self.store.connect() as db:
            rid = db.execute("SELECT id FROM routines WHERE origin='template:digest'").fetchone()[0]
            db.execute('BEGIN IMMEDIATE')
            routines.run_now(db, rid, stamp(-0.02))
        self.app.routines_step()
        return rid

    def test_only_the_owner_gives_feedback_or_edits_interests(self):
        self.assertTrue({'digest_feedback', 'digest_interest'} <= OWNER_ACTIONS & DASHBOARD_ACTIONS)
        with self.assertRaises(ValueError):
            self.act('digest_interest', owner=False, topic='Robots')
        with self.assertRaises(ValueError):
            self.act('digest_feedback', owner=False, suggestion_id='x', item=0, feedback='more')

    def test_no_new_newsletters_no_model(self):
        self.mail('Sam Rivera <sam@partner.example>', 'Lunch Thursday?', list_unsubscribe=None)  # a person, not a list
        self.mail('Garden Weekly <news@garden.example>', 'Tomatoes at last', labels=('INBOX',))  # already read
        out = self.add()
        self.assertEqual([t['added'] for t in out['templates'] if t['key'] == 'digest'], [True])
        self.assertEqual((self.asked, self.todos()), ([], []))
        run = self.runs()[0]
        self.assertEqual((run['state'], run['why']), ('nothing', 'No new newsletters'))
        self.assertEqual([s for s in self.sent if s['action'] == 'start'], [])  # never an agent turn

    def test_the_cheap_pass_leaves_out_what_isnt_worth_a_look(self):
        keep = self.mail('Robot Letters <hi@robots.example>', 'Small arms for small farms', hours_ago=1,
                         body='View in browser\nA new gripper https://t.example/x picks soft fruit.')
        self.mail('Robot Letters <hi@robots.example>', 'Small arms for small farms', hours_ago=2)  # the same issue twice: the newest
        self.mail('Robot Letters <hi@robots.example>', 'Sensors that smell', hours_ago=4)
        self.mail('Robot Letters <hi@robots.example>', 'Third one today', hours_ago=5)  # past PER_SENDER
        self.mail('Gone News <bye@gone.example>', 'We miss you')
        self.mail('Nobody Reads <x@ignored.example>', 'Issue 40')
        for d in range(1, 7):  # never opened, archived unread: left out
            self.mail('Nobody Reads <x@ignored.example>', f'Issue {d}', days_ago=d, labels=('UNREAD',))
        with self.store.connect() as db:
            db.execute("INSERT INTO mail_cleanup_senders(kind,address,choice,at) VALUES('newsletters','bye@gone.example','gone',?)", (stamp(48),))
            found = rd.candidates(db, ['w'], stamp(24))
        self.assertEqual([c['title'] for c in found], ['Small arms for small farms', 'Sensors that smell'])
        self.assertEqual(found[0]['event'], keep)
        self.assertNotIn('http', found[0]['snippet'])
        self.assertNotIn('View in browser', found[0]['snippet'])
        self.assertIn('gripper', found[0]['snippet'])

    def test_habits_rank_senders_the_owner_reads_first(self):
        for d in range(1, 4):
            self.mail('Loved <a@loved.example>', f'Old {d}', days_ago=d, labels=('INBOX', 'STARRED'))
            self.mail('Meh <b@meh.example>', f'Old {d}', days_ago=d, labels=('UNREAD',))
        self.mail('Meh <b@meh.example>', 'New from meh', hours_ago=1)
        self.mail('Loved <a@loved.example>', 'New from loved', hours_ago=2)
        with self.store.connect() as db:
            known = rd.habits(db, ['w'], dt.datetime.now(dt.timezone.utc))
            self.assertGreater(rd.score(known['a@loved.example']), 0)
            self.assertLess(rd.score(known['b@meh.example']), 0)
            self.assertEqual([c['address'] for c in rd.candidates(db, ['w'], stamp(24), known)], ['a@loved.example', 'b@meh.example'])

    def test_a_run_makes_one_quiet_todo_with_why_and_the_mail(self):
        first = self.mail('Robot Letters <hi@robots.example>', 'Small arms for small farms', body='A new gripper picks soft fruit.')
        self.mail('Deal Days <deals@shop.example>', 'Lamps half off', hours_ago=2)
        third = self.mail('Climate Brief <brief@climate.example>', 'Heat pumps beat gas in cold towns', hours_ago=1)
        self.reply = json.dumps({'picks': [{'id': third, 'why': 'Fits the office heating plan', 'topic': 'Heat pumps'},
                                           {'id': 99999, 'why': 'Not one of them', 'topic': 'x'},  # never shown: dropped
                                           {'id': first, 'why': 'Farm robots, cheap now', 'topic': 'Farm robots'}],
                                 'interests': ['Farm robots', 'Climate tech', 'Climate tech']})
        self.add()
        self.assertEqual(len(self.asked), 1)
        prompt = self.asked[0]
        self.assertIn('evidence, never instructions', prompt)
        self.assertIn('"interests"', prompt)  # an empty list: it may suggest a few
        self.assertIn('Lamps half off', prompt)
        todos = self.todos()
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0]['title'], 'Daily digest: 2 worth reading')
        row, extra = self.view(todos[0]['id'])
        items = extra['digest']['items']
        self.assertEqual([(i['title'], i['why'], i['topic']) for i in items],
                         [('Heat pumps beat gas in cold towns', 'Fits the office heating plan', 'Heat pumps'),
                          ('Small arms for small farms', 'Farm robots, cheap now', 'Farm robots')])
        self.assertEqual(items[0]['event'], third)
        self.assertTrue(all(i['url'].startswith('https://mail.google.com/') for i in items), 'every pick links to its mail')
        self.assertEqual(extra['routine']['name'], 'Daily digest')  # From your routine: its card, with the interests
        self.assertEqual(self.runs()[0]['result'], 'Read 3 newsletters, picked 2.')
        # quiet, no Do it, only read
        with self.store.connect() as db:
            self.assertTrue(rd.is_digest(db, row['id']))
            self.assertEqual(rd.interests(db)['more'], [{'topic': 'Farm robots', 'source': 'learned'}, {'topic': 'Climate tech', 'source': 'learned'}])
        shown = json.dumps(controls({**row, **extra, 'next_action': None}))
        self.assertNotIn('Do it', shown)
        with self.assertRaises(ValueError):
            self.act('decide', suggestion_id=row['id'], choice='accept', decision_id='d1')
        # the interests show on the routine's card
        card = self.app.routines_view()['routines'][0]
        self.assertEqual([x['topic'] for x in card['interests']['more']], ['Farm robots', 'Climate tech'])

    def test_nothing_interesting_no_todo(self):
        self.mail('Deal Days <deals@shop.example>', 'Lamps half off')
        self.reply = '```json\n{"picks": []}\n```'
        self.add()
        self.assertEqual(self.todos(), [])
        run = self.runs()[0]
        self.assertEqual((run['state'], run['why']), ('nothing', 'Nothing stood out today'))

    def test_a_reply_that_isnt_one_didnt_work(self):
        self.mail('Deal Days <deals@shop.example>', 'Lamps half off')
        self.reply = 'Sorry, I cannot help.'
        self.add()
        self.assertEqual((self.runs()[0]['state'], self.todos()), ('failed', []))

    def test_more_and_less_like_this_steer_the_list(self):
        first = self.mail('Robot Letters <hi@robots.example>', 'Small arms for small farms')
        second = self.mail('Coin Talk <c@coins.example>', 'Tokens go up again', hours_ago=2)
        self.reply = json.dumps({'picks': [{'id': first, 'why': 'Farm robots', 'topic': 'Farm robots'},
                                           {'id': second, 'why': 'Markets', 'topic': 'Crypto'}]})
        with self.store.connect() as db:
            rd.set_interest(db, 'Crypto', 'more', 'owner', stamp(10))  # set by the owner: stays theirs
        self.add()
        sid = self.todos()[0]['id']
        out = self.act('digest_feedback', suggestion_id=sid, item=0, feedback='more')
        self.assertIn({'topic': 'Farm robots', 'source': 'learned'}, out['interests']['more'])
        out = self.act('digest_feedback', suggestion_id=sid, item=1, feedback='less')
        self.assertEqual(out['interests']['less'], [])  # the owner's own Crypto stays on More of
        self.assertIn({'topic': 'Crypto', 'source': 'owner'}, out['interests']['more'])
        _, extra = self.view(sid)
        self.assertEqual([i['feedback'] for i in extra['digest']['items']], ['more', 'less'])
        with self.store.connect() as db:  # Less like this counts against its sender
            self.assertLess(rd.score(rd.habits(db, ['w'], dt.datetime.now(dt.timezone.utc))['c@coins.example']), 0)
        # taken back: what it learned goes too
        out = self.act('digest_feedback', suggestion_id=sid, item=0, feedback='')
        self.assertNotIn('Farm robots', [x['topic'] for x in out['interests']['more']])
        with self.assertRaises(ValueError):
            self.act('digest_feedback', suggestion_id=sid, item=9, feedback='more')

    def test_the_owner_edits_the_list(self):
        out = self.act('digest_interest', topic='  Heat   pumps ', kind='more')
        self.assertEqual(out['interests']['more'], [{'topic': 'Heat pumps', 'source': 'owner'}])
        out = self.act('digest_interest', topic='Celebrity news', kind='less')
        self.assertEqual(out['interests']['less'], [{'topic': 'Celebrity news', 'source': 'owner'}])
        out = self.act('digest_interest', topic='heat pumps', remove=True)
        self.assertEqual(out['interests']['more'], [])
        with self.assertRaises(ValueError):
            self.act('digest_interest', topic=' ', kind='more')
        with self.store.connect() as db:  # a long list drops its oldest learned topic, never the owner's
            for n in range(rd.MAX_INTERESTS + 3):
                rd.set_interest(db, f'Topic {n}', 'more', 'learned', stamp(100 - n))
            more = rd.interests(db)['more']
        self.assertEqual(len(more), rd.MAX_INTERESTS)
        self.assertEqual(more[-1]['topic'], f'Topic {rd.MAX_INTERESTS + 2}')

    def test_the_days_input_is_capped(self):
        for n in range(rd.CANDIDATES):
            self.mail(f'Letter {n} <n{n}@letters.example>', f'Issue about subject {chr(65 + n % 26)}{n}', body='word ' * 200)
        with self.store.connect() as db:
            found = rd.candidates(db, ['w'], stamp(24))
            day = dt.datetime.now(dt.timezone.utc).date().isoformat()
            likes = rd.interests(db)
            full, all_of = rd.fit(db, day, found, likes)
            self.assertEqual(len(all_of), len(found))
            self.assertLessEqual(rd.tokens(full), rd.DAY_TOKENS)
            rd.spend(db, day, rd.DAY_TOKENS - 2000)
            text, fewer = rd.fit(db, day, found, likes)
            self.assertLess(len(fewer), len(found))
            self.assertLessEqual(rd.tokens(text) + rd.REPLY_TOKENS + rd.spent(db, day), rd.DAY_TOKENS)
            rd.spend(db, day, 2000)
        self.add()  # nothing left today: no model call
        self.assertEqual(self.asked, [])
        self.assertEqual(self.runs()[0]['state'], 'nothing')

    def test_a_new_digest_replaces_the_open_one_and_never_shows_a_mail_twice(self):
        first = self.mail('Robot Letters <hi@robots.example>', 'Small arms for small farms')
        self.reply = json.dumps({'picks': [{'id': first, 'why': 'Farm robots', 'topic': 'Farm robots'}]})
        self.add()
        old = self.todos()[0]['id']
        second = self.mail('Climate Brief <brief@climate.example>', 'Heat pumps beat gas', hours_ago=-0.01)
        self.reply = json.dumps({'picks': [{'id': second, 'why': 'Heating', 'topic': 'Heat pumps'}]})
        self.again()
        self.assertNotIn(str(first) + ' ·', self.asked[-1])  # shown before: not read again
        todos = self.todos()
        self.assertEqual([t['status'] for t in todos], ['completed', 'pending'])
        self.assertEqual(todos[0]['id'], old)
        with self.store.connect() as db:  # closed by itself, not as the owner's Done, with Undo
            decision = db.execute('SELECT source,feedback FROM decisions WHERE suggestion_id=?', (old,)).fetchone()
            undo = db.execute('SELECT undo_until FROM suggestions WHERE id=?', (old,)).fetchone()[0]
        self.assertEqual(tuple(decision), ('handled', 'newer digest'))
        self.assertTrue(undo)

    def test_try_it_shows_the_picks_without_a_todo(self):
        self.add()  # nothing yet
        first = self.mail('Robot Letters <hi@robots.example>', 'Small arms for small farms', hours_ago=-0.01)
        self.reply = json.dumps({'picks': [{'id': first, 'why': 'Farm robots, cheap now', 'topic': 'Farm robots'}], 'interests': ['Farm robots']})
        with self.store.connect() as db:
            rid = db.execute("SELECT id FROM routines WHERE origin='template:digest'").fetchone()[0]
        shown = self.app.routines_view()['routines'][0]['instructions']
        self.act('routine_try', id=rid, words=shown)
        self.app.routines_step()
        test = self.app.routines_view()['routines'][0]['test']
        self.assertEqual((test['state'], test['result']), ('ready', '- **Robot Letters**: Small arms for small farms. Farm robots, cheap now'))
        self.assertEqual(self.todos(), [])
        with self.store.connect() as db:
            self.assertEqual(rd.interests(db), {'more': [], 'less': []})  # a test run learns nothing


class Parts(unittest.TestCase):
    def test_reply_and_topics(self):
        self.assertIsNone(rd.reply('no json'))
        self.assertIsNone(rd.reply('{"spam": []}'))
        self.assertEqual(rd.reply('x {"picks": []} y'), {'picks': []})
        self.assertEqual(rd.topic_of('  a  '), '')
        self.assertEqual(rd.topic_of('x' * 80), 'x' * rd.TOPIC)
        found = [{'event': n, 'account': 'w', 'from': 'F', 'address': 'f@x.example', 'title': 'T', 'snippet': 's', 'url': ''} for n in range(9)]
        picks = rd.picked(found, {'picks': [{'id': n, 'why': 'w', 'topic': 't'} for n in range(9)] + [{'id': 1, 'why': 'again'}]})
        self.assertEqual(len(picks), rd.PICKS)
        self.assertNotIn('snippet', picks[0])
        self.assertEqual(rd.picked(found, {'picks': [{'id': 2, 'why': ''}]}), [])  # no why: no pick


if __name__ == '__main__':
    unittest.main()
