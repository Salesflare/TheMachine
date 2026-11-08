"""A to-do's own sources across areas: a run the owner started (Do it, Try again, a move) reads the messages the to-do
came from wherever they live, and nothing else outside its area; mail in one company's mailbox for another company of
the owner's goes there from the start (suggest company); a run stuck on other messages from another area offers the one
tap that unblocks it ("Use this email for this to-do") instead of a dead Stuck. Offline: nothing is sent."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('todo_own_sources_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import todo_areas  # noqa: E402

# The owner runs Acme (Work) and a second company, Side, whose accounts they labeled Personal.
ACCOUNTS = [
    {'id': 'home-chat', 'service': 'whatsapp', 'boundary': 'personal:whatsapp'},
    {'id': 'acme-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@acme.example', 'boundary': 'work:Acme'},
    {'id': 'side-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@side.example', 'boundary': 'work:Side', 'scope': 'personal'},
    {'id': 'side-cal', 'service': 'calendar', 'transport': 'gog', 'email': 'robin@side.example', 'boundary': 'work:Side', 'scope': 'personal'},
    {'id': 'me-li', 'service': 'linkedin', 'boundary': 'work:linkedin'},
    {'id': 'gateway', 'service': 'gateway', 'boundary': 'owner:system'},
]


def mail(account, source_id, subject, thread):
    return {'account_id': account, 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': '2026-11-02T09:00:00+00:00',
            'title': subject, 'body': 'A new invoice is ready.', 'metadata': {'from': 'Billing <billing@vendor.example>', 'thread_id': thread},
            'deleted': False}


class Companies(unittest.TestCase):
    def test_every_company_of_the_owners_also_one_labeled_personal(self):
        self.assertEqual(todo_areas.owner_companies(ACCOUNTS), [
            {'id': 'work:Acme', 'name': 'Acme', 'domains': ['acme.example'], 'personal': False},
            {'id': 'work:Side', 'name': 'Side', 'domains': ['side.example'], 'personal': True}])  # a profile is no company
        self.assertEqual(todo_areas.company_accounts('work:Side', ACCOUNTS), ['side-mail', 'side-cal'])
        for wrong in ('work:linkedin', 'work:Other', 'personal', ''):
            with self.assertRaisesRegex(ValueError, 'company'):
                todo_areas.company_accounts(wrong, ACCOUNTS)

    def test_the_review_is_told_the_companies_only_when_there_are_several(self):
        line = a.companies_prompt({'accounts': ACCOUNTS})
        self.assertIn('work:Side (side.example, its to-dos are Personal)', line)
        self.assertIn('work:Acme (acme.example)', line)
        self.assertIn('add company=<its id> to suggest', line)
        self.assertIn('never by a name in the text alone', line)
        self.assertEqual(a.companies_prompt({'accounts': ACCOUNTS[:2]}), '')
        self.assertIn('company:<its id>', (ROOT / 'AGENTS.md').read_text())


class Sources(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = ACCOUNTS
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': ACCOUNTS, 'prepare_ahead': False, 'database': str(Path(self.temp.name) / 'e.sqlite')}
        self.store.config = self.app.config
        # 1: the vendor's invoice for Side, forwarded to the Acme mailbox; 2: Side's own copy; 3: an older Side email
        self.store.commit_page('acme-mail', {}, [mail('acme-mail', 'a1', 'New invoice for Side', 't1')])
        self.store.commit_page('side-mail', {}, [mail('side-mail', 's1', 'Your order is confirmed', 't2'), mail('side-mail', 's0', 'Last month', 't0')])

    def suggest(self, **extra):
        return self.app.action('suggest', {'dedupe_key': 'vendor:side:invoice', 'title': 'Pay the vendor for Side',
                                           'body': 'The vendor needs **$210.88** for Side.', 'event_ids': [1, 2], **extra})['id']

    def row(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())

    def card(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            self.store.card_views(db, [row])
        return row

    def start(self, sid):
        self.store.decide(sid, 'accept', '', 'click-' + sid, 'dashboard')
        sent = []
        self.app.preparation_step(lambda req: sent.append(req) or {'status': 'admitted'})
        with self.store.connect() as db:
            job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (sid,)).fetchone()['job_id']
        return job, sent[-1]['message'] if sent else ''

    def lines(self, sid):
        with self.store.connect() as db:
            owner, _ = self.app.card_chat_service(db, sid)
        return [i['text'] for i in owner if i.get('kind') == 'event']

    def test_without_a_company_mail_in_two_mailboxes_lands_in_the_mailboxs_company(self):
        sid = self.suggest()  # how it went before: Side's mailbox is in no area, so the Acme copy made it Work at Acme
        self.assertEqual(todo_areas.current(self.row(sid)['account_ids'], ACCOUNTS), 'work:Acme')

    def test_mail_for_another_company_of_the_owners_lands_there_from_the_start(self):
        sid = self.suggest(company='work:Side')
        row = self.row(sid)
        self.assertEqual((json.loads(row['account_ids']), row['area']), (['side-mail', 'side-cal'], 'work:Side'))
        self.assertEqual((self.card(sid)['scope'], self.card(sid)['area']), ('personal', 'personal'))  # Side's to-dos are Personal
        # A later message on the Acme mailbox about the same matter doesn't pull it back
        self.store.commit_page('acme-mail', {}, [mail('acme-mail', 'a2', 'Reminder: invoice for Side', 't1')])
        self.app.action('suggest', {'dedupe_key': 'vendor:side:reminder', 'title': 'Pay the vendor for Side',
                                    'body': 'A reminder came in.', 'event_ids': [4], 'card_id': sid})
        self.assertEqual(json.loads(self.row(sid)['account_ids']), ['side-mail', 'side-cal'])
        with self.assertRaisesRegex(ValueError, 'company'):
            self.suggest(company='work:Nope', dedupe_key='other')

    def test_do_it_reads_its_own_sources_wherever_they_live_and_nothing_else(self):
        sid = self.suggest()
        _, message = self.start(sid)
        self.assertIn('Its own sources: the owner started this run on this to-do', message)
        self.assertIn('event_ids [1, 2], on acme-mail, side-mail', message)
        self.assertIn('wherever they live (side-mail too)', message)
        self.assertIn('Never record a blocker for reading them', message)
        self.assertIn('still follows its area', message)  # searching for more stays inside it
        self.assertIn('apart from its own sources below', message)
        self.assertIn('use_event_ids', message)
        self.assertNotIn('3]', message.split('Its own sources')[1].split('.')[0])  # only its own messages, not the older one

    def test_after_a_move_to_personal_try_again_still_reads_its_sources(self):
        sid = self.suggest()
        job, _ = self.start(sid)
        self.store.preparation_blocked(sid, job, 'Something else stopped it.')
        self.app.action('card_move', {'suggestion_id': sid, 'area': 'personal', 'decision_id': 'move-1'}, owner_dashboard=True)
        self.assertEqual(json.loads(self.row(sid)['account_ids']), ['home-chat', 'side-mail', 'side-cal'])  # Side's are Personal
        self.store.decide(sid, 'retry', '', 'retry-1', 'dashboard')
        sent = []
        # the old run, which saved its blocker, has ended; then the new run starts
        self.app.preparation_step(lambda req: sent.append(req) or {'status': 'ok' if req.get('action') in ('status', 'stop') else 'admitted'})
        message = next(r['message'] for r in reversed(sent) if r.get('message'))
        self.assertIn('this to-do is in Personal', message)
        self.assertIn('wherever they live (acme-mail too)', message)  # side-mail is in Personal itself

    def test_a_run_prepared_ahead_gets_no_more_than_before(self):
        accounts = '["home-chat"]'
        self.assertNotIn('Its own sources', a.area_prompt(self.app.config, accounts, [(1, 'acme-mail')], owner_started=False))
        self.assertIn('Its own sources', a.area_prompt(self.app.config, accounts, [(1, 'acme-mail')], owner_started=True))
        # All its sources in its area: nothing to add
        self.assertNotIn('Its own sources', a.area_prompt(self.app.config, '["acme-mail"]', [(1, 'acme-mail')], owner_started=True))

    def test_a_mailbox_labeled_personal_is_in_personal_so_a_personal_to_do_never_asks_for_it(self):
        # A Personal to-do from a company mailbox the owner labeled personal: that mailbox is its area's, not another one
        line = a.area_prompt(self.app.config, '["side-mail"]', [(1, 'side-mail')], owner_started=True)
        self.assertIn('this to-do is in Personal (its accounts: whatsapp, gmail, calendar)', line)
        self.assertNotIn('Its own sources', line)  # nothing outside its area to ask for
        self.assertEqual(todo_areas.sources_area(['side-mail', 'home-chat'], ACCOUNTS), 'personal')
        # Work and Personal still cross: a Personal to-do's Acme mail, and a Work to-do's Side mail, are outside
        self.assertIn('wherever they live (acme-mail too)', a.area_prompt(self.app.config, '["side-mail"]', [(1, 'acme-mail')], owner_started=True))
        self.assertIn('wherever they live (side-mail too)', a.area_prompt(self.app.config, '["acme-mail"]', [(1, 'side-mail')], owner_started=True))

    def test_a_personal_handoff_sends_from_a_personal_mailbox_before_a_company_one_labeled_so(self):
        import next_actions
        home = {'id': 'home-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@mail.example', 'boundary': 'personal:me'}
        self.assertEqual(next_actions.sending_account({'accounts': ACCOUNTS + [home]}, ['home-chat'])['id'], 'home-mail')
        self.assertEqual(next_actions.sending_account({'accounts': ACCOUNTS}, ['home-chat'])['id'], 'side-mail')  # the only Personal one
        self.assertEqual(next_actions.sending_account({'accounts': ACCOUNTS + [home]}, ['side-mail'])['id'], 'side-mail')  # its own first

    def test_a_run_stuck_on_other_mail_offers_to_use_it_and_carries_on(self):
        sid = self.suggest()
        job, _ = self.start(sid)
        with self.assertRaisesRegex(ValueError, 'own sources'):
            self.store.preparation_blocked(sid, job, 'It needs the earlier invoice.', use_event_ids=[2])
        with self.assertRaisesRegex(ValueError, 'collected, live'):
            self.store.preparation_blocked(sid, job, 'It needs the earlier invoice.', use_event_ids=[99])
        with self.assertRaisesRegex(ValueError, 'not both'):
            self.store.preparation_blocked(sid, job, 'It needs the earlier invoice.', use_event_ids=[3], move_to='personal')
        for wrong in ([], [3, 3], ['3'], [True], list(range(1, 8))):
            with self.assertRaisesRegex(ValueError, 'use_event_ids'):
                self.store.preparation_blocked(sid, job, 'It needs the earlier invoice.', use_event_ids=wrong)
        self.store.preparation_blocked(sid, job, "Last month's invoice is in Side's mailbox.", use_event_ids=[3])
        card = self.card(sid)
        self.assertEqual((card['preparation_status'], card['preparation_use']), ('blocked', {'n': 1, 'mail': True}))
        self.assertEqual(json.loads(self.row(sid)['event_ids']), [1, 2])  # asking added nothing
        with self.assertRaisesRegex(ValueError, 'owner'):
            self.app.action('card_use_sources', {'suggestion_id': sid, 'decision_id': 'use-1'}, owner_dashboard=False)
        used = self.app.action('card_use_sources', {'suggestion_id': sid, 'decision_id': 'use-1'}, owner_dashboard=True)
        self.assertEqual((used['line'], used['resumed']), ('Added the email to this to-do', True))
        self.assertEqual(json.loads(self.row(sid)['event_ids']), [1, 2, 3])
        self.assertEqual(json.loads(self.row(sid)['account_ids']), ['acme-mail', 'side-mail'])  # its accounts stay
        card = self.card(sid)
        self.assertEqual((card['preparation_status'], card['preparation_use']), ('queued', None))
        self.assertEqual(self.lines(sid), ['Do it', 'Added the email to this to-do'])  # no "You", no Try again of theirs
        self.assertTrue(self.app.action('card_use_sources', {'suggestion_id': sid, 'decision_id': 'use-1'}, owner_dashboard=True)['duplicate'])
        with self.assertRaisesRegex(ValueError, 'Nothing is waiting'):
            self.app.action('card_use_sources', {'suggestion_id': sid, 'decision_id': 'use-2'}, owner_dashboard=True)


class Payment(unittest.TestCase):
    def test_a_bank_transfer_is_prepared_and_the_banks_approval_stays_the_owners(self):
        job = {'job_id': 'j' * 32, 'suggestion_id': 's' * 16}
        for prompt in (a.preparation_prompt(job), a.preparation_prompt({**job, 'ahead': True})):
            self.assertIn('A bank transfer for an invoice is a last step like Pay', prompt)
            self.assertIn('the IBAN, the payee and the payment reference from the invoice itself', prompt)
            self.assertIn("The bank's own approval (its app, card reader or code) is always the owner's", prompt)
        # The existing gates stay as they are: Do it approves what the card offers, the last step waits for Confirm
        rules = (ROOT / 'PREPARATION.md').read_text()
        self.assertIn("Do it is the owner's approval for everything the card offers, including payments", rules)
        self.assertIn('The owner reviews the preview and taps Confirm', rules)


if __name__ == '__main__':
    unittest.main()
