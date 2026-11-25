"""The call shapes a Do it run is told to write are the ones the service takes: every {kind:…} in the rules and the job
message goes through the real validators, and every assistant_signals action they name is in the real tool schema. A run
copies these as they are, so a shape that drifts from its validator is a refused call on every run (2026-11: one in seven)."""
import itertools
import json
import re
import unittest
from pathlib import Path
from unittest import mock
import calendar_writes
import doc_writes
import linear_writes
import next_actions as n
import test_doc_writes
from machine.app import preparation

ROOT = Path(__file__).parent.parent
SOURCES = ('PREPARATION.md', 'machine/app/preparation.py', 'machine/sources/connectors.py', 'machine/new_post.py', 'github_route.py',
           'parked_fixes.py')
CONFIG = {'accounts': [
    {'id': 'work-gmail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@example.com', 'boundary': 'work:Example'},
    {'id': 'work-slack', 'service': 'slack', 'boundary': 'work:Example'}, {'id': 'work-linkedin', 'service': 'linkedin'},
    {'id': 'work-x', 'service': 'x', 'handle': 'robin'}, {'id': 'home-whatsapp', 'service': 'whatsapp'},
    {'id': 'home-telegram', 'service': 'telegram'}, {'id': 'work-teams', 'service': 'teams'},
    {'id': 'work-intercom', 'service': 'intercom', 'credential': 'read', 'reply_credential': 'reply', 'reply_admin_id': '7','reply_admin_name': 'Robin'},
    {'id': 'work-calendar', 'service': 'calendar', 'email': 'robin@example.com', 'gog_client': 'x', 'calendar': {'write': True}}]}
ACCOUNT = {'email': 'work-gmail', 'slack': 'work-slack', 'linkedin': 'work-linkedin', 'x': 'work-x', 'whatsapp': 'home-whatsapp',
           'telegram': 'home-telegram', 'teams': 'work-teams', 'intercom': 'work-intercom', 'doc_write': 'acme-docs'}
CHAT = {'name': 'Sam Example', 'account_id': None}
CONTEXT = {
    'linkedin_threads': {'c1': {**CHAT, 'account_id': 'work-linkedin'}}, 'intercom_conversations': {'c1': {**CHAT, 'account_id': 'work-intercom'}},
    'x_threads': {'mentions': {'t1': {'account_id': 'work-x', 'screen_name': 'sam'}}, 'dms': {'c1': {**CHAT, 'account_id': 'work-x'}}},
    'whatsapp_chats': {'c1': {**CHAT, 'account_id': 'home-whatsapp'}}, 'telegram_chats': {'c1': {**CHAT, 'account_id': 'home-telegram'}},
    'teams_chats': {'c1': {**CHAT, 'account_id': 'work-teams'}},
    'doc_write_context': {
        'accounts': {'acme-docs': {'name': 'Robin', 'provider': 'google', 'writes': ['create', 'edit', 'done']}},
        'files': {**test_doc_writes.FILES, 'task1': {'account_id': 'acme-docs', 'doc_title': 'A task', 'task': True, 'provider': 'notion'}},
        'snapshots': {'doc1': doc_writes.google_snapshot(test_doc_writes.gdoc(['Q4 plan', 'Launch in week 2.']), 'doc1')}}}
SAMPLE = {  # a fitting value for each key; a key no shape here has a value for is new, and needs one
    'to': ['sam@example.com'], 'subject': 'Plan', 'body': 'Hi Sam, here it is.', 'conversation_id': 'c1', 'profile': 'sam-example',
    'to_name': 'Sam Example', 'reply_to': 't1', 'chat_id': 'c1', 'to_email': 'sam@example.com', 'instructions': 'Open it and submit.',
    'preview': 'The claim of 12 October', 'message': 'Hello there', 'title': 'Plan', 'changes': [{'find': 'week 2', 'replace': 'week 3'}],
    'start': '2027-10-27T16:00:00+01:00', 'end': '2027-10-27T17:00:00+01:00', 'location': 'Office', 'notes': 'Bring it', 'calendar': 'work-calendar',
    'event': 5, 'clone': '/nowhere', 'summary': 'It fixes the bug.', 'bug': {}}


def text_of(name):
    text = (ROOT / name).read_text()
    if name.endswith('.py'):  # string literals split over lines, and an f-string's doubled braces
        text = re.sub(r"""["']+\s*\n\s*f?["']+""", '', text).replace('{{', '{').replace('}}', '}')
    return text


def parts(text, stop='}'):
    """The comma-separated items at the start of text up to its closing brace; commas inside <>, [], {} and () are text."""
    found, depth = [''], 0
    for c in text:
        if c in '<[{(':
            depth += 1
        elif c in '>]})':
            if c == stop and not depth:
                return [x.strip() for x in found]
            depth -= 1
        if c == ',' and not depth:
            found.append('')
        else:
            found[-1] += c
    raise AssertionError(f'no end: {text[:80]}')


def shapes(name):
    """[(kind, {key: raw value or ''}, whole)] of each {kind:…} written in the file; not whole: it says "..." or names a part."""
    text, out = text_of(name), []
    for found in re.finditer(r"\{kind:(?=['\w])", text):
        items = parts(text[found.end():])
        kind = items[0].strip("'")
        keys = dict((i.split(':', 1) + [''])[:2] for i in items[1:] if re.match(r'\w+(:|$)', i))
        out.append((kind, keys, '...' not in items[1:]))
    return out


def labels(raw):
    """The labels a shape writes: 'Submit …'/'Pay …' are two; … and <what it is> stand for a few words."""
    return [re.sub(r'…|<[^>]*>', 'Acme', x.replace('{label}', 'Publish post')).strip().strip("'") for x in re.split(r"(?<=')/(?=')", raw)]


def values(kind, keys, whole):
    """The calls a run writes from this shape."""
    base = {'kind': kind}
    for key, raw in keys.items():
        if key == 'account_id':
            base[key] = ACCOUNT[kind]
        elif key == 'url':
            base[key] = 'https://example.com/page'
        elif key == 'file_id':
            base[key] = 'task1' if "'done'" in keys.get('op', '') else 'doc1'
        elif key not in ('label', 'op'):
            base[key] = SAMPLE[key]
    if not whole or kind == 'finish' and 'instructions' not in keys:
        base = {'instructions': SAMPLE['instructions'], 'preview': SAMPLE['preview'], 'label': 'Submit', **base}
    out = [{**base, **({'label': x} if x else {})} for x in labels(keys.get('label', ''))]
    ops = re.findall(r'[a-z]+', keys.get('op', '').replace(' or ', ' '))
    return [{**v, 'op': op, **({'title': 'Plan'} if op == 'update' else {})} for v in out for op in ops] if ops else out


class CallShapes(unittest.TestCase):
    def take(self, value):
        with mock.patch.object(calendar_writes, 'account_for', lambda config, i: CONFIG['accounts'][-1]):
            return n.validate(value, CONFIG, [a['id'] for a in CONFIG['accounts']], calendar_events={5: {
                'account_id': 'work-calendar', 'source_id': 's5', 'title': 'Call', 'start': '2027-10-26T16:00:00+01:00',
                'end': '2027-10-26T17:00:00+01:00', 'all_day': False, 'guests': []}}, **CONTEXT)

    def test_every_written_shape_is_one_the_service_takes(self):
        seen = set()
        for name in SOURCES:
            for kind, keys, whole in shapes(name):
                for value in values(kind, keys, whole):
                    with self.subTest(where=name, value=value):
                        seen.add(kind)
                        if kind == 'merge':  # it reads a clone: its keys and label are checked first
                            with self.assertRaisesRegex(ValueError, 'Fix a clone'):
                                n.validate(value, CONFIG, [])
                        else:
                            self.assertEqual(self.take(value)['kind'], kind)
        self.assertLessEqual({'email', 'linkedin', 'x', 'whatsapp', 'intercom', 'slack', 'handoff', 'merge', 'finish', 'prepare', 'open',
                              'doc_write', 'calendar'}, seen)  # each is still found: the test reads what a run reads

    def test_the_same_shape_fits_the_chats_named_beside_it(self):
        line = next(x for x in (ROOT / 'PREPARATION.md').read_text().splitlines() if x.startswith('`{kind:whatsapp'))
        for kind in re.findall(r'(?<!\{)kind:(\w+)', line):
            self.assertEqual(self.take({'kind': kind, 'label': 'Send reply', 'account_id': ACCOUNT[kind], 'chat_id': 'c1', 'body': 'Hi'})['kind'], kind)

    def test_linear_s_shapes_name_its_own_fields(self):
        said = linear_writes.prompt({'accounts': [{'id': 'l', 'service': 'linear'}]})
        shapes_ = re.findall(r"op:'(\w+)' \{([^}]*)\}", said)
        self.assertEqual({op for op, _ in shapes_}, {'comment', 'state', 'assign', 'create'})
        for op, keys in shapes_:
            value = {'kind': 'linear', 'op': op, **{k.strip(' ?'): 'x' for k in keys.split(',')}}
            with self.assertRaises(ValueError) as caught:  # past its fields and op: only the empty context is refused
                linear_writes.validate(value, {})
            self.assertNotRegex(str(caught.exception), 'A Linear change has|op is comment')

    def test_every_action_they_name_is_in_the_tool_schema(self):
        source = (ROOT / 'openclaw-plugin/index.ts').read_text()
        actions = set(json.loads(re.search(r'const TOOL_ACTIONS = (\[[^\]]*\])', source)[1].replace("'", '"')))
        named = set(itertools.chain(*(re.findall(r'assistant_signals ([a-z]+_?[a-z_]*)(?= args| \{|, |\))', text_of(x)) for x in SOURCES)))
        self.assertLessEqual({'prepare', 'preparation_blocked', 'remember_fact'}, named)
        self.assertEqual(named - actions, set())

    def test_the_limits_they_say_are_the_ones_checked(self):
        rules = (ROOT / 'PREPARATION.md').read_text()
        self.assertIn(f'A label has at most {n.LABEL_MAX} characters', rules)
        long = {'kind': 'prepare', 'label': 'Draft ' + 'x' * n.LABEL_MAX, 'instructions': 'x'}
        with self.assertRaisesRegex(ValueError, f'label has {n.LABEL_MAX + 6} characters, at most {n.LABEL_MAX}: “Draft'):
            n.validate(long, CONFIG, [])
        self.take({**long, 'label': long['label'][:n.LABEL_MAX]})
        for verb in re.search(r'starts with what the click does: ([\w, ]+)…', rules)[1].split(', '):
            self.assertIn(verb, n.FINISH_VERBS)
        self.assertIn(f'at most {doc_writes.MAX_THEN} characters', text_of('machine/sources/connectors.py'))
        handoff = {'kind': 'handoff', 'to_email': 'sam@example.com', 'to_name': 'Sam', 'body': 'x' * 1000}
        self.assertIn('what they get, at most 1000 characters', rules)
        self.take(handoff)
        with self.assertRaisesRegex(ValueError, 'at most 1000'):
            self.take({**handoff, 'body': 'x' * 1001})

    def test_a_label_takes_names_handles_and_amounts(self):
        for text in ('Send to José', 'Send @sam a reply', 'Send the €120 invoice', 'Send Sam & Ana', 'Send #3'):
            self.assertEqual(self.take({'kind': 'linkedin', 'account_id': 'work-linkedin', 'conversation_id': 'c1', 'body': 'x', 'label': text})['label'], text)
        for text in ('Send\nnow', 'Send <b>', '1 reply', 'Send [x](y)', 'Send a.com', '€120'):
            with self.assertRaisesRegex(ValueError, 'short specific'):
                self.take({'kind': 'linkedin', 'account_id': 'work-linkedin', 'conversation_id': 'c1', 'body': 'x', 'label': text})

    def test_do_now_goes_beside_the_steps_and_the_refusal_says_so(self):
        edit = {'kind': 'doc_write', 'op': 'edit', 'file_id': 'doc1', 'changes': SAMPLE['changes']}
        for kind in (edit, {'kind': 'finish', 'label': 'Apply fix', 'instructions': 'x', 'preview': 'y'}):
            with self.assertRaisesRegex(ValueError, 'do_now goes beside next_actions'):
                self.take({**kind, 'do_now': True})
        with self.assertRaisesRegex(ValueError, 'leave out note'):
            self.take({**edit, 'note': 'x'})
        job = {'job_id': 'j' * 32, 'suggestion_id': 's1'}
        for said in (preparation.chat_prompt(job), preparation.preparation_prompt(job)):
            self.assertIn('do_now:true beside next_actions', said)


if __name__ == '__main__':
    unittest.main()
