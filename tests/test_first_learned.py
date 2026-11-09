"""Here's what I've learned (first_learned.py, App.first_look_learned): at the end of the first look, how the owner
writes, the Work people who matter most right now with what they work on together, and their usual hours, from what
the Machine already keeps (no model call); Personal people and accounts never show, nor does anyone without a real
topic. Each item is correctable, and every correction shows under Learning, Changes, with Undo. Made-up data only."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from zoneinfo import ZoneInfo

spec = importlib.util.spec_from_file_location('first_learned_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import first_learned
import learning_loop

TZ = ZoneInfo('Europe/Brussels')
MILA, JONAH, KIM, SIS, QUIET = 'email:mila@fernwave.example', 'email:jonah@halyard.example', 'email:kim@gullwing.example', 'email:sis@mail.example', 'email:old@x.example'


class FirstLearned(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.accounts = [{'id': 'gateway', 'service': 'gateway'}, {'id': 'work', 'service': 'gmail', 'scope': 'work'},
                         {'id': 'home', 'service': 'gmail', 'scope': 'personal'}]
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': self.accounts, 'review_worker': {'enabled': True}}
        # A Wednesday noon in Brussels: the owner's sent mail below falls on the weekdays before it
        self.now = dt.datetime(2026, 11, 4, 11, 0, tzinfo=dt.timezone.utc)
        self.n = 0
        with self.store.connect() as db:
            first_learned.ensure(db)
            db.execute("INSERT INTO voices(channel,text,source,ref,updated_at) VALUES('Email',?,'study','study:r1',?)",
                       ('Short and direct, gets to the point in the first line\nSigns off with "Best, A."\nWrites English and Dutch\nNo emojis', self.now.isoformat()))
            for node, name, strength, side, wrote, heard, last in ((MILA, 'Mila Novak', 3.2, 'work', 4, 5, 1), (JONAH, 'Jonah Reyes', 2.5, 'work', 2, 3, 2),
                                                                  (KIM, 'Kim Gullwing', 2.0, 'work', 0, 6, 1), (SIS, 'Sam Morgan', 4.0, 'personal', 9, 9, 1),
                                                                  (QUIET, 'Old Contact', 1.0, 'work', 3, 3, 90)):
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,?,?,?,?,?,?)",
                           (node, 'person', name, strength, (self.now - dt.timedelta(days=last)).date().isoformat(), 6,
                            json.dumps({'identifiers': [node], 'side': side, 'wrote': wrote, 'heard': heard, 'role': 'investor'})))
            # Mila: on an open project; Jonah: only a thread; Kim: never written to (one way); Sam: Personal
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES('project:1','project','Q4 renewal',2.0,?,5,'{}')",
                       (self.now.date().isoformat(),))
            db.execute("INSERT INTO graph_links(a,b,kind,strength,last_at) VALUES(?,?,'project',1.5,?)", (MILA, 'project:1', self.now.date().isoformat()))
            for node, title, account in ((JONAH, 'Re: Fwd: [Halyard] Sync delay on the EU feed', 'work'), (SIS, 'Birthday dinner', 'home'),
                                         (KIM, 'Gullwing onboarding plan', 'work'), (QUIET, 'Old thing', 'work')):
                event = self.event(account, title, days=2, db=db)
                db.execute('INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,0,1)', (node, event, self.now.isoformat()))

    def event(self, account, title, days=0, hour=None, sent=False, db=None):
        self.n += 1
        when = self.now - dt.timedelta(days=days)
        if hour is not None:  # that day, at this hour in Brussels
            local = when.astimezone(TZ).replace(hour=int(hour), minute=int(hour % 1 * 60))
            when = local.astimezone(dt.timezone.utc)
        meta = {'from': 'Alex <alex@lumenlabs.example>' if sent else 'Someone <someone@example.com>', 'labels': ['SENT'] if sent else ['INBOX']}
        if db is None:
            with self.store.connect() as db:
                return self.event(account, title, days, hour, sent, db)
        return db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) VALUES(?,?,?,?,?,?,?,'h',?)",
                          (account, f's{self.n}', 'gmail.message', when.isoformat(), title, 'Made up.', json.dumps(meta), when.isoformat())).lastrowid

    def summary(self):
        with self.store.connect() as db:
            return first_learned.summary(db, self.app.account_sides(), TZ, self.now)

    def test_work_people_with_what_they_work_on_and_the_main_voice(self):
        got = self.summary()
        self.assertEqual(got['writing'], {'channel': 'Email', 'lines': ['Short and direct, gets to the point in the first line', 'Signs off with "Best, A."',
                                                                         'Writes English and Dutch']})
        self.assertEqual([(p['name'], p['topic'], p['from']) for p in got['people']],
                         [('Mila Novak', 'Q4 renewal', 'project'), ('Jonah Reyes', 'Sync delay on the EU feed', 'thread')])
        shown = json.dumps(got)
        for never in ('Sam Morgan', 'Birthday', 'Kim', 'Old Contact', 'investor'):  # Personal, one way, gone quiet, a role
            self.assertNotIn(never, shown)
        self.assertNotIn('hours', got)  # no sent mail yet: too little to go on, so nothing

    def test_usual_hours_from_their_own_sent_work_mail(self):
        for day in range(1, 22):  # three weeks of weekdays before this Wednesday
            when = self.now - dt.timedelta(days=day)
            if when.astimezone(TZ).isoweekday() > 5:
                continue
            for hour in (8.5, 10, 13, 16, 17.5):
                self.event('work', 'Re: plan', days=day, hour=hour, sent=True)
            self.event('home', 'Re: party', days=day, hour=22, sent=True)  # a Personal mailbox: not their work hours
        for day in (4, 11):  # an email on two Saturdays doesn't make Saturday a working day
            self.event('work', 'Quick one', days=day, hour=23, sent=True)
        self.assertEqual(self.summary()['hours'], {'days': [1, 2, 3, 4, 5], 'start': '08:30', 'end': '17:30', 'messages': 77})

    def test_no_hours_from_a_few_days_or_from_mail_at_all_hours(self):
        for day in range(1, 6):  # a week only: too soon to say
            for hour in (9, 11, 14, 16):
                self.event('work', 'Re: plan', days=day, hour=hour, sent=True)
        self.assertNotIn('hours', self.summary())
        for day in range(6, 22):  # weeks of mail at every hour: no pattern
            for hour in (1, 5, 9, 13, 17, 21):
                self.event('work', 'Re: plan', days=day, hour=hour, sent=True)
        self.assertNotIn('hours', self.summary())

    def test_no_one_they_also_reach_on_a_personal_account_and_no_company_name_as_topic(self):
        with self.store.connect() as db:
            event = self.event('home', 'Saturday?', days=3, db=db)
            db.execute('INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,0,1)', (MILA, event, self.now.isoformat()))
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES('project:2','project','Halyard',3.0,?,5,'{}')",
                       (self.now.date().isoformat(),))
            db.execute("INSERT INTO graph_links(a,b,kind,strength,last_at) VALUES(?,?,'project',2.5,?)", (JONAH, 'project:2', self.now.date().isoformat()))
        self.assertEqual([(p['name'], p['topic']) for p in self.summary()['people']], [('Jonah Reyes', 'Sync delay on the EU feed')])

    def test_nothing_without_signal(self):
        with self.store.connect() as db:
            db.execute('DELETE FROM voices')
            db.execute('DELETE FROM graph_links')
            db.execute('DELETE FROM graph_events')
        self.assertIsNone(self.summary())

    def test_only_at_the_end_of_the_first_look_until_closed(self):
        self.assertIsNone(self.app.first_look_learned(self.now))  # no first look ended here
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at,detail) VALUES('first_dig_done',?,'cards')", ((self.now - dt.timedelta(hours=2)).isoformat(),))
        self.assertEqual(len(self.app.first_look_learned(self.now)['people']), 2)
        self.assertIsNone(self.app.first_look_learned(self.now + dt.timedelta(days=2)))  # a day after it ended: gone
        with self.assertRaises(ValueError):
            self.app.learned_close_action('learned_close', {})  # not from the CLI
        self.app.learned_close_action('learned_close', {}, owner_dashboard=True)
        self.assertIsNone(self.app.first_look_learned(self.now))

    def fix(self, **args):
        return self.app.learned_fix_action('learned_fix', args, owner_dashboard=True)

    def test_a_line_of_how_they_write_reworded_or_removed_with_undo(self):
        with self.assertRaises(ValueError):
            self.app.learned_fix_action('learned_fix', {'item': 'voice', 'channel': 'Email', 'line': 'No emojis', 'text': ''})
        change = self.fix(item='voice', channel='Email', line='Writes English and Dutch', text='Writes English, Dutch and French')['change']
        with self.store.connect() as db:
            voice = db.execute("SELECT text,source FROM voices WHERE channel='Email'").fetchone()
            self.assertEqual(voice['source'], 'owner')  # their own words: the learning loop leaves it alone
            self.assertIn('Writes English, Dutch and French', voice['text'])
            shown = learning_loop.recent(db)[0]
        self.assertEqual((shown['kind'], shown['channel'], shown['why']), ('voice', 'Email', first_learned.WHY))
        with self.assertRaises(ValueError):  # a line that changed since is never changed in the wrong place
            self.fix(item='voice', channel='Email', line='Writes English and Dutch', text='')
        self.store.undo_learning(change)
        with self.store.connect() as db:
            self.assertIn('Writes English and Dutch', db.execute("SELECT text FROM voices WHERE channel='Email'").fetchone()[0])
        self.fix(item='voice', channel='Email', line='No emojis', text='')
        with self.store.connect() as db:
            self.assertNotIn('No emojis', db.execute("SELECT text FROM voices WHERE channel='Email'").fetchone()[0])

    def test_what_they_work_on_becomes_a_fact_about_them(self):
        change = self.fix(item='person', id=JONAH, text='EU feed migration')['change']
        got = next(p for p in self.summary()['people'] if p['id'] == JONAH)
        self.assertEqual((got['topic'], got['from']), ('EU feed migration', 'you'))
        with self.store.connect() as db:
            fact = db.execute("SELECT f.text FROM facts f JOIN fact_about a ON a.fact_id=f.id WHERE a.node_id=? AND f.removed_at IS NULL", (JONAH,)).fetchone()
            self.assertEqual(fact[0], 'Jonah Reyes: EU feed migration')
            self.assertEqual(learning_loop.recent(db)[0]['kind'], 'fact')
        self.fix(item='person', id=JONAH, text='EU feed and invoicing')  # again: replaces the first
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM facts WHERE removed_at IS NULL AND decision_id LIKE 'learned:person:%'").fetchone()[0], 1)
        with self.store.connect() as db:
            last = learning_loop.recent(db)[0]['id']
        self.store.undo_learning(last)
        self.assertEqual(next(p for p in self.summary()['people'] if p['id'] == JONAH)['topic'], 'EU feed migration')
        self.assertTrue(change)

    def test_someone_left_off_stays_off_until_undone(self):
        change = self.fix(item='person', id=MILA, text='', shown='Mila Novak')['change']
        self.assertEqual([p['name'] for p in self.summary()['people']], ['Jonah Reyes'])
        with self.store.connect() as db:
            self.assertEqual((learning_loop.recent(db)[0]['kind'], learning_loop.recent(db)[0]['text']), ('learned', 'Mila Novak'))
        self.store.undo_learning(change)
        self.assertEqual([p['name'] for p in self.summary()['people']], ['Mila Novak', 'Jonah Reyes'])

    def test_hours_in_their_own_words_or_left_off(self):
        self.fix(item='hours', text='Usual hours: Monday to Thursday, 9:00 to 16:00')
        self.assertEqual(self.summary()['hours'], {'text': 'Usual hours: Monday to Thursday, 9:00 to 16:00', 'from': 'you'})
        change = self.fix(item='hours', text='', shown='Weekdays, 8:30 to 17:30')['change']
        self.assertNotIn('hours', self.summary())
        self.store.undo_learning(change)
        self.assertEqual(self.summary()['hours']['from'], 'you')

    def test_the_actions_are_the_owners_own(self):
        self.assertIn('learned_fix', a.OWNER_ACTIONS)
        self.assertIn('learned_close', a.OWNER_ACTIONS)
        with self.assertRaises(ValueError):
            self.app.learned_fix_action('learned_fix', {'item': 'hours', 'text': 'Nights'})

    def test_subjects_read_as_topics(self):
        self.assertEqual(first_learned.subject('RE: Fwd: [Acme] Pricing for 2027'), 'Pricing for 2027')
        self.assertIsNone(first_learned.subject('Re: 12'))
        self.assertIsNone(first_learned.subject(''))
        companies = ['larkfield', 'lumenlabs']  # theirs and the owner's: an introduction's subject says nothing yet
        self.assertFalse(first_learned._says_something('Larkfield and Lumen Labs', companies))
        self.assertTrue(first_learned._says_something('Larkfield rollout', companies))
        self.assertTrue(first_learned._says_something('Q4 at Larkfield', companies))


if __name__ == '__main__':
    unittest.main()
