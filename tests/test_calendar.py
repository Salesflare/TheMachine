"""The dashboard's Calendar: meetings that overlap a window of at most 15 days, as slim read-only rows, soonest first.
Declined and canceled meetings stay out, all-day ones count on every day they cover, and only https links go out.
No live calls."""
import http.client
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('calendar_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

ACCOUNT = {'id': 'cal', 'email': 'owner@example.com', 'service': 'calendar', 'boundary': 'work:Example'}
SHARED = {'id': 'partner-cal', 'email': 'owner@example.com', 'service': 'calendar', 'boundary': 'personal:Home', 'calendar_id': 'robin.lane@example.net'}


def meeting(source_id, start, end, title='Pilot review', account=ACCOUNT, **extra):
    raw = {'id': source_id, 'summary': title, 'start': start, 'end': end, 'status': 'confirmed', 'description': 'Private notes',
           'htmlLink': 'https://calendar.google.com/calendar/event?eid=' + source_id, **extra}
    return a.calendar_event(account, raw, 'Europe/Brussels')


def eid(event, calendar):
    return a.base64.urlsafe_b64encode(f'{event} {calendar}'.encode()).decode().rstrip('=')


class Calendar(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        odd = meeting('odd', {'dateTime': '2026-10-25T09:00:00+02:00'}, {'dateTime': '2026-10-25T09:30:00+02:00'}, 'Odd link')
        odd['metadata']['source_url'] = 'javascript:alert(1)'
        self.store.commit_page('cal', {}, [
            meeting('before', {'dateTime': '2026-10-22T10:00:00+02:00'}, {'dateTime': '2026-10-22T11:00:00+02:00'}, 'Yesterday'),
            meeting('ongoing', {'dateTime': '2026-10-22T23:30:00+02:00'}, {'dateTime': '2026-10-23T00:30:00+02:00'}, 'Late call'),
            meeting('pilot', {'dateTime': '2026-10-23T18:00:00+02:00'}, {'dateTime': '2026-10-23T18:45:00+02:00'}, location='Zoom',
                    attendees=[{'email': 'owner@example.com', 'self': True, 'responseStatus': 'accepted'},
                               {'email': 'sam@client.example'}, {'email': 'kim@client.example'}]),
            meeting('declined', {'dateTime': '2026-10-24T09:00:00+02:00'}, {'dateTime': '2026-10-24T10:00:00+02:00'}, 'Said no',
                    attendees=[{'email': 'owner@example.com', 'self': True, 'responseStatus': 'declined'}]),
            meeting('cancelled', {'dateTime': '2026-10-24T11:00:00+02:00'}, {'dateTime': '2026-10-24T12:00:00+02:00'}, 'Off', status='cancelled'),
            meeting('offsite', {'date': '2026-10-26'}, {'date': '2026-10-28'}, 'Team offsite'),
            meeting('later', {'dateTime': '2026-11-02T09:00:00+01:00'}, {'dateTime': '2026-11-02T10:00:00+01:00'}, 'Next month'),
            odd])
        self.week = ('2026-10-22T22:00:00.000Z', '2026-10-29T23:00:00.000Z')  # Brussels midnight to midnight, seven days

    def test_who_it_is_with_by_name_from_the_graph_and_the_address_when_unknown(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('email:sam@client.example','person','Sam Client',1,0,'{}')")
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('email:kim@client.example','person','kim@client.example',1,0,'{}')")
        pilot = self.store.calendar(['cal'], *self.week)[1]
        self.assertEqual(pilot['with'], [{'name': 'Sam Client', 'email': 'sam@client.example'}, {'name': '', 'email': 'kim@client.example'}])
        self.assertEqual(pilot['people'], ['Sam Client', 'kim@client.example'])

    def test_a_meeting_links_to_its_people_organizations_and_projects_on_the_graph(self):
        with self.store.connect() as db:
            pilot_id = db.execute("SELECT id FROM events WHERE title='Pilot review'").fetchone()[0]
            db.executemany('INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,?,?,1,0,?)', [
                ('email:sam@client.example', 'person', 'Sam Client', json.dumps({'identifiers': ['email:sam@client.example', 'slack:U1'], 'org': 'org:client.example'})),
                ('org:client.example', 'org', 'Client Co', '{}'), ('project:1', 'project', 'Pilot', '{}'), ('project:2', 'project', 'Maybe', '{}'),
                ('project:3', 'project', 'Rollout', '{}'), ('project:4', 'project', 'Old', json.dumps({'closed_at': '2026-01-01'}))])
            db.executemany('INSERT INTO projects(id,name,created_at,closed_at) VALUES(?,?,?,?)', [(3, 'Rollout', '2026-10-01', None), (4, 'Old', '2026-01-01', '2026-02-01')])
            db.executemany("INSERT INTO graph_links(a,b,kind,strength) VALUES('email:sam@client.example',?,'project',1)", [('project:3',), ('project:4',)])
            db.executemany('INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,?,1)', [
                ('email:sam@client.example', pilot_id, '2026-10-23', 0), ('project:1', pilot_id, '2026-10-23', 0), ('project:2', pilot_id, '2026-10-23', 1),
                ('project:4', pilot_id, '2026-10-23', 0)])
        week = self.store.calendar(['cal'], *self.week)
        pilot = week[1]
        self.assertEqual(pilot['with'][0], {'name': 'Sam Client', 'email': 'sam@client.example', 'node_id': 'email:sam@client.example'})
        self.assertNotIn('node_id', pilot['with'][1])  # not on the Graph: no link
        self.assertEqual(pilot['orgs'], [{'node_id': 'org:client.example', 'name': 'Client Co'}])
        # on the meeting, then Sam's open one; a guess and a closed project stay out
        self.assertEqual(pilot['projects'], [{'node_id': 'project:1', 'name': 'Pilot'}, {'node_id': 'project:3', 'name': 'Rollout'}])
        self.assertNotIn('orgs', week[0])

    def test_a_meeting_lists_people_once_never_rooms_and_only_projects_it_is_about(self):
        """The board meeting as it showed: a booked room as a guest, one person on two addresses (one declined), and a
        cofounder who is on every project. Rooms go, the person shows once, and only an outside guest's project ties in."""
        self.store.commit_page('cal', {}, [meeting('board', {'dateTime': '2026-10-28T10:00:00+01:00'}, {'dateTime': '2026-10-28T12:00:00+01:00'}, 'Board Q3',
            attendees=[{'email': 'owner@example.com', 'self': True, 'responseStatus': 'accepted'},
                       {'email': 'lee@example.com', 'displayName': 'Lee Cofounder', 'responseStatus': 'accepted'},
                       {'email': 'falcon_room@venue.example', 'responseStatus': 'accepted'},
                       {'email': 'c_9@resource.calendar.google.com', 'displayName': 'Desk 4', 'resource': True},
                       {'email': 'bo@investor.example', 'responseStatus': 'needsAction'},
                       {'email': 'bo@fund.example', 'displayName': 'Bo (fund)', 'responseStatus': 'declined'},
                       {'email': 'ida@investor.example', 'responseStatus': 'accepted'}])])
        with self.store.connect() as db:
            board_id = db.execute("SELECT id FROM events WHERE title='Board Q3'").fetchone()[0]
            db.executemany('INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,?,?,1,0,?)', [
                ('email:lee@example.com', 'person', 'Lee Cofounder', json.dumps({'identifiers': ['email:lee@example.com'], 'colleague': True})),
                ('email:falcon_room@venue.example', 'person', 'Falcon Meeting Room', json.dumps({'identifiers': ['email:falcon_room@venue.example'], 'org': 'org:venue.example'})),
                ('org:venue.example', 'org', 'Venue Co', '{}'),
                ('email:bo@investor.example', 'person', 'Bo Investor', json.dumps({'identifiers': ['email:bo@investor.example', 'email:bo@fund.example'], 'org': 'org:investor.example'})),
                ('org:investor.example', 'org', 'Investor', '{}'),
                ('email:ida@investor.example', 'person', 'Ida Investor', json.dumps({'identifiers': ['email:ida@investor.example'], 'org': 'org:investor.example'}))])
            db.executemany('INSERT INTO projects(id,name,created_at,closed_at) VALUES(?,?,?,NULL)',
                           [(5, 'Refund', '2026-10-01'), (8, 'Home internet', '2026-10-01'), (9, 'Series A', '2026-10-01')])
            db.executemany("INSERT INTO graph_links(a,b,kind,strength) VALUES(?,?,'project',1)",
                           [('email:lee@example.com', 'project:5'), ('email:lee@example.com', 'project:8'), ('email:lee@example.com', 'project:9'),
                            ('email:ida@investor.example', 'project:9')])
            db.executemany('INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,0,1)',
                           [(n, board_id, '2026-10-28') for n in ('email:lee@example.com', 'email:falcon_room@venue.example', 'email:bo@investor.example',
                                                                  'email:ida@investor.example')])
            db.execute("INSERT INTO graph_resources(identifier,resource,source,event_id,name,created_at) "
                       "VALUES('email:falcon_room@venue.example',1,'review',?,'Falcon Meeting Room','2026-10-27')", (board_id,))
        board = next(m for m in self.store.calendar(['cal'], *self.week, owner={'owner@example.com'}) if m['title'] == 'Board Q3')
        self.assertEqual([w['email'] for w in board['with']], ['lee@example.com', 'bo@investor.example', 'ida@investor.example'])
        self.assertEqual(board['people'], ['Lee Cofounder', 'Bo Investor', 'Ida Investor'])
        self.assertEqual(board['guests'], 3)
        self.assertEqual(board['orgs'], [{'node_id': 'org:investor.example', 'name': 'Investor'}])  # not the room's venue
        self.assertEqual(board['projects'], [{'node_id': 'project:9', 'name': 'Series A'}])  # an outside guest's, not the cofounder's every project
        self.assertNotIn('declined', json.dumps(board))
        self.assertEqual(board['rooms'], ['Falcon Meeting Room', 'Desk 4'])  # shown under Where, by the name the Graph kept

    def test_a_room_by_its_address_or_name_is_where_not_who(self):
        """A room an outside organization booked comes as a plain guest without a flag. Its address or name says it is a
        room: it shows under Where (after the location, once), never as a person; one the owner said is a person stays."""
        self.store.commit_page('cal', {}, [meeting('visit', {'dateTime': '2026-10-28T13:30:00+01:00'}, {'dateTime': '2026-10-28T14:30:00+01:00'}, 'Visit',
            location='Main Street 14, Antwerp',
            attendees=[{'email': 'owner@example.com', 'self': True, 'responseStatus': 'accepted'},
                       {'email': 'falconheavy_room@venue.example', 'responseStatus': 'accepted'},
                       {'email': 'atlas@hall.example', 'displayName': 'Atlas Conference Room', 'responseStatus': 'accepted'},
                       {'email': 'r2@hall.example', 'displayName': 'Main Street 14, Antwerp', 'resource': True},
                       {'email': 'board.room@kept.example', 'displayName': 'Boardroom Bea', 'responseStatus': 'accepted'},
                       {'email': 'kim@client.example', 'displayName': 'Kim Client', 'responseStatus': 'accepted'}]),
            meeting('rooms', {'dateTime': '2026-10-28T15:00:00+01:00'}, {'dateTime': '2026-10-28T16:00:00+01:00'}, 'Room only',
            attendees=[{'email': 'owner@example.com', 'self': True, 'responseStatus': 'accepted'},
                       {'email': 'c_9@resource.calendar.google.com', 'resource': True},
                       {'email': 'falconheavy_room@venue.example', 'responseStatus': 'accepted'}])])
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_resources(identifier,resource,source,event_id,name,created_at) "
                       "VALUES('email:board.room@kept.example',0,'owner',NULL,'Boardroom Bea','2026-10-27')")
        week = {m['title']: m for m in self.store.calendar(['cal'], *self.week, owner={'owner@example.com'})}
        visit = week['Visit']
        self.assertEqual([w['email'] for w in visit['with']], ['board.room@kept.example', 'kim@client.example'])
        self.assertEqual(visit['guests'], 2)
        self.assertEqual((visit['location'], visit['rooms']), ('Main Street 14, Antwerp', ['Falconheavy room', 'Atlas Conference Room']))
        only = week['Room only']
        self.assertEqual((only['with'], only['guests'], only['location'], only['rooms']), ([], 0, '', ['Falconheavy room']))

    def test_the_week_is_slim_rows_soonest_first(self):
        rows = self.store.calendar(['cal'], *self.week)
        self.assertEqual([r['title'] for r in rows], ['Late call', 'Pilot review', 'Odd link', 'Team offsite'])
        pilot = rows[1]
        self.assertEqual(set(pilot), {'id', 'account_id', 'title', 'start', 'end', 'all_day', 'location', 'guests', 'people', 'with', 'url', 'shared'})
        self.assertEqual((pilot['people'], pilot['shared']), (['sam@client.example', 'kim@client.example'], None))
        self.assertEqual(pilot['with'], [{'name': '', 'email': 'sam@client.example'}, {'name': '', 'email': 'kim@client.example'}])
        self.assertEqual((pilot['start'], pilot['end'], pilot['location'], pilot['guests']),
                         ('2026-10-23T16:00:00+00:00', '2026-10-23T16:45:00+00:00', 'Zoom', 2))
        self.assertTrue(pilot['url'].startswith('https://calendar.google.com/'))
        self.assertNotIn('Private notes', json.dumps(rows))  # no bodies
        self.assertIsNone(rows[2]['url'])  # only https links
        self.assertTrue(rows[3]['all_day'])
        self.assertEqual(self.store.calendar([], *self.week), [])
        self.assertEqual(self.store.calendar(['other'], *self.week), [])

    def shared_week(self):
        at = lambda h: {'dateTime': f'2026-10-27T{h}:00:00+01:00'}
        theirs = {'email': 'robin.lane@example.net', 'self': True}  # 'self' on a shared calendar is its owner
        self.store.commit_page('partner-cal', {}, [
            meeting('trip', {'dateTime': '2026-10-23T19:00:00+02:00'}, {'dateTime': '2026-10-25T19:00:00+01:00'}, 'Weekend away', SHARED, organizer=theirs),
            meeting('parents', at('16'), at('17'), 'Parents evening', SHARED, organizer={'email': 'owner@example.com', 'displayName': 'Owner'},
                    attendees=[{'email': 'robin.lane@example.net', 'self': True, 'responseStatus': 'accepted'}],
                    htmlLink='https://www.google.com/calendar/event?eid=' + eid('abc123', 'robin.lane@example.net')),
            meeting('dinner', at('19'), at('21'), 'Dinner with Alex', SHARED, organizer=theirs,
                    attendees=[{'email': 'robin.lane@example.net', 'self': True}, {'email': 'owner@example.com', 'responseStatus': 'accepted'}]),
            meeting('their-no', at('09'), at('10'), 'Dentist', SHARED, organizer=theirs,
                    attendees=[{'email': 'owner@example.com', 'responseStatus': 'declined'}, {'email': 'robin.lane@example.net', 'self': True}])])
        self.store.commit_page('cal', {}, [
            meeting('parents-mine', at('16'), at('17'), 'Parents evening', organizer={'email': 'owner@example.com', 'self': True},
                    htmlLink='https://www.google.com/calendar/event?eid=' + eid('abc123', 'owner@example.com')),
            meeting('copy', at('12'), at('13'), 'Lunch  with Sam'), meeting('copy-2', at('12'), at('13'), 'lunch with sam')])
        return {m['title']: m for m in self.store.calendar(['cal', 'partner-cal'], *self.week, owner={'Owner@example.com'})}

    def test_a_shared_calendar_shows_marked_and_a_meeting_on_both_once_as_the_owners(self):
        rows = self.shared_week()
        # Someone else's event on a calendar shared with the owner: shown, with that person's first name
        self.assertEqual((rows['Weekend away']['shared'], rows['Weekend away']['account_id']), ('Robin', 'partner-cal'))
        # On both calendars (the same Google event): once, the owner's own copy
        self.assertEqual((rows['Parents evening']['account_id'], rows['Parents evening']['shared']), ('cal', None))
        # Invited on the shared calendar: theirs to attend, so it is the owner's meeting; declined stays out
        self.assertIsNone(rows['Dinner with Alex']['shared'])
        self.assertEqual(rows['Dinner with Alex']['guests'], 1)
        self.assertNotIn('Dentist', rows)
        # Two invites with the same start, end and title: once
        self.assertEqual(sum(t.casefold().split() == ['lunch', 'with', 'sam'] for t in rows), 1)

    def test_one_meeting_opened_from_anywhere_is_the_calendars_row(self):
        """A meeting opened from a timeline, Events or a to-do's source shows the Calendar's own row: the copy the Calendar
        keeps (so its notes are the same ones), with its notes marker; one the owner declined still opens."""
        rows = self.shared_week()
        with self.store.connect() as db:
            ids = dict(db.execute("SELECT source_id,id FROM events").fetchall())
            db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,ingested_at) "
                       "VALUES('cal',?,'meeting.notes','2026-10-27T15:00:00+00:00','Notes','We agreed.','{}',0,'h','2026-10-27T18:00:00+00:00')",
                       (f"notes:{ids['parents-mine']}",))
        owner = {'owner@example.com'}
        mine = self.store.meeting(['cal', 'partner-cal'], ids['parents-mine'], owner)
        self.assertEqual({k: v for k, v in mine.items() if k != 'notes'}, rows['Parents evening'])
        self.assertEqual(mine['notes']['by'], 'owner')
        # The shared calendar's copy of it opens as the owner's own, the one its notes are on
        self.assertEqual(self.store.meeting(['cal', 'partner-cal'], ids['parents'], owner)['id'], ids['parents-mine'])
        self.assertEqual(self.store.meeting(['cal'], ids['pilot'], owner)['title'], 'Pilot review')
        self.assertEqual(self.store.meeting(['cal'], ids['declined'], owner)['title'], 'Said no')  # not on the Calendar, still opens
        self.assertIsNone(self.store.meeting(['cal'], ids['cancelled'], owner))
        self.assertIsNone(self.store.meeting(['partner-cal'], ids['pilot'], owner))  # not on these accounts
        self.assertIsNone(self.store.meeting([], ids['pilot'], owner))

    def test_a_shared_calendar_never_makes_cards(self):
        self.shared_week()
        with self.store.connect() as db:
            ids = dict(db.execute("SELECT source_id,id FROM events WHERE source_id IN ('trip','dinner')").fetchall())
        with self.assertRaisesRegex(ValueError, "someone else's calendar"):
            self.store.suggest('trip-prep', 'Pack for the weekend', 'Pack for it.', [ids['trip']])
        self.assertEqual(self.store.suggest('dinner-prep', 'Book the dinner', 'Book a table.', [ids['dinner']])['status'], 'pending')
        with self.store.connect() as db:
            trip = dict(db.execute('SELECT * FROM events WHERE id=?', (ids['trip'],)).fetchone())
        self.assertIn("Robin's calendar", a.review_view(trip)['not_owners'])

    def test_the_window_is_bounded_and_has_time_zones(self):
        for start, end in [('2026-10-23T00:00:00', '2026-10-24T00:00:00'), ('2026-10-23T00:00:00Z', '2026-11-23T00:00:00Z'),
                           ('2026-10-24T00:00:00Z', '2026-10-23T00:00:00Z'), ('', ''), ('soon', 'later')]:
            with self.subTest(start=start), self.assertRaises(ValueError):
                self.store.calendar(['cal'], start, end)

    def test_dashboard_route_is_read_only_for_the_owner(self):
        app = object.__new__(a.App)
        app.store, app.token, app.stop = self.store, 'test-token', threading.Event()
        app.graph_dirty = threading.Event()
        app.owner_token = 'owner-key'
        app.config = {'accounts': [ACCOUNT], 'tailscale_owner': 'owner@example.com', 'dashboard_host': 'machine.example:8443',
                      'port': 0, 'http_timeout': 1}
        servers, real = [], a.http.server.ThreadingHTTPServer
        def capture(*args, **kwargs):
            servers.append(real(*args, **kwargs)); return servers[-1]
        for patcher in (patch.object(a.http.server, 'ThreadingHTTPServer', side_effect=capture), patch.object(a.signal, 'signal'),
                        patch.object(a.App, 'preparation_worker'), patch.object(a.App, 'delivery_worker')):
            patcher.start()
            self.addCleanup(patcher.stop)
        thread = threading.Thread(target=app.serve, daemon=True)
        thread.start()
        while not servers:
            pass
        self.addCleanup(lambda: (app.stop.set(), thread.join(5)))
        port = servers[0].server_address[1]
        owner = {'Host': 'machine.example:8443', 'Tailscale-User-Login': 'owner@example.com'}
        def get(path):
            conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
            conn.request('GET', path, headers=owner)
            r = conn.getresponse()
            body = r.read()
            conn.close()
            return r.status, json.loads(body)
        before = self.store.snapshot([ACCOUNT])
        status, body = get('/api/calendar?from=' + self.week[0] + '&to=' + self.week[1])
        self.assertEqual(status, 200)
        self.assertEqual([m['title'] for m in body['meetings']], ['Late call', 'Pilot review', 'Odd link', 'Team offsite'])
        self.assertEqual(get('/api/calendar?from=2026-10-23T00:00:00Z&to=2027-01-01T00:00:00Z')[0], 400)
        self.assertEqual(get('/api/calendar')[0], 400)
        # One meeting, opened from anywhere: the Calendar's row; none for a signal that is no meeting
        pilot = next(m for m in body['meetings'] if m['title'] == 'Pilot review')
        self.assertEqual(get(f"/api/meeting?event={pilot['id']}"), (200, {'meeting': pilot}))
        self.assertEqual(get('/api/meeting?event=999999'), (200, {'meeting': None}))
        self.assertEqual(get('/api/meeting?event=x')[0], 400)
        after = self.store.snapshot([ACCOUNT])
        self.assertEqual((before['suggestions'], before['decisions']), (after['suggestions'], after['decisions']))


if __name__ == '__main__':
    unittest.main()
