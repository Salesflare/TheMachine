"""Android as a source: the phone's notifications through the paired node (Android), a notification as an event
(android_event), the app names it shows, and its sync from the feed or the node (sync_android). Moved out of
assistant.py as is."""
import datetime as dt
import hashlib
import json
import re
import subprocess

from machine.config import ROOT
from machine.model_usage import node_bin, node_env
from machine.sources.rows import Skips
from machine.text import encoded
from sources import SourceError
from timeutil import now


ANDROID_APP_NAMES = {
    'android': 'Android System', 'com.google.android.gm': 'Gmail',
    'com.google.android.apps.tasks': 'Google Tasks', 'com.google.android.apps.wellbeing': 'Digital Wellbeing',
    'com.openai.chatgpt': 'ChatGPT', 'com.tailscale.ipn': 'Tailscale', 'org.telegram.messenger': 'Telegram',
    'com.whatsapp': 'WhatsApp', 'com.whatsapp.w4b': 'WhatsApp Business',
    'com.android.chrome': 'Chrome', 'com.google.android.calendar': 'Google Calendar',
    'computer.themachine.app': 'The Machine', 'com.android.vending': 'Google Play', 'com.linkedin.android': 'LinkedIn',
    'com.kbc.mobile.android.phone.kbc': 'KBC Mobile', 'com.Slack': 'Slack', 'com.microsoft.teams': 'Teams',
    'com.microsoft.office.outlook': 'Outlook', 'com.google.android.apps.messaging': 'Messages',
    'com.google.android.dialer': 'Phone', 'com.instagram.android': 'Instagram', 'com.facebook.orca': 'Messenger',
    'com.facebook.katana': 'Facebook', 'com.twitter.android': 'X', 'org.thoughtcrime.securesms': 'Signal',
    'com.spotify.music': 'Spotify', 'com.google.android.youtube': 'YouTube', 'com.google.android.apps.maps': 'Google Maps',
    'com.google.android.apps.photos': 'Google Photos', 'com.google.android.apps.docs': 'Google Drive',
    'com.google.android.keep': 'Google Keep', 'com.google.android.apps.meetings': 'Google Meet', 'us.zoom.videomeetings': 'Zoom',
    'com.intercom.android': 'Intercom', 'com.stripe.android.dashboard': 'Stripe', 'com.github.android': 'GitHub',
}


def android_app_name(package):
    # Exact known package labels only; unknown apps retain their package ID.
    return ANDROID_APP_NAMES.get(package, package)


# The parts of a package name that say nothing about the app: its domain's end and platform words
PACKAGE_NOISE = {'com', 'org', 'net', 'io', 'co', 'app', 'apps', 'android', 'mobile', 'phone', 'client', 'main', 'prod', 'release',
                 'free', 'lite', 'ui', 'activity', 'launcher'}


def android_app_shown(package, app_name=None):
    """An app's name as people read it: its known label, else a name read from its package ("com.acme.mobile.android"
    as "Acme", "nl.abn.ab" as "ABN"), never the raw reverse-domain string. The stored app_name stays as it is
    (android_app_name) for an agent's exact matching; this is for lists people scan."""
    package = str(package or '')
    if package in ANDROID_APP_NAMES:
        return ANDROID_APP_NAMES[package]
    name = str(app_name or '').strip()
    if name and name != package and '.' not in name:
        return name
    parts = [p for p in re.split(r'[._]', package) if p]
    words = [p for p in parts[1:] if p.casefold() not in PACKAGE_NOISE and not p.isdigit()] or parts[-1:]
    if not words:
        return 'Unknown app'
    word = words[0]
    if word.casefold() == 'google' and len(words) > 1:
        return 'Google ' + words[-1].capitalize()
    return word.upper() if len(word) <= 3 else word[:1].upper() + word[1:]


class Android:
    def __init__(self, config, account):
        self.config, self.account = config, account

    def snapshot(self):
        try:
            result = subprocess.run([node_bin(self.config), str(ROOT / 'android-notifications.mjs'),
                                     self.account['node_id']], env=node_env(self.config), capture_output=True, text=True, timeout=25)
        except subprocess.TimeoutExpired:
            raise SourceError('android_timeout', retry_after=600) from None
        if result.returncode:
            # The helper emits only an allowlisted class, never protocol contents.
            label = result.stderr.strip()
            raise SourceError(label if label in ('android_offline', 'android_identity_mismatch',
                'android_notifications_unavailable', 'android_gateway_unavailable') else 'android_read_failed', retry_after=600)
        try:
            data = json.loads(result.stdout)
        except ValueError:
            raise SourceError('android_invalid_json') from None
        if not isinstance(data, dict):
            raise SourceError('android_invalid_snapshot')
        return data


def android_event(account, raw):
    if (not isinstance(raw.get('key'), str) or not isinstance(raw.get('packageName'), str)
            or not isinstance(raw.get('postTimeMs'), int)):
        raise SourceError('android_invalid_notification')
    title = str(raw.get('title') or raw['packageName'])
    body = '\n'.join(str(raw.get(k) or '') for k in ('text', 'subText')).strip()
    # OTP values are credentials, not useful long-lived assistant context.
    sensitive = bool(re.search(r'(?i)verification code|security code|one.time (?:code|password)|\bOTP\b|verificatiecode', title + ' ' + body))
    if sensitive:
        body = '[One-time security code omitted]'
        title = re.sub(r'(?<!\d)\d{4,8}(?!\d)', '[code]', title)
    identity = hashlib.sha256((raw['key'] + ':' + str(raw['postTimeMs'])).encode()).hexdigest()
    return {'account_id': account['id'], 'source_id': identity, 'kind': 'android.notification',
            'occurred_at': dt.datetime.fromtimestamp(raw['postTimeMs'] / 1000, dt.timezone.utc).isoformat(),
            'title': title[:1000], 'body': body[:40000], 'deleted': False,
            'metadata': {'package_name': raw['packageName'], 'app_name': android_app_name(raw['packageName']),
                         'notification_key_hash': hashlib.sha256(raw['key'].encode()).hexdigest(),
                         'app_name_source': 'known_package_label' if raw['packageName'] in ANDROID_APP_NAMES else 'package_id_fallback', 'post_time_ms': raw['postTimeMs'],
                         'is_ongoing': bool(raw.get('isOngoing')), 'category': raw.get('category'),
                         'channel_id': raw.get('channelId'), 'source_account': 'unknown',
                         'security_code_omitted': sensitive, 'truncated': True,
                         'coverage': 'Current notifications only; Android limits each text field to 512 characters.'}}


def sync_android_feed(store, config, account):
    with store.connect() as db:
        health = db.execute('SELECT * FROM android_feed_health WHERE id=1').fetchone()
        # Pick complete notification-key groups, not the first 100 observations
        # of a noisy progress bar. Arrival rowid also orders same-ms changes.
        rows = db.execute("SELECT rowid AS arrival_order,* FROM android_inbox WHERE json_extract(payload,'$.notification_key_hash') IN (SELECT json_extract(payload,'$.notification_key_hash') FROM android_inbox GROUP BY json_extract(payload,'$.notification_key_hash') ORDER BY min(rowid) LIMIT 100) ORDER BY rowid").fetchall()
        acked = {r['id'] for r in rows if db.execute('SELECT 1 FROM android_receipts WHERE id=? AND account_id=?',(r['id'],account['id'])).fetchone()}
    healthy = bool(health and health['last_checked'] and not health['error'] and
        (dt.datetime.fromisoformat(now()) - dt.datetime.fromisoformat(health['last_checked'])).total_seconds() <= 90)
    if not healthy and not rows:
        raise SourceError('android_feed_unavailable', retry_after=15)
    events, consumed = store.android_feed_batch(account, [r for r in rows if r['id'] not in acked])
    consumed += list(acked)
    state = store.checkpoint(account['id']) or {}
    if healthy: state.pop('feed_unavailable_since', None)
    else: state.setdefault('feed_unavailable_since', now())
    state.update(mode='incremental', transport='existing_feed_with_reconciliation' if account.get('reconcile_seconds') else 'existing_openclaw_feed',
                 feed_last_checked=health['last_checked'] if health else None, feed_last_event=health['last_recorded'] if health else None,
                 coverage='Existing forwarded notifications only. Phone filters, disconnection and the bounded Gateway queue may omit events.')
    # Evidence, checkpoint and inbox acknowledgment share one transaction.
    store.commit_page(account['id'], state, events, android_inbox_ids=consumed)
    if not healthy:
        # Captured evidence is usable without the Gateway; collection remains
        # visibly degraded rather than calling an offline bridge healthy.
        raise SourceError('android_feed_unavailable', retry_after=15)
    return {'mode': 'incremental', 'events': len(events), 'more': len(rows) >= 100 and bool(consumed)}


def sync_android_preferred(store, config, account, fallback=None):
    result, feed_available = None, True
    try:
        result = sync_android_feed(store, config, account)
    except SourceError as error:
        if error.category != 'android_feed_unavailable' or not account.get('direct_fallback', False):
            raise
        feed_available = False
    if feed_available and not account.get('reconcile_seconds'):
        return result
    state = store.checkpoint(account['id']) or {}
    minimum = max(600, int(account.get('reconcile_seconds') or account.get('fallback_seconds', 600)))
    attempt = state.get('fallback_last_attempt')
    elapsed = (dt.datetime.fromisoformat(now()) - dt.datetime.fromisoformat(attempt)).total_seconds() if attempt else minimum + 1
    if elapsed < minimum:
        if not feed_available:
            raise SourceError('android_feed_unavailable', retry_after=max(15, int(minimum - elapsed))) from None
        return result
    state['fallback_last_attempt'] = now()
    store.commit_page(account['id'], state, [], record_sync=False)
    try:
        snapshot_result = sync_android(store, config, account, fallback, reconcile=True)
    except SourceError as error:
        state = store.checkpoint(account['id'])
        state.update(reconciliation_error=error.category, reconciliation_error_at=now())
        store.commit_page(account['id'], state, [], record_sync=False)
        # Preserve a redacted failed-read receipt even if the passive feed works.
        raise
    else:
        state = store.checkpoint(account['id'])
        state.pop('reconciliation_error', None)
        state.pop('reconciliation_error_at', None)
        state.update(transport='existing_feed_with_reconciliation' if feed_available else 'direct_fallback')
        if not feed_available: state.setdefault('feed_unavailable_since', now())
        store.commit_page(account['id'], state, [], record_sync=False)
        return snapshot_result


def sync_android(store, config, account, source=None, reconcile=False):
    source = source or Android(config, account)
    state = store.checkpoint(account['id']) or {}
    try:
        snapshot = source.snapshot()
        rows = snapshot.get('notifications')
        if snapshot.get('enabled') is not True or snapshot.get('connected') is not True:
            raise SourceError('android_notifications_unavailable', retry_after=600)
        if not isinstance(rows, list) or snapshot.get('count') != len(rows):
            raise SourceError('android_invalid_snapshot')
        skipped = Skips('android_invalid_notification')  # a notification it can't take is counted, never failing the read
        events = [e for e, _ in skipped.every([r for r in rows if not isinstance(r, dict) or r.get('packageName') != 'ai.openclaw.app'],
                                             android_event, account)]
        skipped.check()
        if reconcile:
            with store.connect() as db:
                for i, event in enumerate(events):
                    key = event['metadata']['notification_key_hash']
                    old = db.execute("SELECT * FROM events WHERE account_id=? AND json_extract(metadata,'$.notification_key_hash')=? ORDER BY occurred_at DESC,id DESC LIMIT 1",(account['id'],key)).fetchone()
                    if not old: continue
                    meta = json.loads(old['metadata'])
                    # A forwarded active episode is the same exact current
                    # notification. Do not guess matches by app/title or merge
                    # a post after an observed clear into the previous episode.
                    if meta.get('transport') == 'existing_openclaw_feed' and meta.get('is_active', True):
                        # The passive preview and snapshot have different text
                        # formats. Retain captured text until a newer native post;
                        # presence checks must not create alternating versions.
                        events[i] = {k:old[k] for k in ('account_id','source_id','kind','occurred_at','title','body','deleted')}
                        events[i]['deleted'] = bool(old['deleted'])
                        fingerprint = hashlib.sha256(encoded([event['title'],event['body']]).encode()).hexdigest()
                        prior_fingerprint = meta.get('snapshot_content_hash')
                        if prior_fingerprint and prior_fingerprint != fingerprint:
                            # A changed current snapshot recovers an update lost
                            # by forwarding. First observation establishes a
                            # baseline, since the two preview formats differ.
                            events[i]['title'] = event['title']
                            events[i]['body'] = event['body']
                            meta.update(security_code_omitted=event['metadata']['security_code_omitted'],
                                        last_notification_event_ms=int(dt.datetime.fromisoformat(now()).timestamp()*1000))
                        meta['snapshot_content_hash'] = fingerprint
                        meta['snapshot_checked_at'] = now()
                        events[i]['metadata'] = meta
                    elif old['source_id'] == event['source_id']:
                        event['occurred_at'] = old['occurred_at']
    except SourceError:
        if not state.get('offline_since'):
            state['offline_since'] = now()
            store.commit_page(account['id'], state, [], record_sync=False)
        raise
    stamp = now()
    if state.get('offline_since'):
        gaps = state.get('gaps', [])
        gaps.append({'from': state.pop('offline_since'), 'to': stamp})
        state['gaps'] = gaps[-20:]
    state.update(mode='incremental', observed_from=state.get('observed_from', stamp),
                 snapshot_count=len(rows), last_observed=stamp,
                 coverage='Snapshots only. Notifications cleared between reads or during disconnection can be missed.')
    skipped.note(state)
    store.commit_page(account['id'], state, events)
    return {'mode': 'incremental', 'events': len(events), 'skipped': sum(skipped.values())}
