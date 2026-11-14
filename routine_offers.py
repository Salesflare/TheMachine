"""Offers to turn on a mail cleanup template (docs/help/routines.md#templates): when a lot of newsletters come in, or
the owner moves a lot of mail to spam by hand, one calm line above the to-dos says how much this week and offers the
template (routine_templates.py) that would sort it: Newsletter cleanup or Spam cleanup.

Plain code, no model: the counts are what the templates' own code already reads (mail_cleanup.newsletter_count, the
same test Newsletter cleanup lists by; mail_cleanup.marks_count, the owner's own spam marks Spam cleanup learns from),
over the past WEEK. Quality or nothing: below the bar there is no offer, and an open one that no longer holds goes away.

Each template is offered at most once: Turn it on adds the template's routine as Templates' Add does (it runs once now;
nothing is sent, unsubscribed or moved until the owner confirms on its to-do), No thanks never offers it again, and a
template the owner ever had (on, paused or stopped) is never offered. One offer shows at a time, and the "Make this a recurring to-do?"
offer (recurring.py) goes first.

Table (this module owns it): routine_offers, one row per template: its count, open, added or declined."""
import datetime as dt

import i18n
import routine_templates
from machine.owner_error import OwnerError

WEEK = dt.timedelta(days=7)
NEWSLETTERS_MIN = 25  # newsletters in a week: more than three a day
SENDERS_MIN = 5  # from this many senders, so one chatty list isn't "a lot of newsletters"
SPAM_MIN = 5  # mails moved to spam by hand in a week
LOOK_EVERY = 6 * 3600  # seconds between looks: the count is for the week, so a few times a day is plenty
KEYS = ('newsletters', 'spam')  # the order they are offered in
STATES = ('open', 'added', 'declined')


def ensure(db):
    db.execute('CREATE TABLE IF NOT EXISTS routine_offers(key TEXT PRIMARY KEY,n INTEGER NOT NULL,status TEXT NOT NULL DEFAULT \'open\','
               'created_at TEXT NOT NULL,updated_at TEXT NOT NULL,decided_at TEXT)')


def had(db, key):
    """The owner has, or once had, this template's routine (on, paused or stopped): it is theirs to decide on there."""
    return bool(db.execute('SELECT 1 FROM routines WHERE origin=? LIMIT 1', ('template:' + key,)).fetchone())


def worth(key, counts):
    """The week's count when it clears the bar, else 0. counts: {'newsletters': (mails, senders), 'spam': mails}."""
    if key == 'newsletters':
        n, senders = counts.get(key) or (0, 0)
        return n if n >= NEWSLETTERS_MIN and senders >= SENDERS_MIN else 0
    n = counts.get(key) or 0
    return n if n >= SPAM_MIN else 0


def count(db, accounts, mark_accounts, now):
    """This week's counts: newsletters as (mails, senders) in the owner's mail accounts, and the owner's own spam marks in
    the accounts Spam cleanup reads (mark_accounts)."""
    import mail_cleanup  # its tables and tests; imported here so the dashboard's status never needs it
    mail_cleanup.ensure(db)
    since = (now - WEEK).isoformat()
    return {'newsletters': mail_cleanup.newsletter_count(db, accounts, since) if accounts else (0, 0),
            'spam': mail_cleanup.marks_count(db, mark_accounts, WEEK.days) if mark_accounts else 0}


def look(db, counts, stamp):
    """Keep the offers in step with this week's counts: open (or update the number of) one that clears the bar, drop an
    open one that no longer does. Added and declined ones stay as they are."""
    ensure(db)
    for key in KEYS:
        if key not in counts:
            continue
        n = 0 if had(db, key) else worth(key, counts)
        row = db.execute('SELECT status FROM routine_offers WHERE key=?', (key,)).fetchone()
        if row and row[0] != 'open':
            continue
        if n:
            db.execute('INSERT INTO routine_offers(key,n,created_at,updated_at) VALUES(?,?,?,?) '
                       'ON CONFLICT(key) DO UPDATE SET n=excluded.n,updated_at=excluded.updated_at', (key, n, stamp, stamp))
        elif row:
            db.execute("DELETE FROM routine_offers WHERE key=? AND status='open'", (key,))


def is_open(db, key):
    ensure(db)
    return key in KEYS and bool(db.execute("SELECT 1 FROM routine_offers WHERE key=? AND status='open'", (key,)).fetchone())


def answer(db, key, yes, stamp):
    """The owner's Turn it on or No thanks: never offered again either way. ValueError when it isn't open."""
    if not is_open(db, key):
        raise OwnerError('That suggestion is gone')
    db.execute('UPDATE routine_offers SET status=?,decided_at=? WHERE key=?', ('added' if yes else 'declined', stamp, key))


def view(db):
    """The one open offer the To-dos page shows, or None: {key, n, name, what}, in the owner's language. Not for a
    template the owner has turned on meanwhile (Templates' Add)."""
    try:
        rows = {r[0]: r[1] for r in db.execute("SELECT key,n FROM routine_offers WHERE status='open'")}
        key = next((k for k in KEYS if rows.get(k) and not had(db, k)), None)
    except Exception:  # no table yet: nothing offered
        return None
    if not key:
        return None
    t = routine_templates.TEMPLATES[key]
    return {'key': key, 'n': rows[key], 'name': i18n.t(t['name']), 'what': i18n.t(t['what'])}
