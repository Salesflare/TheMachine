"""Subscriptions and trials (routine_templates.py, subscriptions.py, subscriptions_app.py, docs/help/routines.md
"Templates"): plain code finds recurring charges and trial, renewal and price notices in the mail, and only when there
are any does one small model call confirm them; what it confirms, checked against the mail, is one quiet to-do with Keep
or Cancel per row. Keep is remembered until the price changes; Cancel only hands the owner a draft or a cancel page and
never sends; a daily check warns about a charge within 7 days. Made-up mail only; nothing is sent."""
import datetime as dt
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('subs_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import routine_templates  # noqa: E402
import routines  # noqa: E402
import subscriptions as subs  # noqa: E402
from machine.actions import DASHBOARD_ACTIONS, OWNER_ACTIONS  # noqa: E402

ACCOUNTS = [{'id': 'w', 'email': 'owner@acme.example', 'boundary': 'work:acme.example'},
            {'id': 'p', 'email': 'owner@home.example', 'boundary': 'personal'}]
NOW = dt.datetime.now(dt.timezone.utc)
TODAY = NOW.date()


def day(n):
    """A date n days from today, as a mail would write it: November 17, 2026."""
    d = TODAY + dt.timedelta(days=n)
    return f'{d:%B} {d.day}, {d.year}'


class Subs(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS], 'timezone': 'Europe/Brussels',
                           'openclaw_state': self.temp.name + '/none.sqlite'}
        self.store.accounts = self.app.config['accounts']
        self.sent, self.n, self.asked, self.lie = [], 0, [], None
        for name, value in (('routines_now', lambda s: dt.datetime.now()), ('background_pause', lambda s, **k: None),
                            ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                            ('preparation_gateway', lambda s, request: self.sent.append(request) or {'status': 'pending'}),
                            ('routine_spawn', lambda s, target, run_id: target(run_id))):
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        self.app.subs_model = self.model

    def model(self, prompt):
        """A model that confirms what plain code saw, as the mail shows it; work for the work mailbox. self.lie changes
        one row's amount to one the mail never shows."""
        self.asked.append(prompt)
        rows = []
        for line in prompt.split('<<<\n', 1)[1].split('\n>>>', 1)[0].splitlines():
            c = json.loads(line)
            amount, currency = c['amount_seen'].split(' ')
            change = c['change_seen']
            if change and change.get('kind') == 'up':
                change = {'kind': 'up', 'from': change['from'], 'to': change['to']}
            rows.append({'id': c['id'], 'sure': True, 'name': c['from'].split(' <')[0], 'amount': self.lie if self.lie and c['id'] == 1 else amount,
                         'currency': currency, 'period': c['period_seen'] or 'month', 'next': c['next_seen'], 'change': change,
                         'area': 'work' if c['mailbox'] == 'work' else 'personal'})
        return json.dumps({'rows': rows})

    def act(self, name, owner=True, **args):
        return self.app.action(name, args, owner_dashboard=owner)

    def mail(self, sender, title, body='', days_ago=0, account='w', labels=('INBOX',), **metadata):
        self.n += 1
        meta = {'from': sender, 'labels': list(labels), 'thread_id': f't{self.n}', **metadata}
        when = (NOW - dt.timedelta(days=days_ago, minutes=5)).isoformat()
        with self.store.connect() as db:
            db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at,version) VALUES(?,?,?,?,?,?,?,?,?,?)',
                       (account, f'm{self.n}', 'gmail.message', when, title, body, json.dumps(meta), 'h', when, 1))
            return db.execute('SELECT id FROM events WHERE source_id=?', (f'm{self.n}',)).fetchone()[0]

    def fixture(self):
        """A monthly SaaS, a yearly one, a trial ending in 3 days, a price increase, a one-off and a newsletter."""
        for d in (75, 45, 15):  # monthly, the company's tool
            self.mail('Notely Billing <billing@mail.notely.example>', 'Your Notely receipt', f'Notely Team plan\nTotal: $12.00\nPaid by card', d)
        for d in (370, 5):  # yearly, personal
            self.mail('Cloudvault <invoices@cloudvault.example>', 'Invoice for your Cloudvault plan',
                      'Cloudvault Family, billed yearly\nAmount paid: €99.00', d, account='p')
        self.mail('Canvasly <no-reply@canvasly.example>', 'Your free trial ends in 3 days',
                  f'Your free trial of Canvasly Pro ends on {day(3)}. After that you will be charged $15.00 per month.\n'
                  'Manage or cancel: https://canvasly.example/account/cancel', 0, account='p')
        for d in (62, 31):
            self.mail('Streamly <help@streamly.example>', 'Payment received', 'Streamly Standard\nTotal €9.99', d, account='p')
        self.mail('Streamly <help@streamly.example>', 'Your price is changing',
                  f'Starting {day(10)}, your plan price will increase from €9.99 to €12.99 per month.', 3, account='p')
        self.mail('Gadget Shop <orders@gadgetshop.example>', 'Your order receipt', 'USB-C hub\nTotal: $49.00', 20, account='p')
        self.mail('SaaS Weekly <news@saasweekly.example>', 'Why subscription pricing wins',
                  'Subscription prices are going up everywhere: from $10 to $15 per month for most tools. Read on.', 2,
                  list_unsubscribe=True, labels=('INBOX', 'UNREAD'))

    def todos(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM suggestions WHERE dedupe_key LIKE 'routine-subs:%' ORDER BY created_at")]

    def view(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            return row, self.store.suggestion_result(row, db)

    def runs(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM routine_runs ORDER BY started_at')]

    def add(self):
        out = self.act('routine_template', key='subscriptions')
        self.app.routines_step()
        return out

    def scan(self, soon=False):
        with self.store.connect() as db:
            subs.ensure(db)
            return subs.scan(db, ['w', 'p'], NOW, soon)

    # --- the template --------------------------------------------------------------------------------------------

    def test_it_is_a_monthly_template_and_only_the_owner_picks(self):
        self.assertEqual(routine_templates.rule('subscriptions'), 'monthly')
        self.assertTrue({'subs_pick'} <= OWNER_ACTIONS & DASHBOARD_ACTIONS)
        with self.assertRaises(ValueError):
            self.act('subs_pick', owner=False, suggestion_id='x', item=0, choice='keep')
        for text in [routine_templates.TEMPLATES['subscriptions'][k] for k in ('name', 'what', 'words')]:
            self.assertNotIn('—', text)
        out = self.add()
        self.assertEqual([t['added'] for t in out['templates'] if t['key'] == 'subscriptions'], [True])
        with self.store.connect() as db:
            rule = json.loads(db.execute("SELECT rule FROM routines WHERE origin='template:subscriptions'").fetchone()[0])
        self.assertEqual(rule, {'unit': 'month', 'n': 1})

    # --- detection -------------------------------------------------------------------------------------------------

    def test_plain_code_finds_the_four_and_leaves_out_the_one_off_and_the_newsletter(self):
        self.fixture()
        found = {c['key']: c for c in self.scan()}
        self.assertEqual(sorted(found), ['canvasly.example', 'cloudvault.example', 'notely.example', 'streamly.example'])
        self.assertNotIn('gadgetshop.example', found)  # one receipt: a one-off purchase
        self.assertNotIn('saasweekly.example', found)  # list mail that only talks about subscriptions
        notely, cloud, trial, price = (found[k] for k in ('notely.example', 'cloudvault.example', 'canvasly.example', 'streamly.example'))
        self.assertEqual((notely['period'], str(notely['amount']), notely['currency']), ('month', '12.00', 'USD'))
        self.assertEqual((cloud['period'], str(cloud['amount']), cloud['currency']), ('year', '99.00', 'EUR'))
        self.assertGreater(cloud['next'], (TODAY + dt.timedelta(days=300)).isoformat())
        self.assertEqual((trial['change'], trial['next'], str(trial['amount'])), ({'kind': 'trial'}, (TODAY + dt.timedelta(days=3)).isoformat(), '15.00'))
        self.assertEqual(trial['link'], 'https://canvasly.example/account/cancel')
        self.assertEqual(trial['reply'], '')  # no-reply: the cancel page is the way
        self.assertEqual((price['change']['kind'], str(price['change']['from']), str(price['change']['to'])), ('up', '9.99', '12.99'))
        self.assertEqual(price['next'], (TODAY + dt.timedelta(days=10)).isoformat())
        self.assertEqual(price['reply'], 'help@streamly.example')

    def test_reading_amounts_and_dates(self):
        self.assertEqual(subs.charge('Subtotal: $10.00\nTax $2.10\nTotal: $12.10'), (subs.money('12.10'), 'USD'))
        self.assertEqual(subs.amounts('1.234,50 € a year')[0][:2], (subs.money('1234.50'), 'EUR'))
        self.assertEqual(subs.amounts('CA$ 20')[0][1], 'CAD')
        self.assertEqual(subs.merchant('Acme Tools', 'invoice+statements@stripe.com'), 'stripe.com:acme tools')
        self.assertEqual(subs.merchant('', 'billing@mail.shop.co.uk'), 'shop.co.uk')
        base = dt.date(2026, 11, 14)
        self.assertEqual([d for d, _ in subs.dates('ends on 2026-11-20, or 3 December, or Jan 2', base)],
                         [dt.date(2026, 11, 20), dt.date(2026, 12, 3), dt.date(2027, 1, 2)])
        self.assertIsNone(subs.notice('Our trial results', 'We tried a new recipe.', base))
        self.assertIsNone(subs.notice('Prices', 'Prices of fruit are going up, they say.', base))  # no amounts: no change

    def test_irregular_charges_are_no_subscription(self):
        for d in (80, 61, 9):  # 19 and 52 days apart
            self.mail('Corner Cafe <hello@cornercafe.example>', 'Your receipt', 'Total: €4.50', d)
        self.assertEqual(self.scan(), [])

    # --- a run -------------------------------------------------------------------------------------------------------

    def test_a_run_makes_one_quiet_todo_with_four_rows(self):
        self.fixture()
        self.add()
        self.assertEqual(len(self.asked), 1)  # one small model call
        self.assertNotIn('Gadget', self.asked[0]); self.assertNotIn('SaaS Weekly', self.asked[0])
        self.assertEqual([s for s in self.sent if s['action'] == 'start'], [])  # never an agent turn
        todos = self.todos()
        self.assertEqual(len(todos), 1)
        self.assertFalse(self.app.is_work_suggestion(todos[0]['id']))  # a Personal row: never a Work to-do
        row, extra = self.view(todos[0]['id'])
        names = [r['name'] for r in extra['subs']['rows']]
        self.assertEqual(sorted(names), ['Canvasly', 'Cloudvault', 'Notely Billing', 'Streamly'])
        by = {r['name']: r for r in extra['subs']['rows']}
        self.assertEqual(by['Canvasly']['change'], {'kind': 'trial'})
        on = (TODAY + dt.timedelta(days=10)).isoformat()  # the notice's date, which the model's answer can't change
        self.assertEqual(by['Streamly']['change'], {'kind': 'up', 'from': '9.99', 'to': '12.99', 'on': on})
        self.assertEqual(by['Streamly']['next'], on)
        self.assertEqual((by['Cloudvault']['period'], by['Cloudvault']['amount'], by['Cloudvault']['currency']), ('year', '99.00', 'EUR'))
        self.assertEqual((by['Notely Billing']['area'], by['Cloudvault']['area']), ('work', 'personal'))
        self.assertEqual(names[0], 'Canvasly')  # soonest charge first
        trial = next(x for x in row['body'].splitlines() if 'Canvasly' in x)  # its end and next charge, said once
        self.assertIn('a month after the trial, which ends', trial)
        self.assertNotIn('next charge', trial)
        self.assertIn('Price going up from 9.99 EUR to 12.99 EUR', row['body'])
        self.assertEqual(self.runs()[0]['state'], 'ready')

    def test_an_amount_the_mail_doesnt_show_leaves_the_row_out(self):
        self.fixture()
        self.lie = '11.00'
        self.add()
        _, extra = self.view(self.todos()[0]['id'])
        self.assertEqual(len(extra['subs']['rows']), 3)
        self.assertNotIn('Canvasly', [r['name'] for r in extra['subs']['rows']])  # id 1, the soonest: its amount was made up

    def test_not_sure_is_no_row(self):
        self.fixture()
        self.app.subs_model = lambda prompt: json.dumps({'rows': [{'id': 1, 'sure': False, 'name': 'X', 'amount': '15.00',
                                                                   'currency': 'USD', 'period': 'month', 'next': '2030-01-01'}]})
        self.add()
        self.assertEqual(self.todos(), [])
        self.assertEqual(self.runs()[0]['state'], 'nothing')

    def test_an_empty_run_makes_no_todo_and_no_model_call(self):
        self.mail('Gadget Shop <orders@gadgetshop.example>', 'Your order receipt', 'Total: $49.00', 20)
        self.mail('SaaS Weekly <news@saasweekly.example>', 'Why subscription pricing wins', 'Prices going up from $10 to $15.', 2,
                  list_unsubscribe=True)
        self.add()
        self.assertEqual((self.asked, self.todos()), ([], []))
        run = self.runs()[0]
        self.assertEqual((run['state'], run['why']), ('nothing', 'No subscriptions to look at'))

    def test_a_try_shows_its_rows_and_makes_no_todo(self):
        self.fixture()
        self.add()
        with self.store.connect() as db:
            rid = db.execute("SELECT id FROM routines WHERE origin='template:subscriptions'").fetchone()[0]
        self.act('routine_try', id=rid, words=routine_templates.TEMPLATES['subscriptions']['words'])
        self.app.routines_step()
        test = [r for r in self.runs() if r['period'].startswith('test:')][0]
        self.assertIn('Canvasly', test['result'])
        self.assertEqual(len(self.todos()), 1)

    # --- Keep and Cancel -----------------------------------------------------------------------------------------------

    def test_its_card_offers_only_done_snooze_and_not_needed(self):
        """Keep and Cancel live on the dashboard's rows: the Telegram card has no Do it, Answer or Edit, like a cleanup's."""
        from machine.cards import controls
        self.fixture()
        self.add()
        row, extra = self.view(self.todos()[0]['id'])
        shown = [b['action']['value'].rsplit(':', 1)[1] for block in controls({**row, **extra, 'next_action': None})['blocks']
                 for b in block['buttons'] if b['action']['type'] == 'callback']
        self.assertEqual(sorted(shown), ['complete', 'reject', 'snooze'])

    def test_a_pick_shows_at_once_on_the_kept_todo_list(self):
        """The to-dos' views are kept between status polls until a table they read changes (views.CARD_TABLES): a Keep
        or Cancel on a row shows on the next poll."""
        self.fixture()
        self.add()
        self.store = self.app.store = a.Store(self.store.path)  # a restart: subs_items, made by the first run, is watched now
        self.store.accounts = self.app.config['accounts']
        sid = self.todos()[0]['id']

        def listed():
            with self.store.connect() as db:
                cards = [dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())]
                self.store.card_views(db, cards, jobs=False)
                self.store.card_views(db, cards, jobs=True)
            return {r['n']: r['choice'] for r in cards[0]['subs']['rows']}
        first = listed()
        self.assertEqual(set(first.values()), {None})
        n = min(first)
        self.act('subs_pick', suggestion_id=sid, item=n, choice='keep')
        self.assertEqual(listed()[n], 'keep')

    def test_keep_is_remembered_until_the_price_changes(self):
        self.fixture()
        self.add()
        sid = self.todos()[0]['id']
        rows = self.view(sid)[1]['subs']['rows']
        notely = next(r for r in rows if r['name'] == 'Notely Billing')
        self.act('subs_pick', suggestion_id=sid, item=notely['n'], choice='keep')
        self.assertEqual(self.view(sid)[1]['subs']['rows'][notely['n']]['choice'], 'keep')
        self.assertNotIn('notely.example', [c['key'] for c in self.fresh()])  # not asked again
        self.mail('Notely Billing <billing@mail.notely.example>', 'Your Notely plan',
                  f'From {day(15)}, the Team plan price will increase from $12.00 to $14.00 per month.', 0)  # the price goes up
        self.assertIn('notely.example', [c['key'] for c in self.fresh()])
        self.act('subs_pick', suggestion_id=sid, item=notely['n'], choice=None)  # Undo forgets it
        with self.store.connect() as db:
            self.assertIsNone(db.execute("SELECT 1 FROM subs_kept WHERE key='notely.example'").fetchone())

    def fresh(self):
        with self.store.connect() as db:
            return subs.fresh(db, subs.scan(db, ['w', 'p'], NOW), today=TODAY)

    def test_cancel_drafts_and_never_sends(self):
        self.fixture()
        self.add()
        sid = self.todos()[0]['id']
        rows = {r['name']: r for r in self.view(sid)[1]['subs']['rows']}
        with patch('smtplib.SMTP') as smtp, patch('smtplib.SMTP_SSL') as smtp_ssl:
            got = self.act('subs_pick', suggestion_id=sid, item=rows['Streamly']['n'], choice='cancel')
            trial = self.act('subs_pick', suggestion_id=sid, item=rows['Canvasly']['n'], choice='cancel')
        self.assertFalse(smtp.called or smtp_ssl.called)
        self.assertEqual(got['draft']['to'], 'help@streamly.example')
        self.assertIn('Streamly', got['draft']['subject'])
        self.assertNotIn('—', got['draft']['body'])
        self.assertEqual(trial['draft'], {'link': 'https://canvasly.example/account/cancel'})  # no-reply: its cancel page only
        self.assertEqual([s for s in self.sent if s['action'] == 'start'], [])
        with self.store.connect() as db:
            row = db.execute('SELECT next_action,status FROM suggestions WHERE id=?', (sid,)).fetchone()
            self.assertEqual((row['next_action'], row['status']), (None, 'pending'))  # no draft to send waits on it
            self.assertEqual(db.execute("SELECT count(*) FROM suggestions WHERE dedupe_key NOT LIKE 'routine-subs:%'").fetchone()[0], 0)
        with self.assertRaises(ValueError):  # Do it on the to-do: never a send
            self.act('decide', suggestion_id=sid, choice='accept', decision_id='d1')
        self.assertNotIn('streamly.example', [c['key'] for c in self.fresh()])  # canceled: not asked again
        self.mail('Streamly <help@streamly.example>', 'Payment received', 'Total €12.99', -1, account='p')  # it charged again
        self.assertIn('streamly.example', [c['key'] for c in self.fresh()])

    # --- the 7-day warning -----------------------------------------------------------------------------------------

    def test_the_daily_check_warns_only_about_a_new_charge_within_7_days(self):
        for d in (75, 45, 15):
            self.mail('Notely Billing <billing@mail.notely.example>', 'Your Notely receipt', 'Total: $12.00', d)
        self.add()
        self.assertEqual(len(self.todos()), 1)
        self.assertTrue(self.app.is_work_suggestion(self.todos()[0]['id']))  # the company's tool only: Work
        asked = len(self.asked)
        self.app.subs_soon_step()  # nothing new within 7 days: no model, no to-do
        self.assertEqual((len(self.asked), len(self.todos())), (asked, 1))
        self.mail('Canvasly <no-reply@canvasly.example>', 'Your free trial ends in 3 days',
                  f'Your free trial of Canvasly Pro ends on {day(3)}. After that you will be charged $15.00 per month.', 0, account='p')
        self.app.subs_soon_step()  # checked today already
        self.assertEqual(len(self.todos()), 1)
        with self.store.connect() as db:
            db.execute("DELETE FROM subs_state")
        self.app.subs_soon_step()
        todos = self.todos()
        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[1]['title'], 'A trial or renewal charges this week')
        self.assertEqual([r['name'] for r in self.view(todos[1]['id'])[1]['subs']['rows']], ['Canvasly'])
        self.assertEqual(self.todos()[0]['status'], 'pending')  # the monthly one stays
        with self.store.connect() as db:
            db.execute("DELETE FROM subs_state")
        n = len(self.asked)
        self.app.subs_soon_step()  # shown with that date already: no second warning
        self.assertEqual((len(self.asked), len(self.todos())), (n, 2))

    def test_the_daily_check_waits_for_an_edited_or_paused_routine(self):
        self.mail('Canvasly <no-reply@canvasly.example>', 'Your free trial ends in 3 days', f'Trial ends on {day(3)}. Then $15.00 a month.', 0)
        self.add()
        n = len(self.todos())
        with self.store.connect() as db:
            db.execute("UPDATE routines SET state='paused' WHERE origin='template:subscriptions'")
            db.execute("DELETE FROM subs_state")
        self.mail('Drawbox <no-reply@drawbox.example>', 'Your trial ends soon', f'Your trial ends on {day(2)}. Then $9.00 a month.', 0)
        self.app.subs_soon_step()
        self.assertEqual(len(self.todos()), n)

    def test_copy_is_short_and_has_no_em_dash(self):
        source = Path(subs.__file__).read_text() + Path(subs.__file__).with_name('subscriptions_app.py').read_text()
        for text in re.findall(r"i18n\.t\('([^']+)'", source):
            self.assertNotIn('—', text)
            self.assertLess(len(text), 140)


if __name__ == '__main__':
    unittest.main()
