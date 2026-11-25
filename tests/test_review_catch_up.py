"""What a regular review claims while the Machine is behind (machine/store/review_catch_up.py): recent messages that may
need the owner first, a third for what came in first, everything else about a claim as before. Fake data, no model. A
whole catch-up on some 1,000 made-up signals is in review_backlog.py, run by hand."""
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest

import machine.main as machine_main
import machine.store.review as review
from machine.store import review_catch_up as catch_up
import review_backlog
import timeutil

ME = 'owner@example.com'
NOW = dt.datetime(2026, 11, 24, 12, 0, tzinfo=dt.timezone.utc)


def ago(hours):
    return (NOW - dt.timedelta(hours=hours)).isoformat()


class CatchUp(unittest.TestCase):
    protect = None

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        kept = timeutil.PINNED
        self.addCleanup(lambda: setattr(timeutil, 'PINNED', kept))
        timeutil.pin(NOW)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite', protect=self.protect)
        self.store.accounts = [{'id': 'work', 'service': 'gmail', 'email': ME}, *({'id': x, 'service': x} for x in ('whatsapp', 'slack', 'github', 'calendar', 'teams'))]
        self.store.owner_user_ids = {'U0OWNER'}
        self.boxes = [a['id'] for a in self.store.accounts]
        self.n = 0

    def commit(self, events):
        """Events as (hours ago, account, kind, title, metadata, hours ago it came in): {title: id}"""
        pages, stamps = {}, []
        for hours, account, kind, title, meta, came in events:
            self.n += 1
            stamps.append((ago(came), f's{self.n}'))
            pages.setdefault(account, []).append({'account_id': account, 'source_id': f's{self.n}', 'kind': kind, 'occurred_at': ago(hours), 'title': title,
                                                  'body': 'Can you look at this?', 'metadata': meta, 'deleted': False})
        for account, page in pages.items():
            self.store.commit_page(account, {}, page)
        with self.store.connect() as db:
            db.executemany('UPDATE events SET ingested_at=? WHERE source_id=?', stamps)
            return {r['title']: r['id'] for r in db.execute('SELECT id,title FROM events')}

    def mail(self, title, hours, came=None, sender='Ann <ann@people.example>', to=ME, labels=('INBOX',), thread=None, **meta):
        return (hours, 'work', 'gmail.message', title, {'from': sender, 'to': to, 'labels': list(labels), 'thread_id': thread or title, **meta}, hours if came is None else came)

    def issue(self, title, hours):
        return (hours, 'github', 'github.issue', title, {}, hours)

    def chat(self, title, hours, chat='1@s.whatsapp.net', **meta):
        return (hours, 'whatsapp', 'whatsapp.message', title, {'chat_id': chat, 'from': 'Bo', 'from_me': False, **meta}, hours)

    def old(self, count=300):
        """A backlog that makes the Machine behind: other people's messages of 30 to 40 hours ago."""
        return [self.issue(f'old{i}', 40 - i / 30) for i in range(count)]

    def claim(self, run='one', **kw):
        batch = self.store.begin_analysis(self.boxes, kw.pop('limit', 120), 'private', run, **kw)
        with self.store.connect() as db:
            items = json.loads(db.execute('SELECT items FROM analyses WHERE id=?', (batch['analysis_id'],)).fetchone()[0])
            titles = dict((r['id'], r['title']) for r in db.execute('SELECT id,title FROM events'))
        return batch, [titles[i['id']] for i in items], review.claim_weight(items)

    def finish(self, batch, run='one'):
        self.store.finish_analysis(batch['analysis_id'], 'Assessed', 'private', run)

    def shared_out(self):
        """What a claim took before this (Store.share_out), for the waiting signals as they are."""
        with self.store.connect() as db:
            counts = {a: db.execute('SELECT count(*) FROM events WHERE account_id=? AND analyzed_version<version', (a,)).fetchone()[0] for a in self.boxes}
            return {r['title'] for r in self.store.share_out(db, self.boxes, counts, 120, '', [])[0]}

    def test_a_normal_backlog_is_claimed_as_before(self):
        self.commit(self.old(239) + [self.mail('direct', 30)])
        before = self.shared_out()
        self.assertEqual(set(self.claim()[1]), before)  # 240: two whole reviews, not behind

    def test_newsletters_alone_are_not_behind(self):
        shop = [self.mail(f'deal{i}', 40 - i / 30, sender=f'Shop <news@shop{i}.example>', labels=('CATEGORY_PROMOTIONS',), list_unsubscribe='<mailto:u@x.example>')
                for i in range(500)]
        self.commit(shop)  # title lines: about one review's worth
        before = self.shared_out()
        self.assertEqual(set(self.claim()[1]), before)

    def test_one_more_than_two_reviews_is_behind(self):
        self.commit(self.old(240) + [self.mail('direct', 20)])
        with self.store.connect() as db:
            counts = {a: db.execute('SELECT count(*) FROM events WHERE account_id=?', (a,)).fetchone()[0] for a in self.boxes}
            self.assertIsNotNone(catch_up.claim(self.store, db, counts, 120, review.signal_weight, [], NOW))
            counts['github'] -= 1
            self.assertIsNone(catch_up.claim(self.store, db, counts, 120, review.signal_weight, [], NOW))

    def test_recent_direct_messages_of_every_source_come_first_and_the_oldest_keep_a_third(self):
        direct = [self.mail('mail', 5), self.chat('chat', 6),
                  (7, 'slack', 'slack.message', 'dm', {'conversation_type': 'dm', 'channel_id': 'D1', 'user_id': 'U1', 'message_ts': '1.1', 'thread_ts': '1.1'}, 7),
                  (8, 'teams', 'teams.message', 'teams', {'chat_id': 't1', 'chat_kind': 'oneOnOne', 'from_me': False}, 8),
                  (9, 'teams', 'teams.message', 'mention', {'chat_id': 't2', 'chat_kind': 'group', 'from_me': False, 'mentions_me': True}, 9),
                  (-5, 'calendar', 'calendar.event', 'soon', {}, 20), (-200, 'calendar', 'calendar.event', 'later', {}, 20)]
        noise = [self.chat(f'group{i}', 3 + i / 60, chat=f'{i}@g.us') for i in range(200)]
        noise += [self.mail(f'deal{i}', 2, sender='Shop <news@shop.example>', labels=('CATEGORY_PROMOTIONS',), list_unsubscribe='<mailto:u@x.example>') for i in range(200)]
        self.commit(self.old() + direct + noise)
        _, titles, weight = self.claim()
        self.assertLessEqual({'mail', 'chat', 'dm', 'teams', 'mention', 'soon'}, set(titles))
        self.assertNotIn('later', titles)
        self.assertLessEqual({f'old{i}' for i in range(40)}, set(titles))  # the third, strictly the oldest first
        self.assertFalse([t for t in titles if t.startswith('deal')])
        self.assertEqual(weight, 120)

    def test_a_flood_of_direct_messages_never_takes_the_oldest_ones_share(self):
        self.commit(self.old())
        seen = []
        for run in range(8):  # 300 older ones / 40: within 8 reviews, whatever comes in between
            self.commit([self.chat(f'flood{run}-{i}', 1 - run / 100, chat=f'{run}-{i}@s.whatsapp.net') for i in range(150)])
            batch, titles, weight = self.claim(f'r{run}')
            self.assertLess(weight, 121)
            seen += titles
            self.finish(batch, f'r{run}')
        self.assertLessEqual({f'old{i}' for i in range(300)}, set(seen))

    def test_answered_people_and_the_owners_own_are_not_first(self):
        self.commit(self.old() + [self.mail('asked', 10, thread='t'), self.mail('sent', 9, sender=f'Me <{ME}>', to='ann@people.example', labels=('SENT',), thread='t'),
                                  self.chat('question', 10, chat='9@s.whatsapp.net'), self.chat('reply', 9, chat='9@s.whatsapp.net', from_me=True),
                                  self.mail('open', 8)])
        titles = self.claim()[1]
        self.assertIn('open', titles)
        self.assertFalse({'asked', 'sent', 'question', 'reply'} & set(titles))

    def test_a_conversation_is_claimed_together(self):
        self.commit(self.old() + [self.mail('asked first', 30, thread='t'), self.mail('answered', 29, sender=f'Me <{ME}>', to='ann@people.example', labels=('SENT',), thread='t'),
                                  self.mail('asked again', 5, thread='t'), self.chat('older half', 32), self.chat('newer half', 2)])
        self.assertLessEqual({'asked first', 'answered', 'asked again', 'older half', 'newer half'}, set(self.claim()[1]))

    def test_a_conversation_of_one_takes_only_so_much(self):
        self.commit(self.old() + [self.chat(f'talk{i}', 2 + i / 60) for i in range(150)] + [self.chat('other', 20, chat='2@s.whatsapp.net')])
        titles = self.claim()[1]
        self.assertEqual(sum(t.startswith('talk') for t in titles), catch_up.CONVERSATION)
        self.assertIn('other', titles)

    def test_put_off_once_waits_behind_fresh_and_set_aside_is_not_offered(self):
        ids = self.commit(self.old() + [self.chat('put off', 3, chat='a'), self.chat('aside', 3, chat='b')] +
                          [self.chat(f'fresh{i}', 4, chat=f'c{i}') for i in range(90)])
        with self.store.connect() as db:
            db.execute('UPDATE events SET deferrals=1 WHERE id=?', (ids['put off'],))
            db.execute('UPDATE events SET deferrals=2 WHERE id=?', (ids['aside'],))
        batch, titles, _ = self.claim()
        self.assertFalse({'put off', 'aside'} & set(titles))
        self.finish(batch)
        with self.store.connect() as db:  # the fresh ones reviewed: the one put off once gets its second look
            db.execute("UPDATE events SET analyzed_version=version WHERE account_id='whatsapp' AND deferrals=1 AND id!=?", (ids['put off'],))
            db.execute("UPDATE events SET analyzed_version=version WHERE account_id='whatsapp' AND deferrals=0")
        titles = self.claim('two')[1]
        self.assertIn('put off', titles)
        self.assertNotIn('aside', titles)

    def test_an_unfinished_claim_goes_first(self):
        ids = self.commit(self.old() + [self.chat('recent', 2)])
        mine = [ids[f'old{i}'] for i in range(250, 300)]
        with self.store.connect() as db:
            db.execute("INSERT INTO analyses(id,started_at,finished_at,items,status,owner_session,owner_run) VALUES('gone',?,?,?,'abandoned','x','x')",
                       (ago(2), ago(1), json.dumps([{'id': i, 'version': 1} for i in mine])))
        batch, titles, weight = self.claim()
        self.assertLessEqual({f'old{i}' for i in range(250, 300)}, set(titles))
        self.assertEqual(batch['resumed_from'], 'gone')
        self.assertIn('recent', titles)
        self.assertLessEqual({f'old{i}' for i in range(24)}, set(titles))  # a third of the 70 left
        self.assertEqual(weight, 120)

    def test_a_running_claim_resumes_whole(self):
        self.commit(self.old() + [self.chat('recent', 2)])
        batch, titles, _ = self.claim()
        self.commit([self.chat('newer', 1, chat='2@s.whatsapp.net')])
        again, resumed, _ = self.claim()
        self.assertEqual(again['analysis_id'], batch['analysis_id'])
        self.assertEqual(resumed, titles)

    def test_the_last_look_keeps_its_place(self):
        ids = self.commit(self.old() + [self.mail('set aside', 100)])
        with self.store.connect() as db:
            db.execute('UPDATE events SET deferrals=2 WHERE id=?', (ids['set aside'],))
        _, titles, weight = self.claim()
        self.assertIn('set aside', titles)
        self.assertEqual(weight, 120)

    def test_previews_and_the_quick_look_choose_as_before(self):
        self.commit(self.old() + [self.mail('direct', 5)])
        kept, catch_up.claim = catch_up.claim, lambda *a: self.fail('a preview is never a catch-up')
        self.addCleanup(lambda: setattr(catch_up, 'claim', kept))
        for run, column in (('preview', 'preview'), ('quick', 'promising'), ('window', 'window_hours')):
            with self.store.connect() as db:
                db.execute(f"INSERT INTO review_runs(run_id,status,started_at,updated_at,{column}) VALUES(?,'running',?,?,1)", (run, NOW.isoformat(), NOW.isoformat()))
            batch = self.store.begin_analysis(self.boxes, 120, 'private', run)
            if batch['analysis_id']:
                self.finish(batch, run)

    def test_its_queries_use_the_waiting_indexes(self):
        with self.store.connect() as db:
            for query, args in ((f'SELECT {catch_up.SLIM} FROM events WHERE account_id=? AND analyzed_version<version AND deferrals<? AND occurred_at<=? '
                                 'ORDER BY occurred_at DESC LIMIT ?', ('a', 2, 'x', 5)),
                                ('SELECT deferrals,ingested_at,id FROM events WHERE account_id=? AND analyzed_version<version AND deferrals<? '
                                 'ORDER BY deferrals,ingested_at,id LIMIT ?', ('a', 2, 5))):
                plan = ' '.join(r['detail'] for r in db.execute('EXPLAIN QUERY PLAN ' + query, args))
                self.assertIn('USING INDEX events_pending', plan)


class Sealed(CatchUp):
    """The same with message contents sealed."""
    protect = True


class Backlog(unittest.TestCase):
    def test_the_reported_set_is_the_one_frozen_before_the_order_was_worked_out(self):
        self.assertEqual(review_backlog.digest('held'), review_backlog.HELD_SHA)


if __name__ == '__main__':
    unittest.main()
