"""A person's birthday (person_birthday.py, docs/help/graph.md "Birthday"): one value per person, on their page with
where it came from, and the same one the Birthdays routine reads. The owner's word wins and stays; a month and a day
are enough, the year is optional; a Birthday date field made before is folded in; a birthday never goes to the team.
Made-up people only."""
import datetime as dt
import json
import unittest

import test_birthdays as tb
from test_birthdays import ago

import crm_fields  # noqa: E402
import enrichment  # noqa: E402
import person_birthday as pb  # noqa: E402
import shared_graph  # noqa: E402
from timeutil import local_tz  # noqa: E402

SAM = 'email:sam@mail.example'


class Values(unittest.TestCase):
    def test_a_month_and_a_day_with_an_optional_year(self):
        today = dt.date(2026, 11, 10)
        self.assertEqual(pb.clean(12, 9, today=today), '--12-09')
        self.assertEqual(pb.clean('12', '9', '1990', today=today), '1990-12-09')
        self.assertEqual(pb.clean(2, 29, today=today), '--02-29')  # a day without a year
        self.assertEqual(pb.clean(2, 29, 2024, today=today), '2024-02-29')
        for args, error in (((2, 29, 2023), 'isn’t in that month'), ((4, 31, None), 'isn’t in that month'), ((13, 1, None), 'Pick a month'),
                            ((None, 1, None), 'Pick a month'), ((5, 3, '90'), 'four digits'), ((5, 3, 2027), 'not in the future'),
                            ((5, 3, 1850), 'from 1900')):
            with self.assertRaisesRegex(ValueError, error):
                pb.clean(*args, today=today)
        self.assertEqual(pb.parts('--12-09'), {'month': 12, 'day': 9, 'year': None})
        self.assertEqual(pb.parts('1990-12-09'), {'month': 12, 'day': 9, 'year': 1990})
        self.assertIsNone(pb.parts(''))  # the owner removed it
        self.assertTrue(pb.is_name('Date of birth') and pb.is_name('Verjaardag') and not pb.is_name('Renewal'))


class OnePlace(unittest.TestCase):
    graph_call, event, person, mail = tb.Birthdays.graph_call, tb.Birthdays.event, tb.Birthdays.person, tb.Birthdays.mail

    def setUp(self):
        tb.Birthdays.setUp(self)
        self.person(SAM, 'Sam Rivera', 3.4, events=[self.mail('sam@mail.example', True, 3)],
                    phones=[{'value': '+15550100', 'by': 'you'}])

    def page(self):
        found = self.app.graph_read({'node_id': SAM, 'lines': False})
        return found.get('birthday')

    def routine(self, day):
        with self.store.connect() as db:
            return [p['name'] for p in tb.birthdays.today(db, day, local_tz())]

    def test_the_page_and_the_routine_read_the_same_birthday_and_the_owners_word_wins(self):
        self.assertIsNone(self.page())
        with self.store.connect() as db:  # a Google contact under their number, a Facebook import on the person
            enrichment.offer_facts(db, [(['wa:15550100'], {'birthday': f'--{self.today:%m-%d}'}, enrichment.RECORD)], 'google', ago(2))
        seen = self.page()
        self.assertEqual((seen['month'], seen['day'], seen['year'], seen['source']), (self.today.month, self.today.day, None, 'google'))
        self.assertEqual(self.routine(self.today), ['Sam Rivera'])
        with self.store.connect() as db:
            enrichment.offer_facts(db, [([SAM], {'birthday': '1990-12-09'}, enrichment.RECORD)], 'facebook', ago(0))
        self.assertEqual((self.page()['value'], self.page()['source']), ('1990-12-09', 'facebook'))  # the same rank: the latest
        self.assertEqual(self.routine(self.today), [])
        self.assertEqual(self.routine(dt.date(2026, 12, 9)), ['Sam Rivera'])
        # The owner corrects it: theirs wins, also over a later import
        done = self.app.action('graph_birthday', {'node_id': SAM, 'month': 3, 'day': 1, 'year': ''}, owner_dashboard=True)
        self.assertEqual(done['birthday']['value'], '--03-01')
        with self.store.connect() as db:
            enrichment.offer_facts(db, [(['wa:15550100'], {'birthday': '--07-07'}, enrichment.STATED)], 'google', ago(0))
        self.assertEqual((self.page()['value'], self.page()['source']), ('--03-01', 'owner'))
        self.assertEqual(self.routine(dt.date(2027, 3, 1)), ['Sam Rivera'])
        self.assertEqual(self.routine(dt.date(2027, 7, 7)), [])
        # Removed: gone from the page and the routine, and a contact doesn't bring it back
        self.app.action('graph_birthday', {'node_id': SAM, 'remove': True}, owner_dashboard=True)
        with self.store.connect() as db:
            enrichment.offer_facts(db, [(['wa:15550100'], {'birthday': '--07-08'}, enrichment.STATED)], 'google', ago(0))
        self.assertIsNone(self.page())
        self.assertEqual(self.routine(dt.date(2027, 7, 8)), [])
        # Set again, then removed with nothing else known: no empty mark is left
        self.app.action('graph_birthday', {'node_id': SAM, 'month': 3, 'day': 1}, owner_dashboard=True)
        with self.store.connect() as db:
            db.execute("DELETE FROM person_facts WHERE source<>'owner'")
        self.app.action('graph_birthday', {'node_id': SAM, 'remove': True}, owner_dashboard=True)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM person_facts WHERE field='birthday'").fetchone()[0], 0)

    def test_importers_offer_a_birthday_and_the_owners_word_stays(self):
        with self.store.connect() as db:
            self.assertTrue(pb.offer(db, SAM, '--12-09', 'facebook', ago(0)))
            self.assertFalse(pb.offer(db, SAM, '1990-02-30', 'facebook', ago(0)))  # not a day
            self.assertFalse(pb.offer(db, SAM, '--01-01', 'owner', ago(0)))  # only the page sets the owner's
            self.assertEqual((pb.get(db, SAM)['value'], pb.get(db, SAM)['source']), ('--12-09', 'facebook'))
        self.app.action('graph_birthday', {'node_id': SAM, 'month': 3, 'day': 1}, owner_dashboard=True)
        with self.store.connect() as db:
            self.assertFalse(pb.offer(db, SAM, '--07-07', 'google', ago(0)))
            self.assertEqual(pb.get(db, SAM)['value'], '--03-01')
            self.assertIsNone(pb.get(db, 'email:nobody@mail.example'))

    def test_a_birthday_from_the_owners_notes_shows_and_counts_and_the_owners_word_still_wins(self):
        with self.store.connect() as db:  # notes_people.py: a birthday a note gives, on the person, rank 2, by notes
            self.assertTrue(enrichment.add_fact(db, SAM, 'birthday', '1990-12-09', 2, 'notes', ago(0)))
            self.assertEqual((pb.get(db, SAM)['value'], pb.get(db, SAM)['source']), ('1990-12-09', 'notes'))
        self.assertEqual(self.routine(dt.date(2026, 12, 9)), ['Sam Rivera'])
        self.app.action('graph_birthday', {'node_id': SAM, 'month': 3, 'day': 1}, owner_dashboard=True)
        with self.store.connect() as db:
            self.assertFalse(enrichment.drop_fact(db, SAM, 'birthday', 'notes', '1990-12-09'))  # the note's Undo leaves the owner's
            self.assertFalse(enrichment.add_fact(db, SAM, 'birthday', '1991-01-01', 2, 'notes', ago(0)))
            self.assertEqual((pb.get(db, SAM)['value'], pb.get(db, SAM)['source']), ('--03-01', 'owner'))

    def test_only_the_owner_on_their_dashboard_sets_a_real_day(self):
        with self.assertRaisesRegex(ValueError, 'Only the owner'):
            self.app.action('graph_birthday', {'node_id': SAM, 'month': 3, 'day': 1}, owner_dashboard=False)
        with self.assertRaisesRegex(ValueError, 'isn’t in that month'):
            self.app.action('graph_birthday', {'node_id': SAM, 'month': 2, 'day': 30}, owner_dashboard=True)
        self.assertIsNone(self.page())

    def test_a_birthday_date_field_made_before_is_folded_in_once(self):
        with self.store.connect() as db:
            field = db.execute("INSERT INTO crm_fields(kind,name,type,created_at) VALUES('person','Birthday','date',?)", (ago(0),)).lastrowid
            other = db.execute("INSERT INTO crm_fields(kind,name,type,created_at) VALUES('person','Start date','date',?)", (ago(0),)).lastrowid
            db.execute('INSERT INTO crm_values(node_id,field_id,value,set_at) VALUES(?,?,?,?)', (SAM, field, '1988-04-02', ago(1)))
            db.execute('INSERT INTO crm_values(node_id,field_id,value,set_at) VALUES(?,?,?,?)', (SAM, other, '2020-01-06', ago(1)))
            crm_fields.ensure(db)
            self.assertEqual([f['name'] for f in crm_fields.fields(db, 'person')], ['Start date'])
            self.assertEqual(db.execute('SELECT count(*) FROM crm_values').fetchone()[0], 1)
        self.assertEqual((self.page()['value'], self.page()['source']), ('1988-04-02', 'owner'))
        with self.assertRaisesRegex(ValueError, 'built in'):
            self.app.action('graph_field_save', {'kind': 'person', 'name': 'birthday', 'type': 'text'}, owner_dashboard=True)

    def test_a_birthday_never_goes_to_the_team(self):
        with self.store.connect() as db:
            self.app.action('graph_birthday', {'node_id': SAM, 'month': 3, 'day': 1, 'year': 1990}, owner_dashboard=True)
            text = db.execute("INSERT INTO crm_fields(kind,name,type,created_at) VALUES('person','Date of birth','text',?)", (ago(0),)).lastrowid
            met = db.execute("INSERT INTO crm_fields(kind,name,type,created_at) VALUES('person','Met at','text',?)", (ago(0),)).lastrowid
            db.execute('INSERT INTO crm_values(node_id,field_id,value,set_at) VALUES(?,?,?,?)', (SAM, text, '1 March 1990', ago(0)))
            db.execute('INSERT INTO crm_values(node_id,field_id,value,set_at) VALUES(?,?,?,?)', (SAM, met, 'The fair', ago(0)))
            row = db.execute('SELECT * FROM graph_nodes WHERE id=?', (SAM,)).fetchone()
            out = crm_fields.shared(db, row)
        self.assertEqual(out['fields'], [{'name': 'Met at', 'type': 'text', 'value': 'The fair'}])
        self.assertNotIn('1990', json.dumps(out))
        came = shared_graph._clean_record({'r': 'x', 't': 'person', 'name': 'Sam', 'fields': [{'name': 'Birthday', 'type': 'date', 'value': '1990-03-01'},
                                                                                                {'name': 'Met at', 'type': 'text', 'value': 'The fair'}]})
        self.assertEqual([f['name'] for f in came['fields']], ['Met at'])  # one an older Machine sends is dropped


if __name__ == '__main__':
    unittest.main()
