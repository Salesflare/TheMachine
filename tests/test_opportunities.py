"""Work that only shows across separate threads (opportunities.py): off unless turned on; one turn per area, never
across; threads are tied only by what the Graph resolved (the same confirmed person, organization or project) or two
independent signals in the messages code can check (never a name, first or full, nor one shared word), one person on
two addresses the Graph joined is one, with no date the messages don't give; at most two a week, the best of each area
first. Made-up data, the real Graph build, a stand-in model."""
import datetime as dt
import json
import re
import tempfile
import unittest
from pathlib import Path

import graph
import machine.main as machine_main
import opportunities
import timeutil

NOW = dt.datetime(2026, 11, 9, 18, tzinfo=dt.timezone.utc)
ACCOUNTS = [{'id': 'w', 'service': 'gmail', 'boundary': 'work:Larkspur', 'email': 'robin@larkspur.example'},
            {'id': 'p', 'service': 'gmail', 'boundary': 'personal:home', 'email': 'robin@mail.example'}]


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
        self.n, self.prompts, self.answers = 0, [], []
        self.app.opportunity_model = lambda config, text: (self.prompts.append(text), self.answers.pop(0) if self.answers else '{"proposals": []}')[1]

    def mail(self, account, thread, sender, subject, body, bulk=False, days=3):
        self.n += 1
        meta = {'from': sender, 'to': ACCOUNTS[0 if account == 'w' else 1]['email'], 'thread_id': thread, 'labels': ['INBOX']}
        if bulk:
            meta['list_unsubscribe'] = '<mailto:u@list.example>'
        self.store.commit_page(account, {}, [{'account_id': account, 'source_id': f's{self.n}', 'kind': 'gmail.message', 'deleted': False,
                                              'occurred_at': (NOW - dt.timedelta(days=days)).isoformat(), 'title': subject, 'body': body, 'metadata': meta}])
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (f's{self.n}',)).fetchone()[0]

    def run_once(self, current=NOW):
        timeutil.pin(current)
        with self.store.connect() as db:
            run_id = opportunities.begin(db)
        made = self.app.opportunity_run(run_id, current)
        with self.store.connect() as db:
            cards = [dict(r) for r in db.execute("SELECT title,body,event_ids FROM suggestions WHERE dedupe_key LIKE 'opportunity:%'")]
        return made, cards

    @staticmethod
    def answer(*proposals):
        return json.dumps({'proposals': list(proposals)})

    def test_off_by_default(self):
        self.app.config['review_worker'] = {'enabled': True}
        self.assertIsNone(self.app.opportunity_step())
        self.assertFalse(opportunities.on({}))
        self.assertTrue(opportunities.on({'opportunities': True}))

    def test_one_turn_per_area_and_bulk_stays_out(self):
        self.mail('w', 'a', 'Ana Ruiz <ana@quarry.example>', 'Export bug', 'The export drops the last row.')
        self.mail('w', 'b', 'Ben Cole <ben@birch.example>', 'Export', 'Our export misses the final row too.')
        self.mail('w', 'n', 'news@weekly.example', 'Tips', 'Weekly tips', bulk=True)
        self.mail('p', 'c', 'Mia <mia@mail.example>', 'Dinner', 'Dinner on Friday?')
        self.mail('p', 'd', 'Tom <tom@mail.example>', 'Visit', 'We visit on Friday.')
        self.run_once()
        self.assertEqual(2, len(self.prompts))
        work = next(p for p in self.prompts if 'work mail' in p)
        self.assertNotIn('Dinner on Friday', work)
        self.assertNotIn('Weekly tips', work)
        self.assertNotIn('export', next(p for p in self.prompts if 'personal mail' in p))

    def test_fewer_than_two_threads_means_no_turn(self):
        self.mail('w', 'a', 'Ana Ruiz <ana@quarry.example>', 'Export bug', 'The export drops the last row.')
        self.assertEqual((0, []), self.run_once())
        self.assertEqual([], self.prompts)

    def test_a_shared_first_name_or_one_word_is_not_enough(self):
        a = self.mail('w', 'a', 'Emma Clarke <emma@clarke.example>', 'Seafoam order', 'Two skeins of Seafoam please.')
        b = self.mail('w', 'b', 'Emma Dyer <emma.dyer@dyer.example>', 'Restock?', 'Will Seafoam be back in stock?')
        one = {'title': 'Plan a Seafoam restock for both orders', 'why': 'Two people want Seafoam.', 'work': 'Plan.', 'sources': [f'E{a}', f'E{b}'],
               'links': [{'kind': 'item', 'quotes': [{'source': f'E{a}', 'quote': 'skeins of Seafoam'}, {'source': f'E{b}', 'quote': 'Will Seafoam be back'}]}]}
        named = dict(one, links=one['links'] + [{'kind': 'mention', 'quotes': [{'source': f'E{a}', 'quote': 'Two skeins of Seafoam'}]}])
        self.answers = [self.answer(one, named)]
        self.assertEqual((0, []), self.run_once())

    def test_two_independent_signals_make_a_to_do_without_made_up_dates(self):
        a = self.mail('w', 'a', 'Ana Ruiz <ana@quarry.example>', 'Carton price', 'From 1 January our mailer boxes cost 12% more.')
        b = self.mail('w', 'b', 'Ben Cole <ben@birch.example>', 'Quote', 'We can supply mailer boxes at 0.41 each.')
        p = {'title': 'Compare the mailer box quotes before January', 'why': 'Quarry raises prices from 1 January. Sign by November 30.',
             'work': 'Ben quoted 0.41. Order before December 15 to save.', 'sources': [f'E{a}', f'E{b}'],
             'links': [{'kind': 'item', 'quotes': [{'source': f'E{a}', 'quote': 'our mailer boxes cost 12% more'}, {'source': f'E{b}', 'quote': 'mailer boxes at 0.41'}]},
                       {'kind': 'need_offer', 'quotes': [{'source': f'E{a}', 'quote': 'cost 12% more'}, {'source': f'E{b}', 'quote': 'We can supply mailer boxes'}]}]}
        self.answers = [self.answer(p)]
        made, cards = self.run_once()
        self.assertEqual(1, made)
        self.assertIn('1 January', cards[0]['body'])
        self.assertNotIn('November 30', cards[0]['body'])
        self.assertNotIn('December 15', cards[0]['body'])
        self.assertEqual(sorted([a, b]), sorted(json.loads(cards[0]['event_ids'])))
        self.answers = [self.answer(p)]
        with self.store.connect() as db:
            db.execute('DELETE FROM opportunity_runs')
            db.commit()
        self.assertEqual(0, self.run_once()[0])  # the same threads are never joined twice
        self.assertIn('already proposed together with T', self.prompts[-1])  # and the next turn is told so
    def test_a_title_with_a_made_up_date_is_dropped(self):
        a = self.mail('w', 'a', 'Ana Ruiz <ana@quarry.example>', 'Carton price', 'Our mailer boxes cost 12% more next year.')
        b = self.mail('w', 'b', 'Ben Cole <ben@birch.example>', 'Quote', 'We can supply mailer boxes at 0.41 each.')
        p = {'title': 'Switch mailer boxes to Birch by December 1', 'why': 'Cheaper.', 'work': '', 'sources': [f'E{a}', f'E{b}'],
             'links': [{'kind': 'item', 'quotes': [{'source': f'E{a}', 'quote': 'mailer boxes cost'}, {'source': f'E{b}', 'quote': 'mailer boxes at'}]},
                       {'kind': 'need_offer', 'quotes': [{'source': f'E{a}', 'quote': 'cost 12% more'}, {'source': f'E{b}', 'quote': 'We can supply'}]}]}
        self.answers = [self.answer(p)]
        self.assertEqual(0, self.run_once()[0])

    def test_a_thread_number_as_source_counts_as_the_message_quoted(self):
        a = self.mail('w', 'a', 'Ana Ruiz <ana@quarry.example>', 'Carton price', 'From 1 January our mailer boxes cost 12% more.')
        b = self.mail('w', 'b', 'Ben Cole <ben@birch.example>', 'Quote', 'We can supply mailer boxes at 0.41 each.')
        self.run_once()  # to learn how the turn numbers the threads
        number = {e: n for n, e in ((int(t), int(x)) for t, x in re.findall(r'^T(\d+) \|.*\n  E(\d+)', self.prompts[-1], re.M))}
        ta, tb = f'T{number[a]}', f'T{number[b]}'
        p = {'title': 'Compare the mailer box quotes', 'why': 'Two offers.', 'work': 'Ben quoted 0.41.', 'sources': [ta, tb],
             'links': [{'kind': 'item', 'quotes': [{'source': ta, 'quote': 'our mailer boxes cost 12% more'}, {'source': tb, 'quote': 'mailer boxes at 0.41'}]},
                       {'kind': 'need_offer', 'quotes': [{'source': ta, 'quote': 'cost 12% more'}, {'source': tb, 'quote': 'We can supply mailer boxes'}]}]}
        self.answers = [self.answer(p)]
        made, cards = self.run_once()
        self.assertEqual(1, made)
        self.assertEqual(sorted([a, b]), sorted(json.loads(cards[0]['event_ids'])))

    def test_a_quote_the_message_does_not_have_drops_it(self):
        a = self.mail('w', 'a', 'Ana Ruiz <ana@quarry.example>', 'Carton price', 'Our mailer boxes cost 12% more next year.')
        b = self.mail('w', 'b', 'Ben Cole <ben@birch.example>', 'Quote', 'We can supply mailer boxes at 0.41 each.')
        p = {'title': 'Compare the two mailer box offers', 'why': 'Cheaper.', 'work': '', 'sources': [f'E{a}', f'E{b}'],
             'links': [{'kind': 'item', 'quotes': [{'source': f'E{a}', 'quote': 'mailer boxes cost'}, {'source': f'E{b}', 'quote': 'mailer boxes at'}]},
                       {'kind': 'need_offer', 'quotes': [{'source': f'E{a}', 'quote': 'we need a new supplier'}, {'source': f'E{b}', 'quote': 'We can supply'}]}]}
        self.answers = [self.answer(p)]
        self.assertEqual(0, self.run_once()[0])

    def session(self, work, title='Run one onboarding session for both teams'):
        a = self.mail('w', 'a', 'Mara Lind <mara@fernhill.example>', 'Training', 'Could you train our team on the planner in the first week of November?', days=20)
        b = self.mail('w', 'b', 'Liesel Penn <liesel@penrose.example>', 'Onboarding', 'We need onboarding for the new planner tool in the first week of November.', days=19)
        return {'title': title, 'why': 'Both teams asked for planner training.', 'work': work, 'sources': [f'E{a}', f'E{b}'],
                'links': [{'kind': 'item', 'quotes': [{'source': f'E{a}', 'quote': 'on the planner'}, {'source': f'E{b}', 'quote': 'the new planner tool'}]},
                          {'kind': 'need_offer', 'quotes': [{'source': f'E{a}', 'quote': 'Could you train our team'}, {'source': f'E{b}', 'quote': 'We need onboarding'}]}]}

    def test_a_time_already_over_is_history_not_work(self):
        self.answers = [self.answer(self.session('Hi Mara, shall we hold the session in the first week of November?'))]
        self.assertEqual(0, self.run_once()[0])
        self.assertIn('is history: use a newer date', self.prompts[-1])
        self.assertTrue(opportunities.past_timing('a shared session in the first week of November', NOW))
        self.assertTrue(opportunities.past_timing('Send it by 30 October.', NOW))
        self.assertFalse(opportunities.past_timing('the invoice of 3 November shows the old rate', NOW))  # when it happened, not when to act
        self.assertFalse(opportunities.past_timing('book it for Thursday 10 December', NOW))
        self.assertFalse(opportunities.past_timing('before November 20', NOW))
        self.assertFalse(opportunities.past_timing('by the end of November', NOW))

    def test_several_organizations_get_one_message_each(self):
        self.answers = [self.answer(self.session('Draft to all three: Hi all, we run one planner session for your teams.'))]
        self.assertEqual(0, self.run_once(NOW - dt.timedelta(days=12))[0])  # before that week, so only the group mail drops it
        self.assertIn('never one message to people of different companies', self.prompts[-1])
        people = {'mara@fernhill.example': 'Mara Lind', 'liesel@penrose.example': 'Liesel Penn'}
        self.assertTrue(opportunities.group_mail('Hi Mara and Liesel, we run one session.', people))
        self.assertTrue(opportunities.group_mail('Send it with Liesel in cc.', people))
        self.assertFalse(opportunities.group_mail('Write to each separately. Hi Mara, we run a session.', people))
        self.assertFalse(opportunities.group_mail('Hi Mara and Liesel', {'mara@fernhill.example': 'Mara Lind', 'liesel@fernhill.example': 'Liesel Penn'}))

    def test_separate_messages_to_several_organizations_pass(self):
        self.answers = [self.answer(self.session('Write to each separately. To Mara: Hi Mara, we can train your team on the planner. '
                                                 'To Liesel: Hi Liesel, we can run the planner onboarding for you.'))]
        self.assertEqual(1, self.run_once(NOW - dt.timedelta(days=12))[0])

    def build(self, merge=()):
        """The Graph as the worker builds it; merge: pairs of addresses the owner said are one person."""
        with self.store.connect() as db:
            for a, b in merge:
                graph.merge(db, 'email:' + a, 'email:' + b, True, NOW.isoformat(), source='owner')
            db.commit()
            graph.build(db, self.app.config, NOW.isoformat())
            db.commit()

    def boxes(self, second='Ben Cole <ben@birch.example>'):
        a = self.mail('w', 'a', 'Ana Ruiz <ana@quarry.example>', 'Carton price', 'From 1 January our mailer boxes cost 12% more.')
        b = self.mail('w', 'b', second, 'Quote', 'We can supply mailer boxes at 0.41 each.')
        return a, b, {'title': 'Compare the mailer box quotes', 'why': 'Two offers.', 'work': 'Ben quoted 0.41.', 'sources': [f'E{a}', f'E{b}'],
                      'links': [{'kind': 'item', 'quotes': [{'source': f'E{a}', 'quote': 'our mailer boxes cost 12% more'}, {'source': f'E{b}', 'quote': 'mailer boxes at 0.41'}]},
                                {'kind': 'need_offer', 'quotes': [{'source': f'E{a}', 'quote': 'cost 12% more'}, {'source': f'E{b}', 'quote': 'We can supply mailer boxes'}]}]}

    def test_the_graph_ties_threads_and_says_who_is_one_person(self):
        a = self.mail('w', 'a', 'Ana Ruiz <ana@quarry.example>', 'Export bug', 'The export drops the last row since Monday.')
        b = self.mail('w', 'b', 'Ben Cole <ben@quarry.example>', 'Rollout', 'Can we plan the rollout for our second office?')
        self.build()
        p = {'title': 'Fix the export before the second office rollout', 'why': 'One company.', 'work': 'Plan: fix, then roll out.',
             'sources': [f'E{a}', f'E{b}'], 'links': []}
        self.answers = [self.answer(p)]
        self.assertEqual(1, self.run_once()[0])  # one tie the Graph resolved is enough: the same organization
        self.assertIn('Graph ties: T', self.prompts[-1])
        self.assertIn('same organization', self.prompts[-1])

    def test_a_shared_full_name_alone_never_ties_threads(self):
        a = self.mail('w', 'a', 'Ana Ruiz <ana@quarry.example>', 'Export bug', 'The export drops the last row.')
        b = self.mail('w', 'b', 'Ana Ruiz <ana@birch.example>', 'Rollout', 'Can we plan the rollout?')
        self.build()  # at most a "Same person?" suggestion, which never counts
        self.answers = [self.answer({'title': 'Fix the export before the rollout for Ana', 'why': 'Ana twice.', 'work': 'Plan.',
                                     'sources': [f'E{a}', f'E{b}'], 'links': []})]
        self.assertEqual(0, self.run_once()[0])
        self.assertNotIn('Graph ties: T', self.prompts[-1])

    def test_one_person_on_two_addresses_is_one_once_the_graph_joined_them(self):
        *_, p = self.boxes('Ana Ruiz <ana.ruiz@birch.example>')
        self.build([('ana@quarry.example', 'ana.ruiz@birch.example')])
        self.answers = [self.answer(p)]
        self.assertEqual(0, self.run_once()[0])  # the "two offers" are one person's

    def test_two_signals_in_the_messages_still_tie_threads_without_the_graph(self):
        *_, p = self.boxes()
        self.build()
        self.answers = [self.answer(p)]
        self.assertEqual(1, self.run_once()[0])

    def test_the_same_specific_thing_in_several_words_or_a_code_ties_by_itself(self):
        a = self.mail('w', 'a', 'Ana Ruiz <ana@quarry.example>', 'Freight', 'We need a benchmark of Benelux road freight rates per pallet.')
        b = self.mail('w', 'b', 'Ben Cole <ben@birch.example>', 'Dataset', 'I have a dataset of Benelux road freight rates from 2025.')
        p = {'title': 'Offer the freight rate dataset for the benchmark', 'why': 'One needs it, one has it.', 'work': 'Ask Ben to share it.',
             'sources': [f'E{a}', f'E{b}'],
             'links': [{'kind': 'item', 'quotes': [{'source': f'E{a}', 'quote': 'Benelux road freight rates'}, {'source': f'E{b}', 'quote': 'Benelux road freight rates'}]}]}
        self.answers = [self.answer(p)]
        self.assertEqual(1, self.run_once()[0])

    def test_a_title_says_one_message_each_for_several_organizations(self):
        work = ('Write to each separately. To Mara: Hi Mara, we can train your team on the planner. '
                'To Liesel: Hi Liesel, we can run the planner onboarding for you.')
        self.answers = [self.answer(self.session(work, 'Send the planner training offers to Fernhill and Penrose together'))]
        self.assertEqual(0, self.run_once(NOW - dt.timedelta(days=12))[0])
        self.assertIn('never "together"', self.prompts[-1])

    def test_the_best_of_each_area_first_and_two_at_most(self):
        picked = opportunities.pick({'work': [{'title': 'w1'}, {'title': 'w2'}], 'personal': [{'title': 'p1'}]})
        self.assertEqual(['w1', 'p1'], [p['title'] for p in picked])
        self.assertEqual(opportunities.CAP, len(picked))

    def test_dates(self):
        self.assertEqual({('md', 12, 4)}, opportunities.dates_in('Inspection on 4 December.'))
        self.assertEqual({('md', 12, 4)}, opportunities.dates_in('le 4 décembre'))
        self.assertEqual({('md', 11, 15)}, opportunities.dates_in('by November 15th'))
        self.assertIn(('md', 12, 10), opportunities.dates_in('closed Wednesday 9 to Friday 11 December'))  # a range holds each day
        self.assertIn(('md', 12, 10), opportunities.dates_in('vom 9. bis 11. Dezember'))
        self.assertEqual(['24/7', '40x30x10'], opportunities.CODE.findall('im 24/7-Betrieb, the 40x30x10 box, e-mail'))  # an item's code
        self.assertEqual('Ben quoted less.', opportunities.without_made_up_dates('Ben quoted less. Sign by November 15.', set()))


if __name__ == '__main__':
    unittest.main()
