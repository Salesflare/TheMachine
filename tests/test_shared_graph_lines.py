"""A shared record's Timeline under Team (shared_graph_lines.py): one line per real event however many teammates had it,
in the viewer's language, the one that says who did what, with every teammate it came from."""
import unittest

import shared_graph as sg
import shared_graph_lines as sgl
from shared_graph_takeback import shrunk

A, B = '2026-11-12T14:38:00+01:00', '2026-11-09T14:54:00+01:00'
KA, KB = 'a' * 32, 'b' * 32


def line(who, score, at, text, k=None, lang=None):
    return {'at': at, 'line': text, 'member': ('fl', 'm_' + who.lower()), 'who': who, 'score': score,
            **({'k': k} if k else {}), **({'lang': lang} if lang else {})}


TEAM = ('Mara', 'Ilse', 'Noor', 'Teo', 'Pim', 'Dana')


class Merge(unittest.TestCase):
    def test_the_same_event_from_every_teammate_is_one_line_via_all_of_them(self):
        lines = [line('Mara', 5, A, 'Support follow-up remains with the assigned teammate', KA, 'en'),
                 line('Ilse', 4, A, 'Support verzorgt de verdere klantopvolging.', KA, 'nl'),
                 line('Noor', 3, A, 'Noor closed the unanswered account recovery conversation.', KA, 'en'),
                 line('Teo', 2, A, 'Noor closed the unanswered recovery request', KA, 'en'),
                 line('Pim', 1, A, 'Partner or customer conversation received a follow-up.', KA, 'en'),
                 line('Ilse', 4, B, 'Dana kreeg een antwoord over de facturatie.', KB, 'nl'),
                 line('Noor', 3, B, 'Noor answered Dana about the invoice address', KB, 'en'),
                 line('Teo', 2, B, 'Billing question got a reply.', KB, 'en')]
        got = sgl.merge(lines, 'en', TEAM)
        self.assertEqual([(x['line'], x['via']) for x in got], [
            ('Noor closed the unanswered account recovery conversation', ['Mara', 'Ilse', 'Noor', 'Teo', 'Pim']),
            ('Noor answered Dana about the invoice address', ['Ilse', 'Noor', 'Teo'])])

    def test_two_messages_at_the_same_minute_stay_two_lines(self):
        got = sgl.merge([line('Mara', 2, A, 'Dana asked for the quote', KA), line('Teo', 1, A, 'Dana sent the signed order', KB)], 'en', TEAM)
        self.assertEqual(len(got), 2)

    def test_without_a_message_hash_teammates_lines_within_minutes_are_one_event(self):
        later = '2026-11-12T14:40:30+01:00'
        got = sgl.merge([line('Mara', 2, A, 'Dana asked for the quote'), line('Teo', 1, later, 'Quote request came in')], 'en', TEAM)
        self.assertEqual([(x['line'], x['via']) for x in got], [('Dana asked for the quote', ['Mara', 'Teo'])])
        # an hour apart: two events; one teammate's own two lines are two facts, however close
        hour = '2026-11-12T15:38:00+01:00'
        self.assertEqual(len(sgl.merge([line('Mara', 2, A, 'Dana asked for the quote'), line('Teo', 1, hour, 'Dana paid')], 'en', TEAM)), 2)
        self.assertEqual(len(sgl.merge([line('Mara', 2, A, 'Dana asked for the quote'), line('Mara', 2, later, 'Mara sent it')], 'en', TEAM)), 2)

    def test_the_line_is_in_the_viewers_language(self):
        lines = [line('Mara', 2, A, 'Dana asked for a new quote for 12 seats', KA, 'en'),
                 line('Ilse', 1, A, 'Dana vroeg om een nieuwe offerte voor 12 plaatsen, met korting voor het hele team', KA, 'nl')]
        self.assertEqual(sgl.merge(lines, 'en', TEAM)[0]['line'], 'Dana asked for a new quote for 12 seats')
        self.assertEqual(sgl.merge(lines, 'nl', TEAM)[0]['line'], 'Dana vroeg om een nieuwe offerte voor 12 plaatsen, met korting voor het hele team')
        # a line that doesn't say its language (a Machine from before) comes before one in another language
        old = [line('Mara', 2, A, 'Dana asked for a new quote'), line('Ilse', 1, A, 'Dana vroeg om een nieuwe offerte', KA, 'nl')]
        self.assertEqual(sgl.merge(old, 'en', TEAM)[0]['line'], 'Dana asked for a new quote')

    def test_the_line_that_says_who_did_what_wins_over_a_vague_one(self):
        lines = [line('Mara', 5, A, 'Partner or customer conversation received a follow-up from the team today.', KA, 'en'),
                 line('Teo', 1, A, 'Noor closed the recovery request', KA, 'en')]
        self.assertEqual(sgl.merge(lines, 'en', TEAM)[0]['line'], 'Noor closed the recovery request')

    def test_an_event_line_never_ends_in_a_period_whoever_wrote_it(self):
        self.assertEqual([sgl.bare(x) for x in ('Dana paid.', ' Dana  paid. ', 'Dana paid', 'Dana paid...', 'Dana paid…', '', None)],
                         ['Dana paid', 'Dana paid', 'Dana paid', 'Dana paid...', 'Dana paid…', '', ''])
        got = sgl.merge([line('Mara', 2, A, 'Dana asked for the quote.', KA), line('Teo', 1, B, 'Dana paid.', KB)], 'en', TEAM)
        self.assertEqual([x['line'] for x in got], ['Dana asked for the quote', 'Dana paid'])
        # with and without its period, one fact
        self.assertEqual(len(sgl.unique_lines([{'line': 'Dana paid.'}, {'line': 'Dana paid'}])), 1)
        # what this Machine sends: a review's line and a project's move alike
        self.assertEqual(sg._line('Moved to Won: Dana signed the order form.'), 'Moved to Won: Dana signed the order form')

    def test_the_same_words_on_two_events_show_once(self):
        got = sgl.merge([line('Mara', 2, A, 'Dana and Mara agreed to reschedule', KA), line('Teo', 1, B, 'Dana and Mara agreed to reschedule', KB)], 'en', TEAM)
        self.assertEqual([(x['at'], x['via']) for x in got], [(A, ['Mara', 'Teo'])])


class EventKey(unittest.TestCase):
    def test_the_same_message_has_the_same_key_in_every_mailbox(self):
        one = sgl.event_key('gmail.message', {'message-id': '<Abc@Mail.example>', 'thread_id': 't-1'}, A)
        other = sgl.event_key('ms_graph.message', {'message-id': ' <abc@mail.example> ', 'thread_id': 'AAQk'}, B)
        self.assertEqual(one, other)
        self.assertIsNone(sgl.event_key('gmail.message', {'thread_id': 't-1'}, A))  # a mailbox's own thread id: never
        self.assertEqual(sgl.event_key('slack.message', {'channel_id': 'C1', 'message_ts': '1.2', 'thread_ts': '1.0'}, A), 'slack|C1|1.2')
        self.assertEqual(sgl.event_key('intercom.conversation', {'conversation_id': '77'}, A), 'ic:77|' + A)

    def test_a_teammates_record_keeps_only_a_hash_and_a_known_language(self):
        rec = sg._clean_record({'r': 'x' * 32, 't': 'person', 'timeline': [
            {'at': A, 'line': 'Dana asked', 'k': KA, 'lang': 'nl'},
            {'at': B, 'line': 'Dana paid', 'k': 'lee@client.example', 'lang': 'Klingon <b>'}]})
        self.assertEqual(rec['timeline'], [{'at': A, 'line': 'Dana asked', 'k': KA, 'lang': 'nl'}, {'at': B, 'line': 'Dana paid'}])

    def test_a_take_back_keeps_lines_that_went_before_the_hash(self):
        was = {'r': 'r1', 't': 'person', 'timeline': [{'at': A, 'line': 'Dana asked'}, {'at': B, 'line': 'Dana paid'}]}
        now = {'r': 'r1', 't': 'person', 'timeline': [{'at': A, 'line': 'Dana asked', 'k': KA, 'lang': 'en'}]}
        _, changed, removed = shrunk({'r1': was}, {'r1': 'h'}, {'r1': now})
        self.assertEqual((changed[0]['timeline'], removed), ([{'at': A, 'line': 'Dana asked'}], []))


if __name__ == '__main__':
    unittest.main()
