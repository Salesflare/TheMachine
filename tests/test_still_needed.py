"""Still needed? (still_needed.py): an open to-do nobody touched for a week asks once, with the weekly recap's Drop and
Keep; Keep never asks again, Drop is Not needed, and no answer folds it out of the way instead of deleting it. Made-up
to-dos only; nothing is sent."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

import test_ux as ux
import activity
import still_needed
import timeutil

a = ux.a
NOW = '2026-11-06T09:00:00+00:00'
TZ = ZoneInfo('Europe/Brussels')


def ago(days, now=NOW):
    return (dt.datetime.fromisoformat(now) - dt.timedelta(days=days)).isoformat()


class StillNeeded(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        for p in (patch.object(timeutil, 'LOCAL_TZ', TZ), patch.object(a, 'now', return_value=NOW)):
            p.start()
            self.addCleanup(p.stop)
        self.config = {'accounts': [{'id': 'work', 'service': 'gmail', 'email': 'owner@example.com', 'boundary': 'work:Example'}],
                       'database': str(Path(self.tmp.name) / 'events.sqlite')}
        self.store = a.Store(self.config['database'])
        self.app = object.__new__(a.App)
        self.app.store, self.app.config = self.store, self.config
        self.n = 0

    def event(self, days):
        self.n += 1
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': f'm{self.n}', 'kind': 'gmail.message', 'occurred_at': ago(days),
                                             'title': 'Quote', 'body': 'Could you send the quote?', 'metadata': {'from': 'sam@client.example'}, 'deleted': False}])
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (f'm{self.n}',)).fetchone()[0]

    def card(self, title, days, status='pending', **extra):
        """A made-up to-do made `days` ago from a message just before it, untouched since."""
        sid = self.store.suggest('k-' + title, title, 'Send the quote.', [self.event(days + 0.1)])['id']
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET created_at=?,status=? WHERE id=?', (ago(days), status, sid))
            for k, v in extra.items():
                db.execute(f'UPDATE suggestions SET {k}=? WHERE id=?', (v, sid))
        return sid

    def step(self, at=NOW):
        with patch.object(a, 'now', return_value=at):
            return self.app.still_needed_step(at)

    def shown(self, sid, at=NOW):
        with self.store.connect() as db:
            cards = [dict(r) for r in db.execute('SELECT * FROM suggestions WHERE id=?', (sid,))]
            still_needed.annotate(db, cards, at, TZ)
        return cards[0].get('still_needed')

    def rows(self, sid):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM recap_items WHERE kind=? AND ref=?', (still_needed.KIND, sid))]

    def keep(self, sid, owner_dashboard=True, source=None):
        args = {'id': self.rows(sid)[0]['id'], 'choice': 'keep', 'decision_id': 'keep-' + sid}
        if source:
            args['source'] = source
        return self.app.action('recap_decide', args, owner_dashboard)

    def test_a_week_untouched_asks_once_and_not_before(self):
        old, fresh = self.card('Send Ayla the quote', 8, 'prepared'), self.card('Book the venue', 6)
        self.assertEqual(self.step(), [old])
        self.assertEqual(self.step(), [])  # asked once: never a second question
        self.assertEqual(len(self.rows(old)), 1)
        self.assertEqual(self.shown(old)['folded'], False)
        self.assertEqual(self.shown(old)['id'], self.rows(old)[0]['id'])
        self.assertIsNone(self.shown(fresh))
        self.assertEqual(self.step(ago(-2)), [fresh])  # two days later it is a week old too

    def test_each_kind_of_touch_counts(self):
        opened, chat, edited, message = (self.card(t, 10) for t in ('Opened', 'Chatted', 'Edited', 'New message'))
        newer = self.event(4)
        with self.store.connect() as db:
            activity.ensure(db)
            activity.note_opened(db, opened, ago(3), TZ)
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('c1',?,'other','Shorter please','dashboard',?)", (chat, ago(2)))
            db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_subject,before_body,after_subject,after_body,source,created_at) "
                       "VALUES('e1',?,'r1','r2','email','','a','','b','dashboard',?)", (edited, ago(1)))
            db.execute('UPDATE suggestions SET event_ids=? WHERE id=?', (json.dumps([newer]), message))
        self.assertEqual(self.step(), [])
        # The Machine's own decisions are not a touch
        machine = self.card('Prepared by itself', 10)
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('m1',?,'accept','','assistant',?)", (machine, ago(1)))
        self.assertEqual(self.step(), [machine])

    def test_keep_never_asks_again(self):
        sid = self.card('Renew the domain', 9)
        self.step()
        self.assertEqual(self.keep(sid)['status'], 'kept')
        self.assertIsNone(self.shown(sid))
        self.assertEqual(self.step(ago(-30)), [])
        with self.store.connect() as db:  # the to-do itself stays as it was
            self.assertEqual(db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0], 'pending')

    def test_only_the_dashboard_answers_it(self):
        sid = self.card('Renew the domain', 9)
        self.step()
        with self.assertRaises(ValueError):
            self.keep(sid, owner_dashboard=False, source='telegram')
        with self.assertRaises(ValueError):
            self.keep(sid, owner_dashboard=False)
        self.assertEqual(self.rows(sid)[0]['status'], 'open')

    def test_drop_is_not_needed_and_ends_the_question(self):
        sid = self.card('Answer the survey', 9)
        self.step()
        self.store.decide(sid, 'reject', 'No longer needed', 'drop-1', 'dashboard')  # the dashboard's Drop: its own Not needed
        self.step()
        self.assertEqual(self.rows(sid)[0]['status'], 'dropped')
        self.store.decide(sid, 'undo', '', 'undo-1', 'dashboard')  # Undo brings it back, without asking again
        self.assertIsNone(self.shown(sid))
        self.assertEqual(self.step(ago(-10)), [])

    def test_drop_from_the_question_rejects_the_to_do(self):
        sid = self.card('Answer the survey', 9)
        self.step()
        self.assertEqual(self.app.action('recap_decide', {'id': self.rows(sid)[0]['id'], 'choice': 'drop', 'decision_id': 'd-1'}, True)['status'], 'dropped')
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0], 'rejected')
            self.assertEqual(db.execute("SELECT feedback FROM decisions WHERE suggestion_id=? AND choice='reject'", (sid,)).fetchone()[0], 'No longer needed')

    def test_no_answer_folds_it_away_and_a_touch_brings_it_back(self):
        sid = self.card('Send the brochure', 8)
        self.step()
        self.assertFalse(self.shown(sid, ago(-6))['folded'])
        self.assertTrue(self.shown(sid, ago(-7))['folded'])  # a week without an answer: out of the way, not deleted
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0], 'pending')
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('r1',?,'rename','','dashboard',?)", (sid, ago(-6.5)))
        later = self.shown(sid, ago(-7))
        self.assertFalse(later['folded'])  # touched: back in its list, still asking
        self.assertEqual(later['since'], ago(-6.5))

    def test_to_dos_with_their_own_way_out_are_not_asked(self):
        skipped = [self.card('Looks done', 10, handled_hint=json.dumps({'why': 'PR merged', 'at': ago(9)})),
                   self.card('Waiting on Sam', 10, 'prepared', outcome=json.dumps({'state': 'waiting'})),
                   self.card('Due ahead', 10, due=ago(-3)[:10]),
                   self.card('Before the meeting', 10, expires_at=ago(-1)),
                   self.card('Snoozed', 10, 'snoozed'),
                   self.card('Preparing', 10, 'accepted')]
        with self.store.connect() as db:
            a.recurring.ensure(db)
            repeat = self.card('Weekly numbers', 10)
            db.execute("INSERT INTO recurring_cards(suggestion_id,series_id,due,created_at) VALUES(?,'s1',?,?)", (repeat, ago(10)[:10], ago(10)))
        self.assertEqual(self.step(), [])
        self.assertEqual([self.rows(s) for s in skipped + [repeat]], [[]] * (len(skipped) + 1))

    def test_the_status_payload_carries_it(self):
        sid = self.card('Send Ayla the quote', 8, 'prepared')
        self.step()
        with self.store.connect() as db:
            cards = [dict(r) for r in db.execute('SELECT * FROM suggestions')]
            self.store.card_views(db, cards, jobs=False)
        self.assertEqual(cards[0]['still_needed']['folded'], False)
        self.assertEqual(cards[0]['id'], sid)


if __name__ == '__main__':
    unittest.main()
