"""Where a learned rule holds (learning_loop.contexts, scope_of; Store.in_scope): each signal of a learning pass keeps
the context it came from (area, channel, the people and organizations on its to-do), a rule or fact the pass writes
says where it holds, and every recall (a preparation, a routine's run, get_learnings) leaves it out of work it doesn't
hold for, before any ranking. A scope that can't be placed is never global by default; rules from before stay global.
All local; nothing is sent."""
import json
from pathlib import Path
import tempfile
import unittest

import ai_learnings
import graph
import learning_loop
import machine.main as machine_main
import timeutil
from machine.app.recall import recall

ACCOUNTS = [{'id': 'work', 'service': 'gmail', 'email': 'owner@acme.example', 'boundary': 'work:acme.example'},
            {'id': 'home', 'service': 'gmail', 'email': 'owner@mail.example'}]
PEOPLE = {'pat': ('Pat Lane', 'org-northwind', 'work'), 'dana': ('Dana Ruiz', 'org-globex', 'work'),
          'mom': ('Ann Owner', None, 'home'), 'alex1': ('Alex Kim', 'org-northwind', 'work'), 'alex2': ('Alex Kim', 'org-globex', 'work')}
ORGS = {'org-northwind': 'Northwind', 'org-globex': 'Globex'}
PRICE = 'For Northwind, quote the partner rate of EUR 90 per seat.'


class LearningScope(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = ACCOUNTS
        self.store.config = {'accounts': ACCOUNTS}
        self.app = object.__new__(machine_main.App)
        self.app.store, self.app.config, self.app.fleet = self.store, self.store.config, None
        self.stamp = timeutil.now()
        self.event = 0
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at) VALUES('first_card_shown',?)", (self.stamp,))
            graph.ensure(db)
            for node, name in ORGS.items():
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'organization',?,1,1,'{}')", (node, name))
            for who, (name, org, _) in PEOPLE.items():
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person',?,1,1,?)",
                           ('p-' + who, name, json.dumps({'org': org} if org else {})))

    def todo(self, who, title, kind='email'):
        """A to-do on one message from who, in their area."""
        self.event += 1
        sid = f'{who}-{self.event}'
        account = 'work' if PEOPLE[who][2] == 'work' else 'home'
        with self.store.connect() as db:
            event_id = db.execute("INSERT INTO events(account_id,source_id,kind,title,body,occurred_at,metadata,content_hash,ingested_at) "
                                  "VALUES(?,?,?,?,'',?,'{}',?,?)", (account, sid, 'slack.message' if kind == 'slack' else 'gmail.message', title,
                                                                    self.stamp, sid, self.stamp)).lastrowid
            db.execute('INSERT INTO graph_events(node_id,event_id,at) VALUES(?,?,?)', ('p-' + who, event_id, self.stamp))
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,'',?,?,'pending',?)",
                       (sid, sid, title, json.dumps([event_id]), json.dumps([account]), self.stamp))
        return sid

    def edit(self, todo, before, after, kind='email'):
        with self.store.connect() as db:
            db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_body,after_body,source,created_at) "
                       "VALUES(?,?,'a','b',?,?,?,'dashboard',?)", (f'e{todo}{len(before)}', todo, kind, before, after, self.stamp))

    def note(self, todo, text):
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,'other',?,'dashboard',?)",
                       (f'd{todo}', todo, text, self.stamp))

    def learn(self, changes):
        """One pass: its evidence as the turn reads it, then changes saved and applied as the turn's answer would be.
        changes(n, ref): the turn's changes, with n(to-do title) the numbers of its signals and ref(name) a record's ref."""
        run_id = self.store.tune_due()
        self.assertTrue(run_id)
        with self.store.connect() as db:
            evidence = json.loads(db.execute('SELECT evidence FROM profile_runs WHERE run_id=?', (run_id,)).fetchone()[0])
            n = lambda *titles: [s['n'] for s in evidence['signals'] if s.get('to_do') in titles]
            ref = lambda name: next((w['ref'] for s in evidence['signals'] for w in (s.get('context') or {}).get('with') or () if w['name'] == name), 'r0')
            learning_loop.save_draft(db, run_id, {'changes': changes(n, ref)})
            db.execute("UPDATE profile_runs SET status='ok' WHERE run_id=?", (run_id,))
        self.store.apply_tune(run_id)
        return evidence

    def learned(self):
        with self.store.connect() as db:
            return {r['text']: dict(r) for r in db.execute("SELECT id,text,scope,side FROM facts WHERE removed_at IS NULL AND decision_id LIKE 'tune:%'")}

    def rules_for(self, todo):
        return recall(self.app, 'preparation', {'todo': todo}).text('rules')

    def routine_rules(self, text, channels=()):
        return recall(self.app, 'routine', {'run': 1, 'title': 'Weekly', 'text': text, 'channels': list(channels)}).text('rules')

    def price_pass(self, changes):
        pat = self.todo('pat', 'Seat pricing')
        self.edit(pat, 'Our price is EUR 120 per seat.', 'Our partner price is EUR 90 per seat.')
        self.note(self.todo('pat', 'Renewal'), 'Northwind always gets the partner rate')
        self.note(self.todo('mom', 'Sunday lunch'), 'not now')
        return self.learn(changes)

    def test_two_corrections_in_different_contexts_stay_apart_on_the_evidence(self):
        pat, dana, mom = self.todo('pat', 'Quote'), self.todo('dana', 'Quote'), self.todo('mom', 'Quote')
        for todo in (pat, dana, mom):
            self.edit(todo, 'Dear friend, kind regards', 'Hi, cheers')
        self.store.config[learning_loop.FLAG] = False  # before: the same three signals, nothing to tell them apart by
        with self.store.connect() as db:
            before = learning_loop.evidence(db, self.store.voices(db), accounts=ACCOUNTS, scoped=False)
            after = learning_loop.evidence(db, self.store.voices(db), accounts=ACCOUNTS, scoped=True)
        strip = lambda s: {k: v for k, v in s.items() if k not in ('n', 'context')}
        self.assertEqual(len({json.dumps(strip(s), sort_keys=True) for s in before['signals']}), 1)
        contexts = [s['context'] for s in after['signals']]
        self.assertEqual(sorted(c['area'] for c in contexts), ['personal', 'work', 'work'])
        self.assertEqual({c['channel'] for c in contexts}, {'Email'})
        names = sorted((w['name'], w.get('at')) for c in contexts for w in c['with'] if w['kind'] == 'person')
        self.assertEqual(names, [('Ann Owner', None), ('Dana Ruiz', 'Globex'), ('Pat Lane', 'Northwind')])
        self.assertTrue(set(after['refs'].values()) >= {'p-pat', 'p-dana', 'p-mom', 'org-northwind', 'org-globex'})
        page = json.dumps(learning_loop.page(after))
        self.assertNotIn('p-pat', page)  # refs, never the Graph's ids, on the page
        self.assertIn('scope', learning_loop.prompt('r', after))
        self.assertNotIn('"with:<ref>"', learning_loop.prompt('r', before))

    def test_a_partner_rule_goes_with_its_partner_only(self):
        evidence = self.price_pass(lambda n, ref: [{'kind': 'draft', 'text': PRICE, 'why': 'Two corrections.', 'scope': 'with:' + ref('Pat Lane'),
                                                    'from': n('Seat pricing', 'Renewal')}])
        self.assertIn('p-pat', evidence['refs'].values())
        self.assertEqual(self.learned()[PRICE]['scope'], 'with:p-pat')
        self.assertIn('partner rate', self.rules_for(self.todo('pat', 'Another quote')))
        self.assertNotIn('partner rate', self.rules_for(self.todo('dana', 'A quote')))
        self.assertNotIn('partner rate', self.routine_rules('weekly pipeline and pricing review'))
        self.assertIn('partner rate', self.routine_rules('pricing for Pat Lane this week'))  # a routine that names them

    def test_a_routine_names_a_record_by_its_whole_name_not_by_letters_inside_a_word(self):
        # as apply_tune stores a scoped rule: its scope, and the record it is about in fact_about
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('org-era','organization','Era',1,1,'{}')")
            fact = db.execute("INSERT INTO facts(text,decision_id,created_at,kind,scope) VALUES('Invoice them in USD.','tune:r',?,'draft','with:org-era')",
                              (self.stamp,)).lastrowid
            db.execute("INSERT INTO fact_about(fact_id,node_id,by,created_at) VALUES(?,'org-era','tune',?)", (fact, self.stamp))
        self.assertNotIn('USD', self.routine_rules('general weekly review'))  # "Era" inside "general" names no one
        self.assertNotIn('USD', self.routine_rules('operations sync'))
        self.assertIn('USD', self.routine_rules('invoices for Era this week'))
        self.assertIn('USD', self.routine_rules("check era's invoices"))  # any case, with a possessive, as before

    def test_a_missing_or_wrong_scope_narrows_to_what_its_signals_share_never_global(self):
        self.price_pass(lambda n, ref: [{'kind': 'draft', 'text': PRICE, 'why': 'x', 'from': n('Seat pricing', 'Renewal')},
                                        {'kind': 'draft', 'text': 'Answer within the day.', 'why': 'x', 'scope': 'with:r9',
                                         'from': n('Seat pricing', 'Sunday lunch')},
                                        {'kind': 'draft', 'text': 'Keep it short.', 'why': 'x', 'scope': 'everywhere-ish'}])
        learned = self.learned()
        self.assertEqual(learned[PRICE]['scope'], 'with:p-pat')  # both from Pat: Pat's
        self.assertNotIn('Answer within the day.', learned)  # Pat and family share nothing: not kept
        self.assertNotIn('Keep it short.', learned)

    def test_a_scope_wider_than_its_signals_narrows_to_them(self):
        """global, an area or a channel the pass gives is kept only as far as the signals it names bear it out."""
        self.price_pass(lambda n, ref: [{'kind': 'draft', 'text': PRICE, 'why': 'x', 'scope': 'global', 'from': n('Seat pricing', 'Renewal')},
                                        {'kind': 'draft', 'text': 'Quote per seat.', 'why': 'x', 'scope': 'area:work', 'from': n('Seat pricing', 'Renewal')},
                                        {'kind': 'fact', 'text': 'Lunch can wait.', 'why': 'x', 'scope': 'area:work', 'from': n('Sunday lunch')}])
        learned = self.learned()
        self.assertEqual(learned[PRICE]['scope'], 'with:p-pat')  # two signals, both Pat's: Pat's, not everywhere
        self.assertEqual(learned['Quote per seat.']['scope'], 'with:p-pat')  # nor all of work
        self.assertEqual(learned['Lunch can wait.']['scope'], 'with:p-mom')  # a work scope from a family signal: theirs
        self.assertNotIn('partner rate', self.rules_for(self.todo('dana', 'A quote')))

    def test_global_when_the_signals_span_people_and_areas_or_one_note_says_so(self):
        pat, mom = self.todo('pat', 'Quote'), self.todo('mom', 'Dinner')
        self.edit(pat, 'Great!', 'Great.')
        self.edit(mom, 'Lovely!', 'Lovely.')
        self.note(self.todo('dana', 'Call time'), 'never before 10, for anything')
        self.learn(lambda n, ref: [{'kind': 'draft', 'text': 'Never use exclamation marks.', 'why': 'x', 'scope': 'global', 'from': n('Quote', 'Dinner')},
                                   {'kind': 'fact', 'text': 'You take no calls before 10.', 'why': 'x', 'scope': 'global', 'from': n('Call time')}])
        learned = self.learned()
        self.assertEqual(learned['Never use exclamation marks.']['scope'], 'global')
        self.assertEqual(learned['You take no calls before 10.']['scope'], 'global')  # the owner's own words say where

    def test_an_area_rule_stays_in_its_area_and_out_of_routines(self):
        self.price_pass(lambda n, ref: [{'kind': 'draft', 'text': 'Sign off with Love.', 'why': 'x', 'scope': 'area:personal', 'from': n('Sunday lunch')},
                                        {'kind': 'draft', 'text': 'Never use exclamation marks.', 'why': 'x', 'scope': 'global'}])
        learned = self.learned()
        self.assertEqual((learned['Sign off with Love.']['scope'], learned['Sign off with Love.']['side']), ('area', 'personal'))
        self.assertIn('Sign off with Love', self.rules_for(self.todo('mom', 'Dinner')))
        self.assertNotIn('Sign off with Love', self.rules_for(self.todo('dana', 'Quote')))
        self.assertNotIn('Sign off with Love', self.routine_rules('sign off the weekly family note'))
        for todo in (self.todo('mom', 'Dinner'), self.todo('dana', 'Quote')):
            self.assertIn('exclamation', self.rules_for(todo))  # global: everywhere, as before
        self.assertIn('exclamation', self.routine_rules('weekly note'))

    def test_a_channel_rule_only_where_the_work_goes_out_on_it(self):
        pat = self.todo('pat', 'Ping', 'slack')
        self.edit(pat, 'Dear Pat, hello', 'hey pat', 'slack')
        self.edit(self.todo('dana', 'Ping', 'slack'), 'Dear Dana, hello', 'hey dana', 'slack')
        self.note(self.todo('mom', 'Lunch'), 'not now')
        self.learn(lambda n, ref: [{'kind': 'draft', 'text': 'On Slack, write in lowercase.', 'why': 'x', 'scope': 'channel:Slack', 'from': n('Ping')}])
        self.assertEqual(self.learned()['On Slack, write in lowercase.']['scope'], 'channel:Slack')
        self.assertIn('lowercase', self.rules_for(self.todo('dana', 'Again', 'slack')))
        self.assertNotIn('lowercase', self.rules_for(self.todo('dana', 'Mail')))
        self.assertNotIn('lowercase', self.routine_rules('weekly digest'))
        self.assertIn('lowercase', self.routine_rules('weekly digest', ['Slack']))

    def test_two_people_with_one_name_stay_apart(self):
        first = self.todo('alex1', 'Quote')
        self.edit(first, 'EUR 120', 'EUR 90')
        self.note(self.todo('alex1', 'Again'), 'Alex at Northwind gets the partner rate')
        self.note(self.todo('alex2', 'Hello'), 'not now')
        evidence = self.learn(lambda n, ref: [{'kind': 'draft', 'text': PRICE, 'why': 'x', 'from': n('Quote', 'Again')}])
        self.assertEqual(sorted(w.get('at') for s in evidence['signals'] for w in s['context']['with'] if w['kind'] == 'person'),
                         ['Globex', 'Northwind', 'Northwind'])
        self.assertEqual(len({w['ref'] for s in evidence['signals'] for w in s['context']['with'] if w['kind'] == 'person'}), 2)
        self.assertIn('partner rate', self.rules_for(self.todo('alex1', 'Third')))
        self.assertNotIn('partner rate', self.rules_for(self.todo('alex2', 'Quote')))
        self.assertNotIn('partner rate', self.rules_for(self.todo('alex2', 'Quote for Alex Kim')))  # their name on it: still someone else

    def test_rules_from_before_and_with_the_flag_off_stay_global(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO facts(text,decision_id,created_at,kind) VALUES('Old rule: no emoji.','note-1',?,'draft')", (self.stamp,))
        self.store.config[learning_loop.FLAG] = False
        evidence = self.price_pass(lambda n, ref: [{'kind': 'draft', 'text': PRICE, 'why': 'x'}])
        self.assertNotIn('scoped', evidence)
        self.assertNotIn('context', json.dumps(evidence['signals']))
        self.assertIsNone(self.learned()[PRICE]['scope'])
        dana = self.todo('dana', 'Quote')
        self.assertIn('partner rate', self.rules_for(dana))  # as today: everywhere
        self.assertIn('no emoji', self.rules_for(dana))
        self.assertIn('no emoji', self.routine_rules('weekly'))

    def test_get_learnings_never_gives_a_persons_rule_and_says_a_channel(self):
        with self.store.connect() as db:
            for text, scope, side in (('Pat: partner rate.', 'with:p-pat', None), ('Slack: lowercase.', 'channel:Slack', None),
                                      ('Family: Love.', 'area', 'personal'), ('Old: no emoji.', None, None)):
                db.execute("INSERT INTO facts(text,decision_id,created_at,kind,scope,side) VALUES(?,'tune:r',?,'draft',?,?)", (text, self.stamp, scope, side))
            work = ai_learnings.learnings(db, ACCOUNTS, 'work', lambda t, o: t)
            both = ai_learnings.learnings(db, ACCOUNTS, None, lambda t, o: t)
        self.assertEqual(sorted(r['text'] for r in work['rules']), ['Old: no emoji.', 'Slack: lowercase.'])
        self.assertEqual(next(r for r in work['rules'] if r['text'].startswith('Slack'))['channel'], 'Slack')
        self.assertEqual(next(r for r in both['rules'] if r['text'].startswith('Family'))['area'], 'personal')
        self.assertNotIn('Pat', json.dumps(both))

    def partner_rule(self):
        self.price_pass(lambda n, ref: [{'kind': 'draft', 'text': PRICE, 'why': 'Two corrections.', 'scope': 'with:' + ref('Pat Lane'),
                                         'from': n('Seat pricing', 'Renewal')}])
        change = next(c for c in self.store.snapshot([])['learning_changes'] if c['kind'] == 'draft')
        self.assertEqual((change['text'], change['why']), (PRICE, 'Two corrections.'))  # under Recent changes, with why
        return change

    def test_a_scoped_rule_in_the_owners_words_keeps_where_it_holds(self):
        self.partner_rule()
        self.store.edit_fact(self.learned()[PRICE]['id'], 'For Northwind, quote EUR 90 per seat.')
        self.assertEqual(self.learned()['For Northwind, quote EUR 90 per seat.']['scope'], 'with:p-pat')
        self.assertNotIn('EUR 90', self.rules_for(self.todo('dana', 'A quote')))
        self.assertIn('EUR 90', self.rules_for(self.todo('pat', 'A quote')))

    def test_a_scoped_rule_is_undone_like_any_other(self):
        change = self.partner_rule()
        self.app.action('learning_undo', {'id': change['id']}, owner_dashboard=True)
        self.assertEqual(self.learned(), {})
        self.assertNotIn('partner rate', self.rules_for(self.todo('pat', 'A quote')))

if __name__ == '__main__':
    unittest.main()
