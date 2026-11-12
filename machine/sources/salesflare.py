"""Salesflare as a source: its CRM client (Salesflare, read-only routes and joining the owner's own user to an account),
its emails and meetings as events, the feed and pipeline reads, and its sync (sync_salesflare). Moved out of
assistant.py as is."""
import datetime as dt
import hashlib
import http.client
import json
import logging
import re
import time
import urllib.error
import urllib.parse
import urllib.request

import enrichment
from machine.config import LOG
from machine.sources.exclusions import email_subject_excluded
from machine.text import QUOTED_HISTORY_KEPT, encoded, plain_html, trim_quoted_history
from sources import SourceError, credential
from timeutil import now


class Salesflare:
    """Salesflare CRM reads (GET on the exact routes below). The only write is adding the
    owner's own user to an account, and only when the account config allows it."""
    ROUTES = (r'/me', r'/accounts', r'/accounts/[0-9]+', r'/accounts/[0-9]+/feed', r'/opportunities')

    def __init__(self, config, account):
        self.config, self.account = config, account

    def get(self, path, params=None):
        if not any(re.fullmatch(route, path) for route in self.ROUTES):
            raise SourceError('unsupported_salesflare_method')
        return self.send(path, params)

    def join_account(self, crm_id):
        """Owner-authorized (Oct 10): add the owner's own user to one CRM account. Never
        another user, never PUT (which would replace the account's whole user list)."""
        if not self.account.get('join_pipelines'):
            raise SourceError('salesflare_join_disabled')
        return self.send(f'/accounts/{int(crm_id)}/users', None, [{'id': self.account['user_id']}])

    def token(self):
        values = {}
        for line in credential(self.config, self.account.get('credential', 'salesflare')).splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                key, value = line.split('=', 1)
                values[key.strip()] = value.strip().strip('"').strip("'")
        token = values.get(self.account.get('credential_variable', 'SALESFLARE_STAGING_API_KEY'))
        if not token:
            raise SourceError('missing_salesflare_credential')
        return token

    def key_fingerprint(self):
        """Which key this is, held in memory only (salesflare_confirm): a changed key is never taken as confirmed."""
        return hashlib.sha256(self.token().encode()).hexdigest()

    def send(self, path, params, payload=None):
        token = self.token()
        url = self.account['api_base'] + path + ('?' + urllib.parse.urlencode(params, doseq=True) if params else '')
        request = urllib.request.Request(url, data=encoded(payload).encode() if payload is not None else None,
                                         method='POST' if payload is not None else 'GET',
                                         headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/json',
                                                  'Content-Type': 'application/json'})
        started, route = time.monotonic(), route_of(path)
        # Account list queries ordered by activity are slow on a large team. A feed answers in a second, but now and
        # then hangs until Salesflare's gateway gives up (504 after 120 s): a shorter wait frees the round sooner. The
        # profile (/me) is as small and hangs the same way.
        timeout = self.account.get('timeout_seconds', 180)
        if route in ('/accounts/{id}/feed', '/me'):
            timeout = min(timeout, self.account.get('feed_timeout_seconds', SALESFLARE_FEED_TIMEOUT))
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read()
            return json.loads(raw) if raw.strip() else None  # a write may answer with an empty body
        except urllib.error.HTTPError as error:
            if error.code >= 500:
                # Which route failed and how long it took (ids masked), so support can tell Salesflare exactly what
                # failed: a 504 after two minutes is its gateway giving up on a slow query.
                LOG.warning('salesflare answered route=%s status=%s after=%ds', route, error.code,
                            round(time.monotonic() - started))
            retry = error.headers.get('Retry-After', '')
            failed = SourceError('salesflare', error.code, min(max(int(retry), 1), 86400) if retry.isdigit() else None, route=route)
            if error.code == 403:
                failed.reason = refusal_message(error)
            raise failed from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as error:
            raise SourceError('network:' + type(error).__name__ + ':salesflare_read', route=route) from None
        except ValueError:
            raise SourceError('salesflare_invalid_json', route=route) from None

    def profile(self):
        me = self.get('/me')
        if (not isinstance(me, dict) or str(me.get('email', '')).lower() != self.account['email'].lower()
                or me.get('id') != self.account['user_id'] or (me.get('team') or {}).get('id') != self.account['team_id']):
            raise SourceError('account_identity_mismatch')
        return me


SALESFLARE_FEED_TIMEOUT = 60  # seconds: a feed read that has not answered by then is one of Salesflare's hangs


def refusal_message(error):
    """The `message` of Salesflare's 403 body ("Forbidden"), safe to log: plain words only (no digits, @ or quotes), so no
    id or address gets through; anything else reads 'other'."""
    try:
        message = json.loads(error.read(2000) or b'{}').get('message')
    except (ValueError, AttributeError, OSError, http.client.HTTPException):
        return 'unreadable'
    message = message.strip() if isinstance(message, str) else ''
    return message if re.fullmatch(r"[A-Za-z][A-Za-z ,.()-]{0,79}", message) else 'other' if message else 'none'


def route_of(path):
    """A Salesflare path with its ids masked, safe to log: /accounts/123/feed reads /accounts/{id}/feed."""
    return re.sub(r'/[0-9]+(?=/|$)', '/{id}', path)


def salesflare_time(value):
    """A Salesflare date as UTC. Mostly ISO 8601 with Z, but some email dates come as epoch milliseconds
    (a number, sometimes as text); epoch seconds are accepted too."""
    if isinstance(value, str) and re.fullmatch(r'\s*\d{9,14}(\.\d+)?\s*', value):
        value = float(value)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        try:
            return dt.datetime.fromtimestamp(value / 1000 if abs(value) >= 1e11 else value, dt.timezone.utc)
        except (OverflowError, OSError, ValueError):
            raise SourceError('salesflare_invalid_timestamp') from None
    try:
        stamp = dt.datetime.fromisoformat(str(value).strip().replace('Z', '+00:00'))
    except ValueError:
        raise SourceError('salesflare_invalid_timestamp') from None
    if stamp.tzinfo is None:
        raise SourceError('salesflare_missing_timezone')
    return stamp.astimezone(dt.timezone.utc)


def salesflare_time_or_none(value):
    try:
        return salesflare_time(value)
    except SourceError:
        return None


def salesflare_context(account, crm):
    """Essential account info plus its contacts, keyed for matching."""
    if not isinstance(crm, dict) or not isinstance(crm.get('id'), int):
        raise SourceError('salesflare_invalid_account')
    info = {'id': crm['id'], 'name': crm.get('name') or '', 'domain': crm.get('domain') or ''}
    contacts = {}
    for person in crm.get('customers') or []:
        if isinstance(person, dict) and isinstance(person.get('id'), int):
            contacts[person['id']] = {'id': person['id'], 'name': person.get('name') or '',
                                      'email': (person.get('email') or '').lower(), 'role': person.get('role') or None}
    return info, contacts


def salesflare_link(account, crm_id):
    return f"{account['app_base']}/#/accounts/{crm_id}/info/view"


def salesflare_email_event(account, info, contacts, item, config=None):
    email = item.get('email') or {}
    if email_subject_excluded(config or {}, email.get('subject')):
        return None
    addresses = email.get('addresses') or {}
    people = []
    for field in ('from', 'to', 'cc', 'bcc'):
        value = addresses.get(field) or []
        for entry in (value if isinstance(value, list) else [value]):
            if isinstance(entry, dict) and entry.get('email'):
                people.append((field, entry.get('name') or '', str(entry['email']).lower()))
    owner = {e.lower() for e in account.get('owner_emails', [account['email']])}
    # Email that involves the owner already arrives through Gmail; keep only the rest.
    if email.get('user_id') == account['user_id'] or any(address in owner for _, _, address in people):
        return None
    text, quoted = trim_quoted_history(plain_html('\n'.join(str(part.get('content') or '') for part in email.get('body') or [] if isinstance(part, dict))), email.get('subject') or '')
    header = '\n'.join(f"{field.title()}: {name} <{address}>" if name else f"{field.title()}: {address}" for field, name, address in people)
    involved = [c for c in contacts.values() if c['email'] and c['email'] in {a for _, _, a in people}]
    return {'account_id': account['id'], 'source_id': 'email:' + str(item['id']), 'kind': 'salesflare.email',
            'occurred_at': (salesflare_time_or_none(email.get('date')) or salesflare_time(item.get('time'))).isoformat(),
            'title': (email.get('subject') or '(no subject)')[:1000],
            'body': (header + '\n\n' + text)[:40000],
            'metadata': {'crm_account': info, 'contacts': involved, 'mailbox_user_id': email.get('user_id'),
                         'thread_id': email.get('service_thread_id'), 'from': people[0][2] if people else '',
                         'truncated': len(header) + len(text) + 2 > 40000, 'quoted_history_chars': quoted,
                         'quoted_history_shortened': quoted > QUOTED_HISTORY_KEPT, 'source_url': salesflare_link(account, info['id'])},
            'deleted': False}


def salesflare_meeting_event(account, info, contacts, item):
    notes = plain_html(item.get('notes'))
    if not notes:
        return None  # only meetings with written notes are signals
    involved = []
    for person in item.get('participants') or []:
        if not isinstance(person, dict) or person.get('type') == 'user':
            continue
        known = contacts.get(person.get('id'))
        involved.append(known or {'id': person.get('id'), 'name': person.get('name') or '',
                                  'email': (person.get('email') or '').lower(), 'role': None})
    attendees = ', '.join(p.get('name') or p.get('email') or '' for p in item.get('participants') or [] if isinstance(p, dict))
    description = plain_html(item.get('description'))
    body = f"Attendees: {attendees}\n\nNotes:\n{notes}" + (f"\n\nDescription:\n{description}" if description else '')
    return {'account_id': account['id'], 'source_id': 'meeting:' + str(item['id']), 'kind': 'salesflare.meeting',
            'occurred_at': salesflare_time(item.get('time')).isoformat(),
            'title': (item.get('subject') or 'Meeting')[:1000], 'body': body[:40000],
            'metadata': {'crm_account': info, 'contacts': involved, 'meeting_type': item.get('type'),
                         'host': (item.get('person') or {}).get('email'), 'truncated': len(body) > 40000,
                         'source_url': salesflare_link(account, info['id'])},
            'deleted': False}


def salesflare_recent_accounts(source, field, since, page=50, max_pages=40):
    """CRM account IDs whose last email/meeting date is on or after `since`."""
    found = []
    for number in range(max_pages):
        rows = source.get('/accounts', {'order_by': field + ' desc', 'limit': page, 'offset': number * page, 'details': 'false'})
        if not isinstance(rows, list):
            raise SourceError('salesflare_invalid_page')
        for row in rows:
            stamp = row.get(field)
            parsed = salesflare_time_or_none(stamp) if stamp else None
            if not stamp or (parsed and parsed < since):
                return found
            # An unreadable date still lists the account: reading it once too often beats missing it.
            found.append(row['id'])
        if len(rows) < page:
            return found
    raise SourceError('salesflare_window_limit')  # never claim a complete scan


def salesflare_feed(source, crm_id, kind, since, until, page=100, max_pages=10):
    items, before = [], until
    for _ in range(max_pages):
        rows = source.get(f'/accounts/{crm_id}/feed', {'types': kind, 'after': since.isoformat(), 'before': before.isoformat(), 'limit': page})
        if not isinstance(rows, list):
            raise SourceError('salesflare_invalid_feed')
        items.extend(rows)
        if len(rows) < page:
            return items
        stamps = [stamp for stamp in (salesflare_time_or_none(r.get('time')) for r in rows) if stamp]
        if not stamps:
            raise SourceError('salesflare_invalid_timestamp')
        oldest = min(stamps)
        if oldest >= before:
            raise SourceError('salesflare_feed_not_advancing')
        before = oldest
    raise SourceError('salesflare_feed_limit')


def salesflare_in_pipelines(source, crm_id, pipelines):
    for pipeline in pipelines:
        for closed in (None, 'true'):  # open and won/lost opportunities
            params = {'account': crm_id, 'pipeline': pipeline, 'limit': 1, 'details': 'false'}
            if closed:
                params['closed'] = closed
            rows = source.get('/opportunities', params)
            if not isinstance(rows, list):
                raise SourceError('salesflare_invalid_opportunities')
            if rows:
                return pipeline
    return None


SALESFLARE_APP = 'https://app.salesflare.com'


SALESFLARE_STUCK = dt.timedelta(hours=2)  # a round of accounts still going after this long: the card offers Restart


SALESFLARE_HICCUP = {500, 502, 503, 504}  # its gateway giving up on a slow query: retried, then set aside like a timeout


SALESFLARE_FEED_ROUTE = '/accounts/{id}/feed'


def salesflare_hiccup(error):
    """Salesflare or the network giving up on one request (a 5xx, a timeout): the same read soon after answers."""
    return error.category.startswith('network:') or error.status in SALESFLARE_HICCUP


# Every sync first checks that the key still belongs to the owner (/me). On a large team that read hangs now and then
# until Salesflare's gateway answers 504, like any other, and the sync failed for it though the key was confirmed
# minutes before. A key confirmed within this long goes on through such a hiccup. Only a hiccup: a refusal or another
# user still stops the sync, and a changed key is never taken as confirmed (its fingerprint, kept in memory only).
SALESFLARE_PROFILE_TRUSTED = 3600  # seconds
SALESFLARE_CONFIRMED = {}  # account id: (key fingerprint, time.monotonic() of its last confirmed /me)


def salesflare_confirm(source, account):
    fingerprint = getattr(source, 'key_fingerprint', lambda: None)()
    try:
        source.profile()
    except SourceError as error:
        seen = SALESFLARE_CONFIRMED.get(account['id'])
        age = time.monotonic() - seen[1] if seen else None
        if not (salesflare_hiccup(error) and fingerprint and seen and seen[0] == fingerprint
                and age < SALESFLARE_PROFILE_TRUSTED):
            raise
        LOG.warning('salesflare profile check skipped account=%s error=%s route=%s confirmed=%ds ago', account['id'],
                    error, error.route or '-', round(age))
        return
    if fingerprint:
        SALESFLARE_CONFIRMED[account['id']] = (fingerprint, time.monotonic())


# Salesflare refuses the feed for the whole team (a setting on its side, report s_f0d5d0200384ed92): every account of a
# round answers 403 on the feed while the key's user is part of it. Asking each account again every round changes
# nothing, so one account is asked until one read succeeds: every 10 minutes on the first day (the owner is likely
# getting it switched on), hourly after that. The warning about it is logged at most hourly either way.
SALESFLARE_FEED_RECHECK = dt.timedelta(hours=1)
SALESFLARE_FEED_RECHECK_EARLY = dt.timedelta(minutes=10)
SALESFLARE_FEED_EARLY = dt.timedelta(days=1)


def feed_recheck_every(off, stamp):
    """How long the feed, off since off['since'], waits between re-checks."""
    try:
        early = stamp - dt.datetime.fromisoformat(off['since']) < SALESFLARE_FEED_EARLY
    except (KeyError, TypeError, ValueError):
        early = False
    return SALESFLARE_FEED_RECHECK_EARLY if early else SALESFLARE_FEED_RECHECK


def feed_off_warns(off, stamp):
    """True when a re-check that found the feed still off may log its warning: at most one an hour (off['warned']), so
    the quicker re-checks of the first day are no louder than the hourly ones."""
    try:
        return stamp - dt.datetime.fromisoformat(off['warned']) >= SALESFLARE_FEED_RECHECK
    except (KeyError, TypeError, ValueError):
        return True


def feed_off_wait(state, stamp):
    """True while the feed is off for the team (state['feed_off']) and its next re-check isn't due. Restart sync on the
    card (next_full 0) re-checks right away."""
    off = state.get('feed_off')
    if not off or state.get('window') or ('next_full' in state and not state['next_full']):
        return False
    try:
        return stamp - dt.datetime.fromisoformat(off['checked']) < feed_recheck_every(off, stamp)
    except (KeyError, TypeError, ValueError):
        return False


def salesflare_progress(account, state):
    """The Salesflare card's sync details: the round of accounts being read (how far, since when), what it set aside,
    whether the owner stopped it (connector_sync), and where its API keys are."""
    window = state.get('window') or {}
    total, left = window.get('accounts', len(window.get('pending') or [])), len(window.get('pending') or [])
    started = window.get('until')
    try:
        stuck = bool(started) and dt.datetime.fromisoformat(now()) - dt.datetime.fromisoformat(started) > SALESFLARE_STUCK
    except (TypeError, ValueError):
        stuck = False
    last = state.get('last_round') or None
    done = max(0, total - left)
    # Without access: the last finished round's accounts (inaccessible_accounts, replaced when a round ends). During a
    # round it adds this round's new ones, never more than the round has. An older Machine's list (no last_round) only
    # ever grew, so a running round counts its own until it ends and replaces the list.
    current = window.get('no_access') or []
    if window:
        counted = set(state.get('inaccessible_accounts') or []) if last else set()
        no_access = min(total, len(counted | set(current)))
    else:
        no_access = last['no_access'] if last else len(state.get('inaccessible_accounts') or [])
    # It opens none of them: every account of the last round (or the first 10 of this one) refused. Nothing comes in
    # until the key changes, so the card asks for help instead of saying Connected.
    # Unless Salesflare refuses the feed for the whole team (feed_off): another key changes nothing then, and the card
    # says what does.
    feed_off = bool(state.get('feed_off'))
    if feed_off:
        locked = False
    elif last:
        locked = bool(last.get('accounts')) and not last.get('read') and last.get('no_access') == last.get('accounts')
    else:
        locked = done >= min(total, 10) > 0 and not window.get('read') and len(current) == done
    return {'stopped': state.get('stopped') or None, 'synced_until': state.get('watermark'),
            'round': {'since': window.get('since'), 'started': started, 'accounts': total, 'done': done, 'stuck': stuck,
                      'read': window.get('read'), 'failing': len(window.get('failures') or {})} if window else None,
            'last_round': last, 'no_access_all': locked, 'feed_off': feed_off,
            'slow_accounts': len(window['set_aside']) if 'set_aside' in window else last['set_aside'] if last else len(state.get('skipped_accounts') or []),
            'no_access': no_access,
            'keys_url': (account.get('app_base') or SALESFLARE_APP) + '/#/settings/apikeys'}


def sync_salesflare(store, config, account, source=None):
    state = store.checkpoint(account['id']) or {}
    if state.get('stopped'):  # the owner pressed Stop on its card: nothing is read until Start or Restart
        return {'mode': state.get('mode') or 'incremental', 'events': 0, 'stopped': True}
    source = source or Salesflare(config, account)
    salesflare_confirm(source, account)
    stamp = dt.datetime.now(dt.timezone.utc)
    if feed_off_wait(state, stamp):
        # Nothing to ask until the next re-check. The sync itself worked (the key reads its profile), so it counts.
        store.commit_page(account['id'], state, [])
        return {'mode': state.get('mode') or 'incremental', 'events': 0, 'feed_off': True, 'more': False}
    if not state.get('window'):
        days = config.get('bootstrap_days', 7)
        retained = stamp - dt.timedelta(days=days)
        # A re-check while the feed is off reads the whole week: once it opens, what came in meanwhile is picked up.
        full = not state.get('watermark') or stamp.timestamp() >= state.get('next_full', 0) or bool(state.get('feed_off'))
        since = retained if full else max(retained, dt.datetime.fromisoformat(state['watermark']) - dt.timedelta(hours=6))
        # Notes are often written days after a meeting, without changing its date, so
        # meetings are always reread over a full week; emails follow the incremental window.
        meeting_since = stamp - dt.timedelta(days=account.get('meeting_window_days', 7))
        email_ids = salesflare_recent_accounts(source, 'last_email_date', since)
        # Freeze the window and its account list, then work through it in committed batches.
        pending = list(dict.fromkeys(email_ids + salesflare_recent_accounts(source, 'last_meeting_date', meeting_since)))
        if state.get('feed_off'):
            state['feed_off']['checked'] = stamp.isoformat()  # this round is the re-check, whatever it finds
        state.update(mode='bootstrap' if not state.get('watermark') else 'incremental',
                     window={'since': since.isoformat(), 'meeting_since': meeting_since.isoformat(), 'until': stamp.isoformat(),
                             'full': full, 'pending': pending, 'email_ids': sorted(set(email_ids)), 'accounts': len(pending)})
        store.commit_page(account['id'], state, [], record_sync=False)
    window = state['window']
    since, until = dt.datetime.fromisoformat(window['since']), dt.datetime.fromisoformat(window['until'])
    meeting_since = dt.datetime.fromisoformat(window.get('meeting_since', window['since']))
    email_ids = set(window['email_ids']) if 'email_ids' in window else None  # older frozen windows: read both
    events, skipped, excluded, titles = [], 0, set(), []  # titles: each contact's job title in the CRM, a record about them
    batch = window['pending'][:account.get('accounts_per_batch', 5)]
    read_before, refused_before = window.get('read', 0), len(window.get('no_access') or [])
    for crm_id in batch:
        part_of = 'unread'  # what /accounts/{id} said of the key's user, counted when the feed is refused
        try:
            crm = source.get(f'/accounts/{crm_id}')
            crm = crm[0] if isinstance(crm, list) and crm else crm
            part_of = {True: 'true', False: 'false'}.get(crm.get('part_of'), 'missing') if isinstance(crm, dict) else 'missing'
            info, contacts = salesflare_context(account, crm)
            titles += [(['email:' + c['email']], {'title': c['role']}, enrichment.RECORD) for c in contacts.values() if c['email'] and c['role']]
            if crm.get('part_of') is False and account.get('join_pipelines'):
                pipeline = salesflare_in_pipelines(source, crm_id, account['join_pipelines'])
                if pipeline:
                    source.join_account(crm_id)
                    joined = state.setdefault('joined_accounts', [])
                    joined.append({'id': crm_id, 'pipeline': pipeline, 'at': now()})
                    state['joined_accounts'] = joined[-500:]
                    LOG.info('salesflare joined account=%s pipeline=%s', crm_id, pipeline)
            emails = salesflare_feed(source, crm_id, 'email', since, until) if email_ids is None or crm_id in email_ids else []
            meetings = [(k, item) for k in ('meeting-live', 'meeting-phone') for item in salesflare_feed(source, crm_id, k, meeting_since, until)]
        except SourceError as error:
            if salesflare_hiccup(error):
                # One slow account must not block the window: Salesflare's feed now and then hangs until its gateway
                # answers 504, and the same read a minute later answers at once (report s_f0d5d0200384ed92). So the
                # accounts read before it are kept, this one goes to the back of the round (never asked again right
                # away), and the batch goes on. After three failures it is set aside (visible). Two in a row without
                # an answer in between means Salesflare is down: the sync fails and waits its normal backoff.
                failures = window.setdefault('failures', {})
                failures[str(crm_id)] = failures.get(str(crm_id), 0) + 1
                window['pending'].remove(crm_id)
                if failures[str(crm_id)] < 3:
                    window['pending'].append(crm_id)
                else:
                    window['set_aside'] = window.get('set_aside', []) + [crm_id]
                    state['skipped_accounts'] = sorted(set(state.get('skipped_accounts', [])) | {crm_id})[-500:]
                window['hiccups'] = window.get('hiccups', 0) + 1
                LOG.warning('salesflare slow account error=%s route=%s try=%d in_a_row=%d', error, error.route or '-',
                            failures[str(crm_id)], window['hiccups'])
                if window['hiccups'] >= 2:
                    store.commit_page(account['id'], state, events, record_sync=False, excluded_source_ids=excluded)
                    raise
                continue
            window['pending'].remove(crm_id)
            window['hiccups'] = 0  # Salesflare answered
            if error.status not in (403, 404):
                window['pending'].insert(0, crm_id)  # not read: the next sync resumes at this one
                store.commit_page(account['id'], state, events, record_sync=False, excluded_source_ids=excluded)
                raise
            # No access to this account's timeline (or it was deleted). Visible, never
            # "fixed" by adding the owner to the account: ingestion stays read-only. Counted per round.
            refused = window.setdefault('no_access', [])
            if crm_id not in refused:
                refused.append(crm_id)
            if error.status == 403:
                # Refused on the feed though the key's user is part of the account: not about this account.
                if error.route == SALESFLARE_FEED_ROUTE and part_of == 'true':
                    window['feed_refused'] = window.get('feed_refused', 0) + 1
                    if state.get('feed_off'):
                        # The re-check: still off, and this one account answered for the team. The round is dropped,
                        # nobody else is asked, and the next re-check waits (feed_off_wait). One line per re-check:
                        # a warning at most hourly, the ones in between at INFO.
                        state['feed_off']['checked'] = stamp.isoformat()
                        state['next_full'] = stamp.timestamp()  # a Restart's re-check is done
                        state.pop('window')
                        level = logging.INFO
                        if feed_off_warns(state['feed_off'], stamp):
                            level, state['feed_off']['warned'] = logging.WARNING, stamp.isoformat()
                        LOG.log(level, 'salesflare feed off for team account=%s since=%s recheck=1 route=%s message=%s', account['id'],
                                state['feed_off'].get('since'), error.route, getattr(error, 'reason', None) or '-')
                        store.commit_page(account['id'], state, events, excluded_source_ids=excluded)
                        return {'mode': state.get('mode') or 'incremental', 'events': len(events), 'feed_off': True, 'more': False}
                window['refused'] = window.get('refused', 0) + 1
                # Counts only, for support (report s_f0d5d0200384ed92): did the account say the key's user is part of
                # it, which route refused, and what Salesflare's 403 said.
                detail = window.setdefault('refused_detail', {})
                key = f"part_of={part_of} route={error.route or '-'} message={getattr(error, 'reason', None) or '-'}"
                if key in detail or len(detail) < 10:
                    detail[key] = detail.get(key, 0) + 1
            continue
        window['pending'].remove(crm_id)
        window['read'], window['hiccups'] = window.get('read', 0) + 1, 0
        if state.pop('feed_off', None):  # one read succeeded: the feed is on again, and the round goes on as usual
            LOG.info('salesflare feed on again account=%s', account['id'])
        for item in emails:
            try:
                event = salesflare_email_event(account, info, contacts, item, config)
            except SourceError as error:
                # One unreadable record is skipped and logged; it never holds up the round.
                LOG.warning('salesflare skipped record account=%s crm_account=%s item=email:%s error=%s',
                            account['id'], crm_id, item.get('id'), error.category)
                continue
            events.append(event) if event else None
            skipped += event is None
            if event is None and email_subject_excluded(config, (item.get('email') or {}).get('subject')):
                excluded.add('email:' + str(item['id']))
        for _, item in meetings:
            try:
                event = salesflare_meeting_event(account, info, contacts, item)
            except SourceError as error:
                LOG.warning('salesflare skipped record account=%s crm_account=%s item=meeting:%s error=%s',
                            account['id'], crm_id, item.get('id'), error.category)
                continue
            events.append(event) if event else None
    # Counts only (no names or ids): the journal shows whether the key opens the accounts.
    LOG.info('salesflare batch read=%d no_access=%d left=%d', window.get('read', 0) - read_before,
             len(window.get('no_access') or []) - refused_before, len(window['pending']))
    if not window['pending']:
        # What this round could open: the card counts it (accounts read, without access) until the next one ends.
        no_access = window.get('no_access') or []
        state.update(mode='incremental', watermark=window['until'], inaccessible_accounts=sorted(no_access)[-500:],
                     skipped_accounts=sorted(window.get('set_aside') or [])[-500:],
                     last_round={'at': window['until'], 'accounts': window.get('accounts', 0), 'read': window.get('read', 0),
                                 'no_access': len(no_access), 'refused': window.get('refused', 0),
                                 'set_aside': len(window.get('set_aside') or [])})
        for key, count in sorted((window.get('refused_detail') or {}).items()):
            LOG.warning('salesflare refused account=%s count=%d %s', account['id'], count, key)
        if window.get('accounts') and not window.get('read') and len(no_access) == window['accounts']:
            # A warning, so it shows in the support report: the key reads its profile but no account's timeline.
            LOG.warning('salesflare round opened no account account=%s accounts=%d refused=%d missing=%d', account['id'],
                        window['accounts'], window.get('refused', 0), len(no_access) - window.get('refused', 0))
        if window['full']:
            state['next_full'] = stamp.timestamp() + 86400
        if window.get('accounts') and window.get('feed_refused', 0) == window['accounts']:
            # Every account asked was refused on the feed while the key's user is part of it: Salesflare has the feed
            # off for the whole team. From here one account is asked, now and then (feed_off_wait).
            state['feed_off'] = {'since': stamp.isoformat(), 'checked': stamp.isoformat(), 'warned': stamp.isoformat()}
            LOG.warning('salesflare feed off for team account=%s accounts=%d: one account is re-checked every %d min for a day, '
                        'then every %d min', account['id'], window['accounts'],
                        SALESFLARE_FEED_RECHECK_EARLY.total_seconds() // 60, SALESFLARE_FEED_RECHECK.total_seconds() // 60)
        state.pop('window')
    store.commit_page(account['id'], state, events, excluded_source_ids=excluded)
    involved = {'email:' + str(c.get('email')).lower() for e in events for c in e['metadata'].get('contacts') or ()}
    titles = [t for t in titles if t[0][0] in involved]  # only people in what was kept, as for their messages
    if titles:
        with store.connect() as db:
            enrichment.offer_facts(db, titles, 'salesflare', now())
    return {'mode': state['mode'], 'events': len(events), 'filtered': skipped, 'more': bool(state.get('window'))}
