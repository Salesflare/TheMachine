"""machine/graph/chat_proof.py: a person in a one-to-one chat and the address that chat shows is theirs. They book from
the link the owner sent there, or write their address: one person, with why and Undo. Less than that is a question, and
somebody else with the same first name is never joined."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('chat_proof_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph = a.graph
import ews_calendar  # noqa: E402
import ical  # noqa: E402
import meeting_prep  # noqa: E402
import ms_graph  # noqa: E402
import person_summary  # noqa: E402
import shared_graph  # noqa: E402
from machine.sources.calendar import calendar_event  # noqa: E402

NOW = dt.datetime(2026, 11, 9, 12, tzinfo=dt.timezone.utc)
ME = {'email': 'sam@acme.example', 'responseStatus': 'accepted', 'self': True}
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.example'}, {'id': 'cal', 'email': 'sam@acme.example', 'service': 'calendar'},
                       {'id': 'li', 'service': 'linkedin', 'email': 'LinkedIn'}, {'id': 'wa', 'service': 'whatsapp', 'email': 'Personal WhatsApp'}]}
SHORT = 'https://acme.link/talk'                      # redirects to the booking page: the app never opens it
TOOL = 'Reschedule: https://book.youcanbook.me/r/1'   # what the booking tool writes on the meeting
ROBIN, MAIL = 'li:c1', 'email:robin@lumio.example'
counter = iter(range(1, 10**6))


def at(hours_ago):
    return (NOW - dt.timedelta(hours=hours_ago)).isoformat()


def said(hours_ago, text, mine=False, conv='c1', name='Robin Vale', headline=None):
    n = next(counter)
    return {'account_id': 'li', 'source_id': f'l{n}', 'kind': 'linkedin.message', 'occurred_at': at(hours_ago), 'title': name, 'body': text, 'deleted': False,
            'metadata': {'conversation_id': conv, 'chat_name': name, 'from_me': mine, 'from': 'You' if mine else name, 'headline': headline, 'group': False}}


def wrote(hours_ago, text, mine=False, phone='00000000031', name='Robin Vale'):
    n = next(counter)
    return {'account_id': 'wa', 'source_id': f'w{n}', 'kind': 'whatsapp.message', 'occurred_at': at(hours_ago), 'title': name, 'body': text, 'deleted': False,
            'metadata': {'chat_id': phone + '@s.whatsapp.net', 'chat_name': name, 'from_me': mine, 'from': name, 'sender_id': ('00000000001' if mine else phone) + '@s.whatsapp.net'}}


def mail(hours_ago, sender, to, labels=('INBOX',)):
    n = next(counter)
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': at(hours_ago), 'title': f'Mail {n}', 'body': 'Hello', 'deleted': False,
            'metadata': {'from': sender, 'to': to, 'cc': '', 'labels': list(labels), 'message-id': f'<{n}@x>', 'thread_id': f't{n}'}}


def booked(hours_ago, *guests, body=TOOL, created=True, **more):
    """A meeting put on the calendar hours_ago, for two days from now."""
    n = next(counter)
    raw = {'id': f'e{n}', 'summary': 'Call', 'description': body, 'status': 'confirmed', 'updated': at(hours_ago),
           'start': {'dateTime': at(-48)}, 'end': {'dateTime': at(-49)}, 'organizer': {'email': ME['email'], 'self': True},
           'attendees': [ME, *({'email': g, 'responseStatus': 'accepted'} for g in guests)], **({'created': at(hours_ago)} if created else {}), **more}
    return calendar_event({'id': 'cal', 'email': ME['email']}, raw, 'UTC')


CHAT = (said(30, 'I liked Lumio, how did you build it?', mine=True), said(29, 'Thanks! With two friends.'), said(27, 'Shall we have a call?'))
LINK = said(26, f'Sure: {SHORT}', mine=True)


class ChatProof(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.config = CONFIG
        clock = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        clock.start()
        self.addCleanup(clock.stop)

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])

    def build(self):
        with self.store.connect() as db:
            db.isolation_level = None
            return graph.build(db, {**self.config, 'embeddings': {'model': 'test', 'dims': 4}}, NOW.isoformat())

    def people(self):
        with self.store.connect() as db:
            return {r['id']: json.loads(r['info']) for r in db.execute("SELECT id,info FROM graph_nodes WHERE kind='person'")}

    def asked(self):
        with self.store.connect() as db:
            return {(r['a'], r['b']): r['why'] for r in db.execute('SELECT a,b,why FROM graph_same')}

    def together(self, chat=ROBIN, address=MAIL):
        return any({chat, address} <= set(p['identifiers']) for p in self.people().values())

    def outcome(self, *events, chat=ROBIN, address=MAIL):
        """'joined', 'asked' or None, for a chat and an address."""
        self.add(*events, mail(25.7, 'Sam <sam@acme.example>', address.removeprefix('email:'), ('SENT',)))  # the confirmation
        self.build()
        if self.together(chat, address):
            return 'joined'
        return 'asked' if tuple(sorted((chat, address))) in self.asked() else None

    # Booked from the link in their chat

    def test_the_one_who_books_from_the_link_in_their_chat_is_one_person_with_why_and_undo(self):
        self.assertEqual(self.outcome(*CHAT, LINK, booked(25.8, 'robin@lumio.example')), 'joined')
        with self.store.connect() as db:
            (joined,) = graph.detail(db, MAIL)['joined']
        self.assertEqual((joined['why'], {joined['a'], joined['b']}), ('booked from the link in their chat', {ROBIN, MAIL}))
        with self.store.connect() as db:
            graph.merge(db, MAIL, ROBIN, False, NOW.isoformat(), 'owner')  # Undo
        for _ in range(2):
            self.build()
            self.assertFalse(self.together())
            self.assertEqual(self.asked(), {})  # nor asked again

    def test_a_link_the_app_knows_needs_no_mark_on_the_meeting(self):
        self.config = {**CONFIG, 'booking_links': {'call': 'https://www.acme.link/talk/'}}
        self.assertEqual(self.outcome(*CHAT, LINK, booked(25.8, 'robin@lumio.example', body='')), 'joined')

    def test_the_tools_own_link_needs_no_mark_either(self):
        self.assertEqual(self.outcome(*CHAT, said(26, 'https://calendly.com/sam-acme/30min', mine=True), booked(25.8, 'robin@lumio.example', body='')), 'joined')

    def test_a_link_to_something_else_is_no_booking_link(self):
        for link in (SHORT, 'https://evilcalendly.com/sam', 'https://calendly.com.evil.example/sam'):
            self.assertNotEqual(self.outcome(*CHAT, said(26, link, mine=True), booked(25.8, 'robin@lumio.example', body='')), 'joined', link)

    def test_before_the_calendar_says_when_it_was_made_the_confirmation_mail_does(self):
        self.assertEqual(self.outcome(*CHAT, LINK, booked(25.7, 'robin@lumio.example', created=False)), 'joined')

    def test_the_surname_in_the_address_is_as_good_as_the_company(self):
        self.assertEqual(self.outcome(said(27, 'Shall we talk?'), LINK, booked(25.8, 'robin.vale@mail.example'), address='email:robin.vale@mail.example'), 'joined')

    def test_the_company_in_their_headline_counts(self):
        self.assertEqual(self.outcome(said(27, 'Shall we talk?', headline='Founder at Lumio'), LINK, booked(25.8, 'robin@lumio.example')), 'joined')

    def test_the_briefing_reads_the_chat(self):
        self.assertEqual(self.outcome(*CHAT, LINK, meeting := booked(25.8, 'robin@lumio.example')), 'joined')
        with self.store.connect() as db:
            found = self.evidence(db, meeting)
        self.assertIn('how did you build it', json.dumps(found, default=str))

    def evidence(self, db, meeting, side='work', sides=None):
        row = db.execute('SELECT id FROM events WHERE source_id=?', (meeting['source_id'],)).fetchone()
        return meeting_prep.evidence(db, {'id': row[0], 'title': 'Call', 'account_id': 'cal', 'meta': meeting['metadata'], 'body': '', 'key': 'k',
                                          'start': dt.datetime.fromisoformat(at(-48)), 'guests': [{'email': 'robin@lumio.example', 'name': ''}]},
                                     side, sides or {'cal': 'work', 'work': 'work', 'li': 'work'}, {ME['email']}, {'acme.example'}, NOW, ('pending',), lambda *_: True,
                                     graph.resolve, person_summary.prep_lines, graph.excerpt)

    # Not enough: a question, or nothing

    def test_only_the_first_name_after_a_link_is_a_question(self):
        self.assertEqual(self.outcome(said(27, 'Shall we talk?'), LINK, booked(25.8, 'robin@lumio.example')), 'asked')
        self.assertEqual(list(self.asked().values()), ['A meeting made from their chat'])

    def test_a_call_agreed_in_a_chat_without_a_link_is_a_question_when_the_company_agrees(self):
        self.assertEqual(self.outcome(*CHAT, said(26, 'Tuesday at 12 then', mine=True), booked(25.8, 'robin@lumio.example', body='')), 'asked')

    def test_and_nothing_when_only_the_first_name_does(self):
        self.assertIsNone(self.outcome(said(27, 'Tuesday?'), said(26, 'Tuesday at 12 then', mine=True), booked(25.8, 'robin@lumio.example', body='')))

    def test_a_booking_long_after_the_link_is_nothing(self):
        self.assertIsNone(self.outcome(said(27 + 24 * 9, 'Lumio'), said(26 + 24 * 9, SHORT, mine=True), booked(25, 'robin@lumio.example')))

    def test_a_link_they_sent_is_not_the_owners(self):
        self.assertNotEqual(self.outcome(said(27, f'Lumio: {SHORT}'), booked(25.8, 'robin@lumio.example')), 'joined')

    # Somebody else

    def test_two_people_with_the_same_first_name_are_never_joined(self):
        other = (said(28, 'Is Lumio yours?', mine=True, conv='c2', name='Robin Stone'), said(27.5, 'No', conv='c2', name='Robin Stone'),
                 said(26.5, SHORT, mine=True, conv='c2', name='Robin Stone'))
        self.assertEqual(self.outcome(*CHAT, LINK, *other, booked(25.8, 'robin@lumio.example')), 'asked')
        self.assertFalse(self.together('li:c2'))

    def test_another_one_of_that_name_in_the_mail_those_days_makes_it_a_question(self):
        self.assertEqual(self.outcome(*CHAT, LINK, mail(28, 'Robin <robin1@gmail.com>', 'sam@acme.example'), booked(25.8, 'robin@lumio.example')), 'asked')

    def test_another_one_at_another_company_is_not_who_booked(self):
        self.assertEqual(self.outcome(*CHAT, LINK, mail(28, 'Robin Stone <robin@other.example>', 'sam@acme.example'), booked(25.8, 'robin@lumio.example')), 'joined')

    def test_two_addresses_out_of_one_link_are_a_question(self):
        self.assertEqual(self.outcome(*CHAT, LINK, booked(25.8, 'robin@lumio.example'), booked(25.5, 'robin@shop.example')), 'asked')

    def test_a_colleague_booking_for_them_or_with_the_link_passed_on_stays_apart(self):
        self.assertIsNone(self.outcome(*CHAT, LINK, booked(25.8, 'noor@lumio.example'), address='email:noor@lumio.example'))

    def test_a_colleagues_address_under_their_name_stays_apart(self):
        guest = booked(25.8)
        guest['metadata']['attendees'].append({'email': 'noor@lumio.example', 'displayName': 'Robin', 'responseStatus': 'accepted'})
        self.assertIsNone(self.outcome(*CHAT, said(25, 'and Noor will join'), LINK, mail(40, 'Noor <noor@lumio.example>', 'sam@acme.example'), guest, address='email:noor@lumio.example'))

    def test_another_surname_in_the_address_or_on_the_booking_stays_apart(self):
        for address in ('robin.stone@lumio.example', 'robinstone@lumio.example', 'robins@lumio.example', 'robina@lumio.example'):
            self.assertIsNone(self.outcome(*CHAT, LINK, booked(25.8, address), address='email:' + address), address)
        guest = booked(25.8)
        guest['metadata']['attendees'].append({'email': 'robin@lumio.example', 'displayName': 'Robin Stone', 'responseStatus': 'accepted'})
        self.assertIsNone(self.outcome(guest))

    def test_a_shared_address_a_group_meeting_a_series_and_a_lookalike_say_nothing(self):
        self.assertIsNone(self.outcome(*CHAT, LINK, booked(25.8, 'robin@lumio.example', 'noor@lumio.example'),
                                       booked(25.8, 'robin@lumio.example', recurringEventId='s1')))
        self.assertIsNone(self.outcome(booked(25.8, 'info@lumio.example'), address='email:info@lumio.example'))

    def test_someone_known_at_another_company_is_only_asked_about(self):
        self.outcome(mail(200, 'Robin Vale <robin.vale@first.example>', 'sam@acme.example'), *CHAT, LINK, booked(25.8, 'robin@lumio.example'))
        self.assertFalse(self.together())
        self.assertIn((MAIL, 'email:robin.vale@first.example') if MAIL < 'email:robin.vale@first.example' else ('email:robin.vale@first.example', MAIL), self.asked())

    def test_a_group_chat_is_nobodys_own(self):
        group = [{**e, 'metadata': {**e['metadata'], 'group': True, 'chat_name': 'Founders'}} for e in (*CHAT, LINK)]
        self.assertIsNone(self.outcome(*group, booked(25.8, 'robin@lumio.example')))

    # An address written in a chat

    def test_the_address_they_wrote_in_their_chat_is_theirs(self):
        self.assertEqual(self.outcome(said(27, 'Mail me at robin@lumio.example please')), 'joined')
        with self.store.connect() as db:
            self.assertEqual(graph.detail(db, MAIL)['joined'][0]['why'], 'they wrote this address in their chat')

    def test_one_the_owner_wrote_is_a_question(self):
        self.assertEqual(self.outcome(said(28, 'Hi'), said(27, 'Is robin@lumio.example right?', mine=True)), 'asked')
        self.assertEqual(list(self.asked().values()), ['This address is in your chat'])

    def test_one_written_in_two_chats_or_for_someone_else_stays_apart(self):
        self.assertIsNone(self.outcome(said(27, 'Ask robin@lumio.example', conv='c2', name='Noor Blake'), said(27, 'Hi')))

    def test_one_written_in_the_chats_of_two_of_that_name_stays_apart(self):
        self.assertIsNone(self.outcome(said(27, 'robin@lumio.example'), said(26, 'robin@lumio.example', conv='c2', name='Robin Stone')))

    def test_one_read_off_a_picture_is_not_what_they_wrote(self):
        from whatsapp_images import MARK
        self.assertIsNone(self.outcome(wrote(27, f'{MARK}\nText in it:\nrobin@lumio.example'), chat='wa:00000000031'))

    # Their own sides

    def test_a_personal_chat_stays_personal_out_of_the_work_briefing_and_never_shared(self):
        chat = 'wa:00000000031'
        meeting = booked(25.8, 'robin@lumio.example')
        self.add(wrote(30, 'Lumio is at the beach party too'), wrote(26, SHORT, mine=True), meeting)
        self.build()
        self.assertTrue(self.together(chat))
        with self.store.connect() as db:
            self.assertNotIn('beach party', json.dumps(self.evidence(db, meeting, sides={'cal': 'work', 'work': 'work', 'wa': 'personal'}), default=str))
            self.assertEqual({r[0] for r in db.execute("SELECT account_id FROM events WHERE kind='whatsapp.message'")}, {'wa'})  # the account sharing goes by

    def test_keep_private_goes_with_them(self):
        self.add(*CHAT)
        self.build()
        with self.store.connect() as db:
            shared_graph.ensure(db)
            shared_graph.keep_private(db, ROBIN)
        self.assertEqual(self.outcome(LINK, booked(25.8, 'robin@lumio.example')), 'joined')
        with self.store.connect() as db:
            self.assertIn(MAIL, {r[0] for r in db.execute('SELECT node_id FROM share_private')})

    # When a meeting was put on the calendar

    def test_when_it_was_made_is_kept_beside_never_a_new_version(self):
        self.add(first := booked(25.8, 'robin@lumio.example', created=False))
        with self.store.connect() as db:
            before = tuple(db.execute('SELECT version,analyzed_version FROM events').fetchone())
        self.add({**first, 'metadata': {**first['metadata'], 'created': at(25.8)}})
        with self.store.connect() as db:
            row = db.execute('SELECT version,analyzed_version,metadata FROM events').fetchone()
        self.assertEqual((tuple(row)[:2], json.loads(row['metadata'])['created']), (before, at(25.8)))

    def test_every_calendar_says_when_it_was_made(self):
        ics = ('BEGIN:VCALENDAR\r\nBEGIN:VEVENT\r\nUID:1\r\nSUMMARY:Call\r\nCREATED:20261101T080000Z\r\nDTSTART:20261110T100000Z\r\n'
               'DTEND:20261110T110000Z\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n')
        self.assertIn('2026-11-01T08:00:00+00:00', json.dumps(ical.window_items([ics], NOW, NOW + dt.timedelta(days=9)), default=str))
        outlook = ms_graph.calendar_item({'id': 'x', 'createdDateTime': '2026-11-01T08:00:00Z', 'start': {'dateTime': '2026-11-10T10:00:00', 'timeZone': 'UTC'},
                                          'end': {'dateTime': '2026-11-10T11:00:00', 'timeZone': 'UTC'}}, ME['email'])
        self.assertEqual(outlook['created'], '2026-11-01T08:00:00Z')
        self.assertIn('item:DateTimeCreated', ews_calendar.FIELDS)


if __name__ == '__main__':
    unittest.main()
