"""Notes from the owner's older email (history_notes.py): once a mailbox's history and live sync are in, one bounded pass
reads only what the owner wrote themselves in history and keeps how they work as facts and rules, in their words, with
the day they wrote it. Code decides over the model: the quote must be the owner's, a note says no more than it, a
removed note never comes back, one client's deal stays theirs only when the owner's words say so, the newer wins, and
nothing is ever a to-do. A Personal note stays out of what goes to the team."""
import datetime as dt
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

from seams import patch_everywhere

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('history_notes_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import history_notes  # noqa: E402
import team_learnings  # noqa: E402
from machine.store import history as history_store  # noqa: E402
from machine.store.facts import history_fact  # noqa: E402

NOW = dt.datetime(2026, 10, 16, 12, tzinfo=dt.timezone.utc)
ME = 'sam@acme.example'
CONFIG = {'accounts': [{'id': 'work', 'service': 'gmail', 'email': ME, 'boundary': 'work:acme'}], 'owner_name': 'Sam Owner'}
WALTER = 'email:walter@client.example'


class HistoryNotes(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.store.config = CONFIG
        self.store.accounts = CONFIG['accounts']
        started = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        started.start()
        self.addCleanup(started.stop)
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person','Walter Client',1,0,'{}')", (WALTER,))
        self.n = 0

    def mail(self, days, body, to='Pat Colleague <pat@acme.example>', mine=True, history=True, title='Re: work'):
        self.n += 1
        meta = {'from': f'Sam Owner <{ME}>' if mine else 'Other <other@else.example>', 'to': to, 'thread_id': f't{self.n}',
                'labels': ['SENT'] if mine else ['INBOX']}
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': f'm{self.n}', 'kind': 'gmail.message',
                                             'occurred_at': (NOW - dt.timedelta(days=days)).isoformat(), 'title': title, 'body': body,
                                             'metadata': meta, 'deleted': False}], history=history)
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (f'm{self.n}',)).fetchone()[0]

    def in_(self, done=True):
        with self.store.connect() as db:
            history_store.save(db, 'work', {}, NOW.isoformat(), 10, NOW.isoformat(), done, 365)
            db.execute("INSERT OR IGNORE INTO milestones(name,at) VALUES('first_import:work',?)", (NOW.isoformat(),))

    def model(self, items, check=None, merge=None, seen=None, twins=None):
        """A model: EXTRACT gets items (with "message" filled in from the H-number of the message that has the quote),
        CHECK gets check, MERGE gets merge, TWINS twins(prompt)."""
        def reply(prompt):
            if seen is not None:
                seen.append(prompt)
            if prompt.startswith('Below are older messages'):
                out = []
                for it in items:
                    found = re.search(r'H(\d+) \|[^\n]*\n<<<[^\n]*' + re.escape(it['quote'][:20]), prompt)
                    if found:
                        out.append({'message': 'H' + found.group(1), 'area': 'work', 'about': '', **it})
                return json.dumps({'items': out})
            if prompt.startswith('Below are facts kept'):
                return json.dumps(check or {})
            if prompt.startswith('Below are pairs'):
                return json.dumps(twins(prompt) if twins else {})
            return json.dumps(merge or {'notes': []})
        return reply

    def learn(self, ask):
        return history_notes.run(self.store, CONFIG['accounts'], ['work'], {ME}, 'October 16, 2026', ask)

    def facts(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT id,text,kind,fact_kind,source,side,scope,quote,decision_id FROM facts WHERE removed_at IS NULL ORDER BY id')]

    def test_due_only_after_history_and_live_sync_and_once(self):
        with self.store.connect() as db:
            self.assertEqual(history_notes.due(db, CONFIG['accounts'], CONFIG), [])
        self.in_(done=False)
        with self.store.connect() as db:
            self.assertEqual(history_notes.due(db, CONFIG['accounts'], CONFIG), [])
        self.in_()
        with self.store.connect() as db:
            self.assertEqual(history_notes.due(db, CONFIG['accounts'], CONFIG), ['work'])
            self.assertEqual(history_notes.due(db, CONFIG['accounts'], {**CONFIG, 'history_notes': False}), [])
            history_notes.mark_read(db, ['work'], {'items': [], 'read': 3})
            self.assertEqual(history_notes.due(db, CONFIG['accounts'], CONFIG), [])

    def test_keeps_the_owners_own_words_with_their_day(self):
        event = self.mail(200, 'Hi Pat, we always invoice on the first working day of the month, net 30. Thanks')
        self.mail(100, 'We always invoice weekly and charge a 5% late fee.', mine=False)  # someone else's words
        seen = []
        found = self.learn(self.model([
            {'kind': 'preference', 'text': 'You invoice on the first working day of the month, net 30.',
             'quote': 'we always invoice on the first working day of the month, net 30'},
            {'kind': 'rule', 'text': 'You charge a 5% late fee.', 'quote': 'We always invoice weekly and charge a 5% late fee'}], seen=seen))
        self.assertEqual(found['read'], 1)
        self.assertNotIn('late fee', seen[0])
        [fact] = self.facts()
        self.assertEqual((fact['text'], fact['kind'], fact['fact_kind'], fact['source'], fact['side'], fact['scope']),
                         ('You invoice on the first working day of the month, net 30.', 'fact', 'preference', 'history:email', 'work', 'area'))
        self.assertEqual(fact['decision_id'], f"history:{(NOW - dt.timedelta(days=200)).date()}:{event}")
        self.assertEqual(fact['quote'], 'we always invoice on the first working day of the month, net 30')
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM suggestions').fetchone()[0], 0)  # never a to-do

    def test_newer_live_mail_and_what_learning_knows_end_a_note_but_never_write_one(self):
        self.mail(200, 'Hi Pat, our deposit is 30 percent on every kitchen renovation. Thanks')
        self.mail(5, 'Our deposit is 40 percent on every kitchen renovation now.', history=False)  # live: only checked against
        self.mail(150, 'Patricia handles every supplier payment for us, always has.')
        self.mail(140, 'Our office closes at 5 on Fridays, all year.')
        with self.store.connect() as db:
            db.execute("INSERT INTO facts(text,decision_id,created_at,kind) VALUES('Morgan handles every supplier payment now.','d1',?,'fact')", (NOW.isoformat(),))
        seen = []
        self.learn(self.model([
            {'kind': 'fact', 'text': 'Your deposit is 30 percent on every kitchen renovation.', 'quote': 'our deposit is 30 percent on every kitchen renovation'},
            {'kind': 'responsibility', 'text': 'Patricia handles every supplier payment.', 'quote': 'Patricia handles every supplier payment for us'},
            {'kind': 'fact', 'text': 'Your office closes at 5 on Fridays.', 'quote': 'Our office closes at 5 on Fridays'}],
            check={'F2': {'verdict': 'drop'}, 'F3': {'verdict': 'update', 'text': 'Your office closes at 4 on Fridays.', 'quote': 'closes at 4', 'message': 'N1'}},
            seen=seen))
        self.assertNotIn('40 percent', seen[0])  # never extracted from
        self.assertIn('40 percent', seen[1])  # but the check sees it
        self.assertIn('known now: <<<Morgan handles every supplier payment now.', seen[1])
        self.assertEqual([f['text'] for f in self.facts() if f['source']], [])  # 30 percent changed later; Pat's job is Morgan's now; 4 is said nowhere

    def test_an_update_carries_the_newer_messages_words_and_day(self):
        self.mail(140, 'Our office closes at 5 on Fridays, all year.')
        newer = self.mail(60, 'From now on our office closes at 4 on Fridays.')
        self.learn(self.model([{'kind': 'fact', 'text': 'Your office closes at 5 on Fridays.', 'quote': 'Our office closes at 5 on Fridays'}],
                              check={'F1': {'verdict': 'update', 'text': 'Your office closes at 4 on Fridays.', 'quote': 'our office closes at 4 on Fridays'}}))
        [fact] = self.facts()
        self.assertEqual((fact['text'], fact['quote']), ('Your office closes at 4 on Fridays.', 'our office closes at 4 on Fridays'))
        self.assertEqual(fact['decision_id'], f"history:{(NOW - dt.timedelta(days=60)).date()}:{newer}")

    def test_a_note_that_says_more_than_its_quote_or_quotes_no_one_goes(self):
        self.mail(100, 'I prefer calls before 10 in the morning, please.')
        self.learn(self.model([
            {'kind': 'preference', 'text': 'You prefer calls before 10, or after 4 on Fridays.', 'quote': 'I prefer calls before 10 in the morning'},
            {'kind': 'preference', 'text': 'You prefer email.', 'quote': 'I prefer email for everything always'}]))
        self.assertEqual(self.facts(), [])

    def test_quoted_mail_below_is_not_the_owners(self):
        self.mail(100, 'Sounds good, see you then.\n\nOn Mon, Pat wrote:\n> We always pay suppliers within 7 days of the invoice.')
        self.learn(self.model([{'kind': 'rule', 'text': 'You pay suppliers within 7 days.', 'quote': 'We always pay suppliers within 7 days'}]))
        self.assertEqual(self.facts(), [])

    def test_one_clients_deal_stays_theirs_only_when_the_owners_words_say_so(self):
        self.mail(120, 'Walter, for you we bill quarterly in advance instead of monthly.', to='Walter Client <walter@client.example>')
        self.mail(110, 'Walter, we send every report as a PDF attachment.', to='Walter Client <walter@client.example>')
        self.mail(100, 'We waive the setup fee for the Clients only, this year.', to='Pat Colleague <pat@acme.example>')
        self.learn(self.model([
            {'kind': 'fact', 'text': 'Walter Client is billed quarterly in advance.', 'quote': 'for you we bill quarterly in advance instead of monthly'},
            {'kind': 'preference', 'text': 'You send every report as a PDF attachment.', 'quote': 'we send every report as a PDF attachment', 'about': 'Walter Client'},
            {'kind': 'fact', 'text': 'The setup fee is waived for the Clients.', 'quote': 'We waive the setup fee for the Clients only'}]))
        facts = {f['text']: f for f in self.facts()}
        self.assertEqual(facts['Walter Client is billed quarterly in advance.']['scope'], 'with:' + WALTER)
        self.assertEqual(facts['You send every report as a PDF attachment.']['scope'], 'area')  # told to one client: how the owner works
        self.assertEqual(facts['The setup fee is waived for the Clients.']['scope'], 'with:' + WALTER)  # "for the Clients only": the one Client
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT node_id,by FROM fact_about").fetchall()[0][:], (WALTER, 'history'))

    def test_said_to_one_person_with_nothing_general_stays_theirs_and_no_one_unknown_gets_it(self):
        self.mail(100, 'Walter, your invoices go out on the 15th.', to='Walter Client <walter@client.example>')
        self.mail(90, 'Zed, your reports come as a spreadsheet.', to='Zed Unknown <zed@nowhere.example>')
        self.mail(80, 'Walter, the shared folder link changes each quarter.', to='Walter Client <walter@client.example>, Pat Colleague <pat@acme.example>')
        found = self.learn(self.model([
            {'kind': 'fact', 'text': 'Invoices go out on the 15th.', 'quote': 'your invoices go out on the 15th'},
            {'kind': 'fact', 'text': 'Reports come as a spreadsheet.', 'quote': 'your reports come as a spreadsheet'},
            {'kind': 'fact', 'text': 'The shared folder link changes each quarter.', 'quote': 'the shared folder link changes each quarter'}]))
        facts = {f['text']: f['scope'] for f in self.facts()}
        self.assertEqual(facts, {'Invoices go out on the 15th.': 'with:' + WALTER, 'The shared folder link changes each quarter.': 'area'})
        self.assertEqual(found['dropped'].get('no_one_to_keep_it_to'), 1)

    def test_a_merge_keeps_one_messages_words_and_never_says_more(self):
        self.mail(200, 'We invoice monthly, always on the first.')
        self.mail(100, 'We charge a 5% late fee after 30 days.')
        self.learn(self.model([
            {'kind': 'fact', 'text': 'You invoice monthly on the first.', 'quote': 'We invoice monthly, always on the first'},
            {'kind': 'fact', 'text': 'You charge a 5% late fee.', 'quote': 'We charge a 5% late fee after 30 days'}],
            merge={'notes': [{'text': 'You invoice monthly on the first and charge a 5% late fee.', 'from': ['F1', 'F2']}]}))
        self.assertEqual(sorted((f['text'], f['quote']) for f in self.facts()),
                         [('You charge a 5% late fee.', 'We charge a 5% late fee after 30 days'),
                          ('You invoice monthly on the first.', 'We invoice monthly, always on the first')])

    def test_over_the_bound_the_richest_messages_are_read_across_all_of_history(self):
        self.mail(600, 'Our minimum fee is 300 for every project, always, unless the board says otherwise.')
        for n in range(history_notes.MAX_MESSAGES + 20):
            self.mail(500 - n, f'Thanks, see you then, talk soon friend number {n}.')
        with self.store.connect() as db:
            rows = history_notes.own_history(db, ['work'], {ME})
        self.assertEqual(len(rows), history_notes.MAX_MESSAGES)
        self.assertIn('minimum fee', rows[-1]['text'])  # the oldest, but the one that says how the owner works

    def test_the_newer_wins_and_a_removed_note_never_comes_back(self):
        self.mail(300, 'Our retainer is $1,000 a month for every client, billed upfront.')
        self.mail(30, 'Heads up: our retainer is $1,500 a month for every client from now on.')
        self.mail(200, 'I never take meetings on Friday afternoons, that is family time.')
        with self.store.connect() as db:
            gone = history_fact(db, 'You never take meetings on Friday afternoons.', False, True, 1, '2026-01-01', 'I never take meetings on Friday afternoons', 'personal')
            db.execute('UPDATE facts SET removed_at=? WHERE id=?', (NOW.isoformat(), gone))
        self.learn(self.model([
            {'kind': 'fact', 'text': 'Your retainer is $1,000 a month for every client.', 'quote': 'Our retainer is $1,000 a month for every client'},
            {'kind': 'preference', 'text': 'You never take meetings on Friday afternoons.', 'quote': 'I never take meetings on Friday afternoons'}]))
        self.assertEqual(self.facts(), [])

    def test_one_rule_said_twice_in_other_words_is_kept_once(self):
        self.mail(300, 'Lettie, our tanks only ever hold beer with the Ironbark name on it.')
        self.mail(100, "Barrett, we don't brew under anyone else's label, ever. Point them to Fallow Field.")
        self.mail(90, 'Our delivery minimum is $400 per order for every account.')
        self.mail(80, 'Accounts order online through the portal, every order.')
        with self.store.connect() as db:
            history_fact(db, 'You see new customers at the brewery, never at their venue.', True, False, 1, '2026-01-01',
                         'We see new customers at the brewery, never at their venue', 'work')
        self.mail(70, 'I always meet a new account at our taproom, not at their place.')
        asked = []

        def twins(prompt):  # one rule twice: the label rule says all of it; the taproom rule is on Learning already
            asked.append(prompt)
            out = {}
            for n, block in enumerate(prompt.split('\nP')[1:], 1):
                a, b = block.split('\n  B: ')
                if 'Ironbark name' in a + b and 'label' in a + b:
                    out[f'P{n}'] = {'same': True, 'keep': 'A' if 'label' in a else 'B'}
                elif 'brewery' in a + b and 'taproom' in a + b:
                    out[f'P{n}'] = {'same': True, 'keep': 'A'}
            return out
        found = self.learn(self.model([
            {'kind': 'rule', 'text': 'Your tanks only ever hold beer with the Ironbark name.', 'quote': 'our tanks only ever hold beer with the Ironbark name on it'},
            {'kind': 'rule', 'text': "You don't brew beer under anyone else's label and point them to Fallow Field.",
             'quote': "we don't brew under anyone else's label, ever. Point them to Fallow Field"},
            {'kind': 'rule', 'text': 'Your delivery minimum is $400 per order.', 'quote': 'Our delivery minimum is $400 per order for every account'},
            {'kind': 'rule', 'text': 'Accounts order online through the portal.', 'quote': 'Accounts order online through the portal, every order'},
            {'kind': 'rule', 'text': 'You meet a new account at your taproom, not at their place.', 'quote': 'I always meet a new account at our taproom, not at their place'}],
            twins=twins))
        self.assertEqual(len(asked), 1)
        self.assertIn('the Ironbark name', asked[0])
        self.assertNotIn('$400', asked[0])  # a note with a number pairs only with one with the same numbers
        texts = [f['text'] for f in self.facts()]
        self.assertEqual(sorted(texts), sorted(['You see new customers at the brewery, never at their venue.', "You don't brew beer under anyone else's label and point them to Fallow Field.",
                                                'Your delivery minimum is $400 per order.', 'Accounts order online through the portal.']))
        self.assertEqual(found['dropped'].get('same_meaning'), 2)  # the one already on Learning stays as the owner sees it

    def test_area_by_meaning_and_personal_stays_out_of_the_team(self):
        self.mail(90, 'Wednesday afternoons are for my daughter, I keep them free every week.')
        found = self.learn(self.model([{'kind': 'preference', 'text': 'You keep Wednesday afternoons free for your daughter.',
                                      'quote': 'Wednesday afternoons are for my daughter, I keep them free', 'area': 'personal'}]))
        [fact] = self.facts()
        self.assertEqual((fact['side'], fact['scope']), ('personal', 'area'))
        self.assertEqual(len(found['items']), 1)
        with self.store.connect() as db:
            self.assertFalse(db.execute('SELECT 1 FROM facts WHERE 1=1 ' + team_learnings._owner_facts(db)).fetchone())

    def test_bounded_turns_and_a_check_that_drops(self):
        for n in range(80):
            self.mail(300 - n, f'Note {n}: we always ship orders from the warehouse within two days, said again in other words {n}. ' + 'x' * 400)
        seen = []
        self.learn(self.model([{'kind': 'rule', 'text': 'You ship orders from the warehouse within two days.',
                              'quote': 'we always ship orders from the warehouse within two days'}],
                            check={'F1': {'verdict': 'drop'}}, seen=seen))
        self.assertLessEqual(len(seen), history_notes.MAX_TURNS)
        self.assertEqual(self.facts(), [])

    def test_step_runs_once_in_the_background_after_the_first_look(self):
        app = object.__new__(a.App)
        app.store, app.config = self.store, CONFIG
        app.background_pause = lambda job=None, **k: None
        app.background_spaced = lambda: True
        app.background_started = lambda: None
        app.owner_emails = lambda: {ME}
        app.history_notes_model = self.model([{'kind': 'preference', 'text': 'You send contracts as PDF only.', 'quote': 'I only send contracts as PDF'}])
        self.mail(50, 'I only send contracts as PDF, never as Word files.')
        self.in_()
        self.assertFalse(app.history_notes_step({}))  # before the first look did its job: never
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at) VALUES('first_card_shown',?)", (NOW.isoformat(),))
        self.assertTrue(app.history_notes_step({}))
        app.history_notes_thread.join(10)
        self.assertEqual([f['text'] for f in self.facts()], ['You send contracts as PDF only.'])
        self.assertFalse(app.history_notes_step({}))  # once per mailbox


if __name__ == '__main__':
    unittest.main()
