"""The setup to-do's one suggestion for an owner whose first weeks bring few to-dos (dashboard/setup-card.js,
setup_card.nudge): a row with its reason that leads the card, which its folded line says too. "Try WhatsApp again? The
code ran out.", "Connect WhatsApp? 5 emails mention it.", "Add your other address too? Mail to it shows up here.",
"Connect Slack? 4 emails from Slack this month."

When: in the owner's first DAYS days, on a day with at most QUIET_TODOS new to-dos so far. Which: the first of these
that has a signal, all worked out on this Machine from what it already has:
- retry: a connect that failed and isn't connected since: on the setup page (its hosting agent leaves a note without
  text in the Needs you file, `connect_failed`) or on this dashboard (Connections, + Add: a session that failed);
- whatsapp (hosted, where WhatsApp signs in): ENOUGH or more emails from people in DAYS days with a WhatsApp link
  (wa.me, chat.whatsapp.com) or that name WhatsApp;
- account (hosted): an address of the owner's own (own_addresses.yours) that no connected mailbox brings mail from;
- slack, teams: Connections' Suggested for you counts (machine/sources/suggest.py).
Never without a signal, one at a time, at most one new one a day (milestone setup_nudge: when it was picked, and which),
closed for good with its × (setup:hint-nudge-<id>, as any row), and only on the dashboard: never by email or push.
Its line says a count at most, never a message's text, an address or a name."""
from __future__ import annotations

import datetime as dt
import json
import re
import sqlite3
from pathlib import Path

import i18n
import mail_senders
import own_addresses
import timeutil
from machine import kinds, services
from machine.sources.mail_senders import HINT_MAILS, sender_domain_in
from machine.sources.suggest import COUNT_UP_TO, suggestions

DAYS = 14             # the owner's first days, and how far back a failed connect and the mail count go
QUIET_TODOS = 1       # a day with more new to-dos than this needs no suggestion
ENOUGH = HINT_MAILS   # emails before WhatsApp counts as a signal: the setup hints' bar
MAILS_READ = 400      # the latest emails looked through for WhatsApp
MAIL_KINDS = tuple(k for k in kinds.of(family=kinds.MAIL) if kinds.KINDS[k]['service'] in services.of(group=services.MAIL))
WHATSAPP = re.compile(r'https?://(?:wa\.me/|chat\.whatsapp\.com/|api\.whatsapp\.com/send)|\bwhatsapp\b', re.I)
WHATSAPP_SENDERS = ('whatsapp.com', 'whatsapp.net', 'facebookmail.com', 'facebook.com', 'meta.com')
# The sources a failed connect may be tried again for, and the setup to-do row the suggestion takes the place of
REPLACES = {'whatsapp': 'whatsapp', 'account': 'account'}
SOURCE = re.compile(r'[a-z][a-z0-9_]{1,30}')
# + Add opens these straight in their own sign-in on a hosted Machine (#connect=<sign-in>); anything else: + Add
SIGNIN_LINK = {**services.field('signin'), 'whatsapp': 'whatsapp'}  # WhatsApp links by its QR code
# Where an own address was found (own_addresses' sources) that says its mail already comes in through a connected mailbox
COMES_IN = {'alias', 'received', 'sent', 'sendas'}


def link(service, hosted):
    return f'#connect={SIGNIN_LINK[service]}' if hosted and service in SIGNIN_LINK else '#connections=add'


def failed_connects(config, current, dashboard=()):
    """{service: why} for connects that failed in the last DAYS days: 'expired' (a code that ran out) or 'failed'. From
    the hosting agent's notes in the Needs you file (no text: never a Needs you line) and this dashboard's own failed
    connect sessions (`dashboard`: their source names)."""
    found = {}
    path = config.get('needs_you_file')
    notes = []
    if path:
        try:
            notes = json.loads(Path(path).expanduser().read_text())
        except (OSError, ValueError):
            notes = []
    for note in notes if isinstance(notes, list) else []:
        source = note.get('connect_failed') if isinstance(note, dict) else None
        if not isinstance(source, str) or not SOURCE.fullmatch(source):
            continue
        try:
            at = dt.datetime.fromisoformat(str(note.get('at')))
        except ValueError:
            continue
        if at.tzinfo is not None and current - at <= dt.timedelta(days=DAYS):
            found[source] = 'expired' if note.get('why') == 'expired' else 'failed'
    for source in dashboard:
        if isinstance(source, str) and SOURCE.fullmatch(source):
            found.setdefault(source, 'failed')
    return found


def whatsapp_mails(db, since):
    """How many emails from people since `since` link to WhatsApp or name it (never one a program sent, a mailing, the
    owner's own, or WhatsApp's own mail), counting up to COUNT_UP_TO."""
    marks = ','.join('?' * len(MAIL_KINDS))
    found = 0
    for title, body, metadata in db.execute(f'SELECT title,body,metadata FROM events WHERE kind IN ({marks}) AND deleted=0 AND occurred_at>=? '
                                            'ORDER BY occurred_at DESC LIMIT ?', (*MAIL_KINDS, since, MAILS_READ)):
        try:
            m = json.loads(metadata or '{}')
        except ValueError:
            continue
        if not isinstance(m, dict) or m.get('from_me') or {'SENT', 'DRAFT', 'SPAM'} & set(m.get('labels') or ()):
            continue
        if m.get('list_unsubscribe') or m.get('list_id') or mail_senders.automated(m):
            continue
        sender = (mail_senders.addresses(m.get('from')) or [('', '')])[0][1]
        if not sender or mail_senders.bulk(sender) or mail_senders.RELAY.search(sender) or sender_domain_in(sender, WHATSAPP_SENDERS):
            continue
        text = f'{title if isinstance(title, str) else ""}\n{body if isinstance(body, str) else ""}'
        found += bool(WHATSAPP.search(text))
    return min(found, COUNT_UP_TO)


def other_address(db, config):
    """Whether the owner has an address of their own that no connected mailbox brings in: their own sign-in elsewhere
    (a calendar, Slack), not an alias or an address mail already comes to here."""
    mail = services.of(group=services.MAIL)
    connected = {str(a.get('email') or '').strip().lower() for a in config.get('accounts') or []
                 if isinstance(a, dict) and a.get('service') in mail}
    own_addresses.ensure(db)
    seen = {r[0]: set(json.loads(r[1] or '[]')) for r in db.execute('SELECT address,sources FROM own_addresses')}
    return any(a not in connected and a in seen and not seen[a] & COMES_IN for a in own_addresses.yours(db, config))


def candidates(db, config, current, failed):
    """[(id, title, button, href, icon, replaces)] with a signal, the strongest kind first."""
    import onboarding
    hosted = str(config.get('manage_url') or '').startswith('https://')
    have = {str(a.get('service') or '') for a in config.get('accounts') or [] if isinstance(a, dict) and not a.get('shared')}
    out = []
    for service, why in failed.items():
        if service in have:
            continue
        label = 'WhatsApp' if service == 'whatsapp' else onboarding.label(service)
        title = i18n.t('Try {} again? The code ran out.', label) if why == 'expired' else i18n.t('Try {} again? The sign-in didn’t finish.', label)
        out.append(('retry-' + service, title, i18n.t('Try again'), link(service, hosted), service if service == 'whatsapp' else 'connect',
                    REPLACES.get(service, 'connect')))
    if hosted and 'whatsapp' not in have and 'whatsapp' not in failed:
        count = whatsapp_mails(db, (current - dt.timedelta(days=DAYS)).isoformat())
        if count >= ENOUGH:
            out.append(('whatsapp', i18n.t('Connect WhatsApp? {} emails mention it.', count), i18n.t('Connect'), link('whatsapp', hosted),
                        'whatsapp', 'whatsapp'))
    if hosted and other_address(db, config):
        out.append(('account', i18n.t('Add your other address too? Mail to it shows up here.'), i18n.t('Add'), '#connections=add', 'account', 'account'))
    tiles = [{'name': 'slack', 'label': 'Slack'}] + ([{'name': 'teams', 'label': 'Teams'}] if hosted and config.get('teams_consent') else [])
    tiles = [x for x in tiles if x['name'] not in have and x['name'] not in failed]
    for s in suggestions(db, tiles, (), current) if tiles else []:
        label = 'Slack' if s['name'] == 'slack' else 'Teams'
        title = (i18n.t('Connect {0}? {1} emails from {0} this month.', label, s['count']) if s['why'] == 'mail' else
                 i18n.t('Connect {0}? {1} meetings use it this month.', label, s['count']) if s['why'] == 'meetings' else
                 i18n.t('Connect {0}? {1} messages link to it this month.', label, s['count']))
        out.append((s['name'], title, i18n.t('Connect'), link(s['name'], hosted), 'connect', 'connect'))
    return out


def quiet_today(db, current):
    """Whether today (the owner's day) brought at most QUIET_TODOS new to-dos so far."""
    local = current.astimezone(timeutil.local_tz())
    midnight = local.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(dt.timezone.utc).isoformat()
    return db.execute('SELECT count(*) FROM suggestions WHERE created_at>=?', (midnight,)).fetchone()[0] <= QUIET_TODOS


def pick(store, config, started, dismissed=(), dashboard_failed=(), current=None):
    """The suggestion for the setup to-do, or None: {id, title, button, href, icon, replaces, nudge}. `started`: when the
    owner started (App.started_at); `dismissed`: the setup rows closed (setup:<step>); `dashboard_failed`: sources whose
    connect failed on this dashboard. The one picked today stays today while it has its signal; a new one comes at most
    once a day."""
    current = current or timeutil.clock()
    try:
        begun = dt.datetime.fromisoformat(str(started or '').replace('Z', '+00:00'))
    except ValueError:
        return None
    if begun.tzinfo is None:  # a hosted Machine's signup is a date
        begun = begun.replace(tzinfo=dt.timezone.utc)
    if current - begun > dt.timedelta(days=DAYS):
        return None
    closed = set(dismissed or ())
    try:
        with store.connect() as db:
            if not quiet_today(db, current):
                return None
            found = [c for c in candidates(db, config, current, failed_connects(config, current, dashboard_failed))
                     if 'hint-nudge-' + c[0] not in closed]
            kept = db.execute("SELECT at,detail FROM milestones WHERE name='setup_nudge'").fetchone()
            today = current.astimezone(timeutil.local_tz()).date()
            if kept and dt.datetime.fromisoformat(kept[0]).astimezone(timeutil.local_tz()).date() == today:
                chosen = next((c for c in found if c[0] == kept[1]), None)  # today's, while it still has its signal
            else:
                chosen = found[0] if found else None
                if chosen:
                    db.execute("INSERT OR REPLACE INTO milestones(name,at,detail) VALUES('setup_nudge',?,?)", (current.isoformat(), chosen[0]))
    except (sqlite3.Error, ValueError, OSError):
        return None
    if not chosen:
        return None
    key, title, button, href, icon, replaces = chosen
    return {'id': 'nudge-' + key, 'title': title, 'button': button, 'href': href, 'icon': icon, 'replaces': replaces, 'nudge': True}
