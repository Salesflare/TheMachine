"""The Birthdays template (birthdays.py, birthdays_app.py, docs/help/routines.md "Templates"): each morning a to-do per
close contact whose birthday it is, from the calendars (Google's birthday events, Outlook's Birthdays calendar), Google
contacts and Birthday fields in the Graph, once per person however many sources say so. Strangers and lists get none,
a day without birthdays makes nothing, the greeting is drafted on the channel the owner usually uses with them and
nothing is sent. Made-up people only."""
import datetime as dt
import importlib.util
import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('birthdays_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import birthdays  # noqa: E402
import person_birthday  # noqa: E402
import enrichment  # noqa: E402
import graph  # noqa: E402
import ms_graph  # noqa: E402
import routine_templates  # noqa: E402
from machine.app.workers import GOOGLE_PHOTO_LISTS  # noqa: E402
from machine.sources.calendar import calendar_event  # noqa: E402
from timeutil import local_tz  # noqa: E402

ACCOUNTS = [{'id': 'home', 'email': 'owner@mail.example', 'service': 'gmail', 'boundary': 'personal'},
            {'id': 'cal', 'email': 'owner@mail.example', 'service': 'calendar', 'boundary': 'personal'},
            {'id': 'wa', 'service': 'whatsapp', 'boundary': 'personal'},
            {'id': 'o365', 'email': 'owner@work.example', 'service': 'outlook_calendar', 'transport': 'broker', 'boundary': 'work:work.example'}]


def ago(days):
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).isoformat()


class Words(unittest.TestCase):
    def test_a_birthday_title_names_its_person(self):
        for title, birthday_event, name in (("Sam Rivera's birthday", False, 'Sam Rivera'), ('Sam Rivera’s Birthday 🎂', False, 'Sam Rivera'),
                                            ('Verjaardag van Sam Rivera', False, 'Sam Rivera'), ('Geburtstag von Sam Rivera', False, 'Sam Rivera'),
                                            ('Anniversaire de Sam Rivera', False, 'Sam Rivera'), ('Cumpleaños de Sam Rivera', False, 'Sam Rivera'),
                                            ('Sam Rivera', True, 'Sam Rivera'), ('Sam Rivera', False, None),
                                            ('Birthday party', False, None), ('Birthday party', True, None),
                                            ('Happy birthday!', True, None)):  # the owner's own
            self.assertEqual(birthdays.name_in_title(title, birthday_event), name, title)

    def test_a_kept_birthday_and_its_day(self):
        self.assertEqual(birthdays.birthday_value('1990-05-03'), (5, 3))
        self.assertEqual(birthdays.birthday_value('--05-03'), (5, 3))
        self.assertIsNone(birthdays.birthday_value('1990-13-03'))
        self.assertTrue(birthdays.on(dt.date(2027, 2, 28), (2, 29)))  # not a leap year: the 28th
        self.assertFalse(birthdays.on(dt.date(2028, 2, 28), (2, 29)))
        self.assertEqual(enrichment.clean_fact('birthday', '1990-05-03'), '1990-05-03')
        self.assertIsNone(enrichment.clean_fact('birthday', 'May 3rd'))


class Sources(unittest.TestCase):
    def test_google_birthday_events_say_so(self):
        raw = {'id': 'b1', 'summary': 'Sam Rivera', 'eventType': 'birthday', 'birthdayProperties': {'type': 'birthday', 'contact': 'people/c1'},
               'start': {'date': '2026-11-09'}, 'end': {'date': '2026-11-10'}}
        meta = calendar_event({'id': 'cal'}, raw, 'Europe/Brussels')['metadata']
        self.assertEqual((meta['event_type'], meta['birthday']), ('birthday', {'type': 'birthday'}))
        self.assertNotIn('event_type', calendar_event({'id': 'cal'}, {**raw, 'eventType': 'default'}, 'Europe/Brussels')['metadata'])

    def test_google_contacts_bring_their_birthdays_with_the_same_scope(self):
        connections = GOOGLE_PHOTO_LISTS[0]
        self.assertIn('birthdays', connections[1]['personFields'].split(','))
        self.assertEqual(connections[2], 'https://www.googleapis.com/auth/contacts')  # the scope it already had
        person = {'emailAddresses': [{'value': 'sam@mail.example'}], 'phoneNumbers': [{'canonicalForm': '+15550100'}],
                  'birthdays': [{'date': {'month': 11, 'day': 9}}]}
        self.assertIn((['email:sam@mail.example', 'wa:15550100'], {'birthday': '--11-09'}, enrichment.RECORD), enrichment.google_facts(person))
        only_phone = {'phoneNumbers': [{'canonicalForm': '+15550101'}], 'birthdays': [{'date': {'year': 1990, 'month': 3, 'day': 1}}]}
        self.assertEqual(enrichment.google_facts(only_phone), [(['wa:15550101'], {'birthday': '1990-03-01'}, enrichment.RECORD)])
        self.assertNotIn('birthday', enrichment.with_facts({}, [{'birthday': ('--11-09', 1, 'google', '2026-11-09')}]))  # kept, not on the profile

    def test_google_birthdays_read_at_run_time(self):
        day = dt.date(2026, 11, 9)
        on_day = {'start': {'date': '2026-11-09'}, 'end': {'date': '2026-11-10'}}
        main = [{**on_day, 'summary': "Sam Rivera's birthday", 'eventType': 'birthday', 'birthdayProperties': {'type': 'birthday', 'contact': 'people/c1'}},
                {**on_day, 'summary': 'Happy birthday!', 'eventType': 'birthday', 'birthdayProperties': {'type': 'self'}},
                {**on_day, 'summary': "Kim Park's anniversary", 'eventType': 'birthday', 'birthdayProperties': {'type': 'anniversary'}},
                {**on_day, 'summary': "Lou Grant's birthday", 'eventType': 'birthday', 'status': 'cancelled'},
                {'start': {'date': '2026-11-10'}, 'summary': "Ann Lee's birthday", 'eventType': 'birthday'},  # tomorrow
                {**on_day, 'summary': 'Team offsite', 'eventType': 'default'}]
        self.assertEqual(birthdays.google_birthdays(main, day), [{'name': 'Sam Rivera', 'emails': [], 'date': '2026-11-09'}])
        self.assertEqual(len(birthdays.google_birthdays(main)), 2)  # any day: the year ahead
        contact = lambda kind, **prefs: {**on_day, 'summary': 'x', 'gadget': {'preferences': {'goo.contactsEventType': kind, **prefs}}}
        book = [contact('BIRTHDAY', **{'goo.contactsFullName': 'Sam  Rivera', 'goo.contactsEmail': 'sam@mail.example'}),
                contact('ANNIVERSARY', **{'goo.contactsFullName': 'Kim Park'}), contact('SELF', **{'goo.contactsFullName': 'Owner'})]
        self.assertEqual(birthdays.google_birthdays(book, day, contacts=True), [{'name': 'Sam Rivera', 'emails': ['sam@mail.example'], 'date': '2026-11-09'}])

    def test_outlook_birthdays_calendar_is_read_with_calendars_read(self):
        self.assertEqual(ms_graph.READ['calendars.list'], ('GET', '/me/calendars', 'Calendars.Read'))
        # no scope of its own: Contacts.Read is only Outlook contacts' photos and facts (ms_photos.py)
        self.assertEqual({m for m, r in ms_graph.READ.items() if r[2] == 'Contacts.Read'}, {'contacts.list', 'contacts.photo'})


class Birthdays(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS], 'timezone': 'Europe/Brussels', 'openclaw_state': self.temp.name + '/none.sqlite'}
        self.store.accounts = self.app.config['accounts']
        self.sent, self.outlook, self.n = [], [], 0
        for name, value in (('background_pause', lambda s, **k: None), ('background_spaced', lambda s: True),
                            ('background_started', lambda s: None), ('preparation_gateway', lambda s, request: self.sent.append(request) or {}),
                            ('routine_spawn', lambda s, target, run_id: target(run_id)), ('cleanup_can_mark', lambda s, account: False)):
            owner = a.CleanupTemplate if name in vars(a.CleanupTemplate) else a.App  # the template's own, else the App's
            p = patch.object(owner, name, value); p.start(); self.addCleanup(p.stop)
        p = patch.object(ms_graph, 'call', self.graph_call); p.start(); self.addCleanup(p.stop)
        # The run's Facebook offer runs inline, with no shared browser (test_birthdays_facebook.py covers it): in a thread it
        # could still open the store while the temp dir is removed, and it would ask the desktop's own browser
        self.app.birthdays_facebook_inline = True
        p = patch.object(a.App, 'birthdays_facebook_base', lambda s: None); p.start(); self.addCleanup(p.stop)
        threads = set(threading.enumerate())
        self.addCleanup(lambda: self.assertEqual([t.name for t in set(threading.enumerate()) - threads if t.is_alive()], []))
        self.today = dt.datetime.now(local_tz()).date()
        with self.store.connect() as db:
            graph.ensure(db)

    def graph_call(self, config, credential, account, method, params=None, **kw):
        self.assertEqual(account['id'], 'o365')
        if method == 'calendars.list':
            return {'value': [{'id': 'c-main', 'name': 'Calendar'}, {'id': 'c-bday', 'name': 'Birthdays'}]}
        self.assertEqual((method, params['id']), ('calendars.view', 'c-bday'))
        return {'value': [{'subject': s} for s in self.outlook]}

    def event(self, account, kind, title, meta, at=None):
        self.n += 1
        with self.store.connect() as db:
            return db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) '
                              'VALUES(?,?,?,?,?,?,?,?,?)', (account, f's{self.n}', kind, at or ago(3), title, '', json.dumps(meta), 'h', ago(0))).lastrowid

    def person(self, node_id, name, strength, wrote=3, events=(), **info):
        with self.store.connect() as db:
            db.execute('INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,?,?,?,?,?,?)',
                       (node_id, 'person', name, strength, ago(1), 5, json.dumps({'identifiers': [node_id], 'wrote': wrote, **info})))
            for event_id in events:
                db.execute('INSERT INTO graph_events(node_id,event_id,at,direct) VALUES(?,?,?,1)', (node_id, event_id, ago(1)))

    def birthday_event(self, title, **meta):
        return self.event('cal', 'calendar.event', title, {'all_day': True, 'start': {'date': self.today.isoformat()}, **meta},
                          at=birthdays.window(self.today, local_tz())[0])

    def chat(self, jid, mine, days, group=False):
        return self.event('wa', 'whatsapp.message', 'Chat', {'chat_id': jid + ('@g.us' if group else '@s.whatsapp.net'), 'from_me': mine}, at=ago(days))

    def mail(self, to, mine, days, cc=''):
        return self.event('home', 'gmail.message', 'Hello', {'from': 'owner@mail.example' if mine else to, 'to': to if mine else 'owner@mail.example',
                                                              'cc': cc, 'labels': ['SENT'] if mine else ['INBOX']}, at=ago(days))

    def morning(self):
        self.app.action('routine_template', {'key': 'birthdays'}, owner_dashboard=True)
        self.app.routines_step()
        with self.store.connect() as db:
            todos = [dict(r) for r in db.execute("SELECT * FROM suggestions WHERE dedupe_key LIKE 'birthday:%' ORDER BY title")]
            run = dict(db.execute('SELECT * FROM routine_runs ORDER BY started_at DESC').fetchone())
        return todos, run

    def test_one_todo_per_close_contact_on_their_usual_channel_and_nothing_sent(self):
        # Sam: a close friend the owner mostly chats with one to one; a group chat and one mail don't make it the channel
        sam_chat = [self.chat('15550100', True, 30), self.chat('15550100', True, 10), self.chat('15550100', False, 5)]
        group = self.chat('15550199', True, 1, group=True)
        sam_mail = self.mail('sam@mail.example', True, 20)
        self.person('wa:15550100', 'Sam Rivera', 3.4, events=sam_chat + [group, sam_mail])
        # Ann: a regular work contact the owner mails; her birthday is on Outlook's Birthdays calendar
        ann_mail = [self.mail('ann@client.example', True, 40), self.mail('ann@client.example', False, 8),
                    self.mail('ann@client.example', True, 60, cc='kim@client.example')]
        self.person('email:ann@client.example', 'Ann Lee', 1.2, events=ann_mail)
        # Kim: a cousin (family is enough at a lower closeness), with a Birthday field the owner keeps in the Graph
        kim_chat = [self.chat('15550102', True, 90)]
        self.person('wa:15550102', 'Kim Park', 0.5, events=kim_chat, side='personal', side_why='relation')
        # Pat: a stranger whose birthday is on the calendar; Lou: close, but the owner never wrote to them one to one
        self.person('email:pat@far.example', 'Pat Doe', 0.1, events=[self.mail('pat@far.example', False, 3)])
        self.person('email:lou@mail.example', 'Lou Grant', 2.0, events=[self.mail('lou@mail.example', True, 3, cc='x@mail.example')])
        self.birthday_event('Sam Rivera', event_type='birthday', birthday={'type': 'birthday'})
        self.birthday_event("Pat Doe's birthday")
        self.birthday_event("Lou Grant's birthday")
        self.birthday_event('Happy birthday!', event_type='birthday', birthday={'type': 'self'})
        self.outlook = ["Ann Lee's birthday"]
        with self.store.connect() as db:  # Sam's contact says it too: still one to-do
            enrichment.offer_facts(db, [(['wa:15550100'], {'birthday': f'--{self.today:%m-%d}'}, enrichment.RECORD)], 'google', ago(0))
            field = db.execute("INSERT INTO crm_fields(kind,name,type,created_at) VALUES('person','Birthday','date',?)", (ago(0),)).lastrowid
            db.execute('INSERT INTO crm_values(node_id,field_id,value,set_at) VALUES(?,?,?,?)', ('wa:15550102', field, f'1990-{self.today:%m-%d}', ago(0)))
        todos, run = self.morning()
        self.assertEqual([t['title'] for t in todos], ['Wish Ann Lee a happy birthday', 'Wish Kim Park a happy birthday', 'Wish Sam Rivera a happy birthday'])
        evidence = {t['title'].split()[1]: json.loads(t['event_ids']) for t in todos}
        self.assertEqual(evidence, {'Ann': [ann_mail[1]], 'Kim': kim_chat, 'Sam': [sam_chat[-1]]})  # the latest one-to-one message there
        self.assertTrue(all(t['status'] == 'accepted' for t in todos))  # prepared ahead: the draft is written, not sent
        self.assertTrue(all(t['expires_at'] for t in todos))  # gone after the day
        self.assertEqual(run['state'], 'ready')
        self.assertIn('Sam Rivera', run['result'])
        self.assertEqual([s for s in self.sent if s.get('action') == 'start'], [])  # the run is plain code: no model turn
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM action_jobs").fetchone()[0], 0)  # nothing sent
        # Run again the same day: the same to-dos, none twice
        self.app.action('routine_run_now', {'id': run['routine_id']}, owner_dashboard=True)
        self.app.routines_step()
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM suggestions WHERE dedupe_key LIKE 'birthday:%'").fetchone()[0], 3)

    def test_a_day_without_birthdays_makes_nothing(self):
        self.person('wa:15550100', 'Sam Rivera', 3.4, events=[self.chat('15550100', True, 3)])
        self.birthday_event('Team offsite')
        with self.store.connect() as db:  # someone's birthday is known, just not today's
            other = (self.today + dt.timedelta(days=40)).strftime('--%m-%d')
            enrichment.offer_facts(db, [(['wa:15550199'], {'birthday': other}, enrichment.RECORD)], 'google', ago(0))
        todos, run = self.morning()
        self.assertEqual(todos, [])
        self.assertEqual((run['state'], run['why']), ('nothing', 'No birthdays today'))

    def test_no_birthday_info_at_all_says_so_and_what_adds_some(self):
        self.person('wa:15550100', 'Sam Rivera', 3.4, events=[self.chat('15550100', True, 3)])
        self.birthday_event('Team offsite')
        self.outlook = []
        todos, run = self.morning()
        self.assertEqual(todos, [])
        self.assertEqual((run['state'], run['why']), ('nothing', 'No birthday info yet. Add birthdays to your contacts.'))
        app, why = self.app, lambda: app.birthdays_none(self.today, local_tz())
        app.config['accounts'] = [{**x, 'transport': 'broker'} if x['id'] == 'cal' else x for x in ACCOUNTS if x['id'] != 'o365']
        self.assertEqual(why(), 'No birthday info yet. Add birthdays to your Google contacts.')  # hosted too: Google shows them on the calendar
        app.config['accounts'] = [x for x in ACCOUNTS if x['id'] in ('home', 'wa')]
        self.assertEqual(why(), 'No birthday info yet. Connect your calendar, or add a Birthday field to people in the Graph.')
        app.config['accounts'] = [x for x in ACCOUNTS if x['id'] in ('home', 'o365')]
        self.assertEqual(why(), 'No birthday info yet. Add birthdays to your Outlook contacts.')
        self.outlook = ["Ann Lee's birthday"]  # one later in the year on Outlook's Birthdays calendar: known
        self.assertEqual(why(), 'No birthdays today')
        self.outlook = []
        for found in ('calendar', 'field'):
            with self.store.connect() as db:
                if found == 'calendar':  # a birthday event on another day is info too
                    self.event('cal', 'calendar.event', 'Sam Rivera', {'all_day': True, 'event_type': 'birthday', 'birthday': {'type': 'birthday'}}, at=ago(4))
                else:
                    db.execute('DELETE FROM events WHERE kind=?', ('calendar.event',))
                    field = db.execute("INSERT INTO crm_fields(kind,name,type,created_at) VALUES('person','Verjaardag','date',?)", (ago(0),)).lastrowid
                    db.execute('INSERT INTO crm_values(node_id,field_id,value,set_at) VALUES(?,?,?,?)', ('wa:15550100', field, '1990-01-01', ago(0)))
            self.assertEqual(why(), 'No birthdays today', found)

    def test_a_first_name_alone_or_two_people_with_the_name_is_nobody(self):
        self.person('wa:15550100', 'Sam Rivera', 3.4, events=[self.chat('15550100', True, 3)])
        self.person('wa:15550103', 'Sam Rivera', 2.4, events=[self.chat('15550103', True, 3)])
        self.person('wa:15550104', 'Jo Lane', 2.4, events=[self.chat('15550104', True, 3)])
        self.birthday_event("Sam Rivera's birthday")
        self.birthday_event("Jo's birthday")
        todos, run = self.morning()
        self.assertEqual(todos, [])

    def test_google_birthdays_are_read_at_run_time_with_the_calendars_own_scope(self):
        # The calendar's sync left them out (an excluded title, or the Birthdays calendar isn't connected): read now
        for x in self.app.config['accounts']:
            if x['id'] == 'cal':
                x.update(transport='gog', excluded_title_terms=["'s birthday"])
        self.app.config['accounts'].append({'id': 'cal2', 'email': 'OWNER@mail.example', 'service': 'calendar', 'transport': 'gog'})  # the same account twice
        self.person('email:sam@mail.example', 'Sam Rivera', 3.4, events=[self.mail('sam@mail.example', True, 3)])
        self.person('wa:15550102', 'Kim Park', 2.0, events=[self.chat('15550102', True, 3)])
        self.person('email:pat@far.example', 'Pat Doe', 0.1, events=[self.mail('pat@far.example', False, 3)])
        self.person('email:lou@mail.example', 'Lou Grant', 2.0, events=[self.mail('lou@mail.example', True, 3)])
        self.person('email:ann@mail.example', 'Ann Lee', 2.0, events=[self.mail('ann@mail.example', True, 3)])
        other = self.today + dt.timedelta(days=40)
        with self.store.connect() as db:  # the owner set Lou's to another day and removed the one Ann's contact had: those stay
            person_birthday.set_birthday(db, 'email:lou@mail.example', {'month': other.month, 'day': other.day}, ago(0))
            enrichment.offer_facts(db, [(['email:ann@mail.example'], {'birthday': f'--{self.today:%m-%d}'}, enrichment.RECORD)], 'google', ago(1))
            person_birthday.set_birthday(db, 'email:ann@mail.example', {'remove': True}, ago(0))
        on_day = {'start': {'date': self.today.isoformat()}, 'end': {'date': (self.today + dt.timedelta(days=1)).isoformat()}}
        calls = []

        def read(config, account, api, version, method, params, scope):
            calls.append((account['id'], method, params['calendarId'], params.get('eventTypes'), scope))
            if params['calendarId'] == 'primary':
                return {'items': [{**on_day, 'summary': "Kim Park's birthday", 'eventType': 'birthday', 'birthdayProperties': {'type': 'birthday'}},
                                  {**on_day, 'summary': "Pat Doe's birthday", 'eventType': 'birthday', 'birthdayProperties': {'type': 'birthday'}},
                                  {**on_day, 'summary': "Lou Grant's birthday", 'eventType': 'birthday', 'birthdayProperties': {'type': 'birthday'}},
                                  {**on_day, 'summary': "Ann Lee's birthday", 'eventType': 'birthday', 'birthdayProperties': {'type': 'birthday'}}]}
            # the contacts' calendar names Sam by another name, and by the address the owner writes to
            return {'items': [{**on_day, 'summary': "Sammy R's birthday", 'gadget': {'preferences': {
                'goo.contactsEventType': 'BIRTHDAY', 'goo.contactsFullName': 'Sammy R', 'goo.contactsEmail': 'Sam@mail.example'}}}]}
        with patch('birthdays_app.gog_read', read):
            todos, run = self.morning()
        self.assertEqual([t['title'] for t in todos], ['Wish Kim Park a happy birthday', 'Wish Sam Rivera a happy birthday'])
        read_only = 'https://www.googleapis.com/auth/calendar.readonly'
        self.assertEqual(calls, [('cal', 'calendar.events.list', 'primary', 'birthday', read_only),
                                 ('cal', 'calendar.events.list', 'addressbook#contacts@group.v.calendar.google.com', None, read_only)])
        with self.store.connect() as db:  # no calendar event kept; the birthday is, on the person's page
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE kind='calendar.event'").fetchone()[0], 0)
            sam = person_birthday.get(db, 'email:sam@mail.example')
            self.assertEqual((sam['value'], sam['source']), (f'--{self.today:%m-%d}', 'google_calendar'))
            self.assertIsNone(person_birthday.get(db, 'email:pat@far.example'))  # not close: not saved
            self.assertEqual(person_birthday.get(db, 'email:lou@mail.example')['source'], 'owner')  # the owner's day wins
            self.assertIsNone(person_birthday.get(db, 'email:ann@mail.example'))  # removed stays removed
            kim = person_birthday.get(db, 'wa:15550102')
            person_birthday.set_birthday(db, 'wa:15550102', {'month': self.today.month, 'day': self.today.day, 'year': 1990}, ago(0))
        self.assertEqual(kim['source'], 'google_calendar')
        with patch('birthdays_app.gog_read', read):  # the next run doesn't save the same day again
            self.assertEqual(self.app.birthdays_save(self.app.birthdays_google(self.today, local_tz()), '32'), 0)

        def fails(*args):
            raise a.SourceError('calendar', 403)
        with patch('birthdays_app.gog_read', fails):  # a read that fails is skipped, the run still ends
            self.assertEqual(self.app.birthdays_google(self.today, local_tz()), [])

    def test_a_contact_birthday_finds_its_person_by_any_address_or_number_never_a_shared_one(self):
        # Sam goes by a second address; Kim's number was added in local form (the owner is in Belgium); Lou's with spaces
        self.person('email:sam@mail.example', 'Sam Rivera', 3.4, events=[self.mail('sam@mail.example', True, 3)],
                    emails=[{'value': 'sam@mail.example', 'by': 'mail'}, {'value': 'Sam.Rivera@Home.example', 'by': 'you'}])
        self.person('email:kim@mail.example', 'Kim Park', 2.4, events=[self.mail('kim@mail.example', True, 3)],
                    phones=[{'value': '0475 12 34 56', 'by': 'you'}])
        self.person('email:lou@mail.example', 'Lou Grant', 2.4, events=[self.mail('lou@mail.example', True, 3)],
                    phones=[{'value': '+1 (555) 010-0105', 'by': 'you'}])
        # Jo and Pat share a family number: whose birthday it is can't be told, so it is nobody's
        self.person('email:jo@mail.example', 'Jo Lane', 2.4, events=[self.mail('jo@mail.example', True, 3)], phones=[{'value': '+3225550100', 'by': 'you'}])
        self.person('email:pat@mail.example', 'Pat Lane', 0.1, phones=[{'value': '02 555 01 00', 'by': 'you'}])
        day = f'--{self.today:%m-%d}'
        with self.store.connect() as db:
            enrichment.offer_facts(db, [(['email:sam.rivera@home.example'], {'birthday': day}, enrichment.RECORD),
                                        (['wa:32475123456'], {'birthday': day}, enrichment.RECORD),
                                        (['wa:15550100105'], {'birthday': day}, enrichment.RECORD),
                                        (['wa:3225550100'], {'birthday': day}, enrichment.RECORD)], 'google', ago(0))
            found = birthdays.today(db, self.today, local_tz(), code='32')
            self.assertEqual(sorted(p['name'] for p in found), ['Kim Park', 'Lou Grant', 'Sam Rivera'])
            self.assertEqual(birthdays.person_ids('email:kim@mail.example', {'phones': [{'value': '0475 12 34 56'}]}),
                             {'email:kim@mail.example'})  # without the owner's region a local number is no one's
        self.assertEqual(self.app.birthdays_code(), '32')
        todos, run = self.morning()
        self.assertEqual(sorted(t['title'] for t in todos), ['Wish Kim Park a happy birthday', 'Wish Lou Grant a happy birthday', 'Wish Sam Rivera a happy birthday'])

    def test_offered_as_a_template(self):
        self.assertIn('birthdays', routine_templates.TEMPLATES)
        with self.store.connect() as db:
            self.assertIn('birthdays', [t['key'] for t in routine_templates.view(db, spam_needs='gmail')])


if __name__ == '__main__':
    unittest.main()
