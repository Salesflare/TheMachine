"""Trip notes from booking mail (bookings.py, trip_notes.py, NotesApp.trip_notes_step): a confirmation's structured data
read at sync, bookings grouped into one trip per journey, updates and cancellations, and the owner's edits that stay.
Made-up mail only; nothing is sent, no Gateway, no model."""
import base64
import datetime as dt
import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('trip_notes_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import bookings  # noqa: E402
import note_pages  # noqa: E402
import note_pages_app  # noqa: E402
import trip_notes  # noqa: E402

MAIL = {'id': 'home', 'service': 'gmail', 'email': 'owner@example.com', 'area': 'personal'}
AT = '2026-11-14T10:00:00+00:00'


def flight(number, code, dep, arr, when, until, status='Confirmed', seat=None):
    return {'@context': 'http://schema.org', '@type': 'FlightReservation', 'reservationNumber': code,
            'reservationStatus': 'http://schema.org/Reservation' + status, **({'airplaneSeat': seat} if seat else {}),
            'reservationFor': {'@type': 'Flight', 'flightNumber': number, 'airline': {'@type': 'Airline', 'name': 'Example Air', 'iataCode': 'EX'},
                               'departureAirport': {'@type': 'Airport', 'name': dep + ' Airport', 'iataCode': dep[:3].upper(), 'address': {'addressLocality': dep}},
                               'arrivalAirport': {'@type': 'Airport', 'name': arr + ' Airport', 'iataCode': arr[:3].upper(), 'address': {'addressLocality': arr}},
                               'departureTime': when, 'arrivalTime': until}}


def hotel(name, town, checkin, checkout, code='H-2231'):
    return {'@context': 'http://schema.org', '@type': 'LodgingReservation', 'reservationNumber': code,
            'reservationStatus': 'http://schema.org/ReservationConfirmed', 'checkinTime': checkin, 'checkoutTime': checkout,
            'reservationFor': {'@type': 'LodgingBusiness', 'name': name, 'address': {'@type': 'PostalAddress', 'addressLocality': town}}}


def train(number, dep, arr, when, until, code='TR8812'):
    return {'@context': 'http://schema.org', '@type': 'TrainReservation', 'reservationNumber': code,
            'reservedTicket': {'@type': 'Ticket', 'ticketNumber': '0042', 'ticketedSeat': {'@type': 'Seat', 'seatSection': '5', 'seatNumber': '61'}},
            'reservationFor': {'@type': 'TrainTrip', 'trainNumber': number, 'provider': {'@type': 'Organization', 'name': 'Example Rail'},
                               'departureStation': {'@type': 'TrainStation', 'name': dep}, 'arrivalStation': {'@type': 'TrainStation', 'name': arr},
                               'departureTime': when, 'arrivalTime': until}}


def page(*things):
    return '<html><body><p>Your booking</p><script type="application/ld+json">' + json.dumps(list(things)) + '</script></body></html>'


def message(source, *things, sent=None):
    html = base64.urlsafe_b64encode(page(*things).encode()).decode()
    heads = [{'name': 'From', 'value': 'Bookings <bookings@travel.example>'}, {'name': 'To', 'value': 'owner@example.com'},
             {'name': 'Subject', 'value': 'Your booking is confirmed'}]
    stamp = int((sent or dt.datetime(2026, 11, 1, 9, 0, tzinfo=dt.timezone.utc)).timestamp() * 1000)
    return {'id': source, 'threadId': source, 'labelIds': ['INBOX'], 'internalDate': str(stamp), 'snippet': 'Your booking',
            'payload': {'headers': heads, 'mimeType': 'multipart/alternative', 'parts': [
                {'mimeType': 'text/plain', 'filename': '', 'body': {'data': base64.urlsafe_b64encode(b'Your booking is confirmed.').decode()}},
                {'mimeType': 'text/html', 'filename': '', 'body': {'data': html}}]}}


OUT = flight('2084', 'K7PQ2M', 'Brussels', 'Lisbon', '2026-12-02T07:10:00+01:00', '2026-12-02T08:55:00+00:00', seat='14A')
BACK = flight('2087', 'K7PQ2M', 'Lisbon', 'Brussels', '2026-12-05T18:45:00+00:00', '2026-12-05T22:20:00+01:00')
STAY = hotel('Hotel Alfama Garden', 'Lisbon', '2026-12-02T15:00:00+00:00', '2026-12-05T11:00:00+00:00')


class Bookings(unittest.TestCase):
    def test_a_confirmation_gives_short_flat_rows_without_links(self):
        rows = bookings.read([page(OUT, STAY, {'@type': 'Restaurant', 'name': 'Not a booking'})])
        self.assertEqual(rows[0], {'type': 'flight', 'code': 'K7PQ2M', 'status': 'confirmed', 'start': '2026-12-02T07:10', 'end': '2026-12-02T08:55',
                                   'from': 'Brussels', 'to': 'Lisbon', 'number': 'EX 2084', 'by': 'Example Air', 'seat': '14A'})
        self.assertEqual(rows[1]['type'], 'hotel')
        self.assertEqual((rows[1]['name'], rows[1]['where'], rows[1]['start'], rows[1]['end']), ('Hotel Alfama Garden', 'Lisbon', '2026-12-02T15:00', '2026-12-05T11:00'))
        self.assertEqual(len(rows), 2)

    def test_nothing_is_guessed(self):
        self.assertEqual(bookings.read(['<p>Your flight EX 2084 leaves at 07:10</p>']), [])
        self.assertEqual(bookings.read(['<script type="application/ld+json">{not json</script>']), [])
        no_time = {**OUT, 'reservationFor': {**OUT['reservationFor'], 'departureTime': ''}}
        self.assertEqual(bookings.read([page(no_time)]), [])
        self.assertEqual(bookings.read([page({**OUT, 'reservationStatus': 'http://schema.org/ReservationCancelled'})])[0]['status'], 'canceled')

    def test_microdata_reads_like_json_ld(self):
        """Many airlines and hotels mark up their confirmations as microdata on the mail's own HTML, not as a JSON-LD
        block: loose HTML, values in content and datetime attributes or as text, a link for the status."""
        micro = ('<html><body><table><tr><td>'
                 '<div itemscope itemtype="http://schema.org/FlightReservation">'
                 '<meta itemprop="reservationNumber" content="K7PQ2M">'
                 '<link itemprop="reservationStatus" href="http://schema.org/ReservationConfirmed"/>'
                 '<div itemprop="reservationFor" itemscope itemtype="http://schema.org/Flight">'
                 '<span itemprop="flightNumber">2084</span>'
                 '<div itemprop="airline" itemscope itemtype="http://schema.org/Airline"><meta itemprop="name" content="Example Air"><meta itemprop="iataCode" content="EX"></div>'
                 '<div itemprop="departureAirport" itemscope itemtype="http://schema.org/Airport"><span itemprop="name">Brussels <b>Airport</b></span><meta itemprop="iataCode" content="BRU">'
                 '<div itemprop="address" itemscope itemtype="http://schema.org/PostalAddress"><meta itemprop="addressLocality" content="Brussels"></div></div>'
                 '<div itemprop="arrivalAirport" itemscope itemtype="http://schema.org/Airport"><meta itemprop="name" content="Lisbon Airport"><meta itemprop="iataCode" content="LIS"></div>'
                 '<time itemprop="departureTime" datetime="2026-12-02T07:10:00+01:00">2 Dec</time>'
                 '<meta itemprop="arrivalTime" content="2026-12-02T08:55:00+00:00">'
                 '</div><meta itemprop="airplaneSeat" content="14A"></div>'
                 '<p>Unclosed paragraph<td></table>'
                 '<div itemscope itemtype="https://schema.org/LodgingReservation"><meta itemprop="reservationNumber" content="H-2231">'
                 '<meta itemprop="checkinDate" content="2026-12-02"><meta itemprop="checkoutDate" content="2026-12-05">'
                 '<div itemprop="reservationFor" itemscope itemtype="http://schema.org/LodgingBusiness"><meta itemprop="name" content="Hotel Alfama Garden">'
                 '<div itemprop="address" itemscope itemtype="http://schema.org/PostalAddress"><meta itemprop="addressLocality" content="Lisbon"></div></div></div>'
                 '</body></html>')
        rows = bookings.read([micro])
        self.assertEqual(rows[0], {'type': 'flight', 'code': 'K7PQ2M', 'status': 'confirmed', 'start': '2026-12-02T07:10', 'end': '2026-12-02T08:55',
                                   'from': 'Brussels', 'to': 'Lisbon Airport', 'number': 'EX 2084', 'by': 'Example Air', 'seat': '14A'})
        self.assertEqual((rows[1]['type'], rows[1]['name'], rows[1]['where'], rows[1]['start'], rows[1]['end']),
                         ('hotel', 'Hotel Alfama Garden', 'Lisbon', '2026-12-02', '2026-12-05'))
        self.assertEqual(len(rows), 2)
        # the same reservation as JSON-LD and as microdata in one mail is one row
        self.assertEqual(len(bookings.read([micro.replace('</body>', '<script type="application/ld+json">' + json.dumps(STAY) + '</script></body>')])), 3)
        self.assertEqual(bookings.read([micro + micro]), rows)
        # nothing is guessed: a boarding pass whose time is only text, or no reservation type at all
        self.assertEqual(bookings.read([micro.replace('datetime="2026-12-02T07:10:00+01:00"', '')]), rows[1:])
        self.assertEqual(bookings.read(['<div itemscope itemtype="http://schema.org/Restaurant"><meta itemprop="name" content="x"></div>']), [])
        self.assertEqual(bookings.read(['<div itemscope itemtype="http://schema.org/FlightReservation"><div><span itemprop="x">']), [])

    def test_the_mail_source_keeps_them_in_the_sealed_metadata(self):
        event = a.message_event(MAIL, message('m1', OUT))
        self.assertEqual(event['metadata']['bookings'][0]['code'], 'K7PQ2M')
        self.assertNotIn('bookings', a.message_event(MAIL, {**message('m2', OUT), 'payload': {**message('m2', OUT)['payload'], 'parts': message('m2', OUT)['payload']['parts'][:1]}})['metadata'])


class TripNotes(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite', protect=True)
        self.n = 0

    def mail(self, *things, day=1):
        self.n += 1
        self.store.commit_page('home', None, [a.message_event(MAIL, message(f'm{self.n}', *things, sent=dt.datetime(2026, 11, day, 9, 0, tzinfo=dt.timezone.utc)))], record_sync=False)

    def sync(self):
        with self.store.connect() as db:
            trip_notes.collect(db)
            found, keep = trip_notes.drafts(db, [MAIL])
            note_pages.sync(db, 'trip', found, AT, keep)
            return [note_pages.page(db, x['id']) for x in note_pages.listing(db, '2026-11-14') if x['kind'] == 'trip']

    def test_flights_and_a_hotel_of_one_journey_are_one_trip_in_time_order(self):
        self.mail(OUT, BACK)
        self.mail(STAY, day=3)
        self.mail(train('9114', 'Brussels-Midi', 'London St Pancras', '2027-01-20T08:16:00+01:00', '2027-01-20T09:22:00+00:00'), day=4)
        trips = self.sync()
        self.assertEqual([(x['name'], x['starts'], x['ends']) for x in trips],
                         [('Lisbon', '2026-12-02', '2026-12-05'), ('London St Pancras', '2027-01-20', '2027-01-20')])
        lisbon = trips[0]
        self.assertEqual([x['text'] for x in lisbon['lines']], [
            'Flight EX 2084 Brussels to Lisbon, booking K7PQ2M, seat 14A',
            'Hotel Alfama Garden, 3 nights, booking H-2231',
            'Check out of Hotel Alfama Garden',
            'Flight EX 2087 Lisbon to Brussels, booking K7PQ2M'])
        self.assertTrue(all(x['event_id'] for x in lisbon['lines']))
        self.assertEqual([p['name'] for p in lisbon['path']], ['Trips'])
        self.assertEqual(trips[1]['lines'][0]['text'], 'Train 9114 Brussels-Midi to London St Pancras, booking TR8812, seat 5 61, ticket 0042')

    def test_a_trip_is_a_band_in_the_calendar_windows_it_touches(self):
        self.mail(OUT, BACK)
        self.sync()
        app = type('App', (note_pages_app.NotesApp,), {})()
        app.store = self.store
        week = app.calendar_notes('2026-11-30T00:00:00+01:00', '2026-12-07T00:00:00+01:00')
        self.assertEqual(week, [{'id': week[0]['id'], 'kind': 'trip', 'name': 'Lisbon', 'starts': '2026-12-02', 'ends': '2026-12-05'}])
        self.assertTrue(week[0]['id'].startswith('note:'))
        self.assertEqual(app.calendar_notes('2026-12-14T00:00:00+01:00', '2026-12-21T00:00:00+01:00'), [])
        self.assertEqual(app.calendar_notes('', ''), [])

    def test_a_return_home_days_later_joins_the_way_out(self):
        self.mail(flight('11', 'AB1', 'Brussels', 'Porto', '2026-12-10T07:00:00', '2026-12-10T08:30:00'))
        self.mail(flight('12', 'CD2', 'Porto', 'Brussels', '2026-12-17T19:00:00', '2026-12-17T22:30:00'), day=2)
        self.assertEqual([(x['name'], x['starts'], x['ends'], len(x['lines'])) for x in self.sync()], [('Porto', '2026-12-10', '2026-12-17', 2)])

    def test_a_change_replaces_the_booking_and_a_cancellation_takes_it_out(self):
        self.mail(OUT, BACK)
        self.mail({**OUT, 'airplaneSeat': '3C'}, day=2)
        trip = self.sync()[0]
        self.assertIn('seat 3C', trip['lines'][0]['text'])
        self.assertEqual(len(trip['lines']), 2)
        self.mail({**BACK, 'reservationStatus': 'http://schema.org/ReservationCancelled'}, day=3)
        self.assertEqual(len(self.sync()[0]['lines']), 1)
        self.mail({**OUT, 'reservationStatus': 'http://schema.org/ReservationCancelled'}, day=4)
        self.assertEqual(self.sync(), [])

    def test_the_owners_edits_stay_over_later_mail(self):
        self.mail(OUT, BACK)
        trip = self.sync()[0]
        with self.store.connect() as db:
            note_pages.edit(db, trip['id'], AT, title='Lisbon with the team')
            note_pages.line_edit(db, trip['lines'][0]['id'], 'Flight out, aisle seat asked', AT)
        self.mail(STAY, day=2)
        trip = self.sync()[0]
        self.assertEqual(trip['name'], 'Lisbon with the team')
        self.assertEqual(trip['lines'][0]['text'], 'Flight out, aisle seat asked')
        self.assertEqual(len(trip['lines']), 4)

    def test_bookings_are_sealed_at_rest_and_read_once(self):
        self.mail(OUT)
        self.sync()
        with self.store.connect() as db:
            self.assertEqual(trip_notes.collect(db), 0)  # the cursor moved on
        raw = sqlite3.connect(self.store.path)
        stored = raw.execute('SELECT rows FROM trip_bookings').fetchone()[0]
        raw.close()
        self.assertNotIn(b'K7PQ2M', stored if isinstance(stored, bytes) else stored.encode())


if __name__ == '__main__':
    unittest.main()
