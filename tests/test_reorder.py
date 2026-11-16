"""Reorders (routine_templates.py, reorder.py, reorder_app.py, docs/help/routines.md "Templates"): order mail from
Shopify stores is found in plain code, one small model call judges which are order confirmations and lists their items,
everything it says is checked against the mail, and an item bought at a steady pace becomes one quiet to-do when it is
nearly due again. Its link opens the store; nothing is bought. Made-up stores and mail only; nothing is sent."""
import datetime as dt
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import machine.main as machine_main
import reorder  # noqa: E402
import routine_templates  # noqa: E402
from machine import todo_kinds  # noqa: E402
from machine.owner_error import OwnerError  # noqa: E402

ACCOUNTS = [{'id': 'w', 'email': 'owner@acme.example', 'boundary': 'work:acme.example'},
            {'id': 'p', 'email': 'owner@home.example', 'boundary': 'personal'}]
NOW = dt.datetime.now(dt.timezone.utc)
TODAY = NOW.date()
BEANS = 'Bean Collective <orders@beancollective.example>'
STATUS = 'https://beancollective.example/71234567/orders/0f1e2d3c4b5a69788796a5b4c3d2e1f0'
PRODUCT = 'https://beancollective.example/products/house-blend-1kg'
ITEMS = {'House Blend': 'Whole bean / 1 kg', 'Decaf': 'Ground / 250 g', 'Desk Lamp': 'Black'}  # what the stand-in model "reads"


def order(item='House Blend', variant='Whole bean / 1 kg', price='€24.50', n=1001, status=STATUS, product=PRODUCT):
    return (f'Thank you for your purchase!\nOrder #{n}\n{item}\n{variant}\nQuantity: 1\n{price}\n'
            f'Subtotal {price}\nTotal {price}\nView your order: {status}\nShop again: {product}\n'
            'Powered by Shopify https://cdn.shopify.com/s/files/logo.png')


class Reorders(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(machine_main.App); self.app.store = self.store
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS], 'timezone': 'Europe/Brussels',
                           'openclaw_state': self.temp.name + '/none.sqlite'}
        self.store.accounts = self.app.config['accounts']
        self.sent, self.n, self.asked, self.lie, self.again = [], 0, [], None, True
        for name, value in (('routines_now', lambda s: dt.datetime.now()), ('background_pause', lambda s, **k: None),
                            ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                            ('preparation_gateway', lambda s, request: self.sent.append(request) or {'status': 'pending'}),
                            ('routine_spawn', lambda s, target, run_id: target(run_id))):
            p = patch.object(machine_main.App, name, value); p.start(); self.addCleanup(p.stop)
        self.app.reorder_model = self.model

    def model(self, prompt):
        """A model that reads the made-up mails as a person would: an order is one that says thank you for the
        purchase; its item is the line after the order number. self.lie: a title the mail never shows."""
        self.asked.append(prompt)
        mails = []
        for line in prompt.split('<<<\n', 1)[1].split('\n>>>', 1)[0].splitlines():
            c = json.loads(line)
            if 'Thank you for your purchase' not in c['mail']:
                mails.append({'id': c['id'], 'order': False})
                continue
            item = next(i for i in ITEMS if i in c['mail'])
            variant, price = ITEMS[item], re.search(r'Quantity: 1 (€[\d.]+)', c['mail'])[1]
            mails.append({'id': c['id'], 'order': True, 'area': c['mailbox'], 'items': [
                {'title': self.lie or item, 'variant': variant, 'qty': 1, 'price': price.strip('€'), 'currency': 'EUR',
                 'link': '1' if c['links'] else '', 'again': self.again}]})
        return json.dumps({'mails': mails})

    def mail(self, sender, title, body='', days_ago=0, account='p', labels=('INBOX',), **metadata):
        self.n += 1
        meta = {'from': sender, 'labels': list(labels), 'thread_id': f't{self.n}', **metadata}
        on = dt.datetime.combine(TODAY - dt.timedelta(days=days_ago), dt.time(12), dt.timezone.utc)
        with self.store.connect() as db:
            db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at,version) VALUES(?,?,?,?,?,?,?,?,?,?)',
                       (account, f'm{self.n}', 'gmail.message', on.isoformat(), title, body, json.dumps(meta), 'h', on.isoformat(), 1))
            return db.execute('SELECT id FROM events WHERE source_id=?', (f'm{self.n}',)).fetchone()[0]

    def beans(self, days=(86, 58, 30)):
        """Coffee every four weeks at a Shopify store, each order with its shipping notice."""
        for k, d in enumerate(days):
            self.mail(BEANS, f'Order #{1001 + k} confirmed', order(n=1001 + k), d)
            self.mail(BEANS, f'Your order #{1001 + k} is on the way', f'Your order is on its way. Track it: {STATUS}', d - 2)

    def add(self):
        out = self.app.action('routine_template', {'key': 'reorder'}, owner_dashboard=True)
        self.app.routines_step()
        return out

    def todos(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM suggestions WHERE dedupe_key LIKE 'reorder:%' ORDER BY created_at")]

    def view(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            return row, self.store.suggestion_result(row, db)

    def runs(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM routine_runs ORDER BY started_at')]

    # --- the template --------------------------------------------------------------------------------------------

    def test_it_is_a_daily_template_whose_words_never_buy(self):
        self.assertEqual(routine_templates.rule('reorder'), 'daily')
        for text in [routine_templates.TEMPLATES['reorder'][k] for k in ('name', 'what', 'words')]:
            self.assertNotIn('—', text)
        self.assertIn('Never buy anything.', routine_templates.TEMPLATES['reorder']['words'])
        out = self.add()
        self.assertEqual([t['added'] for t in out['templates'] if t['key'] == 'reorder'], [True])

    # --- detection -------------------------------------------------------------------------------------------------

    def test_only_shopify_stores_with_enough_mail_are_read(self):
        self.beans()
        for d in (90, 60, 30):  # regular, but not a Shopify store
            self.mail('Pet Corner <orders@petcorner.example>', 'Order confirmed', 'Thank you for your purchase!\nOrder #9 Kibble Adult 2 kg Quantity: 1 €19.00', d)
        self.mail('Lamp Studio <hi@lampstudio.example>', 'Order #5 confirmed', order('Desk Lamp', 'Black', '€89.00', 5,
                  'https://lampstudio.example/123/orders/aaaabbbbccccddddeeeeffff', 'https://lampstudio.example/products/desk-lamp'), 40)
        with self.store.connect() as db:
            reorder.ensure(db)
            found = reorder.candidates(db, ['w', 'p'], NOW)
        self.assertEqual({c['store'] for c in found}, {'beancollective.example'})  # one mail from the lamp store: never read
        self.assertEqual(len(found), 6)  # the three orders and their shipping notices
        first = next(c for c in found if c['title'] == 'Order #1001 confirmed')
        self.assertEqual((first['status'], first['products']), (STATUS, [PRODUCT]))
        self.assertNotIn('https://', first['text'])  # links are read in plain code, not given to the model whole
        self.assertTrue(reorder.shopify('orders@shop.myshopify.com', ''))
        self.assertFalse(reorder.shopify('orders@petcorner.example', 'Thanks for shopping with us at https://petcorner.example/'))

    def test_shopify_sender_names_the_store_by_its_order_page(self):
        self.assertEqual(reorder.store_of('Bean Collective', 'mailer@shopify.com', [STATUS]), ('beancollective.example', 'Bean Collective'))
        self.assertEqual(reorder.store_of('Bean Collective', 'mailer@shopify.com', []), ('', 'Bean Collective'))

    # --- a run -------------------------------------------------------------------------------------------------------

    def test_a_steady_item_nearly_due_becomes_one_quiet_todo_that_opens_the_store(self):
        self.beans()
        self.add()
        self.assertEqual(len(self.asked), 1)  # one small model call, never an agent turn
        self.assertEqual([s for s in self.sent if s.get('action') == 'start'], [])
        todos = self.todos()
        self.assertEqual(len(todos), 1)
        row, extra = self.view(todos[0]['id'])
        self.assertEqual(row['title'], 'Running low on House Blend?')
        self.assertIn('Bean Collective', row['body']); self.assertIn('about every 4 weeks', row['body']); self.assertIn('€24.50', row['body'])
        shown = extra['reorder']
        self.assertEqual((shown['title'], shown['variant'], shown['price'], shown['currency'], shown['usual'], shown['times']),
                         ('House Blend', 'Whole bean / 1 kg', '24.50', 'EUR', 28, 3))
        self.assertEqual(shown['last_on'], (TODAY - dt.timedelta(days=30)).isoformat())
        self.assertEqual(shown['way'], {'kind': 'open', 'url': PRODUCT})
        self.assertFalse(self.app.is_work_suggestion(todos[0]['id']))  # the personal mailbox's order
        with self.store.connect() as db:
            self.assertTrue(todo_kinds.quiet(db, todos[0]['id']))  # never a buzz
            self.assertTrue(todo_kinds.refused(db, todos[0]['id']))
        with self.assertRaises(OwnerError):  # nothing to Do: nothing is bought here
            self.app.action('decide', {'suggestion_id': todos[0]['id'], 'choice': 'accept'}, owner_dashboard=True)
        self.assertEqual(self.runs()[0]['state'], 'ready')

    def test_mail_is_read_once_and_the_same_purchase_never_makes_a_second_todo(self):
        self.beans()
        self.add()
        with self.store.connect() as db:
            self.assertEqual(reorder.candidates(db, ['w', 'p'], NOW), [])  # all read
            self.assertEqual(reorder.due(db, TODAY), [])  # its to-do is there
            self.assertEqual(db.execute("SELECT COUNT(*) FROM reorder_mail WHERE state='other'").fetchone()[0], 3)  # the shipping notices

    def test_ordered_again_closes_the_open_todo(self):
        self.beans()
        self.add()
        sid = self.todos()[0]['id']
        self.mail(BEANS, 'Order #1004 confirmed', order(n=1004), 1)
        self.mail(BEANS, 'Order #1005 confirmed', order('Decaf', 'Ground / 250 g', '€9.00', 1005), 1)  # read with it, not the same item
        with self.store.connect() as db:
            routine = dict(db.execute("SELECT * FROM routines WHERE origin='template:reorder'").fetchone())
        self.app.action('routine_run_now', {'id': routine['id']}, owner_dashboard=True)
        self.app.routines_step()
        self.assertEqual(len(self.asked), 2)  # only the new mail
        self.assertNotIn('Order #1001', self.asked[1])
        row, _ = self.view(sid)
        self.assertEqual(row['status'], 'completed')
        self.assertEqual(len(self.todos()), 1)  # the new order starts the next wait

    # --- quality or nothing ------------------------------------------------------------------------------------------

    def test_a_title_the_mail_doesnt_show_leaves_the_item_out(self):
        self.beans()
        self.lie = 'Espresso Roast'
        self.add()
        self.assertEqual(self.todos(), [])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM purchases').fetchone()[0], 0)
        self.assertEqual(self.runs()[0]['state'], 'nothing')

    def test_something_not_used_up_is_never_due(self):
        self.beans()
        self.again = False
        self.add()
        self.assertEqual(self.todos(), [])

    def test_no_pattern_no_todo(self):
        self.beans(days=(58, 30))  # two orders: one gap is no pattern
        self.add()
        self.assertEqual(self.todos(), [])
        rows = [{'bought_on': (TODAY - dt.timedelta(days=d)).isoformat(), 'again': 1} for d in (100, 90, 30)]
        self.assertIsNone(reorder.pattern(rows))  # 10 and 60 days apart: not steady
        rows = [{'bought_on': (TODAY - dt.timedelta(days=d)).isoformat(), 'again': 1} for d in (60, 59, 30, 1)]
        self.assertEqual(reorder.pattern(rows)[0], 29)  # orders a day apart are one

    def test_not_due_yet_or_long_stopped(self):
        self.beans(days=(66, 38, 10))  # due in about two weeks
        self.add()
        self.assertEqual(self.todos(), [])
        rows = [{'bought_on': (TODAY - dt.timedelta(days=d)).isoformat(), 'again': 1} for d in (200, 172, 144)]
        usual, last, *_ = reorder.pattern(rows)
        self.assertGreater(TODAY, last + dt.timedelta(days=2 * usual))  # stopped buying it: never due

    def test_the_way_falls_back_to_the_order_page_then_the_store(self):
        self.assertEqual(reorder.way({'link': '', 'status_link': STATUS, 'store': 'beancollective.example'}), {'kind': 'open', 'url': STATUS})
        self.assertEqual(reorder.way({'link': 'http://x.example/p', 'status_link': '', 'store': 'beancollective.example'}),
                         {'kind': 'open', 'url': 'https://beancollective.example/'})

    def test_a_price_the_mail_doesnt_show_is_no_purchase(self):
        found = [{'id': 1, 'event': 7, 'title': 'Order #1', 'body': order(), 'products': [PRODUCT]}]
        answer = {'mails': [{'id': 1, 'order': True, 'items': [{'title': 'House Blend', 'qty': 1, 'price': '19.99', 'currency': 'EUR', 'again': True}]}]}
        self.assertEqual(reorder.confirmed(found, answer), {7: ('other', 'personal', [])})
        answer['mails'][0]['items'][0].update(price='24.50', link='9', variant='Made up')
        state, _, items = reorder.confirmed(found, answer)[7]
        self.assertEqual((state, items[0]['link'], items[0]['variant']), ('order', '', ''))  # a link or variant it can't show: left out


if __name__ == '__main__':
    unittest.main()
