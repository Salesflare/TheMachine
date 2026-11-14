"""The Calendar's actions, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

New event and edit (calendar_write), a meeting's notes (meeting_notes) and Generate notes (meeting_notes_write). The
methods they call (calendar_write, meeting_notes, meeting_write and its worker) stay in assistant.py for now: they use
the hours, model and source helpers (now, local_tz, has_model, gog_read, ...), which move out of assistant.py first.

Where the Calendar starts (calendar_starts): a calendar's first read goes CALENDAR_BACK_DAYS back from when it was
connected (assistant.sync_calendar). Later reads roll on, and what came in stays, so nothing before that day is there.
Once every calendar's history is in (machine/app/history.py, a year back by default), the Calendar starts where that
history does."""
import datetime as dt
import sqlite3

from machine.store import history

from timeutil import local_tz
from machine.sources.calendar import (
    CALENDAR_BACK_DAYS,
)
from machine.owner_error import OwnerError

CALENDARS = ('calendar', 'outlook_calendar', 'icloud_calendar', 'caldav', 'proton_calendar', 'ics', 'exchange')  # assistant.CALENDAR_SERVICES


def _when(value):
    """An ISO time or a bare (UTC) day as an aware datetime, None when it is neither."""
    try:
        at = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except ValueError:
        return None
    return at if at.tzinfo else at.replace(tzinfo=dt.timezone.utc)


class CalendarApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {
        'calendar_write': 'calendar_write_action',
        'meeting_notes': 'meeting_notes_action',
        'meeting_notes_write': 'meeting_notes_write_action',
    }

    def calendar_write_action(self, name, args, owner_dashboard):
        # the Calendar's New event and edit form: the owner's own tap, from the dashboard only
        if not owner_dashboard:
            raise OwnerError('Calendar changes come from your tap in the dashboard')
        return self.calendar_write(args)

    def meeting_notes_action(self, name, args, owner_dashboard):
        return self.meeting_notes(args, owner_dashboard)

    def meeting_notes_write_action(self, name, args, owner_dashboard):
        # Generate notes on a meeting in the Calendar (meeting_writer.py)
        if not owner_dashboard:
            raise OwnerError('Only the owner asks for notes to be written, in the Calendar')
        return self.meeting_write(args)

    def calendar_starts(self):
        """The first day the Calendar has meetings for: {'day': its local date, 'joined': True when that calendar came
        with the Machine's start, so the day is a week before the owner joined}. From the first successful read of the
        earliest connected calendar (sync history, kept as daily counts after 30 days). None before any calendar read."""
        ids = [a['id'] for a in self.config.get('accounts') or [] if a.get('service') in CALENDARS]
        if not ids:
            return None
        marks = ','.join('?' for _ in ids)
        reads = [f"SELECT MIN(at) FROM sync_activity WHERE status='success' AND account_id IN ({marks})",
                 f'SELECT MIN(day) FROM sync_daily WHERE syncs>failed AND account_id IN ({marks})']
        found = []
        with self.store.connect() as db:
            older, coming = history.calendar_start(db, ids), history.calendar_coming(db, ids)
            for read in reads:
                try:
                    found.append(db.execute(read, ids).fetchone()[0])
                except sqlite3.OperationalError:  # no daily counts yet
                    pass
        first = min((w for w in map(_when, filter(None, found)) if w), default=None)
        if not first or coming:  # no edge while older meetings still come in: they land before it
            return None
        started = _when(self.started_at() or '')
        day = (first - dt.timedelta(days=CALENDAR_BACK_DAYS)).astimezone(local_tz()).date().isoformat()
        if older and older < day:  # its history reaches further back
            return {'day': older, 'joined': False, 'history': True}
        return {'day': (first - dt.timedelta(days=CALENDAR_BACK_DAYS)).astimezone(local_tz()).date().isoformat(),
                'joined': bool(started and abs(first - started) <= dt.timedelta(days=2))}
