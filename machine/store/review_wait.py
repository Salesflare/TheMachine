"""Which waiting signals can wait for a batch (App.review_step, App.review_queue). Every review pays a large fixed start
(instructions, status, context: some 70k fresh tokens on a busy Machine, 2026-11), and a newsletter, a receipt or an
app's notification at night started one on its own every 15 minutes. Now a signal from a person starts a review as
before (at min_signals waiting, or once it waited max_wait_minutes); automated and bulk ones wait for the next review,
at most BATCH_WAIT_MINUTES, and join whatever review starts first.

Told apart without a model, on what the signal itself says: List-Unsubscribe, List-Id, Precedence and Auto-Submitted
headers, Gmail's categories, a system sender (no-reply, notifications, receipts), a mailing the Graph left out, the
kind of app a phone notification came from, a Slack bot. Anything else, and anything unsure, is a person's: a reply,
a known person in the Graph, mail the owner sent, a chat, a calendar change, a time-sensitive title. A late human
to-do costs more than the tokens."""
import datetime as dt
import json
import re

import graph
from machine.store.events import SET_ASIDE_AFTER


# A batchable signal's review starts at most this long after it came in. With the gap after a run (gap_seconds, 10
# minutes) and the run itself, the to-do it brings is there within the hour, also a receipt or a bill with a deadline.
BATCH_WAIT_MINUTES = 45


# Gmail's categories for mail no person wrote by hand (Primary is everything else)
BATCH_LABELS = frozenset({'CATEGORY_PROMOTIONS', 'CATEGORY_SOCIAL', 'CATEGORY_FORUMS', 'CATEGORY_UPDATES'})


BATCH_PRECEDENCE = frozenset({'bulk', 'junk', 'list'})


# A system's address, never a person: no-reply and its kin (graph.bulk has notifications, newsletters, receipts, billing and the mail services)
NO_REPLY = re.compile(r'(?i)^(?:no-?reply|do-?not-?reply|mailer-daemon|postmaster)(?:[+._-][^@]*)?@')


# Calendar mail is a person's invitation or answer, sent by the calendar for them: a calendar change, never batched
CALENDAR_MAIL = re.compile(r'(?i)@(?:[\w-]+\.)*calendar\.google\.com$|^calendar-(?:notification|server)@')


# A title that says it can't wait an hour. Mail in Promotions never counts ("ends today" is a sale).
TIME_SENSITIVE = re.compile(
    r"(?i)\b(?:urgent|asap|immediately|overdue|final notice|action required|respond by|reply by|security alert|suspicious|"
    r"unusual sign.?in|new sign.?in|password reset|payment failed|card declined|(?:due|by|before|expires?|until) (?:today|tonight)|"
    r"starts? (?:in|at|now|soon)|starting (?:now|soon)|in \d+ min(?:ute)?s?|"
    r"dringend|vandaag|onmiddellijk|aujourd.hui|imm[ée]diatement|heute|sofort|urgente|hoy)\b")


# Phone apps a person writes or calls through, or that keep the owner's day: their notifications are a person's
PERSON_APPS = frozenset({
    'com.whatsapp', 'com.whatsapp.w4b', 'org.telegram.messenger', 'org.thoughtcrime.securesms', 'com.facebook.orca',
    'com.instagram.android', 'com.google.android.apps.messaging', 'com.samsung.android.messaging', 'com.android.mms',
    'com.google.android.dialer', 'com.android.dialer', 'com.samsung.android.dialer', 'com.android.server.telecom',
    'com.Slack', 'com.microsoft.teams', 'com.discord', 'com.viber.voip', 'jp.naver.line.android', 'com.skype.raider',
    'com.linkedin.android', 'com.beeper.android', 'com.google.android.gm', 'com.microsoft.office.outlook',
    'com.google.android.calendar', 'com.samsung.android.calendar', 'com.google.android.apps.tachyon',
    'us.zoom.videomeetings', 'com.google.android.apps.meetings', 'com.google.android.deskclock'})


# Android's own notification categories that are a person or the owner's day (a call, a message, a meeting, an alarm)
PERSON_CATEGORIES = frozenset({'call', 'missed_call', 'msg', 'email', 'event', 'reminder', 'alarm', 'location_sharing'})


# Kinds that are a system's report, never a person's message: a failed CI run, a feed's post, a payment event
BATCH_KINDS = frozenset({'github.ci', 'rss.item', 'stripe.event'})


# Stripe events that can't wait an hour
STRIPE_NOW = re.compile(r'^(?:charge\.dispute\.|radar\.early_fraud_warning\.)')


def meta(row):
    value = row['metadata']
    return value if isinstance(value, dict) else json.loads(value or '{}')


def sender(metadata):
    found = graph.addresses(metadata.get('from'))[:1]
    return found[0][1] if found else ''


class People:
    """What the Graph knows about senders, read once per look: people (a person node has their address), the senders
    the owner said are a person (mail_shown) and mailings the Graph left out (mail_hidden)."""

    def __init__(self, db):
        self.db, self.cache = db, {}

    def _one(self, sql, identifier):
        try:
            return bool(self.db.execute(sql, (identifier,)).fetchone())
        except Exception:  # a table this database doesn't have yet
            return False

    def person(self, address):
        key = ('person', address)
        if key not in self.cache:
            identifier = 'email:' + address
            self.cache[key] = self._one("SELECT 1 FROM graph_identifiers i JOIN graph_nodes n ON n.id=i.node_id "
                                        "WHERE i.identifier=? AND n.kind='person' LIMIT 1", identifier) or \
                self._one('SELECT 1 FROM mail_shown WHERE identifier=? LIMIT 1', identifier)
        return self.cache[key]

    def mailing(self, address):
        key = ('mailing', address)
        if key not in self.cache:
            self.cache[key] = self._one('SELECT 1 FROM mail_hidden WHERE identifier=? LIMIT 1', 'email:' + address)
        return self.cache[key]


def mail_wait(metadata, title, people):
    """Why a mail can wait for the batch ('list', 'precedence', 'automated', 'system', 'mailing' or 'category'), or None."""
    labels = set(metadata.get('labels') or ())
    if labels & {'SENT', 'DRAFT'} or metadata.get('from_me') or metadata.get('in-reply-to'):
        return None  # the owner's own mail, and every reply: a thread someone is in
    address = sender(metadata)
    if not address or CALENDAR_MAIL.search(address) or (people and people.person(address)):
        return None  # someone the owner knows, or a calendar change
    if TIME_SENSITIVE.search(title or '') and 'CATEGORY_PROMOTIONS' not in labels:
        return None
    if metadata.get('list_unsubscribe') or metadata.get('list_id'):
        return 'list'
    if str(metadata.get('precedence') or '').lower() in BATCH_PRECEDENCE:
        return 'precedence'
    if metadata.get('auto_submitted'):
        return 'automated'
    if NO_REPLY.match(address) or graph.bulk(address):
        return 'system'
    if people and people.mailing(address):
        return 'mailing'
    if labels & BATCH_LABELS:
        return 'category'
    return None


def can_wait(row, people=None):
    """Why this waiting signal can wait for the batch review, or None when its review should start as before. `row`:
    an events row (kind, title, metadata, deleted); `people`: People for the Graph's senders."""
    kind, title = row['kind'], row['title'] or ''
    metadata = meta(row)
    if not isinstance(metadata, dict) or metadata.get('from_me'):
        return None
    if kind == 'gmail.message':
        return mail_wait(metadata, title, people)
    if kind == 'android.notification':
        package = str(metadata.get('package_name') or '')
        if package in PERSON_APPS or str(metadata.get('category') or '') in PERSON_CATEGORIES or TIME_SENSITIVE.search(title):
            return None
        return 'phone' if package else None
    if kind == 'slack.message':
        return 'bot' if (metadata.get('bot_id') or metadata.get('subtype') == 'bot_message') and not TIME_SENSITIVE.search(title) else None
    if kind == 'whatsapp.message':
        chat = str(metadata.get('chat_id') or '')
        return 'channel' if chat.endswith(('@newsletter', '@broadcast')) else None  # a channel's post or a status, not a chat
    if kind in BATCH_KINDS:
        if TIME_SENSITIVE.search(title) or (kind == 'stripe.event' and STRIPE_NOW.match(str(metadata.get('type') or ''))):
            return None
        return 'system'
    return None


def oldest(db, limit):
    """The oldest waiting signal from a person and the oldest that can wait, by when each came in (ISO text or None),
    among the `limit` that came in first. Signals set aside (SET_ASIDE_AFTER) don't count, as before."""
    people, person, batch = People(db), None, None
    for row in db.execute('SELECT kind,title,metadata,deleted,ingested_at FROM events WHERE analyzed_version<version AND deferrals<? '
                          'ORDER BY ingested_at LIMIT ?', (SET_ASIDE_AFTER, max(int(limit), 1))):
        try:
            waits = can_wait(row, people)
        except (ValueError, TypeError):
            waits = None
        if waits:
            batch = batch or row['ingested_at']
        else:
            person = person or row['ingested_at']
        if person and batch:
            break
    return person, batch


def batch_wait(settings):
    """review_worker batch_wait_minutes (BATCH_WAIT_MINUTES), in minutes; 0 or false: no batch, every signal as a person's."""
    value = (settings or {}).get('batch_wait_minutes', BATCH_WAIT_MINUTES)
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0 else 0


def hold(db, settings, max_wait, limit=200):
    """When the waiting signals' review is due by age (a datetime, None when nothing waits): the oldest person's
    signal once it waited max_wait minutes, the oldest batchable one once it waited batch_wait minutes. Without a
    batch (batch_wait 0) every signal is a person's, as before."""
    wait = batch_wait(settings)
    if not wait:
        found = db.execute('SELECT min(ingested_at) FROM events WHERE analyzed_version<version AND deferrals<?',
                           (SET_ASIDE_AFTER,)).fetchone()[0]
        return dt.datetime.fromisoformat(found) + dt.timedelta(minutes=max_wait) if found else None
    person, batch = oldest(db, limit)
    due = [dt.datetime.fromisoformat(person) + dt.timedelta(minutes=max_wait)] if person else []
    if batch:
        due.append(dt.datetime.fromisoformat(batch) + dt.timedelta(minutes=max(wait, max_wait)))
    return min(due) if due else None
