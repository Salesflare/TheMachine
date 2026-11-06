"""Google Calendar as a source: its API client (Calendar), an event as a signal (calendar_event) with its rooms,
owner and guests, the events a calendar write may change, the people an invite can go to, and its sync
(sync_calendar). Moved out of assistant.py as is."""
import base64
import datetime as dt
import html
import json
import re
import sqlite3
import urllib.parse
from zoneinfo import ZoneInfo

import calendar_writes
import graph
from machine.cards import undated_card
from machine.sources.exclusions import calendar_title_excluded
from machine.sources.rows import Skips
import ms_graph
import own_addresses
from sources import SourceError, gog_read
from timeutil import local_tz, now


class Calendar:
    def __init__(self, config, account):
        self.config, self.account = config, account

    def get(self, method, params):
        if method not in ('calendars.get', 'events.list'):
            raise SourceError('unsupported_calendar_method')
        calendar_id = self.account.get('calendar_id', 'primary')
        if 'calendarId' in params and params['calendarId'] != calendar_id:
            raise SourceError('calendar_identity_mismatch')
        return gog_read(self.config, self.account, 'calendar', 'v3', 'calendar.' + method,
                        {**params, 'calendarId': calendar_id},
                        'https://www.googleapis.com/auth/calendar.readonly')

    def profile(self):
        profile = self.get('calendars.get', {})
        expected = self.account.get('calendar_id', 'primary')
        if expected == 'primary':
            expected = self.account['email']
        if profile.get('id', '').lower() != expected.lower():
            raise SourceError('account_identity_mismatch')
        return profile


def calendar_time(value, timezone):
    if value.get('date'):
        return dt.datetime.combine(dt.date.fromisoformat(value['date']), dt.time(),
                                   ZoneInfo(timezone)).astimezone(dt.timezone.utc).isoformat()
    stamp = dt.datetime.fromisoformat(value['dateTime'].replace('Z', '+00:00'))
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=ZoneInfo(value.get('timeZone', timezone)))
    return stamp.astimezone(dt.timezone.utc).isoformat()


def calendar_event(account, raw, timezone):
    start, end = raw['start'], raw['end']
    # resource: a room or other thing booked on the invite (Google's flag), never a person
    attendees = [{k: a[k] for k in ('email', 'displayName', 'responseStatus', 'self', 'resource') if k in a}
                 for a in raw.get('attendees', [])]
    description = html.unescape(re.sub(r'<[^>]+>', ' ', raw.get('description', '')))
    body = '\n'.join(filter(None, [description, raw.get('location'),
        'Participants: ' + ', '.join(a.get('email', a.get('displayName', '')) for a in attendees)
        if attendees else '']))
    source_url = raw.get('htmlLink', '')
    url = urllib.parse.urlsplit(source_url)
    if url.scheme != 'https' or not (url.hostname == 'calendar.google.com' or
                                    (url.hostname == 'www.google.com' and url.path.startswith('/calendar/'))):
        source_url = ms_graph.web_link(raw.get('webLink'))  # an Outlook event: Outlook on the web
    # An all-day event is a date, not a moment: it starts at midnight on that date in the owner's zone, whatever zone
    # the calendar reports (Outlook's is UTC here), so it stays on its own day on the owner's Calendar and pages.
    zone = str(local_tz()) if 'date' in start else timezone
    metadata = {'start': start, 'end': end, 'end_at': calendar_time(end, zone),
                'all_day': 'date' in start, 'timezone': timezone, 'status': raw.get('status'),
                'updated': raw.get('updated'), 'location': raw.get('location'),
                'organizer': raw.get('organizer'), 'attendees': attendees,
                'recurring_event_id': raw.get('recurringEventId'),
                'original_start': raw.get('originalStartTime'), 'source_url': source_url,
                'ical_uid': raw.get('iCalUID'), 'truncated': len(body) > 40000}
    if account.get('calendar_id', 'primary') != 'primary':
        metadata.update(calendar_id=account['calendar_id'], credential_account=account['email'],
                        access='shared_read_only')
    return {'account_id': account['id'], 'source_id': raw['id'], 'kind': 'calendar.event',
            'occurred_at': calendar_time(start, zone), 'title': raw.get('summary', '(untitled event)')[:1000],
            'body': body[:40000], 'metadata': metadata, 'deleted': raw.get('status') == 'cancelled'}


def calendar_rooms(connect):
    """The Graph's word on meeting rooms, for a meeting's details: addresses that are rooms (graph_resources), the ones
    the owner said are people after all, and the names kept for rooms ({address: name})."""
    try:
        with connect() as db:
            rooms, kept = graph.resources(db), graph.not_resources(db)
            names = {str(r[0])[6:]: r[1] for r in db.execute(
                "SELECT identifier,name FROM graph_resources WHERE resource=1 AND name IS NOT NULL AND identifier LIKE 'email:%' "
                "UNION ALL SELECT node_id,name FROM graph_names WHERE node_id LIKE 'email:%'") if r[1] and '@' not in str(r[1])}
    except sqlite3.OperationalError:
        return set(), set(), {}
    return rooms, kept, names


def calendar_room(attendee, rooms=(), kept=()):
    """Whether a guest on an invite is a meeting room: one the Graph knows is a room, or one whose address or name says so
    (graph.room_like) and that the owner didn't call a person. Google and Outlook flag their own rooms (resource)."""
    email = str(attendee.get('email') or '').strip().lower()
    if attendee.get('self') or not email:
        return False
    return 'email:' + email in rooms or ('email:' + email not in kept and graph.room_like(email, attendee.get('displayName')))


def room_name(attendee, names=None):
    """A booked room's name: the invite's, the one kept for it, or its address made readable ("falconheavy_room" ->
    "Falconheavy room")."""
    email = str(attendee.get('email') or '').strip().lower()
    name = str(attendee.get('displayName') or '').strip()
    if name and '@' not in name:
        return name
    if (names or {}).get(email):
        return str(names[email]).strip()
    if email.endswith('.calendar.google.com'):
        return ''  # a Google room's address is an id, not a name
    local = re.sub(r'[._+-]+', ' ', email.split('@')[0]).strip()
    return local[:1].upper() + local[1:]


def calendar_owned(metadata, owner=()):
    """Whether a meeting is the owner's: on their own calendar, or on one shared with them (someone else's) that
    they organize or are invited to and didn't decline. 'self' on a shared calendar means its owner, not them."""
    if metadata.get('access') != 'shared_read_only':
        return True
    me = {str(e).lower() for e in (*owner, metadata.get('credential_account')) if e}
    if str((metadata.get('organizer') or {}).get('email') or '').lower() in me:
        return True
    return any(isinstance(a, dict) and str(a.get('email') or '').lower() in me and a.get('responseStatus') != 'declined'
               for a in metadata.get('attendees') or [])


def calendar_account_owner(account):
    """Whose a shared calendar is, from its config: calendar_owner, or the name in a display_name like "Sam’s calendar"."""
    name = str(account.get('calendar_owner') or '').strip()
    if not name:
        match = re.fullmatch(r"\s*(\S+?)[’']s calendar\s*", str(account.get('display_name') or ''), re.I)
        name = match[1] if match else ''
    return name[:40] or None


def calendar_owner_name(metadata):
    """The first name of whoever a shared calendar belongs to, for a quiet first-name label."""
    organizer = metadata.get('organizer') or {}
    name = str(organizer.get('displayName') or '').split() if organizer.get('self') else []
    if name:
        return name[0][:40]
    local = re.split(r'[._+\-]', str(metadata.get('calendar_id') or '').split('@')[0])[0]
    return local[:40].capitalize() if local.isalpha() else 'Shared'


def calendar_guests(metadata, owner=()):
    """How many people besides the owner (and, on a shared calendar, its owner) a meeting has: any means it is
    someone's meeting with others, never one The Machine changes."""
    mine = {str(e).lower() for e in (*owner, metadata.get('credential_account'), metadata.get('calendar_id')) if e}
    people = [a for a in metadata.get('attendees') or [] if isinstance(a, dict) and not a.get('self')
              and str(a.get('email') or '').lower() not in mine]
    organizer = metadata.get('organizer') or {}
    other = organizer.get('email') and not organizer.get('self') and str(organizer['email']).lower() not in mine
    return len(people) + (1 if other else 0)


def all_day_span(metadata):
    """An all-day event's (first date, end date exclusive) as ISO dates, or None for a timed one."""
    if not metadata.get('all_day'):
        return None
    start, end = (metadata.get(k) if isinstance(metadata.get(k), dict) else {} for k in ('start', 'end'))
    try:
        first = dt.date.fromisoformat(start.get('date'))
    except (TypeError, ValueError):
        return None
    try:
        until = max(dt.date.fromisoformat(end.get('date')), first + dt.timedelta(days=1))
    except (TypeError, ValueError):
        until = first + dt.timedelta(days=1)
    return first.isoformat(), until.isoformat()


def calendar_edit_times(metadata):
    """(start, end, all_day) as the Calendar form and calendar_writes take them: an all-day event's last day inclusive."""
    start, end, all_day = metadata.get('start') or {}, metadata.get('end') or {}, bool(metadata.get('all_day'))
    if all_day:
        try:
            last = (dt.date.fromisoformat(end.get('date')) - dt.timedelta(days=1)).isoformat()
        except (TypeError, ValueError):
            last = start.get('date')
        return start.get('date'), max(last or '', start.get('date') or ''), True
    return start.get('dateTime'), end.get('dateTime'), False


def calendar_write_events(db, ids, owner=()):
    """What calendar_writes.validate needs about the meetings a change names, by their events id."""
    ids = [i for i in ids if isinstance(i, int) and not isinstance(i, bool)][:20]
    if not ids:
        return {}
    found = {}
    for row in db.execute("SELECT id,account_id,source_id,title,metadata FROM events WHERE kind='calendar.event' AND deleted=0 AND id IN ("
                          + ','.join('?' for _ in ids) + ')', ids):
        m = json.loads(row['metadata'])
        start, end, all_day = calendar_edit_times(m)
        if start and end:
            found[row['id']] = {'account_id': row['account_id'], 'source_id': row['source_id'], 'title': row['title'],
                                'start': start, 'end': end, 'all_day': all_day, 'guests': calendar_guests(m, owner)}
    return found


def company_domains(config):
    """The owner's companies' email domains: those of their Work connections, never a free mail provider's."""
    return sorted({own_addresses.email_domain(a.get('email')) for a in config.get('accounts', [])  # an X handle (@acme) is no domain
                   if str(a.get('boundary') or '').startswith('work:')} - {''} - graph.FREEMAIL)


def team_people(db, query, owner=(), domains=(), teammates=(), limit=8):
    """Teammates to pick by email (Hand off, By email): the owner's Work Fleets' members, then people from the Graph
    on the owner's company domains, then the typed name completed with each domain (bo -> bo@company.com) when no one
    there has that address yet."""
    words = ' '.join(str(query or '').split()).casefold()
    q = words.replace(' ', '')
    if len(q) < 2:
        return []
    mine = {str(e).lower() for e in owner}
    domains = list(dict.fromkeys([*[d for d in domains if d], *[m['email'].rsplit('@', 1)[1] for m in teammates if '@' in m['email']]]))
    domains = [d for d in domains if d not in graph.FREEMAIL]
    found = []
    for m in teammates:
        if m['email'] not in mine and m['email'] not in {p['email'] for p in found} and (q in m['email'] or words in m['name'].casefold()):
            found.append(m)
    found += [p for p in invite_people(db, query, owner, 60) if p['email'].rsplit('@', 1)[1] in domains and p['email'] not in {f['email'] for f in found}]
    found = found[:limit]
    local, at, part = q.partition('@')
    if ' ' not in words and re.fullmatch(r"[a-z0-9][a-z0-9._+'-]{1,63}", local or ''):
        for domain in domains:
            email = local + '@' + domain
            if domain.startswith(part) and email not in {p['email'] for p in found} and email not in mine:
                found.append({'name': '', 'email': email})
    return found[:limit]


def invite_people(db, query, owner=(), limit=8):
    """People from the Graph to invite: a name and an address, the strongest first, matching the typed words."""
    q = ' '.join(str(query or '').split()).casefold()
    if len(q) < 2:
        return []
    like = '%' + q.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%'
    try:
        rows = db.execute("SELECT name,info FROM graph_nodes WHERE kind='person' AND (lower(name) LIKE ? ESCAPE '\\' OR lower(info) LIKE ? ESCAPE '\\') "
                          'ORDER BY strength DESC LIMIT 60', (like, like)).fetchall()
    except sqlite3.OperationalError:
        return []
    found, seen = [], {str(e).lower() for e in owner}
    for name, info in rows:
        try:
            ids = json.loads(info or '{}').get('identifiers') or []
        except ValueError:
            continue
        emails = [i.split(':', 1)[1].lower() for i in ids if isinstance(i, str) and i.startswith('email:')]
        emails = [e for e in emails if calendar_writes.EMAIL.fullmatch(e) and not graph.bulk(e) and not graph.relay(e)]
        named = q in str(name).casefold()
        for email in sorted(emails, key=lambda e: q not in e)[:1 if named else 2]:
            if email not in seen and (named or q in email):
                seen.add(email)
                found.append({'name': ' '.join(str(name).split())[:80] if '@' not in str(name) else '', 'email': email})
        if len(found) >= limit:
            break
    return found[:limit]


def calendar_write_ids(value):
    """The event ids that calendar changes in a next action (or a list of them) name."""
    items = value if isinstance(value, list) else [value]
    return [i.get('event') for i in items if isinstance(i, dict) and i.get('kind') == 'calendar']


def calendar_keys(metadata, title, start, end):
    """What makes two copies of one meeting (on the owner's calendar and a shared one, or two invites) the same."""
    keys = {('when', start, metadata.get('end_at') or end, ' '.join(str(title).split()).casefold())}
    if metadata.get('ical_uid'):
        keys.add(('uid', metadata['ical_uid'], start))
    eid = urllib.parse.parse_qs(urllib.parse.urlsplit(str(metadata.get('source_url') or '')).query).get('eid', [''])[0]
    try:
        event = base64.urlsafe_b64decode(eid + '=' * (-len(eid) % 4)).decode().split(' ')[0] if eid else ''
    except (ValueError, UnicodeDecodeError):
        event = ''
    if event:
        keys.add(('event', event))
    return keys


def sync_calendar(store, config, account):
    source = Calendar(config, account)
    profile = source.profile()  # Only this explicitly configured calendar.
    timezone = profile.get('timeZone', str(local_tz()))
    state = store.checkpoint(account['id']) or {}
    current = dt.datetime.fromisoformat(now())
    outlook_read = {'outlook_read': ms_graph.CALENDAR_READ} if account.get('service') == 'outlook_calendar' else {}  # older read: again
    if not state or (state.get('mode') == 'incremental' and not state.get('page_token') and
                     current >= dt.datetime.fromisoformat(state['refresh_at'])) or (
            outlook_read and state.get('outlook_read') != ms_graph.CALENDAR_READ and not state.get('page_token')):
        # Refresh the rolling window daily so unchanged recurring occurrences enter it.
        state = {'mode': 'bootstrap', 'time_min': (current - dt.timedelta(days=CALENDAR_BACK_DAYS)).isoformat(),
                 'time_max': (current + dt.timedelta(days=30)).isoformat(), 'seen': [],
                 'refresh_at': (current + dt.timedelta(days=1)).isoformat(), **outlook_read}
        store.commit_page(account['id'], state, [], record_sync=False)
    params = {'singleEvents': True, 'showDeleted': True, 'maxResults': 100}
    if state['mode'] == 'incremental':
        params['syncToken'] = state['sync_token']
    else:
        params.update(timeMin=state['time_min'], timeMax=state['time_max'])
    if state.get('page_token'):
        params['pageToken'] = state['page_token']
    try:
        page = source.get('events.list', params)
    except SourceError as error:
        if error.status == 410 and state['mode'] == 'incremental':
            replacement = {k: v for k, v in state.items() if k not in ('sync_token', 'page_token')}
            replacement.update(mode='resync', seen=[], resync_reason='expired_sync_token')
            store.commit_page(account['id'], replacement, [], record_sync=False)
            return {'mode': 'resync', 'events': 0}
        if error.status == 400 and state.get('page_token'):
            state.pop('page_token')
            if state['mode'] != 'incremental':
                state['seen'] = []
            store.commit_page(account['id'], state, [], record_sync=False)
        raise
    events, seen, excluded = [], set(state.get('seen', [])), []
    skipped = Skips('calendar_invalid_event')  # an event it can't take is counted, never failing the page
    def one(raw):
        seen.add(raw['id'])  # seen even when it can't be read, so a complete window never removes it as absent
        if raw.get('unreadable'):  # an Outlook event ms_graph.calendar_item couldn't put in Google's shape
            raise SourceError(str(raw['unreadable']))
        if calendar_title_excluded(account, raw.get('summary')):
            excluded.append(raw['id'])
            return None
        if raw.get('status') == 'cancelled':
            e = store.tombstone(account['id'], raw['id'])
            if e:
                e['metadata']['status'] = 'cancelled'
            return e
        e = calendar_event(account, raw, timezone)
        # Incremental requests cannot use time bounds. Ignore new distant events,
        # but retain updates to already collected occurrences, even when moved out.
        existing = store.tombstone(account['id'], raw['id'])
        if not existing and not (e['occurred_at'] < state['time_max'] and
                                 e['metadata']['end_at'] > state['time_min']):
            return None
        return e
    events = [e for e, _ in skipped.every(page.get('items', []), one) if e]
    next_state = dict(state)
    if page.get('nextPageToken'):
        next_state['page_token'] = page['nextPageToken']
        if state['mode'] != 'incremental':
            next_state['seen'] = sorted(seen)
    else:
        if not page.get('nextSyncToken'):
            raise SourceError('missing_sync_token')
        if state['mode'] != 'incremental':
            # Only a COMPLETE window scan can establish absence. Never prune a partial
            # scan or clear historical evidence on expired tokens.
            with store.connect() as db:
                old = db.execute("SELECT source_id,occurred_at,metadata FROM events WHERE account_id=? AND kind='calendar.event' AND deleted=0",
                                 (account['id'],)).fetchall()
            for row in old:
                metadata = json.loads(row['metadata'])
                if (row['source_id'] not in seen and row['occurred_at'] < state['time_max'] and
                        metadata['end_at'] > state['time_min']):
                    e = store.tombstone(account['id'], row['source_id'])
                    e['metadata']['removal_reason'] = 'absent_from_complete_window'
                    events.append(e)
        next_state.update(mode='incremental', sync_token=page['nextSyncToken'])
        next_state.pop('page_token', None)
        next_state.pop('seen', None)
    skipped.check().note(next_state)
    store.commit_page(account['id'], next_state, events, excluded_source_ids=excluded)
    return {'mode': next_state['mode'], 'events': len(events), 'filtered': len(excluded), 'skipped': sum(skipped.values())}


def event_start(rows):
    """The start of the first timed calendar event among a card's evidence (in its order), as UTC; None without one."""
    for row in rows:
        if row['kind'] != 'calendar.event':
            continue
        try:
            meta = json.loads(row['metadata'] or '{}')
            if meta.get('status') == 'cancelled' or not (meta.get('start') or {}).get('dateTime'):
                continue
            return calendar_time(meta['start'], meta.get('timezone') or str(local_tz()))
        except (ValueError, TypeError, KeyError, AttributeError):
            continue
    return None


def expiry_moment(at, what, rows=()):
    """(expires_at as UTC, expires_what) for a card whose whole point is a moment: an ISO time (its offset, or the
    owner's time zone without one) or a day (its end). When the card's evidence has a calendar event, its start is the
    moment, whatever time the review wrote: the calendar is the truth. Raises for a moment that already passed."""
    what = ' '.join(str(what or '').split())
    at = event_start(rows) or at
    if not at or not what or len(what) > 80:
        raise ValueError('expires_at (the moment, e.g. 2026-10-28T13:30+01:00) goes with expires_what (what it is, '
                         'in a few words: "the meeting with Sam")')
    try:
        text = str(at)
        moment = (dt.datetime.combine(dt.date.fromisoformat(text), dt.time(23, 59)) if len(text) == 10
                  else dt.datetime.fromisoformat(text))
    except ValueError:
        raise ValueError('expires_at is an ISO time with its offset, like 2026-10-28T13:30+01:00, or a day') from None
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=local_tz())
    moment = moment.astimezone(dt.timezone.utc)
    if moment.isoformat() <= now():
        raise ValueError('That moment has passed already, so this to-do is not needed')
    return moment.isoformat(timespec='seconds'), undated_card(what)[0][0]


CALENDAR_BACK_DAYS = 7
