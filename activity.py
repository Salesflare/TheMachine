"""Daily activity counts for the hosted health report: how the owner keeps using The Machine after onboarding.

Plain integers per local day, the last DAYS days, nothing else: never a to-do's title, a name, an address, a subject or
an id. The control plane keeps them next to the setup milestones (first_cards_report) to see whether new owners come
back and get things done.

Per day:
- shown: to-dos on the dashboard's list the owner had open (distinct)
- opened: to-dos the owner opened on the dashboard (distinct)
- do_it: Do it pressed (and Do the next step)
- send: Send pressed
- sent: emails and messages the outbox delivered
- done: Mark done
- dismissed: Not needed
- snoozed: snoozed
- chat: Change and chat messages
- visits: dashboard page loads
- active_hours: hours with the dashboard open (distinct)

Counted from what the app keeps anyway (decisions, the outbox) plus a small local table of distinct marks (seen) for
what it does not: which to-dos were on screen or opened, page loads and active hours. Those marks hold an id only
locally, for counting each once, and are dropped after KEEP_DAYS. Telegram presses count too; shown and opened are the
dashboard's."""
from __future__ import annotations

import datetime as dt
import uuid

DAYS = 7
KEEP_DAYS = 8
SEEN = ('shown', 'opened', 'visits', 'active_hours')
# Owner presses, by the decision they record
CHOICES = {'accept': 'do_it', 'prepare_next': 'do_it', 'send': 'send', 'complete': 'done', 'reject': 'dismissed',
           'snooze': 'snoozed', 'other': 'chat'}
OWNER_SOURCES = ('dashboard', 'telegram')
SEND_KINDS = ('email', 'linkedin', 'slack', 'x', 'whatsapp', 'telegram', 'intercom', 'doc_reply')
KINDS = ('shown', 'opened', 'do_it', 'send', 'sent', 'done', 'dismissed', 'snoozed', 'chat', 'visits', 'active_hours')
SHOWN = "status IN ('pending','accepted','instructions','prepared') AND (deliver_after IS NULL OR deliver_after<=?)"


def ensure(db):
    db.execute('CREATE TABLE IF NOT EXISTS activity_seen(day TEXT NOT NULL,kind TEXT NOT NULL,ref TEXT NOT NULL,PRIMARY KEY(day,kind,ref))')


def local(stamp, tz):
    return dt.datetime.fromisoformat(stamp).astimezone(tz)


def note(db, kind, refs, at, tz):
    """Mark refs (distinct per day) for one of SEEN at `at` (ISO, UTC). Drops marks older than KEEP_DAYS."""
    day = local(at, tz).date().isoformat()
    db.executemany('INSERT OR IGNORE INTO activity_seen(day,kind,ref) VALUES(?,?,?)', [(day, kind, str(r)) for r in refs])
    db.execute('DELETE FROM activity_seen WHERE day<?', ((local(at, tz).date() - dt.timedelta(days=KEEP_DAYS)).isoformat(),))


def note_dashboard(db, at, tz):
    """The dashboard asked for its list: the to-dos it shows and this hour as active."""
    ids = [r[0] for r in db.execute('SELECT id FROM suggestions WHERE ' + SHOWN, (at,))]
    note(db, 'shown', ids, at, tz)
    note(db, 'active_hours', [local(at, tz).strftime('%H')], at, tz)


def note_visit(db, at, tz):
    note(db, 'visits', [uuid.uuid4().hex], at, tz)


def note_opened(db, suggestion_id, at, tz):
    if suggestion_id:
        note(db, 'opened', [suggestion_id], at, tz)


def report(db, tz, current):
    """{'days': [{'day': 'YYYY-MM-DD', <kind>: int, ...}, ...]}: the last DAYS local days up to today, oldest first."""
    today = local(current, tz).date()
    days = [(today - dt.timedelta(days=n)).isoformat() for n in range(DAYS - 1, -1, -1)]
    counts = {day: dict.fromkeys(KINDS, 0) for day in days}
    since = (dt.datetime.combine(today - dt.timedelta(days=DAYS), dt.time(), tz)).astimezone(dt.timezone.utc).isoformat()
    tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}

    def add(stamp, kind):
        try:
            day = local(stamp, tz).date().isoformat()
        except (TypeError, ValueError):
            return
        if day in counts:
            counts[day][kind] += 1
    if 'decisions' in tables:
        for choice, at in db.execute('SELECT choice,created_at FROM decisions WHERE created_at>=? AND source IN (%s) AND choice IN (%s)'
                                     % (','.join('?' * len(OWNER_SOURCES)), ','.join('?' * len(CHOICES))), (since, *OWNER_SOURCES, *CHOICES)):
            add(at, CHOICES[choice])
    if 'action_jobs' in tables:
        for (at,) in db.execute("SELECT updated_at FROM action_jobs WHERE status='sent' AND updated_at>=? AND json_extract(payload,'$.kind') IN (%s)"
                                % ','.join('?' * len(SEND_KINDS)), (since, *SEND_KINDS)):
            add(at, 'sent')
    if 'activity_seen' in tables:
        for day, kind, n in db.execute('SELECT day,kind,count(*) FROM activity_seen WHERE day>=? GROUP BY day,kind', (days[0],)):
            if day in counts and kind in SEEN:
                counts[day][kind] = n
    return {'days': [{'day': day, **counts[day]} for day in days]}
