"""Who a message went to reads as people for every kind of event, whatever way its source keeps `to`: a header, a list
(Teams), people ({name, email}) or such a list kept as text. Never brackets or quotes, and never a bare address when the
chat, a message or the Graph has the name (mail_senders.recipients, message_view.went_to). A new kind is covered by its
row in machine/kinds.py. Lines and messages stored before read right too. All names and data are made up."""
import json
import re
import tempfile
import unittest
from pathlib import Path

from connectors import teams
from machine.app import prep_reads
from machine.cards import source_line_shown
from machine.kinds import CHAT, KINDS
import machine.main as machine_main
from machine.sources.connectors import connector_services, load_connector
from machine.store import message_view
from machine.store.cards import source_kind, source_line
from machine.store.views import source_lines_shown
import mail_senders
import missed_work
import shared_graph

ROOT = Path(__file__).parent.parent
AT = '2026-11-23T09:00:00+00:00'
ADA = 'ada.lopes@client.example'
BO = 'bo.reyes@client.example'
KINDS_ALL = sorted(set(KINDS) | {k for s in connector_services() for k in (getattr(load_connector(s), 'KINDS', None) or {})})
LIST_TEXT = re.compile(r'''\[['"{]|['"}]\]|\['|\{'name''')
# the same one person in every shape a source may keep it in
ONE = {'header': ADA, 'list': [ADA], 'person': {'name': 'Ada Lopes', 'email': ADA}, 'people': [{'name': 'Ada Lopes', 'email': ADA}],
       'json': json.dumps([ADA]), 'json people': json.dumps([{'name': 'Ada Lopes', 'email': ADA}]), 'python text': str([ADA])}
TWO = {'header': f'{ADA}, {BO}', 'list': [ADA, BO], 'json': json.dumps([ADA, BO]), 'python text': str([ADA, BO])}


def row(kind, id=1, **meta):
    return {'id': id, 'account_id': 'a', 'kind': kind, 'occurred_at': AT, 'title': 'Plan', 'body': 'Hi', 'metadata': json.dumps(meta)}


def event(kind, n=1, **meta):
    return {'account_id': 'a', 'source_id': f'{kind}:{n}', 'kind': kind, 'occurred_at': AT, 'title': 'Plan', 'body': 'Hi', 'deleted': False,
            'metadata': meta}


def own(kind):
    return {'labels': ['SENT']} if kind == 'gmail.message' else {'from_me': True}


class Recipients(unittest.TestCase):
    def test_every_shape_gives_the_same_people(self):
        for shape, to in ONE.items():
            self.assertIn(mail_senders.recipients(to), ([ADA], [f'Ada Lopes <{ADA}>']), shape)
            self.assertEqual(mail_senders.header_address(to), ADA, shape)
            self.assertEqual([a for _, a in mail_senders.addresses(to)], [ADA], shape)
        for shape, to in TWO.items():
            self.assertEqual([a for _, a in mail_senders.addresses(to)], [ADA, BO], shape)
            self.assertEqual(', '.join(mail_senders.recipients(to)), f'{ADA}, {BO}', shape)
        self.assertEqual(mail_senders.recipients(str([ADA, "O'Hara <o@client.example>"])), [ADA, "O'Hara <o@client.example>"])
        self.assertEqual(mail_senders.recipients(str([ADA, BO])[:-8])[0], ADA)  # cut short
        self.assertEqual([a for _, a in mail_senders.addresses([[ADA], BO, None])], [ADA, BO])
        for nobody in (None, '', [], {}, '[]', ' ', [None, '']):
            self.assertEqual(mail_senders.to_text({'to': nobody}), '', repr(nobody))
        self.assertEqual([a for _, a in mail_senders.addresses('["' * 5000)], [])  # a header made to break a parser

    def test_a_header_stays_as_it_is(self):
        for header in (f'Ada Lopes <{ADA}>, {BO}', f'"Lopes, Ada" <{ADA}>', f'[Team] Ops <{ADA}>', 'undisclosed-recipients:;'):
            self.assertEqual(mail_senders.to_text({'to': header}), header)


class EveryKind(unittest.TestCase):
    """A new kind of event is checked by being in machine/kinds.py or a connector's KINDS."""

    def printed(self, kind, meta):
        """Every place that prints who a message went to, by name."""
        r = row(kind, **meta)
        message = {**r, 'metadata': meta}
        return {'source line': source_line([r]) or '', 'run brief': prep_reads.source_line(r), 'to_text': mail_senders.to_text(meta),
                'shared thread': shared_graph._message(message)['to'], 'went_to': message_view.went_to(kind, meta)}

    def test_no_kind_prints_a_list_as_text(self):
        for kind in KINDS_ALL:
            for shape, to in {**ONE, **{k + ' two': v for k, v in TWO.items()}}.items():
                for extra in ({}, {'chat_name': 'Ada Lopes', 'chat_kind': 'oneOnOne'}, {'chat_name': 'Launch room', 'chat_kind': 'group'}):
                    for mine in (own(kind), {'from': 'Cy Dale', 'from_email': BO}):
                        for where, text in self.printed(kind, {'to': to, **extra, **mine}).items():
                            self.assertNotRegex(text, LIST_TEXT, (kind, shape, where))
                            if text and where != 'run brief':
                                self.assertNotRegex(text, r'[\[\]{}]', (kind, shape, where))

    def test_a_chat_says_its_name_never_the_address_in_it(self):
        for kind in (k for k in KINDS_ALL if k in KINDS and KINDS[k]['family'] == CHAT and KINDS[k]['name'] and k != 'slack.message'):
            for shape, to in ONE.items():
                line = source_line([row(kind, to=to, from_me=True, chat_kind='oneOnOne', chat_name='Ada Lopes')])
                self.assertTrue(line.startswith(f'Source: {source_kind(kind)} to Ada Lopes · '), (kind, shape, line))
            line = source_line([row(kind, to=[ADA, BO], from_me=True, chat_kind='group', chat_name='Launch room')])
            self.assertTrue(line.startswith(f'Source: {source_kind(kind)} to Launch room · '), (kind, line))

    def test_an_unnamed_chat_says_who_is_in_it(self):
        for kind in (k for k in KINDS_ALL if k in KINDS and KINDS[k]['family'] == CHAT and KINDS[k]['via'] and k != 'slack.message'):
            for word in ('chat', 'group', 'conversation'):
                meta = {'from_me': True, 'chat_name': f"{KINDS[kind]['via']} {word}", 'to': [ADA, BO]}
                rows = [row(kind, **meta), row(kind, 2, **{'from': 'Ada Lopes', 'from_email': ADA})]
                self.assertTrue(source_line(rows).startswith(f'Source: {source_kind(kind)} to Ada Lopes, {BO} · '), source_line(rows))
        many = [f'p{n}@client.example' for n in range(5)]
        self.assertEqual(message_view.went_to('teams.message', {'to': many}), ', '.join(many[:3]) + ', +2')

    def test_mail_says_the_first_person(self):
        for kind in ('gmail.message', 'salesflare.email'):
            for shape, to in {'header': f'Ada Lopes <{ADA}>, {BO}', 'list': [f'Ada Lopes <{ADA}>', BO], 'comma': f'"Ada Lopes" <{ADA}>'}.items():
                line = source_line([row(kind, to=to, **own(kind))])
                self.assertTrue(line.startswith(f'Source: {source_kind(kind)} to Ada Lopes · '), (kind, shape, line))


class Teams(unittest.TestCase):
    ME, ADA_ID, BO_ID = 'u-me', 'u-ada', 'u-bo'
    MEMBERS = {'u-me': ('Robin Hale', 'robin@owner.example'), 'u-ada': ('Ada Lopes', ADA)}

    def message(self, sender, members=None, kind='oneOnOne', topic=''):
        members = members or self.MEMBERS
        chat = {'id': '19:x', 'kind': kind, 'name': teams.chat_name({'topic': topic}, members, self.ME), 'url': None}
        raw = {'id': '1', 'createdDateTime': AT, 'messageType': 'message', 'body': {'contentType': 'text', 'content': 'Hi'},
               'from': {'user': {'id': sender, 'displayName': members[sender][0]}}}
        return teams.message_event({'id': 'a'}, chat, raw, members, self.ME)

    def test_the_owners_own_message_names_the_other_person(self):
        e = self.message(self.ME)
        self.assertEqual(e['metadata']['to'], [ADA])  # what the Graph and sharing read stays as it was
        self.assertTrue(source_line([row('teams.message', **e['metadata'])]).startswith('Source: Teams to Ada Lopes · '))
        self.assertEqual(mail_senders.to_text(e['metadata']), f'Ada Lopes <{ADA}>')

    def test_a_group_by_its_topic_or_its_people(self):
        members = {**self.MEMBERS, 'u-bo': ('Bo Reyes', BO)}
        for topic, want in (('', 'Ada Lopes, Bo Reyes'), ('Launch', 'Launch')):
            e = self.message(self.ME, members, 'group', topic)
            self.assertTrue(source_line([row('teams.message', **e['metadata'])]).startswith(f'Source: Teams to {want} · '))

    def test_their_message_did_not_go_to_themselves(self):
        self.assertEqual(mail_senders.to_text(self.message(self.ADA_ID)['metadata']), '')
        e = self.message(self.ADA_ID, {**self.MEMBERS, 'u-bo': ('Bo Reyes', BO)}, 'group')
        self.assertEqual(mail_senders.to_text(e['metadata']), BO)


class Stored(unittest.TestCase):
    """What an older Machine stored, plain and sealed."""

    def both(self, check):
        for protect in (False, True):
            with self.subTest(sealed=protect), tempfile.TemporaryDirectory() as temp:
                check(machine_main.Store(Path(temp) / 'events.sqlite', protect=protect))

    def shown(self, store, *cards):
        with store.connect() as db:
            source_lines_shown(db, cards)
        return [c['source_line'] for c in cards]

    def test_a_stored_line_names_the_person(self):
        def check(store):
            store.commit_page('a', {}, [event('teams.message', 1, to=[ADA], from_me=True, chat_kind='oneOnOne', chat_name='Ada Lopes', chat_id='c1'),
                                        event('teams.message', 2, to=[ADA, BO], from_me=True, chat_kind='group', chat_name='Launch room', chat_id='c2'),
                                        event('gmail.message', 3, **{'from': 'Ada Lopes <ada@elsewhere.example>', 'to': 'robin@owner.example'})])
            with store.connect() as db:
                ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
            one, two, mail = ids['teams.message:1'], ids['teams.message:2'], ids['gmail.message:3']
            self.assertEqual(self.shown(
                store,
                {'source_line': f"Source: Teams to ['{ADA}'] · Mon, Nov 23 (+6 more)", 'event_ids': json.dumps([mail, one])},
                {'source_line': f"Source: Teams to ['{ADA}' · Mon, Nov 23", 'event_ids': json.dumps([two])},  # two people: cut at the comma
                {'source_line': f"Source: Teams to ['{ADA}'] · Mon, Nov 23", 'event_ids': json.dumps([mail])},  # its message is gone
                {'source_line': 'Source: email from [Team] Ops · Mon, Nov 23', 'event_ids': json.dumps([mail])}),
                ['Source: Teams to Ada Lopes · Mon, Nov 23 (+6 more)', 'Source: Teams to Launch room · Mon, Nov 23',
                 f'Source: Teams to {ADA} · Mon, Nov 23', 'Source: email from [Team] Ops · Mon, Nov 23'])
        self.both(check)

    def test_the_graphs_name_when_only_the_graph_has_it(self):
        def check(store):
            with store.connect() as db:
                for n, (name, address) in enumerate((('Ada Lopes', ADA), ('Bo Reyes', BO))):
                    db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person',?,1,1,?)",
                               ('email:' + address, name, json.dumps({'identifiers': ['email:' + address]})))
            self.assertEqual(self.shown(store, {'source_line': f"Source: Teams to ['{ADA}'] · Mon, Nov 23", 'event_ids': '[]'},
                                        {'source_line': f'Source: Teams to {ADA}, {BO}, +2 · Mon, Nov 23', 'event_ids': '[]'}),
                             ['Source: Teams to Ada Lopes · Mon, Nov 23', 'Source: Teams to Ada Lopes, Bo Reyes, +2 · Mon, Nov 23'])
        self.both(check)

    def test_without_the_graph_the_address_without_brackets(self):  # the Telegram message of a to-do
        self.assertEqual(source_line_shown(f"Source: Teams to ['{ADA}'] · Mon, Nov 23 (+6 more)"), f'Source: Teams to {ADA} · Mon, Nov 23 (+6 more)')

    def test_the_message_viewer_and_the_missed_work_check(self):
        def check(store):
            kinds = [k for k in KINDS_ALL if k in KINDS and KINDS[k]['view'] in ('email', 'chat')]
            store.commit_page('a', {}, [event(k, n, to=to, cc=to, **own(k)) for k in kinds for n, to in enumerate((*ONE.values(), *TWO.values()))])
            with store.connect() as db:
                ids = [r[0] for r in db.execute('SELECT id FROM events')]
                quoted = missed_work.views(db, [{'id': i} for i in ids])
            for o in store.event_views(ids):
                self.assertNotRegex(o['to'] + o['cc'], r'[\[\]{}]', o['source'])
                self.assertIn(ADA, o['to'], o['source'])
            for found in quoted.values():
                self.assertNotRegex(found['to'], r'[\[\]{}]')
        self.both(check)


# str() of a message's `to` or `cc` prints a list with its brackets. Read it with mail_senders.recipients, to_text or addresses.
PRINTS = re.compile(r'''str\(\s*[\w.\[\]'"]*\.get\(['"](?:to|cc)['"]\)|getaddresses\(\[str\(\w+\.get\(|metadata['"]?\]?\.get\(['"](?:to|cc)['"]\) or \'\'''')
NOT_MESSAGES = {'network.py', 'onboarding.py', 'routines_app.py'}  # a request's own "to": a member, a step, a state


class Guard(unittest.TestCase):
    def test_nothing_prints_a_messages_recipients_by_itself(self):
        found = [f'{p.relative_to(ROOT)}:{n}' for p in sorted(ROOT.rglob('*.py'))
                 if not {'tests', 'node_modules', 'evals', 'sandbox', 'scripts'} & set(p.relative_to(ROOT).parts) and p.name not in NOT_MESSAGES
                 for n, line in enumerate(p.read_text(encoding='utf-8').split('\n'), 1) if PRINTS.search(line)]
        self.assertEqual(found, [], 'a message\'s `to` may be a list: mail_senders.recipients, to_text or addresses read it')


if __name__ == '__main__':
    unittest.main()
