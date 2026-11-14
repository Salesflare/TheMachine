"""What a source leaves out: the owner's exclusion rules, the default ones (Android status notices, routine calendar
blocks, automatic mail subjects) and the checks a sync runs on each event. Moved out of assistant.py as is."""
import datetime as dt
import html
import re

from sources import CALENDAR_SERVICES


def routine_recurring_instance(metadata):
    """A recurring meeting's occurrence that still starts at its original time and isn't canceled."""
    if not metadata.get('recurring_event_id') or metadata.get('status') == 'cancelled':
        return False
    start, original = metadata.get('start') or {}, metadata.get('original_start') or {}
    if not isinstance(start, dict) or not isinstance(original, dict):
        return False
    if start.get('date') or original.get('date'):
        return start.get('date') == original.get('date')
    try:
        return dt.datetime.fromisoformat(start['dateTime'].replace('Z', '+00:00')) == \
            dt.datetime.fromisoformat(original['dateTime'].replace('Z', '+00:00'))
    except (KeyError, ValueError, AttributeError):
        return False


def excluded_by_rules(rules, event):
    """Owner-chosen noise that is never stored (account config `exclude`; a routine_recurring rule only skips the review, see
    routine_rules). A rule matches when
    all its conditions hold: `channels` (Slack channel names), `bots_only`, `packages`
    (Android package names), `chats` (WhatsApp or Telegram chat IDs), `senders` (email address substrings)
    or `routine_recurring` (calendar instances of a recurring event that weren't moved or canceled),
    usually combined with `titles` (exact event titles, case-insensitive), or `text`
    (case-insensitive regular expressions searched in the title and body)."""
    metadata = event.get('metadata') or {}
    for rule in rules or []:
        if 'channels' in rule and metadata.get('channel_name') not in rule['channels']:
            continue
        if rule.get('bots_only') and not (metadata.get('bot_id') or metadata.get('subtype') == 'bot_message'):
            continue
        if 'packages' in rule and metadata.get('package_name') not in rule['packages']:
            continue
        if 'chats' in rule and metadata.get('chat_id') not in rule['chats']:
            continue
        if rule.get('routine_recurring') and not routine_recurring_instance(metadata):
            continue
        if 'titles' in rule and str(event.get('title', '')).strip().casefold() not in {t.casefold() for t in rule['titles']}:
            continue
        if 'text' in rule and not any(re.search(p, f"{event.get('title', '')} {event.get('body', '')}", re.I) for p in rule['text']):
            continue
        if 'senders' in rule and not any(s.lower() in str(metadata.get('from', '')).lower() for s in rule['senders']):
            continue
        return True
    return False


# Noise every owner has, on top of their own `exclude` rules. An account's `"default_exclude": false` turns these off.
# Android's own status notices (not storage or security warnings, which still come through).
ANDROID_STATUS_NOTICES = {'packages': ['android'], 'text': [r'is displaying over other apps', r'charging this device via usb',
                                                           r'usb debugging connected', r'wireless debugging connected', r'serial console enabled']}


# Recurring placeholders that weren't moved or canceled: the calendar says nothing new, so no review. They stay on the Calendar.
ROUTINE_CALENDAR = {'routine_recurring': True, 'titles': ['Lunch', 'Block', 'Blocked', 'Busy', 'Focus', 'Focus time', 'Deep work', 'Home',
                                                          'Office', 'Commute', 'Gym', 'Stand up', 'Standup', 'Daily standup', 'Happy birthday!']}


def routine_rules(rules):
    """(dropping, keeping): a `routine_recurring` rule only keeps a meeting out of the review. The meeting is still on the
    owner's day, so it is stored (already reviewed) for the Calendar and Talk. Every other rule means never stored."""
    rules = rules or []
    return [r for r in rules if not r.get('routine_recurring')], [r for r in rules if r.get('routine_recurring')]


# Chat apps' phone notifications never come in (docs/help/android.md promises it). The OpenClaw Android app already
# drops them (NotificationForwardingPolicy.kt, the same list); this keeps the promise with an older OpenClaw build or
# another app that forwards notifications. Their chats come in through their own connections instead. Not
# `default_exclude`: it holds for every owner.
ANDROID_CHAT_APPS = {'packages': ['com.discord', 'com.whatsapp', 'com.whatsapp.w4b', 'org.telegram.messenger',
                                  'org.telegram.messenger.web', 'org.thunderdog.challegram', 'org.thoughtcrime.securesms']}


def default_exclusions(config, account):
    if account.get('service') == 'android' and account.get('default_exclude') is False:
        return [ANDROID_CHAT_APPS]
    if account.get('default_exclude') is False:
        return []
    if account.get('service') == 'android':
        # One connected work account does not cover every mailbox/workspace in
        # the phone app. Unknown account previews stay; explicit owner exclusions
        # can still suppress a whole package when that is genuinely wanted.
        return [ANDROID_CHAT_APPS, ANDROID_STATUS_NOTICES]
    if account.get('service') in CALENDAR_SERVICES:
        return [ROUTINE_CALENDAR]
    return []


# Calendar invite acceptances are noise in every email source. Subject-only, case-insensitive; config `excluded_email_subjects` overrides.
DEFAULT_EXCLUDED_EMAIL_SUBJECTS = [
    r"^\s*(accepted|geaccepteerd|aanvaard|accepté|acceptée|angenommen|akzeptiert|aceptado|aceptada|aceito|aceita"
    r"|accettato|accettata|zaakceptowano|godkänt|accepteret|godtatt|hyväksytty)\s*:",
]


def email_subject_excluded(config, subject):
    normalized = html.unescape(str(subject or '')).replace('’', "'").replace('‘', "'")
    return any(re.search(pattern, normalized, re.I)
               for pattern in config.get('excluded_email_subjects', DEFAULT_EXCLUDED_EMAIL_SUBJECTS))


def calendar_title_excluded(account, title):
    # Narrow owner-requested title matching; do not suppress birthday-related
    # meetings merely because their descriptions mention someone's birthday.
    normalized = html.unescape(str(title or '')).replace('’', "'").casefold()
    return any(str(term).replace('’', "'").casefold() in normalized
               for term in account.get('excluded_title_terms', []) if term)
