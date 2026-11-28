"""Work that only shows across separate threads (opportunities.py): off unless turned on; a ledger of a few checked facts
per thread, read again only when the thread changes; candidate groups found in code; two judging turns per area, never
across, and only what both propose; code checks every quote, date, organization, to-do and earlier join; a quiet
Machine keeps only clear, Graph-tied work; value first, at most CAP a week. Made-up data, a stand-in model."""
import datetime as dt
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import graph
import machine.main as machine_main
import opportunities
import timeutil

NOW = dt.datetime(2026, 11, 9, 18, tzinfo=dt.timezone.utc)
ACCOUNTS = [{'id': 'w', 'service': 'gmail', 'boundary': 'work:Larkspur', 'email': 'robin@larkspur.example'},
            {'id': 'p', 'service': 'gmail', 'boundary': 'personal:home', 'email': 'robin@mail.example'}]
NOISE = ('alpine banjo cactus dolphin ember falcon glacier harbor igloo jasmine kettle lantern meadow nectar orchid pepper '
         'quartz raven saffron tundra umbrella velvet walnut yonder').split()


class Opportunities(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        timeutil.pin(NOW)
        self.addCleanup(timeutil.pin, None)
        self.store = machine_main.Store(Path(self.temp.name) / 'o.sqlite')
        self.store.accounts = ACCOUNTS
        self.addCleanup(setattr, machine_main.Store, 'accounts', [])
        self.app = object.__new__(machine_main.App)
        self.app.store, self.app.config, self.app.fleet = self.store, {'accounts': ACCOUNTS}, None
        self.n, self.prompts, self.facts, self.judged = 0, [], {}, []
        self.verdict = lambda events, sample: None  # {event ids of the group's threads} -> one group's answer, or None
        self.app.opportunity_model = self.model
        quiet = mock.patch.object(opportunities, 'QUIET_LINKED', 0)  # small corpora are quiet; the quiet gate has its own test
        quiet.start()
        self.addCleanup(quiet.stop)
        for account in ('w', 'p'):  # other mail, so word scores work as in a real inbox
            for i in range(8):
                e = self.mail(account, f'other{i}', f'Sender {i} <s{i}@other{i}.example>', f'Note {i}', f'About {NOISE[i]} and {NOISE[i + 8]}.', days=10 + i)
                self.fact(e, f'{NOISE[i]} {NOISE[i + 8]} {NOISE[i + 16]}', f'About {NOISE[i]} and {NOISE[i + 8]}')

    def model(self, config, text):
        self.prompts.append(text)
        blocks = {int(n): [int(e) for e in re.findall(r'^  E(\d+) \|', body, re.M)]
                  for n, body in re.findall(r'^T(\d+)\b[^\n]*\n((?:  .*\n?)+)', text, re.M)}
        if text.startswith('Background task'):  # the ledger turn
            return json.dumps({f'T{n}': [f for e in ids for f in self.facts.get(e, [])] for n, ids in blocks.items()})
        sample = sum(1 for p in self.prompts if p.startswith('Weekly') and p.split('\n', 1)[0] == text.split('\n', 1)[0]) - 1
        out = {}
        for g, members in re.findall(r'^G(\d+): threads (.+)$', text, re.M):
            events = {e for t in re.findall(r'T(\d+)', members) for e in blocks[int(t)]}
            self.judged.append(events)
            out[f'G{g}'] = self.verdict(events, sample % 2) or {'propose': False}
        return json.dumps(out)

    def mail(self, account, thread, sender, subject, body, bulk=False, days=3):
        self.n += 1
        meta = {'from': sender, 'to': ACCOUNTS[0 if account == 'w' else 1]['email'], 'thread_id': thread, 'labels': ['INBOX']}
        if bulk:
            meta['list_unsubscribe'] = '<mailto:u@list.example>'
        self.store.commit_page(account, {}, [{'account_id': account, 'source_id': f's{self.n}', 'kind': 'gmail.message', 'deleted': False,
                                              'occurred_at': (NOW - dt.timedelta(days=days)).isoformat(), 'title': subject, 'body': body, 'metadata': meta}])
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (f's{self.n}',)).fetchone()[0]

    def fact(self, event, about, quote, kind='need', date=''):
        self.facts.setdefault(event, []).append({'kind': kind, 'about': about, 'date': date, 'source': f'E{event}', 'quote': quote})

    def run_once(self, current=NOW):
        timeutil.pin(current)
        with self.store.connect() as db:
            run_id = opportunities.begin(db)
        made = self.app.opportunity_run(run_id, current)
        with self.store.connect() as db:
            cards = [dict(r) for r in db.execute("SELECT title,body,event_ids FROM suggestions WHERE dedupe_key LIKE 'opportunity:%'")]
            db.execute('DELETE FROM opportunity_runs')
            db.commit()
        return made, cards

    def boxes(self, second='Ben Cole <ben@birch.example>', days=3):
        a = self.mail('w', 'a', 'Ana Ruiz <ana@quarry.example>', 'Carton price', 'From 1 January our mailer boxes cost 12% more.', days=days)
        b = self.mail('w', 'b', second, 'Quote', 'We can supply mailer boxes at 0.41 each.', days=days)
        self.fact(a, 'mailer boxes cardboard cartons price increase', 'our mailer boxes cost 12% more', 'price')
        self.fact(b, 'mailer boxes cardboard cartons supply quote', 'We can supply mailer boxes at 0.41', 'offer')
        return a, b

    def proposal(self, a, b, title='Compare the mailer box quotes before January', work='Ben quoted 0.41 a box.', value=3,
                 why='Quarry raises prices from 1 January and Birch quoted less.'):
        return {'propose': True, 'value': value, 'title': title, 'why': why, 'work': work,
                'quotes': [{'source': f'E{a}', 'quote': 'our mailer boxes cost 12% more'}, {'source': f'E{b}', 'quote': 'mailer boxes at 0.41'}]}

    def test_off_by_default(self):
        self.app.config['review_worker'] = {'enabled': True}
        self.assertIsNone(self.app.opportunity_step())
        self.assertFalse(opportunities.on({}))
        self.assertTrue(opportunities.on({'opportunities': True}))

    def test_two_threads_about_one_thing_make_a_to_do_without_made_up_dates(self):
        a, b = self.boxes()
        p = self.proposal(a, b, work='Ben quoted 0.41 a box. Order before December 15 to save.')
        self.verdict = lambda events, sample: p if {a, b} <= events else None
        made, cards = self.run_once()
        self.assertEqual(1, made)
        self.assertIn('1 January', cards[0]['body'])
        self.assertNotIn('December 15', cards[0]['body'])  # a date the messages don't give is taken out
        self.assertEqual(sorted([a, b]), sorted(json.loads(cards[0]['event_ids'])))
        self.assertEqual(0, self.run_once()[0])  # the same threads are never joined twice

    def test_the_ledger_reads_a_thread_again_only_when_it_changes(self):
        a, b = self.boxes()
        self.run_once()
        self.assertEqual(1, sum('Carton price' in p for p in self.prompts if p.startswith('Background task')))
        self.prompts.clear()
        self.run_once(NOW + dt.timedelta(days=7))
        self.assertFalse(any(p.startswith('Background task') for p in self.prompts))  # nothing new: nothing read
        self.assertFalse(any(p.startswith('Weekly') for p in self.prompts))  # and the group judged before is not asked again
        self.mail('w', 'b', 'Ben Cole <ben@birch.example>', 'Re: Quote', 'The 0.41 holds until spring.', days=-6)
        self.prompts.clear()
        self.run_once(NOW + dt.timedelta(days=7))
        ledger = [p for p in self.prompts if p.startswith('Background task')]
        self.assertEqual(1, len(ledger))
        self.assertIn('Re: Quote', ledger[0])
        self.assertNotIn('Carton price', ledger[0])

    def test_a_fact_needs_its_quote_and_a_date_its_day(self):
        a, b = self.boxes()
        self.facts[a].append({'kind': 'date', 'about': 'price change day', 'date': '2027-01-02', 'source': f'E{a}', 'quote': 'From 1 January'})
        self.facts[b].append({'kind': 'need', 'about': 'mailer boxes cartons', 'date': '', 'source': f'E{b}', 'quote': 'words nobody wrote'})
        self.run_once()
        with self.store.connect() as db:
            kept = {r['thread']: json.loads(r['facts']) for r in db.execute('SELECT thread,facts FROM opportunity_facts')}
        self.assertEqual(['price'], [f['kind'] for f in kept['w|a']])  # 2 January is not the day the message gives
        self.assertEqual(['offer'], [f['kind'] for f in kept['w|b']])

    def test_one_shared_word_or_one_person_makes_no_candidate(self):
        a = self.mail('w', 'a', 'Emma Clarke <emma@clarke.example>', 'Seafoam order', 'Two skeins of Seafoam please.')
        b = self.mail('w', 'b', 'Emma Dyer <emma.dyer@dyer.example>', 'Restock?', 'Will the shop be open on Monday?')
        self.fact(a, 'yarn skeins wool order', 'Two skeins of Seafoam', 'need')
        self.fact(b, 'shop opening hours order', 'Will the shop be open', 'need')
        c = self.mail('w', 'c', 'Ana Ruiz <ana@quarry.example>', 'Carton price', 'Our mailer boxes cost 12% more.')
        d = self.mail('w', 'd', 'Ana Ruiz <ana@quarry.example>', 'Cartons', 'Mailer boxes are back in stock.')
        self.fact(c, 'mailer boxes cardboard cartons price increase', 'Our mailer boxes cost 12% more', 'price')
        self.fact(d, 'mailer boxes cardboard cartons stock', 'Mailer boxes are back in stock', 'offer')
        self.run_once()
        self.assertEqual([], self.judged)
        self.assertFalse(any(p.startswith('Weekly') for p in self.prompts))

    def test_one_judging_pair_per_area_never_across_and_bulk_stays_out(self):
        self.boxes()
        self.mail('w', 'n', 'news@weekly.example', 'Tips', 'Weekly tips about mailer boxes', bulk=True)
        c = self.mail('p', 'c', 'Mia <mia@mail.example>', 'Dinner', 'Dinner on Friday 13 November at our place?')
        d = self.mail('p', 'd', 'Tom <tom@mail.example>', 'Visit', 'We land on Friday 13 November in the evening.')
        self.fact(c, 'dinner invitation evening', 'Dinner on Friday 13 November', 'date', '2026-11-13')
        self.fact(d, 'family visit arrival evening', 'We land on Friday 13 November', 'date', '2026-11-13')
        self.run_once()
        judging = [p for p in self.prompts if p.startswith('Weekly')]
        self.assertEqual(4, len(judging))  # two samples per area
        work = [p for p in judging if 'work mail' in p]
        self.assertEqual(2, len(work))
        self.assertTrue(all('Dinner on Friday' not in p and 'Weekly tips' not in p for p in work))
        self.assertTrue(all('mailer boxes' not in p for p in judging if 'personal mail' in p))

    def test_only_what_both_samples_propose_is_kept(self):
        a, b = self.boxes()
        self.verdict = lambda events, sample: self.proposal(a, b) if sample == 0 else None
        self.assertEqual(0, self.run_once()[0])
        with self.store.connect() as db:
            db.execute('DELETE FROM opportunity_asked')
            db.commit()
        self.verdict = lambda events, sample: self.proposal(a, b, value=2 if sample else 3)
        self.assertEqual(1, self.run_once()[0])

    def test_value_one_is_no_proposal(self):
        a, b = self.boxes()
        self.verdict = lambda events, sample: self.proposal(a, b, value=1)
        self.assertEqual(0, self.run_once()[0])

    def test_a_date_already_over_or_a_title_with_a_made_up_date_is_dropped(self):
        a = self.mail('w', 'a', 'Leon Hart <leon@brightline.example>', 'Tickets', 'Free tickets for the boat show on October 24, stand 112.', days=20)
        b = self.mail('w', 'b', 'Victor Lamb <victor@lamb.example>', 'Show?', 'Are you going to the boat show on the 24th? Engines to see.', days=18)
        self.fact(a, 'boat show trade fair tickets', 'Free tickets for the boat show', 'offer')
        self.fact(b, 'boat show trade fair visit engines', 'going to the boat show', 'need')
        shown = {'propose': True, 'value': 3, 'title': 'Offer Victor a boat show ticket', 'why': 'Leon has tickets for October 24.',
                 'work': 'To Victor: shall we meet at stand 112 on October 24?',
                 'quotes': [{'source': f'E{a}', 'quote': 'Free tickets for the boat show'}, {'source': f'E{b}', 'quote': 'going to the boat show'}]}
        self.verdict = lambda events, sample: shown
        self.assertEqual(0, self.run_once()[0])  # October 24 is over on November 9
        self.assertTrue(opportunities.all_dates_over('the show on October 24', NOW))
        self.assertFalse(opportunities.all_dates_over('the show on October 24, the next on November 20', NOW))
        self.assertFalse(opportunities.all_dates_over('no date at all', NOW))
        a2, b2 = self.boxes()
        self.verdict = lambda events, sample: self.proposal(a2, b2, title='Switch mailer boxes to Birch by December 1') if a2 in events else None
        self.assertEqual(0, self.run_once()[0])

    def test_not_needed_on_every_threads_to_do_drops_it(self):
        a, b = self.boxes()
        for n, event in enumerate((a, b)):
            card = self.store.suggest(f'test:{n}', f'Reply about the boxes {n}', 'Reply.', [event])
            self.store.decide(card['id'], 'reject', '', f'd-{n}', 'dashboard')
        self.verdict = lambda events, sample: self.proposal(a, b)
        self.assertEqual(0, self.run_once()[0])

    def test_several_organizations_get_one_message_each(self):
        a, b = self.boxes()
        self.verdict = lambda events, sample: self.proposal(a, b, work='Hi Ana and Ben, we pick one supplier for the boxes.')
        self.assertEqual(0, self.run_once()[0])
        people = {'mara@fernhill.example': 'Mara Lind', 'liesel@penrose.example': 'Liesel Penn'}
        self.assertTrue(opportunities.group_mail('Hi Mara and Liesel, we run one session.', people))
        self.assertTrue(opportunities.group_mail('Send it with Liesel in cc.', people))
        self.assertFalse(opportunities.group_mail('Write to each separately. Hi Mara, we run a session.', people))
        self.assertFalse(opportunities.group_mail('Hi Mara and Liesel', {'mara@fernhill.example': 'Mara Lind', 'liesel@fernhill.example': 'Liesel Penn'}))

    def test_a_title_says_one_message_each(self):
        a, b = self.boxes()
        self.verdict = lambda events, sample: self.proposal(a, b, title='Ask Quarry and Birch for box prices together')
        self.assertEqual(0, self.run_once()[0])
        self.assertIn('never "together"', next(p for p in self.prompts if p.startswith('Weekly')))

    def test_one_person_on_two_addresses_is_one_once_the_graph_joined_them(self):
        a, b = self.boxes('Ana Ruiz <ana.ruiz@birch.example>')
        with self.store.connect() as db:
            graph.merge(db, 'email:ana@quarry.example', 'email:ana.ruiz@birch.example', True, NOW.isoformat(), source='owner')
            db.commit()
            graph.build(db, self.app.config, NOW.isoformat())
            db.commit()
        self.verdict = lambda events, sample: self.proposal(a, b)
        self.assertEqual(0, self.run_once()[0])  # the "two offers" are one person's: no candidate at all
        self.assertEqual([], self.judged)

    def test_a_quiet_machine_keeps_only_clear_graph_tied_work(self):
        a, b = self.boxes()
        self.verdict = lambda events, sample: self.proposal(a, b)
        with mock.patch.object(opportunities, 'QUIET_LINKED', 12):
            self.assertEqual(0, self.run_once()[0])  # value 3, but nothing the Graph ties: Quarry and Birch
        c = self.mail('w', 'c', 'Ana Ruiz <ana@quarry.example>', 'Export bug', 'The export drops the last row of the invoice report.')
        d = self.mail('w', 'd', 'Ben Cole <ben@quarry.example>', 'Rollout', 'Our second office needs the invoice report export next week.')
        self.fact(c, 'invoice report export missing rows bug', 'The export drops the last row', 'problem')
        self.fact(d, 'invoice report export rollout second office', 'needs the invoice report export', 'need')
        with self.store.connect() as db:
            graph.build(db, self.app.config, NOW.isoformat())
            db.commit()
        quotes = [{'source': f'E{c}', 'quote': 'The export drops the last row'}, {'source': f'E{d}', 'quote': 'needs the invoice report export'}]
        fix = {'propose': True, 'value': 2, 'title': 'Fix the invoice export before the second office starts', 'why': 'One company, one bug.',
               'work': 'Plan: fix the last-row bug, then roll out.', 'quotes': quotes}
        self.verdict = lambda events, sample: fix if c in events else None
        with mock.patch.object(opportunities, 'QUIET_LINKED', 12):
            self.assertEqual(0, self.run_once()[0])  # tied, but only useful: not on a quiet Machine
            with self.store.connect() as db:
                db.execute('DELETE FROM opportunity_asked')
                db.commit()
            fix['value'] = 3
            self.assertEqual(1, self.run_once()[0])  # clear work, and the same organization as the Graph resolved it

    def test_value_first_and_at_most_cap(self):
        made = [{'title': f't{n}', 'value': v, 'rank': n} for n, v in enumerate((2, 3, 2, 3, 3, 3, 2))]
        kept = opportunities.keep(made)
        self.assertEqual(['t1', 't3', 't4', 't5'], [p['title'] for p in kept])
        self.assertEqual(['t0', 't2'], [p['title'] for p in opportunities.keep([p for p in made if p['value'] == 2])])
        self.assertEqual(opportunities.CAP, len(kept))

    def test_dates(self):
        self.assertEqual({('md', 12, 4)}, opportunities.dates_in('Inspection on 4 December.'))
        self.assertEqual({('md', 12, 4)}, opportunities.dates_in('le 4 décembre'))
        self.assertEqual({('md', 11, 15)}, opportunities.dates_in('by November 15th'))
        self.assertIn(('md', 12, 10), opportunities.dates_in('closed Wednesday 9 to Friday 11 December'))  # a range holds each day
        self.assertIn(('md', 12, 10), opportunities.dates_in('vom 9. bis 11. Dezember'))
        self.assertEqual('Ben quoted less.', opportunities.without_made_up_dates('Ben quoted less. Sign by November 15.', set()))
        self.assertTrue(opportunities.past_timing('a shared session in the first week of November', NOW))
        self.assertTrue(opportunities.past_timing('Send it by 30 October.', NOW))
        self.assertFalse(opportunities.past_timing('the invoice of 3 November shows the old rate', NOW))  # when it happened, not when to act
        self.assertFalse(opportunities.past_timing('book it for Thursday 10 December', NOW))
        self.assertFalse(opportunities.past_timing('by the end of November', NOW))


if __name__ == '__main__':
    unittest.main()
