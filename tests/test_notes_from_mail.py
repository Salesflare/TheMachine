"""Home, Health and Kids from the owner's Personal mail (section_notes.mail_senders, mail_prompt, mail_reply;
NotesApp.section_notes_mail_run): one call places each sender in one kind and part for all three at once, Home keeps a
line per sender, Health and Kids a dated line per mail. Made-up data only; the model is a stand-in, nothing is sent."""
import json
import tempfile
import unittest
from pathlib import Path
import machine.main as machine_main

import health_notes  # noqa: E402
import home_notes  # noqa: E402
import kids_notes  # noqa: E402
import note_pages  # noqa: E402
import section_notes  # noqa: E402
import timeutil  # noqa: E402
from pinned import pinned  # noqa: E402

HOME = {'id': 'home', 'email': 'sam@example.com', 'boundary': 'personal'}
JOB = {'id': 'job', 'email': 'sam@acme.example', 'boundary': 'work:Acme'}
AT = '2026-11-14T10:00:00+00:00'
KINDS = (home_notes.KIND, health_notes.KIND, kids_notes.KIND)


class Mail(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [HOME, JOB]}
        self.asked, self.places, self.n = [], {}, 0
        self.app.section_notes_model = self.model
        pin = pinned(AT)
        pin.__enter__()
        self.addCleanup(pin.__exit__, None, None, None)

    def model(self, prompt):
        self.asked.append(prompt)
        if 'who writes to the owner' not in prompt:  # a kind's own call (bills, facts): nothing of those here
            return json.dumps({'places': []})
        out = []
        for line in prompt.split('<<<\n', 1)[1].split('\n>>>', 1)[0].splitlines():
            item = json.loads(line)
            place = next((p for k, p in self.places.items() if k in item['from']), None)
            if place:
                out.append({'n': item['n'], 'kind': place[0], 'section': place[1]})
        return json.dumps({'places': out})

    def mail(self, sender, subject, day, account='home', body='', **meta):
        self.n += 1
        with self.store.connect() as db:
            return db.execute('INSERT INTO events(account_id,source_id,kind,title,body,occurred_at,metadata,content_hash,ingested_at) '
                              "VALUES(?,?,'gmail.message',?,?,?,?,?,?)",
                              (account, f'm{self.n}', subject, body, f'{day}T08:00:00+00:00', json.dumps({'from': sender, **meta}),
                               f'h{self.n}', AT)).lastrowid

    def round(self):
        with self.store.connect() as db:
            db.execute('DELETE FROM section_state')
        self.app.section_notes_mail_run()
        for kind in KINDS:
            self.app.section_notes_run(kind)
        with self.store.connect() as db:
            return {(x['kind'], x['name']): note_pages.page(db, x['id']) for x in note_pages.listing(db, '2026-11-14') if x['kind'] != 'note'}

    def mail_prompts(self):
        return [p for p in self.asked if 'who writes to the owner' in p]


class NotesFromMail(Mail):
    def test_home_gets_a_line_per_sender_that_writes_regularly(self):
        self.places = {'Example Energy': ('home', 'Bills and subscriptions'), 'Example Water': ('home', 'Bills and subscriptions'),
                       'Example Plumber': ('home', 'Repairs and upkeep')}
        self.mail('Example Energy <billing@mail.example-energy.be>', 'Your invoice 2026-0801', '2026-08-03', body='EUR 84,20 IBAN BE00')
        self.mail('Example Energy <billing@mail.example-energy.be>', 'Your invoice 2026-0901', '2026-09-03')
        newest = self.mail('Example Energy <invoices@example-energy.be>', 'Your invoice 2026-1001', '2026-10-03')
        self.mail('Example Water <no-reply@example-water.be>', 'Your water bill', '2026-05-10')
        self.mail('Example Water <no-reply@example-water.be>', 'Meter reading', '2026-08-01')
        self.mail('Example Plumber <office@example-plumber.be>', 'Quote for the boiler', '2026-10-20')  # once: not regular
        self.mail('Sam <sam@example.com>', 'Note to self', '2026-10-21')  # the owner's own address
        self.mail('Example Office Rent <rent@example-office.be>', 'Rent', '2026-10-01', account='job')  # a work mailbox: not read
        self.mail('Example Office Rent <rent@example-office.be>', 'Rent', '2026-11-01', account='job')
        notes = self.round()
        bills = notes[('home', 'Bills and subscriptions')]
        self.assertEqual([x['name'] for x in bills['path']], ['Home'])
        self.assertCountEqual([x['text'] for x in bills['lines']],
                              ['Example Energy: mail every month', 'Example Water: 2 mails in the past year'])
        line = next(x for x in bills['lines'] if x['text'].startswith('Example Energy'))
        self.assertEqual((line['at'], line['event_id']), ('2026-10-03', newest), 'subdomains are one sender, opening the newest mail')
        page = self.app.note_page(bills['id'])
        self.assertEqual({x['source']['from'] for x in page['lines']}, {'Example Energy', 'Example Water'})
        self.assertNotIn(('home', 'Repairs and upkeep'), notes)
        prompt = self.mail_prompts()[0]
        self.assertIn('Your invoice ####-####', prompt)
        for private in ('2026-1001', '84,20', 'IBAN', 'billing@', 'Note to self', 'Office Rent'):
            self.assertNotIn(private, prompt)

    def test_kids_and_health_keep_a_dated_line_per_mail(self):
        self.places = {'Example Primary': ('kids', 'School'), 'Example Lab': ('health', 'Test results'),
                       'Example Shop': ('', '')}
        self.mail('Example Primary <office@example-primary.be>', 'Weekly letter: bring a lunch box on Friday', '2026-10-06', list_unsubscribe=True)
        first = self.mail('Example Primary <office@example-primary.be>', 'Re: School trip to the zoo on 21 November', '2026-11-03')
        self.mail('Example Lab <results@example-lab.be>', 'Your blood test results are ready', '2026-09-12')
        self.mail('Example Lab <results@example-lab.be>', 'Your vitamin D result', '2026-10-30')
        self.mail('Example Shop <deals@example-shop.be>', '20% off everything', '2026-10-01')
        self.mail('Example Shop <deals@example-shop.be>', 'Last chance', '2026-10-02')
        notes = self.round()
        self.assertEqual(sorted(notes), [('health', 'Test results'), ('kids', 'School')])
        school = notes[('kids', 'School')]
        self.assertEqual([x['name'] for x in school['path']], ['Kids'])
        self.assertCountEqual([(x['text'], x['at']) for x in school['lines']],
                              [('Weekly letter: bring a lunch box on Friday', '2026-10-06'), ('School trip to the zoo on 21 November', '2026-11-03')])
        self.assertIn(first, [x['event_id'] for x in school['lines']], 'each line opens its mail')
        self.assertCountEqual([x['text'] for x in notes[('health', 'Test results')]['lines']],
                              ['Your blood test results are ready', 'Your vitamin D result'])
        self.assertEqual({n['area'] for n in notes.values()}, {'personal'})

    def test_a_sender_is_asked_about_once_for_every_kind(self):
        self.places = {'Example Primary': ('kids', 'School')}
        self.mail('Example Primary <office@example-primary.be>', 'Weekly letter', '2026-10-06')
        self.mail('Example Primary <office@example-primary.be>', 'Weekly letter', '2026-10-13')
        self.round()
        self.assertEqual(len(self.mail_prompts()), 1)
        self.round()
        self.assertEqual(len(self.mail_prompts()), 1, 'nothing new: no mail call')
        self.mail('Example Club <info@example-club.be>', 'Swimming lessons start', '2026-11-01')
        self.round()
        self.assertEqual(len(self.mail_prompts()), 2)
        self.assertNotIn('Example Primary', self.mail_prompts()[1])
        with self.store.connect() as db:
            rows = {(r['kind'], r['section']) for r in db.execute("SELECT kind,section FROM section_topics WHERE key LIKE 'mail:%'")}
        self.assertEqual(rows, {('home', ''), ('health', ''), ('kids', ''), ('kids', 'School')})

    def test_a_reply_that_isnt_one_keeps_nothing(self):
        self.app.section_notes_model = lambda prompt: 'not now'
        self.mail('Example Primary <office@example-primary.be>', 'Weekly letter', '2026-10-06')
        self.assertEqual(self.app.section_notes_mail_run(), 0)
        with self.store.connect() as db:
            self.assertIsNone(db.execute("SELECT 1 FROM section_topics WHERE key LIKE 'mail:%'").fetchone())

    def test_free_mail_senders_are_people_by_address(self):
        with self.store.connect() as db:
            self.assertEqual(section_notes._sender_group('ana@gmail.com', {'gmail.com'}), 'ana@gmail.com')
            self.assertEqual(section_notes._sender_group('x@billing.example.co.uk', set()), 'example.co.uk')
            self.assertEqual(section_notes._sender_group('x@mail.example.be', set()), 'example.be')
            self.assertEqual(section_notes.subject('RE: Fwd:  Trip  to the zoo'), 'Trip to the zoo')
            self.assertEqual(section_notes.mail_senders(db, [JOB], timeutil.today()), [], 'no Personal mailbox: no mail read')


class FirstFill(Mail):
    """The first fill goes faster: more mail calls a round and rounds every FIRST_EVERY, outside the quiet hours and
    under the budget, then back to MAIL_CALLS every EVERY."""

    def setUp(self):
        super().setUp()
        from unittest import mock
        import note_pages_app
        self.mock, self.note_pages_app = mock, note_pages_app
        for x in (mock.patch.object(section_notes, 'MAIL_ASK_MAX', 2), mock.patch.object(note_pages_app, 'quiet_hours', lambda: (0, 0))):
            x.start()
            self.addCleanup(x.stop)
        self.holds = []
        self.app.background_pause = lambda **_: self.holds.pop(0) if self.holds else None
        self.app.background_spaced = lambda: True
        self.app.background_started = lambda: None

    def senders(self, n, start=0):
        for i in range(start, start + n):
            self.mail(f'Example Shop {i} <news@shop{i}.example>', 'News', '2026-10-06')

    def step(self):
        self.assertTrue(self.app.section_notes_step())
        self.app.section_notes_thread.join(10)
        return len(self.mail_prompts())

    def filled(self):
        with self.store.connect() as db:
            return bool(db.execute('SELECT 1 FROM section_fill WHERE name=?', (section_notes.FILLED,)).fetchone())

    def test_the_first_fill_makes_more_calls_then_goes_back_to_the_usual_pace(self):
        self.senders(20)
        self.assertEqual(self.step(), section_notes.FIRST_MAIL_CALLS, 'first fill: more calls a round')
        self.assertFalse(self.app.section_notes_step(), 'not due before FIRST_EVERY')
        with self.store.connect() as db:
            db.execute('DELETE FROM section_state')
        self.assertEqual(self.step(), 10, 'the rest of the senders')
        self.assertFalse(self.filled())
        with self.store.connect() as db:
            db.execute('DELETE FROM section_state')
        self.step()  # nothing waits after mail was placed: the first fill ends
        self.assertTrue(self.filled())
        self.senders(20, start=100)
        with self.store.connect() as db:
            db.execute('DELETE FROM section_state')
        self.assertEqual(self.step(), 10 + section_notes.MAIL_CALLS, 'after the first fill: MAIL_CALLS again')

    def test_the_budget_and_the_quiet_hours_hold_the_first_fill(self):
        self.senders(20)
        self.holds = [None, {'window': '5h', 'until': None}]  # the step goes, the second call waits for the budget
        self.assertEqual(self.step(), 1)
        with self.store.connect() as db:
            db.execute('DELETE FROM section_state')
        with self.mock.patch.object(self.note_pages_app, 'quiet_hours', lambda: (0, 24)):
            self.assertEqual(self.step(), 1 + section_notes.MAIL_CALLS, 'quiet hours: the usual pace')


if __name__ == '__main__':
    unittest.main()
