"""Scheduling between Machines when the other person has no Machine (meet_link.py): a booking link in the email draft.
A sandbox Machine (test_meet's harness) and a local stand-in for the cloud's task links: it keeps sealed blobs it
can't open and passes on sealed replies, as the cloud does. The person's page is played here with the link's key,
as pick.js does in their browser. No network, no calendar writes: booking is a hook that records what it was asked."""
import datetime as dt
import json
import tempfile
import unittest

import meet
import meet_link
import task_invites
import test_meet as tm


class Links:
    """The cloud's task links for one Machine: create, update, status, revoke. Sealed blobs only."""
    def __init__(self):
        self.links, self.n = {}, 0

    def call(self, body):
        action = body['action']
        if action == 'create':
            assert body['kind'] == 'schedule' and body['days'] in (7, 14)
            for found in self.links.values():  # a retry of the same request makes no second link
                if found['request_id'] == body['request_id']:
                    return {'id': found['id'], 'url': 'https://themachine.computer/t/' + found['id'], 'expires_at': found['expires']}
            self.n += 1
            link_id = ('L%d' % self.n).ljust(22, 'x')
            expires = (tm.MONDAY.date() + dt.timedelta(days=body['days'])).isoformat()
            self.links[link_id] = {'id': link_id, 'sealed': body['sealed'], 'check': body['check'], 'request_id': body['request_id'],
                                   'replies': [], 'expires': expires, 'days': body['days']}
            return {'id': link_id, 'url': 'https://themachine.computer/t/' + link_id, 'expires_at': expires}
        if action == 'update':
            self.links[body['id']]['sealed'] = body['sealed']
            return {'ok': True}
        if action == 'revoke':
            self.links.pop(body['id'], None)
            return {'ok': True}
        if action == 'status':
            seen = body.get('seen') or {}
            return {'replies': {i: [r for r in self.links[i]['replies'] if r['n'] > seen.get(i, 0)] for i in body['ids'] if i in self.links}}
        raise ValueError(action)

    # the person's browser (pick.js): opens the page with the link's key, and seals a pick with its reply key
    def page(self, link):
        link_id, key = task_invites.LINK.fullmatch(link).groups()
        return task_invites._open(self.links[link_id]['sealed'], key)

    def pick(self, link, slot, key=None):
        link_id, real = task_invites.LINK.fullmatch(link).groups()
        sealed, _ = task_invites.seal({'answer': 'pick', 'slot': slot}, task_invites._unb64(task_invites.derived(key or real, 'reply')))
        found = self.links[link_id]
        found['replies'].append({'n': len(found['replies']) + 1, 'sealed': sealed})


class LinkRelay(tm.Relay):
    def __init__(self, net, me, links):
        super().__init__(net, me)
        self.links = links

    def call(self, method, path, body=None, timeout=40):
        if path == '/task-invite':
            if self.down:
                raise tm.fleet.Unavailable('away')
            return self.links.call(body)
        return super().call(method, path, body, timeout)


class BookingLinks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.net, self.links = tm.MeetNetwork(), Links()
        self.ann = tm.Machine(self.temp.name, self.net, 'ann', 'ann@one.example')
        relay = self.ann.relay  # the stand-in the Fleet's relay calls through
        relay.__class__ = LinkRelay
        relay.links = self.links
        self.ann.box.config['owner_name'] = 'Ann Example'
        self.ann.box.meet_tell()
        self.drafts = {}  # card -> (to, body): the to-do's email draft
        self.ann.box.meet_link_draft = self.draft

    def draft(self, card_id, email, lines):
        if card_id not in self.drafts or self.drafts[card_id][0] != email:
            return False
        self.drafts[card_id] = (email, meet_link.with_lines(self.drafts[card_id][1], lines))
        return True

    def start(self, email='carol@three.example', **kw):
        self.drafts['c1'] = (email, 'Hi Carol,\n\nHappy to meet next week.\n\nBest,\nAnn')
        self.ann.busy('2026-11-03T09:00:00+00:00', '2026-11-03T12:00:00+00:00', 'Secret merger call', visibility='private')
        self.assertEqual(self.ann.box.meet_start('c1', email, 'Carol Sample', minutes=30, start='2026-11-03', days=kw.get('days', 3)), 'fallback')
        self.ann.box.meet_round()
        return self.link()

    def link(self):
        found = task_invites.LINK.search(self.drafts['c1'][1])
        return found.group(0) if found else None

    def record(self):
        with self.ann.connect() as db:
            row = db.execute('SELECT * FROM meet_links').fetchone()
        return row['state'], json.loads(row['record'])

    def test_no_machine_puts_a_link_to_free_times_in_the_draft(self):
        link = self.start()
        body = self.drafts['c1'][1]
        self.assertIn('\n\n[Pick a time](' + link + ')\n\nBest,', body)  # the link behind its words
        self.assertNotIn('Get yours', body)  # no branding in the email: the footer is on the page only
        self.assertNotIn('Machine', body)
        page = self.links.page(link)
        self.assertEqual(set(page), {'kind', 'from_name', 'minutes', 'slots', 'brand'})  # nothing else about Ann
        self.assertEqual((page['kind'], page['from_name'], page['minutes'], page['brand']), ('schedule', 'Ann', 30, True))
        # free starts only: on the grid, in work hours, not in her 9-12 (plus buffer), in the asked window, six a day at most
        starts = [meet.parse_slot(s) for s in page['slots']]
        self.assertTrue(starts and all(s.minute % 15 == 0 and 9 <= s.hour < 17 for s in starts))
        self.assertFalse([s for s in starts if s.date() == dt.date(2026, 11, 3) and s.hour < 12])
        self.assertTrue(all(dt.date(2026, 11, 3) <= s.date() <= dt.date(2026, 11, 5) for s in starts))
        self.assertLessEqual(max(sum(1 for s in starts if s.date() == d) for d in {s.date() for s in starts}), meet_link.PER_DAY)
        # the cloud keeps a blob it can't read
        stored = json.dumps(self.links.links)
        for word in ('Secret', 'merger', 'Carol', 'carol@', 'Ann', page['slots'][0]):
            self.assertNotIn(word, stored)
        self.assertEqual(next(iter(self.links.links.values()))['days'], 7)
        self.assertEqual([l['what'] for l in self.ann.log()], ['fallback', 'link'])
        self.assertEqual(self.ann.booked, [])

    def test_a_pick_is_a_to_do_and_only_book_it_books(self):
        link = self.start()
        slot = self.links.page(link)['slots'][2]
        self.links.pick(link, slot)
        self.ann.box.meet_round()
        self.assertEqual(self.ann.booked, [])  # nothing before the owner's tap
        (card, title), = self.ann.cards.items()
        start = meet.parse_slot(slot)
        self.assertEqual(title, 'Meet Carol Sample')
        self.assertEqual(self.record()[0], 'picked')
        with self.ann.connect() as db:
            view = [{'id': card}, {'id': 'c1'}]
            self.ann.box.annotate_links(db, view)
        self.assertEqual((view[0]['meet']['state'], view[0]['meet']['role'], view[0]['meet']['start']), ('picked', 'link', slot))
        self.assertEqual(view[1]['meet']['state'], 'link')
        self.assertEqual(self.ann.box.meet_decide(card, 'book'), {'state': 'booked'})
        end = meet.slot_text(start + dt.timedelta(minutes=30))
        self.assertEqual(self.ann.booked, [{'slot': [slot, end], 'email': 'carol@three.example', 'video': None}])
        self.assertEqual(self.links.links, {})  # revoked: the page is gone
        self.assertEqual(self.record()[0], 'booked')
        self.assertNotIn('key', self.record()[1])
        self.assertIn(card, self.ann.closed)
        self.assertEqual([(l['what'], l['outcome']) for l in self.ann.log()][1:],
                         [('link', 'made'), ('picked_in', 'waiting'), ('booked', 'booked')])
        with self.assertRaisesRegex(ValueError, 'no longer open'):
            self.ann.box.meet_decide(card, 'book')

    def test_not_needed_ends_the_link_without_booking(self):
        link = self.start()
        self.links.pick(link, self.links.page(link)['slots'][0])
        self.ann.box.meet_round()
        card = next(iter(self.ann.cards))
        self.assertEqual(self.ann.box.meet_decide(card, 'skip'), {'state': 'canceled'})
        self.assertEqual((self.ann.booked, self.links.links, self.record()[0]), ([], {}, 'closed'))
        with self.assertRaisesRegex(ValueError, 'no longer open'):
            self.ann.box.meet_decide(card, 'book')

    def test_only_an_offered_time_sealed_with_the_links_key_counts(self):
        link = self.start()
        page = self.links.page(link)
        self.links.pick(link, '2026-11-03T09:00Z')  # not offered: inside Ann's busy block
        self.links.pick(link, page['slots'][0], key=task_invites.seal({})[1])  # sealed with another key
        self.ann.box.meet_round()
        self.assertEqual(self.ann.cards, {})
        self.assertEqual(self.record()[1]['seen'], 2)

    def test_a_time_no_longer_free_makes_no_to_do(self):
        link = self.start()
        slot = self.links.page(link)['slots'][0]
        start = meet.parse_slot(slot)
        self.ann.busy(start.isoformat(), (start + dt.timedelta(hours=1)).isoformat(), 'Late booking')
        self.links.pick(link, slot)
        self.ann.box.meet_round()
        self.assertEqual(self.ann.cards, {})
        self.assertEqual(self.ann.log()[-1]['outcome'], 'taken')

    def test_the_page_follows_the_calendar(self):
        link = self.start()
        first = self.links.page(link)['slots'][0]
        start = meet.parse_slot(first)
        self.ann.busy(start.isoformat(), (start + dt.timedelta(hours=1)).isoformat(), 'Late booking')
        self.ann.clock += dt.timedelta(seconds=meet_link.REFRESH + 60)
        self.ann.box.meet_round()
        self.assertNotIn(first, self.links.page(link)['slots'])

    def test_the_footer_is_off_in_the_setting(self):
        self.ann.box.meet_set(brand=False)
        self.assertFalse(self.ann.box.meet_setting()['brand'])
        link = self.start()
        self.assertIn('[Pick a time](' + link + ')', self.drafts['c1'][1])
        self.assertFalse(self.links.page(link)['brand'])
        with self.assertRaises(ValueError):
            self.ann.box.meet_set(brand='no')

    def test_the_link_waits_for_its_draft_and_ends_if_the_email_went_without_it(self):
        self.drafts.pop('c1', None)
        self.ann.busy('2026-11-03T09:00:00+00:00', '2026-11-03T10:00:00+00:00')
        self.ann.box.meet_start('c1', 'carol@three.example', 'Carol', start='2026-11-03', days=2)
        self.ann.box.meet_round()
        self.assertEqual(self.record()[0], 'open')
        self.assertFalse(self.record()[1]['drafted'])
        self.ann.clock += dt.timedelta(days=meet_link.DRAFT_DAYS, minutes=1)
        self.ann.box.meet_round()
        self.assertEqual((self.record()[0], self.links.links), ('closed', {}))
        self.assertEqual(self.ann.log()[-1]['outcome'], 'unused')

    def test_a_draft_to_someone_else_gets_no_link(self):
        self.start(email='carol@three.example')
        self.drafts['c1'] = ('dave@four.example', 'Hi')
        self.assertFalse(self.draft('c1', 'carol@three.example', ['x']))

    def test_the_link_expires(self):
        link = self.start(days=10)
        self.assertEqual(next(iter(self.links.links.values()))['days'], 14)
        self.ann.clock += dt.timedelta(days=15)
        self.ann.box.meet_round()
        self.assertEqual(self.record()[0], 'expired')
        self.assertNotIn('key', self.record()[1])
        self.assertTrue(link)

    def test_a_declined_ask_gets_no_link(self):
        with self.ann.connect() as db:
            meet.ensure(db)
            db.execute("INSERT INTO meet_sessions(id,peer,role,email,card_id,state,start,days,minutes,note,created_at,updated_at) "
                       "VALUES(?, 'mt_x', 'asker', 'bob@two.example', 'c9', 'fallback', '2026-11-03', 2, 30, 'declined', ?, ?)",
                       ('d' * 32, meet.stamp(tm.MONDAY), meet.stamp(tm.MONDAY)))
        self.drafts['c9'] = ('bob@two.example', 'Hi')
        self.ann.box.meet_round()
        self.assertEqual(self.links.links, {})

    def test_the_network_away_tries_again(self):
        self.ann.relay.down = True
        self.drafts['c1'] = ('carol@three.example', 'Hi')
        self.ann.box.meet_start('c1', 'carol@three.example', 'Carol', start='2026-11-03', days=2)
        self.ann.box.meet_links_round()
        self.assertEqual(self.links.links, {})
        self.ann.relay.down = False
        self.ann.box.meet_links_round()
        self.assertEqual(len(self.links.links), 1)
        self.assertTrue(self.link())


if __name__ == '__main__':
    unittest.main()
