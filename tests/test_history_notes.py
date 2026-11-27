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

    def model(self, items, check=None, merge=None, seen=None):
        """A model: EXTRACT gets items (with "message" filled in from the H-number of the message that has the quote),
        CHECK gets check, MERGE gets merge."""
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
        self.mail(5, 'We always invoice on the first working day, net 15 now.', history=False)  # a live signal: never read
        seen = []
        found = self.learn(self.model([
            {'kind': 'preference', 'text': 'You invoice on the first working day of the month, net 30.',
             'quote': 'we always invoice on the first working day of the month, net 30'},
            {'kind': 'rule', 'text': 'You charge a 5% late fee.', 'quote': 'We always invoice weekly and charge a 5% late fee'}], seen=seen))
        self.assertEqual(found['read'], 1)
        self.assertNotIn('late fee', seen[0])
        self.assertNotIn('net 15', ''.join(seen))
        [fact] = self.facts()
        self.assertEqual((fact['text'], fact['kind'], fact['fact_kind'], fact['source'], fact['side'], fact['scope']),
                         ('You invoice on the first working day of the month, net 30.', 'fact', 'preference', 'history:email', 'work', 'area'))
        self.assertEqual(fact['decision_id'], f"history:{(NOW - dt.timedelta(days=200)).date()}:{event}")
        self.assertEqual(fact['quote'], 'we always invoice on the first working day of the month, net 30')
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM suggestions').fetchone()[0], 0)  # never a to-do

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
