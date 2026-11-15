"""Event notes from ticket mail (bookings.py, event_notes.py, NotesApp.trip_notes_step): a ticket's structured data read
at sync, one dated note per event under Events with every order for it, a band in Calendar, the to-do from the ticket
mail, cancellations, and the area of the mailbox. Made-up mail only; nothing is sent, no Gateway, no model."""
import base64
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
import i18n
import machine.main as machine_main
import machine.sources.gmail as machine_sources_gmail

import bookings  # noqa: E402
import note_pages  # noqa: E402

HOME = {'id': 'home', 'service': 'gmail', 'email': 'owner@example.com', 'boundary': 'personal'}
JOB = {'id': 'job', 'service': 'gmail', 'email': 'owner@acme.example', 'boundary': 'work:Acme'}


def ticket(name, start, end=None, code='TK-4411', status='Confirmed', seats=None, venue='Example Arena', town='Antwerp', seat=None):
    tickets = [{'@type': 'Ticket', 'ticketNumber': '0042', **({'ticketedSeat': {'@type': 'Seat', 'seatSection': 'B', 'seatNumber': seat}} if seat else {})},
               {'@type': 'Ticket', 'ticketNumber': '0043'}]
    return {'@context': 'http://schema.org', '@type': 'EventReservation', 'reservationNumber': code,
            'reservationStatus': 'http://schema.org/Reservation' + status, 'reservedTicket': tickets, **({'numSeats': seats} if seats else {}),
            'provider': {'@type': 'Organization', 'name': 'Example Tickets'},
            'reservationFor': {'@type': 'Event', 'name': name, 'startDate': start, **({'endDate': end} if end else {}),
                               'location': {'@type': 'Place', 'name': venue, 'address': {'@type': 'PostalAddress', 'addressLocality': town}}}}


def page(*things):
    return '<html><body><p>Your tickets</p><script type="application/ld+json">' + json.dumps(list(things)) + '</script></body></html>'


def message(source, *things, sent):
    html = base64.urlsafe_b64encode(page(*things).encode()).decode()
    heads = [{'name': 'From', 'value': 'Example Tickets <orders@tickets.example>'}, {'name': 'To', 'value': 'owner@example.com'},
             {'name': 'Subject', 'value': 'Your tickets'}]
    return {'id': source, 'threadId': source, 'labelIds': ['INBOX'], 'internalDate': str(int(sent.timestamp() * 1000)), 'snippet': 'Your tickets',
            'payload': {'headers': heads, 'mimeType': 'multipart/alternative', 'parts': [
                {'mimeType': 'text/plain', 'filename': '', 'body': {'data': base64.urlsafe_b64encode(b'Your tickets are attached.').decode()}},
                {'mimeType': 'text/html', 'filename': '', 'body': {'data': html}}]}}


CONCERT = ticket('Northern Lights Live', '2026-12-12T20:00:00+01:00', seats=2, seat='14')


class Tickets(unittest.TestCase):
    def test_a_ticket_gives_a_short_flat_row(self):
        self.assertEqual(bookings.read([page(CONCERT)]), [{
            'type': 'event', 'code': 'TK-4411', 'status': 'confirmed', 'start': '2026-12-12T20:00', 'name': 'Northern Lights Live',
            'where': 'Example Arena, Antwerp', 'by': 'Example Tickets', 'guests': '2', 'seat': 'B 14', 'ticket': '0042'}])
        self.assertEqual(bookings.read([page({**CONCERT, 'reservationFor': {**CONCERT['reservationFor'], 'name': ''}})]), [], 'no name, no event')
        self.assertEqual(bookings.read([page({**CONCERT, 'reservationFor': {**CONCERT['reservationFor'], 'startDate': ''}})]), [], 'no day, no event')


class EventNotes(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite', protect=True)
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [HOME, JOB]}
        self.n = 0

    def mail(self, *things, day=1, account=HOME):
        self.n += 1
        event = machine_sources_gmail.message_event(account, message(f'm{self.n}', *things, sent=dt.datetime(2026, 11, day, 9, 0, tzinfo=dt.timezone.utc)))
        self.store.commit_page(account['id'], None, [event], record_sync=False)
        with self.store.connect() as db:
            return db.execute('SELECT max(id) FROM events').fetchone()[0]

    def sync(self):
        self.app.event_notes_at = float('-inf')  # an hour went by
        self.app.trip_notes_step()
        with self.store.connect() as db:
            return {x['name']: self.app.note_page(x['id']) for x in note_pages.listing(db, '2026-11-14') if x['kind'] == 'event'}

    def test_every_order_for_one_event_is_one_dated_note_under_events(self):
        self.mail(CONCERT)
        self.mail(ticket('Northern Lights Live', '2026-12-12T20:00:00+01:00', code='TK-5520'), day=3)
        self.mail(ticket('Harbor Sound Festival', '2027-07-09T12:00:00+02:00', '2027-07-11T23:00:00+02:00', code='HS-77', venue='Harbor Park', town='Ghent'), day=4)
        events = self.sync()
        self.assertEqual(sorted(events), ['Harbor Sound Festival', 'Northern Lights Live'])
        concert = events['Northern Lights Live']
        self.assertEqual((concert['starts'], concert['ends'], [x['name'] for x in concert['path']]), ('2026-12-12', '2026-12-12', ['Events']))
        self.assertCountEqual([x['text'] for x in concert['lines']], ['At Example Arena, Antwerp, 2 tickets, booking TK-4411, seat B 14, ticket 0042',
                                                                      'At Example Arena, Antwerp, booking TK-5520, ticket 0042'])
        self.assertEqual({x['source']['from'] for x in concert['lines']}, {'Example Tickets'}, 'each line says who the tickets came from')
        # a plural entry: languages with more count forms (Russian) get them, and one reads "1 ticket"
        self.assertEqual([i18n.t('{} tickets (to an event)', n, lang='en') for n in (1, 2)], ['1 ticket', '2 tickets'])
        festival = events['Harbor Sound Festival']
        self.assertEqual([(x['at'], x['data']['until'], x['text']) for x in festival['lines']],
                         [('2027-07-09T12:00', '2027-07-11T23:00', 'At Harbor Park, Ghent, booking HS-77, ticket 0042')], 'one line, its date to the end')
        self.assertNotIn('data', concert['lines'][0], 'an evening has no end day')
        self.assertEqual((festival['starts'], festival['ends'], festival['area']), ('2027-07-09', '2027-07-11', 'personal'))
        with self.store.connect() as db:
            self.assertEqual([x for x in note_pages.listing(db, '2026-11-14') if x['kind'] == 'trip'], [], 'tickets make no trip')
        week = self.app.calendar_notes('2026-12-07T00:00:00+01:00', '2026-12-14T00:00:00+01:00')
        self.assertEqual([(x['kind'], x['name']) for x in week], [('event', 'Northern Lights Live')])

    def test_a_todo_from_the_ticket_mail_opens_from_its_line_and_a_cancellation_takes_the_event_out(self):
        mail = self.mail(CONCERT)
        self.assertNotIn('todo', self.sync()['Northern Lights Live']['lines'][0])
        todo = self.store.suggest('tickets', 'Pay for the concert tickets', 'Before Friday.', [mail])['id']
        self.assertEqual(self.sync()['Northern Lights Live']['lines'][0]['todo'], todo, 'a to-do made later still opens from the line')
        self.mail({**CONCERT, 'reservationStatus': 'http://schema.org/ReservationCancelled'}, day=5)
        self.assertEqual(self.sync(), {})

    def test_a_conference_booked_on_the_work_mailbox_is_work(self):
        self.mail(ticket('Example Dev Summit', '2027-03-04', '2027-03-05', code='DS-1', venue='Expo Hall', town='Lyon'), account=JOB)
        summit = self.sync()['Example Dev Summit']
        self.assertEqual(summit['area'], 'work:Acme')
        self.assertEqual([x['text'] for x in summit['lines']], ['At Expo Hall, Lyon, booking DS-1, ticket 0042'])


if __name__ == '__main__':
    unittest.main()
