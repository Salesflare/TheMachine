"""Routine suggestions from what the owner does (routine_patterns.py, routines.py, routines_app.py, docs/help/routines.md).
Plain code finds candidates in the owner's own activity: the same ask, a mail they send, newsletters and busy Slack
channels, each at least three times on a rhythm and still going. Nothing qualifies: no model call at all. The strongest
new one goes to one sorting run a day, the same run and real preview as an OpenClaw job's, and is sorted once. The
suggestion carries why as numbers for the line that says what was seen. A to-do closed on a rhythm stays recurring.py's.
All fixtures are made up."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

spec = importlib.util.spec_from_file_location('patterns_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import recurring  # noqa: E402
import routine_patterns as rp  # noqa: E402
import routines as rt  # noqa: E402

D, T = dt.date, dt.datetime
TZ = ZoneInfo('Europe/Brussels')
SESSION = 'agent:main:assistant-review-routine-'
TODAY = D(2026, 11, 9)  # a Monday
MONDAYS = [TODAY - dt.timedelta(weeks=k) for k in (4, 3, 2, 1, 0)]


def at(day, hour=9, minute=10):
    return T(day.year, day.month, day.day, hour, minute, tzinfo=TZ).astimezone(dt.timezone.utc).isoformat()


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.n = 0

    def ask(self, day, words, hour=9, chat=False):
        self.n += 1
        with self.store.connect() as db:
            sid = f'card{self.n}'
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,?,?,?,?,?)",
                       (sid, 'k' + sid, words, '', '[]', '["w"]', 'completed', at(day, hour)))
            if chat:
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)",
                           (f'd{self.n}', sid, 'other', words, 'dashboard', at(day, hour)))
            else:
                db.execute("UPDATE suggestions SET origin='owner',owner_words=? WHERE id=?", (words, sid))

    def event(self, day, kind, title, body='', hour=9, **metadata):
        self.n += 1
        with self.store.connect() as db:
            db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) VALUES(?,?,?,?,?,?,?,?,?)',
                       ('w', f's{self.n}', kind, at(day, hour), title, body, json.dumps(metadata), 'h', at(day, hour)))

    def found(self, **k):
        with self.store.connect() as db:
            return rp.candidates(db, TODAY, TZ, **k)


class Rhythm(unittest.TestCase):
    def moments(self, days):
        return [T(d.year, d.month, d.day, 9, tzinfo=TZ) for d in days]

    def test_weekly_daily_and_weekdays(self):
        self.assertEqual(rp.rhythm(self.moments(MONDAYS[-3:]), TODAY), ({'unit': 'week', 'n': 1}, MONDAYS[-3:]))
        days = [TODAY - dt.timedelta(days=k) for k in range(6, -1, -1)]
        self.assertEqual(rp.rhythm(self.moments(days), TODAY)[0], {'unit': 'day', 'n': 1})
        weekdays = [d for d in [TODAY - dt.timedelta(days=k) for k in range(10, -1, -1)] if d.weekday() < 5]
        self.assertEqual(rp.rhythm(self.moments(weekdays), TODAY)[0], {'unit': 'weekday', 'n': 1})

    def test_the_latest_run_counts_and_old_or_scattered_ones_dont(self):
        scattered = [D(2026, 8, 3), D(2026, 8, 20)] + MONDAYS[-3:]
        self.assertEqual(rp.rhythm(self.moments(scattered), TODAY)[1], MONDAYS[-3:])
        self.assertIsNone(rp.rhythm(self.moments(MONDAYS[-2:]), TODAY))  # twice is not a rhythm
        self.assertIsNone(rp.rhythm(self.moments([D(2026, 9, 7), D(2026, 9, 14), D(2026, 9, 21)]), TODAY))  # stopped weeks ago
        self.assertIsNone(rp.rhythm(self.moments([D(2026, 10, 1), D(2026, 10, 12), D(2026, 10, 15), D(2026, 11, 2)]), TODAY))


class Candidates(Base):
    def test_nothing_qualifies_on_little_or_random_activity(self):
        self.ask(MONDAYS[-1], 'Sum up the open support tickets')
        self.ask(MONDAYS[-2], 'Sum up the open support tickets')
        self.ask(D(2026, 11, 4), 'Book a table for Friday')
        self.event(TODAY, 'gmail.message', 'Hello', labels=['SENT'], to='sam@example.org')
        self.assertEqual(self.found(), [])

    def test_the_same_ask_every_monday(self):
        for i, day in enumerate(MONDAYS[1:]):
            words = 'Sum up the open support tickets from this week' if i % 2 else 'Sum up open support tickets of the week'
            self.ask(day, words, chat=i == 1)
        got = self.found()
        self.assertEqual(len(got), 1)
        c = got[0]
        self.assertEqual((c['kind'], c['rule'], c['anchor'], c['at'], c['why']),
                         ('ask', {'unit': 'week', 'n': 1}, TODAY, '08:00', {'kind': 'ask', 'n': 4}))
        self.assertTrue(c['key'].startswith('pattern:ask:'))
        self.assertIn('support tickets', c['evidence'][-1])

    def test_a_report_the_owner_sends_on_a_rhythm(self):
        for k, day in enumerate(MONDAYS[1:]):
            self.event(day, 'gmail.message', f'Weekly numbers week {40 + k}', body=f'Signups {100 + k}\nChurn 2\n[Quoted earlier messages] old',
                       hour=16, labels=['SENT'], to='Team <team@acme.example>', **({'in-reply-to': '<x@y>'} if k == 9 else {}))
        self.event(TODAY, 'gmail.message', 'Re: Weekly numbers week 44', labels=['SENT'], to='team@acme.example')  # a reply: not one
        [c] = self.found()
        self.assertEqual((c['kind'], c['at'], c['why']), ('sent', '15:00', {'kind': 'sent', 'n': 4}))
        self.assertIn('Signups 103', c['evidence'][-1])
        self.assertNotIn('old', c['evidence'][-1])

    def test_newsletters_that_keep_coming_and_promotions_apart(self):
        for k in range(6):
            day = TODAY - dt.timedelta(weeks=k, days=1)
            self.event(day, 'gmail.message', f'AI weekly #{k}', labels=['INBOX', 'UNREAD'], **{'from': 'AI Weekly <news@aiweekly.example>', 'list_unsubscribe': True})
            self.event(day, 'gmail.message', f'Tools digest {k}', labels=['INBOX'], **{'from': 'tools@digest.example', 'list_id': 'tools.digest.example'})
            self.event(day, 'gmail.message', f'Sale {k}', labels=['CATEGORY_PROMOTIONS'], **{'from': 'deals@shop.example', 'list_unsubscribe': True})
        self.event(TODAY, 'gmail.message', 'Hi', labels=['INBOX'], **{'from': 'friend@example.org'})  # a person: never
        got = self.found()
        self.assertEqual([c['key'] for c in got], ['pattern:mail:news'])  # one shop alone is no digest
        c = got[0]
        self.assertEqual((c['rule'], c['anchor'].weekday(), c['at'], c['why']), ({'unit': 'week', 'n': 1}, 4, '08:00', {'kind': 'mail', 'n': 2}))
        self.assertTrue(any('news@aiweekly.example' in line and '6 still unread' in line for line in c['evidence']))

    def test_a_busy_channel_the_owner_reads(self):
        for week in range(4):
            for i in range(12):
                self.event(TODAY - dt.timedelta(weeks=week, days=i % 5), 'slack.message', 'x', body=f'Deploy {week}-{i} done',
                           channel_id='C123', channel_name='releases', user_id='UOTHER')
            self.event(TODAY - dt.timedelta(weeks=week), 'slack.message', 'x', body='chat', channel_id='C999', channel_name='team', user_id='UOWNER')
        self.event(TODAY, 'slack.message', 'x', body='Thanks', channel_id='C123', channel_name='releases', user_id='UOWNER')
        for i in range(40):
            self.event(TODAY - dt.timedelta(days=i % 25), 'slack.message', 'x', body='hey', channel_id='D42', user_id='UOTHER')  # a DM: never
        [c] = self.found(owner_ids={'UOWNER'})
        self.assertEqual((c['key'], c['name'], c['why']), ('pattern:slack:C123', '#releases', {'kind': 'slack', 'n': 12}))

    def test_asked_before_or_a_recurring_to_do_already(self):
        for day in MONDAYS[1:]:
            self.ask(day, 'Sum up the open support tickets')
        [c] = self.found()
        self.assertEqual(self.found(skip={c['key']}), [])
        with self.store.connect() as db:
            recurring.cover(db, c['titles'], 'fact', '{"unit":"week","n":1}', TODAY.isoformat(), at(TODAY))
        self.assertEqual(self.found(), [])


def sorting_app(self):
    """An App with the Gateway stubbed (self.gateway), on this test's store and a made-up clock."""
    self.app = object.__new__(a.App); self.app.store = self.store
    self.app.config = {'accounts': [{'id': 'w', 'boundary': 'work:acme.example'}], 'timezone': 'Europe/Brussels',
                       'openclaw_state': self.temp.name + '/none.sqlite'}  # a hosted Machine: no OpenClaw jobs
    self.now = T(2026, 11, 9, 6, 0)
    self.clock = [1_000_000.0]
    for name, value in (('routines_now', lambda s: self.now), ('background_pause', lambda s, **k: None),
                        ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                        ('preparation_gateway', lambda s, request: self.gateway(request))):
        p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
    self.sent, self.answer = [], {'start': {'status': 'admitted'}, 'status': {'status': 'pending'}}


class Sorting(Base):
    def setUp(self):
        super().setUp()
        sorting_app(self)
        for day in MONDAYS[1:]:
            self.ask(day, 'Sum up the open support tickets')

    def gateway(self, request):
        self.sent.append(request)
        return self.answer.get(request['action'], {'status': 'unavailable'})

    def starts(self):
        return [s for s in self.sent if s['action'] == 'start']

    def running(self):
        with self.store.connect() as db:
            row = db.execute("SELECT id FROM routine_runs WHERE state='running'").fetchone()
            return row[0] if row else None

    def report(self, **args):
        return self.app.action('routine_result', {'_routine_session': SESSION + self.running(), **args}, owner_dashboard=False)

    def test_no_pattern_no_model_call(self):
        with self.store.connect() as db:
            db.execute('DELETE FROM suggestions')
        self.app.routines_step()
        self.assertEqual(self.starts(), [])

    def test_a_pattern_becomes_a_suggestion_with_a_real_preview_and_why(self):
        self.app.routines_step()
        [start] = self.starts()
        message = start['message']
        for said in ('Sum up the open support tickets', 'never send', 'Quality or nothing', 'standup', 'weekly on Monday'):
            self.assertIn(said, message)
        self.report(kind='routine', name='Monday support tickets', instructions='Sum up the open support tickets', text='**3 open**, 1 urgent.')
        [s] = self.app.routines_view()['suggested']
        self.assertEqual((s['name'], s['why'], s['from_openclaw'], s['at'], s['runs'][0]['result']),
                         ('Monday support', {'kind': 'ask', 'n': 4}, False, '08:00', '**3 open**, 1 urgent.'))
        self.app.action('routine_accept', {'id': s['id']}, owner_dashboard=True)
        mine = self.app.routines_view()['routines'][0]
        self.assertEqual((mine['state'], mine['rule'], mine['next_due']), ('on', {'unit': 'week', 'n': 1}, '2026-11-09'))

    def test_one_a_day_and_sorted_once(self):
        for day in MONDAYS[1:]:
            self.event(day, 'gmail.message', 'Weekly numbers', labels=['SENT'], to='team@acme.example')
        self.app.routines_step()
        self.report(kind='skip', why='Different matters each time')
        self.app._routines_jobs_at = self.app._routines_patterns_at = 0
        self.app.routines_step()
        self.assertEqual(len(self.starts()), 1)  # the next pattern waits for tomorrow
        self.app._routines_jobs_at = self.app._routines_patterns_at = 0
        with self.store.connect() as db:  # a day later
            db.execute('UPDATE routines SET created_at=?', ((dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=21)).isoformat(),))
        self.app.routines_step()
        self.assertEqual(len(self.starts()), 2)
        self.assertIn('Weekly numbers', self.starts()[1]['message'])
        with self.store.connect() as db:
            origins = [r[0] for r in db.execute('SELECT origin FROM routines ORDER BY created_at')]
        self.assertEqual([o.split(':')[1] for o in origins], ['ask', 'sent'])

    def test_a_to_do_of_the_owners_becomes_a_recurring_to_do_offer_and_is_never_offered_twice(self):
        self.app.routines_step()
        self.report(kind='todo', name='Post the weekly update')
        with self.store.connect() as db:
            offers = {r['key']: dict(r) for r in db.execute('SELECT * FROM recurring_offers')}
            recurring.find_offers(db, TODAY, at(TODAY), TZ)  # the same to-dos, closed every Monday: covered already
            again = db.execute("SELECT count(*) FROM recurring_offers WHERE status='open'").fetchone()[0]
        offer = next(o for k, o in offers.items() if k.startswith('pattern:ask:'))
        self.assertEqual((offer['source'], offer['title'], offer['status']), ('pattern', 'Post the weekly update', 'open'))
        self.assertEqual(again, 1)
        self.assertEqual(self.app.routines_view()['suggested'], [])

    def test_a_failed_run_tries_again_tomorrow_not_now(self):
        self.answer['status'] = {'status': 'ok'}  # the turn ends without a report
        for _ in range(4):
            self.app.routines_step()
        self.assertEqual(len(self.starts()), 1)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT state FROM routines").fetchone()[0], 'sorting')


class Repeats(Base):
    """Manual work the owner repeats: forwards to the same one person, and the same request answered on a rhythm."""
    def mail(self, day, title, account='home', hour=19, body='', **metadata):
        self.n += 1
        metadata.setdefault('labels', ['SENT'])
        with self.store.connect() as db:
            db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) VALUES(?,?,?,?,?,?,?,?,?)',
                       (account, f'm{self.n}', 'gmail.message', at(day, hour), title, body, json.dumps(metadata), 'h', at(day, hour)))

    def forwards(self, days, to='Sam Rivers <sam@mail.example>', account='home'):
        for k, day in enumerate(days):
            self.mail(day, f'Fwd: {"Swim club" if k % 2 else "Oakfield School"} news {k}', account,
                      body=f'See below\n---------- Forwarded message ---------\nFrom: Oakfield School <office@oakfield.example>\nTrip on day {k}',
                      to=to, **{'from': 'Alex <alex@home.example>'})

    def test_forwards_to_the_same_person_week_after_week(self):
        days = [TODAY - dt.timedelta(days=d) for d in (17, 15, 10, 8, 3, 1)]
        self.forwards(days)
        [c] = self.found()
        self.assertEqual((c['kind'], c['account'], c['rule'], c['at'], c['why']),
                         ('forward', 'home', {'unit': 'week', 'n': 1}, '08:00', {'kind': 'forward', 'n': 6, 'weeks': 3, 'to': 'Sam'}))
        self.assertTrue(c['key'].startswith('pattern:forward:'))
        self.assertIn('sam@mail.example', c['evidence'][0])
        self.assertIn('originally from Oakfield School', c['evidence'][-1])
        self.assertGreater(c['anchor'], TODAY)

    def test_weak_or_mixed_forwards_are_no_pattern(self):
        self.forwards([TODAY - dt.timedelta(days=d) for d in (15, 8, 3, 1)])  # four: not enough
        self.forwards([TODAY - dt.timedelta(days=d) for d in (6, 5, 4, 2, 1)], to='Robin <robin@mail.example>')  # one week only
        self.forwards([TODAY - dt.timedelta(days=d) for d in (17, 15, 10, 8, 3, 1)], to='sam@mail.example, kim@mail.example')  # a group
        self.forwards([TODAY - dt.timedelta(days=d) for d in (17, 15, 10, 8, 3, 1)], to='Alex <alex@home.example>')  # their own address
        for d, account in zip((17, 15, 10, 8, 3, 1), ('home', 'w') * 3):  # Work and Personal never add up
            self.forwards([TODAY - dt.timedelta(days=d)], to='Kai <kai@mail.example>', account=account)
        self.forwards([TODAY - dt.timedelta(days=d) for d in (40, 33, 26, 22, 20)], to='Lee <lee@mail.example>')  # stopped weeks ago
        self.assertEqual(self.found(), [])

    def test_a_forward_is_never_a_report_the_owner_sends(self):
        for day in MONDAYS[1:]:
            self.mail(day, 'Doorst: Weekly numbers', to='team@acme.example')
        self.assertEqual(self.found(), [])

    def test_the_same_request_answered_every_month(self):
        for k, day in enumerate((D(2026, 8, 3), D(2026, 9, 2), D(2026, 10, 1), D(2026, 11, 3))):
            for again in range(2):  # a back and forth in one thread counts once
                self.mail(day + dt.timedelta(days=again), f'Re: Timesheet approval {9 + k}/2026', 'w', hour=10, to='Pat Lane <pat@acme.example>',
                          thread_id=f't{k}', **{'in-reply-to': f'<r{k}@acme.example>'})
        self.mail(D(2026, 11, 5), 'Re: Lunch?', 'w', to='pat@acme.example', thread_id='lunch')
        [c] = self.found()
        self.assertEqual((c['kind'], c['account'], c['rule'], c['why']),
                         ('reply', 'w', {'unit': 'month', 'n': 1}, {'kind': 'reply', 'n': 4, 'to': 'Pat'}))
        self.assertEqual(c['titles'], ['timesheet approval'])

    def test_the_same_request_answered_every_quarter(self):
        for k, day in enumerate((D(2026, 2, 3), D(2026, 5, 4), D(2026, 8, 3), D(2026, 11, 2))):
            self.mail(day, 'RE: Quarterly VAT figures', 'w', to='books@accountant.example', thread_id=f'q{k}')
        [c] = self.found()
        self.assertEqual((c['rule'], c['why']), ({'unit': 'month', 'n': 3}, {'kind': 'reply', 'n': 4, 'to': 'books@accountant.example'}))


class RepeatSorting(Base):
    """A repeat goes to the same sorting run: on its own side, at most one new suggestion a week, never again after No thanks."""
    gateway, starts, running, report = Sorting.gateway, Sorting.starts, Sorting.running, Sorting.report
    mail, helper = Repeats.mail, Repeats.forwards

    def setUp(self):
        super().setUp()
        sorting_app(self)
        self.app.config['accounts'].append({'id': 'home', 'boundary': 'personal'})

    def test_forwards_become_a_personal_suggestion_with_their_evidence(self):
        self.helper([TODAY - dt.timedelta(days=d) for d in (17, 15, 10, 8, 3, 1)])
        self.app.routines_step()
        [start] = self.starts()
        for said in ('forwards these mails one by one', 'home (personal)', 'read only that account', 'Oakfield School'):
            self.assertIn(said, start['message'])
        self.report(kind='routine', name='School digest', instructions='Every Friday, sum up the school and club mails for Sam',
                    text='**Trip** on Thursday.')
        [s] = self.app.routines_view()['suggested']
        self.assertEqual(s['why'], {'kind': 'forward', 'n': 6, 'weeks': 3, 'to': 'Sam'})
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT work FROM routines').fetchone()[0], 0)

    def test_a_work_accounts_repeat_stays_work(self):
        self.helper([TODAY - dt.timedelta(days=d) for d in (17, 15, 10, 8, 3, 1)], to='Pat <pat@acme.example>', account='w')
        self.app.routines_step()
        self.assertIn('w (work)', self.starts()[0]['message'])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT work FROM routines').fetchone()[0], 1)

    def later(self, hours):
        with self.store.connect() as db:
            back = lambda s: (dt.datetime.fromisoformat(s) - dt.timedelta(hours=hours)).isoformat()  # noqa: E731
            for table, column in (('routines', 'created_at'), ('routine_runs', 'started_at'), ('routine_runs', 'finished_at')):
                for rowid, value in db.execute(f'SELECT rowid,{column} FROM {table} WHERE {column} IS NOT NULL').fetchall():
                    db.execute(f'UPDATE {table} SET {column}=? WHERE rowid=?', (back(value), rowid))
        self.app._routines_jobs_at = self.app._routines_patterns_at = 0

    def test_one_new_suggestion_a_week_and_no_thanks_is_for_good(self):
        self.helper([TODAY - dt.timedelta(days=d) for d in (17, 15, 10, 8, 3, 1)])
        for k, day in enumerate((D(2026, 8, 3), D(2026, 9, 2), D(2026, 10, 1), D(2026, 11, 3))):
            self.mail(day, f'Re: Timesheet approval {k}', 'w', to='pat@acme.example', thread_id=f't{k}')
        self.app.routines_step()
        self.report(kind='routine', name='School digest', instructions='Sum up the school mails for Sam', text='Nothing urgent.')
        self.later(30)
        self.app.routines_step()
        self.assertEqual(len(self.starts()), 1)  # a day later: still the same week
        self.later(24 * 6)
        self.app.routines_step()
        self.assertEqual(len(self.starts()), 2)  # a week later: the next one
        self.assertIn('answers the same request', self.starts()[1]['message'])
        self.report(kind='skip', why='Different matters')
        [s] = self.app.routines_view()['suggested']
        self.app.action('routine_state', {'id': s['id'], 'to': 'stop'}, owner_dashboard=True)  # No thanks
        with self.store.connect() as db:
            self.assertEqual(rp.candidates(db, TODAY, TZ, skip=rt.sorted_origins(db)), [])


if __name__ == '__main__':
    unittest.main()
