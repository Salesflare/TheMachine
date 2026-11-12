"""Reconnect to add something: an account signed in before a newer feature asked for more (Google contacts, for their
photos). One ask per account and feature, said in one line with why: on that connection's card and as a row of the
setup to-do (setup_card.py), both closed for good by either ×, which is the setup row's own milestone (setup:hint-<id>).
It goes by itself once the sign-in has what the feature needs. Never a push, an email or a to-do of its own.

Whoever finds out what a sign-in lacks notes it here (note): the enrichment worker for Google contacts
(workers.google_contacts_run) and for Outlook's colleague and contact photos (ms_photos.check). A new kind of ask is a key with its sentence in `reason`."""
from __future__ import annotations

import hashlib
import sqlite3

import i18n

GOOGLE_CONTACTS = 'google-contacts'
OUTLOOK_PHOTOS = 'outlook-photos'


def reason(ask):
    """The ask's one line in the owner's language: what reconnecting brings, never a bare "Reconnect"."""
    return {GOOGLE_CONTACTS: i18n.t('Reconnect Google to show your contacts’ photos.'),
            OUTLOOK_PHOTOS: i18n.t('Reconnect Outlook to show your colleagues’ and contacts’ photos.')}.get(ask, '')


def ensure(db):
    db.execute('CREATE TABLE IF NOT EXISTS reconnect_asks(account TEXT NOT NULL, ask TEXT NOT NULL, since TEXT NOT NULL, '
               'checked_at TEXT NOT NULL, PRIMARY KEY(account, ask))')


def note(db, account, ask, missing, at):
    """What a check of the account's sign-in found: `missing` keeps (or starts) the ask, else it goes."""
    ensure(db)
    if missing:
        db.execute('INSERT INTO reconnect_asks(account,ask,since,checked_at) VALUES(?,?,?,?) '
                   'ON CONFLICT(account,ask) DO UPDATE SET checked_at=excluded.checked_at', (account, ask, at, at))
    else:
        db.execute('DELETE FROM reconnect_asks WHERE account=? AND ask=?', (account, ask))


def signed_in_again(db, account, ask, changed_at):
    """Whether an open ask's account was signed in again (its sign-in changed at `changed_at`) since it was last checked:
    worth checking again now, instead of the next day."""
    ensure(db)
    row = db.execute('SELECT checked_at FROM reconnect_asks WHERE account=? AND ask=?', (account, ask)).fetchone()
    return bool(row and changed_at and changed_at > row[0])


def hint_id(account, ask):
    """The setup to-do's row id ([a-z0-9-], at most 40), which the card's × closes too."""
    return f'reconnect-{ask}-' + hashlib.sha256(str(account).encode()).hexdigest()[:8]


def open_asks(store, config):
    """{account id: [{id, reason}]} of the owner's own accounts still in config whose ask wasn't closed."""
    own = {a['id'] for a in config.get('accounts') or [] if isinstance(a, dict) and a.get('id') and not a.get('shared')}
    try:
        with store.connect() as db:
            ensure(db)
            rows = db.execute('SELECT account,ask FROM reconnect_asks ORDER BY since').fetchall()
            closed = {r[0][len('setup:hint-'):] for r in db.execute("SELECT name FROM milestones WHERE name LIKE 'setup:hint-reconnect-%'")}
    except sqlite3.Error:
        return {}
    out = {}
    for account, ask in rows:
        line, key = reason(ask), hint_id(account, ask)
        if account in own and line and key not in closed:
            out.setdefault(account, []).append({'id': key, 'reason': line})
    return out


def hints(asks):
    """The setup to-do's rows for open asks (open_asks): Reconnect does what the card's Reconnect does (reconnect: its
    account)."""
    return [{'id': ask['id'], 'title': ask['reason'], 'text': '', 'button': i18n.t('Reconnect'), 'reconnect': {'account': account}}
            for account, items in asks.items() for ask in items]
