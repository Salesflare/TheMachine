"""machine/kinds.py, the one list of every kind of event and of message: that it says what the code does today, that
the dashboard gets it with the page, and a guard that fails on a new list of kinds written out by hand.

The guard counts, per file, the lists of kinds spelled out in code: two or more event kinds ('slack.message') in a
tuple, list, set, dict's keys or SQL IN list, or three or more message kinds ('email', 'slack', ...) with 'email' or
'doc_reply' among them. The files that have them today are in KIND_LISTS, with their count, which only comes down:
ask machine/kinds.py instead (kinds.of(family=kinds.MAIL), kinds.KINDS[kind]['name']), and lower the count when a
list goes. Connections by kind (mail, calendar, chat: machine/sources/groups.py) is about the services; this is about
what they store."""
import ast
import json
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import dashboard_parts  # noqa: E402
from machine import kinds, names  # noqa: E402

SKIP_DIRS = {'node_modules', '.git', '.venv', '__pycache__', 'tests'}
KINDS_FILE = 'machine/kinds.py'
EVENT_KINDS = frozenset(kinds.KINDS)
SEND_KINDS = frozenset(kinds.SENDS)
SEND_MARKERS = {'email', 'doc_reply'}  # a list of message kinds names one of these; a list of services never does
SQL_LIST = re.compile(r"\(\s*'[a-z_.]+'(?:\s*,\s*'[a-z_.]+')+\s*\)")
JS_ARRAY = re.compile(r'\[([^\[\]]*)\]')
JS_OBJECT = re.compile(r'\{([^{}]*)\}')
JS_STRING = re.compile(r"'([a-z_]+(?:\.[a-z_]+)?)'")
JS_KEY = re.compile(r"(?:^|[,{\s])'?([a-z_]+(?:\.[a-z_]+)?)'?\s*:")

# The hand-written lists of kinds each file has today: these only come down.
KIND_LISTS = {
    'ai_access.py': 1,
    'birthdays.py': 2,
    'check_now.py': 4,
    'connectors/docs.py': 2,
    'connectors/github.py': 2,
    'connectors/google_meet.py': 2,
    'connectors/salesforce.py': 2,
    'connectors/teams.py': 2,
    'connectors/x.py': 2,
    'connectors/zoom.py': 2,
    'embeddings.py': 1,
    'enrichment.py': 1,
    'fleet.py': 1,
    'fleet_learnings.py': 1,
    'fleet_requests.py': 4,
    'follow_ups.py': 2,
    'gap_note.py': 1,
    'graph.py': 18,
    'graph_board_reviews.py': 1,
    'machine/app/action_runs.py': 2,
    'machine/app/card_actions.py': 2,
    'machine/app/first_look.py': 1,
    'machine/app/fleet.py': 1,
    'machine/app/follow_ups.py': 2,
    'machine/app/mail.py': 2,
    'machine/app/new_cards.py': 1,
    'machine/app/promise_checks.py': 1,
    'machine/app/recap.py': 3,
    'machine/app/review.py': 1,
    'machine/browser.py': 1,
    'machine/graph/identities.py': 2,
    'machine/chat.py': 2,
    'machine/sources/connectors.py': 1,
    'machine/sources/gmail.py': 1,
    'machine/sources/mail_senders.py': 1,
    'machine/sources/suggest.py': 1,
    'machine/sources/whatsapp.py': 2,
    'machine/store/cards.py': 3,
    'machine/store/conversation.py': 1,
    'machine/store/core.py': 2,
    'machine/store/message_view.py': 8,
    'machine/store/profile.py': 1,
    'machine/store/review.py': 5,
    'machine/store/review_last_look.py': 1,
    'machine/store/review_wait.py': 1,
    'machine/store/views.py': 3,
    'machine/store/voices.py': 5,
    'machine/web/handler.py': 2,
    'mail_cleanup.py': 1,
    'meeting_mail.py': 2,
    'meeting_notes.py': 3,
    'meeting_prep.py': 1,
    'missed_work.py': 3,
    'next_actions.py': 1,
    'project_about.py': 1,
    'record_log.py': 1,
    'sandbox/fixture.py': 2,
    'shared_graph.py': 3,
    'shared_graph_private.py': 7,
    'talk_live.py': 1,
    'dashboard/events-list.js': 1,
    'dashboard/graph-followups-settings.js': 1,
    'dashboard/graph-record.js': 1,
    'dashboard/graph-tabs.js': 1,
    'dashboard/learning-missed.js': 1,
    'dashboard/new-todo-dialog.js': 1,
    'dashboard/shell-keys.js': 2,
    'dashboard/todos-cards.js': 5,
    'dashboard/todos-chat-talk-view.js': 1,
    'dashboard/todos-chat-thread.js': 2,
    'dashboard/todos-clear.js': 1,
    'dashboard/todos-list.js': 2,
    'dashboard/todos-logos.js': 1,
    'dashboard/todos-send.js': 2,
}


def kind_list(values):
    """Whether these strings are a list of kinds: two or more event kinds, or three or more message kinds with
    'email' or 'doc_reply' among them."""
    values = set(values)
    return len(values & EVENT_KINDS) >= 2 or (len(values & SEND_KINDS) >= 3 and bool(values & SEND_MARKERS))


def python_kind_lists(source, filename='<module>'):
    """[(line, literal)] of the lists of kinds spelled out in a Python module's code or SQL."""
    found = []
    for node in ast.walk(ast.parse(source, filename)):
        if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
            values = [e.value for e in node.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
        elif isinstance(node, ast.Dict):
            values = [k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            for match in SQL_LIST.finditer(node.value):
                if kind_list(re.findall(r"'([a-z_.]+)'", match.group(0))):
                    found.append((node.lineno, match.group(0)))
            continue
        else:
            continue
        if kind_list(values):
            found.append((node.lineno, ast.unparse(node)[:120]))
    return sorted(found)


def js_kind_lists(source):
    """[(line, literal)] of the lists of kinds spelled out in dashboard code: an array of them, or an object keyed by
    them (the innermost braces: an object with another object in it is read as its parts)."""
    found = []
    for pattern, values in ((JS_ARRAY, JS_STRING), (JS_OBJECT, JS_KEY)):
        for match in pattern.finditer(source):
            if kind_list(values.findall(match.group(1))):
                found.append((source.count('\n', 0, match.start()) + 1, match.group(0)[:120]))
    return sorted(found)


def kind_lists():
    """{file: [(line, literal)]} for every Python file outside tests and every dashboard script."""
    out = {}
    for path in sorted(ROOT.rglob('*.py')):
        rel = path.relative_to(ROOT)
        if SKIP_DIRS & set(rel.parts[:-1]) or rel.as_posix() == KINDS_FILE:
            continue
        found = python_kind_lists(path.read_text(encoding='utf-8'), rel.as_posix())
        if found:
            out[rel.as_posix()] = found
    for path in [ROOT / dashboard_parts.PAGE, *sorted((ROOT / 'dashboard').glob('*.js'))]:
        found = js_kind_lists(path.read_text(encoding='utf-8'))
        if found:
            out[path.relative_to(ROOT).as_posix()] = found
    return out


class Registry(unittest.TestCase):
    def test_every_row_is_complete_and_known(self):
        fields = {'service', 'name', 'via', 'view', 'family', 'timeline', 'send', 'mark', 'markdown', 'media', 'messenger'}
        for kind, row in kinds.KINDS.items():
            with self.subTest(kind):
                self.assertRegex(kind, r'^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$')
                self.assertEqual(set(row), fields)
                self.assertIn(row['view'], kinds.VIEWS)
                self.assertIn(row['family'], kinds.FAMILIES)
                self.assertIn(row['timeline'], kinds.TIMELINE_GROUPS)
                self.assertTrue(row['send'] is None or row['send'] in kinds.SENDS)
                self.assertTrue(row['service'] is None or row['service'] in names.SERVICES, 'a service names.SERVICES names')
                self.assertTrue(row['mark'])
        self.assertEqual(kinds.of(family=kinds.MAIL)[:2], ('gmail.message', 'outlook.message'))
        self.assertEqual(set(kinds.of(flag='media')), {'whatsapp.message', 'telegram.message', 'signal.message'})
        self.assertEqual(kinds.of(family=kinds.CHAT, flag='media', service='signal'), ('signal.message',))

    def test_it_says_what_the_code_says_today(self):
        """Until each list moves here, the registry and the list it replaces agree, kind by kind."""
        import follow_ups
        import graph
        import next_actions
        from machine.store import cards, message_view
        for kind, row in kinds.KINDS.items():
            with self.subTest(kind):
                self.assertEqual(row['name'], cards.source_label(kind), 'name: machine/store/cards.source_label')
                self.assertEqual(row['view'], message_view.view_of(kind), 'view: message_view.view_of')
                self.assertEqual(row['timeline'], graph.timeline_source(kind), 'timeline: graph.TIMELINE_SOURCES')
                self.assertEqual(row['markdown'], kind in message_view.MARKDOWN_KINDS)
                self.assertEqual(row['media'], kind in message_view.MEDIA_KINDS)
                if kind in follow_ups.CHANNEL_KINDS:
                    self.assertEqual(row['send'], follow_ups.CHANNEL_KINDS[kind], 'send: follow_ups.CHANNEL_KINDS')
        # A reply goes out on these too, though a follow-up doesn't switch to them (follow_ups.CHANNELS)
        self.assertEqual({k for k, row in kinds.KINDS.items() if row['send'] and k not in follow_ups.CHANNEL_KINDS},
                         {'x.dm', 'x.mention', 'docs.comment', 'docs.mention', 'docs.suggestion'})
        self.assertEqual(tuple(kinds.SENDS), __import__('activity').SEND_KINDS)
        self.assertEqual({k: s['name'] for k, s in kinds.SENDS.items()},
                         {k: v for k, v in __import__('activity_log').MESSAGE_KINDS.items() if k in kinds.SENDS})
        self.assertEqual(tuple(k for k, s in kinds.SENDS.items() if s['text_only']), next_actions.TEXT_KINDS)
        # The send lists that ask the registry now hold what they spelled out before it (PR 2 moved them)
        every = ('email', 'linkedin', 'slack', 'x', 'whatsapp', 'telegram', 'signal', 'intercom', 'doc_reply')
        self.assertEqual(kinds.SEND, every)
        self.assertEqual(kinds.TEXT_ONLY, every[1:])
        self.assertEqual(kinds.TO_PERSON, every[:-1])
        self.assertEqual(kinds.SEND_NOW, ('email', 'linkedin', 'slack', 'x'))
        self.assertEqual(set(next_actions.SEND_KINDS), {*every, 'email_demo'})
        self.assertEqual(set(__import__('talk_live').SEND_KINDS), {*every, 'doc_write'})
        from machine.app import handled_check
        from machine.delivery import push
        self.assertEqual(set(push.NUDGE_KINDS), {*every[:-1], 'handoff'})
        self.assertEqual(handled_check.REACHES, push.NUDGE_KINDS)
        for row in kinds.SENDS.values():
            self.assertEqual(set(row), {'name', 'text_only', 'to_person', 'send_now'})
        # The names that ask the registry now say what they spelled out before it (PR 3 moved them)
        self.assertEqual(cards.SOURCE_KIND, {
            'gmail.message': 'email', 'calendar.event': 'calendar', 'slack.message': 'Slack', 'teams.message': 'Teams',
            'salesflare.email': 'CRM email', 'salesflare.meeting': 'CRM meeting', 'android.notification': 'phone',
            'whatsapp.message': 'WhatsApp', 'telegram.message': 'Telegram', 'signal.message': 'Signal',
            'gateway.alert': 'The Machine', 'machine.system_log': 'The Machine', 'machine.fault': 'The Machine',
            'meeting.notes': 'meeting notes', 'meeting.transcript': 'transcript', 'fleet.request': 'Fleet', 'fleet.email': 'email',
            'owner.card': 'note', 'fleet.message': 'message', 'fleet.intercom': 'Intercom'})
        self.assertEqual(graph.VIA, {
            'linkedin.message': 'LinkedIn', 'gmail.message': 'email', 'salesflare.email': 'email', 'calendar.event': 'calendar',
            'slack.message': 'Slack', 'teams.message': 'Teams', 'whatsapp.message': 'WhatsApp', 'telegram.message': 'Telegram',
            'signal.message': 'Signal', 'x.dm': 'X', 'x.mention': 'X', 'intercom.conversation': 'Intercom', 'github.notification': 'GitHub'})
        self.assertEqual(__import__('activity_log').MESSAGE_KINDS, {
            'email': 'Email', 'email_demo': 'Email', 'linkedin': 'LinkedIn', 'slack': 'Slack', 'x': 'X', 'whatsapp': 'WhatsApp',
            'telegram': 'Telegram', 'signal': 'Signal', 'intercom': 'Intercom', 'doc_reply': 'Docs'})
        # every connector kind is here, with its connector's view
        from machine.sources.connectors import load_connector
        for path in sorted((ROOT / 'connectors').glob('*.py')):
            plugin = load_connector(path.stem)
            for kind in getattr(plugin, 'KINDS', None) or {}:
                with self.subTest(connector=path.stem, kind=kind):
                    self.assertIn(kind, kinds.KINDS)
                    self.assertEqual(kinds.KINDS[kind]['service'], path.stem)

    def test_the_messenger_kinds_are_the_viewers(self):
        """events-message.js THREAD_IM names them by their source line's name."""
        js = (ROOT / 'dashboard' / 'events-message.js').read_text(encoding='utf-8')
        names_ = set(re.findall(r"'([^']+)'", re.search(r'const THREAD_IM=new Set\(\[([^\]]*)\]\)', js).group(1)))
        self.assertEqual({row['name'] for row in kinds.KINDS.values() if row['messenger']}, names_)

    def test_kinds_is_a_leaf(self):
        tree = ast.parse((ROOT / KINDS_FILE).read_text(encoding='utf-8'))
        self.assertFalse([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))], 'machine/kinds.py imports nothing')


class Page(unittest.TestCase):
    def test_the_page_carries_the_registry_as_json(self):
        for page in (dashboard_parts.assemble(ROOT), dashboard_parts.assemble_split(ROOT)[0]):
            self.assertNotIn(dashboard_parts.KINDS_MARK, page)
            data = re.search(r'<script id="source-kinds" type="application/json">(.*?)</script>', page, re.S).group(1)
            self.assertEqual(json.loads(data), json.loads(json.dumps({'kinds': kinds.KINDS, 'sends': kinds.SENDS})))

    def test_another_checkouts_page_gets_its_own_kinds(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            (tmp / 'machine').mkdir()
            (tmp / 'dashboard').mkdir()
            page = tmp / 'page.html'
            page.write_text('<script id="source-kinds" type="application/json">__SOURCE_KINDS__</script>\n')
            self.assertIn('"gmail.message"', dashboard_parts.assemble(page=page), 'a copy of the page alone: these kinds')
            (tmp / 'machine' / 'kinds.py').write_text("KINDS = {'a.b': {'name': '</script>'}}\nSENDS = {}\n")
            page = dashboard_parts.assemble(page=page)
            self.assertIn('"a.b"', page)
            self.assertEqual(page.count('</script>'), 1, 'a name never ends the script element')


class Guard(unittest.TestCase):
    def test_no_new_hand_written_kind_lists(self):
        found = kind_lists()
        for name in sorted(set(found) | set(KIND_LISTS)):
            with self.subTest(name):
                have, allowed = len(found.get(name, ())), KIND_LISTS.get(name, 0)
                self.assertLessEqual(have, allowed, f'{name} spells out {have} lists of kinds ({allowed} allowed): '
                                     f'ask machine/kinds.py instead (code moved here from another file: move its count in '
                                     f'KIND_LISTS with it). Found: {found.get(name)}')
                self.assertGreaterEqual(have, allowed, f'{name} has {have} lists of kinds now: lower its count in '
                                        'KIND_LISTS to that')

    def test_the_guard_finds_lists_of_kinds(self):
        found = python_kind_lists(
            "A = ('gmail.message', 'slack.message')\n"
            "B = {'whatsapp.message': 'WhatsApp', 'telegram.message': 'Telegram'}\n"
            "C = ('email', 'linkedin', 'slack')\n"
            "db.execute(\"SELECT 1 FROM events WHERE kind IN ('gmail.message','outlook.message')\")\n"
            "ok = ('gmail.message',), ('gmail.com', 'outlook.com'), ('slack', 'whatsapp', 'telegram'), kinds.of(family='mail')\n"
            "D = {'gmail': 'Gmail', 'slack': 'Slack', 'whatsapp': 'WhatsApp', 'x': 'X'}\n")
        self.assertEqual([line for line, _ in found], [1, 2, 3, 4], found)
        js = js_kind_lists("const A=['whatsapp.message','linkedin.message'].includes(k);\n"
                           "const B={'gmail.message':'Email','slack.message':'Slack'};\n"
                           "const C={email:'Send',linkedin:'Send',slack:'Send'};\n"
                           "const ok=['gmail.message'],m={gmail:'Gmail',slack:'Slack',x:'X'};\n")
        self.assertEqual([line for line, _ in js], [1, 2, 3], js)


if __name__ == '__main__':
    if '--counts' in sys.argv:
        for name, found in kind_lists().items():
            print(f'    {name!r}: {len(found)},')
    else:
        unittest.main()
