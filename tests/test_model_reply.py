"""A small turn's reply that can't be read is no answer (machine/model_reply.py): read, asked once more, and counted so a
broken model costs a few turns at most. What each job does with it is in its own test."""
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))
from machine import model_reply  # noqa: E402
from machine.model_reply import Unreadable  # noqa: E402


class ModelReply(unittest.TestCase):
    def test_read(self):
        for reply in ('{"a": [1]}', 'Sure:\n```json\n{"a": [1]}\n```', '{"a": [1]}\n{"a": [2]}', '{"a": [1]} Done {ok}.'):
            self.assertEqual(model_reply.read(reply), {'a': [1]})
        for kind, reply in ((dict, None), (dict, 'No.'), (dict, '{"a": [1]'), (dict, '{"a": 1,}'), (list, ''), (list, '[1, 2'), (list, '[' * 100000)):
            with self.assertRaises(Unreadable):
                model_reply.read(reply, kind)

    def test_rows(self):
        self.assertEqual(model_reply.rows('[]', 'todo'), [])
        self.assertEqual(model_reply.rows('[{"todo": "x"}, 1]', 'todo'), [{'todo': 'x'}])
        for reply in ('[{"todo": "x"}, {"tod', '[1]', '{"todo": "x"}'):
            with self.assertRaises(Unreadable):
                model_reply.rows(reply, 'todo')

    def test_one_turn_when_it_reads_one_more_when_not(self):
        asked = []

        def turn(*replies):
            left = iter(replies)
            asked.clear()
            return lambda prompt: (asked.append(prompt), next(left))[1]
        self.assertEqual(model_reply.ask(turn('{}'), 'page', model_reply.read), {})
        self.assertEqual(asked, ['page'])
        self.assertEqual(model_reply.ask(turn('{', '{}'), 'page', model_reply.read), {})
        self.assertEqual(asked, ['page', 'page' + model_reply.AGAIN])
        with self.assertRaises(Unreadable):
            model_reply.ask(turn('{', '{', '{}'), 'page', model_reply.read)
        self.assertEqual(len(asked), 2)

    def test_waiting_rests_and_stops(self):
        app, clock = types.SimpleNamespace(), [1_000_000.0]
        with patch.object(model_reply.time, 'time', lambda: clock[0]):
            wait = model_reply.waiting(app, 'job')
            self.assertIs(model_reply.waiting(app, 'job'), wait)
            self.assertFalse(wait.resting())
            for n in range(1, model_reply.TRIES + 1):
                wait.missed(['a'])
                self.assertTrue(wait.resting())
                self.assertEqual(wait.spent('a'), n == model_reply.TRIES)
                clock[0] += model_reply.REST_SECONDS
                self.assertFalse(wait.resting())
            self.assertFalse(wait.spent('b') or model_reply.waiting(app, 'other').spent('a'))
            for _ in range(model_reply.PASSES_A_DAY - model_reply.TRIES):
                wait.missed(['b'])
                clock[0] += model_reply.REST_SECONDS
            self.assertTrue(wait.out() and wait.resting())
            clock[0] += model_reply.DAY
            self.assertFalse(wait.out() or wait.resting() or wait.spent('a'))


if __name__ == '__main__':
    unittest.main()
