"""A to-do's source line names what its event is, or says nothing: never "Signal" for a kind nothing names, which reads
as the Signal app (machine/store/cards.py shown_source)."""
import json
import tempfile
import unittest
from pathlib import Path

import assistant
from machine.store.cards import source_kind, source_label, source_line
from machine.store.views import source_lines_shown

AT = '2026-11-12T09:00:00+00:00'


def row(kind, id=1, **meta):
    return {'id': id, 'kind': kind, 'occurred_at': AT, 'metadata': json.dumps(meta)}


class SourceLineKinds(unittest.TestCase):
    def test_a_kind_nothing_names_gives_no_line(self):
        for kind in ('assistant.test', 'machine.reconnect_ask', 'nothing.here'):
            self.assertIsNone(source_line([row(kind)]), kind)
        self.assertIsNone(source_label('nothing.here'))
        self.assertEqual(source_kind('nothing.here'), 'signal')  # the model's word for it stays

    def test_a_named_one_after_it_leads_instead(self):
        line = source_line([row('assistant.test'), row('gmail.message', 2, sender_display='Robin')])
        self.assertTrue(line.startswith('Source: email from Robin · '), line)

    def test_the_machines_own_and_meetings_have_names(self):
        self.assertTrue(source_line([row('machine.fault')]).startswith('Source: The Machine · '))
        self.assertTrue(source_line([row('meeting.notes')]).startswith('Source: meeting notes · '))
        self.assertTrue(source_line([row('meeting.transcript')]).startswith('Source: transcript · '))

    def test_a_routines_own_to_do_names_the_routine(self):
        self.assertTrue(source_line([row('routine.cleanup', sender_display='Spam cleanup')]).startswith('Source: your routine Spam cleanup · '))
        self.assertTrue(source_line([row('routine.facebook_birthdays', sender_display='Birthdays')]).startswith('Source: your routine Birthdays · '))
        self.assertTrue(source_line([row('fleet.brief', sender_display='your Fleet')]).startswith('Source: your Fleet · '))

    def test_a_line_saved_before_says_nothing_now(self):
        cards = [{'id': 'a', 'source_line': 'Source: signal · Thu 12 Nov'}, {'id': 'b', 'source_line': 'Source: signal from Sam · Thu 12 Nov'},
                 {'id': 'c', 'source_line': 'Source: email from Robin · Thu 12 Nov'}]
        with tempfile.TemporaryDirectory() as tmp:
            store = assistant.Store(Path(tmp) / 'events.sqlite')
            with store.connect() as db:
                source_lines_shown(db, cards)
        self.assertEqual([c['source_line'] for c in cards], [None, None, 'Source: email from Robin · Thu 12 Nov'])


if __name__ == '__main__':
    unittest.main()
