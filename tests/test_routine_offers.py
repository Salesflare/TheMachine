"""Offers to turn on a mail cleanup template (routine_offers.py, docs/help/routines.md "Templates"): only when a lot of
that mail came in this week, counted in plain code from mail already synced; once, until the owner says yes or no; a
yes adds the template as Templates' Add does, and nothing is unsubscribed or moved before the owner confirms on its
to-do. Made-up mail only; nothing is sent."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('offers_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import mail_cleanup_app  # noqa: E402
import routine_offers as ro  # noqa: E402
from machine.actions import DASHBOARD_ACTIONS, OWNER_ACTIONS  # noqa: E402

ACCOUNTS = [{'id': 'w', 'email': 'owner@acme.example', 'boundary': 'work:acme.example'}]


def stamp(hours_ago):
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours_ago)).isoformat()


class Offers(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS], 'timezone': 'Europe/Brussels',
                           'openclaw_state': self.temp.name + '/none.sqlite'}
        self.store.accounts = self.app.config['accounts']
        self.marks, self.clicked, self.sent, self.n = False, [], [], 0
        for name, value in (('background_pause', lambda s, **k: None), ('background_spaced', lambda s: True),
                            ('background_started', lambda s: None),
                            ('preparation_gateway', lambda s, request: self.sent.append(request) or {'status': 'pending'}),
                            ('routine_spawn', lambda s, target, run_id: target(run_id)),
                            ('cleanup_headers', lambda s, account, message: {}),
                            ('cleanup_can_send', lambda s, account: False),
                            ('cleanup_can_mark', lambda s, account: self.marks)):
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        p = patch.object(mail_cleanup_app, 'one_click', lambda url: self.clicked.append(url) or True); p.start(); self.addCleanup(p.stop)

    def mail(self, sender, title, hours_ago=3, version=1, **metadata):
        self.n += 1
        meta = {'from': sender, 'labels': ['INBOX'], 'thread_id': f't{self.n}', **metadata}
        with self.store.connect() as db:
            db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at,version) VALUES(?,?,?,?,?,?,?,?,?,?)',
                       ('w', f'm{self.n}', 'gmail.message', stamp(hours_ago), title, '', json.dumps(meta), 'h', stamp(hours_ago), version))
        return f'm{self.n}'

    def newsletters(self, senders, each, hours_ago=3):
        for s in range(senders):
            for i in range(each):
                self.mail(f'Shop {s} <news@shop{s}.example>', f'Deals {i}', hours_ago=hours_ago + i * 5, list_unsubscribe=True)

    def look(self):
        self.app._routine_offers_at = 0
        self.app.routine_offers_step()
        with self.store.connect() as db:
            return ro.view(db)

    def act(self, name, owner=True, **args):
        return self.app.action(name, args, owner_dashboard=owner)

    def test_a_week_with_a_lot_of_newsletters_offers_newsletter_cleanup_with_the_count(self):
        self.newsletters(6, 5)  # 30 from 6 senders
        self.mail('Sam Rivera <sam@partner.example>', 'Lunch Thursday?')  # a person: not counted
        self.mail('Old News <news@old.example>', 'Last month', hours_ago=24 * 9, list_unsubscribe=True)  # before this week
        offer = self.look()
        self.assertEqual((offer['key'], offer['n'], offer['name']), ('newsletters', 30, 'Newsletter cleanup'))
        self.assertIn('newsletters', offer['what'])
        self.assertEqual(self.sent, [])  # plain code: no model turn
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM routines').fetchone()[0], 0)  # nothing added by itself
        self.assertEqual(self.look()['n'], 30)  # looked at again: still one offer, the same count

    def test_too_few_newsletters_or_senders_offer_nothing(self):
        self.newsletters(6, 3)  # 18: under the bar
        self.assertIsNone(self.look())
        self.newsletters(1, 7, hours_ago=1)  # seven more from one of them: 25 in the week
        self.assertEqual(self.look()['n'], 25)
        with self.store.connect() as db:
            db.execute('DELETE FROM events')
        self.newsletters(4, 10)  # 40, from four senders: not a lot of newsletters, one busy list
        self.assertIsNone(self.look())  # the open offer that no longer holds is gone

    def test_no_thanks_is_never_offered_again(self):
        self.newsletters(6, 5)
        self.look()
        with self.assertRaises(ValueError):
            self.act('routine_offer', owner=False, key='newsletters', choice='yes')
        self.assertTrue({'routine_offer'} <= OWNER_ACTIONS & DASHBOARD_ACTIONS)
        self.assertEqual(self.act('routine_offer', key='newsletters', choice='no'), {'key': 'newsletters', 'added': None})
        self.newsletters(6, 5, hours_ago=1)
        self.assertIsNone(self.look())
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM routines').fetchone()[0], 0)
        with self.assertRaises(ValueError):
            self.act('routine_offer', key='newsletters', choice='yes')  # gone

    def test_turn_it_on_adds_the_template_and_changes_nothing_before_the_confirm(self):
        self.newsletters(6, 5)
        self.look()
        out = self.act('routine_offer', key='newsletters', choice='yes')
        self.assertTrue(out['added'])
        with self.store.connect() as db:
            row = db.execute("SELECT state,origin FROM routines WHERE id=?", (out['added'],)).fetchone()
            self.assertEqual(tuple(row), ('on', 'template:newsletters'))
            self.assertIsNone(ro.view(db))
        self.assertEqual(self.clicked, [])  # nothing unsubscribed: the to-do waits for the owner's picks
        self.assertIsNone(self.look())  # never offered again

    def test_a_template_the_owner_has_or_had_is_never_offered(self):
        self.newsletters(6, 5)
        self.assertIsNotNone(self.look())
        self.act('routine_template', key='newsletters')  # added on Routines meanwhile
        with self.store.connect() as db:
            self.assertIsNone(ro.view(db))
            rid = db.execute("SELECT id FROM routines WHERE origin='template:newsletters'").fetchone()[0]
        self.act('routine_state', id=rid, to='stop')
        self.assertIsNone(self.look())  # stopped: the owner decided

    def test_spam_moved_by_hand_offers_spam_cleanup_only_where_mail_can_move(self):
        for i in range(6):
            self.mail(f'Pitch {i} <sales@leads{i}.example>', 'Verified leads', hours_ago=30 + i, version=2, labels=['SPAM'])
        self.mail('Filtered <x@junk.example>', 'You won', hours_ago=20, labels=['SPAM'])  # the filter's own: not by hand
        self.assertIsNone(self.look())  # read-only Gmail: no Spam cleanup to offer
        self.marks = True
        self.app._cleanup_marks = None
        offer = self.look()
        self.assertEqual((offer['key'], offer['n']), ('spam', 6))
        self.newsletters(6, 5)
        self.assertEqual(self.look()['key'], 'newsletters')  # one at a time: newsletters first
        self.act('routine_offer', key='newsletters', choice='no')
        with self.store.connect() as db:
            self.assertEqual(ro.view(db)['key'], 'spam')

    def test_the_counts_are_looked_at_a_few_times_a_day(self):
        self.newsletters(6, 5)
        self.app.routine_offers_step()
        with patch.object(ro, 'count', side_effect=AssertionError('looked again')):
            self.app.routine_offers_step()  # within LOOK_EVERY: not again


if __name__ == '__main__':
    unittest.main()
