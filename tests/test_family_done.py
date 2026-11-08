"""Already did this, in a Family Fleet (Fleet.handled_round, family.DONE): a to-do one member closed as done shows on the
same to-do of another (same email, or the same bill), who and when only, and nothing closes by itself. A fake relay
stands in for the control plane; all names, mail and bills are made up, and nothing is sent anywhere."""
import json
import unittest

import test_family as tfam
import test_fleet as tf
from test_fleet import NOW, a, mail

fleet, family = a.fleet, a.fleet.family
FAM = tfam.FAM
BILL = 'Please pay EUR 37.77 to BE71 0961 2345 6769 with reference +++090/9337/55493+++ by the 19th.'
BILL_KEY = 'bill:BE71096123456769|090933755493'


class DoneRelay(tfam.FamilyRelay):
    """/claims as the control plane gives it: who holds a key, and since when."""
    def __init__(self):
        super().__init__()
        self.at = {}

    def call(self, method, path, body=None, timeout=40):
        if path == '/claims' and body.get('fleet') == FAM:
            self.calls.append((method, path, body))
            names = {m['member_id']: m['name'] for f in self.directory['fleets'] if f.get('id') == FAM for m in f['members']}
            return {'claims': {k: {'member_id': v, 'name': names.get(v, 'Owner'), 'mine': v == 'fm_me', 'at': self.at.get(k, '2026-11-09T08:00:00+00:00')}
                               for k, v in self.claims.items() if k in body['keys']}}
        if path == '/claim' and body.get('fleet') == FAM and not body.get('release'):
            self.calls.append((method, path, body))
            self.claims.setdefault(body['key'], 'fm_me')
            return {'mine': self.claims[body['key']] == 'fm_me'}
        return super().call(method, path, body, timeout)


class FamilyDone(unittest.TestCase):
    def setUp(self):
        tf.Fleet.setUp(self)
        self.relay = DoneRelay()
        self.relay.directory['fleets'] = self.relay.directory['fleets'][1:]  # a Family only: no Work rules in the way
        self.fleet = fleet.Fleet(self.store.connect, tf.CONFIG, lambda: 'token', relay=self.relay)
        self.fleet.directory(refresh=True)
        self.app = object.__new__(a.App)
        self.app.store, self.app.config, self.app.fleet = self.store, tf.CONFIG, self.fleet

    def todo(self, key, status='pending', message_id=None, body='Sign up for the school trip.', decided=None):
        event_ids = []
        if message_id:
            letter = mail('home', 1, 'School <office@school.example>', 'owner@gmail.com', message_id=message_id)
            self.store.commit_page('home', {}, [letter])
            with self.store.connect() as db:
                event_ids = [db.execute('SELECT id FROM events WHERE source_id=?', (letter['source_id'],)).fetchone()[0]]
        with self.store.connect() as db:
            db.execute('INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,?,?,?,?,?)',
                       ('c-' + key, key, 'A to-do', body, json.dumps(event_ids), '["home"]', status, NOW.isoformat()))
            if decided:
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,'','dashboard',?)",
                           ('d-' + key, 'c-' + key, decided, NOW.isoformat()))
        return 'c-' + key

    def key(self, source):
        return fleet.Fleet.handled_key('f' * 64, 'done', source)

    def row(self, card):
        with self.store.connect() as db:
            return dict(db.execute('SELECT status,handled_hint,done_elsewhere FROM suggestions WHERE id=?', (card,)).fetchone())

    def line(self, card):
        found = self.row(card)['done_elsewhere']
        return json.loads(found) if found else None

    def test_a_bill_is_its_iban_and_payment_reference_both_checked(self):
        self.assertEqual(family.bill_of(BILL), BILL_KEY[5:])
        self.assertEqual(family.bill_of('IBAN BE71096123456769, ref. RF18 5390 0754 7034'), 'BE71096123456769|RF18539007547034')
        self.assertIsNone(family.bill_of('Pay to BE71 0961 2345 6769.'))  # an account alone isn't one bill: rent, every month
        self.assertIsNone(family.bill_of('BE71 0961 2345 6768 +++090/9337/55493+++'))  # not a real IBAN
        self.assertIsNone(family.bill_of('BE71 0961 2345 6769 +++090/9337/55494+++'))  # nor a real reference
        self.assertIsNone(family.bill_of(''))

    def test_only_done_goes_out_and_only_as_a_code(self):
        self.todo('paid', 'completed', '<letter-1@school.example>', BILL, decided='complete')
        self.todo('skip', 'rejected', '<letter-2@school.example>', decided='reject')
        for _ in range(2):
            self.fleet.handled_round()
        sent = sorted(c['key'] for c in self.relay.sent('/claim'))
        self.assertEqual(sent, sorted([self.key('letter-1@school.example'), self.key(BILL_KEY)]))  # Not needed stays home; once
        self.assertNotIn('letter-1', json.dumps(self.relay.calls))
        self.assertNotIn('BE71', json.dumps(self.relay.calls))
        self.assertNotIn('37.77', json.dumps(self.relay.calls))

    def test_a_to_do_someone_did_shows_who_and_when_and_stays_open(self):
        mail_todo = self.todo('letter', message_id='<letter-3@school.example>')
        bill_todo = self.todo('bill', body=BILL)
        other = self.todo('other', message_id='<letter-4@school.example>')
        self.relay.claims[self.key('letter-3@school.example')] = 'fm_robin'
        self.relay.claims[self.key(BILL_KEY)] = 'fm_alex'
        self.relay.at[self.key(BILL_KEY)] = '2026-11-07T18:30:00+00:00'
        self.fleet.handled_round()
        self.assertEqual(self.line(mail_todo), {'name': 'Robin', 'member_id': 'fm_robin', 'fleet': FAM, 'at': '2026-11-09T08:00:00+00:00'})
        self.assertEqual(self.line(bill_todo)['name'], 'Alex')
        self.assertEqual(self.line(bill_todo)['at'], '2026-11-07T18:30:00+00:00')
        self.assertIsNone(self.line(other))
        for card in (mail_todo, bill_todo):  # never closed, never "Looks done"
            self.assertEqual((self.row(card)['status'], self.row(card)['handled_hint']), ('pending', None))
        row = next(r for r in self.store.snapshot([])['suggestions'] if r['id'] == mail_todo)
        self.assertEqual(json.loads(row['done_elsewhere'])['name'], 'Robin')  # the dashboard gets it
        self.relay.claims.clear()  # Robin and Alex reopened theirs
        self.fleet.handled_round()
        self.assertEqual((self.line(mail_todo), self.line(bill_todo)), (None, None))

    def test_still_needed_keeps_it_quiet_until_theirs_is_reopened(self):
        card = self.todo('letter', message_id='<letter-5@school.example>')
        self.relay.claims[self.key('letter-5@school.example')] = 'fm_robin'
        self.fleet.handled_round()
        with self.assertRaisesRegex(ValueError, 'dashboard'):  # the owner's own tap, never an agent's
            self.app.action('family_still_needed', {'suggestion_id': card})
        self.assertEqual(self.app.action('family_still_needed', {'suggestion_id': card}, owner_dashboard=True), {'kept': True})
        self.assertIn('family_still_needed', a.FAMILY_ACTIONS)
        self.fleet.handled_round()
        self.assertTrue(self.line(card)['kept'])
        self.assertEqual(self.row(card)['status'], 'pending')
        self.relay.claims.clear()
        self.fleet.handled_round()
        self.assertIsNone(self.line(card))
        self.relay.claims[self.key('letter-5@school.example')] = 'fm_robin'  # done again later: it shows again
        self.fleet.handled_round()
        self.assertFalse(self.line(card).get('kept'))
        with self.assertRaisesRegex(ValueError, 'Unknown to-do'):
            self.fleet.keep_done_elsewhere('c-nope')

    def test_the_family_rule_turns_it_off_both_ways(self):
        card = self.todo('letter', message_id='<letter-6@school.example>')
        self.todo('paid', 'completed', '<letter-7@school.example>', decided='complete')
        self.relay.claims[self.key('letter-6@school.example')] = 'fm_robin'
        self.fleet.set_rule(FAM, 'fm_robin', family.DONE, 'never')  # not from Robin
        self.fleet.handled_round()
        self.assertIsNone(self.line(card))
        self.fleet.set_rule(FAM, 'fm_robin', family.DONE, 'always')
        self.fleet.handled_round()
        self.assertEqual(self.line(card)['name'], 'Robin')
        for member in ('fm_robin', 'fm_alex'):  # sharing off with everyone: the line goes, nothing new goes out
            self.fleet.set_rule(FAM, member, family.DONE, 'never')
        calls = len(self.relay.sent('/claim'))
        self.fleet.handled_round()
        self.assertIsNone(self.line(card))
        self.assertFalse([c for c in self.relay.sent('/claim')[calls:] if not c.get('release')])
        with self.assertRaises(ValueError):  # who and when only: no Ask me first
            self.fleet.set_rule(FAM, 'fm_robin', family.DONE, 'ask')

    def test_a_family_default_is_on_and_it_is_a_rule_not_a_question(self):
        self.assertEqual(family.DEFAULT_RULES[family.DONE], 'always')
        self.assertIn(family.DONE, fleet.RULE_KINDS['family'])
        self.assertNotIn(family.DONE, fleet.ASKS['family'])
        self.assertNotIn(family.DONE, fleet.RULE_KINDS['work'])


if __name__ == '__main__':
    unittest.main()
