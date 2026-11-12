"""Reconnect to add something: an account signed in before a newer feature asked for more (Google contacts, for their
photos), now that its sign-in service offers it. One to-do per account and feature in For you, in the account's area:
Reconnect leads and opens that account's sign-in; it closes itself as done once the sign-in has what the feature needs,
and Not needed closes it for good. Created once, never again, and never pushed or mailed: it waits on the dashboard.

Whoever finds out what a sign-in lacks notes it here (note), only for what its sign-in service offers now (a broker's
`offered`), so nothing asks before the service can grant it: the enrichment worker for Google contacts
(workers.google_contacts_run), and for Outlook's colleague and contact photos (ms_photos.check). The worker then makes the to-dos (todos). A new kind of ask is a key with its title and
summary in TITLES and summary()."""
from __future__ import annotations

import sqlite3

import i18n
from machine.store.machine_cards import RECONNECT_KIND, reconnect_source, reconnected

GOOGLE_CONTACTS = 'google-contacts'
OUTLOOK_PHOTOS = 'outlook-photos'
PROVIDERS = {GOOGLE_CONTACTS: 'google', OUTLOOK_PHOTOS: 'microsoft'}  # the hosted sign-in its Reconnect opens (the dashboard's data-hosted-reconnect)


def title(ask):
    """The to-do's title in the owner's language: what reconnecting brings, never a bare "Reconnect"."""
    return {GOOGLE_CONTACTS: i18n.t('Reconnect Google to show your contacts’ photos'),
            OUTLOOK_PHOTOS: i18n.t('Reconnect Microsoft to show your colleagues’ and contacts’ photos')}.get(ask, '')


def summary(ask, email):
    """The to-do's one line under its title: which account, and why."""
    return {GOOGLE_CONTACTS: i18n.t('{} was connected before your Machine read contacts. Reconnect it to add their photos, read-only.',
                                    email),
            OUTLOOK_PHOTOS: i18n.t('{} was connected before your Machine read colleagues and contacts. Reconnect it to add their photos, read-only.',
                                   email)}.get(ask, '')


def ensure(db):
    db.execute('CREATE TABLE IF NOT EXISTS reconnect_asks(account TEXT NOT NULL, ask TEXT NOT NULL, since TEXT NOT NULL, '
               'checked_at TEXT NOT NULL, PRIMARY KEY(account, ask))')


def note(db, account, ask, missing, at):
    """What a check of the account's sign-in found: `missing` (what its service offers and it lacks) keeps or starts the
    ask; nothing missing ends it, and its open to-do closes itself as done."""
    ensure(db)
    if missing:
        db.execute('INSERT INTO reconnect_asks(account,ask,since,checked_at) VALUES(?,?,?,?) '
                   'ON CONFLICT(account,ask) DO UPDATE SET checked_at=excluded.checked_at', (account, ask, at, at))
        return
    db.execute('DELETE FROM reconnect_asks WHERE account=? AND ask=?', (account, ask))
    reconnected(db, account, ask, at)


def signed_in_again(db, account, ask, changed_at):
    """Whether an open ask's account was signed in again (its sign-in changed at `changed_at`) since it was last checked:
    worth checking again now, instead of the next day."""
    ensure(db)
    row = db.execute('SELECT checked_at FROM reconnect_asks WHERE account=? AND ask=?', (account, ask)).fetchone()
    return bool(row and changed_at and changed_at > row[0])


def todos(store, config):
    """A to-do for each open ask of the owner's own accounts still here (never one shared from a Fleet), once ever per
    account and ask (Store.machine_card): one closed as done or Not needed never comes back. Returns how many are new."""
    own = {a['id']: a for a in config.get('accounts') or [] if isinstance(a, dict) and a.get('id') and not a.get('shared')}
    try:
        with store.connect() as db:
            ensure(db)
            rows = db.execute('SELECT r.account,r.ask FROM reconnect_asks r WHERE NOT EXISTS(SELECT 1 FROM events e WHERE e.kind=? '
                              "AND e.source_id='reconnect:'||r.ask||':'||r.account) ORDER BY r.since", (RECONNECT_KIND,)).fetchall()
    except sqlite3.Error:
        return 0
    made = 0
    for account_id, ask in rows:
        account, provider = own.get(account_id), PROVIDERS.get(ask)
        if not account or not provider or not title(ask):
            continue
        email = str(account.get('email') or '')
        made += store.machine_card(account_id, RECONNECT_KIND, reconnect_source(account_id, ask), title(ask), summary(ask, email),
                                   summary(ask, email), {'ask': ask, 'provider': provider, 'email': email}, quiet=True)
    return made
