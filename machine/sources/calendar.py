"""What a calendar event's metadata says: whose meeting it is, who else is in it, its room and its all-day span.
Plain reads of the metadata the calendar sources store (assistant.calendar_event), used by the Calendar, reviews and
meeting writes."""
import datetime as dt
import re


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
