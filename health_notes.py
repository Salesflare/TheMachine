"""Health notes (docs/help/notes.md, "Health"): what the owner's Machine knows about the owner's own health, in a few
notes under Health, kept the way every kind in sections is (section_notes.py: one small model call over what is new
only, the owner's own notes in a part filled in, a part only from two lines).

Each line points to where the thing lives instead of copying it: an appointment's line opens it in the calendar, a
bill's opens its to-do and mail (its amount and payment details stay there), a line from what The Machine learned is
that fact.

Candidates, in plain code: appointments (calendar events within LOOK_BACK days before and LOOK_AHEAD after today that
only the owner is on, not canceled or declined, one per name: its next time, else its last), bills from any payee,
subscriptions the owner didn't cancel, and what The Machine learned that is about no one in the Graph. Health is
always Personal, whatever the account it came in on: a doctor's bill sent to a work address is still the owner's own.
The notes are never shared."""
import datetime as dt
import json

from i18n import t
import section_notes

# The parts of the owner's health a candidate can be about, each a note under Health (English: its key; titled in the
# owner's language through i18n)
SECTIONS = ('Appointments', 'Doctors and care', 'Medicines', 'Allergies and conditions', 'Bills and insurance')
PARTS = {
    'Appointments': 'a visit to a doctor, dentist, physiotherapist, therapist, optician, a test or a vaccination',
    'Doctors and care': 'who takes care of the owner\'s health: their doctor, dentist, practice or hospital, and how to reach them',
    'Medicines': 'a medicine or supplement the owner takes, a prescription, a pharmacy',
    'Allergies and conditions': 'an allergy, a condition, a blood type, something a doctor or nurse should know',
    'Bills and insurance': 'a bill or subscription for care: a doctor, dentist, hospital or pharmacy bill, health insurance',
}
LOOK_BACK = 400
LOOK_AHEAD = 120
NAME_MAX = 120


def _others(meta, mine):
    """Whether someone besides the owner is on a calendar event (a booked room doesn't count)."""
    for a in meta.get('attendees') or ():
        if isinstance(a, dict):
            if not a.get('self') and not a.get('resource') and a.get('email') and str(a['email']).casefold() not in mine:
                return True
        elif isinstance(a, str) and a.strip() and a.strip().casefold() not in mine:
            return True
    return False


def _declined(meta):
    return any(isinstance(a, dict) and a.get('self') and a.get('responseStatus') == 'declined' for a in meta.get('attendees') or ())


def appointments(db, accounts, today):
    """The owner's own calendar events, one per name: [{key, name, count, at, coming, event_id}], its next time if
    there is one, else its last."""
    mine = {str(a.get('email') or '').casefold() for a in accounts} - {''}
    ids = [a['id'] for a in accounts if a.get('id')]
    if not ids:
        return []
    start = (today - dt.timedelta(days=LOOK_BACK)).isoformat()
    end = (today + dt.timedelta(days=LOOK_AHEAD + 1)).isoformat()
    now = today.isoformat()
    found = {}
    for r in db.execute(f"SELECT id,title,occurred_at,metadata FROM events WHERE kind='calendar.event' AND deleted=0 "
                        f"AND account_id IN ({','.join('?' * len(ids))}) AND occurred_at>=? AND occurred_at<? ORDER BY occurred_at,id",
                        [*ids, start, end]):
        try:
            meta = json.loads(r['metadata'] or '{}')
        except ValueError:
            continue
        name = ' '.join(str(r['title'] or '').split())[:NAME_MAX]
        if not name or not isinstance(meta, dict) or meta.get('status') == 'cancelled' or _declined(meta) or _others(meta, mine):
            continue
        day = str(r['occurred_at'])[:10]
        c = found.setdefault(name.casefold(), {'key': 'appt:' + section_notes.key_of(name.casefold()), 'name': name, 'count': 0})
        c['count'] += 1
        if day < now or not c.get('coming'):  # the last one before today, until the first one from today on
            c.update(at=day, coming=day >= now, event_id=r['id'])
    return sorted(found.values(), key=lambda c: c['at'], reverse=True)


def candidates(db, accounts, today):
    return [*appointments(db, accounts, today), *section_notes.bills(db, accounts, today, personal=False),
            *section_notes.subscriptions(db, accounts, personal=False), *section_notes.facts(db, accounts, personal=False)]


def ask(c):
    if c['key'].startswith('appt:'):
        return {'kind': 'calendar', 'name': c['name'], 'times': c['count']}
    return section_notes.ask(c)


def line(db, c):
    if c['key'].startswith('appt:'):  # at: its next day, else its last
        said = t('{}: coming up', c['name']) if c['coming'] else t('{}: last time', c['name'])
        return {'key': c['key'], 'item': 'appointment', 'text': said, 'at': c['at'], 'event_id': c['event_id']}
    return section_notes.line(db, c)


KIND = section_notes.Kind(
    'health', 'Health', SECTIONS, PARTS, 'the owner\'s own health',
    'the home, work, a hobby or a sport, a trip, a meeting, someone else\'s health, like a child\'s or a parent\'s',
    candidates, ask, line)
