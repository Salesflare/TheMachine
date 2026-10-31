"""Recurring to-dos (recurring.py, recurring_app.py): rhythms and their dates, plain words, one open occurrence at a
time that comes on its date in the owner's timezone, missed ones that don't stack, Skip this one, change and stop, the
previous occurrence's result in the next preparation, the one-time offer, and a database from before this change."""
import datetime as dt
import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('recurring_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import recurring as r  # noqa: E402

D = dt.date
ACCOUNTS = [{'id': 'w', 'boundary': 'work:acme.example'}, {'id': 'p', 'boundary': 'personal:pat@home.example'}]


class Dates(unittest.TestCase):
    def test_monthly_keeps_its_day_and_clamps_at_month_end(self):
        rule = {'unit': 'month', 'n': 1}
        self.assertEqual([r.occurrence(rule, D(2026, 1, 31), k) for k in range(4)], [D(2026, 1, 31), D(2026, 2, 28), D(2026, 3, 31), D(2026, 4, 30)])

    def test_first_and_last_weekday_of_the_month(self):
        first = {'unit': 'month', 'n': 1, 'nth': 1}
        self.assertEqual(r.next_after(first, D(2026, 11, 2), D(2026, 11, 2)), D(2026, 12, 7))
        last = {'unit': 'month', 'n': 1, 'nth': -1}
        self.assertEqual(r.next_after(last, D(2026, 10, 30), D(2026, 10, 30)), D(2026, 11, 27))

    def test_weekdays_skip_the_weekend_and_custom_steps(self):
        self.assertEqual(r.next_after({'unit': 'weekday', 'n': 1}, D(2026, 10, 30), D(2026, 10, 30)), D(2026, 11, 2))
        self.assertEqual(r.next_after({'unit': 'week', 'n': 2}, D(2026, 10, 5), D(2026, 10, 19)), D(2026, 11, 2))
        self.assertEqual(r.next_after({'unit': 'day', 'n': 3}, D(2026, 10, 1), D(2026, 10, 2)), D(2026, 10, 4))
        self.assertEqual(r.occurrence({'unit': 'year', 'n': 1}, D(2024, 2, 29), 1), D(2025, 2, 28))

    def test_missed_counts_the_dates_that_passed(self):
        rule = {'unit': 'week', 'n': 1}
        self.assertEqual(r.missed(rule, D(2026, 10, 5), D(2026, 10, 5), D(2026, 10, 11)), 0)
        self.assertEqual(r.missed(rule, D(2026, 10, 5), D(2026, 10, 5), D(2026, 10, 20)), 2)

    def test_rules_are_checked(self):
        for bad in ({'unit': 'hour'}, {'unit': 'week', 'n': 0}, {'unit': 'month', 'nth': 5}, 'sometimes', None):
            with self.assertRaises(ValueError):
                r.clean_rule(bad)
        self.assertEqual(r.clean_rule('weekly'), {'unit': 'week', 'n': 1})


class Words(unittest.TestCase):
    today = D(2026, 10, 31)  # a Saturday

    def read(self, text):
        got = r.parse(text, self.today)
        return got and (got['rule'], got['anchor'], got['rest'])

    def test_plain_words(self):
        self.assertEqual(self.read('every first Monday of the month do payroll'), ({'unit': 'month', 'n': 1, 'nth': 1}, D(2026, 11, 2), 'Do payroll'))
        self.assertEqual(self.read('Water the plants every 3 days'), ({'unit': 'day', 'n': 3}, self.today, 'Water the plants'))
        self.assertEqual(self.read('every Friday send invoices'), ({'unit': 'week', 'n': 1}, D(2026, 11, 6), 'Send invoices'))
        self.assertEqual(self.read('Pay rent on the 1st of every month'), ({'unit': 'month', 'n': 1}, D(2026, 11, 1), 'Pay rent'))
        self.assertEqual(self.read('standup every weekday'), ({'unit': 'weekday', 'n': 1}, D(2026, 11, 2), 'Standup'))
        self.assertEqual(self.read('Board update monthly'), ({'unit': 'month', 'n': 1}, self.today, 'Board update'))
        self.assertEqual(self.read('every last Friday review the pipeline')[0], {'unit': 'month', 'n': 1, 'nth': -1})
        self.assertEqual(self.read('Elke maand facturen sturen')[0], {'unit': 'month', 'n': 1})

    def test_no_rhythm_no_repeat(self):
        for text in ('Send the weekly report', 'Monthly numbers to Sam by Friday', 'Call Sam about every detail', 'Book the trip'):
            self.assertIsNone(r.parse(text, self.today), text)

    def test_describe(self):
        self.assertEqual(r.describe({'unit': 'month', 'n': 1, 'nth': 1}, D(2026, 11, 2)), 'monthly on the first Monday')
        self.assertEqual(r.describe({'unit': 'week', 'n': 2}, D(2026, 11, 6)), 'every 2 weeks on Friday')


class Today:
    """The owner's day, moved by the test."""
    day = D(2026, 11, 2)


class Series(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS], 'timezone': 'Europe/Brussels'}
        Today.day = D(2026, 11, 2)
        patcher = patch.object(type(self.app), 'recurring_today', lambda self: Today.day)
        patcher.start(); self.addCleanup(patcher.stop)

    def act(self, name, **args):
        return self.app.action(name, args, owner_dashboard=True)

    def row(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())

    def series(self):
        with self.store.connect() as db:
            return [dict(x) for x in db.execute('SELECT * FROM recurring_series')]

    def open_cards(self):
        with self.store.connect() as db:
            return [dict(x) for x in db.execute("SELECT * FROM suggestions WHERE status NOT IN ('completed','rejected') ORDER BY created_at")]

    def done(self, sid, choice='complete'):
        self.store.decide(sid, choice, '', 'd-' + sid + choice, 'dashboard')

    def test_new_todo_with_repeats_comes_back_on_its_next_date_and_never_stacks(self):
        made = self.act('card_new', text='Do payroll', scope='work', repeat={'unit': 'month', 'n': 1, 'nth': 1})
        self.assertEqual(made['repeats']['anchor'], '2026-11-02')
        s = self.series()[0]
        self.assertEqual((s['current_id'], s['due'], s['work'], s['account_id']), (made['id'], '2026-11-02', 1, 'w'))
        # Still open: no second one, whatever the date
        Today.day = D(2026, 12, 20)
        self.assertEqual(self.app.recurring_step(), 0)
        self.assertEqual(len(self.open_cards()), 1)
        # It shows what it missed: December's first Monday passed
        with self.store.connect() as db:
            view = {'id': made['id']}
            r.annotate(db, [view], Today.day)
        self.assertEqual((view['repeats']['missed'], view['repeats']['next']), (1, '2027-01-04'))
        # Done late: the next is January's, not the missed December one
        self.done(made['id'])
        self.assertEqual(self.app.recurring_step(), 0)
        self.assertEqual(self.series()[0]['next_due'], '2027-01-04')
        Today.day = D(2027, 1, 4)
        self.assertEqual(self.app.recurring_step(), 1)
        cards = self.open_cards()
        self.assertEqual(len(cards), 1)
        nxt = cards[0]
        self.assertEqual((nxt['title'], nxt['due'], nxt['origin'], json.loads(nxt['account_ids'])), ('Do payroll', '2027-01-04', 'owner', ['w']))
        # Made by itself, sent nowhere: like New to-do, it is only on the screen
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM deliveries WHERE suggestion_id=?', (nxt['id'],)).fetchone()[0], 'not_sent')

    def test_plain_words_in_new_todo_talk_and_voice(self):
        made = self.act('card_new', text='every Friday send invoices', scope='personal')
        card = self.row(made['id'])
        self.assertEqual((card['title'], card['due'], json.loads(card['account_ids'])), ('Send invoices', '2026-11-06', ['p']))
        self.assertEqual(json.loads(self.series()[0]['rule']), {'unit': 'week', 'n': 1})
        # repeat: false keeps the words as typed
        plain = self.act('card_new', text='every Friday send invoices', repeat=False)
        self.assertEqual(self.row(plain['id'])['title'], 'every Friday send invoices')
        self.assertEqual(len(self.series()), 1)

    def test_more_repeat_change_skip_and_stop(self):
        made = self.act('card_new', text='Water the plants', due='2026-11-02')
        got = self.act('card_repeat', suggestion_id=made['id'], repeat='weekly')
        self.assertEqual(got['repeats']['rule'], {'unit': 'week', 'n': 1})
        got = self.act('card_repeat', suggestion_id=made['id'], words='repeat this every 3 days')
        self.assertEqual(got['repeats']['rule'], {'unit': 'day', 'n': 3})
        self.assertEqual(len(self.series()), 1)
        # Skip this one: not needed, and the next comes on its date
        skipped = self.act('card_repeat_skip', suggestion_id=made['id'])
        self.assertEqual((self.row(made['id'])['status'], skipped['next']), ('rejected', '2026-11-05'))
        Today.day = D(2026, 11, 5)
        self.app.recurring_step()
        second = self.open_cards()[0]
        # Snooze moves only this one; the series keeps its dates
        self.store.decide(second['id'], 'snooze', '', 'd-snz', 'dashboard', snooze_option='1w')
        self.assertEqual(self.series()[0]['due'], '2026-11-05')
        # Stop: this one stays an ordinary to-do, no next one
        self.assertIsNone(self.act('card_repeat', suggestion_id=second['id'], words='stop repeating')['repeats'])
        self.done(second['id'])
        Today.day = D(2026, 12, 1)
        self.assertEqual(self.app.recurring_step(), 0)
        self.assertEqual(self.open_cards(), [])
        with self.assertRaises(ValueError):
            self.act('card_repeat_skip', suggestion_id=second['id'])

    def test_only_the_owner_sets_repeats(self):
        made = self.act('card_new', text='Water the plants')
        for name in ('card_repeat', 'card_repeat_skip', 'recurring_offer'):
            with self.assertRaises(ValueError):
                self.app.action(name, {'suggestion_id': made['id'], 'repeat': 'daily'}, owner_dashboard=False)
        self.assertEqual(self.series(), [])

    def test_the_preparation_gets_the_previous_result(self):
        made = self.act('card_new', text='Do payroll', repeat='monthly')
        with self.store.connect() as db:
            self.assertIn('It is the first one', r.prep_lines(db, made['id']))
            db.execute("UPDATE suggestions SET body='Paid 4 people, 18,200 EUR in total. Sam joined.' WHERE id=?", (made['id'],))
        self.store.decide(made['id'], 'complete', 'Use the new bank template next time', 'd-1', 'dashboard')
        Today.day = D(2026, 12, 2)
        self.app.recurring_step()
        nxt = self.open_cards()[0]
        with self.store.connect() as db:
            lines = r.prep_lines(db, nxt['id'])
        self.assertIn('monthly on day 2', lines)
        self.assertIn('18,200 EUR', lines)
        self.assertIn('2026-11-02, done', lines)
        self.assertIn('Use the new bank template', lines)

    def test_offer_from_a_learned_note_is_asked_once_and_makes_nothing_by_itself(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO facts(text,decision_id,created_at) VALUES('Sends the board update every first Monday','x','2026-10-01T00:00:00+00:00')")
            db.execute("INSERT INTO facts(text,decision_id,created_at) VALUES('Lives in Ghent','y','2026-10-01T00:00:00+00:00')")
        self.assertEqual(self.app.recurring_offers_step(), 1)
        self.assertEqual(self.app.recurring_offers_step(), 0)  # once
        with self.store.connect() as db:
            offer = r.offer_view(db)
        self.assertEqual((offer['title'], offer['rule']), ('Sends the board update', {'unit': 'month', 'n': 1, 'nth': 1}))
        self.assertEqual(self.open_cards(), [])
        self.act('recurring_offer', key=offer['key'], choice='no')
        with self.store.connect() as db:
            self.assertIsNone(r.offer_view(db))
        self.assertEqual((self.open_cards(), self.series()), ([], []))

    def test_offer_prefers_commitments_and_skips_rules_and_ended_notes(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO facts(text,decision_id,created_at,fact_kind) VALUES('Waters the office plants every Friday','a','2026-10-01T00:00:00+00:00','fact')")
            db.execute("INSERT INTO facts(text,decision_id,created_at,fact_kind) VALUES('Runs payroll every first Monday','b','2026-10-01T00:00:00+00:00','commitment')")
            db.execute("INSERT INTO facts(text,decision_id,created_at,fact_kind,valid_until) VALUES('Sends the pilot recap every week','c','2026-10-01T00:00:00+00:00','commitment','2026-10-01')")
            db.execute("INSERT INTO facts(text,decision_id,created_at,kind) VALUES('Checks the backups every Monday','d','2026-10-01T00:00:00+00:00','draft')")
        self.assertEqual(self.app.recurring_offers_step(), 1)
        with self.store.connect() as db:
            self.assertEqual(r.offer_view(db)['title'], 'Runs payroll')

    def test_offer_from_a_rhythm_repeats_the_open_one(self):
        with self.store.connect() as db:
            for n, (day, status) in enumerate([('2026-08-03', 'completed'), ('2026-09-01', 'completed'), ('2026-10-01', 'completed'), ('2026-11-02', 'pending')]):
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,?,?,?,?,?)",
                           (f'c{n}', f'k{n}', f'Send the {day[5:7]} invoices to Acme', '', '[]', '["w"]', status, day + 'T08:00:00+00:00'))
        self.app.recurring_offers_step()
        with self.store.connect() as db:
            offer = r.offer_view(db)
        self.assertEqual((offer['source'], offer['rule'], offer['card_id']), ('rhythm', {'unit': 'month', 'n': 1}, 'c3'))
        self.act('recurring_offer', key=offer['key'], choice='yes')
        self.assertEqual(self.series()[0]['current_id'], 'c3')
        self.assertEqual(len(self.open_cards()), 1)


class OldDatabase(unittest.TestCase):
    def test_a_database_from_before_recurring_to_dos_upgrades(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'e.sqlite'
            a.Store(path)
            with sqlite3.connect(path) as db:  # the schema before this change: no recurring tables
                db.executescript('DROP TABLE recurring_series; DROP TABLE recurring_cards; DROP TABLE recurring_offers;')
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES('old','k','Old one','','[]','[\"w\"]','pending','2026-10-01T00:00:00+00:00')")
                cards = [{'id': 'old'}]
                db.row_factory = sqlite3.Row
                r.annotate(db, cards, D(2026, 11, 2))  # before the upgrade: nothing, no error
                self.assertEqual(r.offer_view(db), None)
            store = a.Store(path)
            with store.connect() as db:
                self.assertEqual({x[0] for x in db.execute("SELECT name FROM sqlite_master WHERE name LIKE 'recurring_%' AND type='table'")},
                                 {'recurring_series', 'recurring_cards', 'recurring_offers'})
                self.assertEqual(db.execute("SELECT title FROM suggestions WHERE id='old'").fetchone()[0], 'Old one')


if __name__ == '__main__':
    unittest.main()
