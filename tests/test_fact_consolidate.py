"""Consolidation (machine/store/facts.py): a fact or rule saved again in other words takes the old one's place instead of
piling up next to it (the old one stays behind it, Undo merge, and the chat's Undo brings it back); facts that differ in a
name, day or number stay apart; the owner's own words are never replaced; and the condense pass is told which ones are
close in meaning, from the vectors preparations stored."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from seams import patch_everywhere  # noqa: E402
from machine.store import facts

spec = importlib.util.spec_from_file_location('assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
assistant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assistant)

NOW = '2026-10-31T10:00:00+00:00'
RULE = 'For listing exchange emails, use the listing skill and lead with the partner’s concrete benefit before the ask.'
REWORDED = 'For listing exchange emails and their follow-ups, lead with the partner’s concrete benefit before the ask, and use the listing skill.'
SAME = 'For listing exchange emails, lead with the partner’s concrete benefit before the ask, and use the listing skill.'


def event():
    return {'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': '2026-10-09T10:00:00+00:00',
            'title': 'A real subject', 'body': 'Original', 'metadata': {}, 'deleted': False}


class FactConsolidate(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = assistant.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [event()])
        self.sid = self.store.suggest('facts', 'Check the vendor', 'Body', [1])['id']
        self.store.decide(self.sid, 'reject', 'we stopped using them', 'owner-note', 'dashboard')
        self.at = patch_everywhere(assistant, 'now', return_value=NOW)
        self.at.start()
        self.addCleanup(self.at.stop)

    def current(self):
        with self.store.connect() as db:
            return {r['id']: r['text'] for r in db.execute('SELECT id,text FROM facts WHERE removed_at IS NULL')}

    def test_a_rule_said_again_in_other_words_takes_the_old_ones_place(self):
        old = self.store.remember_fact(RULE, 'owner-note', 'draft', quote='we stopped using them')['id']
        new = self.store.remember_fact(REWORDED, 'owner-note', 'draft', quote='we stopped using them')
        self.assertEqual(new['merged'], 1)
        self.assertEqual(self.current(), {new['id']: REWORDED})
        self.assertEqual(self.store.unmerge_fact(new['id']), {'restored': 1})  # Learning's Undo merge
        self.assertEqual(self.current(), {old: RULE})

    def test_the_chats_undo_brings_back_the_wording_it_replaced(self):
        old = self.store.remember_fact(RULE, 'owner-note', 'draft', quote='we stopped using them')['id']
        new = self.store.remember_fact(REWORDED, 'owner-note', 'draft', quote='we stopped using them')['id']
        self.store.forget_fact(new, undo=True)
        self.assertEqual(self.current(), {old: RULE})

    def test_the_same_words_again_count_as_said_again(self):
        old = self.store.remember_fact(RULE, 'owner-note', 'draft', quote='we stopped using them')['id']
        self.assertEqual(self.store.remember_fact(SAME, 'owner-note', 'draft', quote='we stopped using them'), {'id': old, 'duplicate': True})
        self.assertEqual(self.store.remember_fact('Lead with the partner’s concrete benefit before the ask in listing exchange emails.', 'owner-note', 'draft', quote='we stopped using them'),
                         {'id': old, 'duplicate': True})  # says less: nothing new
        self.assertEqual(self.current(), {old: RULE})

    def test_learnings_remove_does_not_bring_back_what_it_replaced(self):
        self.store.remember_fact(RULE, 'owner-note', 'draft', quote='we stopped using them')
        new = self.store.remember_fact(REWORDED, 'owner-note', 'draft', quote='we stopped using them')['id']
        self.store.forget_fact(new)
        self.assertEqual(self.current(), {})

    def test_facts_that_differ_in_a_name_day_or_number_stay_apart(self):
        for text in ('Sam is on support chat during the week of 2026-10-19.', 'Sam is on support chat during the week of 2026-10-26.',
                     'Lee is on support chat during the week of 2026-10-26.', 'Invoices over 5,000 go to the finance lead.',
                     'Invoices over 9,000 go to the finance lead.', 'The office is closed on Fridays in August.',
                     'The office is closed on Mondays in August.'):
            self.store.remember_fact(text, 'owner-note', quote='we stopped using them')
        self.assertEqual(len(self.current()), 7)

    def test_a_fact_and_a_rule_in_the_same_words_stay_apart(self):
        self.store.remember_fact(RULE, 'owner-note', 'draft', quote='we stopped using them')
        self.store.remember_fact(REWORDED, 'owner-note', quote='we stopped using them')
        self.assertEqual(len(self.current()), 2)

    def test_the_owners_own_words_are_never_replaced(self):
        old = self.store.remember_fact(RULE, 'owner-note', 'draft', quote='we stopped using them')['id']
        self.store.edit_fact(old, RULE.replace('the ask', 'the ask, always'))
        kept = self.current()[old]
        new = self.store.remember_fact(REWORDED.replace('the ask', 'the ask, always'), 'owner-note', 'draft', quote='we stopped using them')['id']
        self.assertEqual(self.current(), {old: kept, new: REWORDED.replace('the ask', 'the ask, always')})  # beside it, not instead

    def test_a_different_name_number_or_a_not_keeps_them_apart(self):
        self.store.remember_fact('Prefers email over calls for contract questions.', 'owner-note', quote='we stopped using them')
        for text in ('Lee prefers email over calls for contract questions.', 'Prefers email over calls for contract questions over 5,000.',
                     'Never prefers email over calls for contract questions.'):
            self.assertNotIn('merged', self.store.remember_fact(text, 'owner-note', quote='we stopped using them'))
        self.assertEqual(len(self.current()), 4)

    def test_the_same_words_in_another_order_that_change_the_meaning_stay_apart(self):
        for first, second in (('Pay the contractor before the landlord each month.', 'Pay the landlord before the contractor each month.'),
                              ('Prefers email over phone calls.', 'Prefers phone calls over email.'),
                              ('Send the summary to the client, then the board.', 'Send the summary to the board, then the client.'),
                              ('Quarterly reports go out after the invoices are checked.', 'Invoices go out after the quarterly reports are checked.')):
            with self.subTest(second=second):
                self.assertIsNone(facts.rewords(second, first))
                self.assertIsNone(facts.rewords(first, second))
        old = self.store.remember_fact('Pay the contractor before the landlord each month.', 'owner-note', quote='we stopped using them')['id']
        new = self.store.remember_fact('Pay the landlord before the contractor each month.', 'owner-note', quote='we stopped using them')
        self.assertNotIn('duplicate', new)
        self.assertEqual(sorted(self.current()), sorted([old, new['id']]))

    def test_clauses_that_only_move_still_count_as_other_words(self):
        self.assertEqual(facts.rewords(REWORDED, RULE), 'more')
        self.assertEqual(facts.rewords(SAME, RULE), 'less')
        self.assertEqual(facts.rewords('Lead with the partner’s concrete benefit before the ask in listing exchange emails.', RULE), 'less')
        self.assertEqual(facts.rewords('Invoices go to finance on the first working day.', 'On the first working day, invoices go to finance.'), 'less')

    def test_the_condense_pass_is_told_which_ones_are_close_in_meaning(self):
        ids = [self.store.remember_fact(t, 'owner-note', 'draft', quote='we stopped using them')['id'] for t in
               ('Lead listing emails with the partner benefit.', 'Open exchange emails with what the partner gains.',
                'Put the order number in the subject line.', 'Keep follow-ups to three short lines.',
                'Sign emails with the first name only.', 'Attach the price sheet to vendor replies.')]
        vectors = {ids[0]: [1.0, 0.0], ids[1]: [0.96, 0.28], ids[2]: [0.0, 1.0], ids[3]: [0.6, 0.8], ids[4]: [-0.6, 0.8], ids[5]: [-1.0, 0.0]}
        with self.store.connect() as db:
            db.executemany('INSERT INTO fact_vectors(fact_id,model,vector) VALUES(?,?,?)',
                           [(i, 'm:2', assistant.embeddings.pack(v)) for i, v in vectors.items()])
        lines = self.store.condense_text().splitlines()
        self.assertIn(f'likely the same as id {ids[1]})', lines[0])
        self.assertIn(f'likely the same as id {ids[0]})', lines[1])
        self.assertFalse(any('likely' in line for line in lines[2:]))


if __name__ == '__main__':
    unittest.main()
