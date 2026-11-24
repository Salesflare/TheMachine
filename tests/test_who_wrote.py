"""Who wrote a mail, and whether it is the answer someone waits for: the address behind a From line, the owner's own
mail, and what closes a to-do that waits on one person. No live calls."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('who_wrote_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

import missed_work  # noqa: E402
from machine.sources import gmail  # noqa: E402
from machine.store import cards, message_view, promises  # noqa: E402
from machine.store.review import own_message  # noqa: E402
from machine.text import _address  # noqa: E402
from machine.web import handler  # noqa: E402

OWN = {'owner@example.com', 'owner@home.example'}


class Addresses(unittest.TestCase):
    def test_never_the_one_written_in_a_name_or_a_comment(self):
        for header in ('"owner@example.com via Docs" <share@docs.example>', 'owner@example.com via Docs <share@docs.example>',
                       "'owner@example.com' via Team <share@docs.example>", 'owner@example.com <share@docs.example>',
                       'Docs (owner@example.com) <share@docs.example>', '"Docs <owner@example.com>" <share@docs.example>',
                       'Docs <owner@example.com> <share@docs.example>', '<owner@example.com> Docs <share@docs.example>',
                       '"Docs (owner@example.com)" <share@docs.example> (owner@example.com)', '[owner@example.com] <share@docs.example>'):
            self.assertEqual(_address(header), 'share@docs.example', header)
            self.assertEqual(message_view._address(header), 'share@docs.example', header)
            self.assertFalse(own_message({'kind': 'gmail.message', 'metadata': {'from': header, 'labels': ['INBOX']}}, own=OWN))
            self.assertFalse(missed_work.mine({'kind': 'gmail.message'}, {'from': header}, OWN))
            self.assertFalse(handler.event_glance({'kind': 'gmail.message', 'body': '', 'metadata': {'from': header}}, [], OWN)['from_me'])
        # The Machine's own mailer by a name only: a review still reads it
        self.assertFalse(gmail.machine_notice('gmail.message', {'from': '"digest@themachine.computer" <x@y.example>', 'machine_notice': True}))
        self.assertTrue(gmail.machine_notice('gmail.message', {'from': 'The Machine <digest@themachine.computer>', 'machine_notice': True}))

    def test_every_usual_shape_still_reads(self):
        for header, address in {
                'ann@x.example': 'ann@x.example', 'Ann <Ann@X.example>': 'ann@x.example', '<ann@x.example>': 'ann@x.example',
                'Doe, Ann <ann@x.example>': 'ann@x.example', '"Doe, Ann" <ann@x.example>, bob@x.example': 'ann@x.example',
                'ann@x.example, Bob <bob@x.example>': 'ann@x.example', 'ann@x.example; bob@x.example': 'ann@x.example',
                'Ann <ann@x.example': 'ann@x.example', 'ann@x.example (Ann)': 'ann@x.example', 'Ann (ann@x.example)': 'ann@x.example',
                'Ann [Team] <ann@x.example>': 'ann@x.example', "O'Brien <o'brien@x.example>": "o'brien@x.example",
                'mailto:ann@x.example': 'ann@x.example', 'ann@x.example,': 'ann@x.example', 'Ann "Q" Doe <ann@x.example>': 'ann@x.example',
                'Ann "Q <ann@x.example>': 'ann@x.example', '32470000000@s.whatsapp.net': '32470000000@s.whatsapp.net',
                'Team: ann@x.example, bob@x.example;': 'ann@x.example', 'undisclosed-recipients:;': '', 'Ann (@ann)': '', 'A @ B': '', '': ''}.items():
            self.assertEqual(_address(header), address, header)
        self.assertEqual(_address(None), '')
        self.assertEqual(_address(['ann@x.example', 'bob@x.example']), 'ann@x.example')

    def test_a_program_sent_it_only_when_auto_submitted_says_so(self):
        sent_by = lambda value: gmail.list_headers({'auto-submitted': value}).get('auto_submitted', False)
        self.assertEqual([sent_by(v) for v in ('no', 'No; reason=x', '', 'auto-replied', 'auto-replied; owner=x')], [False, False, False, True, True])


class OwnMail(unittest.TestCase):
    def test_what_is_shown_counts_every_address_of_theirs_what_decides_only_sent_mail(self):
        mail = lambda sender, *labels: {'kind': 'gmail.message', 'metadata': {'from': sender, 'labels': list(labels)}}
        elsewhere, alias = mail('Owner <owner@home.example>', 'INBOX'), mail('Sales <sales@example.com>', 'SENT')
        self.assertFalse(own_message(elsewhere))  # a From can be made up
        self.assertTrue(own_message(elsewhere, own=OWN))
        self.assertTrue(own_message(alias))
        self.assertTrue(own_message(alias, own=OWN))
        self.assertFalse(own_message(mail('Ann <ann@x.example>', 'INBOX'), own=OWN))
        self.assertTrue(handler.event_glance({**elsewhere, 'body': ''}, [], OWN)['from_me'])


WATCH = {'kind': 'gmail.message', 'account_id': 'work', 'since': '2026-10-10T09:00:00+00:00', 'from': 'bob@x.example', 'thread_id': 't1'}


class Awaited(unittest.TestCase):
    def match(self, watch=WATCH, theirs=(), **meta):
        return cards.awaiting_match(watch, {'kind': 'gmail.message', 'metadata': {'from': 'Bob <bob@x.example>', 'thread_id': 't1', 'labels': ['INBOX'], **meta}}, (), theirs)

    def test_only_a_message_that_person_wrote(self):
        for watch in (WATCH, {**WATCH, 'delegated': True}, {**WATCH, 'promise': True}):
            self.assertTrue(self.match(watch))
            self.assertFalse(self.match(watch, auto_submitted=True))  # an out-of-office
            self.assertFalse(self.match(watch, precedence='bulk'))
            self.assertFalse(self.match(watch, **{'from': 'Carl <carl@y.example>'}))  # someone else in the thread
            self.assertFalse(self.match(watch, **{'from': '"bob@x.example via Docs" <share@docs.example>'}))  # a notice naming them
            self.assertFalse(self.match(watch, labels=['SENT']))
            self.assertTrue(self.match(watch, ('bob@x.example', 'bob@home.example'), **{'from': 'bob@home.example'}))  # another address of theirs
            self.assertTrue(self.match(watch, **{'from': 'Bob <bob+work@x.example>'}))
            # their own reply, passed on by a list they copied
            self.assertTrue(self.match(watch, precedence='list', list_id='<team.x.example>', **{'in-reply-to': '<1@x>'}))
            self.assertTrue(self.match(watch, precedence='list', list_id='<team.x.example>', original_from='Bob <bob@x.example>',
                                       **{'from': "'Bob' via Team <team@x.example>", 'in-reply-to': '<1@x>'}))
            self.assertFalse(self.match(watch, original_from='Bob <bob@x.example>', **{'from': 'Carl <carl@y.example>'}))
        self.assertTrue(self.match(thread_id='t9'))  # a follow-up: they wrote again anywhere
        self.assertFalse(self.match({**WATCH, 'delegated': True}, thread_id='t9'))
        self.assertTrue(self.match({**WATCH, 'delegated': True, 'reply_to': '<me@x>'}, thread_id='t9', **{'in-reply-to': '<me@x>'}))
        self.assertFalse(self.match({**WATCH, 'promise': True}, thread_id='t9'))


def mail(source_id, at, sender, title='Contract', thread='t1', labels=('INBOX',), to='owner@example.com', body='I will send it by Friday.', **meta):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': title, 'body': body, 'deleted': False,
            'metadata': {'from': sender, 'to': to, 'thread_id': thread, 'labels': list(labels), **meta}}


class Closing(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = [{'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Example'}]

    def status(self, sid):
        with self.store.connect() as db:
            self.store.settle_awaiting(db)
            return db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0]

    def person(self, *addresses):
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person','Sam',1,1,?)",
                       ('email:' + addresses[0], json.dumps({'identifiers': ['email:' + x for x in addresses]})))

    def test_a_follow_up_waits_for_them(self):
        self.store.commit_page('work', {}, [mail('p', '2026-10-10T09:00:00+00:00', 'Sam <sam@client.example>')])
        with patch_everywhere(a, 'now', return_value='2026-10-11T10:00:00+00:00'):
            sid = self.store.suggest('contract', 'Contract from Sam', 'Promised by Friday.', [1], awaiting=1, due='2099-10-20')['id']
        self.store.commit_page('work', {}, [mail('away', '2026-10-12T09:00:00+00:00', 'Sam <sam@client.example>', auto_submitted=True),
                                            mail('third', '2026-10-12T10:00:00+00:00', 'Carl <carl@other.example>')])
        self.assertEqual(self.status(sid), 'pending')
        self.person('sam@client.example', 'sam@home.example')
        self.store.commit_page('work', {}, [mail('home', '2026-10-13T09:00:00+00:00', 'Sam <sam@home.example>', thread='t5')])
        self.assertEqual(self.status(sid), 'completed')

    def test_an_answer_to_the_owners_question(self):
        self.person('ann@client.example', 'ann@home.example')
        cases = iter(range(100))

        def answered(*later, to=('ann@client.example',)):
            thread = f'case-{next(cases)}'
            self.store.commit_page('work', {}, [mail(f'{thread}-{i}', '2026-10-09T09:00:00+00:00', sender, thread=thread, **meta)
                                                for i, (sender, meta) in enumerate(later)])
            row = {'account_id': 'work', 'occurred_at': '2026-10-08T09:00:00+00:00', 'metadata': json.dumps({'thread_id': thread})}
            with self.store.connect() as db:
                return promises.someone_answered(db, row, list(to), {'owner@example.com'})
        self.assertFalse(answered())
        self.assertTrue(answered(('Ann <ann@client.example>', {})))
        self.assertTrue(answered(('Ann <ann@home.example>', {})))
        self.assertTrue(answered(('Bo <bo@client.example>', {})))  # a colleague of theirs, for them
        self.assertTrue(answered(('mailer-daemon@googlemail.com', {'auto_submitted': True})))  # it bounced: bounces.py tells
        self.assertTrue(answered(('Desk <support@client.example>', {}), to=('support+id42@client.example',)))
        self.assertFalse(answered(('Ann <ann@client.example>', {'auto_submitted': True})))
        self.assertFalse(answered(('"ann@client.example (Docs)" <share@docs.example>', {})))
        self.assertFalse(answered(('Carl <carl@other.example>', {})))
        self.assertFalse(answered(('Kim <kim@gmail.com>', {}), to=('lee@gmail.com',)))  # free mail is no company
        self.assertFalse(answered(('No reply <noreply@client.example>', {})))
        self.assertTrue(answered(('No reply <noreply@client.example>', {}), ('Ann <ann@client.example>', {})))

    def test_known_addresses_without_the_table(self):
        from machine.store import graph_identifiers
        with self.store.connect() as db:
            graph_identifiers.drop(db)
            self.assertEqual(graph_identifiers.known_addresses(db, 'Ann+news@X.example'), {'ann@x.example'})
            self.assertEqual(graph_identifiers.known_addresses(db, ''), set())


if __name__ == '__main__':
    unittest.main()
