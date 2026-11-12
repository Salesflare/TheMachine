"""Reading the owner's accounts: each account's collector with its lock and waits, a connector's sync, and what an
action-only connection may do. Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
from decimal import Decimal
import json
import re
import secrets
import sqlite3
import threading
import time

import enrichment
import graph
from machine.config import LOG, SIGNIN_ERROR
from machine.faults import db_busy, DB_BUSY_RETRY
from machine.sources.android import feed_backoff, sync_android, sync_android_preferred
from machine.sources.calendar import sync_calendar
from machine.sources.connectors import ABILITY_CHECK_SECONDS, BUILT_IN_SERVICES, CONNECTOR_HELPERS, load_connector
from machine.sources.gateway import sync_gateway
from machine.sources.gmail import sync_gmail
from machine.sources.rows import Skips
from machine.sources.salesflare import salesflare_progress, sync_salesflare
from machine.sources.slack import (Slack, slack_error, slack_event, slack_first_import_plan,
                                   slack_interval, slack_next_due, slack_order, slack_page_names, slack_prune,
                                   slack_read_asked, slack_limits, slack_read_drop, slack_read_now, slack_refused,
                                   slack_set_aside, slack_turn_done, slack_hiccup)
from machine.sources.telegram import sync_telegram
from machine.sources.whatsapp import sync_whatsapp, WhatsApp
from sources import CALENDAR_SERVICES, gog_signed_in_since, MAIL_SERVICES, rate_limited, SourceError, transient, upstream_busy
from timeutil import now
import whatsapp_images


SALESFLARE_RESTART_SPREAD = 180  # seconds: team Machines restarted together start their Salesflare rounds apart


def error_route(error):
    """ route=/accounts/{id}/feed when the source said which endpoint failed (ids masked), else nothing."""
    route = getattr(error, 'route', None)
    return f' route={route}' if route else ''


SALESFLARE_ROUND_SPREAD = 60  # seconds: and a fresh spread each round, so two whose starts landed close drift apart again


SYNC_LOCKS, SYNC_LOCKS_LOCK = {}, threading.Lock()


QUICK_RETRY_SECONDS = 15


QUICK_RETRY_MAX = 60  # a Retry-After longer than this waits in the checkpoint instead


SLACK_STUCK_AFTER = 5  # failed tries in a row at one conversation's read before the others get their turn


def slack_read_failed(store, config, account, state, channel, scan, params, error):
    """A conversation's history or replies read failed. True when the sync goes on without it; False when the caller
    raises the error, as for everything about the connection itself: the sign-in, a rate limit (its Retry-After and
    round stay as they are), Slack or the network down. Either way one conversation never keeps the turn for good."""
    label = slack_error(error)
    if (account.get('fair_incremental') and 'known_threads' in scan and
            scan['phase'] == 'threads' and error.category.startswith('network:')):
        # Save the failed frozen thread page, then let other conversations
        # progress. A repeated timeout cannot starve new channel messages.
        channel['deferred_thread'] = {'ts': params['ts'], 'oldest': params['oldest'], 'latest': params['latest'],
                                      'retry_at': time.time() + 600, 'error': str(error)}
        if scan.get('cursor'):
            channel['deferred_thread']['cursor'] = scan['cursor']
        channel.update(last_scan=scan['latest'], threads=scan['known_threads'],
                       next_thread_index=scan['thread_start'] + 1)
        state.pop('scan', None)
        state['index'] = (state['index'] + 1) % len(state['channels'])
        store.commit_page(account['id'], state, [], record_sync=False)
        error.retry_after = 65
    elif label == 'slack_invalid_cursor':
        scan.pop('cursor', None)
        store.commit_page(account['id'], state, [], record_sync=False)
    elif slack_refused(error) or label == 'slack_thread_not_found':
        # Slack refuses this conversation (the owner left it, or was removed): it says so and rests, and the turn
        # moves on. It used to stay the most overdue one, so every sync read it again and no other conversation was
        # read (2026-11-09). A partly read one is never marked complete: its last_scan stays where it was.
        slack_set_aside(config, channel, label)
        slack_read_drop(account['id'], channel['id'])  # a run's ask for it ends here: slack_read says it can't be read
        slack_turn_done(state)
        store.commit_page(account['id'], state, [], record_sync=False)
        LOG.warning('sync account=%s slack conversation set aside type=%s error=%s refused=%d', account['id'],
                    channel.get('type'), label, channel['refused'])
        # With none left that Slack lets it read, the connection itself says so.
        return not all(c.get('error') for c in state['channels'])
    elif slack_hiccup(error):
        # Slack or the network, as far as anyone can tell: the same page again next time. When it keeps failing at
        # this one conversation, the others get their turn and it comes back after its usual rest.
        scan['failed'] = int(scan.get('failed') or 0) + 1
        if scan['failed'] >= SLACK_STUCK_AFTER:
            channel['due'] = time.time() + slack_interval(config, channel)
            slack_read_drop(account['id'], channel['id'])
            slack_turn_done(state)
        store.commit_page(account['id'], state, [], record_sync=False)
    return False


def sync_slack(store, config, account, source=None):
    source = source or Slack(config, account)
    source.profile()
    state = store.checkpoint(account['id']) or {}
    if not state:
        state = {'mode': 'bootstrap', 'phase': 'discover', 'channels': [],
                 'after': f'{time.time() - config.get("bootstrap_days", 7) * 86400:.6f}'}
        store.commit_page(account['id'], state, [], record_sync=False)
    if state['phase'] == 'discover':
        params = {'user': account['user_id'], 'types': 'public_channel,private_channel,im,mpim',
                  'exclude_archived': 'true', 'limit': 100}
        if state.get('page_token'):
            params['cursor'] = state['page_token']
        else:
            state['listed'] = []  # every id Slack lists, from the first page on: only a complete list may drop one
        try:
            page = source.get('users.conversations', params)
        except SourceError as error:
            if slack_error(error) == 'slack_invalid_cursor':
                state.pop('page_token', None)
                store.commit_page(account['id'], state, [], record_sync=False)
            raise
        channels = {c['id']: c for c in state['channels']}
        if 'listed' in state:
            state['listed'] += [c['id'] for c in page.get('channels', [])]
        for c in page.get('channels', []):
            if c.get('is_archived'):
                continue
            # users.conversations is scoped to actual membership. Never join or open DMs.
            kind = 'dm' if c.get('is_im') else 'group' if c.get('is_mpim') else 'channel'
            channels.setdefault(c['id'], {'id': c['id'], 'name': c.get('name') or
                ('My notes' if c.get('user') == account['user_id'] else 'DM ' + c.get('user', c['id'])),
                'type': kind, 'threads': []})
            # Slack Connect: shared with another company. Everything else is the company's own Slack, among colleagues.
            if c.get('is_ext_shared') or c.get('is_pending_ext_shared'):
                channels[c['id']]['external'] = True
            else:
                channels[c['id']].pop('external', None)
        state['channels'] = list(channels.values())
        cursor = page.get('response_metadata', {}).get('next_cursor')
        if cursor:
            state['page_token'] = cursor
        else:
            state.pop('page_token', None)
            state['next_discovery'] = time.time() + 86400
            slack_prune(state, state.pop('listed', None))
            if state['mode'] == 'bootstrap' and 'index' not in state:
                # First import: a cheap look at every conversation first, so the read order follows activity.
                state.update(phase='triage', triage=0)
            else:
                slack_order(state['channels'])
                state.update(phase='scan', index=0)
        store.commit_page(account['id'], state, [])
        return {'mode': state['mode'], 'events': 0, 'more': True}

    if (state['mode'] == 'bootstrap' and state['phase'] == 'scan' and 'step' not in state and not state.get('scan')
            and state.get('channels') and isinstance(source, Slack)):
        # A first import begun in the old name order: the rest of it follows activity. Conversations already read
        # stay read.
        state.update(phase='triage', triage=0)
        store.commit_page(account['id'], state, [], record_sync=False)

    if state['phase'] == 'triage':
        # conversations.info isn't held to Slack's one-read-a-minute limit. A direct message shows its newest
        # message; a channel or group only when you last read it, which stands in for its activity.
        for _ in range(10):
            if state['triage'] >= len(state['channels']):
                break
            channel = state['channels'][state['triage']]
            try:
                info = source.get('conversations.info', {'channel': channel['id']}).get('channel') or {}
            except SourceError as error:
                if not slack_refused(error):
                    store.commit_page(account['id'], state, [], record_sync=False)
                    raise
                info = {}  # one conversation Slack won't show: read with the quiet ones, never holding up the plan
            latest = info.get('latest') if isinstance(info.get('latest'), dict) else {}
            mark = latest.get('ts') if channel['type'] == 'dm' else info.get('last_read')
            try:
                channel['hint'] = float(mark or 0)
            except (TypeError, ValueError):
                channel['hint'] = 0.0
            state['triage'] += 1
        if state['triage'] >= len(state['channels']):
            slack_first_import_plan(config, state)
        store.commit_page(account['id'], state, [], record_sync=False)
        return {'mode': state['mode'], 'events': 0, 'more': True}

    if not state['channels']:
        state.update(mode='incremental', phase='discover')
        store.commit_page(account['id'], state, [], record_sync=False)
        return {'mode': 'incremental', 'events': 0, 'more': False}
    if state['mode'] == 'incremental' and not state.get('scan') and not slack_next_due(store, config, account, source, state):
        return {'mode': 'incremental', 'events': 0, 'more': False}
    channel = state['channels'][state['index']]
    scan = state.get('scan')
    if not scan:
        # Six-hour overlap catches recent edits; daily retained-window replay catches older
        # edits and thread metadata. No timestamp advances before every page commits.
        full = not channel.get('last_scan') or time.time() >= channel.get('next_full', 0)
        # The retained window rolls forward; state['after'] (first install) only bounds it.
        retained = max(Decimal(state['after']),
                       Decimal(f'{time.time() - config.get("bootstrap_days", 7) * 86400:.6f}'))
        oldest = str(retained) if full else str(max(retained, Decimal(channel['last_scan']) - Decimal(21600)))
        latest = f'{time.time():.6f}'
        step = state.get('step')
        if step == 'recent':
            # First import, active conversations: the last day first; the rest of the window comes after.
            oldest, full = str(max(retained, Decimal(f'{time.time() - 86400:.6f}'))), False
            deepen_to = oldest if Decimal(oldest) > retained else None
        elif step == 'deepen' and channel.get('deepen'):
            oldest, latest = str(retained), channel['deepen']
        # Known threads are polled for late replies only while reasonably recent; the
        # list otherwise grows forever and is rewritten on every page commit.
        horizon = time.time() - config.get('slack_thread_retention_days', 30) * 86400
        channel['threads'] = [ts for ts in channel.get('threads', []) if float(ts) >= horizon]
        scan = {'oldest': oldest, 'latest': latest, 'phase': 'history',
                'thread_index': 0, 'threads': list(channel.get('threads', [])), 'full': full}
        if step:
            scan['step'] = step
            if step == 'recent' and deepen_to:
                scan['deepen_to'] = deepen_to
        if channel.get('threads_waiting'):
            # Threads left for later on the first pass: read them now over the whole window.
            scan.update(thread_oldest=str(retained), thread_latest=f'{time.time():.6f}')
        elif account.get('fair_incremental') and channel.get('last_scan') and not step:
            # One old thread per channel turn, not its entire retained history.
            # Preserve all known threads and rotate durably on completed scans.
            scan['known_threads'] = list(scan['threads'])
            scan['thread_start'] = channel.get('next_thread_index',0)
            scan['threads'] = []
        state['scan'] = scan
        store.commit_page(account['id'], state, [], record_sync=False)
    params = {'channel': channel['id'], 'oldest': scan['oldest'], 'latest': scan['latest'],
              'inclusive': 'true', 'limit': slack_limits(account)['page']}
    if scan['phase'] == 'threads':
        params['ts'] = scan['threads'][scan['thread_index']]
        if scan.get('thread_oldest'):
            params.update(oldest=scan['thread_oldest'],latest=scan['thread_latest'])
    if scan.get('cursor'):
        params['cursor'] = scan['cursor']
    gone_thread = False
    try:
        page = source.get('conversations.history' if scan['phase'] == 'history' else 'conversations.replies', params)
        if page.get('has_more') and not page.get('response_metadata', {}).get('next_cursor'):
            raise SourceError('slack_missing_cursor')
    except SourceError as error:
        if slack_error(error) == 'slack_thread_not_found' and scan['phase'] == 'threads':
            # The thread is gone (its first message was deleted): it leaves the list and the conversation reads on.
            # It used to fail the conversation on every turn, with the thread still in its list.
            gone_thread, page = True, {}
            channel['threads'] = [ts for ts in channel.get('threads', []) if ts != params['ts']]
            if params['ts'] in scan.get('known_threads', []):
                scan['known_threads'].remove(params['ts'])
        elif slack_read_failed(store, config, account, state, channel, scan, params, error):
            return {'mode': state['mode'], 'events': 0, 'more': True}
        else:
            raise
    scan.pop('failed', None)
    names = slack_page_names(store, channel, page.get('messages', []))
    skipped = Skips('slack_invalid_message')  # a message it can't take is counted, never failing the channel's page
    def one(raw):
        if raw.get('subtype') == 'message_deleted':
            return store.tombstone(account['id'], channel['id'] + ':' + raw['deleted_ts'])
        e = slack_event(account, channel, raw, names)
        ts = e['metadata']['message_ts']
        channel['last_activity'] = max(float(channel.get('last_activity') or 0), float(ts))
        if e['metadata']['reply_count'] and ts not in scan['threads']:
            scan['threads'].append(ts)
            if 'known_threads' in scan and ts not in scan['known_threads']:
                scan['known_threads'].append(ts)
        return e
    events = [e for e, _ in skipped.every(page.get('messages', []), one) if e]
    cursor = page.get('response_metadata', {}).get('next_cursor')
    if cursor:
        scan['cursor'] = cursor
    else:
        scan.pop('cursor', None)
        if scan['phase'] == 'history':
            scan['phase'] = 'threads'
            if state['mode'] == 'bootstrap' and len(state['channels']) > 1 and scan['threads']:
                # First pass: every conversation's own messages before any thread replies. Slack
                # allows about one read a minute, so one busy channel's threads would otherwise
                # hold up all the others for hours. The next turn of this channel reads them.
                scan['waiting'], scan['threads'] = scan['threads'], []
            elif 'known_threads' in scan:
                known = scan['known_threads']
                selected = scan['threads'][:1]
                if not selected and known:
                    selected = [known[scan['thread_start'] % len(known)]]
                postponed = channel.get('deferred_thread')
                if postponed and time.time() < postponed['retry_at']:
                    selected = []
                if postponed and time.time() >= postponed['retry_at']:
                    scan['threads'] = [postponed['ts']]
                    scan['thread_oldest'], scan['thread_latest'] = postponed['oldest'], postponed['latest']
                    if postponed.get('cursor'):
                        scan['cursor'] = postponed['cursor']
                    selected = scan['threads']
                scan['threads'] = selected
        else:
            if gone_thread:
                scan['threads'].pop(scan['thread_index'])
            else:
                scan['thread_index'] += 1
            postponed = channel.get('deferred_thread')
            if postponed and params.get('ts') == postponed['ts']:
                channel.pop('deferred_thread',None)
        if scan['thread_index'] >= len(scan['threads']):
            if scan.get('step') == 'deepen' and channel.get('deepen'):
                # The older part of the window: the newest read (last_scan) stays where it was.
                channel.pop('deepen')
                channel['threads'] = list(dict.fromkeys(channel.get('threads', []) + scan['threads'] + scan.get('waiting', [])))
            else:
                channel.update(last_scan=scan['latest'], threads=scan.get('known_threads', scan['threads'] + scan.get('waiting', [])))
                if scan.get('deepen_to'):
                    channel['deepen'] = scan['deepen_to']
            if scan.get('waiting'):
                channel['threads_waiting'] = True
            else:
                channel.pop('threads_waiting', None)
            if 'known_threads' in scan:
                channel['next_thread_index'] = scan['thread_start'] + 1
            channel.pop('error', None)
            channel.pop('refused', None)
            # Thread replies held back on the first pass are read on the very next round.
            channel['due'] = time.time() + (0 if scan.get('waiting') else slack_interval(config, channel))
            if scan['full']:
                channel['next_full'] = time.time() + 86400
            slack_turn_done(state)
    if not state.get('titles_named'):  # once: titles stored before members were named in them
        store.name_slack_titles(account['id'])
        state['titles_named'] = True
    skipped.check().note(state)
    store.commit_page(account['id'], state, events)
    if isinstance(source, Slack):
        remember_slack_names(store, source, events, state.get('channels') or ())
    more = state['mode'] != 'incremental' or state['index'] != 0 or bool(state.get('scan'))
    return {'mode': state['mode'], 'events': len(events), 'more': more, 'skipped': sum(skipped.values())}


def remember_slack_names(store, source, events, channels=(), per_page=3):
    """Names and emails for the people graph: Slack messages carry only user IDs. A few lookups per
    page (new senders, people they mention, then the people behind known DMs), each once a month; the email joins the
    person to their mail. Whether each is outside the company's own Slack (another company's member through Slack
    Connect, or a guest) is kept too (slack_members): shared_graph.visibility shares on it. Titles with a member's id
    are written again with the name once it is known. Best effort."""
    users = {e['metadata'].get('user_id') for e in events} | {
        m[0] for e in events for m in graph.SLACK_MENTION.findall(str(e.get('body') or ''))} | {
        m[1] for name in [e['metadata'].get('channel_name') for e in events] + [c.get('name') for c in channels]
        for m in [re.fullmatch(r'DM ([UW][A-Z0-9]+)', name or '')] if m}
    owner = source.account.get('user_id')
    users = {u for u in users if u}
    with store.connect() as db:
        known = graph.slack_members_known(db, users)
    wanted = sorted(set(store.names_to_check(['slack:' + u for u in users - {owner}])) | {'slack:' + u for u in users - known})
    named = []
    for identifier in wanted[:per_page]:
        member = identifier.split(':', 1)[1]
        try:
            user = source.get('users.info', {'user': member}).get('user', {})
        except SourceError as error:
            if str(error).startswith('slack_invalid_response'):
                continue  # Slack's answer for this one member made no sense: the others are still looked up
            if not str(error).startswith(('slack_user_not_found', 'slack_user_not_visible')):
                return  # away, or Slack's limit: the rest next page
            user = {'id': member, 'deleted': True}  # an account Slack no longer has
        profile = user.get('profile') or {}
        shown = (profile.get('real_name') or profile.get('display_name') or user.get('real_name')
                 or profile.get('real_name_normalized') or profile.get('display_name_normalized') or user.get('name'))
        person = not user.get('is_bot') and member != owner and not user.get('deleted')
        email = str(profile.get('email') or '').lower()[:320] or None
        if member != owner:  # a person's name and email for the people graph (an app: none, checked once a month)
            real = None if user.get('is_bot') else (profile.get('real_name') or profile.get('display_name') or user.get('real_name'))
            store.remember_name(identifier, real and str(real)[:200], None if user.get('is_bot') else email)
        # who is no person in the graph still has a name to show: an app by its name, the owner as themselves, someone
        # whose account is gone by the name it had, else "a former Slack user"
        label = None if person else (shown or (graph.FORMER_SLACK_USER if user.get('deleted') else None))
        team = source.account.get('team_id')
        outside = bool(user.get('is_stranger') or user.get('is_restricted') or user.get('is_ultra_restricted')
                       or (team and user.get('team_id') and user['team_id'] != team))
        with store.connect() as db:
            graph.remember_slack_member(db, member, outside, now(), label)
        if shown or label:
            named.append(member)
        if member == owner or (user.get('deleted') and not profile):
            continue  # the owner's own picture and facts aren't a contact's
        user = {**user, 'id': user.get('id') or member}
        offer, facts = enrichment.slack_photo(user), enrichment.slack_facts(user)
        if offer or facts:
            with store.connect() as db:
                enrichment.offer_photos(db, [offer], 'slack', now(), known_only=False) if offer else None
                enrichment.offer_facts(db, [facts], 'slack', now()) if facts else None
    if named and source.account.get('id'):
        store.name_slack_titles(source.account['id'], named)


def sync_source(store, config, account):
    service = account.get('service', 'gmail')
    if service in MAIL_SERVICES:
        return sync_gmail(store, config, account)
    if service in CALENDAR_SERVICES:
        return sync_calendar(store, config, account)
    if service == 'slack':
        return sync_slack(store, config, account)
    if service == 'whatsapp':
        return sync_whatsapp(store, config, account)
    if service == 'telegram':
        return sync_telegram(store, config, account)
    if service == 'salesflare':
        return sync_salesflare(store, config, account)
    if service == 'gateway':
        return sync_gateway(store, config, account)
    if service == 'android':
        return sync_android_preferred(store, config, account) if account['transport'] == 'openclaw-feed' else sync_android(store, config, account)
    plugin = load_connector(service)
    if plugin is None:
        raise SourceError('unsupported_service')
    return plugin.sync(store, config, account, CONNECTOR_HELPERS)


class SyncApp:
    ACTIONS = {'slack_read': 'slack_read_action'}  # its other actions are still App.action's own branches

    def slack_read_action(self, name, args, owner_dashboard=False):
        """A to-do's run asks for a Slack conversation's newest messages (assistant_signals slack_read {channel}): through
        the Slack connection, never the browser. Slack allows about one read a minute, so the read happens in the
        collector's next turn, ahead of every other conversation, and the run asks again until it is in. status: 'read'
        with the conversation's newest collected messages (event_ids, read with events), 'reading' (ask again in about
        a minute), 'cannot_read' (the owner isn't in it, or Slack refused), 'not_found' with the conversations there
        are, or 'not_connected': the run then records its blocker with connect:'slack', so the to-do offers Connect Slack.
        Read-only: nothing is joined, opened or marked read."""
        wanted = str(args.get('channel') or '').strip()
        wanted = re.sub(r'^(?:slack:)?#?', '', wanted)
        if not wanted:
            raise ValueError('Give channel: the conversation\'s id (C0…, D0…) or its name (#name)')
        accounts = [a for a in self.config.get('accounts') or [] if a.get('service') == 'slack'
                    and (not args.get('account_id') or a.get('id') == args['account_id'])]
        if not accounts:
            return {'status': 'not_connected', 'connect': 'slack',
                    'note': 'Slack is not connected. Record the blocker with connect:\'slack\': the to-do offers Connect Slack, '
                            'and carries on by itself once it is connected. Never the browser for it.'}
        names = []
        for account in accounts:
            state = self.store.checkpoint(account['id']) or {}
            channels = state.get('channels') or []
            names += ['#' + c['name'] if c.get('type') == 'channel' else c['name'] for c in channels]
            channel = next((c for c in channels if c['id'] == wanted), None) or next(
                (c for c in channels if str(c.get('name') or '').lower() == wanted.lower()), None)
            if not channel:
                continue
            if channel.get('error') and not slack_read_asked(account['id'], channel):
                slack_read_drop(account['id'], channel['id'])
                return {'status': 'cannot_read', 'account_id': account['id'], 'error': channel['error'],
                        'note': 'Slack refused this conversation to their sign-in (they may have left it). Say so plainly '
                                'and ask for what you need from it.'}
            last = float(channel.get('last_scan') or 0)
            asked = slack_read_now(account['id'], channel['id'])
            if last >= asked:  # its read started after the ask: a message from a minute before it is in
                slack_read_drop(account['id'], channel['id'])
                with self.store.connect() as db:
                    found = [r['id'] for r in db.execute(
                        "SELECT id FROM events WHERE account_id=? AND deleted=0 AND substr(source_id,1,?)=? "
                        'ORDER BY occurred_at DESC LIMIT 20', (account['id'], len(channel['id']) + 1, channel['id'] + ':'))]
                return {'status': 'read', 'account_id': account['id'], 'channel': channel['name'], 'event_ids': found,
                        'note': 'Read them with events {account_ids:[' + json.dumps(account['id']) + '], event_ids}; newest first.'
                        + ('' if found else ' Nothing in it in the last week.')}
            wakes = self.__dict__.get('collector_wakes') or {}
            if account['id'] in (self.__dict__.get('collector_resting') or ()) and account['id'] in wakes:
                wakes[account['id']].set()
            return {'status': 'reading', 'account_id': account['id'], 'channel': channel['name'], 'wait_seconds': 90,
                    'note': 'Slack allows about one read a minute: the Slack connection reads it next. Call slack_read '
                            'again in about a minute (sleep 60 with exec), up to a few times.'}
        if not names:
            return {'status': 'reading', 'wait_seconds': 120,
                    'note': 'Slack is still bringing in its first conversations. Call slack_read again in a few minutes.'}
        return {'status': 'not_found', 'conversations': sorted(set(names))[:50],
                'note': 'No conversation by that name or id in their Slack. Pick one of these, or say plainly what you '
                        'could not find.'}

    def started_at(self):
        """When this Machine started: `started_at` in the config (a hosted machine's signup), else its first own activity."""
        given = str(self.config.get('started_at') or '')
        if given:
            return given
        if getattr(self, '_started_at', None):  # found once, it stays: the poll asked each time, two passes over big tables
            return self._started_at
        with self.store.connect() as db:
            row = db.execute("SELECT MIN(t) FROM (SELECT MIN(started_at) t FROM analyses UNION ALL SELECT MIN(created_at) FROM suggestions"
                             " UNION ALL SELECT MIN(at) FROM sync_activity UNION ALL SELECT MIN(day) FROM sync_daily)").fetchone()
        self._started_at = row[0] if row and row[0] else None
        return self._started_at

    def resume_wait(self, account):
        """Seconds until a slow source (polled every 10 minutes or less often: LinkedIn, X, CRM) is due
        again after a restart. A restart alone must not cost an extra read; catch-up and new accounts go now.
        Salesflare too, whatever its poll: a round starts with its account lists ordered by activity, which run close
        to Salesflare's 2-minute gateway limit on a large team. A release restarts a team's Machines together, and
        each one starting that list at the same second answered 504 (HTTP gateway timeout), so after a finished
        round it waits out its gap plus a random spread. One mid-round goes now: its list is already read."""
        delay = account.get('poll_seconds', self.config.get('poll_seconds', 300))
        crm = account.get('service') == 'salesflare'
        if delay < 600 and not crm:
            return 0
        state = self.store.checkpoint(account['id']) or {}
        with self.store.connect() as db:
            row = db.execute('SELECT last_success FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
        unfinished = state.get('page_token') or state.get('catchup') or state.get('coverage_complete') is False
        if not row or not row['last_success'] or not state or state.get('mode') != 'incremental' or (unfinished and account.get('service') != 'x') \
                or (crm and state.get('window')):
            return 0
        since = (dt.datetime.fromisoformat(now()) - dt.datetime.fromisoformat(row['last_success'])).total_seconds()
        return max(0, min(delay, delay - since)) + (secrets.randbelow(SALESFLARE_RESTART_SPREAD + 1) if crm else 0)

    def wait_for_retry(self, account, row):
        """Wait until the checkpoint's retry time; True when stopping. An expired Google sign-in
        is retried as soon as the owner signs in again, instead of after the full hour."""
        expired = bool(re.search(SIGNIN_ERROR, row['error'] or ''))
        while True:
            seconds = (dt.datetime.fromisoformat(row['retry_at']) - dt.datetime.fromisoformat(now())).total_seconds()
            if seconds <= 0:
                return False
            if expired and gog_signed_in_since(self.config, account, row['error_at']):
                LOG.info('sync account=%s signed in again, retrying now', account['id'])
                with self.store.connect() as db:
                    db.execute('UPDATE checkpoints SET retry_at=NULL WHERE account_id=?', (account['id'],))
                return False
            if self.stop.wait(min(seconds, 15) if expired else seconds):
                return True

    def sync_lock(self, account_id):
        """One sync of an account at a time: its collector, and a read right after a calendar change (sync_soon)."""
        with SYNC_LOCKS_LOCK:
            return SYNC_LOCKS.setdefault(account_id, threading.Lock())

    def ability_checker(self, account):
        """An action-only connection (Brings in signals off): nothing is read, but what it may do (a Docs connection's
        reads and writes, from its consent) is checked now and every ABILITY_CHECK_SECONDS, for its card."""
        plugin = load_connector(account.get('service', '')) if account.get('service') not in BUILT_IN_SERVICES else None
        refresh = getattr(plugin, 'refresh', None)
        while refresh and not self.stop.is_set():
            try:
                refresh(self.store, self.config, account, CONNECTOR_HELPERS)
            except Exception as error:  # noqa: BLE001 - the card keeps what it knew
                LOG.warning('ability check account=%s error=%s', account['id'], type(error).__name__)
            if self.stop.wait(ABILITY_CHECK_SECONDS):
                break

    def slack_source(self, account):
        """The one Slack client of a connection: its collector and its history (machine/app/history.py) share it, so
        they share its pacing too (Slack allows about one history read a minute)."""
        sources = self.__dict__.setdefault('slack_sources', {})
        found = sources.get(account['id'])
        if found is None or found.account != account:
            found = sources[account['id']] = Slack(self.config, account, self.stop)
        return found

    def collector(self, account):
        source = self.slack_source(account) if account.get('service') == 'slack' else None
        try:
            wait = self.resume_wait(account)
        except Exception as error:  # never keep a source from starting
            LOG.warning('resume_wait account=%s error=%s', account['id'], type(error).__name__)
            wait = 0
        if wait:
            LOG.info('sync account=%s resumes in %ds (last read before the restart)', account['id'], wait)
            if self.stop.wait(wait):
                return
        while not self.stop.is_set():
            try:
                with self.store.connect() as db:
                    row = db.execute('SELECT retry_at,error,error_at,failures FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
                local_android_feed = account.get('service') == 'android' and account.get('transport') == 'openclaw-feed'
                if row and row['retry_at'] and not local_android_feed:
                    if self.wait_for_retry(account, row):
                        break
                delay = account.get('poll_seconds', self.config.get('poll_seconds', 300))
                try:
                    result = self.sync_retrying(account, source)
                    LOG.info('sync account=%s mode=%s read=%d filtered=%d skipped=%d', account['id'], result['mode'], result['events'], result.get('filtered', 0), result.get('skipped', 0))
                    state = self.store.checkpoint(account['id'])
                    if not result.get('stopped') and (result.get('more') or state.get('mode', result['mode']) != 'incremental' or state.get('page_token')):  # a plugin's checkpoint may not keep a mode
                        delay = account.get('poll_seconds', 3600) if account.get('service') == 'x' else 30 if account.get('service') == 'linkedin' else 0 if source else 5
                    elif account.get('service') == 'salesflare':
                        # A finished round: the next one opens with the slow account lists. Rounds of teammates' Machines
                        # take about as long, so two that started close stay together for hours (both answered 504 in a
                        # regular round, 41 minutes after a shared restart). A fresh spread each round breaks that up.
                        delay += secrets.randbelow(SALESFLARE_ROUND_SPREAD + 1)
                except SourceError as error:
                    if self.stop.is_set():
                        break
                    delay = error.retry_after or delay
                    if local_android_feed:
                        # The local queue is read again with a growing wait while the bridge stays down, not every
                        # poll (feed_backoff). Phone fallback attempts keep their own durable cap.
                        delay = feed_backoff(account, row['failures'] if row else 0)
                    error.retry_after = delay
                    self.store.failed(account['id'], error)
                    LOG.warning('sync account=%s error=%s%s', account['id'], error, error_route(error))
                    # Enter the checkpoint wait directly so renewed sign-ins are watched.
                    # Ordinary failures and rate limits retain their normal backoff.
                    if re.search(SIGNIN_ERROR, str(error)):
                        continue
                except sqlite3.OperationalError as error:
                    if not db_busy(error):
                        safe = SourceError(type(error).__name__, retry_after=delay)
                        self.store.failed(account['id'], safe)
                        LOG.error('sync account=%s error=%s', account['id'], safe)
                    else:  # another writer held the database past the busy timeout: transient, read again soon
                        LOG.info('sync account=%s waits: database busy', account['id'])
                        delay = DB_BUSY_RETRY
                except Exception as error:
                    safe = SourceError(type(error).__name__, retry_after=delay)
                    self.store.failed(account['id'], safe)
                    LOG.error('sync account=%s error=%s', account['id'], safe)
            except Exception as error:
                # A database error here (locked, disk full) must never end this
                # account's thread silently while /health stays green.
                LOG.error('collector account=%s internal_error=%s', account['id'], type(error).__name__)
                delay = 60
            self.__dict__.setdefault('collector_reads', {})[account['id']] = time.time()  # a read ended (Check now waits for it)
            self.collector_rest(account['id'], delay)

    def connector_sync(self, args):
        """Stop, Start or Restart on a Salesflare card. Stop: nothing is read until Start, which goes on where it was.
        Restart: the round of accounts it was on is dropped, with its errors and wait, and a new one reads the last
        week again now (a round stuck on slow or failing accounts). What it brought in stays either way."""
        account = next((a for a in self.config['accounts'] if a['id'] == args.get('account')), None)
        if not account or account.get('service') != 'salesflare':
            raise ValueError('Only a Salesflare connection can be stopped or restarted here')
        do = args.get('do')
        if do not in ('stop', 'start', 'restart'):
            raise ValueError('Choose stop, start or restart')
        lock = self.sync_lock(account['id'])
        if not lock.acquire(timeout=20):
            raise ValueError('It is reading a batch of accounts. Try again in a minute')
        try:
            with self.store.connect() as db:
                row = db.execute('SELECT state FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
                state = json.loads(row['state'] or '{}') if row else {}
                if do == 'stop':
                    state['stopped'] = now()
                else:
                    state.pop('stopped', None)
                if do == 'restart':
                    state.pop('window', None)
                    state['next_full'] = 0
                db.execute('INSERT INTO checkpoints(account_id,state) VALUES(?,?) ON CONFLICT(account_id) DO UPDATE SET state=excluded.state'
                           + ('' if do == 'stop' else ',error=NULL,retry_at=NULL,failures=0'), (account['id'], json.dumps(state)))
        finally:
            lock.release()
        LOG.info('connector_sync account=%s do=%s', account['id'], do)
        if do != 'stop':
            self.sync_soon(account['id'])
        return {'ok': True, 'do': do, 'salesflare': salesflare_progress(account, state)}

    def connector_contact_sync(self, args):
        """Update contact details on a Salesforce card (connectors/salesforce.py, crm_sync.py): preview reads what it
        would change now and writes nothing; on needs a preview from the last half hour (the owner saw it first); off
        stops it. Kept in the connection's checkpoint, like Stop."""
        import crm_sync
        account = next((a for a in self.config['accounts'] if a['id'] == args.get('account')), None)
        if not account or account.get('service') != 'salesforce':
            raise ValueError('Only a Salesforce connection updates contact details')
        if account.get('shared'):
            raise ValueError('A connection your Fleet shares only reads')
        do = args.get('do')
        if do not in ('preview', 'on', 'off'):
            raise ValueError('Choose preview, on or off')
        plugin = load_connector('salesforce')
        if do == 'preview':
            try:
                shown, _ = plugin.preview(self.store, self.config, account, CONNECTOR_HELPERS)
            except SourceError as error:
                raise ValueError(f'Salesforce did not answer ({error.category}). Try again in a minute') from None
        lock = self.sync_lock(account['id'])
        if not lock.acquire(timeout=20):
            raise ValueError('It is reading Salesforce. Try again in a minute')
        try:
            with self.store.connect() as db:
                row = db.execute('SELECT state FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
                state = json.loads(row['state'] or '{}') if row else {}
                if do == 'preview':
                    state['contact_preview_at'] = now()
                elif do == 'on':
                    if not crm_sync.preview_fresh(state, now()):
                        raise ValueError('Look at what would change first')
                    state.update(contact_sync=now())
                    state.pop('contact_sync_at', None)  # the first round goes now
                else:
                    state.pop('contact_sync', None)
                db.execute('INSERT INTO checkpoints(account_id,state) VALUES(?,?) ON CONFLICT(account_id) DO UPDATE SET state=excluded.state',
                           (account['id'], json.dumps(state)))
        finally:
            lock.release()
        LOG.info('connector_contact_sync account=%s do=%s', account['id'], do)
        if do == 'on':
            self.sync_soon(account['id'])
        return {'ok': True, 'do': do, **({'changes': shown} if do == 'preview' else {}), 'crm': plugin.card(account, state)}

    def sync_retrying(self, account, source=None):
        """One sync of the account; when the service answers 429 or a transient 5xx, one more try shortly after (its
        Retry-After when that is short, else QUICK_RETRY_SECONDS). A second failure goes to the caller. Not for Slack's
        rate limit: its reads keep their own round (Slack.read_went), and a quick extra read would spend the next one."""
        for attempt in (0, 1):
            try:
                with self.sync_lock(account['id']):
                    return sync_slack(self.store, self.config, account, source) if source else sync_source(self.store, self.config, account)
            except SourceError as error:
                wait = error.retry_after or QUICK_RETRY_SECONDS
                if attempt or not upstream_busy(error) or (source and rate_limited(error)) or wait > QUICK_RETRY_MAX \
                        or self.stop.is_set():
                    raise
                LOG.info('sync account=%s service busy (%s%s), retrying in %ds', account['id'], error, error_route(error), wait)
                if self.stop.wait(wait):
                    raise

    def sync_soon(self, account_id):
        """Read this calendar again now instead of at its next poll, so a change shows in the Calendar in seconds."""
        account = next((a for a in self.config.get('accounts', []) if a.get('id') == account_id), None)
        if not account:
            return

        def read():
            try:
                with self.sync_lock(account_id):
                    sync_source(self.store, self.config, account)
            except Exception as error:  # noqa: BLE001 - the next poll reads it anyway
                LOG.warning('sync_soon account=%s error=%s', account_id, type(error).__name__)
        threading.Thread(target=read, name='sync-soon-' + account_id, daemon=True).start()

    def whatsapp_source(self, account):
        """The WhatsApp source of one of the owner's connections (whatsapp_images_app fetches photos through it)."""
        return WhatsApp(self.config, account)

    def whatsapp_photo_event(self, account_id, source_id):
        """A message whose photo was kept or read, with the photo joined in (whatsapp_images.with_photo), the way its next
        sync builds it: a new version, so the review reads what the photo says."""
        with self.store.connect() as db:
            row = db.execute('SELECT kind,occurred_at,title,body,metadata,deleted FROM events WHERE account_id=? AND source_id=?',
                             (account_id, source_id)).fetchone()
            photo = db.execute('SELECT * FROM whatsapp_photos WHERE account_id=? AND source_id=?', (account_id, source_id)).fetchone()
        if not row or not photo or row['kind'] != 'whatsapp.message':
            return False
        event = {'account_id': account_id, 'source_id': source_id, 'kind': row['kind'], 'occurred_at': row['occurred_at'], 'title': row['title'],
                 'body': whatsapp_images.base_body(row['body']), 'metadata': json.loads(row['metadata']), 'deleted': bool(row['deleted'])}
        self.store.commit_page(account_id, None, [whatsapp_images.with_photo(event, dict(photo))], record_sync=False)
        return True
