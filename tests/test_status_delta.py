"""api/status as a change list (machine/web/status_delta.py): a page that sends its last token gets only what changed."""
import json
import unittest

from machine.web import status_delta


def status(**changes):
    base = {'suggestions': [{'id': 's1', 'title': 'Reply to Ann', 'status': 'pending'}, {'id': 's2', 'title': 'Invoice', 'status': 'pending'}],
            'deliveries': [], 'check': {'at': '10:00'}, 'talk_ready': True}
    return {**base, **changes}


def merged(held, answer):
    """What the dashboard puts together (shell-tabs.js statusMerge), written out in Python."""
    if '_since' not in answer:
        return answer
    out = {k: v for k, v in held.items() if k not in answer.get('_gone', ())}
    for key, value in answer.items():
        if key in ('_since', '_gone'):
            continue
        if isinstance(value, list) and any(isinstance(r, dict) and list(r) == ['='] for r in value):
            was = {json.dumps(r['id']): r for r in held[key]}
            value = [was[json.dumps(r['='])] if isinstance(r, dict) and list(r) == ['='] else r for r in value]
        out[key] = value
    return out


class StatusDelta(unittest.TestCase):
    def test_without_a_token_the_whole_answer_comes_with_one(self):
        first = status_delta.changes(status())
        self.assertEqual({k: v for k, v in first.items() if k != '_token'}, status())
        self.assertTrue(first['_token'])
        self.assertEqual(status_delta.changes(status(), 'unknown')['suggestions'], status()['suggestions'])  # a restart: all of it

    def test_the_same_answer_again_is_only_a_new_token(self):
        first = status_delta.changes(status())
        again = status_delta.changes(status(), first['_token'])
        self.assertEqual(set(again), {'_token', '_since'})
        self.assertNotEqual(again['_token'], first['_token'])

    def test_one_changed_to_do_comes_alone_and_the_rest_by_id(self):
        first = status_delta.changes(status())
        now = status(suggestions=[{'id': 's1', 'title': 'Reply to Ann', 'status': 'completed'}, status()['suggestions'][1],
                                  {'id': 's3', 'title': 'New', 'status': 'pending'}], check={'at': '10:01'})
        answer = status_delta.changes(now, first['_token'])
        self.assertEqual(answer['suggestions'], [now['suggestions'][0], {'=': 's2'}, now['suggestions'][2]])
        self.assertEqual(answer['check'], {'at': '10:01'})
        self.assertNotIn('deliveries', answer)
        self.assertEqual(merged(first, answer) | {'_token': None}, {**now, '_token': None})

    def test_a_part_that_went_is_named(self):
        first = status_delta.changes(status())
        answer = status_delta.changes({k: v for k, v in status().items() if k != 'check'}, first['_token'])
        self.assertEqual(answer['_gone'], ['check'])
        self.assertNotIn('check', merged(first, answer))

    def test_only_the_last_few_tokens_are_kept(self):
        first = status_delta.changes(status())
        for _ in range(status_delta.KEEP):
            status_delta.changes(status())
        self.assertIn('suggestions', status_delta.changes(status(), first['_token']))  # forgotten: the whole answer again

    def test_the_graph_overview_keeps_its_own_tokens(self):
        graph = {'people': [{'id': 'p1', 'name': 'Ann'}, {'id': 'p2', 'name': 'Bo'}], 'counts': {'people': 2}}
        first = status_delta.changes(graph, None, status_delta.GRAPH)
        for _ in range(status_delta.KEEP + 1):  # the status's polls never push the Graph's token out
            status_delta.changes(status())
        now = {'people': [{'id': 'p1', 'name': 'Ann'}, {'id': 'p2', 'name': 'Bo B.'}], 'counts': {'people': 2}}
        answer = status_delta.changes(now, first['_token'], status_delta.GRAPH)
        self.assertEqual(answer['people'], [{'=': 'p1'}, {'id': 'p2', 'name': 'Bo B.'}])
        self.assertNotIn('counts', answer)
        self.assertEqual(merged(first, answer) | {'_token': None}, {**now, '_token': None})
        self.assertNotIn('_since', status_delta.changes(now, first['_token']))  # a Graph token means nothing to the status

    def test_rows_without_ids_or_with_doubles_come_whole(self):
        first = status_delta.changes(status(deliveries=[{'id': 1, 'status': 'a'}, {'id': 1, 'status': 'b'}], promises=[{'what': 'x'}]))
        answer = status_delta.changes(status(deliveries=[{'id': 1, 'status': 'a'}, {'id': 1, 'status': 'c'}], promises=[{'what': 'y'}]),
                                      first['_token'])
        self.assertEqual(answer['deliveries'], [{'id': 1, 'status': 'a'}, {'id': 1, 'status': 'c'}])
        self.assertEqual(answer['promises'], [{'what': 'y'}])


if __name__ == '__main__':
    unittest.main()
