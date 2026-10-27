"""What the Machine creates or sends from now on reads in the owner's language: Telegram replies, event lines, to-do
titles it writes, push notifications. Text already stored stays as it was. The send and write paths below take no new
hard-coded English: every string the owner reads goes through i18n.t()."""
import ast
import json
import pathlib
import sqlite3
import unittest
from unittest import mock

import assistant
import fleet
import i18n
import locale_prefs

ROOT = pathlib.Path(__file__).resolve().parent.parent

# The functions that build text the Machine sends to its owner or writes into a to-do or its Events.
PATHS = {
    'assistant.py': ['card', 'controls', 'prompt_text', 'reminder_line', 'push_notify', 'telegram', 'promise_text', 'checkin_line',
                     'settle_sent', 'recap_graph_lines', 'recap_share_lines', 'weekly_recap_message', 'recap_buttons',
                     'fleet_notify_brief', 'fleet_tell'],
    'fleet.py': ['question_text', 'asks_line', 'push_payload', 'telegram_message', 'notice_push', 'friend_settled', 'brief_text',
                 'decide_notice_from_telegram', '_people',
                 'brief_items', '_team_why', '_waited', '_on_day'],
    'fleet_requests.py': ['question_text', 'how_text', 'answer_text', 'taken_line', 'request_card', 'on_it_line', 'marked_line',
                          'request_answered'],
    'family.py': ['question_text', 'answer_text', 'family_card', 'family_reminders'],
}
# Matched by code elsewhere, so they stay as they are: 'You' sorts the owner first in the Fleet brief.
ALLOWED = {'You', 'heating up'}
# Called with a literal that is not text: their arguments are keys, patterns or SQL.
NOT_TEXT = {'get', 'startswith', 'endswith', 'search', 'match', 'fullmatch', 'sub', 'findall', 'compile', 'execute', 'split',
            'replace', 'strip', 'log', 'join'}


def english(text):
    """A word or a phrase someone reads, not a key, a pattern, a path or SQL."""
    s = text.strip()
    if not any(c.isalpha() for c in s) or s.startswith(('http', '/', '#', '(?', 'SELECT', 'UPDATE', 'INSERT', 'assistant:')):
        return False
    if '_' in s or '\\' in s or '%' in s or '$' in s.replace('${}', ''):
        return False
    words = [w for w in s.split() if w.isalpha() and len(w) > 1]
    return len(words) >= 2 or (len(words) == 1 and s[0].isupper() and s[1:2].islower())


def is_t(node):
    return isinstance(node, ast.Call) and (isinstance(node.func, ast.Name) and node.func.id == 't'
                                           or isinstance(node.func, ast.Attribute) and node.func.attr == 't')


def hard_coded(source, names):
    """(function, literal) for each English literal in those functions that does not go through t()."""
    out = []
    for fn in ast.walk(ast.parse(source)):
        if not isinstance(fn, ast.FunctionDef) or fn.name not in names:
            continue
        skip = set()
        for n in ast.walk(fn):
            parts = []
            if is_t(n) and n.args:
                parts = [n.args[0]]
            elif isinstance(n, ast.Compare):
                parts = [n.left, *n.comparators]
            elif isinstance(n, ast.Dict):
                parts = [k for k in n.keys if k]
            elif isinstance(n, ast.Subscript):
                parts = [n.slice]
            elif isinstance(n, ast.Raise):  # an error the bridge matches by its text (still English, see the PR)
                parts = [n]
            elif isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant):  # a docstring
                parts = [n]
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in NOT_TEXT:
                parts = n.args
            skip |= {id(x) for p in parts for x in ast.walk(p)}
        out += [(fn.name, n.value) for n in ast.walk(fn)
                if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in skip and english(n.value)]
    return out


class NoNewEnglishTest(unittest.TestCase):
    def test_the_send_and_write_paths_have_no_english_outside_the_catalog(self):
        # A label picked first and translated after (controls' choices, the recap's buttons) is a catalog key; anything
        # else needs t() at the spot, in every language.
        keys = set(json.loads((ROOT / 'i18n' / 'en.json').read_text(encoding='utf-8')))
        found = {(path, fn, text) for path, names in PATHS.items()
                 for fn, text in hard_coded((ROOT / path).read_text(encoding='utf-8'), names)
                 if text not in keys and text not in ALLOWED}
        self.assertEqual(sorted(found), [], 'wrap these in t() and add them to i18n/*.json')

    def test_the_check_finds_hard_coded_english(self):
        source = "def telegram(row):\n    return {'title': 'Ready to send', 'ok': t('Done'), 'key': row.get('Some key')}\n"
        self.assertEqual(hard_coded(source, ['telegram']), [('telegram', 'Ready to send')])

    def test_every_key_the_paths_use_is_in_the_catalog(self):
        keys = set(json.loads((ROOT / 'i18n' / 'en.json').read_text(encoding='utf-8')))
        missing = set()
        for path in [*PATHS, 'shared_graph.py']:
            for n in ast.walk(ast.parse((ROOT / path).read_text(encoding='utf-8'))):
                if is_t(n) and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
                    if n.args[0].value not in keys:
                        missing.add((path, n.args[0].value))
        self.assertEqual(sorted(missing), [])


class OwnersLanguageTest(unittest.TestCase):
    def tearDown(self):
        locale_prefs.configure({})

    def each(self):
        """Dutch, then French, then back to English for what follows the loop."""
        for lang in ('nl', 'fr'):
            locale_prefs.configure({'language': lang})
            yield lang
        locale_prefs.configure({})

    def test_a_telegram_reply(self):
        config = {'dashboard_host': 'machine.example', 'telegram_owner': '1'}
        row = {'_result_notice': True, 'title': 'Quote for Acme', 'status': 'prepared', 'id': 'c1', 'message_id': 'web-1'}
        for lang in self.each():
            with mock.patch.object(assistant, 'telegram_request', side_effect=lambda config, args: args):
                sent = assistant.telegram(config, row, 'send')
            self.assertTrue(sent['message'].startswith(i18n.t('Ready: {}', '**Quote for Acme**', lang=lang)), sent['message'])
            self.assertIn({'nl': 'Klaar', 'fr': 'Prêt'}[lang], sent['message'])
            self.assertIn('[' + i18n.t('View result', lang=lang) + ']', sent['message'])
            self.assertNotIn('View result', sent['message'])
        with mock.patch.object(assistant, 'telegram_request', side_effect=lambda config, args: args):
            self.assertTrue(assistant.telegram(config, row, 'send')['message'].startswith('Ready: **Quote for Acme**'))

    def test_an_event_line(self):
        for lang in self.each():
            db = sqlite3.connect(':memory:')
            db.row_factory = sqlite3.Row
            db.executescript("CREATE TABLE suggestions(id,status,next_action,body,outcome);"
                             "CREATE TABLE action_jobs(suggestion_id,revision,status);"
                             "INSERT INTO suggestions VALUES('c1','prepared',NULL,'Draft ready.',NULL);")
            store = mock.Mock()
            self.assertTrue(assistant.settle_sent(store, db, 'c1', 'job1', label='Reply to Pat'))
            line = store._decide.call_args.args[3]
            self.assertEqual(line, i18n.t('Sent: {}', 'Reply to Pat', lang=lang))
            self.assertNotEqual(line, 'Sent: Reply to Pat')
            self.assertFalse(line.split()[0].lower() in ('je', 'jij', 'u', 'vous', 'tu'), line)  # no "You ..." at the start

    def test_a_handoff_title(self):
        promise = {'direction': 'theirs', 'who': 'Pat', 'what': 'send the deck', 'made_at': '2026-10-26T10:00:00+00:00', 'due': None}
        for lang in self.each():
            title, body = assistant.promise_text(promise)
            self.assertEqual(title, i18n.t('Waiting on {}: {}', 'Pat', 'send the deck', lang=lang))
            self.assertNotIn('Waiting on', title)
            self.assertNotIn('Promised', body)
        self.assertEqual(assistant.promise_text(promise)[0], 'Waiting on Pat: send the deck')

    def test_a_push_notification(self):
        row = {'id': 'q1', 'name': 'Pat', 'kind': 'relationships', 'question': json.dumps({'about': 'Acme'})}
        for lang in self.each():
            push = fleet.push_payload([row], 'https://machine.example/')
            self.assertEqual(push['title'], i18n.t("{}'s Machine asks", 'Pat', lang=lang))
            self.assertIn('Machine', push['title'])
            self.assertNotIn('asks', push['title'])
            self.assertEqual(push['body'], i18n.t('Who knows someone at {}?', 'Acme', lang=lang))
            self.assertNotIn('Decline', [a['title'] for a in push['actions']])
            self.assertEqual(fleet.push_payload([row, dict(row, id='q2')], '')['title'], i18n.t('{} Fleet questions wait for you', 2, lang=lang))


if __name__ == '__main__':
    unittest.main()
