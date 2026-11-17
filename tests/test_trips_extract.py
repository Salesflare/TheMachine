"""Trips from booking mail without structured data (bookings.looks_booked, extract_prompt, parse; trip_notes.queue,
pending, answered; TripsApp.trip_extract_step), and one journey as one trip: grouped by dates and connecting places,
every booking on it in time order, and only real gaps flagged. Made-up mail only; the model is a stand-in, nothing is
sent."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import machine.main as machine_main
from machine.text import email_body

import bookings  # noqa: E402
import event_notes  # noqa: E402
import note_pages  # noqa: E402
import trip_notes  # noqa: E402

MAIL = {'id': 'home', 'service': 'gmail', 'email': 'owner@example.com', 'area': 'personal'}
AT = '2026-11-14T10:00:00+00:00'

HOME_RENTAL = '''Your reservation is confirmed
Casa Lumen, Valmar
Check-in Sat, May 16, 2026 from 17:00
Checkout Sat, May 23, 2026 by 10:00
Reservation code HMXQ7741
Address: Carrer del Port 7, 09999 Valmar, Spain
Guests: 5'''
PARKING = '''Your booking at Skyline Park & Fly is confirmed.
Booking number 7F2C9A10
Booked from: Saturday 13 June 2026 - 14:00, Example Airport
Booked until: Saturday 23 May 2026 - 15:30, Example Airport
Address: Airport Road 10, 1000 Southport'''
NEWSLETTER = 'Last minute deals to Portavia! Book your flight now from EUR 49. Offer code SUMMER26 until 30 June 2026.'


def flight(number, dep, arr, start, end, code='K7PQ2M', **more):
    return {'type': 'flight', 'code': code, 'status': 'confirmed', 'start': start, 'end': end, 'from': dep, 'to': arr,
            'number': number, 'by': 'Example Air', **more}


class Looks(unittest.TestCase):
    def test_confirmations_without_structured_data_look_like_bookings_and_offers_dont(self):
        self.assertTrue(bookings.looks_booked('Reservation confirmed: Casa Lumen', 'Stays <stays@homes.example>', HOME_RENTAL))
        self.assertTrue(bookings.looks_booked('Reservering via Example Parking', 'Parking <info@parking.example>', PARKING))
        self.assertTrue(bookings.looks_booked('TKT48213 - Online aankoop', 'Rail <no-reply@rail.example>',
                                              'Bestelnummer: TKT48213\nVan : RIVERTON-WEST\nNaar : OAKDALE AIRPORT\nHeen: 13/06/2026'))
        self.assertFalse(bookings.looks_booked('Last minute deals to Portavia', 'Air <news@air.example>', NEWSLETTER))
        self.assertFalse(bookings.looks_booked('Booking.com – 4Q9Z1B is your verification code', 'b <noreply@booking.example>', 'Code 4Q9Z1B'))
        self.assertFalse(bookings.looks_booked('Your receipt from Example Stays', 'x <a@b.example>', HOME_RENTAL))
        self.assertFalse(bookings.looks_booked('Re: plans', 'Owner <owner@example.com>', HOME_RENTAL, own=['owner@example.com']))
        self.assertTrue(bookings.looks_booked('Fwd: Reservation confirmed', 'Owner <owner@example.com>', HOME_RENTAL, own=['owner@example.com']))

    def test_a_stub_text_part_gives_way_to_the_html(self):
        html_part = '<p>' + 'Your car is confirmed. Pick-up Portavia Airport, 13 June 2026 20:00. ' * 5 + '</p>'
        self.assertIn('Pick-up Portavia Airport', email_body('Your client does not support HTML emails.', [html_part]))
        stub = 'Beste klant,\nWe hebben de bevestiging in HTML-opmaak gestuurd. Klik hieronder om de online versie van deze e-mail te bekijken.'
        self.assertIn('Pick-up Portavia Airport', email_body(stub, [html_part]))


class Parse(unittest.TestCase):
    def test_the_answer_is_checked_field_by_field(self):
        reply = '```json\n' + json.dumps({
            '1': [{'type': 'hotel', 'status': 'confirmed', 'code': 'HMXQ7741', 'start': '2026-06-13T17:00', 'end': '2026-06-20T10:00',
                   'name': 'Casa Lumen', 'where': 'Valmar', 'address': 'Carrer del Port 7, 09999 Valmar', 'guests': 5, 'owner_on_it': 'yes',
                   'link': 'https://example.com/manage?token=x'},
                  {'type': 'spaceship', 'start': '2026-06-13'},
                  {'type': 'flight', 'start': 'soon', 'from': 'A', 'to': 'B'},
                  {'type': 'flight', 'start': '2026-06-13T17:20', 'from': 'Brussels', 'to': 'Portavia', 'owner_on_it': 'no'}],
            '2': [{'type': 'parking', 'status': 'CANCELED','code': '7F2C9A10'}],
            '9': [{'type': 'hotel', 'start': '2026-01-01', 'name': 'Not asked'}]}) + '\n```'
        found = bookings.parse(reply, ['1', '2', '3'])
        self.assertEqual(found['1'], [
            {'type': 'hotel', 'status': 'confirmed', 'code': 'HMXQ7741', 'start': '2026-06-13T17:00', 'end': '2026-06-20T10:00',
             'name': 'Casa Lumen', 'where': 'Valmar', 'address': 'Carrer del Port 7, 09999 Valmar', 'guests': '5', 'read': 'text'},
            {'type': 'flight', 'status': 'confirmed', 'start': '2026-06-13T17:20', 'from': 'Brussels', 'to': 'Portavia', 'others': 1, 'read': 'text'}])
        self.assertEqual(found['2'], [{'type': 'parking', 'status': 'canceled', 'code': '7F2C9A10', 'read': 'text'}])
        self.assertEqual(found['3'], [])
        self.assertNotIn('9', found)
        self.assertIsNone(bookings.parse('I could not read these.', ['1']))
        self.assertEqual(bookings.parse('{"MAIL 7": [{"type": "parking", "start": "2026-09-05T09:00", "where": "Southport", '
                                        '"address": "Avenue 10,, 1000 Southport"}]}', ['7'])['7'][0]['address'], 'Avenue 10, 1000 Southport')

    def test_the_prompt_carries_no_links_and_keeps_each_mail_short(self):
        text = bookings.extract_prompt([{'id': '1', 'title': 'Booking', 'sender': 's@x.example',
                                         'text': 'Manage: https://x.example/m?token=secret\n' + 'x' * 9000}], 'Alex Owner')
        self.assertNotIn('token=secret', text)
        self.assertIn('The owner is Alex Owner.', text)
        self.assertLess(len(text), 7000)


class Journey(unittest.TestCase):
    """A real-shaped journey, made up: a team flight out, the train to the airport, a holiday home, a rental car,
    airport parking, a tour, and the flight home on another airline, from two mailboxes, some with structured data and
    some read by the model."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite', protect=True)
        self.n = 0

    def mail(self, rows, day, account='home', read='markup'):
        self.n += 1
        with self.store.connect() as db:
            trip_notes.keep(db, 1000 + self.n, account, f'2026-03-{day:02d}T09:00:00+00:00', [{**r, **({'read': 'text'} if read == 'text' else {})} for r in rows])

    def trips(self, today='2026-05-01'):
        with self.store.connect() as db:
            found, keep = trip_notes.drafts(db, [MAIL, {'id': 'work', 'service': 'gmail', 'email': 'owner@work.example', 'boundary': 'work'}], today=today)
            note_pages.sync(db, 'trip', found, AT, keep)
            return found

    def journey(self):
        self.mail([flight('EX 3410', 'Brussels', 'Portavia', '2026-06-13T17:20', '2026-06-13T19:50', code='Q4TR7N', seat='12C')], 1, 'work', 'text')
        self.mail([{'type': 'train', 'status': 'confirmed', 'code': 'TKT48213', 'start': '2026-06-13', 'from': 'RIVERTON-WEST',
                    'to': 'BRUSSELS AIRPORT', 'by': 'Example Rail'}], 2, 'work', 'text')
        self.mail([{'type': 'hotel', 'status': 'confirmed', 'code': 'HMXQ7741', 'start': '2026-06-13T17:00', 'end': '2026-06-20T10:00',
                    'name': 'Casa Lumen', 'where': 'Valmar', 'address': 'Carrer del Port 7, 09999 Valmar'}], 3)
        self.mail([{'type': 'car', 'status': 'confirmed', 'code': '90210554', 'start': '2026-06-13T20:00', 'end': '2026-06-20T08:00',
                    'from': 'Portavia Airport', 'to': 'Portavia Airport', 'by': 'Example Cars'}], 4, 'work', 'text')
        self.mail([flight('EX 9120', 'Portavia', 'Bruxel', '2026-06-20T10:05', '2026-06-20T12:40', code='W8KD2P', by='Example Low')], 5, 'work')
        self.mail([{'type': 'event', 'status': 'confirmed', 'code': 'T-88', 'start': '2026-06-16T09:00', 'name': 'Coastal boat tour',
                    'where': 'Valmar marina'}], 6, read='text')
        self.mail([flight('EX 3410', 'Brussels', 'Portavia', '2026-06-14T17:20', '2026-06-14T19:50', code='V2NB6Q', others=1)], 7, 'work', 'text')
        self.mail([{'type': 'train', 'status': 'confirmed', 'code': 'COMMUTE1', 'start': '2026-06-12', 'from': 'Riverton-Central', 'to': 'Oakdale'}], 8, 'work', 'text')

    def test_one_journey_is_one_trip_with_every_booking_in_time_order(self):
        self.journey()
        trips = self.trips()
        self.assertEqual(len(trips), 1)
        trip = trips[0]
        self.assertEqual((trip['title'], trip['starts'], trip['ends']), ('Valmar', '2026-06-13', '2026-06-20'))
        self.assertEqual([x['text'] for x in trip['lines']], [
            'Train Example Rail RIVERTON-WEST to BRUSSELS AIRPORT, booking TKT48213',
            'Casa Lumen, 7 nights, Carrer del Port 7, 09999 Valmar, booking HMXQ7741',
            'Flight EX 3410 Brussels to Portavia, arrives 19:50, booking Q4TR7N, seat 12C',
            'Rental car Example Cars, pick up in Portavia Airport, booking 90210554',
            'Tickets for Coastal boat tour, Valmar marina, booking T-88',
            'Return the rental car in Portavia Airport',
            'Check out of Casa Lumen',
            'Flight EX 9120 Portavia to Bruxel, arrives 12:40, booking W8KD2P'])  # a rental car at hand: nothing missing
        with self.store.connect() as db:
            self.assertEqual(event_notes.drafts(db, [MAIL])[0], [])  # the tour is on the trip, not under Events

    def test_a_trip_already_over_shows_no_gaps_and_real_gaps_show_ahead(self):
        self.mail([flight('EX 6101', 'Southport (North)', 'Seravo', '2026-09-05T11:15', '2026-09-05T13:15', code='R5LM3X'),
                   flight('EX 6102', 'Seravo', 'Southport (North)', '2026-09-12T13:40', '2026-09-12T15:45', code='R5LM3X')], 1)
        self.mail([{'type': 'hotel', 'status': 'confirmed', 'code': '550017342', 'start': '2026-09-05', 'end': '2026-09-10',
                    'name': 'Hotel Bellacosta', 'where': 'Seravo'}], 2, read='text')
        self.mail([{'type': 'parking', 'status': 'confirmed', 'code': '9C41AD02', 'start': '2026-09-05T09:00', 'end': '2026-09-12T16:30',
                    'name': 'Example Park&Fly', 'where': 'Southport Airport'}], 3, read='text')
        lines = [x['text'] for x in self.trips(today='2026-08-01')[0]['lines']]
        self.assertEqual(lines, [
            'Parking at Example Park&Fly, booking 9C41AD02',
            'Flight EX 6101 Southport (North) to Seravo, arrives 13:15, booking R5LM3X',
            'Nothing booked from Seravo airport to Hotel Bellacosta',
            'Hotel Bellacosta, 5 nights, booking 550017342',
            'Check out of Hotel Bellacosta',
            'No place to stay booked for 2 nights',
            'Flight EX 6102 Seravo to Southport (North), arrives 15:45, booking R5LM3X',
            'Pick up the car at Example Park&Fly'])
        gap = next(x for x in self.trips(today='2026-08-01')[0]['lines'] if x.get('item') == 'gap' and 'nights' in x['text'])
        self.assertEqual((gap['at'], gap['data']), ('2026-09-10', {'gap': 1, 'until': '2026-09-11'}))
        self.assertFalse([x for x in self.trips(today='2026-11-01')[0]['lines'] if x.get('item') == 'gap'])

    def test_one_night_without_a_stay_keeps_the_count(self):
        # Every count form keeps the key's {}: the daily translator holds each language's forms to it (Russian "one"
        # is also 21 nights), so a "for the night" form stayed English in every language with a one form.
        self.assertEqual(trip_notes.t('No place to stay booked for {} nights', 1, lang='en'), 'No place to stay booked for 1 night')
        self.assertEqual(trip_notes.t('No place to stay booked for {} nights', 3, lang='en'), 'No place to stay booked for 3 nights')

    def test_a_trip_without_any_stay_flags_no_nights(self):
        self.mail([flight('EX 701', 'Brussels', 'Lisbon', '2026-03-03T17:55', '2026-03-03T19:40', code='J3XKPF'),
                   flight('EX 703', 'Lisbon', 'Natal', '2026-03-03T23:25', '2026-03-04T05:00', code='J3XKPF'),
                   flight('EX 704', 'Natal', 'Lisbon', '2026-03-19T22:25', '2026-03-20T12:00', code='J3XKPF'),
                   flight('EX 702', 'Lisbon', 'Brussels', '2026-03-20T16:15', '2026-03-20T19:50', code='J3XKPF')], 1)
        trip = self.trips(today='2026-02-01')[0]
        self.assertEqual(trip['title'], 'Natal')  # where it stays longest, not the stop on the way
        self.assertFalse([x for x in trip['lines'] if x.get('item') == 'gap'])
        self.assertIn('arrives 05:00 the next day', trip['lines'][1]['text'])

    def test_a_change_of_day_updates_its_line_and_a_cancellation_by_code_takes_it_out(self):
        self.mail([flight('EX 6101', 'Brussels', 'Seravo', '2026-09-05T11:15', '2026-09-05T13:15', code='R5LM3X')], 1)
        self.mail([flight('EX 6101', 'Brussels', 'Seravo', '2026-09-06T11:15', '2026-09-06T13:15', code='R5LM3X')], 2, read='text')
        trip = self.trips()[0]
        self.assertEqual((trip['starts'], len(trip['lines'])), ('2026-09-06', 1))
        self.mail([{'type': 'parking', 'status': 'confirmed', 'code': 'P1', 'start': '2026-09-06T08:00', 'end': '2026-09-08T10:00', 'where': 'Southport'}], 3)
        self.assertEqual(len(self.trips()[0]['lines']), 3)
        self.mail([{'type': 'parking', 'status': 'canceled', 'code': 'P1'}], 4, read='text')
        self.assertEqual(len(self.trips()[0]['lines']), 1)

    def test_a_commute_is_no_trip_and_a_day_out_by_train_is(self):
        ride = lambda code, day, dep, arr, at='': {'type': 'train', 'status': 'confirmed', 'code': code, 'start': f'2026-06-{day:02d}{at}',
                                                   'from': dep, 'to': arr}
        for n, day in enumerate((3, 4, 10)):  # the office: the same route on several days, with times or without
            self.mail([ride(f'C{n}', day, 'OAKDALE', 'RIVERTON-CENTRAL', 'T08:43'), ride(f'D{n}', day, 'RIVERTON-CENTRAL', 'OAKDALE', 'T17:31')], n + 1)
        self.mail([ride('K1', 6, 'ELMSWOOD', 'RIVERTON-CENTRAL'), ride('K2', 6, 'RIVERTON-CENTRAL', 'OAKDALE')], 5)  # one way home
        self.mail([ride('G1', 8, 'OAKDALE', 'HARBORVILLE-EAST'), ride('G1', 8, 'HARBORVILLE-EAST', 'OAKDALE')], 6)
        self.assertEqual([(x['title'], x['starts'], len(x['lines'])) for x in self.trips()], [('Harborville-East', '2026-06-08', 2)])

    def test_one_booking_from_several_mails_is_one_line(self):
        """The holiday home's confirmation with its code, the host's mail without it but with times, and a fellow
        traveler's boarding pass for the owner's flight."""
        self.mail([{'type': 'hotel', 'status': 'confirmed', 'code': 'HM1', 'start': '2026-06-13', 'end': '2026-06-20', 'name': 'VILLA SOL',
                    'where': 'Valmar', 'address': 'Calle 1, Valmar'}], 1, read='text')
        self.mail([{'type': 'hotel', 'status': 'confirmed', 'start': '2026-06-13T17:00', 'end': '2026-06-20T10:00', 'name': 'Villa Sol'}], 2, read='text')
        self.mail([flight('EX 3410', 'Brussels', 'Portavia', '2026-06-13T12:20', '2026-06-13T14:50', code='Q4TR7N')], 3, read='text')
        self.mail([flight('EX3410', 'Brussels', 'Portavia', '2026-06-13T12:20', '2026-06-13T14:50', code='Q4TR7N', seat='31A', others=1)], 4, read='text')
        self.mail([flight('EX 701', 'Paris Orly (ORY)', 'Porto-Francisco Sa Carneiro Airport (OPO)', '2026-06-20T12:00', '2026-06-20T13:40', code='Z1')], 5)
        lines = [x['text'] for x in self.trips()[0]['lines']]
        self.assertEqual(lines, ['Flight EX 3410 Brussels to Portavia, arrives 14:50, booking Q4TR7N',
                                 'Nothing booked from Portavia airport to Villa Sol',
                                 'Villa Sol, 7 nights, Calle 1, Valmar, booking HM1',
                                 'Check out of Villa Sol',
                                 'Nothing booked from Villa Sol to Paris Orly airport',
                                 'Flight EX 701 Paris Orly (ORY) to Porto-Francisco Sa Carneiro Airport (OPO), arrives 13:40, booking Z1'])
        self.assertEqual(bookings.checked({'type': 'flight', 'start': '2026-06-20T00:00', 'from': 'A', 'to': 'B'})['start'], '2026-06-20')

    def test_a_ride_home_days_later_through_another_place_joins_the_way_out(self):
        self.mail([flight('11', 'Brussels', 'Porto', '2026-12-10T07:00', '2026-12-10T08:30', code='A1')], 1)
        self.mail([{'type': 'train', 'status': 'confirmed', 'code': 'B2', 'start': '2026-12-14T10:00', 'end': '2026-12-14T13:00', 'from': 'Porto',
                    'to': 'Lisboa Oriente'}], 2)
        self.mail([flight('12', 'Lisbon', 'Brussels', '2026-12-20T19:00', '2026-12-20T22:30', code='C3')], 3)
        self.mail([flight('13', 'Brussels', 'Rome', '2026-12-28T07:00', '2026-12-28T09:00', code='D4')], 4)
        self.assertEqual([(x['title'], x['starts'], x['ends']) for x in self.trips()],
                         [('Lisboa Oriente', '2026-12-10', '2026-12-20'), ('Rome', '2026-12-28', '2026-12-28')])


class ExtractStep(unittest.TestCase):
    """TripsApp.trip_extract_step: booking-like mail waits, one call reads a few, the trips follow."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite', protect=True)
        self.app = object.__new__(machine_main.App)
        self.app.store, self.app.config = self.store, {'accounts': [MAIL], 'database': str(self.store.path), 'owner_name': 'Alex Owner'}
        self.app.background_pause = lambda **_: None
        self.app.background_spaced = lambda: True
        self.app.background_started = lambda: None
        self.asked = []
        self.answer = None
        self.app.trip_extract_model = lambda prompt: (self.asked.append(prompt), self.answer(prompt))[1]
        today = mock.patch.object(trip_notes, '_today', return_value='2026-05-01')
        today.start()
        self.addCleanup(today.stop)

    def inbox(self, title, body, sender='Stays <stays@homes.example>', minutes=0):
        when = (dt.datetime(2026, 3, 18, 9, 0, tzinfo=dt.timezone.utc) + dt.timedelta(minutes=minutes)).isoformat()
        self.store.commit_page('home', None, [{'account_id': 'home', 'source_id': f's{len(self.asked)}-{minutes}', 'kind': 'gmail.message',
                                               'occurred_at': when, 'title': title, 'body': body, 'deleted': False,
                                               'metadata': {'from': sender, 'to': 'owner@example.com', 'labels': ['INBOX'], 'thread_id': f't{minutes}'}}],
                               record_sync=False)

    def run_step(self):
        self.app.trip_extract_at = -10 ** 9
        started = self.app.trip_extract_step()
        if started:
            self.app._trip_extract_thread.join()
        return started

    def test_booking_mail_is_read_once_and_becomes_a_trip(self):
        self.inbox('Reservation confirmed: Casa Lumen', HOME_RENTAL)
        self.inbox('Reservation confirmed: Casa Lumen', HOME_RENTAL, minutes=1)  # the same mail twice: read once
        self.inbox('Last minute deals', NEWSLETTER, sender='Air <news@air.example>', minutes=2)
        with self.store.connect() as db:
            trip_notes.collect(db)
            self.assertEqual(trip_notes.waiting(db), 2)

        def answer(prompt):
            ids = [x.split()[0] for x in prompt.split('<<<MAIL ')[1:]]
            return json.dumps({ids[0]: [{'type': 'hotel', 'code': 'HMXQ7741', 'start': '2026-06-13T17:00', 'end': '2026-06-20T10:00',
                                         'name': 'Casa Lumen', 'where': 'Valmar', 'owner_on_it': 'unknown'}]})
        self.answer = answer
        self.assertTrue(self.run_step())
        self.assertEqual(len(self.asked), 1)
        self.assertEqual(self.asked[0].count('<<<MAIL'), 1)
        self.assertIn('The owner is Alex Owner.', self.asked[0])
        self.app.trip_notes_step()
        self.assertEqual([x['name'] for x in self.trips()], ['Valmar'])
        self.assertFalse(self.run_step())  # nothing waits: no call
        self.assertEqual(len(self.asked), 1)

    def test_no_answer_is_tried_again_and_the_day_has_a_cap(self):
        self.inbox('Reservation confirmed: Casa Lumen', HOME_RENTAL)
        with self.store.connect() as db:
            trip_notes.collect(db)
        self.answer = lambda prompt: 'Sorry, no.'
        for _ in range(trip_notes.PENDING_TRIES):
            self.assertTrue(self.run_step())
        self.assertFalse(self.run_step())  # passed after its tries
        with self.store.connect() as db:
            self.assertEqual(trip_notes.waiting(db), 0)
        from machine.app import trips as app_trips
        for n in range(3):
            self.inbox('Reservation confirmed: Casa Lumen', HOME_RENTAL.replace('HMXQ7741', f'HMXQ774{n}'), minutes=10 + n * 1440)
        with self.store.connect() as db:
            trip_notes.collect(db)
        self.answer = lambda prompt: '{}'
        self.app.trip_extract_calls = ('2000-01-01', 9)  # an earlier day's calls don't count
        with mock.patch.object(app_trips, 'EXTRACT_MAILS', 1), mock.patch.object(app_trips, 'EXTRACT_CALLS_DAY', 1):
            self.assertTrue(self.run_step())
            self.assertFalse(self.run_step())  # the day's one call is used

    def test_the_history_walk_reads_a_stub_mail_in_full_for_the_model(self):
        """A mail kept with only its "sent in HTML" note waits with that; the history walk reads it in full again
        (HistoryApp.history_bookings) and the model gets the whole text, sealed at rest."""
        self.inbox('Reservation confirmed: Casa Lumen 7 nights', 'Reservation confirmed. Your client does not support HTML.')
        with self.store.connect() as db:
            event_id = db.execute('SELECT id FROM events').fetchone()[0]
            trip_notes.queue(db, event_id, 'home', '2026-03-18T09:00:00+00:00')
            trip_notes.queue(db, event_id, 'home', '2026-03-18T09:00:00+00:00', HOME_RENTAL)
            self.assertIn('HMXQ7741', trip_notes.pending(db, 6)[0]['text'])
        import sqlite3
        raw = sqlite3.connect(self.store.path)
        stored = raw.execute('SELECT text FROM trip_pending').fetchone()[0]
        raw.close()
        self.assertNotIn(b'HMXQ7741', stored if isinstance(stored, bytes) else stored.encode())

    def trips(self):
        with self.store.connect() as db:
            return [x for x in note_pages.dated(db, '0001-01-01', '9999-12-31') if x['kind'] == 'trip']


if __name__ == '__main__':
    unittest.main()
