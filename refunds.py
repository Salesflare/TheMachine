"""Refunds owed to the owner (docs/help/promises.md, "Refunds"): money back that a message promised them (a shop, an
airline, a landlord, an insurer or a marketplace: "we'll refund you", a canceled order, an approved claim), with its
amount, who pays it and the last day it should be in. Plain code from there on, no model.

The review reads the message by meaning, as for any promise, and records it as someone else's promise with refund
{amount, currency, ref, contact} and due (Store.promise). check() holds that to what the message shows: the amount in
that currency, the order or case number, the contact's address, and a due day the message names (a date, or a span of
days counted from the message's day). No amount, payer or day it shows: nothing is kept. Quality or nothing.

Money back (arrived): a later message from the payer's own site, a payment service's mail, or a bank app's notification
on the phone, showing the same amount in the same currency; from a payment service or a bank app it also names the
payer or the order or case number, and from the payer's site the order or case number when there is one. A message
that gave the refund a new date ("still on its way") never counts. The review may close it too, by meaning.

Not in by its day: one quiet to-do, "Chase the €42 refund from Acme", with a short draft to the contact that cites the
order or case number (draft). Nothing is sent by itself. Money back after that closes the to-do by itself, with Undo
(Store.bill_paid). Returns windows are out of scope."""
import datetime as dt
import json
import re
from decimal import Decimal, InvalidOperation

import graph
import i18n
import subscriptions
from machine.store.review_wait import NO_REPLY

MAIL_KINDS = ('gmail.message', 'ms_graph.message', 'outlook.message')
PHONE_KIND = 'android.notification'  # a bank app's notification on the owner's phone
# Payment services that send the money back for a merchant, and say so by mail
PROVIDERS = frozenset((*subscriptions.PROCESSORS, 'klarna.com', 'adyen.com', 'mollie.com', 'squareup.com', 'afterpay.com',
                       'clearpay.co.uk', 'wise.com', 'revolut.com', 'venmo.com', 'shopify.com', 'ebay.com', 'etsy.com'))
FIELDS = ('amount', 'currency', 'ref', 'contact')
SHAPE = ('refund is {"amount", "currency", "ref", "contact"}: the amount and currency as the message shows them '
         '("42.00", "EUR"), the order or case number as written (or ""), and the address to write to about it (or "")')
MAX_DAYS = 120  # a due day further out than this after the message: not a refund to watch
LATE_DAYS = 7  # due longer ago than this when it is recorded (an old message): not watched, it may have come in unseen
READ_LIMIT = 4000  # messages one look reads at most
SIGNS = {'EUR': '€', 'USD': '$', 'GBP': '£', 'JPY': '¥', 'INR': '₹'}
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
NUMBER = re.compile(r'(?<![\d.,/])(\d{1,2})(?![\d.,/]?\d)')  # "5-10 business days": 5 and 10
NUM_DATE = re.compile(r'(?<!\d)(\d{1,2})[./-](\d{1,2})(?:[./-](\d{2,4}))?(?!\d)')


def _text(title, body):
    return f'{title or ""}\n{body or ""}'[:8000]


def _plain(value):
    """An order or case number as compared: no spaces, dashes, hashes or case."""
    return re.sub(r'[\s#:\-_/.]', '', str(value or '')).casefold()


def _meta(value):
    if isinstance(value, dict):
        return value
    try:
        return json.loads(value or '{}')
    except (TypeError, ValueError):
        return {}


def _day(stamp):
    return dt.datetime.fromisoformat(str(stamp)).date()


def business_days(start, n):
    day = start
    while n > 0:
        day += dt.timedelta(days=1)
        n -= day.weekday() < 5
    return day


def due_shown(text, day, due):
    """Whether a message from `day` names `due` as the last day: a date it writes (Nov 20, 2026-11-20, 20/11), or a
    span it gives in days or weeks (5-10 business days: its last day), counted from the message's day, a day either way."""
    if due in {d for d, _ in subscriptions.dates(text, day)}:
        return True
    for m in NUM_DATE.finditer(text):
        a, b, year = int(m[1]), int(m[2]), m[3]
        if year and int(year) % 100 != due.year % 100:
            continue
        if (a, b) in ((due.day, due.month), (due.month, due.day)):
            return True
    for m in NUMBER.finditer(text):
        n = int(m[1])
        if not 1 <= n <= 90:
            continue
        for found in (day + dt.timedelta(days=n), business_days(day, n), day + dt.timedelta(weeks=n)):
            if abs((found - due).days) <= 1:
                return True
    return False


def check(row, refund, due, today, own=False):
    """The refund the review read in a message (row: its event), as the JSON kept on the promise, or (None, why) when
    it isn't one to watch. Raises ValueError (told back to the review) when it doesn't hold up against the message."""
    if not isinstance(refund, dict) or set(refund) - set(FIELDS):
        raise ValueError(SHAPE)
    if own:
        raise ValueError('A refund is promised in the payer\'s message, not one the owner sent: event_id is that message')
    text = _text(row['title'], row['body'])
    currency = str(refund.get('currency') or '').strip().upper()
    amount = subscriptions.money(refund.get('amount'))
    if amount is None or (amount, currency) not in {(v, c) for v, c, _ in subscriptions.amounts(text)}:
        raise ValueError('refund amount and currency are the ones the message shows ("42.00", "EUR"). When it shows none, '
                         'or the amount is unclear, record no refund and no promise')
    day = _day(row['occurred_at'])
    try:
        until = dt.date.fromisoformat(str(due or '')[:10])
    except ValueError:
        raise ValueError('A refund needs due: the last day it should be in, as YYYY-MM-DD. When the message gives no day '
                         'or span, record no refund and no promise') from None
    if not day < until <= day + dt.timedelta(days=MAX_DAYS) or not due_shown(text, day, until):
        raise ValueError('due is the last day the refund should be in: a date the message names, or its span counted from '
                         'the message\'s day (5-10 business days: the 10th business day after it). When it names neither, '
                         'record no refund and no promise')
    if until < today - dt.timedelta(days=LATE_DAYS):
        return None, 'That refund was due long ago; it may have come in unseen, so it is not watched'
    m = _meta(row['metadata'])
    ref = ' '.join(str(refund.get('ref') or '').split())[:60]
    if len(_plain(ref)) < 3 or _plain(ref) not in _plain(text):
        ref = ''  # one the message doesn't show is left out, never made up
    heads = {x.lower() for _, x in graph.addresses([m.get(k) for k in ('from', 'reply-to', 'reply_to') if m.get(k)])}
    contact = str(refund.get('contact') or '').strip().lower()
    if not (EMAIL.fullmatch(contact) and (contact in heads or contact in text.lower()) and not NO_REPLY.match(contact)):
        contact = subscriptions.reply_address(m) if row['kind'] in MAIL_KINDS else ''
    sender = next(iter(graph.addresses([m.get('from')])), ('', ''))[1] if m.get('from') else ''
    return {'amount': str(amount), 'currency': currency, 'ref': ref, 'contact': contact,
            'site': subscriptions._site(sender.rpartition('@')[2]) if sender else ''}, None


def load(value):
    """A promise's refund (its JSON, unsealed), or None."""
    found = _meta(value) if value else None
    try:
        return found if found and Decimal(found['amount']) > 0 and found.get('currency') else None
    except (InvalidOperation, KeyError, TypeError):
        return None


def money_text(refund):
    """'€42', '€42.50', '$1,250', '42 CHF'."""
    value = Decimal(refund['amount'])
    shown = f'{value:,.0f}' if value == value.to_integral() else f'{value:,.2f}'
    sign = SIGNS.get(refund['currency'])
    return f'{sign}{shown}' if sign else f'{shown} {refund["currency"]}'


def arrived(db, promise, refund, after=0):
    """The first message after a refund's promise that shows the money back, and the last event id read:
    (event id or None, last id). promise: its row with made_at. after: the last event id an earlier look read."""
    skip = {promise['event_id']} | {int(r[0]) for r in db.execute(
        "SELECT detail FROM promise_log WHERE promise_id=? AND kind='source'", (promise['id'],)) if str(r[0] or '').isdigit()}
    want = (Decimal(refund['amount']), refund['currency'])
    ref, who = _plain(refund.get('ref')), ' '.join(str(promise['who'] or '').split()).casefold()
    kinds = (*MAIL_KINDS, PHONE_KIND)
    last = after
    for r in db.execute(f"SELECT id,kind,title,body,metadata FROM events WHERE id>? AND deleted=0 AND kind IN ({','.join('?' * len(kinds))}) "
                        'AND occurred_at>? ORDER BY id LIMIT ?', (after, *kinds, promise['made_at'], READ_LIMIT)):
        last = r['id']
        if r['id'] in skip:
            continue
        text = _text(r['title'], r['body'])
        if want not in {(v, c) for v, c, _ in subscriptions.amounts(text)}:
            continue
        named = (ref and ref in _plain(text)) or (len(who) >= 3 and who in text.casefold())
        if r['kind'] == PHONE_KIND:
            if named:
                return r['id'], last
            continue
        m = _meta(r['metadata'])
        if m.get('from_me') or set(m.get('labels') or ()) & {'SENT', 'DRAFT', 'SPAM', 'TRASH'}:
            continue
        found = next(iter(graph.addresses([m.get('from')])), ('', ''))[1] if m.get('from') else ''
        site = subscriptions._site(found.rpartition('@')[2]) if found else ''
        if site and site == refund.get('site') and (not ref or ref in _plain(text)):
            return r['id'], last
        if site in PROVIDERS and named:
            return r['id'], last
    return None, last


def text(promise, refund, said, by):
    """The chase to-do's title and body, in the owner's language. said, by: the promise's day and its due day, as
    written for the owner."""
    money, who = money_text(refund), promise['who']
    title = i18n.t('Chase the {} refund from {}', money, who)
    body = (i18n.t('Promised on {} ({}), to be in by {}. Nothing shows it came in yet.', said, refund['ref'], by) if refund.get('ref') else
            i18n.t('Promised on {}, to be in by {}. Nothing shows it came in yet.', said, by))
    return title, body


def draft(promise, refund, said, signature=''):
    """The short email to the contact, never sent by itself: {'to', 'subject', 'body'}, or None without a contact."""
    if not refund.get('contact'):
        return None
    money = money_text(refund)
    if refund.get('ref'):
        subject = i18n.t('Refund for {}', refund['ref'])
        body = i18n.t('Hello,\n\nOn {} you confirmed a refund of {} ({}). It hasn’t come in yet. Could you check where it is and let me know when it will arrive?\n\nThank you',
                      said, money, refund['ref'])
    else:
        subject = i18n.t('Refund of {}', money)
        body = i18n.t('Hello,\n\nOn {} you confirmed a refund of {}. It hasn’t come in yet. Could you check where it is and let me know when it will arrive?\n\nThank you',
                      said, money)
    return {'to': refund['contact'], 'subject': subject, 'body': body + (f'\n{signature}' if signature else '')}
